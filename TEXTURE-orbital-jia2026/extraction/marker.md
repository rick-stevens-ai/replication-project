<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2605.17462 -->

Geometry-Driven Nonlinear Orbital Magnetoelectric Eﬀect
Jinxiong Jia,1, 2 Zhenhua Qiao,1, 2, ∗ and Jian Wang3, 4, 5, †
1

arXiv:2605.17462v1 [cond-mat.mes-hall] 17 May 2026

International Center for Quantum Design of Functional Materials and Department of Physics,
University of Science and Technology of China, Hefei, Anhui 230026, China
2
Hefei National Laboratory, University of Science and Technology of China, Hefei 230088, China
3
College of Physics and Optoelectronic Engineering, Shenzhen University, Shenzhen 518060, China
4
Quantum Science Center of Guangdong-Hongkong-Macao Greater Bay Area (Guangdong), Shenzhen 518045, China
5
Department of Physics, The University of Hong Kong, Pokfulam Road, Hong Kong, China
We propose a nonlinear orbital magnetoelectric eﬀect, which generates orbital magnetization
quadratically in centrosymmetric materials where the linear orbital magnetoelectric eﬀect is strictly
forbidden. Using extended semiclassical formulation, we derive a gauge-invariant microscopic theory
that separates intrinsic and extrinsic contributions and establishes their distinct dependence on the
relaxation time, providing an experimental discriminator. In two-dimensional systems the nonlinear
response is far less constrained by out-of-plane rotational symmetries than the linear orbital magnetoelectric eﬀect, substantially enlarging the materials platform. Microscopically, the dominant
contributions are governed by a Hermitian-connection structure. Finally, we estimate that the magnitude of the nonlinear orbital magnetoelectric eﬀect lies within the sensitivity of state-of-the-art
magneto-optical Kerr measurements.

Introduction— Orbitronics in condensed matter physics
has attracted increasing attention in recent years [1–7].
Unlike spintronics, which manipulates the spin degree of
freedom of Bloch electrons electrically [8, 9], orbitronics explores generation and transport of orbital angular
momentum, opening new pathways for information processing and storage [10]. In particular, the orbital Hall
eﬀect, which generates a transverse ﬂow of orbital angular momentum in response to an applied electric ﬁeld, has
been theoretically predicted and experimentally observed
in various materials [11–17].
However, similar to the spin Hall eﬀect, the orbital
Hall current is conﬁned in-plane, resulting in orbital accumulation at the edges [11–13]. An alternative approach
is the orbital magnetoelectric eﬀect (OME), which converts an applied electric ﬁeld into a local orbital magnetization. The extrinsic OME has been demonstrated
to generate giant orbital torque, driving magnetization
switching in twisted bilayer graphene [18–21], while the
intrinsic OME has been recently formulated using both
semiclassical theory and response theory [22–24]. This
provides a promising route to electrically control the orbital degree of freedom. Nevertheless, since the orbital
angular momentum is an axial vector, the OME requires
inversion symmetry breaking and is therefore strictly forbidden in centrosymmetric materials. In two-dimensional
(2D) systems, the OME is further constrained by rotational symmetries. Speciﬁcally, any rotational symmetry
about the axis perpendicular to the 2D plane strictly forbids the OME [25], which signiﬁcantly limits the number
of candidate materials.
In this Letter, we propose a nonlinear orbital magnetoelectric eﬀect (NOME), in which an orbital magnetization is induced quadratically by an applied electric ﬁeld.
The NOME is characterized by a rank-3 pseudo-tensor
χc;ab , deﬁned as δM c = χc;ab Ea Eb , where summation

over repeated indices is implied. As the quadratic ﬁeld
term Ea Eb is even under inversion (P), the NOME is permitted even in centrosymmetric materials. Furthermore,
in contrast to the linear OME, the NOME is far less constrained by rotational symmetries (see Table I), making
it a promising platform for exploring orbital physics and
converting orbital magnetization into spin-orbit torque
in 2D materials.
Using an extended semiclassical formulation, we develop a microscopic theory that separates intrinsic and
extrinsic contributions. Owing to the singular nature of
the position operator in periodic crystals [17, 26], the
NOME comprises three distinct components: a conventional contribution driven by orbital angular momentum
matrix elements [17, 27], which has a direct counterpart
in nonlinear spin magnetization [28]; and two geometric
terms that are governed by the quantum geometric tensor and Hermitian connection. We show that both the
intrinsic and extrinsic NOME stem fundamentally from
the Hermitian connection.
Microscopic theory of NOME— Our analysis is based on
the extended semiclassical theory [22, 28, 29], which has
been successfully applied to a variety of nonlinear transport phenomena [30–32] and is known to be equivalent
to the quantum response theory [33]. Within this framework, the orbital magnetization δM c is given by [34]
Z
i
dk h
c
δM =
gn (ǭ)Ω̄cn + f¯n (ǭ)hW̄ |L̂c |W̄ i . (1)
d
BZ (2π)
Here, d is the spatial dimension and BZ the Brillouin
zone. L̂c = 41 εcαβ {r̂α − r0α , v̂ β } is the orbital angular momentum operator, where r0α denotes the center
of mass of the wavepacket [35]. The state |W̄ i represents the normalized wavepacket expanded up to second order in the electric ﬁeld [33]. The ﬁeld induced

2
Berry curvature is given by Ω̄cn = [∇ × (An + an )]c ,
α
where Aα
n = hunk |i∂k |unk i is the intraband Berry connection calculated from the periodic part of Bloch state
|unk i (satisfying H0 (k)|unk i = ǫnk |unk i), and aα
n is
33].
Furthermore,
the ﬁeld-induced positional shift [29,

gn = −kB T ln 1 + e−(ǭn −µ)/kB T is the grand potential density, f¯n is the non-equilibrium distribution function satisfying the Boltzmann equation, and ǭn is the
wave-packet energy up to second order in the electric
ﬁeld [33, 36, 37].
The ﬁrst and second terms in Eq. (1) correspond to
the revolution and self-rotation of the wave packet, respectively. Combining the zeroth- and ﬁrst-order wavepackets with the Boltzmann equation and Eq. (1), recovers the equilibrium orbital magnetization and linear
OME, respectively; the latter includes both intrinsic and
extrinsic contributions [34], in agreement with previous
ﬁndings [22, 23, 35, 38–43]. Finally, by substituting the
second-order wave-packet [33] and the expanded distribution function f (ǭ) into Eq. (1), we ﬁnd that the intrinsic
NOME comprises three distinct contributions:
(0)

(0,od)

(0,d)

(0,ic)

χc;ab = χc;ab + χc;ab + χc;ab .

(2)

Here, "od" denotes the conventional contribution from
the matrix elements P
of orbital angular momentum operator, Lcnm = 41 εcαβ ℓ {rα , v β }nm . In this expression,
a
rnm
= hunk |i∂ka |umk i (n 6= m) is the interband Berry
a
a
connection matrix, and vnm
= δnm ∂ka ǫn + iǫnm rnm
is
the velocity operator matrix with ǫnm = ǫn − ǫm . The
terms "d" and "ic" refer to the dipole-type and positional shift geometric contributions, respectively. Since
these geometric terms originate solely from the diagonal
part of position operator [17, 34], they are naturally described by the Hermitian connection, a gauge-covariant
interband geometric structure that governs nonlinear responses beyond the quantum geometric tensor by encoding the local unitary frame rotation of Bloch eigenstates
across momentum space. This connection is deﬁned
αab
α
a
b
αab
αab
as Cnm
= −ivnm
Dmn
rmn
/ǫnm = Cnm
− iFnm
/2 [44].
ab
Similarly, quantum geometric tensor is given by gnm
=
a
b
ab
ab
−ivnm rmn /ǫnm = Gnm − iΩnm /2 [44–46]. In these exa
pressions, Dmn
= ∂ka − i(Aam − Aan ) is the covariant
αab
αab
derivative, Cnm is the metric connection, Fnm
is the
ab
ab
symplectic connection, and Gnm and Ωnm are the local
quantum metric and Berry curvature, respectively. Using these deﬁnitions, the dominant intrinsic NOME takes
the form [34]

cab
cb
ab
X 
C¯nm
(0,od)
a Ḡnm
c Gnm
χc;ab =
fn L̄mn 2 + 2v̄nm 2 − 2
ǫnm
ǫnm
ǫnm
nm

G ab Lc
(3)
−fn′ nm n ,
ǫnm

εcαβ X  β
(0,ic+d)
β
αab
χc;ab
=
)Nnm
+ ∇β Lαab
fn (vn + vm
nm ,
4 nm
(4)

where fn is the Fermi-Dirac distribution function, fn′ =
a
∂fn /∂ǫn , v̄nm
= ∂ka ǫnm , and L̄cmn = Lcmm − Lcnn . The
components of Eq. (4) are deﬁned as
αa
αab
aαb
Fnm
+ Fnm
b Ωnm
+ v̄mn
,
2
3
ǫnm
ǫnm
αab
Fnm
Ωαa v̄ b
Lαab
+ nm2 mn .
nm =
ǫnm
ǫnm

αab
Nnm
=

(5)
(6)

ab
b
ab
We further deﬁne ḡnm
= −iLanm rmn
/ǫnm = Ḡnm
−
ab
cab
c
a
b
¯
iΩ̄nm /2 and Cnm = −Re iLnm Dmn rmn /ǫnm . These
ab
quantities share the same structural form as gnm
and
αab
Cnm , except that the velocity operator is replaced by the
orbital angular momentum operator.
Furthermore, substituting the nonequilibrium distri(1)
bution function fn = τ Ea ∂a fn into Eq. (1) yields the
(1)
(1,od)
(1,ic)
extrinsic NOME contribution, χc;ab = χc;ab + χc;ab +
(1,d)

χc;ab , with its components deﬁned as
X
(1,od)
χc;ab = −τ
fn ∂ a Ω̄cb
nm ,

(7)

nm

(1,ic)

χc;ab

= −τ εcαβ

X

fn ∂ a

n

(1,d)

χc;ab

=




αb β
Gnm
vn
,
ǫnm

(8)


 β αb
X
v̄ G
τ
βαb
.
εcαβ
fn ∂ a nm nm + Cnm
2
ǫnm
nm

(9)

Similarly, "ic", "d", and "od" represent the itinerant circulation, dipole-type local circulation, and conventional
local circulation terms, respectively.
Equations (3)-(4) and (7)-(9) constitute the central results of this Letter. Several important remarks are in
order. First, the distinct scaling behaviors provide a direct experimental discriminator: the intrinsic response
(0)
χc;ab includes both Fermi-sea and Fermi-surface contri(1)

butions, whereas χc;ab is a purely Fermi-surface term that
scales linearly with τ . This dependence allows one to separate the contributions via disorder engineering or mo(j,ic)
bility control. Second, the geometric contributions χc;ab
(j,d)

and χc;ab for j = 0, 1 are unique to orbital magnetization,
having no counterparts in the nonlinear spin magnetiza(j,od)
tion. Finally, by replacing Lcnm in χc;ab with the velocc
c
ity vnm , spin σnm or spin-current (Jcλ )mn = 21 {ŝλ , v̂ c }mn
matrices, one reproduces the established formulas for
nonlinear Hall eﬀect [29, 47], nonlinear spin magnetization [28, 48], and nonlinear spin Hall eﬀect [32, 49] for
order τ j , respectively.
(0/1)

Symmetry property— As a rank-3 pseudo-tensor, χc;ab
(0)

(1)

is P-even. Furthermore, χc;ab is T -odd, while χc;ab is T even. Unlike spin magnetization or the spin Hall eﬀect,
which rely directly on spin-orbit coupling (SOC), the intrinsic NOME involves only orbital operators and might
initially appear independent of SOC. However, in the absence of SOC, the system usually possesses an additional

3
(0)

(1)

TABLE I. Constraints on the intrinsic NOME (χz;ab ) and extrinsic NOME (χz;ab ) imposed by various magnetic point group
symmetries in 2D systems. The symbols ✓(✗) indicate whether the corresponding NOME component is symmetry-allowed
(forbidden), respectively. Here, the system is assumed to lie in the xy plane, and the ﬁrst four columns corresponds to
symmetries that forbid the linear OME.
P, C2z , Mz

z
z
z
z
C3,4,6
, S3,4,6
C3,6
T , S3,6
T

C4z T , S4z T

C2x,y , Mx,y

T , PT , C2z T , Mz T

C2x,y T , Mx,y T

χz;xx

(0)

✓

χz;yy

(0)

✗

−χz;yy

(0)

✗

✗

✓

(0)
χz;xy

✓

✗

✗

✓

✓

✗

✗

(0)
χz;yy

✓

✓

✗

✓

✗

✗

✓

(1)
χz;xx

✓

(1)
χz;yy

(1)
χz;yy

(1)
χz;yy

✗

✓

✗

(1)
χz;xy

✓

✗

✗

✗

✓

✓

✓

(1)
χz;yy

✓

✓

✓

✓

✗

✓

✗

spin group symmetry [C̄2 ||T ] [50] that constrains the intrinsic NOME to zero [51]. By contrast, the extrinsic
NOME persists even without SOC [52–54] due to its T even nature. This analysis reveals that the intrinsic and
extrinsic NOME obey the same symmetry constraints as
the intrinsic anomalous Hall eﬀect and intrinsic orbital
Hall eﬀect. More generally, constraints imposed by arbitrary magnetic point group (MPG) symmetries are dictated by the transformation rule [55]

as [56–59]

(0/1)

(0/1)

χc;ab = (ηT )1/0 det(R)Raa′ Rbb′ Rcc′ χc′ ;a′ b′ ,

(10)

where Raa′ denotes the matrix representation of the
MPG symmetry, and ηT = −1 (1) for MPG operations
that include (do not include) time-reversal. Here, we
focus on 2D systems, where the magnetization arising
from the angular Hall current vanishes. Table I summarizes the constraints imposed by various MPG symmetries on the intrinsic and extrinsic NOME components;
notably, the ﬁrst four columns correspond to symmetries
that forbid the linear OME. As a result, we identify 41
and 55 MPGs that support the intrinsic and extrinsic
NOME in 2D systems, respectively [34]. In stark contrast, the intrinsic and extrinsic OMEs are allowed only
in 10 and 8 MPGs, respectively [34]. Thus, NOME provides a promising route to generating orbital magnetization in a signiﬁcantly broader range of materials than the
linear OME.
In the following, we investigate two systems: one exhibiting only intrinsic NOME and the other allowing
solely extrinsic NOME. We show that in both cases, the
geometric contribution dominates the conventional contribution.

Honeycomb lattice model— We illustrate the intrinsic
NOME using the modiﬁed Kane-Mele model, deﬁned

H =−t

X †
X †
ciα (σαβ × dij )z cjβ
ciα cjα + iλR
hiji

hiji

+ iλso

X

hhijii

z
vij c†iα σαβ
cjβ + λ

X †
ciα szαβ ciβ .

(11)

i

Here, t denotes the nearest-neighbor hopping, the second
term describes the inversion-breaking Rashba-type SOC,
the third term corresponds to the mirror SOC, and the
last term represents the T -breaking exchange coupling.
The system possesses 6m′ m′ MPG symmetry (containing
C6z and T Mx ). Consequently, Table I indicates that only
(0)
(0)
the intrinsic NOME component χz;xx = χz;yy is ﬁnite,
while both the extrinsic NOME and linear OME vanish.
Fig. 1(a) displays the band dispersion of Eq. (11) using the parameters given in the caption. In Fig. 1(b),
(0,od)
we plot the intrinsic NOME component χz;xx and to(0)
tal χz;xx as a function of chemical potential µ, alongside the nonlinear spin magnetization for comparison.
We observe that the geometric "d" and "ic" contributions dominate the intrinsic NOME when µ lies near
conduction band edge. Notably, the Hermitian connection contribution further dominates over these geometric contributions. When all orbital components are included, the generated orbital magnetization is approximately three times larger than the spin magnetization
and carries the opposite sign. Fig. 1(d) illustrates the
(0,d)
(0,ic)
k-resolved integrand of χz;xx + χz;xx for the third band;
this map reveals that the peak response originates primarily from the region around the band edges at K and
K ′ points. Finally, Fig. 1(c) presents dependence of in(0)
trinsic NOME χz;xx on the Rashba SOC strength at ﬁxed
µ = 50meV. At λR = 0, where the inversion symmetry is restored, the intrinsic NOME retains a non-zero
(0)
minimum of ∼ 10µB /V 2 and χz;xx behaves as an even
function of λR , consistent with its P-even symmetry.
Antiferromagnets— To illustrate the extrinsic NOME,
we consider the minimal PT -symmetric model of the

4
  D 

  E 

   

 R U E L W D O
 R G
 V S L Q
 + &

 í   

 í   

K

kx

  F 

 í   

   

 í   

 

   
 í   
 í   

 í   

 

2
χz(0)
; xx   µB /V  

+
   

K

K

′

 í   
 í  

 

λR   meV 

  

  

  
 
 í  

 R U E L W D O
 + &
 V S L Q

 í  

X

M

  F 

 í   

  

kx

 

FIG. 1.
(a) Band dispersion for Eq. (11). (b) The in(0)
trinsic NOME component χz;xx , its three contributions as a
function of chemical potential µ. For comparison, we also
s(0)
plot the nonlinear spin magnetization component χz;xx , and
(0)
the Hermitian connection of χz;xx termed as HC. (c) The
(0)
Rashba SOC λR dependence of intrinsic NOME χz;xx at ﬁxed
µ = 50meV. (d) The k-resolved distribution of the integrand
(0,ic)
(0,d)
of χz;xx + χz;xx for the third band. Parameters: t = 0.85eV,
λR = 20meV, λ = 10meV, λso = 10meV, and T = 20K.

antiferromagnet CuMnAs, which features two magnetic
sublattices related by PT symmetry. Its tight-binding
Hamiltonian reads [60]
ky
kx
cos
− t′ (cos kx + cos ky )
2
2
+ λτ̂z (σ̂y sin kx − σ̂x sin ky ) + Jn τ̂z σ̂x ,
(12)

H = − 2tτ̂x cos

where τ̂ and σ̂ are Pauli matrices for the sublattice and
spin sectors, respectively. t (t′ ) is the nearest (nextnearest) neighbor hopping, λ is the Rashba-type SOC
strength, and Jn is the exchange coupling. This system
preserves PT , C2z T and C2y symmetries, with both PT
and C2y interchanging the magnetic sublattices. Consequently, while PT symmetry forbids the intrinsic NOME,
the C2y symmetry allows a single non-zero extrinsic
(1)
NOME component, χz;xy , consistent with Table I.
Figure 2(a) illustrates the band dispersion, highlighting two Dirac points along the high-symmetry path X-M.
In Fig. 2(b), we plot the extrinsic nonlinear magnetization versus µ; notably, the orbital component dominates
over the spin component. We further ﬁnd that the Hermitian connection contribution, remains the dominant
term in the extrinsic NOME throughout the entire range
(1,d)
of µ.The k-resolved map of the χz;xy integrand for the

   

µ/t

   

   

+

Y

M

Γ

X
kx

 í  

 í   
−

   

  G 

od
 L F
 G

 í   

 í  

  E 

  

 í  

  G 

 R U E L W D O
 R G
 V S L Q
 + &

ky

2
χz(0)
; xx   µB /V  

K

′

2
χz(1)
; xy   µB /V  

µ/t

 

    

  

   

2
χz(1)
; xy   µB /V  

µ(meV)

   

  D 

ky

   

   

   

µ/t

   

   

−

FIG. 2. (a) Band dispersion for Eq. (12). (b) The extrinsic nonlinear magnetization including orbital and spin components as a function of chemical potential µ. (c) The three
(1)
components of extrinsic nonlinear orbital magnetization χz;xy
as a function of chemical potential µ. (d) The k-resolved dis(1,d)
tribution of the integrand of χz;xy for ﬁrst two bands. Here,
′
we use t = 0.08t, Jn = 0.6t, λ = 0.8t, T = 100K and τ = 10fs.

ﬁrst two bands [Fig. 2(d)], conﬁrms that the main contribution comes from the Dirac points, reﬂecting the interband nature of the NOME. In addition, we plot the three
contributions of extrinsic nonlinear orbital magnetization
(1)
χz;xy versus µ in Fig. 2(c).
Discussion and conclusion— We assess feasibility by estimating the NOME magnitude in our models. Under a
moderate electric ﬁeld E = 105 V/m along the x-axis, the
honeycomb lattice yields an induced orbital magnetization of ∼ 10−5 µB /nm2 [Fig. 1(c)], while CuMnAs yields
∼ 10−6 µB /nm2 [Fig. 2(b)]. Both values are suﬃciently
large to be detected via polar magnetooptical Kerr eﬀect
experiments [11, 12, 54].
(0)
Although the net χc;ab vanishes in PT -symmetric materials, a staggered orbital magnetization can still emerge
on diﬀerent sublattices, analogous to the extrinsic OME
in antiferromagnets [61]. Notably, this staggered intrinsic NOME generally requires lower symmetry than the
extrinsic OME. For instance, in a system with T τ1/2
symmetry, where τ1/2 represents the half-lattice translation, the staggered NOME is allowed, while the linear
counterpart is forbidden. It should be emphasized that
the NOME does not directly generate spin-orbit torque.
Instead, the SOC is required to convert the orbital magnetization into a spin accumulation, thereby exerting a
torque on the magnetic order parameter, similar to the
orbital torque mechanism [3]. While we focus on the τ 0

5
and τ 1 contributions within the relaxation time approximation, an additional extrinsic contribution, referred to
as the Drude NOME, arises at order τ 2
X

(2)
(13)
Ωcn ∂kab gn + Lcn ∂kab fn .
χc;ab =τ 2
n

Since both τ and ∂ka are time-reversal odd, the Drude
NOME shares the same symmetry constraints as the intrinsic NOME. Nevertheless, this contribution becomes
signiﬁcant only in ultra-clean samples where τ is very
large. Finally, by combining Eq. (1) with AC wavepacket
formalism [33], one can also derive a high-frequency
NOME. Remarkably, its intrinsic contribution can be
both T -even and P-even contribution, and may therefore remain ﬁnite even in systems without SOC.
To conclude, we have developed a microscopic theory
of NOME, identifying the Hermitian-connection contribution as the primary source of the eﬀect. This gaugeinvariant formulation is suitable for ﬁrst-principles implementation and quantitative comparison with experiments. Crucially, NOME obeys far fewer symmetry constraints than the linear OME, signiﬁcantly expanding the
candidate materials for orbital control. Owing to their
distinct scaling with the relaxation time τ , we predict
that the intrinsic NOME dominates in moderately disordered samples, whereas the extrinsic NOME dominates
in clean samples.
Acknowledgments — J.J. and Z.Q. are supported by National Natural Science Foundation of
China (12488101, 12474158, and 12234017), Innovation Program for Quantum Science and Technology
(2021ZD0302800), Anhui Initiative in Quantum Information Technologies (AHY170000). J.W. is supported
by the National Natural Science Foundation of China
(12034014). We also thank the Supercomputing Center of University of Science and Technology of China for
providing the high-performance computing resources.

qiao@ustc.edu.cn
jianwang@hku.hk
[1] B. A. Bernevig, T. L. Hughes, and S. C. Zhang, Orbitronics: The Intrinsic Orbital Current in p-Doped Silicon, Phys. Rev. Lett. 95, 066601 (2005).
[2] D. Go, D. Jo, C. Kim and H. W. Lee, Intrinsic
Spin and Orbital Hall Eﬀects from Orbital Texture,
Phys. Rev. Lett. 121, 086602 (2018).
[3] D. Go,
and H. W. Lee,
Orbital torque:
Torque generation by orbital current injection,
Phys. Rev. Res. 2, 013177 (2020).
[4] R. B. Atencia, A. Agarwal, and D. Culcer, Orbital angular momentum of Bloch electrons: equilibrium formulation, magnetoelectric phenomena, and the orbital Hall
eﬀect, Advances in Physics: X 9, 1 (2024).
[5] A. Johansson, Theory of spin and orbital Edelstein effects, J. Phys.: Condens. Matter 36, 423002 (2024).
∗

†

[6] P. Wang, F. Chen, Y. Yang, S. Hu, Y. Li, W. Wang, D.
Zhang, and Y. Jiang, Orbitronics: Mechanisms, Materials, and Devices, Adv. Electron. Mater. 11, 5 (2025).
[7] S. Fukami, K. J. Lee, and M. Kläui, Challenges and opportunities for orbitronics, arXiv:2509.23954.
[8] V. Baltz, A. Manchon, M. Tsoi, T. Moriyama, T.
Ono, and Y. Tserkovnyak, Antiferromagnetic spintronics, Rev. Mod. Phys. 90, 015005 (2018).
[9] A. Manchon, J. Železný, I. M. Miron, T. Jungwirth, J. Sinova, A. Thiaville, K. Garello, and P.
Gambardella,
Current-induced spin-orbit torques
in ferromagnetic and antiferromagnetic systems,
Rev. Mod. Phys. 91, 035004 (2019).
[10] T. P. Cysne, L. M. Canonico, M. Costa, R. B. Muniz, and
T. G. Rappoport, Orbitronics in two-dimensional materials, npj Spintronics 3, 39 (2025).
[11] I. Lyalin, S. Alikhah, M. Berritta, P. M. Oppeneer, and R. K. Kawakami, Magneto-Optical Detection of the Orbital Hall Eﬀect in Chromium,
Phys. Rev. Lett. 131, 156702 (2023).
[12] G. Sala, H. Wang, W. Legrand, and P. Gambardella, Orbital Hanel Magnetoresistance in a 3d Transition Metal,
Phys. Rev. Lett. 131, 156703 (2023).
[13] Y. G. Choi, D. Jo, K. H. Ko, D. Go, K. H. Kim, H.
G. Park, C. Kim, B. C. Min, G. M. Choi, and H. W.
Lee, Observation of orbital Hall eﬀect in a light metal
Ti, Nature, 619, 52 (2023).
[14] H. Liu, and D. Culcer, Dominance of Extrinsic Scattering Mechanisms in the Orbital Hall Eﬀect: Graphene,
Transition Metal Dichalcogenides, and Topological Antiferromagnets, Phys. Rev. Lett. 132, 186302 (2024).
[15] P. Tang, and G. E. W. Bauer, Role of Disorder in the Intrinsic Orbital Hall Eﬀect,
Phys. Rev. Lett. 133, 186302 (2024).
[16] A. Veneri, T. G. Rappoport, and A. Ferreira, Extrinsic Orbital Hall Eﬀect: Orbital Skew Scattering and
Crossover between Diﬀusive and Intrinsic Orbital Transport, Phys. Rev. Lett. 134, 136201 (2025).
[17] H. Liu, J. H. Cullen, D. P. Arovas, and D. Culcer, Quantum Correction to the Orbital Hall Eﬀect,
Phys. Rev. Lett. 134, 036304 (2025).
[18] A. L. Sharpe, E. J. Fox, A. W. Barnard, J.
Finney, K. Watanabe, T. Taniguchi, M. A. Kastner,
and D. Goldhaber-Gordon, Emergent ferromagnetism
near three-quarters ﬁlling in twisted bilayer graphene,
Science 365, 605 (2019).
[19] M. Serlin, C. L. Tschirhart, H. Polshyn, Y. Zhang, J. Zhu,
K. Watanabe, T. Taniguchi, L. Balents, and A. F. Young,
Intrinsic quantized anomalous Hall eﬀect in a moiré heterostructure, Science 367, 900 (2020).
[20] W. Y. He, D. Goldhaber-Gordon, and K. T. Law, Giant orbital magnetoelectric eﬀect and current-induced
magnetization switching in twisted bilayer graphene,
Nat. Commun. 11, 1650 (2020).
[21] C. Huang, N. Li, and A. H. MacDonald, CurrentDriven Magnetization Reversal in Orbital Chern Insulators, Phys. Rev. Lett. 126, 056801 (2021).
[22] C. Xiao, H. Liu, J. Zhao, S. A. Yang, and Q. Niu, Thermoelectric generation of orbital magnetization in metals,
Phys. Rev. B 103, 045401 (2021).
[23] J. Cullen, D. Arovas, R. Raimondi, and D. Culcer,
Quantum geometry and dipolar dynamics in the orbital
magneto-electric eﬀect, arXiv:2505.02911.
[24] X. B. Qiang, T. Liu, H. Z. Lu, and X. C. Xie,

6
Quantum geometric origin of orbital magnetization,
Appl. Phys. Lett. 128, 010501 (2026).
[25] The response tensor of OME is deﬁned as Ma = χa;b Eb ,
which is a rank-2 pseudo-tensor. In the 2D materials in
xy plane, only the orbital magnetization Mz induced
by in-plane electric ﬁeld is relevant, thus the response
tensor reduces to two independent components χz;x and
χz;y . These two components are forbidden by symmetries
z
z
z
z
P, C2z , Mz , C3,4,6
, S3,4,6
, C3,4,6
T and S3,4,6
T.
[26] J. E. Sipe and A. I. Shkrebtii, Second-order optical response in semiconductors, Phys. Rev. B 61, 5337 (2000).
[27] A. Pezo, D. G. Ovalle, and A. Manchon, Orbital Hall
eﬀect in crystals: Interatomic versus intra-atomic contributions, Phys. Rev. B 106, 104414 (2022).
[28] C. Xiao, H. Liu, W. Wu, H. Wang, Q. Niu,
and S. Y. A. Yang, Intrinsic Nonlinear Electric Spin Generation in Centrosymmetric Magnets,
Phys. Rev. Lett. 129, 086602 (2022).
[29] Y. Gao, S. Y. A. Yang, and Q. Niu, Field Induced Positional Shift of Bloch Electrons and Its Dynamical Implications, Phys. Rev. Lett. 112, 166601 (2014).
[30] L. Xiang, C. Zhang, L. Wang, and J. Wang, Third-order
intrinsic anomalous Hall eﬀect with generalized semiclassical theory, Phys. Rev. B 107, 075411 (2023).
[31] J. Jia, L. Xiang, Z. Qiao, and J. Wang, Nonlinear Magnetoelectric Edelstein Eﬀect arXiv:2507.23415.
[32] H. Wang, H. Liu, X. Feng, J. Cao, W. Wu, S. Lai, W.
Gao, C. Xiao, and S. A. Yang, Intrinsic Nonlinear Spin
Hall Eﬀect and Manipulation of Perpendicular Magnetization, Phys. Rev. Lett. 134, 056301 (2025).
[33] J. Jia, L. Xiang, Z. Qiao, and J. Wang, Equivalence of
semiclassical and response theories for second-order nonlinear ac Hall eﬀects, Phys. Rev. B 110, 245406 (2024).
[34] See Supplemental Material for derivation details based on
extended wavepacket theory and the symmetry analysis
of the MPGs in 2D systems.
[35] D. Xiao, M. C. Chang, and Q. Niu, Berry
Phase
Eﬀects
on
Electronic
Properties,
Rev. Mod. Phys. 82, 1959 (2010).
[36] C. Xiao, J. Cao, Q. Niu, and S. A. Yang,
Proper Deﬁnition of Intrinsic Nonlinear Current,
Phys. Rev. Lett. 135, 256306 (2025).
[37] H. Liu, J. Zhao, Y. X. Huang, X. Feng, C. Xiao, W.
Wu, S. Lai, W. Gao, and S. A. Yang, Berry connection polarizability tensor and third-order Hall eﬀect,
Phys. Rev. B 105, 045118 (2022).
[38] D. Xiao, J. Shi, and Q. Niu, Berry Phase Correction to Electron Density of States in Solids,
Phys. Rev. Lett. 95, 137204 (2005).
[39] T. Thonhauser, D. Ceresoli, D. Vanderbilt, and R.
Resta, Orbital Magnetization in Periodic Insulators,
Phys. Rev. Lett. 95, 137205 (2005).
[40] J. Shi, G. Vignale, D. Xiao, and Q. Niu, Quantum Theory
of Orbital Magnetization and Its Generalization to Interacting Systems, Phys. Rev. Lett. 99, 197202 (2007).
[41] C. Xiao, and Q. Niu, Uniﬁed bulk semiclassical theory for intrinsic thermal and magnetization currents,
Phys. Rev. B 101, 235430 (2020).
[42] T. Yoda, T. Yokayama, and S. Murakami, Currentinduced Orbital and Spin Magnetizations in Crystals

with Helical Structure, Sci. Rep. 5, 12024 (2015).
[43] S. Zhong, J. E. Moore, and I. Souza, Gyrotropic Magnetic
Eﬀect and the Magnetic Moment on the Fermi Surface,
Phys. Rev. Lett. 116, 077201 (2016).
[44] J. Ahn, G. Y. Guo, N. Nagaosa, and A. Vishwanath
Riemannian geometry of resonant optical responses,
Nat. Phys. 18, 290 (2022).
[45] L. Xiang, J. Jia F. Xu, Z. Qiao, and J. Wang, Intrinsic Gytropic Magnetic Current from Zeeman Quantum
Geometry, Phys. Rev. Lett. 134, 116301 (2025).
[46] A. Gao, N. Nagaosa, N. Ni, and S. Y. Xu, Quantum
Geometry Phenomena in Condensed Matter Physics,
arXiv:2508 (2025).
[47] I. Sodemann, and L. Fu, Quantum Nonlinear Hall Eﬀect
Induced by Berry Curvature Dipole in Time-Reversal Invariant Materials, Phys. Rev. Lett. 115, 216806 (2015).
[48] C. Xiao, W. Wu, H. Wang, Y. X. Huang, X. Feng,
H. Liu, G. Y. Guo, Q. Niu, and S. A. Yang, TimeReversal-Even Nonlinear Current Induced Spin Polarization, Phys. Rev. Lett. 130, 166302 (2023).
[49] L. Xiang, H. Jin, and J. Wang, Spin Transport Revealed by Spin Quantum Geometry,
Phys. Rev. Lett. 135, 146303 (2025).
[50] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond Conventional Ferromagnetism and Antiferromagnetism: A
Phase with Nonrelativistic Spin and Crystal Rotation
Symmetries, Phys. Rev. X 12, 031042 (2022).
[51] This constraint does not apply to orbital Chern insulators, i.e. Haldane model, where broken time-reversal (T )
symmetry allows a ﬁnite intrinsic NOME.
[52] I. Baek, S. Han, S. Cheon, and H. W. Lee, Nonlinear orbital and spin Edelstein eﬀect in centrosymmetric metals,
npj Spintronics 2, 33 (2024).
[53] X. B. Qiang, X. Liu, H. Z. Lu, and X. C.
Xie, Quantum Christoﬀel Nonlinear Magnetization,
Phys. Rev. Lett. 136, 056301 (2026).
[54] X. Qian, X. B. Qiang, W. Zhu, Y. Huang, Y. Chen, H.
Z. Lu, Y. Ji, and K. Wang, Probing quantum geometric
nonlinear magnetization via second-harmonic magnetooptical Kerr eﬀect, Phys. Rev. B 113, L041407 (2026).
[55] R. E. Newnham, Properties of materials: anisotropy,
symmetry, structure (Oxford university press, 2005).
[56] C. L. Kane and E. J. Mele, Z2 Topological Order and the Quantum Spin Hall Eﬀect,
Phys. Rev. Lett. 95, 146802 (2005).
[57] H. Pan, Z. Li, C. C. Liu, G. Zhu, Z. Qiao, and Y. Yao,
Valley-Polarized Quantum Anomalous Hall Eﬀect in Silicene, Phys. Rev. Lett. 112, 106802 (2014).
[58] F. Liu, Two-dimensional topological insulators: Past,
present and future, Coshare Sci. 02, 01 (2024).
[59] S. Hasegawa, Surface and edge states of quantum materials, Coshare Science 03, 01 (2025).
[60] L. Šmejkal, J. Železný, J. Sinova, and T. Jungwirth,
Electric Control of Dirac Quasiparticles by Spin-Orbit Torque in a Antiferromagnet,
Phys. Rev. Lett. 118, 106402 (2017).
[61] L. Salemi, M. Berritta, A. K. Nandy, and P. M.
Oppeneer,
Orbitally dominated Rashba-Edelstein
eﬀect
in
noncentrosymmetric
antiferromagnets,
Nat. Commun. 10, 5381 (2019).

