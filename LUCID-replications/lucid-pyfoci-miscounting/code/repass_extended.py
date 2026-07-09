#!/usr/bin/env python3
"""
RE-PASS extended replication for PyFoci miscounting paper.

Targets previously-missed claims:
  C-MW  : Mann-Whitney p-values per Fig 1 cell (vs paper's P_Values_Fig1)
  C-MAG : Magnification effect on % miscount (Fig 4, Airyscan)
  C-VOX : Voxel-size trend across all microscopes (Fig 5)
  C-DEC : Deconvolution effect (Fig 6)
  C-3D  : 3D foci analysis (Fig 7) - 3D still under-counts
  C-CLU : Clustering vs miscount (Fig 8, CD_200nm)
  C-REP : Repair kinetics curves (Fig 3) - normalized to 15 min

Outputs:
  results/repass/*.json, *.csv
  figures/repass/*.png
"""
from __future__ import annotations
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-pyfoci-miscounting")
DATA = ROOT / "data" / "extracted"
RESULTS = ROOT / "results" / "repass"
FIGURES = ROOT / "figures" / "repass"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

AIRY63 = DATA / "080322_dataframe_zstack0_airyscan_63x.parquet"
DECONV = DATA / "deconv" / "080322_dataframe_zstack0_airyscan_63x_deconv"
THREED = DATA / "3D" / "220222_dataframe_zstack3D_airyscan_63x_3D.parquet"

# Paper's bi-exponential model constants (Eq 1)
A1, A2 = 0.711, 0.289
TAU1, TAU2 = 1.54, 10.0  # hours
TIMES_S = [0, 900, 1800, 7200, 21600, 86400]
TIMES_H = [t / 3600 for t in TIMES_S]

# Paper Table 1 (XY, Z, NA) for Airyscan
AIRYSCAN_TABLE1 = {
    "10x":  (0.13, 1.14, 0.45),
    "20x":  (0.059, 0.3, 0.8),
    "40x":  (0.035, 0.15, 1.3),
    "63x":  (0.033, 0.12, 1.4),
    "100x": (0.028, 0.1, 1.46),
}

# Paper Table 1 — voxel = XY*XY*Z (all 23 mag configs)
TABLE1_ALL = {
    "airyscan_10x":  (0.13, 1.14),
    "airyscan_20x":  (0.059, 0.3),
    "airyscan_40x":  (0.035, 0.15),
    "airyscan_63x":  (0.033, 0.12),
    "airyscan_100x": (0.028, 0.1),
    "gSTED_23x":     (0.065, 0.3),   # x23 not x20
    "gSTED_40x":     (0.055, 0.20),
    "gSTED_63x":     (0.042, 0.13),
    "gSTED_100x":    (0.44, 0.13),
    "Lowlight_20x":  (0.21, 0.5),
    "Lowlight_40x":  (0.11, 0.3),
    "Lowlight_100x": (0.043, 0.1),
    "MultiPhoton_10x":  (0.20, 1.0),
    "MultiPhoton_25x":  (0.54, 0.25),  # x25 not x20
    "MultiPhoton_40x":  (0.058, 0.2),
    "MultiPhoton_63x":  (0.044, 0.15),
    "Phenix_20x":  (0.3, 0.8),
    "Phenix_40x":  (0.15, 0.5),
    "Phenix_63x":  (0.095, 0.4),
    "STED_20x":   (0.075, 0.4),
    "STED_25x":   (0.06, 0.25),
    "STED_40x":   (0.045, 0.15),
    "STED_63x":   (0.034, 0.1),
    "STED_100x":  (0.035, 0.1),
}

RAD_LABELS = {
    ("photon",): "Cobalt-60",
    # protons identified by LET
}


def label_row(row):
    """Map row to paper radiation label."""
    if row["Particle"] == "photon":
        return "Cobalt-60"
    let = row["LET_keV/um"]
    # paper buckets: 1.7, 7.15, 27.95 keV/um
    return f"Protons ({let:g} keV/um)"


def pct_miscount(counted, actual):
    """Paper's percentage miscount metric (used in Figs 4, 5, 7, S3, S6).

    pct = (counted - actual) / ((counted + actual) * 0.5) * 100
    """
    denom = (counted.astype(float) + actual.astype(float)) * 0.5
    out = np.where(denom > 0, (counted - actual) / denom * 100.0, np.nan)
    return out


# =============================================================================
# C-MW : Mann-Whitney p-values for Fig 1 (Airyscan x63 DSB-marker, by dose)
# =============================================================================
def claim_mw():
    print("\n== C-MW: Mann-Whitney p-values vs paper's P_Values_Fig1 ==")
    df = pd.read_parquet(AIRY63).copy()
    df["RadLabel"] = df.apply(label_row, axis=1)
    # Foci miscount = counted - actual (per paper Fig 1: miscount values)
    df["Miscount_DSB"] = df["DSBCountedBreaks"] - df["ActualBreaksSlice"]

    # Parse paper's published p-values
    pv_text = (DATA / "Explicit_PValues" / "P_Values_Fig1").read_text()
    # Each dose block separated by ---
    blocks = [b.strip() for b in pv_text.split("---")[1::2]] if "---" in pv_text else []
    # Easier: split on dose headers
    blocks = re.split(r"-{30,}\s*\n([0-9.]+Gy.*?)\n", pv_text)
    # blocks now alternates header/body
    paper_pv = {}  # (dose, A, B) -> p
    for i in range(1, len(blocks) - 1, 2):
        header = blocks[i]
        body = blocks[i + 1]
        m = re.match(r"([0-9.]+)Gy", header)
        if not m:
            continue
        dose = float(m.group(1))
        for line in body.splitlines():
            mm = re.match(
                r"(\d+)_(.+?) v\.s\. (\d+)_(.+?): Mann-Whitney.*?P_val=([0-9.eE+-]+) U_stat=([0-9.eE+-]+)",
                line.strip(),
            )
            if not mm:
                continue
            t1, lab1, t2, lab2, pval, ustat = mm.groups()
            assert t1 == t2, f"time mismatch in line: {line}"
            paper_pv[(dose, int(t1), lab1.strip(), lab2.strip())] = (float(pval), float(ustat))

    print(f"  parsed {len(paper_pv)} paper p-values from P_Values_Fig1")

    # Reproduce each Mann-Whitney test
    n_compare = 0
    n_match_dir = 0   # same significance direction (sig vs not at 0.05)
    n_match_mag = 0   # within 1 order of magnitude
    rows = []
    for (dose, time_s, lab1, lab2), (p_paper, u_paper) in paper_pv.items():
        sub = df[(df["Dose_Gy"] == dose) & (df["Time_s"] == time_s)]
        x = sub[sub["RadLabel"] == lab1]["Miscount_DSB"].dropna().values
        y = sub[sub["RadLabel"] == lab2]["Miscount_DSB"].dropna().values
        if len(x) == 0 or len(y) == 0:
            rows.append(dict(dose=dose, time_s=time_s, lab1=lab1, lab2=lab2,
                             p_paper=p_paper, p_ours=None, u_paper=u_paper, u_ours=None,
                             note=f"missing data: |x|={len(x)} |y|={len(y)}"))
            continue
        res = mannwhitneyu(x, y, alternative="two-sided")
        # Bonferroni correction in paper: each Fig 1 panel has 30 comparisons across 4 doses → per dose: 30 tests
        # But paper-published p is already Bonferroni-adjusted. Count per-dose comparisons:
        n_tests_per_dose = sum(1 for k in paper_pv if k[0] == dose)
        p_adj = min(res.pvalue * n_tests_per_dose, 1.0)
        n_compare += 1
        sig_paper = p_paper <= 0.05
        sig_ours = p_adj <= 0.05
        if sig_paper == sig_ours:
            n_match_dir += 1
        # log10 magnitude check (only when both > 0)
        if p_paper > 0 and p_adj > 0:
            if abs(np.log10(p_paper) - np.log10(p_adj)) <= 1.5:
                n_match_mag += 1
        rows.append(dict(dose=dose, time_s=time_s, lab1=lab1, lab2=lab2,
                         p_paper=p_paper, p_ours=p_adj, u_paper=u_paper, u_ours=res.statistic,
                         n_x=len(x), n_y=len(y), n_tests_per_dose=n_tests_per_dose,
                         sig_paper=int(sig_paper), sig_ours=int(sig_ours)))
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS / "mw_fig1.csv", index=False)
    summary = dict(
        n_paper_tests=len(paper_pv),
        n_reproduced=n_compare,
        n_significance_direction_match=n_match_dir,
        n_within_1p5_orders_of_magnitude=n_match_mag,
        pct_dir_match=round(n_match_dir / n_compare * 100, 1) if n_compare else None,
        pct_mag_match=round(n_match_mag / n_compare * 100, 1) if n_compare else None,
    )
    print("  ", summary)
    (RESULTS / "mw_fig1_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# =============================================================================
# C-MAG : Airyscan magnification effect (Fig 4, 2 Gy, 15 min)
# =============================================================================
def claim_mag():
    print("\n== C-MAG: Airyscan magnification effect at 2 Gy / 15 min ==")
    rows = []
    for mag in ["10x", "20x", "40x", "63x", "100x"]:
        f = DATA / f"080322_dataframe_zstack0_airyscan_{mag}.parquet"
        if not f.exists():
            continue
        df = pd.read_parquet(f)
        sub = df[(df["Dose_Gy"] == 2.0) & (df["Time_s"] == 900)].copy()
        sub["pct_dsb"] = pct_miscount(sub["DSBCountedBreaks"], sub["ActualBreaksSlice"])
        sub["pct_h2ax"] = pct_miscount(sub["H2AXCountedBreaks"], sub["ActualBreaksSlice"])
        xy, z, na = AIRYSCAN_TABLE1[mag]
        rows.append(dict(
            mag=mag, xy=xy, z=z, NA=na, voxel=xy*xy*z, n=len(sub),
            mean_actual_slice=float(sub["ActualBreaksSlice"].mean()),
            median_pct_dsb=float(np.nanmedian(sub["pct_dsb"])),
            mean_pct_dsb=float(np.nanmean(sub["pct_dsb"])),
            median_pct_h2ax=float(np.nanmedian(sub["pct_h2ax"])),
            mean_pct_h2ax=float(np.nanmean(sub["pct_h2ax"])),
        ))
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS / "magnification_airyscan.csv", index=False)
    print(out.to_string(index=False))
    # Paper claim: "10x significant under-counting; >x10 percentage miscount largely preserved"
    pct_10 = out[out["mag"] == "10x"]["median_pct_dsb"].iloc[0] if (out["mag"] == "10x").any() else None
    pct_others = out[out["mag"] != "10x"]["median_pct_dsb"].values
    paper_match = (pct_10 is not None) and (pct_10 < np.min(pct_others)) and (pct_10 < -20)
    summary = dict(
        n_magnifications=len(out),
        median_pct_dsb_10x=pct_10,
        median_pct_dsb_others_min=float(np.min(pct_others)) if len(pct_others) else None,
        median_pct_dsb_others_max=float(np.max(pct_others)) if len(pct_others) else None,
        spread_others=float(np.max(pct_others) - np.min(pct_others)) if len(pct_others) else None,
        paper_qualitative_match=bool(paper_match),
    )
    print("  ", summary)
    (RESULTS / "magnification_airyscan_summary.json").write_text(json.dumps(summary, indent=2))

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(out["mag"], out["median_pct_dsb"], color="#3b7", label="DSB-marker median % miscount")
    ax.bar(out["mag"], out["median_pct_h2ax"], color="#d63", alpha=0.5, label="γ-H2AX-marker median % miscount")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("Airyscan magnification")
    ax.set_ylabel("median % foci miscount")
    ax.set_title("Fig 4 reproduction (Airyscan, 2 Gy, 15 min)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "fig4_airyscan_mag.png", dpi=150)
    plt.close()
    return summary


# =============================================================================
# C-VOX : Voxel-size trend across all microscope/mag configs (Fig 5, 2 Gy)
# =============================================================================
def claim_vox():
    print("\n== C-VOX: voxel-size vs % miscount across all 23 configs (Fig 5) ==")
    rows = []
    for key, (xy, z) in TABLE1_ALL.items():
        # Filenames use lowercase 'airyscan' but capitalized everything else
        f = DATA / f"080322_dataframe_zstack0_{key}.parquet"
        if not f.exists():
            continue
        df = pd.read_parquet(f)
        sub = df[df["Dose_Gy"] == 2.0].copy()  # all time points
        sub["pct_dsb"] = pct_miscount(sub["DSBCountedBreaks"], sub["ActualBreaksSlice"])
        sub["pct_h2ax"] = pct_miscount(sub["H2AXCountedBreaks"], sub["ActualBreaksSlice"])
        rows.append(dict(
            config=key, voxel_um3=xy*xy*z, n=len(sub),
            mean_pct_dsb=float(np.nanmean(sub["pct_dsb"])),
            sem_pct_dsb=float(np.nanstd(sub["pct_dsb"]) / np.sqrt(len(sub))),
            mean_pct_h2ax=float(np.nanmean(sub["pct_h2ax"])),
            sem_pct_h2ax=float(np.nanstd(sub["pct_h2ax"]) / np.sqrt(len(sub))),
        ))
    out = pd.DataFrame(rows).sort_values("voxel_um3")
    out.to_csv(RESULTS / "voxel_trend.csv", index=False)
    # Paper claim: "negative relationship between voxel size and % foci miscount"
    from scipy.stats import spearmanr
    r_dsb, p_dsb = spearmanr(out["voxel_um3"], out["mean_pct_dsb"])
    r_h2ax, p_h2ax = spearmanr(out["voxel_um3"], out["mean_pct_h2ax"])
    summary = dict(
        n_configs=len(out),
        spearman_voxel_vs_pct_dsb=dict(r=float(r_dsb), p=float(p_dsb)),
        spearman_voxel_vs_pct_h2ax=dict(r=float(r_h2ax), p=float(p_h2ax)),
        paper_claim="negative relationship voxel vs % miscount",
        paper_qualitative_match=bool(r_dsb < 0),
    )
    print("  ", summary)
    (RESULTS / "voxel_trend_summary.json").write_text(json.dumps(summary, indent=2))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(out["voxel_um3"], out["mean_pct_dsb"], yerr=out["sem_pct_dsb"], fmt="o", label="DSB", color="#3b7")
    ax.errorbar(out["voxel_um3"], out["mean_pct_h2ax"], yerr=out["sem_pct_h2ax"], fmt="s", label="γ-H2AX", color="#d63")
    ax.set_xscale("log")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("voxel size (µm³, log)")
    ax.set_ylabel("mean % foci miscount")
    ax.set_title("Fig 5 reproduction (all configs, 2 Gy)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "fig5_voxel.png", dpi=150)
    plt.close()
    return summary


# =============================================================================
# C-DEC : Deconvolution effect (Fig 6, Airyscan x63, 1 Gy)
# =============================================================================
def claim_dec():
    print("\n== C-DEC: deconvolution effect at 1 Gy (Fig 6) ==")
    df_raw = pd.read_parquet(AIRY63)
    df_dec = pd.read_parquet(DECONV)

    rows = []
    for t_s in (1800, 86400):  # 30 min and 24 h per paper
        for particle, let in [("photon", None), ("proton", 1.7), ("proton", 7.15), ("proton", 27.95)]:
            mask_raw = (df_raw["Dose_Gy"] == 1.0) & (df_raw["Time_s"] == t_s) & (df_raw["Particle"] == particle)
            mask_dec = (df_dec["Dose_Gy"] == 1.0) & (df_dec["Time_s"] == t_s) & (df_dec["Particle"] == particle)
            if let is not None:
                mask_raw &= np.isclose(df_raw["LET_keV/um"], let)
                mask_dec &= np.isclose(df_dec["LET_keV/um"], let)
            sub_raw = df_raw[mask_raw]
            sub_dec = df_dec[mask_dec]
            if len(sub_raw) == 0 or len(sub_dec) == 0:
                continue
            actual = sub_raw["ActualBreaksSlice"].mean()
            dsb_raw = sub_raw["DSBCountedBreaks"].mean()
            h2_raw = sub_raw["H2AXCountedBreaks"].mean()
            dsb_dec = sub_dec["DSBCountedBreaks"].mean()
            h2_dec = sub_dec["H2AXCountedBreaks"].mean()
            label = "Co60" if particle == "photon" else f"P{let}"
            rows.append(dict(
                time_s=t_s, label=label,
                mean_actual=float(actual),
                mean_dsb_raw=float(dsb_raw), mean_h2ax_raw=float(h2_raw),
                mean_dsb_dec=float(dsb_dec), mean_h2ax_dec=float(h2_dec),
                abs_err_dsb_raw=float(abs(dsb_raw - actual)),
                abs_err_h2_raw=float(abs(h2_raw - actual)),
                abs_err_dsb_dec=float(abs(dsb_dec - actual)),
                abs_err_h2_dec=float(abs(h2_dec - actual)),
            ))
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS / "deconv.csv", index=False)
    print(out.to_string(index=False))

    # Paper claims tested:
    #  (a) deconvolved versions give better agreement than non-deconvolved (lower abs err)
    #  (b) at 24h, deconvolved DSB gives best agreement among all 4 visualisations across radiation types
    n_pairs = len(out)
    better_dsb = int((out["abs_err_dsb_dec"] < out["abs_err_dsb_raw"]).sum())
    better_h2 = int((out["abs_err_h2_dec"] < out["abs_err_h2_raw"]).sum())

    # 24h-only check: deconvolved DSB best of {DSB raw, H2AX raw, DSB dec, H2AX dec}
    out24 = out[out["time_s"] == 86400]
    dsb_dec_best = 0
    for _, r in out24.iterrows():
        errs = {"dsb_raw": r.abs_err_dsb_raw, "h2_raw": r.abs_err_h2_raw,
                "dsb_dec": r.abs_err_dsb_dec, "h2_dec": r.abs_err_h2_dec}
        if min(errs, key=errs.get) == "dsb_dec":
            dsb_dec_best += 1
    summary = dict(
        n_groups=n_pairs,
        dsb_deconv_better_than_raw=better_dsb,
        h2ax_deconv_better_than_raw=better_h2,
        n_24h_groups=len(out24),
        n_24h_groups_where_dsb_dec_is_best=int(dsb_dec_best),
        paper_claim_a_match=bool(better_dsb >= 0.6 * n_pairs),
        paper_claim_b_match=bool(dsb_dec_best == len(out24)),
    )
    print("  ", summary)
    (RESULTS / "deconv_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# =============================================================================
# C-3D : 3D foci analysis (Fig 7, Airyscan x63, 1 Gy)
# =============================================================================
def claim_3d():
    print("\n== C-3D: 3D foci analysis (Fig 7) ==")
    df3 = pd.read_parquet(THREED)
    df2 = pd.read_parquet(AIRY63)

    rows = []
    # Paper Fig 7: 1 Gy at 30 min (1800s) and 24h (86400s)
    for t_s in (1800, 86400):
        for particle, let in [("photon", None), ("proton", 1.7), ("proton", 7.15), ("proton", 27.95)]:
            mask3 = (df3["Dose_Gy"] == 1.0) & (df3["Time_s"] == t_s) & (df3["Particle"] == particle)
            mask2 = (df2["Dose_Gy"] == 1.0) & (df2["Time_s"] == t_s) & (df2["Particle"] == particle)
            if let is not None:
                mask3 &= np.isclose(df3["LET_keV/um"], let)
                mask2 &= np.isclose(df2["LET_keV/um"], let)
            s3 = df3[mask3]
            s2 = df2[mask2]
            if len(s3) == 0 or len(s2) == 0:
                continue
            actual = s3["ActualBreaksCell"].mean()  # 3D = whole cell
            dsb3 = s3["DSBCountedBreaks"].mean()
            h23 = s3["H2AXCountedBreaks"].mean()
            actual2 = s2["ActualBreaksSlice"].mean()
            dsb2 = s2["DSBCountedBreaks"].mean()
            label = "Co60" if particle == "photon" else f"P{let}"
            rows.append(dict(
                time_s=t_s, label=label, let=let, n3=len(s3), n2=len(s2),
                actual_cell_3d=float(actual), counted_dsb_3d=float(dsb3), counted_h2ax_3d=float(h23),
                pct_miscount_dsb_3d=float((dsb3 - actual) / ((dsb3 + actual) * 0.5) * 100) if (dsb3 + actual) > 0 else None,
                pct_miscount_h2ax_3d=float((h23 - actual) / ((h23 + actual) * 0.5) * 100) if (h23 + actual) > 0 else None,
                actual_slice_2d=float(actual2), counted_dsb_2d=float(dsb2),
            ))
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS / "threeD.csv", index=False)
    print(out.to_string(index=False))

    # Paper claims:
    #  (a) at 30 min all 3D analyses under-count (pct < 0)
    #  (b) under-counting severity increases with LET in 30-min proton runs
    #  (c) at 24h Ku/DNA-PKcs (DSB) marker 3D matches actual well except at high LET
    out30 = out[out["time_s"] == 1800]
    out24 = out[out["time_s"] == 86400]
    n30_undercount_dsb = int((out30["pct_miscount_dsb_3d"] < 0).sum())

    # LET monotonic in protons at 30 min
    p30 = out30[out30["let"].notna()].sort_values("let")
    let_severity_monotone = bool(len(p30) >= 2 and all(
        p30["pct_miscount_dsb_3d"].iloc[i] >= p30["pct_miscount_dsb_3d"].iloc[i + 1]
        for i in range(len(p30) - 1)
    ))  # more negative as LET goes up

    # 24h DSB low-LET well matched (|pct| < 30%)
    out24_lowlet = out24[(out24["let"].isna()) | (out24["let"] < 10)]
    out24_highlet = out24[out24["let"] >= 10]
    n24_low_match = int((out24_lowlet["pct_miscount_dsb_3d"].abs() < 30).sum())
    n24_high_undercount = int((out24_highlet["pct_miscount_dsb_3d"] < -10).sum())

    summary = dict(
        n_30min_groups=len(out30),
        n_30min_dsb_undercounting=n30_undercount_dsb,
        let_severity_monotone_at_30min=let_severity_monotone,
        n_24h_lowLET_groups=len(out24_lowlet),
        n_24h_lowLET_dsb_within_30pct=n24_low_match,
        n_24h_highLET_groups=len(out24_highlet),
        n_24h_highLET_dsb_undercount_more_than_10pct=n24_high_undercount,
        paper_qualitative_match=bool(
            n30_undercount_dsb == len(out30)
            and let_severity_monotone
            and n24_low_match >= 0.5 * max(len(out24_lowlet), 1)
            and n24_high_undercount >= 0.5 * max(len(out24_highlet), 1)
        ),
    )
    print("  ", summary)
    (RESULTS / "threeD_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# =============================================================================
# C-CLU : Clustering vs miscount (Fig 8, CD_200nm)
# =============================================================================
def claim_clu():
    print("\n== C-CLU: clustering (CD_200nm) vs miscount (Fig 8) ==")
    df = pd.read_parquet(AIRY63).copy()
    df["abs_mis_dsb"] = (df["DSBCountedBreaks"] - df["ActualBreaksSlice"])
    df["abs_mis_h2ax"] = (df["H2AXCountedBreaks"] - df["ActualBreaksSlice"])

    # Drop where no DSBs (CD_200nm is NaN/0)
    mask = df["ActualBreaksSlice"] > 0
    sub = df[mask].copy()
    # Bin clustering values
    bins = [0, 1.5, 2.5, 5, 10, 50, np.inf]
    labels = ["1.0-1.5", "1.5-2.5", "2.5-5", "5-10", "10-50", ">50"]
    sub["clust_bin"] = pd.cut(sub["CD_200nm"], bins=bins, labels=labels, include_lowest=True)
    grouped = sub.groupby("clust_bin", observed=False).agg(
        n=("abs_mis_dsb", "count"),
        median_mis_dsb=("abs_mis_dsb", "median"),
        mean_mis_dsb=("abs_mis_dsb", "mean"),
        median_mis_h2ax=("abs_mis_h2ax", "median"),
        mean_mis_h2ax=("abs_mis_h2ax", "mean"),
    ).reset_index()
    grouped.to_csv(RESULTS / "clustering.csv", index=False)
    print(grouped.to_string(index=False))

    # Paper Fig 8a/b claim: increased clustering -> increased under-counting
    from scipy.stats import spearmanr
    r_dsb, p_dsb = spearmanr(sub["CD_200nm"], sub["abs_mis_dsb"])
    r_h2ax, p_h2ax = spearmanr(sub["CD_200nm"], sub["abs_mis_h2ax"])
    summary = dict(
        n_rows=int(len(sub)),
        spearman_clust_vs_dsb_miscount=dict(r=float(r_dsb), p=float(p_dsb)),
        spearman_clust_vs_h2ax_miscount=dict(r=float(r_h2ax), p=float(p_h2ax)),
        paper_claim_dsb_undercount_with_clustering=bool(r_dsb < 0),
        paper_claim_h2ax_smaller_effect=bool(abs(r_h2ax) < abs(r_dsb)),
    )
    print("  ", summary)
    (RESULTS / "clustering_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# =============================================================================
# C-REP : Repair kinetics curves (Fig 3, Airyscan x63, 2 Gy, normalized to 15 min)
# =============================================================================
def claim_rep():
    print("\n== C-REP: repair kinetics normalized to 15 min (Fig 3) ==")
    df = pd.read_parquet(AIRY63).copy()
    df["RadLabel"] = df.apply(label_row, axis=1)
    sub = df[df["Dose_Gy"] == 2.0]
    grp = sub.groupby(["RadLabel", "Time_s"]).agg(
        actual=("ActualBreaksSlice", "mean"),
        dsb=("DSBCountedBreaks", "mean"),
        h2ax=("H2AXCountedBreaks", "mean"),
    ).reset_index()

    def normalize(d):
        ref_actual = d[d["Time_s"] == 900]["actual"].iloc[0]
        ref_dsb = d[d["Time_s"] == 900]["dsb"].iloc[0]
        ref_h2 = d[d["Time_s"] == 900]["h2ax"].iloc[0]
        d = d.copy()
        d["frac_actual"] = d["actual"] / ref_actual
        d["frac_dsb"] = d["dsb"] / ref_dsb
        d["frac_h2ax"] = d["h2ax"] / ref_h2
        return d

    pieces = []
    for lab, gdf in grp.groupby("RadLabel"):
        pieces.append(normalize(gdf.sort_values("Time_s")))
    norm = pd.concat(pieces, ignore_index=True)
    norm.to_csv(RESULTS / "kinetics.csv", index=False)

    # Paper bi-exp model normalized to t=15min
    def biexp(t_h):
        return A1 * np.exp(-t_h / TAU1) + A2 * np.exp(-t_h / TAU2)

    t_h = np.array(TIMES_H)
    bi_norm = biexp(t_h) / biexp(0.25)  # normalize to 15 min
    bi_df = pd.DataFrame(dict(Time_s=TIMES_S, biexp_norm=bi_norm))

    # Compare actual fractions to bi-exp model
    diffs = []
    for lab in norm["RadLabel"].unique():
        d = norm[norm["RadLabel"] == lab].set_index("Time_s").reindex(TIMES_S)
        diff = (d["frac_actual"].values - bi_norm)
        diffs.append(dict(RadLabel=lab, max_abs_diff=float(np.nanmax(np.abs(diff))),
                          rmse=float(np.sqrt(np.nanmean(diff**2)))))
    diffs_df = pd.DataFrame(diffs)
    diffs_df.to_csv(RESULTS / "kinetics_vs_biexp.csv", index=False)
    print(diffs_df.to_string(index=False))

    # Paper claim: actual repair (panel a) is the SAME bi-exponential across all radiation types
    # (it's enforced as constant in simulation)
    actual_max_diff = float(diffs_df["max_abs_diff"].max())
    paper_match = actual_max_diff < 0.10  # within 10% of bi-exp curve

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    colors = {"Cobalt-60": "tab:blue", "Protons (1.7 keV/um)": "tab:orange",
              "Protons (7.15 keV/um)": "tab:green", "Protons (27.95 keV/um)": "tab:red"}
    for lab in norm["RadLabel"].unique():
        d = norm[norm["RadLabel"] == lab].sort_values("Time_s")
        t_disp = d["Time_s"] / 3600
        c = colors.get(lab, "k")
        axes[0].plot(t_disp, d["frac_actual"], "o-", color=c, label=lab)
        axes[1].plot(t_disp, d["frac_dsb"], "o-", color=c)
        axes[2].plot(t_disp, d["frac_h2ax"], "o-", color=c)
    axes[0].plot(t_h, bi_norm, "k--", label="bi-exp model", alpha=0.7)
    for ax, title in zip(axes, ["a) actual DSBs", "b) DSB-marker", "c) γ-H2AX-marker"]):
        ax.set_xlabel("time (h)")
        ax.set_xscale("symlog", linthresh=0.5)
        ax.set_title(title)
    axes[0].set_ylabel("fraction remaining (norm. 15 min)")
    axes[0].legend(fontsize=7)
    plt.suptitle("Fig 3 reproduction (Airyscan x63, 2 Gy)")
    plt.tight_layout()
    plt.savefig(FIGURES / "fig3_kinetics.png", dpi=150)
    plt.close()

    summary = dict(
        n_radiation_groups=int(norm["RadLabel"].nunique()),
        biexp_norm_at_times_hours=dict(zip(TIMES_H, [float(x) for x in bi_norm])),
        actual_max_abs_diff_vs_biexp=actual_max_diff,
        paper_actual_matches_constant_biexp=bool(paper_match),
    )
    print("  ", summary)
    (RESULTS / "kinetics_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# =============================================================================
if __name__ == "__main__":
    out = {}
    out["C-MW_Fig1_pvalues"] = claim_mw()
    out["C-MAG_Fig4_magnification"] = claim_mag()
    out["C-VOX_Fig5_voxel"] = claim_vox()
    out["C-DEC_Fig6_deconv"] = claim_dec()
    out["C-3D_Fig7_3D_analysis"] = claim_3d()
    out["C-CLU_Fig8_clustering"] = claim_clu()
    out["C-REP_Fig3_repair_kinetics"] = claim_rep()
    (RESULTS / "ALL_CLAIMS_SUMMARY.json").write_text(json.dumps(out, indent=2))
    print("\n=== ALL DONE ===")
    print(f"Results in {RESULTS}")
    print(f"Figures in {FIGURES}")
