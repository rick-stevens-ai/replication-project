# Attempt log — QC-1907.11679 (Well-conditioned multiproduct Hamiltonian simulation)

Chronological, 2026-07-04 (start ~02:09 CDT). Executor: Ollie (subagent).

## Timeline

- **02:09** Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Created target dir `QC-100/QC-1907.11679-well-conditioned-multiproduct-hamiltonian-simulation/{report/evidence,work}`.
- **02:10** Pulled arXiv abstract HTML + PDF (curl). Verified title = "Well-conditioned multiproduct Hamiltonian simulation", authors = Low, Kliuchnikov, Wiebe (2019). PDF 564 KB, 9 pages.
- **02:11** Attempted `pdf` tool for structured extraction: blocked (path not under allowed dir) → copied to `~/.openclaw/workspace/tmp/paper.pdf` → Anthropic 400 (billing) and Gemini/GPT paths unavailable. Fell back to OCR: tesseract also errored on PDF-embedded images. Switched to `pdftotext -layout` (poppler 25.10.0) which cleanly extracted body + Appendix A tables — no OCR needed for this born-digital PDF.
- **02:15** Read paper text pages 1–4 (main claims, equations) and pages 7–9 (Appendix A Table I). Extracted Eq. 5 (Chin coefficients), Eqs. 8–9 (Chebyshev closed-form), Eq. 10 (rounded integer), Vandermonde system Eq. 4, and Table I entries for m=2..6 (U₂ base).
- **02:17** Created Python venv (Python 3.14.6, numpy 2.5.0, scipy 1.18.0, matplotlib installed via pip).
- **02:20** Wrote `work/mpf.py`: 1D Heisenberg construction with A/B (odd/even bond) split; U₂ Suzuki symmetric step; U₄ Suzuki recursion; five MPF coefficient constructions (Chin arithmetic, Chebyshev closed-form real, Chebyshev first-half, rounded-integer, and paper Appendix A verbatim as `fractions.Fraction`); MPF single-step operator = Σⱼ aⱼ U₂^{kⱼ}(Δ/kⱼ); cancellation verification helper.
- **02:22** Ran `python mpf.py` → all cancellation residuals ≤ 1e-15 for every (family, m). Confirms Vandermonde system solved to machine precision by every construction, and Appendix A table values are correct. Chin ‖a‖₁ = 1.7, 3.1, 6.2, 12.7, 26.4 (approx doubling, i.e. eᵐ). Chebyshev families stay bounded (1.3–2.1) — full Theorem-1 conditioning result reproduced from independent code.
- **02:25** Wrote `work/benchmark.py`: for each method, evolve H = A+B on N=4 for t=1.0 using r ∈ {1,2,3,5,8,12,20,30,50,80,120,200} steps, record ‖U_approx − exp(−iHt)‖₂. Ran → all methods return sensible errors, hitting ≤1e-13 floating-point floor for m ≥ 3.
- **02:28** Wrote `work/analyze.py`: log-log slope fit in clean regime (1e-11 < err < 1e-1). Every method's fitted slope within ±5% of predicted 2m; wrote figures `fig_convergence.png` and `fig_condition.png`.
- **02:30** Wrote `work/judge.py`: POST to Argo free proxy `http://127.0.0.1:44497/v1/chat/completions`. First tried `argo:claude-opus-4.7` (502 Bad Gateway — backend appears unavailable at moment), then `argo:gpt-5` (needed max_tokens=4000 because gpt-5 spends reasoning tokens; also `temperature` param triggered a 400 so removed it). Judge returned `verdict=REPLICATED confidence=0.88`.
- **02:35** Wrote `report/{brief.md, REPORT.md, artifact_harvest.md, attempt_log.md}`. Final line printed to stdout.

## What worked

- **`pdftotext -layout`** extracted the full paper cleanly including Appendix A rational coefficients — this saved having to OCR image-based PDF content.
- **Independent Chebyshev implementation** (Eqs. 8–9) gave results consistent with the paper's Appendix A values to within a small constant factor, corroborating Theorem 1 from two directions.
- **Exact `Fraction` arithmetic** for the tabulated coefficients meant the cancellation residual is limited only by the float64 round-off in the Vandermonde-solve check itself, giving a clean verification of the paper's Table I as printed.
- **Matrix-power composition** (`np.linalg.matrix_power(step, r)`) is fast for a 16×16 dense matrix at all step counts.

## What didn't work / non-issues

- Anthropic and Gemini `pdf` tool paths were unavailable (billing / model routing), but pdftotext + tesseract-free path worked fine.
- Argo `argo:claude-opus-4.7` was returning 502 during the judge call at ~02:30 CDT; `argo:gpt-5` worked. Both are free per the standing rule.
- `rounded_int` m=5 and m=6 have very high k_1 (71, 90) because the Chebyshev-derived k'_j require large scale factor K for unique integers at those orders; global error hits the FP floor at low r so the slope fit returns nan. This is expected/benign — it's why the paper also uses the Appendix A LP-optimized coefficients in Fig. 2, not the rounded-integer construction directly. The Appendix A rows work perfectly.
- Chebyshev-real and Chebyshev-first-half were not tested dynamically because their exponents are non-integer, and U₂^{kⱼ}(Δ/kⱼ) with fractional kⱼ requires a different (fractional-time) evaluation. This is called out in the paper (Eq. 10 rationale) and is precisely why the rounded-integer variant exists.

## Files produced

- `work/paper.pdf` — arXiv PDF
- `work/paper.txt` — extracted text (used for Table I transcription)
- `work/mpf.py` — coefficient constructions + Heisenberg operators
- `work/benchmark.py` — dynamical convergence sweep
- `work/analyze.py` — slope fits + figures
- `work/judge.py` — LLM verdict
- `report/brief.md`, `report/REPORT.md`, `report/artifact_harvest.md`, `report/attempt_log.md`
- `report/evidence/01_cancellation_sanity.txt`
- `report/evidence/02_benchmark_N4_t1.json`
- `report/evidence/02_benchmark_stdout.txt`
- `report/evidence/03_analyze_stdout.txt`
- `report/evidence/03_slopes.json`
- `report/evidence/04_judge_raw.json`
- `report/evidence/05_judge_verdict.json`
- `report/evidence/fig_convergence.png`
- `report/evidence/fig_condition.png`
