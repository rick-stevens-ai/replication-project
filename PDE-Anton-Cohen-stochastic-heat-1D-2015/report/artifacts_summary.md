# Artifacts Summary — Anton–Cohen–Quer-Sardanyons (2017/2020) SEXP Replication

Inventory of the code, data, and evidence produced by this replication. Paths are relative
to `~/Dropbox/REPLICATE-PROJECT/PDE-Anton-Cohen-stochastic-heat-1D-2015/`.

## 1. Source paper artifacts

| Path | What it is |
|---|---|
| `work/anton_cohen_2015.pdf` | arXiv v1 PDF of the paper (fetched via `curl`, OA route). |
| `work/anton_cohen_2015.txt` | `pdftotext -layout` dump of the PDF, used for equation extraction. |
| `work/src/` | Unpacked LaTeX e-print (`tar xzf`) — canonical for Eq. (15) symbol chase. |
| `work/src.tar.gz` | Original arXiv e-print tarball. |
| `artifact_harvest.md` | Log of the curl commands, hashes, and access timestamps. |

Access route: `https://arxiv.org/pdf/1711.08340v1` and `.../e-print/1711.08340v1`. OA only,
no paid endpoint, no `pdf` tool.

## 2. Solver code

| Path | Purpose |
|---|---|
| `work/sexp_heat.py` | Core SEXP solver. Applies $e^{A\Delta t}$ via DST diagonalization: `IDST(exp(λ·Δt) * DST(v))` with `scipy.fft.dst/idst` type-1, `norm='ortho'`. Cross-checked at machine precision vs. dense `scipy.linalg.expm` at $M=16$ (max diff 3.3e-16). |
| `work/validate_deterministic.py` | Deterministic sanity harness (σ=0, f=0): checks SEXP linear-part exactness, agreement with $e^{\lambda_1 T}\sin(\pi x)$, and FD spatial convergence rate 2.000 against $u(t,x)=e^{-\pi^2 t}\sin(\pi x)$. Must pass before any stochastic run. |

## 3. Experiment code

| Path | Experiment | Claim addressed |
|---|---|---|
| `work/run_strong_order.py` | Single-process strong-order sweep (pilot / small-M development). | C2 |
| `work/run_strong_order_mp.py` | 96-worker multiprocessing strong-order sweep on uicgpu. Command used: `python3 run_strong_order_mp.py --M 512 --kref 16 --kcoarse 3 4 5 6 7 8 9 10 --samples 500 --procs 96`. Implements Brownian consistency by block-summing the finest increments. | C2 (headline) |
| `work/run_as_convergence.py` | Almost-sure / pathwise convergence, 5 paths, $M=512$, $\Delta t_{\text{ref}}=2^{-15}$. | C3 |
| (embedded in `run_strong_order_mp.py`) | Stability sweep: single path, $\Delta t \in \{2^{-1},\dots,2^{-16}\}$, record final $\max|u|$. | C1 |

## 4. Multi-judge harness

| Path | What it is |
|---|---|
| `work/run_judges.sh` | Bash harness: POSTs `judge_summary.txt` to Argo endpoints and captures each response verbatim. |
| `work/judge_summary.txt` | The exact quantitative summary + prompt served to each judge (identical text across judges). |
| `report/evidence/judge_argo_gpt-5.2.txt` | Full judge response (verdict + rationale). |
| `report/evidence/judge_argo_gemini-2.5-pro.txt` | Full judge response. |
| `report/evidence/judge_argo_gpt-4.1.txt` | Full judge response. |

All three verdicts: **REPLICATED**. Opus deliberately avoided per standing rule for
replication scoring.

## 5. Evidence files (canonical numeric outputs)

| Path | Content | Referenced in |
|---|---|---|
| `report/evidence/validate_deterministic.txt` | Machine-precision checks: 5.5e-15 time-exactness; 1.7e-16 vs analytic; FD rate 2.000 at $M=32,64,128,256,512,1024$. | REPORT §4 / C4 |
| `report/evidence/evidence_strong_order_full.json` | Per-Δt E[sup\|·\|^2] and RMS values for Δt=2^-3..2^-10 at $M=512$, $M_s=500$; slope (log₂) 1.115; RMS strong order 0.558. | REPORT §4 / C2 |
| `report/evidence/evidence_as_convergence.json` | Per-path (5 paths) sup-in-(t,x) errors + fitted per-path slopes {0.568, 0.525, 0.562, 0.547, 0.535}. | REPORT §4 / C3 |
| `report/evidence/judge_*.txt` | Verbatim LLM judge responses. | REPORT §6 |

## 6. Reports

| Path | Role |
|---|---|
| `report/REPORT.md` | Canonical narrative + tables + verdict. |
| `report/REPORT.tex` | Detailed LaTeX with dedicated **GENUINE CRITIQUE** section. |
| `report/open_questions.json` | Five truly open follow-up questions, each with basis + next steps. |
| `report/workflow.md` | End-to-end procedure log. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Documented failure modes and reconciliations. |

## 7. Headline numbers (single-line summary)

- **Verdict.** REPLICATED.
- **Strong temporal RMS order (measured).** 0.558 (paper: 1/2).
- **CFL sweep.** $\max|u|$ ∈ [0.039, 1.98] across $\Delta t = 2^{-1},\dots,2^{-16}$ at $M=512$.
- **Pathwise slopes (5 paths).** 0.568, 0.525, 0.562, 0.547, 0.535.
- **Deterministic validation.** SEXP time-exact to 5.5e-15; FD space rate exactly 2.000.
- **Judges.** 3/3 REPLICATED (gpt-5.2, gemini-2.5-pro, gpt-4.1 on Argo, non-opus).

## 8. Environment pins (for exact reproduction)

| Host | Role | numpy | scipy |
|---|---|---|---|
| CherryRd | validation, pilots | 2.4.3 | 1.18.0 |
| uicgpu (8×A100, 255 cores) | strong-order + a.s. Monte Carlo (96 workers) | 1.23.5 | 1.10.1 |
| Argo proxy `localhost:44497` | LLM judges (gpt-5.2, gemini-2.5-pro, gpt-4.1) | — | — |
