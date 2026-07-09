# Artifact harvest

Every publicly-fetched artifact.

| # | Kind | URL / accession | Size | Local path | Notes |
|---|------|-----------------|------|-----------|-------|
| 1 | PDF | `http://bug.medphys.ucl.ac.uk/papers/2010-Treeby-JBO.pdf` | 414 458 B (12 p) | `work/treeby_cox_2010_kwave.pdf` | Author-hosted preprint of Treeby & Cox 2010 JBO paper (matches SPIE DOI 10.1117/1.3360308). Downloaded 2026-07-04. |
| 2 | Text extract | derived | 61 419 B | `work/kwave2010.txt` | `pdftotext` extract used to grep-verify equations & claims. |

## Prior download attempts (failed)

| URL | Result |
|-----|--------|
| `http://www.medphys.ucl.ac.uk/research/mle/pdf_files/J_2010_Treeby_JBO_k-Wave_MATLAB_toolbox.pdf` | curl timeout after 30 s (server unresponsive). |
| `https://www.spiedigitallibrary.org/journalArticle/Download?fullDOI=10.1117%2F1.3360308` | returned 212 B HTML (login gate). |

## Code / data written by this replication (all local, all in target dir)

- `work/kspace_pstd.py` — from-scratch NumPy k-space PSTD solver + analytic references.
- `work/exp_C1_temporal_dispersion.py` — CFL sweep, 1D Gaussian.
- `work/exp_C2_2d_gaussian.py` — 2D smooth-Gaussian propagation vs Hankel analytic.
- `work/exp_C2b_disk_selfconv.py` — 2D hard-edged disk PSA self-convergence sweep.
- `work/exp_C3_ppw_convergence.py` — spatial PPW convergence sweep (k-space vs PSTD vs FD2).
- `work/debug.py`, `work/check_analytic.py` — sanity-check scripts.

## Evidence files (results consumed by REPORT.md)

- `report/evidence/C1_cfl_sweep.{csv,txt}`
- `report/evidence/C2_gaussian_summary.{csv,txt}`
- `report/evidence/C2_gaussian_snapshot.png`, `C2_gaussian_cut.png`
- `report/evidence/C2_gaussian_snapshot.npy`, `C2_gaussian_analytic.npy`
- `report/evidence/C2b_disk_selfconv.{csv,txt,png}`
- `report/evidence/C3_ppw_convergence.{csv,txt}`
- (Earlier disk-vs-Hankel attempt files `C2_disk.*`, `C2_snapshot.*`, `C2_radial_profile.csv`, `C2_radial_cut.png` retained as artifacts documenting the debugging pass.)

## Reproducibility

All computation is CPU-only, uses only NumPy 2.4.3 + SciPy 1.18.0 + Matplotlib. No random seeds involved (deterministic FFTs). Every experiment reruns to identical numbers on the same machine in a few seconds (C1, C3) to ~45 s (C2b, the 768² sweep).

No k-Wave source code (MATLAB or C++) was fetched or consulted. Numerical results were compared only to closed-form analytic solutions (d'Alembert, Hankel transform of a Gaussian) and to internal self-convergence.
