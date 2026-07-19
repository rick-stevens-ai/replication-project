# Artifacts Summary — zhang2025 (arXiv:2503.17916)

## Produced
| Artifact | Path | Notes |
|---|---|---|
| Original PDF | paper.pdf | sha256 `7ce000a861d787546fcde5e0951d3dc9b69a4cc14faf05999f6a4ef440c7cae0` |
| Marker text | extraction/marker.md | pdftotext (~9.8k words) |
| Nougat stub | extraction/nougat.mmd | GPU-only; sha256+DOI |
| Code | code/zhang2025_replication.py | Table I corr + Stoner dome + SOC-free TB |
| Results JSON | work/results.json | C1/C2/C3 + paper Table I embedded |
| Figure 1 | figs/fig1_strain_altermagnet.png | splitting-vs-moment, dome, SOC-free linearity |
| LaTeX report | report/REPORT.tex (+PDF) | scope statement + Table I + critique |
| Open questions | report/open_questions.json | 5 heavy-duty |
| Workflow | report/workflow.md | |
| Failure analysis | report/failure_analysis.md | |
| LLM-judge | report/evidence/llm_judge.json | PARTIAL cov7 agr6 (sonnet-4.6 free) |

## Key numbers
Spearman rho(moment,split)=0.643; rising-branch Pearson=0.807; dome onset~2.5%, peak~4.3% (Table I peaks: moment 5%, split 4%); SOC-free slope=8.0; theta_AS~7% reported (not recomputed).

## Provenance
arXiv https://arxiv.org/abs/2503.17916 ; DOI 10.48550/arXiv.2503.17916 ; PRB 112, 024415 (2025).
