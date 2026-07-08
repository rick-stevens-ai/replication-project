# Fetching TARGET-NBL data for the Alter et al. 2026 GSVD replication

This is a **concrete recipe**, not a download script. The goal is to get
us as close as possible to the paper's three datasets from public sources,
and to call out precisely what is **not** reconstructable from GDC and
therefore needs Datasets 1–3 from the corresponding author.

The paper's data definitions (from the Data Availability statement and
Sec. III/IV):

* **Dataset 1 — discovery, X = 101 patients.** Patient-matched tumor +
  blood WGS profiles from Complete Genomics sequencing, expressed as
  **log2 of CG read counts in Z1 = 2,831,960 (tumor) / Z2 = 2,831,959
  (blood) nonoverlapping 1 K-nucleotide bins** spanning autosome + X of
  hg19, each profile **centered at its autosomal median**. Plus tumor
  RNA-Seq profiles of 71 of those patients (log2 of Illumina HiSeq 2000
  RNA read counts, Z3 = 15,393 transcripts).
* **Dataset 2 — validation, Y = 419 patients.** Tumor + blood WGS from
  Illumina HiSeq 2500, in the Z1 = 10,354 / Z2 = 10,475 bins **shared**
  with the discovery WGS tumor/blood bins.
* **Dataset 3 — GSVD-derived CBS segments and CNA labels** for the
  tumor-DNA-specific patterns u1,1, u1,100, u1,101.

## 1. The GDC project: `TARGET-NBL`

* **Portal:** <https://portal.gdc.cancer.gov/projects/TARGET-NBL>
* **Project ID:** `TARGET-NBL`
* **Primary site:** nervous system (neuroblastoma)
* **Programs:** TARGET (Therapeutically Applicable Research to Generate
  Effective Treatments).

As of mid-2026 the GDC carries ~1,070 NBL cases (TARGET-NBL =
~1,127 cases) across multiple data categories. The Alter et al. cohort
is the 101-patient WGS subset (discovery) + 419-patient WGS subset
(validation), plus the 71-patient RNA-Seq slice. **Both WGS slices**
are controlled access (dbGaP); the Illumina RNA-Seq counts are partly
open via the GDC Data Portal's "Transcriptome Profiling" category.

### dbGaP accession (controlled-access)

* **phs000218** — TARGET: Therapeutically Applicable Research to Generate
  Effective Treatments. This is the parent study; the NBL substudy is
  **phs000467** (TARGET-NBL).
* WGS and the matched-normal blood data live under phs000467 and require
  an approved dbGaP DAC request (NHGRI). The Alter paper used CG WGS
  (discovery) and Illumina HiSeq 2500 WGS (validation); both are listed
  in phs000467.
* RNA-Seq from Illumina HiSeq 2000 (the 71-patient subset) is part of
  TARGET-NBL Phase II Transcriptome and is partly open / partly
  controlled depending on grain.

## 2. GDC API queries

Replace the API base with `https://api.gdc.cancer.gov`. All queries
return JSON; add `&size=10000` for full lists.

### a. All TARGET-NBL cases

```
GET https://api.gdc.cancer.gov/cases?
    filters={"op":"in","content":{"field":"project.project_id","value":["TARGET-NBL"]}}
    &fields=case_id,submitter_id,disease_type,demographic.vital_status,
            diagnoses.age_at_diagnosis,diagnoses.tumor_stage,
            diagnoses.days_to_death,diagnoses.days_to_last_follow_up,
            diagnoses.classification_of_tumor
    &size=2000
```

This pulls survival metadata (`days_to_death`, `days_to_last_follow_up`,
`vital_status`) and INSS stage / age at diagnosis — these are the
covariates compared in the paper's Table I.

### b. WGS BAMs (controlled)

```
GET https://api.gdc.cancer.gov/files?
    filters={"op":"and","content":[
        {"op":"in","content":{"field":"cases.project.project_id","value":["TARGET-NBL"]}},
        {"op":"in","content":{"field":"experimental_strategy","value":["WGS"]}},
        {"op":"in","content":{"field":"data_format","value":["BAM"]}}
    ]}
    &fields=file_id,file_name,file_size,cases.submitter_id,
            cases.samples.sample_type,platform
    &size=5000
```

`platform` will separate Complete Genomics (discovery) from Illumina
HiSeq 2500 (validation). `cases.samples.sample_type` distinguishes
"Primary Tumor", "Recurrent Tumor", "Blood Derived Normal", etc. Need
the BAMs + a dbGaP-approved download token to use `gdc-client download`.

### c. RNA-Seq counts (mixed open / controlled)

```
GET https://api.gdc.cancer.gov/files?
    filters={"op":"and","content":[
        {"op":"in","content":{"field":"cases.project.project_id","value":["TARGET-NBL"]}},
        {"op":"in","content":{"field":"data_category","value":["Transcriptome Profiling"]}},
        {"op":"in","content":{"field":"data_type","value":[
            "Gene Expression Quantification",
            "Aligned Reads"
        ]}}
    ]}
    &fields=file_id,file_name,access,experimental_strategy,
            cases.submitter_id,analysis.workflow_type
    &size=5000
```

`access = "open"` files (HTSeq/STAR counts, FPKM, FPKM-UQ) are
downloadable without dbGaP. `access = "controlled"` covers the raw BAMs.

## 3. Mapping the paper's pre-processed profiles onto GDC data

This is the **honest limitation** of the public-only path.

| Paper's profile | Public reconstruction from GDC | Gap |
|---|---|---|
| Tumor WGS, Z1 = 2,831,960 1-kb bins of CG read counts, log2, centered at autosomal median | Need CG BAMs from phs000467 + a custom 1-kb autosomal+X binning of read counts. CG sequencing has been retired; the BAMs (if hosted) come from the original CG pipeline. Recompute log2(counts+1), then subtract per-profile autosomal median. | The exact bin coordinate set (which 2,831,960 specific 1-kb intervals over hg19 autosome+X were used after masking) is **not specified in the paper**. Even with identical raw reads, the bin set is ambiguous: there are ~2.88M nonoverlapping 1-kb bins covering hg19 chr1-22+X, so the masking step that drops ~50K bins is paper-internal. Dataset 1 fixes this exactly. |
| Blood WGS, Z2 = 2,831,959 1-kb bins | Same as above for matched-normal BAMs. | One fewer bin than tumor — probably one bin masked in the blood track. Need Dataset 1 to identify it. |
| Validation tumor WGS, Z1 = 10,354 bins / blood Z2 = 10,475 bins (Illumina HiSeq 2500) | Public HiSeq 2500 NBL WGS BAMs exist on GDC; need to recompute per-bin counts in the shared bin subset. | The shared bin set itself (which 10,354 / 10,475 specific bins survived in the validation platform) is paper-internal. Dataset 2 is required. |
| Tumor RNA, Z3 = 15,393 transcripts, log2 HiSeq 2000 counts | GDC carries TARGET-NBL HTSeq counts (Ensembl gene ids) — about 60K rows. The paper kept Z3 = 15,393, so a transcript-filter step (likely: keep transcripts with detectable expression across the 71-patient subset; the exact threshold is not in the methods). | The 15,393-transcript whitelist needs to be derived or — better — taken directly from Dataset 1. |

## 4. Recommended order of operations

1. **Email Orly Alter (orly@sci.utah.edu)** and request Datasets 1, 2, 3
   plus Mathematica Notebook 1 PDF. She offers them on request and
   thanked Rick in the paper, so this is the high-value, low-effort path.
   *(See `../draft-email-to-orly.md`.)*
2. While waiting, pull from GDC (no dbGaP needed):
   * TARGET-NBL clinical / survival metadata (above query a) — survival
     times, INSS stage, age, MYCN status, COG risk, MKI, ploidy,
     histopathology. **This alone lets us regenerate everything in Table I
     for the standard-of-care comparators** (MYCN, INSS, age, ...) once
     we know the 90 / 101 / 419-patient barcode lists.
   * Open-access RNA-Seq counts (above query c with `access=open`) for
     all NBL cases. We can compute log2 counts and stand by for the
     71-patient barcode list to subset.
3. Apply dbGaP DAC for phs000467 only if Orly's Dataset 1/2 doesn't
   materialize. Allow 6–10 weeks for approval; then download BAMs via
   `gdc-client download -t <token> -m manifest.txt` (manifest from
   query b).
4. With Datasets 1–2 in hand, the replication is purely the math:
   * Build D1 (tumor WGS, m1 = 2,831,960, n = 101), D2 (blood WGS,
     m2 = 2,831,959, n = 101).
     **Memory note:** D1 alone is ~2.3 GB float64. CherryRd can hold it,
     but the GSVD step needs the (m1 + m2) x n stacked QR. With our
     `gsvd_reference.gsvd`, scipy's QR uses LAPACK `dgeqrf` — the
     dominant cost is O((m1 + m2) n^2) ≈ 5.7e10 flops, manageable in a
     few minutes on CPU. The R = QR factor is only n x n = 101 x 101, so
     the subsequent SVD is trivial.
   * Run `gsvd(D1, D2)`. Extract `k_first` and `k_last`
     antisymmetric arraylets (V[:, k_first], V[:, k_last]).
   * `classify_patients` on each, then `combine_predictors` -> 3-class
     "Tumor DNA 1+101".
   * Feed (survival_time, event, classifier) into `survival_stats.report`
     and compare to Table I.

## 5. What we cannot get without Dataset 1

* The **exact bin coordinate set** for the 2,831,960 / 2,831,959 tumor /
  blood 1-kb bins. Without it, our `D1`, `D2` will not be in the same
  feature ordering as the paper's, so the GSVD's `V[:, k]` arraylets
  will not numerically equal `u1,1` and `u1,101` even if the math is
  identical.
* The **autosomal-median centering vector** that was subtracted from each
  profile. We can recompute it from raw CG counts, but only after
  resolving the bin set above.
* The **71-patient transcript whitelist** of 15,393 transcripts.

These are the items that make Dataset 1 from the author the unambiguous
critical path; everything else in the math + survival pipeline is
already implemented and tested in this repo.
