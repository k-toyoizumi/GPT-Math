import Mathlib

/-!
# Type II reconstruction for the Erdős–Straus equation

A formally checkable algebraic identity, and one explicit numerical solution.
This does NOT prove that p = 670849 has no Type II witnesses of depth <= 7.
-/

namespace TypeIIReconstruction

theorem cross_multiplication (p a u v alpha : ℕ)
    (h : a * p + u + v = 4 * a * alpha * u * v) :
    4 * (alpha * u * v) * (p * alpha * u * a) * (p * alpha * v * a) =
      p * ((alpha * u * v) * (p * alpha * u * a) +
        (alpha * u * v) * (p * alpha * v * a) +
        (p * alpha * u * a) * (p * alpha * v * a)) := by
  calc
    _ = (4 * a * alpha * u * v) * (p * p * alpha * alpha * u * v * a) := by ring
    _ = (a * p + u + v) * (p * p * alpha * alpha * u * v * a) := by rw [← h]
    _ = _ := by ring

theorem p670849_witness :
    4 * (168240 : ℕ) * 53667920 * 14107954470 =
      670849 * (168240 * 53667920 + 168240 * 14107954470 +
        53667920 * 14107954470) := by
  norm_num

#print axioms TypeIIReconstruction.cross_multiplication
#print axioms TypeIIReconstruction.p670849_witness

end TypeIIReconstruction


/-!
## Exact fixed-first-denominator factorization

This algebraic equivalence is classical; it is a verification bridge, not a
new proof of the Erdős–Straus conjecture.  In particular, it does not
establish the existence of positive divisor factors for arbitrary p.
-/
namespace FixedXFactorization

theorem polynomial_identity (p x y z : ℤ) :
    ((4*x-p)*y-p*x)*((4*x-p)*z-p*x) - (p*x)^2 =
      (4*x-p)*(4*x*y*z - p*(x*y+x*z+y*z)) := by
  ring

theorem equation_iff_factorization (p x y z : ℤ)
    (hshift : 4*x-p ≠ 0) :
    4*x*y*z = p*(x*y+x*z+y*z) ↔
      ((4*x-p)*y-p*x)*((4*x-p)*z-p*x) = (p*x)^2 := by
  have hid := polynomial_identity p x y z
  constructor
  · intro h
    have hr : (4*x-p)*(4*x*y*z-p*(x*y+x*z+y*z)) = 0 := by
      rw [h]
      ring
    exact sub_eq_zero.mp (hid.trans hr)
  · intro h
    have hl : ((4*x-p)*y-p*x)*((4*x-p)*z-p*x) - (p*x)^2 = 0 :=
      sub_eq_zero.mpr h
    have hr : (4*x-p)*(4*x*y*z-p*(x*y+x*z+y*z)) = 0 :=
      hid.symm.trans hl
    have hs : 4*x*y*z-p*(x*y+x*z+y*z) = 0 :=
      (mul_eq_zero.mp hr).resolve_left hshift
    exact sub_eq_zero.mp hs

#print axioms FixedXFactorization.polynomial_identity
#print axioms FixedXFactorization.equation_iff_factorization

end FixedXFactorization
