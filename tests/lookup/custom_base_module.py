from __future__ import annotations

from typing import Any, TypeVar

from parent_lookup.lookup import lookup_registry


class CustomBase:
    _T = TypeVar("_T", bound="CustomBase")

    # TODO @ClaasRostock: Change return type to Self once Python 3.10 support is dropped.
    #      ClaasRostock, 2025-02-03
    def __new__(
        cls: type[_T],
        *args: Any,  # noqa: ANN401, ARG003
        **kwargs: Any,  # noqa: ANN401, ARG003
    ) -> _T:  # noqa: PYI019
        instance = super().__new__(cls)  # pyright: ignore[reportArgumentType]
        lookup_registry.register_parent(instance)
        return instance
