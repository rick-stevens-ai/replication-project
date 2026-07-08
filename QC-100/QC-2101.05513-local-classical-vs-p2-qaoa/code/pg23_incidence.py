#!/usr/bin/env python
"""
Construct PG(2,3): projective plane of order 3.
- 13 points, 13 lines, each line 4 points, each point on 4 lines,
  two points on unique line, two lines meet at unique point.

Coordinates: points = nonzero vectors in F_3^3 modulo scalars (12/2=... wait).
F_3^3 has 27 vectors, minus zero = 26, divided by nonzero scalars (2) = 13 points. Good.

Lines = 2D subspaces of F_3^3, likewise 13.
Point p on line L iff p is in L.

Levi graph: bipartite (P, L), edge (p, L) iff p in L. This is 4-regular (each point on 4 lines, each line has 4 points) with girth 6.
"""

import networkx as nx
import itertools


def canonical(v):
    """Canonical representative of the projective point [v]."""
    v = tuple(x % 3 for x in v)
    if v == (0, 0, 0):
        return None
    # find first nonzero, scale so it is 1
    for x in v:
        if x != 0:
            first = x
            break
    inv = pow(first, -1, 3)
    return tuple((x * inv) % 3 for x in v)


def all_points():
    seen = set()
    pts = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                p = canonical((a, b, c))
                if p is None or p in seen:
                    continue
                seen.add(p)
                pts.append(p)
    return pts  # 13 points


def all_lines(points):
    """A line is spanned by 2 independent points; canonicalize the pair or
    represent line by its set of 4 points (nonzero linear combos mod scalars).
    """
    lines = set()
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if j <= i:
                continue
            # line is set of canonical([a*p + b*q]) for (a,b) in F_3^2 nonzero
            line_pts = set()
            for a in range(3):
                for b in range(3):
                    if a == 0 and b == 0:
                        continue
                    v = tuple((a * p[k] + b * q[k]) % 3 for k in range(3))
                    cp = canonical(v)
                    if cp is not None:
                        line_pts.add(cp)
            lines.add(frozenset(line_pts))
    return sorted(lines, key=lambda s: sorted(s))


def build_incidence_graph():
    P = all_points()
    L = all_lines(P)
    assert len(P) == 13 and len(L) == 13, f"|P|={len(P)}, |L|={len(L)}"
    for line in L:
        assert len(line) == 4, f"line size {len(line)}"
    G = nx.Graph()
    # nodes 0..12 for points, 13..25 for lines
    point_idx = {p: i for i, p in enumerate(P)}
    line_idx = {ln: 13 + i for i, ln in enumerate(L)}
    for p, pi in point_idx.items():
        G.add_node(pi, kind="point", coord=p)
    for ln, li in line_idx.items():
        G.add_node(li, kind="line", pts=tuple(sorted(ln)))
    for ln, li in line_idx.items():
        for p in ln:
            G.add_edge(point_idx[p], li)
    # sanity
    degs = [d for _, d in G.degree()]
    assert all(d == 4 for d in degs), f"degrees: {degs}"
    return G


if __name__ == "__main__":
    G = build_incidence_graph()
    print("nodes:", G.number_of_nodes(), "edges:", G.number_of_edges())
    print("degrees:", sorted(set(d for _, d in G.degree())))
    print("girth:", nx.girth(G))
    print("bipartite:", nx.is_bipartite(G))
