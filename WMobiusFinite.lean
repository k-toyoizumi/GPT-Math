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
abbrev BiAF := ArithmeticFunction AF

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

/-- Remove the weighted zeta factor in the second coordinate as well. -/
def innerKernel (A : BiAF) (r : ℕ) : AF :=
  kernel (outerKernel A r)

theorem outer_reconstruct (A : BiAF) :
    (weightedZeta • outerKernel A : BiAF) = A := by
  simp [outerKernel, ← mul_smul]

theorem inner_reconstruct (A : BiAF) (r : ℕ) :
    weightedZeta * innerKernel A r = outerKernel A r :=
  reconstruct (outerKernel A r)

/--
Exact finite two-variable weighted Möbius inversion, written on divisor
antidiagonals.  In each pair `x`, `x.1 * x.2` is the ambient index:
`x.1` is the harmonic quotient and `x.2` is the kernel index.
-/
theorem finite_double_reconstruct (A : BiAF) (u a : ℕ) :
    A u a =
      ∑ x ∈ u.divisorsAntidiagonal,
        ∑ y ∈ a.divisorsAntidiagonal,
          weightedZeta x.1 * weightedZeta y.1 * innerKernel A x.2 y.2 := by
  rw [← outer_reconstruct A]
  simp only [ArithmeticFunction.smul_apply]
  simp_rw [inner_reconstruct A]
  simp only [ArithmeticFunction.mul_apply]
  simp [Finset.mul_sum, mul_assoc]

#print axioms WMobiusFinite.divideByN_mul
#print axioms WMobiusFinite.weightedZeta_mul_weightedMoebius
#print axioms WMobiusFinite.finite_double_reconstruct

end WMobiusFinite
