#!/usr/bin/env python3
"""Exact finite audit. Standard library only. Generates certificate.csv."""
from math import gcd, isqrt
from pathlib import Path
import csv

P = 670849

def factor(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            k = 0
            while n % d == 0:
                n //= d
                k += 1
            out.append((d, k))
        d = 3 if d == 2 else d + 2
    if n > 1:
        out.append((n, 1))
    return out

def divisors_from_factors(f):
    ds = [1]
    for q, e in f:
        old = ds[:]
        power = 1
        for _ in range(e):
            power *= q
            ds.extend(d * power for d in old)
    return sorted(ds)

def divisors_from_sqrt(n):
    ds = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            ds.add(d)
            ds.add(n // d)
    return sorted(ds)

def residues_from_factors(f, m):
    residues = {1 % m}
    for q, e in f:
        powers = [pow(q, i, m) for i in range(e + 1)]
        residues = {(r * t) % m for r in residues for t in powers}
    return residues

def check(limit):
    rows = []
    for u in range(1, limit + 1):
        for a in range(1, limit + 1):
            if gcd(u, a) != 1:
                continue
            n, m = a * P + u, 4 * u * a
            fs = factor(n)
            ds = divisors_from_factors(fs)
            assert ds == divisors_from_sqrt(n)
            rs = residues_from_factors(fs, m)
            assert rs == {d % m for d in ds}
            hits = [d for d in ds if d % m == m - 1]
            progression = [m * t - 1 for t in range(1, (n + 1) // m + 1)
                           if n % (m * t - 1) == 0]
            assert hits == progression
            rows.append(dict(u=u, a=a, N=n, m=m,
                             factors="*".join(f"{q}^{e}" for q, e in fs),
                             divisor_count=len(ds), residue_count=len(rs),
                             residues=" ".join(map(str, sorted(rs))),
                             witnesses=" ".join(map(str, hits))))
    return rows

def denominators(u, a, s):
    n = a * P + u
    assert n % s == 0 and (s + 1) % (4 * u * a) == 0
    alpha, v = (s + 1) // (4 * u * a), n // s
    x, y, z = alpha * u * v, P * alpha * u * a, P * alpha * v * a
    assert 4 * x * y * z == P * (x * y + x * z + y * z)
    return x, y, z

def main():
    rows7 = check(7)
    assert len(rows7) == 35
    assert sum(r["divisor_count"] for r in rows7) == 426
    assert all(not r["witnesses"] for r in rows7)
    rows8 = check(8)
    hits = [(r["u"], r["a"], r["witnesses"]) for r in rows8 if r["witnesses"]]
    assert hits == [(8, 1, "319 7711")], hits
    assert denominators(8, 1, 319) == (168240, 53667920, 14107954470)
    assert denominators(8, 1, 7711) == (167736, 1293396872, 14065690983)
    print("35 pairs; 426 divisors; no J<=7 witnesses; J=8:", hits)
    print("naive candidates:", sum(r["N"] for r in rows7))
    print("progression candidates:", sum((r["N"] + 1) // r["m"] for r in rows7))
    out = Path(__file__).with_name("certificate.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows7[0].keys())
        writer.writeheader()
        writer.writerows(rows7)
    print("Wrote", out)

if __name__ == "__main__":
    main()
