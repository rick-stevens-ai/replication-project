#!/usr/bin/env python3
"""
Independent spot-check reproduction of RDycore's 1D frictionless
dam-break verification (Bisht et al. 2026, Table 1).

Numerical scheme mirrors RDycore's stated choice:
  * 1D shallow water equations (SWE), conservative form
  * First-order finite volume in space
  * Roe approximate Riemann flux at cell faces
  * Forward Euler in time
  * Frictionless (Manning n=0), flat bed
  * Reflecting walls at both ends of the domain

Case setup (per paper Section 3.1):
  L  = 10 m (domain length)
  x0 = 5 m  (initial discontinuity)
  h_l = 0.005 m
  Dry case: h_r = 0.0 m
  Wet case: h_r = 0.001 m
  Initial velocity: 0 m/s everywhere
  Reference analytical solution from SWASHES.

Grids tested: N = 100, 1000, 10000.
Errors reported: L1 for h on the interior, compared against Ritter (dry)
or Stoker (wet) analytical solution at final time t.

We check the CONVERGENCE-RATE claim: RDycore's R for h is 0.60-0.88 for
dry and 0.77-0.81 for wet, first-order-with-slope-limited-behavior at
shocks.
"""

import math
import numpy as np


G = 9.81   # gravity (m/s^2), same as paper


def roe_flux_vec(hL, huL, hR, huR):
    """Vectorized Roe approximate Riemann flux for 1D SWE (h, hu).

    All inputs are 1D arrays over interfaces. Returns (F_h, F_hu) arrays.
    """
    hL = np.asarray(hL, dtype=float)
    hR = np.asarray(hR, dtype=float)
    huL = np.asarray(huL, dtype=float)
    huR = np.asarray(huR, dtype=float)

    uL = np.where(hL > 1e-14, huL / np.maximum(hL, 1e-14), 0.0)
    uR = np.where(hR > 1e-14, huR / np.maximum(hR, 1e-14), 0.0)

    FL_h  = huL
    FL_hu = huL * uL + 0.5 * G * hL * hL
    FR_h  = huR
    FR_hu = huR * uR + 0.5 * G * hR * hR

    sqL = np.sqrt(np.maximum(hL, 0.0))
    sqR = np.sqrt(np.maximum(hR, 0.0))
    denom = sqL + sqR
    safe = denom > 1e-14
    u_hat = np.where(safe, (sqL * uL + sqR * uR) / np.where(safe, denom, 1.0), 0.0)
    h_hat = 0.5 * (hL + hR)
    c_hat = np.sqrt(G * np.maximum(h_hat, 0.0))

    l1 = u_hat - c_hat
    l2 = u_hat + c_hat

    dh = hR - hL
    dhu = huR - huL

    c_safe = np.where(c_hat > 1e-14, c_hat, 1.0)
    a1 = ((u_hat + c_hat) * dh - dhu) / (2.0 * c_safe)
    a2 = (-(u_hat - c_hat) * dh + dhu) / (2.0 * c_safe)

    # dissipation components
    diss_h  = np.abs(l1) * a1 * 1.0        + np.abs(l2) * a2 * 1.0
    diss_hu = np.abs(l1) * a1 * l1         + np.abs(l2) * a2 * l2

    F_h  = 0.5 * (FL_h  + FR_h)  - 0.5 * diss_h
    F_hu = 0.5 * (FL_hu + FR_hu) - 0.5 * diss_hu

    # When both sides are dry, flux = 0
    dry = (hL < 1e-14) & (hR < 1e-14)
    F_h  = np.where(dry, 0.0, F_h)
    F_hu = np.where(dry, 0.0, F_hu)
    # When c_hat is effectively zero fall back to average of physical fluxes
    no_wave = c_hat <= 1e-14
    F_h  = np.where(no_wave, 0.5 * (FL_h + FR_h),  F_h)
    F_hu = np.where(no_wave, 0.5 * (FL_hu + FR_hu), F_hu)
    return F_h, F_hu


def solve_dambreak(N, hl, hr, L=10.0, x0=5.0, t_end=None, cfl=0.4):
    """Solve 1D dam-break with first-order FV + Roe + forward Euler."""
    dx = L / N
    x = (np.arange(N) + 0.5) * dx      # cell centers
    h = np.where(x <= x0, hl, hr).astype(float)
    hu = np.zeros(N)

    # Final time: use paper-relevant t; a common choice is t at which the
    # wave has moved a fraction of the domain. Ritter: shock speed ~ 2*sqrt(g*hl).
    # Choose t so wave stays inside domain (roughly x0 / (2*sqrt(g*hl))).
    if t_end is None:
        c0 = math.sqrt(G * hl)
        t_end = 0.7 * x0 / (2.0 * c0)  # ~90% of time to reach boundary

    t = 0.0
    while t < t_end:
        # CFL: max wave speed
        u = np.where(h > 1e-14, hu / np.maximum(h, 1e-14), 0.0)
        c = np.sqrt(G * np.maximum(h, 0.0))
        smax = float(np.max(np.abs(u) + c))
        if smax < 1e-14:
            break
        dt = cfl * dx / smax
        if t + dt > t_end:
            dt = t_end - t

        # Build left/right states at N+1 interfaces with reflecting walls.
        # Ghost cells: mirror h, negate hu.
        h_ext  = np.concatenate([[h[0]],  h,  [h[-1]]])
        hu_ext = np.concatenate([[-hu[0]], hu, [-hu[-1]]])
        hL_i  = h_ext[:-1]
        hR_i  = h_ext[1:]
        huL_i = hu_ext[:-1]
        huR_i = hu_ext[1:]
        F_h, F_hu = roe_flux_vec(hL_i, huL_i, hR_i, huR_i)

        h  = h  - (dt / dx) * (F_h[1:]  - F_h[:-1])
        hu = hu - (dt / dx) * (F_hu[1:] - F_hu[:-1])

        # Dry-bed positivity
        h  = np.where(h < 0.0, 0.0, h)
        hu = np.where(h < 1e-14, 0.0, hu)

        t += dt

    return x, h, hu, t


# --------- analytical solutions (SWASHES formulae) ---------

def ritter_dry(x, t, hl, x0=5.0):
    """Ritter solution: dam-break over dry bed, no friction.
    Regions relative to xA = x0 - c0*t, xB = x0 + 2*c0*t, c0 = sqrt(g*hl).
      x < xA: h = hl,        u = 0
      xA <= x <= xB: h = (1/(9g)) * (2c0 - (x - x0)/t)^2
                    u = (2/3) * ((x - x0)/t + c0)
      x > xB: h = 0, u = 0
    """
    c0 = math.sqrt(G * hl)
    xA = x0 - c0 * t
    xB = x0 + 2.0 * c0 * t
    h = np.empty_like(x)
    u = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < xA:
            h[i] = hl
            u[i] = 0.0
        elif xi <= xB:
            h[i] = (1.0 / (9.0 * G)) * (2.0 * c0 - (xi - x0) / t)**2
            u[i] = (2.0 / 3.0) * ((xi - x0) / t + c0)
        else:
            h[i] = 0.0
            u[i] = 0.0
    return h, u


def stoker_wet(x, t, hl, hr, x0=5.0):
    """Stoker's wet dam-break analytical solution.
    Requires solving a nonlinear equation for the intermediate depth hm."""
    c0 = math.sqrt(G * hl)
    cr = math.sqrt(G * hr)

    # Solve for cm = sqrt(g*hm) satisfying Stoker's transcendental eq:
    #   -8 g hr cm^2 (c0 - cm)^2 + (cm^2 - g hr)^2 (cm^2 + g hr) = 0
    # Use bisection between cr and c0.
    def f(cm):
        return (-8.0 * G * hr * cm*cm * (c0 - cm)**2
                + (cm*cm - G*hr)**2 * (cm*cm + G*hr))
    lo, hi = cr + 1e-12, c0 - 1e-12
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        # bracket failed; try wider
        lo, hi = 1e-8, c0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm * f(lo) <= 0:
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) < 1e-14:
            break
    cm = 0.5 * (lo + hi)
    hm = cm*cm / G
    um = 2.0 * (c0 - cm)
    # shock speed
    s = um * hm / (hm - hr)

    # rarefaction head/tail
    xA = x0 - c0 * t                  # head of left-going rarefaction
    xB = x0 + (um - cm) * t           # tail of rarefaction (contact to shock left)
    xC = x0 + s * t                   # shock position

    h = np.empty_like(x)
    u = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < xA:
            h[i] = hl
            u[i] = 0.0
        elif xi < xB:
            # rarefaction fan
            u_r = (2.0 / 3.0) * ((xi - x0) / t + c0)
            c_r = (1.0 / 3.0) * (2.0 * c0 - (xi - x0) / t)
            h[i] = c_r * c_r / G
            u[i] = u_r
        elif xi < xC:
            h[i] = hm
            u[i] = um
        else:
            h[i] = hr
            u[i] = 0.0
    return h, u


def L1_error(sim, ana, dx):
    L_dom = dx * len(sim)
    return float(np.sum(np.abs(sim - ana)) * dx / L_dom)


# ---------- run ----------

def main():
    hl = 0.005
    x0 = 5.0
    L = 10.0

    results = {"dry": [], "wet": []}

    for case_name, hr in [("dry", 0.0), ("wet", 0.001)]:
        print(f"\n=== {case_name} case (hl={hl}, hr={hr}) ===")
        prev_L1 = None
        prev_dx = None
        for N in [100, 1000, 10000]:
            x, h, hu, t = solve_dambreak(N, hl, hr, L=L, x0=x0)
            if case_name == "dry":
                h_ana, u_ana = ritter_dry(x, t, hl, x0)
            else:
                h_ana, u_ana = stoker_wet(x, t, hl, hr, x0)
            l1h = L1_error(h, h_ana, L / N)
            hu_ana = h_ana * u_ana
            l1hu = L1_error(hu, hu_ana, L / N)
            dx = L / N
            R_h = R_hu = None
            if prev_L1 is not None:
                # R defined per paper: log(L1_k1 / L1_k2) / log(dx_k1 / dx_k2)
                R_h  = math.log(prev_L1[0] / l1h)  / math.log(prev_dx / dx)
                R_hu = math.log(prev_L1[1] / l1hu) / math.log(prev_dx / dx)
            print(f"  N={N:>6d}  t={t:.4f}s  L1(h)={l1h:.3e}  L1(hu)={l1hu:.3e}"
                  + (f"  R(h)={R_h:.3f} R(hu)={R_hu:.3f}" if R_h is not None else ""))
            results[case_name].append({"N": N, "t": t, "L1_h": l1h,
                                       "L1_hu": l1hu, "R_h": R_h, "R_hu": R_hu})
            prev_L1 = (l1h, l1hu)
            prev_dx = dx

    # Summary vs. paper
    print("\n=== Summary vs. paper Table 1 ===")
    print(" Paper R(h) dry (1000 vs 100)     : 0.60  |  ours:",
          f"{results['dry'][1]['R_h']:.2f}")
    print(" Paper R(h) dry (10000 vs 1000)   : 0.76  |  ours:",
          f"{results['dry'][2]['R_h']:.2f}")
    print(" Paper R(h) wet (1000 vs 100)     : 0.77  |  ours:",
          f"{results['wet'][1]['R_h']:.2f}")
    print(" Paper R(h) wet (10000 vs 1000)   : 0.81  |  ours:",
          f"{results['wet'][2]['R_h']:.2f}")

    # dump json
    import json, os
    out = os.path.join(os.path.dirname(__file__), "dambreak_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
