# Artifact Harvest

Public artifacts fetched for this replication.

## Primary paper (OA PDF, arXiv)

| item | source | URL | size | notes |
|---|---|---|---|---|
| Preprint PDF | arXiv 2002.07489 v3 (20 May 2021) | https://arxiv.org/pdf/2002.07489 | 1,006,890 bytes, 22 pages | Located via Semantic Scholar `openAccessPdf` field for DOI 10.1137/19M1310098; status `GREEN`. HTTP 200. |
| Text extraction | `pdftotext -layout` (poppler) | (local) | 1343 lines | Used to extract equations and numerical parameters. |
| SIAM DOI page | https://doi.org/10.1137/19M1310098 | (blocked) | HTTP 406 | Publisher landing page blocks web-fetch; OA route used instead. |
| Semantic Scholar metadata | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/19M1310098 | (JSON) | – | Confirmed DOI, ArXiv ID 2002.07489, corpus ID 211146105, MAG 3006579199. Used S2 API key from macOS Keychain (`semantic-scholar-api-key` / `rick-stevens-ai`). |

## Code / data
No code repository is released with the paper (searched preprint header,
acknowledgements, and paper body; no GitHub / Zenodo / supplementary URL).
All numerical results in this replication are generated locally from the
paper's stated equations (2.26–2.30, 3.3–3.5, 3.9–3.16, 3.22–3.31).

## Downstream artifacts produced here
| file | purpose |
|---|---|
| `work/paper.pdf` | The arXiv PDF (as fetched) |
| `work/paper.txt` | Layout-preserving text extraction |
| `work/src/mfmt_1d.py` | 1D MFMT weighted-density and free-energy density implementation with vectorized second-order integration |
| `work/src/experiment_convergence.py` | Fig 4.1 style convergence test against Carnahan-Starling analytic |
| `work/src/pb_solver.py` | Modified PB Picard solver (initial version — kept for reference) |
| `work/src/pb_newton.py` | Newton solver for MF and SC modified PB, with mu_hs bulk-offset renormalization |
| `work/src/plots.py` | Matplotlib figures |
| `work/src/llm_judge.py` | Argo Sonnet 4.6 judge over the three testable claims |
| `report/evidence/fig41_convergence.{json,png}` | Convergence table + plot |
| `report/evidence/fig45_newton_mf_sc.json` | Full MF and SC density/potential/mu_hs profiles |
| `report/evidence/fig45_mf_vs_sc_replication.png` | MF-vs-SC comparison figure |
| `report/evidence/llm_judge.json` | Structured judge verdict |
| `report/evidence/llm_judge_reply.txt` | Raw judge reply |
| `report/evidence/llm_judge_model.txt` | The Argo model actually used (`argo:claude-sonnet-4.6` — Opus 4.7 was 502 during this run) |
