# Workflow — arXiv:2305.04954 replication

**Set:** QC-100
**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2305.04954-xeb-phase-transition/`
**Host:** CherryRd (Darwin 25.3.0)
**Date of replication run:** 2026-07-03
**Backfill date:** 2026-07-06

## Environment
- Python 3.12.13, fresh venv at `./venv`
- `pip install cirq==1.7.0 numpy==2.5.0 matplotlib`
- No paid APIs, no LLM inference in physics pipeline.

## Steps (reproducible verbatim)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2305.04954-xeb-phase-transition/

# 1. Fetch paper
curl -sL https://arxiv.org/pdf/2305.04954 -o paper/2305.04954.pdf
pdftotext paper/2305.04954.pdf paper/2305.04954.txt

# 2. Environment
python3.12 -m venv venv
source venv/bin/activate
pip install cirq numpy matplotlib

# 3. Run simulation (main workhorse ~ 326.6 s on CherryRd)
python -u code/xeb_replication.py

# 4. Plot
python code/plot_results.py

# Outputs: results/xeb_sweep.json, results/fig_F_and_chi_vs_epsN.png,
#          results/fig_log_chi_vs_epsN.png
```

## Circuit family
- Architecture: 1D brickwork (paper's CPU-accessible geometry).
- Depth: `d=8` layers of Haar-random 2-qubit unitaries (QR of complex Ginibre matrix).
- Layer structure: alternating even/odd neighbor pairs.
- Noise: single-qubit depolarizing channel with parameter epsilon applied to every qubit after
  each unitary layer.
- Sweep: `epsilon in [0, min(0.30, 1.6/N)]`, 11 points, chosen so `epsilonN in [0, 1.6]` brackets
  the paper's theoretical Haar all-to-all threshold `ln(5/2) ~ 0.916`.
- N values: 4, 6, 8, 10 (exact statevector / density-matrix ceiling on CPU).
- Instance count K per N: 40, 30, 20, 10.

## Metrics
- Fidelity: `F = <psi_ideal | rho_noisy | psi_ideal>`.
- Linear XEB: `chi = 2^N * sum_x p_ideal(x) * p_noisy(x) - 1`, where
  `p_noisy(x) = rho_xx` (i.e. the honest measurement distribution of the noisy state).
- Diagnostic: ratio `chi / F` as a function of `epsilonN`.

## Sanity checks executed before believing outputs
- Depolarizing channel unit tests: `epsilon=1 -> I/2`, `epsilon=0.5 -> half-mix` (passed).
- `epsilon=0` sweeps recover `F=1` exactly across all N.
- Ideal `chi` averages ~ 1 at `epsilon=0` (Porter-Thomas), with finite-K scatter matching
  expectation.

## Headline exercised
Finite-size onset of `chi/F` divergence as `epsilonN` sweeps through order 1:
`chi/F` grows from ~ 1 to ~ 20 across the paper's theoretical Haar all-to-all threshold
`ln(5/2) ~ 0.916`, on 1D brickwork at N=10 d=8. This is the paper's central
qualitative claim; quantitative reproduction of the asymptotic -0.92/layer XEB decay
rate and the sharp step shape would require N ~ 40 (beyond CPU statevector reach).

## Files touched by this workflow
- `paper/2305.04954.pdf`, `paper/2305.04954.txt`
- `code/xeb_replication.py`, `code/plot_results.py`
- `results/xeb_sweep.json`, `results/fig_F_and_chi_vs_epsN.png`, `results/fig_log_chi_vs_epsN.png`
- `report/REPORT.md`, `report/REPORT.tex`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`
- `report/fig_F_and_chi_vs_epsN.png`, `report/fig_log_chi_vs_epsN.png` (copies)
- `report/evidence/xeb_sweep.json`, `report/evidence/xeb_replication.py` (evidence copies)
- `extraction/nougat.mmd` (stub — see file)
