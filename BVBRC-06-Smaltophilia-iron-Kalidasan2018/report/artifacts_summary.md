# Artifacts & Traces Inventory
_Backfilled to the 8-artifact standard on 2026-07-05._

## Paper
| Item | Path | Size | sha256 (short) | Note |
|------|------|-----:|----------------|------|
| Source PDF | `paper/Kalidasan2018.pdf` | 1,587,503 B | `7a727a05...9883d6` | 16 pages + supp. |
| PDF symlink (item 1 of standard) | `paper.pdf` | (link) | (target) | -> `paper/Kalidasan2018.pdf` |
| Paper hand-extracted claims | `paper/paper_extracted.md` | 2,153 B | -- | original agent extraction |
| DOI | 10.3390/molecules23082048 | -- | -- | https://doi.org/10.3390/molecules23082048 |

## Extraction (items 2--3 of standard)
| Item | Path | Size | Note |
|------|------|-----:|------|
| Marker fallback | `extraction/marker.md` | ~90 KB | pdftotext (Poppler layout mode); marker header appended |
| Nougat placeholder | `extraction/nougat.mmd` | 1.2 KB | Stub w/ sha256 + DOI; pending GPU corpus sweep |

## Report (items 4--8 of standard)
| Item | Path | Size | Note |
|------|------|-----:|------|
| Detailed LaTeX report | `report/REPORT.tex` | ~17 KB | Sections: summary, claims table, method, results-vs-paper, per-claim, critique, verdict, open Qs |
| Open-questions LaTeX insert | `report/open_questions.tex` | ~5 KB | Q1--Q5, matches JSON |
| Open questions JSON | `report/open_questions.json` | ~9 KB | list of 5 `{q, basis, next_steps}` |
| Workflow narrative | `report/workflow.md` | ~5 KB | pipeline + tools + effort |
| Failure analysis | `report/failure_analysis.md` | ~7 KB | root-cause honest analysis |
| Legacy markdown report | `report/REPORT.md` | 16,337 B | preserved for lineage |
| Progress log | `report/PROGRESS.md` | 547 B | original 2026-05-10 log |
| Evidence dir | `report/evidence/` | (dir) | reserved for run captures |

## Data / Analysis / Replication (original run)
| Path | Size | Content |
|------|-----:|---------|
| `data/genome_ids.json` | 347 B | 4 BV-BRC genome IDs |
| `data/iron_subsystems_all.json` | 12,517 B | full "Iron acquisition and metabolism" role/feature table (4 genomes) |
| `data/k279a_iron_subsystems.json` | 3 B | K279a-only slice (nearly empty; see failure_analysis) |
| `data/k279a_target_mapping.json` | 3,817 B | 17 targets: SMLT_RS -> Smlt -> RASTtk role |
| `data/comparative_targets.json` | 18,688 B | v1 comparative presence dump |
| `data/comparative_targets_v2.json` | 8,773 B | v2 merged / dedup |
| `analysis/subsystem_comparison.md` | 3,242 B | narrative vs paper Table 1 |
| `analysis/gene_presence_comparison.md` | 2,204 B | 17-target 4-strain matrix |
| `replication/` | empty | reserved, no scripts checked in |

## External Accessions & URLs
- BV-BRC genome IDs: 522373.48 (K279a), 391008.21 (R551-3), 1163399.19 (D457), 868597.17 (JV3)
- GenBank accessions: AE016879, CP001111, HE798556, CP002986
- Paper: https://www.mdpi.com/1420-3049/23/8/2048
- DOI: https://doi.org/10.3390/molecules23082048
- Publisher API for supplement (Tables S1--S4) NOT fetched by this replication.

## Provenance / Chain of Custody
- 2026-05-10: original agent replication (see `report/PROGRESS.md`).
- 2026-06-26: `report/REPORT.md` last touched (verdict + open-Qs polish).
- 2026-07-05: 8-artifact backfill by argo:claude-opus-4.7 subagent
  (session `agent:main:subagent:d2e59617-...`), driven from
  main session `agent:main:telegram:direct:8542341053`. Backfill added
  items 1--3 (paper.pdf symlink, extraction/) and items 4--8 (report/*.tex,
  *.json, workflow.md, artifacts_summary.md, failure_analysis.md).
