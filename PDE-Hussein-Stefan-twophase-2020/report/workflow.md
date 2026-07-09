# Workflow — Replication of Adil & Hussein (2020) Two-Sided Stefan Problem

Paper: Z. Adil & M.S. Hussein, *Numerical Solution for Two-Sided Stefan Problem*,
Iraqi J. Science **61**(2):444-452, Feb 2020, DOI
[10.24996/ijs.2020.61.2.24](https://doi.org/10.24996/ijs.2020.61.2.24) (Open Access).

Replicator: Ollie (subagent). Host: CherryRd (macOS). Wave: PDE-100 (2026-07-01 night push);
candidate rank 63 in `PDE_TOPUP25_2026-06-26.tsv`.

**Free-endpoint-only compute** — this is a light 1D problem; no GPU needed. All
LLM traffic through Argo (`localhost:44497`).

---

## Stage 0 — Source acquisition (paid PDF tool avoided)

- OA PDF fetched from the publisher OJS galley with `curl`; MD5 checksum
  `9905e28d…` stored in the run log to prevent silent swap.
- Saved as `work/paper.pdf`.
- Text dump: `pdftotext -layout work/paper.pdf work/paper.txt`.
- Equation figures / half-typeset math recovered via
  `pdftoppm -r 300 work/paper.pdf work/page` followed by local `tesseract`
  OCR on each PNG. **No vision-LLM OCR** was used — no free image endpoint was
  available at run time.

## Stage 1 — Model decoding

- From `work/paper.txt` + `tesseract` OCR of the equation pages, extracted the
  original variable-domain PDE (eq. 1), Landau change of variables, and the
  transformed fixed-domain PDE (eq. 4).
- For each of Example 1 and Example 2, wrote down the coefficients
  `a(x,t), b(x,t), c(t), f(x,t)`, the moving boundaries `h1(t), h2(t)`, and
  the claimed exact solution `u_exact(x,t)`.
- **Cross-check:** derived `f = u_t - a u_xx - b u_x - c u` analytically from
  `u_exact` and compared to the paper's printed `f`.
  - Example 1: `max |f_derived - f_printed| = 0.0` → model correctly decoded.
  - Example 2: printed `u(x,t) = x^2 + 2t^2 + 1` is INCONSISTENT with the
    printed `f` (which contains `x^3` and `3x^2` terms) and with the paper's
    own printed transformed exact `v(y,t) = 1 + 2t^2 + (...)^3`. Corrected
    to `u = x^3 + 2t^2 + 1`; consistency restored. (Documented in §5 of
    REPORT.md as an internal paper typo.)

## Stage 2 — From-scratch implementation

- `work/stefan_cn.py`:
  - Encodes the transformed PDE (eq. 4) directly in `y ∈ [0,1]` with
    parameters `a, b, c, f, h1, h2, h3` as callables.
  - Time integration: Crank-Nicolson (θ = ½). Space: centered 2nd-order.
  - Each step assembles a tridiagonal system and solves it via
    `scipy.linalg.solve_banded`.
  - Non-homogeneous Dirichlet BC at `y=0, y=1` at times `t_n, t_{n+1}` folded
    into the CN right-hand side.
- Tool versions locked in the run log: Python 3.x, numpy 2.4.3, scipy 1.18.0.
- **No paper code was consulted**; the implementation is derived from the
  decoded equations only.

## Stage 3 — Reproduction runs

- Meshes `M = N ∈ {10, 20, 40, 80, 100}` and horizon `T = 1`, exactly as
  in the paper.
- `work/tables.py`:
  - For each mesh, evaluates the numerical `v` at the paper's chosen nodes
    `(y, t) ∈ {(0.1,0.1), (0.1,0.2), (0.5,0.5), (0.9,0.8)}` and writes
    `evidence/table_reproduction.json` + `evidence/tables_run.log`.
- `work/convergence_fig.py`:
  - Computes global `max |v_num - v_exact|` per mesh; observed order
    `p = log2(e_M / e_{2M})`.
  - Writes `evidence/convergence.json` and the log-log plot
    `evidence/convergence.png` (with a reference slope-2 line).

## Stage 4 — Independent judgement

- `work/judge.py`:
  - Assembles a compact prompt containing the paper's claims (C1-C5), the
    reproduced tables, and the observed convergence numbers.
  - Sends to Argo `argo:gpt-5.2` at `http://localhost:44497/v1` with
    `OPENAI_API_KEY=stevens`.
  - Verdict + free-text justification saved to `evidence/llm_judge.txt`.

## Stage 5 — Report

- `report/REPORT.md` (canonical) — TL;DR, claims table, method, Tables 1 & 2
  reproduction, convergence table, discrepancies, evidence list, verdict.
- `report/REPORT.tex` — same content in LaTeX with a dedicated
  **Genuine Critique** section (P1-P6).
- `report/open_questions.json` — 5 truly open research questions grounded in
  the two-phase Stefan / moving-boundary literature.
- `report/artifacts_summary.md`, `report/failure_analysis.md`, this file.

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Hussein-Stefan-twophase-2020/work
python3 stefan_cn.py
python3 tables.py            # -> ../evidence/table_reproduction.json, tables_run.log
python3 convergence_fig.py   # -> ../evidence/convergence.{json,png}
python3 judge.py             # -> ../evidence/llm_judge.txt (needs Argo at :44497)
```

## Provenance / policy compliance

- **Free endpoints only** (Argo `argo:gpt-5.2`, localhost:44497). No paid API
  calls, no paid `pdf` tool, no vision endpoint.
- **From-scratch reimplementation** (no paper code used).
- **Cross-checked model decoding** against printed `f` before running.
- **Single-writer, resume-safe** — each stage writes to a distinct file under
  `work/` or `evidence/`; the report files are the only artifacts under
  `report/`.
- **Wave provenance:** PDE-100 replication wave, candidate rank 63, one-line
  result recorded in `WAVE_RESULT` at the bottom of `REPORT.md`.
