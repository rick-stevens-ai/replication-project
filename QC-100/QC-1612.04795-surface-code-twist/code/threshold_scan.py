#!/usr/bin/env python3
"""
Independent replication scaffold for Yoder & Kim 2017 (arXiv:1612.04795)
"The surface code with a twist".

We reproduce the paper's numeric anchor from Table 1: the phenomenological
noise threshold for the rotated surface code family (the direct comparison
target for the twist-based triangle code). The paper reports:

  Rotated surface code, ideal syndrome, bit-flip (X) noise: p_th ≈ 10%
  Rotated surface code, noisy syndrome, bit-flip (X) noise: p_th ≈ 3.2%

We estimate the threshold by simulating logical error rate vs physical error
rate p for a family of distances d = 3, 5, 7 using Stim's built-in rotated
surface code memory circuit + PyMatching MWPM decoder. Crossing point of
logical-error curves = threshold.

We run TWO regimes:
  (A) Ideal syndrome, code-capacity-like: single round, only data errors.
      Expected threshold ~10% (paper Table 1 top-left).
  (B) Phenomenological noisy syndrome: d rounds, X errors on data + noisy
      measurements. Expected threshold ~3% (paper Table 1 bottom-left).

Output: JSON with (d, p, shots, errors, logical_error_rate) rows.
"""
import json
import time
import stim
import pymatching
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def simulate(circuit: stim.Circuit, shots: int):
    sampler = circuit.compile_detector_sampler()
    dets, obs = sampler.sample(shots, separate_observables=True)
    matcher = pymatching.Matching.from_detector_error_model(
        circuit.detector_error_model(decompose_errors=True)
    )
    predictions = matcher.decode_batch(dets)
    num_errors = int(np.sum(np.any(predictions != obs, axis=1)))
    return num_errors


def run_regime(name, gen_kwargs, distances, ps, shots):
    """Sweep p, d for given circuit generator kwargs."""
    rows = []
    for d in distances:
        for p in ps:
            circ = stim.Circuit.generated(
                rounds=gen_kwargs.get("rounds", d),
                distance=d,
                after_clifford_depolarization=0.0,
                after_reset_flip_probability=0.0,
                before_measure_flip_probability=gen_kwargs.get("meas_p", 0.0) * p,
                before_round_data_depolarization=p if gen_kwargs.get("depol_data") else 0.0,
                code_task=gen_kwargs["code_task"],
            )
            t0 = time.time()
            errs = simulate(circ, shots)
            dt = time.time() - t0
            ler = errs / shots
            row = {
                "regime": name,
                "d": d,
                "p": p,
                "shots": shots,
                "errors": errs,
                "logical_error_rate": ler,
                "wall_s": round(dt, 2),
            }
            rows.append(row)
            print(f"[{name}] d={d} p={p:.4f} shots={shots} errs={errs} LER={ler:.4g} ({dt:.1f}s)")
    return rows


def main():
    all_rows = []

    # -------- Regime A: single-round, data-only X noise (code-capacity-ish) --
    # Stim's "surface_code:rotated_memory_x" with 1 round + only data depol
    # gives us a phenomenological-ideal-syndrome sweep.  For X-only threshold
    # in code-capacity we use before_round_data_depolarization (which flips
    # X or Y or Z; the memory_x task is sensitive to X and Y).  This is a
    # depolarizing proxy - true code-capacity X threshold on rotated surface
    # code is ~11% (matches paper's ~10%).
    print("\n=== Regime A: 1 round, ideal syndrome, depolarizing data noise ===")
    ps_A = [0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.18]
    rows_A = run_regime(
        "A_ideal_syndrome",
        {"code_task": "surface_code:rotated_memory_x", "rounds": 1,
         "depol_data": True, "meas_p": 0.0},
        distances=[3, 5, 7],
        ps=ps_A,
        shots=20000,
    )
    all_rows.extend(rows_A)

    # -------- Regime B: d rounds, noisy syndrome (phenomenological) ---------
    # Data depol per round + measurement flips at rate p.  Threshold ~3%.
    print("\n=== Regime B: d rounds, noisy syndrome (phenomenological) ===")
    ps_B = [0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.07]
    rows_B = run_regime(
        "B_phenomenological",
        {"code_task": "surface_code:rotated_memory_x",
         "depol_data": True, "meas_p": 1.0},   # meas flip prob == p
        distances=[3, 5, 7],
        ps=ps_B,
        shots=20000,
    )
    all_rows.extend(rows_B)

    out_path = OUT / "threshold_scan.json"
    out_path.write_text(json.dumps(all_rows, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
