# Artifacts summary

Independent replication of arXiv:0707.2831 (Shor & Jordan, "Estimating
Jones Polynomials is a Complete Problem for One Clean Qubit"). All paths
relative to
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0707.2831-jones-polynomials-dqc1-shor-jordan/`.

## The 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Notes |
|---|---|---|---|---|
| 1 | paper.pdf | `paper.pdf` | ✅ 440 KB, 29 pages | Fetched from arxiv.org/pdf/0707.2831 |
| 2 | Marker parse | `extraction/marker.md` | ✅ (surrogate) | Marker not installed locally; PyMuPDF page-boundaried dump used, tool clearly labelled in file header (see `extraction/README.md`) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ (surrogate) | Nougat not installed locally; `pdftotext -layout` reflow used, tool clearly labelled in file header |
| 4 | REPORT.tex | `report/REPORT.tex` | ✅ 15.5 KB, 5-page compiled `REPORT.pdf` (273 KB) | Full section-by-section: paper summary, claims table (C1-C4), method, results table, verdict |
| 5 | open_questions.json + `## Open Questions` in report | `report/open_questions.json` + REPORT.tex §5 | ✅ 5 heavy-duty questions | Each `{q, basis, next_steps}`; also rendered as itemize in REPORT.tex |
| 6 | workflow.md | `report/workflow.md` | ✅ | Timeline, tool versions, effort estimate |
| 7 | artifacts_summary.md | `report/artifacts_summary.md` | ✅ | This file |
| 8 | failure_analysis.md | `report/failure_analysis.md` | ✅ | Honest gaps + friction log |

## Evidence bundle (`report/evidence/`)

| File | Purpose |
|---|---|
| `replicate_shor_jordan.py` | Main replication script: Fibonacci rep of B_n, Markov trace, SJ Eq. 11, DQC1 Hadamard test on density-matrix simulator |
| `dqc1_qiskit_shots.py`     | Real Qiskit-Aer shot-based DQC1 Hadamard test (right + left trefoil) |
| `run_output.txt`           | Console log of `replicate_shor_jordan.py` (all numeric results printed) |
| `dqc1_shots_output.txt`    | Console log of `dqc1_qiskit_shots.py` |
| `results.json`             | Machine-readable summary of the analytic + density-matrix runs |
| `dqc1_shots_results.json`  | Machine-readable summary of the shot-based run |

## Work-directory (`work/`)

| File | Purpose |
|---|---|
| `paper.pdf`  | Original arXiv download (also copied to `paper.pdf` at project root for artifact-1 compliance) |
| `paper.txt`  | `pdftotext -layout paper.pdf` |
| `venv/`      | Isolated python 3.14 venv with qiskit 2.5.0 + qiskit-aer 0.17.2 + numpy 2.5.1 + scipy 1.18.0 |

## Reproducibility recipe (one-liner)

```
mkdir -p work extraction report/evidence
curl -sL -o work/paper.pdf https://arxiv.org/pdf/0707.2831
python3 -m venv work/venv && source work/venv/bin/activate
pip install -q --upgrade pip qiskit qiskit-aer numpy scipy
python report/evidence/replicate_shor_jordan.py | tee report/evidence/run_output.txt
python report/evidence/dqc1_qiskit_shots.py    | tee report/evidence/dqc1_shots_output.txt
(cd report && pdflatex -interaction=nonstopmode REPORT.tex)
```

## Key headline numbers reproduced

| Quantity | Analytic (paper) | This replication | Match |
|---|---|---|---|
| A = e^{-i·3π/5} | −0.30902 − 0.95106 i | −0.30902 − 0.95106 i | ✅ exact |
| D = −A² − A⁻² | φ = 1.61803… | 1.61803… | ✅ exact |
| V_{trefoil}(t=A⁻⁴) via SJ Eq. 11 | −0.80902 − 1.31433 i | −0.80902 − 1.31433 i | ✅ 0.0 abs error |
| Tr(V)/4 from DQC1 (ideal) | +0.73176 − 0.53166 i | +0.73176 − 0.53166 i | ✅ 1.3e-15 |
| Tr(V)/4 from DQC1 (shots, N=24 000) | ± ~1/√N ~ 6.5e-3 | +0.7394 − 0.5153 i, |Δ|=1.8e-2 | ✅ within ~3 σ |
