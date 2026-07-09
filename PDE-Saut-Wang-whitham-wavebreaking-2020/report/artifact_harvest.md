# Artifact harvest

| URL | local path | size | notes |
|---|---|---|---|
| https://arxiv.org/pdf/2006.03803v1 | work/saut-wang-2020.pdf | 292 912 B | Preprint of Saut & Wang (2020); md5 = 2836ac9b74155027eec69fc67b5056c0 |
| (extracted text) | work/full.txt | 55 kB (approx) | `pdftotext saut-wang-2020.pdf full.txt` |
| DOI 10.1137/20M1345207 | (SIAM published version) | paywalled | preprint text is identical for our purposes |
| Saut & Wang GitHub | none | — | No code accompanies the paper (purely analytical) |

**No accompanying code repository**: the paper is a purely analytical wave-breaking
proof, no numerical experiments in the paper itself. The replication was done
from-scratch with a Fourier pseudo-spectral solver (see `work/whitham_solver.py`).

## Code artifacts produced by this replication
| file | purpose |
|---|---|
| work/whitham_solver.py | Pseudo-spectral integrating-factor-RK4 solver for u_t + u u_x = L u_x |
| work/run_experiments.py | Driver: amplitude sweep for Burgers, Burgers-Hilbert, fKdV(-0.6), Whitham |
| work/verify_qualitative.py | Programmatic sanity check on the JSON results |
| work/results/full_results.json | Per-experiment time series (times, umax, umin, ux_min, mass, energy) |
| work/results/summary.json | Metadata + T*, walltime, |u|_∞ per experiment |
| work/figures/*.png | Per-experiment 3-panel plot + aggregate T*(A) plot |
| report/evidence/verification.txt | Machine-readable qualitative-check table |
