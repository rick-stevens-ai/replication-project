# Artifact Harvest — BVBRC-41

All artifacts are public and free-access.

| Artifact | Source / URL | Accession / ID | Size | Notes |
|---|---|---|---|---|
| Paper full text (XML) | Europe PMC REST `fullTextXML` | PMC8816663 / PMID 35145887 | 120 KB | CC BY open access. `work/fulltext.xml`, `work/fulltext.txt` |
| Genome assembly (FASTA+GFF+GBFF+protein+CDS) | NCBI Datasets v2 REST (`datasets` CLI) | **GCF_014263185.1** (ASM1426318v1) | 8.07 MB zip (26 MB unpacked) | Deposited genome of S. algae 2NE11. `work/dataset/` |
| Chromosome nucleotide record | within assembly | **NZ_CP055159.1** (GenBank CP055159) | 5,030,813 bp | single circular chromosome. md5(fna)=`2da02a203fe7c1841db96992305885e3` |
| SRA raw reads (not downloaded) | NCBI SRA | PRJNA547647 | — | PacBio RSII SMRT reads; not needed for stat/annotation replication |
| BioSample | NCBI | SAMN15232066 | — | strain metadata |
| Assembly data report | NCBI Datasets | GCF_014263185.1-RS_2026_04_02 | — | coverage 231.29×; 2026 RefSeq re-annotation counts |

## Derived artifacts (this replication)
| File | Description |
|---|---|
| `work/genome_stats.json` | recomputed length/GC/contigs |
| `work/gene_content.json` | function-based gene-presence survey (RefSeq GFF/faa) |
| `work/comparison_table.json` | paper Table 2 vs recomputed |
| `work/gi_prediction.json` | independent DIMOB-style genomic-island prediction |
| `work/prokka_out/2NE11.txt`,`.tsv`,`.log` | independent Prokka 1.12 re-annotation (run on uicgpu) |
| `report/evidence/llm_judge.txt` | free-Argo (gpt-5.2) claim-by-claim adjudication |

## Tools / endpoints (all free)
- Europe PMC REST · NCBI Datasets CLI (`datasets`) · NCBI E-utilities (esearch/esummary)
- Python 3 (stdlib only) for stats/GFF parsing/GI prediction
- Prokka 1.12 (uicgpu conda env `/data/stevens/envs/bvbrc28`) for independent annotation
- Argo proxy `localhost:44497` model `argo:gpt-5.2` (LLM judge) — free
