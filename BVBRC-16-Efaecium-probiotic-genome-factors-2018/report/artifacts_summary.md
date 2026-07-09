# Artifacts Summary — BVBRC-16 (Ghattargi 2018, *E. faecium* 17OM39 vs T110)

Everything produced by this replication pass lives under
`~/Dropbox/REPLICATE-PROJECT/BVBRC-16-Efaecium-probiotic-genome-factors-2018/`.

## `report/`

| File | Role |
|---|---|
| `REPORT.md` | Primary human-readable replication report. Verdict: **PARTIAL** (4/6 claims reproduced). Source of truth for all numbers cited below. |
| `REPORT.tex` | LaTeX version of the report with a dedicated GENUINE CRITIQUE section. Compiles with `pdflatex`. |
| `open_questions.json` | 5 genuinely open scientific questions raised by the replication (safe-strain genomic criteria, phenotypic-validation gap, clade B vs A, bile/acid/salt tolerance gene conservation, host-benefit assay design). Each has `{q, basis, next_steps}`. |
| `workflow.md` | Pipeline diagram + wall-clock/cost breakdown + what's needed to promote to full REPLICATED. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Structured analysis of what didn't reproduce (C5 MGE claim) and why. |

## `evidence/` (raw + derived data)

| File | Bytes-class | Content | Rows / notable numbers |
|---|---|---|---|
| `europepmc_ghattargi2018.json` | small | Europe PMC bibliographic record for the paper (DOI, PMID 30180794, PMCID PMC6122445). | 1 record |
| `bvbrc_17OM39_strain.json` | small | BV-BRC genome metadata for 17OM39 (`1352.1047`). | assembly GCF_001652715.1, 2,840,201 bp, 106 contigs, BioProject PRJNA318315 |
| `bvbrc_T110_probiotic_strain.json` | small | BV-BRC genome metadata for T110 (`1344042.3`). | assembly GCA_000737555.1, 2,737,963 bp, finished + 44 kb plasmid `1344042.14` |
| `sp_gene_1352.1047.json` | medium | Full BV-BRC `sp_gene` table for 17OM39 (CARD + NDARO + PATRIC + VFDB + Victors + transporters + drug targets + metal resistance). | 158 rows; 56 AMR (18 CARD, 3 NDARO, 35 PATRIC); 18 VF; 0 `van*`; 0 `tet*` |
| `sp_gene_1344042.3.json` | medium | Same for T110 chromosome. | 148 rows; 52 AMR (14 CARD, 3 NDARO, 35 PATRIC); 19 VF including Cna; 0 `van*`; 0 `tet*` |
| `sp_gene_1344042.14.json` | small | Same for T110's 44 kb plasmid. | included for completeness |
| `sp_gene_summary.json` | small | Derived AMR/VF roll-up across both genomes. | machine-readable summary of §4.2, §4.3 of REPORT.md |
| `features_1352.1047.json` | large | Full CDS feature dump for 17OM39. | **5,776 CDS** |
| `features_1344042.3.json` | large | Full CDS feature dump for T110 chromosome. | **5,173 CDS** |
| `feature_scan_summary.json` | small | Derived MGE + AMR + probiotic-VF keyword counts (basis of §4.4, §4.5 of REPORT.md). | 17OM39: 237 MGE-like CDS (4.10%); T110: 87 (1.68%); ratio 2.72× |

## Key numbers (single-glance table, all from REPORT.md)

| Metric | 17OM39 (`1352.1047`) | T110 (`1344042.3`) | Paper predicts | Reproduced? |
|---|---|---|---|---|
| Genome length | 2,840,201 bp | 2,737,963 bp | ~2.8 Mb both | ✅ |
| Contigs | 106 (draft) | 1 chr + 1 plasmid (finished) | as stated | ✅ |
| Total CDS | 5,776 | 5,173 | — | reference |
| Total `sp_gene` rows | 158 | 148 | — | reference |
| AMR rows | 56 | 52 | — | reference |
| `van*` hits (any) | **0** | **0** | 0 | ✅ |
| `tet*` hits (canonical) | **0** | **0** | 0 | ✅ |
| `tet*` hits (MFS efflux borderline) | 1 | 0 | 0 | minor caveat |
| Acquired AMR (excl. intrinsic) | Lsa(A) + Msr(C) — intrinsic to sp. | same | 0 acquired | ✅ |
| VF rows | 18 | 19 | 17OM39 lacks functional VF | ✅ |
| Collagen adhesin `Cna` | **0** | **1** | 17OM39 lacks | ✅ (17OM39 cleaner than T110) |
| Bile salt hydrolase | 3 | 3 | present | ✅ |
| Bacteriocin / enterocin | 9 | 13 | present | ✅ |
| Sortase A (LPxTG) | 13 | 9 | present | ✅ |
| Transposase CDS | 66 | 21 | 17OM39 fewer | ❌ opposite |
| Total MGE-like CDS | 237 (4.10%) | 87 (1.68%) | 17OM39 fewer | ❌ opposite (draft/finished confound) |

## Not produced this pass (would be new artifacts on a full REPLICATED pass)

| Artifact | Tool | Purpose |
|---|---|---|
| `roary/gene_presence_absence.csv` + `roary/core_gene_alignment.aln` + `roary/tree.nwk` | prokka + roary + FastTree | Test C6 (17OM39 clusters with T110). |
| `isescan/<strain>.gff` for all 4 strains | ISEScan | Fair, contig-break-safe MGE count → re-test C5. |
| `abricate_resfinder.tsv` + `abricate_vfdb.tsv` | abricate | DB-version-exact AMR + VF confirm of C3/C4. |
| Pathogenic comparator arm (`sp_gene` + `features` JSONs for Aus0004 / TX16 / DO) | BV-BRC | Fair MGE baseline for C5. |
| Clade assignment (`mlst.tsv`, `fastANI.tsv`, `lebreton_snps.tsv`) | mlst + fastANI | Strengthens C6 with clade A vs B call. |

## Provenance

- Analyst: Ollie (OpenClaw AI)
- Original spot-check pass: 2026-06-17
- Promotion pass to PARTIAL: 2026-06-25
- Backfill pass (this file + REPORT.tex + open_questions.json + workflow.md + failure_analysis.md): 2026-07-05
- All API pulls: Europe PMC + BV-BRC public endpoints, unauthenticated, free.
- Every number cited above is derived from `evidence/*.json` in this same directory. `jq .` on those files will reproduce the counts.
