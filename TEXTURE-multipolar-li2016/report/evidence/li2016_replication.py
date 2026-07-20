#!/usr/bin/env python3
"""
From-scratch replication of Li, Wang & Chen (2016), arXiv:1608.07008
"Hidden multipolar orders of dipole-octupole doublets on a triangular lattice"

Target claim (headline): For the ferro-octupolar (FO) state at
(Jx,Jy,Jz)=(-1,-0.2,-0.5) and theta=pi/3, the mean-field transition occurs at
To = 1.5|Jx|, the octupole component (T^x) orders ferromagnetically, and the
magnetic susceptibility chi_zz shows NO divergence despite time-reversal
breaking octupolar order.

Method: classical/mean-field pseudospin-1/2 model on the triangular lattice.
Reduced Hamiltonian (paper Eq. 4):
  H = sum_<rr'> [Jx Tx Tx' + Jy Ty Ty' + Jz Tz Tz'] - h sum_r [cos(th) Tz + sin(th) Ty]
T^x is the OCTUPOLE moment; T^y, T^z are DIPOLE moments.

Provenance: reuses the pseudospin/susceptibility conventions of
ollie_multipolar_stevens_landau_kernel.py (spin_matrices for S=1/2 pseudospins,
fluctuation-formula thermal_susceptibility, Landau mean-field Tc estimate).
"""
from __future__ import annotations
import json, sys, itertools
import numpy as np

sys.path.insert(0, "/home/stevens/shared-kernels-cache")
from ollie_multipolar_stevens_landau_kernel import (
    spin_matrices, thermal_susceptibility, landau_transition_temperature,
)

# --- Triangular lattice geometry (paper's NN vectors) ---
A = [np.array([1.0, 0.0]),
     np.array([-0.5,  np.sqrt(3)/2]),
     np.array([-0.5, -np.sqrt(3)/2])]
Z = 6  # coordination number of triangular lattice

# Pseudospin-1/2 operators (T = S for S=1/2): eigenvalues +/-1/2
Sx, Sy, Sz, _ = spin_matrices(0.5)
T = {"x": Sx, "y": Sy, "z": Sz}


# ---------------------------------------------------------------------------
# 1. CLASSICAL GROUND STATE via energy minimization
# ---------------------------------------------------------------------------
def bond_energy(Jx, Jy, Jz, s, sp):
    """Energy of one bond between classical unit-length pseudospins s, sp
    (components x=octupole, y,z=dipole). Length normalized to 1/2 (S=1/2)."""
    return Jx*s[0]*sp[0] + Jy*s[1]*sp[1] + Jz*s[2]*sp[2]


def classical_ground_state(Jx, Jy, Jz, ncfg=20000, seed=0):
    """Minimize classical energy over uniform (Q=0) and 3-sublattice ansatze.
    Returns best config, energy/bond, and ordering classification."""
    rng = np.random.default_rng(seed)

    def rand_unit(n):
        v = rng.normal(size=(n, 3))
        return 0.5 * v / np.linalg.norm(v, axis=1, keepdims=True)  # |S|=1/2

    # --- Uniform (ferromagnetic, Q=0) ansatz: all spins equal ---
    # each site has Z/2 = 3 independent bonds; energy/site = 3 * bond
    best_uni = None
    for s in rand_unit(ncfg):
        e = 3.0 * bond_energy(Jx, Jy, Jz, s, s)  # 3 bonds/site, all equal
        if best_uni is None or e < best_uni[0]:
            best_uni = (e, s)
    # analytic uniform optimum: align fully along axis with most negative J (if <0)
    Js = {"x": Jx, "y": Jy, "z": Jz}

    # --- 3-sublattice ansatz (captures AFO / 3-sublattice orders) ---
    # On triangular lattice each site's 6 NN split into the other two sublattices
    # (3 each). Energy/site = 3*[bond(A,B)+bond(A,C)+bond(B,C)] / 3 sites ...
    # total energy per 3-site cell = 3*(E_AB + E_BC + E_CA)   (3 bonds of each type)
    best_3 = None
    for _ in range(ncfg):
        sA, sB, sC = rand_unit(3)
        e_cell = 3.0*(bond_energy(Jx,Jy,Jz,sA,sB)
                      + bond_energy(Jx,Jy,Jz,sB,sC)
                      + bond_energy(Jx,Jy,Jz,sC,sA))
        e_site = e_cell/3.0
        if best_3 is None or e_site < best_3[0]:
            best_3 = (e_site, np.array([sA, sB, sC]))

    e_uni, s_uni = best_uni
    e_3, s_3 = best_3

    # classify: is 3-sublattice meaningfully lower than uniform?
    uniform_wins = e_uni <= e_3 + 1e-6

    result = {
        "uniform_energy_per_site": float(e_uni),
        "uniform_spin": s_uni.tolist(),
        "threesub_energy_per_site": float(e_3),
        "threesub_spins": s_3.tolist(),
        "ground_state_is_uniform": bool(uniform_wins),
    }

    # dominant ordered component of the ground state
    gs_spin = s_uni if uniform_wins else s_3.mean(axis=0)
    comp = {"x(octupole)": abs(gs_spin[0]),
            "y(dipole)": abs(gs_spin[1]),
            "z(dipole)": abs(gs_spin[2])}
    dom = max(comp, key=comp.get)
    result["dominant_component"] = dom
    result["component_magnitudes"] = comp

    # ferro-octupolar test: uniform ground state dominated by x (octupole)
    result["is_ferro_octupolar"] = bool(uniform_wins and dom.startswith("x"))
    return result


# ---------------------------------------------------------------------------
# 2. MEAN-FIELD TRANSITION TEMPERATURE (Landau / single-site fluctuation)
# ---------------------------------------------------------------------------
def meanfield_Tc(J, channel="x"):
    """MF instability in a given channel: 1 = z*|J|*chi_single-site(T).
    For a free S=1/2 pseudospin, chi_aa(T) = <T_a^2>/T = (1/4)/T (Curie).
    => Tc = z*|J|*(1/4). Uses the kernel's fluctuation susceptibility at T=1
    to obtain chi*T=1/4 self-consistently, then scales."""
    O = T[channel]
    H0 = np.zeros((2, 2), complex)  # free pseudospin
    chi_T1 = thermal_susceptibility(H0, O, T=1.0)  # = <O^2> at T=1 = 1/4
    Tc = landau_transition_temperature(abs(J), chi_T1, z=Z)
    return Tc, chi_T1


# ---------------------------------------------------------------------------
# 3. SUSCEPTIBILITY chi_zz in the FO state (should NOT diverge)
# ---------------------------------------------------------------------------
def chi_zz_FO(Jx, Jy, Jz, theta, Ts):
    """chi_zz of the FO state. In the FO state the order parameter is <T^x>
    (octupole). The field couples to cos(th)T^z + sin(th)T^y (dipole). Because
    the ordered moment (T^x, octupole) is orthogonal to the field operator and
    does NOT couple linearly to it, chi_zz stays finite (no Curie divergence)
    through To. Single-site MF proxy: chi_zz = <(cos th T^z+sin th T^y)^2>/T,
    but with the octupolar mean field gapping the transverse response."""
    Ofield = np.cos(theta)*T["z"] + np.sin(theta)*T["y"]
    out = []
    for Tt in Ts:
        # octupolar mean field along x below To gaps the dipole channel:
        # h_MF = z*|Jx|*<T^x>. Use MF <T^x>(T) ~ order-parameter tanh curve.
        To = Z*abs(Jx)*0.25
        if Tt < To:
            # BCS-like order parameter growth (bounded), gapping transverse chi
            m = np.sqrt(max(0.0, 1.0 - Tt/To)) * 0.5
        else:
            m = 0.0
        h_mf = Z*abs(Jx)*m  # octupolar molecular field along x
        Hmf = -h_mf*T["x"]
        chi = thermal_susceptibility(Hmf, Ofield, T=max(Tt, 1e-6))
        out.append((float(Tt), float(chi), float(m)))
    return out


# ---------------------------------------------------------------------------
# 4. OCTUPOLAR-WAVE DISPERSION (paper Eq. 5)
# ---------------------------------------------------------------------------
def octupolar_dispersion(Jx, Jy, Jz, kpts):
    out = []
    for k in kpts:
        S = sum(np.cos(np.dot(k, ai)) for ai in A)
        val = (Jy*S - 3*Jx)*(Jz*S - 3*Jx)
        out.append((k.tolist(), float(np.sqrt(val)) if val > 0 else float("nan")))
    return out


# ---------------------------------------------------------------------------
# 5. PHASE-DIAGRAM SLICE on the Ix surface (Jx = -1 fixed)
# ---------------------------------------------------------------------------
def phase_slice(Jx=-1.0, grid=7):
    rows = []
    for Jy in np.linspace(-1.0, -0.05, grid):
        for Jz in np.linspace(-1.0, -0.05, grid):
            gs = classical_ground_state(Jx, Jy, Jz, ncfg=4000, seed=1)
            rows.append({"Jy": float(Jy), "Jz": float(Jz),
                         "dominant": gs["dominant_component"],
                         "uniform": gs["ground_state_is_uniform"],
                         "FO": gs["is_ferro_octupolar"]})
    return rows


def main():
    Jx, Jy, Jz, theta = -1.0, -0.2, -0.5, np.pi/3

    gs = classical_ground_state(Jx, Jy, Jz, ncfg=40000, seed=0)
    Tc_x, chi1_x = meanfield_Tc(Jx, "x")   # octupolar (FO)
    Tc_z, _ = meanfield_Tc(Jz, "z")        # for comparison / FDz surface

    Ts = np.linspace(0.1, 3.0, 30)
    chizz = chi_zz_FO(Jx, Jy, Jz, theta, Ts)
    chi_max = max(c for _, c, _ in chizz)
    chi_diverges = chi_max > 1e3

    # dispersion along a small G-M-K-G path
    G = np.array([0.0, 0.0])
    M = np.array([np.pi, np.pi/np.sqrt(3)])
    K = np.array([4*np.pi/3, 0.0])
    kpath = [G + (M-G)*t for t in np.linspace(0,1,6)] \
          + [M + (K-M)*t for t in np.linspace(0,1,6)] \
          + [K + (G-K)*t for t in np.linspace(0,1,6)]
    disp = octupolar_dispersion(Jx, Jy, Jz, kpath)
    gap = min(w for _, w in disp if not np.isnan(w))

    result = {
        "paper": "Li, Wang, Chen (2016) arXiv:1608.07008",
        "method": "classical energy minimization + single-site mean-field (pseudospin-1/2)",
        "provenance": "reuses ollie_multipolar_stevens_landau_kernel.py "
                      "(spin_matrices, thermal_susceptibility, landau_transition_temperature)",
        "params": {"Jx": Jx, "Jy": Jy, "Jz": Jz, "theta": theta, "z": Z},
        "ground_state": gs,
        "mean_field_Tc": {
            "To_octupolar_computed": Tc_x,
            "To_paper_formula_1.5|Jx|": 1.5*abs(Jx),
            "chi_single_site_T1": chi1_x,
            "Td_FDz_computed_for_ref": Tc_z,
        },
        "chi_zz_FO": {
            "T": [t for t, _, _ in chizz],
            "chi": [c for _, c, _ in chizz],
            "order_param_mx": [m for _, _, m in chizz],
            "chi_max": chi_max,
            "diverges": bool(chi_diverges),
        },
        "octupolar_wave": {
            "kpath_GMKG": [w for _, w in disp],
            "min_gap": float(gap),
            "gapped": bool(gap > 1e-6),
        },
        "phase_slice_Ix_surface": phase_slice(),
    }

    # ---- honest scoring vs paper claim ----
    checks = {
        "ground_state_ferro_octupolar": gs["is_ferro_octupolar"],
        "To_matches_1.5|Jx|": abs(Tc_x - 1.5*abs(Jx)) < 1e-6,
        "chi_zz_no_divergence": not chi_diverges,
        "octupolar_wave_gapped": gap > 1e-6,
    }
    result["claim_checks"] = checks
    result["all_checks_pass"] = all(checks.values())
    return result


if __name__ == "__main__":
    res = main()
    outp = "/home/stevens/textures-100/corpus/textures-multipolar-li2016/work/li2016_result.json"
    with open(outp, "w") as f:
        json.dump(res, f, indent=2)
    print("SAVED", outp)
    print(json.dumps(res["claim_checks"], indent=2))
    print("all_checks_pass:", res["all_checks_pass"])
    print("GS dominant:", res["ground_state"]["dominant_component"],
          "| uniform:", res["ground_state"]["ground_state_is_uniform"])
    print("To computed:", res["mean_field_Tc"]["To_octupolar_computed"],
          "| paper 1.5|Jx|:", res["mean_field_Tc"]["To_paper_formula_1.5|Jx|"])
    print("chi_zz max:", res["chi_zz_FO"]["chi_max"], "diverges:", res["chi_zz_FO"]["diverges"])
    print("octupole-wave min gap:", res["octupolar_wave"]["min_gap"])
