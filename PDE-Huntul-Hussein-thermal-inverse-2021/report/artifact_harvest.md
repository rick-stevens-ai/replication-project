# Artifact harvest

| Artifact | URL | Size | SHA-256 |
|---|---|---|---|
| paper.pdf (Huntul & Hussein 2021, 11 pages) | https://ijs.uobaghdad.edu.iq/index.php/eijs/article/download/3085/1510 | 1 683 118 B | a2fac725ea2c2591ba1ccecdecdc385c25fd92ae437d13a4c2cb7049786bc41d |
| paper_landing.html (DOI landing page) | https://doi.org/10.24996/IJS.2021.62.6.22 → https://ijs.uobaghdad.edu.iq/index.php/eijs/article/view/3085 | 50 094 B | (not hashed; navigation only) |

## Code / data written into this replication
All code and evidence are inside `work/` and `report/evidence/` respectively:
- `work/solver.py` — Crank–Nicolson forward solver, Thomas TDMA, inverse via `scipy.optimize.least_squares`.
- `work/example1.py` — Example 1 (smooth exact a(t)=1+t, f(t)=t) driver + Table-1/Table-2 reproduction.
- `work/example2.py` — Example 2 (piecewise-constant a(t), f(t)) driver + Table-2 reproduction.
- `work/make_figures.py` — matplotlib figures.
- `report/evidence/example1_table1_forward.json` — forward-solver RMSE across mesh sizes.
- `report/evidence/example1_table2_inverse.json` — reproduced Table 2 rows for Example 1.
- `report/evidence/example2_table2_inverse.json` — reproduced Table 2 rows for Example 2.
- `report/evidence/example*_trace_*.json` — full recovered (a(t), f(t)) traces.
- `report/evidence/fig_ex*.png` — 4 figures (a(t) and f(t) recovered vs exact).
- `report/evidence/judge_verdict.txt` — LLM-judge output (Argo Claude Opus 4.7).

## Endpoints used
| Purpose | Endpoint | Cost |
|---|---|---|
| PDF equation OCR (pages 2–5, 8) | `argo:gpt-4o` @ localhost:44497 (Argo proxy) | free |
| Replication verdict | `argo:claude-opus-4.7` @ localhost:44497 | free |
| Numerical solves | scipy 1.18.0 on local CPU (CherryRd) | free |

No paid endpoints (Anthropic / OpenAI / OpenRouter) touched.
