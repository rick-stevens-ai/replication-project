"""
detuned_poincare.py
====================

Spears & Szeri (2004), Sec. 3.2 (Figs. 13, 15).  At detuning wf = beta + nu
(nu small), the secondary-forcing carrier becomes

    cos(2 wf t̂) = cos(2 beta t̂) cos(2 nu t̂) - sin(2 beta t̂) sin(2 nu t̂).

Since nu is O(eps), the slow-time forcing frequency is

    Omega_slow := 2 nu / eps         (i.e. cos(Omega_slow * tau))

so the slow ODEs become non-autonomous with forcing period

    T_slow := pi / |nu / eps| = pi * eps / |nu|  (in tau units).

For nu = -0.0008, eps = 1e-3 we get T_slow = pi / 0.8 ~ 3.927 in tau.
That is a factor ~ 1000 cheaper than integrating the fast system to
t ~ 4e7 to see one full Poincare period.

This script:

  1. Re-derives the secularity equations symbolically with the detuning
     carrier  cos(2 wf t̂)  rewritten via the angle-addition formula and
     a slow-time argument theta(tau) = 2 (nu/eps) tau.  The symbolic
     `cos(2 nu t̂)` and `sin(2 nu t̂)` are introduced as free symbols
     `Ct` and `St` so the secularity equations stay linear in (A', B').
  2. Yields slow ODEs of the form
        A'(tau) = ...    + (delta/beta) [Ct B + St A] * D_0 ratio terms ...
        B'(tau) = ...    + (delta/beta) [Ct A - St B] * D_0 ratio terms ...
     (The full expression is computed and saved.)
  3. Integrates the DERIVED slow ODE in tau for >= 10 slow periods,
     strobing at tau = k * T_slow / 2  (we sample twice per slow period
     to make 2-periodicity visible) to build the slow Poincare section.
  4. Counts the discrete points in the section's long-time recurrence;
     if the limit cycle has period 2 T_slow (paper Fig. 15) the strobed
     samples should bounce between two well-separated clusters.

Run:  python3 detuned_poincare.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from mathieu_beta import solve_beta, compute_D_coeffs
from derive_slow_odes import (
    FourierSignal,
    build_z0,
    build_one_plus_cos2t,
)


def derive_detuned_equations():
    """Build (A', B') ODEs with detuning carrier cos(2 wf t̂) where
    wf = beta + nu.  We treat the slow-time factors
        Ct := cos(2 nu t̂) == cos(Omega_slow tau)
        St := sin(2 nu t̂) == sin(Omega_slow tau)
    as free symbols held constant across one secular-removal step.

    The carrier is then
        cos(2 wf t̂) = cos(2 beta t̂) * Ct - sin(2 beta t̂) * St,
    which is a FourierSignal mixed with the (Ct, St) symbols.
    """
    A, B = sp.symbols('A B', real=True)
    Ap, Bp = sp.symbols("A' B'", real=True)
    mu, chi, delta = sp.symbols('mu chi delta', real=True)
    alpha = sp.Symbol('alpha', real=True)
    gamma = sp.Symbol('gamma', real=True)
    beta_sym = sp.Symbol('beta', positive=True)
    Ct = sp.Symbol('Ct', real=True)
    St = sp.Symbol('St', real=True)
    D = {n: sp.Symbol(f"D_{2*n}", real=True) for n in range(-2, 3)}

    z0 = build_z0(D, A, B)
    z0_t = z0.diff_that()
    z0_tau = build_z0(D, Ap, Bp)
    z0_tau_t = z0_tau.diff_that()

    # Secondary forcing carrier 4 delta cos(2 wf t̂)
    # = 4 delta * [Ct cos(2 beta t̂) - St sin(2 beta t̂)]
    carrier = FourierSignal()
    carrier.add('C', 0, 2, Ct)
    carrier.add('S', 0, 2, -St)  # note the leading minus, then sin flip if any
    # In build of secondary forcing, multiply carrier * z0
    tmp = carrier.mul(z0)
    sec_force = FourierSignal()
    for k, v in tmp.terms.items():
        sec_force.add(k[0], k[1][0], k[1][1], 4*delta * v)

    # Cubic term -4 chi (gamma + alpha cos 2 t̂) z0^3
    one_plus = build_one_plus_cos2t()
    z0_sq = z0.mul(z0).simplify()
    z0_cu = z0_sq.mul(z0).simplify()
    cub = one_plus.mul(z0_cu).simplify()
    cubic_term = FourierSignal()
    for k, v in cub.terms.items():
        cubic_term.add(k[0], k[1][0], k[1][1], -4*chi * v)

    damp = FourierSignal()
    for k, v in z0_t.terms.items():
        damp.add(k[0], k[1][0], k[1][1], -mu * v)
    cross = FourierSignal()
    for k, v in z0_tau_t.terms.items():
        cross.add(k[0], k[1][0], k[1][1], -2 * v)

    rhs = FourierSignal()
    rhs.add_signal(sec_force)
    rhs.add_signal(cubic_term)
    rhs.add_signal(damp)
    rhs.add_signal(cross)
    rhs.simplify()

    key_cos_beta = ('C', (sp.Integer(0), sp.Integer(1)))
    key_sin_beta = ('S', (sp.Integer(0), sp.Integer(1)))
    coeff_cos = rhs.terms.get(key_cos_beta, sp.Integer(0))
    coeff_sin = rhs.terms.get(key_sin_beta, sp.Integer(0))

    sol = sp.solve([coeff_cos, coeff_sin], [Ap, Bp], dict=True)
    if not sol:
        raise RuntimeError("Failed to solve detuned secular equations.")
    A_dot = sp.expand(sol[0][Ap])
    B_dot = sp.expand(sol[0][Bp])

    return {
        'A_dot': A_dot,
        'B_dot': B_dot,
        'symbols': dict(A=A, B=B, Ap=Ap, Bp=Bp,
                        mu=mu, chi=chi, delta=delta,
                        alpha=alpha, gamma=gamma, beta=beta_sym,
                        Ct=Ct, St=St, D=D),
    }


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir  = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    alpha = 0.05
    gamma = -0.10
    mu = chi = delta = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    D_dict = compute_D_coeffs(alpha, gamma, beta, n_max=2)
    D_numeric = {n: float(D_dict[n]) for n in range(-2, 3)}

    # Choose detuning inside the resonance window [0.6375, 0.6405] from Fig 12.
    # Brief asks for wf in [0.6375, 0.6405].   For the Fig 4-6 parameters,
    # beta ~ 0.63907.   nu = -0.0008 => wf = 0.63827, just below the window.
    # nu = +0.0005 -> wf = 0.63957, just above.   nu = +0.001 -> wf = 0.64007.
    # The brief's example uses wf in [0.6375, 0.6405] for the Fig.12 params
    # (Fig 12 itself is at the same alpha/gamma).  We use nu = -0.00057
    # ->  wf ~ 0.63850 inside the window.   Slow-time forcing freq
    # = 2 nu / eps = -1.14 rad/tau ; slow period pi / 0.57 ~ 5.51 tau-units.
    nu = -0.00057
    wf = beta + nu
    Omega_slow = 2.0 * nu / eps      # slow-time angular freq of forcing
    T_slow = np.pi / abs(Omega_slow / 2.0)  # FORCING period = pi/|nu/eps|
    print(f"beta = {beta:.6f}")
    print(f"nu   = {nu:+.6f}    wf = {wf:.6f}  (window [0.6375, 0.6405])")
    print(f"slow-time forcing freq Omega_slow = 2nu/eps = {Omega_slow:.4f} rad/tau")
    print(f"slow-time forcing period T_slow   = {T_slow:.4f} tau")

    print("\nDeriving detuned secular-removal equations symbolically...")
    eqs = derive_detuned_equations()
    A_dot = eqs['A_dot']
    B_dot = eqs['B_dot']
    print(f"  Symbolic A' has {len(A_dot.args) if hasattr(A_dot,'args') else 1} additive terms")
    print(f"  Symbolic B' has {len(B_dot.args) if hasattr(B_dot,'args') else 1} additive terms")

    # Substitute the numeric parameters and D's, but leave Ct, St symbolic.
    sub = {
        eqs['symbols']['alpha']: alpha,
        eqs['symbols']['gamma']: gamma,
        eqs['symbols']['mu']:    mu,
        eqs['symbols']['chi']:   chi,
        eqs['symbols']['delta']: delta,
        eqs['symbols']['beta']:  beta,
    }
    for n, sym in eqs['symbols']['D'].items():
        sub[sym] = D_numeric[n]

    A_dot_num = sp.simplify(A_dot.subs(sub))
    B_dot_num = sp.simplify(B_dot.subs(sub))
    A_sym = eqs['symbols']['A']; B_sym = eqs['symbols']['B']
    Ct_sym = eqs['symbols']['Ct']; St_sym = eqs['symbols']['St']
    f_A = sp.lambdify((A_sym, B_sym, Ct_sym, St_sym), A_dot_num, modules='numpy')
    f_B = sp.lambdify((A_sym, B_sym, Ct_sym, St_sym), B_dot_num, modules='numpy')

    def rhs(tau, y):
        Ct = np.cos(Omega_slow * tau)
        St = np.sin(Omega_slow * tau)
        return [float(f_A(y[0], y[1], Ct, St)),
                float(f_B(y[0], y[1], Ct, St))]

    # Initial condition consistent with simulate.py (z(0), z'(0)) = (1, 0)
    sumD = sum(D_numeric[n] for n in range(-2, 3))
    A0 = 1.0 / sumD
    B0 = 0.0
    print(f"\nInitial (A0, B0) = ({A0:.4f}, {B0:.4f})")

    # Integrate for many slow periods.   We need >= 10 periods of T_slow.
    n_periods = 60
    tau_end = n_periods * T_slow
    print(f"Integrating derived detuned slow ODE for {n_periods} slow periods => "
          f"tau_end = {tau_end:.2f}")

    # Sample at >= 5000 points across the run
    sol = solve_ivp(rhs, (0.0, tau_end), [A0, B0],
                    rtol=1e-10, atol=1e-12, method='Radau',
                    dense_output=True, max_step=T_slow / 50.0)
    print(f"  solver: success={sol.success}, status={sol.status}, n_eval={sol.nfev}")

    tau_arr = np.linspace(0, tau_end, 8001)
    yy = sol.sol(tau_arr)
    A_arr, B_arr = yy[0], yy[1]

    # Build slow Poincare section: strobe at tau = k * T_slow (one sample
    # per slow forcing period).  Drop the first ~30% as transient.
    n_skip = int(0.4 * n_periods)
    tau_strobe = np.array([k * T_slow for k in range(n_skip, n_periods + 1)])
    A_strobe = np.interp(tau_strobe, tau_arr, A_arr)
    B_strobe = np.interp(tau_strobe, tau_arr, B_arr)
    print(f"  Poincare section: {len(A_strobe)} samples "
          f"after transient ({n_skip} periods)")

    # Cluster count: try k = 1, 2, 4 and report which fits best (relative SSE drop).
    from scipy.cluster.vq import kmeans2
    pts = np.column_stack([A_strobe, B_strobe])
    sse = {}
    centers = {}
    for k in (1, 2, 4):
        if len(pts) < k:
            continue
        c, l = kmeans2(pts, k, seed=0, minit='++')
        ss = float(np.sum(np.linalg.norm(pts - c[l], axis=1) ** 2))
        sse[k] = ss
        centers[k] = c.tolist()
    print(f"  cluster SSE:  k=1 -> {sse.get(1, float('nan')):.3f}, "
          f"k=2 -> {sse.get(2, float('nan')):.3f}, "
          f"k=4 -> {sse.get(4, float('nan')):.3f}")
    if 1 in sse and 2 in sse:
        drop_1to2 = (sse[1] - sse[2]) / max(sse[1], 1e-12)
        drop_2to4 = (sse[2] - sse[4]) / max(sse[2], 1e-12) if 4 in sse else 0.0
        # Period-N: a true N-cluster orbit has SSE_N == 0 (point-collapse)
        # while SSE_{N-1} >> 0.  Period-2 criterion uses absolute SSE per
        # point against the inter-cluster distance.
        per_point_2 = (sse[2] / max(len(pts), 1)) ** 0.5
        if 2 in centers and len(centers[2]) == 2:
            cc = np.array(centers[2])
            cluster_separation = float(np.linalg.norm(cc[0] - cc[1]))
        else:
            cluster_separation = 0.0
        print(f"  k=1->2 SSE drop:    {drop_1to2*100:.2f}%")
        print(f"  k=2->4 SSE drop:    {drop_2to4*100:.2f}%")
        print(f"  per-point sigma_2:  {per_point_2:.2e}")
        print(f"  cluster separation: {cluster_separation:.4f}")
        # True period-2: per-point variance is << cluster separation
        is_period2 = (drop_1to2 > 0.99) and (per_point_2 < 0.01 * cluster_separation
                                            if cluster_separation > 0 else False)
    else:
        is_period2 = False
        drop_1to2 = drop_2to4 = 0.0
        per_point_2 = 0.0
        cluster_separation = 0.0

    # Save evidence
    np.savez(evdir / "detuned_poincare.npz",
             tau=tau_arr, A=A_arr, B=B_arr,
             tau_strobe=tau_strobe, A_strobe=A_strobe, B_strobe=B_strobe,
             beta=beta, nu=nu, wf=wf, Omega_slow=Omega_slow, T_slow=T_slow,
             alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta, eps=eps,
             cluster_centers_k2=np.array(centers.get(2, [])))
    print(f"  saved evidence/detuned_poincare.npz")

    # Plot trajectory + Poincare section
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    ax = axes[0]
    # color by tau
    sc = ax.scatter(A_arr[::4], B_arr[::4],
                    c=tau_arr[::4], s=2, cmap='viridis')
    ax.plot(A_arr, B_arr, '-', color='grey', lw=0.3, alpha=0.5)
    plt.colorbar(sc, ax=ax, label='tau')
    ax.set_xlabel('A'); ax.set_ylabel('B')
    ax.set_title(f"Slow (A,B) trajectory (derived ODE)\n"
                 f"wf = beta + nu = {wf:.5f}, T_slow = {T_slow:.3f} tau")
    ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.scatter(A_strobe, B_strobe, c=np.arange(len(A_strobe)),
                cmap='plasma', s=80, edgecolor='k', zorder=4)
    if 2 in centers:
        cc = np.array(centers[2])
        ax2.scatter(cc[:, 0], cc[:, 1], color='red', marker='X', s=200,
                    zorder=5, label='k-means k=2 centers')
    ax2.set_xlabel('A'); ax2.set_ylabel('B')
    if is_period2:
        title = ("Slow Poincare section -- PERIOD-2 detected\n"
                 f"({len(A_strobe)} samples, SSE drops k=1->2: {drop_1to2*100:.1f}%, "
                 f"k=2->4: {drop_2to4*100:.1f}%)")
    else:
        title = ("Slow Poincare section\n"
                 f"({len(A_strobe)} samples; period structure: see SSE drops)")
    ax2.set_title(title)
    ax2.set_aspect('equal', adjustable='datalim')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best', fontsize=8)
    fig.tight_layout()
    fig.savefig(figdir / "fig15_poincare_derived.png", dpi=160)
    plt.close(fig)
    print(f"  saved figures/fig15_poincare_derived.png")

    # JSON summary
    out = {
        "alpha": alpha, "gamma": gamma, "mu": mu, "chi": chi, "delta": delta,
        "eps": eps, "beta": beta, "nu": nu, "wf": wf,
        "Omega_slow_per_tau": Omega_slow, "T_slow_in_tau": T_slow,
        "tau_end": tau_end, "n_periods_integrated": n_periods,
        "n_poincare_samples": int(len(A_strobe)),
        "sse_by_k": {str(k): float(v) for k, v in sse.items()},
        "sse_drop_1to2_pct": float(drop_1to2 * 100),
        "sse_drop_2to4_pct": float(drop_2to4 * 100),
        "per_point_sigma_at_k2": float(per_point_2),
        "k2_cluster_separation": float(cluster_separation),
        "is_period_2": bool(is_period2),
        "k2_cluster_centers": centers.get(2, []),
        "method": "Derived symbolic slow ODE (sympy), integrated in tau "
                  "with Ct=cos(Omega_slow tau), St=sin(Omega_slow tau).",
    }
    (evdir / "detuned_poincare.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"  saved evidence/detuned_poincare.json")

    if is_period2:
        print("\n*** Period-2 Poincare orbit confirmed for the detuned slow ODE. ***")
    else:
        print("\n*** Poincare structure: see SSE drops above. ***")


if __name__ == "__main__":
    main()
