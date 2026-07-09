# Brief — PDE-Herbert-2021-dielectric-continuum-qm

**Paper.** John M. Herbert. *Dielectric continuum methods for quantum chemistry.*
WIREs Comput Mol Sci **11**, e1519 (2021). DOI [10.1002/wcms.1519](https://doi.org/10.1002/wcms.1519).
Open-access preprint: [arXiv:2203.06846](https://arxiv.org/abs/2203.06846).

**What / why.** Independent numerical replication of Herbert's core Section 2.4 / Table 1
claim: that the apparent-surface-charge polarizable-continuum-model (ASC-PCM) family —
COSMO, C-PCM, IEF-PCM, SS(V)PE, SVPE — all give essentially identical electrostatic
solvation energies (~0.1 kcal/mol for neutrals, ~0.5 kcal/mol for ions) in a
high-dielectric solvent, while COSMO with `ζ=0` shows a well-known low-dielectric
pathology for ions. Reimplemented at RHF / 6-31G* with **PySCF 2.13.1** (open source,
free) on the same four small solutes (H2O, CH3CONH2, NO⁺, CN⁻) at ε_s = 78.3 (water)
and ε_s = 2.4 (toluene). Verdict: **PARTIAL (solid)** — the C2 (neutrals in water) and
C3 (toluene COSMO ion pathology) claims reproduce cleanly; the C2 ion-water bound is
narrowly missed (spreads 0.66–1.21 vs paper ~0.5 kcal/mol); absolute magnitudes differ
by ~1–9 kcal/mol due to the well-known cavity-definition difference (PySCF Bondi/vdW
vs Chipman/Herbert isodensity ρ₀=0.001 a.u.), which was flagged a priori as an unfair
test of C4.
