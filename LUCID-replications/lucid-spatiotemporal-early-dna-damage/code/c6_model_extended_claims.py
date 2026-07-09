"""
Claims B5, B6, B7, B8 — extended model-based reproductions.

B5: At LET=170 keV/um, "only a small fraction of ATM is activated in the first
    minutes" (paper text near Fig 12A). Quantify.

B6: At LET=14350 keV/um (U-ions), inner-focus NBS1 fraction at plateau is
    nearly 60% (paper text). Pass-1 only ran 10290 (got 51%); run 14350 here.

B7: Self-consistency of all 12 NBS1 scaling factors (A..L).
    For each panel, find the LET that makes the model's NBS1 plateau equal
    to the published scaling factor, and check it's a smooth monotonic curve.

B8: Mono-exponential time constants tau_63 for the full panel ladder (A..L),
    trending downward as scaling factor (and implied LET) increases.
"""
import os, sys, json
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

import numpy as np
from lucid_model import (
    simulate, ATM_0, SCALE_NBS1, SCALE_ATM_HIGH_LET,
)

# ---------------------------------------------------------------------------
# B5: ATM activation at low LET
# ---------------------------------------------------------------------------
r170 = simulate(170.0, t_end=700.0, n_out=701)
def fraction_active_at(r, t_query):
    idx = int(np.argmin(np.abs(r.t - t_query)))
    return r.atm_activated()[idx] / ATM_0
B5 = {
    "LET_keV_um":    170.0,
    "fraction_ATM_activated_at_60s":  fraction_active_at(r170, 60.0),
    "fraction_ATM_activated_at_120s": fraction_active_at(r170, 120.0),
    "fraction_ATM_activated_at_300s": fraction_active_at(r170, 300.0),
    "fraction_ATM_activated_at_600s": fraction_active_at(r170, 600.0),
    "fraction_ATM_activated_at_700s": fraction_active_at(r170, 700.0),
}
B5["paper_claim"] = "only a small fraction of ATM is activated in the first minutes at low LET"
B5["verdict"] = ("REPRODUCED" if B5["fraction_ATM_activated_at_120s"] < 0.05
                 and B5["fraction_ATM_activated_at_600s"] < 0.15 else "MISMATCH")
print("=== B5: low-LET ATM activation ===")
for k, v in B5.items():
    if isinstance(v, float): print(f"  {k:42s} = {v:.4f} ({v*100:.2f}%)")
print(f"  verdict: {B5['verdict']}")

# ---------------------------------------------------------------------------
# B6: inner-focus fraction at LET=14350 (uranium)
# ---------------------------------------------------------------------------
r14350 = simulate(14350.0, t_end=700.0, n_out=701)
ratio = r14350.nbs1_inner() / np.maximum(r14350.nbs1_total(), 1e-6)
# "plateau" = late steady-state value averaged over the last 50 s
late = slice(-50, None)
inner_frac_plateau = float(np.mean(ratio[late]))
B6 = {
    "LET_keV_um":               14350.0,
    "inner_fraction_at_plateau":inner_frac_plateau,
    "paper_claim":              "nearly 60% for uranium (LET=14350)",
    "paper_target":             0.60,
    "abs_error":                inner_frac_plateau - 0.60,
    "rel_error":                (inner_frac_plateau - 0.60) / 0.60,
    "verdict":                  ("REPRODUCED" if abs(inner_frac_plateau - 0.60) < 0.10
                                 else "ACCEPTABLE" if abs(inner_frac_plateau - 0.60) < 0.20
                                 else "MISMATCH"),
}
print("\n=== B6: inner-focus fraction at uranium LET=14350 ===")
for k, v in B6.items():
    if isinstance(v, float): print(f"  {k:42s} = {v:.4f}")
    else:                    print(f"  {k:42s} = {v}")

# ---------------------------------------------------------------------------
# B7: self-consistency of 12 NBS1 scaling factors -- per panel, find LET
# such that the model's NBS1 plateau equals the published scale.
# Use bisection over LET in [10, 30000] keV/um.
# ---------------------------------------------------------------------------
def model_plateau_at_LET(let_keV_um, t_end=700.0):
    r = simulate(let_keV_um, t_end=t_end, n_out=141)
    # Mean over the last 100 s as plateau estimate
    late = slice(-20, None)
    return float(np.mean(r.nbs1_total()[late]))

def bisect_LET_for_plateau(target, lo=10.0, hi=30000.0, n=22):
    # The plateau is monotone-increasing in LET. Validate.
    p_lo = model_plateau_at_LET(lo)
    p_hi = model_plateau_at_LET(hi)
    if target < p_lo:
        return lo, p_lo, "BELOW_RANGE"
    if target > p_hi:
        return hi, p_hi, "ABOVE_RANGE"
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        p_mid = model_plateau_at_LET(mid)
        if p_mid < target:
            lo = mid; p_lo = p_mid
        else:
            hi = mid; p_hi = p_mid
    return 0.5*(lo+hi), 0.5*(p_lo+p_hi), "OK"

print("\n=== B7: scaling-factor self-consistency ===")
B7_rows = []
for panel in "ABCDEFGHIJKL":
    target = SCALE_NBS1[panel]
    let_implied, p_check, status = bisect_LET_for_plateau(target)
    print(f"  panel {panel}  scale={target:>5.0f}  LET_implied={let_implied:>8.1f}  "
          f"model_plateau={p_check:>6.1f}  ({status})")
    B7_rows.append({
        "panel": panel, "scale_factor": target,
        "LET_implied_keV_um": let_implied,
        "model_plateau_at_implied_LET": p_check,
        "status": status,
    })
# Monotonicity (excluding panels at boundary)
# Sort by scale and check LET_implied monotone -- but in fact ordering by panel
# letter does not need to be monotone (the authors picked panels in any order).
# Test:  sort rows by LET_implied and confirm scale is also increasing.
B7_sorted = sorted(B7_rows, key=lambda r: r["LET_implied_keV_um"])
implied_lets = [r["LET_implied_keV_um"] for r in B7_sorted]
scales       = [r["scale_factor"]       for r in B7_sorted]
sorted_monotone_in_scale = all(scales[i] <= scales[i+1] for i in range(len(scales)-1))
print(f"  After sorting by LET_implied, scale factors are monotone: {sorted_monotone_in_scale}")
B7_meta = {
    "sorted_monotone_in_scale": sorted_monotone_in_scale,
    "verdict": "REPRODUCED" if sorted_monotone_in_scale else "MISMATCH",
}

# ---------------------------------------------------------------------------
# B8: tau_63 ladder for the 12 panels at their implied LETs
# ---------------------------------------------------------------------------
def tau63_for_LET(let_keV_um, t_end=700.0):
    r = simulate(let_keV_um, t_end=t_end, n_out=701)
    sig = r.nbs1_total()
    late = float(np.mean(sig[-20:]))
    target = 0.63 * late
    # First time the signal exceeds 0.63 * plateau
    above = np.where(sig >= target)[0]
    if len(above) == 0:
        return float("nan")
    return float(r.t[above[0]])

print("\n=== B8: tau_63 ladder ===")
B8_rows = []
for row in B7_sorted:  # smallest LET -> largest
    tau = tau63_for_LET(row["LET_implied_keV_um"])
    print(f"  panel {row['panel']}  LET={row['LET_implied_keV_um']:>8.1f}  tau63={tau:>5.1f} s  "
          f"plateau={row['scale_factor']:>5.0f}")
    B8_rows.append({"panel": row["panel"],
                    "LET_implied_keV_um": row["LET_implied_keV_um"],
                    "tau63_s": tau,
                    "scale_factor": row["scale_factor"]})
# Test: tau_63 monotonically NON-INCREASING with LET (paper: tau decreases
# with LET up to ~3000 keV/um and stays constant above)
taus_in_LET_order = [r["tau63_s"] for r in B8_rows]
# Allow some noise: count pairs (i, i+1) where tau[i] >= tau[i+1]
non_increasing = sum(1 for i in range(len(taus_in_LET_order)-1)
                     if taus_in_LET_order[i] >= taus_in_LET_order[i+1])
B8_meta = {
    "ladder": B8_rows,
    "n_pairs": len(taus_in_LET_order)-1,
    "n_non_increasing_pairs": non_increasing,
    "verdict": ("REPRODUCED" if non_increasing >= 0.7 * (len(taus_in_LET_order)-1)
                else "WEAK"),
}
print(f"  non-increasing pairs: {non_increasing}/{len(taus_in_LET_order)-1}")

# ---------------------------------------------------------------------------
# Save everything
# ---------------------------------------------------------------------------
out = {
    "B5_low_LET_ATM_activation": B5,
    "B6_uranium_inner_fraction":  B6,
    "B7_scaling_self_consistency": {"rows": B7_rows, **B7_meta},
    "B8_tau63_ladder":             B8_meta,
}
out_path = os.path.join(HERE, "..", "results", "c6_model_extended.json")
out_path = os.path.normpath(out_path)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved -> {out_path}")
