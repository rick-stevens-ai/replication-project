# Workflow — chatterjee2023 (arXiv:2308.12703)

## Narrative
1. PDF already present; text extracted via pdftotext (`extraction/marker.md`, ~1620 lines); Nougat stub recorded (GPU-only, sha256 logged).
2. Identified the reproducible core: the **exact real-space 8×8 BdG lattice model, Eq.(1)** (QSHI/BHZ + noncollinear spin-spiral texture + s-wave SC), and its three numerical headline claims (4 MCMs, quantized quadrupole Qxy=1/2, topological→trivial transition in the spiral pitch g).
3. Built the Γ-matrix algebra (τ⊗σ⊗s Pauli kron products) and assembled H(Eq.1) both densely (for the many-body quadrupole) and sparsely (for cheap near-zero-mode counting via shift-invert).
4. Coded three tests mapping to claims C1–C3: (C1) sparse `eigsh(sigma=0)` → 4 zero modes + corner-localization fraction; (C2) many-body quadrupole (Kang–Fang–Fu / Wheeler formula, Eq.2) over occupied BdG states; (C3) g-sweep of zero-mode count + bulk gap.
5. **Performance fix:** Apple-Accelerate dense `eigh` scales badly (2048-dim ≈ 29 s), so the original all-dense plan (24×24 ⇒ 4608-dim × 9 runs) hung. Refactored to sparse shift-invert for all MCM counting/sweep at L=24, reserving one dense `eigh` per point for Qxy at the smaller L=14. Total runtime then ~1 min.
6. Generated Fig.1 (LDOS of 4 corner modes; |E| spectrum; g-transition), results.json with per-claim match flags (all True), run_log.txt trace.
7. LLM-judge (free Argo `claude-sonnet-4.6` via localhost:4000) scored **REPLICATED, coverage 7, agreement 9**. (opus-4.8 returned 502 through the aggregator on 2026-07-19; sonnet-4.6 substituted, both free Argo.)

## Tools & codes
- Python 3.14, NumPy, SciPy (`scipy.sparse.linalg.eigsh` shift-invert; `numpy.linalg.eigh`), Matplotlib. `pdftotext` (poppler) for extraction.
- `code/chatterjee2023_replication.py` (~270 LOC); `code/make_fig.py` (~60 LOC).
- LLM-judge: `/tmp/judge_chatterjee.py` → `argo:claude-sonnet-4.6` (free).

## Effort estimate
- Compute: CPU-only. Sparse sweep (8 g-points, L=24, k=12 modes each) + 2 dense Qxy solves (L=14, 1568-dim) ≈ 60 s wall.
- Wall clock: ~25 min including the dense→sparse performance refactor and figure.
- ~330 LOC total; ~2 code iterations (JSON-bool fix + dense→sparse refactor).
