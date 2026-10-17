import Mathlib

/-!
Erdos-Straus Type II finite search for p=670849.
UNCOMPILED: no Lean or GitHub Actions success claimed.
A quantified completeness theorem is still pending.
-/

namespace TypeIIDepthSeven

def witnessExists : Bool :=
  (List.range 7).any fun i =>
    (List.range 7).any fun j =>
      let u := i + 1
      let a := j + 1
      (Nat.gcd u a == 1) &&
      (List.range ((a * 670849 + u + 1) / (4 * u * a))).any
        (fun k =>
          let s := (4 * u * a) * (k + 1) - 1
          (a * 670849 + u) % s == 0)

theorem noWitnessInFiniteSearch : witnessExists = false := by
  native_decide

theorem depthEightWitness319 :
    Nat.Coprime 8 1 ∧
    319 ∣ (1 * 670849 + 8) ∧
    (319 + 1) % (4 * 8 * 1) = 0 := by
  constructor
  · decide
  constructor
  · norm_num
  · norm_num

theorem depthEightWitness7711 :
    Nat.Coprime 8 1 ∧
    7711 ∣ (1 * 670849 + 8) ∧
    (7711 + 1) % (4 * 8 * 1) = 0 := by
  constructor
  · decide
  constructor
  · norm_num
  · norm_num

theorem depthEightIdentity319 :
    (4 : ℚ) / 670849 =
      1 / 168240 + 1 / 53667920 + 1 / 14107954470 := by
  norm_num

theorem depthEightIdentity7711 :
    (4 : ℚ) / 670849 =
      1 / 167736 + 1 / 1293396872 + 1 / 14065690983 := by
  norm_num

#print axioms TypeIIDepthSeven.noWitnessInFiniteSearch
#print axioms TypeIIDepthSeven.depthEightWitness7711

end TypeIIDepthSeven
