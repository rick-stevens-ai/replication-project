# Artifacts summary — QC-1802.00171-accelerated-vqe

## Paper
- `paper/1802.00171.pdf` — source paper (arXiv v3, published PRL 122, 140504).
- `paper/1802.00171.txt` — pdftotext extract for programmatic search.

## Code (executable evidence)
- `code/vqe_h2.py` — VQE H₂/STO-3G driver (PennyLane + PySCF + UCCSD + Adam + statevector, seed 42, 10 bond lengths).
- `code/alpha_qpe_rfpe.py` — numpy α-QPE / RFPE simulator reproducing paper Fig. 5 (α ∈ {0, 0.25, 0.5, 0.75, 1}, 200 trials × 60 iters × 600 particles, seed 1802).

## Report
- `report/REPORT.md` — long-form Markdown narrative (verdict, method, results, evidence pointers).
- `report/REPORT.tex` — LaTeX version with genuine critique and open-questions section input.
- `report/open_questions.json` — 5 truly-open questions, machine-readable list.
- `report/open_questions_section.tex` — LaTeX section rendering of the 5 questions.
- `report/workflow.md` — end-to-end reproduction pipeline.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique of what is and is not verified.

## Numerical evidence
- `report/evidence/vqe_h2_summary.json` — full VQE run summary (per bond length: FCI, VQE, error, iterations, wall-time).
- `report/evidence/vqe_h2_pes.csv` — PES table.
- `report/evidence/alpha_qpe_summary.json` — RFPE run summary (per α: median trace, mean trace, log-slope, config).
- `report/evidence/alpha_qpe_median_r.csv` — median r_k vs iteration k table.
- `report/evidence/versions.txt` — frozen software stack.

## Figures
- `figures/vqe_h2_pes.png` — H₂ potential energy surface + error vs FCI panel.
- `figures/alpha_qpe_rfpe_fig5.png` — reproduction of paper Fig. 5 (median r_k vs k, one curve per α).

## Extraction stubs (documentation)
- `extraction/nougat.mmd` — extraction pipeline stub / provenance note.

## Reproduction command
```
python3.12 -m venv .venv && source .venv/bin/activate
pip install pennylane openfermion pyscf numpy scipy matplotlib
python code/vqe_h2.py
python code/alpha_qpe_rfpe.py
```

## Notes
- Total wall-time budget on 1 CPU: ~5 minutes.
- All artifacts produced from open tools; no proprietary data, no HPC, no LLM inference in the numerics path.
