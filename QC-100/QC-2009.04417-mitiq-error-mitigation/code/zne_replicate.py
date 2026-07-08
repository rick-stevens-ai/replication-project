"""
Independent replication of Mitiq (arXiv:2009.04417) headline claim:
Zero-Noise Extrapolation (ZNE) recovers noiseless expectation values from noisy ones.

Setup mirrors Fig. 3 of the paper (two-qubit RB-style circuits, noiseless <00|rho|00>=1).
We construct a self-inverse circuit U * U^dagger on 2 qubits so the noiseless expectation
value of |00><00| is exactly 1. We then simulate under depolarizing noise via Qiskit Aer,
compute:
    - noiseless truth (from statevector or noise-free Aer)
    - raw noisy expectation value
    - ZNE-mitigated expectation value (Richardson + polynomial)
And show |mitigated - truth| < |noisy - truth|.
"""

import json
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_gates_at_random
from mitiq.zne.inference import RichardsonFactory, PolyFactory, LinearFactory

RNG = np.random.default_rng(20260703)
SHOTS = 20000
EVIDENCE = Path(__file__).resolve().parent.parent / "report" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


def rb_like_circuit(n_qubits: int = 2, depth: int = 8, seed: int = 1) -> QuantumCircuit:
    """Build a random 2q circuit and append its inverse -> noiseless identity.
    Ground-truth <00|rho|00> = 1."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n_qubits)
    for _ in range(depth):
        for q in range(n_qubits):
            qc.rz(rng.uniform(0, 2 * np.pi), q)
            qc.rx(rng.uniform(0, 2 * np.pi), q)
            qc.rz(rng.uniform(0, 2 * np.pi), q)
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
    # invert
    inv = qc.inverse()
    qc.compose(inv, inplace=True)
    return qc


def build_noisy_backend(p1: float = 0.005, p2: float = 0.02) -> AerSimulator:
    """Depolarizing noise: single-qubit p1, two-qubit p2."""
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["rz", "rx", "ry", "h", "s", "sdg", "x", "y", "z", "u", "u1", "u2", "u3"])
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx", "cz"])
    sim = AerSimulator(noise_model=nm)
    return sim


NOISELESS_SIM = AerSimulator()
NOISY_SIM = build_noisy_backend(p1=0.01, p2=0.04)  # moderate noise to see effect


def _prob00(counts: dict, n_qubits: int = 2) -> float:
    total = sum(counts.values())
    zero_key = "0" * n_qubits
    return counts.get(zero_key, 0) / total if total else 0.0


def executor_noisy(circuit: QuantumCircuit) -> float:
    """Mitiq executor: run circuit under noise, return <00|rho|00>."""
    circ = circuit.copy()
    circ.measure_all()
    tqc = transpile(circ, NOISY_SIM, optimization_level=0)
    result = NOISY_SIM.run(tqc, shots=SHOTS, seed_simulator=int(RNG.integers(1, 1_000_000))).result()
    counts = result.get_counts()
    return _prob00(counts, circuit.num_qubits)


def executor_noiseless(circuit: QuantumCircuit) -> float:
    circ = circuit.copy()
    circ.measure_all()
    tqc = transpile(circ, NOISELESS_SIM, optimization_level=0)
    result = NOISELESS_SIM.run(tqc, shots=SHOTS, seed_simulator=int(RNG.integers(1, 1_000_000))).result()
    counts = result.get_counts()
    return _prob00(counts, circuit.num_qubits)


def run_one(seed: int, depth: int) -> dict:
    circ = rb_like_circuit(n_qubits=2, depth=depth, seed=seed)

    truth = executor_noiseless(circ)
    raw_noisy = executor_noisy(circ)

    # Richardson (3-point default)
    rich = RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])
    zne_rich = zne.execute_with_zne(circ, executor_noisy, factory=rich, scale_noise=fold_gates_at_random)

    # Quadratic polynomial (paper's default in Fig 4)
    poly = PolyFactory(scale_factors=[1.0, 2.0, 3.0], order=2)
    zne_poly = zne.execute_with_zne(circ, executor_noisy, factory=poly, scale_noise=fold_gates_at_random)

    # Linear
    lin = LinearFactory(scale_factors=[1.0, 2.0, 3.0])
    zne_lin = zne.execute_with_zne(circ, executor_noisy, factory=lin, scale_noise=fold_gates_at_random)

    return {
        "seed": seed,
        "depth": depth,
        "n_gates_before_fold": circ.size(),
        "truth": truth,
        "raw_noisy": raw_noisy,
        "zne_richardson": zne_rich,
        "zne_poly2": zne_poly,
        "zne_linear": zne_lin,
        "err_raw": abs(raw_noisy - truth),
        "err_rich": abs(zne_rich - truth),
        "err_poly": abs(zne_poly - truth),
        "err_lin": abs(zne_lin - truth),
    }


def main():
    print(f"[start] mitiq ZNE replication  shots={SHOTS}")
    depth = 8
    seeds = list(range(1, 11))  # 10 independent circuits
    results = []
    t0 = time.time()
    for i, s in enumerate(seeds, 1):
        r = run_one(s, depth)
        results.append(r)
        print(
            f"  circ {i:2d}/{len(seeds)}: truth={r['truth']:.3f}  "
            f"raw={r['raw_noisy']:.3f}  ZNE-rich={r['zne_richardson']:.3f}  "
            f"ZNE-poly={r['zne_poly2']:.3f}  ZNE-lin={r['zne_linear']:.3f}"
        )

    elapsed = time.time() - t0

    truth_mean = float(np.mean([r["truth"] for r in results]))
    raw_mean = float(np.mean([r["raw_noisy"] for r in results]))
    zne_rich_mean = float(np.mean([r["zne_richardson"] for r in results]))
    zne_poly_mean = float(np.mean([r["zne_poly2"] for r in results]))
    zne_lin_mean = float(np.mean([r["zne_linear"] for r in results]))

    err_raw_mean = float(np.mean([r["err_raw"] for r in results]))
    err_rich_mean = float(np.mean([r["err_rich"] for r in results]))
    err_poly_mean = float(np.mean([r["err_poly"] for r in results]))
    err_lin_mean = float(np.mean([r["err_lin"] for r in results]))

    summary = {
        "paper": "arXiv:2009.04417 (Mitiq)",
        "claim_tested": "ZNE-mitigated expectation value is closer to noiseless truth than raw noisy value (Fig. 3 headline).",
        "n_qubits": 2,
        "circuit_depth_pre_fold": depth,
        "shots_per_circuit_per_scale": SHOTS,
        "n_circuits": len(seeds),
        "noise_model": {"single_qubit_depolarizing_p": 0.01, "two_qubit_depolarizing_p": 0.04},
        "means": {
            "truth_p00": truth_mean,
            "raw_noisy_p00": raw_mean,
            "zne_richardson_p00": zne_rich_mean,
            "zne_poly2_p00": zne_poly_mean,
            "zne_linear_p00": zne_lin_mean,
        },
        "mean_abs_error_vs_truth": {
            "raw_noisy": err_raw_mean,
            "zne_richardson": err_rich_mean,
            "zne_poly2": err_poly_mean,
            "zne_linear": err_lin_mean,
        },
        "improvement_ratio_raw_over_best_zne": err_raw_mean / min(err_rich_mean, err_poly_mean, err_lin_mean),
        "elapsed_seconds": elapsed,
        "verdict_local": (
            "REPLICATED"
            if min(err_rich_mean, err_poly_mean, err_lin_mean) < err_raw_mean
            else "CONTRADICTED"
        ),
        "per_circuit": results,
    }

    outp = EVIDENCE / "zne_results.json"
    outp.write_text(json.dumps(summary, indent=2))
    print(f"\n[done] wrote {outp}  in {elapsed:.1f}s")
    print(f"  truth  ≈ {truth_mean:.3f}")
    print(f"  raw    ≈ {raw_mean:.3f}   err={err_raw_mean:.3f}")
    print(f"  ZNE R  ≈ {zne_rich_mean:.3f}   err={err_rich_mean:.3f}")
    print(f"  ZNE P2 ≈ {zne_poly_mean:.3f}   err={err_poly_mean:.3f}")
    print(f"  ZNE L  ≈ {zne_lin_mean:.3f}   err={err_lin_mean:.3f}")
    print(f"  verdict_local = {summary['verdict_local']}")


if __name__ == "__main__":
    main()
