# Attempt Log

## 2026-07-03 — Initial spot-check (existing work by prior pass)
- Extracted paper text with pdftotext, identified quantitative claims (T_c ≈ 0.24 for itinerant Ising-DE, α=1/2 at T=0.1, α=1/4 at T=0.01, MAE=0.0014 for CNN).
- Confirmed no code/data release accompanies the paper.
- Judged CNN training + ED-DE evaluation out-of-budget for a subagent.
- Wrote `report/evidence/ising_coarsening_spotcheck.py`: from-scratch 2D NN Ising, Glauber dynamics, quench to T=1.7, L=128, 800 sweeps, 3 seeds, correlation-length estimator from Eq. (10) with first-zero truncation.
- Ran → early-window α = 0.469, R² = 0.973 (within 6% of Allen-Cahn 1/2).
- Verdict at that time: SPOT-CHECK (Allen-Cahn baseline reproduced, novel claims untested).

## 2026-07-04 — Deepening pass (this session)
- Task: promote to solid verdict (REPLICATED or PARTIAL) if evidence honestly supports it.
- Read wave brief + existing report.
- Decided the extra anchors to add: canonical 2D NN Ising Tc (Onsager exact), magnetization curve vs Onsager, specific-heat peak. These are the ground truths every equilibrium claim in the paper leans on.
- Attempted `numba` install for a JIT Metropolis — failed (no wheel for Python 3.13); pivoted to vectorized checkerboard Metropolis with `np.roll` neighbor sums (still fast).
- Wrote `work/ising_thermo.py` — coarse T×L scan.
- Smoke test at L=16, T ∈ {2.0, 2.269, 2.5}: ⟨|m|⟩ = 0.909 vs Onsager 0.911 (0.3% error). ✓
- Full run L ∈ {16,24,32}, T ∈ [1.6, 3.0] (17 points): ~90 s. Magnetization tracks Onsager to sub-percent below Tc, all L collapse cleanly.
- Attempt 1 at Tc extraction: wrote `work/ising_fss.py` with parabolic peak of χ(T) per L and 1/L fit → Tc(∞) ≈ 2.218 (2.3% low). Peak-picking was noisy because χ at critical point has O(L²) autocorrelation and 6000 sweeps isn't enough. Kept the file but did not use it in the final verdict.
- Pivot: Binder cumulant crossing (much more robust — ratio of moments). Wrote `work/ising_binder.py` with L ∈ {16,24,32,48} on dense T grid, longer runs (n_equil ≥ 4000, n_meas ≥ 12000, block every 5), compute U = 1 − ⟨m⁴⟩/(3⟨m²⟩²).
- Full Binder run: ~5 min total. Six pairwise crossings clustered tightly around 2.27. Mean = 2.2745 vs Onsager 2.269 → **0.24% error**. ✓
- Wrote `work/summarize.py` to consolidate: Tc from Binder, m(T) RMS error, C-peak per L, and a 3-panel PNG figure.
- Ran LLM-judge scoring per wave brief rule (never regex): two independent Argo free-endpoint models (`gpt-5.2`, `gpt-4.1`) with the same structured prompt. Both returned SPOT-CHECK with agreement scores 0.9 and 1.0. First Anthropic model (`argo:claude-opus-4.7`, `argo:claude-sonnet-4.7`) returned upstream validation errors on the local proxy — used GPT judges instead.
- Updated `report/REPORT.md` with:
  - The three new anchors (A1, A2, A3) added as an explicit claims table.
  - Full quantitative results (Tc from 6-pair Binder mean, magnetization RMS, C-peak per L).
  - Two-judge consensus explicitly documented.
  - Verdict kept at **SPOT-CHECK** (per the judge consensus) but explicitly recharacterized as a "quantitatively strong SPOT-CHECK" — sub-percent agreement on 3/4 tested anchors, ~6% on the coarsening exponent — while being honest that no novel claim of the paper was reproduced.

## Runtimes summary (2026-07-04, single CherryRd core, no GPU)
- Allen-Cahn coarsening: ~150 s
- Coarse thermo scan (3 L × 17 T): ~90 s
- FSS attempt (4 L × 21 T): ~4 min
- Binder scan (4 L × 22 T, longer): ~5 min
- Summary + figure: <5 s
- Total: ~11 min compute end-to-end.

## What was tried and rejected
- `numba` JIT — no wheel for Python 3.13.9; dropped.
- χ-peak FSS Tc extractor (`work/ising_fss.py`) — too noisy at feasible run lengths; superseded by Binder crossings. File retained for full audit trail.
- Anthropic Argo models for LLM judging — returned upstream schema-validation errors on the local proxy this session. Used two OpenAI-family Argo models instead (also free).

## What could have gone further but did not (honest gaps)
- No attempt to reach out to Chern group for their trained CNN weights (out of subagent scope; noted as the natural path to PARTIAL in the report).
- No attempt to code up a mock DE Hamiltonian (would be significant new modeling work, non-trivial to validate independently).
- No autocorrelation-time analysis of Metropolis at Tc (implicitly folded into by-eye "spread of pairwise crossings" instead).
