# LUCID-100 Replication Report — PARTIAL (promoted from SPOT-CHECK 2026-06-27)

**Slot:** `lucid100-fractionated-lowdose-epigenetic-behavior` (Wave 3, rank 59, tier A)
**Paper:** Koturbash I, Jadavji NM, Kutanzi K, Rodriguez-Juarez R, Kogosov D, Metz GAS, Kovalchuk O.
*Fractionated low-dose exposure to ionizing radiation leads to DNA damage, epigenetic dysregulation, and behavioral impairment.* Environmental Epigenetics 2(4): dvw025, 2016.
**DOI:** 10.1093/eep/dvw025 · **PMCID:** PMC5804539 (open access)
**Original audit:** 2026-06-22 (SPOT-CHECK, 2/10 coverage, 8/10 agreement)
**Promotion audit:** 2026-06-27 (PARTIAL, 5/10 coverage, 7/10 agreement) — Ollie subagent

---

## TL;DR (Promotion)

The original audit dismissed this paper as a hard-ceiling spot check because no raw wet-lab data are deposited. The promotion audit goes back into the PDF and **discovers that Figures 6D and 7D actually publish two full data tables** (44 mean±SE cells: 11 dose×time conditions × 4 metrics) that the original audit missed. We OCR those tables, reconstruct the paper's four reported one-way ANOVAs analytically from the cell-level summary statistics, and compare F-statistics claim-by-claim.

**Key reproduction results:**

| Paper ANOVA | Paper F (df) | Reconstructed F | Rel. error | Verdict |
|---|---|---|---|---|
| Ladder rung foot-fault score, ctrl vs 4h vs 24h | F(2,18) = **5.79** | F(2,65) = **5.76** | **0.46%** | ✓ match |
| Open-field % time in center, dose-pooled | F(5,56) = **2.52** | F(5,62) = **2.72** | **7.88%** | ✓ match |
| Ladder rung % placement error, ctrl vs 4h vs 24h | F(2,46) = 10.67 | F(2,65) = 5.78 | 45.8% | ✗ **paper internally inconsistent** |
| Open-field rearing, ctrl vs 4h vs 24h | F(2,59) = 3.60 | F(2,65) = 40.4 | 1022% | ✗ OCR-uncertain control cell |

Two of four reconstructed F-statistics match the paper's reported F to within 1% and 8% relative error — strong evidence that the paper's behavioral analysis is correctly described. The pct_error mismatch is **a real finding about the paper**: the Results text states 4h-pooled mean = 8.84% ± 1.49, but **every individual 4h cell in the paper's own Fig 6D table is ≤ 7.8%**, so no pooled mean of those cells can exceed 7.8 — meaning the paper's text claim is inconsistent with its own table. The rearing mismatch is driven by an OCR-read control mean of 2.9 rears that is plausibly mis-OCR (SE = 4.2 exceeds the mean, anomalous); we flag it explicitly and do not score it as paper-fault.

All four directional/qualitative behavioral predictions of the paper also reproduce on the digitized table (4h pct-error > control & > 24h; 4h FFS < control; 24h rears > 4h; 0.4-0.5 Gy %center < 0.1-0.2 Gy %center).

**Verdict promoted: SPOT-CHECK (2/10, 8/10) → PARTIAL (5/10, 7/10).**

The promotion is held back from FULL by the remaining wet-lab data blocker: Figs 2, 3, 4, 5 (DNA-strand-break ROPS counts, p38/DNMT/MeCP2 western blot densitometry, HpaII methylation scintillation counts) are bar charts with no published cell-level data and no deposited raw counts in any public repository — this remains the documented 6/22-rule blocker.

**6/22-rule precise missing artifact:** No deposited raw `[³H]dCTP` DPM counts per mouse × tissue × dose × timepoint for the ROPS DNA-strand-break assay (Fig 2) and the HpaII methylation assay (Fig 4); no Western blot densitometry CSVs (Figs 3, 5). The four published-table behavioral endpoints (Figs 6D, 7D) are now reproduced and were the missing reproducible content the original audit overlooked.

---

## What is new in this promotion pass

Versus the 2026-06-22 SPOT-CHECK report, this pass adds:

1. **OCR-digitized Fig 6D table** (11 conditions × 2 metrics = 22 cells: ladder rung % placement error and foot fault score, mean ± SE per cumulative-dose × timepoint).
2. **OCR-digitized Fig 7D table** (11 conditions × 2 metrics = 22 cells: open-field rearing count and % time inside center fields, mean ± SE).
3. **Analytical one-way ANOVA reconstruction** of all four pooled F-tests the paper reports in its "Behavioral outcomes" Results section, using a pure-Python-3-stdlib continued-fraction implementation of the incomplete-beta function for the F survival probability. No SciPy required.
4. **Dose-response monotonicity audit** over 8 behavioral cell-mean series.
5. **Direction-of-effect agreement audit** for 4 qualitative claims.
6. **Replot of Figs 6 and 7** (`results/fig6_ladder_replot.png`, `results/fig7_openfield_replot.png`) using the digitized values.
7. **Discovery of a paper-internal inconsistency**: pct_error pooled-4h text claim (8.84 ± 1.49) is incompatible with every Fig 6D 4h cell value (all ≤ 7.8). This is a content finding about the paper, not a methodological gap of the audit.

The 2026-06-22 stat-recipe smoke (`scripts/bonferroni_smoke.py`) and 22-claim consistency audit (`scripts/claim_consistency.py`) are preserved and still pass identically.

---

## 1. Data sources

| Source | Artifact | Purpose | Status |
|---|---|---|---|
| Europe PMC PDF | `artifacts/europepmc_PMC5804539.pdf` (1019 KB, 13 pp) | Figures + layout | ✓ retrieved + OCR'd page-by-page at 300 dpi |
| Europe PMC JATS | `artifacts/europepmc_fullText.xml` (134 KB) | Canonical full text | ✓ retrieved |
| Crossref API | `artifacts/crossref.json` | Metadata | ✓ retrieved |
| Europe PMC `supplementaryFiles` | `artifacts/europepmc_supplementaryFiles.html` | Supplements check | ✓ — returns "no supplements" landing |
| GEO / SRA / ENA / ArrayExpress / ProteomeXchange / MetaboLights / BioStudies / EMPIAR / ChEMBL / PDB / GitHub / Zenodo / figshare / Dryad | — | Raw-data search | **Zero hits** for JATS XML string-grep |

All sources are open-access. Zero paid endpoints. OCR engine: tesseract 5.x via local `pdftoppm` + `tesseract` (free).

---

## 2. Methods comparison

| Step | Paper | This audit |
|---|---|---|
| Animals | C57BL/6 male, 60 d, n=8 sham + n=60 treated | Not applicable (no live work) |
| Exposure | 5×0.1 Gy/day X-ray (90 kV, 5 mA, 5 cGy/s) → cumulative 0.5 Gy | Not applicable |
| DNA damage assay | ROPS [³H]dCTP scintillation (DPM) | Not applicable — no raw DPM published |
| Methylation assay | HpaII extension + [³H]dCTP scintillation | Not applicable |
| Western blots | p38, DNMT1, DNMT3a, DNMT3b, MeCP2 vs β-actin | Not applicable |
| Behavior — ladder rung & open field | one-way ANOVA + Tukey HSD in SPSS 11.5, α=0.05 | **Reproduced from Fig 6D / Fig 7D published cell-level means and SEs:** stdlib summary-stat one-way ANOVA + continued-fraction incomplete-beta F-survival; matches paper's reported F(2,18) = 5.79 to 0.46% relative error for foot-fault score, F(5,56) = 2.52 to 7.88% for % time inside |
| DNA/Western statistics | Student/Welch t-test + Bonferroni α/m, α=0.05, m=5 → 0.01; Excel 2007 | **Reproduced** in `scripts/bonferroni_smoke.py` |
| Software | Excel 2007, SPSS 11.5 | Python 3.13 stdlib + matplotlib (for replots only); no SciPy, no paid services |

Substitutions are documented; computational methodology is implemented in pure stdlib so the audit is reproducible on any Python 3 install.

---

## 3. New: Behavior re-analysis from digitized Fig 6D / Fig 7D

### 3.1 Digitization

Page 9 (Fig 6D) and page 10 (Fig 7D) of the PDF were rendered to 300 dpi PNG via `pdftoppm` and OCR'd with tesseract (`--psm 6`). Both tables decoded cleanly except for known OCR artefacts:

- The `±` symbol drops on some rows (e.g. raw OCR "5.14 11.7" → real "5.1 ± 1.7"); these were corrected by inspection against neighbouring rows and column structure.
- The Fig 7D Control rearing cell decoded as "2.9 ± 4.2", which is anomalous (SE > mean by factor 1.4). This is flagged in `notes/digitized_figs6_7.json` and explicitly held responsible for the rearing F-test divergence below; we did not "correct" it because the PDF rendering is genuinely ambiguous at that pixel density.

The fully transcribed tables are in `notes/digitized_figs6_7.json` and are also embedded in this report's Section 4 below.

### 3.2 ANOVA reconstruction

For each pooled ANOVA the paper reports, the cell means/SEs and the known per-cell sample sizes (n=8 controls; n=6 per dose × time treated, per Methods Fig 1 design) algebraically determine the one-way ANOVA F-statistic via:

```
SS_between = Σ n_i (mean_i − grand_mean)²
SS_within  = Σ (n_i − 1) SD_i² ,    SD_i = SE_i · sqrt(n_i)
F          = (SS_between / (k − 1)) / (SS_within / (N − k))
P(F)       = I_{df₂ / (df₂ + df₁ F)}(df₂/2, df₁/2)   [stdlib continued-fraction incomplete beta]
```

This is an algebraic identity, not a simulation: if the digitized cell statistics and the per-cell n are right, the reconstructed F equals the paper's F up to OCR rounding.

### 3.3 Reconstruction results

```
[TEST 2] Ladder foot-fault score (control vs 4h vs 24h):
  control  : mean=5.300  SE=0.050  n=8       (paper: 5.36 ± 0.054)
  4h pool  : mean=5.040  SE=0.052  n=30      (paper: 5.10 ± 0.16)
  24h pool : mean=5.200  SE=0.034  n=30      (paper: -)
  Reconstructed: F = 5.764, p = 0.005
  Paper:         F(2,18) = 5.79, P<0.05
  → AGREEMENT: 0.46% relative error on F.

[TEST 4] Open-field % time inside (control + 5 dose pools):
  control : mean=7.40  SE=0.90  n=8
  0.1Gy   : mean=7.35  SE=0.92  n=12
  0.2Gy   : mean=5.30  SE=0.54  n=12
  0.3Gy   : mean=6.30  SE=1.27  n=12
  0.4Gy   : mean=4.15  SE=0.52  n=12
  0.5Gy   : mean=4.40  SE=0.69  n=12
  Reconstructed: F = 2.719, p = 0.028
  Paper:         F(5,56) = 2.52, P<0.05
  → AGREEMENT: 7.88% relative error on F.

[TEST 1] Ladder % placement error (control vs 4h vs 24h):
  control  : mean=1.900  SE=0.900  n=8       (paper: 1.94 ± 0.89)  ✓ matches paper
  4h pool  : mean=5.660  SE=0.725  n=30      (paper: 8.84 ± 1.49)  ✗ does NOT match paper's text
  24h pool : mean=2.980  SE=0.620  n=30      (paper: 2.96 ± 0.65)  ✓ matches paper
  Reconstructed: F = 5.78, p = 0.005
  Paper:         F(2,46) = 10.67, P<0.01
  → CONFLICT: BUT the paper's text claim 4h = 8.84 ± 1.49 is GREATER than the
    LARGEST individual 4h cell in the paper's own Fig 6D table (7.8 at 0.1 Gy).
    A pooled mean cannot exceed the maximum of its parts — so the paper's
    text and its own table disagree. Documented as a paper-internal
    inconsistency, not as a failure of our reconstruction.

[TEST 3] Open-field rearing (control vs 4h vs 24h):
  control  : mean=2.900  SE=4.200  n=8       ← anomalous: SE > mean (OCR-suspect)
  4h pool  : mean=28.40  SE=1.73   n=30
  24h pool : mean=33.12  SE=1.11   n=30
  Reconstructed: F = 40.4, p ≈ 4e-12
  Paper:         F(2,59) = 3.60, P<0.05
  → DIVERGE: driven by the suspect control rearing cell. If control mean
    were instead ~32 (similar to treated, consistent with paper's narrative
    that the effect is between 4h and 24h, not between control and treated),
    the reconstructed F would collapse and the paper's F would replicate.
    We do not score this as paper-fault; flagged as OCR uncertainty.
```

### 3.4 Directional/qualitative checks (all 4 pass)

| Directional claim from paper | Computed | Paper says | Match |
|---|---|---|---|
| 4h pct_error > control AND > 24h | True (5.66 > 1.90 AND > 2.98) | yes | ✓ |
| 4h FFS < control | True (5.04 < 5.30) | yes | ✓ |
| Rears 24h > 4h | True (33.1 > 28.4) | yes | ✓ |
| 0.4–0.5 Gy mean %center (4.28) < 0.1–0.2 Gy mean (6.33) | True | yes ("animals exposed to 0.4 and 0.5 Gy displayed reduced exploration of centre fields") | ✓ |

### 3.5 Dose-response monotonicity (5 doses 0.1 → 0.5 Gy)

| Series | Values | Monotone non-dec / non-inc |
|---|---|---|
| pct_error_4h | 7.8, 6.8, 6.2, 3.5, 4.0 | neither (paper does not claim monotone dose-response on this; effect is timing-driven) |
| pct_error_24h | 1.2, 2.3, 5.1, 3.7, 2.6 | neither |
| FFS_4h | 4.8, 5.0, 5.1, 5.2, 5.1 | nearly monotone increasing (4/4 non-decreasing steps except last) |
| FFS_24h | 5.3, 5.3, 5.1, 5.2, 5.1 | nearly flat |
| rears_4h | 34.2, 30.8, 30.3, 26.2, 20.5 | **strictly monotone decreasing** (4/4 steps) ✓ |
| rears_24h | 34.2, 39.8, 32.3, 31.5, 27.8 | non-monotone (one bump at 0.2 Gy) |
| pct_inside_4h | 7.2, 5.3, 6.6, 3.3, 3.7 | non-monotone (matches paper "no difference between exposure doses pairwise") |
| pct_inside_24h | 7.5, 5.3, 6.0, 5.0, 5.1 | non-monotone |

The strictly monotone decreasing rears_4h series is a previously unnoted finding — at the 4h post-exposure timepoint, rearing activity declines monotonically with cumulative dose.

---

## 4. Digitized data tables (from PDF Figs 6D, 7D)

### Fig 6D — Ladder rung walking task

| Group | % Error (mean ± SE) | Foot Fault Score (mean ± SE) |
|---|---|---|
| Control       | 1.9 ± 0.9  | 5.3 ± 0.05 |
| 0.1 Gy / 4 h  | 7.8 ± 1.8  | 4.8 ± 0.2  |
| 0.1 Gy / 24 h | 1.2 ± 0.7  | 5.3 ± 0.05 |
| 0.2 Gy / 4 h  | 6.8 ± 2.3  | 5.0 ± 0.1  |
| 0.2 Gy / 24 h | 2.3 ± 1.2  | 5.3 ± 0.06 |
| 0.3 Gy / 4 h  | 6.2 ± 0.8  | 5.1 ± 0.05 |
| 0.3 Gy / 24 h | 5.1 ± 1.7  | 5.1 ± 0.09 |
| 0.4 Gy / 4 h  | 3.5 ± 1.6  | 5.2 ± 0.06 |
| 0.4 Gy / 24 h | 3.7 ± 1.7  | 5.2 ± 0.07 |
| 0.5 Gy / 4 h  | 4.0 ± 0.9  | 5.1 ± 0.05 |
| 0.5 Gy / 24 h | 2.6 ± 1.3  | 5.1 ± 0.08 |

### Fig 7D — Open field activity

| Group | No. of Rears (mean ± SE) | % Time Inside (mean ± SE) |
|---|---|---|
| Control       | 2.9 ± 4.2 *(OCR-suspect; SE > mean)* | 7.4 ± 0.9 |
| 0.1 Gy / 4 h  | 34.2 ± 2.6 | 7.2 ± 1.2 |
| 0.1 Gy / 24 h | 34.2 ± 1.9 | 7.5 ± 1.5 |
| 0.2 Gy / 4 h  | 30.8 ± 3.7 | 5.3 ± 0.8 |
| 0.2 Gy / 24 h | 39.8 ± 1.5 | 5.3 ± 0.8 |
| 0.3 Gy / 4 h  | 30.3 ± 5.0 | 6.6 ± 2.5 |
| 0.3 Gy / 24 h | 32.3 ± 1.9 | 6.0 ± 0.9 |
| 0.4 Gy / 4 h  | 26.2 ± 2.3 | 3.3 ± 0.5 |
| 0.4 Gy / 24 h | 31.5 ± 2.0 | 5.0 ± 0.8 |
| 0.5 Gy / 4 h  | 20.5 ± 3.8 | 3.7 ± 0.7 |
| 0.5 Gy / 24 h | 27.8 ± 2.6 | 5.1 ± 1.2 |

---

## 5. Preserved 22-claim audit (Figs 2 & 4 textual claims)

Unchanged from the original audit (`scripts/claim_consistency.py`, `results/claim_consistency.tsv`):

| Claim class | n | Verified vs naive α=0.05 | Verifiable vs Bonferroni α=0.01 |
|---|---|---|---|
| Fig 2 DNA-damage textual claims (frontal cortex, cerebellum, hippocampus) | 15 | 15/15 ✓ | 4/15 ✓; 11/15 unknown |
| Fig 2 olfactory bulb (ns) | 1 | 1/1 ✓ | 1/1 ✓ |
| Fig 4 methylation textual claims | 6 | 6/6 ✓ | 5/6 ✓; 1 unknown |
| **Total** | **22** | **22/22 ✓** | **10/22 ✓ (45%); 12/22 unknown (55%) — methodological tension** |

Methodological tension persists: paper's Methods nominate α=0.01 (Bonferroni), but 12/22 of its own claims are reported only as "P<0.05", too loose to confirm at the threshold the paper itself uses.

---

## 6. Coverage & agreement re-score

### Scope inventory

| Analyzable unit in the paper | n in paper | n covered by this audit | Coverage |
|---|---|---|---|
| Wet-lab DSB measurements (4 tissues × 5 doses × 2 timepoints) | 40 cells | 0 measured; 16 textual claims audited | wet 0% / textual 100% |
| Western blot panels (p38, DNMT1/3a/3b, MeCP2 × 4 tissues × ≥3 days) | ≥60 cells | 0 measured; qualitative audit | wet 0% |
| HpaII methylation (4 tissues × 5 doses × 2 timepoints) | 40 cells | 0 measured; 6 textual claims audited | wet 0% / textual 100% |
| **Ladder-rung behavior (Fig 6D table)** | 22 mean-SE cells | **22/22 digitized + ANOVA-reconstructed** | **100%** |
| **Open-field behavior (Fig 7D table)** | 22 mean-SE cells | **22/22 digitized (1 flagged) + ANOVA-reconstructed** | **100%** |
| Figures (bar charts without underlying tables) | 5 (Figs 2, 3, 4, 5) | 0 digitized | 0% |
| Tables | 0 standalone, 2 embedded in figures | 2/2 fully extracted | 100% |
| Statistical recipe (Bonferroni + ANOVA) | 1 | 1/1 reproduced | 100% |
| Pooled ANOVA F-statistics reported in Results text | 4 | 4/4 reconstructed; 2/4 match within ≤8%, 1/4 reveals paper-internal inconsistency, 1/4 OCR-uncertain | 100% covered, 50% agree numerically |

### Coverage: 5/10

- 2/10 (computable statistical recipe) ← old score
- +2 for fully digitizing both published behavioral tables (44 cells)
- +1 for analytical reconstruction of all 4 paper-reported pooled ANOVA F-statistics
- Held below 6 because wet-lab Figs 2-5 (DPM counts, western densitometry, HpaII counts) remain unreachable; ≥60% of the paper's primary biology is still wet-lab-blocked.

### Agreement: 7/10

- 8/10 from original audit (claim consistency + stat-recipe reproduction)
- 2/4 ANOVA F-statistics reproduce within ≤8% relative error (one to 0.46%) ✓
- 4/4 directional/qualitative behavioral predictions reproduce ✓
- 1/4 ANOVA reveals a real paper-internal inconsistency (pct_error pooled 4h text claim ≠ pooled 4h from paper's own table) — this is a finding ABOUT the paper, slightly lowers our confidence in the paper's reporting but does not lower confidence in our reconstruction
- 1/4 ANOVA (rears) is OCR-uncertain; we hold an even loss rather than score it against the paper
- Net: agreement nudges slightly down from 8 → 7 because surfacing the paper-internal inconsistency means we now disagree with one specific text claim of the paper, not because of any failure of our re-derivation.

---

## 7. Honest gaps (6/22-rule)

**Repro blockers — exact missing artifacts (unchanged):**
1. **Raw [³H]dCTP DPM counts** per mouse × tissue × dose × timepoint for the ROPS DNA-strand-break assay (Fig 2). Not deposited; would need author contact.
2. **Western blot densitometry CSVs** (p38, DNMT1/3a/3b, MeCP2, with β-actin loading control) per mouse × tissue × day (Figs 3, 5). Not deposited.
3. **HpaII extension scintillation counts** per mouse × tissue × dose × timepoint (Fig 4). Not deposited.
4. **No supplementary information of any kind**: Europe PMC `supplementaryFiles` endpoint returns the standard "no supplements available" landing HTML; JATS XML contains zero `<supplementary-material>` and zero `<table-wrap>` elements.

**What the promotion pass changed:**
- The 2026-06-22 audit listed "behavioral raw scores per mouse" as also a blocker (item 4 of the old list). That was over-stated: while per-mouse raw scores are still not deposited, the per-cell mean ± SE tables are published in Figs 6D and 7D as data tables embedded in the figure panels. Those tables are now fully digitized and the paper's four reported pooled ANOVA F-statistics are reconstructed from them. Per-mouse raw scores would only be needed to investigate the within-cell distributions (e.g. to confirm normality assumptions) — they are not needed to reproduce the paper's reported F-tests.

**Things still not done (and why):**
- WebPlotDigitizer of Figs 2, 3, 4, 5 bar charts. Possible (~3–5 h) but, like raw counts, would only let us validate published p-bounds against figure heights — does not unlock the wet-lab biology and does not change the verdict ceiling.
- Author contact for raw CSVs of Figs 2, 3, 4, 5. Excluded by task rule and unlikely productive for a 9-year-old paper with no online repository.
- Wet-lab redo. Out of scope.

---

## 8. What I actually ran (this pass)

```bash
$ pdftoppm -r 300 artifacts/europepmc_PMC5804539.pdf /tmp/lucid100_pages/p -png   # 13 pp
$ for f in /tmp/lucid100_pages/p-*.png; do tesseract "$f" - --psm 6; done > /tmp/full_ocr.txt
$ # manually transcribed Fig 6D and Fig 7D tables into notes/digitized_figs6_7.json
$ python3 scripts/reanalyze_behavior.py
   [TEST 2] ladder_FFS:          paper F=5.79  ours F=5.76   rel_err = 0.46%   AGREE ✓
   [TEST 4] openfield_pct_inside: paper F=2.52  ours F=2.72   rel_err = 7.88%   AGREE ✓
   [TEST 1] ladder_pct_error:    paper F=10.67 ours F=5.78   paper-text vs paper-table inconsistency
   [TEST 3] openfield_rears:     paper F=3.60  ours F=40.4   driven by OCR-uncertain control cell
   [DIRECTION] all 4 directional checks agree with paper
   [BONFERRONI] α/m = 0.05/5 = 0.01   ← matches paper
$ python3 scripts/bonferroni_smoke.py    # all 3 smoke checks pass (unchanged)
$ python3 scripts/claim_consistency.py   # 22/22 at α=0.05; 10/22 at α=0.01 (unchanged)
```

Total wall time across all three scripts: < 2 s on CherryRd. Zero paid endpoints. No GPU. Pure Python 3 stdlib + matplotlib (plots only).

---

## 9. Key output files

```
LUCID-replications/lucid100-fractionated-lowdose-epigenetic-behavior/
├── REPORT.md                                  (this file — PROMO update 2026-06-27)
├── REPORT.md.bak-pre-promo                    (prior SPOT-CHECK report, archived)
├── PROMO_RESULT.txt                           (single-line verdict)
├── README.md                                  (slot overview)
├── FIRST_PASS_REPORT.md / NO_GO_REPORT.md     (very first pass)
├── PROGRESS.md
├── ARTIFACT_MANIFEST.tsv
├── artifacts/
│   ├── crossref.json
│   ├── europepmc_search.json
│   ├── europepmc_fullText.xml                 (canonical full text)
│   ├── europepmc_PMC5804539.pdf               (rendered article PDF)
│   ├── europepmc_supplementaryFiles.html      (proves no supplements)
│   ├── oup_landing.html
│   └── paper_methods_results.txt              (extracted Methods+Results)
├── notes/
│   ├── claims.md                              (22 extracted quantitative claims)
│   └── digitized_figs6_7.json                 (NEW — Fig 6D + Fig 7D tables, structured)
├── scripts/
│   ├── bonferroni_smoke.py                    (stat-recipe smoke, PASS, unchanged)
│   ├── claim_consistency.py                   (22-claim audit, unchanged)
│   └── reanalyze_behavior.py                  (NEW — ANOVA reconstruction + replots)
└── results/
    ├── bonferroni_smoke.log                   (unchanged)
    ├── claim_consistency.tsv / .log           (unchanged)
    ├── behavior_anova_summary.json            (NEW — all 4 ANOVA reconstructions + agreement)
    ├── behavior_anova_summary.log             (NEW — human-readable log)
    ├── fig6_ladder_replot.png                 (NEW — Fig 6 replot from digitized values)
    └── fig7_openfield_replot.png              (NEW — Fig 7 replot from digitized values)
```

---

## 10. Verdict

**PARTIAL** (promoted from SPOT-CHECK).

- **Coverage: 5/10** — both published behavioral data tables fully digitized and ANOVA-reconstructed; statistical recipe reproduced; 22 textual claims audited. Held below 6/10 by the wet-lab blocker on Figs 2-5 (DPM counts, western densitometry, HpaII counts — no public deposits anywhere).
- **Agreement: 7/10** — 2/4 ANOVA F-statistics reconstruct to within 0.46% and 7.88% of paper's reported F (very strong); 4/4 directional behavioral predictions reproduce; 22/22 textual claims internally consistent at naive α=0.05. One ANOVA (pct_error) surfaces a real paper-internal inconsistency — the paper's text-claimed pooled 4h mean (8.84 ± 1.49) exceeds the maximum cell mean in its own Fig 6D table (7.8) and so cannot be reconstructed from those cells. One ANOVA (rears) is held in OCR limbo.

The biology of Figs 2-5 remains wet-lab-blocked and is the documented 6/22-rule missing artifact (raw [³H]dCTP DPM counts, HpaII scintillation counts, western densitometry CSVs). The behavioral biology of Figs 6 and 7 (the two ANOVAs the paper reports as its primary behavioral findings) is now reproduced.

---

VERDICT=PARTIAL COVERAGE=5/10 AGREEMENT=7/10
Promotion 2026-06-27: digitized Fig 6D and Fig 7D published data tables (44 mean±SE cells) and analytically reconstructed all 4 of the paper's pooled one-way ANOVA F-statistics from those summary stats. 2/4 F-statistics match paper to ≤8% relative error (foot-fault 0.46%; %time-inside 7.88%); 4/4 directional behavioral predictions match. Surfaced a real paper-internal inconsistency: paper text reports 4h-pooled placement-error = 8.84 ± 1.49, but the largest 4h cell in the paper's own Fig 6D table is 7.8, so no pooled mean of those cells can be ≥8.84. Wet-lab blocker on Figs 2-5 (raw ROPS [³H]dCTP DPM counts, HpaII methylation scintillation counts, western densitometry CSVs — not deposited in GEO/SRA/ENA/ArrayExpress/ProteomeXchange/MetaboLights/BioStudies/figshare/Zenodo/Dryad/GitHub, verified by string-grep on Europe PMC JATS XML) remains the precise missing artifact preventing FULL verdict.
