# Workflow — arXiv:1404.5920 replication

## 1. Acquire + read
- Target dir did not pre-exist; created `TEXTURE-multipolar-chandra2014/` and fetched
  `paper.pdf` from `https://arxiv.org/pdf/1404.5920` (2.3 MB, PDF v1.5).
- `pdf` vision tool unavailable (Anthropic credit exhausted + Google/OpenAI PDF plugins off).
  Fell back to `pdftotext -layout` → 719-line text dump, read in full.
- Identified the paper as a **theory/review of hastatic order** in URu2Si2, contrasting the
  spinorial order parameter against **multipolar-texture** density-wave scenarios.

## 2. Extraction
- Wrote `extraction/marker.md`: title/authors/venue, central claims, all key equations
  (Eqs. 1–31 transcribed), quantitative anchors, and the 5 chosen machine-checkable claims.

## 3. Claim selection (5 tractable, machine-checkable)
- C1 Onsager spin-zero ladder (Eqs. 7, 9)
- C2 splitting bound Δ < ½ħω_c = 0.67 K (Eqs. 11–12)
- C3 dHvA spin zeros from destructive interference (Eqs. 4–7)
- C4 Landau spin-flop + √(Pc−P) soft-mode gap (Eqs. 17–19)
- C5 Ising nonlinear susceptibility χ3 ∝ cos⁴θ

## 4. Implementation
- `code/chandra2014_replication.py` (numpy/scipy/matplotlib). Pure analytic/semi-analytic:
  - C2 from SI constants (e, ħ, m_e, k_B): ω_c = eB/m*, Δ = ½ħω_c/k_B.
  - C1/C3 from α(θ) = g*cosθ · m*/2m_e; half-integer crossings + envelope |cos δ|, δ=πα.
  - C4 minimizes f[Ψ] over spinor orientation; fits log-log slope of the soft-mode gap.
  - C5 expands m=μ tanh(μ B_z/kT) to B³, projects onto field, extracts cos⁴θ shape.
- No paper numbers are hard-coded into the *results* except the physical anchors
  (m*=13 m_e, B=13 T, g*=2.6); everything else is computed.

## 5. Execution
- Ran under `work/`. One JSON-serialization fix (numpy bool) — added `NpEnc` encoder.
- Output: `work/results.json` + `figs/{spin_zeros,landau_softmode_gap,chi3_cos4}.png`.
- Result: **5/5 machine-checkable claims PASS.**

## 6. Reporting
- 8-artifact bar in `report/`: REPORT.tex (+PDF if latex present), open_questions.json (5),
  workflow.md, artifacts_summary.md, failure_analysis.md; plus META.json at root.

## Reproduce
```bash
cd TEXTURE-multipolar-chandra2014/work
python3 ../code/chandra2014_replication.py
# -> work/results.json, figs/*.png
cd ../report && pdflatex REPORT.tex   # optional
```
