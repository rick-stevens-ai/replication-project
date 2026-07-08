#!/usr/bin/env python3
"""
Independent replication of arXiv:1903.00768 "An Experimental Study of Shor's
Factoring Algorithm on IBM Q" (Amico, Saleem, Kumph 2019).

We do NOT have access to ibmqx5 hardware; instead we reproduce their
*classical/quantum-simulated* baseline: the theoretical distributions
P_r^th(s) they compare to, plus their semi-classical/Kitaev-style compiled
Shor circuits run on Qiskit Aer statevector (noiseless = "ideal
experiment") and Aer with a light depolarizing noise model (surrogate
for NISQ noise).

Then compute the paper's headline metric:
  SSO(m, e) = ( sum_j sqrt(m_j) * sqrt(e_j) )^2
between measured (m) and expected (e) probability distributions of the
period register.

Paper's reported SSO values (ibmqx5 experimental):
  N=15, a=2  : max SSO = 0.97 at r=4
  N=15, a=11 : max SSO = 0.92 at r=2
  N=21, a=2  : max SSO = 0.78 at r=6
  N=35, a=4  : max SSO = 0.99 at r=7 (WRONG - true is r=6, SSO 0.98)

Replication targets:
  - Noiseless: SSO ~ 1.0 (recovers true period cleanly)
  - Light depolarizing noise: SSO drops
  - Heavy depolarizing noise: SSO -> flat / period-assignment fails
    (mirroring the paper's N=35 finding at the smaller cases)
"""

from __future__ import annotations
import json
import os
import sys
import math
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ---------------------------------------------------------------------------
# 1. Theoretical distribution P_r^th(s)  (Eq. 1 in the paper)
# ---------------------------------------------------------------------------
def theoretical_distribution(r: int, n_bits: int) -> np.ndarray:
    """
    P(s) = (1/Q^2) * |sum_{d=0}^{Q/r - 1} exp(2*pi*i*s*d*r/Q)|^2 * (Q/r)
    Using the simpler general form: for a period r and Q = 2^n_bits,
    the QPE-of-eigenvalue-with-period-r distribution over s in [0,Q)
    is:
        P(s) = (1/Q^2) * |sum_{x=0}^{Q-1} exp(2*pi*i*s*x/Q) * <x mod r == fixed>|^2
    A textbook simplification: with a uniform superposition of x and the
    period being r, the probability of measuring phase s is:
        P(s) = (1/(r*Q)) * |sum_{k=0}^{floor((Q-1)/r)} exp(2*pi*i*s*k*r/Q)|^2
    which is the standard "Fejer-like" QPE-with-period-r distribution.
    """
    Q = 2**n_bits
    K = Q // r  # number of full periods that fit; approx floor((Q-1)/r)+1
    # If Q is not a multiple of r, the number of terms varies with the phase
    # offset; averaged over offsets we get the following canonical form:
    # P(s) = (1/(r*Q)) * |sin(pi*s*K*r/Q) / sin(pi*s*r/Q)|^2 * (K terms)
    # For r that divides Q exactly the sum is a delta comb at s = j*Q/r.
    probs = np.zeros(Q, dtype=float)
    # Use the exact QFT-of-periodic-signal formula:
    # after inverse QFT of |k*r>_{k=0..K-1} state (uniform), phase s has
    # probability |1/K * sum_{k=0..K-1} exp(-2*pi*i*s*k*r/Q)|^2 * (K/Q)
    # We take that as the canonical P_r^th(s) up to normalization.
    if Q % r == 0:
        # perfect - delta comb
        for j in range(r):
            probs[j * (Q // r)] = 1.0 / r
        return probs
    # general case
    for s in range(Q):
        # sum_{x=0..Q-1} of e^{2*pi*i*s*x/Q} * (x mod r == 0)  / Q
        # equivalently sum_{k=0..K-1} e^{2*pi*i*s*k*r/Q}, K = ceil(Q/r)
        K = int(math.ceil(Q / r))
        # count exact number of x in [0, Q) with x mod r == 0
        Kx = (Q - 1) // r + 1
        acc = 0j
        for k in range(Kx):
            acc += np.exp(2j * np.pi * s * k * r / Q)
        probs[s] = abs(acc) ** 2
    probs /= probs.sum()
    return probs


# ---------------------------------------------------------------------------
# 2. Compiled Shor circuits (following the paper's Fig. 3 semi-classical QFT)
#
# We implement the standard Kitaev / semi-classical-QFT phase estimation
# with a single reused period-register qubit. This is the SAME scheme the
# paper implements on ibmqx5 (Sec IV, appendix A).
#
# We use n_p = 3 bits of period-register precision (matches paper: N=15 a=2
# uses 3 iterations; N=21 a=2 uses 3 bits; etc.).
#
# The controlled-U_a^x gates are implemented as controlled modular
# multiplication: |y> -> |a^x * y mod N>. For the small N we handle here
# (N in {15, 21, 35}), we implement U_a via an explicit permutation matrix
# so this is exact and matches the paper's "compiled" (pre-computed) MEF.
# ---------------------------------------------------------------------------

def _modmul_perm(a: int, N: int, n_q: int) -> np.ndarray:
    """Return the permutation matrix U such that
    U |y> = |(a*y) mod N> for y < N, and U |y> = |y> for y >= N."""
    dim = 2**n_q
    U = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < N and math.gcd(y, N) == 1 and y != 0:
            # a * y mod N is only well-defined-and-injective on units;
            # for the QPE we only need action on |1> and its orbit.
            new = (a * y) % N
            U[new, y] = 1.0
        elif y < N:
            # fixed for non-units (won't be reached from |1> since gcd(a,N)=1)
            U[y, y] = 1.0
        else:
            U[y, y] = 1.0
    return U


def _controlled_unitary_gate(U: np.ndarray, label: str = "cU"):
    """Wrap a unitary as a Qiskit Operator and return its .control()."""
    from qiskit.circuit.library import UnitaryGate
    return UnitaryGate(U, label=label).control(1)


def build_shor_semiclassical(
    N: int, a: int, n_bits: int
) -> Tuple[QuantumCircuit, int]:
    """
    Build the semi-classical-QFT Shor circuit for factoring N with base a,
    using n_bits of period-register precision.

    Returns (circuit, n_q).
    The circuit has n_q + 1 qubits and n_bits classical bits for the phase.
    Circuit ends with classical bits holding an n_bits-bit estimate of s/Q.
    """
    if math.gcd(a, N) != 1:
        raise ValueError(f"a={a} must be coprime to N={N}")

    n_q = int(math.ceil(math.log2(N)))
    dim_q = 2**n_q

    # Precompute controlled powers of U_a: U_{a^{2^k}} = U_a raised to 2^k
    # For the semi-classical QFT we apply c-U_{a^{2^{n_bits-1-k}}} at step k.
    # (Kitaev iterative QPE order.)
    U_a = _modmul_perm(a, N, n_q)
    U_powers = [U_a.copy()]
    for _ in range(1, n_bits):
        U_powers.append(U_powers[-1] @ U_powers[-1])  # U^{2^k}

    p = QuantumRegister(1, "p")   # period register (single qubit, reused)
    q = QuantumRegister(n_q, "q")  # computational register
    c = ClassicalRegister(n_bits, "c")

    qc = QuantumCircuit(p, q, c)

    # Initialize computational register to |1>
    qc.x(q[0])

    # Semi-classical iterative QPE. Iteration k (k=0..n_bits-1) uses power
    # 2^{n_bits-1-k} of U_a. Standard order: most-significant bit first.
    for k in range(n_bits):
        power = n_bits - 1 - k
        cU = _controlled_unitary_gate(U_powers[power], label=f"cU^{2**power}")

        qc.h(p[0])

        # Classical phase corrections from earlier measured bits
        # (semi-classical QFT feedback). The paper uses this too.
        # After measuring bit b_j in earlier step j, apply phase rotation
        #   R_z(-2*pi * b_j / 2^{k-j+1}) on the current p qubit before H.
        # In pure quantum form via c_if: implement via if-else on cbit j.
        for j in range(k):
            angle = -2 * math.pi * (2 ** (j - k - 1))  # -pi/2^{k-j+1} * 2? see below
            # More careful: after measuring b_j into classical bit j, the
            # accumulated phase correction on iteration k is:
            #   sum_{j<k} b_j * (2*pi * 2^{n_bits-1-j} / Q) ... but for semi-classical
            # QPE with output bits in order MSB-first (paper), the correction
            # on iteration k for prior bit j is:  phi = -2*pi * b_j / 2^{k-j+1}
            angle = -2 * math.pi / (2 ** (k - j + 1))
            with qc.if_test((c[j], 1)):
                qc.p(angle, p[0])

        qc.append(cU, [p[0]] + list(q))
        qc.h(p[0])

        qc.measure(p[0], c[k])

        # Reset the p qubit for reuse (only if not last iteration)
        if k < n_bits - 1:
            qc.reset(p[0])

    return qc, n_q


# ---------------------------------------------------------------------------
# 3. SSO computation
# ---------------------------------------------------------------------------
def sso(measured: np.ndarray, expected: np.ndarray) -> float:
    """SSO = (sum_j sqrt(m_j) * sqrt(e_j))^2  (Eq. 2 in paper)."""
    m = np.asarray(measured, dtype=float)
    e = np.asarray(expected, dtype=float)
    # normalize (defensive)
    if m.sum() > 0:
        m = m / m.sum()
    if e.sum() > 0:
        e = e / e.sum()
    val = float(np.sum(np.sqrt(m) * np.sqrt(e)) ** 2)
    return val


def counts_to_probs(counts: Dict[str, int], n_bits: int) -> np.ndarray:
    Q = 2**n_bits
    p = np.zeros(Q, dtype=float)
    tot = sum(counts.values())
    for bitstr, cnt in counts.items():
        # Qiskit classical bits: c[0] is the LSB in the bitstring's rightmost
        # position by default. The paper's phase s is the integer read from
        # bits (b_{n-1}...b_0) in MSB-first order (that's how QPE gives it).
        # In our circuit c[0] is measured FIRST and corresponds to the MSB
        # of the phase (iteration k=0 uses power 2^{n_bits-1}). Qiskit
        # renders classical registers as c[n-1]...c[0] left-to-right in the
        # counts string, so bitstr[0] = c[n-1] (last measured = LSB of phase),
        # bitstr[-1] = c[0] (first measured = MSB of phase).
        # So s = int(bitstr[::-1], 2) reversed... let's do it explicitly:
        bitstr_clean = bitstr.replace(" ", "")
        # In Qiskit, counts key bit index i (from RIGHT, i.e. bitstr[-1-i])
        # corresponds to classical bit c[i]. In our iterative QPE circuit,
        # c[0] is measured FIRST at iteration k=0 with controlled-U^{2^{n-1}}.
        # In iterative/semi-classical QPE the first-measured bit is the LSB
        # of the phase (not MSB) once the semi-classical feedback rotations
        # are applied in the order we implemented. Verified empirically in
        # diagnose.py against the ideal r=4, Q=8 comb.
        # So phase_int = sum_i c[i] * 2^i.
        s = 0
        for i in range(n_bits):
            bit = int(bitstr_clean[-1 - i])  # c[i]
            s += bit * (2 ** i)
        p[s] += cnt
    if tot > 0:
        p /= tot
    return p


# ---------------------------------------------------------------------------
# 4. Run one experiment: N, a, n_bits, noise level -> counts, probs, SSO(r_true)
# ---------------------------------------------------------------------------
def multiplicative_order(a: int, N: int) -> int:
    """Return the multiplicative order of a mod N (r such that a^r = 1 mod N)."""
    x = a % N
    r = 1
    while x != 1:
        x = (x * a) % N
        r += 1
        if r > N:
            return -1
    return r


def run_experiment(
    N: int,
    a: int,
    n_bits: int,
    shots: int = 4096,
    depol_1q: float = 0.0,
    depol_2q: float = 0.0,
    seed: int = 12345,
) -> Dict:
    qc, n_q = build_shor_semiclassical(N, a, n_bits)

    if depol_1q > 0 or depol_2q > 0:
        nm = NoiseModel()
        # apply depolarizing error to basis gates
        if depol_1q > 0:
            err1 = depolarizing_error(depol_1q, 1)
            nm.add_all_qubit_quantum_error(err1, ["u1", "u2", "u3", "rz", "sx", "x", "h", "p"])
        if depol_2q > 0:
            err2 = depolarizing_error(depol_2q, 2)
            nm.add_all_qubit_quantum_error(err2, ["cx", "cz"])
        sim = AerSimulator(noise_model=nm, seed_simulator=seed)
    else:
        sim = AerSimulator(seed_simulator=seed)

    # transpile so custom UnitaryGate + controls decompose into basis gates
    basis = ["u1", "u2", "u3", "rz", "sx", "x", "h", "p", "cx", "cz"]
    tqc = transpile(qc, sim, basis_gates=basis, optimization_level=1)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()

    probs = counts_to_probs(counts, n_bits)

    # Compute SSO against every candidate period r in [2, 2^n_bits - 1]
    Q = 2**n_bits
    sso_by_r = {}
    for r_cand in range(2, Q):
        ep = theoretical_distribution(r_cand, n_bits)
        sso_by_r[r_cand] = sso(probs, ep)

    r_true = multiplicative_order(a, N)
    best_r = max(sso_by_r, key=sso_by_r.get)
    best_sso = sso_by_r[best_r]

    return {
        "N": N,
        "a": a,
        "n_bits": n_bits,
        "n_q": n_q,
        "shots": shots,
        "depol_1q": depol_1q,
        "depol_2q": depol_2q,
        "r_true": r_true,
        "best_r_by_sso": best_r,
        "best_sso": best_sso,
        "sso_at_true_r": sso_by_r.get(r_true, None),
        "sso_by_r": {int(k): float(v) for k, v in sso_by_r.items()},
        "counts": {k: int(v) for k, v in counts.items()},
        "probs": [float(x) for x in probs],
        "n_circuit_ops": dict(tqc.count_ops()),
    }


# ---------------------------------------------------------------------------
# 5. Main experiment sweep
# ---------------------------------------------------------------------------
def main():
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Match the paper's experimental setup (n_bits from paper):
    # - N=15 a=2  : paper uses 3 bits (Q=8)  -> our n_bits=3
    # - N=15 a=11 : paper uses 3 bits        -> our n_bits=3
    # - N=21 a=2  : paper uses 3 bits        -> our n_bits=3
    # (We skip N=35 in the noiseless-verification tier because building
    # its permutation matrix on 7 qubits is fine but the point is the
    # noise-vs-noiseless SSO trend, which N=15,21 already demonstrate.)
    experiments = [
        # (label, N, a, n_bits, depol_1q, depol_2q)
        ("N=15,a=2,noiseless", 15, 2, 3, 0.0, 0.0),
        ("N=15,a=2,depol_p=1e-4", 15, 2, 3, 1e-4, 1e-4),
        ("N=15,a=2,depol_p=1e-3", 15, 2, 3, 1e-3, 1e-3),
        ("N=15,a=2,depol_p=1e-2", 15, 2, 3, 1e-2, 1e-2),
        ("N=15,a=11,noiseless", 15, 11, 3, 0.0, 0.0),
        ("N=15,a=11,depol_p=1e-4", 15, 11, 3, 1e-4, 1e-4),
        ("N=15,a=11,depol_p=1e-3", 15, 11, 3, 1e-3, 1e-3),
        ("N=15,a=11,depol_p=1e-2", 15, 11, 3, 1e-2, 1e-2),
        ("N=21,a=2,noiseless", 21, 2, 3, 0.0, 0.0),
        ("N=21,a=2,depol_p=1e-4", 21, 2, 3, 1e-4, 1e-4),
        ("N=21,a=2,depol_p=1e-3", 21, 2, 3, 1e-3, 1e-3),
        ("N=21,a=2,depol_p=1e-2", 21, 2, 3, 1e-2, 1e-2),
    ]

    all_results = {}
    for label, N, a, n_bits, p1, p2 in experiments:
        print(f"\n=== {label} : N={N} a={a} n_bits={n_bits} depol=({p1},{p2}) ===")
        try:
            res = run_experiment(N, a, n_bits, shots=4096, depol_1q=p1, depol_2q=p2)
            print(f"  r_true={res['r_true']}  best_r_by_sso={res['best_r_by_sso']}  best_sso={res['best_sso']:.4f}  sso@r_true={res['sso_at_true_r']:.4f}")
            print(f"  n_ops={res['n_circuit_ops']}")
            all_results[label] = res
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")
            import traceback; traceback.print_exc()
            all_results[label] = {"error": str(e)}

    # Save
    out_json = out_dir / "shor_replication_results.json"
    with open(out_json, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nWrote {out_json}")

    # Also write a compact summary table
    summary = []
    for label, r in all_results.items():
        if "error" in r:
            summary.append(f"{label:35s}  ERROR: {r['error']}")
            continue
        summary.append(
            f"{label:35s}  r_true={r['r_true']}  best_r={r['best_r_by_sso']}  "
            f"best_SSO={r['best_sso']:.4f}  SSO@r_true={r['sso_at_true_r']:.4f}"
        )
    (out_dir / "shor_replication_summary.txt").write_text("\n".join(summary) + "\n")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
