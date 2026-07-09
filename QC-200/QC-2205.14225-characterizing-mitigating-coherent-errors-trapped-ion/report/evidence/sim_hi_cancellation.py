#!/usr/bin/env python3
"""
Focused test of the Hidden-Inverses cancellation mechanism.

Paper claim (Sec 2): "in the absence of noise, G and G^dagger implement the
same physical operation; this is not true when A, B, C are subjected to
errors."  The HI protocol chooses G or G^dagger such that the coherent
error incurred by an adjacent gate is REVERSED, giving a first-order
cancellation.

Canonical minimal test: two Hadamards back-to-back (an identity in the
noiseless case).  If the compiler picks:
    (A) H . H  -- both same decomposition, over-rot errors ADD
    (B) H . H^dagger -- HI, over-rot errors CANCEL

We measure infidelity vs epsilon on |+> preparation:
    prep: |0> -> H |0> = |+>,  then apply identity in configuration (A) or (B),
    compare to |+>.
"""
import numpy as np, json
from sim_hidden_inverses import (X_noisy, Y_noisy, H_standard, H_hidden,
                                  fidelity_unitary, fidelity_states)

I2 = np.eye(2, dtype=complex)

def bare_HH(eps):
    """H followed by H (both standard decomp). Ideally = I; noisy: errors add."""
    return H_standard(eps) @ H_standard(eps)

def hi_HH(eps):
    """H followed by H^dagger (hidden inverse). Ideally = I; noisy: errors cancel."""
    return H_hidden(eps) @ H_standard(eps)

def run():
    eps_list = np.linspace(-0.1, 0.1, 41)
    rows = []
    for eps in eps_list:
        U_bare = bare_HH(eps)
        U_hi   = hi_HH(eps)
        F_bare = fidelity_unitary(U_bare, I2)
        F_hi   = fidelity_unitary(U_hi,   I2)
        rows.append({"eps": float(eps),
                     "infid_bare": float(1-F_bare),
                     "infid_hi":   float(1-F_hi)})
    # order fit on positive |eps|
    xs = np.array([np.log(abs(r["eps"])) for r in rows if abs(r["eps"])>1e-3])
    ys_b = np.array([np.log(max(r["infid_bare"], 1e-20)) for r in rows if abs(r["eps"])>1e-3])
    ys_h = np.array([np.log(max(r["infid_hi"],   1e-20)) for r in rows if abs(r["eps"])>1e-3])
    slope_b = np.polyfit(xs, ys_b, 1)[0]
    slope_h = np.polyfit(xs, ys_h, 1)[0]

    print(f"Bare  H . H       : 1-F ~ |eps|^{slope_b:.2f}")
    print(f"HI    H . H^dagger : 1-F ~ |eps|^{slope_h:.2f}")

    # ratio at eps = 0.05
    row_005 = min(rows, key=lambda r: abs(r["eps"]-0.05))
    ratio = row_005["infid_bare"] / max(row_005["infid_hi"], 1e-20)
    print(f"At eps=0.05: infid_bare={row_005['infid_bare']:.4e}, "
          f"infid_hi={row_005['infid_hi']:.4e}, ratio={ratio:.2f}x")

    out = {
        "rows": rows,
        "order_bare": float(slope_b),
        "order_hi":   float(slope_h),
        "ratio_at_eps_0p05": float(ratio),
    }
    with open("results_hi_cancellation.json", "w") as f:
        json.dump(out, f, indent=2)
    return out

if __name__ == "__main__":
    run()
