# Artifact Harvest — BVBRC-71

All public artifacts pulled for the independent replication of Oshkin et al. 2019 (PMID 31835835).

| # | Artifact | URL / accession | Size | Notes |
|---|----------|-----------------|------|-------|
| 1 | Paper full-text XML (JATS) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6956133/fullTextXML | 162 211 bytes | Europe PMC open API — used as MDPI PDF was 403-blocked |
| 2 | Paper abstract (PubMed) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=31835835&rettype=abstract | ~1.7 KB | Confirmed authors/venue/claims |
| 3 | *Ca.* Methylospira mobilis Shm1 chromosome, complete genome | GenBank **CP044205.1** — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP044205&rettype=gbwithparts&retmode=text | 10 604 417 bytes | 4,703,534 bp, circular, submitter/PGAP annotation; BioProject PRJNA573467, BioSample SAMN12811188 |
| 4 | *Methylococcus capsulatus* Bath, complete genome | GenBank **AE017282.2** — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=AE017282&rettype=gbwithparts&retmode=text | 7 191 111 bytes | 3,304,561 bp, reference comparator |
| 5 | Extracted Shm1 16S rRNA sequence | derived from CP044205.1 | 1 538 bp | `evidence/shm1_16s.fasta` |
| 6 | Extracted Bath 16S rRNA sequence | derived from AE017282.2 | 1 473 bp | `evidence/bath_16s.fasta` |
| 7 | Global pairwise alignment Shm1 16S vs Bath 16S | Biopython PairwiseAligner | 6 292 bytes | `evidence/16s_alignment.txt`, 93.89 % identity |

## Locally computed evidence artifacts
- `evidence/evidence_genome_stats.json` — feature counts + GC + gene-of-interest tallies for both genomes
- `evidence/evidence_gene_scan.json` — full CDS-product/gene/note scan for 37 pathway markers per genome
- `evidence/claim_verification.md` — human-written 21-claim table with paper vs independent value
- `evidence/llm_judge_verdict.json` — LLM-judge output (verdict PARTIAL, coverage 100%, agreement 86%)
- `evidence/16s_alignment.txt` — full 16S global alignment

## Code
- `work/genome_stats.py` — parse GenBank, count features, compute GC, tally genes of interest
- `work/gene_products_scan.py` — regex-scan CDS products for 37 pathway markers
- `work/rrna_ani2.py` — extract 16S rRNAs and globally align them
- `work/judge2.py` — LLM-judge caller (Argo proxy, argo:gpt-5.2, temperature 0.1)

## Tool versions
- Biopython 1.83 (on uicgpu system Python 3.8)
- Local Python 3.14.6 (CherryRd, for LLM judge only)
- NCBI E-utils API (public, no key)
- Europe PMC REST API (public)
- Argo LLM proxy: localhost:44497, model `argo:gpt-5.2` (free per standing rule)

## LLM endpoint disclosure
- Judge model: `argo:gpt-5.2` via Argo proxy (localhost:44497, API key `stevens`)
- Also tried and got 502 gateway errors: `argo:claude-opus-4.7` with `max_tokens=2500`. Falling back to gpt-5.2 with `max_tokens=1800` succeeded.
- NO paid endpoints used (no anthropic/openai/openrouter direct).
