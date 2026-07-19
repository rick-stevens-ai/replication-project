<!-- extraction: pdftotext | arxiv:2408.04017 -->
Shift photocurrent vortices from topological polarization textures
Aneesh Agarwal,1, ∗ Wojciech J. Jankowski,1 Daniel Bennett,2 and Robert-Jan Slager1, 3, †
Theory of Condensed Matter Group, Cavendish Laboratory, University of Cambridge, J. J. Thomson Avenue, Cambridge CB3 0HE, UK
2
John A. Paulson School of Engineering and Applied Sciences, Harvard University, Cambridge, Massachusetts 02138, USA
3
Department of Physics and Astronomy, University of Manchester, Oxford Road, Manchester M13 9PL, UK
(Dated: May 28, 2025)
Following the recent interest in van der Waals (vdW) ferroelectrics, topologically nontrivial polar structures
have been predicted to form in twisted bilayers. However, these structures have proven difficult to observe experimentally. We propose that these textures may be probed optically by showing that topological polarization
textures result in exotic nonlinear optical responses. We derive this relationship analytically using non-Abelian
Berry connections and a quantum-geometric framework, supported by tight-binding and first-principles calculations. For the case of moiré materials without centrosymmetry, which form networks of polar merons and
antimerons, the shift photoconductivity forms a vortex-like structure in real space. For a range of frequencies
where transitions between topologically trivial bands occur at the Brillouin zone edge, the shift photocurrents
are antiparallel to the in-plane electronic polarization field. Our findings highlight the interplay between complex polarization textures and nonlinear optical responses in vdW materials and provide a sought-after strategy
for their experimental detection.

Introduction.—Twisting layered van der Waals (vdW) materials to form interference patterns known as moiré superlattices [1, 2] offers a broad platform for realizing exotic physical phenomena, including superconductivity [3], correlated
[4, 5] and fractional [6–8] Chern insulators, and the appearance and manipulation of magnetic [9–12] and polar [13–
19] order in two-dimensional (2D) systems. In particular,
stacking-engineering of vdW materials has been shown to
result in ferroelectricity with state-of-the-art performance in
nanoscale devices [14, 20, 21]. Introducing a relative twist in
vdW ferroelectrics results in the formation of a regular network of moiré polar domains (MPDs) [17–19], the origin of
which has been attributed to the symmetry-breaking of the different stacking arrangmenents in a moiré superlattice [22–24].
This symmetry breaking also gives rise to in-plane polarization textures in the MPDs, giving them topological character [25, 26] and providing a new platform to induce band
topology [27, 28]. In this regard it was recently shown that
the real space topology of polar textures is compatible with
non-trivial band topology [29]. While similar polar topological textures have been observed in oxide perovskites [30–33],
this is the first such prediction in vdW materials, and in a 2D
system (less than 1 nm thick). The topological character of
the MPDs has recently been confirmed in twisted WSe2 using
piezoresponse force microscopy (PFM) [34]. Understanding
the physical consequences of polar topological structures in
moiré materials, namely how they influence other materials
properties, may lead to advances in nanotechnology, and may
also reveal new ways to detect these exotic structures experimentally. The advancement of this new direction in nanotechnology hinges on identifying physical observables to harbor
and manipulate these exotic states.
Optical measurements constitute one of the key tools for
experimentally probing new physical effects, with many intriguing optical signatures [35] being reported, most recently

∗ aa2223@cam.ac.uk

† rjs269@cam.ac.uk

Light
AA

Stacking x(r)
AB/BA

DW

j(r)
Shift Current

Ek

arXiv:2408.04017v2 [cond-mat.mes-hall] 26 May 2025

1

~ω

k

Q = − 12

Q = + 12
Polarization P(r)

FIG. 1: Photocurrent response from polarization textures.
A polar moiré material is shown, in which a network of
stacking domains forms. The high symmetry stackings, AA,
AB/BA and DW are sketched above. The stacking domains
have topologically nontrivial polarization, forming a network
of merons and antimerons (winding numbers Q = ± 21 ),
sketched below. Illuminating the sample results in an inhomogeneous shift photocurrent, caused by the shift of Wannier
centers between the valence and conduction bands, sketched
below.
in moiré materials [36–41]. In particular, nonlinear optical
effects [42, 43] such as the shift response [35, 42, 44, 45],
which yield polarization currents due to photoinduced shifts
of electronic charge centers, can result in bulk DC responses:
the generation of these DC currents from light-induced excitations is of interest for photovoltaic applications [46–48]. The
theory of optical responses of topological states has recently
renewed [49–51] interest in relations with quantum geometry [52]. The geometry of quantum states can be described
in terms of the quantum geometric tensor (QGT) that encodes

2
non-Abelian, i.e., multiband, Berry connections [53] and their
derivatives [52]. Apart from many relations to a diverse set
of physical observables that range from superfluid densities to
wavefucntion spreading, the QGT describes dipole transitions
and hence is a useful quantity for capturing topological optical
responses at linear and non-linear orders [49, 51].
In this work, we uncover an intriguing interplay between
topological polar structures [25, 26] and the optical and geometric properties of moiré materials [54] that host topologically trivial bands, see Fig. 1. We discover a definite optical signature for the topological character of polar domains
in moiré materials in the absence of centrosymmetry. Our
findings can be described with a quantum-geometrical framework [51], using its relation to the polarization carried by the
Wannier charge centers [42], see Fig. 1. We illustrate these
findings using tight-binding and first-principles calculations,
using bilayer hexagonal boron nitride (hBN) as an example of
a prototypical vdW ferroelectric, although our results are applicable to a wide variety of vdW materials such as transition
metal dichalcogenides (TMDs).
Results.—The electronic polarization in a 2D crystal is
given by [55–57]
P=−

e
(2π)2

Z

BZ

d2 k

occ
X

fn,k Ann ,

(1)

n

in terms of the diagonal elements of the non-Abelian Berry
connection Anm = i un,k ∇k um,k , integrated over the Brillouin zone (BZ), where un,k are the cell-periodic parts of the
Bloch states. e is an elementary charge and fn,k denotes a
temperature-dependent occupation factor given by the FermiDirac distribution. To describe shift currents, we define the
‘shift vectors’
Ramn ≡ Amm − Ann − i∇k Arg (Aamn ) ,

(2)

which, if the last term is negligible and the a index is omissible, can be thought of as the change in electronic polarization
induced by a photoexcitation (see Methods). The shift photoconductivity σ in response to linearly polarized light is given
by [42, 43, 51]
Z
d2 k
2πe3 X
a 2
c,aa
δ(ω − ωmn ) fnm,k Rc,a
σ (ω) = − 2
mn |Amn | ,
ℏ m,n BZ (2π)2
(3)
where fnm,k = fn,k − fm,k , n (m) denotes a band with energy
En,k (Em,k ), and ωmn ≡ (Em,k − En,k )/ℏ are the frequencies of
optical transitions. The shift photocurrent j is then given
by [42, 43]
j c = 2σc,aa (ω)E a (ω)E a (−ω) ,

(4)

where E a (ω) are the components of an AC electric field of
incident light with frequency ω and Einstein summation convention is assumed.
It was recently proposed that shift currents can be used as
an experimental diagnostic tool for quantum geometry in twodimensional materials [58], and can have nontrivial spatial dependence in supercells such as moiré superlattices, forming

complex structures such as vortices [59]. We propose that the
vortices in the shift current are a direct result of the topological polarization textures that form in these materials: a consequence of the interplay between polarization and shift currents [60, 61].
In materials such as bilayer hBN or TMDs, twisting about
the artificial rhombohedral (parallel) stacking results in a network of MPDs formed by the stacking domains [22–24]. The
supercell consists of four distinct regions: the non-polar AA
stackings, which are energetically unstable but pinned by the
geometry of the superlattice, the AB/BA domains, which are
energetically favorable and have maximum out-of-plane polarization, and the domain walls (DWs) [25, 62], which act
as solitons separating the AB and BA domains. These stackings are sketched in Fig. 1 for bilayer hBN. The MPDs also
have an in-plane polarization texture, which is largest along
the domain walls, see Fig. 2 (a). The dominant contribution
of the Berry connection to the in-plane polarization occurs at
the edge of the BZ, see Fig. 2 (b). Combining the in-plane and
out-of-plane components, the polarization field exhibits topologically nontrivial winding, forming a network of merons
and anti-merons, with winding numbers Q = ± 21 [25, 26].
The winding numbers Q can be calculated by integrating the
local winding of the normalized polarization [26] on a discretized grid (see SI), following the methodology described in
Ref. [25]. The topological index, i.e. the wrapping number
Q, is exactly (half-)quantized, as the local polarization cannot wind across a moiré domain in an arbitrary way, given the
stacking symmetries of the moiré crystal and because of the
periodicity of the supercells.
We observe that the shift photoconductivity vector field, defined as
" x,xx
#
σ (r) + σ x,yy (r)
σ(r) = y,xx
,
(5)
σ (r) + σy,yy (r)
directly coincides with the in-plane polarization field. Combining the responses to both x- and y-polarized electric fields
allows for an analytical averaging of the shift vectors over all
sections of the BZ where optical transitions are dominant (see
SI for additional details). Since the averaged shift vectors
Rmn reflect the local electronic polarization, the components
of σ(r) serve as a probe for the local polarization components,
provided that the optical transition matrix elements are comparable in regions of the BZ that contribute most to the electronic polarization.
We illustrate the correspondence between polarization textures and shift photoconductivity textures using a tightbinding (TB) model of twisted bilayer hBN (t-hBN). The
model consists of four bands, representing the two valence
(conduction) bands closest to the Fermi level, of 2pz character on the N (B) atoms in each layer (see Methods). The local polarization and shift conductivity are calculated using the
configuration space method, under the approximation that for
small twist angles (large supercells), the local stacking order
changes slowly and smoothly, and local environments are well
described by a relative shift between two commensurate layers [25, 26, 63]. The shift photoconductivity vector is shown
in Fig. 2 (c), at a frequency of ωM = 6 eV, roughly corre-

3

(a)

(b)
0.5

0.4
0.4

0.3

0.3

AA

BA
DW

Γ

0.2

K

0.1

AB

(c)

M

0.2

K0

0.1

(d)
8

1.5

6
1.0

AA

Γ

4

BA
0.5

DW

2

AB
0

K

M

K0
0.0

FIG. 2: Polarization and shift photocurrent in twisted boron nitride. (a) In-plane polarization of t-hBN contributed by
electrons. The axes labels x x and xy are the components of the stacking vector x. The polarization texture was obtained using
Eq. (1) with Berry connections calculated from the wavefunctions obtained by diagonalizing the four-band TB model (see
Methods) and using parametrizations detailed in SI. (b) Trace of the Berry connection in momentum-space over occupied bands,
evaluated for the DW stacking. The dominant contribution to the polarization occurs around the M points on the BZ edge. (c)
Plot of the shift photoconductivity vector σ(r) in real space. The photoconductivities are evaluated at a transition energy of
ωM = 6 eV, and are antiparallel to the in-plane polarization. The shift vortex features are stable for a range of frequencies
around ωM (see SI). (d) Trace of the QGT over spatial indices, summed over all interband transitions (for the DW stacking).
The dominant QGT contributions arise from the regions with enhanced Ann (k) (near M points), which fortifies the shift currentelectric polarization correspondence near ωM .
sponding to the resonant transitions at the M point of the BZ.
We note that σ(r) is exactly antiparallel to P(r): the current
flows out of (into) the AB (BA) domains, has largest magni-

tude along the domain walls, and forms vortices around the
AA stacking regions. This correspondence is most strongly
observed within a range of light frequencies where the reso-

4

(a)
σ (ω) (µA Å/V2 )

(b)

AA

30

ωK

20

ωM

10

(c)

AB

y, yy
y, xx
y, xy
x, xy

DW

ωM y, yy
y, xx
y, xy
x, xy

ωK

ωM y, yy

ωK

y, xx
y, xy
x, xy

0
-10
-20
-30

0

2

4

ω (eV)

6

8

10

0

2

4

ω (eV)

6

8

10

0

2

4

ω (eV)

6

8

10

FIG. 3: Spectrally resolved shift photoconductivity. Components of σ defining the shift photoconductivity vector [Eq. (5)]
as a function of light frequency ω, at different relative stackings: (a) AA, (b) AB, and (c) DW. The σy,yy , σy,xx , σy,xy , and σ x,xy
components are plotted in blue, yellow, green, and red respectively. These local shift photoconductivities have similar qualitative
features for the different relative stackings. The first peak at ωK ≈ 5 eV in all stackings arises from transitions at the K point and
makes minor contributions to the electronic polarization. The second peak at ωM ≈ 6 eV corresponds to the photoexcitations of
the electrons near the M point and contributes the dominant part of the electronic polarization, as reflected by their shift vectors
Rmn . The range of frequencies, for which the shift current vortices due to the electronic polarization textures occur, is highlighted
in gray. For AA and AB stackings, the σy,xx and σ x,xy components are equivalent by symmetry (see SI).
nant transitions occur in regions of the BZ which contribute
most dominantly to the in-plane polarization, see Fig. 2 (b).
The origin of this correspondence can be traced to the interplay between the interband transition rates described by the
a
b
QGT, Qab
mn = Anm Amn (see Methods), and the non-Abelian
Berry connection Anm (k). The dominant optical transition
rates occur at the M points (edges) and the K/K′ points (corners) of the BZ (K and K′ correspond to different valleys) as
elucidated by the spatial trace of the QGT in Fig. 2 (d) for the
DW stacking. The shift photocurrents combine both the QGT
and the diagonal elements of the non-Abelian Berry connection Anm (k). However, as shown in Fig. 2 (b), Ann (k) forms
a vortex at the K point. As its magnitude smoothly goes to
zero at the vortex center, transitions at the K point contribute
less to both the electronic polarization and the shift photocurrents. In contrast, at the M points, which are the saddle points
in the effective band structures and the trace of the QGT,
Ann (k) flows with largest magnitude [see Fig. 2 (b)], contributing most strongly to the electronic polarization and shift
photoconductivity. The correspondence between polarization
and shift photoconductivity occurs in a range of frequencies
near ωM , wherein both the QGT and the diagonal elements of
the non-Abelian Berry connection are significant, resulting in
large photovoltaic shift responses. Since the same regions also
contribute strongly to the electronic polarization that is given
by the Berry connection in Eq. (1), these shift currents arise
directly from the electronic polarization and contribute to the
aforementioned correspondence revealed in Figs. 2 (a) and (c)
(see SI for details).
The spectral dependence of σ is shown in Fig. 3. The
spectrally-resolved components σc,ab that determine the shift
photoconductivity vector in Eq. (5) are shown for the AA, AB
and DW stackings. The elements σ x,xy and σy,xy encode the responses to both linearly and circularly polarized light, in their
real and imaginary parts, respectively [64]. Since electric po-

larization is specifically related to linear light polarization, we
focus only on calculating the real parts of the associated shift
photoconductivities.
The first peak occurs at ωK ≈ 5 eV for all three stackings, which corresponds to transitions at the K point. While
this peak represents a relatively significant contribution to the
shift response, as mentioned previously, it does not reflect the
electronic polarization, as the Berry connection forms vortices
around the K points. The most significant contributions to P
come from the peak at ωM which arises due to transitions at
the M point. The M point corresponds to a van Hove singularity in the joint density of states (JDOS), where the Berry
connection is also the largest, and thus makes the strongest
contribution to the electronic polarization (see SI). As noted
earlier, a range of frequencies near ωM achieves the desired
shift current vortices for the electronic polarization correspondence and is highlighted in Fig. 3. In Fig. 3 we also observe
additional peaks at higher frequencies.
The results in Figs. 2 and 3 were validated with firstprinciples calculations of bilayer hBN as a function of relative stacking (see Methods). The electronic structure contains
two valence bands and two conduction bands near the Fermi
level, arising from the 2pz orbitals of the N and B atoms in
the unit cell, respectively (see Fig. 4). We obtain the maximally localized Wannier functions (MLWFs) [65, 66] of these
4 states by projecting the Bloch states onto pz orbitals centered on each atom and numerically minimizing the spread of
the Wannier functions. The shift current was then calculated
using Wannier interpolation [67]. The spectrally resolved shift
photoconductivities are shown in Fig. 4 for the AA, AB and
DW stackings, in good agreement with Fig. 3.
Discussion.—In this work, we show that topological polarization textures can result in exotic nonlinear optical responses, namely a shift photoconductivity with a vortex-like
pattern. We illustrate this concept using bilayer hBN, the

5

(a)

AA

8

(b)

DW

AB

Ek − EF (eV)

4
0

−4

B

−8

−12
−16

DFT
WANNIER 90
Γ

DFT
WANNIER 90
K

(c)

K

Γ Γ

M

k

AA

K

10
5

Γ

M

k

DW

AB
y, yy
y, xx
y, xy
x, xy

15

σ (ω) (µA Å/V2 )

Γ Γ

M

k

DFT
WANNIER 90

y, yy
y, xx
y, xy
x, xy

y, yy
y, xx
y, xy
x, xy

N

0
−5

−10
−15

0

2

4

ω (eV)

6

8

10 0

2

4

ω (eV)

6

8

10 0

2

4

ω (eV)

6

8

10

FIG. 4: First-principles calculations of shift photoconductivity. (a) Electronic band structure of bilayer hBN for the AA, AB
and DW stackings. The bands obtained from first-principles calculations are shown in black. The Wannierized bands of the pz
orbitals are shown in red. (b) Illustration of the real-space Wannier functions corresponding to the pz orbitals on the B (purple)
and N (yellow) atoms, which yield the conduction and valence Wannier bands, respectively. (c) Frequency-resolved shift currents
obtained from the Wannier functions for the AA, AB and DW stackings. The σy,yy , σy,xx , σy,xy , and σ x,xy components are plotted
in blue, yellow, green, and red respectively.
prototypical vdW ferroelectric, as an example, although the
results can be generalized to other materials. The general
shape of the stacking-dependent polarization can be determined solely from symmetry analysis of the space groups of
the different stackings [25, 68]: by symmetry the shape of the
polarization textures in TMDs twisted about the rhombohedral stacking is identical to the textures in t-hBN. Based on the
generality of the presented theoretical framework, we expect
any twisted bilayer with topological polarization to exhibit
shift photoconductivity vortices, such as TMDs [34]. Experimentally, these could be retrieved from the optical frequency
windows determined by the band gaps of TMDs (1-2 eV),
which are practically more accessible than the band gaps of
the twisted hBN (5-6 eV) studied here. While the large band
gap of hBN may pose challenges for the experimental realization of these shift photoconductivity vortices, by selecting
different materials the gap can effectively be tuned to suit the
experimental setup.
In addition to the polarization, the shift current texture is
also constrained by symmetry. As shown in Figs. 3 and 4, the
σy,xy component, which describes the coupling of both x and
y components to in-plane electric fields, is vanishingly small
for all stackings. Furthermore, the C3 rotation symmetry of
the lattice constrains several components of the shift photoconductivity tensor: σ x,xx = −σ x,yy = −σy,xx = −σy,xy [59].
Moreover, σy,yy = −σ x,xy , as demonstrated in Fig. 3. While
our results satisfy these symmetry-imposed constraints, our
model relies on the configuration space approximation, which
explicitly assumes the locality of the shift photocurrents and
the polarization within the supercell [25]. However, the con-

figuration space approximation yields polarization textures in
excellent agreement with experiment [17], and our calculations of the shift photoconductivities are in excellent agreement with large-scale calculations of twisted bilayers [59].
We show that experimentally measurable shift photocurrents can be used to directly map out the in-plane polarization component of MPDs at characteristic light frequencies.
The local correspondence between polarization and shift current proposed here may be used to optically probe topological
polarization textures with sub-diffraction photocurrent spectroscopy techniques. In the previous studies, such polarization
textures have proven difficult to observe experimentally [34].
The photocurrent microscopy techniques provide a tunable
modern platform for spatially resolving photoexcited quantities on the nanometer scale [37, 58, 69–71], which has recently been successfully applied to spatially resolve the photocurrents in twisted WS2 [72]. Although direct optical experiments are limited to lengthscales of order 100 nm, subdiffraction photocurrent spectroscopy techniques can resolve
details on lengthscales of order 10 nm (with an approximate
resolution of 7.5 nm) [37], and should be capable of resolving the photocurrent vortex structures predicted in this work.
Resolving the flow of the shift photoconductivity would indirectly signal the in-plane polarization and the topological
nature of the MPDs in moiré materials. This technique could
also be used to probe topological polarization textures in other
materials, such as oxide perovskites [32, 33].
The shift photoconductivities arising from in-plane electronic polarization in this work include only the photoexcitation part to the shift currents [35, 48]. We note that such

6
photoexcitation contributions can be probed in transient responses with sub-picosecond resolution [73]. In other scenarios, namely over longer timescales, there are additional
contributions from phonon and impurity-dependent intraband
scattering, as well as from carrier relaxation [35, 48]. Finally, we find that the injection currents, i.e. second-order
photocurrents arising from photoinduced changes of group
velocities [42, 43], are negligible in response to linearly polarized light (see SI). This further highlights the feasibility of
experimentally probing electronic polarization textures using
the correspondence to the shift photoconductivities.
In summary, we show that there is a correspondence between shift current vortices and topological polarization textures. We propose that second-order bulk shift photocurrents can be used to deduce the presence of in-plane electronic polarization in 2D ferroelectrics such as t-hBN, facilitating the experimental observation of topological polarization in marginally-twisted bilayers. We anticipate that this
correspondence will therefore play a key role in uncovering
the new landscape of polar domains as a platform for novel
physical effects.
METHODS
Quantum-geometric relations

The quantum geometric details associated with the correspondence between the shift current and the electronic contribution to material’s electronic polarization are summarized in
this section. The non-Abelian (multiband) Berry connection
Aanm [53] is obtained within the TB model. The polarization
can then be related as a volume integral of the trace of the
non-Abelian Berry connection over occupied (‘occ’) states,
which in turn, on projecting on the direction
β, can be writP
ten in terms of Berry phases: Pβ = − aeβ k⊥ ϕ(k⊥ ). The Berry
phases are defined in terms of the Berry connection as,
Z
Z
occ
X
1
1
β
dkβ
Ann =
dkβ tr Aβ ,
(6)
ϕ(k⊥ ) =
2π
2π
n
where aβ is the unit cell size in the direction β. We note that
the above are gauge-invariant objects. The non-Abelian Berry
connection defines the Hermitian connection associated with
the shift photoconductivities [51],
abc
Cnm
= Aanm Db Acmn ,

(7)

where the covariant derivative is defined with diagonal elements of the Berry connection as Da = ∂ka − i(Aamm − Aann ). In
abc
terms of Hermitian connections Cnm
, the shift photoconductivities can be written for a two-dimensional system as [51]
Z
ie3 X
c,ab
acb
bca ∗
σ (ω) = −
d2 k δ(ω − ωmn ) fnm,k [Cnm
− (Cnm
) ].
8πℏ2 m,n
(8)
The above reduces to the shift vector formula [Eq. (3)], upon
recognizing that the shift vectors read componentwise as
c
c
a
Rc,a
mn = Amm − Ann − i∂kc Arg (Amn ).

(9)

In the systems central to this work, under an appropriate
gauge, and for a = b, the last term can be neglected, as we
also detail and numerically demonstrate in the SI. In particular, the contribution due to the last term vanishes identically
in an optical gauge [60] assuming topologically trivial bands.
This then allows the reduction of the shift vector to an entity
with a single spatial index: Rcmn ≈ Acmm − Acnn .
Beyond the shift vector, the shift photoconductivity notably
involves the quantum-geometric tensor (QGT) Qab
mn defined in
terms of non-Abelian Berry connection elements as
a
b
Qab
mn = Anm Amn ,

(10)

which captures the interband transition rates. For more details
on QGT and its relations to optics and geometry, see SI.
Tight-binding model

Following Refs. [74] and [29], we construct an effective
tight-binding model to describe twisted moiré hBN (t-hBN)
bilayer. To that end, we note that the low-energy Hamiltonian,
describing the pz -orbital bands below and above the Fermi
level can be written as
 ∆

tk tBB,k tBN,k 
 2

 t∗
− ∆2 tNB,k tNN,k 

k

H =  ∗
,
(11)
∆
∗
tk 
tBB,k tNB,k 2
∆ 
∗
∗
∗
tBN,k tNN,k tk
−2

where we assumed a basis of cell-periodic Bloch states of
the top (t) and bottom (b) layer boron and nitrogen atoms:
|Bt ⟩ , |Nt ⟩ , |Bb ⟩ , |Nb ⟩. In the above, the implicit layer indices
were dropped for simplicity.
In a moiré insulator with well-preserved gaps, such as thBN, the off-diagonal 2 × 2 blocks can be treated as perturbations. The monolayer problem can be solved first (setting the
2 × 2 off-diagonal
blocks as zero) to obtain unperturbed eigenE
t/b
states uc/v,k [29, 74]. As a next step, the interlayer couplings
can be included within the configuration space approximation
as perturbations [25].
E Correspondingly, one obtains perturbed
eigenstates ũt/b
c/v,k , from the perturbation theory in the interlayer tunnelling constituting the off-diagonal terms. Such a
transformation from the unperturbed to the perturbed eigenstates is an SU(4) transformation and can be described by the
matrix M such that |ũk ⟩ = M T |uk ⟩. Here, the vectors |ũk ⟩ and
|uk ⟩ include the eigenstates in conduction and valence bands
(c, v), with the top and bottom (t, b) layer flavours. Secondorder perturbation theory then dictates that M is given by


bt
tbt
1 − 1 tvc,k 2

0
0
− ∆vc,kk


2 ∆k
tb
tb ∗


2
tvc,k
(tvc,k )
1


0
1 − 2 ∆k
0
∆
k
 ,
M = 
tb
tb
2

t
t

vc,k
1 vc,k
0
−
1
−
0


∆k
2 ∆k
 (tbt )∗

bt
2
t
vc,k
0
0
1 − 12 ∆vc,kk 
∆k
(12)

7
where ∆k is a local energy gap and the interlayer coupling
tb
bt
constants tvc,k
(x), tvc,k
(x) hybridize the hopping terms of the
Hamiltonian H in Eq. (11) (tBN,k , tNB,k , tBB,k , tNN,k ). The hybridized hoppings are given by the stacking x and the kdependent factors, as detailed explicitly in SI.
The above description ensures that any dependence on
stacking is entirely encapsulated in the SU(4) transformation M, and all stacking-dependent properties can therefore
be rewritten as functions of M.
Since all quantum-geometric quantities and subsequent optical properties introduced in the further section, depend on
the non-Abelian Berry connection, it is useful to rewrite it in
terms of the unperturbed connection A and the SU(4) transformation M as
Ã = −i M † ∇k M + M † AM.

(13)

All stacking-dependent electronic polarizations P(x) and shift
photoconductivities σc,ab (x) with a, b, c = x, y, can be extracted from the quantum-geometric relations encoded by the
SU(4)-modified non-Abelian Berry connection matrix Ã. To
study the quantum-geometric relations, we replace the unperturbed connection with the modified one, by relabelling:
Ã → A.
The tight-binding calculations were carried out assuming
the form of the real-space hoppings tXY , with X, Y denoting
the B, N atoms, to be an exponential decay in |x| with an
upper cutoff, following Refs. [29] and [74]. In order to obtain a faithful description of hBN with an interlayer spacing
of 0.33 nm, the tight-binding parameters have been chosen
following Ref. [74] as ∆ = 4.5 eV, t = 2.0 eV, for the in0
tralayer nearest-neighbor hoppings, and t0BN = tNB
= 1.28 eV,
0
0
tBB = 0.8 eV, and tNN = 0.6 eV for the interlayer hopping parameters. The latter parameters were further regularized to account for the relative displacements associated with the local
stackings. The interlayer coupling regularizations have been
chosen following Ref. [29]. In addition to the chosen parameters, the Fermi-Dirac occupations are regarded as fvk = 1
for the valence bands and fck = 0 for the conduction bands,
since the energy gap between the conduction and valence band
∆k ≈ 4.5 eV ≫ kB T for temperatures T ≲ 104 K.

held fixed. The relative stackings were sampled in 2D using
a grid of 6 × 6, which explicitly includes the high symmetry
stackings: the AA stacking, where the two layers are perfectly
aligned, the AB and BA where the opposite atoms in neighboring layers are vertically aligned, given by a relative shift of
x = 31 or 32 of a unit cell diagonal, respectively, and domain
wall (DW) stacking, given by a shift of x = 12 of a unit cell
diagonal. At each point a geometry relaxation was performed
to obtain the equilibrium layer separation, while keeping the
in-plane atomic positions fixed.
Maximally localized Wannier functions (MLWF) were then
constructed for the two valence bands and two conduction
bands closest to the Fermi level, using the interface between
abinit and Wannier90 [65, 66]. The valence (conduction)
bands are of N (B) 2pz character. (see SI). The initial projections were made onto the 2pz orbitals of the four atoms in
the bilayer unit cell. A disentanglement procedure was performed to obtain MLWFs for the entangled bands near the
Fermi level, using a frozen energy window which contains
only the four bands closest to the Fermi level, and an outer
energy window which contains those bands everywhere in the
BZ. After the disentanglement procedure, the spread of the
Wannier functions was then minimized. The shift current was
then obtained using the Wannier interpolation [67]. Calculations were repeated to obtain the MLWFs and shift currents as
a function of relative stacking between the layers.

DATA AVAILABILITY

The datasets generated and analyzed in this study are available from the corresponding author upon request.

CODE AVAILABILITY

The data presented in this study were generated using theoretical models as well as free and open-source first-principles
packages as described in the Methods section.

First-principles calculations

First-principles density functional theory (DFT) calculations were performed to simulate bilayer hBN, in the rhombohedral (aligned) stacking, using the abinit [75, 76] code.
Norm-conserving [77] psml [78] pseudopotentials were used,
obtained from Pseudo-Dojo [79]. abinit employs a planewave basis set, which was determined using a kinetic energy
cutoff of 1000 eV. A Monkhorst-Pack k-point grid [80] of
12×12×1 was used to sample the Brillouin zone. The revPBE
exchange-correlation functional was used [81], and the vdwDFT-D3(BJ) [82] correction was used to treat the vdW interactions between the layers.
In order to sample the relative stackings between the layers in ‘configuration space’ [63], the top layer was translated
along the unit cell diagonal over the bottom layer, which was

ACKNOWLEDGMENTS

The authors acknowledge G. Chaudhary and
A. Mishchenko for helpful discussions. A. A. acknowledges funding from the Cambridge International Scholarship
awarded by the Cambridge Trust. W. J. J. acknowledges funding from the Rod Smallwood Studentship at Trinity College,
Cambridge. D. B. acknowledges the US Army Research Office (ARO) MURI project under grant No. W911NF-21-0147
and the Simons Foundation award No. 896626. R.-J. S. acknowledges funding from a New Investigator Award, EPSRC
grant EP/W00187X/1. R.-J. S. also acknowledges funding
from a EPSRC ERC underwrite grant EP/X025829/1, as well
as Trinity College, Cambridge.

8
AUTHOR CONTRIBUTIONS

A. A. performed the tight-binding calculations with input
from W. J. J. and R.-J. S. A. A., W. J. J. and R.-J. S. developed
the theory analysis of the local shift currents and relation to
quantum geometry. D. B. performed the first-principles cal-

[1] Bistritzer, R. & MacDonald, A. H. Moire bands in twisted
double-layer graphene. PNAS 108, 12233 (2011). URL https:
//www.pnas.org/doi/10.1073/pnas.1108174108.
[2] Carr, S. et al. Twistronics: manipulating the electronic properties of two-dimensional layered structures through their twist
angle. Phys. Rev. B 95, 075420 (2017). URL https://doi.
org/10.1103/PhysRevB.95.075420.
[3] Cao, Y. et al. Unconventional superconductivity in magic-angle
graphene superlattices. Nature 556, 43 (2018). URL https:
//doi.org/10.1038/nature26160.
[4] Nuckolls, K. P. et al.
Strongly correlated Chern insulators in magic-angle twisted bilayer graphene.
Nature
588, 610–615 (2020). URL https://doi.org/10.1038/
s41586-020-3028-8.
[5] Wu, S., Zhang, Z., Watanabe, K., Taniguchi, T. & Andrei,
E. Y. Chern insulators, van hove singularities and topological flat bands in magic-angle twisted bilayer graphene. Nat.
Mater. 20, 488–494 (2021). URL https://doi.org/10.
1038/s41563-020-00911-2.
[6] Xie, Y. et al. Fractional Chern insulators in magic-angle twisted
bilayer graphene. Nature 600, 439–443 (2021). URL https:
//doi.org/10.1038/s41586-021-04002-3.
[7] Zeng, Y. et al. Thermodynamic evidence of fractional Chern
insulator in moiré MoTe2 . Nature 622, 69–73 (2023). URL
https://doi.org/10.1038/s41586-023-06452-3.
[8] Park, H. et al. Observation of fractionally quantized anomalous
Hall effect. Nature 622, 74–79 (2023). URL https://doi.
org/10.1038/s41586-023-06536-0.
[9] Tong, Q., Liu, F., Xiao, J. & Yao, W. Skyrmions in the moiré
of van der Waals 2D magnets. Nano Lett. 18, 7194–7199
(2018). URL https://doi.org/10.1021/acs.nanolett.
8b03315.
[10] Hejazi, K., Luo, Z.-X. & Balents, L. Noncollinear phases in
moiré magnets. PNAS 117, 10721–10726 (2020). URL https:
//doi.org/10.1073/pnas.2000347117.
[11] Song, T. et al. Direct visualization of magnetic domains and
moiré magnetism in twisted 2D magnets. Science 374, 1140–
1144 (2021). URL https://doi.org/10.1126/science.
abj7478.
[12] Bennett, D. et al. Stacking-engineered ferroelectricity and
multiferroic order in van der waals magnets. Phys. Rev. Lett.
133, 246703 (2024). URL https://link.aps.org/doi/10.
1103/PhysRevLett.133.246703.
[13] Stern, M. V. et al. Interfacial ferroelectricity by van der Waals
sliding. Science 372, 1462 (2021). URL https://www.
science.org/doi/10.1126/science.abe8177.
[14] Yasuda, K., Wang, X., Watanabe, K., Taniguchi, T. & JarilloHerrero, P. Stacking-engineered ferroelectricity in bilayer
boron nitride. Science 372, 1458 (2021). URL https://doi.
org/10.1126/science.abd3230.
[15] Wang, X. et al. Interfacial ferroelectricity in rhombohedralstacked bilayer transition metal dichalcogenides. Nat. Nan-

culations. All authors contributed to the analysis and interpretation of the results and to the writing of the paper.
COMPETING INTERESTS

The authors declare no competing interests.

otechnol. 17, 367–371 (2022). URL https://doi.org/10.
1038/s41565-021-01059-z.
[16] Weston, A. et al. Interfacial ferroelectricity in marginally
twisted 2D semiconductors.
Nat. Nanotechnol. 17,
390–395 (2022).
URL https://doi.org/10.1038/
s41565-022-01072-w.
[17] Ko, K. et al. Operando electron microscopy investigation of
polar domain dynamics in twisted van der Waals homobilayers.
Nat. Mater. 1–7 (2023). URL https://doi.org/10.1038/
s41563-023-01595-0.
[18] Molino, L. et al. Ferroelectric switching at symmetry-broken
interfaces by local control of dislocations networks. Adv.
Mater. 35, 2207816 (2023). URL https://doi.org/10.
1002/adma.202207816.
[19] Van Winkle, M. et al. Engineering interfacial polarization switching in van der Waals multilayers. Nat. Nanotechnol. 1–7 (2024). URL https://doi.org/10.1038/
s41565-024-01642-0.
[20] Yasuda, K. et al. Ultrafast high-endurance memory based on
sliding ferroelectrics. Science eadp3575 (2024). URL https:
//doi.org/10.1126/science.adp3575.
[21] Bian, R. et al. Developing fatigue-resistant ferroelectrics using
interlayer sliding switching. Science eado1744 (2024). URL
https://doi.org/10.1126/science.ado1744.
[22] Li, L. & Wu, M. Binary compound bilayer and multilayer with
vertical polarizations: Two-dimensional ferroelectrics, multiferroics, and nanogenerators. ACS Nano 11, 6382–6388
(2017). URL https://pubs.acs.org/doi/abs/10.1021/
acsnano.7b02756.
[23] Bennett, D. & Remez, B. On electrically tunable stacking
domains and ferroelectricity in moiré superlattices. npj 2D
Mater. Appl. 6, 1–6 (2022). URL https://doi.org/10.
1038/s41699-021-00281-6.
[24] Bennett, D. Theory of polar domains in moiré heterostructures.
Phys. Rev. B 105, 235445 (2022). URL https://doi.org/
10.1103/PhysRevB.105.235445.
[25] Bennett, D., Chaudhary, G., Slager, R.-J., Bousquet, E. &
Ghosez, P. Polar meron-antimeron networks in strained and
twisted bilayers. Nat. Commun. 14, 1629 (2023). URL https:
//doi.org/10.1038/s41467-023-37337-8.
[26] Bennett, D., Jankowski, W. J., Chaudhary, G., Kaxiras, E. &
Slager, R.-J. Theory of polarization textures in crystal supercells. Phys. Rev. Res. 5, 033216 (2023). URL https://link.
aps.org/doi/10.1103/PhysRevResearch.5.033216.
[27] Qi, X.-L. & Zhang, S.-C. Topological insulators and superconductors. Rev. Mod. Phys. 83, 1057–1110 (2011). URL https:
//link.aps.org/doi/10.1103/RevModPhys.83.1057.
[28] Hasan, M. Z. & Kane, C. L. Colloquium. Rev. Mod. Phys. 82,
3045–3067 (2010). URL https://link.aps.org/doi/10.
1103/RevModPhys.82.3045.
[29] Jankowski, W. J., Bennett, D., Agarwal, A., Chaudhary, G. & Slager, R.-J.
Polarization textures in crys-

9
tal supercells with topological bands. Phys. Rev. B 110,
085429 (2024). URL https://link.aps.org/doi/10.
1103/PhysRevB.110.085429.
[30] Das, S. et al.
Observation of room-temperature polar
skyrmions. Nature 568, 368–372 (2019). URL https://doi.
org/10.1038/s41586-019-1092-8.
[31] Han, L. et al. High-density switchable skyrmion-like polar
nanodomains integrated on silicon. Nature 603, 63–67 (2022).
URL https://doi.org/10.1038/s41586-021-04338-w.
[32] Junquera, J. et al. Topological phases in polar oxide nanostructures. Rev. Mod. Phys. 95, 025001 (2023). URL https:
//link.aps.org/doi/10.1103/RevModPhys.95.025001.
[33] Sánchez-Santolino, G. et al.
A 2D ferroelectric vortex pattern in twisted BaTiO3 freestanding layers. Nature
626, 529–534 (2024). URL https://doi.org/10.1038/
s41586-023-06978-6.
[34] Vu, T.-H.-Y. et al. Imaging topological polar structures in
marginally twisted 2D semiconductors. arxiv:2405.15126
(2024). URL https://arxiv.org/abs/2405.15126.
[35] Belinicher, V., Ivchenko, E. & Sturman, B. Kinetic theory of
the displacement photovoltaic effect in piezoelectric. Sov. Phys.
JETP 56, 359 (1982). URL http://jetp.ras.ru/cgi-bin/
dn/e_056_02_0359.pdf.
[36] Ochoa, H. & Asenjo-Garcia, A. Flat bands and chiral optical response of moiré insulators. Phys. Rev. Lett. 125,
037402 (2020). URL https://link.aps.org/doi/10.
1103/PhysRevLett.125.037402.
[37] Hesp, N. C. et al. Nano-imaging photoresponse in a moiré unit
cell of minimally twisted bilayer graphene. Nat. Commun. 12,
1640 (2021). URL https://www.nature.com/articles/
s41467-021-21862-5.
[38] Zhang, S. et al. Visualizing moiré ferroelectricity via plasmons and nano-photocurrent in graphene/twisted-WSe2 structures. Nat. Commun. 14, 6200 (2023). URL https://www.
nature.com/articles/s41467-023-41773-x.
[39] Du, L. et al. Moiré photonics and optoelectronics. Science
379, eadg0014 (2023). URL https://www.science.org/
doi/10.1126/science.adg0014.
[40] Kuang, X. et al. Optical properties and plasmons in moiré structures. J. Phys.: Condens. Matter 36, 173001 (2024). URL
https://doi.org/10.1088/1361-648X/ad1f8c.
[41] Zhang, S. et al. Plasmonic polarization sensing of electrostatic
superlattice potentials. arXiv:2406.18028 (2024). URL https:
//arxiv.org/abs/2406.18028.
[42] Sipe, J. E. & Ghahramani, E. Nonlinear optical response
of semiconductors in the independent-particle approximation.
Phys. Rev. B 48, 11705–11722 (1993). URL https://link.
aps.org/doi/10.1103/PhysRevB.48.11705.
[43] Sipe, J. E. & Shkrebtii, A. I.
Second-order optical
response in semiconductors.
Phys. Rev. B 61, 5337–
5352 (2000). URL https://link.aps.org/doi/10.1103/
PhysRevB.61.5337.
[44] Chaudhary, S., Lewandowski, C. & Refael, G. Shift-current response as a probe of quantum geometry and electron-electron
interactions in twisted bilayer graphene. Phys. Rev. Res.
4, 013164 (2022). URL https://link.aps.org/doi/10.
1103/PhysRevResearch.4.013164.
[45] Chen, S., Chaudhary, S., Refael, G. & Lewandowski, C. Enhancing shift current response via virtual multiband transitions.
Commun. Phys. 7, 250 (2024). URL https://www.nature.
com/articles/s42005-024-01729-z.
[46] Cook, A. M., M. Fregoso, B., De Juan, F., Coh, S. & Moore,
J. E. Design principles for shift current photovoltaics. Nat.
Commun. 8, 14176 (2017). URL https://www.nature.com/

articles/ncomms14176.
[47] Kaplan, D., Holder, T. & Yan, B. Twisted photovoltaics at terahertz frequencies from momentum shift current. Phys. Rev.
Res. 4, 013209 (2022). URL https://link.aps.org/doi/
10.1103/PhysRevResearch.4.013209.
[48] Zhu, P. & Alexandradinata, A. Anomalous shift and optical vorticity in the steady photovoltaic current. Phys. Rev. B
110, 115108 (2024). URL https://link.aps.org/doi/10.
1103/PhysRevB.110.115108.
[49] Bouhon, A., Timmel, A. & Slager, R.-J. Quantum geometry beyond projective single bands. arXiv:2303.02180 (2023). URL
https://arxiv.org/abs/2303.02180.
[50] Törmä, P. Essay: Where can quantum geometry lead us? Phys.
Rev. Lett. 131, 240001 (2023). URL https://link.aps.
org/doi/10.1103/PhysRevLett.131.240001.
[51] Ahn, J., Guo, G.-Y., Nagaosa, N. & Vishwanath, A. Riemannian geometry of resonant optical responses. Nat. Phys.
18, 290–295 (2021). URL https://doi.org/10.1038%
2Fs41567-021-01465-z.
[52] Provost, J. & Vallee, G. Riemannian structure on manifolds
of quantum states. Commun. Math. Phys. 76, 289–301 (1980).
URL https://doi.org/10.1007/BF02193559.
[53] Vanderbilt, D. Berry phases in electronic structure theory: electric polarization, orbital magnetization and topological insulators (Cambridge University Press, 2018).
[54] Topp, G. E., Eckhardt, C. J., Kennes, D. M., Sentef,
M. A. & Törmä, P.
Light-matter coupling and quantum geometry in moiré materials.
Phys. Rev. B 104,
064306 (2021). URL https://link.aps.org/doi/10.
1103/PhysRevB.104.064306.
[55] King-Smith, R. & Vanderbilt, D. Theory of polarization of crystalline solids. Phys. Rev. B 47, 1651 (1993). URL https:
//doi.org/10.1103/PhysRevB.47.1651.
[56] Vanderbilt, D. & King-Smith, R. Electric polarization as a bulk
quantity and its relation to surface charge. Phys. Rev. B 48,
4442 (1993). URL https://doi.org/10.1103/PhysRevB.
48.4442.
[57] Resta, R. Macroscopic polarization in crystalline dielectrics:
the geometric phase approach. Rev. Mod. Phys. 66, 899–
915 (1994). URL https://link.aps.org/doi/10.1103/
RevModPhys.66.899.
[58] Ma, Q., Krishna Kumar, R., Xu, S.-Y., Koppens, F. H. L. &
Song, J. C. W. Photocurrent as a multiphysics diagnostic of
quantum materials. Nat. Rev. Phys. 5, 170–184 (2023). URL
https://doi.org/10.1038/s42254-022-00551-2.
[59] Hu, C., Naik, M. H., Chan, Y.-H., Ruan, J. & Louie, S. G.
Light-induced shift current vortex crystals in moiré heterobilayers. PNAS 120, e2314775120 (2023). URL https://www.
pnas.org/doi/abs/10.1073/pnas.2314775120.
[60] Fregoso, B. M., Morimoto, T. & Moore, J. E. Quantitative relationship between polarization differences and
the zone-averaged shift photocurrent.
Phys. Rev. B 96,
075421 (2017). URL https://link.aps.org/doi/10.
1103/PhysRevB.96.075421.
[61] Resta, R. Geometrical theory of the shift current in presence of disorder and interaction.
Phys. Rev. Lett. 133,
206903 (2024). URL https://link.aps.org/doi/10.
1103/PhysRevLett.133.206903.
[62] Carr, S., Fang, S. & Kaxiras, E. Electronic-structure methods for twisted moiré layers. Nature Reviews Materials
5, 748–763 (2020). URL http://dx.doi.org/10.1038/
s41578-020-0214-0.
[63] Carr, S. et al. Relaxation and domain formation in incommensurate two-dimensional heterostructures. Phys. Rev.

10
B 98, 224102 (2018). URL https://doi.org/10.1103/
PhysRevB.98.224102.
[64] Ahn, J., Guo, G.-Y. & Nagaosa, N. Low-frequency divergence and quantum geometry of the bulk photovoltaic effect in topological semimetals. Phys. Rev. X 10, 041041
(2020).
URL https://link.aps.org/doi/10.1103/
PhysRevX.10.041041.
[65] Marzari, N., Mostofi, A. A., Yates, J. R., Souza, I. & Vanderbilt,
D. Maximally localized Wannier functions: Theory and applications. Rev. Mod. Phys. 84, 1419–1475 (2012). URL https:
//link.aps.org/doi/10.1103/RevModPhys.84.1419.
[66] Pizzi, G. et al. Wannier90 as a community code: new features
and applications. J. Phys.: Condens. Matter 32, 165902 (2020).
URL https://doi.org/10.1088/1361-648X/ab51ff.
[67] Ibañez Azpiroz, J., Tsirkin, S. S. & Souza, I. Ab initio calculation of the shift photocurrent by Wannier interpolation. Phys.
Rev. B 97, 245143 (2018). URL https://link.aps.org/
doi/10.1103/PhysRevB.97.245143.
[68] Ji, J., Yu, G., Xu, C. & Xiang, H. J. General theory
for bilayer stacking ferroelectricity. Phys. Rev. Lett. 130,
146801 (2023). URL https://link.aps.org/doi/10.
1103/PhysRevLett.130.146801.
[69] Lang, D. V. & Henry, C. H. Scanning photocurrent microscopy:
A new technique to study inhomogeneously distributed recombination centers in semiconductors. Solid-State Electron. 21,
1519–1524 (1978). URL https://www.sciencedirect.
com/science/article/pii/0038110178902356.
[70] Rauhut, N. et al. Antenna-enhanced photocurrent microscopy
on single-walled carbon nanotubes at 30 nm resolution. ACS
Nano 6, 6416–6421 (2012). URL https://pubs.acs.org/
doi/10.1021/nn301979c.
[71] Xiang, L., Jin, H. & Wang, J. Quantifying the photocurrent
fluctuation in quantum materials by shot noise. Nature Communications 15, 2012 (2024). URL https://doi.org/10.
1038/s41467-024-46264-1.
[72] Li, H. et al. Imaging moiré excited states with photocurrent
tunnelling microscopy. Nat. Mater. 23, 633–638 (2024). URL
https://doi.org/10.1038/s41563-023-01753-4.
[73] Sotome, M. et al. Spectral dynamics of shift current in
ferroelectric semiconductor sbsi.
PNAS 116, 1929–1933
(2019). URL https://www.pnas.org/doi/abs/10.1073/
pnas.1802427116.
[74] Yu, H., Zhou, Z. & Yao, W. Distinct moiré textures of in-plane
electric polarizations for distinguishing moiré origins in homobilayers. Sci. China Phys. Mech. Astron. 66, 107711 (2023).
URL https://doi.org/10.1007/s11433-023-2163-3.
[75] Gonze, X. & et al. Recent developments in the ABINIT
software package. Comput. Phys. Commun. 205, 106 –
131 (2016).
URL https://www.sciencedirect.com/
science/article/pii/S0010465516300923.
[76] Gonze, X. & et al. The ABINIT project: Impact, environment and recent developments. Comput. Phys. Commun. 248,
107042 (2020). URL https://www.sciencedirect.com/
science/article/pii/S0010465519303741.
[77] Hamann, D. Optimized norm-conserving Vanderbilt pseudopotentials. Phys. Rev. B 88, 085117 (2013). URL https:
//doi.org/10.1103/PhysRevB.88.085117.
[78] Garcı́a, A., Verstraete, M. J., Pouillon, Y. & Junquera, J. The
PSML format and library for norm-conserving pseudopotential
data curation and interoperability. Comput. Phys. Commun.
227, 51 (2018). URL https://doi.org/10.1016/j.cpc.
2018.02.011.
[79] Van Setten, M. et al. The pseudodojo: Training and grading a
85 element optimized norm-conserving pseudopotential table.

Comput. Phys. Commun. 226, 39 (2018). URL https://doi.
org/10.1016/j.cpc.2018.01.012.
[80] Monkhorst, H. J. & Pack, J. D. Special points for Brillouinzone integrations. Phys. Rev. B 13, 5188 (1976). URL https:
//doi.org/10.1103/PhysRevB.13.5188.
[81] Zhang, Y. & Yang, W. Comment on “Generalized gradient approximation made simple”. Phys. Rev. Lett. 80,
890 (1998).
URL https://journals.aps.org/prl/
abstract/10.1103/PhysRevLett.80.890.
[82] Becke, A. D. & Johnson, E. R.
A simple effective potential for exchange.
J. Chem. Phys.
124, 221101 (2006).
URL https://pubs.aip.
org/aip/jcp/article/124/22/221101/920551/
A-simple-effective-potential-for-exchange.

SUPPLEMENTARY INFORMATION
Shift photocurrent vortices from topological polarization textures
Aneesh Agarwal,1 Wojciech J. Jankowski,1 Daniel Bennett,2 and Robert-Jan Slager1
1

Theory of Condensed Matter Group, Cavendish Laboratory, University of Cambridge, J. J. Thomson Avenue, Cambridge CB3 0HE, UK
2
John A. Paulson School of Engineering and Applied Sciences, Harvard University, Cambridge, Massachusetts 02138, USA

2
SUPPLEMENTARY NOTE 1: MORE DETAILS ON QUANTUM GEOMETRY

We provide further details on the quantum geometry relevant to this work [1]. The quantum-geometric tensor (QGT) Qab
mn was
defined in terms of multiband (non-Abelian) Berry connection Aanm (k) = i un,k ∂ka um,k [2], with spatial indices a = x, y, . . ., as:
i ab
a
b
ab
Qab
mn ≡ Anm Amn = gmn − F mn ,
2

(1)

ab
which here we furthermore decompose into the quantum metric gab
part) and Berry curvature form contributions Fmn
[3]
mn (real
Punocc
n
ab
(imaginary part); the Berry curvature in band n then reads: Ωab = m Fmn . Notably, in the context of the main text, the
xx
shift photoconductivity components σc,xx and σc,yy only couple electric fields to the quantum metric gmn
and gyy
mn through the
polarization-related shift vector part, whereas the components σ x,xy σ x,yx , σy,xy , σy,yx involve coupling to both the quantum metric,
xy
xy
yx
gmn
= gyx
mn , and symplectic elements, F mn = −F mn .
Following Ref. [4], we can further formalize the formulation of the QGT-based objects that are relevant for studying the
considered optical responses. Accordingly, one can define a transition dipole moment, rmn (k) = ⟨ψmk | r̂ |ψnk ⟩, and identify it as
a tangent vector on the manifold of quantum states with components [4],
a
rmn
(k) = iδmn ∂a + Aamn (k).

(2)

Here, ∂a ≡ ∂∂k is a tangent vector component induced by the local parameter-space coordinates {ka }. Furthermore, local interband
a
transition vectors can be defined [4],
êamn (k) = ramn (k) um,k

un,k ,

(3)

which rigorously define the QGT as a Hermitian metric induced by an inner product of the tangent vectors,
a
b
a b
Qab
mn ≡ ⟨êmn , êmn ⟩ = rnm rmn .

(4)

Here, a Hilbert-Schmidt inner product of matrices is used, which is defined as [4],
h
i X
⟨A, B⟩ = Tr A† B =
A∗ab Bab .

(5)

a,b

As relevant to the shift currents, we further define a Hermitian connection, consistently with Ref. [4],
acb
a b;c
Cmn
≡ ⟨êamn , Dc êbmn ⟩ = rnm
rmn ,

where a covariant derivative can be defined with a parallel-transport equation Dc êamn =
b;c
Here, rnm
is a generalized (covariant) derivative of the transition dipole,

(6)
P

P ad cb
acb
b
ca
d Qmn (C mn )d .
b (C mn )b êmn and C mn ≡

b;c
b
b
b
rmn
(k) ≡ Dc rmn
(k) = ∂c rmn
(k) − i[Acmm (k) − Acnn (k)]rmn
(k),

as utilized in the Methods.

(7)

3
SUPPLEMENTARY NOTE 2: OPTICAL RESPONSES

The optical responses relevant to this work can be recast in terms of their quantum-geometric interpretations, following Refs.
[3, 4] which can be derived from perturbation theory in electric dipole Hamiltonian, for more details see Refs. [5, 6].
The geometric quantities introduced in the previous Section are physically related to the first-order optical conductivity
Z
dd k
πωe2 X
b,a
δ(ω − ωmn ) fnm Qba
(8)
σ =
mn ,
ℏ m,n
(2π)d
where fnm = fn,k − fm,k is the difference between the Fermi-Dirac probability distributions of (occupied) bands n and (unoccupied)
bands m. ℏωmn is the energy gap as a function of k between the bands m and n involved in the photoexcitation.
Furthermore, the quantum-geometric quantities can be used to calculate second-order photoconductivities in materials. Such
photoconductivities can yield DC photovoltaic responses, which for a second-order response decompose into injection and shift
terms,
c,ab
σc,ab = σc,ab
inj + σshift .

(9)

The injection currents arise due to the different band dispersions of the valence and conduction, which cause the group velocities
of the photoexcited electrons to change. The associated injection photoconductivity can be written in terms of the quantum
geometric tensor Qba
mn as
Z
πe3 τ X
d2 k
σc,ab
=
−
δ(ω − ωmn ) fnm Qab
(10)
mn ∂c ωmn .
inj
ℏ2 m,n
(2π)2
Here, τ is a relaxation time for the photoexcited particle to decay.
Centrally to this work, the shift photoconductivity – which is the other part of the second-order photoconductivity that yields
another photovoltaic DC response to light (due to the positional shifts of electrons) beyond the injection currents – can be related
mn
to the Hermitian connection Cacb
as [4]
Z


d2 k
πe3 X
c,ab
acb
bca ∗
.
(11)
δ(ω
−
ω
)
f
i
C
−
(C
)
σshift = − 2
mn
nm
mn
mn
2ℏ m,n
(2π)2

Crucially, the shift conductivities can also be expressed with the shift vectors,

Ramn ≡ Amm − Ann − i∇k Arg (Aamn ),

(12)

corresponding to positional shifts of electronic wavepackets under optical transitions [5, 6], as can be captured by the relation of
the Abelian Berry connection (Acnn ) to Wannier charge centers [7]. Furthermore, on direct substitution, consistently with Ref. [3],
we have,
Z
πe3 X
d2 k
c,a
c,b
σc,ab
=
−
δ(ω − ωmn ) fnm Qba
(13)
mn (Rmn − Rnm ) ,
shift
ℏ2 m,n
(2π)d
which explicitly demonstrates that the non-vanishing shift photoconductivities do not require any band dispersion, unlike the
injection photoconductivities.
The introduced photoconductivities capture the light-induced DC photovoltaic responses [3, 4]:
X
a
b
jcshift/inj (0) = 2
σc,ab
(14)
shift/inj (ω)E (ω)E (−ω),
a,b

for the second order DC currents (‘0’ denotes the vanishing frequency of the shift/injection photocurrent) induced by the electric
fields E a (ω). a, b run over spatial direction indices (x, y, . . .). In the main text, we drop the implicit indices capturing the
vanishing frequency of the DC current, as well as its shift nature, given the context and focus of this work on these aspects.
For the first-order AC responses,
X
jb (ω) =
σb,a (ω)E a (ω),
(15)
a

which were further calculated in the subsequent Sections to contrast with the second-order results. Importantly, the first-order
responses result only in AC currents that can be associated with an oscillatory dynamical polarization of the system, whereas the
second-order DC shift and injection photoconductivities result in non-oscillatory bulk currents measurable as a steady response.

4
SUPPLEMENTARY NOTE 3: CRYSTAL AND ELECTRONIC STRUCTURE OF HEXAGONAL BORON NITRIDE BILAYERS

" #
" #
1
1
and a2 = 21 √ , and a two atom basis with positions
0
3
xB = 0(a1 + a2 ) and xN = 13 (a1 + a2 ). For bilayer hBN, two monolayers are separated in the out-of-plane direction by some
interlayer distance d ∼ 3.3 Å, which modulates slightly with the relative stacking between the two layers. A rigid in-plane shift
is introduced between the layers in order to sample the energy landscape as a function of relative stacking [8–10]. The shape of
the energy landscape is well-known, with maxima for AA stackings, minima for the AB and BA stackings, and saddle points for
domain walls separating the minima [9, 10].
Monolayer hBN has a honeycomb lattice, with lattice vectors a1 =

The orbital-projected bands for bilayer hBN are shown in Supplementary Fig. 1 for the AA stacking. Because the AB sublattice symmetry is broken, a gap opens at the Fermi level, in contrast to graphene. There are four bands near the Fermi level,
corresponding primarily to the 2pz orbitals of each of the four atoms. The valence bands are the pz orbitals of the N atoms and
the conduction bands are the pz orbitals of the B atoms.

5

B1

N1
2s
2px
2py
2pz

4
Ek − EF (eV)

0
−4
−8

−12
−16
−20

Γ

K

M

Γ Γ

K

M

k

k

B2

N2

Γ

2s
2px
2py
2pz

4
Ek − EF (eV)

0
−4
−8

−12
−16
−20

Γ

K

M
k

Γ Γ

K

M

Γ

k

SUPPLEMENTARY FIG. 1: Orbital-projected electronic bands of bilayer hBN for the AA stacking. The four panels show the
projections onto the 2s and 2p orbitals of the B and N atoms in the top and bottom layers.

6
SUPPLEMENTARY NOTE 4: CONFIGURATION SPACE APPROXIMATION

We briefly elaborate on the configuration space approximation utilized in the tight-binding models and first-principles calculations performed in this work. While the configuration space approximation was used to deduce the local polarization P(x) in
moiré supercells [10–12], its application to compute the local shift photoconductivities is a central component of this work.
We first consider a moiré bilayer with a small twist angle. For a moiré bilayer with relative twist angle θ between the layers,
the mapping to configuration space is given by [8]
x(r) = (I − R−1
θ )r ,

(16)

where Rθ is a rotation matrix and r is the real space position modulo any lattice vector. While Eq. (16) is exact, for small θ, the
local environment changes around any unit cells are small, hence the local properties in each can be faithfully approximated by
a commensurate bilayer with a relative translation between the layers. The translation can be expressed as
#
"
0 −1
r.
(17)
x≈θ
1 0
allowing the local properties in small-angle twisted bilayers to be parameterized efficiently using a single commensurate cell of
a bilayer, and sliding one layer over the other, when performing first-principles calculations. What we define as the cell at r j
for moiré systems, is a unit cell of one layer and the atoms of the other layer contained (upon a projection) in that unit cell.
A general projective description of this kind is natural for the configuration space picture, providing an arena to define a local
quantity, such as local polarization [11].

7
SUPPLEMENTARY NOTE 5: TOPOLOGICAL POLARIZATION

The winding of the polarization field (topological charge) can be calculated following the methodology in Ref. [10]. The total
winding number is given by
Z


1
Q=
P · ∂ x P × ∂y P dx ,
(18)
4π

where P is normalized and x = (x, y). The polarization in the unit cell is discretized on a fine grid with spacing ∆, and a plaquette
is constructed around each grid point. The plaquettes form a grid which is offset from the original by half a grid spacing, which
avoids the nonpolar AA stacking. The local winding or topological charge can then be defined as
q(x) =

1
(A(P1 , P2 , P3 ) + A(P1 , P3 , P4 )) ,
4π

(19)

where A is the signed area spanned by three points on a sphere:

The total charge is then given by

A(P1 , P2 , P3 ) = 2 arg 1 + P1 · P2 + P2 · P3 + P3 · P1
.

+ iP1 · (P2 × P3 )
Q=

X

q(x) .

(20)

(21)

x

The winding numbers of the AB and BA domains converge to QAB = −QBA = 21 with grid spacing ∆. To calculate the
polarization textures, we use a 148 x-point hexagonal grid for the local polarization P. The local polarization P is computed
using the Eq. (1) of the main text upon an integration of the intraband Berry connection on a hexagonal mesh of 169 k-points
over the BZ.

8
SUPPLEMENTARY NOTE 6: RECONSTRUCTING LOCAL ELECTRIC POLARIZATION FROM THE SHIFT CURRENTS

We further detail the reconstruction scheme for the in-plane electric polarization, based on the shift photocurrents present.
The shift photoconductivity component in quadratic response to electric field in the x-direction reads,
Z
Z
d2 k
πe3 X
d2 k
πe3 X
c
x 2
xx
δ(ω
−
ω
)
f
R
|A
|
=
−
δ(ω − ωmn ) fnm Rcmn Qmn
.
(22)
σc,xx (ω) = − 2
mn nm mn nm
2
2
ℏ m,n BZ (2π)
ℏ m,n BZ (2π)2
Note that here, an appropriate gauge has been chosen such that the spatial indices on the shift vector corresponding to the
stimulating electric field polarizations can be dropped (as detailed in Methods and in the further Sections). Hence, on combining
with an analogous component for the response in the y-direction,
Z
πe3 X
d2 k
c,xx
c,yy
xx
σ (ω) + σ (ω) = − 2
δ(ω − ωmn ) fnm Rcmn (Qmn
+ Qyy
(23)
mn ).
ℏ m,n BZ (2π)2
xx
Assuming that Qmn
+ Qyy
mn contributes comparably/uniformly in the momentum-space region where the polarization is dominant
within the BZ (the edge of BZ in the moiré bilayers, see the main text), we can approximate
Z
πe3 X xx
d2 k
yy
c,xx
c,yy
σ +σ ≈− 2
⟨Qmn + Qmn ⟩
δ(ω − ωmn ) fnm Rcmn ,
(24)
2
ℏ m,n
BZ (2π)

which follows the idea of Ref. [13]. Additionally, within the effective tight-binding models for the moiré bilayers (see the
following Sections), and owing to the triviality of the Bloch bundle over BZ, we have:
Rcmn ≈ Acmm − Acnn ≈ −2Acnn .

(25)

Therefore, on direct substitution, we further obtain,
σ

c,xx

c,yy

+σ

2πe3 X xx
⟨Q + Qyy
≈ 2
mn ⟩ fnm
ℏ m,n mn

Z

!
2 X
d2 k c
yy
xx
c πe
⟨Q + Qmn ⟩ ∝ −∆Pc ,
A ≈ −∆P
(2π)2 nn
ℏ2 m,n mn

(26)

with c = x, y, and the polarization components ∆Pc defined consistently with the modern theory of polarization [14], as in the
main text. In particular, here Pc ≡ ∆Pc is defined as a change of polarization with respect to a non-polar, or high-symmetry,
state [11]. Note that in the second equality above, it has been assumed that the two valence bands contribute roughly equally
to the polarization, consistently with the model. This concludes the derivation of the correspondence between the local shift
currents and electric in-plane polarizations.

9
SUPPLEMENTARY NOTE 7: SYMMETRY ANALYSIS OF SHIFT PHOTOCONDUCTIVITIES

We present a symmetry analysis of the stacking-dependent shift photoconductivities. Given the correspondence between
electric polarization and shift photocurrents derived above, the analysis parallels the symmetry analysis of the local in-plane
electric polarization in Ref. [10].
We choose the vector n̂ to point along the diagonal of a supercell. Along the n̂ direction, the order of configuration space
stackings follows as: AA, AB, DW, BA, AA. According to Ref. [10], the local polarization satisfies,
P(x) · n̂ = P(−x) · n̂.

(27)

under the present mirror symmetry m : x → −x. Analogously, the shift photoconductivity vectors, as defined in the main text,
satisfy,
σ(x) · n̂ = σ(−x) · n̂.

(28)

Moreover, under C3 symmetry present in t-hBN, the following conditions are satisfied
σ x,xx (x) = −σ x,yy (x) = −σy,xx (x) = −σy,xy (x),
which in the context of transition metal dichalcogenides (TMDs) was also identified in Ref. [15].

(29)

10
SUPPLEMENTARY NOTE 8: EFFECTIVE TIGHT-BINDING MODELS

For completeness, we further detail the form of the tight-binding hopping elements used in the tight-binding Hamiltonian
detailed in Methods. The interlayer coupling constants used in the model, as also defined in Methods, read [12, 16],


3 
3 
X
X



∗
tb
∗2
−ik·∆R
2
ik·∆R

 eik·x ,
i
i
tvc,k (x) = αk βk [tBb Bt (x) − tNb Nt (x)] + βk
tNb Bt ,i (x)e
− αk
tBb Nt ,i (x)e

i=1
i=1
(30)


3 
3 
X
X



bt
tN∗ b Bt ,i (x)eik·∆Ri  e−ik·x .
t∗Bb Nt ,i (x)e−ik·∆Ri − α2k
tvc,k
(x) = αk β∗k [t∗Bb Bt (x) − tN∗ b Nt (x)] + β∗2
k
i=1

i=1

where ∆Ri are displacement vectors between the atoms in the subscripts. In the above αk and βk are the coefficients of the Bloch
orbitals in the standard graphene/hBN Hamiltonian on a monolayer honeycomb lattice in the presence of a diagonal mass term
mσz = diag(m, −m) [17]:
X
X
uv,k = αk
eik·[(R)i +rB ] |Bi ⟩ + βk
eik·[(R)i +rN ] |Ni ⟩ ,
(31)
i

uc,k = (βk )∗

i

X
i

eik·[(R)i +rB ] |Bi ⟩ − αk

X
i

eik·[(R)i +rN ] |Ni ⟩ .

(32)

Here, (R)i is the lattice vector of the i-th unit cell, rB/N are the relative positions of boron (B) and nitrogen (N) atoms with respect
to the unit cell centers, and |Bi ⟩, |Ni ⟩ denote the boron/nitrogen orbitals in the unit cell i, correspondingly.
The stacking-dependent hoppings can be further implemented to obtain effective eigenstates and band structures, as detailed
in Methods. For completeness, we present an effective band structure obtained for the AA, AB, and DW stackings within the
presented tight-binding model, see Fig. 2. Note that in the Supplementary Information, the convention for identifying the A and
B atoms with boron and nitrogen is opposite to that used in Ref. [10] and in the main text.

SUPPLEMENTARY FIG. 2: Effective band structures obtained for the AA stacking (a), AB stacking (b), and DW stacking (c)
configurations within the effective tight-binding model. The band structure quantitatively matches the ab initio band structure
presented in the main text.

11
SUPPLEMENTARY NOTE 9: ADDITIONAL TIGHT-BINDING CALCULATIONS

We furthermore provide additional tight-binding calculations of optical responses within the effective model for twisted
hexagonal boron nitride (t-hBN). For different stackings, we include (i) joint density of states (JDOS), (ii) first-order optical
conductivities, (iii) optical weights, (iv) gauge-dependent shift vector and shift photoconductivity decompositions, (v) shift
photoconductivities at different frequencies, (vi) spectral mean shift photoconductivities at different stackings, (vii) interlayer
contributions and the spatial variations of the shift photoconductivities, (viii) integrated second-order shift photoconductivities,
(ix) frequency-resolved and integrated second-order injection photoconductivities.
Joint density of states

In Fig. 3, we present numerical JDOS obtained within the model (see the previous Section) at the AA, AB, and DW (domain
wall) stackings. We stress that in all cases, the dominant peak arises due to the resonant contributions from the M point of the
Brillouin zone (BZ), cf. the main text, which correspond to the van Hove singularities. Another peak contribution arises at the
frequency of the resonant transitions at the K point, as expected. While both characteristic points yield peak values in the JDOS,
it should be emphasized that it is the response at the frequency resonant for the M point that is relevant for deducing the local
polarization P(x). The latter is the consequence of the presence of dominant Berry connection Ann contributions at the edges
(rather than corners) of the BZ, which constitutes most of the electric polarizations evaluated within the configuration space
approximation.

SUPPLEMENTARY FIG. 3: The JDOS for optical transitions plotted as a function of the transition energy/∆0 (where ∆0 =
4.5 eV is the band gap at the BZ edge). As expected, there is a flattening of the JDOS profile near the energy of the largest band
gap (∼ 5.3 eV) over the different stackings (responsible for the first peak in the photoconductivities) and a sharp peak near the
saddle point energies (∼ 6 eV) in the dispersion relation (responsible for the second peak in the photoconductivities).

First-order optical conductivity

Photocurrents in moiré hBN can be investigated by first employing Eq. (8) to evaluate the first-order optical conductivities in
the presence of an oscillating electric field.
A spectrally resolved calculation of first-order conductivity can be carried out using Eq. (8) directly on replacing the δfunction with a Gaussian of suitable width. To that end, the integration was carried out over a smoother k-grid consisting of
469 k-points to calculate the conductivity as a function of transition energy ℏω. We show these in Figs. 4 (a-c) for the AA, AB
and DW stackings. However, it must be noted that despite the smoother grids for numerical integration and the wide Gaussian
approximations of the δ-function, the curves are still not as smooth as would be expected from an analytical integration.
The qualitative nature of the curve is expected from a consideration of the competition between the transition rate Qba
mn and
the density of states (DOS) g(ωmn ). While the former decreases as the transition energy increases, being the highest at the
edges of the BZ and decreasing upon moving towards the center [see Figs. 5(c), 5(d)], the DOS initially increases as transition
energy increases, before finally decreasing as well. This suggests the qualitative form in Figs. 4 (a-c), where the conductivity
initially increases from zero at the band gap owing to an increase in the DOS and then falls off after reaching a maximum
– owing to a decrease both in the transition rate and the DOS. Such a spectrally resolved calculation of the conductivity has
been performed for small transition energies in [18] using a superlattice potential model to describe the moiré system and a
Lorentzian to approximate the δ-function; the general qualitative nature of the initially increasing conductivity matches their

12

SUPPLEMENTARY FIG. 4: (a-c) Spectrally resolved calculations of first-order photoconductivities σ x,x and σy,y for stackings
(a) AA, (b), AB and (c) DW, as a function of optical transition energy/∆0 (where ∆0 = 4.5 eV is the band gap at the BZ edge). The
initial increase in conductivity can be attributed to an increase in the DOS that can undergo an optical transition at the relevant
transition energy, while the subsequent decrease is due to both a decreasing optical transition rate (∝ Qab
mn ) and a decreasing
DOS. Such a qualitative trend matches the results from a superlattice potential model in [18]. (d-e) First-order photocurrents
associated with the optical conductivity as a function of stacking direction x in response to (d) x-polarized and (e) y-polarized
light at frequency ωM = 6 eV. The current direction is found to be approximately parallel to the polarization of the electric field,
implying a negligible Hall response at first order. Also note that the qualitative dependence of the magnitude of the conductivity
is similar to that of the optical weight in Figs. 5 (a,b).
.

results. However, owing to the flatter bands associated with the superlattice potential model, the curve presented in [18] is not
as smooth as in Figs. 4 (a-c).
The vector plots of the first-order conductivity as a function of stacking in response to x- and y-polarized light at ωM = 6 eV
are also shown in Figs. 4 (d-e). Importantly, the results show that the current direction is approximately the same as the electric
field polarization, that is, there is no first order Hall response, and the qualitative dependence of the current magnitude on x is
similar to that of the relevant optical weight [owing to the Qab
mn factor in the integrand of Eq. (8)]. Moreover, the current direction
remains fairly uniform irrespective of the stacking. Since the stacking only enters the model via the (small) interlayer hoppings,
this suggests that the first-order conductivity is primarily an intralayer effect with the stacking-dependent interlayer effects only
providing small variations of the order of ∼ 3.5% on the background intralayer conductivity. This stands in contrast to the
electronic polarization, which was observed to be a strong function of the stacking, an artifact of the property that monolayer
hexagonal boron nitride is 3-fold symmetric, resulting in vanishing local polarization.

13
Optical weights

To further study the optical conductivities in the context of this work, we define generalized optical weights following
Ref. [19] as frequency-weighted integrals of the first-order AC conductivities,
α
≡
Wab

Z ∞
0

dω

σb,a (ω)
.
ωα

(33)

In the following, we choose α = 1, which allows to target the QGT integrated over the entire BZ in the zero-temperature limit
( fnm = 1):
1
=
Wab

Z ∞
0

dω

σb,a (ω) πe2 X
=
ω
ℏ m,n

Z

d2 k
f Qba .
2 nm mn
(2π)
BZ

(34)

Similarly to the approach for polarization above, the α = 1 optical weight can be calculated as a function of x as a proxy of the
optical absorption rate in the material. Using Eq. (34) and numerically integrating over a k-grid of 169 k-points for 37 different
1
1
1
stackings in the unit cell, W xx
and Wyy
have been plotted in Figs. 5 (a,b). Note that owing to W xy
being two orders of magnitude
1
1
smaller than W xx and Wyy , it has been assumed negligible and not shown here.
Since the photoconductivities to be explored subsequently all involve factors of Qab
mn in their integrands, it is useful to study
its dependence on k in the BZ. Figures Figs. 5 (c,d) show this dependence for DW stacking; note that as with the trace of the
QGT in the main text, Qab
mn is largest at the edge of the BZ where the optical transition energy is the smallest. Importantly, the
significance of the combination of the shift responses to x- and y-polarized light in σ is further highlighted here: only by adding
the two responses is the complete BZ edge and consequently, all of the dominant contribution to the polarization included in the
shift current integral.

Shift vectors and shift photoconductivity decomposition

In this Section, we demonstrate how the individual contributions of the shift vector decomposed in Eq. (12) contribute to the
shift photoconductivities. In particular, we show that by choosing an appropriate gauge, the last term can be made orders of magnitude smaller compared to the diagonal terms of non-Abelian Berry connection that contribute to the net electric polarization.
We show the contributions of the individual terms over stacking in Fig. 6. In that context, we decompose the shift photoconc,ab
c,ab
ductivities as σshift
(x) = σc,ab
P (x) + σArg (x), where band-diagonal Berry connection contribution to the shift photoconductivity

reads: σc,ab
P (x) [Fig. 6(a)], whereas the contribution to the shift photoconductivities due to the non-Abelian Berry connection
phase, i.e. the argument/phase/logarithm term reads: σc,ab
Arg (x) [Fig. 6(b)]. As predicted, the argument term is an order of magnitude smaller than the polarization term and can be made vanishing in the optical gauge (not shown). In Fig. 6(c), we show the
conduction band contributions to the first term resolved in k-space. Notably, the conduction band contributions are equal and
opposite to the valence band contributions, as featured in the main text. In Fig. 6(d), we show the difference of conduction and
valence Berry connections entering the shift vectors (Rcmn ≈ Acmm − Acnn ), which approximately equal twice the conduction band
Berry connection contributions (corresponding to the negative of the electric polarization), as claimed in the considered moiré
Hamiltonians.
It should be stressed again, as mentioned in the Methods, that under the optical gauge, the last (phase) term can be made
vanishingly small. This allows to fully exploit and explore a direct connection between the shift photoconductivities and the
electric polarization [13, 20].

Shift photoconductivities at different frequencies

In Fig. 7, we show that the shift photocurrent vortices associated with the local electric polarization can be observed in a
broader frequency range ω (in twisted hBN, ω = 5.9 − 6.7 eV). Therefore, the deduction of the electric polarization textures
from the shift photocurrents is not limited to the resonant frequency ωM = 6.0 eV studied in the main text, and is robust for a
lasing frequency window around the peak resonant frequency. Intuitively, the reason for the robustness is associated with the
fact that these nearby frequencies still probe transitions in regions where the diagonal Berry connection is strong and contributes
dominantly to both the electronic polarization and the shift photoconductivity.

14

SUPPLEMENTARY FIG. 5: (a-b) Optical weights for α = 1 for an (a) x-polarized and (b) y-polarized driving electric field as
1
a function of the stacking vector x. W xy
is negligible compared to these contributions and is therefore not shown. (c-d) Q xx and
Qyy summed over all valence-to-conduction interband transitions plotted over k in the BZ for DW stacking. As noted in the main
text, adding the responses to x- and y-polarized light in σ ensures that Q xx and Qyy are added, and the entire BZ edge is probed.

Spectral mean local shift photoconductivities

In Fig. 8, we demonstrate spectral mean local shift photoconductivities over different stacking. In the next subsection, we further contrast these findings with the spatially-resolved variations around the mean values. While the mean values are dominated
by the intralayer contributions, we further attribute the variations to the interlayer contributions that are induced by the relative
bilayer stacking.
As earlier with the first-order response, the homogeneity of the shift current direction with stacking vector indicates that intralayer effects dominate, an outcome that is expected since an optical transition from the valence to conduction bands effectively
involves the Wannier center shifting from the near the N atoms to near the B atoms, a non-zero change even within a single layer.

15

SUPPLEMENTARY FIG. 6: (a) Band-diagonal Berry connection contribution to the shift photoconductivity vector, σP (x),
which reflects the change of electric polarization on interband optical transitions. (b) Contribution to the shift photoconductivities
due to the non-Abelian Berry connection phase, i.e. the argument (Arg) term, σArg (x). We observe that under the chosen
fixed gauge, the latter is an order of magnitude smaller [σP (x) ≫ σArg (x)]. (c) Berry connection in the conduction bands,
Acc (k). In the main text, the Berry connection in the valence band, contributing to both the local polarization and local shift
photoconductivities, was presented. We observe that in the moiré Hamiltonian defining the effective model, manifestly: Acc (k) ≈
−Avv (k). (d) Differences of Berry connections in conduction and valence bands entering the shift vector R(k). We observe that
the shift vector magnitude |R(k)| doubles the value of |Avv (k)| across the BZ, consistently with the model introduced in Methods.
Interlayer contributions and the variation of local shift photoconductivities

Having established the uniformity in direction in the various shift photoconductivity components,
is interesting to investigate
R d2 x itc,ab
c,ab
the deviation of the shift current response from the mean. More precisely, δσc,ab
=
σ
−
σ
Acell shift , where Acell is the area
shift
shift
of the unit cell in real space. This has been plotted for the xx, xy, and yy electric field stimuli in Fig. 9. As expected, these
deviations show a strong dependence, both in magnitude and direction, on x. Note that the plots in response to the xx and yy

16

SUPPLEMENTARY FIG. 7: Shift photoconductivity vector σ(x) in twisted boron nitride (t-hBN) plotted over stacking at
different frequencies: (a) ω = 5.9 eV, (b) ω = 6.3 eV, and (c) ω = 6.7 eV. As in the main text, where we analogously demonstrate
σ(r) at the resonant frequency ωM = 6.0 eV, the shift photoconductivity vectors σ here too are antiparallel to the in-plane
polarization. We find that this feature is robust within an extended frequency range ω = 5.9 − 6.7 eV, showing that a lasing
frequency window, rather than a single resonant frequency, is admitted by the effect. As might be expected, at the edges of this
frequency window [as in (c)], while the direction remains anti-parallel to the polarization, the magnitudes are no longer reliable.

SUPPLEMENTARY FIG. 8: Spectral mean shift photoconductivities over different stackings in response to (a) x-polarized, (b)
xy-mixed, and (c) y-polarized electric field stimuli. The variations around the mean shift photoconductivities values are shown
in Fig. 9. The shift photoconductivities respect the crystalline symmetries of the bilayer subject to the oscillating electric fields.

stimuli show a winding across the unit cell similar to the polarization textures shown in the main text.
The variations of the the local shift photoconductivities can be attributed to the interlayer contributions induced on stacking
two twisted layers, see Fig. 9. It should be stressed that these terms vanish completely in the limit of (infinitely) separated
monolayers.

Integrated shift photoconductivities

Furthermore, the second-order optical response Eq. (11) can be used to calculate the total integrated shift photoconductivity.
To that end, the responses to ‘white light’ were found (that is, Eq. (11) was integrated over ω to remove the δ-function), and the
numerical integration in the BZ was carried out over a k-grid consisting of 169 k-points for 37 different stackings. The results
are presented in Fig. 10 as separate vector plots over x for the current direction in response to xx, xy, and yy stimuli.
Importantly, Fig. 10 (d) presents the integrated shift photoconductivity vector σ as a function of stacking and shows that in
addition to shift responses measured near ωM , an integrated response is also antiparallel to the electronic polarization texture.
Hence, it can equally be used as a probe for the same deductions. However, care must be taken to ensure
that such an integrated
R
shift method is not relied upon at small polarization magnitudes, as evidenced by the behaviour of σ dω near the AA stacking.

17

SUPPLEMENTARY FIG. 9: Interlayer contributions to local shift photoconductivities (a-c), and deviations from the mean of
the shift photoconductivities (d-f) as a function of stacking direction in response to: (a,d) xx, (b,e) xy, and (c,f) yy electric field
stimuli.

18

SUPPLEMENTARY FIG. 10: (a-c) Integrated shift photoconductivities as a function of stacking, in response to (a) xx, (b) xy,
and (c) yy electric field stimuli. As with the first-order conductivities in Figs. 4 (d-e), an approximately uniform current direction
over stacking implies dominant intralayer effects. (d) Summed shift photocurrents σ(r) in a vectorized form, cf. main text, as
a function of stacking. This is antiparallel to the in-plane polarization texture as well (except near AA) and can also serve as a
tool for probing the polarization in addition to measuring σ near ωM .

Second-order injection photocurrents

At second order in the driving electric field, Eq. (10) can be used to calculate the injection photoconductivities. Notably, the
magnitudes of the injection responses realized in t-hBN to linearly polarized light are negligibly small and should not interfere
with measurements of σ, as mentioned in the main text. For both frequency-resolved injection photoconductivities and vector
plots of injection responses as a function of stacking, see Fig. 11. Owing to the negligibly small magnitudes of the injection
responses to linearly polarized light, these components are not shown. Contrary to first-order and shift responses, the strong
dependence of the injection currents on x suggests that the intralayer contributions to injection currents are negligible and the
interlayer effects dominate.

19

SUPPLEMENTARY FIG. 11: (a) Frequency-resolved injection photoconductivities at the DW stacking in response to xy electric
field stimuli. (b) Injection photoconductivities at the M point resonant frequency ωM , as a function of stacking in response to
an xy electric field. The σy,xy
inj component vanishes at the DW consistently with the spectrally resolved photoconductivities in
panel (a). (c) Integrated injection photoconductivities as a function of stacking in response to an xy electric field stimulus. σc,xx
inj
c,yy
c,yy
and σinj
are negligible and hence not shown here. Importantly, such a vanishing of σc,xx
and
σ
increases
the
experimental
inj
inj
c,yy
accessibility to the electric polarization-related σc,xx
shift and σshift . Additionally, upon a comparison of the units in these plots (see
the text), it can be concluded that for mean-free-time τ ∼ 10−15 s, injection currents are an order of magnitude smaller than the
shift ones, deeming these unlikely to be visible in an experiment.

The ratio of the units between the shift and injection current magnitudes is 1 : 2 ℏeV τ ∼ 1 : 1 (for τ ∼ 10−15 s), which implies
that injection effects are an order of magnitude smaller than shifts and are likely to not be significant in experimental observations
of second-order effects. Furthermore, owing to the dependence of the injection currents on mean-free-time τ, it is possible to
tune them out by employing experimental methods that decrease τ such as increasing the temperature and thus increasing the
number of activated phonon modes in the phonon-mediated resistivity regime, or by increasing the defect concentration in the
defect-mediated resistivity regime.

20

[1] J. Provost and G. Vallee, Commun. Math. Phys. 76, 289 (1980).
[2] D. Vanderbilt, Berry phases in electronic structure theory: electric polarization, orbital magnetization and topological insulators (Cambridge University Press, 2018).
[3] J. Ahn, G.-Y. Guo, and N. Nagaosa, Phys. Rev. X 10, 041041 (2020).
[4] J. Ahn, G.-Y. Guo, N. Nagaosa, and A. Vishwanath, Nat. Phys. 18, 290 (2021).
[5] J. E. Sipe and E. Ghahramani, Phys. Rev. B 48, 11705 (1993).
[6] J. E. Sipe and A. I. Shkrebtii, Phys. Rev. B 61, 5337 (2000).
[7] R. King-Smith and D. Vanderbilt, Phys. Rev. B 47, 1651 (1993).
[8] S. Carr, D. Massatt, S. B. Torrisi, P. Cazeaux, M. Luskin, and E. Kaxiras, Phys. Rev. B 98, 224102 (2018).
[9] D. Bennett, Phys. Rev. B 105, 235445 (2022).
[10] D. Bennett, G. Chaudhary, R.-J. Slager, E. Bousquet, and P. Ghosez, Nat. Commun. 14, 1629 (2023).
[11] D. Bennett, W. J. Jankowski, G. Chaudhary, E. Kaxiras, and R.-J. Slager, Phys. Rev. Res. 5, 033216 (2023).
[12] W. J. Jankowski, D. Bennett, A. Agarwal, G. Chaudhary, and R.-J. Slager, Phys. Rev. B 110, 085429 (2024).
[13] B. M. Fregoso, T. Morimoto, and J. E. Moore, Phys. Rev. B 96, 075421 (2017).
[14] D. Vanderbilt and R. King-Smith, Phys. Rev. B 48, 4442 (1993).
[15] C. Hu, M. H. Naik, Y.-H. Chan, J. Ruan, and S. G. Louie, PNAS 120, e2314775120 (2023).
[16] H. Yu, Z. Zhou, and W. Yao, Sci. China Phys. Mech. Astron. 66, 107711 (2023).
[17] A. H. Castro Neto, F. Guinea, N. M. R. Peres, K. S. Novoselov, and A. K. Geim, Rev. Mod. Phys. 81, 109 (2009).
[18] H. Ochoa and A. Asenjo-Garcia, Phys. Rev. Lett. 125, 037402 (2020).
[19] Y. Onishi and L. Fu, Physical Review X 14 (2024).
[20] R. Resta, Phys. Rev. Lett. 133, 206903 (2024).

