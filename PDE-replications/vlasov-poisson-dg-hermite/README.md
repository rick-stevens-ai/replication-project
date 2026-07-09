# Vlasov–Poisson DG/Hermite Replication

Independent open-source replication of the SW-Hermite + spectral/DG-x family
of Vlasov–Poisson solvers (Bessemoulin-Chatard & Filbet, Filbet–Sonnendrücker,
Schumer–Holloway, Camporeale–Delzanno).

See `REPORT.md` for the full claim-by-claim table and `PROGRESS.md` for the
session log.

## Quick start

Requires Python 3.10+, NumPy, Matplotlib.

```bash
cd code
# Linear Landau damping benchmark
python run_landau.py --Nx 64 --N 64 --T 30 --dt 0.005

# Convergence sweep in Hermite mode count
python run_convergence.py

# Classical two-stream instability
python run_two_stream.py --variant classical --Nx 128 --N 96 --T 40 --dt 0.005

# Re-generate figures
python make_figures.py
```

Results land in `../results/*.npz` and `../results/*.json`; figures in
`../figures/`.

## Headline numbers

| benchmark | measured | reference |
|---|---|---|
| Landau damping rate γ (Nx=64, N_H=64) | −0.1546 | −0.1533 (0.9 % err) |
| Two-stream growth rate γ (Nx=128, N_H=96) | +0.221  | +0.2845 (22 % low) |
| Mass conservation (Landau, T=30)        | 2.5×10⁻⁸ rel | exact in theory |
| Momentum conservation                   | machine | exact in theory |
| Total energy drift (Landau, T=30)        | 1.6×10⁻⁶ rel | exact in theory |

Coverage / agreement score: **0.83 (5/6 ✅, 1 partial)**. See REPORT for
details and limitations.
