#!/usr/bin/env python3
"""
Exchange splitting of the Gamma8 ground quartet in ordered NpO2, within the
effective Jeff=3/2 pseudospin model of Pourovskii & Khmelevskyi
(arXiv:2009.08908).

Claim tested (RESULTS / excitation section):
  The multipolar order lifts the Gamma8 (Jeff=3/2) quartet degeneracy into a
  singlet - doublet - singlet scheme:
     GS  = Gamma5 singlet     (E = 0)
     1st = doublet            (E = 6.1 meV)   [INS peak ~6.4 meV]
     2nd = singlet            (E = 12.2 meV)
  The paper (and Santini 2006, ref 24) analyze this with a DIAGONAL UNIFORM SEI
  between the three Gamma5 (t2g) triakontadipole moments of the Gamma8 quartet.

Minimal tractable model (this script):
  - Jeff=3/2 pseudospin (4-dim Gamma8 quartet), operators from J=3/2 algebra.
  - The three Gamma5 (yz, xz, xy) time-odd rank-3 (octupole/triakontadipole-like)
    operators for J=3/2, built as the standard symmetrized cubic operators:
        T_yz = (sqrt3/2) * sym( Jx, {Jy,Jz} )   ... i.e. overline{ Jx Jy Jz }-type
    For a spin-3/2 the Gamma5 triad reduces to the three components
        Txyz-family: O_yz ~ overline{Jx Jy Jz} projected on yz, etc.
    We use the standard Santini/Shiina definitions:
        Txyz  = (sqrt15/6) * overline{Jx Jy Jz}
        T_a^b (Gamma5) = sqrt15/6 * overline{ J_a (J_b^2 - J_c^2) }   (rank3, G5)
    The Gamma5 triad {T_x^(yz), T_y^(zx), T_z^(xy)} are the three time-odd
    triakontadipole pseudo-operators. Here for J=3/2 the equivalent compact
    Gamma5 triad is:
        G_yz = overline{Jx (Jy^2 - Jz^2)}
        G_zx = overline{Jy (Jz^2 - Jx^2)}
        G_xy = overline{Jz (Jx^2 - Jy^2)}
    (fully symmetrized products; these transform as the Gamma5 t2g triad and are
    time-odd, i.e. the pseudospin triakontadipoles.)

  - 3k mean-field order: equal self-consistent field on all three components
    (uniform diagonal SEI), field along [111] in triad space:
        H_MF = -h (G_yz + G_zx + G_xy)
    Diagonalize -> Gamma8 quartet splits.

Machine-checkable predictions:
  (P1) degeneracy pattern is 1-2-1 (singlet-doublet-singlet).
  (P2) ratio E(upper singlet)/E(doublet) is a PARAMETER-FREE number fixed by the
       operator algebra; compare to paper 12.2/6.1 = 2.00.
"""
import numpy as np
from itertools import permutations
from cf_j92 import angular_momentum_ops

Jx,Jy,Jz,Jp,Jm,dim = angular_momentum_ops(1.5)   # 4-dimensional Jeff=3/2
I4 = np.eye(4,dtype=complex)

def symprod(mats):
    """fully symmetrized product over all permutations of a list of matrices"""
    perms=list(permutations(range(len(mats))))
    acc=np.zeros((4,4),dtype=complex)
    for p in perms:
        m=I4.copy()
        for idx in p: m=m@mats[idx]
        acc+=m
    return acc/len(perms)

Jx2,Jy2,Jz2 = Jx@Jx, Jy@Jy, Jz@Jz

# Gamma5 (t2g) time-odd rank-3 triad for J=3/2:
#   G_yz = overline{ Jx (Jy^2 - Jz^2) } , cyclic
def G(a, b2, c2):
    return symprod([a, b2 - c2])
Gyz = G(Jx, Jy2, Jz2)
Gzx = G(Jy, Jz2, Jx2)
Gxy = G(Jz, Jx2, Jy2)

def hermit(M): return 0.5*(M+M.conj().T)

def levels(H):
    ev=np.sort(np.linalg.eigvalsh(hermit(H)).real); ev-=ev[0]
    groups=[]; cur=[ev[0]]
    for e in ev[1:]:
        if abs(e-cur[-1])<1e-6: cur.append(e)
        else: groups.append((float(np.mean(cur)),len(cur))); cur=[e]
    groups.append((float(np.mean(cur)),len(cur)))
    return ev,groups

def report(label, Hmf):
    ev,groups=levels(Hmf)
    seq="-".join({1:"S",2:"D",3:"T",4:"Q"}.get(d,str(d)) for _,d in groups)
    print(f"\n[{label}]")
    print(f"  degeneracy sequence: {seq}")
    for e,d in groups:
        nm={1:"singlet",2:"doublet",3:"triplet",4:"quartet"}.get(d,f"deg{d}")
        print(f"     E={e:+.4f} (arb)  {nm}")
    if [d for _,d in groups]==[1,2,1]:
        Ed=groups[1][0]; Es=groups[2][0]
        print("  ** 1-2-1 singlet-doublet-singlet CONFIRMED **")
        ratio=Es/Ed
        print(f"  ratio E(upper singlet)/E(doublet) = {ratio:.4f}")
        scale=6.1/Ed
        print(f"  scaled to doublet=6.1 meV -> upper singlet = {Es*scale:.2f} meV")
        print(f"     paper: doublet 6.1 meV, upper singlet 12.2 meV (ratio 2.00)")
        return ratio
    return None

print("="*72)
print("Gamma8 (Jeff=3/2) exchange splitting under 3k Gamma5-triakontadipole SEI")
print("(diagonal uniform SEI, 3k order = equal field on all three Gamma5 comps)")
print("="*72)

# 3k uniform field along [111] of the Gamma5 triad space:
Hmf_3k = -(Gyz+Gzx+Gxy)
r_3k = report("3k order: -(Gyz+Gzx+Gxy)  [field along 111 in triad space]", Hmf_3k)

# For comparison: single-component (1k) order -- expect different pattern
Hmf_1k = -(Gzx)
report("1k order: -Gzx only (single triakontadipole component)", Hmf_1k)

print("\n"+"="*72)
print("SUMMARY")
print("="*72)
if r_3k is not None:
    print(f"3k Gamma5-triakontadipole order reproduces the SINGLET-DOUBLET-SINGLET")
    print(f"lifting of the Gamma8 quartet, with fixed ratio "
          f"upper-singlet/doublet = {r_3k:.3f}.")
    print(f"Paper value 12.2/6.1 = 2.000.")
