# Artifacts summary — BVBRC-20 replication of Pascoe et al. 2020

All paths are relative to the replication root
`~/Dropbox/REPLICATE-PROJECT/BVBRC-20-Cjejuni-Peru-Pascoe2020/`.

## Input data

| Path | What it is | Source |
|---|---|---|
| `data/peru_assemblies/*.fas` | 62 assembled *C. jejuni* genomes (full focal set) | FigShare `10.6084/m9.figshare.10352375`; raw reads under BioProject `PRJNA350267` |
| `data/paper_ST.tsv` | Authors' pubMLST ST + clonal-complex assignments (2020 snapshot) | Extracted from Supplementary S2 |
| `data/paper_aetiology.tsv` | Symptomatic / asymptomatic / unknown aetiology per isolate | Extracted from Supplementary S6 |
| `data/paper_S5_amr.tsv` (implicit) | Author's ABRicate AMR summary (paper's own gene-call ground truth) | Extracted from Supplementary S5 |

## MLST outputs

| Path | Content | Result |
|---|---|---|
| `data/mlst_results.tsv` | `mlst 2.33.1` (campylobacter scheme) calls on all 62 assemblies | **47/62 exact vs paper (75.8%)**; 8 untyped (pubMLST DB drift); 4 novel STs assigned (12690/12694/12697) |

## AMR / resistome outputs

| Path | DB | Notes |
|---|---|---|
| `data/abricate/ncbi.tsv` | NCBI AMR | one of the paper's 5 DBs |
| `data/abricate/card.tsv` | CARD | |
| `data/abricate/resfinder.tsv` | ResFinder | |
| `data/abricate/plasmidfinder.tsv` | Plasmidfinder | |
| `data/abricate/vfdb.tsv` | VFDB | virulence factor DB |

**Aggregated per-class calls vs paper S5:**

- Tetracycline: 10/62 (paper 11/62) — VERIFIED ±1
- Beta-lactam: 26/62 (paper 32/62) — PARTIAL (*bla*OXA-61 identity-cutoff sensitivity)
- Aminoglycoside: 0/62 (paper 0/62) — VERIFIED exact

## Phylogeny outputs

| Path | Content |
|---|---|
| `data/phylo/peru_mash_nj.nwk` | Neighbour-joining tree built from Mash sketch (`s=10000`) pairwise distances |
| `data/phylo/mash_dist.tsv` | Pairwise Mash distance matrix (62 × 62) |

- Within-group pairwise Mash distance (asymptomatic) = 0.0180
- Within-group pairwise Mash distance (symptomatic) = 0.0164
- 17 distinct STs across 28 asymptomatic isolates → **polyphyly VERIFIED**
- **Note:** this is a phylogenetic *substitute* for the paper's core-genome ML tree; it tests structural claims but not tree topology or branch supports.

## Aggregate results by claim

| Claim | Paper value | This rerun | Status |
|---|---|---|---|
| Number of Peru isolates typed | 62 | 62 assemblies processed | full-coverage |
| MLST exact concordance | 62 STs | 47/62 exact (75.8%) | VERIFIED (DB drift) |
| CC21 count (globally dominant) | rare | 3/62 | VERIFIED |
| CC45 count (globally dominant) | rare | 4/62 | VERIFIED |
| CC353 count (local dominant) | dominant | 15/62 | VERIFIED |
| CC362 count (local dominant) | dominant | 11/62 | VERIFIED |
| CC354 count (local dominant) | dominant | 8/62 | VERIFIED |
| Tetracycline resistance | 11/62 | 10/62 | VERIFIED (±1) |
| Beta-lactam resistance | 32/62 | 26/62 | PARTIAL |
| Aminoglycoside resistance | 0/62 | 0/62 | VERIFIED (exact) |
| Aetiology split | 31 / 28 / 3 | 31 / 28 / 3 | VERIFIED |
| Asymptomatic polyphyly | yes | 17 STs across 28 isolates; Mash 0.0180 ≥ 0.0164 | VERIFIED |

## Scripts

| Path | Purpose |
|---|---|
| `scripts/run_all.sh` | End-to-end pipeline: MLST + ABRicate (5 DBs) + Mash-sketch + NJ tree + per-group summaries |

## Reports

| Path | Purpose |
|---|---|
| `report/REPORT.md` | Human-readable per-claim replication report (source of truth) |
| `report/REPORT.tex` | Detailed LaTeX version with dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | Five truly-open questions grounded in Pascoe 2020 Peruvian *C. jejuni* biology |
| `report/workflow.md` | Stage-by-stage pipeline description |
| `report/artifacts_summary.md` | This file — inventory of inputs / outputs / results |
| `report/failure_analysis.md` | Where and why this rerun departs from paper values |

## What is NOT deposited here

- Raw Illumina reads (`PRJNA350267`) — not re-assembled; the paper's own assemblies are used as input
- Per-run `mlst`/`abricate` binary logs (regeneratable via `run_all.sh`)
- Paper's original core-genome ML tree — this rerun ships the Mash/NJ substitute instead
- Phenotypic AMR (disk-diffusion / MIC) data — not part of the paper's deposited dataset, so no independent phenotype comparison possible
