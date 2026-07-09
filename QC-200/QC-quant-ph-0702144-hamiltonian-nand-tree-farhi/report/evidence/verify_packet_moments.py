#!/usr/bin/env python3
"""Verify the paper's Eqs. (2.12) and (2.13):
   <psi(0)|H|psi(0)>  = 0
   <psi(0)|H^2|psi(0)> = 5/L
for the initial right-moving packet, on the FULL graph (tree attached but
psi(0) has support only on the runway sites, so the tree presence should not
change these moments -- verifying this is itself a small consistency check).
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from nand_tree_qwalk import build_graph, hamiltonian, initial_state

out = {}
for n in (2, 3):
    for L in (8, 16, 32, 64):
        # trivial input; tree attachment is what matters
        bits = tuple(0 for _ in range(2**n))
        G = build_graph(bits, n, M=3*L)
        H = hamiltonian(G)
        psi0 = initial_state(G, L)
        exp_H  = float(np.vdot(psi0, H @ psi0).real)
        exp_H2 = float(np.vdot(psi0, H @ (H @ psi0)).real)
        out[f"n={n},L={L}"] = dict(
            n=n, L=L, dim=G.size,
            exp_H=exp_H, exp_H2=exp_H2,
            paper_pred_5_over_L=5.0/L,
            ratio=exp_H2 / (5.0/L),
        )
        print(f"n={n} L={L}: <H>={exp_H:+.3e}  <H^2>={exp_H2:.6f}  5/L={5/L:.6f}  ratio={exp_H2/(5/L):.6f}")

with open(Path(__file__).resolve().parent / "packet_moments.json", "w") as f:
    json.dump(out, f, indent=2)
