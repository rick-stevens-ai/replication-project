# Attempt log — chronological

- **10:10 CDT** Task received. Read WAVE_BRIEF_2026-07-01.md. Discovered
  an existing sibling replication (`PDE-allen-cahn-maxprinciple-shen-zhang-2021`,
  from 2026-07-02) covering same paper. Per wave brief rule "Preserve
  completed work. Do not overwrite existing sibling replication dirs.
  Write ONLY inside your assigned target dir", I proceed with an
  **independent complementary-angle** replication in my assigned target
  dir. Sibling replicated paper's exact Q2 stencil + Tables 6.1/6.2 +
  operator monotonicity (Thm 3.9). My angle: real time-dependent DMP
  verification in 1D/2D at ε∈{0.01,0.1}, using a well-known compact
  4th-order Laplacian as a complementary probe.
- **10:11** Copied paper.pdf from sibling's `work/` cache (no re-download
  needed; identical PDF, ubcloud arXiv 2104.11813v1).
- **10:12** Checked for marker/nougat on CherryRd and uicgpu: no CLI
  present. Followed corpus convention (used in 90+ other replication
  dirs like BVBRC-122): `pdftotext -layout` as fallback, wrote
  `extraction/marker.md` and `extraction/nougat.mmd` with header notes.
- **10:13** Wrote `work/allen_cahn_dmp.py` (from equations only — no
  paper code). Includes:
  - 1D/2D periodic Laplacians (order 2 standard, order 4 compact)
  - Stabilized IMEX backward-Euler solver with `splu` factorization
  - 6 DMP dynamics runs
  - Manufactured-solution convergence tests, 1D/2D × order 2/4
- **10:14** First run: total wall-clock 1.3 s (small experiments).
  All 6 DMP runs satisfy max|u| ≤ 1. Peak max|u|=0.997 at ε=0.01.
  1D order-2 convergence hits 2.00 asymptotic rate. Order-4 saturates
  at ~6.8e-6 = temporal-error floor from backward-Euler.
- **10:15** Wrote `make_figures.py`, `emit_csvs.py`. Produced 2 PNGs
  (DMP over time, convergence log-log) + 5 CSVs. All in `report/evidence/`.
- **10:16** LLM judge (argo:claude-opus-4.7 via LiteLLM aggregator
  localhost:4000): **HTTP 502**. Also via raw Argo wrapper localhost:44497:
  **HTTP 502**. Body: "Failed to parse upstream response: 1 validation
  error(s): Value at 'choices[0].message' does not match any variant of
  SystemMessage | UserMessage | AssistantMessage | ToolMessage". This is
  reproducible (not transient — retried 3 times over 3 min). Root cause
  looks like LiteLLM's argo-wrapper can't validate Anthropic's response
  shape for our specific prompt (likely a tool_use / refusal content
  block). Falling back to argo:gpt-5.4 which handled it cleanly.
- **10:17** Judge (argo:gpt-5.4) returned clean JSON verdict: C1 =
  OUT-OF-SCOPE, C2 = REPRODUCED, C3 = PARTIAL, C4 = NOT-TESTED, Overall
  = **PARTIAL**. Saved to `evidence/judge_verdict.json`.
- **10:18–19** Wrote all 8 required artifacts: REPORT.md, REPORT.tex,
  brief.md, attempt_log.md (this file), artifact_harvest.md,
  artifacts_summary.md, workflow.md, failure_analysis.md,
  open_questions.json. Cross-checked directory-standard.
- **10:20** Verified 8-artifact completion bar. All present.
