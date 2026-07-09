#!/usr/bin/env python3
"""
Independent replication of Brassard-Høyer-Tapp (BHT) 1997
"Quantum Algorithm for the Collision Problem", arXiv:quant-ph/9705002.

Core claim (Theorem 1): For a two-to-one function F: X -> Y with |X|=N,
Collision(F, k) finds a collision in expected O(k + sqrt(N/k)) evaluations of F.
Optimum at k = N^(1/3), giving O(N^(1/3)) total evaluations, beating the
classical birthday-attack O(sqrt(N)) lower bound.

This replication:
  1) Implements Collision(F, k) using a REAL Qiskit statevector Grover search
     for step 4 (the quantum sub-search over X \\ K for a value already in table L).
  2) Runs the algorithm on 2-to-1 functions of size N in {8, 16, 32, 64}
     with random permutations composed with the folding map, so f is a genuine
     2-to-1 function with unpredictable collisions.
  3) Uses k = ceil(N^(1/3)) (the paper's optimum), computes the total number of
     F-evaluations (classical table build + Grover queries), and compares to the
     classical birthday-attack baseline (~1.18*sqrt(N)).
  4) Sweeps N and log-log fits query count vs N; expected slope ≈ 1/3 for BHT
     and 1/2 for the classical baseline.

Output: report/evidence/bht_results.json + bht_scaling.csv
"""
import json, math, random, csv, sys, os, time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector

HERE = Path(__file__).resolve().parent


# ---------- 2-to-1 function construction ----------
def make_two_to_one(N: int, seed: int) -> list:
    """Return a length-N list f such that f is 2-to-1: exactly N/2 distinct
    output values, each appearing exactly twice, and their placement in the
    domain is scrambled (so BHT's k random preimages don't trivially collide).

    Construction: pair up domain elements via a random matching, and assign
    each pair a distinct output value from {0..N/2-1}.
    """
    assert N % 2 == 0
    rng = random.Random(seed)
    idx = list(range(N))
    rng.shuffle(idx)
    f = [0] * N
    for j in range(N // 2):
        a, b = idx[2 * j], idx[2 * j + 1]
        f[a] = j
        f[b] = j
    return f


# ---------- classical birthday-attack baseline ----------
def classical_birthday_collision(f, seed):
    """Trial-based classical: draw x uniformly at random *without replacement*
    from X until a collision is seen. Return the number of f-evaluations used.
    Standard birthday-paradox expectation ~ 1.25 * sqrt(N) for a 2-to-1 map.
    """
    rng = random.Random(seed)
    N = len(f)
    order = list(range(N))
    rng.shuffle(order)
    seen = {}
    for count, x in enumerate(order, start=1):
        v = f[x]
        if v in seen and seen[v] != x:
            return count
        seen[v] = x
    return N  # pathological


# ---------- Grover subroutine (real Qiskit statevector) ----------
def grover_find_marked(n_qubits: int, marked_set: set, num_iters: int | None = None,
                       forbidden_set: set | None = None):
    """Run standard Grover on n_qubits with an oracle that marks x iff x in marked_set
    AND x not in forbidden_set. Return (measured_x, prob_of_measured, statevector_success_prob).

    Uses the analytical optimal iteration count when num_iters is None.
    Implemented as a real statevector circuit; measurement is sampled from |psi|^2.
    """
    N = 2 ** n_qubits
    if forbidden_set is None:
        forbidden_set = set()
    effective_marked = {x for x in marked_set if x not in forbidden_set}
    t = len(effective_marked)
    if t == 0:
        return None, 0.0, 0.0

    if num_iters is None:
        # Optimal iterations ≈ floor((pi/4) * sqrt(N/t))
        num_iters = max(1, int(round((math.pi / 4) * math.sqrt(N / t))))

    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))

    # Build a full diagonal oracle (phase-flip marked states)
    # Then a diffusion operator. Small N so we can use an explicit diagonal
    # matrix for the oracle applied to the statevector.
    # Represent oracle as an n-qubit diagonal unitary via UnitaryGate.
    from qiskit.circuit.library import UnitaryGate
    diag = np.ones(N, dtype=complex)
    for x in effective_marked:
        diag[x] = -1.0
    oracle_mat = np.diag(diag)
    oracle_gate = UnitaryGate(oracle_mat, label='O')

    # Diffusion operator = H^n (2|0><0| - I) H^n = 2|s><s| - I on the uniform sup.
    # Easiest: build (2|0><0| - I) as a diagonal with -1 everywhere except +1 at |0>
    diff_diag = -np.ones(N, dtype=complex)
    diff_diag[0] = 1.0
    diff_core = UnitaryGate(np.diag(diff_diag), label='D0')

    for _ in range(num_iters):
        qc.append(oracle_gate, range(n_qubits))
        qc.h(range(n_qubits))
        qc.append(diff_core, range(n_qubits))
        qc.h(range(n_qubits))

    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data) ** 2
    success_prob = float(sum(probs[x] for x in effective_marked))

    rng = np.random.default_rng()
    measured = int(rng.choice(N, p=probs / probs.sum()))
    return measured, float(probs[measured]), success_prob


# ---------- BHT Collision(F, k) with quantum Grover step ----------
def bht_collision(f, k: int, seed: int, verbose: bool = False):
    """Run BHT Collision(F,k). Returns dict with keys:
        {collision, classical_queries, grover_queries, grover_iters,
         grover_success_prob, total_queries, k, N, retries}
    """
    N = len(f)
    n_qubits = int(math.log2(N))
    assert 2 ** n_qubits == N, "N must be a power of two for the Grover register"

    rng = random.Random(seed)
    domain = list(range(N))
    rng.shuffle(domain)
    K = domain[:k]  # random subset of size k

    # Step 1-2: classical table L = {(x, f(x)) : x in K}
    L = {}
    fvals_in_L = {}
    classical_queries = 0
    for x in K:
        v = f[x]
        classical_queries += 1
        L[x] = v
        # Step 3: immediate check for a collision inside K
        if v in fvals_in_L and fvals_in_L[v] != x:
            x0 = fvals_in_L[v]
            return dict(collision=(x0, x), classical_queries=classical_queries,
                        grover_queries=0, grover_iters=0, grover_success_prob=None,
                        total_queries=classical_queries, k=k, N=N, retries=0,
                        source='K-internal')
        fvals_in_L[v] = x

    # Step 4: quantum Grover over X to find x1 in X\K with f(x1) in image(L)
    # Marked set = {x in X : f(x) in image(L) and x not in K}
    image_L = set(L.values())
    marked = {x for x in range(N) if f[x] in image_L and x not in set(K)}
    t = len(marked)
    if t == 0:
        return dict(collision=None, classical_queries=classical_queries,
                    grover_queries=0, grover_iters=0, grover_success_prob=0.0,
                    total_queries=classical_queries, k=k, N=N, retries=0,
                    source='no-marked')

    iters = max(1, int(round((math.pi / 4) * math.sqrt(N / t))))
    # Run Grover; retry up to max_retries if measurement misses (paper uses
    # amplitude-amplification with O(1) expected retries -> O(sqrt(N/t)) queries).
    max_retries = 8
    total_grover_calls = 0
    x1 = None
    success_prob = None
    for attempt in range(max_retries):
        measured, meas_prob, success_prob = grover_find_marked(n_qubits, marked, iters)
        total_grover_calls += iters  # each iteration = 1 oracle F-query
        if measured in marked:
            x1 = measured
            break
    if x1 is None:
        # Fall back to declaring failure (retry counted)
        return dict(collision=None, classical_queries=classical_queries,
                    grover_queries=total_grover_calls, grover_iters=iters,
                    grover_success_prob=success_prob,
                    total_queries=classical_queries + total_grover_calls,
                    k=k, N=N, retries=max_retries, source='grover-failed')

    # Step 5: find x0 in K with f(x0) = f(x1)
    v = f[x1]
    x0 = fvals_in_L[v]

    return dict(collision=(x0, x1), classical_queries=classical_queries,
                grover_queries=total_grover_calls, grover_iters=iters,
                grover_success_prob=success_prob,
                total_queries=classical_queries + total_grover_calls,
                k=k, N=N, retries=attempt, source='K-vs-X')


def verify(f, coll):
    if coll is None:
        return False
    x0, x1 = coll
    return x0 != x1 and f[x0] == f[x1]


def run_experiment(Ns, trials_per_N=10, base_seed=42):
    rows = []
    for N in Ns:
        n_qubits = int(math.log2(N))
        assert 2 ** n_qubits == N
        k_opt = max(1, int(round(N ** (1/3))))

        bht_totals = []
        bht_classicals = []
        bht_grovers = []
        bht_iters_list = []
        bht_success_probs = []
        bht_ok = 0
        classical_baseline = []

        for t in range(trials_per_N):
            seed = base_seed + 1000 * N + t
            f = make_two_to_one(N, seed=seed)

            # BHT
            r = bht_collision(f, k=k_opt, seed=seed + 1)
            if verify(f, r['collision']):
                bht_ok += 1
            bht_totals.append(r['total_queries'])
            bht_classicals.append(r['classical_queries'])
            bht_grovers.append(r['grover_queries'])
            bht_iters_list.append(r['grover_iters'])
            if r['grover_success_prob'] is not None:
                bht_success_probs.append(r['grover_success_prob'])

            # Classical birthday baseline (independent trial)
            cq = classical_birthday_collision(f, seed=seed + 2)
            classical_baseline.append(cq)

        rows.append(dict(
            N=N,
            n_qubits=n_qubits,
            k_opt=k_opt,
            trials=trials_per_N,
            bht_success_rate=bht_ok / trials_per_N,
            bht_mean_total_queries=float(np.mean(bht_totals)),
            bht_median_total_queries=float(np.median(bht_totals)),
            bht_mean_classical_queries=float(np.mean(bht_classicals)),
            bht_mean_grover_queries=float(np.mean(bht_grovers)),
            bht_mean_grover_iters=float(np.mean(bht_iters_list)),
            bht_mean_grover_success_prob=float(np.mean(bht_success_probs)) if bht_success_probs else None,
            classical_mean_queries=float(np.mean(classical_baseline)),
            classical_median_queries=float(np.median(classical_baseline)),
            N_cuberoot=N ** (1/3),
            N_sqrt=math.sqrt(N),
        ))
        print(f"N={N:3d}: k={k_opt}, BHT total={np.mean(bht_totals):.2f} "
              f"(cls {np.mean(bht_classicals):.2f} + qm {np.mean(bht_grovers):.2f}), "
              f"success={bht_ok}/{trials_per_N}, "
              f"classical baseline={np.mean(classical_baseline):.2f} "
              f"(N^(1/3)={N**(1/3):.2f}, sqrt(N)={math.sqrt(N):.2f})")

    return rows


def loglog_fit(xs, ys):
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    logx = np.log(xs)
    logy = np.log(ys)
    slope, intercept = np.polyfit(logx, logy, 1)
    return float(slope), float(intercept)


def main():
    Ns = [8, 16, 32, 64, 128, 256, 512, 1024]
    trials_per_N = 30
    print(f"Running BHT vs classical on N in {Ns}, trials={trials_per_N} each...")
    t0 = time.time()
    rows = run_experiment(Ns, trials_per_N=trials_per_N)
    dt = time.time() - t0

    # Fit scaling
    Ns_arr = [r['N'] for r in rows]
    bht_ys = [r['bht_mean_total_queries'] for r in rows]
    cls_ys = [r['classical_mean_queries'] for r in rows]
    bht_slope, bht_int = loglog_fit(Ns_arr, bht_ys)
    cls_slope, cls_int = loglog_fit(Ns_arr, cls_ys)

    result = dict(
        paper='arXiv:quant-ph/9705002 (Brassard, Høyer, Tapp 1997)',
        method='BHT Collision(F, k=ceil(N^(1/3))) with real Qiskit statevector Grover step',
        qiskit_version=__import__('qiskit').__version__,
        trials_per_N=trials_per_N,
        Ns=Ns,
        rows=rows,
        loglog_fit_bht_slope=bht_slope,
        loglog_fit_bht_intercept=bht_int,
        loglog_fit_classical_slope=cls_slope,
        loglog_fit_classical_intercept=cls_int,
        expected_bht_slope=1/3,
        expected_classical_slope=1/2,
        runtime_sec=dt,
    )

    out_json = HERE / 'bht_results.json'
    with open(out_json, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved {out_json}")

    out_csv = HERE / 'bht_scaling.csv'
    with open(out_csv, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Saved {out_csv}")

    print(f"\n=== SCALING FIT ===")
    print(f"BHT log-log slope       = {bht_slope:.3f}  (paper expects 1/3 = 0.333)")
    print(f"Classical log-log slope = {cls_slope:.3f}  (birthday expects 1/2 = 0.500)")
    print(f"Runtime: {dt:.1f}s")


if __name__ == '__main__':
    main()
