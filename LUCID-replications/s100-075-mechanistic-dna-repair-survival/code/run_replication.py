"""
Driver for McMahon 2016 mechanistic radiosensitivity replication.
Generates figures + evidence JSON in ../figures and ../evidence.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import mcmahon2016 as m

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG_DIR = ROOT / "figures"
EV_DIR = ROOT / "evidence"
FIG_DIR.mkdir(exist_ok=True, parents=True)
EV_DIR.mkdir(exist_ok=True, parents=True)


# ---------------------------------------------------------------------------
# 1. DNA repair kinetics (Fig 1)
# ---------------------------------------------------------------------------

def figure1_repair_kinetics():
    t_short = np.logspace(np.log10(0.25), np.log10(8), 200)   # 0.25-8 h
    t_long  = np.logspace(np.log10(1),    np.log10(300), 200) # 1-300 h

    cell_G1_comp = m.CellSpec(phase="G1")
    cell_G1_nhej = m.CellSpec(phase="G1", nhej_defective=True)
    cell_G2_comp = m.CellSpec(phase="G2")
    cell_G2_nhej = m.CellSpec(phase="G2", nhej_defective=True)
    cell_G2_hr   = m.CellSpec(phase="G2", hr_defective=True)

    dose_Gy = 1.0
    N0 = m.DSB_YIELD_PER_GY_PER_GBP * m.HUMAN_GENOME_GBP * dose_Gy

    def curve(spec, ts):
        pf, ps, pm = m.repair_probabilities(spec)
        return m.n_dsb_over_time(ts, N0, pf, ps, pm) / N0     # normalised

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex="col")
    for ax, ts, label in [
        (axes[0, 0], t_short, "G1, short"),
        (axes[0, 1], t_short, "G2, short"),
        (axes[1, 0], t_long,  "G1, long"),
        (axes[1, 1], t_long,  "G2, long"),
    ]:
        is_g2 = "G2" in label
        comp = cell_G2_comp if is_g2 else cell_G1_comp
        nhej = cell_G2_nhej if is_g2 else cell_G1_nhej
        ax.plot(ts, curve(comp, ts), "k-",  label="repair-competent")
        ax.plot(ts, curve(nhej, ts), "k--", label="NHEJ defective")
        if is_g2:
            ax.plot(ts, curve(cell_G2_hr, ts), "k:", label="HR defective")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylim(1e-3, 1.2)
        ax.set_title(label)
        ax.set_xlabel("time (h)")
        ax.set_ylabel("N(t)/N0  (residual DSBs)")
        ax.grid(True, which="both", ls=":", alpha=0.4)
        ax.legend(fontsize=8)
    plt.suptitle("Fig 1 replication: DNA repair kinetics  (1 Gy X-rays)")
    plt.tight_layout()
    out = FIG_DIR / "fig1_repair_kinetics.png"
    plt.savefig(out, dpi=130)
    plt.close(fig)

    # Evidence dump --------------------------------------------------------
    np.savez(EV_DIR / "fig1_curves.npz",
             t_short=t_short, t_long=t_long,
             G1_comp_short=curve(cell_G1_comp, t_short),
             G1_nhej_short=curve(cell_G1_nhej, t_short),
             G1_comp_long=curve(cell_G1_comp, t_long),
             G1_nhej_long=curve(cell_G1_nhej, t_long),
             G2_comp_short=curve(cell_G2_comp, t_short),
             G2_nhej_short=curve(cell_G2_nhej, t_short),
             G2_hr_short=curve(cell_G2_hr, t_short),
             G2_comp_long=curve(cell_G2_comp, t_long),
             G2_nhej_long=curve(cell_G2_nhej, t_long),
             G2_hr_long=curve(cell_G2_hr, t_long),
             )
    return str(out)


# ---------------------------------------------------------------------------
# 2. Misrepair fraction vs dose  (Fig 2)
# ---------------------------------------------------------------------------

def figure2_misrepair_vs_dose():
    doses = np.linspace(0.5, 80.0, 80)
    spec = m.CellSpec(phase="G1")
    frac = []
    for d in doses:
        out = m.predict_endpoints(spec, d, t_assay_hours=24)
        N0 = out["N0_DSB"]
        frac.append(out["Nmis"] / N0)
    frac = np.array(frac)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(doses, 100.0 * frac, "k-", lw=2)
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Misrepair fraction (%)")
    ax.set_title("Fig 2 replication: misrepair vs dose, normal human cells")
    ax.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    out = FIG_DIR / "fig2_misrepair_vs_dose.png"
    plt.savefig(out, dpi=130); plt.close(fig)
    np.savez(EV_DIR / "fig2_misrepair.npz", doses=doses, misrepair_frac=frac)
    return str(out)


# ---------------------------------------------------------------------------
# 3. Chromosome aberrations vs dose  (Fig 3a)
# ---------------------------------------------------------------------------

def figure3a_aberrations_vs_dose():
    doses = np.linspace(0.0, 6.0, 60)
    spec_norm = m.CellSpec(phase="G1")
    spec_nhej = m.CellSpec(phase="G1", nhej_defective=True)

    def aberr(spec):
        ndic = []
        ndel = []
        for d in doses:
            out = m.predict_endpoints(spec, d, t_assay_hours=24)
            ndic.append(out["Ndic"])
            ndel.append(out["Ndel_gt3Mbp"])
        return np.array(ndic), np.array(ndel)

    n_dic_norm, n_del_norm = aberr(spec_norm)
    n_dic_nhej, n_del_nhej = aberr(spec_nhej)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(doses, n_dic_norm + n_del_norm, "k-",  lw=2,
            label="normal (dicentrics + del>3 Mbp)")
    ax.plot(doses, n_dic_nhej + n_del_nhej, "r--", lw=2,
            label="NHEJ defective")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Aberrations per cell")
    ax.set_title("Fig 3a replication: chromosome aberrations vs dose (G1, Giemsa-detectable)")
    ax.legend()
    ax.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    out = FIG_DIR / "fig3a_aberrations_vs_dose.png"
    plt.savefig(out, dpi=130); plt.close(fig)
    np.savez(EV_DIR / "fig3a_aberrations.npz",
             doses=doses,
             dic_norm=n_dic_norm, del_norm=n_del_norm,
             dic_nhej=n_dic_nhej, del_nhej=n_del_nhej)
    return str(out)


# ---------------------------------------------------------------------------
# 4. Survival curves (Fig 5 family)
# ---------------------------------------------------------------------------

def figure5_survival():
    doses = np.linspace(0.05, 10.0, 80)
    cases = [
        ("Human fibroblast, G1 (24h hold)",  m.CellSpec(phase="G1", cycling=False, apoptosis_competent=False)),
        ("Human fibroblast, G1 + apoptosis", m.CellSpec(phase="G1", cycling=True,  apoptosis_competent=True)),
        ("CHO G1, NHEJ defective",           m.CellSpec(phase="G1", nhej_defective=True, cycling=False, apoptosis_competent=False)),
        ("CHO G2, NHEJ defective",           m.CellSpec(phase="G2", nhej_defective=True, cycling=True,  apoptosis_competent=False)),
    ]

    fig, ax = plt.subplots(figsize=(7, 5))
    rows = {}
    for label, spec in cases:
        _, S = m.survival_curve(spec, doses)
        ax.semilogy(doses, S, lw=2, label=label)
        alpha, beta = m.fit_lq(doses, S)
        mid = m.mean_inactivation_dose(spec)
        rows[label] = dict(alpha_Gy_inv=alpha, beta_Gy_inv2=beta,
                           alpha_over_beta=(alpha / beta if beta > 0 else None),
                           MID_Gy=mid)
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Surviving fraction")
    ax.set_title("Fig 5 replication: clonogenic survival curves")
    ax.set_ylim(1e-5, 1.2)
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend(fontsize=8)
    plt.tight_layout()
    out = FIG_DIR / "fig5_survival.png"
    plt.savefig(out, dpi=130); plt.close(fig)
    with open(EV_DIR / "fig5_lq_and_mid.json", "w") as f:
        json.dump(rows, f, indent=2)
    return str(out), rows


# ---------------------------------------------------------------------------
# 5. Mitotic survival (Fig 6)
# ---------------------------------------------------------------------------

def figure6_mitotic():
    doses = np.linspace(0.0, 4.0, 60)
    # In mitosis: cell dies if any DSBs remain. Use S = exp(-phi * N0)
    # since N(t=0)=N0 dominates the kinetics at the mitotic checkpoint.
    N0 = m.DSB_YIELD_PER_GY_PER_GBP * m.HUMAN_GENOME_GBP * doses
    S_mit = np.exp(-m.PHI_MIT * N0)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(doses, S_mit, "k-", lw=2)
    ax.set_xlabel("Dose (Gy)"); ax.set_ylabel("Surviving fraction (mitotic cells)")
    ax.set_title("Fig 6 replication: cells irradiated in mitosis, S = exp(-phi N0)")
    ax.set_ylim(1e-4, 1.2)
    ax.grid(True, which="both", ls=":", alpha=0.5)
    plt.tight_layout()
    out = FIG_DIR / "fig6_mitotic.png"
    plt.savefig(out, dpi=130); plt.close(fig)
    np.savez(EV_DIR / "fig6_mitotic.npz", doses=doses, S=S_mit)
    return str(out)


# ---------------------------------------------------------------------------
# 6. MID stratification (Fig 7)
# ---------------------------------------------------------------------------

def figure7_mid_stratification():
    # Synthetic cell-line panel covering G1/G2 phase, repair competence,
    # cycling/non-cycling.  We compute MID for each.  The paper claims
    # R^2 > 0.9 vs experimental MID; we cannot reproduce the experimental
    # axis from the paper PDF alone (raw data not in the article), so we
    # publish the *model* MID stratification only.
    panel = [
        ("Human fib G1 24h hold",        m.CellSpec(phase="G1", cycling=False, apoptosis_competent=False)),
        ("Human fib G1 cycling",         m.CellSpec(phase="G1", cycling=True,  apoptosis_competent=True)),
        ("Human fib G1 NHEJ-def 24h",    m.CellSpec(phase="G1", nhej_defective=True, cycling=False, apoptosis_competent=False)),
        ("CHO G1 competent",             m.CellSpec(phase="G1", cycling=False, apoptosis_competent=False)),
        ("CHO G1 NHEJ-def",              m.CellSpec(phase="G1", nhej_defective=True, cycling=False, apoptosis_competent=False)),
        ("CHO G2 competent",             m.CellSpec(phase="G2", cycling=True,  apoptosis_competent=False)),
        ("CHO G2 NHEJ-def",              m.CellSpec(phase="G2", nhej_defective=True, cycling=True, apoptosis_competent=False)),
    ]
    mids = {label: m.mean_inactivation_dose(spec) for label, spec in panel}
    fig, ax = plt.subplots(figsize=(7, 4))
    names = list(mids.keys()); vals = [mids[n] for n in names]
    ax.barh(names, vals, color="steelblue")
    ax.set_xlabel("Mean Inactivation Dose (Gy)")
    ax.set_title("Model MID stratification across phenotypes (Fig 7 model axis)")
    plt.tight_layout()
    out = FIG_DIR / "fig7_mid_stratification.png"
    plt.savefig(out, dpi=130); plt.close(fig)
    with open(EV_DIR / "fig7_mids.json", "w") as f:
        json.dump(mids, f, indent=2)
    return str(out), mids


# ---------------------------------------------------------------------------
# 7. Parameter dump
# ---------------------------------------------------------------------------

def dump_parameters():
    params = {
        "DSB_yield_per_Gy_per_Gbp": m.DSB_YIELD_PER_GY_PER_GBP,
        "human_genome_Gbp": m.HUMAN_GENOME_GBP,
        "lambda_F_per_hour": m.LAMBDA_F,
        "lambda_S_per_hour": m.LAMBDA_S,
        "lambda_M_per_hour": m.LAMBDA_M,
        "p_complex": m.P_COMPLEX,
        "p_fail": m.P_FAIL,
        "sigma_frac_Rnuc": m.SIGMA_FRAC,
        "mu_NHEJ": m.MU_NHEJ,
        "mu_MMEJ": m.MU_MMEJ,
        "nu_point": m.NU_POINT,
        "psi_apoptosis_per_break": m.PSI_APOP,
        "phi_mitosis_per_break": m.PHI_MIT,
        "Monte_Carlo_calibration_A": m.OMEGA_A,
        "Monte_Carlo_calibration_B": m.OMEGA_B,
        "source": "McMahon et al. 2016, Sci Rep 6:33290, Table 1 + Methods",
    }
    with open(EV_DIR / "parameters_table1.json", "w") as f:
        json.dump(params, f, indent=2)
    return params


def main():
    print("Dumping parameters ...")
    params = dump_parameters()

    print("Figure 1 -- DNA repair kinetics ...")
    f1 = figure1_repair_kinetics()

    print("Figure 2 -- Misrepair vs dose ...")
    f2 = figure2_misrepair_vs_dose()

    print("Figure 3a -- Aberrations vs dose ...")
    f3a = figure3a_aberrations_vs_dose()

    print("Figure 5 -- Survival curves ...")
    f5, lq_rows = figure5_survival()

    print("Figure 6 -- Mitotic survival ...")
    f6 = figure6_mitotic()

    print("Figure 7 -- MID stratification ...")
    f7, mids = figure7_mid_stratification()

    summary = {
        "figures_written": [f1, f2, f3a, f5, f6, f7],
        "lq_fits": lq_rows,
        "MID_stratification": mids,
        "parameters": params,
    }
    with open(EV_DIR / "run_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("DONE.  Evidence in", EV_DIR)
    print("DONE.  Figures in", FIG_DIR)


if __name__ == "__main__":
    main()
