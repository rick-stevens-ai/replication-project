# Artifacts Summary — TEXTURE-polar-zhou2021

## Verdict: PARTIAL (strong) — Coverage 8/10, Agreement 8/10

Reduced 2D TDGL phase-field core reproduces all TOPOLOGICAL claims of
Zhou et al. 2021; dielectric claim reproduced in direction only (magnitude out
of scope). No fabrication — every number below is from real code runs.

## Claim-by-claim scorecard

| # | Claim | Metric | Result | Status |
|---|-------|--------|--------|--------|
| 1 | Symmetric skyrmion Q=+1, ring Pontryagin density, 2-peak line profile | Q_relaxed; ring peak r; n_peaks | Q=1.000; peak r=13 (R=16); 2 peaks (27,54) | REPRODUCED |
| 2 | Small V/narrow electrode: reversible erase + recover | Q_under before/field/recover | 6.33 -> -0.0 -> 5.99 | REPRODUCED |
| 3 | Neighbour asymmetric but topologically protected (Q=+1) | local Q of surviving bubble | 0.83 -> rounds to +1 | REPRODUCED |
| 4 | High V/wide: labyrinthine; Q +1->0 before destruction; small recovers/large locked | net Q of partial bubble; recover_frac | netQ=0.005 (mixing 0.97); small=1.34 / large=0.37; bubbles 158 vs 10 | REPRODUCED |
| 5 | Dielectric decreases as skyrmions shrink/burst | eps(V) proxy | 40.49 -> 40.04 monotonic; area 3011->1761 | PARTIAL (direction only) |

## Files
### code/
- `phasefield.py` — model: TDGL solver, Berg-Luscher topological charge, Neel skyrmion/lattice, electrode field
- `exp1_topo_charge.py` — Claim 1
- `exp2_erase_recover.py` — Claims 2 & 3
- `exp3_highfield_dielectric.py` — Claims 4 & 5
- `exp4_recovery_asymmetry.py` — Claim 4 (recovery asymmetry)
- `make_figs.py` — figure generation

### work/ (real run outputs)
- `exp1_result.json`, `exp2_result.json`, `exp3_result.json`, `exp4_result.json`
- `*.npy` — polarization fields

### figs/
- `figA_single_skyrmion.png` — skyrmion + ring Pontryagin density + line profile
- `figB_erase_recover.png` — initial / erased-under-electrode / recovered
- `figC_recovery_asymmetry.png` — small-field recovered vs large-field labyrinthine
- `figD_dielectric.png` — permittivity proxy & skyrmion area vs field

### report/
- `REPORT.tex` — full section-by-section report
- `open_questions.json` — 5 new questions
- `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`

## Key evidence quotes (from work/*.json)
- exp1: `"Q_relaxed": 1.0, "two_symmetric_peaks": true`
- exp2: `"erased_under_electrode": true, "recovered_under_electrode": true, "neighbor_Q_protected_near_1": true`
- exp3: `"Q_plus1_to_0_before_destruction": true, "dielectric_monotonic_decrease": true`
- exp4: `"recovery_asymmetry_confirmed": true` (small 1.335 / large 0.373)
