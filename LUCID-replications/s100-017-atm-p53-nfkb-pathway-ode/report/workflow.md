# Replication Workflow — s100-017 (Jonak et al. 2016 ATM/p53/NF-κB ODE)

**Sub-agent:** Argo Opus 4.7 (out-of-band, free-endpoint only)
**Host:** CPU-only, laptop-class
**Date:** 2026-06-22 (original replication) / 2026-07-06 (LaTeX+critique backfill)

## Phase 1 — Acquisition
1. Downloaded paper PDF + all 10 BMC supplementary files (MOESM1..10) to `source/`.
2. `pdftotext -layout` on paper → `ocr/raw_layout.txt`; on each MOESMx.pdf → `ocr/MOESMx.txt`.
   (No OCR pass needed: BMC PDFs are text-layer, not scanned.)
3. Confirmed license: CC-BY 4.0 (BMC open access) — replication + redistribution OK.

## Phase 2 — Model extraction
1. Transcribed MOESM4 parameter tables (5 tables × ~110 rate constants) into
   `code/parameters.py`. Preserved paper's symbol names verbatim.
2. Transcribed MOESM1 equations (Eqs. 1–72) into `code/model.py` as a 60-state
   ODE RHS. Substituted mean-field expressions for the 10 gene-state
   Gillespie propensities: `dG/dt = a_on·(N_A − G) − a_off·G`.
3. Transcribed MOESM3 initial-condition tables (Ctr-RNAi and Wip1-RNAi variants)
   into `code/initial_conditions.py`.
4. Verification pass (line-by-line diff against OCR); resolved 3 typos in
   the parameter table (paper's PDF had non-breaking spaces mid-number).

## Phase 3 — Sanity checks
1. `run_steady.py`: integrate 48 h with zero input (dose=0, TNF=0). Confirmed
   that Ctr-RNAi IC set has <1% drift on every major species → ICs are the
   true steady state → RHS is faithful.
2. Repeated for Wip1-RNAi IC set → same result.

## Phase 4 — Reproduction runs
1. `run_ir.py` — 10 Gy IR (1 Gy/min pulse for 600 s, then 24 h follow-up) for
   both RNAi conditions. Reproduces Figs. 2 & 3. Wrote `evidence/claims_10Gy.json`.
2. `run_dose_response.py` — 6 doses (0, 2, 4, 6, 8, 10 Gy) × 2 RNAi lines,
   plus 3-arm TNFα timing experiment (TNF-only, IR-only, TNF+3h+IR).
   Reproduces Fig. 4. Wrote `evidence/dose_response.json` and `tnf_experiment.json`.
3. Saved full trajectories to `evidence/trajectories_10Gy.npz` (60 × 481 × 2).
4. Plotted 4 figures under `figures/`.

## Phase 5 — Claim tabulation
1. Extracted 15 numerical/qualitative claims from paper Results §1–§3 + Fig 4.
2. Scored each claim against reproduced trajectories: 12 ✅, 1 △ (mean-field
   DSB gap, documented), 2 ⊘ (out-of-scope stochastic).
3. Wrote REPORT.md with claim table + blocker analysis.

## Phase 6 — Verdict
- Coverage 8/10 (deterministic ODE core fully covered; stochastic layer not).
- Agreement 8/10 (all deterministic claims agree qualitatively + semi-quantitatively).
- **Verdict: REPLICATED.** Matches queue.

## Phase 7 — Backfill (2026-07-06)
1. Read existing REPORT.md (report/REPORT.md).
2. Verdict cross-check: queue REPLICATED, on-disk REPLICATED → no mismatch.
3. Wrote REPORT.tex with full claim table + honest Critique section addressing
   Rick's 2026-07-05 hard requirements (pulse period/amplitude, NF-κB timescale,
   identifiability, crosstalk).
4. Wrote 5 truly-open questions targeting: single-cell heterogeneity vs
   population-mean, ATR/CHK1 extension, parameter identifiability, low-dose
   stochastic regime, tumor-cell-line mutation contexts.
5. Wrote workflow.md (this file), artifacts_summary.md, failure_analysis.md,
   extraction/nougat.mmd stub.
6. No re-runs. All artifacts CPU-only, free-endpoint only.

## Reproducibility
- Deterministic (LSODA, no random seeds).
- CPU-only, <30 s total wall-clock for all three run scripts.
- Deps: `numpy scipy matplotlib`.
- Bit-for-bit reproducible on any platform with the same NumPy/SciPy version.

## Free-endpoint compliance
- All model runs local CPU (no LLM inference).
- LaTeX + JSON + Markdown authored offline.
- No paid API calls, no GPU-hours consumed, no external network.
