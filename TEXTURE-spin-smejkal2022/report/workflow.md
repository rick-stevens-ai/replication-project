# Workflow — smejkal2022 (arXiv:2204.10844)

## Narrative
1. Fetched PDF from arXiv; extracted text via pdftotext (`extraction/marker.md`, ~16.6k words); Nougat stub recorded (GPU-only, sha256 logged).
2. Identified the reproducible core of a Perspective/review: the symmetry-classification + representative d-wave altermagnet model (Secs II.B, II.C, III.A) that anchors the paper's central FM–AFM dichotomy thesis.
3. Reused the Wave-3 sasioglu2026 d-wave altermagnet tight-binding template (single-orbital square lattice, spin-dependent anisotropic hopping).
4. Coded three numerical tests mapping to claims C1–C3: (C1) BZ-averaged splitting + half-filling net moment vs local splitting; (C2) C4+spin-flip symmetry residual vs translation residual (the identification rule); (C3) diagonal nodal amplitude + sign-change count around Γ (d-wave lobe count).
5. Ran on a 401×401 k-grid; fixed a sign-change counting bug (zeros at nodes double-counted transitions) by dropping exact zeros and adding periodic wrap.
6. Generated Fig 1 (spin-split map + Fermi surfaces), results.json with per-claim match flags.
7. LLM-judge (free Argo `claude-sonnet-4.6` via localhost:4000) scored REPLICATED, coverage 9, agreement 9.

## Tools & codes
- Python 3.13, NumPy, Matplotlib. `pdftotext` (poppler) for extraction.
- `code/smejkal2022_replication.py` (~200 LOC).
- LLM-judge: `scripts/wave4_llm_judge.py` → `argo:claude-sonnet-4.6` (free). opus-4.x was returning an upstream parse error through the aggregator on 2026-07-19; sonnet-4.6 substituted (both free Argo).

## Effort estimate
- Compute: CPU-only, ~1 s runtime, single process, one k-grid sweep.
- Wall clock: ~10 min including extraction + debugging the node-counting.
- ~200 LOC; ~1 code iteration (one bugfix).
