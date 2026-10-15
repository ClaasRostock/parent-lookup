"""Tests for registry-based parent lookup and supported fixture variants."""

# pyright: reportPrivateUsage=false

from copy import deepcopy

from child_module import Child, SpecialChild
from child_module_with_future_annotations import (
    ChildWithFutureAnnotations,
    SpecialChildWithFutureAnnotations,
)
from custom_child_module import CustomChild, CustomSpecialChild
from custom_parent_module import CustomParent, CustomSpecialParent
from parent_module import Parent
from parent_module_with_future_annotations import ParentWithFutureAnnotations


class DummyChild:
    """Minimal child object used to exercise lookup helpers directly."""

    def __init__(self) -> None:
        """Initialize a minimal child fixture."""


class DummySpecialChild(DummyChild):
    """Subtype of the minimal child fixture."""


class DummyParent:
    """Minimal parent exposing a lookup function for its child instances."""

    def __init__(self) -> None:
        """Initialize a parent fixture with three child instances."""
        self._childs: list[DummyChild] = [DummyChild() for _ in range(3)]

    def lookup_func(self) -> list[DummyChild]:
        """Expose the fixture children to the lookup registry.

        Returns:
            The child instances associated with this parent.
        """
        return self._childs


class DummySpecialParent(DummyParent):
    """Subtype of the minimal parent fixture."""


def test_find_parent() -> None:
    """Find the registered parent containing the requested child."""
    # Prepare
    parent = Parent()
    child = Child()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(Parent)
    # Assert
    assert found_parent is parent


def test_find_latest_parent() -> None:
    """Prefer the most recently registered parent containing the child."""
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
    """Find a deep-copied child through its copied parent."""
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
    """Resolve each child to its own parent when several are registered."""
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
    """Resolve a parent when the lookup return annotation is postponed."""
    # Prepare
    parent = ParentWithFutureAnnotations()
    child = ChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent is parent


def test_find_parent_with_multiple_parents_registered_with_future_annotations() -> None:
    """Resolve separate parents with postponed lookup return annotations."""
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
    """Resolve a child subtype through its registered parent."""
    # Prepare
    parent = Parent()
    child = SpecialChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(Parent)
    # Assert
    assert found_parent is parent


def test_find_parent_from_child_subtype_with_multiple_parents_registered() -> None:
    """Resolve multiple child subtypes to their respective parent instances."""
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
    """Resolve a child subtype when the parent lookup annotation is postponed."""
    # Prepare
    parent = ParentWithFutureAnnotations()
    child = SpecialChildWithFutureAnnotations()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(ParentWithFutureAnnotations)
    # Assert
    assert found_parent is parent


def test_find_parent_from_child_subtype_with_multiple_parents_registered_with_future_annotations() -> None:
    """Resolve multiple child subtypes with postponed lookup annotations."""
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
    """Resolve a child using the custom parent and child fixture classes."""
    # Prepare
    parent = CustomParent()
    child = CustomChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(CustomParent)
    # Assert
    assert found_parent is parent


def test_custom_find_parent_after_deepcopy() -> None:
    """Resolve a copied child through the copied custom parent."""
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
    """Resolve children independently across multiple custom parents."""
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
    """Match children to registered custom parents and their subtypes."""
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
    """Resolve a custom child subtype through its custom parent."""
    # Prepare
    parent = CustomParent()
    child = CustomSpecialChild()
    parent.add_child(child)
    # Execute
    found_parent = child.find_parent(CustomParent)
    # Assert
    assert found_parent is parent


def test_custom_find_parent_from_child_subtype_with_multiple_parents_registered() -> None:
    """Resolve multiple custom child subtypes to their respective parents."""
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
