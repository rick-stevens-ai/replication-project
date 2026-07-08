#!/usr/bin/env python3
"""
Independent replication for arXiv:2005.02421 (Barak-Chou-Gao 2020),
"Spoofing Linear Cross-Entropy Benchmarking in Shallow Quantum Circuits".

Reproducible core we test (per the wave-brief):
  (a) F_XEB ~ 1 when sampling exactly from the circuit distribution q_C
      (For Haar-random circuits, ideal sampling gives E[F_XEB]=1.)
  (b) F_XEB ~ 0 when sampling from the uniform distribution
      (E_uniform[2^n q_C(x)-1] = 2^n * 2^-n - 1 = 0 for a normalized q_C, up to O(1/sqrt(N)).)
  (c) Shallow-depth spoofing insight: at very shallow depth d=1
      (a single layer of 2-qubit gates on disjoint pairs) each qubit is in a
      light cone of just L=2 input bits. A tiny classical strategy that outputs
      the max-probability bitstring of each 2-qubit block *independently*
      gets non-trivial (>>0) F_XEB, illustrating the paper's core theorem
      that light-cone-L circuits are spoofable in time 2^L.

Setup:
  - n = 4..8 qubits (statevector fully enumerable)
  - depth d in {1,2,3,4,5,6}
  - Haar-random 2-qubit gates on a 1D brick-wall pattern (aligned with the
    paper's 1D shallow-circuit setting).
  - We use cirq statevector simulation (exact) to get q_C, then draw samples
    from q_C to compute the "exact-sampling" F_XEB estimator.

Definitions:
  F_C(p) = sum_x p(x) * (2^n * q_C(x) - 1)
  Estimator from N samples x_1..x_N ~ p:
      F_hat = (1/N) sum_i (2^n * q_C(x_i) - 1)
  Exact-p sampler (p = q_C) has expectation:
      E[F_hat] = sum_x q_C(x) * (2^n q_C(x) - 1) = 2^n * ||q_C||_2^2 - 1
      For Haar-random circuits ||q_C||_2^2 concentrates near 2/(2^n+1) so
      E[F_hat] -> 1.
  Uniform sampler (p = uniform) has expectation:
      E[F_hat] = (1/2^n) sum_x (2^n q_C(x) - 1) = 1 - 1 = 0.

Spoofer for depth-1 disjoint-pair brick-wall:
  If gates act on qubits (0,1),(2,3),... independently, then
      q_C(x) = prod_k q_k(x_{2k}, x_{2k+1})
  where q_k is the marginal on that pair. The output of the pair with the
  *highest* q_k probability, concatenated, gives a bitstring x* with
  q_C(x*) = prod_k max_v q_k(v). Since max_v q_k(v) >= 1/4 (uniform) but
  typically ~0.4-0.5 for a random 2-qubit unitary, this deterministic
  spoofer achieves F_XEB = 2^n * prod_k max q_k - 1 >> 0.

At depth d=2 (one brick + one shifted brick) light cones start overlapping,
so the per-pair independence breaks but light-cone size is still small (L=4);
a mild spoofer using 4-bit local marginals should still elevate F above 0.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import List, Tuple

import numpy as np
import cirq


# ------------------------- circuit generators -----------------------------

def haar_random_two_qubit_unitary(rng: np.random.Generator) -> np.ndarray:
    """Sample a Haar-random 4x4 unitary."""
    # Standard trick: QR of complex Gaussian.
    z = (rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))) / np.sqrt(2.0)
    q, r = np.linalg.qr(z)
    # Fix phases so Q is Haar (Mezzadri 2007).
    d = np.diagonal(r)
    ph = d / np.abs(d)
    q = q * ph  # multiply columns
    return q


def brickwall_1d_circuit(
    n_qubits: int, depth: int, rng: np.random.Generator
) -> cirq.Circuit:
    """
    Build a 1D brick-wall random circuit:
      layer t=0: gates on pairs (0,1),(2,3),...
      layer t=1: gates on pairs (1,2),(3,4),...
      alternating. Each 2-qubit gate is a fresh Haar-random unitary.
    """
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    for layer in range(depth):
        offset = layer % 2
        moment_ops = []
        i = offset
        while i + 1 < n_qubits:
            U = haar_random_two_qubit_unitary(rng)
            gate = cirq.MatrixGate(U, name=f"U_{layer}_{i}")
            moment_ops.append(gate.on(qubits[i], qubits[i + 1]))
            i += 2
        if moment_ops:
            circuit.append(cirq.Moment(moment_ops))
    return circuit


def probabilities(circuit: cirq.Circuit, n_qubits: int) -> np.ndarray:
    """Return q_C over all 2^n bitstrings (indexed by big-endian int)."""
    sim = cirq.Simulator(dtype=np.complex128)
    result = sim.simulate(circuit)
    psi = np.asarray(result.final_state_vector)
    p = (psi.conj() * psi).real
    # Numerical clip.
    p = np.clip(p, 0.0, None)
    p /= p.sum()
    return p


# ------------------------- XEB estimators ---------------------------------

def xeb_fidelity_from_samples(q: np.ndarray, samples: np.ndarray) -> float:
    """F_hat = mean_i ( 2^n * q(x_i) - 1 )."""
    n_states = q.shape[0]
    return float(np.mean(n_states * q[samples] - 1.0))


def sample_from_distribution(
    p: np.ndarray, n_samples: int, rng: np.random.Generator
) -> np.ndarray:
    return rng.choice(p.shape[0], size=n_samples, p=p)


# --------------------- shallow-depth spoofer ------------------------------

def spoofer_depth1_bitstring(
    circuit: cirq.Circuit, n_qubits: int
) -> Tuple[int, float]:
    """
    For a depth-1 brick-wall (disjoint pairs), compute per-pair marginals and
    return (best bitstring index, its q_C probability).

    This uses statevector simulation to get the exact pair marginals and
    picks the max-marginal outcome per pair. This is essentially the L=2
    light-cone spoofing algorithm from the paper (in its simplest form),
    used *deterministically* to output the mode of each independent block.
    """
    # For depth-1 brick-wall the circuit factorizes across pairs (0,1),(2,3),...
    # So q_C(x) = prod_k q_k(x_2k, x_2k+1). We compute q via full statevector
    # (cheap for n<=8) and then compute exact pair marginals by summing.
    p_full = probabilities(circuit, n_qubits)
    # p_full is length 2^n, index big-endian: bit for qubit 0 is MSB.
    n_states = p_full.shape[0]
    # Build bit array for each index once.
    idx = np.arange(n_states)
    bits = ((idx[:, None] >> (n_qubits - 1 - np.arange(n_qubits))[None, :]) & 1)
    best_bits = np.zeros(n_qubits, dtype=int)
    for k in range(0, n_qubits - 1, 2):
        q_pair = np.zeros(4)
        for v in range(4):
            b0 = (v >> 1) & 1
            b1 = v & 1
            mask = (bits[:, k] == b0) & (bits[:, k + 1] == b1)
            q_pair[v] = p_full[mask].sum()
        v_star = int(np.argmax(q_pair))
        best_bits[k] = (v_star >> 1) & 1
        best_bits[k + 1] = v_star & 1
    # If n is odd, the last qubit was untouched in a depth-1 brick-wall
    # (gate acts only on (0,1),(2,3),...). Just pick 0.
    x_star = 0
    for j, b in enumerate(best_bits):
        x_star = (x_star << 1) | int(b)
    return x_star, float(p_full[x_star])


def spoofer_depth2_lightcone(
    circuit: cirq.Circuit, n_qubits: int, block: int = 4, rng: np.random.Generator = None
) -> np.ndarray:
    """
    Depth-2 (and general shallow) spoofer: partition the qubits into
    consecutive blocks of `block` qubits, exactly-sample from the marginal
    q_C restricted to that block (integrating out the rest), and stitch.
    For depth 2 with block=4 covering the whole light cone, this recovers
    the light-cone spoofing idea: each block draws from its own marginal
    which is more concentrated than uniform, giving F_XEB > 0.

    Returns one sampled bitstring index.
    """
    if rng is None:
        rng = np.random.default_rng()
    p_full = probabilities(circuit, n_qubits)
    n_states = p_full.shape[0]
    idx = np.arange(n_states)
    bits = ((idx[:, None] >> (n_qubits - 1 - np.arange(n_qubits))[None, :]) & 1)
    sampled_bits = np.zeros(n_qubits, dtype=int)
    for start in range(0, n_qubits, block):
        end = min(start + block, n_qubits)
        width = end - start
        marg = np.zeros(1 << width)
        # sum p_full over all configurations of the block
        for v in range(1 << width):
            m = np.ones(n_states, dtype=bool)
            for j in range(width):
                b = (v >> (width - 1 - j)) & 1
                m &= (bits[:, start + j] == b)
            marg[v] = p_full[m].sum()
        # normalize (defensive) then sample
        marg = np.clip(marg, 0.0, None)
        marg /= marg.sum()
        v_samp = int(rng.choice(1 << width, p=marg))
        for j in range(width):
            sampled_bits[start + j] = (v_samp >> (width - 1 - j)) & 1
    x = 0
    for b in sampled_bits:
        x = (x << 1) | int(b)
    return x


# --------------------- main experiment driver -----------------------------

@dataclass
class RunResult:
    experiment: str
    n_qubits: int
    depth: int
    n_circuits: int
    n_samples: int
    F_mean: float
    F_std: float
    F_per_circuit: List[float]


def experiment_exact_and_uniform(
    n_qubits: int,
    depths: List[int],
    n_circuits: int,
    n_samples: int,
    seed: int = 20260703,
) -> List[RunResult]:
    """(a) exact-sampling F_XEB, (b) uniform-sampling F_XEB across depths."""
    rng = np.random.default_rng(seed)
    out: List[RunResult] = []
    for d in depths:
        F_exact = []
        F_unif = []
        for c in range(n_circuits):
            circ = brickwall_1d_circuit(n_qubits, d, rng)
            q = probabilities(circ, n_qubits)
            # exact sampling from q
            samples_q = sample_from_distribution(q, n_samples, rng)
            F_exact.append(xeb_fidelity_from_samples(q, samples_q))
            # uniform sampling
            samples_u = rng.integers(0, 1 << n_qubits, size=n_samples)
            F_unif.append(xeb_fidelity_from_samples(q, samples_u))
        out.append(RunResult(
            experiment="exact_sampling",
            n_qubits=n_qubits, depth=d,
            n_circuits=n_circuits, n_samples=n_samples,
            F_mean=float(np.mean(F_exact)),
            F_std=float(np.std(F_exact)),
            F_per_circuit=[float(x) for x in F_exact],
        ))
        out.append(RunResult(
            experiment="uniform_sampling",
            n_qubits=n_qubits, depth=d,
            n_circuits=n_circuits, n_samples=n_samples,
            F_mean=float(np.mean(F_unif)),
            F_std=float(np.std(F_unif)),
            F_per_circuit=[float(x) for x in F_unif],
        ))
    return out


def experiment_shallow_spoofer(
    n_qubits: int,
    n_circuits: int,
    n_samples: int,
    seed: int = 20260703,
) -> List[RunResult]:
    """
    (c) shallow-depth spoofer:
      - depth=1: deterministic best-bitstring per disjoint pair (repeated
        n_samples times, since output is a single string per circuit)
      - depth=2: light-cone block sampler with block=4
      - depth=3: same light-cone spoofer but with block=4 (light cone grows
        beyond block, so spoofer weakens — good control)
      - depth=6: light-cone spoofer collapses to near-uniform (control)
    """
    rng = np.random.default_rng(seed + 7)
    results: List[RunResult] = []

    # ---------- depth 1 ----------
    F_d1 = []
    for c in range(n_circuits):
        circ = brickwall_1d_circuit(n_qubits, 1, rng)
        q = probabilities(circ, n_qubits)
        x_star, _ = spoofer_depth1_bitstring(circ, n_qubits)
        samples = np.full(n_samples, x_star, dtype=int)
        F_d1.append(xeb_fidelity_from_samples(q, samples))
    results.append(RunResult(
        experiment="spoofer_depth1_deterministic_best_bitstring",
        n_qubits=n_qubits, depth=1,
        n_circuits=n_circuits, n_samples=n_samples,
        F_mean=float(np.mean(F_d1)),
        F_std=float(np.std(F_d1)),
        F_per_circuit=[float(x) for x in F_d1],
    ))

    # ---------- depth 2,3,6: light-cone block spoofer, block=4 ----------
    for d in [2, 3, 6]:
        F_dk = []
        for c in range(n_circuits):
            circ = brickwall_1d_circuit(n_qubits, d, rng)
            q = probabilities(circ, n_qubits)
            samples = np.array(
                [spoofer_depth2_lightcone(circ, n_qubits, block=4, rng=rng)
                 for _ in range(n_samples)]
            )
            F_dk.append(xeb_fidelity_from_samples(q, samples))
        results.append(RunResult(
            experiment=f"spoofer_lightcone_block4_depth{d}",
            n_qubits=n_qubits, depth=d,
            n_circuits=n_circuits, n_samples=n_samples,
            F_mean=float(np.mean(F_dk)),
            F_std=float(np.std(F_dk)),
            F_per_circuit=[float(x) for x in F_dk],
        ))

    return results


def main() -> None:
    out_dir = os.path.expanduser(
        "~/Dropbox/REPLICATE-PROJECT/QC-100/"
        "QC-2005.02421-xeb-shallow-spoofing/report/evidence"
    )
    os.makedirs(out_dir, exist_ok=True)

    t0 = time.time()

    print("=" * 70)
    print("Experiment 1/2: exact-vs-uniform sampling F_XEB across depths")
    print("=" * 70)
    exp_ab = []
    for n in [4, 6, 8]:
        print(f"[n={n}]")
        rs = experiment_exact_and_uniform(
            n_qubits=n, depths=[1, 2, 3, 4, 6],
            n_circuits=20, n_samples=5000, seed=20260703 + n,
        )
        for r in rs:
            print(f"  n={r.n_qubits} d={r.depth:<2d} {r.experiment:<18s} "
                  f"F_mean={r.F_mean:+.4f} +/- {r.F_std:.4f}")
            exp_ab.append(asdict(r))

    print()
    print("=" * 70)
    print("Experiment 2/2: shallow-depth spoofer (paper's core insight)")
    print("=" * 70)
    exp_c = []
    for n in [6, 8]:
        print(f"[n={n}]")
        rs = experiment_shallow_spoofer(
            n_qubits=n, n_circuits=20, n_samples=1000, seed=20260703 + n,
        )
        for r in rs:
            print(f"  n={r.n_qubits} d={r.depth:<2d} {r.experiment:<50s} "
                  f"F_mean={r.F_mean:+.4f} +/- {r.F_std:.4f}")
            exp_c.append(asdict(r))

    dt = time.time() - t0
    print(f"\nTotal runtime: {dt:.1f} s")

    summary = {
        "paper": "arXiv:2005.02421 (Barak-Chou-Gao 2020)",
        "framework": {
            "tool": "cirq",
            "cirq_version": cirq.__version__,
            "numpy_version": np.__version__,
        },
        "experiment_a_b_exact_vs_uniform": exp_ab,
        "experiment_c_shallow_spoofer": exp_c,
        "runtime_seconds": dt,
    }
    with open(os.path.join(out_dir, "xeb_results.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {os.path.join(out_dir, 'xeb_results.json')}")


if __name__ == "__main__":
    main()
