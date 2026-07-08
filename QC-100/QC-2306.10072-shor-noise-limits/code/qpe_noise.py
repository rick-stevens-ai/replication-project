"""Isolate Cai's QFT-angle noise mechanism on a Quantum Phase Estimation
circuit where the true phase is NON-dyadic. This is the cleanest possible
test-bed for the paper's claim: without QFT-angle noise the QPE has a
sharp peak near round(phi*2^n); with the Cai perturbation the peak
degrades and eventually washes out.

We use phi = 1 / golden_ratio = 0.6180339887... (highly irrational,
worst-case Diophantine approximation) as the eigenphase, and estimate it
on n_count phase qubits with a controlled-P(2*pi*phi) as the target U.

Success metric: probability of measuring within +/-1 of the closest
integer to phi * 2^n_count. This is a standard QPE success band.

We ALSO run a "concatenated QPE" experiment with n_count = 6, 8, 10
qubits to see how the noise threshold scales with n — Cai's theorem
predicts a threshold that shrinks like ~ n^{-1/3} in the QFT gate count.
"""

from __future__ import annotations
import json
import math
import time
from pathlib import Path
from statistics import mean, stdev

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

PHI_TRUE = (math.sqrt(5) - 1) / 2  # 1/golden_ratio ≈ 0.6180339887


def iqft_with_noise(qc: QuantumCircuit, qubits: list[int], eps: float,
                     rng: np.random.Generator) -> None:
    """Inverse QFT with Cai-style angle noise (2306.10072). Angle noise
    on the controlled-R_k gate is 2*pi*eps*r/2^k with r ~ N(0,1)."""
    n = len(qubits)
    for j in reversed(range(n)):
        for m in reversed(range(j + 1, n)):
            k = m - j + 1
            base = -2.0 * math.pi / (2 ** k)
            noise = (2.0 * math.pi * eps * rng.standard_normal() / (2 ** k)
                     if eps > 0.0 else 0.0)
            qc.cp(base + noise, qubits[m], qubits[j])
        qc.h(qubits[j])
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])


def qpe_circuit(n_count: int, phi: float, eps: float,
                rng: np.random.Generator) -> QuantumCircuit:
    """QPE for the 1-qubit unitary U = P(2*pi*phi). Its eigenstate |1>
    has eigenphase exp(2*pi*i*phi). Uses n_count phase qubits + 1 target."""
    ph = QuantumRegister(n_count, "phase")
    tg = QuantumRegister(1, "target")
    cr = ClassicalRegister(n_count, "c")
    qc = QuantumCircuit(ph, tg, cr)

    for q in range(n_count):
        qc.h(ph[q])
    qc.x(tg[0])  # eigenstate

    for q in range(n_count):
        angle = 2.0 * math.pi * phi * (2 ** q)
        qc.cp(angle, ph[q], tg[0])

    iqft_with_noise(qc, [ph[q] for q in range(n_count)], eps, rng)

    for q in range(n_count):
        qc.measure(ph[q], cr[q])
    return qc


def success_band(bitstr: str, phi: float, n_count: int, tol_bits: int = 1) -> bool:
    """Success = measured integer is within tol_bits of the closest integer
    to phi * 2^n_count. int(bitstr, 2) matches the (reversed-phase-register)
    convention that we already verified in the N=15 smoke test."""
    meas = int(bitstr, 2)
    ideal = round(phi * (2 ** n_count)) % (2 ** n_count)
    diff = min(abs(meas - ideal), (2 ** n_count) - abs(meas - ideal))
    return diff <= tol_bits


def run_qpe_cai_sweep(n_count: int, shots: int, eps_list: list[float],
                       n_trials: int, seed: int, outdir: Path) -> dict:
    sim = AerSimulator(method="statevector")
    master = np.random.default_rng(seed)
    results = []
    for eps in eps_list:
        rates = []
        for _ in range(n_trials):
            ts = int(master.integers(0, 2**32 - 1))
            rng = np.random.default_rng(ts)
            qc = qpe_circuit(n_count, PHI_TRUE, eps, rng)
            tqc = transpile(qc, sim, optimization_level=0)
            counts = sim.run(tqc, shots=shots, seed_simulator=ts).result().get_counts()
            succ = sum(c for bs, c in counts.items()
                       if success_band(bs, PHI_TRUE, n_count))
            rates.append(succ / shots)
        m = float(mean(rates))
        s = float(stdev(rates)) if len(rates) > 1 else 0.0
        results.append({"eps": eps, "mean_success": m, "std_success": s,
                        "n_trials": n_trials, "shots": shots,
                        "per_trial": rates})
        print(f"[QPE Cai n_count={n_count}] eps={eps:>7.4g}  "
              f"mean={m:.4f}  std={s:.4f}")
    payload = {
        "experiment": "QPE with Cai QFT-angle noise (non-dyadic phase)",
        "paper": "arXiv:2306.10072",
        "phi_true": PHI_TRUE, "n_count": n_count,
        "shots_per_trial": shots, "n_trials": n_trials,
        "success_band_bits": 1,
        "results": results,
    }
    (outdir / f"qpe_cai_n{n_count}.json").write_text(json.dumps(payload, indent=2))
    return payload


def run_qpe_depolarizing_sweep(n_count: int, shots: int, p_list: list[float],
                                seed: int, outdir: Path) -> dict:
    rng = np.random.default_rng(seed)
    qc = qpe_circuit(n_count, PHI_TRUE, 0.0, rng)
    results = []
    for p in p_list:
        if p == 0.0:
            sim = AerSimulator(method="statevector")
        else:
            nm = NoiseModel()
            one_q = ["u", "u1", "u2", "u3", "h", "x", "y", "z", "s", "sdg",
                     "t", "tdg", "p", "rz", "rx", "ry", "id"]
            two_q = ["cx", "cz", "cp", "swap"]
            nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), one_q)
            nm.add_all_qubit_quantum_error(depolarizing_error(min(1.0, p*10), 2), two_q)
            sim = AerSimulator(method="density_matrix", noise_model=nm)
        tqc = transpile(qc, sim, optimization_level=0)
        counts = sim.run(tqc, shots=shots, seed_simulator=seed).result().get_counts()
        succ = sum(c for bs, c in counts.items()
                   if success_band(bs, PHI_TRUE, n_count))
        rate = succ / shots
        results.append({"p_1q": p, "p_2q": min(1.0, p*10),
                        "success_rate": rate, "shots": shots})
        print(f"[QPE Depol. n_count={n_count}] p_1q={p:.4g}  "
              f"p_2q={min(1.0,p*10):.4g}  rate={rate:.4f}")
    payload = {
        "experiment": "QPE with depolarizing noise (non-dyadic phase)",
        "phi_true": PHI_TRUE, "n_count": n_count, "shots": shots,
        "results": results,
    }
    (outdir / f"qpe_dep_n{n_count}.json").write_text(json.dumps(payload, indent=2))
    return payload


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="../report/evidence")
    ap.add_argument("--shots", type=int, default=4096)
    ap.add_argument("--n_trials", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20260703)
    args = ap.parse_args()
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    eps_list = [0.0, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0, 3.0]
    p_list   = [0.0, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 5e-2]

    t0 = time.time()
    print("\n=== QPE Cai-noise sweeps at n_count = 6, 8, 10 ===")
    for n_count in (6, 8, 10):
        run_qpe_cai_sweep(n_count, args.shots, eps_list, args.n_trials,
                          args.seed + n_count, outdir)

    print("\n=== QPE depolarizing-noise sweep at n_count = 8 ===")
    run_qpe_depolarizing_sweep(8, args.shots, p_list, args.seed, outdir)
    print(f"\nAll QPE experiments done in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
