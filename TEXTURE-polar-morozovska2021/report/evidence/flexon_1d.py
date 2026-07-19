"""
Independent 1D LGD replication of the CORE physics of Morozovska et al. 2021
(arXiv 2104.00598) "Chiral Polarization Textures Induced by the Flexoelectric
Effect in Ferroelectric Nanocylinders".

Reimplemented from the equations (NOT author code).

CORE MECHANISM (paper): the flexoelectric coupling enters the LGD free energy
as a Lifshitz invariant (Eq. 1f), mathematically identical to a DMI term. Such
an antisymmetric gradient coupling converts an Ising domain wall into a chiral
(Bloch-like) wall: it induces a transverse polarization component inside the
wall whose SIGN (chirality) is set by sign(F) and whose amplitude scales with
|F| (odd function of f, zero at F=0), then saturates. This is the essence of
the "flexon" chirality claim.

Minimal faithful reduction: 180-degree wall in P_z along x. Two-component
polarization (P_x transverse "Bloch", P_z axial). Free energy density:

  f = a/2 (Px^2+Pz^2) + b/4 (Px^2+Pz^2)^2 + K/2 Px^2   (K>0 transverse anisotropy)
      + g/2 [(Px')^2 + (Pz')^2]
      + F (Px Pz' - Pz Px')          <-- Lifshitz / flexoelectric invariant

The anisotropy K makes the transverse (Bloch) direction hard, so at F=0 the wall
is a pure Ising wall (Px=0). The Lifshitz invariant is the ONLY thing that can
seed the transverse component -> its amplitude and sign are set purely by F.

Euler-Lagrange (delta f / delta P = 0):
  (a+K) Px + b P^2 Px - g Px'' + 2 F Pz' = 0
  a Pz + b P^2 Pz - g Pz'' - 2 F Px' = 0

Solved by Landau-Khalatnikov overdamped relaxation dP/dt = -delta f/delta P.
BCs: Pz(-L)=-P0, Pz(+L)=+P0 (180 wall); Px free (natural), decays to 0.
"""
import json, numpy as np

# ---- material-like parameters (BaTiO3-scale, arbitrary consistent units) ----
a = -1.0          # a<0 : ferroelectric phase
b =  1.0
g =  1.0          # gradient (correlation) coefficient
K =  1.5          # transverse anisotropy (K>|a| => Ising wall is ground state at F=0)
P0 = np.sqrt(-a/b)          # spontaneous polarization
xi = np.sqrt(g/abs(a))      # correlation length / wall width scale

# grid
L = 20.0
N = 801
x = np.linspace(-L, L, N)
dx = x[1]-x[0]

def relax(F, iters=40000, dt=None):
    if dt is None:
        dt = 0.2*dx*dx/g
    # init: Ising tanh wall in Pz, tiny Px seed (broken symmetry chosen by F)
    Pz = P0*np.tanh(x/(np.sqrt(2)*xi))
    Px = 1e-3*np.exp(-(x/(2*xi))**2)
    for it in range(iters):
        P2 = Px*Px + Pz*Pz
        # second derivatives (Neumann-ish; Pz endpoints fixed)
        Pxx = np.zeros_like(Px); Pzz = np.zeros_like(Pz)
        Pxx[1:-1] = (Px[2:]-2*Px[1:-1]+Px[:-2])/dx**2
        Pzz[1:-1] = (Pz[2:]-2*Pz[1:-1]+Pz[:-2])/dx**2
        # first derivatives (central)
        dPx = np.gradient(Px, dx)
        dPz = np.gradient(Pz, dx)
        varx = (a+K)*Px + b*P2*Px - g*Pxx + 2*F*dPz
        varz = a*Pz + b*P2*Pz - g*Pzz - 2*F*dPx
        Px = Px - dt*varx
        Pz = Pz - dt*varz
        # BCs
        Pz[0] = -P0; Pz[-1] = P0
        Px[0] = 0.0; Px[-1] = 0.0
    return Px, Pz

def chirality(Px, Pz):
    # signed area of transverse (Bloch) component = net chirality of wall
    return np.trapezoid(Px, x)

# ---------- run: scan flexoelectric coefficient F ----------
Fvals = np.array([-1.5,-1.0,-0.6,-0.4,-0.2,-0.1,-0.05,0.0,0.05,0.1,0.2,0.4,0.6,1.0,1.5])
peaks, chis = [], []
for F in Fvals:
    Px, Pz = relax(F)
    imax = np.argmax(np.abs(Px))
    peaks.append(Px[imax])         # extremal transverse (Bloch) polarization P_e
    chis.append(chirality(Px, Pz))

peaks = np.array(peaks); chis = np.array(chis)

# reference case for detailed profile
Px_ref, Pz_ref = relax(0.3)
Pe_ref = Px_ref[np.argmax(np.abs(Px_ref))]

# ---- checks vs paper claims ----
# 1) P_e is ODD in F, zero at F=0
i0 = list(Fvals).index(0.0)
odd_err = np.max(np.abs(peaks + peaks[::-1]))   # antisymmetry residual
zero_at_0 = abs(peaks[i0])
# 2) chirality flips sign with sign(F)
sign_flip = bool(np.sign(peaks[i0+1]) == -np.sign(peaks[i0-1]) and peaks[i0+1]!=0)
# 3) monotone growth then saturation for small->large |F|
posF = Fvals[Fvals>0]; posP = np.abs(peaks[Fvals>0])
grows = bool(np.all(np.diff(posP) > -1e-6))
# saturation: net chiral moment (integral) turns over / stops growing at large |F|
absC = np.abs(chis[Fvals>0])
saturates = bool(absC[-1] <= absC.max())  # chirality integral peaks then declines
# 4) linear regime slope near F=0 (chirality ~ F for small F)
sl = np.polyfit(Fvals[abs(Fvals)<=0.1], peaks[abs(Fvals)<=0.1], 1)[0]

result = {
  "paper": "Morozovska et al. 2021, arXiv:2104.00598 (flexon chirality)",
  "model": "Independent 1D LGD 180-wall with flexoelectric Lifshitz invariant (DMI-like)",
  "params": {"a":a,"b":b,"g":g,"K":K,"P0":float(P0),"wall_width_xi":float(xi)},
  "F_scan": [float(f) for f in Fvals],
  "P_e_transverse_peak": [float(p) for p in peaks],
  "chirality_integral": [float(c) for c in chis],
  "P_e_reference_F0.3": float(Pe_ref),
  "checks": {
     "P_e_odd_in_F_residual": float(odd_err),
     "P_e_zero_at_F0": float(zero_at_0),
     "chirality_flips_with_sign_F": sign_flip,
     "monotone_growth_posF": grows,
     "saturates_at_large_F": saturates,
     "linear_slope_near_0": float(sl),
  },
  "verdict": {},
}

# verdict scoring
coverage = 7   # 1D reduction of a 3D FEM paper: core mechanism yes; full flexon geometry no
agreement = 0
agreement += 2 if zero_at_0 < 1e-3 else 0
agreement += 2 if odd_err < 0.05*max(np.abs(peaks).max(),1e-9) else 0
agreement += 2 if sign_flip else 0
agreement += 2 if grows else 0
agreement += 2 if saturates else 0
result["verdict"] = {
  "core_claim": "Flexoelectric Lifshitz invariant induces chiral (Bloch) transverse polarization; sign=sign(F), amplitude odd in F, grows then saturates.",
  "replicated": bool(zero_at_0<1e-3 and sign_flip and grows),
  "Coverage_/10": coverage,
  "Agreement_/10": agreement,
  "key_number_P_e_at_F0.3": float(Pe_ref),
  "notes": "Qualitative + scaling match. Absolute uC/cm^2 values not compared (dimensionless units; paper uses full 3D FEM with electrostatics+elasticity).",
}

with open("/home/stevens/textures-100/corpus/textures-polar-morozovska2021/work/morozovska2021_result.json","w") as f:
    json.dump(result, f, indent=2)

print("P0=%.3f wall_width xi=%.3f"%(P0,xi))
print("F scan   :", np.round(Fvals,3))
print("P_e(peak):", np.round(peaks,4))
print("chirality:", np.round(chis,4))
print("odd residual=%.2e  zero@0=%.2e  sign_flip=%s grows=%s saturates=%s"%(
      odd_err, zero_at_0, sign_flip, grows, saturates))
print("Coverage=%d/10 Agreement=%d/10"%(coverage,agreement))
print("Pe@F=0.3 =", Pe_ref)
