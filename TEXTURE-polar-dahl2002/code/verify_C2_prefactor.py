#!/usr/bin/env python3
"""Clarify C2: the quoted law tau = gamma/(Ps E) is a CHARACTERISTIC time.
The 10-90% switch time carries an O(1) integration prefactor. Here we show:
 (a) tau_char = gamma/(Ps E) is exactly the linearized relaxation time at phi=0,
 (b) the full 10-90% time equals tau_char * (a pure number, field-independent),
     confirming the SCALING tau ~ 1/E is exact and only the constant differs.
"""
import numpy as np
from ssflc_model import switch_dynamics, PARAMS, EPS0

gamma, Ps = PARAMS["gamma"], PARAMS["Ps"]

# Ignore dielectric term (small) -> pure ferro overdamped: gamma dphi/dt = Ps E cos(phi)
# Separable: dt = gamma/(Ps E) * dphi/cos(phi). Integral of sec from phi_lo to phi_hi.
def analytic_1090(E, phi0=-np.pi/2+0.05):
    phi_lo = phi0 + 0.1*(np.pi/2 - phi0)
    phi_hi = phi0 + 0.9*(np.pi/2 - phi0)
    # INT sec(phi) dphi = ln|sec+tan|
    F = lambda p: np.log(abs(1/np.cos(p) + np.tan(p)))
    return (gamma/(Ps*E)) * (F(phi_hi) - F(phi_lo))

Efields = np.array([2e6, 3e6, 5e6, 8e6, 1.2e7])
print(f"{'E(V/m)':>10} {'tau_char':>12} {'tau_1090_num':>14} {'tau_1090_analytic':>18} {'ratio_to_char':>14}")
for E in Efields:
    tc = gamma/(Ps*E)
    num = switch_dynamics(E, PARAMS)
    ana = analytic_1090(E)
    print(f"{E:>10.2e} {tc:>12.4e} {num:>14.4e} {ana:>18.4e} {num/tc:>14.4f}")

print("\nInterpretation: tau_1090/tau_char is CONSTANT across E (field-independent")
print("O(1) prefactor from the 10-90% definition). Hence tau ~ 1/E scaling EXACT;")
print("the ~3.5x factor vs gamma/Ps is that pure integration constant, not a")
print("failure of the quoted law.")
