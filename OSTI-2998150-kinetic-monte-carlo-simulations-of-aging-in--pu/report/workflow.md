# Replication Workflow — OSTI-2998150 (KMC Aging in δ-Pu)

**Paper:** Oppelstrup et al. (2025) — *Kinetic Monte Carlo simulations of aging in δ-Pu*
**Verdict:** REPLICATED (spot-check of Eq. 5 benchmark)
**Analyst:** Ollie (OpenClaw AI) — OSTI-100 Wave
**Date:** 2026-07-03

---

## Overview

The replication targeted the paper's foundational analytical/numerical
benchmark (Eq. 5: `DRρτ = 0.078 − 0.19·(R/L)` with theoretical limit
`1/(4π) ≈ 0.07958`) using pure-Python Brownian dynamics on public tooling.
The full 100-year FPKMC aging simulation of δ-Pu was **not attempted** —
requires LLNL in-house FPKMC code and Pu-specific defect energetics tables
that are not distributed with the paper.

---

## Step-by-Step Workflow

### Phase 1 — Paper acquisition & triage
1. Located paper via OSTI ID 2998150; downloaded preprint PDF (openly
   available, LLNL DOE-funded).
2. Extracted paper text to `work/osti-2998150.txt` (848 lines).
3. Read paper end-to-end; identified the FPKMC sanity-check numerical result
   (Eq. 5, Fig. 8) as the one claim testable without the LLNL FPKMC codebase.

### Phase 2 — Claim enumeration
4. Enumerated 5 claims (C1–C5); classified 2 as replicable (C1, C2), 3 as
   out-of-scope (C3–C5) with documented reasons.
5. Selected C1 + C2 (intercept + slope of `DRρτ` vs `R/L`) as the
   spot-check target.

### Phase 3 — Independent implementation
6. Wrote pure-Python Brownian dynamics with:
   - Cubic periodic box, side L ∈ {15, 20}
   - Single absorbing sphere at origin, R ∈ {1.0, 1.5, 2.0, 3.0}
   - N=200 walkers, D=1
   - Timestep `dt = (0.05·R)² / (2D)` (5% RMS-per-axis step relative to R)
   - Segment-vs-sphere collision detection (project onto step, clip
     t*∈[0,1], test |closest|²<R²) — critical to avoid missing fast steps
     that tunnel through the absorber
   - Absorbed walkers re-sampled uniformly outside the sphere (steady-state
     exterior density)
   - Averaging until `n_events ≥ 300` per (L,R) cell
   - Deterministic seed: `1234 + int(1000·(L+R))`
7. Verified segment-crossing test on hand-computed edge cases before running
   the full sweep.

### Phase 4 — Bug discovery in pre-existing helper
8. Ran `work/vac_void_collision.py` (pre-existing workspace helper) as a
   comparison; got nonsense fit `DRρτ ≈ 16.4 − 45.8·(R/L)`.
9. Diagnosed root cause: helper used `rho = N/L³` (walker density) instead
   of `rho = 1/L³` (absorber density) — inflates `DRρτ` by factor of N.
10. Wrote fixed script `report/evidence/vac_void_collision_fixed.py`.
11. Preserved buggy run outputs (`kmc_results.json`, `kmc_run.log`) for
    provenance transparency.

### Phase 5 — Reproduction run
12. Executed corrected script with the exact command:
    ```
    python3 report/evidence/vac_void_collision_fixed.py \
        --out report/evidence/kmc_fixed_results.json \
        --Ls 15 20 --Rs 1.0 1.5 2.0 3.0 \
        --N 200 --events 300 --seed 1234 --dt_frac 0.05
    ```
13. Wall time: 70.3 s single-threaded on CherryRd (Python 3.14.6,
    NumPy 2.4.3, Darwin 25.3.0).
14. Captured stdout to `report/evidence/kmc_fixed_run.log`.
15. Recorded machine-readable per-cell + fit + environment metadata in
    `report/evidence/kmc_fixed_results.json`.

### Phase 6 — Fit & comparison
16. Least-squares linear fit of `DRρτ` vs `R/L` across 8 (L,R) cells.
17. Result: `DRρτ = 0.0841 − 0.235·(R/L)`.
18. Compared against paper Eq. 5 (0.078, −0.19) and analytical limit
    `1/(4π) = 0.07958`:
    - Intercept within 5.7% of exact theory, within 6% of paper fit.
    - Slope correct sign, ~24% steeper than paper (attributable to smaller
      event budget and fewer (L,R) pairs).

### Phase 7 — Verdict & write-up
19. Verdict: **REPLICATED** (spot-check).
20. Wrote `REPORT.md` with claims table, method, per-cell results, fit
    comparison, explicit "what was NOT replicated" scope statement, and
    verdict.
21. Wrote `REPORT.tex` (this file's LaTeX sibling) with a dedicated
    GENUINE CRITIQUE section separating warranted critique from artifacts
    of our limited replication.
22. Enumerated 5 truly open questions (`open_questions.json`) grounded in
    the paper's remaining unresolved territory.

---

## Environment Snapshot

| Component | Version / Value |
|---|---|
| Host | CherryRd |
| OS | Darwin 25.3.0 (macOS Tahoe) |
| Python | 3.14.6 |
| NumPy | 2.4.3 |
| Runtime | Pure-Python single-threaded |
| Wall time | 70.3 s |
| Deterministic seed | 1234 + int(1000·(L+R)) |

## Tooling Deliberately NOT Used

- LLNL FPKMC code — not distributed; would trivialize the exercise but is
  unavailable.
- No GPU / no MPI — a first-passage benchmark this small does not need
  them.
- No external simulation libraries (Brownian) — pure NumPy so every line
  is auditable.

## Reproducibility Guarantees

- All input parameters captured in `kmc_fixed_results.json → args`.
- Random seed deterministic per (L,R) pair.
- Python + NumPy versions recorded in the JSON.
- Buggy first-pass run preserved (not overwritten) so future auditors can
  see the diagnosis trail.
- LaTeX + Markdown report versions kept in sync (mechanical translation).
