<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2602.19076 -->

Nonperturbative Magnetic Orbital Hall Effect in Altermagnets
Xukun Feng,1 Jin Cao,2 Lay Kee Ang,3 Shengyuan A. Yang,2, ∗ Cong Xiao,1, † and X. C. Xie1, 4
1

arXiv:2602.19076v2 [cond-mat.mtrl-sci] 21 May 2026

Interdisciplinary Center for Theoretical Physics and Information
Sciences (ICTPIS), Fudan University, Shanghai 200433, China
2
Research Laboratory for Quantum Materials, Department of Applied Physics,
The Hong Kong Polytechnic University, Kowloon, Hong Kong, China
3
Science, Mathematics and Technology, Singapore University of Technology and Design, Singapore 487372, Singapore
4
International Center for Quantum Materials, School of Physics, Peking University, Beijing 100871, China
Recent studies on altermagnets have focused considerable attention on nonrelativistic effects that
persist in the absence of spin-orbit coupling (SOC). As a result, the relative importance of various
phenomena in altermagnets has commonly been judged by their dependence on SOC. Here, we challenge this common wisdom by uncovering the magnetic orbital Hall effect, which is nonperturbative
in SOC strength. We establish the symmetry properties of this effect, demonstrating that it is
strictly forbidden in conventional collinear antiferromagnets yet universally allowed in all ten spinLaue classes of collinear altermagnets. Counterintuitively, although SOC-induced, it reaches giant
magnitudes in altermagnets — comparable to or even exceeding the nonrelativistic spin Hall effect.
Moreover, altermagnetic symmetry enables unconventional collinear-polarized orbital currents, allowing field-free manipulation of perpendicular magnetization. Our first-principles calculations predict strong room-temperature responses in the experimentally established altermagnets CrSb and
FeSb2 . These findings reveal the previously overlooked potential of altermagnetic orbitronics and
broaden the horizons for altermagnets in high-performance magnetic memory applications.

Orbital Hall effect — the generation of a transverse
orbital angular momentum current in response to an applied electric field — has emerged as a vibrant area of
research [1–10]. It has been intensively studied in nonmagnetic systems with weak spin-orbit coupling (SOC),
such as Ti and Cr [11, 12]. In these systems, unlike its
spin counterpart (i.e., the spin Hall effect), the orbital
response does not require SOC, enabling orbital currents
that can be orders of magnitude stronger than spin Hall
effect [11–13]. When injected into an adjacent magnetic
layer, such currents can efficiently drive magnetic switching, offering significant potential for magnetic memory
applications [11, 14–25].
In magnetic systems, a distinct variant known as the
magnetic orbital Hall effect (MOHE) arises [26]. While
the conventional orbital Hall effect in nonmagnetic materials is even under time-reversal (T ) operation, MOHE is
odd under T , meaning that its sign reverses upon flipping
the magnetic order. This property provides an additional
handle for controlling orbital currents, making MOHE
particularly attractive for spintronic and orbitronic devices.
To date, the study on MOHE is rare [26], and has focused on ferromagnetic materials. For practical applications, however, antiferromagnets are preferable as orbital
current sources, because they produce minimal stray
fields and reduced interference with neighboring magnetic layers. Nevertheless, MOHE in antiferromagnets
remains unexplored. This absence stems from two main
challenges. (i) One can show that MOHE is forbidden
in conventional antiferromagnets with PT or t1/2 T symmetry (P denotes inversion and t1/2 a fractional translation). It is not yet clear what kind of antiferromagnets
can support MOHE. (ii) In collinear antiferromagnets,

MOHE must require SOC, leading to the widespread expectation of only weak responses. However, is this expectation really the case? Is it possible to realize strong
MOHE in antiferromagnets? And furthermore, what is
the guideline for finding such materials? These key questions remain to be answered.
In this work, we address these outstanding questions.
We show that although MOHE is forbidden in conventional antiferromagnets, it is universally allowed in altermagnets — a newly recognized class of collinear antiferromagnets that has become a focus of current research [27–41]. From symmetry analysis, we demonstrate
that MOHE exists in all ten spin-group classes that encompass known altermagnets, establishing it as a transport signature that distinguishes altermagnets from conventional antiferromagnets. Our analysis also gives explicit results of how MOHE conductivity scales with spinconserve SOC and spin-flip SOC [42–45] in the perturbative regime. Importantly, we show that although MOHE
here must require SOC, its dependence on SOC can be
nonperturbative, meaning that the MOHE magnitude is
not necessarily small; instead, can be remarkably large
even under weak SOC. This happens when the Fermi
level lies near a small SOC-induced gap. These predictions are confirmed through an effective lattice model
and first-principles calculations on realistic altermagnetic
materials CrSb and FeSb2 . Particularly, in these materials, MOHE can dominate over the spin Hall effect
(even for spin Hall response with nonrelativistic origin),
reaching significant values comparable to or exceeding
the previously reported orbital Hall responses. Moreover, MOHE in altermagnets enables the generation of
collinearly-polarized orbital current (CPOC), a highly
desirable feature for information devices with improved

2

(a)

E

jL

(b)

ers of SOC and constraining the expansion with spin
point group. This approach allows us to find how MOHE
scales with different kinds of SOCs in the perturbative
regime, i.e., when SOC is weak compared to other energy scales in the system. Following Ref. [44], we introduce spin-orbit vectors ζ α , which characterizes the form
of SOC via

jL

E

FIG. 1. Illustration of MOHE in antiferromagnets. (a) The
effect is forbidden in conventional antiferromagnets, where
the magnetic sublattices (denoted by red and blue arrows)
are connected by PT or t1/2 T symmetry. (b) It is generally
permitted in altermagnets with the magnetic sublattices connected by Cn T or Mi T symmetries (C and M are rotation
and mirror operations, respectively).

storage density and endurance [46–48]. Our findings position altermagnets as promising orbital current sources
and establish MOHE as a new hallmark of this emerging class of materials, opening a promising route toward
next-generation information technologies.
Symmetry analysis. The orbital current response is
La
characterized by a rank-3 pseudotensor σbc
defined by
La
jbLa = σbc
Ec ,

(1)

where jbLa is the orbital angular momentum current density flowing in direction b and polarized in direction a, E
is the applied electric field, roman indices denote Cartesian components in real space, roman indices (= x, y, z)
denote the Cartesian components, and repeated indices
are summed over.
First of all, let us see why the MOHE is forbidden in
conventional antiferromagnets. By definition, MOHE is
odd under T . For antiferromagnets with t1/2 T symmetry, its magnetic point group contains T , allowing only
T -even responses, so MOHE is forbidden. As for systems with P T symmetry, one notes that both j L and E
are odd under P T , which also forbids a T -odd response
[see Fig. 1(a)]. In comparison, t1/2 T and P T are broken
in altermagnets, where the two magnetic sublattices are
connected by certain mirror or rotational symmetry. We
shall see altermagnets generally permit a nonzero MOHE
[see Fig. 1(b)].
It was found that altermagnets can host spin Hall effect in the absence of SOC [36]. However, this is not the
case for MOHE. To see this, we note that without SOC,
an altermagnet is described by spin groups [27, 28, 49].
The spin-only group always contains a C2′ = C2 T symmetry, where C2 is a reversal of spin, having no action
on orbitals. It follows that C2′ just acts like an effective
time-reversal symmetry for orbital transport, thus forbidding MOHE. This demonstrates that nonzero MOHE
in altermagnets must require SOC.
Next, we analyze the symmetry-allowed structure of
La
the MOHE conductivity tensor by expanding σbc
in pow-

HSOC = λŝα (ζ α · Ô),

(2)

where ŝα (α = 1, 2, 3 labels spin space directions) are
the three spin operators, Ô is the orbital operator acting
on real space, and λ is the SOC strength. The ζ α vectors help to distinguish spin-conserve and spin-flip SOC
terms (SOC terms with ζ 3 are spin-conserve, whereas
those with ζ 1 and ζ 2 are spin-flip, as detailed in Supplemental Material [50]).
La
The perturbative expansion of σbc
takes the form of
La ,α α
La ,αβ α β
La
σbc
= ℓbc,d
ζd + qbc,de
ζd ζe + · · · .

(3)

Here, ℓ’s and q’s are expansion coefficients for linear and
quadratic terms, respectively. In collinear altermagnets,
as discussed, there is no zeroth order term for MOHE.
And another important common feature imposed by the
spin-only group of collinear magnets is: the linear terms
contain only spin-conserve SOC, while quadratic terms
contain only spin-flip SOC [50]. Therefore, up to second
order of SOC, the spin-only group enforces
La ,12 1 2
La
2 1
a ,3 3
σbc
= ℓL
bc,d ζd + qbc,de (ζd ζe − ζd ζe ).

(4)

Consider the ten spin Laue groups that cover the existing altermagnetic materials. Their allowed coefficients
in (4) can be screened out. Here, we focus on the components that produce CPOC, i.e., with a = b. Table I
shows the results for the case N ∥ẑ (results for N along
x and y directions are presented in Supplemental Material [50]). For comparison, we also list the allowed
coefficients for magnetic spin Hall effect in the table.
One has the following observations. First, one sees that
CPOC from MOHE can be generated in most (7 out of
10) classes. For the remaining three classes, although
they do not support CPOC (for N ∥ẑ), other non-CPOC
La
components of σbc
are still allowed, demonstrating that
MOHE is universally present in altermagnets. Second,
regarding the previously studied spin Hall effect without SOC, its presence is actually quite restricted, only
in the 2 2/2 m class here. This indicates that in most altermagnets, actually both magnetic spin Hall effect and
MOHE are induced by SOC, suggesting that MOHE is
not necessarily weaker than spin response even in the perturbative regime. Third, for the three classes 2 m2 m1 m,
1 1 2 2
4/ m m m and 1 6/1 m2 m2 m, as shown in Supplemental Material [50], CPOC can still be generated when the
Néel vector is along the x or y direction. Finally, we

3
TABLE I. Symmetry-allowed collinearly-polarized components of MOHE and spin Hall conductivities for the 10 spin Laue
groups relevant to collinear altermagnets. ‘×’ represents the component is forbidden. Here, we take N ∥ẑ. The symbols with
blue (red) color correspond to the responses with polarization parallel (perpendicular) to the Néel vector.
Spin Laue Group
2

m2 m1 m
2

Anisotropy

Nonrelativistic limit

Spin-conserve SOC

d-wave

×

×

Spin-flip SOC
×

Ly ,3
x ,3
ℓL
xz,z , ℓyz,z
Ly ,3
Lx ,3
ℓxz,z , ℓyz,z

Ly ,12
Sy ,1
Lx ,12
x ,2
qxz,xy
, qyz,xy
, ℓS
xz,y , ℓyz,x
Sy ,1
Ly ,12
Sx ,2
Lx ,12
ℓxz,y , ℓyz,x , qxz,xy , qyz,xy

×

1

4/ m

d-wave

×

2

4/1 m2 m1 m

d-wave

×

1

4/1 m2 m2 m

g-wave

×

×

1

6/1 m2 m2 m

i-wave

×

×

×

d-wave

S ,(0)
σzyz

Sz ,33
Lx ,3
z ,3
ℓL
zy,z , qzy,zz ; ℓxy,z
Ly ,3
ℓyx,z
Ly ,3
x ,3
ℓL
xy,z , ℓyx,z
x ,3
ℓL
xy,z
Ly ,3
Lx ,3
ℓxz,z , ℓyz,z

Lz ,12
Sz ,11
Sz ,22
Lx ,12
x ,2
qzy,xy
, qzy,xx
, qzy,yy
; qxy,xy
, ℓS
xy,y
Ly ,12
Sy ,1
qyx,xy , ℓyx,x
Ly ,12
Sy ,1
Lx ,12
x ,2
qxy,xy
, qyx,xy
, ℓS
xy,y , ℓyx,x
Lx ,12
x ,2
qxy,xy
, ℓS
xy,y
Ly ,12
Sy ,1
Lx ,12
Sx ,2
qxz,xy , qyz,xy , ℓxz,y , ℓyz,x

2

2

2

2/ m

1 2

3 m

g-wave

×

2

6/2 m

g-wave

×

6/2 m2 m1 m

g-wave

×

i-wave

×

1

m1 32 m

mention that since MOHE requires SOC, its symmetryallowed components may also be analyzed by using magnetic groups. This has also been done [50], and the results
are consistent with those in Table I.
Nonperturbative enhancement of MOHE. To illustrate
the features discussed above, we study a minimal model
for a two-dimensional (2D) d-wave altermagnet on a
square lattice [see Fig. 2(a)], which belongs to the spin
Laue group 2 4/1 m2 m1 m [51, 52]:

states with the same spins. Meanwhile, the degeneracies
at µ ∼ 0.09 eV are of opposite spins, so they are gapped
by spin-flip SOC.
The MOHE conductivity is evaluated from
Z
dk ′ La
e2 X
La
σbc
=− τ
f ⟨j ⟩nk ⟨vc ⟩nk ,
(9)
ℏ n
(2π)d 0 b

where τ is the scattering time, d is dimension of the system, f0 is the Fermi distribution, ⟨vc ⟩nm = ⟨unk |v̂b |umk ⟩
are velocity matrix elements with
P ⟨vc ⟩nk being the diH = H0 + HSOC .
(5)
agonal entries, ⟨jbLa ⟩P
nk ≡ Re
m ⟨vb ⟩nm ⟨La ⟩mn , and
1
1
2
⟨L⟩
=
(ieℏ
/4µ
)
(
mn
B
p̸
=
m,n
Here,
εpk −εmk + εpk −εnk )⟨v⟩mp ×
⟨v⟩pn are the matrix elements of orbital angular momenH0 = 4t1 cos(kx /2) cos(ky /2)τx + 2t2 [cos(kx ) + cos(ky )] τ0 tum [8, 10, 53–55]. According to symmetry analysis, this
L
+2ts [cos(kx ) − cos(ky )] τz + Jτz N · σ,
(6) system should support component σxxz . In Fig. 2(d), we
Lz
plot σxx as a function of spin-conserve SOC strength λc
where τ ’s and σ’s are Pauli matrices denoting respecfor Fermi level at −0.04 eV, away from band degeneracies
tively the sublattice and spin degrees of freedom, t’s
[see Fig. 2(c)]. One observes that MOHE indeed vanishes
are hopping parameters with t2 = 12 (t2a + t2b ) and
when SOC is absent, and its value increases linearly with
Lz
ts = 21 (t2a − t2b ) [as illustrated in Fig. 2(a)], and ts conλc . If we change the SOC to spin-flip type, then σxx
extrols the nonrelativistic spin splitting. The last term is
hibits a quadratic increase, as shown in Fig. 2(e). These
the exchange coupling to Néel order with J being the
results are consistent with our perturbative results in Tacoupling strength, and we shall take N = ẑ. For the
ble I.
SOC part, we can separately consider the spin-conserve
More importantly, MOHE can acquire nonperturbative
f
c
(HSOC
) and spin-flip (HSOC
) components, with
enhancement when the Fermi level lies close to a SOCinduced gap. In Fig. 2(f), we plot the result for a Fermi
c
HSOC
= 4λc sin(kx /2) sin(ky /2)τy σz ,
(7)
level at 0.06 eV, near the small gap opened by spin-flip
f
HSOC
= 4λf sin(kx /2) cos(ky /2)τy σx
SOC. Clearly, the dependence on spin-flip SOC strength
λf deviates from the quadratic scaling predicted by per+4λf cos(kx /2) sin(ky /2)τy σy , (8)
turbative analysis. Moreover, the magnitude of MOHE
exhibits a sharp increase with λf , showing the significant
where λ’s are the corresponding SOC strengths.
enhancement from SOC gaps. From the formula (9), this
Figure 2(b) shows the calculated band structure withnonperturbative characteristic originates from interband
out SOC, displaying characteristic d-wave altermagnetic
coherence amplified by band near-degeneracies.
spin splitting on Γ-X/Y and M -X/Y paths. Turning on
Below, we shall see that the features observed above
SOC opens local gaps in the band structure [Fig. 2(c)].
are also validated in real altermagnetic materials. ParThe crossing points at µ ∼ 0.2 eV are opened by spinticularly, although the MOHE needs SOC, its magnitude
conserve SOC, since these degeneracies are composed of

4

(b)

(a)

(b)

t 2a

y

t1

(c)

Cr

0.06 eV

σL/τ

Energy (eV)

0.5

-0.04 eV

(e)

M

M

Γ

Spin-conserve

0

-10
-0.1

Γ

Spin-ﬂip

(f) 10

0
σL/τ

σL/τ

0

0
λc / t1

0.1

λc / t1
Spin-conserve
Spin-ﬂip

(c)

(d)
1

0
λf / t1

0.1

0

Total
Spin-conserve
Spin-ﬂip

0

0

-400

-1

-800
ΓAʼ Lʼ Hʼ Aʼ

-0.1

50

0
μ (eV)

-50
0.1

FIG. 3. (a) Crystal structure, (b) Brillouin zone, and (c) nonrelativistic band structure of CrSb. (d) Calculated collinearlySx
Lx
/τ (orange
/τ (red solid line) and σxy
polarized responses σxy
dotted line) versus chemical potential. The spin-conserve
(green solid line) and spin-flip (blue solid line) contributions
Lx
to σxy
/τ are also plotted.

-10
-20

-4
-0.1

Lʼ
M

b

a

Γ MK

-0.5
M X Γ Y

K

c

(d) 10

0

Γ

Hʼ

0

-0.5
M X Γ Y

x

Aʼ

σxySx /τ

t 2b

Sb

Energy (eV)

Energy (eV)

0.5

σxyL x /τ

(a)

-30
-0.1

0
λf / t1

0.1

FIG. 2. (a) Illustration of the 2D d-wave altermagnetic model
in (5). (b) Calculated non-relativistic band structure. Spinup and spin-down bands are denoted by red and blue colors.
(c) Band structure with SOC strength λc = λf = 0.1t1 . (d)
σ L /τ versus spin-conserve SOC strength λc . The spin-flip
SOC is turned off. (e) Same as (d), but with the roles of
spin-flip and spin-conserve SOC interchanged. In (d) and (e),
the chemical potential is set to µ = −0.04 eV. (f) The result
at µ = 0.06 eV near an SOC-gap. In the calculation, we take
4t1 = 0.2, 2t2 = −0.08, 2td = −0.04, and J = 0.11. The unit
of σ L /τ is (ℏ/e) Ω−1 cm−1 fs−1 .

in altermagnets can be significant and can dominate over
spin Hall response, contrary to previous expectations.
CrSb: Giant collinearly-polarized MOHE. We first consider the experimentally verified altermagnetic metal
CrSb [56–59]. The crystal structure of CrSb has hexagonal space group P 63 /mmc [Fig. 3(a)]. Its Néel temperature is ∼ 700 K, with Néel vector along z. And the spin
Laue group is 2 6/2 m2 m1 m. Figure 3(c) shows the band
structure without SOC computed using first-principles
methods (calculation details in Ref. [50]).
According to Table I, this material supports only one
Lx
Lx
CPOC component, σxy
. Figure 3(d) plots σxy
/τ as a
function of Fermi level µ at T = 300 K. The correspondSx
ing component σxy
of magnetic spin Hall conductivity
is also plotted for comparison. One observes in a wide

Lx
Sx
energy window, σxy
and σxy
exhibit opposite signs, and
Lx
σxy is about 50 times greater than its spin counterpart.
Interestingly, the orbital and spin responses here originate from different types of SOC: we explicitly show that
the orbital conductivity is mainly from the spin-conserve
SOC, whereas the spin conductivity primarily arises from
spin-flip SOC (Fig. S2 in Supplemental Material), a feature consistent with the results in Table I.
The scattering time can be estimated from experiLx
ment [60] as τ ∼ 15 fs at 300 K. Then, we find σxy
−1
−1
reaches a giant value of ∼ −8703 (ℏ/e) Ω cm at 300
Sx
K [σxy
is ∼ 176 (ℏ/e) Ω−1 cm−1 ], and it can be further increased to be ∼ −3.1×104 (ℏ/e) Ω−1 cm−1 at 100 K (Fig.
S3 in Supplemental Material). For comparison, the previously reported collinearly-polarized spin Hall conductivities are usually less than 50 (ℏ/e) Ω−1 cm−1 [61], and
a recent reported value of 100 ∼ 200 (ℏ/e) Ω−1 cm−1 in
TaIrTe4 was considered very large [62–64]. These demonstrate that the MOHE dominates the angular momentum
transport in altermagnet CrSb, and it offers a remarkably
large CPOC, desired for applications.
FeSb2 : Dominance over nonrelativistic spin response.
Our second example is altermagnetic FeSb2 [65–67],
which crystallizes in the orthorhombic structure with
space group P nnm. Its Néel temperature is ∼ 700 K,
with the easy axis along y [Fig. 4(a)]. Figure 4(c) shows
the calculated nonrelativistic band structure. Differing
from CrSb, the spin Laue group of FeSb2 is 2 m2 m1 m,
S
which allows a nonrelativistic spin Hall conductivity σyxy
in the absence of SOC, with the spin polarization parallel
to the Néel vector. The symmetry of FeSb2 also permits

5
(c) 1
Z

U

Γ

X

R
S

(d)

S

σyxy
L
σyxy

0

S

σyxy,(0)
L
σyxy,(0)

σ/τ

(b)

Energy (eV)

(a)

0

-200

c

-1
ΓX S Γ

(f) 150

S

σyxy
L
σyxy

σyxL y /τ

σ(×103 h/e Ω-1 cm-1)

(e) 0

Fe

-1

Total
Spin-conserve
Spin-ﬂip

200
T (K)

300

Z

X

0
-103

-300
-0.1

0
μ (eV)

-400
-0.1

0
μ (eV)

(h)
103

Γ
-150

Z

U

0

-2
100

(g)

Z U R

0.1

Fermi contour

Nodal surface

Sb

b

a

Z

U

Γ

X

0.1

L

FIG. 4. (a) Crystal structure, (b) Brillouin zone, and (c) non-relativistic band structure of FeSb2 . (d) Calculated σyxy /τ and
S
σyxy /τ versus chemical potential. Here, σ (0) ’s (dashed lines) denote results in the absence of SOC. (e) Dependence of the results
L
on temperature. The solids lines serve as a guide to the eyes. (f) Spin-conserve and spin-flip contributions to σyxy . (g) Spin-flip
Ly
contribution to the k-resolved σyx (the integrand of Eq. (9)) on the ky = 0 plane. (h) In the ky = 0 plane, two bands form a
nodal surface in the absence of SOC. After SOC is turned on, the nodal surface is gapped, leading to the peak values in (g).
L

CPOC component σyxy in the same direction. Usually,
S
L
one may guess that σyxy should be much less than σyxy ,
Ly
given that σyx is of higher order in SOC. Surprisingly,
we find that the reality is not the case.
S

L

Figure 4(d) shows the calculated σyxy and σyxy in the
absence and presence of SOC at T = 300 K. In the nonrelL
S
ativistic limit, σyxy remains finite, whereas σyxy vanishes.
L
Sy
Upon introducing SOC, σyx is not altered much, but σyxy
is significantly increased, acquiring a magnitude compaS
rable to σyxy . Taking τ ∼ 2.5 fs as estimated from experiL
ment [68], we find σyxy ∼ −613 (ℏ/e) Ω−1 cm−1 at 300 K,
S
which is even larger than σyxy ∼ −552 (ℏ/e) Ω−1 cm−1 .
At lower temperatures, the responses become larger, and
the orbital term remains greater than the spin one [Figure 4(e)].
This example clearly demonstrates that one has to be
very careful in judging which effect is larger or weaker
based solely on perturbative argument of the SOC dependence. Here, MOHE, despite being higher order in
SOC, wins the competition against nonrelativistic spin
Hall response. To explore the origin of this counterintuitive result, we analyze the spin-conserve and spin-flip
L
contributions to σyxy in Fig. 4(f), finding that the spinflip SOC dominates the response. In Fig. 4(g), we plot
the spin-flip contribution to the k-resolved integrand in
Eq. (9), showing notable peaks in the ky = 0 plane.
This correlates with a dispersive nodal surface [69] in the
ky = 0 plane enforced by [C2 ∥My ] spin-group symmetry

and formed by two opposite spin states, as illustrated in
Fig. 4(h). This nodal surface crosses the Fermi level with
its SOC gap opened by spin-flip SOC, which explains the
nonperturbative enhancement of MOHE.
Discussion. We have revealed that MOHE, while forbidden in conventional antiferromagnets, universally exists in the emerging class of altermagnetic materials.
Compared to the previously highlighted nonrelativistic
spin Hall effect [36, 70–72], MOHE in altermagnets must
require SOC. It has been a common practice in prior
studies to infer relative importance of an effect in altermagnets based on its SOC dependence. However, this
common wisdom fails here. We demonstrate concrete
material examples where the MOHE reaches giant values,
even surpassing the nonrelativistic spin response. Such
enhancement is of nonperturbative character regarding
SOC. It is connected to small SOC gaps near Fermi level,
leading to increased interband coherence that contributes
to orbital responses. The new understanding obtained
here offers guideline for searching and designing orbital
source materials with improved performance, and opens
a new horizon for the application of altermagnets in information technology.
We have focused on MOHE which is T -odd. There
may also exist the conventional T -even orbital Hall effect in altermagnets. In [50], we also perform symmetry analysis of T -even orbital (and spin) Hall effect in
collinear altermagnets, and show that the CPOC from
T -even response is severely constrained, limited to only

6
4 spin Laue classes of altermagnets. In particular, CPOC
from T -even orbital Hall effect is forbidden in CrSb and
FeSb2 .
Our work already predicts two concrete materials for
exploring MOHE. To utilize MOHE for magnetic manipulation and switching, the generated CPOC current
needs to be injected into an adjacent ferromagnetic layer,
converted to spin current, and then drives the local moments in the ferromagnetic layer. This conversion process
is described by the orbital-to-spin conversion efficiency
η, which is a characteristic number for the ferromagnetic
layer. For example, a large η ∼ 38% can be achieved for
Fe3 GaTe2 [24]. One is usually concerning with the effec∗
tive orbital Hall angle θL
≡ (2e/ℏ)ηρσ L as a performance
indicator, with ρ being the resistivity of the orbital Hall
∗
material. We estimate that at room temperature, θL
can
reach −37% and −15% respectively for CrSb and FeSb2 ,
when Fe3 GaTe2 is used as the ferromagnetic layer. Such
values are much larger than the strongest reported spin
Hall angles (∼ 10%) with collinearly-polarized spin Hall
current [62–64, 73], suggesting them as good platforms
for verifying our theory and for orbitronic applications.

∗

shengyuan.yang@polyu.edu.hk
congxiao@fudan.edu.cn
[1] B. A. Bernevig, T. L. Hughes, and S.-C. Zhang, Orbitronics: The intrinsic orbital current in p-doped silicon,
Phys. Rev. Lett. 95, 066601 (2005).
[2] G. Y. Guo, Y. Yao, and Q. Niu, Ab initio calculation
of the intrinsic spin hall effect in semiconductors, Phys.
Rev. Lett. 94, 226601 (2005).
[3] H. Kontani, T. Tanaka, D. Hirashima, K. Yamada, and
J. Inoue, Giant orbital hall effect in transition metals:
Origin of large spin and anomalous hall effects, Phys.
Rev. Lett. 102, 016601 (2009).
[4] D. Go, D. Jo, C. Kim, and H.-W. Lee, Intrinsic spin and
orbital hall effects from orbital texture, Phys. Rev. Lett.
121, 086602 (2018).
[5] S. Bhowal and S. Satpathy, Intrinsic orbital moment
and prediction of a large orbital hall effect in twodimensional transition metal dichalcogenides, Phys. Rev.
B 101, 121112 (2020).
[6] G. Sala and P. Gambardella, Giant orbital hall effect and
orbital-to-spin conversion in 3 d, 5 d, and 4 f metallic
heterostructures, Phys. Rev. Res. 4, 033037 (2022).
[7] L. Salemi and P. M. Oppeneer, First-principles theory of
intrinsic spin and orbital hall and nernst effects in metallic monoatomic crystals, Phys. Rev. Mater. 6, 095001
(2022).
[8] A. Pezo, D. Garcı́a Ovalle, and A. Manchon, Orbital hall
effect in crystals: Interatomic versus intra-atomic contributions, Phys. Rev. B 106, 104414 (2022).
[9] M. Costa, B. Focassio, L. M. Canonico, T. P. Cysne,
G. R. Schleder, R. B. Muniz, A. Fazzio, and T. G.
Rappoport, Connecting higher-order topology with the
orbital hall effect in monolayers of transition metal
dichalcogenides, Phys. Rev. Lett. 130, 116204 (2023).
†

[10] B. Göbel and I. Mertig, Orbital hall effect accompanying
quantum hall effect: Landau levels cause orbital polarized edge currents, Phys. Rev. Lett. 133, 146301 (2024).
[11] Y.-G. Choi, D. Jo, K.-H. Ko, D. Go, K.-H. Kim, H. G.
Park, C. Kim, B.-C. Min, G.-M. Choi, and H.-W. Lee,
Observation of the orbital hall effect in a light metal ti,
Nature 619, 52 (2023).
[12] I. Lyalin, S. Alikhah, M. Berritta, P. M. Oppeneer, and
R. K. Kawakami, Magneto-optical detection of the orbital
hall effect in chromium, Phys. Rev. Lett. 131, 156702
(2023).
[13] D. Jo, D. Go, and H.-W. Lee, Gigantic intrinsic orbital
hall effects in weakly spin-orbit coupled metals, Phys.
Rev. B 98, 214405 (2018).
[14] Z. C. Zheng, Q. X. Guo, D. Jo, D. Go, L. H. Wang, H. C.
Chen, W. Yin, X. M. Wang, G. H. Yu, W. He, H.-W. Lee,
J. Teng, and T. Zhu, Magnetization switching driven by
current-induced torque from weakly spin-orbit coupled
zr, Phys. Rev. Res. 2, 013127 (2020).
[15] D. Go and H.-W. Lee, Orbital torque: Torque generation
by orbital current injection, Phys. Rev. Res. 2, 013177
(2020).
[16] S. Ding, A. Ross, D. Go, L. Baldrati, Z. Ren, F. Freimuth,
S. Becker, F. Kammerbauer, J. Yang, G. Jakob,
Y. Mokrousov, and M. Kläui, Harnessing orbital-to-spin
conversion of interfacial orbital currents for efficient spinorbit torques, Phys. Rev. Lett. 125, 177201 (2020).
[17] J. Kim, D. Go, H. Tsai, D. Jo, K. Kondou, H.-W.
Lee, and Y. Otani, Nontrivial torque generation by
orbital angular momentum injection in ferromagneticmetal/Cu/al2 o3 trilayers, Phys. Rev. B 103, L020407
(2021).
[18] S. Lee, M.-G. Kang, D. Go, D. Kim, J.-H. Kang, T. Lee,
G.-H. Lee, J. Kang, N. J. Lee, Y. Mokrousov, et al.,
Efficient conversion of orbital hall current to spin current
for spin-orbit torque switching, Commun. Phys. 4, 234
(2021).
[19] D. Lee, D. Go, H.-J. Park, W. Jeong, H.-W. Ko, D. Yun,
D. Jo, S. Lee, G. Go, J. H. Oh, et al., Orbital torque in
magnetic bilayers, Nat. Commun. 12, 6710 (2021).
[20] Z. Zheng, T. Zeng, T. Zhao, S. Shi, L. Ren, T. Zhang,
L. Jia, Y. Gu, R. Xiao, H. Zhou, et al., Effective electrical
manipulation of a topological antiferromagnet by orbital
torques, Nat. Commun. 15, 745 (2024).
[21] S. Ding, M.-G. Kang, W. Legrand, and P. Gambardella,
Orbital torque in rare-earth transition-metal ferrimagnets, Phys. Rev. Lett. 132, 236702 (2024).
[22] Y. Yang, P. Wang, J. Chen, D. Zhang, C. Pan, S. Hu,
T. Wang, W. Yue, C. Chen, W. Jiang, et al., Orbital
torque switching in perpendicularly magnetized materials, Nat. Commun. 15, 8645 (2024).
[23] R. Gupta, C. Bouard, F. Kammerbauer, J. O. LedesmaMartin, A. Bose, I. Kononenko, S. Martin, P. Usé,
G. Jakob, M. Drouard, et al., Harnessing orbital hall effect in spin-orbit torque mram, Nat. Commun. 16, 130
(2025).
[24] D. Zhang, H. Wei, J. Duan, J. Chen, J. Chen, D. Yue,
W. Gong, P. Liu, Y. Yang, J. Gou, et al., Orbital torque
switching of room temperature two-dimensional van der
waals ferromagnet fe3gate2, Nat. Commun. 16, 7047
(2025).
[25] S. Peng, X. Zheng, S. Li, B. Lao, Y. Han, Z. Liao,
H. Zheng, Y. Yang, T. Yu, P. Liu, et al., Unconventional
scaling of the orbital hall effect, Nature Materials 24,

7
1749 (2025).
[26] L. Salemi and P. M. Oppeneer, Theory of magnetic spin
and orbital hall and nernst effects in bulk ferromagnets,
Phys. Rev. B 106, 024410 (2022).
[27] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond conventional ferromagnetism and antiferromagnetism: A phase
with nonrelativistic spin and crystal rotation symmetry,
Phys. Rev. X 12, 031042 (2022).
[28] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging research landscape of altermagnetism, Phys. Rev. X 12,
040501 (2022).
[29] C. Wu, K. Sun, E. Fradkin, and S.-C. Zhang, Fermi liquid
instabilities in the spin channel, Phys. Rev. B 75, 115103
(2007).
[30] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Spin current generation in organic antiferromagnets, Nat. Commun. 10, 4305 (2019).
[31] S. Hayami, Y. Yanagi, and H. Kusunose, Momentumdependent spin splitting by collinear antiferromagnetic
ordering, j. Phys. Soc. Jpn. 88, 123702 (2019).
[32] L. Šmejkal, R. González-Hernández, T. Jungwirth, and
J. Sinova, Crystal time-reversal symmetry breaking and
spontaneous hall effect in collinear antiferromagnets, Sci.
Adv. 6, eaaz8809 (2020).
[33] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, Giant momentum-dependent spin splitting in
centrosymmetric low-z antiferromagnets, Phys. Rev. B
102, 014422 (2020).
[34] D.-F. Shao, S.-H. Zhang, M. Li, C.-B. Eom, and E. Y.
Tsymbal, Spin-neutral currents for spintronics, Nat.
Commun. 12, 7061 (2021).
[35] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia, and
J. Liu, Multifunctional antiferromagnetic materials with
giant piezomagnetism and noncollinear spin current, Nat.
Commun. 12, 2846 (2021).
[36] R. González-Hernández, L. Šmejkal, K. Výborný, Y. Yahagi, J. Sinova, T. c. v. Jungwirth, and J. Železný,
Efficient electrical spin splitter based on nonrelativistic collinear antiferromagnetism, Phys. Rev. Lett. 126,
127701 (2021).
[37] L. Šmejkal, A. B. Hellenes, R. González-Hernández,
J. Sinova, and T. Jungwirth, Giant and tunneling magnetoresistance in unconventional collinear antiferromagnets with nonrelativistic spin-momentum coupling, Phys.
Rev. X 12, 011028 (2022).
[38] D.-F. Shao, Y.-Y. Jiang, J. Ding, S.-H. Zhang, Z.-A.
Wang, R.-C. Xiao, G. Gurung, W. J. Lu, Y. P. Sun, and
E. Y. Tsymbal, Néel spin currents in antiferromagnets,
Phys. Rev. Lett. 130, 216702 (2023).
[39] L. Bai, W. Feng, S. Liu, L. Šmejkal, Y. Mokrousov, and
Y. Yao, Altermagnetism: Exploring new frontiers in magnetism and spintronics, Adv. Funct. Mater. 34, 2409327
(2024).
[40] R.-W. Zhang, C. Cui, R. Li, J. Duan, L. Li, Z.-M. Yu,
and Y. Yao, Predictable gate-field control of spin in altermagnets with spin-layer coupling, Phys. Rev. Lett. 133,
056401 (2024).
[41] C. Song, H. Bai, Z. Zhou, L. Han, H. Reichlova, J. H.
Dil, J. Liu, X. Chen, and F. Pan, Altermagnets as a new
class of functional materials, Nat. Rev. Mater. 10, 473
(2025).
[42] H. Zhang, F. Freimuth, S. Blugel, Y. Mokrousov, and
I. Souza, Role of spin-flip transitions in the anomalous
hall effect of fept alloy, Phys. Rev. Lett. 106, 117202

(2011).
[43] G. Y. Guo, Q. Niu, and N. Nagaosa, Anomalous nernst
and hall effects in magnetized platinum and palladium,
Phys. Rev. B 89, 214406 (2014).
[44] Z. Liu, M. Wei, W. Peng, D. Hou, Y. Gao, and Q. Niu,
Multipolar anisotropy in anomalous hall effect from spingroup symmetry breaking, Phys. Rev. X 15, 031006
(2025).
[45] M. Roig, Y. Yu, R. C. Ekman, A. Kreisel, B. M. Andersen, and D. F. Agterberg, Quasisymmetry-constrained
spin ferromagnetism in altermagnets, Phys. Rev. Lett.
135, 016703 (2025).
[46] H. Kurebayashi, Going in the right direction, Nat. Phys.
13, 209 (2017).
[47] J. Ryu, S. Lee, K.-J. Lee, and B.-G. Park, Currentinduced spin–orbit torques for spintronic applications,
Adv. Mater. 32, 1907148 (2020).
[48] H. Yang and Y. Liu, Field-free and unconventional
switching of perpendicular magnetization at room temperature, Nat. Electron. 6, 724 (2023).
[49] P. Liu, J. Li, J. Han, X. Wan, and Q. Liu, Spin-group
symmetry in magnetic materials with negligible spinorbit coupling, Phys. Rev. X 12, 021016 (2022).
[50] See Supplemental Material for theoretical and computational details.
[51] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F.
Agterberg, Minimal models for altermagnetism, Phys.
Rev. B 110, 144412 (2024).
[52] D. S. Antonenko, R. M. Fernandes, and J. W. Venderbos,
Mirror chern bands and weyl nodal loops in altermagnets,
Phys. Rev. Lett. 134, 096703 (2025).
[53] S. Sun, Z. Song, H. Weng, and X. Dai, Topological metals
induced by the zeeman effect, Phys. Rev. B 101, 125118
(2020).
[54] Óscar Pozo Ocaña and I. Souza, Multipole theory of optical spatial dispersion in crystals, SciPost Phys. 14, 118
(2023).
[55] T. P. Cysne, S. Bhowal, G. Vignale, and T. G. Rappoport, Orbital hall effect in bilayer transition metal
dichalcogenides: From the intra-atomic approximation
to the bloch states orbital magnetic moment approach,
Phys. Rev. B 105, 195421 (2022).
[56] S. Reimers, L. Odenbreit, L. Šmejkal, V. N. Strocov,
P. Constantinou, A. B. Hellenes, R. Jaeschke Ubiergo,
W. H. Campos, V. K. Bharadwaj, A. Chakraborty, et al.,
Direct observation of altermagnetic band splitting in crsb
thin films, Nat. Commun. 15, 2116 (2024).
[57] J. Ding, Z. Jiang, X. Chen, Z. Tao, Z. Liu, T. Li, J. Liu,
J. Sun, J. Cheng, J. Liu, et al., Large band splitting in
g-wave altermagnet crsb, Phys. Rev. Lett. 133, 206401
(2024).
[58] G. Yang, Z. Li, S. Yang, J. Li, H. Zheng, W. Zhu, Z. Pan,
Y. Xu, S. Cao, W. Zhao, et al., Three-dimensional mapping of the altermagnetic spin splitting in crsb, Nat.
Commun. 16, 1442 (2025).
[59] Z. Zhou, X. Cheng, M. Hu, R. Chu, H. Bai, L. Han,
J. Liu, F. Pan, and C. Song, Manipulation of the altermagnetic order in crsb via crystal symmetry, Nature 638,
645 (2025).
[60] X. Peng, Y. Wang, S. Zhang, Y. Zhou, Y. Sun, Y. Su,
C. Wu, T. Zhou, L. Liu, H. Wang, J. Yang, B. Chen,
Z. Fang, J. Du, Z. Jiao, Q. Wu, and M. Fang, Scaling
behavior of magnetoresistance and hall resistivity in the

8
altermagnet crsb, Phys. Rev. B 111, 144402 (2025).
[61] F. Wang, G. Shi, K.-W. Kim, H.-J. Park, J. G. Jang,
H. R. Tan, M. Lin, Y. Liu, T. Kim, D. Yang, et al.,
Field-free switching of perpendicular magnetization by
two-dimensional ptte2/wte2 van der waals heterostructures with high spin hall conductivity, Nat. Mater. 23,
768 (2024).
[62] Y. Liu, G. Shi, D. Kumar, T. Kim, S. Shi, D. Yang,
J. Zhang, C. Zhang, F. Wang, S. Yang, et al., Fieldfree switching of perpendicular magnetization at room
temperature using out-of-plane spins from tairte4, Nat.
Electron. 6, 732 (2023).
[63] Y. Zhang, H. Xu, K. Jia, G. Lan, Z. Huang, B. He,
C. He, Q. Shao, Y. Wang, M. Zhao, et al., Room temperature field-free switching of perpendicular magnetization
through spin-orbit torque originating from low-symmetry
type ii weyl semimetal, Sci. Adv. 9, eadg9819 (2023).
[64] L. Bainsla, B. Zhao, N. Behera, A. M. Hoque,
L. Sjöström, A. Martinelli, M. Abdel-Hafiez, J. Åkerman,
and S. P. Dash, Large out-of-plane spin–orbit torque in
topological weyl semimetal tairte4, Nat. Commun. 15,
4649 (2024).
[65] I. I. Mazin, K. Koepernik, M. D. Johannes, R. GonzálezHernández, and L. Šmejkal, Prediction of unconventional
magnetism in doped fesb2, Proc. Natl. Acad. Sci. U.S.A.
118, e2108924118 (2021).
[66] L. Attias, A. Levchenko, and M. Khodas, Intrinsic
anomalous hall effect in altermagnets, Phys. Rev. B 110,
094425 (2024).
[67] C. Phillips, G. Pokharel, K. Shtefiienko, S. R. Bhandari, D. E. Graf, D. Rai, and K. Shrestha, Electronic

structure of the altermagnet candidate fesb 2: High-field
torque magnetometry and density functional theory studies, Phys. Rev. B 111, 075141 (2025).
[68] C. Petrovic, J. W. Kim, S. L. Bud’ko, A. I. Goldman,
P. C. Canfield, W. Choe, and G. J. Miller, Anisotropy
and large magnetoresistance in the narrow-gap semiconductor fesb2 , Phys. Rev. B 67, 155205 (2003).
[69] W. Wu, Y. Liu, S. Li, C. Zhong, Z.-M. Yu, X.-L. Sheng,
Y. X. Zhao, and S. A. Yang, Nodal surface semimetals:
Theory and material realization, Phys. Rev. B 97, 115125
(2018).
[70] A. Bose, N. J. Schreiber, R. Jain, D.-F. Shao, H. P.
Nair, J. Sun, X. S. Zhang, D. A. Muller, E. Y. Tsymbal, D. G. Schlom, et al., Tilted spin current generated
by the collinear antiferromagnet ruthenium dioxide, Nat.
Electron. 5, 267 (2022).
[71] S. Karube, T. Tanaka, D. Sugawara, N. Kadoguchi,
M. Kohda, and J. Nitta, Observation of spin-splitter
torque in collinear antiferromagnetic ruo2 , Phys. Rev.
Lett. 129, 137201 (2022).
[72] H. Bai, Y. C. Zhang, Y. J. Zhou, P. Chen, C. H. Wan,
L. Han, W. X. Zhu, S. X. Liang, Y. C. Su, X. F. Han,
F. Pan, and C. Song, Efficient spin-to-charge conversion
via altermagnetic spin splitting effect in antiferromagnet
ruo2 , Phys. Rev. Lett. 130, 216701 (2023).
[73] I. Abdelwahab, D. Kumar, T. Bian, H. Zheng, H. Gao,
F. Hu, A. McClelland, K. Leng, W. L. Wilson, J. Yin,
et al., Two-dimensional chiral perovskites with large spin
hall angle and collinear spin hall conductivity, Science
385, 311 (2024).

