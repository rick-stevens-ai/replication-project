#!/usr/bin/env python3
"""
Standard single-qubit Clifford randomized benchmarking (RB) on Qiskit Aer.

Reproduces the eq.(1) claim of Helsen et al. 2019 (arXiv:1806.02048) that
standard RB data fits an exponential  p_m ~ A + B * f^m , with f directly
related to the per-Clifford average infidelity via  r = (1 - f) * (d-1)/d
where d = 2^n_qubits (d=2 for 1 qubit).

We inject a single-qubit depolarizing channel of known per-gate probability
p_gate on every Clifford operation and check that the RB decay recovers a
consistent per-Clifford error rate.

Output: JSON with fit parameters, injected vs recovered error, and full data.
"""
from __future__ import annotations

import argparse
import itertools
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple

import numpy as np
from scipy.optimize import curve_fit

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import (
    IGate, XGate, YGate, ZGate, HGate, SGate, SdgGate,
)
from qiskit.quantum_info import Clifford, Operator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# --- 1-qubit Clifford group construction (24 elements) --------------------
# We enumerate all 24 single-qubit Cliffords by taking products of H, S over
# a small alphabet and deduping via Clifford tableau equality.

def build_1q_clifford_group() -> List[QuantumCircuit]:
    """Return 24 unique 1-qubit Clifford circuits (one representative each)."""
    generators = ["I", "X", "Y", "Z", "H", "S", "Sdg", "HS", "SH", "HSH",
                  "SHS", "HSdg", "SdgH", "HSdgH", "SdgHSdg", "SSS"]
    # brute-force: enumerate short words in {H, S} and dedup by tableau
    seen = {}
    ops = {
        "H": HGate(), "S": SGate(), "Sdg": SdgGate(),
        "X": XGate(), "Y": YGate(), "Z": ZGate(), "I": IGate(),
    }
    alphabet = ["H", "S", "Sdg", "X", "Y", "Z"]
    # words of length up to 5 are more than sufficient to cover 24 elements
    for L in range(0, 6):
        for word in itertools.product(alphabet, repeat=L):
            qc = QuantumCircuit(1)
            for g in word:
                qc.append(ops[g], [0])
            cl = Clifford(qc)
            key = cl.tableau.tobytes()
            if key not in seen:
                seen[key] = qc
            if len(seen) == 24:
                break
        if len(seen) == 24:
            break
    assert len(seen) == 24, f"expected 24 Cliffords, found {len(seen)}"
    return list(seen.values())


def compose_clifford_circuits(circs: List[QuantumCircuit]) -> QuantumCircuit:
    """Concatenate a list of 1q circuits into one 1q circuit."""
    out = QuantumCircuit(1)
    for c in circs:
        out.compose(c, inplace=True)
    return out


def inverse_clifford(qc: QuantumCircuit) -> QuantumCircuit:
    """Return a circuit realizing the inverse Clifford."""
    cl = Clifford(qc)
    inv = cl.adjoint()
    return inv.to_circuit()


# --- RB sequence generator ------------------------------------------------

def build_rb_sequence(m: int, group: List[QuantumCircuit], rng: np.random.Generator
                      ) -> Tuple[QuantumCircuit, QuantumCircuit]:
    """Build one RB sequence of length m (m random Cliffords + 1 inverse).
    Returns (full_circuit_no_measure, ideal_full_op) — ideal is identity by
    construction. Measurement in Z basis, all-zero survival prob."""
    idx = rng.integers(0, len(group), size=m)
    chosen = [group[i] for i in idx]
    seq = compose_clifford_circuits(chosen)
    inv = inverse_clifford(seq)
    full = QuantumCircuit(1, 1)
    for c in chosen:
        full.compose(c, inplace=True)
    full.compose(inv, inplace=True)
    full.measure(0, 0)
    return full


def survival_probability(counts: dict, shots: int) -> float:
    return counts.get("0", 0) / shots


# --- RB experiment --------------------------------------------------------

@dataclass
class RBParams:
    p_gate_depol: float           # per-Clifford depolarizing prob (injected)
    seq_lengths: List[int]
    seqs_per_length: int
    shots: int
    seed: int
    n_cliffs_group: int = 24


def run_rb(params: RBParams, out_dir: Path) -> dict:
    rng = np.random.default_rng(params.seed)

    # Noise model: depolarizing error attached to every gate in the basis
    # (we transpile to a small basis so per-basis-gate noise scales with the
    # Clifford compile length, roughly one depol per Clifford applied).
    noise_model = NoiseModel()
    err_1q = depolarizing_error(params.p_gate_depol, 1)
    # attach to h, s, sdg, x, y, z (1-qubit basis for Cliffords)
    for g in ["h", "s", "sdg", "x", "y", "z", "id"]:
        noise_model.add_all_qubit_quantum_error(err_1q, [g])

    sim = AerSimulator(noise_model=noise_model)

    group = build_1q_clifford_group()

    fidelity_curve = []
    per_m_raw = {}

    for m in params.seq_lengths:
        surv_list = []
        for k in range(params.seqs_per_length):
            circ = build_rb_sequence(m, group, rng)
            # transpile down to basis gates the noise model targets
            tqc = transpile(circ, sim, basis_gates=["h", "s", "sdg", "x",
                                                    "y", "z", "id", "measure"],
                            optimization_level=0)
            res = sim.run(tqc, shots=params.shots).result()
            counts = res.get_counts()
            surv = survival_probability(counts, params.shots)
            surv_list.append(surv)
        mean_surv = float(np.mean(surv_list))
        std_surv = float(np.std(surv_list) / np.sqrt(len(surv_list)))
        fidelity_curve.append((m, mean_surv, std_surv))
        per_m_raw[m] = surv_list
        print(f"  m={m:>3d}  <p>={mean_surv:.4f}  sem={std_surv:.4f}  "
              f"({len(surv_list)} seqs)")

    ms = np.array([x[0] for x in fidelity_curve], dtype=float)
    pm = np.array([x[1] for x in fidelity_curve], dtype=float)
    sem = np.array([max(x[2], 1e-4) for x in fidelity_curve], dtype=float)

    def model(m, A, B, f):
        return A + B * (f ** m)

    # decent initial guess
    p0 = [0.5, 0.5, max(0.5, 1.0 - 2 * params.p_gate_depol)]
    try:
        popt, pcov = curve_fit(model, ms, pm, sigma=sem, p0=p0,
                               bounds=([0, 0, 0], [1, 1, 1]),
                               absolute_sigma=True, maxfev=10000)
        A, B, f = [float(x) for x in popt]
        perr = np.sqrt(np.diag(pcov))
    except Exception as e:
        print("fit failed:", e)
        A, B, f = float("nan"), float("nan"), float("nan")
        perr = [float("nan")] * 3

    d = 2
    # per-Clifford average error rate r = (d-1)/d * (1 - f)
    r_clifford = (d - 1) / d * (1.0 - f) if not np.isnan(f) else float("nan")

    # a single Clifford compiles on average to ~1.875 of our basis 1q gates
    # (varies by decomposition). We report both bulk r_clifford and the
    # per-basis-gate injected p; the point is qualitative recovery.

    result = {
        "fit": {"A": A, "B": B, "f": f,
                "A_stderr": float(perr[0]),
                "B_stderr": float(perr[1]),
                "f_stderr": float(perr[2])},
        "d": d,
        "r_per_clifford_recovered": float(r_clifford),
        "injected_per_basis_gate_depol": params.p_gate_depol,
        "seq_lengths": list(params.seq_lengths),
        "seqs_per_length": params.seqs_per_length,
        "shots": params.shots,
        "seed": params.seed,
        "curve": [{"m": int(m), "p_mean": float(pm_val), "p_sem": float(s)}
                  for m, pm_val, s in fidelity_curve],
        "per_m_raw": {int(k): [float(x) for x in v]
                      for k, v in per_m_raw.items()},
    }
    (out_dir / "rb_standard_result.json").write_text(
        json.dumps(result, indent=2))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=float, default=0.005,
                    help="per-basis-gate depolarizing probability")
    ap.add_argument("--seqs", type=int, default=30,
                    help="sequences per length")
    ap.add_argument("--shots", type=int, default=512)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--lengths", type=str,
                    default="1,3,5,8,12,16,24,32,48,64")
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    lengths = [int(x) for x in args.lengths.split(",")]
    params = RBParams(
        p_gate_depol=args.p,
        seq_lengths=lengths,
        seqs_per_length=args.seqs,
        shots=args.shots,
        seed=args.seed,
    )
    print(f"[standard RB] p={args.p} seqs={args.seqs} shots={args.shots} "
          f"lengths={lengths}")
    t0 = time.time()
    result = run_rb(params, out_dir)
    dt = time.time() - t0
    print(f"[standard RB] fit: A={result['fit']['A']:.4f} "
          f"B={result['fit']['B']:.4f} f={result['fit']['f']:.5f} "
          f"r_per_clifford={result['r_per_clifford_recovered']:.5f} "
          f"(injected p_per_basis_gate={result['injected_per_basis_gate_depol']})")
    print(f"[standard RB] wall={dt:.1f}s")


if __name__ == "__main__":
    main()
