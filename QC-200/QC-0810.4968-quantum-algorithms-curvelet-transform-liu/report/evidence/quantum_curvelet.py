"""Quantum curvelet transform on Qiskit statevector, compared to classical baseline.

We implement the quantum curvelet transform of Liu (arXiv:0810.4968) eq. (15):

    sum_x f(x) |x> |0,0>   -->   sum_{a,b,theta} Gamma f(a,b,theta) |b> |a,theta>

using the three-step recipe from Sec 6.2:

    Q = (IQFT_b tensor I_{a,theta})  *  X  *  (QFT_x tensor I_{a,theta})

where X is the "sector-tagging" isometry that maps
    |k>|0,0>  -->  |k> * sum_{a,theta} chi_{a,theta}(k) |a,theta>.

For Liu's Case (1) (indicator windows on disjoint sets), each frequency bin k lies
in exactly ONE sector j(k), so X acts as a permutation:
    X|k>|0>  =  |k>|j(k)>.
This is efficiently implementable as a controlled-index write (classical function
compiled into a quantum gate) — the quantum version of a lookup table.

We test on 1D signals with N=8, 16, 32 (n=3, 4, 5 qubits) and confirm that the
quantum output amplitudes exactly match the classical curvelet transform.
"""
from __future__ import annotations

import json
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector, Operator

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classical_curvelet import dyadic_windows_1d, curvelet_1d


def build_quantum_curvelet_1d(N: int, chi: np.ndarray) -> QuantumCircuit:
    """Return a QuantumCircuit that computes the 1D quantum curvelet transform.

    Registers:
        pos   : n qubits, index x in {0,...,N-1}  (also serves as b after inverse QFT)
        sec   : ceil(log2 S) qubits, sector index j in {0,...,S-1}
    Input:   |x>|0>
    Output:  |b>|j>   with amplitude  Gamma f(j, b) * (phase convention as in classical)
    """
    n = int(np.log2(N))
    assert 2 ** n == N, "N must be power of 2"
    S = chi.shape[0]
    m = int(np.ceil(np.log2(S)))
    # sector assignment: since chi is hard-partition (0/1), each k has exactly one j
    assign = np.argmax(chi, axis=0)   # shape (N,) -> sector index in [0,S)
    # sanity: chi[assign[k], k] must be 1 for each k
    for k in range(N):
        assert chi[assign[k], k] == 1.0, f"chi is not a hard partition at k={k}"

    pos = QuantumRegister(n, "pos")
    sec = QuantumRegister(m, "sec")
    qc = QuantumCircuit(pos, sec, name="Q_curvelet")

    # Step 1: QFT on pos register (x -> k).
    #   Qiskit's QFT uses the +i convention (|x> -> sum_k e^{+2*pi*i*k*x/N}|k>/sqrt(N))
    #   whereas numpy's fft (which our classical reference uses to compute fhat) uses
    #   the -i convention: fhat(k) = sum_x f(x) e^{-2*pi*i*k*x/N}.
    #   To match numpy's fft convention we therefore call INVERSE QFT here...
    qft = QFT(num_qubits=n, do_swaps=True, inverse=True, name="QFT_minus")
    qc.append(qft, pos)

    # Step 2: X operator -- write sector index into `sec` conditioned on k.
    # Implemented as a *permutation* on the joint |sec>|pos> basis: for each pos=x,
    # swap sec-values 0 <-> j(x). That is unitary by construction (it is its own inverse).
    # Basis-state ordering in Qiskit little-endian for [pos, sec] register list:
    # integer index i = sec_int * N + pos_int  (sec on the high bits).
    dim = 2 ** (n + m)
    perm = np.arange(dim)
    for x in range(N):
        j = int(assign[x])
        if j == 0:
            continue
        i_zero = 0 * N + x
        i_j    = j * N + x
        perm[i_zero], perm[i_j] = perm[i_j], perm[i_zero]
    U = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        U[perm[col], col] = 1.0
    # Verify unitary and correct action on |sec=0>|pos=x>
    assert np.allclose(U.conj().T @ U, np.eye(dim), atol=1e-10), "X op not unitary"
    for x in range(N):
        j = int(assign[x])
        # U applied to |sec=0,pos=x> should give |sec=j,pos=x>
        col = 0 * N + x
        expected_row = j * N + x
        assert U[expected_row, col] == 1.0
    Xop = Operator(U)
    qc.append(Xop, list(pos) + list(sec))

    # Step 3: inverse QFT on pos (k -> b) -- with our flipped convention above, this is
    #   the *forward* Qiskit QFT (which is the +i convention == numpy ifft):
    iqft = QFT(num_qubits=n, do_swaps=True, inverse=False, name="IQFT_plus")
    qc.append(iqft, pos)

    return qc


def run_quantum_curvelet_1d(f: np.ndarray, chi: np.ndarray) -> np.ndarray:
    """Return the joint (S,N) statevector-amplitude table produced by the circuit."""
    N = f.shape[0]
    n = int(np.log2(N))
    S = chi.shape[0]
    m = int(np.ceil(np.log2(S)))

    # Prepare |psi_in> = sum_x f(x) |x>|0>.
    #   In Qiskit little-endian ordering: index = sec*N + pos.
    dim = 2 ** (n + m)
    psi_in = np.zeros(dim, dtype=complex)
    norm = np.linalg.norm(f)
    if norm == 0:
        raise ValueError("f is zero")
    for x in range(N):
        psi_in[x] = f[x] / norm            # sec=0, pos=x
    sv_in = Statevector(psi_in)

    qc = build_quantum_curvelet_1d(N, chi)
    sv_out = sv_in.evolve(qc)
    arr = sv_out.data.reshape(2 ** m, N)   # rows = sec (j), cols = pos (b)
    # take only the S physical sectors
    arr = arr[:S, :]
    # renormalise back to original scale
    arr *= norm
    return arr


def compare(N: int, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    f = rng.standard_normal(N) + 1j * rng.standard_normal(N)
    chi = dyadic_windows_1d(N)
    gamma_classical = curvelet_1d(f, chi)
    gamma_quantum = run_quantum_curvelet_1d(f, chi)
    diff = gamma_classical - gamma_quantum
    max_abs = float(np.max(np.abs(diff)))
    frob = float(np.linalg.norm(diff))
    # also: does the quantum output preserve norm?
    return {
        "N": N,
        "n_qubits_pos": int(np.log2(N)),
        "num_sectors": int(chi.shape[0]),
        "input_norm_sq": float(np.sum(np.abs(f) ** 2)),
        "quantum_output_norm_sq": float(np.sum(np.abs(gamma_quantum) ** 2)),
        "classical_output_norm_sq": float(np.sum(np.abs(gamma_classical) ** 2)),
        "max_abs_amplitude_diff_classical_vs_quantum": max_abs,
        "frobenius_diff": frob,
    }


if __name__ == "__main__":
    results = {}
    for N in (8, 16, 32):
        results[f"N{N}"] = compare(N)
    print(json.dumps(results, indent=2))
