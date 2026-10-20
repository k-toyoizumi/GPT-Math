# T12-G — Concrete finite residual-kernel bridge

## Input and scope

- Input research-branch head: `93b8e667986d9d02ad5537fa82ac5586f0695452`.
- The same-SHA documentation run `39471750443` had succeeded before this
  unit was started.
- This unit connects the definition `innerKernel wArithmetic` to one explicit
  finite double weighted-Möbius sum.  It does not yet evaluate that sum on
  prime powers or prove a finite Euler-product factorization.

## Result

For any two-variable arithmetic function `A`, natural numbers `r,t`, and
`t ≠ 0`, the new theorem `innerKernel_explicit` states

\[
K_A(r,t)=
\sum_{y_1y_2=t}\sum_{x_1x_2=r}
 \frac{\mu(y_1)}{y_1}\frac{\mu(x_1)}{x_1}A(x_2,y_2).
\]

Here the displayed fractions abbreviate the already-defined
`weightedMoebius`.  The theorem is a direct finite expansion of Dirichlet
convolution in the second coordinate and scalar convolution in the first.
The specialization `innerKernel_wArithmetic_explicit` replaces `A` by the
concrete `wWeight` used in `W(J)`.

This closes the definitional gap between the abstract residual kernel and a
finite sum whose prime-power cases can be evaluated.  It does **not** show
that the kernel is multiplicative: that requires a separate normalization
and a proof that the coprimality/totient weight factors across disjoint prime
support.

## Candidate verification record

- Corrected candidate source SHA-256:
  `5f86180ed41fdbdb209fd37842e6c754f1c18ac7ccca214fb7ca59e4e197c3eb`
- Corrected candidate semantic result hash:
  `c0ab91d9baa96f7bc5004ab973de183e218dd55290ab1859c869687055bd0cb7`
- Statement hash, `innerKernel_explicit`:
  `4be4dc4eb8ec13e38546fd773f2ff556c197c4d2d4f04a27c906ed4f22b30c4a`
- Statement hash, `innerKernel_wArithmetic_explicit`:
  `fef61bcee257dcb9f764c6017fbf7999ba89e1709c7b17ffd382cb4cd3d21ae4`

Local execution was unavailable because `lake` is not installed in the
available runtime.  The corrected exact source was instead executed by GitHub
Actions and is **verified for the two finite identities stated above**.

The first published candidate (`eb6b0e5c2ff0f3c3d4810c8a07b49bbbec34c42d`,
source SHA-256 `4d9bb531...b33555`) failed run `39480452833` in the
`lean` job (`118827317860`).  Lean reported an unsolved `y.2 = 0` branch at
the `innerSource` simplification; the axiom audit consequently exposed
`sorryAx`.  The negative-control job (`118827317298`) succeeded.  The
corrected candidate isolates the nonzero-slice equality before expanding the
outer convolution.  The failed source is not treated as verified.

Corrected verification evidence:

- research-branch source commit:
  `0bbcfa982812591834a56e04429d224e88d6d59d`
- tested PR merge SHA: `0b01142c91f9ffca899ccdf3fb040b1040afeee8`
- Actions run `39481126679`, attempt 1, success
- jobs: `lean` (`118829666912`) and `failure-evidence`
  (`118829666573`), both successful
- verification artifact `12290224756`,
  `sha256:e13236d1cb44f8a42f0a90fc8b90e8cc97fe85d943beeb55fcc4f520467c6739`
- negative-control artifact `12291691399`,
  `sha256:2c6d29d51c7d78a21db4530050def5c75fdd1519040eefdf205970e8bd30c739`
- source blob `025f808ba8d757cb544b3f821fb1ccf59c704563`
- source SHA-256
  `5f86180ed41fdbdb209fd37842e6c754f1c18ac7ccca214fb7ca59e4e197c3eb`
- semantic result hash (the two CI statement hashes, in theorem order):
  `81857fa141cef0a5057452b794d328ac92ede26d9ed9b6615474e15c43f3cc6f`

CI statement records:

| theorem | statement hash | axioms / trust |
|---|---|---|
| `innerKernel_explicit` | `0d64dad348c9b18ae71b4b92cb83c0dd15d06bd0aee6c29bfb7af7f0bca3676b` | `propext`, `Classical.choice`, `Quot.sound`; kernel-checked |
| `innerKernel_wArithmetic_explicit` | `6e795605aa3617ca60c28cc03783e7a0eb9b68ed573c84f3bdcca6201debe8b8` | `propext`, `Classical.choice`, `Quot.sound`; kernel-checked |

Neither selected theorem uses `sorryAx`, native decision, or
`Lean.trustCompiler`.  The repository still contains separately labelled
native-assisted finite-search theorems; they are not dependencies of these
two results.

## Separate assessments

- **Formal correctness:** verified for the displayed finite expansion and its
  `wArithmetic` specialization at the exact source and evidence above.
- **Novelty:** no novelty claim; this is an explicit finite convolution
  identity.
- **Research value:** it makes the next prime-power calculation refer to the
  actual `W(J)` kernel rather than to an independently written local table.

## Still unverified

Prime-power support and coefficients, finite Euler-product factorization,
absolute summability, logarithmic moments, tail estimates, the infinite Euler
product, and the asymptotic
`W(J)=9/(2π²)(log J)²+O(log J)` remain unverified.

