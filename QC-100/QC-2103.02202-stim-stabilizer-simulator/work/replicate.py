#!/usr/bin/env python3
"""
Independent replication of Gidney 2021 (arXiv:2103.02202) — Stim.

Targeted small-instance reproduction:
  * d=5 rotated surface code memory Z, rounds=5, circuit-level depolarizing noise
  * Compare Stim's Pauli-frame sampler (compile_detector_sampler) vs a naive
    stim.TableauSimulator inner-loop sampler on the SAME circuit.
  * Decode with PyMatching and extract logical error rate at several noise levels.

Prints machine-readable JSON to stdout AND writes report/evidence/results.json.
"""
from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from pathlib import Path

import numpy as np
import pymatching
import stim


HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)


def build_circuit(distance: int, rounds: int, p: float) -> stim.Circuit:
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=rounds,
        distance=distance,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )


def naive_tableau_sample(circuit: stim.Circuit, shots: int) -> np.ndarray:
    """Sample measurement results the slow way: one full tableau simulation per shot.

    This is the O(n^2)-per-measurement path (CHP-style). Each shot re-runs the full
    circuit through stim.TableauSimulator. Returns shots x num_measurements bool array.
    """
    n_meas = circuit.num_measurements
    out = np.zeros((shots, n_meas), dtype=np.bool_)
    for s in range(shots):
        sim = stim.TableauSimulator()
        sim.do_circuit(circuit)
        rec = sim.current_measurement_record()
        # rec is a list of booleans of length n_meas
        out[s, :] = np.asarray(rec, dtype=np.bool_)
    return out


def timed(fn, *args, **kw):
    t0 = time.perf_counter()
    r = fn(*args, **kw)
    return r, time.perf_counter() - t0


def part_correctness(distance: int, rounds: int, p: float, shots: int = 200) -> dict:
    """Sanity check: at zero noise, all detectors must be silent and logical obs stays 0."""
    circ = build_circuit(distance, rounds, 0.0)
    det = circ.compile_detector_sampler()
    dets, obs = det.sample(shots, separate_observables=True)
    return {
        "distance": distance,
        "rounds": rounds,
        "shots": shots,
        "any_detector_fired": bool(dets.any()),
        "any_obs_flip": bool(obs.any()),
    }


def part_speed(distance: int, rounds: int, p: float, shots_stim: int = 100_000,
               shots_naive: int = 200) -> dict:
    """Speed comparison: Stim Pauli-frame sampler vs naive TableauSimulator loop.

    Both sample the SAME noisy circuit. We compute samples/sec for each and the ratio.
    """
    circ = build_circuit(distance, rounds, p)
    n_qubits = circ.num_qubits
    n_meas = circ.num_measurements
    n_dets = circ.num_detectors

    # --- Stim Pauli-frame sampler (measurements) ---
    smp = circ.compile_sampler()
    # Warm-up + timed run
    _ = smp.sample(1024)
    t0 = time.perf_counter()
    stim_meas = smp.sample(shots_stim)
    stim_dt = time.perf_counter() - t0
    stim_rate = shots_stim / stim_dt

    # --- Stim detector sampler (bulk-friendly path used for decoding) ---
    dsmp = circ.compile_detector_sampler()
    _ = dsmp.sample(1024, separate_observables=True)
    t0 = time.perf_counter()
    stim_det_shots = shots_stim
    det_arr, obs_arr = dsmp.sample(stim_det_shots, separate_observables=True)
    stim_det_dt = time.perf_counter() - t0
    stim_det_rate = stim_det_shots / stim_det_dt

    # --- Naive tableau-loop sampler ---
    t0 = time.perf_counter()
    naive_meas = naive_tableau_sample(circ, shots_naive)
    naive_dt = time.perf_counter() - t0
    naive_rate = shots_naive / naive_dt

    return {
        "circuit": {
            "num_qubits": int(n_qubits),
            "num_measurements": int(n_meas),
            "num_detectors": int(n_dets),
            "distance": distance,
            "rounds": rounds,
            "noise_p": p,
        },
        "stim_sampler": {
            "shots": shots_stim,
            "seconds": stim_dt,
            "shots_per_sec": stim_rate,
            "output_shape": list(stim_meas.shape),
        },
        "stim_detector_sampler": {
            "shots": stim_det_shots,
            "seconds": stim_det_dt,
            "shots_per_sec": stim_det_rate,
            "detector_shape": list(det_arr.shape),
            "obs_shape": list(obs_arr.shape),
        },
        "naive_tableau_sampler": {
            "shots": shots_naive,
            "seconds": naive_dt,
            "shots_per_sec": naive_rate,
            "output_shape": list(naive_meas.shape),
        },
        "speedup_stim_over_naive": stim_rate / naive_rate,
        "speedup_stim_det_over_naive": stim_det_rate / naive_rate,
    }


def part_decode(distance: int, rounds: int, noise_ps: list, shots: int = 20_000) -> dict:
    """Sample with Stim's detector sampler, decode with PyMatching, compute logical
    error rate per noise level."""
    results = []
    for p in noise_ps:
        circ = build_circuit(distance, rounds, p)
        dem = circ.detector_error_model(decompose_errors=True)
        matcher = pymatching.Matching.from_detector_error_model(dem)
        sampler = circ.compile_detector_sampler()

        # timed sampling
        t0 = time.perf_counter()
        det_arr, obs_arr = sampler.sample(shots, separate_observables=True)
        t_samp = time.perf_counter() - t0

        # timed decode
        t0 = time.perf_counter()
        pred = matcher.decode_batch(det_arr)
        t_dec = time.perf_counter() - t0

        # logical error = predicted observable != true observable
        # obs_arr shape: (shots, num_observables); for memory Z there is 1 observable.
        errors = int(np.any(pred != obs_arr, axis=1).sum())
        per = errors / shots
        # Wilson 95% CI (approx)
        z = 1.96
        denom = 1 + z*z/shots
        centre = per + z*z/(2*shots)
        margin = z * ((per*(1-per)/shots + z*z/(4*shots*shots))**0.5)
        lo = (centre - margin) / denom
        hi = (centre + margin) / denom
        results.append({
            "noise_p": p,
            "shots": shots,
            "errors": errors,
            "logical_error_rate": per,
            "wilson95_lo": lo,
            "wilson95_hi": hi,
            "sample_seconds": t_samp,
            "decode_seconds": t_dec,
            "num_detectors": circ.num_detectors,
            "num_qubits": circ.num_qubits,
        })
    return {
        "distance": distance,
        "rounds": rounds,
        "noise_ps": noise_ps,
        "shots_per_p": shots,
        "curve": results,
    }


def main():
    print(f"host: {platform.node()}", file=sys.stderr)
    print(f"python: {sys.version.split()[0]}", file=sys.stderr)
    print(f"stim: {stim.__version__}  pymatching: {pymatching.__version__}  numpy: {np.__version__}",
          file=sys.stderr)

    out = {
        "meta": {
            "paper": "arXiv:2103.02202",
            "title": "Stim: a fast stabilizer circuit simulator",
            "author": "Craig Gidney",
            "year": 2021,
            "replicator_dir": str(HERE.parent),
            "host": platform.node(),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "stim_version": stim.__version__,
            "pymatching_version": pymatching.__version__,
            "numpy_version": np.__version__,
        }
    }

    print("=== Part 1: correctness (noiseless d=5, rounds=5, 200 shots) ===", file=sys.stderr)
    out["correctness"] = part_correctness(5, 5, 0.0, 200)
    print(json.dumps(out["correctness"], indent=2), file=sys.stderr)

    print("=== Part 2: speed comparison at d=5, p=0.001 ===", file=sys.stderr)
    out["speed"] = part_speed(5, 5, 0.001, shots_stim=100_000, shots_naive=200)
    print(json.dumps(out["speed"], indent=2), file=sys.stderr)

    print("=== Part 3: PyMatching logical-error curve (d=5, rounds=5) ===", file=sys.stderr)
    out["decode"] = part_decode(5, 5, [0.001, 0.003, 0.005, 0.008, 0.01, 0.015, 0.02], shots=20_000)
    print(json.dumps(out["decode"], indent=2), file=sys.stderr)

    print("=== Part 4: also run d=3 and d=7 at p=0.005 for scaling flavor ===", file=sys.stderr)
    out["decode_extra"] = {
        "d3_p005": part_decode(3, 3, [0.005], shots=20_000)["curve"][0],
        "d7_p005": part_decode(7, 7, [0.005], shots=20_000)["curve"][0],
    }
    print(json.dumps(out["decode_extra"], indent=2), file=sys.stderr)

    dest = EVID / "results.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"\n== wrote {dest} ==", file=sys.stderr)
    print(json.dumps({"ok": True, "results_path": str(dest)}))


if __name__ == "__main__":
    main()
