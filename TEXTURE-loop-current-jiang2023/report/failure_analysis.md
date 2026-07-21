# Failure analysis — jiang2023 (arXiv:2311.09290v2)

## What was reproduced (theorem-level, fully)
The S-matrix / bipartite crystalline lattice (BCL) flat-band counting theorem —
the paper's central analytic engine explaining kagome quasi-flat bands. All four
synthetic configs plus the s-orbital baseline and the intra-sublattice case
matched predictions to ~1e-14 bandwidth.

## What was NOT attempted (honest scope limits)
1. **DFT band fitting.** The paper fits realistic hopping parameters to ab initio
   bands (claimed 97% wavefunction overlap). We verified only the *idealized*
   flat-band limits, not the material-realistic fitted models. Requires DFT
   outputs / supplementary hopping tables not fetched in this fast pass.
2. **cRPA interactions & AFM ground state.** The interacting-Hamiltonian claim
   (A-type AFM in FeGe) was not tested — needs cRPA U/J and a many-body solver.
3. **1:3:5 (AV3Sb5) extension.** The loop-current-relevant family (where the
   corpus class label originates) was not built; only the general theorem that
   underlies it was verified.
4. **Loop-current physics.** Despite the corpus class ("loop-current"), this
   paper is a flat-band framework, NOT a spontaneous loop-current study. The
   shared loop-current mean-field probe is included only for provenance; its
   susceptibility output is not a paper claim.

## Class-label mismatch (non-fatal)
The corpus assigned class=loop-current, but arXiv:2311.09290 is a multi-orbital
kagome flat-band / bipartite-lattice paper. The replication honestly targets the
paper's actual computable headline rather than fabricating a loop-current result.

## Risk of over-claiming
Because the theorem is exact and the flat bands are pinned by chiral symmetry,
numerical reproduction is trivially clean — this is a *mechanism* verification,
not a materials-level validation. The verdict reflects theorem-level replication
only.
