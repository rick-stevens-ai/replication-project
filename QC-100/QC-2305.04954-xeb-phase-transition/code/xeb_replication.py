#!/usr/bin/env python3
"""
Replication of central claim from Ware, Deshpande, Hangleiter, Niroula, Fefferman, Gorshkov, Gullans
"A sharp phase transition in linear cross-entropy benchmarking" (arXiv:2305.04954, 2023).

Central testable claim (Fig. 2, Sec. III):
  In noisy random Haar circuits with 2-qubit gates + per-qubit depolarizing noise strength eps,
  the linear XEB decay rate matches the fidelity decay rate (1-eps)^{Nd} when eps*N < c
  (with c = ln(5/2) ~ 0.916 for Haar 2-qubit gates), and saturates at
  Delta{ln chi} ~ -0.92 per layer for eps*N >> c.

This script performs an EXACT statevector simulation (Cirq) of shallow random
1D brickwork Haar-random circuits at multiple noise rates and multiple N in {4,6,8,10}
at fixed depth. It computes:
  - fidelity F = <psi_ideal | rho_noisy | psi_ideal>
  - linear XEB score chi = 2^N * sum_x p_ideal(x)*p_noisy(x) - 1
averaged over K random circuit instances.

We reproduce the shape of F and chi vs eps and check:
  * At low eps*N, chi tracks F (both close to (1-eps)^{Nd}).
  * At higher eps, chi curves flatten (transition tail visible even at small N).
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import cirq

RNG_SEED = 12345
OUT_DIR = Path(__file__).resolve().parent.parent / "results"
OUT_DIR.mkdir(exist_ok=True)


def random_two_qubit_haar_unitary(rng):
    """Draw a Haar-random 4x4 unitary via QR of complex Ginibre matrix."""
    z = (rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))) / np.sqrt(2.0)
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    ph = d / np.abs(d)
    return q * ph


def build_brickwork_circuit(n_qubits, depth, rng):
    """1D brickwork of random Haar 2-qubit gates."""
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    for layer in range(depth):
        offset = layer % 2
        ops = []
        i = offset
        while i + 1 < n_qubits:
            U = random_two_qubit_haar_unitary(rng)
            gate = cirq.MatrixGate(U)
            ops.append(gate.on(qubits[i], qubits[i + 1]))
            i += 2
        if ops:
            circuit.append(ops, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    return circuit, qubits


def ideal_final_state(circuit, qubits):
    sim = cirq.Simulator(seed=0)
    result = sim.simulate(circuit, qubit_order=qubits)
    return result.final_state_vector


def apply_single_qubit_depolarizing_layer(rho, eps, n_qubits):
    """Apply single-qubit depolarizing channel with parameter eps to every qubit.

    Depolarizing (parameter eps): rho -> (1-eps)*rho + eps*I/2 (on that qubit).
    Vectorized: reshape rho into 2^N x 2^N as (a_ket, a_bra), then reshape into a rank-2N tensor
    with ket qubits and bra qubits separately; for each qubit q we compute
    rho -> (1-eps)*rho + eps * (I_q x Tr_q rho) / 2.
    """
    if eps == 0.0:
        return rho
    dim = 2 ** n_qubits
    for q in range(n_qubits):
        left = 2 ** q
        right = 2 ** (n_qubits - q - 1)
        # Reshape to (left, 2, right, left, 2, right)
        rho_r = rho.reshape(left, 2, right, left, 2, right)
        # Partial trace over qubit q: sum diag of the (2,2) block
        rho_traced = rho_r[:, 0, :, :, 0, :] + rho_r[:, 1, :, :, 1, :]
        # Build I/2 tensor rho_traced (on qubit q), reshaped back
        # (I_q x rho_rest)[i s j, i' s' j'] = delta_{s s'} * rho_rest[i j, i' j']
        mixed = np.zeros_like(rho_r)
        mixed[:, 0, :, :, 0, :] = 0.5 * rho_traced
        mixed[:, 1, :, :, 1, :] = 0.5 * rho_traced
        rho = ((1.0 - eps) * rho_r + eps * mixed).reshape(dim, dim)
    return rho


def simulate_noisy_density_layered(circuit, qubits, eps):
    """Simulate circuit as pure evolution + noise after each moment, in density-matrix picture."""
    n = len(qubits)
    dim = 2 ** n
    psi0 = np.zeros(dim, dtype=complex)
    psi0[0] = 1.0
    rho = np.outer(psi0, psi0.conj())
    for moment in circuit:
        sub = cirq.Circuit(moment)
        U = sub.unitary(qubit_order=qubits)
        rho = U @ rho @ U.conj().T
        if eps > 0.0:
            rho = apply_single_qubit_depolarizing_layer(rho, eps, n)
    return rho


def linear_xeb(p_ideal, p_noisy, n_qubits):
    return (2 ** n_qubits) * float(np.sum(p_ideal * p_noisy)) - 1.0


def run_sweep(n_qubits, depth, eps_values, n_circuits, rng_seed):
    rng = np.random.default_rng(rng_seed)
    records = []
    for eps in eps_values:
        fidels = []
        xebs = []
        t0 = time.time()
        for k in range(n_circuits):
            circuit, qubits = build_brickwork_circuit(n_qubits, depth, rng)
            psi_ideal = ideal_final_state(circuit, qubits)
            p_ideal = np.abs(psi_ideal) ** 2
            rho_noisy = simulate_noisy_density_layered(circuit, qubits, eps)
            F = float(np.real(np.vdot(psi_ideal, rho_noisy @ psi_ideal)))
            p_noisy = np.clip(np.real(np.diag(rho_noisy)), 0.0, None)
            chi = linear_xeb(p_ideal, p_noisy, n_qubits)
            fidels.append(F)
            xebs.append(chi)
        dt = time.time() - t0
        record = {
            "n": n_qubits,
            "d": depth,
            "eps": float(eps),
            "epsN": float(eps * n_qubits),
            "n_circuits": n_circuits,
            "F_mean": float(np.mean(fidels)),
            "F_std": float(np.std(fidels)),
            "chi_mean": float(np.mean(xebs)),
            "chi_std": float(np.std(xebs)),
            "F_gwn_pred": float((1.0 - eps) ** (n_qubits * depth)),
            "wall_s": dt,
        }
        records.append(record)
        print(f"  n={n_qubits} d={depth} eps={eps:.3f} epsN={eps*n_qubits:.3f} "
              f"F={record['F_mean']:.4f} chi={record['chi_mean']:.4f} "
              f"gwn=(1-eps)^Nd={record['F_gwn_pred']:.4f}  ({dt:.1f}s)", flush=True)
    return records


def main():
    t0 = time.time()
    depth = 8
    all_records = []
    # eps values: span epsN from 0 to ~1.6 so we cross the theoretical threshold epsN=ln(5/2)~0.916
    for n, n_circuits in [(4, 40), (6, 30), (8, 20), (10, 10)]:
        eps_max = min(0.30, 1.6 / n)
        eps_values = np.linspace(0.0, eps_max, 11)
        print(f"\n=== n={n} d={depth} n_circuits={n_circuits} eps in [0, {eps_max:.3f}] ===", flush=True)
        recs = run_sweep(n, depth, eps_values, n_circuits, rng_seed=RNG_SEED + n)
        all_records.extend(recs)

    out_path = OUT_DIR / "xeb_sweep.json"
    with open(out_path, "w") as f:
        json.dump({"records": all_records,
                   "elapsed_s": time.time() - t0,
                   "notes": "linear XEB replication of Ware et al 2305.04954, brickwork 1D Haar, per-qubit depolarizing noise per layer"},
                  f, indent=2)
    print(f"\nSaved: {out_path}  ({time.time()-t0:.1f}s total)", flush=True)


if __name__ == "__main__":
    main()
