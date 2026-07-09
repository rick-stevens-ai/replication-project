"""
Replicate Scott 2011 Figures 1, 2, 3, 4, 5 (smoke replication of MULTISIG1 model).

Run:   python code/replicate_figures.py
Outputs PNGs in figures/ and a JSON summary in results/.
"""
from __future__ import annotations
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from multisig1 import (
    MultiSig1Params, B_of_D, BPM, phi_n, Psi_n, Cum, Att_n, RB, RBM
)

# Try to use matplotlib; if missing, skip plots but still write numeric outputs.
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception as e:
    print(f"[warn] matplotlib not available ({e}); skipping plots.")
    HAVE_MPL = False


def main():
    p = MultiSig1Params()
    fig_dir = os.path.join(ROOT, "figures")
    res_dir = os.path.join(ROOT, "results")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    summary = {
        "paper": "Scott 2011, Dose-Response 9:579-601",
        "doi": "10.2203/dose-response.10-039.Scott",
        "parameters": p.__dict__,
        "checks": {},
    }

    # --- Figure 1: phi_n(t) for n = 1..4 -----------------------------------
    t = np.linspace(0.01, 25.0, 200)
    phis = {n: np.array([phi_n(n, ti, p) for ti in t]) for n in (1, 2, 3, 4)}

    if HAVE_MPL:
        plt.figure(figsize=(6, 4))
        markers = {1: "D", 2: "s", 3: "^", 4: "o"}
        for n, vals in phis.items():
            plt.plot(t, vals, marker=markers[n], markevery=20, label=f"phi_{n}(t)")
        plt.xlabel("Time post exposure (h)")
        plt.ylabel("phi_n(t)  (1/h)")
        plt.title("Fig 1: Repair-time density per-molecule (MRC-5, 90 kV x-rays)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "fig1_phi_n.png"), dpi=120)
        plt.close()

    # Spot-check: phi_1 peaks at t=0 with value 1/beta = 0.4
    summary["checks"]["phi1_at_t=0_expected_1/beta"] = {
        "expected": 1.0 / p.beta, "got": phi_n(1, 0.0, p)
    }

    # --- Figure 2: attributions Att_n(D) up to D = 1000 mGy ----------------
    Ds = np.linspace(0.0, 1000.0, 201)
    atts = {n: np.array([Att_n(n, D, p) for D in Ds]) for n in (1, 2, 3, 4)}

    if HAVE_MPL:
        plt.figure(figsize=(6, 4))
        markers = {1: "D", 2: "s", 3: "^", 4: "o"}
        for n, vals in atts.items():
            plt.plot(Ds, vals, marker=markers[n], markevery=20, label=f"Att_{n}(D)")
        plt.xlabel("Dose D (mGy)")
        plt.ylabel("Attribution (%)")
        plt.title("Fig 2: Attribution to overall repair kinetics")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "fig2_attributions.png"), dpi=120)
        plt.close()

    # Paper text (p.589): "for D=1000 mGy, Att2=46.7%, Att3=13.6%, Att4=3.4%"
    summary["checks"]["Att_at_D=1000mGy"] = {
        "Att1": Att_n(1, 1000.0, p),
        "Att2_expected_46.7": Att_n(2, 1000.0, p),
        "Att3_expected_13.6": Att_n(3, 1000.0, p),
        "Att4_expected_3.4":  Att_n(4, 1000.0, p),
    }
    # Text also says for D<10 mGy, Att1 > 99%
    summary["checks"]["Att1_at_D=10mGy_expected_>99"] = Att_n(1, 10.0, p)

    # --- Figure 3: Psi_n(t) for n = 1..4 -----------------------------------
    psis = {n: np.array([Psi_n(n, ti, p) for ti in t]) for n in (1, 2, 3, 4)}
    if HAVE_MPL:
        plt.figure(figsize=(6, 4))
        markers = {1: "D", 2: "s", 3: "^", 4: "o"}
        for n, vals in psis.items():
            plt.plot(t, vals, marker=markers[n], markevery=20, label=f"Psi_{n}(t)")
        plt.xlabel("Time post exposure (h)")
        plt.ylabel("Cumulative probability of repair")
        plt.title("Fig 3: Per-molecule cumulative repair distribution")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "fig3_Psi_n.png"), dpi=120)
        plt.close()

    # --- Figure 4: Cum(t, D) for D=100 and D=1000 mGy ----------------------
    cum100 = np.array([Cum(ti, 100.0, p) for ti in t])
    cum1000 = np.array([Cum(ti, 1000.0, p) for ti in t])
    if HAVE_MPL:
        plt.figure(figsize=(6, 4))
        plt.plot(t, cum100, "D-", markevery=20, label="Cum(t, 100 mGy)")
        plt.plot(t, cum1000, "s-", markevery=20, label="Cum(t, 1000 mGy)")
        plt.xlabel("Time post exposure (h)")
        plt.ylabel("Cum(t, D)")
        plt.title("Fig 4: Poisson-weighted cumulative repair (MRC-5)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "fig4_Cum.png"), dpi=120)
        plt.close()

    # --- Figure 5: RB(t, D) for D in {0, 5, 20, 100, 200} mGy --------------
    t5 = np.linspace(0.01, 25.0, 300)
    fig5_doses = [5.0, 20.0, 100.0, 200.0]
    rbs = {D: np.array([RB(ti, D, p) for ti in t5]) for D in fig5_doses}
    control = np.full_like(t5, p.B0)  # D=0 horizontal at B0

    if HAVE_MPL:
        plt.figure(figsize=(7, 5))
        markers = {5.0: "D", 20.0: "s", 100.0: "^", 200.0: "o"}
        for D in fig5_doses:
            plt.semilogy(t5, rbs[D], marker=markers[D], markevery=30, label=f"{int(D)} mGy")
        plt.semilogy(t5, control, "k--", label="0 mGy (control)")
        plt.xlabel("Time post exposure (h)")
        plt.ylabel("Residual DSBs per cell  (log scale)")
        plt.title("Fig 5: Predicted residual DSBs/cell (MRC-5, 90 kV x-rays)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "fig5_residual_DSBs.png"), dpi=120)
        plt.close()

    # Save Figure-5 numerical table
    fig5_rows = ["time_h," + ",".join(f"D_{int(D)}mGy" for D in fig5_doses)]
    for i, ti in enumerate(t5):
        fig5_rows.append(
            f"{ti:.4f}," + ",".join(f"{rbs[D][i]:.6f}" for D in fig5_doses)
        )
    with open(os.path.join(res_dir, "fig5_RB.csv"), "w") as f:
        f.write("\n".join(fig5_rows) + "\n")

    # Spot-checks vs paper:
    #  - RB(t->inf, D) -> BT = 0.1 for any D > T
    #  - RB(t=0, D) = BT + alpha*(D-T) = B_of_D(D) - (effectively, since BT = B0+alpha*T)
    #  - At D=0.1 mGy (below T): paper says 0.0535 DSBs/cell, independent of t
    summary["checks"]["RB_at_D=0.1mGy_expected_0.0535"] = RB(10.0, 0.1, p)
    summary["checks"]["RB_t=inf_D=100mGy_expected_BT_0.1"] = RB(1000.0, 100.0, p)
    summary["checks"]["RB_t=0_D=100mGy_expected_B(D)=B0+alpha*D=3.55"] = RB(0.0, 100.0, p)
    summary["checks"]["RB_t=0_D=5mGy_expected_~0.225"] = RB(0.0, 5.0, p)
    summary["checks"]["RB_t=0_D=20mGy_expected_~0.75"] = RB(0.0, 20.0, p)

    with open(os.path.join(res_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print("Spot-check results vs paper:")
    print(f"  Att2(1000 mGy) = {Att_n(2,1000.0,p):.2f}  (paper: 46.7)")
    print(f"  Att3(1000 mGy) = {Att_n(3,1000.0,p):.2f}  (paper: 13.6)")
    print(f"  Att4(1000 mGy) = {Att_n(4,1000.0,p):.2f}  (paper: 3.4)")
    print(f"  Att1(10  mGy)  = {Att_n(1,  10.0,p):.4f} (paper: >99)")
    print(f"  RB(t=10h, D=0.1 mGy) = {RB(10.0,0.1,p):.4f}  (paper text: 0.0535)")
    print(f"  RB(t->inf, D=100 mGy) = {RB(1000.0,100.0,p):.4f}  (expected BT = 0.1)")
    print(f"  RB(t=0, D=100 mGy)    = {RB(0.0,100.0,p):.4f}  (expected B0+alpha*D = 3.55)")
    print(f"  phi_1(t=0) = {phi_n(1,0.0,p):.4f}  (expected 1/beta = 0.40)")
    print("=" * 60)
    print(f"Wrote figures to {fig_dir}/")
    print(f"Wrote results to {res_dir}/summary.json and fig5_RB.csv")


if __name__ == "__main__":
    main()
