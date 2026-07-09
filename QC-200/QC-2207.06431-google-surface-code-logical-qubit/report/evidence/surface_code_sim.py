#!/usr/bin/env python3
"""
Independent replication of arXiv:2207.06431 (Google Quantum AI, Nature 2023):
"Suppressing quantum errors by scaling a surface code logical qubit"

Core claim we test: for a rotated surface code memory experiment under
depolarizing (circuit-level) noise at physical error rate p, the logical
error rate per round eps_d DECREASES with distance d when p < threshold,
and the suppression factor Lambda = eps_{d-2} / eps_d is greater than 1.

We use Stim's built-in circuit-level noise model for a rotated_memory_z
surface code, decode syndromes with PyMatching, and sweep distances
{3, 5, 7} at physical noise p in {0.001, 0.003, 0.005, 0.01, 0.02}.

Output:
  results.json  (structured results)
  results.csv   (per-config logical error per round)
"""
import json, math, time, csv, os, sys
import numpy as np
import stim
import pymatching


def logical_error_rate_per_round(distance: int, rounds: int, p: float,
                                 shots: int, seed: int = 12345):
    """Build a Stim rotated-memory-Z surface code circuit at (d, r, p),
    sample syndromes, decode with PyMatching, and return (num_errors, shots,
    logical_error_prob, logical_error_per_round)."""
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler(seed=seed)
    dets, obs = sampler.sample(shots=shots, separate_observables=True)
    preds = matcher.decode_batch(dets)
    num_errors = int(np.sum(np.any(preds != obs, axis=1)))
    p_L = num_errors / shots
    # Per-round logical error: p_L ~ 1 - (1-eps)^r  =>  eps = 1 - (1 - p_L)^(1/r)
    # Guard against p_L == 0 (use conservative upper bound via +1/2 shots)
    p_L_eff = max(p_L, 0.5 / shots)
    eps = 1 - (1 - p_L_eff) ** (1 / rounds)
    # Wilson-like error bar for p_L, then propagated
    if 0 < p_L < 1:
        se_p_L = math.sqrt(p_L * (1 - p_L) / shots)
    else:
        se_p_L = math.sqrt((0.5 / shots) * (1 - 0.5 / shots) / shots)
    se_eps = se_p_L / (rounds * max((1 - p_L_eff), 1e-12))
    return {
        "distance": distance,
        "rounds": rounds,
        "p": p,
        "shots": shots,
        "num_logical_errors": num_errors,
        "p_L": p_L,
        "p_L_se": se_p_L,
        "eps_per_round": eps,
        "eps_per_round_se": se_eps,
    }


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    t0 = time.time()

    # Config: match Google paper's ROUNDS = 25 memory cycles
    rounds = 25
    # Distances: d=3,5 (headline comparison), plus d=7 to show trend
    distances = [3, 5, 7]
    # Physical noise sweep. Threshold in the paper's circuit-noise model is
    # ~0.5-1% for surface code with matching. We probe below/near/above.
    ps = [0.001, 0.003, 0.005, 0.01, 0.02]

    # Shot budget scaled per (p, d) so runtime stays reasonable but tail
    # is well-resolved for small p (very few logical errors otherwise).
    def shot_budget(p, d):
        if p <= 0.001:
            return {3: 200_000, 5: 400_000, 7: 400_000}[d]
        if p <= 0.003:
            return {3: 100_000, 5: 200_000, 7: 200_000}[d]
        if p <= 0.005:
            return {3: 50_000,  5: 100_000, 7: 100_000}[d]
        if p <= 0.01:
            return {3: 20_000,  5: 40_000,  7: 40_000}[d]
        return {3: 10_000, 5: 20_000, 7: 20_000}[d]

    rows = []
    for p in ps:
        for d in distances:
            shots = shot_budget(p, d)
            print(f"[run] d={d} p={p} rounds={rounds} shots={shots}", flush=True)
            r = logical_error_rate_per_round(d, rounds, p, shots, seed=1000 + d * 7 + int(p * 1e5))
            print(f"     -> logical_errors={r['num_logical_errors']} p_L={r['p_L']:.4g} "
                  f"eps/round={r['eps_per_round']:.4g} +/- {r['eps_per_round_se']:.2g}",
                  flush=True)
            rows.append(r)

    # Compute Lambda_{3/5} and Lambda_{5/7} per p
    by_pd = {(r["p"], r["distance"]): r for r in rows}
    lambdas = []
    for p in ps:
        row = {"p": p}
        for a, b in [(3, 5), (5, 7)]:
            ea = by_pd[(p, a)]["eps_per_round"]
            eb = by_pd[(p, b)]["eps_per_round"]
            if eb > 0:
                row[f"Lambda_{a}/{b}"] = ea / eb
            else:
                row[f"Lambda_{a}/{b}"] = float("inf")
        lambdas.append(row)

    elapsed = time.time() - t0
    out = {
        "paper": "arXiv:2207.06431",
        "tool_versions": {
            "stim": stim.__version__,
            "pymatching": pymatching.__version__,
            "numpy": np.__version__,
            "python": sys.version.split()[0],
        },
        "config": {
            "code": "rotated_memory_z (Stim built-in)",
            "noise_model": "circuit-level depolarizing (Stim: after_clifford_depolarization + reset_flip + measure_flip + before_round_data_depolarization)",
            "rounds": rounds,
            "distances": distances,
            "physical_error_rates": ps,
        },
        "results": rows,
        "lambda_ratios": lambdas,
        "elapsed_seconds": elapsed,
    }
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(out, f, indent=2)

    # CSV
    with open(os.path.join(out_dir, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "distance", "rounds", "p", "shots",
            "num_logical_errors", "p_L", "p_L_se",
            "eps_per_round", "eps_per_round_se"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Save a Stim circuit sample for evidence (d=5, p=0.001, rounds=25 header)
    demo = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=5, rounds=25,
        after_clifford_depolarization=0.001,
        after_reset_flip_probability=0.001,
        before_measure_flip_probability=0.001,
        before_round_data_depolarization=0.001)
    with open(os.path.join(out_dir, "example_circuit_d5_r25_p1e-3.stim"), "w") as f:
        f.write(str(demo))

    print(f"[done] elapsed {elapsed:.1f}s. Wrote results.json + results.csv")


if __name__ == "__main__":
    main()
