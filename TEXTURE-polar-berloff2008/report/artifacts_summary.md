# Artifacts summary — Berloff 2008 (arXiv:0801.2964)

**Paper:** N. G. Berloff, *Vortex Splitting in Subcritical Nonlinear Schrödinger
Equations*, arXiv:0801.2964 (2008).
**Verdict:** PARTIAL — coverage 7/10, agreement 8/10.

## The 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-berloff2008.pdf` | present (460 KB, arXiv v1) |
| 2 | Marker extraction | `extraction/marker.md` | **interim** (`pdftotext -layout`; marker binary absent) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | **interim** (`pdftotext`; nougat binary absent) |
| 4 | Detailed report | `report/REPORT.tex` | complete (LaTeX, section-by-section + verdict) |
| 5 | Open questions | `report/open_questions.json` | complete (5 heavy Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | complete (tools/versions/effort) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
|   | Evidence | `report/evidence/` | result JSON + all code |
|   | Work / code | `work/` | code + intermediates |

## Evidence traces (`report/evidence/`)
- `berloff2008_result.json` — machine-readable per-claim result: Part A
  (stationary profile vs Table 1) + Part B (2D dynamics) + verdict block with
  coverage/agreement/gaps.
- `vortex_profile.py` — Part A solver (Eq 21, Newton relaxation).
- `vortex_split_2d.py` — Part B solver (Eq 16, split-step Fourier + winding tracker).
- `save_result.py` — driver that runs both and emits the result JSON.

## Headline numbers (this work vs paper)
| Quantity | This work | Paper | Rel. err |
|----------|-----------|-------|----------|
| a1(ξ→0) | 0.962 | 0.9575 | 0.5% |
| a1(ξ=5/8) | 0.2863 | 0.286 (exact) | 0.1% |
| ξ_crit | 0.690 | 0.689 | 0.1% |
| total charge (2D, s=2 seed) | 2 (conserved) | 2 (only s=±1 stable) | ✓ topological |
| core breathing r_core | 3.09→6.74→3.05 | Figs 6/7 breathing | qualitative ✓ |

## Reproduce
```bash
PY=/home/stevens/comfyui-env/bin/python
cd work
$PY vortex_profile.py       # Part A: statics vs Table 1
$PY vortex_split_2d.py 128 200 0.10 1   # Part B: 2D dynamics (grid T eps drive)
$PY save_result.py          # writes berloff2008_result.json + verdict
```

## Notes
- Extractions 2 & 3 are `pdftotext` interims because `marker`/`nougat` are not
  installed on this host. Content is faithful reading-order/layout text; only the
  math-token fidelity of nougat and the block structure of marker are missing.
  Regenerate on a GPU host with the models when available.
- `work/` and `paper.pdf` are gitignored per the REPLICATE-PROJECT `.gitignore`;
  the tracked deliverables are `extraction/`, `report/`, and `report/evidence/`.
