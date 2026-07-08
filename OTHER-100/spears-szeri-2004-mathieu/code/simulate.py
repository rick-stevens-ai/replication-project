"""
simulate.py
============

Direct numerical integration of Spears & Szeri (2004) Eq. (2), the RESCALED
form.  The OCR of Eq. (2) (tesseract on the original PDF) gives

    z'' + eps * mu * z' + 4 ( gamma + alpha cos(2 t)
                              - eps * delta * cos(2 wf t) ) * ( -z + eps * chi z^3 ) = 0,

with chi, delta, mu all O(1) and eps << 1.  This is the form that matches
the multiple-scales O(eps^1) equation (7) of the paper and that reproduces
the sustained large-amplitude attractor at central resonance shown in
their Fig. 1 / Fig. 5 (amplitude ~ 2-3, here ~ 2.8 for the Fig. 1
parameters).  The pdftotext-extracted OCR drops the explicit eps factors
and makes Eq. (2) look like
    z'' + mu z' + 4 ( gamma + alpha cos 2t - delta cos 2 wf t ) ( -z + chi z^3 ) = 0,
but that un-rescaled form does NOT reproduce the central-resonance
attractor with the figure parameters -- the basin of attraction of the
trivial z = 0 fixed point swallows every initial condition we tried.
We therefore use the rescaled form.

Reproduces the time-series figures:
    Fig. 1  — central resonance, sustained large-amplitude oscillation
              on a knotted torus (alpha=0.15, gamma=-0.05, wf=beta).
    Fig. 2  — secondary resonance p=2 (alpha=0.25, gamma=0.001,
              wf=2+beta, delta=10).
    Fig. 3  — off-resonance decay (alpha=0.15, gamma=-0.05, wf=2*beta).

A small initial perturbation away from z=0 is given so the trivial fixed
point is left.  We integrate with scipy.solve_ivp's RK45.

Output:
    figures/fig1_central_resonance.png
    figures/fig2_p2_resonance.png
    figures/fig3_off_resonance_decay.png
    evidence/fig1_timeseries.npz, fig2_..., fig3_...

Run:  python3 simulate.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from mathieu_beta import solve_beta


# ----------------------------------------------------------------------
# Right-hand side
# ----------------------------------------------------------------------

def rhs_factory(alpha: float, gamma: float, mu: float, chi: float,
                delta: float, eps: float, wf: float):
    """Return the time-dependent rhs f(t, y) for y = (z, z').

    Implements Eq. (2) of Spears & Szeri (2004) in its rescaled form,
    where the damping, secondary forcing, and cubic terms all carry
    explicit eps prefactors:

        z'' = - eps * mu * z'
              - 4 * ( gamma + alpha cos 2t - eps * delta cos 2 wf t )
                  * ( -z + eps * chi * z^3 ).
    """
    def rhs(t, y):
        z, zdot = y
        envelope = (gamma + alpha * np.cos(2.0 * t)
                    - eps * delta * np.cos(2.0 * wf * t))
        zddot = (- eps * mu * zdot
                 - 4.0 * envelope * (-z + eps * chi * z * z * z))
        return [zdot, zddot]
    return rhs


def simulate(alpha, gamma, mu, chi, delta, eps, wf,
             t_end, y0=(0.05, 0.0), t_eval=None,
             rtol=1e-8, atol=1e-10, max_step=None):
    rhs = rhs_factory(alpha, gamma, mu, chi, delta, eps, wf)
    kwargs = dict(rtol=rtol, atol=atol)
    if max_step is not None:
        kwargs["max_step"] = max_step
    sol = solve_ivp(rhs, [0.0, t_end], list(y0), method="RK45",
                    t_eval=t_eval, **kwargs)
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    return sol.t, sol.y[0], sol.y[1]


# ----------------------------------------------------------------------
# Plot helpers
# ----------------------------------------------------------------------

def plot_three_window(t, z, t_end, windows, title, savepath,
                      window_width=140.0):
    """Three side-by-side panels showing zoomed-in windows of z(t)."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    for ax, t0 in zip(axes, windows):
        m = (t >= t0) & (t <= t0 + window_width)
        ax.plot(t[m], z[m], lw=0.5, color="k")
        ax.set_xlabel("t")
        ax.set_ylabel("z")
        ax.set_title(f"t ∈ [{t0:.0f}, {t0+window_width:.0f}]")
        ax.grid(True, alpha=0.3)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(savepath, dpi=160)
    plt.close(fig)


def plot_full_envelope(t, z, title, savepath):
    """Single panel showing the full time series (good for decay/figure 3)."""
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.plot(t, z, lw=0.4, color="k")
    ax.set_xlabel("t")
    ax.set_ylabel("z(t)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(savepath, dpi=160)
    plt.close(fig)


# ----------------------------------------------------------------------
# Three fundamental cases
# ----------------------------------------------------------------------

def case_fig1(figdir: Path, evdir: Path):
    """Central resonance: alpha=0.15, gamma=-0.05, wf=beta."""
    alpha, gamma = 0.15, -0.05
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    wf = beta
    print(f"[Fig 1] beta = {beta:.6f}; wf = {wf:.6f}")

    t_end = 50_000.0
    # Sample densely enough to see fast 1/beta oscillation: dt ~ 0.05
    t_eval = np.arange(0.0, t_end, 0.1)
    t, z, zdot = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                          t_end=t_end, y0=(0.5, 0.0),
                          t_eval=t_eval, rtol=1e-9, atol=1e-11)

    np.savez_compressed(evdir / "fig1_timeseries.npz",
                        t=t.astype(np.float32),
                        z=z.astype(np.float32),
                        zdot=zdot.astype(np.float32),
                        alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                        delta=delta, eps=eps, wf=wf, beta=beta)
    print(f"[Fig 1] wrote {evdir/'fig1_timeseries.npz'}; final |z|={abs(z[-1]):.3f}")

    # Two views: long term & three zoomed windows
    plot_full_envelope(t, z,
        f"Fig 1 — central resonance (α=0.15, γ=-0.05, ω_f=β={beta:.4f})",
        figdir / "fig1_central_resonance_full.png")
    plot_three_window(t, z, t_end,
        windows=[40_000.0, 45_000.0, 49_700.0],
        window_width=140.0,
        title=f"Fig 1 — knotted-torus oscillation (α=0.15, γ=-0.05, ω_f=β={beta:.4f})",
        savepath=figdir / "fig1_central_resonance.png")

    return dict(case="Fig1", alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                delta=delta, eps=eps, wf=wf, beta=beta,
                final_amplitude=float(np.max(np.abs(z[-2000:]))),
                sustained=bool(np.max(np.abs(z[-2000:])) > 0.5))


def case_fig2(figdir: Path, evdir: Path):
    """p=2 resonance: alpha=0.25, gamma=0.001, wf = 2 + beta, delta=10."""
    alpha, gamma = 0.25, 0.001
    mu = 0.8
    delta = 10.0
    chi = 5.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    wf = 2.0 + beta
    print(f"[Fig 2] beta = {beta:.6f}; wf = {wf:.6f}")

    # This resonance is more delicate (paper says "easily destroyed by small
    # increases in damping"); also smaller amplitude. Need long-time run.
    t_end = 50_000.0
    t_eval = np.arange(0.0, t_end, 0.05)
    t, z, zdot = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                          t_end=t_end, y0=(0.3, 0.0),
                          t_eval=t_eval, rtol=1e-9, atol=1e-11)

    np.savez_compressed(evdir / "fig2_timeseries.npz",
                        t=t.astype(np.float32),
                        z=z.astype(np.float32),
                        zdot=zdot.astype(np.float32),
                        alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                        delta=delta, eps=eps, wf=wf, beta=beta)
    print(f"[Fig 2] wrote {evdir/'fig2_timeseries.npz'}; final |z|_max(last 2k)={np.max(np.abs(z[-2000:])):.4f}")

    plot_full_envelope(t, z,
        f"Fig 2 — p=2 resonance (α=0.25, γ=0.001, μ=0.8, δ=10, χ=5, ω_f=2+β={wf:.4f})",
        figdir / "fig2_p2_resonance_full.png")
    plot_three_window(t, z, t_end,
        windows=[40_000.0, 45_000.0, 49_500.0],
        window_width=140.0,
        title=f"Fig 2 — p=2 resonance (α=0.25, γ=0.001, ω_f=2+β={wf:.4f})",
        savepath=figdir / "fig2_p2_resonance.png")

    return dict(case="Fig2", alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                delta=delta, eps=eps, wf=wf, beta=beta,
                final_amplitude=float(np.max(np.abs(z[-2000:]))),
                sustained=bool(np.max(np.abs(z[-2000:])) > 0.01))


def case_fig3(figdir: Path, evdir: Path):
    """Off-resonance decay: alpha=0.15, gamma=-0.05, wf = 2*beta."""
    alpha, gamma = 0.15, -0.05
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    wf = 2.0 * beta
    print(f"[Fig 3] beta = {beta:.6f}; wf = {wf:.6f}")

    t_end = 10_000.0
    t_eval = np.arange(0.0, t_end, 0.05)
    t, z, zdot = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                          t_end=t_end, y0=(0.5, 0.0),
                          t_eval=t_eval, rtol=1e-9, atol=1e-11)

    np.savez_compressed(evdir / "fig3_timeseries.npz",
                        t=t.astype(np.float32),
                        z=z.astype(np.float32),
                        zdot=zdot.astype(np.float32),
                        alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                        delta=delta, eps=eps, wf=wf, beta=beta)
    final_amp = float(np.max(np.abs(z[-2000:])))
    print(f"[Fig 3] wrote {evdir/'fig3_timeseries.npz'}; final |z|_max(last 2k)={final_amp:.2e}")

    plot_full_envelope(t, z,
        f"Fig 3 — off-resonance decay (α=0.15, γ=-0.05, ω_f=2β={wf:.4f})",
        figdir / "fig3_off_resonance_decay.png")

    return dict(case="Fig3", alpha=alpha, gamma=gamma, mu=mu, chi=chi,
                delta=delta, eps=eps, wf=wf, beta=beta,
                final_amplitude=final_amp,
                # paper says solutions decay exponentially; eps*mu=1e-3 damping
                # rate gives ~exp(-eps mu t / 2) = exp(-5) ~ 7e-3 from z0=0.5
                # over t=10000, so threshold ~ 0.01 captures the decay regime.
                decayed=bool(final_amp < 0.01))


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    summary = []
    summary.append(case_fig1(figdir, evdir))
    summary.append(case_fig3(figdir, evdir))
    summary.append(case_fig2(figdir, evdir))

    summary_path = evdir / "simulate_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print()
    print(f"Summary written to {summary_path}")
    for s in summary:
        keys = [k for k in ("sustained", "decayed") if k in s]
        extras = "  ".join(f"{k}={s[k]}" for k in keys)
        print(f"  {s['case']}: wf={s['wf']:.4f} final_amp={s['final_amplitude']:.4f}  {extras}")


if __name__ == "__main__":
    main()
