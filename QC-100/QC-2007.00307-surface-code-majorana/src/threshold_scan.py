#!/usr/bin/env python3
"""
Threshold scan: rotated_memory_z surface code at d in {3,5,7}, sweeping p
across the paper's expected threshold band, to actually see the LER/round
curves cross. Uses more shots at high p and adds d=7 so we can bracket the
threshold from both sides.
"""
import json
import math
import time
import sys
from pathlib import Path

import numpy as np
import pymatching
import stim


def build(distance, rounds, regime, p):
    kw = dict(
        code_task="surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    if regime == "depol":
        kw["after_clifford_depolarization"] = p
    elif regime == "biased":
        kw["after_clifford_depolarization"] = p * 0.1
    else:
        raise ValueError(regime)
    return stim.Circuit.generated(**kw)


def ler(circuit, shots):
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler()
    dets, obs = sampler.sample(shots=shots, separate_observables=True)
    preds = matcher.decode_batch(dets)
    n_err = int(np.sum(np.any(preds != obs, axis=1)))
    p_hat = n_err / shots
    sigma = math.sqrt(max(p_hat * (1 - p_hat), 1.0 / shots) / shots)
    return p_hat, sigma, n_err


def per_round(x, T):
    if x <= 0.0:
        return 0.0
    return 1.0 - (1.0 - x) ** (1.0 / T)


def main():
    rounds = 8
    # Denser sweep across paper's expected threshold band
    ps = [1e-3, 1.5e-3, 2e-3, 2.5e-3, 3e-3, 4e-3, 6e-3, 1e-2]
    # For biased regime, threshold is higher, so also add higher ps
    ps_biased = ps + [1.5e-2, 2e-2]
    ds = [3, 5, 7]

    def shots_for(p):
        # target ~ >=50 logical errors at largest distance where possible
        if p <= 2e-3:
            return 30_000
        if p <= 5e-3:
            return 20_000
        return 10_000

    all_results = []
    t0 = time.time()
    for regime, plist in [("depol", ps), ("biased", ps_biased)]:
        for d in ds:
            for p in plist:
                shots = shots_for(p)
                c = build(d, rounds, regime, p)
                lt, sig, ne = ler(c, shots)
                lr = per_round(lt, rounds)
                rec = dict(regime=regime, d=d, rounds=rounds, p=p,
                           shots=shots, num_err=ne,
                           ler_total=lt, ler_sigma=sig, ler_round=lr)
                all_results.append(rec)
                print(f"[{time.time()-t0:7.1f}s] {regime:6s} d={d} p={p:.2e} "
                      f"shots={shots:>6d} errs={ne:>4d} "
                      f"LER/round={lr:.3e}+/-{sig:.1e}", flush=True)

    out = Path(__file__).resolve().parent.parent / "report" / "evidence"
    (out / "threshold_scan.json").write_text(json.dumps(
        {"tool": {"stim": stim.__version__,
                  "pymatching": pymatching.__version__,
                  "python": sys.version.split()[0]},
         "results": all_results}, indent=2))

    # Extract crossings between distances
    print("\n--- Crossings (LER/round curves) ---")
    summary = {}
    for regime in ["depol", "biased"]:
        summary[regime] = {}
        rows = [r for r in all_results if r["regime"] == regime]
        by_d = {}
        for r in rows:
            by_d.setdefault(r["d"], []).append((r["p"], r["ler_round"]))
        for d in by_d:
            by_d[d].sort()
        for (d1, d2) in [(3, 5), (5, 7), (3, 7)]:
            c1 = by_d[d1]; c2 = by_d[d2]
            # Align by p
            ps_common = sorted(set(p for p, _ in c1) & set(p for p, _ in c2))
            crossings = []
            for i in range(len(ps_common) - 1):
                p_lo = ps_common[i]; p_hi = ps_common[i + 1]
                l1_lo = dict(c1)[p_lo]; l1_hi = dict(c1)[p_hi]
                l2_lo = dict(c2)[p_lo]; l2_hi = dict(c2)[p_hi]
                dlo = l1_lo - l2_lo
                dhi = l1_hi - l2_hi
                if dlo * dhi < 0 and dlo != dhi:
                    frac = dlo / (dlo - dhi)
                    pc = math.exp(math.log(p_lo) + frac * (math.log(p_hi) - math.log(p_lo)))
                    crossings.append(pc)
            summary[regime][f"d{d1}_vs_d{d2}"] = crossings
            print(f"  regime={regime} d={d1} vs d={d2}: crossings ~ {crossings}")

    (out / "threshold_crossings.json").write_text(json.dumps(summary, indent=2))
    print("\nWrote:", out / "threshold_scan.json")
    print("Wrote:", out / "threshold_crossings.json")


if __name__ == "__main__":
    main()
