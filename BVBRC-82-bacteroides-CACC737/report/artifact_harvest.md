# Artifact Harvest — BVBRC-82

All artifacts pulled during this replication run.

## Primary paper
| Item | URL / accession | Size | Notes |
|------|-----------------|------|-------|
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/33987575/ | JSON via eutils esummary | PMID 33987575 |
| PMC full-text XML | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7721585/ | ~10 KB text after tag strip | Open Access CC BY-NC |
| DOI | 10.5187/jast.2020.62.6.952 | – | Publisher landing page |

## Genome assembly (Bacteroides sp. CACC 737)
BioProject: PRJNA647194 · BioSample: (embedded in each record) · Taxon: 2755405

| Accession | Type | Length | GenBank file | Topology |
|-----------|------|--------|--------------|----------|
| CP059408.1 | Chromosome | 4,470,359 bp | seqs/CP059408.gb (9.87 MB) | circular |
| CP059406.1 | Plasmid pCACC737_1 | 29,366 bp | seqs/CP059406.gb (63 KB) | circular |
| CP059407.1 | Plasmid pCACC737_2 | 21,756 bp | seqs/CP059407.gb (42 KB) | circular |
| CP059409.1 | Plasmid pCACC737_3 | 40,439 bp | seqs/CP059409.gb (88 KB) | circular |
| CP059410.1 | Plasmid pCACC737_4 | 22,781 bp | seqs/CP059410.gb (42 KB) | circular |
| CP059411.1 | Plasmid pCACC737_5 | 29,300 bp | seqs/CP059411.gb (59 KB) | circular |
| CP059412.1 | Plasmid pCACC737_6 | 20,435 bp | seqs/CP059412.gb (40 KB) | circular |

Fetch method: `efetch db=nuccore rettype=gbwithparts retmode=text` — one file per accession, 1 s sleep between calls.

## Reference sequence for novel-species test
| Accession | Species | Purpose | File |
|-----------|---------|---------|------|
| NR_112945.1 | *Bacteroides uniformis* JCM 5828 (RefSeq type-strain 16S rRNA) | 16S divergence comparison | work/NR_112945.fa (1,587 B) |

## Query subseq used for the 16S check
- `work/cacc737_16S.fa` (1,534 bp) — first of four 16S paralogs from CP059408 chromosome features.

## Derived / computed artifacts
- `work/genome_stats.json` — per-replicon length/GC/CDS/rRNA/tRNA + comparison-vs-paper table.
- `work/16S_identity_check.json` — CACC737 vs *B. uniformis* JCM 5828 pairwise identity (97.83%, paper 97.5%).
- `work/accessions_verified.json` — esummary confirmation of all 7 accessions.
- `work/plasmid_selfblast.tsv` — cross-plasmid BLAST hits (backbone homology).
- `work/all_plasmids.fa` + `work/plasmid_db.*` — combined multi-FASTA + blast db.
- `work/paper_text.txt` — tag-stripped PMC full text used for accession harvest and claim mining.
- `work/llm_judge_output.md` — argo:gpt-5 judgment (also copied to `report/evidence/`).

## Tools used
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14.6 (system) | scripting |
| Biopython | (system) | GenBank parse, pairwise alignment |
| NCBI BLAST+ blastn/makeblastdb | (system, `/usr/local/bin`) | plasmid self-BLAST |
| Argo proxy | localhost:44497, model argo:gpt-5 | LLM judge |

## Endpoints touched
- `eutils.ncbi.nlm.nih.gov/entrez/eutils/{esearch,esummary,efetch}` — free, no auth
- `127.0.0.1:44497/v1/chat/completions` (Argo, free per standing policy)

No paid endpoint was used. No raw-read (SRA) files were pulled (paper's SRA/BioProject reads not needed for structural claims tested here).
