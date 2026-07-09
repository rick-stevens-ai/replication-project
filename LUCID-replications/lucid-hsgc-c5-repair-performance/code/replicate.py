"""
Replicate Figure 5 of Sakata et al. (Cancers 13:6046, 2021).

Uses:
  * Paper's published Table 1 TLK parameters (lam1, lam2, eta, beta1, beta2, gamma)
  * Simulated DSB yields (Sigma1, Sigma2) recovered from Section 3.2 + Discussion
  * Public supplements SF.csv and FAR.csv (HSGc-C5 = "HSG" rows only)

Outputs:
  * results/sf_pred.csv  : measured SF, model SF, residuals
  * results/far_pred.csv : measured FAR, model FAR, residuals
  * results/metrics.json : per-condition + overall RMSE, chi2, R^2
  * figures/sf_curve.png, figures/far_curve.png
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tlk_model import (
    TABLE1, sf_at_dose, far_curve, sigmas_for, T_END_SF,
    SIGMA1_0MM, SIGMA1_32MM, SIGMA2_0MM, SIGMA2_32MM,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "supplement"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: c.strip() for c in df.columns})
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
    return df


def load_sf() -> pd.DataFrame:
    df = pd.read_csv(DATA / "SF.csv", skipinitialspace=True)
    df = _clean_columns(df)
    df = df[df["Cell"] == "HSG"].copy()
    df["PMMA"] = df["PMMAthick[mm]"].astype(int)
    df["Dose"] = df["Dose(Gy)"].astype(float)
    df["SF"] = df["SF"].astype(float)
    df["StdDev"] = df["StdDev"].astype(float)
    return df.reset_index(drop=True)


def load_far() -> pd.DataFrame:
    df = pd.read_csv(DATA / "FAR.csv", skipinitialspace=True)
    df = _clean_columns(df)
    df = df[df["Cell"] == "HSG"].copy()
    df["PMMA"] = df["PMMAthick[mm]"].astype(int)
    df["Dose"] = df["Dose(Gy)"].astype(float)
    df["time"] = df["time(h)"].astype(float)
    df["FAR"] = df["FAR(%)"].astype(float)
    return df.reset_index(drop=True)


def predict_sf(sf_df: pd.DataFrame, params: dict) -> pd.DataFrame:
    preds = []
    for pmma, group in sf_df.groupby("PMMA"):
        sigma1, sigma2 = sigmas_for(int(pmma))
        for _, row in group.iterrows():
            pred = sf_at_dose(row["Dose"], params, sigma1, sigma2)
            preds.append({
                "PMMA": int(pmma),
                "Dose": row["Dose"],
                "SF_meas": row["SF"],
                "StdDev": row["StdDev"],
                "SF_pred": pred,
                "Sigma1": sigma1,
                "Sigma2": sigma2,
            })
    out = pd.DataFrame(preds)
    out["resid"] = out["SF_pred"] - out["SF_meas"]
    return out


def predict_far(far_df: pd.DataFrame, params: dict) -> pd.DataFrame:
    preds = []
    for pmma, group in far_df.groupby("PMMA"):
        sigma1, sigma2 = sigmas_for(int(pmma))
        for dose, sub in group.groupby("Dose"):
            sub = sub.sort_values("time")
            times = sub["time"].to_numpy()
            rel = far_curve(float(dose), params, sigma1, sigma2, times)
            for t, meas, pred in zip(times, sub["FAR"].to_numpy(), rel):
                preds.append({
                    "PMMA": int(pmma),
                    "Dose": float(dose),
                    "time": float(t),
                    "FAR_meas": float(meas),
                    "FAR_pred": float(pred),
                })
    out = pd.DataFrame(preds)
    out["resid"] = out["FAR_pred"] - out["FAR_meas"]
    return out


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a), np.asarray(b)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def r2(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a), np.asarray(b)
    ss_res = float(np.sum((a - b) ** 2))
    ss_tot = float(np.sum((a - np.mean(a)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def log_rmse(meas: np.ndarray, pred: np.ndarray) -> float:
    """RMSE in log10(SF) space for survival curves spanning decades."""
    m = (meas > 0) & (pred > 0)
    if not m.any():
        return float("nan")
    return float(np.sqrt(np.mean((np.log10(meas[m]) - np.log10(pred[m])) ** 2)))


def compute_metrics(sf_pred: pd.DataFrame, far_pred: pd.DataFrame) -> dict:
    metrics = {"SF": {}, "FAR": {}}
    for pmma, sub in sf_pred.groupby("PMMA"):
        metrics["SF"][f"PMMA_{int(pmma)}mm"] = {
            "n": int(len(sub)),
            "rmse": rmse(sub["SF_meas"], sub["SF_pred"]),
            "log10_rmse": log_rmse(sub["SF_meas"].to_numpy(), sub["SF_pred"].to_numpy()),
            "r2": r2(sub["SF_meas"], sub["SF_pred"]),
        }
    metrics["SF"]["overall"] = {
        "n": int(len(sf_pred)),
        "rmse": rmse(sf_pred["SF_meas"], sf_pred["SF_pred"]),
        "log10_rmse": log_rmse(sf_pred["SF_meas"].to_numpy(), sf_pred["SF_pred"].to_numpy()),
        "r2": r2(sf_pred["SF_meas"], sf_pred["SF_pred"]),
    }
    for pmma, sub in far_pred.groupby("PMMA"):
        metrics["FAR"][f"PMMA_{int(pmma)}mm"] = {
            "n": int(len(sub)),
            "rmse": rmse(sub["FAR_meas"], sub["FAR_pred"]),
            "r2": r2(sub["FAR_meas"], sub["FAR_pred"]),
        }
    metrics["FAR"]["overall"] = {
        "n": int(len(far_pred)),
        "rmse": rmse(far_pred["FAR_meas"], far_pred["FAR_pred"]),
        "r2": r2(far_pred["FAR_meas"], far_pred["FAR_pred"]),
    }
    return metrics


def plot_sf(sf_pred: pd.DataFrame, sf_df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    colors = {0: "tab:blue", 32: "tab:red"}
    dense_dose = np.linspace(0, 8, 81)
    for pmma in sorted(sf_df["PMMA"].unique()):
        sigma1, sigma2 = sigmas_for(int(pmma))
        sf_curve = [sf_at_dose(float(d), TABLE1, sigma1, sigma2) for d in dense_dose]
        ax.plot(dense_dose, sf_curve, "-", color=colors[pmma],
                label=f"Cal. PMMA {pmma} mm")
        sub = sf_df[sf_df["PMMA"] == pmma]
        ax.errorbar(sub["Dose"], sub["SF"], yerr=sub["StdDev"], fmt="o",
                    color=colors[pmma], capsize=3,
                    label=f"Exp. PMMA {pmma} mm")
    ax.set_yscale("log")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Cell Surviving Fraction")
    ax.set_title("HSGc-C5 SF (replication of Sakata et al. Figure 5, left)")
    ax.set_ylim(1e-2, 1.5)
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_far(far_pred: pd.DataFrame, far_df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    colors = {0: "tab:blue", 32: "tab:red"}
    for (pmma, dose), sub in far_df.groupby(["PMMA", "Dose"]):
        sigma1, sigma2 = sigmas_for(int(pmma))
        dense_t = np.linspace(0, max(12.5, sub["time"].max()), 200)
        rel = far_curve(float(dose), TABLE1, sigma1, sigma2, dense_t)
        ax.plot(dense_t, rel, "-", color=colors[pmma],
                label=f"Cal. PMMA {pmma} mm, {int(dose)} Gy")
        ax.plot(sub["time"], sub["FAR"], "o", color=colors[pmma],
                label=f"Exp. PMMA {pmma} mm, {int(dose)} Gy")
    ax.set_xlabel("Time after irradiation (h)")
    ax.set_ylabel("Relative FAR")
    ax.set_title("HSGc-C5 FAR (replication of Sakata et al. Figure 5, right)")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main():
    sf_df = load_sf()
    far_df = load_far()
    print(f"Loaded {len(sf_df)} SF rows and {len(far_df)} FAR rows (HSGc-C5 only).")

    sf_pred = predict_sf(sf_df, TABLE1)
    far_pred = predict_far(far_df, TABLE1)

    sf_pred.to_csv(RESULTS / "sf_pred.csv", index=False)
    far_pred.to_csv(RESULTS / "far_pred.csv", index=False)

    metrics = compute_metrics(sf_pred, far_pred)
    metrics["sigmas"] = {
        "PMMA_0mm":  {"Sigma1": SIGMA1_0MM,  "Sigma2": SIGMA2_0MM},
        "PMMA_32mm": {"Sigma1": SIGMA1_32MM, "Sigma2": SIGMA2_32MM},
    }
    metrics["params_used"] = TABLE1
    (RESULTS / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))

    plot_sf(sf_pred, sf_df, FIGURES / "sf_curve.png")
    plot_far(far_pred, far_df, FIGURES / "far_curve.png")
    print("Wrote SF/FAR figures.")


if __name__ == "__main__":
    main()
