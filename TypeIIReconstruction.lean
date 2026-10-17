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
