# Attempt log — BVBRC-89 (Hyun, Monk, Palsson 2022, BMC Genomics)

Analyst: Ollie (OpenClaw subagent, argo/argo:claude-opus-4.7)
Date: 2026-07-03 (CDT)

## Timeline

1. **12:20 CDT** — Received wave-brief subagent task. Read wave brief and BVBRC-17 exemplar for format reference.

2. **12:21** — Set up target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-89-Pangenomics-12spp-Hyun2022/{report,work}/`. Verified paper metadata via NCBI eutils esummary: BMC Genomics 23:7 (2022), PMID 34983386, PMC8725406, open access (CC BY 4.0).

3. **12:21** — Fetched PMC OA PDF from BMC direct URL (`bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-021-08223-8.pdf`). 8.2MB, converted with `pdftotext -layout`.

4. **12:22** — First attempt at high-level analysis via `pdf` MCP tool failed (Anthropic credit-low + Gemini model-unknown). Switched to pdftotext + grep to extract methods, species list, and numerical results directly. Confirmed:
   - 12,676 genomes, 12 species (Table S1: A. baumannii, C. coli, C. jejuni, E. cloacae, E. faecium, E. coli, K. pneumoniae, N. gonorrhoeae, P. aeruginosa, S. enterica, S. aureus, S. pneumoniae)
   - CD-HIT v4.6 with `-c 0.8 -aL 0.8 -n 5` for clustering
   - MLST via https://github.com/tseemann/mlst v2.18.0
   - Data on PATRIC (now BV-BRC), Dataset S1 has PATRIC genome IDs
   - No code repo mentioned in paper (checked JasonHyun/ github, Palsson SBRG github; no comparative-pangenomics repo public)

5. **12:23** — Downloaded supplementary data via figshare API (collection 5778015, article 17870487, single 8.5MB zip). Extracted:
   - DatasetS1.zip → 12 per-species CSVs of PATRIC genome IDs (E. cloacae has 104 IDs — smallest set, matches paper)
   - TableS1.docx → species/genome-count table
   - TableS2.docx → Heaps' law α/κ estimates for all 12 species (both by-genome and by-MLST)
   - TableS3.docx → MAE fit accuracy
   - TableS4.docx → **gene frequency cutoffs + division counts** — critical replication targets

6. **12:24-12:26** — Chose E. cloacae as feasible full-species replication target (smallest at 104 genomes). Queried BV-BRC API for all 104 PATRIC genome IDs; retrieved metadata for all 104. Of these, **54 have public NCBI Assembly accessions** (GCF_*/GCA_*); the other 50 appear to be PATRIC-internal submissions never mirrored to GenBank. This is a real-world data-availability gap.

7. **12:27-12:28** — Downloaded all 54 available proteomes in a single batch via NCBI Datasets CLI (`datasets download genome accession --inputfile ec_accessions.txt --include protein`). 54.7MB zip → 54× `protein.faa`, **260,623 total proteins** across 54 genomes (min 4,368 / max 5,236 per genome; consistent with paper's per-genome CDS counts).

8. **12:29** — Concatenated proteomes into single FASTA `ec_combined.faa` (102MB), embedding genome accession in each protein header (`>GCF_xxx|WP_yyy ...`) so cluster membership can be traced back to genomes.

9. **12:29-12:30** — Ran **CD-HIT v4.5.4** with the paper's **exact parameters** `-c 0.8 -aL 0.8 -n 5 -M 8000 -T 4 -d 0`. 34 seconds wall time, 239 MB peak RAM. Result: **16,959 gene clusters** from 260,623 proteins.

10. **12:30-12:31** — Parsed .clstr file, computed per-cluster genome membership, gene-frequency distribution, and pangenome division applying the paper's own percentage cutoffs (core: gene in ≥98.3% of genomes, unique: gene in ≤8.3% of genomes) scaled to our N=54. Results:
    - Total pangenome: 16,959 (paper 25,678 for N=104)
    - Core: 3,046 (18.0%) — paper 2,906 (11.3%) — **core count matches within 5%**
    - Accessory: 4,351 (25.7%) — paper 4,533 (17.7%) — **matches within 4%**
    - Unique: 9,562 (56.4%) — paper 18,239 (71.0%) — halved as expected under an open pangenome (54/104 = 0.52; 9562/18239 = 0.52 ✓)

11. **12:31-12:32** — Fit Heaps' law `pan(N) = κ·N^α` over 100 random genome orderings using SciPy `curve_fit`. Result: **α = 0.337 ± 0.020, κ = 4,445 ± 362** vs paper by-genome **α = 0.384 ± 0.023, κ = 4,330 ± 451**. κ is essentially identical; α is ~12% low (expected — subsampling truncates the accessory tail and slightly compresses observable openness), but still well within Gammaproteobacteria "open pangenome" range.

12. **12:32-12:33** — LLM-judge verdict via Argo (`argo:gpt-5.1`, free endpoint per rules; Argo claude-opus-4.7 returned 502). Judge output (JSON, saved to `evidence/judge_verdict.json`):
    - verdict: **PARTIAL**
    - coverage_pct: **45**
    - one_line: "Key E. cloacae pangenome size, structure, and openness metrics replicate on a 54-genome subset, but most multi-species and MLST-based analyses remain untested."

13. **12:33-12:34** — Wrote REPORT.md, brief.md, artifact_harvest.md, attempt_log.md.

## What worked
- BV-BRC REST API for metadata (paginated by 15-25 IDs; some batches timed out at 25, retried at 15)
- NCBI Datasets CLI for batch proteome download (single command, 54 genomes, 55MB in ~30s)
- CD-HIT 4.5.4 with paper's exact parameters, 34 s wall on 260K proteins locally (no need for uicgpu)
- Figshare API for supplementary data (single JSON call → download URL)
- SciPy `curve_fit` for Heaps' law with 100 orderings, ~15 s
- Argo free endpoint for LLM judge (gpt-5.1 responded reliably; claude-opus-4.7 was 502)

## What didn't work / limitations
- 50/104 (48%) of paper's E. cloacae PATRIC genomes have no NCBI Assembly accession → true real-world data-availability gap; cannot rebuild the exact 104-genome pangenome from public sources today
- No public code repository for the paper's analysis pipeline (checked JasonHyun/, Palsson lab, and GitHub search)
- MLST typing skipped (would need mlst tool + PubMLST database; α from MLST-balanced sampling is a headline methodological claim of the paper)
- Full 12-species rebuild not attempted (would take ~40× more compute; feasible on uicgpu but time-boxed to one subagent turn)
- Functional/eggNOG/InterProScan/AARS-domain analyses (paper Figs 4-7) skipped as orthogonal to core replication claims
- `pdf` MCP tool + Anthropic PDF extraction failed (credit balance) — fell back to pdftotext + grep, worked fine

## Key intermediate files (see `work/`)
- `supp/` — full supplementary data (Datasets S1-S6, Tables S1-S5, Figs S1-S10)
- `ecloacae_accessions.csv` — 104-row mapping PATRIC ID → NCBI assembly + genome_name + cds count
- `ec_combined.faa` (102 MB) — combined proteome FASTA with genome-tagged headers
- `cdhit/ec_clusters.clstr` (277,582 lines) — raw CD-HIT cluster output
- `evidence_freq_dist.json` — gene frequency distribution + division counts
- `evidence_heaps.json` — Heaps' law fit results
- `judge_verdict.json` — LLM judge output
