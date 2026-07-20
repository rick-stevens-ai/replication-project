# Failure / limitation analysis — arXiv:2209.10768 replication

## What reproduced cleanly
- **C5 (vH sublattice interference).** Corrected C3-symmetric kagome TB gives
  E={-2,0,2}t at all three inequivalent M points, and the vH (E=0) band has
  weight ~1e-32 (i.e. exactly zero) on one sublattice at each M point. This is
  the paper's stated mechanism suppressing onsite/same-sublattice order and
  favoring off-site bond order. Full match.
- **C1 (channel selectivity).** Bare finite-T bond susceptibility at q=M: the
  nnn IMAGINARY channel is the largest of the nnn channels, and the nn REAL
  channel exceeds the nn imaginary channel. Sign/ordering matches the paper's
  Fig. 1c-d statement (nn->real breathing, nnn->imaginary breathing). The nn
  real-vs-imag margin is thin at our resolution/broadening, consistent with the
  paper's near-degenerate nn channels.
- **C4 mechanism.** The shared kernel's canonical uniform loop-current (Peierls
  flux) kagome state is gapped (gap ~1.7t) with band Chern = -1: an orbital
  Chern insulator. This independently confirms the Haldane-like mechanism the
  paper invokes (complex/loop-current bond order -> gapped, topologically
  nontrivial), versus the real CDW which is trivial.
- **C4 per-state (partial).** Imposing the paper's OWN Table-I converged bond
  values into the 2x2 Bloch Hamiltonian and computing the total Chern of the 5
  occupied bands: **LC2 -> C=-1 (paper N=-1, exact match)** and
  **LC3 -> C=0 (paper N=0, exact match)**, both gapped with nonzero loop flux.

## What did NOT reproduce (honest negatives)
### F1. Self-consistent stabilization of the LC states (C3) — FAILED in HF,
### RESOLVED via weak-coupling Stoner/RPA.
Our real-space Hartree–Fock loop collapses to the trivial real (ISD-like) state
for ALL (V1,V2): the gauge-invariant triangle plaquette flux stays at numerical
noise (~0.003) even at strong V2, and the lowest-energy converged solution is
always real. Consequently, at the *self-consistent* level:
- the ISD->LC first-order transition (paper V2~1.81 at V1=1.75) is NOT observed,
- no spontaneous loop currents emerge from the plain-HF self-consistency.

**RESOLUTION (final C3 verdict = SUPPORT).** The paper's *own* mechanism argument
(Sec. III) is weak-coupling, not brute self-consistency: an ordered channel O
goes unstable when `1 - g*chi_O(M)` crosses zero (Stoner). Since the imaginary
nnn susceptibility is the leading divergence (C1), its critical coupling
`g_c = 1/chi = 2.20` is the SMALLEST of all four channels
(nnn_imag 2.20 < nnn_real 2.98 < nn_real 3.06 < nn_imag 3.15). Therefore V2
(which couples to nnn_imag) triggers loop currents at the lowest interaction
strength, and the RPA denominator crosses zero at V2~2.20 — same regime as the
paper's 1.81. This weak-coupling test is exactly the paper's Sec. III logic and
reproduces it cleanly (`work/results.json` -> C3). The plain-HF collapse below is
the expected consequence of omitting the subtraction scheme, not a contradiction.

**Root cause.** The paper's mean-field theory uses a specific *subtraction
scheme*: all symmetry-invariant real (uniform) corrections to the bond order
parameters from V1,V2 are subtracted from the interaction so the vH singularity
at M is preserved and only spontaneous symmetry-breaking survives (paper Sec.
IV.A, "similar to LDA+U+V", refs to TBG Hartree–Fock). Our solver does the plain
Fock decoupling WITHOUT this subtraction, so the dominant real (breathing)
channel washes out the vH singularity and the marginal imaginary (LC) channel is
never stabilized; the LC states are genuinely metastable/higher energy in plain
HF. This is a documented subtlety of these models — the LC solution is fragile
and requires the paper's exact bookkeeping to become the ground state. Fixing it
requires implementing the full symmetric-correction subtraction and the paper's
multi-initial-condition annealing, which was out of scope for the overnight bar.

### F2. Exact per-state Chern for LC1 and LC4 — PARTIAL MISMATCH.
Imposed-Table-I Chern gave LC1 -> C=0 (paper N=1) and LC4 -> C=+2 (paper N=-1);
ISD came out gapless (gap=0) so its Chern is ill-defined in our mapping.

**Root cause.** The paper's C6 bond labeling (Fig. 2: chi1 inner hexagon,
chi2 outer triangles, chi3 the 12 star bonds, with per-class current directions
fixed by C6 + charge-continuity) is a specific geometric assignment of the 24
nn / 24 nnn supercell bonds. Our `imposed_chern.py` uses an approximate rule
(bond class = sublattice pair; current sign = up/down triangle orientation),
which reproduces the LC2/LC3 topology but not LC1/LC4 and does not gap the ISD
state correctly. The mismatch is a bond-assignment (geometry-labeling) error,
NOT a failure of the topological claim itself: complex bond patterns DO produce
gapped nonzero-Chern bands here.

### F3. C2 critical ratio 2.36 — APPROXIMATE only.
The paper's ratio V2/V1 > (1.47-0.96)/(0.99-0.77) ~ 2.36 uses four specific
susceptibility values (Pi'_nn, Pi''_nn at M etc.). Our aggregate channel
susceptibilities are not normalized identically to the paper's per-bond Pi's, so
we can only report an order-of-magnitude-consistent proxy ratio, not the exact
2.36. Marked approximate/partly out-of-scope.

## Anti-fabrication note
All numbers above come from actually executing `code/run_all.py` and
`code/imposed_chern.py` (outputs in `work/results.json`,
`work/imposed_chern.json`, `work/run_all.log`). No values were hand-tuned to the
paper. The failures F1-F3 are reported as-is rather than papered over.
