#!/usr/bin/env python3
"""
strengthen_fits.py — Strengthened LQ + Induced-Repair (IR) reproduction on
Polgár 2022 STOREDB DATASET1252, for the final LUCID-100 verdict on
Sennhenn et al. 2026 (Radiat Res 205(5):472-483, paywalled body).

This script extends the smoke replication with:

  1. Per-curve fits with formal goodness-of-fit on log-survival residuals:
        R^2(log10 SF), RMSE(log10 SF), reduced chi^2 if SF errors available.
  2. Non-parametric bootstrap (B=500) of LQ and IR parameters
        -> 95% CIs for alpha, beta, alpha_r, alpha_s, D_c, beta_IR per curve.
  3. Model selection (AICc and BIC, IR vs LQ) per curve.
  4. Per-cell-line aggregation (median +/- IQR of fitted params).
  5. Low-LET vs high-LET subset analysis with explicit LET band breakdown
        (low-LET <= 5 keV/um; intermediate 5-30; high >= 30; plus neutrons).
        Reports Mann-Whitney U test on D_c and alpha_s/alpha_r where n>=3.
  6. Combined CSVs:
        results/fits_strengthened.csv    (per-curve, with CIs + GOF)
        results/cellline_summary.csv     (per-cell-line aggregates)
        results/let_band_summary.csv     (per-LET-band aggregates + tests)
  7. Figures:
        figures/gof_loglog.png           (R^2 distribution LQ vs IR)
        figures/let_band_dc.png          (D_c by LET band, boxplot)
        figures/let_band_amp.png         (alpha_s/alpha_r by LET band)
        figures/published_vs_fit.png     (scatter, our re-fit vs published)
  8. results/strengthened_summary.json   (machine-readable headline numbers)

CPU-only, single-thread, ~30 s on CherryRd.
"""
from __future__ import annotations
import csv, json, math, re, warnings
from pathlib import Path
from collections import defaultdict
warnings.filterwarnings('ignore')

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import mannwhitneyu
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260622)

ROOT = Path(__file__).resolve().parent.parent
LONG = ROOT / "results" / "curves_long.csv"
META = ROOT / "results" / "curves_meta.csv"
OUT_FITS = ROOT / "results" / "fits_strengthened.csv"
OUT_CELL = ROOT / "results" / "cellline_summary.csv"
OUT_LET  = ROOT / "results" / "let_band_summary.csv"
OUT_JSON = ROOT / "results" / "strengthened_summary.json"
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

B_BOOT = 200
MIN_POINTS = 6  # require >=6 dose points for bootstrap CIs


# -------- models --------
def lq(D, alpha, beta):
    return np.exp(-(alpha * D + beta * D * D))

def ir(D, alpha_r, alpha_s, Dc, beta):
    safe_Dc = max(Dc, 1e-6)
    eff = alpha_r * (1.0 + (alpha_s / alpha_r - 1.0) * np.exp(-D / safe_Dc))
    return np.exp(-(eff * D + beta * D * D))

LQ_P0     = [0.3, 0.03]
LQ_BNDS   = ([0.0, 0.0], [10.0, 5.0])
IR_P0     = [0.3, 1.0, 0.3, 0.03]
IR_BNDS   = ([0.0, 0.0, 1e-3, 0.0], [10.0, 30.0, 10.0, 5.0])


def fit_lq(D, S):
    return curve_fit(lq, D, S, p0=LQ_P0, bounds=LQ_BNDS, maxfev=20000)[0]

def fit_ir(D, S):
    return curve_fit(ir, D, S, p0=IR_P0, bounds=IR_BNDS, maxfev=30000)[0]


def safe_fit(D, S, kind):
    try:
        if kind == "LQ":
            return fit_lq(D, S)
        else:
            return fit_ir(D, S)
    except Exception:
        return None


def gof_log(D, S, S_hat):
    """Goodness-of-fit on log10(SF). Returns (R2, RMSE) on log-scale."""
    y = np.log10(np.clip(S, 1e-12, None))
    yh = np.log10(np.clip(S_hat, 1e-12, None))
    ss_res = float(np.sum((y - yh) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    rmse = math.sqrt(ss_res / len(y))
    return r2, rmse


def aicc(rss, n, k):
    if n - k - 1 <= 0 or rss <= 0:
        return float("inf")
    aic = n * math.log(rss / n) + 2 * k
    return aic + (2 * k * (k + 1)) / (n - k - 1)

def bic(rss, n, k):
    if rss <= 0 or n <= 0:
        return float("inf")
    return n * math.log(rss / n) + k * math.log(n)


def bootstrap(D, S, kind, B=B_BOOT):
    """Non-parametric resampling bootstrap (resample (D,S) pairs with replacement)."""
    n = len(D)
    params = []
    if n < MIN_POINTS:
        return None
    fails = 0
    max_fails = B * 3
    while len(params) < B and fails < max_fails:
        idx = rng.integers(0, n, n)
        Db = D[idx]; Sb = S[idx]
        # Avoid degenerate samples (all same dose) which break curve_fit
        if len(np.unique(Db)) < 3:
            fails += 1
            continue
        p = safe_fit(Db, Sb, kind)
        if p is not None:
            params.append(p)
        else:
            fails += 1
    if len(params) < 30:
        return None
    arr = np.asarray(params)
    lo = np.percentile(arr, 2.5, axis=0)
    hi = np.percentile(arr, 97.5, axis=0)
    med = np.percentile(arr, 50.0, axis=0)
    return {"lo": lo.tolist(), "hi": hi.tolist(), "med": med.tolist(), "B_used": len(params)}


# -------- LET parsing / classification --------
def parse_let(irr: str):
    if not irr:
        return None
    s = irr.replace("μ", "u")
    m = re.search(r"LET\s*=\s*([0-9]+\.?[0-9]*)\s*keV/?u?m?", s, re.I)
    if m: return float(m.group(1))
    m = re.search(r"([0-9]+\.?[0-9]*)\s*keV/?u?m?", s, re.I)
    if m: return float(m.group(1))
    return None

def is_photon_lowLET(irr: str):
    if not irr: return False
    s = irr.lower()
    return any(k in s for k in [
        "x-ray", "kvp", "kv x", "gamma", "γ-ray", "γ ray", "γrays",
        "6 mv", "4 mv", "60co", "co60", "cobalt", "mv photon"])

def classify_let(irr: str):
    """Return (band_label, nominal_LET_keV_per_um) or (None, None) if unknown."""
    let = parse_let(irr)
    if let is not None:
        if let < 5:
            return ("low", let)
        if let < 30:
            return ("intermediate", let)
        return ("high", let)
    if is_photon_lowLET(irr):
        return ("low", 2.0)   # nominal kV/MV/Co60 ~2 keV/um
    # neutrons / unspecified ions
    s = (irr or "").lower()
    if "neutron" in s:
        return ("neutron", None)
    if any(k in s for k in ["mev/u", "mev/n", "12c", "carbon", "helium", "alpha", "ion"]):
        return ("ion-unspecLET", None)
    return (None, None)


# -------- load data --------
def load():
    pts = defaultdict(list)
    for row in csv.DictReader(LONG.open()):
        try:
            d = float(row["dose_Gy"]); sf = float(row["SF"])
        except ValueError:
            continue
        if sf <= 0 or not math.isfinite(sf):
            continue
        smin = row["SF_min"]; smax = row["SF_max"]
        smin = float(smin) if smin not in ("", "X", None) else None
        smax = float(smax) if smax not in ("", "X", None) else None
        pts[int(row["id"])].append((d, sf, smin, smax))
    meta = {int(r["id"]): r for r in csv.DictReader(META.open())}
    for k in pts:
        pts[k].sort(key=lambda t: t[0])
    return pts, meta


# -------- main --------
def main():
    pts, meta = load()
    out_rows = []
    n_lq_ok = n_ir_ok = 0
    n_with_boot_lq = n_with_boot_ir = 0
    hrs_curves = []

    ids_sorted = sorted(pts)
    print(f"Starting fits over {len(ids_sorted)} datasets (B_BOOT={B_BOOT})...", flush=True)
    import time
    t_start = time.time()
    for i, did in enumerate(ids_sorted, 1):
        rows = pts[did]
        if len(rows) < 4:
            continue
        if i % 5 == 0 or i == 1 or i == len(ids_sorted):
            print(f"  [{i}/{len(ids_sorted)}] id={did} n_pts={len(rows)} t={time.time()-t_start:.1f}s", flush=True)
        D = np.array([r[0] for r in rows], float)
        S = np.array([r[1] for r in rows], float)
        n = len(D)
        m = meta.get(did, {})
        cl = (m.get("cell_line") or "").strip()
        irr = (m.get("cell_line"), m.get("irradiation"))[1] or ""

        p_lq = safe_fit(D, S, "LQ")
        p_ir = safe_fit(D, S, "IR")

        # GOF + AICc + BIC
        if p_lq is not None:
            Sh = lq(D, *p_lq)
            rss_lq = float(np.sum((S - Sh) ** 2))
            r2_lq, rmse_lq = gof_log(D, S, Sh)
            aicc_lq = aicc(rss_lq, n, 2)
            bic_lq  = bic(rss_lq, n, 2)
            n_lq_ok += 1
        else:
            rss_lq = r2_lq = rmse_lq = aicc_lq = bic_lq = float("nan")

        if p_ir is not None:
            Sh = ir(D, *p_ir)
            rss_ir = float(np.sum((S - Sh) ** 2))
            r2_ir, rmse_ir = gof_log(D, S, Sh)
            aicc_ir = aicc(rss_ir, n, 4)
            bic_ir  = bic(rss_ir, n, 4)
            n_ir_ok += 1
        else:
            rss_ir = r2_ir = rmse_ir = aicc_ir = bic_ir = float("nan")

        d_aicc = (aicc_lq - aicc_ir) if math.isfinite(aicc_ir) and math.isfinite(aicc_lq) else float("nan")
        d_bic  = (bic_lq  - bic_ir)  if math.isfinite(bic_ir)  and math.isfinite(bic_lq)  else float("nan")

        # Bootstrap CIs
        b_lq = bootstrap(D, S, "LQ") if p_lq is not None else None
        b_ir = bootstrap(D, S, "IR") if p_ir is not None else None
        if b_lq: n_with_boot_lq += 1
        if b_ir: n_with_boot_ir += 1

        band, let_val = classify_let(irr)

        # Tag HRS-positive
        is_hrs = False
        if p_ir is not None and math.isfinite(d_aicc):
            if d_aicc > 4 and p_ir[1] > 1.5 * p_ir[0] and p_ir[2] < 1.0:
                is_hrs = True
                hrs_curves.append(did)

        row = {
            "id": did, "n_points": n,
            "cell_line": cl, "irradiation": irr,
            "let_band": band or "", "let_keV_per_um": let_val if let_val is not None else "",
            "doi": (m.get("doi") or "").strip(),
            "lq_alpha": p_lq[0] if p_lq is not None else "",
            "lq_beta":  p_lq[1] if p_lq is not None else "",
            "lq_r2_log": r2_lq, "lq_rmse_log": rmse_lq,
            "lq_aicc": aicc_lq, "lq_bic": bic_lq,
            "ir_alpha_r": p_ir[0] if p_ir is not None else "",
            "ir_alpha_s": p_ir[1] if p_ir is not None else "",
            "ir_dc":      p_ir[2] if p_ir is not None else "",
            "ir_beta":    p_ir[3] if p_ir is not None else "",
            "ir_r2_log":  r2_ir, "ir_rmse_log": rmse_ir,
            "ir_aicc":    aicc_ir, "ir_bic": bic_ir,
            "delta_aicc_LQ_minus_IR": d_aicc,
            "delta_bic_LQ_minus_IR":  d_bic,
            "is_HRS_positive": int(is_hrs),
            # CIs (LQ)
            "lq_alpha_lo": b_lq["lo"][0] if b_lq else "", "lq_alpha_hi": b_lq["hi"][0] if b_lq else "",
            "lq_beta_lo":  b_lq["lo"][1] if b_lq else "", "lq_beta_hi":  b_lq["hi"][1] if b_lq else "",
            # CIs (IR)
            "ir_alpha_r_lo": b_ir["lo"][0] if b_ir else "", "ir_alpha_r_hi": b_ir["hi"][0] if b_ir else "",
            "ir_alpha_s_lo": b_ir["lo"][1] if b_ir else "", "ir_alpha_s_hi": b_ir["hi"][1] if b_ir else "",
            "ir_dc_lo":      b_ir["lo"][2] if b_ir else "", "ir_dc_hi":      b_ir["hi"][2] if b_ir else "",
            "ir_beta_lo":    b_ir["lo"][3] if b_ir else "", "ir_beta_hi":    b_ir["hi"][3] if b_ir else "",
            "boot_B_lq": b_lq["B_used"] if b_lq else 0,
            "boot_B_ir": b_ir["B_used"] if b_ir else 0,
        }
        out_rows.append(row)

    # Write per-curve CSV
    with OUT_FITS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader(); w.writerows(out_rows)

    # --- cell-line aggregation ---
    by_cl = defaultdict(list)
    for r in out_rows:
        if r["cell_line"]:
            by_cl[r["cell_line"]].append(r)

    cl_rows = []
    for cl, rs in sorted(by_cl.items()):
        def col(name):
            vals = [r[name] for r in rs if r[name] not in ("", None)]
            vals = [float(v) for v in vals if isinstance(v, (int, float, str)) and str(v) != ""]
            vals = [v for v in vals if math.isfinite(v)]
            return vals
        rec = {"cell_line": cl, "n_curves": len(rs)}
        for col_name in ("lq_alpha", "lq_beta", "ir_alpha_r", "ir_alpha_s", "ir_dc"):
            vs = col(col_name)
            if vs:
                rec[f"{col_name}_median"] = float(np.median(vs))
                rec[f"{col_name}_iqr_lo"] = float(np.percentile(vs, 25))
                rec[f"{col_name}_iqr_hi"] = float(np.percentile(vs, 75))
            else:
                rec[f"{col_name}_median"] = ""
                rec[f"{col_name}_iqr_lo"] = ""
                rec[f"{col_name}_iqr_hi"] = ""
        rec["n_HRS_positive"] = sum(1 for r in rs if r["is_HRS_positive"])
        cl_rows.append(rec)

    with OUT_CELL.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cl_rows[0].keys()))
        w.writeheader(); w.writerows(cl_rows)

    # --- LET band aggregation ---
    by_band = defaultdict(list)
    for r in out_rows:
        b = r["let_band"]
        if b:
            by_band[b].append(r)

    band_rows = []
    for band in ("low", "intermediate", "high", "neutron", "ion-unspecLET"):
        rs = by_band.get(band, [])
        if not rs:
            continue
        def col(name):
            vs = [r[name] for r in rs if r[name] not in ("", None)]
            vs = [float(v) for v in vs if str(v) != ""]
            vs = [v for v in vs if math.isfinite(v)]
            return vs
        dc = col("ir_dc")
        ar = col("ir_alpha_r"); aS = col("ir_alpha_s")
        ratios = [s/r for r, s in zip(ar, aS) if r > 1e-9]
        n_hrs = sum(1 for r in rs if r["is_HRS_positive"])
        rec = {
            "let_band": band,
            "n_curves": len(rs),
            "n_HRS_positive": n_hrs,
            "ir_dc_median": float(np.median(dc)) if dc else "",
            "ir_dc_iqr_lo": float(np.percentile(dc, 25)) if dc else "",
            "ir_dc_iqr_hi": float(np.percentile(dc, 75)) if dc else "",
            "ratio_alpha_s_over_r_median": float(np.median(ratios)) if ratios else "",
            "ratio_iqr_lo": float(np.percentile(ratios, 25)) if ratios else "",
            "ratio_iqr_hi": float(np.percentile(ratios, 75)) if ratios else "",
            "ir_alpha_r_median": float(np.median(ar)) if ar else "",
            "ir_alpha_s_median": float(np.median(aS)) if aS else "",
        }
        band_rows.append(rec)

    with OUT_LET.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(band_rows[0].keys()))
        w.writeheader(); w.writerows(band_rows)

    # --- Mann-Whitney tests low vs high ---
    def col_band(band, name):
        rs = by_band.get(band, [])
        vs = [r[name] for r in rs if r[name] not in ("", None)]
        vs = [float(v) for v in vs if str(v) != ""]
        return [v for v in vs if math.isfinite(v)]

    mw_tests = {}
    low_dc = col_band("low", "ir_dc")
    high_dc = col_band("high", "ir_dc")
    if len(low_dc) >= 3 and len(high_dc) >= 3:
        u, p = mannwhitneyu(low_dc, high_dc, alternative="two-sided")
        mw_tests["dc_low_vs_high"] = {"U": float(u), "p": float(p),
                                       "n_low": len(low_dc), "n_high": len(high_dc),
                                       "median_low": float(np.median(low_dc)),
                                       "median_high": float(np.median(high_dc))}
    # ratio
    def ratios_band(band):
        rs = by_band.get(band, [])
        out = []
        for r in rs:
            try:
                ar = float(r["ir_alpha_r"]); aS = float(r["ir_alpha_s"])
                if ar > 1e-9:
                    out.append(aS / ar)
            except Exception:
                pass
        return out
    rl = ratios_band("low"); rh = ratios_band("high")
    if len(rl) >= 3 and len(rh) >= 3:
        u, p = mannwhitneyu(rl, rh, alternative="two-sided")
        mw_tests["ratio_low_vs_high"] = {"U": float(u), "p": float(p),
                                          "n_low": len(rl), "n_high": len(rh),
                                          "median_low": float(np.median(rl)),
                                          "median_high": float(np.median(rh))}

    # --- Figures ---
    # GOF
    r2_lq = [r["lq_r2_log"] for r in out_rows if isinstance(r["lq_r2_log"], float) and math.isfinite(r["lq_r2_log"])]
    r2_ir = [r["ir_r2_log"] for r in out_rows if isinstance(r["ir_r2_log"], float) and math.isfinite(r["ir_r2_log"])]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    bins = np.linspace(-0.5, 1.0, 41)
    ax.hist(r2_lq, bins=bins, alpha=0.55, label=f"LQ  (n={len(r2_lq)}, median={np.median(r2_lq):.3f})", color="C1")
    ax.hist(r2_ir, bins=bins, alpha=0.55, label=f"IR  (n={len(r2_ir)}, median={np.median(r2_ir):.3f})", color="C0")
    ax.axvline(np.median(r2_lq), color="C1", ls="--", lw=1)
    ax.axvline(np.median(r2_ir), color="C0", ls="--", lw=1)
    ax.set_xlabel("R² on log10(SF)"); ax.set_ylabel("# curves")
    ax.set_title("Goodness-of-fit: LQ vs IR (per-curve R² on log-survival)")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "gof_loglog.png", dpi=140); plt.close(fig)

    # Published vs fit scatter (IR alpha_r, alpha_s, Dc)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    for ax, key, label in zip(
        axes,
        ("ir_alpha_r", "ir_alpha_s", "ir_dc"),
        (r"IR $\alpha_r$ [Gy$^{-1}$]", r"IR $\alpha_s$ [Gy$^{-1}$]", r"IR $D_c$ [Gy]")
    ):
        pub_key = {"ir_alpha_r": "ir_alpha_r", "ir_alpha_s": "ir_alpha_s", "ir_dc": "ir_dc"}[key]
        xs, ys = [], []
        for did, m in meta.items():
            try:
                pub = float(m.get(pub_key, "") or "nan")
            except Exception:
                continue
            if not math.isfinite(pub) or pub <= 0:
                continue
            r = next((x for x in out_rows if x["id"] == did), None)
            if r is None or r[key] in ("", None):
                continue
            try:
                fit = float(r[key])
            except Exception:
                continue
            if not math.isfinite(fit):
                continue
            xs.append(pub); ys.append(fit)
        ax.scatter(xs, ys, s=22, alpha=0.7, color="C2")
        lim_lo = max(min(xs + ys + [1e-3]) * 0.5, 1e-3)
        lim_hi = max(xs + ys + [1.0]) * 1.4
        ax.plot([lim_lo, lim_hi], [lim_lo, lim_hi], "k--", lw=1, alpha=0.5)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(lim_lo, lim_hi); ax.set_ylim(lim_lo, lim_hi)
        ax.set_xlabel(f"Published {label}")
        ax.set_ylabel(f"Re-fit {label}")
        ax.set_title(f"n={len(xs)}")
        ax.grid(True, which="both", alpha=0.3)
    fig.suptitle("Independent re-fit vs published IR parameters (Polgár 2022 STOREDB v2)", fontsize=10)
    fig.tight_layout(); fig.savefig(FIG / "published_vs_fit.png", dpi=140); plt.close(fig)

    # D_c by LET band (boxplot)
    bands_order = [b for b in ("low", "intermediate", "high", "neutron") if by_band.get(b)]
    data_dc = [col_band(b, "ir_dc") for b in bands_order]
    labels = [f"{b}\n(n={len(d)})" for b, d in zip(bands_order, data_dc)]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    if any(len(d) for d in data_dc):
        ax.boxplot(data_dc, labels=labels, showmeans=True)
        ax.set_ylabel(r"IR transition dose $D_c$ [Gy]")
        ax.set_title("Joiner–Marples IR transition dose by LET band (STOREDB v2)")
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout(); fig.savefig(FIG / "let_band_dc.png", dpi=140)
    plt.close(fig)

    # alpha_s/alpha_r by LET band
    data_r = [ratios_band(b) for b in bands_order]
    labels = [f"{b}\n(n={len(d)})" for b, d in zip(bands_order, data_r)]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    if any(len(d) for d in data_r):
        # clip extreme outliers for visibility
        clipped = [[min(x, 60) for x in d] for d in data_r]
        ax.boxplot(clipped, labels=labels, showmeans=True)
        ax.set_ylabel(r"HRS amplitude $\alpha_s/\alpha_r$ (clipped at 60)")
        ax.set_title("HRS amplitude by LET band (STOREDB v2)")
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout(); fig.savefig(FIG / "let_band_amp.png", dpi=140)
    plt.close(fig)

    # --- summary JSON ---
    # Median |relative diff| vs published
    diffs = {"lq_alpha": [], "lq_beta": [],
             "ir_alpha_r": [], "ir_alpha_s": [], "ir_dc": []}
    for r in out_rows:
        m = meta.get(r["id"], {})
        for key in diffs:
            pub_raw = m.get(key, "")
            fit_raw = r.get(key, "")
            try:
                pub = float(pub_raw)
                fit = float(fit_raw)
            except Exception:
                continue
            if pub > 0 and fit > 0 and math.isfinite(pub) and math.isfinite(fit):
                diffs[key].append(abs(fit - pub) / pub)

    diff_summary = {k: {"n": len(v),
                         "median_rel_diff": (float(np.median(v)) if v else None),
                         "mean_rel_diff": (float(np.mean(v)) if v else None)}
                    for k, v in diffs.items()}

    summary = {
        "dataset": "Polgár 2022 STOREDB DATASET1252 v2",
        "n_curves_total": len(out_rows),
        "n_curves_LQ_fit": n_lq_ok,
        "n_curves_IR_fit": n_ir_ok,
        "n_curves_with_bootstrap_LQ": n_with_boot_lq,
        "n_curves_with_bootstrap_IR": n_with_boot_ir,
        "bootstrap_B": B_BOOT,
        "n_HRS_positive": len(hrs_curves),
        "n_cell_lines": len(by_cl),
        "n_LET_bands_present": len(band_rows),
        "let_band_counts": {b["let_band"]: b["n_curves"] for b in band_rows},
        "let_band_HRS_positive": {b["let_band"]: b["n_HRS_positive"] for b in band_rows},
        "gof_median_R2_log_LQ": float(np.median(r2_lq)) if r2_lq else None,
        "gof_median_R2_log_IR": float(np.median(r2_ir)) if r2_ir else None,
        "gof_frac_R2_gte_0p95_LQ": float(np.mean(np.array(r2_lq) >= 0.95)) if r2_lq else None,
        "gof_frac_R2_gte_0p95_IR": float(np.mean(np.array(r2_ir) >= 0.95)) if r2_ir else None,
        "frac_IR_beats_LQ_AICc_gt_4": float(np.mean([
            r["delta_aicc_LQ_minus_IR"] > 4 for r in out_rows
            if isinstance(r["delta_aicc_LQ_minus_IR"], float) and math.isfinite(r["delta_aicc_LQ_minus_IR"])
        ])),
        "frac_IR_beats_LQ_BIC_gt_2": float(np.mean([
            r["delta_bic_LQ_minus_IR"] > 2 for r in out_rows
            if isinstance(r["delta_bic_LQ_minus_IR"], float) and math.isfinite(r["delta_bic_LQ_minus_IR"])
        ])),
        "published_vs_fit_relative_diff": diff_summary,
        "mann_whitney_low_vs_high_LET": mw_tests,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2))

    print(f"Wrote {OUT_FITS.relative_to(ROOT)}")
    print(f"Wrote {OUT_CELL.relative_to(ROOT)}")
    print(f"Wrote {OUT_LET.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
