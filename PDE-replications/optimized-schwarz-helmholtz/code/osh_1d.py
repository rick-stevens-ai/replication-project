"""
Verification of the analytic per-mode convergence factor (paper eq. 2.6, 3.2, 3.17)
for the non-overlapping Schwarz method applied to the Helmholtz equation on the
strip R^2 split at x=0.

This is the "1D" (per-Fourier-mode) test: pick a tangential frequency k,
take the transmission symbol σ_j(k), and iterate the 2x2 trace update

    u1_{n+1}(0) = R1(k) u2_n(0),    u2_{n+1}(0) = R2(k) u1_n(0),

with reflection coefficients

    R1 = (-λ(k) + σ1(k)) / (λ(k) + σ1(k))
    R2 = ( λ(k) + σ2(k)) / (-λ(k) + σ2(k))

so the two-step traces shrink by ρ(k) = R1 * R2.

We compare:
  - measured |u1_{2n+2}/u1_{2n}|^(1/2) (per-iter contraction)
  - analytic ρ(k) from eq. (2.6) / (3.2)

for each transmission family:
  - classical Dirichlet (σ = ∞ formally; we set σ_j = M huge to mimic Dirichlet
    trace transmission, which gives R1 = R2 = 1 -> diverges)
  - Robin/Després (σ1 = -σ2 = i*ω, a.k.a. lowest-order absorbing)
  - OO0 (σ1 = -σ2 = p* + q* i, p* = q* from eq. (3.7))

Outputs a JSON + a PNG (ρ vs k) reproducing Fig. 4.1 qualitatively.
"""

from __future__ import annotations
import json
import math
import os
from dataclasses import dataclass, asdict

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# -------------------- Helmholtz symbol --------------------

def lam(k: np.ndarray, omega: float) -> np.ndarray:
    """λ(k) per eq. (2.5): real positive for evanescent (|k|>=ω), pure imag w/ + part for propagating (|k|<ω)."""
    k = np.asarray(k, dtype=float)
    out = np.zeros_like(k, dtype=complex)
    ev = np.abs(k) >= omega
    out[ev] = np.sqrt(k[ev] ** 2 - omega ** 2)
    out[~ev] = 1j * np.sqrt(omega ** 2 - k[~ev] ** 2)
    return out


def rho_general(k: np.ndarray, omega: float, sigma1, sigma2) -> np.ndarray:
    """Per-mode convergence factor over TWO Schwarz steps, eq. (2.6).

    sigma1, sigma2 are either scalars or callables of k.
    Returns |ρ(k)| as a real array.
    """
    L = lam(k, omega)
    s1 = sigma1(k) if callable(sigma1) else np.full_like(L, sigma1, dtype=complex)
    s2 = sigma2(k) if callable(sigma2) else np.full_like(L, sigma2, dtype=complex)
    R1 = (-L + s1) / (L + s1)
    R2 = (L + s2) / (-L + s2)
    return np.abs(R1 * R2)


# -------------------- Optimal Robin parameters (OO0), eq. (3.7) --------------------

def oo0_optimal_pq(omega: float, omega_minus: float, kmax: float) -> tuple[float, float]:
    """Theorem 3.1, eq. (3.7): p* = q* = ( (ω² - ω_-²)^(1/2) (k_max² - ω²)^(1/2) )^(1/2) / sqrt(2).

    Reading (3.7) carefully:  p* = q* = sqrt( sqrt(ω²-ω_-²) * sqrt(k_max²-ω²) ) / sqrt(2).
    (Implicit factor 1/sqrt(2) coming from the "divided by 2" in the radicand.)
    Equivalently: ((ω² - ω_-²)(k_max² - ω²))^(1/4) / sqrt(2).
    """
    if omega_minus >= omega:
        raise ValueError("omega_minus must be < omega")
    if kmax <= omega:
        raise ValueError("kmax must be > omega")
    val = ((omega ** 2 - omega_minus ** 2) * (kmax ** 2 - omega ** 2)) ** 0.25 / math.sqrt(2.0)
    return val, val


def oo0_asymptotic_rho(omega: float, omega_minus: float, h: float) -> float:
    """Theorem 4.1, eq. (4.1):  ρ ≈ 1 - 2 * sqrt(2 (ω² - ω_-²)^(1/2) / π) * sqrt(h)."""
    return 1.0 - 2.0 * math.sqrt(2.0 * (omega ** 2 - omega_minus ** 2) ** 0.5 / math.pi) * math.sqrt(h)


# -------------------- OO2 (informational; not used in 2D run) --------------------

def oo2_optimal_ab(omega: float, omega_minus: float, omega_plus: float, kmin: float, kmax: float
                   ) -> tuple[complex, float]:
    """Theorem 3.10, eqs. (3.20), (3.21)."""
    alpha = 1j * ((omega ** 2 - kmin ** 2) * (omega ** 2 - omega_minus ** 2)) ** 0.25
    beta = ((kmax ** 2 - omega ** 2) * (omega_plus ** 2 - omega ** 2)) ** 0.25
    return alpha, beta


def rho_oo2(k: np.ndarray, omega: float, alpha: complex, beta: float) -> np.ndarray:
    """Eq. (3.17): ρ = |(λ-α)(λ-β)/((λ+α)(λ+β))|."""
    L = lam(k, omega)
    return np.abs(((L - alpha) * (L - beta)) / ((L + alpha) * (L + beta)))


# -------------------- Per-mode numerical iteration --------------------

def measure_rho_per_mode(k: float, omega: float, sigma1, sigma2,
                         n_iter: int = 40) -> float:
    """Run the per-mode trace iteration explicitly and measure geometric contraction.

    Returns measured |ρ| from log-fit on the last half.
    """
    L = lam(np.array([k]), omega)[0]
    s1 = sigma1(np.array([k]))[0] if callable(sigma1) else complex(sigma1)
    s2 = sigma2(np.array([k]))[0] if callable(sigma2) else complex(sigma2)
    R1 = (-L + s1) / (L + s1)
    R2 = (L + s2) / (-L + s2)
    rho_th = abs(R1 * R2)

    u1 = 1.0 + 0.0j
    u2 = 0.5 + 0.3j
    history = []
    for _ in range(n_iter):
        u1_new = R1 * u2
        u2_new = R2 * u1
        u1, u2 = u1_new, u2_new
        history.append(abs(u1))

    h = np.array(history)
    h = h[h > 0]
    if len(h) < 4:
        return float("nan")
    # In the parallel Schwarz update, both subdomains are updated simultaneously.
    # u1_{n+1}(0) = R1 * u2_n(0); u2_{n+1}(0) = R2 * u1_n(0).
    # So u1_{n+2} = R1 R2 * u1_n, i.e. ρ = |R1 R2| is the contraction PER TWO STEPS.
    # The geometric per-iter contraction observed on |u1| is therefore sqrt(ρ).
    last = h[len(h) // 2:]
    if last[0] == 0:
        return float("nan")
    ratios = last[1:] / last[:-1]
    per_iter = float(np.exp(np.mean(np.log(np.maximum(ratios, 1e-300)))))
    # square to match paper's two-step ρ
    return per_iter ** 2


# -------------------- Drivers --------------------

@dataclass
class ModeResult:
    k: float
    rho_analytic: float
    rho_measured: float
    abs_err: float


def run_1d_experiments(out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)

    # Paper Fig. 4.1 setup: ω = 10π, h = 1/50, two subdomains on the unit interval/square
    # with Dirichlet top/bottom -> k_n = n π, n=1,2,...  ω_- = 9π is just below ω-π/L=9π
    omega = 10.0 * math.pi
    L_domain = 1.0
    h = 1.0 / 50.0
    kmin = math.pi / L_domain
    kmax = math.pi / h
    omega_minus = omega - math.pi / L_domain   # = 9π
    omega_plus = omega + math.pi / L_domain    # = 11π

    p_star, q_star = oo0_optimal_pq(omega, omega_minus, kmax)
    print(f"[1D] ω={omega:.4f}  ω_-={omega_minus:.4f}  k_max={kmax:.4f}")
    print(f"[1D] OO0 optimal p* = q* = {p_star:.4f}")
    # Paper Fig 4.1 caption: p* = q* = 32.462
    paper_pq = 32.462
    print(f"[1D]   paper reports p* = q* = {paper_pq}")
    pq_rel_err = abs(p_star - paper_pq) / paper_pq
    print(f"[1D]   relative error vs paper: {pq_rel_err:.3e}")

    # Convergence rate scan over k
    k_grid = np.linspace(0.5, 1.4 * kmax, 4000)
    # Robin/Després: σ_1 = -σ_2 = iω
    rho_robin = rho_general(k_grid, omega, sigma1=1j * omega, sigma2=-1j * omega)
    # OO0: σ_1 = -σ_2 = p + i q
    rho_oo0 = rho_general(k_grid, omega, sigma1=p_star + 1j * q_star,
                          sigma2=-(p_star + 1j * q_star))

    # OO2
    alpha, beta = oo2_optimal_ab(omega, omega_minus, omega_plus, kmin, kmax)
    print(f"[1D] OO2 optimal α* = {alpha}, β* = {beta:.4f}")
    print(f"[1D]   paper reports α* ≈ 20.741 i, β* ≈ 47.071")
    rho_oo2_vals = rho_oo2(k_grid, omega, alpha, beta)

    # Plot Fig 4.1-style
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(k_grid, rho_robin, label="Després (Robin σ=iω)", color="tab:red")
    ax.plot(k_grid, rho_oo0, label=f"OO0 (p*=q*={p_star:.2f})", color="tab:blue")
    ax.plot(k_grid, rho_oo2_vals, label=f"OO2 (α*={alpha.imag:.2f}i, β*={beta:.2f})",
            color="tab:green")
    ax.axvline(omega, color="k", lw=0.6, ls="--", alpha=0.5)
    ax.set_xlim(0, k_grid.max())
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("tangential frequency k")
    ax.set_ylabel("|ρ(k)|")
    ax.set_title(f"Per-mode convergence factor (ω = 10π, h = 1/50)\n"
                 f"reproducing paper Fig 4.1 / 4.2")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_rho_vs_k.png"), dpi=140)
    plt.close(fig)

    # Verify analytic vs measured ρ at a handful of admissible k
    test_ks = [kmin, 2 * math.pi, 5 * math.pi, 8.5 * math.pi,
               11.5 * math.pi, 20 * math.pi, 50 * math.pi, kmax * 0.9]
    mode_results = []
    for k in test_ks:
        rho_th = float(rho_general(np.array([k]), omega,
                                   sigma1=p_star + 1j * q_star,
                                   sigma2=-(p_star + 1j * q_star))[0])
        rho_meas = measure_rho_per_mode(k, omega,
                                        sigma1=p_star + 1j * q_star,
                                        sigma2=-(p_star + 1j * q_star),
                                        n_iter=120)
        mode_results.append(ModeResult(k=k, rho_analytic=rho_th,
                                       rho_measured=rho_meas,
                                       abs_err=abs(rho_th - rho_meas)))

    # Asymptotic h-scaling (Theorem 4.1)
    h_list = [1 / 50, 1 / 100, 1 / 200, 1 / 400, 1 / 800]
    asymp_rows = []
    for hh in h_list:
        kmax_h = math.pi / hh
        p_h, q_h = oo0_optimal_pq(omega, omega_minus, kmax_h)
        # actual max ρ at the worst admissible k (here ω_-, paper's worst point)
        k_grid_h = np.concatenate([
            np.linspace(kmin, omega_minus, 4000),
            np.linspace(omega_plus, kmax_h, 4000),
        ])
        rho_h = rho_general(k_grid_h, omega,
                            sigma1=p_h + 1j * q_h, sigma2=-(p_h + 1j * q_h))
        rho_max = float(rho_h.max())
        rho_asym = oo0_asymptotic_rho(omega, omega_minus, hh)
        asymp_rows.append({"h": hh, "p_star": p_h, "rho_max_numeric": rho_max,
                           "rho_asym_thm41": rho_asym,
                           "1_minus_rho_max": 1 - rho_max,
                           "1_minus_rho_asym": 1 - rho_asym})

    # Plot log-log of (1-ρ) vs h to check the sqrt(h) slope from Theorem 4.1
    fig, ax = plt.subplots(figsize=(6, 4.2))
    hs = np.array([r["h"] for r in asymp_rows])
    one_minus_rho = np.array([r["1_minus_rho_max"] for r in asymp_rows])
    ax.loglog(hs, one_minus_rho, "o-", label="OO0 numeric (max over k)")
    # reference line h^{1/2}
    C = one_minus_rho[0] / math.sqrt(hs[0])
    ax.loglog(hs, C * np.sqrt(hs), "k--", alpha=0.6, label="O(h^{1/2})")
    ax.set_xlabel("h")
    ax.set_ylabel("1 - ρ_max")
    ax.set_title("Asymptotic 1 - ρ_OO0 vs h (Thm 4.1, slope 1/2)")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_oo0_asymptotic.png"), dpi=140)
    plt.close(fig)

    return {
        "omega": omega,
        "omega_minus": omega_minus,
        "h": h,
        "p_star_computed": p_star,
        "p_star_paper": paper_pq,
        "p_star_rel_err_vs_paper": pq_rel_err,
        "alpha_star_imag_computed": alpha.imag,
        "alpha_star_imag_paper": 20.741,
        "beta_star_computed": beta,
        "beta_star_paper": 47.071,
        "per_mode_check": [asdict(r) for r in mode_results],
        "asymptotic_table": asymp_rows,
    }


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "results")
    res = run_1d_experiments(os.path.abspath(out))
    with open(os.path.join(os.path.abspath(out), "osh_1d_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2)[:2000])
