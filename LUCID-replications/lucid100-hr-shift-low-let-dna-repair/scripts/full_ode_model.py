#!/usr/bin/env python3
"""
Full ODE replication of the Belov et al. 2023 (CIMB 45:7352) DSB repair model.

Implements Eqs. (A4)-(A7), 30 ODEs total, with parameters from Appendix C Table A1.
Computes:
  - gamma-H2AX foci time-courses for the seven paper doses (Fig. 5 analog)
  - Rad51 foci time-courses for the seven paper doses (Fig. 6 analog)
  - PHR(D) = 100 * mean(y9) / mean(x14)  over [0, 24h]  (Eq. 28/29, Fig. 7 analog)

Cell-cycle routing: paper says HF19-like asynchronous culture with 45% G0/G1+early-S
and 55% late-S/G2/M.  G0/G1+early-S cells -> NHEJ+Alt-EJ only (no HR/SSA).  Late-S/G2/M
cells -> all four pathways.  Since HR/SSA only occur in the 55% subpopulation, we run
the full model for the 55% cells and a reduced model (NHEJ+Alt-EJ only) for the 45%
cells, then population-average the foci-bearing variables.

Outputs: results/ode_h2ax_kinetics.csv, results/ode_rad51_kinetics.csv,
results/ode_PHR_vs_dose.csv, figures/ode_full_model.png, results.json.

Run: python3 full_ode_model.py
Time: ~10 s on a laptop CPU for 7 doses and a 25-point PHR sweep.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

# matplotlib optional
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None


# ============================================================================
# Paper constants (Appendix C, Table A1)
# ============================================================================
A_PARAM = 27.5        # Gy^-1 per cell  (DSB induction slope at L=0)
B_PARAM = 2.43e-3     # (keV/um)^-1
LET = 0.3             # keV/um, low-LET X-rays (200 kVp), used in alpha(L)

# Scaling factors
X1 = 9.19e-7          # M, Ku molar concentration
K8 = 0.552            # h^-1, NHEJ final scaling constant
NA = 6.022e23
V_NUCL = 7.23e-13     # L

# Constant variables (in scaled units, all == x1 == 1.0)
# x1=Ku, x3=DNA-PKcs, x7=LigIV-XRCC4-XLF, x9=PNK, x11=Pol, x15=H2AX
# y1=MRN, y3=ATM, y7=RPA, y9=Rad51-Rad51par-BRCA2 (precursor), y12=DNAinc
# z1=Rad52, z4=ERCC1-XPF, z7=LigIII
# w1=PARP1, w3=Pol, w6=LigI
# NOTE: in the model the SAME symbol y9 is reused with two meanings:
#   (1) y9 as a constant precursor (Rad51-Rad51par-BRCA2 enzyme level), and
#   (2) y9(t) as the dynamic [D-loop+DNAinc] complex (downstream foci-bearing variable)
# Reading Eq. (A5) the dynamic state vector uses y2,y4,y5,y6,y8,y10,y11,y13,y14,y15
# and Eq. (28) defines PHR using y9 as one of these dynamics. We follow the more
# common interpretation: y9_PHR is the time-integrated [Rad51 filament + downstream]
# proxy. We use y11+y13+y14+y15 (Rad51-filament and post-filament foci-bearing complexes)
# as the "Rad51 foci" reporter. y9 in PHR (Eq. 28) is interpreted as y11 (Rad51 filament).

X_CONST = 1.0  # scaled constant concentration for x1,x3,x7,x9,x11,x15 (and y1,y3,y7,y9c,y12,z1,z4,z7,w1,w3,w6)


# --- Rate constants (UNSCALED, in Table A1 units) ----------------------------
K1, Km1   = 11.05,   6.6e-4       # M^-1 h^-1, h^-1
Km2       = 0.526
K3        = 1.86                  # M^-1 h^-1 (note: this is autophosphorylation, first-order in x4)
Km4       = 3.86e-4
K5, Km5   = 15.24,   8.28
K6, Km6   = 18.06,   1.33
K7, Km7   = 2.73e5,  3.20
K9        = 0.166                 # h^-1
K11       = 7.5e-2
K12       = 11.10

P1, Pm1   = 1.75e3,  1.33e-4
P2        = 7.21
P3, Pm3   = 1.37e4,  2.34
P4        = 5.52e-2
P5, Pm5   = 1.20e5,  8.82e-5
P6, Pm6   = 1.87e5,  1.55e-3
P7        = 21.36
P8, Pm8   = 1.20e4,  2.49e-4
P10       = 7.20e-3
P11       = 6.06e-4
P12       = 2.76e-1

Q1, Qm1   = 7.80e3,  1.71e-4
Q2        = 3.00e4
Q3, Qm3   = 6.00e3,  6.06e-4
Q4        = 1.66e-6
Q5, Qm5   = 8.40e4,  4.75e-4
Q6        = 11.58

R1, Rm1   = 2.39e3,  12.63
R2        = 4.07e4
R3        = 9.82
R4, Rm4   = 1.47e5,  2.72
R5        = 0.165


# --- Dose-dependent functions (Table A1) ------------------------------------
def K2_of_D(D):
    """K2(D) = 18.83 * (1.09 - exp(-21.42 / D^1.82))  M^-1 h^-1"""
    D = max(D, 1e-6)
    return 18.83 * (1.09 - math.exp(-21.42 / D**1.82))


def K4_of_D(D):
    """K4(D) = 1.20 + 4.48e5 * exp(-12.70 * D^0.09)  M^-1 h^-1"""
    D = max(D, 1e-6)
    return 1.20 + 4.48e5 * math.exp(-12.70 * D**0.09)


def P9_of_D(D):
    """P9(D) = 1.11 * exp(6.16e-6 / D^2.68 - D^0.03)  h^-1
    Capped to avoid blow-up at very small D where the first term explodes.
    """
    D = max(D, 1e-6)
    arg = 6.16e-6 / D**2.68 - D**0.03
    # Cap argument to avoid overflow at very small D
    arg = min(arg, 50.0)
    return 1.11 * math.exp(arg)


def K10_of_D(D):
    """K10 = 1.93e-7 / Nirrep(D)   M"""
    nr = Nirrep(D)
    return 1.93e-7 / max(nr, 1e-4)


def Nirrep(D):
    """Irreparable fraction of DSBs (Table A1)."""
    if D >= 1.0:
        return 0.01
    return 0.12 * math.exp(-2.48 * D**2.02) - 0.11 * math.exp(-5.43 * D**0.76)


def alpha_of_L(L):
    return A_PARAM * math.exp(-B_PARAM * L)


# --- Scaled rate constants (Appendix C scaling rules) ------------------------
def scaled_rates(D):
    """Compute all dimensionless rate constants for a given dose D (Gy)."""
    s = {}
    # NHEJ (Eq A4)
    s['k1']   = K1 * X1 / K8
    s['km1']  = Km1 / K8
    s['k2']   = K2_of_D(D) * X1 / K8
    s['km2']  = Km2 / K8
    s['k3']   = K3 / K8                # autophosphorylation: first-order in x4
    s['k4']   = K4_of_D(D) * X1 / K8
    s['km4']  = Km4 / K8
    s['k5']   = K5 * X1 / K8
    s['km5']  = Km5 / K8
    s['k6']   = K6 * X1 / K8
    s['km6']  = Km6 / K8
    s['k7']   = K7 * X1 / K8
    s['km7']  = Km7 / K8
    s['k8']   = 1.0                    # by definition (K8/K8)
    s['k9']   = K9 / K8
    s['k10']  = K10_of_D(D) / X1
    s['k11']  = K11 / K8
    s['k12']  = K12 / K8
    # HR (Eq A5)
    s['p1']   = P1 * X1 / K8
    s['pm1']  = Pm1 / K8
    s['p2']   = P2 / K8
    s['p3']   = P3 * X1 / K8
    s['pm3']  = Pm3 / K8
    s['p4']   = P4 / K8
    s['p5']   = P5 * X1 / K8
    s['pm5']  = Pm5 / K8
    s['p6']   = P6 * X1 / K8
    s['pm6']  = Pm6 / K8
    s['p7']   = P7 / K8
    s['p8']   = P8 * X1 / K8
    s['pm8']  = Pm8 / K8
    s['p9']   = P9_of_D(D) / K8        # Table A1 gives P9 = X1/K8 scaled, but the formula in the table is in h^-1 already
    s['p10']  = P10 / K8
    s['p11']  = P11 / K8
    s['p12']  = P12 / K8
    # SSA (Eq A6)
    s['q1']   = Q1 * X1 / K8
    s['qm1']  = Qm1 / K8
    s['q2']   = Q2 * X1 / K8
    s['q3']   = Q3 * X1 / K8
    s['qm3']  = Qm3 / K8
    s['q4']   = Q4 / K8
    s['q5']   = Q5 * X1 / K8
    s['qm5']  = Qm5 / K8
    s['q6']   = Q6 / K8
    # Alt-EJ (Eq A7)
    s['r1']   = R1 * X1 / K8
    s['rm1']  = Rm1 / K8
    s['r2']   = R2 * X1 / K8
    s['r3']   = R3 / K8
    s['r4']   = R4 * X1 / K8
    s['rm4']  = Rm4 / K8
    s['r5']   = R5 / K8
    return s


# ============================================================================
# ODE system  (30 dynamic states, ordered)
# ============================================================================
# State index layout:
#   NHEJ + gamma-H2AX (11): 0=n0, 1=x2, 2=x4, 3=x5, 4=x6, 5=x8, 6=x10, 7=x12, 8=x13, 9=x14
#       (note: x14 = scaled gamma-H2AX foci; we keep x13 = dsDNA for completeness)
#   HR (10): 10=y2, 11=y4, 12=y5, 13=y6, 14=y8, 15=y10, 16=y11, 17=y13, 18=y14, 19=y15
#   SSA (5):  20=z2, 21=z3, 22=z5, 23=z6, 24=z8
#   Alt-EJ (4): 25=w2, 26=w4, 27=w5, 28=w7
# Total = 11 + 10 + 5 + 4 = 30

N_STATES = 30
IDX = {
    'n0':0, 'x2':1, 'x4':2, 'x5':3, 'x6':4, 'x8':5, 'x10':6, 'x12':7, 'x13':8, 'x14':9,
    'y2':10, 'y4':11, 'y5':12, 'y6':13, 'y8':14, 'y10':15, 'y11':16, 'y13':17, 'y14':18, 'y15':19,
    'z2':20, 'z3':21, 'z5':22, 'z6':23, 'z8':24,
    'w2':25, 'w4':26, 'w5':27, 'w7':28,
}
# NOTE: We have 29 dynamic states above. The 30th is x15 (H2AX histone pool) which is held
# constant per paper text. We do NOT add it to state vector. So actual state size = 29.
N_STATES = 29


def rhs(t, u, s, cycle_full=True):
    """ODE right-hand side.
    s: dict of scaled rate constants.
    cycle_full: True for 55% subpopulation (all 4 pathways active),
                False for 45% subpopulation (only NHEJ + Alt-EJ).
    Time t in hours.
    """
    # Unpack
    n0  = u[IDX['n0']]
    x2  = u[IDX['x2']]
    x4  = u[IDX['x4']]
    x5  = u[IDX['x5']]
    x6  = u[IDX['x6']]
    x8  = u[IDX['x8']]
    x10 = u[IDX['x10']]
    x12 = u[IDX['x12']]
    x13 = u[IDX['x13']]
    x14 = u[IDX['x14']]

    y2  = u[IDX['y2']]
    y4  = u[IDX['y4']]
    y5  = u[IDX['y5']]
    y6  = u[IDX['y6']]
    y8  = u[IDX['y8']]
    y10 = u[IDX['y10']]
    y11 = u[IDX['y11']]
    y13 = u[IDX['y13']]
    y14 = u[IDX['y14']]
    y15 = u[IDX['y15']]

    z2 = u[IDX['z2']]
    z3 = u[IDX['z3']]
    z5 = u[IDX['z5']]
    z6 = u[IDX['z6']]
    z8 = u[IDX['z8']]

    w2 = u[IDX['w2']]
    w4 = u[IDX['w4']]
    w5 = u[IDX['w5']]
    w7 = u[IDX['w7']]

    # Constants
    x1 = X_CONST  # Ku, DNA-PKcs, LigIV.., PNK, Pol, H2AX, MRN, ATM, RPA, Rad51-..-BRCA2, DNAinc, Rad52, ERCC1-XPF, LigIII, PARP1, Pol, LigI
    x3 = X_CONST; x7 = X_CONST; x9 = X_CONST; x11 = X_CONST; x15 = X_CONST
    y1 = X_CONST; y3 = X_CONST; y7 = X_CONST; y9c = X_CONST; y12 = X_CONST
    z1 = X_CONST; z4 = X_CONST; z7 = X_CONST
    w1 = X_CONST; w3 = X_CONST; w6 = X_CONST

    # Convenience: a switch off HR/SSA for non-cycling subpopulation
    if not cycle_full:
        # Zero out HR and SSA derivatives (and zero their feedback into Alt-EJ via y6)
        y2 = y4 = y5 = y6 = y8 = y10 = y11 = y13 = y14 = y15 = 0.0
        z2 = z3 = z5 = z6 = z8 = 0.0

    # --- NHEJ + gamma-H2AX (Eq A4) ---
    # dn0/dt = alpha(L)*dD/dt * Nir - n0*(k1*x1 + p1*y1) + km1*x2 + pm1*y2
    #  Here we treat radiation as instantaneous: the source term alpha*dD/dt*Nir is folded into
    #  the initial condition n0(0) = alpha(L)*D * Nirrep(D) / X1 (normalized).
    #  Wild-type IC per paper: n0(0) = alpha(L)*D  (in raw units; here we use scaled n0).
    # Also: for cycle_full=False, the y1 sink term still exists (NHEJ still binds via Ku);
    #  but we have p1*y1*n0 term that competes with k1. In non-HR cells we still allow Ku binding only.
    if cycle_full:
        dn0 = -n0 * (s['k1']*x1 + s['p1']*y1) + s['km1']*x2 + s['pm1']*y2
    else:
        dn0 = -n0 * (s['k1']*x1) + s['km1']*x2

    dx2  = s['k1']*n0*x1 - x2*(s['km1'] + s['k2']*x3) + s['km2']*x4
    dx4  = s['k2']*x2*x3 - x4*(s['k3'] + s['km2'])
    dx5  = s['k3']*x4 - s['k4']*x5*x5 + s['km4']*x6
    # Note Eq A4 dx5: k3*x4 - k4*x5^2 + km4*x6   (paper has dimer bridging => x5^2)
    dx6  = s['k4']*x5*x5 - x6*(s['k5']*x7 + s['km4']) + s['km5']*x8
    # Eq A4 line shown for dx8: dx8 = km6*x10 + k5*x6*x7 - x8*(km5 + k6*x9)
    dx8  = s['km6']*x10 + s['k5']*x6*x7 - x8*(s['km5'] + s['k6']*x9)
    # dx10/dt = km7*x12 + k6*x8*x9 - x10*(km6 + k7*x11)
    dx10 = s['km7']*x12 + s['k6']*x8*x9 - x10*(s['km6'] + s['k7']*x11)
    # dx12/dt = k7*x10*x11 - x12*(k8 + km7)
    dx12 = s['k7']*x10*x11 - x12*(s['k8'] + s['km7'])
    # dx13/dt = k8*x12 + p12*y14 + p11*y15 + q6*z8 + r5*w7    (dsDNA accumulation)
    dx13 = s['k8']*x12 + s['p12']*y14 + s['p11']*y15 + s['q6']*z8 + s['r5']*w7
    # dx14/dt = k9*(x5+x6+x8+x10+x12+y5)*x15 / (k10 + (x5+x6+x8+x10+x12+y5)) - k11*x13 - k12*x14
    #  Per Eq.(25/26), [Sum] includes the y5 ATMP complex (from HR initial steps). We include it.
    sum_active = x5 + x6 + x8 + x10 + x12 + y5
    dx14 = s['k9'] * sum_active * x15 / (s['k10'] + sum_active) - s['k11']*x13 - s['k12']*x14

    # --- HR (Eq A5) ---
    # dy2 = p1*n0*y1 - y2*(pm1 + p3*y4) + pm3*y5
    dy2  = s['p1']*n0*y1 - y2*(s['pm1'] + s['p3']*y4) + s['pm3']*y5
    # dy4 = p2*y3 - y4*(pm2_proxy + p3*y2) + y5*(p4 + pm3)
    #  Paper has y4 dynamics: dy4/dt = p2*y3 - y4*(pm2 + p3*y2) + y5*(p4 + pm3)
    #  But pm2 not defined. We interpret as: dy4 = p2*y3 - y4*(p3*y2) + y5*(p4 + pm3) - p2*y4 (decay back)
    #  Actually rereading paper Eq A5: dy4/dτ = p2 y3 - y4 (p-2 + p3 y2) + y5 (p4 + p-3)
    #  There's a p-2 term but Table A1 has no Pm2. It's a duplicate of the K-2 = 0.526, but for HR's autophosphorylation rev.
    #  We use pm2 = 0 since no value given and ATM autophosphorylation is generally treated as one-way in this paper.
    pm2 = 0.0
    dy4  = s['p2']*y3 - y4*(pm2 + s['p3']*y2) + y5*(s['p4'] + s['pm3'])
    # dy5 = p3*y2*y4 - y5*(p4 + pm3)
    dy5  = s['p3']*y2*y4 - y5*(s['p4'] + s['pm3'])
    # dy6 = p4*y5 - y6*(p5*y7 + r1*w1) + pm5*y8 + rm1*w2
    dy6  = s['p4']*y5 - y6*(s['p5']*y7 + s['r1']*w1) + s['pm5']*y8 + s['rm1']*w2
    # dy8 = pm6*y10 + p5*y6*y7 - y8*(pm5 + p6*y9c + q1*z1) + qm1*z2
    dy8  = s['pm6']*y10 + s['p5']*y6*y7 - y8*(s['pm5'] + s['p6']*y9c + s['q1']*z1) + s['qm1']*z2
    # dy10 = p6*y8*y9c - y10*(p7 + pm6)
    dy10 = s['p6']*y8*y9c - y10*(s['p7'] + s['pm6'])
    # dy11 = p7*y10 - p8*y11*y12 + pm8*y13
    dy11 = s['p7']*y10 - s['p8']*y11*y12 + s['pm8']*y13
    # dy13 = p8*y11*y12 - y13*(p9 + pm8)
    dy13 = s['p8']*y11*y12 - y13*(s['p9'] + s['pm8'])
    # dy14 = p9*y13 - y14*(p10 + p12)
    dy14 = s['p9']*y13 - y14*(s['p10'] + s['p12'])
    # dy15 = p10*y14 - p11*y15
    dy15 = s['p10']*y14 - s['p11']*y15

    # --- SSA (Eq A6) ---
    # dz2 = q1*y8*z1 - z2*(qm1 + q2*z2^2)    (Note: z2 dimer for flap)
    dz2  = s['q1']*y8*z1 - z2*(s['qm1'] + s['q2']*z2*z2)
    # dz3 = q2*z2^2 - q3*z3*z4 + qm3*z5
    dz3  = s['q2']*z2*z2 - s['q3']*z3*z4 + s['qm3']*z5
    # dz5 = q3*z3*z4 - z5*(q4 + qm3)
    dz5  = s['q3']*z3*z4 - z5*(s['q4'] + s['qm3'])
    # dz6 = q4*z5 - q5*z6*z7 + qm5*z8
    dz6  = s['q4']*z5 - s['q5']*z6*z7 + s['qm5']*z8
    # dz8 = q5*z6*z7 - z8*(q6 + qm5)
    dz8  = s['q5']*z6*z7 - z8*(s['q6'] + s['qm5'])

    # --- Alt-EJ (Eq A7) ---
    # dw2 = r1*w1*y6 - w2*(r2 + rm1)
    dw2  = s['r1']*w1*y6 - w2*(s['r2'] + s['rm1'])
    # dw4 = r2*w2*w3 - r3*w4
    dw4  = s['r2']*w2*w3 - s['r3']*w4
    # dw5 = r3*w4 - r4*w5*w6 + rm4*w7
    dw5  = s['r3']*w4 - s['r4']*w5*w6 + s['rm4']*w7
    # dw7 = r4*w5*w6 - w7*(r5 + rm4)
    dw7  = s['r4']*w5*w6 - w7*(s['r5'] + s['rm4'])

    du = np.zeros(N_STATES)
    du[IDX['n0']]  = dn0
    du[IDX['x2']]  = dx2
    du[IDX['x4']]  = dx4
    du[IDX['x5']]  = dx5
    du[IDX['x6']]  = dx6
    du[IDX['x8']]  = dx8
    du[IDX['x10']] = dx10
    du[IDX['x12']] = dx12
    du[IDX['x13']] = dx13
    du[IDX['x14']] = dx14
    du[IDX['y2']]  = dy2
    du[IDX['y4']]  = dy4
    du[IDX['y5']]  = dy5
    du[IDX['y6']]  = dy6
    du[IDX['y8']]  = dy8
    du[IDX['y10']] = dy10
    du[IDX['y11']] = dy11
    du[IDX['y13']] = dy13
    du[IDX['y14']] = dy14
    du[IDX['y15']] = dy15
    du[IDX['z2']]  = dz2
    du[IDX['z3']]  = dz3
    du[IDX['z5']]  = dz5
    du[IDX['z6']]  = dz6
    du[IDX['z8']]  = dz8
    du[IDX['w2']]  = dw2
    du[IDX['w4']]  = dw4
    du[IDX['w5']]  = dw5
    du[IDX['w7']]  = dw7
    return du


def run_one_dose(D_Gy, L=LET, t_max=24.0, n_pts=200, cycle_full=True):
    """Run a single ODE solve from t=0 to t=t_max for a given dose D (Gy).
    Returns (t, U) where U has shape (N_STATES, n_pts).
    """
    s = scaled_rates(D_Gy)
    # Initial conditions: only n0 nonzero.
    # Paper: n0(0) = alpha(L)*D (in raw DSB/cell units); scaled n0 = N0/X1_count_equiv
    # The variables are normalized by X1_molar=9.19e-7 M, which corresponds to
    # N=400000 Ku molecules per cell. So scaled n0(0) = N0_count / 400000.
    N0 = alpha_of_L(L) * D_Gy  # DSBs per cell
    n0_scaled_0 = N0 / 400000.0
    u0 = np.zeros(N_STATES)
    u0[IDX['n0']] = n0_scaled_0
    t_eval = np.linspace(0.0, t_max, n_pts)
    sol = solve_ivp(
        rhs, (0.0, t_max), u0, t_eval=t_eval, args=(s, cycle_full),
        method='LSODA', rtol=1e-8, atol=1e-12, max_step=0.5,
    )
    if not sol.success:
        raise RuntimeError(f"ODE failed at D={D_Gy} Gy: {sol.message}")
    return sol.t, sol.y, N0


def gamma_h2ax_foci_per_cell(U, N0):
    """Convert scaled x14 back to absolute foci/cell.
    Paper normalizes x14 = X14_molar / X1_molar; X1 corresponds to 400000 molecules/cell.
    So foci/cell = x14 * 400000. But this is histone-pool units. The visible foci-count
    is typically the number of DSBs being processed, not the number of phosphorylated histones.
    We follow the paper convention that x14*X1_count == 'foci-count proxy' for plotting.
    """
    return U[IDX['x14'], :] * 400000.0


def rad51_foci_per_cell(U, N0):
    """Rad51 foci proxy: y11 (Rad51 filament) + y13 + y14 + y15 (downstream)."""
    s = U[IDX['y11'], :] + U[IDX['y13'], :] + U[IDX['y14'], :] + U[IDX['y15'], :]
    return s * 400000.0


def main():
    here = Path(__file__).resolve().parent
    root = here.parent
    res_dir = root / "results"
    fig_dir = root / "figures"
    res_dir.mkdir(exist_ok=True)
    fig_dir.mkdir(exist_ok=True)

    t0 = time.time()
    doses_mGy = np.array([20, 40, 80, 160, 250, 500, 1000])
    doses_Gy = doses_mGy / 1000.0
    T_END = 24.0
    N_PTS = 200

    # Cell-cycle weights
    W_CYCLE = 0.55  # late-S/G2/M (HR-competent)
    W_NO    = 0.45  # G0/G1/early-S (HR-suppressed)

    h2ax_all = {}   # per-dose foci/cell time-course (population-averaged)
    rad51_all = {}
    t_grid = None

    print("Running 7-dose time-course solves (full + reduced subpopulations)...")
    for D_mGy, D_Gy in zip(doses_mGy, doses_Gy):
        t, U_full,  N0 = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=True)
        _, U_red,   _  = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=False)
        h2ax = W_CYCLE * gamma_h2ax_foci_per_cell(U_full, N0) + W_NO * gamma_h2ax_foci_per_cell(U_red, N0)
        rad51 = W_CYCLE * rad51_foci_per_cell(U_full, N0)  # Rad51 only in cycling cells
        h2ax_all[D_mGy] = h2ax
        rad51_all[D_mGy] = rad51
        t_grid = t
        peak_h2ax = float(np.max(h2ax))
        t_peak_h2ax = float(t[np.argmax(h2ax)])
        resid_h2ax = float(h2ax[-1])
        peak_r51 = float(np.max(rad51))
        t_peak_r51 = float(t[np.argmax(rad51)])
        resid_r51 = float(rad51[-1])
        print(f"  D={D_mGy:>4} mGy: N0={N0:6.2f} DSB/cell | gH2AX peak={peak_h2ax:7.2f} @ t={t_peak_h2ax:.2f}h, 24h={resid_h2ax:6.2f} "
              f"| Rad51 peak={peak_r51:7.2f} @ t={t_peak_r51:.2f}h, 24h={resid_r51:6.3f}")

    # Save kinetics CSVs
    import csv
    with open(res_dir / "ode_h2ax_kinetics.csv", "w", newline="") as f:
        w = csv.writer(f)
        header = ["t_h"] + [f"D_{d}_mGy" for d in doses_mGy]
        w.writerow(header)
        for i, t in enumerate(t_grid):
            row = [f"{t:.4f}"] + [f"{h2ax_all[d][i]:.4f}" for d in doses_mGy]
            w.writerow(row)
    with open(res_dir / "ode_rad51_kinetics.csv", "w", newline="") as f:
        w = csv.writer(f)
        header = ["t_h"] + [f"D_{d}_mGy" for d in doses_mGy]
        w.writerow(header)
        for i, t in enumerate(t_grid):
            row = [f"{t:.4f}"] + [f"{rad51_all[d][i]:.4f}" for d in doses_mGy]
            w.writerow(row)
    print(f"Wrote {res_dir/'ode_h2ax_kinetics.csv'}")
    print(f"Wrote {res_dir/'ode_rad51_kinetics.csv'}")

    # PHR(D) sweep
    print("\nRunning PHR(D) sweep on 25 dose points (full cycle subpopulation only)...")
    dose_sweep_mGy = np.array([5, 10, 20, 40, 60, 80, 120, 160, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000])
    PHR_vals = []
    for D_mGy in dose_sweep_mGy:
        D_Gy = D_mGy / 1000.0
        t, U_full, N0 = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=True)
        h2ax_t = gamma_h2ax_foci_per_cell(U_full, N0)
        rad51_t = rad51_foci_per_cell(U_full, N0)
        # Time-average (mean over 0-24h)
        mean_h2ax = float(np.trapezoid(h2ax_t, t) / T_END)
        mean_r51  = float(np.trapezoid(rad51_t, t) / T_END)
        # PHR = 100 * mean(Rad51) / mean(gH2AX) per Eq 28/29
        if mean_h2ax > 1e-12:
            phr = 100.0 * mean_r51 / mean_h2ax
        else:
            phr = float('nan')
        PHR_vals.append(phr)
        print(f"  D={D_mGy:>4} mGy: mean(gH2AX)={mean_h2ax:7.3f} mean(Rad51)={mean_r51:7.3f} PHR={phr:6.2f}%")

    # Save PHR CSV
    with open(res_dir / "ode_PHR_vs_dose.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mGy", "PHR_percent"])
        for d, p in zip(dose_sweep_mGy, PHR_vals):
            w.writerow([d, f"{p:.4f}"])
    print(f"Wrote {res_dir/'ode_PHR_vs_dose.csv'}")

    # Compute summary metrics for PROMO_RESULT
    PHR_arr = np.array(PHR_vals)
    # Find PHR at 20 mGy and 1000 mGy
    phr_at_20  = float(PHR_arr[np.where(dose_sweep_mGy == 20)[0][0]])
    phr_at_1000 = float(PHR_arr[np.where(dose_sweep_mGy == 1000)[0][0]])
    # Check monotonic decrease (allowing small noise)
    decreasing_segments = int(np.sum(np.diff(PHR_arr) < 0))
    total_segments = len(PHR_arr) - 1
    monotonic_frac = decreasing_segments / total_segments
    PHR_ratio_20_over_1000 = phr_at_20 / max(phr_at_1000, 1e-6)

    # Peak-timing shift check (paper claims shift between 250 and 500 mGy)
    peak_times = {}
    for d in doses_mGy:
        peak_times[int(d)] = float(t_grid[int(np.argmax(h2ax_all[d]))])
    peak_shift_present = (peak_times[1000] <= peak_times[250]) or (peak_times[500] <= peak_times[250])

    # Residual gH2AX at 24h: paper says elevated for 40-80 mGy vs control, suppressed for 500-1000
    # We don't have a true 'control' in this model (n0(0)=0 yields zero foci);
    # we measure absolute 24h-foci normalized to peak to see the residual fraction.
    residual_frac = {}
    for d in doses_mGy:
        peak = float(np.max(h2ax_all[d]))
        r24  = float(h2ax_all[d][-1])
        residual_frac[int(d)] = (r24 / peak) if peak > 1e-9 else float('nan')

    # Bundle results.json
    results = {
        "doses_mGy": doses_mGy.tolist(),
        "h2ax_peak_per_cell": {int(d): float(np.max(h2ax_all[d])) for d in doses_mGy},
        "h2ax_peak_time_h":   {int(d): float(t_grid[int(np.argmax(h2ax_all[d]))]) for d in doses_mGy},
        "h2ax_residual_24h":  {int(d): float(h2ax_all[d][-1]) for d in doses_mGy},
        "rad51_peak_per_cell":{int(d): float(np.max(rad51_all[d])) for d in doses_mGy},
        "rad51_peak_time_h":  {int(d): float(t_grid[int(np.argmax(rad51_all[d]))]) for d in doses_mGy},
        "rad51_residual_24h": {int(d): float(rad51_all[d][-1]) for d in doses_mGy},
        "residual_h2ax_frac_of_peak": residual_frac,
        "PHR_sweep": {
            "dose_mGy": dose_sweep_mGy.tolist(),
            "PHR_percent": [float(p) for p in PHR_vals],
        },
        "PHR_at_20_mGy": phr_at_20,
        "PHR_at_1000_mGy": phr_at_1000,
        "PHR_decrease_ratio_20_over_1000": PHR_ratio_20_over_1000,
        "PHR_monotonic_decreasing_fraction": monotonic_frac,
        "peak_timing_shift_present": bool(peak_shift_present),
        "wall_clock_s": time.time() - t0,
    }
    with open(root / "results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {root/'results.json'}")
    print(f"Total wall-clock: {time.time()-t0:.1f} s")

    # Plot
    if plt is not None:
        fig, axes = plt.subplots(2, 2, figsize=(12, 9))
        # Panel A: gH2AX kinetics, low doses
        for d in [20, 40, 80]:
            axes[0,0].plot(t_grid, h2ax_all[d], label=f"{d} mGy")
        axes[0,0].set_xlabel("Time post-IR (h)")
        axes[0,0].set_ylabel("gamma-H2AX foci / cell (model)")
        axes[0,0].set_title("Fig 5 analog (low doses 20-80 mGy)")
        axes[0,0].legend(); axes[0,0].grid(alpha=0.3)

        # Panel B: gH2AX kinetics, high doses
        for d in [160, 250, 500, 1000]:
            axes[0,1].plot(t_grid, h2ax_all[d], label=f"{d} mGy")
        axes[0,1].set_xlabel("Time post-IR (h)")
        axes[0,1].set_ylabel("gamma-H2AX foci / cell (model)")
        axes[0,1].set_title("Fig 5 analog (160-1000 mGy)")
        axes[0,1].legend(); axes[0,1].grid(alpha=0.3)

        # Panel C: Rad51 kinetics, all doses
        for d in doses_mGy:
            axes[1,0].plot(t_grid, rad51_all[d], label=f"{d} mGy")
        axes[1,0].set_xlabel("Time post-IR (h)")
        axes[1,0].set_ylabel("Rad51 foci / cell (model)")
        axes[1,0].set_title("Fig 6 analog (Rad51 kinetics)")
        axes[1,0].legend(fontsize=8); axes[1,0].grid(alpha=0.3)

        # Panel D: PHR(D)
        axes[1,1].plot(dose_sweep_mGy, PHR_vals, 'o-', color='C3')
        axes[1,1].set_xlabel("Dose (mGy)")
        axes[1,1].set_ylabel("PHR (%)  = 100 * mean(Rad51) / mean(gH2AX) over 24h")
        axes[1,1].set_title("Fig 7 analog: PHR(D) shift")
        axes[1,1].grid(alpha=0.3)

        fig.suptitle("Belov et al. 2023 CIMB — full ODE replication (29 states, scipy LSODA)", fontsize=12)
        fig.tight_layout()
        out_png = fig_dir / "ode_full_model.png"
        fig.savefig(out_png, dpi=130)
        print(f"Wrote {out_png}")

if __name__ == "__main__":
    main()
