"""
Fast refinement using raw numpy state-vector simulation.

Same MoG-VQE circuit family (Fig 2a generalized-CNOT blocks). Bypasses PennyLane's tracing
overhead by building the Hamiltonian matrix once, then applying gates as dense/sparse
matrix multiplications on the 2^4 = 16-dim state vector. This makes each energy evaluation
microseconds instead of milliseconds → 100-1000x speedup.
"""

import json
import os
import random
import time
import numpy as np
import pennylane as qml
from pennylane import qchem
from scipy.optimize import minimize

random.seed(2025)
np.random.seed(2025)

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(OUT, "report", "evidence")
os.makedirs(EVID, exist_ok=True)

symbols = ["H", "H"]
coords = np.array([[0.0, 0.0, -0.37], [0.0, 0.0, 0.37]])
H, n_qubits = qchem.molecular_hamiltonian(symbols, coords, charge=0, mult=1, basis="sto-3g", method="pyscf")
Hmat = qml.matrix(H, wire_order=range(n_qubits))
E_FCI = float(np.linalg.eigvalsh(Hmat)[0])
CHEM_ACC = 1.6e-3
print(f"FCI={E_FCI:.8f}, chem_acc={CHEM_ACC}", flush=True)

# HF state |1100> in JW convention (wire 0 is leftmost bit → basis index 12)
def hf_statevec():
    v = np.zeros(2**n_qubits, dtype=complex)
    # convention: qml.BasisState([1,1,0,0], wires=[0,1,2,3]) prepares |1100>
    # in binary with wire 0 most significant: bit string 1100 → integer 12
    idx = int("1100", 2)  # = 12
    v[idx] = 1.0
    return v

# Verify HF energy
psi_hf = hf_statevec()
E_HF = float(np.real(psi_hf.conj() @ Hmat @ psi_hf))
print(f"HF energy: {E_HF:.8f}", flush=True)

# Gate matrices (2x2)
def RY(a):
    c, s = np.cos(a/2), np.sin(a/2)
    return np.array([[c, -s], [s, c]], dtype=complex)

def RZ(a):
    return np.array([[np.exp(-1j*a/2), 0], [0, np.exp(1j*a/2)]], dtype=complex)


def apply_1q(state, U, q, n):
    """Apply 1-qubit gate U on wire q (wire 0 = most significant)."""
    # reshape state as tensor of shape [2]*n and swap wire q to axis 0
    s = state.reshape([2] * n)
    # Move axis q to front
    s = np.moveaxis(s, q, 0)  # shape (2, ...)
    s = s.reshape(2, -1)
    s = U @ s
    s = s.reshape([2] * n)
    s = np.moveaxis(s, 0, q)
    return s.reshape(-1)


def apply_cnot(state, ctrl, tgt, n):
    """Apply CNOT with control=ctrl, target=tgt."""
    s = state.reshape([2] * n)
    # For control=1, flip target
    # Move ctrl to axis 0, tgt to axis 1
    s = np.moveaxis(s, [ctrl, tgt], [0, 1])
    s = s.copy()
    # index [1, :, ...] target part swap [0]<->[1]
    tmp = s[1, 0].copy()
    s[1, 0] = s[1, 1]
    s[1, 1] = tmp
    s = np.moveaxis(s, [0, 1], [ctrl, tgt])
    return s.reshape(-1)


def circuit_state(topology, theta, n=4):
    """Build the state vector for a given topology and angles."""
    psi = hf_statevec()
    # single-qubit init layer: RY on each wire
    for q in range(n):
        psi = apply_1q(psi, RY(theta[q]), q, n)
    idx = n
    for c, t in topology:
        a, b, cc, d, e = theta[idx:idx+5]
        psi = apply_1q(psi, RY(a), c, n)
        psi = apply_1q(psi, RY(b), t, n)
        psi = apply_1q(psi, RZ(cc), t, n)
        psi = apply_cnot(psi, c, t, n)
        psi = apply_1q(psi, RY(d), c, n)
        psi = apply_1q(psi, RY(e), t, n)
        idx += 5
    return psi


def energy_fn(topology):
    def loss(theta):
        psi = circuit_state(topology, theta)
        return float(np.real(psi.conj() @ Hmat @ psi))
    return loss


# Smoke test
tp = [(0, 1), (2, 3)]
loss = energy_fn(tp)
theta_test = np.zeros(4 + 5*len(tp))
t0 = time.time()
for _ in range(1000):
    _ = loss(theta_test)
print(f"1000 evals of 2-block circuit: {time.time()-t0:.3f}s", flush=True)


def optimize_topology(topology, restarts=8, maxiter=500):
    loss = energy_fn(topology)
    n = 4 + 5 * len(topology)
    best_e, best_x = np.inf, None
    for r in range(restarts):
        x0 = np.random.randn(n) * (0.15 + 0.1 * r)
        res = minimize(loss, x0, method="L-BFGS-B",
                       options={"maxiter": maxiter, "ftol": 1e-10, "gtol": 1e-8})
        if res.fun < best_e:
            best_e, best_x = float(res.fun), res.x
    return best_e, best_x


QUBIT_PAIRS = [(i, j) for i in range(n_qubits) for j in range(n_qubits) if i != j]

results = {}
for k in [2, 3, 4]:
    print(f"\n=== k={k} CNOT blocks ===", flush=True)
    N = 60 if k <= 3 else 40
    seen = set(); ca_hits = []
    per_k_best = np.inf; per_k_best_topo = None; per_k_best_energy = np.inf
    t_start = time.time()
    for i in range(N):
        while True:
            topo = tuple(random.choice(QUBIT_PAIRS) for _ in range(k))
            if topo not in seen: seen.add(topo); break
        e, x = optimize_topology(list(topo), restarts=8, maxiter=400)
        err = e - E_FCI
        if err < per_k_best:
            per_k_best = err; per_k_best_topo = topo; per_k_best_energy = e
        if err < CHEM_ACC:
            ca_hits.append((topo, e, err))
        tag = "★" if err < CHEM_ACC else " "
        if i % 5 == 0 or err < CHEM_ACC:
            elapsed = time.time() - t_start
            print(f"  [{i+1:3d}/{N}] {tag} topo={topo}  E={e:.6f}  err={err:.3e}  ({elapsed:.0f}s)", flush=True)
    results[k] = {
        "n_topologies_tried": N,
        "best_err": per_k_best,
        "best_energy": per_k_best_energy,
        "best_topology": [list(p) for p in per_k_best_topo] if per_k_best_topo else None,
        "chem_acc_hits": [
            {"topology": [list(p) for p in t], "energy_Ha": e, "abs_error_Ha": err}
            for t, e, err in ca_hits
        ],
        "n_chem_acc": len(ca_hits),
        "wall_time_s": time.time() - t_start,
    }
    print(f"k={k} summary: best err={per_k_best:.3e}, {len(ca_hits)}/{N} circuits reached chem-acc")

min_k_ca = None
for k in sorted(results):
    if results[k]["n_chem_acc"] > 0:
        min_k_ca = k; break

with open(os.path.join(EVID, "mog_vqe_h2_refined.json"), "w") as f:
    json.dump({
        "chem_acc_Ha": CHEM_ACC, "E_FCI_Ha": E_FCI, "E_HF_Ha": E_HF,
        "per_k_results": results, "min_k_reaching_chem_acc": min_k_ca,
    }, f, indent=2, default=str)

print(f"\n=== REFINED RESULT ===")
print(f"Minimum CNOT count reaching chemical accuracy: {min_k_ca}")
if min_k_ca is not None:
    r = results[min_k_ca]
    print(f"  Number of CA-reaching circuits at k={min_k_ca}: {r['n_chem_acc']}/{r['n_topologies_tried']}")
    print(f"  Best circuit at k={min_k_ca}: topology={r['best_topology']}, E={r['best_energy']:.8f}, err={r['best_err']:.3e}")
