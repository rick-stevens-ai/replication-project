#!/usr/bin/env python3
"""
Replication spot-check for arXiv:2310.12981
"Improved Pairwise Measurement-Based Surface Code" (Grans-Samuelsson et al., 2023).

Headline claim: pair-measurement based realization of the rotated surface code
achieves a fault-tolerance threshold of approximately 0.66% under a standard
circuit noise model. Compared favorably to the 4.8.8 Floquet code (~1.3%).

What we do here (SPOT-CHECK scope):
  1. Simulate d=3,5,7 rotated surface code memory in Stim using its built-in
     standard CNOT-based syndrome extraction circuit (NOT the paper's pair-
     measurement circuit; implementing that from scratch is out of scope).
  2. Sweep physical error rate p across a range that brackets the surface-code
     threshold (~0.5%..1.5%).
  3. Estimate the threshold by finding the p at which curves cross (LER per
     round vs distance).
  4. Compare our measured threshold (expected ~1% for standard CNOT surface
     code) to the paper's 0.66% for their pair-measurement variant.

Note: The standard surface code threshold on this noise model is well known to
be ~1% (e.g. Fowler et al. 2012). The paper's 0.66% is lower because their
circuit uses two-qubit *measurements* on ancilla+data instead of CNOTs, which
introduces more measurement noise per stabilizer round. So we expect our number
to be higher than 0.66% — that's the point: the paper's contribution is that
their pair-measurement circuit (constrained by Majorana hardware) *still*
achieves ~0.66%, competitive with prior pair-meas realizations.

We are NOT claiming to reproduce 0.66% — we are reproducing the *methodology*
(Stim + PyMatching threshold sweep) and giving a sanity-check baseline
threshold that bounds the pair-measurement value from above.
"""

import json
import time
from pathlib import Path

import numpy as np
import pymatching
import stim

OUT = Path(__file__).resolve().parents[1] / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def count_logical_errors(circuit: stim.Circuit, num_shots: int) -> int:
    """Standard Stim + PyMatching sampling loop."""
    sampler = circuit.compile_detector_sampler()
    detection_events, observable_flips = sampler.sample(
        num_shots, separate_observables=True
    )
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    predictions = matcher.decode_batch(detection_events)
    return int(np.sum(np.any(predictions != observable_flips, axis=1)))


def logical_error_per_round(num_errors, num_shots, rounds):
    """Convert shot-level LER to per-round LER (standard formula)."""
    if num_shots == 0:
        return float("nan")
    p_shot = num_errors / num_shots
    if p_shot <= 0.0:
        return 0.0
    if p_shot >= 1.0:
        return 1.0
    # p_round derived from p_shot = 0.5 * (1 - (1 - 2 p_round)^rounds)
    inner = 1.0 - 2.0 * p_shot
    if inner <= 0.0:
        return 0.5
    per_round = 0.5 * (1.0 - inner ** (1.0 / rounds))
    return float(per_round)


def run_sweep():
    distances = [3, 5, 7]
    physical_error_rates = [
        0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.0066,
        0.008, 0.009, 0.010, 0.012, 0.014, 0.017, 0.020,
    ]
    physical_error_rates = sorted(set(physical_error_rates))
    num_shots_max = 20000
    # Fewer shots at low p (all zeros anyway), more shots near threshold.

    results = []
    t0 = time.time()

    for d in distances:
        rounds = d  # standard convention: rounds = distance
        for p in physical_error_rates:
            circuit = stim.Circuit.generated(
                "surface_code:rotated_memory_z",
                rounds=rounds,
                distance=d,
                after_clifford_depolarization=p,
                after_reset_flip_probability=p,
                before_measure_flip_probability=p,
                before_round_data_depolarization=p,
            )
            # Adaptive shot count: cheap floor, more shots if we see errors.
            shots = num_shots_max
            errs = count_logical_errors(circuit, shots)
            p_shot = errs / shots
            per_round = logical_error_per_round(errs, shots, rounds)

            row = {
                "distance": d,
                "rounds": rounds,
                "physical_error_rate": p,
                "shots": shots,
                "logical_errors": errs,
                "p_logical_per_shot": p_shot,
                "p_logical_per_round": per_round,
            }
            results.append(row)
            print(
                f"  d={d} p={p:.4f} shots={shots} errs={errs} "
                f"p_shot={p_shot:.4g} p_round={per_round:.4g} "
                f"(elapsed {time.time()-t0:.1f}s)",
                flush=True,
            )

    return results


def estimate_threshold(results):
    """
    Rough threshold estimator: find the p at which the d=3 and d=5 curves
    cross (per-round LER). Below this p, larger distance is better; above, it's
    worse. Uses linear interpolation between adjacent sweep points.
    """
    by_dist = {}
    for r in results:
        by_dist.setdefault(r["distance"], []).append(r)
    for d in by_dist:
        by_dist[d].sort(key=lambda r: r["physical_error_rate"])

    d_low, d_high = 3, 5
    if d_low not in by_dist or d_high not in by_dist:
        return None

    ps = sorted({r["physical_error_rate"] for r in by_dist[d_low]}
                & {r["physical_error_rate"] for r in by_dist[d_high]})
    prev_p, prev_diff = None, None
    crossings = []
    for p in ps:
        low = next(r for r in by_dist[d_low] if r["physical_error_rate"] == p)
        high = next(r for r in by_dist[d_high] if r["physical_error_rate"] == p)
        diff = high["p_logical_per_round"] - low["p_logical_per_round"]
        # Below threshold: high < low (bigger distance helps) → diff < 0.
        # Above threshold: high > low → diff > 0. Crossing where diff flips sign.
        if prev_diff is not None and prev_diff <= 0 < diff:
            # linear interp on diff
            if diff == prev_diff:
                p_cross = p
            else:
                p_cross = prev_p + (p - prev_p) * (0 - prev_diff) / (diff - prev_diff)
            crossings.append({"p_cross": p_cross, "between": [prev_p, p]})
        prev_p, prev_diff = p, diff

    return crossings


def main():
    print("=== QC-100 replication: 2310.12981 threshold sweep ===")
    print("Tool versions:")
    print(f"  stim {stim.__version__}")
    print(f"  pymatching {pymatching.__version__}")
    print(f"  numpy {np.__version__}")
    print()

    results = run_sweep()

    thresholds = estimate_threshold(results)

    out = {
        "paper_arxiv_id": "2310.12981",
        "paper_title": "Improved Pairwise Measurement-Based Surface Code",
        "paper_claimed_threshold": 0.0066,
        "circuit_type": "surface_code:rotated_memory_z (Stim built-in, CNOT-based)",
        "note": "Standard CNOT-based rotated surface code, NOT the paper's exact "
                "pair-measurement circuit. Used as methodology spot-check.",
        "tool_versions": {
            "stim": stim.__version__,
            "pymatching": pymatching.__version__,
            "numpy": np.__version__,
        },
        "results": results,
        "estimated_threshold_crossings_d3_d5": thresholds,
    }

    out_path = OUT / "threshold_sweep_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")

    # CSV for humans
    csv_path = OUT / "threshold_sweep_results.csv"
    with open(csv_path, "w") as f:
        f.write("distance,rounds,physical_error_rate,shots,logical_errors,"
                "p_logical_per_shot,p_logical_per_round\n")
        for r in results:
            f.write(f"{r['distance']},{r['rounds']},{r['physical_error_rate']},"
                    f"{r['shots']},{r['logical_errors']},"
                    f"{r['p_logical_per_shot']:.6g},"
                    f"{r['p_logical_per_round']:.6g}\n")
    print(f"Wrote {csv_path}")

    if thresholds:
        print("\nEstimated d=3/d=5 crossing(s):")
        for c in thresholds:
            print(f"  p_threshold ≈ {c['p_cross']:.4f} "
                  f"(bracket {c['between']})")
    else:
        print("\nNo d=3/d=5 crossing detected in sweep range.")

    print("\nPaper claim: 0.66% for pair-measurement surface code.")
    print("Standard CNOT surface code threshold (literature): ~1.0%.")


if __name__ == "__main__":
    main()
