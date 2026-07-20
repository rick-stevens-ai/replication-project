# Extraction marker — arXiv:2311.09290

**Paper:** Yi Jiang, Haoyu Hu, Dumitru Călugăru, Claudia Felser, Santiago
Blanco-Canosa, Hongming Weng, Yuanfeng Xu, B. Andrei Bernevig,
*"FeGe as a building block for the kagome 1:1, 1:6:6, and 1:3:5 families:
hidden d-orbital decoupling of flat band sectors, effective models and
interaction Hamiltonians"*, arXiv:2311.09290v2 [cond-mat.str-el] (3 Apr 2025).

## Extraction method
- `pdftotext -layout paper.pdf paper.txt` (poppler 25.x). PDF is 38 MB, vision
  not needed — text layer clean. 6483 lines extracted.
- All equations/figures cross-checked against the -layout text (§II–§VIII + Apps
  II, D). Figure panels referenced but not OCR'd (band-structure plots — we
  regenerate the physics instead).

## Scope classification vs the assigned "loop-current" class
**IMPORTANT SCOPE NOTE.** This paper was filed under the *loop-current* class of
the TEXTURES-100 set, and the reusable kernel supplied
(`loop_current_kagome_kernel.py`) targets kagome **Peierls-flux / loop-current**
physics (staggered flux, TRS breaking, Chern/AHE). **This paper contains NO
loop-current / flux-order / TRS-breaking-current content.** It is a
*d-orbital tight-binding + S-matrix flat-band-engineering* paper for FeGe-class
kagome **materials**. The overlap with the kernel is limited to the shared
substrate: the nearest-neighbor **kagome tight-binding Bloch Hamiltonian** and
its **flat band + Dirac + van Hove** spectral structure. That substrate is
exactly the `flux=0` ('none') limit of the kernel's `KagomeModel`, so we reuse
that piece and cite provenance; the flux/Chern/loop-current machinery of the
kernel is **out of scope** for this paper and is not exercised. See
failure_analysis.md.

## Central claims of the paper
1. The "spaghetti" Fe-d band structure of FeGe (SG 191) decomposes by symmetry
   into **three decoupled orbital groups**: H1 = (d_xy, d_x2-y2) ⊕ Ge_t (px,py);
   H2 = (d_xz, d_yz) ⊕ Ge pz; H3 = d_z2 (⊕ GeH sp2). Total model
   H(k) = H1 ⊕ H2 ⊕ H3.
2. Each group forms a **bipartite crystalline lattice (BCL)**; the S-matrix
   formalism explains the origin of the quasi-flat bands near E_F.
3. **BCL flat-band counting theorem** (App. D): for a chiral BCL with sublattice
   orbital counts N_L, N_L̃ and inter-sublattice hopping rank r_s = rank(S_k),
   there are **N_L + N_L̃ − 2 r_s** perfectly flat bands at E=0. With intra-
   sublattice term A(k) having a k-independent eigenvalue of multiplicity
   n_a > N_L̃, there are at least **n_a − N_L̃** flat bands (energy ≠ 0).
4. **NN kagome Hamiltonian** hosts one perfectly flat band; the FeGe quasi-flat
   band is a weakly-dispersing descendant. The bare s-orbital NN kagome model
   (Eq. S2.25) gives flat band + Dirac cone at K + vHS (saddle) at M.
5. cRPA interactions have an approximate hidden **O_h symmetry**; averaged NN/NNN
   Hubbard U1 = 1.41 eV, U2 = 1.22 eV; on-site U ≈ 4.15 eV (Table I).
   Hartree-Fock reproduces the A-type AFM order (Q = (0,0,1/2)).

## Machine-checkable claims selected for replication (see report)
- C1: NN kagome spectrum = {flat band at +2t (degenerate, 1/3 of states), two
  dispersive bands}, Dirac touching at K, saddle (vHS) at M. Eq. S2.25 / Fig.4.
- C2: BCL Case-counting: Case#1 (only inter-sublattice, chiral) → N_d−N_p=6−2=4
  flat bands at E=0; Case#4 (H_d2=μ·1, S_{d1,d2}=0) → N_d2−N_p=3−2=1 flat band.
- C3: General chiral BCL theorem N_L+N_L̃−2·rank(S) at E=0, verified numerically
  on the paper's own S-matrix structure across BZ.
- C4: The realistic fitted H_d2/S_{d1,d2} being *small* makes the dx2-y2 band
  quasi-flat: quantify flatness (bandwidth) vs turning those hoppings on.
- C5: DOS of the NN kagome model shows a logarithmic vHS peak at the M-point
  energy and a delta-like flat-band peak (structure claim, Fig. 2/4).
