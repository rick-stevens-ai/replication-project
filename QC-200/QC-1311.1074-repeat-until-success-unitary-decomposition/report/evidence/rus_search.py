"""
Brute-force search over small 2-qubit circuits (1 ancilla + 1 data) using
gates {H, T, T†, S, S†, CNOT (both directions), CZ} to find any circuit
whose K_0 (projection onto ancilla=0 after the circuit, with ancilla
starting in |0>) is exactly a scalar multiple of (I + i*sqrt(2) X)/sqrt(3)
with |scalar| = sqrt(3)/2, giving success prob 3/4.

Enforce: exactly 2 T-or-T† gates on the ancilla (per the paper's "smallest
circuit with 2 T gates"). Search all layer sequences up to length ~9.

Also allow Y-axis or Z-axis versions of the target (Clifford-equivalent):
  (I + i√2 X)/√3, (I - i√2 X)/√3, (I ± i√2 Y)/√3, (I ± i√2 Z)/√3.

This is more expensive but purely deterministic — it will either find the
circuit or prove no length-≤N circuit over this gate set works.
"""
import numpy as np
from itertools import product

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
S = np.array([[1,0],[0,1j]], dtype=complex)
Sdg = S.conj().T
T = np.array([[1,0],[0,np.exp(1j*np.pi/4)]], dtype=complex)
Tdg = T.conj().T

CNOT_ad = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
CNOT_da = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]], dtype=complex)
CZ = np.diag([1,1,1,-1]).astype(complex)

# Gate library (label, matrix, is_T_gate)
GATES = [
    ("H_a", np.kron(H, I2), False),
    ("H_d", np.kron(I2, H), False),
    ("S_a", np.kron(S, I2), False),
    ("Sdg_a", np.kron(Sdg, I2), False),
    ("S_d", np.kron(I2, S), False),
    ("Sdg_d", np.kron(I2, Sdg), False),
    ("T_a", np.kron(T, I2), True),
    ("Tdg_a", np.kron(Tdg, I2), True),
    # Note: paper says 2 T gates on the ANCILLA in Fig 8
    ("CNOT_ad", CNOT_ad, False),
    ("CNOT_da", CNOT_da, False),
    ("CZ", CZ, False),
]

def kraus(W):
    K = []
    for m in (0,1):
        Km = np.zeros((2,2), dtype=complex)
        for i in (0,1):
            for j in (0,1):
                Km[i,j] = W[2*m+i, 0*2+j]
        K.append(Km)
    return K

def is_scalar_times_unitary(K, tol=1e-9):
    s = np.linalg.svd(K, compute_uv=False)
    if len(s) < 2:
        return False, 0.0
    if abs(s[0] - s[1]) < tol:
        return True, s[0]
    return False, s[0]

candidate_targets = [
    ("(I+i√2 X)/√3", (I2 + 1j*np.sqrt(2)*X)/np.sqrt(3)),
    ("(I-i√2 X)/√3", (I2 - 1j*np.sqrt(2)*X)/np.sqrt(3)),
    ("(I+i√2 Y)/√3", (I2 + 1j*np.sqrt(2)*Y)/np.sqrt(3)),
    ("(I-i√2 Y)/√3", (I2 - 1j*np.sqrt(2)*Y)/np.sqrt(3)),
    ("(I+i√2 Z)/√3", (I2 + 1j*np.sqrt(2)*Z)/np.sqrt(3)),
    ("(I-i√2 Z)/√3", (I2 - 1j*np.sqrt(2)*Z)/np.sqrt(3)),
]

# Enumerate 24 single-qubit Cliffords for equivalence check
def enumerate_cliffords():
    gens = [H, S]
    def key(U):
        for i in range(4):
            v = U.flat[i]
            if abs(v) > 1e-9:
                U2 = U / (v / abs(v))
                break
        return tuple(np.round(U2, 6).flat)
    seen = {key(I2): I2}
    frontier = [I2]
    while frontier:
        newf = []
        for U in frontier:
            for g in gens:
                for W in (g @ U, U @ g):
                    k = key(W)
                    if k not in seen:
                        seen[k] = W
                        newf.append(W)
        frontier = newf
    return list(seen.values())

cliffords = enumerate_cliffords()

def is_clifford_equiv(U_test, U_ref, tol=1e-6):
    for CL in cliffords:
        for CR in cliffords:
            cand = CL @ U_ref @ CR
            # up to global phase
            for i in range(4):
                if abs(cand.flat[i]) > 1e-9:
                    if abs(U_test.flat[i]) < 1e-9:
                        continue
                    phase = U_test.flat[i] / cand.flat[i]
                    if abs(abs(phase)-1) > 1e-6:
                        break
                    if np.linalg.norm(U_test - phase*cand) < tol:
                        return True, phase, CL, CR
                    break
    return False, None, None, None

def search(max_len=8, max_solutions=30, verbose_every=None):
    """Iterative deepening search."""
    n = len(GATES)
    found = []
    checked = 0
    for L in range(1, max_len+1):
        print(f"Searching length {L}: {n**L} candidates...")
        for combo in product(range(n), repeat=L):
            labels = [GATES[i][0] for i in combo]
            mats = [GATES[i][1] for i in combo]
            t_count = sum(GATES[i][2] for i in combo)
            if t_count != 2:
                continue
            W = np.eye(4, dtype=complex)
            for m in mats:
                W = m @ W
            # verify W is unitary (should be, since gates are)
            K0, K1 = kraus(W)
            ok, c = is_scalar_times_unitary(K0)
            if not ok:
                continue
            # Must have |c| = sqrt(3)/2 (i.e., success prob 3/4)
            if abs(c - np.sqrt(3)/2) > 1e-6:
                continue
            U0 = K0 / c
            for tname, target in candidate_targets:
                eq, phase, CL, CR = is_clifford_equiv(U0, target)
                if eq:
                    # Check K_1 is Clifford (up to scalar sqrt(1/4)=0.5)
                    ok1, c1 = is_scalar_times_unitary(K1)
                    U1 = K1/c1 if ok1 and c1>1e-9 else None
                    k1_clifford = False
                    if U1 is not None:
                        for C in cliffords:
                            for i in range(4):
                                if abs(C.flat[i])>1e-9:
                                    if abs(U1.flat[i])<1e-9: continue
                                    ph = U1.flat[i]/C.flat[i]
                                    if abs(abs(ph)-1)>1e-6: break
                                    if np.linalg.norm(U1 - ph*C) < 1e-6:
                                        k1_clifford = True; break
                                    break
                            if k1_clifford: break
                    found.append({
                        "length": L,
                        "labels": labels,
                        "target_match": tname,
                        "|c|": c,
                        "c1": c1 if ok1 else None,
                        "K1_clifford": k1_clifford,
                    })
                    print(f"  FOUND L={L} T=2: {labels}  →  {tname}  (|c|={c:.6f}, K1_clifford={k1_clifford})")
                    if len(found) >= max_solutions:
                        return found
                    break
        if found:
            print(f"  Total found at L≤{L}: {len(found)}")
            if len(found) >= 1:
                # early exit — we have at least one
                return found
    return found

results = search(max_len=7)
print(f"\n\n=== TOTAL FOUND: {len(results)} ===")
for r in results:
    print(f"  L={r['length']}  {' '.join(r['labels'])}  →  {r['target_match']}  (K1 Clifford: {r['K1_clifford']})")
