# PROVENANCE — TEXTURE-loop-current-xu2023

**Target paper:** arXiv:2306.16192v1 (Xu, Capponi, Chen, Vanderstraeten, Hasik,
Nevidomskyy, Mambrini, Penc, Poilblanc), *Phase diagram of the chiral SU(3)
antiferromagnet on the kagome lattice.*

## Kernel reuse
Adapted from the shared reusable kernel
`~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
(originally built for Fernandes–Birol–Ye–Vanderbilt, arXiv:2502.16657 — the first
loop-current paper in the REPLICATE-PROJECT set).

### What was reused
- Kagome geometry conventions: 3 sublattices, primitive vectors
  `a1=(1,0), a2=(1/2,√3/2)`, `_reciprocal()` for hexagonal BZ vectors `B1,B2`,
  and the `bz_grid(nk)` fractional-coordinate BZ sampler.
- The batched **`eigvalsh` over a stack of Bloch matrices on a BZ grid** pattern
  (`all_eigvals` → here `all_magnon_eigs`).
- The core conceptual mapping: **imaginary NN hopping = broken time-reversal**
  (the kernel's Peierls `flux`; here the chiral `±iK_I`).

### What was specialised / rewritten for THIS paper
- The 3×3 Bloch matrix is **NOT** the kernel's tight-binding kagome hopping. It is
  the paper's **single-magnon** matrix Eq. (A1): diagonal `−4(J+K_R)`, off-diagonal
  `2(J+K_R ∓ iK_I)cos(·)` with the three kagome bond directions
  `(qx∓√3 qy)/2` and `qx`. Implemented in `code/magnon_su3_kagome.py:magnon_matrix`.
- The kernel's Chern/Kubo/Berry routines were **deliberately not used**: the paper's
  topological (TSL/CSL) claims are many-body ED/tensor-network results, out of scope
  for a single-node overnight run (see `extraction/marker.md`).

## Files
- `code/magnon_su3_kagome.py` — Eq. A1 matrix, BZ utilities, analytic formulas.
- `code/run_checks.py` — the 5 quantitative claim checks → `work/results.json`.
- `code/plot_bands.py` — magnon band plots + chiral hexagon-mode phase probe.
- `work/` — outputs (results.json, run_log.txt, magnon_bands.png).
- `report/` — 8-artifact deliverables.

## Environment
Python 3 (system), numpy 2.4.3, scipy 1.18.0, matplotlib (Agg). pdflatex available.
Host: CherryRd. No external endpoints used (pure local computation).
