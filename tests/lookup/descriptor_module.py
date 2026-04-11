from __future__ import annotations

from parent_lookup import ParentLookup, is_child_lookup, lookup_registry


class DescriptorParent:
    def __init__(self) -> None:
        self._childs: list[DescriptorChild] = []

    def __new__(cls) -> DescriptorParent:  # noqa: PYI034
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: DescriptorChild) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[DescriptorChild]:
        return self._childs


class DescriptorChild:
    parent: ParentLookup[DescriptorParent] = ParentLookup(DescriptorParent)

    def __init__(self) -> None:
        pass


class DescriptorSpecialChild(DescriptorChild):
    def __init__(self) -> None:
        super().__init__()
