# Artifact Harvest

## Paper (open access)
- Europe PMC full-text XML: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7066406/fullTextXML`
  → `work/fulltext.xml` (112,688 bytes), plain text `work/fulltext.txt` (45,100 chars).
- DOI: 10.1155/2020/4109186 · PMID 32190639 · PMCID PMC7066406 · License CC-BY.

## Genome under study — *Priestia megaterium* NCT-2 (paper: *Bacillus megaterium* NCT-2)
- Assembly **GCA_000334875.3** (ASM33487v3, Complete Genome), downloaded via NCBI Datasets v2 REST
  (`include_annotation_type=GENOME_FASTA,GENOME_GFF,PROT_FASTA`).
  - `work/gca/.../GCA_000334875.3_ASM33487v3_genomic.fna` — 11 replicons.
  - `work/gca/.../genomic.gff` — 12,397 lines.
  - `work/gca/.../protein.faa` — 5,605 proteins.
  - zip md5: `e7271d82875dab90cf3ef2ec879af151`.
- Replicon accessions (match paper Data Availability exactly):
  - Chromosome CP032527.2
  - Plasmids pNCT2_1..pNCT2_10 = CP032528.1, CP032530.1, CP032531.1, CP032532.1, CP032533.1,
    CP032534.1, CP032535.1, CP032536.1, CP032537.1, CP032529.1.
- RefSeq equivalent GCF_000334875.3 (v.1 = old draft/contig; v.3 = the complete genome replacing draft).

## Comparator genomes (paper Table 1)
Downloaded via NCBI Datasets v2 REST (GENOME_FASTA):
- *Priestia megaterium* QM B1551 — **GCF_000025825.1** (NC_014019.1 + plasmids)
- *Priestia megaterium* DSM 319 — **GCF_000025805.1** (NC_014103.1)
- *Bacillus subtilis* subsp. subtilis 168 — **GCF_000009045.1** (NC_000964.3)
- *Bacillus cereus* Q1 — **GCF_000013065.1** (NC_011969.1)
- *Bacillus licheniformis* DSM 13 (= ATCC 14580) — **GCF_000011645.1** (NC_006270.3)

## Tools
- NCBI Datasets v2 REST API (free, no auth).
- Europe PMC REST (free).
- fastANI v (local, /usr/local/bin/fastANI) for ANI.
- Python 3 stdlib for FASTA/GFF parsing (no fabricated numbers; all derived from downloaded files).
