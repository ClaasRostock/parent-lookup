# sourcery skip: dont-import-test-modules

from tests.lookup.custom_base_module import CustomBase
from tests.lookup.custom_child_module import CustomChild

from parent_lookup.lookup import is_child_lookup


class CustomParent(CustomBase):
    def __init__(self) -> None:
        self._childs: list[CustomChild] = []

    def add_child(self, child: CustomChild) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[CustomChild]:
        return self._childs


class CustomSpecialParent(CustomParent):
    def __init__(self) -> None:
        super().__init__()

    def add_child(self, child: CustomChild) -> None:
        super().add_child(child)

    @property
    @is_child_lookup
    def childs(self) -> list[CustomChild]:
        return self._childs
