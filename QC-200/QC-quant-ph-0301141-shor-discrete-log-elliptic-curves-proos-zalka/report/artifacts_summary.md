# Artifacts summary — QC-200 replication of quant-ph/0301141

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301141-shor-discrete-log-elliptic-curves-proos-zalka/`

## Mandatory 8-artifact bar (per QC_WAVE_BRIEF_2026-07-03.md)

| # | Path | Present? | Notes |
|---|------|----------|-------|
| 1 | `paper.pdf` | ✅ | arXiv PDF v2 22 Jan 2004, 330 595 bytes |
| 2 | `extraction/marker.md` | ✅ | **fallback** = poppler pdftotext (Marker not installed); provenance note at top of file |
| 3 | `extraction/nougat.mmd` | ✅ | **fallback** = poppler pdftotext (Nougat not installed); provenance note at top of file |
| 4 | `report/REPORT.tex` (+ `REPORT.pdf`) | ✅ | 6-page compiled PDF, section-by-section per-claim results, verdict = REPLICATED |
| 5 | `report/open_questions.json` (+ inline `## Open Questions` section as `open_questions_body.tex`) | ✅ | 5 questions with q / basis / next_steps |
| 6 | `report/workflow.md` | ✅ | tools, versions, exact commands, work estimate |
| 7 | `report/artifacts_summary.md` | ✅ | this file |
| 8 | `report/failure_analysis.md` | ✅ | honest gap list |

## Evidence files (under `report/evidence/`)

| Path | Content |
|------|---------|
| `resource_formulas.py` | Reproduces f, f', Table 4 for all 5 published rows + standard ECC levels |
| `resource_table.json` | Machine-readable Table 4 reproduction |
| `shor_dlp_ec.py` | Real Qiskit statevector implementation of Shor's DLP on an EC subgroup |
| `shor_dlp_result.json` | Probability grid, hidden/recovered s for every s ∈ {1..7} |
| `shor_dlp_circuit.txt` | ASCII circuit of the QFTs on the x- and y-registers |
| `point_addition_demo.py` | Group-shift unitary + controlled version, verified on all basis states |
| `point_addition_result.json` | Verification records |
| `point_addition_shift_by_3.txt` | ASCII circuit of the +3 mod 8 shift |

## Work / intermediate files (under `work/`)

| Path | Content |
|------|---------|
| `paper.txt` | pdftotext dump used for headline extraction |

## Environment (under `venv/`)

Python 3.14 virtualenv with qiskit 2.5.0, qiskit-aer 0.17.2, numpy, sympy.
Reproducible: `python -m venv venv && source venv/bin/activate && pip install qiskit qiskit-aer numpy sympy`.

## Traces

- Every headline number in `REPORT.tex` is grep-verifiable in the corresponding `*.json` under `evidence/`.
- All Python entry points are self-contained and print their results to stdout.
- The QFT convention chosen (Qiskit's +i, giving `y' ≡ s·x'`) is documented in the docstring of `recover_s_from_measurements`.
