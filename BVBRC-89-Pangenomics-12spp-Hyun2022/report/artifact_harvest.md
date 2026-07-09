# Artifact harvest — BVBRC-89 (Hyun et al. 2022)

## Paper + supplements

| Artifact | Source | URL | Size | Notes |
|---|---|---|---|---|
| Full-text PDF | BMC Genomics OA | https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-021-08223-8.pdf | 8.2 MB | CC BY 4.0; also PMC8725406 |
| Supplementary data collection | figshare | https://api.figshare.com/v2/collections/5778015 | — | DOI 10.6084/m9.figshare.17870487.v1 |
| Additional file 1 (all supp) | figshare | https://ndownloader.figshare.com/files/32584002 | 8.5 MB zip | Contains DatasetS1-S6, TableS1-S5, FigS1-S10 |
| Dataset S1 (genome IDs) | figshare (from above zip) | — | 128 KB | 12 CSVs, per-species PATRIC genome IDs |
| Dataset S3 (Heaps fits per species) | figshare | — | — | Fitted κ, α parameters and derived cutoffs |
| Table S1 (species/taxon counts) | figshare | — | — | 12 species, 12,676 total genomes |
| Table S2 (Heaps α, κ) | figshare | — | — | Per-species by-genome and by-MLST |
| Table S4 (core/acc/uniq divisions) | figshare | — | — | E. cloacae: 2906 / 4533 / 18239 / 25678 |

## Data pulled for actual replication

| Species | Paper N | Attempted | Fetched | Source | Notes |
|---|---:|---:|---:|---|---|
| Enterobacter cloacae | 104 | 104 metadata + 54 proteomes | 54 proteomes (260,623 proteins) | NCBI Datasets CLI | 50/104 PATRIC IDs have no NCBI assembly accession |

## BV-BRC metadata queries

- Endpoint: `https://www.bv-brc.org/api/genome/` (REST, no auth)
- Query pattern: `in(genome_id,(id1,id2,...))&select(genome_id,genome_name,assembly_accession,cds,contigs,genome_status,genome_length)&http_accept=application/json`
- Rate limit: informal — batches of 15 IDs worked, 25 timed out ~10% of the time. Retry logic added.
- Result: 104/104 metadata retrieved; 54/104 with NCBI Assembly accession.
- Saved: `report/evidence/ecloacae_accessions.csv` (all 104 rows, PATRIC ID + NCBI assembly + name + CDS count)

## NCBI Datasets batch download

- Tool: `datasets` CLI (NCBI)
- Command: `datasets download genome accession --inputfile ec_accessions.txt --include protein --filename ec_download/ec_proteomes.zip`
- Wall time: ~30 s
- Output: 54.7 MB zip → 54 × `protein.faa` (total 260,623 proteins)

## Tools used (versions)

| Tool | Version | Purpose |
|---|---|---|
| CD-HIT | 4.5.4 (built 2014-02-05) | Protein clustering (paper used v4.6; parameters `-c 0.8 -aL 0.8 -n 5` identical) |
| NCBI Datasets CLI | latest | Batch proteome fetch |
| Python | 3.14.6 | Analysis scripts |
| SciPy `curve_fit` | latest | Heaps' law nonlinear least-squares fit |
| pdftotext (poppler) | — | Paper text extraction |
| python-docx | — | Supplementary Table S1-S5 parsing |
| Argo proxy (Anthropic/OpenAI models) | localhost:44497 | LLM judge (used `argo:gpt-5.1`; free per project rules) |

## Not attempted / not available

- **Full 12-species pangenome rebuild** — would need ~3M proteins; time-boxed to one subagent turn.
- **50 PATRIC-only E. cloacae genomes** — public BV-BRC does not offer bulk protein-FASTA download for these; would need PATRIC data portal + login flow.
- **MLST-balanced Heaps' fit** — needs `mlst` tool + PubMLST DB, not installed here.
- **Paper's code** — no public repository located (checked JasonHyun/, Palsson lab, GitHub search 2026-07-03).
- **eggNOG/COG/InterProScan functional annotation** (paper Figs 2, 4-7) — orthogonal to core-methodology replication.
