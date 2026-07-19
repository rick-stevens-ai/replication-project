# Workflow — zhao2025 replication

## Tools / codes
- Python 3 (numpy; matplotlib for graph figures). No DFT run (symmetry + paper-reported coefficients).
- Independent reimplementation: code/zhao2025_replication.py (487 lines).

## Steps
1. Read paper (extraction/marker.md) + method_extract.md; identified the graph-coupling classification method and 3 worked material examples + HfO2.
2. Built symmetry-adapted mode graph (nodes=irrep modes, edges=symmetry-allowed invariants).
3. Implemented the proper/improper/triggered classifier from graph structure + the eta = min/max mixing metric.
4. Applied to Fig.1 framework, LaGaO3/YGaO3, SrTiO3/CaTiO3, and HfO2 Pca2_1.
5. Emitted work/results.json (4 claims, all matched) + 3 graph figures.

## Work estimate
~1 subagent session (died late during cleanup) + parent recovery of the 5 report artifacts. Compute: trivial CPU (<10 s). Science verified by re-execution (exit 0, 4/4 PASS).
