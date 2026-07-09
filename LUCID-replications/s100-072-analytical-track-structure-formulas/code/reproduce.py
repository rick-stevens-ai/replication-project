#!/usr/bin/env python3
"""
Reproduction of Kundrat et al., Sci. Rep. 10:15775 (2020),
"Analytical formulas representing track-structure simulations on DNA damage
induced by protons and light ions at radiotherapy-relevant energies"
DOI: 10.1038/s41598-020-72857-z

Reproduces Figures 1-5 (SB, SSB, DSB, DSB clusters, DSB sites vs LET)
using Eqs. (1) and (2) with parameters from Tables 1 and 2.

Eq. (1)  (SB, SSB):
    Yield = p1 - (p2*LET)^p3 - p4 / (1 + log^2(LET/p5))

Eq. (2)  (DSB, DSB clusters, DSB sites):
    Yield = (p1 + (p2*LET)^p3) / (1 + (p4*LET)^p5)

Where Yield is in Gy^-1 GBp^-1, LET in keV/um, log = natural logarithm.

When a parameter is "N.A." in the paper's tables, the corresponding term
was dropped (zeroed) per the paper's text.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT_FIG = HERE.parent / "figures"
OUT_EVD = HERE.parent / "evidence"
OUT_FIG.mkdir(parents=True, exist_ok=True)
OUT_EVD.mkdir(parents=True, exist_ok=True)

# -------------------- Analytical formulas --------------------

def yield_eq1(LET, p1, p2, p3, p4, p5):
    """SB/SSB form. Drop a sub-term by passing None or NaN for that p."""
    LET = np.asarray(LET, dtype=float)
    out = np.full_like(LET, float(p1), dtype=float)
    if p2 is not None and not (isinstance(p2, float) and math.isnan(p2)) \
       and p3 is not None and not (isinstance(p3, float) and math.isnan(p3)):
        out = out - (p2 * LET) ** p3
    if p4 is not None and not (isinstance(p4, float) and math.isnan(p4)) \
       and p5 is not None and not (isinstance(p5, float) and math.isnan(p5)):
        out = out - p4 / (1.0 + np.log(LET / p5) ** 2)
    return out


def yield_eq2(LET, p1, p2, p3, p4, p5):
    """DSB / DSB cluster / DSB site form."""
    LET = np.asarray(LET, dtype=float)
    num = float(p1)
    if p2 is not None and not (isinstance(p2, float) and math.isnan(p2)) \
       and p3 is not None and not (isinstance(p3, float) and math.isnan(p3)):
        num = num + (p2 * LET) ** p3
    denom = 1.0
    if p4 is not None and not (isinstance(p4, float) and math.isnan(p4)) \
       and p5 is not None and not (isinstance(p5, float) and math.isnan(p5)):
        denom = 1.0 + (p4 * LET) ** p5
    return num / denom


# -------------------- Parameter tables (from paper Tables 1 & 2) --------------------
# Ion order: H, He, Li, Be, B, C, N, O, Ne
IONS = ["H", "He", "Li", "Be", "B", "C", "N", "O", "Ne"]

# Convenience: NaN sentinel for N.A.
NA = float("nan")

# Table 1 - SB
SB_TOTAL = {
    "H":  (170, 1.335,  0.7023,  8.541,  6.902),
    "He": (170, 0.4632, 0.8913, 11.81,   7.542),
    "Li": (170, 0.405,  0.8499, 12.25,   8.795),
    "Be": (170, 0.6563, 0.7454, 10.84,   7.203),
    "B":  (170, 0.7101, 0.7173, 10.36,   9.02),
    "C":  (170, 0.9285, 0.6785, 10.02,   9.499),
    "N":  (170, 0.9985, 0.6579,  9.627, 11.12),
    "O":  (170, 1.754,  0.5993,  9.64,   8.154),
    "Ne": (170, 2.388,  0.5616,  8.841,  9.224),
}
SB_DIRECT = {
    "H":  (64, NA,        NA,    3.532, 12.51),
    "He": (64, NA,        NA,    4.015, 20.46),
    "Li": (64, 0.004687,  3.354, 3.525, 15.07),
    "Be": (64, 0.005799,  2.023, 4.085, 16.17),
    "B":  (64, 0.006684,  1.662, 3.704, 15.59),
    "C":  (64, 0.006881,  1.621, 3.802, 16.69),
    "N":  (64, 0.006951,  1.485, 3.747, 18.77),
    "O":  (64, 0.01046,   1.168, 3.224, 19.08),
    "Ne": (64, 0.009527,  1.127, 3.748, 18.59),
}
SB_INDIRECT = {
    "H":  (106, 1.076, 0.8189, 5.679,  9.223),
    "He": (106, 1.815, 0.6758, 5.652, 13.93),
    "Li": (106, 1.784, 0.6373, 6.574, 13.43),
    "Be": (106, 3.298, 0.5625, 5.735, 13.88),
    "B":  (106, 4.198, 0.5332, 4.87,  13.1),
    "C":  (106, 6.272, 0.5007, 4.717, 15.26),
    "N":  (106, 7.44,  0.4832, 4.843, 17.03),
    "O":  (106,14.64,  0.4437, 3.151, 15.89),
    "Ne": (106,20.28,  0.4207, 3.219, 28.1),
}

# Table 1 - SSB
SSB_TOTAL = {
    "H":  (156, 0.9613, 0.9173, 10.21,  7.124),
    "He": (156, 1.681,  0.7616,  9.093, 8.052),
    "Li": (156, 1.856,  0.7023,  9.737, 8.993),
    "Be": (156, 3.771,  0.6105,  7.937, 7.851),
    "B":  (156, 5.414,  0.5695,  6.837, 8.997),
    "C":  (156, 9.511,  0.5256,  5.818, 8.409),
    "N":  (156,12.73,   0.5006,  5.67,  8.453),
    "O":  (156,21.17,   0.4693,  4.926, 6.674),
    "Ne": (156,52.47,   0.4215,  NA,    NA),
}
SSB_DIRECT = {
    "H":  (60, 39.79,  0.2471, 4.189, 35.17),
    "He": (60,  1.765, 0.5268, 1.127,  1.642),
    "Li": (60,  0.3056,0.7,    4.357,  8.53),
    "Be": (60,  0.2586,0.6959, 5.034, 11.37),
    "B":  (60,  0.298, 0.6564, 4.575, 12.74),
    "C":  (60,  0.3865,0.6131, 4.429, 16.03),
    "N":  (60,  0.3666,0.605,  4.612, 19.38),
    "O":  (60,  0.651, 0.5414, 3.499, 20.59),
    "Ne": (60,  0.8246,0.5072, 3.615, 24.24),
}
SSB_INDIRECT = {
    "H":  (102, 2.438, 0.7084, 4.389,  7.916),
    "He": (102, 3.242, 0.6263, 4.999, 12.97),
    "Li": (102, 3.067, 0.5961, 6.479, 13.54),
    "Be": (102, 6.137, 0.5251, 5.421, 14.58),
    "B":  (102, 9.016, 0.4909, 4.265, 14.22),
    "C":  (102,14.25,  0.4602, 4.069, 16.06),
    "N":  (102,19.0,   0.4397, 4.008, 17.7),
    "O":  (102,40.6,   0.4036, 2.215, 15.94),
    "Ne": (102,65.9,   0.3788, 2.26,  30.59),
}

# Table 2 - DSB
DSB_TOTAL = {
    "H":  (6.8, 0.1835, 0.9583, NA,       NA),
    "He": (6.8, 0.1679, 0.9704, 0.004323, 1.359),
    "Li": (6.8, 0.2148, 0.864,  0.00399,  0.9872),
    "Be": (6.8, 0.2148, 0.9999, 0.009586, 1.019),
    "B":  (6.8, 0.2303, 0.9711, 0.009576, 1.016),
    "C":  (6.8, 0.2052, 1.02,   0.009922, 1.106),
    "N":  (6.8, 0.2043, 1.023,  0.01002,  1.121),
    "O":  (6.8, 0.2122, 1.077,  0.01311,  1.146),
    "Ne": (6.8, 0.1916, 1.112,  0.01261,  1.204),
}
DSB_DIRECT = {
    "H":  (2.8, 0.07011, 1.231, NA,       NA),
    "He": (2.8, 0.08076, 0.816, NA,       NA),
    "Li": (2.8, 0.07501, 0.7078,NA,       NA),
    "Be": (2.8, 0.08651, 0.9131,0.003924, 0.8367),
    "B":  (2.8, 0.1168,  0.9562,0.009723, 0.8111),
    "C":  (2.8, 0.09374, 1.076, 0.01033,  1.006),
    "N":  (2.8, 0.09184, 1.103, 0.01089,  1.05),
    "O":  (2.8, 0.108,   1.184, 0.01773,  1.088),
    "Ne": (2.8, 0.09018, 1.34,  0.01838,  1.263),
}
DSB_INDIRECT = {
    "H":  (2.2, 0.03598, 0.5834,NA,        NA),
    "He": (2.2, 0.02683, 0.6349,0.002725, 2.022),
    "Li": (2.2, 0.03443, 0.6439,0.002556, 1.057),
    "Be": (2.2, 0.03583, 0.7321,0.003678, 1.088),
    "B":  (2.2, 0.03316, 0.7289,0.003393, 1.133),
    "C":  (2.2, 0.03152, 0.6538,0.002669, 1.114),
    "N":  (2.2, 0.03022, 0.6392,0.002471, 1.13),
    "O":  (2.2, 0.03304, 0.6638,0.002959, 1.085),
    "Ne": (2.2, 0.0308,  0.5917,0.002172, 1.081),
}

# Table 2 - DSB clusters
DSBC_TOTAL = {
    "H":  (0.07, 0.01532,  2.396, NA,        NA),
    "He": (0.07, 0.01015,  1.794, 0.003817,  3.255),
    "Li": (0.07, 0.008907, 2.004, 0.004511,  2.064),
    "Be": (0.07, 0.007692, 1.736, 0.003448,  2.088),
    "B":  (0.07, 0.007604, 1.726, 0.003789,  1.991),
    "C":  (0.07, 0.006858, 1.498, 0.002778,  2.208),
    "N":  (0.07, 0.00661,  1.418, 0.002577,  2.194),
    "O":  (0.07, 0.007119, 1.514, 0.003193,  2.095),
    "Ne": (0.07, 0.006894, 1.418, 0.002865,  2.108),
}
DSBC_DIRECT = {
    "H":  (0.018, 0.01152,  2.844, NA,        NA),
    "He": (0.018, 0.006072, 1.762, NA,        NA),
    "Li": (0.018, 0.005925, 2.183, 0.004068,  1.607),
    "Be": (0.018, 0.00427,  1.746, 0.002058,  2.09),
    "B":  (0.018, 0.004394, 1.817, 0.002721,  1.85),
    "C":  (0.018, 0.003932, 1.678, 0.002187,  2.14),
    "N":  (0.018, 0.003585, 1.519, 0.00184,   2.216),
    "O":  (0.018, 0.003711, 1.533, 0.002088,  2.046),
    "Ne": (0.018, 0.003522, 1.485, 0.001971,  2.097),
}
DSBC_INDIRECT = {
    "H":  (0.004, 0.002534, 1.952, NA,        NA),
    "He": (0.004, 0.00101,  1.464, NA,        NA),
    "Li": (0.004, 0.0006276,1.35,  NA,        NA),
    "Be": (0.004, 0.00048,  1.242, 0.001365,  5.796),
    "B":  (0.004, 0.0003195,1.1,   0.001242, 37.32),
    "C":  (0.004, 0.0005724,1.265, 0.001473,  1.094),
    "N":  (0.004, 0.0004915,1.207, 0.00144,   0.9436),
    "O":  (0.004, 0.0005992,1.322, 0.002002,  1.108),
    "Ne": (0.004, 0.001511, 1.71,  0.007381,  1.29),
}

# Table 2 - DSB sites
DSBS_TOTAL = {
    "H":  (6.8, 0.1773, 0.9314, NA,        NA),
    "He": (6.8, 0.1471, 1.038,  0.006239,  1.582),
    "Li": (6.8, 0.1653, 0.8782, 0.004284,  1.406),
    "Be": (6.8, 0.1425, 0.95,   0.005151,  1.407),
    "B":  (6.8, 0.1587, 0.8714, 0.004345,  1.389),
    "C":  (6.8, 0.156,  0.9214, 0.005245,  1.395),
    "N":  (6.8, 0.1641, 0.875,  0.004607,  1.391),
    "O":  (6.8, 0.1749, 0.8722, 0.004987,  1.347),
    "Ne": (6.8, 0.1797, 0.8657, 0.004917,  1.346),
}
DSBS_DIRECT = {
    "H":  (2.8, 0.06901, 1.196, NA,        NA),
    "He": (2.8, 0.06555, 1.023, 0.003748,  1.763),
    "Li": (2.8, 0.06093, 0.9556,0.003178,  1.402),
    "Be": (2.8, 0.06199, 0.9224,0.003301,  1.322),
    "B":  (2.8, 0.063,   0.9255,0.003655,  1.305),
    "C":  (2.8, 0.06191, 0.9903,0.004525,  1.369),
    "N":  (2.8, 0.06171, 0.9649,0.004156,  1.389),
    "O":  (2.8, 0.0664,  0.969, 0.004754,  1.341),
    "Ne": (2.8, 0.06408, 1.023, 0.0053,    1.386),
}
DSBS_INDIRECT = {
    "H":  (2.2, 0.035,   0.5841,NA,        NA),
    "He": (2.2, 0.02656, 0.6415,0.002875,  1.994),
    "Li": (2.2, 0.03349, 0.6485,0.002736,  1.109),
    "Be": (2.2, 0.0341,  0.7328,0.003678,  1.136),
    "B":  (2.2, 0.03117, 0.7196,0.003265,  1.182),
    "C":  (2.2, 0.02946, 0.6435,0.002585,  1.166),
    "N":  (2.2, 0.02776, 0.6216,0.00231,   1.189),
    "O":  (2.2, 0.03004, 0.6396,0.002652,  1.136),
    "Ne": (2.2, 0.02847, 0.5684,0.002006,  1.128),
}


# -------------------- Plot helpers --------------------

ION_COLORS = {
    "H":  "#000000",
    "He": "#1f77b4",
    "Li": "#ff7f0e",
    "Be": "#2ca02c",
    "B":  "#d62728",
    "C":  "#9467bd",
    "N":  "#8c564b",
    "O":  "#e377c2",
    "Ne": "#17becf",
}


def make_fig(name, formula, totals, directs, indirects, ylabel, ymax,
             title, evd_lines, ymin=0.0, semilog=False):
    """Generate one of the paper's figures (Figs 1-5)."""
    LET = np.logspace(np.log10(0.1), np.log10(1000), 400)
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    for ion in IONS:
        c = ION_COLORS[ion]
        y_t = formula(LET, *totals[ion])
        y_d = formula(LET, *directs[ion])
        y_i = formula(LET, *indirects[ion])
        ax.plot(LET, y_t, "-",  color=c, lw=1.4, label=ion)
        ax.plot(LET, y_d, "--", color=c, lw=0.9, alpha=0.7)
        ax.plot(LET, y_i, ":",  color=c, lw=0.9, alpha=0.7)
    ax.set_xscale("log")
    if semilog:
        ax.set_yscale("log")
    ax.set_xlim(0.1, 1000)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("LET (keV/µm)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(ncol=3, fontsize=8, loc="best")
    fig.tight_layout()
    out = OUT_FIG / name
    fig.savefig(out, dpi=160)
    plt.close(fig)
    # Sample values for sanity logging
    LET_samples = np.array([0.5, 1.0, 5.0, 20.0, 100.0, 200.0])
    for ion in IONS:
        y_t = formula(LET_samples, *totals[ion])
        y_d = formula(LET_samples, *directs[ion])
        y_i = formula(LET_samples, *indirects[ion])
        evd_lines.append(f"{title:18s} ion={ion:2s} LET={LET_samples.tolist()} "
                         f"total={np.round(y_t,3).tolist()} "
                         f"direct={np.round(y_d,3).tolist()} "
                         f"indirect={np.round(y_i,3).tolist()}")
    return out


def main():
    evd_lines = []
    figs = []

    figs.append(make_fig(
        "fig1_SB.png", yield_eq1,
        SB_TOTAL, SB_DIRECT, SB_INDIRECT,
        "SB (Gy$^{-1}$ Gbp$^{-1}$)", ymax=180,
        title="Fig 1 — Strand breakage (SB)",
        evd_lines=evd_lines,
    ))
    figs.append(make_fig(
        "fig2_SSB.png", yield_eq1,
        SSB_TOTAL, SSB_DIRECT, SSB_INDIRECT,
        "SSB (Gy$^{-1}$ Gbp$^{-1}$)", ymax=180,
        title="Fig 2 — Single-strand breaks (SSB)",
        evd_lines=evd_lines,
    ))
    figs.append(make_fig(
        "fig3_DSB.png", yield_eq2,
        DSB_TOTAL, DSB_DIRECT, DSB_INDIRECT,
        "DSB (Gy$^{-1}$ Gbp$^{-1}$)", ymax=22,
        title="Fig 3 — Double-strand breaks (DSB)",
        evd_lines=evd_lines,
    ))
    figs.append(make_fig(
        "fig4_DSBclusters.png", yield_eq2,
        DSBC_TOTAL, DSBC_DIRECT, DSBC_INDIRECT,
        "DSB clusters (Gy$^{-1}$ Gbp$^{-1}$)", ymax=3.0,
        title="Fig 4 — DSB clusters",
        evd_lines=evd_lines,
    ))
    figs.append(make_fig(
        "fig5_DSBsites.png", yield_eq2,
        DSBS_TOTAL, DSBS_DIRECT, DSBS_INDIRECT,
        "DSB sites (Gy$^{-1}$ Gbp$^{-1}$)", ymax=17,
        title="Fig 5 — DSB sites",
        evd_lines=evd_lines,
    ))

    # Save a per-ion table of yields at selected reference LET points
    LET_ref = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
    with open(OUT_EVD / "yield_samples.tsv", "w") as fh:
        fh.write("damage\teffect\tion\t" +
                 "\t".join(f"LET={L}" for L in LET_ref) + "\n")
        cases = [
            ("SB",         "total",    yield_eq1, SB_TOTAL),
            ("SB",         "direct",   yield_eq1, SB_DIRECT),
            ("SB",         "indirect", yield_eq1, SB_INDIRECT),
            ("SSB",        "total",    yield_eq1, SSB_TOTAL),
            ("SSB",        "direct",   yield_eq1, SSB_DIRECT),
            ("SSB",        "indirect", yield_eq1, SSB_INDIRECT),
            ("DSB",        "total",    yield_eq2, DSB_TOTAL),
            ("DSB",        "direct",   yield_eq2, DSB_DIRECT),
            ("DSB",        "indirect", yield_eq2, DSB_INDIRECT),
            ("DSBcluster", "total",    yield_eq2, DSBC_TOTAL),
            ("DSBcluster", "direct",   yield_eq2, DSBC_DIRECT),
            ("DSBcluster", "indirect", yield_eq2, DSBC_INDIRECT),
            ("DSBsite",    "total",    yield_eq2, DSBS_TOTAL),
            ("DSBsite",    "direct",   yield_eq2, DSBS_DIRECT),
            ("DSBsite",    "indirect", yield_eq2, DSBS_INDIRECT),
        ]
        for damage, effect, fn, tbl in cases:
            for ion in IONS:
                y = fn(np.array(LET_ref), *tbl[ion])
                fh.write(f"{damage}\t{effect}\t{ion}\t" +
                         "\t".join(f"{v:.4f}" for v in y) + "\n")

    with open(OUT_EVD / "run_log.txt", "w") as fh:
        fh.write("Reproduction of Kundrat et al. 2020, Sci. Rep. 10:15775\n")
        fh.write("=" * 70 + "\n")
        fh.write("Generated figures:\n")
        for f in figs:
            fh.write(f"  {f}\n")
        fh.write("\nSample yields per ion / damage class at "
                 "[0.5, 1, 5, 20, 100, 200] keV/um:\n")
        for line in evd_lines:
            fh.write(line + "\n")

    # Sanity / acceptance probes
    print("[acceptance probes]")
    # Low-LET limits (text claims): SB total ~170, direct ~64, indirect ~106
    # SSB total ~156, direct ~60, indirect ~102; DSB total ~6.8;
    # DSB cluster total ~0.07; DSB site total ~6.8.
    low = 0.3
    for ion in ["H", "He", "C", "Ne"]:
        print(f"  ion={ion} LET={low} keV/um:")
        print(f"    SB  total = {yield_eq1(low, *SB_TOTAL[ion]):.2f}  "
              f"(target ~170)")
        print(f"    SSB total = {yield_eq1(low, *SSB_TOTAL[ion]):.2f}  "
              f"(target ~156)")
        print(f"    DSB total = {yield_eq2(low, *DSB_TOTAL[ion]):.3f}  "
              f"(target ~6.8)")
        print(f"    DSBclu    = {yield_eq2(low, *DSBC_TOTAL[ion]):.4f}  "
              f"(target ~0.07)")
        print(f"    DSBsite   = {yield_eq2(low, *DSBS_TOTAL[ion]):.3f}  "
              f"(target ~6.8)")

    # Peak DSB site yield should be ~15 sites/Gy/Gbp at LET 100-200 keV/um
    LET_grid = np.logspace(-1, 3, 4000)
    print("  Peak DSB site total yield per ion (paper target ~15):")
    for ion in IONS:
        y = yield_eq2(LET_grid, *DSBS_TOTAL[ion])
        i = int(np.argmax(y))
        print(f"    {ion}: peak={y[i]:.2f} at LET={LET_grid[i]:.1f} keV/um")

    # Peak DSB ~20 at low energy ions
    print("  Peak DSB total yield per ion (paper target ~20 for high LET):")
    for ion in IONS:
        y = yield_eq2(LET_grid, *DSB_TOTAL[ion])
        i = int(np.argmax(y))
        print(f"    {ion}: peak={y[i]:.2f} at LET={LET_grid[i]:.1f} keV/um")

    print(f"\nFigures written to {OUT_FIG}")
    print(f"Evidence written to {OUT_EVD}")


if __name__ == "__main__":
    main()
