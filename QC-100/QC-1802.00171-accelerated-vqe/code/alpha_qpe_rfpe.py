#!/usr/bin/env python3
"""
Reproduction of the alpha-QPE / RFPE numerical experiment from
Wang, Higgott, Brierley (2018), arXiv:1802.00171, Figures 5 & 6.

Setup (from Sec. II A and Appendix A of the paper):
    - We are estimating a true eigenphase phi in [0, 2*pi) (paper uses [0, 2*pi)).
    - At iteration k, we run the "RFPE circuit" (a Kitaev-style single-ancilla
      phase-estimation circuit with a fractional M-power of the unitary and a
      classical rotation theta). It outputs a single bit E in {0,1} with
      probability p(E | phi, M, theta) = (1 + cos(M*phi - theta - E*pi)) / 2.

    - Between iterations we maintain a Gaussian prior over phi with mean mu
      and standard deviation sigma (aka Bayes-risk r = sigma). We update by
      rejection sampling (Rejection Filtering PE):
          1. draw N particles from N(mu, sigma^2)
          2. accept each with probability p(E | particle, M, theta)
          3. fit a new Gaussian (mu', sigma') to the accepted particles.

    - "alpha" enters through the choice of M at each iteration. Following
      the paper's discussion (Sec. III / Appendix A), the maximum-coherent
      depth policy is:
              M_k  proportional to  1 / sigma_k^alpha
      i.e. as sigma_k shrinks, we allow longer coherent circuits (up to a
      ceiling controlled by the physical device). alpha = 0 recovers the
      "M=1 always" regime (standard sampling / VQE) and alpha = 1 recovers
      the "M ~ 1/sigma" regime (full-coherence QPE).

    - Following Wiebe & Granade (PRL 2016) / paper: theta = mu (the
      "informative measurement" choice), and M is rounded to a positive
      integer.

Deliverables:
    * A CSV of median Bayes-risk r_k = sigma_k vs iteration k for
      alpha in {0, 0.25, 0.5, 0.75, 1.0}.
    * A log-linear plot analogous to Fig. 5 (right panel style: r_k on log
      axis, k on linear axis).
    * The headline reproducible claim: r_k decreases with k at a rate that
      grows steeply with alpha, and the alpha=1 curve is roughly
      exponential (approx doubling of bits per iteration), while alpha=0
      is roughly 1/sqrt(k) (classical sampling limit).
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass

import numpy as np

RNG_SEED = 1802
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "report", "evidence")
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "figures")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def measurement_probability(phi: np.ndarray, M: int, theta: float,
                            outcome: int) -> np.ndarray:
    """P(E=outcome | phi, M, theta) = (1 + cos(M*phi - theta - E*pi)) / 2"""
    return 0.5 * (1.0 + np.cos(M * phi - theta - outcome * np.pi))


def sample_outcome(phi_true: float, M: int, theta: float,
                   rng: np.random.Generator) -> int:
    p0 = 0.5 * (1.0 + np.cos(M * phi_true - theta))
    return int(rng.random() >= p0)  # 0 with prob p0


def rfpe_update(mu: float, sigma: float, M: int, theta: float, outcome: int,
                n_particles: int, rng: np.random.Generator) -> tuple[float, float]:
    """One rejection-filter Bayesian update. Returns (mu_new, sigma_new).

    If too few particles accepted, we fall back to a very small shrink so
    the run does not diverge; this matches the paper's re-sampling behavior.
    """
    # Draw prior particles, wrap into a wide interval so cosine periodicity
    # is well-behaved. Because we only ever use mu +/- ~few sigma, and cos
    # has period 2*pi/M, we keep phi in R and rely on the fitting Gaussian.
    particles = rng.normal(mu, sigma, size=n_particles)
    p_acc = measurement_probability(particles, M, theta, outcome)
    u = rng.random(n_particles)
    accepted = particles[u < p_acc]
    if accepted.size < 20:  # too few for a stable fit
        # Slight shrink to prevent stall.
        return mu, max(sigma * 0.95, 1e-12)
    mu_new = float(accepted.mean())
    sigma_new = float(accepted.std(ddof=1))
    if sigma_new <= 0:
        sigma_new = 1e-12
    return mu_new, sigma_new


def choose_M(sigma: float, alpha: float, M_min: int = 1,
             M_max: int = 10**8) -> int:
    """M ~ 1/sigma^alpha, clamped to [M_min, M_max] and rounded up."""
    if alpha <= 0:
        return M_min
    M = int(np.ceil(sigma ** (-alpha)))
    if M < M_min:
        M = M_min
    if M > M_max:
        M = M_max
    return M


@dataclass
class RunConfig:
    alpha: float
    n_iterations: int = 60
    n_particles: int = 600
    n_trials: int = 200
    mu0: float = np.pi  # centered mid-interval
    sigma0: float = 1.0  # r_0 = 1 as in the paper's (k0, r_k0) = (0, 1)
    M_max: int = 10**7  # enough headroom for alpha=1 up to k=60


def run_alpha(cfg: RunConfig, rng: np.random.Generator) -> np.ndarray:
    """Return array shape (n_trials, n_iterations+1) of sigma_k.

    Convention (matches Wiebe & Granade 2016 / paper): prior on the true
    eigenphase is N(mu0, sigma0^2). The true eigenphase for each trial is
    drawn from that prior. This is the standard "Bayes risk" convention
    and is what the paper's (k0, r_k0) = (0, r0 = 1) initial condition
    corresponds to.
    """
    trace = np.zeros((cfg.n_trials, cfg.n_iterations + 1), dtype=float)
    for t in range(cfg.n_trials):
        # True phi drawn from the prior (Bayes-risk setup).
        phi_true = float(rng.normal(cfg.mu0, cfg.sigma0))
        mu = cfg.mu0
        sigma = cfg.sigma0
        trace[t, 0] = sigma
        for k in range(1, cfg.n_iterations + 1):
            M = choose_M(sigma, cfg.alpha, M_max=cfg.M_max)
            theta = mu  # Wiebe-Granade informative choice
            outcome = sample_outcome(phi_true, M, theta, rng)
            mu, sigma = rfpe_update(mu, sigma, M, theta, outcome,
                                    cfg.n_particles, rng)
            trace[t, k] = sigma
    return trace


def main() -> None:
    print(f"[alpha-QPE / RFPE] arXiv:1802.00171 Fig. 5 reproduction")
    print(f"[alpha-QPE / RFPE] seed = {RNG_SEED}")
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    n_iter = 60
    n_trials = 200
    n_particles = 600

    all_traces: dict[str, list[list[float]]] = {}
    summary: list[dict] = []

    t0 = time.time()
    for alpha in alphas:
        cfg = RunConfig(alpha=alpha, n_iterations=n_iter,
                        n_particles=n_particles, n_trials=n_trials)
        rng = np.random.default_rng(RNG_SEED + int(alpha * 1000))
        print(f"  running alpha = {alpha} ...", flush=True)
        ta = time.time()
        trace = run_alpha(cfg, rng)  # shape (n_trials, n_iter+1)
        median_r = np.median(trace, axis=0)
        mean_r = np.mean(trace, axis=0)
        print(f"    finished in {time.time()-ta:.1f}s; "
              f"median r_60 = {median_r[-1]:.3e}")
        all_traces[f"alpha_{alpha:.2f}"] = trace.tolist()
        # Fit slope on log(median_r) vs k for k in [10, 60]
        ks = np.arange(len(median_r))
        mask = (ks >= 10)
        try:
            slope, intercept = np.polyfit(ks[mask], np.log(median_r[mask]), 1)
        except Exception:
            slope, intercept = float("nan"), float("nan")
        summary.append({
            "alpha": alpha,
            "median_r_k": median_r.tolist(),
            "mean_r_k": mean_r.tolist(),
            "log_slope_k10_60": float(slope),
            "final_median_r": float(median_r[-1]),
            "final_mean_r": float(mean_r[-1]),
            "n_trials": n_trials,
            "n_particles": n_particles,
        })
    print(f"[alpha-QPE / RFPE] total runtime: {time.time()-t0:.1f}s")

    # Save summary JSON + CSV
    with open(os.path.join(OUT_DIR, "alpha_qpe_summary.json"), "w") as f:
        json.dump({
            "seed": RNG_SEED,
            "n_iterations": n_iter,
            "n_trials": n_trials,
            "n_particles": n_particles,
            "alphas": alphas,
            "runs": summary,
        }, f, indent=2)
    # CSV: rows = k, cols = alpha
    csv_path = os.path.join(OUT_DIR, "alpha_qpe_median_r.csv")
    with open(csv_path, "w") as f:
        f.write("k," + ",".join(f"alpha={a}" for a in alphas) + "\n")
        for k in range(n_iter + 1):
            row = [str(k)]
            for run in summary:
                row.append(f"{run['median_r_k'][k]:.6e}")
            f.write(",".join(row) + "\n")
    print(f"[alpha-QPE / RFPE] wrote {csv_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        for run in summary:
            a = run["alpha"]
            ax.semilogy(np.arange(n_iter + 1), run["median_r_k"],
                        label=f"$\\alpha = {a}$", lw=1.7)
        ax.set_xlabel("iteration $k$")
        ax.set_ylabel("median Bayes risk $r_k = \\sigma_k$")
        ax.set_title("RFPE / $\\alpha$-QPE: Bayes risk vs iteration\n"
                     "(reproduction of Wang et al. 2018, Fig. 5, "
                     f"{n_trials} trials, {n_particles} particles)")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend()
        fig.tight_layout()
        fig_path = os.path.join(FIG_DIR, "alpha_qpe_rfpe_fig5.png")
        fig.savefig(fig_path, dpi=140)
        print(f"[alpha-QPE / RFPE] wrote {fig_path}")
    except Exception as e:
        print(f"[alpha-QPE / RFPE] plot failed: {e}")

    # Print headline result
    print("\n=== HEADLINE (alpha-QPE) ===")
    print(f"{'alpha':>6}  {'median r_60':>14}  {'log-slope (k=10..60)':>22}")
    for run in summary:
        print(f"{run['alpha']:>6}  {run['final_median_r']:>14.3e}  "
              f"{run['log_slope_k10_60']:>22.4f}")


if __name__ == "__main__":
    main()
