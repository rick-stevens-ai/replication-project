"""
Direct verification of the closed-form gate-count formulas from
Cai (arXiv:1910.02719), Appendix A2:

    N1q,ha(V) = 4 * V^{3/2} + 7 * V - 4 * sqrt(V)
    N2q,ha(V) = 8 * V^{3/2} +   V   - 4 * sqrt(V)

    T(V) = (8 sqrt(V) + 5) tau_1q + (16 sqrt(V) + 2) tau_2q

Reported headline (V=25, 5x5 Hubbard = 50-qubit target of the paper):

    N1q ~= 650
    N2q ~= 1000
    T   ~= 45 tau_1q + 80 tau_2q

This script:
  1. Evaluates the formulas at a sweep of V values.
  2. Confirms V=25 -> N1q~650, N2q~1000, T~45 tau_1q + 80 tau_2q.
  3. Writes a JSON evidence file.
"""

from __future__ import annotations

import json
import math
import os
import sys


def n1q_ha(V: int) -> float:
    return 4 * V ** 1.5 + 7 * V - 4 * math.sqrt(V)


def n2q_ha(V: int) -> float:
    return 8 * V ** 1.5 + 1 * V - 4 * math.sqrt(V)


def time_ha(V: int) -> tuple[float, float]:
    return (8 * math.sqrt(V) + 5, 16 * math.sqrt(V) + 2)


def main():
    sizes = [4, 6, 9, 12, 16, 20, 25, 30, 36, 49]
    print("V     N1q,ha      N2q,ha      T (tau_1q, tau_2q)")
    print("-" * 55)
    rows = []
    for V in sizes:
        n1 = n1q_ha(V)
        n2 = n2q_ha(V)
        t1, t2 = time_ha(V)
        print(f"{V:<4}  {n1:>9.2f}   {n2:>9.2f}   ({t1:>6.2f}, {t2:>6.2f})")
        rows.append({
            "V": V,
            "N1q_ha": n1,
            "N2q_ha": n2,
            "T_tau1q": t1,
            "T_tau2q": t2,
        })

    # Headline check
    V = 25
    n1, n2 = n1q_ha(V), n2q_ha(V)
    t1, t2 = time_ha(V)
    paper_n1, paper_n2 = 650, 1000
    paper_t1, paper_t2 = 45, 80
    print()
    print(f"Headline check (paper reports N1q~{paper_n1}, N2q~{paper_n2}, "
          f"T~{paper_t1} tau_1q + {paper_t2} tau_2q at V=25):")
    print(f"  formula: N1q = {n1:.2f}, N2q = {n2:.2f}, "
          f"T = {t1:.2f} tau_1q + {t2:.2f} tau_2q")
    print(f"  |diff| : |N1q| = {abs(n1-paper_n1):.2f}, "
          f"|N2q| = {abs(n2-paper_n2):.2f}, "
          f"|T1| = {abs(t1-paper_t1):.2f}, |T2| = {abs(t2-paper_t2):.2f}")

    tol = 10
    ok_n1 = abs(n1 - paper_n1) <= tol
    ok_n2 = abs(n2 - paper_n2) <= tol
    ok_t1 = abs(t1 - paper_t1) <= 2
    ok_t2 = abs(t2 - paper_t2) <= 5
    all_ok = ok_n1 and ok_n2 and ok_t1 and ok_t2
    print(f"  MATCH within stated tolerance: {all_ok}")

    out = os.path.join(os.path.dirname(__file__), "..", "report",
                       "evidence", "formula_check.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({
            "paper": "1910.02719",
            "formulas": {
                "N1q_ha": "4 V**1.5 + 7 V - 4 sqrt(V)",
                "N2q_ha": "8 V**1.5 +   V - 4 sqrt(V)",
                "T": "(8 sqrt(V)+5) tau_1q + (16 sqrt(V)+2) tau_2q",
            },
            "sweep": rows,
            "headline_V25": {
                "formula": {"N1q": n1, "N2q": n2,
                            "T_tau1q": t1, "T_tau2q": t2},
                "paper":   {"N1q": paper_n1, "N2q": paper_n2,
                            "T_tau1q": paper_t1, "T_tau2q": paper_t2},
                "match": all_ok,
            },
        }, f, indent=2)
    print(f"\nWrote {out}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
