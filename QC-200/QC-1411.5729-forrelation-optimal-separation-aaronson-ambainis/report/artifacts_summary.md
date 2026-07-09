# Artifacts Summary — Forrelation replication (arXiv:1411.5729)

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1411.5729-forrelation-optimal-separation-aaronson-ambainis/`

## Required 8-artifact bar

| # | Artifact | Path | Status | Notes |
|---|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` | ✅ | 569 kB, 60 pp, arXiv v1 21 Nov 2014. Copy also in `work/`. |
| 2 | Marker parse | `extraction/marker.md` | ✅ *surrogate* | PyMuPDF (fitz) 1.27.2.3 with page markers. Marker not installed; header labels surrogacy. |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ *surrogate* | `pdftotext -layout` reflow. Nougat not installed; header labels surrogacy. |
| 4 | LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf`) | ✅ | Section-by-section, claim-by-claim, verdict. |
| 5 | Open questions | `report/open_questions.json` + § in REPORT | ✅ | 5 Q's, each `{q, basis, next_steps}`. |
| 6 | Workflow | `report/workflow.md` | ✅ | Env, tools+versions, steps, ~40 min wall clock. |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | This file. |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | 5 residual gaps flagged, no primary failures. |

## Evidence + code (`report/evidence/`)

| File | Purpose |
|---|---|
| `forrelation_sim.py` | Full simulator: dense H^n, quantum circuit, closed-form Φ, WHT-consistency check, Monte-Carlo classical estimator, doubling-search K_needed, scaling plot. ~330 lines pure numpy. |
| `sim.log` | Full stdout of the sim run (2026-07-05). |
| `forrelation_results.json` | Machine-readable results: per-instance Φ, Φ², P(|0ⁿ⟩), |diff|; per-n K needed; log-linear fit; verdict. |
| `classical_scaling.png` | log₂(K) vs n, with slope-1/2 (Ω(2^{n/2})) reference line. |

## Raw / intermediate (`work/`)

| File | Purpose |
|---|---|
| `paper.pdf` | Downloaded arXiv PDF (byte-identical to top-level `paper.pdf`). |
| `paper.txt` | `pdftotext -layout` dump used for skim + extraction. |

## Reproducibility
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1411.5729-forrelation-optimal-separation-aaronson-ambainis
python3 report/evidence/forrelation_sim.py
```
Deterministic (numpy Generator seeded 42 for quantum, 101 for classical),
runs in <1 s on a modern CPU.
