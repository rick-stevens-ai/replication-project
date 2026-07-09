#!/usr/bin/env python3
"""
Reproduction of Abolfath/Grosshans/Mohan (Med Phys 2020, DOI 10.1002/mp.14548)
Eqs. (1)-(2): coupled ROS/NROS rate equations.

    dN1/dt = G(t) - 2 Df N1^2 - Df N1 N2     ... (1)
    dN2/dt = Df N1^2                          ... (2)

Pulse experiment from Sec III.A:
  FLASH-UHDR  : G1(t) = 100   for 0 <= t <= 0.01 s   (integrated dose = 1)
  CDR         : G2(t) = 0.01  for 0 <= t <= 100  s   (integrated dose = 1)
  Df chosen = 1 (paper does not specify; equations are written in
                  dimensionless form, and ratio of long-time N2 between
                  pulses is independent of Df; see Eq.(9) which gives
                  N2 ~ G^(2/3) Df^(-1/3) t^(1/3)).

Headline numerical claim (Fig.7 caption):
  "At longer times, N2 at UHDR is approximately twice that at CDR
   for the specific pulse used in this calculation."

We integrate Eqs.(1)-(2) with scipy and check the long-time ratio.
We also verify the short-time scaling laws Eqs.(7)-(8): N1 ~ G t, N2 ~ G^2 Df t^3,
and the long-time scaling Eq.(9): N2 ~ G^(2/3) Df^(-1/3) t^(1/3).
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs(t, y, G_func, Df):
    N1, N2 = y
    G = G_func(t)
    dN1 = G - 2.0 * Df * N1 * N1 - Df * N1 * N2
    dN2 = Df * N1 * N1
    return [dN1, dN2]


def integrate(G_amp, pulse_width, Df=1.0, t_end=None, n_eval=4000):
    """Integrate Eqs.(1)-(2) for a square pulse of amplitude G_amp and
    duration pulse_width. Track for several decades after pulse end."""
    if t_end is None:
        t_end = max(100.0, pulse_width * 10.0)

    def G(t):
        return G_amp if (0.0 <= t <= pulse_width) else 0.0

    # log-spaced eval times starting just past 0; clip to t_end
    t_eval = np.geomspace(min(1e-4 * pulse_width, t_end / 1e6), t_end, n_eval)
    t_eval = t_eval[t_eval <= t_end]
    sol = solve_ivp(
        rhs,
        (0.0, t_end),
        [0.0, 0.0],
        t_eval=t_eval,
        args=(G, Df),
        method="LSODA",
        rtol=1e-9,
        atol=1e-14,
        max_step=pulse_width / 20.0,
    )
    assert sol.success, sol.message
    return sol.t, sol.y[0], sol.y[1]


def main():
    Df = 1.0
    # Paper's two pulses (Sec III.A)
    cases = {
        "FLASH-UHDR (G=100, w=0.01s)": (100.0, 0.01),
        "CDR        (G=0.01, w=100s)": (0.01, 100.0),
    }
    results = {}
    for name, (Gamp, w) in cases.items():
        t, n1, n2 = integrate(Gamp, w, Df=Df, t_end=200.0)
        results[name] = (t, n1, n2)
        # report N1, N2 at several decades
        print(f"\n=== {name} ===")
        print(f"  Integrated G dt = {Gamp * w:.4f}  (should be 1)")
        for tprobe in [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]:
            if tprobe > t[-1]:
                continue
            idx = np.searchsorted(t, tprobe)
            idx = min(idx, len(t) - 1)
            print(f"  t={t[idx]:10.4g}  N1={n1[idx]:12.4e}  N2={n2[idx]:12.4e}")

    # Long-time N2 ratio (paper says ~2x at long time)
    print("\n=== Headline check: N2(UHDR)/N2(CDR) at long time ===")
    t_u, _, n2_u = results["FLASH-UHDR (G=100, w=0.01s)"]
    t_c, _, n2_c = results["CDR        (G=0.01, w=100s)"]
    for tprobe in [10.0, 50.0, 100.0, 200.0]:
        iu = min(np.searchsorted(t_u, tprobe), len(t_u) - 1)
        ic = min(np.searchsorted(t_c, tprobe), len(t_c) - 1)
        ratio = n2_u[iu] / n2_c[ic] if n2_c[ic] > 0 else float("nan")
        print(
            f"  t={tprobe:6.1f}  N2_UHDR={n2_u[iu]:.4e}  "
            f"N2_CDR={n2_c[ic]:.4e}  ratio={ratio:.3f}"
        )

    # Short-time scaling test (Eqs. 7-8): N1 ~ G t, N2 ~ G^2 Df t^3
    print("\n=== Short-time scaling check (Eqs. 7-8): constant-G run ===")
    # Use constant-G "infinitely long" pulse, sample early times
    t, n1, n2 = integrate(G_amp=1.0, pulse_width=1e6, Df=1.0, t_end=1.0,
                          n_eval=2000)
    # Early time: pick t small enough that nonlinear sinks negligible
    for tprobe in [1e-3, 1e-2, 1e-1]:
        idx = np.searchsorted(t, tprobe)
        # Predicted: N1 = G t, N2 = G^2 Df t^3 / 3 (integrating dN2/dt = N1^2 = G^2 t^2)
        pred_n1 = 1.0 * t[idx]
        pred_n2 = (1.0 ** 2) * 1.0 * t[idx] ** 3 / 3.0
        print(
            f"  t={t[idx]:.4e}  N1={n1[idx]:.4e} (pred {pred_n1:.4e})  "
            f"N2={n2[idx]:.4e} (pred {pred_n2:.4e})"
        )

    # Long-time stationary scaling Eq.(9): N2 ~ (3 t)^(1/3) (in dimensionless),
    # which in physical units is N2 ~ G^(2/3) Df^(-1/3) (3 t)^(1/3)
    print("\n=== Long-time scaling check (Eq. 9): constant-G run ===")
    t, n1, n2 = integrate(G_amp=1.0, pulse_width=1e6, Df=1.0, t_end=1e4,
                          n_eval=4000)
    for tprobe in [1.0, 10.0, 100.0, 1000.0]:
        idx = np.searchsorted(t, tprobe)
        pred_n2 = (1.0 ** (2.0 / 3.0)) * (1.0 ** (-1.0 / 3.0)) * (3.0 * t[idx]) ** (1.0 / 3.0)
        ratio = n2[idx] / pred_n2
        print(f"  t={t[idx]:.4e}  N2={n2[idx]:.4e}  pred={pred_n2:.4e}  ratio={ratio:.3f}")

    # Dose-rate G dependence of N2 at fixed dose (long time, post pulse)
    print("\n=== Dose-rate sweep at fixed integrated dose = 1 ===")
    for Gamp in [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0]:
        w = 1.0 / Gamp
        t, n1, n2 = integrate(Gamp, w, Df=1.0, t_end=200.0)
        idx_end = -1
        print(f"  G={Gamp:8.3g} w={w:8.3g}  N2(t=200)={n2[idx_end]:.4e}  "
              f"N1(t=200)={n1[idx_end]:.4e}")


if __name__ == "__main__":
    main()
