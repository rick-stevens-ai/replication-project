#!/usr/bin/env python3
"""
Independent replication of Maciejewski et al. 2021 (arXiv:2101.02331)
"Modeling and mitigation of cross-talk effects in readout noise..."

Reproducible core:
  1. Build a small-N (N=4) readout noise model with CROSS-TALK
     (bit-flip probabilities on qubit i depend on the state of qubit i's neighbor).
  2. Compare three mitigation strategies on a real Qiskit Aer simulation:
       (a) No mitigation (raw noisy counts)
       (b) Tensor-product / uncorrelated response matrix (product of 1q A_i)
       (c) Correlated 2^N x 2^N response matrix (fully characterizes cross-talk)
  3. Compare TVD of estimated distribution vs ideal, and error on <Z0Z1+Z1Z2+Z2Z3>
     for a small QAOA-like circuit.
  4. Repeat over multiple random circuits and report average error-reduction factors.

Output: JSON + prints to stdout. Real Aer sim, no fabrication.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

RNG = np.random.default_rng(20260703)

# --------------------------------------------------------------------- #
# 1. Cross-talk readout noise model
# --------------------------------------------------------------------- #
# Per-qubit measurement error is described by a 2x2 stochastic matrix A_i:
#   A_i[m,t] = Pr(measure m | true state t) on qubit i
# For UNCORRELATED noise the full N-qubit response is A = ⊗ A_i.
#
# For CROSS-TALK (Maciejewski et al. §2), the noise on qubit i depends on
# the true state of a neighbor. We model this on N=4 as follows:
#   - qubits 0,3 have single-qubit noise (independent)
#   - qubits 1,2 form a cross-talk cluster:
#       P(flip on q1 | true state of q2 == 1) is larger than when q2==0
#       ditto P(flip on q2 | true state of q1 == 1)
# We build the full 16x16 response matrix R by summing over hidden noise
# outcomes for each true 4-bit input.

N = 4
DIM = 2**N

# Base single-qubit flip probabilities (typical NISQ device: few percent)
P0_TO_1 = np.array([0.02, 0.03, 0.03, 0.04])  # Pr(read 1 | true 0)
P1_TO_0 = np.array([0.06, 0.07, 0.07, 0.09])  # Pr(read 1 -> 0)  (asymmetric like paper)

# Cross-talk boost: if neighbor is |1>, flip prob on the affected qubit
# is increased additively by DELTA. Cluster is qubits {1,2}.
DELTA = 0.05  # 5 percentage-point boost, deliberately visible


def single_q_A(p01: float, p10: float) -> np.ndarray:
    """2x2 measurement matrix. Rows indexed by measured bit m, cols by true t."""
    return np.array(
        [[1 - p01, p10], [p01, 1 - p10]],
        dtype=float,
    )


def build_response_matrix(p01_arr: np.ndarray, p10_arr: np.ndarray,
                          delta_cluster: float = DELTA) -> np.ndarray:
    """Build full 16x16 correlated response matrix R[measured, true].

    Uncorrelated part on q0,q3. Cluster on q1,q2 has state-dependent flip probs.
    R[m,t] = Pr(measured bitstring m | true bitstring t)
    """
    R = np.zeros((DIM, DIM))
    for t in range(DIM):
        # true bits: index 0 = q0 (MSB in our convention below? use little-endian)
        # we'll say bit i of the integer = qubit i (i=0 LSB)
        t_bits = [(t >> i) & 1 for i in range(N)]
        # Effective flip probs for this true state
        p01 = p01_arr.copy()
        p10 = p10_arr.copy()
        # Cluster: q1 affected by q2's true value; q2 affected by q1's true value
        if t_bits[2] == 1:
            p01[1] += delta_cluster
            p10[1] += delta_cluster
        if t_bits[1] == 1:
            p01[2] += delta_cluster
            p10[2] += delta_cluster
        # Clamp
        p01 = np.clip(p01, 0.0, 0.5)
        p10 = np.clip(p10, 0.0, 0.5)
        # Per-qubit A_i(t_bits[i]) columns
        for m in range(DIM):
            m_bits = [(m >> i) & 1 for i in range(N)]
            prob = 1.0
            for i in range(N):
                A_i = single_q_A(p01[i], p10[i])
                prob *= A_i[m_bits[i], t_bits[i]]
            R[m, t] = prob
    # Sanity: columns sum to 1
    assert np.allclose(R.sum(axis=0), 1.0, atol=1e-9), "R columns must sum to 1"
    return R


def build_uncorrelated_response(p01_arr: np.ndarray, p10_arr: np.ndarray) -> np.ndarray:
    """Tensor-product uncorrelated response matrix (baseline model that IGNORES cross-talk).

    We treat q1,q2 with their BASE flip probs (no delta), which is what a
    tensor-product characterization sees on average. This is the strawman
    the paper improves upon.
    """
    R = np.array([[1.0]])
    for i in range(N):
        A_i = single_q_A(p01_arr[i], p10_arr[i])
        # Kronecker order: qubit 0 = innermost / LSB
        # We want bit i of index = qubit i, so kron with q0 first as LSB means
        # R = A_{N-1} ⊗ ... ⊗ A_0
        R = np.kron(A_i, R)
    return R


# --------------------------------------------------------------------- #
# 2. Apply noise to ideal counts (real: use Aer to sample noiseless dist then apply R)
# --------------------------------------------------------------------- #
def ideal_probs_from_circuit(qc: QuantumCircuit, shots: int = 200000) -> np.ndarray:
    """Run circuit on Aer noiseless, return empirical prob vector of length DIM."""
    sim = AerSimulator()
    tqc = transpile(qc, sim)
    tqc.measure_all()
    res = sim.run(tqc, shots=shots).result()
    counts = res.get_counts()
    probs = np.zeros(DIM)
    for bitstr, c in counts.items():
        # Qiskit returns MSB-first string; strip spaces
        bs = bitstr.replace(" ", "")
        idx = int(bs, 2)
        # Convert to our little-endian convention (bit i = qubit i)
        # Qiskit bitstring: leftmost char is highest-index classical bit.
        # measure_all creates cregs where classical bit i = qubit i.
        # The string 'b_{n-1} ... b_1 b_0' -> int with b_0 as LSB.
        # int(bs,2) treats leftmost as MSB — which matches (MSB = q_{n-1}).
        # So idx bit i already = qubit i. Good.
        probs[idx] = c / shots
    return probs


def sample_noisy_from_R(true_probs: np.ndarray, R: np.ndarray, shots: int) -> np.ndarray:
    """Given true prob vector and response matrix R, form the noisy prob vector p_noisy = R @ p_true,
    then draw `shots` finite samples and return empirical probs."""
    p_noisy = R @ true_probs
    p_noisy = np.clip(p_noisy, 0, None)
    p_noisy = p_noisy / p_noisy.sum()
    draws = RNG.multinomial(shots, p_noisy)
    return draws / shots


# --------------------------------------------------------------------- #
# 3. Mitigation
# --------------------------------------------------------------------- #
def mitigate(p_noisy_emp: np.ndarray, R_model: np.ndarray) -> np.ndarray:
    """Solve R_model @ p_mit = p_noisy_emp; project to simplex."""
    try:
        p_mit = np.linalg.solve(R_model, p_noisy_emp)
    except np.linalg.LinAlgError:
        p_mit = np.linalg.lstsq(R_model, p_noisy_emp, rcond=None)[0]
    return project_to_simplex(p_mit)


def project_to_simplex(v: np.ndarray) -> np.ndarray:
    """Project onto probability simplex (Wang & Carreira-Perpinan 2013)."""
    v = np.asarray(v, dtype=float)
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    rho = np.nonzero(u * np.arange(1, n + 1) > cssv)[0][-1]
    theta = cssv[rho] / (rho + 1.0)
    w = np.maximum(v - theta, 0.0)
    return w


# --------------------------------------------------------------------- #
# 4. Observable expectation on prob vector
# --------------------------------------------------------------------- #
def z_expectation(probs: np.ndarray, qubit_mask: list) -> float:
    """Compute <Z_{q1} Z_{q2} ...> from a probability vector.
    qubit_mask: list of qubit indices whose Z's are in the product."""
    exp = 0.0
    for idx, p in enumerate(probs):
        parity = 0
        for q in qubit_mask:
            parity ^= (idx >> q) & 1
        sign = 1.0 if parity == 0 else -1.0
        exp += sign * p
    return exp


def tvd(p: np.ndarray, q: np.ndarray) -> float:
    return 0.5 * np.sum(np.abs(p - q))


# --------------------------------------------------------------------- #
# 5. Small QAOA-flavored circuits
# --------------------------------------------------------------------- #
def random_qaoa_circuit(seed: int) -> QuantumCircuit:
    """Random p=2 QAOA-like circuit on 4 qubits with random parameters and a
    line-graph MaxCut Hamiltonian (edges 0-1, 1-2, 2-3)."""
    rng = np.random.default_rng(seed)
    gammas = rng.uniform(0, np.pi, 2)
    betas = rng.uniform(0, np.pi / 2, 2)
    qc = QuantumCircuit(N)
    for i in range(N):
        qc.h(i)
    edges = [(0, 1), (1, 2), (2, 3)]
    for p in range(2):
        for (a, b) in edges:
            qc.cx(a, b)
            qc.rz(2 * gammas[p], b)
            qc.cx(a, b)
        for i in range(N):
            qc.rx(2 * betas[p], i)
    return qc


# --------------------------------------------------------------------- #
# 6. Main experiment
# --------------------------------------------------------------------- #
def main():
    outdir = Path(os.environ.get(
        "OUTDIR",
        "/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2101.02331-crosstalk-readout-noise/report/evidence",
    ))
    outdir.mkdir(parents=True, exist_ok=True)

    # Build both noise models
    R_true = build_response_matrix(P0_TO_1, P1_TO_0, DELTA)   # ground truth (with cross-talk)
    R_tp   = build_uncorrelated_response(P0_TO_1, P1_TO_0)   # tensor-product (ignores cross-talk)
    R_corr = R_true                                            # correlated model = ground truth

    # Sanity: R_true != R_tp
    diff_tp = np.max(np.abs(R_true - R_tp))
    print(f"Max abs difference (R_true vs R_tp)          = {diff_tp:.4f}")

    n_circuits = 25
    shots = 100000

    edges = [(0, 1), (1, 2), (2, 3)]

    per_circuit = []
    for s in range(n_circuits):
        qc = random_qaoa_circuit(seed=s + 100)
        p_ideal = ideal_probs_from_circuit(qc, shots=shots)
        # noisy emp
        p_noisy_emp = sample_noisy_from_R(p_ideal, R_true, shots)
        # mitigations
        p_mit_tp   = mitigate(p_noisy_emp, R_tp)
        p_mit_corr = mitigate(p_noisy_emp, R_corr)

        # (a) TVD in probability space
        tvd_raw  = tvd(p_noisy_emp, p_ideal)
        tvd_tp   = tvd(p_mit_tp,   p_ideal)
        tvd_corr = tvd(p_mit_corr, p_ideal)

        # (b) Sum of ZZ observables along edges (MaxCut Hamiltonian analogue)
        e_ideal = sum(z_expectation(p_ideal,       list(e)) for e in edges)
        e_noisy = sum(z_expectation(p_noisy_emp,   list(e)) for e in edges)
        e_tp    = sum(z_expectation(p_mit_tp,      list(e)) for e in edges)
        e_corr  = sum(z_expectation(p_mit_corr,    list(e)) for e in edges)

        err_noisy = abs(e_noisy - e_ideal)
        err_tp    = abs(e_tp    - e_ideal)
        err_corr  = abs(e_corr  - e_ideal)

        per_circuit.append({
            "seed": s,
            "tvd_raw": tvd_raw, "tvd_tp": tvd_tp, "tvd_corr": tvd_corr,
            "e_ideal": e_ideal, "e_noisy": e_noisy, "e_tp": e_tp, "e_corr": e_corr,
            "err_noisy": err_noisy, "err_tp": err_tp, "err_corr": err_corr,
        })

    # Aggregate
    def mean(k): return float(np.mean([c[k] for c in per_circuit]))
    def med(k):  return float(np.median([c[k] for c in per_circuit]))

    agg = {
        "n_circuits": n_circuits,
        "shots_per_circuit": shots,
        "N_qubits": N,
        "delta_cluster": DELTA,
        "R_true_vs_R_tp_maxabs": float(diff_tp),
        "mean_tvd_raw":  mean("tvd_raw"),
        "mean_tvd_tp":   mean("tvd_tp"),
        "mean_tvd_corr": mean("tvd_corr"),
        "mean_err_energy_noisy": mean("err_noisy"),
        "mean_err_energy_tp":    mean("err_tp"),
        "mean_err_energy_corr":  mean("err_corr"),
        "median_err_energy_noisy": med("err_noisy"),
        "median_err_energy_tp":    med("err_tp"),
        "median_err_energy_corr":  med("err_corr"),
    }
    agg["factor_reduction_tvd_tp"]   = agg["mean_tvd_raw"] / max(agg["mean_tvd_tp"],   1e-12)
    agg["factor_reduction_tvd_corr"] = agg["mean_tvd_raw"] / max(agg["mean_tvd_corr"], 1e-12)
    agg["factor_reduction_energy_tp"]   = agg["mean_err_energy_noisy"] / max(agg["mean_err_energy_tp"],   1e-12)
    agg["factor_reduction_energy_corr"] = agg["mean_err_energy_noisy"] / max(agg["mean_err_energy_corr"], 1e-12)

    print("\n=== Aggregate results (mean over 25 random p=2 QAOA-like circuits, N=4) ===")
    for k, v in agg.items():
        if isinstance(v, float):
            print(f"  {k:38s} = {v:.6f}")
        else:
            print(f"  {k:38s} = {v}")

    (outdir / "results.json").write_text(json.dumps(
        {"aggregate": agg, "per_circuit": per_circuit},
        indent=2,
    ))

    # ---------------------- (c) QAOA parameter sweep -------------------- #
    # Small p=1 QAOA on line-4 MaxCut, sweep (gamma,beta) coarsely and find the
    # arg-min of energy (equivalently arg-max of MaxCut ratio). Compare noisy vs
    # mitigated grids.
    print("\n=== (c) QAOA p=1 grid: noisy vs mitigated optima ===")
    gammas = np.linspace(0, np.pi, 13)
    betas  = np.linspace(0, np.pi / 2, 13)

    def qaoa_p1_energy(g, b, R, mitigate_with=None):
        qc = QuantumCircuit(N)
        for i in range(N):
            qc.h(i)
        for (a, bb) in edges:
            qc.cx(a, bb); qc.rz(2 * g, bb); qc.cx(a, bb)
        for i in range(N):
            qc.rx(2 * b, i)
        p_ideal = ideal_probs_from_circuit(qc, shots=shots)
        p_emp = sample_noisy_from_R(p_ideal, R, shots)
        if mitigate_with is not None:
            p_final = mitigate(p_emp, mitigate_with)
        else:
            p_final = p_emp
        # MaxCut cost expectation: sum_e (1 - <Z_a Z_b>) / 2
        cost = sum((1 - z_expectation(p_final, list(e))) / 2 for e in edges)
        return cost, p_ideal

    grid_ideal   = np.zeros((len(gammas), len(betas)))
    grid_noisy   = np.zeros_like(grid_ideal)
    grid_mit_tp  = np.zeros_like(grid_ideal)
    grid_mit_corr= np.zeros_like(grid_ideal)

    for i, g in enumerate(gammas):
        for j, b in enumerate(betas):
            qc = QuantumCircuit(N)
            for k in range(N):
                qc.h(k)
            for (a, bb) in edges:
                qc.cx(a, bb); qc.rz(2 * g, bb); qc.cx(a, bb)
            for k in range(N):
                qc.rx(2 * b, k)
            p_ideal = ideal_probs_from_circuit(qc, shots=shots)
            p_emp   = sample_noisy_from_R(p_ideal, R_true, shots)
            p_tp    = mitigate(p_emp, R_tp)
            p_cr    = mitigate(p_emp, R_corr)
            grid_ideal[i, j]    = sum((1 - z_expectation(p_ideal, list(e))) / 2 for e in edges)
            grid_noisy[i, j]    = sum((1 - z_expectation(p_emp,   list(e))) / 2 for e in edges)
            grid_mit_tp[i, j]   = sum((1 - z_expectation(p_tp,    list(e))) / 2 for e in edges)
            grid_mit_corr[i, j] = sum((1 - z_expectation(p_cr,    list(e))) / 2 for e in edges)

    # Max ratio and where they occur
    def best(grid):
        idx = np.unravel_index(np.argmax(grid), grid.shape)
        return float(grid[idx]), idx

    b_ideal, i_ideal = best(grid_ideal)
    b_noisy, i_noisy = best(grid_noisy)
    b_tp,    i_tp    = best(grid_mit_tp)
    b_cr,    i_cr    = best(grid_mit_corr)

    # MaxCut on line graph (4 nodes, 3 edges): max cut = 3
    r_ideal = b_ideal / 3
    r_noisy = b_noisy / 3
    r_tp    = b_tp    / 3
    r_cr    = b_cr    / 3

    qaoa_res = {
        "best_cost_ideal":       b_ideal, "argmax_ideal":       list(map(int, i_ideal)),
        "best_cost_noisy":       b_noisy, "argmax_noisy":       list(map(int, i_noisy)),
        "best_cost_mit_tp":      b_tp,    "argmax_mit_tp":      list(map(int, i_tp)),
        "best_cost_mit_corr":    b_cr,    "argmax_mit_corr":    list(map(int, i_cr)),
        "approx_ratio_ideal":    r_ideal,
        "approx_ratio_noisy":    r_noisy,
        "approx_ratio_mit_tp":   r_tp,
        "approx_ratio_mit_corr": r_cr,
    }
    for k, v in qaoa_res.items():
        print(f"  {k:32s} = {v}")

    (outdir / "qaoa_grid_results.json").write_text(json.dumps(qaoa_res, indent=2))
    np.savez(outdir / "qaoa_grids.npz",
             gammas=gammas, betas=betas,
             grid_ideal=grid_ideal, grid_noisy=grid_noisy,
             grid_mit_tp=grid_mit_tp, grid_mit_corr=grid_mit_corr)

    print(f"\nAll evidence saved under {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
