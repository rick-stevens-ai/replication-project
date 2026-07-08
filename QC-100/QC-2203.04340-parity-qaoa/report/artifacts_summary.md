# Artifacts Summary — QC-2203.04340

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2203.04340-parity-qaoa/`

## Original (pre-backfill)
- `report/REPORT.md` — full replication report (Markdown), 6.5 KB. Verdict: REPLICATED.
- `report/evidence/results.json` — per-instance E_res + fidelity for 24 seeds across nr in {0.0, 0.4, 0.6, 1.0} plus standard-QAOA baseline; medians and IQRs.
- `code/parity_qaoa.py` — ~600 LoC, numpy-only statevector simulator. Independent reimplementation, no Qiskit.
- `logs/full_run.log` — per-instance progress log, 24 lines + summary block.
- `work/2203.04340.pdf` — the paper.
- `work/2203.04340.txt` — pdftotext dump for grep.
- `venv/` — numpy 2.5.0, scipy 1.18.0, networkx 3.6.1.

## Backfill (added 2026-07-06)
- `report/REPORT.tex` — LaTeX render of the report with an explicit Honest Critique section (7 numbered caveats). `\input{open_questions_section.tex}` at end.
- `report/open_questions.json` — **bare JSON list of exactly 5 objects** `{q, basis, next_steps}` (no wrapper dict). Follow-ups on weighted / higher-order Ising, error mitigation (ZNE + symmetry verification), device-level depth vs SWAP-compiled standard QAOA, constraint-strength scheduling, moderate-N modularisation depth.
- `report/open_questions_section.tex` — LaTeX version of the same 5 questions, `\input`ed by REPORT.tex.
- `report/workflow.md` — end-to-end workflow: acquisition → claim extraction → environment → simulator design → sanity → run → verdict → backfill.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique: what was NOT tested (noise, weighted Ising, larger N, alternate optimisers, real device compilation), plus per-claim confidence.
- `extraction/nougat.mmd` — stub only. Nougat OCR was NOT run for this paper; extraction used pdftotext (already sufficient for QAOA equations and Fig. 7 markers). See file header.

## Headline exercised?
**YES.** The paper's headline (Fig. 7 noiseless panel: monotone
$E_{\mathrm{res}}(n_r)$ + inverse monotone fidelity + implicit parity
QAOA $\gg$ standard unencoded QAOA) was reproduced from a
first-principles independent simulator. Verdict `REPLICATED` is
substantively earned.

## Not exercised
- Fig. 6 depth scaling across N in {8, 10, 12, 15}.
- Fig. 7 CNOT-noise sweep (only y-intercept done).
- Fig. 5 modular construction for large N.

## Verdict (preserved)
**REPLICATED.**
