#!/usr/bin/env python3
"""
QC-100 replication for arXiv:2007.00307
(Chao, Beverland, Delfosse, Haah -- "Optimization of the surface code design
for Majorana-based qubits").

Approach (SPOT-CHECK / PARTIAL):
    The paper introduces custom windmill / double-ancilla surface-code layouts
    that use ONLY single- and two-qubit Pauli measurements (no CNOTs), aimed at
    Majorana-based qubits, and reports circuit-level thresholds pth = 1.54e-3
    (windmill) and 2.37e-3 (double ancilla) under a uniform circuit-level
    depolarizing noise model with a Union-Find decoder.

    We cannot rebuild the bespoke windmill/double-ancilla layouts in a few
    minutes, but we CAN do the closest tractable spot-check on the paper's
    central methodological claim ("surface-code LER can be estimated at
    circuit level under stochastic Pauli noise and thresholds are in the ~1e-3
    ballpark") using Stim's built-in rotated-memory surface code and PyMatching
    MWPM decoding.

    We compare two noise regimes:
      (a) Standard uniform circuit-level depolarizing noise -- proxy for the
          conventional CNOT-based / regular-qubit picture. Uses Stim's
          `surface_code:rotated_memory_z` generator with `noise=p` on all
          gates + reset + measurement.
      (b) A biased/measurement-heavy noise regime -- proxy for the
          Majorana / pair-measurement picture where the dominant fault is on
          the (pair-)measurement primitive rather than on multi-qubit gates.
          Same generator but noise concentrated on measurement flips
          (after_reset_flip_probability, before_measure_flip_probability
          bumped, two-qubit-gate depolarization suppressed).

    We sweep p across the paper's threshold ballpark (5e-4 .. 5e-3), compute
    LER per QEC round for d=3 and d=5, and check:
      (i) LER curves cross near p ~ 1e-3 for regime (a)   -- rough threshold
      (ii) Regime (b) (measurement-biased) LER at fixed p is comparable to or
           better than (a) for d>=5, matching the paper's qualitative claim
           that pair-measurement-based surface codes are competitive.
"""

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import pymatching
import stim


def build_circuit(distance: int, rounds: int, regime: str, p: float) -> stim.Circuit:
    """
    Return a Stim rotated memory surface code circuit at physical error rate p
    under one of two noise regimes.

    regime='depol':  uniform circuit-level depolarizing noise (all channels = p).
    regime='biased': measurement-flip-dominated noise (proxy for pair-meas./Majorana).
    """
    if regime == "depol":
        return stim.Circuit.generated(
            code_task="surface_code:rotated_memory_z",
            distance=distance,
            rounds=rounds,
            after_clifford_depolarization=p,
            after_reset_flip_probability=p,
            before_measure_flip_probability=p,
            before_round_data_depolarization=p,
        )
    if regime == "biased":
        # Measurement-heavy: reset and measurement flips at p, and 1q pre-round
        # depol at p, but two-qubit clifford depolarization reduced by 10x
        # -- reflects the paper's setting where the dominant fault is the
        # pair-measurement primitive rather than the emulated CNOT.
        return stim.Circuit.generated(
            code_task="surface_code:rotated_memory_z",
            distance=distance,
            rounds=rounds,
            after_clifford_depolarization=p * 0.1,
            after_reset_flip_probability=p,
            before_measure_flip_probability=p,
            before_round_data_depolarization=p,
        )
    raise ValueError(f"unknown regime {regime!r}")


def logical_error_rate(circuit: stim.Circuit, shots: int) -> tuple[float, float, int]:
    """
    Decode `shots` shots of `circuit` with PyMatching MWPM.
    Returns (ler_estimate, one_sigma, num_errors).
    """
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler()
    dets, obs = sampler.sample(shots=shots, separate_observables=True)
    preds = matcher.decode_batch(dets)
    num_err = int(np.sum(np.any(preds != obs, axis=1)))
    ler = num_err / shots
    # Wilson-ish 1-sigma binomial error
    sigma = math.sqrt(max(ler * (1 - ler), 1.0 / shots) / shots)
    return ler, sigma, num_err


def per_round_ler(ler_total: float, rounds: int) -> float:
    """Convert total-experiment LER into a per-round LER (small-p approx)."""
    if ler_total <= 0.0:
        return 0.0
    if ler_total >= 1.0:
        return 1.0
    return 1.0 - (1.0 - ler_total) ** (1.0 / rounds)


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Threshold ballpark from paper: 1.5e-3 .. 2.4e-3
    physical_error_rates = [5e-4, 1e-3, 1.5e-3, 2e-3, 3e-3, 5e-3]
    distances = [3, 5]
    regimes = ["depol", "biased"]
    rounds = 8  # keep small so d=5 finishes in minutes at each p

    # Shots per configuration -- scaled so we expect >=30 logical errors near
    # threshold at d=5 (rough targets; hard cap for wall time).
    shots_by_p = {
        5e-4: 20_000,
        1e-3: 20_000,
        1.5e-3: 15_000,
        2e-3: 10_000,
        3e-3: 8_000,
        5e-3: 5_000,
    }

    results = []
    t0 = time.time()
    for regime in regimes:
        for d in distances:
            for p in physical_error_rates:
                shots = shots_by_p[p]
                circ = build_circuit(distance=d, rounds=rounds, regime=regime, p=p)
                ler_total, sigma, num_err = logical_error_rate(circ, shots)
                ler_round = per_round_ler(ler_total, rounds)
                elapsed = time.time() - t0
                rec = {
                    "regime": regime,
                    "distance": d,
                    "rounds": rounds,
                    "p": p,
                    "shots": shots,
                    "num_logical_errors": num_err,
                    "ler_total": ler_total,
                    "ler_total_sigma": sigma,
                    "ler_per_round": ler_round,
                    "wall_seconds_cumulative": round(elapsed, 2),
                }
                results.append(rec)
                print(
                    f"[{elapsed:7.1f}s] regime={regime:6s} d={d} p={p:.1e} "
                    f"shots={shots:>6d} errs={num_err:>4d} "
                    f"LER_total={ler_total:.3e}+/-{sigma:.1e} "
                    f"LER/round={ler_round:.3e}",
                    flush=True,
                )

    out_json = out_dir / "results.json"
    out_json.write_text(json.dumps(
        {
            "paper": "arXiv:2007.00307",
            "tool": {
                "stim": stim.__version__,
                "pymatching": pymatching.__version__,
                "numpy": np.__version__,
                "python": sys.version.split()[0],
            },
            "notes": (
                "Rotated-memory-Z surface code from stim.Circuit.generated, "
                "MWPM decoding via PyMatching. 'depol' = uniform circuit-level "
                "depolarizing noise (all channels set to p). 'biased' = "
                "measurement-flip-heavy proxy for the paper's pair-measurement "
                "primitives (two-qubit gate depolarization reduced 10x)."
            ),
            "results": results,
        },
        indent=2,
    ))
    print(f"\nWrote {out_json}")

    # Also write a CSV for quick eyeballing
    csv_path = out_dir / "results.csv"
    with csv_path.open("w") as f:
        f.write("regime,distance,rounds,p,shots,num_logical_errors,ler_total,ler_total_sigma,ler_per_round\n")
        for r in results:
            f.write(
                f"{r['regime']},{r['distance']},{r['rounds']},{r['p']},{r['shots']},"
                f"{r['num_logical_errors']},{r['ler_total']:.6e},"
                f"{r['ler_total_sigma']:.6e},{r['ler_per_round']:.6e}\n"
            )
    print(f"Wrote {csv_path}")

    # Simple threshold estimate: for regime='depol', find the p where LER/round
    # curves for d=3 and d=5 cross.
    def curve(regime: str, d: int) -> list[tuple[float, float]]:
        pts = [(r["p"], r["ler_per_round"]) for r in results
               if r["regime"] == regime and r["distance"] == d]
        return sorted(pts)

    thresh_summary = {}
    for regime in regimes:
        c3 = curve(regime, 3)
        c5 = curve(regime, 5)
        # Find first p where LER(d=3) < LER(d=5) -> below threshold, and last p
        # where LER(d=3) > LER(d=5) -> above threshold. Threshold is between.
        assert len(c3) == len(c5)
        crossings = []
        for i in range(len(c3) - 1):
            p_lo, l3_lo = c3[i]; _, l5_lo = c5[i]
            p_hi, l3_hi = c3[i + 1]; _, l5_hi = c5[i + 1]
            if (l3_lo - l5_lo) * (l3_hi - l5_hi) < 0:
                # linear interpolate crossing in log-p
                # solve for p where (l3 - l5)(p) = 0
                d_lo = l3_lo - l5_lo
                d_hi = l3_hi - l5_hi
                frac = d_lo / (d_lo - d_hi)
                p_cross = math.exp(
                    math.log(p_lo) + frac * (math.log(p_hi) - math.log(p_lo))
                )
                crossings.append(p_cross)
        thresh_summary[regime] = {
            "curve_d3": c3,
            "curve_d5": c5,
            "estimated_threshold_crossings": crossings,
        }

    (out_dir / "threshold_summary.json").write_text(
        json.dumps(thresh_summary, indent=2)
    )
    print(f"Wrote {out_dir / 'threshold_summary.json'}")
    for regime, s in thresh_summary.items():
        print(f"  regime={regime}: crossings ~ {s['estimated_threshold_crossings']}")


if __name__ == "__main__":
    main()
