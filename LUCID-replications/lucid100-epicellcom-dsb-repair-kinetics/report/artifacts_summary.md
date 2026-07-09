# Artifacts Summary — Scott 2011 Epicellcom DSB Repair Kinetics

## Directory
`~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-epicellcom-dsb-repair-kinetics/`

## Preserved (pre-backfill)
- `README.md`
- `PROGRESS.md`
- `REPORT.md` — the authoritative narrative report
- `ARTIFACT_MANIFEST.json`
- `data/scott2011_epicellcom.pdf` (source PDF, EuropePMC PMC3315173, sha256 `e880e6dfac420f2f6cfc1826c10c4310e9aebea48dd8c7190a86192f72904bf8`)
- `data/scott2011_epicellcom.txt` (text extract for grep)
- `code/multisig1.py` — pure-Python re-implementation of Eqs 3, 5, 6, 8, 10-14
- `code/replicate_figures.py` — driver that emits all figures + summary.json
- `figures/fig1_phi_n.png`
- `figures/fig2_attributions.png`
- `figures/fig3_Psi_n.png`
- `figures/fig4_Cum.png`
- `figures/fig5_residual_DSBs.png`
- `results/summary.json` (spot-check values)
- `results/fig5_RB.csv` (numeric RB(t,D) grid backing Fig 5)

## Added by backfill (2026-07-06)
- `report/REPORT.tex` — LaTeX version of the report with genuine critique section (5 subsections: cell-cell communication framing vs test, epithelial-vs-fibroblast, monolayer-vs-3D geometry, low-dose bystander threshold, absent wet-lab overlay)
- `report/open_questions.json` — 5 truly-open questions, each with why_open + concrete next_steps + effort estimate + free-endpoint flag
- `report/open_questions_section.tex` — LaTeX drop-in for the report
- `report/workflow.md` — end-to-end runbook (paper acquisition, equations transcribed, params, figures, spot-checks)
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — verdict cross-check + genuine failure modes / limitations
- `extraction/nougat.mmd` — stub (nougat not re-run; paper.pdf sha256 recorded for provenance)

## Coverage summary (from REPORT.md, unchanged)
- Coverage (out of 10): 8
- Agreement to paper's own numerics (out of 10): 9
- Agreement to wet-lab data (out of 10): not assessed (open question Q4/Q5)
- Verdict: REPLICATED — model / equations

## Endpoints and cost
- No LLM calls, no compute reservation, no paid endpoints.
- Pure local Python; <1 s runtime.
