# Marker Extraction (proxy)

**Note (Ollie, 2026-07-05):** Full Marker/Nougat was not run on this paper as no pre-parsed copy exists in the central corpus and the paper is a clean, digital PDF (not scanned). The `pdftotext -layout` extraction preserves all text, equations (in LaTeX-ish form), tables, and figure captions with high fidelity. Marker would provide slightly cleaner Markdown formatting of tables but no new information.

## Extracted text

See `pdftotext.txt` for full linear extraction. Section landmarks:

- I. INTRODUCTION (lines 40-90)
  - A. Consequences of negative weights: `f(P+) = 1/(2P+ - 1)²` (Eq. 1)
  - B. Origin of negative weights (Sherpa NLO subtraction, dipole subtraction, ME+PS matching)

- II. REWEIGHTING METHOD DERIVATION (lines 174-280)
  - Eq. 2: PDF(x) = a·PDF+(x) - b·PDF-(x), with a≥b≥0, a-b=1
  - Eq. 3: P+(x) = a·PDF+/(a·PDF+ + b·PDF-)
  - Eq. 5: g(x) = 2·P+(x) - 1
  - Eq. 6: PDF_reweight(x) = g(x)·(a·PDF+ + b·PDF-)
  - II.A Application strategy (Eqs. 7, 8: cross-section reweighting)

- III. REWEIGHTING WHEN g(x) IS KNOWN EXACTLY (lines 293-395)
  - Eqs. 9-12: variance derivation → Var[σ_rw] = Σ w² g² ≤ Σ w² = Var[σ]
  - III.A DOUBLE SLIT INTERFERENCE MC (Eqs. 13-21)
    - α = 1, δ = 0.25
    - Eq. 15: <p|Ψ> = (1/√(2πδ)) ∫[α-δ,α+δ] cos(px) dx
    - Eq. 16: <p|Ψ> = (1/(p√(2πδ)))·[sin(p(α+δ)) - sin(p(α-δ))]
    - Eq. 17: P(p) = |<p|Ψ>|² = (1/(2πp²δ))·[sin(p(α+δ)) - sin(p(α-δ))]²
    - Eq. 18 P_base(p) = (1/(2πp²δ))·[sin²(p(α+δ)) + sin²(p(α-δ))]
    - Eq. 19 P_interference(p) = -(1/(πp²δ))·sin(p(α+δ))·sin(p(α-δ))
    - Table I sampling: base [-10,10]×[0,1.5], 100000; pos-interf [-10,10]×[0,0.075], 5000; neg-interf [-10,10]×[0,1.5], 100000
    - Eq. 20 P+(p) = min([sin² + sin²]/[sin+sin]², 1)
    - Eq. 21 g(p) = min(2·[sin²+sin²]/[sin+sin]² - 1, 1)

- IV. UNCERTAINTY QUANTIFICATION (lines 400-620)
  - IV.A Model choice — DNN ensemble (20 nets), rebalance formula Eq. 26
  - IV.B Properties of uncertainty
  - IV.C Event-by-event uncertainty (Eqs. 27-36)
    - Eq. 34: Var[σ_rw] = Σ w²(g² + 2δg²) — no off-diagonal
    - Eq. 36: relative uncertainty (fully-correlated worst case) = (δg/g)·√(1 + 1/N + 1/(g²·N))
    - Eq. 38: reweighted-better-than-original threshold N < (1 - g² - δg²)/δg²  (Example: g=0.7, δg=0.07 → N<103)
  - IV.D Final-observable-level uncertainty (PCA of ensemble histograms)

- V. HEP EXAMPLE (lines 635+)
  - V.A Sherpa V+jets samples (ATLAS OpenData), Powheg VH signal
  - V.B DNN inputs (Table IV, ~50 variables)
  - V.C-V.E Closure, signal region, PCA systematics, Asimov significance table (Table VII): nominal 2.56 → reweighted+PCA 3.84 (≈50% gain)

## Data Availability
Refs [16] and [18]: ATLAS DAOD_PHYSLITE MC electroweak/higgs samples on CERN Open Data Portal.

