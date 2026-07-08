# Artifacts and Traces — Summary

## Public artifacts pulled
| URL | What | Size | Note |
|---|---|---|---|
| https://arxiv.org/pdf/quant-ph/9805082 | Paper PDF | 176,410 bytes, 12 pages, PDF 1.4 | Saved as `paper.pdf` |

No code repository was published with this 1998 paper (it predates arXiv source uploads for the first author on this preprint); reproduction is from first principles.

## Produced files in this replication directory
| Path | Size (bytes) | Purpose |
|---|---|---|
| `paper.pdf` | 176410 | Source paper |
| `extraction/marker.md` | 37934 | pdftotext-fallback Marker-equivalent |
| `extraction/nougat.mmd` | 37774 | pdftotext-fallback Nougat-equivalent |
| `work/paper.txt` | ~35k | Raw pdftotext output |
| `work/quantum_counting.py` | 9684 | Analytic QPE + sweep |
| `work/verify_qiskit.py` | ~4k | Gate-level Qiskit circuit + single-case verify |
| `work/verify_qiskit_multi.py` | ~1.7k | Multi-case gate-vs-analytic cross-check |
| `work/llm_judge.py` | ~6k | Argo LLM-judge harness |
| `work/venv/` | (venv) | Python venv with qiskit 2.5.0 / qiskit-aer 0.17.2 / numpy |
| `report/REPORT.tex` | 12140 | LaTeX detailed report |
| `report/REPORT.pdf` | 262130 | Compiled report |
| `report/REPORT.md` | (see) | Markdown mirror |
| `report/brief.md` | (see) | 1-paragraph summary |
| `report/attempt_log.md` | (see) | Chronological log |
| `report/artifact_harvest.md` | (see) | Public-artifact inventory (this file's URL row) |
| `report/open_questions.json` | 4165 | 5 heavy-duty open questions with next_steps |
| `report/workflow.md` | 3197 | Workflow + tools + effort |
| `report/artifacts_summary.md` | (self) | This file |
| `report/failure_analysis.md` | (see) | Failure analysis |
| `report/evidence/sweep_results.json` | ~30k | 90-config sweep results (structured) |
| `report/evidence/sweep_results.csv` | ~10k | Same, CSV form |
| `report/evidence/sweep_run.log` | (see) | Stdout from sweep run |
| `report/evidence/qiskit_verify.log` | (see) | Single-case gate-vs-analytic verify |
| `report/evidence/qiskit_verify_multi.log` | (see) | Multi-case gate-vs-analytic verify (7 cases, worst L∞ = 2.72e-15) |
| `report/evidence/llm_judge_raw.txt` | (see) | Raw judge response |
| `report/evidence/llm_judge.json` | (see) | Parsed judge JSON |

## Traces summary
- **90/90** sweep configurations satisfied the paper's Theorem-5 error bound.
- **90/90** configurations had exact success-probability ≥ 8/π².
- Gate-level Qiskit implementation cross-validated to `L∞ ≤ 2.72e-15` on 7 diverse cases.
- LLM-judge (Argo `argo:gpt-5.4`): **verdict = PARTIAL**, agreement = 1.00, coverage = 0.67.
