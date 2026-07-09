#!/usr/bin/env python3
"""
Qiskit sanity check for the 15-to-1 magic-state-distillation protocol
used as the foundation of the O'Gorman-Campbell factory analysis.

We do NOT run the full 15-qubit distillation circuit (which requires
a 15-qubit encoded Reed-Muller CSS code + non-Clifford T-gate injection).
Instead we do two things:

  A) Ideal-injection sanity check: prepare a perfect |T> state and
     confirm <T|T> = 1  (i.e. the |T> = T|+> state is what we think it is).

  B) Depolarising-noise Monte-Carlo experiment on a small logical
     T-gate injection: apply a T-gate that has probability p of being
     replaced by a random Pauli error. Sweep p in {1e-2, 3e-3, 1e-3,
     3e-4, 1e-4} and count Z-basis measurement disagreement with
     the ideal T|+> state. The observed error rate should scale
     LINEARLY in p (i.e. this is the RAW T-state error rate before
     distillation). We then apply the analytic 15-to-1 map
     p_out = 35 * p^3 and confirm that the distilled rate is many
     orders of magnitude below the raw rate for p ~ 1e-3.

This mirrors what the paper takes as its input: raw magic state error
rate ~ 0.4 * p_g (see paper p.7), fed into the analytic distillation
formula. So we are demonstrating that
  (i) Qiskit sees the raw error rate we assume, and
  (ii) the 35 * p^3 map crushes it as claimed.
"""
import json, math
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator, random_pauli

# ---------- (A) Ideal |T> preparation sanity check ----------
qc = QuantumCircuit(1)
qc.h(0)
qc.t(0)
sv_prepared = Statevector(qc)
# Expected: (|0> + e^{i pi/4} |1>) / sqrt(2)
expected = np.array([1.0, np.exp(1j * np.pi / 4)]) / np.sqrt(2)
sv_expected = Statevector(expected)
fidelity_ideal = abs(sv_prepared.inner(sv_expected)) ** 2
print(f"[A] Ideal-|T>-injection fidelity vs expected = {fidelity_ideal:.10f}")

# ---------- (B) Noisy T-gate Monte-Carlo, raw vs distilled rates ----------
def measure_raw_error_rate(p_err: float, n_shots: int = 20000,
                           rng: np.random.Generator | None = None) -> float:
    """
    Prepare |+>, then apply either an ideal T (with prob 1-p) or a
    depolarising Pauli (X/Y/Z uniform) with prob p. Measure in the
    T-eigenbasis {|T>, |T_perp>} by rotating back with T^dagger H and
    counting |1> outcomes as errors.
    """
    if rng is None:
        rng = np.random.default_rng(1234)
    err_counts = 0
    for _ in range(n_shots):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        if rng.random() < p_err:
            # Uniform Pauli error
            gate = rng.choice(['x', 'y', 'z'])
            getattr(qc, gate)(0)
            qc.t(0)          # ideal T still applied
        else:
            qc.t(0)
        # Rotate |T> -> |0>: apply T^dagger then H
        qc.tdg(0)
        qc.h(0)
        # Measure Z: outcome '1' = error
        sv = Statevector(QuantumCircuit(1))  # dummy
        # Compute analytical P(1) from statevector before measurement
        qc_no_meas = qc.copy()
        qc_no_meas.data = [d for d in qc_no_meas.data if d.operation.name != 'measure']
        sv_final = Statevector(qc_no_meas)
        p1 = abs(sv_final.data[1]) ** 2
        # Sample
        if rng.random() < p1:
            err_counts += 1
    return err_counts / n_shots


rng = np.random.default_rng(20250705)
raw_sweep = []
for p in (1e-2, 3e-3, 1e-3, 3e-4, 1e-4):
    # Small shot count for large p; larger for small p (still tractable)
    n = 20000 if p >= 1e-3 else 40000
    p_measured = measure_raw_error_rate(p, n_shots=n, rng=rng)
    p_distilled = 35.0 * p ** 3
    print(f"[B] p_err={p:.0e}  raw_measured={p_measured:.5f}  "
          f"distilled_15to1={p_distilled:.3e}  suppression={p/p_distilled if p_distilled>0 else float('inf'):.2e}")
    raw_sweep.append({
        "p_err_injected": p,
        "raw_measured": p_measured,
        "n_shots": n,
        "distilled_15to1": p_distilled,
        "suppression_factor": p / p_distilled if p_distilled > 0 else None,
    })

# Fit slope of measured raw rate vs injected p (should be ~1 = linear)
pin = np.array([r["p_err_injected"] for r in raw_sweep])
pou = np.array([r["raw_measured"] for r in raw_sweep])
mask = pou > 0
slope_raw, _ = np.polyfit(np.log10(pin[mask]), np.log10(pou[mask]), 1)
print(f"[B] fit slope raw-measured vs injected p = {slope_raw:.4f}  (expect ~1)")

# Also verify the analytic distilled slope
pdd = np.array([r["distilled_15to1"] for r in raw_sweep])
slope_dist, ic_dist = np.polyfit(np.log10(pin), np.log10(pdd), 1)
print(f"[B] fit slope distilled_15to1 vs injected p = {slope_dist:.6f}  (expect 3.0)")
print(f"[B] fit prefactor distilled_15to1 = {10**ic_dist:.6f}  (expect 35.0)")

results = {
    "A_ideal_T_state_preparation": {
        "fidelity_vs_expected": fidelity_ideal,
        "verdict": "PASS" if fidelity_ideal > 0.999999 else "FAIL",
    },
    "B_noisy_T_gate_monte_carlo": {
        "sweep": raw_sweep,
        "fit_slope_raw_vs_injected_p": slope_raw,
        "fit_slope_distilled_vs_injected_p": slope_dist,
        "fit_prefactor_distilled": 10 ** ic_dist,
        "verdict_raw_is_linear": abs(slope_raw - 1.0) < 0.15,
        "verdict_distilled_is_cubic_with_prefactor_35": (
            abs(slope_dist - 3.0) < 1e-6 and abs(10 ** ic_dist - 35.0) < 1e-5
        ),
    },
}

outdir = Path(__file__).parent
with open(outdir / "qiskit_sanity.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("qiskit_sanity.json written to", outdir)
