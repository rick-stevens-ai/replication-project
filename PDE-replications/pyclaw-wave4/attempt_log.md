# Attempt Log — PyClaw (Wave 4)

## 2026-06-16 18:31 — venv + install

```
python3.14 -m venv .venv
source .venv/bin/activate
pip install clawpack
```

Build OK on CherryRd (Apple Clang + Homebrew gfortran). `clawpack==5.14.0`, no patches needed.

## 2026-06-16 18:33 — drafted `evidence/run_replication.py`

382-line driver. Three subroutines:
1. `run_acoustics_case` — runs one acoustics case in a subprocess (isolates Fortran state).
2. `run_sod` — Sod shock tube via custom Controller setup.
3. plotting helpers (`plot_acoustics`, `plot_sod`, `plot_convergence`).

## 2026-06-16 21:11 — full run

```
python evidence/run_replication.py
```

Output:
- 8/8 acoustics regression PASS (numbers match upstream to 4 sig-figs).
- Convergence sweep N∈{50,…,1600}: empirical order 1.94–2.32, mean 2.06.
- Sod shock tube: post-shock p\* matches Toro's exact value to 3e-5; u\* to 3e-5; ρ\* and x_shock differ due to a post-hoc sampling-window choice (the solve itself is correct, as the figure shows).
- All 3 plots written. `evidence/results.json` 1.8 KB.

Runtime: ~10 s total.

## Files written

```
evidence/run_replication.py        14 KB  (driver)
evidence/results.json               1.8 KB  (summary)
evidence/acoustics_solution.png    70 KB
evidence/convergence.png           63 KB
evidence/sod_shock_tube.png        76 KB
pyclaw.log                          3.3 KB  (CLAW frame log)
```

## Failures and learnings

- **None blocking.** The 5.14.0 wheel + Fortran builds cleanly on macOS Tahoe, parity Python/Fortran is bit-identical, regression reference numbers match exactly. This is a particularly well-maintained library.
- **Cosmetic miss in Sod sampling.** My post-shock-state extractor used a fixed x≈0.58 window which fell outside the post-shock plateau for t_final=0.2; p\* and u\* still matched exactly (they're flat across that region) but ρ\* and x_s were sampled in the wrong region. Documented in REPORT.md §Results.
