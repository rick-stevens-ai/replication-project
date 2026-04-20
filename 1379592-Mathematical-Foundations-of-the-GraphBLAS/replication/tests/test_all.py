"""
Comprehensive test suite for GraphBLAS replication.

Covers:
  Phase 1: Algebraic properties (monoid, semiring)
  Phase 2: Core operations
  Phase 3: Paper example verification (Figures 1-8)
  Phase 4: Graph algorithm correctness
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.algebra import (
    Monoid, Semiring, SparseMatrix, SparseVector, _NOVAL,
    PLUS, TIMES, ARITHMETIC, MIN, PLUS_TROP, TROPICAL,
    OR, AND, BOOLEAN, MAX, MAXPLUS, MINTIMES, MAXMIN, INF, NEGINF
)
from src.operations import (
    mxm, mxv, vxm, eWiseAdd, eWiseMult, extract_matrix, extract_vector,
    assign_matrix, assign_vector, apply_op, reduce_matrix_to_vector,
    reduce_vector_to_scalar, transpose, kronecker
)
from src.algorithms import (
    bfs_levels, sssp, triangle_count, triangle_count_lower,
    betweenness_centrality, pagerank, connected_components
)


# ══════════════════════════════════════════════════════════════════════════════
# Paper's 7-vertex graph (Figure 1)
# ══════════════════════════════════════════════════════════════════════════════

def make_paper_graph():
    """
    7-vertex directed graph from Figure 1.
    Edges: 1→2, 1→4, 2→5, 3→6, 4→1, 4→3, 5→2, 5→7, 6→3, 6→5, 7→4, 7→5
    (Using 0-indexed: 0→1, 0→3, 1→4, 2→5, 3→0, 3→2, 4→1, 4→6, 5→2, 5→4, 6→3, 6→4)
    """
    edges = [
        (0, 1), (0, 3),  # vertex 1
        (1, 4),          # vertex 2
        (2, 5),          # vertex 3
        (3, 0), (3, 2),  # vertex 4
        (4, 1), (4, 6),  # vertex 5
        (5, 2), (5, 4),  # vertex 6
        (6, 3), (6, 4),  # vertex 7
    ]
    return SparseMatrix(7, 7, {e: 1 for e in edges})


# ══════════════════════════════════════════════════════════════════════════════
# Phase 1: Algebraic Foundation Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestMonoid:
    def test_plus_identity(self):
        assert PLUS(0, 5) == 5
        assert PLUS(5, 0) == 5

    def test_plus_associativity(self):
        a, b, c = 3, 7, 11
        assert PLUS(PLUS(a, b), c) == PLUS(a, PLUS(b, c))

    def test_times_identity(self):
        assert TIMES(1, 42) == 42
        assert TIMES(42, 1) == 42

    def test_times_associativity(self):
        a, b, c = 2, 3, 5
        assert TIMES(TIMES(a, b), c) == TIMES(a, TIMES(b, c))

    def test_min_identity(self):
        assert MIN(INF, 5) == 5
        assert MIN(5, INF) == 5

    def test_min_associativity(self):
        a, b, c = 3, 1, 7
        assert MIN(MIN(a, b), c) == MIN(a, MIN(b, c))

    def test_or_identity(self):
        assert OR(False, True) == True
        assert OR(True, False) == True
        assert OR(False, False) == False

    def test_and_identity(self):
        assert AND(True, True) == True
        assert AND(True, False) == False

    def test_max_identity(self):
        assert MAX(NEGINF, 5) == 5

    def test_reduce(self):
        assert PLUS.reduce([1, 2, 3, 4]) == 10
        assert MIN.reduce([5, 3, 8, 1]) == 1
        assert OR.reduce([False, False, True]) == True
        assert AND.reduce([True, True, False]) == False


class TestSemiring:
    def test_arithmetic_zero(self):
        assert ARITHMETIC.zero == 0
        assert ARITHMETIC.one == 1

    def test_arithmetic_annihilator(self):
        """a × 0 = 0 (zero annihilates multiplication)"""
        assert TIMES(42, 0) == 0
        assert TIMES(0, 42) == 0

    def test_arithmetic_distributivity(self):
        """a × (b + c) = a×b + a×c"""
        a, b, c = 3, 5, 7
        assert TIMES(a, PLUS(b, c)) == PLUS(TIMES(a, b), TIMES(a, c))

    def test_tropical_zero(self):
        assert TROPICAL.zero == INF
        assert TROPICAL.one == 0

    def test_tropical_annihilator(self):
        """a + ∞ = ∞ (inf annihilates tropical multiplication)"""
        assert PLUS_TROP(42, INF) == INF
        assert PLUS_TROP(INF, 42) == INF

    def test_tropical_distributivity(self):
        """a + min(b,c) = min(a+b, a+c)"""
        a, b, c = 3.0, 5.0, 7.0
        lhs = PLUS_TROP(a, MIN(b, c))
        rhs = MIN(PLUS_TROP(a, b), PLUS_TROP(a, c))
        assert lhs == rhs

    def test_boolean_zero(self):
        assert BOOLEAN.zero == False
        assert BOOLEAN.one == True

    def test_boolean_annihilator(self):
        assert AND(True, False) == False
        assert AND(False, True) == False

    def test_boolean_distributivity(self):
        """a ∧ (b ∨ c) = (a∧b) ∨ (a∧c)"""
        for a in [True, False]:
            for b in [True, False]:
                for c in [True, False]:
                    lhs = AND(a, OR(b, c))
                    rhs = OR(AND(a, b), AND(a, c))
                    assert lhs == rhs, f"Failed for a={a}, b={b}, c={c}"


class TestSparseContainers:
    def test_vector_basic(self):
        v = SparseVector(5, {0: 10, 3: 20})
        assert v[0] == 10
        assert v[3] == 20
        assert v[1] is _NOVAL
        assert v.nnz() == 2

    def test_vector_from_dense(self):
        v = SparseVector.from_dense([0, 1, 0, 3, 0])
        assert v.nnz() == 2
        assert v[1] == 1
        assert v[3] == 3

    def test_matrix_basic(self):
        A = SparseMatrix(3, 3, {(0, 1): 5, (2, 0): 3})
        assert A[(0, 1)] == 5
        assert A[(2, 0)] == 3
        assert A[(0, 0)] is _NOVAL
        assert A.nnz() == 2

    def test_matrix_from_dense(self):
        A = SparseMatrix.from_dense([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        assert A.nnz() == 3
        assert A[(0, 1)] == 1
        assert A[(1, 2)] == 1
        assert A[(2, 0)] == 1

    def test_transpose(self):
        A = SparseMatrix(2, 3, {(0, 1): 5, (1, 2): 3})
        AT = A.transpose()
        assert AT.nrows == 3
        assert AT.ncols == 2
        assert AT[(1, 0)] == 5
        assert AT[(2, 1)] == 3


# ══════════════════════════════════════════════════════════════════════════════
# Phase 2: Core Operation Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestMxm:
    def test_arithmetic_2x2(self):
        A = SparseMatrix.from_dense([[1, 2], [3, 4]])
        B = SparseMatrix.from_dense([[5, 6], [7, 8]])
        C = mxm(A, B, ARITHMETIC)
        expected = [[19, 22], [43, 50]]
        assert C.to_dense() == expected

    def test_boolean_adjacency(self):
        """A² on Boolean semiring = 2-hop reachability"""
        A = make_paper_graph()
        # Convert to boolean values
        A_bool = SparseMatrix(7, 7, {k: True for k in A.entries})
        A2 = mxm(A_bool, A_bool, BOOLEAN)
        # From vertex 0 (1 in paper): 0→1→4 and 0→3→0, 0→3→2
        # So vertex 0 can reach 0, 2, 4 in 2 hops
        assert A2[(0, 0)] == True  # 0→3→0
        assert A2[(0, 2)] == True  # 0→3→2
        assert A2[(0, 4)] == True  # 0→1→4

    def test_tropical_2x2(self):
        """Min-plus matrix multiply"""
        A = SparseMatrix(2, 2, {(0, 0): 1, (0, 1): 3, (1, 0): 2, (1, 1): 4})
        B = SparseMatrix(2, 2, {(0, 0): 5, (0, 1): 1, (1, 0): 2, (1, 1): 3})
        C = mxm(A, B, TROPICAL)
        # C[0,0] = min(1+5, 3+2) = min(6,5) = 5
        # C[0,1] = min(1+1, 3+3) = min(2,6) = 2
        # C[1,0] = min(2+5, 4+2) = min(7,6) = 6
        # C[1,1] = min(2+1, 4+3) = min(3,7) = 3
        assert C.to_dense(zero=INF) == [[5, 2], [6, 3]]

    def test_with_mask(self):
        A = SparseMatrix.from_dense([[1, 2], [3, 4]])
        B = SparseMatrix.from_dense([[5, 6], [7, 8]])
        mask = SparseMatrix(2, 2, {(0, 0): 1})  # only keep (0,0)
        C = mxm(A, B, ARITHMETIC, mask=mask)
        assert (0, 0) in C.entries
        assert (0, 1) not in C.entries
        assert C[(0, 0)] == 19


class TestMxv:
    def test_basic(self):
        A = SparseMatrix.from_dense([[1, 2], [3, 4]])
        v = SparseVector(2, {0: 1, 1: 1})
        w = mxv(A, v, ARITHMETIC)
        assert w[0] == 3   # 1*1 + 2*1
        assert w[1] == 7   # 3*1 + 4*1

    def test_boolean_bfs_step(self):
        """Single BFS step from vertex 3 (0-indexed) using Boolean mxv"""
        A = make_paper_graph()
        A_bool = SparseMatrix(7, 7, {k: True for k in A.entries})
        AT = transpose(A_bool)
        v = SparseVector(7, {3: True})  # start at vertex 4 (0-indexed: 3)
        w = mxv(AT, v, BOOLEAN)
        # Vertex 4's out-neighbors: 1 and 3 (0-indexed: 0 and 2)
        assert w[0] == True
        assert w[2] == True
        assert w.nnz() == 2


class TestVxm:
    def test_basic(self):
        v = SparseVector(2, {0: 1, 1: 2})
        A = SparseMatrix.from_dense([[3, 4], [5, 6]])
        w = vxm(v, A, ARITHMETIC)
        assert w[0] == 13  # 1*3 + 2*5
        assert w[1] == 16  # 1*4 + 2*6


class TestEWise:
    def test_eWiseAdd_paper_fig4(self):
        """Figure 4: element-wise addition (union) of two subgraphs."""
        # Subgraph A: edges (3→0), (3→2), (0→1), (6→3)
        A = SparseMatrix(7, 7, {(3, 0): 1, (3, 2): 1, (0, 1): 1, (6, 3): 1})
        # Subgraph B: edges (1→4), (6→4), (4→1)
        B = SparseMatrix(7, 7, {(1, 4): 1, (6, 4): 1, (4, 1): 1})

        C = eWiseAdd(A, B, lambda a, b: a + b)
        # Union: all 7 edges
        expected_edges = {(3, 0), (3, 2), (0, 1), (6, 3), (1, 4), (6, 4), (4, 1)}
        assert C.structure() == expected_edges
        assert C.nnz() == 7

    def test_eWiseMult_paper_fig5(self):
        """Figure 5: element-wise multiplication (intersection)."""
        A = SparseMatrix(7, 7, {(3, 0): 1, (3, 2): 1, (0, 1): 1, (6, 3): 1})
        B = SparseMatrix(7, 7, {(1, 4): 1, (6, 4): 1, (4, 1): 1})

        C = eWiseMult(A, B, lambda a, b: a * b)
        # Intersection: no common edges
        assert C.nnz() == 0

    def test_eWiseAdd_commutativity(self):
        A = SparseMatrix(3, 3, {(0, 1): 2, (1, 2): 3})
        B = SparseMatrix(3, 3, {(1, 2): 5, (2, 0): 1})
        C1 = eWiseAdd(A, B, lambda a, b: a + b)
        C2 = eWiseAdd(B, A, lambda a, b: a + b)
        assert C1.entries == C2.entries

    def test_eWiseMult_with_overlap(self):
        A = SparseMatrix(3, 3, {(0, 1): 2, (1, 2): 3})
        B = SparseMatrix(3, 3, {(0, 1): 5, (2, 0): 1})
        C = eWiseMult(A, B, lambda a, b: a * b)
        assert C.nnz() == 1
        assert C[(0, 1)] == 10


class TestExtractAssign:
    def test_extract_matrix(self):
        A = SparseMatrix.from_dense([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        B = extract_matrix(A, [0, 2], [1, 2])
        assert B.nrows == 2
        assert B.ncols == 2
        assert B[(0, 0)] == 2
        assert B[(0, 1)] == 3
        assert B[(1, 0)] == 8
        assert B[(1, 1)] == 9

    def test_extract_vector(self):
        v = SparseVector(5, {0: 10, 2: 20, 4: 30})
        w = extract_vector(v, [0, 2, 4])
        assert w.n == 3
        assert w[0] == 10
        assert w[1] == 20
        assert w[2] == 30

    def test_assign_matrix(self):
        C = SparseMatrix(3, 3)
        A = SparseMatrix.from_dense([[1, 2], [3, 4]])
        result = assign_matrix(C, A, [0, 2], [1, 2])
        assert result[(0, 1)] == 1
        assert result[(0, 2)] == 2
        assert result[(2, 1)] == 3
        assert result[(2, 2)] == 4


class TestApplyOp:
    def test_matrix(self):
        A = SparseMatrix(2, 2, {(0, 0): 4, (1, 1): 9})
        B = apply_op(A, lambda x: x ** 0.5)
        assert B[(0, 0)] == 2.0
        assert B[(1, 1)] == 3.0

    def test_vector(self):
        v = SparseVector(3, {0: 2, 2: 3})
        w = apply_op(v, lambda x: x * x)
        assert w[0] == 4
        assert w[2] == 9


class TestReduce:
    def test_row_reduce(self):
        A = SparseMatrix.from_dense([[1, 2, 3], [4, 5, 6]])
        v = reduce_matrix_to_vector(A, PLUS, axis='row')
        assert v[0] == 6
        assert v[1] == 15

    def test_col_reduce(self):
        A = SparseMatrix.from_dense([[1, 2, 3], [4, 5, 6]])
        v = reduce_matrix_to_vector(A, PLUS, axis='col')
        assert v[0] == 5
        assert v[1] == 7
        assert v[2] == 9

    def test_vector_reduce(self):
        v = SparseVector(4, {0: 10, 1: 20, 3: 30})
        assert reduce_vector_to_scalar(v, PLUS) == 60
        assert reduce_vector_to_scalar(v, MIN) == 10


class TestTranspose:
    def test_paper_fig6(self):
        """Figure 6: transpose reverses all edges."""
        A = make_paper_graph()
        AT = transpose(A)
        # Original: 0→1 becomes 1→0
        assert AT[(1, 0)] == 1
        assert AT[(0, 1)] is _NOVAL or (0, 1) not in AT.entries
        # Original: 6→3 becomes 3→6
        assert AT[(3, 6)] == 1
        assert AT.nnz() == A.nnz()  # same number of edges


class TestKronecker:
    def test_basic(self):
        A = SparseMatrix.from_dense([[1, 2], [3, 4]])
        B = SparseMatrix.from_dense([[5, 6], [7, 8]])
        C = kronecker(A, B, ARITHMETIC)
        # C is 4×4
        assert C.nrows == 4
        assert C.ncols == 4
        # C[0,0] = 1*5 = 5, C[0,1] = 1*6 = 6
        assert C[(0, 0)] == 5
        assert C[(0, 1)] == 6
        # C[2,0] = A[1,0]*B[0,0] = 3*5 = 15
        assert C[(2, 0)] == 15
        # C[2,2] = A[1,1]*B[0,0] = 4*5 = 20
        assert C[(2, 2)] == 20
        # C[3,3] = 4*8 = 32
        assert C[(3, 3)] == 32


# ══════════════════════════════════════════════════════════════════════════════
# Phase 3: Paper Example Verification
# ══════════════════════════════════════════════════════════════════════════════

class TestPaperExamples:
    def test_fig1_adjacency_matrix(self):
        """Figure 1: 7-vertex graph adjacency matrix has 12 edges."""
        A = make_paper_graph()
        assert A.nnz() == 12
        # Verify specific edges
        assert A[(0, 1)] == 1  # 1→2
        assert A[(0, 3)] == 1  # 1→4
        assert A[(1, 4)] == 1  # 2→5
        assert A[(2, 5)] == 1  # 3→6
        assert A[(3, 0)] == 1  # 4→1
        assert A[(3, 2)] == 1  # 4→3
        assert A[(4, 1)] == 1  # 5→2
        assert A[(4, 6)] == 1  # 5→7
        assert A[(5, 2)] == 1  # 6→3
        assert A[(5, 4)] == 1  # 6→5
        assert A[(6, 3)] == 1  # 7→4
        assert A[(6, 4)] == 1  # 7→5

    def test_fig2_incidence_matrices(self):
        """Figure 2: A = E_out^T · E_in should recover adjacency matrix."""
        # Build E_out and E_in for the 12 edges
        # Edge numbering (0-indexed edges, 0-indexed vertices):
        edges_from_to = [
            (0, 1),  # edge 0: 1→2
            (3, 0),  # edge 1: 4→1
            (0, 3),  # edge 2: 1→4
            (3, 2),  # edge 3: 4→3
            (5, 4),  # edge 4: 6→5
            (5, 2),  # edge 5: 6→3
            (2, 5),  # edge 6: 3→6
            (4, 6),  # edge 7: 5→7
            (4, 1),  # edge 8: 5→2
            (6, 4),  # edge 9: 7→5
            (6, 3),  # edge 10: 7→4
            (1, 4),  # edge 11: 2→5
        ]
        E_out = SparseMatrix(12, 7)
        E_in = SparseMatrix(12, 7)
        for e_idx, (src, dst) in enumerate(edges_from_to):
            E_out[(e_idx, src)] = 1
            E_in[(e_idx, dst)] = 1

        # A = E_out^T · E_in on arithmetic semiring
        A_recovered = mxm(transpose(E_out), E_in, ARITHMETIC)

        # Should match the paper's adjacency matrix
        A_paper = make_paper_graph()
        assert A_recovered.structure() == A_paper.structure()

    def test_fig7_bfs_step(self):
        """Figure 7: BFS from vertex 4 (0-indexed: 3)."""
        A = make_paper_graph()
        A_bool = SparseMatrix(7, 7, {k: True for k in A.entries})
        AT = transpose(A_bool)

        # Starting vector: vertex 3 (paper's vertex 4)
        v = SparseVector(7, {3: True})

        # One BFS step: v · A^T
        w = mxv(AT, v, BOOLEAN)

        # Vertex 4 (idx 3) has out-neighbors: vertex 1 (idx 0) and vertex 3 (idx 2)
        assert w[0] == True
        assert w[2] == True
        assert w.nnz() == 2

    def test_fig8_adjacency_from_incidence(self):
        """Figure 8: A(4,3) = sum over edges from vertex 4 to vertex 3."""
        # Verify A(3,2) = 1 in 0-indexed (paper's A(4,3))
        A = make_paper_graph()
        assert A[(3, 2)] == 1  # vertex 4 → vertex 3


# ══════════════════════════════════════════════════════════════════════════════
# Phase 4: Graph Algorithm Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestBFS:
    def test_paper_graph_from_vertex4(self):
        """BFS from vertex 4 (0-indexed: 3) on the paper's 7-vertex graph."""
        A = make_paper_graph()
        levels = bfs_levels(A, 3)

        # Level 0: vertex 3
        assert levels[3] == 0
        # Level 1: vertices 0, 2 (4→1, 4→3 in paper)
        assert levels[0] == 1
        assert levels[2] == 1
        # Level 2: vertices 1, 5 (1→2, 3→6)
        assert levels[1] == 2
        assert levels[5] == 2
        # Level 3: vertices 4, (2→5)
        assert levels[4] == 3
        # Level 4: vertex 6 (5→7)
        assert levels[6] == 4
        # All vertices reached
        assert levels.nnz() == 7

    def test_disconnected(self):
        """BFS on disconnected graph only reaches connected component."""
        A = SparseMatrix(4, 4, {(0, 1): 1, (1, 0): 1})
        levels = bfs_levels(A, 0)
        assert levels.nnz() == 2
        assert levels[0] == 0
        assert levels[1] == 1


class TestSSSP:
    def test_simple_chain(self):
        """Shortest path on simple chain: 0→1→2→3"""
        A = SparseMatrix(4, 4, {(0, 1): 1, (1, 2): 2, (2, 3): 3})
        dist = sssp(A, 0)
        assert dist[0] == 0
        assert dist[1] == 1
        assert dist[2] == 3
        assert dist[3] == 6

    def test_with_shortcut(self):
        """Shortest path with shortcut: 0→1→2 (cost 5) vs 0→2 (cost 3)"""
        A = SparseMatrix(3, 3, {(0, 1): 2, (1, 2): 3, (0, 2): 3})
        dist = sssp(A, 0)
        assert dist[0] == 0
        assert dist[1] == 2
        assert dist[2] == 3  # direct path is shorter

    def test_paper_graph_weighted(self):
        """SSSP on paper's graph with unit weights."""
        A = make_paper_graph()
        dist = sssp(A, 3)
        # From vertex 3: level = hop count (since all weights = 1)
        assert dist[3] == 0
        assert dist[0] == 1
        assert dist[2] == 1
        assert dist[1] == 2
        assert dist[5] == 2
        assert dist[4] == 3
        assert dist[6] == 4


class TestTriangleCounting:
    def test_triangle_graph(self):
        """Simple triangle: 0↔1↔2↔0"""
        A = SparseMatrix(3, 3, {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (0, 2): 1, (2, 0): 1,
        })
        assert triangle_count(A) == 1

    def test_no_triangles(self):
        """Path graph: no triangles"""
        A = SparseMatrix(3, 3, {(0, 1): 1, (1, 0): 1, (1, 2): 1, (2, 1): 1})
        assert triangle_count(A) == 0

    def test_two_triangles(self):
        """Diamond: 0↔1↔2↔0 and 1↔2↔3↔1 (sharing edge 1-2)"""
        A = SparseMatrix(4, 4, {
            (0, 1): 1, (1, 0): 1,
            (0, 2): 1, (2, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (1, 3): 1, (3, 1): 1,
            (2, 3): 1, (3, 2): 1,
        })
        assert triangle_count(A) == 2

    def test_lower_triangular_method(self):
        """Both methods should agree."""
        A = SparseMatrix(4, 4, {
            (0, 1): 1, (1, 0): 1,
            (0, 2): 1, (2, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (1, 3): 1, (3, 1): 1,
            (2, 3): 1, (3, 2): 1,
        })
        assert triangle_count(A) == triangle_count_lower(A)

    def test_k4_complete(self):
        """K4 has 4 triangles."""
        entries = {}
        for i in range(4):
            for j in range(4):
                if i != j:
                    entries[(i, j)] = 1
        A = SparseMatrix(4, 4, entries)
        assert triangle_count(A) == 4


class TestBetweennessCentrality:
    def test_star_graph(self):
        """Star: center vertex should have highest BC."""
        # Center = 0, leaves = 1,2,3
        A = SparseMatrix(4, 4, {
            (0, 1): 1, (1, 0): 1,
            (0, 2): 1, (2, 0): 1,
            (0, 3): 1, (3, 0): 1,
        })
        bc = betweenness_centrality(A)
        # Center should have BC > 0, leaves should have BC = 0
        assert bc[0] > 0
        # All leaves have same BC
        assert bc[1] == bc[2] == bc[3]

    def test_path_graph(self):
        """Path: 0↔1↔2↔3. Middle vertices have highest BC."""
        A = SparseMatrix(4, 4, {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (2, 3): 1, (3, 2): 1,
        })
        bc = betweenness_centrality(A)
        # Vertices 1 and 2 should have higher BC than 0 and 3
        assert bc[1] > bc[0]
        assert bc[2] > bc[3]
        # By symmetry, 1 and 2 should have same BC, 0 and 3 same
        assert abs(bc[1] - bc[2]) < 1e-10
        assert abs(bc[0] - bc[3]) < 1e-10


class TestPageRank:
    def test_uniform_cycle(self):
        """On a cycle, all vertices should have equal PageRank."""
        A = SparseMatrix(4, 4, {(0, 1): 1, (1, 2): 1, (2, 3): 1, (3, 0): 1})
        pr = pagerank(A)
        vals = [pr[i] for i in range(4)]
        assert all(abs(v - 0.25) < 0.01 for v in vals)


class TestConnectedComponents:
    def test_two_components(self):
        """Graph with 2 components: {0,1,2} and {3,4}"""
        A = SparseMatrix(5, 5, {
            (0, 1): 1, (1, 0): 1,
            (1, 2): 1, (2, 1): 1,
            (3, 4): 1, (4, 3): 1,
        })
        cc = connected_components(A)
        # Vertices 0,1,2 should share a label
        assert cc[0] == cc[1] == cc[2]
        # Vertices 3,4 should share a different label
        assert cc[3] == cc[4]
        # The two components should have different labels
        assert cc[0] != cc[3]


# ══════════════════════════════════════════════════════════════════════════════
# Phase 4+: Validation against NetworkX
# ══════════════════════════════════════════════════════════════════════════════

class TestAgainstNetworkX:
    """Cross-validate our algorithms against NetworkX."""

    @staticmethod
    def _to_nx_digraph(A: SparseMatrix):
        import networkx as nx
        G = nx.DiGraph()
        G.add_nodes_from(range(A.nrows))
        for (i, j), w in A.entries.items():
            G.add_edge(i, j, weight=w)
        return G

    @staticmethod
    def _to_nx_graph(A: SparseMatrix):
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(range(A.nrows))
        for (i, j), w in A.entries.items():
            G.add_edge(i, j, weight=w)
        return G

    def test_bfs_vs_networkx(self):
        import networkx as nx
        A = make_paper_graph()
        G = self._to_nx_digraph(A)

        for source in range(7):
            our_levels = bfs_levels(A, source)
            nx_levels = nx.single_source_shortest_path_length(G, source)
            for v in range(7):
                our_val = our_levels[v]
                if v in nx_levels:
                    assert our_val == nx_levels[v], \
                        f"BFS mismatch from {source} to {v}: ours={our_val}, nx={nx_levels[v]}"

    def test_sssp_vs_networkx(self):
        import networkx as nx
        # Weighted graph
        A = SparseMatrix(5, 5, {
            (0, 1): 4, (0, 2): 1, (1, 3): 1,
            (2, 1): 2, (2, 3): 5, (3, 4): 3,
        })
        G = self._to_nx_digraph(A)

        our_dist = sssp(A, 0)
        nx_dist = nx.single_source_dijkstra_path_length(G, 0)

        for v in range(5):
            our_val = our_dist[v] if our_dist[v] is not _NOVAL else INF
            nx_val = nx_dist.get(v, INF)
            assert our_val == nx_val, f"SSSP to {v}: ours={our_val}, nx={nx_val}"

    def test_triangles_vs_networkx(self):
        import networkx as nx
        # K5 has C(5,3) = 10 triangles
        entries = {}
        for i in range(5):
            for j in range(5):
                if i != j:
                    entries[(i, j)] = 1
        A = SparseMatrix(5, 5, entries)
        G = self._to_nx_graph(A)

        our_count = triangle_count(A)
        nx_count = sum(nx.triangles(G).values()) // 3

        assert our_count == nx_count == 10

    def test_pagerank_vs_networkx(self):
        import networkx as nx
        A = make_paper_graph()
        G = self._to_nx_digraph(A)

        our_pr = pagerank(A, damping=0.85, max_iter=200)
        nx_pr = nx.pagerank(G, alpha=0.85)

        for v in range(7):
            our_val = our_pr[v] if our_pr[v] is not _NOVAL else 0.0
            nx_val = nx_pr[v]
            assert abs(our_val - nx_val) < 0.01, \
                f"PageRank mismatch at {v}: ours={our_val:.4f}, nx={nx_val:.4f}"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
