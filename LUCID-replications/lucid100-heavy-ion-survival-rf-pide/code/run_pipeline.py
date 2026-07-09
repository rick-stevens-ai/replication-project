#!/usr/bin/env python3
"""
Replicate Debreceni et al. 2024 (Toxics 12(8):545) pipeline on the
reconstructed NB1RGB heavy-ion dataset.

Models:
  (1) LQM  : S = exp(-(alpha*D + beta*D^2)), fit alpha,beta on train (dose only)
  (2) LocReg: locally weighted regression S ~ dose (LOWESS-style kernel)
  (3) RF   : RandomForestRegressor on [dose, LET]

Validation: Monte Carlo cross-validation, 100 iterations, random train/test
split (~70/30). Report mean R2 and RMSE per model.

Paper targets:
  LQM   R2=0.8843  RMSE=0.0959
  LocReg R2=0.8986 RMSE=0.0921
  RF     R2=0.9685 RMSE=0.0196
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import json

df = pd.read_csv("../data/nb1rgb_reconstructed.csv")
D = df["dose"].values
LET = df["LET"].values
S = df["SF"].values
N = len(df)
print(f"N={N}, experiments={df.exp_id.nunique()}")

def lqm_S(D, a, b):
    return np.exp(-(a * D + b * D * D))

def fit_lqm(Dtr, Str):
    # bound alpha,beta >=0 as in radiobiology
    try:
        p, _ = curve_fit(lqm_S, Dtr, Str, p0=[0.3, 0.03],
                         bounds=([0, 0], [5, 2]), maxfev=10000)
    except Exception:
        p = [0.3, 0.03]
    return p

def locreg_predict(Dtr, Str, Dte, frac=0.3):
    """Locally weighted (tricube kernel) regression, 1D on dose."""
    span = frac * (Dtr.max() - Dtr.min() + 1e-9)
    preds = []
    for x in Dte:
        d = np.abs(Dtr - x)
        # bandwidth = distance to k-th nearest, robust kernel
        h = max(span, np.sort(d)[min(len(d) - 1, max(3, int(frac * len(Dtr))))])
        u = d / (h + 1e-12)
        w = (1 - np.clip(u, 0, 1) ** 3) ** 3
        if w.sum() < 1e-9:
            preds.append(Str[np.argmin(d)]); continue
        # weighted linear fit
        Xw = np.vstack([np.ones_like(Dtr), Dtr]).T
        W = np.diag(w)
        try:
            beta = np.linalg.lstsq(Xw.T @ W @ Xw, Xw.T @ W @ Str, rcond=None)[0]
            preds.append(beta[0] + beta[1] * x)
        except Exception:
            preds.append(np.average(Str, weights=w))
    return np.array(preds)

def rmse(y, yp):
    return float(np.sqrt(mean_squared_error(y, yp)))

ITERS = 100
rng = np.random.default_rng(42)
res = {"LQM": {"r2": [], "rmse": []},
       "LocReg": {"r2": [], "rmse": []},
       "RF": {"r2": [], "rmse": []}}
alphas, betas = [], []

for it in range(ITERS):
    idx = rng.permutation(N)
    ntr = int(0.7 * N)
    tr, te = idx[:ntr], idx[ntr:]

    # ---- LQM (dose only) ----
    a, b = fit_lqm(D[tr], S[tr])
    alphas.append(a); betas.append(b)
    pred = lqm_S(D[te], a, b)
    res["LQM"]["r2"].append(r2_score(S[te], pred))
    res["LQM"]["rmse"].append(rmse(S[te], pred))

    # ---- Local regression (dose only) ----
    predlr = locreg_predict(D[tr], S[tr], D[te], frac=0.3)
    res["LocReg"]["r2"].append(r2_score(S[te], predlr))
    res["LocReg"]["rmse"].append(rmse(S[te], predlr))

    # ---- Random Forest (dose + LET) ----
    rf = RandomForestRegressor(n_estimators=1000, random_state=it,
                               n_jobs=-1, min_samples_leaf=1)
    rf.fit(np.c_[D[tr], LET[tr]], S[tr])
    predrf = rf.predict(np.c_[D[te], LET[te]])
    res["RF"]["r2"].append(r2_score(S[te], predrf))
    res["RF"]["rmse"].append(rmse(S[te], predrf))

summary = {}
for m in res:
    r2 = np.array(res[m]["r2"]); rm = np.array(res[m]["rmse"])
    summary[m] = dict(R2_mean=round(float(r2.mean()), 4),
                      R2_std=round(float(r2.std()), 4),
                      RMSE_mean=round(float(rm.mean()), 4),
                      RMSE_std=round(float(rm.std()), 4))
summary["LQM_params"] = dict(alpha_mean=round(float(np.mean(alphas)), 4),
                             beta_mean=round(float(np.mean(betas)), 4))

paper = {"LQM": {"R2": 0.8843, "RMSE": 0.0959},
         "LocReg": {"R2": 0.8986, "RMSE": 0.0921},
         "RF": {"R2": 0.9685, "RMSE": 0.0196}}

print(json.dumps(summary, indent=2))
print("\nPAPER TARGETS:", json.dumps(paper))
out = {"reproduced": summary, "paper_targets": paper, "N": N,
       "iters": ITERS, "note": "reconstructed NB1RGB dataset (PIDE email-gated)"}
json.dump(out, open("../results/pipeline_results.json", "w"), indent=2)
print("\nwrote ../results/pipeline_results.json")
