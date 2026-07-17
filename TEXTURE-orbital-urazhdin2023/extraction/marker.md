<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2309.04442 -->

Symmetry constraints on the orbital transport in solids
Sergei Urazhdin
Department of Physics, Emory University, Atlanta, GA, USA.

arXiv:2309.04442v2 [cond-mat.mtrl-sci] 16 Nov 2023

We show that electron interaction with the crystal lattice imposes stringent symmetry constrains
on the atomic orbital moment propagation. We present examples that elucidate the underlying
mechanisms and reveal an additional effect of ultrafast orbital moment oscillations not captured by
the semiclassical models. The constraints revealed by our analysis warrant re-interpretation of prior
observations, and suggest routes for efficient orbitronic device implementation.

Spin-electronic phenomena such as spin transfer
torque (STT) [1], Rashba-Edelstein and spin Hall effect
(SHE) [2, 3] have attracted intense interest as important manifestations of the interplay between electron’s
spin and orbital degrees of freedom, with applications
in sensing and information technology. SHE, one of the
most promising mechanisms for spin current generation,
is facilitated by spin-orbit coupling (SOC), which couples spin to chiral orbital transport [4]. Bypassing the
requirement for a large SOC, and directly using orbital
moments may enable efficient low-cost orbitronic devices
based on light elements instead of the heavy metals in
SOC-based devices [5]. This possibility has motivated
a flurry of research into orbital moment generation and
transport effects analogous to those involving spin, including orbital Hall effect (OHE) as a counterpart to
SHE enabling efficient generation of orbital moment in
light transition metals [6–10] illustrated in Fig. 1, orbital
torque that similarly to STT may enable control of magnetic moments [11–13], and long-range orbital moment
transport [14–16]. However, the differences between spin
and orbital counterparts remain largely unexplored.

moving in the potential U (r), this relation is [7, 11]

Spin carried by the Bloch waves is only weakly perturbed by the lattice via SOC. In contrast, we show below
that atomic orbital moment dynamics can be dominated
by interaction with the lattice potential even in the absence of SOC. The resulting effects are dependent on the
orientation of the orbital moments and the propagation
direction, imposing hitherto largely unrecognized symmetry constraints on orbitronic device geometries and
structure qualitatively distinct from spintronics.

which signifies the conservation of orbital angular momentum, enabling control of the local orbital moment in
a certain volume by its injection into this volume, for
example via OHE. However, if the torque dominates the
dynamics described by Eq. (1), orbital current produced
by OHE cannot be used to control orbital moments. In
particular, accumulation of orbital moment generated
by OHE can be prevented by its precession due to the
crystal-field torque analogous to spin precession due to
the Larmor torque produced by the magnetic field.
To elucidate the effects of orbital torque, consider the
z-component of orbital angular momentum L̂z = xpˆy −
y p̂x = −ih̄∂/∂ϕ, where ϕ is the polar angle in cylindrical
coordinates. The corresponding component of torque is

The concept of transport of physical quantities emerges
from the relations connecting their local variations to
flux. For the density operator ˆlα (r, t) of αth component
of orbital angular momentum L̂ = r × p̂ of an electron

j

(a)

jSz

(b)
j

∂ ˆlα (r, t)
= −∇ · q̂Lα + T̂α .
∂t

Here, q̂Lα is the density of the orbital angular momentum
current
Q̂Lα = {L̂α , v̂}/2,

Figure 1. Analogy between SHE (a) and OHE (b).

(2)

where v̂ is the electron velocity operator, and T̂α is the
density of the αth component of orbital torque
Γ̂ =

i
[U, L̂] = r × F(r)
h̄

(3)

exerted by U (r), where F = −∇U is the force.
According to Eq. (1), the rate of variation of angular
momentum in a unit volume is determined by its flux
through the boundary plus the torque exerted by U . In
the absence of torque, it reduces to the continuity relation
∂ lˆα (r, t)
= −∇ · q̂Lα ,
∂t

Γ̂z = y

qLz

(1)

∂U
∂U
∂U
−x
=−
.
∂x
∂y
∂ϕ

(4)

(5)

As expected from the Noether’s theorem, the continuity
relation Eq. (4) is satisfied if the potential is symmetric
with respect to rotation around the z-axis.
In crystals, continuous rotational symmetry is broken
by the lattice. Nevertheless, if the Fermi surface is welldescribed by the free electron approximation, the effects

2
of lattice potential are small so the continuity equation
Eq. (4) is expected to provide a good approximation for
orbital dynamics. This can be seen from Eq. (5). If
the wavefunction does not significantly vary over the lattice constant, one can replace ∂U
∂ϕ with its integral over a
sphere centered at r = 0, which identically vanishes.
In orbitronic devices based on transition metals [7–
9, 13], most of the angular momentum is expected to be
carried by the atomic moments of d-electrons, for which
such an averaging procedure is unjustified since the wavefunction phase varies over at least 2π within a single
atomic site. Our main result is the prediction of a large
non-classical orbital crystal torque which can suppress
certain components of propagating orbital moment over
essentially a single lattice constant. The identified mechanism does not contradict the possibility of local orbital
moment generation via OHE or its importance as the
mechanism underlying SHE [17]. Nevertheless, it places
stringent constraints on the possibility of atomic orbital
moment diffusion and accumulation over distances exceeding a few lattice constants [11, 17].
First, we consider the conduction band of complex
transition metal oxides exemplified by SrTiO3 , which
is dominated by the t2g orbitals of the transition metal
atoms on a cubic lattice [18, 19]. Each of the t2g orbitals
hybridizes via oxygen atoms located on the lines between
transition metal atoms with only four of the six nearest
neighbors, e.g. the dxy orbital hybridizes with four dxy
orbitals of the nearest neighbors in the xy plane [19, 20].
The corresponding tight-binding Hamiltonian is
X
Ĥ = −V
(1 − δl,m )ĉ+
(6)
n+l,m,s ĉn,m,s ,
n,l,m,s

where dm = (dyz , dxz , dxy ), the operator ĉ+
n,m,s creates an
electron on site n with spin s in the orbital state m, l is
a unit vector in one of the six principal directions, and V
is the hopping matrix element describing orbital-selective
hybridization. In the reciprocal space,
X
Ĥ =
ϵm (k)ĉ+
(7)
k,m,s ĉk,m,s ,
k,m,s

P iakn +
√1
ĉn,m,s , N
where ĉ+
ne
k,m,s =
N

is the number of
lattice sites, a is the lattice constant, with dispersion
X
ϵm (k) = −2V
cos(km′ a).
(8)
m′ ̸=m

This spectrum is orbitally degenerate along the planes
ki = kj , which allows Bloch states to carry angular momentum [21]. Consider, for example, a superposition of
the Bloch states formed by orbitals dxz and dyz ,
1
+ iσĉ+
ψk,σ,s = √ (ĉ+
k,yz,s )|0⟩,
2 k,xz,s

(9)

where σ = ±1. They are stationary states (Bloch waves)
in the two planes kx = ±ky at the intersection between
the dyz and dxz sub-bands.

The contribution to orbital moment from the crystalline momentum identically vanishes for the plane wave
by symmetry. On the other hand, the z-component of the
atomic orbital momentum carried by this wave is
X
ˆlz (n)|ψσ,k,s ⟩ = σh̄,
⟨Lˆz ⟩ = ⟨ψσ,k,s |
n

where lˆz (n) is the z-component of atomic angular momentum on site n, and we used lˆz dxz = idyz , lˆz dyz =
−idxz .
Because of the anisotropy of the subbands ϵxz (k),
ϵyz (k), the component dxz of the wave cannot propagate in the y-direction, while the component dyz - in
the x-direction. Thus, the dispersion of the wavepackets
formed by the states Eq. (9) is minimized for wavevectors
along the z-axis. We conclude that orbital momentum
along one of the principal axis is conserved by electrons
propagating along this axis. The conservation of orbital
angular momentum is ensured by the orbital selectivity of
hopping, making complex oxides attractive for orbitronic
applications. The requirement L ∥ k for orbital moment
conservation has been identified for other materials [21],
and will be shown in another example below, suggesting
its general importance.
For kx ̸= ±ky , ψσ,k,s is not a stationary state, resulting
in the evolution of the relative phase between its dxz and
dyz components according to
1
+ieit(ϵ2 (k)−ϵ1 (k))/h̄ σĉ+
ψσ,k,s (t) = √ (ĉ+
k,1,s )|0⟩. (10)
2 k,2,s
This state is characterized by the oscillating angular momentum
⟨L̂z ⟩ = σh̄ cos[t(ϵ2 (k) − ϵ1 (k))/h̄].
The flux divergence vanishes, so this oscillation cannot
be described by the continuity relation Eq. (4). It results
entirely from the torque exerted by the crystal potential
described by the orbitally-selective Hamiltonian. The expectation values of both L̂x and L̂y remain zero, so the
oscillation cannot be interpreted as precession of semiclassical angular momentum vector. Using V = 0.2 eV,
we estimate that the frequency of oscillation ranges from
zero at the center of the Brillouin zone (BZ) to 1014 Hz
at the BZ boundary along the kx or ky axes.
The underlying mechanism is similar to STT in ferromagnets [1, 22]. In STT, an electron is injected into a
ferromagnet with its spin polarization non-collinear with
the magnetization. Since the band structure is split into
spin-dependent sub-bands, this state is not an eigenstate
of the Hamiltonian, resulting in oscillation of the relative
phase between the spin-up and spin-down components
of the wavefunction manifested as spin precession. This
dynamics involves angular momentum exchange between
the magnetization and the injected spin producing STT.

3
(a)

4

(b)

6

3
dyz
dxz 1

dxz 2

dyz
5

y
x

Γ
r

F2

Lz>0

Lz<0

site 1

site 2

Figure 2. (a) Orbitally-selective hopping of electron initially
localized on site 1 in a cubic complex oxide. (b) Mechanism
of orbital selectivity of hopping in the direction transverse to
the orbital moment.

In the considered example of orbital dynamics, the role
of exchange torque is played by the orbital torque produced by the crystal potential, and the reciprocal effect
of this torque is a periodic rotation of the lattice. Semiclassical precession of orbital moment is not possible in
this case, because angular momentum operator does not
have matrix elements between ψ+,k,s and ψ−,k,s .
Since orbital dynamics depends on the wavevector, oscillation of the orbital moment carried by a wavepacket
decays due to dephasing between different momentum
components, similar to spin dephasing in STT [1, 22].
Consider a Gaussian wavepacket centered around k0 ∥ x̂
and wavevector spread ∆k. The orbital moment dephases over the time interval
∆t =

1
h̄
=
,
∂ϵ2
∆kv
∆k ∂k
|
g
k=k0
x

where vg is the group velocity. Since the wavepacket
width is ∆x = ∆k −1 = vg ∆t, the components of orbital
moment orthogonal to the direction of propagation decay
over the packet width.
To elucidate the underlying microscopic mechanism,
we consider an electron with orbital moment Lz = h̄ initially localized on site 1, Fig. 2(a). Based on the above
analysis, orbital moment is expected to decay as the
wavefunction spreads over the wave packet width, in this
case a single lattice spacing. Indeed, because of the orbital selectivity of hopping, orbital component dxz flows
to sites 2 and 4 along the x-axis, while orbital component
dyz flows to sites 3 and 5 along the y-axis. The same orbital selectivity prevents reconstruction of the finite-Lz
orbital state by mixing between dxz and dyz along the
diagonal, as shown in Fig. 2(a) for site 6. Thus, a single electron hop along one of the principal axes quenches
orbital moment normal to this axis, on the time scale
∆t ∼ h̄/V ∼ 10−15 s. The possibility to transport Lz
in the xy plane by a wave packet with kx = ±ky is illusory, since the components dxz and dyz of the wave
packet propagate in orthogonal directions along the xand y-axes, respectively.
We now demonstrate similar symmetry constraints
on orbital moment dynamics for a system with a completely different symmetry, a triangular 2d lattice which

approximates a single {111} fcc plane or (0001) hcp
plane in transition metals studied in the context of
OHE [8, 9, 12, 13, 15, 16]. The hexagonal symmetry of
the crystal field of triangular lattice does not quench the
normal component of angular momentum of d-electrons,
providing a close approximation for the axial rotational
symmetry which according to Eq. (5) allows its conservation.
To the best of our knowledge, the d-orbital composition
of the Bloch states on the triangular lattice does not have
a simple form amenable to the analysis of orbital dynamics, due to the mismatch between d-orbital symmetries
and the lattice geometry [23]. We avoid this issue by considering an electron initially localized on a single site with
the projection Lz of orbital moment on the z-axis normal to the plane. We choose Lz = 2h̄ for concreteness,
but the results are similar for other values of Lz ̸= 0.
Orbital moment evolution is determined by hopping to
the six nearest neighbors. By symmetry, hopping amplitudes onto the same orbitals of different neighbors are the
same aside from the phase, so it is sufficient to consider
a single neighbor on the x-axis, Fig. 2(b). In the SlaterKoster method, hopping between neighboring d-orbitals
is described by the parameters Vddσ , Vddπ = −2Vddσ /3,
and Vddδ = Vddσ /6 [24]. Their specific values, which
can be calculated in the muffin-tin approximation, are
not important. The matrix elements VLz L′z (with indices scaled by h̄) describing hopping from Lz = 2h̄ onto
the orbitals L′z are V22 = 0.06Vddσ , V21 = V2−1 = 0,
V20 = −0.36Vddσ , V2−2 = 0.73Vddσ . The probability that
orbital moment is conserved on hopping is about 30 times
smaller than the probability that it is lost (L′z = 0), and
about 150 times smaller than the probability that it is
reversed.
This somewhat counter-intuitive orbital selectivity favoring orbital moment reversal results from the constructive interference between opposite-moment orbitals
which remain in phase over the region of their overlap
illustrated by curved arrows in Fig. 2(b), as opposed
to partially destructive interference of same-moment orbitals. Qualitatively, electron initially moving counterclockwise (Lz > 0) around site 1 in the region between
the sites, is moving clockwise with respect to site 2. As
a consequence, there is a finite probability that it continues its motion as clockwise rotation around site 2, i.e.
hopping tends to flip orbital moment normal to the hopping direction. The vanishing amplitudes V2±1 ensure
that orbital moment remains normal to the plane, i.e.
the evolution is non-classical as in the previous example.
To put this dynamics in the framework of the continuity relation Eq. (1), consider a volume surrounding site 1
and its nearest neighbors, such that at sufficiently short
times the flux through its surface is negligible. The relaxation of orbital moment is caused by the crystal orbital
torque exerted on the electron as it hops from site 1 to
its nearest neighbors and is this directly related to the

4
hopping mechanism itself, as illustrated in Fig. 2(b).
We conclude that hopping in the direction normal to
the orbital moment results in its relaxation over a single lattice constant. On the other hand, similar analysis
for the orbital moment initially aligned with the x-axis
shows that orbital moment along the hopping direction
is conserved, as in the previous example. Thus, despite
substantial differences between the two considered systems, both exhibit the same symmetry constraints on
the atomic orbital moment dynamics in relation to hopping direction. In contrast to cubic complex oxides, for
the hexagonal 2d lattice crystal torque-mediated orbital
relaxation occurs for any in-plane moment direction, because hopping to at least some of the six nearest neighbors is always non-collinear with the orbital moment. By
the same argument, relaxation within distances comparable to the lattice constant is expected for any orbital moment direction on the 3d fcc or hcp lattice. This conclusion is consistent with numeric calculations, which show
that orbital moment accumulation due to OHE in transition metals is limited to a few atomic constants from
their surfaces or interfaces [11, 17, 25].
In summary, we analyzed two systems whose highly
symmetric crystal fields allow unquenched atomic orbital
moments. Our analysis reveals a dramatic anisotropy of
atomic angular momentum dynamics dependent on its
direction relative to electron transport and crystal axes,
placing stringent symmetry constraints on the possible
structure and geometry of orbitronic devices. Orbitallyselective electron hopping along principal axes in cubic
transition metal oxides such as SrTiO3 preserves the component of atomic orbital moment in the hopping direction, making such materials particularly attractive for
orbitronic applications. On the other hand, the normal
component of atomic orbital moment is suppressed over
essentially a single lattice spacing, making it impossible
for this moment to propagate transverse to its direction
or to locally accumulate in a small volume away from interfaces. We also demonstrate the possibility of orbital
moment oscillations induced by lattice potential analogous to spin precession induced by the exchange field of
ferromagnets. Thus, in contrast to spin, orbital moments
can be controlled by the electron wavevector, without
the need for magnetic fields, orbital moment injection or
SOC. One can expect rapid relaxation of orbital moment
injected into fcc or hcp transition metals, since at least
some of the electron hopping is always non-collinear with
the orbital moment. This does not contradict the existence of OHE or its importance for orbital moment generation and SHE. Nevertheless, it places stringent constraints on the geometry and crystal structure of devices
where atomic orbital moment is generated by OHE in
one material, and is injected into another. On the other
hand, the interatomic contribution to orbital moment is
not constrained by the identified relaxation mechanism,
warranting more detailed analyses of different contribu-

tions to orbital moment transport.
Recent observations of anomalous current-induced
torques in transition metal-based magnetic heterostructures were attributed to orbital moment generation via
OHE and its long-range propagation through transition
metals such as Pt and Ni [15, 16]. In the studied geometries, OHE generated orbital moments parallel to the
thin-film interfaces, which were assumed to become injected across the interfaces and diffuse through a significant thickness of ferromagnetic layers. This is precisely
the transverse geometry that according to our analysis
does not allow for atomic orbital moment transport. It is
possible that the observed effects resulted entirely from
the interatomic orbital moment contribution. We also
propose two alternative explanations for the anomalous
observations. First, orbitally-selective hopping in transition metals can stabilize an orbital liquid − an orbitally
correlated state of electrons that cannot be described in
single-particle terms and can exist in both magnetic and
non-magnetic materials [23]. Orbital correlations are ferromagnetic in the direction normal to the orbital moment, and may mediate long-range orbital torques by
analogy to the spin exchange stiffness in ferromagnets.
This many-particle mechanism is consistent with the interpretation in terms of orbital moments, but cannot be
described by the single-particle picture.
One of the central experimental observations attributed to the orbital moment injection is the variation
of STT effects at large ferromagnet thicknesses [15, 16]
inconsistent with the usual STT whose length scale of
a few atomic spacings is determined by the rapid dephasing of precession of spin transverse to the magnetization [1, 22]. In contrast, the collinear to the magnetization spin propagates over a much larger longitudinal
spin diffusion length. The observed long-range effects
may thus be associated with the longitudinal spin transfer whose role in current-induced phenomena remains
poorly understood [26, 27]. These possibilities warrant
more detailed studies of the symmetries underlying spin
and orbital transport in solids.
This work was supported by the NSF award ECCS2005786.

[1] J. Slonczewski, Journal of Magnetism and Magnetic Materials 159, L1 (1996).
[2] M. Dyakonov and V. Perel, Physics Letters A 35, 459
(1971).
[3] E. I. Rashba, Journal of Superconductivity 18, 137
(2005).
[4] J. Sinova, S. O. Valenzuela, J. Wunderlich, C. H. Back,
and T. Jungwirth, Rev. Mod. Phys. 87, 1213 (2015).
[5] T. Jungwirth, J. Wunderlich, and K. Olejnı́k, Nature Materials 11, 382 (2012).
[6] H. Kontani, T. Tanaka, D. S. Hirashima, K. Yamada,

5
and J. Inoue, Phys. Rev. Lett. 100, 096601 (2008).
[7] T. Tanaka, H. Kontani, M. Naito, T. Naito, D. S. Hirashima, K. Yamada, and J. Inoue, Phys. Rev. B 77,
165117 (2008).
[8] H. Kontani, T. Tanaka, D. S. Hirashima, K. Yamada,
and J. Inoue, Phys. Rev. Lett. 102, 016601 (2009).
[9] D. Jo, D. Go, and H.-W. Lee, Phys. Rev. B 98, 214405
(2018).
[10] A. Pezo, D. Garcı́a Ovalle, and A. Manchon, Phys. Rev.
B 106, 104414 (2022).
[11] D. Go, F. Freimuth, J.-P. Hanke, F. Xue, O. Gomonay,
K.-J. Lee, S. Blügel, P. M. Haney, H.-W. Lee, and
Y. Mokrousov, Phys. Rev. Res. 2, 033401 (2020).
[12] S. Lee, M.-G. Kang, D. Go, D. Kim, J.-H. Kang, T. Lee,
G.-H. Lee, J. Kang, N. J. Lee, Y. Mokrousov, S. Kim,
K.-J. Kim, K.-J. Lee, and B.-G. Park, Commun. Phys. 4
(2021).
[13] G. Sala and P. Gambardella, Phys. Rev. Res. 4, 033037
(2022).
[14] D. Go, D. Jo, H.-W. Lee, M. Kläui, and Y. Mokrousov,
EPL 135, 37001 (2021).
[15] A. Bose, F. Kammerbauer, R. Gupta, D. Go,
Y. Mokrousov, G. Jakob, and M. Kläui, Phys. Rev. B
107, 134423 (2023).
[16] H. Hayashi, D. Jo, D. Go, T. Gao, S. Haku,

Y. Mokrousov, H.-W. Lee, and K. Ando, Commun. Phys.
6 (2023).
[17] D. Go, D. Jo, C. Kim, and H.-W. Lee, Phys. Rev. Lett.
121, 086602 (2018).
[18] Y. Tokura and N. Nagaosa, Science 288, 462 (2000).
[19] M. T. Dylla, S. D. Kang, and G. J. Snyder, Angewandte
Chemie International Edition 58, 5503 (2019).
[20] S. Urazhdin, E. Towsif, and A. Mitrofanov, Phys. Rev.
B 106, 224519 (2022).
[21] D. Go, D. Jo, K.-W. Kim, S. Lee, M.-G. Kang, B.-G.
Park, S. Blügel, H.-W. Lee, and Y. Mokrousov, Phys.
Rev. Lett. 130, 246701 (2023).
[22] D. C. Ralph and M. D. Stiles, Journal of Magnetism and
Magnetic Materials 320, 1190 (2007).
[23] S. Ivanov, J. Peacock, and S. Urazhdin, Phys. Rev.
Mater. 7, 014404 (2023).
[24] W. A. Harrison, Electronic Structure and the Properties
of Solids: The Physics of the Chemical Bond (Dover Publications, New York, 1989).
[25] D. Go, D. Jo, T. Gao, K. Ando, S. Blügel, H.-W. Lee,
and Y. Mokrousov, Phys. Rev. B 103, L121113 (2021).
[26] A. Zholud, R. Freeman, R. Cao, A. Srivastava, and
S. Urazhdin, Phys. Rev. Lett. 119, 257201 (2017).
[27] A. Mitrofanov and S. Urazhdin, Phys. Rev. Lett. 126,
037203 (2021).

