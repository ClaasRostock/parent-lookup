# sourcery skip: dont-import-test-modules
from __future__ import annotations

from tests.lookup.child_module_with_future_annotations import ChildWithFutureAnnotations  # noqa: TC002

from parent_lookup.lookup import is_child_lookup, lookup_registry


class ParentWithFutureAnnotations:
    def __init__(self) -> None:
        self._childs: list[ChildWithFutureAnnotations] = []
        lookup_registry.register_parent(self)

    def add_child(self, child: ChildWithFutureAnnotations) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[ChildWithFutureAnnotations]:
        return self._childs
