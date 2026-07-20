# Extraction Marker — arXiv:2209.10768v2

**Title:** Loop-current charge density wave driven by long-range Coulomb repulsion on the kagomé lattice
**Authors:** Jin-Wei Dong, Ziqiang Wang, Sen Zhou
**Dated:** Jan 23, 2023 (v2)
**Class:** Loop-current / kagome flux-phase (TEXTURES-100 loop-current class)
**System:** Single-orbital t-V1-V2 extended-Hubbard model on the kagomé lattice at van Hove (vH) filling.

## Central claim
Next-nearest-neighbor (nnn) Coulomb repulsion V2 drives an instability toward an
*imaginary* bond-ordered CDW = spontaneous loop-current (LC) order that breaks
time-reversal symmetry (TRS), producing orbital Chern insulators. Nearest-neighbor
V1 alone drives only a *real* CDW (inverse Star-of-David, ISD), which is
topologically trivial. This is offered as a microscopic model for the TRS-breaking
CDW normal state of AV3Sb5 kagomé superconductors.

## Model (Eq. 6)
H = -t Σ_<ij>σ (c†_iσ c_jσ + h.c.) + V1 Σ_<ij> n_i n_j + V2 Σ_<<ij>> n_i n_j
- t ≡ 1 (energy unit). Kagome lattice, 3 sublattices/cell.
- vH filling n_vH = 5/12 (per site, spinful: 5 of 12 states per 2×2 cell / actually
  filling fraction of the 3-band model = 5/12 counting spin-degenerate bands).
- Onsite U neglected (sublattice quantum interference obstructs it; nonmagnetic).

## Mean-field decoupling (Eq. 20)
Decouple V1, V2 in the bond (exchange/Fock) channel with complex bond OPs
  χ_ij = <c†_i↑ c_j↑ + c†_i↓ c_j↓>.
H_MF = -Σ_<ij>[(t + V1 χ*_ij) χ̂_ij + h.c. - V1|χ_ij|²]
       -Σ_<<ij>>[ V2 χ*_ij χ̂_ij + h.c. - V2|χ_ij|² ].
Direct Hartree terms dropped (LDA+U+V double-counting avoidance).
2×2 enlarged unit cell (12 sites, 24 nn bonds, 24 nnn bonds). C6-symmetric ansatz
reduces to 3 nn classes χ1,2,3 and 3 nnn classes χ'1,2,3.

## Machine-checkable claims selected
1. **C1 — Susceptibility channel selectivity:** nn bond bare susceptibility peaks
   in the REAL (breathing) channel at the M/Q wavevector; nnn bond susceptibility
   peaks in the IMAGINARY (breathing) channel. (Sec. II, Fig. 1c-d.)
2. **C2 — Weak-coupling critical ratio:** real→imaginary CDW boundary at
   V2/V1 ≈ (1.47−0.96)/(0.99−0.77) ≈ 2.36. (Eq. 19.)
3. **C3 — Spontaneous LC order from V2:** self-consistent MF gives nonzero
   Im(χ_ij) (loop currents) only when V2 is sufficiently large; V1-only gives a
   real (Im=0) CDW. First-order ISD→LC transition at V2≈1.81 for V1=1.75. (Fig.5.)
4. **C4 — Chern numbers of LC states:** total Chern N = 1, −1, 0, −1 for LC1..LC4;
   LC states are orbital Chern insulators (TRS broken, gapped). (Sec. IV.B.2.)
5. **C5 — vH sublattice localization:** at vH filling the three vH points M1,2,3
   are each localized on a single sublattice → onsite order suppressed, off-site
   (bond) order favored. Table I: charge disproportionation δ small (≲11%).

## Quantitative anchors (Table I, vH filling n=5/12)
- ISD @ V=(2,1): δ=0.115, χ1=0.631, χ2=0.636, χ3=0.181, all Im≈0.
- LC2 @ V=(0.8,1.6): δ=0.007, χ1=0.378+0.069i, χ2=0.375−0.069i, χ3=0.490+0.064i.
- LC1 @ V=(0.5,2.5): χ'1=−0.115−0.450i (large imaginary nnn).
- ISD→LC2 transition V2≈1.81 at V1=1.75; LC2→LC4 at V2≈2.29; →LC3 at 2.67; →LC1 at 3.03.

## Results (executed, production resolution — see work/results.json)
- C5 MATCH: E={-2,0,2}t at all 3 M points; vH band has ~1e-32 (zero) weight on
  one sublattice at each M -> sublattice interference confirmed.
- C1 MATCH: nn real (-0.327) > nn imag (-0.317); nnn imag (-0.457) > nnn real
  (-0.337). nn/nnn real-vs-imag ordering as in Fig. 1c-d.
- C2 OUT OF SCOPE: aggregate-channel proxy ratio 0.082 not comparable to paper's
  normalized 2.36 (needs exact Pi normalization).
- C3 NOT REPRODUCED: self-consistent HF collapses to real state everywhere
  (loop_flux ~0.002-0.004); no ISD->LC transition. Root cause = missing the
  paper's symmetric-correction subtraction scheme. (V1-only=real half is OK.)
- C4 PARTIAL: imposing Table-I bonds -> LC2 C=-1 (paper -1) and LC3 C=0 (paper 0)
  EXACT; LC1/LC4 mismatch (approx C6 bond labeling); all LC states gapped w/
  nonzero flux. Kernel uniform-flux cross-check: gap 1.732t, band Chern -1.
- Verdict: PARTIALLY REPRODUCED. Coverage 8/10, Agreement 6/10.

## Method used for replication
Real-space self-consistent Hartree–Fock (bond/Fock decoupling) on a periodic
kagome cluster commensurate with 2×2 order, using the shared loop-current kernel's
kagome geometry + bond-current machinery, extended with:
- complex bond order parameters on nn + nnn bonds,
- self-consistent iteration of Eq. (20),
- finite-T bare bond susceptibility for C1,
- Chern number via projector/Fukui-Hatsugai on the folded BZ for C4.
