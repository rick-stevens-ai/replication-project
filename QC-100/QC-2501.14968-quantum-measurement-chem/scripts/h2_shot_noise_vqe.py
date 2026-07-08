"""
H2 shot-noise VQE energy estimate: with vs without QWC grouping.

Reproduces the paper's central operational claim (arXiv:2501.14968):
  For a fixed total shot budget, grouping Pauli terms into QWC (or FC) fragments
  reduces the variance of the H expectation-value estimator versus measuring
  each Pauli term individually.

We run REAL Qiskit sampling here — no fabricated numbers.
For each Pauli-string P_j:
  - Rotate the state so P_j -> Z...Z (Clifford rotation on qubits where P_j has X or Y)
  - Sample computational-basis measurements N times
  - Parity of the sampled bits on the P_j support gives an unbiased estimator of <P_j>
For a QWC group of Pauli strings that all share the same measurement basis per qubit:
  - Build ONE compatible measurement circuit for the whole group and re-use the shots.

We compare, over R independent noise-realizations:
  <H>_ungrouped  (each of 15 terms measured with M/15 shots)
  <H>_qwc        (each QWC group measured with M/K_qwc shots)
Estimator variance (over R runs) is the metric.
"""

from __future__ import annotations
import json
import time
import numpy as np
from pathlib import Path
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, SparsePauliOp, Pauli
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper


ART = Path(__file__).resolve().parents[1] / "artifacts"
ART.mkdir(parents=True, exist_ok=True)


def build_h2():
    driver = PySCFDriver(
        atom="H 0 0 0; H 0 0 0.735",
        basis="sto3g",
        charge=0, spin=0, unit=DistanceUnit.ANGSTROM,
    )
    prob = driver.run()
    H = JordanWignerMapper().map(prob.hamiltonian.second_q_op())
    return H, prob.nuclear_repulsion_energy


def qwc(a: str, b: str) -> bool:
    for x, y in zip(a, b):
        if x != "I" and y != "I" and x != y:
            return False
    return True


def group_qwc(labels):
    n = len(labels)
    incompat = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if not qwc(labels[i], labels[j]):
                incompat[i].add(j)
                incompat[j].add(i)
    order = sorted(range(n), key=lambda i: -len(incompat[i]))
    color_of = {}
    groups = []
    for v in order:
        used = {color_of[u] for u in incompat[v] if u in color_of}
        c = 0
        while c in used:
            c += 1
        color_of[v] = c
        while len(groups) <= c:
            groups.append([])
        groups[c].append(v)
    return groups


def group_meas_basis(group_labels):
    """For a QWC group, per qubit pick the non-I label (X/Y/Z), else I."""
    n_q = len(group_labels[0])
    basis = ["I"] * n_q
    for lab in group_labels:
        for q, ch in enumerate(lab):
            if ch != "I":
                if basis[q] == "I":
                    basis[q] = ch
                else:
                    assert basis[q] == ch, "Not QWC compatible!"
    return "".join(basis)


def sample_in_basis(psi_state: Statevector, basis: str, shots: int, rng):
    """Rotate psi according to basis (X->H, Y->Sdg then H, Z->identity) and sample.
    Note: Qiskit label ordering is LITTLE-ENDIAN in strings -> qubit 0 is the RIGHTMOST char.
    We follow the same convention (label[-1-q] refers to qubit q)."""
    n = len(basis)
    qc = QuantumCircuit(n)
    # basis[i] is character at index i; qubit index q corresponds to basis[n-1-q]
    for q in range(n):
        b = basis[n - 1 - q]
        if b == "X":
            qc.h(q)
        elif b == "Y":
            qc.sdg(q)
            qc.h(q)
        # I or Z: no rotation
    # Apply to state (compose the circuit unitary)
    rotated = psi_state.evolve(qc)
    probs = rotated.probabilities()  # length 2^n, index = bitstring as int
    # Sample
    idx = rng.choice(len(probs), size=shots, p=probs)
    return idx  # array of ints


def pauli_parity_from_samples(samples_int, pauli_label, n_qubits):
    """For each sampled bitstring, compute product of Z-eigenvalues on qubits
    where pauli_label is not I.
    pauli_label indexed s.t. label[n-1-q] refers to qubit q.
    A bit b_q => Z-eigenvalue (1 - 2*b_q)."""
    mask = 0
    for q in range(n_qubits):
        ch = pauli_label[n_qubits - 1 - q]
        if ch != "I":
            mask |= 1 << q
    if mask == 0:
        return np.ones_like(samples_int, dtype=float)  # identity Pauli
    # popcount of (samples & mask), parity
    masked = samples_int & mask
    # Compute bit popcount parity for each element
    parity = np.zeros_like(samples_int)
    v = masked.copy()
    while v.any():
        parity = parity ^ (v & 1)
        v >>= 1
    return 1.0 - 2.0 * parity  # +1 for even parity, -1 for odd


def build_reference_state():
    """Prepare H2/STO-3G exact GS on 4 qubits."""
    H, nre = build_h2()
    H_mat = H.to_matrix()
    e, V = np.linalg.eigh(H_mat)
    psi = V[:, 0]
    sv = Statevector(psi)
    return H, nre, sv, float(e[0]) + nre


def energy_estimate_ungrouped(H_labels, H_coeffs, sv, shots_per_term, rng):
    """Measure each term independently with `shots_per_term` shots.
    Returns estimator of <H> (qubit part, no NRE)."""
    n_q = len(H_labels[0])
    total = 0.0
    for lab, c in zip(H_labels, H_coeffs):
        # For non-identity terms, sample in the basis matching this single Pauli
        basis = ["I"] * n_q
        for q in range(n_q):
            ch = lab[n_q - 1 - q]
            if ch != "I":
                basis[n_q - 1 - q] = ch
        basis_str = "".join(basis)
        if all(b == "I" for b in basis):
            # Pure identity term: <I> = 1
            total += float(np.real(c))
            continue
        samples = sample_in_basis(sv, basis_str, shots_per_term, rng)
        p = pauli_parity_from_samples(samples, lab, n_q)
        total += float(np.real(c)) * float(np.mean(p))
    return total


def energy_estimate_grouped(H_labels, H_coeffs, sv, groups, shots_per_group, rng):
    n_q = len(H_labels[0])
    total = 0.0
    for grp in groups:
        grp_labels = [H_labels[j] for j in grp]
        # Identity-only group?
        if all(all(ch == "I" for ch in lab) for lab in grp_labels):
            for j in grp:
                total += float(np.real(H_coeffs[j]))
            continue
        basis_str = group_meas_basis(grp_labels)
        samples = sample_in_basis(sv, basis_str, shots_per_group, rng)
        for j in grp:
            lab = H_labels[j]
            if all(ch == "I" for ch in lab):
                total += float(np.real(H_coeffs[j]))
                continue
            p = pauli_parity_from_samples(samples, lab, n_q)
            total += float(np.real(H_coeffs[j])) * float(np.mean(p))
    return total


def main():
    t0 = time.time()
    H, nre, sv, E_ref = build_reference_state()
    labels = list(H.paulis.to_labels())
    coeffs = np.array(H.coeffs, dtype=complex)
    print(f"H2/STO-3G, {len(labels)} Pauli terms; exact ground-state energy = {E_ref:.6f} Ha")

    # Grouping
    groups = group_qwc(labels)
    K = len(groups)
    print(f"QWC groups = {K}  (terms/group = {len(labels)/K:.2f})")
    for idx, g in enumerate(groups):
        print(f"  group {idx}: {[labels[j] for j in g]}")

    # Shot budget experiment
    # Try a couple of total shot budgets; run R noise realizations each.
    rng = np.random.default_rng(20260703)
    R = 200

    results = {}
    for M_total in [1500, 15000, 150000]:
        shots_per_term = max(M_total // len(labels), 1)   # ungrouped: M/n_terms per term
        shots_per_group = max(M_total // K, 1)             # grouped:   M/K per group
        # But note: the ungrouped case actually spends n_terms * shots_per_term shots
        # and the grouped case spends K * shots_per_group shots -> same-ish budget.
        actual_M_ung = shots_per_term * len(labels)
        actual_M_grp = shots_per_group * K
        print(f"\n== Shot budget nominally {M_total} "
              f"(ungrouped actual {actual_M_ung}, grouped actual {actual_M_grp}) ==")

        E_ungrp = np.zeros(R)
        E_grp = np.zeros(R)
        for r in range(R):
            E_ungrp[r] = energy_estimate_ungrouped(labels, coeffs, sv, shots_per_term, rng) + nre
            E_grp[r] = energy_estimate_grouped(labels, coeffs, sv, groups, shots_per_group, rng) + nre

        print(f"  Ungrouped:  mean={E_ungrp.mean():+.5f}  std={E_ungrp.std(ddof=1):.5f}  "
              f"|mean-ref|={abs(E_ungrp.mean()-E_ref):.5f}")
        print(f"  QWC group:  mean={E_grp.mean():+.5f}  std={E_grp.std(ddof=1):.5f}  "
              f"|mean-ref|={abs(E_grp.mean()-E_ref):.5f}")
        variance_reduction = (E_ungrp.std(ddof=1) ** 2) / (E_grp.std(ddof=1) ** 2)
        print(f"  Variance ratio (ungrouped/grouped) = {variance_reduction:.2f}x")

        results[str(M_total)] = {
            "shots_per_term_ungrouped": int(shots_per_term),
            "shots_per_group_grouped": int(shots_per_group),
            "actual_shots_ungrouped": int(actual_M_ung),
            "actual_shots_grouped": int(actual_M_grp),
            "R_repeats": R,
            "E_ref_Ha": E_ref,
            "ungrouped": {
                "mean": float(E_ungrp.mean()),
                "std": float(E_ungrp.std(ddof=1)),
                "|bias|": float(abs(E_ungrp.mean() - E_ref)),
            },
            "qwc_grouped": {
                "mean": float(E_grp.mean()),
                "std": float(E_grp.std(ddof=1)),
                "|bias|": float(abs(E_grp.mean() - E_ref)),
            },
            "variance_ratio_ungrouped_over_grouped": float(variance_reduction),
        }

    out = {
        "paper": "arXiv:2501.14968",
        "molecule": "H2/STO-3G",
        "n_pauli_terms": len(labels),
        "n_qwc_groups": K,
        "qwc_groups_labels": [[labels[j] for j in g] for g in groups],
        "shot_budgets": results,
        "wall_seconds": time.time() - t0,
    }
    with open(ART / "h2_shot_noise_result.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nWrote {ART/'h2_shot_noise_result.json'}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
