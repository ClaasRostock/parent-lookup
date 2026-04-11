from __future__ import annotations

from parent_lookup import ParentLookup, is_child_lookup, lookup_registry


class DescriptorParentWithFutureAnnotations:
    def __init__(self) -> None:
        self._childs: list[DescriptorChildWithFutureAnnotations] = []

    def __new__(cls) -> DescriptorParentWithFutureAnnotations:  # noqa: PYI034
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: DescriptorChildWithFutureAnnotations) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[DescriptorChildWithFutureAnnotations]:
        return self._childs


class DescriptorChildWithFutureAnnotations:
    parent: ParentLookup[DescriptorParentWithFutureAnnotations] = ParentLookup(DescriptorParentWithFutureAnnotations)

    def __init__(self) -> None:
        pass


class DescriptorSpecialChildWithFutureAnnotations(DescriptorChildWithFutureAnnotations):
    def __init__(self) -> None:
        super().__init__()
