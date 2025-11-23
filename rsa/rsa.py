import random
import math
from typing import Tuple, Optional

def extended_gcd(a: int, b: int) -> Tuple[int,int,int]:
    """Return (g, x, y) with g = gcd(a,b) and a*x + b*y = g."""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def is_prime(n: int) -> bool:
    """Deterministic trial division testing suitable for n <= ~1e7.
       Inputs are limited to <= 100000 in UI, so this is fine."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def coprime(a: int, b: int) -> bool:
    return math.gcd(a,b) == 1

def find_random_e(m, limit_attempts: int=1000) -> Optional[int]:
    """Find random e such that gcd(e, m) == 1. Returns None if not found.
       We pick e in [3, m-1] odd numbers for efficiency."""
    if (m <= 2):
        return None
    for i in range(limit_attempts):
        e = random.randrange(3, m)
        if (e % 2 == 0):
            e += 1
        if (e >= m):
            e -= 2
        if (math.gcd(e, m)) == 1:
            return e
    for e in range(3, m):
        if math.gcd(e, m) == 1:
            return e
    return None

def modular_inverse(e: int, m: int) -> Optional[int]:
    """Return d such that (e*d) % m == 1, or None if inverse doesn't exist."""
    g, x, y = extended_gcd(e, m)
    if (g != 1):
        return None
    # x is inverse modulo m; ensure positivity
    d = x % m
    return d

def gen_keys(p: int, q: int) -> dict:
    """Given primes p and q, return a dictionary of RSA constants"""
    n = p*q
    m = (p-1) * (q-1)
    e = find_random_e(m)
    if e is None:
        raise ValueError("Could not select e coprime to phi.")
    d = modular_inverse(e, m)
    if d is None:
        raise ValueError("Modular inverse not found.")
    return {"n": n, "m": m, "e": e, "d": d}

def encrypt_integer(M: int, e: int, n: int) -> int:
    return pow(M, e, n)

def decrypt_integer(C: int, d: int, n: int) -> int:
    return pow(C, d, n)