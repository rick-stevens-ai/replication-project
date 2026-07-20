# Extraction marker — cond-mat/0611113 (Hotta 2006)

## Source
- File: `paper.pdf` (8 pages, arXiv:cond-mat/0611113v1, 5 Nov 2006)
- Extracted text: `work/paper.txt` via `pdftotext -layout` (797 lines)
- Title: *Multipole Susceptibility of Multiorbital Anderson Model Coupled with Jahn-Teller Phonons*, Takashi Hotta (JAEA), J. Phys. Soc. Jpn.

## System
Sm-based filled skutterudites (SmT4X12). Multiorbital Anderson impurity model
built on a local f-electron effective Hamiltonian in the j-j coupling scheme,
solved by NRG. Central physics: which **multipole moment** (dipole/quadrupole/
octupole) dominates the low-T phase, with and without dynamical Jahn-Teller
phonons.

## Key equations extracted (page-level)
- eq (1)-(3): H_loc = H_so + H_int + H_CEF; spin-orbit matrix elements zeta.
- eq (4)-(6): Coulomb H_int with Slater-Condon F^k = 10U,5U,3U,U.
- eq (7)-(9): CEF term H_CEF; **Hutchings/Th matrix B_{m,m'}** with B40,B60,B62
  parameterized by (W,x,y): B40=Wx/15, B60=W(1-|x|)/180, B62=Wy/24, W=-6e-4 eV.
- eq (10)-(13): effective model Heff (j=5/2), Racah E0,E1,E2.
- eq (14)-(15): multiorbital Anderson H + electron-phonon H_eph (Eg JT modes).
- eq (16)-(22): **multipole operators** for j=5/2 (dipole 4u; quadrupole 3g,5g;
  octupole 2u,4u,5u) with orthonormal redefinition Tr(Xg Xg')=delta.
- eq (23)-(24): maximized multipole susceptibility matrix chi_{gg'}.
- eq (25)-(28): NRG recursion (Lambda=5, 3000 states, Nph=20).

## Figures
- Fig 1: CEF energy levels of Heff for n=2,3,5 (a-d), CEF phase diagram (e),
  jj-scheme electron configs n=1,5 (f).
- Fig 2: T*chi, entropy, specific heat without phonons (G5 and G67 GS).
- Fig 3: same with dynamical JT phonons + average displacements.

## Reported numbers targeted for machine checks
- SO gap (7/2)*lambda; j=5/2 sextet + j=7/2 octet.
- Ground-state flip Gamma5 doublet <-> Gamma67 quartet with sign of x (Fig 1f).
- Multipole operator orthonormality (below eq 22).
- 4u/5u non-mixing for n=5 (Sec 4.1, 5).
- Mixing coefficients (p,q,r): (0.326,-0.946),(0.560,0.828),(0.761,0.428,-0.488),(0.67,-0.739,0).

## Scope decision
Replicated the exactly-diagonalizable local/operator physics (single-electron
CEF+SO, multipole operator algebra). NRG-dependent chi(T) curves and many-body
Heff (n=2,3,5) marked out-of-scope (require dedicated NRG; no fabrication).
