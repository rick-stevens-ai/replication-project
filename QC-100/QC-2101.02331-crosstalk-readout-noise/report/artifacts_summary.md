# Artifacts Summary: QC-2101.02331-crosstalk-readout-noise

Set: QC-100. Verdict: REPLICATED.

## Directory layout

```
QC-2101.02331-crosstalk-readout-noise/
├── code/
│   ├── reproduce.py       # noise model, mitigation, metrics, QAOA grid
│   └── plot.py            # fig1_error_bars.png, fig2_qaoa_landscapes.png
├── evidence/
│   ├── results.json                # per-circuit + aggregate TVD, |ΔE|
│   ├── qaoa_grid_results.json      # grid best-cost, arg-max per surface
│   ├── qaoa_grids.npz              # 4 x 13x13 cost surfaces (numpy)
│   ├── run.log                     # stdout of reproduce.py
│   ├── tool_versions.txt           # pip freeze
│   ├── fig1_error_bars.png         # TVD + |ΔE| bar chart, 3 strategies
│   └── fig2_qaoa_landscapes.png    # 2x2 grid of cost surfaces
├── extraction/
│   └── nougat.mmd                  # PDF text-extraction placeholder
├── report/
│   ├── REPORT.md                   # source of truth (canonical, pre-existing)
│   ├── REPORT.tex                  # LaTeX version (added)
│   ├── workflow.md                 # step-by-step protocol (added)
│   ├── artifacts_summary.md        # this file (added)
│   ├── failure_analysis.md         # honest critique (added)
│   ├── open_questions.json         # 5 open Qs, JSON list (added)
│   └── open_questions_section.tex  # LaTeX open-Qs section (added)
└── venv/                            # local Python 3.14.6 venv
```

## Artifact inventory (8-artifact standard check)

| # | Artifact                        | Status    |
|---|--------------------------------|-----------|
| 1 | `report/REPORT.md`             | present (pre-existing) |
| 2 | `report/REPORT.tex`            | added |
| 3 | `report/workflow.md`           | added |
| 4 | `report/artifacts_summary.md`  | added |
| 5 | `report/failure_analysis.md`   | added |
| 6 | `report/open_questions.json`   | added (bare JSON list, 5 items) |
| 7 | `report/open_questions_section.tex` | added |
| 8 | `extraction/nougat.mmd`        | added (stub) |

Plus pre-existing evidence: `code/`, `evidence/*.json`, `evidence/*.png`, run
log, version pin.

## Headline numbers

- **Reduction factor (correlated vs raw, energy error):** 30.8x
- **Reduction factor (tensor-product vs raw, energy error):** 3.4x
- **Paper claim (IBM 15q Melbourne):** >22x
- **QAOA p=1 approximation ratio recovery:** ideal 0.788 → raw 0.718 →
  correlated 0.790

## Reproducibility

Deterministic seeded (`numpy.random.default_rng(seed)` per circuit; grid seed
fixed). `python code/reproduce.py` regenerates all evidence in < 5 min on
CherryRd CPU.
