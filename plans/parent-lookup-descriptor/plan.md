## Plan: Add Generic ParentLookup Descriptor

Add a new descriptor-based API that lets child classes declare parent lookup declaratively while preserving the existing find_parent approach. The descriptor will delegate to LookupRegistry.lookup_parent, remain fully generic over parent type, and be validated across both annotation modes (with and without from __future__ import annotations) using mirrored test modules.

**Steps**
1. Phase 1 - API design and compatibility contract: define the ParentLookup public API and behavior contract (descriptor access on instance returns resolved parent or None; descriptor access on class returns descriptor itself); confirm no behavioral change to existing LookupRegistry and existing tests. This phase is a prerequisite for all implementation steps.
2. Phase 2 - Core implementation in lookup module (*depends on 1*): add a generic ParentLookup[TParent] descriptor class in src/parent_lookup/lookup.py that stores a parent type reference and calls lookup_registry.lookup_parent(instance, parent_type) in __get__. Add overloads/type annotations so static type checkers infer TParent | None for instance access and ParentLookup[TParent] for class access.
3. Phase 3 - Public package export (*depends on 2*): expose ParentLookup from src/parent_lookup/__init__.py and include it in __all__ so descriptor API is first-class and discoverable without breaking existing imports.
4. Phase 4 - New test helper modules for descriptor usage (*parallel with 5 after 2*): add child/parent helper modules under tests/lookup that model descriptor-based children in both annotation modes (standard and _with_future_annotations), reusing current parent registration pattern with @is_child_lookup and register_parent in parent __new__.
5. Phase 5 - Descriptor behavior tests (*parallel with 4 after 2*): add a new test module under tests/lookup (for example test_parent_lookup_descriptor.py) that mirrors existing AAA style and doubled future-annotations pattern. Cover baseline lookup, latest-parent preference, subtype child lookup, multiple parent instances, and deepcopy behavior for descriptor-based child classes.
6. Phase 6 - Typing and docs alignment (*depends on 2 and 3*): add/adjust public docstrings for ParentLookup, update README and/or docs/source parent_lookup references with descriptor usage examples, and add CHANGELOG Unreleased entry describing the new additive API.
7. Phase 7 - Verification and release readiness (*depends on 4, 5, 6*): run focused and full validation (pytest tests/lookup, then full pytest, ruff format/check, pyright, mypy) and confirm existing tests remain unchanged and passing.

**Relevant files**
- c:/Dev/parent-lookup/src/parent_lookup/lookup.py - add ParentLookup[TParent] descriptor, overloads, and docstrings; reuse LookupRegistry.lookup_parent and existing generic conventions (TParent).
- c:/Dev/parent-lookup/src/parent_lookup/__init__.py - export ParentLookup and update __all__.
- c:/Dev/parent-lookup/tests/lookup/test_lookup.py - reference for naming, Arrange-Act-Assert structure, and mirrored future-annotation testing style (do not modify existing tests unless unavoidable).
- c:/Dev/parent-lookup/tests/lookup/parent_module.py - reference parent registration and @is_child_lookup conventions to mirror in new descriptor fixture modules.
- c:/Dev/parent-lookup/tests/lookup/parent_module_with_future_annotations.py - reference for future-annotations-safe parent definitions.
- c:/Dev/parent-lookup/tests/lookup/child_module.py - reference current explicit child API to keep backward compatibility while adding descriptor-based alternative.
- c:/Dev/parent-lookup/tests/lookup/child_module_with_future_annotations.py - reference future-annotations-safe child definitions.
- c:/Dev/parent-lookup/README.md - document new descriptor usage as additive API.
- c:/Dev/parent-lookup/docs/source/parent_lookup.rst - extend API documentation for ParentLookup.
- c:/Dev/parent-lookup/CHANGELOG.md - add Unreleased note for descriptor API.

**Verification**
1. Run targeted descriptor tests only: pytest tests/lookup -k parent_lookup_descriptor.
2. Run full lookup suite regression: pytest tests/lookup.
3. Run full project tests: pytest.
4. Run formatting and linting gates: ruff format . and ruff check .
5. Run typing gates: pyright and mypy.
6. Confirm documentation references build cleanly (if docs build is part of local workflow): sphinx build via existing docs Makefile.

**Decisions**
- Keep current API fully intact: existing find_parent implementations and tests remain valid and unchanged.
- ParentLookup is additive and opt-in: child classes may choose descriptor approach without forcing migration.
- Descriptor should delegate to lookup_registry.lookup_parent rather than duplicate registry logic, minimizing behavioral drift.
- Type safety is first-class: ParentLookup is generic over TParent to preserve static return-type precision.
- Future-annotations compatibility is required and validated via duplicated test modules mirroring existing project pattern.
- Python compatibility target is explicit: implement only Python >= 3.11 syntax/features and validate against the declared project requirement in pyproject.toml (requires-python = ">= 3.11").

**Further Considerations**
1. Constructor flexibility recommendation: start with ParentLookup(parent_type: type[TParent]) only; defer optional registry injection unless testability requires it.
2. Naming recommendation: use singular child attribute names in examples (for example parent) to emphasize descriptor semantics.
3. Backward-compatibility guard: avoid changing LookupRegistry internals unless required by failing descriptor edge-case tests.
