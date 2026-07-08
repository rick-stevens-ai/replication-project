#!/usr/bin/env python3
"""
Gradient-descent geometry optimization for H2 using the VQE energy gradient.
Reproduces paper Fig. 4a claim: gradient-based opt converges to (0.741 Å, -1.137 Ha).
"""
import json
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from vqe_h2_gradients import vqe_energy_and_params, vqe_gradient_hellmann_feynman

def main():
    R = 1.0  # start far from equilibrium (paper uses several starting points)
    lr = 0.5  # Å per (Ha/Å)  step
    max_iter = 30
    tol_grad = 1e-4  # Ha/Å

    print(f"H2 geometry optimization from R0={R:.3f} Å, lr={lr}")
    print(f"{'iter':>4} {'R (Å)':>10} {'E (Ha)':>14} {'dE/dR':>14}")
    hist = []
    params = None
    for it in range(max_iter):
        e, params, _, _ = vqe_energy_and_params(R, init_params=params)
        g = vqe_gradient_hellmann_feynman(R, params)
        hist.append({"iter": it, "R_A": float(R), "E_Ha": float(e), "dEdR": float(g)})
        print(f"{it:>4d} {R:>10.6f} {e:>14.8f} {g:>+14.6e}")
        if abs(g) < tol_grad:
            print(f"Converged at iter {it}: |dE/dR|={abs(g):.2e} < {tol_grad:.0e}")
            break
        R = R - lr * g

    out = {
        "start_R_A": 1.0,
        "learning_rate": lr,
        "tol_grad_HaPerA": tol_grad,
        "history": hist,
        "final_R_A": float(R),
        "final_E_Ha": float(hist[-1]["E_Ha"]),
        "paper_target_R_A": 0.741,
        "paper_target_E_Ha": -1.137,
    }
    out_path = "/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2106.06463-qc-chem-energy-derivatives/report/evidence/geom_opt_h2.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nFinal: R={R:.4f} Å (paper 0.741 Å), E={hist[-1]['E_Ha']:.6f} Ha (paper -1.137 Ha)")
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
