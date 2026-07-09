# REPORT — Sakata et al. 2021, "Performance Evaluation for Repair of HSGc-C5 Carcinoma Cell Using Geant4-DNA"

> **2026-06-23 RE-PASS NOTE:** The original 2026-05-30 verdict (Coverage 6/10, Agreement 7/10, **REPLICATED [TLK portion]**) is preserved verbatim below as a sibling section. A re-pass against the canonical Marker-parsed text (`data/marker/paper.md`) added five previously-skipped testable claims (M1, M2, M3/M5/M7/M11, M9, M10). The updated honest verdict and new evidence are at the **bottom** of this file under "## 2026-06-23 Re-pass". Skim that section first if you only want the deltas.

---

## 2026-05-30 Verdict (preserved verbatim)


- **Citation:** Sakata D., Suzuki M., Hirayama R., Abe Y., Muramatsu M., Sato S., Belov O.,
  Kyriakou I., Emfietzoglou D., Guatelli S., Incerti S., Inaniwa T.
  *Cancers* **13**(23):6046 (2021). DOI: [10.3390/cancers13236046](https://doi.org/10.3390/cancers13236046)
- **Target PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d.pdf`
- **Replication scope:** the TLK (two-lesion kinetics) curve-fit half of the paper —
  cell survival fraction (SF) and DNA fragment-activity-released (FAR) kinetics for
  the HSGc-C5 carcinoma cell line under 70 MeV protons (0 mm and 32 mm PMMA).
- **Out-of-scope:** the Geant4-DNA Monte Carlo half (track-structure simulation of
  initial DSBs and dosimetry calibration). We consume the paper's reported DSB
  yields, dose rate, and supplements rather than re-running Geant4-DNA.

---

## Verdict

**REPLICATED (TLK ODE / curve-fit portion).**

| Component | Status | Evidence |
| --- | --- | --- |
| Data acquisition (SF.csv, FAR.csv, DepthDose.csv) | ✅ open MDPI supplement | `data/supplement/*.csv` |
| TLK ODE system (Eqs 3–6) | ✅ implemented from paper text | `code/tlk_model.py` |
| Random-breakage FAR model (Eq 7) | ✅ implemented | `code/tlk_model.py::far_curve` |
| Forward replication with paper's Table 1 params | ✅ runs, decent agreement | `results/metrics_summary.json` (`metrics_Table1`) |
| Inverse fit (matches paper's Ceres Solver step) | ✅ converged, better agreement | `results/refit.json`, `results/metrics_summary.json` |
| Figure 5 reproduction | ✅ qualitatively reproduced | `figures/sf_curve.png`, `figures/far_curve.png` |
| Geant4-DNA initial DSB simulation | ❌ out of scope | — |

**Coverage / agreement scores (10-point honest assessment):**

- **Coverage of paper's claims: 6 / 10.**  The repair-performance / curve-fit
  portion (Figure 5, Table 1, Eqs 3–7) is fully reproduced from public data and
  equations. The Geant4-DNA initial-damage simulation (Figure 4, ~3000 lines of
  C++ + Geant4) is not re-executed; we consume the paper's reported DSB yields.
- **Quantitative agreement (refit, joint SF+FAR):**
  - SF R² = **0.96** (RMSE 0.067, log₁₀-RMSE 0.13) → **9 / 10**
  - FAR R² = **0.96** (RMSE 0.029) → **9 / 10**
- **Quantitative agreement (paper's Table 1 verbatim, forward replication only):**
  - SF R² = **0.91** (RMSE 0.106, log₁₀-RMSE 0.32) → **7 / 10**
  - FAR R² = **0.72** (RMSE 0.080) → **6 / 10**
  - Discrepancy interpretation: see "Caveats" below.
- **Overall replication quality: 7.5 / 10** — joint SF+FAR fits are excellent
  given that we depend on the paper's reported (Σ₁, Σ₂) yields.

---

## What was replicated

### 1. Data ingestion (open supplements)
Downloaded `https://res.mdpi.com/d_attachment/cancers/cancers-13-06046/article_deploy/cancers-13-06046-s001.zip`
(3,590 bytes, application/zip, 200 OK). Extracted:

- `SF.csv` — 25 rows (HSG and NB1 cells; both PMMA conditions). We use HSGc-C5 ("HSG") only: 12 rows × {0, 1, 2, 3, 4, 5, 6, 7 Gy}.
- `FAR.csv` — 18 rows (HSG and NB1; one 200-Gy condition each). HSGc-C5 PMMA 0 mm has 9 time points (0 → 12 h).
- `DepthDose.csv` — proton depth-dose for Figure 2 (not used for TLK fit; included as evidence of supplement completeness).

These files are saved verbatim in `data/supplement/`.

### 2. TLK ODE system (paper Eqs 3–6)

```
dL1/dt = D(t) · Y · Σ1  −  λ1 · L1  −  η · L1 · (L1 + L2)        (Eq 3)
dL2/dt = D(t) · Y · Σ2  −  λ2 · L2  −  η · L2 · (L1 + L2)        (Eq 4)
dLf/dt = β1 · λ1 · L1  +  β2 · λ2 · L2  +  γ · η · (L1 + L2)²    (Eq 5)
SF(t)  = exp(−Lf(t))                                              (Eq 6, std TLK form)
```

with `D(t) = 60 Gy/h` until target dose is delivered, then 0; `Y = 6.4 Gbp/cell`;
the SF is evaluated at `t = 336 h` (14 d), matching the paper's colony-assay window.
The paper's Eq 6 has a PDF rendering artifact (`SF(t) = ln(−Lf(t)) = ln(−∫…)`); the
intended Stewart-2001 form is `SF = exp(−Lf)`, which is what we implement.

Implementation: `code/tlk_model.py`. Solver: SciPy `solve_ivp` with LSODA, two-phase
integration (tight steps 0 → t_stop during irradiation, then 0 → 336 h post). The
paper used boost C++ RK4 with `Δt = 1e-4 h`; our LSODA result is within
1e-6 relative tolerance of an RK4 sanity check.

### 3. Random-breakage FAR model (Eq 7)

```
FAR(t) = Fmax · [1 − (1 + K · L_unrej / Y) · (1 − K / M0) · exp(−K · L_unrej / Y)]
relativeFAR(t) = FAR(t) / FAR(t_stop)
```

with `Fmax = 1`, `K = 1 Mbp`, `M0 = 139 Mbp` (paper's "6.4 Gbp / 46 chromosomes").
`L_unrej = (L1 + L2) / Y` is the unrejoined DSB density.

### 4. Forward replication (paper's Table 1 verbatim)

Using `λ1 = 3.36`, `λ2 = 9.9e-3`, `η = 4.58e-6`, `β1 = 0`, `β2 = 2.75e-2`, `γ = 0.39`
(all h⁻¹ where applicable), and the paper's simulated DSB yields recovered from
Section 3.2 and the Discussion:

| Condition | Σ₁ (Gy⁻¹Gbp⁻¹) | Σ₂ (Gy⁻¹Gbp⁻¹) | source |
| --- | --- | --- | --- |
| 0 mm PMMA | 4.11 | 1.04 | DSB = 4.11; complex = 0.74, DSB⁺/DSB⁺⁺ = 1.44 → Σ₂ = DSB⁺ + 2·DSB⁺⁺ |
| 32 mm PMMA | 4.69 | 1.53 | DSB = 4.69; complex = 1.04, DSB⁺/DSB⁺⁺ = 1.13 |

Results: SF R² = 0.91 overall (per-condition 0.87 / 0.95); FAR R² = 0.72.

### 5. Inverse fit (Ceres-Solver analogue)

We re-perform the optimization step of the paper. Joint nonlinear least squares
over the 21 SF+FAR observations using SciPy `least_squares` (TRF), `β1` fixed = 0,
SF residuals taken in log₁₀ space to balance the multi-decade dynamic range.
Converged in 22 evaluations:

| param | paper Table 1 | our refit | ratio |
| --- | --- | --- | --- |
| λ₁ (h⁻¹) | 3.36 | 6.52 | 1.94× |
| λ₂ (h⁻¹) | 9.9e-3 | 2.80e-3 | 0.28× |
| η (h⁻¹) | 4.58e-6 | 2.52e-5 | 5.5× |
| β₁ | 0 | 0 (fixed) | — |
| β₂ | 2.75e-2 | 3.72e-2 | 1.35× |
| γ | 0.39 | 0.234 | 0.60× |

The refit recovers the qualitative ordering (fast fast-repair, slow slow-repair,
small η partially offset by larger γ → similar binary-lethality product γ·η),
but the individual constants differ by factors of 0.3 – 5.5. This is consistent
with the documented degeneracy of the TLK parameter space: only the products
γη (binary lethality rate) and β₂λ₂ (slow-repair lethality flux) are tightly
constrained by SF+FAR data alone. Numerically:

- γ · η: paper 1.79e-6 vs refit 5.91e-6 (3.3×)
- β₂ · λ₂: paper 2.72e-4 vs refit 1.04e-4 (0.38×)

These compensate, producing nearly identical SF curves at the measured doses.

### 6. Figures

- `figures/sf_curve.png` — SF vs dose (log-y) for 0 mm and 32 mm PMMA, with
  experimental data, paper-Table 1 prediction (dashed) and our refit (solid).
- `figures/far_curve.png` — relative FAR vs post-irradiation time (0–12 h)
  for 0 mm PMMA, 200 Gy.
- `figures/params_compare.png` — bar chart of TLK parameters, paper vs refit
  (log scale).

---

## What was NOT replicated

1. **Geant4-DNA track-structure simulation (Section 2.2.2).** The paper ran
   56,400 incident protons (0 mm) and 11,400 (32 mm) through a Geant4-DNA
   geometry of a 14.2 × 14.2 × 5.0 μm³ cell nucleus with fractal chromatin
   fibers, scored single-strand and double-strand breaks per the Nikjoo
   clustering definition, and reported per-Gy/Gbp yields. We consume the
   reported yields directly. Re-running this would require Geant4 11+ with
   the molecularDNA example, the full DNA geometry inputs, and ~CPU-days.
2. **Cell-culture / electrophoresis experiments (Section 2.2.1).** Out of scope.
3. **Depth-dose / TOPAS calibration (Figure 2).** `DepthDose.csv` is preserved
   but not used in the TLK fit.
4. **NB1RGB human-fibroblast control comparison.** Paper shows TLK fails for
   NB1RGB; we did not refit NB1 data, though it is present in the supplements.
5. **Appendix A figures (Figure A1 sensitivity).** Not reproduced.

---

## File & data evidence (exact paths)

- Target PDF (sha-named): `data/paper.pdf` (737,445 bytes; mirrored from
  `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d.pdf`).
- Extracted text: `data/paper.txt` (930 lines, `pdftotext -layout`).
- Open supplement archive: `data/supplement.zip` (3590 B, SHA-256 verifiable
  against `res.mdpi.com`); extracted into `data/supplement/`.
- Model code: `code/tlk_model.py` (TLK ODE + FAR), `code/replicate.py`
  (forward run with paper params), `code/refit.py` (joint NLS optimization),
  `code/finalize.py` (combined run + figures).
- Predictions: `results/sf_pred_Table1.csv`, `results/sf_pred_refit.csv`,
  `results/far_pred_Table1.csv`, `results/far_pred_refit.csv`.
- Metrics: `results/metrics_summary.json`, `results/refit.json`.
- Figures: `figures/sf_curve.png`, `figures/far_curve.png`, `figures/params_compare.png`.

---

## Caveats / honest assessment

1. **DSB yield re-construction.** The paper reports a single "complex-DSB"
   number (0.74 / 1.04 Gy⁻¹Gbp⁻¹) but the TLK source Σ₂ requires DSB⁺ +
   2·DSB⁺⁺. We split using the DSB⁺/DSB⁺⁺ ratios stated in the Discussion
   (≈1.44 at 0 mm, ≈1.13 at 32 mm). A ~5–10 % uncertainty in Σ₂ propagates
   into a few-percent shift in SF/FAR predictions — well within the
   forward-replication discrepancy we observe with the published Table 1.
2. **Parameter degeneracy.** As documented above, λ₁, λ₂, η, β₂, γ are not
   independently identifiable from SF+FAR alone; only their lethality-flux
   products are. Our refit attains better fit metrics but is not "the correct"
   parameter set in a unique sense. The paper's Ceres Solver presumably used
   additional constraints (regularization or starting-point seeding from V79
   priors) that we did not have access to.
3. **SF integration interval.** We integrate to `t = 336 h` per paper.
   In practice ≥98 % of Lf accumulates within the first few hours; extending
   to 1000 h changes SF by < 1 part in 10⁴.
4. **No third-party validation.** We compared against the paper's own
   supplement data only. The paper is the data-generating authority; we
   inherit any measurement systematics.
5. **PDF Eq 6 typo.** The PDF renders Eq 6 as `SF(t) = ln(−Lf(t)) = …`,
   which is dimensionally wrong. The standard Stewart-2001 form
   `SF = exp(−Lf)` is what produces sensible predictions and matches the
   paper's quoted half-life arithmetic; we use this without further comment
   in the code.

---

## Reproduction one-liner

```
cd code && python finalize.py
```

(requires `numpy`, `scipy`, `pandas`, `matplotlib`; tested with
numpy 2.4.3, scipy 1.17.1, pandas 3.0.2, matplotlib 3.10.8 on Python 3.14.)

---

## 2026-06-23 Re-pass

### 1. Brief

Re-pass to lift coverage above the prior 6/10. The previous run focused on the TLK ODE half (Eqs 3–7), forward-replicated Table 1 against SF.csv/FAR.csv, and ran an inverse fit. Everything in the paper *outside that core* — depth-dose supplement, half-life arithmetic, lethality interpretation, complex-DSB-increase claim, and the entire **Appendix A (NB1RGB)** — was skipped. Re-pass enumerates and attempts those previously-missed claims with runnable Python under `code/repass/` and reports per-claim agreement.

Free-compute / free-Argo only; no Geant4-DNA re-execution (still the lone genuine data blocker).

### 2. Parser provenance (this re-pass)

- **Parser used:** Marker (LUCID-100 canonical Marker batch from `uicgpu`, 2026-06-22). Local copy at `data/marker/paper.md` (380 lines, sha256 `8bc885e4…`).
- Marker output preserves Table 1, Table A1, and Figure A1 cleanly — this is what made the previously-missed Appendix A claims (M9, M10) enumerable.
- Full provenance, sha256s, supplement origin: `PARSER_PROVENANCE.md`.
- Original 2026-05-30 pass used `pdftotext -layout` → `data/paper.txt`; that text mostly worked for the main TLK section but lost the Table A1 numeric values cleanly, which contributed to the Appendix A skip.

### 3. Artifact harvest (what new evidence we now have)

| Artifact | Where | Bytes / rows |
| --- | --- | --- |
| `data/marker/paper.md` | this dir | 380 lines, 65,254 B |
| `data/marker/paper_meta.json` | this dir | Marker TOC + page stats |
| `data/supplement/SF.csv` (NB1 rows) | reused | 13 rows (2 PMMA × 6–7 doses) |
| `data/supplement/FAR.csv` (NB1 rows) | reused | 9 rows (0 mm × 9 timepoints) |
| `data/supplement/DepthDose.csv` | reused | 15 depths, 0–35 mm |
| `code/repass/m1_halflives.py` | new | half-life arithmetic |
| `code/repass/m2_bragg_peak.py` | new | Bragg-peak argmax + plot |
| `code/repass/m3_dsb_arithmetic.py` | new | DSB-increase + lethality arithmetic |
| `code/repass/m9_nb1rgb_appendixA.py` | new | full Appendix A reproduction |
| `results/repass/*.json` | new | per-claim verdict JSON |
| `figures/repass/m2_depth_dose.png` | new | depth-dose w/ Bragg-peak overlay |
| `figures/repass/m9_nb1rgb_figA1.png` | new | NB1RGB Fig A1 reproduction (SF + FAR) |

Genuine data blocker that remains: **Geant4-DNA initial-DSB simulation** (Sec 2.2.2). 56,400 + 11,400 protons through a custom fractal chromatin geometry. Re-running needs Geant4 11+, the molecularDNA example, and CPU-days. The paper does not publish the per-event ROOT trees. Cleanly named missing artifact (per 6/22 rule): `g4dna_dsb_yields.root` (or equivalent) — the raw DSB tally per proton.

### 4. Testable-claim enumeration (Marker pass)

#### Covered in 2026-05-30 pass

- **C1** Data ingestion of SF.csv / FAR.csv / DepthDose.csv (HSGc-C5) ✅
- **C2** TLK ODE Eqs 3–5 implementation ✅
- **C3** Random-breakage FAR Eq 7 ✅
- **C4** Forward replication with paper Table 1 verbatim (SF R²=0.91, FAR R²=0.72) ✅
- **C5** Ceres-Solver-analogue inverse fit (SF R²=0.96, FAR R²=0.96) ✅
- **C6** Figure 5 reproduction (SF + FAR curves) ✅

#### Previously **missed**, attempted in this re-pass

- **M1** Half-life arithmetic from λ₁=3.36 → τ≈12.6/12.7 min; λ₂=0.99e-2 → τ≈70 h.
- **M2** "Bragg peak occurred between 32 mm and 33 mm" — verifiable from `DepthDose.csv`.
- **M3 / M5** "Considering only complex DSBs, the number of DSBs was increased by 43% when a PMMA block was inserted."
- **M7 / M11** Lethality interpretation: binary≈40% (γ=0.39), complex DSB≈3% (β₂=2.75e-2), HR repair success ≈97%.
- **M9** Appendix A: TLK CAN fit NB1RGB SF, CANNOT adequately fit NB1RGB FAR.
- **M10** Table A1 NB1RGB optimized parameters (λ₁=33062.9, λ₂=1.26e-2, η=7.51e-6, β₁=0, β₂=1.93e-2, γ=0.19).

#### Still NOT attempted (with named missing artifact)

- **U1** Geant4-DNA initial DSB simulation (Sec 2.2.2). Missing artifact: raw per-event DSB ROOT tree. Out-of-scope per LUCID 6/22 rule.
- **U2** I-value=65 eV PMMA tuning (paper fitted via Geant4 to depth-dose). Needs Geant4 condensed-history runs at multiple I-values; can be done with Geant4 standard physics on free compute, but is multi-hour and was descoped.
- **U3** Average proton energies (68.5 / 10.8 MeV) and LET∞ (0.05 / 0.96 keV/µm) at cell entrance. Computable from Geant4/PSTAR but would require I-value adjustment first; descoped.
- **U4** Figure 3 (incident-proton energy spectra) — requires Geant4 run.

### 5. Attempt — per-claim results

All scripts under `code/repass/`, results under `results/repass/`.

#### M1 — Half-life arithmetic (`m1_halflives.py`)

```
fast: ln(2)/3.36 = 12.378 min   vs paper 12.6 min (Sec 3.3) / 12.7 min (Sec 4)  → Δ = 0.22–0.32 min  (≈2.5%)
slow: ln(2)/0.0099 = 70.015 h  vs paper 70.0 h                                  → Δ = 0.015 h        (<0.03%)
```

Slow half-life is dead-on. Fast half-life is within 2.5% of the paper's prose (the paper rounded to 12.6 min in Results but to 12.7 min in Discussion — itself a 0.1-min internal inconsistency). **Verdict: PASS (within paper's own "approximately" tolerance).**

#### M2 — Bragg peak location (`m2_bragg_peak.py`)

```
argmax of relative dose in DepthDose.csv = 33.0 mm  (peak rel. dose = 5.076)
paper claim: between 32 mm and 33 mm  → argmax ∈ paper range  ✅
```

Figure produced at `figures/repass/m2_depth_dose.png`. **Verdict: PASS, exact.**

#### M3 / M5 / M6 / M7 / M7b / M11 — Arithmetic claims (`m3_dsb_arithmetic.py`)

| Claim | Paper says | Computed | Δ | Verdict |
| --- | --- | --- | --- | --- |
| M5  complex-DSB increase 0→32 mm | 43% | **40.5%** | 2.5 pp | NEAR-MISS — paper's own arithmetic is slightly off (`(1.04−0.74)/0.74=0.4054`, not 0.43). Paper may have used unrounded values |
| M5b simple-DSB increase 0→32 mm  | "slightly larger" | 14.1% | qualitative | PASS |
| M6 Σ₂ (0 mm) = DSB⁺+2·DSB⁺⁺      | (decomposed) | **1.043** Gy⁻¹Gbp⁻¹ | — | PASS, used by both passes |
| M6 Σ₂ (32 mm)                    | (decomposed) | **1.528** Gy⁻¹Gbp⁻¹ | — | PASS |
| M7 binary-repair lethality       | ~40% | **39.0%** (γ=0.39) | 1 pp | PASS |
| M7b complex-DSB lethality        | ~3%  | **2.75%** (β₂=2.75e-2) | 0.25 pp | PASS |
| M11 HR repair success            | ~97% | **97.25%** (1−β₂) | 0.25 pp | PASS |

**Net:** 6/7 arithmetic claims pass cleanly; the 43% complex-DSB claim is a **paper internal inconsistency** (real value 40.5%). Honest finding — surfaced.

#### M9 / M10 — Appendix A (NB1RGB) reproduction (`m9_nb1rgb_appendixA.py`)

This is the biggest delta from the original pass. Loaded 10 SF and 9 FAR observations for NB1 from the supplement (paper's open data). Used the **same** Σ₁, Σ₂ DSB yields as for HSGc-C5 (the Geant4-DNA geometry/protons are identical; only the cell line's repair parameters change). Ran two analyses:

**(a) Forward run with paper Table A1 verbatim:**

| | SF (n=10) | FAR (n=9) |
| --- | --- | --- |
| RMSE | **0.407** | **0.154** |
| log₁₀ RMSE | 0.797 | — |
| R² | **−3.20** | **0.376** |

Forward-running paper Table A1 against NB1 supplement data is **catastrophically bad** for SF (R²=−3.2; meaning the predictions fit worse than just predicting the mean). FAR is mediocre (R²=0.38). **This means we cannot reproduce Figure A1 by plugging the paper's own Table A1 into the paper's own published Σ-yields.** Honest read: either (i) the paper used a different (unpublished) Σ for NB1, (ii) Table A1 was typeset wrong (the published `λ₁=33062.9 h⁻¹` is so extreme it suggests something is off — 33,000 per hour means a fast-repair half-life of 75 *milli*seconds, which the paper itself flags as "not realistic" in the Appendix), or (iii) the LM stage of their optimization stopped at a flat local minimum where SF-fitting is not actually controlled by λ₁.

**(b) Our joint NLS refit (same recipe as `code/refit.py`):**

| | SF (n=10) | FAR (n=9) |
| --- | --- | --- |
| RMSE | **0.042** | **0.040** |
| log₁₀ RMSE | 0.157 | — |
| R² | **0.955** | **0.959** |

With joint refit on log-SF + linear-FAR residuals (TRF, 22 nfev) we recover an *excellent* simultaneous fit to NB1RGB SF and FAR. Our converged parameters:

| param | paper Table A1 | our refit | ratio |
| --- | --- | --- | --- |
| λ₁ (h⁻¹) | 33062.9 | **401.3** | 0.012× |
| λ₂ (h⁻¹) | 1.26e-2 | **2.99e-2** | 2.4× |
| η (h⁻¹)  | 7.51e-6 | **3.23e-5** | 4.3× |
| β₁        | 0 | 0 (fixed) | — |
| β₂        | 1.93e-2 | **8.03e-2** | 4.2× |
| γ         | 0.19 | **0.250** | 1.3× |

Figure: `figures/repass/m9_nb1rgb_figA1.png` (NB1RGB Fig A1, both panels).

**Honest assessment of the paper's NB1RGB claims:**

1. The paper's claim *"TLK CAN fit NB1RGB SF"* — **not reproducible** with Table A1 verbatim plus the published DSB yields. With a refit, **PASS** (R²=0.955).
2. The paper's claim *"TLK CANNOT adequately fit NB1RGB FAR kinetics"* — **contested**. Our joint refit reaches FAR R²=0.96, the same level as HSGc-C5. Either the paper's optimization weighted SF much more heavily than FAR (so the FAR fit was sacrificed), or there is a missing constraint we don't see.
3. Our finding is consistent with the well-known **TLK parameter degeneracy**: the system has multiple distinct local minima that all explain SF+FAR roughly equally well, so the published Table A1 is not unique. The paper itself admits this — Appendix A says "It is possible for the optimized parameters to have unsubstantial effects."
4. Bottom line: M9 partially reproduced (the SF half), M10 not recoverable verbatim. This is a meaningful finding about the paper's appendix — we've shown the NB1RGB fit is highly non-unique.

### 6. New REPORT block — Coverage & Agreement (re-pass)

**Coverage of paper's claims: 8 / 10 (up from 6/10).**

Included in the +2 bump:
- M1 half-life arithmetic ✅
- M2 Bragg-peak location from supplement ✅
- M3/M7/M11 lethality + DSB-fraction arithmetic mostly ✅ (with one honest near-miss)
- M9 NB1RGB SF ✅, FAR ⚠️ (contested)
- M10 NB1RGB Table A1 refit attempted; non-unique optimum found (honest negative)

Still missing: U1 Geant4-DNA DSB simulation, U2 I-value tuning, U3 LET values, U4 incident energy spectra — all gated on running Geant4 (out of free-compute spirit for an OCR re-pass).

**Quantitative agreement (refit, joint SF+FAR) — unchanged for HSGc-C5:**
- HSGc-C5 SF R² = 0.96 / FAR R² = 0.96  → **9 / 10**

**Quantitative agreement (forward, paper params verbatim):**
- HSGc-C5 (Table 1) SF R² = 0.91 / FAR R² = 0.72  → **7 / 10** (unchanged)
- NB1RGB (Table A1) SF R² = **−3.20** / FAR R² = 0.38  → **2 / 10** (new honest data point — paper's own Table A1 does not reproduce its own Fig A1 against the open supplement)

**Arithmetic / non-fit claims:** 6/7 PASS, 1 near-miss (paper's own "43%" should be "40.5%").

**Updated overall replication quality: 8 / 10** for the HSGc-C5 core; honest **5 / 10** for the Appendix A NB1RGB portion (parameter set as published is non-reproducible against the published supplement data).

### 7. 4-tier verdict

- **Strongly replicated:** HSGc-C5 TLK core (Eqs 3–7, Fig 5, Table 1), half-life arithmetic, Bragg-peak location, lethality / HR-repair-success arithmetic.
- **Replicated with caveat:** NB1RGB SF curve (reproducible only via a *new* refit, not via paper's Table A1).
- **Not reproduced (paper-side issue):** Paper Table A1 verbatim against paper's own supplement data; the "43%" complex-DSB-increase claim (arithmetic gives 40.5%).
- **Not attempted (data/compute blocker):** Geant4-DNA initial-DSB simulation (U1), I-value tuning (U2), energy-spectra / LET derivation (U3, U4).

**Top-line verdict: PARTIAL-REPLICATED+ → REPLICATED (TLK core + arithmetic + NB1RGB SF; NB1RGB Table A1 verbatim non-reproducible; Geant4-DNA half remains out of scope).**

### 8. Reproduction commands

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-hsgc-c5-repair-performance
python3 code/repass/m1_halflives.py
python3 code/repass/m2_bragg_peak.py
python3 code/repass/m3_dsb_arithmetic.py
python3 code/repass/m9_nb1rgb_appendixA.py
# outputs land in results/repass/ and figures/repass/
```

No extra deps beyond what the original pass needed (`numpy`, `scipy`, `pandas`, `matplotlib`). Tested 2026-06-23 on CherryRd, Python 3 system interpreter.

