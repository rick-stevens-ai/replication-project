# LUCID replication: Stochastic DNA Fragments Rejoining (Li et al. 2012)

Independent open reimplementation of:

> Li Y, Qian H, Wang Y, Cucinotta FA (2012). *A Stochastic Model of DNA Fragments
> Rejoining.* PLoS ONE 7(9): e44293. [doi:10.1371/journal.pone.0044293](https://doi.org/10.1371/journal.pone.0044293)

Pure NumPy / Python Gillespie direct method. CPU only. No external data.

## Quick start

```bash
cd code/
python3 smoke_test.py                  # ~1 s, verifies simulator
python3 run_fig4_kinetics.py           # ~2 s, reproduces Fig 4
python3 run_fig3_impact_factors.py     # ~5 s, reproduces Fig 3 trends
```

Outputs land in `results/` (NPZ arrays) and `figures/` (PNGs); per-experiment
logs in `logs/`.

## What's where

- `code/gillespie_rejoining.py` — the simulator + initial-distribution helpers.
- `code/run_fig4_kinetics.py` — Fig 4: mean kinetics γ-ray vs Fe-ion.
- `code/run_fig3_impact_factors.py` — Fig 3 trends: V, count, mean-length sweeps.
- `REPORT.md` — claim-by-claim comparison, numerical results, limitations.
- `PROGRESS.md` — replication progress log.

## Headline result

| Condition | Mean rejoin time (arb units) | Median | Std |
|---|---:|---:|---:|
| Low-LET γ (3% short fragments) | 15.6 | 14.8 | 5.0 |
| High-LET Fe (30% short fragments) | 35.7 | 22.7 | 35.4 |

Sharp L\* = 45 bp threshold in `Fig 3(b)`: mean rejoin time drops 6.3× across
the threshold (90.1 → 14.4 arb units).

## Status

✅ Implementation complete · ✅ Smoke-tested · ✅ ≥2 figure trends reproduced ·
✅ Central biological claim reproduced.

See `REPORT.md` for the full claim table and limitations.
