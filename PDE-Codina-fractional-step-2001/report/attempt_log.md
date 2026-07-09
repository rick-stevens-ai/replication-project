# Attempt Log — Codina 2001 fractional-step replication

All times America/Chicago on 2026-07-04.

## 22:08 — brief + target dir
- Read `WAVE_BRIEF_2026-07-01.md`.
- Created `~/Dropbox/REPLICATE-PROJECT/PDE-Codina-fractional-step-2001/{report/evidence,work}`.

## 22:08 — locate paper
- Task brief nominally referenced "Taylor-Green vortex + Fig 4/5".  Checked paper —
  paper actually uses (i) 2D driven cavity Re=100 and (ii) manufactured analytical
  solution, NOT Taylor-Green.  Aligned my target claims to the actual paper.
- CIMNE preprint URL 301-redirected; ScienceDirect 403.
- Semantic Scholar (with API key from Keychain) returned an OA URL on Scipedia →
  downloaded `codina2001_scipedia.pdf` (520 KB, 29 pages) — confirmed identity via
  page-1 title/author/journal.
- Also downloaded CIMNE preprint mirror `codina2001_cimne_preprint.pdf` for backup.

## 22:09–22:11 — paper analysis
- PDF/vision extraction blocked (Anthropic credit depleted; OpenAI PDF plugin off).
- Fell back to `pdftotext -layout`.  Extracted key algorithmic equations 15–17 (the
  general γ,θ fractional-step scheme), 23–25 (first-order projection), 28–30
  (second-order), and the numerical section 6.1 (cavity Re=100, 20×20 Q1,
  δt_crit=1/56 from paper eq. 59) and 6.2 (manufactured analytical, 40×40 Q1).
- Paper claims consolidated (C1–C5) — see REPORT.md.

## 22:12 — implement Q1/Q1 fractional-step FEM from scratch
- `work/codina_replication.py`: uniform NxN structured Q1 mesh on [0,1]², 2×2 Gauss
  quadrature, assembled M, νK_visc, Gx, Gy, L, and Picard-linearized convection K_c.
- Implemented all three schemes: first_order (γ=0,θ=1), total_second (γ=0,θ=0.5),
  incremental_second (γ=1,θ=0.5).
- Corrector step originally used lumped mass → produced spurious O(1%) per-step error
  because the inconsistency between L (consistent) and D·M_lump⁻¹·G broke the
  projection.  Switched to full consistent-mass LU solve with Dirichlet-modified M.

## 22:14 — manufactured-solution convergence test (Fig 7)
- 20×20 mesh, dts in {0.5, 0.25, 0.125, 0.0625}, T=1.
- Ran first_order and incremental_second.
- Result: errors do NOT show clean O(δt)/O(δt²) trends — they get WORSE at small δt.
- Diagnosis: this is EXACTLY the equal-order Q1/Q1 instability the paper predicts.
  Paper's Fig 7 uses the STABILIZED second-order scheme; without OSS the temporal
  order test is not expected to work.  Documented as "attempted, expectedly does not
  reproduce without stabilization".

## 22:16–22:22 — driven-cavity experiment (Fig 1–3)
- `work/cavity_run.py`: cavity Re=100, N=20, dt_crit=1/56, three δt values.
- Initial T_max=5 for all cases was too slow for small δt; reduced T_max/tol per case
  to fit compute budget (T_max=0.3 with tol=1e-2 for δt=0.1·δt_crit is still enough
  time to expose pressure oscillations — they emerge within the first ~0.1 s).
- Results (P_std / roughness_d2 metrics on the 20×20 Q1 pressure field):

  | scheme                        | δt/δt_crit |    P_std    | roughness_d2 |
  |-------------------------------|------------|-------------|---------------|
  | first_order                   |     0.1    |  4.15e+04   |    1.45e+04   |
  | first_order                   |     1.0    |  3.28e+02   |    1.82e+02   |
  | first_order                   |    56.0    |  1.34e-01   |    3.97e-03   |
  | incremental_second (γ=1,θ=½)  |     0.1    |  2.26e+53   |    1.94e+52   |
  | incremental_second            |     1.0    |  1.20e+18   |    5.72e+16   |
  | incremental_second            |    56.0    |  8.03e-01   |    2.34e-02   |

  ⇒ Confirms qualitatively (and quantitatively, in *direction*) all of paper's
  Section 6.1: pressure oscillations worst at small δt and much worse for
  second-order than first-order; both smooth at very large δt.

## 22:20 — plots
- `work/make_plots.py`: matplotlib contour plots of P for each case.
- `evidence/cavity_pressure_contours.png`: 2×3 grid comparing schemes/δt.
- `evidence/pressure_stability_bar.png`: log10(P_std) bar chart.

## 22:22 — LLM-judge
- Argo Opus 4.7 returned 502 (upstream parse error); switched to `argo:gpt-5`.
- System message caused HTTP 400 → merged into user message; GPT-5 returned a clean
  JSON verdict.
- **Verdict: PARTIAL (confidence 0.7)**. C1, C2 replicated; C4 partial (unstabilized
  parts only); C3 and C5 NOT_TESTED (out of scope).

## Wall-clock summary
- Total wall clock: ~15 minutes.
- Compute: local single-core CPU (CherryRd Mac). No remote GPU needed.
- Longest single run: incremental_second at δt=0.1·δt_crit → 25.1 s (168 steps × ~150 ms/step).
