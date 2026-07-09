# Artifacts Summary — Patra 2022 POLβ Radiosensitivity Replication

## Top-Level
- `REPORT.md` — canonical, verbose replication report (11 sections, original)
- `README.md` — dir overview
- `PROGRESS.md` — session log

## `code/` (4 scripts)
| Script | Purpose | Runtime |
|---|---|---|
| `01_sequence_check.py` | Translate WT + Δ Polβ cDNA (Biopython); verify frame; align; check canonical residues | ~2 s |
| `02_lq_fit.py` | LQ fit of digitized Fig. 2 clonogenic survival; DMF calc; plot | ~3 s |
| `03_quantitative_audit.py` | Internal-consistency audit of ROS / cell-cycle / Annexin / docking tables | ~1 s |
| `04_pdb_structural_check.py` | Download 11 PDBs from RCSB; parse; verify Polβ active site; audit partner identities | ~90 s (network-bound) |

## `data/`
- `paper.pdf` + `paper.txt` (pdftotext)
- `suppl{1,2,3,4}.pdf` + `.txt` companions
- `pdb/` — 11 RCSB PDB files (1TV9, 1DE8, 1EBM, 1TDH, 1WSR, 1XNA, 2BRF, 2FOZ, 2RCW, 3Q8K, 4ZZY)

## `results/`
| File | Content |
|---|---|
| `sequence_check.json` | Frame check, deletion coordinates, translation summary |
| `alignment.txt` | WT vs Δ Polβ protein alignment |
| `wt_protein.fasta` / `del_protein.fasta` | Translated FASTA |
| `wt_nt.fasta` / `del_nt.fasta` | Input cDNA FASTA |
| `lq_fit.json` | α, β, α/β, D10, DMF per line |
| `quant_audit.json` / `.txt` | Anomaly flags (ROS non-monotonicity, Annexin sum, unit errors, deletion-range mismatch) |
| `pdb_audit.json` / `.txt` | Per-PDB structural verification; 1WSR mislabel finding |

## `figures/`
- `page4-06.png …` — full-page PDF renders (source figures)
- `fig2_replication.png` — our LQ refit overlaid on digitized points

## `report/` (this backfill, 6 files)
| File | Purpose |
|---|---|
| `REPORT.tex` | Formal LaTeX summary of the top-level REPORT.md |
| `open_questions.json` | 5 open questions (JSON list, machine-readable) |
| `open_questions_section.tex` | Same 5 open questions rendered in LaTeX |
| `workflow.md` | End-to-end pipeline description |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Honest critique of what worked / failed / was blocked |

## `extraction/` (this backfill, 1 file)
- `nougat.mmd` — stub note explaining why Nougat MMD was not run

## Coverage Ledger (from top-level REPORT.md Section 1)
- Wet-lab (clonogenic, Western, DAPI, AO/PI, DCFDA, cell-cycle, Annexin): **not run** (LUCID scope; no cells; no raw data deposited)
- Computational (sequence, LQ fit, quant audit, PDB audit): **fully run**
- Remote-server dockings (ClusPro × 9, HDOCK × 4): **spot-checked via inputs/outputs, not re-executed** (queue-time + AUP)

## Total Artifacts
- Original: 4 scripts + 8 data files + 11 PDBs + 11 results files + N figures = ~35 files
- Backfill adds: 7 files (6 in `report/`, 1 in `extraction/`)
