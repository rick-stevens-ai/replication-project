#!/usr/bin/env python3
"""
Driver for arXiv:2209.10768 replication. Runs all 5 machine-checkable claims,
writes work/results.json. Real computation only.

Loop-current order parameter = GAUGE-INVARIANT triangle plaquette flux
(triangle_flux), NOT raw Im(chi_ij) (which is gauge dependent).

Usage: python3 run_all.py [--quick]
"""
from __future__ import annotations
import json, sys, time, os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kagome_tV1V2 as M

QUICK = "--quick" in sys.argv
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "results.json")


def sanitize(o):
    """Recursively convert numpy scalars/arrays/bools to JSON-native types."""
    if isinstance(o, dict):
        return {k: sanitize(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [sanitize(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return sanitize(o.tolist())
    return o


results = {"paper": "arXiv:2209.10768", "quick": QUICK, "claims": {}}
t0 = time.time()

# ---------------------------------------------------------------------------
# C5 / baseline: kagome TB band structure & vH sublattice localization.
# ---------------------------------------------------------------------------
print("[C5] baseline TB / vH check ...", flush=True)
tb = M.tb_bands_and_dos(nk=48 if not QUICK else 24, filling=5.0/12.0)
subw = np.array(tb["M_subweight"])          # rows=sublattice, cols=band
max_localization = subw.max(axis=0).tolist()
results["claims"]["C5_vH_localization"] = {
    "M_energies": tb["M_energies"],
    "M_subweight_per_band": tb["M_subweight"],
    "max_sublattice_weight_per_band": max_localization,
    "vh_band_min_sublattice_weight": tb["vh_band_min_sublattice_weight"],
    "chemical_potential_at_5_12": tb["mu"],
    "bandmin": tb["bandmin"], "bandmax": tb["bandmax"],
    "note": "Kagome vH saddle at each M with E={-2,0,2}t. The vH band has ~0 "
            "weight on one sublattice at each M point (sublattice interference), "
            "which suppresses onsite/same-sublattice order -> off-site bond order.",
}
print(f"   M energies = {np.round(tb['M_energies'],3)}  vH-band min sublattice weight = {tb['vh_band_min_sublattice_weight']}")

# ---------------------------------------------------------------------------
# C1: bare bond susceptibility channel selectivity at q=M.
# ---------------------------------------------------------------------------
print("[C1] bare bond susceptibilities at q=M ...", flush=True)
chi = M.bare_bond_susceptibility(nk=60 if not QUICK else 30, T=0.005, filling=5.0/12.0)
nn_real, nn_imag = chi["nn_real"], chi["nn_imag"]
nnn_real, nnn_imag = chi["nnn_real"], chi["nnn_imag"]
c1_pass = (abs(nn_real) > abs(nn_imag)) and (abs(nnn_imag) > abs(nnn_real))
results["claims"]["C1_susceptibility_channel"] = {
    "nn_real": nn_real, "nn_imag": nn_imag,
    "nnn_real": nnn_real, "nnn_imag": nnn_imag,
    "nn_real_dominates": abs(nn_real) > abs(nn_imag),
    "nnn_imag_dominates": abs(nnn_imag) > abs(nnn_real),
    "pass": c1_pass,
    "note": "Paper: nn real (breathing) leads; nnn imaginary (breathing) leads.",
}
print(f"   nn_real={nn_real:.4f} nn_imag={nn_imag:.4f} | nnn_real={nnn_real:.4f} nnn_imag={nnn_imag:.4f} | pass={c1_pass}")

# ---------------------------------------------------------------------------
# C3: self-consistent MF. Loop-current OP = gauge-invariant triangle flux.
# ---------------------------------------------------------------------------
print("[C3] self-consistent mean-field ...", flush=True)
sc = M.Supercell()
nk_mf = 8 if QUICK else 12
Tmf = 0.004

def solve(V1, V2, seeds=("ISD","LC","LCstrong"), nk=nk_mf, nrs=None):
    if nrs is None:
        nrs = 1 if QUICK else 2
    best = None
    allres = []
    for s in seeds:
        for rs in range(nrs):
            r = M.self_consistent(sc, t=1.0, V1=V1, V2=V2, filling=5.0/12.0,
                                  nk=nk, T=Tmf, seed=s, rng_seed=rs,
                                  max_iter=300 if not QUICK else 120,
                                  tol=1e-6, mix=0.4)
            r["seed_won"] = s
            allres.append(r)
            if best is None or r["E_per_site"] < best["E_per_site"]:
                best = r
    return best, allres

r_v1only, _ = solve(2.0, 0.0)
r_lc2, _ = solve(0.8, 1.6)
r_lc1, _ = solve(0.5, 2.5)

results["claims"]["C3_spontaneous_LC"] = {
    "V1only_V=(2,0)": {"loop_flux": r_v1only["loop_flux"], "maxIm_nnn": r_v1only["max_Im_nnn"],
                        "E": r_v1only["E_per_site"], "seed": r_v1only["seed_won"]},
    "LC2_V=(0.8,1.6)": {"loop_flux": r_lc2["loop_flux"], "maxIm_nnn": r_lc2["max_Im_nnn"],
                         "E": r_lc2["E_per_site"], "seed": r_lc2["seed_won"]},
    "LC1_V=(0.5,2.5)": {"loop_flux": r_lc1["loop_flux"], "maxIm_nnn": r_lc1["max_Im_nnn"],
                         "E": r_lc1["E_per_site"], "seed": r_lc1["seed_won"]},
    "note": "loop_flux = gauge-invariant triangle plaquette flux (true LC OP). "
            "V1-only should give ~0 loop flux (real CDW); V2 points nonzero.",
}
print(f"   V1only loop_flux={r_v1only['loop_flux']:.4f}")
print(f"   LC2    loop_flux={r_lc2['loop_flux']:.4f}")
print(f"   LC1    loop_flux={r_lc1['loop_flux']:.4f}")

# ISD->LC transition scan at V1=1.75. ISD seed = purely real; LC seed = complex.
print("[C3b] ISD->LC transition scan (V1=1.75) ...", flush=True)
scan = []
v2vals = np.arange(1.5, 3.21, 0.3 if QUICK else 0.15)
for V2 in v2vals:
    r_isd = M.self_consistent(sc, 1.0, 1.75, V2, nk=nk_mf, T=Tmf, seed="ISD",
                              max_iter=250 if not QUICK else 100, tol=1e-6, mix=0.4)
    r_lc, _ = solve(1.75, V2, seeds=("LC","LCstrong"))
    gs = r_isd if r_isd["E_per_site"] <= r_lc["E_per_site"] else r_lc
    scan.append({"V2": float(V2), "E_isd": r_isd["E_per_site"], "E_lc": r_lc["E_per_site"],
                 "isd_loopflux": r_isd["loop_flux"], "lc_loopflux": r_lc["loop_flux"],
                 "gs_loopflux": gs["loop_flux"], "gs_is_LC": gs["loop_flux"] > 0.01})
    print(f"   V2={V2:.2f} E_isd={r_isd['E_per_site']:.4f}(flux {r_isd['loop_flux']:.3f}) "
          f"E_lc={r_lc['E_per_site']:.4f}(flux {r_lc['loop_flux']:.3f}) gs_LC={gs['loop_flux']>0.01}")
trans = None
for i in range(1, len(scan)):
    if (not scan[i-1]["gs_is_LC"]) and scan[i]["gs_is_LC"]:
        trans = 0.5*(scan[i-1]["V2"]+scan[i]["V2"]); break
results["claims"]["C3b_ISD_LC_transition"] = {"scan": scan, "transition_V2": trans,
    "paper_value": 1.81, "note": "First-order ISD->LC2 transition; paper V2~1.81 at V1=1.75."}
print(f"   transition V2 ~ {trans} (paper 1.81)")

# ---------------------------------------------------------------------------
# C4: Chern numbers of converged LC states.
# ---------------------------------------------------------------------------
print("[C4] Chern numbers of LC states ...", flush=True)
nk_ch = 12 if QUICK else 18
chern = {}
for label, (V1, V2), r in [("LC1", (0.5,2.5), r_lc1), ("LC2", (0.8,1.6), r_lc2)]:
    C = M.chern_number(sc, r["chi_nn"], r["chi_nnn"], t=1.0, V1=V1, V2=V2,
                       filling=5.0/12.0, nk=nk_ch, T=Tmf)
    chern[label] = {"chern_occupied": C, "V": [V1,V2], "loop_flux": r["loop_flux"]}
    print(f"   {label} Chern(occupied) = {C}")
results["claims"]["C4_chern_numbers"] = {
    "computed": chern,
    "paper_total_N": {"LC1": 1, "LC2": -1, "LC3": 0, "LC4": -1},
    "note": "Total Chern of occupied bands (nocc=5). Paper N=1,-1,0,-1 for LC1..4. "
            "Overall sign is orientation/gauge convention dependent; |C| and the "
            "nontrivial-vs-trivial distinction are the physical content.",
}

results["runtime_sec"] = round(time.time()-t0, 1)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(sanitize(results), f, indent=2)
print(f"\nWrote {OUT}  ({results['runtime_sec']}s)")
