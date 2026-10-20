# T12-E — Concrete `W` weight specialization and analytic boundary

## Scope

This unit specializes the already verified generic finite two-variable weighted
Möbius inversion to

\[
A(u,a)=\mathbf 1_{u,a\ge 1}\mathbf 1_{(u,a)=1}\,\varphi(4ua)^{-1}.
\]

The Lean source calls this zero-extended rational-valued function `wWeight`.
The extension by zero is only an encoding device for `ArithmeticFunction`; on
positive coprime inputs it is definitionally the summand of `W(J)`.

## Formal result in this unit

`WMobiusFinite.finite_wWeight_reconstruct` is intended to prove the exact
finite identity

\[
A(u,a)=\sum_{qr=u}\sum_{st=a}\frac1q\frac1s K(r,t),
\qquad K(r,t)=\operatorname{innerKernel}(A)(r,t),
\]

for `a ≠ 0`, with both sums represented by divisor antidiagonals.  This is a
specialization of `finite_double_reconstruct`, not a convergence result.

Verification status: **verified for this finite identity only**.  The exact
branch head `043ad653531721add32a148c648ff552c34179bc` was checked by Actions
run `39463131474`, attempt 1.  Both jobs completed successfully.  This label
does not extend to any infinite sum or asymptotic statement.

## Verification evidence

- PR: <https://github.com/k-toyoizumi/GPT-Math/pull/3>
- source commit: `043ad653531721add32a148c648ff552c34179bc`
- tested pull-request merge SHA: `8e3dfb9b9e97281be97f1b60d3fb3b25ad9c3443`
- run: <https://github.com/k-toyoizumi/GPT-Math/actions/runs/39463131474>
- attempt: 1
- jobs: `lean` (`118767405165`) and `failure-evidence`
  (`118767405785`), both successful
- verification artifact: `12282979286`,
  `sha256:f10d0a6848d5a68bf8bcc0facebc4f90a00e89c749a5ab1f29e96f795530e6b3`
- negative-control artifact: `12282739383`,
  `sha256:6747864323008b43620e791c181a20f97ee76e4dacb6a4b9d49b2fb1c046c5e4`
- `WMobiusFinite.lean` blob: `d10b3862c5d480f9afc8c5102c313ece5ad1b630`
- source SHA-256:
  `72cbcbd8440a2e4d21c47f415388d97256de4e32fe06402916d7cd8b83b96b19`
- `finite_wWeight_reconstruct` statement hash:
  `31e5d1b0544c78b207efb3d956f748b3d713c98b7a05b577bfe181731897c044`
- trust: kernel-checked; axioms `[propext, Classical.choice, Quot.sound]`;
  no `sorryAx`, native-decide, or compiler-trust dependency for this theorem
- CI semantic result hash:
  `06be94f54acbea09c7bf5e6601142975e15b73585bb00e9c1fb5f345d26a6af5`

## Exact analytic reduction after summing the finite identity

For positive `u,a ≤ J`, summing and changing the order of finite sums gives

\[
W(J)=\sum_{r,t\le J}K(r,t)
H_{\lfloor J/r\rfloor}H_{\lfloor J/t\rfloor},
\]

where `H_n=\sum_{m\le n}1/m`.  The change of order here is finite; it does not
justify replacing the truncated kernel sum by an infinite Euler product.

## Analytic obligations still open

The following are proof obligations, not results of this unit:

1. **Absolute summability:** prove an adequate bound for
   `Σ_{r,t≥1} |K(r,t)|`.
2. **Logarithmic moments:** control at least
   `Σ |K(r,t)|(log(2r)+log(2t))`; stronger moments may be needed for the
   claimed remainder.
3. **Tail transfer:** obtain a quantitative estimate strong enough that
   truncating at `r,t≤J` changes the `log² J` main term by `O(log J)`.  Bare
   convergence is insufficient; a sufficient target is
   `Σ_{max(r,t)>J}|K(r,t)| = O(1/log J)`.
4. **Harmonic-error aggregation:** bound the total error from
   `H_floor(J/r)=log(J/r)+γ+O(r/J)` after weighting by `K`.  This may require a
   separate weighted tail or arithmetic-moment estimate; it is not implied
   automatically by absolute summability.
5. **Euler product:** prove multiplicativity/local factorization, absolute
   convergence at the evaluation point, and
   `Σ K(r,t)=9/(2π²)`.  The constant is still a candidate until this transfer
   is proved, including the special local factor at `p=2` caused by `4ua`.

Only after these obligations are discharged can the finite identity support
`W(J)=9/(2π²)(log J)²+O(log J)`.

## Separation of assessments

- **Formal correctness:** verified for the zero extension, its positive
  coprime reduction, and the exact finite reconstruction at the evidence above.
- **Novelty:** not assessed by this Lean specialization.  Comparison with
  Dahan and related literature remains a separate bibliography task.
- **Research value:** it fixes the exact algebraic/analytic interface and
  prevents finite computation or finite inversion from being mistaken for the
  asymptotic proof.

