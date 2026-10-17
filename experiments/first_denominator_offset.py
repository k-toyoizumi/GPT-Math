#!/usr/bin/env python3
"""Exact exhaustive offset audit for primes p == 1 (mod 24), p < 100000.

x0 = (p+3)//4. For each p find the least j in [0,15] such that
4/p = 1/(x0+j) + 1/y + 1/z for positive integers y,z.

Factorization and divisor-pair search are complete for EACH fixed x:
B=4*x-p, A=p*x, (B*y-A)*(B*z-A)=A*A.
Both congruences are checked independently.
The bound on j is experimental, NOT a theorem.
"""
from collections import Counter
from fractions import Fraction
from math import isqrt

LIMIT = 100_000
MAX_OFFSET = 15

def primes_below(n):
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for q in range(2, isqrt(n-1)+1):
        if sieve[q]:
            sieve[q*q:n:q] = b"\x00" * (((n-1-q*q)//q)+1)
    return (p for p in range(n) if sieve[p])

def factor(n):
    factors = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            factors[d] = factors.get(d,0)+1
            n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        factors[n] = factors.get(n,0)+1
    return factors

def square_divisors(n):
    divisors = [1]
    for q, exponent in factor(n).items():
        divisors = [d*q**j for d in divisors for j in range(2*exponent+1)]
    return divisors

def first_witness(p,x):
    A=p*x
    B=4*x-p
    assert B>0
    for d in square_divisors(A):
        e=A*A//d
        if d>e:
            continue
        if (A+d)%B or (A+e)%B:
            continue
        y,z=(A+d)//B,(A+e)//B
        assert y>0 and z>0
        assert Fraction(4,p)==Fraction(1,x)+Fraction(1,y)+Fraction(1,z)
        return (x,y,z)
    return None

def main():
    counts=Counter()
    examples={}
    for p in primes_below(LIMIT):
        if p%24 != 1:
            continue
        x0=(p+3)//4
        found=None
        for offset in range(MAX_OFFSET+1):
            witness=first_witness(p,x0+offset)
            if witness is not None:
                found=offset
                examples.setdefault(offset,(p,witness))
                break
        counts[found]+=1
    print("limit",LIMIT,"max_offset",MAX_OFFSET)
    print("total",sum(counts.values()))
    print("offset_counts",sorted((str(k),v) for k,v in counts.items()))
    print("examples",sorted(examples.items()))
    assert sum(counts.values())==1181
    assert counts == Counter({0:575,1:475,2:83,3:11,4:16,5:15,6:1,7:5})

if __name__=="__main__":
    main()
