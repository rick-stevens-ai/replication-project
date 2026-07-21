# MARKER EXTRACTION (interim: pdftotext fallback)

> Interim extraction via pdftotext; marker/nougat not run in this fast pass. Source: jiang2023.pdf (arXiv:2311.09290v2). Full text at work/textures-loop-current-jiang2023.txt (297KB).

FeGe as a building block for the kagome 1:1, 1:6:6, and 1:3:5 families: hidden d-orbital decoupling
of flat band sectors, effective models and interaction Hamiltonians
Yi Jiang,1, 2, 3, ∗ Haoyu Hu,3, 4, ∗ Dumitru Călugăru,4, ∗ Claudia Felser,5 Santiago
Blanco-Canosa,3, 6 Hongming Weng,7, 8 Yuanfeng Xu,9, † and B. Andrei Bernevig4, 3, 6, ‡

arXiv:2311.09290v2 [cond-mat.str-el] 3 Apr 2025

1

Beijing National Laboratory for Condensed Matter Physics and Institute of Physics, Chinese Academy of Sciences, Beijing 100190, China
2
University of Chinese Academy of Sciences, Beijing 100049, China
3
Donostia International Physics Center (DIPC), Paseo Manuel de Lardizábal. 20018, San Sebastián, Spain
4
Department of Physics, Princeton University, Princeton, New Jersey 08544, USA
5
Max Planck Institute for Chemical Physics of Solids, 01187 Dresden, Germany
6
IKERBASQUE, Basque Foundation for Science, 48013 Bilbao, Spain
7
Beijing National Laboratory for Condensed Matter Physics, and Institute of Physics, Chinese Academy of Sciences, Beijing 100190, China
8
Songshan Lake Materials Laboratory, Dongguan, Guangdong 523808, China
9
Center for Correlated Matter and School of Physics, Zhejiang University, Hangzhou 310058, China
The electronic structure and interactions of kagome materials, such as the 1:1 (FeGe) and 1:6:6 (MgFe6 Ge6 )
classes, are complicated and involve many orbitals and bands around the Fermi level. Current theoretical models
treat the systems in an s-orbital kagome representation, unsuited and incorrect both quantitatively and qualitatively to the material realities. In this work, we lay the basis of a faithful framework of the electronic model for
this large class of materials. We show that the complicated “spaghetti” of electronic bands near the Fermi level
can be decomposed into three groups of Fe d orbitals coupled to specific Ge orbitals via symmetry and chemical
analysis. Such a decomposition allows for a clear analytical understanding (leading to different results than the
simple s-orbital kagome models) of the flat bands in the system based on the S-matrix formalism of generalized
bipartite lattices. Our three minimal Hamiltonians can reproduce the quasiflat bands, van Hove singularities,
topology, and Dirac points close to the Fermi level, which we prove by extensive ab initio studies. We also
obtain the interacting Hamiltonian for the d orbitals in FeGe using the constraint random phase approximation
(cRPA) method, which faithfully describes the antiferromagnetic phase. We then use FeGe as a fundamental
“LEGO-like” building block for a large family of 1:6:6 kagome materials, which can be obtained by doubling
and perturbing the FeGe Hamiltonian. We apply the model to its kagome siblings FeSn and CoSn, and also
MgFe6 Ge6 . We further extend the formalism developed for the 1:1 family to the 1:3:5 family AB3Z5 (A = K,
Rb, Cs; B = Cr, V, Ti; Z = Sb, Bi), demonstrating the broad applicability of the LEGO-like building block
approach. Moreover, our method has the potential to be applied to a wider range of materials beyond kagome
systems, provided that the relevant LEGO-like building blocks in the crystal and electronic structures can be
identified. Our work serves as the first complete framework for the study of the interacting phase diagram of
kagome compounds.

I.

INTRODUCTION

Kagome materials exhibit a rich phase diagram including charge density waves1–25 , superconductivity26–49 , different magnetic orders50–57 and topological states58–67 . In recent years, kagome superconductors AV3 Sb5 (A=K, Cs, and
Rb)68–73 of the 1:3:5 class (with unusual charge orders74–81 but
no soft phonon modes observed82–85 ) and ScV6Sn686? ? –98 of
the 1:6:6 class51,99–103 (with soft phonon modes first observed
in experiments87,89 ) have attracted much attention. Among the
kagome materials, the kagome magnet FeGe50,104–119 of the
1:1 class (or, equivalently, the 3:3 class) is particularly attractive: it develops an A-type antiferromagnetic (AFM) order below TN = 410 K120–122 , and, more interestingly, has a CDW
transition at TCDW = 100 K50,104 . The kagome 1:1 class materials in space group (SG) 191 have formula TZ, where T are
transition metals and Z are main group elements. The 1:6:6
class, however, has the formula MT6 Z6 where M are metallic
elements, which can be seen as a doubled 1:1 material (which
is T3Z3) with inserted M atoms.
A commonly used theoretical model for understanding the
non-trivial phase diagram of kagome systems is the s-orbital
tight-binding (TB) model with nearest-neighbor (NN) hop-

pings on a kagome lattice123 . However, such an s-orbital TB
model is incorrect for FeGe. It is oversimplified and fails to
give quantitative descriptions for realistic kagome materials,
which have a large number of orbitals near the Fermi level
that are entangled together. Moreover, the model also suffers a qualitative fault: the Z element occupies the triangular
and honeycomb lattice sites around the kagome T element and
electrons from the former can “hop” onto the latter. This type
of model, in general, should not have flat bands.
In this work, for the first time, we provide a clear and comprehensive understanding of the complicated “spaghetti” of
electronic bands for the kagome 1:1 and 1:6:6 materials. Our
strategy is to decompose the intricate band structures into several small groups where, within each group, a simple and analytical understanding of the band structures is feasible. We
first consider the 1:1 class and take FeGe as a representative. We separate the d orbitals of Fe into three groups that
are combined with specific orbitals of Ge based on chemical and symmetry principles. Three decoupled effective tightbinding models for the three groups of orbitals can then be
constructed, where the effective tight-binding models not only
quantitatively reproduce the quasi-flat bands, van Hove singularities (vHS), and Dirac points, but also provide an analytical understanding of the origin of flat bands, which are only

2

(a) triangular

(b) honeycomb

(c) kagome

(d) FeGe

(e) MgFe6Ge6

(f) CsV3Sb5

(a)

(b)

Figure 1.
Representative 2D lattices and crystal structures of
kagome materials in the 1:1, 1:6:6, and 1:3:5 families. The first
row illustrates representative 2D hexagonal lattices: (a) triangular,
(b) honeycomb, and (c) kagome lattices. (d)-(f) show the crystal
structures of prototype kagome materials in the 1:1, 1:6:6, and 1:3:5
families, i.e., FeGe, MgFe6Ge6, and CsV3Sb5, respectively. In FeGe,
the Fe atoms form a kagome lattice and Ge atoms form a triangular
(denoted by Ge-T in the plot) and a honeycomb lattice (denoted by
Ge-H). MgFe6Ge6 can be built by “doubling” FeGe along z-direction
and inserting Mg atoms in the middle plane of the honeycomb Ge.
The 1:3:5 CsV3Sb5 has two honeycomb layers of Sb surrounding the
kagome V layer.

flat on part of the BZ. Moreover, we also provide the full interacting Hamiltonian constructed via the constraint random
phase approximation (cRPA) method and identify a hidden
Oh symmetry of the interacting term. A Hartree-Fock meanfield study of the interacting Hamiltonian accurately reproduces the AFM phase. We next consider the 1:6:6 family,
MT6Z6, where we observe that the Hamiltonian for this family can be derived by doubling and perturbing the Hamiltonian
of the 1:1 family. By treating FeGe as a “LEGO-like” building block, we successfully construct the band structures of the
1:6:6 material MgFe6Ge651 . Finally, we adapt the formalism
