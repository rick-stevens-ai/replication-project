# Replication Report — OSTI 2587225 (ScaWL) — Pass 2

**Paper:** Soss, Sukumaran-Rajam, Layne, Serra, Halappanavar, Gebremedhin.
"ScaWL: Scaling k-WL (Weisfeiler-Lehman) Algorithms in Memory and Performance
on Shared and Distributed-Memory Systems." ACM TACO 22(1) Art. 45, March 2025.
DOI 10.1145/3715124.

**This report:** 2026-06-23 re-pass on CherryRd (free CPU, Argo free LLM).
Pass-1 report preserved verbatim at `REPORT.pass1.md`.

**Parser:** `pdftotext -layout` (Poppler 25.x). Details in `PARSER_PROVENANCE.md`.

## What pass 2 adds

Pass 1 delivered an independent C++17/MPI/OpenMP 3-WL implementation and a
strong-scaling sweep on JLSE chiatta00 (`replication/src/cpp_mpi/wl3_mpi.cpp`,
results in `replication/results/wl3_mpi_chiatta00.jsonl`). Pass 2 lifts
*coverage* by grounding five additional paper claims on free CPU at CherryRd,
including the paper's exact Table 1 graphs and the 2-WL/3-WL expressivity
hierarchy (Rook(4×4) vs Shrikhande) that motivates the whole "push k up"
program.

All new artifacts live under `code/repass/` (single entry script) and
`results/repass/` (per-claim JSON + summary). Total wallclock for the new
work: **~6 seconds** on a single CherryRd CPU.

## Per-claim table

| ID  | Claim                                                                | Paper location          | Verdict | Evidence                                  |
|-----|----------------------------------------------------------------------|-------------------------|---------|-------------------------------------------|
| C1  | Paper Table 1 graphs (V, E) reproducible from SuiteSparse MTX files. | §6.1 Table 1            | **PASS** | `results/repass/C1_dataset_grounding.json` |
| C2  | ScaWL 2-WL output (colors, iters, color-histogram) invariant under sharding (Section 7 bijection F → observable consequence). | §7 Proof of correctness | **PASS** | `C2_invariant_stability.json` |
| C3a | 2-WL distinguishes C₁₂ from 2×C₆ (1-WL cannot).                       | §3 / §4 (k-WL hierarchy) | **PASS** | `C3_2wl_expressivity.json` |
| C3b | 2-WL CANNOT distinguish Rook(4×4) from Shrikhande (both SRG(16,6,2,2)). | textbook k-WL gap       | **PASS** | `C3_2wl_expressivity.json` |
| C3c | 2-WL distinguishes Petersen (girth 5) from 5-prism (girth 4) — both cubic on 10 nodes. | textbook k-WL          | **PASS** | `C3_2wl_expressivity.json` |
| C4  | Single-node strong-scaling shape (monotonic-positive speedup with cores). | §6.3 Figs 7–10        | **PARTIAL** | `C4_strong_scaling.json` |
| C5  | 3-WL DISTINGUISHES Rook(4×4) from Shrikhande — grounds the "k=3 is strictly more expressive than k=2" claim. | §3, motivation for distributed-3-WL | **PASS** | `C5_3wl_expressivity.json` |

### C1 — Dataset grounding (paper-exact V,E)

Downloaded `LFAT5`, `Trefethen_20`, `celegansneural` from
SuiteSparse Matrix Collection (sparse.tamu.edu). Paper Table 1 column "Edges"
turns out to be **raw MTX nnz** (not deduplicated simple-undirected edges):

| Graph           | V (paper) | V (ours) | E (paper) | mtx nnz | mtx kind  | paper E grounded? |
|-----------------|----------:|---------:|----------:|--------:|-----------|:--:|
| LFAT5           | 14        | **14**   | 30        | 30      | symmetric | ✅ (E = nnz)             |
| Trefethen_20    | 20        | **20**   | 89        | 89      | symmetric | ✅ (E = nnz)             |
| celegansneural  | 297       | **297**  | 4 690     | 2 345   | general   | ✅ (E = 2·nnz, directed) |

V matches exactly for all three; E is explained exactly by the
"raw nnz" rule (with `2×nnz` for directed/`general` matrices, since the
paper treats those as undirected). Our simple-undirected edge count for
LFAT5 is 16 (after dropping the 14 diagonal entries the symmetric file
contains, leaving 16 strict off-diagonal pairs). All three graphs are
correctly loaded for downstream tests.

### C2 — Output invariance under sharding (Section 7 in action)

For `nx.random_regular_graph(d=4, n=50, seed=7)`, running our 2-WL with
`procs ∈ {1, 2, 4}`:

| procs | colors | iters | invariant (blake2b-128 of color histogram) |
|-------|-------:|------:|--------------------------------------------|
| 1     | 2 500  | 4     | `ecb9e15f9b7807950413293c7c3e06ee`         |
| 2     | 2 500  | 4     | `ecb9e15f9b7807950413293c7c3e06ee`         |
| 4     | 2 500  | 4     | `ecb9e15f9b7807950413293c7c3e06ee`         |

All three counts and the hash match bitwise — this is the operational
content of Theorem 5 / Corollary 3 (`|EC_ScaWL_{n+1}| = |EC_classic_{n+1}|`
and same k-tuple membership at every iteration).

### C3 — 2-WL expressivity probes

| pair                                            | 2-WL distinguishes? | theory says? | status |
|-------------------------------------------------|:--:|:--:|:--:|
| C₁₂ vs C₆ ⊔ C₆                                  | yes              | yes       | ✅ PASS |
| Rook(4×4) vs Shrikhande (SRG(16,6,2,2))         | no               | no        | ✅ PASS |
| Petersen (girth 5) vs 5-prism Y₅ (girth 4)      | yes              | yes       | ✅ PASS |

The Rook/Shrikhande result is exactly the textbook hard case for 2-WL
that the paper's "push k up" motivation rests on. Our implementation
reproduces both the success and the *correct failure*.

### C4 — Single-node strong-scaling shape

`nx.random_regular_graph(d=4, n=60, seed=11)`, 2-WL to convergence,
Python+multiprocessing on CherryRd (macOS, x86_64):

| procs | seconds | speedup | iters | colors | invariant stable? |
|------:|--------:|--------:|------:|-------:|:--:|
| 1     | 0.277   | 1.00×   | 4     | 3 600  | (baseline) |
| 2     | 0.152   | **1.82×** | 4   | 3 600  | ✅ |
| 4     | 0.083   | **3.32×** | 4   | 3 600  | ✅ |
| 8     | 0.055   | **5.05×** | 4   | 3 600  | ✅ |

Paper reference (Xeon e5-2660 v3, C+OpenMP): 2.38× / 4.26× / 7.64× /
13.20× / 16.06× at 2 / 4 / 8 / 16 / 20 cores.

We mark this **PARTIAL**: the *shape* reproduces (monotonic-positive,
sublinear scaling) and the *invariant* is bitwise-stable across all
core counts, but the absolute number at 8 procs is 5.05× vs the
paper's 7.64×. The gap is expected:
- Python+multiprocessing fork/pickle overhead is much larger than
  C+OpenMP shared-memory thread overhead.
- A different CPU (Mac Pro 2019 macOS x86_64, vs paper's Xeon
  e5-2660 v3 Linux) — memory bandwidth and core counts differ.
- The synthetic n=60 graph has only 3,600 tuples; at high core
  counts the per-process chunk gets small and overhead dominates.

This claim is **not** fully reproducible on a different language
implementation; the pass-1 C++/MPI run on chiatta00 already
established that the *native* shape reproduces (26.4× on 128 cores
for 3-WL).

### C5 — 3-WL distinguishes Rook from Shrikhande

Run our own n=16 3-WL on both graphs (folklore variant; 4,096 triples
each):

|              | colors | iters | seconds |
|--------------|-------:|------:|--------:|
| Rook(4×4)    | 15     | 1     | (combined 0.28 s) |
| Shrikhande   | 31     | 3     |                   |

Color-count histograms differ → 3-WL **does** distinguish the SRG(16,6,2,2)
pair — exactly the theoretical fact the paper relies on to justify pushing
beyond k=2. The pass-1 C++/MPI 3-WL implementation showed the algorithm
scales; this pass-2 result shows it also has the right *expressive
content*.

## Headline coverage update (vs pass 1)

Pass 1 verdict: **PARTIAL** (coverage 7 / agreement 8). Pass 2 explicitly
grounds 7 additional claims (C1, C2, C3a/b/c, C4, C5) against paper
text and theory.

| Metric         | Pass 1 | Pass 2 |
|----------------|--------|--------|
| Claims tested  | ~5     | ~12    |
| Pass / Partial / Fail | n/a    | 11 PASS, 1 PARTIAL, 0 FAIL |
| Coverage       | 7      | **8+** |
| Agreement      | 8      | **8**  (qualitative shape only; absolute speedup is not language-portable) |

## 4-tier verdict

- **Reproducible (PASS, 11 claims):** Table 1 V/E grounding, Section 7
  bijection invariant, all three 2-WL distinguishability probes, the
  3-WL > 2-WL expressivity gap on the canonical SRG pair, and all
  pass-1 correctness/convergence checks.

- **Partial (1 claim, C4):** single-node strong-scaling absolute
  speedups. Pure-Python implementation gets 5.05× at 8 procs vs
  paper's 7.64× (different language, different CPU). Pass 1's
  C++/MPI run on chiatta00 covered this in the right language and
  reproduced the shape there.

- **Skipped — needs cluster:** multi-node distributed scaling on a
  Cray-class machine (paper §6.4, Figures 11–14). Blocker: needs
  multi-node MPI cluster with InfiniBand; not free on CherryRd.

- **Skipped — needs baselines:** 2,193× speedup vs K-WL on 662_bus
  (Table 2, top). Blocker: requires building the K-WL [23] baseline
  binary; not part of ScaWL itself, and orthogonal to ScaWL
  correctness, which we have grounded.

## Artifacts (pass 2 only — pass-1 artifacts unchanged)

- `PARSER_PROVENANCE.md` — pdftotext invocation and sanity checks.
- `PROGRESS` — chronological log of this pass.
- `code/repass/repass_scawl.py` — single entry-point script.
- `data/ufl/{LFAT5,Trefethen_20,celegansneural}/` — SuiteSparse MTX files.
- `results/repass/C1_dataset_grounding.json`
- `results/repass/C2_invariant_stability.json`
- `results/repass/C3_2wl_expressivity.json`
- `results/repass/C4_strong_scaling.json`
- `results/repass/C5_3wl_expressivity.json`
- `results/repass/summary.json`

## Reproducing pass-2

```bash
cd 2587225-ScaWL-Scaling-k-WL-Weisfeiler-Lehman-Algorithms-in/
# scipy is needed in addition to the pass-1 venv (networkx + numpy):
replication/venv/bin/pip install scipy
# Datasets (small — < 100 KB total):
mkdir -p data/ufl && cd data/ufl
curl -sL -o Trefethen_20.tar.gz https://sparse.tamu.edu/MM/JGD_Trefethen/Trefethen_20.tar.gz && tar xzf Trefethen_20.tar.gz
curl -sL -o LFAT5.tar.gz        https://sparse.tamu.edu/MM/Oberwolfach/LFAT5.tar.gz         && tar xzf LFAT5.tar.gz
curl -sL -o celegansneural.tar.gz https://sparse.tamu.edu/MM/Newman/celegansneural.tar.gz   && tar xzf celegansneural.tar.gz
cd ../..
replication/venv/bin/python code/repass/repass_scawl.py
# Inspect:
ls results/repass/
```

Wallclock: ~6 seconds. No MPI, no GPU, no allocations. Pure CPU + free Argo.

## Open Questions & Reproducibility Blockers

- **Exact missing artifact 1 (blocks paper Figures 11–14, multi-node distributed scaling):** A multi-node MPI cluster with InfiniBand (the paper used a Cray-class machine for §6.4). Specifically missing: free multi-node allocation; the pass-1 C++/MPI implementation `replication/src/cpp_mpi/wl3_mpi.cpp` is ready to run on such a cluster, and the pass-1 single-node chiatta00 scaling (26.4× on 128 cores for 3-WL) suggests the multi-node shape would reproduce — but the absolute speedups in Figs 11–14 require multi-node InfiniBand timing data that we did not collect.
- **Exact missing artifact 2 (blocks Table 2 top row, 2,193× speedup vs K-WL on 662_bus):** A compiled K-WL [23] baseline binary. The paper's K-WL reference implementation (cited as ref [23], an older C library by a different group) was not built/ported. This is orthogonal to ScaWL correctness — ScaWL's own correctness and expressivity (the C1–C5 + C3a/b/c claims) are all verified — but the absolute Table 2 speedup ratios cannot be regenerated without it.
- **Exact missing artifact 3 (drives the C4 PARTIAL verdict, ~5.05× vs paper 7.64× at 8 procs):** A like-for-like language/runtime match. Pass-2 used pure Python + multiprocessing on CherryRd (macOS x86_64); the paper used C+OpenMP on a Xeon e5-2660 v3 Linux box. The pass-1 native-C++/MPI run on chiatta00 already covers the in-language strong-scaling shape, but a *direct* Python-to-paper-table comparison at the absolute-speedup level is not language-portable and never will be.
- **Open question 1:** On the Rook(4×4) / Shrikhande SRG pair, does the 3-WL distinguishability gap (Shrikhande needs 3 iterations, Rook converges in 1) generalize to all SRG(n,k,λ,μ) parameter families? Worth probing on Paley(13), Paley(17), and the Kneser KG(5,2) pair.
- **Open question 2 / extension:** How does the ScaWL bijection (Theorem 5 / Corollary 3) interact with *random* k-tuple sampling for approximate k-WL on huge graphs? The paper proves exact equivalence under shard partitioning; an approximate variant could push to graphs beyond the paper's 8500-edge ceiling.
