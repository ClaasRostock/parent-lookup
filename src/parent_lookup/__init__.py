"""Python package enabling a child object to dynamically lookup its parent at runtime."""

from parent_lookup.lookup import (
    TParent,
    is_child_lookup,
    lookup_registry,
)

__all__ = [
    "TParent",
    "is_child_lookup",
    "lookup_registry",
]
