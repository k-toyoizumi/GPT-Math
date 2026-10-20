import Mathlib

/-!
Generic completeness of the arithmetic-progression enumeration for Type II
divisor witnesses. This lemma is elementary and not a new mathematical result.
It ensures that a bounded progression enumerates all positive divisors
s of N with m ∣ (s+1), provided m>0 and N>0.
-/

namespace TypeIIProgression

theorem divisor_witness_progression
    (N m s : ℕ) (hm : 0 < m) (hN : 0 < N) (hs : 0 < s)
    (hdiv : s ∣ N) (hmod : (s + 1) % m = 0) :
    ∃ t : ℕ, 0 < t ∧ t ≤ (N + 1) / m ∧ s = m * t - 1 := by
  obtain ⟨t, ht⟩ := Nat.dvd_of_mod_eq_zero hmod
  have hle : s ≤ N := Nat.le_of_dvd hN hdiv
  have htpos : 0 < t := by
    by_contra h
    have hzero : t = 0 := by omega
    simp [hzero] at ht
  have hbound : t ≤ (N + 1) / m := by
    apply (Nat.le_div_iff_mul_le hm).2
    calc
      t * m = s + 1 := by simpa [Nat.mul_comm] using ht.symm
      _ ≤ N + 1 := by omega
  refine ⟨t, htpos, hbound, ?_⟩
  omega

theorem progression_witness_divisibility
    (m s t : ℕ) (hm : 0 < m) (ht : 0 < t)
    (heq : s = m * t - 1) :
    (s + 1) % m = 0 := by
  have hmul : 0 < m * t := Nat.mul_pos hm ht
  have hsplus : s + 1 = m * t := by omega
  rw [hsplus]
  simp

end TypeIIProgression
