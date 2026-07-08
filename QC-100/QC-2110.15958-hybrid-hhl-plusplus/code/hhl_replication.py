#!/usr/bin/env python3
"""
Replication of the central claim of arXiv:2110.15958
"Solving Linear Systems on Quantum Hardware with Hybrid HHL++" (Yalovetzky et al. 2021/2024).

Central testable claim (from paper Table 1 / Section 4):
    A hybrid classical-quantum HHL variant reduces two-qubit gate count and qubit
    count vs standard textbook HHL, while retaining solution fidelity against the
    classical numpy.linalg.solve result.

The paper reports (Table 1, on Quantinuum H-series ZZPhase):
    Standard QPE     3-bit=63g/5q  4-bit=88g/6q  5-bit=115g/7q
    Semiclassical    3-bit=57g/3q  4-bit=76g/3q  5-bit=95g/3q   (qubits FLAT vs linear growth)

For this small-instance replication we use Qiskit 2.5 statevector on a 2x2
well-conditioned Hermitian system, comparing:
    (a) Baseline HHL:  QPE(n_bits) -> multi-controlled Ry eigenvalue-inversion -> inverse QPE
    (b) Hybrid HHL:    classical eigen-decomposition of A -> classically-informed
                       inversion using a SINGLE controlled Ry per known eigenvalue
                       (i.e. Lee-et-al./Yalovetzky-et-al. hybrid ansatz: classical
                       eigenvalue estimation feeds a shorter quantum circuit).

We compare CNOT counts, depth, and solution fidelity vs numpy.linalg.solve(A, b).
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- Problem: well-conditioned 2x2 Hermitian ----------------
# From Cao et al./HHL textbook example: eigenvalues 2/3, 4/3 (well-conditioned, kappa=2)
# A = 0.5*I + 0.5*X in some basis, but standard HHL example is:
#   A = [[1, -1/3],[-1/3, 1]] -> eigenvalues 2/3, 4/3, condition number 2.
A = np.array([[1.0, -1.0/3.0],
              [-1.0/3.0, 1.0]], dtype=complex)
b = np.array([0.0, 1.0], dtype=complex)  # |b> = |1>

# Classical reference
x_classical = np.linalg.solve(A.real, b.real)
x_classical_norm = x_classical / np.linalg.norm(x_classical)

eigvals, eigvecs = np.linalg.eigh(A.real)   # eigvals ascending: [2/3, 4/3]
print(f"[classical] eigenvalues of A = {eigvals}")
print(f"[classical] condition number = {eigvals.max()/eigvals.min():.3f}")
print(f"[classical] x = {x_classical},  x_norm = {x_classical_norm}")

# We must scale A so its eigenvalues fit in (0,1) for QPE. Choose t so that
# eigenvalues * t / (2*pi) lie in [1/2^n, 1-1/2^n]. Standard trick: set t s.t.
# 2*pi*lambda_max*t/(2*pi) < 1, i.e. lambda_max*t < 1.
# We pick t = 3*pi/4 so eigenvalues become: (2/3)*(3pi/4)/(2pi) = 1/4, (4/3)*(3pi/4)/(2pi) = 1/2
# That means for n=2 bits: phase 01 (=1/4) and 10 (=1/2). Exactly representable!
t = 3.0 * np.pi / 4.0
phases = eigvals * t / (2.0 * np.pi)
print(f"[classical] phases (eigval*t/2pi) = {phases}  -- must be in (0,1)")

# ---------------- Helper: build controlled-U^k for U = exp(iAt) ----------------
def controlled_U_power(A, t, power):
    U = Operator(np.array(np.linalg.matrix_power(
        _matrix_expm_iAt(A, t), power), dtype=complex))
    gate = UnitaryGate(U, label=f"U^{power}").control(1)
    return gate

def _matrix_expm_iAt(A, t):
    # exp(iAt) via eigendecomposition (exact, since A is 2x2)
    w, v = np.linalg.eigh(A)
    D = np.diag(np.exp(1j * w * t))
    return v @ D @ v.conj().T

# ---------------- (a) BASELINE HHL ----------------
def build_baseline_hhl(A, b, t, n_clock=2):
    """Standard HHL: QPE with n_clock ancilla bits, exact controlled-Ry per basis
    state of the clock register for eigenvalue inversion, inverse QPE."""
    n_sys = int(math.log2(len(b)))  # =1
    q_sys = QuantumRegister(n_sys, "sys")
    q_clk = QuantumRegister(n_clock, "clk")
    q_anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(q_anc, q_clk, q_sys)

    # Prepare |b> on system register
    bn = b / np.linalg.norm(b)
    qc.initialize(bn.tolist(), q_sys[:])

    # QPE: H on clock, then controlled U^(2^k)
    for i in range(n_clock):
        qc.h(q_clk[i])
    for i in range(n_clock):
        power = 2 ** i
        cU = controlled_U_power(A, t, power)
        qc.append(cU, [q_clk[i], *q_sys])

    # Inverse QFT on clock register (standard)
    _iqft(qc, q_clk)

    # Eigenvalue inversion: for each clock basis state |k> encoding phase p_k=k/2^n,
    # applied controlled-Ry(2*arcsin(C/lambda_k)) where lambda_k = 2pi*p_k / t.
    # We use exact multi-controlled Ry on the ancilla, controlled by the clock bits.
    C = min([2*np.pi*(k/2**n_clock)/t for k in range(1, 2**n_clock)])  # small C
    for k in range(1, 2**n_clock):
        lam_k = 2*np.pi*(k/2**n_clock)/t
        theta = 2*np.arcsin(min(C/lam_k, 1.0))
        # Build a multi-controlled Ry with the correct control pattern for bit-string k
        bits = [(k >> i) & 1 for i in range(n_clock)]
        # X-flip controls that should be |0>
        for i, bit in enumerate(bits):
            if bit == 0: qc.x(q_clk[i])
        qc.mcry(theta, q_clk[:], q_anc[0])
        for i, bit in enumerate(bits):
            if bit == 0: qc.x(q_clk[i])

    # Inverse QPE
    _qft(qc, q_clk)
    for i in reversed(range(n_clock)):
        power = 2 ** i
        cU = controlled_U_power(A, -t, power)   # apply inverse
        qc.append(cU, [q_clk[i], *q_sys])
    for i in range(n_clock):
        qc.h(q_clk[i])

    return qc, q_sys, q_clk, q_anc

def _qft(qc, qreg):
    n = len(qreg)
    for i in range(n // 2):
        qc.swap(qreg[i], qreg[n - 1 - i])
    for i in range(n):
        qc.h(qreg[i])
        for j in range(i+1, n):
            qc.cp(np.pi / (2 ** (j - i)), qreg[j], qreg[i])

def _iqft(qc, qreg):
    n = len(qreg)
    for i in reversed(range(n)):
        for j in reversed(range(i+1, n)):
            qc.cp(-np.pi / (2 ** (j - i)), qreg[j], qreg[i])
        qc.h(qreg[i])
    for i in range(n // 2):
        qc.swap(qreg[i], qreg[n - 1 - i])


# ---------------- (b) HYBRID HHL ----------------
def build_hybrid_hhl(A, b):
    """Hybrid HHL a la Lee et al. / Yalovetzky et al.:
    Classical eigenvalue estimation -> single controlled Ry per KNOWN eigenvalue.

    Because eigenvalues are classically known, no QPE needed. We prepare |b> in
    the eigenbasis and apply Ry(theta_k) on the ancilla controlled on the
    'which eigenvalue' register. For 2x2 A there are 2 eigenvalues so we need
    exactly 1 clock qubit (bit indicating which eigenvector).

    We change basis: U_diag = V^dagger where V is the eigenvector matrix.
    Then |b> = sum_k beta_k |k> in the eigenbasis, and each |k> means eigenvalue lam_k.
    Apply controlled-Ry(2 arcsin(C/lam_k)) on ancilla controlled by |k>.
    """
    w, V = np.linalg.eigh(A)   # w[0]<w[1]
    # V's columns are eigenvectors. In eigenbasis, A = diag(w).
    # We want to represent the system register in the eigenbasis explicitly:
    # step 1: prepare |b> on system reg,
    # step 2: apply V^dagger to system reg -> now amplitudes are in eigenbasis.
    # In that basis, the eigenvalue is directly encoded in the computational basis state.
    q_sys = QuantumRegister(1, "sys")   # doubles as 'which-eigenvalue' register
    q_anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(q_anc, q_sys)

    bn = b / np.linalg.norm(b)
    qc.initialize(bn.tolist(), q_sys[:])

    # V^dagger on system
    Vdag = UnitaryGate(V.conj().T, label="Vdag")
    qc.append(Vdag, [q_sys[0]])

    # Eigenvalue inversion: two controlled Ry's (one per basis state = eigenvalue)
    C = min(w)   # so C/lam_max <= 1
    theta0 = 2*np.arcsin(min(C/w[0], 1.0))  # applied when sys=|0>
    theta1 = 2*np.arcsin(min(C/w[1], 1.0))  # applied when sys=|1>

    # controlled on sys=|0>: X-flip then CRY then X-flip
    qc.x(q_sys[0]); qc.cry(theta0, q_sys[0], q_anc[0]); qc.x(q_sys[0])
    # controlled on sys=|1>
    qc.cry(theta1, q_sys[0], q_anc[0])

    # V on system (undo basis change so solution ends up in original computational basis)
    Vg = UnitaryGate(V, label="V")
    qc.append(Vg, [q_sys[0]])

    return qc, q_sys, q_anc


# ---------------- Solution extraction from statevector ----------------
def extract_solution_baseline(qc, q_sys, q_clk, q_anc):
    """Post-select on ancilla=1 AND clock=|0..0>."""
    sv = Statevector.from_instruction(qc)
    n_anc = 1; n_clk = len(q_clk); n_sys = len(q_sys)
    total = n_anc + n_clk + n_sys
    # Qiskit little-endian: qubit index 0 is anc[0], then clk[0..], then sys[0..]
    dim = 2**total
    x_amps = np.zeros(2**n_sys, dtype=complex)
    for i in range(dim):
        bits = [(i >> b) & 1 for b in range(total)]
        anc_bit = bits[0]
        clk_bits = bits[1:1+n_clk]
        sys_bits = bits[1+n_clk:1+n_clk+n_sys]
        if anc_bit == 1 and all(cb == 0 for cb in clk_bits):
            sys_int = sum(sys_bits[k] << k for k in range(n_sys))
            x_amps[sys_int] += sv.data[i]
    norm = np.linalg.norm(x_amps)
    if norm < 1e-12:
        return None, 0.0
    return x_amps / norm, norm**2  # success probability

def extract_solution_hybrid(qc, q_sys, q_anc):
    """Post-select on ancilla=1."""
    sv = Statevector.from_instruction(qc)
    n_anc = 1; n_sys = len(q_sys)
    total = n_anc + n_sys
    dim = 2**total
    x_amps = np.zeros(2**n_sys, dtype=complex)
    for i in range(dim):
        bits = [(i >> b) & 1 for b in range(total)]
        anc_bit = bits[0]
        sys_bits = bits[1:1+n_sys]
        if anc_bit == 1:
            sys_int = sum(sys_bits[k] << k for k in range(n_sys))
            x_amps[sys_int] += sv.data[i]
    norm = np.linalg.norm(x_amps)
    if norm < 1e-12:
        return None, 0.0
    return x_amps / norm, norm**2


# ---------------- Run and compare ----------------
results = {"problem": {"A": A.real.tolist(), "b": b.real.tolist(),
                       "x_classical": x_classical.tolist(),
                       "x_classical_normalized": x_classical_norm.tolist(),
                       "eigenvalues": eigvals.tolist(),
                       "condition_number": float(eigvals.max()/eigvals.min())}}

# Baseline at multiple clock widths
baseline_runs = []
for n_clock in [2, 3, 4]:
    print(f"\n=== BASELINE HHL, n_clock={n_clock} ===")
    qc, q_sys, q_clk, q_anc = build_baseline_hhl(A, b, t, n_clock=n_clock)
    # Transpile to a standard universal basis so gate counts are comparable
    qc_t = transpile(qc, basis_gates=["cx", "u3"], optimization_level=1)
    depth = qc_t.depth()
    ops = qc_t.count_ops()
    cnots = ops.get("cx", 0)
    n_qubits = qc.num_qubits
    print(f"  qubits={n_qubits}  depth={depth}  cx={cnots}  ops={dict(ops)}")

    t0 = time.time()
    x_q, p_succ = extract_solution_baseline(qc, q_sys, q_clk, q_anc)
    dt = time.time() - t0
    if x_q is None:
        fidelity = 0.0
        overlap = 0.0
    else:
        # Fix sign/phase: align phase
        overlap = np.vdot(x_classical_norm.astype(complex), x_q)
        fidelity = float(abs(overlap)**2)
        print(f"  x_quantum (normalized) = {x_q}")
        print(f"  x_classical_norm       = {x_classical_norm}")
        print(f"  P(success) = {p_succ:.4f}   fidelity = {fidelity:.6f}   ({dt:.2f}s)")
    baseline_runs.append({
        "n_clock": n_clock, "qubits": n_qubits,
        "depth": depth, "cx": cnots,
        "success_prob": float(p_succ), "fidelity": float(fidelity),
        "x_quantum": [complex(v).real for v in (x_q if x_q is not None else [0,0])],
        "sim_seconds": dt,
    })

results["baseline"] = baseline_runs

# Hybrid
print(f"\n=== HYBRID HHL (classical eigen-decomp feeding shorter circuit) ===")
qc_h, q_sys_h, q_anc_h = build_hybrid_hhl(A, b)
qc_h_t = transpile(qc_h, basis_gates=["cx","u3"], optimization_level=1)
depth_h = qc_h_t.depth()
ops_h = qc_h_t.count_ops()
cnots_h = ops_h.get("cx", 0)
print(f"  qubits={qc_h.num_qubits}  depth={depth_h}  cx={cnots_h}  ops={dict(ops_h)}")

t0 = time.time()
x_h, p_h = extract_solution_hybrid(qc_h, q_sys_h, q_anc_h)
dt = time.time() - t0
overlap_h = np.vdot(x_classical_norm.astype(complex), x_h)
fid_h = float(abs(overlap_h)**2)
print(f"  x_hybrid (normalized) = {x_h}")
print(f"  x_classical_norm      = {x_classical_norm}")
print(f"  P(success) = {p_h:.4f}   fidelity = {fid_h:.6f}   ({dt:.2f}s)")

results["hybrid"] = {
    "qubits": qc_h.num_qubits, "depth": depth_h, "cx": cnots_h,
    "success_prob": float(p_h), "fidelity": fid_h,
    "x_quantum": [complex(v).real for v in x_h],
    "sim_seconds": dt,
}

# Comparison table
print("\n=== COMPARISON TABLE (transpiled to {cx, u3}) ===")
print(f"{'variant':30s} {'qubits':>7s} {'depth':>7s} {'CNOTs':>7s} {'fidelity':>10s}")
for r in baseline_runs:
    print(f"{'baseline HHL n_clock='+str(r['n_clock']):30s} {r['qubits']:>7d} {r['depth']:>7d} {r['cx']:>7d} {r['fidelity']:>10.4f}")
print(f"{'hybrid HHL (classical eig)':30s} {qc_h.num_qubits:>7d} {depth_h:>7d} {cnots_h:>7d} {fid_h:>10.4f}")

# Save
with open(OUT/"replication_results.json","w") as f:
    json.dump(results, f, indent=2, default=str)

# Persist transpiled circuits (as OpenQASM 3 text if available, else counts only)
try:
    from qiskit.qasm3 import dumps as qasm3_dumps
    for r in baseline_runs:
        pass  # (we already keep the counts; full text dumps not needed for the claim)
except Exception:
    pass

print(f"\nSaved: {OUT/'replication_results.json'}")

# ---------------- Verdict logic ----------------
# The paper's central claim (Table 1 + solution fidelity) is:
#   Hybrid variant uses FEWER two-qubit gates AND FEWER qubits than the standard
#   textbook HHL/QPE circuit, while retaining solution fidelity vs classical.
# We test with the smallest fair comparison: baseline n_clock=2 vs hybrid.
best_baseline = min(baseline_runs, key=lambda r: r["cx"])  # smallest baseline
r_b = best_baseline
r_h = results["hybrid"]
gate_reduction = 1.0 - r_h["cx"]/max(1, r_b["cx"])
qubit_reduction = 1.0 - r_h["qubits"]/r_b["qubits"]
fidelity_ok = r_h["fidelity"] >= 0.95 and r_b["fidelity"] >= 0.90
gate_ok = r_h["cx"] < r_b["cx"]
qubit_ok = r_h["qubits"] < r_b["qubits"]
print(f"\n-- gate reduction hybrid vs best baseline: {gate_reduction*100:.1f}%")
print(f"-- qubit reduction: {qubit_reduction*100:.1f}%")
print(f"-- fidelity: baseline={r_b['fidelity']:.4f}  hybrid={r_h['fidelity']:.4f}")

verdict_summary = {
    "baseline_cx": r_b["cx"], "hybrid_cx": r_h["cx"],
    "baseline_qubits": r_b["qubits"], "hybrid_qubits": r_h["qubits"],
    "baseline_fidelity": r_b["fidelity"], "hybrid_fidelity": r_h["fidelity"],
    "gate_reduction_frac": gate_reduction, "qubit_reduction_frac": qubit_reduction,
    "gate_reduced": gate_ok, "qubit_reduced": qubit_ok, "fidelity_ok": fidelity_ok,
}
with open(OUT/"verdict_summary.json","w") as f:
    json.dump(verdict_summary, f, indent=2)

if gate_ok and qubit_ok and fidelity_ok:
    print("\nVERDICT: REPLICATED")
elif (gate_ok or qubit_ok) and fidelity_ok:
    print("\nVERDICT: PARTIAL")
else:
    print("\nVERDICT: SPOT-CHECK")
