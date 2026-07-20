# Artifacts Summary — Yuan & Chen 2023 (polar SkX in PbTiO3)

**Verdict: REPLICATED** (reduced 2D LGD; headline sub-claims reproduced)
**Coverage: 7/10  ·  Agreement: 8/10  ·  Runtime: ~0.5 s (budget 6 min)**

## Headline tested
Out-of-plane field stabilizes a hexagonal close-packed polar skyrmion lattice
(each |Q|=1) that collapses to a single-domain ferroelectric (Q->0) at high field.

## Key numbers (from `work/yuan2023_result.json`)
| Quantity | Value |
|---|---|
| Seeded cores | 16 |
| Net integer charge Q_net (SkX, Ez=0) | 15.86 (~16) |
| Mean |Q| per core | 0.99 (~1) |
| Total \|Q\| low field (Ez=0) | 27.80 |
| Total \|Q\| high field (Ez=2.4) | 0.0016 (~0) |
| Mean Pz low -> high field | 0.00 -> 1.17 (single-domain FE) |

## Artifact inventory (8)
1. `extraction/marker.md` — pdftotext-layout extraction + marker-style header (interim; neural marker unavailable).
2. `extraction/nougat.mmd` — pdftotext-layout extraction + nougat MMD header (interim; neural nougat unavailable).
3. `report/REPORT.tex` — full replication write-up (LaTeX).
4. `report/open_questions.json` — 5 open questions {question, why_it_matters, next_step} + next_steps.
5. `report/workflow.md` — end-to-end method, iterations, reproduce command.
6. `report/artifacts_summary.md` — this file.
7. `report/failure_analysis.md` — honest gaps, detector caveats, numerical pitfalls.
8. `report/evidence/` — `yuan2023_result.json`, `yuan2023_replication.py`, and both credited kernels.

## Figures (`report/figs/`)
- `skyrmion_vs_Ez.png` — total |Q| and core count vs Ez (the collapse curve).
- `polar_textures.png` — Pz + in-plane quiver for SkX / partial / FE.
- `pontryagin_density_SkX.png` — |Pontryagin density| of the SkX ground state.

## Provenance / credit
- `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` — TDGL relaxation + seeding.
- `ollie_berg_luscher_topological_charge_kernel.py` — Berg-Luscher Pontryagin charge.

## Scoring rationale
- **Coverage 7/10:** reproduced SkX existence, per-core |Q|=1, and field-driven
  SkX->FE collapse; did NOT cover spontaneous field-induced nucleation, the
  labyrinth/stripe low-field phases, the full T-E phase diagram, or Kittel w^2~h.
- **Agreement 8/10:** for the sub-claims tested, agreement is strong and
  quantitatively clean (integer Q_net, monotone |Q| collapse, Pz saturation);
  docked because field magnitudes are reduced-unit, not physical MV/cm.
