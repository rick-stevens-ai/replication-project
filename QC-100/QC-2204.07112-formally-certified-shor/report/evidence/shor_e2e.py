#!/usr/bin/env python3
"""
End-to-end functional replication of Shor's factorization algorithm
for QC-100 replication of arXiv:2204.07112.

Paper reproducible headline (from Fig. 4b):
  - N=15 factorization empirical success probability ~43.77%
    (proved lower bound 0.17%) using their extracted OpenQASM circuit.
  - N=7 order finding (a=3) empirical success rate ~28.40%
    for correct order r=6 (proved lower bound 0.34%).

This script does NOT reproduce their Coq→OCaml→OpenQASM extraction
pipeline. It DOES reproduce, end-to-end, the *executable functional
check* that the certified impl claims: for a=coprime to N, the
Shor quantum order-finding subroutine + continued-fractions post-
processing recovers a non-trivial factor of N with reasonable
frequency across shots on a Qiskit statevector simulator.

Checks performed:
  (a) Modular exponentiation unitary is correct on classical basis
      states: U|y> = |a*y mod N> for y in [0, N-1].
  (b) QFT + measurement on the phase register produces measurement
      outcomes whose ratios s/2^m are close to k/r for k in [0,r-1].
  (c) Continued-fractions post-processing recovers r; then
      gcd(a^{r/2} +/- 1, N) yields a non-trivial factor of N.

Instances: N=15 (headline), and N=21 if time permits.
"""

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from math import gcd

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator


# ---------- (a) Modular exponentiation as controlled unitary ----------

def c_amod_n(a: int, power: int, N: int, n_target: int) -> QuantumCircuit:
    """Controlled multiplication by a^power mod N on the target register.

    Implementation approach: build the modular multiplication as a
    permutation matrix on the |0..2^n_target-1> basis, then wrap as
    a Gate via UnitaryGate. This is O(2^n_target)-size classically
    but gives an EXACT quantum operation for the small N we test.
    """
    from qiskit.circuit.library import UnitaryGate

    dim = 1 << n_target
    a_pow = pow(a, power, N)
    U = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < N:
            U[(a_pow * y) % N, y] = 1
        else:
            # Leave states |y>=|N..dim-1> as identity (they never appear
            # during the algorithm because we init the target to |1>).
            U[y, y] = 1
    gate = UnitaryGate(U, label=f"{a}^{power} mod {N}")
    c_gate = gate.control(1)
    qc = QuantumCircuit(1 + n_target, name=f"c-{a}^{power}mod{N}")
    qc.append(c_gate, list(range(1 + n_target)))
    return qc


def verify_modexp_classical(a: int, N: int) -> dict:
    """CHECK (a): the modexp unitary really does |y> -> |a*y mod N>.

    Verifies for all classical basis states y in [0, N-1] by running
    the (controlled) unitary with control=|1> on |y> and checking
    the resulting state is a computational basis state |a*y mod N>.
    """
    n_target = max(1, int(math.ceil(math.log2(N))))
    sim = AerSimulator(method="statevector")
    errors = []
    for y in range(N):
        qc = QuantumCircuit(1 + n_target, name="check")
        # control qubit
        qc.x(0)
        # prepare |y> on target (little-endian, qiskit)
        for bit in range(n_target):
            if (y >> bit) & 1:
                qc.x(1 + bit)
        qc.append(c_amod_n(a, 1, N, n_target).to_gate(), list(range(1 + n_target)))
        qc.save_statevector()
        result = sim.run(transpile(qc, sim)).result()
        sv = np.asarray(result.get_statevector())
        # Expected basis state index: control=1 at qubit 0, target=(a*y mod N)
        expected = 1 | (((a * y) % N) << 1)
        # Find nonzero amplitude
        idx = int(np.argmax(np.abs(sv)))
        amp = complex(sv[idx])
        if idx != expected or abs(abs(amp) - 1.0) > 1e-8:
            errors.append({"y": y, "expected_idx": expected, "got_idx": idx,
                            "amp": [amp.real, amp.imag]})
    return {"check": "modexp_classical", "a": a, "N": N, "n_target": n_target,
            "cases_tested": N, "errors": errors, "pass": len(errors) == 0}


# ---------- (b) QPE / order-finding circuit ----------

def build_order_finding_circuit(a: int, N: int, n_count: int) -> QuantumCircuit:
    """Build Shor's order-finding circuit for a given a, N with n_count
    counting qubits (m in the paper). Target has n_target = ceil(log2 N)
    qubits, initialized to |1>."""
    n_target = max(1, int(math.ceil(math.log2(N))))
    qc = QuantumCircuit(n_count + n_target, n_count)
    # Initialize counting register in uniform superposition
    for q in range(n_count):
        qc.h(q)
    # Initialize target register to |1>
    qc.x(n_count)  # least significant target qubit
    # Controlled-U^{2^j}
    for j in range(n_count):
        power = 1 << j
        cU = c_amod_n(a, power, N, n_target).to_gate()
        cU.name = f"c-{a}^{power} mod {N}"
        qubits = [j] + [n_count + t for t in range(n_target)]
        qc.append(cU, qubits)
    # Inverse QFT on counting register
    qc.append(QFT(n_count, inverse=True, do_swaps=True).to_gate(label="IQFT"),
              list(range(n_count)))
    qc.measure(range(n_count), range(n_count))
    return qc


# ---------- (c) Continued-fractions post-processing ----------

def cf_recover_order(measured: int, n_count: int, N: int) -> list:
    """Given a measurement outcome s in [0, 2^n_count), return candidate
    orders r via continued fractions applied to s / 2^n_count, keeping
    denominators <= N."""
    if measured == 0:
        return []
    frac = Fraction(measured, 1 << n_count).limit_denominator(N)
    candidates = []
    if frac.denominator > 0:
        candidates.append(frac.denominator)
    # Also try nearby convergents by scanning limit_denominator over N/2..N
    for lim in [N, N - 1, N // 2, max(2, N // 3)]:
        f = Fraction(measured, 1 << n_count).limit_denominator(lim)
        if f.denominator not in candidates and f.denominator > 0:
            candidates.append(f.denominator)
    return candidates


def try_factor_from_order(a: int, N: int, r: int):
    """Given candidate order r, try to extract a non-trivial factor of N."""
    if r <= 0 or r % 2 != 0:
        return None
    if pow(a, r, N) != 1:
        return None
    x = pow(a, r // 2, N)
    if x == N - 1:
        return None
    f1 = gcd(x - 1, N)
    f2 = gcd(x + 1, N)
    for f in (f1, f2):
        if 1 < f < N:
            return f
    return None


# ---------- Full end-to-end factorization ----------

def coprime_candidates(N: int):
    return [a for a in range(2, N) if gcd(a, N) == 1]


def run_shor(N: int, shots: int = 4096, n_count: int | None = None,
             a_list: list | None = None, seed: int = 0):
    """Run end-to-end Shor's factorization for N.

    Returns dict with per-a stats and aggregate empirical success prob.
    """
    n_target = max(1, int(math.ceil(math.log2(N))))
    if n_count is None:
        n_count = 2 * n_target + 1  # standard Shor choice (>= 2n)
    if a_list is None:
        a_list = coprime_candidates(N)
    sim = AerSimulator(seed_simulator=seed)
    per_a = []
    global_success = 0
    global_shots = 0
    for a in a_list:
        # Classical order (for reference)
        r_true = 1
        while pow(a, r_true, N) != 1:
            r_true += 1
        qc = build_order_finding_circuit(a, N, n_count)
        tqc = transpile(qc, sim)
        job = sim.run(tqc, shots=shots)
        counts = job.result().get_counts()
        success = 0
        outcomes = 0
        recovered_r = {}
        found_factors = set()
        for bitstring, c in counts.items():
            outcomes += c
            # qiskit returns big-endian classical bit string; convert
            measured = int(bitstring, 2)
            cands = cf_recover_order(measured, n_count, N)
            # Try multiples too (r/2, r, 2r) since CF might return factor
            expanded = set()
            for r in cands:
                for k in (1, 2, 3):
                    rr = r * k
                    if rr <= 2 * N:
                        expanded.add(rr)
            factor_here = None
            for rr in expanded:
                f = try_factor_from_order(a, N, rr)
                if f is not None:
                    factor_here = f
                    break
            if factor_here is not None:
                success += c
                found_factors.add(factor_here)
                recovered_r.setdefault(rr, 0)
                recovered_r[rr] += c
        per_a.append({
            "a": a,
            "r_true": r_true,
            "shots": outcomes,
            "success": success,
            "success_prob": success / outcomes,
            "factors_found": sorted(found_factors),
            "recovered_r_hist": recovered_r,
        })
        global_success += success
        global_shots += outcomes
    aggregate = {
        "N": N,
        "n_count": n_count,
        "n_target": n_target,
        "shots_per_a": shots,
        "a_list": a_list,
        "global_success_prob": global_success / global_shots if global_shots else 0.0,
        "per_a": per_a,
    }
    return aggregate


# ---------- Order-finding (N=7, a=3) reproduction ----------

def run_order_finding(a: int, N: int, shots: int = 100000,
                      n_count: int | None = None, seed: int = 0):
    n_target = max(1, int(math.ceil(math.log2(N))))
    if n_count is None:
        n_count = 2 * n_target + 1
    r_true = 1
    while pow(a, r_true, N) != 1:
        r_true += 1
    sim = AerSimulator(seed_simulator=seed)
    qc = build_order_finding_circuit(a, N, n_count)
    tqc = transpile(qc, sim)
    job = sim.run(tqc, shots=shots)
    counts = job.result().get_counts()
    correct_r_shots = 0
    total = 0
    for bitstring, c in counts.items():
        total += c
        measured = int(bitstring, 2)
        cands = cf_recover_order(measured, n_count, N)
        if r_true in cands:
            correct_r_shots += c
    return {
        "a": a, "N": N, "n_count": n_count, "n_target": n_target,
        "shots": total, "r_true": r_true,
        "correct_r_shots": correct_r_shots,
        "empirical_success_prob": correct_r_shots / total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=15)
    parser.add_argument("--shots", type=int, default=4096)
    parser.add_argument("--n-count", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--include-of7", action="store_true",
                        help="Also run N=7, a=3 order finding replication.")
    parser.add_argument("--include-21", action="store_true",
                        help="Also run N=21 factorization (slower).")
    parser.add_argument("--out", type=str, default="/tmp/shor_result.json")
    args = parser.parse_args()

    t0 = time.time()
    print(f"[shor_e2e] Starting; N={args.N} shots={args.shots}")

    # (a) modexp classical correctness for at least one coprime a
    a_check = None
    for a in range(2, args.N):
        if gcd(a, args.N) == 1:
            a_check = a
            break
    print(f"[shor_e2e] (a) verifying modexp unitary for a={a_check}, N={args.N} ...")
    modexp = verify_modexp_classical(a_check, args.N)
    print(f"[shor_e2e]   -> pass={modexp['pass']} errors={len(modexp['errors'])}")

    # (b)+(c) full run for N
    print(f"[shor_e2e] (b)+(c) running full Shor on N={args.N} across all coprime a ...")
    result_N = run_shor(args.N, shots=args.shots, n_count=args.n_count, seed=args.seed)
    print(f"[shor_e2e]   -> N={args.N} global success prob = {result_N['global_success_prob']:.4f}")

    output = {
        "paper": "arXiv:2204.07112",
        "modexp_check": modexp,
        "factorization": {str(args.N): result_N},
    }

    if args.include_of7:
        print("[shor_e2e] order finding replication N=7 a=3 ...")
        of7 = run_order_finding(3, 7, shots=100000, seed=args.seed)
        print(f"[shor_e2e]   -> N=7 a=3 emp success = {of7['empirical_success_prob']:.4f}")
        output["order_finding_N7_a3"] = of7

    if args.include_21:
        print("[shor_e2e] factorization replication N=21 ...")
        result_21 = run_shor(21, shots=args.shots, seed=args.seed)
        print(f"[shor_e2e]   -> N=21 global success prob = {result_21['global_success_prob']:.4f}")
        output["factorization"]["21"] = result_21

    dt = time.time() - t0
    output["elapsed_sec"] = dt
    with open(args.out, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"[shor_e2e] wrote {args.out} in {dt:.1f}s")


if __name__ == "__main__":
    main()
