"""
Analyze the K_0 operator from the p_succ=3/4 variants to determine what
single-qubit unitary is implemented, and compare to paper's headline
U = (I + i*sqrt(2) X) / sqrt(3).

Two unitaries U and V are equivalent up to left/right Clifford dressing iff
V = C_L U C_R for Clifford C_L, C_R. Since the paper only cares about the
unitary implemented (with Clifford wrap-around being "free"), we look for
Clifford-equivalence with the target.

Also: two Kraus operators K_0 = c U and K_0' = c U' with same |c|=sqrt(3)/2
implement the SAME channel up to global phase (which is unobservable).
"""
import numpy as np
from itertools import product

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
Sdg = S.conj().T
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
Tdg = T.conj().T

def kron(*mats):
    out = np.array([[1.0+0.j]])
    for m in mats: out = np.kron(out, m)
    return out

CNOT_ad = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)  # anc control, data target
CNOT_da = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]], dtype=complex)  # data control, anc target

H_a = kron(H, I2); T_a = kron(T, I2); Tdg_a = kron(Tdg, I2)
H_d = kron(I2, H); T_d = kron(I2, T); Tdg_d = kron(I2, Tdg)

def build(ops):
    W = np.eye(4, dtype=complex)
    for g in ops: W = g @ W
    return W

def kraus(W):
    K = []
    for m in (0,1):
        Km = np.zeros((2,2), dtype=complex)
        for i in (0,1):
            for j in (0,1):
                Km[i,j] = W[2*m+i, 0*2+j]
        K.append(Km)
    return K

def is_unitary(U, tol=1e-9):
    return np.allclose(U @ U.conj().T, np.eye(U.shape[0]), atol=tol)

def polar_scale(K):
    """K = c * U with U unitary. Return (c, U) where c > 0 real (absorbing phase into U)."""
    # ||K||_op = |c|
    s = np.linalg.svd(K, compute_uv=False)
    c = s[0]  # should equal |c| (all singular values equal for c*U)
    U = K / c
    return c, U

def gate_seq_labels_to_ops(label):
    """Convert a short label sequence like ['H','T','CNOT_da','Tdg','H'] on ancilla into ops."""
    raise NotImplementedError

# Variant C circuit (from previous run)
variant_C_ops = [
    H_a, H_d,
    T_a,
    CNOT_da,
    Tdg_a,
    H_a, H_d,
]
# Variant F
variant_F_ops = [
    H_a, H_d,
    T_a,
    CNOT_da,
    T_a,
    H_a, H_d,
]

TARGET_U = (I2 + 1j*np.sqrt(2)*X) / np.sqrt(3)

# Small Clifford group generators — we'll enumerate the 24-element single-qubit Clifford group
def enumerate_clifford_group():
    gens = [H, S]
    seen = {}
    def key(U):
        # Normalize global phase then round
        # Find first nonzero element and divide by its phase
        for i in range(4):
            v = U.flat[i]
            if abs(v) > 1e-9:
                U2 = U / (v / abs(v))
                break
        return tuple(np.round(U2, 6).flat)
    frontier = [np.eye(2, dtype=complex)]
    seen[key(np.eye(2, dtype=complex))] = np.eye(2, dtype=complex)
    while frontier:
        new_frontier = []
        for U in frontier:
            for g in gens:
                for W in (g @ U, U @ g):
                    k = key(W)
                    if k not in seen:
                        seen[k] = W
                        new_frontier.append(W)
        frontier = new_frontier
    return list(seen.values())

cliffords = enumerate_clifford_group()
print(f"Enumerated Clifford group: {len(cliffords)} elements (should be 24)")

def clifford_equiv(U_test, U_ref, cliffords, tol=1e-6):
    for CL in cliffords:
        for CR in cliffords:
            cand = CL @ U_ref @ CR
            # up to global phase
            # match: U_test = e^{iφ} cand
            for i in range(4):
                if abs(cand.flat[i]) > 1e-9 and abs(U_test.flat[i]) > 1e-9:
                    phase = U_test.flat[i] / cand.flat[i]
                    if abs(abs(phase)-1) > 1e-6:
                        break
                    diff = np.linalg.norm(U_test - phase*cand)
                    if diff < tol:
                        return True, phase, CL, CR, diff
                    break
    return False, None, None, None, None

for name, ops in [("C", variant_C_ops), ("F", variant_F_ops)]:
    W = build(ops)
    K0, K1 = kraus(W)
    c0, U0 = polar_scale(K0)
    c1, U1 = polar_scale(K1)
    print(f"\n=== Variant {name} ===")
    print(f"  |c_0| = {c0:.6f}   (paper: sqrt(3)/2 ≈ {np.sqrt(3)/2:.6f})")
    print(f"  |c_1| = {c1:.6f}   (paper: sqrt(1)/2 = 0.5 for identity branch)")
    print(f"  K_0 unitary part U_0 =")
    print(f"  {np.round(U0, 5)}")
    print(f"  K_1 unitary part U_1 =")
    print(f"  {np.round(U1, 5)}")
    print(f"  Is U_0 unitary? {is_unitary(U0)}")
    ok, phase, CL, CR, diff = clifford_equiv(U0, TARGET_U, cliffords)
    print(f"  U_0 Clifford-equivalent to (I+i√2 X)/√3? {ok} (diff={diff}, phase={phase})")
    if ok:
        # Identify Clifford labels
        def label(C):
            for lbl, M in [("I",I2),("H",H),("S",S),("S†",Sdg),("Z",Z),("X",X),("Y",Y),
                            ("HS",H@S),("SH",S@H),("SHS",S@H@S),("HSH",H@S@H),
                            ("SHSH",S@H@S@H),("HSHS",H@S@H@S)]:
                for phi in np.linspace(0, 2*np.pi, 8, endpoint=False):
                    if np.allclose(C, np.exp(1j*phi)*M, atol=1e-6):
                        return lbl + (f" (phase {phi:.2f})" if abs(phi)>1e-3 else "")
            return "?"
        print(f"    Left Clifford CL ≈ {label(CL)}")
        print(f"    Right Clifford CR ≈ {label(CR)}")
    # Success prob (state-independent since U_0 is unitary)
    p_succ = np.real(np.trace(K0.conj().T @ K0)) / 2
    print(f"  average success prob = {p_succ:.6f} (paper: 0.75)")
    # Also print: what is U_0^2 and its eigenphases?
    evals, _ = np.linalg.eig(U0)
    print(f"  eigenvalues of U_0: {np.round(evals, 5)} (phases: {[np.angle(e) for e in evals]})")
    tevals, _ = np.linalg.eig(TARGET_U)
    print(f"  eigenvalues of target: {np.round(tevals, 5)} (phases: {[np.angle(e) for e in tevals]})")
