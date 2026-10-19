# T01–T02: asset inventory and integration baseline

Date: 2026-10-20. Source: [remediation plan](2026-10-20-remediation-plan.md). This is a read-only inventory of GitHub refs, **not** proof that any unintegrated script ran in CI.

## Baseline

- Default branch `main` observed at `f7866a810ba4efcdf329c6bae921b242b1c046b0`.
- Integration branch: `ci/lean-coverage-evidence-20261020-0338`; initial head `e1325d73d` (review, plan, inventory script, tests).
- Do not merge to main until acceptance tests pass. Preserve existing branch history.
- Inventory comparison is against the baseline SHA, not against a branch name that may move.

| Asset | Source commit | Files differing from baseline | Status and next action |
|---|---|---|---|
| Existing Lean and Python baseline | f7866a810ba4efcdf329c6bae921b242b1c046b0 | baseline | Existing CI covers four Lean targets; Python CI coverage and artifacts not established |
| Inventory and tests | e1325d73d | scripts/lean_inventory_gate.py; tests/test_lean_inventory_gate.py; two review/plan notes | Present on integration branch; connect inventory to compilation and enforce unknown-file failure |
| Dependency gate | a49ffbdeca0395e97daac91caf98a6092d8e95df | lake-manifest.json; scripts/ci_status.py; scripts/dependency_lock_gate.py; scripts/lean_inventory_gate.py | Compare and port selectively; raw regex escaping bug reported by independent review; not CI-verified |
| Fixed-x equivalence | 8212448c91ccc378023537ea6e3d9c998c46f80f | TypeIIReconstruction.lean | Separately proven algebraic candidate; inspect exact diff and avoid accidental overwrite |
| Type-II finite certificate | 9adfe595522f613a94c29d70ba1d2f2d3766874e | .github/workflows/lean.yml; research/2026-10-18-typeii-670849/{ProgressionCompleteness.lean,README.md,TypeIIDepthSeven_UNCOMPILED.lean,TypeIIDivisorComplete.lean,minimal_modulus_certificate.py,verify.py} | Some Lean sources have no confirmed successful CI compile; classify as draft pending tests |

## Acceptance gate for T01/T02

- [x] Fixed baseline and integration branch selected.
- [x] Identified candidate refs and per-file differences via GitHub compare.
- [ ] Exhaustive audit of all remote branches, including empty aliases, completed.
- [ ] Individual source content reviewed and adoption decision recorded for each file.
- [ ] Confirm integration branch is current immediately before modifying workflows.
- [ ] CI evidence for new integrated implementation obtained.

## Next minimal steps

1. Inspect current workflow and the two competing inventory implementations.
2. Fix dependency gate with positive and negative tests, keeping Lean 4.24.0 / Mathlib v4.24.0.
3. Wire gates and adopted Lean/Python into workflow, then inspect the **new head SHA's** Actions run.
4. Do not report CI completion on the basis of this inventory commit.
