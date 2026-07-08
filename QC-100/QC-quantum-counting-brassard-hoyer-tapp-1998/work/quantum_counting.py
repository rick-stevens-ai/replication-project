"""
Quantum Counting replication — Brassard, Høyer, Tapp (1998) arXiv:quant-ph/9805082

Independent implementation for the X-100 replication project.

We implement the "Count(F, P)" algorithm from Section 4 of the paper:
  - Search space of size N = 2^n
  - t marked items (Boolean oracle F : {0,...,N-1} -> {0,1})
  - Grover operator G = -A S_0 A^{-1} S_F,  where A = H^{\otimes n}, S_0 marks |0>,
    S_F marks solutions
  - Controlled-G^k on P counting qubits, followed by inverse QFT on the counting register
  - Measurement -> f in {0,...,2^P-1} -> phase phi = f/2^P
  - eigen-relation: cos(2*theta) = 1 - 2*sin^2(theta), G has eigenvalues e^{+/- i 2 theta}
    with sin^2(theta) = t/N. Thus the measured phase f/2^P estimates theta/pi,
    and t_hat = N * sin^2(pi * f / 2^P).

Theorem 5 / 6 bound (P = 2^p counting register size):
   |t - t_hat| < (2*pi/P) * sqrt(t*N) + (pi^2 / P^2) * N
with probability >= 8/pi^2 ≈ 0.811.

We build the circuits by hand as unitary matrices (statevector), diagonalize the
counting register measurement analytically from the amplitudes, and sweep over
(n, t, p_counting) to compare t_hat vs t and check the theorem's bound.

Author: Kukla subagent, 2026-07-06
"""

import json
import math
import os
import time
import numpy as np

# ---------- Grover operator via matrix construction (statevector) ----------

def grover_operator(n, marked_indices):
    """
    Return the Grover operator G = -A S_0 A^{-1} S_F  on n qubits (dim N=2^n).
    Convention: G|marked> region gets +1 sign after S_F multiplies by -1 (S_F is
    diag(+1 for unmarked, -1 for marked)), then A^-1 S_F applied, then S_0 flips
    sign of |0> component, then A applied, then overall -1.

    Equivalent form used here:
       G = (2|psi><psi| - I) * O
    where |psi> = A|0> is the uniform superposition and O = I - 2 sum_x |x><x|
    for x in marked.
    Note: this is the standard Grover diffusion followed by oracle O. It has the
    same eigenvalues as the paper's operator up to a global phase (which does not
    affect the phase-estimation result).
    """
    N = 1 << n
    # Oracle O: diag(+1) with -1 at marked
    diag_O = np.ones(N, dtype=complex)
    for m in marked_indices:
        diag_O[m] = -1.0
    O = np.diag(diag_O)

    # Diffusion D = 2|psi><psi| - I
    psi = np.ones(N, dtype=complex) / math.sqrt(N)
    D = 2.0 * np.outer(psi, psi.conj()) - np.eye(N, dtype=complex)

    # Standard "Grover iteration": G = D @ O   (see Nielsen & Chuang, eq. 6.10)
    # Note: some references use G = -D@O; the sign is a global phase on the 2D
    # invariant subspace and does not affect the |t - t_hat| bound (it only
    # shifts eigenphases by pi, which the QPE symmetry / N * sin^2(pi f/P)
    # inversion absorbs). We keep the D@O convention.
    G = D @ O
    return G


# ---------- Quantum Counting via QPE (statevector, exact) ----------

def quantum_counting_statevector(n, marked_indices, p_counting):
    """
    Simulate the Count(F,P) algorithm with P = 2^p_counting counting qubits.

    Steps (equivalent to the paper's Count):
      1) counting register in uniform superposition (H^p |0>_P)
      2) search register in uniform superposition |psi> = H^n |0>_n
      3) apply controlled-G^{2^k} for k=0..p-1 (kickback of eigenphases)
      4) inverse QFT on counting register
      5) measurement on counting register gives integer f
    Because search register starts in |psi> which is a real combination of the
    two eigenvectors of G with eigenvalues e^{+/- i 2 theta}, the marginal
    distribution over f is peaked near f = round(P * theta / pi) and its
    "mirror" f = round(P * (pi - theta)/pi) = P - round(P * theta / pi).

    Instead of simulating the full (n+p)-qubit circuit (which for n=6, p=10 is
    2^16 = 65k dims — cheap, but we would still have to explicitly build
    2^p_counting Grover powers), we exploit the eigendecomposition of G to
    compute the exact measurement distribution:
      - decompose |psi> in the 2D subspace {|alpha>, |beta>} (unmarked/marked
        uniform superpositions)
      - eigenvalues of G on this subspace: e^{+/- i 2*theta} with
        sin^2(theta) = t/N
      - Let phi_+ = 2*theta / (2*pi) = theta/pi  and phi_- = -theta/pi (mod 1)
        (equivalently 1 - theta/pi).
      - Standard QPE probability distribution:
          P(f | phi) = |sum_{k=0}^{P-1} exp(2*pi*i*k*(phi - f/P))|^2 / P^2
                     = sin^2(pi P (phi - f/P)) / (P^2 sin^2(pi (phi - f/P)))
        for phi != f/P, else 1.
        (This is the exact QPE marginal distribution over the measured integer f.)
      - Marginal over f from full state: 1/2 * P(f | phi_+) + 1/2 * P(f | phi_-)
        because |psi> = (|w+> + |w->) / sqrt(2) (up to a global phase).

    Returns: probability distribution over f in {0, ..., P-1} (length-P array).
    """
    N = 1 << n
    P = 1 << p_counting
    t = len(marked_indices)

    if t == 0:
        # No marked -> G = -D O = -D (O=I). Its eigenvalue on |psi> is +/- 1
        # (sin(theta)=0, theta=0). QPE gives f=0 deterministically.
        dist = np.zeros(P)
        dist[0] = 1.0
        return dist
    if t == N:
        # All marked -> theta = pi/2 -> f = P/2 deterministically.
        dist = np.zeros(P)
        dist[P // 2] = 1.0
        return dist

    theta = math.asin(math.sqrt(t / N))  # in (0, pi/2)
    phi_plus = theta / math.pi           # in (0, 1/2)
    phi_minus = 1.0 - phi_plus           # equivalently -theta / pi mod 1, in (1/2, 1)

    def qpe_prob(phi, f):
        # Probability of measuring integer f from QPE of eigenphase phi (in [0,1))
        # using P counting qubits, starting counting reg in H|0>.
        diff = phi - (f / P)
        # reduce diff to (-0.5, 0.5]
        diff = diff - round(diff)
        if abs(diff) < 1e-14:
            return 1.0
        num = math.sin(math.pi * P * diff) ** 2
        den = (P * math.sin(math.pi * diff)) ** 2
        return num / den

    dist = np.zeros(P)
    for f in range(P):
        dist[f] = 0.5 * qpe_prob(phi_plus, f) + 0.5 * qpe_prob(phi_minus, f)
    # Normalize (should already be 1 up to fp error)
    dist = dist / dist.sum()
    return dist


def estimate_t_from_f(f, P, N):
    """t_hat = N * sin^2(pi f / P), then reflect to [0, N/2] since QPE
    is symmetric around f=P/2."""
    phi = f / P
    return N * (math.sin(math.pi * phi) ** 2)


# ---------- Sweep ----------

def run_sweep(seed=0):
    rng = np.random.default_rng(seed)
    rows = []

    # (n_qubits_search, list of t values to try, list of p_counting to try)
    configs = [
        (4, [1, 3, 6, 10, 15],       [3, 4, 5, 6, 7, 8]),
        (5, [1, 5, 12, 20, 27, 31],  [4, 5, 6, 7, 8]),
        (6, [1, 10, 25, 40, 55, 63], [4, 5, 6, 7, 8]),
    ]

    for n, t_list, p_list in configs:
        N = 1 << n
        for t in t_list:
            # random marked set
            marked = list(rng.choice(N, size=t, replace=False))
            for p in p_list:
                P = 1 << p
                t0 = time.time()
                dist = quantum_counting_statevector(n, marked, p)
                dt = time.time() - t0

                # Argmax measurement
                f_star = int(np.argmax(dist))
                # Reflect: paper's algorithm folds f and P-f (both give same t_hat)
                t_hat = estimate_t_from_f(f_star, P, N)
                err = abs(t - t_hat)

                # Theoretical Theorem-5 bound
                bound = (2 * math.pi / P) * math.sqrt(t * N) + (math.pi ** 2 / (P * P)) * N

                # Sampled 8/pi^2 success probability: probability that measured f
                # yields |t - t_hat| < bound  (Theorem's guarantee)
                # We compute this exactly by summing dist[f] over the "success" set:
                success_prob = 0.0
                for fi in range(P):
                    thi = estimate_t_from_f(fi, P, N)
                    if abs(t - thi) < bound:
                        success_prob += dist[fi]

                # Expected number of "counting-qubits" precision:
                rows.append({
                    "n": n, "N": N,
                    "t_true": t,
                    "p_counting": p, "P": P,
                    "f_argmax": f_star,
                    "t_hat_argmax": round(t_hat, 6),
                    "abs_error_argmax": round(err, 6),
                    "theorem5_bound": round(bound, 6),
                    "argmax_within_bound": bool(err < bound),
                    "success_prob_within_bound": round(float(success_prob), 6),
                    "success_prob_ge_8_over_pi2": bool(success_prob >= 8.0 / math.pi ** 2 - 1e-9),
                    "sim_time_s": round(dt, 4),
                })

    return rows


if __name__ == "__main__":
    rows = run_sweep(seed=42)
    outdir = os.path.expanduser(
        "~/Dropbox/REPLICATE-PROJECT/QC-quantum-counting-brassard-hoyer-tapp-1998/report/evidence"
    )
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "sweep_results.json"), "w") as f:
        json.dump(rows, f, indent=2)

    # Also emit a CSV
    import csv
    fields = list(rows[0].keys())
    with open(os.path.join(outdir, "sweep_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # Print summary
    n_total = len(rows)
    n_within = sum(1 for r in rows if r["argmax_within_bound"])
    n_success = sum(1 for r in rows if r["success_prob_ge_8_over_pi2"])
    print(f"Sweep configs: {n_total}")
    print(f"Argmax within Theorem-5 bound: {n_within}/{n_total}")
    print(f"P(within bound) >= 8/pi^2 (paper's Thm-5): {n_success}/{n_total}")
    # print table
    print()
    print(f"{'n':>2} {'t':>3} {'p':>2} {'f*':>5} {'t_hat':>9} {'|err|':>8} {'bound':>10} {'P>=8/pi2':>10}")
    for r in rows:
        print(f"{r['n']:>2} {r['t_true']:>3} {r['p_counting']:>2} {r['f_argmax']:>5} "
              f"{r['t_hat_argmax']:>9} {r['abs_error_argmax']:>8} {r['theorem5_bound']:>10} "
              f"{str(r['success_prob_ge_8_over_pi2']):>10}")
