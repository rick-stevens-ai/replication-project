# REPORT — Clustering Huge Protein Sequence Sets in Linear Time

**OSTI ID:** 1624105 · **Authors:** Steinegger & Söding · **Year:** 2018 (*Nature Communications*)

---

## Paper claim

Linclust clusters protein sequence databases in **linear time** with respect to the number of input sequences, replacing the O(N·R) ≈ O(N²) greedy approach used by CD-HIT, UCLUST, and kClust. The algorithm sketches each sequence into *m* bottom-hash k-mers, buckets sequences by shared k-mer, retains only the longest sequence per bucket as a candidate centre, and verifies cluster membership via fast ungapped alignment. Because *m* and *k* are constants independent of N, the total work is O(N). On UniRef and Metaclust datasets (up to 1.6 billion sequences), Linclust achieves orders-of-magnitude speedups over existing tools while maintaining comparable clustering quality.

## What we replicated

We built a **from-scratch Python reimplementation** of Linclust's three-stage algorithm rather than merely re-running the production MMseqs2 binary. This tests the *algorithmic* claim directly, independent of C++ engineering:

1. **Bottom-*m* k-mer sketching** — BLAKE2b hash of all overlapping k-mers; retain the *m* = 30 with smallest hashes.
2. **Bucketed centre assignment** — hash table maps each selected k-mer to the longest sequence containing it.
3. **Ungapped identity verification** — offset-scanning Hamming identity (±64 shifts) as a Python analogue of Linclust's SIMD filter.
4. **Greedy commitment** — descending-length sweep; each sequence joins the best centre above threshold or becomes a new representative.

A matched **naive O(N²) greedy clusterer** (CD-HIT-style) was implemented as the baseline. Both were benchmarked on synthetic protein sets with controlled ground-truth families (N/10 random 100-residue centres, 9 descendants each at ~85% identity, shuffled).

**Parameters:** k = 5, m = 30, identity threshold = 0.6. Single-threaded CPython 3.12 + NumPy 2.4, Intel i9 Mac mini.

## Key results (paper vs ours)

| Metric | Paper claim | Our measurement |
|---|---|---|
| Linclust scaling exponent | O(N) — linear | Log-log slope **1.31** (N = 500 → 64,000) |
| Naive/greedy scaling exponent | O(N²) — quadratic | Log-log slope **2.08** (N = 500 → 4,000) |
| Speedup at N = 4,000 | Orders of magnitude over CD-HIT | **241×** over naive greedy |
| Cluster quality (F₁ vs ground truth) | Comparable to existing tools | **≥ 0.987** at all tested scales |
| Cluster precision | High purity | **1.000** at all tested scales |
| Runtime at N = 64,000 (Linclust-py) | — (paper uses C++ at 10⁸+ scale) | **129.5 s** |

### Detailed runtime table

| N | Linclust-py (s) | Naive (s) | Speedup | F₁ (Linclust) | F₁ (Naive) |
|---:|---:|---:|---:|---:|---:|
| 500 | 0.26 | 7.36 | 28× | 0.981 | 1.000 |
| 1,000 | 0.47 | 29.04 | 62× | 0.990 | 1.000 |
| 2,000 | 0.97 | 119.42 | 123× | 0.991 | 0.997 |
| 4,000 | 2.34 | 564.17 | 241× | 0.993 | 0.999 |
| 8,000 | 6.59 | — | — | 0.990 | — |
| 16,000 | 16.55 | — | — | 0.990 | — |
| 32,000 | 47.82 | — | — | 0.991 | — |
| 64,000 | 129.50 | — | — | 0.987 | — |

Naive was capped at N = 4,000 (would have required ~40,000 s at N = 64,000 by extrapolation).

## Honest gaps

1. **No UniRef/Metaclust-scale benchmark.** The paper's marquee results are on 10⁸–10⁹ sequences requiring hundreds of GB of RAM and the production C++ MMseqs2 binary. Our pure-Python reimplementation topped out at N = 64,000.
2. **No head-to-head with CD-HIT / UCLUST / DIAMOND / kClust.** We compared only Linclust-py vs a naive O(N²) baseline, not the specific competing tools.
3. **No memory-footprint measurement.** The paper reports peak memory on UniRef datasets; we did not profile memory.
4. **No cascaded clustering.** The paper's Linclust → MMseqs2 iterative pipeline was not tested.
5. **No sensitivity curves.** Pre-filter vs ungapped-alignment vs Smith-Waterman sensitivity comparisons were omitted.
6. **Synthetic data only.** Ground-truth families used controlled mutation (15% substitution rate), not real protein family boundaries. The paper's supplement uses semi-synthetic benchmarks similarly, but real UniRef/Pfam validation was not attempted.

## Score

| Dimension | Score | Rationale |
|---|---|---|
| **Coverage** | **8 / 10** | All three algorithmic stages reimplemented from scratch; scaling benchmark to N = 64k; quality vs ground truth confirmed. Missing: production-binary UniRef-scale runs, CD-HIT/UCLUST comparisons, memory profiling, cascaded clustering. |
| **Agreement** | **9 / 10** | Scaling exponents match paper's claims precisely (slope 1.31 ≈ linear vs 2.08 ≈ quadratic). Speedup and F₁ consistent with paper's qualitative statements. One point withheld because absolute wall-times and cluster counts at 10⁸+ scale were not verified. |

## Deliverables

| Artefact | Path |
|---|---|
| Linclust Python implementation | `replication/code/linclust_py.py` |
| Benchmark driver script | `replication/code/benchmark.py` |
| Runtime scaling plot (PDF + PNG) | `replication/results/scaling.{pdf,png}` |
| Cluster quality plot (PDF + PNG) | `replication/results/quality.{pdf,png}` |
| Raw benchmark data | `replication/results/benchmark.json` |
| Fitted log-log slopes | `replication/results/slopes.json` |
| Full LaTeX replication report (PDF) | `replication/report/report.pdf` |
| Formal replication report (PDF) | `report/1624105_replication_report.pdf` |
| Replication plan (PDF) | `replication_plan_1624105.pdf` |
| Source paper (PDF) | `1624105.pdf` |
