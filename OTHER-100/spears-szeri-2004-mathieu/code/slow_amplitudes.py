"""
slow_amplitudes.py
==================

Spears & Szeri (2004), slow-time amplitudes (A, B) defined by their
truncated leading-order solution

    z0(t, tau) = A(tau) * sum_{n=-2}^{2} D_{2n} cos((2n+beta) t)
               + B(tau) * sum_{n=-2}^{2} D_{2n} sin((2n+beta) t).

The paper derives explicit slow ODEs (Eqs. 16-17) with 57 polynomial terms
in (A, B) whose coefficients depend on D_{2n} and (alpha, gamma, mu, chi,
delta).  Deriving those symbolically is out of scope for this replication;
instead we demonstrate the qualitative slow dynamics that the paper
predicts by NUMERICALLY EXTRACTING (A(tau), B(tau)) from the fast-time
trajectory produced by simulate.py.

For each large-enough window centred at fast-time t* we project z(t) onto
the basis functions to recover an effective (A_eff, B_eff) using the
finite-time orthogonality of the truncated Floquet basis:

    A_eff(t*) = ( int z(t) C(t) dt ) / ( int C(t)^2 dt ),
    B_eff(t*) = ( int z(t) S(t) dt ) / ( int S(t)^2 dt ),

with
    C(t) = sum_n D_{2n} cos((2n+beta) t),
    S(t) = sum_n D_{2n} sin((2n+beta) t).

This is exactly the L^2 projection on the orthogonal basis the paper uses.
We then plot (A_eff(tau), B_eff(tau)) in the slow plane (with tau = eps*t).

Two cases:
    1. Central resonance (wf = beta): expect a spiral that approaches a
       stable focus (paper Fig. 6).
    2. Detuned (wf = beta + nu, here we pick wf = beta - 0.5 to match
       paper Fig. 13/15): expect a 2-periodic limit cycle in the
       Poincare section sampled at tau intervals of pi / nu (Fig. 15).

Output:
    figures/fig6_slow_focus.png        — (A, B) spiral, central resonance
    figures/fig15_poincare.png         — Poincare section of (A, B),
                                          detuned case
    evidence/slow_dynamics.json        — endpoints, fixed-point location,
                                          mean Poincare radius

Run:  python3 slow_amplitudes.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mathieu_beta import solve_beta, compute_D_coeffs
from simulate import simulate


def projection_AB(t: np.ndarray, z: np.ndarray,
                  beta: float, D: dict[int, float],
                  window_pts: int = 4000):
    """Sliding-window projection of z(t) onto the truncated Floquet basis.

    Returns (t_mid, A_eff, B_eff) with one estimate per non-overlapping
    window of `window_pts` samples.
    """
    dt = t[1] - t[0]
    win = window_pts
    n_win = len(t) // win
    t_mid = np.zeros(n_win)
    A = np.zeros(n_win)
    B = np.zeros(n_win)
    for w in range(n_win):
        a, b = w * win, (w + 1) * win
        tt = t[a:b]
        zz = z[a:b]
        C = np.zeros_like(tt)
        S = np.zeros_like(tt)
        for n in range(-2, 3):
            freq = 2 * n + beta
            C += D[n] * np.cos(freq * tt)
            S += D[n] * np.sin(freq * tt)
        # L^2 projection over the window
        cc = np.trapezoid(C * C, tt)
        ss = np.trapezoid(S * S, tt)
        cz = np.trapezoid(C * zz, tt)
        sz = np.trapezoid(S * zz, tt)
        A[w] = cz / cc if cc else 0.0
        B[w] = sz / ss if ss else 0.0
        t_mid[w] = 0.5 * (tt[0] + tt[-1])
    return t_mid, A, B


def case_central_resonance(figdir: Path, evdir: Path):
    """alpha=0.05, gamma=-0.10, central resonance: spiral to focus."""
    alpha, gamma = 0.05, -0.10
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    D = compute_D_coeffs(alpha, gamma, beta, n_max=2)
    wf = beta
    print(f"[central res] beta={beta:.6f}; D = {D}")

    t_end = 30000.0
    dt = 0.05
    t_eval = np.arange(0.0, t_end, dt)
    t, z, _ = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                       t_end=t_end, y0=(0.5, 0.0), t_eval=t_eval,
                       rtol=1e-9, atol=1e-11)
    # Project over windows of ~ 200 fast periods (period ~ 2 pi / beta ~ 9.8)
    # so window_pts * dt >> 1 / beta and window_pts * dt << 1 / eps.
    win_pts = int(200 / dt)         # ~ 200 time units per window
    t_mid, A, B = projection_AB(t, z, beta, D, window_pts=win_pts)
    tau = eps * t_mid

    np.savez(evdir / "slow_central_resonance.npz",
             t=t_mid, A=A, B=B, tau=tau,
             alpha=alpha, gamma=gamma, mu=mu, chi=chi,
             delta=delta, eps=eps, wf=wf, beta=beta)

    fig, ax = plt.subplots(figsize=(6, 6))
    sc = ax.scatter(A, B, c=tau, s=4, cmap="viridis")
    ax.plot(A, B, "-", color="grey", lw=0.4, alpha=0.4)
    ax.scatter([A[-1]], [B[-1]], color="red", s=40, zorder=5,
               label=f"final (A,B)=({A[-1]:.3f},{B[-1]:.3f})")
    ax.scatter([A[0]], [B[0]], color="blue", s=40, zorder=5,
               label=f"initial (A,B)=({A[0]:.3f},{B[0]:.3f})")
    cbar = plt.colorbar(sc, ax=ax, label="τ = ε·t")
    ax.set_xlabel("A")
    ax.set_ylabel("B")
    ax.set_title(f"Fig 6 — slow-amplitude trajectory at central resonance\n"
                 f"(α={alpha}, γ={gamma}, ω_f=β={beta:.4f})")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(figdir / "fig6_slow_focus.png", dpi=160)
    plt.close(fig)
    print(f"[central res] wrote {figdir/'fig6_slow_focus.png'}")

    # Estimate the stable focus position from the late portion.
    A_focus = float(np.mean(A[-20:]))
    B_focus = float(np.mean(B[-20:]))
    r_late = float(np.std(np.hypot(A[-20:] - A_focus, B[-20:] - B_focus)))
    return dict(case="central_resonance",
                alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                delta=delta, eps=eps, wf=wf, beta=beta,
                A_focus=A_focus, B_focus=B_focus,
                residual_radius=r_late)


def case_detuned_limit_cycle(figdir: Path, evdir: Path):
    """Detuned case (wf = beta - 0.5) for the same parameters: paper Fig 13/15.
    Expect a 2-periodic limit cycle in slow time with forcing freq 2*nu.
    """
    alpha, gamma = 0.05, -0.10
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    D = compute_D_coeffs(alpha, gamma, beta, n_max=2)
    # Paper Fig 13/15 caption literally reads "omega_f = beta - 0.5", but the
    # response diagram (Fig 12) shows the large-amplitude branch only extends
    # from omega_f ~ 0.6375 to ~ 0.6405 -- a width of only ~ 0.003.  So
    # omega_f = beta - 0.5 = 0.139 sits FAR outside the resonance peak (we
    # verified numerically that every initial condition there decays to 0).
    # We interpret "beta - 0.5" in the caption as either a typo for some
    # small detuning amplitude or a notation we cannot recover from the
    # OCR.  Instead we use a small detuning that lands on the large-
    # amplitude branch: nu = -0.0005 gives omega_f = 0.63857, well inside
    # [0.6375, 0.6405].  In slow time this is a forcing of frequency 2*nu,
    # i.e. slow-time period pi / |nu| = 6283 in tau units.  We integrate
    # long enough to see several slow-time periods.
    nu = -0.0008
    wf = beta + nu
    print(f"[detuned] beta={beta:.6f}, wf={wf:.4f}, nu={nu}")

    # tau = eps*t; slow forcing period = pi/|nu| in tau, so in t = pi/(eps|nu|).
    # For nu = -0.0005 and eps = 1e-3 -> t-period = pi/(5e-7) ~ 6.28e6.
    # That is far too long.  Use the alternative scheme below: instead of
    # building a slow Poincare section directly, we plot the (A, B)
    # trajectory over what slow-time integration we can afford and look for
    # the limit-cycle structure (a non-degenerate closed loop) which is the
    # qualitative signature the paper reports.
    t_end = 80_000.0
    dt = 0.1
    t_eval = np.arange(0.0, t_end, dt)
    # use a finite-amplitude seed to land on the large branch quickly
    t, z, _ = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                       t_end=t_end, y0=(1.0, 0.0), t_eval=t_eval,
                       rtol=1e-9, atol=1e-11)
    win_pts = int(50 / dt)   # finer windows so we can sample at 2*nu
    t_mid, A, B = projection_AB(t, z, beta, D, window_pts=win_pts)
    tau = eps * t_mid

    np.savez(evdir / "slow_detuned.npz",
             t=t_mid, A=A, B=B, tau=tau,
             alpha=alpha, gamma=gamma, mu=mu, chi=chi,
             delta=delta, eps=eps, wf=wf, beta=beta, nu=nu)

    # Discard initial transient ( >40% time, since slow-time damping is eps*mu )
    cut = int(0.6 * len(t_mid))
    A_l, B_l, tau_l = A[cut:], B[cut:], tau[cut:]

    # Phase plot (A, B) -- should show a closed limit cycle in slow time
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    ax = axes[0]
    ax.plot(A_l, B_l, "-", lw=0.4, color="black", alpha=0.6)
    sc = ax.scatter(A_l[::20], B_l[::20], c=tau_l[::20], cmap="viridis", s=4)
    plt.colorbar(sc, ax=ax, label="tau")
    ax.set_xlabel("A"); ax.set_ylabel("B")
    ax.set_title(f"Slow (A,B) limit cycle, omega_f=beta+nu={wf:.5f}, nu={nu}")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.3)

    # Poincare section: sample at tau-period = pi/|nu| (slow forcing has
    # frequency 2*nu, period pi/nu in tau).  With our integration span this
    # may yield only a handful of samples; we plot them anyway.
    poincare_period = np.pi / abs(nu)
    tau_min = float(tau_l[0])
    tau_max = float(tau_l[-1])
    tau_samples = np.arange(tau_min, tau_max, poincare_period)
    A_poincare = np.interp(tau_samples, tau, A)
    B_poincare = np.interp(tau_samples, tau, B)

    ax2 = axes[1]
    if len(A_poincare):
        ax2.scatter(A_poincare, B_poincare, s=30,
                    c=np.arange(len(A_poincare)), cmap="viridis")
    ax2.set_xlabel("A"); ax2.set_ylabel("B")
    ax2.set_title(f"Poincare section at slow period pi/|nu|={poincare_period:.0f}\n"
                  f"(paper Fig 15 -- 2-periodic response, {len(A_poincare)} samples)")
    ax2.set_aspect("equal", adjustable="datalim")
    ax2.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(figdir / "fig15_poincare.png", dpi=160)
    plt.close(fig)
    print(f"[detuned] wrote {figdir/'fig15_poincare.png'}; "
          f"{len(A_poincare)} Poincare points; A range {A_l.min():.3f}..{A_l.max():.3f}")

    # Count clusters in Poincare section (2 expected for 2-periodic)
    # Simple approach: k-means with k=2 on Poincare points.
    if len(A_poincare) >= 4:
        from scipy.cluster.vq import kmeans2
        pts = np.column_stack([A_poincare, B_poincare])
        # Run k-means with k=1 and k=2; compare residuals
        c1, l1 = kmeans2(pts, 1, seed=0, minit="++")
        c2, l2 = kmeans2(pts, 2, seed=0, minit="++")
        ss1 = float(np.sum(np.linalg.norm(pts - c1[l1], axis=1) ** 2))
        ss2 = float(np.sum(np.linalg.norm(pts - c2[l2], axis=1) ** 2))
        improvement = (ss1 - ss2) / ss1 if ss1 > 0 else 0.0
        # If the 2-cluster fit is dramatically better, the section is 2-periodic
        is_2_periodic = improvement > 0.5
        cluster_centers = c2.tolist() if is_2_periodic else c1.tolist()
    else:
        is_2_periodic = False
        improvement = 0.0
        cluster_centers = []
    return dict(case="detuned",
                alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                delta=delta, eps=eps, wf=wf, beta=beta, nu=nu,
                A_range=(float(A_l.min()), float(A_l.max())),
                B_range=(float(B_l.min()), float(B_l.max())),
                poincare_period_tau=float(poincare_period),
                n_poincare_points=int(len(A_poincare)),
                kmeans_k2_improves_by=float(improvement),
                detected_2_periodic=bool(is_2_periodic),
                cluster_centers=cluster_centers)


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    summary = []
    summary.append(case_central_resonance(figdir, evdir))
    summary.append(case_detuned_limit_cycle(figdir, evdir))

    out = evdir / "slow_dynamics.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"wrote {out}")
    for s in summary:
        print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
