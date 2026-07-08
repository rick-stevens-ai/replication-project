"""
Independent replication (small-instance) of arXiv:2208.04100:
"Noise-resilient phase estimation with randomized compiling"
Gu, Ma, Forcellini, Liu (2022/2023).

Core claim reproduced here:
  Under COHERENT (unitary over-rotation) noise of angle theta, the phase-estimation
  error scales LINEARLY with theta in the bare (unmitigated) circuit.
  With Randomized Compiling (Pauli twirling of noise), coherent noise is converted
  to a stochastic Pauli channel and the phase-estimation error scales as a HIGHER
  POWER of theta (paper reports ~theta^1 vs ~theta^2.73 for their Fig 3(a) fit).

Small-instance design (single-qubit, tractable on CPU):
  - Ideal unitary U = R_Z(2*phi_true)   with phi_true known.
  - Robust/iterative phase estimation: circuit_L = H . U^L . H, measure Z.
      P(0|L) = cos^2(phi * L)   (ideal, for R_Z(2*phi) sandwiched by Hadamards).
      Actually H R_Z(2*phi) H = R_X(2*phi), so H R_Z(2*phi)^L H = R_X(2*phi*L),
      and starting from |0>, <Z> = cos(2*phi*L).
    So P(0|L) = (1 + cos(2*phi*L))/2.
  - Coherent noise: each U is replaced by U * R_Z(eps), i.e. an over-rotation of eps
    per gate (matches paper's Sec IV S.I. noise model: Z-rotation error per single-qubit gate).
  - Randomized Compiling (RC): sample Pauli P_k in {I,X,Y,Z} independently for each
    of the L cycles. Replace the noisy gate G_k = U*R_Z(eps) by P_k G_k P_k, and
    correct by inserting a compensating (P_k @ P_{k-1}) rotation on the idle single-qubit
    identity slot between cycles (absorbed into a virtual "easy" Clifford cycle).
    For a chain of L noisy gates the twirled channel converges (in Nr average) to a
    stochastic Pauli channel; this removes the systematic phase bias.

Estimator: standard "robust phase estimation" (Kimmel-Low-Yoder style) via a set of
increasing L values (L=1,2,4,8,...,Lmax) and majority-vote / arctan on empirical cos.
We use the simple least-squares fit of cos(2*phi*L) to averaged P(0|L) since we only
compare BIAS scaling with noise angle.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Operator
import json, os, time, sys

np.random.seed(20260703)

# -------- experiment parameters --------
PHI_TRUE = 0.37123456                      # rad, arbitrary non-trivial single-qubit phase
L_LIST   = [1, 2, 4, 8, 16, 32, 64, 100]   # PE circuit depths (matches paper Lmax=100 order-finding)
NS_PER_CIRCUIT = 4000                      # shots per bare circuit
NR = 20                                     # number of random compilations (paper uses Nr=20)
NOISE_ANGLES = [0.003, 0.006, 0.01, 0.02, 0.04, 0.08, 0.15]   # coherent over-rotation eps (rad)
SEED_SIM = 42

sim = AerSimulator(method="statevector", seed_simulator=SEED_SIM)

# Pauli label -> unitary
PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0,1],[1,0]], dtype=complex),
    "Y": np.array([[0,-1j],[1j,0]], dtype=complex),
    "Z": np.array([[1,0],[0,-1]], dtype=complex),
}
PAULI_LABELS = ["I","X","Y","Z"]

def rz(angle):
    return np.array([[np.exp(-1j*angle/2), 0],
                     [0, np.exp( 1j*angle/2)]], dtype=complex)

def build_circuit_bare(L, eps):
    """H . (U * Rz(eps))^L . H, measure in Z basis (== X basis of the H-sandwiched ideal U)."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    for _ in range(L):
        # ideal U = Rz(2*PHI_TRUE), noise Rz(eps) applied per gate
        qc.rz(2*PHI_TRUE, 0)
        qc.rz(eps, 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def build_circuit_rc(L, eps, rng):
    """Randomized-compiled version: independent Pauli twirl on each noisy gate,
    with compensating boundary Paulis so the net LOGICAL action equals bare circuit's ideal.
    Implementation: because U_ideal = Rz(2*phi) is diagonal in Z, X U_ideal X = Rz(-2*phi),
    which flips the phase; naive twirl over all 4 Paulis would kill signal.
    Correct RC construction: sample P_k, insert P_k^dagger on the LEFT and P_k on the RIGHT
    of the NOISY-GATE ONLY, i.e. we treat noise as (U_ideal * Rz(eps)) but we only twirl the
    NOISE Rz(eps) portion by conjugation. This models the standard RC construction where
    easy (Clifford) cycles are randomized and hard (non-Clifford) cycles absorb the twirl
    inversion into the following easy cycle.

    Concretely for a single-qubit chain U^L, we implement per cycle:
        Rz(2*phi)  ;  P_k  ;  Rz(eps)  ;  P_k^dagger
    which equals  Rz(2*phi) * (P_k Rz(eps) P_k^dagger)
    -- ideal action unchanged, noise conjugated by a random Pauli each cycle.
    Averaged over P_k in {I,X,Y,Z}, the coherent Rz(eps) noise channel is twirled into
    a Pauli-diagonal (stochastic) channel, matching the paper's Theorem 1 condition.
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    for _ in range(L):
        qc.rz(2*PHI_TRUE, 0)                 # ideal U
        p = rng.choice(PAULI_LABELS)
        # apply P
        if p == "X": qc.x(0)
        elif p == "Y": qc.y(0)
        elif p == "Z": qc.z(0)
        # noise (coherent over-rotation) -- gets conjugated by P
        qc.rz(eps, 0)
        # apply P^dagger (Paulis are self-inverse)
        if p == "X": qc.x(0)
        elif p == "Y": qc.y(0)
        elif p == "Z": qc.z(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def run_circuit(qc, shots):
    tqc = transpile(qc, sim)
    res = sim.run(tqc, shots=shots).result()
    counts = res.get_counts()
    n0 = counts.get("0", 0)
    n1 = counts.get("1", 0)
    return n0 / (n0 + n1)   # P(0)

def estimate_phi_from_curve(L_list, p0_list):
    """
    We have p0(L) ~= (1 + cos(2*phi_est * L))/2 for the bare/ideal chain,
    or the twirled ensemble average version for RC.
    Fit phi_est by minimizing sum_L ( p0(L) - (1+cos(2*phi*L))/2 )^2 over a fine phi grid
    restricted to a small window around PHI_TRUE (since PE ambiguity is handled by iterative L doubling
    in practice; for scaling of BIAS this simple 1-D fit is sufficient).
    """
    p0 = np.array(p0_list)
    L  = np.array(L_list, dtype=float)
    # search phi in [PHI_TRUE - 0.5, PHI_TRUE + 0.5]  (well outside any noise we test)
    phis = np.linspace(PHI_TRUE - 0.5, PHI_TRUE + 0.5, 20001)
    best = None
    for phi in phis:
        pred = (1 + np.cos(2*phi*L))/2
        err = float(np.sum((p0 - pred)**2))
        if best is None or err < best[0]:
            best = (err, float(phi))
    return best[1]

def experiment_bare(eps):
    p0 = []
    for L in L_LIST:
        qc = build_circuit_bare(L, eps)
        p0.append(run_circuit(qc, NS_PER_CIRCUIT))
    phi_est = estimate_phi_from_curve(L_LIST, p0)
    return phi_est, p0

def experiment_rc(eps, nr, ns_total):
    """Average P(0|L) over Nr random compilations, each with ns_total/Nr shots."""
    shots_per_rc = max(1, ns_total // nr)
    rng = np.random.default_rng(int(1e6*eps) + 999)
    p0_avg = []
    for L in L_LIST:
        vals = []
        for _ in range(nr):
            qc = build_circuit_rc(L, eps, rng)
            vals.append(run_circuit(qc, shots_per_rc))
        p0_avg.append(float(np.mean(vals)))
    phi_est = estimate_phi_from_curve(L_LIST, p0_avg)
    return phi_est, p0_avg

def main():
    t0 = time.time()
    print(f"# arXiv:2208.04100 — small-instance replication")
    print(f"# phi_true = {PHI_TRUE}")
    print(f"# L_list   = {L_LIST}")
    print(f"# Ns/circuit = {NS_PER_CIRCUIT}, Nr = {NR}")
    print(f"# coherent noise angles: {NOISE_ANGLES}")
    print()

    results = {
        "phi_true": PHI_TRUE,
        "L_list": L_LIST,
        "Ns_per_circuit": NS_PER_CIRCUIT,
        "Nr": NR,
        "noise_angles": NOISE_ANGLES,
        "phi_bare": {},        # eps -> phi_est
        "phi_rc":   {},
        "err_bare": {},
        "err_rc":   {},
        "p0_bare":  {},
        "p0_rc":    {},
    }

    for eps in NOISE_ANGLES:
        te0 = time.time()
        phi_b, p0_b = experiment_bare(eps)
        phi_r, p0_r = experiment_rc(eps, NR, NS_PER_CIRCUIT)
        err_b = abs(phi_b - PHI_TRUE)
        err_r = abs(phi_r - PHI_TRUE)
        results["phi_bare"][f"{eps}"] = phi_b
        results["phi_rc"  ][f"{eps}"] = phi_r
        results["err_bare"][f"{eps}"] = err_b
        results["err_rc"  ][f"{eps}"] = err_r
        results["p0_bare" ][f"{eps}"] = p0_b
        results["p0_rc"   ][f"{eps}"] = p0_r
        print(f"eps={eps:6.4f} | bare phi_est={phi_b:.6f} err={err_b:.3e} "
              f"| rc phi_est={phi_r:.6f} err={err_r:.3e} "
              f"| ratio(bare/rc)={err_b/max(err_r,1e-12):8.2f} "
              f"| dt={time.time()-te0:.1f}s")

    # Fit log-log slopes of error vs eps (in strong-noise regime, per the paper)
    # Use the largest ~4 noise values for the strong-noise power law
    strong = NOISE_ANGLES[-5:]   # 5 largest angles
    eb = np.array([results["err_bare"][f"{e}"] for e in strong])
    er = np.array([results["err_rc"  ][f"{e}"] for e in strong])
    ex = np.array(strong)
    slope_b, int_b = np.polyfit(np.log(ex), np.log(np.maximum(eb, 1e-15)), 1)
    slope_r, int_r = np.polyfit(np.log(ex), np.log(np.maximum(er, 1e-15)), 1)
    results["slope_bare_strongnoise"] = float(slope_b)
    results["slope_rc_strongnoise"]   = float(slope_r)

    print()
    print(f"POWER-LAW FIT (strong-noise regime, eps in {strong}):")
    print(f"  bare  err(eps) ~ eps^{slope_b:.3f}    (paper reports ~1.04, i.e. linear)")
    print(f"  RC    err(eps) ~ eps^{slope_r:.3f}    (paper reports ~2.73, i.e. superlinear)")
    print(f"  slope-gap = {slope_r - slope_b:.3f}   (paper ~ 1.7)")

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(results, f, indent=2, default=float)

    # ---- verdict decision ----
    # Headline: bare slope should be ~1 (linear in eps), RC slope should be strictly > bare
    bare_ok = 0.7 <= slope_b <= 1.3
    rc_gt   = slope_r > slope_b + 0.3   # any clear scaling improvement
    print()
    print(f"headline check: bare_slope~1 ({slope_b:.3f}) -> {'PASS' if bare_ok else 'FAIL'}")
    print(f"headline check: rc_slope > bare_slope by >=0.3 ({slope_r-slope_b:.3f}) -> {'PASS' if rc_gt else 'FAIL'}")
    print(f"total wall time: {time.time()-t0:.1f}s")

    return results, slope_b, slope_r, bare_ok, rc_gt

if __name__ == "__main__":
    main()
