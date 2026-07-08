"""
Surface code d=3 (planar / unrotated) definitions.

Layout (L=3 planar code, qubits on edges of a 3x3 lattice, following Fig 1(b) of
Higgott et al. arXiv:2002.00362).

We use the standard "unrotated" planar surface code. It has L^2 + (L-1)^2 = 13
data qubits for L=3.

Qubit indexing (13 qubits, arranged as horizontal edges + vertical edges):

We use rows and columns of a 3x3 grid of vertices (indices 0..2 in each dim).
- Horizontal edges: between vertex (r,c) and (r,c+1), for r in 0..2, c in 0..1
  => 3*2 = 6 horizontal edges
- Vertical edges: between vertex (r,c) and (r+1,c), for r in 0..1, c in 0..2
  => 2*3 = 6 vertical edges
Total = 12 edges, but we need 13 physical qubits for L=3 planar (L^2+(L-1)^2=13).

Actually the standard planar surface code with distance L has:
- data qubits: L^2 + (L-1)^2
- X-stabilizers: L*(L-1)  [on "vertices" of one type]
- Z-stabilizers: (L-1)*L  [on "faces" of the other type]
- logical qubits: 1

For L=3: 9+4=13 data qubits, 6 X-stabs, 6 Z-stabs, 1 logical qubit.
13 = 12 stabs + 1 logical  ✓  (satisfies n = m + k with independent generators)

Layout: standard "rotated-45" view (equivalent to unrotated).
We use a 5x5 grid where data qubits sit at positions with (r+c) even,
and stabilizer plaquettes fit into (r+c) odd cells. For L=3:

Grid coordinates (row, col), 0-indexed, size 5x5:
Positions with (r+c) even are data qubits (13 of them):
  (0,0) (0,2) (0,4)
  (1,1) (1,3)
  (2,0) (2,2) (2,4)
  (3,1) (3,3)
  (4,0) (4,2) (4,4)

Positions with (r+c) odd hold stabilizers or are empty (boundary).
- X-type stabilizers on faces where the "smooth" boundary is at top/bottom
- Z-type stabilizers on faces where the "rough" boundary is at left/right

Standard convention for planar code:
- X stabilizers at positions where r is even (except at top/bottom row internal) — no, easier to just enumerate.

Actually, the cleanest way is to define the code by its stabilizers directly.
We'll enumerate the qubit positions and stabilizer support explicitly.
"""

import stim
import numpy as np
from itertools import product


def build_d3_planar_surface_code():
    """
    Build a d=3 unrotated planar surface code.
    Returns:
        n: number of data qubits (13)
        qubit_coords: dict mapping qubit_index -> (row, col)
        x_stabs: list of tuples of qubit indices for X-type stabilizers (6 of them)
        z_stabs: list of tuples of qubit indices for Z-type stabilizers (6 of them)
        logical_x: tuple of qubit indices for logical X operator
        logical_z: tuple of qubit indices for logical Z operator
    """
    # Use a 5x5 grid where data qubits sit at (r+c) even.
    # We use the "square lattice" planar code where:
    # - vertices of the lattice are at (r,c) with r,c in {0,2,4}
    # - edges of the lattice hold data qubits
    # For L=3 there are 3x3=9 vertices and 2*3*(3-1) = 12 edges... no wait,
    # edges = L*(L-1) horizontal + (L-1)*L vertical = 2*L*(L-1) = 12 for L=3.
    # But planar code needs L^2 + (L-1)^2 = 13 qubits.
    #
    # Different convention: qubits on both edges AND vertices of an (L-1)x(L-1) grid,
    # or, more commonly, use two interlocking lattices.
    #
    # I'll use the standard "dual lattice" convention:
    # For distance L, arrange L rows of L qubits + (L-1) rows of (L-1) qubits interleaved.
    # Row 0: L qubits at columns 0..L-1
    # Row 1 (offset): L-1 qubits at columns 0..L-2 (shifted by half)
    # Row 2: L qubits
    # ...
    # Total rows: L + (L-1) = 2L-1
    # Total qubits: L*L + (L-1)*(L-1) = L^2 + (L-1)^2  ✓ = 13 for L=3
    #
    # This is the "rotated by 45" view but is the standard unrotated planar code.

    L = 3
    qubit_coords = {}  # idx -> (row, col) in the 5x5 grid
    coord_to_idx = {}
    idx = 0
    # "Big" rows (rows 0, 2, 4): L=3 qubits at cols 0, 2, 4
    # "Small" rows (rows 1, 3): L-1=2 qubits at cols 1, 3
    for r in range(2 * L - 1):
        if r % 2 == 0:
            # big row
            for c in range(0, 2 * L - 1, 2):
                qubit_coords[idx] = (r, c)
                coord_to_idx[(r, c)] = idx
                idx += 1
        else:
            # small row
            for c in range(1, 2 * L - 2, 2):
                qubit_coords[idx] = (r, c)
                coord_to_idx[(r, c)] = idx
                idx += 1
    n = idx
    assert n == L * L + (L - 1) * (L - 1) == 13, f"n={n}"

    # Stabilizers:
    # X-plaquette centers are at positions (r,c) with r odd and c even (in the 5x5 grid).
    # They act on 4 (bulk) or 3 (boundary) neighboring qubits at (r±1, c) and (r, c±1).
    # Actually let's think again.
    #
    # In the planar code (rotated view), plaquettes are the empty cells of the
    # (2L-1)x(2L-1) grid, at (r,c) with (r+c) odd.
    # There are (2L-1)^2 - n = 25 - 13 = 12 empty cells for L=3.
    # These 12 cells split into 6 X-type and 6 Z-type based on some pattern.
    #
    # Convention:
    # - X-plaquettes: (r,c) with r odd (rows 1, 3) and c even (cols 0, 2, 4).
    #   For L=3: (1,0),(1,2),(1,4),(3,0),(3,2),(3,4) => 6 X-stabs.
    #   But (1,0),(1,4),(3,0),(3,4) are at the boundary (weight-3).
    # - Z-plaquettes: (r,c) with r even (rows 0, 2, 4) and c odd (cols 1, 3).
    #   For L=3: (0,1),(0,3),(2,1),(2,3),(4,1),(4,3) => 6 Z-stabs.
    #   (0,1),(0,3),(4,1),(4,3) are boundary weight-3.
    #
    # Total: 12 stabs, n - k = 13 - 1 = 12  ✓

    x_stabs = []
    for r in range(1, 2 * L - 1, 2):  # rows 1, 3
        for c in range(0, 2 * L - 1, 2):  # cols 0, 2, 4
            # X stabilizer at (r,c), acts on qubits at (r-1,c),(r+1,c),(r,c-1),(r,c+1)
            support = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_to_idx:
                    support.append(coord_to_idx[(nr, nc)])
            x_stabs.append(tuple(sorted(support)))

    z_stabs = []
    for r in range(0, 2 * L - 1, 2):  # rows 0, 2, 4
        for c in range(1, 2 * L - 2, 2):  # cols 1, 3
            support = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_to_idx:
                    support.append(coord_to_idx[(nr, nc)])
            z_stabs.append(tuple(sorted(support)))

    assert len(x_stabs) == 6 and len(z_stabs) == 6

    # Logical operators for planar code:
    # Logical Z runs vertically through the code (spans top-to-bottom).
    # Logical X runs horizontally.
    # Simplest choice:
    #   Logical Z on column c=0: qubits at (0,0),(2,0),(4,0) — 3 qubits, weight 3 = d ✓
    #   Logical X on row r=0: qubits at (0,0),(0,2),(0,4) — 3 qubits, weight 3 = d ✓
    # Verify: logical_x must anticommute with logical_z at exactly qubit (0,0), which it does.
    logical_z = tuple(coord_to_idx[(r, 0)] for r in [0, 2, 4])
    logical_x = tuple(coord_to_idx[(0, c)] for c in [0, 2, 4])

    return {
        'L': L,
        'n': n,
        'qubit_coords': qubit_coords,
        'coord_to_idx': coord_to_idx,
        'x_stabs': x_stabs,
        'z_stabs': z_stabs,
        'logical_x': logical_x,
        'logical_z': logical_z,
    }


def verify_code_structure(code):
    """Verify stabilizers commute and logicals anticommute with correct stab and each other."""
    x_stabs = code['x_stabs']
    z_stabs = code['z_stabs']
    logical_x = code['logical_x']
    logical_z = code['logical_z']

    # Check X-stabs mutually commute (trivially: both act only with X)
    # Check Z-stabs mutually commute (trivially)
    # Check every X-stab commutes with every Z-stab (overlap must be even)
    for xs in x_stabs:
        for zs in z_stabs:
            overlap = len(set(xs) & set(zs))
            assert overlap % 2 == 0, f"X-stab {xs} and Z-stab {zs} anticommute (overlap={overlap})"
    # Check logical_x commutes with every stabilizer
    for zs in z_stabs:
        overlap = len(set(logical_x) & set(zs))
        assert overlap % 2 == 0, f"logical_X {logical_x} and Z-stab {zs} anticommute"
    for xs in x_stabs:
        overlap = len(set(logical_z) & set(xs))
        assert overlap % 2 == 0, f"logical_Z {logical_z} and X-stab {xs} anticommute"
    # Check logical_x anticommutes with logical_z
    overlap = len(set(logical_x) & set(logical_z))
    assert overlap % 2 == 1, f"logicals commute (overlap={overlap})"
    return True


if __name__ == "__main__":
    code = build_d3_planar_surface_code()
    print(f"L = {code['L']}")
    print(f"n = {code['n']} data qubits")
    print(f"X stabilizers ({len(code['x_stabs'])}):")
    for i, xs in enumerate(code['x_stabs']):
        print(f"  X{i}: qubits {xs} (weight {len(xs)})")
    print(f"Z stabilizers ({len(code['z_stabs'])}):")
    for i, zs in enumerate(code['z_stabs']):
        print(f"  Z{i}: qubits {zs} (weight {len(zs)})")
    print(f"Logical X: qubits {code['logical_x']}")
    print(f"Logical Z: qubits {code['logical_z']}")
    print()
    verify_code_structure(code)
    print("Code structure valid: all stabilizers commute, logicals anticommute.")
