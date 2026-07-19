# Artifacts Summary --- Cullen 2025 (arXiv:2509.20436v3)

**Verdict: PARTIAL** (Coverage 5/10, Agreement 5/10).
Conventional interband Kubo OHE for Ge = **~49 (hbar/e) Ohm^-1 cm^-1** (converged);
paper total headline = **~10^3** (dominated by unbuilt quantum corrections).

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-orbital-cullen2025.pdf` | present |
| 2 | Marker text extraction (PROSE) | `extraction/marker.md` | INTERIM (pdftotext -layout + header) |
| 3 | Nougat math extraction (MATH) | `extraction/nougat.mmd` | INTERIM (pdftotext + hand-transcribed Eqs 1,2,3,6,7,conv) |
| 4 | Section-by-section report | `report/REPORT.tex` | complete (ships as source) |
| 5 | 5 open questions + next_steps | `report/open_questions.json` | complete (valid JSON) |
| 6 | Workflow / tools / effort | `report/workflow.md` | complete |
| 7 | This inventory | `report/artifacts_summary.md` | complete |
| 8 | Failure / gap analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/cullen2025_result.json`, `report/evidence/ohe_spherical.py` | copied |
| + | Work | `work/ohe_spherical.py`, `work/cullen2025_result.json` | present |

## Headline numbers traced to evidence
All numbers below trace to `report/evidence/cullen2025_result.json`:
- `runs.coarse_N21_EF10.sigma_OHE_hbar_e_Ohm_cm` = 48.30
- `runs.N31_EF10.sigma_OHE_hbar_e_Ohm_cm` = 49.92 (live re-verified 2026-07-19 -> 49.9217)
- `runs.N41_EF10.sigma_OHE_hbar_e_Ohm_cm` = 49.41  <-- converged conventional value
- `runs.N41_EF5.sigma_OHE_hbar_e_Ohm_cm` = 33.77  (EF-dependence)
- `runs._verdict.kF_heavy_hole_perm` = 2.762e8, `kmax_perm` = 4.0e8, `grid_covers_FS` = true
- `paper_headline_hbar_e_Ohm_cm` = 1000.0

## Physics one-liner
4x4 spherical Luttinger model of Ge (g1=13.38, gbar=4.97); conventional interband Kubo /
Berry-curvature orbital Hall conductivity with j^{Lz}_x = 1/2{Lz,vx}; got ~49 vs paper's
~10^3 total, consistent because the paper (Fig. 2) says quantum corrections Delta sigma_1,2
dominate the total and the conventional piece is sub-dominant.

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-orbital-cullen2025/
/home/stevens/comfyui-env/bin/python work/ohe_spherical.py
# -> work/cullen2025_result.json : N21/31/41 convergence + _verdict block
```

## Notes on interim artifacts
`marker` and `nougat` binaries are NOT installed on this host (`which marker nougat` -> not
found). Artifacts 2 & 3 are the documented pdftotext interim (poppler), each with an in-file
provenance header + the exact regenerate command. Fidelity loss is confined to math-token
rendering; the authoritative equations are hand-transcribed into `extraction/nougat.mmd`
(the math artifact) and `report/REPORT.tex`. This is an extraction-TOOLING gap, not a physics gap.
