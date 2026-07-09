"""
LUCID replication: Pariset et al. 2020
"53BP1 Repair Kinetics for Prediction of In Vivo Radiation Susceptibility in 15 Mouse Strains"
Radiat Res 194:485-499, DOI 10.1667/RADE-20-00122.1

This script:
1. Implements the paper's exponential-decay repair kinetics model (Eqs. 1-6).
2. Loads per-strain tau / rho values DIGITIZED from Fig. 4 bar charts.
3. Reproduces the Pearson correlation between tau_HZE and q_HZE across 15 strains
   and compares with the paper's Table 1A.
4. Reproduces the Fig. 4 ranking of strains by repair speed.
5. Reproduces a sanity-check correlation of Fig. 7C cancer correlations
   (reported r values only; cannot regenerate from raw data without MTB pull
    + raw per-strain repair kinetics).
6. Reports a synthetic in-silico verification: simulate decay with known
   (tau, q, RIFmax) -> recover them by least-squares fit, confirming
   identifiability of the model.

UNCERTAINTY: All per-strain numerical values are vision-digitized from a
PDF bar chart. Treat them as approximate (~+/-0.5 h for tau, +/-0.01 for rho).
The paper provides NO supplementary data tables with the raw per-strain
kinetic parameters; only the bar charts in Fig. 4 and Table 1's
strain-aggregated correlation matrix.
"""

from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGS.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# 1. Model equations (verbatim from paper)
# -----------------------------------------------------------------------------
def repair_kinetics_HZE(t, RIFmax, tau, q):
    """Eq. (1): RIF/um(t) = (a/Cl)*LET * (q*exp(-t/tau) + (1-q))
    where (a/Cl)*LET == RIFmax. Returned in same units as RIFmax."""
    return RIFmax * (q * np.exp(-t / tau) + (1.0 - q))


def repair_kinetics_Xray_0p1Gy(t, tau):
    """Eq. (3): RIF/cell(t) = 1.28 * exp(-t/tau) for 0.1 Gy X rays (no clustering, q=1).
    1.28 == b * dose = 12.8 DSB/Gy * 0.1 Gy."""
    return 1.28 * np.exp(-t / tau)


def repair_kinetics_Xray_1Gy(t, tau, Cl):
    """Eq. (4): RIF/cell(t) = (b/Cl)*dose * exp(-t/tau)
    with b=12.8 DSB/Gy, dose=1 Gy."""
    b = 12.8
    dose = 1.0
    return (b / Cl) * dose * np.exp(-t / tau)


def repair_kinetics_Xray_4Gy(t, a, tau, RIF_48h):
    """Eq. (5): RIF(t) = a*exp(-t/tau) + 0.7*RIF(t=48h)
    with residual damage set to 70% of RIF/cell observed at 48h."""
    return a * np.exp(-t / tau) + 0.7 * RIF_48h


# -----------------------------------------------------------------------------
# 2. Load digitized data
# -----------------------------------------------------------------------------
def load_fig4():
    """Return list of dicts for the 15 strains."""
    rows = []
    with open(DATA / "digitized_fig4.csv") as f:
        for line in f:
            if line.startswith("#") or not line.strip() or line.startswith("strain"):
                continue
            parts = line.strip().split(",")
            rows.append({
                "strain": parts[0],
                "tau_HZE": float(parts[1]),
                "q_HZE": float(parts[2]),
                "tau_Xray4Gy": float(parts[3]),
                "q_Xray4Gy": float(parts[4]),
            })
    return rows


# -----------------------------------------------------------------------------
# 3. Reproduce paper's Table 1 correlations on digitized data
# -----------------------------------------------------------------------------
def replicate_table1():
    strains = load_fig4()
    tau_HZE = np.array([s["tau_HZE"] for s in strains])
    q_HZE = np.array([s["q_HZE"] for s in strains])
    tau_X4 = np.array([s["tau_Xray4Gy"] for s in strains])
    q_X4 = np.array([s["q_Xray4Gy"] for s in strains])

    results = {}

    # Paper Table 1A reports r(tau_40Ar, q_40Ar) = 0.13 and r(tau_56Fe, q_56Fe) = -0.31
    # Our digitization combines 40Ar+56Fe into a single HZE fit ("all LET"), so the
    # cleanest cross-check is the COMBINED-HZE tau vs q correlation, which is not
    # directly tabulated. We compute it and compare to the per-particle entries.
    r_HZE, p_HZE = pearsonr(tau_HZE, q_HZE)
    results["r(tau_HZE_combined, q_HZE_combined)"] = (round(r_HZE, 3), round(p_HZE, 4))

    # Paper Table 1B reports r(tau_4Gy, q_4Gy) = -0.75 (significant). Strong test.
    r_X4, p_X4 = pearsonr(tau_X4, q_X4)
    results["r(tau_Xray4Gy, q_Xray4Gy)  PAPER=-0.75"] = (round(r_X4, 3), round(p_X4, 4))

    # Paper has no direct r between HZE and X-ray kinetics for the same strain.
    # We add it as an extra sanity check.
    r_tau_cross, p_tau_cross = pearsonr(tau_HZE, tau_X4)
    results["r(tau_HZE, tau_Xray4Gy)  cross-modality"] = (round(r_tau_cross, 3), round(p_tau_cross, 4))
    r_q_cross, p_q_cross = pearsonr(q_HZE, q_X4)
    results["r(q_HZE, q_Xray4Gy)  cross-modality"] = (round(r_q_cross, 3), round(p_q_cross, 4))
    return results


# -----------------------------------------------------------------------------
# 4. Model self-verification: simulate decay, recover parameters
# -----------------------------------------------------------------------------
def model_identifiability_check():
    """Simulate noisy 53BP1 RIF kinetics at 4, 8, 24, 48 h with known parameters
    and recover them by curve_fit, confirming the model is identifiable."""
    rng = np.random.default_rng(0)
    truth = {"RIFmax": 4.0, "tau": 6.5, "q": 0.88}  # representative HZE strain
    t = np.array([4.0, 8.0, 24.0, 48.0])
    y_true = repair_kinetics_HZE(t, **truth)

    n_trials = 200
    rec = {"RIFmax": [], "tau": [], "q": []}
    for _ in range(n_trials):
        y_obs = y_true + rng.normal(0, 0.10 * y_true.mean(), size=t.size)
        try:
            popt, _ = curve_fit(
                repair_kinetics_HZE,
                t, y_obs,
                p0=[4.0, 5.0, 0.9],
                bounds=([0.1, 0.1, 0.0], [20.0, 50.0, 1.0]),
                maxfev=10000,
            )
            rec["RIFmax"].append(popt[0])
            rec["tau"].append(popt[1])
            rec["q"].append(popt[2])
        except Exception:
            continue
    summary = {}
    for k, vals in rec.items():
        arr = np.array(vals)
        summary[k] = {
            "true": truth[k],
            "median_recovered": round(float(np.median(arr)), 3),
            "p16": round(float(np.percentile(arr, 16)), 3),
            "p84": round(float(np.percentile(arr, 84)), 3),
            "n_fits": int(arr.size),
        }
    return summary


# -----------------------------------------------------------------------------
# 5. Plot: re-create Fig. 4 from digitized values
# -----------------------------------------------------------------------------
def plot_fig4_recreated():
    strains = load_fig4()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    # Panel A: HZE
    sortedA = sorted(strains, key=lambda s: s["tau_HZE"])
    names = [s["strain"] for s in sortedA]
    taus = [s["tau_HZE"] for s in sortedA]
    qs = [s["q_HZE"] for s in sortedA]
    axes[0, 0].bar(range(15), taus, color="steelblue")
    axes[0, 0].set_xticks(range(15))
    axes[0, 0].set_xticklabels(names, rotation=60, ha="right", fontsize=8)
    axes[0, 0].set_ylabel("τ (all LET) [h]")
    axes[0, 0].set_title("A. HZE irradiation (digitized)")
    axes[0, 0].set_ylim(0, 15)

    axes[1, 0].bar(range(15), qs, color="indianred")
    axes[1, 0].set_xticks(range(15))
    axes[1, 0].set_xticklabels(names, rotation=60, ha="right", fontsize=8)
    axes[1, 0].set_ylabel("ρ (all LET)")
    axes[1, 0].set_ylim(0.7, 1.0)

    # Panel B: X-ray
    sortedB = sorted(strains, key=lambda s: s["tau_Xray4Gy"])
    namesB = [s["strain"] for s in sortedB]
    tausB = [s["tau_Xray4Gy"] for s in sortedB]
    qsB = [s["q_Xray4Gy"] for s in sortedB]
    axes[0, 1].bar(range(15), tausB, color="steelblue")
    axes[0, 1].set_xticks(range(15))
    axes[0, 1].set_xticklabels(namesB, rotation=60, ha="right", fontsize=8)
    axes[0, 1].set_ylabel("τ (4 Gy X rays) [h]")
    axes[0, 1].set_title("B. X-ray irradiation (digitized)")
    axes[0, 1].set_ylim(0, 15)

    axes[1, 1].bar(range(15), qsB, color="indianred")
    axes[1, 1].set_xticks(range(15))
    axes[1, 1].set_xticklabels(namesB, rotation=60, ha="right", fontsize=8)
    axes[1, 1].set_ylabel("ρ (4 Gy X rays)")
    axes[1, 1].set_ylim(0.7, 1.0)

    plt.tight_layout()
    out = FIGS / "fig4_recreated.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_kinetics_curves():
    """Plot example decay curves with each model variant."""
    t_dense = np.linspace(0, 48, 200)
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # HZE: vary tau
    for tau in (4, 7, 12):
        y = repair_kinetics_HZE(t_dense, RIFmax=4.0, tau=tau, q=0.88)
        ax[0].plot(t_dense, y, label=f"τ={tau} h, q=0.88, RIFmax=4")
    # vary q
    for q in (0.7, 0.85, 1.0):
        y = repair_kinetics_HZE(t_dense, RIFmax=4.0, tau=7, q=q)
        ax[0].plot(t_dense, y, ls="--", label=f"τ=7, q={q}, RIFmax=4")
    ax[0].set_xlabel("Time post-irradiation [h]")
    ax[0].set_ylabel("RIF/μm (HZE)")
    ax[0].set_title("HZE model (Eq. 1) sensitivity")
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=0.3)

    # X-ray 0.1 Gy
    for tau in (3, 6, 9):
        y = repair_kinetics_Xray_0p1Gy(t_dense, tau=tau)
        ax[1].plot(t_dense, y, label=f"τ={tau} h")
    ax[1].set_xlabel("Time post-irradiation [h]")
    ax[1].set_ylabel("RIF/cell (0.1 Gy X-ray)")
    ax[1].set_title("0.1 Gy X-ray model (Eq. 3)")
    ax[1].legend()
    ax[1].grid(alpha=0.3)

    plt.tight_layout()
    out = FIGS / "model_kinetics_examples.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


# -----------------------------------------------------------------------------
# 6. Fig. 7C reported-r summary
# -----------------------------------------------------------------------------
def summarize_fig7c():
    rows = []
    with open(DATA / "fig7c_cancer_correlations.csv") as f:
        for line in f:
            if line.startswith("#") or not line.strip() or line.startswith("organ"):
                continue
            parts = line.strip().split(",")
            organ = parts[0]
            r = None if parts[1] == "NA" else float(parts[1])
            rows.append((organ, r))
    # report counts in each r-magnitude bin
    bins = {"strong_pos>=0.8": 0, "mod_pos 0.4-0.8": 0, "weak_or_neg": 0, "missing": 0}
    for organ, r in rows:
        if r is None:
            bins["missing"] += 1
        elif r >= 0.8:
            bins["strong_pos>=0.8"] += 1
        elif r >= 0.4:
            bins["mod_pos 0.4-0.8"] += 1
        else:
            bins["weak_or_neg"] += 1
    return rows, bins


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
    out_lines = []
    out_lines.append("=== Pariset et al. 2020 — replication results ===\n")

    # Table 1 replication
    t1 = replicate_table1()
    out_lines.append("\n-- Section 3: Pearson correlations on digitized Fig. 4 data --")
    for k, v in t1.items():
        out_lines.append(f"  {k}: r={v[0]}  p={v[1]}")
    out_lines.append(
        "\n  Paper Table 1B reports r(tau_4Gy, q_4Gy) = -0.75 (sig, n=15).\n"
        "  Our digitized value is the key validation point."
    )

    # Identifiability check
    out_lines.append("\n-- Section 4: model self-identifiability (sim/recovery, 200 trials, 10% noise) --")
    ident = model_identifiability_check()
    for k, v in ident.items():
        out_lines.append(f"  {k}: true={v['true']}  median={v['median_recovered']}  68%-CI=({v['p16']},{v['p84']})  n={v['n_fits']}")

    # Fig 7C summary
    out_lines.append("\n-- Section 6: Fig. 7C cancer-correlation digitization summary --")
    rows, bins = summarize_fig7c()
    for organ, r in rows:
        rep = "NA" if r is None else f"{r:+.2f}"
        out_lines.append(f"  {organ:25s}  r(tau_0.1Gy, incidence) = {rep}")
    out_lines.append(f"\n  bin counts: {bins}")
    out_lines.append(
        "  NOTE: n=4 strains; |r|>0.95 required for p<0.05. The paper itself does\n"
        "  not bold these for significance — they are descriptive only."
    )

    # Plots
    f1 = plot_fig4_recreated()
    f2 = plot_kinetics_curves()
    out_lines.append(f"\nFigures written:\n  {f1}\n  {f2}")

    text = "\n".join(out_lines)
    print(text)
    (RESULTS / "replication_results.txt").write_text(text)


if __name__ == "__main__":
    main()
