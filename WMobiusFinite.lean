import Mathlib

/-!
Finite weighted Möbius inversion for the two-variable kernel underlying
`W(J)`.  This file proves only finite algebraic identities.  It does not prove
absolute summability, an Euler-product limit, or the asymptotic formula for
`W(J)`.
-/

namespace WMobiusFinite

open ArithmeticFunction
open scoped ArithmeticFunction

abbrev AF := ArithmeticFunction ℚ
abbrev BiAF := ArithmeticFunction (ℕ → ℚ)

/-- Divide the value of an arithmetic function at `n` by `n`.
At zero this is zero, as required by `ArithmeticFunction`. -/
def divideByN (f : AF) : AF :=
  ⟨fun n => f n / (n : ℚ), by simp⟩

@[simp]
theorem divideByN_apply (f : AF) (n : ℕ) :
    divideByN f n = f n / (n : ℚ) :=
  rfl

/-- Dividing coefficients by their index respects Dirichlet convolution. -/
theorem divideByN_mul (f g : AF) :
    divideByN (f * g) = divideByN f * divideByN g := by
  ext n
  by_cases hn : n = 0
  · simp [hn]
  simp only [divideByN_apply]
  rw [ArithmeticFunction.mul_apply, ArithmeticFunction.mul_apply, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro x hx
  have hmul : x.1 * x.2 = n :=
    (Nat.mem_divisorsAntidiagonal.mp hx).1
  have hprod : x.1 * x.2 ≠ 0 := by
    simpa [hmul] using hn
  have hx1 : (x.1 : ℚ) ≠ 0 := by
    exact_mod_cast left_ne_zero_of_mul hprod
  have hx2 : (x.2 : ℚ) ≠ 0 := by
    exact_mod_cast right_ne_zero_of_mul hprod
  have hcast : (x.1 : ℚ) * (x.2 : ℚ) = (n : ℚ) := by
    exact_mod_cast hmul
  simp only [divideByN_apply]
  rw [← hcast]
  field_simp

@[simp]
theorem divideByN_one : divideByN (1 : AF) = 1 := by
  ext n
  by_cases hn : n = 1
  · simp [hn]
  · simp [divideByN, ArithmeticFunction.one_apply, hn]

/-- The harmonic Dirichlet kernel `n ↦ 1/n` on positive naturals. -/
def weightedZeta : AF :=
  divideByN (ζ : AF)

/-- The inverse kernel `n ↦ μ(n)/n` on positive naturals. -/
def weightedMoebius : AF :=
  divideByN (ArithmeticFunction.moebius : AF)

@[simp]
theorem weightedZeta_mul_weightedMoebius :
    weightedZeta * weightedMoebius = 1 := by
  rw [weightedZeta, weightedMoebius, ← divideByN_mul]
  simp

@[simp]
theorem weightedMoebius_mul_weightedZeta :
    weightedMoebius * weightedZeta = 1 := by
  rw [mul_comm, weightedZeta_mul_weightedMoebius]

/-- One-dimensional finite weighted Möbius kernel. -/
def kernel (f : AF) : AF :=
  weightedMoebius * f

theorem reconstruct (f : AF) :
    weightedZeta * kernel f = f := by
  simp [kernel, ← mul_assoc]

/-- Remove the weighted zeta factor in the first coordinate. -/
def outerKernel (A : BiAF) : BiAF :=
  (weightedMoebius • A : BiAF)

theorem outer_reconstruct (A : BiAF) :
    (weightedZeta • outerKernel A : BiAF) = A := by
  rw [outerKernel, ← ArithmeticFunction.mul_smul']
  simp

/-- The second-coordinate slice, with the irrelevant zero index normalized. -/
def innerSource (A : BiAF) (r : ℕ) : AF :=
  ⟨fun a => if a = 0 then 0 else outerKernel A r a, by simp⟩

/-- Remove the weighted zeta factor in the second coordinate as well. -/
def innerKernel (A : BiAF) (r : ℕ) : AF :=
  kernel (innerSource A r)

theorem inner_reconstruct (A : BiAF) (r a : ℕ) (ha : a ≠ 0) :
    (weightedZeta * innerKernel A r) a = outerKernel A r a := by
  have h := congrArg (fun f : AF => f a) (reconstruct (innerSource A r))
  simpa [innerKernel, innerSource, ha] using h

/--
Exact finite two-variable weighted Möbius inversion, written on divisor
antidiagonals.  In each pair `x`, `x.1 * x.2` is the ambient index:
`x.1` is the harmonic quotient and `x.2` is the kernel index.
-/
theorem finite_double_reconstruct (A : BiAF) (u a : ℕ) (ha : a ≠ 0) :
    A u a =
      ∑ x ∈ u.divisorsAntidiagonal,
        ∑ y ∈ a.divisorsAntidiagonal,
          weightedZeta x.1 * weightedZeta y.1 * innerKernel A x.2 y.2 := by
  calc
    A u a = (weightedZeta • outerKernel A : BiAF) u a := by
      exact congrArg (fun B : BiAF => B u a) (outer_reconstruct A).symm
    _ = ∑ x ∈ u.divisorsAntidiagonal,
          weightedZeta x.1 * outerKernel A x.2 a := by
      simp only [ArithmeticFunction.smul_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
    _ = ∑ x ∈ u.divisorsAntidiagonal,
          ∑ y ∈ a.divisorsAntidiagonal,
            weightedZeta x.1 * weightedZeta y.1 * innerKernel A x.2 y.2 := by
      apply Finset.sum_congr rfl
      intro x hx
      rw [← inner_reconstruct A x.2 a ha, ArithmeticFunction.mul_apply]
      simp [Finset.mul_sum, mul_assoc]

/-- The concrete summand used in `W(J)`, extended by zero to the axes and to
non-coprime pairs so that it is an `ArithmeticFunction` in the first variable. -/
def wWeight (u a : ℕ) : ℚ :=
  if u = 0 ∨ a = 0 ∨ ¬ Nat.Coprime u a then 0
  else 1 / (Nat.totient (4 * u * a) : ℚ)

/-- `wWeight` packaged for the two-variable finite inversion theorem. -/
def wArithmetic : BiAF :=
  ⟨fun u a => wWeight u a, by
    funext a
    simp [wWeight]⟩

/--
The residual kernel is exactly the finite double weighted-Möbius transform
of the original two-variable arithmetic function.  The nonzero hypothesis is
only needed to unfold the normalized second-coordinate slice.

This is a finite identity: it does not assert multiplicativity, identify any
prime-power coefficient, or pass to an Euler product.
-/
theorem innerKernel_explicit (A : BiAF) (r t : ℕ) (ht : t ≠ 0) :
    innerKernel A r t =
      ∑ y ∈ t.divisorsAntidiagonal,
        ∑ x ∈ r.divisorsAntidiagonal,
          weightedMoebius y.1 * weightedMoebius x.1 * A x.2 y.2 := by
  rw [innerKernel, kernel, ArithmeticFunction.mul_apply]
  apply Finset.sum_congr rfl
  intro y hy
  have hyprod : y.1 * y.2 = t :=
    (Nat.mem_divisorsAntidiagonal.mp hy).1
  have hyprod_ne : y.1 * y.2 ≠ 0 := by
    simpa [hyprod] using ht
  have hy2 : y.2 ≠ 0 := right_ne_zero_of_mul hyprod_ne
  simp only [innerSource, hy2, if_false, outerKernel,
    ArithmeticFunction.smul_apply, Finset.sum_apply, Pi.smul_apply,
    smul_eq_mul]
  simp [Finset.mul_sum, mul_assoc]

/-- The explicit finite double transform specialized to the summand of `W(J)`. -/
theorem innerKernel_wArithmetic_explicit (r t : ℕ) (ht : t ≠ 0) :
    innerKernel wArithmetic r t =
      ∑ y ∈ t.divisorsAntidiagonal,
        ∑ x ∈ r.divisorsAntidiagonal,
          weightedMoebius y.1 * weightedMoebius x.1 * wWeight x.2 y.2 := by
  simpa [wArithmetic] using innerKernel_explicit wArithmetic r t ht

@[simp]
theorem wWeight_of_ne_zero_coprime (u a : ℕ) (hu : u ≠ 0) (ha : a ≠ 0)
    (hcop : Nat.Coprime u a) :
    wWeight u a = 1 / (Nat.totient (4 * u * a) : ℚ) := by
  simp [wWeight, hu, ha, hcop]

/--
Concrete finite weighted Möbius reconstruction of the summand of `W(J)`.
This is still only an exact finite identity; it supplies no convergence,
tail estimate, Euler-product evaluation, or asymptotic statement.
-/
theorem finite_wWeight_reconstruct (u a : ℕ) (ha : a ≠ 0) :
    wWeight u a =
      ∑ x ∈ u.divisorsAntidiagonal,
        ∑ y ∈ a.divisorsAntidiagonal,
          weightedZeta x.1 * weightedZeta y.1 *
            innerKernel wArithmetic x.2 y.2 := by
  simpa [wArithmetic] using finite_double_reconstruct wArithmetic u a ha

/-!
The following rational identities are the local algebra needed for the
residual kernel.  For an odd prime represented by a rational variable `p`,
the normalized local weight has axis value `1 / (p - 1)`.  Applying the
weighted Möbius difference gives the axis and diagonal coefficients below.
The hypotheses exclude only the vanishing denominators; primality and the
passage to an infinite Euler product are deliberately outside these lemmas.
-/

/-- Residual-kernel coefficient at exponent pair `(1,0)` or `(0,1)`. -/
def oddAxisCoeff (p : ℚ) : ℚ :=
  1 / (p * (p - 1))

/-- Residual-kernel coefficient at exponent pair `(1,1)`. -/
def oddDiagonalCoeff (p : ℚ) : ℚ :=
  -(p + 1) / (p ^ 2 * (p - 1))

theorem odd_axis_from_weighted_moebius (p : ℚ) (hp0 : p ≠ 0) (hp1 : p ≠ 1) :
    1 / (p - 1) - 1 / p = oddAxisCoeff p := by
  unfold oddAxisCoeff
  field_simp [hp0, sub_ne_zero.mpr hp1]
  <;> ring

theorem odd_diagonal_from_weighted_moebius
    (p : ℚ) (hp0 : p ≠ 0) (hp1 : p ≠ 1) :
    -(1 / p) * (1 / (p - 1)) - (1 / p) * (1 / (p - 1)) +
        (1 / p) ^ 2 =
      oddDiagonalCoeff p := by
  unfold oddDiagonalCoeff
  field_simp [hp0, sub_ne_zero.mpr hp1]
  <;> ring

/-- The signed odd-prime local mass is `1 + p⁻²`. -/
theorem odd_local_mass (p : ℚ) (hp0 : p ≠ 0) (hp1 : p ≠ 1) :
    1 + 2 * oddAxisCoeff p + oddDiagonalCoeff p = 1 + 1 / p ^ 2 := by
  unfold oddAxisCoeff oddDiagonalCoeff
  field_simp [hp0, sub_ne_zero.mpr hp1]
  <;> ring

/-- Excess of the absolute local mass over one at an odd prime. -/
def oddAbsoluteExcess (p : ℚ) : ℚ :=
  2 / (p * (p - 1)) + (p + 1) / (p ^ 2 * (p - 1))

theorem oddAbsoluteExcess_eq (p : ℚ) (hp0 : p ≠ 0) (hp1 : p ≠ 1) :
    oddAbsoluteExcess p = (3 * p + 1) / (p ^ 2 * (p - 1)) := by
  unfold oddAbsoluteExcess
  field_simp [hp0, sub_ne_zero.mpr hp1]
  <;> ring

/-- A simple summable comparison target for the odd-prime absolute factors. -/
theorem oddAbsoluteExcess_le (p : ℚ) (hp : 2 ≤ p) :
    oddAbsoluteExcess p ≤ 8 / p ^ 2 := by
  have hp0 : 0 < p := lt_of_lt_of_le (by norm_num) hp
  have hp1 : 0 < p - 1 := sub_pos.mpr (lt_of_lt_of_le (by norm_num) hp)
  rw [oddAbsoluteExcess_eq p (ne_of_gt hp0) (by nlinarith)]
  have hnum : 3 * p + 1 ≤ 8 * (p - 1) := by
    nlinarith
  have hden : 0 < p ^ 2 * (p - 1) :=
    mul_pos (pow_pos hp0 2) hp1
  calc
    (3 * p + 1) / (p ^ 2 * (p - 1))
        ≤ (8 * (p - 1)) / (p ^ 2 * (p - 1)) :=
      (div_le_div_iff_of_pos_right hden).2 hnum
    _ = 8 / p ^ 2 := by
      field_simp [ne_of_gt hp0, ne_of_gt hp1]

/-- At `p = 2`, the normalized axis coefficient vanishes. -/
theorem two_axis_from_weighted_moebius :
    (1 / 2 : ℚ) - 1 / 2 = 0 := by
  norm_num

/-- At `p = 2`, the only nonzero off-origin coefficient is diagonal. -/
theorem two_diagonal_from_weighted_moebius :
    -(1 / 2 : ℚ) * (1 / 2) - (1 / 2) * (1 / 2) + (1 / 2) ^ 2 =
      -(1 / 4) := by
  norm_num

/-- The normalized two-adic signed local mass is `3/4`. -/
theorem two_local_mass :
    (1 : ℚ) - 1 / 4 = 3 / 4 := by
  norm_num

/--
Conditional constant transport: a global normalization `1/2`, the two-adic
factor `3/4`, and an odd-prime product `12/π²` give `9/(2π²)`.
This theorem does not prove that the odd-prime Euler product has that value.
-/
theorem candidate_constant_transfer :
    (1 / 2 : ℝ) * (3 / 4) * (12 / Real.pi ^ 2) =
      9 / (2 * Real.pi ^ 2) := by
  have hpi : Real.pi ^ 2 ≠ 0 := pow_ne_zero 2 Real.pi_ne_zero
  field_simp [hpi]
  <;> ring

#print axioms WMobiusFinite.divideByN_mul
#print axioms WMobiusFinite.weightedZeta_mul_weightedMoebius
#print axioms WMobiusFinite.finite_double_reconstruct
#print axioms WMobiusFinite.finite_wWeight_reconstruct
#print axioms WMobiusFinite.innerKernel_explicit
#print axioms WMobiusFinite.innerKernel_wArithmetic_explicit
#print axioms WMobiusFinite.odd_axis_from_weighted_moebius
#print axioms WMobiusFinite.odd_diagonal_from_weighted_moebius
#print axioms WMobiusFinite.odd_local_mass
#print axioms WMobiusFinite.oddAbsoluteExcess_le
#print axioms WMobiusFinite.two_local_mass
#print axioms WMobiusFinite.candidate_constant_transfer

end WMobiusFinite
