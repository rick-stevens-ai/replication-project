#!/usr/bin/env python3
"""
Replication of MLE-based Amplitude Estimation from
"Low depth amplitude estimation on a trapped ion quantum computer"
Giurgica-Tiron et al., arXiv:2109.09685 (2021), Algorithm IV.1.

We reproduce the core noiseless-simulation kernel using Qiskit Aer:
  - Oracle A: single-qubit Ry(2 theta) so that A|0> = cos(theta)|0> + sin(theta)|1>
    (this is the canonical toy AE oracle; equivalent statistics to the
    inner-product oracle for the MLE reconstruction, which only sees
    the good-state probability = sin^2((2d+1) theta) at depth d).
  - Grover operator Q = -A S0 A^dagger S_chi (implemented as
    S_chi = Z on the ancilla-good bit, and A S0 A^dagger = reflection about |psi>).
  - Depth-d circuit: A followed by Q^d, measure.
  - Schedule: linear (t, N_shot=500) with t = 0..T_max as in paper (T_max up to 7).
  - MLE: brute-force grid search over theta in [0, pi/2] using
      log L(theta) = sum_d [ N0_d * 2*log|cos((2d+1)theta)| + N1_d * 2*log|sin((2d+1)theta)| ]
    with epsilon = 1e-3 grid (1000 buckets) exactly as paper.

Outputs JSON to artifacts/ so downstream analysis / plotting is deterministic.
"""

import argparse, json, os, sys, time
from pathlib import Path
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_depth_d_circuit(theta_true: float, d: int) -> QuantumCircuit:
    """Single-qubit AE toy circuit at depth d.

    A = Ry(2*theta_true).  Good state = |1>.
    Grover Q applied d times.  After A * Q^d, P(measure 1) = sin^2((2d+1) theta_true).
    Implementation: build the explicit unitary by successive multiplication
    is not necessary — we can use the identity that G^d A produces the state
    sin((2d+1) theta_true) |1> + cos((2d+1) theta_true) |0>.
    But per the paper's spirit (and to keep this a real quantum circuit run,
    not an analytic shortcut), we build A and Q as gate sequences and let
    Qiskit-Aer compute the amplitudes.
    """
    qc = QuantumCircuit(1, 1)
    # A |0> = cos(theta)|0> + sin(theta)|1>  -->  Ry(2*theta)
    two_theta = 2.0 * theta_true
    qc.ry(two_theta, 0)
    # Grover operator Q = -A S_0 A^dagger S_chi
    #   S_chi = Z (marks |1>)
    #   A S_0 A^dagger = reflection about |A|0>> = 2|psi><psi| - I
    #     For single qubit and A = Ry(2 theta):
    #       A S_0 A^dagger  ==  Ry(2 theta) Z Ry(-2 theta)   (S_0 = Z on the |0> subspace? actually S_0 = 2|0><0|-I = Z with a global phase up to sign)
    # Cleanest: implement Q as its full 2x2 matrix.
    # But per "real circuit" we can just apply the equivalent gate sequence:
    #   Q = -A * Z0 * A^dagger * Z  where Z0 marks |0>.
    #   Z0 = X Z X (up to global phase, marks |0>)
    for _ in range(d):
        # S_chi: mark good state |1> with phase -1  -->  Z
        qc.z(0)
        # A S_0 A^dagger: reflection about A|0>
        qc.ry(-two_theta, 0)
        qc.z(0)
        # S_0 marks |0> instead of |1>; standard trick: S_0 = X Z X
        qc.x(0); qc.z(0); qc.x(0)
        # actually simpler: S_0 (reflection about |0>) is Z with a sign flip on |1>.
        # For a single qubit: 2|0><0| - I = diag(1,-1) = Z.  So S_0 = Z.
        # Above we did Z then X Z X = Z * (-Z) = -I on the state, that's wrong.
        # Rewrite properly below.
        pass

    return qc


def build_depth_d_circuit_v2(theta_true: float, d: int) -> QuantumCircuit:
    """Cleaner build: G = A * S0 * A^dagger * S_chi where
       S_chi = Z (marks good state |1> with phase -1)
       S_0   = Z with sign flip (marks bad/|0>); on 1 qubit S_0 acts as diag(-1,1) = -Z
    So G = -A * Z * A^dagger * Z, and G^d A on |0> has probability sin^2((2d+1)theta) on |1>.
    We drop the global -1 (irrelevant for probabilities).
    """
    two_theta = 2.0 * theta_true
    qc = QuantumCircuit(1, 1)
    qc.ry(two_theta, 0)  # A
    for _ in range(d):
        qc.z(0)            # S_chi
        qc.ry(-two_theta, 0)  # A^dagger
        qc.z(0)            # S_0 (up to global sign)
        qc.ry(two_theta, 0)   # A
    qc.measure(0, 0)
    return qc


def run_schedule(theta_true: float, T_max: int, n_shot: int, seed: int) -> dict:
    """Run circuits at depths 0..T_max with n_shot each. Return counts dict."""
    sim = AerSimulator(seed_simulator=seed)
    depth_counts = {}
    for d in range(0, T_max + 1):
        qc = build_depth_d_circuit_v2(theta_true, d)
        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=n_shot).result()
        counts = result.get_counts()
        n1 = counts.get("1", 0)
        n0 = counts.get("0", 0)
        depth_counts[d] = {"n0": int(n0), "n1": int(n1),
                           "p_hat_1": n1 / (n0 + n1),
                           "p_true_1": float(np.sin((2*d + 1) * theta_true)**2)}
    return depth_counts


def mle_theta(depth_counts: dict, eps: float = 1e-3) -> float:
    """Grid-search MLE for theta in (0, pi/2) with 1/eps buckets (paper: eps=0.001 -> 1000 buckets)."""
    n_buckets = int(round(1.0/eps))
    thetas = (np.arange(n_buckets) + 0.5) * (np.pi/2) / n_buckets  # midpoints in (0, pi/2)
    logL = np.zeros_like(thetas)
    for d, c in depth_counts.items():
        m = 2*d + 1
        s = np.sin(m * thetas); co = np.cos(m * thetas)
        # avoid log(0)
        s2 = np.clip(s**2, 1e-300, 1.0); c2 = np.clip(co**2, 1e-300, 1.0)
        logL += c["n1"] * np.log(s2) + c["n0"] * np.log(c2)
    k_star = int(np.argmax(logL))
    return float(thetas[k_star])


def total_oracle_calls(T_max: int, n_shot: int) -> int:
    """N_q = sum_{d=0..T_max} n_shot * (2d+1) (each Q application counts as 1 oracle call;
       plus the initial A adds 1 per shot; consistent with the paper's x-axis)."""
    return int(sum(n_shot * (2*d + 1) for d in range(0, T_max + 1)))


def total_oracle_calls_classical(N_shot: int) -> int:
    """Classical direct sampling from A alone."""
    return int(N_shot)


def rmse(estimates: list, truth: float) -> float:
    a = np.array(estimates)
    return float(np.sqrt(np.mean((a - truth)**2)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=0.3, help="true amplitude a = sin(theta)")
    ap.add_argument("--Tmax", type=int, default=7, help="max Grover depth (paper: 7)")
    ap.add_argument("--nshot", type=int, default=500, help="shots per depth (paper: 500)")
    ap.add_argument("--eps", type=float, default=1e-3, help="MLE bucket width (paper: 0.001)")
    ap.add_argument("--trials", type=int, default=25, help="repeat trials for RMSE")
    ap.add_argument("--Tmax_scan", type=int, nargs="+", default=[0, 1, 2, 3, 4, 5, 6, 7],
                    help="depths at which to compute cumulative RMSE-vs-Nq")
    ap.add_argument("--out", type=str, required=True, help="output JSON path")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    theta_true = float(np.arcsin(args.a))
    print(f"[cfg] true a={args.a}  theta={theta_true:.6f}  Tmax={args.Tmax}  nshot={args.nshot}  trials={args.trials}")

    all_out = {
        "config": vars(args),
        "theta_true": theta_true,
        "a_true": args.a,
        "trials": [],
        "rmse_vs_Tmax": {},
        "rmse_classical_vs_Nshot": {},
        "qiskit_version": None,
        "aer_version": None,
    }
    import qiskit, qiskit_aer
    all_out["qiskit_version"] = qiskit.__version__
    all_out["aer_version"] = qiskit_aer.__version__

    rng = np.random.default_rng(args.seed)

    # ---- MLE quantum: for each trial, run the full schedule 0..Tmax and for each subset 0..T compute MLE
    trial_records = []
    for trial in range(args.trials):
        seed_t = int(rng.integers(1, 2**31 - 1))
        depth_counts = run_schedule(theta_true, args.Tmax, args.nshot, seed_t)
        # For each Tmax in scan, MLE using depths 0..T
        est_by_T = {}
        for T in args.Tmax_scan:
            sub = {d: depth_counts[d] for d in range(0, T+1)}
            theta_hat = mle_theta(sub, eps=args.eps)
            a_hat = float(np.sin(theta_hat))
            est_by_T[T] = {"theta_hat": theta_hat, "a_hat": a_hat,
                           "abs_err_a": abs(a_hat - args.a),
                           "N_q": total_oracle_calls(T, args.nshot)}
        trial_records.append({"trial": trial, "seed": seed_t,
                              "depth_counts": depth_counts, "est_by_T": est_by_T})
        if (trial+1) % 5 == 0:
            print(f"[trial {trial+1}/{args.trials}] a_hat(Tmax={args.Tmax})={est_by_T[args.Tmax]['a_hat']:.4f}")

    all_out["trials"] = trial_records

    # Aggregate RMSE vs T
    for T in args.Tmax_scan:
        a_hats = [rec["est_by_T"][T]["a_hat"] for rec in trial_records]
        N_q = trial_records[0]["est_by_T"][T]["N_q"]
        r = rmse(a_hats, args.a)
        all_out["rmse_vs_Tmax"][str(T)] = {"N_q": N_q, "rmse_a": r,
                                            "mean_a_hat": float(np.mean(a_hats)),
                                            "std_a_hat": float(np.std(a_hats))}
        print(f"[MLE] T={T}  N_q={N_q:>7d}  RMSE(a)={r:.5f}")

    # ---- Classical direct sampling: draw N samples from Bernoulli(a^2) and estimate a = sqrt(p_hat)
    # Use N_shot values matched to MLE N_q so log-log slope comparison is fair.
    Nq_targets = [all_out["rmse_vs_Tmax"][str(T)]["N_q"] for T in args.Tmax_scan]
    for N in Nq_targets:
        a_hats_cls = []
        for _ in range(args.trials):
            n1 = rng.binomial(N, args.a**2)
            p_hat = n1 / N
            a_hat = float(np.sqrt(max(0.0, min(1.0, p_hat))))
            a_hats_cls.append(a_hat)
        r = rmse(a_hats_cls, args.a)
        all_out["rmse_classical_vs_Nshot"][str(N)] = {"N_q": int(N), "rmse_a": r,
                                                       "mean_a_hat": float(np.mean(a_hats_cls))}
        print(f"[classical] N={N:>7d}  RMSE(a)={r:.5f}")

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(all_out, indent=2))
    print(f"[done] wrote {outp}")


if __name__ == "__main__":
    main()
