# Artifacts summary — Treeby & Cox (2010) k-Wave replication

Verdict: **REPLICATED** (C1, C2, C3 — the paper's three testable numerical claims).

## Reports
| File | Purpose |
|---|---|
| `report/REPORT.md` | Canonical prose replication report (claims table, method, results, verdict). |
| `report/REPORT.tex` | LaTeX version + dedicated **GENUINE CRITIQUE** section. |
| `report/open_questions.json` | 5 truly-open follow-on questions (fractional absorption, heterogeneous/interface, GPU/multi-node scaling, elastic extension, FDTD/DG comparison). |
| `report/workflow.md` | Step-by-step independent-replication protocol. |
| `report/failure_analysis.md` | What went wrong and how it was fixed. |
| `report/artifacts_summary.md` | This file. |

## Kernel & experiments (`work/`)
| Script | Runtime | Purpose |
|---|---|---|
| `work/exp_C1_temporal_dispersion.py` | ~1 s | 1D CFL sweep 0.1..5.0 — k-space vs plain PSTD vs d'Alembert analytic. |
| `work/exp_C2_2d_gaussian.py` | ~5 s | 2D Gaussian source at 3 μs vs Hankel analytic (256², σ=0.5 mm). |
| `work/exp_C2b_disk_selfconv.py` | ~45 s | 2D disk PSA self-convergence, N ∈ {128,256,512,768}, snapshot 3 μs. |
| `work/exp_C3_ppw_convergence.py` | ~5 s | 1D traveling sinusoid, PPW ∈ {2..32}, k-space vs plain PSTD vs FD2. |
| `work/attempt.log` | — | Development log including the first-timestep leapfrog bug + fix. |

## Evidence (`report/evidence/`)

### C1 — temporal dispersion / stability
- `C1_cfl_sweep.csv`, `C1_cfl_sweep.txt`
- Key numbers: k-space L2 = 2e-15 across CFL 0.1..5.0; plain PSTD blows up at CFL ≥ 0.7.

### C2 — analytic-solution comparison
- `C2_gaussian_summary.csv`, `C2_gaussian_summary.txt`
- `C2_gaussian_snapshot.png` — 2D pressure snapshot at 3 μs.
- `C2_gaussian_cut.png` — horizontal cut vs Hankel analytic.
- Key numbers: k-space L2 = 1.07e-5 vs plain PSTD 9.40e-3 (~880× better at same cost).

### C2b — disk PSA self-convergence
- `C2b_disk_selfconv.csv`, `C2b_disk_selfconv.txt`
- `C2b_disk_selfconv.png`
- Key numbers: N=768 leading-front peak at x = 7.467 mm vs physical 7.500 mm (miss = Δx = 0.033 mm).

### C3 — spectral convergence at ~2 PPW
- `C3_ppw_convergence.csv`, `C3_ppw_convergence.txt`
- Key numbers: k-space L2 = 3e-15 at PPW=2; FD2 needs PPW=32 to reach 2e-2.

### Judge cross-check
- `judge_prompt.txt` — prompt sent to Argo GPT-4o (`127.0.0.1:44497`, key `stevens`).
- `judge_response.txt` — judge's coverage/honesty audit; does not overrule numerical evidence.

## Environment
- Host: CherryRd (macOS 25.3.0)
- Python 3, NumPy 2.4.3, SciPy 1.18.0, Matplotlib
- No GPU, no network, no MATLAB, no k-Wave code consulted (paper equations only).

## Constants
- c₀ = 1500 m/s (water), ρ₀ = 1000 kg/m³
- 1D grid: 512 pts / 51.2 mm (C1, C3)
- 2D grid: 256² / dx=0.1 mm (C2 Gaussian); 128/256/512/768 (C2b disk)

## Reproducibility
Deterministic; rerun `python3 work/exp_*.py` to regenerate all CSV/PNG (~1 min total).
