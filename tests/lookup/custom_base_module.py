from __future__ import annotations

from typing import TypeVar

from typing_extensions import Self

from parent_lookup.lookup import lookup_registry


class CustomBase:
    _T = TypeVar("_T", bound="CustomBase")

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(cls) -> Self:
        instance = super().__new__(cls)  # pyright: ignore[reportArgumentType]
        lookup_registry.register_parent(instance)
        return instance
