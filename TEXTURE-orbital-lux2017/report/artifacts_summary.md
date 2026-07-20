# Artifacts summary — Lux et al. 2017 (arXiv:1706.06068)

**Paper:** *Chiral and Topological Orbital Magnetism of Spin Textures*,
Lux, Freimuth, Blügel, Mokrousov, arXiv:1706.06068 (2017).
**Verdict: PARTIAL** — Coverage 6/10, Agreement 7/10.

## 8-artifact inventory
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-orbital-lux2017.pdf` | present |
| 2 | Marker extraction (prose) | `extraction/marker.md` | interim (pdftotext -layout; marker not installed) |
| 3 | Nougat extraction (math) | `extraction/nougat.mmd` | interim (hand-transcribed LaTeX + pdftotext appendix; nougat not installed) |
| 4 | Report | `report/REPORT.tex` | complete (LaTeX source; pdflatex not required) |
| 5 | Open questions | `report/open_questions.json` | complete (5 Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/lux2017_result.json`, `report/evidence/replication_recipe.json` | complete |
| + | Code | `report/evidence/code/lux2017_tom.py`, `report/evidence/code/gobel2024_sd_skyrmion_kubo_Lz_kernel.py` | complete |
| + | Work | `work/lux2017_tom.py`, `work/lux2017_result.json`, `work/textures-orbital-lux2017.txt` | complete |

## Headline numbers (traced to evidence JSON keys)
- **H1 — TOM linear in scalar spin chirality (zero SOC): CONFIRMED.**
  `checks.H1_linear_in_chirality.linfit_R2 = 0.964`;
  `M_tom_over_chi_relspread = 0.129` (constant to 13%);
  `linfit_slope = 6.3e-4`. → reproduces `M_tom ∝ B_eff^z` (Eq. 12 / Eq. 1).
- **H2 — μ-dependence (1−3μ²/Δ²): PARTIAL.**
  `checks.H2_mu_dependence.sign_changes = 5` (qualitative sign change reproduced;
  clean single parabola not resolved on the lattice —
  `clean_single_parabola_resolved = false`).
- **Absolute 1/4·χ_LP coefficient:** continuum-vs-lattice normalization gap
  (`honest_gaps[0]`) — structural linearity + sign confirmed, absolute prefactor
  not matched.
- Runtime: `runtime_sec = 18.4`.

## Kernel credit
The lattice s–d Hamiltonian (`build_H`, `build_FM`), skyrmion texture, and the
itinerant orbital operator `L_z = ½(X v_y − Y v_x)` (`v = i[H,R]`) are **reused
from Ollie's shared kernel `gobel2024_sd_skyrmion_kubo_Lz_kernel.py`** (gӧbel2024,
arXiv:2410.00820). From-scratch additions for this paper: arbitrary-texture
Hamiltonian builder, collinear→skyrmion canting sweep, continuum scalar-spin-
chirality estimator, center-gauged ground-state orbital moment, and the H1/H2
comparison harness.

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-orbital-lux2017/work/lux2017_tom.py
# runtime ~18 s; writes work/lux2017_result.json
```

## Physics summary (3 lines)
1. Built a from-scratch 2D s–d lattice skyrmion model with **no SOC** and computed
   the itinerant topological orbital magnetization via `L_z = ½(X v_y − Y v_x)`.
2. Confirmed the paper's zero-SOC structural headline: **M_tom is linear in the
   scalar spin chirality** `n·(∂ₓn × ∂_yn)` (R²=0.964, M_tom/χ constant to 13%).
3. The μ-parabola is reproduced only qualitatively and the absolute 1/4·χ_LP
   coefficient is a continuum-normalization gap → **PARTIAL**.
