from copy import deepcopy

from descriptor_module import DescriptorChild, DescriptorParent, DescriptorSpecialChild
from descriptor_module_with_future_annotations import (
    DescriptorChildWithFutureAnnotations,
    DescriptorParentWithFutureAnnotations,
    DescriptorSpecialChildWithFutureAnnotations,
)

from parent_lookup import ParentLookup


def test_descriptor_finds_parent() -> None:
    # Prepare
    parent = DescriptorParent()
    child = DescriptorChild()
    parent.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent


def test_descriptor_finds_latest_parent() -> None:
    # Prepare
    child = DescriptorChild()
    parent1 = DescriptorParent()
    parent1.add_child(child)
    parent2 = DescriptorParent()
    parent2.add_child(child)
    parent3 = DescriptorParent()
    parent3.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent3


def test_descriptor_finds_parent_after_deepcopy() -> None:
    # Prepare
    parent = DescriptorParent()
    child = DescriptorChild()
    parent.add_child(child)
    parent_copy = deepcopy(parent)
    child_copy = parent_copy.childs[0]
    # Execute
    found_parent = child_copy.parent
    # Assert
    assert found_parent is parent_copy


def test_descriptor_finds_parent_from_child_subtype() -> None:
    # Prepare
    parent = DescriptorParent()
    child = DescriptorSpecialChild()
    parent.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent


def test_descriptor_on_class_returns_descriptor() -> None:
    # Execute
    class_level_parent_lookup = DescriptorChild.parent
    # Assert
    assert isinstance(class_level_parent_lookup, ParentLookup)


def test_descriptor_returns_none_when_no_parent_registered() -> None:
    # Prepare
    child = DescriptorChild()
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is None

def test_descriptor_finds_parent_with_future_annotations() -> None:
    # Prepare
    parent = DescriptorParentWithFutureAnnotations()
    child = DescriptorChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent


def test_descriptor_finds_latest_parent_with_future_annotations() -> None:
    # Prepare
    child = DescriptorChildWithFutureAnnotations()
    parent1 = DescriptorParentWithFutureAnnotations()
    parent1.add_child(child)
    parent2 = DescriptorParentWithFutureAnnotations()
    parent2.add_child(child)
    parent3 = DescriptorParentWithFutureAnnotations()
    parent3.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent3


def test_descriptor_finds_parent_after_deepcopy_with_future_annotations() -> None:
    # Prepare
    parent = DescriptorParentWithFutureAnnotations()
    child = DescriptorChildWithFutureAnnotations()
    parent.add_child(child)
    parent_copy = deepcopy(parent)
    child_copy = parent_copy.childs[0]
    # Execute
    found_parent = child_copy.parent
    # Assert
    assert found_parent is parent_copy


def test_descriptor_finds_parent_from_child_subtype_with_future_annotations() -> None:
    # Prepare
    parent = DescriptorParentWithFutureAnnotations()
    child = DescriptorSpecialChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.parent
    # Assert
    assert found_parent is parent
