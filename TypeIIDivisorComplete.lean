import Mathlib

/-!
Finite Type II divisor criterion at p=670849, J<=7.

Unlike a Boolean arithmetic-progression search, this statement quantifies over
the actual Finset of positive divisors of a*p+u. The second theorem converts
divisibility to divisor-set membership using Mathlib's theorem.

Verification status: PENDING CI. Do not cite as Lean-verified without checking
the successful job log for this exact file and commit.
-/

namespace TypeIIDivisorComplete

theorem noWitnessInDivisorSets :
    ∀ u ∈ Finset.Icc 1 7, ∀ a ∈ Finset.Icc 1 7,
      Nat.Coprime u a →
      ∀ s ∈ Nat.divisors (a * 670849 + u),
        (s + 1) % (4 * u * a) ≠ 0 := by
  native_decide

theorem noWitnessForAnyPositiveDivisor
    (u a s : ℕ)
    (hu : 1 ≤ u ∧ u ≤ 7)
    (ha : 1 ≤ a ∧ a ≤ 7)
    (hcop : Nat.Coprime u a)
    (hdiv : s ∣ a * 670849 + u) :
    (s + 1) % (4 * u * a) ≠ 0 := by
  have hn : a * 670849 + u ≠ 0 := by omega
  have hs : s ∈ Nat.divisors (a * 670849 + u) :=
    Nat.mem_divisors.mpr ⟨hdiv, hn⟩
  exact noWitnessInDivisorSets u (Finset.mem_Icc.mpr hu)
    a (Finset.mem_Icc.mpr ha) hcop s hs

#print axioms TypeIIDivisorComplete.noWitnessInDivisorSets
#print axioms TypeIIDivisorComplete.noWitnessForAnyPositiveDivisor

end TypeIIDivisorComplete
