#!/usr/bin/env python3
"""Replicates Fig. 9 (TCP for 10^6 H460 cells) and Fig. 10 (CDP for 100 H460 cells)
of Abolfath et al. EPJ-D 73:64 (2019) using the published Guan 2015 H460 α(LET), β(LET)
table and the paper's TCP / CDP formulae.

Paper Eq. 50:  TCP(∞) = 1 − e^{−L[n(∞)]}^{N_0}  =  (1 − SF)^{N_0}
Paper Eq. 52:  TCP = Π_k (1 − SF_k)^{N_k}
For a single-voxel mono-energetic beam: TCP(D, LET) = (1 − SF(D, LET))^{N_0}

For CDP (cell death probability for a 100-cell well — Sec. III D):
    CDP(D, LET) = 1 − TCP^{-1}(N_0=1) trivial; use authors' definition:
    CDP = 1 − (1 − killprob_per_cell)^N0  with killprob = 1 − SF
    => CDP = 1 − SF(D, LET)^{N_0}  is the survival of >=1 cell in the well; flip:
    CDP_authors = 1 − SF(D, LET)^{N_0}  for "any cell dies" is wrong direction.
    The authors actually define CDP as "probability the well is dead" = (1−SF)^{N_0}.
    For 100 cells, this is a sigmoid that turns on near where SF drops below ~5/N0.

We compute both TCP_N0 and CDP_100 = (1-SF)^N0 with N0=100; sigmoid turning point
should coincide with the maximum measured dose at each LET (Table 1 last column).
"""
from __future__ import annotations

import csv
import json
import math
import pathlib

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "guan2015_table1.csv"
FIG  = ROOT / "figures"
OUT  = ROOT / "results" / "tcp_cdp_eq50.json"


def load_alpha_beta(cell: str) -> dict:
    rows = []
    with DATA.open() as fh:
        for r in csv.DictReader(fh):
            rows.append({k: float(v) for k, v in r.items()})
    return {
        "LET":   np.array([r["LET_keV_per_um"] for r in rows]),
        "alpha": np.array([r[f"{cell}_alpha"]  for r in rows]),
        "beta":  np.array([r[f"{cell}_beta"]   for r in rows]),
    }


def sf(D: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    return np.exp(-alpha * D - beta * D**2)


def tcp_curve(D: np.ndarray, alpha: float, beta: float, N0: int) -> np.ndarray:
    """Eq. 50: TCP = (1 - SF)^N0  — probability ALL N0 cells die."""
    s = sf(D, alpha, beta)
    # Numerical guard: when s is near 1, (1-s)^N0 underflows fine
    return np.power(1.0 - s, N0)


def d_at_tcp(target_tcp: float, alpha: float, beta: float, N0: int) -> float:
    """Bisection root for D where TCP = target."""
    lo, hi = 0.0, 50.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if tcp_curve(np.array([mid]), alpha, beta, N0)[0] < target_tcp:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> int:
    d = load_alpha_beta("H460")
    LETs = d["LET"]
    alphas = d["alpha"]; betas = d["beta"]

    Dgrid = np.linspace(0, 12, 481)
    result = {"cell_line": "H460", "N0_TCP": 1_000_000, "N0_CDP": 100,
              "LET_keV_per_um": LETs.tolist(), "TCP_50pct_dose_Gy": {},
              "CDP_50pct_dose_Gy": {}, "fig9_sigmoid_shift": {}}

    # Fig. 9: TCP for N0=1e6 cells, mm voxel
    fig, ax = plt.subplots(figsize=(7, 5))
    for L, a, b in zip(LETs, alphas, betas):
        tcp = tcp_curve(Dgrid, a, b, 1_000_000)
        ax.plot(Dgrid, tcp, label=f"LET={L:.1f}")
        try:
            d50 = d_at_tcp(0.5, a, b, 1_000_000)
        except Exception:
            d50 = float("nan")
        result["TCP_50pct_dose_Gy"][f"{L:.2f}"] = d50
    ax.set_xlabel("Dose [Gy]"); ax.set_ylabel("TCP")
    ax.set_title(r"H460 TCP (Eq. 50) — N$_0$ = 10$^6$ cells per voxel")
    ax.set_xlim(0, 12); ax.legend(fontsize=7, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "tcp_eq50_H460_fig9.png", dpi=130); plt.close(fig)

    # Fig. 10b: CDP for N0=100 cells per well
    fig, ax = plt.subplots(figsize=(7, 5))
    for L, a, b in zip(LETs, alphas, betas):
        cdp = tcp_curve(Dgrid, a, b, 100)
        ax.plot(Dgrid, cdp, label=f"LET={L:.1f}")
        try:
            d50 = d_at_tcp(0.5, a, b, 100)
        except Exception:
            d50 = float("nan")
        result["CDP_50pct_dose_Gy"][f"{L:.2f}"] = d50
    ax.set_xlabel("Dose [Gy]"); ax.set_ylabel("CDP")
    ax.set_title(r"H460 CDP (Eq. 50) — N$_0$ = 100 cells per well (Fig. 10b)")
    ax.set_xlim(0, 12); ax.legend(fontsize=7, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "cdp_eq50_H460_fig10b.png", dpi=130); plt.close(fig)

    # Headline claim test: Fig. 9 says TCP sigmoid shifts to LOWER dose with INCREASING LET
    d50_vec = np.array([result["TCP_50pct_dose_Gy"][f"{L:.2f}"] for L in LETs])
    monotone_decrease = bool(d50_vec[-1] < d50_vec[0])
    result["fig9_sigmoid_shift"] = {
        "D50_TCP_at_LET0p9": float(d50_vec[0]),
        "D50_TCP_at_LET19":  float(d50_vec[-1]),
        "shift_factor":      float(d50_vec[0] / d50_vec[-1]),
        "monotone_decrease": monotone_decrease,
    }

    # Headline claim test from Sec III D: for LET=19 keV/µm, "no cells survive beyond
    # D=1.6 Gy"; that should put the CDP_100 sigmoid turning point near 1.6 Gy.
    d50_CDP_LET19 = result["CDP_50pct_dose_Gy"]["19.00"]
    d50_CDP_LET0p9 = result["CDP_50pct_dose_Gy"]["0.90"]
    paper_max_dose_LET19 = 1.6  # Gy, quoted in §III D / Fig 10a arrow
    result["fig10_termination_check"] = {
        "CDP_50pct_dose_LET19_Gy":    float(d50_CDP_LET19),
        "paper_quoted_max_dose_LET19_Gy": paper_max_dose_LET19,
        "abs_err_Gy":     float(abs(d50_CDP_LET19 - paper_max_dose_LET19)),
        "rel_err_pct":    float(100 * abs(d50_CDP_LET19 - paper_max_dose_LET19) / paper_max_dose_LET19),
        "CDP_50pct_dose_LET0p9_Gy":   float(d50_CDP_LET0p9),
    }

    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps({
        "fig9":  result["fig9_sigmoid_shift"],
        "fig10": result["fig10_termination_check"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
