"""Parent and child fixtures that resolve parents through descriptors."""

from __future__ import annotations

from parent_lookup import ParentLookup, is_child_lookup, lookup_registry


class DescriptorParent:
    """Parent fixture whose children are discovered through a property."""

    def __init__(self) -> None:
        """Initialize an empty collection of descriptor children."""
        self._childs: list[DescriptorChild] = []

    def __new__(cls) -> DescriptorParent:  # noqa: PYI034
        """Create and register a descriptor parent instance.

        Args:
            cls: The descriptor parent class being instantiated.

        Returns:
            The registered parent instance.
        """
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: DescriptorChild) -> None:
        """Associate a child with this descriptor parent.

        Args:
            child: The child to include in this parent's lookup results.
        """
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[DescriptorChild]:
        """Return the child collection used by parent lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs


class DescriptorChild:
    """Child fixture resolved through a :class:`ParentLookup` descriptor.

    Attributes:
        parent: Descriptor that resolves this child's registered parent.
    """

    parent: ParentLookup[DescriptorParent] = ParentLookup(DescriptorParent)

    def __init__(self) -> None:
        """Initialize a child fixture resolved through its parent descriptor."""


class DescriptorSpecialChild(DescriptorChild):
    """Descriptor child subtype used to test inherited parent resolution."""

    def __init__(self) -> None:
        """Initialize a specialized child using the base fixture setup."""
        super().__init__()
