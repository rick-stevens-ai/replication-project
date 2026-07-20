#!/usr/bin/env python3
"""
Replication of Gurung et al. (2023) "Nearly Perfect Spin Polarization of
Noncollinear Antiferromagnets" (Mn3GaN).

FROM-SCRATCH tight-binding surrogate of the paper's Fig. 1 illustrative model:
a 2D KAGOME lattice with a 120-degree (Gamma_5g-like) noncollinear AFM texture,
one orbital per atom, spin-independent nearest-neighbor hopping t, and an
on-site exchange splitting Delta aligned with each sublattice's local moment:

    H(k) = H_hop(k) (x) I_2   +   (Delta/2) * sum_i P_i (x) (m_i . sigma)

- 3 kagome sublattices (A,B,C) x 2 spin  => 6 bands (matches paper: "six bands").
- m_A,m_B,m_C = in-plane 120-deg directions (noncollinear AFM), breaking P.T and
  T.t so bands are spin-split without SOC (the paper's key symmetry point).

EFFECTIVE MOMENTUM-DEPENDENT SPIN POLARIZATION (paper Eqs. 1-2):
Transport along x; conserved transverse momentum k|| = ky. For fixed (ky, E_F)
we find all conduction channels = Fermi crossings E_n(kx)=E_F along kx, take the
spin expectation s_n = <psi_n|sigma/2|psi_n> (3-vector) of each, and form

    s_k||   = sum_n s_n
    p_k||   = |s_k||| / sum_n |s_n|          (Eq. 2)

p_k|| = 100% when all channel spins are parallel OR only one channel exists.
We verify the headline: nearly 100% spin polarization over a BROAD area of the
(ky, E_F) map (paper Fig. 1c, Delta/t = 1.5).

Credit: physics/structure informed by the shared Textures-100 kernels
(gobel2024_sd_skyrmion_kubo_Lz_kernel.py s-d lattice pattern; loop_current_kagome
kagome-geometry pattern). Written from scratch for this noncollinear-AFM model.
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))

# Pauli matrices
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

# ---------------- Kagome geometry ----------------
# Lattice vectors (a=1)
a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, np.sqrt(3)/2])
# Sublattice positions (A,B,C): midpoints of the honeycomb bonds
rA = np.array([0.0, 0.0])
rB = 0.5 * a1
rC = 0.5 * a2
pos = [rA, rB, rC]

# Nearest-neighbor bond vectors between sublattices (each pair has 2 NN bonds).
# For kagome, each site has 4 NN. Build inter-sublattice NN displacement lists.
# A-B bonds: dr and dr - a1 ; A-C bonds: dr and dr - a2 ; B-C bonds: (rC-rB) and (rC-rB)+a1-a2
def nn_bonds():
    dAB = [rB - rA, rB - rA - a1]
    dAC = [rC - rA, rC - rA - a2]
    dBC = [rC - rB, rC - rB - a1 + a2]
    return {(0, 1): dAB, (0, 2): dAC, (1, 2): dBC}

BONDS = nn_bonds()

# ---------------- Noncollinear 120-deg AFM moments (in-plane, Gamma_5g-like) ----------------
def moments(chi=1.0):
    """3 in-plane unit vectors at 120 deg. chi flips chirality (Neel-vector sense)."""
    angs = np.array([90.0, 210.0, 330.0]) * np.pi/180.0  # 120-deg apart, in xy-plane
    if chi < 0:
        angs = angs[::-1]
    m = np.array([[np.cos(a), np.sin(a), 0.0] for a in angs])
    return m  # shape (3,3)

def m_dot_sigma(mvec):
    return mvec[0]*sx + mvec[1]*sy + mvec[2]*sz

# ---------------- Bloch Hamiltonian ----------------
def H_of_k(kx, ky, t=1.0, Delta=1.5, chi=1.0):
    """6x6 spinful Bloch Hamiltonian. Basis order: (subl, spin) = A up,A dn,B up,..."""
    k = np.array([kx, ky])
    H = np.zeros((6, 6), dtype=complex)
    # Hopping (spin-independent): -t sum over NN bonds
    for (i, j), drs in BONDS.items():
        hij = 0.0 + 0.0j
        for dr in drs:
            hij += -t * np.exp(1j * np.dot(k, dr))
        # place 2x2 spin block
        H[2*i:2*i+2, 2*j:2*j+2] += hij * I2
        H[2*j:2*j+2, 2*i:2*i+2] += np.conj(hij) * I2
    # On-site exchange splitting along local moment
    m = moments(chi)
    for i in range(3):
        H[2*i:2*i+2, 2*i:2*i+2] += (Delta/2.0) * m_dot_sigma(m[i])
    # Hermitize (guard)
    H = 0.5 * (H + H.conj().T)
    return H

def spin_expect(vec):
    """Spin expectation (sx,sy,sz)/2 for a 6-component eigenvector (spinful, 3 subl)."""
    v = vec.reshape(3, 2)  # (subl, spin)
    s = np.zeros(3)
    for i in range(3):
        u = v[i]
        s[0] += np.real(np.vdot(u, sx @ u))
        s[1] += np.real(np.vdot(u, sy @ u))
        s[2] += np.real(np.vdot(u, sz @ u))
    return 0.5 * s  # spin-1/2 units

# ---------------- Effective spin polarization p_k||(ky, EF) ----------------
def spin_pol_map(t=1.0, Delta=1.5, chi=1.0, nky=41, nkx=601, nEF=41,
                 EF_range=(-2.2, 2.2)):
    """For transport along x, k||=ky. Returns arrays ky_vals, EF_vals, P[nEF,nky]."""
    ky_vals = np.linspace(-np.pi, np.pi, nky)      # ky in units of 1/a (BZ ~ +-pi)
    EF_vals = np.linspace(EF_range[0], EF_range[1], nEF)
    kx_vals = np.linspace(-np.pi, np.pi, nkx)
    P = np.full((nEF, nky), np.nan)
    Nchan = np.zeros((nEF, nky))

    for iy, ky in enumerate(ky_vals):
        # Precompute bands & spins along kx for this ky
        Ekx = np.zeros((nkx, 6))
        Skx = np.zeros((nkx, 6, 3))
        for ix, kx in enumerate(kx_vals):
            w, V = np.linalg.eigh(H_of_k(kx, ky, t, Delta, chi))
            Ekx[ix] = w
            for n in range(6):
                Skx[ix, n] = spin_expect(V[:, n])
        # For each EF, find Fermi crossings along kx (channels)
        for ie, EF in enumerate(EF_vals):
            svecs = []
            for n in range(6):
                d = Ekx[:, n] - EF
                sign = np.sign(d)
                idx = np.where(np.diff(sign) != 0)[0]
                for ix in idx:
                    # linear interp fraction
                    f = d[ix] / (d[ix] - d[ix+1]) if (d[ix]-d[ix+1]) != 0 else 0.5
                    sv = (1-f)*Skx[ix, n] + f*Skx[ix+1, n]
                    svecs.append(sv)
            if len(svecs) == 0:
                continue
            svecs = np.array(svecs)
            s_tot = svecs.sum(axis=0)
            denom = np.sum(np.linalg.norm(svecs, axis=1))
            p = np.linalg.norm(s_tot)/denom if denom > 1e-9 else np.nan
            P[ie, iy] = p
            Nchan[ie, iy] = len(svecs)
    return ky_vals, EF_vals, P, Nchan


def main():
    t_hop, Delta = 1.0, 1.5   # paper: Delta/t = 1.5
    # Band-structure sanity: 6 bands, spin-split (noncollinear AFM, no SOC)
    ks = np.linspace(-np.pi, np.pi, 200)
    bands = np.array([np.linalg.eigvalsh(H_of_k(k, 0.0, t_hop, Delta)) for k in ks])
    nbands = bands.shape[1]

    # Check spin splitting: are bands non-degenerate away from high symmetry?
    kx_t, ky_t = 0.7, 0.3
    w = np.linalg.eigvalsh(H_of_k(kx_t, ky_t, t_hop, Delta))
    gaps = np.diff(np.sort(w))
    max_pairwise_deg = float(np.min(gaps))  # small => degenerate somewhere

    # Spin polarization map
    ky_vals, EF_vals, P, Nchan = spin_pol_map(t_hop, Delta, nky=41, nkx=601, nEF=41)

    valid = ~np.isnan(P)
    Pv = P[valid]
    frac_ge_90 = float(np.mean(Pv >= 0.90)) if Pv.size else 0.0
    frac_ge_95 = float(np.mean(Pv >= 0.95)) if Pv.size else 0.0
    frac_ge_99 = float(np.mean(Pv >= 0.99)) if Pv.size else 0.0
    mean_p = float(np.mean(Pv)) if Pv.size else 0.0
    median_p = float(np.median(Pv)) if Pv.size else 0.0

    # "Broad area" metric: fraction of (ky,EF) cells with a Fermi surface that are >=90%
    # Restrict to EF away from band bottom (paper: reduced only at small EF)
    hi_ef = EF_vals >= -0.5
    Phi = P[np.ix_(hi_ef, np.ones(len(ky_vals), bool))]
    vhi = ~np.isnan(Phi)
    frac_hi_ge_90 = float(np.mean(Phi[vhi] >= 0.90)) if vhi.any() else 0.0

    max_p = float(np.nanmax(P)) if valid.any() else 0.0

    result = {
        "paper": "gurung2023",
        "title": "Nearly Perfect Spin Polarization of Noncollinear Antiferromagnets (Mn3GaN)",
        "model": "from-scratch 2D kagome tight-binding, 120-deg noncollinear AFM (Gamma_5g-like), one orbital/atom, NN hopping t, on-site exchange Delta",
        "params": {"t": t_hop, "Delta": Delta, "Delta_over_t": Delta/t_hop,
                   "n_sublattice": 3, "n_spin": 2, "n_bands": nbands},
        "headline_claim": "Mn3GaN / noncollinear AFM exhibits nearly 100% spin polarization in a broad area of the Fermi surface.",
        "band_structure_check": {
            "n_bands": int(nbands),
            "expected_bands": 6,
            "bands_match": bool(nbands == 6),
            "spin_split_no_SOC": bool(max_pairwise_deg > 1e-4),
            "min_pairwise_gap_at_generic_k": max_pairwise_deg,
        },
        "spin_polarization": {
            "definition": "p_k|| = |sum_n s_n| / sum_n |s_n| over Fermi-crossing conduction channels (Eq.2), transport along x, k||=ky",
            "grid": {"nky": 41, "nkx": 601, "nEF": 41, "EF_range": [-2.2, 2.2]},
            "max_p": max_p,
            "mean_p": mean_p,
            "median_p": median_p,
            "frac_cells_p_ge_0.90": frac_ge_90,
            "frac_cells_p_ge_0.95": frac_ge_95,
            "frac_cells_p_ge_0.99": frac_ge_99,
            "frac_cells_p_ge_0.90_EF_above_-0.5": frac_hi_ge_90,
            "n_valid_cells": int(Pv.size),
        },
        "headline_verification": {
            "nearly_100pct_reached": bool(max_p >= 0.99),
            "broad_area_ge_90pct": bool(frac_hi_ge_90 >= 0.5),
            "verdict_basis": "max p ~1.0 and >=90% polarization over broad (ky,EF) region away from band bottom",
        },
        "runtime_sec": round(time.time()-t0, 2),
    }
    return result


if __name__ == "__main__":
    res = main()
    out = os.path.join(HERE, "gurung2023_result.json")
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    print("\nSaved:", out)
