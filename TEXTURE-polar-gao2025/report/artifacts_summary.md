# Artifacts Summary — TEXTURE-polar-gao2025

| Path | Description |
|---|---|
| `code/gao2025_replication.py` | Full replication: PS→n(r) field builder, Berg–Lüscher + FD topological charge, named-state eval, Q(2θ) sweep, hybrid builder, figure generation. numpy/matplotlib, CPU, <5 s. |
| `work/results.json` | All Q values: 4 named states + full Q(2θ) sweep (90°→45°). Saved before report writing. |
| `figs/textures.png` | pz-colour + in-plane-arrow textures for equator vortex, Q=−1 antiskyrmion, Q=+1 skyrmion. |
| `figs/Q_vs_2theta.png` | Q(2θ) along OAM branch (Berg integers + FD crossover), hybrid window shaded. |
| `figs/hybrid.png` | Hybrid state: +1 skyrmion lobe / −1 antiskyrmion lobe, net Q≈0. |
| `report/REPORT.tex` / `REPORT.pdf` | Full write-up with method, results table, figures, verdict, caveats. |
| `report/open_questions.json` | 5 open questions (q / basis / next_steps). |
| `report/workflow.md` | Step-by-step workflow + reproduce command. |
| `report/failure_analysis.md` | What broke, fixes, remaining limitations. |
| `report/method_extract.md` | (pre-existing) physics extraction from the paper. |
| `META.json` | Updated status + verdict. |

## Headline numbers
- Equator (2θ=90°): **Q = 0** (vortex/antivortex) — Claim 1 ✓
- 2θ=75°: **Q = −1** (antiskyrmion) — Claim 2 ✓
- Skyrmion reference: **Q = +1** — Claim 3 ✓
- Hybrid (2θ=70°): left lobe **+1**, right lobe **−1**, net **0** — Claim 4 ✓

## Verdict
**REPLICATED** at the field-topology level (all 4 topological-charge claims and
the PS-knob mechanism). Not a second-principles MD reproduction — energetics,
dynamics, and exact transition boundaries are out of scope.
