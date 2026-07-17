# Artifacts Summary — jia2026 NOME reproduction

**Paper:** Geometry-Driven Nonlinear Orbital Magnetoelectric Effect (Jia, Qiao, Wang, arXiv:2605.17462)
**Verdict:** PARTIAL

## Inventory

### Extraction
- `extraction/marker.md` — marker/pdftotext extraction of the paper (equations legible).
- `extraction/nougat.mmd` — Nougat fallback stub.
- `paper.pdf` — source PDF.

### Method
- `report/method_extract.md` — claims C1–C6, both model Hamiltonians, parameters, recipe.

### Code + data
- `work/reproduce.py` — from-scratch numpy Kane–Mele (Eq. 11) implementation + response evaluation + sweeps.
- `work/results.json` — per-claim paper vs reproduced values, match flags, numeric dumps.
- `work/COMPUTE_NOTES.md` — detailed compute-phase notes (what built, what matched, caveats).

### Figures
- `work/figs/fig1a_bands.png` — 4-band structure along K′–Γ–M–K–Γ (Fig 1a analogue).
- `work/figs/fig1b_chi_vs_mu.png` — chi^{(0,od)}_{z;xx} vs μ (orbital & spin).
- `work/figs/fig1c_chi_vs_lamR.png` — chi vs λ_R at μ=50 meV (even-symmetry demo).

### Report set
- `report/REPORT.tex` (+ `REPORT.pdf` if compiled) — full write-up.
- `report/open_questions.json` — 5 new heavy open questions.
- `report/workflow.md` — workflow, tools, effort.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest gap analysis.

## Key reproduced numbers (trace)

Model: modified Kane–Mele honeycomb (Eq. 11); params t=0.85 eV, λ_R=20 meV,
λ=10 meV, λ_so=10 meV, T=20 K; 120×120 BZ mesh.

| Quantity | Reproduced value | Match |
|---|---|---|
| Number of bands | 4 | ✔ |
| Energy range | −2560 … +2560 meV (≈6t bandwidth) | ✔ |
| Central gap (band 2↔3) | 18.04154837722515 meV | ✔ |
| λ_R-even symmetry rel. err | 9.082279743054616e-16 | ✔ (machine precision) |
| χ^{(0,od)}_{z;xx} at λ_R=0 (raw) | 13.943143440336225 (nonzero minimum) | ✔ (structure) |
| Even check λ_R=0.01 (+/−) | +2.193426222912495 / +2.1934262229124903 | ✔ |
| Even check λ_R=0.02 (+/−) | −5.2896687883299345 / −5.289668788329926 | ✔ |
| Even check λ_R=0.03 (+/−) | −0.2066981391265077 / −0.20669813912650806 | ✔ |
| Orbital/spin ratio (median, cond. edge) | 11.611273790339222 | partial (not 3x) |
| Orbital/spin ratio (peak) | −115.64244686229591 | ✗ (not 3×) |
| Orbital vs spin sign near gap | opposite | ✔ (qualitative) |
| Absolute μB/V² prefactor | not pinned (raw units) | — |

**Summary:** fully matched = band structure + λ_R-evenness (P-even, machine
precision). Partial = orbital/spin (sign yes, 3× no). Not verified = only-xx
symmetry enumeration, absolute μB/V² scale (C6). Not attempted = CuMnAs Model 2
(C5), MPG enumeration (C3), full geometric/Hermitian-connection sector (Eqs. 4–9).
