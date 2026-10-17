import Mathlib

/-! Checks a numerical discrepancy in a displayed example attributed to
Xu, arXiv:2609.29250. This is NOT a proof that the underlying theorem is false.
Compare the transcription against the paper before citing this result. -/

namespace XuAudit

private def lhs : ℚ := (1 : ℚ) / 540 + 1 / 51288 + 1 / 1521544
private def rhs : ℚ := (4 : ℚ) / 2137

theorem displayed_residual : lhs - rhs = (23 : ℚ) / 102704220 := by
  norm_num [lhs, rhs]

theorem displayed_identity_false : lhs ≠ rhs := by
  intro h
  have hzero : lhs - rhs = 0 := sub_eq_zero.mpr h
  rw [displayed_residual] at hzero
  norm_num at hzero

private def correctedLhs : ℚ :=
  (1 : ℚ) / 534 + 1 / 50712 + 1 / 1504456
private def correctedRhs : ℚ := (4 : ℚ) / 2113

theorem corrected_example : correctedLhs = correctedRhs := by
  norm_num [correctedLhs, correctedRhs]

end XuAudit
