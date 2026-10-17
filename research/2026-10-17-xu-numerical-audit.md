# 2026-10-17 — Numerical identity audit (Xu, arXiv:2609.29250)

- **Status:** Lean-verified numerical statements; source transcription and novelty not yet independently audited.
- **Scope:** Exact rational-number expressions written in [XuTheorem41Audit.lean](../XuTheorem41Audit.lean).
- **Verified:** `1/540 + 1/51288 + 1/1521544 - 4/2137 = 23/102704220`, hence the two sides differ.
- **Verified:** `1/534 + 1/50712 + 1/1504456 = 4/2113`.
- **Lean evidence:** [successful CI job](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39014378628/job/117343326415), Lean 4.24.0 and Mathlib.
- **Caution:** These are checks of transcribed expressions. Compare against the exact paper text, equation numbers, errata, and mathematical context before alleging a publication error.
- **Not established:** Invalidity of the general theorem, originality, or significance sufficient for a paper.
- **Next step:** Audit the PDF line by line and identify the minimal general lemma, if any.
