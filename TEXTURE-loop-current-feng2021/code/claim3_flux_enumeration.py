"""
claim3_flux_enumeration.py
==========================
Replicates the paper's brute-force enumeration principle for flux phases on the
kagome lattice (Sec. III). The paper's ONLY selection rule (their Eq. 24 +
surrounding text) is:

  "the currents must conserve at each lattice site without generating any
   charge sink or source"  (Kirchhoff / charge-continuity),
  "we also assume that the amplitudes of the complex hopping terms at all bonds
   must be the same"  (each bond carries current +1, -1, or 0 units).

We implement this directly on the kagome NN graph and COUNT the charge-conserving
directed-current configurations, then compare with the paper's reported totals.

Kagome unit cell = 3 sites (A,B,C), 6 NN bonds per cell (each site has 4 NN).
We tile the cell into an N1 x N2 supercell with PERIODIC boundary conditions.
Each bond gets a signed integer current in {-1,0,+1}; charge conservation:
sum of signed currents into each site = 0. We count solutions and (for the 1x1
cell) classify by net triangle/hexagon flux pattern.

CLAIM (paper abstract + Sec III + Tables II-IV):
  * 1x1: 3 CLASSES; configuration count in the paper's own text = "10 flux
    phases in 1*1 unit cell" (Nagaosa 2 + flow-a 2 + flow-b 6 = 10).
  * total (1x1)+(2x2)+(1x2) = 183 flux phases within 2x2 unit cell.
NOTE: the paper counts symmetry-inequivalent physical CONFIGURATIONS with the
"same amplitude" rule AND a nonzero-flux (genuinely chiral) requirement. Our
raw Kirchhoff count is a SUPERSET (it also includes the trivial all-zero and
pure-CDW-like states). We therefore report BOTH the raw Kirchhoff solution
count and the count restricted to nonzero-current (flux-bearing) states, and
compare the STRUCTURE (number of independent cycles) rather than claiming exact
identity with the paper's symmetry-reduced classes.
"""
import numpy as np
import itertools, json, os
from fractions import Fraction

# ---------------------------------------------------------------------------
# Kagome NN graph for an N1 x N2 supercell with PBC.
# Sites: 3 sublattices A,B,C per cell. Cell index (i,j), i in 0..N1-1, etc.
# NN bonds of kagome (from the standard kagome connectivity, |a|=1):
#   Within cell (up-triangle): A-B, B-C, C-A
#   To neighboring cells (down-triangle bonds):
#     A(i,j) - C(i-1,j)      (along -a1 for the A-C down bond)
#     B(i,j) - A(i, j-1)? ...
# We use the well-known kagome NN list where each site has 4 neighbors,
# and the down-triangle connects A(i,j)-B(i-1,j+?), etc. To be robust we
# GENERATE the NN graph from site coordinates + distance cutoff.
# ---------------------------------------------------------------------------
SQRT3 = np.sqrt(3.0)
A1 = np.array([1.0, 0.0]); A2 = np.array([0.5, SQRT3/2.0])
# sublattice offsets (midpoints of triangular NN bonds)
TAU = {0: 0.5*A1, 1: 0.5*A2, 2: 0.5*(A1+A2)}

def build_graph(N1, N2):
    """Return list of undirected bonds as (site_u, site_v) index pairs, where
    each site is (i,j,s). NN determined by minimum-image distance = 0.5."""
    sites = {}
    coords = {}
    idx = 0
    for i in range(N1):
        for j in range(N2):
            for s in range(3):
                sites[(i, j, s)] = idx
                coords[idx] = i*A1 + j*A2 + TAU[s]
                idx += 1
    n = idx
    # supercell lattice vectors for min image
    L1 = N1*A1; L2 = N2*A2
    def mindist(p, q):
        best = 1e9
        for m in (-1, 0, 1):
            for k in (-1, 0, 1):
                d = np.linalg.norm(p - q + m*L1 + k*L2)
                best = min(best, d)
        return best
    bonds = []
    keys = list(coords.keys())
    for a in range(n):
        for b in range(a+1, n):
            if abs(mindist(coords[a], coords[b]) - 0.5) < 1e-6:
                bonds.append((a, b))
    return n, bonds, coords

def count_kirchhoff(N1, N2, values=(-1, 0, 1), require_nonzero=False, cap=None):
    """Count bond-current assignments (u<v gives + direction) with net current
    zero at every site. Brute force over values^len(bonds). Feasible for 1x1."""
    n, bonds, coords = build_graph(N1, N2)
    nb = len(bonds)
    # incidence matrix: rows sites, cols bonds; +1 at u, -1 at v (current u->v)
    Inc = np.zeros((n, nb), dtype=int)
    for c, (u, v) in enumerate(bonds):
        Inc[u, c] += 1
        Inc[v, c] -= 1
    solutions = 0
    nonzero_solutions = 0
    flux_signatures = set()
    total = len(values)**nb
    if cap and total > cap:
        return dict(n_sites=n, n_bonds=nb, feasible=False, total_space=total)
    for combo in itertools.product(values, repeat=nb):
        j = np.array(combo)
        if np.all(Inc @ j == 0):
            solutions += 1
            if np.any(j != 0):
                nonzero_solutions += 1
                flux_signatures.add(tuple(combo))
    return dict(n_sites=n, n_bonds=nb, kirchhoff_solutions=solutions,
                nonzero_flux_solutions=nonzero_solutions,
                distinct_flux_configs=len(flux_signatures),
                cycle_rank=nb - (n - 1))   # independent cycles (connected graph)

if __name__ == "__main__":
    out = {}
    print("=== 1x1 kagome cell: brute-force charge-conserving current configs ===")
    r11 = count_kirchhoff(1, 1)
    out["1x1"] = r11
    print(json.dumps(r11, indent=2))

    # The number of INDEPENDENT flux loops (cycles) = triangles + hexagon
    # For the 1x1 kagome torus: 3 sites, 6 bonds -> cycle rank = 6-(3-1)=4.
    # Physically: 2 triangles (up/down) + ... on the torus. The paper's
    # "10 flux phases" counts amplitude-1 chiral (nonzero, sink-free) configs.
    print("\nCycle rank (independent flux loops) for 1x1 torus:",
          r11["cycle_rank"])

    # 1x2 cell (still tractable): 6 sites, 12 bonds -> 3^12 ~ 531k, fine.
    print("\n=== 1x2 kagome cell ===")
    r12 = count_kirchhoff(1, 2, cap=2_000_000)
    out["1x2"] = r12
    print(json.dumps(r12, indent=2))

    # Compare to paper's reported class/config structure
    paper = {
        "1x1_classes": 3, "1x1_configs_text": 10,
        "2x2_classes": 18, "2x2_configs": 122,
        "1x2_classes": 8, "1x2_configs": 17*3,
        "total_configs": 183,
    }
    out["paper_reported"] = paper
    print("\n=== paper's reported totals ===")
    print(json.dumps(paper, indent=2))
    print(f"  183 = 10(1x1) + 122(2x2) + 51(1x2)? -> "
          f"{10+122+51} (== 183: {10+122+51==183})")

    with open(os.path.join(os.path.dirname(__file__), "..", "work",
              "claim3_output.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
