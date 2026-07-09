#!/usr/bin/env python3
"""
fit_models.py — Smoke replication of the LQ and Induced Repair (IR) survival
models against the Polgár 2022 STOREDB curated dataset, plus a small high-LET
slice that the 2026 LET/HRS paper extends with MML+LEM.

This script demonstrates that:

  1. The classical Linear-Quadratic (LQ) model
         S(D) = exp(-(alpha D + beta D^2))
     fits well at moderate-to-high doses but typically over-estimates SF at
     very low doses where hyper-radiosensitivity (HRS) is present.

  2. The Induced Repair (IR) model of Joiner & Marples,
         S(D) = exp(-alpha_r D * (1 + (alpha_s/alpha_r - 1) * exp(-D / Dc))
                    - beta D^2)
     captures the HRS "dip" at low dose and the induced radioresistance (IRR)
     plateau between ~0.3 and 1 Gy.

  3. Our re-fitted parameters reproduce, within reasonable agreement, the
     published LQ and IR fits recorded in the curated database.

Outputs go to results/ and figures/.
"""
from __future__ import annotations
import csv
import math
import json
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
LONG = ROOT / "results" / "curves_long.csv"
META = ROOT / "results" / "curves_meta.csv"
FIT_OUT = ROOT / "results" / "fits.csv"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def lq(D, alpha, beta):
    return np.exp(-(alpha * D + beta * D * D))


def ir(D, alpha_r, alpha_s, Dc, beta):
    # Joiner & Marples (1993) / Lambin (1993) induced-repair model.
    # alpha_s: low-dose hypersensitive slope (alpha_s >= alpha_r typically).
    # alpha_r: residual high-dose slope (-> alpha of LQ at large D).
    # Dc:      transition dose between HRS and induced radioresistance.
    # beta:    quadratic LQ-like term.
    safe_Dc = max(Dc, 1e-6)
    eff_alpha = alpha_r * (1.0 + (alpha_s / alpha_r - 1.0) * np.exp(-D / safe_Dc))
    return np.exp(-(eff_alpha * D + beta * D * D))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_data():
    points = defaultdict(list)
    with LONG.open() as f:
        for row in csv.DictReader(f):
            try:
                d = float(row["dose_Gy"])
                sf = float(row["SF"])
            except ValueError:
                continue
            if sf <= 0 or not np.isfinite(sf):
                continue
            sf_min = float(row["SF_min"]) if row["SF_min"] not in ("", "X") else None
            sf_max = float(row["SF_max"]) if row["SF_max"] not in ("", "X") else None
            points[int(row["id"])].append((d, sf, sf_min, sf_max))

    meta = {}
    with META.open() as f:
        for row in csv.DictReader(f):
            meta[int(row["id"])] = row

    # Sort by dose
    for k in points:
        points[k].sort(key=lambda t: t[0])
    return points, meta


def fit_one(D, S, model="LQ"):
    """Fit one curve. Returns (params, perr) or (None, None) on failure."""
    D = np.asarray(D, float)
    S = np.asarray(S, float)
    if len(D) < 4:
        return None, None
    try:
        if model == "LQ":
            p0 = [0.3, 0.03]
            bounds = ([0.0, 0.0], [10.0, 5.0])
            p, cov = curve_fit(lq, D, S, p0=p0, bounds=bounds, maxfev=10000)
        else:
            # IR initial guess
            p0 = [0.3, 1.0, 0.3, 0.03]
            bounds = ([0.0, 0.0, 1e-3, 0.0], [10.0, 30.0, 10.0, 5.0])
            p, cov = curve_fit(ir, D, S, p0=p0, bounds=bounds, maxfev=20000)
        if cov is None or not np.all(np.isfinite(cov)):
            perr = np.full_like(p, np.nan)
        else:
            perr = np.sqrt(np.diag(np.clip(cov, 0, None)))
        return p, perr
    except Exception:
        return None, None


def aicc(rss, n, k):
    if n - k - 1 <= 0 or rss <= 0:
        return float("inf")
    aic = n * math.log(rss / n) + 2 * k
    return aic + (2 * k * (k + 1)) / (n - k - 1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    points, meta = load_data()
    fit_rows = []
    hrs_ids = []  # candidate datasets demonstrating HRS (IR significantly better than LQ)

    for did in sorted(points):
        pts = points[did]
        if len(pts) < 5:
            continue
        D = np.array([p[0] for p in pts])
        S = np.array([p[1] for p in pts])

        p_lq, _ = fit_one(D, S, "LQ")
        p_ir, _ = fit_one(D, S, "IR")

        if p_lq is None:
            continue
        S_lq = lq(D, *p_lq)
        rss_lq = float(np.sum((S - S_lq) ** 2))
        aicc_lq = aicc(rss_lq, len(D), 2)

        if p_ir is not None:
            S_ir = ir(D, *p_ir)
            rss_ir = float(np.sum((S - S_ir) ** 2))
            aicc_ir = aicc(rss_ir, len(D), 4)
        else:
            rss_ir = float("nan")
            aicc_ir = float("nan")

        # HRS demonstration: IR meaningfully better than LQ (delta AICc > 4)
        delta = (aicc_lq - aicc_ir) if math.isfinite(aicc_ir) else float("-inf")
        if delta > 4 and p_ir is not None and p_ir[1] > p_ir[0] * 1.5 and p_ir[2] < 1.0:
            hrs_ids.append((did, delta, p_ir))

        row = {
            "id": did,
            "n_points": len(D),
            "lq_alpha_fit": p_lq[0] if p_lq is not None else None,
            "lq_beta_fit": p_lq[1] if p_lq is not None else None,
            "lq_rss": rss_lq,
            "lq_aicc": aicc_lq,
            "ir_alpha_r_fit": p_ir[0] if p_ir is not None else None,
            "ir_alpha_s_fit": p_ir[1] if p_ir is not None else None,
            "ir_dc_fit": p_ir[2] if p_ir is not None else None,
            "ir_beta_fit": p_ir[3] if p_ir is not None else None,
            "ir_rss": rss_ir,
            "ir_aicc": aicc_ir,
            "delta_aicc_LQ_minus_IR": delta if math.isfinite(delta) else None,
            "cell_line": meta[did].get("cell_line", ""),
            "irradiation": meta[did].get("irradiation", ""),
            "doi": meta[did].get("doi", ""),
            # Published references (may be empty)
            "lq_alpha_pub": meta[did].get("lq_alpha", ""),
            "lq_beta_pub": meta[did].get("lq_beta", ""),
            "ir_alpha_r_pub": meta[did].get("ir_alpha_r", ""),
            "ir_alpha_s_pub": meta[did].get("ir_alpha_s", ""),
            "ir_dc_pub": meta[did].get("ir_dc", ""),
            "ir_beta_pub": meta[did].get("ir_beta", ""),
        }
        fit_rows.append(row)

    # Write fit table
    with FIT_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fit_rows[0].keys()))
        w.writeheader()
        w.writerows(fit_rows)

    # Summary stats
    n_total = len(fit_rows)
    n_lq = sum(1 for r in fit_rows if r["lq_alpha_fit"] is not None)
    n_ir = sum(1 for r in fit_rows if r["ir_alpha_r_fit"] is not None)
    print(f"Fitted {n_total} curves: LQ={n_lq}, IR={n_ir}")
    print(f"Datasets where IR beats LQ by delta_AICc > 4 with HRS-shaped params: {len(hrs_ids)}")

    # Published-vs-fit comparison (when both available)
    diffs = {"lq_alpha": [], "lq_beta": [], "ir_alpha_r": [], "ir_alpha_s": [], "ir_dc": []}
    for r in fit_rows:
        for key in diffs:
            pub = r.get(f"{key}_pub", "")
            fit = r.get(f"{key}_fit")
            if pub not in ("", None) and fit is not None:
                try:
                    pub_v = float(pub)
                    if pub_v > 0 and fit > 0:
                        diffs[key].append((pub_v, fit))
                except (ValueError, TypeError):
                    pass

    print("\nFit vs. published (median |relative diff|, n):")
    for key, pairs in diffs.items():
        if not pairs:
            print(f"  {key}: no overlap")
            continue
        rels = [abs(f - p) / abs(p) for p, f in pairs]
        print(f"  {key:>14}: median={np.median(rels):.3f}  mean={np.mean(rels):.3f}  n={len(pairs)}")

    # ---- Figure 1: best HRS example - LQ vs IR vs data ----
    if hrs_ids:
        hrs_ids.sort(key=lambda t: -t[1])
        for rank, (did, delta, pir) in enumerate(hrs_ids[:3]):
            D = np.array([p[0] for p in points[did]])
            S = np.array([p[1] for p in points[did]])
            Sm = np.array([p[2] if p[2] is not None else p[1] for p in points[did]])
            SM = np.array([p[3] if p[3] is not None else p[1] for p in points[did]])
            yerr = np.vstack([np.maximum(S - Sm, 0), np.maximum(SM - S, 0)])

            # Use the fitted LQ + IR
            row = next(r for r in fit_rows if r["id"] == did)
            p_lq = (row["lq_alpha_fit"], row["lq_beta_fit"])

            Dgrid = np.linspace(0.01, D.max() * 1.05, 400)
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.errorbar(D, S, yerr=yerr, fmt="o", ms=4, color="k", label="data")
            ax.plot(Dgrid, lq(Dgrid, *p_lq), "--", color="C1", label=f"LQ fit (α={p_lq[0]:.2f}, β={p_lq[1]:.3f})")
            ax.plot(Dgrid, ir(Dgrid, *pir), "-", color="C0",
                    label=f"IR fit (αs={pir[1]:.2f}, αr={pir[0]:.2f}, Dc={pir[2]:.2f}, β={pir[3]:.3f})")
            ax.set_xscale("linear")
            ax.set_yscale("log")
            ax.set_xlabel("Dose [Gy]")
            ax.set_ylabel("Surviving fraction")
            ax.set_title(f"Dataset {did}: HRS-IRR signature\n{(row['cell_line'] or '')[:50]}  |  {(row['irradiation'] or '')[:50]}")
            ax.legend(fontsize=8, loc="lower left")
            ax.grid(True, which="both", alpha=0.3)
            out = FIG_DIR / f"hrs_example_rank{rank+1}_id{did}.png"
            fig.tight_layout()
            fig.savefig(out, dpi=140)
            plt.close(fig)
            print(f"  wrote {out.relative_to(ROOT)}  (delta AICc={delta:.1f})")
    else:
        print("No HRS-shaped datasets passed criteria (this would be unexpected).")

    # ---- Figure 2: cohort-level histogram of delta AICc (IR vs LQ) ----
    deltas = [r["delta_aicc_LQ_minus_IR"] for r in fit_rows if r["delta_aicc_LQ_minus_IR"] is not None]
    deltas = np.array(deltas)
    if len(deltas):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(deltas, bins=40, color="C0", alpha=0.8)
        ax.axvline(0, color="k", lw=1)
        ax.axvline(4, color="r", lw=1, ls="--", label="ΔAICc=4 (IR favored)")
        ax.set_xlabel("ΔAICc = AICc(LQ) - AICc(IR)")
        ax.set_ylabel("# datasets")
        ax.set_title("Model selection across 101 HRS curves\n(positive = IR fits better than LQ)")
        ax.legend()
        out = FIG_DIR / "delta_aicc_histogram.png"
        fig.tight_layout()
        fig.savefig(out, dpi=140)
        plt.close(fig)
        print(f"  wrote {out.relative_to(ROOT)}")
        frac = float(np.mean(deltas > 4))
        print(f"  fraction of curves where IR meaningfully beats LQ: {frac:.2%} ({int(np.sum(deltas > 4))}/{len(deltas)})")

    # Provenance dump
    prov = {
        "n_datasets_total": n_total,
        "n_datasets_LQ_fit": n_lq,
        "n_datasets_IR_fit": n_ir,
        "n_HRS_signatures": len(hrs_ids),
        "fit_vs_published": {k: int(len(v)) for k, v in diffs.items()},
    }
    (ROOT / "results" / "fit_summary.json").write_text(json.dumps(prov, indent=2))
    print(f"\nWrote summary to results/fit_summary.json")


if __name__ == "__main__":
    main()
