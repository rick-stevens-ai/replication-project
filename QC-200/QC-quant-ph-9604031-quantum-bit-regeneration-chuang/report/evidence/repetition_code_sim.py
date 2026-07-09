#!/usr/bin/env python3
"""
Independent replication analog for Chuang & Yamamoto (1996),
"Quantum Bit Regeneration" (arXiv:quant-ph/9604031).

The paper itself proposes a dual-rail photonic scheme with balanced-loss QND
measurement for AMPLITUDE-DAMPING regeneration. That specific scheme requires
optical hardware or a full Lindblad simulation of a photonic Hilbert space and
is not the "reproducible core" we were tasked with. Per the QC-200 wave brief,
we reproduce the *spirit* of the paper -- quantum regeneration by redundancy --
using the canonical 3-qubit bit-flip repetition code that appeared in the same
year (Shor 1995 / Steane 1996) and is the standard textbook analog of the
"regenerate a noisy qubit" claim.

Headline check (analog):
  - Raw channel per-qubit error:  p
  - 3-qubit bit-flip repetition code, majority-vote decoding:  3p^2 - 2p^3
So there is a crossover: encoded error < raw error whenever p < 1/2.
This is the analog of the paper's central claim that redundancy + parity/QND
measurement can suppress the effective error rate.

Method:
  - Real density-matrix simulation on 3 qubits (8x8 rho).
  - Encoding via CNOT_{1->2} CNOT_{1->3}.
  - Independent bit-flip channel on each qubit:
        rho -> (1-p) rho + p X_i rho X_i.
  - Stabilizer syndrome measurement of Z1Z2 and Z2Z3.
  - Pauli-X correction based on syndrome.
  - Decode via CNOT_{1->3} CNOT_{1->2}, trace out qubits 2 and 3.
  - Compare recovered single-qubit rho to input.
  - Also: no-encoding baseline (single qubit + bit-flip).
  - Monte Carlo: N=10_000 syndrome trajectories per p.

Outputs:
  - report/evidence/repetition_code_results.json
  - report/evidence/repetition_code_results.csv
  - report/evidence/repetition_code_plot.png
"""

from __future__ import annotations
import json, os, csv, math, time
import numpy as np

# ---- single-qubit ops ----
I = np.array([[1,0],[0,1]], dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def op1(pauli, i, n=3):
    """Single-qubit Pauli on qubit i (0-indexed, left=qubit 0)."""
    mats = [I]*n
    mats[i] = pauli
    return kron_list(mats)

# ---- CNOT with explicit control/target ----
def cnot(ctrl, tgt, n=3):
    dim = 2**n
    U = np.zeros((dim, dim), dtype=complex)
    for basis in range(dim):
        bits = [(basis >> (n-1-k)) & 1 for k in range(n)]
        if bits[ctrl] == 1:
            bits[tgt] ^= 1
        out = 0
        for k in range(n):
            out |= bits[k] << (n-1-k)
        U[out, basis] = 1
    return U

# Encoding: |psi>|0>|0>  --CNOT01--> --CNOT02-->  a|000>+b|111>
CNOT01 = cnot(0, 1, 3)
CNOT02 = cnot(0, 2, 3)
ENC = CNOT02 @ CNOT01
DEC = CNOT01 @ CNOT02   # inverse (self-inverse: CNOT^2=I, order reversed)

X0 = op1(X, 0)
X1 = op1(X, 1)
X2 = op1(X, 2)
Z0 = op1(Z, 0)
Z1 = op1(Z, 1)
Z2 = op1(Z, 2)

# Stabilizers
ZZ01 = Z0 @ Z1
ZZ12 = Z1 @ Z2

# Projectors onto +1/-1 eigenspaces of a Hermitian operator O with O^2=I
def eig_projectors_pm1(O):
    dim = O.shape[0]
    P_plus  = 0.5 * (np.eye(dim) + O)
    P_minus = 0.5 * (np.eye(dim) - O)
    return P_plus, P_minus

P01_plus, P01_minus = eig_projectors_pm1(ZZ01)
P12_plus, P12_minus = eig_projectors_pm1(ZZ12)

# Syndrome table: (s01, s12) -> correction
#   +1,+1 -> no error (or error on unencoded logical, treated as none)
#   -1,+1 -> error on qubit 0  -> apply X0
#   -1,-1 -> error on qubit 1  -> apply X1
#   +1,-1 -> error on qubit 2  -> apply X2
CORRECTIONS = {
    (+1, +1): np.eye(8, dtype=complex),
    (-1, +1): X0,
    (-1, -1): X1,
    (+1, -1): X2,
}

# ---- density-matrix helpers ----
def dm_from_state(psi):
    psi = psi.reshape(-1, 1)
    return psi @ psi.conj().T

def apply_bitflip_channel_qubit(rho, i, p, n=3):
    Xi = op1(X, i, n)
    return (1-p) * rho + p * (Xi @ rho @ Xi)

def apply_bitflip_all(rho, p, n=3):
    for i in range(n):
        rho = apply_bitflip_channel_qubit(rho, i, p, n)
    return rho

def project_measure(rho, projectors):
    """Return list of (probability, post-measurement rho) for each projector."""
    out = []
    for P in projectors:
        M = P @ rho @ P
        prob = np.real(np.trace(M))
        if prob > 1e-15:
            out.append((prob, M / prob))
        else:
            out.append((0.0, None))
    return out

def partial_trace_keep_qubit0(rho8):
    """Trace out qubits 1 and 2 (0-indexed, left-most = qubit 0) from 3-qubit rho."""
    # reshape (2,2,2, 2,2,2) then contract indices for q1 and q2
    T = rho8.reshape(2,2,2, 2,2,2)
    # trace q1: sum over axis 1 and 4
    T = np.einsum('abcadc->bd', T)  # trace q1 (axes 1 and 4) then q2 (axes 2 and 5)
    # Wait: after reshape indices are (i0,i1,i2, j0,j1,j2). We want tr over i1=j1 and i2=j2.
    # Re-do properly:
    T = rho8.reshape(2,2,2, 2,2,2)
    T2 = np.einsum('abcdec->abde', T)  # trace q2: contract axes 2 & 5 -> (i0,i1, j0,j1)
    T3 = np.einsum('abcb->ac', T2)     # trace q1: contract axes 1 & 3 -> (i0, j0)
    return T3  # 2x2

def fidelity(rho, sigma):
    """Fidelity F(rho,sigma) = (tr sqrt(sqrt(rho) sigma sqrt(rho)))^2, for 2x2 states."""
    # for small matrices, do it directly
    evals_r, evecs_r = np.linalg.eigh(rho)
    evals_r = np.clip(evals_r, 0, None)
    sqrt_r = evecs_r @ np.diag(np.sqrt(evals_r)) @ evecs_r.conj().T
    M = sqrt_r @ sigma @ sqrt_r
    ev = np.linalg.eigvalsh(M)
    ev = np.clip(ev, 0, None)
    return float(np.real(np.sum(np.sqrt(ev)))**2)

# ---- One trajectory of protected transmission ----
def run_protected_trajectory(psi, p, rng):
    """
    Encode -> per-qubit bit-flip -> stochastic syndrome measurement ->
    correction -> decode -> partial trace -> return recovered 1-qubit rho.
    We *sample* an actual syndrome instead of averaging over the (unphysical)
    coherent post-channel state, so this matches a real protocol.
    """
    psi3 = np.kron(np.kron(psi, np.array([1,0], dtype=complex)),
                             np.array([1,0], dtype=complex))
    rho3 = dm_from_state(psi3)
    rho3 = ENC @ rho3 @ ENC.conj().T

    # Apply channel one qubit at a time by *sampling* whether each qubit flipped.
    for q in range(3):
        if rng.random() < p:
            Xq = op1(X, q, 3)
            rho3 = Xq @ rho3 @ Xq

    # Syndrome sampling: measure ZZ01 first
    outs01 = project_measure(rho3, [P01_plus, P01_minus])
    probs01 = [o[0] for o in outs01]
    total = sum(probs01)
    r = rng.random() * total
    if r < probs01[0]:
        s01 = +1; rho3 = outs01[0][1]
    else:
        s01 = -1; rho3 = outs01[1][1]

    outs12 = project_measure(rho3, [P12_plus, P12_minus])
    probs12 = [o[0] for o in outs12]
    total = sum(probs12)
    r = rng.random() * total
    if r < probs12[0]:
        s12 = +1; rho3 = outs12[0][1]
    else:
        s12 = -1; rho3 = outs12[1][1]

    C = CORRECTIONS[(s01, s12)]
    rho3 = C @ rho3 @ C.conj().T

    # Decode
    rho3 = DEC @ rho3 @ DEC.conj().T
    rho1 = partial_trace_keep_qubit0(rho3)
    return rho1

def run_raw_trajectory(psi, p, rng):
    rho = dm_from_state(psi)
    if rng.random() < p:
        rho = X @ rho @ X
    return rho

# ---- Monte Carlo ----
def infidelity(psi, rho_out):
    F = fidelity(dm_from_state(psi), rho_out)
    return max(0.0, 1.0 - F)

def sweep(p_values, N=10_000, seed=0xC0FFEE):
    """
    Return dict p -> {raw_err, prot_err, raw_err_se, prot_err_se,
                       raw_err_theory, prot_err_theory, N}.
    Theory: raw = p, protected = 3 p^2 - 2 p^3.
    We average the infidelity per trajectory.
    """
    rng = np.random.default_rng(seed)
    # For the bit-flip *probability* headline claim (raw=p, code=3p^2-2p^3),
    # we use logical basis states |0>,|1> where a bit-flip *always* produces
    # infidelity 1.0 (X|0>=|1>, X|1>=|0>). Averaging infidelity over these
    # then directly measures the effective bit-flip probability.
    # We also include |+>,|->,|+i> in a separate 'coherent' pass to verify
    # phase coherence is preserved by the code.
    bitflip_states = [
        np.array([1, 0], dtype=complex),                                 # |0>
        np.array([0, 1], dtype=complex),                                 # |1>
    ]
    coherent_states = [
        (1/np.sqrt(2)) * np.array([1, 1], dtype=complex),                # |+>
        (1/np.sqrt(2)) * np.array([1, -1], dtype=complex),               # |->
        (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex),               # |+i>
    ]
    results = {}
    for p in p_values:
        # bit-flip probability channel (headline)
        raw_infids = []
        prot_infids = []
        per_state = max(1, N // len(bitflip_states))
        for psi in bitflip_states:
            for _ in range(per_state):
                rho_out = run_raw_trajectory(psi, p, rng)
                raw_infids.append(infidelity(psi, rho_out))
                rho_prot = run_protected_trajectory(psi, p, rng)
                prot_infids.append(infidelity(psi, rho_prot))
        raw_arr = np.array(raw_infids)
        prot_arr = np.array(prot_infids)
        # coherent-state pass (average infidelity for phase-superposition states)
        raw_coh = []
        prot_coh = []
        per_state_c = max(1, N // len(coherent_states))
        for psi in coherent_states:
            for _ in range(per_state_c):
                rho_out = run_raw_trajectory(psi, p, rng)
                raw_coh.append(infidelity(psi, rho_out))
                rho_prot = run_protected_trajectory(psi, p, rng)
                prot_coh.append(infidelity(psi, rho_prot))
        raw_coh_arr = np.array(raw_coh)
        prot_coh_arr = np.array(prot_coh)
        results[p] = dict(
            raw_err=float(raw_arr.mean()),
            prot_err=float(prot_arr.mean()),
            raw_err_se=float(raw_arr.std(ddof=1) / math.sqrt(len(raw_arr))),
            prot_err_se=float(prot_arr.std(ddof=1) / math.sqrt(len(prot_arr))),
            raw_err_theory=float(p),
            prot_err_theory=float(3*p*p - 2*p*p*p),
            coh_raw_infid=float(raw_coh_arr.mean()),
            coh_prot_infid=float(prot_coh_arr.mean()),
            N=int(len(raw_arr)),
            N_coh=int(len(raw_coh_arr)),
        )
    return results

def main():
    t0 = time.time()
    p_values = [0.01, 0.05, 0.1, 0.2]
    print(f"Running Monte Carlo sweep over p={p_values}, ~10^4 traj/p ...")
    res = sweep(p_values, N=10_000, seed=42)
    for p, r in res.items():
        print(f"  p={p:>5}: raw={r['raw_err']:.5f} (theory {r['raw_err_theory']:.5f}), "
              f"prot={r['prot_err']:.5f} (theory {r['prot_err_theory']:.5f})  "
              f"advantage={r['raw_err'] - r['prot_err']:+.5f}")
    dt = time.time() - t0
    print(f"elapsed {dt:.1f}s")

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "repetition_code_results.json"), "w") as f:
        json.dump({
            "paper": "arXiv:quant-ph/9604031 (Chuang & Yamamoto, 1996)",
            "note": ("Analog replication: paper describes dual-rail photonic "
                     "amplitude-damping regeneration; we reproduce the "
                     "underlying claim [redundancy + syndrome measurement "
                     "quadratically suppresses per-qubit error] with the "
                     "3-qubit bit-flip repetition code."),
            "monte_carlo_trials_per_p": 10_000,
            "test_states": ["|0>","|1>","|+>","|->","|+i>"],
            "elapsed_seconds": dt,
            "results": {str(k): v for k, v in res.items()},
        }, f, indent=2)

    with open(os.path.join(outdir, "repetition_code_results.csv"), "w") as f:
        w = csv.writer(f)
        w.writerow(["p","N","raw_err","raw_err_se","raw_err_theory",
                    "prot_err","prot_err_se","prot_err_theory","advantage"])
        for p, r in res.items():
            w.writerow([p, r["N"], r["raw_err"], r["raw_err_se"], r["raw_err_theory"],
                        r["prot_err"], r["prot_err_se"], r["prot_err_theory"],
                        r["raw_err"] - r["prot_err"]])

    # matplotlib is optional
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ps = list(res.keys())
        raw = [res[p]["raw_err"] for p in ps]
        prot = [res[p]["prot_err"] for p in ps]
        raw_t = [res[p]["raw_err_theory"] for p in ps]
        prot_t = [res[p]["prot_err_theory"] for p in ps]
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(ps, raw_t, 'b--', label='raw theory  p')
        ax.plot(ps, prot_t, 'r--', label=r'code theory  $3p^2-2p^3$')
        ax.plot(ps, raw, 'bo', label='raw MC')
        ax.plot(ps, prot, 'rs', label='code MC')
        ax.set_xlabel('per-qubit bit-flip probability p')
        ax.set_ylabel('effective logical error / infidelity')
        ax.set_title('3-qubit bit-flip repetition code vs. raw channel\n'
                     '(analog of Chuang & Yamamoto 1996 regeneration)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, "repetition_code_plot.png"), dpi=140)
        print("wrote plot")
    except Exception as e:
        print(f"skipped plot: {e}")

if __name__ == "__main__":
    main()
