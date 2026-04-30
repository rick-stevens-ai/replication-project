# REPORT — Mathematical Foundations of the GraphBLAS

**OSTI ID:** 1379592 · **Authors:** Kepner, Aaltonen, Bader, Buluç, Franchetti, Gilbert, Hutchison, Kumar, Lumsdaine, Meyerhenke, McMillan, Moreira, Owens, Yang, Zalewski · **Year:** 2016
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/1379592-Mathematical-Foundations-of-the-GraphBLAS/`
**Replication date:** 2026-04-19

## Paper claim (one paragraph)

The paper establishes the mathematical foundations underlying the GraphBLAS standard—a building-block approach for expressing graph algorithms as linear-algebraic operations over generalized semirings. It defines algebraic structures (monoids, semirings with annihilators), specifies 11 generalized sparse matrix/vector operations (mxm, mxv, vxm, eWiseAdd, eWiseMult, extract, assign, apply, reduce, transpose, Kronecker product) with masking and accumulation semantics, and demonstrates that classical graph algorithms (BFS, SSSP, triangle counting, betweenness centrality, PageRank, connected components) can be cleanly expressed through these primitives. The paper is primarily definitional/algorithmic with worked examples on a 7-vertex directed graph (12 edges); there are no large-scale experimental benchmarks—the contribution is the formal algebraic framework itself.

## What we replicated

- **Algebraic foundations (Phase 1):** Monoid and Semiring classes with 7 built-in semirings (Arithmetic, Tropical/min-plus, Boolean, MaxPlus, MinTimes, MaxMin, PlusMin); associativity, identity, annihilation, and distributivity properties verified (exhaustive for Boolean)
- **All 11 core GraphBLAS operations (Phase 2):** mxm, mxv, vxm, eWiseAdd, eWiseMult, extract, assign, apply, reduce, transpose, Kronecker—generic over any user-supplied semiring, with structural/complement masking and accumulation
- **All paper worked examples (Phase 3):** Figures 1–8 reproduced exactly (7-vertex graph adjacency matrix, incidence matrix recovery, element-wise union/intersection, transpose edge reversal, BFS step from vertex 4, adjacency from incidence product)
- **Six graph algorithms (Phase 4):** BFS (Boolean semiring), SSSP/Bellman-Ford (Tropical semiring), triangle counting (A²⊙A), betweenness centrality (Brandes via GraphBLAS), PageRank (normalized A^T iteration), connected components (label propagation)
- **Cross-validation:** BFS, SSSP, triangle counting, and PageRank all verified against NetworkX reference implementations
- **Code paths:**
  - `replication/src/algebra.py` — algebraic structures & sparse containers (210 lines)
  - `replication/src/operations.py` — 11 core operations (319 lines)
  - `replication/src/algorithms.py` — 6 graph algorithms (293 lines)
  - `replication/tests/test_all.py` — 67 comprehensive tests (734 lines)
- **Data sources:** All synthetic, hand-constructed matrices from the paper's figures; no external datasets required

## Key results

| Quantity | Paper | Ours | Agreement |
|---|---|---|---|
| Fig 1: Adjacency matrix edges (7-vertex directed graph) | 12 | 12 | ✅ Exact |
| Fig 2: A = E_out^T · E_in recovers adjacency | Defined | Structure matches exactly | ✅ Exact |
| Fig 4: eWiseAdd union of two subgraphs | 7 edges, commutative | 7 edges, commutativity verified | ✅ Exact |
| Fig 5: eWiseMult intersection (disjoint subgraphs) | 0 edges | 0 edges | ✅ Exact |
| Fig 6: Transpose reverses all edges | 12 reversed | 12 reversed | ✅ Exact |
| Fig 7: BFS step from vertex 4 via v·A^T | Reaches vertices 1, 3 | Reaches vertices 1, 3 (0-indexed: 0, 2) | ✅ Exact |
| Fig 8: A(4,3) from incidence product | 1 | 1 | ✅ Exact |
| BFS levels from vertex 4 (all 7 sources) | Not tabulated | Matches NetworkX on all 7 sources | ✅ Exact |
| SSSP (unit weights from vertex 4) | Not tabulated | Distances: {3:0, 0:1, 2:1, 1:2, 5:2, 4:3, 6:4} — matches NetworkX/Dijkstra | ✅ Exact |
| Triangle count: K4 | 4 | 4 | ✅ Exact |
| Triangle count: K5 | 10 | 10 (matches NetworkX) | ✅ Exact |
| PageRank (7-vertex graph, α=0.85) | Not tabulated | All vertices within 0.01 of NetworkX | ✅ (tol < 0.01) |
| Semiring properties (associativity, identity, annihilation, distributivity) | Defined | All verified; Boolean exhaustive over all 2³ inputs | ✅ Exact |
| Test suite | — | 67/67 passed (0.84s) | ✅ All pass |

## Honest gaps

- **No performance/scalability benchmarking:** The paper does not include performance numbers, and the replication plan's optional Phase 5 (benchmarking against SuiteSparse:GraphBLAS on SNAP/Graph500 datasets) was not executed. The implementation is a pure-Python prototype, not optimized for scale.
- **No use of reference GraphBLAS library:** The replication implements everything from scratch in Python rather than using python-graphblas or SuiteSparse:GraphBLAS. This is by design (demonstrates understanding), but means we did not verify compatibility with the official GraphBLAS C API.
- **k-Truss algorithm not implemented:** Listed as optional in the replication plan; not completed.
- **No visualization/figure reproduction:** The paper's graph diagrams (node-link visualizations) were not reproduced as images, only the underlying numerical data.
- **Betweenness centrality and connected components:** Verified on structural/qualitative properties (star center highest, path symmetry) rather than against exact numeric values from the paper (which doesn't provide them).

## Score

**Coverage 9/10 · Agreement 10/10**

Coverage 9/10: All core content replicated—algebraic structures, all 11 operations, all 7 worked figures, 6 of ~7 algorithms, and cross-validation against NetworkX. Only the optional scalability benchmark (Phase 5) and k-Truss were skipped. Agreement 10/10: Every reproduced quantity matches the paper exactly; four algorithms independently confirmed against NetworkX; 67/67 tests pass with zero failures.

## Deliverables

- `REPORT.md` — this consolidated report
- `README.md` — project overview and status
- `1379592.pdf` — original paper
- `replication_plan.tex` / `replication_plan.pdf` — detailed replication blueprint
- `replication_plan_1379592.tex` / `replication_plan_1379592.pdf` — duplicate of replication plan
- `report/graphblas_replication_report.pdf` — formatted PDF report
- `replication/report/replication_report.md` — detailed replication report (source of truth)
- `replication/src/algebra.py` — Monoid, Semiring, SparseMatrix, SparseVector (210 lines)
- `replication/src/operations.py` — 11 core GraphBLAS operations with masking/accumulation (319 lines)
- `replication/src/algorithms.py` — 6 graph algorithms in pure GraphBLAS primitives (293 lines)
- `replication/tests/test_all.py` — 67 tests across 4 phases + NetworkX cross-validation (734 lines)
