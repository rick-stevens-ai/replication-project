"""
REPASS-1 / C7-revisit — biphasic two-exponential fit of Fig 4 kinetics.

Paper page 5–6: "Our kinetic model naturally leads to such a biphasic
description where long DNA fragments (≥45 bp) are joined through fast
kinetics and short DNA fragments (<45 bp) are joined through slow kinetics."

Pass-1 said "biphasic shape reproduced visually" but never quantified
the two time-scales.  Here we re-run the Fig 4 ensemble (or load it
if already computed) and fit:

   M(t) / M(0) ≈ A_fast * exp(-t/τ_fast) + (1 - A_fast) * exp(-t/τ_slow)

with A_fast, τ_fast, τ_slow > 0.  The claim is τ_slow >> τ_fast under
high-LET (30% short) but much closer under low-LET (3% short).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from gillespie_rejoining import (
    SimParams,
    simulate,
    initial_high_LET_Fe_1Gy,
    initial_low_LET_gamma_1Gy,
    mean_remaining_fraction_curve,
)

OUT_RESULTS = ROOT / "results" / "repass1"
OUT_LOGS = ROOT / "logs" / "repass1"
OUT_FIGS = ROOT / "figures" / "repass1"
for d in (OUT_RESULTS, OUT_LOGS, OUT_FIGS):
    d.mkdir(parents=True, exist_ok=True)


def biexp(t, A, tau_f, tau_s):
    A = np.clip(A, 0.0, 1.0)
    tau_f = max(tau_f, 1e-3)
    tau_s = max(tau_s, 1e-3)
    return A * np.exp(-t / tau_f) + (1 - A) * np.exp(-t / tau_s)


def fit_biexp(t_grid, frac):
    """Bounded LM-style fit using scipy.optimize.curve_fit if available,
    else fallback to a coarse grid search."""
    try:
        from scipy.optimize import curve_fit
        # initial guess: A=0.7, tau_f = t90 (time to reach 0.1), tau_s = 5x that
        # locate approximate decay time
        ok = frac > 0.001
        if ok.sum() < 5:
            return None
        # heuristic guess
        idx10 = np.searchsorted(-frac[ok], -0.1)
        idx10 = min(idx10, ok.sum() - 1)
        tau_guess = max(t_grid[ok][idx10] / 2.3, 1.0)
        p0 = [0.5, tau_guess * 0.4, tau_guess * 3.0]
        popt, _ = curve_fit(biexp, t_grid, frac, p0=p0,
                            bounds=([0.0, 1e-3, 1e-3], [1.0, 1e6, 1e6]),
                            maxfev=20000)
        return tuple(float(x) for x in popt)
    except Exception as e:
        print(f"  (scipy fit failed: {e}; falling back to grid)")
        best = None
        for A in np.linspace(0.05, 0.95, 19):
            for tf in np.logspace(-1, 2, 25):
                for ts in np.logspace(0, 3, 25):
                    if ts <= tf:
                        continue
                    pred = biexp(t_grid, A, tf, ts)
                    err = float(np.mean((pred - frac) ** 2))
                    if best is None or err < best[0]:
                        best = (err, A, tf, ts)
        if best:
            return (best[1], best[2], best[3])
        return None


def run_condition(label, init_factory, n_runs=200, k1=1.0, k2=0.5, k3=0.1):
    """Run an ensemble and return (t_grid, mean_remaining_fraction)."""
    rng_master = np.random.default_rng(hash(label) & 0x7FFFFFFF)
    all_traj = []
    for k in range(n_runs):
        seed = int(rng_master.integers(0, 2**31 - 1))
        P = SimParams(k1=k1, k2=k2, k3=k3, E=1.0, V=1.0, rng_seed=seed)
        init = init_factory(np.random.default_rng(seed + 11))
        _t_end, traj = simulate(init, P)
        all_traj.append(traj)
    # Build common time grid (linear; max trajectory end across runs).
    t_max = max(p.t for traj in all_traj for p in traj)
    t_grid = np.linspace(0, t_max, 500)
    frac = mean_remaining_fraction_curve(all_traj, t_grid)
    return t_grid, frac


def main():
    rng_master = np.random.default_rng(13579)
    n_runs = 150
    n_dsb = 30

    t0 = time.time()
    out = {}
    for label, factory in [
        ("high_LET_Fe", lambda rng: initial_high_LET_Fe_1Gy(
            rng, n_dsb=n_dsb, frac_short=0.30)),
        ("low_LET_gamma", lambda rng: initial_low_LET_gamma_1Gy(
            rng, n_dsb=n_dsb, frac_short=0.03)),
    ]:
        print(f"\n=== {label} ===")
        t_grid, frac = run_condition(label, factory, n_runs=n_runs)
        fit = fit_biexp(t_grid, frac)
        if fit is None:
            print(f"  fit FAILED for {label}")
            out[label] = {"fit": None}
            continue
        A, tau_f, tau_s = fit
        ratio = float(tau_s / tau_f) if tau_f > 0 else float("inf")
        out[label] = {
            "A_fast": A,
            "tau_fast": tau_f,
            "tau_slow": tau_s,
            "ratio_tau_slow_over_tau_fast": ratio,
            "t_max": float(t_grid[-1]),
            "n_runs": n_runs,
        }
        print(f"  fit: A_fast={A:.3f}  tau_fast={tau_f:.3f}  tau_slow={tau_s:.3f}  "
              f"slow/fast={ratio:.2f}")
        np.savez(OUT_RESULTS / f"c7_revisit_{label}.npz",
                 t_grid=t_grid, frac=frac,
                 fit_A=A, fit_tau_fast=tau_f, fit_tau_slow=tau_s)

    elapsed = time.time() - t0

    high = out.get("high_LET_Fe", {})
    low = out.get("low_LET_gamma", {})

    verdict = "INCONCLUSIVE"
    if high.get("ratio_tau_slow_over_tau_fast") and low.get("ratio_tau_slow_over_tau_fast"):
        if high["ratio_tau_slow_over_tau_fast"] > 5.0:
            verdict = "STRONG"
        elif high["ratio_tau_slow_over_tau_fast"] > 2.0:
            verdict = "PARTIAL"

    summary = {
        "claim": "C7-revisit: biphasic kinetics, tau_slow >> tau_fast under high-LET",
        "results": out,
        "verdict": verdict,
        "elapsed_s": elapsed,
    }
    (OUT_LOGS / "c7_revisit.json").write_text(json.dumps(summary, indent=2))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        for label in ["high_LET_Fe", "low_LET_gamma"]:
            d = np.load(OUT_RESULTS / f"c7_revisit_{label}.npz")
            ax.plot(d["t_grid"], d["frac"], label=f"{label} data")
            A = float(d["fit_A"]); tf = float(d["fit_tau_fast"]); ts = float(d["fit_tau_slow"])
            ax.plot(d["t_grid"], biexp(d["t_grid"], A, tf, ts),
                    "--", alpha=0.6, label=f"{label} biexp fit τf={tf:.1f}, τs={ts:.1f}")
        ax.set_xlabel("time (arb)")
        ax.set_ylabel("mean remaining fraction")
        ax.set_yscale("log")
        ax.set_ylim(1e-3, 1.1)
        ax.set_title("C7-revisit: biphasic two-exponential fit")
        ax.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGS / "c7_revisit_biphasic.png", dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"  (plot skipped: {e})")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
