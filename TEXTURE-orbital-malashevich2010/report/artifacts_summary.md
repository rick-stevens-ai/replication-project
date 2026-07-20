# Artifacts Summary — Malashevich 2010

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction (marker) | `extraction/marker.md` | Curated header: claim, OMP decomposition, model, key eqs |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | pdftotext body dump (interim machine extraction) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report |
| 4 | Open questions | `report/open_questions.json` | 5 questions + next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end procedure |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Why agreement is PARTIAL |
| 8 | Evidence | `report/evidence/` | result JSON + sweep JSON + `malashevich2010_omp.py` + `malashevich2010_sweep.py` |

## Key numbers
- Model: 8-band spinless cubic TB (2×2×2), 2 valence bands, **insulating gap = 1.64**.
- Bounded-sample α_zz range over φ: **[−1.6e−3, +5e−5]**.
- k-space α_iso^CS range over φ: **[−3e−6, +1.2e−5]**.
- Cross-method correlation over φ: **≈ −0.07** (signal at noise floor).
- **Verdict: PARTIAL — Coverage 6/10, Agreement 3/10.**
- Runtime: main ~2s, sweep ~10s (well under 6 min budget).

## Credit
Berry/orbital machinery adapted from the **gobel2024** Kubo/L_z kernel
(`/home/stevens/shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py`).
