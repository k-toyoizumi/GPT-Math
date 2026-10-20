# GPT-Math

Lean 4 + Mathlib formal verification of mathematical claims.

## Xu paper numerical audit (preliminary)

`XuTheorem41Audit.lean` checks rational-number identities attributed to arXiv:2609.29250. It proves a numerical discrepancy and checks a corrected numerical example. This does not disprove the general theorem. The transcription must be checked against the paper before any public correction claim.

[Lean CI](../../actions/workflows/lean.yml). Only a successful workflow run with no `sorry` qualifies as Lean-verified.

## Infrastructure verification and stop state

Research is paused. The current infrastructure work is on
`ci/lean-coverage-evidence-20261020-0338`; it is not merged into main.
See [remediation status and continuation contract](research/2026-10-20-remediation-status.md).

The six sources in `lean-sources.json` are adopted. There are no silently skipped
Lean drafts on this integration branch. Other research branches remain unadopted.
`lake build` covers every adopted target. Register any new tracked Lean file;
unknown files and mismatched default targets fail CI.

Use Lean 4.24.0 / the committed Mathlib lock and Python 3.12. After resolving the
locked dependencies (`lake exe cache get`), run `python3 scripts/verify_ci.py`.
Success requires the current Actions run, compiled-environment axiom audit,
Python reproduction, fault controls, and SHA-bound evidence. Native-assisted
proofs explicitly retain compiler/runtime trust; they are not classified as
kernel-only proofs. A green run on a different source is not evidence for edits.

Actions includes an isolated job that deliberately corrupts a dependency pin.
Its verifier step must fail, and the enclosing control job passes only after
checking that failure evidence was retained. This is an expected negative test.

Main integration, new research and recurring schedules require separate user
direction after the infrastructure acceptance record is complete.
