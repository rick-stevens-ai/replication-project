# Artifacts Summary --- textures-polar-verga2014

Paper: **Verga, "Skyrmion collapse," arXiv:1409.0256v2 (2014)**
Verdict: **PARTIAL** --- Coverage 6/10, Agreement 8/10.

## 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-verga2014.pdf` | present (1.9 MB, valid) |
| 2 | Marker extraction | `extraction/marker.md` | **interim (pdftotext)** --- marker not installed |
| 3 | Nougat extraction | `extraction/nougat.mmd` | **interim (pdftotext + hand-transcribed eqns)** --- nougat not installed |
| 4 | Report | `report/REPORT.tex` | complete (section-by-section + critique + verdict) |
| 5 | Open questions | `report/open_questions.json` | complete (5 heavy Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | complete (tools/versions/effort/compute target) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete (honest gaps) |
| + | Evidence | `report/evidence/` | result JSON + replication code |
| + | Work | `work/` | code + result JSON (scratch) |

## Evidence traces (`report/evidence/`)

- **`verga2014_result.json`** --- machine-readable results:
  - `four_pi_J = 5.0265` (continuum benchmark)
  - `energy_vs_lambda`: E/(4piJ) = 0.9895 / 0.9966 / 0.9962 / 0.9872 / 0.9513 for
    lambda = 4 / 8 / 16 / 32 / 64 on L=512; Q = -0.9998 ... -0.9512
  - `Q_charge_minus = -0.980`, `Q_charge_plus = +0.980` (L=256, lambda=20)
  - `scale_inv_break`: E(lambda) profile, E_max/(4piJ)=0.988, no barrier -> collapse
  - `self_similar_exponents`: alpha_computed=1.0, beta_computed=0.5 (paper: 1, 1/2)
  - `verdict`: coverage 6, agreement 8
- **`verga2014_repl.py`** --- from-scratch numpy replication code (BP field,
  discrete exchange energy, Berg-Luscher charge, exponent-balance solve).

## Key numbers (this work vs paper)

| Quantity | Paper | This work |
|----------|-------|-----------|
| Exchange energy E_xc | 4piJ = 5.0265 | 5.009 (lambda=8), <0.5% |
| Topological charge Q | +/-1 | -/+0.980 (correct sign) |
| Self-similar alpha | 1 | 1.000 |
| Self-similar beta | 1/2 | 0.500 |

## Extraction-tool note
Marker and Nougat are not installed on this host. Per the replication skill,
`pdftotext` is the sanctioned interim fallback; the marker.md / nougat.mmd slots
are filled with pdftotext-derived content (nougat.mmd additionally carries the
key equations hand-transcribed to LaTeX/Mathpix-Markdown so downstream math checks
are self-contained). Re-run with real Marker + Nougat when available.

## Physics note
The paper uses **exchange + spin-transfer torque + polarization (b-)field, and NO
DMI**. Any "DMI" framing in the task brief is generic; we replicated the paper's
actual pure-exchange BP-skyrmion-under-STT model.
