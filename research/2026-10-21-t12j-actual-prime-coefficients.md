# T12-J — Actual odd-prime residual-kernel coefficients

## Input and scope

- Input research-branch head: `5c15b5d542085360e2bb3eba041e555c47cd0578`.
- Latest `main`: `3802f98cb272791ba6c0dc8d1a9cc21b7648804f`; run `39419058414` succeeded for that exact SHA.
- This unit specializes `innerKernel_wArithmetic_explicit` at one odd prime and connects the actual concrete kernel to the T12-F rational table at exponent pairs `(1,0)`, `(0,1)`, and `(1,1)`.
- It does not prove the remaining prime-power support, a finite Euler product, an infinite Euler product, absolute summability, logarithmic moments, tail estimates, or the asymptotic formula for `W(J)`.

## Verified statements

For an odd prime `p`, Lean proves:

[
2K(p,1)=\frac1{p(p-1)},\qquad
2K(1,p)=\frac1{p(p-1)},\qquad
2K(p,p)=-\frac{p+1}{p^2(p-1)},
]

where `K(r,t) = innerKernel wArithmetic r t`.  The factor `2` is exactly the normalization already encoded by `normalizedWWeight`.

The proof first expands the actual finite double weighted-Möbius transform over `p.divisorsAntidiagonal`, rewrites it through `Nat.sum_divisorsAntidiagonal` and `Nat.sum_divisors_prime_pow`, reduces `μ(p)=-1`, and then invokes the previously verified normalized axis and same-prime mixed-support formulas. No finite enumeration is used.

## Exact source and CI evidence

- Source commit: `8c3c4abdfc89b72832f18e541eace32c123c4307`
- PR test-merge SHA: `d92890201f73a79e88f2100510f45c0170388652`
- Source blob: `c904b998f7ee50ad6de9b0232ef5a6b2f18a9c91`
- Source SHA-256: `25c0f0fcab905fb821dad94d1f2edfd8864424f16c7a8b565d95d0c80a1c7027`
- Actions run/attempt: `39501530517` / `1`
- Jobs: `lean` `118899956465` success; `failure-evidence` `118899956065` success
- Verification artifact: `12302015176`, `sha256:97722c7900b42d0d761046f3fd7d884c3c0467d8b43955e3ea1577dd44536113`
- Negative-control artifact: `12301410782`, `sha256:d60f6e67602e77f85cbae6f42479ed1fbdf9133bee9f672233be75f508481176`
- Semantic result hash: `89f88ea7bdb5c49bdb3c93cba3ecc0b70f377ea6b15793c5fae69a64a483d4d6`

Exact declaration hashes (SHA-256 of the source declaration text through `:= by`):

- `innerKernel_wArithmetic_prime_one`: `a8a0f6121b40b1772a99476754ae210c8b4e01bc775da6c0fb585cf041bd3fc0`
- `innerKernel_wArithmetic_one_prime`: `e6c093b1e34d119148cb6af710c817110f27f89ac1b95c267c7c89bc57705d37`
- `innerKernel_wArithmetic_prime_prime`: `2d0b36f17e359fca103d1a3ab7888325b33ccc57972224fd4b32210940b6bd4d`
- `normalized_innerKernel_wArithmetic_odd_prime_axis`: `d58a41c721996fc25fa5f76a5621eb133e11e3ee327311a7bd56e4c40c3c7b0b`
- `normalized_innerKernel_wArithmetic_one_odd_prime_axis`: `be4a0280d2d2879907bdf3d510e8e332d86c4a77f302c36536e46df90abaa574`
- `normalized_innerKernel_wArithmetic_odd_prime_diagonal`: `3bfedd23baa6afdb06cd4291de8acf26b64d64018b2c7b798125c60b2fc662e0`

The Lean log reports all six new theorems with exactly the axioms `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx`, native-decision, or compiler-trust dependency in these theorems. The verification artifact passed the repository evidence gate. The execution environment was unavailable, so the artifact ZIP was not locally extracted; artifact metadata, digest, source SHA, successful jobs, evidence gate, and theorem-level axiom logs were checked.

## Failed candidates and repair

The first nine CI runs for this unit failed and are not verification evidence: `39496247386`, `39497001329`, `39497461823`, `39497918537`, `39498360138`, `39498771244`, `39499194084`, `39499637652`, and `39500055017`.

The failures exposed, in order, unresolved divisor-antidiagonal sums, natural-to-rational cast normal forms, the normalized origin calculation, a diagonal negation normal form, the positivity premise for `Nat.div_self`, and the missing explicit reduction of `ArithmeticFunction.moebius_apply_prime`. The final proof makes each of these steps explicit. Failed runs were not reused as success.

## Separate assessments

- **Formal correctness:** verified for the six finite statements at the exact source and CI identifiers above.
- **Novelty:** no novelty claim; these are elementary local coefficient identifications.
- **Research value:** this closes the concrete-definition gap for the three nontrivial exponent-one cells. It does not yet prove that all higher prime-power cells vanish.

## Pre-publication recovery

Every candidate source was stored as an unreferenced Git blob before branch publication. The final full-audit candidate blob is `c904b998f7ee50ad6de9b0232ef5a6b2f18a9c91`. Earlier T12-A/T12-B ZIPs and the original rejection text remain unavailable.
