from typing import overload

from parent_lookup.lookup import TParent, lookup_registry


class Child:
    def __init__(self) -> None:
        pass

    @overload
    def find_parent(self, parent_type: type[TParent]) -> TParent | None:
        pass

    @overload
    def find_parent(self, parent_type: TParent) -> TParent | None:
        pass

    def find_parent(self, parent_type: type[TParent] | TParent) -> TParent | None:
        return lookup_registry.lookup_parent(self, parent_type)


class SpecialChild(Child):
    def __init__(self) -> None:
        super().__init__()
