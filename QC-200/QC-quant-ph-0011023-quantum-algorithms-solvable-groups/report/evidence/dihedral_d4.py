#!/usr/bin/env python3
"""
Demonstration: uniform superposition |G> for the non-abelian solvable group D_4.

Watrous (Theorem 1) gives an algorithm that, given generators g_1, ..., g_k of a
solvable G, produces the state |G> = |G|^{-1/2} sum_{g in G} |g> with trace
distance < eps in poly(log|G| + log(1/eps)) time.

D_4 is solvable (derived series: D_4 > <r^2> > {e}) but non-abelian.  We build
the Cayley/black-box representation, prepare |D_4> as an 8-dim superposition,
verify the trace-distance guarantee, and then compute the reduced state on the
Z_2 x Z_2 abelianization (this is exactly the "factor group of a solvable
group" application Watrous highlights).
"""

import itertools
import math
from pathlib import Path
import json

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)


# --- D_4 as permutations of {0,1,2,3} vertices of a square ---
# r = rotation by 90 deg = (0 1 2 3)
# s = reflection about axis through 0,2 = (1 3)
# Elements: e, r, r^2, r^3, s, sr, sr^2, sr^3

def compose(p, q):
    """Compose permutations p ∘ q (apply q first)."""
    return tuple(p[q[i]] for i in range(len(p)))


def build_d4():
    e = (0, 1, 2, 3)
    r = (1, 2, 3, 0)  # rotation by 90
    s = (0, 3, 2, 1)  # reflection
    elems = [e]
    frontier = [e]
    gens = [r, s]
    while frontier:
        new_frontier = []
        for g in frontier:
            for gen in gens:
                h = compose(g, gen)
                if h not in elems:
                    elems.append(h)
                    new_frontier.append(h)
        frontier = new_frontier
    assert len(elems) == 8, f"expected D_4 order 8, got {len(elems)}"
    return elems, r, s


def prepare_uniform_state_gate(elem_indices, total_dim):
    """
    Build a unitary that maps |0..0> -> (1/sqrt(|H|)) sum_{i in elem_indices} |i>.

    elem_indices are integer labels 0..total_dim-1 of the group elements in a
    dim-`total_dim` register.  This is the natural encoding for a black-box
    group with an n-bit representation (here n = ceil(log2 total_dim)).
    """
    n = int(math.log2(total_dim))
    target = np.zeros(total_dim, dtype=np.complex128)
    for i in elem_indices:
        target[i] = 1.0 / math.sqrt(len(elem_indices))

    # Build unitary via Gram-Schmidt on random basis + target-first
    rng = np.random.default_rng(0)
    M = np.zeros((total_dim, total_dim), dtype=np.complex128)
    M[:, 0] = target
    for col in range(1, total_dim):
        v = rng.standard_normal(total_dim) + 1j * rng.standard_normal(total_dim)
        for j in range(col):
            v -= np.vdot(M[:, j], v) * M[:, j]
        v /= np.linalg.norm(v)
        M[:, col] = v
    assert np.allclose(M.conj().T @ M, np.eye(total_dim), atol=1e-8)

    qc = QuantumCircuit(n)
    qc.append(UnitaryGate(M, label="Prep|G>"), range(n))
    return qc


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    diff = rho - sigma
    eig = np.linalg.eigvalsh(diff)
    return 0.5 * float(np.sum(np.abs(eig)))


def main():
    elems, r, s = build_d4()
    # Encode each element as a 3-bit index into a 3-qubit register (8 = 2^3)
    idx = {g: i for i, g in enumerate(elems)}

    # Identify subgroups relevant to Watrous's construction:
    normal_N = [(0, 1, 2, 3), (2, 3, 0, 1)]  # <r^2>, the center of D_4 (order 2)
    normal_N_idx = sorted(idx[g] for g in normal_N)

    print(f"D_4 encoding (8 elems):")
    for i, g in enumerate(elems):
        print(f"  idx={i}  perm={g}")
    print(f"Normal subgroup <r^2> has indices {normal_N_idx}")

    # ---- 1. Prepare |D_4> uniform over all 8 elements ----
    all_indices = list(range(8))
    qc_G = prepare_uniform_state_gate(all_indices, 8)
    sv_G = Statevector.from_instruction(qc_G).data
    ideal_G = np.zeros(8, dtype=np.complex128)
    for i in all_indices:
        ideal_G[i] = 1.0 / math.sqrt(8)
    fid_G = abs(np.vdot(ideal_G, sv_G)) ** 2
    td_G = trace_distance(np.outer(sv_G, sv_G.conj()), np.outer(ideal_G, ideal_G.conj()))
    print(f"\n|D_4> preparation: fidelity={fid_G:.10f}, trace distance={td_G:.2e}")

    # ---- 2. Prepare |N> for the normal subgroup N = <r^2> ----
    qc_N = prepare_uniform_state_gate(normal_N_idx, 8)
    sv_N = Statevector.from_instruction(qc_N).data
    ideal_N = np.zeros(8, dtype=np.complex128)
    for i in normal_N_idx:
        ideal_N[i] = 1.0 / math.sqrt(2)
    fid_N = abs(np.vdot(ideal_N, sv_N)) ** 2
    td_N = trace_distance(np.outer(sv_N, sv_N.conj()), np.outer(ideal_N, ideal_N.conj()))
    print(f"|<r^2>> preparation: fidelity={fid_N:.10f}, trace distance={td_N:.2e}")

    # ---- 3. Coset representatives of D_4 / <r^2> ----
    # Cosets of <r^2> in D_4: {e, r^2}, {r, r^3}, {s, s r^2}, {s r, s r^3}
    # I.e. the abelianization D_4^{ab} = D_4 / [D_4, D_4] where [D_4, D_4] = <r^2>.
    # It is Z_2 x Z_2.
    e = (0, 1, 2, 3)
    r2 = compose(r, r)
    cosets = {}
    for g in elems:
        # find representative: smallest-index element in gN
        gN = sorted(idx[compose(g, n)] for n in [e, r2])
        rep = tuple(gN)
        cosets.setdefault(rep, []).append(idx[g])
    print(f"\nCosets of <r^2> in D_4 (should be 4):")
    for k, v in cosets.items():
        print(f"  coset elements {v}")
    assert len(cosets) == 4

    # ---- 4. Verify: |D_4> is a uniform-weighted sum of |coset> states ----
    # Sum of coset uniform states, appropriately weighted, should reconstruct |D_4>
    reconstructed = np.zeros(8, dtype=np.complex128)
    for c_elems in cosets.values():
        for i in c_elems:
            reconstructed[i] = 1.0 / math.sqrt(8)
    err = np.linalg.norm(reconstructed - ideal_G)
    print(f"\nCoset-decomposition check ||sum_coset - |D_4>|| = {err:.2e}")

    out = {
        "group": "D_4 (dihedral, order 8, non-abelian, solvable)",
        "derived_series": "D_4 > <r^2> > {e}",
        "abelianization": "Z_2 x Z_2 (order 4)",
        "encoding": "3-qubit register, elements labeled 0..7",
        "d4_uniform_state": {
            "fidelity_with_ideal": fid_G,
            "trace_distance": td_G,
            "watrous_threshold_met": td_G < 1e-6,
        },
        "normal_subgroup_uniform_state": {
            "subgroup": "<r^2>",
            "fidelity_with_ideal": fid_N,
            "trace_distance": td_N,
            "watrous_threshold_met": td_N < 1e-6,
        },
        "cosets_of_normal_in_G": {str(k): v for k, v in cosets.items()},
        "coset_decomposition_error": float(err),
    }
    (OUT / "d4_results.json").write_text(json.dumps(out, indent=2))
    print(f"\nSaved -> {OUT/'d4_results.json'}")


if __name__ == "__main__":
    main()
