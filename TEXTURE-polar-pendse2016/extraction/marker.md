<!-- extracted via pdftotext | arxiv:1602.05303 | 2026-07-19T04:40:35Z -->
Effect of non-local interactions on the vortex solution in Bose-Einstein Condensates
Abhijit Pendse∗ and A. Bhattacharyay†

arXiv:1602.05303v8 [cond-mat.quant-gas] 28 Oct 2017

Department of Physics, Indian Institute of Science Education and Research, Pune, Maharashtra 411008, India.
(Dated: June 15, 2022)
We consider the Gross-Pitaevskii (GP) model of a Bose-Einstein Condensate (BEC) to study a
single vortex line in the presence of non-local repulsive s-wave scattering. We show that in addition
to the vortex solution with core width of the order of the healing length, there exists a vortex
solution whose width is a microscopic length scale of the order of s-wave scattering length and is
independent of the healing length. We compare the two classes of vortex solution and show the
region where one can possibly observe the vortex whose width is of the order of scattering length.
PACS numbers: 03.75.Lm, 03.75.Kk

I.

INTRODUCTION

Healing length of a Bose-Einstein Condensate (BEC)
is the distance from a hard-wall boundary at which a
BEC heals to its ground state uniform density. There
exists selection of this length scale (healing length ξ0 ) via
an exact solution of the full non-linear Gross-Pitaevskii
(GP) equation in one dimension (1D)[1, 2]. Note that,
a vortex neither involves a hard boundary nor is it a
structure in 1D. Due to these reasons one might expect
to get another length scale for the size of a vortex core
apart from the healing length when a non-local correction
to the local GP equation is present.
The conventional vortex solution of core size ξ0 is in
general arrived at within the realm of a local GP equation where one takes into account contact interactions
between bosons. The three body interactions are suppressed in an atomic BEC by working in the diluteness
1
limit a << n− 3 . Even in a dilute condensate, however,
if one has to probe a vortex line with a core so thin that
the Lindemann criterion works[3, 4], one actually probes
a length scale of the order of scattering length a. In this
situation the interaction cannot be treated as a contact
interaction and one should take corrections for the nonlocality of interactions.
In this paper we take into account the leading order
non-local interaction correction on top of the local GP
dynamics to study here a single vortex in an open condensate. In this procedure of considering corrections to
the local GP dynamics we use first a standard correction
term as employed to the local GP equation considering
the microscopics of the non-local nature of inter-atomic
interactions in the references[5, 6] and then propose a
generalization using a Taylor expansion of the interaction
term. We compare the energy of this new class of vortices with the conventional ones and propose a possible
way to experimentally realize this new class of vortices
which has core-size of the order of scattering length.
The non-locality of interactions induced vortices of
core-size of the order of scattering length (thin vortex)
∗ abhijeet.pendse@students.iiserpune.ac.in
† a.bhattacharyay@iiserpune.ac.in

which we show in the present paper are obviously of
higher energy than the vortices of core-size of the order
of healing length (thick vortex). Therefore, the class of
the thin vortices, we capture here in the presence of nonlocal corrections, can only show up in a situation where
the thick vortex solution breaks down. It is well known
that the thick vortex solution which is arrived at variationally on the basis of an approximate form of solution
(so called Padé approximation) exists for ξ0 << D where
D is a large distance cut off employed in the variational
calculations in order to manage the logarithmic divergence of energy of the vortex. In this paper we also give
a plausibility argument as to how to reach the ξ0 ∼ D
limit in a realistic situation where the conventional thick
vortex solution would break down and one might experimentally capture the thin vortex solution that we obtain.
Such a scenario, if exists, can possibly result in vortex
lattice melting which is of immense importance in the
context of atomic quantum Hall effect which is yet to be
experimentally realized[7–12].
The paper is organized in the following way. We first
discuss the well-known thick vortex solution using the
standard procedure in the dilute limit of the GP equation
and show that for the existence of this solution, or for the
demand of the variational method that captures this solution, the size of the core of this solution is ξ0 << D. The
variational method will break down for ξ0 ≃ D. Then
we show that taking the leading order correction for nonlocal interactions on top of the GP dynamics at the dilute
limit does even not help this same class of solution survive in the regime ξ0 ≃ D. This is something important
to check because the non-local correction actually introduces a competing length scale in the dynamics which
is of the order of the s-wave scattering length a and one
would expect to get a solution here reflecting this length
scale. We capture this solution (thin vortex) using similar variational method in the following section using a
model already in literature which provides standard leading order non-local correction to GP equation. We show
that, unlike the thick vortices, the existence of this new
class of solution does not depend on the radial cut off D
and, therefore, can exist in the regime ξ0 ≃ D where the
thick vortex solution breaks down. We then generalize
results to vortices of any quantum of circulation which

2
is followed by a detailed discussion of our results in the
context of possibility of vortex lattice melting using such
thin vortices.
II.

STANDARD THEORY

Let us look at how [1] one gets a standard vortex solution in local GP model. It would be explicitly shown
that the length scale selection is applicable only when
D >> ξ0 , where D is the radial cut off which is roughly
the lateral extent allowed to a single vortex. A radial cut
off for a vortex energy calculation is essential because the
energy of the vortex increases logarithmically with its radial spread. This crucial condition shall be utilized, in
what follows, for showing a comparison between the two
classes of vortex solutions. The theory that is shown in
this section is quite standard and well known, except for
the part presented in subsection C.
A.

Solution from GP dynamics

The local Gross-Pitaevskii (GP) equation at dilute
limit a << n−1/3 , where n is density of the condensate,
is given by

i~

~2 2
∂ψ0 (r, t) 
= −
∇ + Vext (r, t)
∂t
2m
+ g |ψ0 (r, t)|

2



(1)
ψ0 (r, t).

Here ψ0 (r, t) is the BEC order parameter.The particles
of BEC interact here via contact interactions (δ−function
interaction potential). Vext (r, t) is the external trapping
potential applied to the BEC. |ψ0 (r, t)|2 is the density n
of the BEC. Taking the ansatz ψ0 (r, t) = ψ0 (r)e−iµt/~ in
presence of a time-independent external potential, where
µ is the chemical potential, one gets a time independent
form of Eq.(1) as


−


~2 2
∇ + Vext (r) − µ + g |ψ0 (r)|2 ψ0 (r) = 0.
2m

(2)

A vortex solution corresponds to ψ0 (r) = eisφ |ψ0 (r)|.
This particular wave-function (order parameter) represents a rotation around the axis of symmetry (say z-axis)
with a tangential velocity at a distance r from the vortexcore vs = ~s/mr, where over a closed contour around zH
~ = 2π~s/m. Here s is the number of quantum
axis v~s .dl
of angular momentum (h) the vortex carries. For practical purposes, s = 1 state is important because it is the
most stable one and higher order vortices quickly break
into the s = 1 state.
The radial part of the vortex state
√ is found out from
Eq.(2) by taking an ansatz |ψ0 | = nf (η), where η =
r/ξ0 is the radial distance in the unit of healing length.
Thus the equation for f (η) ≡ f is

1 d
d 
s2 
η f + 1 − 2 f − f 3 = 0,
η dη dη
η

(3)

where Vext = 0 has been set for the sake of simplicity
to study a single vortex somewhere near the middle of
the trap where effects of boundary are not appreciable.
Far away from the core of the vortex, i.e. at large
enough η, a solution constant over space should exist and
one gets non-trivial solution f = 1 by equating (f − f 3 )
to zero. At a small η, one takes f ∼ η |s| , where s is an
integer. Then, Eq.(3) reduces to
|s|2 η |s|−2 − s2 η |s|−2 + η |s| − η 3|s| = 0.
A balance of the dominant terms at small η , i.e. η |s|−2
shows that f = η |s| is a solution and this solution holds
for all s at the leading order. For a vortex with s = 1,
d
the cancellation happens between the terms η1 dη
f and
1
η 2 f which is somewhat a special case giving the same
solution f = η |s| .
Since the vortex core solution of any order comes from
the leading order terms resulting from the Laplacian, the
selection of the scale ξ0 is not accomplished in this computation. To actually determine this scale following the
present procedure, one has to look at the balance of the
terms at next to the leading order. This, however, is
not possible if one does not take into account non-local
interactions.
B.

Scale selection using energy functional

A scale selection for this vortex core is obtained by the
variation of the grand canonical free energy functional
of the local GP equation (Eq.1) in general. By taking
an ansatz√[2] for the vortex solution to be of the form
ψ(r, t) = n |f (r)|ei|s|φ e−iµt/~ where s is an integer.
Let
p
2
us consider the case |s| = 1 and take |f (r)| = r/ β + r2
as an ansatz. Since, this is a procedure employing energy
variations, the term containing any constant phase factor of f (r) is of no use. We plug this ansatz in the grand
canonical energy functional of the local GP equation and
minimize the energy with respect to β to get a scale selection. The grand canonical energy functional of the local
GP equation is [1]

E=

Z L2 Z 2π Z D h
−L
2

0

0

~2
|∇ψ(r, t)|2
2m
(4)
i
g
2
+ (|ψ(r, t)| − n) r dr dφ dz.
2

After putting the aforementioned ansatz for ψ(r, t) in
the above energy functional, we extremize it by setting
(∂E/∂β) = 0. This gives the following equation for
e βe = β/D),
β(

3

βe4 [6ξ02 − D2 ] + βe2 (4ξ02 − D2 ) + 2ξ02 = 0,
√
where ξ0 = ~/ 2mgn. We can find the roots of the above
equation in e
β, which gives
p
(D2 − 4ξ02 ) ± D4 − 32ξ04
2
e
β =
.
2(6ξ02 − D2 )

For the above equation to have roots, D4 ≥ 32ξ04 . This
condition is tailored in a BEC while exciting multiple
vortices[13, 14]. In this D >> ξ0 limit, we see that taking
the + sign makes the numerator ∼ 2D2 . However, we see
that there is another factor [6ξ02 −D2 ] in the denominator,
which becomes negative for D >> ξ0 , in turn making βe2
negative. If we take the − sign from the ±, the numerator
of the above equation becomes ∼ (−ξ02 ) , giving βe2 ∼
(ξ02 /D2 ) for D >> ξ0 . This gives us a scale selection of
β ∼ ξ0 . This is the vortex with core size of the order of
healing length.
The important point to note here is that for D4 −
32ξ04 < 0, the solution breaks down because βe becomes
complex. Now, D being a free parameter of a single vortex, it can be increased up to the system size, but in a
vortex lattice, D is restricted by the position of the nearest neighbours and in what follows we are going to look
at this limit after introducing the other class of solution.
C.

Existing non-local model

The condition for the above mentioned class of vortex
solution’s breakdown appears in the context of a local
GP dynamics is what we have seen so far. An important
question to ask at this point is - does the leading order
non-local correction to the local dynamics improve the
situation?
Let us revisit the above variational procedure taking
into consideration non-local interactions. We do that
to see if there exists a vortex solution of core size ξ0
when √
non-local interactions are present, despite having
D2 < 32ξ02 . Contemporary modifications to the local
GP equation (Eq.(1)) [5, 6, 15] involve adding a first order correction term, considering some microscopic potential underlying s-wave interactions. Using, for example,
the notations used by Collin et al., we get the following
non-local GP equation [6]

i~

∂ψ0 (r, t) h
~2 2
= −
∇ + Vext (r)
∂t
 2m

+ g |ψ0 (r, t)|2 + g2 ∇2 |ψ0 (r, t)|2

 2



i
ψ0 (r, t),

external potential and determine the nature of vortex
solution.
The energy functional for the non-local GP equation
given by Eq.(5) is [16]
Z L2 Z 2π Z D h

~2
g
|∇ψ(r, t)|2 + (|ψ(r, t)| − n)2 +
2m
2
−L
0
0
2
i
gg2
|ψ(r, t)|2 ∇2 |ψ(r, t)|2 r dr dφ dz.
2
(6)
p
We plug in the same ansatz, |f (r)| = r/ β 2 + r2 as
in the previous section and check for energy functional
minimization. Note that, since we do not want three
body effects to dominate, it is desirable to work in the
diluteness limit a3 n << 1 and hence g2 << ξ02 which can
safely be considered in orders of magnitude as g2 ∼ a2 .
The minimization condition yields
E=

βe6 (6ξ02 − D2 ) + βe4 (10ξ02 − 2D2 + 4g2 )
βe2 (6ξ 2 − D2 − 4g2 ) + 2ξ 2 = 0.
0

(7)

0

The above condition is cubic in βe2 . The coefficients
show that the length scale dictated by g2 would be
masked by that by ξ0 , unless g2 ≥ ξ02 . However, this
would take us away from the diluteness limit and into the
region where three body effects would become important.
Hence while we stay in the diluteness limit, the length
scale dictated by ξ0 would always dominate. Now,
√ in the
previous section, we have seen that for D2 < 32ξ02 , the
solution breaks down. For the same condition over most
of the parameter space, one can see that all the coefficients of Eq.(7) are positive which denies any acceptable
solution for βe2 . Therefore, even the presence of non-local
interaction
√ does not help getting such a vortex solution
for D2 < 32ξ02 in a system when the leading order nonlocal correction has been taken into account.
III.

SCALE SELECTION FROM NON-LOCAL
MODEL

Let us now consider the GP model with non-local correction and fix the length scale of the vortex from the dynamics. This is only doable in the presence of non-local
corrections to the local GP equation. We then minimize
the energy of this class of vortices by variation and fix
the entire profile.
√
Considering µ = gn and ψ0 (r) = nf (r)eisφ , we take
the standard ansatz, as already mentioned in section A,
f (r) = R|s| near the origin, where R = βr. Using this
ansatz, Eq.(5) near the origin is given by

(5)

where g2 = a3 − ar2e and re is the effective range of twobody interaction. Let us take Eq.(5) in the absence of an

β 2 |s|2 R|s|−2 − β 2 |s|2 R|s|−2 − 8πanR3|s|
i
h
+ 8πanR|s| 1 − g2 β 2 (2|s|)2 R2|s|−2 = 0,

(8)

4
Note that irrespective of the choice of β and |s|, the
balance between the leading order terms, i.e. the first
two terms of the above equation is always there. On top
of that, due to the non-local correction term introduced
in Eq.(5), there now exists a special case of |s| = 1 where
there exists a balance in the sub-leading terms in brackets
in Eq.(8). This now imposes a selection of β, given by β =
√
1/(2 g2 ) only for |s| = 1. This selection exists when gg2
is positive, or having g positive when g2 is also positive,
i.e. re < 2a/3. This in general would be a situation when
repulsive s-wave scattering is the dominant interaction
mechanism in BEC, which is well known to be the case
for all metastable BEC. Since, in this regime, g2 ∼ a2 ,
hence, we get from the above β selection that β ∼ 1/a.
The next obvious line of inquiry would be generalizing
this approach to include all vortices.

IV.


~2 1 d  d
~2 s2
r |ψ0 | +
|ψ0 | + g|ψ0 |2 ψ0 − µ|ψ0 |
2m r dr dr
2mr2
 a4  1 d
h a2 1 d  d
d 2
r |ψ0 |2 +
|ψ0 |2
r
+ g|ψ0 |
2 r dr dr
8 r dr dr
i
a2l  1 d
d 2l
+ ..... +
r
|ψ0 |2 + .... = 0,
(2l)!! r dr dr
(10)
−

√
Considering µ = gn, ψ0 (r) = nf (r), and f (r) =
R near the origin, where R = βr, for a vortex with
|s| quanta of circulation, the series in square brackets in
Eq.(10) terminates at 2|s|-th order in derivatives as all
other higher order derivatives would be zero. Thus, we
get
|s|

h
β 2 |s|2 R|s|−2 − β 2 |s|2 R|s|−2 − 8πanR3|s| + 8πanR|s| 1

GENERALIZATION

a2 β 2
a4 β 4
(2|s|)2 R2|s|−2 −
(2|s|)2 (2|s| − 2)2 R2|s|−4
2
8
i
a2|s| β 2|s|
((2|s|)!!)2 = 0.
− .... −
(2|s|)!!

−
The local GP equation follows from its full non-local
form




~
∂ψ0 (r, t)
= −
∇2 + Vext (r, t) ψ0 (r, t)
i~
∂t
2mZ
′
+ ψ0 (r, t) dr ψ0∗ (r′ , t)V (r′ − r)ψ0 (r′ , t).
2

(9)
Let us consider the interaction to be repulsive s-wave
scattering, which is the most dominant interaction in a
BEC.
Under the first Born approximation, s-wave scattering can be captured by using an effective repulsive softpotential [1, 17]. The range of this effective repulsive potential is in general of the order of the scattering length.
We use this approach in what follows, because the system
we deal with is necessarily having lowest energy repulsive
s-wave scattering. We Taylor expand the wave-function
to explore the structure of ψ and the corresponding density n. The effective potential simply sets the length scale
over which the density variation is now being probed. Important to note that, although we are capturing here the
interactions underlying s-wave scattering through an effective repulsive potential for the sake of simplicity, the
actual potential can have bound states and, thus, can
undergo Feshbach resonance.
We, therefore, take the interaction pseudopotential as
′ 2
√
′
|
V (r − r) ≃ Vef f = [g/( 2πa)3 ] × exp[− |r−r
2a2 ]. Following the arguments given above, the range of the Vef f
would be of the order of s-wave scattering length and
hence we set the range of Vef f as a. Doing a Taylor
′
expansion of the wave-function ψ(r , t) about r, we get

The first 3 terms correspond to local GP equation and
at the leading order R|s|−2 we get the same result as is
already shown. The next higher order terms are the first
and the last terms in the square bracket which are in bal1
ance when β = 1/a[(2|s|)!!] 2|s| giving us a selection on β.
Note that, the first term in the square bracket comes from
the linear term µ|ψ0 | in Eq.(10). Note also that, had we
considered any other flat symmetric repulsive potential
in the place of the Gaussian one, the Taylor expansion
would only change coefficients involving |s|. Thus, the
scaling β ∼ 1/a is always there.
The natural truncation of the Taylor expansion of the
interaction term, depending upon the order of the quantized vortex, is something of immense importance here.
There exists no need to truncate the series based on order
of magnitude arguments. The structure of the core of a
vortex, i.e. f (r) = R|s| naturally truncates the series and
that is where the Taylor expansion makes perfect sense
to be in use. For the kind of order parameters which
does not provide such a natural truncation of the Taylor
series, the Taylor expansion method cannot be used for
these small scale structures where λ ∼ a.
Having constructed the core with a definite selection
of the length scale, we can construct a full variational
solution for a vortex with |s| quantum of circulation. To
compute the free energy in what follows, we take the energy integral over R varying from 0 to D, where r = D/β
is the radial cut off. To obtain the solution, we divide the
region (0, D) in two parts. These regions are (0, α|s| ) and
(α|s| , D). In the region (0, α|s| ) we consider the vortex
solution as R|s| (as was shown above in the analysis to
obtain β) and in the region (α|s| , D), we take the ansatz
f (R) = (1 − λ|s| e−δ|s| R ). The choice of this latter part of

5
the solution is particularly good because it rises to unity
at large R and it involves two free parameters which we
can adjust to get a continuous solution. By matching of
these two functions and their derivatives at R = α|s| we
obtain λ|s| = (1 − (α|s| )|s| ) · exp[|s|(α|s| )|s| /(1 − (α|s| )|s| )],


δ|s| = |s|/ (α|s| )(1−|s|) − α|s| as a function of α|s| . Then,
Z D
0

d 2
gn2
df 2 ~2 β 2 f 2
gn2 f 2 n β 2 a2 1 d
2πRdR h ~2 β 2
+
R
n
n 2+
(1 − f 2 )2 +
f
2
β
2m
dR
2m R
2
2
2 R dR dR
β 4 a4  1 d
d 2 2
β 2|s| a2|s|  1 d
d 2|s| 2 oi
+
.
R
f + ... +
R
f
8
R dR dR
(2|s|)!! R dR dR

We use the above mentioned prescription and evaluate
the energy minimum in terms of α|s| . As we assume the
diluteness limit a3 n << 1, we can take an << β 2 for
any |s| since β ∼ 1/a. Making use of this inequality and
keeping terms which go as β 2 over terms which go as (an)
we get an expression for free energy as

E=

2π~2 n h |s|2  D 
ln
m
2
α|s|

THIN VORTEX IN A HARMONIC TRAP

Let us now consider the analysis applied above for a
BEC in a harmonic trap. We shall discuss a vortex solution with unit circulation, i.e. s = 1 using the model
by Collin et al. . We consider cylindrical geometry and
assume tight confinement along the z direction. This
consideration would give the GP model used by Collin et
al. as
~2 2 1
∂ψ0 (r, t) h
= −
∇ + mω 2 r2
∂t
2
 2m

+ g |ψ0 (r, t)|2 + g2 ∇2 |ψ0 (r, t)|2

0.8

sP=1
s=1
s=2
s=3

0.6

0.2

The minimization of the above energy functional gives
p
1
α|s| = [(1 − |s| + 49|s|2 − 10|s| + 1)/(12|s| − 2)] |s| . Using this α|s| , we can now evaluate λ|s| and δ|s| for a
given value of |s|, thus we determine f (R) for the interval
(α|s| , D).
We plot f (R) for |s| = 1, 2, 3 in Fig.(1) for the generalized non-local model and for the non-local model by
Collin et al. [6] with |s| = 1. For the non-local model of
Collin et al we have taken re = a/2 to plot the density
profile of the vortex. The figure shows that the width of
the vortices is of the order of s-wave scattering length.

i~

(11)

1.0

0.4

2|s|
 λ2 
|s|α|s| i
|s|
(1 + 2α|s| δ|s| )e−2α|s| δ|s| +
.
+
8
2

V.

The free energy functional corresponding to the general
vortex of number of circulation |s| in the solution we have
chosen is [16]

f

Ev =

we plug in the complete solution (from 0 to D) in the
energy functional (Eq.(10)) [16] to minimize the energy
and thereby fix the position of matching α|s| .

i
ψ0 (r, t),

(12)

0.0
0.0

1.0

2.0

3.0

r/a
FIG. 1. Figure shows the density profile of single vortex line
for different circulations s for the generalized model and also
for the microscopic interaction model by Collin et al. labelled
by sP for |s| = 1 with re = a/2.

where ω is the trap frequency and r is the radial distance from the trap centre. Due to the harmonic trapping, the ground state of the BEC is no longer one with
uniform density, but would fall off away from the centre of the trap. The Thomas-Fermi(TF) density of the
condensate can be evaluated by neglecting the kinetic
contribution coming from the Laplacian terms. By con√
sidering ψ0 = nT F e−iµt/~ , we get the TF density as
nT F = g1 (µ − 21 mω 2 r2 ). We wish to probe the vortex
core scaling similar to the previous analysis (where we
had considered a uniform background density). To this
end, we consider a vortex with unit circulation(s = 1)
at a distance d away from the trap centre. If we consider a coordinate system (ρ, θ) centred at the vortex
core, we would get the vortex profile near the core as
p
nT F (d) β ρeiθ e−iµt/~ , where nT F (d) is the TF density
at a distance d from the trap centre. In considering a
linear profile, we have assumed that the TF density of
the condensate remains constant up to the first order in
ρ. Also, as before we have considered here the vortex as
an excited state on top of the ground state density. With

6

p
p
~2 h eiφ r2 − 2rd cos φ + d2
2
2
µ r − 2rd cos φ + d =
2m
r(d − eiφ r)
p
eiφ r2 − 2rd cos φ + d2 i
−
r(d − eiφ r)
p
1
+ mω 2 r2 r2 − 2rd cos φ + d2
2
p
+ gnT F (d)β 2 ( r2 − 2rd cos φ + d2 )3
p
+ 4gg2 nT F (d)β 2 r2 − 2rd cos φ + d2 .
(13)
From the equation above, we can see that the terms
coming from ∇2 ψ cancel each other out. We then wish to
look at the remaining terms in Eq.(13). Since we consider
ρ to be small, we go back to the (ρ, θ) coordinate system.
This gives us

joining the trap centre to the core), viz., the region of the
core (−α, α) and the regions away from the core (α, D−d)
and (−(D + d), −α) . In our calculation, we write the TF
density in terms of the radial coordinates of the vortex
centre (̺, θ), where ̺ = βρ. Thus, the TF density is
2
2
2
2
nT F (̺) = (1/g)(µ − mω
2 [(̺ /β ) + 2̺(d/β) cos θ + d ]).
We take the ansatz for vortex solution of the form ψ =
f (̺) eiθ e−iµt/~ . For the interval of the core given by
(0, α), f = ̺ nT F (̺). Outside the core, the ansatz is
f (̺) = (1 − λe−δ̺ ) nT F (̺). As before, we match the
two solutions and their derivatives at ̺ = α. Further, we
minimize the energy functional with respect to α as before. Following this procedure, we numerically evaluate
the parameters in the variational procedure and thus obtain the profile shown in Fig.(2) for the constant mω 2 /2µ
set equal to unity. Our variational method works perfectly in determining the large scale profile of the vortex.

1.0

0.8

g f/µ

respect to the coordinate system (r,pφ) around the trap
centre, ρ and θ transform as ρ = r2 − 2rd cos φ + d2
and θ = tan−1 [r sin φ/(r cos φ − d)].
Considering
this, we can write the density profile of the vortex
at a distance d from the trap centre as ψ0 (r, t) =
p
p
r sin φ
−1
nT F (d) β r2 − 2rd cos φ + d2 ei tan [ r cos φ−d ] e−iµt/~ .
Putting this ansatz in Eq.(12) gives us

0.6

0.4



1
ρ µ − mω 2 d2 − gg2 nT F (d)β 2 − ρ2 (mω 2 d cos θ)
2


3 1
−ρ
mω 2 + gnT F (d)β 2 = 0.
2
Up to the leading order in ρ then, we get, [µ− 21 mω 2 d2 −
4gg2 nT F (d)β 2 ] = 0. As the TF density at a distance d
from the trap centre is given as nT F = g1 (µ − 12 mω 2 d2 ),
√
we get the expression for β as β = 1/2 g2 , same as for a
BEC in the absence of a trap. While, the vortex profile
far away from the core may be different from that in
the uniform density background case, the scaling of the
density profile near the vortex core remains the same.
This shows that the thin vortex solution obtained on top
of a BEC with uniform density can be obtained for a
harmonically trapped BEC as well. An anharmonic term
of the order r4 in the potential will again get absorbed
by the TF density profile and will not change our result
up to the scope of the present approximation.
Having obtained the core, we can now use the variational method applied in the previous section to obtain
the entire vortex solution. We take the large scale cut-off
width for the harmonically trapped BEC to be D and divide the radial interval (0, D) into two regions as before.
So long as D is bigger than the width of the actual confinement, there is no problem because the density vanishing beyond the actual width makes the integrand vanish
and the integral remains the same as the one obtained
considering the actual width. If the vortex is situated at
a distance d from the trap centre, there would in effect be
three regions in the coordinates of the vortex(along a line

0.2

0.0
-20.0

-16.0

-12.0

-8.0

-4.0

0.0

4.0

8.0

12.0

16.0

20.0

x/a
FIG. 2. Figure shows the density profile of single vortex line
in a harmonically trapped BEC situated at d/a = 12 from
the centre of the trap based on the model by Collin et al. for
|s| = 1 with re = a/2.

VI.

COMPARISON OF ENERGY OF TWO
CLASSES OF VORTICES

We now return to the discussion of vortex solution for
a uniform BEC in the absence of any trap. Let us now
compare the grand canonical energy of the two classes of
vortices, one with core size of the order of healing length
(thick vortex) and other with core size of the order of
s-wave scattering length (thin vortex). To the leading
order, the energies of the vortex with core of size of healing length (Eξ0 ) and that with core size of scattering

2

length (Ea ) are given by Eξ0 ∼ ( π~mLn )ln |s|D
and
ξ0


2
D
respectively, where α|s| is an orEa ∼ ( π~mLn )ln α|s|
a
der unity number. From these terms, we can see that if
the healing length and the s-wave scattering length are of
equal order, the two classes of vortices actually become
comparable in energy. However, as we change the scat-

7
tering length and make it smaller by keeping the density
fixed, we increase the healing length. In this case, the
thick vortex with the length scale corresponding to the
healing length will be energetically favoured because it is
a state of lower energy.
However, as mentioned earlier that, for the thick vortex
solution to exist, the condition is D4 ≥ 32ξ04 . In the case
D4 < 32ξ04 , the thick vortex would cease to exist as that
length scale selection is no longer present. Hence, the
vortex solution existing in this regime could be a thin
vortex with core size of the order of the s-wave scattering
length.
Let us discuss an experimentally plausible situation
where a thick vortex solution does not exist and a thin
vortex state can possibly be captured. Note that, the
radial cut off D corresponding to a single vortex inside
a vortex lattice is rather restricted and is actually much
smaller than the system size. In such a situation, one
can employ Feshbach mechanism off resonance to reduce
the s-wave scattering length to smaller values such that
ξ0 ∼ D or make the packing of the vortices in the lattice
so dense that the ξ0 ∼ D condition is satisfied. One can
reasonably expect here that the thin vortices to show up
in the absence of thick vortices and some already trapped
quantized angular momenta.
VII.

DISCUSSION

Note that in arriving at the new class of vortex solution
we have used here the already existing method of fixing
the vortex core structure, in the presence of non-local
corrections. The variational procedure then is employed
to make this vortex core smoothly evolve to the uniform
density far field. As opposed to Padé type approximate
solution being used as a variational ansatz, which is standard, our variational analysis(practically for all vortices)
is using a well determined solution of the core of the
vortices at small r up to next to leading order approximation. As we have already shown in the section named
’Standard Theory’, at the leading order, at small r, near
the core of a vortex, the conventional theory based on the
dynamics cannot give a length scale selection and works
fine for the thick vortices. However, in order to go to
the sub-leading corrections, one must take the non-local
correction into account which we have done and have determined the solution for the core of the vortex from the
dynamics itself where the appropriate length scale shows
up. Then, while making this core of the vortex recover to
the uniform field, far away from the core, we have used

[1] L. Pitaevskii and S. Stringari, Bose-Einstein Condensation (Oxford Science Publications, 2003)
[2] C. Pethick and H. Smith, Bose-Einstein Condensation in
Dilute Gases (Cambridge University Press, 2001)

variation to have a smooth transition. Thus, our variational approach is just not based entirely on guessed
ansatz, rather, the most important part of the solution is
obtained from the dynamics and then it is extrapolated
to the far field smoothly using variation.
Note that the results involving higher order vortices
resulting from the higher order terms of the expansion
although are coming out through a general procedure,
but, may not all be physically accessible because of involvement of higher derivative i.e. smaller length scales.
However, the first correction term should always be there
since a Laplacian is already present in the local model.
So, the result involving the lowest order vortex which is
most stable is there.
A consistent mathematical analysis following well established methods of theoretically capturing vortex solutions, indicate here the presence of thin vortex solutions
due to non-local interactions. The non-local interaction
correction taken in the present context and in other previous works [6] presents small length scales on top of that
captured by the mean field GP dynamics. The origin of
such fluctuations probably lies in the quantum effects not
captured by the local GP dynamics. In that sense, the
dynamics of these thin vortices would possibly manifest
quantum fluctuations in the system which are required
for vortex lattice melting and also important in the context of superfluid turbulence that has attracted a lot of
attention lately [18]. Apart from the possible experimental situation where the thick vortex breaks down, which
we have identified as a plausible situation where our thin
vortex solution can be realized, a quench through the critical point and subsequent formation of vortex-antivortex
pairs through Kibble-Zurek [19] mechanism could also
be a possible procedure to realize such a vortex. If experimentally realized, these objects can possibly demonstrate quantum fluctuations in vortices which involves
rich physics.

ACKNOWLEDGMENTS

Abhijit Pendse would like to acknowledge the support
provided by the Council of Scientific and Industrial Research(CSIR), India. AP and AB would like to acknowledge very useful suggestions by anonymous referees which
has helped us put this work in proper context.
AP and AB have made equal contributions to this research.

[3] N. R. Cooper, N. K. Wilkin, and J. Gunn, Phys. Rev.
Lett. 87, 120405 (2001)
[4] A. Rozhkov and D. Stroud, Physical Review B 54,
R12697 (1996)

8
[5] H. Fu, Y. Wang, and B. Gao, Phys. Rev. A 67, 053612
(2003)
[6] A. Collin, P. Massignan, and C. Pethick, Physical Review
A 75, 013615 (2007)
[7] S. Viefers, Journal of Physics: Condensed Matter 20,
123202 (2008)
[8] N. Regnault and T. Jolicoeur, Phys. Rev. Lett. 91,
030402 (2003)
[9] M. Roncaglia, M. Rizzi, and J. Dalibard, Scientific reports 1 (2011)
[10] P. Nikolić, Phys. Rev. A 90, 023623 (2014)
[11] N. Rougerie, S. Serfaty, and J. Yngvason, Phys. Rev. A
87, 023618 (2013)
[12] S. Furukawa and M. Ueda, Phys. Rev. A 86, 031604 (Sep

2012)
[13] K. Madison, F. Chevy, W. Wohlleben, and J. Dalibard,
Phys. Rev. Lett. 84, 806 (2000)
[14] J. Abo-Shaeer, C. Raman, J. Vogels, and W. Ketterle,
Science 292, 476 (2001)
[15] H. Veksler, S. Fishman, and W. Ketterle, Physical Review A 90, 023620 (2014)
[16] A. Pendse, arXiv:1512.00152(2015)
[17] J. J. Sakurai and J. Napolitano, Modern quantum mechanics (Addison-Wesley, 2011)
[18] E. Kozik and B. Svistunov, Journal of Low Temperature
Physics 156, 215 (2009)
[19] B. Damski and W. H. Zurek, Physical review letters 104,
160404 (2010)

