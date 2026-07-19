# Workflow — chen2023 (arXiv:2312.10473)

## Narrative
1. Fetched PDF; pdftotext (~8.2k words); Nougat stub (GPU, sha256).
2. Extracted the physics: LSWT on Kitaev-Gamma honeycomb TmX (18 spins/cell); nonzero magnon Chern; field-driven successive topological transitions; thermal Hall sign change; edge modes.
3. Scoped to the universal mechanism (18-band TmX out of scope): minimal Haldane/DMI 2-band topological-magnon model.
4. C1: Chern via Fukui-Hatsugai-Suzuki plaquette -> C=-1 (nonzero).
5. C2: swept field-proxy mass m across DMI gap (~2.08); Chern flips -1->0 (topological transition).
6. C3: magnon thermal Hall kappa_xy = -sum c2(E/T) Omega; large (+2.35) in topological region, reverses to -0.13 trivial -> sign change tracking Chern.
7. Two bugfixes: (a) Haldane mass sign structure (valley-odd) so a topological gap opens (was C=0 everywhere); (b) replaced a divergent hand-rolled Li2 series with scipy.special.spence (kappa was 1e+225).
8. LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 6, agreement 5.

## Tools & codes
Python 3.13, NumPy, SciPy (spence dilogarithm), Matplotlib; pdftotext. code/chen2023_replication.py (~180 LOC). FHS Chern + magnon THE. LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~25s per run (96x96 plaquette Chern x 17 field points). Wall clock ~30 min incl. 2 bugfixes. ~180 LOC, 3 iterations.
