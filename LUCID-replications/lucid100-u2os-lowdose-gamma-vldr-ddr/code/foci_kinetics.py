"""
foci_kinetics.py — minimal 53BP1 foci formation+resolution model for the
Plodowska 2025 (DNA Repair, U2OS VLDR gamma DDR) replication scaffold.

This is the *kinetic backbone* used in essentially every gamma-induced DSB
foci paper since Rothkamm/Lobrich 2003 and operationalised analytically by
Lengert et al. (Sci Rep 2018, 8:17472 — already in the LUCID portfolio as
slot 2 / lucid-autofoci-detection). It is intentionally minimal so that, once
the next analyst has digitised Plodowska Fig 1/2/3, only the data file path
needs to change.

Model
-----
  dN/dt  =  R(t)  -  k_repair * N(t)
where N(t) is the per-cell mean number of 53BP1 foci and R(t) is the
instantaneous induction rate, which depends on the exposure mode:

* Acute (CD, 1 Gy at 1 Gy/min):
      R(t) = Y_acute * delta(t - t0)            (impulse at t0)
      => N(t>=t0) = Y_acute * exp(-k_repair*(t-t0))

* Chronic / very low dose rate (AD, 5.9 mGy at 31 uGy/h or 10.5 mGy at 55 uGy/h):
      R(t) = Y_per_Gy * dose_rate_Gy_per_h / 3600       (foci per cell per second)
      for 0 <= t <= T_exposure, else 0.
  Closed-form solution during exposure:
      N(t) = (R/k) * (1 - exp(-k*t))
  After exposure ends at T:
      N(t>T) = N(T) * exp(-k_repair*(t-T))

* Adapt-then-challenge (AD followed by CD at t = T_ad + gap):
      N solved piecewise: chronic build during [0, T_ad], free decay during
      gap, then impulse Y_acute added at t = T_ad + gap, continued decay.

Parameters
----------
Y_per_Gy   : foci induced per Gy per cell (acute reference; ~30-40 for
             53BP1 in typical mammalian lines).
k_repair   : first-order repair rate (1/h); ~0.3-0.7/h for short-component
             53BP1 foci in human cells.
T_ad_h     : duration of the AD exposure in hours.
dose_rate_Gy_per_h : VLDR rate during AD (e.g. 31e-6 or 55e-6 Gy/h).
gap_h      : time between end of AD and the CD (publishers typically use 0
             or a small fixed interval; refit once the methods section is in hand).
CD_dose_Gy : challenging dose (paper: 1.0 Gy).

ATM perturbation handle
-----------------------
KU-55933 reduces (does not abolish) Y_acute for the CD-only condition and
in Plodowska 2025 *fails to inhibit* AD-only foci induction. We expose a
simple modifier dict
    atm_modifier = {
        "AD_yield_factor":      1.00,   # KU has ~no effect on AD-only
        "CD_yield_factor":      0.40,   # KU reduces CD-only by ~60%
        "AD_plus_CD_factor":    1.00,   # KU does not abolish AD+CD signal
    }
that scales the per-condition yield. Refit these once digitised data exists.

Usage
-----
  python3 foci_kinetics.py --demo
      Synthesises a plausible 5-condition curve set and writes
      results/smoke_synthetic.csv + figures/smoke_synthetic.png.

  python3 foci_kinetics.py --fit data/digitized_fig.csv
      (stub — wired to scipy.optimize.curve_fit once data file is in place)
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

@dataclass
class FociParams:
    Y_per_Gy: float = 35.0          # foci/cell/Gy (acute reference)
    k_repair: float = 0.45          # 1/h  (short-component 53BP1)
    dose_rate_AD_Gy_per_h: float = 31e-6    # 31 uGy/h
    T_ad_h: float = 5.9e-3 / 31e-6           # = 190.3 h to deliver 5.9 mGy at 31 uGy/h
    CD_dose_Gy: float = 1.0
    gap_h: float = 0.0              # time between end of AD and CD start


def chronic_N(t_h: float, R_foci_per_h: float, k: float, T_h: float) -> float:
    """Foci/cell at time t (h) under chronic exposure of length T_h."""
    if t_h <= 0:
        return 0.0
    if t_h <= T_h:
        return (R_foci_per_h / k) * (1.0 - math.exp(-k * t_h))
    # Post-exposure free decay from N(T)
    NT = (R_foci_per_h / k) * (1.0 - math.exp(-k * T_h))
    return NT * math.exp(-k * (t_h - T_h))


def acute_N(t_h: float, t0_h: float, Y: float, k: float) -> float:
    """Foci/cell at time t (h) for an acute impulse of Y foci/cell at t0_h."""
    if t_h < t0_h:
        return 0.0
    return Y * math.exp(-k * (t_h - t0_h))


def ad_curve(t_h: float, p: FociParams, atm_factor: float = 1.0) -> float:
    """AD-only condition."""
    R = atm_factor * p.Y_per_Gy * p.dose_rate_AD_Gy_per_h   # foci/cell/h
    return chronic_N(t_h, R, p.k_repair, p.T_ad_h)


def cd_curve(t_h: float, p: FociParams, atm_factor: float = 1.0,
             t0_cd_h: float | None = None) -> float:
    """CD-only condition."""
    t0 = 0.0 if t0_cd_h is None else t0_cd_h
    Y = atm_factor * p.Y_per_Gy * p.CD_dose_Gy
    return acute_N(t_h, t0, Y, p.k_repair)


def ad_then_cd_curve(t_h: float, p: FociParams,
                     ad_factor: float = 1.0, cd_factor: float = 1.0,
                     ad_plus_cd_factor: float = 1.0) -> float:
    """AD followed by CD at t = T_ad + gap. Returns foci/cell at time t (h)
    measured from the start of AD."""
    t_cd_start = p.T_ad_h + p.gap_h
    n_from_ad = ad_curve(t_h, p, atm_factor=ad_factor)
    n_from_cd = cd_curve(t_h, p, atm_factor=cd_factor, t0_cd_h=t_cd_start)
    # ad_plus_cd_factor is a non-linear cross-talk modifier on the *combined*
    # signal, motivated by Plodowska's observation that AD modulates CD response.
    return ad_plus_cd_factor * (n_from_ad + n_from_cd)


# ---------------------------------------------------------------------------
# Smoke driver
# ---------------------------------------------------------------------------

def smoke(out_csv: Path, out_png: Path | None = None) -> dict:
    """Emit a 5-condition synthetic curve set spanning the AD exposure window
    plus 24 h post-CD, with two sample VLDR arms and a KU-55933 toggle."""
    p_low  = FociParams(dose_rate_AD_Gy_per_h=31e-6, T_ad_h=5.9e-3 / 31e-6)   # 5.9 mGy arm
    p_high = FociParams(dose_rate_AD_Gy_per_h=55e-6, T_ad_h=10.5e-3 / 55e-6)  # 10.5 mGy arm

    # Time grid: 0 ... T_ad ... T_ad+gap+24h
    Tmax = max(p_low.T_ad_h, p_high.T_ad_h) + 24.0
    times = [i * 1.0 for i in range(0, int(Tmax) + 1)]   # 1-hour resolution

    # Plodowska headline: KU has ~no effect on AD-only; reduces CD-only ~60%;
    # AD+CD signal is *not* abolished by KU. Numbers are placeholders.
    KU = dict(AD_yield_factor=1.00, CD_yield_factor=0.40, AD_plus_CD_factor=1.00)

    rows = [["time_h",
             "AD_lowVLDR",  "AD_lowVLDR_KU",
             "AD_highVLDR", "AD_highVLDR_KU",
             "CD_only",     "CD_only_KU",
             "AD_low_then_CD",  "AD_low_then_CD_KU",
             "AD_high_then_CD", "AD_high_then_CD_KU"]]
    for t in times:
        rows.append([
            t,
            ad_curve(t, p_low),
            ad_curve(t, p_low,  atm_factor=KU["AD_yield_factor"]),
            ad_curve(t, p_high),
            ad_curve(t, p_high, atm_factor=KU["AD_yield_factor"]),
            cd_curve(t, p_low,  t0_cd_h=p_low.T_ad_h),     # CD impulse at same wall-clock
            cd_curve(t, p_low,  t0_cd_h=p_low.T_ad_h, atm_factor=KU["CD_yield_factor"]),
            ad_then_cd_curve(t, p_low),
            ad_then_cd_curve(t, p_low,  ad_factor=KU["AD_yield_factor"],
                             cd_factor=KU["CD_yield_factor"],
                             ad_plus_cd_factor=KU["AD_plus_CD_factor"]),
            ad_then_cd_curve(t, p_high),
            ad_then_cd_curve(t, p_high, ad_factor=KU["AD_yield_factor"],
                             cd_factor=KU["CD_yield_factor"],
                             ad_plus_cd_factor=KU["AD_plus_CD_factor"]),
        ])

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as fh:
        csv.writer(fh).writerows(rows)

    plotted = False
    if out_png is not None:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            ts = [r[0] for r in rows[1:]]
            fig, ax = plt.subplots(figsize=(7, 4.5))
            for ci, name in enumerate(rows[0][1:], start=1):
                ys = [r[ci] for r in rows[1:]]
                style = "--" if "_KU" in name else "-"
                ax.plot(ts, ys, style, linewidth=1.4, label=name)
            ax.set_xlabel("time (h, from start of AD)")
            ax.set_ylabel("mean 53BP1 foci per cell (model)")
            ax.set_title("Plodowska 2025 — kinetic scaffold (SMOKE, synthetic params)")
            ax.legend(fontsize=7, ncol=2, loc="upper right", frameon=False)
            fig.tight_layout()
            out_png.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out_png, dpi=150)
            plotted = True
        except Exception as exc:
            sys.stderr.write(f"[warn] matplotlib unavailable, skipping PNG: {exc}\n")

    # Sanity invariants the smoke test asserts on every run
    n_steady_low  = p_low.Y_per_Gy * p_low.dose_rate_AD_Gy_per_h / FociParams().k_repair
    n_steady_high = p_high.Y_per_Gy * p_high.dose_rate_AD_Gy_per_h / FociParams().k_repair
    assert n_steady_high > n_steady_low > 0
    cd_peak = max(r[5] for r in rows[1:])
    assert cd_peak > n_steady_high, "CD impulse should exceed VLDR steady state"

    return {
        "n_timepoints": len(rows) - 1,
        "ad_low_steady_state_foci": round(n_steady_low, 5),
        "ad_high_steady_state_foci": round(n_steady_high, 5),
        "cd_peak_foci": round(cd_peak, 3),
        "csv": str(out_csv),
        "png": str(out_png) if plotted else None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--demo", action="store_true",
                    help="Emit synthetic curve set under results/ + figures/.")
    ap.add_argument("--fit", metavar="CSV",
                    help="Fit k_repair and Y_per_Gy to a digitised Fig CSV "
                         "(stub — wire scipy.optimize once data is in place).")
    args = ap.parse_args(argv)

    here = Path(__file__).resolve().parent.parent
    if args.demo:
        info = smoke(
            out_csv=here / "results" / "smoke_synthetic.csv",
            out_png=here / "figures" / "smoke_synthetic.png",
        )
        print("SMOKE OK:", info)
        return 0
    if args.fit:
        sys.stderr.write(
            "fit mode is a stub: digitise Plodowska Fig 1/2/3 with "
            "WebPlotDigitizer into data/digitized_fig*.csv, then wire "
            "scipy.optimize.curve_fit to (chronic_N, acute_N, ad_then_cd_curve). "
            "Holding off until the article PDF is in hand.\n"
        )
        return 2
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
