# Artifacts summary — lucid100-uhdr-plasmid-dna-topas-nbio

## Top-level documentation
- `README.md` — original paper overview (7.5 KB).
- `FIRST_PASS_REPORT.md` — prior smoke-GO verdict (7.9 KB, 2026-06-09).
- `REPORT.md` — full 26-row claim audit + narrative (18.6 KB, 2026-06-22).
- `ARTIFACT_MANIFEST.md` — provenance + SHA-256 ledger (3.4 KB).
- `PROGRESS.md` — phase log (2.8 KB).

## `report/` (this backfill, 2026-07-06)
- `REPORT.tex` — condensed LaTeX audit; preserves SPOT-CHECK verdict.
- `open_questions.json` — 5 machine-readable open questions with basis + concrete next_steps.
- `open_questions_section.tex` — LaTeX-formatted open questions block.
- `workflow.md` — step-by-step workflow narrative.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of scope/limitations.

## `artifacts/` (source & metadata)
- `paper.pdf` — CC-BY 4.0 full text, 15 pp, 2.0 MB.
- `paper.txt` — pdftotext extract, 1116 lines.
- `crossref.json`, `semanticscholar.json`, `openalex.json`, `unpaywall.json` — metadata.
- `unpaywall_dkondo2021.json`, `unpaywall_dkondo2024.json` — precursor chemistry references.
- `ae62c6_esummary.json` — NCBI (PMID 42013902).
- `ae62c6_epmc.xml` — EuropePMC probe (empty; paper not in EPMC fulltext).
- `SHA256SUMS.txt` — content integrity ledger.

## `scripts/` (executable reproduction)
- `chemistry_table1.csv` — all 43 chemistry reactions (R1–R43*) extracted verbatim.
- `smoke_scavenging_capacity.py` — Eq. (4) + intertrack reproducer with in-line assertions.
- `smoke_dsb_audit.py` — DSB / Model 2 / bp-threshold sensitivity with 200 000-iter Poisson MC.
- `smoke_results.csv`, `smoke_dsb_results.csv` — numeric outputs.
- `smoke_run.log`, `smoke_dsb_run.log` — full run logs with assertion pass/fail.

## `figures/`
- `smoke_ssb_vs_sigma.png` — SSB shape vs σ (normalized).
- `smoke_intertrack_vs_oh_lifetime.png` — Fig. 4 mechanism reproducer.
- `smoke_dsb_ratio_vs_sigma.png` — DSB UHDR/CONV ratio vs scavenging capacity.
- `smoke_dsb_bp_sensitivity.png` — bp-threshold sensitivity sweep.

## `notes/`
- `HPC_JOB_PLAN.md` — concrete plan for full MC rerun on Aurora / uicgpu when TOPAS-nBio chemistry decks are released.
- `REPRODUCIBILITY_SCORECARD.md` — 3.6/5 roll-up.

## `extraction/`
- `nougat.mmd` — stub / placeholder (paper is text-extractable via pdftotext at 1116 lines with full Methods + Tables 1&2 + §3.1/3.2 numeric content; no Nougat OCR pass was needed for this pipeline).

## What is NOT here (blockers documented)
- **No `sim/` directory:** No TOPAS-nBio simulation was executed. See `report/failure_analysis.md`.
- **No `chemistry_decks/`:** Models 1 & 2 `TsChemistry` `.topas` files were never released by the authors.
- **No cross-code outputs:** No Geant4-DNA standalone or PARTRAC comparison run.
- **No cellular-geometry runs:** Paper is naked-plasmid only; chromatin extrapolation is left open (open question #1).

## Provenance summary
- All metadata endpoints are public/free. Semantic Scholar key from macOS Keychain (`security find-generic-password -a rick-stevens-ai -s semantic-scholar-api-key -w`).
- No paid endpoints used. No author contact attempted. Author GitHub profiles (`masilela`, `d-kondo`) checked — both empty.
- Backfill (2026-07-06) added the 7 `report/` and `extraction/` artifacts without modifying any pre-existing file (`REPORT.md`, `FIRST_PASS_REPORT.md`, `ARTIFACT_MANIFEST.md`, `PROGRESS.md`, `README.md`, `artifacts/*`, `scripts/*`, `figures/*`, `notes/*` all preserved unchanged).
