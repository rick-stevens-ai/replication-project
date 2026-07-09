# LUCID-100 Slot 21 — Top-Level REPORT

**Paper.** Sennhenn K., Polgár S., Loewer A., Madas B., Friedrich T. (2026).
"Influence of LET on Low-dose Radiation Responses: Signatures of
Hyper-radiosensitivity after High-LET Irradiation."
*Radiation Research* **205**(5): 472–483.
DOI: [10.1667/rade-25-00194](https://doi.org/10.1667/rade-25-00194) ·
PMID 41651140.

**Replication folder:** `lucid100-let-hyperradiosensitivity-high-let/`
**Report date:** 2026-06-25 (Thu) America/Chicago.
**Detailed audit:** `report/REPORT.md` (~18 KB, written 2026-06-22). This
top-level file is the LUCID-100 close-out summary.

---

## Brief

The paper introduces an analytical **Modified Multi-Hit Linear (MML)**
survival equation as a mechanistic account of low-dose
hyper-radiosensitivity (HRS) and induced radioresistance (IRR), and
couples MML with the **Local Effect Model (LEM)** to predict how those
signatures change with LET. Headline empirical claim: HRS is
*progressively compressed* with increasing LET, eventually replaced by a
steep initial decline without recovery, validated on helium and carbon
ion clonogenic data.

The paper's data backbone is the Polgár et al. 2022 *Sci Data* / STOREDB
DATASET1252 (CC-BY-4.0, ≈101 curves, 52 cell lines, 1020 dose-SF
points). Two paper co-authors (Polgár, Madas) are common to both
publications. The article body itself is **paywalled** (Allen Press /
KGL Meridian; Unpaywall `is_oa=false`; no preprint on arXiv, bioRxiv, or
Europe PMC; no PMC mirror).

---

## VERDICT

> **PARTIAL.** **Coverage 5 / 10. Agreement 8 / 10.**

The reproducible **backbone** — LQ and Joiner–Marples Induced-Repair
(IR) survival fits across the full open Polgár 2022 cohort — is
independently and quantitatively reproduced on this machine using only
free / CC-BY sources. The paper's **novel** contributions (the
analytical MML equation, the MML × LEM coupling, the headline
ion-validation LET-compression curve) are **not** independently
verifiable from open material in this pass: the article body is
paywalled and the helium/carbon-ion validation cohort is not bundled in
STOREDB.

Four-tier scale: [ ] REPLICATED [x] **PARTIAL** [ ] SPOT-CHECK [ ] NO-GO.

---

## Evidence summary

**Pipeline.** Four CPU-only scripts (`code/parse_db.py`,
`code/fit_models.py`, `code/let_compression.py`,
`code/strengthen_fits.py`) total ≈45 KB Python. End-to-end run < 4 min,
single core on CherryRd, deps `numpy / scipy / matplotlib / openpyxl /
pandas`. Deterministic (seed 20260622).

**Coverage (5/10) — what was reproduced:**
- 101 / 101 curves loaded from STOREDB v2 → both LQ and IR fit
  successfully (98 / 101 with bootstrap CIs, B = 200).
- Cohort-level model selection: **IR beats LQ ΔAICc > 4 in 41 %** (40 /
  98); **ΔBIC > 2 in 79 %**.
- Goodness-of-fit on log10 SF: median R² **0.969 (IR) vs 0.851 (LQ)**;
  fraction R² ≥ 0.95 = 58 % (IR) vs 29 % (LQ).
- HRS-IRR signature (ΔAICc > 4 ∧ α_s > 1.5 α_r ∧ D_c < 1 Gy)
  detected in 40 / 98 curves. Top hits include the landmark studies
  Marples & Joiner 1993 V79 (ΔAICc 35.6, α_s/α_r ≈ 29, D_c ≈ 0.37 Gy)
  and Lambin 1993 HT29 (ΔAICc 25.2, α_s/α_r ≈ 19, D_c ≈ 0.19 Gy) —
  textbook HRS reference cases, exactly where they should sit.

**Agreement (8/10) — quantitative reproduction of published numbers:**
Independent bounded-NLS re-fit reproduces the published IR parameters
the source spreadsheet carries to a **median |relative diff| of
~11 %**:
- α_r: 10.6 % (n = 57)
- α_s: 11.8 % (n = 59)
- D_c: 11.2 % (n = 66)

This is well inside the floor for independent re-fitting of digitised
colony-survival data. The LQ α also matches at 19 % (n = 26); LQ β is
noisy at 87 % median (n = 20), but β is not load-bearing for the HRS
shape claims.

**Direction-of-effect on LET-compression (cannot reach paper's
headline):** Open-cohort subset is photon-dominated (51 low-LET vs 7
parsable high-LET; 1 neutron; 1 ion of unspecified LET). Mann–Whitney
low- vs high-LET: D_c U = 128, p = 0.24 (medians 0.184 vs 0.220 Gy);
α_s/α_r U = 186, p = 0.14 (medians 11.4 vs 5.5). The α_s/α_r
direction-of-effect is consistent with the paper's "compression"
hypothesis but is **underpowered (n_high = 7)** and cannot replace the
paper's helium/carbon ion validation cohort.

**Artifacts** (all CC-BY-4.0, sha256-stamped in `ARTIFACT_MANIFEST.tsv`):
4 raw STOREDB files (≈ 810 KB) + 4 derived CSVs + 1 summary JSON + 9
figures + 4 scripts. Total project size ≈ 1.6 MB. No paid endpoints, no
author contact, no paywall circumvention.

---

## Blocker critique (mandatory 6/22 rule)

The reproducibility blocker is **data**, not compute: the **paper's
helium / carbon-ion validation cell-survival cohort is not a public
artifact and cannot be reconstructed from open sources.** This is the
single artifact whose absence prevents independent verification of the
paper's headline empirical claim.

### Specific missing data artifact

**Name.** The Materials-and-Methods / Supplementary table of helium-
and carbon-ion clonogenic survival curves used for MML × LEM validation
in Sennhenn et al. 2026.

**Required fields (per curve):** cell line, ion species, beam energy,
LET (keV/μm), dose points (Gy), surviving fraction with uncertainty,
published LQ / IR fit parameters, and DOI of the originating
experimental publication.

**Where it should be:** inside the paywalled article body (DOI
[10.1667/rade-25-00194](https://doi.org/10.1667/rade-25-00194)) and/or
its supplementary materials hosted by Allen Press / KGL Meridian.
Neither is on Europe PMC, PMC, arXiv, or bioRxiv. The open STOREDB
DATASET1252 (the only open survival database the paper draws from)
contains only ~7 parsable high-LET curves — far too few for the LET
sweep the paper claims to validate.

**Why this is the blocker (not the article body itself):** The article
body is paywall-gated (Blocker 1 in `report/REPORT.md`), but a one-time
library unlock at Argonne would dissolve that gate. The *data table*
gated behind it is the irreducible artifact: without it, even with the
text in hand, the LET-compression curve cannot be reconstructed.

**Free fallback for a future pass:** PIDE-v3.2 (GSI Particle
Irradiation Data Ensemble, public) is the obvious open proxy for an ion
cell-survival cohort. It is **not identical** to the paper's
validation set, but is the cheapest tractable substitute and is not
bundled in STOREDB. Acquiring PIDE-v3.2 is the natural next-pass
action.

### Two secondary, non-data blockers (documented in `report/REPORT.md`)

- **Article body paywall** — needed for the analytical MML equation,
  the MML × LEM coupling, and the exact "93-curve" filter rule the
  authors apply on top of the ≈101-curve open database. Unlock path:
  Argonne library / RRS member access. Not attempted this pass.
- **No published MML / LEM implementation.** The
  `Radiobiology-Informatics-Consortium` GitHub org (the authors' org)
  exists but contains a single repo (`RBO`, Radiation Biology
  Ontology). No MML, no LEM, no `mml-lem` companion code. Local
  `pdftotext | grep -iE "(LEM|MML|GitHub|Radiobiology-Informatics|
  local effect|multiscale)"` on both STOREDB v1 and v2 description PDFs
  → zero hits. Confirmed verification, not a guess.

### Recommendation

Retain in LUCID-100 with worktype retagged from `omics/signature
replication` → **`computational model / dose-response`**. The
replication-relevant LQ / IR backbone claim is robustly reproduced on
open material; the novel MML × LEM modelling content is paywall- and
data-gated and is honestly out of reach for a no-author-contact /
no-paid-endpoint pass.

---

*See `report/REPORT.md` for the full claim-by-claim audit, per-cell-line
table, figure inventory, and detailed next-pass plan.*
