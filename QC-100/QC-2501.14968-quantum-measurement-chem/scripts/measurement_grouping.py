"""
Independent replication of the core measurement-grouping methodology reviewed in
arXiv:2501.14968 (Patel, Jayakumar, Yen, Izmaylov 2025).

Central claim under test:
  Grouping Pauli terms in the electronic Hamiltonian into simultaneously
  measurable fragments (qubit-wise commuting = QWC, or fully commuting = FC)
  reduces the total number of shots required to estimate <H> to a given
  precision, compared to measuring every Pauli term individually.

The paper cites Crawford et al. (Ref. 17) as showing 2-4x reduction from greedy
grouping, and later combined methods 1-3 orders of magnitude on small molecules.

What this script does (real Qiskit + PySCF simulation, no fabrication):
  1. Build the H2/STO-3G electronic Hamiltonian via PySCF + Jordan-Wigner
     mapping (Qiskit Nature) -> list of (coeff, Pauli-string) terms.
  2. Solve for the exact ground state (numpy exact diagonalization of the
     4-qubit SparsePauliOp) => reference energy and |psi>.
  3. Compute per-Pauli-term variances Var(P_j) = <psi|P_j^2|psi> - <psi|P_j|psi>^2
     = 1 - <P_j>^2 for Pauli-string operators. Compute the "no-grouping"
     measurement cost M_ungrouped = ( sum_j |c_j| * sqrt(Var(P_j)) )^2 / eps^2
     (this is the paper's Eq. ~72-73 optimal-shot-allocation bound, aka
     the "individual measurement" baseline).
  4. Build the QWC compatibility graph over Pauli terms and color it (greedy
     largest-first) to obtain QWC fragments. For each fragment H_alpha, compute
     Var(H_alpha) w.r.t. |psi> (using the full 2^n density on 4 qubits, so
     covariances are exact). Compute M_qwc = ( sum_alpha sqrt(Var(H_alpha)) )^2 / eps^2.
  5. Also build the fully-commuting (FC) graph (Pauli-Pauli commutation, not
     just qubit-wise) and color it. This is the general commuting-clique version.
     Report shot count similarly.
  6. Print/save a JSON with:
       n_terms, n_qwc_groups, n_fc_groups,
       M_ungrouped, M_qwc, M_fc, reduction factors, energy check.

Small instance size (H2, 4 qubits) so it finishes in seconds on CPU.
"""

from __future__ import annotations
import json
import time
import numpy as np
from pathlib import Path

# ---- Qiskit Nature: build electronic Hamiltonian ---------------------------
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit.quantum_info import SparsePauliOp, Pauli, Statevector, Operator


OUT_DIR = Path(__file__).resolve().parents[1] / "artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build_h2_hamiltonian(bond_length: float = 0.735) -> SparsePauliOp:
    driver = PySCFDriver(
        atom=f"H 0 0 0; H 0 0 {bond_length}",
        basis="sto3g",
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    fermionic_op = problem.hamiltonian.second_q_op()
    mapper = JordanWignerMapper()
    qubit_op = mapper.map(fermionic_op)  # SparsePauliOp
    # Add nuclear repulsion so the energy matches chemistry ref
    nre = problem.nuclear_repulsion_energy
    return qubit_op, nre, problem


def pauli_labels_and_coeffs(op: SparsePauliOp):
    """Return list of (coeff_complex, label_str)."""
    return list(zip(op.coeffs, op.paulis.to_labels()))


def qubit_wise_commute(a: str, b: str) -> bool:
    """QWC: for every qubit position, either operator is I or both agree."""
    assert len(a) == len(b)
    for x, y in zip(a, b):
        if x == "I" or y == "I":
            continue
        if x != y:
            return False
    return True


def general_commute(a: str, b: str) -> bool:
    """Two Pauli strings commute iff # of positions where both non-I and differ is even."""
    assert len(a) == len(b)
    diff = 0
    for x, y in zip(a, b):
        if x == "I" or y == "I":
            continue
        if x != y:
            diff += 1
    return (diff % 2) == 0


def build_compat_graph(labels, commute_fn):
    """Return adjacency dict where edge = 'compatible' (can share a group).
    We color the COMPLEMENT graph to get cliques of pairwise-compatible terms:
    equivalently we color the incompatibility graph and each color = clique."""
    n = len(labels)
    incompat = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if not commute_fn(labels[i], labels[j]):
                incompat[i].add(j)
                incompat[j].add(i)
    return incompat


def greedy_color_lf(incompat: dict[int, set[int]]) -> list[list[int]]:
    """Greedy Largest-First coloring of the incompatibility graph.
    Each color class is a clique of pairwise-compatible Pauli terms => one group."""
    order = sorted(incompat.keys(), key=lambda i: -len(incompat[i]))
    color_of: dict[int, int] = {}
    groups: list[list[int]] = []
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


def build_pauli_matrix(label: str) -> np.ndarray:
    return Pauli(label).to_matrix()


def expval(psi: np.ndarray, M: np.ndarray) -> complex:
    return np.vdot(psi, M @ psi)


def variance(psi: np.ndarray, M: np.ndarray) -> float:
    ev = expval(psi, M)
    ev2 = expval(psi, M @ M)
    return float(np.real(ev2 - ev * ev))


def main():
    t0 = time.time()
    print("[1] Building H2/STO-3G Hamiltonian via PySCF + Jordan-Wigner ...")
    H, nre, problem = build_h2_hamiltonian(bond_length=0.735)
    n_qubits = H.num_qubits
    terms = pauli_labels_and_coeffs(H)
    print(f"    n_qubits={n_qubits}, n_pauli_terms={len(terms)}, "
          f"nuclear_repulsion={nre:.6f}")

    # Exact GS via dense diagonalization
    print("[2] Diagonalizing 2^n x 2^n Hamiltonian for reference energy ...")
    H_mat = H.to_matrix()  # 16x16
    e_qubit, V = np.linalg.eigh(H_mat)
    e_gs_qubit = float(e_qubit[0])
    e_gs_total = e_gs_qubit + nre
    psi = V[:, 0]
    # Reference literature value: H2 STO-3G FCI ~ -1.137270 Ha at R=0.735 Å
    print(f"    E_gs (qubit op) = {e_gs_qubit:.6f} Ha")
    print(f"    E_gs (total, incl. nuclear rep) = {e_gs_total:.6f} Ha")
    print(f"    Reference (literature, H2 STO-3G, R=0.735 Å) ~ -1.137270 Ha")

    # Precompute Pauli matrices for each term
    print("[3] Computing per-Pauli-term expectation values and variances ...")
    coeffs = np.array([c for c, _ in terms])
    labels = [l for _, l in terms]
    P_mats = [build_pauli_matrix(l) for l in labels]
    Pev = np.array([np.real(expval(psi, M)) for M in P_mats])
    Pvar = 1.0 - Pev * Pev  # for Pauli strings, P^2 = I, so Var = 1 - <P>^2
    # Sanity: reconstruct <H>
    E_reconstruct = float(np.real(np.sum(coeffs * Pev)))
    print(f"    sum_j c_j <P_j> = {E_reconstruct:.6f} Ha  (should match E_gs qubit)")

    # ---- No-grouping baseline shot count ----
    # Optimal shot allocation: M >= ( sum_j |c_j| sqrt(Var(P_j)) )^2 / eps^2
    abs_c = np.abs(coeffs).astype(float)
    sqrt_var = np.sqrt(np.maximum(Pvar, 0.0))
    S_ungrouped_coef = float(np.sum(abs_c * sqrt_var))  # divide by eps to get shots
    M_ungrouped_scale = S_ungrouped_coef ** 2  # eps^2 * M

    # ---- QWC grouping ----
    print("[4] Building QWC compatibility graph & greedy coloring ...")
    incompat_qwc = build_compat_graph(labels, qubit_wise_commute)
    qwc_groups = greedy_color_lf(incompat_qwc)
    print(f"    QWC: {len(labels)} terms -> {len(qwc_groups)} groups")

    # Per-group variance: build H_alpha = sum_{j in group} c_j P_j, compute Var
    def group_variance(group_idx):
        H_alpha = np.zeros_like(H_mat)
        for j in group_idx:
            H_alpha = H_alpha + coeffs[j] * P_mats[j]
        return variance(psi, H_alpha)

    qwc_vars = [group_variance(g) for g in qwc_groups]
    S_qwc_coef = float(np.sum([np.sqrt(max(v, 0.0)) for v in qwc_vars]))
    M_qwc_scale = S_qwc_coef ** 2

    # ---- Fully commuting (general commuting) grouping ----
    print("[5] Building FC (general commuting) graph & greedy coloring ...")
    incompat_fc = build_compat_graph(labels, general_commute)
    fc_groups = greedy_color_lf(incompat_fc)
    print(f"    FC:  {len(labels)} terms -> {len(fc_groups)} groups")

    fc_vars = [group_variance(g) for g in fc_groups]
    S_fc_coef = float(np.sum([np.sqrt(max(v, 0.0)) for v in fc_vars]))
    M_fc_scale = S_fc_coef ** 2

    # ---- Reduction factors ----
    red_qwc = M_ungrouped_scale / M_qwc_scale if M_qwc_scale > 0 else float("inf")
    red_fc = M_ungrouped_scale / M_fc_scale if M_fc_scale > 0 else float("inf")

    # ---- Concrete shot budget example: eps = 1 mHa = 1.6e-3 Ha (chemical accuracy) ----
    # Using eps for the standard-error requirement on <H>
    eps = 1.6e-3
    shots_ungrouped = M_ungrouped_scale / eps ** 2
    shots_qwc = M_qwc_scale / eps ** 2
    shots_fc = M_fc_scale / eps ** 2

    result = {
        "paper_arxiv": "2501.14968",
        "molecule": "H2",
        "basis": "STO-3G",
        "bond_length_ang": 0.735,
        "n_qubits": int(n_qubits),
        "n_pauli_terms": int(len(labels)),
        "reference_ground_state_energy_Ha": e_gs_total,
        "literature_H2_STO3G_FCI_Ha_at_0.735": -1.137270,
        "energy_reconstruction_from_pauli_sum": E_reconstruct + nre,
        "grouping": {
            "n_qwc_groups": len(qwc_groups),
            "n_fc_groups": len(fc_groups),
        },
        "measurement_cost_epssq_times_shots": {
            "ungrouped": M_ungrouped_scale,
            "qwc": M_qwc_scale,
            "fc": M_fc_scale,
        },
        "reduction_factor_vs_ungrouped": {
            "qwc": red_qwc,
            "fc": red_fc,
        },
        "shots_for_eps_1p6mHa_chem_accuracy": {
            "ungrouped": shots_ungrouped,
            "qwc": shots_qwc,
            "fc": shots_fc,
        },
        "wall_seconds": time.time() - t0,
    }

    # Save
    out_json = OUT_DIR / "h2_grouping_result.json"
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2, default=float)
    print(f"[6] Wrote {out_json}")

    # Save term list + group assignments for evidence
    with open(OUT_DIR / "h2_pauli_terms.json", "w") as f:
        json.dump(
            {
                "labels": labels,
                "coeffs_real": [float(np.real(c)) for c in coeffs],
                "coeffs_imag": [float(np.imag(c)) for c in coeffs],
                "term_expectation_values": Pev.tolist(),
                "term_variances": Pvar.tolist(),
                "qwc_groups": qwc_groups,
                "fc_groups": fc_groups,
            },
            f,
            indent=2,
        )

    # Summary print
    print("\n" + "=" * 70)
    print(f"H2/STO-3G measurement grouping (Jordan-Wigner, 4 qubits)")
    print("=" * 70)
    print(f"  # Pauli terms:         {len(labels)}")
    print(f"  # QWC groups:          {len(qwc_groups)}    "
          f"(term-to-group ratio {len(labels)/len(qwc_groups):.2f})")
    print(f"  # FC  groups:          {len(fc_groups)}    "
          f"(term-to-group ratio {len(labels)/len(fc_groups):.2f})")
    print()
    print(f"  eps^2 * M (ungrouped): {M_ungrouped_scale:.6f}")
    print(f"  eps^2 * M (QWC):       {M_qwc_scale:.6f}   "
          f"(reduction {red_qwc:.2f}x)")
    print(f"  eps^2 * M (FC):        {M_fc_scale:.6f}   "
          f"(reduction {red_fc:.2f}x)")
    print()
    print(f"  Shots for eps=1.6 mHa (chemical accuracy):")
    print(f"    ungrouped: {shots_ungrouped:>12.1f}")
    print(f"    QWC:       {shots_qwc:>12.1f}   ({shots_ungrouped/shots_qwc:.2f}x fewer)")
    print(f"    FC:        {shots_fc:>12.1f}   ({shots_ungrouped/shots_fc:.2f}x fewer)")
    print()
    print(f"  Total wall time: {result['wall_seconds']:.2f} s")


if __name__ == "__main__":
    main()
