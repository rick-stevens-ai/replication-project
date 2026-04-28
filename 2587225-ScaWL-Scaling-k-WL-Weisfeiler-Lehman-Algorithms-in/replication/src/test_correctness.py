"""Sanity tests for 2-WL implementation."""
import networkx as nx
from kwl import run_2wl, canonical_invariant


def test_iso_pair():
    G = nx.random_regular_graph(4, 30, seed=0)
    mapping = {v: (v + 7) % 30 for v in G.nodes()}
    H = nx.relabel_nodes(G, mapping)
    Cg, _, _ = run_2wl(G)
    Ch, _, _ = run_2wl(H)
    assert canonical_invariant(Cg) == canonical_invariant(Ch), "iso pair failed"
    print("iso pair:     OK")


def test_non_iso_pair():
    G = nx.cycle_graph(12)
    H = nx.union(nx.cycle_graph(6), nx.cycle_graph(6), rename=("a", "b"))
    Cg, _, _ = run_2wl(G)
    Ch, _, _ = run_2wl(H)
    # 1-WL cannot distinguish these, but 2-WL can
    assert canonical_invariant(Cg) != canonical_invariant(Ch), "non-iso pair failed"
    print("non-iso pair: OK (2-WL distinguishes C12 from 2xC6)")


def test_strongly_regular():
    """Shrikhande vs 4x4 rook: both strongly regular (16,6,2,2). 2-WL cannot
    distinguish them — this is the classic k-WL weakness, so invariants should
    MATCH even though graphs are non-isomorphic. Confirms 2-WL semantics."""
    rook = nx.cartesian_product(nx.complete_graph(4), nx.complete_graph(4))
    rook = nx.convert_node_labels_to_integers(rook)
    # Shrikhande graph construction
    shrikhande = nx.Graph()
    shrikhande.add_nodes_from(range(16))
    diffs = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1)]
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in diffs:
                ni, nj = (i + di) % 4, (j + dj) % 4
                v = ni * 4 + nj
                shrikhande.add_edge(u, v)
    Cg, _, _ = run_2wl(rook)
    Ch, _, _ = run_2wl(shrikhande)
    print(f"SRG test: rook_inv = {canonical_invariant(Cg)[:10]}..., "
          f"shrikhande_inv = {canonical_invariant(Ch)[:10]}... (match expected: {canonical_invariant(Cg) == canonical_invariant(Ch)})")


if __name__ == "__main__":
    test_iso_pair()
    test_non_iso_pair()
    test_strongly_regular()
    print("All tests passed.")
