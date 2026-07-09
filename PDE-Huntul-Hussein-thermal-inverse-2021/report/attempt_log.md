# Attempt log — chronological

**2026-07-04 22:08 CDT** — Task received (subagent). Target dir created:
`~/Dropbox/REPLICATE-PROJECT/PDE-Huntul-Hussein-thermal-inverse-2021/{report/evidence,work}`.
Read wave brief — free endpoints only, LLM-judge for verdict, real replication of PDE inverse solver.

**22:08–22:09** — Fetched paper PDF (open access, Iraqi Journal of Science). DOI resolved to
`https://ijs.uobaghdad.edu.iq/index.php/eijs/article/view/3085`; PDF download at
`.../article/download/3085/1510` (1.68 MB, 11 pages).

**22:09–22:11** — Text extraction: `pdftotext` extracts prose cleanly but mangles all math
(equations render as scattered symbols/whitespace because Adobe glyph mapping is unusual). Fell
back to page-by-page vision OCR via Argo `argo:gpt-4o` (free endpoint) with each page rendered
at 200 dpi by `pdftoppm`. Successfully transcribed:
- p.2: PDE (eq. 1), IC/BC/overdet (2–4), uniqueness condition W(t) (5)
- p.3: Crank–Nicolson coefficients, heat-flux formulas (10–11), Tikhonov objective (12)
- p.4: noise model (15–16), RMSE definitions (17–18), a(0)/f(0) derivation, Example 1 input
- p.5: Example 1 exact solutions, Table 1 (direct RMSE)
- p.8: Example 2 piecewise a(t) and f(t)

The paper's Example 2 g_0, g_1 piecewise functions and the exact u(x,t) were partially garbled
by OCR; I therefore constructed a self-consistent Example 2 test using u(x,t)=e^(x+t) with the
paper's piecewise a(t) ∈ {1,2,1,2} and f(t) ∈ {0,1,0,1} targets. This is disclosed in the report.

**22:11–22:14** — Wrote `work/solver.py` (Crank–Nicolson forward solver + Thomas TDMA + inverse
via `scipy.optimize.least_squares`). Wrote `work/example1.py`.

**22:14** — First run of Example 1: forward RMSE was ~0.6 (paper: ~0.002). Debugged: the c(x,t)
term had a sign error in both the LHS diagonal (B_new) and RHS diagonal (B_old) of the CN
scheme. Root cause: I had written `B = dt*a/dx^2 + dt*c/2` but the correct discretization has
`c` on the LHS with the same sign as `a` after moving to LHS, i.e. it should reduce
`(1 + B_new)` to `(1 + dt*a/dx^2 - dt*c/2)`. Fixed both signs.

**22:15** — Verification: forward RMSE now matches paper's Table 1 within 5–10 %:
- M=N=10:  rmse(μ_3) 3.45e-3 vs paper 3.7e-3;  rmse(μ_4) 0.0193 vs paper 0.0198
- M=N=20:  rmse(μ_3) 7.9e-4 vs paper 8.4e-4;   rmse(μ_4) 0.0049 vs paper 0.0050
- M=N=40:  rmse(μ_3) 1.9e-4 vs paper 2.0e-4;   rmse(μ_4) 0.00125 vs paper 0.00120

**22:16–22:17** — Full inverse run for Example 1 across the 7 noise/regularization cases in
paper's Table 2. All within factor of ~1–2× of paper.

**22:17–22:19** — Wrote `work/example2.py` and ran. Similar agreement, factor ~1–2×.

**22:19** — Generated 4 figures (2 per example: noiseless and noisy+regularized) via matplotlib.

**22:19–22:20** — LLM judge invocation via `argo:claude-opus-4.7` (free endpoint) with the full
comparison table; verdict: **PARTIAL**.

**22:20** — Report and artifact_harvest written; final result printed.
