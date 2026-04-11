"""parent_lookup - Python package enabling a child object to dynamically lookup its parent at runtime."""

from parent_lookup.lookup import (
    ParentLookup,
    TParent,
    is_child_lookup,
    lookup_registry,
)

__all__ = [
    "ParentLookup",
    "TParent",
    "is_child_lookup",
    "lookup_registry",
]
