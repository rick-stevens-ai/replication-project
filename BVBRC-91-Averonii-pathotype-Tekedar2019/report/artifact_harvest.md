# BVBRC-91 — Artifact Harvest

## Bibliographic / OA
- Europe PMC full-text XML (255,866 bytes): `work/fulltext.xml` — PMC6715197, PLoS ONE, CC BY 4.0.
- ID resolution (`work/pmid_lookup.json`): PMID 31465454 ↔ PMCID PMC6715197 ↔ DOI 10.1371/journal.pone.0221018.

## Genomes downloaded via NCBI Datasets REST (free, no auth)

| Strain | Paper accession (2019) | BV-BRC genome_id | NCBI Assembly | Local path (relative to `work/`) |
|---|---|---|---|---|
| ML09-123 (USA, catfish, this-study) | PPUW01000001 | 654.112 | GCA_002906945.1 (ASM290694v1) | `genomes/GCA_002906945.1_dir/…/GCA_002906945.1_ASM290694v1_genomic.fna` |
| TH0426 (China, yellowhead catfish) | NZ_CP012504.1 | 654.45  | GCA_001593245.1 (ASM159324v1) | `genomes/GCA_001593245.1_dir/…/GCA_001593245.1_ASM159324v1_genomic.fna` |

Local file sizes: 4,816,369 B (ML09-123, 32 contigs) and 4,984,608 B (TH0426, 1 contig).

## BV-BRC Specialty-Gene API pulls

- `work/sp_gene_654.112.json` — 399 rows, ML09-123.
- `work/sp_gene_654.45.json` — 705 rows, TH0426.
- `work/sp_gene_654.48.json` — 465 rows, AVNIH1 (GCA_001634325.1) as T3SS/T6SS-negative control.
- `work/bvbrc_test.json`, `work/bvbrc_count.json` — sanity check of BV-BRC API + total *A. veronii* genome count (**726 as of 2026-07-04**, vs 41 used in 2019 paper).

## 41-strain paper-panel BV-BRC lookup
- `work/paper_strain_bvbrc_lookup.json` — 34/41 strains resolved via exact strain-name match against `taxon_id=654`; the 7 unmatched (AER39, LMG 13067, AMC35, CECT 4257, CCM 4359, B565, AER397) are still available in NCBI/BV-BRC under either (a) different strain-catalog aliases or (b) a separate strain-level taxon ID (e.g., B565 → taxon 998088, GCF_000204115.1, verified 2026-07-04). Effective availability = 41/41.

## Analysis tools used (versions)
- `fastANI` v1.34+ (system `/usr/local/bin/fastANI`) — pairwise ANI via mash-mash-style fragment mapping.
- `skani` v0.2+ (system `/usr/local/bin/skani`) — ANI via sparse chaining (learned-ANI mode default).
- `nucmer` v4 (available; not used in this pass — fastANI + skani suffice for cross-check).
- Python 3 stdlib (json/urllib) for BV-BRC + NCBI Datasets REST.

## Output evidence files
- `report/evidence/fastani_ML_vs_TH.txt` — forward ANI query.
- `report/evidence/fastani_TH_vs_ML.txt` — reverse ANI query.
- `report/evidence/skani_ML_vs_TH.txt` — skani ANI query.
- `report/evidence/genome_stats.txt` — computed genome-stat table for ML09-123 and TH0426.
- `report/evidence/sp_gene_summary.txt` — Specialty-Gene source/property breakdowns for the three test genomes.
