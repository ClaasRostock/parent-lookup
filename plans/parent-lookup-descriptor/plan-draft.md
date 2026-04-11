# Plan: Implement a `ParentLookup` Descriptor class

## Problem Statement
Currently, child classes need to implement several methods in order to support the lookup of their parent(s). This is considered boilerplate code.
Goal is to develop an additional approach, not replacing but amending the current API, which reduces the necessary declarative and implementation effort for child classes to declare the type(s), i.e. the parent class(es), a child class expects to be a child of and wants to lookup.
Idea is to implement a `ParentLookup` class that implements the Descriptor protocol. A child class would then be able to declare a parent attribute, assigning an instance of this Descriptor class.
When this attribute is accessed on a child instance, the `ParentLookup` Descriptor would implement and handle the parent-class specific lookup, i.e. all the code which currently needs to be implemented by each child class.
The specific parent class (parent type) should be handled as a generic type variable in `ParentLookup`. A user could pass the specific parent type then e.g. as an argument to `ParentLookup`s constructor.

## Context
- Relevant modules:/src/parent_lookup/lookup.py
- Related tests: All tests in /tests/lookup
- Constraints:
  - The solution should not yet replace the current API but amend it. Alike, current tests should not be altered, but additional tests be created for the added functionality.
  - The solution shall make use of a generic type variable for the parent type, ensuring that static type checkers resolve e.g. the correct type of return values of methods.
  - The proposed solution needs to be agnostic to whether the modules in which a parent class or a child class is implemented in declares `from __future__ import annotations`.

## Assumptions
- None

## Proposed Approach
- Implement a `ParentLookup` class that implements the Descriptor protocol.

## Alternatives Considered
- So far no alternative considered. However, feel free to propose an alternative approach if you have a good idea.

## Validation Strategy
- Tests to add or update: Create additional test modules.
- Edge cases to cover: Write tests for cases where the parent or child class are defined inside (test) modules which declare `from __future__ import annotations`, and similarly for cases where `from __future__ import annotations` is not used. (You will find this pattern of "doubled" tests also in the test modules already existing. Simply follow the same approach for the new, additional test modules.)

## Risks & Mitigations
- None

## Definition of Done
- [ ] Code implemented
- [ ] Tests passing
- [ ] Documentation updated (if needed)
