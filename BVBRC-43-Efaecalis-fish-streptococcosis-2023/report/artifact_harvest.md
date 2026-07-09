# Artifact Harvest — BVBRC-43

All artifacts are free / public. No paywalled or paid API used.

## Paper (open access)
| Artifact | Source | ID / URL |
|---|---|---|
| Full-text XML | Europe PMC REST | `PMC9883459/fullTextXML` (142 KB) |
| Bibliographic metadata | Europe PMC search | PMID 36707682, DOI 10.1038/s41598-022-25968-8 |

## Genomes (NCBI Datasets v2alpha REST, free, no auth)
| Strain | Host | Paper nuccore acc | Assembly acc | Size (bp) | Contigs | Download |
|---|---|---|---|---:|---:|---|
| BFFF11 | Nile tilapia | CP045918 | **GCA_009685155.1** | 3,067,042 | 1 | genome+protein+CDS+GFF |
| BFF1B1 | Nile tilapia | CP046022 | **GCF_017357805.1** | 2,761,629 | 1 | genome+protein+CDS+GFF |
| BFPS6 | Thai sarpunti | JADBGH010000000 | **GCF_021375735.1** | 2,866,855 | 45 | genome+protein+CDS+GFF |
| V583 (reference) | human (control) | AE016830 | **GCF_000007785.1** | 3,359,974 | 4 | genome+protein+CDS+GFF |

Accession mapping was done via NCBI eutils elink (nuccore→assembly) + esummary; verified strain names.

Download URL pattern (free):
`https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/<ACC>/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF`

## MD5 (genomic FASTA)
```
5c31614eb206fc56f958a5e5fdb9d693  GCA_009685155.1 (BFFF11) genomic.fna
dff3ec2a9dba2a94e85e4616ece836b4  GCF_017357805.1 (BFF1B1) genomic.fna
0354f885251a141bb540c84ee9047d5a  GCF_021375735.1 (BFPS6) genomic.fna
95955cb00cff4a4fcf6371a88225c8d5  GCF_000007785.1 (V583)   genomic.fna
```

## Reference virulence proteins (for tblastn query)
Extracted from the V583 reference proteome (GCF_000007785.1) by product name; 13 curated
markers (fsrA/B, ace, ebpA/C, srtA/C, cylLS/LL, cylR2, tpx, agg/prgB/Asa1 x2) — see
`work/vf_query.faa`.

## Tools / databases (free)
| Tool | Version | DB | Host |
|---|---|---|---|
| AMRFinderPlus | 3.12.8 | 2024-07-22.1 | uicgpu (micromamba env `amr`) |
| mlst | (Torsten Seemann) | efaecalis scheme | uicgpu env `amr` |
| fastANI | (bvbrc28) | — | uicgpu |
| BLAST+ tblastn/makeblastdb | local + bvbrc28 | — | CherryRd + uicgpu |
| NCBI Datasets CLI/REST | v2alpha | — | — |
| Europe PMC REST | — | — | — |
