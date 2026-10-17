#!/usr/bin/env python3
"""Exact, standard-library audit of a fixed-first-denominator subfamily.

For prime p = 24k+1, set a=(p+3)//4. Check the restricted question:
does 4/p = 1/a + 1/y + 1/z have positive integer y,z?

This does NOT search all first denominators, nor prove the conjecture.
"""
from fractions import Fraction
from math import isqrt

LIMIT = 100_000

def primes_below(n):
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for q in range(2, isqrt(n - 1) + 1):
        if sieve[q]:
            sieve[q*q:n:q] = b"\x00" * (((n-1-q*q)//q)+1)
    return (q for q in range(n) if sieve[q])

def factors(n):
    result = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            result[d] = result.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result

def divisors_of_square(n):
    ds = [1]
    for q, exp in factors(n).items():
        ds = [d*q**j for d in ds for j in range(2*exp+1)]
    return ds

def run(limit=LIMIT):
    count = good = 0
    for p in primes_below(limit):
        if p % 24 != 1:
            continue
        count += 1
        a = (p + 3) // 4
        assert p == 4*a - 3 and a % 3 == 1
        bad_mod3_factor = [q for q in factors(a) if q % 3 == 2]
        expected = bool(bad_mod3_factor)
        A = p*a
        ds = divisors_of_square(A)
        # Full divisor-pair criterion; both congruences are tested.
        possible = any(d % 3 == 2 and (A*A//d) % 3 == 2 for d in ds)
        assert possible == expected, (p, a)
        if expected:
            good += 1
            d = bad_mod3_factor[0]
            e = A*A//d
            assert d*e == A*A and d % 3 == e % 3 == 2
            y, z = (A+d)//3, (A+e)//3
            assert y > 0 and z > 0
            assert Fraction(4, p) == Fraction(1, a) + Fraction(1, y) + Fraction(1, z)
    print(f"prime p < {limit}, p % 24 == 1: {count}")
    print(f"fixed a=(p+3)/4 solvable: {good}")
    print(f"fixed a not solvable: {count-good}")
    print("All exact rational and divisor-pair checks passed.")

if __name__ == "__main__":
    run()
