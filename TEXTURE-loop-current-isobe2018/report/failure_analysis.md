# Failure analysis

## Scope mismatch (primary, honestly flagged)
The TEXTURES-100 shared kernel `loop_current_kagome_kernel.py` targets kagome
tight-binding + Peierls-flux loop-current physics (Fernandes et al 2025). This
paper (Isobe-Yuan-Fu 2018) is a hot-spot **patch RG** model for twisted bilayer
graphene: no lattice Hamiltonian, no flux, no Chern number. The kernel's core
machinery (KagomeModel, chern_number, bond_current_and_charge,
triangle_flux_from_config) is therefore inapplicable and was NOT used. This is a
class mismatch, not a code defect. In-scope core (RG flow + susceptibilities)
was reimplemented from the paper's equations instead.

## Test-construction bug found and fixed during the run
Claim 5 initially failed because the first draft set g11=g31=g41 (all equal) as
the "finite exchange" case. Algebraically d-SC - p-SC = 4(g41 - g31), so equal
g31=g41 leaves d/p degenerate — the test was wrong, not the physics. Fixed to use
distinct exchange values (g31 != g41, g11 != 0), after which the degeneracy lift
appears (d/p split 0.8, CDW/SDW split 1.2) exactly as Eqs. (17)-(19) predict.
Lesson: derive the algebraic lifting condition before choosing test inputs.

## Known limitations / not attempted (honest negatives)
- Full 2D phase-boundary curves of Fig. 4(a),(b) were not digitized/overlaid;
  we verified the SC->DW ordering and Q- dominance, not the exact boundary shape
  (see open_questions #1).
- d_as held constant within the nested window (as the paper's main analysis
  does); the y-dependent da+(y) and Appendix-F generalized RG not implemented.
- Sec V CDW- mean-field band reconstruction / n=2 gap (Delta_c) not built — needs
  the explicit nested dispersion beyond the patch-RG core (open_questions #4).
- Perturbative RG integration is stopped at |g|=50 (strong-coupling breakdown);
  robustness to this cutoff quantified only qualitatively (open_questions #5).

## No fabrication
All numbers in results.json are produced by running the code. Where a target was
out of scope or not attempted, it is marked as such rather than faked.
