# Artifacts summary — Kumar, Sun & Fradkin (2015)

**Paper:** Chiral spin liquids on the kagome lattice — Kumar, Sun & Fradkin,
PRB 92, 094433 (2015), arXiv:1507.01278.
**Method class:** model-Hamiltonian (kagome tight-binding realization of the
flux-attachment / Chern-Simons mean-field chiral flux state).
**Verdict:** REPLICATED (topological; explicit (2π,π/2,π/2) flux).

## Headline result
In the XY regime, the scalar-chirality term drives a **zero-field chiral spin
liquid**: finite chirality flux opens a gap, gives the lowest kagome band
**Chern number C = +1**, hence **σ_xy^s = C/2 = 1/2**. This is confirmed both in
a uniform-flux sweep AND in the paper's **explicit (2π, π/2, π/2) flux state**
on the doubled 6-site magnetic unit cell (all plaquette fluxes numerically
verified): half-filling gap = 1.464 t (open), gauge-robust non-Abelian
**occupied bottom-3 Chern = +1**, **σ_xy^s = 1/2** — matching the paper's
Eq. 4.20 (occupied Chern +1) exactly, with a spontaneous loop current.

## Artifact inventory (8)
| # | Artifact | Path |
|---|----------|------|
| 1 | Marker extraction | `extraction/marker.md` (+ `marker_body.txt`) |
| 2 | Nougat MMD | `extraction/nougat.mmd` |
| 3 | Report (LaTeX) | `report/REPORT.tex` |
| 4 | Open questions | `report/open_questions.json` (5 Qs + next_steps) |
| 5 | Workflow | `report/workflow.md` |
| 6 | Artifacts summary | `report/artifacts_summary.md` (this file) |
| 7 | Failure analysis | `report/failure_analysis.md` |
| 8 | Evidence | `report/evidence/` (result JSON + driver + kernel + recipe) |

## Evidence files
- `report/evidence/kumar2015_result.json` — full flux sweep + explicit-flux section + verdict fields.
- `report/evidence/run_kumar2015.py` — from-scratch uniform-flux driver.
- `report/evidence/run_kumar2015_explicit_flux.py` — explicit (2π,π/2,π/2) doubled-cell driver.
- `report/evidence/loop_current_kagome_kernel.py` — kernel (credited).
- `report/evidence/replication_recipe.json` — prep recipe.

## Kernel credit
`loop_current_kagome_kernel.py` — `KagomeModel`: NN kagome tight-binding +
Peierls loop-current flux + Fukui–Hatsugai–Suzuki Chern number + loop-current
order parameter. Originally built for Fernandes–Birol–Ye–Vanderbilt
(arXiv:2502.16657); reused here for the kagome flux-phase class.

## Self-score
- **Coverage: 9/10** — full pipeline, all 8 artifacts, correct model & mechanism
  extracted, AND the paper's explicit (2π, π/2, π/2) flux state built on the
  doubled 6-site magnetic cell with numerically-verified plaquette fluxes;
  missing only the fully self-consistent flux solve and XXZ-anisotropy sweep.
- **Agreement: 9/10** — exact match on the quantized σ_xy^s = 1/2 and occupied
  Chern = +1, now in the paper's EXPLICIT flux (not just a uniform proxy), with
  correct Heisenberg baseline; only the self-consistent onset in h/J and the
  band-by-band per-band Chern labels (touching-band gauge) remain open.
