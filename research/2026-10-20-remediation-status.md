# Remediation ledger and resumption contract

Scope: infrastructure only. T12/T13 and all new mathematics remain stopped.
Integration: `ci/lean-coverage-evidence-20261020-0338`. Baseline: `d2c933d2b77df7c858f60ffadf685c37527291c9`.

| Task | Implementation | Evidence required before acceptance |
|---|---|---|
| T01 | All 48 remote refs and baseline file differences recorded in branch-inventory.json | Snapshot; branch names are not proof status |
| T02 | Existing integration branch retained; no force pushes or merges | Parent SHA recorded by each commit |
| T03 | Exact Lean/Mathlib and full manifest digest; nine resolved revisions | Positive/negative CI controls |
| T04 | Six adopted sources explicitly registered; defaultTargets equal adopted build targets; unknown tracked Lean rejected | New-head `lake build` and coverage.json |
| T05 | Both original Python programs plus exact p=670849 certificate run unchanged in mathematical scope | experiments.json, CSV, logs |
| T06 | Isolated invalid Lean, sorry, axiom, dependency, Python, pipefail controls; inventory/artifact unit tests | faults.json and unit-tests.log from real Actions |
| T07 | Compiled Lean environment enumerates every theorem defined in adopted modules, including generated declarations | proofs.json: structural statement hash, source blob, axioms, trust |
| T08 | Adopt existing progression completeness and quantified divisor-set theorem from 9adfe595 | Exact source compilation; no success claim before log |
| T09 | SHA/tree/run/attempt metadata, full file checksums, always-upload, setup-failure fallback | Retrieved artifact and integrity validation |
| T10 | This ledger and handoff contract; failure categories; research stopped | Latest validated run linked in final acceptance record |
| T11 | Atomic handoff, explicit next action, duplicate fingerprint; two subprocess continuation test | CI unit log and handoff.json; hourly continuation disabled |

## Adoption decisions

- Retain the four existing Lean sources and original two Python experiments.
- Adopt `ProgressionCompleteness.lean`, `TypeIIDivisorComplete.lean`, and `verify.py` from fixed commit `9adfe595522f613a94c29d70ba1d2f2d3766874e`. Place Lean modules at project root; rename Python to `experiments/verify_certificate.py`. Add prime/positive-denominator assertions only. The bounded claim stays p=670849, 1<=u,a<=7, with witnesses at depth 8.
- Do not adopt the redundant `TypeIIDepthSeven_UNCOMPILED.lean`: the retained baseline already contains that finite Boolean search. The adopted quantified theorem separately covers all divisors, so the Boolean result alone is never described as completeness.
- Do not adopt the minimal-modulus exploration or other mathematical candidate branches: they are outside this infrastructure-only task. In particular `8212448...` fixed-x equivalence remains an unadopted candidate; existing reconstruction must not be overwritten.
- Previous automation branches are provenance only. The registry, current source blobs, and current run determine verification status; no green result on another branch is inherited.

## Trust and evidence

`kernel-checked` permits `propext`, `Classical.choice`, `Quot.sound`. `native-assisted` additionally permits the explicitly named native compiler bridge `Lean.ofReduceBool` / `Lean.trustCompiler`. Any other axiom, including `sorryAx`, fails. Native results retain extra compiler/runtime trust. No novelty claim follows from successful compilation.

`proofs.json` is generated from the compiled environment, not from theorem-name regex. Statement hash is SHA256 of Lean's structural expression representation under the fixed toolchain; source blob SHA and source SHA256 are separate fields.

Artifacts retain 90 days. Before expiry, copy the accepted run's run/proof/experiment/coverage/fault/handoff JSON, CSV, checksums and job log into `research/evidence/<source-sha>/` in a follow-up evidence-only commit; never edit the source SHA in that snapshot. A later documentation commit may reference that accepted source run without claiming its own new mathematical code was checked.

## Continuation and stopping

The external hourly remediation task was observed enabled and explicitly paused during this manual integration to avoid concurrent writers. The research-only hourly task was observed disabled. No hourly continuation is required after completion. Two-process state tests verify continuation/duplicate handling; they are not claimed to be two hourly scheduler deliveries.

For future authorized work: fetch this branch, inspect the latest acceptance record, compare the new source tree to accepted hashes, run `python3 scripts/verify_ci.py` in the pinned environment, inspect Actions and download the artifact. Use `scripts/handoff.py` to record task ID, input SHA, result hash, status and next action. Identical task/input/result is a repeat attempt, not progress. An existing state lock must be investigated before removal. Git ref updates must use an expected-head lease.

Failure classes: `not_executed`, `inventory_failed`, `dependency_failed`, `lean_failed`, `python_failed`, `artifact_failed`, `publication_blocked`, `stale_evidence`. On publication refusal record exact rejection and patch; do not bypass review.

On G1 acceptance stop. Do not resume mathematics, merge main, create schedules, or start W investigations automatically. The next action is to wait for explicit user direction in ordinary chat.
