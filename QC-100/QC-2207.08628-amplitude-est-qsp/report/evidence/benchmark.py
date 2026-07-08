"""Benchmark IQAE vs ChebAE against the paper's Empirical Claims 18 & 20.

We reduce the paper's 1000 runs per epsilon to N_RUNS (default 200) to fit our
time budget, but the target is the same: reproduce (approximately) the ratio
ChebAE/IQAE ~= 0.45-0.65 and the fC-model fits (IQAE ~ 9.93/eps, ChebAE ~ 4.66/eps).
"""
from __future__ import annotations
import argparse, json, math, os, pathlib, sys, time
import numpy as np

from ae_algorithms import iqae, chebae

def run_bench(a_true=0.5, delta=0.05,
              epsilons=(1e-2, 3e-3, 1e-3, 3e-4, 1e-4),
              n_runs=200, seed=20260703):
    rng_master = np.random.default_rng(seed)
    results = {"a_true": a_true, "delta": delta, "n_runs": n_runs, "seed": seed,
               "epsilons": list(epsilons), "iqae": {}, "chebae": {}}

    for eps in epsilons:
        for algo_name, algo in [("iqae", iqae), ("chebae", chebae)]:
            t0 = time.time()
            qs, errs, ok = [], [], []
            for i in range(n_runs):
                rng = np.random.default_rng(rng_master.integers(1<<63))
                res = algo(a_true, eps, delta, rng=rng)
                qs.append(res.total_queries_Zpi)
                errs.append(abs(res.a_hat - a_true))
                ok.append(res.correct)
            qs = np.array(qs)
            errs = np.array(errs)
            ok = np.array(ok)
            d = {
                "epsilon": eps,
                "n_runs": n_runs,
                "mean_Q": float(qs.mean()),
                "median_Q": float(np.median(qs)),
                "min_Q": int(qs.min()),
                "max_Q": int(qs.max()),
                "std_Q": float(qs.std()),
                "mean_abs_err": float(errs.mean()),
                "max_abs_err": float(errs.max()),
                "n_correct": int(ok.sum()),
                "frac_correct": float(ok.mean()),
                "wall_time_sec": time.time() - t0,
            }
            results[algo_name][f"{eps:.0e}"] = d
            print(f"eps={eps:.0e}  {algo_name:6s}  mean_Q={d['mean_Q']:>10.0f}  "
                  f"correct_frac={d['frac_correct']:.3f}  time={d['wall_time_sec']:.1f}s")
        # ratio
        i = results["iqae"][f"{eps:.0e}"]["mean_Q"]
        c = results["chebae"][f"{eps:.0e}"]["mean_Q"]
        print(f"    ChebAE/IQAE mean_Q ratio = {c/i:.3f} (paper: 0.45-0.65)")

    return results

def summarize(results):
    """Fit fC(eps) = C/eps to mean_Q data for each algo; print vs paper's numbers."""
    from scipy.optimize import curve_fit
    print("\n=== fC(eps)=C/eps fits (paper: IQAE C=9.93, ChebAE C=4.66) ===")
    fits = {}
    for algo in ["iqae", "chebae"]:
        eps  = np.array([results[algo][k]["epsilon"] for k in results[algo]])
        meanQ = np.array([results[algo][k]["mean_Q"]  for k in results[algo]])
        # C = mean(meanQ * eps) (LSQ minimizer of relative error at each eps -> geo mean of prod)
        Cs = meanQ * eps
        # fC that minimizes max relative error:
        C_geom = float(np.exp(np.mean(np.log(Cs))))
        C_lsq  = float(np.sum(meanQ * eps) / len(eps))  # simple mean of C_i = Q_i*eps_i
        fits[algo] = {"C_geom": C_geom, "C_lsq_mean": C_lsq,
                       "per_eps_C": {f"{e:.0e}": float(c) for e,c in zip(eps, Cs)}}
        print(f"  {algo:6s}: per-eps C = {dict(zip(['%.0e'%e for e in eps], ['%.2f'%c for c in Cs]))}")
        print(f"    geometric mean C = {C_geom:.3f}")
    results["fits_fC"] = fits
    # ratio of C values
    ratio_geom = fits["chebae"]["C_geom"] / fits["iqae"]["C_geom"]
    results["chebae_iqae_C_ratio"] = ratio_geom
    print(f"\n  ChebAE/IQAE C ratio (geom-mean) = {ratio_geom:.3f}  (paper: 4.66/9.93 = 0.469)")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-runs", type=int, default=100)
    ap.add_argument("--epsilons", type=str, default="1e-2,3e-3,1e-3,3e-4")
    ap.add_argument("--out", type=str, default="../report/evidence/benchmark_results.json")
    args = ap.parse_args()

    eps_list = tuple(float(x) for x in args.epsilons.split(","))
    print(f"Running IQAE vs ChebAE benchmark: {args.n_runs} runs per epsilon, eps={eps_list}")
    print(f"(paper used 1000 runs, 9 log-spaced eps in [1e-2,1e-6])\n")

    res = run_bench(n_runs=args.n_runs, epsilons=eps_list)
    res = summarize(res)

    out = pathlib.Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2))
    print(f"\n[wrote] {out}")
