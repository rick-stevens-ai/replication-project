<!-- BACKFILL 2026-07-06: pdftotext -layout fallback (Marker not installed locally).
     Source: paper.pdf (fetched from https://math.nyu.edu/faculty/greengar/poiss2d.pdf)
     SHA256: 6634e8d832c85a546a5ef4fe2c08edc5db235195d181b07edde8979e411c091e
     DOI: 10.1137/S1064827500369967
     Backfill this later from the central Marker corpus keyed on the above sha256 or DOI. -->

SIAM J. SCI. COMPUT.                              c
                                                   2001 Society for Industrial and Applied Mathematics
Vol. 23, No. 3, pp. 741–760




 A NEW FAST-MULTIPOLE ACCELERATED POISSON SOLVER IN
                  TWO DIMENSIONS∗
                         FRANK ETHRIDGE† AND LESLIE GREENGARD‡
    Abstract. We present an adaptive fast multipole method for solving the Poisson equation in
two dimensions. The algorithm is direct, assumes that the source distribution is discretized using
an adaptive quad-tree, and allows for Dirichlet, Neumann, periodic, and free-space conditions to be
imposed on the boundary of a square. The amount of work per grid point is comparable to that of
classical fast solvers, even for highly nonuniform grids.

      Key words. fast multipole method, Poisson equation, adaptive reﬁnement, fast Poisson solver

      AMS subject classiﬁcations. 31A10, 35J05, 65R10, 78A30

      PII. S1064827500369967


     1. Introduction. A variety of problems in scientiﬁc computing involve the so-
lution of the Poisson equation
(1)                                          ∆ψ = f,
subject to appropriate radiation or boundary conditions. In simple geometries (cir-
cular or rectangular domains) with regular grids, there are well-known fast direct
solvers [6, 7] which typically rely on the fast Fourier transform (FFT) and are well
suited to the task. When either restriction is relaxed, however, these methods no
longer apply. Since practical problems tend to involve complex geometries, highly
inhomogeneous source distributions f , or both, there has been a lot of eﬀort directed
at developing alternative approaches. Most currently available solvers rely on itera-
tive techniques using multigrid, domain decomposition, or some other preconditioning
strategy [5, 9, 21]. Unfortunately, while such multilevel strategies can achieve nearly
optimal eﬃciency in theory, they require an appropriate hierarchy of coarse grids
which is not provided in practice. Although there has been signiﬁcant progress in this
direction [1, 2, 10, 11, 20, 23], the available solvers compare unfavorably with the fast
direct solvers in terms of work per grid point.
     In this paper, we describe an integral equation method for solving the Poisson
equation in two dimensions which is direct, high order accurate, insensitive to the
degree of adaptive mesh reﬁnement, and accelerated by the fast multipole method
(FMM) [16, 17, 26]. It is competitive with standard fast solvers in terms of work per
grid point. This is a rather stringent test, since we compare the time for a classical,
FFT-based solver using N mesh points with our adaptive, FMM-based solver using
the same number of points, ignoring the fact that the latter solver uses grids which
are highly inhomogeneous. We allow for the imposition of various combinations of
free-space, periodic, Dirichlet, and Neumann conditions on the boundary of a square.
     Earlier work on FMM-based integral equation schemes in two dimensions includes
[15, 22, 29]. The paper [22] describes a fast Poisson solver for complex geometries,
   ∗ Received by the editors April 3, 2000; accepted for publication (in revised form) December 8,

2000; published electronically August 15, 2001.
     http://www.siam.org/journals/sisc/23-3/36996.html
   † Department of Computer Science, Yale University, New Haven, CT 06520 (ethridge@cs.yale.edu).
   ‡ Courant Institute of Mathematical Sciences, New York University, New York, NY 10012

(greengard@cims.nyu.edu). The work of this author was supported by the Applied Mathematical
Sciences Program of the U.S. Department of Energy under contract DEFGO288ER25053.
                                                741
742                  FRANK ETHRIDGE AND LESLIE GREENGARD


where the boundary can be arbitrarily shaped and multiply-connected, but where
the right-hand side is speciﬁed on a uniform underlying mesh. The other two papers
discuss the inversion of (1) in free space by evaluation of the analytic solution
                                        
                                    1
(2)                       ψ(x) =            f (y) log(|x − y|) dy.
                                   2π   D


The algorithms of both [15] and [29] are highly adaptive, with the former relying on a
quad-tree and the latter relying on an unstructured triangulation. Neither, however,
goes beyond the free-space problem.
    The present approach is similar to that outlined in [15] but diﬀers in several
respects.
     1. In the method of [15], one solves local Poisson problems with spectral methods
        on each leaf node of a quad-tree data structure and then patches the solutions
        together using the FMM in a domain decomposition approach. Here, we apply
        the FMM directly to the volume integral, using high order quadratures.
     2. We incorporate a new version of the FMM described in [19], which is based
        on diagonal forms for translation operators (see section 3.8).
     3. We incorporate the method of images to solve a variety of boundary value
        problems on a square (with adaptive reﬁnement).
     4. For fourth and sixth order accurate discretizations, we use locally uniform
        meshes, compatible with adaptive mesh reﬁnement (AMR) data structures
        [3]. For eighth order accuracy, we follow [13, 15, 24] and rely on local spectral
        meshes.
    The paper is organized as follows. In section 2, we outline the relevant potential
theory, with particular emphasis on the method of images. In section 3, we describe
the fast multipole algorithm itself, and in section 4, we present several numerical
examples. Finally, it should be noted that our algorithm shares a number of features
with the recently developed scheme of [12] for solving the pseudodiﬀerential equation

(3)                                 (−∆)1/2 ψ = ω

in the plane via the integral representation
                                            
                                                ω(y)
                                ψ(x) =                 dy.
                                            R2 |x − y|


    2. Potential theory. To complete a description of a well-posed problem, we
must obviously add to the Poisson equation (1) a speciﬁcation of boundary conditions
on the unit square D. We allow the free-space conditions deﬁned by (2), periodic
boundary conditions, Dirichlet conditions, and Neumann conditions. We can also
handle mixed conditions, but assume that the transition from one type to another
(Dirichlet–Neumann, etc.) occurs only at corners. The solution to all these problems
can be constructed analytically using the method of images.
    For periodic boundary conditions, one simply imagines the entire plane to be tiled
with copies of the source distribution contained in the unit cell D. (How to compute
the inﬂuence of each of these images eﬃciently is discussed in the next section.) For
other boundary conditions, the construction is a bit more subtle. Let us consider, for
             A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                        743

example, the boundary value problem

                                    ∆ψ = f      in D,
                                     ψ = gL     on ΓL ,
(4)                                   ψ = gR    on ΓR ,
                                 ∂ψ/∂n = gT     on ΓT ,
                                 ∂ψ/∂n = gB     on ΓB ,

where ΓL denotes the “left” boundary (x = −0.5, −0.5 ≤ y ≤ 0.5), ΓR denotes the
“right” boundary (x = 0.5, −0.5 ≤ y ≤ 0.5), ΓT denotes the “top” boundary (−0.5 ≤
x ≤ 0.5, y = 0.5), and ΓB denotes the “bottom” boundary (−0.5 ≤ x ≤ 0.5, y = −0.5).
    This problem can be conveniently broken up into two parts. First, we can solve
the Poisson equation:

                                    ∆ψ1 = f     in D,
                                     ψ1 = 0     on ΓL ,
(5)                                   ψ1 = 0    on ΓR ,
                                 ∂ψ1 /∂n = 0    on ΓT ,
                                 ∂ψ1 /∂n = 0    on ΓB .

Then we can solve the Laplace equation with inhomogeneous boundary conditions:

                                   ∆ψ2 = 0      in D,
                                     ψ2 = gL    on ΓL ,
(6)                                  ψ2 = gR    on ΓR ,
                                ∂ψ2 /∂n = gT    on ΓT ,
                                ∂ψ2 /∂n = gB     on ΓB .

Clearly, ψ = ψ1 + ψ2 .
     To solve (5), suppose that we tile the plane with the pattern of images depicted
in Figure 1. The shaded box is the computational domain containing the source
distribution f . fT denotes the even reﬂection of the function f across the top boundary
ΓT , −fR denotes the odd reﬂection of the function f across the right boundary ΓR ,
and −fRT denotes the even reﬂection of the function −fR across the line y = + 12 . It
is easy to verify that the vertical lines x = ± 12 are lines of odd symmetry and that the
horizontal lines y = ± 12 are lines of even symmetry. Thus, the desired homogeneous
boundary conditions are enforced if we account for the ﬁeld due to all images. This
task is simpliﬁed by the observation that the 2 × 2 supercell outlined with dashes in
Figure 1 tiles the plane periodically.
     To handle the inhomogeneous boundary conditions in (6), we recall the following
classical results from potential theory [18, 30].
     Lemma 2.1. Let u(x, y) satisfy the Laplace equation ∆u = 0 in the half-space
y > 0 with Dirichlet boundary conditions u(x, 0) = f (x). Then u(x, y) is given by the
double layer potential
                     ∞                              ∞
                       ∂G                       1                y
        u(x, y) = 2       (x − ξ, y) f (ξ) dξ =                   2    2
                                                                         f (ξ) dξ.
                    −∞ ∂y                       π       −∞ (x − ξ) + y
744                     FRANK ETHRIDGE AND LESLIE GREENGARD



                             f         f         f         f         f
                                        R                   R

                             f         f         f         f         f
                              T         RT        T         RT       T
                                              1111
                                              0000
                                              0000
                                              1111
                                              1111
                                              0000
                                              1111
                                              0000
                             f         f        f
                                              0000
                                              1111         f         f
                                        R     0000
                                              1111
                                              1111
                                              0000          R
                                              1111
                                              0000
                             f         f         f         f         f
                              T         RT        T         RT       T

                             f         f         f         f         f
                                        R                   R

     Fig. 1. A source distribution tiling the plane which solves the Poisson equation with the homoge-
neous boundary conditions described by the system (5). The shaded box represents the computational
domain itself. fT denotes the even reﬂection of the function f across the top boundary ΓT , −fR
denotes the odd reﬂection of the function f across the right boundary ΓR , and −fRT denotes the
even reﬂection of the function −fR across the line y = + 12 . The 2 × 2 “supercell” with the dashed
outline can be seen to tile the plane periodically.


                                                     ∂u
The solution satisfying Neumann boundary conditions ∂n  (x, 0) = g(x) is given by the
single layer potential
                     ∞                          ∞ 
                                              1
        u(x, y) = 2     G(x − ξ, y) g(ξ) dξ =      ln (x − ξ)2 + y 2 g(ξ) dξ.
                     −∞                       π −∞

    Consider now the system of layer potentials depicted in Figure 2. We leave it to
the reader to verify that, from the preceding lemma and symmetry considerations,
the boundary conditions of (6) are satisﬁed. As with the tiling of source distributions,
the task of accounting for the ﬁeld due to all images is simpliﬁed by the observation
that the layer potentials on boundary segments outlined with dots in Figure 2 tile the
plane periodically. The evaluation of layer potentials is discussed in section 3.7.
     3. Data structures and the FMM. We assume that the source distribution
f in (2) is supported inside the unit square D, centered at the origin, on which is
superimposed a hierarchy of reﬁnements (a quad-tree). Grid level 0 is deﬁned to be
D itself, and grid level l + 1 is obtained recursively by subdividing each square at level
l into four equal parts. Using standard terminology, if d is a ﬁxed square at level l,
the four squares at level l + 1 obtained by its subdivision will be referred to as its
children. In order to allow for adaptivity, we do not use the same number of levels
in all regions of D. We do, however, assume that the quad-tree satisﬁes one fairly
standard restriction, namely, that two leaf nodes which share a boundary point must
be no more than one reﬁnement level apart (Figure 3).
     3.1. The volume integral. We restrict our attention, for the moment, to the
free-space problem. Extended volume integrals such as the ones depicted in Figure 1
will be discussed in section 3.6.
     The leaf nodes on which the source distribution is given will be denoted by Di .
               A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                                745

                           -Sbr          Sb                  -Sbr             Sb


                     Drb           Dlb                 Drb          Dlb            Drb
                           -Str          St                  -Str             St


                     Dr            Dl                  Dr           Dl             Dr

                           -Sbr          Sb                  -Sbr             Sb


                     Drb           Dlb                 Drb          Dlb            Drb
                           -Str          St                  -Str             St


                     Dr            Dl                  Dr           Dl             Dr

                           -Sbr          Sb                  -Sbr             Sb
     Fig. 2. A tiling of the plane with layer potentials to solve (6). The computational domain
is indicated with diagonal dashes. Dl denotes a double layer potential with density gL , and Dr
denotes a double layer potential with density gR . Their even reﬂections across the bottom boundary
ΓB are Dlb and Drb, respectively. St denotes a single layer potential with density gT , and Sb
denotes a single layer potential with density gB . Their odd reﬂections across the right boundary ΓR
are −Str and −Sbr, respectively. Symmetry considerations show that all four boundary conditions
are satisﬁed. Note that the layer potentials on boundary segments outlined with dots tile the plane
periodically.



                            i      i          i              i      i          i

                                          s       s
                            i      i                         n      n          i
                                                   -
                                          s       n
                                                   -
                                          s       n
                            i      i                         B
                                                   -                       +
                                          s       n
                                                                          n
                            i      i          n              n


                            i      i
                                                       i                  i
                            i      i


     Fig. 3. For the childless node B , colleagues are labeled n, coarse neighbors are labeled n + ,
and ﬁne neighbors are labeled n − . The interaction list for B consists of the boxes marked i. The
boxes marked by s are children of B’s colleagues which are separated from B, so they are not ﬁne
neighbors. They constitute the s-list for B (see Deﬁnition 3.1).
746                    FRANK ETHRIDGE AND LESLIE GREENGARD


Thus, D = ∪M
           i=1 Di and we rewrite (2) in the form

                                  M
                                     
                                    1
(7)                      ψ(x) =                    f (y) log(|x − y|) dy.
                                  i=1
                                        2π    Di


     Definition 3.1. The colleagues of a square B are squares at the same reﬁnement
level which share a boundary point with B. (B is considered to be a colleague of itself.)
The coarse neighbors of B are leaf nodes at the level of B’s parent which share a
boundary point with B. The ﬁne neighbors of B are leaf nodes one level ﬁner than B
which share a boundary point with B. Together, the union of the colleagues, coarse
neighbors, and ﬁne neighbors of B will be referred to as B’s neighbors. The s-list of a
box B consists of those children of B’s colleagues which are not ﬁne neighbors of B.
     The interaction region for B consists of the area covered by the neighbors of
B’s parent, excluding the area covered by B’s colleagues and coarse neighbors. The
interaction list for B consists of those squares in the interaction region which are at
the same reﬁnement level, as well as leaf nodes in the interaction region which are at
coarser levels. When the distinction is important, the squares at the same reﬁnement
level will be referred to as the standard interaction list, while the squares at coarser
levels will be referred to as the coarse interaction list.
     In our FMM, following [8, 16, 17], terms in the convolution integral (7) from
neighbor leaf nodes are computed directly. More distant interactions are accounted
for on coarser levels, through the use of a hierarchy of far-ﬁeld and local multipole
expansions. We consider the local interactions ﬁrst.
    3.2. Local interactions. For fourth and sixth order accuracy, we assume that
we are given f on a cell-centered k × k grid for each leaf node B, with k = 4 or 6,
respectively. We can, therefore, take these k 2 data points and construct a kth order
polynomial approximation to f of the form
                                       Nk
                                       
                         fB (x, y) ≈         cB (j) bj (x − xB , y − yB ),
                                       j=1


where Nk = k(k+1)2  is the number of basis functions needed for kth order accuracy and
where (xB , yB ) denotes the center of B. The basis functions b1 (x, y), . . . , bNk (x, y) are
given by

                              {xi y j | i, j ≥ 0, i + j ≤ k − 1}.

If we let fB ∈ Rk denote the given function values (in standard ordering), then the
                   2


calculation of the coeﬃcient vector cB is clearly overdetermined. We obtain it through
a least squares ﬁt based on the singular value decomposition. The pseudoinverse
                    2
matrix P ∈ RNk ×k , such that

                                         cB = P fB ,

can be precomputed and stored.
    Remark 3.1. For eighth order accuracy, we assume that f is given on a scaled
8 × 8 classical tensor product Chebyshev grid [7] and use as basis functions

                           {Ti (x)Tj (y)| i, j ≥ 0, i + j ≤ k − 1},
             A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                                            747

where Ti (x) denotes the Chebyshev polynomial of degree i. The coeﬃcients of the
Chebyshev expansion can be computed eﬃciently using the fast cosine transform.
    Consider now a target point Q, which lies in a neighbor of B. The ﬁeld induced
at Q by fB is approximated by

                                                    Nk
                                                    
(8)                                 ψB (Q) =              cB (n)f (Q, n),
                                                    n=1


where
                                
                          1
(9)           f (Q, n) =                bn (x − xB , y − yB ) log |Q − (x, y)| dxdy.
                         2π         B

Since the target points Q are regularly spaced in each neighboring square, we can
precompute the weights (9) for each of the k 2 possible locations at each of 9 possible
colleagues, 12 possible ﬁne neighbors, and 12 possible coarse neighbors. To be more
precise, we can precompute the weights assuming that B is the unit square [−0.5, 0.5]2
because of the following straightforward lemma.
     Lemma 3.2. Let B be a leaf node at level l and let Q denote a target point in
one of B’s neighbors. Let Q∗ denote the scaled target point for the unit cell centered
at the origin

                                    Q∗ = 2l−1 · (Q − (xB , yB )),

let
                                     1/2  1/2
                                1
(10)          f ∗ (Q∗ , n) =                              bn (x, y) log |Q∗ − (x, y)| dxdy,
                               2π       −1/2       −1/2


and let
                                     d+2  1/2  1/2                                      
                       1        1                                                      1
(11)       f¯(n, l) =                                             bn (x, y) log                  dxdy.
                      2π       2l−1                −1/2    −1/2                       2l−1

Then the integral f (Q, n) deﬁned in (9) is given by
                                                   d+2
                                               1
                       f (Q, n) =                           f ∗ (Q∗ , n) + f¯(n, l),
                                             2l−1

where d is the degree of the polynomial basis function bn .
    Thus, we need only obtain weights for a box of unit area. Elementary counting
arguments show that the storage required for this precomputation is

                   k × k · Nk · 9 real numbers for colleagues,
                  k × k · Nk · 12 real numbers for ﬁne neighbors,
                  k × k · Nk · 12 real numbers for coarse neighbors,

for a total of approximately 17 × k 4 real numbers.
748                 FRANK ETHRIDGE AND LESLIE GREENGARD


    3.3. Far-ﬁeld interactions. We turn now to the calculation of far-ﬁeld inter-
actions, which are computed by means of multipole expansions. We refer the reader
to [14, 16] for more detailed discussions of potential theory. Our starting point is
the usual multipole expansion for a charge distribution, which we state formally as a
theorem.
    Theorem 3.3 (multipole expansion). Let ρ(y) be a charge distribution contained
within a square Di with center C and let Φ(x) denote the induced ﬁeld at a point x
in the interaction list of Di :
                                     
                                   1
                           Φ(x) =        log |x − y|ρ(y) dy.
                                  2π Di

Then Φ(x) can be described by the multipole expansion
                                              ∞                        
                                                            αk
(12)             Φ(x) = α0 log |x − C| +                                   ,
                                                      (x1 + ix2 − C)k
                                                k=1

where C is viewed as a point in the complex plane, x = (x1 , x2 ), and (w) denotes
the real part of the complex quantity w. The coeﬃcients αk are given by
                              
                           1
                     α0 =         ρ(y1 , y2 )dy1 dy2 ,
                          2π Di
                                
                             1      (y1 + iy2 − C)k ρ(y1 , y2 )
(13)                αk = −                                      dy1 dy2 .
                            2π Di                 k

In the hierarchical framework of the FMM, an upper bound for the error in truncating
the expansion after n terms is given by
                            n    
                            1    1
(14)                                  |ρ(y1 , y2 )| dy1 dy2 .
                            2   2π Di

    Theorem 3.4 (local expansion). Let ρ(y) be a charge distribution contained
outside the neighbors of a square Di with center C and let Ψ(x) denote the induced
ﬁeld at x ∈ Di . Then Ψ(x) can be described by a local expansion
                                    ∞                          
                                     
(15)                     Ψ(x) =           βl (x1 + ix2 − C)l       ,
                                     l=0

where C is viewed as a point in the complex plane and x = (x1 , x2 ).
     The FMM relies on the ability to manipulate multipole and local expansions for
every box in the tree hierarchy. We omit the technical details and refer the reader to
the original papers [8, 14, 16, 17].
     Definition 3.5. We denote by Sl,k the kth square at reﬁnement level l.
     We denote by Φl,k the multipole expansion describing the far ﬁeld due to the source
distribution supported inside Sl,k .
     We denote by Ψl,k the local expansion describing the ﬁeld due to the source dis-
tribution outside the neighbors of Sl,k .
     We denote by Ψ̃l,k the local expansion describing the ﬁeld due to the source dis-
tribution outside the neighbors of the parent of Sl,k .
             A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                        749

    Remark 3.2. Let Sl,k be a square in the quad-tree hierarchy and let Sl ,k be a
square in its interaction list. Then there is a linear operator TM M for which

(16)                  Φl,k = TM M [Φ(C1 ), Φ(C2 ), Φ(C3 ), Φ(C4 )],

where Φ(Cj ) denotes the multipole expansion for the jth child of Sl,k . In other words,
we can merge the expansions for four children into a single expansion for the parent.
Similarly, there is a linear operator TLL for which

(17)                  [Ψ̃(C1 ), Ψ̃(C2 ), Ψ̃(C3 ), Ψ̃(C4 )] = TLL Ψl,k ,

where Cj denotes the jth child of Sl,k . In other words, we can shift the local expansion
Ψ for a box to the corresponding expansion Ψ̃ for each of its children. Finally, there
is a linear operator TM L for which the ﬁeld in Sl,k due to the source distribution in
Sl ,k is described by Ψ = TM L Φl ,k . It is easy to verify that
                                                  
(18)                          Ψl,k = Ψ̃l,k +           T M L Φi ,
                                               i∈IL

where IL denotes the interaction list for square Sl,k .
     Remark 3.3. One slight complication in the adaptive algorithm concerns the
interaction between boxes of diﬀerent sizes. Referring to Figure 3, we need to account
for the inﬂuence of a childless square B on each box marked s and vice versa. (This
interaction doesn’t arise if B undergoes further reﬁnement.) For the box marked s,
its multipole expansion is rapidly convergent at each of the k 2 target points in B.
Thus, its inﬂuence can be computed by direct evaluation of the truncated series. For
the reverse, however, note that B’s multipole expansion is not so rapidly convergent.
In this case, we can map directly from the polynomial coeﬃcients cB of B to the local
expansion in s. A more precise statement than (18) is
                                                   
(19)                Ψl,k = Ψ̃l,k +     T M L Φi , +     Ldirect (ci ),
                                   i∈SIL              i∈CIL

where SIL denotes the standard interaction list and CIL denotes the coarse in-
teraction list. The operator Ldirect , which maps the coeﬃcients of the polynomial
approximation of the density in the coarse box onto the p coeﬃcients of the local
expansion can be precomputed and stored.
    The bulk of the work in the FMM consists of applying the operators TM M , TLL ,
and especially TM L in a systematic fashion. Unfortunately, these operators are dense.
Using multipole and local expansions truncated after p terms, the naive cost of appli-
cation is proportional to p2 . Recent improvements in the FMM have reduced this cost
in both two and three space dimensions [17, 19]. A brief discussion of the technical
ideas is presented in section 3.8.

       3.4. The FMM algorithm.
                                   Initialization
Comment [We assume we are given a square domain D = S0,0 , on which is superim-
posed an adaptive hierarchical quad-tree structure. We let M be the number of leaf
nodes and denote them by Di , i = 1, . . . , M . The number of grid points is, therefore,
N = 16M . We let p denote the order of the multipole expansion (p ≈ log2 ), where )
is the desired accuracy). We let lmax denote the maximum reﬁnement level.]
750                  FRANK ETHRIDGE AND LESLIE GREENGARD


                              Step I: Multipole sweep
                                    Upward pass
      for l = lmax , . . . , 0
           for all boxes j on level l
               if j is childless then
                     form the multipole expansion Φl,j from (12)
               else
                     form the multipole expansion Φl,j by merging the expansions of
                     its children using the operator TM M (see (16))
           end
      end

                                         Downward pass
     Initialize the local expansion Ψ0,0 = 0.
     for l = 1, . . . , lmax
          for all squares j on level l
              Compute Ψ̃l,j by shifting its parent’s Ψ expansion using the operator TLL
              Compute Ψl,j by adding in the contributions from all squares in j’s
                  interaction list according to (19).
              if j is childless then
                       for all boxes k in the s-list of j:
                            evaluate the multipole expansion Φk at each
                            target in square j.
                       end
                       Evaluate the local expansion Ψl,j at each
                       target in square j.
              endif
          end
     end
Cost [The upward pass requires approximately M p2 work, where M is the number of
leaf nodes. The downward pass requires approximately 3M p2 work using plane-wave
expansions (see section 3.8 below).]

                            Step II: Local interactions
Comment [At this point, for each leaf node Di , we have computed the inﬂuence of
the source distribution f over all leaf nodes Dj outside the neighbors of Di .]
     do i = 1, . . . , M
         For each target point in Di , evaluate the inﬂuence of each
              neighbor according to (8) using the precomputed
              tables of coeﬃcients (10).
     end
Cost [The maximum number of neighbors a square can have is thirteen (twelve ﬁne
neighbors and itself). Thus the local work is bounded by is 13 · k(k+1)
                                                                    2   · N operations.]

     3.5. Periodic boundary conditions. The inversion formula (2) and the fast
algorithm described above assume that the right-hand side f is supported within a
unit square. When imposing periodic boundary conditions, as mentioned in section 2,
one can simply assume that the entire plane is tiled with copies of f centered at the
lattice points {(i, j)|i, j ∈ Z}. In order to account for the inﬂuence of these images, we
follow the approach introduced in [16], the essence of which can already be found in
              A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                            751

Lord Rayleigh’s classic paper [25]. The main thing to notice is that, after the upward
pass in the FMM, we have a net multipole expansion describing the far ﬁeld due to
the entire source distribution f contained in the unit cell centered at the origin:
                                           p      
                                             αn
(20)                             φ(x) =             .
                                            n=1
                                                zn

(There is no logarithmic term since we assume that the source distribution has no net
charge.) This is then the expansion for each of the periodic images of the box with
respect to its own center. All of these images, except for the nearest neighbors centered
at {(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)}, are well separated from the
computational domain itself. Thus, the ﬁelds they induce inside the computational
domain are accurately representable by a p-term local expansion where, as before, p is
the number of terms needed to achieve a relative precision ). This local representation
can be written as
                                                  p          
                                                   
                                                            n
(21)                              Ψ0,0 (w) =          βn w     .
                                                n=0

    It remains only to obtain the operator mapping the coeﬃcients {αn } to the coef-
ﬁcients {βn }. We refer the reader to [4, 16, 25] for a discussion of this operator, which
is based on the precomputation of certain lattice sums. The reason we denote the
local expansion in (21) by Ψ0,0 is for consistency of notation with the FMM described
above; the downward pass is modiﬁed in the initialization step. In the remainder of
the downward pass and in Step II, only two changes are required; the interaction list
and the local computations must be adjusted for boxes near the boundary to account
for periodic images. This involves no signiﬁcant increase in the amount of work.
     3.6. Other homogeneous boundary conditions. As noted in section 2, prob-
lems with homogeneous Dirichlet and Neumann conditions can be solved using the
method of images. Since there is a 2 × 2 “supercell” which tiles the plane periodi-
cally, it is straightforward to embed such problems in a periodic version of the FMM.
Done naively, this would entail a fourfold increase in CPU time and storage. Careful
implementation considerations allow one to recover this overhead, but the details are
tedious and will be omitted.
     3.7. Inhomogeneous boundary conditions. In order to impose inhomoge-
neous boundary conditions using potential theory, we need to consider arrangements
of single and double layer potentials such as the one depicted in Figure 2. These can
be viewed as singular charge distributions and can be handled by the same FMM as
above, with three modiﬁcations. First, the far ﬁeld due to a box B with a single layer
density σ and a double layer density µ along its boundary Γ is given by
                                                 ∞
                                                                     
                                                           αk
(22)          φ(x) =  α0 log |x1 + ix2 − C| +                         ,
                                                     (x1 + ix2 − C)k
                                                       k=1

where
                                               
                                           1
(23)                               α0 = −            σ(s)ds
                                          2π     Γ
and
                   
               1     (y1 (s) + iy2 (s) − C)k σ(s)
(24) αk = −                                       + (y1 (s) + iy2 (s) − C)k−1 µ(s) ds.
              2π   Γ               k
752                   FRANK ETHRIDGE AND LESLIE GREENGARD


Here, (y1 (s), y2 (s)) is an arclength parametrization of Γ. Second, contributions to the
local ﬁeld from a leaf node containing layer potentials are precomputed as in section
3.2. Finally, the interaction list and the local computations must be adjusted for
boxes near the boundary.
     3.8. Fast translation operators. Consider a box B centered at XB , containing
sources {z1 , . . . , zM } with source strengths {q1 , . . . , qM } and a target box D centered
at XD in its interaction list. We assume for the moment that (XD ) > (XB ). In
the original FMM, the ﬁeld outside B is represented as
                                                          p
                                                                                  
                                                                      αk
(25)          φ(x) =  α0 log(x1 + ix2 − XB ) +                                     .
                                                                (x1 + ix2 − XB )k
                                                           k=1

The ﬁeld inside D is represented as
                                  p                       
                                    
                                                         l
(26)                    φ(x) =       βl (x1 + ix2 − XD )
                                        l=0

with
                              ∞
                                       αk
β0 = α0 log(XD − XB ) +                         (−1)k ,
                                    (XD − XB )k
                              k=1
                                     ∞
                                                        
              α0             1             αk        l+k−1
βl = −                 +                                    (−1)k for l ≥ 1.
       l · (XD − XB )l   (XD − XB )l   (XD − XB )k    k−1
                                              k=1

This describes the translation operator denoted by TM L in section 3.3 and requires
O(p2 ) work to apply. In [19], Hrycak and Rokhlin suggest an alternative representa-
tion of φ, based on the formula
                                        ∞
                                1
(27)                                =      e−λ(z−w) dλ.
                              z−w       0

This integral can be discretized using generalized Gaussian quadratures [31] which
take into account the nature of the integrand as well as the precise geometry of the
interaction list. The number of quadrature nodes needed to achieve a precision ) is
less than or equal to the number of multipole coeﬃcients. Tables of weights and nodes
for various values of ) are provided in [31]. For numerical purposes, we begin with an
approximation of the form
                                             p
                                   1
                                       ≈   wk e−λk (zi −w) .
                                zi − w
                                           k=1

Integrating both sides, we have
                                         p
                                          −wk
                         log(zi − w) ≈                   e−λk (zi −w) + C,
                                                  λk
                                         k=1

where C is a constant of integration. Choosing
                                              p
                                               wk
                                      C=                 e−λk
                                                    λk
                                              k=1
             A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                       753

enforces the condition that log(1) = 0.
     Instead of the classical multipole expansion (25), we instead work with the expo-
nential representation
                                 p                             
                                   
                                           −λk (x1 +ix2 −XB )
(28)                   φ(x) =         ak e                   +C ,
                                 k=1

where the coeﬃcients ak are exponential moments of the charge distribution:
                                      M
                                      
                               ak =          qj e+λk (zj −XB )
                                       j=1


and
                                           
                                      M
                                  C =   qj  · C.
                                             j=1


The advantage of this approach is that translation has been diagonalized. Transmit-
ting the expansion from box B to D is carried out by computing
                               p                            
                                
                                        −λk (x1 +ix2 −XD )
(29)                 ψ(x) =        bk e                   +C ,
                                  k=1

where the new coeﬃcients bk are obtained from the ak through the translation formula

                                bk = ak e−λk (XD −XB ) .

  The details of how to incorporate such expansions into an adaptive two-dimensional
FMM code can be found in [19]. For the three-dimensional analogue, see [17].
     4. Numerical results. Fast Poisson solvers using the algorithms described
above have been implemented in Fortran 77. Here, we demonstrate their perfor-
mance on four problems involving varying degrees of adaptivity. All of the timings
listed below correspond to calculations performed on a 440MHz SUN Ultra-10 with
256 MB RAM using the compiler option (-fast).
     There are few eﬃcient adaptive solvers which are widely available. Therefore,
we have chosen a simple and stringent standard for comparison: the time taken by
a classical FFT-based code for the same number of degrees of freedom (grid points).
Using the second order accurate FORTRAN code HWSCRT by Swartztrauber [27]
and Swartztrauber and Sweet [28] (available from www.netlib.org), with the same
machine and compiler option as above, we obtain the data shown in Table 1.
     We have, as yet, said little about our adaptive reﬁnement strategy. It is straight-
forward. Let B be a leaf node with k × k grid points, as discussed in section 3.2 and
let fB (x) denote the kth order polynomial used to approximate the right-hand side on
B. We then evaluate fB (x, y) on a 2k × 2k grid covering B and compute the discrete
L2 error E2 = f (x, y) − fB (x, y)2 over these target points. If E2 > tol, the leaf
node B is subdivided. Of course, the tree obtained by this procedure may not satisfy
the level restriction that neighboring leaf nodes be at most one level apart. It is a
straightforward matter to “ﬁx” the tree in a subsequent sweep. We omit the details.
  754                                FRANK ETHRIDGE AND LESLIE GREENGARD


                                                Table 1
       Timing results for the FFT-based second order accurate code HWSCRT. N denotes the number
  of grid points, Thwscrt denotes the required solution time in seconds, and rate denote the number
  of grid points “processed” per second (N/Thwscrt ).

                                                 N                       Thwscrt      Rate
                                                 256 × 256                  0.17   3.8 105
                                                 512 × 512                  0.78   3.4 105
                                                 1024 × 1024                 4.0   2.6 105
                                                 2048 × 2048                19.4   2.2 105




 0.5


 0.4
                                                                          1.2

 0.3
                                                                            1

 0.2                                                                      0.8


 0.1                                                                      0.6

                                                                          0.4
  0
                                                                          0.2
−0.1
                                                                            0

−0.2
                                                                          -0.2
                                                                          0.5
−0.3
                                                                                                               0.5

−0.4                                                                                0
                                                                                                           0

−0.5
  −0.5   −0.4   −0.3   −0.2   −0.1   0   0.1   0.2    0.3    0.4   0.5                       -0.5   -0.5


      Fig. 4. The left-hand ﬁgure shows an adaptive mesh resolving the source distribution in (30).
  The right-hand ﬁgure shows a surface plot of the solution.



          Example 4.1. In our ﬁrst experiment, we consider the equation

                                                     3
                                                                                                      2
  (30)                               ∆ψ(x) =                (4α2 x − xi 2 − 4α)e−α x−xi
                                                     i=1


  in free space, for which the exact solution (Figure 4) is the sum of three Gaussians

                                                                   3
                                                                                       2
  (31)                                                ψ(x) =              e−α x−xi .
                                                                   i=1


  We consider the case where α = 250, x1 = (.1, .1), x2 = (0, 0), and x3 = (−.15, .1).
  The right-hand side in (30) is supported, with an exponentially small error, in the
  box [−0.5, 0.5]2 , which we use as the computational domain. Our adaptive mesh
  is depicted in Figure 4. Note that ﬁne grids are created only near the centers of
  the Gaussians. The performance of the fourth, sixth, and eighth order codes are
  summarized in Table 2.
                  A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                             755
                                               Table 2
     Timing results for the fourth, sixth, and eighth order accurate codes in Example 4.1. F M M
denotes the requested precision from far-ﬁeld interactions within the FMM, RHS denotes the re-
quested precision in discretizing the right-hand side, and Nlev denotes the number of levels used in
the FMM hierarchy. E2 and E∞ denote the relative L2 and L∞ errors of the computed solution, N
denotes the number of grid points used, TF M M denotes the required solution time in seconds, and
rate denote the number of grid points “processed” per second (N/TF M M ).

          F M M    RHS    Nlev    E2            E∞                N    TF M M       Rate
                                            Fourth order
          10−3      10−3    7       3.7 10−4      1.2 10−4      11488       0.08   1.4 105
          10−3      10−6    9       7.0 10−5      1.4 10−4      96592       0.64   1.5 105
          10−6      10−6    9       4.9 10 −6     1.3 10−6      96592       1.08   8.9 104
          10−6      10−9    10      8.4 10 −8     4.9 10−7     821824       8.38   9.8 104
          10−9      10−9    10      1.4 10 −8     3.4 10−9     821824      12.17   6.8 104
                                             Sixth order
          10−3      10−3    6       8.2 10−5      1.2 10−4      10296       0.08   1.3 105
          10−3      10−6    7       7.0 10−5      1.6 10−4      43236       0.29   1.5 105
          10−6      10−6    7       1.5 10−7      4.2 10−7      43236       0.39   1.1 105
          10−6      10−9    9       8.6 10−8      5.6 10−7     279432       2.45   1.1 105
          10−9      10−9    9       2.4 10 −9     2.2 10−9     279432       3.48   8.0 104
          10−9      10−12   10      2.3 10 −10    2.4 10−9    1725984      17.19   1.0 105
          10−12     10−12   10      2.0 10 −12    8.4 10−13   1725984      27.28   6.3 104
                                            Eighth order
          10−3      10−3    6       1.0 10−4      2.0 10−4      13888       0.16   8.7 104
          10−3      10−6    7       9.0 10−5      2.0 10−4      63616       0.68   9.4 104
          10−6      10−6    7       1.7 10−7      6.8 10−7      63616       0.80   8.0 104
          10−6      10−9    8       1.4 10 −7     6.8 10−7     273280       3.11   8.8 104
          10−9      10−9    8       4.4 10 −10    2.7 10−9     273280       3.62   7.5 104
          10−9      10−12   9       4.2 10 −10    2.8 10−9    1281472      16.02   8.4 104
          10−12     10−12   9       9.2 10 −13    6.1 10−13   1281472      21.68   5.9 104



       Example 4.2. For our second experiment, we consider the singular equation

                                         ∆ψ = 0    in D,
                                          ψ=0      on ΓL ,
(32)                                      ψ=0      on ΓR ,
                                          ψ=1      on ΓT ,
                                          ψ=0      on ΓB ,

    In Figure 5, we plot the solution obtained with our solver on an adaptive grid,
the solution obtained by HWSCRT on a uniform 64 × 64 mesh, and the error in the
HWSCRT solution. Note that we resolve the corner singularities adaptively and that
our solution is exact (up to the requested FMM tolerance), since the data is piecewise
polynomial (here, constant).
    Remark 4.1. There is an enormous diﬀerence in the meaning of “order of ac-
curacy” in our solver and in standard ﬁnite diﬀerence or ﬁnite element codes. Our
solver is exact for a certain order of approximation of the data. A kth order accurate
PDE-based solver on an N × N mesh has a global error which decays like (1/N )k with
a constant of proportionality which depends on the kth derivative of the solution. In
the present example, our solver is exact. The ﬁnite diﬀerence code is only ﬁrst order
756                         FRANK ETHRIDGE AND LESLIE GREENGARD




       1                                             1


    0.8                                             0.8


    0.6                                             0.6


    0.4                                             0.4


    0.2                                             0.2


      0                                               0
    0.5                                             0.5

                                             0.5                                                                           0.5

             0                                                      0
                                   0                                                                      0


                    -0.5    -0.5                                                   -0.5     -0.5

                                                     0.5


                                                     0.4


                                                     0.3


                                                     0.2

    0.15
                                                     0.1

      0.1
                                                      0
    0.05

                                                    -0.1
       0

                                                    -0.2
   –0.05


    –0.1                                            -0.3
     0.5

                                              0.5
                                                    -0.4
             0
                                       0
                                                    -0.5
                     –0.5   –0.5                      -0.5   -0.4   -0.3    -0.2     -0.1      0   0.1   0.2   0.3   0.4   0.5




    800                                             2500

    700
                                                    2000
    600

    500
                                                    1500
    400

    300                                             1000

    200
                                                     500
    100

        0                                              0
      0.5                                            0.5

                                             0.5                                                                           0.5

             0                                                          0
                                   0                                                                       0


                    -0.5    -0.5                                                    -0.5    -0.5


     Fig. 5. The upper left-hand ﬁgure shows the solution obtained by HWSCRT to Example 4.2 and
the upper right-hand ﬁgure shows the solution obtained using our solver. The middle ﬁgures show
the error in the solution obtained by HWSCRT and the adaptive grid use by our solver, respectively.
The lower ﬁgures show the electrostatic energy ∇ψ2 obtained from HWSCRT and our solver,
respectively.
                 A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                              757




                                                      10
  50
                                                       9
   0
                                                       8
  -50
                                                       7
 -100
                                                       6
 -150
                                                       5
 -200
 -250                                                  4

 -300                                                  3

 -350                                                   2
  0.5                                                 0.5

                                               0.5                                              0.5

            0                                                0
                                   0                                                 0


                    -0.5   -0.5                                        -0.5   -0.5




                                                      12
  500

                                                      10
        0


  -500                                                 8

 -1000
                                                       6

 -1500
                                                       4
 -2000

 -2500                                                  2
   0.5                                                0.5

                                               0.5                                              0.5

             0                                               0
                                   0                                                 0


                    -0.5   -0.5                                        -0.5   -0.5


     Fig. 6. The left-most ﬁgure shows a surface plot of the right-hand side for 10 randomly placed
Gaussians as described in (33) with α = 100 and the ﬁgure to the right of it shows the corresponding
solution. The two lower ﬁgures show both the right-hand side and corresponding solution for α =
1000.




accurate because of the corner singularities.
    Example 4.3. In order to evaluate the performance of our code with widely
varying degrees of adaptivity, we consider the source distribution
                                            10
                                                                  2
(33)                              ∆ψ(x) =            −2αe−α x−xi
                                            i=1

in free space. With α = 100, the distribution is fairly smooth, while with α = 1000,
the Gaussians fall oﬀ sharply and require many levels of reﬁnement near the centers
(see Figure 6). The experiment was run using the fourth order code and )F M M =
)RHS = 10−6 . Table 3 lists our timing data for various values of α.
     In addition to comparing various levels of adaptivity, it is also worth noting that
758                   FRANK ETHRIDGE AND LESLIE GREENGARD

                                         Table 3
                      Timings for the FMM-based solver in Example 4.3.

                M     N          TF M M          Rate   N         TF M M      Rate
                                 α = 100                         α = 250
                5     43969         0.44    9.9 104     73840        0.76   9.7 104
                10    70864         0.68    1.0 105     138640       1.43   9.7 104
                25    119296        1.33    8.9 104     212800       2.06   1.0 105
                100   233296        2.43    9.6 104     262144       2.60   1.0 105
                                 α = 500                         α = 1000
                5     97648         1.08    9.0 104     108544       1.17   9.3 104
                10    196336        2.09    9.4 104     225616       2.40   9.4 104
                25    377248        4.03    9.4 104     460912       4.96   9.3 104
                100   785632        8.39    9.4 104     916336       9.44   9.7 104



                                           Table 4
     Timings for the FMM-based solver in Example 4.3 using free-space and periodic boundary con-
ditions.

                M     N          TF M M       Rate      N        TF M M       Rate
                                Free space                       Periodic
                10    138640        1.43   9.7 104      139696      1.63    8.6 104
                30    241168        2.38   1.0 105      241552      2.63    9.2 104
                50    253696        2.41   1.0 105      253840      2.62    9.7 104
                100   262144        2.60   1.0 105      262192      2.94    8.9 104



the periodic and free-space solvers execute in nearly the same time. To show this, we
consider a right-hand side given by
                                           M
                                                                  2
(34)                           ∆ψ(x) =           (−1)i 2αe−α x−xi .
                                           i=1

This ensures that the net charge in the periodic cell is zero. Table 4 compares the per-
formance of the fourth order accurate code with either free-space or periodic boundary
conditions with α = 250 and )F M M = )RHS = 10−6 .
    Example 4.4. Most of the preceding examples involve adaptive reﬁnement around
a “point-like” singularity. Here we consider the case of a singularity along a curve.
We simply deﬁne a source distribution which takes the value 1 inside a circle of radius
.25 and 0 outside. The right-hand side is shown in Figure 7 along with the computed
solution. Using the fourth order solver with 7 levels or reﬁnement and 7936 grid
points, the L2 and L∞ errors are less than 10−3 and the solver executes at the rate
1.3 105 points per second. Using the sixth order solver with 12 levels or reﬁnement
and 681,408 grid points, the L2 and L∞ errors are less than 10−6 and the solver
executes at the rate 8.5 104 points per second. Both of these timings are comparable
to those in Example 4.1.
    The following observations can be made from the preceding data.
      1. The timings for the FMM-based solver grow linearly with the number of
         unknowns. For fourth order accuracy with a three-digit FMM tolerance,
         the present implementation achieves a processing speed between 5.9 104 and
         1.5 105 points per second. The classical second order FFT-based solver pro-
         cesses 2.6 105 points per second on a 1024 × 1024 grid.
      2. For three-digit accuracy, the fourth order accurate code is fastest (≈ 1.4 105
         points per second), while for six-digit accuracy, the sixth order accurate code
                       A NEW FMM-BASED POISSON SOLVER IN TWO DIMENSIONS                                                                          759


                                             0.5


                                             0.4
 1
                                                                                                                   −0.01
                                             0.3
0.8
                                                                                                                   −0.02
                                             0.2

0.6
                                                                                                                   −0.03
                                             0.1

0.4
                                              0                                                                    −0.04


0.2                                         −0.1                                                                   −0.05


                                            −0.2
  0                                                                                                                −0.06
0.5                                                                                                                  0.5
                                            −0.3
                                      0.5                                                                                                              0.5

          0                                 −0.4                                                                           0
                             0                                                                                                               0

                                            −0.5
               −0.5   −0.5                    −0.5   −0.4   −0.3   −0.2   −0.1   0   0.1   0.2   0.3   0.4   0.5               −0.5   −0.5




       Fig. 7. The left-hand ﬁgure shows the right-hand side. The middle ﬁgure shows the grid and
  the right ﬁgure shows the solution.



              is fastest (≈ 1.1 105 points per second). For twelve-digit accuracy, the sixth
              and eighth order codes are only about twice as slow (≈ 6.3 104 points per
              second).
      5. Conclusions. We have developed a new adaptive, high order accurate solver
  for the Poisson equation in two dimensions. The method is direct, fast-multipole-
  based, and allows for the speciﬁcation of a variety of boundary conditions on a unit
  square. These include free-space conditions, periodic boundary conditions, Dirichlet,
  Neumann, and a variety of mixed conditions. The amount of work scales linearly with
  the number of degrees of freedom in the computational domain and is competitive
  with classical FFT-based solvers in terms of work per grid point, despite the ﬂexibility
  of adaptive mesh reﬁnement.
      In order to develop a black box Poisson solver of broad interest, of course, we
  need to allow for complex geometry. It would also be of value to be able to solve the
  Helmholtz and linearized Poisson–Boltzmann equations,

                                 ∆u + λ2 u = f                            and              ∆u − λ2 u = f,

  with a similar approach. These extensions are underway and will be reported at a
  later date.

                                                            REFERENCES

      [1] A. S. Almgren, J. B. Bell, P. Colella, and L. H. Howell, An adaptive projection method
              for the incompressible Euler equation, in Proceedings of the Eleventh AIAA Computational
              Fluid Dynamics Conference, 1993, pp. 530–539.
      [2] C. Anderson, Domain decomposition techniques and the solution of Poisson’s equation in
              inﬁnite domains, in Proceedings of the Second International Symposium on Domain De-
              composition Methods, 1988, pp. 129–139.
      [3] M. J. Berger and P. Colella, Local adaptive mesh reﬁnement for shock hydrodynamics, J.
              Comput. Phys., 53 (1989), pp. 484–512.
      [4] C. L. Berman and L. Greengard, A renormalization method for the evaluation of lattice
              sums, J. Math. Phys., 35 (1994), pp. 6036–6048.
      [5] A. Brandt, Multi-level adaptive solutions to boundary value problems, Math. Comp., 31 (1977),
              pp. 330–390.
      [6] B. L. Buzbee, G. H. Golub, and C. W. Nielson, On direct methods for solving Poisson’s
              equations, SIAM J. Numer. Anal., 7 (1970), pp. 627–656.
760                    FRANK ETHRIDGE AND LESLIE GREENGARD


 [7] C. Canuto, M. Y. Hussaini, A. Quarteroni, and T. A. Zang, Spectral Methods in Fluid
          Dynamics, Springer-Verlag, New York, 1988.
 [8] J. Carrier, L. Greengard, and V. Rokhlin, A fast adaptive multipole algorithm for particle
          simulations, SIAM J. Sci. Statist. Comput., 9 (1988), pp. 669–686.
 [9] T. F. Chan, R. Glowinski, J. Periaux, and O. B. Widlund, eds., Domain Decomposition
          Methods, SIAM, Philadelphia, 1989.
[10] T. Chan and B. Smith, Domain decomposition and multigrid algorithms for elliptic problems
          on unstructured meshes, Electron. Trans. Numer. Anal., 2 (1994), pp. 171–182.
[11] G. Chesshire and W. D. Henshaw, Composite overlapping meshes for the solution of partial
          diﬀerential equations, J. Comput. Phys., 90 (1991), pp. 1–64.
[12] Z. Gimbutas, L. Greengard, and M. Minion, Coulomb interactions on planar structures:
          Inverting the square root of the Laplacian, SIAM J. Sci. Comput., 22 (2001), pp. 2093–
          2108.
[13] D. Gottlieb and S. A. Orszag, Numerical Analysis of Spectral Methods: Theory and Appli-
          cations, SIAM, Philadelphia, 1977.
[14] L. Greengard, The Rapid Evaluation of Potential Fields in Particle Systems, MIT Press,
          Cambridge, MA, 1988.
[15] L. Greengard and J. Y. Lee, A direct adaptive Poisson solver of arbitrary order accuracy,
          J. Comput. Phys., 125 (1996), pp. 415–424.
[16] L. Greengard and V. Rokhlin, A fast algorithm for particle simulations, J. Comput. Phys.,
          73 (1987), pp. 325–348.
[17] L. Greengard and V. Rokhlin, A new version of the fast multipole method for the Laplace
          equation in three dimensions, Acta Numer., 6 (1997), pp. 229–269.
[18] R. B. Guenther and J. W. Lee, Partial Diﬀerential Equations of Mathematical Physics and
          Integral Equations, Prentice-Hall, Englewood Cliﬀs, NJ, 1988.
[19] T. Hrycak and V. Rokhlin, An improved fast multipole algorithm for potential ﬁelds, SIAM
          J. Sci. Comput., 19 (1998), pp. 1804–1826.
[20] H. Johansen and P. Colella, A Cartesian grid embedded boundary method for Poisson’s
          equation on irregular domains, J. Comput. Phys., 147, (1998), pp. 60–85.
[21] S. McCormick, ed., Multigrid Methods, SIAM, Philadelphia, 1987.
[22] A. McKenney, L. Greengard, and A. Mayo, A fast Poisson solver for complex geometries,
          J. Comput. Phys., 118 (1995), pp. 348–355.
[23] M. L. Minion, A projection method for locally reﬁned grids, J. Comput. Phys., 127 (1996), pp.
          158–177.
[24] A. T. Patera, A spectral element method for ﬂuid dynamics: Laminar ﬂow in a ﬂuid expan-
          sion, J. Comput. Phys., 54 (1984), pp. 468–488.
[25] Lord Rayleigh, On the inﬂuence of obstacles arranged in a rectangular order upon the prop-
          erties of the medium, Philos. Mag., 34 (1892), p. 481.
[26] V. Rokhlin, Rapid solution of integral equations of classical potential theory, J. Comput. Phys.,
          60 (1985), pp. 187–207.
[27] P. N. Swarztrauber, The methods of cyclic reduction, Fourier analysis and the FACR algo-
          rithm for the discrete solution of Poisson’s equation on a rectangle, J. Comput. Phys., 15
          (1974), pp. 46–54.
[28] P. Swarztrauber and R. Sweet, Eﬃcient Fortran Subprograms for the Solution of Elliptic
          Partial Diﬀerential Equations, NCAR Technical Note NCAR-TN/IA-109, 1975, pp. 135–
          137.
[29] G. Russo and J. Strain, Fast triangulated vortex methods for the 2D Euler equations, J.
          Comput. Phys., 111 (1994), pp. 291–323.
[30] I. Stakgold, Boundary Value Problems of Mathematical Physics, Macmillan, New York, 1968.
[31] N. Yarvin and V. Rokhlin, Generalized Gaussian quadratures and singular value decomposi-
          tions of integral operators, SIAM J. Sci. Comput., 20 (1999), pp. 699–718.
