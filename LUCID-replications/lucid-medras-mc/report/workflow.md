# Workflow — Medras-MC replication (LUCID batch)

## Objective
Re-run the mechanistic Monte Carlo backbone of McMahon & Prise (2021)
Medras-MC and confirm all shipped-code-derived observables match the paper.

## Stages

### Stage 0 — Repo + openness
- `git clone https://github.com/sjmcmahon/Medras-MC` @ commit `0e51be7`
- Verified per-file BSD-2-Clause header (no top-level `LICENSE` file — noted as friction).
- Confirmed FOSS deps: numpy, scipy, openpyxl, matplotlib.

### Stage 1 — Damage generation
- Called `damagegenerator.damageModel.basicXandIon(runs=20)`.
- Output: 23 SDD v1.0 damage files (photons 6 doses; protons 10 LETs; carbon 7 LETs).
- Nucleus radius 4.229 μm; 46 chromosomes; 35 DSB/Gy; p_complex=0.43; directFrac=0.4.
- Wall: 114 s.

### Stage 2 — Repair MC
- Called `repairanalysis.medrasrepair.repairSimulation(folder, 'Fidelity')`.
- Defaults: `repeats=50`, `repairFailure=True`, `addFociDelay=True`.
- Output: per-file Fidelity summary + 0.1 h kinetics trace to 25 h.
- Wall: 144 s.

### Stage 3 — Parse + plot
- `scripts/parse_and_plot.py` → `results/fidelity_summary.csv` + 3 figures.
- Wall: <2 s.

### Stage 4 — Claim-by-claim table
- 7 mechanistic claims (C1–C7) extracted from paper text/figures.
- All 7 reproduced qualitatively; 2/2 testable-quantitative within paper-stated uncertainty.

### Stage 5 — Documentation
- Original `REPORT.md` at top level (2026-05-28).
- Backfill (this doc): `report/REPORT.tex`, `open_questions*`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd`.

## Out-of-scope (not attempted)
- MID-vs-cell-line survival scatter (Fig 4) — requires Paganetti compilation.
- RBE-vs-LET overlays with data (Fig 5).
- Dose-rate sparing curves (Fig 6) — requires Lehmann/Newman raw.
- Dose-rate MID predictions (Fig 7).
- PIDE 3.4 dataset — GSI registration wall.

## Reproducibility gates
- Deterministic seed: NOT exposed by upstream → ±5–10% run-to-run at 20×50 repeats.
- Filesystem order: `os.listdir` nondeterministic → sorted downstream.
- Kinetics column labels: absent → inferred from `kineticLimit` and stride.
