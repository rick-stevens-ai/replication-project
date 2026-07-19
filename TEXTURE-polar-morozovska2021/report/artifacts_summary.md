# Artifacts Summary --- morozovska2021 (arXiv:2104.00598)

**Paper:** Morozovska, Hertel, Cherifi-Hertel, Reshetnyak, Eliseev, Evans,
"Chiral Polarization Textures Induced by the Flexoelectric Effect in Ferroelectric
Nanocylinders" (2021), arXiv:2104.00598.

**Verdict:** `replicated` (mechanism-level) --- Coverage 7/10, Agreement 10/10.

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-morozovska2021.pdf` | present |
| 2 | Marker text extraction | `extraction/marker.md` | **interim** (pdftotext -layout + NOTE header; marker not installed) |
| 3 | Nougat math extraction | `extraction/nougat.mmd` | **interim** (pdftotext + hand-transcribed LaTeX Eqs 1a-1g; nougat not installed) |
| 4 | Detailed report | `report/REPORT.tex` | complete (ships as source; no pdflatex on host) |
| 5 | Open questions + next steps | `report/open_questions.json` | complete (5 heavy Qs + 5 next_steps) |
| 6 | Workflow / tools / effort | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure / gap analysis | `report/failure_analysis.md` | complete |
|   | Evidence | `report/evidence/morozovska2021_result.json`, `report/evidence/flexon_1d.py` | complete |
|   | Work (gitignored) | `work/flexon_1d.py`, `work/morozovska2021_result.json` | present |

## Headline numbers (traced to evidence JSON keys)
| Quantity | Value | Evidence JSON key |
|----------|-------|-------------------|
| Reference transverse peak `P_e(F=0.3)` | **-0.34797** | `P_e_reference_F0.3` |
| `P_e(F=0)` (pure Ising, ~0) | 1.90e-12 | `checks.P_e_zero_at_F0` |
| Odd-in-F antisymmetry residual | 4.52e-05 | `checks.P_e_odd_in_F_residual` |
| Chirality flips with sign(F) | True | `checks.chirality_flips_with_sign_F` |
| Monotone growth for F>0 | True | `checks.monotone_growth_posF` |
| Saturates at large |F| | True | `checks.saturates_at_large_F` |
| Linear-response slope dP_e/dF at 0 | -1.2185 | `checks.linear_slope_near_0` |
| Coverage / Agreement | 7 / 10 | `verdict.Coverage_/10`, `verdict.Agreement_/10` |

## Extraction-tooling note (not a physics gap)
`marker` and `nougat` binaries are not installed on this packaging host; only
poppler `pdftotext` is available. Artifacts 2 and 3 are honest pdftotext interims
with explicit in-file NOTE headers stating the regen commands. Equation fidelity
is degraded by pdftotext (Unicode math mangled) --- the authoritative equations
are hand-transcribed into LaTeX inside `extraction/nougat.mmd` (the math artifact)
and `report/REPORT.tex`. This is an environment limitation, not a replication gap.

## Reproduce block
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-polar-morozovska2021/work/flexon_1d.py
# -> work/morozovska2021_result.json ; prints F-scan + all checks.
# Interpreter: /home/stevens/comfyui-env/bin/python (numpy 2.3.5)
```
Live re-run 2026-07-19 reproduced the saved JSON to all quoted digits.
