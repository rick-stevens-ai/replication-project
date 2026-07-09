# Artifacts Summary — PDE-Hussein-Stefan-twophase-2020

Directory root: `~/Dropbox/REPLICATE-PROJECT/PDE-Hussein-Stefan-twophase-2020/`

## report/ — human-readable outputs (canonical)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical Markdown replication report (TL;DR, claims C1-C5, method, Tables 1 & 2 reproduction, convergence, discrepancies, verdict). |
| `REPORT.tex` | LaTeX version of the report with a dedicated **Genuine Critique** section (P1-P6). |
| `open_questions.json` | 5 truly open research questions on two-phase Stefan / moving-boundary numerics (front-tracking vs level-set, t=0+ singularity, 2D/3D anisotropic extension, convection coupling, coupled Stefan condition). |
| `workflow.md` | End-to-end replication workflow: source acquisition → model decoding → implementation → reproduction → judgement → report. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Documented issues encountered and how they were resolved (paper typos, OCR-only decoding, MMS-scope limits). |

## work/ — source code and paper materials

| File | Purpose |
|---|---|
| `paper.pdf` | Open-access source PDF from the publisher galley (MD5 `9905e28d…`). Fetched via `curl`; **not** via the paid `pdf` tool. |
| `paper.txt` | `pdftotext -layout` dump of the paper for text-level reference. |
| `stefan_cn.py` | From-scratch Crank-Nicolson solver for the Landau-transformed fixed-domain PDE (eq. 4). Uses numpy 2.4.3 + `scipy.linalg.solve_banded` (scipy 1.18.0). |
| `tables.py` | Driver that reproduces Table 1 (Ex 1) and Table 2 (Ex 2) node values on meshes M=N ∈ {10,20,40,80,100}. |
| `convergence_fig.py` | Computes global `max|v_num − v_exact|` per mesh, observed order `p = log2(e_M/e_{2M})`, and emits the log-log convergence plot with a reference slope-2 line. |
| `judge.py` | Sends the compact claims-plus-results prompt to Argo `argo:gpt-5.2` at `localhost:44497` and records the returned verdict. |

## evidence/ — machine-checkable outputs

| File | Purpose |
|---|---|
| `table_reproduction.json` | Node-by-node numerical vs. exact vs. paper values for Table 1 and Table 2. |
| `tables_run.log` | Console output of the reproduction runs. |
| `convergence.json` | Per-mesh `max` absolute error and observed convergence order. |
| `convergence.png` | Log-log error vs. `h` plot with reference slope-2 line. |
| `llm_judge.txt` | Free-Argo (`gpt-5.2`) LLM judge verdict + justification. |

## Headline numbers (from REPORT.md)

**Example 1 (Table 1):** all four selected node values match the paper's own
transformed exact formula to 4 decimal places; global error `O(10⁻¹³)–O(10⁻¹⁴)`
across all meshes (matches paper). One printed value (`3.4124` at node
`(0.1,0.2)`) is a paper typo — the correct value from the paper's own formula
is `3.1424`.

**Example 2 (Table 2):** every printed node value on every mesh
(M=N ∈ {10,20,40,80,100}) matches this replication to 4 decimal places.

**Convergence (Ex 2):**

| M=N | max abs error | observed p |
|---|---|---|
| 10 | 3.75e-03 | — |
| 20 | 9.60e-04 | 1.97 |
| 40 | 2.41e-04 | 2.00 |
| 80 | 6.02e-05 | 2.00 |
| 100 | 3.85e-05 | 2.00 |

`p → 2.0` confirms the paper's claim of second-order accuracy.

## Compute footprint

- **Hardware:** local numpy/scipy on CherryRd (macOS). No GPU. No HPC.
- **Wall time:** small — the 1D CN tridiagonal solve at M=N=100, T=1 is
  sub-second per run; the full mesh sweep + tables + convergence plot
  completes in well under a minute end-to-end.
- **LLM cost:** free — Argo `argo:gpt-5.2` at `localhost:44497` only, one
  judge call.

## Policy / provenance flags

- Free endpoints only (no paid API, no paid `pdf` tool, no vision endpoint).
- From-scratch reimplementation (no paper code consulted).
- Model decoding cross-checked against the paper's own printed `f` (Ex 1:
  exact match; Ex 2: mismatch flagged and traced to an internal paper typo).
- Verdict: **REPLICATED**.
