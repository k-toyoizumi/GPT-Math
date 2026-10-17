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
      (Nat.divisors (a * 670849 + u)).toList.any
        (fun s => (s + 1) % (4 * u * a) == 0)

theorem noWitnessInFiniteSearch : witnessExists = false := by
  native_decide

end TypeIIDepthSeven
