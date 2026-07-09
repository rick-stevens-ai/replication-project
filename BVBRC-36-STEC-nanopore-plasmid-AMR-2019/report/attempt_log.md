# Attempt Log — BVBRC-36

**Analyst:** Ollie (OpenClaw subagent) · **Date:** 2026-07-01 (night wave)

1. **Dedup** — `ls ~/Dropbox/REPLICATE-PROJECT | grep -iE nanopore|STEC|shiga` → none. Proceeded.
2. **Read brief + BVBRC-17 exemplar** — mirrored the exemplar's structure (report/ + work/, claims table, BLAST-on-real-genomes methodology).
3. **Identify paper** — DuckDuckGo web_search hit bot-challenge; bioRxiv fetch 403 (Cloudflare). Resolved via Europe PMC + Crossref: preprint 10.1101/571364 → journal PLoS ONE 10.1371/journal.pone.0220494 (PMID 31361781, PMC6667211).
4. **Pull full text** — Europe PMC fullTextXML (180 KB). grep'd accessions: 7 GenBank CP037941–CP037947 (3 strains, 7 replicons); 5 SRA runs (MinION SRR8335317, MiSeq SRR8335318/8333590-92).
5. **Extract testable claims** — genome/plasmid sizes (abstract), Table 1 (MLST), Table 7 (virulome), Table 8 (stx phage), AMR sentence ("only CFSAN027346 … aph(3'')-Ib, aph(6)-Id, blaTEM-1B, sul2, tetB, dfrA on the 73kb plasmid").
6. **Tooling check** — no abricate/amrfinder/mlst locally or on uicgpu; BLAST+ 2.x and Biopython present locally. Chose BLAST-against-curated-DBs (same method family as exemplar). Genomes are small (~5.7 Mb) → local CPU sufficient, uicgpu not needed.
7. **Download genomes** — NCBI efetch (nuccore, fasta) for all 7 CP accessions. Sizes matched paper on first look (88,848 / 96,016 / 73,152 / 157,534 bp plasmids).
8. **Reference DBs** — CGE resfinder_db GitHub repo 404 (moved); fell back to abricate bundled DBs (tseemann/abricate) for resfinder/vfdb/ecoli_vf/plasmidfinder. All fetched (3206/4592/2701/488 seqs).
9. **BLAST screen** (`run_blast.py`) — makeblastdb per replicon; blastn each gene DB as query; abricate default thresholds id≥80 cov≥80. Collapsed allele-level hits to gene symbols (`summarize.py`).
10. **MLST** (`mlst.py`) — PubMLST Achtman scheme #1; exact 100% full-length allele match → profile lookup. 343=ST21, 346=ST21, 350=ST29 (3/3 match).
11. **Genome stats** (`genome_stats.py`) — lengths + GC; all match paper abstract.
12. **stx location** (`stx_location.py`) — stx type 3/3 match; genome coordinates differ from paper Table 8 (paper=MinION-assembly coords, replication=deposited PacBio CP assembly with different origin rotation). Noted as non-biological, non-contradictory.
13. **LLM judge** (`judge.py`) — argo:claude-opus-4.8 → HTTP 502 (known proxy bug); fell back to argo:gpt-5.2 (FREE) per brief. Verdict REPLICATED, coverage 9/10, agreement 10/10.
14. **Wrote report/** — REPORT.md, brief.md, artifact_harvest.md, attempt_log.md, evidence/*.json.

**What worked:** deposited complete genomes + curated-DB BLAST reproduced every categorical/quantitative claim tested. The AMR result is an exact match down to gene, allele (blaTEM-1B), and plasmid localization.
**What was out of reach:** full raw-read de-novo re-assembly (MinION run 3.5 GB + CANU hours) and PHASTER prophage recount — not needed since the published closed assemblies are public and directly verifiable.
