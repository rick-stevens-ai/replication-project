"""
Generate X-ray survival curve replication for HSG and V79 (Wang 2018, Fig 2c,d).

Two scenarios are plotted side-by-side:
  - "MCDS-McMahon Y": Y_X = 5.738 DSB/Gy/Gbp * cell DNA content (literature ref)
  - "Self-consistent Y": Y inferred so that model + Table 1 params reproduce
                          the paper's reported D10 (HSG=4.08, V79=7.07 Gy)

This makes the unknown-MCDS-calibration issue explicit and honest.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from wang2018_model import HSG_PARAMS, V79_PARAMS, cell_survival, cell_alpha_beta

D = np.linspace(0.0, 12.0, 600)

# Reference LQ "Furusawa-derived" parameters (paper Results section + Suzuki/Furusawa
# X-ray fits reproduced widely in literature):
LQ_REF = {
    "HSG": {"alpha": 0.313, "beta": 0.0615, "D10": 4.08,
            "source": "Furusawa et al. 2000 / Suzuki et al. 2000 LQ fit"},
    "V79": {"alpha": 0.129, "beta": 0.0517, "D10": 7.07,
            "source": "Furusawa et al. 2000 / many follow-ups"},
}

LAM = 1.0
# Scenario A: literature MCDS calibration
Y_A = {"HSG": 5.738 * 6.0, "V79": 5.738 * 5.6}

# Scenario B: solved-from-D10 (see find_Y_from_D10.py)
Y_B = {"HSG": 55.478, "V79": 50.935}

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)

for ax, cell, name in [(axes[0], HSG_PARAMS, "HSG"), (axes[1], V79_PARAMS, "V79")]:
    # Reference LQ fit from paper-cited Furusawa
    ref = LQ_REF[name]
    S_ref = np.exp(-(ref["alpha"] * D + ref["beta"] * D ** 2))
    ax.semilogy(D, S_ref, "k-", lw=2,
                label=f"LQ ref: α={ref['alpha']:.3f}, β={ref['beta']:.4f}")

    # Scenario A
    Sa = cell_survival(D, Y_A[name], LAM, Y_A[name], cell)
    ax.semilogy(D, Sa, "b--", lw=1.5,
                label=f"Wang model, Y={Y_A[name]:.1f} (McMahon MCDS)")

    # Scenario B
    Sb = cell_survival(D, Y_B[name], LAM, Y_B[name], cell)
    ax.semilogy(D, Sb, "r:", lw=1.8,
                label=f"Wang model, Y={Y_B[name]:.1f} (Y inferred from D10)")

    # Mark SF=10%
    ax.axhline(0.1, color="grey", ls="-.", lw=0.7)
    ax.axvline(ref["D10"], color="grey", ls="-.", lw=0.7)
    ax.text(ref["D10"], 0.013, f"D10={ref['D10']} Gy",
            ha="left", va="bottom", fontsize=8)

    ax.set_title(f"{name}  X-ray survival")
    ax.set_xlabel("Dose (Gy)")
    if ax is axes[0]:
        ax.set_ylabel("Surviving fraction")
    ax.set_ylim(1e-3, 1.2)
    ax.set_xlim(0, 12)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=8)

fig.suptitle("Wang et al. 2018, Fig. 2c,d replication — X-ray survival curves\n"
             "(Table 1 parameters used; Y from MCDS NOT published in paper)",
             fontsize=10)
fig.tight_layout(rect=(0, 0, 1, 0.94))
out = os.path.join(os.path.dirname(__file__), "..", "figures", "fig2cd_xray_survival.png")
fig.savefig(out, dpi=130)
print(f"Wrote {out}")

# Quantitative comparison
print("\nQuantitative comparison (X-ray, lam_p=1):")
print(f"{'cell':>4} {'scenario':>30} {'alpha':>8} {'beta':>10} {'a/b':>7} {'D10':>7}")

def d10(D, S):
    lnS = np.log(np.clip(S, 1e-30, None))
    return np.interp(np.log(0.1), lnS[::-1], D[::-1])

for cell, name in [(HSG_PARAMS, "HSG"), (V79_PARAMS, "V79")]:
    ref = LQ_REF[name]
    print(f"{name:>4} {'LQ reference (Furusawa)':>30} "
          f"{ref['alpha']:>8.4f} {ref['beta']:>10.5f} "
          f"{ref['alpha']/ref['beta']:>7.2f} {ref['D10']:>7.2f}")
    for label, Y in [("Wang model, Y=McMahon", Y_A[name]),
                     ("Wang model, Y=D10-inferred", Y_B[name])]:
        a, b = cell_alpha_beta(Y, LAM, cell)
        S = cell_survival(D, Y, LAM, Y, cell)
        d10v = d10(D, S)
        print(f"{name:>4} {label:>30} {a:>8.4f} {b:>10.5f} {a/b:>7.2f} {d10v:>7.2f}")
