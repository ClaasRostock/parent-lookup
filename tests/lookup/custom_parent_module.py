"""Custom parent fixtures with marked child lookup properties."""

from custom_base_module import CustomBase
from custom_child_module import CustomChild

from parent_lookup.lookup import is_child_lookup


class CustomParent(CustomBase):
    """Parent fixture with a child collection and a marked lookup property."""

    def __init__(self) -> None:
        """Initialize an empty child collection for this custom parent."""
        self._childs: list[CustomChild] = []

    def add_child(self, child: CustomChild) -> None:
        """Add a child to the collection used by the lookup fixture.

        Args:
            child: The child instance to register with this parent.
        """
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[CustomChild]:
        """Return the children inspected by the lookup registry.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs


class CustomSpecialParent(CustomParent):
    """Custom parent subtype used to test parent-type matching."""

    def __init__(self) -> None:
        """Initialize a specialized parent using the base setup."""
        super().__init__()

    def add_child(self, child: CustomChild) -> None:
        """Add a child using the inherited parent collection.

        Args:
            child: The child instance to associate with this parent.
        """
        super().add_child(child)

    @property
    @is_child_lookup
    def childs(self) -> list[CustomChild]:
        """Return the inherited collection for child lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs
