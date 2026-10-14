"""parent-lookup - Python package enabling a child object to dynamically lookup its parent at runtime."""

# Import `metadata`, but alias it as private.
# Otherwise `metadata` would be added as public attribute `parent_lookup.metadata`
# to the package namespace, which is not intended.
from importlib import metadata as _metadata

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

def _get_package_version() -> str:
    """Dynamically retrieve the version of `parent-lookup`.

    The function retrieves the version number from the metadata of the
    installed package.

    If the package metadata is not available (e.g. when running from source
    without installing the package), it falls back to "(version unknown)".

    Returns:
        The version of the package, or "(version unknown)" if the version
        cannot be determined.
    """
    try:
        version = _metadata.version("parent-lookup")
    except _metadata.PackageNotFoundError:
        # Fallback
        version = "(version unknown)"
    return version


__version__: str = _get_package_version()
