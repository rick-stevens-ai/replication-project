# FLUPS Replication

Replication of: **Caprace, Gillis, Chatelain — "FLUPS: A Fourier-Based Library of Unbounded Poisson Solvers"**, *SIAM Journal on Scientific Computing* 43(1):C31–C60 (2021). arXiv:[2006.09300](https://arxiv.org/abs/2006.09300). DOI: [10.1137/19M1303848](https://doi.org/10.1137/19M1303848).

Done by Ollie (subagent) for Rick, 2026-05-28, on CherryRd (macOS iMac, Intel x86_64, 12 cores).

## TL;DR

We built the open-source [FLUPS library](https://github.com/vortexlab-uclouvain/flups) from source on macOS, built and ran its `validation` sample, and **independently re-derived three of the paper's verified-convergence-order claims** on a unit-cube Poisson problem with a Gaussian source:

| Scenario | Paper claim | Our measured L2 fit | Verdict |
|---|---|---|---|
| Fully unbounded, **CHAT2** kernel | 2nd order | **1.93** | ✅ matches |
| Fully unbounded, **HEJ4** kernel | "spectral-like" / 4th order | **3.19** (asymptotically increasing — 48→96 gives 3.74) | ✅ qualitatively matches; pre-asymptotic |
| Fully periodic, CHAT2 kernel | spectral / round-off | **~3×10⁻¹⁶** (machine precision, all N) | ✅ exactly matches |

Plus an MPI sanity check: 2-rank parallel run reproduces the serial answer bitwise (1.187796827220e-04 at N=64).

## Layout

- `REPORT.md` — full claim-by-claim report, friction tags, limitations.
- `PROGRESS.md` — running log.
- `scripts/` — build helpers, convergence runner, analysis script, (failed) independent reference solver.
- `results/` — `unb_chat2/`, `unb_hej4/`, `per_chat2/` raw `N L2 Linf` data, plus `convergence.png` and `summary.json`.
- `logs/` — build + run logs.

## How to reproduce on a fresh macOS box

```sh
brew install open-mpi fftw hdf5 gcc

# h3lpr (helper lib)
git clone https://github.com/vanreeslab/h3lpr.git
cd h3lpr
OMPI_CXX=g++-15 OMPI_CC=gcc-15 CXX=mpic++ CC=mpicc \
    PREFIX=/tmp/install/h3lpr ARCH_FILE=make_arch/make.default make install -j4
cd ..

# flups
git clone https://github.com/vortexlab-uclouvain/flups.git
cd flups
cp ../<this-repo>/scripts/make.cherryrd make_arch/    # or write your own
OMPI_CXX=g++-15 OMPI_CC=gcc-15 ARCH_FILE=make_arch/make.cherryrd \
    PREFIX=/tmp/install/flups make install -j4

cd samples/validation
OMPI_CXX=g++-15 OMPI_CC=gcc-15 ARCH_FILE=make_arch/make.cherryrd \
    FLUPS_INC=/tmp/install/flups/include FLUPS_LIB=/tmp/install/flups/lib \
    H3LPR_INC=/tmp/install/h3lpr/include H3LPR_LIB=/tmp/install/h3lpr/lib \
    FFTW_INC=$(brew --prefix fftw)/include  FFTW_LIB=$(brew --prefix fftw)/lib \
    HDF5_INC=$(brew --prefix hdf5)/include  HDF5_LIB=$(brew --prefix hdf5)/lib \
    make -j4

# the .so install name needs a small patch on macOS:
install_name_tool -id /tmp/install/h3lpr/lib/libh3lpr.so /tmp/install/h3lpr/lib/libh3lpr.so
for b in flups_validation_a2a flups_validation_nb flups_validation_isr; do
  install_name_tool -change h3lpr.so /tmp/install/h3lpr/lib/libh3lpr.so $b
done

# run a sweep
bash <this-repo>/scripts/run_convergence.sh
python3 <this-repo>/scripts/analyze.py
```
