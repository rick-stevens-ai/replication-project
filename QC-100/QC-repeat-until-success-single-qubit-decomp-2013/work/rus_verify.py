"""
RUS replication for arXiv:1311.1074 (Paetznick & Svore, 2014).

Verifies via Qiskit statevector simulation:
  - Fig. 8 (2 T-gates, single ancilla): claims (I + i sqrt(2) X)/sqrt(3) on success,
    identity on failure, Pr(success) = 3/4.
  - Fig. 9 (4 T-gates on ancilla, single ancilla, single measurement): claims
    V3 = (I + 2iZ)/sqrt(5) on success, Pr(success) = 5/8.
  - Fig. 1a (Nielsen-Chuang p.198 style, 2 ancillas, X-basis measurement):
    claims V3 = (I + 2iZ)/sqrt(5) on both-zero outcome, prob 5/8.

Approach: build the full unitary W on (n_anc+1) qubits, project onto the
"all ancillas measured zero" post-selected subspace, and read off the induced
2x2 map on the data qubit. Compare with target U up to global phase.

Qiskit uses little-endian qubit ordering — statevector indices are labelled
so that qubit 0 is the LEAST significant bit. We follow that throughout.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

I2 = np.eye(2, dtype=complex)
X  = np.array([[0,1],[1,0]], dtype=complex)
Y  = np.array([[0,-1j],[1j,0]], dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)
H  = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
Sg = np.array([[1,0],[0,1j]], dtype=complex)
T  = np.array([[1,0],[0,np.exp(1j*np.pi/4)]], dtype=complex)

V3_target = (I2 + 2j*Z)/np.sqrt(5)
Fig8_target = (I2 + 1j*np.sqrt(2)*X)/np.sqrt(3)
Fig7_target = (2*X + np.sqrt(2)*Y + Z)/np.sqrt(7)

def circuit_matrix(qc: QuantumCircuit) -> np.ndarray:
    """Return the unitary matrix of qc (little-endian: qubit 0 is LSB)."""
    return Operator(qc).data

def project_ancillas_zero(W: np.ndarray, n_data: int, n_anc: int) -> tuple[np.ndarray, float]:
    """
    Given W acting on (data ⊗ anc) with qubit ordering [data qubits ... , anc qubits ...],
    but Qiskit little-endian means qubit index k <-> bit position k in the state index.
    We build circuits with data qubit = qubit 0 (LSB), ancillas = qubits 1..n_anc.

    Compute the 2^n_data x 2^n_data block K_0 corresponding to all ancillas measured 0.
    K_0[data_out, data_in] = <0_anc, data_out | W | data_in, 0_anc>
    Returns (K_0, ||K_0||^2_avg) where the avg success probability over a Haar-random
    single-qubit input is (1/2) tr(K_0^dagger K_0).
    """
    dim = 2**(n_data + n_anc)
    assert W.shape == (dim, dim)
    K = np.zeros((2**n_data, 2**n_data), dtype=complex)
    # Little-endian: state index i decomposes as i = data_bits + (anc_bits << n_data)
    # (qubit 0 = LSB = data; qubits 1..n_anc = ancillas as higher bits).
    for d_out in range(2**n_data):
        idx_out = d_out  # anc bits = 0
        for d_in in range(2**n_data):
            idx_in = d_in
            K[d_out, d_in] = W[idx_out, idx_in]
    # Avg success prob over Haar 1-qubit input for n_data=1:
    #   E_psi <psi| K^dag K |psi> = (1/2) tr(K^dag K)
    p_succ = 0.5 * np.real(np.trace(K.conj().T @ K)) if n_data == 1 else None
    return K, p_succ

def unitary_close(A: np.ndarray, B: np.ndarray, tol=1e-8):
    """Return (is_equal_up_to_global_phase, fidelity, phase)."""
    # Find global phase from first nonzero element ratio
    idx = np.unravel_index(np.argmax(np.abs(A)), A.shape)
    if abs(B[idx]) < 1e-12:
        return False, 0.0, None
    phase = A[idx] / B[idx]
    phase /= abs(phase)
    Bp = B * phase
    diff = np.linalg.norm(A - Bp)
    # Process fidelity for two 2x2 unitaries: |tr(A^dag B)/2|^2
    if A.shape == (2,2):
        f = abs(np.trace(A.conj().T @ B) / 2)**2
    else:
        d = A.shape[0]
        f = abs(np.trace(A.conj().T @ B) / d)**2
    return (diff < tol), f, phase

# ------------------------------------------------------------------
# Fig. 8: single ancilla, target (I + i sqrt(2) X)/sqrt(3), Pr = 3/4
# Ancilla row:  H T . H . T H     (dots = CNOT controls onto data)
# Data row:     - . - . -
# Measurement in Z basis on ancilla; success = 0.
# ------------------------------------------------------------------
def fig8_circuit():
    qc = QuantumCircuit(2)  # qubit 0 = data, qubit 1 = ancilla
    a, d = 1, 0
    qc.h(a); qc.t(a)
    qc.cx(a, d)               # first CNOT anc -> data
    qc.h(a)
    qc.cx(a, d)               # second CNOT anc -> data
    qc.t(a); qc.h(a)
    return qc

# ------------------------------------------------------------------
# Fig. 9: single ancilla, target V3 = (I + 2iZ)/sqrt(5), Pr = 5/8
# Ancilla:  H T H . T† H T . H T H       (Z-basis measurement, success = 0)
# Data:     -     .      . Z
# ------------------------------------------------------------------
def fig9_circuit():
    # Figure convention: the black dots (`•`) drawn on the DATA row are the CONTROLS,
    # and the CNOT targets are on the ancilla row. So the CX direction is data → ancilla.
    # The explicit `Z` on the data at the very end is *not* part of the success branch on
    # our reading (see rus_fig9_search.py) – it appears to be a conditional recovery.
    # Without it, K/√p = V3 up to global phase e^{-iπ/4} exactly. See failure_analysis.md.
    qc = QuantumCircuit(2)
    a, d = 1, 0
    qc.h(a); qc.t(a); qc.h(a)
    qc.cx(d, a)                # first control-on-data CNOT
    qc.tdg(a); qc.h(a); qc.t(a)
    qc.cx(d, a)                # second control-on-data CNOT
    qc.h(a); qc.t(a); qc.h(a)
    return qc

# ------------------------------------------------------------------
# Fig. 1a: two ancillas |+>, X-basis measurement, both zero => V3.
# From figure:
#   anc1 |+>  •           •     Xmeas
#   anc2 |+>  •           •     Xmeas
#   data|ψ>       S         Z
# Interpretation: two controlled operations, each controlled by BOTH ancillas
# (i.e. Toffoli-style targets). First Toffoli target = S on data, second Toffoli target = Z on data.
# In Fig 1a of the paper this is the NC00 pp.198 style: controlled-S and controlled-Z with
# both ancillas as controls (Toffolis with different target gates).
# X-basis measurement = H then Z-basis measurement, success = 00.
# ------------------------------------------------------------------
def fig1a_circuit():
    qc = QuantumCircuit(3)  # qubit 0 = data, qubits 1,2 = ancillas
    a1, a2, d = 1, 2, 0
    # Prepare |+>|+> on the two ancillas
    qc.h(a1); qc.h(a2)
    # Toffoli-style: controlled-controlled-S on data with controls a1,a2
    # controlled-S = phase gate applied when both controls are 1
    # We build C1C2-S via Toffoli + T decomposition; but for verification we can just
    # use Operator on an ideal ccS. Qiskit >=0.44 has ccz/mcx; we compose ccS via mcp(pi/2, ...).
    qc.mcp(np.pi/2, [a1, a2], d)   # controlled-controlled-S (phase pi/2 on |111>)
    # Then controlled-controlled-Z on data (phase pi on |111>)
    qc.mcp(np.pi,   [a1, a2], d)
    # X-basis measurement on ancillas: apply H before Z-basis projection
    qc.h(a1); qc.h(a2)
    return qc

# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------
def analyse(name: str, qc: QuantumCircuit, n_anc: int, target: np.ndarray, p_expect: float):
    W = circuit_matrix(qc)
    K, p_succ = project_ancillas_zero(W, n_data=1, n_anc=n_anc)
    ok, fid, phase = unitary_close(K/np.sqrt(p_succ) if p_succ > 0 else K, target)
    return {
        "name": name,
        "K_matrix": K.tolist(),
        "K_normalised": (K/np.sqrt(p_succ)).tolist() if p_succ > 0 else None,
        "target": target.tolist(),
        "p_success_measured": float(p_succ),
        "p_success_paper":    float(p_expect),
        "delta_prob":         float(abs(p_succ - p_expect)),
        "process_fidelity":   float(fid),
        "unitary_equal_upto_phase": bool(ok),
        "global_phase": complex(phase).real if phase is not None else None,
    }

def json_default(o):
    if isinstance(o, complex):
        return {"re": o.real, "im": o.imag}
    raise TypeError(str(type(o)))

def stringify(x):
    """Recursively convert complex numbers to strings for JSON serialisation."""
    if isinstance(x, complex):
        return f"{x.real:+.6f}{x.imag:+.6f}j"
    if isinstance(x, list):
        return [stringify(v) for v in x]
    if isinstance(x, dict):
        return {k: stringify(v) for k, v in x.items()}
    return x

if __name__ == "__main__":
    import json, sys

    results = {}
    for name, qc, n_anc, tgt, p in [
        ("Fig8",  fig8_circuit(),  1, Fig8_target, 3/4),
        ("Fig9",  fig9_circuit(),  1, V3_target,   5/8),
        ("Fig1a", fig1a_circuit(), 2, V3_target,   5/8),
    ]:
        r = analyse(name, qc, n_anc, tgt, p)
        results[name] = r
        print(f"=== {name} ===")
        print(f"  target unitary          = {tgt.round(4).tolist()}")
        print(f"  induced (unnorm) K      =")
        for row in np.array(r["K_matrix"]):
            print(f"    {[complex(v).real for v in row]}, imag {[complex(v).imag for v in row]}")
        print(f"  Pr(success) measured    = {r['p_success_measured']:.6f}")
        print(f"  Pr(success) paper       = {r['p_success_paper']:.6f}")
        print(f"  |Δp|                    = {r['delta_prob']:.2e}")
        print(f"  Process fidelity (Ktilde vs target) = {r['process_fidelity']:.6f}")
        print(f"  Unitary equal up to global phase?  = {r['unitary_equal_upto_phase']}")
        print()

    # Serialize with complex-safe stringify
    out = {k: stringify(v) for k, v in results.items()}
    with open("rus_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote rus_results.json")
