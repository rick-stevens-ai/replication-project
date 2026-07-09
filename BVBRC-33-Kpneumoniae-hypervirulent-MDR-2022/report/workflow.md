# Workflow — BVBRC-33 Replication of Altayb et al. (2022)

**Paper:** Altayb HN et al., *Antibiotics* 2022; 11(5):596. DOI 10.3390/antibiotics11050596. PMC9137517.
**Verdict:** PARTIAL REPLICATION (strong). LLM-judge 15/18 = 0.83.

## Overview

Wet-lab-independent, deposition-only replication of a single-isolate MDR hypervirulent (hypermucoviscous) *K. pneumoniae* study. Test whether the paper's core genomic-typing, headline mechanism (rmpA/rmpA2-negative hypermucoviscous strain retaining RcsAB), and AMR/virulome claims reproduce on the authors' own deposited genome using modern, curated tools that mostly post-date the paper.

## Step-by-step

### Step 1 — Paper text acquisition
- **Source:** Europe PMC `fullTextXML` for PMC9137517.
- **MDPI PDF:** bot-blocked; not used.
- **Extracted:** Data Availability section → BioProject **PRJNA767482**, BioSample **SAMN26332310**, WGS **JAKWFM000000000**.

### Step 2 — Genome retrieval
- **Resolver:** BioSample SAMN26332310 → assembly **GCA_022511605.1** via NCBI Datasets REST.
  - *Gotcha:* BioProject PRJNA767482 is an umbrella project holding many unrelated isolates; querying by BioProject would return the wrong genome. BioSample is the correct key.
- **Downloader:** `datasets download genome accession GCA_022511605.1 --include genome,protein,gff3`
- **Assembly stats (Biopython):**
  - Length: 5,364,730 bp
  - Contigs: 83
  - GC: 57.33%
  - N50: 220,979
  - Largest contig: 665,441
  - Verdict: consistent with a draft KpSC genome; usable for typing.

### Step 3 — Typing (Kleborate v3)
- **Command:** `kleborate --preset kpsc -o kleborate_out -a <assembly.fna>`
- **Modules run:** KpSC species/Mash, chromosomal MLST, Kaptive K & O locus typing, curated virulence loci (rmst, rmpa2, abst, smst, ybst, cbst), KpSC AMR module.
- **Output:** `report/evidence/kleborate_full.tsv`.

### Step 4 — Resistome (AMRFinderPlus)
- **Version:** 4.2.7, DB 2026-05-15.1.
- **Command:** `amrfinder --nucleotide <assembly.fna> --organism Klebsiella_pneumoniae --plus -o amrfinderplus.tsv`
- **Output:** `report/evidence/amrfinderplus.tsv`.

### Step 5 — Targeted checks
- **blaCTX-M-15 presence/absence:** `blastn` of reference NG_048935.1 vs the assembly.
  - Result: only spurious fragments (≤44 bp, ≤7% query coverage) → **absent full-length**.
- **PGAP product-name inspection:** grep on `protein.faa` (5,064 proteins) for RcsA, RcsB, IroE, IroN, IutA, T6SS components, fimbrial products.
  - Recovered: RcsA (MCH6120814.1), RcsB (MCH6119087.1), IroE (MCH6118329.1), 32 T6SS products, 46 fimbrial/pilus products.
  - Not recovered: IroN, IutA.

### Step 6 — Reconciliation with paper
- Built a claim-by-claim table (C1–C18) mapping paper assertions to independent tool outputs.
- Distinguished exact matches (13), allele/family-level matches with database naming drift (aac(6′)-Ib-cr5 vs cr6; fosA/FosA5 family vs fosA6), tool-dependent discrepancies (iutA absent, iroN absent), and hard non-replications (blaCTX-M-15 absent from deposited draft).

### Step 7 — LLM judge
- **Primary:** `argo:claude-opus-4.8` (free) → HTTP 502 (Argo proxy bug).
- **Fallback:** `argo:gpt-5.2` (free).
- **Prompt:** claims table + evidence excerpts → structured verdict.
- **Result:** 15/18 = 0.83; verdict PARTIAL REPLICATION (strong); most important discrepancy = missing plasmid-borne blaCTX-M-15.

### Step 8 — Report write-up
- `report/REPORT.md` — human-readable Markdown report.
- `report/REPORT.tex` — LaTeX version with dedicated GENUINE CRITIQUE section (this backfill).
- `report/evidence/` — machine-readable evidence bundle.
- `report/open_questions.json` — 5 domain-grounded open questions (this backfill).

## Environment
- `bioconda` env `kleb`: minimap2 2.31, mash, AMRFinderPlus 4.2.7, BLAST+ 2.17.0.
- Python venv (pip): `kleborate` v3, `kaptive`.
- Compute: local (uicgpu / m1 class, single node, no GPU needed for typing).

## Provenance discipline
- No fabricated numbers. Every numeric claim in `REPORT.md` traces to a file in `report/evidence/` or a run log in `work/`.
- LLM judge output preserved in `work/judge/` (prompt + verdict).
- Assembly accession + tool versions locked; re-running with the same inputs is expected to reproduce exactly (Kleborate v3 KpSC preset + AMRFinderPlus DB 2026-05-15.1).
