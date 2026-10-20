# G1 acceptance and ordinary-chat handoff

Date: 2026-10-20 (Asia/Tokyo). Scope: research infrastructure remediation only.
**G1 is satisfied for the integration candidate. Mathematics remains stopped. Main has not been merged.**

## Accepted implementation and actual execution

- Integration branch: `ci/lean-coverage-evidence-20261020-0338`.
- Implementation head: [`3a805415e6e33a9ab2665d285b45f4961bd91f69`](https://github.com/k-toyoizumi/GPT-Math/commit/3a805415e6e33a9ab2665d285b45f4961bd91f69).
- PR: [#2](https://github.com/k-toyoizumi/GPT-Math/pull/2); main merge requires user approval.
- Accepted full workflow: [39415127573](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39415127573), attempt 1, event `pull_request`, conclusion `success`.
- Actual tested PR merge SHA: `b3efc0fa91f4ed8d3402166a6a29748321b69a6a`; PR head SHA: `3a805415e6e33a9ab2665d285b45f4961bd91f69`. These are deliberately separate fields in run.json. No main merge occurred.
- Successful proof job: [118602182607](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39415127573/job/118602182607).
- Artifact: [12260737458](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39415127573/artifacts/12260737458); downloaded ZIP digest `c8babb888d16b87dba738bde52d90ae34e290362b3adb1e6cf8508002cc9af8d`. Every upstream file checksum and every structural statement hash was independently rechecked after download. Every proof source blob matches the candidate source.
- Persistent mandatory evidence: [tested merge source snapshot](evidence/b3efc0fa91f4ed8d3402166a6a29748321b69a6a/). Its provenance identifies the tested source; the later documentation/snapshot commit is not substituted for that source.

## G1 checklist

| Acceptance condition | Result and evidence |
|---|---|
| All adopted Lean and required Python executed | PASS: six adopted Lean modules built using ordinary `lake build`; three Python programs reproduced; 15 unit tests passed |
| Valid dependencies pass; changed dependencies and coverage holes rejected | PASS: nine pinned packages, full-manifest digest, isolated corrupt/missing/version controls; unknown root/nested tracked Lean fixtures rejected; dedicated corrupted-dependency job rejects through the production verifier |
| Every adopted theorem's axiom/native dependencies explicit | PASS: compiled environment enumerated 26 theorem declarations, including generated helpers; all name/statement-hash/source-blob/axiom/trust rows persisted. Five rows are native-assisted (three user-facing theorems plus two helpers); all others kernel-checked under the listed standard axioms |
| Artifacts tied to SHA/run/attempt obtainable | PASS: run/coverage/proof/experiment/fault/handoff JSON, CSV, logs and checksums downloaded and verified; both positive and negative artifacts retrieved |
| Fresh environment reproduces same finite result | PASS: independent clean GitHub-hosted jobs reproduced the identical certificate CSV: 35 coprime pairs, 426 divisors, no depth<=7 witness; depth 8 has u=8,a=1,s=319 and 7711. These are pre-existing finite results, not new research |
| Notes match actual verification state | PASS: current ledger and adoption registry distinguish adopted sources, archived candidates, earlier failures and exact accepted execution. Historical notes are preserved and linked to the new status |
| If hourly operation continues, continuity and dedup validated | NOT APPLICABLE to continued scheduling: hourly remediation and research are stopped. The handoff mechanism itself passed two independent subprocess invocations plus a two-attempt evidence record with progress_count=1. No claim of two hourly deliveries is made |

T01–T11 are implemented and accepted within this stopped-operation scope. T12/T13 have not started.

## Reproduction and failure evidence

- Initial clean integration: [39413799356](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39413799356), source `baa0f2ccc69cfc47acca4702f593b959cbac2bd3`, attempt 1, success. [Original artifact snapshot](evidence/baa0f2ccc69cfc47acca4702f593b959cbac2bd3/). Its initial source-name audit was later superseded by compiled-environment enumeration; do not use its 14-name list as the final complete audit.
- Independent clean full-environment audit and failure-retention controls: [39414485885](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39414485885), source `845d7e56572216d8f8057f426f989658965605c0`, success. [Persistent snapshot including deliberately rejected dependency evidence](evidence/845d7e56572216d8f8057f426f989658965605c0/). Certificate bytes match the first clean run and the final accepted run.
- Deliberate faults: invalid Lean, sorryAx, custom axiom, missing/modified/mismatched dependency, damaged Python expectation, and a failing pipe retain rejection semantics. Unit tests additionally reject unknown tracked Lean, missing/stale evidence and checksum corruption. The outer negative-control job is green only because its inner production verifier actually failed as expected.
- A transient toolchain-download TLS error occurred in [39415121593](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39415121593), job 118602162679. It is `not_executed`, not proof failure or success. The setup-failure artifact was saved (12262010175). The separate PR execution of the same implementation succeeded in a fresh environment. No dependency pin was changed to work around the network error.
- The diagnostic 90-second audit limit in superseded source `5cf482...` was below observed full-environment enumeration time and timed out in [39414884411](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39414884411). Root cause: `EnvironmentHeader.moduleNames` maps all imported modules, so recomputing it for every declaration repeated work proportional to declarations × modules. Caching it once reduced accepted audit time to about 6.7 seconds. All subprocess stages now have a 300-second limit and retain partial logs on timeout. A failed or timed-out audit is never accepted.

## What changed

Dependency checks now bind all nine resolved packages, rather than checking only the shape of SHA strings. The source registry aligns coverage and default Lake targets, and includes the pre-existing progression and quantified divisor-completeness files. Existing Python experiments and the independent finite certificate run in real CI. The theorem audit operates on the compiled environment, includes generated helpers, and rejects unapproved axioms. Evidence checks enforce run identity, checksums, mandatory files and failure preservation.

Handoff records carry task ID, source SHA, semantic result hash, status and next action. Identical task/input/result is not counted as new progress. Writes use an exclusive lock and atomic replacement. Semantic result hashes omit run-ID timestamps and verbose statement copies, so a new CI run alone is not new mathematical progress.

## Residual limits

- Native-assisted finite theorems retain trust in Lean's native compiler/runtime bridge. They are not relabelled kernel-only.
- Theorems and finite checks establish their stated scope only; neither novelty nor the general Erdős–Straus conjecture follows.
- Full raw GitHub artifacts expire after 90 days. Required proof metadata, source hashes, CSV, run records and stage/job logs are stored in git. Persistent proof JSON omits only the verbose optional structural statement string; its verified statement hash remains. See [snapshot format](evidence/README.md).
- External download failures can still prevent execution; they are classified as not executed and do not become green proof evidence.
- No two-hour external scheduler-delivery guarantee is claimed because recurring operation is stopped. Re-enabling it requires a new explicit instruction and delivery-level validation.

## Ordinary-chat starting point

1. Read this acceptance record and [remediation ledger](2026-10-20-remediation-status.md); fetch the integration branch and inspect PR #2's latest checks.
2. For a future authorized code change, keep the exact toolchain and manifest, update the explicit source registry when needed, run the complete workflow, and inspect/download the new source's evidence. Never inherit old verification after modifying proof or experiment code.
3. Reuse [continuation-state.json](continuation-state.json) for task continuity with `scripts/handoff.py`; inspect input/result hashes before deciding whether progress is new. The state currently says to stop and wait for authorization.
4. The immediate next operation is **wait for user direction**. Do not resume mathematics, start W investigations, merge main, or re-enable schedules automatically.

The external remediation task `6ad3c0e624dc819180f7c97bbb599b7d` was explicitly paused; research task `6ad2f9cf31a08191b05515931207c9c8` was observed disabled. Other unrelated tasks were not modified.
