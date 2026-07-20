"""
al_scaling.py — Analytic AL vs MT vertex-correction scaling (SM Eq. S10 + text).

Paper's analytic argument near magnetic criticality in 2D:
  chi_mag(q, w=0) = a xi^2 / (1 + xi^2 (q-Q)^2)        (S10, static)
  X^AL(0,0)  ~ sum_p [chi_mag(p,0)]^2  ~  xi^2       (in 2D)
  X^MT(0,0)  ~ sum_p  chi_mag(p,0)     ~  log xi
Therefore AL / MT ~ xi^2 / log(xi) -> AL dominates for xi >> 1.
General d: X^AL ∝ max{xi^{4-d}, 1}.

This module numerically evaluates the momentum sums for the Ornstein-Zernike
form on a 2D grid and confirms the xi^2 (AL) vs log xi (MT) scaling, plus the
d-dependence X^AL ∝ xi^{4-d}.
"""
import numpy as np


def chi_mag_grid(xi, nk=400, Q=(np.pi, np.pi), a=1.0):
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    KX, KY = np.meshgrid(ks, ks, indexing="ij")
    dq2 = (KX - Q[0]) ** 2 + (KY - Q[1]) ** 2
    # wrap distance to nearest Q image (periodic)
    return a * xi ** 2 / (1.0 + xi ** 2 * dq2)


def X_AL(xi, nk=400):
    chi = chi_mag_grid(xi, nk)
    return np.mean(chi ** 2)  # sum_p chi^2 / N


def X_MT(xi, nk=400):
    chi = chi_mag_grid(xi, nk)
    return np.mean(chi)       # sum_p chi / N


def X_AL_ddim(xi, d, nk=200):
    """AL sum in d dimensions on OZ form, to check X^AL ∝ xi^{4-d}."""
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    if d == 1:
        q = ks
        dq2 = q ** 2
        chi = xi ** 2 / (1 + xi ** 2 * dq2)
        return np.mean(chi ** 2)
    if d == 2:
        return X_AL(xi, nk)
    if d == 3:
        # coarser grid for 3D
        n3 = 60
        k = np.linspace(-np.pi, np.pi, n3, endpoint=False)
        KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
        dq2 = KX ** 2 + KY ** 2 + KZ ** 2
        chi = xi ** 2 / (1 + xi ** 2 * dq2)
        return np.mean(chi ** 2)


def fit_powerlaw(x, y):
    lx, ly = np.log(x), np.log(y)
    A = np.vstack([lx, np.ones_like(lx)]).T
    slope, icpt = np.linalg.lstsq(A, ly, rcond=None)[0]
    return slope, icpt


def X_AL_continuum(xi, d, R=50.0, n=4000):
    """Continuum OZ integral over |q|<R (no lattice cutoff) to recover clean 4-d exponent.
    In d dims, integral of chi^2 ~ xi^4 * int d^d q /(1+xi^2 q^2)^2.
    Substitute u=xi q -> xi^{4-d} * int d^d u/(1+u^2)^2 (converges for d<4)."""
    if d == 1:
        q = np.linspace(-R, R, n)
        chi = xi ** 2 / (1 + xi ** 2 * q ** 2)
        return np.trapezoid(chi ** 2, q)
    if d == 2:
        q = np.linspace(1e-6, R, n)
        chi = xi ** 2 / (1 + xi ** 2 * q ** 2)
        return np.trapezoid(2 * np.pi * q * chi ** 2, q)
    if d == 3:
        q = np.linspace(1e-6, R, n)
        chi = xi ** 2 / (1 + xi ** 2 * q ** 2)
        return np.trapezoid(4 * np.pi * q ** 2 * chi ** 2, q)


if __name__ == "__main__":
    import json
    xis = np.array([2, 4, 8, 16, 32, 64], dtype=float)
    al = np.array([X_AL(x) for x in xis])
    mt = np.array([X_MT(x) for x in xis])
    s_al, _ = fit_powerlaw(xis, al)
    # MT expected log: fit mt vs log(xi)
    coef = np.polyfit(np.log(xis), mt, 1)
    print("# 2D AL vs MT scaling (Ornstein-Zernike chi_mag)")
    print(f"{'xi':>6} {'X_AL':>12} {'X_MT':>12} {'AL/MT':>10}")
    for x, a, m in zip(xis, al, mt):
        print(f"{x:6.0f} {a:12.4f} {m:12.4f} {a/m:10.3f}")
    print(f"\nX_AL power-law exponent (expect ~2.0): {s_al:.3f}")
    print(f"X_MT vs log(xi) linear slope (log fit, expect ~const growth): {coef[0]:.3f}")
    # d-dependence: exponent of xi should be (4-d)
    print("\n# X_AL ∝ xi^(4-d) check:")
    dres = {}
    for d in (1, 2, 3):
        al_d = np.array([X_AL_ddim(x, d) for x in xis])
        s, _ = fit_powerlaw(xis, al_d)
        print(f"  d={d}: fitted exponent={s:.3f}  (expected 4-d={4-d})")
        dres[d] = {"fitted_exponent": float(s), "expected": 4 - d}
    print("\n# X_AL ∝ xi^(4-d) — CONTINUUM (no lattice UV cutoff):")
    dres_cont = {}
    for d in (1, 2, 3):
        al_c = np.array([X_AL_continuum(x, d) for x in xis])
        s, _ = fit_powerlaw(xis, al_c)
        print(f"  d={d}: fitted exponent={s:.3f}  (expected 4-d={4-d})")
        dres_cont[d] = {"fitted_exponent": float(s), "expected": 4 - d}
    with open("al_scaling_summary.json", "w") as f:
        json.dump({"xis": xis.tolist(), "X_AL": al.tolist(), "X_MT": mt.tolist(),
                   "AL_exponent_2d": float(s_al), "expected_AL_exponent_2d": 2.0,
                   "d_dependence": dres,
                   "d_dependence_continuum": dres_cont,
                   "AL_over_MT_growth": {"xi": xis.tolist(),
                                        "ratio": (al / mt).tolist()}}, f, indent=2)
