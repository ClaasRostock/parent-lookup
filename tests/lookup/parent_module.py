# sourcery skip: dont-import-test-modules
from __future__ import annotations

from typing import Any

from tests.lookup.child_module import Child  # noqa: TC002

from parent_lookup.lookup import is_child_lookup, lookup_registry


class Parent:
    def __init__(self) -> None:
        self._childs: list[Child] = []

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(  # noqa: PYI034
        cls,
        *args: Any,  # noqa: ANN401, ARG003
        **kwargs: Any,  # noqa: ANN401, ARG003
    ) -> Parent:
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: Child) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[Child]:
        return self._childs


class SpecialParent(Parent):
    def __init__(self) -> None:
        super().__init__()

    def add_child(self, child: Child) -> None:
        super().add_child(child)

    @property
    @is_child_lookup
    def childs(self) -> list[Child]:
        return self._childs
