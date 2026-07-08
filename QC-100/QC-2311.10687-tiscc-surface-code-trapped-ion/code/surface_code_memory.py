"""
Surface code memory experiment: d=3, d=5 rotated surface code memory
Circuit-level depolarizing noise via Stim's standard generator.
Decoded with PyMatching. Measures logical error rate p_L vs physical error rate p.

This is a SPOT-CHECK reproducing the standard surface code behavior
(rotated_memory_z circuit) — the code family used by the TISCC paper as
its target abstraction.
"""
import json
import time
import numpy as np
import stim
import pymatching


def run_experiment(distance: int, p: float, rounds: int, shots: int, seed: int = 1234):
    """Build a rotated surface code memory circuit, sample syndromes, decode, return errors."""
    circuit = stim.Circuit.generated(
        code_task="surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    # Convert to detector error model + matching graph
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)

    sampler = circuit.compile_detector_sampler(seed=seed)
    detector_samples, actual_observables = sampler.sample(
        shots=shots, separate_observables=True
    )

    predictions = matcher.decode_batch(detector_samples)
    errors = int(np.sum(np.any(predictions != actual_observables, axis=1)))
    return errors


def main():
    ps = [1e-3, 3e-3, 1e-2]
    distances = [3, 5]
    rounds_map = {3: 3, 5: 5}          # d rounds (standard)
    shots_map = {1e-3: 20000, 3e-3: 20000, 1e-2: 10000}

    results = []
    t0 = time.time()
    for d in distances:
        for p in ps:
            shots = shots_map[p]
            r = rounds_map[d]
            t_a = time.time()
            errs = run_experiment(d, p, r, shots)
            dt = time.time() - t_a
            p_L = errs / shots
            # Wilson-ish stderr
            se = (p_L * (1 - p_L) / shots) ** 0.5
            row = {
                "distance": d,
                "rounds": r,
                "p_physical": p,
                "shots": shots,
                "errors": errs,
                "p_logical": p_L,
                "stderr": se,
                "sec": round(dt, 2),
            }
            results.append(row)
            print(
                f"d={d}  p={p:.0e}  rounds={r}  shots={shots}  errs={errs}  "
                f"p_L={p_L:.4e}  se={se:.2e}  ({dt:.1f}s)"
            )
    total = time.time() - t0
    out = {
        "stim_version": stim.__version__,
        "pymatching_version": pymatching.__version__,
        "code_task": "surface_code:rotated_memory_z",
        "noise_model": "uniform circuit-level depolarizing "
        "(after_clifford_depolarization = after_reset_flip = "
        "before_measure_flip = before_round_data_depolarization = p)",
        "results": results,
        "total_sec": round(total, 2),
    }
    with open("results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nTotal wall-clock: {total:.1f}s")
    print("Wrote results.json")


if __name__ == "__main__":
    main()
