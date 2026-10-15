"""Custom child fixtures built on the automatically registering base."""

from typing import overload

from custom_base_module import CustomBase

from parent_lookup.lookup import TParent, lookup_registry


class CustomChild(CustomBase):
    """Child fixture using the custom base class and registry lookup."""

    def __init__(self) -> None:
        """Initialize a custom child fixture without additional state."""

    @overload
    def find_parent(self, parent_type: type[TParent]) -> TParent | None:
        pass

    @overload
    def find_parent(self, parent_type: TParent) -> TParent | None:
        pass

    def find_parent(self, parent_type: type[TParent] | TParent) -> TParent | None:
        """Resolve this custom child fixture's parent through the registry.

        Args:
            parent_type: The parent class or instance to match.

        Returns:
            The matching parent, or ``None`` if no match is registered.
        """
        return lookup_registry.lookup_parent(self, parent_type)


class CustomSpecialChild(CustomChild):
    """Custom child subtype used to test inherited parent lookup."""

    def __init__(self) -> None:
        """Initialize a specialized custom child using the base setup."""
        super().__init__()
