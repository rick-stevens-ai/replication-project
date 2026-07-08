# Artifacts summary — MC-VQE Parrish 2019 replication

Target: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-MC-VQE-electronic-transitions-Parrish2019/`

## Report

- `report/REPORT.md` — canonical markdown report (source of truth, pre-existing).
- `report/REPORT.tex` — LaTeX version of the report (this backfill).
- `report/open_questions.json` — 5 open questions in machine-readable form.
- `report/open_questions_section.tex` — LaTeX open-questions section (input by
  REPORT.tex).
- `report/workflow.md` — step-by-step recipe (paper → build → runs → judge →
  verdict).
- `report/failure_analysis.md` — honest critique of the replication (gaps,
  scope-limits, unresolved threats to reproducibility).
- `report/artifacts_summary.md` — this file.

## Evidence

- `report/evidence/perstate_energies.csv` — per-state excitation-energy comparison
  (FCI / MC-VQE / CIS) for N=8 and N=12.
- `report/evidence/perstate_oscillator.csv` — per-state oscillator-strength
  comparison.
- `report/evidence/summary.json` — headline metrics in JSON form
  (max/mean errors, C5 residual, iteration counts).
- `report/evidence/judge_gpt-5.2.json` — free Argo `argo:gpt-5.2` LLM-judge
  output on the raw combined metrics (PARTIAL, coverage 7/10, agreement 5/10).

## Working code

- `work/QC-MC-VQE-exciton.py` — from-scratch NumPy/SciPy MC-VQE (exciton
  builder, FCI, CIS, MC-VQE, oscillator strengths); handles N=8 stack.
- `work/run_ring12.py` — driver for the N=12 cyclic LH2-type ring.
- `work/mcvqe_judge.py` — LLM-judge harness (free Argo endpoints only).
- `work/results_combined.json` — combined N=8 + N=12 results consumed by the
  judge.

## Extraction

- `extraction/nougat.mmd` — placeholder / stub. Full Nougat PDF→LaTeX
  extraction of the paper was not run in this replication (paper equations were
  transcribed manually from PDF + arXiv source; supplemental TeraChem numbers
  are absent from arXiv). The stub records this decision.

## Verdict (preserved)

**REPLICATED** — core claims C1, C2, C3, C5, C7 independently reproduced;
C4 magnitude reproduced; C6 partial (converges but slower than paper) and full
N=18 scale not completed within budget. See `REPORT.md` §5 and
`failure_analysis.md` for the honest scope of the reproduction.
