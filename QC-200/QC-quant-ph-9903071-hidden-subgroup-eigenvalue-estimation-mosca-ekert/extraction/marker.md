# The Hidden Subgroup Problem and Eigenvalue Estimation on a Quantum Computer

**Authors:** Michele Mosca, Artur Ekert
**arXiv:** quant-ph/9903071 (v1, 20 Mar 1999)

> NOTE: Marker/Nougat binaries not installed on this host; this file is a pdftotext-based markdown fallback for the required extraction artifact. Layout preserved via `pdftotext -layout`.

---

                                           The Hidden Subgroup Problem and Eigenvalue
                                               Estimation on a Quantum Computer




arXiv:quant-ph/9903071v1 20 Mar 1999
                                                            Michele Mosca∗               Artur Ekert†
                                                                            May 1998


                                                                             Abstract
                                                 A quantum computer can efficiently find the order of an element in
                                             a group, factors of composite integers, discrete logarithms, stabilisers in
                                             Abelian groups, and hidden or unknown subgroups of Abelian groups. It
                                             is already known how to phrase the first four problems as the estimation
                                             of eigenvalues of certain unitary operators. Here we show how the so-
                                             lution to the more general Abelian hidden subgroup problem can also be
                                             described and analysed as such. We then point out how certain instances
                                             of these problems can be solved with only one control qubit, or flying
                                             qubits, instead of entire registers of control qubits.


                                       1     Introduction
                                       Shor’s approach to factoring [Sh], (by finding the order of elements in the multi-
                                       plicative group of integers mod N , referred to as Z∗N ) is to extract the period in
                                       a superposition by applying a Fourier transform. Another approach, based on
                                       Kitaev’s technique [Ki], is to estimate an eigenvalue of a certain unitary opera-
                                       tor. The difference between the two analyses is that the first one considers (or
                                       even ’measures’ or ’observes’) the target or output register in the standard com-
                                       putational basis, while the analysis we detail here considers the target register
                                       in a basis containing eigenvectors of unitary operators related to the function
                                       f . The actual network of quantum gates, as highlighted in [CEMM], is the
                                       same for both algorithms; it is helpful to understand both approaches. In some
                                       cases, which we discuss in Sect. 5, this approach suggests implementations
                                       which do not require a register of control qubits. A more general formulation
                                       of the order-finding problem as well as the discrete logarithm problem, and the
                                       Abelian stabiliser problem, is the hidden subgroup problem (or the unknown sub-
                                       group problem [Hø]). In the case that G is presented as the product of a finite
                                       number of cyclic groups (so G is finitely generated and Abelian), all of these
                                          ∗ Clarendon Laboratory, Parks Road, Oxford, OX1 3PU, U.K. and Mathematical Institute,

                                       24-29 St. Giles’, Oxford, OX1 3LB, U.K.
                                          † Clarendon Laboratory, Parks Road, Oxford, OX1 3PU, U.K.




                                                                                  1
Figure 1: The function f can be viewed as the composition of a homomorphism
g to a group H, and some 1-to-1 mapping h to the set X. Our hidden subgroup
K will be the kernel of g, and H is isomorphic to G/K.


problems are solved by the familiar sequence of a Fourier transform, a function
application, and an inverse Fourier transform. In this paper we describe how
this more general problem can also be viewed and analysed as an estimation of
eigenvalues of unitary operators.


2    The Hidden Subgroup Problem
Let f be a function from a finitely generated group G to a finite set X such
that f is constant on the cosets of a subgroup K (of finite index, since X is
finite), and distinct on each coset. The hidden subgroup problem is to find
K (that is, a generating set for K), given a way of computing f . When K is
normal in G, we could in fact decompose f as h ◦ g, where g is a homomorphism
from G to some finite group H, and h is some 1-to-1 mapping from H to the
set X. In this case, K corresponds to the kernel of g and H is isomorphic to
G/K. We will occasionally refer to this decomposition, which we illustrate in
Fig. 1. Define the input size, n, to be of order log2 [G : K]. We will count
the number of operations, or the running time, in terms of n. An algorithm
is considered efficient if its running time is polynomial in the input size. By
elementary quantum operations, we are referring to a finite set of quantum logic
gates which allow us to approximate any unitary operation. See [BBCDMSSSW]
for a discussion and further references. Our running times will always refer to
expected running times, unless explicitly stated otherwise. By expected running


                                       2
time we are referring to the expected number of operations for any input (and
not just an average of the expected running times over all inputs).
     We should be clear about what it means to have a finitely generated group
G, and to be able to compute the function f . This is difficult without losing
some generality or being dry and technical, or both. The algorithms we de-
scribe only apply for groups G which are represented as finite tuples of integers
corresponding to the direct product of cyclic groups (consequently, G is finitely
generated and Abelian). Conversely, for any finitely generated Abelian G, there
is a temptation to point out that G is isomorphic to such a direct product of
cyclic groups, and assume that we can easily access this product structure. This
is not always the case, even in cases of practical interest. For example, Z∗N , the
multiplicative group of integers modulo N for some large integer N , which is
Abelian of order φ(N ) (the Euler φ-function) and thus isomorphic to a product
of cyclic groups of prime power order. We will not necessarily know φ(N ) or
have a factorisation of it along with a set of generators for Z∗N . However, in
light of the quantum algorithms described in this paper, we could efficiently
find such an isomorphism, thereby increasing the number of finitely generated
Abelian groups which can be efficiently expressed in a manner which allows us
to employ these algorithms. We will however leave further discussion of these
details to another note [EM]. When we talk about computing f , we assume
that we have some unitary operation Uf which takes us from state | xi | 0i to
| xi | f (x)i. It could, for example, take | xi | yi to | xi | y + f (x)i, where + de-
notes an appropriate group operation, such as addition modulo N when the
second register is used to represent the integers modulo N .
     Various cases of the hidden subgroup problem are described in [Si], [Sh],
[Ki], [BL], [Gr], [Jo], [CEMM], and [Hø]. We note that [BL] also covers the
case that f is not necessarily distinct on each coset (that is, h is not 1-to-1),
and this is discussed in the appendix. Finding the order r of an element in a
group H of unknown size, or the period r of a function f , is a special case where
G = Z and K = rZ. For any generator ej of a finitely generated G, we can
use the algorithm in Sect. 4.2 to find an integer k such that f (kej ) = f (0),
so that kej ∈ K. We find this k with O(n) applications of f and O(n2 ) other
elementary quantum operations. We can then assume that ej is of order k (that
is, factor hkej i out of G), and in general assume that G is a finite group.
     We give a few examples.
     Deutsch’s Problem: Consider a function f mapping Z2 = {0, 1} to {0, 1}.
Then f (x) = f (y) if and only if x − y ∈ K, where where K is either {0} or
Z2 = {0, 1}. If K is {0}, then f is 1 − to − 1 (or balanced ), and if K is Z2 then
f is constant. [De] [CEMM]

   Simon’s Problem: Consider a function f from Z2 l to some set X with
the property that f (x) = f (y) if and only if x − y ∈ {0, s} for some string s of
length l. Here K = {0, s} is the hidden subgroup of Z2 l . Simon [Si] presents
an efficient algorithm for solving this problem, and the solution to the hidden
subgroup problem in the Abelian case is a generalisation.



                                          3
    Discrete Logarithms: Let G be the group Zr ×Zr where Zr is the additive
group of integers modulo r. Let the set X be the subgroup generated by some
element a of a group H, with ar = 1. For example, H = F∗q , the multiplicative
group of the field of order q, where r = q − 1. Let a, b ∈ G, and suppose
b = am . Define f to map (x, y) to ax by . Here the hidden subgroup of G
is K = {(k, −km)|k = 0, 1, . . . , r − 1} = h(1, −m)i, the subgroup generated
by (1, −m). Finding this hidden subgroup will give us the logarithm of b to
the base a. The security of the U.S. Digital Signature Algorithm is based on
the computational difficulty of this problem in F∗q (see [MOV] for details and
references). Here the input size is n = ⌈log2 r⌉. Shor’s algorithm [Sh] was the
first to solve this problem efficiently. In this case, f is also a homomorphism
which can make implementations more simple as described in Sect. 5.

     Self-Shift-Equivalent Polynomials: Given a polynomial P in l variables
X1 , X2 , . . . , Xl over Fq , the function f which maps (a1 , a2 , . . . , al ) ∈ Flq to
P (X1 − a1 , X2 − a2 , . . . , Xl − al ) is constant on cosets of a subgroup K of
Flq . This subgroup K is the set of self-shift-equivalences of the polynomial P .
Grigoriev [Gr] shows how to compute this subgroup. He also shows, in the case
that q has characteristic 2, how to decide if two polynomials P1 and P2 are
shift-equivalent, and to generate the set of elements (a1 , a2 , . . . , al ) such that
P1 (X1 − a1 , X2 − a2 , . . . , Xl − al ) = P2 (X1 , X2 , . . . , Xl ). The input size n is at
most l log2 q.

    Abelian Stabiliser Problem: Let G be any group acting on a finite set
X. That is, each element of G acts as a map from X to X, in such a way that
for any two elements a, b ∈ G, a(b(x)) = (ab)(x) for all x ∈ X. For a particular
element x of X, the set of elements which fix x (that is, the elements a ∈ G
such that a(x) = x), form a subgroup. This subgroup is called the stabiliser of
x in G, denoted StG (x). Let fx denote the function from G to X which maps
g ∈ G to g(x). The hidden subgroup corresponding to fx is K = StG (x). The
finitely generated Abelian case of this problem was solved by Kitaev [Ki], and
includes finding orders and discrete logarithms as special cases.


3     Phase Estimation and the Quantum Fourier
      Transform
In this section, we review the relationship between phase estimation and the
quantum Fourier transform which was highlighted in [CEMM].
   The quantum Fourier transform for the cyclic group of order N , FN , maps
                                           N −1
                                     1 X 2πiax/N
                             | ai → √       e    | xi .
                                      N x=0




                                              4
So FN−1 maps
                               N −1
                           1 X 2πiax/N
                          √      e     | xi → | ai .
                           N x=0

More generally, for any φ, 0 ≤ φ < 1, FN−1 maps
                          N −1           N −1
                        1 X 2πiφx        X
                       √       e  | xi →      αφ,x | xi                        (1)
                        N x=0            x=0

where the amplitudes αφ,x are concentrated near values of x such that x/N are
good estimates of φ. The closest estimate of φ will have amplitude at least 4/π 2 .
The probability that x/N will be within k/N of φ is at least 1 − 1/(2k − 1). See
[CEMM] for details in the case that N is a power of 2; the same proof works for
any N . Thus to estimate φ such that, with probability at least 1 − ǫ, the error
is less than 1/M , we should use a control register containing values from 0 to
N − 1 and apply FN−1 for any N ≥ M (1/ǫ + 1)/2. For example, if we desire an
error of at most 1/2n with probability at least 1−1/2m we could use N = 2n+m .
In practice, it will be best to use the N that corresponds to the group that is
easiest to represent and work with in the particular physical realisation of the
quantum computer at hand. We expect that this N will be a power of two.
    For convenience, we will omit normalising factors in the remainder of this
paper. It will also be convenient to have a compact notation for the state on
the right hand side of (1) which we consider to be a good estimator for | φi. So
let us refer to this state as φe N or just φe if the value of N is understood.
Lastly, we will use exp(x) to denote ex .


4     The Algorithm
To restrict attention from finitely generated groups G to finite groups we need
to know how to solve the cyclic case (just one generator), that is, to find the
period of a function from Z to the set X. We will first describe how to find the
order of an element a in a group H, or equivalently, the period of the function
f : t → at , as Shor [Sh] did for the group H = Z∗N , the multiplicative group of
integers modulo N . We will then show how to generalise it to find the period of
any function f : Z → X. If f were a homomorphism (so h is an isomorphism of
H, when f is decomposed as f = h ◦ g), we would just be finding the order of
f (1) in H. The difference is that we are showing how to deal with a non-trivial
h which hides the homomorphism structure. The details will also help explain
how to find hidden subgroups of finite Abelian groups.

4.1    Finding Orders in Groups
We have an element a from a group H and we wish to find the smallest positive
integer r such that ar = 1. The group H is not necessarily Abelian; all that
matters is that the subgroup generated by a is Abelian, and this is always true.

                                        5
The idea is to create an operator Ua which corresponds to multiplication by a (so
it maps | yi to | ayi). Since ar = 1, then Uar = I, the identity operator. Hence
the eigenvalues of Ua are rth roots of unity, exp(2πik/r), k = 0, 1, . . . , r − 1. By
estimating a random eigenvalue of Ua , with accuracy 1/2r2 , we can determine
the fraction k/r. The denominator (with the fraction in lowest terms) will be a
factor of r. We thus seek to estimate an eigenvalue of Ua ; note that Uar = Uar .
    For any integer x define Uax to be the operator that maps | yi to | ax yi.
Define Uax to be the operator which maps | xi | yi to | xi Uax | yi = | xi | ax yi.
Note that Uax acts on two registers and x is a variable which takes on the value
in the first register, while Uax acts on one register and x is fixed. Consider the
eigenvectors
                          r−1
                          X
               | Ψk i =         exp(−2πikt/r) at , k = 0, 1, . . . , r − 1,       (2)
                          t=0

of Uax and respective eigenvalues exp(2πikx/r) . If we start with the superpo-
sition
                                  l
                                 2X −1
                                       | xi | Ψk i
                                           x=0
and then apply Uax we get
                                 l
                                2X −1
                                        exp(2πikx/r) | xi | Ψk i .
                                x=0

As discussed in the previous section, applying F2−1 l   to the first register gives
 g | Ψk i and thus a good estimate of k/r.
 k/r                                                                   Pr
   We will not typically have | Ψk i but we do know that | 1i =          k=0 | Ψk i.
Therefore we can start with
                                     r
                                     X          r
                                                X
                    | 0i | 1i = | 0i   | Ψk i =   | 0i | Ψk i                   (3)
                                            k=0          k=0

and then apply F2l to the first register to produce
                                  l        
                             r−1
                             X     2X−1
                                       | xi | Ψk i .                            (4)
                                    k=0      x=0

We then apply Uax to get
                                 l                     
                          r−1
                          X       2X−1
                                      exp(2πikx/r) | xi | Ψk i                  (5)
                          k=0      x=0

followed by F2−1
              l  on the control register to yield
                                          r−1
                                          X
                                                g | Ψk i .
                                                k/r                               (6)
                                          k=0


                                                   6
    Observing the first register will give an estimate of k/r for an integer k
chosen uniformly at random from the set {0, 1, . . . , r − 1}. As shown in [Sh],
we choose l > 2 log2 r, and use the continued fractions algorithm to find the
fraction k/r. Of course, we do not know r, so we must either use an l we
know will be larger than 2 log2 r, such as 2 log2 N in the case that H is Z∗N .
(Alternatively, we could guess a lower bound for r, and if the algorithm fails,
subsequently double the guess and repeat.) We then repeat O(1) times to find r.
This algorithm thus uses O(1) exponentiations, or O(n) group multiplications,
and O(n2 ) elementary quantum operations to do the Fourier transforms.
    We can factor the integer N by finding orders of elements in Z∗N . This uses
only O(n3 ) or exp(c log n) elementary quantum operations, for c = 3 + o(1) (or
c = 2 + o(1) if we use fast Fourier transform
                                        √        techniques). Other deterministic
factoring methods will factor N in O( N ) or exp(cn) steps, where c = 1/2 +
o(1). The best known rigorous probabilistic classical algorithm (using index
calculus methods) [LP] uses exp(c(n log n)1/2 ) elementary classical operations,
c = 1 + o(1). There is also an algorithm with a heuristic expected running
time of exp(c(n1/3 (log n)2/3 ) elementary classical operations (see [MOV] for an
overview and references) for c = 1.902 + o(1). Thus, in terms of elementary
operations, a quantum computer provides a drastic improvement over known
classical methods to factor integers.

4.2    Finding the Period of a Function
The above algorithm, as pointed out in [BL], can be applied to a more general
setting. Replace the mapping from t to at with any function f from the integers
to some finite set X. Define Uf (x) to be an operator that maps f (y) to f (y + x).
This is a generalisation of Uax except it does not matter how it is defined on
values not in the range of f , as long as it is unitary. Define Uf (x) to be an
operator which maps | xi | f (y)i to | xi Uf (x) | f (y)i = | xi | f (y + x)i.
    The following are eigenvectors of Uf (x) :
                        r−1
                        X
             | Ψk i =         exp(−2πikt/r) | f (t)i , k = 0, 1, . . . , r − 1,   (7)
                        t=0

with respective eigenvalues exp(2πikx/r). As in (3), we can start with
                                                  r−1
                                                  X
                                | 0i | f (0)i =         | 0i | Ψk i
                                                  k=0

except with our new, more general, definition of | Ψk i. We apply F2n to the
first register to produce (4), and then apply Uf (x) to produce (5), followed by
F2−1
   n to get (6). Observing the first register will give an estimate of k/r for an

integer k chosen uniformly at random, and the same analysis as in the previous
section applies to find r.
    One important issue is how to compute Uf (x) only knowing how to compute
f . Note that from (4) to (5) (using the modified definition of | Ψk i) we simply

                                              7
go from                                                                      !
                         n                         n
                        2X −1                     2X −1      r−1
                                                             X
                                | xi | f (0)i =                    | xi | Ψk i       (8)
                         x=0                       x=0       k=0

to             n                         n                                       !
              2X −1                     2X −1          r−1
                                                       X
                      | xi | f (x)i =           | xi         exp(2πixk/r) | Ψk i     (9)
               x=0                      x=0            k=0

which could be accomplished by applying Uf , which we do have, to the starting
state                            n
                                2X −1
                                      | xi | 0i .
                                          x=0

Thus even if we do not know how to explicitly compute the operators Uf (x) ,
any operator Uf which computes the function f will give us the state (9). This
state permits us to estimate an eigenvalue of Uf (x) which lets us find the period
of the function f with just O(1) applications of the operator Uf and O(n2 )
other elementary operations. The equality in (9) is the key to the equivalence
between the two approaches to these quantum algorithms. On the left hand side
is the original approach ([Si], [Sh], [BL]) which considers the target register in
the standard computational basis. We can analyse the Fourier transform of the
preimages of these basis states, which is less easy when the Fourier transforms
do not exactly correspond to the group G. On the right hand side of (9) we
consider the target register in a basis containing the eigenvectors of the unitary
operators which we apply to it (as done in [Ki] and [CEMM], for example), and
this gives us (5), from which it is easy to see and analyse the effect of the inverse
Fourier transform even when it does not perfectly match the size of G.

4.3    Finding Hidden Subgroups
As discussed in Sect. 2, any finite Abelian group G is the product of cyclic
groups. In light of the order-finding algorithm, which also permits us to factor,
we can assume that the group G is represented as a product of cyclic groups of
prime power order. Further, for any product of two groups Gp and Gq whose
orders are coprime, any subgroup K of Gp × Gq must be equal to Kp × Kq
from some subgroups Kp and Kq of Gp and Gq respectively. We can therefore
consider our function f separately on Gp and Gq and determine Kp and Kq
separately. Thus we can further restrict ourselves to groups G of prime power
order. This not only simplifies any analysis, it could reduce the size of quantum
control registers necessary in any implementation of these algorithms.
    Let us thus assume that G = Zpm1 × Zpm2 × · · · × Zpml for some prime p and
positive integers m1 ≤ m2 ≤ · · · ≤ ml = m. The ‘promise’ is that f is constant
on cosets of a subgroup K, and distinct on each coset. The hidden subgroup
K is {k = (k1 , k2 , . . . , kl )|f (x) = f (x + k) for all x ∈ G}. In practice, this
will usually be a consequence of the nature of f , as in the case of discrete
logarithms where f (x1 , x2 ) = ax1 bx2 , or whenever f is constructed as h ◦ g for


                                                   8
some homomorphism g from G to some finite group H, and a 1-to-1 mapping
h from H to the set X.
     Let Uf be an operator which maps | xi | 0i to | xi | f (x)i. Define e1 =
(1, 0, . . . , 0), e2 = (0, 1, 0, . . . , 0), and so on. Let us also consider an oper-
ator related to Uf , Uf (xej ) , which maps | xi | f (y)i to | xi Uf (xej ) | f (y)i =
| xi | f (y + xej )i. In the case of Simon’s Problem, the operator Uf (x(0,1,0))
maps | 1i | f (y1 , y2 , y3 )i to | 1i Uf (0,1,0) | f (y1 , y2 , y3 ))i = | 1i | f (y1 , y2 + 1, y3 )i
and does nothing to | 0i | f (y1 , y2 , y3 )i.
     For each t = (t1 , t2 , . . . , tl ), 0 ≤ tj < pmj , satisfying
                       l
                       X
                              pm−mj hj tj = 0 mod pm for all h ∈ K                              (10)
                       j=1

define                                                                           
                               X                     l
                                                −2πi X
                   | Ψt i =             exp                       pm−mj tj aj  | f (a)i .     (11)
                                                   pm       j=1
                              a∈G/K

We are summing over a set of representatives of the cosets of K modulo G,
and by condition (10) on t, this sum is well-defined. Let T denote the set of t
satisfying (10), which corresponds to the group of characters of G/K. The | Ψt i
are eigenvectors of each Uf (xej ) , with respective eigenvalues exp(2πixtj /pmj ) .
By determining these eigenvalues, for j = 1, 2, . . . , l, we will determine t. If we
had | Ψt i in an auxiliary register, we could estimate tj /pmj using Uf (xej ) by the
technique of the previous section. If we use Fp−1 mj we would determine tj exactly,

                                   −1
or we could use the simpler F2k , for some k > log2 (pmj ), and obtain tj with
high probability. For simplicity, we will use Fp−1                                 −1
                                                   mj . In practice we could use F k
                                                                                   2
for a large enough k so that the probability of error is sufficiently small.
    By estimating tj /pmj for j = 1, 2, . . . , l, we determine t. The algorithm
starts by preparing l control registers in the state | 0i and one target or auxiliary
register in the state | Ψt i, applies the appropriate Fourier transforms to produce
                               pm 1
                                               !            pm
                                                                             !
                                X−1                          X l −1

                                        | x1 i · · ·                    | xl i | Ψt i           (12)
                                x1 =0                           xl =0

followed by Uf (xej ) for j = 1, 2, . . . , n, using the jth register as the control and
| Ψt i as the target, to produce
         pm 1 −1
                                  !                    pm l −1
                                                                               !
          X           x1 t1                             X           xl tl
               exp(2πi m1 ) | x1 i · · ·                     exp(2πi m ) | xl i | Ψt i .        (13)
          x =0
                      p                                 x =0
                                                                    p l
            1                                               l



Then apply Fp−1
             mj to the jth control register for each j to yield



                                        | t1 i | t2 i . . . | tl i | Ψ t i                      (14)



                                                        9
from which we can extract t. As in the previous section, we do not know how
to construct | Ψt i, but we do know that
                                          X
                               | f (0)i =   | Ψt i .
                                                         t∈T

So we start with
                                                             X
                          | 0i | 0i · · · | 0i | f (0)i =           | 0i | 0i · · · | 0i | Ψt i
                                                             t∈T

apply Fourier transforms to get
                                     pm 1
                                                   !           pm
                                                                               !
                              X       X−1                       X l −1

                                              | x1 i · · ·                 | xl i | Ψt i               (15)
                              t∈T     x1 =0                        xl =0

then apply Uf (xej ) using the jth register as a control register, for j = 1, 2, . . . , n,
and the last register as the target register to produce

           pm 1 −1
                                       !                     pm l −1
                                                                                    !
     X      X              x1 t1                              X          xl tl
                    exp(2πi m1 ) | x1 i · · ·                     exp(2πi m ) | xl i | Ψt i .          (16)
               x =0
                           p                                 x =0
                                                                         p l
     t∈T        1                                              l


We finally apply Fp−1
                   mj             to the jth control register for j = 1, 2, . . . , l, to produce
                                                X
                                                      | ti | Ψt i .                                    (17)
                                                t∈T

Observing the first register lets us sample the t’s uniformly at random, and
thus with O(n) repetitions we will, by (10), have enough independent linear
relations for us to determine a generating setPfor   K. For example, in the case of
                                                 l
Simon’s problem, the | ti all satisfy t · s = j=1 tj sj mod 2 = 0 mod 2, where
K = {0, s}. We could also guarantee that each new non-zero element of T will
increase the span by a technique discussed in the appendix.
    This analysis of eigenvectors and eigenvalues is based on the work in [Ki].
The problem is that, unlike in [Ki], we do not always have the operator Uf (xej ) .
However, note that, like in Sect. 4.2, going from (15) to (16) maps
                                             
                                  X
                                         | xi | f (0)i
                                           0≤xj ≤pmj

to                                             X
                                                         | xi | f (x)i
                                                    mj
                                           0≤xj ≤p


                    pm 1 −1
                                            !                      pm l −1
                                                                                           !
         X           X          x1 t1                               X           xl tl
     =                   exp(2πi m1 ) | x1 i · · ·                       exp(2πi m ) | xl i | Ψt i .
                    x =0
                                p                                   x =0
                                                                                p l
         t∈T          1                                              l




                                                       10
    We can create state (16) by applying Uf , which we do have, to the starting
state                             X
                                        | xi | 0i
                                 0≤xi <pmi

and proceeding with the remainder of the algorithm. As in Sect. 4.2, we are
considering the target register in the basis containing the eigenvectors | Ψk i
instead of the computational basis.


5     Reducing the Size of Control Registers
5.1    Discrete Logarithms
In practice, it might be advantageous to reduce the number of qubits required
to solve a problem, or the length of time each qubit must be isolated from
the environment. For example, suppose we wish to find m such that am = b,
where the order of a divides r. The operators Uax and Ubx , which correspond to
multiplication by ax and bx respectively, share the eigenvectors | Ψk i (see (2))
and have corresponding eigenvalues exp(2πikx/r) and exp(2πikmx/r). We can
assume we know r by applying the order-finding algorithm if necessary. By using
Uax with one control register we can approximate k/r, and by using Ubx with
another control register we can approximate (km mod r)/r and then extract
m modulo r/gcd(r, k). Note that since we know r, we only need log r bits of
precision when estimating k/r and (km mod r)/r, instead of 2 log2 r when using
continued fractions. Note further that, knowing r, it may be possible to actually
place | Ψk i into the target register (by direct construction or otherwise) for some
known k, and thus only require one control register with over log2 r qubits to
estimate (km mod r)/r. One way of doing this is to keep the target register
after we have applied the order-finding algorithm and observed an estimate of
k/r in the control register. At this point, the target register is almost entirely
in the state | Ψk i, and we could now just estimate the eigenvalue of Ubx on this
eigenstate, which we know will be (km mod r)/r.

5.2    One Control Bit
Consider the case that we have an efficient computational means of mapping
| f (y)i to | f (y + x)i for any x. If we consider f to be of the form h ◦ g for a
homomorphism g, we are requiring that h is the identity or some other function
with enough structure that we can efficiently map h(g(y)) to h(g(y + x)) =
h(g(y)+g(x)). In this case we can efficiently solve the hidden subgroup problem
with only one control bit or a sequence of flying qubits [THLMK]. We illustrate
this method for the problem of finding the order of an element a in a group H.
     Figure 2 shows the relationship between F2−1  n  and the controlled multipli-
cations by powers of a in the order-finding algorithm. As already pointed out
in [GN], the measurements could be performed before the controlled rotations.
The quantum controlled rotations could then be replaced with ‘semi-classically’


                                        11
                                                                        P7
Figure 2: We start with (| 0i + | 1i)(| 0i + | 1i)(| 0i + | 1i) | Ψk i = x=0 | xi | Ψk i.
                                                    P7
The controlled multiplications create the state x=0 exp(2πik/r) | xi | Ψk i. The
remaining gates create the state k/r g (apart from reversing the order of the
qubits) which we then observe. The H-gates correspond to Hadamard trans-
forms, and the Rj -gates correspond to a controlled phase shift of exp(2πi/2j )
on state | 1i.




Figure 3: Here we employ a ‘semi-classical’ version of F2−1 3 . We could mea-
sure each qubit before it is used as a control, perform the controlled rotations
‘semi-classically’, and the probability of observing each possible output state
| x1 i | x2 i | x3 i is the same as in Fig. 2.




                                           12
controlled rotations of the subsequent qubits (that is, the control bit is measured
and, if the outcome is 1, the rotation is done quantumly). This brings us to Fig.
3, where we observe further that all the operations on the first qubit could be
performed before we even prepare the second qubit. All the operations could
be done sequentially, starting from the first qubit, the results of measuring the
previous qubits determining how to prepare the next qubit before measurement.
This means we could in fact do all the quantum controlled multiplications with
a single control qubit provided we can execute the ‘semi-classical’ controls which
allow us to reset a qubit to | 0i + | 1i and perform a rotation dependent upon the
previous measurements (the rotations could in fact be implemented at any time
after resetting the qubit and before applying the final Hadamard transform and
measuring it; they could also be omitted provided we repeat each step a few
extra times and do some additional classical post-processing as done in [Ki]).
Alternatively, the control qubits could be a sequence of flying qubits which are
measured (or prepared) in a way dependent upon the outcomes of the previous
measurements of control qubits.
    For the more general hidden subgroup problem in Abelian groups we would
have a sequence of applications of Uf (xej ) controlled by one qubit, which is
measured, then reset to a superposition of | 0i and | 1i plus some rotation that
is dependent upon the previous measurements. In summary:

 The hidden subgroup K of a finitely generated Abelian group G generated by
e1 , e2 , . . . ek , corresponding to a function f from G to a finite set X, can be
found with probability close to 1 by ‘semi-classical’ methods with only one con-
trol bit (or a sequence of flying qubits) and polynomial in n applications of the
operators | xi | f (y)i → | xi | f (y + xej )i for j = 1, 2, . . . , k, where n is the index
of K in G.


Acknowledgments
Many thanks to Peter Høyer for helping prepare this paper, to Mark Ettinger
and Richard Hughes for helpful discussions and hospitality in Los Alamos, to
BRICS (Basic Research in Computer Science, Centre of the Danish National
Research Foundation), and to Wolfson College.
    This work was supported in part by CESG, the European TMR Research
Network ERP-4061PL95-1412, Hewlett-Packard, The Royal Society London,
and the U.S. National Science Foundation under Grant No. PHY94-07194. Part
of this work was done at the 1997 Elsag-Bailey – I.S.I. Foundation workshop on
quantum computation, at NIS-8 division of the Los Alamos National Labora-
tory, and at the BRICS 1998 workshop on Algorithms in Quantum Information
Processing.




                                            13
References
[BBCDMSSSW] Barenco, A., Bennett, C.H., Cleve, R, DiVincenzo, D.P., Mar-
   golus, N., Shor, P., Sleater, T., Smolin, J., Weinfurter, H.: Phys. Rev. A
   52, (1995) 3457.
[BL] Boneh, D., and Lipton, R.J.: Quantum cryptanalysis of hidden linear
    functions (Extended abstract). Lecture Notes on Computer Science 963
    (1995) 424–437
[CEMM] Cleve, R., Ekert, E., Macchiavello, C., and Mosca, M.: Quantum
   Algorithms Revisited, Proc. Roy. Soc. Lond. A, 454, (1998) 339-354.
[De] Deutsch, D. : Quantum Theory, the Church-Turing principle and the uni-
     versal quantum computer. Proc. Roy. Soc. Lond. A, 400, (1985) 97-117.
[EM] Ekert, A., Mosca, M.: (note in preparation, 1998).
[GN] Griffiths, R.B. and Niu, C.-S.: Semi-classical Fourier Transform for Quan-
    tum Computation, Phys. Rev. Lett. 76 (1996) 3228-3231.
[Gr] Grigoriev, D. Y.: Testing the shift-equivalence of polynomials by determin-
     istic, probabilistic and quantum machines. Theoretical Computer Science,
     180 (1997) 217-228.
[Hø] Høyer, P. : Conjugated Operators in Quantum Algorithms. preprint,
    (1997).
[Jo] Jozsa, R.: Quantum Algorithms and the Fourier Transform, Proc. Roy.
     Soc. Lond. A, 454, (1998) 323-337.
[Ki] Kitaev, A. Y. : Quantum measurements and the Abelian stabiliser problem.
     e-print quant-ph/9511026 (1995)
[LP] Lenstra, H. W. Jr., and Pomerance, C.: A Rigorous Time Bound For
    Factoring Integers, Journal of the AMS, Volume 5, Number 2, (1992) 483-
    516.
[MOV] Menezes, A., van Oorschot, P., Vanstone, S. : Handbook of Applied
   Cryptography, C.R.C. Press, 1997.
[Sh] Shor, P. : Algorithms for quantum computation: Discrete logarithms and
     factoring. Proc. 35th Ann. Symp. on Foundations of Comp. Sci. (1994)
     124–134
[Si] Simon, D.: On the Power of Quantum Computation. Proc. 35th Ann.
     Symp. on Foundations of Comp. Sci. (1994) 116–123
[THLMK] Turchette, Q.A., Hood C.J., Lange W., Mabuchi H., and Kimble
   H.J.: Measurement of conditional phase shifts for quantum logic. Phys.
   Rev. Lett. , 76, 3108 (1996).


                                      14
Appendix: When f is many-to-1 on G/K
The question of what happens when f is many-to-1 on cosets of K was first
addressed in [BL]. This is a slight weakening of the promise that f is distinct
on each coset. Suppose f can have up to m cosets going to the same output,
for some known m. That is, f = h ◦ g where g is a homomorphism from G to a
some group H with kernel K, and h is a mapping from H to X that is at most
m-to-1. If m divides the order of K, we clearly have a problem. For example,
suppose K is the cyclic group of order 2M , and m = 2, but by changing √        one
value of f it √would have period M . It can easily be shown that Ω( M ) (that
is, at least c M for some positive constant c) applications of f are necessary
to distinguish such a modified f from the original one with probability greater
than 3/4, and thus no polynomial time algorithm, quantum or classical, could
distinguish the two cases. Thus one requirement for there to exist an efficient
solution in the worst case is that m is less than the smallest prime factor of |K|,
the number of elements in K.
    The problem when f is not 1-to-1 is the following. Running the same quan-
tum algorithm will produce the state
                                     r−1
                                     X
                                             g | Ψ′ i
                                             k/r  k
                                     k=0

where
                                    r−1
                                    X
                        | Ψ′k i =         exp(−2πikt/r) | f (t)i .
                                    t=0

This is the same definition as in (7) except now the | f (t)i are not necessarily
distinct. This means the sizes of each of the | Ψ′k i are not necessarily the same
since both destructive and constructive interference can occur. Also, the | Ψ′k i
are no longer orthogonal, and thus some constructive interference could occur
on the poor estimates of k/r. Recall that even the close estimates of k/r will
not yield useful results when k = 0. Any other k will at least reveal a small
factor of r. So we need to guarantee that the probability of observing a close
enough estimate of k/r for some k 6= 0 is significant.
    By making our estimates precise enough, say by using over 2 log2 r + ǫ/m2
control qubits, the estimates of k/r will have error less than 1/2r2 (so that
continued fractions will work) with probability at least 1−ǫ/m2 . Thus assuming
f is 1-to-1, the probability of observing a bad output other than 0 would be at
most ǫ/m2 , and the probability of observing 0 would be at most 1/r + ǫ/m2 .
However, since f is at most m-to-1, these probabilities could amplify by at most
a factor of m2 to ǫ and m2 /r + ǫ respectively. Observing a 0 means we either
got a bad output, or the period of f is 1. Getting 0 as a bad output is not very
harmful, however getting another bad output is more complicated, since it will
give us a false factor of r. It will be useful to make ǫ small, so that it is unlikely
our answer is tainted by false factors of r. Once we have one factor r1 of r,
we can replace f (x) with f (r1 x) (as done in [BL]), which has period r/r1 and


                                              15
find a factor of r/r1 . Once we have a big enough factor r′ of r, we might start
observing 0’s, which tells us that the remaining factor of the original r, namely
r/r′ , is less than m2 . Thus we can explicitly test f (r′ ), f (2r′ ), f (3r′ ), . . . , until
we find the period, which will occur after at most m2 applications. We thus have
an algorithm with running time, in terms of elementary quantum operations and
applications of f , polynomial in log(r) and quadratic in m.
    The trick of reducing the order of the function can be applied to reduce the
size of the group and hidden subgroup in the finite Abelian hidden subgroup
problem. When G = Zp , we can efficiently test if K = G or K = {1}. The
above analysis tells us how to deal with the case that G = Zpl for n > 1. A
similar technique will reduce G = Zpl1 × · · · Zplk to a quotient group G and we
can again proceed inductively until the size of G is less than m2 . We can then
exhaustively test G for the hidden subgroup K in another O(m2 ) steps.
    We emphasize that this is a worst-case analysis. If there were a noticeable
difference in the behaviour of a 1-to-1 and an m-to-1 function f , m > 1, we
could decide if a given function h is 1-to-1 or many-to-one (by composing h
with a function f whose period or hidden Abelian subgroup we know, and test
for this difference in behaviour). Distinguishing 1-to-1 functions from many-to-1
functions seems like a very difficult task in general, and would solve the graph
automorphism problem, for example.




                                              16
