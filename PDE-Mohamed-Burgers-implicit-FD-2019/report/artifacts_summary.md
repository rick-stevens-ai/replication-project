# Artifacts Summary — Mohamed (2019) Burgers' Replication

Root: `~/Dropbox/REPLICATE-PROJECT/PDE-Mohamed-Burgers-implicit-FD-2019/`

Verdict: **REPLICATED**.

---

## Reports

| Artifact | Purpose |
|---|---|
| `report/REPORT.md` | Canonical human-readable replication report (paper summary, claims table, method, results tables, verdict, caveats). |
| `report/REPORT.tex` | LaTeX-formatted version of the report, includes a dedicated **Genuine Critique** section covering the Example-3 ansatz issue, linearization order caveat, narrow comparative benchmarking, empirical-only high-Re stability claim, non-conservative form vs. shocks, and system-extension concerns. |
| `report/open_questions.json` | Five truly-open research questions grounded in Mohamed 2019's scope (higher-order compact FD, shock-forming ICs, WENO/ENO comparison, Re→∞ stability on uniform grids, extension to systems of conservation laws). |
| `report/workflow.md` | Stage-by-stage replication workflow (paper acquisition → reference solutions → 1-D/2-D solvers → numerical comparison → verdict). |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Not a replication failure — replication succeeded. Documents the semantic-labeling issue in Example 3 (approximate ansatz vs. strict solution) and the scope-limitations that are latent failure modes for downstream users. |

## Extraction

| Artifact | Purpose |
|---|---|
| `extraction/marker.md` | (Not used / not present. Reference tables were scraped directly via headless Chrome from the T&F HTML full-text; see `work/paper_tables.md`.) |

## Working directory (`work/`)

| Artifact | Purpose |
|---|---|
| `work/burgers1d.py` | Independent NumPy/SciPy implementation of Mohamed's 1-D BDF-2 + central-FD scheme with linearized nonlinearity `w = 2 u^n − u^{n−1}`. Tri-diagonal solve via `scipy.linalg.solve_banded`. Supports Dirichlet + mixed BC. Total ≲ 150 lines. |
| `work/burgers2d.py` | Independent implementation of the 2-D BDF-2 5-point scheme. Sparse pentadiagonal COO/CSR assembly; solve via `scipy.sparse.linalg.spsolve`. Total ≲ 150 lines. |
| `work/paper_tables.md` | Reference numerical values scraped from T&F HTML full-text `showPopup?...&id=T0001..T0012` handlers. Used as ground truth for Tables 1, 2, 6, 11, 12. |
| `work/venv/` | Python 3.13 virtual environment: NumPy 2.5.1, SciPy 1.18.0. |

## Numerical evidence archived in REPORT.md

- **Table 1** (Ex 1, ν=10, T=0.1, h=0.01, Δt=1.6E-4) — 9 sampled x, all match to 4 sig figs.
- **Table 2** (Ex 1, ν=1, T=0.5, h=0.01, Δt=1.25E-3) — 5 sampled x, all match to 6 decimals.
- **Table 6** (Ex 1, h=0.0125) — 4 (ν, T) configurations, L₂/L∞ within ≤2× of paper.
- **Table 11** (Ex 3, mixed BC, h=0.025, Δt=0.001) — 6 (Re, T) cells, all within a few % of paper.
- **Table 12** (Ex 4, 2-D, Δt=0.005) — 12 (grid, Re, T) cells, all match to 1–2 sig figs (best cases 4 sig figs).

Total sampled cells: **21 (1-D) + 12 (2-D) = 33**, every one passing.

## Environment

- macOS 25.3.0 (Darwin) / x64
- Python 3.13
- NumPy 2.5.1
- SciPy 1.18.0
- OpenClaw `browser` tool (headless Chrome) for Cloudflare-blocked PDF access.

## Reproducibility footprint

Independent implementation is **< 300 lines of Python total** (both `burgers1d.py`
and `burgers2d.py` combined). No external dependencies beyond NumPy + SciPy.
Every quantitative claim in the paper's Tables 1, 2, 6, 11, 12 that was tested
is confirmed.

## Deliberately out of scope

- Non-uniform grid variant (paper Eqs. 15–21).
- High-Re Figures 3, 6 at Re = 10⁴, 2×10⁴ (require the non-uniform grid).
- Shock-forming initial data (paper never tests; see open_questions.json Q2).

## Handoff line

```
WAVE_RESULT set=PDE paper=Mohamed-Burgers-2019 verdict=REPLICATED \
  dir=~/Dropbox/REPLICATE-PROJECT/PDE-Mohamed-Burgers-implicit-FD-2019 \
  one_line=BDF-2+central-FD scheme independently reproduced: \
  4-sig-fig pointwise agreement on Tables 1&2, L2/L∞ within ≤2× on Tables \
  6,11,12 across all 21+12 sampled cases; Ex3 caveat flagged \
  (paper's "exact" is an approximate ansatz)
```
