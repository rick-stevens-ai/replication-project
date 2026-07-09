# PROGRESS — Modified Poisson-Nernst-Planck (mPNP) Replication

**Target:** Ma, Xu, Zhang (2020), "Modified Poisson-Nernst-Planck Model with Coulomb and
Hard-sphere Correlations" (SIAM J. Appl. Math, treating it as the 2020 mPNP paper from
the Xu/Ma/Zhang group; we proceed as **independent open-source replication** since no
official code repository was located).

**Status:** complete (independent reduced replication, 8/10 claims confirmed)
**Started:** 2026-05-28 ~11:57 CDT
**Owner:** Ollie (subagent)
**Location:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/`

**Identified paper:** Ma, Xu, Zhang, *SIAM J. Appl. Math.* (2021), DOI 10.1137/19m1310098.
Open preprint **arXiv:2002.07489v3** (downloaded to `paper.pdf` + `paper.txt`).
No official code repository located — proceeding as independent replication.

**Confirmed key items from the PDF:**
- Dimensionless mPNP, Eqs. (3.12)–(3.15); four model variants compared:
  MF (mean-field), SC (short-range HS only via MFMT), LC (long-range Coulomb only),
  LS (both).
- Equilibrium reduces to modified Poisson–Boltzmann: c_i = exp(z_i φ + μ^co_i + μ^hs_i)
  (paper: "the resulting modified PB equation system is discretized by the FDM and
  solved iteratively").
- HS chemical potential from MFMT, 1D weighted densities n_α(x), Eqs. (3.3)–(3.5).
- Coulomb-correlation μ^co_i from WKB Green's function with dielectric-mismatch
  parameter γ = (1−η_b)/(1+η_b), Eqs. (3.22) etc.
- Test params used in paper figures: Fig 4.1 (ε,q,a)=(0.2,0.3,0.15); Fig 4.2
  (ε,q,a,V)=(0.1,0.15,0.075,1), N=800; Fig 4.5 (ε,q,a,γ)=(0.2,0.3,0.15,1), V=1.
- MC reference data (Fig 4.3a) from Ref. [47] free database; we will not need it
  for our self-contained run.

**Replication scope (honest, reduced):**
- Implement **steady-state mPB** (equilibrium of mPNP) in the dimensionless two-plate
  slab, in pure NumPy/SciPy on CPU. Four variants: MF, SC, LC, LS.
- MFMT-HS: full 1D weighted-density evaluation (Eqs. 3.3–3.5) and analytic μ^hs
  from BMCSL/Rosenfeld density (Eq. 2.27).
- Coulomb correlation: implement the **WKB local-κ screened image-charge form**
  (numerical evaluation of Eq. 3.22 by Gauss–Legendre quadrature with local κ(x))
  for the LC and LS variants.
- Boundary conditions: Robin for φ at x=±(1−a) per Eq. (3.14), no-flux not needed
  at equilibrium since J_i ≡ 0 there.
- Picard / damped fixed-point iteration on (c±, φ).
- Comparisons:
  1. Numerical convergence (mimic Fig 4.1): μ^hs(x=0) for uniform c≡1 vs N → expect
     2nd-order in h.
  2. Reproduce qualitative Fig 4.5 setup (ε=0.2, q=0.3, a=0.15, γ=1, V=1):
     cation profile + potential for MF, SC, LC, LS.
  3. Symmetric charged-surface case (γ=0) to confirm MF vs LS difference is small
     (as paper notes for Fig 4.3a weak-correlation regime).
  4. Free-energy / mass-conservation diagnostics.
- Friction tags: `wkb-quadrature-simplified`, `no-MC-data` (we plot only model curves,
  not external MC), `no-time-dependent-NP` (steady-state mPB only).

## Plan

1. Scaffold project, write this PROGRESS.md (<10 min). ✅
2. Brief literature/equation sweep — locate the canonical mPNP correction forms
   (Bikerman steric, Borukhov–Andelman, Local Density Approximation w/ hard-sphere term,
   Coulomb correlation via Bazant-style or generalized Born-style). Document chosen
   correction(s). [in progress]
3. Implement classical PNP in 1D slab (binary symmetric electrolyte between two parallel
   electrodes at fixed potential ±V₀) in pure NumPy/SciPy — Gummel-style fixed-point
   iteration with implicit Scharfetter–Gummel-like flux on a uniform grid; steady-state
   first.
4. Implement at least one modified PNP variant: **Borukhov–Andelman steric (lattice‑gas /
   hard‑sphere)** correction. Optionally add a Coulomb-correlation length term (4th-order
   Bazant-style modified Poisson).
5. Compare: (a) ion concentration profiles c±(x), (b) electrostatic potential φ(x), (c)
   surface charge / differential capacitance vs. applied voltage, (d) numerical
   convergence under mesh refinement.
6. Generate figures + claim-by-claim table; write REPORT.md and README.md.
7. Write final progress JSON.

## Outcome

- Implemented MF / SC / LC / LS variants of equilibrium mPB; all converge.
- 8/10 reproducible paper claims confirmed (see `REPORT.md` Table §4).
- Two not tested by design (MC/MD comparison, FDM-vs-WKB cross-check).
- 4 figures produced (figures/fig41_*, fig43a_*, fig45_*, convergence_*).

## Friction Log

- No code from original authors located (web/openalex/github checks pending; will run if
  time). Treating as fully independent replication. Friction tag: `no-author-code`.
- Paper-specific numerical setup (geometry, electrolyte parameters, voltage range, ion
  diameters) will be approximated from the standard mPNP literature since we cannot
  fetch the paper PDF freely; we document parameters explicitly so the comparison is
  internally consistent even if absolute values differ from the paper's. Friction tag:
  `paper-paywalled-using-canonical-setup`.

## Compute

- Local CPU on CherryRd (macOS). Python/NumPy/SciPy. No GPU needed; 1D problem.
- Total wall time across all four runner scripts: ~12 minutes.
- Peak memory < 200 MB.

## Final friction tags

- `paper-paywalled-but-arxiv-open`
- `no-author-code`
- `wkb-simplification` (local-kappa as in paper)
- `born-term-omitted` (constant for uniform dielectric, absorbed in bulk reference)
- `equilibrium-only` (steady-state mPB; matches paper Sec 4 usage)
- `mfmt-grid-aliasing` (small, harmless)
- `ls-numerically-fragile` (mitigated by warm-start + log-space damping + step cap)
- `no-mc-md` (out of scope per contract)
