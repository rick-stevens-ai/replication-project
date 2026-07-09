# Artifact harvest — BVBRC-63

## Primary assembly (the paper's genome)
- **Accession:** GCF_002356035.1 (RefSeq) / GCA_002356035.1 (GenBank) / AP017900.1 (nuccore)
- **Assembly name:** ASM235603v1
- **BioProject:** PRJDB5277 (DDBJ) / PRJNA224116 (RefSeq)
- **BioSample:** SAMD00066002
- **Submitter:** Research Center for Bioinformatics and Biosciences, National Research Institute of Fisheries Science, Japan Fisheries Research and Education Agency
- **Sequencing tech:** PacBio RS, 133× coverage, SMRT Analysis 2.2.0
- **Release date:** 2017-09-25 (GenBank/RefSeq); submitted 2016-12-01
- **URLs:**
  - https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/356/035/GCF_002356035.1_ASM235603v1/GCF_002356035.1_ASM235603v1_genomic.fna.gz (2,309,102 bytes)
  - .../GCF_002356035.1_ASM235603v1_protein.faa.gz (1,410,501 bytes; 7,130 proteins)
  - .../GCF_002356035.1_ASM235603v1_genomic.gff.gz (621,485 bytes)

## Comparator assemblies (paper's 4 named comparators)
| Strain | Accession | Proteins | URL |
|--------|-----------|----------|-----|
| N. farcinica IFM 10152 | GCF_000009805.1 (ASM980v1) | 5,942 | ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/805/GCF_000009805.1_ASM980v1/ |
| N. brasiliensis HUJEG-1 (ATCC 700358) | GCF_000250675.2 (ASM25067v3) | 8,428 | .../GCF/000/250/675/GCF_000250675.2_ASM25067v3/ |
| N. cyriacigeorgica GUH-2 | GCF_000284035.1 (ASM28403v1) | 5,533 | .../GCF/000/284/035/GCF_000284035.1_ASM28403v1/ |
| N. nova SH22a | GCF_000523235.1 (ASM52323v1) | 7,508 | .../GCF/000/523/235/GCF_000523235.1_ASM52323v1/ |

## Paper metadata (PubMed E-utilities)
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28257489&rettype=abstract&retmode=text

## Tools used (versions on uicgpu env /data/stevens/envs/bvbrc28)
- Prokka 1.12
- Prodigal 2.6.3
- HMMER 3.4 (hmmpress, hmmscan)
- BLAST+ 2.5 (blastp, makeblastdb)
- barrnap, aragorn, minced 4.2
- Biopython (via python 3.x)
- CD-HIT (v4.x — used for initial coarse clustering; superseded by BLASTP-RBH)

## Compute
uicgpu (8× A100, 255 cores, 2 TB RAM). BLASTP: 4 pairwise runs × 2 directions with 16 threads each. Full annotation + comparative RBH ≈ 8 min wall.
