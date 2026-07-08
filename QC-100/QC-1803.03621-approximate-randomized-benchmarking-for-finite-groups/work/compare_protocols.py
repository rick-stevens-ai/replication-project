"""
Compare three RB protocols on the same monomial-unitary MU(d,8) group with the same noise:

  P1: Full uniform sampling from the group (Section 4 protocol).
      Each RB gate is drawn uniformly at random from MU(d,8).
  P2: Generator-based (Section 6 protocol).
      Each RB gate is the product of b generator steps chosen uniformly from the generator set.
  P3: Approximate-Haar sampling via Markov chain (Section 5 protocol).
      Same as P2 but for a larger b (mixing block); we treat b=large as effectively approximate-Haar.

Paper's claim (Section 7.2 final paragraph + Figure 1): "the three yield indistinguishable
results in the high fidelity regime".  We test this by fitting the same exponential decay
and comparing extracted F_hat across the three protocols on the same channel.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

# reuse code
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from monomial_rb import (
    Monomial, sample_monomial, identity_monomial, apply_noise,
    sample_random_density_matrix, true_avg_fidelity, fit_single_exp
)


def monomial_generators(d: int, n: int) -> list[Monomial]:
    """A natural generator set for MU(d, n): adjacent transpositions of the permutation
    part + phase gates diag(1, ..., 1, e^(2 pi i /n), 1, ..., 1) at each position.

    - (d-1) adjacent transpositions of positions
    - d diagonal phase-shift gates (each puts an n-th root of unity on one position)
    - their inverses

    This is closed under inverse (transpositions self-inverse; phase gates inverse = another power).
    """
    gens = []
    # adjacent transpositions
    for i in range(d - 1):
        perm = np.arange(d, dtype=np.int32)
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
        phases = np.ones(d, dtype=complex)
        gens.append(Monomial(perm=perm, phases=phases))
    # phase gates: at position i, put e^(2 pi i / n) with all others 1
    omega = np.exp(2j * np.pi / n)
    for pos in range(d):
        phases = np.ones(d, dtype=complex)
        phases[pos] = omega
        perm = np.arange(d, dtype=np.int32)
        gens.append(Monomial(perm=perm, phases=phases))
    # inverses of phase gates: e^(-2 pi i /n)
    omega_inv = np.exp(-2j * np.pi / n)
    for pos in range(d):
        phases = np.ones(d, dtype=complex)
        phases[pos] = omega_inv
        perm = np.arange(d, dtype=np.int32)
        gens.append(Monomial(perm=perm, phases=phases))
    return gens


def compose_gens(idxs: np.ndarray, gens: list[Monomial], d: int) -> Monomial:
    out = identity_monomial(d)
    for i in idxs:
        out = gens[int(i)] @ out
    return out


def run_seq_full(d: int, n: int, m: int, p: float, sigma: np.ndarray, rng: np.random.Generator) -> float:
    """Protocol 1: sample m elements uniformly from MU(d,n)."""
    gates = [sample_monomial(d, n, rng) for _ in range(m)]
    composite = identity_monomial(d)
    for g in gates:
        composite = g @ composite
    inv = composite.inverse()

    rho = np.zeros((d, d), dtype=complex)
    rho[0, 0] = 1.0
    for g in gates:
        M = g.to_matrix()
        rho = M @ rho @ M.conj().T
        rho = apply_noise(rho, sigma, p)
    Minv = inv.to_matrix()
    rho = Minv @ rho @ Minv.conj().T
    return float(rho[0, 0].real)


def run_seq_gen(d: int, n: int, m: int, b: int, gens: list[Monomial],
                p: float, sigma: np.ndarray, rng: np.random.Generator) -> float:
    """Protocol 2/3: each 'gate' = b generator steps; noise per gate (per Clifford analog)."""
    total = m * b
    idxs = rng.integers(0, len(gens), size=total)
    composite = identity_monomial(d)
    for i in idxs:
        composite = gens[int(i)] @ composite
    inv = composite.inverse()

    rho = np.zeros((d, d), dtype=complex)
    rho[0, 0] = 1.0
    for block in range(m):
        for k in range(b):
            M = gens[int(idxs[block * b + k])].to_matrix()
            rho = M @ rho @ M.conj().T
        rho = apply_noise(rho, sigma, p)
    Minv = inv.to_matrix()
    rho = Minv @ rho @ Minv.conj().T
    return float(rho[0, 0].real)


def run_experiment(d: int, n: int, p: float, M: int, m_list: list[int],
                   sigma: np.ndarray, b_gen: int, b_approx: int,
                   gens: list[Monomial], rng: np.random.Generator):
    def avg_over_M(runner, m):
        return float(np.mean([runner(m) for _ in range(M)]))

    P_full = np.array([avg_over_M(lambda mm: run_seq_full(d, n, mm, p, sigma, rng), m) for m in m_list])
    P_gen  = np.array([avg_over_M(lambda mm: run_seq_gen(d, n, mm, b_gen, gens, p, sigma, rng), m) for m in m_list])
    P_apx  = np.array([avg_over_M(lambda mm: run_seq_gen(d, n, mm, b_approx, gens, p, sigma, rng), m) for m in m_list])

    m_arr = np.array(m_list)
    _, _, f_full = fit_single_exp(m_arr, P_full)
    _, _, f_gen  = fit_single_exp(m_arr, P_gen)
    _, _, f_apx  = fit_single_exp(m_arr, P_apx)

    F_true = true_avg_fidelity(p, d)
    F_full = true_avg_fidelity(f_full, d)
    F_gen  = true_avg_fidelity(f_gen, d)
    F_apx  = true_avg_fidelity(f_apx, d)
    return {
        "F_true": F_true,
        "F_full": F_full, "err_full": abs(F_true - F_full),
        "F_gen":  F_gen,  "err_gen":  abs(F_true - F_gen),
        "F_apx":  F_apx,  "err_apx":  abs(F_true - F_apx),
        "P_full": P_full.tolist(), "P_gen": P_gen.tolist(), "P_apx": P_apx.tolist(),
        "f_full": f_full, "f_gen": f_gen, "f_apx": f_apx,
    }


def main():
    d, n = 4, 8
    p = 0.95
    M = 60
    m_list = [1, 2, 4, 8, 12, 20, 30, 40]
    b_gen = 3
    b_approx = 15
    rng = np.random.default_rng(20260704)
    gens = monomial_generators(d, n)
    print(f"MU({d},{n}) generator count = {len(gens)}")

    n_channels = 10
    entries = []
    t0 = time.time()
    for c in range(n_channels):
        sigma = sample_random_density_matrix(d, rng)
        res = run_experiment(d, n, p, M, m_list, sigma, b_gen, b_approx, gens, rng)
        entries.append(res)
        print(f"[ch {c+1:02d}] F_true={res['F_true']:.5f}  "
              f"F_full={res['F_full']:.5f} (err {res['err_full']:.5f})  "
              f"F_gen={res['F_gen']:.5f} (err {res['err_gen']:.5f})  "
              f"F_apx={res['F_apx']:.5f} (err {res['err_apx']:.5f})")
    dt = time.time() - t0

    errs_full = np.array([e["err_full"] for e in entries])
    errs_gen  = np.array([e["err_gen"] for e in entries])
    errs_apx  = np.array([e["err_apx"] for e in entries])
    print(f"\nMean errors  full={errs_full.mean():.5f}  gen(b={b_gen})={errs_gen.mean():.5f}  approx(b={b_approx})={errs_apx.mean():.5f}")
    print(f"time = {dt:.1f}s")

    out = Path(__file__).resolve().parent.parent / "report" / "evidence" / "results_compare.json"
    out.write_text(json.dumps({
        "paper": "arXiv:1803.03621 França & Hashagen",
        "test": "Section 7.2 final paragraph / Fig 1: three protocols yield indistinguishable results in high-fidelity regime",
        "config": {"d": d, "n": n, "p": p, "M": M, "m_list": m_list,
                   "b_gen": b_gen, "b_approx": b_approx, "n_channels": n_channels,
                   "generators_count": len(gens)},
        "per_channel": entries,
        "summary": {
            "mean_err_full": float(errs_full.mean()),
            "mean_err_gen":  float(errs_gen.mean()),
            "mean_err_apx":  float(errs_apx.mean()),
            "median_err_full": float(np.median(errs_full)),
            "median_err_gen":  float(np.median(errs_gen)),
            "median_err_apx":  float(np.median(errs_apx)),
            "std_err_full": float(errs_full.std()),
            "std_err_gen":  float(errs_gen.std()),
            "std_err_apx":  float(errs_apx.std()),
        },
        "time_seconds": dt,
    }, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
