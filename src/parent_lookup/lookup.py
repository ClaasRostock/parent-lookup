"""Core module. Contains the decorators and functions providing the parent lookup functionality."""

# pyright: reportArgumentType=false

from __future__ import annotations

import contextlib
import inspect
import logging
import typing
import weakref
from collections.abc import Callable
from types import GenericAlias
from typing import Any, NamedTuple, TypeVar, cast, overload

from typing_inspect import get_origin

logger: logging.Logger = logging.getLogger(__name__)

TParent = TypeVar("TParent")
TChild = TypeVar("TChild")
_TLookupFunction = Callable[[TParent], list[TChild]] | Callable[[TParent], TChild]
TFunc = TypeVar("TFunc")


class _BoundLookupFunction(NamedTuple):
    parent: weakref.ReferenceType[object]
    child_type: type[object]
    member_name: str
    member: Callable[..., Any]
    func: _TLookupFunction[object, object]


class _UnBoundLookupFunction(NamedTuple):
    parent_type: type[object]
    child_type: type[object]
    member_name: str
    member: Callable[..., Any]
    func: _TLookupFunction[object, object]


class LookupRegistry:
    """Registry for management and lookup of parent-child relations at runtime."""

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(  # noqa: D102, PYI034
        cls,
        *args: Any,  # noqa: ANN401, ARG003
        **kwargs: Any,  # noqa: ANN401, ARG003
    ) -> LookupRegistry:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        # The lookup table is a dictionary of dictionaries of lists
        # It maps child types to parent types to instance bound child lookup functions
        # In other words:
        # child type -> parent type -> all lookup functions on all existing parent instances
        # which return children of the child type
        self._bound_lookup_functions: dict[type[object], dict[type[object], list[_BoundLookupFunction]]] = {}
        # For performance reasons, we also keep a separate dictionary of unbound lookup functions
        # The structure, however, is simpler: It only maps parent type to all child lookup functions
        # found and registered for that parent type.
        # In other words:
        # parent type -> all lookup functions on parent type which return children
        self._unbound_lookup_functions: dict[type[object], list[_UnBoundLookupFunction]] = {}

    def register_parent(self, parent: TParent) -> None:  # pyright: ignore [reportInvalidTypeVarUse]
        """Register a parent object and its associated child lookup functions.

        This method performs the following steps:
        1. Determines the type of the provided parent object.
        2. Checks if the parent type is already registered.
        3. If the parent type is not registered, it finds and registers any unbound child lookup functions.
        4. Creates and registers bound child lookup functions for the parent object.

        Args:
            parent (TParent): The parent object to be registered.

        Returns
        -------
            None
        """
        parent_type: type[TParent] = type(parent)
        if not self._parent_type_is_registered(parent_type):
            self._find_and_register_unbound_child_lookup_functions(parent)
        self._create_and_register_bound_child_lookup_functions(parent)

    @overload
    def lookup_parent(self, child: object, parent: type[TParent]) -> TParent | None: ...

    @overload
    def lookup_parent(self, child: object, parent: TParent) -> TParent | None: ...

    def lookup_parent(  # noqa: C901, PLR0912
        self,
        child: object,
        parent: type[TParent] | TParent,
    ) -> TParent | None:
        """Look up the parent of a given child object.

        Args:
            child (object): The child object for which to find the parent.
            parent (type[TParent] | TParent): The type or instance of the parent to look for.

        Returns
        -------
            TParent | None: The parent object if found, otherwise None.
        """
        matching_child_types_registered: list[type[Any]] = [
            child_type for child_type in self._bound_lookup_functions if issubclass(type(child), child_type)
        ]
        if not matching_child_types_registered:
            return None

        for child_type in matching_child_types_registered:
            matching_parent_types_registered: list[type[Any]]
            if inspect.isclass(parent):
                parent = cast(type[TParent], parent)
                matching_parent_types_registered = [
                    parent_type
                    for parent_type in self._bound_lookup_functions[child_type]
                    if issubclass(parent_type, parent)
                ]
            else:
                parent = cast(TParent, parent)
                matching_parent_types_registered = [
                    parent_type
                    for parent_type in self._bound_lookup_functions[child_type]
                    if issubclass(parent_type, type(parent))
                ]
            if not matching_parent_types_registered:
                continue

            must_match_parent_instance: bool = not inspect.isclass(parent)

            for parent_type in matching_parent_types_registered:
                child_lookups: list[_BoundLookupFunction] = list(  # create a copy to avoid concurrent modification
                    self._bound_lookup_functions[child_type][parent_type]
                )
                child_lookups.reverse()  # reverse the list to prefer the most recently registered parent instances
                for child_lookup in child_lookups:
                    _parent = child_lookup.parent()
                    if not _parent:
                        # parent instance has been garbage collected -> remove lookup function from registry
                        self._bound_lookup_functions[child_type][parent_type].remove(child_lookup)
                        continue
                    if must_match_parent_instance and _parent is not parent:
                        continue
                    if childs_in_parent := child_lookup.func(_parent):
                        if not isinstance(childs_in_parent, list):
                            childs_in_parent = [childs_in_parent]
                        for child_in_parent in childs_in_parent:
                            if child_in_parent is child:
                                return cast(TParent, _parent)

        return None

    def _find_and_register_unbound_child_lookup_functions(self, parent: object) -> None:
        parent_type: type[object] = type(parent)
        parent_members: list[tuple[str, Callable[..., object]]] = []
        parent_members = self._get_members(parent_type)

        class LookupFunction(NamedTuple):
            member_name: str
            member: Callable[..., object]
            func: _TLookupFunction[object, object]

        lookup_functions: list[LookupFunction] = []

        def is_lookup_function(
            member: Callable[..., Any],
        ) -> _TLookupFunction[TParent, Any] | None:
            if hasattr(member, "is_child_lookup"):
                return member

            sub_members: list[tuple[str, Callable[..., object]]] = []
            sub_members = self._get_members(member)

            for sub_member in sub_members:
                if is_lookup_function(sub_member[1]):
                    return sub_member[1]

            return None

        for member in parent_members:
            func: _TLookupFunction[Any, Any] | None = is_lookup_function(member[1])
            if func is not None:
                lookup_function = LookupFunction(
                    member_name=member[0],
                    member=member[1],
                    func=func,
                )
                lookup_functions.append(lookup_function)

        for lookup_function in lookup_functions:
            type_hints: dict[str, type[object]] = {}
            try:
                type_hints = typing.get_type_hints(lookup_function.func)
            except NameError as e:
                msg = (
                    f"Failed to get type hints for {lookup_function.func}. NameError occurred. "
                    f"Hint: This usually happens when the import statement for the child type "
                    "returned by {lookup_function} is located within an `if TYPE_CHECKING` block."
                    "To fix this, move the import statement for the child type to be looked up "
                    "out of the `if TYPE_CHECKING` block."
                )
                logger.exception(msg)
                raise NameError(msg) from e
            return_type = type_hints.get("return")
            assert return_type is not None

            # Unpack the return type if it is an iterable
            return_class = None
            return_class = return_type if inspect.isclass(return_type) else get_origin(return_type)
            if issubclass(return_class, list) or (  # works for Python 3.11 and later
                issubclass(type(return_class), GenericAlias)  # workaround check for Python 3.10 compatibility
                and str(return_class).lower().startswith("list[")
            ):
                return_type = typing.get_args(return_type)[0]
                return_class = return_type if inspect.isclass(return_type) else get_origin(return_type)
            assert return_class is not None
            assert inspect.isclass(return_class)
            assert not issubclass(return_class, list)
            assert not issubclass(type(return_class), GenericAlias)

            child_type = return_class

            unbound_child_lookup_function = _UnBoundLookupFunction(
                parent_type=parent_type,
                child_type=child_type,
                member_name=lookup_function.member_name,
                member=lookup_function.member,
                func=lookup_function.func,
            )

            self._register_unbound_child_lookup_function(unbound_child_lookup_function)

    def _register_unbound_child_lookup_function(
        self,
        unbound_child_lookup_function: _UnBoundLookupFunction,
    ) -> None:
        parent_type: type[object] = unbound_child_lookup_function.parent_type
        if not self._parent_type_is_registered(parent_type):
            self._unbound_lookup_functions[parent_type] = []
        self._unbound_lookup_functions[parent_type].append(unbound_child_lookup_function)

    def _get_unbound_child_lookup_functions(self, parent: object) -> list[_UnBoundLookupFunction] | None:
        parent_type: type[object] = type(parent)
        if not self._parent_type_is_registered(parent_type):
            return None
        return self._unbound_lookup_functions[parent_type]

    def _create_and_register_bound_child_lookup_functions(self, parent: object) -> None:
        unbound_lookup_functions = self._get_unbound_child_lookup_functions(parent)
        if not unbound_lookup_functions:
            return
        for unbound_lookup_function in unbound_lookup_functions:
            self._create_and_register_bound_child_lookup_function(unbound_lookup_function, parent)

    def _create_and_register_bound_child_lookup_function(
        self,
        unbound_child_lookup_function: _UnBoundLookupFunction,
        parent: object,
    ) -> None:
        bound_child_lookup_function = _BoundLookupFunction(
            parent=weakref.ref(parent),
            child_type=unbound_child_lookup_function.child_type,
            member_name=unbound_child_lookup_function.member_name,
            member=unbound_child_lookup_function.member,
            func=unbound_child_lookup_function.func,
        )

        parent_type: type[object] = type(parent)
        child_type: type[object] = bound_child_lookup_function.child_type
        registered_child_types: list[type[object]] = list(self._bound_lookup_functions.keys())
        child_type_found: type[object] | None = self._find_exact_type(child_type, registered_child_types)
        if not child_type_found:
            self._bound_lookup_functions[child_type] = {}
            child_type_found = child_type
        registered_parent_types: list[type[object]] = list(self._bound_lookup_functions[child_type_found].keys())
        parent_type_found: type[object] | None = self._find_closest_type(parent_type, registered_parent_types)
        if not parent_type_found:
            self._bound_lookup_functions[child_type_found][parent_type] = []
            parent_type_found = parent_type
        self._bound_lookup_functions[child_type_found][parent_type_found].append(bound_child_lookup_function)

    def _parent_type_is_registered(self, parent_type: type[object]) -> bool:
        return parent_type in self._unbound_lookup_functions

    def _find_closest_type(
        self,
        type_to_find: type[Any],
        registered_types: list[type[Any]],
        max_distance: int = 999,
    ) -> type[Any] | None:
        parent_super_types = inspect.getmro(type_to_find)
        closest_super_type: type[Any] | None = None
        best_distance_so_far: int = 999
        # Reverse the list of registered types to prefer the most recently registered types
        registered_types_reversed = list(reversed(registered_types))
        for registered_parent_type in registered_types_reversed:
            if registered_parent_type in parent_super_types:
                distance = parent_super_types.index(registered_parent_type)
                if distance < best_distance_so_far:
                    best_distance_so_far = distance
                    closest_super_type = registered_parent_type
        return closest_super_type if best_distance_so_far <= max_distance else None

    def _find_exact_type(
        self,
        type_to_find: type[Any],
        registered_types: list[type[Any]],
    ) -> type[Any] | None:
        return self._find_closest_type(type_to_find, registered_types, max_distance=0)

    def _get_members(self, obj: object) -> list[tuple[str, Callable[..., object]]]:
        _getter_functions: list[tuple[str, Callable[..., object]]] = []
        _functions: list[tuple[str, Callable[..., object]]] = []
        _properties: list[tuple[str, Callable[..., object]]] = []
        with contextlib.suppress(Exception):
            _getter_functions = inspect.getmembers(
                obj,
                lambda member: (hasattr(member, "__name__") and str(member.__name__).__contains__("fget")),
            )
        with contextlib.suppress(Exception):
            _functions = inspect.getmembers(
                obj,
                inspect.isfunction,
            )
        with contextlib.suppress(Exception):
            _properties = inspect.getmembers(
                obj,
                lambda member: isinstance(member, property),
            )
        members: list[tuple[str, Callable[..., object]]] = _getter_functions + _functions + _properties
        return members


#: Singleton instance of the lookup registry
lookup_registry: LookupRegistry = LookupRegistry()


def is_child_lookup(
    func: TFunc,
) -> TFunc:
    """Decorator to mark a function as a child lookup function."""  # noqa: D401
    # create a new attribute on the function object
    func.is_child_lookup = True  # type: ignore[attr-defined]
    return func
