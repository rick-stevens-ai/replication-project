# Artifacts Summary — chen2023 (arXiv:2312.10473)

## Produced
| Artifact | Path | Notes |
|---|---|---|
| Original PDF | paper.pdf | sha256 `b3223af38129e625d85e44d8a40d62e4f8e37374986e0da00414bb048886199e` |
| Marker text | extraction/marker.md | pdftotext (~8.2k words) |
| Nougat stub | extraction/nougat.mmd | GPU-only; sha256+DOI |
| Code | code/chen2023_replication.py | topological magnon: FHS Chern + kappa_xy(T) |
| Results JSON | work/results.json | C1/C2/C3 match flags |
| Figure 1 | figs/fig1_topological_magnon_THE.png | Chern vs m + kappa_xy vs m |
| LaTeX report | report/REPORT.tex (+PDF) | scope + critique + bugfix log |
| Open questions | report/open_questions.json | 5 heavy-duty |
| Workflow | report/workflow.md | |
| Failure analysis | report/failure_analysis.md | |
| LLM-judge | report/evidence/llm_judge.json | PARTIAL cov6 agr5 (sonnet-4.6 free) |

## Key numbers
Chern=-1 (topological), flips -1->0 at |m|~2.1; kappa_xy=+2.35 (topological) vs -0.13 (trivial) => sign reversal.

## Provenance
arXiv https://arxiv.org/abs/2312.10473 ; DOI 10.48550/arXiv.2312.10473 ; Lanzhou Univ (Chen, Luo, Zhao).
