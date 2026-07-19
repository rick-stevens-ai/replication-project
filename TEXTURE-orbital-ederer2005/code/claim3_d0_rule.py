#!/usr/bin/env python3
"""
Claim 3 (the "d0 rule", central physics claim of the review, Intro + Ref.[5,14,15,16]):

"conventional ferroelectricity in perovskite oxides involves a transition-metal B
cation with a formal d0 electron configuration ... for magnetism a partially filled
d shell is indispensable" -> chemical incompatibility explains scarcity of
magnetoelectric multiferroics.

MECHANISM (second-order/pseudo Jahn-Teller, a.k.a. vibronic coupling): the B-cation
off-centering (ferroelectric distortion) is driven by hybridization between EMPTY
metal d states and FILLED oxygen 2p states. If the d shell is EMPTY (d0), the
bonding p-d combination created by off-centering is fully occupied and the anti-
bonding one empty -> net energy LOWERING -> spontaneous off-center (ferroelectric).
If the d states are OCCUPIED (d^n, n>0, needed for magnetism), the antibonding
p-d combination also fills -> the energy gain is cancelled -> no ferroelectric
instability. This is the microscopic content of the d0 rule.

We capture it with a minimal 2-level (one O-2p + one metal-d) vibronic model and
compute the total electronic energy vs off-center displacement Q for different d
occupations n_d in {0,1,2}. A ferroelectric double well (energy minimum at Q != 0)
should appear ONLY for d0.

Two-level Hamiltonian at displacement Q (off-centering turns on hybridization ~ g*Q):
    H(Q) = [[ e_p ,  g*Q ],
            [ g*Q ,  e_d ]]
plus an elastic restoring cost (1/2) k Q^2 for the lattice.
e_p = O-2p level (filled, lower), e_d = metal-d level (higher), g = vibronic coupling.
Electronic energy = sum over occupied MOs; fill 2 electrons in the p-derived level
always (O 2p full), plus n_d electrons in the d-derived level.
"""
import numpy as np

e_p, e_d = -3.0, 0.0      # eV, O2p below metal-d
g  = 1.6                  # eV/Angstrom vibronic coupling
k  = 2.2                  # eV/Angstrom^2 elastic stiffness

def levels(Q):
    H = np.array([[e_p, g*Q],[g*Q, e_d]])
    w,_ = np.linalg.eigh(H)   # w[0]=bonding (p-like), w[1]=antibonding (d-like)
    return w

def total_energy(Q, n_d):
    """Elastic + electronic. O2p contributes 2 e in bonding level always.
       n_d extra electrons go into the antibonding (d-derived) level."""
    wb, wa = levels(Q)
    E_el = 2*wb + n_d*wa      # bonding doubly occupied; d-electrons in antibonding
    E_elastic = 0.5*k*Q**2
    return E_el + E_elastic

Qs = np.linspace(-2.0, 2.0, 801)
print("d_occ  E(Q=0)    min E     Q*_at_min   double_well?")
summary = {}
for n_d in [0,1,2]:
    Es = np.array([total_energy(Q,n_d) for Q in Qs])
    imin = np.argmin(Es)
    Qstar = Qs[imin]
    E0 = total_energy(0.0,n_d)
    Emin = Es[imin]
    well_depth = E0 - Emin
    double_well = (abs(Qstar) > 1e-3) and (well_depth > 1e-3)
    print(f"  d{n_d}   {E0:+7.3f}  {Emin:+7.3f}   {Qstar:+6.3f}     "
          f"{'YES' if double_well else 'no ':>3}  (well depth {well_depth:.3f} eV)")
    summary[f"d{n_d}"] = {"Qstar": round(float(Qstar),3),
                          "well_depth_eV": round(float(well_depth),3),
                          "ferroelectric": bool(double_well)}

print("\nInterpretation:")
print(" d0 -> off-center energy minimum (ferroelectric double well): CONVENTIONAL FE.")
print(" d1,d2 -> minimum stays at Q=0: filling the antibonding p-d state cancels the")
print("          energy gain -> NO ferroelectric instability. == the d0 rule.")
print(" A cation needs empty d (FE) OR partly-filled d (magnetism), not both -> the")
print(" chemical incompatibility that makes magnetoelectric multiferroics rare.")

import json
print("\nJSON:", json.dumps(summary))
