# Artifact Harvest — Hussain 2023

| Artifact | Source | URL | Size | SHA-256 |
|---|---|---|---|---|
| Paper PDF | Sciendo / IJMCE | https://reference-global.com/download/article/10.2478/ijmce-2024-0004.pdf | 6 246 032 B | `4ccf458f1ddc087080777339ef54df2e15125e341443fb6025b30354b7507ffa` |
| Paper text (pdftotext -layout) | derived | (local `work/paper.txt`) | 108 KB | (derived) |

**Retrieval note**: DOI 10.2478/ijmce-2024-0004 resolves to `https://reference-global.com/article/10.2478/ijmce-2024-0004` (Sciendo's new "reference-global" front end). PDF link comes from `<meta name="citation_pdf_url">`. Fetch was done from uicgpu (proxy-enabled) with a Mozilla UA + explicit Referer. HTTP 200, `application/pdf`, ~6 MB.

**Code artifacts** (all in `work/`):

- `verify_bbmpb.py` — first attempt at direct substitution of paper's eq (32) into BBMPB reduced ODE. Result: h^k coefficients not identically zero → paper's eq (32) inconsistent.
- `verify_bbmpb_v3.py` / `verify_bbmpb_v4.py` — cascade solve for the correct b₁, b₂, ω₁, ω₂ order-by-order. Result: correct `b₂ = -12(μ+β)ω₃²ln²φ/θ` (nonzero when μ+β ≠ 0), paper's `b₂ = 0` is wrong branch.
- `verify_fig1_numerical.py` / `verify_fig1_v2.py` — numeric finite-difference check of paper's Fig 1 solution against original OBBMB PDE. Residuals ~ 0.1–2.
- `verify_symbolic_v1_obbmb.py` — symbolic proof that paper's △ = ω₂² − ω₁ω₃ is strictly positive under eq (48) constraints (numerator = quadratic in θb₀ with negative discriminant), so Case 1 (△<0) is unreachable.
- `verify_std_disc.py` — same proof for the standard Δ = ω₂² − 4ω₁ω₃: Δ = γ²/(α²ln²φ), still positive.
- `verify_correct_neda_obbmb.py` — full correct NEDA cascade for OBBMB. Symbolic PDE residual at Fig 1 params = 1e-18 (i.e. machine-epsilon zero).
- `final_cascade_obbmb.py` — clean cascade output.
- `careful_fig1_check.py` — decisive symbolic side-by-side: paper's ansatz gives nonzero PDE residual, correct cascade gives exact 0.

**LLM-judge cross-check** (free Argo endpoints, per hard rules):

- `llm_judge_prompt.txt` — the mathematical prompt.
- `llm_judge_response.json` — Argo GPT-5.2 verdict.
- `llm_judge2_response.json` — Argo Claude Opus 4.7 verdict.

Both judges independently confirmed all three findings without qualification.
