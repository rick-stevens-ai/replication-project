"""
Clifford generator-based RB (Section 6 + Section 7.2, Tables 3/5 of arXiv:1803.03621).

Setup:
  n_qubits = 2, d = 4
  Generators A = { H_i, S_i, S_i^{-1}, CNOT_{i,j} } on 2 qubits
  Random walk on Clifford group C(2) via uniform sampling from A (closed under inverse).
  For each "gate" step in the RB sequence we apply b generators as an initialization
  (this is the paper's mixing block, so that the b-th composition approximates a Haar-random
  Clifford), then apply noise, then continue.

We do NOT use the full 11520-element Clifford enumeration.  Following the paper's Sec 6,
we approximate a Haar-random Clifford by taking b generator steps (each with noise between).
We fit the survival curve of |00><00| to  A + B * f^m,  convert f -> p_hat,
and compare to the true average fidelity of the injected noise channel.

Noise channel used here (paper's Table 5-style, low Kraus rank version):
  T(rho) = p*rho + (1-p) * U rho U^dagger
where U is a random Haar unitary drawn once per RB run.  This is delta-covariant with
delta = p, so the paper's theorem applies for p close to 1.

For n=2 (d=4), true avg fidelity of this channel is
  F(T) = p * 1 + (1-p) * F_avg(U)
where F_avg(U) = (|Tr(U)|^2 + d) / (d * (d+1))
Assumes noise is per-gate (applied after every generator).
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

RNG = np.random.default_rng(20260704)

# --- 1-qubit gates ---
I1 = np.eye(2, dtype=complex)
X1 = np.array([[0, 1], [1, 0]], dtype=complex)
H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
# paper's "pi-gate": (1, 0; 0, i) = S gate  (called "pi gate" -- eq 57)
S1 = np.array([[1, 0], [0, 1j]], dtype=complex)
Sdag1 = S1.conj().T


def kron(*ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def single_qubit_on(op1, i, n):
    """Return d^n x d^n operator with op1 acting on qubit i (0-indexed, 0 = leftmost = highest)."""
    ops = [I1] * n
    ops[i] = op1
    return kron(*ops)


def cnot_on(i, j, n):
    """CNOT with control i, target j, on n qubits, dimension 2^n."""
    d = 2 ** n
    # Build in computational basis
    U = np.zeros((d, d), dtype=complex)
    for k in range(d):
        bits = [(k >> (n - 1 - q)) & 1 for q in range(n)]  # bits[q] = qubit q
        if bits[i] == 1:
            bits[j] ^= 1
        k2 = 0
        for q in range(n):
            k2 |= bits[q] << (n - 1 - q)
        U[k2, k] = 1.0
    return U


def clifford_generators(n_qubits: int) -> list[np.ndarray]:
    """Set A from paper eq. 58: H_i, S_i, S_i^{-1}, CNOT_{i,j} for i != j.  On n qubits."""
    gens = []
    for i in range(n_qubits):
        gens.append(single_qubit_on(H1, i, n_qubits))
        gens.append(single_qubit_on(S1, i, n_qubits))
        gens.append(single_qubit_on(Sdag1, i, n_qubits))
    for i in range(n_qubits):
        for j in range(n_qubits):
            if i != j:
                gens.append(cnot_on(i, j, n_qubits))
    return gens


def sample_random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random unitary via QR of Ginibre."""
    Z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    D = np.diag(R) / np.abs(np.diag(R))
    return Q * D


def noise_channel(rho: np.ndarray, U_noise: np.ndarray, p: float) -> np.ndarray:
    return p * rho + (1.0 - p) * (U_noise @ rho @ U_noise.conj().T)


def true_avg_fidelity_unitary_mix(p: float, U_noise: np.ndarray, d: int) -> float:
    """Average gate fidelity of T(rho) = p*rho + (1-p) * U rho U^dagger."""
    trU = np.trace(U_noise)
    F_U = (abs(trU) ** 2 + d) / (d * (d + 1))  # avg fidelity of U vs I
    return p * 1.0 + (1.0 - p) * F_U


def run_rb_sequence_clifford(
    generators: list[np.ndarray],
    d: int,
    m: int,        # number of Clifford "gates" in sequence
    b: int,        # number of generator steps per Clifford (mixing depth)
    p: float,
    U_noise: np.ndarray,
    rng: np.random.Generator,
) -> float:
    """One RB sequence: m Clifford gates each composed of b generators.
    Noise is applied ONCE per Clifford (per paper's protocol, where each 'gate' is one Clifford
    and the noise T describes the imperfection of implementing one gate; here each 'gate' is
    the product of b generators, so we lump b generators together as one implementable Clifford
    and apply noise once at the end of each block).
    Then invert the total composition (perfectly), measure P(|0..0>).
    """
    total_gens = m * b
    idxs = rng.integers(0, len(generators), size=total_gens)
    # Precompute the composite unitary of the applied sequence (for inversion)
    composite = np.eye(d, dtype=complex)
    for i in idxs:
        composite = generators[i] @ composite

    U_inv = composite.conj().T  # perfect inversion

    # Now simulate with density matrix
    rho = np.zeros((d, d), dtype=complex)
    rho[0, 0] = 1.0
    for block in range(m):
        # Apply b generators (perfectly), then one noise event (paper's convention)
        for k in range(b):
            U = generators[idxs[block * b + k]]
            rho = U @ rho @ U.conj().T
        # Noise per Clifford block
        rho = noise_channel(rho, U_noise, p)
    # Inversion (noiseless in this idealization)
    rho = U_inv @ rho @ U_inv.conj().T
    return float(rho[0, 0].real)


def rb_experiment_clifford(
    generators: list[np.ndarray],
    d: int,
    m_list: list[int],
    b: int,
    p: float,
    M: int,
    U_noise: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    P_out = np.zeros(len(m_list))
    for k, m in enumerate(m_list):
        vals = np.array([
            run_rb_sequence_clifford(generators, d, m, b, p, U_noise, rng)
            for _ in range(M)
        ])
        P_out[k] = vals.mean()
    return np.array(m_list), P_out


def fit_single_exp(m, P):
    def model(m, A, B, f):
        return A + B * (f ** m)
    A0 = float(P[-1])
    B0 = float(P[0] - A0)
    try:
        popt, _ = curve_fit(model, m, P, p0=[A0, B0, 0.99], maxfev=20000,
                            bounds=([0.0, -2.0, 0.0], [1.0, 2.0, 1.0]))
        return float(popt[0]), float(popt[1]), float(popt[2])
    except Exception as e:
        print("fit failed:", e)
        return float("nan"), float("nan"), float("nan")


# Fidelity conversion:  the fit's f gives an effective per-Clifford decay rate.
# Standard RB relation: for a d-dim depolarizing channel with avg fidelity F,
#   survival probability decays as A + B * f^m with f = (d*F - 1)/(d - 1).
# Inverting:  F = ((d-1)*f + 1)/d.
def f_to_F_hat(f: float, d: int) -> float:
    return ((d - 1) * f + 1) / d


def main():
    n_qubits = 2
    d = 2 ** n_qubits
    gens = clifford_generators(n_qubits)
    print(f"n_qubits={n_qubits}, |A|={len(gens)} generators (expect 3n + n(n-1) = {3*n_qubits + n_qubits*(n_qubits-1)})")

    rng = np.random.default_rng(20260704)

    # Sweep (p, b, M) similar to paper's Table 3-style
    settings = [
        {"p": 0.99, "b": 8, "M": 40, "m_list": [1, 2, 4, 8, 12, 20, 30, 40]},
        {"p": 0.98, "b": 8, "M": 40, "m_list": [1, 2, 4, 8, 12, 20, 30, 40]},
        {"p": 0.95, "b": 8, "M": 40, "m_list": [1, 2, 4, 8, 12, 20, 30, 40]},
    ]

    results = []
    for cfg in settings:
        p, b, M = cfg["p"], cfg["b"], cfg["M"]
        m_list = cfg["m_list"]
        errs = []
        fs = []
        F_trues = []
        # Multiple random noise channels
        n_channels = 10
        t0 = time.time()
        for c in range(n_channels):
            U_noise = sample_random_unitary(d, rng)
            F_true = true_avg_fidelity_unitary_mix(p, U_noise, d)
            m_arr, P_arr = rb_experiment_clifford(gens, d, m_list, b, p, M, U_noise, rng)
            A, B, f = fit_single_exp(m_arr, P_arr)
            if not math.isnan(f):
                F_hat = f_to_F_hat(f, d)
                # F_hat is the estimated F per GENERATOR event since noise is per-generator.
                # F_true above is the fidelity of the T channel applied per GENERATOR.
                err = abs(F_true - F_hat)
                errs.append(err); fs.append(f); F_trues.append(F_true)
        errs = np.array(errs); fs = np.array(fs); F_trues = np.array(F_trues)
        dt = time.time() - t0
        print(f"[Clif n={n_qubits} p={p} b={b} M={M}] channels={len(errs)}/{n_channels} "
              f"<F_true>={F_trues.mean():.6f} <F_hat>={f_to_F_hat(fs.mean(), d):.6f} "
              f"mean_err={errs.mean():.6f} median_err={np.median(errs):.6f} "
              f"std_err={errs.std():.6f} time={dt:.1f}s")
        results.append({
            "group": f"Clifford({n_qubits})",
            "n_qubits": n_qubits, "d": d, "p": p, "b": b, "M": M,
            "n_channels": len(errs),
            "F_true_mean": float(F_trues.mean()),
            "F_hat_mean": float(f_to_F_hat(fs.mean(), d)),
            "mean_error": float(errs.mean()),
            "median_error": float(np.median(errs)),
            "std_error": float(errs.std()),
            "time_seconds": dt,
            "m_list": m_list,
        })

    out = Path(__file__).resolve().parent.parent / "report" / "evidence" / "results_clifford.json"
    out.write_text(json.dumps({
        "paper": "arXiv:1803.03621 França & Hashagen",
        "table": "Section 7.2, Table 3/5-style (generator-based Clifford RB, low-Kraus-rank noise)",
        "notes": (
            "We use n_qubits=2 (d=4) instead of paper's n=5. Noise is T(rho) = p*rho + (1-p) U rho U^dagger "
            "with U Haar-random per run (paper's Table 5 setup, delta-covariant with delta=p). "
            "b is the number of generator steps per Clifford; m is the number of Clifford blocks. "
            "Success criterion: mean |F_true - F_hat| should be O(10^-3) for p close to 1."
        ),
        "generators_count": len(gens),
        "results": results,
    }, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
