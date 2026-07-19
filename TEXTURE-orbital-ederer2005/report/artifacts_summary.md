# Artifacts Summary — TEXTURE-orbital-ederer2005

## Verdict: REPLICATED (model-level) — Coverage 8/10, Agreement 8/10

Review article (arXiv:cond-mat/0512330). Five machine-checkable claims extracted and
reproduced with real, tractable code (no DFT faked; DFT-absolute magnitudes flagged
out of scope).

## Claims & results (all from executed code)

| # | Claim (review) | Model | Result | Verdict |
|---|----------------|-------|--------|---------|
| C1 | BiFeO3 polarization quantum = 185.6 uC/cm^2 (Fig.1) | geometric eR/V | **178.3 uC/cm^2, 3.9% err** (residual = LSDA volume, sign consistent) | reproduced <4% |
| C2 | P is Berry phase mod e*R/V; only ΔP physical (Sec.2) | Rice-Mele KSV Berry phase | quantized to 0 & −e/2 exactly; odd switching path resid 2.8e-16 | reproduced exact |
| C3 | d0 rule: FE needs empty d, magnetism needs partial d | 2-level vibronic (pseudo-JT) | double well ONLY d0 (0.294 eV); d1/d2 flat | reproduced decisive |
| C4 | YMnO3 improper FE: K3 drives Γ2⁻; ~80/15 split (Sec.3.1) | Landau F(Q,P), λQ²P | K3 alone condenses; P∝Q0² induced; 80:15 at λ=0.181 | reproduced mechanism |
| C5 | DM canting → M~0.1 μB/cell; reverses with rotation mode | J+DM two-sublattice spins | 0.1 μB at D/J=0.02, 0.57° canting; M flips sign | reproduced quant. |

## Files
- `code/claim1_polarization_quantum.py` … `claim5_bifeo3_canting.py` — one per claim
- `work/claim1_out.txt` … `claim5_out.txt` — captured runs
- `work/results_summary.json` — machine-readable aggregate
- `report/REPORT.tex` — section-by-section report (reproduced / failed / out of scope)
- `report/open_questions.json` — 5 new questions
- `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`

## Out of scope (flagged, not faked)
Absolute DFT polarization (~95 μC/cm^2 BiFeO3), DFPT phonon spectra (YMnO3/CdCr2S4),
Bi2FeCrO6 predictions (P~80, M=2μB, Tc<100K), all experimental values.
