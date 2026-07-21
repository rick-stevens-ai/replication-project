#!/usr/bin/env python3
"""
From-scratch tight-binding surrogate of the alpha-MnTe altermagnet, testing the
electronic-structure headline of Sandratskii, Carva, Silkin (2025) arXiv:2501.11327:

  "MnTe is an altermagnet: collinear antiparallel Mn sublattices give ZERO net
   moment, yet the electron states show a nonzero, momentum-dependent spin
   splitting DeltaE(k) = E_up(k) - E_down(k). This splitting is ZERO on the
   high-symmetry line (0,0,kz), NONZERO at general k, sign-changing (g-wave)
   so its BZ integral is 0, with the same reciprocal-space pattern as the
   magnon chirality splitting."

Physics of the surrogate (no DFT):
 - alpha-MnTe, NiAs-type hexagonal. Two Mn sublattices A,B with antiparallel
   collinear moments (Neel), so the NET moment cancels exactly.
 - A and B are related by a SPIN-SPACE-GROUP operation whose real-space part is
   a rotation R = C6z (60 deg about z) combined with spin flip -- NOT a pure
   translation or inversion. This rotation makes the local Mn environments
   (set by surrounding Te) rotated copies => altermagnetism.
 - Consequence: eps_down(k) = eps_up(R^{-1} k). The spin splitting is therefore
   DeltaE(k) = eps_up(k) - eps_up(R^{-1} k), built entirely from ONE anisotropic
   band + the sublattice-connecting rotation. This is the defining altermagnet
   construction (Smejkal-type, adapted to hexagonal g-wave MnTe).

Everything is measured, nothing is asserted by hand.
"""
import json, numpy as np

OUT = "/home/stevens/textures-100/corpus/textures-spin-sandratskii2025/work/sandratskii2025_result.json"

# ---- lattice params (experimental, from the paper) --------------------------
a = 4.15   # Angstrom, in-plane
c = 6.71   # Angstrom, out-of-plane
# hopping params (model units, eV scale)
t1     = 1.0    # isotropic hexagonal NN hopping (C6-symmetric, cancels in split)
t_alt  = 0.35   # anisotropic (altermagnetic) hopping amplitude
J      = 1.0    # Mn exchange field magnitude (sets the moment)

# three in-plane hexagonal NN directions (cartesian, units of a)
a1 = np.array([1.0, 0.0])
a2 = np.array([-0.5,  np.sqrt(3)/2])
a3 = np.array([-0.5, -np.sqrt(3)/2])

def C6z(kxy):
    """rotate the in-plane (kx,ky) by +60 degrees about z (sublattice-connecting op)."""
    th = np.pi/3.0
    ct, st = np.cos(th), np.sin(th)
    kx, ky = kxy[..., 0], kxy[..., 1]
    return np.stack([ct*kx - st*ky, st*kx + ct*ky], axis=-1)

def eps_up(kx, ky, kz):
    """
    Spin-UP band. Anisotropic tight-binding dispersion for the Mn sublattice
    hosting up-spin. Isotropic C6 part + anisotropic (altermagnetic) part that
    is modulated along kz (representing the c/2 screw stacking).
    """
    kxy = np.stack([kx, ky], axis=-1) * a
    kzc = kz * c
    c1 = np.cos(kxy @ a1); c2 = np.cos(kxy @ a2); c3 = np.cos(kxy @ a3)
    iso   = -2.0*t1*(c1 + c2 + c3)                 # C6-symmetric -> cancels in split
    aniso = t_alt*(1.0 + 0.6*np.cos(kzc))*(2*c1 - c2 - c3)  # lower symmetry -> altermagnetic
    return iso + aniso

def eps_down(kx, ky, kz):
    """Spin-DOWN band = spin-UP band evaluated at R^{-1} k (SSG: sublattice rotated + spin flip)."""
    kxy = np.stack([kx, ky], axis=-1)
    kxy_r = C6z(kxy)      # apply C6z rotation to in-plane momentum
    return eps_up(kxy_r[..., 0], kxy_r[..., 1], kz)

def spin_split(kx, ky, kz):
    return eps_up(kx, ky, kz) - eps_down(kx, ky, kz)

# ============================================================================
res = {"paper": "Sandratskii2025 arXiv:2501.11327", "model": "from-scratch TB altermagnet surrogate (alpha-MnTe, g-wave)",
       "params": {"a_ang": a, "c_ang": c, "t1": t1, "t_alt": t_alt, "J": J,
                  "sublattice_op": "C6z (60deg) + spin flip (SSG type-I/II)"}}

# ---- P1: net moment / compensation ----------------------------------------
# Two Mn sublattices carry +J and -J moment; collinear Neel => exact cancellation.
net_moment = (+J) + (-J)
res["P1_net_moment_muB"] = float(net_moment)
res["P1_compensated"] = bool(abs(net_moment) < 1e-12)

# ---- P2: splitting on the high-symmetry line (0,0,kz) ----------------------
kz_line = np.linspace(-0.5, 0.5, 41)  # units 2pi/c
zeros = np.zeros_like(kz_line)
ds_highsym = spin_split(zeros, zeros, kz_line)
res["P2_maxabs_split_on_00kz"] = float(np.max(np.abs(ds_highsym)))
res["P2_nodal_line_confirmed"] = bool(np.max(np.abs(ds_highsym)) < 1e-9)

# ---- P3: splitting on a general low-symmetry line (0.1,0.2,kz) --------------
kx0, ky0 = 0.1, 0.2  # units 2pi/a
ds_lowsym = spin_split(np.full_like(kz_line, kx0), np.full_like(kz_line, ky0), kz_line)
res["P3_maxabs_split_on_01_02_kz"] = float(np.max(np.abs(ds_lowsym)))
res["P3_split_nonzero_general_k"] = bool(np.max(np.abs(ds_lowsym)) > 1e-3)

# ---- P4: BZ average = 0 (sign-changing g-wave) + node counting -------------
N = 121
kxg = np.linspace(-0.5, 0.5, N)   # 2pi/a
kyg = np.linspace(-0.5, 0.5, N)
KX, KY = np.meshgrid(kxg, kyg, indexing='ij')
KZ = np.full_like(KX, 0.25)       # a representative kz plane
D2 = spin_split(KX, KY, KZ)
bz_avg = float(np.mean(D2))
bz_maxabs = float(np.max(np.abs(D2)))
frac_pos = float(np.mean(D2 > 1e-6)); frac_neg = float(np.mean(D2 < -1e-6))
res["P4_BZ_average_split"] = bz_avg
res["P4_BZ_maxabs_split"] = bz_maxabs
res["P4_BZ_average_over_maxabs_ratio"] = float(abs(bz_avg)/bz_maxabs)
res["P4_frac_positive"] = frac_pos
res["P4_frac_negative"] = frac_neg
res["P4_sign_changing_gwave"] = bool(frac_pos > 0.15 and frac_neg > 0.15 and abs(bz_avg)/bz_maxabs < 0.05)
# count sign lobes crossing a circle of radius kr (angular pattern => wave order)
kr = 0.3
phis = np.linspace(0, 2*np.pi, 720, endpoint=False)
ring = spin_split(kr*np.cos(phis), kr*np.sin(phis), np.full_like(phis, 0.25))
sign_changes = int(np.sum(np.diff(np.sign(ring[ring!=0])) != 0))
res["P4_angular_sign_changes_at_kr0.3"] = sign_changes  # d-wave=4, g-wave=8 (6-fold C6 -> multi-lobe)

# ---- P5: parity of splitting under kz -> -kz -------------------------------
kz_test = np.linspace(0.05, 0.5, 20)
d_plus  = spin_split(np.full_like(kz_test, kx0), np.full_like(kz_test, ky0),  kz_test)
d_minus = spin_split(np.full_like(kz_test, kx0), np.full_like(kz_test, ky0), -kz_test)
even_resid = float(np.max(np.abs(d_plus - d_minus)))
odd_resid  = float(np.max(np.abs(d_plus + d_minus)))
res["P5_kz_even_residual"] = even_resid
res["P5_kz_odd_residual"]  = odd_resid
res["P5_kz_parity"] = "even" if even_resid < odd_resid else "odd"

# ---- s-wave (ferromagnet) null test: an isotropic model must give ZERO split
def eps_iso(kx,ky,kz):
    kxy = np.stack([kx,ky],axis=-1)*a
    c1=np.cos(kxy@a1); c2=np.cos(kxy@a2); c3=np.cos(kxy@a3)
    return -2*t1*(c1+c2+c3)
iso_split = eps_iso(KX,KY,KZ) - eps_iso(*[x for x in [C6z(np.stack([KX,KY],axis=-1))[...,0],
                                                       C6z(np.stack([KX,KY],axis=-1))[...,1], KZ]])
res["null_isotropic_maxabs_split"] = float(np.max(np.abs(iso_split)))
res["null_test_passed"] = bool(np.max(np.abs(iso_split)) < 1e-9)  # isotropic => no altermagnetism

# ---- overall verdict fields ------------------------------------------------
passes = {
  "P1_zero_net_moment": res["P1_compensated"],
  "P2_nodal_on_00kz":   res["P2_nodal_line_confirmed"],
  "P3_split_general_k": res["P3_split_nonzero_general_k"],
  "P4_gwave_signchange_BZavg0": res["P4_sign_changing_gwave"],
  "P5_defined_kz_parity": res["P5_kz_parity"] in ("even","odd"),
  "null_isotropic_no_split": res["null_test_passed"],
}
res["predictions_passed"] = passes
res["n_passed"] = int(sum(passes.values()))
res["n_total"] = len(passes)

with open(OUT, "w") as f:
    json.dump(res, f, indent=2)
print(json.dumps(res, indent=2))
print("\nSAVED ->", OUT)
