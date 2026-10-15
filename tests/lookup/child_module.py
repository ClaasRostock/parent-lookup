"""Child fixtures with the standard parent lookup method."""

from typing import overload

from parent_lookup.lookup import TParent, lookup_registry


class Child:
    """Basic child fixture with a registry-backed parent lookup method."""

    def __init__(self) -> None:
        """Initialize a child fixture without additional state."""

    @overload
    def find_parent(self, parent_type: type[TParent]) -> TParent | None:
        pass

    @overload
    def find_parent(self, parent_type: TParent) -> TParent | None:
        pass

    def find_parent(self, parent_type: type[TParent] | TParent) -> TParent | None:
        """Resolve this child fixture's parent through the lookup registry.

        Args:
            parent_type: The parent class or instance to match.

        Returns:
            The matching parent, or ``None`` if no match is registered.
        """
        return lookup_registry.lookup_parent(self, parent_type)


class SpecialChild(Child):
    """Child subtype used to verify parent lookup for inherited child types."""

    def __init__(self) -> None:
        """Initialize a specialized child using the base fixture setup."""
        super().__init__()
