import Mathlib

/-!
Finite, executable audit for p = 670849 and 1 ≤ u,a ≤ 7.
The predicate searches every positive divisor of a*p+u, for each coprime
positive pair. The theorem certifies the executable search result only.
It does not assert the global Erdős–Straus conjecture.
-/

namespace TypeIIDepthSeven

def witnessExists : Bool :=
  (List.range 7).any fun i =>
    (List.range 7).any fun j =>
      let u := i + 1
      let a := j + 1
      (Nat.gcd u a == 1) &&
      (List.range (a * 670849 + u)).any
        (fun k =>
          let s := k + 1
          (a * 670849 + u) % s == 0 &&
          (s + 1) % (4 * u * a) == 0)

theorem noWitnessInFiniteSearch : witnessExists = false := by
  native_decide

/-! A matching positive witness appears at depth 8: u=8, a=1, s=319. -/

theorem depthEightWitness :
    Nat.Coprime 8 1 ∧
    319 ∣ (1 * 670849 + 8) ∧
    (319 + 1) % (4 * 8 * 1) = 0 := by
  constructor
  · decide
  constructor
  · norm_num
  · norm_num

theorem depthEightUnitFractionIdentity :
    (4 : ℚ) / 670849 =
      1 / 168240 + 1 / 53667920 + 1 / 14107954470 := by
  norm_num


end TypeIIDepthSeven
