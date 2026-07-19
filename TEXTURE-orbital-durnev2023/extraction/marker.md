# durnev2023 — text extraction (pdftotext interim)

> NOTE: `marker` and `nougat` binaries are not installed on this host
> (`which marker nougat` -> not found). This is the pdftotext-derived
> extraction used as an interim substitute. Layout/equations are
> linearized; consult the source PDF for exact equation typesetting.

```
Faraday and Kerr rotation due to photoinduced orbital magnetization in
two-dimensional electron gas
M. V. Durnev

arXiv:2306.08509v1 [cond-mat.mes-hall] 14 Jun 2023

Ioffe Institute, 194021 St. Petersburg, Russia
We study theoretically the Faraday and Kerr rotation of a probe field due to the orbital magnetization of a two-dimensional electron gas induced by a circularly polarized pump. We develop a
microscopic theory of these effects in the intraband spectral range based on the analytical solution of
the kinetic equation for linear and parabolic energy dispersion of electrons and arbitrary scattering
potential. We show that the spectral dependence of rotation angles and accompanying ellipticities
experiences a sharp resonance when the probe and pump frequencies are close to each other. At the
resonance, the Faraday and Kerr rotation angles are of the order of 0.1◦ per 1 kW/cm2 of the pump
intensity in graphene samples, corresponding to a pump-induced synthetic magnetic field of about
0.1 T. We also analyze the influence of the dielectric contrast between dielectric media surrounding
the two-dimensional electron gas on the rotation angles.

I.

INTRODUCTION

Optically induced magnetization and its manipulation
in solids have recently attracted significant attention in
solid-state physics [1–4]. Absorption of circularly polarized photons results in efficient magnetization of electron
and hole systems in the process of optical spin orientation
through both the interband and intraband optical transitions [5–10]. Besides the spin orientation, the circularly
polarized light induces orbital currents of charge carriers,
and hence, the orbital magnetic moment, known as the
inverse Faraday effect (IFE) [11, 12]. The orbital magnetization due to the IFE is being actively studied in different systems, including metals and semiconductors [13–16],
ferromagnets [17], superconductors [18], metallic nanoparticles [19] and graphene [20].

ing in the circular birefringence and dichroism. This, in
turn, leads to rotation of the transmitted and reflected
probe field. Moreover, the initially linearly polarized
probe becomes elliptically polarized (acquires ellipticity),
Fig. 1. We develop a microscopic theory of the pumpinduced high-frequency conductivity of 2DEG due to intraband optical transitions and calculate the Faraday and
Kerr angles as well as the corresponding ellipticities. The
theory accounts for electron scattering by impurities and
describes both non-absorbing and absorbing regimes of
the pump and probe fields. We derive analytical expressions for the Faraday and Kerr angles and ellipticities valid
for parabolic and linear energy dispersion of 2D electrons
and arbitrary scattering potential. We also analyze the influence of the dielectric contrast between dielectric media
surrounding 2DEG on the rotation angles.

To probe the light-induced orbital magnetic moment,
one can use the pump-probe Faraday and Kerr spectroscopy – the method, which is widely employed to study
the magnitude and dynamics of magnetization related to
both spin and orbital magnetic moment [4, 7, 21–27].
In this method, one measures the rotation of the polarization plane of linearly polarized probe beam, which is
reflected from or transmitted through the medium with
pump-induced magnetization. While the theory of the
pump-probe Faraday and Kerr effects due to spin magnetization has been developed for bulk and low-dimensional
semiconductor systems [7, 28–30], consistent microscopic
theory of these effects due to orbital magnetization is still
missing. The naive mechanism of such a Faraday rotation could involve magnetic field induced by the orbital
currents, however this magnetic field is extremely small
and, hence, cannot be the major source of rotation. The
third-order contribution to ac current induced by elliptically polarized electric field in graphene and responsible
for the Faraday rotation, has been calculated in Ref. [31].
However, the calculations were based on a simplified relaxation model, which does not fully capture the specifics
of electron scattering in two-dimensional systems.

FIG. 1. Schematic picture of the pump-induced Faraday and
Kerr rotation in the two-dimensional electron gas. Electric
field of the circularly polarized pump acts as a synthetic magnetic field resulting in the rotation of the linearly polarized
probe field. θF and θK are the Faraday and Kerr rotation angles, respectively.

Here, we study the Faraday and Kerr rotation due to
the orbital magnetization induced by circularly polarized
pump in a two-dimensional electron gas (2DEG). We show
that the circularly polarized electric field of the pump
modifies the high-frequency conductivity of 2DEG, result-

We show that the spectral dependence of rotation angles and ellipticities experiences a sharp resonance, when
probe and pump frequencies are close to each other. The
width and the magnitude of resonance are determined by

pump E⌦ (t)

probe E! (t)
✓K

x

y
z

✓F

2
a long energy relaxation time, rather than a short momentum relaxation time. At the resonance, and at Ωτ1 ∼ 1,
where Ω is the pump frequency, and τ1 is the momentum relaxation time, the Faraday and Kerr rotation angles are of the order of 0.1◦ per 1 kW/cm2 of the pump
intensity in graphene samples. We also calculate a synthetic magnetic field, an effective magnetic field, which
leads to the same rotation angles as the circularly polarized pump. In graphene samples, this synthetic magnetic
field amounts to ∼ 0.1 T per 1 kW/cm2 of the pump
intensity at Ωτ1 ∼ 1.

II.

FARADAY AND KERR ROTATION BY A 2D
CONDUCTING MEDIUM

We consider 2DEG occupying the plane z = 0 and
surrounded by dielectrics with refractive indices n1 at
z < 0 and n2 at z > 0. The 2DEG is irradiated by
normally incident pump and probe beams with electric
fields EΩ (t) = EΩ e−iΩt + c.c and Eω (t) = Eω e−iωt + c.c,
respectively, see Fig. 1. In the absence of pump field,
EΩ = 0, the probe field induces electric current in 2DEG
j(t) = jω e−iωt + c.c, which oscillates at the probe frequency and is parallel to the probe electric field Eω . The
current is related to the probe field as jω = σEω , where
σ = e2 ne τ1 /m(1 − iωτ1 ) is the high-frequency 2DEG conductivity, e and m are the electron charge and effective
mass, respectively, ne is the 2D electron concentration
and τ1 is the momentum relaxation time.
In the presence of the pump field, the third-order contributions to the current jω appear. These contributions
in the isotropic 2DEG are described by the following equation with three complex parameters γj [32]:
∗
∗
jω = γ1 |EΩ |2 Eω + γ2 [EΩ
(EΩ · Eω ) + EΩ (EΩ
· Eω )]
∗
+ iγ3 [Eω × [EΩ × EΩ ]] . (1)

Here, γ1 describes the change of isotropic conductivity
due to the pump radiation, whereas γ2 and γ3 give rise to
the transverse current in the direction perpendicular to
Eω induced by linearly and circularly polarized pump, respectively. In this paper, we consider circularly polarized
pump, and therefore, the γ3 contribution [33]. For circularly polarized pump, Eq. (1) yields the transverse current
described by the off-diagonal conductivity σxy = −σyx =
γ3 |EΩ |2 Pcirc , where Pcirc = ±1 for right-hand and lefthand circular polarization, respectively. Note that, when
the probe field is static, i.e. at ω = 0, the γ3 contribution
describes the appearance of a transverse direct current in
the presence of a circularly polarized pump – the so-called
photovoltaic or circular Hall effect [32, 34, 35].
Pump-induced transverse conductivity σxy = −σyx
leads to circular birefringence and circular dichroism, i.e.
different transmission and absorption of the right-hand
and left-hand circularly polarized components of the probe
field. The incident linearly polarized probe field is a su(i)
(i)
perposition of circularly polarized fields Eω,± = Eω o± ,
where o± are circularly polarized unit vectors related√to
the unit vectors ex ∥ x and ey ∥ y as o± = (ex ± iey )/ 2.
The amplitude transmission and reflection coefficients of

(i)

Eω,± are given by [36]
t± =

t12
,
1 + α±

r± =

r12 − α±
,
1 + α±

(2)

where r12 = (n1 − n2 )/(n1 + n2 ) and t12 = r12 + 1 are the
amplitude reflection and transmission coefficients for the
light incident on the boundary between two dielectrics in
the absence of the 2DEG layer, α± = 2πσ± /(cn̄), σ± =
σxx ± iσxy , n̄ = (n1 + n2 )/2, and c is the speed of light in
vacuum.
Pump-induced anisotropy of the transmission and reflection coefficients leads to the rotation of the linear polarization of the transmitted and reflected probe
fields. We will further consider the low-intensity regime,
when the pump-induced off-diagonal conductivity is much
smaller then the diagonal one, i.e. |σxy | ≪ |σxx |, and
σxx ≈ σ. In that case the differences t+ − t− and r+ − r+
are much smaller than the corresponding sums, and the
Faraday rotation angle θF and the ellipticity ϵF of the
transmitted probe field are [7, 37, 38]
ϵF − iθF ≈

t+ − t−
.
t+ + t−

(3)

Analogously, the Kerr rotation angle θK and the accompanying ellipticity ϵK of the reflected probe field are given
by
ϵK − iθK ≈

r+ − r−
.
r+ + r−

(4)

By substituting Eq. (2) to Eqs. (3) and (4), we obtain
2πσxy
,
cn̄(1 + α)

(5)

2πt12 σxy
,
cn̄(1 + α)(r12 − α)

(6)

θF + iϵF ≈
and
θK + iϵK ≈

where α = 2πσ/(cn̄). Note that Eq. (6) is not valid when
the difference r12 − α is close to zero, since in this case the
condition |r+ − r− | ≪ |r+ + r− | does not hold. When, in
addition to a small ratio |σxy /σ|, the parameter α is also
small, i.e. |α| ≪ 1 and |α| ≪ |r12 |, it follows from Eqs. (5)
and (6), that the ratio of the Faraday and Kerr angles is
constant, θK /θF = t12 /r12 . On the other hand, in the
absence of dielectric contrast, when n1 = n2 = n̄, and
r12 = 0, t12 = 1, the frequency dependences of the Faraday and Kerr angles differ, i.e. θF ≈ 2πRe{σxy }/(cn̄),
while θK ≈ −2πRe{σxy /α}/(cn̄).
In a typical pump-probe experiment, see e.g. Ref. [39],
one measures the Faraday and Kerr rotation signals equal
to the difference between the intensities of the transmitted
(t)
(t)
(t)
(t)
and reflected beams, such as Iω,x′ −Iω,y′ and Iω,σ+ −Iω,σ− .
′ ′
Here, (x , y ) are the axes rotated by π/4 with respect to
the initial (x, y) frame, and σ± denotes right- and lefthand circular polarization. These signals are related to
the rotation angles and ellipticities as
(t)

(t)

Iω,x′ − Iω,y′ = 2θF T Iω ,

(t)

(t)

Iω,σ+ − Iω,σ− = 2ϵF T Iω , (7)

3
and
(r)

(r)

Iω,x′ − Iω,y′ = 2θK RIω ,

(r)

(r)

Iω,σ+ − Iω,σ− = 2ϵK RIω , (8)



∂f1Ω
∂f1ω
− i(ω + Ω)f2,ω+Ω + e Eω ·
+ EΩ ·
∂p
∂p
= St f2,ω+Ω , (12c)

where
T =

n2 |t̄|2
,
n1

R = |r̄|2 ,

(9)

t̄ = (t+ +t− )/2, r̄ = (r+ +r− )/2, and Iω is the intensity of
the incident probe field. Note that the dielectric contrast
n1 ̸= n2 is crucial for the experimental observation of the
Kerr rotation signal, since the reflection coefficient R for
the free-standing 2D layer is proportional to the parameter
|α|2 , see Eq. (2), which might be small [39].
III.

PUMP-INDUCED TRANSVERSE
CONDUCTIVITY

Now, we develop a microscopic theory of the transverse
conductivity σxy (ω, Ω) induced by the circularly polarized pump field. The kinetics of 2D electrons driven by
the pump and probe electric fields is described by the
Boltzmann equation for the electron distribution function
f (p, t)
∂f
∂f
+ e [EΩ (t) + Eω (t)] ·
= Stf .
∂t
∂p

(10)

Here, p is the electron momentum, e is the electron charge
and Stf is the collision integral. The fields EΩ (t) and
Eω (t) in Eq. (10) are electric fields experienced by the
2DEG, i.e. the sum of the incident and reflected fields
at z = 0. Equation (10) is valid in the classical regime,
when ℏω and ℏΩ are much less than the mean electron
energy. We solve Eq. (10) by expanding the distribution
function f (p, t) in the series in the electric field amplitude
as follows:

− iωf3,ω + eEω ·

∂f2,ω−Ω
∂f2
+ eEΩ ·
∂p
∂p
∗ ∂f2,ω+Ω
= St f3,ω . (12d)
+ eEΩ
·
∂p

Equation for f1Ω is obtained from Eq. (12a) by replacing ω
with Ω, and equation for f2,ω−Ω is obtained from Eq. (12c)
by replacing Ω with −Ω and making use of the relations
∗
∗
E−Ω = EΩ
, f1,−Ω = f1Ω
.
In order to derive the σyx component of the conductivity
tensor, we calculate the transverse electric current jω,y =
σyx Eω,x driven by the x-component of the probe field.
The current reads
X
jω,y = eν
vy f3,ω ,
(13)
p

where ν is the factor of spin and valley degeneracy. Multiplying Eq. (12d) by vy and averaging the result over the
directions of p, we obtain

 
∂f2
∂f2,ω−Ω
⟨vy f3,ω ⟩ = −eτ1ω vy Eω ·
+ EΩ ·
∂p
∂p


∗ ∂f2,ω+Ω
− eτ1ω vy EΩ
, (14)
·
∂p
where ⟨. . .⟩ denotes averaging over the directions of p,
τ1ω = τ1 /(1 − iωτ1 ), and τ1−1 = − ⟨vStf ⟩ / ⟨vf ⟩ is the
energy-dependent momentum relaxation rate. Summation of Eq. (14) over p and integration by parts yield
jω,y = e2 ν

X

∗
(f2 Eω + f2,ω−Ω EΩ + f2,ω+Ω EΩ
)·

p



f (p, t) = f0 + f1ω (p)e−iωt + f1Ω (p)e−iΩt + c.c.
h
i
+f2 (p)+ f2,ω+Ω (p)e−i(ω+Ω)t + f2,ω−Ω (p)e−i(ω−Ω)t + c.c.


+ f3,ω (p)e−iωt + c.c. . (11)
Here, f0 is the equilibrium distribution function, whereas
the first-order corrections f1ω ∝ Eω and f1Ω ∝ EΩ determine Drude conductivity, responsible for ac electric currents oscillating at frequencies ω and Ω, respectively. The
∗
second-order corrections are f2 ∝ EΩ EΩ
, f2,ω+Ω ∝ Eω EΩ
∗
and f2,ω−Ω ∝ Eω EΩ . The desired transverse current oscillating at ω is determined by the third-order correction
∗
f3,ω ∝ Eω EΩ EΩ
.
Considering the term e [EΩ (t) + Eω (t)] · ∂f /∂p in
Eq. (10) as a perturbation we obtain the following equations for the corrections to the distribution function:
∂f0
= St f1ω ,
∂p

(12a)



∂f ∗
∗ ∂f1Ω
e EΩ · 1Ω + EΩ
·
= St f2 ,
∂p
∂p

(12b)

−iωf1ω + eEω ·

∂(vy τ1ω )
.
∂p

(15)
We start with calculating jω,y for parabolic energy dispersion of electrons ε(p) = |p|2 /2m. This dispersion is
typical for low-energy electrons in III-V quantum wells,
bilayer graphene, monolayers of transition metal dichalcogenides, etc. Calculating derivative in the right-hand side
of Eq. (15), one obtains
jω,y = e2 νEω,x

X

′
vx vy τ1ω
f2

p
2


e νX
∗
+
(ετ1ω )′ f2,ω−Ω EΩ,y + f2,ω+Ω EΩ,y
m p
+


e2 ν X ′ 
τ1ω f2,ω−Ω 2vx vy EΩ,x − (vx2 − vy2 )EΩ,y
2 p

∗
∗
+f2,ω+Ω 2vx vy EΩ,x
− (vx2 − vy2 )EΩ,y
. (16)

Here, (. . . )′ denotes derivative over energy, and we took
into account that Eω ∥ x. The nature of the contributions to the ac current Eq. (16) is similar to the one discussed in Ref. [32] for a static current. The first and the
third contributions, proportional to vx vy f2 , vx vy f2,ω±Ω

4
and (vx2 − vy2 )f2,ω±Ω , are related to the optical alignment
of electron momenta by the oscillating electric field. The
second term, proportional to (ετ1ω )′ , is related to the dynamic heating and cooling of 2DEG by the oscillating
fields.
The first-order corrections to the distribution function
are found from Eq. (12a) and read
f1ω = −eτ1ω (Eω · v)f0′ ,

f1Ω = −eτ1Ω (EΩ · v)f0′ , (17)

where τ1Ω = τ1 /(1−iΩτ1 ). Calculation shows that the first
term in Eq. (16) proportional to the time-independent correction f2 vanishes for circularly polarized pump. Therefore, we do not consider this term in the following. Other
second-order corrections are found by solving Eq. (12c)
with f1ω and f1Ω given by Eq. (17), which yields
1
′
f2,ω+Ω = ⟨f2,ω+Ω ⟩ + e2 Eω,x τ2,ω+Ω [(τ1Ω + τ1ω )f0′ ]
2


× (vx2 − vy2 )EΩ,x + 2vx vy EΩ,y . (18)
Here, ⟨f2,ω+Ω ⟩ is the zeroth angular harmonic of f2,ω+Ω ,
τ2−1 = − ⟨vx vy Stf ⟩ / ⟨vx vy f ⟩ is the energy-dependent relaxation rate of the second angular harmonic of the distribution function, and τ2,ω+Ω = τ2 /[1 − i(ω + Ω)τ2 ].
We describe the relaxation of the zeroth angular harmonic of the distribution function ⟨f (p, t)⟩ by the collision
integral St ⟨f ⟩ = −(⟨f ⟩ − f0 )/τ0 , where τ0 is the energyindependent relaxation time determined by the electronelectron scattering and energy-relaxation processes (e.g.,
caused by phonon scattering). Equation (12c) yields
⟨f2,ω+Ω ⟩ =

e2 τ0,ω+Ω
′
[ε(τ1Ω + τ1ω )f0′ ] Eω,x EΩ,x ,
m

(19)

where τ0,ω+Ω = τ0 /[1 − i(ω + Ω)τ0 ]. The f2,ω−Ω function
is found from f2,ω+Ω by replacing Ω with −Ω and using
∗
∗
the relations τ1,−Ω = τ1Ω
and E−Ω = EΩ
.
Finally, substituting Eqs. (18) and (19) into Eq. (16) for
the current and calculating the sums, we obtain the transverse conductivity of the degenerate electron gas induced
by the circularly polarized pump
σxy (ω, Ω) = F (ω, Ω) − F (ω, −Ω) ,

(20)

where for parabolic spectrum
iσe2 |EΩ |2 Pcirc [2 − i(ω + Ω)τ1 ]
(21)
2m(1 − iΩτ1 )
′′
′
′
′
× [(εF τ1ω
+ 2τ1ω
)τ0,ω+Ω − εF (τ1ω
τ2,ω+Ω )′ − 2τ1ω
τ2,ω+Ω ] .

σxy given by Eq. (20) with
iσe2 v02 |EΩ |2 Pcirc [2 − i(ω + Ω)τ1 ]
F (lin) (ω, Ω) = −
4εF (1 − iΩτ1 )


τ1ω
′′
′
′
× εF τ1ω
+ τ1ω
−
τ0,ω+Ω − εF (τ1ω
τ2,ω+Ω )′
εF


τ2,ω+Ω
′
′
−τ1ω
τ2,ω+Ω + τ1ω τ2,ω+Ω
+
.
(22)
εF
Here, the high-frequency conductivity and the electron
density are given by σ = e2 v02 ne τ1ω /εF and ne =
νε2F /(4πℏ2 v02 ).
Note that at ω = 0, Eqs. (20 – 22) describe the static
transverse photoconductivity of 2DEG and agree with the
second line of Eq. (16) in Ref. [32]. Conductivity given by
Eqs. (21) and (22) is proportional to |EΩ |2 , which is the
square of the pump field at z = 0. |EΩ |2 is related to
(i)
the intensity of the incident pump IΩ = cn1 [EΩ ]2 /2π as
2
|EΩ | = 2πT (Ω)IΩ /(cn2 ), where T is given by Eq. (9).

IV.

DISCUSSION

Equations (5), (6) and (20 – 22) can be applied to
calculate the photoinduced Faraday and Kerr rotation
and ellipticity in different 2D systems, such as quantum
wells, monolayer and bilayer graphene, transition metal
dichalcogenide monolayers and other doped 2D materials.
In this section we present results for two illustrative examples with linear and parabolic energy dispersion, monolayer and bilayer graphene, respectively. We also analyze
the role of the dielectric contrast (n2 − n1 )/n̄ between the
two dielectric media surrounding 2DEG on the rotation
angles and ellipticities.

A.

2D layer on a substrate

First, we consider the case of the 2D layer lying on
a substrate by setting the refractive indices n1 = 1 and
n2 = 3. In the discussion below Eq. (6), we showed that in
case of a large dielectric contrast, the Kerr angle and ellipticity are related to the corresponding Faraday quantities
as θK /θF ≈ t12 /r12 , and ϵK /ϵF ≈ t12 /r12 . Hence, for
the chosen n1 and n2 we have θK ≈ −θF and ϵK ≈ −ϵF ,
and in this subsection we discuss the Faraday angle and
ellipticity only [40].

F (par) (ω, Ω) = −

Here, the relaxation times and its energy derivatives are
taken at the Fermi energy εF , σ = e2 ne τ1ω /m is the
high-frequency conductivity, and ne = νmεF /(2πℏ2 ) is
the electron density.
Similar calculations can be applied to 2DEG with linear energy dispersion, e.g. in graphene or HgTe/CdHgTe
quantum wells of the critical thickness. Using ε(p) = v0 |p|
and performing calculations shown in App. A, one obtains

1.

Parabolic spectrum. Bilayer graphene.

Figure 2 shows the dependence of the calculated Faraday angle and the accompanying ellipticity for parabolic
energy dispersion and a set of parameters relevant to bilayer graphene [41]. It follows from Eq. (21) that in case
of the energy independent relaxation times τ1 and τ2 , relevant for short-range scatterers, the transverse conductivity σxy vanishes. Hence, the curves in Fig. (2) are plotted for unscreened Coulomb scatterers corresponding to
τ1 = 2τ2 ∝ ε. We use the electron density ne = 1012 cm−2

5

✓F

0.1

⌦⌧1 = 1

0

−0.1
−0.2

⌦⌧1 = 0.5
0
0.5
1.0
Probe frequency (ωτ1)

(b)
0.4

✏F

0.2

0

0
0.5
1.0
Probe frequency (ωτ1)

FIG. 2. (a) Photoinduced Faraday rotation angle θF and (b)
the accompanying ellipticity ϵF of the two-dimensional electron gas with parabolic spectrum for a large dielectric contrast between the surrounding media. Three curves correspond
to three values of the pump frequency: Ωτ1 = 0.1, 0.5, 1.
Sharp resonances at ω ≈ Ω occur. The curves are calculated
after Eqs. (5), (20) and (21) for the following parameters:
τ1 (εF ) = 0.1 ps, ne = 1012 cm−2 , τ0 = 5 ps, m = 0.03m0 ,
τ1 = 2τ2 ∝ ε (Coulomb scatterers), IΩ = 1 kW/cm2 , n1 = 1,
n2 = 3 and Pcirc = 1.

The dependence of rotation angles and ellipticities on
the probe frequency experiences sharp resonances in the
region, where the probe frequency ω is close to the
pump frequency Ω. At Ωτ1 ≲ 1 and pump intensity
IΩ = 1 kW/cm2 , the Faraday angle at the resonance is
θF ∼ 0.1◦ , and the corresponding ellipticity ϵF ∼ 0.1 %,
see Fig. 2. Note that for such intensity, the inequality
|σxy | ≪ |σxx | still holds so that we are still in the perturbative regime. To study the shape of the resonances
in more detail, we analyze the pump-induced conductivity, Eqs. (20 – 21), at τ0 ≫ τ1 relevant for 2DEG at low
temperature, and Ωτ0 ≫ 1. In this case we have a sharp
resonance in the conductivity, which shape for Coulomb
scatterers is given by
2iσ0 e2 τ1 τ0 |EΩ |2 Pcirc
.
mεF [1 − i(ω − Ω)τ0 ](1 + Ω2 τ12 )(1 − iΩτ1 )3
(23)
Equation (23) allows one to calculate the frequency dependence of the Faraday angle near the resonance. Substituting Eq. (23) to Eq. (5), one obtains
σxy (ω) ≈

4πσ0 e2 τ1 τ0 |EΩ |2 Pcirc
cn̄
mεF
2 2
Ωτ1 (Ω τ1 − 3) + (ω − Ω)τ0 (3Ω2 τ12 − 1)
×
. (24)
(1 + Ω2 τ12 )4 [1 + (ω − Ω)2 τ02 ]

θF (ω) ≈

It follows from Eq. (24), that depending on Ωτ1 , the resonance shape varies between Lorentzian and Lorentzian
multiplied by (ω − Ω), see Fig. 2a. Interestingly, the resonance width is given by the relaxation rate of the zeroth

2.

Linear spectrum. Single-layer graphene.

Figure 3 shows the dependence of the calculated Faraday angle and the accompanying ellipticity for linear energy dispersion and a set of parameters relevant to monolayer graphene [42]. For linear energy dispersion, the relaxation times are τ1 = 2τ2 ∝ ε−1 for short-range scatterers and τ1 = 3τ2 ∝ ε for Coulomb scatterers [31]. It follows from Eq. (22) that both types of scatterers contribute
to the transverse conductivity. For the calculations we use
ne = 3 × 1011 cm−2 and τ1 (εF ) = 0.1 ps, which results in
εF ≈ 64 meV and 2πσ0 /(cn̄) ≈ 0.071. In that case, the
transmission and reflection coefficients of the probe beam
lie in the range T = 0.65 − 0.71 and R = 0.26 − 0.28,
respectively.
(a) 0.05

(b)

⌦⌧1 = 0.1

✓F

0

⌦⌧1 = 1
−0.05

⌦⌧1 = 0.5
0
0.5
1.0
Probe frequency (ωτ1)

Faraday ellipticity (%)

Faraday angle (deg)

⌦⌧1 = 0.1

Faraday ellipticity (%)

(a)

angular harmonic τ0−1 rather than the momentum relaxation rate. The magnitude of the resonance is determined
by the product of 4πσ0 /(cn̄) and the dimensionless parameter e2 |EΩ |2 τ1 τ0 /(mεF ) proportional to the intensity
of the pump radiation.
We note, that strictly at resonance, when ω = Ω, the
developed theory is not applicable. In this case, one
should consider a third-order response to the monochromatic electric field, since the pump and probe fields cannot
longer be distinguished as in Eq. (1). This situation corresponds to the self-induced rotation of electric field, when
the field modifies dielectric properties of the 2D layer and,
at the same time, experience rotation due to this modification. Such a self-induced rotation has been considered for
graphene within a simplified relaxation model in Ref. [31].
In App. B, we calculate the third-order photocurrent induced by a monochromatic electric field being a sum of
large circularly polarized and small linearly polarized contributions, see Eq. (B8).

Faraday angle (deg)

and momentum relaxation time τ1 (εF ) = 0.1 ps, which
results in εF ≈ 39 meV and 2πσ0 /(cn̄) ≈ 0.088, where
σ0 = e2 ne τ1 /m is the static 2DEG conductivity. In
the studied frequency range the transmission and reflection coefficients (9) lie in the range T = 0.63 − 0.7 and
R = 0.27 − 0.29, respectively.

✏F
0

−0.05
−0.10
−0.15
0
0.5
1.0
Probe frequency (ωτ1)

FIG. 3. (a) Photoinduced Faraday rotation angle θF and (b)
accompanying ellipticity ϵF of the two-dimensional electron gas
with linear spectrum for a large dielectric contrast (n2 − n1 )/n̄
between the surrounding media. Three curves correspond to
three values of the pump frequency: Ωτ1 = 0.1, 0.5, 1. Sharp
resonances at ω ≈ Ω occur. The curves are calculated after
Eqs. (5), (20) and (22) for the following parameters: τ1 (εF ) =
0.1 ps, ne = 3 × 1011 cm−2 , τ0 = 5 ps, v0 = 108 cm/s, τ1 =
2τ2 ∝ ε−1 (short-range scatterers), IΩ = 1 kW/cm2 , n1 = 1,
n2 = 3 and Pcirc = 1.

As in the case of a bilayer graphene, the rotation an-

6

θF (ω) ≈
×

πσ0 e2 v02 τ1 τ0 |EΩ |2 Pcirc
cn̄
ε2F

Ωτ1 [Ω4 τ14 + 6Ω2 τ12 − 3 + 8Ωτ1 (ω − Ω)τ0 ]
. (26)
(1 + Ω2 τ12 )4 [1 + (ω − Ω)2 τ02 ]

The magnitude of the resonance is determined by the
product of πσ0 /(cn̄) and the dimensionless parameter e2 |EΩ |2 τ1 τ0 /(m∗ εF ) with the effective electron mass
m∗ = εF /v02 (m∗ ≈ 0.01 m0 in our calculations).
B.

Free-standing monolayer graphene

In this section we consider a free-standing 2D layer by
setting the refractive indices n1 = n2 = 1. In this case
r12 = 0, t12 = 1, and as shown below Eq. (6), the Faraday
and Kerr angles have different spectral dependences. Figure 4 shows the results of calculations for a free-standing
monolayer graphene. The values of the rotation angles
and ellipticities are larger for the free-standing layer than
for the layer on a substrate, Figs. 2 and 3, for two reasons.
First, the rotation angles and ellipticites are proportional
to 1/n̄, see Eqs. (5) and (6). Second, the pump field at
z = 0, |EΩ |2 = 2πT (Ω)IΩ /(cn2 ), is larger at a given pump
intensity. Moreover, the values of the Kerr angle and ellipticity are significantly larger than the corresponding Faraday values, since θF ∝ Re{σxy }, while θK ∝ Re{σxy /α}
at |α| ≪ 1. Note that, however, the experimentally measured Kerr rotation signals, see Eq. (8), are still small due
to the small reflection from the free-standing layer.
The calculated Faraday rotation angles for graphene
samples are ∼ 0.1◦ − 1◦ per 1 kW/cm2 of the pump intensity, see Figs. 2, 3 and 4. Similar values of the Faraday angles were measured in monolayer and multilayer graphene
in the terahertz and far-infrared frequency range at external magnetic field Bz ∼ 1 T in Refs. [42, 43]. The rotation
angles can be further increased in high-mobility 2DEG in
GaAs/AlGaAs quantum wells with larger values of τ1 , see,
e.g., Ref. [44].
C.

Synthetic magnetic field induced by pump

The action of the circularly polarized pump on 2DEG
can be described in terms of a synthetic magnetic field
Bsyn . This field equals to an external magnetic field,
which rotates the polarization plane by the same angle as
the pump. The Faraday angle in the presence of external
magnetic field is given by Eq. (5) with the Hall conductivity σxy (Bz ), which results in θF ∼ (ωc τ1 )2πσ0 /(cn̄), where

Rotation angle (deg)

σ0 e2 v02 (3 − iΩτ1 )Ωτ12 τ0 |EΩ |2 Pcirc
.
2ε2F [1 − i(ω − Ω)τ0 ](1 + Ω2 τ12 )(1 − iΩτ1 )3
(25)
Interestingly, Eq. (25) holds both for short-range and
Coulomb scatterers. Substituting Eq. (25) to Eq. (5), we
obtain for the Faraday angle near the resonance:
σxy (ω) ≈ −

(a)
0.2 ⌦⌧1 = 0.1

(b)
4

✓F

✓K

3
0

2

−0.2

⌦⌧1 = 1

−0.4

⌦⌧1 = 0.5
0

0.5

1
0
−1

1.0

(c)
Ellipticity (%)

gles and ellipticities in a single-layer graphene experience
sharp resonances at ω ≈ Ω. The photoconductivity σxy
in the vicinity of resonance has the form

✏F

0

0
(d)
6

0.5

1.0

✏K

4
−0.5

2
0

−1.0
0
0.5
1.0
Probe frequency (ωτ1)

−2

0
0.5
1.0
Probe frequency (ωτ1)

FIG. 4. (a, b) Photoinduced Faraday and Kerr rotation angles θF and θK and (c, d) the accompanying ellipticities ϵF
and ϵK of the two-dimensional electron gas in a free-standing
graphene. Three curves correspond to three values of the pump
frequency: Ωτ1 = 0.1, 0.5, 1. Sharp resonances at ω ≈ Ω occur. The curves are calculated after Eqs. (5), (6) and (22) for
the following parameters: τ1 (εF ) = 0.1 ps, ne = 3×1011 cm−2 ,
τ0 = 5 ps, v0 = 108 cm/s, τ1 = 2τ2 ∝ ε−1 (short-range scatterers), IΩ = 1 kW/cm2 , n1 = n2 = 1 and Pcirc = 1.

ωc = eBz /mc is the cyclotron frequency. By comparison
with Eqs. (24) and (26) at Ωτ1 ∼ 1, one can estimate the
synthetic magnetic field from ωc τ1 ∼ e2 |EΩ |2 τ1 τ0 /(mεF ),
which yields
Bsyn ∼

ec|EΩ |2 τ0
.
εF

(27)

Note that the value of Bsyn is quite universal, since it does
not depend on the electron mobility and energy dispersion.
It depends, however, on the energy relaxation time τ0 and,
hence, should increase with decreasing temperature.
Synthetic magnetic field induced by the pump with intensity IΩ = 1 kW/cm2 at εF = 50 meV and τ0 = 10 ps is
Bsyn ∼ 0.1 T. This value increases with the growth of radiation intensity and may reach 1 T for several kW/cm2 terahertz and far-infrared radiation, which is used for spectroscopy of electron gas in graphene [34, 35]. Note that
Bsyn is significantly (several orders of magnitude) larger
than the actual magnetic field induced by the orbital currents being the source of the inverse-Faraday magnetization [13, 41].
V.

SUMMARY

To summarize, we have studied theoretically the pumpprobe Faraday and Kerr rotation due to the orbital magnetization in the two-dimensional electron gas (2DEG).
We have shown that the circularly polarized electric field

7
of the terahertz-range pump results in the transverse conductivity σxy (ω, Ω) of 2DEG, which is proportional to the
pump intensity and depends on both the probe and pump
frequencies ω and Ω, respectively. This pump-induced
anisotropy of conductivity results in the circular birefringence and dichroism for a probe field. We have derived
analytical expressions for σxy (ω, Ω) and the corresponding
Faraday and Kerr rotation angles for parabolic and linear energy dispersion of 2D electrons and arbitrary scattering potential. We have shown that at ω ≈ Ω rotation angles are resonantly enhanced, reaching 0.1◦ − 1◦
for 1 kW/cm2 of the pump intensity in graphene samples
at Ωτ1 ∼ 1, where τ1 is the momentum relaxation time.
Similar values of the Faraday angles were measured in
monolayer and multilayer graphene in the terahertz and
far-infrared frequency range in an external magnetic field
Bz ∼ 1 T [42, 43]. The calculated Faraday and Kerr angles are governed by the momentum and energy relaxation
of 2D electrons, and hence, can elucidate mechanisms and
rates of electron relaxation processes in pump-probe experiments.

The f2,ω−Ω function is obtained from Eqs. (A2), (A3) by
∗
replacing Ω with −Ω and using the relations τ1,−Ω = τ1Ω
∗
and E−Ω = EΩ . Finally, substituting f2,ω±Ω given by
Eqs. (A2–A3) into Eq. (A1) for the current and calculating
the sums we obtain Eqs. (20) and (22) of the main text.

Appendix B: Transverse photoconductivity at
coinciding pump and probe frequencies

In this section, we calculate third-order response similar
to Eq. (1) but at coinciding pump and probe frequencies,
ω = Ω. Electric field at the 2DEG plane E(t) = Ee−iωt +
c.c. is a sum of large circularly polarized (pump) and small
linearly polarized (probe) contributions:
E1
Ex = √ + E2 ,
2

√
Ey = iPcirc E1 / 2 ,

(B1)

where Pcirc = ±1 and E2 ≪ E1 .
We search the electron distribution function f (p, t) in
the form

ACKNOWLEDGMENTS

The author thanks S. A. Tarasenko and M. M. Glazov
for fruitful discussions. The work was supported by the
Russian Science Foundation (Project No. 21-72-00047).
Appendix A: Transverse photoconductivity of 2DEG
with linear energy spectrum

Here, we calculate pump-induced transverse conductivity for electrons with linear energy dispersion ε = v0 p.
We start with the general equation for the current (15).
Calculating derivative on the right-hand side of Eq. (15)
one obtains
 τ ′
X
1ω
jω,y = e2 νEω,x
vx vy ε
f2
ε
p

e2 v02 ν X (ετ1ω )′
∗
f2,ω−Ω EΩ,y + f2,ω+Ω EΩ,y
2
ε
p

e2 ν X  τ1ω ′ 
+
ε
f2,ω−Ω 2vx vy EΩ,x − (vx2 − vy2 )EΩ,y
2 p
ε

∗
∗
+f2,ω+Ω 2vx vy EΩ,x
− (vx2 − vy2 )EΩ,y
. (A1)
+

The first contribution in Eq. (A1) proportional to f2 vanishes for circularly polarized pump. The first-order corrections to the distribution function coincide with the ones
given by Eq. (17), whereas the second-order correction
f2,ω+Ω has the form

′
e2 Eω,x
(τ1Ω + τ1ω )f0′
f2,ω+Ω = ⟨f2,ω+Ω ⟩ +
τ2,ω+Ω ε
2
ε
 2

2
× (vx − vy )EΩ,x + 2vx vy EΩ,y , (A2)
where
⟨f2,ω+Ω ⟩ =

e2 v02 τ0,ω+Ω
′
[ε(τ1ω + τ1Ω )f0′ ] Eω,x EΩ,x . (A3)
2ε



f (t) = f0 + f1 (p)e−iωt + c.c. + f2 (p)
h
i 

+ f˜2 (p)e−2iωt + c.c. + f3 (p)e−iωt + c.c. , (B2)
where corrections to the distribution function satisfy the
following equations
∂f0
= St f1 ,
∂p


∂f ∗
∂f1
e E · 1 + E∗ ·
= St f2 ,
∂p
∂p
∂f1
−2iω f˜2 + eE ·
= St f˜2 ,
∂p
∂ f˜2
∂f2
+ eE ∗ ·
= St f3 .
−iωf3 + eE ·
∂p
∂p
−iωf1 + eE ·

(B3a)
(B3b)
(B3c)
(B3d)

The transverse electric current is determined by the
third-order correction f3 and reads
jω,y = e

X

vy f3 = e2

p

X
p

 ∂(v τ )
y 1ω
f2 E + f˜2 E ∗ ·
.
∂p

(B4)
Taking derivative in the right-hand side for the case of
linear dispersion and simplifying, we obtain

ε  τ1ω ′
+
f2 Ey
ε
2 ε
p

e2 X  τ1ω ′ 
+
ε
f2 2vx vy Ex − (vx2 − vy2 )Ey
2 p
ε

X  τ1ω
ε  τ1ω ′ ˜ ∗
+ e2 v02
+
f2 Ey
ε
2 ε
p

e2 X  τ1ω ′ ˜ 
+
ε
f2 2vx vy Ex∗ − (vx2 − vy2 )Ey∗ . (B5)
2 p
ε

jω,y = e2 v02

X  τ1ω

8
By solving Eqs. (B3b) and (B3c) with the use of
Eq. (17), we obtain
2

( 

f2 = e τ2 Re ε

τ1ω f0′
ε

′ )

 2

(vx − vy2 )S1 + 2vx vy S2

+ e2 v02 τ0 S0 Re



(ετ1ω f0′ )′
ε

(B1) in Eq. (B5) for the current, performing summation
over p and simplifying, we finally obtain


iσe2 v02 Pcirc E12 E2
2τ0
− τ0,2ω A
εF
1 + iωτ1


τ2 A + εF τ2′ B
3
′
−
+
τ2,2ω A + εF τ2,2ω
B
, (B8)
1 + iωτ1
2

jω,y = −


, (B6)
where

and
2

e τ2,2ω
ε
f˜2 =
2



τ1ω f0′
ε

′

 2

(vx − vy2 )s1 + 2vx vy s2
e2 v02 τ0,2ω s0
(ετ1ω f0′ )′ . (B7)
2ε

′′
′
A = εF τ1ω
+ τ1ω
−

τ1ω
,
εF

′
B = τ1ω
−

τ1ω
.
εF

(B9)

Here, S0 = |E|2 , S1 = |Ex |2 − |Ey |2 , S2 = Ex Ey∗ + Ex∗ Ey
are the Stokes parameters, and s0 = Ex2 + Ey2 , s1 = Ex2 −
Ey2 , s2 = 2Ex Ey . By substituting Eqs. (B6), (B7) and

Here, we only left contributions to the current proportional to E12 E2 .
Note that, for a simplified relaxation model with relaxation times τ0 = τ1 = τ2 and independent of energy,
the current given by Eq. (B8) coincides with Eq. (69) of
Ref. [31].

[1] A. Kirilyuk, A. V. Kimel, and T. Rasing, Ultrafast optical
manipulation of magnetic order, Rev. Mod. Phys. 82, 2731
(2010).
[2] A. Stupakiewicz, K. Szerenos, D. Afanasiev, A. Kirilyuk, and A. V. Kimel, Ultrafast nonthermal photomagnetic recording in a transparent medium, Nature 542,
71 (2017).
[3] Z. Chai, X. Hu, F. Wang, X. Niu, J. Xie, and Q. Gong, Ultrafast all-optical switching, Adv. Opt. Mater. 5, 1600665
(2017).
[4] O. H.-C. Cheng, D. H. Son, and M. Sheldon, Lightinduced magnetism in plasmonic gold nanoparticles, Nat.
Photonics 14, 365 (2020).
[5] M. I. Dyakonov, ed., Spin physics in semiconductors
(Springer-Verlag: Berlin, Heidelberg, 2008).
[6] Y. Kusrayev and G. Landwehr, Optical orientation, Semicond. Sci. Technol. 23, 110301 (2008).
[7] M. M. Glazov, Coherent spin dynamics of electrons and
excitons in nanostructures (a review), Phys. Solid State
54, 1 (2012).
[8] S. D. Ganichev, E. L. Ivchenko, V. V. Bel’kov, S. A.
Tarasenko, M. Sollinger, D. Weiss, W. Wegscheider, and
W. Prettl, Spin-galvanic effect, Nature 417, 153 (2002).
[9] E. L. Ivchenko and S. A. Tarasenko, Monopolar optical
orientation of electron spins in bulk semiconductors and
heterostructures, J. Exp. Theor. Phys. 99, 379 (2004).
[10] B. N. Murdin, K. Litvinenko, D. G. Clarke, C. R. Pidgeon, P. Murzyn, P. J. Phillips, D. Carder, G. Berden,
B. Redlich, A. F. G. van der Meer, S. Clowes, J. J. Harris,
L. F. Cohen, T. Ashley, and L. Buckle, Spin relaxation
by transient monopolar and bipolar optical orientation,
Phys. Rev. Lett. 96, 096603 (2006).
[11] L. P. Pitaevskii, Electric forces in a transparent dispersive
medium, Sov. Phys. JETP 12, 1008 (1961).
[12] J. P. van der Ziel, P. S. Pershan, and L. D. Malmstrom,
Optically-induced magnetization resulting from the inverse Faraday effect, Phys. Rev. Lett. 15, 190 (1965).
[13] R. Hertel, Theory of the inverse Faraday effect in metals,
J. Magn. Magn. Mater. 303, L1 (2006).
[14] M. Battiato, G. Barbalinardo, and P. M. Oppeneer,
Quantum theory of the inverse Faraday effect, Phys. Rev.
B 89, 014413 (2014).

[15] M. Berritta, R. Mondal, K. Carva, and P. M. Oppeneer,
Ab initio theory of coherent laser-induced magnetization
in metals, Phys. Rev. Lett. 117, 137203 (2016).
[16] I. I. Ryzhov, G. G. Kozlov, D. S. Smirnov, M. M. Glazov,
Y. P. Efimov, S. A. Eliseev, V. A. Lovtcius, V. V. Petrov,
K. V. Kavokin, A. V. Kavokin, and V. S. Zapasskii, Spin
noise explores local magnetic fields in a semiconductor,
Sci. Rep. 6, 21062 (2016).
[17] A. V. Kimel, A. Kirilyuk, P. A. Usachev, R. V. Pisarev,
A. M. Balbashov, and T. Rasing, Ultrafast non-thermal
control of magnetization by instantaneous photomagnetic
pulses, Nature 435, 655 (2005).
[18] S. V. Mironov, A. S. Mel’nikov, I. D. Tokman, V. Vadimov, B. Lounis, and A. I. Buzdin, Inverse Faraday effect
for superconducting condensates, Phys. Rev. Lett. 126,
137002 (2021).
[19] J. Hurst, P. M. Oppeneer, G. Manfredi, and P.-A.
Hervieux, Magnetic moment generation in small gold
nanoparticles via the plasmonic inverse Faraday effect,
Phys. Rev. B 98, 134439 (2018).
[20] I. D. Tokman, Q. Chen, I. A. Shereshevsky, V. I. Pozdnyakova, I. Oladyshkin, M. Tokman, and A. Belyanin,
Inverse Faraday effect in graphene and Weyl semimetals,
Phys. Rev. B 101, 174429 (2020).
[21] D. D. Awschalom, J. M. Halbout, S. von Molnar,
T. Siegrist, and F. Holtzberg, Dynamic spin organization in dilute magnetic systems, Phys. Rev. Lett. 55, 1128
(1985).
[22] N. Zheludev, M. Brummell, R. Harley, A. Malinowski,
S. Popov, D. Ashenford, and B. Lunn, Giant specular
inverse Faraday effect in Cd0.6Mn0.4Te, Solid State Commun. 89, 823 (1994).
[23] Y. K. Kato, R. C. Myers, A. C. Gossard, and D. D.
Awschalom, Observation of the spin Hall effect in semiconductors, Science 306, 1910 (2004).
[24] S. A. Crooker and D. L. Smith, Imaging spin flows in
semiconductors subject to electric, magnetic, and strain
fields, Phys. Rev. Lett. 94, 236601 (2005).
[25] A. Greilich, D. R. Yakovlev, A. Shabaev, A. L. Efros, I. A.
Yugova, R. Oulton, V. Stavarache, D. Reuter, A. Wieck,
and M. Bayer, Mode locking of electron spin coherences
in singly charged quantum dots, Science 313, 341 (2006).

+

9
[26] M. M. Glazov, I. A. Yugova, S. Spatzek, A. Schwan,
S. Varwig, D. R. Yakovlev, D. Reuter, A. D. Wieck, and
M. Bayer, Effect of pump-probe detuning on the Faraday rotation and ellipticity signals of mode-locked spins in
(In,Ga)As/GaAs quantum dots, Phys. Rev. B 82, 155325
(2010).
[27] F. Passmann, S. Anghel, T. Tischler, A. V. Poshakinskiy,
S. A. Tarasenko, G. Karczewski, T. Wojtowicz, A. D. Bristow, and M. Betz, Persistent spin helix manipulation by
optical doping of a CdTe quantum well, Phys. Rev. B 97,
201413 (2018).
[28] A. G. Aronov and E. L. Ivchenko, Dichroism and optical
anisotropy of media with oriented spins of free electrons,
Sov. Phys. Solid State 15, 160 (1973).
[29] Y. P. Svirko and N. I. Zheludev, Coherent and incoherent
pump–probe specular inverse Faraday effect in media with
instantaneous nonlinearity, J. Opt. Soc. Am. B 11, 1388
(1994).
[30] I. A. Yugova, M. M. Glazov, E. L. Ivchenko, and A. L.
Efros, Pump-probe Faraday rotation and ellipticity in an
ensemble of singly charged quantum dots, Phys. Rev. B
80, 104436 (2009).
[31] M. Glazov and S. Ganichev, High frequency electric field
induced nonlinear effects in graphene, Phys. Rep. 535, 101
(2014).
[32] M. V. Durnev, Photovoltaic hall effect in the twodimensional electron gas: Kinetic theory, Phys. Rev. B
104, 085306 (2021).
[33] Linearly polarized pump causes linear birefringence and
dichroism of 2DEG, which manifests itself in different
transmission, reflection and absorption of the probe field
polarized parallel and perpendicular to the pump field.
[34] J. W. McIver, B. Schulte, F. U. Stein, T. Matsuyama,
G. Jotzu, G. Meier, and A. Cavalleri, Light-induced
anomalous Hall effect in graphene, Nature Phys. 16, 38
(2020).
[35] S. Candussio, S. Bernreuter, T. Rockinger, K. Watanabe,
T. Taniguchi, J. Eroms, I. A. Dmitriev, D. Weiss, and

S. D. Ganichev, Terahertz radiation induced circular Hall
effect in graphene, Phys. Rev. B 105, 155416 (2022).
[36] K. Chiu, T. Lee, and J. Quinn, Infrared magnetotransmittance of a two-dimensional electron gas, Surf. Sci.
58, 182 (1976).
[37] E. D. Palik and J. K. Furdyna, Infrared and microwave
magnetoplasma effects in semiconductors, Rep. Prog.
Phys. 33, 1193 (1970).
[38] R. F. O’Connell and G. Wallace, Ellipticity and Faraday rotation due to a two-dimensional electron gas in a
metal-oxide-semiconductor system, Phys. Rev. B 26, 2231
(1982).
[39] E. A. Zhukov, D. R. Yakovlev, M. Bayer, M. M. Glazov,
E. L. Ivchenko, G. Karczewski, T. Wojtowicz, and J. Kossut, Spin coherence of a two-dimensional electron gas induced by resonant excitation of trions and excitons in
CdTe/CdMgTe quantum wells, Phys. Rev. B 76, 205310
(2007).
[40] We assume that n1,2 are frequency-independent in the
considered frequency range.
[41] S. Candussio, M. V. Durnev, S. A. Tarasenko, J. Yin,
J. Keil, Y. Yang, S.-K. Son, A. Mishchenko, H. Plank,
V. V. Bel’kov, S. Slizovskiy, V. Fal’ko, and S. D.
Ganichev, Edge photocurrent driven by terahertz electric
field in bilayer graphene, Phys. Rev. B 102, 045406 (2020).
[42] R. Shimano, G. Yumoto, J. Y. Yoo, R. Matsunaga, S. Tanabe, H. Hibino, T. Morimoto, and H. Aoki, Quantum
Faraday and Kerr rotations in graphene, Nature Commun.
4, 1841 (2013).
[43] I. Crassee, J. Levallois, A. L. Walter, M. Ostler, A. Bostwick, E. Rotenberg, T. Seyller, D. van der Marel, and
A. B. Kuzmenko, Giant Faraday rotation in single- and
multilayer graphene, Nature Phys. 7, 48 (2011).
[44] V. Suresh, E. Pinsolle, C. Lupien, T. J. Martz-Oberlander,
M. P. Lilly, J. L. Reno, G. Gervais, T. Szkopek, and
B. Reulet, Quantitative measurement of giant and quantized microwave Faraday rotation, Phys. Rev. B 102,
085302 (2020).

```
