# Attempt Log

**Session:** 2026-07-06 14:08–14:15 CDT, CherryRd, subagent depth 1/1, label QC-quant-ph-0503205.

| Time | Action | Outcome |
|------|--------|---------|
| 14:08 | Read WAVE_BRIEF and REPLICATION_DIR_STANDARD | OK — 8-artifact bar, free-endpoint only |
| 14:08 | `mkdir -p` target dir + subdirs; `curl` paper PDF | 138 kB, 13 pp saved |
| 14:09 | Checked for existing central-corpus parses | Found `QC-200/QC-quant-ph-0503205-.../extraction/{marker.md,nougat.mmd}` from 2026-07-05 |
| 14:09 | Copied Marker + Nougat parses into `extraction/` | Verified both readable; marker is pdftotext-fallback, nougat is real |
| 14:10 | Read §1–§5 of paper | Understood: `U R_s U† R_t U`, recursion `U_{m+1} = U_m R_s U_m† R_t U_m`, identity `P = 1 − ε^(3^m)` |
| 14:10 | `python3 -m venv work/.venv`; `pip install numpy matplotlib` | numpy 2.5.1, matplotlib 3.11.0 |
| 14:11 | Wrote `work/pi3_search.py` (240 LOC) | Pure numpy statevector: Hadamard, phase shifts, both algorithms, figures |
| 14:11 | Ran `pi3_search.py` | All 5 recursion levels match theory to 1e-14; standard Grover peaks/dips as expected; monotone=True; 2 PNG figures written |
| 14:11 | Wrote `work/llm_judge.py` (130 LOC, Argo POST) | — |
| 14:12 | First LLM call: `argo:claude-opus-4.7` | HTTP 502 Bad Gateway (Argo proxy) |
| 14:12 | Verified Argo endpoint alive with `argo:gpt-4o` smoke test | 200 OK, gpt-4o responds |
| 14:12 | Swapped judge model to `argo:gpt-4o`; re-ran | Clean JSON verdict: REPLICATED, coverage 1.0, agreement 1.0 |
| 14:13 | Wrote REPORT.md | ~10 kB, section-by-section |
| 14:14 | Wrote REPORT.tex | ~9 kB, LaTeX detailed report |
| 14:14 | Wrote open_questions.json | 5 questions, each `{q, basis, next_steps}`, all grounded in what the sim actually surfaced |
| 14:14 | Wrote workflow.md, artifacts_summary.md, failure_analysis.md, brief.md, artifact_harvest.md, this file | 8-artifact bar met |
| 14:15 | Verified all 8 required artifacts present + read `.DS_Store` cleanup not needed (mac invisible files) | Ready to print WAVE_RESULT |

## What worked first-try
- numpy statevector: perfect match to 1e-14 with no debugging.
- Standard Grover Nielsen–Chuang convention: peak at k=3 as expected.
- Monotonicity of π/3 recursion: True on first run.
- Central-corpus text extraction copy (no need to run Marker/Nougat locally).

## What needed a retry
- Argo `argo:claude-opus-4.7` HTTP 502 → switched to `argo:gpt-4o` (also free, both on the same proxy). No other retries.
