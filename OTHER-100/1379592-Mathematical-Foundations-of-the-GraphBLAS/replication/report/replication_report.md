# Replication Report: Mathematical Foundations of the GraphBLAS

**Paper:** Kepner et al., "Mathematical Foundations of the GraphBLAS" (2016)  
**OSTI ID:** 1379592  
**Replication Date:** 2026-04-19  
**Verdict:** ✅ FULLY CONFIRMED

---

## 1. Overview

This paper establishes the mathematical foundations underlying the GraphBLAS standard — a framework for expressing graph algorithms as linear-algebraic operations over generalized semirings. The paper is primarily definitional and algorithmic rather than experimental, so replication means implementing the specified algebraic machinery from scratch, verifying it against the paper's worked examples, and demonstrating that classical graph algorithms can be correctly expressed through these primitives.

## 2. What Was Implemented

### Phase 1: Algebraic Foundations
- **Monoid** class: associative binary operator + identity element
- **Semiring** class: additive monoid + multiplicative monoid with annihilator
- **Built-in semirings**: Arithmetic (+,×), Tropical (min,+), Boolean (∨,∧), MaxPlus, MinTimes, MaxMin, PlusMin
- **Sparse containers**: SparseMatrix and SparseVector with structural zero semantics
- All algebraic properties verified: associativity, identity, annihilation, distributivity (exhaustive for Boolean)

### Phase 2: Core GraphBLAS Operations (10 operations)
| Operation | Description | Status |
|-----------|-------------|--------|
| mxm | Generalized matrix-matrix multiply | ✅ |
| mxv | Matrix-vector multiply | ✅ |
| vxm | Vector-matrix multiply | ✅ |
| eWiseAdd | Element-wise addition (union semantics) | ✅ |
| eWiseMult | Element-wise multiplication (intersection semantics) | ✅ |
| extract | Sub-matrix/vector extraction | ✅ |
| assign | Sub-matrix/vector assignment | ✅ |
| apply | Unary function application | ✅ |
| reduce | Matrix→vector or vector→scalar reduction | ✅ |
| transpose | Matrix transposition | ✅ |
| kronecker | Kronecker product over semiring | ✅ |

All operations are generic over any user-supplied semiring. Masking (structural, complement) and accumulation semantics are supported.

### Phase 3: Paper Example Verification

Every concrete numeric example from the paper was reproduced:

| Figure | Content | Result |
|--------|---------|--------|
| Fig 1 | 7-vertex directed graph, 12-edge adjacency matrix | ✅ Exact match (12 edges verified) |
| Fig 2 | Incidence matrices E_out, E_in; A = E_out^T · E_in | ✅ Recovered adjacency matrix exactly |
| Fig 4 | Element-wise addition (union of subgraphs) | ✅ 7 edges, commutativity verified |
| Fig 5 | Element-wise multiplication (intersection) | ✅ Empty intersection confirmed |
| Fig 6 | Transpose (edge reversal) | ✅ All 12 edges reversed correctly |
| Fig 7 | BFS step: v·A^T from vertex 4 | ✅ Reaches vertices 1,3 in one hop |
| Fig 8 | A(4,3) from incidence product | ✅ Value = 1 |

### Phase 4: Graph Algorithms

Six graph algorithms implemented **purely** using GraphBLAS primitives (no direct graph traversal):

| Algorithm | Method | Verification |
|-----------|--------|--------------|
| BFS | Boolean semiring mxv iteration | ✅ Matches NetworkX on all 7 source vertices |
| SSSP | Tropical semiring vxm (Bellman-Ford) | ✅ Matches NetworkX/Dijkstra on weighted graphs |
| Triangle Count | A²⊙A reduce (arithmetic semiring) | ✅ K4=4, K5=10, matches NetworkX |
| Betweenness Centrality | Brandes via GraphBLAS forward/backward pass | ✅ Star graph center highest, path symmetry |
| PageRank | Normalized A^T iteration with damping | ✅ Matches NetworkX within 0.01 tolerance |
| Connected Components | Label propagation via min | ✅ Correctly identifies components |

### Cross-Validation Against NetworkX
All four quantitative algorithms (BFS, SSSP, triangles, PageRank) were cross-validated against NetworkX reference implementations on the paper's 7-vertex graph and additional test graphs. All results match.

## 3. Test Summary

```
67 tests passed, 0 failed (0.84s)

Phase 1 — Algebraic Foundations:     19 tests ✅
Phase 2 — Core Operations:          22 tests ✅
Phase 3 — Paper Examples:            4 tests ✅
Phase 4 — Graph Algorithms:         18 tests ✅
Cross-validation vs NetworkX:        4 tests ✅
```

## 4. Implementation Details

- **Language:** Python 3.14
- **Dependencies:** pytest, networkx, numpy, scipy (for NetworkX PageRank only)
- **Lines of code:** ~750 (algebra + operations + algorithms + tests)
- **Runtime:** <1 second for all tests
- **No external GraphBLAS library used** — all operations implemented from first principles

## 5. Key Insights

1. **The semiring abstraction is powerful.** The same `mxm` code handles standard matrix multiply, shortest-path computation, and reachability analysis — just by swapping the semiring.

2. **Structural vs value zeros matter.** The distinction between "no edge" (structural zero) and "edge with weight 0" is critical for correctness, especially in eWiseAdd/eWiseMult semantics.

3. **Graph algorithms map cleanly to linear algebra.** BFS, SSSP, and triangle counting each reduce to 5-10 lines of GraphBLAS operations. The paper's claim that these primitives form a sufficient basis for graph computation is well-supported.

4. **The masked multiply pattern is central.** Triangle counting (B=A²; C=B⊙A; reduce(C)) demonstrates how masking enables efficient graph pattern matching through algebraic operations.

## 6. Files

```
src/algebra.py       — Monoid, Semiring, SparseMatrix, SparseVector
src/operations.py    — 11 core GraphBLAS operations  
src/algorithms.py    — 6 graph algorithms
tests/test_all.py    — 67 comprehensive tests
```

## 7. Conclusion

All claims in the paper are verified. The mathematical framework is correctly specified, the worked examples reproduce exactly, and classical graph algorithms are cleanly expressible through GraphBLAS primitives. The paper is a definitional work, and its definitions are internally consistent and practically useful.

**Replication status: FULLY CONFIRMED ✅**
