                                                        Quantum Algorithms Using the Curvelet Transform
                                                                                          Yi-Kai Liu
                                                                             Institute for Quantum Information
                                                                              California Institute of Technology




arXiv:0810.4968v2 [quant-ph] 25 Mar 2009
                                                                                     Pasadena, CA, USA
                                                                                   yikailiu@caltech.edu

                                                                                         Mar. 25, 2009


                                                                                            Abstract
                                                     The curvelet transform is a directional wavelet transform over Rn , which is used to analyze
                                                 functions that have singularities along smooth surfaces (Candès and Donoho, 2002). I demon-
                                                 strate how this can lead to new quantum algorithms. I give an efficient implementation of a
                                                 quantum curvelet transform, together with two applications: a single-shot measurement proce-
                                                 dure for approximately finding the center of a ball in Rn , given a quantum-sample over the ball;
                                                 and, a quantum algorithm for finding the center of a radial function over Rn , given oracle access
                                                 to the function. I conjecture that these algorithms succeed with constant probability, using one
                                                 quantum-sample and O(1) oracle queries, respectively, independent of the dimension n — this
                                                 can be interpreted as a quantum speed-up. To support this conjecture, I prove rigorous bounds
                                                 on the distribution of probability mass for the continuous curvelet transform. This shows that
                                                 the above algorithms work in an idealized “continuous” model.


                                           1    Introduction
                                           One of the most remarkable demonstrations of the power of a quantum computer is Shor’s algorithm
                                           for factoring and discrete logarithms [26]. This has motivated many researchers to try to generalize its
                                           key components—the quantum Fourier transform over ZN , and the algorithm for period-finding—to
                                           solve other problems [13]. In particular, this motivated the study of the quantum Fourier transform
                                           and the hidden subgroup problem (HSP) on non-Abelian groups, as a route to solving certain lattice
                                           problems and the graph isomorphism problem [23, 3, 25].
                                               In this paper we study a different generalization of the Fourier transform, namely the curvelet
                                           transform over Rn [10]. This is a kind of “directional” wavelet transform, which can resolve features
                                           over the spatial and frequency domains simultaneously. A curvelet basis function resembles a wave-
                                                                                                                             ~
                                           packet, with high-frequency oscillations in one direction (like a plane wave eik·~x , as in the Fourier
                                           transform on Rn ), but which is also supported on a small region of space (unlike the plane wave).
                                           We show that this leads to fast quantum algorithms for some new classes of problems, outside the
                                           framework of the HSP. To the best of our knowledge, this is the first attempt to design quantum
                                           algorithms based on the curvelet transform.
                                               Intuitively, the curvelet transform is helpful in analyzing functions on Rn that are discontinuous
                                           along (n−1)-dimensional surfaces. If a function f is discontinuous along a surface S, then its curvelet
                                           transform Γf will be “large” at those locations (~b, ~ θ), where ~b is a point on S and θ~ is the vector
                                                            ~                            ~  ~
                                           normal to S at b. The set of all such pairs (b, θ) is called the “wavefront set” of f .


                                                                                                 1
    The basic model P for a quantum algorithm using the curvelet transform is as follows: first prepare
a quantum state ~x∈Rn f (~x)|~xi, which is a weighted superposition of points in Rn ; then apply the
quantum curvelet transform, to get the state ~b,θ~ Γf (~b, ~
                                                           θ)|~b, ~θi; and finally measure ~b and ~
                                                 P
                                                                                                   θ. For the
                                                                                 n
time being, we ignore implementation issues, such as how to discretize R and how to compute the
quantum curvelet transform efficiently. The more basic question is whether we can find functions f
such that we can prepare the initial state efficiently, and such that a measurement in the “curvelet
basis” yields useful information.
    One example consists of letting f be the indicator function of a ball in Rn . We can efficiently
prepare a uniform superposition over points in a ball, using the techniques of [2, 17]. (This is called
“quantum-sampling,” and it can be done more generally, e.g., for convex bodies.) Then, measuring
in the curvelet basis extracts information about the center of the ball.
    Another example consists of choosing f to be the indicator function of a spherical shell in Rn .
This is motivated by the problem of finding the center of a radial function on Rn . Let G be a radial
function, centered around some unknown point ~c. Prepare a uniform superposition over a large
region of space, then compute G(~x) and measure it; this produces a uniform superposition over one
of the level sets of G, which is a spherical shell centered at ~c. Then, measuring in the curvelet basis
extracts information about the location of ~c.
    The goal of this paper is to make this intuition precise. We can interpret Γf as a wavefunction,
and we want to show that its probability mass |Γf |2 is concentrated near the wavefront set. We
can prove this for the continuous curvelet transform, for the two cases of interest, where f is the
indicator function of a ball or a spherical shell in Rn . In these cases, (~b, ~θ) is near the wavefront set
                                                      ~    ~
with high probability. This implies that the line {b + λθ | λ ∈ R} passes near the center of the ball
or spherical shell.
    Next, we give an efficient implementation of a quantum curvelet transform. (This is a dis-
crete version of the transform described above, acting on superposition states.) Then we propose
polynomial-time quantum algorithms for two problems: (1) given a single quantum-sample over a
ball in Rn , find the center of the ball, with accuracy ±∆ where ∆ is a constant fraction of the radius
of the ball; (2) given oracle access to a radial function f that is centered around some unknown
                                                                                          1
point ~c ∈ Rn , find the point ~c exactly (i.e., with accuracy ±∆ in time poly(log ∆        ), assuming that
the function f fluctuates on sufficiently small scales).
    For the first problem, we conjecture that our quantum procedure succeeds with constant prob-
ability, while the best classical procedure succeeds with probability that is exponentially small in
n. Classically, this problem is hard because the volume of a ball in Rn is concentrated near its
surface. But this same fact is helpful to the quantum curvelet transform, which works by finding a
line normal to the surface of the ball.
    For the second problem, we conjecture that our quantum algorithm uses only a constant number
of queries, whereas any classical algorithm requires Ω(n) queries. Intuitively, this is because the
curvelet transform uses constructive interference to find a direction in Rn from just one query.
    We then prove that these algorithms work in an idealized “continuous” model — this follows
from our rigorous results on the continuous curvelet transform. However, we do not have a rigorous
analysis of the effects caused by discretization, though we can argue that these should be small.
    These examples demonstrate that one can use the curvelet transform to obtain a quantum speed-
up. These examples are artificially simple, in order to allow a rigorous analysis. But the underlying
idea—using the curvelet transform to find normal vectors to a surface—should work on more com-
plicated geometric objects.

1.1 Technical Contributions: First, in Section 2, we define the continuous curvelet transform over


                                                     2
Rn . This generalizes the definition over R2 given in [8]. Given a function f (~x), the continuous curvelet
transform returns a function Γf (a, ~b, ~  θ). Here, ~x ∈ Rn represents a “location,” while 0 < a < 1 is a
“scale” (smaller values denote finer scales, larger values denote coarser scales), ~b ∈ Rn is a “location,”
and θ~ ∈ S n−1 (the unit sphere in Rn ) is a “direction.”
    Next, we study the distribution of probability mass |Γf |2 over different values of (a, ~b, θ).
                                                                                                 ~ This is
technically quite difficult. Γf (a, ~b, θ)
                                        ~ is defined by an oscillatory integral, and while there are various
methods for bounding the asymptotic decay rates of such quantities [28, 7], we need non-asymptotic
bounds on the total probability mass in a given region. In Section 3 we develop some tools for proving
such bounds, in the case where f is a radial function. Then, in Sections 4 and 5, we specialize to
the case where f is the indicator function of a ball or a spherical shell. Here, the analysis relies on
powerful classical results that bound the oscillation and decay of Bessel functions [1, 30].
    In Section 4 we let f be the indicator function of a ball in Rn , with radius β, centered at the
origin. We expect that, after applying the curvelet transform, ~b and θ~ will be concentrated near the
wavefront set of f : that is, ~b will be concentrated near the line {λ~θ | λ ∈ R}, at about distance β from
the origin. Furthermore, we expect that ~b will become more tightly concentrated, the smaller the
value of a. We show that this is essentially what happens. In particular, with constant probability,
the distance from ~b to the line {λ~    θ | λ ∈ R} will be at most a constant fraction of β; remarkably,
this holds independent of the dimension n.
    In Section 5, we let f be supported on a thin spherical shell, having radius β and thickness
δ ≪ β. Here, after applying the curvelet transform, we get a qualitatively similar behavior of a, ~b
and θ.~ Quantitatively, however, we find that we can observe much smaller scales a, on the order of
δ/β; and thus we can find the center of the shell with much greater precision. Essentially, by making
the shell extremely thin, we can find its center with arbitrarily high precision.
    Finally, we turn to the discrete curvelet transform, and quantum algorithms. In Section 6 we
give an efficient implementation of a quantum curvelet transform. This uses ideas from the fast
classical curvelet transform [6]. However, there is a new complication in the quantum case: we need
to prepare certain states which are superpositions of different scales and directions (a, θ). ~ We design
families of curvelets that allow this step to be performed efficiently, and that have similar analytic
properties to the curvelets used in Sections 3-5.
    In Section 7, we formally define the two problems mentioned earlier: estimating the center of a
ball, given a single quantum-sample state; and finding the center of a radial function, given oracle
access. We present quantum algorithms for these problems, and use our results from Sections 4 and
5 to prove that the algorithms work in a continuous model. We also sketch a classical lower bound
for finding the center of a radial function.
    This paper omits most of the proofs, due to lack of space. The proofs can be found in the full
version [21]. Also, note that this paper contains some additional results there were not present in
the first version of [21]. This paper contains an improved algorithm for finding the center of a radial
function, and a classical lower bound for that problem.

1.2 Related Work: Curvelets over R2 and R3 have been studied as a tool for image processing
and simulating wave propagation [10, 9, 6, 20]. The curvelet transform is also related to older ideas
from harmonic analysis; see, e.g., Smith [27]. It can be viewed as an algorithmic implementation of
a technique known as second dyadic decomposition [28].
    There are a few rigorous results on the behavior of the curvelet transform which are similar in
spirit to our work [10, 7, 8, 5]. These results apply to much broader classes of functions, but they are
only known to hold over R2 (or R3 in some cases). Although one would expect them to generalize in
some fashion to Rn , it is perhaps surprising that the scaling with n is as favorable as we find here.


                                                     3
    In connection with quantum algorithms, there has been some work on the quantum wavelet
transform [31, 15, 32, 16]. But the curvelet transform on Rn is quite different from the “ordinary”
wavelet transform on Rn , which consists of a product of 1-D transforms. The ordinary wavelet
transform on Rn can detect the locations of discontinuities, but it cannot resolve directions.
    The geometric problems studied in this paper are reminiscent of some recent work on finding
hidden nonlinear structures, although the details are different. Shifted subset problems [12, 22]
involve translational invariance, so the natural tool for solving them is the Fourier transform, rather
than curvelets. Hidden polynomial problems [12, 14] resemble our problem of finding the center of
a radial function. However, they are much more general (and thus much harder), and they are set
over a finite field rather than Rn .
    These problems can also be studied from the perspective of quantum state discrimination [11],
e.g., what is the optimal quantum measurement for estimating the center of a ball? However, we
stress that our algorithms using the quantum curvelet transform are computationally efficient.
    Finally, we recently became aware of a quantum algorithm for estimating the gradient of a
function f on Rn , using only O(1) queries [19]. This is quite similar to our algorithm for finding the
center of a radial function — it is like applying the curvelet transform at a single location ~b. Viewing
this as a curvelet transform has the advantage of providing a more general framework, where one
can do this procedure on an arbitrary input state. Also, note that our emphasis in this paper is on
functions f that are not smooth—in this case, the gradient is not well-defined.


2    The Continuous Curvelet Transform
We begin by defining the continuous curvelet transform over Rn . This generalizes the definition of
[8] over R2 . Given a function f (~x), the continuous curvelet transform returns a function Γf (a, ~b, θ).
                                                                                                       ~
Here, ~x ∈ Rn represents a “location,” while 0 < a < 1 is a “scale” (smaller values denote finer scales,
larger values denote coarser scales), ~b ∈ Rn is a “location,” and ~θ ∈ S n−1 (the unit sphere in Rn ) is
a “direction.” All functions return values in C.
    Intuitively, the curvelet transform decomposes f into pieces corresponding to different scales a
                ~ we can view Γf (a, ~b, θ)
and directions θ;                        ~ as a family of functions, indexed by a and θ,
                                                                                      ~ each representing
some “piece” of f (~x) (note that the variables ~b and ~x both represent locations in space). To get one
such piece of f , we will take its Fourier transform, and then multiply by a “window function” χa,θ~
which is defined over the frequency domain.
    More precisely, the curvelet transform is defined to be
                                                 Z
                                        ~  ~                             ~~
                                 Γf (a, b, θ) :=     fˆ(~k)χa,θ~ (~k)e2πik·b d~k.                     (1)
                                                Rn

Here, fˆ is the Fourier transform of f , and χa,θ~ is a function that is smooth, real, non-negative, and
supported on a “sector” of frequency space Sa,θ~ ⊂ Rn . We will describe these sectors below. Before
doing so, we remark that the curvelet transform consists of (1) taking the Fourier transform of f , (2)
separating fˆ into pieces corresponding to different scales and directions, and (3) taking the inverse
Fourier transform. This description suggests how to compute the curvelet transform efficiently.
    The “sector” Sa,θ~ is roughly given by the intersection of the cone centered around the vector
~θ with angular width √a, and the annulus with inner radius 1/a and outer radius 2/a. Thus, the
“piece” of f at scale a and direction θ~ is somewhat like the restriction of fˆ to frequencies ~k ≈ (1/a)θ~
(which represent oscillations in direction ~θ, at higher frequencies when the scale a is small). Note,



                                                     4
                                                       √
however, that the sector has dimensions 1/a × (1/ a)n−1 , so its shape is not constant — the sector
becomes longer and narrower when the scale a is small.
   This construction can also be understood from a second perspective. We can define a family of
curvelet basis functions γa,~b,θ~ as follows. The curvelet at location ~b is obtained by translation from
the curvelet at location ~0, that is, γ ~ ~ (~x) := γ ~ ~(~x − ~b). The curvelet at location ~0 is defined in
                                         a,b,θ        a,0,θ
terms of its Fourier transform, which is simply the window function χa,θ~ , that is, γ̂a,~0,θ~ (~k) := χa,θ~ (~k).
It is easy to check that the curvelet transform defined earlier is equivalent to taking inner products
with this family of curvelet basis functions: Γf (a, ~b, θ)
                                                          ~ = hγ ~ ~ , f i.
                                                                   a,b,θ
     Now we can see how our choice of the window function χa,θ~ implies (and is motivated by) certain
properties of the curvelet basis functions γa,~b,θ~ . Since χa,θ~ is smooth, the γa,~b,θ~ are rapidly decaying.
Also, each γa,~b,θ~ has high-frequency oscillations in the ~θ direction, and is essentially supported on a
                                                                                           √
plate-like region, centered at location ~b, orthogonal to ~  θ, with dimensions a × ( a)n−1 . Intuitively,
γa,~b,θ~ resembles a plane-wave in direction ~θ, localized around the point ~b.
     Finally, we define the window function χ ~ as follows. Write ~k using spherical coordinates
                                                     a,θ
(r, φ1 , . . . , φn−1 ), centered around the direction ~θ, so that φ1 is the angle between ~k and ~θ. Then
                                        √
define χa,θ~ (~k) := W (λar)V (φ1 / a)Λa (φ1 ). Here λ is a constant, which can be chosen freely; we
will explain how to set it later. W is a radial window function,          R ∞real, nonnegative,   supported on
                                                                                    2 dr
the interval [1/e, 1], and satisfying the admissibility condition 0 W (r) r = 1. V is an angular
window function,         real, nonnegative, supported on the interval [0, π/2], and satisfying the admissibility
condition S n−1 V (φ1 )2 dσ(φ1 , . . . , φn−1 ) = 1, where dσ denotes integration over the unit sphere S n−1
                R

in Rn .                                                                                  √ √ (n−2)/2
                                                                                       1 / a) a
     Λa is a normalization and adjustment factor: Λa (φ1 ) := a(n+1)/4 sin(φsin(φ          1)
                                                                                                       . This is
needed because the volume of the sector Sa,θ~ (on which χa,θ~ is supported) changes with a. Note
that, when φ1 is small, Λa (φ1 ) ≈ a(n+1)/4 . This is the main point where defining curvelets over Rn is
more complicated than over R2 ; note that in dimension n = 2, Λa (φ1 ) = a(n+1)/4 = a3/4 exactly. We
remark that a simpler approach would be to use a constant normalization factor that only depends
on a and not φ1 ; however, our more complicated construction will be more convenient in the later
sections of this paper.
     We now state some basic properties of the curvelet transform. First, note that the curvelet
transform works primarily on the high-frequency components of f , which correspond to fine-scale
elements (a small). The constant factor λ, mentioned above, sets the low-frequency cutoff value,
which corresponds to the coarsest scale (a = 1). For convenience, here we assume that f has
no low-frequency components below the cutoff value. In practice, when f has such low-frequency
components, the curvelet transform leaves them unchanged, and simply returns them as a residual
function fres .
                                                                  ~ dσ(θ)
                                                                       ~
     Next, we define the reference measure dµ(a, ~b, ~θ) := da dabn+1     . This weights the contributions
of Γf (a, ~b, ~
              θ) differently according to the scale a. Intuitively, this is needed because the sectors
Sa,θ~ do not cover the frequency domain uniformly, and the translations of a curvelet γa,~0,θ~ (for
fixed a and ~   θ) to different locations ~b do not cover the spatial domain uniformly. Rather, (a, ~b, θ)
                                                                                                        ~
                                                                            d~b        ~
                                                                                    dσ(θ)
should be “sampled” in a certain way. To see this, write dµ(a, ~b, θ)
                                                                   ~ = da (n+1)/2
                                                                       a a        a(n−1)/2
                                                                                           . Note that
da
 a = d(log a), suggesting that we should sample log(a) at uniform intervals, i.e., we √   should set a
                                       ~
equal to powers of 2; we should sample b on a grid in R whose cells have size a × ( a)n−1 ; and
                                                         n
                                                                √
we should sample θ~ on a mesh on S n−1 whose cells have size ( a)n−1 . Later, when we construct


                                                           5
                                                                           ~ in place of the reference
the discrete curvelet transform, we will use this sampling trick for a and θ,
measure.
   Then we have the following theorems:
                            ˆ~                      ~
Theorem 1 Suppose that R f (k) = 0 for all |k| < 1/λ. Then we can recover f from its curvelet
transform Γf : f (~x) = a<1 Γf (a, b, θ)γa,~b,θ~(~x)dµ(a, ~b, θ).
                                  ~   ~                       ~


      R 2 Suppose
Theorem                that fˆ(~k) = 0 for all |~k| < 1/λ. Then the curvelet transform preserves the L2
norm: Rn |f (~x)|2 d~x = a<1 |Γf (a, ~b, θ)|
                                         ~ 2 dµ(a, ~b, θ).
                                                       ~
                         R


These are straightforward generalizations (to the case of Rn ) of results in [8]. We sketch the proofs
in Appendix A.


3    The Curvelet Transform of a Radial Function
|Γf (a, ~b, ~θ)|2 dµ(a, ~b, θ)
                            ~ can be interpreted as a probability density over the different scales, locations
and directions (a, ~b, θ).   ~ In this section we will develop some tools for understanding where this
probability mass is concentrated. We will consider the case where f has rotational symmetry. Though
there is no simple analytic expression for Γf , we can deduce certain properties from symmetry, and
we can upper-bound the variance of ~b (this latter point is our main result).
     Let f be a radial function,
                               R∞       f (~x) = f0 (|~x|). Its Fourier transform is also radial, fˆ(~k) = F0 (|~k|),
                         2π
where F0 (ρ) = ρ(n−2)/2 0 J(n−2)/2 (2πρr)f0 (r)r n/2 dr, and J is a Bessel function (see, e.g., [29]). We
assume that f is normalized so that Rn |f (~x)|2 d~x = 1.
                                               R

     When f is radial, Γf has the following symmetries: Γf (a, ~b, ~θ) = Γf (a, −~b, −~θ), and for any
rotation R, Γf (a, ~b, θ)   ~ = Γf (a, R(~b), R(~θ)).
     We make a particular choice for the radial and angular windows W and V . These windows are
C smooth, which is necessary in our analysis of the variance of ~b. We let W (r) = [Cw sin(π p
   1                                                                                                        log r)2
if 1/e ≤ r q                                                  2
               ≤ 1; 0 otherwise] and V (t) = [Cv cos(t) if 0 ≤ t ≤ π/2; 0 otherwise], where Cw = 8/3,
              2(n+2)n
and Cv =        3S0 .

3.1 The probability of observing a scale a: First, we claim that the probability of observing
a fine-scale element a ≤ η isR essentially given by the amount
                                                             R of probability   mass of fˆ at frequencies
                                          ~ ~  2     ~ ~                  ˆ ~ 2 ~
above 1/(λη): Pr[a ≤ η] = a≤η |Γf (a, b, θ)| dµ(a, b, θ) ≥ |~k|≥1/(λη) |f (k)| dk. This follows from the
same argument used to prove Theorem 2. In the case of a radial function, we write this as:
                                                  Z ∞
                                  Pr[a ≤ η] ≥ S0         F0 (ρ)2 ρn−1 dρ,                             (2)
                                                        1/(λη)

           2π    n/2
where S0 = Γ(n/2) is the surface area of the sphere S n−1 ⊂ Rn .

3.2 The location ~b and direction θ:      ~ We claim that the location ~b has expectation value ~0. To
see this, observe that E(bj ) = −E(bj ), due to the reflection symmetry of Γf ; thus E(bj ) = 0. Note
that this remains true when we condition on the value of a.
    Also, we claim that the direction ~    θ is uniformly distributed. This follows from the rotational
symmetry of Γf . Note that this remains true when we condition on the value of a, and when we
condition on the value of ~b · θ~ (since this preserves the rotational symmetry).


                                                         6
3.3 The variance of ~b perpendicular to θ:        ~ Finally, we seek to upper-bound the variance of ~b, in
the directions perpendicular to ~    θ, as well as parallel to ~  θ. These results are rather complicated, so
we defer most of the details to Appendix B.1. However, these results are a basic component of our
proofs in Sections 4 and 5, so we will sketch some of the calculations.
   First, the variance of ~b perpendicular to ~θ is:
                                            Z 1Z
                                                                                             da
                                      Z
              E(~bT (I − θ~θ~T )~b) =               (~bT (I − θ~θ~T )~b)|Γf (a, ~b, ~
                                                                                    θ)|2 d~b n+1 dσ(~θ).  (3)
                                       S n−1 0   Rn                                         a
Note that a similar formula holds when we condition on observing a ≤ η.
    We can take advantage of rotational symmetry to do the θ~ integral. Fix a vector ~u = (1, 0, . . . , 0),
and for each ~θ, let R be a rotation that maps θ~ to ~u. Then we can replace the expression inside
the integral with (R(~b)T (I − ~u~uT )R(~b))|Γf (a, R(~b), ~u)|2 . Then change variables ~b 7→ R−1 (~b). The
integrand is now independent of ~   θ, so we can do the θ~ integral. We get:
                                           Z 1Z
                     ~       ~~                                                               da
                       T        T ~
                   E(b (I − θθ )b) = S0             (~bT (I − ~u~uT )~b)|Γf (a, ~b, ~u)|2 d~b n+1 .       (4)
                                             0   Rn                                          a
     Now the key idea is to replace integration over the spatial domain with integration over the
 frequency domain, via Plancherel’s theorem. (Recall that curvelets are defined more simply over the
 frequency domain.) We introduce some new notation, Φa,θ~ (~b) := Γf (a, ~b, θ).       ~ By equation (1), the
 Fourier transform of Φa,θ~ is given by Φ̂a,θ~(~k) = fˆ(~k)χa,θ~ (~k).
                                                                                      Pn R          2       ~ 2 ~
     Let IK denote the innermost integral in equation (4). Then IK =                    j=2 Rn |bj | |Φa,~
                                                                                                         u (b)| db.
 Using P
       Plancherel’s       theorem, and symmetryR with respect to rotations around the ~u axis, we can write
 IK = nj=2 Rn | 2πi     1 ∂           ~ 2 ~      n−1        ∂        ~ 2 ~
                R
                                   u (k)| dk = (2π)2 Rn | ∂k2 Φ̂a,~
                           ∂kj Φ̂a,~                              u (k)| dk.
     We can expand out the integral on the right hand side, as follows. Using spherical coordinates
~k = (r, φ1 , . . . , φn−1 ), we write Φ̂a,~u (~k) as a product of a radial part and an angular part: Φ̂a,~u (~k) =
                                                                           √
 L(r)M (φ1 ), where L(r) = F0 (r)W (λar), and M (φ1 ) = V (φ1 / a)Λa (φ1 ). Then we have
                               ∂         ~     ′           ∂r         ′      ∂φ1
                              ∂k2 Φ̂a,~
                                      u (k) = L (r)M (φ1 ) ∂k2 + L(r)M (φ1 ) ∂k2 ,                             (5)

      ∂r
where ∂k 2
           = sin φ1 cos φ2 , and ∂φ 1
                                 ∂k2 =
                                       cos φ1 cos φ2
                                             r       . So we get: (note that Φ̂a,~u (~k) is real)
                                                     Z ∞
                                 n−1
                                           Z
                            IK =                         L′ (r)M (φ1 ) sin φ1 cos φ2 +
                                 (2π)2       S n−1    0
                                                                            2                                 (6)
                                               ′
                                     L(r)M (φ1 )r      −1
                                                            cos φ1 cos φ2        r   n−1        ~
                                                                                           drdσ(φ).

  We can then upper-bound these integrals in terms of F0 (the radial component of fˆ). See
Appendix B.1 for details. The final result is:

                      E(~bT (I − θ~θ~T )~b | a ≤ η)
                                                                   Z ∞
                                1        n−1           h
                        ≤                       S  0 ·   1
                                                         2 (n − 2)           F0 (r)2 r n−3 dr
                            Pr[a ≤ η] (2π)2                         1/(ληe)
                                Z ∞                                     Z ∞                                  (7)
                                                 ′     2 n−2
                             5
                        + n−1 λ   1
                                               F0 (r) r       dr + λ17
                                                                                  F0 (r)2 r n−4 dr
                                      1/(ληe)                             1/(ληe)
                                                    Z ∞                       i
                        + (2n + 9 + n−3    10
                                              )eλ             F0 (r)2 r n−2 dr .
                                                     1/(ληe)


                                                               7
In sections 4 and 5, we will explain how this is used.

3.4 The variance of ~b parallel to ~
                                   θ: In a similar way, we can upper-bound the variance of ~b · ~
                                                                                                θ.
See Appendix B.2 for details.


4     The Ball in Rn
Let B be a ball in p  Rn , of radius β. In this section we will analyze the curvelet transform of the
function f (~x) = [1/ vol(B) if ~x ∈ B, 0 otherwise]. This is the wavefunction one gets by quantum-
sampling over B.
    We assume n ≥ 4, and we use the window functions W and V specified in Section 3. We set the
parameter λ to lie in the range 2πβe/n ≤ λ ≤ 2 · 2πβe/n. We show the following:
Theorem 3 Almost all of the power in fˆ is located at frequencies |~k| ≥ 1/λ: |~k|≤1/λ |fˆ(~k)|2 d~k < πn
                                                                                                        1
                                                                              R
                                                                                                          .
                    2
For any η ≤ 1/e , the probability of observing a fine-scale element a ≤ η is lower-bounded by:
Pr[a ≤ η] ≥ 14  eη
                   (1 − n1 ). Furthermore, if η ≤ (1/2e2 )(1 − n+22
                                                                    ), then the variance of ~b, in the
directions orthogonal / parallel to ~θ, conditioned on a ≤ η, is upper-bounded by:

                              E(~bT (I − ~
                                         θ~
                                          θ T )~b | a ≤ η) ≤ ηβ 2 (14300 + O( n1 )),                         (8)

                                   E((~b · ~
                                           θ)2 | a ≤ η) ≤ β 2 (242 + O( n1 )).                               (9)
      The first claim shows that only an inverse-polynomial fraction of the probability mass lies below
 the low-frequency cutoff; this justifies our use of the curvelet transform and Theorems 1 and 2. The
 second claim shows that, for any sufficiently small constant η, we observe scale a ≤ η with constant
 probability. This is due to the fact that fˆ has a lot of power at high frequencies (a “heavy tail”),
 which is caused by the discontinuity of f along the surface of the ball. (For comparison, one would
 not observe this behavior if f were, say, a Gaussian.) The third claim shows that, when a ≤ η, ~b lies
                       √                                                                                 ~ Also,
 within distance O( ηβ) of the line that passes through the center of the ball with direction θ.
~b lies within distance O(β) of the center (and we expect, though we do not prove, that this distance
 is also lower bounded by Ω(β)).
      As mentioned previously, it is remarkable that these bounds do not depend on the dimension
 n. It is also interesting that this concentration of probability mass can hold even when the window
 function χa,θ~ is only C 1 -smooth. By contrast, in order for Γf to be asymptotically rapidly decaying,
 χa,θ~ must usually be C k or C ∞ -smooth.
      We prove this using our results from Section 3. Note that the curvelet transform behaves in a
 simple way when we translate the function f : if g(~x) = f (~x − z~), then using equation (1), we see
 that Γg (a, ~b, ~
                 θ) = Γf (a, ~b − ~z, ~
                                      θ). Thus, without loss of generality, we can assume that the ball B is
 centered at the origin. In this case f is a radial function.
      We will be interested in the Fourier       transform of f . We write f (~x) = f0 (|~x|), where f0 (r) = [C
 if r ≤ β, 0 otherwise], and C = 1/ vol(B) = (S0 β n /n)−1/2 , where S0 is the surface area of the unit
                                          p

 sphere S n−1 in Rn . Then the Fourier transform of f is given by fˆ(~k) = F0 (|~k|), where
                                                    q
                                                          1
                                           F0 (ρ) = Sn0 ρn/2 Jn/2 (2πρβ),                                    (10)

                                                       d
using the definition from Section 3, and the identity dz (z ν Jν (z)) = z ν Jν−1 (z) (see [1], eqn. (9.1.30)).
    The behavior of F0 (ρ) depends on the behavior of the Bessel function Jν (z) when ν ≥ 0 and
z ≥ 0. Jν (z) is very small when z ≪ ν, it undergoes a transition near z ≈ ν, and it is approximately

                                                        8
given by 2/(πz) cos(z − 12 νπ − 41 π) when z ≫ ν (see [1]). Thus, our intuition is that F0 (ρ) ≈ 0 when
          p

ρ . (n/2)/(2πβ), and F0 (ρ) ≈ (const)/ρ(n+1)/2 times an oscillating factor when ρ & (n/2)/(2πβ).
     We now sketch the proof, omitting the details. First we choose λ ≈ (const)·(2πβ)/n, so that very
little power lies at frequencies below 1/λ. Substituting into (2), we get that Pr[a ≤ η] ≈ (const) · η.
     Then we bound the variance of ~b perpendicular to θ, ~ as follows. (A similar argument holds for
the variance of ~b · ~
                     θ.) We start with (7), and use the fact that r ≥ 1/(ληe) implies r · ληe ≥ 1:

                E(~bT (I − θ~θ~T )~b | a ≤ η)
                                                                  Z ∞
                          1        n−1         h
                                                                2
                  ≤                              1
                                          S0 · 2 (n − 2)(ληe)               F0 (r)2 r n−1 dr
                      Pr[a ≤ η] (2π)2                               1/(ληe)
                                 Z ∞                                    Z ∞
                                                                      3
                                                                                                
                       5    ληe              ′    2 n−1      17(ληe)                    2 n−1
                  + n−1 λ                  F0 (r) r     dr +      λ              F0 (r)  r    dr
                                   1/(ληe)                               1/(ληe)
                                                   Z ∞                      i
                  + (2n + 9 + n−3    10
                                        )eλ(ληe)           F0 (r)2 r n−1 dr .
                                                    1/(ληe)
                                                      q
                                                          n −n/2
A standard calculation shows that F0′ (r) = −             S0 r   J(n/2)+1 (2πβr)(2πβ), which behaves simi-
larly to F0 (r), except that it oscillates differently and is larger by a factor of 2πβ. Thus we can get
a reasonable estimate by replacing F0′ (r) with F0 (r)(2πβ) in the integral:

                     E(~bT (I − θ~θ~T )~b | a ≤ η)
                               1        n−1           h
                                                        1             2
                       .                        S 0 ·   2 (n − 2)(ληe)
                           Pr[a ≤ η] (2π)2
                                                    17(ληe)3
                                                                                      i
                            5    ληe          2                              10
                       + n−1      λ  (2πβ)      +       λ      + (2n +  9 + n−3 )eλ(ληe)
                         Z ∞
                       ·           F0 (r)2 r n−1 dr
                             1/(ληe)

Using the definition of λ,

                      E(~bT (I − ~
                                 θ~
                                  θ T )~b | a ≤ η)
                                1       n−1            h               2
                        .                        S 0 ·   (const) (2πβ)
                                                                    n η
                                                                           2
                            Pr[a ≤ η] (2π)2
                                             2               (2πβ)2 3                (2πβ)2
                                                                                            i
                        + (const) (2πβ)  n     η +   (const)   n3
                                                                     η     + (const)    n   η
                          Z ∞
                        ·          F0 (r)2 r n−1 dr.
                             1/(ληe)

Now recall the expression for Pr[a ≤ η] given by (2). We expect the two integrals to roughly cancel
out, so we get
                                 E(~bT (I − θ~θ~T )~b | a ≤ η) . O(β 2 η).                     (11)
    This argument can be made rigorous, using known results about Bessel functions Jν (z). However,
there is a technical obstacle: our theorem concerns the case where z is roughly proportional to ν.
This is still in the transition regime, and the usual asymptotic expansions for Jν (z) do not work
here (they only work when z & νp    2 , or when z/ν is some fixed ratio). Fortunately, there are useful

bounds on the quantity Mν (z) := Jν (z)2 + Yν (z)2 , and representations of Jν (z) and Yν (z) in terms
of a modulus and phase, that do work in this regime [1, 30]. This leads to a rigorous proof of our
theorem—see the Appendix for details.

                                                          9
5    Spherical Shells
We now consider the curvelet transform of a function supported on a thin spherical shell in Rn . We
will show results similar to the previous section, except that they now depend on the thickness of
the shell. Intuitively, when the shell is very thin, we can measure very fine-scale elements (a small)
with significant probability, and ~b is tightly concentrated around the wavefront set.
     Without loss of generality, we can assume the shell is centered at the origin (see Section 4).
Sop consider the following function on Rn , f (~x) = [C if β < |~x| ≤ β + δ, 0 otherwise], where C =
1/ (β + δ)n B0 − β n B0 , and B0 is the volume of the unit ball in Rn . This represents a uniform
superposition over a spherical shell centered at the origin, with inner radius β and thickness δ. We
call this a spherical shell with “square” cross-section.
     This is the exactly the kind of state that appears in our quantum algorithm. However, it is
difficult to analyze, as its Fourier transform involves a linear combination of two Bessel functions
oscillating at different rates. We are interested in the case where δ ≪ β. In Appendix D.1, we give a
heuristic explanation of why the curvelet transform of this state will be tightly concentrated around
the wavefront set. (This holds when δ . β/n.)
     Here, we give a more rigorous argument, for spherical shells that have “Gaussian” cross-sections—
when δ ≪ β, these functions are similar to the above, but they are analytically tractable. We
define f = Cf g ∗ q, where: Cf is a normalization factor; g is a Gaussian of width δ, that is,
g(~x) = δ−n/2 exp(−π|~x|2 /δ2 ); q is the measure supported on the sphere of radius β around the origin,
which is obtained by restricting the usual volume measure on Rn ; and the star denotes convolution.
Intuitively, q represents a shell with infinitesimal thickness, and f represents a “smoothed” shell
with thickness δ.
     The Fourier transform of f is given by fˆ = Cf ĝ · q̂, where: ĝ is a Gaussian of width 1/δ, ĝ(~k) =
δ n/2 exp(−πδ2 |~k|2 ); and q̂ is given by q̂(~k) = Q0 (|~k|), where Q0 (ρ) = ρ(n/2)−1
                                                                                  2π
                                                                                       J(n/2)−1 (2πβρ)β n/2 .
Intuitively, the Fourier transform of the spherical shell is somewhat like the Fourier transform of the
ball, except that it decays more slowly (i.e., has more power at high frequencies), for frequencies up
to roughly 1/δ; the power at frequencies above 1/δ is suppressed by ĝ.
     Note that this is quite similar to equation (128), describing a spherical shell with “square” cross-
section, when we substitute in the upper and lower bounds on Cf (to be given later in this section).
This suggests that the spherical shell with “square” cross-section can indeed be approximated by
one with “Gaussian” cross-section, when δ . β/n.
     We will prove bounds on the continuous curvelet transform, with the same window functions as
in Section 4. We use a slightly different scaling parameter λ: we set λ = 2π     β̃e
                                                                              n−2 , where β̃ is an estimate
of the true radius of the shell, which satisfies β ≤ β̃ ≤ Sβ, for some S ≥ 1. We assume that the
dimension n is at least 4, and we assume that the      thickness of the shell is small compared to the
                                       6       1   1 1                                        1      1
radius: δ = εβ, where ε ≤ min (n−2)2 , n+2 , en , 5 . (Note that for these values of n, en       ≤ n+2  and
 1   1
en ≤ 5 , so the second and fourth conditions are actually redundant.) Under these assumptions, we
prove the following:

Theorem 4 Almost all of the power in fˆ is located at frequencies |~k| ≥ 1/λ:                             ˆ~ 2 ~      ε
                                                                                            R
                                                                                                |~k|≤1/λ |f (k)| dk ≤ 5 .
Let ηc = (δ/β̃)(n − 2)/e. The probability of observing a fine-scale element a ≤ ηc is lower-bounded
by: Pr[a ≤ ηc ] > 0.045. Furthermore, the variance of ~b, in the directions orthogonal / parallel to ~
                                                                                                     θ,
conditioned on a ≤ ηc , is upper-bounded by:

                                    θ T )~b | a ≤ ηc ) ≤ (n − 1)εβ 2 (507 + O( n1 )) · S,
                                   θ~
                        E(~bT (I − ~                                                                                (12)


                                                       10
                                 E((~b · θ)
                                         ~ 2 | a ≤ ηc ) ≤ β 2 (23 + O( 12 )).
                                                                      n
                                                                                                      (13)

    The proof uses a similar strategy to what we showed in Section 4. The intuition is as follows. First
write fˆ(~k) = F0 (|~k|). The important difference (compared to Section 4) is that here F0 (r) decays
more slowly, like 1/r (n−1)/2 , for r . 1/δ. Substituting into (2), we see that a constant fraction of
the probability mass lies at frequencies of order 1/δ. So with constant probability, we can observe
fine-scale elements a ≤ ηc where ηc is of order δ/λ. Note that ηc ≈ δ/λ ≈ (const)(δ/β)(n − 2) ≈
(const)ε(n−2). So, when the shell is very thin, ηc will be very small, and ~b will be tightly concentrated
around the wavefront set.
    The rigorous proof is given in Appendix D.2.


6    A Fast Quantum Curvelet Transform

6.1 The Discrete Curvelet Transform: First, we describe the discrete curvelet transform, which
has been studied in the classical setting [6]. The discrete curvelet transform takes a function f (~x)
and returns a function Γf (a, ~b, θ),
                                   ~ where both functions are defined over finite domains. This is
constructed analogously to the continuous curvelet transform, except that one now uses the discrete
Fourier transform on (ZM )n , and a discrete set of scale/direction pairs (a, ~  θ).
     The discrete Fourier transform is defined as follows. We assume that f is defined on a domain
Z consisting of a discrete grid in a finite region of Rn . For example, let Z = (σZ)n ∩ [−L, L)n ,
                                                                                             1
the intersection of a tightly-spaced square lattice and a large cube. Also let Ẑ = ( 2L       Z)n ∩
[− 2σ , 2σ ) . The discrete Fourier transform maps f to a function fˆ defined on Ẑ, as follows:
     1   1 n
                                 ~                                        ~
fˆ(~k) = ( σ )n/2     f (~x)e−2πik·~x , and f (~x) = ( σ )n/2 ~ fˆ(~k)e2πik·~x .
                  P                                          P
         2L       ~
                  x∈Z                                  2L       k∈Ẑ
     One can argue that this is approximates the continuous Fourier transform in the following sense.
Let fcont be a function on Rn , and let fˆcont be its continuous Fourier transform. Suppose that fcont
is supported inside the cube [−L, L)n , and fˆcont has all except an ε fraction of its probability mass
                     1    1 n
inside the cube [− 2σ  , 2σ ) . Then there exists a function fdis on Z, with discrete Fourier transform
fdis , such that fdis ≈ σ n/2 fcont |Z and fˆdis = ( 2L
 ˆ                                                       1 n/2 ˆ
                                                          ) fcont|Ẑ , up to errors whose total probability
mass is roughly ε. See Appendix E.1 for more details.
     Now the discrete curvelet transform is given by
                                                                                 ~~
                                Γf (a, ~b, ~                 fˆ(~k)χa,θ~ (~k)e2πik·b .
                                                          X
                                                    σ n/2
                                           θ) := ( 2L )                                               (14)
                                                        ~k∈Ẑ


The “location” variables ~x and ~b take values in Z, and the “scale” and “direction” variables (a, θ)
                                                                                                    ~
take values in some discrete set G, which we will describe below. The window functions χa,θ~ are
defined over Ẑ, and are constructed so that
                                             P         ~ 2      ~
                                                ~ χ ~ (k) = 1, ∀k ∈ Ẑ. This ensures that the curvelet
                                                 a,θ    a,θ
transform can be realized as a unitary operation on the space spanned by the states |~k, a, ~ θi.
   Recall from Section 2 that each window function χa,θ~ is supported on a “sector” Sa,θ~ that has
              √
angular width a, inner radius 1/a and outer radius 2/a. To satisfy the above condition on χa,θ~ , we
                                            ~ that corresponds to a discrete collection of sectors S ~ ,
want to choose a discrete set of values (a, θ),                                                        a,θ
that forms a “tiling” of the frequency domain. Intuitively, this is done by setting a equal to powers
                                                              √
of 2, and sampling θ~ from a mesh with angular spacing a on the sphere Sn−1 . Then the sectors
Sa,θ~ fit together nicely, as in Figure 1. (This picture is a slight oversimplification; actually, since we
want the window functions χa,θ~ to decay smoothly to zero, we should make their supports overlap


                                                       11
Figure 1: Construction of a 2-D discrete curvelet transform — “tiling” of the frequency domain into
sectors Sa,θ~ , plus special sectors Slow and Shigh for very low and very high frequencies. Within the
annulus, a takes on values 1/2k , for k = 0, 1, 2, 3, 4. Each sector has inner radius 2k = 1/a, outer
                                                               √
radius 2k+1 = 2/a, and angular width (π/2)/2⌊k/2⌋ ≈ (π/2) a.


slightly.) We will describe a construction of this kind in the next section; other constructions were
given in [6, 20].
                                                    ~ relative to the continuous case. Intuitively, the
    This discretization affects the values of a and θ,
“discrete” a can differ from the “continuous” a by a constant factor, and the “discrete” ~θ can differ
                                                       √
from the “continuous” θ~ by an additive error of size a.

6.2 The Quantum Curvelet Transform: The quantum curvelet transform is the unitary opera-
tion that maps
                                                 Γf (a, ~b, θ)|
                                                            ~ ~bi|a, θi.
                                                                     ~
                      X                        X
                          f (~x)|~xi|0, ~0i 7→                                      (15)
                               ~
                               x                  a,~b,θ~

This can be implemented as follows: P    first apply the quantum Fourier transform (QFT), then the
operation X that maps |ki|0, 0i 7→ |ki a,θ~ χa,θ~ (~k)|a, θi,
                           ~    ~     ~                   ~ and then the inverse QFT.
     We want to compute this in time polynomial in n and log(M ) (where M = 2L/σ is the length of
the discrete Fourier transform). This is possible for the QFT. But it is not clear how to perform the
operation X , for a generic choice of the window functions χa,θ~ . (Note that we want the functions
χa,θ~ to be C 1 -smooth, so their supports will necessarily overlap; thus the operation X must prepare
a superposition containing 2Θ(n) terms.)
    Nonetheless, we can perform X efficiently in two cases: (1) when the window functions are
indicator functions supported on disjoint sets, and (2) when the window functions are smooth “bump”
functions that can be expressed as products of 1-D functions using spherical coordinates. The first
case has poor analytic properties, but the second case is a reasonable approximation of the curvelets
used in Sections 3-5. Thus we get an efficient quantum curvelet transform. See Appendix E.2 for
details.



                                                  12
7    Quantum Algorithms using the Curvelet Transform

7.1 Single-shot measurement of a quantum-sample state: Consider the following problem.
Let B be a ball of (unknown) radius β centered at some (unknown) point ~c in Rn , for n ≥ 4. We
are given as input: n, the dimension; β̃, an estimate of the radius of the ball (we are promised that
β̃/2 ≤ β ≤ β̃); R, an outer bound on the location of the center (we are promised that |~c| ≤ R); µ,
the desired accuracy of our answer; a description of the set of grid points G = (σZ)n ∩ [−L, L)n ,
                                πe µ2      1
such that L ≥ R + β̃ and σ ≤ 600   β̃ 14300n+Q1 (for some constant Q1 , to be specified later); and a
quantum state √ 1
                        P
                   |G∩B|  x∈G∩B |~
                          ~      xi, that is, a single quantum-sample over the ball B. We are then
asked to output a point ~z in Rn , that lies within distance µ of the center ~c.
    We propose the following algorithm. Intuitively, this algorithm uses the curvelet transform to
find a line that passes near the center of the ball, then guesses a random point along this line.

Algorithm 1:
Let |ψi be the input quantum state.
               2
Set η = 61 µβ̃ 2 14300+(Q
                       1
                          1 /n)
                                , where Q1 is some constant.
Apply the fast quantum curvelet transform, with λ = 2πnβ̃e , smin = 1, smax = lg η1 + 3.
Measure the scale a = 2−s , location ~b and direction θ.
                                                      ~
If a > η, then
           √ preturn “no answer.”
Set Q3 = 3 242 + (Q2 /n), where Q2 is some constant.
Guess some u ∈ [−1, 1] uniformly at random.
Return the point ~b′ = ~b + uQ3 β̃ θ.
                                   ~

     We are especially interested in instances where the error µ is a constant fraction of the radius β,
i.e., µ = νβ, for some fixed ν < 1. We conjecture that, for any ν, Algorithm 1 solves these instances
with probability Ω(ν 3 ), independent of the dimension n. (In other words, the success probability has
a “heavy tail.”) This is a sharp contrast to what happens in the classical case: if we choose a single
point uniformly at random from the ball, then the success probability is ν n , which is exponentially
small in n. This is because, in high dimensions, most of the volume of the ball lies near its surface.
This is bad for classical sampling, but it helps the quantum curvelet transform, which works by
finding a line normal to the surface of the ball.
     We now show how our results from Section 4 support this conjecture. We prove the following:

Theorem 5 Consider a “continuous” analogue of Algorithm 1, using the continuous curvelet trans-
form over Rn . This algorithm succeeds with constant probability ≥ Ω(ν 3 ).

We will also argue, non-rigorously, that the discrete algorithm will behave like the continuous one,
provided that the grid G is sufficiently fine. When the grid is chosen properly, the discrete algorithm
runs in time poly(n, log R, log β̃, log µ1 ). See Appendix F.1 for details.
   We remark that it should be possible to achieve a better success probability, Ω(ν 2 ), using the
quantum curvelet transform. Here, we showed that ~b was within distance O(β) of the center, so in
the last step of the algorithm, we simply guessed a point along the line, with success probability
Ω(ν). But in fact, ~b should lie at distance ≈ β from the center, so we should be able to guess one of
the two points ~b ± β ~
                      θ, with success probability Ω(1).
   We also remark that classical sampling becomes more powerful if one is allowed any constant
number of samples, instead of just one. By sampling k random points from the ball and taking


                                                       13
                                                          √
their average, one can find the center with accuracy ±β/ k, with constant probability. (However,
for fixed k, the success probability does not have a “heavy tail,” i.e., one cannot expect to get
better accuracy with significant probability. This is because, in high dimensions, random sampling
produces k vectors that are nearly orthogonal.)

7.2 Quantum algorithm for finding the center of a radial function: Let f be a radial
function on Rn (where n ≥ 4), centered at some point ~c, and taking values in some arbitrary set.
Suppose that the level sets of f are concentric spherical shells of thickness δ centered at ~c, i.e., f is
constant on each shell, and f takes on distinct values on different shells. (Note, in previous versions
of this paper, we made an additional assumption, that one can efficiently compute the radius of a
shell, given the value of f on that shell. This assumption is no longer needed.)
    Consider the following problem. We are given as input: n, the dimension; R, an outer bound
on the location of the center (we are promised that |~c| ≤ R); δ, the thickness of the spherical shells;
µ, the desired accuracy of our answer; and an oracle that computes the radial function f . We are
asked to output a point ~z in Rn , that lies within distance µ of the center ~c.
    We propose the following algorithm. The basic idea is to prepare a quantum superposition over a
large ball around the origin, then measure the value of f to get a superposition over a spherical shell
centered at ~c, then apply the curvelet transform, and find a line that passes near ~c. The algorithm
does this twice, then returns the point on the first line that lies closest to the second line (note that,
with high probability, the two lines are nearly orthogonal).
Algorithm 2:
Set R′ = nR. Let B be a ball of radius R′ around ~0.
Choose the grid G = (σZ)n ∩ [−L, L)n , where L = 2R′ and σ = δ/400.
For i ∈ {1, 2}, do the following:
    Prepare the state √ 1
                               P
                                  x∈G∩B |~
                                  ~|G∩B|
                                         xi, using the methods of [2] or [17].
     Compute the value of f in an auxiliary register, and measure it; call this y (i) .
     Set β̃ (i) = R′ − R.
     Set η (i) = (δ/β̃ (i) )(n − 2)/e.
     Apply the fast quantum curvelet transform,
                           (i)     (i)           (i)
     with λ(i) = 2πn−2
                    β̃ e
                         , smin = 1, smax = lg η(i)1
                                                        + 3.
                                    (i)
                           (i)
     Measure the scale a = 2     −s     , location b and direction ~θ(i) .
                                                   ~ (i)

      If a(i) > η (i) , then return “no answer.”
End for.
If |~θ(1) · ~θ(2) | > 3/4, then return “no answer.”
Set r = ~θ(1) · ~   θ (2) , s = ~θ (1) · (~b(1) − ~b(2) ), t = ~θ(2) · (~b(1) − ~b(2) ).
Return the point −s+rt      1−r 2
                                  θ~(1) + ~b(1) .
    We conjecture that Algorithm 2 finds the center with arbitrary precision µ, provided that δ is
sufficiently small, i.e., the radial function f computed by the oracle is sufficiently “precise.” Let us
                    1        µ2            1
assume that δ ≤ 192     · (n−1) 2 R · 761+(Q /n) , for some constant Q1 to be defined later. We conjecture
                                             1
that Algorithm 2 then finds a solution with constant probability, independent of the dimension n.
Thus, only O(1) oracle queries are needed. This is an improvement over the classical case, where
Ω̃(n log R
         µ ) queries are required. (The Ω̃ indicates that we are omitting some log factors.)
    We now show how our results from Section 5 support this conjecture. We prove the following:
Theorem 6 Consider a “continuous” analogue of Algorithm 2, using the continuous curvelet trans-
form over Rn . This algorithm succeeds with constant probability.

                                                                     14
We will also argue, non-rigorously, that the discrete algorithm will behave like the continuous one,
provided that the grid G is sufficiently fine. When the grid is chosen properly, the algorithm runs
in time poly(n, log R, log µ1 ). See Appendix F.2 for details.

7.3 Classical lower bound: We claim that any classical algorithm for finding the center of a
radial function must use at least Ω̃(n log R µ ) queries. (The Ω̃ indicates that we are omitting some log
factors.)
    Our intuition is as follows. Any algorithm can be described as a decision tree, where each node
represents a query to the oracle f , and the algorithm chooses which branch to follow depending on
the oracle’s answer. However, the values of the function f are meaningless by themselves, so when the
algorithm receives an answer from the oracle, the algorithm cannot do anything besides comparing
this answer with the answers returned previously. Thus, after its k’th query, the algorithm can
choose one of at most k distinct branches.
    It follows that, if the algorithm makes ℓ queries, the number of possible outputs (i.e., the number
of leaves in the tree) is at most ℓ!. In order to solve this problem, however, the algorithm must be able
to output at least (R/µ)n different points. So we have (R/µ)n ≤ ℓ!, which implies ℓ ≥ Ω̃(n log R    µ ).
    A formal statement and proof of this result is given in Appendix F.3.

7.4 Finding the center through multiple iterations: We now describe a variant of Algorithm
2, for finding the center of a radial function. This new algorithm will use multiple iterations, and a
larger number of queries, but it has a less demanding requirement on the thickness of the shells that
form the level sets of the radial function f .
    First, we describe a single iteration of the new algorithm. We call this procedure OneRound().
This is similar to Algorithm 2, but it starts out with a promise that  the center lies within distance R
                                                                     √ p
of some point ~p, and it returns a point q~ that lies within distance R µ/2 of the center. OneRound()
also takes a parameter S ≥ 1 that controls the accuracy and success probability: OneRound() returns
a point q~ (instead of “no answer”) with constant probability, and when this happens, the point q~ is
accurate with probability ≥ 1 − O( S1 ).

Procedure OneRound(R, p~, S):
Set R′ = nSR. Let B be a ball of radius R′ around ~0.
Choose the grid G = (σZ)n ∩ [−L, L)n , where L = 2R′ and σ = δ/400.
For i ∈ {1, 2}, do the following:
    Prepare the state √ 1
                               P
                                  x∈G∩B |~
                                  ~
                                  |G∩B|
                                         xi, using the methods of [2] or [17].
     Define the function g(~x) = f (~x + p~).
     Compute the value of g in an auxiliary register, and measure it; call this y (i) .
     Set β̃ (i) = R′ − R.
     Set η (i) = (δ/β̃ (i) )(n − 2)/e.
     Apply the fast quantum curvelet transform,
                           (i)    (i)            (i)
     with λ(i) = 2πn−2
                    β̃ e                        1
                         , smin = 1, smax = lg η(i) + 3.
                                   (i)
     Measure the scale a(i) = 2−s , location ~b(i) and direction ~θ(i) .
      If a(i) > η (i) , then return “no answer.”
End for.
If |θ~(1) · θ~(2) | > 3/4, then return “no answer.”
Set r = ~θ(1) · ~   θ (2) , s = ~
                                θ (1) · (~b(1) − ~b(2) ), t = ~θ(2) · (~b(1) − ~b(2) ).
Return the point q~ = p~ + −s+rt      1−r 2
                                              θ~(1) + ~b(1) .


                                                                     15
    Now we describe the full algorithm, with multiple iterations. This algorithm begins
                                                                                      √ p with a point
at distance R from the center, then uses OneRound() to find a point at distance R µ/2 from the
center, and by repeating the procedure, shrinks the distance to R1/4 (µ/2)3/4 , R1/8 (µ/2)7/8 and so
on. It may seem surprising that the distance decreases by more than a constant factor during each
iteration. Intuitively, this is because the spherical shells used by the algorithm are not exact dilations
of each other. Recall that the shells have different radii β, but they all have the same thickness δ.
The larger the radius β, the smaller the ratio ε = δ/β; so a larger shell allows a significantly more
precise determination of its center. In a sense, the algorithm makes more progress during the early
iterations, when the spherical shells are larger.

Algorithm 3:
Set Rcur = R and p~cur = ~0.
Set niter = ⌈lg lg 2R
                    µ ⌉, S = (9.4)niter and ntries = 910 log S.
While Rcur ≥ µ do:
     Try running OneRound(Rcur , p~cur , S) up to ntries times.
     If OneRound() returns “no answer” on every attempt,
     then return “no answer.”
     Let q~ be the pointp  returned by OneRound() on one of the successful attempts.
                  √
     Set Rcur = Rcur µ/2 and ~       pcur = q~.
End while.
Return p~cur .

    We conjecture that Algorithm 3 will succeed when
                                                      µ
                                  δ<                              Q1
                                                                        ,                            (16)
                                       128(10 lg lg 2R  3 2
                                                     µ ) n (507 + n )

which is a weaker requirement than that of Algorithm 2, where δ had to scale like 1/R. We conjecture
that this algorithm then finds a solution with constant probability. Note that this algorithm uses
                    2R                                                                   R
O(lg lg 2R
         µ lg lg lg µ ) queries, which still beats the classical lower bound of Ω̃(n log µ ) queries.
   We now show how our results from Section 5 support this conjecture. We prove the following:

Theorem 7 Consider a “continuous” analogue of Algorithm 3, using the continuous curvelet trans-
form over Rn . This algorithm succeeds with constant probability.

We will also argue, non-rigorously, that the discrete algorithm will behave like the continuous one,
provided that the grid G is sufficiently fine. When the grid is chosen properly, the algorithm runs
in time poly(n, log R, log µ1 ). See Appendix F.4 for details.


8    Conclusions
We introduced the curvelet transform as a tool for quantum algorithms, and demonstrated how it
can solve problems involving geometric objects in Rn . We showed that: (1) for functions with radial
symmetry, the continuous curvelet transform concentrates probability mass near the wavefront set;
(2) a quantum curvelet transform (which is a discrete approximation of the continuous curvelet
transform) can be implemented efficiently; (3) this leads to quantum algorithms for approximately
finding the center of a ball in Rn , given a single quantum-sample state, and for exactly finding the
center of a radial function in Rn , using O(1) oracle queries.


                                                   16
    There are several ways in which these results might be extended. Perhaps one can adapt these
quantum algorithms to solve more general problems, like finding the center of an ellipsoid. Perhaps
the quantum speed-up can be amplified using a recursive construction, as in [4, 18].
    A general open problem is to understand the behavior of the curvelet transform on more com-
plicated shapes. Can one prove that the probability mass of the curvelet transform is concentrated
near the wavefront set, for arbitrary functions on Rn ? That would generalize the results of this
paper, [10] and [7]. Also, can one rigorously bound the approximation of the continuous curvelet
transform by a discrete one?
    Another problem is to find new quantum algorithms based on the curvelet transform. For ex-
ample, can one construct a curvelet transform over Fnq , that could help to solve hidden polynomial
problems [12]? Are there quantum states with “wavefront” features, from which the curvelet trans-
form could extract useful information? Some candidates are quantum-sample states over convex
polytopes [2, 17], and states produced by the evolution of a quantum walk.
    One might also try to use the output of the curvelet transform in a more sophisticated way. In
this paper, we simply measured the output state, and we made very little use of the scale variable
a, which measures the “sharpness” of the wavefront discontinuity.

Acknowledgements: The author is grateful to R. Koenig, J. Preskill, L. Schulman, A. Childs, D.
Meyer, N. Wallach, S. Jordan, E. Candès, U. Vazirani (who suggested the iterative algorithm in
section 7.4), Z. Landau, D. Aharonov (who pointed out reference [4]), E. Eban, T. Vidick, and the
anonymous referees, for helpful discussions and comments. Supported by an NSF Mathematical
Sciences Postdoctoral Fellowship.


References
 [1] M. Abramowitz and I. A. Stegun, editors. Handbook of Mathematical Functions. U.S. National
     Bureau of Standards, 1972 (tenth printing).

 [2] D. Aharonov and A. Ta-Shma. Adiabatic quantum state generation and statistical zero knowl-
     edge. In STOC, pages 20–29, 2003.

 [3] D. Bacon, A. M. Childs, and W. van Dam. From optimal measurement to efficient quantum
     algorithms for the hidden subgroup problem over semidirect product groups. In FOCS, pages
     469–478, 2005.

 [4] E. Bernstein and U. Vazirani. Quantum complexity theory. SIAM J. Comput., 26(5):1411–1473,
     1997.

 [5] F.J. Blanco-Silva. A generalized curvelet transform. Approximation properties. Univ. of S.
     Carolina, technical report, 2008.

 [6] E. J. Candès, L. Demanet, D. L. Donoho, and L. Ying. Fast discrete curvelet transforms.
     Multiscale Model. Simul., 5:861–899, 2005.

 [7] E. J. Candès and D. L. Donoho. Continuous curvelet transform: I. resolution of the wavefront
     set. Appl. Comput. Harmon. Anal., 19:162–197, 2003.

 [8] E. J. Candès and D. L. Donoho. Continuous curvelet transform: II. discretization and frames.
     Appl. Comput. Harmon. Anal., 19:198–222, 2003.


                                                17
 [9] E.J. Candès and L. Demanet. The curvelet representation of wave propagators is optimally
     sparse. Comm. Pure Appl. Math., 58:1472–1528, 2004.

[10] E.J. Candès and D. L. Donoho. New tight frames of curvelets and optimal representations of
     objects with piecewise-c2 singularities. Comm. Pure Appl. Math., 57:219–266, 2002.

[11] A. Chefles. Quantum state discrimination. Contemporary Physics, 41(6):401–424, 2000.

[12] A. M. Childs, L. J. Schulman, and U. V. Vazirani. Quantum algorithms for hidden nonlinear
     structures. In FOCS, pages 395–404, 2007.

[13] A.M. Childs and W. van Dam. Quantum algorithms for algebraic problems. ArXiv preprint
     0812.0380, to appear in Rev. Mod. Phys., 2008.

[14] T. Decker, J. Draisma, and P. Wocjan. Efficient quantum algorithm for identifying hidden
     polynomials. arXiv:0706.1219v3 [quant-ph], 2007.

[15] A. Fijany and C.P. Williams. Quantum wavelet transforms: Fast algorithms and complete
     circuits. arXiv:quant-ph/9809004v1, 1998.

[16] M. H. Freedman. Poly-locality in quantum computing. arXiv:quant-ph/0001077, 2000.

[17] L. Grover and T. Rudolph. Creating superpositions that correspond to efficiently integrable
     probability distributions. arXiv:quant-ph/0208112v1, 2002.

[18] S. Hallgren and A. Harrow. Superpolynomial speedups based on almost any quantum circuit.
     In ICALP, pages 782–795, 2008.

[19] S. P. Jordan. Fast quantum algorithm for numerical gradient estimation. Phys. Rev. Lett.,
     95(5):050501, 2005.

[20] L. Demanet L. Ying and E. Candès. 3d discrete curvelet transform. In Proc. SPIE Wavelets
     XI, 2005.

[21] Y.-K. Liu. Quantum algorithms using the curvelet transform. ArXiv preprint 0810.4968, 2008.

[22] A. Montanaro. Quantum algorithms for shifted subset problems. arXiv:0806.3362v2 [quant-ph],
     2008.

[23] C. Moore, A. Russell, and P. Sniady. On the impossibility of a quantum sieve algorithm for
     graph isomorphism. In STOC, pages 536–545, 2007.

[24] L. Rademacher and S. Vempala. Dispersion of mass and the complexity of randomized geometric
     algorithms. In FOCS, pages 729–738, 2006.

[25] O. Regev. Quantum computation and lattice problems. SIAM J. Comput., 33(3):738–760, 2004.

[26] P. W. Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a
     quantum computer. SIAM J. Comput., 26(5):1484–1509, 1997.

[27] H. F. Smith. A hardy space for fourier integral operators. J. Geom. Anal., 8(4):629–653, 1998.

[28] E. M. Stein and T. S. Murphy. Harmonic Analysis: Real-variable Methods, Orthogonality, and
     Oscillatory Integrals. Princeton University Press, 1993.

                                                18
[29] E.M. Stein and R. Shakarchi. Fourier Analysis: An Introduction. Princeton University Press,
     2003.

[30] G.N. Watson. A Treatise on the Theory of Bessel Functions. Cambridge, 1962 (2nd ed.).

[31] P. Høyer. Efficient quantum transforms. arXiv:quant-ph/9702028v1, 1997.

[32] P. Høyer and J. Neerbek. Bounds on quantum ordered searching. arXiv:quant-ph/0009032v2,
     2000.


A      The Continuous Curvelet Transform
We now sketch the proofs of Theorems 1 and 2.
  First, for any a and ~
                       θ, let us define
                                               Z
                                 ga,θ~ (~x) :=   hγa,~b,θ~ , f iγa,~b,θ~ (~x)d~b.                                                       (17)
                                                                       Rn

We claim that
                                                                                    2
                                                            ĝa,θ~ (~k) = χa,θ~ (~k) fˆ(~k).                                            (18)
    To see this, write
                                                        Z
                               hγa,~b,θ~, f i =                   ∗
                                                                 γa,       y − ~b)f (~y )d~y = (γ̃a,
                                                                    ~0,θ~ (~
                                                                                                  ∗             ~
                                                                                                    ~0,θ~ ∗ f )(b),
                                                            Rn

where we define
                                                             γ̃a,~0,θ~(~x) = γa,~0,θ~(−~x).
Thus we can write ga,θ~ (~x) as
                             Z
                ga,θ~ (~x) =                    γa,~0,θ~(~x − ~b)(γ̃a,
                                                                    ∗             ~ ~                  ∗             ~
                                                                      ~0,θ~ ∗ f )(b)db = (γa,~0,θ~ ∗ γ̃a,~0,θ~ ∗ f )(b).
                                           Rn

    Taking the Fourier transform, we get

                               ĝa,θ~ (~k) = γ̂a,~0,θ~ (~k)(γ̃a,
                                                              ∗          ~ ˆ~                ~ 2ˆ~
                                                                ~0,θ~ )ˆ(k)f (k) = γ̂a,~0,θ~(k) f (k),

using the fact that
                                   Z                                              Z
                                                               ~                                          ~                        ∗
                 ∗
              (γ̃a,         ~
                   ~0,θ~ )ˆ(k) =
                                              ∗
                                             γa,        x)e−2πik·~x d~x =
                                                ~0,θ~ (−~
                                                                                            ∗
                                                                                           γa,      x)e2πik·~x d~x = γ̂a,~0,θ~ (~k) .
                                                                                              ~0,θ~(~
                                       R   n                                          Rn

This proves equation (18).
   Next, we claim that, for all |~k| ≥ 1/λ,
                                  Z 1Z
                                                                                       da
                                                                  |χa,θ~ (~k)|2 dσ(~θ) n+1 = 1.                                         (19)
                                                    0       S n−1                     a

   To see this, proceed as follows. Fix ~k, and write θ~ in spherical coordinates centered around ~k,
such that θ1 is the angle between θ~ and ~k. Then we have
                                                                    √ √
                                                √ (n+1)/4  sin(θ1 / a) a (n−2)/2
                           ~          ~
                    χa,θ~ (k) = W (λa|k|)V (θ1 / a)a                               .
                                                                sin(θ1 )

                                                                            19
Then substitute into the integral:
      Z 1Z
                                         da
                 |χa,θ~ (~k)|2 dσ(~ θ) n+1
       0   S n−1                        a
                     Z 1Z
                                                        √                 sin(θ /√a) n−2                       da
                                                                                  1
                  =                 W (λa|~k|)2 V (θ1 / a)2 a(n+1)/2                          a(n−2)/2 dσ(~θ) n+1
                       0     S n−1                                            sin(θ1 )                          a
                     Z 1Z
                                                        √                    √                              da
                  =                 W (λa|~k|)2 V (θ1 / a)2 sinn−2 (θ1 / a)dθ1 dσ(θ2 , . . . , θn−1 ) 3/2 .
                       0     S n−1                                                                         a
                  √                                               √
Note that V (θ1 / a) is nonzero only when θ1 ∈ [0, π a], so we can restrict the integral to this range.
                                          √
Then change variables, θ1′ = θ1 / a, to get:
           Z 1Z
                                              da
                         |χa,θ~ (~k)|2 dσ(~θ) n+1
             0    S n−1                      a
                             Z 1Z
                                                                                  √                         da
                          =                W (λa|~k|)2 V (θ1′ )2 sinn−2 (θ1′ )dθ1′ a dσ(θ2 , . . . , θn−1 ) 3/2
                               0     S n−1                                                                 a
                             Z 1Z
                                                                       da
                          =                W (λa|~k|)2 V (θ1 )2 dσ(~θ)
                               0     S n−1                              a
                             Z λ|~k|
                                              da
                                                 Z
                          =           W (a)2            V (θ1 )2 dσ(~θ)
                               0               a  S n−1

                          = 1,

using the admissibility conditions. This proves equation (19).
    We now prove Theorem 1. We write
                         Z
                               Γf (a, ~b, θ)γ
                                          ~ ~ ~(~x)dµ(a, ~b, θ)
                                              a,b,θ
                                                                     ~
                           a<1
                                   Z 1Z
                                                                                            da
                                                Z
                               =                      hγa,~b,θ~ , f iγa,~b,θ~ (~x)d~bdσ(~θ) n+1
                                    0     S n−1   R n                                      a
                                   Z 1Z
                                                                      da
                               =                ga,θ~ (~x)dσ(~θ) n+1 ,
                                    0     S n−1                      a

and we claim that this equals f (~x). Taking the Fourier transform, we get
                                      Z 1Z
                                                                   da
                                                 ĝa,θ~ (~k)dσ(~θ) n+1 ,
                                       0   S n−1                  a

and we claim that this equals fˆ(~k). Using equations (18) and (19), we rewrite this integral as:
                            Z 1Z
                                                                    da
                                         |χa,θ~ (~k)|2 fˆ(~k)dσ(~θ) n+1 = fˆ(~k).
                              0    S n−1                           a

(The last equality holds because of (19) when |~k| ≥ 1/λ, and because fˆ(~k) = 0 when |~k| < 1/λ.)
This proves Theorem 1.
   Finally, we prove Theorem 2. We write
                                                  Z 1Z
                                                                                            da
               Z                                            Z
                            ~   ~  2     ~   ~
                     |Γf (a, b, θ)| dµ(a, b, θ) =               |hγa,~b,θ~, f i|2 d~bdσ(~θ) n+1 .
                 a<1                               0   S n−1 Rn                            a

                                                             20
We rewrite the innermost integral, applying some of the identities used to prove (18):
                          Z                         Z
                                              2 ~            ∗              ~ 2 ~
                                hγa,~b,θ~, f i db =       (γ̃a,~0,θ~ ∗ f )(b) db
                              n                        n
                            R
                                                    ZR
                                                             ∗
                                                          (γ̃a,         ~ ˆ~ 2 ~
                                                  =            ~0,θ~ )ˆ(k)f (k) dk
                                                       n
                                                    ZR
                                                                                  2
                                                  =       (γ̂a,~0,θ~ (~k))∗ fˆ(~k) d~k
                                                       n
                                                    ZR
                                                  =      |χa,θ~ (~k)|2 |fˆ(~k)|2 d~k.
                                                                Rn

Substituting in, and using (19), we get:
                         Z
                               |Γf (a, ~b, θ)|
                                           ~ 2 dµ(a, ~b, ~θ)
                           a<1
                                  Z 1Z
                                                                                       da
                                                Z
                                =                    |χa,θ~ (~k)|2 |fˆ(~k)|2 d~kdσ(~θ) n+1
                                    0     S n−1 Rn                                    a
                                  Z Z 1Z
                                                                             da
                                =                    |χa,θ~ (~k)|2 dσ(~θ) n+1 |fˆ(~k)|2 d~k
                                      n          n−1                       a
                                  ZR 0 S                Z
                                =          ˆ ~  2 ~
                                         |f (k)| dk =          |f (~x)|2 d~x.
                                           Rn                    Rn

This proves Theorem 2.


B      The Curvelet Transform of a Radial Function
B.1     The variance of ~b perpendicular to ~θ
This is a continuation of Section 3.3. Recall that we have L(r) = F0 (r)W (λar), and M (φ1 ) =
       √
V (φ1 / a)Λa (φ1 ). Then we write:
                         Z
                               | ∂k∂ 2 Φ̂a,~u (~k)|2 d~k
                           R n
                                     Z          Z ∞
                                =                      L′ (r)M (φ1 ) sin φ1 cos φ2 +
                                       S n−1     0                                        (20)
                                                                           2
                                        L(r)M ′ (φ1 )r −1 cos φ1 cos φ2 r n−1 drdσ(φ)~

                                     = IAr IA1 I2 + 2IBr IB1 I2 + ICr IC1 I2 ,

where we define                    Z ∞                                     Z π
                           IAr =         L′ (r)2 r n−1 dr,       IA1 =           M (φ1 )2 sinn φ1 dφ1 ,             (21)
                                    0                                        0
                     Z ∞                                          Z π
             IBr =          L′ (r)L(r)r n−2 dr,           IB1 =           M ′ (φ1 )M (φ1 ) cos φ1 sinn−1 φ1 dφ1 ,   (22)
                       0                                             0
                            Z ∞                                     Z π
                   ICr =           L(r)2 r n−3 dr,        IC1 =           M ′ (φ1 )2 cos2 φ1 sinn−2 φ1 dφ1 ,        (23)
                             0                                        0
                                                Z
                                         I2 =            cos2 φ2 dσ(φ2 , . . . , φn−1 ).                            (24)
                                                 S n−2


                                                               21
    This shows that the variance of ~b perpendicular to θ~ is:
                                            Z 1
               ~ T     ~~ T ~    n−1                                                             da
             E(b (I − θ θ )b) =         S 0      I Ar I A1 I 2 + 2I Br I B1 I 2 + I Cr I C1 I 2       .        (25)
                                 (2π)2       0                                                   an+1

A similar formula gives the variance conditioned on observing a ≤ η:
                                                 Z η
     ~ T     ~~ T ~               1    n−1                                                            da
   E(b (I − θθ )b | a ≤ η) =                 S 0      I Ar I A1 I 2 + 2I Br I B1 I 2 + I Cr I C1 I 2       .   (26)
                             Pr[a ≤ η] (2π)2      0                                                   an+1

We will now upper-bound the various integrals appearing on the right hand side of equation (26).

B.1.1
                                   Rη                     n+1 . A straightforward calculation shows that
We begin with the integral          0 IBr IB1 I2 da/a

                                              1
                                                         Z
                                        I2 =                       dσ(φ2 , . . . , φn−1 ).                     (27)
                                             n−1           S n−2
                                                               Rπ
   We can simplify IB1 , by integrating by parts: IB1 = − 0 12 M (φ1 )2 (−1 + n cos2 φ1 ) sinn−2 φ1 dφ1 .
Substituting in the definition of M (φ1 ), changing variables, and using the fact that V is supported
on the interval [0, π/2], we get:
                    Z π                                   √
                                  √ 2 (2n−1)/2  sin(φ1 / a) n−2
         IB1 = −         1
                         2 V (φ1 /  a) a                          (−1 + n cos2 φ1 ) sinn−2 φ1 dφ1
                                                     sin φ1
                    Z0 π
                                  √   2 (2n−1)/2         √
              =−         1
                         2 V (φ1 / a) a          sin(φ1 / a)n−2 (−1 + n cos2 φ1 )dφ1
                        0
                     Z π/√a
                                         2 n    n−2                    √
               =−               1
                                2 V (ω1 ) a sin     ω1 (−1 + n cos2 (ω1 a))dω1
                        0
                   Z π/2
                            1         2 n    n−2                2      √
               =            2 V (ω 1 ) a  sin    ω 1 (1 − n cos   (ω 1  a))dω1 ,
                    0

hence                                                        Z π/2
                                  |IB1 | ≤ 21 an (n − 1)               V (ω1 )2 sinn−2 ω1 dω1 .
                                                              0
Combining this with I2 , we get:
                                                Z
                            |IB1 I2 | ≤ 12 an           V (ω1 )2 dσ(ω1 , φ2 , . . . , φn−1 ) = 12 an .         (28)
                                                S n−1
                                                                        R∞
    Next, we can simplify IBr , by integrating by parts: IBr = − 0 12 L(r)2 (n − 2)r n−3 dr. Combining
this with IB1 and I2 , substituting in the definition of L(r), and exchanging the integrals, we get:
               Z η                    Z η                   Z ηZ ∞
                              da                  1 da                                         da
                   IBr IB1 I2 n+1 ≤        |IBr | 2      =          1
                                                                    2 L(r)2 (n − 2)r n−3 dr 12
                             a                       a       0                                 a
                0
                                      Z0 η Z ∞                   0
                                                  1        2        2         n−3       da
                                    =             2 F0 (r) W (λar) (n − 2)r       dr 12
                                        0    0                                           a
                                      Z ∞               Z η
                                                      2                 da
                                    ≤       1
                                            2 F0 (r)         W (λar)2 21 (n − 2)r n−3 dr.
                                        0                0               a


                                                                  22
By the definition of W ,
                                     Z η                          Z ληr
                                                       da                              dα
                                           W (λar)2 21    =                W (α)2 12      ≤ 21 ,                  (29)
                                      0                 a              0               α
and vanishes when r ≤ 1/(ληe). Thus we have:
                           Z η                                             Z ∞
                                         da
                              IBr IB1 I2 n+1 ≤ 41 (n − 2)                             F0 (r)2 r n−3 dr.           (30)
                            0           a                                   1/(ληe)


B.1.2
                              Rη                  n+1 . We already have a bound for I . For I , we write:
Next, consider the integral      0 IAr IA1 I2 da/a                                   2       A1
                              Z π                               √
                                       √ 2 (2n−1)/2  sin(φ1 / a) n−2 n
                      IA1 =     V (φ1 / a) a                              sin φ1 dφ1
                             0                             sin φ1
                                √
                            Z π/ a
                                                                 √
                          =        V (ω1 )2 an sinn−2 ω1 sin2 (ω1 a)dω1 .
                                 0
                                                                             √               2
Using the fact that V is supported on [0, π/2], and the simple bound sin2 (ω1 a) ≤ ω12 a ≤ π4 a, we
get:
                                      Z π/2
                                                                        2
                            0 ≤ IA1 ≤       V (ω1 )2 an sinn−2 ω1 dω1 π4 a.
                                                     0
Combining with I2 , we get:

                                     π 2 an+1                                                        π 2 an+1
                                                Z
                  0 ≤ IA1 I2 ≤                              V (ω1 )2 dσ(ω1 , φ2 , . . . , φn−1 ) =            .   (31)
                                     4 n−1          S n−1                                            4 n−1

   We now turn to IAr . First, combining with IA1 and I2 , we have
                               Z η                  Z η
                                              da                    π2
                          0≤       IAr IA1 I2 n+1 ≤     IAr da ·          .                                       (32)
                                0            a       0           4(n − 1)

We can upper-bound IAr as follows. Note that, for any two L2 functions, the Cauchy-Schwarz
inequality implies that

            kf + gk2 = kf k2 + 2hf, gi + kgk2 ≤ kf k2 + 2kf kkgk + kgk2 ≤ 2kf k2 + 2kgk2 ;       (33)
                                                                        √
in the last step we used the arithmetic-geometric mean inequality, ab ≤ a+b      2 for a, b ≥ 0, with
a = kf k2 and b = kgk2 . Thus we can write
                                Z ∞                                    2
                     0 ≤ IAr =        F0′ (r)W (λar) + F0 (r)W ′ (λar)λa r n−1 dr
                                 0                                                               (34)
                                             2        2           2
                             = kG1 + G2 k ≤ 2kG1 k + 2kG2 k ,

where we define

                                           G1 (r) = F0′ (r)W (λar)r (n−1)/2                                       (35)
                                                                   ′             (n−1)/2
                                           G2 (r) = F0 (r)W (λar)λar                       .                      (36)



                                                                  23
Thus we have
                           Z η             Z η            Z η
                                     da              2
                                                                             π2
                     0≤   IAr IA1 I2 n+1 ≤      kG1 k da +     kG2 k2 da ·          .                                                      (37)
                        0           a        0              0              2(n − 1)
                                             Rη                 Rη
We then want to upper-bound the integrals 0 kG1 k2 da and 0 kG2 k2 da.
  For the first one, we have:
                         Z η             Z ηZ ∞
                             kG1 k2 da =          F0′ (r)2 W (λar)2 r n−1 drda
                          0
                                         Z0 ∞ 0        Z η
                                                ′   2
                                       =      F0 (r)       W (λar)2 da r n−1 dr.
                                                                  0              0

Using the fact that W is supported on [1/e, 1], we can write
                     Z η                                 Z ληr                           Z ληr
                                           2                           2   1                                dα 1    1
                           W (λar) da =                           W (α) dα    ≤                  W (α)2           ≤    ,                   (38)
                      0                                   0                λr             0                  α λr   λr

and vanishes when r ≤ 1/(ληe). Hence,
                                               Z η                     Z ∞
                                                             1
                                                  kG1 k da ≤  2
                                                                                       F0′ (r)2 r n−2 dr.                                  (39)
                                                0            λ             1/(ληe)


   For the second integral, we have:
                      Z η            Z ηZ ∞
                               2
                          kG2 k da =         F0 (r)2 W ′ (λar)2 λ2 a2 r n−1 drda
                       0              0  0
                                     Z ∞         Z η
                                               2
                                   =     F0 (r)      W ′ (λar)2 λ2 a2 da r n−1 dr.
                                                              0             0

Note that the derivative of W is given by
                                     (
                                      Cw sin(2π log r)π/r,                                    1/e ≤ r ≤ 1,
                           W ′ (r) =                                                                                                       (40)
                                      0,                                                      otherwise,
               p
where Cw =         8/3. So we can write
   Z η                           Z ληr                                          Z 1
           ′       2 2 2                             ′     1
                                                           2 2                                                1                      1
         W (λar) λ a da =                       W (α) α dα 3 ≤                         Cw2 (π/α)2 α2 dα         3
                                                                                                                  = 38 π 2 (1 − 1e ) 3 ,   (41)
    0                                 0                   λr                     1/e                         λr                     λr

and vanishes when r ≤ 1/(ληe). Hence,
                                 Z η                                             Z ∞
                                                                      1
                                                 2
                                          kG2 k da ≤ 83 π 2 (1 − 1e )                          F0 (r)2 r n−4 dr.                           (42)
                                  0                                   λ              1/(ληe)




                                                                           24
B.1.3
                                   Rη
Finally, we consider the integral 0 ICr IC1 I2 da/an+1 . We already have a bound for I2 . For IC1 we
can write:
                   Z π
                                 √     √                    √           2
         0 ≤ IC1 =      V ′ (φ1 / a)(1/ a)Λa (φ1 ) + V (φ1 / a)Λ′a (φ1 ) cos2 φ1 sinn−2 φ1 dφ1
                     0                                                                          (43)
                               2        2          2
                 = kU1 + U2 k ≤ 2kU1 k + 2kU2 k ,

where we define
                                                √     √
                            U1 (φ1 ) = V ′ (φ1 / a)(1/ a)Λa (φ1 ) cos φ1 sin(n−2)/2 φ1                                      (44)
                                               √
                            U2 (φ1 ) = V (φ1 / a)Λ′a (φ1 ) cos φ1 sin(n−2)/2 φ1 .                                           (45)

Then
                                            0 ≤ IC1 I2 ≤ 2kU1 k2 I2 + 2kU2 k2 I2 .                                          (46)
We now evaluate kU1 k2 and kU2 k2 .
  For kU1 k2 , we can write
                     Z π                                      √
                 2         ′      √ 2 −1 (2n−1)/2  sin(φ1 / a) n−2
           kU1 k =       V (φ1 / a) a a                                 cos2 φ1 sinn−2 φ1 dφ1
                      0                                  sin(φ1 )
                     Z π
                                  √                          √
                   =     V ′ (φ1 / a)2 a(2n−3)/2 sinn−2 (φ1 / a) cos2 φ1 dφ1
                            0
                        Z π/√a
                                                                         √
                    =                  V ′ (ω1 )2 an−1 sinn−2 ω1 cos2 (ω1 a)dω1
                            0
                                  Z π/2
                            n−1
                    ≤a                     V ′ (ω1 )2 sinn−2 ω1 dω1 .
                                   0

   The derivative of V is given by
                                                   (
                                                       −2Cv cos(t) sin(t), 0 ≤ t ≤ π/2,
                                       V ′ (t) =                                                                            (47)
                                                       0,                  otherwise,
             q
                 2(n+2)n
where Cv =         3S0 .        Using these formulas and ([1], eqn. 4.3.127), a straightforward calculation
shows that           Z π/2                                                            Z π
                                                                  4n     1
                                   ′        2
                                  V (ω1 ) sin      n−2
                                                         ω1 dω1 =      1−                   sinn−2 ω1 dω1 .                 (48)
                        0                                         3S0     n             0
   So we have                                                              Z π
                                                           4n    1
                                   kU1 k2 ≤ an−1 ·             1−                 sinn−2 ω1 dω1 .
                                                           3S0    n         0
Combining with I2 , we get
                                            4n    1    1
                                                                      Z
           0 ≤ kU1 k2 I2 ≤ an−1 ·               1−    ·                           dσ(ω1 , φ2 , . . . , φn−1 ) = 34 an−1 .   (49)
                                            3S0    n    n−1               S n−1

   Next we evaluate kU2 k2 . The derivative of Λa is given by:
                                  sin(φ /√a) (n−4)/2  cos(φ /√a) sin(φ /√a) cos(φ ) 
         ′
       Λa (φ1 ) = a (2n−1)/4 n−2
                            ( 2 )
                                        1
                                                          √ 1         −
                                                                         1          1
                                                                                         ,                                  (50)
                                     sin(φ1 )              a sin(φ1 )    sin2 (φ1 )

                                                                 25
hence
                                                                     √           √
                   √                        (n−4)/2      √  cos(φ1 / a) sin(φ1 / a) cos(φ1 ) 
 U2 (φ1 ) = V (φ1 / a)a(2n−1)/4 ( n−2
                                   2  ) sin         (φ1 / a)     √      −                       cos φ1 ,
                                                                   a           sin(φ1 )
and
           Z π                                                         √           √
                     √                                    √  cos(φ1 / a) sin(φ1 / a) cos(φ1 ) 2
kU2 k2 =      V (φ1 / a)2 a(2n−1)/2 ( n−2
                                       2  )2
                                             sin n−4
                                                     (φ1 / a)     √      −                        cos2 φ1 dφ1
           0                                                         a           sin(φ 1 )
          Z π/√a                                  cos(ω ) sin(ω ) cos(ω √a) 2           √
        =        V (ω1 )2 an ( n−2 2
                                2 ) sin
                                       n−4
                                            (ω1 )     √ 1 −        1
                                                                        √1      cos2 (ω1 a)dω1 .
           0                                            a        sin(ω1 a)
Recall that V is supported on [0, π/2]. For ω1 in this range, we have the following crude bound:
(using [1], eqn. 4.3.81)
                                      √                                        √
              cos(ω1 ) sin(ω1 ) cos(ω1 a)         1        sin(ω1 )   sin(ω1 a)        1  1
                √     −           √          ≤√ +               √ ·          √       ≤√ +√ .
                  a        sin(ω1 a)               a sin(ω1 a)           ω1 a           a  a
                       √
Also, we have cos2 (ω1 a) ≤ 1. Hence,
                                   Z π/2
                                                            2   n−4
                              2
                         kU2 k ≤         V (ω1 )2 an ( n−2
                                                        2 ) sin     (ω1 )( √2a )2 dω1
                                         0
                                                       Z π/2
                                     = 4an−1 ( n−2
                                                2 )
                                                   2
                                                                 V (ω1 )2 sinn−4 ω1 dω1 .
                                                        0

   Note that
                    Z π/2                                                    Z π/2
                                                             5 
                            V (ω1 )2 sinn−4 ω1 dω1 = 1 +                              V (ω1 )2 sinn−2 ω1 dω1 ,           (51)
                     0                                       n−3              0

using the definition of V , and integration by parts.
    So we have:                                       Z                π/2
                         kU2 k2 ≤ 4an−1 ( n−2 2      5
                                           2 ) (1 + n−3 )                    V (ω1 )2 sinn−2 ω1 dω1 .
                                                                   0
Combining with I2 , we get:
                                                                   Z
                 0 ≤ kU2 k2 I2 ≤ 4an−1 ( n−2 2      5     1
                                          2 ) (1 + n−3 ) n−1                      V (ω1 )2 dσ(ω1 , φ2 , . . . , φn−1 )
                                                                       S n−1                                             (52)
                               ≤ an−1 (n − 2)(1 + n−3
                                                   5
                                                      ).
   So, by substituting into (46), we have
                               0 ≤ IC1 I2 ≤ 2 · 43 an−1 + 2 · an−1 (n − 2)(1 + n−3
                                                                                5
                                                                                   ).                                    (53)
   Finally, we turn to ICr . Combining it with IC1 and I2 , we have
                        Z η
                                       da                          Z η    da
                                              8                  5
                   0≤       ICr IC1 I2 n+1 ≤ 3 + 2(n − 2)(1 + n−3 )      ICr 2 .
                         0            a                               0     a
We can bound the integral on the right hand side as follows.
                        Z η           Z ηZ ∞
                                da                                      da
                            ICr 2 =            F0 (r)2 W (λar)2 r n−3 dr 2
                                a                                       a
                          0
                                      Z0 ∞ 0       Z η
                                                                 da
                                    =      F0 (r)2     W (λar)2 2 r n−3 dr.
                                       0            0            a

                                                            26
Using the fact that W is supported on [1/e, 1],
                 Z η              Z ληr              Z ληr
                            2 da                2 dα             dα
                     W (λar) 2 =        W (α) 2 λr ≤       W (α)2 eλr ≤ eλr,                               (54)
                  0           a     0             α   0          α
and vanishes when r ≤ 1/(ληe). Hence
                             Z η            Z ∞
                                    da
                                 ICr 2 ≤ eλ          F0 (r)2 r n−2 dr.
                               0    a        1/(ληe)

                   Z η                                                     Z ∞
                              da                          
              0≤   ICr IC1 I2 n+1 ≤ 38 + 2(n − 2)(1 + n−3
                                                       5
                                                          ) eλ                         F0 (r)2 r n−2 dr.   (55)
                 0           a                                               1/(ληe)



B.2    The variance of ~b parallel to θ~
Finally, we seek to bound the variance of ~b, in the direction parallel to θ.     ~ The analysis is similar to
                                          ~
the previous case (i.e., the variance of b orthogonal to θ). ~
   The variance of ~b parallel to θ~ is:
                                           Z 1Z
                                                                        ~ 2 d~b da dσ(~θ).
                                    Z
                          ~  ~ 2
                      E((b · θ) ) =               (~b · θ)
                                                        ~ 2 |Γf (a, ~b, θ)|                               (56)
                                      S n−1 0  Rn                              an+1
We can simplify this by taking advantage of rotational symmetry. Fix a vector ~u = (1, 0, . . . , 0), and
for each ~θ, let R be a rotation that maps θ~ to ~u. Then
                                       Z 1Z
                                                                                     da
                                 Z
                      ~   ~ 2
                   E((b · θ) ) =              (R(~b) · ~u)2 |Γf (a, R(~b), ~u)|2 d~b n+1 dσ(~θ).     (57)
                                  S n−1 0  Rn                                       a

Then change variables ~b 7→ R−1 (~b). The integrand is now independent of θ,        ~ so we can do the ~
                                                                                                       θ
integral. We get:                           Z 1Z
                                                                              da
                              ~   ~ 2
                           E((b · θ) ) = S0         b21 |Γf (a, ~b, ~u)|2 d~b n+1 .                 (58)
                                             0   Rn                          a
   We now introduce some new notation,

                                            Φa,θ~ (~b) := Γf (a, ~b, θ),
                                                                     ~                                     (59)

to emphasize that we view this as a function of ~b. By equation (1), the Fourier transform of Φa,θ~ is
given by
                                      Φ̂a,θ~(~k) = fˆ(~k)χa,θ~ (~k).                            (60)
And we have, by Plancherel’s theorem:
                                                 Z 1Z
                                                                            da
                            E((~b · θ)
                                    ~ 2 ) = S0      b21 |Φa,~u (~b)|2 d~b n+1
                                              0  Rn                        a
                                             Z 1Z                                                          (61)
                                                       1 ∂                   2    da
                                        = S0                      Φ̂a,~u (~k) d~k n+1 .
                                              0  Rn 2πi ∂k1                      a

   Now, using spherical coordinates ~k = (r, φ1 , . . . , φn−1 ), we write Φ̂a,~u (~k) as a product of a radial
part and an angular part:
                                       Φ̂a,~u (~k) = L(r)M (φ1 ),                                          (62)

                                                        27
where                                                                        √
                              L(r) = F0 (r)W (λar),         M (φ1 ) = V (φ1 / a)Λa (φ1 ).         (63)
Then we have
                                ∂                              ∂r                  ∂φ1
                                   Φ̂a,~u (~k) = L′ (r)M (φ1 )     + L(r)M ′ (φ1 )     ,          (64)
                               ∂k1                             ∂k1                 ∂k1
where
                                         ∂r                    ∂φ1    sin φ1
                                             = cos φ1 ,            =−        .                    (65)
                                         ∂k1                   ∂k1       r
Now we can expand out the following integral: (note that Φ̂a,~u (~k) is real)
                                              Z ∞
                    ∂            2
               Z                       Z
                               ~   ~
                       Φ̂a,~u (k) dk =             L′ (r)M (φ1 ) cos φ1
                Rn ∂k1                   S n−1 0
                                                                    2                            (66)
                                                                                ~
                                          − L(r)M ′ (φ1 )r −1 sin φ1 r n−1 drdσ(φ)
                                               = KAr KA1 K2 − 2KBr KB1 K2 + KCr KC1 K2 ,

where we define
                                          Z ∞
                                 KAr =           L′ (r)2 r n−1 dr                                 (67)
                                           0
                                          Z π
                                 KA1 =           M (φ1 )2 cos2 φ1 sinn−2 φ1 dφ1                   (68)
                                           0
                                          Z
                                   K2 =            dσ(φ2 , . . . , φn−1 )                         (69)
                                            n−2
                                          ZS∞
                                 KBr =           L′ (r)L(r)r n−2 dr                               (70)
                                          Z0 π
                                 KB1 =           M ′ (φ1 )M (φ1 ) cos φ1 sinn−1 φ1 dφ1            (71)
                                           0
                                          Z ∞
                                 KCr =           L(r)2 r n−3 dr                                   (72)
                                           0
                                          Z π
                                 KC1 =           M ′ (φ1 )2 sinn φ1 dφ1 .                         (73)
                                           0

   Thus we can write the variance of ~b parallel to θ~ as:
                               Z 1
               ~   ~ 2      S0                                               da
            E((b · θ) ) =           K    K
                                       Ar A1 2K   −   2K   K  K
                                                         Br B1 2 + K  K  K
                                                                    Cr C1 2       .               (74)
                          (2π)2 0                                            an+1

A similar formula gives the variance conditioned on observing a ≤ η:

  E((~b · ~θ)2 | a ≤ η)
                                                  Z η                                      da
                                  1       S0
                          =                           KAr KA1 K2 − 2KBr KB1 K2 + KCr KC1 K2 n+1 . (75)
                              Pr[a ≤ η] (2π)2      0                                        a

We would then like to bound the various integrals appearing on the right hand side.




                                                            28
B.2.1
                           Rη
We begin with the integral 0 KBr KB1 K2 da/an+1 .
   Note that K2 = (n − 1)I2 , while KB1 = IB1 and KBr = IBr . Using the argument from the
previous section, we have:
                   Z η                                                   Z ∞
                                 da
                      KBr KB1 K2 n+1 ≤ 41 (n − 1)(n − 2)                              F0 (r)2 r n−3 dr.   (76)
                    0           a                                         1/(ληe)


B.2.2
                            Rη
Next, consider the integral 0 KAr KA1 K2 da/an+1 . We already have a bound for K2 . For KA1 , we
write:
                      Z π
                                  √
               KA1 =       V (φ1 / a)2 Λa (φ1 )2 cos2 φ1 sinn−2 φ1 dφ1
                      Z0 π                                  √
                                  √ 2 (2n−1)/2  sin(φ1 / a) n−2
                    =      V (φ1 / a) a                              cos2 φ1 sinn−2 φ1 dφ1
                        0                             sin φ1
                      Z π/√a
                                                             √
                    =         V (ω1 )2 an sinn−2 ω1 cos2 (ω1 a)dω1 .
                         0
                                                                             √
Using the fact that V is supported on [0, π/2], and the simple bound cos2 (ω1 a) ≤ 1, we get:
                                               Z π/2
                               0 ≤ KA1 ≤                V (ω1 )2 an sinn−2 ω1 dω1 .
                                                0

Combining with K2 , we get:
                                          Z
                     0 ≤ KA1 K2 ≤ a   n
                                                      V (ω1 )2 dσ(ω1 , φ2 , . . . , φn−1 ) = an .         (77)
                                              S n−1

   We now turn to KAr . First, combining with KA1 and K2 , we have
                                 Z η                  Z η
                                                da            da
                            0≤       KAr KA1 K2 n+1 ≤     KAr .                                           (78)
                                  0            a       0       a

Note that KAr = IAr , so we can upper-bound KAr as in the previous section:

                                   0 ≤ KAr ≤ 2kG1 k2 + 2kG2 k2 ,                                          (79)

where we define

                                 G1 (r) = F0′ (r)W (λar)r (n−1)/2                                         (80)
                                                            ′           (n−1)/2
                                 G2 (r) = F0 (r)W (λar)λar                        .                       (81)

Thus we have             Z η                                   Z η
                                      da     Z η                         da 
                                                        2 da
                  0≤     KAr KA1 K2 n+1 ≤ 2        kG1 k     +     kG2 k2      .                          (82)
                       0             a          0         a     0          a
                                         Rη                  Rη
We then want to upper-bound the integrals 0 kG1 k2 da/a and 0 kG2 k2 da/a.


                                                          29
   For the first one, we have:
                         Z η             Z ηZ ∞
                                    da                                        da
                             kG1 k2    =           F0′ (r)2 W (λar)2 r n−1 dr
                          0         a                                          a
                                         Z0 ∞ 0         Z η
                                                                      da
                                       =      F0′ (r)2      W (λar)2 r n−1 dr.
                                          0              0             a

Using equation (29), we get:
                                  Z η                        Z ∞
                                                      da
                                          kG1 k2         ≤                 F0′ (r)2 r n−1 dr.                      (83)
                                      0                a         1/(ληe)


   For the second integral, we have:
                      Z η             Z ηZ ∞
                                 da                                              da
                          kG2 k2    =          F0 (r)2 W ′ (λar)2 λ2 a2 r n−1 dr
                                 a                                                a
                       0
                                      Z0 ∞ 0       Z η
                                    =      F0 (r)2     W ′ (λar)2 λ2 ada r n−1 dr.
                                                  0                 0

Recall that the derivative of W is given by equation (40). So we can write
            Z η                           Z ληr                               Z 1
                    ′    2 2                           ′    12                                    1          1
                  W (λar) λ ada =                 W (α) αdα 2 ≤                    Cw2 (π/α)2 αdα 2 = 83 π 2 2 ,   (84)
             0                             0               r                   1/e               r          r

and vanishes when r ≤ 1/(ληe). Hence,
                                Z η                              Z ∞
                                               da
                                      kG2 k2      ≤ 83 π 2                   F0 (r)2 r n−3 dr.                     (85)
                                 0              a                  1/(ληe)


B.2.3
                                   Rη
Finally, we consider the integral 0 KCr KC1 K2 da/an+1 . We already have a bound for K2 . For KC1
we can write:
                         Z π
                                       √     √                    √           2
             0 ≤ KC1 =        V ′ (φ1 / a)(1/ a)Λa (φ1 ) + V (φ1 / a)Λ′a (φ1 ) sinn φ1 dφ1
                          0                                                                   (86)
                                     2        2          2
                      = kŨ1 + Ũ2 k ≤ 2kŨ1 k + 2kŨ2 k ,

where we define
                                                    √     √
                               Ũ1 (φ1 ) = V ′ (φ1 / a)(1/ a)Λa (φ1 ) sinn/2 φ1                                    (87)
                                                   √
                               Ũ2 (φ1 ) = V (φ1 / a)Λ′a (φ1 ) sinn/2 φ1 .                                         (88)

Then
                                  0 ≤ KC1 K2 ≤ 2kŨ1 k2 K2 + 2kŨ2 k2 K2 .                                         (89)
We now evaluate kŨ1 k2 and kŨ2 k2 .




                                                                 30
   For kŨ1 k2 , we can write
                             Z π
                                           √                   sin(φ /√a) n−2
                                                                     1
                   kŨ1 k2 =      V ′ (φ1 / a)2 a−1 a(2n−1)/2                    sinn φ1 dφ1
                                                                  sin(φ1 )
                             Z0 π
                                           √                          √
                           =      V ′ (φ1 / a)2 a(2n−3)/2 sinn−2 (φ1 / a) sin2 φ1 dφ1
                               0
                              Z π/√a
                                                                              √
                         =                  V ′ (ω1 )2 an−1 sinn−2 ω1 sin2 (ω1 a)dω1
                               0
                                           Z π/2
                              π2       n
                         ≤         a               V ′ (ω1 )2 sinn−2 ω1 dω1 .
                              4             0
                                            √               2
(In the last step we used the bound sin2 (ω1 a) ≤ ω12 a ≤ π4 a.)
    Then, using equation (48), we have

                                    π 2 n 4n       1  π n−2
                                                        Z
                                 2
                           kŨ1 k ≤    a ·      1−           sin ω1 dω1 .
                                    4      3S0      n 0
Combining with K2 , we get
                              π 2 n 4n     1
                                                               Z
                                                                                                         2
           0 ≤ kŨ1 k2 K2 ≤      a ·     1−    ·                           dσ(ω1 , φ2 , . . . , φn−1 ) = π3 an (n − 1).   (90)
                              4      3S0    n                      S n−1

   Next we evaluate kŨ2 k2 . The derivative of Λa is given by equation (50), hence
                                                                  √             √
                    √ (2n−1)/4 n−2       (n−4)/2      √  cos(φ1 / a) sin(φ1 / a) cos(φ1 ) 
 Ũ2 (φ1 ) = V (φ1 / a)a       ( 2 ) sin         (φ1 / a)     √      −                       sin φ1 ,
                                                                a             sin(φ1 )
and
          Z π                                                    √            √
      2             √ 2 (2n−1)/2 n−2 2 n−4          √  cos(φ1 / a) sin(φ1 / a) cos(φ1 ) 2 2
kŨ2 k =     V (φ1 / a) a        ( 2 ) sin     (φ1 / a)     √      −                        sin φ1 dφ1
          0                                                    a            sin(φ1 )
         Z π/√a                              cos(ω ) sin(ω ) cos(ω √a) 2         √
       =               2 n n−2 2
                V (ω1 ) a ( 2 ) sinn−4
                                       (ω1 )    √ 1 −        1
                                                                  √1       sin2 (ω1 a)dω1 .
          0                                       a        sin(ω1 a)
Recall that V is supported on [0, π/2]. For ω1 in this range, we have the following crude bound:
(using [1], eqn. 4.3.81)
                                      √                             √
              cos(ω1 ) sin(ω1 ) cos(ω1 a)     1     sin(ω1 )  sin(ω1 a)      1     1
                √     −           √        ≤√ +          √ ·       √     ≤√ +√ .
                  a        sin(ω1 a)            a sin(ω1 a)      ω1 a         a     a
                       √              2
Also, we have sin2 (ω1 a) ≤ ω12 a ≤ π4 a. Hence,
                                           Z π/2
                               2                                     2   n−4                  π2
                        kŨ2 k ≤                   V (ω1 )2 an ( n−2
                                                                  2 ) sin    (ω1 )( √2a )2       adω1
                                            0                                                 4
                                                          Z π/2
                                   = π 2 an ( n−2
                                               2 )
                                                  2
                                                                  V (ω1 )2 sinn−4 ω1 dω1 .
                                                           0

   By equation (51), we have:
                                                                       Z π/2
                       kŨ2 k2 ≤ π 2 an ( n−2 2      5
                                           2 ) (1 + n−3 )                      V (ω1 )2 sinn−2 ω1 dω1 .
                                                                           0


                                                                  31
Combining with K2 , we get:
                                                                 Z
               0 ≤ kŨ2 k2 K2 ≤ π 2 an ( n−2 2      5
                                          2 ) (1 + n−3 )                     V (ω1 )2 dσ(ω1 , φ2 , . . . , φn−1 )
                                                                     S n−1                                                 (91)
                                  2
                              ≤ π4 an (n − 2)2 (1 + n−3
                                                     5
                                                        ).

    So, by substituting into (89), we have
                                          2                              2
                     0 ≤ KC1 K2 ≤ 2 · π3 an (n − 1) + 2 · π4 an (n − 2)2 (1 + n−3
                                                                               5
                                                                                  ).                                       (92)

    Finally, we turn to KCr . Combining it with KC1 and K2 , we have
                 Z η
                                 da     2                             Z η    da
                                         2π          π2       2      5
             0≤      KCr KC1 K2 n+1 ≤ 3 (n − 1) + 2 (n − 2) (1 + n−3 )      KCr .
                  0             a                                        0      a

We can bound the integral on the right hand side as follows.
                        Z η           Z ηZ ∞
                                da                                       da
                            KCr     =          F0 (r)2 W (λar)2 r n−3 dr
                                 a                                        a
                         0
                                      Z0 ∞ 0       Z η
                                                                 da
                                    =      F0 (r)2     W (λar)2 r n−3 dr.
                                        0           0             a

Using equation (29), we get
                                  Z η                Z ∞
                                              da
                                        KCr      ≤                   F0 (r)2 r n−3 dr.
                                   0           a       1/(ληe)

         Z η                                                                               Z ∞
                      da    2              2
                                                                
      0≤   KCr KC1 K2 n+1 ≤ 2π3 (n − 1) + π2 (n − 2)2 (1 + n−3
                                                            5
                                                               )                                       F0 (r)2 r n−3 dr.   (93)
         0           a                                                                       1/(ληe)



C     The Ball in Rn
We prove Theorem 3.

C.1     The low-frequency components
First, we claim that almost all the power in fˆ is located at frequencies above some threshold 1/λ.
This justifies our use of the curvelet transform, and theorems 1 and 2, for an appropriate choice of
the parameter λ.                                               Rz
    We start by proving an upper-bound on the integral 0 t−1 Jν (t)2 dt, for ν > 0. Note that ([1],
eqn. (9.1.62))
                                             ( 1 t)ν
                                  |Jν (t)| ≤ 2         (ν ≥ − 21 , t ≥ 0).                      (94)
                                                ν!
Also ([1], eqn. (6.1.38)),
                                           √         1
                                     ν! > 2πν (ν+ 2 ) e−ν (ν > 0).                              (95)
Hence
                                                 ( 21 t)ν                    1  te ν
                                |Jν (t)| < √            1            =√                ,                                   (96)
                                               2πν ν+ 2 e−ν                  2πν 2ν

                                                            32
and
            Z z                          Z z
                      −1        2              1 1  te 2ν       1  e 2ν 1 2ν z    1  ez 2ν
                  t        Jν (t) dt <                      dt =              t    =             .    (97)
             0                            0    t 2πν 2ν          2πν 2ν    2ν    0   4πν 2 2ν

This upper bound is useful when z ≤ 2ν/e.
   We can now calculate the amount of power contained in the low-frequency components of f :
                                           Z z
                                               n 1
                       Z
                               ˆ  ~  2 ~
                              |f (k)| dk =            J (2πρβ)2 · S0 ρn−1 dρ
                         ~                     S   ρ n n/2
                        |k|≤z               0    0
                                             Z 2πβz
                                         =n          t−1 Jn/2 (t)2 · dt                   (98)
                                                               0
                                                           1  2πβez n
                                                        <n 2            .
                                                          πn     n
Setting z = n/(2πβe), we get
                                                                                    1
                                                 Z
                                                                   |fˆ(~k)|2 d~k <    .               (99)
                                                     |~k|≤n/(2πβe)                 πn

Recall that we set the parameter λ so that λ ≥ 2πβe/n. So the region {|~k| ≤ 1/λ} contains at most
a 1/(πn) fraction of the total power.

C.2     The decay of Jν (x)
We now prove some technical lemmas on the decay of Jν (x) for x ≥ 2ν, ν ≥ 1/2. These follow
from classical results on Bessel functions [1, 30], though some care is required near the transition
region at x ≈ ν. In particular, the usual asymptotic expansions for Jν (x) only work when x ≥ ν 2 ,
or when x = αν for some fixed constant α. For our purposes, we use an asymptotic expansion of
Jν (x)2 + Yν (x)2 , that behaves well when x ≥ ν.

C.2.1
We start by quoting the following result from ([30], p.447). Define
                                             p
                                   Mν (x) = Jν (x)2 + Yν (x)2 .                                      (100)

Then for all x ≥ ν ≥ 1/2,
                                                  2               2
                                                    < Mν (x)2 < √         .                          (101)
                                                 πx            π x2 − ν 2
   This immediately implies an upper bound on Jν (x)2 , for all x ≥ 2ν, ν ≥ 1/2:
                                                           2          2   2
                                     Jν (x)2 ≤ Mν (x)2 < √         ≤    ·√ .                         (102)
                                                        π x2 − ν 2   πx    3

C.2.2
We next prove a lower bound on |Jν (x)|, for x within certain intervals. Note that Jν (x) is large at a
zero of Yν (x). We will show that (1) the zeroes of Yν (x) are not too far apart, and (2) Jν (x) is large
in a neighborhood around each zero of Yν (x).



                                                                   33
   To see this, note that Jν (x) and Yν (x) can be written in terms of a modulus and phase,

                                        Jν (x) = Mν (x) cos θν (x),                                      (103)
                                        Yν (x) = Mν (x) sin θν (x),                                      (104)

where Mν (x) is as defined above, and θν (x) satisfies the equation
                                                          2
                                           θν′ (x) =                                                     (105)
                                                       πxMν (x)2

(see [1], eqn. 9.2.21, and [30], p.514). This implies lower and upper bounds on θν′ (x), for all x ≥ 2ν:
                                             √
                                               3   ′
                                              2 < θν (x) < 1.                                            (106)
                                                             2π
   First, we claim that for any t ≥ 2ν, the interval [t, t + √3
                                                                ] contains a zero of Yν (x). To see this,
write the following, for any δ ≥ 0:
                                                  Z x+δ                          √
                          θν (x + δ) = θν (x) +             θν′ (y)dy ≥ θν (x) + 23 δ.
                                                   x

           2π                                                                                    2π
So θν (t + √3
              ) ≥ θν (t) + π. So θν (x) must equal an integer multiple of π for some x ∈ [t, t + √ 3
                                                                                                     ]; and
Yν (x) must vanish at that point. This proves our first claim.
    Second, let φ be a zero of Yν (x), satisfying φ ≥ 2ν. We claim that, for any δ ∈ [−π/2, π/2],

                                     |Jν (φ + δ)| ≥ Mν (φ + δ) cos δ.                                    (107)

To see this, write

            |Jν (φ + δ)| = Mν (φ + δ)| cos θν (φ + δ)| = Mν (φ + δ) cos |θν (φ + δ) − θν (φ)| .

(The last step follows because θν (φ) is an integer multiple of π.) Then note that
                                                        Z φ+δ
                              |θν (φ + δ) − θν (φ)| =             θν′ (y)dy ≤ |δ|.
                                                            φ

Hence we have
                               cos |θν (φ + δ) − θν (φ)| ≥ cos |δ| = cos δ.
This proves our second claim.

C.2.3
Finally, we prove the following lower bound on a sum of squares of Bessel functions:

         Let ν1 , . . . , νm ∈ [1/2, νmax ]. Let t ≥ 2νmax . Then there exists some t′ ∈ [t − π2 , t +
      2π
      √
       3
         + π2 ] such that
                                                m
                                               X               m
                                                   Jνk (t′ )2 ≥ ′ .                            (108)
                                                               7t
                                            k=1




                                                       34
   Proof: Essentially, we will show that there must exist a point t′ where a constant fraction of the
functions Jνk (t′ )2 (k = 1, . . . , m) are large simultaneously.
                                         2π
   Define the interval I = [t, t + √      3
                                            ]. For each k = 1, . . . , m, I contains a zero of Yνk (x), call it φk .
Now define the function
                                         (
                                           cos2 (x − φk ) if φk − π2 ≤ x ≤ φk + π2 ,
                            χk (x) =
                                           0              otherwise.

Note that
                                                                           2
                                      Jνk (x)2 ≥ Mνk (x)2 χk (x) >           χk (x).
                                                                          πx
Furthermore, define the function
                                                          m
                                                          X
                                                 u(x) =         χk (x),
                                                          k=1

and note that
                                             m
                                             X                   2
                                                   Jνk (x)2 ≥      u(x).
                                                                πx
                                             k=1

    Define the interval I ′ = [t − π2 , t + √
                                            2π
                                              3
                                                + π2 ]; this interval contains the support of all of the functions
χk (x) (k = 1, . . . , m). Then write
                                                 m Z φk +(π/2)
                                                                                       π
                               Z                 X
                                      u(x)dx =                     χk (x)dx = m ·        .
                                 I′                    φk −(π/2)                       2
                                                 k=1

So there must exist a point t′ ∈ I ′ such that
                                        1               1     π π
                                           Z
                             u(t′ ) ≥ ′         u(x)dx ≥ · m · = m,
                                       |I | I ′         7     2 14

and the claim follows.

C.3     The probability of observing a scale a
Next we claim that fˆ has a heavy tail. This implies that we will observe fine-scale elements (a small)
with significant probability.                      R∞
   Again, we start by proving a lower bound on z t−1 Jν (t)2 dt, when ν is of the form m or m+(1/2)
(where m is an integer), ν ≥ 1, and z ≥ 2ν. We will show that:
                              Z ∞                       1      1
                                   t−1 Jν (t)2 dt ≥ 1 −                 .                         (109)
                               z                        2ν 7(z + 5.20)

    First, consider the case of ν = m. We assume m ≥ 1 and z ≥ 2m. Using ([1], eqn. 11.3.36), we




                                                          35
can write
                    Z ∞                                Z ∞
                            t   −1           2
                                     Jν (t) dt =               t−1 Jm (t)2 dt
                        z                              z
                                                                                            m−1
                                                         1                       X         ∞
                                                   =−       J0 (t)2 + Jm (t)2 + 2   Jk (t)2
                                                        2m                                   z
                                                                                            k=1
                                                                                           m−1
                                                       1                                  X                
                                                   =           J0 (z)2 + Jm (z)2 + 2              Jk (z)2
                                                       2m
                                                                                           k=1
                                                                             m−1
                                                       1                    X               
                                                   ≥           Jm (z)2 + 2            Jk (z)2 .
                                                       2m
                                                                                k=1

Then, using the lemma from the previous section, we get the following, for some z ′ ∈ [z, z + 5.20]:
                    Z ∞
                                           1 2m − 1        1       1
                         t−1 Jν (t)2 dt ≥       ′
                                                   ≥   1 −                  .                   (110)
                      z                   2m 7z            2ν 7(z + 5.20)
    Next, consider the case ν = m + (1/2). We assume m ≥ 1 and z ≥ 2m + 1. Using ([1], eqn.
11.3.36), we can write
Z ∞                   Z ∞
     t−1 Jν (t)2 dt =     t−1 Jm+(1/2) (t)2 dt
 z                  z
                                 Z ∞                                                                            m−1
                    1                                             1                                 X               ∞
                =                        t   −1            2
                                                  J1/2 (t) dt −        J1/2 (t)2 + Jm+(1/2) (t)2 + 2   Jk+(1/2) (t)2
                  2m + 1             z                          2m + 1                                                z
                                                                                                                k=1
                                                               m−1
                      1                                       X                
                ≥                J1/2 (z)2 + Jm+(1/2) (z)2 + 2     Jk+(1/2) (z)2 .
                    2m + 1
                                                                                k=1

Then, using the lemma from the previous section, we get the following, for some z ′ ∈ [z, z + 5.20]:
                    Z ∞
                          −1     2        1     2m         1        1
                         t Jν (t) dt ≥             ′
                                                     ≥ 1−                    .                  (111)
                      z                2m  +  1 7z         2ν    7(z + 5.20)

   We now proceed to lower-bound the probability of observing a fine-scale element a. The following
bound holds for any n ≥ 2 and any η ≤ 1/e2 .
                                    Z
                        Pr[a ≤ η] ≥               |fˆ(~k)|2 d~k
                                      |~k|≥1/(λη)
                                    Z ∞
                                               n −n
                                  =               ρ Jn/2 (2πρβ)2 · S0 ρn−1 dρ
                                      1/(λη) 0S
                                        Z ∞
                                  =n               t−1 Jn/2 (t)2 dt
                                          2πβ/(λη)
                                        Z ∞
                                  ≥n            t−1 Jn/2 (t)2 dt,
                                                        n/(eη)

where in the last step we used the fact that λ ≥ 2πβe/n. Then, by equation (109), and using the
fact that n/(eη) ≥ 2e ≥ 5.43, we get
                                  1      1             1 1      eη     1
                Pr[a ≤ η] ≥ n 1 −        n         ≥n 1−        n =      1−    .          (112)
                                   n 7( eη + 5.20)        n 14 eη   14      n

                                                                     36
                                                        eη    1
                                       Pr[a ≤ η] ≥          1−    .                               (113)
                                                        14     n

C.4    The variance of ~b orthogonal to θ~
First, we give a simple upper bound on integrals of the form
                                         Z ∞
                                             t−k Jν (t)2 dt,
                                                 z

for k ≥ 1, z ≥ 2ν and ν ≥ 1/2. This follows from equation (102):
               Z ∞               Z ∞
                                         2 2
                    −k     2
                   t Jν (t) dt ≤     t−k √ dt
                z                 z      πt 3
                                      Z ∞                                                         (114)
                                   4                  4          ∞   4
                               = √        t−k−1 dt = √ (−1/k)t−k   = √ z −k .
                                 π 3 z               π 3         z  π 3k

   We now use this to upper-bound the integral
                                    Z ∞
                                            F0 (r)2 r n−k dr,
                                            1/(ληe)

for k ≥ 1 and η ≤ 1/2e2 . We write the following: (for the last step, recall that λ ≤ 2 · 2πβe/n, which
implies 2πβ/(ληe) ≥ n/(2ηe2 ))
                   Z ∞                          Z ∞
                                             n
                                  2 n−k
                            F0 (r) r    dr =            J (2πβr)2 r −k dr
                    1/(ληe)                  S0 1/(ληe) n/2
                                                Z ∞
                                             n
                                           =              J (t)2 t−k dt · (2πβ)k−1                (115)
                                             S0 2πβ/(ληe) n/2
                                             n 4  2ηe2 k
                                           ≤     √              · (2πβ)k−1 .
                                             S0 π 3k     n


   In a similar way, we can upper-bound the integral
                                     Z ∞
                                             F0′ (r)2 r n−k dr,
                                            1/(ληe)

                   n
for k ≥ 1 and η ≤ n+2 (1/2e2 ). First, note that
                                            q
                              F0′ (r) = −       n −n/2
                                                S0 r   J(n/2)+1 (2πβr)(2πβ).                      (116)
                                q
                                  n         n/2 g(2πβr), where g(x) = x−n/2 J                    ′
(To see this, write F0 (r) =      S0 (2πβ)                                        n/2 (x). Then F0 (r) =
q
   n      n/2 g ′ (2πβr)(2πβ), where g ′ (x) = −x−n/2 J
  S0 (2πβ)                                              (n/2)+1 (x), see [1] eqn. 9.1.30.) Then we write
the following: (for the last step, recall the fact that λ ≤ 2 · 2πβe/n, which implies 2πβ/(ληe) ≥




                                                      37
n/(2ηe2 ))
                  Z ∞                             Z ∞
                                               n
                             F0′ (r)2 r n−k dr =         J        (2πβr)2 r −k dr · (2πβ)2
                   1/(ληe)                     S0 1/(ληe) (n/2)+1
                                                  Z ∞
                                               n
                                             =             J         (t)2 t−k dt · (2πβ)k+1              (117)
                                               S0 2πβ/(ληe) (n/2)+1
                                               n 4  2ηe2 k
                                             ≤     √             · (2πβ)k+1 .
                                               S0 π 3k    n


   We now combine this with the results of section 3, to show a bound on the variance of ~b perpen-
dicular to ~θ, conditioned on a ≤ η.
   We can simplify equations (30), (37) and (55) as follows:
                          Z η                            Z ∞
                                         da    1
                              IBr IB1 I2 n+1 ≤ 4 (n − 2)          F0 (r)2 r n−3 dr,
                           0            a                 1/(ληe)
      Z η
                 da         π2       1 ∞                             π2        17 ∞
                                       Z                                           Z
                                                 ′    2 n−2
 0≤   IAr IA1 I2 n+1 ≤             ·            F0 (r) r    dr +             ·              F0 (r)2 r n−4 dr,
    0           a       2(n  −  1)   λ  1/(ληe)                   2(n −  1)    λ    1/(ληe)
                   Z η                                         Z ∞
                                   da
                0≤     ICr IC1 I2 n+1 ≤ (2n + 9 + n−3   10
                                                           )eλ          F0 (r)2 r n−2 dr.
                    0             a                             1/(ληe)

Plugging in our bounds for the integrals on the right hand side, we get:
                                Z η
                                                da     25 (2η)3
                                     IBr IB1 I2 n+1 ≤           (2πβ)2 ,
                                  0            a       S 0  n
                  Z η
                                   da        5 8                  3600 (2η)4        
               0≤     IAr IA1 I2 n+1 ≤              (2η)2 (2πβ)2 +            (2πβ)2
                                                                                      ,
                   0             a         n − 1 S0                 S0 n 2
                          Z η
                                           da            5  640 (2η)2
                     0≤        ICr IC1 I2 n+1 ≤ 1 +                      (2πβ)2 .
                           0              a            n − 3 S0 n
Substituting into equation (26), and using (113), we get:

   E(~bT (I − θ~θ~T )~b | a ≤ η)
            5.20            1  2                        3200                   18000       
          ≤          1+          β 640(2η)2 + 40(2η)2 +         (2η)2 + 50(2η)3 +       (2η)4
                                                                                                         (118)
              η            n−1                             n−3                     n2
                                                      
          ≤ (1 + O( n1 ))β 2 η 3536 + 260(2η) + O( n1 ) · 4.

Using our assumption that 2η ≤ 1/e2 , we can rewrite this as

                              E(~bT (I − ~
                                         θ~
                                          θ T )~b | a ≤ η) ≤ ηβ 2 (14300 + O( n1 )).                     (119)




                                                       38
C.5    The variance of ~b parallel to ~θ
We also get a bound on the variance of ~b parallel to ~
                                                      θ, conditioned on a ≤ η.
  Substituting into equations (76), (82) and (93), we get:
                             Z η
                                               da       25
                                 KBr KB1 K2 n+1 ≤          (2η)3 (2πβ)2 ,
                              0               a         S0
                     Z η
                                      da       12                5300 (2η)3
                  0≤     KAr KA1 K2 n+1 ≤         (2η)(2πβ)2 +             2
                                                                             (2πβ)2 ,
                       0             a        S 0                  S 0   n
               Z η
                                da     700 (2η)3            500               5 
           0≤      KCr KC1 K2 n+1 ≤               (2πβ)2 +       (2η)3 1 +          (2πβ)2 .
                0             a         S 0  n               S 0             n − 3
Substituting into equation (75), and using (113), we get:
                            5.20         1  2                                               
     E((~b · ~
             θ)2 | a ≤ η) ≤       1+           β 12(2η) + 100(2η)3 ( n532 + 21 + n7 + 5 + n−3
                                                                                           25
                                                                                              )
                              η         n−1                                                        (120)
                                                                    
                          ≤ (1 + O( n1 ))β 2 63 + 3120(2η)2 + O( n1 ) · 2.

Using our assumption that 2η ≤ 1/e2 , we can rewrite this as

                                   E((~b · ~
                                           θ)2 | a ≤ η) ≤ β 2 (242 + O( n1 )).                     (121)


D     Spherical Shells
D.1    Spherical shell with square cross-section
In this section, we give a heuristic analysis of the spherical shell with square cross-section.
     We can write f = h − g, where h is C times the indicator function of a ball of radius β + δ around
the origin, and g is C times the indicator function of a ball of radius β around the origin. Then its
Fourier transform is fˆ = ĥ − ĝ, where ĥ and ĝ are calculated as in Section 4. We can write this as:
fˆ(~k) = F0 (|~k|),
                               C                                   C
                   F0 (ρ) =     n/2
                                    (β + δ)n/2 Jn/2 (2π(β + δ)ρ) − n/2 β n/2 Jn/2 (2πβρ).          (122)
                              ρ                                   ρ
   We are interested in the case where δ ≪ β. Note that interference between the two Bessel
functions begins to play a major role when ρ & 1/(2πδ). We claim that F0 (ρ) decays quite slowly,
out to distance ρ ∼ 1/(2πδ).
   It will be convenient to define

                                          K(β) = β n/2 Jn/2 (2πβρ),                                (123)

so we have
                                                 C
                                     F0 (ρ) =        (K(β + δ) − K(β)).                            (124)
                                                ρn/2
We can approximate F0 (ρ) by a simpler expression. First, when δ . β/n, we can write C as follows:
                                                    r
                                          1            β     1
                               C≈p                =       √ n .                              (125)
                                       nβ n−1 δB0      nδ β B0

                                                       39
Also, when δ is sufficiently small (we will elaborate on this point later),

                                                           C
                                              F0 (ρ) ≈         δK ′ (β).                               (126)
                                                          ρn/2

A straightforward calculation (see [1], equation 9.1.30) shows that

                                      K ′ (β) = (2πρ)β n/2 J(n/2)−1 (2πβρ).                            (127)

Note that K ′ (β) is roughly 2πρ times larger than K(β), so we expect the approximation to be
accurate when δ . 1/(2πρ), or equivalently, when ρ . 1/(2πδ). Combining the above equations, we
get the following approximation for F0 (ρ):
                               r
                                 β     1       1
                      F0 (ρ) ≈      √ n     · n/2 δ · (2πρ)β n/2 J(n/2)−1 (2πβρ)
                                 nδ β B0 ρ
                               r                                                          (128)
                                 βδ 2π
                             =              J        (2πβρ) when ρ . 1/(2πδ),
                                 S0 ρ(n/2)−1 (n/2)−1

where S0 is the surface area of the sphere in Rn (note that B0 = S0 /n).
    Compared to the Fourier transform of the ball (Section 4), this function decays more slowly, out
to distance ρ ∼ 1/(2πδ). Thus, when we apply the curvelet transform, with significant probability,
we can observe fine-scale elements a ≤ η, where η shrinks proportional to δ. This suggests that a
very thin spherical shell (i.e., δ very small) allows us to find the center with very high precision,
proportional to δ.

D.2    Spherical shell with Gaussian cross-section
In the next few sections, we will prove Theorem 4, for a spherical shell with Gaussian cross-section.
    We begin by proving upper and lower bounds on the normalization factor Cf . The following
identity will be useful: (this follows from the definition of F0 (ρ) and a change of variables)
                 Z α′                                     Z 2πβα′
                             2 n−1
                        F0 (ρ) ρ     dρ = Cf2 εn β 2n−2                    1 2 2
                                                                    exp(− 2π ε t )J(n/2)−1 (t)2 tdt.   (129)
                  α                                        2πβα


Then the L2 norm of fˆ(~k) is given by:
                Z                     Z ∞
                       ˆ ~   2 ~
                     |f (k)| dk = S0        F0 (ρ)2 ρn−1 dρ
                  Rn                    0
                                                    Z ∞
                                 = S0 Cf2 εn β 2n−2            1 2 2
                                                        exp(− 2π ε t )J(n/2)−1 (t)2 tdt                (130)
                                                           0
                                      = S0 Cf2 εn β 2n−2 (N1 + N2 ),

where we split the integral into two parts,
                                    Z n−2
                                                 1 2 2
                              N1 =        exp(− 2π ε t )J(n/2)−1 (t)2 tdt,                             (131)
                                          0
                                          Z ∞
                                                        1 2 2
                                   N2 =          exp(− 2π ε t )J(n/2)−1 (t)2 tdt.                      (132)
                                           n−2



                                                          40
   We now prove upper bounds on N1 and N2 . For N1 , using trivial upper bounds on exp(−x2 )
and Jν (x)2 (see [1], eqn. 9.1.60), we get:
                                                Z n−2
                                                         1       1        2
                                         N1 ≤            2 tdt = 4 (n − 2) .                  (133)
                                                   0

For N2 , using the upper bound on Jν (x)2 from equation (102), we get:
                                   Z ∞
                                                1 2 2 √
                             N2 ≤        exp(− 2π ε t ) π 4 3 dt
                                     n−2
                                        √ 1Z ∞
                                     4
                                 = π√3 2π ε                exp(−τ 2 )dτ                       (134)
                                                          √1 ε(n−2)
                                                           2π

                                          4
                                              √ 1 √π     q
                                                           21
                                       ≤ π√ 3
                                               2π ε 2 = 2  3 ε.

   Substituting into (130), we get
                        Z                                                     q
                            |fˆ(~k)|2 d~k ≤ S0 Cf2 εn β 2n−2 ( 14 (n − 2)2 + 2 23 1ε ).
                             Rn
                                                                               q
                 6                                                1        2     21
We assumed ε ≤ (n−2)2 , and it is easy to check that this implies 4 (n − 2) ≤ 2  3 ε . Thus
                                   Z                                         q
                                         |fˆ(~k)|2 d~k ≤ S0 Cf2 εn β 2n−2 · 4 23 1ε .
                                    Rn

Setting the left side equal to 1 implies a lower bound on Cf2 :

                                                          1
                                                                       q
                                           Cf2 ≥                 ·1        3
                                                                           2.                 (135)
                                                   S0 εn−1 β 2n−2 4

   Next we show lower bounds on N1 and N2 . For N1 we have a trivial lower bound,

                                                       N1 ≥ 0.                                (136)
                                               2
For N2 , we use the lower bound Jν (x)2 > πx     cos2 (θν (x)) (see equations (103) and (101)). For
convenience, we define θ(x) = θν (x), suppressing the ν subscript. We get:

                                     2 ∞
                                       Z
                                                   1 2 2
                             N2 ≥           exp(− 2π ε t ) cos2 (θ(t))dt.                      (137)
                                     π n−2

   Note that θ(t) is a monotone increasing function (equation (106)), hence it is one-to-one and has
a well-defined inverse. We make a change of variables, τ = θ(t), t = θ −1 (τ ):

                            2 ∞
                             Z
                                            1 2 −1
                       N2 ≥          exp(− 2π ε (θ (τ ))2 ) cos2 τ · (θ −1 )′ (τ )dτ.          (138)
                            π θ(n−2)

Note that, whenever τ = θ(t), we have (θ −1 )′ (τ ) = θ′1(t) . Hence, by equation (106),

                                  1 < (θ −1 )′ (τ ) < √23 ,     for τ ≥ θ(n − 2).             (139)


                                                          41
Also note that
                                                                        Z τ
                              θ   −1
                                       (τ ) = θ    −1
                                                        (θ(n − 2)) +               (θ −1 )′ (x)dx
                                                                         θ(n−2)                             (140)
                                                ≤ n − 2 + √23 (τ − θ(n − 2)).

Substituting in, we get:
                           Z ∞
                      2                        1 2
                 N2 ≥                   exp(− 2π ε · (n − 2 + √23 (τ − θ(n − 2)))2 ) cos2 τ dτ.             (141)
                      π     θ(n−2)

   We will use the following simple fact: if a function f is nonnegative and monotone decreasing on
the interval [α, ∞), then       Z           ∞           Z                     ∞
                                                  f (x) cos2 xdx ≥ 21              f (x)dx.                 (142)
                                            α                                α+π

This follows because
                   Z ∞                                 ∞ Z α+(k+1)π
                                                       X
                                        2
                           f (x) cos xdx =                               f (x) cos2 xdx
                     α                                 k=0       α+kπ

                                                       X∞                          Z α+(k+1)π
                                                   ≥         f (α + (k + 1)π)                    cos2 xdx
                                                       k=0                          α+kπ

                                                       X∞
                                                   =         f (α + (k + 1)π) π2
                                                       k=0                                                  (143)
                                                       ∞
                                                       X                            Z α+(k+2)π
                                                   =         f (α + (k + 1)π) 21                    dx
                                                       k=0                            α+(k+1)π
                                                       ∞
                                                       X Z α+(k+2)π
                                                             1
                                                   ≥         2                f (x)dx
                                                       k=0        α+(k+1)π
                                                          Z ∞
                                                   = 12           f (x)dx.
                                                          α+π

   Using the above fact, and a change of variables, we get

                         1 ∞
                           Z
                 N2 ≥                         ε · (n − 2 + √23 (τ − θ(n − 2)))2 )dτ
                                            1 2
                                     exp(− 2π
                        π θ(n−2)+π
                        √ Z ∞
                           3                 1 2 2
                     =                exp(− 2π  ε x )dx                                                     (144)
                         2π n−2+ √2π
                                   3
                          √
                            3 1 ∞
                               Z
                     =√                         exp(−y 2 )dy.
                           2π ε √1 ε(n−2+ √2π )
                                            2π               3


Recall that we assumed ε ≤ n+2 1
                                  . This implies √12π ε(n − 2 + √ 2π
                                                                   3
                                                                     ) ≤ √12π . So, substituting in and
integrating numerically, we get that
                                      √
                                         3 1 ∞                      1
                                             Z
                                N2 ≥  √             exp(−y 2 )dy ≥ .                              (145)
                                        2π ε   √1                  4ε
                                                 2π



                                                                   42
   Substituting into (130), we get that
                    Z
                        |fˆ(~k)|2 d~k ≥ S0 Cf2 εn β 2n−2 (0 + 4ε
                                                              1
                                                                 ) = S0 Cf2 εn−1 β 2n−2 · 14 .                       (146)
                          Rn

Setting the left side equal to 1 implies an upper bound on Cf2 :

                                                                             4
                                                           Cf2 ≤                      .                              (147)
                                                                   S0 εn−1 β 2n−2

D.3    The low-frequency components
Next, we show that fˆ(~k) has very little power at low frequencies, corresponding to coarse scales
a ≥ 1. This justifies our use of the curvelet transform, which effectively ignores these low-frequency
components (recall Theorems 1 and 2).
   The total amount of power at frequencies less than z (for any z ≥ 0) is given by:
                Z                      Z z
                        ˆ  ~  2 ~
                       |f (k)| dk = S0     F0 (ρ)2 ρn−1 dρ
                   |~k|≤z                              0
                                                                      Z 2πβz                                         (148)
                                                                                         1 2 2
                                          = S0 Cf2 εn β 2n−2                      exp(− 2π ε t )J(n/2)−1 (t)2 tdt.
                                                                        0

(We used equation (129).) Using a trivial upper bound exp(−x2 ) ≤ 1, and the upper bound for
Jν (x) (when x is small) from equation (96), we get:
                                                                            Z 2πβz
                                                                                        1     te n−2
                    Z
                                 |fˆ(~k)|2 d~k ≤ S0 Cf2 εn β 2n−2                                      tdt
                        |~k|≤z                                               0       π(n − 2) n − 2
                                                                                                                     (149)
                                                                                en−2     1
                                                = S0 Cf2 εn β 2n−2 ·                    · (2πβz)n .
                                                                             π(n − 2)n−1 n

Using our upper bound on Cf2 (equation (147)), we get

                                                                    en−2       1
                                   Z
                                              |fˆ(~k)|2 d~k ≤ 4ε ·            · (2πβz)n
                                     |~k|≤z                      π(n − 2)n−1 n
                                                                                                                     (150)
                                                              4ε     en
                                                             ≤ 2·          · (2πβz)n .
                                                              πe (n − 2)n
                n−2
   Now, fix z = 2πβe . Recall that λ ≥ 2πβe
                                       n−2 , hence 1/λ ≤ z. Then we have


                                                                                  4ε   ε
                                                 Z
                                                                |fˆ(~k)|2 d~k ≤     2
                                                                                      ≤ .                            (151)
                                                     |~k|≤1/λ                     πe   5

                              1
Recall that we assumed ε ≤ n+2  . So the frequencies below 1/λ only constitute a small fraction of
the total probability mass. This justifies our use of the curvelet transform, with this choice of the
parameter λ.




                                                                       43
D.4    The probability of measuring a fine-scale element
We give a lower bound on the probability of measuring the scale variable to be small, a ≤ ηc , where

                                                     δ (n − 2)
                                              ηc =             .                                     (152)
                                                     β̃   e

We will show that a ≤ ηc with at least constant probability.
  First, we write Pr[a ≤ ηc ] as follows, using Section 3.1 and equation (129):
                                  Z ∞
                Pr[a ≤ ηc ] ≥ S0            F0 (ρ)2 ρn−1 dρ
                                   1/(ληc )
                                                Z ∞                                                  (153)
                                   2 n 2n−2                       1 2 2
                            = S 0 Cf ε β                   exp(− 2π ε t )J(n/2)−1 (t)2 tdt.
                                                  2πβ/(ληc )

The lower limit of integration can be simplified, by substituting in the definitions of λ and ηc ,

                    2πβ        2π β̃e −1  δ (n − 2) −1               β 1
                        = 2πβ                              = 2πβ(2πδ)−1 = = .                        (154)
                    ληc         n−2          β̃   e                      δ ε

This integral is similar to the integral N2 which we encountered earlier (equation (132)). We can get a
lower bound using the same technique (equations (137) - (144)); in particular, note that 1/ε ≥ n − 2,
as required in that calculation (this holds because we assumed ε ≤ 1/(n + 2)). This leads to:
                                                    √
                                                       3 1 ∞
                                                           Z
                                         2 n 2n−2
                      Pr[a ≤ ηc ] ≥ S0 Cf ε β     · √                        exp(−y 2 )dy.       (155)
                                                      2π ε   √1      1   2π
                                                                  ε( ε + √ )
                                                               2π         3


   The lower limit of integration can be written as
                                                       r
                          1 1  2π  1    2π    1      2
                         √ ε   +√ =√    1+ √ ε ≤ √ ·2=     ,                                         (156)
                          2π ε   3   2π     3     2π     π

where the last inequality follows because ε ≤ 15 . Thus we can lower-bound our integral as follows:
                                                          √
                                                             3 1 ∞
                                                                Z
                                           2 n 2n−2                       2
                        Pr[a ≤ ηc ] ≥ S0 Cf ε β        ·√         √ exp(−y )dy
                                                           2π ε    2/π
                                                         0.15                                   (157)
                                    > S0 Cf2 εn β 2n−2 ·
                                                           ε
                                    = (0.15)S0 Cf2 εn−1 β 2n−2 .

Now, using our lower bound for Cf2 (equation (135)), we get:
                                                               q
                                                                   3
                                   Pr[a ≤ ηc ] ≥ (0.15) · 14       2 > 0.045.                        (158)


D.5    Some more integrals
Our next goal is to bound the variance of ~b. We begin by proving upper bounds on certain integrals
involving F0 (r) and F0′ (r). Then, in the following two sections, we will bound the variance of ~b in
the directions orthogonal and parallel to ~θ.

                                                      44
   First, we consider integrals of the following form, where k ≥ 1:
                                           Z ∞
                                               F0 (r)2 r n−k dr.                                        (159)
                                                      α

Using the definition of F0 (r), and a change of variables,
          Z ∞                                             Z ∞
                                                                                             dt
               F0 (r)2 r n−k dr = Cf2 εn (2π)k−1 β 2n+k−3              1 2 2
                                                                exp(− 2π ε t )J(n/2)−1 (t)2 k−2 .
           α                                               2πβα                            t

    We will upper-bound this integral, assuming that α ≥ n−2
                                                         2πβ . First, using equation (102), we have
                 4 1
J(n/2)−1 (t)2 ≤ π√ 3t
                      , and we get:
              Z ∞                                                             Z ∞
                               2 n−k                                     4              1 2 2 dt
                    F0 (r) r           dr ≤ Cf2 εn (2π)k−1 β 2n+k−3 ·    √       exp(− 2π ε t ) k−1 .
               α                                                        π 3 2πβα               t

Next, we use a simple inequality: tk−1 ≥ (2πβα)k−1 , whenever t ≥ 2πβα. Thus,
                 Z ∞                                       Z ∞
                           2 n−k       2 n 2n−2    4    1               1 2 2
                     F0 (r) r    dr ≤ Cf ε β    ·  √   k−1
                                                                 exp(− 2π ε t )dt.
                  α                               π 3 α     2πβα

The integral on the right hand side can be bounded as follows:
                                                                 √
          Z ∞
                        1 2 2
                                   Z ∞
                                                     2
                                                           √ 1     π √ 1   π 1
                exp(− 2π ε t )dt =             exp(−τ )dτ · 2π ≤    · 2π = √ .
           2πβα                      √1
                                        ε·2πβα                 ε  2     ε   2ε
                                                 2π


Substituting in, we get:
                    Z ∞
                                                                4 1                           n−2
                          F0 (r)2 r n−k dr ≤ Cf2 εn−1 β 2n−2 · √ k−1 ,              for α ≥       .     (160)
                     α                                           6α                           2πβ

   Next, we consider integrals of the following form, where k = 1, 2:
                                          Z ∞
                                              F0′ (r)2 r n−k dr.                                        (161)
                                                      α

   In order to calculate F0′ (r), we write F0 (r) in the following form:

                           F0 (r) = Cf εn/2 (2π)β n · (2πβ)(n/2)−1 · H(r) · K(2πβr),

where
                                                                              1
                           H(x) = exp(−πε2 β 2 x2 ),         K(x) =              J(n/2)−1 (x).
                                                                        x(n/2)−1
Then F0′ (r) can be written as
                                                           (a)          (b)
                                                F0′ (r) = F0 (r) + F0 (r),
where
                         (a)
                     F0 (r) = Cf εn/2 (2π)β n · (2πβ)(n/2)−1 · H ′ (r) · K(2πβr),
                         (b)
                     F0 (r) = Cf εn/2 (2π)β n · (2πβ)(n/2)−1 · H(r) · K ′ (2πβr)(2πβ).


                                                             45
We can expand this out. Note that (see [1], equation (9.1.30))
                                                                                     1
                   H ′ (x) = exp(−πε2 β 2 x2 )(−2πε2 β 2 x),           K ′ (x) = − (n/2)−1 Jn/2 (x).
                                                                                  x
Substituting in, we get
               (a)                       1
              F0 (r) = Cf εn/2 (2π)β n (n/2)−1 · exp(−πε2 β 2 r 2 )(−2πε2 β 2 r)J(n/2)−1 (2πβr),
                                      r
                (b)                      1
              F0 (r) = Cf εn/2 (2π)β n (n/2)−1 · exp(−πε2 β 2 r 2 )(−1)Jn/2 (2πβr)(2πβ).
                                      r
Thus F0′ (r) is given by:
                             1                                                                 
 F0′ (r) = Cf εn/2 (2π)β n (n/2)−1 exp(−πε2 β 2 r 2 )· −2πε2 β 2 rJ(n/2)−1 (2πβr)−2πβJn/2 (2πβr) . (162)
                          r
Substituting into our integral, and performing a change of variables, we get:
Z ∞                                           Z ∞                                                 2 dt
        ′   2 n−k        2 n     k−1 2n+k−3                  1 2 2     2
      F0 (r) r    dr = Cf ε (2π) β                    exp(− 2π ε t ) ε βtJ(n/2)−1 (t) + 2πβJn/2 (t)       .
 α                                              2πβα                                                 tk−2
                                                                                                     (163)
                                                                 n
   We will upper-bound this integral, assuming that α ≥ 2πβ         . First, using equation (102), we have
              4 1
Jn/2 (t)2 ≤ π√ 3t
                  , and similarly for J(n/2)−1 (t)2 . So we get:
  Z ∞                                                   Z ∞                             2  4 1  dt
                                                                     1 2 2
        F0′ (r)2 r n−k dr ≤ Cf2 εn (2π)k−1 β 2n+k−3           exp(− 2π ε t ) ε2 βt + 2πβ      √         . (164)
   α                                                     2πβα                                π 3 t tk−2
Changing variables and rearranging, we get:
Z ∞
    F0′ (r)2 r n−k dr
 α
                              Z ∞                    √                    4 dτ
    ≤ Cf2 εn (2π)k−1 β 2n+k−3 √          exp(−τ 2 )( 2πεβτ + 2πβ)2 √ k−1 · ( √12π ε)k−2
                                 2πεβα                                  π 3τ
                                                  Z ∞
                                                                                                                    dτ
    = Cf2 εn (2π)k−1 β 2n+k−3 · π√
                                 4
                                   3
                                     ( √12π ε)k−2 √        exp(−τ 2 )(2πε2 β 2 τ 2 + 2(2π)3/2 εβ 2 τ + (2π)2 β 2 ) k−1
                                                     2πεβα                                                        τ
                     √ k
                                         Z ∞
                                                                                                 dτ
    = Cf2 εn+k−2 2π β 2n+k−1 · π 4√3 √             exp(−τ 2 )(2πε2 τ 2 + 2(2π)3/2 ετ + (2π)2 ) k−1 .
                                             2πεβα                                             τ
                                                                                                          (165)

    We can handle integrals of the form
                                                Z ∞
                                                                       dτ
                                                          exp(−τ 2 )                                       (166)
                                                    a                  τℓ
as follows. When ℓ ≥ 0, we have
                        Z ∞                                        √
                                      dτ   1 ∞                 1     π
                                             Z
                            exp(−τ 2 ) ℓ ≤ ℓ    exp(−τ 2 )dτ ≤ ℓ ·     .                                   (167)
                         a            τ   a   a               a     2
When ℓ = −1, we have
                Z ∞                            Z ∞                                         ∞
                            exp(−τ 2 )τ dτ ≤            exp(−τ 2 )τ dτ = − 12 exp(−τ 2 )       = 21 .      (168)
                        a                       0                                          0


                                                              46
When ℓ = −2, we have
 Z ∞                       Z ∞                                          Z ∞                      √
             2 2                        2 2         1          2
                                                                    ∞
                                                                              1         2          π
      exp(−τ )τ dτ ≤            exp(−τ )τ dτ = − 2 exp(−τ )τ −              − 2 exp(−τ )dτ =         < 0.45.
  a                         0                                       0    0                        4
                                                                                                       (169)
    Now, we can upper-bound our integral in the k = 2 case:
        Z ∞
            F0′ (r)2 r n−2 dr
         α
                                          Z ∞
                                                                                              dτ
                  2 n
            ≤ Cf ε (2π)β      2n+1    4
                                   · π√3 √        exp(−τ 2 )(2πε2 τ 2 + 2(2π)3/2 ετ + (2π)2 )
                                            2πεβα                                              τ       (170)
                                                                  √                   √ 
                  2 n         2n+1    4       2  1         3/2       π      2      1    π
            ≤ Cf ε (2π)β           · π√3 2πε · 2 + 2(2π) ε · 2 + (2π) · √2πεβα 2
                                               √                                n
            = Cf2 εn (2π)β 2n+1 · √83 21 ε2 + 2πε + √π2 εβα  1
                                                                  ,    for α ≥       .
                                                                                2πβ
   We can also upper-bound our integral in the k = 1 case:
         Z ∞
             F0′ (r)2 r n−1 dr
          α
                           √            Z ∞
                   2 n−1
              ≤ Cf ε            2n   4
                             2πβ · π 3 √
                                    √           exp(−τ 2 )(2πε2 τ 2 + 2(2π)3/2 ετ + (2π)2 )dτ
                                          2πεβα                                                       (171)
                           √                  √                             √ 
              ≤ Cf2 εn−1 2πβ 2n · π 4√3 2πε2 · 4π + 2(2π)3/2 ε · 12 + (2π)2 · 2π
                           √           √       √                             n
              = Cf2 εn−1 2πβ 2n · √83 4π ε2 + 2πε + π 3/2 ,          for α ≥      .
                                                                              2πβ

D.6    The variance of ~b orthogonal to ~θ
We now bound the variance of ~b orthogonal to ~θ, conditioned on observing a ≤ ηc . Recall that
ηc = β̃δ (n−2)
           e .
    We start with the results of Section 3. From equation (30), we get:
                      Z η                               Z ∞
                                     da      1
                          IBr IB1 I2 n+1 ≤ 4 (n − 2)ληe          F0 (r)2 r n−2 dr.        (172)
                        0           a                    1/(ληe)

(We used the fact that 1 ≤ r · ληe, for all r in this interval.) From equations (37), (39) and (42), we
get:

                                                          1 ∞
                     Z η
                                     da          π2
                                                            Z
                 0≤      IAr IA1 I2 n+1 ≤               ·           F ′ (r)2 r n−2 dr+
                       0           a         2(n − 1) λ 1/(ληe) 0
                                                                  Z ∞                             (173)
                                                π2          2   2                 2 n−2
                                                       · 24e λη            F0 (r) r     dr.
                                            2(n − 1)               1/(ληe)

(Again, we used the fact that 1 ≤ r · ληe, for all r in this interval.) From equation (55), we get:
                        Z η                                  Z ∞
                                       da
                    0≤      ICr IC1 I2 n+1 ≤ 2(n + 10)eλ              F0 (r)2 r n−2 dr.          (174)
                          0           a                       1/(ληe)

(We used the fact that 83 + 2(n − 2)(1 + n−3
                                          5
                                             ) = 83 + 2(n + 3 + n−3
                                                                 5
                                                                    ) ≤ 2(n + 10), assuming n ≥ 4.)

                                                    47
   Now we fix η = ηc , and we upper-bound these integrals, using equations (160) and (170). (Note
                                                                                                  δ (n−2)
                                                              n
that, in order to apply these results, we must have λη1c e ≥ 2πβ . Recall that λ = 2π β̃e
                                                                                   n−2 , and ηc = β̃  e .
                                      1
Also, recall that we assumed ε ≤ en     . Then ληc = 2πδ = 2πεβ, and λη1c e = 2πβεe   1     n
                                                                                        ≥ 2πβ , as desired.)
   After some tedious calculation, we get:
                    Z ηc
                                      da
                          IBr IB1 I2 n+1 ≤ (n − 2) · Cf2 εn−1 β 2n−2 · 120ε2 β 2 ,                     (175)
                      0              a
                     Z ηc
                                       da
                 0≤        IAr IA1 I2 n+1 ≤ 5 · Cf2 εn−1 β 2n−2 · εβ 2 (12000ε2 + 9ε + 80),            (176)
                        0             a
                     Z ηc
                                       da
                 0≤        ICr IC1 I2 n+1 ≤ Cf2 εn−1 β 2n−2 · 2600εβ 2 (1 + n−2
                                                                              12
                                                                                 ) · S.                (177)
                       0              a

Then, by combining these equations and using our assumption that ε ≤ O( n12 ), we get:
      Z ηc                                       da
            IAr IA1 I2 + 2IBr IB1 I2 + ICr IC1 I2 n+1
       0                                          a
                2 n−1 2n−2
           ≤ Cf ε      β         2         2                                    12
                            · εβ (60000ε + 45ε + 400 + 2(n − 2)120ε + 2600(1 + n−2 )S)                (178)

            ≤ Cf2 εn−1 β 2n−2 · εβ 2 (400 + 2600 + O( n1 )) · S.

   Next, recall from equation (157) that:

                                    Pr[a ≤ ηc ] ≥ (0.15)S0 Cf2 εn−1 β 2n−2 .                          (179)

Finally, by substituting into equation (26) and simplifying, we get a bound on the variance of ~b, in
the subspace orthogonal to ~ θ, conditioned on observing a ≤ ηc :

                        E(~bT (I − θ~~
                                     θ T )~b | a ≤ ηc ) ≤ (n − 1)εβ 2 (507 + O( n1 )) · S.            (180)


D.7    The variance of ~b parallel to θ~
We now bound the variance of ~b parallel to ~θ, conditioned on observing a ≤ ηc . Recall that ηc =
δ (n−2)
β̃  e .
    We start with the results of Section 3. From equation (76), we get:
                   Z η                                     Z ∞
                                     da
                       KBr KB1 K2 n+1 ≤ 41 (n − 1)(n − 2)            F0 (r)2 r n−3 dr.       (181)
                    0               a                        1/(ληe)

From equations (82), (83) and (85), we get:
                          Z η                    Z ∞
                                          da
                     0≤       KAr KA1 K2 n+1 ≤ 2            F0′ (r)2 r n−1 dr+
                           0             a          1/(ληe)
                                                         Z ∞                                          (182)
                                              2 · 38 π 2          F0 (r)2 r n−3 dr.
                                                                   1/(ληe)

From equation (93), we get:
                    Z η                                 Z ∞
                                   da    π2  2
                0≤      KCr KC1 K2 n+1 ≤ 2 (n + 3n + 3)          F0 (r)2 r n−3 dr.                    (183)
                     0            a                      1/(ληe)


                                                       48
                            2             2                          2                       2
(We used the fact that 2π3 (n − 1) + π2 (n − 2)2 (1 + n−3
                                                        5
                                                           ) = π2 (n2 + 73 n − 37 + n−3
                                                                                     5
                                                                                        ) ≤ π2 (n2 + 3n + 3),
assuming n ≥ 4.)
   Now we fix η = ηc , and we upper-bound these integrals, using equations (160) and (171). (Note
                                                                                                      δ (n−2)
                                                              n
that, in order to apply these results, we must have λη1c e ≥ 2πβ . Recall that λ = 2π  β̃e
                                                                                     n−2 , and ηc = β̃    e .
Also, recall that we assumed ε ≤ en 1
                                      . Then ληc = 2πδ = 2πεβ, and λη1c e = 2πβεe1
                                                                                    ≥ 2πβn
                                                                                           , as desired.)
   After some tedious calculation, we get:
                    Z ηc
                                       da
                          KBr KB1 K2 n+1 ≤ Cf2 εn−1 β 2n−2 · n2 · 120ε2 β 2 ,                       (184)
                                      a
                     Z0 ηc
                                        da
                 0≤        KAr KA1 K2 n+1 ≤ Cf2 εn−1 β 2n−2 · β 2 (25200ε2 + 60ε + 132),            (185)
                       0               a
                     Z ηc
                                        da
                 0≤        KCr KC1 K2 n+1 ≤ Cf2 εn−1 β 2n−2 · 2400(n2 + 3n + 3)ε2 β 2 .             (186)
                       0               a
Then, by combining these equations and using our assumption that ε ≤ O( n12 ), we get:
     Z ηc                                         da
           KAr KA1 K2 − 2KBr KB1 K2 + KCr KC1 K2 n+1
      0                                             a
             2 n−1 2n−2
          ≤ Cf ε   β     · β (25200ε + 60ε + 132 + 2 · 120n2 ε2 + 2400(n2 + 3n + 3)ε2 )
                            2       2                                                                  (187)

           ≤ Cf2 εn−1 β 2n−2 · β 2 (132 + O( n12 )).
    Next, recall from equation (157) that:
                                     Pr[a ≤ ηc ] ≥ (0.15)S0 Cf2 εn−1 β 2n−2 .                          (188)

Finally, by substituting into equation (75) and simplifying, we get a bound on the variance of ~b, in
the direction ~
              θ, conditioned on observing a ≤ ηc :

                                   E((~b · ~
                                           θ)2 | a ≤ ηc ) ≤ β 2 (23 + O( n12 )).                       (189)


E     A Fast Quantum Curvelet Transform
E.1    The Discrete Curvelet Transform
First, we argue that the discrete Fourier transform approximates the continuous Fourier transform,
in the sense described in Section 6.1. This follows from the definitions of the different transforms.
Recall the continuous Fourier transform that takes a function on Rn to a function on Rn :
                                                  Z
                                             ~                     ~
                                  Fcont (f )(k) =      f (~x)e−2πik·~x d~x,                     (190)
                                                     n
                                                  ZR
                                                                ~
                                   −1
                                  Fcont (g)(~x) =      g(~k)e2πik·~x d~k.                       (191)
                                                        Rn
Now consider the Fourier transform that takes a function on the cube C = [−L, L)n (or equivalently,
a function on Rn that is periodic with respect to the lattice (2LZ)n ) to a function on the (dual)
                1
lattice Ĉ = ( 2L Z)n . We refer to this as the “semi-discrete” Fourier transform:
                                                         Z
                                           ~       1 n/2                ~
                                Fsemi (f )(k) = ( 2L )       f (~x)e−2πik·~x d~x,            (192)
                                                           C
                                                                       ~
                                                              g(~k)e2πik·~x .
                                                         X
                                   −1              1 n/2
                                Fsemi (g)(~x) = ( 2L )                                       (193)
                                                             ~k∈Ĉ



                                                        49
Also recall the discrete Fourier transform, that takes a function on Z = (σZ)n ∩ [−L, L)n to a
                    1           1    1 n
function on Ẑ = ( 2L Z)n ∩ [− 2σ , 2σ ) :
                                                                                 ~
                                  Fdis (f )(~k) = ( 2L
                                                             X
                                                     σ n/2
                                                       )             f (~x)e−2πik·~x ,                   (194)
                                                             ~
                                                             x∈Z
                                                                              ~
                                                                     g(~k)e2πik·~x .
                                                             X
                                   −1               σ n/2
                                  Fdis (g)(~x) = ( 2L )                                                  (195)
                                                             ~k∈Ẑ

   We are given a function fcont on Rn that vanishes outside the cube C. We define a function fsemi
on C by restriction, fsemi = fcont|C . Then it follows from the definitions that fˆsemi = ( 2L    1 n/2 ˆ
                                                                                                   ) fcont|Ĉ .
                 ˆ                                                                1  1 n
   Recall that fcont has most of its probability mass inside the cube [− 2σ , 2σ ) . Then the same
should be true for fˆsemi . Now define a function fˆdis on Ẑ by restriction, fˆdis = fˆsemi |Ẑ . Then, using
the definitions, we see that fdis ≈ σ n/2 fsemi |Z .

    Note that an example of a discrete curvelet transform (over R2 or R3 ) can be found in [6]. There,
the frequency space is partitioned into concentric cubes according to the scale a, and these are
divided into wedges according to the direction θ. ~ For our purposes, we will use a tiling based on
concentric balls (in Rn ), which more closely approximates the continuous curvelet transform defined
in Section 2.
    As a classical computation, the discrete curvelet transform can be implemented using the fast
Fourier transform [6] (see in particular the “wrapping” method). We will use these ideas to implement
a quantum curvelet transform. The following discussion will be self-contained; but for readers who
are familiar with [6], we mention that we omit the “wrapping” step. Our transform produces curvelet
coefficients that are somewhat oversampled, but this does not cause any problems in our situation.

E.2    Constructing the Window Functions χa,θ~(~k)

 We will construct two families of window functions χa,θ~ (~k), for which the operation X can be
 performed efficiently.
 S First, suppose we have some partition    of the frequency domain into disjoint subsets, (ZM )n =
       S , such that given any point ~k ∈ (ZM )n , we can efficiently compute which set Sa,θ~ contains
   a,θ~ a,θ~
~k. Define the window functions to be the indicator functions for these sets,
                                                       (
                                                        1,   if ~k ∈ Sa,θ~ ,
                                        χa,θ~ (~k) =                                                     (196)
                                                        0,   otherwise.

Then the operation X can be implemented efficiently: it simply maps |~ki|0, ~0i 7→ |~ki|a, θi,
                                                                                           ~ where a
and θ~ denote the set S ~ that contains ~k.
                         a,θ
    Unfortunately, these window functions are sharply discontinuous, so the resulting curvelets are
not very well-localized in space. This makes them poorly suited for the applications proposed in this
paper (recall that the results of Sections 3, 4 and 5 required window functions that were C 1 -smooth).
    Smooth window functions are more challenging to implement, because the supports of the func-
tions χa,θ~ (~k) necessarily overlap. Thus, at a given point ~k, the operation X must create a super-
position of many values of a and ~    θ. These superpositions can be complicated: for instance, if we
imagine that the tiling of frequency space looks (locally) like an array of n-dimensional cubes, then
a significant amount of volume lies near the corners of the cubes, and each corner point touches 2n


                                                        50
different cubes, so we would have to prepare superpositions of 2n different values of a and ~θ. This
seems impossible for many choices of the window functions.
    However, the above example also suggests a solution to the problem. We can use spherical
coordinates, which look locally like Cartesian coordinates (except at the poles). If we define the
window functions to be products of simpler functions, each depending on a single variable, then we
can prepare these superpositions efficiently. We now demonstrate this construction.
    First, recall the definition of spherical coordinates in Rn : we have (r, φ1 , . . . , φn−1 ), where r ∈
[0, ∞), φ1 , . . . , φn−2 ∈ [0, π] ∪ {“undef”}, and φn−1 ∈ (−π, π] ∪ {“undef”}. We use the value “undef”
to represent points on the “poles” of the sphere, e.g., if φj = 0 or π, then φj+1 = · · · = φn−1 =
“undef” (a similar situation arises when r = 0).
    Cartesian coordinates are written in terms of spherical coordinates as follows:

                x1 = r cos φ1    (or 0 if undefined),                                                         (197)
                xj = r sin φ1 · · · sin φj−1 cos φj     (or 0 if undefined) (j = 2, . . . , n − 1),           (198)
                xn = r sin φ1 · · · sin φn−1      (or 0 if undefined).                                        (199)

The reverse mapping is given by:
         q
    r = x21 + · · · + x2n ,                                                                                   (200)
    φ1 = arccos(x1 /r) (or “undef” if r = 0),                                                                 (201)
    φj = arccos(xj /(r sin φ1 · · · sin φj−1 ))     (or “undef” if φj−1 ∈ {0, π, “undef”})      (j = 2, . . . , n − 2),
                                                                                                                (202)
 φn−1 = sign(xn ) arccos(xn−1 /(r sin φ1 · · · sin φn−2 ))         (or “undef” if φn−2 ∈ {0, π, “undef”}). (203)

   Next we will define discrete values for the scale variable a and the direction variable ~θ. In the
notation, it will be convenient to represent the scale variable by s instead of a, where

                                                       a = 2−s .                                              (204)

We will then define window functions χs,θ~(~k). These will be products of radial and angular compo-
nents (we write ~k = (r, φ)
                         ~ using spherical coordinates):

                                           χs,θ~(~k) = ws (λr)vs,θ~ (φ).
                                                                     ~                                        (205)

Here, λ is a parameter that sets the radial scaling. For future use, we define the function c : [0, ∞) →
R,                                          (
                                              cos x, 0 ≤ x ≤ π/2,
                                    c(x) =                                                          (206)
                                              0,      x > π/2.
   We begin with the scale variable a = 2−s . We fix the cutoff values smin , smax ∈ Z, where
1 ≤ smin ≤ smax . Then we let s ∈ {smin , smin + 1, . . . , smax } ∪ {“coarse”, “fine”}.




                                                          51
             1

            0.8

            0.6

            0.4

            0.2

             0
                  0      1         2       3           4            5        6         7      8       9       10


             Figure 2: A family of radial window functions: w“coarse” , w1 , w2 and w“fine” .

   We define radial window functions ws (r) as follows:
                                   π s
                               
                                                 s−1     s−1 ≤ r ≤ 2s ,
                               c( 2 (2 − r)/2 ), 2
                               
                      ws (r) = c( π2 (r − 2s )/2s ),    2s ≤ r ≤ 2s+1 ,                                            (207)
                               
                                0,                      otherwise,
                               
                               
                               1,
                                                                 0 ≤ r ≤ 2smin −1 ,
                                   π
                w“coarse” (r) = c( 2 (r − 2smin −1 )/2smin −1 ), 2smin −1 ≤ r ≤ 2smin ,                            (208)
                               
                                0,                                r ≥ 2smin ,
                               
                               
                               0,
                                                               0 ≤ r ≤ 2smax ,
                  w“fine” (r) = c( π2 (2smax +1 − r)/2smax ), 2smax ≤ r ≤ 2smax +1 ,                               (209)
                               
                                1,                              r ≥ 2smax .
                               

An example is shown in Figure 2. It is easy to check that
                                    X
                                        ws (r)2 = 1 (∀r ≥ 0).                                                      (210)
                                               s

(Note that at any given point r, at most two of the functions ws (r) are nonzero.)
    We let the direction variable ~θ take on values in the set Gs (S n−1 ). (Assume for the time being
that s ∈/ {“coarse”, “fine”}; we will handle those special cases later.) The set Gs (S n−1 ) contains
grid        on the sphere S n−1 , defined using spherical coordinates, with angular spacing π/2⌈s/2⌉ ≈
   √ points √
      s
π/ 2 = π a. This set is defined recursively:

 Gs (S 1 ) = {πt/2⌈s/2⌉ | t ∈ Z, 0 ≤ t ≤ 2 · 2⌈s/2⌉ − 1},                                                          (211)
        k             ⌈s/2⌉                        ⌈s/2⌉                  k−1
 Gs (S ) = {πt/2              | t ∈ Z, 1 ≤ t ≤ 2           − 1} × Gs (S          ) ∪ {0, π} × {“undef”}   (k ≥ 2). (212)

(See Figure 3 for an example.)
                                            ~ as follows:
   We define angular window functions vs,θ~(φ)

                                                              n−1
                                                     ~ =
                                                              Y
                                               vs,θ~(φ)             us,θj (φj ),                                   (213)
                                                              j=1

where
                                          us,θj (φj ) = c(2⌈s/2⌉ |φj − θj |/2).                                    (214)

                                                               52
       Figure 3: G6 (S 2 ), the set of grid points on the sphere S 2 ⊂ R3 , with angular spacing π/8.


This requires some further explanation.
     Intuitively, us,θj (φj ) is a one-dimensional “bump” function centered around θj , and vs,θ~(φ) ~ is a
product of these functions.
     Note that, for the first n − 2 coordinates j = 1, . . . , n − 2, us,θj (φj ) is defined on the interval
[0, π], whereas for the last coordinate j = n − 1, us,θj (φj ) is defined on the circle (−π, π]; in this
latter case, we interpret |φj − θj | as the shortest-path distance around the circle.
     Also, in the definition of vs,θ~ ( ~
                                       φ), we simply omit those factors that have θj = “undef” or φj =
“undef”. We claim that this is a natural thing to do, in that it yields a simple geometric picture.
Intuitively, θj = “undef” means that θ~ is located on a pole of the sphere, with some coordinate θi
(i < j) equal to 0 or π. Then this construction produces a bump function that covers a circular
region around the pole, and so does not depend on φj . On the other hand, if φj = “undef”, then φ         ~
is located on a pole of the sphere, with some coordinate φi (i < j) equal to 0 or π. If θi 6= φi , then
us,θi (φi ) = 0, hence vs,θ~(φ)~ = 0, independent of φj . If θi = φi , then ~θ is located on a pole, hence
      ~ does not depend on φj .
v ~ (φ)
 s,θ
    Note that at least the first (j = 1) factor will always be defined, since θ1 is always defined
whenever θ~ ∈ Gs (S n−1 ), and φ1 is always defined whenever ~k 6= ~0 (we can ignore the case of ~k = ~0,
because it is relevant only when s = “coarse”, in which case we will not use these angular windows).
    Finally, in the special case where s = “coarse” or “fine”, we do not resolve any directions ~      θ.
Instead, we fix θ~ = “undef”, and we define the angular window to be trivial, vs,θ~(φ)
                                                                                     ~ = 1.
    We now show how to perform the operation X that maps

                                     |~ki|0, ~0i 7→ |~ki   χs,θ~ (~k)|s, θi.
                                                                         ~
                                                         X
                                                                                                   (215)
                                                     s,θ~


We will do this by converting ~k to spherical coordinates (r, φ),
                                                              ~ performing an operation X ′ that




                                                    53
creates the superposition over s and ~
                                     θ, then converting back to Cartesian coordinates:

                             |~ki|0, ~0i|0, ~0i 7→ |~ki|r, φi|0,
                                                           ~     ~0i

                                                7→ |~ki|r, φi
                                                           ~                    ~     ~
                                                              X
                                                                   ws (λr)vs,θ~(φ)|s, θi
                                                              s,θ~

                                             = |~ki|r, ~             χs,θ~ (~k)|s, ~                (216)
                                                            X
                                                       φi                          θi
                                                              s,θ~

                                             7→ |~ki|0, ~0i          χs,θ~(~k)|s, θi.
                                                                                  ~
                                                              X

                                                              s,θ~

The operation X ′ is implemented recursively, acting on the variables r, φ1 , . . . , φn−1 one at a time:
// The “s” register
If λr < 2smin , then let s1 = “coarse” and s2 = smin .
Else if λr > 2smax , then let s1 = smax and s2 = “fine”.
Else, let s1 = ⌊lg(λr)⌋ and s2 = ⌈lg(λr)⌉.
If s1 = s2 , then set the “s” register to |s1 i.
Else, set the “s” register to ws1 (λr)|s1 i + ws2 (λr)|s2 i.

// The “θ1 ” register
If s ∈ {“coarse”, “fine”}, then set the “θ1 ” register to |“undef”i.
Else, begin:
      Let τ1 = (π/2s )⌊φ1 (2s /π)⌋ and τ2 = (π/2s )⌈φ1 (2s /π)⌉.
      If τ1 = τ2 , then set the “θ1 ” register to |τ1 i.
      Else, set the “θ1 ” register to us,τ1 (φ1 )|τ1 i + us,τ2 (φ1 )|τ2 i.
      // Note, φ1 6= “undef”, since otherwise we would have s = “coarse”
      // Note, if φ1 ∈ {0, π}, then τ1 = τ2 , hence θ1 ∈ {0, π}
End.
Recurse on the “θ2 ” register.

// The “θℓ ” register, for ℓ = 2, . . . , n − 2
If θℓ−1 ∈ {0, π, “undef”}, then set the “θℓ ” register to |“undef”i.
Else, begin:
      Let τ1 = (π/2s )⌊φℓ (2s /π)⌋ and τ2 = (π/2s )⌈φℓ (2s /π)⌉.
      If τ1 = τ2 , then set the “θℓ ” register to |τ1 i.
      Else, set the “θℓ ” register to us,τ1 (φℓ )|τ1 i + us,τ2 (φℓ )|τ2 i.
      // Note, φℓ 6= “undef”, since otherwise we would have, in some previous iteration k,
      // φk ∈ {0, π}, hence θk ∈ {0, π}, and θℓ−1 ∈ {0, π, “undef”}
      // Note, if φℓ ∈ {0, π}, then τ1 = τ2 , hence θℓ ∈ {0, π}
End.
Recurse on the “θℓ+1 ” register.

// The “θn−1 ” register
If θn−2 ∈ {0, π, “undef”}, then set the “θn−1 ” register to |“undef”i.
Else, begin:
      Let τ1 = (π/2s )⌊φn−1 (2s /π)⌋ and τ2 = (π/2s )⌈φn−1 (2s /π)⌉.
      If τ1 = τ2 , then set the “θn−1 ” register to |τ1 i.

                                                         54
       Else, set the “θn−1 ” register to ũs,τ1 (φn−1 )|τ1 i + ũs,τ2 (φn−1 )|τ2 i.
       // Note, φn−1 6= “undef”, since otherwise we would have, in some previous iteration k,
       // φk ∈ {0, π}, hence θk ∈ {0, π}, and θn−2 ∈ {0, π, “undef”}
End.


    This construction yields a fast quantum curvelet transform using smooth window functions.
Note that we can carry out this construction using other choices of the function c(x), which lead to
different window functions χs,θ~ (~k). We only need c(x) to satisfy the identity c(x)2 + c( π2 − x)2 = 1
(for all 0 ≤ x ≤ π/2).
    For instance, we can define
                                          (
                                            cos(h(x)), 0 ≤ x ≤ π/2,
                                   c(x) =                                                          (217)
                                            0,         x > π/2,

where h(x) is any increasing function that satisfies h(0) = 0, h( π2 ) = π2 , and h( π2 − x) = π2 − h(x)
(for all 0 ≤ x ≤ π/2).
    In particular, if we set h(x) = π2 sin2 x, then the resulting function c(x) is C 1 -smooth. Thus we
get window functions χs,θ~(~k) that are C 1 -smooth, and are qualitatively similar to the ones used in
Sections 3-5 of this paper.


F      Quantum Algorithms using the Curvelet Transform
F.1     Single-shot measurement of a quantum-sample state
Here we analyze a “continuous” analogue of our single-shot measurement procedure for finding the
center of a ball.
   First, we claim that a ≤ η with probability ≥ Ω(ν 2 ). By Theorem 3, we have

                                     Pr[a ≤ η] ≥ (0.19)η(1 − n1 ).                                (218)

Note that η ≥ Ω(ν 2 ), which follows from the definition of η and the fact that µ = νβ ≥ ν β̃/2. This
shows the claim.
    From this point on, all probabilities are conditioned on having a ≤ η.
    Without loss of generality, assume ~c = ~0. The algorithm succeeds when it outputs a point close
to 0. Let Π1 be the projector onto the subspace orthogonal to ~θ, and let Π2 be the projector onto
   ~
the direction ~
              θ. We will show that, with constant probability, |Π1~b| is small and |Π2~b| is not too
large.
    Let X = |Π1~b|2 , µX = E(X), and let Y = |Π2~b|2 , µY = E(Y ). By Markov’s inequality,

                               Pr[X ≥ 3µX ] ≤ 13 ,     Pr[Y ≥ 3µY ] ≤ 31 .

Then, the union bound implies:

                 Pr[X ≤ 3µX and Y ≤ 3µY ] ≥ 1 − Pr[X ≥ 3µX ] − Pr[Y ≥ 3µY ] ≥ 13 .

So, with probability ≥ 1/3, we have X ≤ 3µX and Y ≤ 3µY .
    We now rewrite this in terms of |Π1~b| and |Π2~b|. From Theorem 3, we know that

                       µX ≤ ηβ 2 (14300 + (Q1 /n)),     µY ≤ β 2 (242 + (Q2 /n)),

                                                  55
for some constants Q1 and Q2 . So, we have
                        √ √ p                                        √ p
                |Π1~b| ≤ 3 ηβ 14300 + (Q1 /n),            |Π2~b| ≤    3β 242 + (Q2 /n).            (219)

    This shows that |Π1~b| (the error orthogonal to θ)
                                                    ~ is small. Indeed, substituting in our choice of
η, and using the fact that β/β̃ ≤ 1, we see that

                                             |Π1~b| ≤ √12 µ.                                       (220)

   However, |Π2~b| (the error parallel to θ)
                                          ~ is not so small. So the algorithm tries to guess this error
and output a corrected point. It succeeds when
                                         √ p
                               Π2~b − u( 3β̃ 242 + (Q2 /n))~θ ≤ √12 µ.                            (221)

Call this event E.√The pprobability of E is the probability that a random    point chosen uniformly
                                                                    1
from the interval 3β̃ 242 + (Q2 /n) · [−1, 1] lies within distance 2 µ of some fixed point in the
                                                                   √
                           √ p
(possibly smaller) interval 3β 242 + (Q2 /n) · [−1, 1]. This probability is lower-bounded by

                                    √1 µ
                                                         1          µ
                      Pr[E] ≥ √ p 2              = √ p                 ,                           (222)
                             2 3β̃ 242 + (Q2 /n)  2 6 242 + (Q2 /n) β̃

which is ≥ Ω(ν), since µ = νβ ≥ ν β̃/2.
   So the algorithm succeeds with probability ≥ Ω(ν 3 ). This proves Theorem 5. 

    Finally, we argue that, when the grid G = (σZ)n ∩ [−L, L)n is chosen properly, the discrete
algorithm will behave like the continuous one. Recall from Section 6 that we can approximate a
function f on Rn with a function f2 on G, provided that most of the probability mass of f lies within
distance L of the origin, and most of the probability mass of fˆ lies within distance 2σ
                                                                                       1
                                                                                         of the origin.
This holds for our algorithm, provided that:
                                                        100    1
                                       R + β ≤ L,           ≤    .                                 (223)
                                                        λη    2σ
(The first condition follows immediately, since f is supported on a ball. The second condition follows
from the decay of fˆ; details omitted.) These conditions hold whenever

                                                    πe µ2       1
                               L ≥ R + β̃,    σ≤                       .                           (224)
                                                    600 β̃ 14300n + Q1

    Also, we argue that the discretization of the “direction” variable θ~ will not introduce too much
error in the output of the algorithm. Our algorithm constructs a line ℓ = {~b + λ~θ | λ ∈ R}, and if
                                                                           √
θ~ were a continuous variable, this line would pass within distance O( aβ) of the center ~c. Recall
                                                                                 √
from Section 6 that the discrete curvelet transform resolves ~θ within error ± a in angular distance.
Since ~b lies at distance O(β) from the center ~c, the error in θ~ can increase the distance from ℓ to ~c
                 √
by at most O( aβ). Thus the error in the output of the algorithm increases by at most a constant
factor.
    We can bound the running time of our algorithm as follows. Let M be the number of grid points
along one direction. Then M = 2L/σ, and the running time is ≤ poly(n, log M ). Say we choose L
and σ so that the above inequalities are tight (up to constant factors). Then M ≤ O(Rβ̃n/µ2 ), and
the running time is ≤ poly(n, log R, log β̃, log µ1 ).

                                                   56
F.2    Quantum algorithm for finding the center of a radial function
Here we analyze the “continuous” analogue of our algorithm for finding the center of a radial function.
    First, consider what happens for each i ∈ {1, 2}.
    We quantum-sample over a ball of radius R′ around ~0, then measure the value of f , and get a
superposition over a shell of radius β (i) around ~c. If the shell is too large, it will not lie completely
within our original ball, so we only get a fragment of the shell. However, if β (i) ≤ R′ − R, then we
are guaranteed to get a complete shell.
    We claim that we observe β (i) ≤ R′ − R with constant probability. To see this, write:
                                         volume of ball of radius R′ − R around ~c
                    Pr[β (i) ≤ R′ − R] =
                                           volume of ball of radius R′ around ~0                     (225)
                                         (R′ − R)n
                                       =           = (1 − n1 )n ≥ e−1.2 > 0.30,
                                           (R′ )n

using the fact that 1 − x ≥ e−(1.2)x for all 0 ≤ x ≤ 1/4 (recall that we assumed n ≥ 4).
    Our algorithm does not know the shell’s true radius β (i) , so it uses β̃ (i) = R′ − R as an estimate.
We claim that β (i) ≤ β̃ (i) ≤ (3/2)β (i) , with constant probability. Observe that

                                         volume of ball of radius (2/3)(R′ − R) around ~c
            Pr[β (i) < (2/3)(R′ − R)] =
                                               volume of ball of radius R′ around ~0                 (226)
                                         ((2/3)(R′ − R))n
                                       =                   = (2/3)n (1 − n1 )n .
                                               (R′ )n
So
                    Pr[(2/3)(R′ − R) ≤ β (i) ≤ R′ − R] = (1 − ( 23 )n )(1 − n1 )n
                                                                                                     (227)
                                                          ≥ (1 − 0.20)(0.30) = 0.24,

using the fact that n ≥ 4.
    Next, we claim that we observe a(i) ≤ η (i) , with constant probability. This follows from Theorem
4:
                                        Pr[a(i) ≤ η (i) ] > 0.045.                                (228)
     From this point on, we take probabilities conditioned on a(i) ≤ η (i) .
                                                         (i)
     Without loss of generality, assume ~c = ~0. Let Π1 be the projector onto the subspace orthogonal
                    (i)
to θ~(i) , and let Π2 be the projector onto the direction θ~(i) .
                        (i)                     (i)
     We claim that |Π1 ~b(i) | is small, and |Π2 ~b(i) | is of order β, with constant probability. We use
the same argument as in the previous section, together with Theorem 4. We define ε(i) = δ/β (i) .
We get that, with probability ≥ 1/3,

           (i)      √ q                                         (i)      √
       |Π1 ~b(i) | ≤ 3 (n − 1)ε(i) β (i) 761 + (Q1 /n), |Π2 ~b(i) | ≤ 3β (i) 23 + (Q2 /n2 ),
                                        p                                      p
                                                                                                    (229)

for some constants Q1 and Q2 .
    Using the definition of ε(i) , and the fact that β (i) ≤ R′ − R = (n − 1)R, this implies that
        (i)        √        √ p                           (i)     √
      |Π1 ~b(i) | ≤ 3(n − 1) δR 761 + (Q1 /n), |Π2 ~b(i) | ≤ 3(n − 1)R 23 + (Q2 /n2 ).
                                                                             p
                                                                                                  (230)

   The algorithm carries out this procedure twice, for i = 1 and 2. With constant probability, this
produces two lines, ℓ1 = {~b(1) + λθ~(1) | λ ∈ R} and ℓ2 = {~b(2) + λθ~(2) | λ ∈ R}, which both pass near

                                                    57
                                       p1 , p2                                                     p1
                                                                           b         ϕ

                   q1                                              q1                          c

                                                                          a
                        ~c        q2                                                     q2′


     ℓ1                                             ℓ1


                             ℓ2                                                ℓ′2


                                                  Figure 4:


the point ~c. The algorithm then checks that these lines are nearly orthogonal, and if they are, it
returns the point on ℓ1 closest to ℓ2 . A straightforward calculation shows that this point is given by
−s+rt ~(1)
 1−r 2
       θ + ~b(1) .
    First, we claim that the lines ℓ1 and ℓ2 are nearly orthogonal (|~θ(1) · θ~(2) | ≤ 3/4) with at least
constant probability.
   We want to upper-bound the probability that |~θ(1) · θ~(2) | > 3/4. Recall that these are independent
random vectors, chosen uniformly from the unit sphere S n−1 in Rn . It follows that

                                  Pr[|θ~(1) · θ~(2) | > 3/4] = Pr[|x1 | > 3/4],                          (231)

where ~x = (x1 , . . . , xn ) is a random vector chosen uniformly from S n−1 . Note that E(~x) = ~0, hence
E(x1 ) = 0; also, E(|~x|2 ) = 1, hence E(x21 ) = 1/n. Then by Markov’s inequality,

                         Pr[|x1 | > 3/4] = Pr[x21 > 9/16] ≤ 16 1   4
                                                             9 n ≤ 9 (for n ≥ 4).                        (232)

Thus, we observe |~  θ (1) · ~
                             θ (2) | ≤ 3/4, with probability ≥ 5/9. (This is a rather weak bound, especially
                                                                                                          √
when n is large, but it is adequate for our purposes. Actually, it is the case that |~θ(1) ·~θ(2) | ≤ O(1/ n),
with probability ≥ Ω(1).)
    Next, we claim that when ℓ1 and ℓ2 are nearly orthogonal (|~θ(1) · θ~(2) | ≤ 3/4), the point on ℓ1
closest to ℓ2 (call it p1 ) is close to ~c.
    Let q1 be the point on ℓ1 closest to ~c, and let p1 be the point on ℓ1 closest to ℓ2 . Similarly, let q2
be the point on ℓ2 closest to ~c, and let p2 be the point on ℓ2 closest to ℓ1 . (See Figure 4.)
√ We know       p q1 and q2 are both close to ~c: |q1 − ~c| ≤ ∆, and |q2 − ~c| ≤ ∆, where ∆ =
           √ that
  3(n − 1) δR 761 + (Q1 /n). Furthermore, p1 and p2 are close together: |p1 − p2 | ≤ 2∆.
    Now suppose that p1 is far from ~c:
                                                   |p1 − ~c| ≥ 8∆.                                        (233)
From this we will derive a contradiction.


                                                      58
    First, note that p1 is far from q1 :
                                                |p1 − q1 | ≥ 7∆.                                            (234)
   Consider the line ℓ′2 = ℓ2 + (p1 − p2 ). Define another point q2′ = q2 + (p1 − p2 ). The line ℓ′2 is
parallel to ℓ2 , it intersects ℓ1 at p1 , and it passes through q2′ . Note that q2′ is close to ~c: |q2′ −~c| ≤ 3∆.
   Note that p1 is far from q2′ :
                                                  |p1 − q2′ | ≥ 5∆.                                           (235)
    Note that q1 and q2′ are close to each other:

                                                |q1 − q2′ | ≤ 4∆.                                           (236)

   We will use equations (234), (235) and (236) to show that the angle between ℓ1 and ℓ′2 is small.
(See Figure 4.) We have a ≤ 4∆, b ≥ 7∆ and c ≥ 5∆.
   Using the law of cosines, and the fact that x + x1 ≥ 2 for all x > 0, we get:
                                                          2     2
                                                            c +b −a   2
                                |~
                                 θ (1) · θ~(2) | = cos ϕ =
                                                                2bc
                                                   1  c b a2 
                                                 =       + −
                                                   2 b c bc
                                                                                                            (237)
                                                        a2
                                                 ≥1−
                                                        2bc
                                                          (4∆)2           8
                                                 ≥1−                = 1 − 35 > 43 .
                                                        2(7∆)(5∆)

This contradicts our assumption that ℓ1 and ℓ2 are nearly orthogonal.
   So we conclude that p1 is close to ~c, as desired:
                                             √        √ p
                         |p1 − ~c| ≤ 8∆ = 8 3(n − 1) δR 761 + (Q1 /n).                                      (238)

    Finally, using our assumed upper bound on δ, we get that:

                                                  |p1 − ~c| ≤ µ.                                            (239)

So the algorithm succeeds with constant probability. This proves Theorem 6. 

    Finally, we argue that, when the grid G = (σZ)n ∩ [−L, L)n is chosen properly, the discrete
algorithm will behave like the continuous one. Recall from Section 6 that we can approximate a
function f on Rn with a function f2 on G, provided that most of the probability mass of f lies within
distance L of the origin, and most of the probability mass of fˆ lies within distance 2σ
                                                                                       1
                                                                                         of the origin.
This holds for our algorithm, provided that:
                                                         100    1
                                             R′ ≤ L,         ≤    .                                         (240)
                                                          δ    2σ
(The first condition follows immediately, since f is supported on a ball. The second condition follows
from the decay of fˆ; details omitted.)
    Also, we argue that the discretization of the “direction” variable θ~ will not introduce too much
error in the output of the algorithm. The key part of our algorithm involves constructing a line
ℓ = {~b + λ~θ | λ ∈ R}; and if ~θ were a continuous variable, this line would pass within distance
   √
O( aβ) of the center ~c. Recall from Section 6 that the discrete curvelet transform resolves θ~ within

                                                        59
        √
error ± a in angular distance. Since ~b lies at distance O(β) from the center ~c, the error in θ~ can
                                                √
increase the distance from ℓ to ~c by at most O( aβ). Thus the error in the output of the algorithm
increases by at most a constant factor.
    We can bound the running time of our algorithm as follows. Say we choose L and σ so that
the above inequalities are tight (up to constant factors). Also, suppose δ satisfies equation (??)
exactly up to constant factors. Let M be the number of grid points along one direction. Then
M = 2L/σ ≤ O(R2 n3 /µ2 ), and the running time is ≤ poly(n, log M ) ≤ poly(n, log R, log µ1 ).

F.3      Classical lower bound
We will prove a lower bound on classical randomized algorithms for finding the center of a radial
function. Recall that an instance of the problem is specified by an oracle f and parameters n, R, δ
and µ. Let us define m = lg(R/µ). Consider algorithms that query points within some finite subset
D ⊂ Rn . We will show that Ω(nm/ lg(nm)) queries are needed to solve this problem.

Theorem 8 The following holds for any parameters n, R, δ and µ, and for any finite subset D ⊂ Rn .
Let us define m = lg(R/µ). For any classical randomized algorithm that queries points within the
set D and uses at most ( 21 nm)/ lg( 21 nm) oracle queries, there exists a problem instance (depending
on D, and having the specified parameters n, R, δ and µ) that causes the algorithm to fail with
probability at least 1 − 2−nm/2 .

    The assumption that the algorithm queries points within the set D can be understood intuitively
as follows. We are assuming that the algorithm follows some (arbitrary) convention for how it
describes points in Rn when it queries the oracle. We let D ⊂ Rn be the set of points that can be
queried, and note that D must be finite: if the algorithm runs in time T , then clearly |D| ≤ 2T .
    Note that this assumption does not weaken our lower bound. The assumption is needed because
the construction of the hard instance depends on D; however, the actual lower bound (i.e., the
number of oracle queries and the resulting probability of success) is independent of D.

Proof: We will use the following version of Yao’s minimax lemma, due to Rademacher and Vempala
[24]:

Lemma 9 Let I be a set of problem instances and A be a set of deterministic algorithms. For any
probability measure π over I, and any probability measure ν over A, we have that

   inf    Pr [algorithm A fails on instance I] ≤ sup    Pr [algorithm A fails on instance I].     (241)
  A∈A I∼π(I)                                      I∈I A∼ν(A)

We will use the following approach. First we will fix a probability distribution π over instances, and
prove that the best deterministic algorithm still fails with high probability. Note that a randomized
algorithm is simply a probability distribution over deterministic algorithms; so the minimax lemma
implies that for any randomized algorithm ν, there exists an instance that causes the algorithm to
fail with high probability.
     We let A be the set of deterministic algorithms that query points within the subset D and make
at most ℓ queries, for some ℓ to be specified later.
     We let I be the set of problem instances, such that n, R, δ and µ are fixed, but f and ~c can vary.
That is, we fix the dimension n, the radius R of the ball in which the center lies, the thickness δ of
the spherical shells, and the desired accuracy µ. We define m = lg(R/µ), which is fixed. However,
the values returned by the radial function f , and the location of its center ~c, are arbitrary.


                                                  60
    We now fix a distribution π on problem instances. Random instances according to this distribu-
tion are constructed as follows. First, we choose the center point ~c uniformly at random from the
ball of radius R around the origin. Let f be of the form

     f (~x) = [sk if ~x ∈ Ak ], where Ak = {~x | kδ ≤ |~x − ~c| < (k + 1)δ}, for k = 0, 1, 2, . . . .   (242)

Next, we choose the values of f on the points in the set D (these are the points that the algorithm
can query). Equivalently, we will choose the values of sk , for those k such that Ak ∩ D 6= ∅. Let K
be the set of those k, and note that |K| ≤ |D|. Let S = {1, 2, . . . , |D|}. Choose a random injective
map σ : K ֒→ S, and then set sk = σ(k).
     Consider any deterministic algorithm A ∈ A, and let U be the set of possible outputs of the
algorithm. We claim that |U | ≤ 2ℓ lg ℓ . To see this, note that the algorithm A can be described as a
decision tree, where each node represents a query to the oracle f , and the algorithm chooses which
branch to follow depending on the oracle’s answer. We claim that after seeing the answer to its
k’th query, the algorithm can have at most k distinct branches. This is because, while the oracle
can return many different values, they are meaningless except in cases where the oracle returns the
same value as it did for a previous query. (Note that, for any permutation σ on the range of f ,
we can replace the oracle f with σ ◦ f , to get a new instance of the problem that has the same
desired solution. These two instances occur with equal probability under the distribution π.) So,
when the algorithm receives the answer to its k’th query, all it can do is compare that value to the
answers to its previous queries. The number of branches is at most the number of distinct values
that have been seen previously (which is at most k − 1), plus 1 (if the new value does not match
any of the previous ones); thus the number of branches is at most k. Finally, note that the size of
U is at most the number of leaves at the final level of the decision tree, i.e., after the ℓ’th query. So
|U | ≤ 1 · 2 · 3 · · · ℓ ≤ ℓℓ = 2ℓ lg ℓ .
     Thus we can upper-bound the probability that algorithm A succeeds on a random instance
I ∼ π(I):

                           Pr [algorithm A succeeds on instance I]
                       I∼π(I)
                                                                  X
                               ≤ Pr[∃~z ∈ U s.t. |~z − ~c| ≤ µ] ≤   Pr[|~z − ~c| ≤ µ]
                                    ~c                                   ~c
                                                                   ~∈U
                                                                   z
                                    X volume of ball of radius µ           µ n                        (243)
                                ≤                                   = |U |
                                         volume of ball of radius R         R
                                    ~∈U
                                    z
                                      ℓ lg ℓ −mn
                                ≤2       2         .

Now suppose that ℓ, the number of queries, is at most ( 12 nm)/ lg( 21 nm). Then
                             1
                             2 nm
                ℓ lg ℓ ≤              (lg( 12 nm) − lg lg( 21 nm)) ≤ 12 nm (assuming nm ≥ 4).           (244)
                           lg( 12 nm)
So we have
                             Pr [algorithm A succeeds on instance I] ≤ 2−nm/2 ,                         (245)
                           I∼π(I)

and this holds for all algorithms A ∈ A. So

                       inf      Pr [algorithm A fails on instance I] ≥ 1 − 2−nm/2 .                     (246)
                       A∈A I∼π(I)

Now plug into the minimax lemma and the result follows. 

                                                       61
F.4     Finding the center through multiple iterations
Here we analyze the “continuous” analogue of our algorithm for finding the center of a radial function.
    First, we analyze the procedure OneRound(). Consider what happens for each i ∈ {1, 2}.
    We quantum-sample over a ball of radius R′ around ~0, then measure the value of f , and get a
superposition over a shell of radius β (i) around ~c. If the shell is too large, it will not lie completely
within our original ball, so we only get a fragment of the shell. However, if β (i) ≤ R′ − R, then we
are guaranteed to get a complete shell.
    We claim that we observe β (i) ≤ R′ − R with probability ≥ 1 − O( S1 ). To see this, write:

                                       volume of ball of radius R′ − R around ~c
                  Pr[β (i) ≤ R′ − R] =
                                         volume of ball of radius R′ around ~0                       (247)
                                       (R′ − R)n          1 n
                                     =           = (1 − nS  ) ≥ e−(1.2)/S ≥ 1 − 1.2
                                                                                 S ,
                                         (R′ )n

using the fact that 1 − x ≥ e−(1.2)x for all 0 ≤ x ≤ 1/4 (recall that we assumed n ≥ 4).
    Our algorithm does not know the shell’s true radius β (i) , so it uses β̃ (i) = R′ − R as an estimate.
We claim that β (i) ≤ β̃ (i) ≤ Sβ (i) , with probability ≥ 1 − O( S1 ). Observe that

                                         volume of ball of radius (1/S)(R′ − R) around ~c
             Pr[β (i) < (1/S)(R′ − R)] =
                                              volume of ball of radius R′ around ~0                  (248)
                                         ((1/S)(R′ − R))n
                                       =                    = (1/S)n (1 − nS
                                                                           1 n
                                                                             ) .
                                              (R′ )n
So

                   Pr[(1/S)(R′ − R) ≤ β (i) ≤ R′ − R] = (1 − ( S1 )n )(1 − nS
                                                                            1 n
                                                                              )
                                                                                                     (249)
                                                           ≥ (1 − S1 )(1 − 1.2     2.2
                                                                            S )>1− S .

     Next, we claim that we observe a(i) ≤ η (i) , with constant probability. This follows from Theorem
4:
                                           Pr[a(i) ≤ η (i) ] > 0.045.                                (250)
     From this point on, we take probabilities conditioned on a(i) ≤ η (i) .
                                                         (i)
     Without loss of generality, assume ~c = ~0. Let Π1 be the projector onto the subspace orthogonal
                       (i)
to θ~(i) , and let Π2 be the projector onto the direction θ~(i) .
                           (i)                  (i)
     We claim that |Π1 ~b(i) | is small, and |Π2 ~b(i) | is of order β, with probability ≥ 1 − O( S1 ). We
use a similar argument as in the previous section, together with Theorem 4. We define ε(i) = δ/β (i) .
We get that, with probability ≥ 1 − S2 ,

             (i)
                          √ q               q
                                                                   (i)
                                                                            √      q
           |Π1 ~b(i) | ≤ S (n − 1)ε(i) β (i) (507 + Qn1 ) · S, |Π2 ~b(i) | ≤ Sβ (i) 23 + Q 2
                                                                                          n2
                                                                                             ,        (251)

for some constants Q1 and Q2 .
    Using the definition of ε(i) , and the fact that β (i) ≤ R′ − R = (nS − 1)R < nSR, this implies
that
                   (i)
                                      √ q                   (i)
                                                                            q
                 |Π1 ~b(i) | ≤ S 3/2 n δR 507 + Qn1 , |Π2 ~b(i) | ≤ S 3/2 nR 23 + Q
                                                                                  n2
                                                                                    2
                                                                                      .       (252)

    The algorithm carries out this procedure twice, for i = 1 and 2. With probability ≥ 1 − O( S1 ),
this produces two lines, ℓ1 = {~b(1) + λθ~(1) | λ ∈ R} and ℓ2 = {~b(2) + λθ~(2) | λ ∈ R}, which both pass

                                                      62
near the point ~c. The algorithm then checks that these lines are nearly orthogonal, and if they are,
it returns the point on ℓ1 closest to ℓ2 . A straightforward calculation shows that this point is given
by −s+rt   ~(1) + ~b(1) .
     1−r 2 θ
    First, we claim that the lines ℓ1 and ℓ2 are nearly orthogonal (|~θ(1) · θ~(2) | ≤ 3/4) with probability
≥ 5/9. This follows from the same argument as in the previous section.
    Next, we claim that when ℓ1 and ℓ2 are nearly orthogonal (|~θ(1) · θ~(2) | ≤ 3/4), the point on ℓ1
closest to ℓ2 (call it p1 ) is close to ~c. Using the same argument as in the previous section, we conclude
that:
                                                            √ q
                                        |p1 − ~c| ≤ 8S 3/2 n δR 507 + Qn1 .                           (253)
   Finally, using our assumed upper bound on δ, we get that:
                                                √ p
                                     |p1 − ~c| ≤ R µ/2.                                               (254)

    In summary, we have shown that the procedure OneRound() has the following two properties:
(1) OneRound() returns a point q~ (rather than “no answer”) with probability

                                         ≥ (0.045)2 · 59 > 0.0011,                                    (255)
                                                                                   √ p
and (2) when OneRound() returns a point q~, that point q~ lies within distance      R µ/2 of the center
point ~c, with probability
                                                2
                                                               2
                             ≥ (1 − 2.2
                                     S  )(1 − 2
                                              S )   > (1 − 4.2      8.4
                                                            S ) >1− S .                               (256)


    We now analyze the complete algorithm, consisting of multiple iterations.
    First, let us upper-bound the number of iterations, assuming that every iteration is successful.
Let k denote the number of iterations. We claim that k ≤ ⌈lg lg 2R µ ⌉.
    Let Ri denote the value  √ of p
                                  Rcur following the i’th iteration, so we have R0 = R (when the
algorithm starts), Ri+1 = Ri µ/2 (the recurrence relation), and Rk ≤ µ (when the algorithm
finishes).                                                                                p
                        Ri                         R
    Let us define R̃i = µ/2 . Then we have R̃0 = µ/2  (when the algorithm starts), R̃i+1 = R̃i (the
recurrence relation), and R̃k ≤ 2 (when the algorithm finishes).
                                              k
    It is easy to see that R̃k = (R̃0 )(1/2) , and a straightforward calculation shows that it suffices to
set k = ⌈lg lg 2R
                µ ⌉.
    Next, we show that the algorithm succeeds (i.e., every iteration is successful) with constant prob-
ability. First, consider a single iteration. The algorithm makes ntries attempts to run OneRound(),
and it succeeds if at least one of those attempts returns a point q~ that lies near the center. The prob-
ability that OneRound() returns “no answer” every time is ≤ (0.9989)ntries = (0.9989)910 log S ≤ 1/S.
So the probability that OneRound() returns a point q~ at least once is ≥ 1 − S1 . When this happens,
the point q~ is near the center with probability ≥ 1 − 8.4    S . So the iteration succeeds with overall
probability ≥ (1 − S1 )(1 − 8.4S  ) >  1 − 9.4
                                            S   = 1 −   1
                                                      niter .
    The algorithm makes niter iterations, and it succeeds if all of the iterations succeed. This occurs
                             1
with probability ≥ (1 − niter    )niter ≥ 1/e2 . (We assumed that R ≥ 8µ, so niter ≥ 2, and we used the
fact that 1 − x ≥ e−2x for all 0 ≤ x ≤ 1/2.) So the algorithm succeeds with constant probability.
                                                                                           2R
    Finally, note that the number of oracle queries is 2ntries niter ≤ O(lg lg 2R
                                                                                µ lg lg lg µ ). This proves
Theorem 7. 


                                                    63
    Finally, we argue that, when the grid G = (σZ)n ∩ [−L, L)n is chosen properly, the discrete
algorithm will behave like the continuous one. Recall from Section 6 that we can approximate a
function f on Rn with a function f2 on G, provided that most of the probability mass of f lies within
distance L of the origin, and most of the probability mass of fˆ lies within distance 2σ
                                                                                       1
                                                                                         of the origin.
This holds for our algorithm, provided that:
                                                   100    1
                                        R′ ≤ L,        ≤    .                                    (257)
                                                    δ    2σ
(The first condition follows immediately, since f is supported on a ball. The second condition follows
from the decay of fˆ; details omitted.)
    Also, we argue that the discretization of the “direction” variable θ~ will not introduce too much
error in the output of the algorithm. The key part of our algorithm involves constructing a line
ℓ = {~b + λθ~ | λ ∈ R}; and if θ~ were a continuous variable, this line would pass within distance
   √
O( aβ) of the center ~c. Recall from Section 6 that the discrete curvelet transform resolves θ~ within
        √
error ± a in angular distance. Since ~b lies at distance O(β) from the center ~c, the error in θ~ can
                                                 √
increase the distance from ℓ to ~c by at most O( aβ). Thus the error in the output of the algorithm
increases by at most a constant factor.
    We can bound the running time of our algorithm as follows. Say we choose L and σ so that
the above inequalities are tight (up to constant factors). Also, suppose δ satisfies equation (??)
exactly up to constant factors. Let M be the number of grid points along one direction. Then
M = 2L/σ ≤ O(R2 n3 /µ2 ), and the running time is ≤ poly(n, log M ) ≤ poly(n, log R, log µ1 ).




                                                  64
