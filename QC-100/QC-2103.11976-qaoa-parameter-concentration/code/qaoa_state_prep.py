"""
Independent replication of arXiv:2103.11976 (Akshay, Rabinovich, Campos, Biamonte 2021)
"Parameter Concentration in Quantum Approximate Optimization"

Central claim tested:
  For QAOA variational state preparation with target |t> = |0...0> (all-zeros),
  problem Hamiltonian Hz = 1 - |t><t|, and mixer Hx = sum_i X_i,
  optimal circuit parameters concentrate as 1/n:
    p=1:  beta*  = pi/n  - 4 pi/n^2 + O(n^-3),   approximated by  beta = pi/(n+2)
          gamma* = pi - 2 pi/n + 8 pi/n^2 + O(n^-3),  approximated by  gamma = pi * (n+2)/(n+4)
  The concentration |theta_{n+1} - theta_n|^2 scales as O(1/n^4).

Approach:
  (A) Use the paper's exact analytical overlap F_1(gamma, beta) from eq. (5),
      evaluate on a fine grid + local refinement (scipy) to find OPT parameters for n=4..20.
  (B) Cross-verify at small n (n=4,6,8) by BUILDING the actual QAOA circuit in Qiskit
      and computing overlap from statevector -- this proves eq. (5) matches a real circuit
      and validates the analytical approach we're using for the sweep.

Outputs saved as JSON + CSV under report/evidence/.
"""
import json
import math
import os
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVID = os.path.join(ROOT, "report", "evidence")
os.makedirs(EVID, exist_ok=True)


# -----------------------------------------------------------------------------
# (A) Analytical overlap from paper eq. (5)
# -----------------------------------------------------------------------------
def F1(gamma, beta, n):
    """Overlap |<t|psi(gamma,beta)>|^2 for p=1 QAOA state-prep, eq. (5) of the paper.

    F1 = (1/2^n) * [ 1 + 2 cos^n(beta) * (cos(gamma - n beta) - cos(n beta))
                      + 2 cos^{2n}(beta) * (1 - cos gamma) ]
    """
    cb = math.cos(beta)
    cb_n = cb ** n
    cb_2n = cb ** (2 * n)
    return (1.0 / (2.0 ** n)) * (
        1.0
        + 2.0 * cb_n * (math.cos(gamma - n * beta) - math.cos(n * beta))
        + 2.0 * cb_2n * (1.0 - math.cos(gamma))
    )


def neg_F1(x, n):
    return -F1(x[0], x[1], n)


def optimize_p1(n, n_starts=64, seed=0):
    """Grid + local refinement to find global max of F1 on gamma in [0, 2 pi), beta in [0, pi).

    Returns (gamma*, beta*, F*).  Uses the paper's asymptotic guess as one of the seeds,
    plus a random grid, so we don't miss the target basin.
    """
    rng = np.random.default_rng(seed)
    best = (None, None, -1.0)

    # Deterministic seeds: paper's approximations + coarse grid
    seeds = [
        (math.pi * (n + 2) / (n + 4), math.pi / (n + 2)),  # paper approximation
        (math.pi - 2 * math.pi / n, math.pi / n),  # leading-order asymptotic
    ]
    # Add random seeds
    for _ in range(n_starts):
        g0 = rng.uniform(0, 2 * math.pi)
        b0 = rng.uniform(0, math.pi)
        seeds.append((g0, b0))

    for (g0, b0) in seeds:
        res = minimize(
            neg_F1,
            x0=[g0, b0],
            args=(n,),
            method="L-BFGS-B",
            bounds=[(0.0, 2 * math.pi), (0.0, math.pi)],
        )
        val = -res.fun
        if val > best[2]:
            best = (float(res.x[0]), float(res.x[1]), float(val))

    return best  # gamma*, beta*, F*


# -----------------------------------------------------------------------------
# p=2 analytical amplitude via eq. (4), (13); overlap = |g2|^2
# g1(gamma, beta) = (1/sqrt(2^n)) * ( exp(-i beta n) + cos^n(beta) * (exp(-i gamma) - 1) )
# g2(gamma1, beta1, gamma2, beta2) = g1(gamma1, beta1 + beta2)
#                                    + g1(gamma1, beta1) * cos^n(beta2) * (exp(-i gamma2) - 1)
# -----------------------------------------------------------------------------
def g1(gamma, beta, n):
    return (1.0 / math.sqrt(2.0 ** n)) * (
        np.exp(-1j * beta * n) + (math.cos(beta) ** n) * (np.exp(-1j * gamma) - 1.0)
    )


def F2(g1_a, b1, g2_a, b2, n):
    amp = g1(g1_a, b1 + b2, n) + g1(g1_a, b1, n) * (math.cos(b2) ** n) * (
        np.exp(-1j * g2_a) - 1.0
    )
    return float(np.abs(amp) ** 2)


def neg_F2(x, n):
    return -F2(x[0], x[1], x[2], x[3], n)


def optimize_p2(n, n_starts=128, seed=0):
    rng = np.random.default_rng(seed)
    best = (None, None, None, None, -1.0)
    # Seed with paper's asymptotics for p=2 (eqs. 15-18):
    # beta2 ~ pi/n - 4 pi/n^2, gamma2 ~ pi - 2 pi/n, beta1 ~ pi/n, gamma1 ~ pi
    seeds = [
        (math.pi, math.pi / n, math.pi - 2 * math.pi / n, math.pi / n - 4 * math.pi / (n * n)),
        (math.pi * (n + 2) / (n + 4), math.pi / (n + 4), math.pi, math.pi / n),
    ]
    for _ in range(n_starts):
        seeds.append(
            (
                rng.uniform(0, 2 * math.pi),
                rng.uniform(0, math.pi),
                rng.uniform(0, 2 * math.pi),
                rng.uniform(0, math.pi),
            )
        )
    for s in seeds:
        res = minimize(
            neg_F2,
            x0=list(s),
            args=(n,),
            method="L-BFGS-B",
            bounds=[
                (0.0, 2 * math.pi),
                (0.0, math.pi),
                (0.0, 2 * math.pi),
                (0.0, math.pi),
            ],
        )
        val = -res.fun
        if val > best[4]:
            best = (
                float(res.x[0]),
                float(res.x[1]),
                float(res.x[2]),
                float(res.x[3]),
                float(val),
            )
    return best  # g1, b1, g2, b2, F


# -----------------------------------------------------------------------------
# (B) Qiskit statevector cross-check for small n
# -----------------------------------------------------------------------------
def qiskit_overlap_p1(gamma, beta, n):
    """Build a real QAOA circuit in Qiskit and return overlap |<0...0|psi>|^2.

    QAOA state-prep with target |t> = |0...0>:
      U_C(gamma) = exp(-i gamma |t><t|) = diag(exp(-i gamma), 1, ..., 1) on 2^n states
      U_M(beta)  = prod_i exp(-i beta X_i) = tensor product of RX(2*beta)
      Init state = |+>^n = H^{otimes n} |0...0>
      psi = U_M(beta) U_C(gamma) |+>^n
    """
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector, Operator
    import numpy as _np

    qc = QuantumCircuit(n)
    # Init |+>^n
    for i in range(n):
        qc.h(i)
    # U_C(gamma): diagonal, e^{-i gamma} on |0...0>, 1 elsewhere.
    # Build as a multi-controlled phase on all-zero using X-sandwich trick:
    # flip all qubits, apply n-controlled Rz on last qubit that gives global phase e^{-i gamma},
    # flip back. Simpler: construct the diagonal Operator directly.
    diag = _np.ones(2 ** n, dtype=complex)
    diag[0] = _np.exp(-1j * gamma)  # index 0 = |0...0>
    from qiskit.circuit.library import Diagonal

    qc.append(Diagonal(diag.tolist()), list(range(n)))
    # U_M(beta): RX(2*beta) on each qubit
    for i in range(n):
        qc.rx(2 * beta, i)

    sv = Statevector.from_instruction(qc)
    amp = sv.data[0]  # <0...0|psi>
    return float(abs(amp) ** 2)


# -----------------------------------------------------------------------------
# Main sweeps
# -----------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Independent replication of arXiv:2103.11976 (parameter concentration)")
    print("=" * 70)

    # ---- p=1 sweep ----
    print("\n[p=1] Sweeping n = 4..20 with analytical F1 (eq. 5)...")
    p1_rows = []
    for n in range(4, 21):
        g, b, F = optimize_p1(n)
        # Paper approximations for comparison:
        beta_paper = math.pi / (n + 2)
        gamma_paper = math.pi * (n + 2) / (n + 4)
        # Leading-order asymptotic (eqs. 9, 10):
        beta_asymp = math.pi / n - 4 * math.pi / (n * n)
        gamma_asymp = math.pi - 2 * math.pi / n + 8 * math.pi / (n * n)
        p1_rows.append(
            {
                "n": n,
                "gamma_opt": g,
                "beta_opt": b,
                "overlap": F,
                "beta_paper_approx": beta_paper,   # pi/(n+2)
                "gamma_paper_approx": gamma_paper,  # pi*(n+2)/(n+4)
                "beta_asymptotic": beta_asymp,
                "gamma_asymptotic": gamma_asymp,
            }
        )
        print(
            f"  n={n:2d}  gamma*={g:.6f}  beta*={b:.6f}  F*={F:.6f}   "
            f"beta_paper={beta_paper:.6f}  gamma_paper={gamma_paper:.6f}"
        )

    # ---- Concentration diagnostic: |theta_{n+1} - theta_n|^2 vs 1/n^4 ----
    print("\n[p=1] Concentration diagnostic |Delta|^2 vs n:")
    conc_rows = []
    for i in range(len(p1_rows) - 1):
        a, b_ = p1_rows[i], p1_rows[i + 1]
        # Some optima admit the beta -> pi - beta, gamma -> 2 pi - gamma symmetry.
        # Fold to the small-beta branch (< pi/2) so successive n's are comparable.
        def fold(g, b):
            if b > math.pi / 2:
                return (2 * math.pi - g) % (2 * math.pi), math.pi - b
            return g, b

        g_a, b_a = fold(a["gamma_opt"], a["beta_opt"])
        g_b, b_b = fold(b_["gamma_opt"], b_["beta_opt"])
        d2 = (g_b - g_a) ** 2 + (b_b - b_a) ** 2
        conc_rows.append(
            {"n": a["n"], "n_plus_1": b_["n"], "delta_sq": d2, "n_pow_minus_4": 1.0 / (a["n"] ** 4)}
        )
        print(
            f"  n={a['n']:2d}->{b_['n']:2d}  |Delta|^2 = {d2:.3e}   "
            f"1/n^4 = {1.0 / (a['n'] ** 4):.3e}   ratio = {d2 / (1.0 / (a['n'] ** 4)):.3f}"
        )

    # ---- p=2 sweep ----
    print("\n[p=2] Sweeping n = 4..15 with analytical F2 (eq. 13)...")
    p2_rows = []
    for n in range(4, 16):
        g1_, b1_, g2_, b2_, F = optimize_p2(n)
        p2_rows.append(
            {
                "n": n,
                "gamma1": g1_,
                "beta1": b1_,
                "gamma2": g2_,
                "beta2": b2_,
                "overlap": F,
                # Paper Table I fit (row 2 for p=2, but Table I is for p=5;
                # for p=2 the leading behavior from eq. 15-18 is beta2 ~ pi/n, gamma2 ~ pi - 2pi/n)
                "beta2_leading": math.pi / n,
                "gamma2_leading": math.pi - 2 * math.pi / n,
                "beta1_leading": math.pi / n,
                "gamma1_leading": math.pi,
            }
        )
        print(
            f"  n={n:2d}  g1={g1_:.4f}  b1={b1_:.4f}  g2={g2_:.4f}  b2={b2_:.4f}  F*={F:.6f}"
        )

    # ---- Qiskit cross-check at small n ----
    print("\n[Qiskit cross-check] Building real QAOA circuits for n=4,6,8...")
    cross_rows = []
    for n in [4, 6, 8]:
        row = [r for r in p1_rows if r["n"] == n][0]
        F_analytic = row["overlap"]
        F_qiskit = qiskit_overlap_p1(row["gamma_opt"], row["beta_opt"], n)
        diff = abs(F_analytic - F_qiskit)
        cross_rows.append(
            {
                "n": n,
                "gamma_opt": row["gamma_opt"],
                "beta_opt": row["beta_opt"],
                "F_analytic_eq5": F_analytic,
                "F_qiskit_statevector": F_qiskit,
                "abs_diff": diff,
                "match": diff < 1e-9,
            }
        )
        print(
            f"  n={n}  F_analytic={F_analytic:.10f}  F_qiskit={F_qiskit:.10f}  diff={diff:.2e}"
        )

    # ---- Save all evidence ----
    with open(os.path.join(EVID, "p1_sweep.json"), "w") as f:
        json.dump(p1_rows, f, indent=2)
    with open(os.path.join(EVID, "p1_concentration.json"), "w") as f:
        json.dump(conc_rows, f, indent=2)
    with open(os.path.join(EVID, "p2_sweep.json"), "w") as f:
        json.dump(p2_rows, f, indent=2)
    with open(os.path.join(EVID, "qiskit_crosscheck.json"), "w") as f:
        json.dump(cross_rows, f, indent=2)

    # CSVs
    def write_csv(path, rows):
        if not rows:
            return
        keys = list(rows[0].keys())
        with open(path, "w") as f:
            f.write(",".join(keys) + "\n")
            for r in rows:
                f.write(",".join(str(r[k]) for k in keys) + "\n")

    write_csv(os.path.join(EVID, "p1_sweep.csv"), p1_rows)
    write_csv(os.path.join(EVID, "p1_concentration.csv"), conc_rows)
    write_csv(os.path.join(EVID, "p2_sweep.csv"), p2_rows)
    write_csv(os.path.join(EVID, "qiskit_crosscheck.csv"), cross_rows)

    print("\nSaved evidence to:", EVID)
    print("Done.")


if __name__ == "__main__":
    main()
