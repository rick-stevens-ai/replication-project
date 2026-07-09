# Workflow — Anton–Cohen–Quer-Sardanyons (2017/2020) Replication

**Paper.** *A fully discrete approximation of the one-dimensional stochastic heat equation*
(arXiv:1711.08340, IMA J. Numer. Anal.). Rank 30 on `PDE_NEXT50_2026-06-26.tsv`.
**Set.** PDE-100 replication wave.
**Verdict.** REPLICATED.

This document is a **process** log of how the replication was executed, complementing
`REPORT.md` (which records the results). It exists so a follow-up replication (human or
subagent) can rerun the pipeline end-to-end without re-deriving the ordering.

---

## Phase 0 — Selection & framing

- Pulled Rank 30 from `PDE_NEXT50_2026-06-26.tsv` (score 52.77, 90 citations).
- Confirmed distinctness from other PDE-100 stochastic dirs (Burgers, Zhang-modal, deepxde) —
  none implement the FD + stochastic exponential integrator (SEXP) scheme.
- Registered target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Anton-Cohen-stochastic-heat-1D-2015/`
  and family = "Parabolic SPDE / stochastic PDE numerics".

## Phase 1 — Artifact harvest

1. `curl -o work/anton_cohen_2015.pdf https://arxiv.org/pdf/1711.08340v1`
2. `curl -o work/src.tar.gz https://arxiv.org/e-print/1711.08340v1`
3. `pdftotext -layout work/anton_cohen_2015.pdf work/anton_cohen_2015.txt`
4. `tar xzf work/src.tar.gz -C work/src/`
5. Log: `artifact_harvest.md`.

**Rule followed.** OA-only fetch via `curl`; no `pdf` tool; no paid endpoint.

## Phase 2 — Method extraction (paper → executable spec)

Read Sec. 2 (scheme, Eq. 15) and Sec. 2.2.3 (numerical experiment). Extracted:

- Domain: (0, 1), Dirichlet BC.
- Space: FD on interior grid $x_m = m/M$, $m=1..M-1$, $\Delta x = 1/M$.
- Operator: $A = M^2 D$, $D = \mathrm{tridiag}(1,-2,1)$.
  Eigenvalues $\lambda_j = -4 M^2 \sin^2(j\pi / 2M)$, sine eigenvectors.
- Time: **SEXP** Eq. (15): $U^{n+1} = e^{A \Delta t} U^n + F(U^n)\Delta t + \Sigma(U^n) \Delta W^n$.
- Test problem: $u_0 = \sin(\pi x)$, $f(u) = u/2$, $\sigma(u) = 1-u$, $T = 0.5$, $M = 512$,
  $\Delta t \in \{2^{-1}, \dots, 2^{-16}\}$, $M_s = 500$.

## Phase 3 — Implementation

Files under `work/`:

- **`sexp_heat.py`** — SEXP solver. Applies $e^{A \Delta t}$ via DST diagonalization:
  `IDST(exp(λ·Δt) * DST(v))` using `scipy.fft.dst/idst` type-1, `norm='ortho'`.
- **`validate_deterministic.py`** — deterministic sanity checks.
- **`run_strong_order.py`** — single-process strong-order sweep (development/pilot).
- **`run_strong_order_mp.py`** — 96-worker multiprocessing version for `uicgpu`.
- **`run_as_convergence.py`** — 5-path almost-sure/pathwise convergence experiment.
- **`run_judges.sh`** + **`judge_summary.txt`** — multi-judge harness against Argo free tier.

## Phase 4 — Validation (BEFORE any stochastic runs)

Executed on CherryRd (numpy 2.4.3, scipy 1.18.0):

1. **DST-diagonalization vs. dense `expm`:** max diff = 3.3e-16 at M=16. ✓
2. **SEXP linear-part exact in time (σ=0, f=0):**
   `max|u(Δt=2^-4) - u(Δt=2^-10)| = 5.5e-15`. ✓
3. **SEXP vs. analytic $e^{\lambda_1 T} \sin(\pi x)$:** `1.7e-16`. ✓
4. **FD → analytic PDE spatial convergence** ($u = e^{-\pi^2 t}\sin(\pi x)$):
   rate 2.000, 2.000, 2.000, 2.000, 2.000 across $M = 32, 64, 128, 256, 512, 1024$. ✓

Only after all four passed did we proceed to stochastic experiments. Evidence:
`evidence/validate_deterministic.txt`.

## Phase 5 — Strong-convergence experiment (C2)

Compute host: **uicgpu** (8×A100, 255 cores; numpy 1.23.5, scipy 1.10.1), 96 workers.

**Brownian consistency.** Coarse and fine share the SAME Brownian path via block-summing
of the finest increments (fine grid at Δt_ref = 2^-16, coarse grids at Δt = 2^-3..2^-10
formed by summing $2^{16-k}$ consecutive fine increments per coarse step). This isolates
the *temporal* discretization error and is standard for SPDE strong-order estimation.

Command:
```
python3 run_strong_order_mp.py \
    --M 512 --kref 16 --kcoarse 3 4 5 6 7 8 9 10 \
    --samples 500 --procs 96
```

Error metric:
$$\sup_{(t,x) \in [0, 0.5]\times[0,1]} \mathbb{E}[|u^{M,N}(t,x) - u^M_{\text{ref}}(t,x)|^2]$$
implemented as spatial max over interior nodes × temporal max over a snapshot grid ×
Monte-Carlo mean over 500 samples.

Output: `evidence/evidence_strong_order_full.json`.
Slope of $\mathbb{E}[\sup|\cdot|^2]$ vs. Δt (log₂) = 1.115 ⇒ RMS order = **0.558**.

## Phase 6 — Pathwise experiment (C3)

Same host, 5 independent paths, $M = 512$, $\Delta t_{\text{ref}} = 2^{-15}$. Per-path
sup-in-(t,x) error vs. Δt fitted per-path.
Slopes: 0.568, 0.525, 0.562, 0.547, 0.535.
Output: `evidence/evidence_as_convergence.json`.

## Phase 7 — Stability sweep (C1)

Single path, $M = 512$, log-spaced $\Delta t \in \{2^{-1}, \dots, 2^{-16}\}$, record
final $\max|u|$. Confirms bounded $\mathcal{O}(1)$ across the full range → CFL-free.
Output table in `REPORT.md §4/C1`.

## Phase 8 — Noise-scaling reconciliation

During Phase 7 the literal-symbol reading of Eq. (15) with $\Delta W^n \sim \mathcal{N}(0, \Delta t)$
was found to blow up at $M = 512$ for $\Delta t > 2^{-10}$ (measured $\max|u| \sim 10^6$–$10^{13}$).
Traced to double-application of the $\sqrt{M}$ factor. The physically-standard cell-increment
reading ($\Delta W^n \sim \mathcal{N}(0, \Delta t / M)$) cancels one $\sqrt{M}$, giving net per-node
noise $\sigma(u_m)\sqrt{\Delta t}\,\xi$, and recovers CFL-freeness + Fig-1 order.
Documented in `REPORT.md §5`. All three judges accepted the reconciliation.

## Phase 9 — Multi-judge scoring

Free Argo endpoints only (**no opus**), each given the same summary + prompt:

- `argo:gpt-5.2`
- `argo:gemini-2.5-pro`
- `argo:gpt-4.1`

All three returned **REPLICATED**. Full texts: `evidence/judge_*.txt`.

## Phase 10 — Report assembly

- `REPORT.md` — canonical narrative + tables + verdict.
- `REPORT.tex` — detailed LaTeX version with dedicated **GENUINE CRITIQUE** section.
- `open_questions.json` — 5 truly open follow-up questions with basis and next steps.
- `workflow.md` (this file).
- `artifacts_summary.md` — inventory of code and evidence.
- `failure_analysis.md` — record of the noise-scaling blowup and validation-first discipline.

---

## Environment pins

| Host | Role | numpy | scipy |
|---|---|---|---|
| CherryRd | validation, pilots | 2.4.3 | 1.18.0 |
| uicgpu (8×A100, 255 cores) | strong-order + a.s. Monte Carlo (96 workers) | 1.23.5 | 1.10.1 |
| Argo proxy `localhost:44497` | LLM judges (gpt-5.2, gemini-2.5-pro, gpt-4.1) | — | — |

## Standing rules honored

- Free endpoints only (Argo, no paid API).
- No `pdf` tool.
- Deterministic validation BEFORE any stochastic experiment.
- Coarse/fine Brownian consistency (block-summing) for strong-order.
- Non-opus judges (as per Rick's standing rule for replication scoring).
