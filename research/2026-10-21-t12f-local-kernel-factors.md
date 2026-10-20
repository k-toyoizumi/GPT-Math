# T12-F — Residual-kernel local factors and first absolute bound

## Input and scope

- Input branch head: `11c02f120f12a5cfed5c6ca61210f6ab009b17e9`.
- This unit derives the prime-local algebra following the verified finite
  reconstruction.  It does not prove the infinite Euler product or the
  asymptotic for `W(J)`.
- To restore multiplicativity at the origin, put `F(u,a)=2 wWeight(u,a)` on
  positive inputs.  Then `F(1,1)=1`, while the kernel for `wWeight` is
  one half of the normalized kernel for `F`.

## Local calculation

Let `β_p(e,f)` be the local factor of `F`.  Coprimality forces
`β_p(e,f)=0` when both exponents are positive.

For an odd prime `p`,

\[
β_p(0,0)=1,\qquad
β_p(e,0)=β_p(0,e)=\frac1{p^{e-1}(p-1)}\quad(e\ge1).
\]

Applying the weighted Möbius difference in both coordinates gives support only
at `(0,0),(1,0),(0,1),(1,1)`:

\[
κ_p(0,0)=1,\quad
κ_p(1,0)=κ_p(0,1)=\frac1{p(p-1)},\quad
κ_p(1,1)=-\frac{p+1}{p^2(p-1)}.
\]

Consequently,

\[
\sum_{e,f\ge0}κ_p(e,f)=1+\frac1{p^2}.
\]

At `p=2`, the normalized local weight is
`β_2(e,0)=β_2(0,e)=2^{-e}`.  The axis Möbius differences vanish and
`κ_2(1,1)=-1/4`, so the signed two-adic mass is `3/4`.

The original unnormalized kernel therefore has the conditional total mass

\[
\frac12\cdot\frac34
\prod_{p\text{ odd}}\left(1+\frac1{p^2}\right).
\]

Using the still-to-be-formalized Euler-product identity

\[
\prod_{p\text{ odd}}(1+p^{-2})=\frac{12}{\pi^2}
\]

transfers this to `9/(2π²)`.  The Lean theorem
`candidate_constant_transfer` checks only this final algebraic transfer, not
the Euler-product premise.

## First absolute-convergence comparison

The excess of the odd-prime absolute local mass over one is

\[
E_p=\frac{2}{p(p-1)}
 +\frac{p+1}{p^2(p-1)}
 =\frac{3p+1}{p^2(p-1)}
 \le \frac8{p^2}\qquad(p\ge2).
\]

Thus the local product is dominated by a convergent `Σ_p p⁻²` comparison.
The algebraic inequality is a Lean target in this unit.  Passing from these
local bounds to an absolutely convergent two-variable series still requires a
formal Euler-product/Tonelli argument and is not claimed here as Lean-verified.

The same finite-support calculation suggests stronger weighted estimates:
for any fixed `0<δ<1/2`, the simultaneous `(1,1)` term is
`O(p^{-2+2δ})`, while the axis terms are `O(p^{-2+δ})`.  A proved global
`(rt)^δ` moment would imply a power-saving kernel tail.  This is the next
analytic target; it is not established by the present local identities alone.

## Verification status

Candidate source SHA-256 before publication:
`28b501e4746f526e96c3e8178bcfdf5d12a4e60ef52ea65a5ad480b56991af7b`.

Status: **verified for the listed local algebra and comparison inequality**.
The exact PR head `5000e6c4805c2c3f1ab32e5b01825a904a71ba0f`
was checked by Actions run `39471118090`, attempt 1.

Evidence:

- tested PR merge SHA: `4e4acfa30efa6857d2cdf56d3fc111b05f78bcc2`
- jobs: `lean` (`118795112829`) and `failure-evidence`
  (`118795113183`), both successful
- verification artifact: `12286693375`,
  `sha256:02dc22cd4121714a47ff33ff2ceeffc0ef9ba96d01854ef47f7b31934236c826`
- negative-control artifact: `12287826246`,
  `sha256:47ded51554d43bc933b1564aa7431da110eddbb59d157ed8d3f2f68882d18c21`
- source blob: `2240a1430ec687c366101b3bb617f671d2795133`
- source SHA-256:
  `28b501e4746f526e96c3e8178bcfdf5d12a4e60ef52ea65a5ad480b56991af7b`
- CI semantic result hash:
  `a84464fd735b8f7d4bedbc5c2ff4e5e8561d4191f5e92c37aa8828ce976929e1`

Selected statement hashes:

| theorem | statement hash |
|---|---|
| `odd_axis_from_weighted_moebius` | `5643657d0244ae9f44751293998ae18525d9c870c7f4166289c9624680f77120` |
| `odd_diagonal_from_weighted_moebius` | `d8faf3c0dca3e43e89553bd427a85da8d0a9ac821fd2120e7c440524615d8540` |
| `odd_local_mass` | `1c43c4fb1b4f20721c00a2cfe7d7e957c1c42008af71e175517cbdc7d0ec7c8f` |
| `oddAbsoluteExcess_le` | `504f0772f7ade620ff8da2ea3db5cabb34bfeb8613344a288f2a835fb9763dd5` |
| `two_local_mass` | `2823455ad962a414df563f59a3bc4e3859d8492de400d1fbbb598f43dd6e7e90` |
| `candidate_constant_transfer` | `10d37c81ebd4b719196d4677de87ebdf28cdbf787b852a05a87a6a4c1cbb71b9` |

All listed theorems are kernel-checked with
`[propext, Classical.choice, Quot.sound]`; none uses `sorryAx`,
native-decision, or `Lean.trustCompiler`.

## Separate assessments

- **Formal correctness:** verified only for the displayed rational identities,
  local mass values, the bound `E_p≤8/p²`, and the conditional final constant
  arithmetic.  Connection to the concrete global kernel and infinite products
  remains unformalized.
- **Novelty:** no novelty claim.  These are elementary local calculations;
  their value is to isolate the exact interface required by the larger proof.
- **Research value:** the calculation exposes the special `p=2` factor and
  supplies a concrete summable majorant, replacing an unspecified
  “absolute-convergence step” with explicit remaining obligations.

