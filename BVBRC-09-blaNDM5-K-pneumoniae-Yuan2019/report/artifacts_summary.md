# Artifacts Summary — Yuan et al. 2019 Replication (BVBRC-09)

## Source paper

- **Citation:** Yuan Y, Li Y, Wang G, Li C, Chang Y-F, Chen W, Nian S, Mao Y, Zhang J, Zhong F, Zhang L. *blaNDM-5 carried by a hypervirulent Klebsiella pneumoniae with sequence type 29.* Antimicrob Resist Infect Control. 2019;8:140.
- **DOI:** 10.1186/s13756-019-0596-1
- **PMID:** 31452874
- **PMC:** PMC6701021
- **PDF:** `paper.pdf` (3,087,068 bytes, sha256 `204f058d324790ee989f89629bd54778c6712df94f51129a69b52a70c7e27906`)
- **License:** CC-BY 4.0 (Open Access)

## Extraction (item 2 & 3)

| Artifact | Path | Size | Method | Status |
|---|---|---|---|---|
| Marker parse | `extraction/marker.md` | ~486 lines | pdftotext -layout (fallback; canonical Marker parse not found in central SCOUT/OSTI corpus by paper sha256) | present |
| Nougat parse | `extraction/nougat.mmd` | placeholder stub | GPU-required; deferred to next central corpus sweep. Stub contains sha256 and DOI for later resolution. | pending |

## Public data pulled (from NCBI RefSeq / GenBank)

| Accession | Description | Local file | Size |
|---|---|---|---|
| GCF_008320705.1 | Complete K. pneumoniae SCNJ1 genome (RefSeq assembly) | `data/SCNJ1_complete.fasta` | 5,526,578 bytes |
| NZ_CP174529.1 | SCNJ1 chromosome | `data/SCNJ1_chromosome.fasta` | 5,265,612 bytes |
| NZ_CP174530.1 | pVir-SCNJ1 (virulence plasmid) | `data/SCNJ1_pVir.fasta` | 214,974 bytes |
| NZ_CP174531.1 | pNDM5-SCNJ1 (resistance plasmid) | `data/SCNJ1_pNDM5.fasta` | 45,992 bytes |
| KF220657 | pNDM_MGR194 (comparator IncX3 plasmid, India) | `data/pNDM_MGR194.fasta` | 47,004 bytes |
| NC_005249 | pLVPK (comparator virulence plasmid, K1 KpVP-1 ref) | `data/pLVPK.fasta` | 222,594 bytes |
| NZ_CP031258 | pL22-1 (comparator virulence plasmid, K. quasipneumoniae) | `data/pL22_1.fasta` | 215,761 bytes |
| GCA_001630805 | SCLZ15-011 (paper's stated closest relative) | `data/ref_SCLZ15-011.fasta`, `data/ref_sclz_MCWA010000*.fasta`, `data/ref_sclz15.zip` | 5,682,039 + fragments |
| (59 ST29 assemblies) | Phase-2 phylogeny cohort | staged on chiatta00 | (not in Dropbox copy) |
| (231 IncX3 plasmids) | Phase-2 IncX3 cohort | staged on chiatta00 | (not in Dropbox copy) |

## Primary in-silico evidence (item 6 outputs)

| Artifact | Path | Size (bytes) | sha256 (first 16) | Interpretation |
|---|---|---|---|---|
| Kleborate output | `analysis/kleborate/klebsiella_pneumo_complex_output.txt` | 4,461 | 0bf30f8d2d934d85 | ST29; K54; virulence=4; resistance=2; ybt9-ICEKp3; iuc1; iro1; rmp1-KpVP-1 |
| ABRicate ResFinder | `analysis/abricate_resfinder.tsv` | 1,140 | 7f81940a24c95fd5 | blaNDM-5 on pNDM5 100%; blaSHV-187 chromosome 100%; oqxA/B chromosome ~99%; fosA6 chromosome 99.29% |
| ABRicate VFDB | `analysis/abricate_vfdb.tsv` | 26,573 | 09ec7e2188d056e1 | Full ybt / ent / mrk / iuc / iro / rmp clusters detected, 98-100% identity |
| ABRicate PlasmidFinder | `analysis/abricate_plasmidfinder.tsv` | 586 | 50c39afaf5dc1348 | IncX3 on pNDM5-SCNJ1; repB_KLEB_VIR + RepB_1_pC39 on pVir-SCNJ1 |
| BLAST pNDM5↔MGR194 | `analysis/blast_pNDM5_vs_MGR194.txt` | 874 | a65b44fd74d58ddc | 100% coverage, 99.99% identity (matches paper) |
| BLAST pVir↔pLVPK | `analysis/blast_pVir_vs_pLVPK.txt` | 5,224 | 775fb56cf8bde8de | 94% qcovs, 99.58% identity (paper: 93%, 99.71%) |
| BLAST pVir↔pL22-1 | `analysis/blast_pVir_vs_pL22.txt` | 6,004 | 2a97dfcaf98e9258 | 99% qcovs, 99.73% identity (paper: 99%, 99.99%) |

## Phase-2 phylogeny artifacts

| Artifact | Path | Size | Notes |
|---|---|---|---|
| ST29 Parsnp tree (initial) | `analysis/phylogeny/st29/parsnp.tree` | 3,726 B | 60-taxon core-genome tree |
| ST29 Gubbins filtered SNPs | `analysis/phylogeny/st29/st29_gubbins.filtered_polymorphic_sites.fasta` | 405,052 B | 6,731 sites retained; 368,803 bp of recombinant regions masked |
| ST29 Gubbins recomb GFF | `analysis/phylogeny/st29/st29_gubbins.recombination_predictions.gff` | 368,803 B | Per-branch recombination coordinates |
| ST29 Gubbins tree | `analysis/phylogeny/st29/st29_gubbins.final_tree.tre` | 2,339 B | Post-filter tree |
| ST29 RAxML best ML tree | `analysis/phylogeny/st29/st29_tree.raxml.bestTree` | 2,052 B | GTR+G best tree |
| ST29 RAxML bootstrap support | `analysis/phylogeny/st29/st29_tree.raxml.support` | 2,189 B | 100-bootstrap support values |
| ST29 final tree | `analysis/phylogeny/st29/st29_final.nwk` | 2,189 B, sha256[16]=f23d6bb808bb4cb8 | Deliverable ML tree with bootstrap support |
| ST29 SNP distances from SCNJ1 | `analysis/phylogeny/st29/snp_distances_from_SCNJ1.json` | 5,190 B | Closest 3: GCA_003286975 (33), GCA_002845925 (38), GCA_002870985 (38); SCLZ15-011 = 53 SNPs |
| IncX3 Mash NJ tree | `analysis/phylogeny/incx3/incx3_mash_nj_v2.nwk` | 8,018 B, sha256[16]=d27ff5094b3e46a7 | 231-plasmid NJ tree from Mash distances (k=21, s=1000) |
| IncX3 OrthoFinder species tree | `analysis/phylogeny/incx3/SpeciesTree_rooted.txt` | 4,440 B | Protein-orthogroup-based species tree (Phase-2 alternative) |
| IncX3 analysis summary | `analysis/phylogeny/incx3/incx3_analysis_summary.json` | (small) | Closest neighbors of pNDM5-SCNJ1: KP776609 (0.000072), AP018141 (0.000119), MF547511, MH234502, CP028536 |
| IncX3 mash distance matrix | `analysis/phylogeny/incx3/mash_distances_v2.tab` | (staged on chiatta00 large) | Full 231x231 pairwise Mash matrix |

## Report artifacts (this backfill — items 4-8)

| # | Artifact | Path | Description |
|---|---|---|---|
| 4 | LaTeX report | `report/REPORT.tex` | Detailed section-by-section replication report with critique; compile with pdflatex |
| 5 | Open questions | `report/open_questions.json` | 5 deep open questions with basis + next_steps (also in REPORT.tex §Open Questions) |
| 6 | Workflow | `report/workflow.md` | Full narrative + tool inventory + effort estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | Honest gap analysis, shortcuts taken, tolerance hand-waving, closure plan |

Plus the pre-existing:
- `report/REPORT.md` — Phase-1+2 markdown report (Rick's original replication doc)
- `report/PROGRESS.md` — Phase-1 progress checklist
- `paper/paper_notes.md` — extracted quantitative claims

## Traces / logs

| Trace | Path | Type |
|---|---|---|
| ST29 RAxML checker log | `analysis/phylogeny/st29/st29_check.raxml.log` | RAxML-NG stdout |
| ST29 RAxML parse log | `analysis/phylogeny/st29/st29_parse.raxml.log` | RAxML-NG stdout |
| ST29 RAxML tree log | `analysis/phylogeny/st29/st29_tree.raxml.log` | RAxML-NG main run log |
| ST29 Gubbins log | `analysis/phylogeny/st29/st29_gubbins.log` | Gubbins main log |
| ST29 Parsnp checkpoint | `analysis/phylogeny/st29/checkpoint.txt` | Parsnp progress marker |
| BLAST DBs | `analysis/pL22_1_db.*`, `analysis/pLVPK_db.*`, `analysis/pNDM_MGR194_db.*` | BLAST+ makeblastdb output files (.nhr .nin .nsq .ndb .njs .not .ntf .nto) |

## Not-produced / missing (documented gaps)

- Raw sequencing reads (SPSD00000000 SRA reads) — never downloaded; would allow a fully-controlled re-assembly.
- CSI Phylogeny replicate run — never executed; the 198-vs-53 SNP discrepancy is unresolved.
- MK715436 vs NZ_CP174530.1 byte-level diff — never run; the +51 bp size difference is unexplained at the sequence level.
- rmpA2 frameshift coordinate localization — never localized to a nucleotide position; only detected as truncated.
- Central Marker parse — not found; using pdftotext fallback.
- Central Nougat parse — not generated (no GPU in backfill session); stub placeholder in `extraction/nougat.mmd`.
