# Artifacts summary — lucid100-fast-neutron-lymphocyte-dsbs-doserate

## Paper
- `artifacts/paper.pdf` (1.3 MB, sha256 `4c4beae28a75716987e4968b9df6b8d9cf990810fd72805bbe2f86869f19022d`) — OA PDF from Europe PMC.
- `artifacts/paper_fulltext.xml` — JATS XML (119 KB).
- `artifacts/paper.txt` — pdftotext -layout output (49 KB, digitization source).
- `artifacts/paper_unpaywall_s2_acquired.pdf` — secondary copy (4.5 MB).
- `artifacts/epmc_search.json` — EPMC search API metadata + OA flags.
- `artifacts/MANIFEST.md` — provenance for harvested files.

## Digitized data
- `data/table1_induction.csv` — 5 doses × HDR/LDR mean+SD (induction curve).
- `data/table2_hdr_ldr_ratio.csv` — per-dose HDR/LDR ratio.
- `data/table3_repair_kinetics.csv` — 6 time points × HDR/LDR mean+SD at 1 Gy.
- `data/paper_key_numbers.json` — hand-extracted abstract/Discussion claims (audit ground truth).

## Analysis scripts
- `scripts/smoke_replicate.py` — first-pass 3-check harness (2026-06-09).
- `scripts/extended_replicate.py` — audit 7-check harness (2026-06-22).

## Results
- `scripts/smoke_outputs/smoke_results.json` — first-pass JSON (3/3 PASS).
- `scripts/smoke_outputs/smoke_plots.png` — induction + repair overlay.
- `results/extended_results.json` — audit JSON (7/7 PASS, C7 anomaly flagged).
- `results/extended_summary.md` — machine-readable claim table.
- `results/induction_and_repair_overlay.png` — overlay plot for the report.

## Reports
- `REPORT.md` — full audit narrative (2026-06-22, Ollie subagent).
- `FIRST_PASS_REPORT.md` — original 2026-06-09 first-pass narrative.
- `PROGRESS.md` — running log.
- `README.md` — folder overview.

## Backfill (2026-07-06)
- `report/REPORT.tex` — LaTeX audit summary (this backfill).
- `report/open_questions.json` — 5 open questions in JSON.
- `report/open_questions_section.tex` — 5 open questions in LaTeX prose.
- `report/workflow.md` — end-to-end workflow.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — reproducibility-blocker analysis + hard critique.
- `extraction/nougat.mmd` — nougat/marker stub (paper.pdf sha256 + note that full run was not performed under free-endpoint-only + no-re-run policy).

## What we do NOT have (upstream data gaps)
- Per-cell γ-H2AX foci CSV (~32 000 rows).
- Metafer/MetaCyte classifier configuration.
- GraphPad Prism v5 project file.
- iThemba LABS p(66)/Be(40) neutron energy spectrum / LET file.
- Raw immunofluorescence micrographs.
- IRB approval number / consent chain metadata.
