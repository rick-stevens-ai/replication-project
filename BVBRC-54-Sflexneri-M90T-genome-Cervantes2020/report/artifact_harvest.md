# Artifact Harvest — BVBRC-54 (S. flexneri 5a M90T)

## Paper (Open Access, CC BY 4.0)
- Title: *Complete genome sequence and annotation of the laboratory reference strain Shigella flexneri serotype 5a M90T and genome-wide transcriptional start site determination*
- Cervantes-Rivera R, Tronnet S, Puhar A. BMC Genomics 21:285 (2020).
- DOI: 10.1186/s12864-020-6565-5 · PMID 32252626 · PMC7132871
- Full text XML (Europe PMC): https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7132871/fullTextXML
  → saved to work/paper_fulltext.xml (215,470 bytes)

## Genome assembly (independently downloaded, NCBI Datasets REST v2alpha, no auth)
- Assembly: GCF_004799585.1 / GCA_004799585.1 (ASM479958v1), submitter **Umeå University**, released 2019-04-18, level **Complete Genome**.
- BioSample: SAMN10608416
- Download URL: https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_004799585.1/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF,SEQUENCE_REPORT
  → work/Sflex_M90T.zip (2,695,927 bytes)
- Replicons:
  - Chromosome: RefSeq **NZ_CP037923.1** / GenBank **CP037923.1** — 4,596,714 bp, GC 50.92%
  - Plasmid pWR100: RefSeq **NZ_CP037924.1** / GenBank **CP037924.1** — 232,195 bp, GC 45.68%
- Files:
  - GCF_004799585.1_ASM479958v1_genomic.fna (4,889,425 bytes; 2 sequences)
  - protein.faa (3,874 RefSeq proteins)
  - genomic.gff (RefSeq annotation)

## Tools run (all free, on uicgpu — 8×A100 node, conda envs)
- env bvbrc28: **prokka 1.12**, **datasets 18.32.0**, barrnap 0.9
- env bvbrc14: **abricate 1.4.0** (dbs: vfdb 4592, victors 4545, card 6052, resfinder 3206, ncbi 8232, plasmidfinder 488, ecoli_vf 2701 — all 2026-Apr-3), **amrfinder 4.2.7**, **mlst 2.33.1**

## Derived evidence files (report/evidence/)
- genome_stats_comparison.md — replicon/annotation table vs paper Tables 1 & 2
- virulence_T3SS_summary.txt — T3SS/effector reconstruction, AMR, plasmid type, MLST
- abricate_{vfdb,victors,card,ecoli_vf,plasmidfinder}.tsv — raw specialty-gene calls
- amrfinder.tsv — AMRFinderPlus raw output (25 rows: 1 AMR, 1 STRESS, 23 VIRULENCE)
- mlst.tsv — Achtman ST call
- prokka_stats.txt, prokka_features.tsv — independent re-annotation
