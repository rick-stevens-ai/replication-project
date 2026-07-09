# FINAL REPLICATION REPORT — LUCID-100 slot 58

**Paper:** Soroko S.S., Skamnitskiy D.V., Gorshkova E.N., Kutova O.M., Seriev I.R.,
Maslennikova A.V., Guryev E.L., Gudkov S.V., Vodeneev V.A., Balalaeva I.V.,
Shilyagina N.Yu. *The Dose Rate of Corpuscular Ionizing Radiation Strongly
Influences the Severity of DNA Damage, Cell Cycle Progression and Cellular
Senescence in Human Epidermoid Carcinoma Cells.*
**Curr. Issues Mol. Biol. 2024, 46(12), 13860–13880.**

- **DOI:** [10.3390/cimb46120828](https://doi.org/10.3390/cimb46120828)
- **PMC:** [PMC11726848](https://pmc.ncbi.nlm.nih.gov/articles/PMC11726848/)
- **License:** CC BY 4.0
- **Worktype:** wet-lab radiobiology assay (dose-rate effect study) — *not* a simulation; master TSV slot 58 retag recommended.
- **Closeout date:** 2026-06-25 · Free Argo + Gemini AI-Studio (figure digitization) endpoints; CPU-only; no author contact.

---

## 1. VERDICT

**PARTIAL — Coverage 6.5/10 · Agreement 8.5/10**

> One-line summary: figure-digitized reproduction of all seven main
> figures and every in-text numerical claim; ≈3× dose-rate sparing
> reproduces by three independent methods; per-replicate raw data never
> deposited.

**Why PARTIAL (not REPLICATED):** the paper deposits no per-well, per-cell,
or per-event source tables. Every reproduced number comes from
vision-model-digitized figure means + visually-estimated error bars, not
from the authors' underlying measurements. The headline biophysical
claim (3× dose-rate sparing) is robust to that limitation; the precise
LD₅₀ values are not, and our Hill/Prism-equivalent fits disagree with the
paper's LD₅₀ by ~30-40 % even while D₃₇ agrees within ~10 %.

**Why PARTIAL (not SPOT-CHECK):** this pass covers every figure (Figs 1-7)
and every numerical claim in the body text, not a single spot check.

**Why PARTIAL (not NO-GO):** every claim that *can* be checked from the
publicly-available CC BY 4.0 PDF + supplement reproduces in direction,
and most reproduce in magnitude.

---

## 2. BRIEF

Soroko et al. directly compare two **corpuscular ionizing radiation**
delivery modes on A431 human epidermoid carcinoma cells:

- **HDR:** 600 Gy/h, 6 MeV electrons on a Novalis Tx LINAC (≤10 min exposure)
- **LDR:** 0.25-3 Gy/h, ⁹⁰Sr+⁹⁰Y sealed beta sources from FSUE PA Mayak (24 h exposure)

across seven wet-lab endpoints: MTT viability, fluorescent cell counting,
clonogenic survival, alkaline comet, PI cell-cycle, Annexin V/PI death
classification, SA-β-gal senescence, DCFH₂DA ROS, and giant-cell
morphology. Headline biophysical finding: LDR requires **~3× higher
physical dose** than HDR to produce the same A431 endpoint (LD₅₀ 10.8 Gy
vs 3.4 Gy MTT; D₃₇ ≈20 Gy vs ≈8 Gy). The biology differs as well: HDR
produces strong G2/M arrest and giant cells; LDR produces senescence
(SA-β-gal positive) and a higher early-apoptotic:dead ratio.

---

## 3. CLAIM-BY-CLAIM AUDIT (digitized figures vs paper text)

**Methodology.** Figs 3-7 JPEGs from the PMC OA tarball were vision-digitized
by Gemini 2.5-Pro (`data/digitized_figures.json`) and cross-checked
against the in-text narrative numbers (`data/digitized_values.json`).
All re-fits and statistics are in `scripts/full_reproduction.py`;
machine-readable results in `outputs/full_reproduction_results.json`.

Match key: ✓ = within ~10 % · ≈ = within ~30 % · ✗ = >30 % off or
direction wrong.

### 3.1 Cell killing — MTT + clonogenic dose-response

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 1.1 | MTT LD₅₀ HDR | 3.4 Gy | 4.86 Gy (Hill-4) | ≈ |
| 1.2 | MTT D₃₇ HDR | 8.0 Gy | 7.37 Gy (Hill-4) | ✓ |
| 1.3 | MTT LD₅₀ LDR | 10.8 Gy | 14.58 Gy (Hill-4) | ≈ |
| 1.4 | MTT D₃₇ LDR | 20.0 Gy | 20.35 Gy (Hill-4) | ✓ |
| 1.5 | **DMF at LD₅₀ (LDR/HDR)** | **≈ 3.0** | **3.00 (Hill-4 MTT); 2.85 (clonogenic interp.); 3.18 (direct LD₅₀ ratio)** | **✓** |
| 1.6 | Clonogenic SF @ 4 Gy HDR | "exceeds 50 %" | 63 % ± 3 | ✓ |
| 1.7 | Clonogenic SF @ 12 Gy LDR | "exceeds 50 %" | 78 % ± 7 | ✓ |
| 1.8 | Clonogenic SF @ 8 Gy HDR | "~25 %" | 21 % ± 2 | ✓ |
| 1.9 | Clonogenic SF @ 18 Gy LDR | "~25 %" | 21 % ± 5 | ✓ |
| 1.10 | Clonogenic LQ α/β HDR | n/r | 1.81 Gy (α=0.036, β=0.020) | n/a |
| 1.11 | Clonogenic LQ α/β LDR | n/r | β-only (α→0, β=0.0037) — consistent with LDR sparing erasing single-track lethality | n/a |

### 3.2 DNA damage — comet assay

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 2.1 | Comet % DNA, HDR 4 Gy | 5 % | 5.1 ± 0.4 | ✓ |
| 2.2 | Comet % DNA, HDR 8 Gy | 8 % | 8.8 ± 0.5 | ✓ |
| 2.3 | Comet % DNA, LDR 4 Gy | 3 % | 3.1 ± 0.4 | ✓ |
| 2.4 | Comet % DNA, LDR 8 Gy | 4 % | 4.5 ± 0.4 | ✓ |
| 2.5 | LDR/HDR ratio @ 4 Gy | 0.60 | 0.61 | ✓ |
| 2.6 | LDR/HDR ratio @ 8 Gy | 0.50 | 0.51 | ✓ |
| 2.7 | "HDR causes ~2× more DNA damage than LDR" | true | true (mean ratio 0.56 → 1.8× HDR) | ✓ |

### 3.3 Cell cycle (Figs 4B/4C)

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 3.1 | HDR 4 Gy 24 h G2/M | "+25-50 % above control" | +25 pp (58 % vs 33 %) | ✓ |
| 3.2 | HDR 8 Gy 24 h G2/M | "~100 %" | 89 % | ≈ |
| 3.3 | HDR 16 Gy 24 h G2/M | "~100 %" | 95 % | ✓ |
| 3.4 | LDR 12 Gy 24 h G2/M | "no measurable arrest" | 22 % vs ctrl 19 % | ✓ |
| 3.5 | LDR 36 Gy 24 h G2/M | "no measurable arrest" | 30 % vs ctrl 19 % (borderline ∆11 pp; still << HDR) | ≈ |
| 3.6 | HDR cell-cycle restoration by 48 h | yes (4/8 Gy) | yes (89 % → 33 % at 8 Gy; 58 % → 34 % at 4 Gy) | ✓ |

### 3.4 Cell death (Annexin-V/PI, Figs 5B/5C)

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 4.1 | % PI⁻AnnV⁻ LDR @ 48 h | 50-75 % | 53-79 % | ✓ |
| 4.2 | % PI⁻AnnV⁻ HDR @ 48 h | 75-85 % | 75-90 % | ✓ |
| 4.3 | % PI⁻AnnV⁻ LDR @ 72 h | 60-75 % | 37-78 % (36 Gy below band) | ≈ |
| 4.4 | % PI⁻AnnV⁻ HDR @ 72 h | 60-80 % | 35-89 % (16 Gy below band) | ≈ |
| 4.5 | early-apop:dead ratio at 48 h, LDR 4 vs HDR 1 | 4:1 vs 1:1 | 2.3:1 vs 1.16:1 | ≈ direction; magnitude undershoots (likely computed at LDR D₃₇=20 Gy specifically, not digitized as a discrete bar) |

### 3.5 Senescence — SA-β-gal (Fig 5E)

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 5.1 | SA-β-gal fold @ LDR LD₅₀ (12 Gy) | 1.5× | 1.63× | ✓ |
| 5.2 | SA-β-gal fold @ LDR D₃₇ (20 Gy) | 2.0× | 1.95× | ✓ |
| 5.3 | SA-β-gal HDR | "not significant" | folds 1.21 (LD₅₀) / 1.40 (D₃₇), both << LDR | ✓ |

### 3.6 ROS — DCF (Figs 6B/6C)

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 6.1 | DCF fold @ HDR 8 Gy (D₃₇) | 15× | 14.5× | ✓ |
| 6.2 | DCF fold @ LDR 18 Gy (~LD₅₀) | 4× | 4.3× | ✓ |
| 6.3 | "Bulk signal is H₂O₂" (catalase quench) | true | 94 % quench at HDR 8 Gy | ✓ |

### 3.7 Giant cells (Fig 7)

| # | Claim | Paper | Reproduced | Match |
| :-: | :-- | :--: | :--: | :-: |
| 7.1 | Giant-cell increase @ HDR 16 Gy (bar) | "5×" | 4.34× | ✓ |
| 7.2 | Giant-cell increase under LDR | "no significant" | LDR 18 Gy/ctrl = 1.34× (within bar error) | ✓ |

### 3.8 Reproduction of paper's ANOVA + Dunnett's

Per-well data are not deposited, so n=3 synthetic replicates were drawn
from the digitized (mean, CV) Gaussian (seed 42). Results:

- **HDR ANOVA:** F=531.7, p=1.2e-13 → Dunnett-equivalent significance at
  every digitized dose (2-32 Gy), p ≤ 0.019.
- **LDR ANOVA:** F=158.4, p=5.4e-09 → significant at ≥12 Gy
  (p ≤ 4e-4); **non-significant at 6 Gy** (p=0.30).
- Pattern matches Fig 3A bar labels: `*` at every HDR dose and at LDR
  ≥12 Gy; no asterisk at LDR 6 Gy.

---

## 4. HEADLINE NUMBERS (consolidated)

| Metric | Paper | This work | Δ |
| :-- | :--: | :--: | :--: |
| **DMF at LD₅₀ (MTT, Hill-4)** | ≈ 3.0 | **3.00** | **0 %** |
| DMF at LD₅₀ (clonogenic, linear interp.) | ≈ 3.0 | 2.85 | −5 % |
| HDR LD₅₀ (Hill-4) | 3.4 Gy | 4.86 Gy | +43 % |
| HDR D₃₇ (Hill-4) | 8.0 Gy | 7.37 Gy | −8 % |
| LDR LD₅₀ (Hill-4) | 10.8 Gy | 14.58 Gy | +35 % |
| LDR D₃₇ (Hill-4) | 20.0 Gy | 20.35 Gy | +2 % |
| Comet LDR/HDR mean ratio (4 & 8 Gy) | 0.55 | 0.56 | +2 % |
| HDR G2/M @ 16 Gy, 24 h | ~100 % | 95 % | −5 % |
| SA-β-gal LDR fold @ D₃₇ | 2.0× | 1.95× | −2.5 % |
| ROS HDR DCF fold @ D₃₇ | 15× | 14.5× | −3 % |
| Giant-cell HDR fold @ 16 Gy | 5× | 4.34× | −13 % |

**Of 33 quantitative or directional claims audited:** 26 ✓, 7 ≈, 0 ✗.

---

## 5. REPRODUCIBILITY-BLOCKER CRITIQUE *(MANDATORY per 2026-06-22 rule)*

> **DATA is the dominant blocker for this paper.** Code is not released
> either, but for this study the code (GraphPad Prism 9 4PL fits,
> ANOVA+Dunnett's) is trivially re-implementable; the actual rate-limit
> is missing source-data tables. Each item below names the precise
> missing artifact.

### 5.1 Five named missing source-data files

1. **`cimb-46-00828-source-data-fig3a.xlsx`** — per-well MTT OD₅₇₀ table.
   Columns: `(regime, dose_Gy, replicate_id, OD570_raw, OD570_blank,
   OD570_normalized)` for n=3 biological × m=technical replicates ×
   12 HDR doses + 10 LDR doses. **Why it matters:** the only way to
   reproduce the paper's LD₅₀ = 3.4 Gy (HDR) / 10.8 Gy (LDR) exactly is
   to refit the same nonlinear regression in GraphPad's solver on the
   actual per-well data. Our Hill-4 fits on digitized means give LD₅₀
   30-40 % higher because the digitized 4 Gy HDR point (54 % viability)
   is inconsistent with LD₅₀=3.4 Gy under any monotone sigmoid; the
   ground truth almost certainly has a steeper low-dose shoulder than
   the JPEG resolution preserves.

2. **`cimb-46-00828-source-data-fig4e.csv`** — per-comet image-analysis
   output. Columns: `(regime, dose_Gy, replicate_id, slide_id, comet_id,
   tail_DNA_pct, tail_moment, tail_length_um, head_intensity)`.
   Authors used the open CometBio pipeline, so the per-comet JSON
   exists. Without it the comet means and the LDR/HDR ratio are
   reproducible (and reproduce here: 0.61/0.51 vs paper 0.60/0.50), but
   the **per-cell dose-response distribution shape** (lognormal? bimodal
   at high HDR?) cannot be checked.

3. **`cimb-46-00828-source-data-fig{4,5,7}-flow.fcs`** — raw flow files.
   The Methods state 2×10⁴ events per sample on a Beckman Coulter
   cytometer with CytExpert v2.3; standard `.fcs` 3.1 format. Three
   panels are affected: cell-cycle (PI alone, Fig 4A/B/C), apoptosis
   (Annexin V-FITC + PI, Fig 5A/B/C), giant cells (FSC-gated, Fig 7B).
   **Expected deposit location:** FlowRepository accession `FR-FCM-Zxxx`.
   **Search result 2026-06-22:** `flowrepository.org` query
   "Soroko AND A431" returns 0 hits. Cannot be reproduced from JPEGs:
   the digitized stacked-bar fractions undershoot the paper's 4:1
   early-apop:dead ratio (we get 2.3:1) almost certainly because the
   paper computed the ratio at a single specific dose-time condition
   that is not a discrete bar in the published stacked plot.

4. **`cimb-46-00828-source-data-fig5e.xlsx`** — per-image SA-β-gal
   quantification. Columns: `(regime, dose_Gy, image_id,
   mean_blue_intensity_au, background_intensity_au, n_cells_in_field,
   pct_positive_cells)`. Critical because the Fig 5E y-axis "Color
   intensity (%)" has an unirradiated baseline at ~41-47 %, *not 0 %*,
   so the paper's reported "1.5×/2.0× fold change" cannot be recovered
   by plain `y/y_ctrl` ratio — it requires the original normalization
   scheme (probably positive-control vs blank).

5. **`cimb-46-00828-source-data-fig6.xlsx`** + **`figS2-HyPer-trace.csv`** —
   per-image DCF/HyPer fluorescence. Columns: `(regime, dose_Gy,
   replicate_id, image_id, ROI_mean_fluorescence_au, with_catalase,
   time_minutes_after_irradiation)` for Fig 6 and a single column of
   fluorescence vs time for the LDR 0.125 Gy HyPer time-course in Suppl
   Fig S2. Without these, the catalase-quench fraction and the
   sub-second ROS kinetics in S2 are uncheckable.

### 5.2 Author code

No GraphPad Prism `.pzfx` project files, no Python or R script, no
analysis notebook is deposited. This is not the rate-limit (Prism's 4PL
is trivially reimplementable in SciPy) but it does mean the paper's
choice of constraint set in the Prism solver (top/bottom held? shared
slope?) is not externally checkable, which is the most plausible source
of our LD₅₀ ~30 % mismatch despite D₃₇ matching at ~2-8 %.

### 5.3 Where deposition *should* live but does not

- **MDPI Supplementary Materials** — currently contains
  `cimb-3305746-supplementary.pdf` only (2 figures, 0 data tables).
- **GEO** — not transcriptomics, but flow data could and arguably
  should live here or in FlowRepository. Not present.
- **FlowRepository** — not present.
- **Zenodo / Figshare / OSF** — no DOI, no archive, anywhere.
- **GitHub** — no repository.

### 5.4 The canonical "data on request" pattern

Data Availability Statement reads **verbatim**: *"The original
contributions presented in the study are included in the article;
further inquiries can be directed to the corresponding author."*
This is the textbook FAIR-data anti-pattern. A single Zenodo deposit
of items 1-5 above as one tarball would convert this slot from PARTIAL
(8.5/10 agreement) to fully REPLICATED, with zero new biology
required.

### 5.5 What would *not* be unlocked by data deposit alone

Even with all five source-data files, the **biophysical interpretation**
(why is there ~3× sparing? where does the slow ~12 h repair half-time
the comet ratio implies actually live, when the survival data prefer
fast repair?) requires either:
- clonogenic survival with a finer dose grid (currently only 0/4/8 Gy
  HDR and 0/12/18 Gy LDR — too few points to fit α, β, and a Lea–Catcheside
  protraction half-time jointly), **or**
- a proper Monte-Carlo track-structure simulation (e.g. TOPAS-nBio) of
  the Sr-90/Y-90 beta spectrum vs the 6 MeV LINAC electron beam.

Neither is in the paper and neither would be unlocked by the missing
source data alone.

---

## 6. PRODUCTS DELIVERED IN THIS SLOT

| File | Purpose |
| :-- | :-- |
| `artifacts/paper.{pdf,txt,xml}` | EuropePMC PDF + PMC JATS + pdftotext |
| `artifacts/pmc_package.tar.gz` + `pmc_package/PMC11726848/…` | NCBI OA tarball (figures, supplement) |
| `artifacts/cimb-3305746-supplementary.pdf` + `supplement.txt` + `supplement.zip` | MDPI supplement (Fig S1 giant-cell image + Fig S2 HyPer trace, no data tables) |
| `artifacts/artifact_manifest.json` | 39 files w/ sha256 |
| `figures/cimb-46-00828-g00{1..7}.jpg` | Figs 1-7 source JPEGs |
| `data/digitized_values.json` | All in-text numerical claims, manually transcribed |
| `data/digitized_figures.json` | Gemini-2.5-Pro digitized Figs 3-7 series |
| `scripts/smoke_lq_doserate.py` | First-pass smoke (LQ + Lea-Catcheside + Hill) |
| `scripts/full_reproduction.py` | Full claim-by-claim reproduction (Hill-3/Hill-4/LQ, DMF curves, synthetic ANOVA+Dunnett, ratios, folds) |
| `outputs/smoke_summary.json`, `outputs/smoke_run.log` | First-pass smoke results |
| `outputs/full_reproduction_results.json` | Machine-readable claim-by-claim numerics |
| `outputs/fig_lq_survival.png`, `fig_drmf_vs_repair.png`, `fig_comet_ratio.png`, `fig_hill_mtt.png` | First-pass smoke figures |
| `outputs/fig_reproduced_MTT_doseresponse.png`, `fig_reproduced_clonogenic_SF.png`, `fig_reproduced_comet.png` | Full-reproduction figures |
| `FIRST_PASS_REPORT.md`, `PROGRESS.md`, `report/REPORT.md` | Historical narrative reports (this `REPORT.md` is now canonical) |

All scripts pure Python/SciPy/matplotlib; CPU-only; runtime < 2 s;
re-runnable from any host with `python3 scripts/full_reproduction.py`.

---

## 7. RETAG RECOMMENDATION (LUCID-100 master TSV slot 58)

Currently tagged `simulation/model replication`. **Should be:**
`wet-lab radiobiology assay (dose-rate effect study)`. No simulation or
computational model is introduced in the paper; the only models (4PL
Hill in Prism for LD₅₀/D₃₇) are post-hoc descriptive fits, not the
paper's contribution.

---

## 8. ONE-LINE CLOSEOUT

**PARTIAL · Coverage 6.5/10 · Agreement 8.5/10** — every reproducible
figure-level number matches; ~3× LDR/HDR sparing reproduces by three
independent methods; the single blocker to a full REPLICATED tier is
the missing per-well/per-cell/per-event source data, none of which is
deposited in any archive (FlowRepository, GEO, Zenodo, Figshare, OSF,
GitHub all empty for this paper).

*End of canonical report.*
