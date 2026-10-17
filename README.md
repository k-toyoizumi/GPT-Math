# GPT-Math

Lean 4 + Mathlib formal verification of mathematical claims.

## Xu paper numerical audit (preliminary)

`XuTheorem41Audit.lean` checks rational-number identities attributed to arXiv:2609.29250. It proves a numerical discrepancy and checks a corrected numerical example. This does not disprove the general theorem. The transcription must be checked against the paper before any public correction claim.

[Lean CI](../../actions/workflows/lean.yml). Only a successful workflow run with no `sorry` qualifies as Lean-verified.
