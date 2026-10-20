# T12-C: local factor and finite-convolution scope for \(W(J)\)

Date: 2026-10-20 (Asia/Tokyo)  
Input source SHA: `3802f98cb272791ba6c0dc8d1a9cc21b7648804f`  
Task status: paper derivation only; no Lean theorem or asymptotic has been verified.

## Recovery and provenance boundary

The previously reported files `GPT-Math_T12A_publication_blocked.zip` and
`GPT-Math_T12B_Dahan_primary_source_20261020.zip` were not found in the available
persistent file store. The branch `research/t12-w-formalization-20261020` is
identical to `main` at the input SHA, with no T12 note commit. The original
write-rejection text, rejected tool call, target path, and unsaved note bytes
remain unavailable. This note is a new independent reconstruction of one narrow
subproblem; it is not the recovered T12-A or T12-B text.

## Primary-source comparison

Dahan's arXiv v1 (submitted 2026-08-25), Lemma 4.22, defines

\[
W(J)=\sum_{\substack{u,a\le J\\(u,a)=1}}\frac1{\varphi(4ua)}
\]

and proves only the lower bound

\[
W(J)\ge \left(\frac{3}{2\pi^2}+o(1)\right)(\log J)^2.
\]

The paper reports numerical extrapolation near `0.46` and explicitly says that
a sharper lower bound remains to be proved. Therefore the candidate equality

\[
W(J)=\frac{9}{2\pi^2}(\log J)^2+O(\log J)
\]

is not established by Lemma 4.22. Primary source:
<https://arxiv.org/abs/2608.24035> (PDF pp. 26--27, Lemma 4.22 and following
discussion; pp. 38--39, item (8)/open problem).

## Independent local-factor calculation

Let

\[
A(u,a)=\mathbf 1_{(u,a)=1}/\varphi(4ua).
\]

Formally factor the two-variable Dirichlet series of \(A\) as
\(\zeta(1+s)\zeta(1+t)H(s,t)\). At \((s,t)=(0,0)\), an odd prime may occur in
at most one of \(u,a\), hence its unnormalised local factor is

\[
1+2\sum_{k\ge1}\frac1{\varphi(p^k)}
=1+\frac{2p}{(p-1)^2}.
\]

Removing the two zeta factors gives

\[
(1-p^{-1})^2\left(1+\frac{2p}{(p-1)^2}\right)=1+p^{-2}.
\]

At \(p=2\), the cases are: both variables odd, contributing \(1/2\), or one
variable has exact exponent \(k\ge1\), contributing \(2^{-(k+1)}\). Thus the
unnormalised local factor is

\[
\frac12+2\sum_{k\ge1}2^{-(k+1)}=\frac32,
\]

and after removing the two zeta factors it is \(3/8\). Consequently the formal
residue is

\[
H(0,0)=\frac38\prod_{p>2}(1+p^{-2})
=\frac38\frac{\zeta(2)/\zeta(4)}{1+2^{-2}}
=\frac{9}{2\pi^2}.
\]

This calculation identifies the candidate coefficient and agrees numerically
with Dahan's extrapolation, but it is not by itself an asymptotic proof.

## Exact finite identity proposed as the first Lean target

Let \(b(m,n)=1/(mn)\), whose two-variable Dirichlet series is
\(\zeta(1+s)\zeta(1+t)\), and define the finite divisor kernel

\[
h(r,s)=\sum_{d\mid r}\sum_{e\mid s}
\frac{\mu(d)\mu(e)}{de}\,A(r/d,s/e).
\]

Two applications of finite Möbius inversion give the exact identity

\[
A(u,a)=\sum_{r\mid u}\sum_{s\mid a}
\frac{h(r,s)}{(u/r)(a/s)}.
\]

Summing this identity over the finite square yields

\[
W(J)=\sum_{r,s\le J}h(r,s)
H_{\lfloor J/r\rfloor}H_{\lfloor J/s\rfloor},
\]

where \(H_n=\sum_{m\le n}1/m\). Both statements are finite algebraic
identities. They are the recommended minimal Lean target before any analytic
claim. A suitable theorem should use exact rationals/reals, positive naturals,
`Nat.divisors`, `Nat.Moebius`, and explicit nonzero/positivity side conditions.

## Analytic gap after the finite Lean target

To upgrade the formal residue calculation to
\(W(J)=H(0,0)(\log J)^2+O(\log J)\), a paper proof still has to establish:

1. absolute summability of the two-variable kernel \(h\);
2. sufficient logarithmic moments of \(|h(r,s)|\);
3. uniform control of the tails introduced by \(r,s\le J\);
4. justified passage from local factors to the Euler product and its value;
5. expansion of the two harmonic factors with an aggregate \(O(\log J)\)
   remainder.

A convenient sufficient package would be a weighted bound strong enough to
sum \(|h(r,s)|(1+\log r)(1+\log s)\), plus a quantitative tail estimate. It has
not been proved here and may require a more careful region of absolute
convergence than the value of the Euler product at the origin alone suggests.

## Verification and novelty labels

- Finite convolution identity: paper-derived candidate; Lean not written or run.
- Local factors and coefficient: independently algebraically checked; not a
  Lean-verified theorem and not a proof of the asymptotic.
- General asymptotic: unproved.
- Novelty: unresolved. Dahan records the numerical constant and the need for a
  sharper proof; the exact coefficient and error term require a broader
  prior-art search before any novelty claim.
- Downstream sieve improvement: not transferred in this work unit; it is a
  separate conditional calculation.

## Next minimal operation

Formalise and run only the finite two-variable Möbius-inversion identity in the
pinned Lean/Mathlib environment. Do not label the asymptotic verified. After a
new source commit, require a same-SHA successful GitHub Actions run and inspect
its proof evidence before changing the verification label.
