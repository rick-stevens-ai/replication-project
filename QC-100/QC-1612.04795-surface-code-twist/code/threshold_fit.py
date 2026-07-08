#!/usr/bin/env python3
"""
Estimate the crossing-point threshold from threshold_scan.json.

Uses a simple bracket-and-linear-interpolate method: for each pair of adjacent
distances (d, d+2), find the p at which their logical-error-rate curves cross
(smaller d has lower LER below threshold, higher LER above).
"""
import json
from pathlib import Path

EV = Path(__file__).resolve().parents[1] / "report" / "evidence"

def crossings(rows, regime):
    data = [r for r in rows if r["regime"] == regime]
    by_d = {}
    for r in data:
        by_d.setdefault(r["d"], []).append((r["p"], r["logical_error_rate"]))
    for d in by_d:
        by_d[d].sort()
    dists = sorted(by_d)
    print(f"\n--- {regime} ---")
    for i in range(len(dists) - 1):
        d1, d2 = dists[i], dists[i + 1]
        c1 = by_d[d1]
        c2 = by_d[d2]
        ps1 = [p for p, _ in c1]
        # walk shared ps and find sign change in (LER_d2 - LER_d1)
        prev_sign = None
        prev_p = None
        prev_diff = None
        for (p1, l1), (p2, l2) in zip(c1, c2):
            assert abs(p1 - p2) < 1e-9
            diff = l2 - l1  # negative below threshold (higher-d wins)
            sign = 1 if diff > 0 else (-1 if diff < 0 else 0)
            if prev_sign is not None and prev_sign * sign < 0:
                # linear interp in p vs diff
                p_cross = prev_p + (p1 - prev_p) * (-prev_diff) / (diff - prev_diff)
                print(f"  d={d1} vs d={d2}: threshold ≈ {p_cross:.4f}")
                break
            prev_sign, prev_p, prev_diff = sign, p1, diff
        else:
            print(f"  d={d1} vs d={d2}: no sign change in swept range")

def main():
    rows = json.loads((EV / "threshold_scan.json").read_text())
    crossings(rows, "A_ideal_syndrome")
    crossings(rows, "B_phenomenological")

if __name__ == "__main__":
    main()
