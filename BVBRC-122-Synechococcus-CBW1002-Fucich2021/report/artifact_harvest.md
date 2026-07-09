# Artifact Harvest — BVBRC-122

Every public artifact pulled during this replication. All free, all NCBI or PMC.

| Artifact | Type | URL / accession | Size | Notes |
|---|---|---|---:|---|
| Paper PDF | preprint PDF | https://europepmc.org/articles/PMC7881327?pdf=render | 483,090 B | fetched via uicgpu (HTTPS proxy) |
| CBW1002 fasta | genome FASTA | ftp.ncbi.nlm.nih.gov/…/GCF_015840915.1_ASM1584091v1/…_genomic.fna.gz | 1,096,056 B gz / 3,902,368 B fna | NZ_CP060398.1 |
| CBW1002 gff | GFF3 | ftp.ncbi.nlm.nih.gov/…/GCF_015840915.1_ASM1584091v1/…_genomic.gff.gz | 304,322 B gz | PGAP re-annotation |
| CBW1002 protein.faa | proteome | …_protein.faa.gz | 662,599 B gz | 3,448 proteins |
| CBW1002 assembly stats | stats text | …_assembly_stats.txt | 5,560 B | ASM1584091v1, coverage 17.68× |
| CBW1006 fasta | genome FASTA | …GCF_015840525.1_ASM1584052v1/…_genomic.fna.gz | 1,102,658 B gz | NZ_CP060396.1 |
| CBW1006 gff | GFF3 | …_genomic.gff.gz | 304,362 B gz | PGAP re-annotation |
| CBW1006 protein.faa | proteome | …_protein.faa.gz | 675,657 B gz | 3,553 proteins |
| CBW1006 assembly stats | stats text | …_assembly_stats.txt | 5,560 B | coverage 34.51× |
| BS55D fasta+gff+faa | reference | GCF_004332415.1_ASM433241v1 | 2,263,814 B fna | 2,366 proteins |
| CB0101 fasta+gff+faa | reference | GCF_000179235.2_ASM17923v2 | 2,824,586 B fna | 2,956 proteins |
| WH8102 fasta+gff+faa | reference | GCF_000195975.1_ASM19597v1 | 2,464,928 B fna | 2,631 proteins |
| PCC7002 fasta+gff+faa | reference | GCF_000019485.1_ASM1948v1 | 3,453,082 B fna | 3,196 proteins |
| PCC6312 fasta+gff+faa | reference | GCF_000316685.1_ASM31668v1 | 3,767,144 B fna | 3,621 proteins |
| Cyanobium PCC6307 fasta+gff+faa | reference | GCF_000316515.1_ASM31651v1 | 3,384,203 B fna | 3,312 proteins |
| S. elongatus PCC7942 fasta+gff+faa | reference | GCF_000012525.1_ASM1252v1 | 2,776,712 B fna | 2,707 proteins |
| Synechocystis PCC6803 fasta+gff+faa | reference | GCF_000009725.1_ASM972v1 | 3,996,711 B fna | 3,576 proteins |
| Prochlorococcus MED4 fasta+gff+faa | reference | GCF_000011465.1_ASM1146v1 | 1,678,801 B fna | 1,872 proteins (outgroup) |

**Total ingest:** ~120 MB uncompressed across 33 files (11 genomes × 3 files each). All from NCBI, no auth required, all under permissive research-use terms.

## Live-verified endpoints

- `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi` — assembly + pubmed metadata
- `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` — accession discovery
- `https://ftp.ncbi.nlm.nih.gov/genomes/all/` — genomic FASTA + GFF + protein FAA
- `https://europepmc.org/articles/` — full-text PDF for open-access papers
- `http://<tailnet-aggregator>:4000/v1/chat/completions` — LiteLLM aggregator → Argo GPT-4o (free)
