# Artifacts summary — dar2026 (TEXTURE-orbital-dar2026)

Paper: Dar, Scheurer, Schrade, "Altermagnetic spin textures coupled to
superconductors: Domain wall spin-triplet superconductivity and
supercurrent-induced torques", arXiv:2607.15249v1.

**VERDICT: PARTIAL** — Coverage ~5/10, Agreement ~6/10.

## 8-artifact inventory

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-orbital-dar2026.pdf` | present |
| 2 | Marker text extraction | `extraction/marker.md` | INTERIM (pdftotext -layout; marker absent) |
| 3 | Nougat math extraction | `extraction/nougat.mmd` | INTERIM (hand-transcribed eqs + pdftotext dump; nougat absent) |
| 4 | Report | `report/REPORT.tex` | present (ships as .tex source; pdflatex absent) |
| 5 | Open questions | `report/open_questions.json` | present (5 Q + next_steps; JSON-valid) |
| 6 | Workflow | `report/workflow.md` | present |
| 7 | Artifacts summary | `report/artifacts_summary.md` | present (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | present |
|   | Evidence | `report/evidence/` | result JSON + solver + recipe |
|   | Work (gitignored) | `work/` | `dar2026_bdg.py`, `dar2026_result.json` |

## Headline numbers traced to evidence JSON keys
All from `report/evidence/dar2026_result.json` (live re-run confirmed, ~125 s):

| Quantity | Value | JSON key |
|----------|-------|----------|
| Hermiticity residual | 0.0 | `hermiticity_residual` |
| Min \|E_BdG\| (gap) | 5.10e-4 eV | `min_abs_bdg_eigenvalue` |
| Singlet max (AM) | 2.437e-3 | `singlet_max_AM` |
| Triplet/singlet ratio (AM) | 0.0038 | `triplet_max_over_singlet_max_AM` |
| Triplet I_t max AM / AFM | 8.52e-11 / 8.42e-11 | `triplet_It_max_AM` / `_AFM` |
| Triplet localization frac AM / AFM | 0.992 / 0.993 | `triplet_localization_frac_AM` / `_AFM` |
| On-wall angular modulation AM / AFM | 0.119 / 0.122 | `angular_modulation_AM` / `_AFM` |
| Fourfold (l=4) FFT power AM / AFM | 2.88e-11 / 3.00e-11 | `fft_angular_power_AM["4"]` / `_AFM["4"]` |
| Spin-resolved up / dn angular profiles | see arrays | `angular_It_up_AM` / `angular_It_dn_AM` |

## Claim-by-claim
- **Triplet localized at wall** (claim 1): **MATCH** (loc frac 0.99).
- **Spin-resolved anisotropy** (claim 3): **MATCH** (up peaks chi~+/-pi/2, dn peaks chi~0,pi).
- **Fourfold modulation unique to AM, vanishes in AFM** (claim 2, the discriminator): **FAIL**
  (AM 0.119 ≈ AFM 0.122; l=4 power nearly identical).
- **Supercurrent quadrupolar torque** (Sec. VII): **NOT ATTEMPTED** (scoped out).

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-orbital-dar2026/work
/home/stevens/comfyui-env/bin/python dar2026_bdg.py   # ~125 s -> dar2026_result.json
```
Interpreter: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0).

## Notes on degraded artifacts (NOT physics gaps)
- `marker`/`nougat` binaries not installed → artifacts 2,3 are honest `pdftotext`
  interims with NOTE headers and the exact regenerate commands. Authoritative
  equations are hand-transcribed in `nougat.mmd` and `REPORT.tex`.
- `pdflatex` not installed → REPORT.tex delivered as source; compiles off-host.
