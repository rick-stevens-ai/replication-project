#!/usr/bin/env python3
"""
Driver: evaluate the five machine-checkable claims (C1-C5) for the Kang-Shiozaki-Cho
many-body quadrupole order parameter on the BBH model.

Writes JSON results to work/ (path passed as argv[1], default ../work).
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bbh_multipole as bm


def qxy(L, gx, gy, lx, ly, delta, s=0.0):
    """Referenced many-body quadrupole (trivial->0, topo->1/2), |<U2>|, gap."""
    return bm.quadrupole(L, L, gx, gy, lx, ly, delta, referenced=True, s=s)


def to_half(q):
    """map angle mod 1 into distance-from {0, 0.5}; return canonical value 0 or 0.5."""
    q = q % 1.0
    # fold to [0,0.5]
    return min(q, 1.0 - q)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "work")
    os.makedirs(outdir, exist_ok=True)
    results = {}

    Ls = [6, 8, 10, 12]
    s = 0.0

    # ---- C1: trivial phase Q ~ 0 ; C2: topological phase Q ~ 0.5 --------------
    print("== C1/C2: quantized quadrupole, delta=0, lambda=1 ==")
    c12 = {"trivial": [], "topological": []}
    for L in Ls:
        Qt, mt, gt = qxy(L, 1.5, 1.5, 1, 1, 0.0, s)
        Qo, mo, go = qxy(L, 0.5, 0.5, 1, 1, 0.0, s)
        c12["trivial"].append({"L": L, "Q": Qt, "absU": mt, "gap": gt})
        c12["topological"].append({"L": L, "Q": Qo, "absU": mo, "gap": go})
        print(f"  L={L:2d}  trivial Q={Qt:.4f} |U|={mt:.3e}   topo Q={Qo:.4f} |U|={mo:.3e}")
    results["C1_C2_quantization"] = c12

    # ---- C3: sharp transition across gamma_y = 1 (cut gamma_x=0.5, Fig 1c) ----
    print("== C3: transition sweep gamma_y, gamma_x=0.5, lambda=1, delta=0 (L=10) ==")
    L = 10
    sweep = []
    for gy in np.linspace(0.2, 1.8, 17):
        Q, m, g = qxy(L, 0.5, gy, 1, 1, 0.0, s)
        sweep.append({"gy": round(float(gy), 3), "Q": Q, "absU": m, "gap": g})
    for row in sweep:
        print(f"  gy={row['gy']:.2f}  Q={row['Q']:.4f}  |U|={row['absU']:.3e}")
    results["C3_transition_sweep"] = {"L": L, "gamma_x": 0.5, "sweep": sweep}

    # ---- C4: polarization vanishes (well-definedness) + mirror sign ----------
    print("== C4: dipole P_x, P_y (should be ~0) and mirror Q->-Q ==")
    L = 10
    Px_t, mPx_t = bm.dipole(L, L, 1.5, 1.5, 1, 1, 0.0, axis='x')
    Py_t, mPy_t = bm.dipole(L, L, 1.5, 1.5, 1, 1, 0.0, axis='y')
    Px_o, mPx_o = bm.dipole(L, L, 0.5, 0.5, 1, 1, 0.0, axis='x')
    Py_o, mPy_o = bm.dipole(L, L, 0.5, 0.5, 1, 1, 0.0, axis='y')

    def fold_pol(p):  # distance to nearest integer (0 => polarization vanishes)
        return min(p % 1.0, 1.0 - (p % 1.0))
    # fold reported P into (-0.5,0.5] for readability
    Px_t, Py_t = bm._fold_half(Px_t), bm._fold_half(Py_t)
    Px_o, Py_o = bm._fold_half(Px_o), bm._fold_half(Py_o)
    c4 = {
        "trivial": {"Px": Px_t, "Py": Py_t, "Px_fold": fold_pol(Px_t), "Py_fold": fold_pol(Py_t)},
        "topological": {"Px": Px_o, "Py": Py_o, "Px_fold": fold_pol(Px_o), "Py_fold": fold_pol(Py_o)},
    }
    print(f"  trivial     Px={Px_t:.4f} Py={Py_t:.4f}")
    print(f"  topological Px={Px_o:.4f} Py={Py_o:.4f}")
    results["C4_polarization"] = c4

    # ---- C5: isotropic Thouless pumping (Eq. 9): phase vs theta ---------------
    print("== C5: isotropic Thouless pump (Eq. 9), L=10, closed loop ==")
    L = 10
    pump = []
    for theta in np.linspace(0, 2 * np.pi, 25):
        g = 1 - 0.6 * np.sin(theta)
        lam = 1 + 0.6 * np.sin(theta)
        dl = 0.6 * np.cos(theta)
        Q, m, gap = qxy(L, g, g, lam, lam, dl, s)
        pump.append({"theta": round(float(theta), 4), "gamma": round(float(g), 4),
                     "lam": round(float(lam), 4), "delta": round(float(dl), 4),
                     "Q": Q, "absU": m})
    for row in pump[::4]:
        print(f"  th={row['theta']:.2f} g={row['gamma']:.2f} l={row['lam']:.2f} "
              f"d={row['delta']:+.2f}  Q={row['Q']:.4f} |U|={row['absU']:.3e}")
    results["C5_thouless_pump"] = {"L": L, "path": "Eq9_isotropic", "pump": pump}

    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nWrote", os.path.join(outdir, "results.json"))


if __name__ == "__main__":
    main()
