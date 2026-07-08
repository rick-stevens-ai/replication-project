"""
v2 - broader replication of measurement-grouping methodology (arXiv:2501.14968).

Additions vs v1:
  * Test multiple molecules (H2, LiH, H2O) and geometries.
  * Compute BOTH shot-cost metrics that appear in the literature:
      (a) Optimal-Wu shot allocation (paper's Eq. ~72, best case), given true variances/covariances
      (b) Uniform-shot naive allocation: M shots split evenly among fragments
  * Report the "measurement cost proxy" = ( sum_alpha sqrt(Var(H_alpha)) )^2 for
    grouped, vs baseline ( sum_j |c_j| sqrt(1-<P_j>^2) )^2 for ungrouped.
  * Also report a purely combinatorial group-count reduction (# terms / # groups),
    which is a coarse but widely reported metric.
  * Sort/report per-molecule results into artifacts/summary.json.
"""

from __future__ import annotations
import json
import time
import numpy as np
from pathlib import Path
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper
from qiskit.quantum_info import Pauli, SparsePauliOp


OUT_DIR = Path(__file__).resolve().parents[1] / "artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build_hamiltonian(atom_str: str, basis: str = "sto3g", spin: int = 0,
                      charge: int = 0, mapper_kind: str = "jw"):
    driver = PySCFDriver(atom=atom_str, basis=basis, charge=charge,
                          spin=spin, unit=DistanceUnit.ANGSTROM)
    problem = driver.run()
    fermionic_op = problem.hamiltonian.second_q_op()
    if mapper_kind == "jw":
        mapper = JordanWignerMapper()
    else:
        mapper = ParityMapper(num_particles=problem.num_particles)
    qubit_op = mapper.map(fermionic_op)
    return qubit_op, problem.nuclear_repulsion_energy, problem


def qubit_wise_commute(a: str, b: str) -> bool:
    for x, y in zip(a, b):
        if x == "I" or y == "I":
            continue
        if x != y:
            return False
    return True


def general_commute(a: str, b: str) -> bool:
    diff = 0
    for x, y in zip(a, b):
        if x == "I" or y == "I":
            continue
        if x != y:
            diff += 1
    return (diff % 2) == 0


def build_incompat(labels, commute_fn):
    n = len(labels)
    incompat = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if not commute_fn(labels[i], labels[j]):
                incompat[i].add(j)
                incompat[j].add(i)
    return incompat


def greedy_color_lf(incompat):
    order = sorted(incompat.keys(), key=lambda i: -len(incompat[i]))
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


def expval(psi, M):
    return np.vdot(psi, M @ psi)


def variance(psi, M):
    ev = expval(psi, M)
    ev2 = expval(psi, M @ M)
    return float(np.real(ev2 - ev * ev))


def analyze_hamiltonian(H: SparsePauliOp, nre: float, label: str,
                        n_qubits_cap: int = 12):
    n_qubits = H.num_qubits
    if n_qubits > n_qubits_cap:
        return {"skipped": True,
                "reason": f"n_qubits {n_qubits} exceeds cap {n_qubits_cap}"}

    labels = list(H.paulis.to_labels())
    coeffs = np.array(H.coeffs, dtype=complex)
    n_terms = len(labels)

    # Reference GS
    H_mat = H.to_matrix()
    e_qubit, V = np.linalg.eigh(H_mat)
    psi = V[:, 0]
    e_gs_total = float(np.real(e_qubit[0])) + nre

    # Per-term
    P_mats = [Pauli(l).to_matrix() for l in labels]
    Pev = np.array([np.real(expval(psi, M)) for M in P_mats])
    Pvar = 1.0 - Pev * Pev
    E_reconstruct = float(np.real(np.sum(np.real(coeffs) * Pev)))

    # Baseline (ungrouped optimal allocation): S = sum_j |c_j| sqrt(Var(P_j))
    S_ungrouped = float(np.sum(np.abs(coeffs) * np.sqrt(np.maximum(Pvar, 0.0))))
    # Baseline (ungrouped uniform allocation): M_j = M/n_terms
    # Var[H_hat] = sum_j c_j^2 Var(P_j) / M_j = n_terms * sum_j c_j^2 Var(P_j) / M
    # so 'proxy' for M given eps: n_terms * sum_j c_j^2 Var(P_j) / eps^2
    S_ungrouped_unif = float(n_terms * np.sum(np.abs(coeffs) ** 2 * Pvar))
    # (Note: dimensioned differently than S_ungrouped^2, but ratio makes sense
    #  when comparing uniform vs uniform.)

    def compute_group_metrics(groups):
        # Build per-fragment matrix and variance
        var_list = []
        for grp in groups:
            H_alpha = np.zeros_like(H_mat)
            for j in grp:
                H_alpha = H_alpha + coeffs[j] * P_mats[j]
            var_list.append(max(variance(psi, H_alpha), 0.0))
        S_opt = float(np.sum(np.sqrt(var_list)))
        # Uniform-alloc: n_groups * sum_alpha Var(H_alpha)
        S_unif = float(len(groups) * np.sum(var_list))
        return {
            "n_groups": len(groups),
            "S_opt": S_opt,
            "S_opt_sq": S_opt ** 2,
            "S_unif": S_unif,
            "per_fragment_variance": var_list,
        }

    incompat_qwc = build_incompat(labels, qubit_wise_commute)
    qwc_groups = greedy_color_lf(incompat_qwc)
    qwc_metrics = compute_group_metrics(qwc_groups)

    incompat_fc = build_incompat(labels, general_commute)
    fc_groups = greedy_color_lf(incompat_fc)
    fc_metrics = compute_group_metrics(fc_groups)

    return {
        "skipped": False,
        "molecule_label": label,
        "n_qubits": int(n_qubits),
        "n_pauli_terms": int(n_terms),
        "e_gs_total_Ha": e_gs_total,
        "e_reconstructed_qubit": float(E_reconstruct + nre),
        "baseline_ungrouped": {
            "S_opt": S_ungrouped,
            "S_opt_sq (proxy eps^2 * M for optimal alloc)": S_ungrouped ** 2,
            "S_unif (proxy eps^2 * M for uniform alloc)": S_ungrouped_unif,
        },
        "qwc": qwc_metrics,
        "fc": fc_metrics,
        "reductions_vs_ungrouped": {
            "optimal_alloc_qwc_over_ungrouped": (
                (S_ungrouped ** 2) / qwc_metrics["S_opt_sq"]
                if qwc_metrics["S_opt_sq"] > 0 else None
            ),
            "optimal_alloc_fc_over_ungrouped": (
                (S_ungrouped ** 2) / fc_metrics["S_opt_sq"]
                if fc_metrics["S_opt_sq"] > 0 else None
            ),
            "uniform_alloc_qwc_over_ungrouped": (
                S_ungrouped_unif / qwc_metrics["S_unif"]
                if qwc_metrics["S_unif"] > 0 else None
            ),
            "uniform_alloc_fc_over_ungrouped": (
                S_ungrouped_unif / fc_metrics["S_unif"]
                if fc_metrics["S_unif"] > 0 else None
            ),
            "combinatorial_terms_per_qwc_group": n_terms / len(qwc_groups),
            "combinatorial_terms_per_fc_group": n_terms / len(fc_groups),
        },
    }


def summarize(res, out):
    print("=" * 78)
    print(f"MOLECULE: {res['molecule_label']}")
    print("=" * 78)
    if res.get("skipped"):
        print("  SKIPPED:", res.get("reason"))
        return
    print(f"  n_qubits={res['n_qubits']}, n_pauli_terms={res['n_pauli_terms']}")
    print(f"  E_gs = {res['e_gs_total_Ha']:.6f} Ha")
    print(f"  Reconstructed sum_j c_j <P_j> = {res['e_reconstructed_qubit']:.6f} Ha")
    b = res["baseline_ungrouped"]
    q = res["qwc"]
    f = res["fc"]
    r = res["reductions_vs_ungrouped"]
    print(f"\n  Ungrouped:  S_opt^2 = {b['S_opt_sq (proxy eps^2 * M for optimal alloc)']:.4f}   "
          f"S_unif = {b['S_unif (proxy eps^2 * M for uniform alloc)']:.4f}")
    print(f"  QWC groups={q['n_groups']:>3d}  S_opt^2 = {q['S_opt_sq']:.4f}   "
          f"S_unif = {q['S_unif']:.4f}   "
          f"terms/group = {res['n_pauli_terms']/q['n_groups']:.2f}")
    print(f"  FC  groups={f['n_groups']:>3d}  S_opt^2 = {f['S_opt_sq']:.4f}   "
          f"S_unif = {f['S_unif']:.4f}   "
          f"terms/group = {res['n_pauli_terms']/f['n_groups']:.2f}")
    print(f"\n  Reduction factors vs ungrouped (higher = grouping wins):")
    print(f"    opt-alloc  QWC: {r['optimal_alloc_qwc_over_ungrouped']:.3f}x   "
          f"FC: {r['optimal_alloc_fc_over_ungrouped']:.3f}x")
    print(f"    unif-alloc QWC: {r['uniform_alloc_qwc_over_ungrouped']:.3f}x   "
          f"FC: {r['uniform_alloc_fc_over_ungrouped']:.3f}x")
    print(f"    combinatorial QWC (terms/groups): {r['combinatorial_terms_per_qwc_group']:.2f}x   "
          f"FC: {r['combinatorial_terms_per_fc_group']:.2f}x")


def main():
    t0 = time.time()
    molecules = [
        ("H2_R=0.735",   "H 0 0 0; H 0 0 0.735",  "sto3g", 0, 0),
        ("H2_R=1.500",   "H 0 0 0; H 0 0 1.500",  "sto3g", 0, 0),
        ("LiH_R=1.595",  "Li 0 0 0; H 0 0 1.595", "sto3g", 0, 0),
        ("H2O",          "O 0 0 0; H 0.757 0.586 0; H -0.757 0.586 0", "sto3g", 0, 0),
    ]

    all_results = {}
    for label, atom, basis, spin, charge in molecules:
        print(f"\n>>> building {label} in {basis} ...")
        t1 = time.time()
        try:
            H, nre, prob = build_hamiltonian(atom, basis=basis, spin=spin, charge=charge)
        except Exception as e:
            print(f"    ERROR building {label}: {e}")
            all_results[label] = {"skipped": True, "reason": f"build failed: {e}"}
            continue
        n_qubits = H.num_qubits
        n_terms = len(H.paulis)
        print(f"    n_qubits={n_qubits}, n_pauli_terms={n_terms}")
        # We can only do exact diagonalization for small n
        # For H2O in STO3G we get 14 qubits -> 16384x16384; ok but ~2GB memory
        # Cap at 12 to stay safe.
        n_cap = 12
        if n_qubits > n_cap:
            print(f"    Skipping variance analysis (n_qubits {n_qubits} > cap {n_cap}); "
                  f"reporting group-count only.")
            # Even without diagonalization we can compute groupings
            labels = list(H.paulis.to_labels())
            qwc = greedy_color_lf(build_incompat(labels, qubit_wise_commute))
            fc = greedy_color_lf(build_incompat(labels, general_commute))
            all_results[label] = {
                "skipped_variance": True,
                "n_qubits": int(n_qubits),
                "n_pauli_terms": int(n_terms),
                "n_qwc_groups": len(qwc),
                "n_fc_groups": len(fc),
                "combinatorial_terms_per_qwc_group": n_terms / len(qwc),
                "combinatorial_terms_per_fc_group": n_terms / len(fc),
                "elapsed_s": time.time() - t1,
            }
            print(f"    QWC groups: {len(qwc)}  (terms/group={n_terms/len(qwc):.2f})")
            print(f"    FC  groups: {len(fc)}   (terms/group={n_terms/len(fc):.2f})")
            continue
        res = analyze_hamiltonian(H, nre, label, n_qubits_cap=n_cap)
        res["elapsed_s"] = time.time() - t1
        all_results[label] = res
        summarize(res, out=None)

    all_results["_meta"] = {
        "paper": "arXiv:2501.14968",
        "total_wall_seconds": time.time() - t0,
    }

    with open(OUT_DIR / "grouping_summary.json", "w") as f:
        json.dump(all_results, f, indent=2, default=float)
    print(f"\nWrote {OUT_DIR / 'grouping_summary.json'}")
    print(f"Total: {time.time()-t0:.1f} s")


if __name__ == "__main__":
    main()
