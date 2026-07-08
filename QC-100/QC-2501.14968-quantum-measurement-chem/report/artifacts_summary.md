# Artifacts Summary — QC-2501.14968

Paper: Patel, Jayakumar, Yen, Izmaylov, *Quantum Measurement for Quantum
Chemistry on a Quantum Computer*, arXiv:2501.14968 (2025). Review article.

Verdict: **REPLICATED** for the analytical spine (Eq. 63, optimal-allocation
metric, 2–4× grouping reduction, FC>QWC).

## Directory layout

```
QC-2501.14968-quantum-measurement-chem/
├── report/
│   ├── REPORT.md                        # source-of-truth prose (existing)
│   ├── REPORT.tex                       # typeset version (this backfill)
│   ├── open_questions.json              # 5 open questions (JSON list)
│   ├── open_questions_section.tex       # LaTeX version, \input by REPORT.tex
│   ├── workflow.md                      # method + pipeline
│   ├── artifacts_summary.md             # THIS FILE
│   ├── failure_analysis.md              # honest critique
│   └── evidence/                        # per-run logs and JSON dumps
├── artifacts/
│   ├── grouping_summary_v3.json         # canonical numerical result
│   ├── h2_shot_noise_result.json        # Monte-Carlo cross-check
│   ├── h2_pauli_terms.json              # H2 Pauli decomposition
│   ├── h2_grouping_result.json          # H2 QWC/FC grouping
│   ├── measurement_grouping_v3.py       # main script
│   └── h2_shot_noise_vqe.py             # MC shot-noise script
└── extraction/
    └── nougat.mmd                        # extracted arXiv text (stub — this backfill)
```

## Headline numbers (all independently computed)

| Quantity | Value | Paper claim | Match? |
|---|---|---|---|
| H2 E_gs (STO-3G, R=0.735) | −1.137306 Ha | textbook | yes (1e-14) |
| LiH E_gs (STO-3G, R=1.595) | −7.882402 Ha | textbook | yes (1e-14) |
| LiH QWC M_opt reduction | 3.03× | 2–4× (Crawford et al., reviewed) | **yes, inside window** |
| LiH FC M_opt reduction | 53.8× | FC > QWC (reviewed) | **yes, direction + magnitude** |
| LiH # QWC groups | 136 | (not tabulated) | — |
| LiH # FC groups | 35 | (not tabulated) | — |
| H2 shot-noise σ scaling | ~1/√N (10× shots → 3.2× lower σ) | Eq. 63 CLT | yes |

## Files (with size / provenance)

- `artifacts/grouping_summary_v3.json` — canonical result JSON; produced by
  `measurement_grouping_v3.py`. Contains per-molecule per-fragment variances,
  group counts, and `M_opt` values for ungrouped / QWC / FC.
- `artifacts/h2_shot_noise_result.json` — 200-repeat MC output at 1.5k/15k/150k
  shots; produced by `h2_shot_noise_vqe.py`.
- `artifacts/measurement_grouping_v3.py` — main pipeline (PySCF → JW → dense
  diag → variance sweep → greedy coloring → M_opt).
- `artifacts/h2_shot_noise_vqe.py` — Monte-Carlo cross-check on H2.
- `report/REPORT.md` — narrative + assessment (unchanged by this backfill).
- `report/REPORT.tex` — LaTeX version with honest critique section (added
  by this backfill).
- `report/open_questions.json` / `open_questions_section.tex` — 5 open
  questions with concrete probes (added by this backfill).
- `report/failure_analysis.md` — honest critique (added by this backfill).
- `report/workflow.md` — pipeline documentation (added by this backfill).
- `extraction/nougat.mmd` — extracted paper text stub (added by this backfill).

## Compute footprint

- CPU-only, local venv, no external endpoints.
- H2 pipeline: seconds. LiH pipeline: minutes. MC on H2: ~1 minute per budget.
- No GPU, no cloud, no LLM in the numerical path.

## Provenance / reproducibility

- All Python: pyscf 2.13, qiskit 2.5, qiskit-nature 0.8, openfermion 1.7,
  numpy stock.
- No random seeds needed for analytical results (deterministic).
- MC used numpy default RNG (seed logged in `h2_shot_noise.log`).
