# Artifacts Summary — smejkal2022 (arXiv:2204.10844)

## Produced
| Artifact | Path | Notes |
|---|---|---|
| Original PDF | paper.pdf | sha256 `714cea1bd4b7add4091e0952a1e1c7303411784dd665221940bc565546579c52` |
| Marker text | extraction/marker.md | pdftotext fallback (~16.6k words) |
| Nougat stub | extraction/nougat.mmd | GPU-only; sha256+DOI recorded for later corpus sweep |
| Replication code | code/smejkal2022_replication.py | ~200 LOC, CPU-only |
| Results JSON | work/results.json | per-claim match flags C1/C2/C3 |
| Figure 1 | figs/fig1_dwave_classification.png | d-wave spin-split map + spin-split Fermi surfaces |
| LaTeX report | report/REPORT.tex | section-by-section, claims table, critique |
| Open questions | report/open_questions.json | 5 heavy-duty, paper-grounded |
| Workflow | report/workflow.md | narrative + tools + effort |
| Failure analysis | report/failure_analysis.md | this set |
| LLM-judge verdict | report/evidence/llm_judge.json | REPLICATED, cov 9, agr 9 (sonnet-4.6, free) |

## Traces
- Run outputs captured to stdout (C1/C2/C3 diagnostic values); all match flags True.
- Key numbers: BZ-avg split=0, net moment=0, local max=2.40t, C4+flip residual=0, translation residual=2.40, diagonal node=0, sign-changes=4.

## Provenance
- arXiv: https://arxiv.org/abs/2204.10844 ; DOI 10.48550/arXiv.2204.10844
- Published as Rev. Mod. Phys. Perspective (2022).
