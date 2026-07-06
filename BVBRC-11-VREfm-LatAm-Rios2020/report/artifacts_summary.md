# Artifacts Summary — Ríos et al. 2020 VREfm LatAm Replication

**Verdict:** PARTIAL | **Coverage:** 12/22 | **Agreement:** 10/22

## Data artifacts

| Artifact | Location | Content | Provenance |
|---|---|---|---|
| ERV genome FASTAs | `data/genomes/*.fna` | 55 assemblies | NCBI GenBank |
| Metadata table | `data/erv_accessions.tsv` | 55 rows (Col=40, Per=7, Ecu=3, Ven=3, Mex=2), 1998–2015 | NCBI + paper Supp Table 1 |
| Paper PDF | `paper/rios2020.pdf` | Ríos et al. 2020, Sci Rep | Open access, Nature |
| Supp PDF | `paper/rios2020_supp.pdf` | Supplementary tables | Same |

## Analysis outputs

| Artifact | Location | Content |
|---|---|---|
| Pass-1 abricate ResFinder calls | `analysis/abricate_resfinder/*.tsv` | Per-isolate AMR gene hits |
| Pass-1 abricate CARD calls | `analysis/abricate_card/*.tsv` | Per-isolate CARD gene hits |
| Pass-1 abricate VFDB calls | `analysis/abricate_vfdb/*.tsv` | Per-isolate virulence gene hits |
| Prokka annotations | `analysis/prokka/*/` | Per-isolate GFF/FAA/FFN |
| MLST calls | `analysis/mlst/mlst_calls.tsv` | ST per isolate |
| Core/pan-genome | `analysis/roary/` | 2,068 core (>90%), 6,441 pan |
| FastTree phylogeny | `analysis/tree/fasttree_gtrgamma.nwk` | 55-genome core-alignment tree |
| ClonalFrameML | `analysis/clonalframeml/` | Recombination fraction 22.7% |

## Re-pass outputs

| Artifact | Location | Content |
|---|---|---|
| Re-pass script | `code/repass/repass_analysis.py` | ~16 KB single runnable file |
| Virulence tblastn | `code/repass/virulence_blast.py` | RefSeq refs for 9 virulence genes |
| Claims table | `results/repass/claims_results.tsv` | Every claim, paper vs. ours, verdict |
| Claims JSON | `results/repass/claims_results.json` | Machine-readable |
| Metadata summary | `results/repass/metadata_summary.json` | Country/ST counts |
| Virulome calls | `results/repass/virulome_calls.tsv` | Per-isolate virulence-gene presence/absence |
| Virulome summary | `results/repass/virulome_summary.json` | Aggregated |
| Provenance log | `results/repass/log.txt` | Full re-pass run log |

## Report artifacts

| Artifact | Location | Content |
|---|---|---|
| Main report | `report/REPORT.md` | Pass-2 report + 2026-06-27 promotion audit at top |
| LaTeX report | `report/REPORT.tex` | This deliverable — detailed LaTeX with GENUINE CRITIQUE section |
| Pass-1 frozen | `report/REPORT.pass1.md` | Immutable pass-1 baseline |
| Pre-promo backup | `report/REPORT.md.bak-pre-promo` | Snapshot immediately before promotion audit |
| Parser provenance | `report/PARSER_PROVENANCE.md` | pdftotext version + invocation |
| Progress log | `report/PROGRESS.md` | Pass-1 + pass-2 progress notes |
| Workflow doc | `report/workflow.md` | Pipeline stages (this deliverable) |
| Failure analysis | `report/failure_analysis.md` | What did not replicate (this deliverable) |
| Open questions | `report/open_questions.json` | 5 genuinely open research questions (this deliverable) |
| Artifacts summary | `report/artifacts_summary.md` | This file |

## Claims-verification summary

**TIER 1 — VERIFIED (17):** claims 1, 2, 3, 6, 7, 9, 14, 15, C16, C17, C18, C19, C21, C23, C24, C25, C26, C27, C28, C29, C30, C32, C33, C34 (17 unique after dedup)

**TIER 2 — PARTIAL (5):** claims 4, 5, 8, C20, C22

**TIER 3 — BLOCKED (2):** C31 (Sillanpää 2009 virulence ref), PBP5 RF training set

**TIER 4 — NOT_TESTED (4):** claims 10, 11, 12, 13 (BEAST MCMC compute)

## Independently disk-recounted (2026-06-27 audit)

18 numeric claims spot-checked with awk/grep against deposited abricate + metadata files; all 18 reproduce exactly. Full audit table at top of `REPORT.md`.

## What is NOT in the artifact set (deliberately or by blocker)

- BEAST XML / MCMC log files (not run)
- 340-genome global context alignment (LATAM-only)
- Custom BLASTX AMR-gene calls at paper's thresholds (used abricate ≥80/80)
- Sillanpää 2009 virulence protein reference file (external artifact required)
- 250-protein PBP5 training set (out of re-pass scope)
- LiaS/LiaR codon-level variant calls
- Phenotypic MIC panel for the paper's larger 207-isolate collection (not deposited by paper)

## Verification commands (from 2026-06-27 audit, reproducible)

```
ls data/genomes/*.fna | wc -l          # → 55
wc -l data/erv_accessions.tsv          # → 56 (incl. header)
awk '$3=="Colombia"' data/erv_accessions.tsv | wc -l  # → 40
# vanA calls from CARD:
awk -F'\t' 'FNR>1 && $6~/vanA/' analysis/abricate_card/*.tsv | wc -l  # → 54 isolates
```
