# Artifact Harvest — BVBRC-50

All artifacts are public and were pulled from free, no-auth endpoints.

## Paper (open access)
- MDPI HTML/PDF: https://www.mdpi.com/2076-2607/11/12/2961
- PMC full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC10745600/ (CC BY 4.0)
- DOI: 10.3390/microorganisms11122961 · PMID 38138105

## Genome assemblies (NCBI Datasets REST, `datasets download genome accession ... --include genome,protein,gff3`)

Target genome:
- **GCF_030848765.1** — *S. oncorhynchi* Z-P2 (GenBank CP132914, CGMCC 1.62135). fna 5,097,623 B, md5 `5c7fc8f1534630782e6cb146dc44451d`. Sequence length 5,034,612 bp (exact paper match).

Comparators — 10 *S. putrefaciens* complete RefSeq genomes:
| Accession | Strain | fna bytes | md5 |
|---|---|---|---|
| GCF_019599085.1 | **YZ08** (paper closest) | 5,126,573 | 477370788bae3db28a0f64d785ae21ca |
| GCF_002157365.2 | SA70 | 5,383,534 | da968f4c5eed4f3c42c505ec12bf2e9b |
| GCF_009730575.1 | FDAARGOS_681 | 4,717,950 | d12e15059f64bff18a4a01b8da4c7970 |
| GCF_016406305.1 | CGMCC-1.6515 | 4,632,677 | 611297608c39ed9f4d81343e7b78d64d |
| GCF_016406325.1 | ATCC 8071 | 4,441,244 | 67cc0b576c494ca04101cd01d402253b |
| GCF_017068195.1 | XY07 | 4,441,144 | 99c9cfd0d87d42da481469df7bc76611 |
| GCF_019599125.1 | YZ-J | 4,441,066 | eb37082d956cb4228a55aee5c2c128fd |
| GCF_025402875.1 | 4H | 4,689,162 | e6583dd92b76d2311cd01f884346c381 |
| GCF_900636665.1 | NCTC12093 | 5,112,602 | ada14411629563d29581251542050afe |
| GCF_003044255.1 | WS13 | 4,439,345 | f5874862fa7b3e819065944703310a72 |

(Storage on uicgpu: `/data/stevens/bvbrc50/genomes/{fna,faa,gff}/`.)

## Derived outputs (in `report/evidence/`)
- `genome_stats.json` — length/GC/contigs/CDS for all 11 genomes.
- `fastani_zp2_vs_all.txt` — fastANI, Z-P2 query vs all.
- `roary70_summary_statistics.txt`, `roary70_analysis.json` — pan-genome @70% id (matched-threshold, headline numbers).
- `roary_default_summary_statistics.txt`, `roary_default_analysis.json` — pan-genome @95% id (default; over-split control).
- `bgc_regions.txt` — CDS products in each of the paper's 5 antiSMASH coordinate windows.
- `llm_judge_argo_gpt52.md` — Argo gpt-5.2 claim-by-claim scoring + verdict.

## Retained on uicgpu (not copied to Dropbox — large)
- `/data/stevens/bvbrc50/genomes/` — raw fna/faa/gff.
- `/data/stevens/bvbrc50/prokka/` — Prokka annotations (11 genomes).
- `/data/stevens/bvbrc50/out/roary/`, `out/roary70/` — full Roary outputs incl. gene_presence_absence.csv.

## Tools
NCBI datasets CLI; Prokka 1.12; Roary 3.12; fastANI; BLAST+ (makeblastdb/blastn); Python 3.11 — conda env `/data/stevens/envs/bvbrc28`. LLM judge: Argo proxy `localhost:44497` model `argo:gpt-5.2` (free).
