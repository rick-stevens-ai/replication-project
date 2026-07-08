# Artifacts Summary — QC-2312.08044

## 8-artifact standard

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | REPORT.md (human-readable narrative) | `report/REPORT.md` | ✅ pre-existing |
| 2 | REPORT.tex (LaTeX, honest critique, \input{open_questions_section.tex}) | `report/REPORT.tex` | ✅ backfilled |
| 3 | open_questions.json (5 objects, bare list) | `report/open_questions.json` | ✅ backfilled |
| 4 | open_questions_section.tex | `report/open_questions_section.tex` | ✅ backfilled |
| 5 | workflow.md (step-by-step method) | `report/workflow.md` | ✅ backfilled |
| 6 | artifacts_summary.md (this file) | `report/artifacts_summary.md` | ✅ backfilled |
| 7 | failure_analysis.md (honest critique) | `report/failure_analysis.md` | ✅ backfilled |
| 8 | extraction/nougat.mmd (paper-body extraction stub) | `extraction/nougat.mmd` | ✅ backfilled (stub) |

## Pre-existing evidence (preserved, untouched)

- `code/trotter_strang.py` — TFIM driver
- `code/hubbard_dimer.py` — Hubbard dimer driver
- `code/make_plot.py` — plot generator
- `results/trotter_strang_scaling.json` — TFIM numeric results
- `results/hubbard_dimer.json` — Hubbard-dimer numeric results
- `results/err_vs_r.csv` — TFIM tabular
- `report/evidence/err_vs_r.png` — log-log plot
- `report/evidence/*.json` — mirrored numeric evidence
- `report/REPORT.md` — original replication write-up

## Headline claims exercised

- **C1** (1st-order Trotter slope −1, bounded H): **YES** — TFIM op-norm −1.0095, state −1.0033; Hubbard op-norm/state −1.0196. All within ~2%.
- **C2** (2nd-order Strang slope −2, bounded H): **YES** — TFIM op-norm −2.0129, state −2.0133; Hubbard op-norm/state −2.0180. All within ~1%.
- **C3** (state-dependent tightness): PARTIAL — scaling reproduced; constant tightness not head-to-head compared with Childs-Su-Tran-Wiebe (open question 2).
- **C4** (hydrogen ground state N^(-1/4), paper's headline novelty): NOT-TESTED — requires real-space Coulomb sim.

## Verdict (headline-exercised rule)

**REPLICATED** — the paper's standard-regime scaling machinery (C1 + C2), which is the
headline-testable part of the paper accessible to a small-instance CPU reproduction,
is confirmed on two independent Hamiltonians in both operator-2-norm and state error.
The paper's novelty (C4) is flagged as not-tested (not contradicted).

## Cost / provenance

- Compute: ~1 s CPU on CherryRd.
- LLM judges: 2 Argo local (`argo:gpt-5.2`, `argo:gpt-4o`) — free endpoints.
- No paid endpoints used at any step.
