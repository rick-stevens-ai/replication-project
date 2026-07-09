#!/usr/bin/env python3
"""
Independent replication of Brassard, Høyer, Tapp — "Quantum Counting"
arXiv: quant-ph/9805082 (1998).

We implement Algorithm Count(F, P) from the paper:
   1. Prepare |0>|0> on (t precision qubits) ⊗ (n search qubits)
   2. Apply W ⊗ W (Hadamards on both registers)
   3. Apply controlled-Grover-iterations: on the precision register acting
      as control counter, apply G_F^m to the search register (i.e. QPE of G_F)
   4. Inverse QFT on precision register
   5. Measure precision register -> f_tilde in [0, P)
      (if f_tilde > P/2 then f_tilde <- P - f_tilde)
   6. Output t_hat = N * sin^2( pi * f_tilde / P )

Theorem 5:  |t - t_hat| < (2*pi/P) * sqrt(t*N) + (pi^2 / P^2) * N
            with probability >= 8/pi^2 ~ 0.811.

Small instance:  n = 4 (search space N = 16), M/t ∈ {1,2,4,8},
                 t precision qubits P ∈ {2^4=16, 2^5=32}.
We run REAL Qiskit statevector simulation (Aer) and record the empirical
success probability vs the analytical bound.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT, DiagonalGate, GroverOperator
from qiskit_aer import AerSimulator

SHOTS = 4096
EVIDENCE_DIR = Path(__file__).resolve().parent


def grover_operator(n: int, marked: list[int]) -> QuantumCircuit:
    """Build the Grover operator Q = D S_f using Qiskit's GroverOperator.

    Oracle S_f flips the phase of the marked computational-basis states via a
    DiagonalGate; D = H^n S_0 H^n uses Qiskit's default zero-reflection.
    Eigenvalues of Q are e^{±2iθ} with sin²(θ) = t/N (per BHT'98).
    """
    diag = np.ones(2**n, dtype=complex)
    for m in marked:
        diag[m] = -1.0
    oracle = QuantumCircuit(n, name="S_f")
    oracle.append(DiagonalGate(diag.tolist()), list(range(n)))
    G = GroverOperator(oracle)
    return G


def quantum_counting_circuit(n_search: int, t_prec: int, marked: list[int]) -> QuantumCircuit:
    """Assemble the full quantum counting circuit.

    n_search  : # search qubits  (N = 2**n_search)
    t_prec    : # precision qubits (P = 2**t_prec)
    marked    : list of marked-item indices
    """
    prec = QuantumRegister(t_prec, name="p")
    srch = QuantumRegister(n_search, name="s")
    creg = ClassicalRegister(t_prec, name="c")
    qc = QuantumCircuit(prec, srch, creg)

    # Step 1-2: |Psi_0> = W|0> W|0>
    qc.h(prec)
    qc.h(srch)

    # Step 3: controlled Grover powers  G^(2^j) controlled on prec[j]
    G = grover_operator(n_search, marked).to_gate(label="G")
    for j in range(t_prec):
        power = 2**j
        # controlled G^power = repeat controlled-G power times
        Gc = G.control(1)
        for _ in range(power):
            qc.append(Gc, [prec[j], *srch])

    # Step 4: inverse QFT on precision register
    qc.append(QFT(t_prec, inverse=True, do_swaps=True).to_gate(label="IQFT"), prec[:])

    # Measurement
    qc.measure(prec, creg)
    return qc


def run_instance(n_search: int, t_prec: int, M: int, shots: int = SHOTS, seed: int = 42) -> dict:
    """Run one instance and return a rich result dict."""
    N = 2**n_search
    P = 2**t_prec
    assert 0 <= M <= N, f"M={M} out of range for N={N}"
    # Choose the first M items as marked (arbitrary label — doesn't affect counting).
    marked = list(range(M))

    qc = quantum_counting_circuit(n_search, t_prec, marked)
    sim = AerSimulator(method="statevector", seed_simulator=seed)
    tqc = transpile(qc, sim)
    t0 = time.time()
    result = sim.run(tqc, shots=shots).result()
    elapsed = time.time() - t0
    counts = result.get_counts()

    # For each measured bitstring (little-endian in Qiskit), decode f_tilde,
    # fold via f_tilde <- min(f_tilde, P - f_tilde), then t_hat = N sin^2(pi f_tilde / P).
    est_counts = {}
    total = 0
    for bitstr, c in counts.items():
        # Qiskit puts prec[0] as the rightmost bit -> int(bitstr, 2) already treats
        # prec[0] as the LSB, matching a standard QPE readout with `do_swaps=True`.
        f_raw = int(bitstr, 2)
        f_fold = f_raw if f_raw <= P // 2 else P - f_raw
        t_hat = N * math.sin(math.pi * f_fold / P) ** 2
        est_counts[bitstr] = {
            "f_raw": f_raw,
            "f_fold": f_fold,
            "t_hat": t_hat,
            "shots": c,
        }
        total += c

    # Analytic error bound from Theorem 5:  epsilon = (2*pi/P)*sqrt(t*N) + (pi^2/P^2)*N
    t_true = M
    if t_true == 0:
        bound = (math.pi**2 / P**2) * N
    else:
        bound = (2 * math.pi / P) * math.sqrt(t_true * N) + (math.pi**2 / P**2) * N

    # Empirical success probability under the theorem's inequality.
    good_shots = 0
    weighted_err = 0.0
    for meta in est_counts.values():
        err = abs(t_true - meta["t_hat"])
        weighted_err += err * meta["shots"]
        if err < bound:
            good_shots += meta["shots"]
    p_success = good_shots / total
    mean_abs_err = weighted_err / total

    # Best single estimate = arg-max shot bin.
    best_bit, best_meta = max(est_counts.items(), key=lambda kv: kv[1]["shots"])
    best_t_hat = best_meta["t_hat"]
    best_round = int(round(best_t_hat))

    return {
        "n_search": n_search,
        "N": N,
        "t_prec": t_prec,
        "P": P,
        "M_true": M,
        "shots": total,
        "elapsed_sec": elapsed,
        "bound_thm5": bound,
        "p_success_empirical": p_success,
        "p_success_theorem_bound": 8.0 / math.pi**2,
        "mean_abs_err": mean_abs_err,
        "best_t_hat": best_t_hat,
        "best_M_rounded": best_round,
        "abs_err_best": abs(best_t_hat - t_true),
        "num_qubits": qc.num_qubits,
        "circuit_depth": tqc.depth(),
        "gate_count": sum(tqc.count_ops().values()),
    }


def main():
    results = []
    n_search = 4  # N = 16
    for t_prec in (4, 5):
        for M in (1, 2, 4, 8):
            print(f"[run] N=16 M={M} t_prec={t_prec} P={2**t_prec}", flush=True)
            r = run_instance(n_search, t_prec, M)
            print(
                f"      best M~ {r['best_t_hat']:.3f} (rounded {r['best_M_rounded']}), "
                f"bound<{r['bound_thm5']:.3f}, "
                f"P(success)_emp={r['p_success_empirical']:.3f} vs 8/pi^2={r['p_success_theorem_bound']:.3f}",
                flush=True,
            )
            results.append(r)

    out = {
        "paper": "arXiv:quant-ph/9805082 Brassard, Hoyer, Tapp — Quantum Counting",
        "impl": "Qiskit 2.5.0 + qiskit-aer 0.17.2 (statevector)",
        "shots": SHOTS,
        "results": results,
    }
    out_path = EVIDENCE_DIR / "results.json"
    with out_path.open("w") as fh:
        json.dump(out, fh, indent=2)

    print(f"\n[done] wrote {out_path}")

    # CSV-style summary
    csv_path = EVIDENCE_DIR / "results.csv"
    with csv_path.open("w") as fh:
        fh.write("N,M_true,P,best_t_hat,best_M_rounded,abs_err_best,bound_thm5,p_success_emp,p_success_thm,mean_abs_err,depth,gates\n")
        for r in results:
            fh.write(
                f"{r['N']},{r['M_true']},{r['P']},{r['best_t_hat']:.4f},"
                f"{r['best_M_rounded']},{r['abs_err_best']:.4f},{r['bound_thm5']:.4f},"
                f"{r['p_success_empirical']:.4f},{r['p_success_theorem_bound']:.4f},"
                f"{r['mean_abs_err']:.4f},{r['circuit_depth']},{r['gate_count']}\n"
            )
    print(f"[done] wrote {csv_path}")


if __name__ == "__main__":
    main()
