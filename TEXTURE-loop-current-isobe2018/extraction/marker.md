# Extraction marker — arXiv:1805.06449

- Extraction method: `pdftotext -layout paper.pdf` (PDF text layer intact; no
  OCR / vision needed). Paper is 8+ pages PRX with equations in text layer.
- Title: Unconventional Superconductivity and Density Waves in Twisted Bilayer Graphene
- Authors: Hiroki Isobe, Noah F. Q. Yuan, Liang Fu (MIT)
- Venue: Phys. Rev. X 8, 041041 (2018); arXiv:1805.06449v2 [cond-mat.str-el], 6 Jul 2018

## Model class
Hot-spot patch renormalization-group (RG) model for twisted bilayer graphene
near n=2 (Van Hove filling). NOT a tight-binding / loop-current-kagome model.

## Key extracted equations (machine-checkable)
- Eq. (1): general 16-process interaction Hamiltonian; 9 momentum-conserving gij.
- Eqs. (2)-(7): bare particle-hole / particle-particle susceptibilities.
- Eq. (8): d_as(y) = d chi_as / dy nesting parameters; d0- = 1.
- Eqs. (9)-(15): one-loop RG flow of g11,g22,g31,g32,g41,g42 (and gi4 frozen).
- Eq. (16),(24): RPA-resummed susceptibility chi_eta and its divergence.
- Eqs. (17)-(23): interaction strengths V_eta for s/d/p/f-SC, CDW-, CDW0,
  SDW-, SDW0, PDW+.

## Central claims
1. gi4 (intravalley) do not flow (Eq. 9).
2. Sym density-density, no exchange: mean-field finds no SC; RG generates
   attractive d/p-SC via generated g42-g32 < 0.
3. Under nesting (d1->0) g22 grows unchecked (forward scattering) while BCS-
   coupled g32,g42 decrease -> drives Q- density wave + d/p-SC.
4. Two leading instabilities: CDW-/SDW- at Q- and d/p-wave SC; weak nesting
   favors SC, strong nesting favors density wave; Q- dominates Q0.
5. No exchange -> s=f, d=p, CDW-=SDW- susceptibility degeneracies; exchange
   interactions lift them.
