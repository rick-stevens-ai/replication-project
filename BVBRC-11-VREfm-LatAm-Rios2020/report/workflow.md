# Workflow — Ríos et al. 2020 VREfm LatAm Replication

**Verdict:** PARTIAL (17/26 verified, 5 partial, 2 blocked, 4 not-tested)
**Compute envelope:** free CherryRd local CPU + free Argo Opus 4.7
**Passes:** pass-1 (2026-06, cov=6/22 agr=8/22) → pass-2 re-pass (2026-06-23, cov≈12/22 agr≈10/22) → promotion audit (2026-06-27, all pass-2 numbers disk-recounted, PARTIAL sustained)

## Pipeline stages

### 1. Ingestion
- Paper PDF + supp PDF (open access, Nature)
- Parser: `pdftotext` (Poppler) — canonical text dump for claim enumeration
- Parser provenance: `PARSER_PROVENANCE.md`

### 2. Data acquisition
- 55/55 ERV genome assemblies pulled from NCBI GenBank
- Metadata table: `data/erv_accessions.tsv` (55 rows + header = 56 lines)
- Assemblies at `data/genomes/*.fna`; avg 2.99 Mb (range 2.73–3.47)
- All 55 pass quality checks (confirmed pass-1)

### 3. Annotation & typing
- Prokka v1.14.6 (substitution for paper's RAST — RAST web-only/deprecated)
- MLST: Seemann `mlst` v2.33.1 (identical tool as paper)

### 4. Resistome & virulence calling
- abricate with ResFinder + CARD + VFDB DBs at ≥80% identity / ≥80% coverage
- Per-isolate outputs archived from pass-1 (re-used by re-pass without re-running)
- Virulence re-test: `code/repass/virulence_blast.py` — tblastn RefSeq refs for esp, hylEfm, acm, scm, sgrA, fms6, fms22, swpC, ptsD

### 5. Core/pan-genome
- Roary or equivalent orthogroup call from Prokka GFFs
- Core: 2,068 orthogroups (>90% presence); paper reports 1,674
- Pan: 6,441 orthogroups; paper reports 6,735 (95.6% agreement)

### 6. Phylogeny
- FastTree v2.2.0 (GTR+Γ) on 55-genome core alignment (substitution for paper's RAxML)
- ClonalFrameML v1.13 for recombination (identical tool as paper)
- Two-clade split: 26+28 tips after ERV168 pruning

### 7. Re-pass analysis (2026-06-23)
- Single runnable script: `code/repass/repass_analysis.py` (~16 KB)
- Consumes existing abricate outputs + metadata TSV
- Emits:
  - `results/repass/claims_results.tsv` — every claim, paper vs. ours, verdict
  - `results/repass/claims_results.json` — machine-readable
  - `results/repass/metadata_summary.json` — country/ST counts
  - `results/repass/log.txt` — provenance log

### 8. Promotion audit (2026-06-27)
- Independent awk/grep recount of every pass-2 numeric claim against deposited abricate outputs + metadata
- 18 spot-checked numbers reproduced exactly on independent recount
- Verdict sustained at PARTIAL

## Explicitly NOT run
- **BEAST v1.8.4 MCMC** for TMRCA claims 10–13 (compute budget)
- **Paper's custom BLASTX** for AMR-gene calling (used stricter abricate thresholds; explains tet(M) and aac(6')-aph(2'') gaps)
- **250-protein PBP5 random-forest training** (out of re-pass scope)
- **Per-isolate LiaS/LiaR codon inspection** (tractable in a future pass)
- **340-genome global context tree** (55-LATAM core only)

## Reproducibility notes
- Pass-1 report frozen at `report/REPORT.pass1.md`
- Pre-promotion backup at `report/REPORT.md.bak-pre-promo`
- All re-pass code and outputs under `code/repass/` and `results/repass/`
- Free tooling throughout (Argo Opus 4.7 for analyst reasoning; CherryRd for compute)

## Handoff to next pass
Named artifacts required to promote PARTIAL → REPLICATED:
1. CIPRES/HPC time budget for BEAST v1.8.4 on 340-genome alignment (claims 10–13)
2. Sillanpää 2009 *J. Infect. Dis.* supplementary protein reference file (claim C31 virulence-gene differential)
3. Paper's curated 250-protein PBP5 alignment with linked AMP MICs (out-of-scope PBP5 RF claim)
4. Per-isolate variant calls on liaSR loci (LiaS/LiaR daptomycin substitutions)
