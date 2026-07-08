"""
Linear Cross-Entropy Benchmarking (Linear XEB) demonstration.

Replicating the core benchmark discussed in:
  Aaronson & Gunn, "On the Classical Hardness of Spoofing Linear Cross-Entropy
  Benchmarking", arXiv:1910.12085 (2019/2020).

Paper's key facts (Section 2, page 4):
  - For samples z from an *ideal* random-circuit distribution (Porter-Thomas):
        E[|<z|C|0^n>|^2] ~= 2 / 2^n
    i.e. F_XEB := 2^n * E[P(z)]  ~=  2  (equivalently, XHOG parameter b ~= 2).
  - For samples z drawn *uniformly at random* from {0,1}^n:
        E[P(z)] = 1/2^n  =>  F_XEB = 1  (spoofing parameter b = 1, trivial).

We build small random circuits (n = 4..8 qubits) in Cirq, compute the exact
statevector, then:
   (a) sample from the ideal distribution      -> expect F_XEB ~ 2
   (b) sample uniformly                        -> expect F_XEB ~ 1

We also report the standard "linear XEB fidelity" estimator
        F  =  2^n * mean_i P(z_i)  -  1
which is 0 for uniform noise and ~1 for perfect Porter-Thomas sampling
(this is the Google-supremacy convention). Both conventions are reported.
"""

import json
import time
from pathlib import Path

import cirq
import numpy as np


def random_google_style_circuit(n_qubits: int, depth: int, rng: np.random.Generator) -> cirq.Circuit:
    """1D chain of qubits; alternating layers of random single-qubit gates
    (sqrt-X / sqrt-Y / sqrt-W) and neighbor CZ entanglers, then a final layer
    of random single-qubit gates. Mimics the Boixo/Arute recipe on a line.
    """
    qubits = cirq.LineQubit.range(n_qubits)
    # Google-supremacy-style random single-qubit gate set: sqrt(X), sqrt(Y), sqrt(W)
    # where W = (X+Y)/sqrt(2). Realize sqrt(W) as PhasedXPowGate(phase_exponent=0.25, exponent=0.5).
    single_qubit_choices = [
        cirq.X ** 0.5,
        cirq.Y ** 0.5,
        cirq.PhasedXPowGate(phase_exponent=0.25, exponent=0.5),  # sqrt(W)
    ]
    circuit = cirq.Circuit()
    # Initial Hadamard layer to get out of |0..0>
    circuit.append(cirq.H.on_each(*qubits))

    last_single = [-1] * n_qubits  # avoid repeating the same 1q gate on a qubit
    for layer in range(depth):
        # single-qubit random layer
        for i, q in enumerate(qubits):
            while True:
                idx = int(rng.integers(len(single_qubit_choices)))
                if idx != last_single[i]:
                    break
            last_single[i] = idx
            circuit.append(single_qubit_choices[idx].on(q))
        # two-qubit entangling layer; alternate even/odd pairs
        if layer % 2 == 0:
            pairs = [(qubits[i], qubits[i + 1]) for i in range(0, n_qubits - 1, 2)]
        else:
            pairs = [(qubits[i], qubits[i + 1]) for i in range(1, n_qubits - 1, 2)]
        for a, b in pairs:
            circuit.append(cirq.CZ(a, b))

    # Final single-qubit layer
    for i, q in enumerate(qubits):
        idx = int(rng.integers(len(single_qubit_choices)))
        circuit.append(single_qubit_choices[idx].on(q))
    return circuit


def ideal_probabilities(circuit: cirq.Circuit, n_qubits: int) -> np.ndarray:
    """Return the length-2^n array of ideal output probabilities."""
    simulator = cirq.Simulator(dtype=np.complex128)
    state = simulator.simulate(circuit).final_state_vector
    probs = np.abs(state) ** 2
    # numerical safety
    probs = probs / probs.sum()
    return probs


def sample_ideal(probs: np.ndarray, n_samples: int, rng: np.random.Generator) -> np.ndarray:
    """Sample indices from the ideal distribution."""
    dim = probs.shape[0]
    return rng.choice(dim, size=n_samples, replace=True, p=probs)


def sample_uniform(n_qubits: int, n_samples: int, rng: np.random.Generator) -> np.ndarray:
    return rng.integers(0, 2 ** n_qubits, size=n_samples)


def xeb_scores(probs: np.ndarray, sample_indices: np.ndarray, n_qubits: int) -> dict:
    """Return both XEB conventions.

    b_xhog       = 2^n * mean_i P(z_i)                  (Aaronson-Gunn XHOG "b")
    linear_xeb_F = 2^n * mean_i P(z_i) - 1              (Google-supremacy F_XEB)
    """
    p_of_z = probs[sample_indices]
    mean_p = float(np.mean(p_of_z))
    b_xhog = (2 ** n_qubits) * mean_p
    linear_xeb_f = b_xhog - 1.0
    # sample-mean standard error for the mean of 2^n * P(z_i)
    stderr = float((2 ** n_qubits) * np.std(p_of_z, ddof=1) / np.sqrt(len(p_of_z)))
    return {
        "mean_prob": mean_p,
        "b_xhog": b_xhog,
        "linear_xeb_F": linear_xeb_f,
        "stderr_of_b": stderr,
        "n_samples": int(len(sample_indices)),
    }


def porter_thomas_stats(probs: np.ndarray) -> dict:
    """Sanity check: for a Haar-random state on 2^n dim, 2^n * P should be ~ Exp(1),
    with E = 1, Var = 1. Ideal XEB (samples from the state itself) then gives
        E[2^n * P(z)] = E[X^2] / E[X] where X = 2^n * P for uniform z ...
    Concretely: mean(2^n * P over uniform z) = 1, mean(2^n * P over samples from P) = 2.
    """
    dim = probs.shape[0]
    scaled = dim * probs
    return {
        "mean_scaled_prob_over_dim": float(scaled.mean()),  # should be 1.0
        "var_scaled_prob": float(scaled.var()),            # ~1 for PT
        "sum_prob": float(probs.sum()),
        "dim": int(dim),
    }


def run_experiment(seed: int = 42, ns=(4, 5, 6, 7, 8), depth_map=None, n_circuits=20, n_samples=20000):
    if depth_map is None:
        depth_map = {4: 10, 5: 10, 6: 12, 7: 14, 8: 16}
    rng = np.random.default_rng(seed)
    all_results = []
    for n in ns:
        depth = depth_map.get(n, 12)
        per_n_ideal = []
        per_n_uniform = []
        pt_means = []
        pt_vars = []
        t0 = time.time()
        for c_idx in range(n_circuits):
            circ = random_google_style_circuit(n, depth, rng)
            probs = ideal_probabilities(circ, n)
            pt = porter_thomas_stats(probs)
            pt_means.append(pt["mean_scaled_prob_over_dim"])
            pt_vars.append(pt["var_scaled_prob"])
            idx_ideal = sample_ideal(probs, n_samples, rng)
            idx_uniform = sample_uniform(n, n_samples, rng)
            per_n_ideal.append(xeb_scores(probs, idx_ideal, n))
            per_n_uniform.append(xeb_scores(probs, idx_uniform, n))
        t1 = time.time()

        def agg(records, key):
            vals = np.array([r[key] for r in records], dtype=float)
            return float(vals.mean()), float(vals.std(ddof=1)), float(vals.std(ddof=1) / np.sqrt(len(vals)))

        b_ideal_mean, b_ideal_std, b_ideal_sem = agg(per_n_ideal, "b_xhog")
        b_unif_mean, b_unif_std, b_unif_sem = agg(per_n_uniform, "b_xhog")
        f_ideal_mean, _, f_ideal_sem = agg(per_n_ideal, "linear_xeb_F")
        f_unif_mean, _, f_unif_sem = agg(per_n_uniform, "linear_xeb_F")

        result = {
            "n_qubits": n,
            "depth": depth,
            "n_circuits": n_circuits,
            "n_samples_per_circuit": n_samples,
            "wall_time_sec": round(t1 - t0, 3),
            "porter_thomas_check": {
                "mean_scaled_prob": float(np.mean(pt_means)),  # ~1.0
                "var_scaled_prob": float(np.mean(pt_vars)),    # ~1.0 for PT
            },
            "ideal_sampling": {
                "b_xhog_mean": b_ideal_mean,
                "b_xhog_std_across_circuits": b_ideal_std,
                "b_xhog_sem_across_circuits": b_ideal_sem,
                "linear_xeb_F_mean": f_ideal_mean,
                "linear_xeb_F_sem": f_ideal_sem,
            },
            "uniform_spoof": {
                "b_xhog_mean": b_unif_mean,
                "b_xhog_std_across_circuits": b_unif_std,
                "b_xhog_sem_across_circuits": b_unif_sem,
                "linear_xeb_F_mean": f_unif_mean,
                "linear_xeb_F_sem": f_unif_sem,
            },
        }
        all_results.append(result)
        print(
            f"n={n:2d} depth={depth:2d}  "
            f"PT mean={result['porter_thomas_check']['mean_scaled_prob']:.4f} var={result['porter_thomas_check']['var_scaled_prob']:.4f}  |  "
            f"IDEAL b={b_ideal_mean:.4f}+/-{b_ideal_sem:.4f} F={f_ideal_mean:.4f}+/-{f_ideal_sem:.4f}  |  "
            f"UNIF  b={b_unif_mean:.4f}+/-{b_unif_sem:.4f} F={f_unif_mean:.4f}+/-{f_unif_sem:.4f}  |  "
            f"{result['wall_time_sec']}s"
        )
    return all_results


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n-circuits", type=int, default=20)
    ap.add_argument("--n-samples", type=int, default=20000)
    args = ap.parse_args()

    print("cirq version:", cirq.__version__)
    print("numpy version:", np.__version__)
    results = run_experiment(seed=args.seed, n_circuits=args.n_circuits, n_samples=args.n_samples)

    out_path = args.out or "results.json"
    Path(out_path).write_text(json.dumps({
        "cirq_version": cirq.__version__,
        "numpy_version": np.__version__,
        "seed": args.seed,
        "n_circuits": args.n_circuits,
        "n_samples_per_circuit": args.n_samples,
        "results": results,
    }, indent=2))
    print("Wrote:", out_path)
