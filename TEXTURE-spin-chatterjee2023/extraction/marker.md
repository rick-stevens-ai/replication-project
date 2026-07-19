Second-order topological superconductor via noncollinear magnetic texture
Pritam Chatterjee ID ,1, 2 Arnob Kumar Ghosh ID ,1, 2, 3 Ashis K. Nandy ID ,4, ∗ and Arijit Saha ID 1, 2, †

arXiv:2308.12703v2 [cond-mat.mes-hall] 29 Jan 2024

2

1
Institute of Physics, Sachivalaya Marg, Bhubaneswar-751005, India
Homi Bhabha National Institute, Training School Complex, Anushakti Nagar, Mumbai 400094, India
3
Department of Physics and Astronomy, Uppsala University, Box 516, 75120 Uppsala, Sweden
4
School of Physical Sciences, National Institute of Science Education and Research,
An OCC of Homi Bhabha National Institute, Jatni 752050, India

We put forth a theoretical framework for engineering a two-dimensional (2D) second-order topological superconductor (SOTSC) by utilizing a heterostructure: incorporating noncollinear magnetic
textures between an s-wave superconductor and a 2D quantum spin Hall insulator. It stabilizes the
higher order topological superconducting phase, resulting in Majorana corner modes (MCMs) at
four corners of a 2D domain. The calculated non-zero quadrupole moment characterizes the bulk
topology. Subsequently, through a unitary transformation, an effective low-energy Hamiltonian reveals the effects of magnetic textures, resulting in an effective in-plane Zeeman field and spin-orbit
coupling. This approach provides a qualitative depiction of the topological phase, substantiated by
numerical validation within exact real-space model. Analytically calculated effective pairings in the
bulk illuminate the microscopic behavior of the SOTSC. The comprehension of MCM emergence
is supported by a low-energy edge theory, which is attributed to the interplay between effective
pairings of (px + py )-type and (px + ipy )-type. Our extensive study paves the way for practically
attaining the SOTSC phase by integrating noncollinear magnetic textures.

Introduction.— The appearance of Majorana zero
modes (MZMs) in topological superconductors (TSCs)
has sparked significant interest in the quantum condensed matter community. [1–8]. In the quest to achieve
MZMs in heterostructures, the placement of magnetic
adatoms fabricated on a bulk s-wave superconductor
presents a promising route, uniting theoretical and experimental efforts [9–34]. The interplay between classical spin magnetism, represented by chains or adatoms,
and superconductors (SCs) results in the emergence of
Yu-Shiba-Rusinov (YSR) states (Shiba states), within
the superconducting gap [9, 10, 35]. The overlap of
Shiba states lead to Shiba bands, potentially governing a first-order TSC phase [9, 10, 36–43], analogous to
the one-dimensional Kitaev model [1, 4]. Experimentally, the YSR states and/or the MZMs have been observed by growing magnetic impurities on an s-wave SC
substrate [44–54]. Nevertheless, the creation of YSR
states goes beyond 1D systems; in a two-dimensional
(2D) arrangement where noncollinear magnetic textures
proximitized with an s-wave SC, unique effects like the
emergence of 1D Majorana dispersive/flat edge modes
emerges [37–39, 55–64], setting them notably different
from the typical observation of MZMs.
Conversely, the higher-order topological insulators (HOTIs) [65–79] and the higher-order topological superconductors (HOTSCs) [80–107], hosting mdimensional boundary modes (m=d–n, where d is the dimension and n is the topological order), have generated a
profound research interest. In this emerging field, certain
theoretical proposals offer elegant strategies to create
second-order topological superconductors (SOTSCs) in

∗ aknandy@niser.ac.in
† arijit@iopb.res.in

FIG. 1. We present a schematic illustration of a heterostructure setup featuring a 2D noncollinear magnetic texture (blue
arrows) and an s-wave superconductor (yellow), with a quantum spin Hall insulator (green) in between. In the topological phase, the system hosts localized Majorana corner modes
(brown spheres) at its four corners. These features can be experimentally realized using standard scanning tunnelling microscopy (STM) technique. The four edges in the setup are
labelled by I, II, III and IV.

2D heterostructures hosting zero-dimensional (0D) Majorana corner modes (MCMs), involving 2D quantum
spin Hall insulators (QSHIs) or two-dimensional electron
gases with Rashba spin-orbit coupling (SOC) proximitized by an s-wave superconductor [86, 90]. Notably,
an in-plane Zeeman term stabilizes the MCMs. Another
proposal for SOTSC centers around the ferromagnetic
alignment of magnetic adatoms on an s-wave SC with
Rashba SOC [107]. A SC version of the Bernevig-HughesZhang (BHZ) model has also been proposed in the context of monolayer Fe(Se,Te) heterostructures [85], where
the magnetic layer exbibits bicollinear antiferromagnetic

2

FIG. 2. (a) The LDOS distribution associated with the energy E=0 is computed using H [Eq. (1)] in the 2D domain
i.e., the Lx -Ly plane where MCMs are localized at four corners of the domain. In the inset, the eigenvalue spectrum as a
function of the state index n exhibits four zero-energy (E=0)
modes within a gap. The simulated domain consists of 30×30
lattice sites while we choose the model parameters as, t=1.0,
Jex =0.8, g=0.2, ∆0 =0.4, λx =λy =λ=0.5, and ϵ0 =1. In panel
(b), the eigenvalue spectra corresponding to H in Eq. (1) are
depicted as a function of the spiral wave vector g under open
boundary conditions. The topological phase transition point
is highlighted by a vertical red dashed line.

(AFM) order. Subsequently, Ref. [54] introduces an alternative materials-centric strategy, presenting a sophisticated experimental plan to achieve the SOTSC phase,
supported by a Rashba SOC-inclusive model Hamiltonian describing a magnet-superconductor hybrid (MSH)

H=

system. Indeed, the experiment has confirmed an AFM
order of Cr layer on Nb(110). Currently, no theoretical
proposal via a model Hamiltonian approach exists to realize the SOTSC phase in the presence of a noncollinear
magnetic texture but excludes the Rashba SOC term.
Thus, several intriguing questions arise to generate the
SOTSC phase using a MSH setup: (a) How can a SOTSC
phase hosting MCMs be achieved by initiating from a 2DQSHI positioned between a texture of magnetic atoms
and an s-wave SC? (b) What characterizes the pairing
structures that are responsible for the emergence of the
MCMs?
In this letter, our model setup comprises of a heterostructure geometry featuring a QSHI (mimicking a
CdTe-HgTe-CdTe type quantum-well [108, 109]) coupled
with a noncollinear magnetic texture, positioned in close
proximity to a bulk s-wave SC (see Fig. S1). Subsequently, we establish a unitary transformation to derive
a momentum-space Hamiltonian, offering analytical insights into our analysis by calculating the effective lowenergy edge theory. By employing a duality transformation, we uncover two varieties of SC pairings - (px + py )type and (px + ipy )-type - whose interplay leads to the
emergence of the SOTSC phase.
Realization of the SOTSC phase and characterizing its
topological properties.— The real-space Hamiltonian for
our configuration is given by:

X †
ci,j [{ϵ0 Γ1 +∆0 Γ2 +Jex (Γ3 cos ϕij + Γ4 sin ϕij )} ci,j −{tΓ1 + iλx Γ5 } ci+1,j −{tΓ1 + iλy Γ6 } ci,j+1 ] + h.c. , (1)
i,j

where, the lattice site indices i and j runs along xand y-direction, respectively and the Γ matrices (8 ×
8) are given as Γ1 =τz σz s0 , Γ2 =τx σ0 s0 , Γ3 =τ0 σ0 sx ,
Γ4 =τ0 σ0 sy , Γ5 =τz σx sz , and Γ6 =τz σy s0 . The three Pauli
matrices σ, s and τ act on orbital (a, b), spin (↑, ↓),
and particle-hole degrees of freedom, respectively. We
work with the Bogoliubov-de Gennes (BdG) basis as:
n
oT
ci∈x,y = cia↑ , cia↓ , cib↑ , cib↓ , −c†ia↓ , c†ia↑ , −c†ib↓ , c†ib↑ , and
T denotes the transpose operation. Here, ϵ0 , ∆0 , t,
and λx,y represent staggered mass term, superconducting gap, hopping amplitude, and the strength of SOC,
respectively. In this context, Jex signifies the local exchange interaction strength between the magnetic impurity spin and the SC electrons, while ϕ denotes the angle between adjacent spins within the magnetic texture.
We have chosen ϕxy = gx x + gy y [64], where the pitch
of the noncollinear magnetic phase, particularly in the
context of the spin-spiral state with a specific propagation direction, is dictated by gx and gy . Note that, the
Hamiltonian in Eq. (1) reduces to the BHZ model of 2D
QSHI [108, 109] when Jex = ∆0 = 0. This model was
proposed based on two specific types of materials, such
as HgTe-CdTe quantum wells. These materials possess

intrinsic SOC, represented by λx and λy in Eq. (1). The
BHZ model already exhibits first-order topology hosting
gapless helical edge modes. This motivates us to achieve
a SOTSC by introducing the terms Jex and ∆0 , representing a noncollinear spin texture and an s-wave superconductor, respectively. The composite (three layer) system can then represent the schematic described in Fig. S1
and the real space Hamiltonian introduced in Eq. (1). To
simplify matters, we assume gx =gy =g and λx =λy =λ in
our numerical computations, without loss of generality.
We qualitatively discuss our results in the case of rotational asymmetry, where gx ̸= gy and λx ̸= λy (see the
supplemental material (SM) [110] for details). We further emphasize that higher-order topology predicted in
our model does not depend on the square-shaped geometry, and one can still obtain the MCMs in a disc or
triangular geometry (see SM [110] for details).
Moving towards the numerical results associated with
the Hamiltonian in Eq. (1), we analyze the eigenvalue
spectrum and the local density of states (LDOS). We depict the LDOS associated with E=0 in Fig. S2 (a) and
in the inset, the eigenvalue spectrum En as a function
of state index n is illustrated, obtained by utilizing open

3
Exact

Exact

MCMs

MCMs

Effective

The SOTSC phase can be topologically characterized
by employing the bulk quadrupole moment (Qxy ) calculation [65, 66, 111, 112]. Within the topological regime,
the value of Qxy is quantized to 1/2 and hence, one expects the presence of highly localized corner states. In
contrast, the value of Qxy becomes zero in the trivial
phase. The Qxy is defined through the formula [111–113]

 
q
1
Qxy =
det(W † )
, (2)
Im ln det U † WU
2π

Effective

MCMs

MCMs

FIG. 3. To establish the topological phases, the calculation
of the quadrupole moment, Qxy , is performed using both the
exact real space Hamiltonian H in Eq.(1) and the effective
Hamiltonian in Eq.(4). For the first case, panels (a) and (b),
illustrate the phases in the λ-g plane (with a fixed Jex = 0.8)
and Jex -g plane (with a fixed λ = 1.0), respectively. For the
later case, these phase diagrams are depicted in panels (c) and
(d). The calculated Qxy value is quantized to 1/2 within the
topological region (yellow) and remains at zero in the trivial
region (blue). In the lattice model, we consider a simulated
domain of 30 × 30 lattice sites. The phase boundaries, indicated by the white line, is determined using the low-energy
edge theory. The rest of the model parameters take the same
value as mentioned in Fig. S2.

boundary conditions (OBC). The Majorana modes are located at E = 0 with a negligible separation from the zeroenergy ∼ O(10−7 ) in a finite size system. The presence of
zero-energy states becomes evident when examining the
eigenvalue spectrum, and the localization of these states
at the four corners of the 2D domain i.e., the MCMs
corroborates the second-order topological nature of the
system [96]. To trace out the phase boundary, we display
the eigenvalue spectra E of H as a function of the spiral
pitch vector g in Fig. S2 (b) and here, we highlight a qualitative phase transition boundary, indicating a transition
to a trivial SC state. Note that, in the limit g=0 (i.e., a
trivial collinear magnetic texture), H in Eq. (1) resembles the system with a QSHI, s-wave SC, and a constant
Zeeman field as discussed in Refs. [90, 96]. On the other
hand, we emphasize that in our system, we consider a
spatial variation of the magnetic impurity spins through
noncollinear 2D magnetic textures, while in earlier studies in this context, a rotating applied magnetic field has
been considered without any spatial variation [93, 105].
Importantly, our model Hamiltonian setup works without any external magnetic field as far as the origin of
MCMs is concerned.

where, U is an N ×Nocc dimensional matrix encompassing the number of occupied eigenstates Nocc in H, see
Eq. (1), arranged according to their energy. The operator W=exp [i2π q̂xy ] corresponds to the microscopic
quadrupole operator q̂xy =x̂ŷ/L2 , where x̂ (ŷ) is position
operator defined in the system with dimension L along
one direction.
By solving the lattice model Hamiltonian numerically,
we calculate the quadrupole moment Qxy and illustrate
its behavior in the λ-g and Jex -g plane in Figs. S3(a)
and (b), respectively. Here, the yellow (blue) region designates a second order topological (trivial) regime with
Qxy = 0.5 (0). Fig. S3(a) indicates that one can obtain
the SOTSC phase for g ̸= 0 in the presence of a nonzero
SOC strength λ in the QSHI. Moreover, an increase in the
pitch g reveals constraints on the permissible values of λ
necessary to exhibit the SOTSC phase. In Fig. S3(b),
we observe that as the value of g increases, there is a
need to increase the local exchange interaction strength,
Jex to achieve the topological phase. The phase boundaries in both Figs. S3(a) and (b) are bounded by a line
(white lines), which one can compute analytically, and
we provide that analysis in the latter part.
Effective model.— To add an analytical perspective to
our investigation, we employ a low-energy continuum version of our Hamiltonian H in Eq. (1). Especially, we consider the following low-energy mixed-space Hamiltonian
as,
HL = ξk Γ1 +∆0 Γ2 +2λx kx Γ5 +2λy ky Γ6 +Jex S(r).s , (3)


where, ξk = ϵ0 − 4t + t(kx2 + ky2 ) and the spin at po
sition r, S(r)= cos[ϕ(r)], sin[ϕ(r)], 0 . ϕ(r) quantifies
the angle between neighboring spins. Here, k=(kx , ky )
denotes the 2D momentum vector. We introduce a
i
unitary transformation as U =τ0 σ0 e− 2 ϕ(r)sz , such that
Heff = U † HL U [64, 114]. The effective Hamiltonian Heff
reads (see the SM [110] for the detailed derivation)
Heff =ξkeff Γ1 + ∆0 Γ2 + Jex Γ3 + 2λx kx Γ5 + 2λy ky Γ6
t
− (g · k)Γ7 − λx gx Γ8 − λy gy Γ9 ,
(4)
2
where, ξkeff =ϵ0 − 4t + t(kx2 + ky2 ) + (t/4)(gx2 + gy2 ) and
Γ7 =τz σz sz , Γ8 =τz σx s0 , and Γ9 =τz σy sz . As a result of
this transformation, the 2D noncollinear magnetic texture gives rise to an effective in-plane Zeeman field (proportional to Jex ) and a corresponding effective spin-orbit

4
coupling proportional to g [64, 114]. Moreover, if we
set λx,y =0, Heff in Eq. (4) for nonzero g (=|g|) gives
rise to a gapless TSC phase hosting Majorana flat edge
modes [64]. In a different scenario, if both gx and gy are
set to zero while maintaining non-zero λx and λy values,
Eq. (4) closely resembles the model proposed in Ref. [90]
assuming the magnetization lies in-plane.

Utilizing this effective Hamiltonian, we demonstrate
the topological phase diagram in the model parameter
space as presented in Fig. S3(c) and (d), and we compare
the same with the results obtained from the exact lattice
model in Eq. (1). In our approach, we employ the lattice
regularized version of Heff by substituting kx,y → sin kx,y
2
and 1 − (kx,y
/2) → cos kx,y , followed by the computation
of Qxy . Corresponding results in the λ-g and Jex -g planes
are shown in Figs. S3(c) and (d), respectively. While the
effective theory successfully identifies the topological regions (depicted in yellow), it is important to note that
the phase boundaries separating the topological and trivial phases deviate notably from the numerically obtained
boundary lines using the exact lattice Hamiltonian, see
the white lines in Figs. S3(c) and (d). Crucially, the
effective theory provides a qualitative representation of
the lattice model, demonstrating notably strong agreement for lower values of g. This discrepancy can be attributed to the fact that the effective Hamiltonian encapsulates only one component of the magnetic impurity
spins (Jex Γ3 ), while the other component gets suppressed
during the transformation. While we initially consider a
2D noncollinear spin texture, the resulting effective magnetic field in this approach is confined to one direction.
This infers that the complex magnetic spin texture might
not be fully incorporated in the effective Hamiltonian,
which could explain such deviation from the exact numerical result. Nevertheless, this Heff in Eq. (4) further
sets the ground for us to investigate the emergence of the
MCMs in our system, which we discuss in the subsequent
text. Nevertheless, development of a formalism for the
direct computation of Qxy from the low-energy effective
Hamiltonian [Eq. (4)] can be an intriguing avenue for
future investigation, and will be presented elsewhere.

Low-energy edge theory.— Here, we utilize the lowenergy Heff [Eq. (4)] to formulate an effective edge Hamiltonian for our 2D heterostructure geometry presented in
Fig. S1. We employ the
 Fu-Kane’s criteria such that
ϵ′ = ϵ0 − 4t + 4t (gx2 + gx2 ) < 0 [115]. In the context of
edge-II as a representative example within the 2D geometry in Fig. S1, we conduct the edge theory calculation. Here, we apply periodic boundary condition along
the x-direction and OBC along the y-direction. Hence,
we substitute ky with −i∂y and treat kx , ∆0 , Jex , and
gx,y as small parameters, ensuring that tgx,y remains finite. Neglecting the kx2 term, we can partition Heff into
Heff = H0 (−i∂y )+Hp (kx , g, Jex , ∆0 ), where their expres-

sions are:
H0 =(ϵ′ − t∂y2 )Γ1 − 2iλy ∂y Γ6 + i

tgx
∂y Γ7 ,
2

tgx
kx Γ7 + ∆0 Γ2 + Jex Γ3 − λx gx Γ8
2
− λy gy Γ9 .
(5)

Hp =2λx kx Γ5 −

Through the exact solution of H0 and perturbation calculations using the eigenstates of H0 , the matrix elements
of Hp are obtained; for detailed steps, see Section S2
of the SM [110]. The edge Hamiltonian associated with
edge-II in Fig. S1 is given by,
HII = 2λx kx σx sz − λx gx σx s0 + Jex σ0 sx + ∆0 σz s0 . (6)
This Hamiltonian corresponds to a 1D Dirac equation
with mass terms proportional to λx gx , ∆0 , and Jex . Following a similar procedure, one can procure the Hamiltonian for the other edges also (see Section S2 of SM [110]
for a comprehensive discussion). We present a unified
form for the Hamiltonian of all edges as follows:
Hj = 2Aj kj σx sz + Bj σx s0 + Cj σ0 sx + ∆0 σz s0 ,

(7)

where, j indicates edges as depicted by I, II, III, and IV
in Fig. S1. Here, kI,III =ky and kII,IV =kx , and Aj ,Bj and
Cj are {−λy , λx , −λy , λx }, {λy gy , −λx gx , λy gy , −λx gx },
and {0, Jex , 0, Jex }, respectively.
By examining the edge Hamiltonians presented in
Eq. (7), it is evident that the sign of the mass terms
for
p the two intersecting edge Hamiltonians changes when
g 2 λ2 + ∆20 > Jex (see Section S2(C) in the SM [110] for
a detailed explanation). As a consequence, the JackiwRebbi theory [96, 116] can be employed to obtain the
zero-energy modes that emerge at the intersection of
the two edges, resulting in the formation of localized
MCMs. Notably, the critical value of gc , indicating the
phase boundary for the emergence of MCMs, can be
analytically
computed from the gap-closing relation as
p
2 − ∆2 /λ. We highlight this g by a red dashed
gc = Jex
c
0
line in Fig. S2 (b). Hence, the gap-closing relation offers an alternative analytical interpretation for the phase
boundary indicated by the white line in Figs. S3(a)-(d),
based on the values of Qxy . The phase boundaries obtained from the analytical expressions align well with
the actual boundaries observed in the numerical lattice model results, see Figs. S3(a) and (b). However,
it exhibits notable discrepancies when compared to the
boundaries derived from the lattice regularized version of
the effective model as shown in Figs. S3(c) and (d).
Analysis of the effective bulk pairing.— After examining the topological phase boundaries and the emergence
of MCMs, we briefly outline the nature of bulk superconducting pairing that is effectively generated through
the interplay of SOC, the spin texture, and the s-wave
SC utilizing the derived effective Hamiltonian in Eq. (4).
Applying a duality transformation [117, 118], we derive
a dual Hamiltonian H̃D from Heff as follows:


˜ D (k)
ϵ̃ +J σ s
∆
H̃D (k)= UD† Heff UD = D ˜ ex 0 x
, (8)
∆D (k) −ϵ̃D +Jex σ0 sx

5
˜ D =−ξ eff σz s0 − f˜(k); with
where, ϵ̃D =∆0 σ0 s0 and ∆
k
f˜(k)=2λx kx σx sz + 2λy ky σy s0 − λx gx σx s0 − λy gy σy sz −
t
2 (g.k)σz sz (see the details in Section S3 of SM [110]).
Despite of originating from Heff in Eq. (4), H̃D (k) in
Eq. (8) does not inherently ensure the same topological
phase as Heff [117, 118]. Nevertheless, to ensure that the
dual Hamiltonian is also capable of hosting the SOTSC
phase, we compute Qxy by employing the real space formulation of H̃D (k). Interestingly, H̃D (k) also captures
the same topological phase as Heff .
Continuing our analysis, we examine the nature of bulk
˜ D (k). Notably, we observe that the inpairing using ∆
trinsic SOC terms λx,y undergo a transformation into
(px + ipy )-type SC pairings, yielding a gap ∆px +ipy proportional to λ. In contrast, the SOC induced due to the
presence of noncollinear magnetic textures, characterized
by gx,y , transforms into a (px +py )-type SC pairing with a
gap ∆px +py that scales with g. In the context of 2D firstorder TSC, it is well-known that (px + ipy )-type pairing
induces dispersive Majorana edge modes [55, 117, 119],
while (px + py )-type pairing is responsible for the emergence of flat Majorana edge modes [55, 64, 120, 121].
When the SOC strength is set to zero, λx,y =0, the
TSC phase exclusively features the flat edge modes [64],
which seems to restrict the emergence of opposite mass
terms in the intersecting edge Hamiltonians. Thus, the
presence of SOC is crucial in creating the dispersive
edge modes, which can be gaped out by incorporating the sign-changing mass terms across the edge intersection. In conclusion, the system enters a SOTSC
phase when the (px + ipy )-pairing term (∆px +ipy ) prevails over the (px + py )-pairing term (∆px +py ). Moreover, when ∆px +ipy pairing is effectively induced in the
edges, the corner modes are really of Majorana nature
i.e., γ̃ = γ̃ †
where γ̃ is the quasi-particle operator.
E=0
Conclusion and Discussion.— We have investigated
how the arrangement of a 2D heterostructure, featuring a
QSHI sandwiched between a noncollinear magnetic texture and an s-wave superconductor, results in the SOTSC
phase hosting MCMs. The numerical outcomes, encompassing the eigenvalue spectrum and the spatial distribution of the LDOS in a lattice model, demonstrate the feasibility of creating MCMs on a 2D finite domain. These
features could be detectable using local probing methods, such as conventional scanning tunnelling microscopy
(STM) experiments. We calculate Qxy using the lattice
Hamiltonian to illustrate the phase diagram in different
parameter space. Additionally, we establish a connection with an effective continuum model through a unitary
transformation for analytical insights. The edge theory
derived from the effective Hamiltonian can explain the
numerically obtained MCMs. We also analyse the effective bulk SC pairings generated in this setup using a dual-

ity transformation. In summery, the SOTSC phase arises
from the interplay of two types of pairings - px + ipy and
px + py - due to the presence of non-zero λ and g in the
system.
Regarding practical implementation, conventional SCs
like Nb(110) exhibits a substantial SC gap, ∆0 ≈ 1.51
meV [47]. Recently, Mn/Nb(110) MSH system has found
to exhibit the coexistence of AFM and SC phases together [52]. Nevertheless, the noncollinear spin-spiral
state can be stabilized in heterostructures even with SC
substrate, owing to the effects of frustration in exchange
interactions [64, 122], and such systems can be fabricated
and investigated using Scanning Tunneling Microscopy
(STM) technique [50, 123–125]. Therefore, the potential experimental scenario for our setup involves placing
a monolayer of magnetic adatoms (Mn/Cr etc.) on top of
an s-wave superconductor (Nb/Al etc.). Such setup has
made significant recent development for the experimental realization of first-order topological superconductivity, hosting Majorana zero modes [47, 50–52]. Additionally, in our theoretical proposal, we need to introduce
another 2D layer of a QSHI, mimicking a HgTe-CdTe
quantum-well type structure [108, 109] for the realization of SOTSC hosting MCMs. To capture the signature of MCMs via LDOS [∼ (dI/dV )], one needs to employ a STM tip coated with either Nb or Cr on top of
the trilayer heterostructure [52]. Considering the SC gap
∆0 ≈ 1.51 meV (e.g., Nb) as a reference, the remaining
model parameters can take up the values (for Fig. S2): t ∼
3.78 meV, the magnetic impurity strength Jex ∼ 3.02
meV, the SOC λ ∼ 1.89 meV. However, for this set of
other model parameter values, one can find from Fig. S3
that the SOC strength λ can take up a value as small
as 0.23 meV to realize the SOTSC phase. In literature,
several articles have proposed potential values for the experimental parameters such as the intrinsic SOC strength
(λ) for the material Hg0.32 Cd0.68 Te/HgTe [108, 109],
and exchange coupling strength (Jex ∼ eV) for Fe/Mn
etc. [44, 126]. In our theoretical work, we assume all
these model parameters in terms of the superconducting gap ∆0 . However, in a real experiment, the kinetic
energy of the actual material is 100−1000 times larger
than the superconducting gap. Therefore, if we conduct
a similar analysis on the kinetic energy (hopping element
t) scale, the model parameters may fall within the range
of possible materials.

[1] A. Y. Kitaev, “Unpaired majorana fermions in quantum
wires,” Physics-Uspekhi 44, 131 (2001).

[2] D. A. Ivanov, “Non-abelian statistics of half-quantum

Acknowledgments.— P.C., A.K.G., and A.S. acknowledge SAMKHYA: High-Performance Computing Facility
provided by Institute of Physics, Bhubaneswar, for numerical computations. P.C. acknowledges Sandip Bera
for stimulating discussions. A.S. and A.K.N. acknowledge the support from Department of Atomic Energy
(DAE), Govt. of India.

6
vortices in p-wave superconductors,” Phys. Rev. Lett.
86, 268–271 (2001).
[3] C. Nayak, S. H. Simon, A. Stern, M. Freedman, and
S. Das Sarma, “Non-abelian anyons and topological
quantum computation,” Rev. Mod. Phys. 80, 1083–1159
(2008).
[4] A. Kitaev, “Periodic table for topological insulators and
superconductors,” AIP Conference Proceedings 1134,
22–30 (2009).
[5] X.-L. Qi and S.-C. Zhang, “Topological insulators
and superconductors,” Rev. Mod. Phys. 83, 1057–1110
(2011).
[6] J. Alicea, “New directions in the pursuit of majorana
fermions in solid state systems,” Reports on Progress in
Physics 75, 076501 (2012).
[7] M. Leijnse and K. Flensberg, “Introduction to topological superconductivity and majorana fermions,” 27,
124003 (2012).
[8] C. Beenakker, “Search for majorana fermions in superconductors,” Annual Review of Condensed Matter
Physics 4, 113–136 (2013).
[9] F. Pientka, L. I. Glazman, and F. von Oppen, “Topological superconducting phase in helical shiba chains,”
Phys. Rev. B 88, 155420 (2013).
[10] S. Nadj-Perge, I. K. Drozdov, B. A. Bernevig, and
A. Yazdani, “Proposal for realizing majorana fermions
in chains of magnetic atoms on a superconductor,”
Phys. Rev. B 88, 020407 (2013).
[11] J. Klinovaja, P. Stano, A. Yazdani, and D. Loss,
“Topological superconductivity and majorana fermions
in rkky systems,” Phys. Rev. Lett. 111, 186805 (2013).
[12] B. Braunecker and P. Simon, “Interplay between
classical magnetic moments and superconductivity in
quantum one-dimensional conductors: Toward a selfsustained topological majorana phase,” Phys. Rev. Lett.
111, 147202 (2013).
[13] M. M. Vazifeh and M. Franz, “Self-organized topological
state with majorana fermions,” Phys. Rev. Lett. 111,
206802 (2013).
[14] J. D. Sau and E. Demler, “Bound states at impurities as
a probe of topological superconductivity in nanowires,”
Phys. Rev. B 88, 205402 (2013).
[15] F. Pientka, L. I. Glazman, and F. von Oppen, “Unconventional topological phase transitions in helical shiba
chains,” Phys. Rev. B 89, 180505 (2014).
[16] K. Pöyhönen, A. Westström, J. Röntynen, and T. Ojanen, “Majorana states in helical shiba chains and ladders,” Phys. Rev. B 89, 115109 (2014).
[17] I. Reis, D. J. J. Marchand, and M. Franz, “Selforganized topological state in a magnetic chain on the
surface of a superconductor,” Phys. Rev. B 90, 085124
(2014).
[18] W. Hu, R. T. Scalettar, and R. R. P. Singh, “Interplay
of magnetic order, pairing, and phase separation in a
one-dimensional spin-fermion model,” Phys. Rev. B 92,
115133 (2015).
[19] H.-Y. Hui, P. M. R. Brydon, J. D. Sau, S. Tewari,
and S. D. Sarma, “Majorana fermions in ferromagnetic
chains on the surface of bulk spin-orbit coupled s-wave
superconductors,” Scientific Reports 5, 8880 (2015).
[20] S. Hoffman, J. Klinovaja, and D. Loss, “Topological phases of inhomogeneous superconductivity,” Phys.
Rev. B 93, 165418 (2016).
[21] M. H. Christensen, M. Schecter, K. Flensberg, B. M.

Andersen, and J. Paaske, “Spiral magnetic order and
topological superconductivity in a chain of magnetic
adatoms on a two-dimensional superconductor,” Phys.
Rev. B 94, 144509 (2016).
[22] G. Sharma and S. Tewari, “Yu-shiba-rusinov states and
topological superconductivity in ising paired superconductors,” Phys. Rev. B 94, 094515 (2016).
[23] G. M. Andolina and P. Simon, “Topological properties
of chains of magnetic impurities on a superconducting
substrate: Interplay between the shiba band and ferromagnetic wire limits,” Phys. Rev. B 96, 235411 (2017).
[24] V. Kaladzhyan, P. Simon, and M. Trif, “Controlling
topological superconductivity by magnetization dynamics,” Phys. Rev. B 96, 020507 (2017).
[25] A. Theiler, K. Björnson, and A. M. Black-Schaffer,
“Majorana bound state localization and energy oscillations for magnetic impurity chains on conventional superconductors,” Phys. Rev. B 100, 214504 (2019).
[26] D. Sticlet and C. Morari, “Topological superconductivity from magnetic impurities on monolayer nbse2 ,”
Phys. Rev. B 100, 075420 (2019).
[27] M. Mashkoori and A. Black-Schaffer, “Majorana bound
states in magnetic impurity chains: Effects of d-wave
pairing,” Phys. Rev. B 99, 024505 (2019).
[28] G. C. Ménard, C. Brun, R. Leriche, M. Trif, F. Debontridder, D. Demaille, D. Roditchev, P. Simon, and
T. Cren, “Yu-shiba-rusinov bound states versus topological edge states in Pb/Si(111),” The European Physical Journal Special Topics 227, 2303–2313 (2019).
[29] M. Mashkoori, S. Pradhan, K. Björnson, J. Fransson,
and A. M. Black-Schaffer, “Identification of topological superconductivity in magnetic impurity systems using bulk spin polarization,” Phys. Rev. B 102, 104501
(2020).
[30] R. L. R. C. Teixeira, D. Kuzmanovski, A. M. BlackSchaffer, and L. G. G. V. D. da Silva, “Enhanced majorana bound states in magnetic chains on superconducting topological insulator edges,” Phys. Rev. B 102,
165312 (2020).
[31] S. Rex, I. V. Gornyi, and A. D. Mirlin, “Majorana
modes in emergent-wire phases of helical and cycloidal
magnet-superconductor hybrids,” Phys. Rev. B 102,
224501 (2020).
[32] V. Perrin, M. Civelli, and P. Simon, “Identifying majorana bound states by tunneling shot-noise tomography,”
Phys. Rev. B 104, L121406 (2021).
[33] A. Kobialka, N. Sedlmayr, M. M. Maśka,
and
T. Domański, “Dimerization-induced topological superconductivity in a rashba nanowire,” Phys. Rev. B 101,
085402 (2020).
[34] D. Mondal, A. K. Ghosh, T. Nag, and A. Saha,
“Engineering anomalous floquet majorana modes and
their time evolution in helical shiba chain,” (2023),
arXiv:2304.02352 [cond-mat.mes-hall].
[35] H. Shiba, “Classical Spins in Superconductors,”
Progress of Theoretical Physics 40, 435–451 (1968).
[36] V. Kaladzhyan, C. Bena, and P. Simon, “Asymptotic behavior of impurity-induced bound states in lowdimensional topological superconductors,” Journal of
Physics: Condensed Matter 28, 485701 (2016).
[37] J. Röntynen and T. Ojanen, “Topological superconductivity and high chern numbers in 2d ferromagnetic shiba
lattices,” Phys. Rev. Lett. 114, 236803 (2015).
[38] J. Röntynen and T. Ojanen, “Chern mosaic: Topology

7
of chiral superconductivity on ferromagnetic adatom
lattices,” Phys. Rev. B 93, 094521 (2016).
[39] N. Dai, K. Li, Y.-B. Yang, and Y. Xu, “Topological
quantum phase transitions in metallic shiba lattices,”
Phys. Rev. B 106, 115409 (2022).
[40] J. Ortuzar, S. Trivini, M. Alvarado, M. Rouco, J. Zaldivar, A. L. Yeyati, J. I. Pascual, and F. S. Bergeret,
“Yu-shiba-rusinov states in two-dimensional superconductors with arbitrary fermi contours,” Phys. Rev. B
105, 245403 (2022).
[41] A. Ghazaryan, A. Kirmani, R. M. Fernandes, and
P. Ghaemi, “Anomalous shiba states in topological ironbased superconductors,” Phys. Rev. B 106, L201107
(2022).
[42] H. Schmid, J. F. Steiner, K. J. Franke, and F. von Oppen, “Quantum Yu-Shiba-Rusinov dimers,” Phys. Rev.
B 105, 235406 (2022).
[43] P. Chatterjee, S. Pradhan, A. K. Nandy, and A. Saha,
“Tailoring the phase transition from topological superconductor to trivial superconductor induced by magnetic textures of a spin chain on a p-wave superconductor,” Phys. Rev. B 107, 085423 (2023).
[44] A. Yazdani, B. A. Jones, C. P. Lutz, M. F. Crommie,
and D. M. Eigler, “Probing the local effects of magnetic
impurities on superconductivity,” Science 275, 1767–
1770 (1997).
[45] A. Yazdani, C. M. Howald, C. P. Lutz, A. Kapitulnik,
and D. M. Eigler, “Impurity-induced bound excitations
on the surface of Bi2 Sr2 CaCu2 O8 ,” Phys. Rev. Lett. 83,
176–179 (1999).
[46] A. Yazdani, “Visualizing majorana fermions in a chain
of magnetic atoms on a superconductor,” Physica
Scripta 2015, 014012 (2015).
[47] L. Schneider, P. Beck, T. Posske, D. Crawford, E. Mascot, S. Rachel, R. Wiesendanger, and J. Wiebe, “Topological shiba bands in artificial spin chains on superconductors,” Nature Physics 17, 943–948 (2021).
[48] P. Beck, L. Schneider, L. Rózsa, K. Palotás, A. Lászlóffy,
L. Szunyogh, J. Wiebe, and R. Wiesendanger, “Spinorbit coupling induced splitting of Yu-Shiba-Rusinov
states in antiferromagnetic dimers,” Nature Communications 12, 2040 (2021).
[49] D. Wang, J. Wiebe, R. Zhong, G. Gu, and R. Wiesendanger, “Spin-polarized yu-shiba-rusinov states in an
iron-based superconductor,” Phys. Rev. Lett. 126,
076802 (2021).
[50] L. Schneider, P. Beck, J. Neuhaus-Steinmetz, L. Rózsa,
T. Posske, J. Wiebe, and R. Wiesendanger, “Precursors
of majorana modes and their length-dependent energy
oscillations probed at both ends of atomic shiba chains,”
Nature Nanotechnology 17, 384–389 (2022).
[51] F. Küster, S. Brinker, R. Hess, D. Loss, S. S. P. Parkin,
J. Klinovaja, S. Lounis, and P. Sessi, “Non-majorana
modes in diluted spin chains proximitized to a superconductor,” Proceedings of the National Academy of
Sciences 119, e2210589119 (2022).
[52] R. Lo Conte, M. Bazarnik, K. Palotás, L. Rózsa,
L. Szunyogh, A. Kubetzka, K. von Bergmann, and
R. Wiesendanger, “Coexistence of antiferromagnetism
and superconductivity in Mn/Nb(110),” Phys. Rev. B
105, L100406 (2022).
[53] A. Yazdani, F. von Oppen, B. I. Halperin, and A. Yacoby, “Hunting for majoranas,” Science 380, eade0850
(2023).

[54] M. O. Soldini, F. Küster, G. Wagner, S. Das, A. Aldarawsheh, R. Thomale, S. Lounis, S. S. P. Parkin,
P. Sessi, and T. Neupert, “Two-dimensional shiba
lattices as a possible platform for crystalline topological superconductivity,” Nature Physics (2023),
10.1038/s41567-023-02104-5.
[55] S. Nakosai, Y. Tanaka,
and N. Nagaosa, “Twodimensional p-wave superconducting states with magnetic moments on a conventional s-wave superconductor,” Phys. Rev. B 88, 180503 (2013).
[56] S. S. Pershoguba, S. Nakosai, and A. V. Balatsky,
“Skyrmion-induced bound states in a superconductor,”
Phys. Rev. B 94, 064513 (2016).
[57] G. Yang, P. Stano, J. Klinovaja, and D. Loss, “Majorana bound states in magnetic skyrmions,” Phys. Rev.
B 93, 224505 (2016).
[58] K. Pöyhönen, A. Westström, S. S. Pershoguba, T. Ojanen, and A. V. Balatsky, “Skyrmion-induced bound
states in a p-wave superconductor,” Phys. Rev. B 94,
214509 (2016).
[59] M. Garnier, A. Mesaros, and P. Simon, “Topological superconductivity with deformable magnetic skyrmions,”
Communications Physics 2, 126 (2019).
[60] S. Rex, I. V. Gornyi, and A. D. Mirlin, “Majorana
modes in emergent-wire phases of helical and cycloidal
magnet-superconductor hybrids,” Phys. Rev. B 102,
224501 (2020).
[61] N. Mohanta, S. Okamoto, and E. Dagotto, “Skyrmion
control of majorana states in planar josephson junctions,” Communications Physics 4, 163 (2021).
[62] J. Nothhelfer, S. A. Dı́az, S. Kessler, T. Meng, M. Rizzi,
K. M. D. Hals, and K. Everschor-Sitte, “Steering majorana braiding via skyrmion-vortex pairs: A scalable
platform,” Phys. Rev. B 105, 224509 (2022).
[63] V. Pathak, S. Dasgupta, and M. Franz, “Majorana zero
modes in a magnetic and superconducting hybrid vortex,” Phys. Rev. B 106, 224518 (2022).
[64] P. Chatterjee, S. Banik, S. Bera, A. K. Ghosh, S. Pradhan, A. Saha, and A. K. Nandy, “Topological superconductivity by engineering noncollinear magnetism
in magnet/ superconductor heterostructures: A realistic prescription for 2d Kitaev model,” (2023),
arXiv:2303.03938 [cond-mat.mes-hall].
[65] W. A. Benalcazar, B. A. Bernevig, and T. L. Hughes,
“Quantized electric multipole insulators,” Science 357,
61–66 (2017).
[66] W. A. Benalcazar, B. A. Bernevig, and T. L. Hughes,
“Electric multipole moments, topological multipole moment pumping, and chiral hinge states in crystalline insulators,” Phys. Rev. B 96, 245115 (2017).
[67] Z. Song, Z. Fang, and C. Fang, “(d − 2)-Dimensional
Edge States of Rotation Symmetry Protected Topological States,” Phys. Rev. Lett. 119, 246402 (2017).
[68] J. Langbehn, Y. Peng, L. Trifunovic, F. von Oppen,
and P. W. Brouwer, “Reflection-Symmetric SecondOrder Topological Insulators and Superconductors,”
Phys. Rev. Lett. 119, 246401 (2017).
[69] F. Schindler, A. M. Cook, M. G. Vergniory, Z. Wang,
S. S. Parkin, B. A. Bernevig, and T. Neupert, “Higherorder topological insulators,” Science adv. 4, eaat0346
(2018).
[70] S. Franca, J. van den Brink, and I. C. Fulga, “An
anomalous higher-order topological insulator,” Phys.
Rev. B 98, 201114 (2018).

8
[71] Z. Wang, B. J. Wieder, J. Li, B. Yan, and B. A.
Bernevig, “Higher-Order Topology, Monopole Nodal
Lines, and the Origin of Large Fermi Arcs in Transition Metal Dichalcogenides XTe2 (X = Mo, W),” Phys.
Rev. Lett. 123, 186401 (2019).
[72] M. Ezawa, “Higher-Order Topological Insulators and
Semimetals on the Breathing Kagome and Pyrochlore
Lattices,” Phys. Rev. Lett. 120, 026801 (2018).
[73] D. Călugăru, V. Juričić, and B. Roy, “Higher-order
topological phases: A general principle of construction,”
Phys. Rev. B 99, 041301 (2019).
[74] L. Trifunovic and P. W. Brouwer, “Higher-Order BulkBoundary Correspondence for Topological Crystalline
Phases,” Phys. Rev. X 9, 011012 (2019).
[75] E. Khalaf, “Higher-order topological insulators and superconductors protected by inversion symmetry,” Phys.
Rev. B 97, 205136 (2018).
[76] A. K. Ghosh, G. C. Paul, and A. Saha, “Higher order
topological insulator via periodic driving,” Phys. Rev.
B 101, 235403 (2020).
[77] B. Xie, H. Wang, X. Zhang, P. Zhan, J. Jiang, M. Lu,
and Y. Chen, “Higher-order band topology,” Nat. Rev.
Phys. 3, 520–532 (2021).
[78] L. Trifunovic and P. W. Brouwer, “Higher-order topological band structures,” Phys. Status Solidi B 258,
2000090 (2021).
[79] A. K. Ghosh, T. Nag, and A. Saha, “Systematic generation of the cascade of anomalous dynamical first- and
higher-order modes in floquet topological insulators,”
Phys. Rev. B 105, 115418 (2022).
[80] X. Zhu, “Tunable majorana corner states in a twodimensional second-order topological superconductor
induced by magnetic fields,” Phys. Rev. B 97, 205134
(2018).
[81] T. Liu, J. J. He, and F. Nori, “Majorana corner states
in a two-dimensional magnetic topological insulator on
a high-temperature superconductor,” Phys. Rev. B 98,
245413 (2018).
[82] Z. Yan, F. Song, and Z. Wang, “Majorana corner modes
in a high-temperature platform,” Phys. Rev. Lett. 121,
096803 (2018).
[83] Y. Wang, M. Lin, and T. L. Hughes, “Weak-pairing
higher order topological superconductors,” Phys. Rev.
B 98, 165144 (2018).
[84] Q. Wang, C.-C. Liu, Y.-M. Lu, and F. Zhang, “Hightemperature majorana corner states,” Phys. Rev. Lett.
121, 186801 (2018).
[85] R.-X. Zhang, W. S. Cole, X. Wu, and S. Das Sarma,
“Higher-order topology and nodal topological superconductivity in fe(se,te) heterostructures,” Phys. Rev. Lett.
123, 167001 (2019).
[86] Y. Volpez, D. Loss, and J. Klinovaja, “Second-order
topological superconductivity in π-junction rashba layers,” Phys. Rev. Lett. 122, 126402 (2019).
[87] Z. Yan, “Majorana corner and hinge modes in secondorder topological insulator/superconductor heterostructures,” Phys. Rev. B 100, 205406 (2019).
[88] S. A. A. Ghorashi, X. Hu, T. L. Hughes, and E. Rossi,
“Second-order dirac superconductors and magnetic field
induced majorana hinge modes,” Phys. Rev. B 100,
020509 (2019).
[89] Z. Yan, “Higher-order topological odd-parity superconductors,” Phys. Rev. Lett. 123, 177001 (2019).
[90] Y.-J. Wu, J. Hou, Y.-M. Li, X.-W. Luo, X. Shi,

and C. Zhang, “In-plane zeeman-field-induced majorana
corner and hinge modes in an s-wave superconductor
heterostructure,” Phys. Rev. Lett. 124, 227001 (2020).
[91] K. Laubscher, D. Chughtai, D. Loss, and J. Klinovaja,
“Kramers pairs of majorana corner states in a topological insulator bilayer,” Phys. Rev. B 102, 195401 (2020).
[92] B. Roy, “Higher-order topological superconductors in
P-, T -odd quadrupolar dirac materials,” Phys. Rev. B
101, 220506 (2020).
[93] S.-B. Zhang, W. B. Rui, A. Calzona, S.-J. Choi, A. P.
Schnyder, and B. Trauzettel, “Topological and holonomic quantum computation based on second-order
topological superconductors,” Phys. Rev. Res. 2, 043025
(2020).
[94] J. Ahn and B.-J. Yang, “Higher-order topological superconductivity of spin-polarized fermions,” Phys. Rev.
Res. 2, 012060 (2020).
[95] R. W. Bomantara and J. Gong, “Measurement-only
quantum computation with floquet majorana corner
modes,” Phys. Rev. B 101, 085401 (2020).
[96] A. K. Ghosh, T. Nag, and A. Saha, “Floquet generation of a second-order topological superconductor,”
Phys. Rev. B 103, 045424 (2021).
[97] M. Kheirkhah, Z. Yan, and F. Marsiglio, “Vortex-line
topology in iron-based superconductors with and without second-order topology,” Phys. Rev. B 103, L140502
(2021).
[98] X.-J. Luo, X.-H. Pan, and X. Liu, “Higher-order topological superconductors based on weak topological insulators,” Phys. Rev. B 104, 104510 (2021).
[99] A. K. Ghosh, T. Nag, and A. Saha, “Hierarchy of
higher-order topological superconductors in three dimensions,” Phys. Rev. B 104, 134508 (2021).
[100] B. Roy and V. Juričić, “Mixed-parity octupolar pairing
and corner majorana modes in three dimensions,” Phys.
Rev. B 104, L180503 (2021).
[101] A. K. Ghosh, T. Nag, and A. Saha, “Floquet second order topological superconductor based on unconventional
pairing,” Phys. Rev. B 103, 085413 (2021).
[102] D. Vu, R.-X. Zhang, Z.-C. Yang, and S. Das Sarma,
“Superconductors with anomalous floquet higher-order
topology,” Phys. Rev. B 104, L140502 (2021).
[103] A. K. Ghosh and T. Nag, “Non-hermitian higher-order
topological superconductors in two dimensions: Statics
and dynamics,” Phys. Rev. B 106, L140303 (2022).
[104] A. K. Ghosh, T. Nag, and A. Saha, “Dynamical construction of quadrupolar and octupolar topological superconductors,” Phys. Rev. B 105, 155406 (2022).
[105] X.-H. Pan, X.-J. Luo, J.-H. Gao, and X. Liu, “Detecting and braiding higher-order majorana corner states
through their spin degree of freedom,” Phys. Rev. B
105, 195106 (2022).
[106] A. K. Ghosh, T. Nag, and A. Saha, “Time evolution of majorana corner modes in a floquet second-order
topological superconductor,” Phys. Rev. B 107, 035419
(2023).
[107] K. H. Wong, M. R. Hirsbrunner, J. Gliozzi, A. Malik, B. Bradlyn, T. L. Hughes, and D. K. Morr,
“Higher order topological superconductivity in magnetsuperconductor hybrid systems,” npj Quantum Materials 8, 31 (2023).
[108] B. A. Bernevig, T. L. Hughes, and S.-C. Zhang, “Quantum spin hall effect and topological phase transition in
hgte quantum wells,” Science 314, 1757–1761 (2006).

9
[109] M. König, S. Wiedmann, C. Brüne, A. Roth, H. Buhmann, L. W. Molenkamp, X.-L. Qi, and S.-C. Zhang,
“Quantum spin hall insulator state in hgte quantum
wells,” Science 318, 766–770 (2007).
[110] Supplemental Material at XXXXXXXXXXX for the
derivation of the effective Hamiltonian, low-energy edge
theory, derivation of the effective bulk pairings, effects due to asymmetry of the spin texture and Rashba
spin-orbit coupling, and emergence of Majorana corner
modes in disc and triangular geometry.
[111] W. A. Wheeler, L. K. Wagner, and T. L. Hughes,
“Many-body electric multipole operators in extended
systems,” Phys. Rev. B 100, 245135 (2019).
[112] B. Kang, K. Shiozaki, and G. Y. Cho, “Many-body
order parameters for multipoles in solids,” Phys. Rev.
B 100, 245134 (2019).
[113] C.-A. Li, B. Fu, Z.-A. Hu, J. Li, and S.-Q. Shen,
“Topological phase transitions in disordered electric
quadrupole insulators,” Phys. Rev. Lett. 125, 166801
(2020).
[114] R. Hess, H. F. Legg, D. Loss, and J. Klinovaja, “Prevalence of trivial zero-energy subgap states in nonuniform
helical spin chains on the surface of superconductors,”
Phys. Rev. B 106, 104503 (2022).
[115] L. Fu and C. L. Kane, “Topological insulators with inversion symmetry,” Phys. Rev. B 76, 045302 (2007).
[116] R. Jackiw and C. Rebbi, “Solitons with fermion number
1
,” Phys. Rev. D 13, 3398–3409 (1976).
2
[117] M. Sato, Y. Takahashi, and S. Fujimoto, “Non-abelian
topological order in s-wave superfluids of ultracold
fermionic atoms,” Phys. Rev. Lett. 103, 020401 (2009).
[118] M. Sato, Y. Takahashi, and S. Fujimoto, “Non-abelian
topological orders and majorana fermions in spin-singlet
superconductors,” Phys. Rev. B 82, 134521 (2010).
[119] H. Hu, I. I. Satija, and E. Zhao, “Chiral and counterpropagating majorana fermions in a p-wave superconductor,” New Journal of Physics 21, 123014 (2019).
[120] P. Wang, S. Lin, G. Zhang, and Z. Song, “Topological gapless phase in kitaev model on square lattice,”
Scientific Reports 7, 17179 (2017).
[121] K. L. Zhang, P. Wang, and Z. Song, “Majorana flat
band edge modes of topological gapless phase in 2d Kitaev square lattice,” Scientific Reports 9, 4978 (2019).
[122] A. K. Nandy, N. S. Kiselev, and S. Blügel, “Interlayer exchange coupling: A general scheme turning chiral magnets into magnetic multilayers carrying atomicscale skyrmions,” Phys. Rev. Lett. 116, 177202 (2016).
[123] D. M. Eigler and E. K. Schweizer, “Positioning single
atoms with a scanning tunnelling microscope,” Nature
344, 524–526 (1990).
[124] H. Kim, A. Palacio-Morales, T. Posske, L. Rózsa,
K. Palotás, L. Szunyogh, M. Thorwart, and R. Wiesendanger, “Toward tailoring majorana bound states in artificially constructed magnetic atom chains on elemental
superconductors,” Science Advances 4, eaar5251 (2018).
[125] L. Schneider, S. Brinker, M. Steinbrecher, J. Hermenau,
T. Posske, M. dos Santos Dias, S. Lounis, R. Wiesendanger, and J. Wiebe, “Controlling in-gap end states by
linking nonmagnetic atoms and artificially-constructed
spin chains on superconductors,” Nature Communications 11, 4707 (2020).
[126] S. Nadj-Perge, I. K. Drozdov, J. Li, H. Chen, S. Jeon,
J. Seo, A. H. MacDonald, B. A. Bernevig, and A. Yazdani, “Observation of majorana fermions in ferromag-

netic atomic chains on a superconductor,” Science 346,
602–607 (2014).

i

Supplemental material for “Second-order topological superconductor via noncollinear
magnetic texture”
Pritam Chatterjee ID 1,2 , Arnob Kumar Ghosh ID 1,2,3 , Ashis K. Nandy ID 4 , and Arijit Saha ID 1,2
1

Institute of Physics, Sachivalaya Marg, Bhubaneswar-751005, India
Homi Bhabha National Institute, Training School Complex, Anushakti Nagar, Mumbai 400094, India
3
Department of Physics and Astronomy, Uppsala University, Box 516, 75120 Uppsala, Sweden
4
School of Physical Sciences, National Institute of Science Education and Research, An OCC of Homi Bhabha National
Institute, Jatni 752050, India
2

In the supplementary material (SM), we provide detailed explanations in different sections. In Sec. S1, we explore the
derivation of the effective Hamiltonian, which provides us with analytical insights into our numerical results. Moving
to Sec. S2, we establish a low-energy edge theory based on our effective continuum model. Sec. S3 is dedicated to
deriving effective superconducting pairings in the bulk. Sec. S4 and Sec. S5 are devoted to the discussion of the effects
of the asymmetry of the spin texture and Rashba spin-orbit coupling (SOC), respectively, on our setup. Finally, we
discuss the emergence of Majorana corner modes (MCMs) in disc and triangular geometry in Sec. S6.
S1.

DERIVATION OF THE EFFECTIVE HAMILTONIAN

In this section, we outline the method used to derive an effective Hamiltonian, Heff , the Eq.(4) in the main text,
from the low-energy continuum form of our lattice model H i.e., the Eq.(1) in the main text. In particular, we
make use of the low-energy Hamiltonian HL as stated in Eq. (3) of the main text, and upon replacing (kx , ky ) with
(−i∇x , −i∇y ), it assumes the form:
HL = ξΓ1 + ∆0 Γ2 + 2λx kx Γ5 + 2λy ky Γ6 + Jex S(r).s ,

(S1)

where, Γ1 = τz σz s0 , Γ2 = τxσ0 s0 , Γ3 = τ0 σ0 sx , Γ4= τ0 σ0 sy , Γ5 = τz σx sz , Γ6 = τz σy s0 , Γ7 = τz σz sz , Γ8 = τz σx s0 ,
and Γ9 = τz σy sz . Here, ξ = ϵ0 − 4t − t(▽2x + ▽2y ) . To obtain the effective continuum Hamiltonian, we introduce a
i
unitary transformation U = τ0 σ0 e− 2 ϕ(r)σz , such that H̃eff = U † HU [64, 114]. Hence, H̃eff reads as
"

2

 #
X
1 ∂ϕ
1
∂ϕ
∂ϕ
2
∇ ri −
H̃eff = − t
−
i
∇r + i∇ri
sz σz τz + (ϵ0 − 4t)Γ1 + ∆0 Γ2 + Jex Γ3 + 2λx kx Γ5
4 ∂ri
2 ∂ri i
∂ri
ri =x,y
 
 
∂ϕ
∂ϕ
Γ8 − λy
Γ9 .
(S2)
+ 2λy ky Γ6 − λx
∂x
∂y
The effective Hamiltonian Heff takes on a specific form due to the presence of the 2D noncollinear spin texture defined
as ϕ(x, y) = g.r = gx x + gy y. As a result, the form of Heff becomes:
t
Heff =ξkeff Γ1 + ∆0 Γ2 + Jex Γ3 + 2λx kx Γ5 + 2λy ky Γ6 − (g · k)Γ7 − λx gx Γ8 − λy gy Γ9 .
2
The basis in which we perform our analysis is denoted as,
n
oT
Ψk = ck,a,↑ , ck,a,↓ , ck,b,↑ , ck,b,↓ , −c†−k,a,↓ , c†−k,a,↑ , −c†−k,b,↓ , c†−k,b,↑
.

S2.

(S3)

(S4)

LOW-ENERGY EDGE THEORY FROM THE EFFECTIVE MODEL

Here, we elaborate on the process of developing the low-energy edge theory follwoing Refs. [82, 90, 96] based on
our effective continuum model presented in Eq. (S3). We have examined the edges labeled as I and II, as illustrated
in Figure 1 of the main text.
A.

Hamiltonian for edge-I

For edge-I, we apply periodic boundary condition (PBC) along the y-direction and open boundary condition (OBC)
along the x-direction, resulting in the substitution of kx with −i∂x in the analysis. We divide the original Hamiltonian

ii
Heff into two terms: Heff = H0 (−i∂x ) + Hp (ky , g, Jex , ∆0 ), considering Hp as a perturbation to H0 . By neglecting ky2
term in H0 , we obtain:
H0 =(ϵ′ − t∂x2 )Γ1 − 2iλx ∂x Γ5 + i
Hp =2λy ky Γ6 −

tgx
∂x Γ7 ,
2

tgy
ky Γ7 + ∆0 Γ2 + Jex Γ3 − λx gx Γ8 − λy gy Γ9 ,
2

(S5)



where ϵ′ = ϵ0 − 4t + 4t (gx2 + gx2 ) . Assuming the impact of Hp on H0 to be small, we solve H0 exactly and treat Hp as
a perturbation. The trial solution for H0 is assumed to be Ψα (x) = eγx χα , satisfying H0 Ψα = 0 for the zero-energy
states. Here, γ is a complex quantity mimicking complex wave-vector and χα represents eight-component spinors, see
below. Therefore, the secular equation reads,


tgx
′
2
det (ϵ − tγ )Γ1 − 2iλx γΓ5 + i
γΓ7 = 0 .
(S6)
2
Employing the boundary condition Ψα (0) = Ψα (∞) = 0, the γα and χα reads as
p




−igx′ t + 2λx + −(gx′ t + 2iλx )2 + 4tϵ′
λx
gx′
γ1 = −
= − α̃ +
− i β̃ −
,
2t
t
2
p




ig ′ t − 2λx + −(gx′ t + 2iλx )2 + 4tϵ′
λx
g′
= α̃ −
+ i β̃ + x ,
γ2 = x
2t
t
2
p




′
′
2
′
ig t + 2λx + −(gx t − 2iλx ) + 4tϵ
λx
g′
= − α̃ +
+ i β̃ − x ,
γ3 = − x
2t
t
2
p




′
′
′
2
′
−igx t − 2λx + −(gx t − 2iλx ) + 4tϵ
λx
g
γ4 =
= α̃ −
− i β̃ + x ,
2t
t
2

(S7)

 ′ 2
p
p
′
λ2
g
where gx′ = g2x , α̃ = α2 + β 2 cos(θ/2), and β̃ = α2 + β 2 sin(θ/2); with α = ϵt + t2x − 2x , β = gxtλx , and


gx λx
θ = 2 tan−1
. The corresponding normalized spinors can be written as
′2 t
gx
λ2
x
ϵ′ −

4

+ t




1
 0
 
−i

1
 0
χ1 =   ,
2  1
 0
 
−i
0




0
 1
 
 0

1
−i
χ2 =   ,
2  0
 1
 
 0
−i

 
0
1
 
0

1
 i
χ3 =   ,
2 0
1
 
0
i

 
1
0
 
 i

1
0
χ4 =   .
2 1
0
 
 i
0

As a result, the matrix elements of Hp using the aforementioned basis states are:
Z ∞
I,Edge
Hαβ
=
dx Ψ†α (x)Hp Ψβ (x) .

(S8)

(S9)

0

We hence obtain the Hamiltonian for edge-I as,
HI = −2λy ky σx sz + ∆0 σz s0 + 2λy gy′ σx s0 .

(S10)

Using a similar approach, the Hamiltonian for edge-III can be derived as follows:
HIII = −2λy ky σx sz + ∆0 σz s0 + 2λy gy′ σx s0 .
B.

(S11)

Hamiltonian for edge-II

To derive the Hamiltonian for edge-II, we utilize PBC (OBC) along the x- (y)-direction, while also substituting ky
with −i∂y in the calculation (see also the main text). We now rewrite Heff as Heff = H0 (−i∂y ) + Hp (kx , g, Jex , ∆0 )

iii
and neglect the kx2 term. Thus, we obtain
H0 =(ϵ′ − t∂y2 )Γ1 − 2iλy ∂y Γ6 + i
Hp =2λx kx Γ5 −

tgx
∂y Γ7 ,
2

tgx
kx Γ7 + ∆0 Γ2 + Jex Γ3 − λx gx Γ8 − λy gy Γ9 .
2

(S12)

Assuming the trial solution of the Hamiltonian H0 as Ψα = eγy χα and focusing on the zero-energy solution, we
consider H0 Ψα = 0. Thus, the secular equation reads


tgx
det (ϵ′ − tγ 2 )Γ1 − 2iλy γΓ6 + i
γΓ7 = 0 .
(S13)
2
Employing the boundary condition Ψα (0) = Ψα (∞) = 0, we obtain the γα and χα as
q




−igy′ t + 2λy + −(gy′ t + 2iλy )2 + 4tϵ′
gy′
λy
γ1 = −
= − α̃ +
− i β̃ −
,
2t
t
2
q




igy′ t − 2λy + −(gy′ t + 2iλy )2 + 4tϵ′
gy′
λy
γ2 =
= α̃ −
+ i β̃ +
,
2t
t
2
q




igy′ t + 2λy + −(gy′ t − 2iλy )2 + 4tϵ′
gy′
λy
= − α̃ +
+ i β̃ −
,
γ3 = −
2t
t
2
q




−igy′ t − 2λy + −(gy′ t − 2iλy )2 + 4tϵ′
gy′
λy
= α̃ −
− i β̃ +
,
γ4 =
2t
t
2

(S14)

 ′ 2
p
p
′
λ2
g
g
g λ
where gy′ = 2y , α̃ = α2 + β 2 cos(θ/2), and β̃ = α2 + β 2 sin(θ/2); with α = ϵt + t2y − 2y , β = yt y , and


gy λy
. The corresponding normalized spinors reads
θ = 2 tan−1
′2
2
gy t
λy
ϵ′ −

4

+ t

 
1
0
 
1

1
0
χ1 =   ,
2 1
0
 
1
0


1
 0
 
 1

1
 0
χ2 =   ,
2 −1
 0
 
−1
0


 
0
1
 
0

1
1
χ3 =   ,
2 0
1
 
0
1


0
 1
 
 0

1
 1
χ4 =   .
2  0
−1
 
 0
−1


Therefore, the matrix elements of Hp employing the above basis states can be written as,
Z ∞
II,Edge
Hαβ
=
dy Ψ†α (y)Hp Ψβ (y) .

(S15)

(S16)

0

Therefore, we obtain the Hamiltonian for edge-II as,
HII = 2λx kx σx sz + ∆0 σz s0 + Jex σ0 sx − 2λx gx′ σx s0 .

(S17)

In a similar fashion, one obtains the Hamiltonian for edge-IV as,
HIV = 2λx kx σx sz + ∆0 σz s0 + Jex σ0 sx − 2λx gx′ σx s0 .

(S18)

So, the Hamiltonians for all four edges are as follows:
HI = − 2λy ky σx sz + ∆0 σz s0 + 2λy gy′ σx s0 ,
HII =2λx kx σx sz + ∆0 σz s0 + Jex σ0 sx − 2λx gx′ σx s0 ,
HIII = − 2λy ky σx sz + ∆0 σz s0 + 2λy gy′ σx s0 ,
HIV =2λx kx σx sz + ∆0 σz s0 + Jex σ0 sx − 2λx gx′ σx s0 .

(S19)

iv
C.

Condition for sign change of the mass gaps between the two edges

We can compute the eigenvalues of the edge Hamiltonians HI in Eq. (S10) and HII in Eq. (S17) at ky = 0 and
kx = 0, respectively, leading to the following results:
q
q
q
o
n q
∆20 + gy2 λ2y , ∆20 + gy2 λ2y ,
EI = − ∆20 + gy2 λ2y , − ∆20 + gy2 λ2y ,


q
q
q
q
EII = −Jex − ∆20 + gx2 λ2x , −Jex + ∆20 + gx2 λ2x , Jex − ∆20 + gx2 λ2x , Jex + ∆20 + gx2 λ2x .
(S20)
For a non-zero value of ∆0 , gp
y , and λy , edge-I Hamiltonian always exhibits a gap at ky = 0. However, for edge-II, one
can close the gap for Jex = | ∆20 + gx2 λ2x |. Thus, comparing the eigenvalues determined from HI and HII , we obtain
the condition for sign change of the mass gap between the two adjacent or crossing edges as
q
g 2 λ2 + ∆20 > Jex .
(S21)
Here, we consider gx = gy = g and λx = λy = λ for simplicity. Hence, as per the Jackiw-Rebbi theory [116], we
identify the emergence of localized Majorana zero modes at the corners of the system (MCMs), indicating the presence
of a second-order topological superconducting phase.
S3.

DERIVATION OF THE EFFECTIVE PAIRING

In the following section, we present the derivation of the effective pairings in the bulk as discussed in the main text.
We begin by reexpressing the effective Hamiltonian Heff in Eq. (S3) as,
 eff

ξk σz s0 + f˜(k) + Jex σ0 sx
∆0 σ0 s0
Heff =
,
(S22)
∆0 σ0 s0
−ξkeff σz s0 − f˜(k) + Jex σ0 sx
2
terms.
where, f˜(k) = 2λx kx σx sz + 2λy ky σy s0 − λx gx σx s0 − λy gy σy sz − 2t (g · k)σz sz . Here, we have neglected the kx,y
We have derived a “dual” Hamiltonian which is unitary equivalent
to
the
H
[117,
118].
The
duality
transformation
is
eff


1
−1
facilitated by the unitary operator, UD = τ̃ σ0 s0 , where τ̃ = √12
. The matrix τ̃ obeys the following relations,
1 1

τ̃ † τz τ̃ = − τx
τ̃ † τx τ̃ =τz .
After the transformation, the dual Hamiltonian H̃D (k) is expressed as:


˜D
ϵ̃D + Jex σ0 sx
∆
†
,
H̃D (k) = UD Heff UD =
˜D
∆
−ϵ̃D + Jex σ0 sx

(S23)

(S24)

˜ D = −ξ eff σz s0 − f˜(k). Here, ϵ̃D represents the kinetic term and the off-diagonal element
where, ϵ̃D = ∆0 σ0 s0 and ∆
k
˜
∆D denotes the effective pairings that we have discussed in the main text. However, the diagonal kinetic term ϵ̃D
˜ D , it is evident that the SOC terms
is independent of momenta. Nevertheless, from the off-diagonal pairing term ∆
undergo a transformation into px + ipy -type superconducting pairing proportional to λx,y . On the other hand, the
SOC generated via the noncollinear magnetic textures transforms into a px + py -type pairing that scales with gx,y .
S4.

IMPACT OF THE ROTATIONAL ASYMMETRY

In this section, we discuss the effect of asymmetry of the spin spiral (gx ̸= gy ) and intrinsic SOC (λx ̸= λy ) on
the SOTSC phase. It is crucial to note that rotational symmetries are not essential to obtain the SOTSC phase
hosting MCMs in our system. As a result, even if we consider asymmetry either in gx and gy or λx and λy the
system still exhibits four MCMs at energy E = 0. In Fig. S1(a), Fig. S1(b), and Fig. S1(c), we present the eigenvalue
spectrum and the corresponding local density of states (LDOS) for three distinct cases: (a) gx ̸= gy , λx = λy , (b)
gx = gy , λx ̸= λy and (c) gx ̸= gy , λx ̸= λy . Notably, in all of these cases, we consistently observe the presence of four
Majorana corner modes at energy E = 0.

v

FIG. S1. Panels (a), (b), and (c) correspond to the eigenvalue spectrum and the corresponding LDOS for three different
scenarios. In panel (a), we consider gx = 0.2, gy = 0.3, and λx = λy = 0.5. In panel (b), we take gx = gy = 0.2, and λx = 0.5,
λy = 0.8. Finally, in panel (c), we choose gx = 0.2, gy = 0.3, and λx = 0.5, λy = 0.8. The rest of the model parameters remain
the same as mentioned in the main text: Jex = 0.8, ∆0 = 0.4, ϵ0 = 1.
S5.

EFFECT OF RASHBA SPIN-ORBIT COUPLING

This section is devoted to the discussion of the effect of external Rashba SOC on SOTSC phase. In our theoretical
setup, we propose a quantum spin hall insulating (QSHI) layer on top of a 2D non-collinear magnetic texture. In
particular, the QSHI layer of our setup possesses an intrinsic SOC while the non-collinear magnetic texture (spin
spiral) can generate another effective SOC. Therefore, SOTSC hosting MCMs are stabilized due to the interplay
between these two types of SOC. Hence, we do not need any Rashba SOC to obtain the SOTSC. However, we here
present a qualitative study of our problem in the presence of external Rashba SOC to examine the stability of the
SOTSC phase. Therefore, the Hamiltonian in Eq. (1) of the main text, in the presence of Rashba SOC, is modified
to,

FIG. S2. We illustrate the eigenvalue spectrum and the corresponding LDOS with the Rashba SOC strength aR = 0.5. The
rest of the model parameter values remain the same as mentioned in the main text: Jex = 0.8, ∆0 = 0.4, ϵ0 = 1, gx = gy = 0.2
and λx = λy = 0.5.

H=

X †
ci,j {ϵ0 Γ1 + ∆0 Γ2 + Jex (Γ3 cos ϕij + Γ4 sin ϕij )} ci,j
i,j

n
aR o
ci+1,j
− c†i,j tΓ1 + iλx Γ5 − i ΓR
2 5o
n
a
R
− c†i,j tΓ1 + iλy Γ6 + i ΓR
ci,j+1 + h.c. ,
2 6

(S25)

vi
where, the lattice site indices i and j runs along x- and y-direction, respectively and the Γ matrices (8×8) are given as
Γ1 =τz σz s0 , Γ2 =τx σ0 s0 , Γ3 =τ0 σ0 sx , Γ4 =τ0 σ0 sy , Γ5 =τz σx sz , Γ6 =τz σy s0 , Γ7 =τz σ0 sy , and Γ8 =τz σ0 sx . The three Pauli
matrices σ, s and τ act on orbital (a, b), spin (↑, ↓), and particle-hole degrees of freedom, respectively. The symbol
λR represents the strength of the Rashba SOC, and the rest of the symbols carry the same meaning as mentioned in
the main text. In Fig. S2, we depict the eigenvalue spectrum and the corresponding LDOS using Eq. (S25) choosing
a moderate value of the Rashba SOC strength. We still obtain the SOTSC phase hosting MCMs at E = 0 for λR ̸= 0.
Thus, the presence of Rashba SOC does not modify the presence of MCMs in our system. Therefore, we can conclude
that in the presence of Rashba SOC, we can’t expect any new physics. Instead, the Rashba SOC term aR merely can
lead to a renormalization of certain topological regime.

S6.

MCMS IN DISC AND TRIANGULAR GEOMETRY

Finally, in this section of the SM, we present our findings for both circular disc and triangular geometries based on
our lattice model [Eq. (1) in the main text]. In Fig. S3(a), we illustrate the LDOS and the corresponding eigenvalue
spectrum (inset) for the circular disc geometry. In Figs. S3(b) and (c), we demonstrate the same employing triangular
geometry for two different orientations. It is evident that zero-dimensional localized MCMs emerge in the LDOS
spectrum at E = 0 supported by the eigenvalue spectra. Notably, the critical distinction between the two geometries
lies in the number of MCMs: the disc geometry supports four corner modes [see Fig. S3(a)] while the triangular
setup only exhibits two corner modes [Figs. S3(b) and (c)] [90, 93]. Interestingly, the position of these corner modes
depends on the orientations of the triangle. This has also been shown in other models of SOTSC [90, 93]. Therefore,
our results affirm that higher-order topology remains consistent irrespective of the system’s geometric configuration.

1.0

30

1.0

30

En

0.00

−0.05
3595

0.5
3600

Ly

En

1

Lx

0.5

0.00

−0.05
3595

3605

3600

Ly

En

30

0

1
1

Lx

0.5

0.00

−0.05
3595

3605

n

n

1

0.05

0.05

0.05

Ly

1.0

30

3600

3605

n

30

0

1
1

Lx

30

0

FIG. S3. In panel (a), we show the LDOS associated with E = 0, for circular disc geometry. In panels (b) and (c), we showcase
the same employing triangular geometry with two different orientations. In the insets, we depict the eigenvalue spectra for
the corresponding geometries highlighting the E = 0 localized MCMs. We assume all the model parameters remain same as
mentioned in the main text i.e., for the square geometry: Jex = 0.8, ∆0 = 0.4, ϵ0 = 1.0, λx = λy = 0.5, gx = gy = 0.2, and
t = 1.0.

