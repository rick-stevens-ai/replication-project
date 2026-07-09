# Artifacts Summary — BVBRC-19 (Propionibacterium pan-genome + metabolic replication)

Verdict: **PARTIAL** · Coverage 9/10 · Agreement 10/10

## Input data (author-provided)

| Path | Description | Source |
|---|---|---|
| `data/genbank/Genbank_files/*.gbk` | 6 inter-species representative genomes (PAC_4875, PAC_55737, PSHE, PAVI, PACN, PPRO) | Paper Supp. File 4 (Genbank_files.zip) |
| `data/PMC7650540/.../Model_XML_files/*.xml` | 6 published genome-scale metabolic models (SBML) | Paper Supp. Model_XML_files.zip |

**Total CDS with translation extracted:** 17,525

## Layer 1 — Pan-genome artifacts (NEW this re-tier)

| Path | Description | Size / detail |
|---|---|---|
| `data/proteins/{TAG}.faa` | Per-strain protein FASTA (6 files) | 17,525 total seqs |
| `data/proteins/all_proteins.faa` | Concatenated all-strain protein FASTA | for blast db |
| `data/blast/all_vs_all.tsv` | all-vs-all blastp results | 414,365 hits |
| `data/pangenome/clusters.txt` | MCL clusters at inflation 1.5, ≥75% cov, ≥30% id | 5,946 total pan clusters |
| `report/evidence/pangenome.json` | Per-strain pangenome metrics + accumulation curves (30 orderings) | machine-readable |

**Key numbers recovered:**
- Core clusters (all-6): **909** (paper: 792-906)
- Pan clusters (all-6): **5,946**
- Strain-specific: **3,123** (52.5% of pan)
- Pan-genome accumulation: 2459 → 3482 → 4274 → 4926 → 5508 → 5946 (still open at genome #6)

## Layer 2 — Pathway-audit artifacts (NEW this re-tier)

| Path | Description |
|---|---|
| `scripts/pathway_audit.py` | Enzyme-scan script (`/function/`, `/product/`, `/note/`, `/EC_number/`) |
| `report/evidence/pathway_audit.json` | Per-strain enzyme hit counts + M1-M6 claim verdicts |

**Six diagnostic enzyme claims audited:** M1 methylmalonyl-CoA mutase, M2 transaldolase, M3 L-lactate DH, M4 xylose isomerase, M5 sucrose-6-P hydrolase, M6 PFOR/nifJ.
**Verdict: 6/6 exact matches** (including diagnostic absences).

## Layer 3 — FBA artifacts (from prior re-tier 2026-06-25)

| Path | Description |
|---|---|
| `scripts/fba_reproduce.py` | FBA reproduction driver |
| `scripts/inspect_models.py` | Per-model μ, exchange, vitamin dependency inspection |
| `report/evidence/fba_replication.json` | Per-model μ (default & no-glucose), propionate flux, vitamin auxotrophy |

**Six models tested:** PSHE, PAC_4875, PAC_55737, PAVI, PACN, PPRO — all solve to positive growth; propionate major fermentation product across all six; auxotrophy hierarchy nests as reported (dairy < commensal < opportunist).

## Scripts (executable)

| Script | Purpose |
|---|---|
| `scripts/extract_proteins.py` | GBK → per-strain FASTA |
| `scripts/build_pangenome.py` | blastp → MCL → core/pan/singleton metrics + accumulation curves |
| `scripts/pathway_audit.py` | Diagnostic enzyme presence/absence scan |
| `scripts/fba_reproduce.py` | COBRApy FBA driver over 6 GEMs |
| `scripts/inspect_models.py` | Per-model exchange / vitamin / growth inspection |

## Reports

| Path | Description |
|---|---|
| `report/REPORT.md` | Full replication report (Markdown, verdict + claim-by-claim table) |
| `report/REPORT.tex` | LaTeX report + GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 truly open scientific questions grounded in this work |
| `report/workflow.md` | Step-by-step pipeline documentation |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | What did NOT replicate + why + methodology criticisms |
| `report/REPORT.md.bak-pre-promo` | Prior PARTIAL verdict version (preserved) |

## What is NOT in the artifact set (deliberately)

- **Raw NCBI assemblies + KBase/RAST/GLIMMER re-annotation output.** The upstream annotation step was not re-derived — we started from author-deposited standardized GenBank files. This is the residual 1/10 coverage gap.
- **MCL inflation sensitivity sweep.** Only I=1.5 (paper's value) was run.
- **MEMOTE / gap-fill / essentiality validation** of the six GEMs — beyond scope of paper-behavior replication.

## Compute footprint

Entire pipeline runs on local CPU (16 threads). blastp step is the bottleneck at ~3 min; MCL clustering and FBA both complete in seconds. No GPU, no HPC, no external service dependency.
