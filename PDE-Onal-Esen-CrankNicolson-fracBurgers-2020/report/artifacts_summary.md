# Artifacts Summary — Onal & Esen 2020 replication

## Layout
```
PDE-Onal-Esen-CrankNicolson-fracBurgers-2020/
├── report/
│   ├── REPORT.md                    canonical narrative report (Markdown)
│   ├── REPORT.tex                   full LaTeX report with dedicated critique section
│   ├── open_questions.json          5 truly-open follow-on research questions
│   ├── workflow.md                  chronological process record
│   ├── artifacts_summary.md         (this file) index of every artifact
│   └── failure_analysis.md          what did NOT reproduce and why
├── extraction/
│   └── marker.md                    marker-OCR extraction of paper text/tables
├── evidence/
│   ├── results_all.json             machine-readable Tables 1–7 (ours vs paper)
│   ├── run_full.log                 raw stdout of the full sweep on uicgpu
│   ├── evidence_convergence.txt     spatial-order fit from Table-1 data
│   ├── fig1_repro.png               solution-vs-exact plot for Ex1
│   └── judge_results.json           multi-judge scoring (3 Argo models)
├── work/
│   └── cn_frac_burgers.py           independent Python 3 + NumPy solver
├── artifact_harvest.md              PDF provenance (Wayback Machine)
└── attempt_log.md                   step-by-step notes incl. forcing-time-level study
```

## Primary results (from `evidence/results_all.json`)

| Table | Scope | Deviation vs paper | Status |
|---|---|---|---|
| Table 1 | Ex1 M-sweep at γ=0.5, ν=1, Δt=0.00025, tf=1 | 0.000% (8 sig figs, both L² and L∞) | **EXACT** |
| Table 2 (Present col) | Ex1 M ∈ {40, 80, 100} | 0.000% | **EXACT** |
| Table 3 | Ex1 ν-sweep, N=40 | our N=40 value matches paper's own Table 1 at N=40 (1.2201) but paper's Table 3 lists 0.4176 | **paper-internally inconsistent** |
| Table 4 | Ex1 γ-sweep at N=120 | 0.000% | **EXACT** |
| Tables 5–7 | Ex2 (`t² cos(πx)`) and Ex3 (`t² eˣ`) | ours 60–95% below paper; forcing symbolically verified | **not reproduced (attributed to paper)** |

## Convergence check
- Spatial order estimated from Table-1 M ∈ {10, 20, 40, 80}: **≈ 2.06 → 2.86** (see `evidence/evidence_convergence.txt`).
- Consistent with central-difference O(Δx²) design (temporal error negligible at fixed Δt=0.00025 for the coarser M).

## Multi-judge scoring (from `evidence/judge_results.json`)

| Judge | Verdict | Confidence |
|---|---|---|
| argo:gemini-2.5-pro | REPLICATED | 1.00 |
| argo:gpt-4.1 | REPLICATED | 0.98 |
| argo:gpt-5.2 | PARTIAL | 0.86 |

Majority: **REPLICATED** (2/3), one PARTIAL dissent.

## Provenance
- Publisher PDF recovered from **Wayback Machine** snapshot dated **2020-08-19** of `content.sciendo.com` (live Sciendo/De Gruyter pages dead / bot-walled).
- Full harvest details: `artifact_harvest.md`.

## Reproducibility recipe
```bash
cd work
python3 cn_frac_burgers.py      # runs Tables 1–7 vs paper; writes evidence/results_all.json
python3 judge.py                # multi-judge Argo scoring via localhost:44497
```
Runtime on `uicgpu`: minutes for the tabulated sweeps.
