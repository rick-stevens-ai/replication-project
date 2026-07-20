<!-- EXTRACTION PROVENANCE NOTE
  Tool: marker (marker_single) is NOT installed on this runner.
  This file is the DOCUMENTED INTERIM FALLBACK produced with `pdftotext -layout`.
  ROLE of this file: PROSE artifact — section text, figure captions, discussion,
  in reading-friendly layout. Equation rendering is DEGRADED (Unicode math glyphs,
  Majorana symbols, and product/sum operators do not survive pdftotext) — this is a
  known pdftotext limitation, NOT a physics gap.
  Authoritative equation transcriptions live in report/REPORT.tex and in
  extraction/nougat.mmd (Key-equations block).
  Regenerate with the real tool when available:
      marker_single textures-loop-current-chung2009.pdf --output_dir extraction/
-->

                                                       Nature of a topological quantum phase transition in a chiral spin liquid model
                                                                         1
                                                                             Suk Bum Chung, 1 Hong Yao, 1 Taylor L. Hughes, and 2 Eun-Ah Kim
                                                                               1
                                                                                   Department of Physics, Stanford University, Stanford, CA 94305
                                                                                   2
                                                                                    Department of Physics, Cornell University, Ithaca, NY 14853
                                                                                                      (Dated: July 27, 2021)
                                                                  We study the finite temperature nature of a quantum phase transition between an Abelian and a
                                                               non-Abelian topological phase in an exactly solvable model of a chiral spin liquid [1]. By virtue of
                                                               the exact solvability, this model can serve as a testbed for developing better measures for describing
                                                               topological quantum phase transitions. We characterize this phase transition in terms of the global
                                                               flux and entanglement entropy, and discuss to what extent the existence of a topologically ordered
                                                               ground state with non-Abelian excitations is revealed at finite temperature.
arXiv:0909.2655v1 [cond-mat.str-el] 14 Sep 2009




                                                     Characterizing and detecting topological order is one          (CSL) model [1] can provide an ideal testbed for develop-
                                                  of the central questions in the field of topological phases.      ing a better understanding of a topological QPT by play-
                                                  The challenge lies in that these new type of quantum              ing the role that the transverse field Ising chain played
                                                  ground states are not associated with any local broken            in the study of conventional QPTs. It has the virtue of
                                                  symmetry. Of broader interest in the context of quantum           being exactly solvable, and exhibiting a non-trivial QPT
                                                  phase transitions(QPT) is a question of the nature of a           between non-Abelian(nA) and Abelian(A) phases anal-
                                                  quantum critical point when a system enters a topologi-           ogous to the weak pairing and strong pairing limits of
                                                  cally ordered phase [2]. In a conventional QPT, in which          a p + ip superconductor; the same physics can also be
                                                  a local order parameter starts to gain an expectation             accomplished for the honeycomb model with three-spin
                                                  value at the quantum critical point (QCP), the nature of          interaction [14]. We take a twofold approach: First, we
                                                  the QCP is of ultimate significance. Even though it is ef-        employ the notion of an “expectation value” of a global
                                                  fectively a point of measure zero, it governs a much larger       flux operator introduced by Nussinov and Ortiz [12] as
                                                  phase space often called the “quantum critical region”            a finite temperature extension of the concept of ground
                                                  (See Fig.1(a) where we denote the expectation value of            state degeneracy. Second, we contrast this result to what
                                                  an order parameter by hφi). One can ask if, and to what           can be learned from entanglement entropy.
                                                  extent, an analogy holds for topological quantum phase
                                                  transitions. For such a question, we need a formulation
                                                  and understanding of measures of topological order at
                                                  finite temperature.
                                                     Since Wen and Niu [3] coined the term “topological or-
                                                  der” in association with the ground state degeneracy of
                                                  (Abelian) fractional quantum Hall (FQH) states on topo-
                                                  logically non-trivial surfaces, such ground state degener-
                                                  acy has been widely used as an indicator of topological
                                                  order including the non-Abelian FQH states [4]. Further,
                                                  the implications of such degeneracy on fractionalization          FIG. 1: Phase diagrams in g − T phase space. (a)A typical
                                                  has also been discussed[5, 6]. However, the extension of          QPT phase diagram for conventional order with the quan-
                                                                                                                    tum fluctuations controlled by tuning parameter g. Here we
                                                  this indicator, which is defined at T = 0 and not directly
                                                                                                                    sketched a case with the dynamical critical exponent z = 1.
                                                  accessible experimentally, to a measure at finite temper-         (b)Topological QPT phase diagram.
                                                  ature is an open question.
                                                     More recently, the concept of “topological entangle-
                                                                                                                       Model– The exactly solvable CSL model on the star
                                                  ment entropy” has been gaining interest as an indicator of
                                                                                                                    lattice [1] is a variant of a spin model with topological
                                                  topological order [7, 8] or a topological QCP [9]. The cor-
                                                                                                                    order first introduced by Kitaev[13] on the honeycomb
                                                  responding quantity at finite temperature has also been
                                                                                                                    lattice. In this variation, ground states spontaneously
                                                  studied [10]. However, one of the issues with topological
                                                                                                                    break time reversal symmetry and a QPT between A and
                                                  entanglement entropy is that it does not always distin-
                                                                                                                    nA phases is accessible through the exact solution. For
                                                  guish phases with obviously different topological orders
                                                                                                                    brevity we employ a Majorana fermion representation of
                                                  such as weak pairing (vortices follow non-Abelian statis-
                                                                                                                    the model. We represent spin-1/2 Pauli operators σiα
                                                  tics) and strong pairing (vortices are Abelian) p + ip
                                                                                                                    (α = x, y, z) of the original spin model at each lattice
                                                  superconductors [11]. This shows that the information
                                                                                                                    site i[1] by four species of Majorana fermions ci and dα
                                                                                                                                                                           i ,
                                                  about the ground state is significantly condensed upon
                                                                                                                    σiα = ici dα
                                                                                                                               i under  the constraint
                                                  mapping to a single entropic quantity.
                                                     We start with the observation that a chiral spin liquid                             Di ≡ ci dxi dyi dzi = 1           (1)
so that σ x σ y σ z = i as is expected of spin 1/2 operators.
In terms of these Majorana fermions, the Hamiltonian is
                  X                               X
 H[{Ûij }] = J             Ûij ici cj + J 0               Ûij ici cj , (2)
               x,y,z−link                   x0 ,y 0 ,z 0 −link

                                                    0
where Ûij ≡ −idα       α
                     i dj is defined at each α and α bonds
between sites (i, j) (see Fig.2) and acts as a Z2 gauge
field living on the ij bond [18]. As Ûij has no dynamics
([Ûij , H] = 0) it can be replaced by a set of Z2 variables
uij = ±1 reducing Eq. (2) to a quadratic Hamiltonian
H[{uij }] parameterized   Q by {uij }. For a loop L, the Z2
flux is given by φL = ij∈L uij = ±1.
   Defining g ≡ J 0 /J, H[{uij }] can be diagonalized as
                                                                                    FIG. 2: A decorated brick wall lattice that is topologically
                          n,~k [{uij }; g] (b† ~ bn,~k − 1/2),                     equivalent to the star lattice of Ref.[1], on the surface of a
                    X
    H[{uij }] = J                                                       (3)
                                              n,k                                   torus. Green links denote uij configurations contributing to a
                    n,~
                      k                                                             global flux threading. The inset defines α links for ‘triangles’
                                                                                    and α0 links connecting ‘triangles’ with α = x, y, z. This la-
by finding the complex fermion operators bn,~k that are                             belling of links specifies components of spins interacting across
linear in ci ’s for momentum ~k and band index n =                                  the links in the original spin model.
1, 2, 3 (there are six sites per unit cell in the Majorana
fermion Hamiltonian). This yields the entire spectrum
                                                                                    where α = x, y label two global cycles Γx and Γy .
n,~k [{uij }; g]. The ground states are uniform flux states
                                                                                    Now (Φx , Φy ) = (±1, ±1) are four distinct states where
with φ0L = −1 for all 12-plaquettes and φ0L = 1 or −1 for                           Φx = −1 and Φy = −1 indicates π flux threaded through
all triangular plaquettes, spontaneously breaking time re-                          the distinct holes of the torus (see Fig.2). Normally
versal symmetry. A vortex on a plaquette L, defined by                              the fermion parity in the unprojected ground state wave
φL = −φ0L , costs finite energy for all g. Moreover, the                            function in all four topological sectors is even and in-
uniform flux ground state is degenerate on a torus and                              dependent of g. Thus, they will survive the projection
the topological√degeneracy changes across the nA to A                               and give rise to four-fold topological degeneracy. This
QPT at gc = 3[1]. However, care is needed for discern-                              is indeed the case on the A side (g > gc ). However,
ing physical states that satisfy the constraint Eq. (1) for                         the fermion parity in the unprojected ground state wave
each configuration of {uij }.                                                       function in the (−1, −1) sector on the nA side (g < gc ) is
   Topological degeneracy and the projection                                        odd and consequently it does not survive projection [20].
operator– A clue towards an extension of topological                                Thus there is only a three-fold topological ground state
degeneracy to finite temperature lies in the g-dependent                            degeneracy in the nA phase. In summary, for A phases
effects of the constraint Eq. (1). The constraint de-                               with uniform flux, all the physical states consist of an
fines the physical states of the free fermion Hamiltonian                           even number of fermionic quasiparticle excitations above
Eq. (3) and is sensitive to g. Eq. (1) can     Q be imple-                          the ground states in all four topological sectors. For nA
mented using a projection operator P̂ = i 12 (1 + Di )                              phases with uniform flux, all physical states have an even
since Di P̂ = P̂ [1, 13, 16]. Moreover, P̂ commutes with                            number of fermion excitations in sectors (1, 1), (1, −1),
the original Hamiltonian H[{Ûij }]. We can show that                               and (−1, 1), but an odd number of fermion excitations
whether a state survives projectionQ only depends on the                            in the sector (−1, −1). This has consequences not only
fermion parity, defined as Pf = ij∈x0 ,y0 z0 -links ici cj , and                    for the topological ground state degeneracy, but also at
the parity of the number of vortex excitations [19] on                              finite temperature, as shown below.
triangle plaquettes.                                                                   Global flux expectation value– Motivated by the
   In the uniform flux sector, all physical states have                             connection between the change in the allowed physical
even fermion parity Pf = 1, which is particularly impor-                            spectrum at the topological QPT and the global flux
tant for determining the topological degeneracy of the                              states, we consider the ‘expectation value’ of the global
ground states on a torus. Topological degeneracy comes                              flux hΦα i defined as [12]
from the identical free fermion spectra, in the thermo-
                                                                                                                   1
dynamic limit, in the four possible topological sectors,                                             hΦα (T )i ≡     tr Φα e−H/T                 (5)
distinguished by the choice of the Z2 global flux:                                                                 Z
                             Y                                                      in a finite size system with N sites. This ties the topo-
                  Φα ≡               uij = ±1,                          (4)         logical degeneracy to the spectrum and offers a natural
                           hiji∈Γα                                                  finite T extension of topological degeneracy. If we further


                                                                                2
restrict ourselves to uniform flux states (which is valid at
T = 0 and is a good approximation in the vicinity of the
QCP where the fermion gap vanishes but vortex gap is
finite), Eq. (5) can be recast as
                                             (Φx ,Φy )
                       P
                           Φx ,Φy =±1 Φα Z
             hΦα i =                                     ,   (6)
                                   Z
where we have defined a sub-partition function for each
global flux sector (Φx , Φy ). So, for the uniform flux states
Z (Φx ,Φy ) = tr (Φx ,Φy ) exp(−H/T ).
   Clearly, in the absence of a dependence of the physical             FIG. 3: Defining T ∗ through the exponential decay of the
spectrum on the global flux, all the sub-partition func-               hΦx (T )i. The plot is for g = 1.3 < gc on a 60 × 40 lattice.
tions will be identical Z (−1,−1) = Z (1,1) = Z (1,−1) =
Z (−1,1) and hΦα i will average out to be identically zero.
This is the case for the A phase; and the case of toric
code previously studied[12]. However, for the nA phase
of the CSL model, the (−1, −1) sector is projected out of
the ground state Hilbert space and hence Z (−1,−1) (T =
0)nA = 0. This yields a finite and definite hΦα i in the
nA phase at T = 0:
                              (
                                1/3 (nA, g < gc )
            hΦx i(T = 0) =                        .        (7)
                                   0 (A, g > gc )
                                                                       FIG. 4: The T ∗ (solid line) compared to the single fermion
The significance of Eq.(7) is that hΦx i is the first identi-          excitation gap (dashed line) for a 60×40 lattice in the vicinity
fication of a quantity that can be defined in a thermody-              of gc . Although both Abelian and non-Abelian phases are
namic sense that changes at the topological QPT. Now                   gapped, T ∗ is defined only in the non-Abelian phase.
the relation hΦx i(T = 0) can be related to the topological
degeneracy through
                                                                       which allows the identification of the nA phase at finite
                nDEG = 4 − 3hΦx i(T = 0).                    (8)       temperature.
                                                                         The crossover scale T ∗ has an intriguing system size
Most importantly, this identification allows one to extend             dependence. For a large system of N sites,
the notion of topological degeneracy to finite temperature
                                                                                                       ∆(g)
through hΦx i(T 6= 0) and to investigate the vicinity of the                                    T∗ ∼        ,                      (9)
topological QPT that is largely unknown in Fig.1(b).                                                   ln N
   Analogous to Tc (g) (the solid line of Fig.1(a)) and the            where ∆(g) is the energy gap in the fermion spectrum(see
cross over line (dashed line in Fig.1(a)) in the vicinity              Fig.4). Hence T ∗ → 0 as N → ∞, but at a rate slower
of a conventional QCP, we define and investigate a cross               than any other quantity in the system. Therefore, the
over temperature scale T ∗ (g) above which hΦx i falls off to          distinction between the A phase and the nA phase, while
zero for a system with finite size. As shown in Fig. (3), a            strictly vanishing at finite temperature in the thermo-
crossover temperature scale T ∗ (g) can be defined as the              dynamic limit, can be meaningful in some sizable range
temperature scale at which hΦx i(T ) falls off exponen-                of N . Interestingly, this system size dependence bares
tially from its zero temperature value at a given value of             similarity with the crossover scale for the finite tempera-
g < gc . In Fig. (3), we show hΦx i(T ) for g = 1.3 as de-             ture topological entanglement entropy of the toric code in
fined in Eq.(5). For all g < gc , hΦx i is nearly a constant           Ref.[10]. It is also reminiscent of the finite temperature
(1/3) for T < T ∗ (g), but decays exponentially to zero                behavior of an Ising chain of finite length. An Ising chain
at higher temperatures. We have defined T ∗ (g) as the                 does not order at any finite temperature in the thermo-
point at which Z (−1,−1) (T ∗ )/Z (1,1) (T ∗ ) = e−1 by con-           dynamic limit. However, one can define a finite crossover
vention. Above T ∗ , the distinction between the A and                 temperature scale in a finite size system of length N by
the nA phase vanishes. The plot of T ∗ (g) in Fig.4 shows              comparing the energy cost 2J for a domain wall and the
that T ∗ (g) is a distinct scale which is non-vanishing at             entropic gain of T log N for N possible choice for the po-
the QCP g = gc , unlike the excitation gap which van-                  sition of the domain wall. Nevertheless, the present size
ishes. The excitation gap is non-vanishing in both phases              dependence Eq.(9) is rather a consequence of hΦx i(T ) be-
where, in contrast, T ∗ (g) is only non-zero for g < gc                ing bounded from below by tanhN (∆/2T )/3 (see SOM)


                                                                   3
                                                                    through the problem, we consider the change in the en-
                                                                    tanglement entropy in the presence of a pair of vortex
                                                                    excitations, one each in the two regions A and B whose
                                                                    entanglements are under consideration. Fig. (5) shows
                                                                    the result as a function of g. The additional entropy of
                                                                    log 2 of the nA phase reflects the double degeneracy asso-
                                                                    ciated with Majorana fermion vortex core states respon-
                                                                    sible for the non-Abelian statistics of the vortices. It is
                                                                    clear that the characteristics of finite-energy excitations
                                                                    are important qualities of the topological phases.
                                                                       Closing remarks– We studied the nature of the topo-
FIG. 5: The entanglement entropy change due to a vortex             logical QPT between a nA phase and an A phase in
pair excitation for 30 × 30 Kagomé lattice sites on a torus.       an exactly solvable model using finite temperature ex-
The change at gc is not sharp for this finite size, though it       tensions of two separate measures of topological order.
approaches the thermodynamic limit value of ln 2 in the nA          The expectation value of the global flux hΦi(T ) is a fi-
phase.                                                              nite temperature extension of the ground state topolog-
                                                                    ical degeneracy which clearly changes at the QPT. We
                                                                    found that hΦi(T ) retains the T = 0 value for g < gc
and it is unrelated to local fluctuations. Possible con-            up to a crossover temperature scale which decays loga-
nections underlying these apparent similarities and their           rithmically with the system size. Whether this type of
implications for a “quantum critical region” is an open             crossover is ubiquitous for topological phases in two spa-
question.                                                           tial dimension is an open question. As a step towards a
   Towards finite T entanglement entropy–While                      finite temperature extension of γ, which is independent of
the topological entanglement entropy [7, 8] of the ground           g at T = 0, we considered the effect of a pair of vortices.
state wave function has been widely adopted as a measure            This indicates the possibility that γ(T ) might distinguish
of topological order, it is does not distinguish the A phase        the nA phase from the A phase.
from the nA phase in the present case [17]. The topolog-               Acknowledgement- We would like to thank C.
ical entanglement entropy γ is defined as the universal             Castelnovo, C. Chamon, S. Kivelson, Z. Nussinov, G.
constant term in the entanglement entropy in addition               Ortiz, M. Oshikawa, J. Pachos, S. Sondhi, M. Stone,
to the usual term proportional to the perimeter of the              S. Trebst, Z. Wang, T. Xiang for sharing their insights.
boundary: Sent = αL − γ. Further it is known that γ is              SBC and TLH are supported by DOE grant DE-AC03-
given by the total
                 pP quantum dimension of the   √ topological        76SF00515; SBC also by SITP at Stanford University.
phase : γ = ln          d2 . Since {d } = {1, 2, 1} in the
                     α α              α                             HY is supported by DOE grant DEFG03-01ER45925
nA phase while {dα } = {1, 1, 1, 1} in the A phase [17],            and SGF at Stanford University. E-AK is supported in
the topological QPT does not affect γ which is equal to             part by the Nanoscale Science and Engineering Initia-
2 in both phases. However, it is possible a finite tem-             tive of the National Science under NSF Award #EEC-
perature extension of this quantity might offer a possible          0646547. We acknowledge the UIUC ICMT for its hospi-
distinction between the two phases, as excitations with             tality through “Workshop on Topological Phases in Con-
distinct statistics would contribute.                               densed Matter” during early stages of this work.
   An extension of the entanglement entropy to T 6= 0
must involve the inclusion of thermal excitations. For
instance, the extension proposed in Ref.[10] (an alterna-
tive definition was proposed in Ref.[15]) retains the basic
form Sent = −Tr(−ρA ln ρA ) but uses for the ρA , a ther-            [1] H. Yao and S. A. Kivelson, Phys. Rev. Lett. 99, 247203
malized reduced density matrix                                           (2007).
                                                                     [2] X.-Y. Feng, G.-M. Zhang and T. Xiang, Phys. Rev. Lett.
                        X e−Eλ /T                                        98, 087204 (2007); I. S. Tupitsyn et al, arXiv:0804.3175;
            ρA (T ) =               TrB |Φλ ihΦλ |,     (10)             C. Gils et al, arXiv:0906.1579.
                             Z                                       [3] X.-G. Wen and Q. Niu, Phys. Rev. B 41, 9377 (1990).
                        λ
                                                                     [4] G. Moore and N. Read, Nucl. Phys. B, 360, 362 (1991).
where |Φλ i’s are energy eigenstates. Clearly Eq.(10) re-            [5] M. Oshikawa and T. Senthil, Phys. Rev. Lett. 96, 060601
duces to the usual definition at T = 0 when only the                     (2006); Y.-S. Wu, Y. Hatsugai, and M. Kohmoto, Phys.
ground state(s) enter the sum.                                           Rev. Lett. 66, 659 (1991).
                                                                     [6] M. Oshikawa et al, Ann. Phys. (NY), 322, 1477-1498
   While the zero temperature topological entanglement                   (2007); S. B. Chung and M. Stone, J. Phys. A 40, 4923
entropies of the A and nA phases are identical, the dif-                 (2007).
ferent excitations of each phase will generically lead to            [7] A. Yu. Kitaev and J. Preskill, Phys. Rev. Lett. 96,
different finite-temperature quantities. As a first pass                 110404 (2006).


                                                                4
 [8] M. Levin and X-G. Wen, Phys. Rev. Lett. 96, 110405                 Since in the nA phase, the fermion occupation number
     (2006).                                                            parity is odd in the (Φx , Φy ) = (−1, −1) sector and even
 [9] E. Fradkin and J. Moore, Phys. Rev. Lett. 97,050404                in all the other sectors
     (2006)
[10] C. Castelnovo and C. Chamon, Phys. Rev. B 78, 155120
                                                                         (1,1)    (−1,−1)
                                                                                                                Y
     (2008).                                                            ZCSL ±ZCSL          = 2 exp(−EG /T )     [1±exp(−n,~k /T )],
[11] N. Read and D. Green, Phys. Rev. B 61, 10267 (2000).                                                       n,~
                                                                                                                  k
[12] Z. Nussinov and G. Ortiz, Phys. Rev. B 77, 064302                                                                     (12)
     (2008).
[13] A. Yu. Kitaev, Ann. Phys. (N.Y) 321, 2 (2006).
                                                                        where EG is the ground state energy. With Eq.(12),
[14] D.-H. Lee, G.-M. Zhang, and T. Xiang, Phys. Rev. Lett.             we can recast the global flux thermal expectation value
     99, 196805 (2007).                                                 hΦx i(T ) as
[15] S. Iblisdir et al, Phys. Rev. B 79, 134303 (2009), S. Ib-
     lisdir et al, arXiv: 0812.4975.                                                              Q
                                                                                                       ~ tanh(n,~
                                                                                                     n,k         k /2T )
[16] H. Yao, S.-C. Zhang, and S. A. Kivelson, Phys. Rev. Lett.                    hΦx i(T ) =        Q                       .   (13)
     102, 217201 (2009)                                                                         2+       k tanh(n,~
                                                                                                       n,~         k /2T )
[17] Zhenghan Wang, private communication.
[18] Note that the original representation in Ref. 1 introduces
     Z2 gauge fields only on z, z 0 , and the ‘cut’ links, which        This implies
     corresponds to a particular gauge choice here.
[19] After gauge fixing, the P̂ expansion of Ref. [16] can be                         N                                 N
                             Q                    Q                       1       ∆(g)               1       ∆(g) + W (g)
     factorized: P̂ = [1 + i Di ]Ĝ = [1 + Pf L∈4,O φL ]Ĝ,                  tanh          < hΦx i <    tanh
                                                                          3        2T                2            2T
     where Ĝ = [1+ j Dj + i<j Di Dj +· · · ] (note Di2 = 1).
                      P        P
                                                                                                                            (14)
[20] The exclusion of the (−1, −1) state from the ground state
     for g < gc is tied to the nA statistics of the vortices.           where ∆(g) and ∆(g) + W (g) are respectively the min-
     A global flux threading Φα is equivalent to the proce-             imum and maximum of the energy spectrumn,~k [g] that
     dure of (i)creating a vortex pair (ii) transporting one vor-       depends on g. Since ∆(g) and W (g) remains finite in the
     tex around the loop Γα (iii) annihilating the pair[6]. The         thermodynamic limit of N → ∞ Eq.(14) implies
     (−1, −1) sector is equivalent to two vortex loops linked
     to each other, which cannot be undone in the nA phase.
                                                                                                lim hΦx i → 0                    (15)
                                                                                                N →∞

 THE SUPPORTING ONLINE MATERIAL: THE
  SYSTEM SIZE DEPENDENCE OF T ∗ IN THE                                  in the thermodynamic limit.            Further using
          NON-ABELIAN PHASE.                                            [tanh(∆/2T )]N ≈ 1 − 2N exp(−∆/T ) at large N
                                                                        and low T , we find the system size dependence of the
   Since the vortex gap never closes for all values of g,               crossover temperature:
we can ignore the vortex excitation in calculating hΦx i
in the vicinity of the QPT:                                                                            ∆(g)
                                                                                                T∗ ∼        ,                    (16)
                            (1,1)     (−1,−1)
                                                                                                       ln N
                          Z        − ZCSL
              hΦx i(T ) = CSL(1,1)     (−1,−1)
                                               .            (11)
                         3ZCSL + ZCSL




                                                                    5
