# pyright: reportPrivateUsage=false
# sourcery skip: dont-import-test-modules

# sourcery skip: dont-import-test-modules

from copy import deepcopy

from tests.lookup.child_module import Child, SpecialChild
from tests.lookup.child_module_with_future_annotations import (
    ChildWithFutureAnnotations,
    SpecialChildWithFutureAnnotations,
)
from tests.lookup.custom_child_module import CustomChild, CustomSpecialChild
from tests.lookup.custom_parent_module import CustomParent, CustomSpecialParent
from tests.lookup.parent_module import Parent
from tests.lookup.parent_module_with_future_annotations import ParentWithFutureAnnotations


class DummyChild:
    def __init__(self) -> None:
        pass


class DummySpecialChild(DummyChild):
    pass


class DummyParent:
    def __init__(self) -> None:
        self._childs: list[DummyChild] = [DummyChild() for _ in range(3)]

    def lookup_func(self) -> list[DummyChild]:
        return self._childs


class DummySpecialParent(DummyParent):
    pass


def test_find_parent() -> None:
    # Prepare
    parent = Parent()
    child = Child()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(Parent)
    # Assert
    assert found_parent is parent


def test_find_latest_parent() -> None:
    # Prepare
    child = Child()
    parent1 = Parent()
    parent1.add_child(child)
    parent2 = Parent()
    parent2.add_child(child)
    parent3 = Parent()
    parent3.add_child(child)
    # Execute
    found_parent = child.find_parent(Parent)
    # Assert
    assert found_parent is parent3


def test_find_parent_after_deepcopy() -> None:
    # Prepare
    parent = Parent()
    child = Child()
    parent.add_child(child)
    parent_copy = deepcopy(parent)
    child_copy = parent_copy.childs[0]
    # Execute
    found_parent = child_copy.find_parent(Parent)
    # Assert
    assert found_parent is parent_copy


def test_find_parent_with_multiple_parents_registered() -> None:
    # Prepare
    parent_1 = Parent()
    child_1 = Child()
    parent_1.add_child(child_1)
    parent_2 = Parent()
    child_2 = Child()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(Parent)
    found_parent_2 = child_2.find_parent(Parent)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2


def test_find_parent_with_future_annotations() -> None:
    # Prepare
    parent = ParentWithFutureAnnotations()
    child = ChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent is parent


def test_find_parent_with_multiple_parents_registered_with_future_annotations() -> None:
    # Prepare
    parent_1 = ParentWithFutureAnnotations()
    child_1 = ChildWithFutureAnnotations()
    parent_1.add_child(child_1)
    parent_2 = ParentWithFutureAnnotations()
    child_2 = ChildWithFutureAnnotations()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(ParentWithFutureAnnotations)
    found_parent_2 = child_2.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2


def test_find_parent_from_child_subtype() -> None:
    # Prepare
    parent = Parent()
    child = SpecialChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(Parent)
    # Assert
    assert found_parent is parent


def test_find_parent_from_child_subtype_with_multiple_parents_registered() -> None:
    # Prepare
    parent_1 = Parent()
    child_1 = SpecialChild()
    parent_1.add_child(child_1)
    parent_2 = Parent()
    child_2 = SpecialChild()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(Parent)
    found_parent_2 = child_2.find_parent(Parent)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2


def test_find_parent_from_child_subtype_with_future_annotations() -> None:
    # Prepare
    parent = ParentWithFutureAnnotations()
    child = SpecialChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent is parent


def test_find_parent_from_child_subtype_with_multiple_parents_registered_with_future_annotations() -> None:
    # Prepare
    parent_1 = ParentWithFutureAnnotations()
    child_1 = SpecialChildWithFutureAnnotations()
    parent_1.add_child(child_1)
    parent_2 = ParentWithFutureAnnotations()
    child_2 = SpecialChildWithFutureAnnotations()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(ParentWithFutureAnnotations)
    found_parent_2 = child_2.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2


def test_custom_find_parent() -> None:
    # Prepare
    parent = CustomParent()
    child = CustomChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(CustomParent)
    # Assert
    assert found_parent is parent


def test_custom_find_parent_after_deepcopy() -> None:
    # Prepare
    parent = CustomParent()
    child = CustomChild()
    parent.add_child(child)
    parent_copy = deepcopy(parent)
    child_copy = parent_copy.childs[0]
    # Execute
    found_parent = child_copy.find_parent(CustomParent)
    # Assert
    assert found_parent is parent_copy


def test_custom_find_parent_with_multiple_parents_registered() -> None:
    # Prepare
    parent_1 = CustomParent()
    child_1 = CustomChild()
    parent_1.add_child(child_1)
    parent_2 = CustomParent()
    child_2 = CustomChild()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(CustomParent)
    found_parent_2 = child_2.find_parent(CustomParent)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2


def test_custom_find_parent_with_multiple_parent_subtypes_registered() -> None:
    # Prepare
    parent_1 = CustomParent()
    child_1 = CustomChild()
    parent_1.add_child(child_1)
    parent_2 = CustomSpecialParent()
    child_2 = CustomChild()
    parent_2.add_child(child_2)
    parent_3 = CustomParent()
    child_3 = CustomChild()
    parent_3.add_child(child_3)
    parent_4 = CustomSpecialParent()
    child_4 = CustomChild()
    parent_4.add_child(child_4)

    # Execute
    found_parent_1 = child_1.find_parent(CustomParent)
    found_parent_2 = child_2.find_parent(CustomParent)
    found_parent_3 = child_3.find_parent(CustomParent)
    found_parent_4 = child_4.find_parent(CustomParent)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2
    assert found_parent_3 is parent_3
    assert found_parent_4 is parent_4


def test_custom_find_parent_from_child_subtype() -> None:
    # Prepare
    parent = CustomParent()
    child = CustomSpecialChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(CustomParent)
    # Assert
    assert found_parent is parent


def test_custom_find_parent_from_child_subtype_with_multiple_parents_registered() -> None:
    # Prepare
    parent_1 = CustomParent()
    child_1 = CustomSpecialChild()
    parent_1.add_child(child_1)
    parent_2 = CustomParent()
    child_2 = CustomSpecialChild()
    parent_2.add_child(child_2)
    # Execute
    found_parent_1 = child_1.find_parent(CustomParent)
    found_parent_2 = child_2.find_parent(CustomParent)
    # Assert
    assert found_parent_1 is parent_1
    assert found_parent_2 is parent_2
