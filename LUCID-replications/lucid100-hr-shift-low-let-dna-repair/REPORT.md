# REPORT — Belov et al. 2023 (CIMB 45:7352)
**DOI:** 10.3390/cimb45090465  
**Replicated paper:** Dose-Dependent Shift in Relative Contribution of HR to DNA Repair after Low-LET Ionizing Radiation Exposure: Empirical Evidence and Numerical Simulation
**LUCID-100 slot:** Wave 2, slot 19
**Promotion attempt:** 2026-06-27 by Ollie sub-agent (model: argo:claude-opus-4.7)
**Pre-promotion state:** SPOT-CHECK (audit 2026-06-20, coverage 2/10, agreement 6/10)

---

## Verdict

**PARTIAL — full ODE model implemented and run; reproducibility issue surfaced.**

| Dimension | Score | Notes |
|---|---:|---|
| **Coverage** | **5/10** | Closed-form smoke (DSB yield + Nirrep) **and** full 29-state ODE system (Eqs A4–A7) **and** PHR(D) sweep (Fig 7 analog) **and** γH2AX/Rad51 kinetics for all 7 paper doses (Figs 5/6 analog) **and** cell-cycle population averaging (45/55 split) **and** sensitivity analysis on K12. Empirical data (Figs 2, 3, 4, 8 foci-count tables and CENPF fractions) remain blocked (data unavailable from authors). |
| **Agreement** | **4/10** | Closed-form quantities reproduce paper formulas exactly. Full ODE as-printed in Table A1 **contradicts the paper's central claim** of monotonic PHR(D) decrease — instead produces a U-shaped PHR(D) and γH2AX foci 4-6 orders of magnitude smaller than the kinetics shown in Figs 5–6. With a 100× correction to K12 (γH2AX spontaneous-decay rate; a plausible decimal-point typo correction), the low-dose half of the PHR(D) curve qualitatively matches paper text (~93% → ~22% from 5 to 250 mGy), but the high-dose half still inverts (PHR(1000 mGy) = 189% in our model vs paper's qualitative ~15%). |

**Promotion outcome:** SPOT-CHECK (2/10, 6/10) → **PARTIAL (5/10, 4/10)**.  Note that Agreement dropped because the deeper ODE replication exposes a substantive contradiction that the prior smoke-only audit could not have detected. This is an honest demotion-of-agreement that should not be averaged out.

---

## What was done in this promotion pass

### 1. Closed-form smoke (carried over from first pass)
- **Eq A1** initial DSB yield N0 = α(L)·D with α(L)=a·exp(−bL); a=27.5, b=2.43e-3 — reproduces paper formula exactly.
- **Table A1** Nirrep(D) piecewise — reproduces paper formula exactly; shape is non-monotonic with peak ≈0.087 near 250 mGy and floor 0.01 at D ≥ 1 Gy.
- Code: `scripts/smoke_dsb_yield.py`.  Outputs: `results/smoke_dsb_yield*.csv`, `figures/smoke_dsb_yield.png`.

### 2. Full ODE replication — NEW
- **`scripts/full_ode_model_v2.py`** — 29 dynamic states, raw-units integration (M, h), scipy LSODA.  Implements Eqs (A4)–(A7) verbatim from JATS XML (`artifacts/equations_A4_A7.txt`).  ~1 s wall-clock per dose.
- **`scripts/full_ode_model.py`** — original scaled-units version, retained for cross-check. Produces identical trajectories up to numerical noise.
- All 7 paper doses (20, 40, 80, 160, 250, 500, 1000 mGy) computed for both HR-competent (55% late-S/G2/M) and HR-incompetent (45% G0/G1/early-S) subpopulations, then population-weighted per paper §2.2.
- **PHR(D) sweep** on 18 dose points from 5 to 1000 mGy.
- Code: `scripts/full_ode_model_v2.py`. Outputs: `results/ode_h2ax_kinetics.csv`, `results/ode_rad51_kinetics.csv`, `results/ode_PHR_vs_dose.csv`, `results.json`, `figures/ode_full_model.png`.

### 3. Sensitivity-corrected run — NEW
- **`scripts/sensitivity_corrected.py`** — same model with K12 (γH2AX spontaneous decay) reduced 100× from the printed 11.10 h⁻¹ to 0.111 h⁻¹.  Rationale: 11.10 h⁻¹ gives a γH2AX foci half-life of ~4 minutes, contradicting the widely-established literature consensus of 3–8 h (Rogakou 1999, Riballo 2004, Bouquet 2006).  A missing decimal in 11.10 vs 0.111 is the most parsimonious explanation.
- Outputs: `results/ode_h2ax_kinetics_corrected.csv`, `results/ode_rad51_kinetics_corrected.csv`, side-by-side PHR comparison in `results/ode_PHR_vs_dose.csv`, four-panel figure in `figures/ode_full_model.png`.

---

## Claim-by-claim verification table

| # | Paper claim | Source | Tested? | Result | Tolerance / Notes |
|---|---|---|---|---|---|
| 1 | DSB induction follows α(L)·D with a=27.5, b=2.43e-3 | Table A1, Eq A1 | ✅ Yes | **VERIFIED** | Exact reproduction of formula |
| 2 | Nirrep(D) piecewise: low-dose biexponential, plateau 0.01 at D≥1 Gy | Table A1 | ✅ Yes | **VERIFIED** | Exact reproduction of formula |
| 3 | PHR(D) decreases ~monotonically with dose; PHR ≈ 70% at low D and ≈ 15% at 1 Gy | §3.2, Fig 7 (text only — figure values not OCR'd, derived from PDF text) | ✅ Yes | **PARTIALLY CONTRADICTED** | As-printed ODE gives U-shape (4341→1012→8821 % from 5→200→1000 mGy). K12-corrected ODE: monotonic decrease at 5–250 mGy (93→22 %), then *increases* back up at 250–1000 mGy (22→189 %). Low-dose magnitude (~93% at 5 mGy → ~22% at 250 mGy) is within ~30% of paper's qualitative endpoints, but high-dose behavior diverges. |
| 4 | Peak γH2AX timing shifts: 500–1000 mGy peak at 0.25–1.0 h vs 20–250 mGy peak at 0.25–2.0 h | §3.1, Fig 2 (text) | ✅ Yes | **CONTRADICTED** | Our model peaks at t=24 h for ALL doses (monotonically growing source from chained recruitment).  No early-peak structure in either as-printed or K12-corrected runs.  This is the same failure mode as claim 3: γH2AX dynamics are wrong without empirical-fit overrides. |
| 5 | γH2AX residual at 24 h elevated at 40–80 mGy, suppressed at 500–1000 mGy vs control | §3.1, Fig 2 (text) | ⚠️ Partial | **NOT INTERPRETABLE** | The model has no "control" baseline (no background DSBs in the equations), so the "below-control" qualitative claim cannot be tested. The residual γH2AX/peak ratio is ~100% for all doses in our model (no decay over 24h because peak is at 24h). |
| 6 | Cell-cycle (CENPF+) S/G2 fraction decreases 2.15×, 3.69×, 6.93× at 250, 500, 1000 mGy | §3.3, Fig 8 | ❌ No | **BLOCKED** | This is a measurement, not a model output. Raw cell counts not released. |
| 7 | Foci-count "shift bins": peak-timing 250–500 mGy, residual γH2AX 80–500 mGy, residual Rad51 80–160 mGy | §4, Discussion | ❌ No | **BLOCKED** | Requires raw foci-count tables behind Figs 2, 3 (not released). |
| 8 | 30-ODE mass-action model with parameters in Table A1 successfully reproduces the experimental γH2AX & Rad51 kinetics in Figs 5–6 | §3.2, Figs 5–6 | ✅ Yes | **CONTRADICTED** | Model runs but produces γH2AX peaks of order 10⁻⁵ – 5×10⁻⁴ foci/cell, vs paper figures showing ~5–30 foci/cell. Even with K12-corrected, peaks are still 10⁻³ – 10⁻² foci/cell (~1000× too small). Several rate constants in Table A1 (notably K1=11.05 M⁻¹h⁻¹ for Ku binding) are 6–10 orders of magnitude smaller than literature consensus values and produce essentially no NHEJ throughput. |

**Summary:** Of 8 testable claims, 2 are fully VERIFIED (closed-form formulas), 1 PARTIALLY CONTRADICTED (PHR(D) shape — qualitative low-dose match, high-dose disagreement), 2 fully CONTRADICTED (peak timing, full-model agreement with Figs 5–6), 1 NOT INTERPRETABLE, and 2 BLOCKED by data unavailability.

---

## Headline numerical comparison

### PHR(D) — model vs paper (qualitative text values, no figure OCR available)

| Dose (mGy) | Paper (text estimate) | Model (as-printed K12=11.10) | Model (K12=0.111 corrected) |
|---:|---:|---:|---:|
| 20  | ~70%  | 2399.42% | **51.42%** |
| 80  | ~50%  | 1278.13% | 27.41% |
| 250 | ~30%  | 1011.72% | 21.70% |
| 500 | ~20%  | 1445.94% | 31.01% |
| 1000| ~15%  | 8821.99% | **188.67%** |

Bold rows: low- and high-dose model values. The corrected model agrees with paper at low dose (51% vs ~70%), but inverts at high dose (189% vs ~15%).

### γH2AX foci peak per cell (corrected K12=0.111/h)

| Dose (mGy) | Peak foci/cell (model) | Time of peak (h) | 24-h residual/peak (model) |
|---:|---:|---:|---:|
| 20  | 1.10e-5 | 24.0 | 100% |
| 40  | 3.07e-5 | 24.0 | 100% |
| 80  | 8.30e-5 | 24.0 | 100% |
| 160 | 2.04e-4 | 24.0 | 100% |
| 250 | 3.28e-4 | 24.0 | 100% |
| 500 | 4.59e-4 | 24.0 | 100% |
| 1000| 1.49e-4 | 24.0 | 100% |

Paper Figs 2, 5 show peaks of order 5–30 foci/cell with peaks at 0.25–2.0 h.  **Both magnitude (1000× too small) and timing (24h vs sub-hour) of the simulated foci disagree with the paper figures.**

---

## Root-cause analysis of the as-printed model failure

The published Table A1 parameter set, integrated faithfully, produces:
1. Nearly-zero γH2AX foci because the NHEJ recruitment chain (K1=11.05 M⁻¹h⁻¹ is the slowest 2nd-order rate constant in the entire table by 3+ orders of magnitude) barely consumes the initial n0 over 24 h.
2. Saturating Rad51 foci because the HR chain has irreversibly fast late steps (P7=21.36/h, P8=1.2e4 M⁻¹h⁻¹) but extremely slow terminal cleanup (P11=6.06e-4/h, half-life ~1100 h).
3. A U-shaped PHR(D) curve because Nirrep(D) has a sharp discontinuity at D=1 Gy (cliff from ~0.04 to 0.01) which spikes K10 = 1.93e-7/Nir from ~5e-6 M to 1.93e-5 M and suppresses γH2AX via the Michaelis-Menten term.

The paper's stated formula PHR(D) = 100 × ȳ9(D) / x̄14(D) (Eq 29) is therefore extremely sensitive to:
- The K12 value (γH2AX decay)
- The Nirrep(D) cliff at D=1 Gy
- The choice of "Rad51 foci" proxy (paper notation y9 is ambiguous: it is reused as both a constant precursor concentration and an unlabeled dynamic variable)

With K12=0.111/h (likely typo correction) and Rad51 proxy = sum of y11+y13+y14+y15 (Rad51 filament and downstream complexes), the model matches the paper's qualitative low-dose claim but contradicts the high-dose claim.

---

## Sensitivity analysis (K12 scan)

| K12 (h⁻¹) | PHR(20 mGy) | PHR(80 mGy) | PHR(250 mGy) | PHR(1000 mGy) | Shape |
|---:|---:|---:|---:|---:|---|
| 11.10 (as printed) | 2399% | 1278% | 1012% | 8822% | U-shape |
| 1.110 (10× lower) | 260% | 139% | 110% | 956% | U-shape |
| 0.555 | 142% | 76% | 60% | 522% | U-shape |
| 0.333 | 96% | 51% | 40% | 352% | U-shape |
| 0.222 | 73% | 39% | 31% | 268% | U-shape |
| **0.111 (100× lower)** | 51% | 27% | 22% | 189% | U-shape |
| 0.055 | 41% | 22% | 17% | 151% | U-shape |

**Even with arbitrary K12 reduction, PHR(D) never becomes monotonically decreasing across 5–1000 mGy.**  The U-shape persists.  The high-dose upturn comes from the Nirrep(D) cliff at D=1 Gy, not from K12.

Holding K10 constant (no D-dependence on Nirrep) flattens PHR(D) to ~97% across all doses — confirming that the dose-dependence of PHR is entirely driven by the K2(D), K4(D), P9(D), and K10(D) phenomenological parameterizations, none of which the paper derives mechanistically.

---

## Reproducibility friction (updated)

| Friction | Severity | New evidence |
|---|---|---|
| As-printed Table A1 does not reproduce paper's central claim | **HIGH** (NEW) | Full 29-ODE solve under multiple parameter interpretations consistently produces wrong PHR(D) shape and wrong γH2AX magnitudes |
| K12 = 11.10 h⁻¹ likely typo (should be 0.111 or 1.110) | **HIGH** (NEW) | Implausible 4-min γH2AX half-life vs literature 3–8 h; 100× reduction produces qualitatively-correct low-dose PHR(D) |
| K1 = 11.05 M⁻¹h⁻¹ likely typo (should be ~1e7) | **HIGH** (NEW) | 6+ orders of magnitude below literature values for Ku-DSB binding; the rate-limiting step makes the entire NHEJ chain too slow to repair DSBs in 24 h |
| R4 listed twice (1.47e5 vs 12.30) | LOW (carried over) | Almost certainly typesetting collision with missing R5 label |
| Source model (Belov 2015 JTB) paywalled | MED (carried over) | "Particular details of parameter evaluation" unavailable |
| Data Availability = "Not applicable" | HIGH (carried over) | Empirical foci-count tables withheld |
| No source code released | HIGH (carried over) | "Authors' own code"; no GitHub or supplement |
| Cell-cycle fractions hard-coded to "HF19-like" 45/55 | LOW (carried over) | Justified via ref [49] |
| Integration step dt = 1e-10 s (paper) | NOTE (carried over) | LSODA handles much larger steps fine |

---

## 6/22 rule — exact missing artifacts

This pass is **NOT blocked** in the 6/22 sense; full ODE re-implementation succeeded.  Remaining work *would* require:

1. **Raw foci-count tables** for the 7 doses × 8 time-points (≈336 cell-population means) behind Figs 2 and 3.  These are not released and not available via Europe PMC supplement (see `paper/supp_list.json`).  Without them, the dose-dependent functions K2(D), K4(D), P9(D), and the Nirrep(D) piecewise can NOT be independently re-fit, and the question of whether a corrected parameter set could match Figs 5–7 cannot be answered from the paper alone.
2. **Authors' simulation source code** — not on GitHub or as supplement; would resolve any ambiguity about the y9 notation collision and the scaling convention.

Both blockers are documented in `PROGRESS.md`; campaign policy is to NOT contact authors for raw data.

---

## Deliverables in this folder

### Carried over from first pass
* `paper/` — paper PDF (Europe PMC render), JATS XML, stripped markdown
* `artifacts/equations_A4_A7.txt` — verbatim ODE systems
* `artifacts/table_A1_parameters.csv` — full Appendix C parameter table
* `scripts/smoke_dsb_yield.py` — closed-form smoke script (DSB yield + Nirrep)
* `results/smoke_dsb_yield*.csv`, `figures/smoke_dsb_yield.png`
* `README.md`, `PROGRESS.md`, `ARTIFACT_MANIFEST.md` — overview / status / inventory

### New in this promotion pass (2026-06-27)
* `scripts/full_ode_model.py` — 29-state ODE in scaled units (v1, retained for cross-check)
* `scripts/full_ode_model_v2.py` — 29-state ODE in raw units (M, h), used for headline results
* `scripts/sensitivity_corrected.py` — side-by-side as-printed vs K12-corrected run
* `results/ode_h2ax_kinetics.csv`, `results/ode_rad51_kinetics.csv` — kinetics for 7 paper doses (as-printed)
* `results/ode_h2ax_kinetics_corrected.csv`, `results/ode_rad51_kinetics_corrected.csv` — same with K12=0.111
* `results/ode_PHR_vs_dose.csv` — PHR(D) sweep, both runs side-by-side
* `results.json` — bundled headline metrics for both runs + claim-check map
* `figures/ode_full_model.png` — 4-panel comparison (kinetics top, PHR(D) bottom)
* `logs/full_ode_model_v2.log`, `logs/sensitivity_corrected.log` — full stdout

### Backups
* `REPORT.md.bak-pre-promo` — pre-promotion REPORT (first-pass + 2026-06-20 audit overlay)

---

## Bottom line

The first-pass report claimed the full ODE replication was "feasible from the paper alone … estimated at 2–4 person-days" but flagged "high uncertainty in the fitted rate constants."  This promotion pass actually executed that work in a few hours of agent time — and confirmed the high-uncertainty concern with concrete evidence: **the published Table A1 parameter set, integrated faithfully, contradicts the paper's central PHR(D) claim**.

This is a substantive finding for the LUCID-100 portfolio.  The closed-form quantities (Eq A1, Nirrep) are exactly reproducible from text alone.  The mechanistic ODE model has at least two probable typos (K12, K1) and at least one structural issue (the Nirrep cliff at D=1 Gy producing a U-shaped PHR(D)).  Without raw foci-count data to refit K2(D)/K4(D)/P9(D)/Nirrep(D), no parameter perturbation we tried recovers the paper's monotonic PHR(D) curve across the full 5–1000 mGy range.

The model is reproducible at the "every equation runs" level (5/10 coverage); whether it is reproducible at the "matches Figs 5–7" level (≤2/10 agreement at high dose) cannot be answered without data that is not available.  We assign PARTIAL.
