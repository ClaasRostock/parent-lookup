# Plan: Add and refine Python type annotations

## Problem Statement

Improve type completeness in the Python codebase by adding missing
annotations and replacing explicit `Any` annotations with more specific types
where the implementation and call sites support doing so. Preserve public
runtime behavior and keep all types aligned with the supported Python
versions, static type checkers, and existing tests.

The current static diagnostics do not report missing annotations, but the
type-authoring inventory identifies a small set of source-level candidates:
module variables with no explicit annotation and private helpers whose type
signatures use explicit `Any`. The implementation should verify each
candidate's real value flow and avoid changing types merely to satisfy a
mechanical count.

## Baseline

- Worktree: clean on branch `rename-demos-to-examples`, at commit
  `6d85fad` (`refine internal lookup type annotations`).
- Python file scope: 17 Python files are present across `src/`, `tests/`, and
  `docs/source/`. The library package contains four Python files under
  `src/parent_lookup/`; tests comprise `tests/conftest.py` and 11 Python
  files under `tests/lookup/`; `docs/source/conf.py` is the remaining Python
  support file. Confirm any additional source-bearing directories if the
  branch changes before implementation.
- Ruff configuration:
  - `ruff.toml` selects `ALL` and does not globally ignore the `ANN` family.
  - `tests/**/*` has per-file ignores for ANN201 and ANN202.
  - Other per-file exceptions are scoped to stubs, notebooks, examples, and
    specific modules; no `src/parent_lookup/` annotation suppressions were
    found.
- Annotation-specific Ruff results:
  - `uv run ruff check`: passed with 0 findings.
  - `uv run ruff check --ignore ANN --ignore RUF100`: passed with 0 findings.
  - `uv run ruff check --select ANN --config "lint.per-file-ignores = {}"`:
    passed with 0 findings. This direct check disables per-file ignores and
    confirms that ANN findings are not hidden by test exceptions.
- Type-authoring inventory, refreshed with Pylance over the four library
  package modules:
  - `src/parent_lookup/lookup.py`: 2 candidates reported as `explicitAny`:
    `_get_members`'s return annotation and the nested
    `is_lookup_function.member` parameter.
  - `src/parent_lookup/utils/logging.py`: 2 missing-annotation inventory
    entries for module variables, `__all__` and `logger`.
  - `src/parent_lookup/__init__.py`: 1 missing-annotation inventory entry,
    `__all__`.
  - `src/parent_lookup/utils/__init__.py`: no candidates.
  - Total: 5 candidates. The three module variables already infer to
    `list[str]`, `list[str]`, and `logging.Logger`, respectively, so adding
    redundant source annotations is not warranted.
- Implementation already present in commit `6d85fad`: narrowed the private
  type lookup helpers to `type[object]` and `list[type[object]]`, and changed
  the nested callable parameter from `Callable[..., Any]` to
  `Callable[..., object]`. The remaining dynamic candidates were reviewed
  against runtime values and are intentionally retained; see
  [Implementation findings](#implementation-findings).
- `uv run ruff format --check`: passed; 49 files already formatted.
- `uv run pyright`: passed; 0 errors, 0 warnings, 0 informations.
- `uv run mypy`: passed; no issues found in 16 source files.
- `uv run pytest -q`: passed; 26 tests passed in 0.17 seconds.
- `uv run pytest --collect-only -q`: passed; collected 26 tests. The test
  suite includes 16 lookup behavior tests and 10 descriptor tests.
- Draft-baseline comparison: the draft specified commands but no measured
  results. Current Ruff annotation checks, pyright, mypy, formatting, and
  pytest all pass. The original Pylance inventory identified 11 candidates;
  the committed refinement addressed the supported private helper types.
  The remaining candidates are not reported as diagnostics by pyright or
  mypy and are retained for the evidence-based reasons below.

## Context

- Relevant modules: all Python source files in `src/parent_lookup/` are the
  primary annotation scope. Review the 11 files under `tests/lookup/`,
  `tests/conftest.py`, and `docs/source/conf.py` for type dependencies and
  compatibility, but change tests or documentation support files only when
  needed to maintain correct annotations or type checking.
- Related tests: All existing tests (26 collected by
  `uv run pytest --collect-only -q`), especially the 16 tests in
  `tests/lookup/test_lookup.py` and 10 descriptor tests in
  `tests/lookup/test_parent_lookup_descriptor.py`.
- Constraints:
  - Follow `/AGENTS.md` Type Annotations guidance: specific types, avoid
    `Any` unless truly necessary, and remove stale type-ignore comments.
  - Preserve public API behavior and Python compatibility; the project
    supports Python 3.12 and later.
  - Do not add ignores or relax type-checking rules to hide findings.
  - Treat docstrings' type information as subordinate to annotations and do
    not duplicate or contradict types in prose.
  - Update the Unreleased changelog for code changes.

## Assumptions

- The 11 Pylance candidates are the initial actionable inventory for package
  source, not an exhaustive promise that all variables in tests and tool
  configuration require annotations.
- Explicit `Any` may remain only where dynamic behavior or a third-party
  boundary makes a narrower truthful type impractical; document that
  rationale in code only when necessary and consistent with project style.
- Changes to public signatures are in scope only if they accurately express
  existing behavior and do not alter runtime semantics.
- Test changes are not expected unless more precise annotations expose a
  genuine typing or behavior issue.

## Implementation findings

- `_get_members` concatenates results from `inspect.getmembers` predicates
  for getter-like values, functions, and properties. A runtime check returned
  both a callable function and a non-callable `property` descriptor. The
  current `Callable[..., object]` return annotation therefore excludes a
  real result. The general introspection predicates do not establish a
  callable type for every returned object; correcting the return type would
  require propagating `object` through discovery and narrowing before the
  dynamically marked callable is returned. Do not replace this annotation
  with a guessed callable type.
- The nested `is_lookup_function` receives values from `_get_members`,
  including property descriptors, while its successful result depends on a
  dynamically attached marker and the decorated callable's unknown child
  return shape. Replacing the remaining `Any` with an invented fixed
  signature or broadening the parameter alone would not accurately type both
  traversal inputs and the returned callable without additional narrowing
  logic or a type guard. Retain the existing annotation rather than change
  runtime behavior solely to reduce the inventory count.

## Proposed Approach

Work incrementally from low-risk module-level declarations to harder dynamic
helper types. After each phase, format changed Python files, check and remove
stale `# type: ignore` or `# pyright: ignore` comments, and run the
phase-appropriate validation.

1. **Establish the current implementation scope**
   - Confirm the active branch, clean worktree, source-bearing directories,
     and Python file list before editing.
   - Re-run the configured Ruff check and direct ANN-family check with
     per-file ignores disabled. Record any change from this plan's baseline.
   - Re-run the Pylance annotation inventory for the source modules and
     inspect relevant type definitions and call sites before assigning
     replacement types.

2. **Annotate module-level exported variables**
   - Review `__all__` in `src/parent_lookup/__init__.py` and
     `src/parent_lookup/utils/logging.py`; add explicit, specific annotations
     only if the actual value shape is not already inferred or covered by an
     annotation.
   - Review `logger` in `utils/logging.py` and annotate it with the
     appropriate logging type if missing.
   - Confirm these annotations do not alter package exports or import
     behavior.

3. **Refine private helper signatures**
   - Trace inputs and outputs for `_find_closest_type`,
     `_find_exact_type`, and the nested
     `_find_and_register_unbound_child_lookup_functions` helper.
   - Replace explicit `Any` components with the narrowest truthful types
     supported by the values and callers. Consider `type[object]`,
     `Sequence[type[object]]`, or other appropriate abstractions only after
     validating actual usage; do not use a guessed replacement.
   - Keep generic relationships where they convey real type information.
     Retain `Any` only at a proven dynamic boundary where a more specific
     annotation would be misleading.

4. **Resolve suppression drift**
   - After each annotation phase, run pyright with
     `reportUnnecessaryTypeIgnoreComment` active and run
     `uv run mypy --warn-unused-ignores`.
   - Remove obsolete suppressions. If mypy and pyright disagree about a
     line-level suppression, follow the repository guidance: use a
     rule-specific module-level mypy disable only when required for mypy, or
     replace an unnecessary shared ignore with a specific `# pyright: ignore`
     when only pyright still requires it.
   - Do not remove a suppression based only on one type checker; verify both.

5. **Validate and document**
   - Re-run the Pylance inventory and direct ANN check. Confirm intended
     candidates are resolved or have a documented, evidence-based rationale
     for retaining `Any`.
   - Run the complete quality gates, inspect all diffs for runtime behavior
     changes, and add a concise Unreleased changelog entry.

## Alternatives Considered

- Treat a clean Ruff ANN or type-checker result as proof that no improvement
  is possible: rejected because Pylance identifies explicit `Any` and
  unannotated module variables beyond current diagnostics.
- Replace every `Any` with `object`: rejected because it can erase useful
  behavior and is not necessarily assignable to the operations performed by
  these helpers.
- Add blanket suppressions or loosen pyright/mypy/Ruff configuration:
  rejected because the task is to improve type information, not hide
  uncertainty.
- Annotate every local test variable: rejected as unnecessary noise unless
  a type-checking issue or a clear maintainability benefit warrants it.

## Validation Strategy

- Run `uv run ruff format --check` and `uv run pytest -q`; compare to
  baselines of 49 formatted files and 26 passing tests.
- Run `uv run ruff check` and
  `uv run ruff check --ignore ANN --ignore RUF100`; both should remain clean.
- Run `uv run ruff check --select ANN --config "lint.per-file-ignores = {}"`
  so test-specific ANN201/ANN202 ignores cannot conceal findings. Compare
  with the zero-finding baseline.
- Run `uv run pyright` and `uv run mypy`; require zero errors and no
  regression from the clean baseline. Include
  `uv run mypy --warn-unused-ignores` and verify pyright's
  `reportUnnecessaryTypeIgnoreComment` results for any suppression changed.
- Run `uv run pre-commit run --all-files` as part of the project's complete
  quality gate if code changes are made.
- Run `uv run pytest --collect-only -q` if test scope or test collection
  changes; compare the collected test set with the 26-test baseline.
- Review each replacement type against assignments, callers, and runtime
  values; inspect the final diff for unintended behavior changes and run
  `git diff --check`.

## Risks & Mitigations

- Risk: A superficially narrower annotation could misrepresent dynamic
  introspection or descriptor behavior.
  - Mitigation: trace values through assignments and call sites, and verify
    with both pyright and mypy before accepting the type.
- Risk: A changed ignore comment can affect both type checkers or leave a
  stale suppression.
  - Mitigation: run the stale-ignore checks in both tools after every typing
    phase and apply the documented divergence policy.
- Risk: More precise public annotations could accidentally imply changed
  API behavior.
  - Mitigation: limit changes to truthful static information, inspect runtime
    diffs, and run all tests without changing executable logic.
- Risk: Broad annotation changes in tests create noise or test-only typing
  regressions.
  - Mitigation: keep implementation focused on package source; edit tests
    only when needed to preserve accurate types or validate changed behavior.

## Definition of Done

- [x] Missing or overly broad annotations in the approved source scope are
      addressed, or retained `Any` uses have a specific, evidence-based
      reason in the implementation findings above.
- [x] All added or changed annotations are specific, truthful, and compatible
      with Python 3.12 and later.
- [x] Stale `# type: ignore` and `# pyright: ignore` comments are removed or
      narrowed after checking both pyright and mypy.
- [x] `uv run ruff format --check` passes.
- [x] `uv run pytest -q` passes with no regression compared to the baseline
      of 26 tests.
- [x] `uv run ruff check` passes with no regression compared to its
      zero-finding baseline.
- [x] `uv run ruff check --ignore ANN --ignore RUF100` passes with no
      regression compared to its zero-finding baseline.
- [x] `uv run ruff check --select ANN --config "lint.per-file-ignores = {}"`
      passes with no regression compared to its zero-finding baseline.
- [x] `uv run pyright` and `uv run mypy` pass with no regression compared to
      their clean baselines.
- [x] `uv run mypy --warn-unused-ignores` and pyright's
      `reportUnnecessaryTypeIgnoreComment` check reveal no newly stale
      suppressions.
- [x] `uv run pre-commit run --all-files` passes.
- [x] No Ruff ignore rules or type-checker configuration were weakened.
- [x] The Unreleased changelog documents the source annotation changes, and
      `git diff --check` passes.
