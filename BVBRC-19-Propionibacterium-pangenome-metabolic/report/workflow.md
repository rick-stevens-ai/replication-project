# Workflow — BVBRC-19 (McCubbin 2020 Propionibacterium pan-genome + metabolic replication)

Verdict: **PARTIAL** · Coverage 9/10 · Agreement 10/10 (as of 2026-06-27)

## Overview
Three independent replication layers were executed on top of the authors' deposited
standardized GenBank files (Supplementary File 4). The upstream KBase/RAST/GLIMMER
re-annotation step was **not** re-derived (this is the source of the PARTIAL verdict).

```
Author-deposited GenBank files (Supp. File 4)
        │
        ├──► Layer 1: Pan-genome reconstruction
        │       extract_proteins → blastp → filter → MCL@1.5
        │
        ├──► Layer 2: Pathway-content audit
        │       scan /function/, /product/, /note/, /EC_number/ per CDS
        │
        └──► Layer 3: FBA reproduction
                load 6 SBML models → COBRApy → μ, exchange fluxes, auxotrophy
```

## Step-by-step

### Step 0 — Inputs
- `data/genbank/Genbank_files/*.gbk` — 6 inter-species reps (PAC_4875, PAC_55737, PSHE, PAVI, PACN, PPRO); 17,525 CDS with translations
- `data/PMC7650540/.../Model_XML_files/*.xml` — 6 published GEMs
- Source: paper's Supplementary File 4 (Genbank_files.zip) and Model XML files zip

### Step 1 — Protein extraction (Layer 1 prep)
- Script: `scripts/extract_proteins.py`
- Input: per-strain GBK
- Output: `data/proteins/{TAG}.faa` (6 files) + concatenated `data/proteins/all_proteins.faa`
- Total: 17,525 protein sequences

### Step 2 — All-vs-all blastp
- makeblastdb on `all_proteins.faa`
- blastp -query all_proteins.faa -db all_proteins.faa -evalue 1e-5 -num_threads 16
- Output: `data/blast/all_vs_all.tsv` (414,365 hits; all 17,525 queries returned)
- Runtime: ~3 min on local CPU (16 threads)

### Step 3 — Cluster construction (MCL)
- Script: `scripts/build_pangenome.py`
- Filter blast hits to ≥30% identity AND ≥75% coverage of shorter protein (paper: 75% cov)
- Symmetrize edges, weight by bit-score
- `mcxload` → `mcl -I 1.5` (paper's inflation)
- Output: `data/pangenome/clusters.txt`
- Metrics dumped to `report/evidence/pangenome.json` (core/pan/singleton counts, accumulation curves averaged over 30 random genome orderings)

### Step 4 — Pathway-content audit (Layer 2)
- Script: `scripts/pathway_audit.py`
- Independent scan of every CDS's `/function/`, `/product/`, `/note/`, `/EC_number/` fields for 6 diagnostic enzymes: MCM (5.4.99.16), transaldolase (2.2.1.2), L-lactate DH (1.1.1.27), xylose isomerase (5.3.1.5), sucrose-6-P hydrolase, PFOR/nifJ
- Per-strain presence/absence tabulation
- Output: `report/evidence/pathway_audit.json` (hit counts + verdicts per claim)

### Step 5 — FBA reproduction (Layer 3, prior re-tier 2026-06-25)
- Script: `scripts/fba_reproduce.py` + `scripts/inspect_models.py`
- Load 6 SBML models via COBRApy
- Compute μ under default media and glucose-out media; report propionate secretion flux, open exchange count, essential vitamin set
- Output: `report/evidence/fba_replication.json`

### Step 6 — Claim-by-claim reconciliation
- Cross-tabulate results against the 14 numerical / presence-absence claims C1-C5, P1-P3, M1-M6
- Written into `report/REPORT.md`

## What was NOT done
- **KBase/RAST/GLIMMER re-annotation of raw NCBI assemblies.** Would require the frozen 2014-2015 KBase pipeline. This is the residual 1/10 coverage gap and the reason the verdict here is PARTIAL rather than full end-to-end.
- **Sensitivity analysis on MCL inflation.** Ran only at I=1.5 (paper's value).
- **Model-quality metrics** (MEMOTE, gap-fill fraction, essentiality prediction) — beyond scope of replication of the paper's reported behaviors.
- **Expanded panel beyond 6 reps** — 65% strain-specific figure would require all 16 closed genomes; we ran only the 6 inter-species reps used for the paper's primary pan-genome comparison.

## Compute
- Local CPU: makeblastdb + blastp 16 threads ≈ 3 min
- mcxload + mcl: seconds
- COBRApy FBA: seconds
- No GPU / no HPC — entire pipeline is laptop-scale.

## Reproducibility
- Full artifact tree in `data/`, `scripts/`, `report/evidence/`
- All scripts are pure Python + shell; no proprietary dependencies
- Paper's supplementary material is fully available (Genbank_files.zip, Model_XML_files.zip)
- Not reproducibility-blocked; only the upstream annotation step is underspecified in the paper
