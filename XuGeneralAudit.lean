import Mathlib

/-!
General rational-function audit of Xu, arXiv:2609.29250v1, Eq. (4.32).
This checks an algebraic identity for nonnegative rational parameters.
It does NOT prove the entire Erdős–Straus conjecture or any novelty claim.
-/

namespace XuGeneralAudit

def expression (m r c : ℚ) : ℚ :=
  (1 : ℚ) / (6 * (m + 1)) +
  1 / (12 * (3 * r + 2) * (c + 1) * (24 * m + 1)) +
  1 / (4 * (3 * r + 2) * (c + 1) * (138 * r + 89) * (24 * m + 1))

theorem general_residual (m r c : ℚ)
    (hm : 0 ≤ m) (hr : 0 ≤ r) (hc : 0 ≤ c) :
    expression m r c - 4 / (24 * m + 1) =
      23 * (m + 1 - (c + 1) * (138 * r + 89)) /
        (6 * (c + 1) * (138 * r + 89) * (m + 1) * (24 * m + 1)) := by
  have hM : m + 1 ≠ 0 := by positivity
  have hB : 3 * r + 2 ≠ 0 := by positivity
  have hT : c + 1 ≠ 0 := by positivity
  have hQ : 138 * r + 89 ≠ 0 := by positivity
  have hN : 24 * m + 1 ≠ 0 := by positivity
  unfold expression
  field_simp [hM, hB, hT, hQ, hN]
  ring

theorem equality_iff_corrected (m r c : ℚ)
    (hm : 0 ≤ m) (hr : 0 ≤ r) (hc : 0 ≤ c) :
    (expression m r c = 4 / (24 * m + 1)) ↔
      m + 1 = (c + 1) * (138 * r + 89) := by
  have hden :
      6 * (c + 1) * (138 * r + 89) * (m + 1) * (24 * m + 1) ≠ (0 : ℚ) := by
    positivity
  rw [← sub_eq_zero, general_residual m r c hm hr hc]
  simp [hden, sub_eq_zero]

#print axioms XuGeneralAudit.general_residual
#print axioms XuGeneralAudit.equality_iff_corrected

end XuGeneralAudit
