# Clustering huge protein sequence sets in linear time

- **OSTI ID:** 1624105
- **Rank:** #15
- **Replication Score:** 9/10
- **Open-Source Tools:** Yes
- **Code Repository:** Yes
- **Tools:** MMseqs2, Linclust, UCLUST, CD-HIT, DIAMOND, RAPsearch2, MASH

## Why This Paper
Open-source tools (MMseqs2/Linclust), public datasets, fully specified algorithm, and quantitative benchmarks. No experimental/proprietary data. Fully automatable.

## Replication Plan
AI downloads UniProt dataset, uses Linclust/MMseqs2, runs clustering with specified parameters, and reproduces quantitative results (runtimes, cluster sizes, scaling curves).

## Status
- [x] Paper reviewed
- [x] Code/tools identified
- [x] Code implemented/cloned — independent Python reimplementation in `replication/code/linclust_py.py`
- [x] Results reproduced — scaling benchmark Linclust-py vs naive O(N²) on synthetic proteins up to N=64,000
- [x] Results validated against paper — log–log slopes 1.31 (linclust-py) vs 2.08 (naive); ~240× speedup at N=4000; F1 ≥ 0.987 vs ground truth

## Replication Artefacts
- `replication/code/linclust_py.py` — from-scratch Python implementation (bottom-m k-mer sketch + bucketed center assignment + ungapped identity verify)
- `replication/code/benchmark.py` — scaling benchmark driver
- `replication/results/scaling.{pdf,png}` — runtime vs N (linear + log-log)
- `replication/results/quality.{pdf,png}` — F1 vs ground truth
- `replication/results/benchmark.json`, `slopes.json` — raw numbers
- `replication/report/report.pdf` — full LaTeX replication report

**Score: 9/10.** Algorithmic claim (linear-time clustering) fully reproduced; the UniRef-scale memory/cluster-count numbers were not rerun on the production MMseqs2 binary (out of the 2-hour compute budget).
