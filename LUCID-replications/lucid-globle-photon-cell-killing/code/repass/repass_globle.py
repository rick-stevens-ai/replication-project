#!/usr/bin/env python3
"""
Re-pass for the GLOBLE photon-cell-killing replication.

Goal: lift coverage by reproducing claims that pass 1 left untested:

  C-A. All-17-cell-line Table-2 sanity (ε_i ≤ ε_c, HLT_i median, parameter
       coherence) — reproduces the paper's text claim that "ε_i is always
       << ε_c" and "median HLT_i = 0.458 h".
  C-B. Dose-rate survival curves for the OTHER cell lines (HX138, HX142,
       C3H 10T1/2, HX118, HX32, HX58, LL, B16, HX34, IN859, IN1265, SB,
       NFF28, CHO 10B2, CHO K1) — pass 1 only plotted RT112/MT.
  C-C. Split-dose survival curves for the 5 cell lines with split-dose
       parameters in Table 2 (MT, LL, B16, HX34, CHO 10B2) — pass 1 only
       plotted MT.
  C-D. Table 3 reproduction: the GLOBLE dose-rate and split-dose HLT_i
       column values are exactly the HLT_i parameters from Table 2 — verify
       row-by-row.
  C-E. Analytical limits across multiple cell lines: numerically confirm
       (a) high-dose-rate ODE → static GLOBLE (Eqs. 6-7) and
       (b) low-dose-rate ODE → closed-form Eq. 38.
  C-F. Eq. (8) Taylor identity: α = ε_i * α_DSB for every Table-2 entry,
       checked by survival-curve slope at low dose at high dose rate.

Compute: CherryRd CPU only. No GPU. No network. No fabrication: every
number is computed from the implemented ODE/closed-form expressions.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "code"))

from globle import (
    GlobleParams,
    survival_single_dose,
    survival_static,
    survival_split_dose,
    survival_low_dose_rate_closed_form,
    ALPHA_DSB,
)
from cell_lines import CELL_LINES, DOSE_RATES

OUT_RES = REPO / "results" / "repass"
OUT_FIG = REPO / "figures" / "repass"
OUT_RES.mkdir(parents=True, exist_ok=True)
OUT_FIG.mkdir(parents=True, exist_ok=True)


def _mk(p):
    return GlobleParams(eps_i=p.eps_i, eps_c=p.eps_c, hlt_i=p.hlt_i)


# ---------------- C-A. Table-2 sanity ---------------- #

def claim_A_table2_sanity():
    rows = []
    eps_i_le_eps_c = True
    hlt_i_values = []
    for cl, sets in CELL_LINES.items():
        for col, ps in sets.items():
            row = {
                "cell_line": cl,
                "column": col,
                "eps_i": ps.eps_i,
                "eps_c": ps.eps_c,
                "hlt_i_h": ps.hlt_i,
                "eps_i_lt_eps_c": ps.eps_i < ps.eps_c,
            }
            rows.append(row)
            hlt_i_values.append(ps.hlt_i)
            if not row["eps_i_lt_eps_c"]:
                eps_i_le_eps_c = False
    median_hlt_all = statistics.median(hlt_i_values)
    dr_vals = [sets["dose_rate"].hlt_i for sets in CELL_LINES.values() if "dose_rate" in sets]
    sp_vals = [sets["split"].hlt_i     for sets in CELL_LINES.values() if "split" in sets]
    median_dr  = statistics.median(dr_vals)
    median_sp  = statistics.median(sp_vals)
    out = {
        "claim": "Table 2 self-consistency",
        "n_param_sets": len(rows),
        "n_cell_lines": len(CELL_LINES),
        "all_eps_i_lt_eps_c": eps_i_le_eps_c,
        "median_HLT_i_h_all_22_param_sets":   median_hlt_all,
        "median_HLT_i_h_dose_rate_column_17": median_dr,
        "median_HLT_i_h_split_dose_column_5": median_sp,
        "paper_claimed_median_HLT_i_h": 0.458,
        "paper_median_matches_split_dose_column": abs(median_sp - 0.458) < 0.005,
        "rows": rows,
    }
    (OUT_RES / "claim_A_table2.json").write_text(json.dumps(out, indent=2))
    return out


# ---------------- C-B. Dose-rate curves for all cell lines ---------------- #

def claim_B_dose_rate_curves():
    doses = np.linspace(0.05, 14.0, 60)
    summary = {}
    cell_lines = [cl for cl, sets in CELL_LINES.items() if "dose_rate" in sets]
    # one big multi-panel figure
    ncols = 4
    nrows = int(np.ceil(len(cell_lines) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows),
                             sharey=True)
    axes = axes.ravel()
    for i, cl in enumerate(cell_lines):
        ax = axes[i]
        ps = CELL_LINES[cl]["dose_rate"]
        p = _mk(ps)
        rates = DOSE_RATES.get(cl, [])
        rates_sorted = sorted(rates, reverse=True)
        per_line = {}
        for r in rates_sorted:
            s = np.array([survival_single_dose(p, d, r) for d in doses])
            ax.plot(doses, s, label=f"{r:g} Gy/h")
            per_line[f"{r:g} Gy/h"] = {
                "doses_gy": doses.tolist(),
                "survival": s.tolist(),
                "S_at_2Gy": float(survival_single_dose(p, 2.0, r)),
                "S_at_8Gy": float(survival_single_dose(p, 8.0, r)),
            }
        ax.set_yscale("log")
        ax.set_ylim(1e-6, 1.2)
        ax.set_xlim(0, 14)
        ax.set_title(f"{cl}\nε_i={ps.eps_i:g} ε_c={ps.eps_c:g} HLT_i={ps.hlt_i:g}h",
                     fontsize=8)
        ax.legend(fontsize=6, loc="lower left")
        ax.grid(True, which="both", alpha=0.3)
        ax.set_xlabel("Dose [Gy]")
        if i % ncols == 0:
            ax.set_ylabel("Survival")
        summary[cl] = {
            "eps_i": ps.eps_i, "eps_c": ps.eps_c, "hlt_i_h": ps.hlt_i,
            "dose_rates_gy_per_h": rates_sorted,
            "per_dose_rate": per_line,
            "monotonic_in_dose": all(
                all(per_line[k]["survival"][j] >= per_line[k]["survival"][j+1] - 1e-12
                    for j in range(len(doses)-1)) for k in per_line
            ),
        }
    # hide unused panels
    for j in range(len(cell_lines), nrows * ncols):
        axes[j].axis("off")
    fig.suptitle("GLOBLE dose-rate survival families — all Table-2 cell lines",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUT_FIG / "dose_rate_all_cell_lines.png", dpi=130)
    plt.close(fig)
    (OUT_RES / "claim_B_dose_rate_all.json").write_text(json.dumps(summary, indent=2))
    # how many cell lines have monotonic-in-dose survival at every dose rate?
    n_mono = sum(1 for v in summary.values() if v["monotonic_in_dose"])
    return {"cell_lines_plotted": list(summary.keys()),
            "n_cell_lines": len(summary),
            "n_monotonic": n_mono}


# ---------------- C-C. Split-dose curves for all split-dose cell lines ---------------- #

def claim_C_split_dose_curves():
    cell_lines = [cl for cl, sets in CELL_LINES.items() if "split" in sets]
    ts = np.concatenate([np.array([0.0]), np.logspace(-2, 1.5, 60)])
    # canonical split doses for each cell line (paper uses 5+5 Gy and 6+6 Gy
    # for MT/LL/B16/HX34/CHO 10B2 — paper Fig 3 caption + text Sec. "Split dose")
    splits_per_cl = {
        "MT":       [5.0, 6.0],
        "LL":       [5.0],
        "B16":      [5.0, 6.0],
        "HX34":     [5.0, 6.0],
        "CHO 10B2": [5.0, 6.0],
    }
    summary = {}
    fig, axes = plt.subplots(1, len(cell_lines),
                             figsize=(3.5 * len(cell_lines), 3.5), sharey=True)
    if len(cell_lines) == 1:
        axes = [axes]
    for ax, cl in zip(axes, cell_lines):
        ps = CELL_LINES[cl]["split"]
        p = _mk(ps)
        per_d = {}
        for d in splits_per_cl.get(cl, [5.0]):
            s = np.array([survival_split_dose(p, d, t) for t in ts])
            ax.plot(ts, s, label=f"{d:g}+{d:g} Gy")
            per_d[f"{d:g}+{d:g}_Gy"] = {
                "t1_h": ts.tolist(),
                "survival": s.tolist(),
                "S_at_t1=0h":  float(survival_split_dose(p, d, 0.0)),
                "S_at_t1=2h":  float(survival_split_dose(p, d, 2.0)),
                "S_at_t1=10h": float(survival_split_dose(p, d, 10.0)),
            }
        ax.set_yscale("log")
        ax.set_xscale("symlog", linthresh=0.05)
        ax.set_xlim(0, 30)
        ax.set_xlabel("Separation time t₁ [h]")
        ax.set_title(f"{cl}\nε_i={ps.eps_i:g} ε_c={ps.eps_c:g} HLT_i={ps.hlt_i:g}h",
                     fontsize=8)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=7)
        # recovery check: S(t1=10h) >= S(t1=0)
        d_test = splits_per_cl.get(cl, [5.0])[0]
        s0 = survival_split_dose(p, d_test, 0.0)
        s10 = survival_split_dose(p, d_test, 10.0)
        summary[cl] = {
            "eps_i": ps.eps_i, "eps_c": ps.eps_c, "hlt_i_h": ps.hlt_i,
            "doses_tested": splits_per_cl.get(cl, [5.0]),
            "per_dose": per_d,
            "recovers": s10 > s0 + 1e-12,
            "S(t1=0)": s0, "S(t1=10h)": s10, "recovery_factor": s10 / s0,
        }
    axes[0].set_ylabel("Survival")
    fig.suptitle("GLOBLE split-dose recovery — all Table-2 split-dose cell lines",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_FIG / "split_dose_all_cell_lines.png", dpi=130)
    plt.close(fig)
    (OUT_RES / "claim_C_split_dose_all.json").write_text(json.dumps(summary, indent=2))
    return {"cell_lines_plotted": list(summary.keys()),
            "all_recover": all(v["recovers"] for v in summary.values())}


# ---------------- C-D. Table 3 reproduction ---------------- #

def claim_D_table3():
    paper_table3 = {
        # cl: (exp_HLT, GLOBLE_dose_rate, GLOBLE_split_dose)
        "CHO 10B2": (1.17, 6.10, 1.34),
        "HX118":    (0.42, 0.24, None),
        "HX32":     (2.02, 5.69, None),
        "HX58":     (1.42, 0.94, None),
        "MT":       (0.19, 0.09, 0.29),
        "LL":       (0.61, 0.10, 0.46),
        "B16":      (0.16, 0.13, 0.15),
        "HX34":     (0.97, 0.13, 1.10),
        "RT112":    (0.93, 0.48, None),
        "HX138":    (1.00, 1.18, None),
        "HX142":    (1.60, 1.08, None),
    }
    rows = []
    for cl, (exp_hlt, gd, gs) in paper_table3.items():
        sets = CELL_LINES[cl]
        dr_hlt = round(sets["dose_rate"].hlt_i, 2) if "dose_rate" in sets else None
        sp_hlt = round(sets["split"].hlt_i, 2) if "split" in sets else None
        row = {
            "cell_line": cl,
            "paper_exp_HLT_h": exp_hlt,
            "paper_GLOBLE_dose_rate_HLT_h": gd,
            "paper_GLOBLE_split_dose_HLT_h": gs,
            "our_table2_dose_rate_HLT_h": dr_hlt,
            "our_table2_split_dose_HLT_h": sp_hlt,
            "dose_rate_match": (gd is None) or (dr_hlt is None) or abs(dr_hlt - gd) <= max(0.01, 0.05 * gd),
            "split_dose_match": (gs is None) == (sp_hlt is None) and (gs is None or abs(sp_hlt - gs) <= max(0.02, 0.05 * gs)),
        }
        rows.append(row)
    n_dr_match = sum(1 for r in rows if r["dose_rate_match"])
    n_sp_match = sum(1 for r in rows if r["split_dose_match"])
    out = {
        "claim": "Table 3 reproduction: GLOBLE HLT_i columns equal Table 2 HLT_i",
        "rows": rows,
        "n_rows": len(rows),
        "n_dose_rate_match": n_dr_match,
        "n_split_dose_match": n_sp_match,
    }
    (OUT_RES / "claim_D_table3.json").write_text(json.dumps(out, indent=2))
    return out


# ---------------- C-E. Analytical limits ---------------- #

def claim_E_limits():
    """High-dose-rate ODE survival ≈ static GLOBLE; low-dose-rate ODE survival
    ≈ closed-form Eq. 38."""
    out_hi = []
    out_lo = []
    test_doses = [2.0, 5.0, 10.0]
    for cl, sets in CELL_LINES.items():
        ps = sets["dose_rate"]
        p = _mk(ps)
        # high dose-rate: 1e6 Gy/h => 10 Gy in 36 µs, well below all HLT_i
        # (smallest HLT_i in Table 2 is 0.035 h = 126 s for CHO K1)
        for d in test_doses:
            S_ode = survival_single_dose(p, d, 1.0e6)
            S_stat = survival_static(p, d)
            # relative err where possible, abs in log space otherwise
            denom = max(abs(S_stat), 1e-300)
            rel = abs(S_ode - S_stat) / denom
            # for very small S compare -log
            logL_ode = -np.log(max(S_ode, 1e-300))
            logL_st  = -np.log(max(S_stat, 1e-300))
            ldiff = abs(logL_ode - logL_st)
            out_hi.append({
                "cell_line": cl, "dose_gy": d,
                "dose_rate_gy_per_h": 1e6,
                "S_ode": S_ode, "S_static": S_stat,
                "rel_err": rel, "abs_log_err": ldiff,
            })
        # low dose-rate: pick small rate
        for d in test_doses:
            r_lo = 1.0e-3  # 1 mGy/h-ish in this paper
            S_ode = survival_single_dose(p, d, r_lo)
            S_cf  = survival_low_dose_rate_closed_form(p, d, r_lo)
            logL_ode = -np.log(max(S_ode, 1e-300))
            logL_cf  = -np.log(max(S_cf, 1e-300))
            ldiff = abs(logL_ode - logL_cf)
            rel = abs(logL_ode - logL_cf) / max(logL_cf, 1e-12)
            out_lo.append({
                "cell_line": cl, "dose_gy": d,
                "dose_rate_gy_per_h": r_lo,
                "S_ode": S_ode, "S_closed_form_eq38": S_cf,
                "abs_log_err": ldiff, "rel_log_err": rel,
            })
    max_hi = float(max(x["abs_log_err"] for x in out_hi))
    max_lo = float(max(x["abs_log_err"] for x in out_lo))
    out = {
        "claim": "High-dose-rate ODE → static GLOBLE (Eqs 6-7); low-dose-rate ODE → Eq. 38",
        "max_abs_log_err_high_dose_rate": max_hi,
        "max_abs_log_err_low_dose_rate":  max_lo,
        "tolerance_log_err": 0.05,
        "high_pass": bool(max_hi < 0.05),
        "low_pass":  bool(max_lo < 0.05),
        "high_dose_rate_detail": out_hi,
        "low_dose_rate_detail":  out_lo,
    }
    (OUT_RES / "claim_E_limits.json").write_text(json.dumps(out, indent=2))
    return out


# ---------------- C-F. Eq. (8): α = ε_i * α_DSB ---------------- #

def claim_F_alpha_taylor():
    """At small dose & high dose rate, -ln(S) ≈ α D with α = ε_i * α_DSB.
    Verify by finite-difference slope at D=0.01 Gy, rate=1e4 Gy/h."""
    rows = []
    d_eps = 1e-3  # Gy
    rate = 1.0e4  # high to suppress repair
    for cl, sets in CELL_LINES.items():
        ps = sets["dose_rate"]
        p = _mk(ps)
        alpha_expected = ps.eps_i * ALPHA_DSB
        S = survival_single_dose(p, d_eps, rate)
        alpha_measured = -np.log(S) / d_eps
        rel = abs(alpha_measured - alpha_expected) / max(abs(alpha_expected), 1e-12)
        rows.append({
            "cell_line": cl,
            "eps_i": ps.eps_i,
            "alpha_expected_per_Gy": alpha_expected,
            "alpha_measured_per_Gy": alpha_measured,
            "rel_err": rel,
        })
    max_err = float(max(r["rel_err"] for r in rows))
    out = {
        "claim": "Eq. (8): α_initial = ε_i * α_DSB across all cell lines",
        "max_rel_err": max_err,
        "tolerance": 0.05,
        "pass": bool(max_err < 0.05),
        "rows": rows,
    }
    (OUT_RES / "claim_F_alpha_taylor.json").write_text(json.dumps(out, indent=2))
    return out


# ---------------- main ---------------- #

if __name__ == "__main__":
    print(">> Claim A: Table 2 sanity")
    A = claim_A_table2_sanity()
    print(f"   n_param_sets={A['n_param_sets']}, "
          f"all eps_i<eps_c={A['all_eps_i_lt_eps_c']}, "
          f"median(split-dose col)={A['median_HLT_i_h_split_dose_column_5']:.3f}h "
          f"(paper says 0.458h => match={A['paper_median_matches_split_dose_column']})")

    print(">> Claim B: dose-rate curves for all cell lines")
    B = claim_B_dose_rate_curves()
    print(f"   n_cell_lines={B['n_cell_lines']}, n_monotonic={B['n_monotonic']}")

    print(">> Claim C: split-dose curves for all cell lines with split params")
    C = claim_C_split_dose_curves()
    print(f"   cell_lines={C['cell_lines_plotted']}, "
          f"all recover plateau={C['all_recover']}")

    print(">> Claim D: Table 3 reproduction (HLT_i columns == Table 2)")
    D = claim_D_table3()
    print(f"   dose-rate match {D['n_dose_rate_match']}/{D['n_rows']}, "
          f"split-dose match {D['n_split_dose_match']}/{D['n_rows']}")

    print(">> Claim E: analytical limits across cell lines")
    E = claim_E_limits()
    print(f"   high-DR max |Δlog L|={E['max_abs_log_err_high_dose_rate']:.3e}  pass={E['high_pass']}")
    print(f"   low-DR  max |Δlog L|={E['max_abs_log_err_low_dose_rate']:.3e}  pass={E['low_pass']}")

    print(">> Claim F: α = ε_i * α_DSB (Eq. 8) across all cell lines")
    F = claim_F_alpha_taylor()
    print(f"   max rel err={F['max_rel_err']:.3e}  pass={F['pass']}")

    summary = {
        "A_table2_sanity": A,
        "B_dose_rate_curves": B,
        "C_split_dose_curves": C,
        "D_table3": D,
        "E_limits": E,
        "F_alpha_taylor": F,
    }
    (OUT_RES / "repass_summary.json").write_text(json.dumps(summary, indent=2,
                                                            default=str))
    print("Done. Outputs in", OUT_RES, "and", OUT_FIG)
