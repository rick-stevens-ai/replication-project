# Artifacts Summary — lucid-stochastic-rejoining

## Directory inventory

```
lucid-stochastic-rejoining/
├── PROGRESS.md
├── README.md
├── REPORT.md                          ← REPASS-1 verdict (canonical text report)
├── REPORT.pass1.md                    ← pass-1 report, preserved verbatim
├── PARSER_PROVENANCE                  ← Marker canonical parse pointer + sha256
├── report/                            ← BACKFILL 2026-07-06 artifacts
│   ├── REPORT.tex                     ← LaTeX build of the report
│   ├── open_questions.json            ← 5 open questions, machine-readable
│   ├── open_questions_section.tex     ← \input-able LaTeX section
│   ├── workflow.md                    ← tools/versions/reproducer
│   ├── artifacts_summary.md           ← THIS FILE
│   └── failure_analysis.md            ← honest critique
├── code/
│   ├── gillespie_rejoining.py         ← core SSA implementation
│   ├── run_fig3_impact_factors.py     ← pass-1: L̄, V, M_T sweeps
│   ├── run_fig4_kinetics.py           ← pass-1: biphasic high/low-LET kinetics
│   ├── smoke_test.py                  ← pass-1: single-run correctness
│   └── repass1/                       ← REPASS-1 six-claim battery
│       ├── brief.md
│       ├── c7_revisit_biphasic_fit.py
│       ├── c9_secondary_jump.py
│       ├── c10_event_count_check.py
│       ├── c11_2d_fraction_surface.py
│       ├── c12_variance_check.py
│       └── c13_k3_sweep.py
├── extraction/
│   └── nougat.mmd                     ← BACKFILL: stub w/ paper.pdf sha256
├── logs/
│   ├── (pass-1 *.log)
│   └── repass1/                       ← JSON summaries + stdout logs
├── results/
│   ├── (pass-1 *.npz)
│   └── repass1/                       ← c{7,9,10,11,12,13}_*.npz
├── figures/
│   ├── (pass-1 *.png)
│   └── repass1/                       ← c{7,9,11,12,13}_*.png
└── artifacts/
    └── repass1/                       ← reserved
```

## Artifact classes

### Text reports
- `REPORT.md` — canonical REPASS-1 verdict (Markdown)
- `REPORT.pass1.md` — pass-1 verdict, preserved
- `report/REPORT.tex` — LaTeX build for typeset PDF distribution
- `report/failure_analysis.md` — honest critique (this backfill)

### Code
- `code/gillespie_rejoining.py` — Gillespie SSA implementation of the three-channel reaction system (recruitment, joining, release) with fragment-length gating at $L_m$ and $L^\ast$.
- `code/run_fig3_*.py`, `code/run_fig4_*.py` — pass-1 sweep drivers.
- `code/repass1/c*.py` — one script per REPASS-1 claim; each ends in a JSON dump + optional matplotlib figure.

### Traces (evidence of runs)
- `logs/repass1/*.json` — machine-readable summaries with rate constants, seeds, sample sizes, headline numbers.
- `logs/repass1/*.log` — full stdout capture per script.
- `logs/*.log` — pass-1 stdout captures.

### Numerical outputs
- `results/*.npz`, `results/repass1/*.npz` — NumPy binary arrays: full-length T distributions, event-count vectors, k3-sweep tables, (r1,r2) heatmap grids.

### Figures
- `figures/*.png` — pass-1 mean-time vs L̄ / V / M_T plots, biphasic kinetics log-time plots.
- `figures/repass1/*.png` — c9 secondary-jump plot, c11 2D heatmap, c12 std-vs-L̄ discontinuity, c13 k3 sweep, c7-rev biexponential fit.

### Machine-readable metadata
- `PARSER_PROVENANCE` — Marker canonical parse pointer + sha256 (added REPASS-1).
- `report/open_questions.json` — 5 open questions in structured form (this backfill).
- `extraction/nougat.mmd` — nougat parse stub (this backfill; not required — Marker was clean).

## Friction tags (from REPORT.md §11, condensed)

| Tag | Description | Severity |
|-----|-------------|----------|
| `parser:pass-1-pre-marker` | Pass-1 text source predates canonical Marker; REPASS-1 verified originals correct | resolved |
| `paper-simplification:recruit-count` | Paper's "2 M_T recruits" is informal upper bound; observed ~2.58 M_T | flagged, doesn't overturn biology |
| `axis-asymmetry:C11-r1-weak` | Fig 3(d) symmetric-looking surface is r2-dominated (0.89 vs 0.39 corr) | paper-side omission |
| `secondary-jump:confirmed` | Paper's L*/m prediction under-emphasised; strongly reproduces at L*/2 | improved paper coverage |
| `data:53BP1-foci-not-digitized` | C7 external calibration deferred (Asaithamby scatter Fig 4 not tabulated) | data gap, not model gap |
| `simplification:spatial-geometry` | Well-mixed assumption — no chromosome territories | scope limit |
| `simplification:no-aberration-scoring` | Rejoining times reported; chromosome aberrations not scored | scope limit; see Q5 |
| `numerics:weighted-choice-linear` | O(N) event sampler adequate for M_T ≤ 50; PQ needed for bigger | scaling |

## Provenance / integrity

- **Paper PDF sha256:** see `extraction/nougat.mmd` for hash pointer.
- **Marker parse:** canonical path `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/10_1371_journal_pone_0044293/`.
- **Author code:** NOT available (checked PLoS, GitHub, Cucinotta lab pages — all empty).
- **All code in this dir is our reimplementation** from the paper's equations only.

## Distribution notes

- Complete reproducer runs in ~50 s CPU on any modern laptop — no HPC needed.
- Zero external data dependencies (except C7 which is honestly deferred).
- Zero paid endpoints.
- LaTeX report needs `pdflatex` (TeX Live 2024+) with standard packages (amsmath, booktabs, longtable, hyperref, xcolor, listings).
