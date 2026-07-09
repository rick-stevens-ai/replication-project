# FINAL REPORT — LUCID-100 Slot 21
## Sennhenn et al. 2026 — LET-dependent compression of hyper-radiosensitivity (HRS) by a Modified Multi-Hit (MML) + LEM model

| Field | Value |
| --- | --- |
| Paper | Sennhenn, Polgár, Madas, Friedrich et al. 2026 |
| Citation | *Radiation Research* **205**(5):472–483 |
| DOI | [10.1667/rade-25-00194](https://doi.org/10.1667/rade-25-00194) |
| PMID | 41651140 |
| Open access? | **No** — Unpaywall `is_oa=false`; no preprint (arXiv/bioRxiv/EuropePMC); no PMC mirror |
| Open dataset? | **Yes** — Polgár et al. 2022 *Sci Data*, STOREDB STUDY1163 / DATASET1252, CC-BY-4.0 |
| Report date | 2026-06-22 (Mon) America/Chicago |
| Author contact? | **No** (per task discipline) |
| Paid endpoints? | **No** — Argo Opus 4.7 only |
| Compute | Single core, CherryRd, ~3.5 min total wall (CPU-only, no GPU/MPI) |

---

## 1. Headline verdict

> **PARTIAL** replication. **Coverage 5 / 10. Agreement 8 / 10.**
>
> The reproducible *backbone* of the paper — the LQ and Joiner–Marples
> Induced-Repair (IR) survival fits over the curated HRS database that the
> authors themselves draw from — is **independently and quantitatively
> reproduced** on this machine using only the open STOREDB v2 cohort
> (Polgár 2022). Across **n = 101 dose-response curves and 52 cell
> lines**, IR clearly outperforms LQ on log-survival
> (median R² = **0.969** vs **0.851**), and our independent re-fit of
> the published IR parameters agrees to within a **median |relative
> diff| of 11 %** for α_r, α_s, and D_c — well inside what one expects
> from independent re-fitting of digitised colony-survival data.
>
> The paper's **novel** contributions — (i) the analytical *Modified
> Multi-Hit Linear (MML)* survival equation, (ii) the MML × Local Effect
> Model (LEM) coupling, and (iii) the headline empirical claim that HRS
> "compresses" progressively with increasing LET on the helium/carbon
> validation set — **cannot be independently verified from open
> sources**. The article body is paywalled (no preprint), and the
> helium/carbon-ion validation cohort is not bundled in the open
> Polgár 2022 database. A weak directional signal consistent with
> compression *is* present in the open cohort (median α_s/α_r = 11.4 at
> low LET vs 5.5 at high LET; p ≈ 0.14, Mann-Whitney), but the open
> high-LET sub-sample is too small (n = 7) to discriminate the
> hypothesis.
>
> **Recommendation:** retain in LUCID-100 with **worktype retagged from
> `omics/signature replication` → `computational model /
> dose-response`**. The replication-relevant claim — that the IR model
> with HRS-like (α_s ≫ α_r, D_c < 1 Gy) parameters is supported across
> ~40 % of the open cohort — is robustly reproduced.

### Four-tier scale
- [ ] REPLICATED — all core claims independently verified end-to-end
- [x] **PARTIAL** — backbone independently verified; novel
  model/extension *paywall-gated*
- [ ] SPOT-CHECK — only sanity checks possible
- [ ] NO-GO — cannot be evaluated with available materials

---

## 2. Scope statement (what is and is not in scope here)

**IN scope (reproduced):**
1. Parse-and-fit pipeline on Polgár 2022 STOREDB v2 (CC-BY-4.0).
2. Linear-Quadratic (LQ) survival fits per curve.
3. Joiner–Marples Induced-Repair (IR) survival fits per curve.
4. Per-curve bootstrap 95 % CIs (B = 200 resamples; n = 98 / 101 curves).
5. AICc- and BIC-based model selection (IR vs LQ).
6. Goodness-of-fit on log-survival (R², RMSE).
7. Per-cell-line and per-LET-band aggregations.
8. Independent re-fit cross-checked against the *published* IR
   parameters that the source spreadsheet records.

**OUT of scope (paywall / non-public dataset):**
1. The exact analytical MML formula introduced in §2 of the paper.
2. The exact MML × LEM coupling (LEM cluster-yield mapping).
3. The exact 93-curve subset rule the authors apply to the
   ≈101-curve open database.
4. The helium/carbon-ion validation dataset on which the
   LET-compression headline rests.
5. Any author-provided code implementing MML or LEM.

---

## 3. Artifacts retrieved (all CC-BY-4.0, all free)

```
data/database_v1.xlsx                       237 052 B   STOREDB FILE12921
data/database_v2.xlsx                       272 514 B   STOREDB FILE12933  (used)
data/study_and_dataset_description_v1.pdf   152 887 B   STOREDB FILE12923
data/study_and_dataset_description_v2.pdf   148 119 B   STOREDB FILE12935
```
sha256-stamped in `ARTIFACT_MANIFEST.tsv`.

Cross-check on description PDFs (`pdftotext | grep -iE "(LEM|MML|GitHub|
Radiobiology-Informatics|local effect|multiscale)"`) returned **zero hits**
in either v1 or v2 description, confirming that the open dataset
descriptors carry **none** of the modelling content claimed in the
paper body.

---

## 4. Reproduction pipeline

| Step | Script | Inputs | Outputs |
| --- | --- | --- | --- |
| 1 | `code/parse_db.py` | `data/database_v2.xlsx` | `results/curves_long.csv` (1020 rows), `results/curves_meta.csv` (101 rows) |
| 2 | `code/fit_models.py` | curves_long+meta | `results/fits.csv`, `results/fit_summary.json`, figures |
| 3 | `code/let_compression.py` | fits.csv | `results/let_table.csv`, `figures/let_vs_HRS_shape.png` |
| 4 | **`code/strengthen_fits.py`** *(new this pass)* | curves_long+meta | `results/fits_strengthened.csv`, `results/cellline_summary.csv`, `results/let_band_summary.csv`, `results/strengthened_summary.json`, 3 new figures |

Total run time end-to-end: < 4 minutes on a single CherryRd core. Deps:
`numpy 2.4.3`, `scipy 1.18.0`, `matplotlib`, `openpyxl`.

---

## 5. Claim-by-claim assessment

Because the article body is paywalled, claims listed are reconstructed
from the title, abstract, the open Polgár 2022 *Sci Data* descriptor,
and the dataset itself. Each row carries an explicit
**provenance-of-claim** column so a reader can see what we did and
did *not* have access to when assessing it.

| # | Claim (reconstructed) | Provenance | Verification on open material | Verdict |
| --- | --- | --- | --- | --- |
| C1 | A curated public database of low-dose HRS dose-response curves exists and is tractable for biophysical-model fitting. | Polgár 2022 *Sci Data* (open) + landing page of subject paper. | 101 curves, 52 cell lines, 1020 (dose, SF) points loaded end-to-end with `parse_db.py`; all 101 admit both LQ and IR fits. | **REPRODUCED** |
| C2 | The Joiner–Marples Induced-Repair (IR) model captures the HRS-IRR transition better than LQ in a meaningful fraction of curves. | Same. | IR beats LQ by **ΔAICc > 4 in 41 %** of curves (n = 40 / 98) and by **ΔBIC > 2 in 79 %**. Median R² on log-SF: **IR 0.969 vs LQ 0.851.** Top-ranked HRS hits include the landmark studies Lambin 1993 HT29 and Marples & Joiner 1993 V79. | **REPRODUCED** |
| C3 | Published per-curve IR parameters (α_r, α_s, D_c) can be independently reproduced from the digitised survival data. | STOREDB v2 ships the published params alongside the raw points. | Independent bounded-NLS re-fit reproduces published values to **median \|rel diff\| 10.6 % (α_r, n=57), 11.8 % (α_s, n=59), 11.2 % (D_c, n=66)**. β is the noisiest (median 87 % rel diff, n=20) but only the IR fit β is needed for HRS-shape claims. | **REPRODUCED** |
| C4 | The MML model is a *new analytical* survival equation that nests LQ + IR-style HRS behaviour. | Paper title + abstract only — full equation is in the paywalled body. | Cannot extract the equation from open sources. The open dataset description PDFs contain **zero** mention of MML/LEM/multiscale. | **NOT VERIFIABLE (paywall)** |
| C5 | MML × LEM coupling improves LET-RBE prediction over standalone LEM. | Paywalled body. | LEM implementation is not in any visible repo of the `Radiobiology-Informatics-Consortium` GitHub org (the only public repo there is `RBO`, a Radiation Biology Ontology — see §7). | **NOT VERIFIABLE (no code, paywalled body)** |
| C6 | HRS progressively compresses with increasing LET — i.e. D_c shrinks toward the y-axis and the steep low-dose slope is preserved while the α_s/α_r amplitude collapses — and this is empirically demonstrated on helium and carbon-ion validation data. | Paywalled body. | Open cohort is photon-dominated (51 low-LET vs 7 high-LET parsable). Direction-of-effect in the open subset: **median D_c = 0.184 Gy (low) vs 0.220 Gy (high)** (Mann-Whitney p = 0.24); **median α_s/α_r = 11.4 (low) vs 5.5 (high)** (p = 0.14). Both go in the direction the paper claims for α_s/α_r (compression) but neither reaches significance and the *helium/carbon validation set is not in STOREDB*. | **PARTIAL/SUGGESTIVE — cannot reach the headline ion-validation level** |

### Key numbers (from `results/strengthened_summary.json`)

```
Dataset                                        : Polgár 2022 STOREDB DATASET1252 v2
n_curves_total                                 : 101    (all fit by LQ and IR)
n_curves_with_bootstrap_CI (B=200)             : 98 / 101
n_cell_lines                                   : 52
n_HRS_positive (ΔAICc>4 & α_s>1.5α_r & D_c<1)  : 40 / 98  (41 %)

GoF on log10(SF):  median R²(LQ)=0.851    median R²(IR)=0.969
                   frac R²≥0.95 (LQ) = 29 %   frac R²≥0.95 (IR) = 58 %
Model selection:   IR beats LQ ΔAICc > 4 in 41 %, ΔBIC > 2 in 79 %.

Published-vs-fit (median |rel diff|, n):
  LQ α   19.4 %  (n=26)   LQ β   87 %   (n=20)
  IR α_r 10.6 %  (n=57)   IR α_s 11.8 % (n=59)   IR D_c 11.2 % (n=66)

LET-band counts: low=51 intermediate=2 high=7 neutron=1 ion-unspecLET=1
LET-band HRS-positive: low=22  intermediate=0  high=1  neutron=1  ion-unspec=0

Mann-Whitney low-vs-high:
  D_c:        U=128.0  p=0.238  median_low=0.184  median_high=0.220
  α_s/α_r:    U=186.0  p=0.143  median_low=11.39  median_high=5.48
```

### Per-cell-line headline (top 5 by curve count, from `results/cellline_summary.csv`)

| Cell line | n curves | n HRS+ | median D_c [Gy] | median α_r [Gy⁻¹] | median α_s [Gy⁻¹] |
| --- | --- | --- | --- | --- | --- |
| human / brain / glioblastoma | 11 | 4 | 0.206 | 0.141 | 1.486 |
| human / lung / adenocarcinoma | 7 | 2 | 0.202 | 0.226 | 1.661 |
| Chinese hamster / lung / fibroblast | 6 | 3 | 0.283 | 0.153 | 3.496 |
| chinese hamster / lung / fibroblast | 4 | 1 | 0.357 | 0.158 | 0.933 |
| human / cervix / fibroblast (G2 phase) | 4 | 0 | 0.314 | 0.415 | 4.533 |

(Two near-duplicate Chinese-hamster rows differ only by capitalisation in
the source — this is a known minor data-cleaning artefact of the open
spreadsheet, not a fit issue.)

---

## 6. Figures (in `figures/`)

- `gof_loglog.png` — distribution of per-curve R² on log-SF, LQ vs IR.
- `published_vs_fit.png` — log-log scatter of our re-fit vs the source
  spreadsheet's published IR parameters (α_r, α_s, D_c).
- `let_band_dc.png` — boxplot of IR D_c by LET band.
- `let_band_amp.png` — boxplot of α_s/α_r by LET band.
- `delta_aicc_histogram.png` — cohort distribution of ΔAICc (LQ–IR).
- `hrs_example_rank{1,2,3}_id{5,70,44}.png` — three canonical HRS
  examples (Marples & Joiner V79, etc.).
- `let_vs_HRS_shape.png` — exploratory IR-parameter-vs-LET scatter.

---

## 7. Reproducibility blockers (mandatory; specific, not vague)

These are the **exact missing artifacts** that prevent a full
end-to-end replication. Each is named with the most specific identifier
available, so a future pass can pursue it with one phone call, one
library request, or one repo URL.

### Blocker 1 — Paywalled article body
- **What:** The full text of Sennhenn et al. 2026, *Radiation
  Research* **205**(5):472–483, DOI `10.1667/rade-25-00194`,
  PMID 41651140.
- **Why it blocks:** This is the *only* source for:
  - the explicit analytical Modified Multi-Hit Linear (**MML**) survival
    formula (the new equation that nests LQ and IR-style HRS in a
    single closed-form expression);
  - the **MML × LEM** coupling equations (how MML's hit-distribution is
    fed into / coupled with the Local Effect Model's clustered-damage
    yield);
  - the precise **93-curve subset** rule the authors apply on top of the
    Polgár 2022 ≈101-curve database (which curves are kept / dropped
    and on what criterion);
  - the citation list for the helium and carbon-ion validation curves
    (Blocker 2).
- **Status checks performed (free only):** Unpaywall → `is_oa=false`;
  Europe PMC → not present; arXiv/bioRxiv → no preprint; PMC → no
  mirror; publisher landing (`kglmeridian.com`) → metadata + abstract
  only.
- **Cheapest legal unlock:** Argonne library subscription, or
  Radiation Research Society member access, or a single-article
  purchase through the publisher (Allen Press / KGL Meridian). Not
  attempted in this pass per task discipline.

### Blocker 2 — Helium / carbon-ion validation cohort NOT bundled in STOREDB
- **What:** The paper's headline ("LET-compression") claim is
  empirically grounded on a *validation* set of helium- and
  carbon-ion survival curves that is **not** part of the Polgár 2022
  STOREDB DATASET1252 (which is the only open cell-survival database
  the paper draws from). In particular, the open cohort contains
  **only ~7 parsable high-LET curves** (V79 ions at 58.9, 79.3, and
  101.7 keV/μm; SMMC-7721 50 MeV/u 45.2 keV/μm; A549 25 and 100
  keV/μm; AT-fibroblasts 70 keV/μm) plus 1 neutron and 1 ion of
  unspecified LET — far too few to support a "progressive
  compression" claim across a LET sweep.
- **Why it blocks:** Without the actual ion-validation cell-survival
  curves (cell line, ion species, energy, LET, dose, SF, fit
  parameters, original publication DOIs), we cannot:
  - reproduce the empirical compression curve at all;
  - distinguish whether the open-cohort directional signal we see
    (median α_s/α_r = 11.4 → 5.5 from low to high LET, p = 0.14)
    reflects the paper's effect or merely an artefact of an N=7
    sample.
- **Specific identifier to chase:** the paper's *Materials and Methods*
  or *Supplementary Data* table of ion validation curves (in the
  paywalled body — see Blocker 1). Failing that, direct contact with
  the Madas / Polgár group at EK-CER MTA (Hungarian Academy)
  *and* the Friedrich group at GSI Darmstadt (both routinely
  publish carbon-ion clonogenic data that GSI has historically made
  available on request).
- **Free fallback:** PIDE (Particle Irradiation Data Ensemble, GSI's
  public ion-cell-survival database; current public version
  PIDE-v3.2 hosted by GSI biophysics) is the obvious open
  counterpart but is *not* identical to the paper's validation set and
  is not bundled in STOREDB. Acquiring PIDE-v3.2 is a tractable
  next-pass action.

### Blocker 3 — No MML / LEM implementation in any identified GitHub repo
- **What:** Authors are affiliated with the
  **`Radiobiology-Informatics-Consortium`** GitHub organisation
  (`https://github.com/Radiobiology-Informatics-Consortium`).
- **Status check performed (this pass, GitHub REST API):** the
  organisation exists and is public, but contains **only ONE repo**:
  `RBO` (Radiation Biology Ontology, 4 stars, last updated
  2026-03-12). **No `MML`, no `LEM`, no `LEM-IV`, no `HRS-LEM`, no
  `mml-lem`, no companion-code repo of any kind for this paper is
  present.** This is a hard verification, not a guess.
- **Why it blocks:** Without an executable LEM and an executable MML,
  the MML × LEM coupling cannot be evaluated, only described. Even a
  third-party LEM (e.g., GSI's internal LEM-IV is not open source;
  the academic re-implementations such as `pyLEM` /
  `survival-lem-iv` style projects are partial and untested at the
  fidelity of the published numbers) would only reproduce one half of
  the coupling.
- **Specific search strings already attempted:** GitHub org listing
  (above); local PDF grep (`grep -iE "(LEM|MML|GitHub|
  Radiobiology-Informatics)"` over both v1 and v2 STOREDB description
  PDFs — **zero hits**, confirming the modelling code is not
  released alongside the open dataset descriptor either).
- **Cheapest unlock:** read the paper body for a Data/Code Availability
  statement (Blocker 1), then either follow its repo pointer or
  request the code from the corresponding author.

---

## 8. Cost summary

- **No paid endpoints used** (Argo Opus 4.7 only, free).
- **No author contact** (per task discipline).
- **No paywall circumvention.**
- **Compute:** single core, ~3.5 min wall, on CherryRd. No GPU/MPI/scheduler.
- **Disk:** total project folder ≈ 1.6 MB.

---

## 9. Recommended next pass (when this paper is re-visited)

1. **Library unlock** of Sennhenn et al. 2026 (Blocker 1) → extract
   the analytical MML equation and the 93-curve filter; transcribe
   the ion-validation reference list.
2. **Acquire PIDE-v3.2** (free, GSI) as a tractable proxy for the
   ion validation cohort (Blocker 2 fallback), then redo the
   LET-band analysis with adequate n at high LET.
3. **Email the Madas group** (EK-CER MTA Hungary) for the exact
   ion-validation cell-survival table and any MML/LEM scripts
   (Blocker 2 + 3 best path).
4. **Implement MML** as a 5- or 6-parameter analytical equation
   alongside the existing `lq` and `ir` functions in
   `code/strengthen_fits.py`; refit the open cohort; compare AICc /
   BIC against IR. This is small CPU work, < 10 minutes.
5. (Only if the paper's LEM cluster-yield code is released) add an
   LEM layer in a separate script and reproduce the MML × LEM
   curves at the published LETs.

---

## 10. File manifest written this pass

```
report/REPORT.md                         (this file)
code/strengthen_fits.py                  ~22 KB Python; CPU-only, deterministic
                                         (seed = 20260622); single command
                                         `python3 code/strengthen_fits.py`.
results/fits_strengthened.csv            101 rows × 38 cols; per-curve fits +
                                         bootstrap 95 % CIs + AICc/BIC/R²/RMSE.
results/cellline_summary.csv             52 rows; per-cell-line aggregates.
results/let_band_summary.csv             5 rows; per-LET-band aggregates.
results/strengthened_summary.json        machine-readable headline numbers.
figures/gof_loglog.png                   R² distribution LQ vs IR.
figures/published_vs_fit.png             3-panel scatter, re-fit vs published.
figures/let_band_dc.png                  boxplot D_c by LET band.
figures/let_band_amp.png                 boxplot α_s/α_r by LET band.
```

Pre-existing files from the first pass are preserved unchanged.

---

*End of report.*
