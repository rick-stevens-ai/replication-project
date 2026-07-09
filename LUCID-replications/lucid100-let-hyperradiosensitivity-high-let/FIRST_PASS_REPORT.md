# FIRST PASS REPORT — LUCID100 Wave 3 / Slot 21

**Paper.** Sennhenn et al. 2026, *Radiation Research* 205(5):472–483.
DOI: [10.1667/rade-25-00194](https://doi.org/10.1667/rade-25-00194). PMID 41651140.
**Worktype tag (master TSV).** `omics/signature replication`.
**This-pass date.** 2026-06-09 (Tue) America/Chicago.

---

## Verdict

> **KEEP and re-tag.** Replication-plausible **with caveats**. Retag worktype
> from `omics/signature replication` → **`computational model / dose-response`**
> (closer fit; the work is a biophysical-model paper, not an omics study).

A meaningful **smoke replication of the underlying dataset + classical LQ and
Induced-Repair (IR) survival models** runs end-to-end on this machine in
under 10 seconds and is checked in to `code/` and `results/`. The paper's
**proprietary contributions** — analytical MML formulation, MML×LEM coupling,
LET-compression demonstration on helium/carbon ions — are **not** reproducible
in this pass because (a) the article body is paywalled (no preprint, no OA
license, no PMC mirror) and (b) the ion validation dataset and LEM
implementation are not bundled.

---

## Legitimacy / accessibility check

| Check                                  | Result                                         |
| -------------------------------------- | ---------------------------------------------- |
| Paper exists, Crossref-resolvable      | ✅ DOI 10.1667/rade-25-00194 → Radiat Res 205(5) |
| PubMed indexed                         | ✅ PMID 41651140, May 2026 publication        |
| Authors verifiable                     | ✅ Sennhenn (TU Darmstadt-style); Polgár & Madas (Hungarian Academy / EK MTA), Friedrich (GSI) — long-standing radiobiology modelling groups |
| Open access                            | ❌ Unpaywall says no OA copy                  |
| Preprint                               | ❌ No arXiv/bioRxiv/Europe PMC preprint       |
| Supplementary materials                | ❌ Not visible on landing page (likely with paywalled article) |
| **Underlying curated dataset, open?**  | ✅ **Yes** — Polgár 2022 STOREDB DATASET1252, CC-BY-4.0 |
| **Code repository**                    | ❓ Authors point to a GitHub org (`Radiobiology-Informatics-Consortium`) in the *prior* dataset paper, but no repo specifically for the LET/MML model has been identified via S2/Crossref search |
| Paid endpoints needed for first pass   | ❌ No — all artifacts harvested for free       |
| Author contact required for first pass | ❌ Skipped per task spec                       |

**Conclusion:** legitimate, traceable, replication-relevant, but the *novel
modelling* portion is gated by the paywall. The dataset infrastructure is
fully open, which is what enables a substantive first pass.

---

## Artifact harvest

**4 primary artifacts** retrieved from STOREDB (CC-BY-4.0; see
`ARTIFACT_MANIFEST.tsv` for full sha256s):

```
data/database_v2.xlsx                       272514 B  ec57277…  STOREDB FILE12933
data/database_v1.xlsx                       237052 B  6ff9a0e…  STOREDB FILE12921
data/study_and_dataset_description_v2.pdf   148119 B  59f08c4…  STOREDB FILE12935
data/study_and_dataset_description_v1.pdf   152887 B  0a6ee6a…  STOREDB FILE12923
```

After parsing (`code/parse_db.py`):

```
results/curves_long.csv      1020 (dose, SF, SF_min, SF_max) rows
results/curves_meta.csv      101 datasets × {LQ, IR} published params + metadata
```

The 101-dataset count matches Polgár 2022's documented `v2` content (46
articles, 1993–2021), and includes 7 candidate high-LET entries (V79
α-particles, V79 100 MeV/u carbon, SMMC-7721 12C, GM0639 carbon ion, 14.1 MeV
neutrons, 50 MeV/u ions @ 45.2 keV/μm, AT-derived fibroblasts @ 70 keV/μm).

---

## Minimal replication that runs

Three small scripts (~17 KB total Python, dependencies: numpy, scipy,
matplotlib, openpyxl):

1. **`code/parse_db.py`** — Excel → tidy CSV. ✅
2. **`code/fit_models.py`** — bounded `scipy.optimize.curve_fit` for the
   classical LQ model `S(D) = exp(-(αD + βD²))` and the Joiner–Marples
   Induced-Repair model
   `S(D) = exp(-α_r D · (1 + (α_s/α_r − 1) exp(-D/D_c)) − β D²)`,
   plus AICc-based model selection. ✅
3. **`code/let_compression.py`** — exploratory plot of IR `D_c` and
   `α_s/α_r` vs LET (with photons placed at nominal 2 keV/μm). ✅

### Quantitative outputs (full numbers in `results/fit_summary.json`)

- **All 101 curves fit successfully** under both models.
- **Reproduction of *published* IR parameters** (when reported in the source
  Excel): median |relative difference| ≈ **11%** for `α_r`, `α_s`, `D_c`
  (n=57, 59, 66 datasets, respectively). This is well inside what one
  expects from an independent re-fit of digitized survival data.
- **HRS-IRR signature detected** (IR meaningfully better than LQ by
  ΔAICc > 4 *and* `α_s > 1.5 α_r` *and* `D_c < 1 Gy`) in **40 of 98** (41%)
  curves. The well-known landmark studies — Lambin 1993 HT29 (id=1, ΔAICc
  25.2, `α_s/α_r ≈ 19`, `D_c ≈ 0.19 Gy`) and Marples & Joiner V79 (id=5,
  ΔAICc 35.6, `α_s/α_r ≈ 29`, `D_c ≈ 0.37 Gy`) — appear at the top of the
  ranking, which is a strong sanity check.
- **Cohort-level histogram** (`figures/delta_aicc_histogram.png`) shows a
  clear right-tail population of HRS-positive curves.

### Where the smoke replication cannot reach the paper's headline result

The paper claims "progressive compression of HRS with increasing LET". We
attempted this empirically (`code/let_compression.py`):

| Median IR parameter (LET subset)                | low-LET photons (n=51) | high-LET (n=9) |
| ----------------------------------------------- | ---------------------- | -------------- |
| HRS transition dose `D_c` [Gy]                  | 0.184                  | 0.220          |
| HRS amplitude `α_s/α_r`                         | 11.6                   | 11.0           |

Direction is essentially flat in this slice, **as expected**: the public
dataset is heavily photon-dominated, and the paper's LET-compression result
relies on **external helium/carbon ion data not bundled with STOREDB**.
Reproducing it would require either (a) the article body for the cited ion
datasets or (b) author contact for the validation set. Both are out of scope
for this first pass.

---

## Heavy-compute job plan

**Not required.** Total CPU time for end-to-end repro is < 10 s on
CherryRd (single core). No GPU, no MPI, no scheduler involvement. The
artifact pack is < 1 MB.

If a full MML+LEM rebuild were later commissioned, the natural compute
target would be a small Aurora or uicgpu job for the LEM Monte Carlo
component (one-time, hours-scale), with the MML fit again being trivial
CPU work. No job plan written this pass.

---

## Blockers

1. **Paywall** on the article body. Blocks: exact analytical MML formula,
   exact ion validation dataset, exact 93-curve filter rule.
2. **No public code from authors** for this specific MML / MML×LEM
   computation (Polgár 2022 Sci Data says "no custom code was used to
   generate the database"; the *modelling* paper might cite a github repo
   inside the paywalled body — not visible here).
3. **High-LET coverage in STOREDB v2 is limited** (~7 datasets). The
   paper's headline LET-compression curve cannot be checked from public data
   alone.

None of these are show-stoppers for *scoping* a fuller replication; they
just bound what a no-author-contact / no-paid-endpoint first pass can claim.

---

## Next actions (recommended)

1. **Retag** master TSV row 52 worktype: `omics/signature replication` →
   `computational model / dose-response`. (Hand-off note for QA pass.)
2. **(Optional, later)** Pull the article body via an institutional
   subscription (Argonne library / RRS member access) to extract:
   - the exact analytical MML equation;
   - the curated 93-curve subset list;
   - the helium / carbon ion validation datasets and their references.
   Then extend `code/` with an MML implementation and an LEM-style RBE layer.
3. **(Optional)** Approach the authors for the MML code and ion validation
   set (Madas group, BME / EK MTA Hungary). Not done this pass per spec.
4. **(Optional)** Cross-link this folder from the LUCID100 Wave 3 progress
   ledger; the dataset cache here is reusable for several other HRS / IR-model
   replications in the master TSV (e.g. Pariset, Mariotti, Patra, etc.).

---

## Files written this pass

See `ARTIFACT_MANIFEST.tsv`. 4 downloaded artifacts + 3 scripts + 10 derived
files + 3 narrative docs (this report, README.md, PROGRESS.md). Total folder
size ≈ 1.2 MB.


## Verdict

**Verdict: PARTIAL** (Coverage 5/10, Agreement 7/10). — Reproduced 101-curve LQ/IR fits to ~11% vs published params; paywalled LET-compression headline not reachable

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
