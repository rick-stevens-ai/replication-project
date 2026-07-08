"""Robust Phase Estimation (RPE) simulation for a single-qubit X-rotation
with a small over-rotation error epsilon.

Reproduces the core claim of Kimmel, Low, Yoder (arXiv:1502.02677):
RPE achieves Heisenberg-limited scaling of the estimation error,
sigma(eps_hat) ~ 1/N, versus the shot-noise 1/sqrt(N) scaling.

Setup
-----
Gate under test: U(phi) = R_x(phi + eps),  with phi = pi/2 (target rotation).
We want to estimate the phase A = phi + eps  (mod 2pi).  Equivalently, we
estimate eps = A - phi.

Following Higgins et al. / Kimmel et al. (Eqs. V.1-V.3):
For each generation j = 1..K, we take k_j = 2^{j-1} applications of U and
perform two families of experiments:

    p0(A, k) = (1 + cos(k*A)) / 2       -- "cos" experiment (|0>-prep)
    p+(A, k) = (1 + sin(k*A)) / 2       -- "sin" experiment (|+>-prep)

We use M_j samples of each, form estimators
    a0_hat = successes_cos / M_j,  a+_hat = successes_sin / M_j,
    k*A_hat = atan2(a+_hat - 1/2,  a0_hat - 1/2)   in (-pi, pi],
and combine across j to lift the 2*pi/k_j ambiguity (Higgins ladder).

Circuit implementation for a single-qubit X-rotation phase experiment
----------------------------------------------------------------------
Let U = R_x(A) (up to a global phase).  Applying U^k gives R_x(k*A), so

    <0| U^k |0>  =  cos(k*A/2)^2 = (1 + cos(k*A))/2   -> matches p0 (with A -> A? see note)

Wait: cos(k*A/2)^2 = (1 + cos(k*A))/2.  So measuring |0> after U^k|0> gives
p0(A, k) = (1 + cos(k*A))/2, exactly as required.

For the sin experiment we need (1 + sin(k*A))/2 = |<0| R_y(-pi/2) U^k |0>|^2?
Compute:  R_y(-pi/2)|0> = cos(pi/4)|0> + sin(pi/4)|1> = |+>.
Apply U^k = R_x(k*A):  R_x(theta)|+> = cos(theta/2)|+> - i sin(theta/2)|->? 
Simpler: use the "sin" family via preparing |+> and measuring in Y basis, or
equivalently prepend a Y(pi/2) so we measure the sine quadrature.

We use the standard trick: for the sin experiment, apply S^dagger H before
measurement (measure in Y basis).  For R_x(k A) starting in |0>:
    |psi> = cos(kA/2)|0> - i sin(kA/2)|1>
    <Y=+1|psi>^2 = |<+i|psi>|^2 = |(1/sqrt2)(cos(kA/2) - (-i)*i sin(kA/2))|^2
                 = |(1/sqrt2)(cos(kA/2) - sin(kA/2))|^2 ... hmm.

To be safe, we bypass Qiskit's simulator quirks and compute exact statevector
outcome probabilities analytically for the R_x^k circuit (equivalent to
Qiskit statevector), then sample counts via numpy binomial.  We ALSO run
the Qiskit statevector simulator on the same circuit to cross-check the
analytic probabilities (see code/qiskit_verify.py).

References
----------
Kimmel, Low, Yoder, arXiv:1502.02677, Eqs. (V.1)-(V.3), Sec. V.
Higgins et al., New J. Phys. 11, 073023 (2009).
"""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
from typing import Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Exact single-qubit probabilities for the R_x(k*A) experiments.
# ---------------------------------------------------------------------------

def cos_prob(A: float, k: int) -> float:
    """P(outcome=0 | apply R_x(k*A) to |0>, measure Z)  =  (1 + cos(kA))/2."""
    return 0.5 * (1.0 + math.cos(k * A))


def sin_prob(A: float, k: int) -> float:
    """Sin-quadrature experiment.

    Prepare |0>, apply R_x(k*A), then apply S H to rotate the Y-basis
    measurement into a Z-measurement.  The probability of outcome=0 is
    (1 + sin(kA))/2.

    Derivation (single qubit):
        R_x(theta)|0>  =  cos(theta/2)|0> - i sin(theta/2)|1>.
        Measurement in the Y basis: |+_y> = (|0> + i|1>)/sqrt2,
                                    |-_y> = (|0> - i|1>)/sqrt2.
        <+_y|psi> = (1/sqrt2)(cos(theta/2) - i * i * sin(theta/2))
                  = (1/sqrt2)(cos(theta/2) + sin(theta/2)).
        |<+_y|psi>|^2 = 0.5 (1 + 2 cos(theta/2) sin(theta/2))
                      = 0.5 (1 + sin(theta)).
    So P(Y=+1) = (1 + sin(kA))/2 for theta = kA.  Good.
    """
    return 0.5 * (1.0 + math.sin(k * A))


# ---------------------------------------------------------------------------
# Single RPE run: given true A, budget schedule, return estimate A_hat.
# ---------------------------------------------------------------------------

def rpe_estimate(A_true: float, K: int, M: int, rng: np.random.Generator) -> Tuple[float, int]:
    """Run one RPE estimate.

    Parameters
    ----------
    A_true : float
        True phase we want to estimate (in radians, in (-pi, pi]).
    K : int
        Number of generations.  k_j = 2^{j-1} for j = 1..K.
    M : int
        Samples per experiment per generation (same for cos and sin).
    rng : numpy Generator

    Returns
    -------
    A_hat : float
    total_queries : int
        Total number of applications of U across all experiments.
    """
    A_hat = 0.0
    total_queries = 0
    prev = None  # previous generation's estimate

    for j in range(1, K + 1):
        k = 2 ** (j - 1)
        # Draw counts for cos and sin experiments (M shots each).
        p0 = cos_prob(A_true, k)
        pp = sin_prob(A_true, k)
        n0 = rng.binomial(M, p0)
        npl = rng.binomial(M, pp)
        # Estimator for k*A in (-pi, pi]:
        # atan2(a+_hat - 1/2, a0_hat - 1/2) since
        #   a0_hat - 1/2 = 0.5 cos(kA), a+_hat - 1/2 = 0.5 sin(kA).
        kA_hat = math.atan2(npl / M - 0.5, n0 / M - 0.5)
        # Naive candidate estimate.
        A_j_raw = kA_hat / k
        if prev is None:
            A_j = A_j_raw
        else:
            # Unwrap: choose n so that A_j = A_j_raw + 2*pi*n/k is closest to prev.
            # Equivalently, add multiple of 2*pi/k to A_j_raw to minimize
            # |A_j - prev|.
            spacing = 2.0 * math.pi / k
            n = round((prev - A_j_raw) / spacing)
            A_j = A_j_raw + n * spacing
        prev = A_j
        A_hat = A_j
        # Each experiment applies U k times, and we run 2 experiment families
        # (cos + sin) with M shots each: total queries at generation j = 2*M*k.
        total_queries += 2 * M * k

    return A_hat, total_queries


# ---------------------------------------------------------------------------
# Sweep over K to build a precision-vs-N curve.
# ---------------------------------------------------------------------------

def wrap_pi(x: float) -> float:
    """Wrap x to (-pi, pi]."""
    y = (x + math.pi) % (2.0 * math.pi) - math.pi
    if y == -math.pi:
        y = math.pi
    return y


def run_sweep(A_true: float, K_values, M: int, trials: int, seed: int = 12345):
    rng = np.random.default_rng(seed)
    results = []
    for K in K_values:
        errs = []
        Ns = []
        for _ in range(trials):
            A_hat, N = rpe_estimate(A_true, K, M, rng)
            err = wrap_pi(A_hat - A_true)
            errs.append(err)
            Ns.append(N)
        errs = np.asarray(errs)
        Ns = np.asarray(Ns)
        rmse = float(np.sqrt(np.mean(errs ** 2)))
        median_abs = float(np.median(np.abs(errs)))
        mean_N = float(np.mean(Ns))
        results.append({
            "K": int(K),
            "k_max": int(2 ** (K - 1)),
            "M_per_experiment": int(M),
            "trials": int(trials),
            "mean_total_queries_N": mean_N,
            "rmse_error": rmse,
            "median_abs_error": median_abs,
        })
    return results


def run_shot_noise_baseline(A_true: float, N_values, trials: int, seed: int = 6789):
    """Shot-noise baseline: use ONLY k=1 experiments (no Heisenberg speedup),
    just increase M until you've used ~N queries.  Estimator: same atan2 on
    the k=1 data.  Standard deviation should scale as 1/sqrt(N)."""
    rng = np.random.default_rng(seed)
    results = []
    for N in N_values:
        # k=1, cos+sin, so M = N/2.
        M = max(1, int(N // 2))
        errs = []
        for _ in range(trials):
            n0 = rng.binomial(M, cos_prob(A_true, 1))
            npl = rng.binomial(M, sin_prob(A_true, 1))
            A_hat = math.atan2(npl / M - 0.5, n0 / M - 0.5)
            errs.append(wrap_pi(A_hat - A_true))
        errs = np.asarray(errs)
        rmse = float(np.sqrt(np.mean(errs ** 2)))
        results.append({
            "N_target": int(N),
            "M_at_k1": int(M),
            "actual_queries": int(2 * M),
            "rmse_error": rmse,
        })
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=str, default=str(Path(__file__).resolve().parents[1] / "data"))
    ap.add_argument("--epsilon", type=float, default=0.037,
                    help="over-rotation angle for R_x(pi/2 + epsilon)")
    ap.add_argument("--K-min", type=int, default=1)
    ap.add_argument("--K-max", type=int, default=12)
    ap.add_argument("--M", type=int, default=30, help="samples per experiment per generation")
    ap.add_argument("--trials", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260703)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # True gate phase: target R_x(pi/2) with over-rotation epsilon.
    A_true = math.pi / 2 + args.epsilon
    A_true = wrap_pi(A_true)

    K_values = list(range(args.K_min, args.K_max + 1))
    rpe_results = run_sweep(A_true, K_values, args.M, args.trials, args.seed)

    # Shot-noise baseline over the same total-query budgets as RPE.
    N_values = [int(round(r["mean_total_queries_N"])) for r in rpe_results]
    sn_results = run_shot_noise_baseline(A_true, N_values, args.trials, args.seed + 1)

    payload = {
        "paper": "arXiv:1502.02677",
        "gate_under_test": "R_x(pi/2 + epsilon)",
        "epsilon_true": args.epsilon,
        "A_true": A_true,
        "K_values": K_values,
        "M_per_experiment": args.M,
        "trials_per_point": args.trials,
        "seed": args.seed,
        "rpe": rpe_results,
        "shot_noise_baseline": sn_results,
    }
    out_json = outdir / "rpe_sweep.json"
    out_json.write_text(json.dumps(payload, indent=2))
    print(f"[ok] wrote {out_json}")

    # Quick console table.
    print(f"\nA_true = {A_true:.6f} rad  (epsilon = {args.epsilon:.6f})")
    print(f"{'K':>3} {'k_max':>6} {'<N>':>10} {'RPE RMSE':>12} {'SN RMSE':>12}")
    for r, s in zip(rpe_results, sn_results):
        print(f"{r['K']:>3} {r['k_max']:>6} {r['mean_total_queries_N']:>10.0f} "
              f"{r['rmse_error']:>12.3e} {s['rmse_error']:>12.3e}")


if __name__ == "__main__":
    main()
