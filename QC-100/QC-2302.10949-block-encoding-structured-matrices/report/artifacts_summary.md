# Artifacts summary — QC-2302.10949 block-encoding-structured-matrices

## Report
- `report/REPORT.md` — original narrative report
- `report/REPORT.tex` — LaTeX report with honest critique + open-questions include
- `report/open_questions.json` — 5 open questions, structured JSON
- `report/open_questions_section.tex` — LaTeX version of the open questions
- `report/workflow.md` — step-by-step replication workflow
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — honest critique / limits of what was exercised

## Evidence (numerical outputs preserved)
- `report/evidence/U_N4.npy`, `U_N8.npy`, `U_N16.npy` — full block-encoding
  unitaries (complex128 numpy arrays) for N ∈ {4, 8, 16}
- `report/evidence/block_encoding_results.json` — per-N qubit counts,
  unitarity residual, block-encoding max error, Qiskit re-verify error,
  and A / A_hat matrices
- `report/evidence/run_log.txt` — full stdout of the replication run

## Implementation
- `src/block_encode_tridiagonal.py` — full independent reimplementation:
  labelling, oracles-as-permutations, multiplexed R_y data loading,
  assembly of U, unitarity + block-encoding verification, and the
  N-scan comparing base-scheme flag-qubit count to Gilyén et al.

## Source paper
- `work/paper.pdf`, `work/paper.txt` — arXiv:2302.10949 v2 (Jan 8, 2024)

## Extraction (paper text / MMD)
- `extraction/nougat.mmd` — placeholder stub (pdftotext-derived; nougat
  not run for this replication because the paper's numerical claims
  were sourced from directly-readable text passages, not equations
  rendered as images)

## Sizes
Run `du -sh` on the directory to confirm; artifacts are small (<10 MB
total), all evidence is CPU-simulable and reproducible in ≈5 s.
