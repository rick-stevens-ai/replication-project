# Artifacts Summary — PDE-Bernardi-Darcy-heat-spectral-2016

**Paper:** Bernardi, Maarouf, Yakoubi (2016), IMA J. Numer. Anal., DOI 10.1093/imanum/drv047.
**Verdict:** REPLICATED.

## Code (work/)

| File | Purpose | Key API / output |
|------|---------|------------------|
| `spectral_gll.py` | GLL nodes, weights, differentiation matrix from scratch | `gll_nodes(N)`, `gll_weights(N)`, `gll_diff(N)`; self-tested to ~1e-14 |
| `verify_mms.py` | Symbolic strong-residual check of eq. (5.6) source terms | Prints exact residuals; diagnoses paper typo |
| `darcy_heat_solver.py` | Coupled GLL-Galerkin Darcy + heat solver + N-sweep driver | Writes `evidence/convergence.json`, per-N error tuple + fp iters |
| `analyze.py` | Exponential-rate fits `e^{-bN}`, convergence figure | Writes `evidence/analysis_summary.json`, `evidence/convergence.png` |
| `fig_solution.py` | Exact vs discrete T at N=17 (Fig. 2 replica) | Writes `evidence/solution_compare.png`; max\|T−T_N\| = 1.5e-14 |
| `judge.py` | LLM-judge harness against free Argo endpoints | Writes `evidence/llm_judge_verdict.txt` |

## Source paper

| File | Notes |
|------|-------|
| `work/bernardi_darcy_heat_2016.pdf` | HAL preprint `hal-01085011`, 23 pp., MD5 `2d6ead2ce797287b0718d8cc156a1ecd` |
| `work/paper.txt` | Extracted text |

## Evidence (report/evidence/)

| File | Content |
|------|---------|
| `convergence.json` | Full per-N table: L²(u), L²(p), L²(T), H¹(p), H¹(T), fp iteration count for N = 5..25 |
| `analysis_summary.json` | Fitted `b` per norm; observed floor N; number of pre-floor points used |
| `convergence.png` | Semilog plot: five error curves vs N, straight lines with visible plateau at ~N=16–18 |
| `solution_compare.png` | Fig. 2 replica — exact vs discrete T at N=17, visually indistinguishable |
| `convergence_sweep.txt` | Raw stdout of the N-sweep, one row per N |
| `gll_selftest.txt` | Machine-precision GLL self-test output |
| `mms_residual_printed_sources.txt` | Symbolic dump of the eq. (5.6) typo residuals |
| `llm_judge_verdict.txt` | Full JSON responses from Argo gpt-5.2 and claude-sonnet-4.5 (both REPLICATED) |

## Reports (report/)

| File | Purpose |
|------|---------|
| `REPORT.md` | Source-of-truth narrative report (verdict, method, results, finding) |
| `REPORT.tex` | LaTeX render with a dedicated Genuine Critique section |
| `open_questions.json` | 5 truly open questions grounded in coupled Darcy–heat spectral-method domain |
| `workflow.md` | Chronological reproducible workflow |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Failure log (paper typo, Argo opus-4.8 502, out-of-scope items) |

## Key numeric results (excerpted from REPORT.md § 4)

| N | L²(u) | L²(p) | L²(T) | H¹(p) | H¹(T) | fp iters |
|---|-------|-------|-------|-------|-------|----------|
| 5 | 4.44e-01 | 2.00e-02 | 1.80e-03 | 1.31e-01 | 1.12e-02 | 4 |
| 8 | 5.70e-03 | 1.60e-04 | 1.04e-05 | 1.47e-03 | 7.96e-05 | 4 |
| 11| 2.35e-05 | 3.23e-07 | 1.68e-08 | 4.08e-06 | 2.02e-07 | 3 |
| 14| 4.34e-08 | 4.31e-10 | 2.21e-11 | 6.85e-09 | 3.22e-10 | 2 |
| 17| 4.21e-11 | 2.58e-13 | 1.24e-14 | 5.00e-12 | 2.26e-13 | 1 |
| 20| 3.50e-14 | 4.94e-15 | 2.84e-16 | 2.62e-14 | 5.39e-15 | 1 |
| 25| 4.30e-14 | 1.60e-14 | 3.66e-16 | 4.77e-14 | 8.02e-15 | 1 |

Fitted exponential rates `e^{-bN}`: b ≈ 1.94 (L²u), 2.11 (L²p), 2.15 (L²T), 2.02 (H¹p), 2.05 (H¹T).
Machine-precision floor at N ≈ 16–18. Fig. 2 replica: max|T−T_N|_{N=17} = 1.5e-14.

## What was NOT produced (out of scope)

- Existence/uniqueness proofs (C7 — theoretical, cannot be numerically replicated).
- Re-derivation of the a priori estimate (4.16) (C6 — indirectly confirmed by observed decay).
- Horton–Rogers–Lapwood physics demo (C8 — no error metric, no manufactured solution;
  qualitative-only in the paper).
- 3D convergence sweep on Ω = (−1,1)³ (paper's Fig. 1 shows only 2D; noted as open question).
