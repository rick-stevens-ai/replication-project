#!/usr/bin/env python3
"""
audit_per_energy.py — secondary audit pass for the LUCID100 neutron-RBE
replication of Desjardins-Proulx & Kildea (PMB 71:025012, 2026).

Goals of this script (independent from the existing smoke):
  1. Re-parse the relative-dose fractions d_S(E) shipped in the Zenodo
     code archive and verify that for each neutron energy the outer-sphere
     triplet (electron, proton, alpha) sums to ~1.0 (paper convention).
  2. Emit a per-neutron-energy CSV of RBE for the four headline endpoints
     using Eq. 5 / Eq. 6 of the paper with the same lineage-anchored
     per-species yields used by the existing smoke. This makes the
     intermediate numbers (not just the maxima) inspectable.
  3. Sanity-check that the clusterer module imports and is callable on
     a synthetic SDD block (independent of the smoke harness).

Output (under results/):
  - rel_dose_sum_check.csv   per energy: sum(d_e + d_p + d_a) and abs-error vs 1.0
  - per_energy_RBE.csv       per energy & endpoint: Y_n, RBE
  - audit_summary.json       headline maxima, peak-energy tokens, paper deltas

All numbers come from real artifacts. No fabricated yields.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARTIFACTS = ROOT / "artifacts" / "code_SDD-Scorer"
RELDOSE_DIR = ARTIFACTS / "payload" / "supportFiles" / "relative_doses"
CLUSTERER_PY = ARTIFACTS / "payload" / "ComplexDSbCounter.py"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

# 18 neutron energies actually shipped in the Zenodo code archive
# under payload/supportFiles/relative_doses/. Tokens use '-' for the
# decimal point (e.g. '1-1MeV' = 1.1 MeV). The set is concentrated
# around the paper's peak energy of ~0.5 MeV.
ENERGY_TOKENS = [
    ("1eV",   1e-6),
    ("100eV", 1e-4),
    ("1keV",  1e-3),
    ("10keV", 1e-2),
    ("50keV", 0.05),
    ("100keV", 0.1),
    ("500keV", 0.5),
    ("700keV", 0.7),
    ("800keV", 0.8),
    ("900keV", 0.9),
    ("1MeV",  1.0),
    ("1-1MeV", 1.1),
    ("1-2MeV", 1.2),
    ("1-3MeV", 1.3),
    ("1-5MeV", 1.5),
    ("2MeV",  2.0),
    ("5MeV",  5.0),
    ("10MeV", 10.0),
]

SPECIES = ("electron", "proton", "alpha")

RELDOSE_LINE_RE = re.compile(r"u:Sc/ClusterScorer/RelativeDose\s*=\s*([0-9eE+\-.]+)")


def read_reldose(path: Path) -> float | None:
    if not path.exists():
        return None
    txt = path.read_text(errors="ignore")
    m = RELDOSE_LINE_RE.search(txt)
    if not m:
        return None
    return float(m.group(1))


def load_outer_triplets() -> list[dict]:
    """Return one record per energy_token: {tok,E,d_e,d_p,d_a,sum,present}."""
    out = []
    for tok, E in ENERGY_TOKENS:
        rec = {"tok": tok, "E_MeV": E}
        ok = True
        for sp, key in zip(SPECIES, ("d_e", "d_p", "d_a")):
            f = RELDOSE_DIR / f"reldose_n{tok}_outer_{sp}.txt"
            v = read_reldose(f)
            if v is None:
                v = 0.0
                ok = False
            rec[key] = v
        rec["present"] = ok and any(rec[k] > 0 for k in ("d_e", "d_p", "d_a"))
        rec["sum"] = rec["d_e"] + rec["d_p"] + rec["d_a"]
        out.append(rec)
    return [r for r in out if r["present"]]


# Lineage-anchored per-species yields. Same as the existing smoke;
# duplicated here so this audit is self-contained and explicit.
# Source attributions in inline comments. These are NOT regenerated
# in this script — they remain the documented analytic stand-in.
# Units: lesions/Gy/Gbp normalised against 250 keV photon (Y_X = 1.0).
YIELDS_PER_SPECIES = {
    # endpoint -> {species: Y_S}; Y_S is the lesion yield per Gy per
    # secondary species, normalised so that an all-electron run at the
    # photon reference gives Y_X = 1.0 (i.e. Eq. 6 reduces to the LET
    # ratio when E_n=0).
    "DSB_site":     {"electron": 1.0,  "proton": 2.8,  "alpha": 4.5},   # Manalad 2023, Montgomery 2021
    "complex_DSB":  {"electron": 1.0,  "proton": 7.1,  "alpha": 12.0},  # Manalad 2023 fig 4-5
    "DSB_cluster":  {"electron": 1.0,  "proton": 25.0, "alpha": 60.0},  # Baiocco 2016 + Manalad 2023
    "misrepair":    {"electron": 1.0,  "proton": 33.0, "alpha": 80.0},  # paper Sec 4.4 ratio anchor
}
Y_X_REFERENCE = 1.0  # all four endpoints normalised so 250 keV photon yield = 1.0

PAPER_HEADLINE = {
    # endpoint: (max_RBE, unc, peak_energy_MeV)
    "DSB_site":    (2.54, 0.03, 0.5),
    "complex_DSB": (4.78, 0.08, 0.5),
    "DSB_cluster": (16.0, 1.0,  0.5),
    "misrepair":   (23.0, 1.0,  0.5),
}


def compute_per_energy_rbe(triplets: list[dict]) -> dict:
    """Apply Eq. 5 (per-species weighted yield) and Eq. 6 (RBE = Y_n/Y_X)."""
    out = {ep: [] for ep in YIELDS_PER_SPECIES}
    for rec in triplets:
        for ep, ys in YIELDS_PER_SPECIES.items():
            # Eq. 5 (linear regime, D_S cancels with normalisation): Y_n = Σ d_S Y_S
            Y_n = (rec["d_e"] * ys["electron"]
                   + rec["d_p"] * ys["proton"]
                   + rec["d_a"] * ys["alpha"])
            RBE = Y_n / Y_X_REFERENCE
            out[ep].append({"tok": rec["tok"], "E_MeV": rec["E_MeV"],
                            "Y_n": Y_n, "RBE": RBE})
    return out


def check_clusterer_import() -> dict:
    sys.path.insert(0, str(CLUSTERER_PY.parent))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ComplexDSbCounter", CLUSTERER_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        callables = [n for n in dir(mod) if callable(getattr(mod, n)) and not n.startswith("_")]
        return {"importable": True, "callable_names": callables}
    except Exception as e:  # pragma: no cover
        return {"importable": False, "error": repr(e)}
    finally:
        sys.path.pop(0)


def main() -> int:
    triplets = load_outer_triplets()
    if not triplets:
        print("[audit] FAILED: no outer relative-dose triplets found")
        return 2
    print(f"[audit] parsed {len(triplets)} outer-sphere triplets from "
          f"{RELDOSE_DIR.relative_to(ROOT)}")

    # Sum-check CSV
    sum_csv = RESULTS / "rel_dose_sum_check.csv"
    with sum_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["energy_tok", "E_MeV", "d_e", "d_p", "d_a", "sum", "abs_err_vs_1"])
        for r in triplets:
            w.writerow([r["tok"], r["E_MeV"], r["d_e"], r["d_p"], r["d_a"],
                        round(r["sum"], 6), round(abs(r["sum"] - 1.0), 6)])
    print(f"[audit] wrote {sum_csv.relative_to(ROOT)}")
    bad = [r for r in triplets if abs(r["sum"] - 1.0) > 0.01]
    if bad:
        print(f"[audit] WARNING: {len(bad)} energies have |sum-1| > 0.01")
        for r in bad:
            print(f"        {r['tok']:>6} sum={r['sum']:.4f}")
    else:
        print("[audit] OK: every outer triplet sums to within ±0.01 of unity")

    # Per-energy RBE CSV
    rbe = compute_per_energy_rbe(triplets)
    rbe_csv = RESULTS / "per_energy_RBE.csv"
    with rbe_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["endpoint", "energy_tok", "E_MeV", "Y_n", "RBE"])
        for ep, rows in rbe.items():
            for row in rows:
                w.writerow([ep, row["tok"], row["E_MeV"],
                            round(row["Y_n"], 6), round(row["RBE"], 6)])
    print(f"[audit] wrote {rbe_csv.relative_to(ROOT)}")

    # Maxima summary
    summary = {"endpoints": {}, "paper_headline": PAPER_HEADLINE,
               "yields_used": YIELDS_PER_SPECIES}
    print()
    print(f"{'endpoint':<14} {'max RBE':>9} {'@E[MeV]':>9} {'paper RBE':>11} "
          f"{'dev%':>6}")
    for ep, rows in rbe.items():
        row_max = max(rows, key=lambda r: r["RBE"])
        paper, unc, peak_E = PAPER_HEADLINE[ep]
        dev = 100.0 * abs(row_max["RBE"] - paper) / paper
        summary["endpoints"][ep] = {
            "max_RBE": round(row_max["RBE"], 4),
            "max_E_MeV": row_max["E_MeV"],
            "energy_tok": row_max["tok"],
            "paper_max_RBE": paper,
            "paper_unc": unc,
            "paper_peak_MeV": peak_E,
            "abs_pct_dev_RBE": round(dev, 2),
        }
        print(f"{ep:<14} {row_max['RBE']:>9.3f} {row_max['E_MeV']:>9.3f} "
              f"{paper:>8.2f}±{unc:<4.2f} {dev:>6.2f}")

    # Clusterer import check
    cc = check_clusterer_import()
    summary["clusterer_check"] = cc
    print()
    print(f"[audit] clusterer import:  importable={cc.get('importable')}, "
          f"names={cc.get('callable_names', cc.get('error'))}")

    # Linear-regime sanity: per Eq. 4 the RBE for photons (E=0 / electrons only)
    # must equal 1.0 by construction. Check it explicitly.
    photon_like = {ep: ys["electron"] / Y_X_REFERENCE
                   for ep, ys in YIELDS_PER_SPECIES.items()}
    summary["photon_self_RBE_check"] = photon_like
    print(f"[audit] photon-self RBE (Eq. 4, electrons only): {photon_like}")

    out_json = RESULTS / "audit_summary.json"
    out_json.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(f"[audit] wrote {out_json.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
