# Workflow — jia2026 NOME reproduction

**Paper:** Jia, Qiao, Wang, *Geometry-Driven Nonlinear Orbital Magnetoelectric Effect*, arXiv:2605.17462
**Verdict:** PARTIAL

## Pipeline

1. **Extraction.** PDF → `extraction/marker.md` (marker/pdftotext; heavy tensor
   equations legible, sub/superscripts mangled but structurally intact). Nougat
   fallback stub at `extraction/nougat.mmd`.
2. **Method extraction.** Distilled claims C1–C6, the two model Hamiltonians
   (Eq. 11 Kane–Mele, Eq. 12 CuMnAs), parameters, and the response-formula recipe
   (Eqs. 3–9) → `report/method_extract.md`.
3. **Implementation.** From-scratch `numpy` tight-binding code of Model 1
   (modified Kane–Mele, Eq. 11) → `work/reproduce.py`. Builds the 4-band Bloch
   Hamiltonian; computes per-k eigenenergies, velocity matrices (central finite
   difference in k), interband Berry connection, orbital-moment matrix L^z,
   quantum metric, and spin matrix S^z; evaluates the conventional "od" intrinsic
   NOME term chi^{(0,od)}_{z;xx} and its spin analogue as BZ integrals.
4. **Sweeps.** Band structure along K′–Γ–M–K–Γ (Fig 1a); chi vs μ (Fig 1b);
   chi vs λ_R at μ=50 meV (Fig 1c). Outputs → `work/results.json`,
   `work/figs/*.png`.
5. **Analysis & write-up.** Compared reproduced vs paper values, checked the
   λ_R-even symmetry, orbital/spin sign+ratio → this report set.

## Tools & environment

- **Language/libraries:** Python 3, `numpy` (linear algebra, BZ mesh sums,
  finite-difference k-derivatives), `matplotlib` (figures). No specialized
  physics packages; no DFT.
- **Model:** 4-band Bloch Hamiltonian (2 sublattice × 2 spin), dense
  `120×120` Brillouin-zone mesh, Fermi–Dirac occupation at T=20 K.
- **Parameters (Eq. 11 / Fig 1):** t=0.85 eV, λ_R=20 meV, λ=10 meV,
  λ_so=10 meV, T=20 K; μ swept; λ_R swept at μ=50 meV.

## Effort

- **Host:** CherryRd (CPU only; no GPU needed).
- **Compute time:** ~4 min for the full `reproduce.py` run (120×120 mesh +
  μ and λ_R sweeps + figures).
- **Scope:** Model 1 intrinsic "od" term only. The geometric/Hermitian-connection
  sector (Eqs. 4–9), Model 2 (CuMnAs), and the MPG enumeration (C3) were not
  implemented in this pass (see `failure_analysis.md`).
