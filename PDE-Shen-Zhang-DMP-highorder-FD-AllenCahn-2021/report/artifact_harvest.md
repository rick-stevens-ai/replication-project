# Artifact harvest

Public artifacts pulled or reused during this replication.

| Artifact | Source | Size | Notes |
|---|---|---|---|
| Paper PDF (arXiv:2104.11813v1) | Sibling cache `~/Dropbox/REPLICATE-PROJECT/PDE-allen-cahn-maxprinciple-shen-zhang-2021/work/paper_2104.11813.pdf`; originally from https://arxiv.org/pdf/2104.11813v1 | 3.6 MB | Copied to `paper.pdf` in target dir. Public arXiv preprint. Journal DOI 10.4310/cms.2022.v20.n5.a9 (paywalled published version, not fetched — preprint identical in content per paper's arXiv-mode footnote). |
| Sibling text extraction | Sibling `work/paper_2104.11813.txt` | 87 KB (2049 lines) | Reused only for cross-checking equation numbers; no other content transferred. |
| Sibling `report/REPORT.md` | Sibling target dir | 15 KB | Consulted to confirm claim table and plan a *complementary* angle. Not copied. |

## Reference URLs

- arXiv preprint page: https://arxiv.org/abs/2104.11813
- Journal DOI: https://doi.org/10.4310/cms.2022.v20.n5.a9  (paywalled; not accessed for this run)
- Related: Feng & Prohl, "Numerical analysis of the Allen–Cahn equation
  and approximation for mean curvature flows", Numer. Math. 94 (2003)
  33–65 — provides the classical stabilized IMEX / linear-stabilizer
  framework we use in our time stepping.

## Data / code we generated ourselves

| File | Type | Purpose |
|---|---|---|
| `work/allen_cahn_dmp.py` | Python, ~350 LoC | Core numerical solver + convergence tests |
| `work/make_figures.py` | Python | Plot generation |
| `work/emit_csvs.py` | Python | Human-friendly CSV export |
| `work/judge.py` | Python | LLM-judge call (Argo endpoints only) |
| `work/dmp_and_convergence_results.json` | JSON | Master results dict |
| `report/evidence/dmp_summary.csv` | CSV | 6-row DMP dynamics summary |
| `report/evidence/conv_{1d,2d}_o{2,4}.csv` | CSV × 4 | Convergence tables |
| `report/evidence/dmp_over_time.png` | PNG | Figure 1 |
| `report/evidence/convergence_loglog.png` | PNG | Figure 2 |
| `report/evidence/judge_prompt.txt` | txt | Prompt sent to judge |
| `report/evidence/judge_raw.txt` | txt | Raw JSON returned by judge |
| `report/evidence/judge_verdict.json` | JSON | Parsed verdict |
| `report/evidence/judge_used.txt` | txt | Which model+endpoint the judge used |

No external data was downloaded — this is a pure numerical replication.
