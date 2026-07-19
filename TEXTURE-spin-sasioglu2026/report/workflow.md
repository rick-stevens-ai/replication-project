# Workflow — Şaşıoğlu et al. 2026 (arXiv:2606.08757) TB replication

## Goal
Reproduce the tight-binding core: the nanotube altermagnetic spin splitting follows a
`cos(2θ)` chiral-angle law (nodal-vanishing, antinodal-maximal), derived by zone-folding a
2D d-wave altermagnet.

## Steps executed
1. **Read** `report/method_extract.md` (pre-extracted physics; did NOT re-derive).
2. **Wrote** `code/sasioglu2026_replication.py`:
   - Analytic d-wave altermagnet dispersion `E_σ(k)= -2t(cos kx+cos ky) - 2σ t_AM(cos kx-cos ky)`.
   - Spin splitting `Δ(k) = -4 t_AM (cos kx - cos ky)` (d_{x²-y²}).
   - Explicit 4×4 sublattice⊗spin Bloch Hamiltonian as a rigor cross-check.
   - Bulk checks: net magnetization, diagonal node, antinodal amplitude, analytic-vs-Bloch.
   - Zone folding: circumferential quantization `k_c = 2π m/N` at chiral angle θ, continuous
     axial `k_a`; axial-resolved spin-splitting curvature as the tube observable.
   - θ sweep 0→90° for tube indices N=8,12,16; least-squares fit to `A cos(2θ)+B`.
3. **Ran** it (CPU, ~1.2 s). Saved `work/results.json` (per-claim expectation/reproduced/match/note)
   and two figures in `figs/`.
4. **Fixed two issues** found on first run:
   - Bloch consistency check averaged both sublattices → cancelled splitting; corrected to a
     sublattice-resolved comparison (now exact match, diff = 0).
   - Original RMS-over-folded-BZ observable was rotation-invariant (isotropic) → replaced with
     the physically meaningful axial-projected splitting, which correctly folds as cos(2θ).
5. **Built 8 artifacts** (report .tex/.pdf, open_questions, workflow, artifacts_summary,
   failure_analysis, updated META.json).

## Parameters
- `t = 1.0` (energy unit), `t_AM = 0.30` (altermagnetic anisotropic hopping).
- BZ grid 401×401; θ grid 0–90° in 1° steps; axial fit window k_a∈[-0.4,0.4], 201 pts.

## Reproduce
```
cd TEXTURE-spin-sasioglu2026
python3 code/sasioglu2026_replication.py
# -> work/results.json, figs/fig1_*.png, figs/fig2_*.png
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

## Dependencies
numpy, scipy (eigvalsh only via numpy.linalg), matplotlib. CPU-only, no network, no paid APIs.
