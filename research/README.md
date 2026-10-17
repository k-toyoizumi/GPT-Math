# Research notebook / 研究ノート

This directory records work on the Erdős–Straus conjecture, including unsuccessful attempts.

## Evidence levels
- **Idea**: untested conjecture or heuristic.
- **Numerically checked**: reproducible computation, with stated range.
- **Mathematically proved**: a complete human-readable argument.
- **Lean-verified**: exact source file and successful GitHub Actions run are linked.
- **Novelty checked**: dated literature search and comparison with prior results.
- **Paper candidate**: proved, significant and novel enough to merit a manuscript.

These labels are independent: Lean verification does not establish novelty.

## Workflow
1. Create a dated note from [template.md](template.md).
2. Record precise statements, assumptions, attempts, counterexamples and sources.
3. Put reproducible experiments under `experiments/` and Lean proofs under `proofs/` (or link an existing root-level proof).
4. Record the commit and CI run URL; do not mark a theorem Lean-verified until the job passes.
5. Compare against prior work before moving a result into `paper-candidates/`.

**Never silently delete failed approaches.** Record why they failed so they are not repeated.
