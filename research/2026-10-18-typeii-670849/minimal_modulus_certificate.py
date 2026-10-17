#!/usr/bin/env python3
"""Independent exact finite certificate for p=670849, 1<=u,a<=7.

Only standard-library integer arithmetic. A proper divisor q of m=4*u*a
may already exclude the target residue -1 modulo m. This does NOT establish
a uniform bound, a new general theorem, or a counterexample to Erdős–Straus.
"""
from math import gcd, isqrt, prod

P = 670849

def divisors(n):
    assert n > 0
    ds = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            ds.update((d, n // d))
    return sorted(ds)

def factors(n):
    fs = []
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            fs.append((d, e))
    if n > 1:
        fs.append((n, 1))
    return fs

def factor_residues(fs, q):
    rs = {1 % q}
    for prime, exponent in fs:
        rs = {(r * pow(prime, k, q)) % q
              for r in rs for k in range(exponent + 1)}
    return rs

def main():
    rows = []
    for u in range(1, 8):
        for a in range(1, 8):
            if gcd(u, a) != 1:
                continue
            N, m = a * P + u, 4 * u * a
            ds, fs = divisors(N), factors(N)
            assert prod(p ** e for p, e in fs) == N
            assert len(ds) == prod(e + 1 for _, e in fs)
            blockers = []
            for q in divisors(m):
                if q <= 1:
                    continue
                rs = factor_residues(fs, q)
                assert rs == {d % q for d in ds}
                if q - 1 not in rs:
                    blockers.append((q, rs))
            assert blockers, (u, a)
            q, rs = min(blockers, key=lambda item: item[0])
            assert m % q == 0
            assert all(d % m != m - 1 for d in ds)
            rows.append((u, a, N, m, q, len(ds), len(rs)))
    assert len(rows) == 35
    assert sum(row[5] for row in rows) == 426
    assert sum(row[4] < row[3] for row in rows) == 25
    print("u a N m minimal_q divisors residue_count")
    for row in rows:
        print(*row)
    print("PASS: 35 coprime pairs; 426 divisors; 25 proper-modulus blockers.")

if __name__ == "__main__":
    main()
