#!/usr/bin/env python3
"""Quantitative replication of Abolfath et al. (EPJ-D 2019) Eq. 32 piecewise-linear
fit to the H460/H1437 NSCLC α(LET), β(LET) clonogenic survival data of
Guan et al. (Sci. Rep. 5:9850, 2015 — Table 1).

The paper's working model (Eq. 32) is:
    α(LET_d) = α0 + α1·LET_d   (piecewise: slope1 for LET≤5.08 keV/µm, slope2 for LET≥10.8)
    β(LET_d) = β_x             (in the simplest form: β constant at the photon value)
The paper notes (Sec. III A) that β is in fact also weakly LET-dependent and is fit as
a polynomial in the 3D global fit; we test both "β constant" (Eq. 32 strict) and
"β piecewise linear" (Eq. 21–22 truncation) variants.

Outputs: results/guan2015_eq32_fit.json  +  figures/{guan_alpha_fit,guan_beta_fit,guan_rbe_compare}.png
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
OUT  = ROOT / "results" / "guan2015_eq32_fit.json"

# Regime boundaries the paper explicitly names (sec III A, p. 14 of arXiv preprint):
LET_LOW  = 5.08   # keV/µm
LET_HIGH = 10.8   # keV/µm

# Reference photon (Cs-137) LQ from Guan 2015 Table 1
PHOTON_REF = {
    "H460":  {"alpha_x": 0.290, "beta_x": 0.083},
    "H1437": {"alpha_x": 0.050, "beta_x": 0.041},
}

# -----------------------------------------------------------------------------
def load_guan() -> dict:
    rows = []
    with DATA.open() as fh:
        for r in csv.DictReader(fh):
            rows.append({k: float(v) for k, v in r.items()})
    LET = np.array([r["LET_keV_per_um"] for r in rows])
    return {
        "LET": LET,
        "H460":  {"alpha": np.array([r["H460_alpha"]  for r in rows]),
                  "beta":  np.array([r["H460_beta"]   for r in rows]),
                  "RBE10": np.array([r["H460_RBE10"]  for r in rows])},
        "H1437": {"alpha": np.array([r["H1437_alpha"] for r in rows]),
                  "beta":  np.array([r["H1437_beta"]  for r in rows]),
                  "RBE10": np.array([r["H1437_RBE10"] for r in rows])},
    }


def piecewise_linear_fit(LET: np.ndarray, y: np.ndarray) -> dict:
    """Fit Abolfath's piecewise-linear form: separate (intercept, slope) for low
    (LET ≤ 5.08) and high (LET ≥ 10.8) regimes; intermediate is linearly
    interpolated between the regime endpoints."""
    mask_lo = LET <= LET_LOW
    mask_hi = LET >= LET_HIGH
    # low regime fit
    A_lo = np.vstack([np.ones(mask_lo.sum()), LET[mask_lo]]).T
    p_lo, *_ = np.linalg.lstsq(A_lo, y[mask_lo], rcond=None)
    # high regime fit
    A_hi = np.vstack([np.ones(mask_hi.sum()), LET[mask_hi]]).T
    p_hi, *_ = np.linalg.lstsq(A_hi, y[mask_hi], rcond=None)
    return {
        "low":  {"intercept": float(p_lo[0]), "slope": float(p_lo[1]),
                 "n_points": int(mask_lo.sum())},
        "high": {"intercept": float(p_hi[0]), "slope": float(p_hi[1]),
                 "n_points": int(mask_hi.sum())},
    }


def predict(LET: np.ndarray, fit: dict) -> np.ndarray:
    out = np.zeros_like(LET, dtype=float)
    for i, L in enumerate(LET):
        if L <= LET_LOW:
            out[i] = fit["low"]["intercept"] + fit["low"]["slope"] * L
        elif L >= LET_HIGH:
            out[i] = fit["high"]["intercept"] + fit["high"]["slope"] * L
        else:
            yL = fit["low"]["intercept"]  + fit["low"]["slope"]  * LET_LOW
            yH = fit["high"]["intercept"] + fit["high"]["slope"] * LET_HIGH
            t  = (L - LET_LOW) / (LET_HIGH - LET_LOW)
            out[i] = yL + t * (yH - yL)
    return out


def rbe_from_lq(alpha_p: np.ndarray, beta_p: np.ndarray, alpha_x: float, beta_x: float,
                sf_target: float = 0.10) -> np.ndarray:
    """RBE = D_x / D_p at fixed surviving fraction.
    D = (-α + sqrt(α² - 4β·ln SF)) / (2β)."""
    c = math.log(sf_target)
    Dx = (-alpha_x + math.sqrt(alpha_x**2 - 4 * beta_x * c)) / (2 * beta_x)
    Dp = (-alpha_p + np.sqrt(alpha_p**2 - 4 * beta_p * c)) / (2 * beta_p)
    return Dx / Dp


def rms(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(a) - np.asarray(b))**2)))


def mape(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.abs((np.asarray(a) - np.asarray(b)) / np.asarray(b))) * 100)


# -----------------------------------------------------------------------------
def main() -> int:
    data = load_guan()
    LET  = data["LET"]
    summary = {"regime_boundaries_keV_per_um": [LET_LOW, LET_HIGH], "cell_lines": {}}

    for cell in ("H460", "H1437"):
        alpha  = data[cell]["alpha"]
        beta   = data[cell]["beta"]
        rbe_p  = data[cell]["RBE10"]
        ax     = PHOTON_REF[cell]["alpha_x"]
        bx     = PHOTON_REF[cell]["beta_x"]

        # Eq. 32 strict: piecewise α, β fixed at photon value
        fit_a = piecewise_linear_fit(LET, alpha)
        alpha_pred = predict(LET, fit_a)
        beta_const = np.full_like(beta, bx)
        rbe_eq32   = rbe_from_lq(alpha_pred, beta_const, ax, bx)

        # Eq. 21–22 truncation: β also piecewise linear in LET
        fit_b = piecewise_linear_fit(LET, beta)
        beta_pred = predict(LET, fit_b)
        rbe_full  = rbe_from_lq(alpha_pred, beta_pred, ax, bx)

        # RBE from the *measured* Guan α,β table (sanity check on Cs-137 reference)
        rbe_meas_lq = rbe_from_lq(alpha, beta, ax, bx)

        summary["cell_lines"][cell] = {
            "photon_ref":          {"alpha_x": ax, "beta_x": bx},
            "alpha_fit":           fit_a,
            "beta_fit":            fit_b,
            "alpha_residual_rms":  rms(alpha_pred, alpha),
            "beta_residual_rms":   rms(beta_pred,  beta),
            "alpha_residual_mape_pct": mape(alpha_pred, alpha),
            "beta_residual_mape_pct":  mape(beta_pred,  beta),
            "rbe10_published":           rbe_p.tolist(),
            "rbe10_from_table_lq":       rbe_meas_lq.tolist(),
            "rbe10_eq32_strict":         rbe_eq32.tolist(),
            "rbe10_eq32_with_beta_fit":  rbe_full.tolist(),
            "rbe10_mape_pct_table_vs_published":      mape(rbe_meas_lq, rbe_p),
            "rbe10_mape_pct_eq32_strict_vs_published":   mape(rbe_eq32,  rbe_p),
            "rbe10_mape_pct_eq32_full_vs_published":     mape(rbe_full,  rbe_p),
        }

        # Plots
        Lgrid = np.linspace(LET.min(), LET.max(), 400)
        fig, ax_ = plt.subplots(figsize=(6, 4))
        ax_.plot(LET, alpha, "ko", label="Guan 2015 Table 1")
        ax_.plot(Lgrid, predict(Lgrid, fit_a), "r-", label="Eq. 32 piecewise-linear fit")
        ax_.axvspan(LET_LOW, LET_HIGH, color="gray", alpha=0.15, label="data-poor gap (Abolfath)")
        ax_.set_xlabel(r"LET$_d$ [keV/µm]")
        ax_.set_ylabel(r"$\alpha$ [Gy$^{-1}$]")
        ax_.set_title(f"{cell} — α(LET) Abolfath Eq. 32 fit to Guan 2015")
        ax_.legend(); fig.tight_layout()
        fig.savefig(FIG / f"guan_alpha_fit_{cell}.png", dpi=130); plt.close(fig)

        fig, ax_ = plt.subplots(figsize=(6, 4))
        ax_.plot(LET, beta, "ko", label="Guan 2015 Table 1")
        ax_.plot(Lgrid, predict(Lgrid, fit_b), "r-", label="piecewise-linear fit (Eq. 21–22 trunc)")
        ax_.axhline(bx, ls="--", color="b", label=f"β_x (photon ref) = {bx}")
        ax_.axvspan(LET_LOW, LET_HIGH, color="gray", alpha=0.15)
        ax_.set_xlabel(r"LET$_d$ [keV/µm]")
        ax_.set_ylabel(r"$\beta$ [Gy$^{-2}$]")
        ax_.set_title(f"{cell} — β(LET) — Eq. 32 (β=const) vs full piecewise")
        ax_.legend(); fig.tight_layout()
        fig.savefig(FIG / f"guan_beta_fit_{cell}.png", dpi=130); plt.close(fig)

        fig, ax_ = plt.subplots(figsize=(6, 4))
        ax_.plot(LET, rbe_p,        "ko", label="Guan 2015 published RBE_10%")
        ax_.plot(LET, rbe_eq32,     "rs--", label="Eq. 32 strict (β=β_x)")
        ax_.plot(LET, rbe_full,     "b^-",  label="Eq. 32 + β piecewise")
        ax_.set_xlabel(r"LET$_d$ [keV/µm]")
        ax_.set_ylabel(r"RBE$_{10\%}$")
        ax_.set_title(f"{cell} — RBE_10% Abolfath replication vs Guan data")
        ax_.legend(); fig.tight_layout()
        fig.savefig(FIG / f"guan_rbe_compare_{cell}.png", dpi=130); plt.close(fig)

    OUT.write_text(json.dumps(summary, indent=2))
    print(json.dumps({c: {
        "alpha_mape_pct": summary["cell_lines"][c]["alpha_residual_mape_pct"],
        "beta_mape_pct":  summary["cell_lines"][c]["beta_residual_mape_pct"],
        "rbe_eq32_strict_mape_pct": summary["cell_lines"][c]["rbe10_mape_pct_eq32_strict_vs_published"],
        "rbe_eq32_full_mape_pct":   summary["cell_lines"][c]["rbe10_mape_pct_eq32_full_vs_published"],
        "rbe_table_lq_mape_pct":    summary["cell_lines"][c]["rbe10_mape_pct_table_vs_published"],
    } for c in ("H460", "H1437")}, indent=2))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
