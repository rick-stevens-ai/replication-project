# Workflow — BVBRC-71 Independent Replication

**Paper:** Oshkin et al. 2019, *Microorganisms* 7(12):683 (Methylospira mobilis Shm1 complete-genome announcement).
**Workflow class:** BV-BRC Comprehensive Genome Analysis (RASTtk annotation + comparative gene-content mining), executed here in a lightweight Biopython-based reproduction.
**Verdict:** PARTIAL.

## Compute Layout

| Stage | Host | Notes |
|-------|------|-------|
| Text retrieval + accession discovery | CherryRd | Europe PMC + NCBI E-utils, free endpoints |
| Genome download (~18 MB combined) | uicgpu | curl on E-utils efetch, `gbwithparts` |
| Parsing / stats / gene-presence scan | uicgpu | Biopython 1.83 in local venv |
| 16S global alignment | uicgpu | Biopython PairwiseAligner |
| LLM-judge (`argo:gpt-5.2`) | CherryRd | Argo proxy at localhost:44497 |

All endpoints free (NCBI E-utils, Europe PMC OA, Argo proxy). No paid API traffic.

## Step-by-Step

### Step 1 — Paper text
- Europe PMC full-text XML for PMC6956133 (MDPI PDF blocked by Akamai; PMC OA tarball 404'd).
- Stripper → plain text.
- Cross-check: NCBI PubMed E-utils `efetch db=pubmed id=31835835 rettype=abstract`.

### Step 2 — Accession discovery
- Regex-scan paper text for `[A-Z]{2}\d{6,}` patterns.
- Found: `CP044205` (Shm1 chromosome), `AE017282` (Methylococcus capsulatus Bath).
- Confirmed BioProject **PRJNA573467**, BioSample **SAMN12811188** in the CP044205 GenBank header.

### Step 3 — Genome download
```
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP044205&rettype=gbwithparts&retmode=text" -o genomes/CP044205.gb   # 10.6 MB
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=AE017282&rettype=gbwithparts&retmode=text" -o genomes/AE017282.gb   # 7.2 MB
```

### Step 4 — Genome statistics
- Script: `work/genome_stats.py`
- Deps: Biopython 1.83.
- Actions:
  - Parse each GenBank record; concatenate CONTIG-derived sequence.
  - Compute GC% directly from sequence (do NOT trust header line).
  - Tally feature counts by type (CDS, tRNA, rRNA, gene, misc_feature).
  - Count 34 gene-name markers of interest via `qualifiers['gene']` and `qualifiers['product']`.
  - Emit JSON with all counts + Mbp length + circular/linear topology.

### Step 5 — Pathway-gene presence scan
- Script: `work/gene_products_scan.py`
- Approach: regex over CDS `product`, `gene`, `note` qualifiers.
- 37 pathway markers grouped by category:
  - **Methane oxidation:** pmoA/B/C (× possible operon copies), mmoX/Y/B/Z/D/C
  - **Methanol oxidation:** mxaF/I, xoxF, mdh (fallback)
  - **N-fixation:** nifH/D/K + nifE/N; vnfD/K/G/H
  - **Carbon fixation / RuMP / serine:** rbcL/S, hxlA/B, glyA, sga, hprA, mtdA/B, mch, ppc
  - **Electron transport:** cydA/B/X (bd-type), cbb3/ccoN/O/P (high-aff), ctaC/D/E
  - **Motility:** fliA/D/E/F/G/H/M/N/P/Q/R, flgB/C/D/E/F/G/H/I/K/L, motA/B, cheA/B/R/W/Y/Z/D
  - **CRISPR:** cas1/2/3, casA/B, cas5e, cas6e, cas7e
  - **Mobile elements:** transposase-family product strings, IS-family names.
- Because deposited annotation is **PGAP** (descriptive product strings), matching was performed BOTH on bare gene symbols AND on product-string subfamilies. This is why the report flags C12 (MxaFI/XoxF) as substring-level evidence.

### Step 6 — 16S rRNA identity
- Script: `work/rrna_ani2.py`
- Extract 16S rRNA features (Shm1: 3 × ~1538 bp; Bath: 2 × ~1473 bp).
- Take one copy from each.
- Global alignment via Biopython `PairwiseAligner`:
  - match = +1, mismatch = −1, gap open = −5, gap extend = −1.
- Identity = matches / ungapped positions.
- Result: **93.89 %** (paper: 94.06 %; delta −0.17 pp).

### Step 7 — LLM-judge verdict
- Script: `work/judge2.py`
- Input: the 21-claim table + a curated paper-fact summary (~2 pages).
- Endpoint: Argo proxy `http://localhost:44497/v1/chat/completions`.
- Model: `argo:gpt-5.2` (fallback from `argo:claude-opus-4.7` which reproducibly 502'd at max_tokens ≥ 2500).
- Params: `temperature=0.1`, `max_tokens=1800`.
- Judge output schema: per-claim `{claim_id, agrees_bool, note}`, plus overall `coverage_pct`, `agreement_pct`, `verdict ∈ {REPLICATED,PARTIAL,NOT-REPLICATED,INCONCLUSIVE}`, `concerns`, `justification`.
- Result: verdict=PARTIAL, coverage=100, agreement=86, 17/21 agrees=true.
- Persisted to `evidence/llm_judge_verdict.json`.

## Provenance & Reproducibility
- **Inputs:** two GenBank flatfiles (CP044205.gb 10.6 MB, AE017282.gb 7.2 MB) with SHA-256 hashes recorded in `work/downloads.sha256`.
- **Environment:** Biopython 1.83, Python 3.11, on uicgpu; Argo proxy on CherryRd.
- **Scripts:** all under `work/` in this dir (`genome_stats.py`, `gene_products_scan.py`, `rrna_ani2.py`, `judge2.py`).
- **Endpoints:** all free (NCBI E-utils, Argo proxy). No API-key gated services were used.
- **Verdict:** `evidence/llm_judge_verdict.json` (independent LLM judge output, single-judge).

## Known Non-Reproductions
1. **Did NOT re-run RASTtk.** The paper's CDS count of 4858 is a RAST number; the deposited annotation is PGAP (4214). We compare against PGAP.
2. **Did NOT run HMMER / BLAST orthology.** Gene-presence work is substring-based, which is why claims C12 (MxaFI/XoxF) and C16 (IS load) are flagged as weakly supported.
3. **Did NOT run ISfinder / ISEScan** for IS-element enumeration. Our 194 transposase-CDS count is a proxy for the paper's ">200 IS elements" figure.
4. **Single LLM judge.** Only `argo:gpt-5.2` was used; no cross-judge ensemble.
