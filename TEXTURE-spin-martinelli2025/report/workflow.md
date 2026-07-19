# Workflow — martinelli2025 (arXiv:2512.17587)

## Narrative
1. Fetched PDF; pdftotext (~10.6k words); Nougat stub (GPU, sha256).
2. Read abstract + intro + Sec on multipole parametrization: identified the two central STRUCTURAL claims reproducible on CPU (quantitative multipole<->NRSS relation; superposition/multi-component necessity). Flagged SrCrO3/LaVO3 DFT as out of scope.
3. Built a minimal 2-channel multipole model Delta(k)=O(cos kx-cos ky)+T(cos2kx-cos2ky), BZ-compensated form factors.
4. C1: single-channel NRSS (BZ-RMS |Delta|) linear in O (slope=form-factor RMS, residual 1e-16).
5. C2 (the key test): generated 200 synthetic materials with correlated (O,T); regressed NRSS on O-only (R2=0.83) vs O+T (R2=0.99) -> superposition needed, dR2=+0.16. Matches paper's central conclusion.
6. C3: band-independent BZ-RMS measure; BZ-avg Delta ~ 1e-17 (compensated).
7. LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 6, agreement 5 (honest: model-based, DFT not run).

## Tools & codes
Python 3.13, NumPy, Matplotlib; pdftotext. code/martinelli2025_replication.py (~180 LOC). LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~1s. Wall clock ~12 min incl. extraction. ~180 LOC, 1 iteration.
