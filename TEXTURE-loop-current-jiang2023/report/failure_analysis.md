# Failure analysis — arXiv:2311.09290

## 1. Class misclassification (the biggest "failure")
This paper was filed under the **loop-current** class of TEXTURES-100, and the
supplied reusable kernel (`loop_current_kagome_kernel.py`) targets kagome
Peierls-flux / loop-current physics (staggered flux, TRS breaking, Chern/AHE).
**The paper contains none of that.** It is a d-orbital tight-binding +
S-matrix flat-band-engineering paper for FeGe-class kagome *materials*.

- **Impact:** the kernel's flux/Chern/current-operator machinery is not
  applicable and was NOT exercised (doing so would have produced meaningless
  "results" for a paper that makes no such claims — a fabrication risk we
  avoided).
- **What we reused instead:** the shared kagome TB substrate — the flux=0 limit
  of `KagomeModel`, plus `.bands`/`.dos`. That substrate IS the paper's building
  block (the NN kagome Hamiltonian), so the reuse is physically honest and
  provenance is preserved by importing the kernel directly.
- **Recommendation for the set curator:** relabel this entry as a
  *flat-band / bipartite-lattice* paper, not loop-current.

## 2. Out-of-scope items (marked, not faked)
The paper's second half rests on external DFT / cRPA / Wannier inputs that an
independent-code replication cannot regenerate without the authors' pipeline:
- Fitted per-orbital hopping tables (Appendix II) — DFT-band fits.
- DFT–TB wavefunction overlaps (97%, 85%) — need DFT eigenvectors.
- cRPA interaction matrix (Table I), hidden O_h symmetry — need cRPA.
- Hartree–Fock AFM magnetic moments (§VI) — need the full interacting solve
  with the cRPA inputs.
- 1:6:6 (MgFe6Ge6) and 1:3:5 (CsV3Sb5 etc.) extensions — need DFT for each.

These are explicitly excluded from the Coverage score rather than approximated
with invented numbers.

## 3. Code bugs hit and fixed (during this run)
- **Shape mismatch in `bcl_flat_count`:** NL/NLt were swapped relative to the S
  block orientation → broadcast error. Fixed by defining NL as the LARGER
  sublattice (rows of S). No effect on physics; caught immediately.
- **C4 selected the wrong band:** in the +2t·HKagome convention the flat band is
  the LOWEST band, but the code initially took the top band (dispersive) → the
  "NN-only flat" check failed (width 1.47 instead of 0). Fixed by selecting the
  minimum-bandwidth band. After the fix, NN-only width = 2.6e-15 (exactly flat),
  matching the theory.

## 4. Residual limitations / caveats
- **Rank(S) BZ-constancy:** the numeric rank of the reconstructed S-matrix drops
  at isolated mesh points; the BCL theorem uses the generic (BZ-maximal) rank,
  which is what we report. Rank drops at symmetry points could in principle add
  fragile touchings (see open_questions.json #3) — not investigated further.
- **S-matrix reconstruction:** we rebuilt `S_{ptxy,d1}(k)` from Eq. S2.18 with a
  single leading amplitude; the flat-band COUNT is amplitude-independent (verified
  with a randomized-amplitude control), so this is sufficient for C2/C3. We did
  NOT reproduce the fine dispersion of the fitted realistic model (that needs the
  DFT hopping tables — out of scope).
- **Energy conventions:** the kernel uses t=1, energy zero at the M-saddle; the
  paper uses eV with DFT-referenced E_F. C1/C2/C3/C5 are convention-independent
  (degeneracies, counts, relative peak positions); C4 uses the paper's fitted
  t^NN_d1 = 0.49 eV directly.

## 5. No fabrication
Every reported number comes from a real run of `code/verify_jiang2023.py`
(reproducible in <30 s). Out-of-scope quantities are labeled, not estimated.
