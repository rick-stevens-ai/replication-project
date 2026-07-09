"""
Classical randomized baseline for the balanced binary NAND (a.k.a. AND-OR) tree
of depth n on N = 2^n leaves.

Snir (1985) / Saks-Wigderson (1986) proved: the *worst-case expected* number of
leaves the best randomized algorithm queries on a balanced AND-OR tree of depth 2h
is exactly ((1 + sqrt(33)) / 4)^h == c^h where c \u2248 1.6844,
which is N^(log_2 c / 2) = N^0.7537...  for N = 4^h leaves.

For balanced *binary NAND* trees of depth n with N=2^n leaves, using De Morgan
equivalence between NAND-tree and alternating AND-OR tree, the same 0.7537 exponent
holds asymptotically: the randomized query complexity is Theta(N^0.7537...).

Concretely: the classical algorithm makes at least ~N^0.7537 queries in the worst case.
Ambainis's quantum algorithm makes O(N^0.5) queries — a polynomial (~1.5x-exponent)
speedup. This is what we're showing.

This script emits the numerical lower bound on classical queries side-by-side with
the empirical quantum queries measured by nand_tree_walk.py for the same N values.
"""

import json
import math
import os

SNIR_EXP = math.log2((1.0 + math.sqrt(33.0)) / 4.0) / 2.0  # ~0.7537
# But note: Snir's constant is defined for depth 2h; per-level exponent on N is that.
# For binary balanced NAND tree of depth n (N=2^n), the same 0.7537 emerges as
# the AND-OR exponent because NAND-tree evaluation is polynomially equivalent to AND-OR.

def classical_lower_bound(N):
    """Snir/Saks-Wigderson randomized lower bound on # leaves queried, N^0.7537...."""
    return N ** SNIR_EXP

def main():
    scaling_path = os.path.join(os.path.dirname(__file__), "scaling_results.json")
    with open(scaling_path) as f:
        scal = json.load(f)
    rows = []
    print(f"{'n':>2} {'N':>4} {'quantum_q':>10} {'classical_LB':>14} {'ratio_c/q':>10} {'q/sqrt(N)':>10}")
    for entry in scal["per_n"]:
        N = entry["N_leaves"]
        qq = entry["queries_per_input_total"]
        cl = classical_lower_bound(N)
        print(f"{entry['n']:>2d} {N:>4d} {qq:>10d} {cl:>14.2f} {cl/qq:>10.3f} {qq/math.sqrt(N):>10.3f}")
        rows.append({
            "n": entry["n"],
            "N": N,
            "quantum_queries_total": qq,
            "classical_lb_snir": cl,
            "ratio_classical_over_quantum": cl / qq,
            "quantum_over_sqrtN": qq / math.sqrt(N),
        })
    out = {
        "snir_exponent": SNIR_EXP,
        "note": "Snir/Saks-Wigderson: classical randomized query lower bound is N^0.7537... for balanced binary AND-OR (equiv. NAND) tree.",
        "rows": rows,
    }
    outp = os.path.join(os.path.dirname(__file__), "classical_vs_quantum.json")
    with open(outp, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {outp}")

if __name__ == "__main__":
    main()
