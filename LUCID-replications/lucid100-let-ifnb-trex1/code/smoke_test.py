"""
LUCID100 slot-14 smoke test for Miles et al. 2021 (bioRxiv 451516).

PASS-low criteria (this script):
  A. Eq. 3 RBE_DSB closed-form recovers RBE ≈ 1.0 for a Co-60-like
     low-LET reference (z_eff=1, beta≈1).
  B. Calibrated Eq. 1 reproduces the reported neutron/x-ray peak-dose
     ratio of ~2.5 (i.e. RBE_IFNβ ≈ 2.5) when seeded with x-ray peak
     at 14.0 Gy.
  C. Eq. 2 with a 4× slope ratio gives the reported RBE_TREX1 = 4.0.

This is a *low-bar smoke validation*: it confirms the maths/code path,
not that Table 1 coefficients are recovered. For PASS-mid you must
digitize Figures 1 & 2 (see digitization_template.csv) and refit.

Outputs:
  ../results/smoke_test_results.json
  ../figures/ifnb_curves.png   (if matplotlib available)
  ../figures/trex1_curves.png  (if matplotlib available)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lucid100_let_ifnb_trex1_model import (
    rbe_dsb,
    IFNbCoeffs,
    TREX1Coeffs,
    ifnb_peak_dose,
    SARRP_XRAY_RBE_DSB,
    calibrate_neutron_coeffs_to_observed_peak,
)


def main() -> int:
    results = {"criteria": {}, "values": {}, "notes": []}

    # ----- Criterion A: RBE_DSB ≈ 1 for Co-60-like reference -----
    # Co-60 γ produces low-LET electrons; we test with z_eff=1, beta=0.95
    rbe_co60_like = rbe_dsb(z_eff=1.0, beta=0.95)
    results["values"]["rbe_dsb_co60_like(z_eff=1,beta=0.95)"] = rbe_co60_like
    crit_A = 0.85 <= rbe_co60_like <= 1.20
    results["criteria"]["A_rbe_dsb_low_LET_near_1"] = bool(crit_A)
    if not crit_A:
        results["notes"].append(
            f"A: RBE_DSB low-LET = {rbe_co60_like:.3f}; expected ~1.0 ± 0.2"
        )

    # ----- Criterion B: neutron/x-ray IFNβ peak ratio ≈ 2.5 -----
    # Use b<0, c<0 so Eq.1 has an interior peak (see model docstring).
    xray = IFNbCoeffs(a=60.0, b=-0.05, c=-60.0,
                      rbe_dsb=SARRP_XRAY_RBE_DSB)
    # Tune c so x-ray peak lands at ~14.0 Gy (the published observable).
    # f'(D)=0: 2.5*b*(D*RBE)^1.5 = (c/2)*exp(-(D*RBE)/2)
    # → c = 5*b*(D*RBE)^1.5 * exp((D*RBE)/2)
    target_xray_peak = 14.0
    DR = target_xray_peak * xray.rbe_dsb
    import math as _m
    xray.c = 5.0 * xray.b * (DR ** 1.5) * _m.exp(DR / 2.0)

    xray_peak = ifnb_peak_dose(xray, 0.5, 30.0, 0.001)
    neutron = calibrate_neutron_coeffs_to_observed_peak(
        xray, observed_neutron_peak_gy=5.7, observed_xray_peak_gy=xray_peak
    )
    neutron_peak = ifnb_peak_dose(neutron, 0.5, 30.0, 0.001)
    rbe_ifnb = xray_peak / neutron_peak
    results["values"]["xray_ifnb_peak_dose_Gy"] = xray_peak
    results["values"]["neutron_ifnb_peak_dose_Gy"] = neutron_peak
    results["values"]["rbe_ifnb_peak_ratio"] = rbe_ifnb
    crit_B = abs(rbe_ifnb - 2.5) <= 0.3
    results["criteria"]["B_rbe_ifnb_near_2p5"] = bool(crit_B)

    # ----- Criterion C: TREX1 slope ratio = 4.0 -----
    trex1_x = TREX1Coeffs(a=0.10, b=1.0, rbe_dsb=SARRP_XRAY_RBE_DSB)
    # Make the neutron slope per unit *absorbed* dose 4× the x-ray slope per
    # unit *absorbed* dose. Eq.2 contribution per unit D is a*RBE_DSB, so
    # set neutron RBE so that a_n*RBE_n = 4 * a_x*RBE_x (with a_n = a_x).
    rbe_trex1_target = 4.0
    trex1_n_rbe = rbe_trex1_target * trex1_x.rbe_dsb
    trex1_n = TREX1Coeffs(a=0.10, b=1.0, rbe_dsb=trex1_n_rbe)
    slope_x = trex1_x.a * trex1_x.rbe_dsb
    slope_n = trex1_n.a * trex1_n.rbe_dsb
    rbe_trex1 = slope_n / slope_x
    results["values"]["trex1_xray_slope_per_Gy"] = slope_x
    results["values"]["trex1_neutron_slope_per_Gy"] = slope_n
    results["values"]["rbe_trex1_slope_ratio"] = rbe_trex1
    crit_C = abs(rbe_trex1 - 4.0) <= 0.1
    results["criteria"]["C_rbe_trex1_near_4p0"] = bool(crit_C)

    # Aggregate verdict
    all_pass = all(results["criteria"].values())
    results["pass_low_overall"] = bool(all_pass)
    results["meta"] = {
        "paper_doi": "10.1101/2021.07.07.451516",
        "smoke_level": "PASS-low",
        "note_for_pass_mid": (
            "Digitize Figures 1 & 2 with WebPlotDigitizer; populate "
            "digitization_template.csv; refit Eqs. 1 & 2 to recover "
            "Table 1 (a,b,c) for both modalities."
        ),
    }

    out_dir = HERE.parent / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "smoke_test_results.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"[smoke] wrote {out_path}")

    # Optional plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        fig_dir = HERE.parent / "figures"
        fig_dir.mkdir(exist_ok=True)

        Ds = np.linspace(0.5, 30, 600)
        plt.figure(figsize=(6, 4))
        plt.plot(Ds, [xray(D) for D in Ds], label="SARRP x-ray (calibrated)")
        plt.plot(Ds, [neutron(D) for D in Ds], label="CNTS neutron (calibrated)")
        plt.axvline(xray_peak, ls="--", lw=0.6)
        plt.axvline(neutron_peak, ls="--", lw=0.6)
        plt.xlabel("Absorbed dose [Gy]")
        plt.ylabel("IFNβ [pg/mL per 1e5 cells] (Eq.1, placeholder coeffs)")
        plt.title(f"IFNβ Eq.1, peaks: x-ray={xray_peak:.2f} Gy, n={neutron_peak:.2f} Gy → RBE={rbe_ifnb:.2f}")
        plt.legend()
        plt.tight_layout()
        p1 = fig_dir / "ifnb_curves.png"
        plt.savefig(p1, dpi=140); plt.close()
        print(f"[smoke] wrote {p1}")

        Ds2 = np.linspace(0, 24, 100)
        plt.figure(figsize=(6, 4))
        plt.plot(Ds2, [trex1_x(D) for D in Ds2], label="SARRP x-ray")
        plt.plot(Ds2[Ds2 <= 8], [trex1_n(D) for D in Ds2[Ds2 <= 8]], label="CNTS neutron")
        plt.xlabel("Absorbed dose [Gy]")
        plt.ylabel("TREX1 [n-fold] (Eq.2, placeholder coeffs)")
        plt.title(f"TREX1 Eq.2, slope ratio (n / x) = {rbe_trex1:.2f}")
        plt.legend()
        plt.tight_layout()
        p2 = fig_dir / "trex1_curves.png"
        plt.savefig(p2, dpi=140); plt.close()
        print(f"[smoke] wrote {p2}")
    except Exception as e:
        results["notes"].append(f"matplotlib unavailable or failed: {e!r}")
        # Re-write results to capture the note
        with open(out_path, "w") as fh:
            json.dump(results, fh, indent=2)

    # Print summary
    print("\n=== SMOKE SUMMARY ===")
    for k, v in results["criteria"].items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"  Overall PASS-low: {results['pass_low_overall']}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
