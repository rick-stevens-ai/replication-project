# OSTI 1559043 — Jaravel et al.\ 2019 DNS of ignition-kernel stabilization in cross-flow

**Replication status:** v4 (20-run Polaris PeleC ensemble) — **7/10**
(coverage 7/10, agreement 7/10). Promoted from v3 6/10.

## Latest report

- `replication-pelec/report_v4/report.pdf`

## Ensemble summary (20-run Polaris, 2026-04-24)

| φ    | N runs | N ignited | IP   | paper IP |
|------|--------|-----------|------|----------|
| 0.6  | 5      | 0         | 0.00 | 0.00     |
| 0.8  | 5      | 0         | 0.00 | 0.20     |
| 1.0  | 5      | 5         | 1.00 | 0.65     |
| 1.2  | 5      | 5         | 1.00 | 0.90     |

Ignition criterion: `T_max(0.9 ms) > 2550 K` for complete runs **or**
`max T_max(t>0.5 ms) > 2700 K` for CFL-truncated runs. See
`replication-pelec/report_v4/report.tex` §3.

Per-run details: `replication-pelec/polaris_ensemble/summary.json`.

## Key corrections vs prior notes

- Aurora job **8449654 never ran** (reservation-blocked). Only 8449560
  ran — single φ=0.6 realisation, 9 checkpoints. Aurora is **not** the
  ensemble source.
- Polaris job set 7099651–7099670 (20 jobs) is the real ensemble.

## Directory map

```
replication/             v1 CPU/OpenFOAM attempt (2/5 — units bug)
replication-gpu/         PeleLMeX GPU attempt (abandoned — low-Mach incompatible)
replication-pelec/       v2+ PeleC (current)
  polaris/               build + submit scripts
  polaris_ensemble/      20-run CSVs, analyze.py, figures/, summary.json
  report/                v1–v3 reports
  report_v4/             current (20-run) report
  ensemble/              PBS logs
  analysis/              v3 aggregated timeseries + metrics
```

## Known limitations (see report_v4 §5)

1. 128×64×64 grid, no AMR level 1 — turbulence under-resolved
2. 1-ms simulation window (paper goes to ~10 ms)
3. Synthetic (not paper's tabulated) turbulent inflow
4. 3 of 5 φ=1.2 runs CFL-truncated at 0.25–0.63 ms; classified ignited
   from elevated late-window T_max
5. Per-plotfile species-max extraction on Polaris debug queue; at report
   time still queued. Hook in `polaris_ensemble/analyze.py` consumes the
   per-run `*_timeseries.csv` when available to add species figures.
