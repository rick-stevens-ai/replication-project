# Artifacts Summary — ding2021 (arXiv:2105.04495)

## Produced
| Artifact | Path | Notes |
|---|---|---|
| Original PDF | paper.pdf | sha256 `feeb78f8cef2ddaf9a8a623d28b0fcc94e8c0a80868d25da351d3f8205fe4aca` |
| Marker text | extraction/marker.md | pdftotext (~4.8k words) |
| Nougat stub | extraction/nougat.mmd | GPU-only; sha256+DOI |
| Code | code/ding2021_replication.py | SMR/OREMR angular model + thickness |
| Results JSON | work/results.json | C1/C2/C3 match flags |
| Figure 1 | figs/fig1_oremr_angular.png | three-plane angular MR + thickness plateau |
| LaTeX report | report/REPORT.tex (+PDF) | scope + critique |
| Open questions | report/open_questions.json | 5 heavy-duty |
| Workflow | report/workflow.md | |
| Failure analysis | report/failure_analysis.md | |
| LLM-judge | report/evidence/llm_judge.json | PARTIAL cov7 agr6 (sonnet-4.6 free) |

## Key numbers
AMR beta p2p=0 (flat) vs OREMR beta p2p=0.015 (cos^2); alpha/beta/gamma cos^2 fits R2=1.0; MR-ratio plateau flatness=0 for t<=5nm.

## Provenance
arXiv https://arxiv.org/abs/2105.04495 ; DOI 10.48550/arXiv.2105.04495 ; PRL 128 (2022). Peking Univ / Mainz / Julich (Go, Mokrousov, Klaui, Yang).
