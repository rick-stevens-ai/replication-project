#!/usr/bin/env python3
"""
From-scratch replication of Li, Kim & Kee, "Intertwined van-Hove Singularities
as a Mechanism for Loop Current Order in Kagome Metals" (arXiv:2309.03288v2).

CLAIM UNDER TEST (headline):
  For two coupled van-Hove singularities (vH1, vH2) with small energy separation
  delta_eps, the nearest-neighbor repulsion favors a Loop-Current + Charge-Bond
  Order (LCBO) ground state that is LOWER in free energy than the competing
  charge-bond-order CBO-. Quantitatively (Eq. 4):

    f_CBO- - f_LCBO
      = |lambda|^2 k_cut^4 |Delta| (|b|^2+|b'|^2)
        / [16 pi (2|Delta|(|b|^2+|b'|^2)+delta_eps)(4|Delta|(|b|^2+|b'|^2)-delta_eps)]
      > 0

  and LCBO is favored when  delta_eps < 4(|b|^2+|b'|^2)|Delta|.

METHOD (built from scratch here):
  Construct the 6x6 effective patch Hamiltonian H_eff(k, Delta) of Eq.(2):

     rows/cols = [u1(MA),u1(MB),u1(MC), u2(MA),u2(MB),u2(MC)]

        | e1   s1 D  s1 D*  | l* k1   0     0    |
        | s1 D* e1   s1 D   |  0    l* k2   0    |
        | s1 D  s1 D* e1    |  0     0    l* k3  |
        | l k1  0     0     | e2   s2 D*  s2 D   |
        |  0   l k2   0     | s2 D  e2   s2 D*   |
        |  0    0    l k3    | s2 D* s2 D  e2     |

     s1 = -2|b'|^2 , s2 = 2|b|^2  (mirror-symmetry-fixed coefficients).
     k1 = -kx/2 + sqrt3/2 ky , k2 = -kx/2 - sqrt3/2 ky , k3 = kx.

  Free energy density f(Delta) = (1/A) * (-T) sum_k sum_n ln(1 + e^{-(E_n(k)-mu)/T}).
  We compare:
     CBO-  : Delta = -|Delta|
     LCBO  : Delta =  |Delta| e^{+i pi/3}
  (the two degenerate minima at lambda=0, per the paper's gauge argument).

  Delta f = f_CBO- - f_LCBO is computed by direct numerical patch summation and
  compared to the closed-form Eq.(4).

Kernel credit: structure and loop-current bookkeeping informed by the shared
TEXTURES-100 loop-current kernels
  /home/stevens/shared-kernels-cache/loop_current_meanfield_kernel.py
  /home/stevens/shared-kernels-cache/loop_current_kagome_kernel.py
(Peierls-flux / imaginary-bond-order = loop current convention). The 6x6 patch
model itself is implemented directly from the paper's Eq.(2)-(4).
"""
from __future__ import annotations
import json, sys
import numpy as np

SQ3 = np.sqrt(3.0)


def k_components(kx, ky):
    k1 = -0.5 * kx + 0.5 * SQ3 * ky
    k2 = -0.5 * kx - 0.5 * SQ3 * ky
    k3 = kx
    return k1, k2, k3


def h_eff(kx, ky, Delta, eps1, eps2, s1, s2, lam):
    """6x6 effective patch Hamiltonian, Eq.(2). Delta complex."""
    k1, k2, k3 = k_components(kx, ky)
    D = Delta
    Dc = np.conjugate(Delta)
    H = np.zeros((6, 6), dtype=complex)
    # P1 block (vH1): circulant [eps1, s1 D, s1 D*]
    H[0, 0] = H[1, 1] = H[2, 2] = eps1
    H[0, 1] = s1 * D;  H[1, 2] = s1 * D;  H[2, 0] = s1 * D
    H[1, 0] = s1 * Dc; H[2, 1] = s1 * Dc; H[0, 2] = s1 * Dc
    # P2 block (vH2): circulant [eps2, s2 D*, s2 D]
    H[3, 3] = H[4, 4] = H[5, 5] = eps2
    H[3, 4] = s2 * Dc; H[4, 5] = s2 * Dc; H[5, 3] = s2 * Dc
    H[4, 3] = s2 * D;  H[5, 4] = s2 * D;  H[3, 5] = s2 * D
    # Q coupling block (diagonal, linear in k): l k_i couples u1(Mi)-u2(Mi)
    H[0, 3] = np.conjugate(lam) * k1; H[3, 0] = lam * k1
    H[1, 4] = np.conjugate(lam) * k2; H[4, 1] = lam * k2
    H[2, 5] = np.conjugate(lam) * k3; H[5, 2] = lam * k3
    return H


def free_energy_density(Delta, eps1, eps2, s1, s2, lam, mu, T,
                        k_cut, nk, add_delta_sq_term=True, V=1.3):
    """Patch-summed mean-field free energy density.

    Integrates over the circular patch |k|<k_cut with nk x nk grid inside the
    bounding box (points outside the disk are dropped). The +|Delta|^2/V constant
    (Eq. 6) is common to both phases and cancels in the difference; included for
    completeness when add_delta_sq_term=True.
    """
    xs = np.linspace(-k_cut, k_cut, nk)
    dk = xs[1] - xs[0]
    tot = 0.0
    npts = 0
    for kx in xs:
        for ky in xs:
            if kx * kx + ky * ky > k_cut * k_cut:
                continue
            E = np.linalg.eigvalsh(h_eff(kx, ky, Delta, eps1, eps2, s1, s2, lam))
            x = (E - mu) / T
            # numerically stable -T*ln(1+e^-x) = -T*softplus(-x)
            sp = np.where(x > 0, np.log1p(np.exp(-x)), -x + np.log1p(np.exp(x)))
            tot += -T * np.sum(sp)
            npts += 1
    area = np.pi * k_cut * k_cut          # physical patch area
    # convert grid sum to integral: sum * dk^2 gives integral over k-space;
    # free energy density per unit area = integral / area
    f = tot * dk * dk / area
    if add_delta_sq_term:
        # 3 bonds (AB,BC,CA) each contribute 2 Nc |Delta|^2 / V per cell -> density
        f += 3.0 * abs(Delta) ** 2 / V
    return f


def eq3_eigs(Delta_abs, eps1, eps2, b, bp, mu):
    """Analytic eigenvalues at the minima, Eq.(3) (k=0, at CBO-/LCBO minima)."""
    E1 = eps2 - mu - 4 * b ** 2 * Delta_abs
    E2 = E3 = eps1 - mu - 2 * bp ** 2 * Delta_abs
    E4 = E5 = eps2 - mu + 2 * b ** 2 * Delta_abs
    E6 = eps1 - mu + 4 * bp ** 2 * Delta_abs
    return np.array([E1, E2, E3, E4, E5, E6])


def eq4_formula(lam_kcut, k_cut, Delta_abs, b, bp, delta_eps):
    """Closed-form Eq.(4) free-energy difference density.

    Written with lam*k_cut grouped (paper quotes lambda*k_cut = 0.1 eV). The
    |lambda|^2 k_cut^4 in the numerator = (lam_kcut)^2 * k_cut^2.
    """
    bb = b ** 2 + bp ** 2
    num = (lam_kcut ** 2) * (k_cut ** 2) * Delta_abs * bb
    den = 16 * np.pi * (2 * Delta_abs * bb + delta_eps) * (4 * Delta_abs * bb - delta_eps)
    return num / den


def main():
    # ---- paper parameters (Fig. 4) ----
    eps1 = 6.16          # eV
    eps2 = 6.40          # eV
    b = 0.52
    bp = 0.96            # b'
    lam_kcut = 0.1       # lambda * k_cut = 0.1 eV (paper)
    T_K = 90.0
    kB = 8.617333262e-5  # eV/K
    T = kB * T_K         # eV
    mu = eps2            # chemical potential near vH2 (LCBO most pronounced)

    s1 = -2 * bp ** 2
    s2 = 2 * b ** 2
    delta_eps = eps2 - eps1   # 0.24 eV -- but this is the *bare* vHS separation

    # patch cutoff (arbitrary units; lambda = lam_kcut / k_cut)
    k_cut = 1.0
    lam = lam_kcut / k_cut
    nk = 61

    # Order-parameter magnitude. Choose |Delta| so that the LCBO condition
    # delta_eps < 4(|b|^2+|b'|^2)|Delta| is satisfied (small effective separation).
    bb = b ** 2 + bp ** 2
    # threshold |Delta| for LCBO:
    Delta_thresh = delta_eps / (4 * bb)

    results = {"paper": "Li, Kim, Kee arXiv:2309.03288v2",
               "method": "from-scratch 6x6 effective patch mean-field (Eq.2-4)",
               "kernel_credit": "TEXTURES-100 loop_current_meanfield_kernel / loop_current_kagome_kernel (Peierls-flux loop-current convention)",
               "params": {"eps1": eps1, "eps2": eps2, "b": b, "bp": bp,
                          "s1": s1, "s2": s2, "lam_kcut": lam_kcut,
                          "T_K": T_K, "mu": mu, "delta_eps_bare": delta_eps,
                          "k_cut": k_cut, "nk": nk,
                          "Delta_thresh_for_LCBO": Delta_thresh},
               "scans": []}

    print("delta_eps (bare) =", delta_eps, " Delta_thresh =", Delta_thresh)

    # --- Scan over |Delta| at fixed small separation, mu=eps2 ---
    # Use a reduced effective separation to probe the small-separation regime as
    # in the headline: sweep the ratio delta_eps/(4 bb |Delta|).
    for Delta_abs in [0.02, 0.05, 0.08, 0.10, 0.15, 0.20, 0.30]:
        D_cbo = -Delta_abs
        D_lcbo = Delta_abs * np.exp(1j * np.pi / 3)
        f_cbo = free_energy_density(D_cbo, eps1, eps2, s1, s2, lam, mu, T, k_cut, nk)
        f_lcbo = free_energy_density(D_lcbo, eps1, eps2, s1, s2, lam, mu, T, k_cut, nk)
        df_num = f_cbo - f_lcbo
        df_formula = eq4_formula(lam_kcut, k_cut, Delta_abs, b, bp, delta_eps)
        lcbo_condition = delta_eps < 4 * bb * Delta_abs
        eigs = eq3_eigs(Delta_abs, eps1, eps2, b, bp, mu)
        results["scans"].append({
            "Delta_abs": Delta_abs,
            "f_CBO_minus": f_cbo,
            "f_LCBO": f_lcbo,
            "df_numeric_CBOminus_minus_LCBO": df_num,
            "df_eq4_formula": df_formula,
            "LCBO_favored_condition_met": bool(lcbo_condition),
            "LCBO_lower_numeric": bool(df_num > 0),
            "eq3_eigs_at_minimum": eigs.tolist(),
            "n_negative_eigs": int(np.sum(eigs < 0)),
        })
        print(f"|D|={Delta_abs:5.3f} cond={lcbo_condition!s:5} "
              f"df_num={df_num:+.6e} df_eq4={df_formula:+.6e} "
              f"LCBO_lower={df_num>0}")

    # --- lambda dependence at fixed |Delta| in LCBO regime (Fig 4b) ---
    Delta_abs = 0.20   # satisfies condition (4*bb*0.2 = 0.788 > 0.24)
    lam_scan = []
    for lk in [0.0, 0.02, 0.05, 0.1, 0.15, 0.2]:
        lmb = lk / k_cut
        D_cbo = -Delta_abs
        D_lcbo = Delta_abs * np.exp(1j * np.pi / 3)
        f_cbo = free_energy_density(D_cbo, eps1, eps2, s1, s2, lmb, mu, T, k_cut, nk)
        f_lcbo = free_energy_density(D_lcbo, eps1, eps2, s1, s2, lmb, mu, T, k_cut, nk)
        lam_scan.append({"lam_kcut": lk, "f_CBO_minus": f_cbo, "f_LCBO": f_lcbo,
                         "df": f_cbo - f_lcbo})
        print(f"lam_kcut={lk:4.2f} df={f_cbo-f_lcbo:+.6e} (LCBO lower if >0)")
    results["lambda_scan_at_Delta0.20"] = lam_scan

    # --- separation dependence: LCBO condition boundary ---
    sep_scan = []
    Delta_abs = 0.20
    for de in [0.10, 0.24, 0.50, 0.788, 0.90, 1.2]:
        e2 = eps1 + de
        mu_local = e2
        D_cbo = -Delta_abs
        D_lcbo = Delta_abs * np.exp(1j * np.pi / 3)
        f_cbo = free_energy_density(D_cbo, eps1, e2, s1, s2, lam, mu_local, T, k_cut, nk)
        f_lcbo = free_energy_density(D_lcbo, eps1, e2, s1, s2, lam, mu_local, T, k_cut, nk)
        sep_scan.append({"delta_eps": de, "df": f_cbo - f_lcbo,
                         "condition_met": bool(de < 4 * bb * Delta_abs),
                         "threshold_4bbD": 4 * bb * Delta_abs})
        print(f"delta_eps={de:5.3f} df={f_cbo-f_lcbo:+.6e} cond={de<4*bb*Delta_abs}")
    results["separation_scan_at_Delta0.20"] = sep_scan

    with open("/home/stevens/textures-100/corpus/textures-loop-current-li2023/work/li2023_result.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\nSAVED work/li2023_result.json")
    return results


if __name__ == "__main__":
    main()
