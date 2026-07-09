#!/usr/bin/env python3
"""
Follow-up UQ analysis: does ensemble-std need recalibration?
And does the RF per-tree UQ (larger K = 300) work better than GBR-20?

Reads the saved arrays from ensemble_replication.py.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path
from statistics import mean

import numpy as np
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"

# 1. Load saved arrays
data = np.load(EVID / "ensemble_predictions.npz")
y_te = data["y_test"]
gbr = data["gbr_preds_20"]      # (20, n_test)
rf20 = data["rf_preds_20"]      # (20, n_test)
mu = data["ensemble_mean_gbr20"]
sigma = data["ensemble_std_gbr20"]
resid = y_te - mu
abs_resid = np.abs(resid)
n = len(y_te)

# --------------------------------------------------------------- #
# 2. Sharpness/calibration scaling — is the σ shape right, just scaled wrong?
# Optimal scalar τ that maximises Gaussian log-lik:  τ² = mean(resid² / σ²)
# --------------------------------------------------------------- #
tau2 = float(np.mean(resid**2 / (sigma**2 + 1e-8)))
tau = float(np.sqrt(tau2))
sigma_calib = tau * sigma
cov1_calib = float((abs_resid <= sigma_calib).mean())
cov2_calib = float((abs_resid <= 2 * sigma_calib).mean())
print(f"[GBR-20 uncalibrated] cov@±1σ={((abs_resid<=sigma).mean()):.3f}  "
      f"cov@±2σ={((abs_resid<=2*sigma).mean()):.3f}")
print(f"Optimal Gaussian scale τ = {tau:.3f}  (σ_pred underestimates by ~{tau:.1f}×)")
print(f"[GBR-20 τ-recalibrated] cov@±1σ={cov1_calib:.3f}  cov@±2σ={cov2_calib:.3f}")

# Gaussian NLL after recalibration
eps = 1e-8
nll_uncal = float(0.5 * np.mean(np.log(2*np.pi*(sigma**2+eps)) + resid**2/(sigma**2+eps)))
nll_calib = float(0.5 * np.mean(np.log(2*np.pi*(sigma_calib**2+eps)) + resid**2/(sigma_calib**2+eps)))
print(f"NLL uncalibrated = {nll_uncal:.3f}   recalibrated = {nll_calib:.3f}")

# --------------------------------------------------------------- #
# 3. RF per-tree UQ (much larger effective ensemble K = 300 trees)
# --------------------------------------------------------------- #
# Refit one RF and extract per-tree predictions on the held-out test set
# so we get an intra-model per-instance variance estimate.
from matminer.datasets import load_dataset

df = load_dataset("expt_gap")
df = df[df["gap expt"] > 0].drop_duplicates(subset=["formula"]).reset_index(drop=True)

# Recreate features (import from sibling script)
import importlib.util
spec = importlib.util.spec_from_file_location("er", HERE / "ensemble_replication.py")
er = importlib.util.module_from_spec(spec)
# guard against the module running its main-block CV on import — it uses no
# __main__ guard, so we monkey-patch load_dataset to return an empty frame
# to short-circuit. Cleaner approach: just re-featurize inline here.
import re

FORMULA_RE = re.compile(r"([A-Z][a-z]?)(\d*\.?\d*)")
def parse_formula(f, ELEM):
    parts = FORMULA_RE.findall(f)
    out = {}
    for el, amt in parts:
        if not el or el not in ELEM: continue
        v = float(amt) if amt else 1.0
        out[el] = out.get(el, 0.0) + v
    return out

# grab ELEM by executing the ensemble_replication.py file namespace lazily.
# Instead of running its side-effects, just re-declare the small table? Faster
# to import the ELEM constant. We'll parse the source for the ELEM dict.
src = (HERE / "ensemble_replication.py").read_text()
import ast
tree = ast.parse(src)
ELEM = None
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
            and node.targets[0].id == "ELEM":
        ELEM = ast.literal_eval(node.value)
        break
assert ELEM is not None, "Could not extract ELEM"
print(f"Extracted ELEM table with {len(ELEM)} elements")

def compose_features(formula, ELEM):
    comp = parse_formula(formula, ELEM)
    if not comp: return None
    tot = sum(comp.values())
    if tot <= 0: return None
    weights = np.array([comp[el] / tot for el in comp])
    props = np.array([ELEM[el] for el in comp])
    wmean = (weights[:, None] * props).sum(axis=0)
    wvar = (weights[:, None] * (props - wmean) ** 2).sum(axis=0)
    wstd = np.sqrt(np.maximum(wvar, 0.0))
    pmin = props.min(axis=0)
    pmax = props.max(axis=0)
    prng = pmax - pmin
    n_elem = np.array([len(comp)])
    total_atoms = np.array([tot])
    return np.concatenate([wmean, wstd, pmin, pmax, prng, n_elem, total_atoms])

rows, keep = [], np.zeros(len(df), dtype=bool)
for i, f in enumerate(df["formula"]):
    v = compose_features(f, ELEM)
    if v is not None and np.all(np.isfinite(v)):
        rows.append(v); keep[i] = True
X = np.asarray(rows, dtype=float)
y = df.loc[keep, "gap expt"].to_numpy()

X_tr, X_te2, y_tr, y_te2 = train_test_split(X, y, test_size=0.2, random_state=0)
assert np.allclose(y_te2, y_te), "Test split mismatch — cannot compare"

print(f"\n[RF-300 per-tree UQ]")
rf = RandomForestRegressor(n_estimators=300, max_depth=None, min_samples_leaf=2,
                           max_features="sqrt", n_jobs=-1, random_state=0,
                           bootstrap=True)
rf.fit(X_tr, y_tr)
# Per-tree preds
per_tree = np.array([t.predict(X_te2) for t in rf.estimators_])   # (300, n_test)
mu_rf = per_tree.mean(axis=0)
sig_rf = per_tree.std(axis=0, ddof=1)
resid_rf = y_te2 - mu_rf

rho_rf, _ = spearmanr(sig_rf, np.abs(resid_rf))
mae_rf = mean_absolute_error(y_te2, mu_rf)
rmse_rf = float(np.sqrt(mean_squared_error(y_te2, mu_rf)))
r2_rf = r2_score(y_te2, mu_rf)
cov1_rf = float((np.abs(resid_rf) <= sig_rf).mean())
cov2_rf = float((np.abs(resid_rf) <= 2*sig_rf).mean())
print(f"  MAE={mae_rf:.4f}  RMSE={rmse_rf:.4f}  R²={r2_rf:.4f}")
print(f"  Spearman ρ(σ_tree, |resid|) = {rho_rf:.4f}")
print(f"  cov@±1σ = {cov1_rf:.3f} (nominal 0.683)")
print(f"  cov@±2σ = {cov2_rf:.3f} (nominal 0.954)")

tau_rf = float(np.sqrt(np.mean(resid_rf**2 / (sig_rf**2 + 1e-8))))
sig_rf_c = tau_rf * sig_rf
cov1_rf_c = float((np.abs(resid_rf) <= sig_rf_c).mean())
cov2_rf_c = float((np.abs(resid_rf) <= 2*sig_rf_c).mean())
print(f"  Optimal τ = {tau_rf:.3f}")
print(f"  cov@±1σ after τ-recal = {cov1_rf_c:.3f}")
print(f"  cov@±2σ after τ-recal = {cov2_rf_c:.3f}")

# --------------------------------------------------------------- #
# 4. Sample-selective-prediction curve: sort by predicted σ, drop most
#     uncertain, plot MAE-vs-coverage. If UQ is informative, curve
#     should monotonically decrease (well-calibrated in RANK sense).
# --------------------------------------------------------------- #
print("\n[Selective-prediction curve — GBR-20]")
order_gbr = np.argsort(sigma)     # ascending: most-certain first
fracs = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
sel_gbr = []
for frac in fracs:
    k = int(frac * n)
    idx = order_gbr[:k]
    mae_k = mean_absolute_error(y_te[idx], mu[idx])
    sel_gbr.append({"frac": frac, "n": k, "mae": float(mae_k)})
    print(f"  keep {frac*100:>5.0f}%  n={k:>3}  MAE={mae_k:.4f}")

print("\n[Selective-prediction curve — RF-300]")
order_rf = np.argsort(sig_rf)
sel_rf = []
for frac in fracs:
    k = int(frac * n)
    idx = order_rf[:k]
    mae_k = mean_absolute_error(y_te2[idx], mu_rf[idx])
    sel_rf.append({"frac": frac, "n": k, "mae": float(mae_k)})
    print(f"  keep {frac*100:>5.0f}%  n={k:>3}  MAE={mae_k:.4f}")

# Random-baseline selective curve: average over 20 random draws
rng = np.random.RandomState(42)
rand_curve = []
for frac in fracs:
    k = int(frac * n)
    mses = []
    for _ in range(20):
        idx = rng.choice(n, size=k, replace=False)
        mses.append(mean_absolute_error(y_te[idx], mu[idx]))
    rand_curve.append({"frac": frac, "n": k, "mae_mean": float(np.mean(mses)),
                       "mae_std": float(np.std(mses))})
print("\n[Random selection baseline — for reference]")
for r in rand_curve:
    print(f"  keep {r['frac']*100:>5.0f}%  MAE={r['mae_mean']:.4f}±{r['mae_std']:.4f}")

# --------------------------------------------------------------- #
# 5. Persist
# --------------------------------------------------------------- #
out = {
    "gbr20_recalibration": {
        "tau_optimal": tau,
        "cov1_uncal": float((abs_resid<=sigma).mean()),
        "cov2_uncal": float((abs_resid<=2*sigma).mean()),
        "cov1_recal": cov1_calib,
        "cov2_recal": cov2_calib,
        "nll_uncal": nll_uncal,
        "nll_recal": nll_calib,
    },
    "rf300_per_tree_uq": {
        "mae": float(mae_rf), "rmse": rmse_rf, "r2": float(r2_rf),
        "spearman_rho": float(rho_rf),
        "cov1_uncal": cov1_rf, "cov2_uncal": cov2_rf,
        "tau_optimal": tau_rf,
        "cov1_recal": cov1_rf_c, "cov2_recal": cov2_rf_c,
    },
    "selective_prediction_gbr20": sel_gbr,
    "selective_prediction_rf300": sel_rf,
    "selective_prediction_random_baseline_gbr": rand_curve,
}
(EVID / "uq_recalibration_results.json").write_text(json.dumps(out, indent=2, default=float))
print(f"\nWrote {EVID / 'uq_recalibration_results.json'}")
print("DONE")
