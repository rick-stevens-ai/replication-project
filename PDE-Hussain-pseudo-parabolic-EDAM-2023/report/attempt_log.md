# Attempt Log — Hussain pseudo-parabolic EDAM 2023

## 2026-07-04T15:09:33Z — start
- Assigned paper: Hussain et al. 2023, 'New closed form solutions of some nonlinear pseudo-parabolic models via a new extended direct algebraic method'
- DOI: 10.2478/ijmce-2024-0004 (IJMCE — International Journal of Mathematics and Computer in Engineering, Sciendo)
- Note: DOI prefix 10.2478 = Sciendo/De Gruyter; journal is open access.

## 2026-07-04T15:12Z — fetch PDF
- On uicgpu (proxy), DOI resolves via Sciendo’s `reference-global.com` front-end (Next.js SSR).
- `citation_pdf_url` meta → `https://reference-global.com/download/article/10.2478/ijmce-2024-0004.pdf`
- HTTP 200, 6 246 032 B, application/pdf. Copied to CherryRd `work/paper.pdf`. SHA-256 `4ccf458f…a507ffa`.
- `pdftotext -layout paper.pdf paper.txt` — 2422 lines, clean.

## 2026-07-04T15:20Z — pdf tool disabled (paid Anthropic route)
- `pdf` tool tried anthropic/claude-opus-4-8 (paid, credit exhausted) and google/gemini-3-flash-preview (unknown model). Fallback to pdftotext + manual reading was fine.

## 2026-07-04T15:30Z — characterize paper
- 4 PDEs: BBMPB (eq 3), OBBMB (eq 5), 1D Oskolkov (eq 6), generalized HERW (eq 8).
- Method: NEDA — traveling-wave reduction + finite polynomial ansatz in h(ξ), h(ξ) satisfies Riccati auxiliary.
- Fig 1 plots OBBMB v1 (Case 1, eq 49) with α=γ=1, θ=-1, μ=3, b0=1, φ=e, ω3=1.
- Fig 2 plots OBBMB v6 (eq 66). Fig 3 plots OBBMB |v8| (eq 50). Fig 4 plots HERW v36 (eq 75).

## 2026-07-04T15:40Z — first symbolic check (v1 BBMPB)
- Direct substitution of paper eq (32) into BBMPB reduced ODE (29). Result: h^k coefficients not identically zero for any k in {0,1,2,3}.
- Suspicion: eq (32) as written must have a typo (`a = -b`) that I’m misinterpreting.

## 2026-07-04T15:50Z — attempt full solve of coefficient system
- `sp.solve(equations, [b1, b2, ω1, ω2, alpha])` — hangs at >2 minutes on both v2 and v3 scripts. Killed.

## 2026-07-04T16:00Z — manual cascade solve
- `work/verify_bbmpb_v3.py`, then `v4.py`, then clean `final_cascade_obbmb.py`.
- OBBMB result:
  - Step 1 (h^4=0): `b2 = -12μω3² ln²φ/θ` (nontrivial branch, NOT 0)
  - Step 2 (h^3=0): `b1 = 12ω3(α – 5μω2·lnφ)lnφ/(5θ)`
  - Step 3 (h^2=0): ω1 quadratic-in-ω2 expression
  - Step 4 (h^1=0): quadratic in ω2 with 2 roots
  - Step 5 (h^0=0): parameter consistency `(6α² - 25γμ + 25μ²)(6α² + 25γμ - 25μ²) / (1250μ²θ) = 0` — sometimes vacuous once ω2 substituted.
- KEY finding: paper’s "b2 = 0" branch is the TRIVIAL root of the h^4 equation.

## 2026-07-04T16:15Z — Fig 1 direct verification
- `careful_fig1_check.py`: at Fig 1 params, paper's ansatz → v = 1 + tanh((3t-x)/2). Plugged into OBBMB PDE symbolically. Residual = `(9/4)tanh^4 - tanh^3 - (9/2)tanh^2 + tanh + 9/4` — NOT identically zero. FAIL.
- My correct cascade at same params → b2=36, b1=≂21, ω1≈0.07, ω2≈-0.52. Plugged in → residual identically 0. PASS.
- Independent confirmation: the paper's plotted Fig 1 solution is not a valid PDE solution.

## 2026-07-04T16:25Z — discriminant reachability analysis
- `verify_symbolic_v1_obbmb.py` + `verify_std_disc.py`: symbolic proof that `△_paper = ω2² - ω1ω3 = [3(θb0)²+6θb0γ+4γ²]/(4α²ln²φ)` has strictly positive numerator (its own discriminant in θb0 is `-12γ² < 0`).
- Standard Δ = ω2² - 4ω1ω3 = `γ²/(α²ln²φ)`, also strictly positive.
- Under both conventions, OBBMB Case 1 (△<0 or Δ<0) is UNREACHABLE for any real parameter choice — vacuous case. Fig 1 cannot cite eq (49) legitimately.

## 2026-07-04T16:35Z — LLM-judge cross-check (Argo, free)
- `argo:gpt-5.2` → corroborates all three findings verbatim, no qualification.
- `argo:claude-opus-4.7` → corroborates all three findings, computes same 9/4 constant term, states "You are not missing an interpretation."
- Two-independent-judge triangulation passes.

## 2026-07-04T16:45Z — finalize report
- REPORT.md, brief.md, attempt_log.md, artifact_harvest.md written.
- Evidence stored in report/evidence/: llm_judge_gpt5.json, llm_judge_opus47.json, careful_fig1_check.log, final_cascade.log.
- Verdict: CONTRADICTED (WAVE_RESULT NOT_REPL per canonical wave brief vocabulary).
