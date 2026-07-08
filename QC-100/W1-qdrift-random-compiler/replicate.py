#!/usr/bin/env python3
"""
Replication of Campbell 2019 ("A random compiler for fast Hamiltonian simulation").

Central quantitative claim under test:
    qDRIFT diamond-norm error vs target unitary U = exp(iHt) is bounded by
        eps  <=  2 lambda^2 t^2 / N
    where lambda = sum_j |h_j| is the L1 norm of Hamiltonian coefficients,
    N is the total gate count, and the bound is INDEPENDENT of L (number of terms).

    Standard first-order (deterministic) Trotter error scales like
        eps  ~  L^2 Lambda^2 t^2 / (2 r)     with N_gates = L * r,
    so its gate count scales as L^3 (Lambda t)^2 / eps.

Methods:
    - Build random Pauli-string Hamiltonians on n=4 qubits.
    - Use scipy.linalg.expm for the exact unitary U = exp(itH) (ground truth)
      and for per-term unitaries exp(i tau H_j) used by both compilers.
    - Trotter (1st order, deterministic, repeated-r): cycle through terms in order.
    - qDRIFT: sample term j with prob p_j = h_j / lambda, apply exp(i tau H_j),
      tau = lambda*t/N. Channel error estimated by averaging over many samples
      of the random unitary V (single qDRIFT trajectory) for many input states
      and comparing E[V rho V*] (computed via Monte Carlo) to U rho U*.

Error measure used here:
    epsilon(N) := (1/2) || E^N(rho) - U rho U^dagger ||_1
        averaged over a small Haar-random set of pure input states |psi>.
    This is a per-state trace-norm distance, which is upper-bounded by the
    diamond distance d_diamond(E^N, U). It is the natural classically-tractable
    proxy: the diamond norm bound in the paper IMPLIES our measured trace-norm
    distance.  We expect our measured epsilon <= 2 lambda^2 t^2 / N (Campbell Eq. 11)
    once the Monte Carlo estimate of E^N(rho) is well-converged.

Output:
    results.json + results.csv + figures (PNG): error vs N for Trotter and qDRIFT
    across multiple L (with lambda held roughly fixed by scaling h_j).
"""
from __future__ import annotations

import csv
import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.linalg import expm

# --------------------------------------------------------------------------- #
#  Pauli operators and random Hamiltonian construction
# --------------------------------------------------------------------------- #

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = {"I": I2, "X": X, "Y": Y, "Z": Z}


def pauli_string(label: str) -> np.ndarray:
    """Return the tensor product of single-qubit Paulis given by label like 'XIZY'."""
    op = np.array([[1.0 + 0.0j]])
    for ch in label:
        op = np.kron(op, PAULIS[ch])
    return op


def random_pauli_labels(n_qubits: int, L: int, rng: np.random.Generator) -> list[str]:
    """L random non-identity Pauli-string labels on n qubits (dedup, with replacement OK)."""
    alphabet = "IXYZ"
    seen = set()
    out: list[str] = []
    while len(out) < L:
        label = "".join(rng.choice(list(alphabet), size=n_qubits))
        if label == "I" * n_qubits:
            continue
        # Allow duplicates rarely; mostly keep unique to control L meaningfully.
        if label in seen and len(seen) < 4 ** n_qubits - 1:
            continue
        seen.add(label)
        out.append(label)
    return out


@dataclass
class Hamiltonian:
    n_qubits: int
    labels: list[str]
    coeffs: np.ndarray          # h_j, all positive (we absorb signs into H_j as Hermitian Paulis already)
    terms: list[np.ndarray]     # H_j (Hermitian, unit operator norm = 1 for non-identity Paulis)

    @property
    def L(self) -> int:
        return len(self.labels)

    @property
    def lambda_(self) -> float:
        return float(np.sum(self.coeffs))

    @property
    def Lambda(self) -> float:
        return float(np.max(self.coeffs))

    def matrix(self) -> np.ndarray:
        H = np.zeros_like(self.terms[0])
        for h, T in zip(self.coeffs, self.terms):
            H = H + h * T
        return H


def build_hamiltonian(n_qubits: int, L: int, lambda_target: float,
                      rng: np.random.Generator,
                      coeff_dist: str = "uniform") -> Hamiltonian:
    """
    Build a Hamiltonian with L random Pauli terms, rescaling coefficients so that
    sum_j h_j == lambda_target.  Coefficients are drawn positive (we keep H_j as
    Hermitian Pauli strings of norm 1 -> non-identity Pauli has eigenvalues +/-1
    so operator norm == 1, matching Campbell's normalisation).
    """
    labels = random_pauli_labels(n_qubits, L, rng)
    terms = [pauli_string(lbl) for lbl in labels]
    if coeff_dist == "uniform":
        raw = rng.uniform(0.5, 1.5, size=L)
    elif coeff_dist == "lognormal":
        raw = rng.lognormal(mean=0.0, sigma=0.5, size=L)
    else:
        raise ValueError(coeff_dist)
    scale = lambda_target / raw.sum()
    coeffs = raw * scale
    return Hamiltonian(n_qubits=n_qubits, labels=labels, coeffs=coeffs, terms=terms)


# --------------------------------------------------------------------------- #
#  Simulators
# --------------------------------------------------------------------------- #

def exact_unitary(H: Hamiltonian, t: float) -> np.ndarray:
    """Ground-truth U = exp(i t H_total)."""
    return expm(1j * t * H.matrix())


def trotter_unitary(H: Hamiltonian, t: float, r: int,
                    term_cache: list[np.ndarray] | None = None) -> tuple[np.ndarray, int]:
    """
    First-order deterministic Trotter:
        V_r = prod_j exp(i (t/r) h_j H_j),  then V_total = V_r^r.
    Returns (unitary, gate_count) with gate_count = L * r.
    """
    if term_cache is None:
        # exp(i (t/r) h_j H_j)
        step_unis = [expm(1j * (t / r) * H.coeffs[j] * H.terms[j]) for j in range(H.L)]
    else:
        step_unis = term_cache
    Vr = step_unis[0].copy()
    for U in step_unis[1:]:
        Vr = U @ Vr
    V = np.linalg.matrix_power(Vr, r)
    return V, H.L * r


def qdrift_unitary(H: Hamiltonian, t: float, N: int,
                   rng: np.random.Generator,
                   term_exp_cache: list[np.ndarray] | None = None) -> np.ndarray:
    """
    Single qDRIFT trajectory: V = prod_{k=1..N} exp(i tau H_{j_k}), tau = lambda*t/N,
    with j_k iid sampled with prob p_j = h_j / lambda.
    """
    lam = H.lambda_
    tau = lam * t / N
    probs = H.coeffs / lam
    if term_exp_cache is None:
        # exp(i tau H_j)  -- depends only on tau, not on h_j (Campbell's trick).
        term_exp_cache = [expm(1j * tau * H.terms[j]) for j in range(H.L)]
    picks = rng.choice(H.L, size=N, p=probs)
    dim = term_exp_cache[0].shape[0]
    V = np.eye(dim, dtype=complex)
    for j in picks:
        V = term_exp_cache[j] @ V
    return V


# --------------------------------------------------------------------------- #
#  Error metric (trace norm distance, averaged over Haar-random states)
# --------------------------------------------------------------------------- #

def haar_states(dim: int, n_states: int, rng: np.random.Generator) -> np.ndarray:
    """Return shape (n_states, dim) array of Haar-random pure states."""
    raw = rng.standard_normal((n_states, dim)) + 1j * rng.standard_normal((n_states, dim))
    norms = np.linalg.norm(raw, axis=1, keepdims=True)
    return raw / norms


def trace_norm(rho: np.ndarray) -> float:
    """||rho||_1 = sum of singular values."""
    # rho is Hermitian -> use eigvalsh
    if np.allclose(rho, rho.conj().T, atol=1e-10):
        evals = np.linalg.eigvalsh(rho)
        return float(np.sum(np.abs(evals)))
    return float(np.sum(np.linalg.svd(rho, compute_uv=False)))


def state_error_deterministic(V: np.ndarray, U: np.ndarray,
                              psis: np.ndarray) -> float:
    """
    For a deterministic compiler producing unitary V, compute the average
    trace-norm distance (1/2)||V|psi><psi|V* - U|psi><psi|U*||_1 over the supplied states.
    For pure-state-vs-pure-state this equals sqrt(1 - |<U psi|V psi>|^2).
    """
    out = 0.0
    for psi in psis:
        a = U @ psi
        b = V @ psi
        ov = abs(np.vdot(a, b)) ** 2
        ov = min(1.0, max(0.0, ov))
        out += np.sqrt(1.0 - ov)
    return out / len(psis)


def state_error_mixed(rho_target: np.ndarray, rho_actual: np.ndarray) -> float:
    """(1/2)||rho_actual - rho_target||_1."""
    return 0.5 * trace_norm(rho_actual - rho_target)


def qdrift_channel_error(H: Hamiltonian, t: float, N: int,
                         n_samples: int, n_states: int,
                         rng: np.random.Generator,
                         term_exp_cache: list[np.ndarray] | None = None) -> tuple[float, float]:
    """
    Estimate (1/2)||E^N(rho) - U rho U*||_1 averaged over n_states Haar-random pure inputs.
    E^N is the qDRIFT channel approximated by Monte Carlo over n_samples trajectories.
    Returns (mean_error, std_error_estimate_over_states).
    """
    dim = H.terms[0].shape[0]
    U = exact_unitary(H, t)
    if term_exp_cache is None:
        lam = H.lambda_
        tau = lam * t / N
        term_exp_cache = [expm(1j * tau * H.terms[j]) for j in range(H.L)]
    psis = haar_states(dim, n_states, rng)
    rho_targets = [np.outer(U @ psi, (U @ psi).conj()) for psi in psis]

    rho_actuals = [np.zeros((dim, dim), dtype=complex) for _ in psis]
    for _ in range(n_samples):
        V = qdrift_unitary(H, t, N, rng, term_exp_cache=term_exp_cache)
        for i, psi in enumerate(psis):
            phi = V @ psi
            rho_actuals[i] += np.outer(phi, phi.conj())
    for i in range(n_states):
        rho_actuals[i] /= n_samples

    errs = np.array([state_error_mixed(rt, ra) for rt, ra in zip(rho_targets, rho_actuals)])
    return float(errs.mean()), float(errs.std(ddof=1) if len(errs) > 1 else 0.0)


# --------------------------------------------------------------------------- #
#  Experiments
# --------------------------------------------------------------------------- #

def trotter_sweep(H: Hamiltonian, t: float, r_values: Sequence[int],
                  psis: np.ndarray) -> list[dict]:
    U = exact_unitary(H, t)
    out = []
    for r in r_values:
        V, gates = trotter_unitary(H, t, r)
        err = state_error_deterministic(V, U, psis)
        out.append({
            "method": "trotter1_det",
            "r": int(r),
            "gates": int(gates),
            "error": float(err),
            "bound_qdrift": float(2 * H.lambda_**2 * t**2 / max(gates, 1)),
        })
    return out


def qdrift_sweep(H: Hamiltonian, t: float, N_values: Sequence[int],
                 n_samples: int, n_states: int,
                 rng: np.random.Generator) -> list[dict]:
    out = []
    for N in N_values:
        # Cache exponentials of H_j at this tau (the same for every gate slot in qDRIFT).
        lam = H.lambda_
        tau = lam * t / N
        term_exp_cache = [expm(1j * tau * H.terms[j]) for j in range(H.L)]
        mean_err, std_err = qdrift_channel_error(H, t, N, n_samples, n_states, rng,
                                                 term_exp_cache=term_exp_cache)
        bound = 2 * H.lambda_**2 * t**2 / N
        out.append({
            "method": "qdrift",
            "N": int(N),
            "gates": int(N),
            "error": float(mean_err),
            "error_std": float(std_err),
            "bound_qdrift": float(bound),
        })
    return out


def main():
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(exist_ok=True)
    rng = np.random.default_rng(20260626)

    n_qubits = 4
    dim = 2 ** n_qubits

    # We test the L-independence claim at FIXED lambda by building Hamiltonians
    # with different L but the same lambda (so smaller h_j when L is larger).
    lambda_target = 4.0
    t = 0.5
    L_values = [8, 24, 60]

    # Gate counts to sweep.  Trotter needs N = L * r so we pick r and derive N.
    trotter_r_values = [1, 2, 3, 5, 8, 12, 20, 32]
    qdrift_N_values = [16, 32, 64, 128, 256, 512, 1024, 2048]

    # Monte Carlo settings (kept modest to keep runtime reasonable but enough
    # for the order-of-magnitude trends we're testing).
    n_samples = 600
    n_states = 4

    results = {
        "config": {
            "n_qubits": n_qubits, "dim": dim,
            "lambda_target": lambda_target, "t": t,
            "L_values": L_values,
            "trotter_r_values": trotter_r_values,
            "qdrift_N_values": qdrift_N_values,
            "n_samples": n_samples, "n_states": n_states,
            "numpy": np.__version__,
            "seed": 20260626,
        },
        "runs": [],
    }

    psis = haar_states(dim, n_states, np.random.default_rng(1234))  # fixed test states across all runs

    t0 = time.time()
    for L in L_values:
        print(f"\n=== L = {L} ===")
        H = build_hamiltonian(n_qubits=n_qubits, L=L, lambda_target=lambda_target, rng=rng)
        print(f"  L={H.L}  lambda={H.lambda_:.4f}  Lambda(max h_j)={H.Lambda:.4f}  "
              f"||H||_op={np.linalg.norm(H.matrix(), 2):.4f}")

        trot = trotter_sweep(H, t, trotter_r_values, psis)
        print(f"  Trotter (det): {len(trot)} points; smallest error = "
              f"{min(x['error'] for x in trot):.3e} at N={[x['gates'] for x in trot][-1]}")

        qdrft = qdrift_sweep(H, t, qdrift_N_values, n_samples, n_states, rng)
        print(f"  qDRIFT       : {len(qdrft)} points; smallest error = "
              f"{min(x['error'] for x in qdrft):.3e} at N={[x['gates'] for x in qdrft][-1]}")

        run = {
            "L": L,
            "lambda": H.lambda_,
            "Lambda": H.Lambda,
            "trotter": trot,
            "qdrift": qdrft,
            "labels_sample": H.labels[:5],
        }
        results["runs"].append(run)
    dt = time.time() - t0
    results["wall_seconds"] = dt
    print(f"\nTotal wall time: {dt:.1f}s")

    with open(out_dir / "results.json", "w") as fh:
        json.dump(results, fh, indent=2)

    # Flatten to CSV
    csv_rows = []
    for run in results["runs"]:
        for row in run["trotter"] + run["qdrift"]:
            r = {"L": run["L"], "lambda": run["lambda"], "Lambda": run["Lambda"]}
            r.update(row)
            csv_rows.append(r)
    keys = sorted({k for r in csv_rows for k in r.keys()})
    with open(out_dir / "results.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in csv_rows:
            w.writerow(row)

    # Plot (matplotlib optional)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7, 5))
        colors = {8: "#1f77b4", 24: "#ff7f0e", 60: "#2ca02c"}
        for run in results["runs"]:
            L = run["L"]
            c = colors.get(L, None)
            xs = [x["gates"] for x in run["trotter"]]
            ys = [x["error"] for x in run["trotter"]]
            ax.loglog(xs, ys, "o--", color=c, label=f"Trotter L={L}")
            xs = [x["gates"] for x in run["qdrift"]]
            ys = [x["error"] for x in run["qdrift"]]
            ax.loglog(xs, ys, "s-", color=c, alpha=0.85, label=f"qDRIFT L={L}")
        # Theory line 2 lambda^2 t^2 / N at lambda_target
        xs = np.array(qdrift_N_values, dtype=float)
        ax.loglog(xs, 2 * lambda_target ** 2 * t ** 2 / xs, "k:",
                  label=r"qDRIFT bound  $2\lambda^2 t^2 / N$")
        ax.set_xlabel("gate count  N")
        ax.set_ylabel(r"avg trace-norm error  $\frac{1}{2}\,\|\rho_{\rm out} - U\rho U^{\dagger}\|_1$")
        ax.set_title(f"qDRIFT vs first-order Trotter, n={n_qubits} qubits, "
                     f"λ={lambda_target}, t={t}")
        ax.legend(fontsize=8, ncol=2)
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / "error_vs_gates.png", dpi=130)
        plt.close(fig)
    except Exception as exc:  # noqa
        print(f"  (matplotlib plot skipped: {exc})")


if __name__ == "__main__":
    main()
