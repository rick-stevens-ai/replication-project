# Data provenance — pediatric MB analog

## GEO

| Accession | File on uicgpu (/data/stevens/alter-pediatric-mb/data/) | Size | What | Used as |
|---|---|---|---|---|
| GSE85217 | `gse85217_exp.txt.gz` | 131 MB | Affymetrix HuGene 1.1 ST expression, 21 642 probes × 763 MB patients | D1 (expression layer) |
| GSE85217 | `gse85217_matrix.txt.gz` | 85 MB | Full GEO series matrix incl. expression + sample metadata | metadata only (header → `gse85217_meta.txt`) |
| GSE85217 | `gse85217_meta.txt` | derived | metadata header (65 lines, no expression) | per-sample subgroup labels |
| GSE85212 | `gse85212_meth_beta.txt.gz` | 2.0 GB | Illumina 450K methylation beta, 321 175 CpGs × 763 MB patients (one patient missing → 762 matched) | D2 (methylation layer) |
| GSE85212 | `gse85212_matrix.txt.gz` | 36 KB | Methylation series matrix | metadata header (`gse85212_meta.txt`) |

Both subseries of GSE85218 (SuperSeries, Cavalli et al. 2017 Cancer Cell, "Intertumoral
Heterogeneity within Medulloblastoma Subgroups"). Patient-matched on
`MB_SubtypeStudy_55XXX` IDs (methylation samples carry `_methylation` suffix).

Sample-level fields exposed in GEO:
- `tissue:` (always "medulloblastoma")
- `subgroup:` ∈ {WNT, SHH, Group3, Group4}
- `subtype:` ∈ {WNT_alpha/beta, SHH_alpha/beta/gamma/delta, Group3_alpha/beta/gamma, Group4_alpha/beta/gamma}
- (methylation only) `type: primary tumor`

**Not exposed by GEO:** per-sample OS_MONTHS / OS_STATUS / PFS / age / sex /
M-stage. Those are in the paper's paywalled Cancer Cell supplementary Table S1.

## cBioPortal

| Study ID | n patients | What used |
|---|---|---|
| mbl_icgc | 125 | Full clinical: SUBGROUP, OS_MONTHS, OS_STATUS, PFS_MONTHS, CLIN_M_STAGE, AGE, SEX, MUTATION_COUNT, HISTOLOGY, RADICALITY |
| mbl_sickkids_2016 | 46 | Secondary baseline: SUBGROUP, OS_MONTHS, OS_STATUS, M_STAGE, AGE, SEX |

Saved as JSON dicts (`{patient_id: {field: value}}`) in `mbl_icgc_clinical.json` and
`mbl_sickkids_2016_clinical.json`.

Pulled via the cBioPortal REST API endpoint
`https://www.cbioportal.org/api/studies/{sid}/clinical-data?clinicalDataType=PATIENT|SAMPLE`,
no auth required, free tier.

## Studies considered and rejected

| Source | Reason rejected |
|---|---|
| cBioPortal `mbl_dkfz_2017` (n=491) | Only mutations + SVs, no CN matrix, no OS in clinical attributes |
| cBioPortal `mbl_broad_2012` (n=92) | Mutations only |
| cBioPortal `mbl_pcgp` (n=37) | Mutations only |
| cBioPortal `brain_cptac_2020` (n=218 mixed pediatric brain) | Has CN+RNA+OS but only 22 MB samples in the mix — too small for cohort GSVD |
| TARGET-PBTA / OpenPedCan / Kids First | Survey-level metadata accessible, per-patient CN+RNA matrices require dbGaP/Kids First credentialed access (not open in the same sense as GEO/cBioPortal public) |
| Cavalli paper supplementary Table S1 (per-patient OS) | Cancer Cell paywalled; PMC marked "not open access" |

## Cohort sizes achieved

- FRONT 1 (real OS): mbl_icgc n=103 with valid OS; mbl_sickkids_2016 n=28 with OS
- FRONT 2 (GSVD on matched omics): Cavalli n=762 (expression × methylation intersection)
- F3 (Group3+Group4 restricted): n=470 (G3=144, G4=326)
