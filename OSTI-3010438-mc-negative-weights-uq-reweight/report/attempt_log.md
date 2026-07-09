# Attempt log — OSTI 3010438 replication

## 2026-07-05 22:08 CDT (start)

1. **Read WAVE_BRIEF_2026-07-01.md.** Note constraints: free endpoints only, LLM-judge required,
   no fabrication, no-overwrite, 8-artifact bar.
2. **Create target dir** `~/Dropbox/REPLICATE-PROJECT/OSTI-3010438-mc-negative-weights-uq-reweight/`
   with `work/`, `report/evidence/`, `extraction/`.
3. **Fetch paper** — `ssh uicgpu` with `~/env.sh` proxy env (direct curl blocked by proxy),
   then `scp` to workspace. 9.16 MB PDF.
4. **Text extract** via `pdftotext -layout` → 1094 lines. All equations preserved in Unicode,
   tables in layout form.
5. **Read paper in full** via `sed -n` chunks (100-400, 400-700, 700-1094). Identify:
   - Domain: UQ / HEP MC negative-weights reweighting
   - Core mathematical claim: PDF = g·(a·PDF+ + b·PDF-)
   - Section III.A: fully self-contained double-slit MC (α=1, δ=0.25) — ideal for replication
   - Sec. V: HEP Sherpa V+jets + ATLAS OpenData — out of scope
6. **Enumerate claims C1-C7** in report structure.
7. **Write `replicate_double_slit.py`** (~500 lines) with 6 subclaim tests:
   - C0 analytic sanity (PDF forms, g identity, ∫ over sampling range)
   - C1 Eq.1 sample scaling (Poisson-1 counts with fixed signs)
   - C2/C3/C4 double-slit MC (rejection sampling per Table I)
   - C5 P+ closure (Fig. 4 counterpart)
   - C6 Eq.38 threshold (fully-correlated toy)
8. **Debug run 1 (T+15m):** `AttributeError: 'trapz'` — NumPy 2.x deprecated. Fix `→ trapezoid`.
9. **Debug run 2 (T+18m):** Reweighted integral 0.62 vs truth 0.897 — 30% bias.
10. **Root-cause 2:** Two bugs: (a) `P_interf` sampling used `abs(P_interf)` instead of
    `max(0, P_interf)` for pos-part and `max(0, -P_interf)` for neg-part; (b) reweighted
    estimator was `Σ w_signed · g` but should be `Σ |w| · g` per Eq. 6's identity.
11. **Fix both bugs.** Re-run: unbiased-mean `integrals_rw_mean = 0.8976 ± 0.0052` vs truth `0.897`. ✓
12. **Debug run 3 (T+35m):** C1 f_MC values ~2× off from paper.
13. **Root-cause 3:** MC used Bernoulli sign draws (variance `4P+(1-P+)`) but paper's Eq. 1
    assumes fixed signs + Poisson-1 counts (variance `1`).
14. **Fix C1.** Redraw signs once, iterate Poisson counts. Now within few-percent tolerance.
15. **Generate plots** with `make_plots.py` — Fig. 2 (P_base/P_interf/g) and Fig. 3
    (nom/rw/truth histograms + pulls + var ratios) counterparts.
16. **Write `llm_judge.py`.**
17. **Debug run 4 (T+45m):** Argo returns 502 with `temperature=0.0`.
18. **Root-cause 4:** Argo Claude proxy rejects `temperature=0.0` (upstream returns unparseable
    response). Remove `temperature` param → works.
19. **LLM judge success (T+55m):** all C1-C6 REPLICATED, overall PARTIAL (excluding C7).
20. **Write REPORT.md, REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md,
    open_questions.json** (T+65m).
21. **Final directory verification** — all 8 required artifacts in place.
22. **Emit WAVE_RESULT.**

## Total elapsed

~75 minutes wall-clock from `cat WAVE_BRIEF` to WAVE_RESULT emission. Three debugging cycles
totalling ~15 minutes. No blockers; all failures resolved within the run.
