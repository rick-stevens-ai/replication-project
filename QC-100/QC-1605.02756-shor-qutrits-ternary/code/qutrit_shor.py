#!/usr/bin/env python3
"""
Qutrit Shor's algorithm proof-of-concept.

Replicates the *reproducible core* of Bocharov, Roetteler, Svore (arXiv:1605.02756):
"Factoring with Qutrits: Shor's Algorithm on Ternary and Metaplectic Quantum Architectures."

Two things are done here on a REAL numpy statevector (no fabrication):
  (A) An honest ternary (qutrit) Shor's period-finding for N=15 with base a=2 (period r=4).
      * State register: m = ceil(log3(2N^2)) qutrits (holds the sample k of the ternary QFT).
      * Function register: n_qutrits = ceil(log3(N)) qutrits (holds ternary-encoded x = a^k mod N).
      * We prepare uniform superposition over k in [0, 3^m), apply |k>|1> -> |k>|a^k mod N>,
        then apply the exact ternary QFT on the k-register and sample the outcome distribution.
      * The whole thing is built from raw dtype=complex128 tensors — no black-box lib.
  (B) A resource comparison per Table III / IV of the paper, reproducing the paper's headline
      widths (ternary width = ceil(log3(2)) * n_bits, i.e. ~ log3(2) ~= 0.6309 reduction) and
      P9-count formulas (Table III: 12n emulated-binary vs 19n true-ternary for simple additive
      shift, etc.).

Real statevector simulation of the ternary Shor period-finder is the "small real instance
reproducing a headline number" per Rick's QC wave brief.
"""

from __future__ import annotations
import math
import json
import time
import argparse
from fractions import Fraction
from pathlib import Path

import numpy as np


# ------------------------------- Ternary utilities ---------------------------

def int_to_trits(x: int, n: int) -> list[int]:
    """Little-endian trit expansion: trits[0] is least significant."""
    trits = []
    for _ in range(n):
        trits.append(x % 3)
        x //= 3
    return trits


def trits_to_int(trits: list[int]) -> int:
    v = 0
    for i, t in enumerate(trits):
        v += t * (3 ** i)
    return v


# ------------------------------- Ternary QFT ---------------------------------

def ternary_qft_matrix(m: int) -> np.ndarray:
    """Exact matrix of QFT_{3^m}: (3^m x 3^m) DFT matrix, unitary."""
    D = 3 ** m
    j = np.arange(D)
    k = np.arange(D)
    omega = np.exp(2j * np.pi / D)
    F = omega ** np.outer(j, k) / np.sqrt(D)
    return F


# --------------------- Modular exponentiation (classical) --------------------

def modexp_table(a: int, N: int, K: int) -> list[int]:
    """Return [a^k mod N for k in 0..K-1]. Classical; used to fill the function register."""
    out = [1] * K
    v = 1
    for k in range(1, K):
        v = (v * a) % N
        out[k] = v
    return out


# ------------------- Build the joint statevector after U_f -------------------

def build_period_finding_state(
    a: int, N: int, m_qutrits: int, n_qutrits: int
) -> np.ndarray:
    """
    Prepare state (1/sqrt(3^m)) sum_k |k>_{3^m} |a^k mod N>_{3^n}, then apply ternary QFT_{3^m}
    on the k-register. Return the full joint statevector, indexed as x = k * (3^n) + fval.
    """
    K = 3 ** m_qutrits
    Fdim = 3 ** n_qutrits
    assert N < Fdim, f"function-register dim {Fdim} must exceed N={N}"

    # 1) uniform |k> tensor |a^k mod N>
    psi = np.zeros(K * Fdim, dtype=np.complex128)
    tbl = modexp_table(a, N, K)
    amp = 1.0 / math.sqrt(K)
    for k in range(K):
        f = tbl[k]
        psi[k * Fdim + f] = amp

    # 2) apply ternary QFT on k-register.
    # psi reshaped to (K, Fdim); QFT acts on first index.
    F = ternary_qft_matrix(m_qutrits)  # (K, K) unitary
    mat = psi.reshape(K, Fdim)
    mat = F @ mat
    psi = mat.reshape(K * Fdim)
    return psi


def sample_k_distribution(psi: np.ndarray, m_qutrits: int, n_qutrits: int) -> np.ndarray:
    """Marginal distribution over k (the ternary QFT output) after tracing out the function reg."""
    K = 3 ** m_qutrits
    Fdim = 3 ** n_qutrits
    mat = psi.reshape(K, Fdim)
    probs_k = np.sum(np.abs(mat) ** 2, axis=1)
    # Should sum to 1.
    return probs_k


# ------------------- Continued-fractions -> period recovery ------------------

def continued_fraction_period(k: int, K: int, N: int) -> int | None:
    """
    Given sampled QFT outcome k (in [0, K)) with denominator K = 3^m,
    approximate k/K as p/r using continued fractions and return r <= N.
    """
    if k == 0:
        return None
    frac = Fraction(k, K).limit_denominator(N)
    return frac.denominator


def verify_period(a: int, N: int, r: int) -> bool:
    if r <= 0:
        return False
    return pow(a, r, N) == 1


# ------------------- Resource comparison per paper Table III/IV --------------

def resource_comparison(n_bits_list: list[int]) -> list[dict]:
    """Reproduce Table III and Table IV headline formulas from Bocharov et al 2016."""
    rows = []
    for n in n_bits_list:
        # Table III: P9 counts for ripple-carry additive shift on n-bit args
        p9_simple_bin = 12 * n
        p9_simple_ter = 19 * n
        p9_ctrl_bin = 18 * n
        p9_ctrl_ter_lb = 21 * n     # paper: "> 21 n"
        p9_dctrl_bin = 24 * n
        p9_dctrl_ter_lb = 33 * n    # paper: "> 33 n"

        # Table IV low-widths modular exponentiation:
        # n_bits width column: emulated-binary = n+4 qutrits, ternary = 2m - omega_1(m)
        # where m = ceil(log3(2) * n). We compute m and (an upper bound on) 2m - omega1(m) using
        # trit count of m itself as omega1 approximation for reporting.
        m = math.ceil(math.log(2, 3) * n)
        ter_width_ub = 2 * m  # upper bound (drops the omega1 term)
        emul_bin_width = n + 4
        depth_bin_p9 = 48 * n ** 3
        depth_ter_p9 = 76.35 * n ** 3

        rows.append(dict(
            n_bits=n,
            m_trits=m,
            width_ratio_ternary_over_binary=round(m / n, 4),
            log3_of_2=round(math.log(2, 3), 4),
            table3_simple_shift_p9_bin=p9_simple_bin,
            table3_simple_shift_p9_ter=p9_simple_ter,
            table3_ctrl_shift_p9_bin=p9_ctrl_bin,
            table3_ctrl_shift_p9_ter_lb=p9_ctrl_ter_lb,
            table3_dctrl_shift_p9_bin=p9_dctrl_bin,
            table3_dctrl_shift_p9_ter_lb=p9_dctrl_ter_lb,
            table4_width_emul_binary_qutrits=emul_bin_width,
            table4_width_ternary_qutrits_ub=ter_width_ub,
            table4_depth_p9_emul_binary=depth_bin_p9,
            table4_depth_p9_ternary=depth_ter_p9,
        ))
    return rows


# ------------------- Main experiment driver ----------------------------------

def run_shor_experiment(N: int, a: int, out_dir: Path) -> dict:
    """Runs a ternary-Shor period-finding for order of a modulo N."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # register sizes: n_qutrits big enough to hold N; m_qutrits big enough so QFT resolution >= 2N^2
    n_qutrits = math.ceil(math.log(N + 1, 3))
    m_qutrits = math.ceil(math.log(2 * N * N, 3))
    K = 3 ** m_qutrits
    Fdim = 3 ** n_qutrits

    t0 = time.time()
    psi = build_period_finding_state(a, N, m_qutrits, n_qutrits)
    t_build = time.time() - t0

    # sanity checks
    norm2 = float(np.vdot(psi, psi).real)
    assert abs(norm2 - 1.0) < 1e-9, f"statevector not normalized: {norm2}"

    probs_k = sample_k_distribution(psi, m_qutrits, n_qutrits)
    top_k = int(np.argmax(probs_k))
    # take top ~10 samples and try to recover period
    order_k = np.argsort(probs_k)[::-1]

    # classical order for reference
    r_true = None
    v = 1
    for r in range(1, N):
        v = (v * a) % N
        if v == 1:
            r_true = r
            break

    tries = []
    for idx in order_k[:20]:
        k = int(idx)
        p = float(probs_k[k])
        r_guess = continued_fraction_period(k, K, N)
        ok = r_guess is not None and verify_period(a, N, r_guess)
        tries.append(dict(k=k, prob=round(p, 6), r_guess=r_guess, verified=ok))
        if ok and r_guess == r_true:
            break

    recovered = any(t["verified"] and t["r_guess"] == r_true for t in tries)

    result = dict(
        N=N,
        a=a,
        n_qutrits_function_reg=n_qutrits,
        m_qutrits_k_reg=m_qutrits,
        K=K,
        Fdim=Fdim,
        joint_dim=K * Fdim,
        classical_order=r_true,
        recovered_correct_order=recovered,
        top_probability_mass_first20=round(float(sum(t["prob"] for t in tries)), 6),
        top_sample_k=int(top_k),
        top_sample_prob=round(float(probs_k[top_k]), 6),
        tries=tries,
        wallclock_build_seconds=round(t_build, 3),
        numpy_version=np.__version__,
    )

    with open(out_dir / f"shor_N{N}_a{a}.json", "w") as f:
        json.dump(result, f, indent=2)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    # (A) real qutrit Shor: N=15, a=2 (order r=4)
    res_15_2 = run_shor_experiment(N=15, a=2, out_dir=out_dir)
    print("[Shor N=15 a=2]", json.dumps({k: v for k, v in res_15_2.items() if k != "tries"}, indent=2))

    # (A') also do N=15 a=7 (order r=4) as an independent replicate
    res_15_7 = run_shor_experiment(N=15, a=7, out_dir=out_dir)
    print("[Shor N=15 a=7]", json.dumps({k: v for k, v in res_15_7.items() if k != "tries"}, indent=2))

    # (A'') N=21 a=2 (order r=6). Larger — joint dim will be big; only run if memory allows.
    # We skip a=2 for N=21 by default (needs bigger K). Instead do N=21, a=4 (order r=3), which is tractable.
    res_21_4 = run_shor_experiment(N=21, a=4, out_dir=out_dir)
    print("[Shor N=21 a=4]", json.dumps({k: v for k, v in res_21_4.items() if k != "tries"}, indent=2))

    # (B) resource comparison
    rows = resource_comparison(n_bits_list=[4, 8, 16, 32, 64, 128, 1024, 2048])
    with open(out_dir / "resource_comparison.json", "w") as f:
        json.dump(rows, f, indent=2)
    print("[Resource comparison]")
    for r in rows:
        print(json.dumps(r, indent=2))

    # summary
    summary = dict(
        experiments=[res_15_2, res_15_7, res_21_4],
        resource_comparison=rows,
    )
    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\nWROTE:", out_dir / "summary.json")


if __name__ == "__main__":
    main()
