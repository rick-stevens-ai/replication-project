# Workflow — Pendse & Bhattacharyay 2016 replication

## Inputs
- `paper.pdf` (arXiv:1602.05303)
- `extraction/marker.md` (full-text extraction)
- `report/method_extract.md` (pre-extracted method summary)

## Steps executed
1. **Read method + key equations** from `method_extract.md` and `marker.md` (Eqs. 2–12), identifying:
   - Eq.3 = dimensionless local-GP vortex ODE (thick vortex).
   - Local-GP energy quartic in β̃ + existence condition D⁴ ≥ 32 ξ₀⁴.
   - Non-local GP (Eq.5, g₂∇²|ψ|² term) → near-origin β = 1/(2√g₂) ~ 1/a (Eq.8).
   - Generalized Taylor-kernel selection β = 1/(a[(2|s|)!!]^{1/2|s|}) (Eq.9–10).
   - Piecewise thin-vortex variational profile + α,λ,δ closed forms (Eq.11).
   - Leading-order energy comparison E_ξ₀ ~ ln(|s|D/ξ₀) vs E_a ~ ln(D/(α a)).
2. **Wrote** `code/pendse2016_replication.py` (single file, numpy/scipy):
   - `solve_thick_vortex` — `scipy.integrate.solve_bvp` on Eq.3.
   - `thick_beta_selection` — quartic roots + discriminant.
   - `thin_beta_generalized`, `thin_alpha`, `thin_lambda_delta`, `thin_profile` — non-local thin branch.
   - `E_thick`, `E_thin` — energy comparison.
   - `add_claim` — logs paper_value/reproduced_value/match/note per claim.
3. **Ran** it. Fixed one numpy-bool JSON serialization bug. Final: 12/12 claims PASS.
4. **Saved** `work/results.json` (claims + meta) and 4 figures to `figs/`.
5. **Wrote 8 artifacts** (report/REPORT.tex + compiled REPORT.pdf via pdflatex ×2, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md; updated META.json).

## Reproduce
```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/TEXTURE-polar-pendse2016
python3 code/pendse2016_replication.py         # writes work/results.json + figs/
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

## Environment
- CPU-only, Python 3.14, numpy + scipy + matplotlib (Agg). No paid APIs, no cluster.
- Runtime: ~3 s for the full solve+figures (well under the 500 s target).
