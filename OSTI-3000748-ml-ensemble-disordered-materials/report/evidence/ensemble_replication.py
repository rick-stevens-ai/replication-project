#!/usr/bin/env python3
"""
Independent ML-ensemble + UQ-calibration replication for OSTI-3000748
(Fang, Hsu, Yan 2025 — "A Machine Learning Framework for Modeling Ensemble
Properties of Atomically Disordered Materials").

This script does NOT try to reproduce the paper's Ti3C2O2-xFx DFT numbers
(underlying dataset is not distributed; see report/REPORT.md § 3a). Instead
it tests the two GENERALIZABLE methodological claims the paper depends on:

  M1. An ensemble of ML regressors reduces error relative to a single
      randomly-seeded member on real materials-property data.
  M2. The between-member spread of an ensemble provides a *calibrated*
      uncertainty estimate (i.e. predicted-uncertainty ranks and scales
      with the actual absolute residual).

Both claims are tested on the *matminer* `expt_gap` dataset — 6,354 real
experimental band gaps of inorganic semiconductors from Zhuo et al.
(open-access, shipped with matminer via Figshare). Features are hand-
computed composition-only statistics over Mendeleev atomic properties
(no pymatgen/spglib dependency).

Real numbers. Written for this replication on 2026-07-04.
"""
from __future__ import annotations

import json
import re
import sys
import time
import warnings
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import pandas as pd
from matminer.datasets import load_dataset
from scipy.stats import spearmanr, pearsonr
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, train_test_split

warnings.filterwarnings("ignore")

OUT_DIR = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------- #
# 1. Element property table (subset from Mendeleev / IUPAC / CRC).
#    Hard-coded so we don't need the `mendeleev` or `pymatgen` deps.
# --------------------------------------------------------------------- #
# columns: Z, atomic_mass, group, period, pauling_en, atomic_radius_pm,
# valence_electrons, electron_affinity_kJmol
ELEM = {
 "H":(1,1.008,1,1,2.20,25,1,72.8),"He":(2,4.0026,18,1,0.0,120,2,0),
 "Li":(3,6.94,1,2,0.98,145,1,59.6),"Be":(4,9.0122,2,2,1.57,105,2,0),
 "B":(5,10.81,13,2,2.04,85,3,26.7),"C":(6,12.011,14,2,2.55,70,4,153.9),
 "N":(7,14.007,15,2,3.04,65,5,7.0),"O":(8,15.999,16,2,3.44,60,6,141.0),
 "F":(9,18.998,17,2,3.98,50,7,328.0),"Ne":(10,20.180,18,2,0.0,160,8,0),
 "Na":(11,22.990,1,3,0.93,180,1,52.8),"Mg":(12,24.305,2,3,1.31,150,2,0),
 "Al":(13,26.982,13,3,1.61,125,3,42.5),"Si":(14,28.085,14,3,1.90,110,4,133.6),
 "P":(15,30.974,15,3,2.19,100,5,72.0),"S":(16,32.06,16,3,2.58,100,6,200.4),
 "Cl":(17,35.45,17,3,3.16,100,7,349.0),"Ar":(18,39.948,18,3,0.0,71,8,0),
 "K":(19,39.098,1,4,0.82,220,1,48.4),"Ca":(20,40.078,2,4,1.00,180,2,2.37),
 "Sc":(21,44.956,3,4,1.36,160,3,18.1),"Ti":(22,47.867,4,4,1.54,140,4,7.6),
 "V":(23,50.942,5,4,1.63,135,5,50.6),"Cr":(24,51.996,6,4,1.66,140,6,64.3),
 "Mn":(25,54.938,7,4,1.55,140,7,0),"Fe":(26,55.845,8,4,1.83,140,8,15.7),
 "Co":(27,58.933,9,4,1.88,135,9,63.7),"Ni":(28,58.693,10,4,1.91,135,10,112.0),
 "Cu":(29,63.546,11,4,1.90,135,11,118.4),"Zn":(30,65.38,12,4,1.65,135,12,0),
 "Ga":(31,69.723,13,4,1.81,130,3,28.9),"Ge":(32,72.63,14,4,2.01,125,4,119.0),
 "As":(33,74.922,15,4,2.18,115,5,78.0),"Se":(34,78.971,16,4,2.55,115,6,195.0),
 "Br":(35,79.904,17,4,2.96,115,7,324.6),"Kr":(36,83.798,18,4,3.00,88,8,0),
 "Rb":(37,85.468,1,5,0.82,235,1,46.9),"Sr":(38,87.62,2,5,0.95,200,2,5.03),
 "Y":(39,88.906,3,5,1.22,180,3,29.6),"Zr":(40,91.224,4,5,1.33,155,4,41.1),
 "Nb":(41,92.906,5,5,1.6,145,5,86.1),"Mo":(42,95.95,6,5,2.16,145,6,71.9),
 "Tc":(43,98.0,7,5,1.9,135,7,53.0),"Ru":(44,101.07,8,5,2.2,130,8,101.3),
 "Rh":(45,102.91,9,5,2.28,135,9,110.3),"Pd":(46,106.42,10,5,2.20,140,10,54.2),
 "Ag":(47,107.87,11,5,1.93,160,11,125.6),"Cd":(48,112.41,12,5,1.69,155,12,0),
 "In":(49,114.82,13,5,1.78,155,3,28.9),"Sn":(50,118.71,14,5,1.96,145,4,107.3),
 "Sb":(51,121.76,15,5,2.05,145,5,101.1),"Te":(52,127.60,16,5,2.10,140,6,190.2),
 "I":(53,126.90,17,5,2.66,140,7,295.2),"Xe":(54,131.29,18,5,2.60,108,8,0),
 "Cs":(55,132.91,1,6,0.79,260,1,45.5),"Ba":(56,137.33,2,6,0.89,215,2,13.95),
 "La":(57,138.91,3,6,1.10,195,3,45.0),"Ce":(58,140.12,3,6,1.12,185,3,55.0),
 "Pr":(59,140.91,3,6,1.13,185,3,93.0),"Nd":(60,144.24,3,6,1.14,185,3,184.87),
 "Pm":(61,145.0,3,6,1.13,185,3,12.45),"Sm":(62,150.36,3,6,1.17,185,3,15.63),
 "Eu":(63,151.96,3,6,1.2,185,3,11.2),"Gd":(64,157.25,3,6,1.20,180,3,13.22),
 "Tb":(65,158.93,3,6,1.10,175,3,112.4),"Dy":(66,162.50,3,6,1.22,175,3,33.96),
 "Ho":(67,164.93,3,6,1.23,175,3,32.61),"Er":(68,167.26,3,6,1.24,175,3,30.10),
 "Tm":(69,168.93,3,6,1.25,175,3,99.30),"Yb":(70,173.05,3,6,1.10,175,3,-1.93),
 "Lu":(71,174.97,3,6,1.27,175,3,32.83),"Hf":(72,178.49,4,6,1.30,155,4,0.0),
 "Ta":(73,180.95,5,6,1.5,145,5,31.0),"W":(74,183.84,6,6,2.36,135,6,78.6),
 "Re":(75,186.21,7,6,1.9,135,7,14.5),"Os":(76,190.23,8,6,2.2,130,8,106.1),
 "Ir":(77,192.22,9,6,2.20,135,9,151.0),"Pt":(78,195.08,10,6,2.28,135,10,205.3),
 "Au":(79,196.97,11,6,2.54,135,11,222.8),"Hg":(80,200.59,12,6,2.00,150,12,0),
 "Tl":(81,204.38,13,6,1.62,190,3,19.2),"Pb":(82,207.2,14,6,2.33,180,4,35.1),
 "Bi":(83,208.98,15,6,2.02,160,5,90.9),"Po":(84,209.0,16,6,2.0,190,6,183.3),
 "At":(85,210.0,17,6,2.2,50,7,270.1),"Rn":(86,222.0,18,6,0.0,120,8,0),
 "Fr":(87,223.0,1,7,0.7,260,1,44.0),"Ra":(88,226.0,2,7,0.9,215,2,10.0),
 "Ac":(89,227.0,3,7,1.1,195,3,33.77),"Th":(90,232.04,3,7,1.3,180,3,50.0),
 "Pa":(91,231.04,3,7,1.5,180,3,0.0),"U":(92,238.03,3,7,1.38,175,3,50.94),
 "Np":(93,237.0,3,7,1.36,175,3,45.85),"Pu":(94,244.0,3,7,1.28,175,3,-48.33),
}

FORMULA_RE = re.compile(r"([A-Z][a-z]?)(\d*\.?\d*)")

def parse_formula(f: str) -> dict[str, float]:
    """Parse a simple formula (no parens). Returns element→amount dict."""
    parts = FORMULA_RE.findall(f)
    out: dict[str, float] = {}
    for el, amt in parts:
        if not el or el not in ELEM:
            continue
        v = float(amt) if amt else 1.0
        out[el] = out.get(el, 0.0) + v
    return out

PROP_NAMES = ("Z","mass","group","period","EN","radius","valence","EA")

def compose_features(formula: str) -> np.ndarray | None:
    comp = parse_formula(formula)
    if not comp:
        return None
    tot = sum(comp.values())
    if tot <= 0:
        return None
    # weighted per-element property vectors
    weights = np.array([comp[el] / tot for el in comp])
    props = np.array([ELEM[el] for el in comp])  # (n_el, 8)
    # weighted mean, weighted std, min, max, range, mode-weight (max weight)
    wmean = (weights[:, None] * props).sum(axis=0)
    wvar = (weights[:, None] * (props - wmean) ** 2).sum(axis=0)
    wstd = np.sqrt(np.maximum(wvar, 0.0))
    pmin = props.min(axis=0)
    pmax = props.max(axis=0)
    prng = pmax - pmin
    n_elem = np.array([len(comp)])
    total_atoms = np.array([tot])
    feats = np.concatenate([wmean, wstd, pmin, pmax, prng, n_elem, total_atoms])
    return feats

def featurize(formulas: list[str]) -> tuple[np.ndarray, np.ndarray]:
    rows = []
    keep = np.zeros(len(formulas), dtype=bool)
    for i, f in enumerate(formulas):
        v = compose_features(f)
        if v is None or not np.all(np.isfinite(v)):
            continue
        rows.append(v)
        keep[i] = True
    return np.asarray(rows, dtype=float), keep

# --------------------------------------------------------------------- #
# 2. Load real data
# --------------------------------------------------------------------- #
print("Loading matminer expt_gap dataset (6,354 experimental band gaps)…")
t0 = time.time()
df = load_dataset("expt_gap")
print(f"  loaded shape={df.shape} in {time.time()-t0:.1f}s")

# Drop metals (gap == 0), duplicate compositions, and any parse failures.
df = df[df["gap expt"] > 0].reset_index(drop=True)
df = df.drop_duplicates(subset=["formula"]).reset_index(drop=True)

X, keep = featurize(df["formula"].tolist())
y = df.loc[keep, "gap expt"].to_numpy()
formulas = df.loc[keep, "formula"].tolist()
print(f"  after clean+featurize: {X.shape[0]} rows, {X.shape[1]} features")

# --------------------------------------------------------------------- #
# 3. Single-model baseline vs deep ensemble (train/test split)
# --------------------------------------------------------------------- #
rng = np.random.RandomState(0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
print(f"\nSplit: train={len(y_tr)}, test={len(y_te)}")

def train_gbr(seed: int) -> GradientBoostingRegressor:
    m = GradientBoostingRegressor(
        n_estimators=400, max_depth=5, learning_rate=0.05,
        subsample=0.8, random_state=seed,
    )
    m.fit(X_tr, y_tr)
    return m

def train_rf(seed: int) -> RandomForestRegressor:
    m = RandomForestRegressor(
        n_estimators=300, max_depth=None, min_samples_leaf=2,
        max_features="sqrt", n_jobs=-1, random_state=seed,
        bootstrap=True,
    )
    m.fit(X_tr, y_tr)
    return m

def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = r2_score(y_true, y_pred)
    print(f"  {name}: MAE={mae:.4f}  RMSE={rmse:.4f}  R²={r2:.4f}")
    return {"mae": mae, "rmse": rmse, "r2": r2}

print("\n[M1] Ensemble size sweep — does ensemble mean reduce error?\n")
ensemble_sizes = [1, 2, 3, 5, 10, 20]
gbr_preds_all: list[np.ndarray] = []
for seed in range(20):
    t = time.time()
    m = train_gbr(seed)
    gbr_preds_all.append(m.predict(X_te))
    print(f"  GBR seed={seed:>2} trained in {time.time()-t:.1f}s")
gbr_preds_all_np = np.asarray(gbr_preds_all)  # (20, n_test)

sweep = []
for k in ensemble_sizes:
    # Average k members from seeds 0..k-1 (deterministic prefix)
    p_mean = gbr_preds_all_np[:k].mean(axis=0)
    m = evaluate(y_te, p_mean, f"GBR ensemble k={k:>2}")
    m["k"] = k
    sweep.append(m)

# Random-forest cross-check
print("\n  Random-Forest ensemble sweep (independent model family):")
rf_preds_all = []
for seed in range(20):
    t = time.time()
    m = train_rf(seed)
    rf_preds_all.append(m.predict(X_te))
    print(f"  RF  seed={seed:>2} trained in {time.time()-t:.1f}s")
rf_preds_all_np = np.asarray(rf_preds_all)

sweep_rf = []
for k in ensemble_sizes:
    p_mean = rf_preds_all_np[:k].mean(axis=0)
    m = evaluate(y_te, p_mean, f"RF  ensemble k={k:>2}")
    m["k"] = k
    sweep_rf.append(m)

# --------------------------------------------------------------------- #
# 4. UQ CALIBRATION — the paper's other core methodological claim
# --------------------------------------------------------------------- #
print("\n[M2] Deep-ensemble UQ calibration on GBR (k=20)")

K = 20
mu = gbr_preds_all_np.mean(axis=0)          # ensemble mean prediction
sigma = gbr_preds_all_np.std(axis=0, ddof=1)  # ensemble stdev (predicted UQ)
resid = y_te - mu
abs_resid = np.abs(resid)

# 4a. Rank correlation of predicted std with actual abs error
rho, rho_p = spearmanr(sigma, abs_resid)
r, r_p = pearsonr(sigma, abs_resid)
print(f"  Spearman ρ(σ_pred, |resid|) = {rho:.4f}  (p={rho_p:.2e})")
print(f"  Pearson  r(σ_pred, |resid|) = {r:.4f}  (p={r_p:.2e})")

# 4b. Reliability curve — bin by predicted std, check observed std matches
n_bins = 10
order = np.argsort(sigma)
bin_edges = np.linspace(0, len(sigma), n_bins + 1).astype(int)
reliability = []
for i in range(n_bins):
    idx = order[bin_edges[i]:bin_edges[i+1]]
    if len(idx) < 2:
        continue
    pred_sigma = float(sigma[idx].mean())
    obs_sigma = float(np.sqrt((resid[idx] ** 2).mean()))  # RMSE within bin
    reliability.append({
        "bin": i,
        "n": int(len(idx)),
        "pred_sigma_mean": pred_sigma,
        "obs_sigma_rmse": obs_sigma,
    })
print("\n  Reliability curve (bin predicted σ → observed RMSE):")
print(f"    {'bin':>3} {'n':>4} {'pred_σ':>8} {'obs_σ':>8}")
for r_ in reliability:
    print(f"    {r_['bin']:>3d} {r_['n']:>4d} {r_['pred_sigma_mean']:>8.4f} {r_['obs_sigma_rmse']:>8.4f}")

# Miscalibration area (mean |pred - obs| across bins, normalized)
pred_arr = np.array([r["pred_sigma_mean"] for r in reliability])
obs_arr = np.array([r["obs_sigma_rmse"] for r in reliability])
miscal_area = float(np.mean(np.abs(pred_arr - obs_arr)))
print(f"  Miscalibration area (bin-avg |pred-obs|) = {miscal_area:.4f}")

# 4c. Sharpness = mean predicted sigma
sharpness = float(sigma.mean())
print(f"  Sharpness (mean predicted σ) = {sharpness:.4f}")

# 4d. Gaussian negative-log-likelihood
eps = 1e-6
nll_gauss = float(0.5 * np.mean(np.log(2 * np.pi * (sigma ** 2 + eps)) +
                                resid ** 2 / (sigma ** 2 + eps)))
print(f"  Mean Gaussian NLL (assuming σ_pred = σ_true) = {nll_gauss:.4f}")

# 4e. Coverage at ±1σ, ±2σ
cov1 = float((abs_resid <= sigma).mean())
cov2 = float((abs_resid <= 2 * sigma).mean())
print(f"  Empirical coverage at ±1σ = {cov1:.3f} (nominal 0.683)")
print(f"  Empirical coverage at ±2σ = {cov2:.3f} (nominal 0.954)")

# --------------------------------------------------------------------- #
# 5. Cross-validated single-vs-ensemble for a robust headline number
# --------------------------------------------------------------------- #
print("\n[CV] 5-fold CV: single-GBR (seed=0) vs 5-member GBR ensemble")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_single_mae, cv_ens_mae = [], []
cv_single_r2, cv_ens_r2 = [], []
cv_spearman = []
for fi, (tr, te) in enumerate(kf.split(X)):
    Xtr_, Xte_ = X[tr], X[te]
    ytr_, yte_ = y[tr], y[te]
    preds_k = []
    for s in range(5):
        m = GradientBoostingRegressor(
            n_estimators=400, max_depth=5, learning_rate=0.05,
            subsample=0.8, random_state=s,
        )
        m.fit(Xtr_, ytr_)
        preds_k.append(m.predict(Xte_))
    preds_k = np.asarray(preds_k)
    single = preds_k[0]
    ens_mean = preds_k.mean(axis=0)
    ens_std = preds_k.std(axis=0, ddof=1)
    cv_single_mae.append(mean_absolute_error(yte_, single))
    cv_ens_mae.append(mean_absolute_error(yte_, ens_mean))
    cv_single_r2.append(r2_score(yte_, single))
    cv_ens_r2.append(r2_score(yte_, ens_mean))
    rho_i, _ = spearmanr(ens_std, np.abs(yte_ - ens_mean))
    cv_spearman.append(float(rho_i))
    print(f"  fold {fi+1}: single MAE={cv_single_mae[-1]:.4f}  ens MAE={cv_ens_mae[-1]:.4f}  "
          f"ΔMAE={cv_single_mae[-1]-cv_ens_mae[-1]:+.4f}  ρ={rho_i:.3f}")

print(f"\n  CV single-model MAE = {mean(cv_single_mae):.4f} ± {stdev(cv_single_mae):.4f}")
print(f"  CV 5-ens     MAE   = {mean(cv_ens_mae):.4f} ± {stdev(cv_ens_mae):.4f}")
print(f"  CV single-model R²  = {mean(cv_single_r2):.4f}")
print(f"  CV 5-ens     R²    = {mean(cv_ens_r2):.4f}")
print(f"  CV Spearman ρ(σ,|e|) mean = {mean(cv_spearman):.4f}")

# --------------------------------------------------------------------- #
# 6. Persist everything
# --------------------------------------------------------------------- #
out = {
    "dataset": "matminer.expt_gap",
    "n_rows_used": int(X.shape[0]),
    "n_features": int(X.shape[1]),
    "test_size": int(len(y_te)),
    "ensemble_sweep_gbr": sweep,
    "ensemble_sweep_rf": sweep_rf,
    "uq_calibration_gbr_k20": {
        "spearman_rho_sigma_vs_absresid": float(rho),
        "pearson_r_sigma_vs_absresid": float(r),
        "reliability_curve": reliability,
        "miscalibration_area": miscal_area,
        "sharpness_mean_sigma": sharpness,
        "gaussian_nll": nll_gauss,
        "coverage_1sigma": cov1,
        "coverage_2sigma": cov2,
    },
    "cv_5fold_gbr": {
        "single_mae_mean": mean(cv_single_mae),
        "single_mae_std": stdev(cv_single_mae),
        "ensemble5_mae_mean": mean(cv_ens_mae),
        "ensemble5_mae_std": stdev(cv_ens_mae),
        "single_r2_mean": mean(cv_single_r2),
        "ensemble5_r2_mean": mean(cv_ens_r2),
        "spearman_rho_mean": mean(cv_spearman),
        "delta_mae_pct": 100.0 * (mean(cv_single_mae) - mean(cv_ens_mae)) / mean(cv_single_mae),
    },
    "python": sys.version,
    "sklearn": __import__("sklearn").__version__,
    "numpy": np.__version__,
    "scipy": __import__("scipy").__version__,
}

out_path = OUT_DIR / "ensemble_replication_results.json"
out_path.write_text(json.dumps(out, indent=2, default=float))
print(f"\nWrote {out_path}")

# Also save the raw arrays for figure-making later
np.savez(
    OUT_DIR / "ensemble_predictions.npz",
    y_test=y_te,
    gbr_preds_20=gbr_preds_all_np,
    rf_preds_20=rf_preds_all_np,
    ensemble_mean_gbr20=mu,
    ensemble_std_gbr20=sigma,
)
print(f"Wrote {OUT_DIR / 'ensemble_predictions.npz'}")
print("\nDONE")
