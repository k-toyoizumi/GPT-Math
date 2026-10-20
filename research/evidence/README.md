# Persistent verification evidence

Each source-SHA directory identifies exactly the source that was executed.
The snapshot commit is later and must not be substituted for that source SHA.
Artifacts were downloaded through GitHub, ZIP SHA256 compared with GitHub's
digest, then every upstream file checksum verified before snapshot creation.

`baa0f2c.../artifact/` retains the first integration artifact verbatim.
Later snapshots project `proofs.json` by dropping only the large optional
structural statement string; statement hashes, theorem names, source blobs,
trust labels, all axiom dependencies, run ID and attempt remain. The original
artifact checksum manifest is `upstream-SHA256SUMS`; it describes original
bytes, not the projection. Re-running the fixed source regenerates the exact
statement strings. The redundant full axiom JSON log is omitted in projected
snapshots; proofs.json retains its complete results. Other stage logs and
JSON/CSV are copied unchanged. `SNAPSHOT-SHA256SUMS` checks the persistent files.

`negative-control/` is deliberately rejected verification, not successful
proof evidence. `provenance.json` records upstream artifact identities and
checksums. Full upstream artifacts have a 90-day retention window; the
required proof metadata and reproducibility inputs remain here permanently.
