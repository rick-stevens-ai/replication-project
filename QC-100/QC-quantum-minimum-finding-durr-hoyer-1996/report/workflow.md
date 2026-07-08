# Workflow, tools, and effort estimate

## Workflow narrative

1. **Read brief + standard.** Parsed `WAVE_BRIEF_2026-07-01.md` and
   `REPLICATION_DIR_STANDARD_2026-07-05.md`. Identified 8 mandatory artifacts and
   verdict vocabulary.
2. **Fetch paper.** `curl -sL https://arxiv.org/pdf/quant-ph/9607014 -o paper.pdf`.
3. **Fetch extractions.** Found existing sibling `QC-200/QC-quant-ph-9607014-durr-hoyer-quantum-minimum`
   with Marker+Nougat already run; copied `extraction/marker.md` and `extraction/nougat.mmd`
   (deterministic PDF text). Left QC-200 untouched (Rick's no-overwrite rule).
4. **Read paper.** Extracted core claims C1–C4 from `extraction/marker.md`.
5. **Implement.** Wrote `durr_hoyer_independent.py` from scratch in pure NumPy
   (statevector, ~250 LOC). Implemented Grover core, BBHT, outer DH loop, and
   experiment driver with dataclass summaries + JSON serialization.
6. **Sanity check.** Wrote `grover_sanity.py` to cross-check the Grover core
   against the closed-form success probability across an (N, k) grid.
7. **Main run.** N ∈ {4, 8, 16, 32, 64}, 300 trials each, seed=20260706.
8. **First LLM judge.** Argo `argo:claude-opus-4.7/4.8` returned HTTP 502 for 3
   retries each (upstream Argo hiccup); auto-fallback to `argo:gpt-5.2` produced a
   PARTIAL verdict flagging missing t-sweep + missing classical baseline.
9. **Address gaps.** Wrote `bbht_t_sweep.py` (21 (N, t) cells, 300 trials each) and
   `classical_baseline.py` (100 trials per N ∈ {4..512}). Both ran <2s wall.
10. **Second LLM judge.** Re-ran with the richer evidence. Still PARTIAL (same
    model), but now C3 and C4 both graded REPRODUCED; only C1 downgraded to
    PARTIALLY REPRODUCED due to no stress test of the ≥1/2 bound tightness.
11. **Write artifacts.** REPORT.md, REPORT.tex, brief.md, attempt_log.md,
    artifact_harvest.md, open_questions.json, workflow.md, artifacts_summary.md,
    failure_analysis.md.
12. **Attempt PDF compile.** Ran `pdflatex REPORT.tex` on CherryRd; fell back to no-PDF
    if unavailable (standard says "when possible").

## Tools / code used

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14.6 (Homebrew) | interpreter |
| NumPy | 2.4.3 | statevector arithmetic |
| curl | system | paper fetch |
| shasum | system | checksums |
| Argo LLM proxy | localhost:44497 (free, key=stevens) | LLM-judge |
| Judge model | argo:gpt-5.2 (fallback after argo:claude-opus-4.7/4.8 502) | verdict |

Scripts (all in `work/`):

- `durr_hoyer_independent.py` — 250 LOC — main replication.
- `grover_sanity.py` — 60 LOC — Grover-core cross-check.
- `bbht_t_sweep.py` — 60 LOC — BBHT scaling measurement.
- `classical_baseline.py` — 45 LOC — classical baseline.
- `llm_judge.py` — 130 LOC — Argo LLM-judge harness with fallbacks.

## Effort estimate

| Bucket | Estimate |
|--------|----------|
| Read paper + brief + standard | 2 min |
| Implement `durr_hoyer_independent.py` | 8 min |
| Grover sanity script | 2 min |
| Main run + debugging (none needed) | <1 min |
| BBHT t-sweep script + run | 3 min |
| Classical baseline + run | 1 min |
| LLM-judge harness + 2 rounds | 4 min |
| Write all 8 artifacts | 12 min |
| **Total wall-clock** | **~33 min** |
| **Total compute wall** | **< 5 seconds** (all runs) |
| **Total LOC written** | ~550 (Python) + ~600 (LaTeX/Markdown docs) |
| **Judge tokens** | ~2 × ~15 K input / ~4 K output |
| **Ext. datasets pulled** | 1 (paper PDF, 77 KB) |
