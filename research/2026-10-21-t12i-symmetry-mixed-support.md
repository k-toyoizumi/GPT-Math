# T12-I — Symmetry and same-prime mixed support

## Input and scope

- Input research-branch head: `2c4c5b5cbec2039ac76452f74375caa3189909ef`.
- Its Actions run `39492230599` succeeded in both jobs.
- This unit proves only coordinate symmetry of the concrete normalized weight,
  the second-axis odd-prime-power value, and vanishing when positive powers of
  the same prime occur in both coordinates.
- It does not yet evaluate `innerKernel wArithmetic` at prime powers or prove
  a finite Euler-product factorization.

## Candidate statements

1. `wWeight u a = wWeight a u`.
2. `normalizedWWeight u a = normalizedWWeight a u`.
3. For odd prime `p` and `e > 0`,
   `normalizedWWeight 1 (p^e) = 1 / (p^(e-1) * (p-1))`.
4. For prime `p` and positive `e,f`,
   `normalizedWWeight (p^e) (p^f) = 0`.

The fourth statement follows from the original coprimality condition, using
`Nat.coprime_pow_left_iff`, `Nat.coprime_pow_right_iff`, and
`Nat.Prime.dvd_iff_not_coprime`.  No finite enumeration is used.

## Pre-publication backup

The execution environment was unavailable, so a ZIP could not be produced.
Before changing the branch, the complete candidate source was saved as an
unreferenced Git blob:

- candidate source blob: `6550ae0abd5f8f050d509e0d768d3d430ed13877`
- candidate source SHA-256: `ecec88ab100a5db452969562286aea7504c6ffa4a9d23d3821fdab979c1e6e2a`
- candidate semantic hash: `b35983596731ee0e02957bc1761eea4c3d6f4bfa62320d40ac75aa8bf0be6d20`
- statement hashes, in theorem order:
  - `ce5da97bced330989b3744ae1005a396461e89703dbacd875542be15dfe048dc`
  - `6df61d9c27bbfe6f5af45706a2147fd8910915a655244cd0528a799b7ca20f6c`
  - `6e916a17119ea2f9be5f3d126b01f9630e46b9c3897a9c1206a4b967aeb2b8f8`
  - `8c1441b93cde76e4aed137a7539dcde2fa366e6a64dbb8f6d8c0bc9facbe3db6`

Status at backup time: **not executed locally and not verified**.  The exact
candidate source subsequently passed repository CI:

- research-branch source commit: `7a179db9fe735310ef1af26d29190b393655d0c5`
- PR test-merge source SHA: `53bad71aa8b5f633b14b25da1478eb984bf7dc7b`
- source blob: `6550ae0abd5f8f050d509e0d768d3d430ed13877`
- source SHA-256: `ecec88ab100a5db452969562286aea7504c6ffa4a9d23d3821fdab979c1e6e2a`
- Actions run/attempt: `39493614349` / `1`
- jobs: `lean` `118872845538` success; `failure-evidence`
  `118872846039` success
- verification artifact: `12295704819`,
  `sha256:a32e4ded42424bc19c262cf904fdb3b9920c45e8e9569de2ea62cfc31daefe4e`
- negative-control artifact: `12296274592`,
  `sha256:ec6d1cebe4c969a5585ee017b3961bb3c4ab1aac37173e2e26d586b83d0a1f7a`

The successful `evidence_gate` checked the generated evidence, and the Lean
job log reports all four theorems with exactly the axioms `propext`,
`Classical.choice`, and `Quot.sound`.  No `sorryAx`, native-decision, or
compiler-trust dependency appears.  The execution environment was unavailable,
so the artifact ZIP itself was not locally extracted; its ID, digest, source
SHA, successful evidence gate, and theorem-level axiom logs were checked.

## Separate assessments

- **Formal correctness:** verified for the four finite statements at the exact
  source and CI identifiers above.
- **Novelty:** no novelty claim; these are elementary consequences of symmetry
  and coprimality.
- **Research value:** these lemmas provide the missing concrete inputs for
  comparing both axes and the same-prime mixed cell with the T12-F local table.

## Still unverified

Actual residual-kernel prime-power coefficients, finite Euler-product
factorization, absolute summability, logarithmic moments, tail estimates, the
infinite Euler product, and the asymptotic formula for `W(J)` remain
unverified.
