"""
Shor's algorithm for N=15 with base a=7, factorable via order-finding.
Two independent noise-sweep experiments:
  (A) Cai (2306.10072) noise model — perturb each controlled-R_k rotation
      angle in the (inverse) QFT by 2*pi*eps*r/2^k with r ~ N(0,1).
  (B) Aer depolarizing noise on 1- and 2-qubit gates at increasing p.

Success metric per shot: after measuring the phase register, apply the
continued-fractions post-processing to extract a candidate period r.
A shot is "successful" iff the classical post-processing recovers a
divisor of the true order (here r=4 for a=7 mod 15) that yields a
non-trivial factor of N (i.e., gcd(a^{r/2} +/- 1, N) is 3 or 5).

Statevector simulator only (no hardware). Full Aer sim for the noise
model runs, ideal statevector for the noiseless baseline.
"""

from __future__ import annotations
import argparse
import json
import math
import os
import random
import sys
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

import numpy as np

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ---------------------------------------------------------------------------
# Modular exponentiation gate for a^x mod 15 (a in {2, 4, 7, 8, 11, 13})
# ---------------------------------------------------------------------------
# We use the classic hand-designed controlled-U_a for N=15 documented in the
# Qiskit textbook (Nielsen-Chuang, Vandersypen 2001 NMR paper). It acts on the
# 4-qubit work register and is controlled on the phase register qubit.

def _c_amod15(a: int, power: int) -> QuantumCircuit:
    """Controlled multiplication by a^power mod 15."""
    if a not in (2, 4, 7, 8, 11, 13):
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in (2, 13):
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in (7, 8):
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in (4, 11):
            U.swap(1, 3)
            U.swap(0, 2)
        if a in (7, 11, 13):
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U


# ---------------------------------------------------------------------------
# Inverse QFT built with explicit controlled-phase gates so we can inject
# Cai-style angle noise on each controlled-R_k (k = 2, 3, ..., n).
# ---------------------------------------------------------------------------

def iqft_with_noise(qc: QuantumCircuit, qubits: list[int], eps: float,
                     rng: np.random.Generator) -> None:
    """Append an inverse QFT on `qubits` (in *little-endian* Qiskit layout,
    i.e. qubits[0] = LSB) to `qc`. Each controlled-R_k gate has its rotation
    angle perturbed by 2*pi*eps*r/2^k with r ~ N(0,1). Setting eps=0 gives
    the exact inverse QFT. Includes the standard SWAP layer at the end (which
    for the inverse QFT is at the start of the equivalent forward-QFT^dagger).
    """
    n = len(qubits)
    # Standard Qiskit-textbook inverse QFT construction:
    # for j = n-1 downto 0:
    #   for m = n-1 downto j+1:  controlled-Rk^{-1} where k = m-j+1
    #   H on qubit j
    for j in reversed(range(n)):
        for m in reversed(range(j + 1, n)):
            k = m - j + 1  # >= 2
            # Ideal angle for inverse QFT controlled-R_k is -2*pi/2^k
            base = -2.0 * math.pi / (2 ** k)
            # Cai noise: multiplicative angle perturbation eps * r / 2^k
            # meaning R_k -> exp(2*pi*i*(1+eps*r)/2^k), so extra phase
            # 2*pi*eps*r/2^k. On the inverse gate we still add a random
            # perturbation of the same magnitude (sign is absorbed in r).
            if eps > 0.0:
                noise = 2.0 * math.pi * eps * rng.standard_normal() / (2 ** k)
            else:
                noise = 0.0
            qc.cp(base + noise, qubits[m], qubits[j])
        qc.h(qubits[j])
    # Bit-reversal SWAPs so that little-endian measurement matches
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])


# ---------------------------------------------------------------------------
# Full Shor circuit for N = 15
# ---------------------------------------------------------------------------

def shor15_circuit(a: int, n_count: int, eps: float,
                    rng: np.random.Generator) -> QuantumCircuit:
    """Build the Shor order-finding circuit for N=15 with `n_count` phase
    qubits and base `a`. `eps` is the Cai QFT-noise amplitude."""
    phase = QuantumRegister(n_count, "phase")
    work = QuantumRegister(4, "work")
    cr = ClassicalRegister(n_count, "c")
    qc = QuantumCircuit(phase, work, cr)

    # Initialize phase register to |+>^n and work register to |1>
    for q in range(n_count):
        qc.h(phase[q])
    qc.x(work[0])  # |0001> = 1

    # Controlled modular exponentiation
    for q in range(n_count):
        qc.append(_c_amod15(a, 2 ** q),
                  [phase[q]] + [work[0], work[1], work[2], work[3]])

    # Inverse QFT on phase register with Cai noise
    iqft_with_noise(qc, [phase[q] for q in range(n_count)], eps, rng)

    # Measure phase register into little-endian classical bits
    for q in range(n_count):
        qc.measure(phase[q], cr[q])
    return qc


# ---------------------------------------------------------------------------
# Classical post-processing: continued fractions -> candidate order -> factor
# ---------------------------------------------------------------------------

def phase_to_factor(measured_int: int, n_count: int, a: int, N: int) -> int | None:
    """Return a non-trivial factor of N if the measured integer yields one
    via the standard continued-fractions period-finding post-processing,
    else None."""
    if measured_int == 0:
        return None
    phase = measured_int / (2 ** n_count)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    if r == 0 or r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    if x in (1, N - 1):
        return None
    f1 = gcd(x - 1, N)
    f2 = gcd(x + 1, N)
    for f in (f1, f2):
        if 1 < f < N:
            return f
    return None


# ---------------------------------------------------------------------------
# Experiment drivers
# ---------------------------------------------------------------------------

def run_cai_noise_sweep(a: int, n_count: int, shots: int,
                        eps_list: list[float], seed: int,
                        outdir: Path) -> dict:
    """Sweep Cai QFT-angle noise. For each eps, build one circuit with
    freshly sampled r's (per Cai's model: r is fresh per gate), and take
    `shots` measurements from that noisy circuit. Then measure success rate
    as (# shots yielding a non-trivial factor of 15) / shots. Because the
    Cai perturbation is applied *once* per circuit compilation and Aer will
    sample many shots from it, we repeat with `n_trials` fresh circuits and
    average — matching the paper's E_r[success] convention.
    """
    N = 15
    sim = AerSimulator(method="statevector")
    n_trials = 32  # circuits per eps (i.e. 32 fresh noise realizations)

    results: list[dict] = []
    master_rng = np.random.default_rng(seed)
    for eps in eps_list:
        trial_success_rates: list[float] = []
        trial_success_counts: list[int] = []
        for t in range(n_trials):
            trial_seed = int(master_rng.integers(0, 2**32 - 1))
            rng = np.random.default_rng(trial_seed)
            qc = shor15_circuit(a=a, n_count=n_count, eps=eps, rng=rng)
            tqc = transpile(qc, sim, optimization_level=0)
            job = sim.run(tqc, shots=shots, seed_simulator=trial_seed)
            counts = job.result().get_counts()
            succ = 0
            for bitstr, c in counts.items():
                # Qiskit bit string layout: cr[n-1]..cr[0] (MSB left).
                # Combined with our controlled-U ordering, the correct
                # phase integer is int(bitstr, 2) directly.
                meas = int(bitstr, 2)
                fac = phase_to_factor(meas, n_count, a, N)
                if fac is not None:
                    succ += c
            trial_success_rates.append(succ / shots)
            trial_success_counts.append(succ)
        mean = float(np.mean(trial_success_rates))
        std = float(np.std(trial_success_rates))
        results.append({
            "eps": eps,
            "mean_success_rate": mean,
            "std_success_rate": std,
            "n_trials": n_trials,
            "shots_per_trial": shots,
            "per_trial_success_rates": trial_success_rates,
        })
        print(f"[Cai noise]  eps={eps:.4g}  mean_success={mean:.4f}  std={std:.4f}"
              f"  ({n_trials} trials x {shots} shots)")
    payload = {
        "experiment": "Cai QFT rotation-angle noise sweep",
        "paper": "arXiv:2306.10072",
        "N": N, "a": a, "n_count": n_count,
        "shots_per_trial": shots, "n_trials_per_eps": n_trials,
        "seed": seed,
        "results": results,
    }
    (outdir / "cai_noise_sweep.json").write_text(json.dumps(payload, indent=2))
    return payload


def run_depolarizing_sweep(a: int, n_count: int, shots: int,
                            p_list: list[float], seed: int,
                            outdir: Path) -> dict:
    """Sweep uniform depolarizing noise. Build one ideal circuit, wrap Aer
    in a NoiseModel with depolarizing_error(p, 1) on all 1q gates and
    depolarizing_error(p, 2) on all 2q gates (density-matrix method)."""
    N = 15
    rng = np.random.default_rng(seed)
    qc = shor15_circuit(a=a, n_count=n_count, eps=0.0, rng=rng)

    results: list[dict] = []
    for p in p_list:
        if p == 0.0:
            sim = AerSimulator(method="statevector")
            tqc = transpile(qc, sim, optimization_level=0)
            job = sim.run(tqc, shots=shots, seed_simulator=seed)
        else:
            nm = NoiseModel()
            one_q = ["u", "u1", "u2", "u3", "h", "x", "y", "z", "s", "sdg", "t",
                     "tdg", "p", "rz", "rx", "ry", "id"]
            two_q = ["cx", "cz", "cp", "swap"]
            nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), one_q)
            nm.add_all_qubit_quantum_error(depolarizing_error(min(1.0, p * 10), 2), two_q)
            sim = AerSimulator(method="density_matrix", noise_model=nm)
            tqc = transpile(qc, sim, optimization_level=0)
            job = sim.run(tqc, shots=shots, seed_simulator=seed)
        counts = job.result().get_counts()
        succ = 0
        for bitstr, c in counts.items():
            meas = int(bitstr, 2)
            fac = phase_to_factor(meas, n_count, a, N)
            if fac is not None:
                succ += c
        rate = succ / shots
        results.append({
            "p": p,
            "p_1q": p, "p_2q": min(1.0, p * 10),
            "success_count": succ,
            "shots": shots,
            "success_rate": rate,
        })
        print(f"[Depolar.]   p_1q={p:.4g}  p_2q={min(1.0,p*10):.4g}  "
              f"success_rate={rate:.4f}  ({succ}/{shots})")
    payload = {
        "experiment": "Uniform depolarizing noise sweep (1q and 2q)",
        "paper": "arXiv:2306.10072 (companion Aer experiment)",
        "N": N, "a": a, "n_count": n_count,
        "shots": shots, "seed": seed,
        "results": results,
    }
    (outdir / "depolarizing_sweep.json").write_text(json.dumps(payload, indent=2))
    return payload


def gate_count_extrapolation(outdir: Path) -> dict:
    """Extrapolate the number of controlled-R_k gates in a full-precision
    Shor QFT (order-finding) for N with n-bit modulus. Number of controlled-
    R_k gates per QFT: sum_{i=2..n_qft} (n_qft - i + 1) = n(n-1)/2.
    Shor's order-finding uses n_count ~ 2n phase qubits plus one QFT.
    """
    data = []
    for nbits in [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
        n_count = 2 * nbits
        crk_qft = n_count * (n_count - 1) // 2
        # For each ctrl-R_k in the (banded) QFT, Cai requires eps < ~ n^{-1/3}
        # to keep the phase register peak intact (heuristic from Theorem 1's
        # b + log2(1/eps) < (1/3) log2 n - c). So eps_thresh ~ 1/n_count^{1/3}.
        eps_thresh = 1.0 / (n_count ** (1.0 / 3.0))
        data.append({
            "N_bits": nbits, "n_count": n_count,
            "num_ctrl_Rk_in_qft": crk_qft,
            "cai_eps_threshold_scaling": eps_thresh,
        })
    payload = {
        "note": "Controlled-R_k gate count in the (final) QFT of Shor's "
                "order-finding as a function of modulus size, and the "
                "asymptotic Cai (2306.10072) noise threshold eps ~ n^{-1/3}.",
        "table": data,
    }
    (outdir / "extrapolation.json").write_text(json.dumps(payload, indent=2))
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="report/evidence")
    ap.add_argument("--a", type=int, default=7)
    ap.add_argument("--n_count", type=int, default=8)
    ap.add_argument("--shots", type=int, default=2048)
    ap.add_argument("--seed", type=int, default=20260703)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("=== Environment ===")
    import qiskit, qiskit_aer
    print(f"qiskit={qiskit.__version__}  qiskit_aer={qiskit_aer.__version__}")
    print(f"a={args.a}  n_count={args.n_count}  shots={args.shots}  seed={args.seed}\n")

    t0 = time.time()

    # Sanity: noiseless N=15 factoring should succeed with prob ~0.5 (since
    # a=7 has order r=4 mod 15, and only 2 of the 4 useful phases give
    # non-trivial factors after continued fractions).
    print("--- Cai QFT-noise sweep ---")
    eps_list = [0.0, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]
    cai = run_cai_noise_sweep(args.a, args.n_count, args.shots, eps_list,
                              args.seed, outdir)

    print("\n--- Depolarizing noise sweep ---")
    p_list = [0.0, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 5e-2]
    dep = run_depolarizing_sweep(args.a, args.n_count, args.shots, p_list,
                                 args.seed, outdir)

    print("\n--- Gate-count extrapolation ---")
    ex = gate_count_extrapolation(outdir)
    for row in ex["table"]:
        print(f"  n_bits={row['N_bits']:5d}  n_count={row['n_count']:5d}  "
              f"# ctrl-R_k = {row['num_ctrl_Rk_in_qft']:>10d}  "
              f"eps_thresh~{row['cai_eps_threshold_scaling']:.4f}")

    dt = time.time() - t0
    print(f"\nAll runs done in {dt:.1f}s")

    summary = {
        "elapsed_seconds": dt,
        "cai_last_point": cai["results"][-1],
        "cai_baseline": cai["results"][0],
        "dep_last_point": dep["results"][-1],
        "dep_baseline": dep["results"][0],
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("Summary written.")


if __name__ == "__main__":
    sys.exit(main() or 0)
