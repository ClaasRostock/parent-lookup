"""Descriptor lookup fixtures using postponed type annotations."""

from __future__ import annotations

from parent_lookup import ParentLookup, is_child_lookup, lookup_registry


class DescriptorParentWithFutureAnnotations:
    """Descriptor parent fixture using postponed child type annotations."""

    def __init__(self) -> None:
        """Initialize an empty collection of descriptor children."""
        self._childs: list[DescriptorChildWithFutureAnnotations] = []

    def __new__(cls) -> DescriptorParentWithFutureAnnotations:  # noqa: PYI034
        """Create and register a descriptor parent instance.

        Args:
            cls: The descriptor parent class being instantiated.

        Returns:
            The registered parent instance.
        """
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: DescriptorChildWithFutureAnnotations) -> None:
        """Associate a child with this descriptor parent.

        Args:
            child: The child to include in this parent's lookup results.
        """
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[DescriptorChildWithFutureAnnotations]:
        """Return the child collection used by parent lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs


class DescriptorChildWithFutureAnnotations:
    """Descriptor child using postponed annotations for its parent type.

    Attributes:
        parent: Descriptor that resolves this child's registered parent.
    """

    parent: ParentLookup[DescriptorParentWithFutureAnnotations] = ParentLookup(DescriptorParentWithFutureAnnotations)

    def __init__(self) -> None:
        """Initialize a child fixture resolved through its parent descriptor."""


class DescriptorSpecialChildWithFutureAnnotations(DescriptorChildWithFutureAnnotations):
    """Postponed-annotation child subtype for descriptor lookup tests."""

    def __init__(self) -> None:
        """Initialize a specialized child using the base fixture setup."""
        super().__init__()
