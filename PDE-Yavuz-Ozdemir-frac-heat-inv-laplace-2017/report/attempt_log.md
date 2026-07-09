# Attempt Log — 2026-07-04 (subagent run)

Chronological trace of what was done during this replication attempt.

## 12:08 — start
- Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Yavuz-Ozdemir-frac-heat-inv-laplace-2017/` with `report/`, `work/`, `report/evidence/`.

## 12:09 — PDF hunt
- Tried `https://doi.org/10.2298/TSCI170804285Y` and `http://www.doiserbia.nb.rs/img/doi/0354-9836/2017/0354-98361705295Y.pdf`: HTTP 503 (Serbian OA gateway down at the time).
- Tried the same URLs from `ssh uicgpu` (proxied network): also 503.
- Queried Crossref → learned real citation is `vol 22, Suppl. 1, pp. 185-194, 2018` (submitted Aug 2017, published 2018), so the year suffix in the vinca URL should be `papers-2018`, not `papers-2017`.
- Fetched `https://thermalscience.vinca.rs/pdfs/papers-2018/TSCI170804285Y.pdf` from uicgpu: HTTP 200, 867,501 B, PDF v1.4, 10 pages.
- `scp` back to CherryRd; SHA-1 `3fda2ba1872f1a267898f01613dea7b28c2bebb9`.

## 12:12 — paper transcription
- `pdftotext -layout paper.pdf` → `paper.txt` (642 lines).
- Manually transcribed:
  - Method: eqs (1)-(14), Stehfest formula.
  - Example 1: fractional Burgers PDE (eq 15), IC (16), exact for α=1 (eq 17), LHPM recurrence (eq 18), closed-form H (eq 19), collapse to x²+t² (eq 20).
  - Example 2: fractional heat with source (eq 21), zero IC (22), recurrence (23), H series (24), infinite series (eq 25), α=2 special case (eq 26) → noise-cancelled to u=x³t³ (eq 27).
  - Example 3: fractional heat with source (eq 28), IC (29), BC (30), exact (eq 31), recurrence (32), H (eq 33), u_n (eq 34), infinite (eq 35), Table 1 verbatim.

## 12:15 — implementation `work/lhpm.py`
- Python 3.14 venv with `mpmath 1.4.1`, `numpy 2.5.1`, `scipy 1.18.0`.
- Implemented Stehfest coefficients via exact `Fraction` (float precision) and via `mpmath` (arbitrary precision) — cross-verified they agree.
- Implemented Stehfest inversion `stehfest_invert(F, t, p, use_mpmath)`.
- Implemented `example1_H(x, s, alpha)` = x²/s + 2/s³ (paper's eq 19).
- Implemented `example3_H(x, s, alpha, n_terms)` = 2(2x - x²)/s³ + 8/s³ · Σ_{k=0..n_terms-1} 1/s^{(2k+1)α} (paper's eq 33).
- Implemented `example3_exact(x, t, alpha, k_max)` = x(2-x)t² + Σ_k 8 t^{(2k+1)α+2} / Γ((2k+1)α+3) (paper's eq 31), summed to 300 terms at 50 dps.

## 12:17 — Example 1 verification
- Run `python lhpm.py` at p=8 Stehfest, mpmath 30 dps.
- Across (x∈{0.5, 1.0}, α∈{0.25, 0.5, 0.75, 1.0}, t∈{0.25, 0.5, 0.75, 1.0}): max |u_stehfest - (x²+t²)| = **2.588e-07**.
- Confirms: LHPM gives exact H = x²/s + 2/s³ (all Ψ_{j≥3} vanish, independent of α), Stehfest recovers x²+t² to expected numerical precision for p=8. **CLAIM C1 CONFIRMED.**

## 12:19 — Example 3 first pass
- Same run, at p=8, n_terms∈{3,5,8,12}, α∈{0.25,0.40,0.75}, (x,t) on paper grid.
- Analytic truncation error is tiny for α=0.75 (~10⁻⁴⁰ at n=12) but Stehfest numerical error at large t degrades badly:
  - α=0.25, t=0.9: err ≈ 1.08e-3 (paper reports 1.7e-9).
  - α=0.75, t=0.9: err ≈ 4.52e-4 (paper reports 7.0e-9).
- Immediate concern: my Stehfest reconstruction of u_n at t=0.9 is 5-6 decades worse than paper.

## 12:22 — parameter sweep to find best (p, n_terms) match
- `e3_sweep.py`: swept p ∈ {4,5,6,7,8,10,12,16} × n_terms ∈ {3,5,8,12,20,40}.
- Best std of log₁₀(my_err/paper_err) at p=4 n=3 (but bias +6.8 decades).
- Best mean bias (close to 0) at p=12 n=12: mean_log10 = -0.38, std = 3.06.
- Even the best (p, n) combo cannot match paper's specific cell values — std_log ~3 means individual cells vary by ~1000x from paper.
- Interpretation: paper's Table 1 shows non-monotonic near-random-looking magnitudes that look consistent with implementation-specific finite-precision roundoff in whatever CAS/software they used; the overall magnitude range 1e-10 to 5.7e-7 is broadly consistent with LHPM + Stehfest at small t but NOT at t=0.9.

## 12:26 — final canonical run
- `e3_final.py` at p=8, n_terms=12 (defensible defaults).
- 75 cells (5x × 5t × 3α). Summary:
  - Median log₁₀(my_err/paper_err) = **+3.68** (my errors ~5000× larger, median).
  - Std log₁₀ ratio = 2.50.
  - Cells within ±1 decade of paper: **18/75 = 24%**.
  - Min replication err: 1.01e-08 (small t, small α).
  - Max replication err: 1.31 (α=0.25, t=0.9, x=0.5 — Stehfest fully unstable).
- Written to `e3_final_table.json`.

## 12:30 — Example 2 verification
- `e2_verify.py`: directly summed paper's eq (25) at α=2 for (x, t) values and compared to claimed limit u=x³t³.
- At (x=1, t=1): sum = **1.307** vs claim = **1.000**, error = 0.307.
- At (x=0.5, t=1): sum = 0.279 vs claim = 0.125, error = 0.154.
- Fig 1 shape at α=1.6, 1.9 (x=0.5, t=0..1) approximately matches paper's plotted curves.
- α=1.3 diverges more strongly.
- Interpretation: the paper's α=2 → x³t³ collapse is only obtained after **subjective identification and manual cancellation of specific "noise terms"** in eq (26). This is a documented weakness of He's HPM method — not a robust algorithmic collapse.

## 12:34 — LLM judge (argo → GPT-5.2 fallback)
- Preferred model per brief: `argo:claude-opus-4.7`. Argo proxy is up (small requests return cleanly) but Claude Opus consistently returns HTTP 500 "Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage" for this specific replication-judge prompt (four different attempts with varying max_tokens, system prompts, and prompt lengths). This is an upstream/proxy contract issue independent of the judge task.
- Switched judge model to `argo:gpt-5.2` (also a free Argo-proxied endpoint, allowed by wave brief hard-rule set) with the same prompt — clean response, verdict **PARTIAL**.
- Judge reasoning: C1 fully confirmed, C2 requires manual noise-cancellation, C3 quantitatively non-reproducible; agreement 45%, coverage 100%.

## 12:38 — cleanup + report
- Files finalized:
  - `report/brief.md`
  - `report/artifact_harvest.md`
  - `report/attempt_log.md` (this file)
  - `report/REPORT.md`
  - `report/evidence/e3_final_table.json`, `e3_sweep_results.json`, `judge_gpt52_response.json`, `judge_verdict.txt`, `paper.txt`
  - `work/lhpm.py`, `work/e3_sweep.py`, `work/e3_final.py`, `work/e2_verify.py`, `work/llm_judge.py`, `work/llm_judge2.py`, `work/paper.pdf`
