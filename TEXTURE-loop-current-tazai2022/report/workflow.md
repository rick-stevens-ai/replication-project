# Workflow — Tazai, Yamakawa & Kontani (arXiv:2207.08068v4)

Replication of *"Charge-loop current order and Z3 nematicity mediated by bond
order fluctuations in kagome metals."*

## 0. Environment
- Host: CherryRd (macOS), Python 3 + numpy 2.4.3 + scipy + matplotlib.
- No paid API / no external compute. All checks run locally in seconds.

## 1. Extraction
- `pdftotext -layout paper.pdf paper.txt` (1687 lines; a couple of embedded-image
  operator warnings, body text extracted cleanly).
- Prior attempt's `extraction/marker.md` already present and accurate — reused and
  cross-read against `paper.txt` (main text + Supplementary Notes 1-4).

## 2. Kernel reuse (no rebuild)
- Imported the shared loop-current mean-field kernel
  `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_meanfield_kernel.py`:
  - `kagome_cluster(Lx,Ly)` — periodic kagome torus, up/down triangle plaquettes.
  - `occupied_density(H, filling)` — one-body density matrix rho.
  - `bond_currents(H, rho, bonds)` — J_ij = -2 Im(H_ij rho_ji).
  - `loop_order`, `probe` — plaquette loop order + finite-field susceptibility.
- Copied verbatim into `code/reused_loop_current_meanfield_kernel.py` for provenance.

## 3. Paper-specific adaptation (`work/tazai2022_loop_current_checks.py`)
Added, on top of the kernel:
- `build_H_with_bo_clc(...)` — kagome NN Hamiltonian carrying BOTH a real
  even-parity BO modulation `dt^b` (Hermitian symmetric) and a pure-imaginary
  odd-parity cLC modulation `dt^c` (Hermitian antisymmetric, staggered up/down
  triangle 3Q texture).
- `velocity_ops` + `kubo_hall_realspace` — real-space Kubo intrinsic Hall
  conductivity, TRS-exact-zero for real H.
- `kagome_hk`, `bare_bands`, `lindhard_chi0` — momentum-space band structure and
  bare BO (inter-sublattice Lindhard) susceptibility for the nesting check.
- `folded_gap` — minimal 2-band avoided-crossing gap from combined BO+cLC.

## 4. Machine-checkable claims (5)
| # | Claim | Method |
|---|-------|--------|
| C1 | cLC (imaginary) carries bond currents; BO (real) does not | real-space bond currents on 6x6 torus |
| C2 | 3Q loop currents alternate hexagon vs triangle; zero net site current | oriented loop currents split by up/down triangle |
| C3 | AHE nonzero only with cLC, TRS-odd (dt^c -> -dt^c flips sign) | real-space Kubo sigma_xy vs dt^c |
| C4 | BO susceptibility chi0(q) peaks at M-point nesting, not Gamma | Lindhard chi0(q) on kagome bands at vHS filling |
| C5 | Hybridization gap Delta = 2 sqrt(\|dt^b\|^2 + \|dt^c\|^2) | 2-band folded avoided crossing |

## 5. Run + figures
- `python3 work/tazai2022_loop_current_checks.py` -> `work/results.json` (+ stdout summary).
- `python3 work/make_figs.py` -> `work/verification_figures.png`, `work/gap_scaling.png`.

## 6. Reporting
- `report/REPORT.tex` (+ compiled PDF if pdflatex available), this workflow,
  `artifacts_summary.md`, `failure_analysis.md`, `open_questions.json` (5),
  `extraction/marker.md`.

## Reproduce
```bash
cd work
python3 tazai2022_loop_current_checks.py   # prints 5/5, writes results.json
python3 make_figs.py                        # writes PNGs
```
