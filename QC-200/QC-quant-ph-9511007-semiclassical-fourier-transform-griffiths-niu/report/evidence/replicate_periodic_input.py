#!/usr/bin/env python3
"""
Stronger test of Griffiths-Niu: prepare a *periodic* superposition
   |psi> = 1/sqrt(K) sum_{k=0}^{K-1} |k * period mod 2^n>
which is exactly the kind of state that appears just before the QFT in
Shor's period-finding.  For such states, QFT|psi> concentrates on values
c such that c*period/2^n is close to an integer -- a highly NON-UNIFORM
distribution.  This is a much more discriminating test than |x> alone
(where QFT|x> is uniform and any bug that scrambles phases is invisible
in probabilities).

We compare:
  (i) standard full QFT circuit (H + CP two-qubit gates)
  (ii) Griffiths-Niu semiclassical QFT (H + measurement + classically-
       conditioned single-qubit phase gates via if_test)
against each other and against the analytic QFT probability distribution
computed by an exact numpy DFT.
"""

from __future__ import annotations

import json
import math
import os
from collections import Counter
from pathlib import Path

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import AerSimulator

import sys

sys.path.insert(0, str(Path(__file__).parent))
from replicate_semiclassical_qft import (  # noqa: E402
    standard_qft_circuit,
    semiclassical_qft_circuit,
    counts_to_probs,
    tvd,
)


HERE = Path(__file__).resolve().parent


def periodic_state_prep_circuit(n: int, period: int) -> QuantumCircuit:
    """Prepare 1/sqrt(K) sum_{k=0}^{K-1} |k*period mod 2^n> on n qubits.

    We prepare it via direct amplitude initialization (Statevector -> initialize),
    because this is a stand-in for whatever prepares the register before the
    Fourier transform in Shor.  It doesn't matter for testing the QFT half of
    the algorithm.
    """
    N = 2 ** n
    amps = np.zeros(N, dtype=complex)
    # values k*period mod N for k=0..N-1, dedup'ed (period-divides-N case gives
    # a nice uniform sum on the {0, period, 2*period, ...} sub-lattice).
    values = sorted(set((k * period) % N for k in range(N)))
    for v in values:
        amps[v] = 1.0
    amps /= np.linalg.norm(amps)

    qr = QuantumRegister(n, "q")
    qc = QuantumCircuit(qr)
    qc.initialize(amps.tolist(), qr[:])
    return qc, amps


def build_full_qft_from_state(n: int, state_prep: QuantumCircuit) -> tuple[QuantumCircuit, dict]:
    """Full standard QFT applied after a state-prep circuit, then measure."""
    qc_qft_only, gc = standard_qft_circuit(n, input_x=0)  # we'll strip its |0> prep + measurement, then re-attach
    # Rebuild fresh so we have separate control over prep and measurement:
    qr = QuantumRegister(n, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)
    qc.compose(state_prep, qubits=qr[:], inplace=True)
    counts = {"h": 0, "cp": 0, "measure": 0, "one_qubit_phase": 0}
    for j in reversed(range(n)):
        qc.h(qr[j])
        counts["h"] += 1
        for k in reversed(range(j)):
            m = j - k + 1
            angle = 2.0 * math.pi / (2 ** m)
            qc.cp(angle, qr[k], qr[j])
            counts["cp"] += 1
    for j in range(n):
        qc.measure(qr[j], cr[n - 1 - j])
        counts["measure"] += 1
    return qc, counts


def build_semi_qft_from_state(n: int, state_prep: QuantumCircuit) -> tuple[QuantumCircuit, dict]:
    """Semiclassical QFT applied after a state-prep circuit."""
    qr = QuantumRegister(n, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)
    qc.compose(state_prep, qubits=qr[:], inplace=True)
    counts = {"h": 0, "cp": 0, "measure": 0, "one_qubit_phase": 0}
    for j in reversed(range(n)):
        qc.h(qr[j])
        counts["h"] += 1
        cbit = n - 1 - j
        qc.measure(qr[j], cr[cbit])
        counts["measure"] += 1
        for k in reversed(range(j)):
            m = j - k + 1
            angle = 2.0 * math.pi / (2 ** m)
            with qc.if_test((cr[cbit], 1)):
                qc.p(angle, qr[k])
            counts["one_qubit_phase"] += 1
    return qc, counts


def analytic_qft_prob(state_amps: np.ndarray) -> np.ndarray:
    """|c-amplitude|^2 where c-amplitudes = numpy IDFT(state)/sqrt(N) ... actually the
    conventional QFT of Nielsen/Chuang is:
        |c> gets amplitude 1/sqrt(N) sum_x amps[x] exp(2*pi*i*x*c/N)
    """
    N = len(state_amps)
    idx = np.arange(N)
    # matrix M[c,x] = exp(2 pi i x c / N) / sqrt(N)
    M = np.exp(2j * math.pi * np.outer(idx, idx) / N) / math.sqrt(N)
    out = M @ state_amps
    return np.abs(out) ** 2


def main():
    shots = int(os.environ.get("SHOTS", "16384"))
    seed = 20260705
    sim = AerSimulator(seed_simulator=seed)

    cases = [
        # (n, period)
        (3, 2),   # concentrates on c in {0, 4}
        (3, 4),   # concentrates on c in {0, 2, 4, 6}
        (4, 2),   # concentrates on c in {0, 8}
        (4, 4),   # concentrates on c in {0, 4, 8, 12}
        (4, 8),   # concentrates on c in {0, 2, 4, 6, 8, 10, 12, 14}
    ]

    results = []
    for n, period in cases:
        prep, amps = periodic_state_prep_circuit(n, period)
        qc_full, gc_full = build_full_qft_from_state(n, prep)
        qc_semi, gc_semi = build_semi_qft_from_state(n, prep)
        p_ana = analytic_qft_prob(amps)

        tqc_full = transpile(qc_full, sim)
        tqc_semi = transpile(qc_semi, sim)

        r_full = sim.run(tqc_full, shots=shots, seed_simulator=seed).result()
        r_semi = sim.run(tqc_semi, shots=shots, seed_simulator=seed + 1).result()

        p_full = counts_to_probs(r_full.get_counts(), n)
        p_semi = counts_to_probs(r_semi.get_counts(), n)

        d_full = tvd(p_full, p_ana)
        d_semi = tvd(p_semi, p_ana)
        d_full_semi = tvd(p_full, p_semi)

        peaks_ana = sorted(int(c) for c in np.where(p_ana > 1e-6)[0])
        peaks_semi = sorted(int(c) for c, p in enumerate(p_semi) if p > 0.5 / (2 ** n))

        results.append(
            {
                "n": n,
                "period": period,
                "shots": shots,
                "expected_peaks_analytic": peaks_ana,
                "observed_peaks_semi": peaks_semi,
                "tvd_full_vs_analytic": d_full,
                "tvd_semi_vs_analytic": d_semi,
                "tvd_full_vs_semi": d_full_semi,
                "gate_counts_full": gc_full,
                "gate_counts_semi": gc_semi,
                "agree_within_0.03": d_full_semi < 0.03,
            }
        )
        print(
            f"n={n} period={period}: peaks_ana={peaks_ana}  peaks_semi={peaks_semi}  "
            f"TVD(full|ana)={d_full:.4f}  TVD(semi|ana)={d_semi:.4f}  "
            f"TVD(full|semi)={d_full_semi:.4f}"
        )

    all_agree = all(r["agree_within_0.03"] for r in results)
    print(f"ALL AGREE within TVD<0.03: {all_agree}")

    out = HERE / "results_periodic.json"
    with out.open("w") as f:
        json.dump({"cases": results, "all_agree_within_0.03": all_agree}, f, indent=2)
    print("Wrote", out)


if __name__ == "__main__":
    main()
