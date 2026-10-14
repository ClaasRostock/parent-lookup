"""Parent fixtures that register and expose child lookup methods."""

from __future__ import annotations

from child_module import Child  # noqa: TC002

from parent_lookup.lookup import is_child_lookup, lookup_registry


class Parent:
    """Parent fixture that registers itself and exposes its child collection."""

    def __init__(self) -> None:
        """Initialize an empty child collection for this parent."""
        self._childs: list[Child] = []

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(cls) -> Parent:  # noqa: PYI034
        """Create and register a parent instance with the lookup registry.

        Args:
            cls: The parent class being instantiated.

        Returns:
            The registered parent instance.
        """
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: Child) -> None:
        """Associate a child with this parent.

        Args:
            child: The child to include in this parent's lookup results.
        """
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[Child]:
        """Return the children inspected by parent lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs


class SpecialParent(Parent):
    """Parent subtype used to verify matching across parent inheritance."""

    def __init__(self) -> None:
        """Initialize a specialized parent using the base setup."""
        super().__init__()

    def add_child(self, child: Child) -> None:
        """Associate a child using the inherited parent collection.

        Args:
            child: The child to include in this parent's lookup results.
        """
        super().add_child(child)

    @property
    @is_child_lookup
    def childs(self) -> list[Child]:
        """Return the inherited collection used by parent lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs
