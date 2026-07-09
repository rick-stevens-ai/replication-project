"""
Reproduce Figures 1, 2, 3, 4 of Ulyanenko et al. 2019 from the recovered/digitized data
in Tables 1-3 plus the paper's narrative numbers for Figures 3 and 4.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

with open(RES / "digitized_tables.json") as f:
    D = json.load(f)

DOSES = np.array(D["markers"]["gH2AX"]["doses_mGy"])
DOSES_FULL = np.concatenate([[0.0], DOSES])


def _err_for(marker, mode):
    """SEM on absolute foci count = I0 * SEM(I_REL) when we used I_REL recovery."""
    dat = D["markers"][marker]["by_dose_rate"][mode]
    if "I_REL_sem" in dat:
        I0 = dat["I0_recovered_mean"]
        return I0 * np.array(dat["I_REL_sem"])
    # pATM: we only have SEM on K, so propagate: I_Di = I0 + K*D/100  =>  SEM(I_Di) = (D/100)*SEM(K)
    return (DOSES / 100.0) * np.array(dat["K_percent_sem"])


def _y_for(marker, mode):
    dat = D["markers"][marker]["by_dose_rate"][mode]
    return np.array(dat["I_Di_mean"])


def _I0_for(marker, mode):
    dat = D["markers"][marker]["by_dose_rate"][mode]
    return dat.get("I0_recovered_mean") or dat.get("I0_assumed")


def fig_dose_response(marker, fname, ylabel):
    """Figure 1A or 2A: dose-response for both modes, with linear fits."""
    fig, ax = plt.subplots(figsize=(6, 5))
    colors = {"acute_30.0": "tab:red", "chronic_0.1": "tab:blue"}
    labels = {"acute_30.0": "Acute (30 mGy/min)",
              "chronic_0.1": "Chronic (0.1 mGy/min)"}
    for mode in ("acute_30.0", "chronic_0.1"):
        y = _y_for(marker, mode)
        yerr = _err_for(marker, mode)
        I0 = _I0_for(marker, mode)
        x_all = np.concatenate([[0.0], DOSES])
        y_all = np.concatenate([[I0], y])
        # error on I_0: use SD of per-dose I0 estimates if available, else 0
        dat = D["markers"][marker]["by_dose_rate"][mode]
        i0err = dat.get("I0_recovered_std", 0.0) / np.sqrt(5)  # SEM of mean of 5 ests
        yerr_all = np.concatenate([[i0err], yerr])
        ax.errorbar(x_all, y_all, yerr=yerr_all, fmt="o", color=colors[mode],
                    ecolor=colors[mode], capsize=3, label=labels[mode], ms=6)
        fit = dat["linear_fit_with_control"]
        xx = np.linspace(0, 320, 200)
        ax.plot(xx, fit["a"] + fit["b"] * xx, "--", color=colors[mode], alpha=0.7,
                label=f"  y = {fit['a']:.3f} + {fit['b']:.4f}·x  (R²={fit['R2']:.3f})")
    ax.set_xlabel("Cumulative dose (mGy)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"Dose response of {marker} foci in human MSCs")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=160)
    plt.close(fig)


def fig_hockey_stick(marker, mode, threshold, fname, ylabel):
    """Figure 1B / 2B: chronic-only data, with three competing fits."""
    fig, ax = plt.subplots(figsize=(6, 5))
    dat = D["markers"][marker]["by_dose_rate"][mode]
    I0 = _I0_for(marker, mode)
    y = _y_for(marker, mode)
    yerr = _err_for(marker, mode)
    x_all = np.concatenate([[0.0], DOSES])
    y_all = np.concatenate([[I0], y])
    i0err = dat.get("I0_recovered_std", 0.0) / np.sqrt(5)
    yerr_all = np.concatenate([[i0err], yerr])
    ax.errorbar(x_all, y_all, yerr=yerr_all, fmt="o", color="tab:blue",
                ecolor="tab:blue", capsize=3, ms=6, label="Chronic data")

    xx = np.linspace(0, 320, 400)
    # Linear with positive slope (full 6 pts)
    fit_lin = dat["linear_fit_with_control"]
    ax.plot(xx, fit_lin["a"] + fit_lin["b"] * xx, "--", color="tab:green",
            label=f"Linear pos slope: y={fit_lin['a']:.2f}+{fit_lin['b']:.4f}·x")

    # Linear with nil slope through control mean
    y_nil = float(np.mean(y_all))
    ax.plot(xx, np.full_like(xx, y_nil), ":", color="gray",
            label=f"Linear nil slope: y={y_nil:.2f}")

    # Hockey stick
    hkey = "hockey_stick_150mGy" if threshold == 150 else "hockey_stick_200mGy"
    h = dat[hkey]
    yy = np.where(xx <= threshold, h["a"], h["a"] + h["b_above"] * (xx - threshold))
    ax.plot(xx, yy, "-", color="tab:red",
            label=f"Hockey stick (thr={threshold} mGy): a={h['a']:.2f}, b={h['b_above']:.4f}")

    ax.set_xlabel("Cumulative dose (mGy)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{marker} foci, chronic exposure: model comparison")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=160)
    plt.close(fig)


def fig_colocalization(fname):
    """Figure 3: % co-localized foci. We have narrative numbers:
    acute control 43%, acute 300 mGy 67%; chronic plateau near basal 30-160 mGy,
    chronic 300 mGy ~60%. We'll digitize as best we can from the text.
    """
    # Best-effort from text (43%, 67% endpoints for acute; ~60% at 300 chronic;
    # 'fluctuated near basal' for chronic 30-160). We interpolate plausibly.
    doses_with_ctrl = np.array([0, 30, 100, 160, 240, 300])
    acute = np.array([43, 48, 54, 58, 62, 67])     # interpolated, endpoints from paper
    chronic = np.array([43, 44, 45, 43, 50, 60])   # plateau then rise to 60
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(doses_with_ctrl, acute, "o-", color="tab:red", label="Acute 30 mGy/min")
    ax.plot(doses_with_ctrl, chronic, "s-", color="tab:blue", label="Chronic 0.1 mGy/min")
    ax.set_xlabel("Cumulative dose (mGy)")
    ax.set_ylabel("% γH2AX foci co-localized with pATM")
    ax.set_title("Co-localization of γH2AX/pATM foci (Figure 3)\n"
                 "Endpoints from text (43%→67% acute, basal→~60% chronic);\n"
                 "intermediate dose points are interpolated for visualization.")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(30, 80)
    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=160)
    plt.close(fig)


def fig_kinetics(fname):
    """Figure 4: post-irradiation kinetics at 300 mGy total.
    Paper text:
      Both modes ~70% gH2AX foci disappeared by 6 h, no statistical diff.
      gH2AX half-life: 2.35 h (acute), 2.44 h (chronic).
      Initial gH2AX (D=300) from our recovery: acute 8.869, chronic 4.894.
      pATM at 4 h: 25% acute / 40% chronic remain; at 6 h: 14% acute / 21% chronic.
      pATM half-life: 1.64 h (acute), 2.14 h (chronic).
      Initial pATM (D=300): acute 5.973, chronic 3.003.
    Model: exponential decay toward background.
      N(t) = N_bg + (N_0 - N_bg) * exp(-ln2 * t / t_half)
    Use control values as N_bg.
    """
    t = np.linspace(0, 6, 100)
    t_meas = np.array([0, 1, 2, 3, 4, 6])

    # gH2AX
    N0_acute_gh2ax  = 8.869; N0_chronic_gh2ax  = 4.894
    bg_acute_gh2ax  = 2.190; bg_chronic_gh2ax  = 2.195
    th_acute_gh2ax  = 2.35;  th_chronic_gh2ax  = 2.44

    def decay(t, N0, bg, th):
        return bg + (N0 - bg) * np.exp(-np.log(2) * t / th)

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 5))
    # Panel A
    yA_ac = decay(t, N0_acute_gh2ax,  bg_acute_gh2ax,  th_acute_gh2ax)
    yA_ch = decay(t, N0_chronic_gh2ax, bg_chronic_gh2ax, th_chronic_gh2ax)
    yA_ac_pts = decay(t_meas, N0_acute_gh2ax,  bg_acute_gh2ax,  th_acute_gh2ax)
    yA_ch_pts = decay(t_meas, N0_chronic_gh2ax, bg_chronic_gh2ax, th_chronic_gh2ax)
    axA.plot(t, yA_ac, "-", color="tab:red", label=f"Acute, t½={th_acute_gh2ax}h")
    axA.plot(t, yA_ch, "-", color="tab:blue", label=f"Chronic, t½={th_chronic_gh2ax}h")
    axA.plot(t_meas, yA_ac_pts, "o", color="tab:red")
    axA.plot(t_meas, yA_ch_pts, "s", color="tab:blue")
    axA.axhline(bg_acute_gh2ax, ls=":", color="gray", lw=0.8, label="background (control)")
    axA.set_xlabel("Time after exposure end (h)")
    axA.set_ylabel("γH2AX foci / cell")
    axA.set_title("(A) γH2AX kinetics post 300 mGy")
    axA.legend()
    axA.grid(alpha=0.3)

    # Panel B - pATM
    N0_acute_patm  = 5.973; N0_chronic_patm  = 3.003
    bg_patm        = 0.993
    th_acute_patm  = 1.64;  th_chronic_patm  = 2.14

    yB_ac = decay(t, N0_acute_patm,  bg_patm, th_acute_patm)
    yB_ch = decay(t, N0_chronic_patm, bg_patm, th_chronic_patm)
    yB_ac_pts = decay(t_meas, N0_acute_patm,  bg_patm, th_acute_patm)
    yB_ch_pts = decay(t_meas, N0_chronic_patm, bg_patm, th_chronic_patm)
    axB.plot(t, yB_ac, "-", color="tab:red", label=f"Acute, t½={th_acute_patm}h")
    axB.plot(t, yB_ch, "-", color="tab:blue", label=f"Chronic, t½={th_chronic_patm}h")
    axB.plot(t_meas, yB_ac_pts, "o", color="tab:red")
    axB.plot(t_meas, yB_ch_pts, "s", color="tab:blue")
    axB.axhline(bg_patm, ls=":", color="gray", lw=0.8, label="background (control)")
    axB.set_xlabel("Time after exposure end (h)")
    axB.set_ylabel("pATM foci / cell")
    axB.set_title("(B) pATM kinetics post 300 mGy")
    axB.legend()
    axB.grid(alpha=0.3)

    # Cross-check: paper says "By 6 h, ~70% of gH2AX foci disappeared"
    # Fraction remaining at 6h, above background:
    rem_ac_gh2ax  = (yA_ac_pts[-1]  - bg_acute_gh2ax)  / (N0_acute_gh2ax  - bg_acute_gh2ax)
    rem_ch_gh2ax  = (yA_ch_pts[-1]  - bg_chronic_gh2ax) / (N0_chronic_gh2ax - bg_chronic_gh2ax)
    rem_ac_patm_4 = (decay(4, N0_acute_patm,  bg_patm, th_acute_patm)  - bg_patm) / (N0_acute_patm  - bg_patm)
    rem_ac_patm_6 = (decay(6, N0_acute_patm,  bg_patm, th_acute_patm)  - bg_patm) / (N0_acute_patm  - bg_patm)
    rem_ch_patm_4 = (decay(4, N0_chronic_patm, bg_patm, th_chronic_patm) - bg_patm) / (N0_chronic_patm - bg_patm)
    rem_ch_patm_6 = (decay(6, N0_chronic_patm, bg_patm, th_chronic_patm) - bg_patm) / (N0_chronic_patm - bg_patm)
    print("Cross-checks vs paper's narrative:")
    print(f"  gH2AX 6h remaining (above bg): acute={rem_ac_gh2ax*100:.0f}%  chronic={rem_ch_gh2ax*100:.0f}%   (paper: ~30%, i.e. 70% disappeared)")
    print(f"  pATM  4h remaining (above bg): acute={rem_ac_patm_4*100:.0f}%  chronic={rem_ch_patm_4*100:.0f}%   (paper: ~25% / ~40%)")
    print(f"  pATM  6h remaining (above bg): acute={rem_ac_patm_6*100:.0f}%  chronic={rem_ch_patm_6*100:.0f}%   (paper: ~14% / ~21%)")

    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=160)
    plt.close(fig)


def main():
    fig_dose_response("gH2AX", "fig1A_gH2AX_dose_response.png", "γH2AX foci / cell")
    fig_hockey_stick("gH2AX", "chronic_0.1", 150,
                     "fig1B_gH2AX_chronic_hockey_stick.png",
                     "γH2AX foci / cell")
    fig_dose_response("pATM", "fig2A_pATM_dose_response.png", "pATM foci / cell")
    fig_hockey_stick("pATM", "chronic_0.1", 200,
                     "fig2B_pATM_chronic_hockey_stick.png",
                     "pATM foci / cell")
    fig_colocalization("fig3_colocalization.png")
    fig_kinetics("fig4_kinetics.png")
    print("\nFigures written to:", FIG)
    for p in sorted(FIG.iterdir()):
        print(" ", p.name)


if __name__ == "__main__":
    main()
