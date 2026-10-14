"""Parent fixture whose marked child lookup uses postponed annotations."""

from __future__ import annotations

from child_module_with_future_annotations import ChildWithFutureAnnotations  # noqa: TC002

from parent_lookup.lookup import is_child_lookup, lookup_registry


class ParentWithFutureAnnotations:
    """Parent fixture whose child lookup return type is postponed."""

    def __init__(self) -> None:
        """Initialize an empty child collection and register this parent."""
        self._childs: list[ChildWithFutureAnnotations] = []
        lookup_registry.register_parent(self)

    def add_child(self, child: ChildWithFutureAnnotations) -> None:
        """Associate a child with this parent.

        Args:
            child: The child to include in this parent's lookup results.
        """
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[ChildWithFutureAnnotations]:
        """Return the children inspected by parent lookup.

        Returns:
            The children currently associated with this parent.
        """
        return self._childs
