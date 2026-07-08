#!/usr/bin/env python3
"""
Surface-code threshold sanity check for QC-100 replication of
arXiv:1712.00294 (Fukui/Tomita/Okamoto/Fujii, 2017/18)
"High-threshold fault-tolerant quantum computation with analog quantum error correction"

The paper's headline is an *analog-QEC-enhanced* threshold for GKP-encoded
surface codes under a Gaussian channel (σ_th improves from ~0.542 digital
to ~0.607 analog, corresponding to squeezing-level reduction from 4.7 dB
to 3.5 dB in the phenomenological model).

Full GKP/analog reproduction is out of scope for a small CPU replication.
What IS a real, cheap sanity check that verifies the *methodology*
(surface code + MWPM decoding) the paper builds on:

  - Simulate rotated surface code at distances d = 3, 5, 7
  - Standard depolarizing circuit-level noise (Stim's built-in)
  - MWPM decoding via PyMatching
  - Extract logical error rate vs physical error rate p
  - Verify the crossing/threshold behavior around p_th ~ 0.5%-1.0%

This confirms the *substrate* (surface code + MWPM) that the paper's
analog upgrade sits on top of. Verdict target: SPOT-CHECK/PARTIAL.
"""
import stim, pymatching, numpy as np, json, time, sys, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "report", "evidence")
os.makedirs(OUT, exist_ok=True)


def count_logical_errors(circuit: stim.Circuit, num_shots: int) -> int:
    sampler = circuit.compile_detector_sampler()
    detection_events, observable_flips = sampler.sample(
        num_shots, separate_observables=True
    )
    detector_error_model = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(detector_error_model)
    predictions = matcher.decode_batch(detection_events)
    num_errors = int(np.sum(np.any(predictions != observable_flips, axis=1)))
    return num_errors


def run():
    distances = [3, 5, 7]
    # depolarizing noise strengths spanning the ~1% threshold
    physical_ps = [0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03]
    shots_per_point = 20000

    results = {
        "paper": "arXiv:1712.00294",
        "sim_tool": {"stim": stim.__version__, "pymatching": pymatching.__version__,
                     "numpy": np.__version__},
        "code": "rotated_memory_z (surface code)",
        "noise_model": "circuit-level depolarizing (Stim built-in)",
        "shots_per_point": shots_per_point,
        "runs": [],
    }

    t0 = time.time()
    for d in distances:
        for p in physical_ps:
            circuit = stim.Circuit.generated(
                "surface_code:rotated_memory_z",
                rounds=d,
                distance=d,
                after_clifford_depolarization=p,
                after_reset_flip_probability=p,
                before_measure_flip_probability=p,
                before_round_data_depolarization=p,
            )
            n_err = count_logical_errors(circuit, shots_per_point)
            p_L = n_err / shots_per_point
            se = float(np.sqrt(max(p_L * (1 - p_L), 1e-12) / shots_per_point))
            row = {
                "distance": d,
                "physical_p": p,
                "shots": shots_per_point,
                "logical_errors": n_err,
                "logical_error_rate": p_L,
                "stderr": se,
            }
            results["runs"].append(row)
            print(f"  d={d:>2}  p={p:.4f}  logical={n_err:>5}/{shots_per_point}  "
                  f"p_L={p_L:.5f}  se={se:.5f}",
                  flush=True)
    results["wall_time_seconds"] = round(time.time() - t0, 1)

    out_path = os.path.join(OUT, "threshold_scan.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}")

    # crude threshold extraction: p_th ~ where the d curves cross
    print("\nLogical error rate table (rows=distance, cols=physical_p):")
    print("d \\ p", "  ".join(f"{p:>7.4f}" for p in physical_ps))
    for d in distances:
        row_vals = [r["logical_error_rate"] for r in results["runs"] if r["distance"] == d]
        print(f"d={d:<3}", "  ".join(f"{v:>7.5f}" for v in row_vals))

    # find approximate crossing
    ps = np.array(physical_ps)
    curves = {d: np.array([r["logical_error_rate"] for r in results["runs"]
                           if r["distance"] == d]) for d in distances}
    threshold_estimate = None
    for i in range(len(ps) - 1):
        # threshold: the smallest p where larger d starts to give higher p_L
        if (curves[7][i] < curves[3][i]) and (curves[7][i + 1] >= curves[3][i + 1]):
            threshold_estimate = 0.5 * (ps[i] + ps[i + 1])
            break
    if threshold_estimate is None:
        # fall back: p where d=3 and d=7 curves cross
        diff = curves[3] - curves[7]
        sign_change = np.where(np.diff(np.sign(diff)) != 0)[0]
        if len(sign_change) > 0:
            i = sign_change[0]
            threshold_estimate = 0.5 * (ps[i] + ps[i + 1])
    print(f"\nApprox threshold p_th ~ {threshold_estimate} "
          f"(target ~ 0.005-0.01 for circuit-level depolarizing)")
    results["approx_threshold"] = float(threshold_estimate) if threshold_estimate else None
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    run()
