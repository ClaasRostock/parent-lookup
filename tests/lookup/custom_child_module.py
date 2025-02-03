# sourcery skip: dont-import-test-modules

from typing import overload

from tests.lookup.custom_base_module import CustomBase

from parent_lookup.lookup import TParent, lookup_registry


class CustomChild(CustomBase):
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


class CustomSpecialChild(CustomChild):
    def __init__(self) -> None:
        super().__init__()
