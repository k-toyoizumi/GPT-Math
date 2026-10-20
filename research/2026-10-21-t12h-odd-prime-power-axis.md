# T12-H — Odd-prime-power specialization of the concrete weight

## Input and scope

- Input research-branch head: `0a715cb35466632c5ccbbcca3f1f8ed14ff2719f`.
- Its Actions run `39481905839` succeeded in both jobs before this unit.
- This unit specializes the actual normalized weight `2 * wWeight` on a
  coordinate axis.  It does not yet evaluate `innerKernel` itself on prime
  powers and does not prove a finite Euler-product factorization.

## Candidate result

Define

\[
  F(u,a)=2\,wWeight(u,a).
\]

The first theorem shows that if `n ≠ 0` and `2 ∤ n`, then

\[
  F(n,1)=\frac1{\varphi(n)}.
\]

The proof uses the concrete definition of `wWeight`, coprimality of `4` and
`n`, Mathlib's finite identity
`Nat.totient_mul`, and `φ(4)=2`.  Thus the normalization factor is not an
informal constant transfer.

The prime-power corollary uses `Nat.totient_prime_pow`: for prime `p`,
`2 ∤ p`, and `e>0`,

\[
  F(p^e,1)=\frac1{p^{e-1}(p-1)}.
\]

This is exactly the odd-prime axis input assumed by the T12-F local table.
It therefore connects that table to the concrete `1/φ(4ua)` weight on one
axis, but it does not yet prove the weighted-Möbius differences or their
factorization across a finite set of primes.

## Verification record

- Sixth candidate source SHA-256:
  `35a707e0d2af7b279c0ae5b7bd9d002ec812dee7be153424971bf176a2f0b6c3`
- Sixth candidate theorem-block hash:
  `2906f4555bda462ba14270ae496b3c209ebe8c7ab9203e04b892c04eb0dc7dab`
- Source-level statement hash, `normalizedWWeight_axis_of_two_not_dvd`:
  `653017e7792dd9dee52ba094d57f11c6594ad7eee23069b3df9f9866d1b1a2a6`
- Source-level statement hash, `normalizedWWeight_odd_prime_pow_axis`:
  `ff28a4fa865078015f8f83411f98e34a0bfb5ac6d26cdccca55cee6a731d0d5c`

Status at candidate-backup time: **not executed locally** because `lake` is
not installed in the available runtime.  The sixth candidate was subsequently
verified by the repository CI:

- research-branch commit: `a10e05e13f0000a4a2d1deb4d40e50f707510ea4`
- PR test-merge source SHA: `35d242867a366dad0f7b94acefa98b0265f025f4`
- content blob: `171fab8bcb97cacec440d034f29ccca6a70612e9`
- Actions run/attempt: `39491539197` / `1`
- jobs: `lean` `118865684612` success; `failure-evidence` `118865684931`
  success
- verification artifact: `12296630965`,
  `sha256:6f83812eacb228a1848e2760b0a83673e5e9d2ded2da89ea9418304cdb833236`
- negative-control artifact: `12296430923`,
  `sha256:f464c367ab7b42b22407e593432f005e5d85e4be68e4c0cf16c9ccf5de4f8af1`
- CI statement hash, `normalizedWWeight_axis_of_two_not_dvd`:
  `d0142cf3ada688ae070ee67375c4f4da49133bb303bfe60237949a5998c90056`
- CI statement hash, `normalizedWWeight_odd_prime_pow_axis`:
  `ecee570e1b539d3409daed8c80c67d683858d3efd572ce951dcabf01d72e2125`
- semantic result hash (the two CI statement hashes in theorem order):
  `d44b84e70d703e41b566d1f339c9cb020c9959ae5e2947e14466d92f2478a03b`

Both theorem records are `kernel-checked`, depend only on `propext`,
`Classical.choice`, and `Quot.sound`, and contain no `sorryAx`, native-decision,
or compiler-trust dependency.

The first published candidate (`330d57c9a32243a63f361fc369df02a3fdc7e77b`,
source SHA-256 `eedfd285...26e651`) failed run `39488693672` in
the `lean` job (`118855731354`).  The log reported `Unknown identifier` for a
helper theorem declared later in the file; the resulting unsolved goal was
correctly exposed as `sorryAx`.  The negative-control job (`118855730838`)
succeeded.  The corrected candidate unfolds `wWeight` directly and does not
treat the failed source as verified.

The second candidate (`aa035f8c83e3da04e56a02a8e5ff19191292b59c`)
removed the declaration-order error, but run `39489314771` still rejected an
unsolved final equality because `φ(4)=2` was not reduced automatically.  The
third candidate (`524e5121e8f9e8e796641d60f1fe68e0e457c3b8`)
also failed run `39489806830`: direct `norm_num [Nat.totient]` left the
finite-cardinality goal for `φ(4)` unsolved, and the final rational
normalization equality was still open.  The fourth candidate instead derives
`φ(4)=2` from `Nat.totient_prime_pow Nat.prime_two` and closes the remaining
rational identity with `ring`; it does not use `native_decide`.

That fourth candidate (`38cf105d3af0c00ab21675a582baf223d9969d44`)
failed run `39490410472` because `ring` deliberately treats inverses as
atoms: the remaining goal was
`(↑(n.totient * 2))⁻¹ * 2 = (↑n.totient)⁻¹`.  The fifth candidate explicitly
rewrites casts and the inverse of a product, then normalizes the rational
factor.  Run `39490410472` has verification artifact `12294419997`
(`sha256:116ffa349936b5bca58c433a4ac9ec22107fccfc44565c8be20520ed4dcdd71d`);
its `lean` job `118861760721` failed and negative-control job `118861761169`
succeeded.

The fifth candidate (`9673ae37d82e9413f58f6898a669a06d6ceeca2f`)
failed run `39491006810`: the cast and inverse-product rewrites worked, but
`norm_num` left the purely commutative identity
`2 * ((↑n.totient)⁻¹ * (1 / 2)) = (↑n.totient)⁻¹`.  The sixth candidate
applies `ring` only after reaching that form.  Run `39491006810` has
verification artifact `12295257854`
(`sha256:6ceb9d568804c5144af60e9f1326f8dbf0d06e015bb7e3894b7052ec4ec8782f`);
its `lean` job `118863869655` failed and negative-control job `118863869791`
succeeded.

## Separate assessments

- **Formal correctness:** verified for the two displayed finite axis theorems
  at the exact source and CI identifiers above.
- **Novelty:** no novelty claim; the totient of an odd prime power is standard.
- **Research value:** this removes one conditional premise from the T12-F
  local calculation by deriving its axis input from the repository's concrete
  `wWeight` definition.

## Still unverified

The second-axis symmetry, the mixed positive-exponent zero, actual
`innerKernel` prime-power coefficients, finite Euler-product factorization,
absolute summability, logarithmic moments, tail bounds, the infinite Euler
product, and the claimed asymptotic for `W(J)` remain unverified.

