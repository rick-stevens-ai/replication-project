# Artifact Harvest — MC-VQE (Parrish et al. 2019)

Paper: R. M. Parrish, E. G. Hohenstein, P. L. McMahon, T. J. Martínez,
"Quantum Computation of Electronic Transitions using a Variational Quantum
Eigensolver", Phys. Rev. Lett. 122, 230401 (2019).
DOI: 10.1103/PhysRevLett.122.230401 · arXiv: 1901.01234

## Public artifacts pulled (all open-access)

| Artifact | Source URL | Size | Notes |
|---|---|---|---|
| arXiv abstract page | https://arxiv.org/abs/1901.01234 | ~30 KB HTML | title/authors/DOI verified |
| ar5iv full HTML | https://ar5iv.org/abs/1901.01234 | 1,401,277 B | full main text, equations |
| arXiv e-print source tarball | https://arxiv.org/e-print/1901.01234 | 782,755 B | gzip, contains tex + figures |
| main text tex | (from source) qem.tex | 48,717 B | Eqs 1-8, algorithm 4 stages |
| supplement tex | (from source) qem-supp.tex | 34,755 B | Ham element defs, CIS circuit, SO(4) entangler, comp details |
| figures | abs.pdf, circuit.pdf, stack2.pdf | — | not needed for numerics |

## Data availability note
The paper's *numerical* ab-initio exciton Hamiltonian for the N=18 LH2 B850 ring
(monomer ωPBE/6-31G* TeraChem outputs, XYZ geometry, .NPZ data packet) is
referenced as a "supplemental data packet" but is NOT contained in the arXiv
source tarball (only the tex + figure PDFs are). The exact monomer energies /
transition dipoles are therefore not in-corpus.

Consequence for replication: the *method* (MC-VQE algorithm, exciton-model
construction rules Eq.8 + supp element formulas, CIS state prep, SO(4) entangler,
state-averaged optimization, contracted-H diagonalization, oscillator-strength
formula) is fully specified and reproduced exactly. The *specific numbers*
(TeraChem monomer data) are reconstructed from a physically-faithful BChl-a
parametrization (Qy gap ~1.6 eV, transition dipole ~6 D, dipole/transition-dipole
two-body model per the supp) rather than the exact TeraChem outputs. The paper's
quantitative CLAIMS are about method accuracy (MC-VQE vs FCI vs CIS), which are
geometry-robust and are what we test.
