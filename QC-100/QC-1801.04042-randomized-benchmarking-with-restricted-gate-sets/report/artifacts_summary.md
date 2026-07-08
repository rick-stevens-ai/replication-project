# Artifacts Summary — QC-1801.04042 (Brown & Eastin 2018)

Standard 8-artifact layout (post-backfill 2026-07-06).

## Report artifacts (`report/`)
1. `REPORT.md` — primary narrative (paper summary, claims table, method, results, verdict, LLM-judge).
2. `REPORT.tex` — LaTeX render of REPORT.md with the same technical content + honest critique section.
3. `open_questions.json` — 5 truly-open questions with `basis` + `next_steps`, as bare JSON list.
4. `open_questions_section.tex` — LaTeX version of the same 5 open questions, ready to `\input` into a compilation.
5. `workflow.md` — chronological reconstruction of the replication workflow.
6. `artifacts_summary.md` — this file.
7. `failure_analysis.md` — honest critique of gaps, unknowns, and things not tested.
8. `brief.md` — one-paragraph what/why (pre-existing).
9. `attempt_log.md` — pre-existing chronological log with bugs and fixes.
10. `artifact_harvest.md` — pre-existing record of public artifacts pulled.

## Extraction artifacts (`extraction/`)
- `nougat.mmd` — Nougat-style scientific-Markdown stub of the paper (backfill 2026-07-06).
- Original PDF at `work/paper.pdf`; plain-text extract at `work/paper.txt`.

## Evidence artifacts (`report/evidence/`)
- `results.json` — low-stats (60 seq/length) symmetric-noise λ_fit for Exps 1, 2, 3a, 3b.
- `results_asym.json` — low-stats asymmetric-noise λ_fit for |00⟩ and |++⟩.
- `results_baseline_hi_n.json` — 400 seq/length full-Clifford re-run.
- `results_hi_stats_with_errorbars.json` — 250 seq/length × 300 bootstrap resamples for the two critical cases.
- `run2.log`, `run_asym.log`, `run_hi_n.log`, `run_hi_stats.log` — full stdout from each simulator run.
- `rb_decay_symmetric.png`, `rb_decay_asymmetric.png` — decay figures.
- `judge_verdict.json` — Argo LLM-judge output (model: `argo:gpt-5.2`, verdict: REPLICATED / high confidence).

## Working code (`work/`)
- `rb_replication.py` — main harness (full Clifford, real Clifford, CNOT+Pauli, symmetric depolarizing).
- `rb_asym.py` — asymmetric pure-Z noise stress test (block-selection falsification).
- `rb_baseline_high_n.py` — high-stats baseline for the |00⟩ full-Clifford case.
- `rb_final_hi_stats.py` — bootstrap error-bar computation.
- `make_figure.py` — matplotlib figure generation.
- `llm_judge.py` — Argo LLM-judge invocation script.
- `paper.pdf`, `paper.txt` — source paper.

## Verdict + verdict provenance
- **Verdict: REPLICATED.**
- Load-bearing evidence: CNOT+Pauli |++⟩ under Z_ERROR(0.02) gives λ_fit = 0.94672 ± 0.00758 vs theory 0.94720 (0.06σ), while |00⟩ under the same noise gives λ_fit = 1.0000 exactly. The same-noise-different-initial-state block selection is quantitatively confirmed.
- Independent LLM judge (`argo:gpt-5.2`) concurs: REPLICATED / high confidence. Cited weakness: random-walk subgroup sampling not formally proved uniform; only n=2 shown.

## Compute footprint
- All simulation local, m1 CPU; Stim tableau backend.
- Argo LLM-judge: free endpoint (per Rick's free-endpoint-only policy).
- No paid API calls, no cloud GPUs, no downloaded datasets beyond the arXiv PDF.
