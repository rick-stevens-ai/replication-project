# Replication report — Dürr & Høyer (1996) "A quantum algorithm for finding the minimum"

- **arXiv:** [quant-ph/9607014](https://arxiv.org/abs/quant-ph/9607014) (v2, 7 Jan 1999)
- **Set / rank:** QC / 17
- **Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-quantum-minimum-finding-durr-hoyer-1996/`
- **Replicator:** independent subagent, 2026-07-06
- **Verdict:** **PARTIAL**
- **Judge model:** `argo:gpt-5.2` (via Argo free endpoint, key=stevens)

## 1. Paper summary

Dürr & Høyer give a quantum algorithm that finds the index of the minimum value in an
unsorted table `T[0..N-1]` of distinct elements using `O(√N)` oracle probes. The scheme:
pick a random threshold index `y`, invoke Grover-search (via BBHT's exponential
searching that does not assume knowledge of the count of marked items) with the oracle
that marks all `j` with `T[j] < T[y]`, and if a strictly smaller element is measured
adopt it as the new threshold; repeat until an iteration budget is exhausted. Theorem 1
states this returns the true minimum with probability ≥ 1/2 within a budget of
`22.5·√N + 1.4·lg²N` Grover iterations.

## 2. Claims table

| # | Claim | Type | Testable? | Tested? |
|---|-------|------|-----------|---------|
| C1 | Algorithm returns true minimum with probability ≥ 1/2 within stated budget (Thm 1). | Correctness/probability | Yes | Yes (300 trials × 5 sizes) |
| C2 | Iteration budget expression is `22.5·√N + 1.4·lg²N`. | Formula | Yes | Yes (checked implementation matches) |
| C3 | BBHT subroutine finds a marked item in expected `O(√(N/t))` iters for t ≥ 1 marked. | Complexity | Yes | Yes (t-sweep, 21 (N,t) cells) |
| C4 | Classical baseline requires linear O(N) probes. | Reference bound | Yes | Yes (measured) |

## 3. Method (numbered)

1. **Environment** — Python 3.14.6, numpy 2.4.3. No external quantum SDK — pure NumPy
   statevector was chosen for independence and speed.
2. **Grover core** (`work/durr_hoyer_independent.py`) — on `n = log₂ N` qubits: initial
   state `|s⟩ = 1/√N Σ_j |j⟩`; oracle `O_f: |j⟩ ↦ (-1)^{f(j)}|j⟩` implemented as
   in-place amplitude sign flip on a boolean mask; diffusion `D = 2|s⟩⟨s| - I`
   implemented as `2·mean(ψ) - ψ`; measurement via inverse-CDF sampling of `|ψ|²`.
3. **Grover sanity check** (`work/grover_sanity.py`) — for `(N,k)` in a 12-cell grid,
   compared empirical single-shot success prob (2000 trials each) at `r* = round(π/4·√(N/k))`
   against closed-form `sin²((2r+1)θ)`, `sinθ=√(k/N)`. Max |Δ| = 0.027.
4. **BBHT subroutine** — starts `m = 1`, on each round samples `r ∈ [0, ⌈m⌉)` uniformly,
   runs `r` Grover iterations, measures, tests membership in marked set, on failure sets
   `m ← min(6/5·m, √N)` and repeats. If no items are marked (t = 0) it burns through the
   available budget without ever succeeding (matches the "runs forever" corner in the paper).
5. **Outer Dürr–Høyer loop** — random-uniform initial `y`; while total Grover-iterations
   used < budget: mark all `j` with `T[j] < T[y]`, call BBHT with the remaining budget;
   if it returns an index whose value is smaller than `T[y]`, adopt it.
6. **Budget** — implemented exactly as `⌈22.5·√N + 1.4·lg²N⌉` (values below).
7. **Main experiment** — `--Ns 4 8 16 32 64 --trials 300 --seed 20260706` per size, each
   trial a fresh random permutation of `range(N)`. Wrote `report/evidence/results.json`.
8. **BBHT t-sweep** — for `N ∈ {16, 32, 64, 128}` and `t ∈ {1, 2, 4, N/8, N/4, N/2}`,
   300 trials each; recorded mean/median/std Grover iters and ratio `mean/√(N/t)`.
   Wrote `report/evidence/bbht_t_sweep.json`.
9. **Classical baseline** — deterministic linear-scan argmin, 100 trials per `N ∈ {4..512}`.
   Wrote `report/evidence/classical_baseline.json`.
10. **LLM-judge** — POSTed paper text + all three evidence blobs to
    `http://localhost:44497/v1/chat/completions` (Argo, free) with a strict rubric,
    parsed the returned JSON. Argo Claude Opus was returning 502 during the run so the
    verdict was rendered by `argo:gpt-5.2` (also free).

## 4. Results vs paper

### 4.1 C1 — Success probability (Theorem 1)

| N | trials | successes | success prob | paper bound |
|---|--------|-----------|--------------|-------------|
| 4 | 300 | 300 | **1.000** | ≥ 0.5 |
| 8 | 300 | 300 | **1.000** | ≥ 0.5 |
| 16 | 300 | 300 | **1.000** | ≥ 0.5 |
| 32 | 300 | 300 | **1.000** | ≥ 0.5 |
| 64 | 300 | 300 | **1.000** | ≥ 0.5 |

**Reproduced** in all tested sizes (with margin). Judge downgrades to *partially* because
the tight ≥1/2 bound is not stress-tested (empirical failure never observed at N ≤ 64).

### 4.2 C2 — Budget formula

| N | 22.5·√N | 1.4·lg²N | budget (impl) | budget (paper) |
|---|---------|----------|---------------|----------------|
| 4 | 45.00 | 5.60 | 51 | 22.5·√N + 1.4·lg²N |
| 8 | 63.64 | 12.60 | 77 | ″ |
| 16 | 90.00 | 22.40 | 113 | ″ |
| 32 | 127.28 | 35.00 | 163 | ″ |
| 64 | 180.00 | 50.40 | 231 | ″ |

Implementation matches the paper's formula exactly (rounded up). **Reproduced.**

### 4.3 C3 — BBHT scaling `O(√(N/t))`

Ratio `mean_iters_to_marked / √(N/t)` should be bounded by an O(1) constant.

| N | t | mean_iters | √(N/t) | ratio |
|---|---|-----------|--------|-------|
| 16 | 1 | 1.85 | 4.00 | 0.463 |
| 16 | 2 | 1.13 | 2.83 | 0.400 |
| 16 | 4 | 0.67 | 2.00 | 0.333 |
| 32 | 1 | 3.31 | 5.66 | 0.585 |
| 32 | 4 | 1.20 | 2.83 | 0.424 |
| 64 | 1 | 5.89 | 8.00 | 0.737 |
| 64 | 4 | 1.67 | 4.00 | 0.417 |
| 128 | 1 | 9.09 | 11.31 | 0.803 |
| 128 | 4 | 3.35 | 5.66 | 0.593 |
| 128 | 16 | 1.00 | 2.83 | 0.355 |
| 128 | 32 | 0.68 | 2.00 | 0.342 |

All 21 cells have ratio ≤ 0.81 (with a mild upward drift in N at fixed t, as expected
from the sub-leading terms in BBHT). **Reproduced.**

### 4.4 C4 — Classical baseline O(N)

| N | mean_probes | O(N) |
|---|-------------|------|
| 4 | 4 | 4 |
| 64 | 64 | 64 |
| 512 | 512 | 512 |

Deterministic, exactly `N`. **Reproduced.**

## 5. Verdict + justification

**PARTIAL** (per LLM-judge). Rationale:
- Core algorithmic behavior reproduced end-to-end on real (randomly generated) input:
  100% empirical success at the paper-stated budget for N up to 64.
- Budget formula matches.
- BBHT sqrt(N/t) scaling directly measured and consistent.
- Classical O(N) baseline measured and consistent.
- Judge held back "REPLICATED" because (a) N up to 64 is small (single log-scale
  spread), (b) the ≥1/2 tightness never observed in a failure regime, (c) no
  confidence intervals reported. All fair calls — flagged in `failure_analysis.md`.

## 6. Open Questions

See `open_questions.json`. Q1..Q5:

- **Q1** — At what N does the empirical success prob start dipping toward the ≥1/2
  paper bound? (My N=4..64 sees 300/300; higher N with fewer iterations may reveal it.)
- **Q2** — Ratio `iters/√(N/t)` in BBHT drifts from 0.46 (N=16, t=1) to 0.80 (N=128,
  t=1). Is that transient (log-lower-order term) or does the effective constant grow?
- **Q3** — How does the outer-loop iteration count itself scale relative to the H_N
  harmonic-number bound the paper derives? I did not extract that per-run.
- **Q4** — Non-distinct values (ties): the paper assumes distinct T[j]; how does the
  algorithm degrade if the oracle uses `<=` vs `<`?
- **Q5** — Sensitivity of BBHT to λ (I used 6/5): does another value in (1, √2) speed
  up the outer loop's expected iterations?

## 7. Files

- `paper.pdf`
- `extraction/{marker.md, nougat.mmd}`
- `work/durr_hoyer_independent.py` (main)
- `work/grover_sanity.py`
- `work/bbht_t_sweep.py`
- `work/classical_baseline.py`
- `work/llm_judge.py`
- `report/REPORT.tex` (detailed)
- `report/{brief.md, attempt_log.md, artifact_harvest.md, workflow.md,
  artifacts_summary.md, failure_analysis.md, open_questions.json}`
- `report/evidence/{results.json, grover_sanity.json, bbht_t_sweep.json,
  classical_baseline.json, llm_judge.json}`
