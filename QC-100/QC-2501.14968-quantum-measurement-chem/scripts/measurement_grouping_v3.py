"""
v3 - efficient variance/grouping analysis for larger Hamiltonians.

Key change from v2:
  - Use SparsePauliOp arithmetic to build fragment operators and evaluate
    variances via Statevector.expectation_value (which handles sparse ops).
  - Cap in-memory dense matrix use.
"""
from __future__ import annotations
import json, time, numpy as np
from pathlib import Path
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit.quantum_info import SparsePauliOp, Statevector

ART = Path(__file__).resolve().parents[1] / "artifacts"
ART.mkdir(parents=True, exist_ok=True)


def build_hamiltonian(atom_str, basis="sto3g", spin=0, charge=0):
    driver = PySCFDriver(atom=atom_str, basis=basis, charge=charge,
                          spin=spin, unit=DistanceUnit.ANGSTROM)
    prob = driver.run()
    H = JordanWignerMapper().map(prob.hamiltonian.second_q_op())
    return H, prob.nuclear_repulsion_energy


def qwc(a, b):
    for x, y in zip(a, b):
        if x != "I" and y != "I" and x != y:
            return False
    return True


def general_commute(a, b):
    diff = 0
    for x, y in zip(a, b):
        if x != "I" and y != "I" and x != y:
            diff += 1
    return diff % 2 == 0


def color_greedy(labels, commute_fn):
    n = len(labels)
    incompat = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if not commute_fn(labels[i], labels[j]):
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


def analyze(H: SparsePauliOp, nre: float, name: str):
    n_q = H.num_qubits
    labels = list(H.paulis.to_labels())
    coeffs = np.array(H.coeffs, dtype=complex)
    n_terms = len(labels)
    print(f"[{name}] n_qubits={n_q} n_terms={n_terms}")

    # Ground state
    if n_q <= 12:
        Hmat = H.to_matrix()  # up to 4096^2 = 16M complex128 = 256 MB
        e, V = np.linalg.eigh(Hmat)
        psi_arr = np.ascontiguousarray(V[:, 0], dtype=complex)
        del Hmat
        e_gs = float(e[0]) + nre
        sv = Statevector(psi_arr)
    else:
        print(f"[{name}] SKIP: n_qubits > 12")
        return None
    print(f"[{name}] E_gs = {e_gs:.6f} Ha")

    # Per-term ev via SparsePauliOp expectation
    print(f"[{name}] computing per-term expectations ...")
    Pev = np.array([np.real(sv.expectation_value(SparsePauliOp(labels[j])))
                     for j in range(n_terms)])
    Pvar = 1.0 - Pev * Pev
    E_reconstruct = float(np.real(np.sum(coeffs.real * Pev))) + nre

    abs_c = np.abs(coeffs)
    S_ung_opt = float(np.sum(abs_c * np.sqrt(np.maximum(Pvar, 0.0))))
    S_ung_unif = float(n_terms * np.sum(abs_c ** 2 * Pvar))

    # QWC
    print(f"[{name}] coloring QWC ...")
    t = time.time()
    qwc_g = color_greedy(labels, qwc)
    print(f"[{name}] QWC groups={len(qwc_g)}  ({time.time()-t:.1f}s)")

    # FC
    print(f"[{name}] coloring FC ...")
    t = time.time()
    fc_g = color_greedy(labels, general_commute)
    print(f"[{name}] FC  groups={len(fc_g)}   ({time.time()-t:.1f}s)")

    # Fragment variance via SparsePauliOp
    def frag_var(group):
        subop = SparsePauliOp([labels[j] for j in group],
                              coeffs=[coeffs[j] for j in group])
        ev = complex(sv.expectation_value(subop))
        # <H_a^2> = <H_a . H_a> - use simplify
        ev2op = (subop @ subop).simplify()
        ev2 = complex(sv.expectation_value(ev2op))
        return max(float(np.real(ev2 - ev * ev)), 0.0)

    print(f"[{name}] computing QWC fragment variances ...")
    t = time.time()
    qwc_vars = [frag_var(g) for g in qwc_g]
    print(f"[{name}]   ({time.time()-t:.1f}s)")
    S_qwc_opt = float(np.sum(np.sqrt(qwc_vars)))
    S_qwc_unif = float(len(qwc_g) * np.sum(qwc_vars))

    print(f"[{name}] computing FC fragment variances ...")
    t = time.time()
    fc_vars = [frag_var(g) for g in fc_g]
    print(f"[{name}]   ({time.time()-t:.1f}s)")
    S_fc_opt = float(np.sum(np.sqrt(fc_vars)))
    S_fc_unif = float(len(fc_g) * np.sum(fc_vars))

    result = {
        "molecule": name,
        "n_qubits": int(n_q),
        "n_pauli_terms": int(n_terms),
        "e_gs_total_Ha": e_gs,
        "e_reconstruct": E_reconstruct,
        "n_qwc_groups": len(qwc_g),
        "n_fc_groups": len(fc_g),
        "combinatorial_terms_per_qwc_group": n_terms / len(qwc_g),
        "combinatorial_terms_per_fc_group": n_terms / len(fc_g),
        "S_opt_ungrouped_squared": S_ung_opt ** 2,
        "S_opt_qwc_squared": S_qwc_opt ** 2,
        "S_opt_fc_squared": S_fc_opt ** 2,
        "S_unif_ungrouped": S_ung_unif,
        "S_unif_qwc": S_qwc_unif,
        "S_unif_fc": S_fc_unif,
        "opt_alloc_reduction_qwc": (S_ung_opt ** 2) / (S_qwc_opt ** 2) if S_qwc_opt > 0 else None,
        "opt_alloc_reduction_fc": (S_ung_opt ** 2) / (S_fc_opt ** 2) if S_fc_opt > 0 else None,
        "unif_alloc_reduction_qwc": S_ung_unif / S_qwc_unif if S_qwc_unif > 0 else None,
        "unif_alloc_reduction_fc": S_ung_unif / S_fc_unif if S_fc_unif > 0 else None,
    }
    print(f"[{name}] ungrouped S_opt^2 = {S_ung_opt**2:.4f}   S_unif = {S_ung_unif:.4f}")
    print(f"[{name}] QWC       S_opt^2 = {S_qwc_opt**2:.4f}   S_unif = {S_qwc_unif:.4f}   "
          f"opt_red={result['opt_alloc_reduction_qwc']:.2f}x  unif_red={result['unif_alloc_reduction_qwc']:.2f}x")
    print(f"[{name}] FC        S_opt^2 = {S_fc_opt**2:.4f}   S_unif = {S_fc_unif:.4f}   "
          f"opt_red={result['opt_alloc_reduction_fc']:.2f}x  unif_red={result['unif_alloc_reduction_fc']:.2f}x")
    return result


def main():
    t0 = time.time()
    mols = [
        ("H2_R=0.735",  "H 0 0 0; H 0 0 0.735"),
        ("H2_R=1.500",  "H 0 0 0; H 0 0 1.500"),
        ("LiH_R=1.595", "Li 0 0 0; H 0 0 1.595"),
    ]
    out = {}
    for name, atom in mols:
        try:
            H, nre = build_hamiltonian(atom, basis="sto3g")
            r = analyze(H, nre, name)
            if r is not None:
                out[name] = r
        except Exception as e:
            print(f"ERROR {name}: {e}")
            out[name] = {"error": str(e)}
    out["_meta"] = {"paper": "arXiv:2501.14968", "wall_s": time.time() - t0}
    with open(ART / "grouping_summary_v3.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nWrote {ART/'grouping_summary_v3.json'}  in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
