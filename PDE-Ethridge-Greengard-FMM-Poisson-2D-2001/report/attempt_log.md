# Attempt Log

Chronological, single-subagent turn, 2026-07-06 (America/Chicago).

- **08:16** Received subagent task. Read WAVE_BRIEF_2026-07-01.md; confirmed
  target dir does not exist; created skeleton.
- **08:17** Fetched paper metadata via S2 API (Keychain key), got Green OA PDF
  URL. Downloaded `paper.pdf` (2.86 MB), extracted with `pdftotext -layout`.
  Scanned Tables 1-4 to identify testable claims (P1 = FMM engine, P2 = high-
  order adaptive, P3 = HWSCRT timings).
- **08:18** Checked local + uicgpu for FMM libraries (fmm2dpy, pyfmmlib,
  kifmm). None available. Decision: implement own pure-Python FMM engine.
- **08:19-08:21** Wrote `work/fmm2d.py` from scratch. First self-test at
  N=200, p=12: rel err 27%. Sign bug in M2L formula.
- **08:22** Re-derived M2L directly from the log-expansion, encoded the
  derivation into the docstring, fixed the code. Re-tested: rel err 5e-8 at
  p=12. Good.
- **08:23** Wrote `work/run_experiments.py` with 4 experiments C1..C4.
- **08:23** First run: hung (my $N=16000$ + $N_{\rm side}=256$ estimates
  were way too optimistic for pure-Python FMM). Killed, trimmed.
- **08:24** Second run: 65 s wall, all 4 experiments succeeded cleanly.
  C1 shows p=4->1.9e-4 all the way to p=20->2.5e-11. C2 shows expected
  quadratic direct (0.013s->0.521s over N=500->4000). C3 shows uniform-grid
  baseline getting E2 ~ 4% at N_side=128 (paper's high-order gets 4.9e-6
  at similar N). C4 shows FFT Poisson at 1.2e7 pts/s on 2048^2.
- **08:25** Wrote `work/make_plots.py`, generated 4 PNG figures.
- **08:26** Wrote `work/llm_judge.py`. First attempt via argo:claude-opus-4.7
  through localhost:44497: HTTP 502. Retry via localhost:4000: also 502.
  Retry with argo:claude-opus-4.8: also 502.
- **08:27** Isolated the root cause with curl: LiteLLM Pydantic validator
  rejects Argo's Anthropic message shape for large payloads. Switched to
  argo:gpt-5.4: succeeded first try, returned clean strict-JSON verdict:
  PARTIAL with coverage breakdown.
- **08:28** Saved judge verdict JSON.
- **08:29** Created extraction/marker.md (pdftotext fallback with backfill
  header) and extraction/nougat.mmd (pending-central-parse header).
- **08:30-08:40** Wrote all 8 mandatory report artifacts:
  REPORT.md, REPORT.tex, open_questions.json, workflow.md,
  artifacts_summary.md, failure_analysis.md; plus brief.md, attempt_log.md,
  artifact_harvest.md.
- **08:41** Final directory listing verified 8-artifact bar met.

## Model used

- Driver: argo/argo:claude-opus-4.7 (this session's default per Runtime
  header).
- LLM judge: argo:gpt-5.4 via localhost:4000 (FREE endpoint per project
  rule; Argo Opus 4.x models 502'd on this payload -- see failure_analysis.md).

## Total elapsed

~35 minutes wall clock, ~2 minutes of actual compute, ~15 minutes of writing.
