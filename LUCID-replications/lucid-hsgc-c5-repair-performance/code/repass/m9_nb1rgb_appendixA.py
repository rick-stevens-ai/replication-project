"""M9+M10: Reproduce Appendix A (NB1RGB) — Figure A1 and Table A1.

Paper claims (Appendix A):
  - Same TLK setup applied to NB1RGB human fibroblasts.
  - TLK *can* be optimized to fit NB1RGB SF (Fig A1 left).
  - TLK *cannot* adequately fit NB1RGB DNA-rejoining (FAR) kinetics (Fig A1 right).
    "The TLK model could not adequately describe the DNA-rejoining kinetics of NB1RGB."
  - Table A1 optimized parameters:
      lam1 = 33062.9 h^-1   (~1000x HSGc-C5 lam1=3.36; "unsubstantial")
      lam2 = 1.26e-2 h^-1
      eta  = 7.51e-6 h^-1
      beta1= 0
      beta2= 1.93e-2
      gamma= 0.19

We:
  1. Load NB1 rows from supplement SF.csv and FAR.csv.
  2. Use the SAME DSB-yield reconstruction approach as for HSGc-C5 (the paper
     uses the same initial DSB simulation, so Sigma1/Sigma2 are identical to
     the HSGc-C5 values — what differs is the *repair* parameters per cell line).
  3. Joint nonlinear least squares refit (same approach as code/refit.py for HSG)
     to compare with Table A1.
  4. Forward run with paper Table A1 verbatim to check Fig A1 reproduction.
  5. Compute fit metrics and explicitly report the FAR-misfit claim.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "code"))

from tlk_model import (  # noqa: E402
    SIGMA1_0MM, SIGMA1_32MM, SIGMA2_0MM, SIGMA2_32MM,
    far_curve, sf_at_dose,
)

# Table A1 (paper, NB1RGB)
NB1_TABLE_A1 = dict(
    lam1=33062.9,
    lam2=1.26e-2,
    eta=7.51e-6,
    beta1=0.0,
    beta2=1.93e-2,
    gamma=0.19,
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_sf_nb1(path: Path):
    rows = []
    with path.open() as f:
        for row in csv.reader(f):
            if not row or row[0].strip() == "Cell":
                continue
            cell = row[0].strip()
            if cell != "NB1":
                continue
            pmma = int(row[1])
            dose = float(row[2])
            sf = float(row[3])
            std = float(row[4]) if row[4].strip() else 0.0
            rows.append((pmma, dose, sf, std))
    return rows  # list of (pmma_mm, dose_Gy, sf, std)


def load_far_nb1(path: Path):
    rows = []
    with path.open() as f:
        for row in csv.reader(f):
            if not row or row[0].strip() == "Cell":
                continue
            cell = row[0].strip()
            if cell != "NB1":
                continue
            pmma = int(row[1])
            dose = float(row[2])
            t = float(row[3])
            far = float(row[4])
            rows.append((pmma, dose, t, far))
    return rows


SF_NB1 = load_sf_nb1(ROOT / "data" / "supplement" / "SF.csv")
FAR_NB1 = load_far_nb1(ROOT / "data" / "supplement" / "FAR.csv")
print(f"Loaded NB1: n_sf={len(SF_NB1)}, n_far={len(FAR_NB1)}")


def sigmas_for(pmma_mm: int) -> tuple[float, float]:
    if pmma_mm == 0:
        return SIGMA1_0MM, SIGMA2_0MM
    if pmma_mm == 32:
        return SIGMA1_32MM, SIGMA2_32MM
    raise ValueError(pmma_mm)


# ---------------------------------------------------------------------------
# Forward predictions with Paper Table A1
# ---------------------------------------------------------------------------
def predict_sf(params: dict) -> list[tuple]:
    out = []
    for pmma, dose, sf_obs, std in SF_NB1:
        s1, s2 = sigmas_for(pmma)
        if dose == 0.0:
            sf_pred = 1.0
        else:
            sf_pred = sf_at_dose(dose, params, s1, s2)
        out.append((pmma, dose, sf_obs, sf_pred, std))
    return out


def predict_far(params: dict) -> list[tuple]:
    # NB1 FAR rows: PMMA 0 mm, 200 Gy, multiple times
    times = np.array([t for (pmma, _d, t, _f) in FAR_NB1 if pmma == 0])
    far_obs = np.array([f for (pmma, _d, _t, f) in FAR_NB1 if pmma == 0])
    if len(times) == 0:
        return [], np.array([]), np.array([])
    # Use 200 Gy dose for FAR
    s1, s2 = sigmas_for(0)
    far_pred = far_curve(200.0, params, s1, s2, times)
    rows = []
    for t, fo, fp in zip(times, far_obs, far_pred):
        rows.append((0, 200.0, float(t), float(fo), float(fp)))
    return rows, times, far_pred


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def rmse(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def r2(obs, pred):
    obs = np.asarray(obs, float); pred = np.asarray(pred, float)
    ss_res = np.sum((obs - pred) ** 2)
    ss_tot = np.sum((obs - obs.mean()) ** 2)
    if ss_tot <= 0:
        return float("nan")
    return float(1.0 - ss_res / ss_tot)


def sf_metrics(rows):
    obs = [r[2] for r in rows]
    pred = [r[3] for r in rows]
    # log10 RMSE for SF
    log_obs = np.log10(np.clip(obs, 1e-12, None))
    log_pred = np.log10(np.clip(pred, 1e-12, None))
    return {
        "n": len(rows),
        "rmse": rmse(obs, pred),
        "log10_rmse": rmse(log_obs, log_pred),
        "r2": r2(obs, pred),
    }


def far_metrics(rows):
    obs = [r[3] for r in rows]
    pred = [r[4] for r in rows]
    return {
        "n": len(rows),
        "rmse": rmse(obs, pred),
        "r2": r2(obs, pred),
    }


# ---------------------------------------------------------------------------
# Joint NLS refit (same recipe as code/refit.py)
# ---------------------------------------------------------------------------
def residuals(params_vec, sf_data, far_data):
    """params_vec = [lam1, lam2, eta, beta2, gamma]; beta1 forced 0."""
    p = dict(
        lam1=params_vec[0], lam2=params_vec[1], eta=params_vec[2],
        beta1=0.0, beta2=params_vec[3], gamma=params_vec[4],
    )
    resids = []
    # SF residuals in log10
    for pmma, dose, sf_obs, _std in sf_data:
        if dose == 0.0:
            continue
        s1, s2 = sigmas_for(pmma)
        try:
            sf_pred = sf_at_dose(dose, p, s1, s2)
        except Exception:
            return np.full(len(sf_data) + len(far_data), 1e3)
        l_obs = np.log10(max(sf_obs, 1e-12))
        l_pred = np.log10(max(sf_pred, 1e-12))
        resids.append(l_obs - l_pred)
    # FAR residuals (linear)
    if far_data:
        times = np.array([t for (pmma, _d, t, _f) in far_data if pmma == 0])
        far_obs = np.array([f for (pmma, _d, _t, f) in far_data if pmma == 0])
        s1, s2 = sigmas_for(0)
        try:
            far_pred = far_curve(200.0, p, s1, s2, times)
        except Exception:
            return np.full(len(sf_data) + len(far_data), 1e3)
        for fo, fp in zip(far_obs, far_pred):
            resids.append(fo - fp)
    return np.array(resids)


def refit_nb1():
    # Bounds: keep lam1 huge (paper says it goes to ~33000), and allow others
    # reasonable ranges similar to HSG refit.
    x0 = np.array([1000.0, 1e-2, 5e-6, 2e-2, 0.2])
    lb = np.array([1.0, 1e-6, 1e-9, 1e-6, 1e-3])
    ub = np.array([1e7,  1.0,  1e-1, 1.0,  10.0])
    res = least_squares(
        residuals, x0, bounds=(lb, ub),
        args=(SF_NB1, FAR_NB1),
        method="trf", x_scale="jac",
        max_nfev=200,
    )
    p = dict(
        lam1=float(res.x[0]), lam2=float(res.x[1]), eta=float(res.x[2]),
        beta1=0.0, beta2=float(res.x[3]), gamma=float(res.x[4]),
    )
    return p, int(res.nfev), float(res.cost), bool(res.success)


# ---------------------------------------------------------------------------
# Run forward with paper Table A1 (replication check of Fig A1)
# ---------------------------------------------------------------------------
print("\n--- Forward with paper Table A1 ---")
sf_rows_A1 = predict_sf(NB1_TABLE_A1)
far_rows_A1, _, _ = predict_far(NB1_TABLE_A1)
m_sf_A1 = sf_metrics([r for r in sf_rows_A1 if r[1] > 0])
m_far_A1 = far_metrics(far_rows_A1)
print(f"SF Table A1: {m_sf_A1}")
print(f"FAR Table A1: {m_far_A1}")

# ---------------------------------------------------------------------------
# Refit NB1 from scratch
# ---------------------------------------------------------------------------
print("\n--- Joint NLS refit on NB1 SF+FAR ---")
refit_p, nfev, cost, ok = refit_nb1()
print(f"refit nfev={nfev} cost={cost:.4g} ok={ok}")
print(f"refit params: {refit_p}")

sf_rows_refit = predict_sf(refit_p)
far_rows_refit, _, _ = predict_far(refit_p)
m_sf_refit = sf_metrics([r for r in sf_rows_refit if r[1] > 0])
m_far_refit = far_metrics(far_rows_refit)
print(f"SF refit: {m_sf_refit}")
print(f"FAR refit: {m_far_refit}")

# ---------------------------------------------------------------------------
# Figure A1 reproduction
# ---------------------------------------------------------------------------
fig, (ax_sf, ax_far) = plt.subplots(1, 2, figsize=(11, 4.2))

# Left: SF vs dose for both PMMA conditions
for pmma, color, marker in [(0, "C0", "o"), (32, "C3", "s")]:
    obs = [(r[1], r[2]) for r in sf_rows_A1 if r[0] == pmma]
    obs.sort()
    doses = np.array([o[0] for o in obs])
    sfs = np.array([o[1] for o in obs])
    ax_sf.plot(doses, sfs, marker, color=color, ms=6,
               label=f"NB1 data {pmma} mm")

    # Paper Table A1 curve
    dose_grid = np.linspace(0.01, 7.0, 80)
    s1, s2 = sigmas_for(pmma)
    sf_grid_paper = [sf_at_dose(d, NB1_TABLE_A1, s1, s2) for d in dose_grid]
    ax_sf.plot(dose_grid, sf_grid_paper, "--", color=color, alpha=0.7,
               label=f"Paper Table A1 {pmma} mm")
    # Our refit curve
    sf_grid_refit = [sf_at_dose(d, refit_p, s1, s2) for d in dose_grid]
    ax_sf.plot(dose_grid, sf_grid_refit, "-", color=color, alpha=0.55,
               label=f"Our refit {pmma} mm")

ax_sf.set_yscale("log")
ax_sf.set_xlabel("Dose [Gy]")
ax_sf.set_ylabel("SF")
ax_sf.set_title("NB1RGB SF (paper Fig A1 left)")
ax_sf.set_ylim(5e-3, 2.0)
ax_sf.grid(alpha=0.3, which="both")
ax_sf.legend(fontsize=7, loc="lower left")

# Right: relative FAR vs time for 0 mm
times_obs = np.array([r[2] for r in far_rows_A1])
far_obs = np.array([r[3] for r in far_rows_A1])
ax_far.plot(times_obs, far_obs, "o", color="C0", ms=6, label="NB1 data 0 mm")
t_grid = np.linspace(0.0, 12.0, 80)
s1, s2 = sigmas_for(0)
far_grid_paper = far_curve(200.0, NB1_TABLE_A1, s1, s2, t_grid)
ax_far.plot(t_grid, far_grid_paper, "--", color="C0", alpha=0.7,
            label="Paper Table A1")
far_grid_refit = far_curve(200.0, refit_p, s1, s2, t_grid)
ax_far.plot(t_grid, far_grid_refit, "-", color="C2", alpha=0.7,
            label="Our refit")
ax_far.set_xlabel("Time after irradiation [h]")
ax_far.set_ylabel("relative FAR")
ax_far.set_title("NB1RGB relative FAR (paper Fig A1 right)")
ax_far.set_ylim(0.0, 1.05)
ax_far.grid(alpha=0.3)
ax_far.legend(fontsize=8)

fig.suptitle("Replication of Appendix A (NB1RGB) — Sakata et al. 2021")
fig.tight_layout()
fig_out = ROOT / "figures" / "repass" / "m9_nb1rgb_figA1.png"
fig.savefig(fig_out, dpi=150)
plt.close(fig)
print(f"Wrote {fig_out}")

# ---------------------------------------------------------------------------
# Compare refit params to Table A1
# ---------------------------------------------------------------------------
def ratio(a, b):
    if b == 0:
        return None
    return a / b


param_compare = {
    k: {
        "paper": NB1_TABLE_A1[k],
        "refit": refit_p[k],
        "ratio_refit_over_paper": ratio(refit_p[k], NB1_TABLE_A1[k]),
    }
    for k in NB1_TABLE_A1
}

out = {
    "claim_M9_NB1RGB_SF_fit_ok": {
        "paper_qualitative": "TLK CAN be optimized to fit NB1RGB SF",
        "paper_TableA1_metrics": m_sf_A1,
        "our_refit_metrics": m_sf_refit,
        "interpretation": (
            "SF reproducible. R^2 with paper Table A1 ~= {0:.3f}; "
            "our refit reaches R^2 ~= {1:.3f}."
        ).format(m_sf_A1["r2"], m_sf_refit["r2"]),
    },
    "claim_M9_NB1RGB_FAR_misfit": {
        "paper_qualitative": "TLK CANNOT adequately fit NB1RGB FAR kinetics",
        "paper_TableA1_FAR_metrics": m_far_A1,
        "our_refit_FAR_metrics": m_far_refit,
        "interpretation": (
            "If FAR R^2 with paper Table A1 is poor (<<1) and even our joint "
            "refit cannot bring it to HSGc-C5 level (~0.96), this confirms "
            "the paper's claim that TLK fails on NB1RGB rejoining kinetics."
        ),
        "paper_claim_confirmed": (
            m_far_A1["r2"] < 0.6 and m_far_refit["r2"] < 0.85
        ),
    },
    "claim_M10_TableA1_params_recovered": {
        "comparison": param_compare,
        "lam1_huge": refit_p["lam1"] > 1e3,
        "qualitative_match": (
            refit_p["lam1"] > 1e3 and refit_p["lam2"] < 5e-2
            and refit_p["eta"] < 5e-5
        ),
        "exact_match_within_2x": all(
            (0.5 <= (refit_p[k] / NB1_TABLE_A1[k]) <= 2.0)
            for k in ("lam2", "eta", "beta2", "gamma")
            if NB1_TABLE_A1[k] != 0
        ),
    },
    "refit_meta": {
        "nfev": nfev, "cost": cost, "success": ok,
    },
}

OUT_JSON = ROOT / "results" / "repass" / "m9_nb1rgb_appendixA.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(out, indent=2))
print(f"\n{json.dumps(out, indent=2)}")
