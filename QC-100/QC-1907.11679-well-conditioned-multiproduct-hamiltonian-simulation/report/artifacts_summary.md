# Artifacts summary — QC-1907.11679

| File | Purpose | Provenance |
|---|---|---|
| `work/paper.pdf` | Source PDF (arXiv:1907.11679v2, 9pp, 564KB) | `curl -L https://arxiv.org/pdf/1907.11679` |
| `work/paper.txt` | Extracted text (main body + Appendix A) | `pdftotext -layout` (poppler 25.10.0) |
| `work/mpf.py` | Five coefficient constructions + cancellation verifier | independent implementation of Eqs. 5, 8–10, verbatim entry of Appendix A Table I as `fractions.Fraction` |
| `work/heisenberg.py` | Dense 1D Heisenberg N=4 PBC, odd/even bond split | first-principles Pauli tensor product build |
| `work/suzuki.py` | Second- and fourth-order Suzuki base formulas | first-principles Suzuki recursion, $p=1/(4-4^{1/3})$ |
| `work/benchmark.py` | Dynamical benchmark harness | `scipy.linalg.expm` reference; operator-2-norm error |
| `work/analyze.py` | Slope fit + figure gen | least-squares log-log fit in clean regime $10^{-11}<\text{err}<10^{-1}$ |
| `work/judge.py` | LLM judge call to Argo free proxy | `argo:gpt-5`, strict JSON schema, no regex heuristic |
| `evidence/01_cancellation_sanity.txt` | Vandermonde residual per family for m=2..6 | run output |
| `evidence/02_benchmark_N4_t1.json` | Error vs step-count table for every method | run output |
| `evidence/03_slopes.json` | Fitted slopes vs expected 2m | analysis output |
| `evidence/04_judge_raw.json` | Raw LLM-judge response | Argo free proxy |
| `evidence/05_judge_verdict.json` | Parsed verdict + confidence | Argo free proxy |
| `evidence/fig_convergence.png` | log-log error vs step-count for all methods | matplotlib |
| `evidence/fig_condition.png` | $\|a\|_1$ vs $2m$ for Chin, Chebyshev, rounded, Appx-A | matplotlib |
| `report/REPORT.md` | Markdown narrative | this replication |
| `report/REPORT.tex` | LaTeX narrative | this backfill |
| `report/open_questions.json` | 5 open research questions | this backfill |
| `report/open_questions_section.tex` | LaTeX open-questions section | this backfill |
| `report/workflow.md` | Reproduction workflow | this backfill |
| `report/artifacts_summary.md` | This file | this backfill |
| `report/failure_analysis.md` | Honest critique of gaps + risks | this backfill |
| `report/artifact_harvest.md` | SHA256 of source PDF | prior harvest |
| `extraction/nougat.mmd` | Extraction stub (nougat placeholder) | this backfill |

## Endpoints used
- Argo free proxy (`argo:gpt-5`) — LLM judge only. No paid endpoints. No hardware runs.

## Verdict artifact
`evidence/05_judge_verdict.json` → `REPLICATED` confidence 0.88.

## Not present (deliberately, out-of-scope)
- No quantum-circuit simulator output (LCU / oblivious amp amp) — C7.
- No symbolic BCH expansion — C8.
- No large-$N$ sparse/Krylov/MPS runs — C9.
- No hardware noise study — see failure_analysis §3.
- No qDRIFT/qSWIFT comparison — see open_questions #1.
