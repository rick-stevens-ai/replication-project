# LUCID100 Wave 3 / Slot 21 — LET dependence of low-dose hyper-radiosensitivity

**Paper.** Sennhenn K., Polgár S., Loewer A., Madas B., Friedrich T. (2026).
"Influence of LET on Low-dose Radiation Responses: Signatures of
Hyper-radiosensitivity after High-LET Irradiation."
*Radiation Research* **205**(5): 472–483.
DOI: [10.1667/rade-25-00194](https://doi.org/10.1667/rade-25-00194)
PubMed: [41651140](https://pubmed.ncbi.nlm.nih.gov/41651140/)

**Access.** Article body **paywalled** (Allen Press / kglmeridian; not OA,
no preprint, no PMC). Abstract is openly readable and was captured here.

**Why this paper for LUCID100.** The paper introduces an analytical
formulation of the *Minimum Mutation Load* (MML) model — a mechanistic
explanation of HRS as a self-protective tissue strategy — and extends it to
high-LET radiation by composing it with the *Local Effect Model* (LEM). The
combined MML+LEM model is fit against a curated cohort of **93 experimental
survival curves** and validated on helium and carbon ion data. Central claim:
HRS and induced radioresistance are *progressively compressed* with
increasing LET, eventually replaced by an initial steep decline without
recovery.

This sits squarely inside LUCID100's "dose-rate / low-dose response;
radiation quality / RBE; computational model / simulation" theme and is
tractable to scope without paid endpoints because the *underlying curated
dataset is fully public*.

---

## What's in this folder

```
README.md                          ← this file
FIRST_PASS_REPORT.md               ← go/no-go verdict + replication scope
PROGRESS.md                        ← chronological log of this pass
ARTIFACT_MANIFEST.tsv              ← every file with size + sha256 + origin

data/
  database_v2.xlsx                 ← Polgár 2022 STOREDB v2 (101 curves)
  database_v1.xlsx                 ← v1 for completeness (100 curves)
  study_and_dataset_description_v2.pdf   ← official data dictionary
  study_and_dataset_description_v1.pdf

code/
  parse_db.py                      ← XLSX → tidy long/meta CSV (101 datasets)
  fit_models.py                    ← LQ + Induced-Repair fits + HRS detection
  let_compression.py               ← exploratory: HRS shape vs LET

results/
  curves_long.csv                  ← 1020 (dose, SF, SF_min, SF_max) rows
  curves_meta.csv                  ← 101 datasets × metadata + published fits
  fits.csv                         ← 101 datasets × {LQ, IR} fit + ΔAICc
  fit_summary.json                 ← top-level summary numbers
  let_table.csv                    ← per-dataset LET-keyed IR parameters

figures/
  hrs_example_rank{1,2,3}_id*.png  ← per-curve LQ vs IR fits (HRS signatures)
  delta_aicc_histogram.png         ← model selection across the 101-curve cohort
  let_vs_HRS_shape.png             ← exploratory LET vs (D_c, αs/αr)
```

---

## Provenance of the dataset

The 2026 LET paper's "curated dataset of 93 experimental survival curves"
is almost certainly a usability-filtered subset of:

> Polgár, S., Schofield, P.N., Madas, B.G. (2022). *Datasets of in vitro
> clonogenic assays showing low dose hyper-radiosensitivity and induced
> radioresistance.* **Scientific Data** 9, 555.
> DOI: [10.1038/s41597-022-01653-3](https://doi.org/10.1038/s41597-022-01653-3) ·
> PMC: [PMC9458642](https://pmc.ncbi.nlm.nih.gov/articles/PMC9458642/)

Hosted at:

- **STOREDB STUDY1163 / DATASET1252** — DOI
  [10.20348/STOREDB/1163](https://doi.org/10.20348/STOREDB/1163) ·
  [study page](https://www.storedb.org/store_v3/study.jsp?studyId=1163)
- **STOREDB files**: download.jsp?fileId=12921 (v1 xlsx), 12923 (v1 pdf),
  12933 (v2 xlsx), 12935 (v2 pdf) — all copies cached in `data/`
- License: CC-BY-4.0 (per STOREDB Data Sharing Policy)

Two model-side authors (Polgár, Madas) are common to both papers — i.e., the
LET paper's data backbone is *their own* prior open dataset.

---

## Quick reproduction

```bash
cd <this folder>
# requires: numpy, scipy, matplotlib, openpyxl, pandas
python3 code/parse_db.py       # ~1 s
python3 code/fit_models.py     # ~5 s
python3 code/let_compression.py
```

Headline numbers from the smoke run (see `results/fit_summary.json`):

| Quantity                                                | Value |
| ------------------------------------------------------- | ----- |
| Datasets parsed                                         | 101   |
| (dose, SF) data points                                  | 1020  |
| LQ-fit-vs-published, median \|relative diff\| α         | 0.19  |
| IR-fit-vs-published, median \|relative diff\| α_s, α_r, D_c | ≈0.11 |
| Datasets where IR beats LQ (ΔAICc > 4, HRS-shaped)      | 40/98 (~41%) |
| High-LET datasets with parseable LET                    | 9     |
| Low-LET photon datasets                                 | 51    |

---

## What this replication *can* and *cannot* claim

### Can (re-)produce on this machine in seconds

1. The Polgár 2022 cohort itself, structured into tidy CSV.
2. LQ and Induced-Repair fits to all 101 curves.
3. The classic HRS-IRR signature for the original Lambin 1993 HT29 study
   (id=1) and many others.
4. Statistical evidence (ΔAICc histogram) that the IR model is preferred over
   LQ in a substantial subset of the cohort.

### Cannot reproduce without additional work

5. **The MML model itself** is not in this dataset. The paper *derives* an
   analytical MML formulation; reproducing that requires the article body
   (paywalled) for equations and parameter conventions.
6. **The MML×LEM composition for ion data** requires (a) an LEM
   implementation (e.g. GSI's LEM IV) and (b) the helium/carbon ion survival
   data used for validation. Neither is in this dataset.
7. **The "93-curve" published filtering rule** isn't documented in the
   abstract; the exact subset selection would need the article body.

A modest follow-up could:

- Implement the MML model from prior Madas group publications (none Polgár-authored
  in S2 results yet — would need a literature search behind the paywall or via
  related Madas papers).
- Wire up an existing open LEM (e.g., the LEM-style scoring layer in PARTRAC
  or libamtrack) and reproduce the ion validation slice.

Estimated additional effort: 1–3 days of focused work plus author-supplied
clarifications. **No author contact requested in this pass per task spec.**

---

## License notes

- The Polgár 2022 STOREDB dataset is CC-BY-4.0 — redistribution permitted
  with citation. The cached copies in `data/` carry that license.
- The Sennhenn 2026 paper itself is copyright Radiation Research Society;
  we only quote the openly-available abstract.
- This replication code is original work for the LUCID100 program.
