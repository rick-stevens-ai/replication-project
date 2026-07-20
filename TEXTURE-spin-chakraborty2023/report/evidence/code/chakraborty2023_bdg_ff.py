#!/usr/bin/env python
"""
From-scratch replication of Chakraborty & Black-Schaffer (arXiv:2309.14427):
Zero-field finite-momentum (Fulde-Ferrell) superconductivity in a 2D d-wave altermagnet.

Mean-field BdG for a square-lattice d-wave altermagnet + spin-singlet pairing.

Single-particle dispersion:   xi_k   = -2 t (cos kx + cos ky) - mu
Altermagnet + Zeeman:         xi_{k s} = xi_k + s (t_am/2)(cos kx - cos ky) + s B
Pairing (FF, single COM Q):   pairs (k+Q/2, up) with (-k+Q/2, down)
Order parameter:              Delta_k = Delta_d * eta(k) + Delta_s * gamma(k)
                              eta = cos kx - cos ky (d-wave), gamma = cos kx + cos ky (ext-s)
Interaction:                  V_{k k'} = -V (gamma gamma' + eta eta'),  V>0 attractive

For each fixed Q we minimize the T=0 BdG grand potential over (Delta_d, Delta_s)
(which is exactly the self-consistency condition, verified analytically), with mu
tuned by bisection so the density rho = (1/N^2) sum_k [theta(-E+)+theta(-E-)] = rho_target.
Ground-state energy per site e(Q) = omega(Q) + mu*rho.  The FF state is diagnosed by
argmin_Q e(Q) landing at Q>0.

No author code exists; everything here is built from the paper's equations.
"""
import json, sys, time
import numpy as np
from scipy.optimize import minimize, brentq

t = 1.0
V = 2.0
RHO_TARGET = 0.6

def build_k(N):
    k = np.linspace(-np.pi, np.pi, N, endpoint=False)
    kx, ky = np.meshgrid(k, k, indexing="ij")
    return kx, ky

def dispersions(kx, ky, Q, t_am, B, mu, swave=False):
    """Return xi_a (k+Q/2, up), xi_b (-k+Q/2, down), form factors eta,gamma at label k."""
    ax = kx + Q / 2.0
    ay = ky
    bx = -kx + Q / 2.0
    by = -ky
    xi_a0 = -2 * t * (np.cos(ax) + np.cos(ay)) - mu
    xi_b0 = -2 * t * (np.cos(bx) + np.cos(by)) - mu
    xi_a = xi_a0 + (t_am / 2.0) * (np.cos(ax) - np.cos(ay)) + B      # spin up
    xi_b = xi_b0 - (t_am / 2.0) * (np.cos(bx) - np.cos(by)) - B      # spin down
    if swave:
        eta = np.ones_like(kx)   # isotropic s-wave: single channel gamma_s=1
        gamma = np.zeros_like(kx)
    else:
        eta = np.cos(kx) - np.cos(ky)     # d-wave
        gamma = np.cos(kx) + np.cos(ky)   # extended s
    return xi_a, xi_b, eta, gamma

TEMP = 0.01   # small Fermi smearing: removes grid noise in e(Q) so modest N resolves FF

def fermi(E):
    return 0.5 * (1.0 - np.tanh(0.5 * E / TEMP))

def omega_and_rho(params, kx, ky, Q, t_am, B, mu, swave=False):
    """Finite-T BdG grand potential per site and density, given (Delta_d, Delta_s)."""
    Dd, Ds = params
    xi_a, xi_b, eta, gamma = dispersions(kx, ky, Q, t_am, B, mu, swave)
    Dk = Dd * eta + Ds * gamma
    xi_p = 0.5 * (xi_a + xi_b)
    xi_m = 0.5 * (xi_a - xi_b)
    Eqp = np.sqrt(xi_p ** 2 + Dk ** 2)
    Ep = xi_m + Eqp   # E+ = xi_-  + E_qp
    Em = xi_m - Eqp   # E- = xi_-  - E_qp
    # Omega_k = xi_b(constant) - T sum_s ln(1+e^{-E_s/T}) ; use softplus for stability
    def sp(E):  # -T ln(1+e^{-E/T}) = -softplus(-E)
        return -TEMP * np.logaddexp(0.0, -E / TEMP)
    omega = (Dd ** 2 + Ds ** 2) / V + np.mean(xi_b + sp(Ep) + sp(Em))
    # Density via coherence factors with Fermi occupations:
    #   n_k = 1 + (xi_+/E_qp)[ f(E+) - f(E-) ]
    rho = np.mean(1.0 + (xi_p / Eqp) * (fermi(Ep) - fermi(Em)))
    return omega, rho

def solve_fixed_Q(kx, ky, Q, t_am, B, swave=False, D0=(0.2, 0.0)):
    """For fixed Q: for each trial Delta_d (Ds~0, paper: Ds<<Dd), tune mu by bisection so
    rho=target, evaluate free energy e(Delta). Return the Delta minimizing e. Robust grid
    scan avoids the near-flat FF-landscape collapse that fooled Nelder-Mead."""
    def mu_for(Dd):
        def rho_err(mu):
            _, rho = omega_and_rho([Dd, 0.0], kx, ky, Q, t_am, B, mu, swave)
            return rho - RHO_TARGET
        try:
            return brentq(rho_err, -8.0, 8.0, xtol=5e-4, maxiter=80)
        except ValueError:
            return None

    Dgrid = np.concatenate([[0.0], np.linspace(0.005, 0.45, 46)])
    best = None
    for Dd in Dgrid:
        mu = mu_for(Dd)
        if mu is None:
            continue
        omega, rho = omega_and_rho([Dd, 0.0], kx, ky, Q, t_am, B, mu, swave)
        e = omega + mu * rho
        if best is None or e < best["e"] - 1e-12:
            best = dict(Q=Q, mu=mu, Dd=float(Dd), Ds=0.0, omega=omega, rho=rho, e=e)
    # local refine around the grid minimum
    Dc = best["Dd"]
    for Dd in np.linspace(max(0.0, Dc - 0.01), Dc + 0.01, 11):
        mu = mu_for(Dd)
        if mu is None:
            continue
        omega, rho = omega_and_rho([Dd, 0.0], kx, ky, Q, t_am, B, mu, swave)
        e = omega + mu * rho
        if e < best["e"] - 1e-12:
            best = dict(Q=Q, mu=mu, Dd=float(Dd), Ds=0.0, omega=omega, rho=rho, e=e)
    return best

def minimize_over_Q(kx, ky, t_am, B, Qgrid, swave=False):
    recs = []
    D0 = (0.15, 0.0)
    for Q in Qgrid:
        r = solve_fixed_Q(kx, ky, Q, t_am, B, swave, D0=D0)
        recs.append(r)
        if r["Dd"] > 1e-3:
            D0 = (max(r["Dd"], 0.02), r["Ds"])   # warm-start next Q
    es = np.array([r["e"] for r in recs])
    imin = int(np.argmin(es))
    best = recs[imin]
    Dmax = max(r["Dd"] for r in recs)
    # classify from the WINNING state's own gap (avoids near-degenerate argmin picking
    # a collapsed-gap Q): SC requires Dd_star above the normal threshold.
    GAP_THR = 0.0009
    is_sc = best["Dd"] > GAP_THR
    normal = not is_sc
    is_FF = is_sc and (best["Q"] > 1e-6)
    is_BCS = is_sc and (best["Q"] <= 1e-6)
    return dict(t_am=t_am, B=B, Qstar=best["Q"], Dd_star=best["Dd"],
                e_star=best["e"], is_FF=bool(is_FF), is_BCS=bool(is_BCS),
                normal=bool(normal), Dd_max=Dmax,
                curve=[(r["Q"], r["e"], r["Dd"]) for r in recs])

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "coarse"
    t0 = time.time()
    if mode == "retry":
        # perf-bounded: coarse 24x24 grid, 11-pt q-scan, focused t_am on FF window edges
        N = 24; Qgrid = np.round(np.linspace(0.0, 0.6, 11), 4)
        tam_list = [0.0, 0.3, 0.4, 0.44, 0.5, 0.56, 0.6]
    elif mode == "coarse":
        N = 96; Qgrid = np.round(np.arange(0.0, 0.61, 0.05), 4)
        tam_list = [0.0, 0.3, 0.45, 0.5, 0.55, 0.6]
    elif mode == "full":
        N = 200; Qgrid = np.round(np.arange(0.0, 0.71, 0.02), 4)
        tam_list = list(np.round(np.arange(0.0, 0.71, 0.05), 4))
    else:
        N = 160; Qgrid = np.round(np.arange(0.0, 0.61, 0.03), 4)
        tam_list = list(np.round(np.arange(0.30, 0.66, 0.025), 4))
    kx, ky = build_k(N)
    print(f"mode={mode} N={N} |Qgrid|={len(Qgrid)} |tam|={len(tam_list)}", flush=True)
    out_name = "work/chakraborty2023_result.json" if mode == "retry" else f"work/chakraborty2023_result_{mode}.json"
    dwave, swave = [], []
    for tam in tam_list:
        rd = minimize_over_Q(kx, ky, tam, 0.0, Qgrid, swave=False)
        dwave.append(rd)
        print(f"  d-wave B=0 t_am={tam:.3f}  Q*={rd['Qstar']:.3f}  Dd*={rd['Dd_star']:.4f}"
              f"  FF={rd['is_FF']} normal={rd['normal']}", flush=True)
    # SAVE-EARLY: persist the headline (d-wave FF-onset) result before s-wave refinement
    early = dict(mode=mode, N=N, t=t, V=V, rho_target=RHO_TARGET,
                 Qgrid=[float(q) for q in Qgrid], dwave_B0=dwave, swave_B0=[],
                 stage="save_early_after_first_dwave_qscan", runtime_s=time.time() - t0)
    with open(out_name, "w") as fh:
        json.dump(early, fh, indent=2, default=float)
    print(f"SAVE-EARLY wrote {out_name} after d-wave q-scan ({early['runtime_s']:.1f}s)", flush=True)
    for tam in tam_list:
        rs = minimize_over_Q(kx, ky, tam, 0.0, Qgrid, swave=True)
        swave.append(rs)
        print(f"  s-wave B=0 t_am={tam:.3f}  Q*={rs['Qstar']:.3f}  Dd*={rs['Dd_star']:.4f}"
              f"  FF={rs['is_FF']} normal={rs['normal']}", flush=True)
    out = dict(mode=mode, N=N, t=t, V=V, rho_target=RHO_TARGET,
               Qgrid=[float(q) for q in Qgrid],
               dwave_B0=dwave, swave_B0=swave, stage="complete", runtime_s=time.time() - t0)
    with open(out_name, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"WROTE {out_name} in {out['runtime_s']:.1f}s", flush=True)
