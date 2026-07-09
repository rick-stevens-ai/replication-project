# Artifact Harvest — OSTI 3365789

| Artifact | Source | Size | Checksum | Notes |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3365789 (via ssh uicgpu proxy) | 6,847,904 B | md5 `40866275c55dbe2068245fecfba25102` | OA accepted manuscript, J. Sci. Comput. 2026 |
| Paper text | `pdftotext` of the above | 60,289 B | — | `work/paper_3365789.txt` |

## Public code
- The paper cites its network architecture from ref [11] but does **not** release a public code repository for this specific Parareal integration (compute done on OLCF Frontier / PyTorch, no GitHub/Zenodo link in text). Replication was therefore done **from the equations** (Eqs. 6–14), which are fully specified — no proprietary data or code required.

## Data
- **No external dataset needed.** All inputs are analytic: the merging-bubbles initial condition (paper Eq. 16), a random initial condition (grain-coarsening style, seed=0), and a smooth manufactured solution for the order test. Fully self-contained.

## Compute
- uicgpu (8×A100 host; used CPU/numpy only — problem is small, FFT-exact solves). numpy 1.23.5, Python 3.
- LLM-judge: Argo proxy `http://127.0.0.1:44497/v1` model `argo:gpt-5.2` (free), temperature 0.

## Generated evidence (in `report/evidence/`)
- `V1_convergence.json` — failed first-attempt kink test (kept for transparency).
- `V1b_manufactured.json` — manufactured-solution spatial/temporal order (spatial 2nd-order confirmed).
- `V2V3_fine.json` — MBP + energy dissipation on merging bubbles.
- `C4C5_parareal.json` — Parareal invariant + convergence, merging bubbles.
- `C5b_random_parareal.json` — numerical-coarse Parareal on random IC.
- `llm_judge_request.json`, `llm_judge_verdict.md` — LLM-judge I/O.
