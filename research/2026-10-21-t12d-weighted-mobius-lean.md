# T12-D: finite weighted Möbius inversion in Lean

## Scope and result

Task input was research-branch head `65cd80e79ed8b28e8eba0450355945d51e2c530e`.
`WMobiusFinite.lean` now proves, over rational-valued arithmetic functions:

1. coefficient division by `n` respects Dirichlet convolution;
2. the kernels `n ↦ 1/n` and `n ↦ μ(n)/n` are convolution inverses;
3. one-coordinate reconstruction; and
4. a finite two-coordinate reconstruction on divisor antidiagonals, for a positive second index.

The source file SHA-256 is
`7d562475cf5d99fe25865b4d8429b7522eefe34fe6bae51e4f30cac7a73898d9`.

## Verification evidence

- Research head: `e327a16208f71773cc33e68d76da8322b65a4dc2`
- Pull-request merge ref checked by Actions: `15344452bf6a02c425a3ce806559ef62153bdba4`
- Actions run: `39458226341`, attempt 1
- Lean job: `118750565863`, success
- Negative-control job: `118750566307`, success
- Verification artifact: `12282050743`, digest
  `sha256:8331e87326cb9a076ff140bc5e8eeba91968aa1eb3f7719f9af01c4c354bd8ea`
- Negative-control artifact: `12280628980`, digest
  `sha256:670f61f9b24c7e62e67edf0b926c7d95b1d3939355825f060121c9289ed1ffe2`
- Lean 4.24.0 / Mathlib revision
  `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`

Key statement hashes from `proofs.json`:

| theorem | statement hash | trust / axioms |
|---|---|---|
| `divideByN_mul` | `b7741509bc05be083d3de23613cf89ac722ef280364617c9bb9c2e29952313dc` | kernel-checked; `propext`, `Classical.choice`, `Quot.sound` |
| `weightedZeta_mul_weightedMoebius` | `6996570a6610b1fb1ab282ea339e071a2a5cad4306616bf0eb298de09990975a` | kernel-checked; same standard axioms |
| `finite_double_reconstruct` | `b242e9a344abb0f214e8443d7b7bdb971f6fa32827d3d9b2e1e0d809fda63013` | kernel-checked; same standard axioms |

No `sorryAx`, `Lean.ofReduceBool`, or `Lean.trustCompiler` occurs in these
three theorem dependencies.

## Failed attempts retained as evidence

Runs `39455248679`, `39456202413`, `39456863075`, and `39457673746`
failed before the successful run. Their artifacts identified, respectively:

- unfolding and ambiguous Möbius notation errors;
- a missing pointwise module structure for nested arithmetic-function values;
- explicit function-evaluation requirements; and
- an over-broad rewrite that changed the kernel argument on both sides.

Each corrected candidate and its preceding failure log was backed up before
publication. These failures are not formal results.

## Mathematical boundary

This verifies only an exact finite algebraic identity. It does **not** prove
the proposed asymptotic

\[
W(J)=\frac{9}{2\pi^2}(\log J)^2+O(\log J).
\]

The concrete weight `1/φ(4ua)`, the coprimality restriction, absolute
summability, logarithmic moments, tail estimates, and the Euler-product limit
remain unformalized. Formal correctness of the finite identity is verified;
novelty and research value of the asymptotic remain separate and unresolved.

## Next minimal operation

Specialize the finite identity to the concrete two-variable weight and state
the precise analytic hypotheses needed to pass from the finite identity to the
asymptotic. Do not label the asymptotic verified until those analytic steps are
proved and checked at the corresponding source SHA.
