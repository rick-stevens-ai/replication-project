#!/usr/bin/env python3
"""
Zero-Noise Extrapolation (ZNE) replication of Temme, Bravyi, Gambetta (2016/2017).
arXiv:1612.02058, "Error mitigation for short-depth quantum circuits."

Implements Richardson-extrapolation Eq. (3-4):
    E_hat^n(lambda) = sum_j gamma_j * E_hat(c_j lambda),   sum gamma_j = 1,
                                                            sum gamma_j c_j^k = 0 for k=1..n.

We instantiate a short-depth "control-problem" style circuit similar in spirit to Fig. 1(a) of
the paper:  a small N-qubit random circuit of alternating single-qubit rotations + entangling
CX layers, with per-gate depolarizing noise at rate epsilon (base) and 2*eps, 3*eps as the
noise-scaled runs.  Because we control the simulator noise directly we can scale it exactly
without needing a physical time-rescaling protocol.

Observable:  <Z_0 Z_1> after the circuit.  We compute:
   - the *ideal* (noiseless) expectation E_ideal,
   - the noisy expectations E(eps), E(2 eps), E(3 eps) via qiskit-aer,
   - two ZNE estimators:
        * linear (n=1) using {c0=1, c1=2}
        * quadratic-Richardson (n=2) using {c0=1, c1=2, c2=3}

For the linear estimator with c=(1,2), Eq. (4) gives (gamma0, gamma1) = (2, -1).
For the Richardson n=2 with c=(1,2,3), Eq. (4) gives (gamma0, gamma1, gamma2) = (3, -3, 1).

Success criterion (paper's headline qualitative claim):
   |E_ZNE_n - E_ideal| <  |E(eps) - E_ideal|          (mitigation beats raw noisy)
   |E_ZNE_2 - E_ideal| <= |E_ZNE_1 - E_ideal|          (higher-order n reduces error more)
"""

from __future__ import annotations
import json, os, sys, time
import numpy as np
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ------------------------------------------------------------
# Richardson coefficients from Eq. (4) of Temme/Bravyi/Gambetta
# ------------------------------------------------------------
def richardson_coeffs(cs: list[float]) -> np.ndarray:
    """Solve the Vandermonde-like system: sum gamma_j c_j^k = delta_{k,0},
       for k = 0..n where n = len(cs)-1."""
    n_plus_1 = len(cs)
    n = n_plus_1 - 1
    A = np.zeros((n_plus_1, n_plus_1))
    b = np.zeros(n_plus_1)
    for k in range(n_plus_1):
        for j in range(n_plus_1):
            A[k, j] = cs[j] ** k
    b[0] = 1.0
    gammas = np.linalg.solve(A, b)
    return gammas


# ------------------------------------------------------------
# Build a short-depth "random-control" circuit (paper Fig. 1 style)
# ------------------------------------------------------------
def build_circuit(n_qubits: int = 4, depth: int = 6, seed: int = 0) -> QuantumCircuit:
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n_qubits)
    for d in range(depth):
        # random single-qubit U3-like layer
        for q in range(n_qubits):
            th = rng.uniform(0, np.pi)
            ph = rng.uniform(0, 2 * np.pi)
            la = rng.uniform(0, 2 * np.pi)
            qc.u(th, ph, la, q)
        # brick-wall CX layer
        offset = d % 2
        for q in range(offset, n_qubits - 1, 2):
            qc.cx(q, q + 1)
    return qc


def make_noise_model(eps: float, n_qubits: int) -> NoiseModel:
    """Depolarizing noise on every 1q gate (rate eps) and every 2q gate (rate eps).
       For eps=0 the returned model is a no-op (identity) — we handle that at call site."""
    nm = NoiseModel()
    if eps <= 0:
        return nm
    err1 = depolarizing_error(eps, 1)
    err2 = depolarizing_error(eps, 2)
    nm.add_all_qubit_quantum_error(err1, ["u", "u1", "u2", "u3", "rx", "ry", "rz", "h", "s", "sdg", "t", "tdg", "id", "x", "y", "z"])
    nm.add_all_qubit_quantum_error(err2, ["cx", "cz"])
    return nm


# ------------------------------------------------------------
# Expectation value <Z_0 Z_1> from density-matrix simulation (exact, no shot noise)
# ------------------------------------------------------------
def z0z1_expectation(qc: QuantumCircuit, eps: float) -> float:
    n = qc.num_qubits
    if eps <= 0:
        sim = AerSimulator(method="density_matrix")
        tqc = transpile(qc, sim, basis_gates=["u", "cx"])
    else:
        nm = make_noise_model(eps, n)
        sim = AerSimulator(method="density_matrix", noise_model=nm)
        tqc = transpile(qc, sim, basis_gates=["u", "cx"])
    # append save_density_matrix AFTER transpile so BasisTranslator doesn't touch it
    tqc.save_density_matrix()
    result = sim.run(tqc).result()
    rho = np.asarray(result.data(0)["density_matrix"])
    # build Z_0 Z_1 (x) I on n qubits.  Qiskit qubit-order: qubit 0 = least significant.
    I2 = np.eye(2, dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    op = 1
    for q in range(n):
        m = Z if q in (0, 1) else I2
        op = np.kron(m, op) if q > 0 else m
    ev = np.real(np.trace(op @ rho))
    return float(ev)


# ------------------------------------------------------------
# Main experiment
# ------------------------------------------------------------
def run(out_dir: Path, n_qubits: int = 4, depth: int = 6, seed: int = 42,
        eps_grid: list[float] = None, n_circuits: int = 8):
    if eps_grid is None:
        eps_grid = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]

    # noise-scaling factors used for ZNE
    cs_lin = [1.0, 2.0]            # linear extrapolation
    cs_ric = [1.0, 2.0, 3.0]       # Richardson n=2

    g_lin = richardson_coeffs(cs_lin)
    g_ric = richardson_coeffs(cs_ric)
    print(f"[coeffs] linear (c=1,2) gammas = {g_lin}   (should be [2,-1])")
    print(f"[coeffs] Richardson (c=1,2,3) gammas = {g_ric}   (should be [3,-3,1])")
    # sanity check
    assert np.allclose(g_lin, [2.0, -1.0]), g_lin
    assert np.allclose(g_ric, [3.0, -3.0, 1.0]), g_ric

    all_results = []
    for ci in range(n_circuits):
        circ_seed = seed + ci
        qc = build_circuit(n_qubits=n_qubits, depth=depth, seed=circ_seed)
        E_ideal = z0z1_expectation(qc, eps=0.0)

        per_eps = []
        for eps in eps_grid:
            # noisy evals at c*eps for c in {1,2,3}
            Es = {}
            for c in [1.0, 2.0, 3.0]:
                Es[c] = z0z1_expectation(qc, eps=c * eps)
            E_raw = Es[1.0]
            E_zne1 = g_lin[0] * Es[cs_lin[0]] + g_lin[1] * Es[cs_lin[1]]
            E_zne2 = g_ric[0] * Es[cs_ric[0]] + g_ric[1] * Es[cs_ric[1]] + g_ric[2] * Es[cs_ric[2]]

            err_raw = abs(E_raw - E_ideal)
            err_zne1 = abs(E_zne1 - E_ideal)
            err_zne2 = abs(E_zne2 - E_ideal)

            per_eps.append({
                "eps": eps,
                "E_ideal": E_ideal,
                "E_c1_raw": Es[1.0],
                "E_c2": Es[2.0],
                "E_c3": Es[3.0],
                "E_zne1_linear": E_zne1,
                "E_zne2_richardson": E_zne2,
                "err_raw": err_raw,
                "err_zne1": err_zne1,
                "err_zne2": err_zne2,
                "improvement_ratio_zne1_over_raw": (err_raw / err_zne1) if err_zne1 > 0 else float("inf"),
                "improvement_ratio_zne2_over_raw": (err_raw / err_zne2) if err_zne2 > 0 else float("inf"),
            })
            print(f"  [circ {ci} seed={circ_seed} eps={eps:.1e}] "
                  f"E_ideal={E_ideal:+.6f} raw={E_raw:+.6f} zne1={E_zne1:+.6f} zne2={E_zne2:+.6f} "
                  f"| err raw={err_raw:.4e} zne1={err_zne1:.4e} zne2={err_zne2:.4e}")

        all_results.append({"circuit_index": ci, "seed": circ_seed,
                            "n_qubits": n_qubits, "depth": depth,
                            "E_ideal": E_ideal, "per_eps": per_eps})

    # aggregate stats per epsilon (mean absolute error across circuits)
    agg = []
    for i, eps in enumerate(eps_grid):
        errs_raw = np.array([r["per_eps"][i]["err_raw"]  for r in all_results])
        errs_zne1 = np.array([r["per_eps"][i]["err_zne1"] for r in all_results])
        errs_zne2 = np.array([r["per_eps"][i]["err_zne2"] for r in all_results])
        agg.append({
            "eps": eps,
            "mean_err_raw":  float(errs_raw.mean()),
            "mean_err_zne1": float(errs_zne1.mean()),
            "mean_err_zne2": float(errs_zne2.mean()),
            "median_err_raw":  float(np.median(errs_raw)),
            "median_err_zne1": float(np.median(errs_zne1)),
            "median_err_zne2": float(np.median(errs_zne2)),
            "n_zne1_better_than_raw":  int((errs_zne1  < errs_raw).sum()),
            "n_zne2_better_than_raw":  int((errs_zne2  < errs_raw).sum()),
            "n_zne2_better_than_zne1": int((errs_zne2  < errs_zne1).sum()),
            "n_circuits": int(len(errs_raw)),
        })

    out = {
        "paper": "arXiv:1612.02058 Temme/Bravyi/Gambetta",
        "richardson_coefficients": {
            "cs_linear": cs_lin, "gammas_linear": g_lin.tolist(),
            "cs_richardson": cs_ric, "gammas_richardson": g_ric.tolist(),
        },
        "config": {
            "n_qubits": n_qubits, "depth": depth, "seed": seed,
            "eps_grid": eps_grid, "n_circuits": n_circuits,
            "observable": "<Z_0 Z_1>",
            "noise_model": "depolarizing on every 1q (rate eps) and 2q (rate eps) gate",
            "simulator": "qiskit-aer density_matrix",
        },
        "per_circuit_results": all_results,
        "aggregate_by_eps": agg,
    }
    out_json = out_dir / "zne_results.json"
    out_json.write_text(json.dumps(out, indent=2))
    print(f"\n[saved] {out_json}")

    print("\n===== Aggregate (mean absolute error across circuits) =====")
    print(f"{'eps':>10s}  {'raw':>12s}  {'ZNE1':>12s}  {'ZNE2':>12s}  {'#ZNE1<raw':>9s}  {'#ZNE2<raw':>9s}  {'#ZNE2<ZNE1':>10s}")
    for a in agg:
        print(f"{a['eps']:>10.1e}  {a['mean_err_raw']:>12.4e}  {a['mean_err_zne1']:>12.4e}  "
              f"{a['mean_err_zne2']:>12.4e}  {a['n_zne1_better_than_raw']:>9d}  "
              f"{a['n_zne2_better_than_raw']:>9d}  {a['n_zne2_better_than_zne1']:>10d}")

    return out


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    res = run(out_dir, n_qubits=4, depth=6, seed=42,
              eps_grid=[1e-4, 3e-4, 1e-3, 3e-3, 1e-2],
              n_circuits=8)
    dt = time.time() - t0
    print(f"\n[done] {dt:.1f} s")
