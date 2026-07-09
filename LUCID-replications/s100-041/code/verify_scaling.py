"""
Verify the three analytic scaling laws of Abolfath et al. (Eqs 7, 8, 9):

  Eq 7 (short time)  : N1 ~ G * t
  Eq 8 (short time)  : N2 ~ G^2 * Df * t^3
  Eq 9 (long  time)  : N2 ~ G^(2/3) * Df^(-1/3) * t^(1/3)

Method: integrate Eqs 1-2 with a CONSTANT source G (no pulse) so the short-time
power laws are clean, then fit log-log slopes in clearly-separated windows.
"""

import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path

EVDIR = Path(__file__).resolve().parent.parent / "evidence"
EVDIR.mkdir(exist_ok=True, parents=True)

def integrate_constant_G(G, Df=1.0, t_end=1e6, n=4000):
    def rhs(t, y):
        N1, N2 = y
        return [G - 2*Df*N1*N1 - Df*N2*N1, Df*N1*N1]
    t_eval = np.logspace(-8, np.log10(t_end), n)
    sol = solve_ivp(rhs, (0.0, t_end), [0.0, 0.0],
                    method="Radau", t_eval=t_eval,
                    rtol=1e-10, atol=1e-16)
    return sol.t, sol.y[0], sol.y[1]

def fit_loglog_slope(x, y, mask):
    lx = np.log(x[mask]); ly = np.log(y[mask])
    p = np.polyfit(lx, ly, 1)
    return p[0], p[1]   # slope, intercept

lines = []
lines.append("=== Verification of analytic scaling laws (Eqs 7, 8, 9) ===\n")

for G in [1.0, 100.0]:
    Df = 1.0
    t, N1, N2 = integrate_constant_G(G=G, Df=Df, t_end=1e6)

    # Short-time window: small enough that N1 << equilibrium
    # Equilibrium scale t1 = 1/sqrt(Df*G); use t << t1
    t1 = 1.0/np.sqrt(Df*G)
    short_mask = (t > 1e-6 * t1) & (t < 1e-3 * t1) & (N1 > 0) & (N2 > 0)
    long_mask  = (t > 1e2 * t1)  & (t < 1e5 * t1)  & (N1 > 0) & (N2 > 0)

    s_N1, _ = fit_loglog_slope(t, N1, short_mask)
    s_N2_short, _ = fit_loglog_slope(t, N2, short_mask)
    s_N2_long,  _ = fit_loglog_slope(t, N2, long_mask)

    # Coefficient check for Eq 7: N1/(G*t) -> 1
    ratio_eq7 = (N1[short_mask] / (G * t[short_mask])).mean()
    # Coefficient check for Eq 8: N2 = G^2 Df t^3 / 3 (exact from integrating N2'=Df*(Gt)^2)
    ratio_eq8 = (N2[short_mask] / (G*G * Df * t[short_mask]**3 / 3.0)).mean()
    # Coefficient check for Eq 9: from Ñ2 = (3 t̃)^(1/3) ⇒ N2 = (3 t)^(1/3) * G^(2/3) * Df^(-1/3)
    expected_N2_long = (3.0 * t[long_mask])**(1.0/3.0) * G**(2.0/3.0) * Df**(-1.0/3.0)
    ratio_eq9 = (N2[long_mask] / expected_N2_long).mean()

    block = (
        f"\n--- G = {G}, Df = {Df}, t1 = 1/sqrt(Df*G) = {t1:.3e} s ---\n"
        f"Eq 7  (N1 ~ G*t)            slope = {s_N1:.4f}    (analytic = 1.000)   "
        f"N1/(G*t) mean = {ratio_eq7:.4f} (expect 1.000)\n"
        f"Eq 8  (N2 ~ G^2 Df t^3)     slope = {s_N2_short:.4f}    (analytic = 3.000)   "
        f"N2/(G^2 Df t^3 / 3) mean = {ratio_eq8:.4f} (expect 1.000)\n"
        f"Eq 9  (N2 ~ (G^2/Df)^1/3 t^1/3) slope = {s_N2_long:.4f}    (analytic = 0.333)   "
        f"N2/((3t)^1/3 G^2/3 Df^-1/3) mean = {ratio_eq9:.4f} (expect 1.000)\n"
    )
    lines.append(block)
    print(block)

with open(EVDIR / "scaling_exponents.txt", "w") as f:
    f.writelines(lines)

print(f"\nWrote {EVDIR/'scaling_exponents.txt'}")
