#!/usr/bin/env python3
"""
Internal-consistency audit of Brahme 2024 Eq. (1):

    P+(D) = PB(D) - PI(D) + delta * (1 - PB(D)) * PI(D)

We verify the algebraic limits that the paper either explicitly or
implicitly relies on:

  L1. delta = 0  =>  P+ = PB - PI  (Brahme's "no compensation" baseline).
  L2. delta = 1  =>  P+ = PB - PB*PI  =  PB * (1 - PI)
        (statistical independence: tumor cure AND no injury).
  L3. PI = 0     =>  P+ = PB  (no injury -> cure equals tumor benefit).
  L4. PB = 1     =>  P+ = 1 - PI + delta*0*PI = 1 - PI
        (perfect tumor cure -> only injury matters; delta drops out).
  L5. PB = 0     =>  P+ = -PI + delta*PI = (delta-1)*PI  <= 0 for delta in [0,1].
        (no tumor benefit -> P+ is non-positive; with delta=0 it equals -PI,
         the maximum-penalty case Brahme calls the "pessimistic" form.)
  L6. Monotonicity in delta: dP+/d(delta) = (1-PB)*PI >= 0 for PB,PI in [0,1].
        So increasing delta (more independence assumption) can never decrease P+.

We also verify the documented numerical results in the smoke
(p_plus_smoke.py) by recomputing them here from scratch.

Outputs a single status line per check (PASS/FAIL) and a summary.
"""

from __future__ import annotations
import math
import sys
import numpy as np


def p_plus(PB, PI, delta):
    return PB - PI + delta * (1.0 - PB) * PI


def poisson_sigmoid(D, D50, gamma50):
    return np.power(2.0, -np.exp(math.e * gamma50 * (1.0 - D / D50)))


def check(label, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {label}" + (f"   ({detail})" if detail else ""))
    return ok


def main() -> int:
    all_ok = True
    print("Brahme 2024 Eq. (1) — analytic internal-consistency audit")
    print("---------------------------------------------------------")

    rng = np.random.default_rng(0)
    PB = rng.uniform(0.0, 1.0, size=20000)
    PI = rng.uniform(0.0, 1.0, size=20000)

    # L1: delta = 0
    lhs = p_plus(PB, PI, 0.0)
    rhs = PB - PI
    all_ok &= check("L1  delta=0  =>  P+ = PB - PI",
                    np.allclose(lhs, rhs),
                    f"max|err|={np.max(np.abs(lhs-rhs)):.2e}")

    # L2: delta = 1 -> PB*(1-PI)
    lhs = p_plus(PB, PI, 1.0)
    rhs = PB * (1.0 - PI)
    all_ok &= check("L2  delta=1  =>  P+ = PB*(1-PI)",
                    np.allclose(lhs, rhs),
                    f"max|err|={np.max(np.abs(lhs-rhs)):.2e}")

    # L3: PI = 0 -> P+ = PB
    PI0 = np.zeros_like(PB)
    for d in (0.0, 0.2, 0.5, 1.0):
        lhs = p_plus(PB, PI0, d)
        all_ok &= check(f"L3  PI=0,  delta={d}  =>  P+ = PB",
                        np.allclose(lhs, PB),
                        f"max|err|={np.max(np.abs(lhs-PB)):.2e}")

    # L4: PB = 1 -> P+ = 1 - PI
    PB1 = np.ones_like(PI)
    for d in (0.0, 0.2, 0.5, 1.0):
        lhs = p_plus(PB1, PI, d)
        rhs = 1.0 - PI
        all_ok &= check(f"L4  PB=1,  delta={d}  =>  P+ = 1 - PI (delta drops out)",
                        np.allclose(lhs, rhs),
                        f"max|err|={np.max(np.abs(lhs-rhs)):.2e}")

    # L5: PB = 0 -> P+ = (delta - 1)*PI <= 0
    PB0 = np.zeros_like(PI)
    for d in (0.0, 0.2, 0.5, 1.0):
        lhs = p_plus(PB0, PI, d)
        rhs = (d - 1.0) * PI
        ok = np.allclose(lhs, rhs) and np.all(lhs <= 1e-12)
        all_ok &= check(f"L5  PB=0,  delta={d}  =>  P+ = (delta-1)*PI <= 0",
                        ok,
                        f"max P+={float(np.max(lhs)):.3e}, max|err|={float(np.max(np.abs(lhs-rhs))):.2e}")

    # L6: monotonicity in delta
    delta_grid = np.linspace(0.0, 1.0, 51)
    nonmono = 0
    for i in range(0, len(PB), 1000):  # subsample for speed
        vals = [p_plus(PB[i], PI[i], d) for d in delta_grid]
        if any(vals[k+1] - vals[k] < -1e-12 for k in range(len(vals)-1)):
            nonmono += 1
    all_ok &= check("L6  P+ is monotone non-decreasing in delta on [0,1]",
                    nonmono == 0,
                    f"violations={nonmono} (out of {len(range(0, len(PB), 1000))} samples)")

    # Numerical reproduction of smoke values
    print("\nNumerical reproduction of smoke headline numbers:")
    D = np.linspace(0.0, 100.0, 1001)
    PBd = poisson_sigmoid(D, 60.0, 3.0)
    PId = poisson_sigmoid(D, 70.0, 4.0)
    expected = {
        0.0: (0.503, 62.9),
        0.2: (0.512, 63.1),
        1.0: (0.554, 63.9),
    }
    for d, (pp_exp, dstar_exp) in expected.items():
        arr = p_plus(PBd, PId, d)
        i = int(np.argmax(arr))
        pp, dstar = float(arr[i]), float(D[i])
        ok = abs(pp - pp_exp) < 1e-3 and abs(dstar - dstar_exp) < 0.2
        all_ok &= check(f"reproduce  delta={d}  P+_max={pp:.3f}  D*={dstar:.1f}",
                        ok,
                        f"expected {pp_exp:.3f} @ {dstar_exp:.1f}")

    # High-LET case
    PB_hi = poisson_sigmoid(D, 60.0, 1.8)
    arr = p_plus(PB_hi, PId, 0.2)
    i = int(np.argmax(arr))
    pp, dstar = float(arr[i]), float(D[i])
    ok = abs(pp - 0.474) < 1e-3 and abs(dstar - 61.4) < 0.2
    all_ok &= check(f"reproduce high-LET delta=0.2  P+_max={pp:.3f}  D*={dstar:.1f}",
                    ok,
                    "expected 0.474 @ 61.4")

    print("\nOverall:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
