# Workflow — Replication of arXiv:0805.3922

## 1. Ingest
- `pdftotext -layout paper.pdf paper.txt` (648 lines, clean text layer).
- Read intro, Sec. II (formalism, Eqs. 1-8), Sec. III (results, Figs. 1-4),
  Sec. IV (summary). Identified the paper is *magnetic-field-induced
  incommensurate resonance in cuprates* — NOT "multipolar texture" (task-label
  mismatch, flagged in `extraction/marker.md`).

## 2. Claim selection
Picked 5 machine-checkable claims (see marker.md): (1) Zeeman branch splitting
±2ε_B; (2/3) field-driven commensurate→IC resonance + critical field;
(4) energy-selectivity/hourglass-breakdown scale; (5) ε_B↔B (g-factor)
internal consistency.

## 3. Scope decision
Full self-consistent Σ^(s) (Eq. 6 double momentum sum + gap Eqs. 7a,7b) is a
heavy iterative program → OUT OF SCOPE for a minimal analytic replication.
Chose to test the falsifiable *mechanism* in Eqs. (4), (8), (9) with a
physically-motivated single-band MF spin excitation ω_k and a k-peaked
schematic self-energy.

## 4. Implementation (`code/`)
- `model.py`: square-lattice structure factors γ_k, γ'_k; gapped MF spin mode
  ω_k (gap DELTA0 at Q, disperses upward); schematic Re/Im Σ peaked at Q;
  S(k,ω) via Eq. 8 with the (ω−2ε_B) Zeeman shift; cut-scan and peak-finder;
  incommensurability extractor.
- `run_checks.py`: runs all 5 claim checks, writes `work/results.json` and
  three PNGs; includes an analytic Eq.9 isolation (`claim2b_eq9_analytic`) that
  cleanly captures the commensurate→IC splitting the full-S scan cannot.

## 5. Execution (`work/`)
- `python3 code/run_checks.py` → `work/results.json`, `fig_cut.png`,
  `fig_delta_vs_field.png`, `fig_omega_spin.png`. All numbers computed at run
  time; no answers hard-coded.

## 6. Compare & report
- Quantitative comparison table in `report/REPORT.tex` /
  `report/artifacts_summary.md`.
- Honest negative result documented: the raw denominator-form S(k,ω) scan is
  dispersion-dominated and does NOT reproduce the field-driven transition; the
  analytic Eq.9 isolation does (critical field ~6.2 T, bracketed by the paper's
  4-10 T). See `failure_analysis.md`.

## Reproduce
```bash
cd TEXTURE-multipolar-zhang2008
pdftotext -layout paper.pdf paper.txt      # optional, already done
python3 code/run_checks.py                 # writes work/results.json + PNGs
pdflatex -output-directory report report/REPORT.tex   # optional, needs latex
```
Dependencies: python3, numpy, scipy (2.4.3 / 1.18.0 used), matplotlib (optional
for plots), pdftotext (poppler), pdflatex (optional).
