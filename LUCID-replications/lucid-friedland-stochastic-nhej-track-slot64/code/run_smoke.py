"""Driver: run the NHEJ smoke for two damage qualities, write CSV/JSON/figure."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from nhej_smoke import (
    NHEJParams,
    simulate_ensemble,
)


def _half_time(times: np.ndarray, frac: np.ndarray) -> float | None:
    """Time at which surviving fraction first crosses 0.5 (linear interp)."""
    below = np.where(frac <= 0.5)[0]
    if len(below) == 0:
        return None
    i = below[0]
    if i == 0:
        return float(times[0])
    f1, f2 = frac[i - 1], frac[i]
    t1, t2 = times[i - 1], times[i]
    if f1 == f2:
        return float(t2)
    return float(t1 + (t2 - t1) * (f1 - 0.5) / (f1 - f2))


def _biexp_fit(times: np.ndarray, frac: np.ndarray):
    """Quick non-linear fit S(t) = a * exp(-t/tau_f) + (1-a-r) * exp(-t/tau_s) + r.
    Uses a simple grid + least-squares fallback; sufficient for a smoke report.
    """
    from scipy.optimize import curve_fit  # type: ignore
    def model(t, a, tau_f, tau_s, r):
        a = max(min(a, 1.0), 0.0)
        r = max(min(r, 0.5), 0.0)
        slow = max(0.0, 1.0 - a - r)
        return a * np.exp(-t / max(tau_f, 1e-3)) \
             + slow * np.exp(-t / max(tau_s, 1e-3)) + r
    try:
        p0 = [0.7, 30.0, 300.0, 0.05]
        popt, _ = curve_fit(model, times, frac, p0=p0, maxfev=20000)
        return {
            "a_fast": float(popt[0]),
            "tau_fast_min": float(popt[1]),
            "tau_slow_min": float(popt[2]),
            "residual_floor": float(popt[3]),
        }
    except Exception as exc:  # noqa: BLE001
        return {"error": repr(exc)}


def main() -> None:
    here = Path(__file__).resolve().parent
    proj = here.parent
    res_dir = proj / "results"
    fig_dir = proj / "figures"
    log_dir = proj / "logs"
    for d in (res_dir, fig_dir, log_dir):
        d.mkdir(exist_ok=True)

    params = NHEJParams()

    t0 = time.time()
    # Two damage qualities: low-LET (mostly clean) and high-LET (mostly dirty)
    n_dsb = 40         # illustrative (no PARTRAC input available)
    n_rep = 5
    dt_min = 2.0
    t_max_min = 24 * 60
    # case -> (dirty fraction, cluster fraction)
    cases = {
        "low_LET":  (params.dirty_fraction_lowLET,  0.05),
        "high_LET": (params.dirty_fraction_highLET, 0.35),
    }
    summary: dict = {
        "schema_version": 1,
        "model": "Friedland-Jacob-Kundrát 2010 NHEJ (architectural smoke)",
        "doi": "10.1667/RR1965.1",
        "rate_constants_source": "Li 2014 PLoS ONE (companion); not RR1965 verbatim",
        "synapsis_radius_um": params.synapsis_radius,
        "D_end_um2_per_min": params.D_end,
        "n_dsb_per_run": n_dsb,
        "n_repeats": n_rep,
        "t_max_min": t_max_min,
        "dt_min": dt_min,
        "cases": {},
    }
    curves = {"time_min": None}

    for name, (dirty, clust) in cases.items():
        print(f"[smoke] running {name}: dirty fraction {dirty}, clustering {clust}")
        sim = simulate_ensemble(
            n_dsb=n_dsb, dirty_fraction=dirty, params=params,
            n_repeats=n_rep, t_max_min=t_max_min, dt_min=dt_min,
            cluster_fraction=clust,
            base_seed=2024 + (10 if name == "high_LET" else 0),
        )
        if curves["time_min"] is None:
            curves["time_min"] = sim.times.tolist()
        curves[f"surviving_{name}"] = sim.surviving_dsb_frac.tolist()
        curves[f"misrejoin_{name}"] = sim.misrejoined_cum.tolist()
        curves[f"correct_{name}"]   = sim.correct_rejoined_cum.tolist()

        t_half = _half_time(sim.times, sim.surviving_dsb_frac)
        biexp = _biexp_fit(sim.times, sim.surviving_dsb_frac)
        case_summary = {
            "dirty_fraction": dirty,
            "cluster_fraction": clust,
            "final_residual_frac_24h": sim.final_residual_frac,
            "final_misrejoin_frac_24h": sim.final_misrejoin_frac,
            "final_correct_frac_24h":   sim.final_correct_frac,
            "t_half_min": t_half,
            "biexp_fit": biexp,
        }
        summary["cases"][name] = case_summary
        for k, v in case_summary.items():
            print(f"  {name}.{k} = {v}")

    summary["wallclock_s"] = round(time.time() - t0, 2)

    # CSV
    csv_path = res_dir / "rejoining_curves.csv"
    with csv_path.open("w") as f:
        headers = ["time_min", "surviving_low_LET", "surviving_high_LET",
                   "misrejoin_low_LET", "misrejoin_high_LET",
                   "correct_low_LET",   "correct_high_LET"]
        f.write(",".join(headers) + "\n")
        n = len(curves["time_min"])
        for i in range(n):
            row = [curves["time_min"][i],
                   curves["surviving_low_LET"][i], curves["surviving_high_LET"][i],
                   curves["misrejoin_low_LET"][i], curves["misrejoin_high_LET"][i],
                   curves["correct_low_LET"][i],   curves["correct_high_LET"][i]]
            f.write(",".join(f"{x:.6g}" for x in row) + "\n")

    # JSON
    json_path = res_dir / "smoke_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True))

    # Figure
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    t = np.array(curves["time_min"])
    ax.plot(t, curves["surviving_low_LET"],  label="surviving DSBs, low-LET (30% dirty)", lw=2)
    ax.plot(t, curves["surviving_high_LET"], label="surviving DSBs, high-LET (70% dirty)", lw=2)
    ax.plot(t, curves["misrejoin_low_LET"],  ls="--", label="misrejoined, low-LET", lw=1)
    ax.plot(t, curves["misrejoin_high_LET"], ls="--", label="misrejoined, high-LET", lw=1)
    ax.set_xscale("symlog", linthresh=1.0)
    ax.set_xlabel("Time after irradiation [min]")
    ax.set_ylabel("Fraction of initial DSBs")
    ax.set_title("Friedland 2010 (RR1965) NHEJ smoke — surviving + misrejoined DSBs")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig_path = fig_dir / "dsb_rejoining.png"
    fig.savefig(fig_path, dpi=140)

    print(f"\n[smoke] wallclock {summary['wallclock_s']} s")
    print(f"[smoke] wrote {csv_path}")
    print(f"[smoke] wrote {json_path}")
    print(f"[smoke] wrote {fig_path}")


if __name__ == "__main__":
    main()
