# Workflow — QC-200 replication of arXiv:quant-ph/0208135

## Timeline (2026-07-05, CherryRd)

| Step | Duration | Notes |
|------|----------|-------|
| 1. Fetch PDF (arXiv) | ~3 s | `curl` from arxiv.org/pdf/quant-ph/0208135 |
| 2. pdftotext + skim + claim extraction | ~4 min | Identified 5 claims (C1-C5) |
| 3. Write full-Hilbert-space script (`adiabatic_paths.py`) | ~12 min | H_B, H_P, H_E on 2^n; sanity checks |
| 4. Run sanity checks (n=3,4,5) | ~1 s | Permutation-symmetry and HP-ground-state checks pass |
| 5. Full run: n=4..8 sweep + 50 random-A samples at n=8 | ~125 s | JSON + log written |
| 6. Symmetric-subspace reduction (`symmetric_subspace.py`) | ~10 min to write | H_B, H_P, H_E in (n+1)-dim spin subspace |
| 7. Validate sym-subspace vs full 2^n at n=4,5,6 | ~5 s | Match to 10^-14 |
| 8. Scaling run (n=4..80, mixed full+leading-order H_E) | ~25 s | Scaling JSON |
| 9. Refined scaling (n=4..200, dense 2001-pt grid, refined 4001-pt local) | ~2 min | Refined JSON |
| 10. Plots (`make_plots.py`) | ~5 s | 4 figures (PNG) |
| 11. Marker/Nougat extraction | ~5 min | Neither tool installed; used pdftotext-derived Markdown/MMD with clear provenance notes |
| 12. Write REPORT.tex | ~15 min | Section-by-section |
| 13. pdflatex REPORT.tex (2 passes) | ~3 s | 8-page PDF, 490 kB |
| 14. Write open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md | ~10 min | This file + siblings |

**Total wall-clock: ~1 hour.**

## Tools + versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 (system) | Driver language |
| numpy | 2.4.3 | Dense linear algebra, `eigvalsh` |
| scipy | 1.18.0 | Sparse ops (imported but not needed at these sizes) |
| matplotlib | shipped w/ conda-forge default | Plots |
| poppler / pdftotext | Homebrew, latest | PDF -> text |
| pdflatex (TeX Live 2026) | `/usr/local/bin/pdflatex` | Report -> PDF |
| curl | macOS system | arXiv PDF fetch |

## What I did NOT use

- No qiskit / cirq / pennylane / stim (small-system exact diag was more direct
  than any circuit-simulator wrapper).
- No LLM inference (deterministic numerical replication doesn't need it).
- No Marker or Nougat (neither installed; pdftotext gave clean output because
  the 2002 arXiv source is a text-based, not scanned, PDF).
- No GPU/HPC (largest matrix is 1024x1024 for full 2^n at n=10; symmetric
  subspace goes to n=200 which is a 201x201 matrix -- trivially CPU-bound).

## Estimate of effort by human-equivalent

- Understanding the paper's math (equations 1-30, effective-potential ansatz,
  P2 construction): **~30 min** of focused reading.
- Writing the exact-diag script correctly (getting the 3-qubit-embedding
  operator, HP construction, HB coefficient right): **~1-2 h** for a competent
  numerical physicist; ~15 min here because the paper's formulation is
  unusually explicit and the answers are checkable at each step.
- Symmetric-subspace reduction: **~1 h**. Requires knowing spin-1/2 addition
  and the standard Wigner-Eckart mechanics.
- Report writing: **~1-2 h**.
- Total human-equivalent: ~5-8 hours of focused senior-postdoc-level work.

## Reproducibility

```
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0208135-adiabatic-different-paths-farhi

# Fetch paper
curl -sL https://arxiv.org/pdf/quant-ph/0208135 -o work/paper.pdf

# Run everything
cd report/evidence
python3 adiabatic_paths.py           # n=4..8 sweep + random-A @ n=8
python3 symmetric_subspace.py        # validate sym-subspace + scaling to n=80
python3 refined_scaling.py           # dense-grid refined scaling to n=200
python3 make_plots.py                # 4 PNG figures

# Build report
cd ..
pdflatex -interaction=nonstopmode REPORT.tex
pdflatex -interaction=nonstopmode REPORT.tex
```

RNG seed = 42 (fixed in `adiabatic_paths.py`). Everything is deterministic.
