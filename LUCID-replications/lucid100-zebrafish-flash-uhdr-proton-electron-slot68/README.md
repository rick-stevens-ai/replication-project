# LUCID100 slot 68 — Zebrafish embryo FLASH dose & dose-rate dependence (proton + electron)

**Master rank:** 99 (Wave 7, Tier B, priority 12, candidate_curated)
**DOI:** 10.1016/j.radonc.2024.110197
**PMID:** 38447870 · **HZDR Publ:** Publ-37761-1
**Citation:** Horst F, Bodenstein E, Brand M, Hans S, Karsch L, Leßmann E, Löck S, Schürer M, Pawelke J, Beyreuther E. *Dose and dose rate dependence of the tissue sparing effect at ultra-high dose rate studied for proton and electron beams using the zebrafish embryo model.* Radiother Oncol 2024;194:110197. (Volume 194, pp. 1–7, electronic publication 2024-03-05.)
**License:** CC-BY-NC (HYBRID open access per Unpaywall / Semantic Scholar)

## Why this slot
A comprehensive **wet-lab** zebrafish-embryo radiobiology study from the OncoRay / HZDR-Dresden group characterising the FLASH tissue-sparing effect across:

- **Three beams** at matched physical dose: proton entrance channel, proton spread-out-Bragg-peak (SOBP), and 30 MeV electrons.
- **Wide dose range** 15 – 95 Gy at both UHDR (~10² Gy/s class) and reference dose rate (~10⁻¹ Gy/s class).
- **Four morphological endpoints** at 4 days post-irradiation: pericardial edema, curved spine, embryo length, eye diameter.
- Dose-dependent **FLASH Modifying Factor (FMF)** ≈ 0.7–0.8 above ~50 Gy.
- Demonstrates that **proton RBE** and **UHDR sparing** are *both* needed to predict the resulting dose response — important for clinical translation.

## ⚠️ QA RECLASSIFICATION REQUEST (master TSV)
Current QA tag in `LUCID100_SOLID_MASTER_QA.tsv` row 127:
`worktype = simulation/model replication`
`verdict_or_plan = TODO: simulation/model replication; artifact harvest; brief; run; report`

This is a **misclassification**. The paper is overwhelmingly **wet-lab radiobiology**:

- One-day-old zebrafish embryos irradiated at UHDR vs CONV
- Four scored morphological endpoints at 4 dpi
- Dose-response and FMF curves built from animal data, not Monte Carlo

A minor modelling element exists (LQ-style or sigmoidal dose-response fits and FMF parameterisation), but the substantive content is **wet-lab animal radiobiology + dose-response fitting**.

**Recommended retag:**
- `worktype` → `wet-lab phenotype dose-response replication (zebrafish FLASH)` *(or the project's nearest fit, e.g. `radiobiology / animal model`)*
- `themes` → keep `dose-rate / low-dose response; radiation quality / RBE` and add `FLASH / UHDR; zebrafish embryo model` (drop or downweight `computational model / simulation`).
- `verdict_or_plan` → `Scoping/no-go-without-PDF: paywalled CC-BY-NC; no public code or supplementary data flagged (europepmc hasSuppl=N, hasData=N); replication requires either (a) WebPlotDigitize of dose-response figures from publisher PDF, or (b) author contact for tabular UHDR/CONV survivor fractions and FMF fit parameters. Smoke-replication scaffold built in synthetic-data mode.`

## Source of truth
- Master TSV: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` (row 127 = rank 99)
- This folder: `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-zebrafish-flash-uhdr-proton-electron-slot68/`

## Folder layout
```
README.md                # this file
PROGRESS.md              # session-by-session log
FIRST_PASS_REPORT.md     # verdict + reproducibility scoping
ARTIFACT_MANIFEST.md     # what was collected, with provenance
artifacts/               # PDFs, OAI metadata, blocked-landing snapshots
notes/                   # extracted text from accessible PDFs
scripts/                 # smoke replication script (synthetic-data mode)
data/                    # (empty until tables are digitized from PDF)
figures/                 # (empty until smoke script runs)
```

## Reproducibility snapshot
| Resource | Status | Notes |
| --- | --- | --- |
| Publisher PDF | **blocked** | Elsevier/ScienceDirect captcha; CC-BY-NC but bot-walled. Direct curl/browser both hit "Are you a robot?" challenge. |
| Author repository (HZDR Publ-37761-1) | **OAI metadata only** | Marked open access but no file URL exposed; landing page CMS-gated. |
| Europe PMC full text | **not present** (`inEPMC=N`, `inPMC=N`, `hasSuppl=N`, `hasData=N`) | Confirmed via REST. |
| Unpaywall locations | 1 (publisher only) | Same blocked URL. |
| Preprint (bioRxiv / medRxiv / arXiv) | **none found** | bioRxiv API and bibliographic search both negative. |
| Public code (GitHub / Zenodo / OSF) | **none advertised** | Not in paper metadata; group's prior zebrafish FLASH papers (Beyreuther 2019, Karsch 2022) also do not publish code. |
| Supplementary tables | **not accessible** | Even if the PDF were obtained, supplementary CSV files typically sit on the Elsevier supplementary-material endpoint, equally bot-walled. |

## Smoke replication plan (when PDF arrives)
1. Use WebPlotDigitize (or `plotdigitizer` Python) on Figure 2/3/4 of Horst 2024 to recover ~ 6–8 UHDR + CONV dose-response points per (beam, endpoint).
2. Drop the digitized table into `data/horst2024_doseresponse.csv` with columns: `beam, endpoint, dose_Gy, dose_rate_Gy_per_s, fraction_affected, n_embryos`.
3. Re-run `scripts/smoke_replicate_horst2024.py` (already scaffolded in synthetic mode) to:
   - Fit sigmoidal dose-response *p(D) = 1 / (1 + (D50/D)^k)* per (beam, endpoint, dose-rate) group.
   - Recover `D50_UHDR` and `D50_CONV` and compute `FMF = D50_CONV / D50_UHDR` (equivalent dose ratio for iso-effect; the paper's FMF convention).
   - Plot `FMF(D)` against the meta-analytic ZFE points from Wu et al. 2024 (Karsch 2022, Beyreuther 2019, Saade 2023) to check whether Horst's "FMF ≈ 0.7–0.8 above 50 Gy" sits in family.
4. Verdict gate: FMF reproduced within ±0.05 of the paper's stated 0.7–0.8 band ⇒ PARTIAL SUCCESS; failure to reproduce + no public data ⇒ NO-GO without author contact.

## Compute footprint
**Trivial.** All fits are `scipy.optimize.curve_fit` on ≤ 100 datapoints. Runs in seconds on CherryRd. **No heavy-compute job plan needed.**

## What was *not* done (per task constraints)
- No author contact.
- No paid endpoints.
- No captcha bypass / sci-hub scraping.
- No heavy compute on CherryRd (not needed).
