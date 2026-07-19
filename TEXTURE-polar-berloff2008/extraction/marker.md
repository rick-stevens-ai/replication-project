# Marker extraction — Berloff 2008 (arXiv:0801.2964)

> **NOTE (interim):** `marker` binary not installed on this host. This file is a
> `pdftotext -layout` interim extraction standing in for the Marker artifact.
> Layout-preserving mode retains column/table structure best for equations.
> Regenerate with `marker_single textures-polar-berloff2008.pdf` when available.

---

                                                      Vortex Splitting in Subcritical Nonlinear
                                                              Schrödinger Equations
arXiv:0801.2964v1 [cond-mat.other] 17 Jan 2008




                                                                             Natalia G. Berloff ∗
                                                           Department of Applied Mathematics and Theoretical Physics
                                                        University of Cambridge, Cambridge, CB3 0WA, United Kingdom



                                                 Abstract

                                                 Vortices and axisymmetric vortex rings are considered in the framework of the
                                                 subcritical nonlinear Schrödinger equations. The higher order nonlinearity present
                                                 in such systems models many-body interactions in superfluid systems and allows one
                                                 to study the effects of negative pressure on vortex dynamics. We find the critical
                                                 pressure for which the straight-line vortex becomes unstable to radial expansion of
                                                 the core. The energy of the straight-line vortices and energy, impulse and velocity
                                                 of vortex rings are calculated. The effect of a varying pressure on the vortex core is
                                                 studied. It is shown that under the action of the periodically varying pressure field
                                                 a vortex ring may split into many vortex rings and the conditions for which this
                                                 happens are elucidated. These processes are also relevant to experiments in Bose-
                                                 Einstein condensates where the strength and the sign of two-body interactions can
                                                 be changed via Feshbach resonance.

                                                 Key words: superfluidity, vortices, vortex rings, nonlinear Schrödinger equation.




                                                 1   Introduction


                                                 The nonlinear Schrödinger (NLS) equation

                                                                                     1
                                                                              − iψt = ∇2 ψ + g|ψ|2ψ,                               (1)
                                                                                     2
                                                 where g = ±1, is one of the most studied equations of mathematical physics
                                                 with applications ranging from nonlinear optics, where ψ represents the elec-
                                                 tric field, Bose-Einstein condensates (BECs) and superfluidity, where ψ is the
                                                 ∗ Email address: N.G.Berloff@damtp.cam.ac.uk



                                                 Preprint submitted to Elsevier Science                              30 October 2018
field wavefunction, to fluid dynamics, where ψ describes the amplitude of al-
most monochromatic wave. The nonlinear term in this equation represents the
action of a refraction index that depends on the electric field intensity in non-
linear optics or corresponds to the two-body repulsive (g = −1) or attractive
interactions (g = 1) of the bosons in superfluids and BECs.

The formation of singularities in finite time for the focusing NLS equation
(with g = 1) is in practice been arrested by higher order nonlinear terms
that come from the expansion of the nonlinear refraction index in optics, from
many-body interactions in superfluids or from the effects of the geometry of
the trapping potential in BECs that offers the reduction in the number of
dimensions. These leads to a modification of the focusing NLS equation to
what is known as “subcritical” or cubic-quintic NLS equation

                             1
                      − iψt = ∇2 ψ + (g1 |ψ|2 − g2 |ψ|4)ψ.                   (2)
                             2
This model was used to study cavitation and vortex nucleation (Josserand
et al, 1995), formation of vapor droplets in superfluids (Josserand and Rica,
1997), solitary waves in nonlinear optics (Kivshar and Agrawal, 2002), and
bright solitons in elongated BECs (Sinha et al, 2006; Khaykovich and Mal-
omed, 2006).

In this paper we consider a general class of subcritical NLS (SNLS) equations
that allow for different orders of nonlinearity

                          1
                   − iψt = ∇2 ψ + (g1 |ψ|2 − g2 |ψ|2(1+γ) )ψ,                (3)
                          2
where γ is an integer. The choice of the parameter γ = 1 corresponds to
the first-order term in the expansion of nonlinearity in the correlation energy
and results in the the cubic-quintic equation (2), whereas γ = 3 is close to
the value 2.8 used in density-functional theories (Dalfovo, 1992) to produce a
quantitatively correct equation of state for superfluid helium II.

Thus, we can view Eq. (3) to be a dimensionless form of a modified Gross-
Pitaevskii equation

                            ~2 2                          
                 i~ψt = −      ∇ ψ + W0 |ψ|2(1+γ) − V0 |ψ|2 ψ,               (4)
                            2m
where m is the mass of a boson, V0 is a δ−function two-body attractive inter-
action potential and many-body repulsive interactions are characterized by a
parameter W0 . Equation 4 can be written in the Hamiltonian form

                                       ∂ψ   δH
                                  i~      =      ,                           (5)
                                       ∂t   δψ ∗


                                          2
where the Hamiltonian (energy functional) of the system is
                   Z                                                !
                          ~2        V0       W0
              H=             |∇ψ|2 − |ψ|4 +     |ψ|2(2+γ) dx.                       (6)
                      V   2m        2       2+γ

To find the ground state the energy functional (6) has toR be minimized subject
to the conservation of the number of particles N = |ψ|2 dx. This can be
achieved by introducing a Lagrange multiplier µ and minimizing H − µN.
The energy of the ground state becomes

                                   V0 N 2    W0 N 2+γ
                          H0 = −          +             ,                           (7)
                                   2 V      2 + γ V 1+γ
                                                        R
and the ground state is given by ψ02 = N/V , V =             dx. The chemical potential
µ can be introduced into (4) explicitly by

                              ψ → ψ exp(−iµt/~),                                    (8)

so that (4) becomes

                          ~2 2                              
              i~ψt = −       ∇ ψ + W0 |ψ|2(1+γ) − V0 |ψ|2 − µ ψ.                    (9)
                          2m
The ground state, ψ0 , gives the value of the chemical potential as
                                       2(1+γ)
                             µ = W0 ψ0          − V0 ψ02 .                         (10)


The hydrostatic pressure of the system is found as

                           ∂H0   (1 + γ)W0 2(2+γ) V0 4
                   P =−        =          ψ0     − ψ0 .                            (11)
                           ∂V       2+γ           2
Hydrodynamic relation for the compressibility
                                     1     ∂n
                                       2
                                         =                                         (12)
                                    mc     ∂P
where n = |ψ0 |2 is the number density, gives the expression for the speed of
sound, c as
                                (1 + γ)W0 n1+γ − V0 n
                          c2 =                        .                  (13)
                                          m
We conclude that the SNLS model, in particular, can be used to study the
effects of a negative pressure. This is not possible with the cubic NLS model
(1) that is often used as a phenomenological model of superfluid helium, but
where P ∼ ρ2 .

In the last couple of decades there has been a number of experiments which
explore the behaviour of superfluid helium at negative pressure by means of


                                         3
ultrasound waves that produce an oscillating pressure within a small volume
of helium (Nissen et al, 1989; Maris and Xiong, 1989; Xiong and Maris, 1989).
In BECs experiments, Feshbach resonance is used to change the magnitude
and sign of the scattering length. This can be modelled by Eq. (4) with a
periodically varying V0 (t) in the presence of the external magnetic trap. In
this paper we shall study the effects of variations of V0 on the vortex structure
and dynamics.

We cast Eq. (9) into dimensionless form by

                                         ~
                 x → b x,       t→         2(1+γ)
                                                    t,   ψ → ψ0 ψ,          (14)
                                     W0 ψ0

where the healing length, b, is defined by

                                      ~
                              b= q             ,                            (15)
                                        2(1+γ)
                                  W0 mψ0

so that Eq. (9) becomes

                     1                                   
              − iψt = ∇2 ψ + |ψ|2(1+γ) − 2ξ|ψ|2 + (1 − 2ξ) ψ,               (16)
                     2
where we denoted ξ = V0 /2W0 ψ0γ .

At P = 0, n0 = (V0 (2 + γ)/2(1 + γ)W0 )1/γ and the speed ofqsound is c20 = (1 +
γ)γW0 n1+γ
        0 /(2 + γ).The healing length becomes b = ~/mc0 γ(1 + γ)/(2 + γ).
Since the known speed of sound in superfluid helium is qapproximately 238 m
 −1
s , the healing length at zero pressure is b = 0.6685 γ(1 + γ)/(2 + γ) Å,
which for γ = 3 gives b = 1 Å and the unit of time as 6.28 × 10−13 s.

In dimensionless units, the wavefunction in the bulk is ψ0 = 1, the density is
ρ = |ψ|2, and the local pressure and the local speed of sound are


          1 + γ 2+γ
    P=         ρ    − ξρ,                                                   (17)
          2+γ
          q
     c=    (1 + γ)ρ1+γ − 2ξρ.                                               (18)

The paper is organized as follows. In Section 2 we study the amplitude and
energy of the straight-line vortex at various pressures (interactomic strengths).
We find the critical value of ξ at which the vortex becomes unstable to radial
expansion for various values of γ. Section 3 is devoted to vortex rings and
other travelling coherent structures that propagate with a fixed velocity. We
calculate the energy and impulse of these matter waves. The time evolution of
a line vortex and a vortex ring with a periodically varying pressure is studied


                                       4
in Section 4. We show that the vortex ring splits into many vortex rings if
the negative pressure reaches the critical value for the vortex instability. We
conclude with Section 5.



2   Vortex Lines


A vortex line is defined by a zero of the wave function ψ = 0. In cylindrical
coordinates (r, θ, z) the wave function of the straight-line vortex takes form

                                  ψ = f (r) exp[isθ],                              (19)

where s is an integer (“winding number”, “topological charge”). Fluid rotates
around the z-axis with the tangential velocity
                                            s
                                   u = s∇θ = eθ                                    (20)
                                            r
and the amplitude, f , satisfies
              "          !         #
           1 1 d    df        s2
                  r          − 2 f + 2ξf 3 + (1 − 2ξ)f − f 2(1+γ)+1 = 0.           (21)
           2 r dr dr          r

The boundary conditions are f (0) = 0 and f → 1 as r → ∞. Analysis of Eq.
(21) shows that near the origin f (r) ∼ as r |s| and at infinity

                     s2          s2 (2γ 2 s2 + γ(8 + 3s2 ) − (8 + s2 )(2ξ − 1))
f (r) ≈ 1 −                    −                                                + · · ·.
              4(1 + γ − 2ξ)r 2                 32(1 + γ − 2ξ)3r 4
                                                                                 (22)
Similar to the case of the cubic defocusing NLS equation, only vortices with
single unit of quantization, s = ±1, are dynamically stable (Josserand et
al, 1995). Equation 21 was solved using a finite-difference discretization and
Newton-Raphson iterations. Figure 1 gives plots of the vortex amplitudes f
as functions of r. Figure 2 depicts the slopes at the origin of the vortex am-
plitudes, a1 , as functions of ξ for various values of γ. Above a critical value of
ξcrit (γ) the vortex becomes unstable and expands in a radial direction as seen
by numerically integrating Eq. (16) starting with the stable vortex and rais-
ing the value of ξ. The existence of a critical pressure for the vortex stability
has been established in the context of density-functional theory by Xiong and
Maris (1991) (giving the value of the critical pressure as −6.5 bars) and by
a more sophisticated theory by Dalfovo (1992) (giving the value of −8 bars).
We observe that the instability occurs when the slope of the vortex amplitude
at the center of the vortex becomes zero and the negative pressure forces can
no longer be balanced by the centrifugal energy of the fluid flow.

We can find the values of the critical pressure for the instability by evaluating


                                          5
Fig. 1. The amplitudes of straight-line vortices for s = ±1 as solutions of Eq. (21)
for various γ = 1, 2, 3, 4, 5 and ξ = (1 + γ)/(2 + γ) that correspond to zero pressure.
The larger values of γ correspond to tighter vortex cores.

               1.0
       f (r)
               0.8


               0.6


               0.4


               0.2


               0.0
                     0.0   0.5         1.0             1.5    2.0       2.5
                                                       r
Fig. 2. The slopes at the origin, a1 , of the amplitudes of straight-line vortices for
s = ±1 as solutions of Eq. (21) for various γ = 1, 2, 3, 4 as functions of ξ. Dots
represent numerical integration, solid lines – Eq.(23). The values of (ξ, a1 ) that
correspond to zero pressure are shown by red crosses.


         a1 1.0
               0.8

                                                               γ=4
               0.6


               0.4
                                                   γ=1
                                                                              x x
                                                                        x
               0.2                                                  x

               0.0
                     0.0         0.2         0.4             0.6            0.8
                                                        ξ
Eq. (17) with ργ = V0 /2W0 ξcrit and calculating W0 and V0 at zero pressure
using the speed of sound 238 m s−1 , mass of the boson 6.628 × 10−27 kg and
the density 145.2 kg m−3 . For γ = 3 we obtained the critical pressure as −6
bar, that agrees quite well with the estimates using much more sophisticated
density-functional theories.

Phenomenologically, the slope at the origin obeys a simple law
                                                       q
                                 a1 (ξ) = a1 (0) 1 − ξ/ξcrit,                       (23)

where a1 (0) = limξ→0 a1 (ξ) and ξcrit = a−1
                                          1 (0). Equation (23) gives the slope
at the origin accurate to two significant digits. For instance, our calculations


                                                   6
agree with the result presented by Josserand et al (1995) done for γ = 1.
Numerically, we get a1 = 0.286 for ξ = 5/8, and Eq. (23) gives a1 = 0.29.
Table 1 shows the values of a1 (0) and ξcrit for various γ.
                                   Table 1.

           γ=1              γ=2                γ=3               γ=4
 a1 (0) 0.9575 1.02155 1.05921 1.08409
 ξcrit     0.689            0.789              0.851             0.893

To determine the energy of the vortex, we need to modify the energy functional
(6) by the presence of the ground state. To do this we restore dimensional
units temporarily. Following Jones and Roberts (1982) we denote by ψu the
wavefunction of the undisturbed system of the same mass, so that
                                                 Z
                                                         |ψ|2 dx = ψu2 v,                            (24)
                                                 V
            R
where v = V dx, and by ψ∞ the wavefunction of the bulk: ψ → ψ∞ as r → ∞.
For the quartic term in the expression for the energy we write using Eq. (24)
                     Z                                   Z
           q2 =            |ψ| dx − ψu4 v =
                                4
                                                               (|ψ|2 − ψ∞
                                                                        2 2
                                                                          ) dx − (ψu2 − ψ∞
                                                                                         2 2
                                                                                           ) v.      (25)
                      V                                    V

Similarly, we obtained recursively

                Z                               Z
         q3 =        |ψ|6 dx − ψu6 v =                   (|ψ|2 − ψ∞
                                                                  2 3              2 3
                                                                    ) dx − (ψu2 − ψ∞         2
                                                                                     ) v + 3ψ∞ q2 .
                ZV                                   V               Z
                           2(2+n)
    q2+n =           |ψ|            dx − ψu2(2+n) v =                    (|ψ|2 − ψ∞
                                                                                  2 2+n
                                                                                    ) dx
                 V                                                 V
                                                                  n
                                                                  X
                               −(ψu2 − ψ∞
                                        2 2+n
                                          ) v+                           (−1)k−1 C2+n
                                                                                  k    2k
                                                                                      ψ∞  q2+n−k ,   (26)
                                                                  k=1

where n is a positive integer and Cik are the binomial coefficients. The terms
  2
(ψ∞ − ψu2 )n v are O(1/v) and vanish as v → ∞. In this limit, the dimensionless
energy becomes
                               Z                             Z
                     1                     2                                           1
                Eγ =                |∇ψ| dx − ξ                  (|ψ 2 | − 1)2 dx +       Q2+γ ,     (27)
                     2                                                                2+γ
where Q2+γ are defined recursively as

                Z
         Q2 =        (|ψ|2 − 1)3 dx,
                Z                                        n
                                                         X
                           2         2+n
    Q2+n =           (|ψ| − 1)             dx +              (−1)k−1 C2+n
                                                                      k
                                                                          Q2+n−k .                   (28)
                                                     k=1



                                                                 7
Fig. 3. Values of vortex core parameter ℓ defined by (31) of straight-line vortices
for s = ±1 for various γ = 1, 2, 3, 4 as functions of ξ. The values of the vortex core
parameter ℓ at zero pressure are −0.09 for γ = 1, 0.22 for γ = 2, 0.37 for γ = 3,
0.46 for γ = 4. The phenomenological fit (32) is given by the solid lines.


                               γ=3
       ξ 0.8
                                      γ=2
         0.6
                          γ=1
                                                                                       γ=4
         0.4



         0.2



         0.0
                -0.2           0.0          0.2    0.4       0.6     0.8      1.0        1.2
                                        ℓ
In dimensional units the energy per unit length of the line vortex becomes

                           ∞ "        #
                    κ2 ρ∞ Z     dR 2 R2            Z ∞
               Ev =                  + 2 r dr − 2ξ     (R2 − 1)2 r dr
                     4π         dr    r             0
                                      0
                          2          hZ ∞
                     +                      (R2 − 1)2+γ r dr
                         2+γ          0
                         γ                        Z ∞                          !
                         X                                                    i
                     +       (−1)k−1 C2+γ
                                      k
                                                         (R2 − 1)2+γ−k r dr        .           (29)
                         k=1                       0


The second term in the first integral in Eq. (29) represents the classical kinetic
energy that diverges. This can be remedied by introducing a cut-off distance
L, corresponding to the characteristic size of the container, and writing
               Z ∞           Z L/b        Z 1 2      Z ∞ 2
                     R2            1         R          R −1
                        dr =         dr +       dr +         dr.                               (30)
               0     r        1    r       0  r       1    r
The energy per unit length of the line vortex can, therefore, be expressed in
the form                                       
                               κ2 ρ∞      L
                         Ev =         ln      +ℓ ,                       (31)
                                 4π       b
where ℓ can be found by numerical integration. Figure 3 shows the values of
the vortex core parameter ℓ as a function of ξ for various values of γ.

Phenomenologically, the relationship between ξ and ℓ has the form

                         ξ = ξcrit − σ1 (ℓ − ℓcrit ) − σ2 (ℓ − ℓcrit )3 ,                      (32)


                                                       8
where ℓcrit is the value of ℓ at ξcrit . The values of parameters σi and ℓcrit for
various γ are given in Table 2.
                                    Table 2.

The coefficients of Eq.(32) that define the vortex core parameter ℓ.


          γ=1         γ=2        γ=3         γ=4
 ℓcrit   -0.299578    0.00410   0.15429     0.247549
    σ1   0.117906     0.20718   0.261971 0.298006
    σ2   0.264568    0.449719 0.590682 0.701111



3    Vortex Rings


In this section we consider the circular vortex rings that propagate in z−direction
preserving their form. For large vortex rings with the radius R much greater
than the size of the core characterized by the healing length b the energy can
be found by using the energy of the straight line vortex (31) in the region
close to the vortex line and using only the kinetic energy term in the region
away from the vortex line. The sum of these two contributions to energy gives
a simple result (Amit and Gross, 1966; Roberts and Grant, 1971)
                                                     
                           1           8R
                        E = κ2 ρ∞ R ln    −2+ℓ .                             (33)
                           2            b

The momentum of the large vortex ring becomes

                                p = κρ∞ πR2 ez ,                             (34)

where ez is the unit vector in the direction of the ring motion.

The vortex rings and other travelling wave structures that propagate with a
constant velocity correspond to stationary solutions of the SNLS equations in
the frame of reference moving with the velocity of the ring. The wavefunction
satisfies
                 ∂ψ    1                                     
              iU    = ∇2 ψ + |ψ|2(1+γ) − 2ξ|ψ|2 + (1 − 2ξ) ψ.            (35)
                 ∂z    2
We can perform a variation ψ → ψ + δψ in the expressions for momentum
(see Jones and Roberts, 1982)

                        1 Z
                     p=     [(ψ ∗ − 1)∇ψ − (ψ − 1)∇ψ ∗ ] dx                  (36)
                        2i


                                       9
and energy (27) and using (35) show that δE = Uδp, or

                                              ∂E
                                        U=       .                                    (37)
                                              ∂p

We can differentiate Eqs. (33) and (34) with respect to R and after substitution
into Eq. (37) obtain the expression for the velocity of the large vortex ring as
                                                         
                                   κ     8R
                            U=        ln    −1+ℓ .                                    (38)
                                  4πR     b
We can also use the Hamiltonian group relation (37) to derive an alternative
form of the energy functional (27). We substitute z → αz, for a constant α in
Eqs (27) and (36). Then using the variational relationship

                                 ∂
                                   δ (E − Up)     =0                                  (39)
                                ∂α            α=1

gives
                                         Z        2
                                                  ∂ψ
                                   E=                   dx.                            (40)
                                                  ∂z
As the radius of the vortex ring decreases the expressions (33), (34) and (38)
are no longer accurately describe the energy, impulse and velocity of the ring.
The sequence of the small vortex rings and other localized disturbances can
be found numerically by a Newton-Raphson iteration technique. The infinite
domain is mapped by the transformations xb = tan−1 (Dx) and yb = tan−1 (Dy)
to a finite grid (− π2 , π2 )×(− π2 , π2 ). D is a constant chosen to lie in the range D ∼
0.4−0.8. The resulting equations are expressed in second-order finite-difference
form. Taking 2012 grid points in the finite domain, the resulting non-linear
equations are solved by a Newton-Raphson iteration procedure using a banded
matrix linear solver based on the bi-conjugate gradient stabilized iterative
method. The accuracy of the obtained solutions is verified by evaluating the
integral identities (37) and (40).

The families of the travelling wave solutions found are qualitatively similar to
the sequence of such waves found by Jones and Roberts (1982) for the Gross-
Pitaevskii model. They calculated the energy E and momentum p and showed
that the sequence in the p−E plane is given by two branches meeting at a cusp
where p and E assume their minimum values, pm and Em . As p → ∞ on each
branch, E → ∞. On the lower branch the solutions were asymptotic to the
large vortex rings. As E and p decrease from infinity along the lower branch,
the solutions begin to lose their similarity to large vortex rings, and Eqs. (33),
(34) and (38) determine E, p, and U less and less accurately. Eventually,
for a momentum p0 slightly greater than pm , the rings lose their vorticity (ψ
loses its zero), and thereafter the solitary solutions may better be described
as ‘rarefaction waves’. The upper branch consists entirely of these and, as


                                             10
Fig. 4. Families of travelling wave solutions of the subcritical NLS equation (16) for
γ = 1 (red thin solid line), γ = 2 (blue thick solid line), and γ = 3 (black dashed
line) and (a) ξ = 1/2 and (b) ξ = (1 + γ)/(2 + γ). Dots show the positions of the
transition between a vortex ring and a rarefaction pulse on the lower branches. The
critical velocities at which the vortex ring becomes the rarefaction pulse are given
in Table 3.

               100


          E     80


                60       (a)

                40


                20


                 0
                     0         20     40        60        80       100
               100


          E     80

                         (b)
                60


                40


                20


                 0
                     0         20     40        60        80       100

                                            p


p → ∞ on this branch, the solutions asymptotically approach infinitesimal
sound waves. Figure 4 shows the positions of such cusps for the SNLS equations
(16) for two values of ξ: ξ = 1/2 and ξ = (1 + γ)/(2 + γ). The critical velocities
at which the vortex ring becomes the rarefaction pulse are given in Table 3.

In Berloff and Roberts (1999) we discussed how a nonlocal NLS equation with
a higher order nonlinearity brings the vortex core parameter ℓ and the healing
length b into the agreement. We observe that the same harmony is achieved
by the subcritical NLS model (16) for γ = 3. At zero pressure that gives b = 1
Å, the same value as the one found from the sound speed in Section 1. This
also agrees with the experiments of Rayfield and Reif (1964), where the vortex
ring travelling at 27 cm s−1 has the energy 10 eV.
                                   Table 3.


                                           11
The critical velocity of the transition between a vortex ring and a rarefaction
pulse.


    ξ      γ=1 γ=2 γ=3
     1
     2
            0.7    0.91     1.03
    1+γ
    2+γ
            0.45   0.6      0.7



4        Vortex splitting


In this section we discuss a novel mechanism of creating vorticity in super-
fluids. Previously, the semi-classical formation of vortices has been attributed
to one of the four basic mechanisms: due to the existence of critical veloci-
ties (Frisch et al, 1992), due to the transverse instabilities of dispersive waves
(Kuznetsov and Rasmussen, 1995), due to collapse of cavities (Berloff and
Barenghi, 2004), due to energy transfer between waves (Berloff, 2004) and
during the condensation (Berloff and Svistunov, 2002). Here we show that
there exists another mechanism of vortex formation based on the expansion
and collapse of the vortex core.

A negative pressure is generated in superfluid helium II by an ultrasonic trans-
ducer that is used to produce periodic sound pulses (Maris, 1994). This tech-
nique has been extremely successful in detecting electron bubbles in superflu-
ids (Ghosh and Maris, 2005). It has been shown that the tensile strength of
superfluid helium is much less than predicted by theory and this suggests that
the quantized vortices may play a role in the cavitation process.

To consider the dynamics of a straight line vortex and a vortex ring in super-
fluid under the time-varying pressure field, we integrated Eq. (16) numerically
forward in time. We used the 4th order accurate finite difference scheme in
space and the 4th order Runge-Kutta in time.

We start by considering a single straight line vortex under the action of a vary-
ing pressure field controlled by parameter ξ. The pressure oscillates according
to Eq. (17) with
                            ξ(t) = ξ0 + ǫ sin(πt/2η),                        (41)
where ǫ is a small parameter and ξ0 corresponds to the initial zero pressure
ξ0 = (1+γ)/(2+γ). If ξ0 +ǫ ≤ ξcrit, then the vortex never becomes unstable and
the size of the core increases until t = η and decreases back to the unperturbed
value at t = 2η in response to the applied pressure. If ξ0 + ǫ > ξcrit, then the
vortex core continues to increase while pressure is negative. This instability
becomes arrested by the growing positive pressure, so the vortex core returns


                                       12
Fig. 5. Density contour plots of the vortex under the action of periodically varying
pressure field characterized by Eq. (41) with ǫ = 1/20, γ = 1 and η = 100. The
centre of the vortex is seen as black region, intermediate densities are shown in light
gray, larger densities in dark gray.


        t=0                                   t = 200




        t = 300                               t = 400




to the unperturbed value at t = 4η. Figure 5 shows the density contour plots
for the dynamics of the vortex for ǫ = 1/20, γ = 1 and η = 100. The field
around the vortex remains radially symmetric and there is no vortex splitting.
The extra energy gained is emitted by the vortex core radially as sound waves.

To understand the action of the pressure on the vortex we calculated the
energy of the system which in our dimensionless units is (see Eq. (31))
                                     "                  #
                              E = π ln(L/b) + ℓ(t) .                              (42)

Figure 6 shows the plots of ℓ(t) as a function of t. The corresponding values
of pressure are given by dashed line (and magnified by a factor of 100 for
η = 100 and by a factor of 500 for η = 200.). The energy of the system,
characterized by ℓ(t), increases between pressure minimum and maximum. To
follow the evolution of the vortex core we plot the density of the field in the
radial direction on Fig. 7 for ǫ = 1/20, γ = 1 and η = 100. The vortex core
grows while the pressure stays negative (until t = 2η), after that the core


                                         13
Fig. 6. The vortex core parameter ℓ(t) in (42) as a function of time for the dynamics
of the vortex under the action of periodically varying pressure field characterized
by Eq. (41) with ǫ = 1/20 and γ = 1 (solid lines). Dashed line gives the evolution of
pressure given by Eq.(17) magnified by a factor of 100 (top panel) or 500 (bottom
panel).


               15
            ℓ(t)            η = 100
               10



                   5



                   0



               -5
                        0             100    200      300         400
                   80


            ℓ(t)60 η = 200

                   40


                   20


                    0


               -20

                        0             200    400       600         800

                                             time
stabilizes and then decreases in size as pressure increases; see the top panel
of Fig. 7. For positive pressures the core continues to decrease in size while
having an energy density much larger than the energy of the stationary vortex
at a given positive pressure; a large density accumulates at the vortex core at
t = 340; see the bottom panel of Fig. 7. This extra energy is emitted by the
vortex core as outgoing sound wave packet as it tries to regain its stationary
density profile; see t = 350 density profile at the bottom panel of Fig. 7. The
increase in the period of the pressure oscillations leads to qualitatively similar
scenario. The difference is that the energy of the vortex has a longer growth
period and, therefore, reaches larger values; see the bottom panel of Fig. 6.

For the vortices of large radii the effect of the pressure varying field is similar
to that on the straight-line vortex, but the velocity field created by the vortex
loop changes the pressure distribution around the core. The vortex core col-
lapses faster where the velocity is lower leading to the vortex splitting as Figs.


                                            14
Fig. 7. Time snapshots of the density of a straight-line vortex under the action
of varying pressure field characterised by Eq. (41) with ǫ = 1/20. On the top
panel the times are 0, 50, 100, 150, 200, 250, 300; on the bottom panel the times are
300, 310, 320, 330, 340, 350. The thinner lines correspond to later times.

               1.0

            ρ 0.8
               0.6


               0.4


               0.2


               0.0
                     0      10       20        30        40        50

               1.2

               1.0

               0.8

               0.6

               0.4

               0.2

               0.0
                     0      10       20        30        40        50

                                           r



8 and 9 illustrate for γ = 1 and γ = 3 respectively. In both cases we start with
a vortex ring of radius 50 at zero pressure. The parameter ξ varies according
to Eq. (41) with ǫ = 1/20 (for γ = 1), ǫ = 1/10 (for γ = 3) and η = 100.
The vortex ring splits into three rings (two of positive circulation and one ring
with the negative circulation) on Fig. 8. There are many more vortex rings
generated on Fig. 9. We can roughly estimate the number of vortex rings that
will be created by calculating the available energy just before splitting. Under
the action of the pressure field characterized by (41) with ǫ = 1/20, γ = 1
and η = 100, the single straight-line vortex emits sound when ℓ ≈ 8 (seen as a
sharp cusp on Fig. (6)). The total energy available can be estimated from Eq.
(27) and for R = 50 is about 3 times the energy of one vortex ring of radius
50 at zero pressure.


                                          15
Fig. 8. Density contour plots of the cross section of the vortex ring under the action
of periodically varying pressure field characterized by (41) with ǫ = 1/20, η = 100
and γ = 1. The cross-sections of vortex rings are seen as black dots, intermediate
densities are shown in light gray, larger densities in dark gray. An initial vortex
of radius 50b is split into three vortex rings at the end of one period of pressure
oscillations.


        t=0                                   t = 200




        t = 300                               t = 400




5   Conclusions


In summary, we considered the families of straight-line vortices and axisym-
metric vortex rings in the framework of subcritical NLS equations with a
focusing cubic nonlinearity and defocusing higher order term, characterized
by the parameter γ; see Eq. (16). These models can be used to study the ef-
fects of negative pressure in superfluids and capture the dynamics of the many
body systems with attractive two-body interactions such as spin-polarized Li7
(Bradley et al, 1995; Sackett et al, 1998). The strength of the two-body interac-
tions as well as the hydrodynamic pressure are characterized by the parameter
ξ.

We determined the structure and energy of the straight-line vortices and
showed that the vortex becomes unstable to uniform radial expansion when
the slope of the amplitude at the vortex center becomes zero and calculated


                                         16
Fig. 9. Density contour plots of the cross section of the vortex ring under the action
of periodically varying pressure field characterized by Eq.(41) with ǫ = 1/10, γ = 3
and η = 100. The cross-sections of vortex rings are seen as black dots, intermediate
densities are shown in light gray, larger densities in dark gray. An initial vortex
of radius 50b is split into many vortex rings at the end of one period of pressure
oscillations.


        t=0                                   t = 275




        t = 375                               t = 425




the critical value of ξ for this instability. The corresponding critical pressure
for γ = 3 is close to the one obtained by much more sophisticated density-
functional theories. We calculated the energy, impulse and velocity of the
axisymmetric vortex rings and showed the families of the travelling coherent
structures on the impulse-energy plane.

We considered the periodic oscillations of the parameter ξ in time and eluci-
dated its effect on the vortex core. There are three possible scenarios of the
dynamics of the vortex.

1. If the value of ξ never reaches the critical value for the vortex instability,
   then the vortex core simply adjusts to the varying pressure. As pressure
   decreases (increases), the vortex size grows (shrinks).
2. If the value of ξ exceeds the critical value during the time evolution, then
   the vortex core grows while pressure stays negative and continues to do so
   until shortly before pressure reaches its maximum positive value. After that


                                         17
   the vortex core shrinks and the extra energy is emitted as outgoing sound
   waves.
3. Same as in item 2, but in the presence of large variations of the velocity
   field around the core, such as in the case of the vortex rings, the vortex core
   breaks into odd number of vortices (vortex rings) to preserve the total unit
   of circulation of ±1 around the initial vortex.

Finally, we suggest that the processes of the vortex instability and vortex
splitting can be seen in trapped BECs where the magnitude and sign of the
scattering length, which is represented by ξ in our model, are changed by
Feshbach resonance. In particular, our results indicate that there is a critical
value of the interatomic attractive interactions for which a straight-line vortex
becomes unstable. It seems likely that this instability can be arrested by the
presence of a harmonic trapping potential. By periodically varying the sign
and the magnitude of the two-body interactions in the trapped BEC it may
be possible to produce the vortex spitting if the trap is not too close to being
perfectly axisymmetric.



Acknowledgments


The author gratefully acknowledges the financial support from the EPSRC-
UK and useful discussions with Humphrey Maris.



References

Amit D. and Gross E. P. 1966. Vortex Rings in a Bose Fluid, Phys. Rev. 145,
  130.
Berloff N.G and Roberts P. H. 1999. Motions in a Bose condensate VI. Vortices
  in a nonlocal model , J. of Phys. A: Math. and Gen., 32, 1-15.
Berloff N.G. and Barenghi C.F., 2004. Vortex nucleation by collapsing bubbles
  in Bose-Einstein condensates, Phys. Rev. Lett., 93, 090401.
Berloff N.G. 2004. Pade approximations of solitary wave solutions of the Gross-
  Pitaevskii equation, J. of Phys. A: Math. and Gen., 37, 1617 - 1632.
Berloff N.G. and Svistunov B. V. 2002. Scenario of strongly non-equilibrated
  Bose-Einstein condensation, Phys. Rev. A, 66, 013603.
Bradley C.C., Sackett C. A., Tollett J. J., and Hulet R. G. 1995. Evidence of
  Bose-Einstein Condensation in an Atomic Gas with Attractive Interactions,
  Phys. Rev. Lett. 75, 1687.
Dalfovo F, 1992. Structure of vortices in helium at zero temperature, Phys.
  Rev. B 46, 5482 - 5488.


                                       18
Frisch T, Pomeau Y, and Rica S 1992. Transition to dissipation in a model of
  superflow, Phys. Rev. Letts. 69 1644-1648.
Jones C A and Roberts P H 1982. Motions in a Bose condensate: IV. Axisym-
  metric solitary waves, J. Phys. A: Gen. Phys. 15 2599 -2619.
Josserand C., Pomeau Y., and Rica S., 1995. Cavitation versus Vortex Nucle-
  ation in a Superfluid Model. Phys. Rev. Lett. 75, 3150.
Josserand C. and Rica S. 1997. Coalescence and Droplets in the Subcritical
  Nonlinear Schrdinger Equation, Phys. Rev. Lett. 78, 1215.
Ghosh A. and Maris H. J. 2005. Observation of a New Type of Electron Bubble
  in Superfluid Helium, Phys. Rev. Lett. 95, 265301.
Khaykovich L. and Malomed B. A., 2006. Deviation from one dimensionality
  in stationary properties and collisional dynamics of matter-wave solitons,
  Phys. Rev. A 74, 023607.
Kivshar Yu. S. and Agrawal G., Optical Solitons: From Fibers to Photonic
  Crystals (Academic Press, San Diego, 2003).
Kuznetsov E.A. and Juul RasmussenJ. 1995. Instability of two-dimensional
  solitons and vortices in defocusing media, Phys. Rev. E 51, 4479.
Maris H. J. and Xiong Q. 1989. Nucleation of bubbles in liquid helium at
  negative pressure, Phys. Rev. Lett. 63, 1078;
Maris H.J. 1994. Nucleation of Bubbles on Quantized Vortices in Helium-4, J.
  Low Temp. Phys. 94, 125-144.
Nissen J. A., Bodegom E. and Semura J. S., 1989. Tensile strength of liquid
  4He, Phys. Rev. B 40, 6617.
Rayfield G. W and Reif F. 1964. Quantized Vortex Rings in Superfluid Helium,
  Phys. Rev. 136, A1194-1208.
Roberts P. H. and Grant J. 1971, Motions in a Bose condensate. I. The struc-
  ture of the large circular vortex, J. Phys. A: Gen. Phys. —bf 4, 55-72.
Sackett A., Stoof H.T., and Hulet R.G.1998. Growth and Collapse of a Bose-
  Einstein Condensate with Attractive Interactions, Phys. Rev. Lett. 80, 2031.
Sinha S., Cherny A. Yu., Kovrizhin D., and Brand J. 2006. Friction and Dif-
  fusion of Matter-Wave Bright Solitons, Phys. Rev. Lett. 96, 030406.
Xiong Q. and Maris H. J. 1989. Liquid helium at negative pressures: Nucleation
  of bubbles and anomalous phonon dispersion, J. Low Temp. Phys. 77, 347;
  82, 105 (1991)




                                     19
