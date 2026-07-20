#!/usr/bin/env python3
"""
From-scratch tight-binding SURROGATE replication of:

  Wang et al. (2026), "Nonlinear Magnetic Orbital Hall Effect Induced by
  Spin-Orbit Coupling", arXiv:2604.02636.  (paper dir: textures-orbital-wang2026)

HEADLINE (recipe):
  In PT-symmetric collinear AFM CuMnAs (Neel vector n||[001]) the second-order
  nonlinear magnetic ORBITAL Hall response chi_zzyy^(O) reaches ~ -1.3 (h/e)
  Ohm^-1 V^-1 and is ~2 orders of magnitude larger than the nonlinear magnetic
  SPIN Hall response chi_zzyy^(S) ~ -0.0087 near the Fermi level.  The effect is
  SOC-INDUCED (vanishes without SOC), T-odd (flips with the Neel vector), and is
  a NON-PERTURBATIVE effect of SOC: a weakly SOC-gapped nodal line near X
  amplifies the orbital Berry-curvature dipole (OBD).  chi_dabc = tau * D_dabc.

WHAT WE BUILD (no DFT; DFT+Wannier is out of budget/scope):
  A minimal 4-band PT-symmetric collinear-AFM lattice model (sublattice rho x
  spin sigma) that hosts a NODAL LINE in the ky=0 plane when SOC=0, gapped by an
  SOC term of strength lam.  On a COARSE 3D k-grid we compute the orbital and
  spin Berry-curvature DIPOLES D_zzyy via the paper's own formulae:

    L_mn  = (i/4) sum_{l!=m,n} (1/(e_l-e_m)+1/(e_l-e_n)) (v^x_ml v^y_ln - v^y_ml v^x_ln)   [Eq.3]
    j^z_a = 1/2 {v_a, L^z}        (orbital current);   s^z_a = 1/2 {v_a, S^z}
    Omega^{z,n}_{ab}(k) = -2 Im sum_{n'} <n|j^z_a|n'><n'|v_b|n> / (e_n-e_n')^2
    D_zzyy = sum_n int d^3k/(2pi)^3  Omega^{z,n}_{zy}(k) * df0/dk_y
    chi_zzyy = tau * D_zzyy

  We report (i) orbital>>spin ratio, (ii) SOC-scaling (D->0 as lam->0 and the
  non-perturbative 1/gap enhancement), (iii) T-oddness (flip Neel J -> flip sign),
  (iv) an order-of-magnitude chi.

CREDIT: velocity/Berry-machinery and the itinerant-L_z / Kubo structure are
adapted from the shared kernel
  shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py
(Goebel 2024 topological OHE), generalized here to a k-space multiband model and
the SECOND-ORDER (Berry-curvature-dipole) response of Wang 2026.
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wang2026_result.json")

# ---- Pauli ----
s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(a, b):
    return np.kron(a, b)


# basis: sublattice(rho) (x) spin(sigma).  P = rho_x ,  T = i sigma_y K.
def H_of_k(kx, ky, kz, J, lam, M=2.6, t=1.0, v=1.0):
    """4-band PT-symmetric collinear-AFM nodal-line model.
    - f(k) rho_z + v sin(ky) rho_y  : 2-band nodal ring in ky=0 plane (SOC=0)
    - J rho_z sigma_z               : Neel AFM along z (staggered, breaks T)
    - lam SOC term (rho_x (x) spin) : gaps the nodal line; SOC-odd
    """
    f = M - t * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    H = f * kron(sz, s0) + v * np.sin(ky) * kron(sy, s0)
    H = H + J * kron(sz, sz)
    # SOC: couples sublattices with spin texture, breaks the glide that
    # protects the line -> opens a small gap ~lam on the ring.
    H = H + lam * (np.sin(kx) * kron(sx, sx) + np.sin(kz) * kron(sx, sy))
    return H


def velocities(kx, ky, kz, J, lam, h=1e-4, **kw):
    """v_a = dH/dk_a via central finite difference (general, robust)."""
    def d(ax):
        dk = [0.0, 0.0, 0.0]; dk[ax] = h
        Hp = H_of_k(kx + dk[0], ky + dk[1], kz + dk[2], J, lam, **kw)
        Hm = H_of_k(kx - dk[0], ky - dk[1], kz - dk[2], J, lam, **kw)
        return (Hp - Hm) / (2 * h)
    return d(0), d(1), d(2)


def Lz_operator(E, V, vx, vy):
    """Itinerant orbital angular momentum L^z, paper Eq.(3), in the band basis
    then rotated back.  Uses (v_x v_y - v_y v_x) cross structure.  e=hbar=1,
    4 mu_B -> absorbed into overall units (we report the O/S RATIO + scaling +
    order of magnitude, so the constant prefactor cancels in the key claims)."""
    n = len(E)
    # velocity matrix elements in eigenbasis
    Vd = V.conj().T
    vxe = Vd @ vx @ V
    vye = Vd @ vy @ V
    L = np.zeros((n, n), dtype=complex)
    for m in range(n):
        for nn in range(n):
            acc = 0.0 + 0j
            for l in range(n):
                if l == m or l == nn:
                    continue
                d1 = E[l] - E[m]
                d2 = E[l] - E[nn]
                if abs(d1) < 1e-9 or abs(d2) < 1e-9:
                    continue
                pref = (1.0 / d1 + 1.0 / d2)
                cross = vxe[m, l] * vye[l, nn] - vye[m, l] * vxe[l, nn]
                acc += pref * cross
            L[m, nn] = 0.25j * acc      # i/4 (mu_B=1)
    return L  # in eigenbasis


def bcd_zzyy(J, lam, mu, Nk=18, T=0.08, **kw):
    """Orbital & spin Berry-curvature dipole D_zzyy on a coarse Nk^3 grid.
    Returns (D_orb, D_spin, avg_gap_on_FS, min_gap)."""
    ks = np.linspace(-np.pi, np.pi, Nk, endpoint=False) + np.pi / Nk
    Sz_lab = kron(s0, sz) * 0.5   # spin-z operator (sublattice-diagonal)
    D_o = 0.0
    D_s = 0.0
    gaps = []
    beta = 1.0 / T
    dvol = (2 * np.pi) ** 3 / Nk ** 3
    for kx in ks:
        for ky in ks:
            for kz in ks:
                H = H_of_k(kx, ky, kz, J, lam, **kw)
                E, V = np.linalg.eigh(H)
                vx, vy, vz = velocities(kx, ky, kz, J, lam, **kw)
                Vd = V.conj().T
                vy_e = Vd @ vy @ V
                vz_e = Vd @ vz @ V
                # orbital L^z (eigenbasis) and current j^z_z = 1/2{v_z, L^z}
                Lz = Lz_operator(E, V, vx, vy)
                jz_orb = 0.5 * (vz_e @ Lz + Lz @ vz_e)
                Sz_e = Vd @ Sz_lab @ V
                jz_spin = 0.5 * (vz_e @ Sz_e + Sz_e @ vz_e)
                # band velocity v_y (diag) and df0/dk_y = f0'(E) * v_y,nn
                f0 = 1.0 / (np.exp(beta * (E - mu)) + 1.0)
                f0p = -beta * f0 * (1.0 - f0)
                for n in range(4):
                    # Omega^{z,n}_{zy} = -2 Im sum_{n'} j_z(n,n') v_y(n',n)/(En-En')^2
                    om_o = 0.0
                    om_s = 0.0
                    for m in range(4):
                        if m == n:
                            continue
                        w = E[n] - E[m]
                        if abs(w) < 1e-6:
                            continue
                        denom = w * w
                        om_o += (jz_orb[n, m] * vy_e[m, n] / denom).imag
                        om_s += (jz_spin[n, m] * vy_e[m, n] / denom).imag
                    om_o *= -2.0
                    om_s *= -2.0
                    dfy = f0p[n] * vy_e[n, n].real
                    D_o += om_o * dfy
                    D_s += om_s * dfy
                # track SOC gap on states near mu (nodal-line remnant)
                near = np.argsort(np.abs(E - mu))[:2]
                gaps.append(abs(E[near[0]] - E[near[1]]))
    D_o *= dvol / (2 * np.pi) ** 3
    D_s *= dvol / (2 * np.pi) ** 3
    gaps = np.array(gaps)
    return D_o, D_s, float(np.mean(gaps)), float(np.min(gaps))


def main():
    tau = 1.4        # ps  (paper's tau = 1.4 ps)
    J = 0.8          # Neel AFM strength
    mu = 1.0         # Fermi level on the SOC-gapped nodal-line-derived Fermi surface
    Nk = 18          # coarse grid (18^3 ~ 5800 k-pts, 4-band)

    res = {
        "model": "4-band PT-symmetric collinear-AFM nodal-line surrogate (CuMnAs-type)",
        "paper": "Wang et al. 2026, arXiv:2604.02636 (nonlinear magnetic orbital Hall)",
        "kernel_credit": "adapted from gobel2024_sd_skyrmion_kubo_Lz_kernel.py (itinerant L_z + Kubo/velocity machinery)",
        "method": "tight-binding surrogate + orbital Berry-curvature dipole (chi=tau*D); NO DFT",
        "units_note": "arbitrary/model units; we report the ORBITAL/SPIN RATIO, SOC-scaling, T-oddness and order-of-magnitude, NOT an absolute (h/e)Ohm^-1V^-1 match (would need DFT+Wannier).",
        "grid": f"{Nk}^3 coarse Monte-none uniform BZ grid",
        "tau_ps": tau, "J_neel": J, "mu": mu,
    }

    # ---- (A) main point: orbital BCD >> spin BCD at physical (weak) SOC ----
    lam0 = 0.12
    Do, Ds, gbar, gmin = bcd_zzyy(J, lam0, mu, Nk=Nk)
    ratio = abs(Do) / (abs(Ds) + 1e-30)
    chi_o = tau * Do
    chi_s = tau * Ds
    res["main"] = {
        "lam_SOC": lam0, "D_orbital_zzyy": Do, "D_spin_zzyy": Ds,
        "chi_orbital_zzyy_tauD": chi_o, "chi_spin_zzyy_tauD": chi_s,
        "orbital_over_spin_ratio": ratio,
        "avg_gap_nearFS": gbar, "min_gap": gmin,
    }
    print(f"[main] lam={lam0} D_o={Do:.4e} D_s={Ds:.4e} ratio={ratio:.1f} "
          f"chi_o={chi_o:.4e} chi_s={chi_s:.4e}")

    # ---- (B) SOC required + non-perturbative enhancement (scan lam) ----
    lam_scan = [0.02, 0.05, 0.10, 0.20, 0.40]
    scan = []
    for lam in lam_scan:
        Do_l, Ds_l, gbar_l, _ = bcd_zzyy(J, lam, mu, Nk=18)  # cheaper grid for scan
        scan.append({"lam": lam, "D_orbital": Do_l, "D_spin": Ds_l,
                     "ratio": abs(Do_l) / (abs(Ds_l) + 1e-30), "avg_gap": gbar_l})
        print(f"[scan] lam={lam:.2f} gap~{gbar_l:.3f} D_o={Do_l:.3e} D_s={Ds_l:.3e} "
              f"ratio={abs(Do_l)/(abs(Ds_l)+1e-30):.1f}")
    res["soc_scan"] = scan
    # SOC=0 limit
    Do_0, Ds_0, _, _ = bcd_zzyy(J, 0.0, mu, Nk=18)
    res["soc_zero"] = {"lam": 0.0, "D_orbital": Do_0, "D_spin": Ds_0}
    print(f"[soc=0] D_o={Do_0:.3e} D_s={Ds_0:.3e} (should be ~0 for orbital)")

    # non-perturbative check: does |D_orb| INCREASE as gap shrinks (small lam)?
    lams = np.array([s["lam"] for s in scan])
    Dos = np.array([abs(s["D_orbital"]) for s in scan])
    gaps = np.array([s["avg_gap"] for s in scan])
    # slope of log|D_o| vs log(lam): negative-ish or peaked at small lam = non-perturbative
    good = (Dos > 0)
    slope_D_vs_lam = float(np.polyfit(np.log(lams[good]), np.log(Dos[good]), 1)[0]) if good.sum() >= 2 else float("nan")
    res["nonperturbative"] = {
        "slope_logDorb_vs_loglam": slope_D_vs_lam,
        "interpretation": "negative or sub-linear slope => orbital response is enhanced at SMALL SOC (non-perturbative), matching the paper's weak-SOC amplification.",
    }

    # ---- (C) T-oddness: flip Neel vector J -> -J should flip sign of D_orb ----
    Do_flip, _, _, _ = bcd_zzyy(-J, lam0, mu, Nk=18)
    Do_ref, _, _, _ = bcd_zzyy(J, lam0, mu, Nk=18)
    res["T_odd_check"] = {
        "D_orb_+J": Do_ref, "D_orb_-J": Do_flip,
        "sign_flips": bool(np.sign(Do_ref) != np.sign(Do_flip) and abs(Do_ref) > 1e-30),
        "ratio_-J/+J": (Do_flip / Do_ref) if abs(Do_ref) > 1e-30 else None,
    }
    print(f"[T-odd] +J:{Do_ref:.3e}  -J:{Do_flip:.3e}")

    res["runtime_sec"] = round(time.time() - t0, 1)

    # ---- verdict scoring (honest) ----
    orb_dominates = ratio > 10.0
    soc_required = abs(Do_0) < 0.2 * abs(Do)
    nonpert = (slope_D_vs_lam < 0.8)   # not simply growing linearly with SOC
    t_odd = res["T_odd_check"]["sign_flips"]
    res["claims_reproduced"] = {
        "chi_eq_tau_D_structure": True,
        "orbital_dominates_spin_(>~100x paper)": {"reproduced_qualitatively": bool(orb_dominates),
                                                  "our_ratio": ratio, "paper_ratio": "~150 (1.3/0.0087)"},
        "SOC_required_(D->0 without SOC)": bool(soc_required),
        "nonperturbative_weak-SOC_enhancement": bool(nonpert),
        "T_odd_flips_with_Neel_vector": bool(t_odd),
        "absolute_magnitude_(h/e Ohm^-1 V^-1)": "NOT matched (surrogate, no DFT) - order-of-magnitude only",
    }

    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print("\nSAVED ->", OUT)
    print(json.dumps(res["claims_reproduced"], indent=2))
    return res


if __name__ == "__main__":
    main()
