# Workflow — li2019 magnon spin Nernst replication (RETRY)

## Goal
Independently reproduce, from the paper text alone, the intrinsic magnon spin
Nernst conductivity of the kagome antiferromagnet KFe3(OH)6(SO4)2 (Li,
Sandhoefner & Kovalev, arXiv:1907.10567v3), and package an 8-artifact bundle.

## Context: this was a RETRY
The prior attempt **timed out at 1200 s** and produced physically garbage
numbers (Chern ~10^5, alpha ~10^4). Root cause: a broken Colpa diagonalization
(wrong eigenvalue/T assembly) plus wrong Berry-curvature matrix elements. This
run rebuilt the numerics correctly and kept the grid coarse and time-bounded
(full run now ~8 s).

## Steps executed
1. **Read** paper text (`work/textures-spin-li2019.txt`), recipe
   (`report/evidence/replication_recipe.json`), and the shared gobel2024 Kubo
   kernel for the machinery pattern.
2. **Extracted** exact parameters and targets from the paper:
   J1=3.18, J2=0.11 meV, |Dp|/J1=0.062, Dz/J1=-0.062, S=5/2; targets
   eta=1.9 deg, Chern (-3,1,2), alpha^y_yx/kB ~3.5, alpha^z_yx two orders smaller.
3. **Rebuilt** `work/li2019_kernel.py` from scratch:
   - kagome geometry + NN/NNN bond enumeration; radial in-plane DMI + chirality-
     staggered Dz.
   - classical noncollinear q=0 order with canting eta; local HP frames u_i.
   - 6x6 bosonic BdG H(k) = [[A(k),B(k)],[B^dag,A^T(-k)]] with analytic k-derivatives.
   - **Colpa paraunitary diagonalization** via Cholesky + Hermitian eig of
     K sigma3 K^dag (robust to degeneracy; paraunitary residual ~1e-13).
   - generalized (spin) Berry curvature (Eq. 9) + spin Nernst c1 formula (Eq. 15).
4. **Debugged** iteratively (see `failure_analysis.md`):
   - direct non-Hermitian eig of sigma3 H -> failed on degeneracies (paraerr 1e12) -> switched to Colpa.
   - fixed A/B block u-vector conjugation convention.
   - added Lorentzian denominator + IR energy floor to tame the AFM Goldstone at Gamma.
5. **SAVE-EARLY**: `work/li2019_result.json` written after each grid (nk=24 headline).
6. **Compared** to paper targets and scored honestly.
7. **Packaged** 8 artifacts (extraction x2, report x5, evidence copies).

## Tools / environment
- Physics runner: `/home/stevens/comfyui-env/bin/python` (numpy only, vectorized).
- Extraction: poppler `pdftotext` (marker/nougat binaries unavailable -> interim + hand-typeset equations).
- Runtime: ~8 s for the full 3-grid sweep (was >1200 s timeout before).

## Result headline (nk=24)
eta=1.91 deg (exact), band width ~3.4 J1S, alpha^y_yx/kB peak = 2.70,
alpha^z_yx/alpha^y_yx ~ 6.5e-3. Verdict PARTIAL.
