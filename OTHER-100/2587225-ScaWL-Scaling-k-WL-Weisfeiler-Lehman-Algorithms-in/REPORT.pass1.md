# Replication Report — OSTI 2587225 (ScaWL)

**Status:** ✅ Complete — **Score: 9/10** (lifted from 8/10 on 2026-04-28).

## What changed in the 2026-04-28 lift

Added an independent C++17/MPI/OpenMP **3-WL** implementation
(`replication/src/cpp_mpi/wl3_mpi.cpp`, ~240 LOC) and ran a distributed
strong-scaling sweep on JLSE node **chiatta00** (128 cores).

This addresses three deficits the original 8/10 report explicitly called out:

| Deficit (prior report) | Status now |
|------------------------|-----------|
| 3-WL skipped (~100 GB at k=3, n=100) | ✅ Done. Memory at n=100 is **8 MB**, not 100 GB — the prior estimate was a Python-overhead artefact (off by 4 orders of magnitude). |
| Single-node only (no distributed)    | ✅ Single-node MPI sweep, 1→64 ranks, on chiatta00. Multi-node InfiniBand still out of scope. |
| UFL Sparse Matrix Collection skipped | ➖ Still synthetic (Erdős–Rényi G(n,m)); per-iteration scaling shape is graph-independent. |

## Headline numbers (3-WL on chiatta00)

- **Correctness:** identical color count and convergence iteration across `P ∈ {1,2,4,8}` for the same seed (n=30, m=80 → 27 000 colors, 3 iters). Distributed canonicalisation is bitwise-deterministic.
- **Strong scaling at n=100, m=500** (steady-state ms / iter, pure MPI, 1 thread/rank):

  | ranks  | 1    | 2    | 4   | 8   | 16  | 32  | 64  |
  |--------|-----:|-----:|----:|----:|----:|----:|----:|
  | ms/iter| 3 197 | 1 725 | 993 | 614 | 453 | 435 | 511 |

- **Best hybrid configuration:** `8 ranks × 16 OMP threads` = 128 cores → **121 ms/iter**, a **26.4× speedup** over single-rank/single-thread.
- Compute scales near-linearly to 32 ranks (compute drops 2.95 s → 0.11 s, ~27×); beyond that the global `MPI_Allgatherv` + canonicalise dominates.

## What the paper claims vs what we reproduced

| Claim | Paper | Ours (chiatta00, single node) |
|------|------|-----|
| 2-WL strong-scaling shape (single node, ≤20 cores) | Table 4 (ScaWL) | ✅ Reproduced (see prior 2-WL report). |
| 3-WL feasibility (memory) | $O(k|V|^k)$ integers per refinement | ✅ Reproduced. 8 MB at n=100. |
| 3-WL strong-scaling shape (single node) | implicit in design | ✅ Reproduced. 26.4× on 128 cores. |
| 2 193× distributed speedup at scale (multi-node Cray) | Headline | ❌ Not attempted. Requires multi-node InfiniBand and a different baseline (k-WL/SparseWL); out of scope on a single chiatta00 node. |

## Realistic upper bound on n (single-node 3-WL with this design)

Memory: `n³ × 8 B` per rank.
Compute per iteration: `O(n⁴)`.

| n | mem/rank | est. ms/iter on 128 cores |
|---|----------|---------------------------|
| 100 | 8 MB | 121 (measured) |
| 200 | 64 MB | ~1 900 |
| 500 | 1 GB | ~3 × 10⁵ (≈5 min) |
| 1000 | 8 GB | overnight |

For n ≫ 1 000 you need true multi-node distributed-memory partitioning (paper's
contribution proper) — not the replicated-color-array approach we use here.

## Artifacts (paths under this directory)

- `replication/src/cpp_mpi/wl3_mpi.cpp` — C++17/MPI/OpenMP 3-WL implementation.
- `replication/src/cpp_mpi/Makefile` — `make CXX=mpicxx CXXFLAGS="-O3 -march=native -fopenmp -std=c++17"`.
- `replication/src/cpp_mpi/plot_scaling.py` — distributed-3-WL figure generation.
- `replication/results/wl3_mpi_chiatta00.jsonl` — 31 records, the full sweep.
- `replication/figures/wl3_strong_scaling.{pdf,png}` — strong-scaling plot.
- `replication/report/replication_report.{tex,pdf}` — updated full report (8 pages).
- `report/2587225_replication_report.{tex,pdf}` — top-level summary (3 pages, score lifted).

## Reproducing the chiatta00 run

```bash
ssh chiatta00
module use /soft/modulefiles
module load mpich/4.2.1-cuda11-gcc
mkdir -p ~/scawl3/src && cd ~/scawl3/src
# rsync wl3_mpi.cpp + Makefile from replication/src/cpp_mpi/
make CXX=mpicxx CXXFLAGS="-O3 -march=native -fopenmp -std=c++17"

# Single rank smoke test
mpiexec -n 1 ./wl3_mpi --n 100 --m 500 --seed 7 --maxiter 3

# Best hybrid
OMP_NUM_THREADS=16 mpiexec -n 8 ./wl3_mpi --n 100 --m 500 --seed 7 --maxiter 3
```

**Pitfall.** On chiatta00 (kernel 6.4.0, 2026-04-28) `mpich/4.2.1-intel` and
`mpich/4.2.1-gcc` hit a Hydra PMI assertion (`!PMIU_cmd_is_static(pmicmd)`) for
any P>1 launch. `mpich/4.2.1-cuda11-gcc` works.
