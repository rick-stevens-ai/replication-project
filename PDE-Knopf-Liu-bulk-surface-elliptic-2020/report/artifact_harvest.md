# Artifact harvest

| Artifact | URL / source | Local path | Size | Notes |
|---|---|---|---|---|
| Preprint PDF | https://arxiv.org/pdf/2008.00895 (v2, 6 Nov 2021) | `work/paper.pdf` | 326 946 B | Full 30-page arXiv v2, identical technical content to published version (per arXiv note). |
| Extracted text | derived (`pdftotext -layout`) | `work/paper.txt` | 1629 lines | Used to locate all Theorem/Corollary/Proposition anchors and abstract. |
| Published record | https://ems.press/journals/ifb/articles/3324284 | (metadata only, journal PDF paywalled) | — | Publisher confirms the arXiv version is the accepted preprint. |
| Code (paper's own) | none | — | — | Paper contains no numerical experiments and ships no code, by design (pure analysis). |
| Independent 2nd-order FEM verification code | this project | `work/eigen_1d_analog.py` | 12 KB | Standalone Python (numpy/scipy). |
| Independent 4th-order Hermite FEM code | this project | `work/eigen_fourth_order_1d.py` | 11 KB | Standalone Python (numpy/scipy). |
| LLM-judge script | this project | `work/llm_judge.py`, `work/llm_judge_claude.py` | 6 KB each | Argo endpoints only (gpt-5.2, claude-sonnet-4.6). |
| Numerical evidence | derived | `report/evidence/eigen_1d_results.json`, `report/evidence/eigen_fourth_order_1d_results.json` | — | Structured results. |
| LLM judge raw + parsed | derived | `report/evidence/llm_judge_*.json`, `.txt` | — | Two independent free-endpoint judges, both PARTIAL. |
| Numerical run logs | derived | `report/evidence/eigen_1d_run.log`, `report/evidence/eigen_fourth_order_run.log`, `report/evidence/llm_judge_run.log` | — | |

## Endpoints used

- **Argo proxy** `http://127.0.0.1:44497/v1` (localhost tunnel, key = `stevens`) — free.
- Models: `argo:gpt-5.2` (judge 1), `argo:claude-sonnet-4.6` (judge 2, cross-check).
- No paid endpoints (no Anthropic-direct, no OpenAI-direct, no OpenRouter).

## Reproducibility

Everything runs from a stock venv:
```
python3 -m venv venv && . venv/bin/activate
pip install numpy scipy
python3 eigen_1d_analog.py
python3 eigen_fourth_order_1d.py
ARGO_API_KEY=stevens python3 llm_judge.py
ARGO_API_KEY=stevens python3 llm_judge_claude.py
```

Total wall time on CherryRd: ~10 s for both FEM runs, ~30–60 s per LLM-judge call.
