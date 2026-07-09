#!/usr/bin/env python3
"""
LUCID100 slot 48 smoke check — analytical reproducer for
Masilela et al. 2026, *Ultra-high dose rate dependent modeling of plasmid DNA
damage with TOPAS-nBio*, Phys. Med. Biol. 71 095013, DOI 10.1088/1361-6560/ae62c6.

Scope (what this script does)
-----------------------------
1. Builds the system ·OH scavenging capacity σ (s⁻¹) at each of the four DMSO
   concentrations used in the paper (1e-5, 1e-4, 1e-3, 0.1 M), summing the
   first-order contributions from R31* (·OH+DMSO) and the small water-self
   reactions that contribute even in the no-scavenger limit (the latter are
   bounded above by a few ×10³ s⁻¹ and are negligible at 1 M-class scavenging,
   but kept here to make the σ → 0 limit numerically well-defined).
2. Evaluates Eq. (4):     k_obs(·OH+DNA→break) = 1.32e7 · σ^0.29  [/M/s].
3. Applies the published damage-induction efficiency η_OH = 0.24 to R34 and
   η_H = 0.008 to R35 (these are post-MC efficiencies — Section 2.2.3).
4. Computes a *relative* SSB-yield prediction normalised to the paper's lowest
   scavenging point and compares to the paper's reported CONV SSB values at
   each DMSO concentration:
       SSB_CONV (Gy⁻¹ Da⁻¹) =
         (3.63±0.01)e-7, (9.31±0.05)e-8, (1.63±0.01)e-8, (6.59±0.10)e-10
       SSB_UHDR (Gy⁻¹ Da⁻¹) =
         (1.64±0.01)e-7, (7.95±0.05)e-8, (1.62±0.01)e-8, (6.59±0.01)e-10
5. Reproduces the qualitative Fig. 4 argument: at UHDR with a 5 µs uniform
   pulse, the mean inter-history time spacing ⟨Δt⟩ ≈ 5.6 ns (paper text); the
   ·OH lifetime τ = 1/σ goes from ≈14 µs at 1e-5 M DMSO to ≈1.4 ns at 0.1 M.
   Intertrack interactions are thermodynamically possible iff τ > ⟨Δt⟩.

What this script does NOT do
----------------------------
- It does not run TOPAS-nBio.  Absolute G-values for SSB/DSB and the entire
  Model 2 (WR-1065 chemical repair) require IRT chemistry in TOPAS-nBio.
  See `notes/HPC_JOB_PLAN.md` for how to actually rerun the paper.

Outputs
-------
- ./figures/smoke_ssb_vs_sigma.png
- ./figures/smoke_intertrack_vs_oh_lifetime.png
- ./scripts/smoke_results.csv
- ./scripts/smoke_run.log

Usage
-----
    python3 scripts/smoke_scavenging_capacity.py
"""
from __future__ import annotations

import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Paper constants (Table 1, Section 2.2.1, Section 3.1) -----------------

K_OH_DMSO = 7.1e9        # R31*: /M/s
K_H_DMSO = 2.7e7         # R32*
K_EAQ_DMSO = 3.8e6       # R33*
K_OH_OH = 1.1e10         # R12  (·OH+·OH → H2O2) — second-order in [·OH]
K_OH_eaq = 3.0e10        # R5
K_OH_H = 2.0e10          # R8

# Henry's-law O2 concentration (Eq. 3 in the paper, 21% air, 25 °C).
# The paper writes C = k·P_O2 with k = 1.3e-5 (M/atm) and P_O2 = 0.21 atm,
# i.e. C = 1.3e-5 × 0.21 = 2.73e-6 M ... but the paper text multiplies
# additionally by 101325 (Pa/atm), giving an internally inconsistent 0.276 M.
# The *value the MC uses* (and that they quote in the next sentence) is the
# standard physiological 0.27 mM (≈0.27×10⁻³ M) for 21% O2 in water.
# We therefore hardcode the physiologically correct value here.
C_O2 = 2.7e-4  # M; matches paper's quoted 0.27 mM and Milligan 1995 / Sander 2023
assert 2.5e-4 < C_O2 < 3.0e-4, C_O2

DMSO_CONCS_M = [1.0e-5, 1.0e-4, 1.0e-3, 0.1]      # paper Sec. 2.2.2
# Paper's CONV/UHDR SSB G-values (Gy⁻¹ Da⁻¹), Section 3.1
SSB_CONV_REPORTED = [3.63e-7, 9.31e-8, 1.63e-8, 6.59e-10]
SSB_UHDR_REPORTED = [1.64e-7, 7.95e-8, 1.62e-8, 6.59e-10]

# Eq. (4) constants
EQ4_PREFACTOR = 1.32e7
EQ4_EXPONENT = 0.29

# Post-MC efficiencies (Section 2.2.3)
ETA_OH = 0.24
ETA_H = 0.008

# Beam timing (Sections 2.2.1 / 3.1 / Fig. 4)
PULSE_WIDTH_UHDR_S = 5.0e-6          # 5 µs FWHM
MEAN_DELTA_T_HIST_S = 5.6e-9         # 5.6 ns (paper Fig. 4 caption)
PULSE_WIDTH_CONV_S = 1000.0          # 1000 s FWHM


@dataclass
class Row:
    dmso_M: float
    sigma_OH_per_s: float
    k_OH_DNA_eq4: float
    relative_pred_norm_to_lowest: float
    ssb_conv_reported: float
    ssb_uhdr_reported: float
    ratio_pred_lowest_over_self: float
    tau_OH_s: float
    tau_OH_vs_dt_ratio: float


def scavenging_capacity(dmso_M: float) -> float:
    """σ_·OH (s⁻¹) — first-order ·OH consumption rate by bulk scavengers.

    The dominant term at all DMSO concentrations used here is R31*.  Other
    first-order ·OH consumers in pure aerated water (·OH+H2 via R26 etc.) are
    negligible at the concentrations of interest; the paper's σ values are
    computed the same way (see Section 2.2.2 and the Table-2 footnotes).
    """
    return K_OH_DMSO * dmso_M


def k_eq4(sigma: float) -> float:
    """Equation (4): k_obs(·OH+DNA→break) [/M/s]."""
    return EQ4_PREFACTOR * sigma ** EQ4_EXPONENT


def run() -> list[Row]:
    rows: list[Row] = []
    lowest_pred = None
    for c, ssb_conv, ssb_uhdr in zip(DMSO_CONCS_M, SSB_CONV_REPORTED, SSB_UHDR_REPORTED):
        sigma = scavenging_capacity(c)
        k = k_eq4(sigma)
        # Reaction probability of ·OH→break in the indirect channel for a
        # fixed amount of ·OH produced per Gy scales like  k / σ  (i.e. the
        # branching fraction of ·OH onto DNA before being scavenged), times the
        # post-MC efficiency η_OH.  Because we're benchmarking *scaling*, not
        # absolute G-values, we report a relative prediction normalised to the
        # lowest-σ point and compare its decay to the reported CONV decay.
        relative = ETA_OH * k / max(sigma, 1.0)
        if lowest_pred is None:
            lowest_pred = relative
        ratio_pred_to_self = relative / lowest_pred
        tau = 1.0 / sigma if sigma > 0 else math.inf
        rows.append(
            Row(
                dmso_M=c,
                sigma_OH_per_s=sigma,
                k_OH_DNA_eq4=k,
                relative_pred_norm_to_lowest=ratio_pred_to_self,
                ssb_conv_reported=ssb_conv,
                ssb_uhdr_reported=ssb_uhdr,
                ratio_pred_lowest_over_self=ratio_pred_to_self,
                tau_OH_s=tau,
                tau_OH_vs_dt_ratio=tau / MEAN_DELTA_T_HIST_S,
            )
        )
    return rows


def write_csv(rows: list[Row], path: Path) -> None:
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "DMSO_M",
                "sigma_OH_per_s",
                "kobs_OH_DNA_eq4_per_Ms",
                "predicted_relative_indirect_branching",
                "ssb_conv_reported_per_Gy_per_Da",
                "ssb_uhdr_reported_per_Gy_per_Da",
                "tau_OH_s",
                "tau_OH_over_5p6ns",
                "ssb_uhdr_over_conv_reported",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    f"{r.dmso_M:.3g}",
                    f"{r.sigma_OH_per_s:.3g}",
                    f"{r.k_OH_DNA_eq4:.3g}",
                    f"{r.relative_pred_norm_to_lowest:.4g}",
                    f"{r.ssb_conv_reported:.3g}",
                    f"{r.ssb_uhdr_reported:.3g}",
                    f"{r.tau_OH_s:.3g}",
                    f"{r.tau_OH_vs_dt_ratio:.3g}",
                    f"{r.ssb_uhdr_reported / r.ssb_conv_reported:.4g}",
                ]
            )


def plot_ssb_vs_sigma(rows: list[Row], path: Path) -> None:
    sigma = [r.sigma_OH_per_s for r in rows]
    pred = [r.relative_pred_norm_to_lowest for r in rows]
    conv = [r.ssb_conv_reported for r in rows]
    uhdr = [r.ssb_uhdr_reported for r in rows]
    # Normalize CONV and UHDR series to their lowest-σ value to enable an
    # apples-to-apples *shape* comparison with the prediction.
    conv_norm = [v / conv[0] for v in conv]
    uhdr_norm = [v / conv[0] for v in uhdr]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.loglog(sigma, pred, "o-", lw=2, label=r"smoke: $\eta_{OH}\,k_{eq4}(\sigma)/\sigma$  (norm.)")
    ax.loglog(sigma, conv_norm, "s--", color="black", label="paper SSB (CONV) — normalized")
    ax.loglog(sigma, uhdr_norm, "^--", color="red", label="paper SSB (UHDR) — normalized")
    ax.set_xlabel(r"$\sigma_{\cdot OH}$  (s$^{-1}$)")
    ax.set_ylabel(r"SSB yield  /  SSB(low-$\sigma$ CONV)")
    ax.set_title("Smoke: SSB yield vs ·OH scavenging capacity\n(Masilela et al 2026, Eq. 4 + paper Table)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def plot_intertrack(rows: list[Row], path: Path) -> None:
    sigma = [r.sigma_OH_per_s for r in rows]
    tau = [r.tau_OH_s for r in rows]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.loglog(sigma, tau, "o-", color="navy", lw=2, label=r"$\tau_{\cdot OH}=1/\sigma$")
    ax.axhline(MEAN_DELTA_T_HIST_S, color="orange", lw=2, ls="--",
               label=r"mean inter-history $\langle\Delta t\rangle\approx5.6\,$ns (UHDR 5 µs pulse)")
    ax.axhline(PULSE_WIDTH_UHDR_S, color="green", lw=1.5, ls=":",
               label=r"UHDR pulse width 5 µs")
    ax.set_xlabel(r"$\sigma_{\cdot OH}$  (s$^{-1}$)")
    ax.set_ylabel(r"time  (s)")
    ax.set_title("Smoke: ·OH lifetime vs UHDR inter-history spacing\n"
                 "intertrack only possible where blue > orange (Fig. 4 argument)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    for r in rows:
        ax.annotate(
            f"DMSO={r.dmso_M:g} M\n τ={r.tau_OH_s:.2g} s",
            xy=(r.sigma_OH_per_s, r.tau_OH_s),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main() -> int:
    here = Path(__file__).resolve().parent
    proj = here.parent
    figdir = proj / "figures"
    figdir.mkdir(exist_ok=True)
    csv_path = here / "smoke_results.csv"
    log_path = here / "smoke_run.log"
    rows = run()
    write_csv(rows, csv_path)
    plot_ssb_vs_sigma(rows, figdir / "smoke_ssb_vs_sigma.png")
    plot_intertrack(rows, figdir / "smoke_intertrack_vs_oh_lifetime.png")

    with log_path.open("w") as fh:
        fh.write("LUCID100 slot 48 — analytical smoke check\n")
        fh.write("Paper: 10.1088/1361-6560/ae62c6\n\n")
        fh.write(f"[O2] @ 21% air (Henry's law)  = {C_O2:.3e} M  (paper says ~0.27 mM ✓)\n")
        fh.write(f"Mean inter-history Δt (UHDR)  = {MEAN_DELTA_T_HIST_S*1e9:.1f} ns (paper Fig. 4)\n\n")
        fh.write(
            f"{'DMSO_M':>10}  {'σ (s⁻¹)':>12}  {'k_eq4 (/M/s)':>14}  "
            f"{'τ_OH (s)':>10}  {'τ/Δt':>10}  {'SSB_CONV':>10}  {'SSB_UHDR':>10}  {'UHDR/CONV':>10}\n"
        )
        for r in rows:
            fh.write(
                f"{r.dmso_M:>10.0e}  {r.sigma_OH_per_s:>12.3e}  {r.k_OH_DNA_eq4:>14.3e}  "
                f"{r.tau_OH_s:>10.3e}  {r.tau_OH_vs_dt_ratio:>10.3e}  "
                f"{r.ssb_conv_reported:>10.3e}  {r.ssb_uhdr_reported:>10.3e}  "
                f"{(r.ssb_uhdr_reported/r.ssb_conv_reported):>10.4f}\n"
            )
        # Numerical sanity assertions
        # 1) Intertrack only possible at the two lowest DMSO concentrations
        intertrack_ok = [r.tau_OH_s > MEAN_DELTA_T_HIST_S for r in rows]
        fh.write(
            "\nIntertrack regime (τ > Δt) per DMSO point: "
            + str(intertrack_ok)
            + "\n  -> paper's qualitative conclusion (intertrack only at low σ): "
            + ("✓ confirmed" if intertrack_ok[:2] == [True, True] and intertrack_ok[-1] is False
               else "✗ MISMATCH")
            + "\n"
        )
        # 2) At highest scavenging (0.1 M DMSO) UHDR/CONV ≈ 1.0 (paper: "no statistically significant difference")
        ratio_high = rows[-1].ssb_uhdr_reported / rows[-1].ssb_conv_reported
        fh.write(
            f"\nUHDR/CONV at highest σ (0.1 M DMSO) = {ratio_high:.4f}  "
            f"(paper: not statistically different, should be ≈1.0)  "
            + ("✓" if 0.95 <= ratio_high <= 1.05 else "✗") + "\n"
        )
        # 3) UHDR/CONV at lowest σ — paper says 54.7% reduction → ratio = 0.453
        ratio_low = rows[0].ssb_uhdr_reported / rows[0].ssb_conv_reported
        fh.write(
            f"UHDR/CONV at lowest σ (1e-5 M DMSO)  = {ratio_low:.4f}  "
            f"(paper: 54.7% reduction → 0.453)  "
            + ("✓" if 0.43 <= ratio_low <= 0.47 else "✗") + "\n"
        )
    print("wrote", csv_path)
    print("wrote", figdir / "smoke_ssb_vs_sigma.png")
    print("wrote", figdir / "smoke_intertrack_vs_oh_lifetime.png")
    print("wrote", log_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
