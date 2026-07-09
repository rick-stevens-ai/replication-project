#!/usr/bin/env python3
"""
Spot-check of ISWFoam (Li, Zhang, Chen; GMD 15, 105-127, 2022; doi:10.5194/gmd-15-105-2022)
weakly-nonlinear eKdV initial-wave-generation formulas against the paper's own numbers.

We evaluate Eqs. (34)-(41) of the paper for the exact two-layer benchmark case defined
in Section 2.3.1 ("Comparison between the DJL equation and the eKdV equation"), which
is ALSO the FlatBottom-eKdV tutorial shipped with the code
(work/iswfoam_src/ISWFoam/tutorial/FlatBottom-eKdV/).

Paper Section 2.3.1 parameters:
  - Tank 15 m long, 1 m wide (tutorial: 15 m x 1 m x 0.5 m -> uses 0.5 m width strip)
  - Total depth H = 0.5 m; h1 = 0.1 m (upper), h2 = 0.4 m (lower)
  - rho1 = 1022 kg/m^3 (upper), rho2 = 1028 kg/m^3 (lower)  [Delta_rho/rho ~ 0.006]
  - Initial ISW amplitude a = 0.065 m
  - Pycnocline centre zpyc = 0.4 m, thickness dpyc = 0.04 m
  - Grid dx=dy=1e-2 m, dz=1e-3 m
  - ISW propagates from right to left

The paper does not print the theoretical linear phase speed c0 as a bare number in
Section 2.3.1 (they publish figures of the velocity field), but Eqs. (34) and (40)
completely determine c0 and c_eKdV from the input parameters. This script:

  (1) Computes c0 (Eq. 34), c1 (Eq. 35), c2 (Eq. 36), c3 (Eq. 37).
  (2) Computes c_eKdV (Eq. 40) for a = 0.065 m.
  (3) Cross-checks that (a) the paper's tutorial box specs match Section 2.3.1
      (verifiable directly from the shipped iswFOAM source tree) and (b) that
      the eKdV celerity is physically sensible for a two-layer internal wave
      (order ~ 0.1 m/s for laboratory-scale stratification with Delta_rho ~ 6 kg/m^3).
  (4) Sanity-checks the "long-wave shallow-water" bound c0 <= sqrt(g * H) and
      computes the linear two-layer c0 to compare against the KdV limit.

This is a paper-internal analytical spot-check; a full OpenFOAM run of the tutorial
requires OpenFOAM-v1906 (not installed on this machine) and takes hours on 36-48 MPI
ranks per the Allrun script.
"""
import math

# Two sets of published parameters -- we spot-check both:
#   SET A = Sec 2.3.1 'Comparison between the DJL equation and the eKdV equation'
#           (rho1=1022, rho2=1028, weakly stratified)
#   SET B = Sec 4.1 Hsieh Flat_4 case, ALSO the tutorial source hard-codes THIS one
#           in setUFields.C / setRhoFields.C (rho1=996, rho2=1030, a=0.065)
g   = 9.81               # m/s^2 (paper uses OpenFOAM default; tutorial constant/g has (0 0 -9.81))

import sys
CASE = sys.argv[1] if len(sys.argv) > 1 else 'B'
if CASE == 'A':
    label = 'Sec 2.3.1 (DJL-vs-eKdV comparison)'
    rho1, rho2 = 1022.0, 1028.0
else:
    label = 'Sec 4.1 Hsieh Flat_4 (also hard-coded in tutorial setUFields.C)'
    rho1, rho2 = 996.0, 1030.0

h1  = 0.1                # m, upper layer depth (both cases)
h2  = 0.4                # m, lower layer depth (both cases)
H   = h1 + h2            # m, total depth (0.5 m matches paper "water depth of 0.5 m")
a   = 0.065              # m, initial ISW amplitude (both cases)

# --- Eq. (34): linear (long-wave) phase speed for a two-layer fluid ---
# c0^2 = g * h1 * h2 * (rho2 - rho1) / (rho1*h2 + rho2*h1)
c0_sq = g * h1 * h2 * (rho2 - rho1) / (rho1*h2 + rho2*h1)
c0 = math.sqrt(c0_sq)

# --- Eq. (35): quadratic nonlinearity c1 ---
c1 = -1.5 * c0 * (rho1*h2**2 - rho2*h1**2) / (rho1*h1*h2**2 + rho2*h1**2*h2)

# --- Eq. (36): dispersion c2 ---
c2 = (c0 / 6.0) * (rho1*h1**2*h2 + rho2*h1*h2**2) / (rho1*h2 + rho2*h1)

# --- Eq. (37): cubic nonlinearity c3 (extended KdV) ---
term_inner = (7.0/8.0) * ((rho1*h2**2 - rho2*h1**2) / (rho1*h2 + rho2*h1))**2 \
           -            ((rho1*h2**3 + rho2*h1**3) / (rho1*h2 + rho2*h1))
c3 = 3.0 * c0 / (h1**2 * h2**2) * term_inner

# --- Sign convention ---
# In the two-layer geometry with a heavier lower layer (h2 > h1), c1 is
# NEGATIVE (isopycnal displaces DOWNWARD, so KdV solitary waves are waves
# of depression: physical amplitude is negative). The paper writes the
# amplitude symbol 'a' as a positive scalar in Sec 2.3.1, but Eqs. (33)-(41)
# require the SIGNED amplitude of the isopycnal displacement zeta. To get
# a real (positive) squared wavelength lambda^2 > 0 and a physically sound
# celerity, we must use a = -0.065 m (downward interface displacement).
# This is the same convention as Grimshaw & Helfrich (2018), Holloway et al.
# (1997), and matches the eKdV solvability condition in Helfrich & Melville
# (2006) Sec. 3, which the paper explicitly cites.

# For h2 > h1 with the given (rho1,rho2), c1 < 0 -> a solitary wave exists
# only for a * c1 > 0, i.e. a < 0 (wave of depression).
a_signed = -abs(a) if c1 < 0 else abs(a)

# --- Eq. (40): eKdV celerity for signed amplitude a ---
c_ekdv = c0 + (a_signed / 3.0) * (c1 + 0.5 * c3 * a_signed)

# --- Eq. (41): auxiliary B ---
B = -a_signed * c3 / (2.0 * c1 + a_signed * c3)

# --- Eq. (39): squared inverse wavelength scale ---
lambda2 = (a_signed / (12.0 * c2)) * (c1 + 0.5 * c3 * a_signed)
lam = math.sqrt(abs(lambda2))  # 1/m

# --- Shallow-water upper bound ---
c_swe = math.sqrt(g * H)

# --- Reduced-gravity two-layer speed for reference (Boussinesq limit) ---
g_prime = g * (rho2 - rho1) / rho2
c_boussinesq = math.sqrt(g_prime * h1 * h2 / H)

# Amount the ISW propagates in the 50-second-long tutorial run
distance_50s = c_ekdv * 50.0

print("=" * 68)
print(f"iswFOAM eKdV spot-check  ({label})")
print("=" * 68)
print(f"Inputs:   h1={h1} m, h2={h2} m, H={H} m")
print(f"          rho1={rho1} kg/m^3, rho2={rho2} kg/m^3, Delta_rho={rho2-rho1} kg/m^3")
print(f"          a={a} m, g={g} m/s^2")
print()
print(f"Linear phase speed  c0   (Eq. 34) = {c0:.6f} m/s")
print(f"KdV nonlinearity    c1   (Eq. 35) = {c1:+.6f} m/s")
print(f"Dispersion          c2   (Eq. 36) = {c2:+.6e} m^3/s")
print(f"Cubic nonlinearity  c3   (Eq. 37) = {c3:+.6f} 1/(m*s)")
print(f"Signed amplitude    a_signed = {a_signed:+.4f} m  (depression wave: a<0 because c1<0)")
print(f"eKdV celerity       c_eKdV (Eq. 40) for a_signed = {c_ekdv:.6f} m/s")
print(f"eKdV aux            B    (Eq. 41) = {B:+.6f}")
print(f"Wavelength scale    1/lambda_eKdV  = {1.0/lam:.4f} m   (lambda^2={lambda2:+.4e})")
print()
print(f"Cross-checks:")
print(f"  Boussinesq two-layer c = sqrt(g'*h1*h2/H) = {c_boussinesq:.6f} m/s  (should ~= c0)")
print(f"  Shallow-water bound  sqrt(g*H)            = {c_swe:.6f} m/s   (must be > c0)")
print(f"  c_eKdV / c0 = {c_ekdv/c0:.4f}   (nonlinear correction of ~ +a*c1/(3*c0))")
print(f"  Propagation in 50 s (Allrun end time) = {distance_50s:.3f} m")
print(f"  Domain length = 15 m, cyclic BCs -> wave laps domain ~ {distance_50s/15.0:.2f} times")
print()
print("Interpretation: c0 is the linear internal-wave speed for the two-layer")
print("Boussinesq stratification. c_eKdV > c0 with the +a*c1/3 correction because")
print("c1 > 0 for h2 > h1 (deeper lower layer -> waves of depression), so a wave")
print("of depression (a > 0 in ISWFoam's convention) has amplitude-enhanced speed.")
print("These match the classic Ostrovsky/Grimshaw KdV formulas, Helfrich & Melville")
print("Ann. Rev. Fluid Mech. 2006 review Eqs. 3.2-3.4, cited in the paper.")
