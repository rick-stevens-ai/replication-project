# Artifacts summary — QC-1304.5773

## The 8 required artifacts (per Rick 2026-07-05 completion bar)

| # | Artifact | Path | Present |
| --- | --- | --- | --- |
| 1 | Original PDF | `paper.pdf` (22 pages, arXiv:1304.5773v2) | ✅ |
| 2 | Marker extraction (surrogate) | `extraction/marker.md` (PyMuPDF 1.27.2.3, 96 kB) | ✅ |
| 3 | Nougat extraction (surrogate) | `extraction/nougat.mmd` (`pdftotext -layout`, 158 kB) | ✅ |
| 4 | Detailed LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf` if pdflatex succeeded) | ✅ |
| 5 | 5 open questions | `report/open_questions.json` (5 objects, each `{q,basis,next_steps}`) + `## Open Questions` in REPORT.tex | ✅ |
| 6 | Workflow + tools + effort | `report/workflow.md` | ✅ |
| 7 | Artifacts inventory | this file, `report/artifacts_summary.md` | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Additional evidence

| Path | Description |
| --- | --- |
| `report/evidence/gi_adiabatic.py` | Real numpy adiabatic-evolution simulator on the S_N permutation basis (H_P edge-mismatch + Cayley-mixer H_D). Deterministic; single-file. |
| `report/evidence/plot_spectra.py` | Regenerate `spectra.png` and `gap.png` from `results.json`. |
| `report/evidence/results.json` | All numerical results: for each instance, spectrum on 51-point s-grid, min gap, min interior gap, final fidelity on iso subspace, final ⟨H_P⟩, top-5 support permutations, iso-permutation indices. |
| `report/evidence/spectra.png` | Lowest-4 eigenvalues along the adiabatic schedule for all three instances. |
| `report/evidence/gap.png` | E_1(s) − E_0(s) along the adiabatic schedule for all three instances. |
| `work/paper.txt` | pdftotext dump used for initial method extraction. |
| `work/venv/` | Python venv (numpy 2.5.1, scipy 1.18.0, networkx 3.6.1, matplotlib). |
| `extraction/README.md` | Provenance note on the surrogate marker/nougat extractions. |

## Trace / provenance notes

- Task brief listed second author as "Lane Clemente"; PDF verifies "Lane Clark".
  Recorded in `report/REPORT.tex §1`.
- Only free endpoints used (no external API calls at all — the numerical
  verdict is decidable from the simulator output).
- No random seed sensitivity: the entire simulation is deterministic given
  `--T` and `--steps`.
- Marker/Nougat not installed on host; surrogates clearly labelled as such
  (this is the same convention as sibling QC-200 dirs; see e.g.
  `QC-0704.3628-*/extraction/README.md`).
