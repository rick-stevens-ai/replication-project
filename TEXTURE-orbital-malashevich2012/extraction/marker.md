# Extraction — marker.md

**Paper:** Full magnetoelectric response of Cr₂O₃ from first principles
**Authors:** A. Malashevich, S. Coh, I. Souza, D. Vanderbilt
**Ref:** Phys. Rev. B **86**, 094430 (2012) — arXiv:1207.5873v2
**Method:** First-principles DFT (Quantum ESPRESSO), SOC LSDA+U, finite electric field

> Extraction note: this is a `pdftotext -layout` interim extraction (a Marker/Nougat
> GPU pipeline was not run in this fast pass). The verbatim table values below were
> transcribed by hand from the layout dump; full raw text is in `nougat.mmd`.

## Headline
Transverse linear ME response of Cr₂O₃ at T=0:
**|α⊥| = 1.04 ps/m**, in good agreement with experiment (0.7–1.6 ps/m).

## Table II — contributions to α⊥ (ps/m)
| channel   | Spin | Orb.   | Total |
|-----------|------|--------|-------|
| Electronic| 0.26 | −0.014 | 0.25  |
| Lattice   | 0.77 |  0.025 | 0.80  |
| **Total** | 1.03 |  0.011 | **1.04** |

- Spin-lattice ≈ 75% of α⊥; spin-electronic ≈ 25%; orbital < 2%.
- Longitudinal α∥: spin negligible (0.003), orbital nearly cancels → total ≈ 0.002 ps/m
  (vs. experimental 0.2–0.3 ps/m — unaccounted, thermal fluctuations implicated).

## Table III — orbital ME decomposition of α⊥ᵒʳᵇ (ps/m)
Electronic: Local circ. −0.0064, Itinerant circ. −0.0084, Chern-Simons +0.0012, subtotal −0.0136.
Lattice: LC −0.0237, IC +0.0135, subtotal −0.0090.

## Key methodological anchor
Chern-Simons (axion) orbital-electronic ME quantum:
**α_CS = (θ/π)·(e²/2h)·μ₀**, with quantum (e²/2h)·μ₀ = **24.3 ps/m** (paper, intro).

## Key parameters (recipe)
LSDA, Hubbard U=2.0 eV, Hund J=0.8 eV, SOC on for magnetization, fully-relativistic
NCPP, 150 Ry cutoff, 4×4×4 MP mesh, a=5.35 Å c=13.76 Å, u=0.1536, E≈1e9 V/m, collinear AFM.
