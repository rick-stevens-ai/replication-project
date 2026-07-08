"""
probe_central.py — Section 2.3 investigation (CORRECTED equation).

OCR cross-check (tesseract) of the equation region revealed the embedded-text
layer had DROPPED the epsilon factors. True equations:

  Eq.(1):  z'' + mu z' + 4(gamma + alpha cos2t - eps cos 2 wf t)(-z + chi z^3) = 0
  Eq.(2):  z'' + mu z' + 4(gamma + alpha cos2t - eps cos 2 wf t)(-z + eps*chi*z^3) = 0

i.e. after the rescale used for multiple scales, the CUBIC term is O(eps):
  (-z + eps*chi*z^3).
This is consistent with Eq.(7), where the chi*z0^3 term sits at O(eps^1).

Consequence: with eps=1e-3 the cubic is a weak nonlinearity, so z=+-1 are NOT
hard equilibria and the blow-up we saw with (-z + chi z^3) disappears.  The
leading behaviour is the linear Mathieu operator -4(gamma+alpha cos2t)(-z)
= +4(gamma+alpha cos2t) z  plus weak damping and weak secondary forcing.

We test Eq.(2) [eps-scaled cubic] at central resonance vs off resonance.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, str(__file__.rsplit('/',1)[0]))
from mathieu_beta import solve_beta

def rhs_eq2(t, y, mu, gamma, alpha, delta, eps, chi, wf):
    # Eq.(2): cubic scaled by eps; secondary forcing amplitude = delta*eps
    z, zd = y
    drive = 4.0*(gamma + alpha*np.cos(2*t) - delta*eps*np.cos(2*wf*t))
    zdd = -mu*zd - drive*(-z + eps*chi*z**3)
    return [zd, zdd]

def steady_amp(t, y, frac=0.2):
    k = int(len(t)*(1-frac))
    return float(np.max(np.abs(y[0, k:])))

def run(rhs, mu, gamma, alpha, delta, eps, chi, wf, z0, T, label):
    sol = solve_ivp(rhs, (0, T), [z0, 0.0],
                    args=(mu, gamma, alpha, delta, eps, chi, wf),
                    method='RK45', rtol=1e-9, atol=1e-11, max_step=0.2)
    amp = steady_amp(sol.t, sol.y)
    print(f"{label:36s} z0={z0:5.2f} wf={wf:.4f} delta={delta:4.1f}  end|z|(last20%)={amp:.4e}  ok={sol.success}")
    return amp

if __name__ == "__main__":
    alpha, gamma = 0.15, -0.05
    mu = delta = chi = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    print(f"beta(Fig1) = {beta:.6f}  (paper 0.5094)\n")
    T = 8000.0

    print("=== Eq.(2): cubic = eps*chi*z^3  (CORRECTED) ===")
    print("--- central resonance wf=beta, vary IC ---")
    for z0 in [0.5, 1.0, 2.0, 3.0]:
        run(rhs_eq2, mu, gamma, alpha, delta, eps, chi, beta, z0, T, "Fig1 central res")
    print("--- off resonance wf=2beta (expect decay, Fig3) ---")
    for z0 in [2.0, 3.0]:
        run(rhs_eq2, mu, gamma, alpha, delta, eps, chi, 2*beta, z0, T, "Fig3 off-res 2beta")

    print("\n--- Fig2 params: alpha=.25 gamma=.001 mu=.8 delta=10 chi=5, wf=2+beta ---")
    a2,g2 = 0.25, 0.001
    b2 = solve_beta(a2,g2)
    for z0 in [0.5, 1.0, 2.0]:
        run(rhs_eq2, 0.8, g2, a2, 10.0, eps, 5.0, 2+b2, z0, T, "Fig2 p=2 res")
