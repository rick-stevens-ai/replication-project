"""
Replication of Parker & Plenio, arXiv:quant-ph/0102136
"Entanglement Simulations of Shor's Algorithm"

Reproducible core:
- Shor's order-finding for N=15, a=2 (period r=4), pure state variant.
- 7-qubit register: 3 counting qubits (top) + 4 work qubits (bottom).
- Compute bipartite log-negativity Eneg = log2( Tr |rho^T_A| ) at each stage:
  after H^n on counting, after each controlled-U_a^{2^k}, after inverse QFT.
- Also compute the paper's summary quantity: average bipartite entanglement
  across all 2^(n-1)-1 = 63 bipartite partitionings, averaged over post-cU_a
  and post-measurement stages (their Figs. 11, 15 at epsilon = 0, pure alg).

We use log-negativity (paper's Eneg, section III C, Eq. 18) as the entanglement
measure, which is the paper's chosen bipartite measure for mixed states.

Reference values from Parker & Plenio Fig. 15 (pure, N=15, a=2, epsilon=0):
- "ent. after cU_a" curve at prob-of-finding-r ~ 0.5:  Eneg ~ 0.13-0.20
- "ent. after meas."                                      Eneg ~ 0.05-0.15
- Combined average (both classes of stages)               Eneg ~ 0.10-0.18
Values are read from Fig. 15 (log-neg vs prob. of finding r) — the pure-state
algorithm at eps=0 sits at the rightmost point (highest prob. of finding r).
"""
import json, os, itertools, math, sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Build modular exponentiation for a=2, N=15 (7-qubit register)
# Convention: qubits 0..2 = counting (LSB..MSB), qubits 3..6 = work (little endian for |y>)
# Controlled U_a^{2^k}: applies |y> -> |y * a^{2^k} mod N>
# ----------------------------------------------------------------------

N_MOD = 15
A_BASE = 2
N_COUNT = 3            # counting register
N_WORK = 4             # work register (needs 4 bits to hold values 0..14)
N_TOTAL = N_COUNT + N_WORK   # 7

def c_amod15(a: int, power: int) -> QuantumCircuit:
    """
    Controlled modular multiplication |y> -> |y * a^power mod 15>
    Standard textbook decomposition for N=15 (works only for a in {2,4,7,8,11,13}
    and the four allowed a in Qiskit's classic tutorial).  Here a=2 => order 4.

    Returns a 5-qubit circuit (1 control + 4 work) implementing the operation
    when the control qubit (index 0) is |1>.
    """
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError(f"a={a} not supported by this simple mod-15 unitary")
    U = QuantumCircuit(N_WORK, name=f"U_a^{power}")
    for _ in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(N_WORK):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    cU = U.control()
    return cU

def qft_dagger(n: int) -> QuantumCircuit:
    """Inverse QFT on n qubits (standard Qiskit-tutorial form)."""
    qc = QuantumCircuit(n, name="QFT†")
    # swaps
    for q in range(n // 2):
        qc.swap(q, n - 1 - q)
    for j in range(n):
        for m in range(j):
            qc.cp(-math.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    return qc

# ----------------------------------------------------------------------
# Entanglement helpers
# ----------------------------------------------------------------------

def log_negativity(state, part_A):
    """
    Compute log-negativity E_N = log2( ||rho^{T_A}||_1 ) on the given state
    (Statevector or DensityMatrix), where part_A is a set/list of qubit indices
    to treat as subsystem A.  Follows Parker & Plenio Eq. 18.
    """
    n = state.num_qubits
    part_B = [q for q in range(n) if q not in part_A]
    if isinstance(state, Statevector):
        rho = DensityMatrix(state)
    else:
        rho = state
    # Partial transpose over subsystem A
    rho_TA = _partial_transpose(rho, part_A)
    # trace norm = sum of singular values (Hermitian => sum |eigenvalues|)
    eigs = np.linalg.eigvalsh(rho_TA)
    trnorm = np.sum(np.abs(eigs))
    if trnorm <= 0:
        return 0.0
    val = math.log2(trnorm)
    # Numerical floor: negativity is >= 0
    return max(val, 0.0)

def _partial_transpose(rho: DensityMatrix, part_A):
    """
    Partial transpose of an n-qubit density matrix rho over subsystem A
    (a list of qubit indices).  Uses tensor reshape.
    Qiskit qubit-0 == least significant index in the flat basis.  We reshape
    into (2,)*n for row and (2,)*n for column with axis 0 => qubit (n-1).
    """
    data = np.asarray(rho.data)
    n = rho.num_qubits
    # reshape flat 2^n x 2^n -> (2,)*n row indices  (2,)*n col indices
    shape = (2,) * n + (2,) * n
    T = data.reshape(shape)
    # axes: 0..n-1 = row qubit indices (Qiskit qubit q lives at row axis (n-1-q))
    #       n..2n-1 = col qubit indices
    # For each qubit in part_A, swap its row axis and col axis
    row_axes = list(range(n))          # axis for qubit q is (n-1-q)
    col_axes = list(range(n, 2 * n))   # axis for qubit q is n + (n-1-q)
    perm = list(range(2 * n))
    for q in part_A:
        r_axis = n - 1 - q
        c_axis = n + (n - 1 - q)
        perm[r_axis], perm[c_axis] = perm[c_axis], perm[r_axis]
    T2 = T.transpose(perm)
    return DensityMatrix(T2.reshape(2 ** n, 2 ** n))

def all_bipartitions(n: int):
    """Yield all bipartitions (A, B) with 1 <= |A| < n and canonical A."""
    parts = []
    seen = set()
    all_qubits = list(range(n))
    for size in range(1, n):
        for combo in itertools.combinations(all_qubits, size):
            A = frozenset(combo)
            B = frozenset(q for q in all_qubits if q not in combo)
            key = frozenset([A, B])
            if key in seen:
                continue
            seen.add(key)
            parts.append(list(A))
    return parts

def average_bipartite_neg(state):
    """Average log-negativity across all bipartite partitionings."""
    parts = all_bipartitions(state.num_qubits)
    vals = [log_negativity(state, A) for A in parts]
    return float(np.mean(vals)), vals, parts

# ----------------------------------------------------------------------
# Build the Shor circuit and sample at every stage
# ----------------------------------------------------------------------

def build_shor_stages():
    """Build Shor's algorithm as a list of stages.  Each stage returns the
    incremental circuit to append.  Stages match the paper's 'l' index:
      stage 0 : initial |0...0>
      stage 1 : after Hadamards on counting register + init work register to |1>
      stage 2+2k : after controlled U_a^{2^k}   (k = 0 .. N_COUNT-1)
      stage 3+2k : after 'measurement' (we use partial trace to model non-selective
                   measurement of the control qubit for entanglement snapshot only;
                   for the pure-state coherent trace we skip this and just track
                   cU_a stages, which matches the paper's 'ent. after cU_a' curve)
      final stage : after inverse QFT on counting register
    We return TWO stage sequences:
      (a) coherent  — no measurement, produces post-cU_a snapshots
      (b) with non-selective measurement after each cU_a — models 'ent. after meas.'
    """
    return None  # sequence built inline in run()

def run():
    # === Coherent trace (post-cU_a snapshots + post-iQFT) ===============
    qc = QuantumCircuit(N_TOTAL)
    # Init: work register starts |0001> = |1>  (qubit 3 = LSB of work)
    qc.x(N_COUNT)                       # sets work-qubit 0 -> |1>, i.e. |y>=1
    # Hadamards on counting
    for q in range(N_COUNT):
        qc.h(q)

    snapshots = []
    def snap(label):
        sv = Statevector.from_instruction(qc)
        avg, vals, parts = average_bipartite_neg(sv)
        # Canonical bipartition = counting vs work (qubits {0,1,2} vs {3,4,5,6})
        e_cw = log_negativity(sv, [0, 1, 2])
        snapshots.append({
            "stage": label,
            "avg_bipartite_lognneg": avg,
            "counting_vs_work_lognneg": e_cw,
            "n_partitions": len(parts),
        })
        print(f"[stage {label}]  <E_neg>_bipart = {avg:.6f}   E(counting|work) = {e_cw:.6f}")

    snap("s1_after_H_and_init")

    # Controlled modular exp: qubit k (k=0..N_COUNT-1) controls U_a^{2^k}
    for k in range(N_COUNT):
        cU = c_amod15(A_BASE, 2 ** k)
        qc.append(cU, [k] + list(range(N_COUNT, N_TOTAL)))
        snap(f"s2_after_cU_a_pow_{2**k}_(k={k})")

    # Inverse QFT on counting register
    iqft = qft_dagger(N_COUNT)
    qc.append(iqft.to_gate(), list(range(N_COUNT)))
    snap("s3_after_inverse_QFT")

    # === Non-selective measurement trace (post-meas snapshots) ===========
    # Rebuild and apply a non-selective (dephasing) measurement on the counting
    # qubits after each cU_a step to model the paper's 'ent. after meas.' curve.
    # Non-selective measurement of qubit q = complete dephasing in Z basis:
    # rho -> |0><0|_q rho |0><0|_q + |1><1|_q rho |1><1|_q.
    def dephase_qubit(rho: DensityMatrix, q: int) -> DensityMatrix:
        n = rho.num_qubits
        # Build projectors on qubit q, tensored with identity elsewhere.
        # Efficient reshape trick:
        d = 2 ** n
        data = np.asarray(rho.data).copy()
        # reshape as (2,)*n x (2,)*n
        shape = (2,) * n + (2,) * n
        T = data.reshape(shape)
        r_axis = n - 1 - q
        c_axis = n + (n - 1 - q)
        # Zero out the off-diagonal blocks in qubit q
        # i.e. entries where index at r_axis != index at c_axis
        idx0 = [slice(None)] * (2 * n)
        idx1 = [slice(None)] * (2 * n)
        # Off-diagonal 0,1
        for a, b in [(0, 1), (1, 0)]:
            sl = [slice(None)] * (2 * n)
            sl[r_axis] = a
            sl[c_axis] = b
            T[tuple(sl)] = 0.0
        return DensityMatrix(T.reshape(d, d))

    print("\n--- Non-selective measurement trace ---")
    qc2 = QuantumCircuit(N_TOTAL)
    qc2.x(N_COUNT)
    for q in range(N_COUNT):
        qc2.h(q)

    rho = DensityMatrix.from_instruction(qc2)
    meas_snaps = []
    def snap_rho(label, r):
        avg, vals, parts = average_bipartite_neg(r)
        e_cw = log_negativity(r, [0, 1, 2])
        meas_snaps.append({
            "stage": label,
            "avg_bipartite_lognneg": avg,
            "counting_vs_work_lognneg": e_cw,
            "n_partitions": len(parts),
        })
        print(f"[meas-stage {label}]  <E_neg>_bipart = {avg:.6f}   "
              f"E(counting|work) = {e_cw:.6f}")

    # Apply each cU_a to rho then dephase the corresponding control qubit
    for k in range(N_COUNT):
        cU = c_amod15(A_BASE, 2 ** k)
        gate_qc = QuantumCircuit(N_TOTAL)
        gate_qc.append(cU, [k] + list(range(N_COUNT, N_TOTAL)))
        rho = rho.evolve(gate_qc)
        # non-selective measurement of control qubit k
        rho = dephase_qubit(rho, k)
        snap_rho(f"m_after_cU_a_pow_{2**k}_and_meas_k{k}", rho)

    # Final iQFT on the (already dephased) density matrix
    gate_qc = QuantumCircuit(N_TOTAL)
    gate_qc.append(iqft.to_gate(), list(range(N_COUNT)))
    rho = rho.evolve(gate_qc)
    snap_rho("m_final_after_iQFT", rho)

    # === Summary averages (mirror Fig. 11/15, epsilon=0 pure state) =====
    post_cUa_avg = np.mean([s["avg_bipartite_lognneg"]
                            for s in snapshots
                            if s["stage"].startswith("s2_after_cU_a")])
    post_meas_avg = np.mean([s["avg_bipartite_lognneg"]
                             for s in meas_snaps
                             if s["stage"].startswith("m_after_cU_a")])
    combined = 0.5 * (post_cUa_avg + post_meas_avg)

    # === Classical-simulable "no-entanglement" control ==================
    # In Shor's algorithm the entanglement is generated by the controlled
    # modular multiplications.  A classical-simulable variant that avoids
    # entanglement replaces controlled U_a^{2^k} with a plain U_a^{2^k}
    # applied unconditionally (i.e. the control is discarded), producing a
    # product state |+>^{n} tensor |y=a^{Sum 2^k} mod 15>.  We confirm the
    # avg bipartite log-negativity is zero throughout.
    print("\n--- No-entanglement control (classical-simulable variant) ---")
    qc_ctrl = QuantumCircuit(N_TOTAL)
    qc_ctrl.x(N_COUNT)
    for q in range(N_COUNT):
        qc_ctrl.h(q)
    ctrl_snaps = []
    def snap_ctrl(label):
        sv = Statevector.from_instruction(qc_ctrl)
        avg, vals, parts = average_bipartite_neg(sv)
        ctrl_snaps.append({"stage": label, "avg_bipartite_lognneg": avg})
        print(f"[ctrl {label}]  <E_neg>_bipart = {avg:.6f}")
    snap_ctrl("c1_after_H_and_init")
    for k in range(N_COUNT):
        # apply U_a^{2^k} unconditionally to the work register
        U_uncontrolled = QuantumCircuit(N_WORK)
        for _ in range(2 ** k):
            # a=2 mod 15 = cyclic-swap chain (same as inside c_amod15 without control)
            U_uncontrolled.swap(0, 1); U_uncontrolled.swap(1, 2); U_uncontrolled.swap(2, 3)
        qc_ctrl.append(U_uncontrolled.to_gate(), list(range(N_COUNT, N_TOTAL)))
        snap_ctrl(f"c2_after_uncontrolled_U_pow_{2**k}")
    qc_ctrl.append(iqft.to_gate(), list(range(N_COUNT)))
    snap_ctrl("c3_after_iQFT")

    ctrl_max = max(s["avg_bipartite_lognneg"] for s in ctrl_snaps)

    results = {
        "paper": "Parker & Plenio, arXiv:quant-ph/0102136v2",
        "problem": {"N": N_MOD, "a": A_BASE, "period_r": 4,
                    "n_counting": N_COUNT, "n_work": N_WORK, "n_total": N_TOTAL},
        "entanglement_measure": "log-negativity (log2 trace norm of rho^{T_A})",
        "num_bipartitions": 2 ** (N_TOTAL - 1) - 1,
        "coherent_snapshots": snapshots,
        "measurement_snapshots": meas_snaps,
        "control_no_entanglement_snapshots": ctrl_snaps,
        "summary": {
            "avg_post_cUa_lognneg": float(post_cUa_avg),
            "avg_post_meas_lognneg": float(post_meas_avg),
            "combined_avg_lognneg": float(combined),
            "control_max_lognneg": float(ctrl_max),
        },
        "paper_reference_from_fig15_pure_eps0": {
            "ent_after_cUa_approx": "0.13-0.20",
            "ent_after_meas_approx": "0.05-0.15",
            "combined_approx":       "0.10-0.18",
        }
    }

    out_json = os.path.join(OUT_DIR, "shor_entanglement_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print("\nWrote", out_json)
    print("\n=== SUMMARY ===")
    print(json.dumps(results["summary"], indent=2))
    return results

if __name__ == "__main__":
    run()
