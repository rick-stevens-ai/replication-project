"""
Regenerate predicted-survival curves from Matsuya 2019 (Figs 3, 4, 5) using the
published Table-1 parameters. Saves PNG/CSV under ../figures and ../data.

This is forward-model only: it does NOT fit anything. It checks whether the
published parameters, plugged into the published equations, produce the curves
the paper shows. Experimental data points are not re-plotted here (they would
have to be digitized from Figs 2-6 in a follow-up pass).
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from imk_model import (
    AGO_MF, AGO_UF, DU145_MF, DU145_UF,
    YD_INFIELD_KEV_PER_UM, YD_OUTOFFIELD_KEV_PER_UM,
    dose_response_curve, fractionated_constant_rate, survival_total_continuous,
)

OUT_FIG = Path(__file__).resolve().parent.parent / "figures"
OUT_DAT = Path(__file__).resolve().parent.parent / "data"
OUT_FIG.mkdir(exist_ok=True)
OUT_DAT.mkdir(exist_ok=True)


def write_csv(path: Path, header, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------
# Figure 3: dose-response (single-dose), in-field MF vs in-field UF vs OOF MF
# ---------------------------------------------------------------------------

def figure3_like():
    doses = np.linspace(0.0, 10.0, 81)
    rate = 0.59  # Gy/min, single-dose dose-rate from the paper

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, (p_MF, p_UF, cell) in zip(
        axes,
        [(AGO_MF, AGO_UF, "AGO1522"), (DU145_MF, DU145_UF, "DU145")],
    ):
        S_inMF = dose_response_curve(p_MF, p_MF, doses, rate, field="in")
        S_inUF = dose_response_curve(p_UF, p_UF, doses, rate, field="in")
        S_outMF = dose_response_curve(p_MF, p_MF, doses, rate, field="out")
        ax.semilogy(doses, S_inMF, "b-", label="in-field, half-field (MF, $A_{IF}=0.5$)")
        ax.semilogy(doses, S_inUF, "g--", label="in-field, uniform-field (UF, $A_{IF}=1.0$)")
        ax.semilogy(doses, S_outMF, "r-.", label="out-of-field, half-field")
        ax.set_xlabel("In-field dose D (Gy)")
        ax.set_ylabel("Surviving fraction")
        ax.set_title(f"{cell} — Fig 3 forward model")
        ax.set_ylim(1e-4, 2.0)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)

        rows = list(zip(doses.tolist(), S_inMF.tolist(), S_inUF.tolist(),
                        S_outMF.tolist()))
        write_csv(OUT_DAT / f"fig3_{cell}.csv",
                  ["dose_Gy", "S_in_MF", "S_in_UF", "S_out_MF"], rows)

    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig3_dose_response.png", dpi=160)
    plt.close(fig)
    print(f"  → {OUT_FIG / 'fig3_dose_response.png'}")


# ---------------------------------------------------------------------------
# Figure 4: dose-rate effects at 4 Gy total, four rates (0.59, 0.20, 0.10, 0.05 Gy/min)
# ---------------------------------------------------------------------------

def figure4_like():
    rates = np.array([0.05, 0.10, 0.20, 0.59])  # Gy/min
    total_dose = 4.0

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, (p_MF, p_UF, cell) in zip(
        axes,
        [(AGO_MF, AGO_UF, "AGO1522"), (DU145_MF, DU145_UF, "DU145")],
    ):
        S_in_MF = [fractionated_constant_rate(p_MF, p_MF, total_dose, r,
                                               n_intervals=400, field="in")
                   for r in rates]
        S_in_UF = [fractionated_constant_rate(p_UF, p_UF, total_dose, r,
                                               n_intervals=400, field="in")
                   for r in rates]
        S_out_MF = [fractionated_constant_rate(p_MF, p_MF, total_dose, r,
                                                n_intervals=400, field="out")
                    for r in rates]

        ax.semilogy(rates, S_in_MF, "bo-", label="in-field, MF")
        ax.semilogy(rates, S_in_UF, "g^--", label="in-field, UF")
        ax.semilogy(rates, S_out_MF, "rd-.", label="out-of-field, MF")
        ax.set_xlabel("Average dose-rate (Gy/min)")
        ax.set_ylabel("Surviving fraction at 4 Gy total")
        ax.set_title(f"{cell} — Fig 4 forward model")
        ax.set_xscale("log")
        ax.set_ylim(1e-3, 2.0)
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=8)

        rows = list(zip(rates.tolist(), S_in_MF, S_in_UF, S_out_MF))
        write_csv(OUT_DAT / f"fig4_{cell}.csv",
                  ["rate_Gy_per_min", "S_in_MF", "S_in_UF", "S_out_MF"], rows)

    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig4_dose_rate.png", dpi=160)
    plt.close(fig)
    print(f"  → {OUT_FIG / 'fig4_dose_rate.png'}")


# ---------------------------------------------------------------------------
# Key landmark table — extracted summary
# ---------------------------------------------------------------------------

def landmarks_table():
    rows = []
    for p_TE, p_IC, label in [
        (AGO_MF, AGO_MF, "AGO1522 MF"),
        (AGO_UF, AGO_UF, "AGO1522 UF"),
        (DU145_MF, DU145_MF, "DU145 MF"),
        (DU145_UF, DU145_UF, "DU145 UF"),
    ]:
        S2 = survival_total_continuous(2.0, 2.0 / 35.4, p_TE, p_IC, field="in")
        S4 = survival_total_continuous(4.0, 4.0 / 35.4, p_TE, p_IC, field="in")
        S8 = survival_total_continuous(8.0, 8.0 / 35.4, p_TE, p_IC, field="in")
        # D10 = dose giving 10% survival, brute-force over fine grid
        Ds = np.linspace(0.01, 12.0, 1200)
        Ss = dose_response_curve(p_TE, p_IC, Ds, 0.59, field="in")
        idx = int(np.argmin(np.abs(Ss - 0.10)))
        D10 = Ds[idx]
        rows.append((label, S2, S4, S8, D10))

    out = OUT_DAT / "landmarks.csv"
    write_csv(out, ["model", "S(2Gy)", "S(4Gy)", "S(8Gy)", "D10_Gy"],
              [(r[0], f"{r[1]:.4f}", f"{r[2]:.4e}", f"{r[3]:.4e}", f"{r[4]:.2f}")
               for r in rows])
    print(f"  → {out}")
    print()
    print("  Model landmarks (single dose, in-field, dose-rate 0.59 Gy/min):")
    print(f"  {'model':14s}  {'S(2Gy)':>8s}  {'S(4Gy)':>10s}  {'S(8Gy)':>10s}  {'D10 (Gy)':>9s}")
    for r in rows:
        print(f"  {r[0]:14s}  {r[1]:>8.4f}  {r[2]:>10.4e}  {r[3]:>10.4e}  {r[4]:>9.2f}")


def main():
    print(f"Output figures dir: {OUT_FIG}")
    print(f"Output data dir:    {OUT_DAT}")
    print()
    print("Figure 3 (single-dose dose-response):")
    figure3_like()
    print()
    print("Figure 4 (dose-rate effects at 4 Gy):")
    figure4_like()
    print()
    print("Survival landmarks:")
    landmarks_table()


if __name__ == "__main__":
    main()
