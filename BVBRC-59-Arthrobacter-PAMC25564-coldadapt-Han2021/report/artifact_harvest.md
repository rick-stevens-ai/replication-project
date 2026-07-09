# Artifact Harvest — BVBRC-59 (Arthrobacter sp. PAMC25564)

| Artifact | Source / URL | Accession | Size | Notes |
|---|---|---|---|---|
| Paper full text (JATS XML) | Europe PMC `PMC8171050/fullTextXML` | PMC8171050 | 165 KB | OA, BMC Genomics |
| Focal genome nucleotide FASTA | NCBI efetch nuccore | CP039290.1 (RefSeq NZ_CP039290.1) | 4,170,970 bp | PacBio Sequel / HGAP4 |
| Focal assembly report (GenBank) | NCBI Datasets v2 | GCA_004798705.1 | — | annotation PGAP 2019-04-11 (paper-contemporaneous) |
| Focal assembly report (RefSeq) | NCBI Datasets v2 | GCF_004798705.1 | — | re-annotated RS_2024_05_22 (drifted) |
| Focal proteome (protein FASTA) | NCBI Datasets v2 download | GCA_004798705.1 PROT_FASTA | 3,613 proteins / 1.48 MB | matches paper protein-coding count |
| Genome feature table | NCBI efetch (rettype=ft) | CP039290.1 | — | for rRNA/tRNA counts |
| dbCAN HMM database | pro.unl.edu/dbCAN2 | dbCAN-HMMdb-V9 | 99 MB (HMMER3) | closest available to paper's dbCAN2/V8 |
| CAZyme domtbl (hmmscan out) | computed on uicgpu | — | 261 KB | HMMER 3.4 |
| Comparator genomes (verified real) | NCBI esummary | CP040018.1, CP007595.1, CP017421.1, CP018863.1, CP002379.1, +others | — | sample of the 16–26 Arthrobacter/Pseudarthrobacter comparators |

## Key metadata
- BioProject: PRJNA531357  ·  BioSample: SAMN11356967
- Submitter: Korea Polar Research Institute  ·  Assembly: ASM479870v1
- Tax ID: 2565366 (Arthrobacter sp. PAMC25564), isolated from cryoconite (Antarctica)

## Compute
- hmmscan (HMMER 3.4, antismash conda env) on uicgpu01, 16 CPU, ~4 min, 3,613 proteins vs dbCAN-HMMdb-V9 (~700 HMMs).
- All genome/annotation stats: NCBI REST + local FASTA parse.
