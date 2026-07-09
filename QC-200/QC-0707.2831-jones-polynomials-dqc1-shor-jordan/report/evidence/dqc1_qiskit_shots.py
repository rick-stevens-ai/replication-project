#!/usr/bin/env python3
"""
Real DQC1 Hadamard test via Qiskit AerSimulator with shots.

We estimate Re[Tr(V)/2^n] and Im[Tr(V)/2^n] of the embedded 4x4 unitary
V = rho_A(sigma_1^3) (+) 1 built in replicate_shor_jordan.py by running the
actual Hadamard-test circuit with 1 clean control qubit + 2 mixed qubits
(sampled uniformly over the 4 computational basis states, which is equivalent
to the maximally mixed state I/4).

Then we combine with the Shor-Jordan formula:
    V_jones(t = A^-4) = (-A)^{3w} * D^{n-1} * f_Tr(U)
with the Fibonacci-weighted trace f_Tr(U) computed exactly (the DQC1 machine
would use a different mixed-state weighting to get f_Tr directly; here we
verify the plain trace estimate matches the analytic Tr(V)).
"""
from __future__ import annotations
import json, math, cmath, os, sys, time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sys.path.insert(0, os.path.dirname(__file__))
from replicate_shor_jordan import (
    rho_A_braid, markov_trace_fibonacci, A, D, PHI, V_trefoil_right
)

# Build U and embedded V = U (+) 1 on 2 qubits (dim 4)
n_strands = 2
word = [1, 1, 1]     # sigma_1^3, trefoil
U, paths = rho_A_braid(n_strands, word)
dim = U.shape[0]     # 3
V = np.eye(4, dtype=complex)
V[:dim, :dim] = U

# Also do left-handed trefoil for cross-check
word_L = [-1, -1, -1]
UL, _ = rho_A_braid(n_strands, word_L)
VL = np.eye(4, dtype=complex)
VL[:dim, :dim] = UL


def hadamard_test_shots(V_mat: np.ndarray, imag: bool, shots_per_state: int = 4000, seed: int = 42):
    """
    Sample Re or Im part of Tr(V)/2^n via the Hadamard test on n+1 qubits.
    We prepare the maximally mixed state I/2^n on the target by sampling
    uniformly over all 2^n computational basis states, running shots_per_state
    circuits for each, and averaging.
    """
    n = int(round(math.log2(V_mat.shape[0])))
    from qiskit.circuit.library import UnitaryGate

    # Controlled-V gate (ctrl = qubit 0)
    cV = UnitaryGate(V_mat).control(1)

    sim = AerSimulator(seed_simulator=seed)
    total_p0 = 0.0
    n_states = 2**n
    total_shots = 0

    for t_init in range(n_states):
        qc = QuantumCircuit(1 + n, 1)
        # Prepare target in |t_init> (comp basis)
        for b in range(n):
            if (t_init >> b) & 1:
                qc.x(1 + b)  # target qubits are 1..n
        # Prepare ctrl
        qc.h(0)
        # Apply controlled-V (ctrl=0, target=1..n)
        qc.append(cV, [0] + list(range(1, 1+n)))
        # For Im part: apply S^dagger on control BEFORE the final H, so the
        # measurement effectively projects the ctrl in the Y-basis.
        # This gives p0 = 1/2 + 1/2 Im(<psi|V|psi>) (averaged over target basis states).
        if imag:
            qc.sdg(0)
        qc.h(0)
        qc.measure(0, 0)

        tqc = transpile(qc, sim, optimization_level=1)
        result = sim.run(tqc, shots=shots_per_state).result()
        counts = result.get_counts()
        c0 = counts.get('0', 0)
        c1 = counts.get('1', 0)
        p0 = c0 / (c0 + c1)
        total_p0 += p0
        total_shots += (c0 + c1)

    p0_avg = total_p0 / n_states   # averaged over the uniform mixture
    # Re: 2 p0 - 1 = Re(Tr(V)/2^n).  Im: 2 p0 - 1 = Im(Tr(V)/2^n).
    return 2 * p0_avg - 1, total_shots


t0 = time.time()

# Exact Tr(V) / 4
tr_exact = np.trace(V) / 4
trL_exact = np.trace(VL) / 4
print(f"[exact] Tr(V)/4 = {tr_exact}")
print(f"[exact] Tr(V_L)/4 = {trL_exact}   (left trefoil)")

# Shot-based estimates
shots_per = 6000
print(f"\n[shots] Running Hadamard test in Qiskit AerSimulator, {shots_per} shots per basis state, 4 states = {4*shots_per} total shots per part.")
re_est, sh_re = hadamard_test_shots(V, imag=False, shots_per_state=shots_per, seed=42)
im_est, sh_im = hadamard_test_shots(V, imag=True,  shots_per_state=shots_per, seed=43)
tr_est = re_est + 1j * im_est
err = abs(tr_est - tr_exact)
print(f"[shots R-trefoil] Tr(V)/4 estimate = {tr_est}   err_abs={err:.4e}")

reL_est, _ = hadamard_test_shots(VL, imag=False, shots_per_state=shots_per, seed=44)
imL_est, _ = hadamard_test_shots(VL, imag=True,  shots_per_state=shots_per, seed=45)
trL_est = reL_est + 1j * imL_est
errL = abs(trL_est - trL_exact)
print(f"[shots L-trefoil] Tr(V_L)/4 estimate = {trL_est}   err_abs={errL:.4e}")

# Recover Tr(U) from Tr(V) = Tr(U) + 1
trU_from_shots = 4 * tr_est - 1
trU_exact = np.trace(U)
print(f"\n[recover] Tr(U) from shots = {trU_from_shots}")
print(f"[recover] Tr(U) exact       = {trU_exact}")
print(f"[recover] err_abs = {abs(trU_from_shots - trU_exact):.4e}")

# Compute Jones polynomial from Fibonacci Markov trace + Shor-Jordan formula
fTr = markov_trace_fibonacci(U, paths)
w = 3
prefactor = (-A)**(3*w) * (D**(n_strands - 1))
V_jones = prefactor * fTr

t_arg = A**(-4)
V_analytic = V_trefoil_right(t_arg)

print(f"\n[jones] V(A^-4) via Shor-Jordan Eq. 11:    {V_jones}")
print(f"[jones] V(t) analytic for right trefoil:   {V_analytic}")
print(f"[jones] |diff| = {abs(V_jones - V_analytic):.4e}")

# Left trefoil analytic check (mirror: V_{3_1_L}(t) = V_{3_1_R}(1/t))
fTrL = markov_trace_fibonacci(UL, paths)
wL = -3
prefactorL = (-A)**(3*wL) * (D**(n_strands - 1))
V_jonesL = prefactorL * fTrL
V_analyticL = V_trefoil_right(1.0 / t_arg)   # mirror trefoil
print(f"\n[jones L] V(A^-4) via Shor-Jordan Eq. 11:    {V_jonesL}")
print(f"[jones L] V(1/t) analytic for left trefoil:  {V_analyticL}")
print(f"[jones L] |diff| = {abs(V_jonesL - V_analyticL):.4e}")

dt = time.time() - t0

# Dump JSON
out = {
    "runtime_seconds": dt,
    "shots_per_state": shots_per,
    "total_shots_per_part_per_braid": 4 * shots_per,
    "software": {
        "qiskit": __import__("qiskit").__version__,
        "qiskit_aer": __import__("qiskit_aer").__version__,
    },
    "R_trefoil": {
        "exact_Tr_over_4": [tr_exact.real, tr_exact.imag],
        "shots_Tr_over_4": [tr_est.real, tr_est.imag],
        "abs_error": float(err),
        "Tr_U_from_shots": [trU_from_shots.real, trU_from_shots.imag],
        "Tr_U_exact": [trU_exact.real, trU_exact.imag],
        "V_jones_from_rep": [V_jones.real, V_jones.imag],
        "V_jones_analytic": [V_analytic.real, V_analytic.imag],
        "V_diff": float(abs(V_jones - V_analytic)),
    },
    "L_trefoil": {
        "exact_Tr_over_4": [trL_exact.real, trL_exact.imag],
        "shots_Tr_over_4": [trL_est.real, trL_est.imag],
        "abs_error": float(errL),
        "V_jones_from_rep": [V_jonesL.real, V_jonesL.imag],
        "V_jones_analytic_at_inverse_t": [V_analyticL.real, V_analyticL.imag],
        "V_diff": float(abs(V_jonesL - V_analyticL)),
    },
}
out_path = os.path.join(os.path.dirname(__file__), "dqc1_shots_results.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\n[out] wrote {out_path}")
print(f"[time] total runtime {dt:.1f}s")
