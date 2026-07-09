"""Generate replication figures matching the four panels of Fig. 1, the
Fig. 2 (ERR/Gy vs dose-rate) and Fig. 4 dysplasia curves.

Outputs all PNGs into ../figures/ and dumps a CSV of the model curves into
../evidence/ for downstream auditing.
"""
from __future__ import annotations
import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import ERR, P_DEFAULT, TX_DAYS

# Output paths -----------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.abspath(os.path.join(HERE, "..", "figures"))
EVI_DIR = os.path.abspath(os.path.join(HERE, "..", "evidence"))
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(EVI_DIR, exist_ok=True)

A_AGE = 800.0   # default age at follow-up; sensitivity in evidence/age_sensitivity.csv

# Common dose grids ------------------------------------------------------------
DG_GRID = np.linspace(0.0, 0.5, 41)      # gamma dose 0..0.5 Gy
DN_GRID = np.linspace(0.0, 0.10, 41)     # neutron dose 0..0.1 Gy
DD_GRID = np.linspace(0.0, 75.0, 41)     # DMBA dose 0..75 mg

RG_HIGH = 576.0
RG_LOW = 0.01
RN_HIGH = 360.0
RN_LOW = 0.01

DMBA_PRE = 2.5  # mg

# -----------------------------------------------------------------------------
# Fig. 1 - four-panel tumour ERR plot
# -----------------------------------------------------------------------------

def fig1():
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)

    # Panel A: DMBA alone (linear)
    ax = axes[0, 0]
    err_d = [ERR(D_DMBA=d) for d in DD_GRID]
    ax.plot(DD_GRID, err_d, '-', label='DMBA alone')
    ax.set_xlabel('DMBA dose (mg)')
    ax.set_ylabel('Tumour ERR')
    ax.set_title('A. DMBA only (initiator)')
    ax.grid(alpha=0.3)
    ax.legend()

    # Panel B: gamma-rays HDR vs LDR, with/without DMBA
    ax = axes[0, 1]
    for R, lab, ls in [(RG_HIGH, f'HDR ({RG_HIGH:.0f} Gy/d)', '-'),
                        (RG_LOW, f'LDR ({RG_LOW:.2f} Gy/d)', '--')]:
        y = [ERR(D_gamma=d, R_gamma=R) for d in DG_GRID]
        ax.plot(DG_GRID, y, ls, label=f'gamma {lab}')
        yD = [ERR(D_gamma=d, R_gamma=R, D_DMBA=DMBA_PRE) for d in DG_GRID]
        ax.plot(DG_GRID, yD, ls, label=f'gamma {lab} + DMBA', alpha=0.6)
    ax.set_xlabel('gamma dose (Gy)')
    ax.set_ylabel('Tumour ERR')
    ax.set_title('B. Gamma-rays +/- DMBA')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)

    # Panel C: neutrons HDR vs LDR
    ax = axes[1, 0]
    for R, lab, ls in [(RN_HIGH, f'HDR ({RN_HIGH:.0f} Gy/d)', '-'),
                        (RN_LOW, f'LDR ({RN_LOW:.2f} Gy/d)', '--')]:
        y = [ERR(D_n=d, R_n=R) for d in DN_GRID]
        ax.plot(DN_GRID, y, ls, label=f'neutron {lab}')
    ax.set_xlabel('neutron dose (Gy)')
    ax.set_ylabel('Tumour ERR')
    ax.set_title('C. Neutrons (inverse dose-rate effect)')
    ax.grid(alpha=0.3)
    ax.legend()

    # Panel D: neutrons + DMBA (synergy)
    ax = axes[1, 1]
    for R, lab, ls in [(RN_HIGH, f'HDR ({RN_HIGH:.0f} Gy/d)', '-'),
                        (RN_LOW, f'LDR ({RN_LOW:.2f} Gy/d)', '--')]:
        y = [ERR(D_n=d, R_n=R) for d in DN_GRID]
        yD = [ERR(D_n=d, R_n=R, D_DMBA=DMBA_PRE) for d in DN_GRID]
        ax.plot(DN_GRID, y, ls, label=f'n {lab}')
        ax.plot(DN_GRID, yD, ls, label=f'n {lab} + DMBA', alpha=0.6)
    ax.set_xlabel('neutron dose (Gy)')
    ax.set_ylabel('Tumour ERR')
    ax.set_title('D. Neutrons + DMBA (synergy)')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)

    fig.suptitle('Replication of Shuryak et al. 2011 (PLoS ONE 6:e28559) Fig. 1\n'
                 f'A = {A_AGE:.0f} d, Tx = {TX_DAYS:.0f} d, L = {P_DEFAULT.L:.0f} d',
                 fontsize=12)
    out = os.path.join(FIG_DIR, "fig1_tumour_ERR.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


# -----------------------------------------------------------------------------
# Fig. 2 - tumour ERR per Gy as function of dose / dose-rate for gamma and n
# -----------------------------------------------------------------------------

def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)

    # ERR/Gy versus dose at several dose rates
    ax = axes[0]
    Rs_g = [0.01, 0.1, 1.0, 10.0, 100.0, 576.0]
    Ds_g = np.linspace(0.02, 0.5, 25)
    for R in Rs_g:
        y = np.array([ERR(D_gamma=d, R_gamma=R) for d in Ds_g]) / Ds_g
        ax.plot(Ds_g, y, '-', label=f'R = {R:g} Gy/d')
    ax.set_xlabel('gamma dose (Gy)')
    ax.set_ylabel('Tumour ERR / Gy')
    ax.set_title('Gamma: ERR/Gy vs dose, family of dose rates')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7)

    ax = axes[1]
    Rs_n = [0.01, 0.1, 1.0, 10.0, 100.0, 360.0]
    Ds_n = np.linspace(0.005, 0.1, 25)
    for R in Rs_n:
        y = np.array([ERR(D_n=d, R_n=R) for d in Ds_n]) / Ds_n
        ax.plot(Ds_n, y, '-', label=f'R = {R:g} Gy/d')
    ax.set_xlabel('neutron dose (Gy)')
    ax.set_ylabel('Tumour ERR / Gy')
    ax.set_title('Neutron: ERR/Gy vs dose (inverse dose-rate)')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7)

    fig.suptitle('Replication of Shuryak et al. 2011 Fig. 2: ERR/Gy vs dose/dose-rate',
                 fontsize=12)
    out = os.path.join(FIG_DIR, "fig2_ERR_per_Gy_vs_doserate.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


# -----------------------------------------------------------------------------
# Fig. 4 - dysplasia ERR ~ 1/1.5-2.0 of tumour ERR
# Recreate the same dose-response shapes scaled by 1/1.75.
# -----------------------------------------------------------------------------

def fig4():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    scale = 1.0 / 1.75    # paper: dysplasia ERR ~ tumour ERR / (1.5..2.0)

    ax = axes[0]
    for R, lab, ls in [(RG_HIGH, f'HDR ({RG_HIGH:.0f} Gy/d)', '-'),
                        (RG_LOW, f'LDR ({RG_LOW:.2f} Gy/d)', '--')]:
        y = np.array([ERR(D_gamma=d, R_gamma=R) for d in DG_GRID]) * scale
        ax.plot(DG_GRID, y, ls, label=f'gamma {lab}')
        yD = np.array([ERR(D_gamma=d, R_gamma=R, D_DMBA=DMBA_PRE) for d in DG_GRID]) * scale
        ax.plot(DG_GRID, yD, ls, label=f'gamma {lab} + DMBA', alpha=0.6)
    ax.set_xlabel('gamma dose (Gy)')
    ax.set_ylabel('Dysplasia ERR')
    ax.set_title(r'Dysplasia ERR (tumour ERR / 1.75)')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)

    ax = axes[1]
    for R, lab, ls in [(RN_HIGH, f'HDR ({RN_HIGH:.0f} Gy/d)', '-'),
                        (RN_LOW, f'LDR ({RN_LOW:.2f} Gy/d)', '--')]:
        y = np.array([ERR(D_n=d, R_n=R) for d in DN_GRID]) * scale
        ax.plot(DN_GRID, y, ls, label=f'n {lab}')
        yD = np.array([ERR(D_n=d, R_n=R, D_DMBA=DMBA_PRE) for d in DN_GRID]) * scale
        ax.plot(DN_GRID, yD, ls, label=f'n {lab} + DMBA', alpha=0.6)
    ax.set_xlabel('neutron dose (Gy)')
    ax.set_ylabel('Dysplasia ERR')
    ax.set_title(r'Dysplasia ERR (tumour ERR / 1.75)')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)

    fig.suptitle('Replication of Shuryak et al. 2011 Fig. 4 (dysplasia, scaled tumour ERR)',
                 fontsize=12)
    out = os.path.join(FIG_DIR, "fig4_dysplasia_ERR.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


# -----------------------------------------------------------------------------
# Evidence: tabular comparison vs explicit numerical claims in the paper
# -----------------------------------------------------------------------------

PAPER_CLAIMS_NEUTRON = [
    # (D_n Gy, R_n Gy/d, DMBA mg, paper_ERR)
    (0.025, 0.01, 0.0, 1.6),
    (0.050, 0.01, 0.0, 2.2),
    (0.100, 0.01, 0.0, 2.5),
    (0.025, 0.01, 2.5, 3.1),
    (0.050, 0.01, 2.5, 3.7),
    (0.100, 0.01, 2.5, 4.5),
    (0.025, 360., 0.0, 0.5),
    (0.050, 360., 0.0, 1.1),
    (0.100, 360., 0.0, 1.4),
    (0.025, 360., 2.5, 1.0),
    (0.050, 360., 2.5, 1.6),
    (0.100, 360., 2.5, -0.7),   # note paper itself has this odd negative number
]


def claim_table_csv():
    rows = []
    rows.append(["D_n_Gy", "R_n_Gy_per_day", "DMBA_mg", "paper_ERR",
                 "model_ERR_A=800", "rel_diff",
                 "model_ERR_best_A", "best_A"])
    for D, R, dm, claim in PAPER_CLAIMS_NEUTRON:
        e800 = ERR(D_n=D, R_n=R, D_DMBA=dm, A=A_AGE)
        # also report the best-fit age (which gives max value, since lifetime peak ~400d)
        best_e, best_A = -1e9, None
        for A in np.linspace(300, 900, 61):
            e = ERR(D_n=D, R_n=R, D_DMBA=dm, A=A)
            if e > best_e:
                best_e, best_A = e, A
        rd = (e800 - claim) / max(abs(claim), 1e-3)
        rows.append([D, R, dm, claim, round(e800, 3), round(rd, 2),
                     round(best_e, 3), round(best_A, 1)])
    out = os.path.join(EVI_DIR, "claim_table_neutron.csv")
    with open(out, 'w', newline='') as f:
        csv.writer(f).writerows(rows)
    return out


def age_sensitivity_csv():
    """ERR vs follow-up age for selected scenarios."""
    rows = [["age_d", "g_1Gy_HDR", "g_1Gy_LDR", "g_0.5Gy_HDR",
             "n_0.025Gy_HDR", "n_0.025Gy_LDR",
             "n_0.05Gy_HDR", "n_0.05Gy_LDR",
             "n_0.1Gy_HDR", "n_0.1Gy_LDR",
             "DMBA_25mg"]]
    for A in np.linspace(200, 1000, 41):
        row = [round(A, 1),
               ERR(D_gamma=1.0, R_gamma=576.0, A=A),
               ERR(D_gamma=1.0, R_gamma=0.01, A=A),
               ERR(D_gamma=0.5, R_gamma=576.0, A=A),
               ERR(D_n=0.025, R_n=360.0, A=A),
               ERR(D_n=0.025, R_n=0.01, A=A),
               ERR(D_n=0.05, R_n=360.0, A=A),
               ERR(D_n=0.05, R_n=0.01, A=A),
               ERR(D_n=0.1, R_n=360.0, A=A),
               ERR(D_n=0.1, R_n=0.01, A=A),
               ERR(D_DMBA=25.0, A=A)]
        rows.append([round(v, 3) if isinstance(v, float) else v for v in row])
    out = os.path.join(EVI_DIR, "age_sensitivity.csv")
    with open(out, 'w', newline='') as f:
        csv.writer(f).writerows(rows)
    return out


def reduced_xi2_proxy():
    """Approximate reduced chi^2 with the 11 paper-quoted neutron tumour ERR
    values (the -0.7 outlier is paper-acknowledged and excluded). Variance is
    estimated from the paper's quoted ~95% CIs (half-width ~0.5-1.5) which
    correspond to sigma ~ 0.25-0.75. We report a range plus the assumption-free
    RMSE/RMS-relative-error."""
    import math
    data = [(D, R, dm, c) for D, R, dm, c in PAPER_CLAIMS_NEUTRON if c >= 0]
    n = len(data)
    diffs = []
    rels = []
    for D, R, dm, claim in data:
        m = ERR(D_n=D, R_n=R, D_DMBA=dm, A=A_AGE)
        diffs.append(m - claim)
        rels.append((m - claim) / claim)
    rmse = math.sqrt(sum(x * x for x in diffs) / n)
    rms_rel = math.sqrt(sum(x * x for x in rels) / n)
    out = os.path.join(EVI_DIR, "reduced_chi2_neutron_proxy.txt")
    with open(out, 'w') as f:
        f.write(
            f"Goodness-of-fit proxy on n = {n} paper-quoted neutron tumour ERR values\n"
            f"(excludes paper-acknowledged outlier at 0.1 Gy HDR + DMBA = -0.7).\n"
            f"\n"
            f"Absolute RMSE on ERR (model - paper):  {rmse:.3f}\n"
            f"RMS relative error:                    {rms_rel*100:.1f}%\n"
            f"\n"
            f"For reduced chi^2 with sigma per point:\n"
            f"  sigma = 0.25 -> chi^2/n = {sum(x*x for x in diffs)/n / 0.25**2:.3f}\n"
            f"  sigma = 0.50 -> chi^2/n = {sum(x*x for x in diffs)/n / 0.50**2:.3f}\n"
            f"  sigma = 0.75 -> chi^2/n = {sum(x*x for x in diffs)/n / 0.75**2:.3f}\n"
            f"\n"
            f"Paper reports overall reduced chi^2 = 1.35 over its FULL tumour+dysplasia\n"
            f"data set (more points, original error weights, full simulated-annealing fit).\n"
            f"Our proxy uses only 11 author-quoted point values without their CIs.\n"
        )
    return out


if __name__ == "__main__":
    outs = []
    outs.append(fig1())
    outs.append(fig2())
    outs.append(fig4())
    outs.append(claim_table_csv())
    outs.append(age_sensitivity_csv())
    outs.append(reduced_xi2_proxy())
    print("Wrote:")
    for o in outs:
        print(" ", o)
