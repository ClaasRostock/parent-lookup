"""Custom base class that registers parent fixture instances."""

from __future__ import annotations

from typing import Self, TypeVar

from parent_lookup.lookup import lookup_registry


class CustomBase:
    """Base fixture that automatically registers instances as lookup parents."""

    _T = TypeVar("_T", bound="CustomBase")

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(cls) -> Self:
        """Create an instance and register it as a parent.

        Args:
            cls: The custom parent class being instantiated.

        Returns:
            The registered instance.
        """
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance
