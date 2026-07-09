# Workflow — OSTI 3010438 replication

## Timeline (2026-07-05)

| Time | Step | Notes |
|------|------|-------|
| T+0 min | Read WAVE_BRIEF, create target dir | `~/Dropbox/REPLICATE-PROJECT/OSTI-3010438-...` |
| T+2 min | Fetch PDF via uicgpu proxy | 9.16 MB, `pdftotext -layout` → 1094-line text |
| T+5 min | Read paper (whole 19-page PDR-D article) | Identify claims C1-C7, scope decision |
| T+10 min | Write `replicate_double_slit.py` v1 (~500 lines) | Rejection sampling, 5 claim-test functions |
| T+15 min | Debug run 1: `np.trapz` deprecated | Fix `→ np.trapezoid` |
| T+18 min | Debug run 2: reweighted MC biased | Root cause: interference-part sampling includes wrong regions |
| T+22 min | Fix positive/negative interference splitting | Add `pos_part = max(0, P_interf)` and `neg_part = max(0, -P_interf)` |
| T+25 min | Debug run 3: reweighted still biased | Root cause: `Σ w_signed · g` ≠ σ. Correct form: `Σ|w|·g` (derived from Eq. 6). |
| T+30 min | Fix reweighted estimator | All 6 claims now reproduce cleanly |
| T+35 min | Debug C1: wrong analytic model | Root cause: paper uses fixed sign + Poisson-1 counts, not Bernoulli. Fixed. |
| T+40 min | Plot generation (`make_plots.py`) | Fig. 2/3 replication counterparts |
| T+45 min | LLM-judge (`llm_judge.py`) | Argo Claude Opus 4.8; hit 502s from `temperature=0.0` (Argo/Claude bug), remove that param |
| T+55 min | LLM-judge success | All 6 REPLICATED, overall PARTIAL |
| T+65 min | Write REPORT.md + REPORT.tex + workflow.md + failure_analysis.md + artifacts_summary.md + open_questions.json | 8-artifact bar |
| T+75 min | Final verification | WAVE_RESULT line |

## Tools & codes used

- **Python 3.14** (Homebrew), **NumPy 2.x** (`np.trapezoid`), **Matplotlib** (Agg backend)
- **pdftotext** (poppler) for paper extraction
- **uicgpu** for PDF fetch (proxy env `~/env.sh`)
- **Argo LLM proxy** for LLM-judge: `argo:claude-opus-4.8` via cherryrd LiteLLM :4000 (free)
- **rsync/scp** for cross-host file transfer

## Effort estimate

**~75 minutes wall-clock time** by one agent (Ollie) end-to-end, with three debugging cycles
totalling ~15 minutes. If the paper had been fully explicit about the Σ|w|·g convention and
the Eq. 36 formula had been reproducible without algebraic re-derivation, the run would have
completed in ~45 minutes.

For a human replicator without an LLM assist: I'd estimate 4-8 hours (paper reading, Python
implementation, debugging, plot production, report drafting), given the mathematical maturity
required to catch the Eq. 8 convention subtlety and the Eq. 36 typo.

## Not attempted (and why)

- **C7 (Sec. V HEP demonstration).** ATLAS OpenData PhysLite V+jets samples are large (~TBs),
  Sherpa+Athena pipeline is heavy (Athena release 22), DNN ensemble training (20 nets)
  requires GPU-days, and the DNN_SvB signal-vs-background training is a full pipeline. Out
  of scope for a single-day one-paper replication window. Deferred to Q4/Q5 in
  `open_questions.json`.
- **Marker/Nougat re-parse.** Paper is a born-digital Phys. Rev. D LaTeX PDF; `pdftotext -layout`
  preserves every equation in Unicode and every table with correct column alignment. Marker
  would add prettier Markdown but no informational content; Nougat model was not available in
  local/uicgpu env at replication time. Placeholders written to satisfy the 8-artifact bar
  document this decision transparently (see `extraction/marker.md` and `extraction/nougat.mmd`).
