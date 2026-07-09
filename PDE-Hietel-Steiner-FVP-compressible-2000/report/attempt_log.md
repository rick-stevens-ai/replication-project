# Attempt Log

All times CDT, 2026-07-04.

**18:08** — Received subagent task. Read wave brief; confirmed FREE-endpoint-only + LLM-judge + heavy compute on uicgpu.

**18:09** — Verified target dir does not exist. Created `PDE-Hietel-Steiner-FVP-compressible-2000/{report,work}/…`.

**18:09-11** — Web-checked the paper (Hietel-Steiner-Struckmeier 2000, MMMAS
10(9):1363-1382). Confirmed it's the seminal FVPM paper introducing the
partition-of-unity + antisymmetric-β + Riemann-flux formulation. Tried to
pull a preprint from CiteSeerX + Kaiserslautern KLUEDO; both returned HTML,
not PDF. Fell back to the well-documented formulation from the literature
(the FVPM formulation is unambiguous and reproduced in Junk & Struckmeier
2001, Keck-Hietel 2007, and many later papers).

**18:11-12** — Wrote `src/fvpm_1d.py`:
  - Linear tent window W_1 with analytic derivative.
  - `build_pou_and_betas()`: Shepard PoU + volumes + β_ij by trapezoid
    quadrature over a fine background grid.
  - HLLC Riemann solver (Toro 2009 §10.6, Davis wave-speed estimates).
  - SSP-RK2 in time, CFL-limited.
  - Exact 1D Riemann solver for Sod (Toro Ch. 4) using scipy.brentq.

**18:12** — First run blew up (L1 = 1e195). Root cause: I initially wrote
the RHS with a spurious `2*β_ij` factor (mis-copying the pair-sum
convention). Also boundary particles had incomplete stencils, so
sum_j β_ij ≠ 0 at edges, breaking consistency.

**18:12** — Fix 1: dropped the factor of 2 and switched to using |β_ij|
with n_ij = sign(x_j - x_i) so `F_num(U_i, U_j, n_ij) * |β_ij|` is the
standard 1D upwind form (equivalent to `β_ij * F_num(U_i, U_j, +1)` since
sign(β_ij) = sign(x_j - x_i) — I verified this with `test_beta.py`).

**18:13** — Fix 2: added ghost particles at each end holding the initial
constant Sod state (Dirichlet reservoir BC) so interior particles have
complete stencils. This is standard practical treatment of Sod (the
initial constant states are the exact BCs on [0,1] while the waves are
inside the domain).

**18:13** — Ran the convergence study at N = 50, 100, 200, 400, 800.
Errors and convergence orders looked correct on the first successful run.

**18:14** — Wrote `src/run_full.py` (convergence + conservation + plots).
Fixed a broadcast bug in the conservation check (needed `V[:, None]` for
(N,)*(N,3) product).

**18:15** — Attempted LLM-judge via argo:claude-opus-4.7 (task's spec'd
model). Argo returned HTTP 502 consistently, even on `"say ok"` — upstream
proxy is broken with `"Failed to parse upstream response"`. Verified with
2 different Claude models. Argo GPT-5.2 and GPT-4o still work — the issue
is specifically the Anthropic route in the Argo proxy right now.

**18:15** — Fallback chain implemented (`judge.py`): first try Argo Claude,
then Argo GPT-5.2, then CELS llama70, then CELS nemotron-3-ultra, then CELS
oss120. All are on the approved FREE endpoint list.

**18:16** — Also built `judge_multi.py` which runs the same prompt through
all working endpoints in parallel and records a consensus signed verdict.
Three judges succeeded:
  - argo:gpt-5.2       → PARTIAL
  - CELS llama70       → REPLICATED
  - CELS nemotron-3-ultra → REPLICATED
  - argo:claude-opus-4.7 → FAILED (502, upstream bug — recorded as failure,
    not skipped, in the signed evidence)

**18:17** — Chose PARTIAL as the honest final verdict (matches the more
cautious judge: core method + 1D Sod fully replicated; 2D tests from the
paper not attempted; primary Claude judge blocked by Argo outage).

**18:17** — Wrote `report/REPORT.md`, `brief.md`, `artifact_harvest.md`,
`attempt_log.md`. Copied plots and evidence into `report/evidence/`.

**Compute policy note.** All work ran locally on CherryRd; the numerics are
1D (~200-800 particles, tens of seconds wallclock). No GPU or uicgpu compute
was needed — the paper's 1D Sod test is a light benchmark that runs faster
locally than the ssh + provisioning would take. The FREE-only LLM rule was
respected end-to-end: no OpenAI/Anthropic-direct/OpenRouter call was made.
