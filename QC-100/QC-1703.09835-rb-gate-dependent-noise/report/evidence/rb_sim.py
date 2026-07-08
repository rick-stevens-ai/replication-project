#!/usr/bin/env python3
"""
Single-qubit Clifford Randomized Benchmarking replication for
Wallman 2017, "Randomized benchmarking with gate-dependent noise"
(arXiv:1703.09835).

Testable prediction (Theorem 4, eq. 2-3):
Average survival probability at sequence length m is
   A p^m + B + eps_m,     with  |eps_m| <= delta1 * delta2^m
where p = (d*f(E,I) - 1)/(d-1)  and E is the "suitably defined average" noise.

For a single qubit (d=2), the average gate infidelity is r = 1 - f
so  r = (1 - p) * (d-1)/d = (1 - p) / 2.

We compare two noise models fitted with the SAME standard exponential RB
decay curve  y = A p^m + B:

  (a) Uniform depolarizing noise: every Clifford gets the same depolarizing
      channel of average infidelity r_target. Fit r_fit should reproduce r_target
      within statistical error (STANDARD RB works trivially here).

  (b) Gate-dependent noise: each Clifford gets an independently sampled random
      unitary noise with (Pauli/depolarizing-like) infidelity r_g drawn so that
      the AVERAGE infidelity over the group is r_target. Under Wallman's theorem,
      the standard single-exponential fit STILL applies and its recovered p
      corresponds to the average noise E — up to a small perturbation
      delta1 * delta2^m that decays exponentially.

We simulate with Qiskit Aer's density-matrix simulator, running the full
Clifford (24 elements) sequence and inserting per-gate noise (custom KrausOp per Clifford index).
"""
import argparse, json, os, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, random_unitary, Statevector, DensityMatrix, average_gate_fidelity
from qiskit.circuit.library import IGate, XGate, YGate, ZGate, HGate, SGate, SdgGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, QuantumError
from qiskit.quantum_info import Kraus, SuperOp, Choi

# ----------------------------------------------------------------------
# Build the 24 single-qubit Cliffords as (unitary matrix, gate label str)
# ----------------------------------------------------------------------
def build_single_qubit_cliffords():
    """Return list of 24 (Operator, name) covering the single-qubit Clifford group.
    Composed from the 6 rotations x {I,X,Y,Z}: 6*4 = 24 = |C_1|.
    """
    I = np.eye(2, dtype=complex)
    X = np.array([[0,1],[1,0]], dtype=complex)
    Y = np.array([[0,-1j],[1j,0]], dtype=complex)
    Z = np.array([[1,0],[0,-1]], dtype=complex)
    H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
    S = np.array([[1,0],[0,1j]], dtype=complex)
    Sdg = np.array([[1,0],[0,-1j]], dtype=complex)
    # 6 axis-rotations (the "rotation" cosets of Pauli group)
    rot_bases = [
        ("I",   I),
        ("H",   H),
        ("S",   S),
        ("HS",  H @ S),
        ("SH",  S @ H),
        ("HSH", H @ S @ H),
    ]
    paulis = [("I", I), ("X", X), ("Y", Y), ("Z", Z)]
    cliffs = []
    for rname, R in rot_bases:
        for pname, P in paulis:
            U = R @ P
            cliffs.append((f"{rname}*{pname}", U))
    # Dedup by unitary up to global phase (should be exactly 24, but be safe)
    unique = []
    seen = []
    for name, U in cliffs:
        keep = True
        for U2 in seen:
            # up to global phase: check |Tr(U^\dagger U2)| == 2 (d=2)
            if abs(abs(np.trace(U.conj().T @ U2)) - 2.0) < 1e-9:
                keep = False
                break
        if keep:
            seen.append(U)
            unique.append((name, U))
    assert len(unique) == 24, f"got {len(unique)} unique Cliffords, expected 24"
    return unique

CLIFFS = build_single_qubit_cliffords()
CLIFF_OPS = [Operator(U) for _, U in CLIFFS]

def find_inverse_index(prod_U):
    """Given a target unitary (the product of a random sequence), return
    the index of the Clifford whose action inverts it (up to global phase)."""
    for i, (_, U) in enumerate(CLIFFS):
        # want U @ prod_U == e^{i phi} I
        M = U @ prod_U
        # M should be proportional to identity: check |M[0,0]| ~ 1 and off-diag ~ 0
        phase = M[0,0]
        if abs(abs(phase) - 1) < 1e-8:
            Mnorm = M / phase
            if np.allclose(Mnorm, np.eye(2), atol=1e-6):
                return i
    raise RuntimeError("no inverse found")

# ----------------------------------------------------------------------
# Noise: build a KrausOp per Clifford
# ----------------------------------------------------------------------
def single_qubit_depolarizing_kraus(r):
    """Depolarizing channel with average gate infidelity r
    (single qubit: r = p_dep * (d-1)/d = p_dep/2, so p_dep = 2r).
    """
    p = 2.0 * r
    p = max(0.0, min(1.0, p))
    return depolarizing_error(p, 1)  # QuantumError

def random_unitary_error_infidelity_r(r, rng):
    """Sample a random single-qubit unitary noise U with infidelity r.
    Following Wallman eq (44)-(45):
       U = V exp(-i theta Z) V^\dagger,  V ~ Haar,
       r = (2 - cos^2 theta)/3  =>  cos^2 theta = 2 - 3r, sin theta = sqrt(3r/2 * (1 - ...))
    More directly: theta = arcsin(sqrt(3r/2)).
    """
    if r <= 0:
        U = np.eye(2, dtype=complex)
    else:
        arg = min(1.0, np.sqrt(1.5 * r))
        theta = np.arcsin(arg)
        # Haar-random V
        V = random_unitary(2, seed=int(rng.integers(0, 2**31))).data
        Z = np.array([[1,0],[0,-1]], dtype=complex)
        expm = np.cos(theta)*np.eye(2) - 1j*np.sin(theta)*Z
        U = V @ expm @ V.conj().T
    # Build a coherent (unitary) quantum error via its Kraus (= [U])
    return QuantumError([(Kraus([U]), 1.0)])

def build_noise_model_uniform_depol(r_target):
    """Uniform depolarizing on every custom Clifford label."""
    nm = NoiseModel()
    err = single_qubit_depolarizing_kraus(r_target)
    for idx in range(24):
        nm.add_quantum_error(err, [f"cl{idx}"], [0])
    return nm, [r_target]*24

def build_noise_model_gate_dependent(r_target, spread, rng):
    """Per-Clifford independently sampled *coherent* random-unitary noise with
    infidelity r_g drawn from a distribution centered at r_target.

    We sample r_g uniformly in [r_target*(1-spread), r_target*(1+spread)] and
    build a coherent (unitary) noise per Clifford.  Each Clifford therefore
    has a DIFFERENT infidelity AND a different noise channel direction
    (both magnitude- and structure-dependent variation).
    """
    nm = NoiseModel()
    r_per = []
    for idx in range(24):
        lo = max(0.0, r_target * (1 - spread))
        hi = r_target * (1 + spread)
        r_g = float(rng.uniform(lo, hi))
        r_per.append(r_g)
        err = random_unitary_error_infidelity_r(r_g, rng)
        nm.add_quantum_error(err, [f"cl{idx}"], [0])
    return nm, r_per

# ----------------------------------------------------------------------
# Circuit assembly
# ----------------------------------------------------------------------
def build_rb_circuit(cliff_seq_indices, inverse_index):
    """Build a QuantumCircuit that applies each Clifford as a custom unitary
    with label 'clK' so the NoiseModel picks up the label-based noise."""
    qc = QuantumCircuit(1, 1)
    for k in cliff_seq_indices:
        _, U = CLIFFS[k]
        qc.unitary(U, [0], label=f"cl{k}")
    _, Uinv = CLIFFS[inverse_index]
    qc.unitary(Uinv, [0], label=f"cl{inverse_index}")
    qc.measure(0, 0)
    return qc

# ----------------------------------------------------------------------
# RB experiment
# ----------------------------------------------------------------------
def run_rb(noise_model, m_list, n_seqs, shots, sim_seed, cliff_rng):
    simulator = AerSimulator(noise_model=noise_model, method="density_matrix", seed_simulator=sim_seed)
    survivals = {m: [] for m in m_list}
    for m in m_list:
        for s in range(n_seqs):
            # random sequence of m Cliffords
            seq = cliff_rng.integers(0, 24, size=m).tolist()
            # compute inverse Clifford
            prod = np.eye(2, dtype=complex)
            for k in seq:
                prod = CLIFFS[k][1] @ prod
            inv_idx = find_inverse_index(prod)
            qc = build_rb_circuit(seq, inv_idx)
            result = simulator.run(qc, shots=shots).result()
            counts = result.get_counts()
            p0 = counts.get('0', 0) / shots
            survivals[m].append(p0)
    return survivals

def fit_rb(m_list, survivals):
    """Fit y = A p^m + B."""
    means = np.array([np.mean(survivals[m]) for m in m_list])
    stds = np.array([np.std(survivals[m], ddof=1) / np.sqrt(len(survivals[m])) for m in m_list])
    stds = np.where(stds < 1e-6, 1e-6, stds)  # avoid zero weights
    def model(m, A, p, B):
        return A * p**m + B
    try:
        popt, pcov = curve_fit(model, m_list, means, sigma=stds, absolute_sigma=True,
                               p0=[0.5, 0.99, 0.5],
                               bounds=([0.0, 0.0, 0.0], [1.0, 1.0, 1.0]),
                               maxfev=20000)
        A, p, B = popt
        perr = np.sqrt(np.diag(pcov))
        return {"A": A, "p": p, "B": B, "A_err": perr[0], "p_err": perr[1], "B_err": perr[2],
                "means": means.tolist(), "stds": stds.tolist()}
    except Exception as e:
        return {"error": str(e), "means": means.tolist(), "stds": stds.tolist()}


def r_from_p(p, d=2):
    return (1.0 - p) * (d - 1) / d


# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r_target", type=float, default=0.01,
                    help="target average gate infidelity")
    ap.add_argument("--spread", type=float, default=0.5,
                    help="fractional half-spread of gate-dependent r_g around r_target")
    ap.add_argument("--m_list", type=int, nargs='+',
                    default=[2, 4, 8, 16, 32, 64, 128])
    ap.add_argument("--n_seqs", type=int, default=30)
    ap.add_argument("--shots", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260703)
    ap.add_argument("--out", type=str, default="rb_results.json")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    print(f"[cfg] r_target={args.r_target}  spread={args.spread}  m_list={args.m_list}  n_seqs={args.n_seqs}  shots={args.shots}")
    t0 = time.time()

    # --- (a) Uniform depolarizing ---
    print("[uniform] building noise model...", flush=True)
    nm_uni, r_per_uni = build_noise_model_uniform_depol(args.r_target)
    print("[uniform] running RB...", flush=True)
    surv_uni = run_rb(nm_uni, args.m_list, args.n_seqs, args.shots,
                      sim_seed=args.seed, cliff_rng=np.random.default_rng(args.seed + 1))
    fit_uni = fit_rb(args.m_list, surv_uni)
    r_fit_uni = r_from_p(fit_uni["p"]) if "p" in fit_uni else None
    print(f"[uniform] p_fit={fit_uni.get('p'):.6f} r_fit={r_fit_uni}  r_target={args.r_target}", flush=True)

    # --- (b) Gate-dependent (coherent random unitary per Clifford) ---
    print("[gate-dep] building noise model...", flush=True)
    nm_gd, r_per_gd = build_noise_model_gate_dependent(
        args.r_target, args.spread, np.random.default_rng(args.seed + 2))
    r_mean_gd = float(np.mean(r_per_gd))
    print(f"[gate-dep] mean(r_per_gate)={r_mean_gd:.6f}  min={min(r_per_gd):.4f} max={max(r_per_gd):.4f}", flush=True)
    print("[gate-dep] running RB...", flush=True)
    surv_gd = run_rb(nm_gd, args.m_list, args.n_seqs, args.shots,
                     sim_seed=args.seed + 100, cliff_rng=np.random.default_rng(args.seed + 3))
    fit_gd = fit_rb(args.m_list, surv_gd)
    r_fit_gd = r_from_p(fit_gd["p"]) if "p" in fit_gd else None
    print(f"[gate-dep] p_fit={fit_gd.get('p'):.6f} r_fit={r_fit_gd}  mean(r_per_gate)={r_mean_gd}", flush=True)

    elapsed = time.time() - t0
    out = {
        "config": vars(args),
        "elapsed_seconds": elapsed,
        "uniform": {
            "r_per_gate": r_per_uni,
            "r_target": args.r_target,
            "fit": fit_uni,
            "r_fit": r_fit_uni,
            "m_list": args.m_list,
            "survivals": {str(m): surv_uni[m] for m in args.m_list},
        },
        "gate_dependent": {
            "r_per_gate": r_per_gd,
            "r_mean_per_gate": r_mean_gd,
            "fit": fit_gd,
            "r_fit": r_fit_gd,
            "m_list": args.m_list,
            "survivals": {str(m): surv_gd[m] for m in args.m_list},
        },
        "notes": [
            "Uniform depolarizing: standard RB assumption satisfied; fit r should ~ r_target.",
            "Gate-dependent (coherent random unitary per Clifford with spread in r_g): tests Wallman 2017 claim that the standard single-exponential fit STILL holds and recovers a well-defined average infidelity.",
        ],
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"[done] elapsed={elapsed:.1f}s -> {args.out}")

if __name__ == "__main__":
    main()
