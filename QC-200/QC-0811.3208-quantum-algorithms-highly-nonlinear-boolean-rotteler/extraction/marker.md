# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:0811.3208 — Martin Rötteler, 'Quantum algorithms for highly non-linear Boolean functions'
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

arXiv:0811.3208v2  [quant-ph]  24 Nov 2009
Quantum algorithms for highly non-linear Boolean functions
Martin R¨otteler
NEC Laboratories America
4 Independence Way, Suite 200
Princeton, NJ 08540, U.S.A.
mroetteler@nec-labs.com
October 22, 2018
Abstract
Attempts to separate the power of classical and quantum models of computation have a long history.
The ultimate goal is to ﬁnd exponential separations for computational problems. However, such separa-
tions do not come a dime a dozen: while there were some early successes in the form of hidden subgroup
problems for abelian groups–which generalize Shor’s factoring algorithm perhaps most faithfully–only
for a handful of non-abelian groups efﬁcient quantum algorithms were found. Recently, problems have
gotten increased attention that seek to identify hidden sub-structures of other combinatorial and algebraic
objects besides groups. In this paper we provide new examples for exponential separations by consid-
ering hidden shift problems that are deﬁned for several classes of highly non-linear Boolean functions.
These so-called bent functions arise in cryptography, where their property of having perfectly ﬂat Fourier
spectra on the Boolean hypercube gives them resilience against certain types of attack. We present new
quantum algorithms that solve the hidden shift problems for several well-known classes of bent functions
in polynomial time and with a constant number of queries, while the classical query complexity is shown
to be exponential. Our approach uses a technique that exploits the duality between bent functions and
their Fourier transforms.
1
Introduction
A salient feature of quantum computers is that they allow to solve certain problems much more efﬁciently
than any classical machine. The ultimate goal of quantum computing is to ﬁnd problems for which an
exponential separations between quantum and classical models of computation can be shown in terms of
the required resources such as time, space, communication, or queries. It turns out that the question about
a provably exponential advantage of a quantum computer over classical computers is a challenging one and
examples showing a separation are not easy to come by. Currently, only few (promise) problems giving an
exponential separation between quantum and classical computing are known. A common feature they share
is that, simply put, they all ask to extract hidden features of certain algebraic structures. Examples for this
are hidden shift problems [vDHI03], hidden non-linear structures [CSV07], and hidden subgroup problems
(HSPs). The latter class of hidden subgroup problems was studied quite extensively over the past decade.
There are some successes such as the efﬁcient solution of the HSP for any abelian group [Sho97, Kit97],
including factoring and discrete log as well as Pell’s equation [Hal02], and efﬁcient solutions for some non-
abelian groups [FIM+03, BCvD05]. However, meanwhile some limitations of the known approaches to this
1


---- page 2 ----

problem are known [HMR+06] and presently it is unclear whether the HSP can lend itself to a solution to
other interesting problems such as the graph isomorphism problem.
Most of these methods invoke Fourier analysis over a ﬁnite group G. In some sense the Fourier transform
is good at capturing some non-trivial global properties of a function f which at the same time are hard to
ﬁgure out for the classical computer which can probe the function only locally at polynomially many places.
For many groups G the quantum computer has the unique ability to compute a Fourier transform for G very
efﬁciently, i. e., in time logO(1) n, where n is the input size. Even though the access to the Fourier spectrum
is somewhat limited, namely via sampling, it nevertheless has been shown that this limited access can be
quite powerful. Historically, the ﬁrst promise problems which tried to leverage this power were deﬁned for
certain classes of Boolean functions: the Deutsch-Jozsa problem [DJ92] is to decide whether a Boolean
function f : Zn
2 →Z2 that is promised to be either constant or a balanced function is actually constant
or balanced. In the Fourier picture this asks to distinguish between functions that have all their spectrum
supported on the 0 frequency and functions which have no 0 frequency component at all. It therefore comes
as no surprise that by sampling from the Fourier spectrum the problem can be solved. Furthermore, it can
be shown that any deterministic classical algorithm must make an exponential number of queries. However,
this problem can be solved on a bounded error polynomial time classical machine. Hence other, more
challenging, problems were sought which asked for more sophisticated features of the function f and were
still amenable to Fourier sampling. One such problem is to identify r ∈Zn
2 from black box access to a linear
Boolean function f(x) = rx, where x ∈Zn
2. Again, in the Fourier domain the picture looks very simple as
each f corresponds to a perfect delta peak localized at frequency r, leading to an exact quantum algorithm
which identiﬁes r using a single query. Classically, it can be shown that Θ(n) queries are necessary and
sufﬁcient to identify r with bounded error. Based on the observation that a quantum computer can even
handle the case well in which access to x is not immediate but rather through solving another problem of
a smaller size, Bernstein and Vazirani [BV97] deﬁned the recursive Fourier sampling (RFS) problem by
organizing many instances of learning a hidden linear function in a tree-like fashion. By choosing the height
of this tree to be log n they showed a separation between quantum computers, which can solve the problem
in n queries, and classical computers which require nlog n queries. Soon after this, more algorithms were
found that used the power of Fourier sampling over an abelian group, namely Simon’s algorithm [Sim94]
for certain functions f : Zn
2 →Zn−1
2
, and Shor’s algorithms [Sho97], where f was deﬁned on cyclic groups
and products thereof, eventually leading to the HSP.
The idea to achieve speedups from Boolean functions themselves has obtained signiﬁcantly less atten-
tion. Recently, Hallgren and Harrow [HH08] revisited the RFS problem and showed that other unitary
matrices can serve the role of the Fourier transform in the deﬁnition of RFS problems. They have obtained
superpolynomial speedups over classical computing for a wide class of Boolean functions and unitary matri-
ces, including random unitary matrices. Together with lower bound results [Aar03] this gives a reasonably
good understanding of the power and limitations of the RFS problem. In another important development, it
was shown that the ability to efﬁciently perform Fourier transforms on a quantum computer can also be used
to efﬁciently perform correlations between certain functions. In the so-called hidden shift problem deﬁned
by van Dam, Hallgren, and Ip [vDHI03] this was used in the context of computing a correlation between
a black box implementation of f(x) =

x+s
p

, where

x
p

denotes the Legendre symbol and s ∈Zp is a
ﬁxed element, and the Legendre symbol itself. The main idea behind this is that the Fourier transform of a
shifted function picks up a linear phase which depends on the shift. Since a correlation corresponds to point-
wise multiplication of the Fourier transforms and since the Legendre symbol is its own Fourier transform,
the correlation can be performed by computing the Legendre symbol into the phase, leading to an efﬁcient
algorithm that needs only a constant number of queries. The classical query complexity of this problem is
2


---- page 3 ----

polynomial in log p.
Our results. Our main contribution is a generalization of the hidden shift problem for a class of Boolean
functions known as bent functions [Rot76]. Bent functions are those Boolean functions for which the Ham-
ming distance to the set of all linear Boolean functions is maximum (based on comparing their truth tables).
For this reason bent functions are also called maximum non-linear functions.1 A direct consequence of this
is that the Fourier transform of a bent function f is perfectly ﬂat, i. e., in absolute value all Fourier coef-
ﬁcients, which are deﬁned with respect to the real valued function x 7→(−1)f(x), are equal and as small
as possible. This feature of having a ﬂat Fourier spectrum is desirable for cryptographic purposes because,
roughly speaking, such a function is maximally resistant against attacks that seek to exploit a dependence
of the outputs on some linear subspace of the inputs. It turns out that bent functions exist if and only if the
number of variables is even and that there are many of them: asymptotically, the number of bent functions in
n variables is at least Ω

2n/2+1
e
2n/2 √
2π2n/2

, see for instance [CG06]. What is more, several explicit
constructions of inﬁnite families of bent functions are known and they are related to so-called difference sets
which are objects studied in combinatorics. Since the Fourier transform of f is ﬂat and the Boolean Fourier
transform is real, it follows that (up to normalization) the Fourier spectrum takes only values ±1, i. e.,
it again is described by a Boolean function, called the dual bent function and denoted by ef. Arguably, the
most prominent example for a bent function is the inner product function ipn(x1, . . . , xn) = Pn/2
i=1 x2i−1x2i
written in short as ipn(x, y) = xyt. This function can be generalized to f(x, y) = xπ(y)t + g(y), where π
is an arbitrary permutation of strings of length n/2 and g : Zn/2
2
→Z2 is an arbitrary function. This leads
to the class of so-called Maiorana-McFarland bent functions. The dual bent function is then given by the
Boolean function ef(x, y) = π−1(x)yt + g(π−1(x)).
We deﬁne the hidden shift problem for a ﬁxed bent function f as follows: an oracle O provides us with
access to f and g, where g is promised to be a shifted version of f with respect to some unknown shift s.
Using oracles of this kind, we show an exponential separation of the quantum and classical query complexity
of the hidden shift problem, the former being at most linear, the latter being exponential. Furthermore, we
also consider a variation of the problem where an oracle e
O in addition provides oracle access to the dual
bent function ef. We show that s can be extracted from eO by a quantum algorithm using one query to f
and one query to ef. We present two other classes of bent functions, namely the partial spread class deﬁned
by Dillon [Dil75] and a class deﬁned by Dobbertin [Dob95], which uses properties of certain Kloosterman
sums over ﬁnite ﬁelds to show the bentness of the functions.
What is the signiﬁcance of our result? In short, we provide new examples for exponential separations
between quantum and classical computing. The class of problems studied in this paper yields a large new
set of problems for exponential separations in query complexity with respect to oracles. A feature of the
quantum algorithms presented here are their simplicity in that besides classical computation of function
values the only quantum operation required are the Fourier transform over the groups Zn
2.
How does this relate to other separations? While exponential separations in query complexity were
known before, for instance for abelian hidden subgroup problems, the hidden shift problems for bent func-
tions are the ﬁrst problems for which such a separation can be shown from Boolean functions. In the case
of abelian HSP for order 2 subgroups of Zn
2, it is possible to assume that the functions hiding the hidden
subgroup take the form f(x) = π(Ax), where A ∈F(n−1)×n
2
is a matrix of rank n −1, and π is a permu-
1Note that high nonlinearity of a function refers to the spectral characterization, i. e., the Hamming weight of the highest non-
zero frequency component is high. It does not imply that f(x) = P
ν∈Zn
2 ανxν, when written as a multivariate polynomial over
F2, has a high (algebraic) degree, deﬁned as the maximum degree of any monomial xν. Indeed, there are many examples of highly
nonlinear functions whose algebraic degree is 2.
3


---- page 4 ----

tation of strings of length n −1. The goal is to ﬁnd a vector s ∈Fn
2 in the kernel of A. Note that these
functions are not Boolean functions but rather functions from Zn
2 →Zn−1
2
. To the best of our knowledge the
best separations that were obtainable so far from Boolean functions were the superpolynomial separations
shown in [HH08]. Those were obtained by generalizing the ideas of recursive Fourier sampling from parity
functions to more general classes of Boolean functions.
Related work. The techniques used in this paper are related to the techniques used in [vDHI03], in
particular the method of using the Fourier transform thrice in order to correlate a shifted function with
a given reference function, thereby solving a deconvolution problem. We see the main difference in the
richness of the class of Boolean functions for which the method can be applied and the query lower bound.
It was observed in [FIM+03, Kup05] that the hidden shift problem for injective functions f, g : G →S
from an abelian G to a set S is equivalent to hidden subgroup problem over G ⋊Z2, where the action of Z2
on G is given by the inverse. There are several other papers that deal with the injective hidden shift problem
over abelian and non-abelian groups [CvD07, CW07, MRRS07]. In contrast, the functions studied here
are deﬁned on the abelian group Zn
2 and very far from being injective. As we show it will be nevertheless
possible to deﬁne a related hidden subgroup problem over an elementary abelian group, however, for this
we have to consider “quantum functions” to encode the period.
Perhaps most closely related to our scenario is the work by Russell and Shparlinski [RS04] who consid-
ered shift problems for the case of χ(f(x)), where f is a polynomial on a ﬁnite group G and χ a character
of G, a general setup that includes our scenario. The two cases for which algorithms were given in [RS04]
are the reconstruction of a monic, square-free polynomial f ∈Fp[X], where χ is the quadratic character
(Legendre symbol) over Fp and the reconstruction of a hidden shift over a ﬁnite group χ(sx), where χ is the
character of a known irreducible representation of G. The technique used in [RS04] is a generalization of
the technique of [vDHI03]. In the present paper we extend the class of functions for which the hidden shift
problem can be solved to the case where f is a multivariate polynomial and G is the group Zn
2.
Related to the hidden shift problem is the problem of unknown shifts, i. e., problems in which we are
given a supply of quantum states of the form |D + s⟩, where s is random, and D has to be identiﬁed.
Problems of this kind have been studied by Childs, Vazirani, and Schulman [CSV07], where D is a sphere of
unknown radius, Decker, Draisma, and Wocjan [DDW08], where D is a graph of a function, and Montanaro
[Mon09], where D is the set of points of a ﬁxed Hamming-weight. The latter paper also considers the cases
where D hides other Boolean functions such as juntas, a problem that was also studied in [AS07]. In contrast
to all these problems in our case the set D is already known, but the shift s has to be identiﬁed.
We are only aware of relatively few occasions where bent functions have been used in theoretical com-
puter science: they were used in the context of learning of intersections of halfspaces [KS07], where they
gave rise to maximum possible number of slicings of edges of the hypercube. Also the recent counterexam-
ple for failure of the inverse Gowers conjecture in small characteristic [LMS08] uses a special bent function.
2
Fourier analysis of Boolean functions
We recall some basic facts about Fourier analysis of Boolean functions, see also the recent review article
[dW08] for an introduction. Let f : Zn
2 →R be a real valued function on the n-dimensional Boolean
hypercube. The Fourier representation of f is deﬁned as follows. First note that for any subset S ⊆[n] =
{1, . . . , n} we can deﬁne a character of Zn
2 via χS : x 7→(−1)Sxt, where x ∈Zn
2 (the transpose is necessary
as we assume that all vectors are row vectors). The inner product of two functions on the hypercube is
deﬁned as ⟨f, g⟩=
1
2n
P
x f(x)g(x) = Ex(fg). The χS are inequivalent characters of Zn
2, hence they obey
the orthogonality relation Ex(χSχT ) = δS,T . The Fourier transform of f is a function bf : Zn
2 →R deﬁned
4


---- page 5 ----

by
bf(S) = Ex(fχS) = 1
2n
X
x∈Zn
2
χS(x)f(x),
(1)
bf(S) is the Fourier coefﬁcient of f at frequency S, the set of all Fourier coefﬁcients is called the Fourier
spectrum of f and we have the representation f = P
S bf(S)χS. Two useful facts about the Fourier trans-
form of Boolean functions are Parseval’s identity and the convolution property. Parseval’s identity says
that ∥f∥2
2 = P
S bf(S)2 which is a special case of ⟨f, g⟩= P
S bf(S)bg(S). For two Boolean functions
f, g : Zn
2 →R their convolution (f ∗g) is the function deﬁned as (f ∗g)(x) =
1
2n
P
y∈Zn
2 f(x + y)g(y). A
standard feature of the Fourier transform is that it maps the group operation to a point wise operation in the
Fourier domain. Concretely, this means that [
f ∗g(S) = bf(S)bg(S), i. e., convolution becomes point-wise
multiplication and vice-versa.
In quantum notation the Fourier transform on the Boolean hypercube differs slightly in terms of the
normalization and is given by the unitary matrix
H2n =
1
√
2n
X
x,y∈Zn
2
(−1)xyt |x⟩⟨y| .
This is sometimes called the Hadamard transform [NC00]. In this paper we will also use the Fourier spec-
trum deﬁned with respect to the Hadamard transform which differs from (1) by a factor of 2−n/2. It is
immediate from the deﬁnition of H2n that it can be written in terms of a tensor (Kronecker) product of the
Hadamard matrix of size 2 × 2, namely H2n = (H2)⊗n, a fact which makes this transform appealing to use
on a quantum computer since it can be computed using O(n) elementary operations. Also note that in the
context of cryptography also the name Walsh-Hadamard transform for H2n is common.
Another note on a convention which applies when we consider Z2 valued functions f : Zn
2 →Z2. Then
we tacitly assume that the real valued function corresponding to f is actually F : x 7→(−1)f(x). The
Fourier transform is then deﬁned with respect to F, i. e., we obtain that
bF(w) = 1
2n
X
x∈Zn
2
(−1)wxt+f(x),
(2)
where we use w ∈Zn
2 instead of S ⊆[n] to denote the frequencies. Other than this notational convention,
the Fourier transform used in (2) for Boolean valued functions and the Fourier transform used in (1) for real
valued functions are the same. In the paper we will sloppily identify bf = bF and it will be clear from the
context which deﬁnition has to be used.
3
Bent functions
Deﬁnition 1. Let f : Zn
2 →Z2 be a Boolean function. We say that f is bent if the Fourier coefﬁcients
bf(w) =
1
2n
P
x∈Zn
2 (−1)wxt+f(x) satisfy | bf(w)| = 2−n/2 for all w ∈Zn
2, i. e., if the spectrum of f is ﬂat.
Necessary for bent functions in n variables to exist is that n is even [Dil75, MS77]. If f is bent, then
this implicitly deﬁnes another Boolean function via 2n/2 bf(w) =: (−1) ef(w). Then this function ef is again a
bent function and called the dual bent function of f. By taking the dual twice we obtain f back: eef = f.
5


---- page 6 ----

3.1
A ﬁrst example: the inner product function
The most simple bent function is f(x, y) := xy where x, y ∈Z2. It is easy to verify that f deﬁnes a bent
function. This can be generalized to 2n variables [MS77] and we obtain the inner product
ipn(x1, . . . , xn, y1, . . . , yn) :=
n
X
i=1
xiyi.
Again, it is easy to see that ipn is bent. In Section 3.2 we will see that ipn belongs to a much larger class
of bent functions. There (in Lemma 4) we also establish that that ipn = eipn is its own dual bent function
which also implies that the vector [(−1)ipn(x,y)]x,y∈Zn
2 is an eigenvector of H2n. This should be compared
to [vDHI03] where it was used that the Legendre symbol

·
p

gives rise to an eigenvector of the Fourier
transform DFTp over the cyclic group Zp. The shift problem for the inner product function is closely related
to the Fourier sampling problem of ﬁnding a string a that is hidden by the function f(a, x) = axt [BV97],
and indeed the string a can be readily identiﬁed from the state
1
√
2n
P
x∈Zn
2 (−1)axt |x⟩. In the hidden shift
problem the problem is to identify (a, b) from
1
2n
P
x,y∈Zn
2 (−1)ipn(x+a,y+b) |x, y⟩. This state is up to a
global phase given by
1
2n
P
x,y∈Zn
2 (−1)xyt+xbt+yat |x, y⟩. By computing ipn into the phase the latter can be
mapped to
1
2n
P
x,y∈Zn
2 (−1)xbt+yat |x, y⟩. From this state the string (a, b) can be extracted by applying to it
a Boolean Fourier transform followed by measurement in the computational basis.
3.2
Bent function families
Many examples of bent functions are known and we brieﬂy review some of these classes. Recall that
any quadratic Boolean function f has the form f(x1, . . . , xn) = P
i<j qi,jxixj + P
i ℓixi which can be
written as f(x) = xQxt + Lxt, where x = (x1, . . . , xn) ∈Zn
2. Here, Q ∈Fn×n
2
is an upper triangular
matrix and L ∈Fn
2. Note that since we are working over the Boolean numbers, we can without loss of
generality assume that the diagonal of Q is zero (otherwise, we can absorb the terms into L). It is useful
to consider the associated symplectic matrix B = (Q + Qt) with zero diagonal which deﬁnes a symplectic
form B(u, v) = uBvt. This form is non-degenerate if and only if rank(B) = n. The coset of f + R(n, 1)
of the ﬁrst order Reed-Muller code is described by the rank of B. This follows from Dickson’s theorem
[MS77] which gives a complete classiﬁcation of symplectic forms over Z2:
Theorem 1 (Dickson). Let B ∈Zn×n
2
be a symmetric matrix with zero diagonal (such matrices are also
called symplectic matrices). Then there exists R ∈GL(n, Z2) and h ∈[n/2] such that RBRt = D, where
D is the matrix (1h ⊗σx) ⊕0n−2h considered as a matrix over Z2 (where σx is the permutation matrix
corresponding to (1, 2)). In particular, the rank of B is always even. Furthermore, under the base change
given by R the function f becomes the quadratic form iph(x1, . . . , x2h) + L′(x1, . . . , xn) where we used
the inner product function iph and a linear function L′.
Next, we give a characterization of the Fourier transform of an afﬁne transform of a bent function.
Lemma 2 (Afﬁne transforms). Let f be a bent function, let A ∈GL(n, Z2) and b ∈Zn
2, and deﬁne
g(x) := f(xA + b). Then also g(x) is a bent function and bg(w) = (−1)−w(A−1)tb bf(w(A−1)t) for all
w ∈Zn
2.
6


---- page 7 ----

Proof. We compute bg(w) using the substitution y = xA + b as follows:
bg(w)
=
1
2n
X
x
(−1)wxt+f(xA+b)
=
1
2n
X
y
(−1)w·(A−1)t(y−b)t+f(y)
=
1
2n (−1)−w(A−1)tb X
y
(−1)w(A−1)tyt+f(y)
=
(−1)−w(A−1)tb bf(w(A−1)t).
By combining Theorem 1 and Lemma 2 we arrive at the following corollary which characterizes the
class of quadratic bent functions.
Corollary 3. Let f(x) = xQxt + Lxt be a quadratic Boolean function such that the associated symplectic
matrix B = (Q+Qt) satisﬁes rank(B) = 2h = n. Then f is a bent function. The dual of this bent function
is again a quadratic bent function.
A complete classiﬁcation of all bent functions has only been achieved for n = 2, 4, and 6 variables.
For larger number of variables some families are known, basically coming from ad hoc constructions. We
present another one of the known families called M (Maiorana and McFarland). First, we remark there
are also constructions for making new bent functions from known ones, the simplest one takes two bent
functions f and g in n and m variables and outputs (x, y) 7→f(x) ⊕g(y). The class M of Maiorana-
McFarland bent functions consists of the functions f(x, y) := xπ(y)t + g(y), where π is an arbitrary
permutation of Zn
2 and g is an arbitrary Boolean function depending on y only. The following lemma
characterizes the dual of a bent function in M.
Lemma 4. Let f(x, y) := xπ(y)t + g(y) be a Maiorana-McFarland bent function. Then the dual bent
function of f is given by ef(x, y) = π−1(x)yt + g(π−1(x)).
Proof. Let bf(u, v) be the Fourier transform of f at (u, v) ∈Z2n
2 . We obtain
bf(u, v)
=
1
22n
X
x,y∈Zn
2
(−1)f(x,y)+(u,v)(x,y)t
=
1
22n
X
x,y∈Zn
2
(−1)xπ(y)t+g(y)+(u,v)(x,y)t
=
1
22n
X
y∈Zn
2
(−1)vyt+g(y)

X
x∈Zn
2
(−1)(u+π(y))xt


=
1
2n
X
y∈Zn
2
(−1)vyt+g(y)δu,π(y)
=
1
2n (−1)vπ−1(u)t+g(π−1(u)).
Hence the dual bent function is given by ef(x, y) = π−1(x)yt + g(π−1(x)).
7


---- page 8 ----

Another class of bent functions called PS (partial spreads) was introduced by Dillon [Dil75] and provides
examples of bent functions outside of M.
Theorem 5. [Dil75] Let U1, . . . , U2n/2−1 be n/2-dimensional subspaces of Zn
2 such that Ui ∩Uj = {0}
holds for all i ̸= j. Let χi be the characteristic function of Ui. Then f := P2n/2−1
i=1
χi is a bent function.
A collection of sets Ui as in Theorem 5 is called a partial spread. Explicitly, the Ui can be chosen as
Ui = {(x, aix) : x ∈F2n/2} where ai ∈F×
2n/2 satisﬁes g(ai) = 1 for a ﬁxed balanced function g. Here
we have identiﬁed Zn
2 with the ﬁnite ﬁeld F2n by choosing a polynomial basis. This provides an explicit
construction for bent functions in PS. A further class deﬁned by Dobbertin has the property to include M
and PS is deﬁned as follows: ﬁrst, identify Zn
2 with F2n/2 × F2n/2. Let g be a balanced Boolean function of
n/2 variables, ϕ be a permutation of F2n/2 and ψ be an arbitrary map from F2n/2 to F2n/2. Then
f(x, y) :=
(
g

x+ψ(ϕ−1(y))
ϕ−1(y)

: if y ̸= 0,
0
: if y = 0
is a bent function.
There are other constructions of bent functions by means of so-called trace monomials. For this con-
nection, an understanding of certain Kloosterman sums turns out to be important. Recall that the Klooster-
man sum in F2n is deﬁned as Kl(a) = P
x∈F×
2n(−1)tr(x−1+ax), where F×
2n denotes the non-zero elements
of F2n and tr denotes the trace map from F2n to Z2. For a ∈F2n let fa(x) be the Boolean function
fa(x) = tr(ax2n/2−1). It is known that if a is contained in the subﬁeld F2n/2 and Kl(a) = −1, then fa
is a bent function [Dil75]. The existence of such an element a was conjectured in Dillon’s paper and was
proved in [LW90] (see also [HZ99]) where its existence was shown for all n, thereby showing existence
bent functions in this class of trace monomials.
3.3
Other characterizations of bent functions
Finally, we note that there are many other characterizations of bent functions via other combinatorial objects,
in particular difference sets. The connection is rather simple: we get that Df := {x : f(x) = 1} is a
difference set in Zn
2, i. e., the set ∆Df = {d1 −d2 : d1, d2 ∈Df} of differences covers each non-zero
element of Zn
2 an equal number of times. We brieﬂy highlight some other connections to combinatorial
objects in the following:
Circulant Hadamard matrices.
Bent functions give rise to Hadamard matrices of size 2n × 2n in a very
natural way as group circulants as follows. Let Af := ((−1)f(x+y))x,y∈Zn
2 , then f is bent if and only if
Af is a Hadamard matrix, i. e, AfA†
f = n1n. Another way of saying this is that the shifted functions
x 7→(−1)f(x+s) for s ∈Zn
2 are orthogonal. Moreover, in the basis given by the columns of H2n the matrix
Af becomes diagonal, the diagonal entries being ef(x).
Balanced derivatives.
Besides the property of Af being a Hadamard matrix another equivalent character-
izations of f to be bent is that the function ∆h(f) := f(x + h) + f(x) is a balanced Boolean function (i. e.,
f takes 0 and 1 equally often) for all non-zero h.
8


---- page 9 ----

Reed-Muller codes.
Bent functions can also be characterized in terms of the Reed-Muller codes [MS77].
Recall that the set of all truth tables (evaluations) of all polynomials over Z2 of degree up to r in n variables
is called the Reed-Muller R(n, r). Then bent functions correspond to functions which have the maximum
possible distance to all linear functions, i. e., elements of R(n, 1). Quadratic bent functions in R(n, 2) are
of particular interest. They correspond to symplectic forms of maximal rank and play a role, e. g., in the
deﬁnition of the Kerdock codes.
Difference sets.
Finally, we note that bent functions are equivalent to objects known as difference sets in
combinatorics, namely difference sets for the elementary abelian groups Zn
2 [BJL99]. A difference set is
deﬁned as follows: Let G be a ﬁnite group of order v = |G|. A (v, k, λ)-difference set in G is a subset
D ⊆G such that the following properties are satisﬁed: |D| = k and the set ∆D = {a −b : a, b ∈D, a ̸=
b} contains every element in G precisely λ times. Examples for difference sets are for instance the set
D = {x2 : x ∈Fq} of all squares in a ﬁnite ﬁeld. Here the group G is the additive group of Fq, where
q ≡3 (mod 4) is a prime power. The parameters of this family of difference sets is given by (q, q−1
2 , q−3
4 ).
Bent functions on the other hand give rise to difference sets in the elementary abelian group G = Zn
2. The
connection is as follows: Df := {x : f(x) = 1} is a difference set in Zn
2 if and only if f is a bent function,
a result due to Dillon [Dil75]. In this fashion we obtain (2n, 2n−1 ± 2(n−2)/2, 2n−2 ± 2(n−2)/2) difference
sets in Zn
2, see also [BJL99].
4
Quantum algorithms for the shifted bent function problem
We introduce the hidden shift problem for Boolean functions. In general, the hidden shift problem is a
quite natural source of problems for which a quantum computer might have an advantage over a classical
computer. See [CvD08] for more background on hidden shifts and related problems.
Deﬁnition 2 (Hidden shift problem). Let n ≥1 and let Of be an oracle which gives access to two Boolean
functions f, g : Zn
2 →Z2 such that the following conditions hold: (i) f, and g are bent functions, and (ii)
there exist s ∈Zn
2 such that g(x) = f(x + s) for all x ∈Zn
2. We then say that Of hides an instance of a
shifted bent function problem for the bent function f and the hidden shift s ∈Zn
2. If in addition to f and g
the oracle also provides access to the dual bent function ef, then we use the notation Of, ef to indicate this
potentially more powerful oracle.
Theorem 6. Let Of, ef be an oracle that hides an instance of a shifted bent function problem for a function
f and hidden shift s and provides access to the dual bent function ef. Then there exists a polynomial time
quantum algorithm A1 that computes s with zero error and makes two quantum queries to Of, ef.
Proof. Let f : Zn
2 →Z2 be the bent function. We have oracle access to the shifted function g(x) = f(x+s)
via the oracle, i. e., we can apply the map |x⟩|0⟩7→|x⟩|f(x + s)⟩where s ∈Zn
2 is the unknown string.
Recall that whenever we have a function implemented as |x⟩|0⟩7→|x⟩|f(x)⟩, we can also compute f into
the phase as Uf : |x⟩7→(−1)f(x) |x⟩by applying f to a qubit initialized in
1
√
2(|0⟩−|1⟩). The hidden
shift problem is solved by the following algorithm A1: (i) Prepare the initial state |0⟩, (ii) apply the Fourier
transform H⊗n
2
to prepare an equal superposition
1
√
2n
P
x∈Zn
2 |x⟩of all inputs, (iii) compute the shifted
function g into the phase to get
1
√
2n
P
x∈Zn
2 (−1)f(x+s) |x⟩, (iv) Apply H⊗n
2
to get P
w(−1)swt bf(w) |w⟩=
1
√
2n
P
w(−1)swt(−1) ef(w) |w⟩, (v) compute the function |w⟩7→(−1) ef(w) |w⟩into the phase resulting in
1
√
2n
P
w(−1)swt |w⟩, where we have used the fact that f is a bent function, and (vi) ﬁnally apply another
9


---- page 10 ----

Hadamard transform H⊗n
2
to get the state |s⟩and measure s. From this description it is clear that we
needed one query to g and one query to ef to solve the problem, that the algorithm is exact, and that the
overall running time is given by O(n) quantum operations. A quantum circuit implementing this algorithm
is shown in Figure 1(a).
Next, we consider the situation where the oracle deﬁnes a hidden shift problem but does not provide
access to the dual bent function. It turns out that in this case we can still extract the hidden shift with a
polynomial time quantum algorithm, however the number of queries increases from constant to linear.
Theorem 7. Let Of be an oracle that hides an instance of a shifted bent function problem for a function f
and hidden shift s. Then there exists a polynomial time quantum algorithm A2 that computes s with constant
probability of success and makes O(n) queries to Of.
Proof. First, note that as in Theorem 6 we can assume that the oracle computes the functions f, g : Zn
2 →Z2
into the phase. Furthermore, we can assume that the oracle can be applied conditionally on a bit b, i. e.,
we can apply the map Λ1(Uf) : |b⟩|x⟩7→|b⟩|x⟩if b = 0 and |b⟩|x⟩7→|b⟩(−1)f(x) |x⟩if b = 1.
Indeed, using a Fredkin gate FRED (see [NC00]) which speciﬁed by |b⟩|x⟩|y⟩7→|b⟩|x⟩|y⟩if b = 0 and
|b⟩|x⟩|y⟩7→|b⟩|y⟩|x⟩if b = 1, it is easy to implement Λ1(Uf) as follows: (Λ1(Uf) ⊗12n) |b⟩|x⟩|0⟩=
(FRED ◦(12 ⊗Uf ⊗12n) ◦FRED) |b⟩|x⟩|0⟩, up to a global phase.
We prove the theorem by reducing to an abelian hidden subgroup problem in the group Zn+1
2
. To do
this, we use f and g to deﬁne “quantum functions”, namely F : x 7→P
y∈Zn
2 (−1)f(x+y) |y⟩and G :
x 7→P
y∈Zn
2 (−1)g(x+y) |y⟩. Observe that due to the bentness of f and g, the two functions F and G
are injective quantum functions, i. e., they are injective complex valued functions that with respect to some
basis, which in general might be different from the computational basis, become classical injective functions.
Indeed, this follows from the fact that all derivatives of a bent function are balanced, see Section 3.2. Now,
a well known connection between the hidden shift problem for injective functions f, g over an abelian
group A and a hidden subgroup problem can be used [Kup05, FIM+03]. For this, the hidden subgroup
problem is deﬁned with respect to the semidirect product A ⋊Z2 where the action is given by inversion
in A. In our case we have A ⋊Z2 ∼= Zn+1
2
since the inversion action is trivial over Z2. The hiding
function for the HSP over Zn+1
2
is deﬁned as H(b, x) = F(x) if b = 0 and H(b, x) = G(x) if b = 1.
This deﬁnes a hidden subgroup {(0, 0), (1, s)} of order 2, knowledge of which clearly implies that we
know s. Once we have shown how to implement the hiding function H, the algorithm will therefore be
the standard algorithm for the HSP: (i) Prepare the initial state |0⟩, (ii) apply the Fourier transform H⊗n
2
to
prepare an equal superposition
1
√
2n+1
P
b∈Z2,x∈Zn
2 |x⟩of all inputs, (iii) compute the function into the second
register to get
1
√
2n+1
P
b∈Z2,x∈Zn
2 |b, x⟩|H(b, x)⟩, (iv) Apply H⊗n+1
2
to the ﬁrst register, and (v) measure
the ﬁrst register. This leads to a measurement result a ∈Zn+1
2
that satisﬁes (1, s)at = 0. Repeating
steps (i)-(v) a total number of O(n) times, we get a constant probability to uniquely characterize s from
the measurement data. Hence, the algorithm needs O(n) queries to f and g to solve the problem and the
overall running time is given by O(n2) quantum operations. The function H(b, x) can be implemented in
a straightforward way using Hadamard transforms, controlled NOT operations [NC00], and the controlled
oracle calls Λ1(Uf) mentioned above. A quantum circuit implementing one iteration of this algorithm is
shown in Figure 1(b).
It is perhaps interesting to note that the “probabilistic method” of directly implementing ef via sampling
of f at a polynomial number of inputs and using the Chernoff bound is not sufﬁcient for our purposes (see
e. g., [Man94] for the argument that P
i∈I χS(xi)f(xi) is exponentially close to ef for all S for a sample set
10


---- page 11 ----

|0⟩⊗n ✂✂H⊗n
Ug
H⊗n
U ef
H⊗n
|s⟩
(a) Quantum algorithm A1
|0⟩⊗n
|0⟩⊗n
|0⟩
✂✂
✂✂
H⊗n
H⊗n
H
t
♥Ug
t
Uf
❞
t
♥H⊗n
H⊗n
H







meas.
(b) Quantum algorithm A2
Figure 1: Quantum algorithms for the hidden shift problem for bent functions. The quantum circuit in (a)
implements algorithm A1. This algorithm can be used if access to the shifted function g(x) = f(x + s) as
well as access to the dual bent function ef is given. The algorithm uses one query to g and one query to ef
and is zero-error, i. e., it always returns the hidden shift s. The quantum circuit in (b) implements algorithm
A2. This algorithm uses access to f and g only and can be applied if access to ef is not available. The shown
circuit has to be applied O(n) times, after which the data acquired by measuring the upper n + 1 qubits
characterizes the hidden shift s with constant probability of success.
I of polynomial size). The issue is that for bent functions we would have to distinguish exponentially small
Fourier coefﬁcients ±1/
√
2n. We conjecture that in the worst case it takes an exponential number of queries
to f in order to implement one query to ef, but have no proof for this.
Finally, we state the two results that provide new query complexity separations between quantum and
classical algorithms. Our main tool is the Maiorana-McFarland class of bent functions which turns out to be
rich enough to prove the two results. First, we show that the classical query complexity for the hidden shift
problem over this class of bent functions is of order Θ(n), while it can be solved with 2 quantum queries.
Theorem 8. Let Of, ef be an oracle that hides a hidden shift s for an instance (f, g, ef) of a hidden shift
problem for a bent function f from Maiorana-McFarland class. Then classically Θ(n) queries are necessary
and sufﬁcient to identify the hidden shift s. Further, there exists a recursively deﬁned oracle Orec which
makes calls to Of, ef and whose quantum query complexity is poly(n), whereas its classical query complexity
is superpolynomial.
Proof. The proof of the lower bound on the classical query complexity for O is information theoretic. The
tightness of the bound follows since n bits of information about s have to be gathered and each query can
yield at most 1 bit. To see that O(n) are indeed sufﬁcient, consider the following (adaptive) strategy for
ﬁnding a shift (s, s′) of g(x, y) = (x + s)π(y + s′): ﬁrst query g(x, y) on (0, 0) to extract sπ(s′). Then
subtract this from the values at the points (ei, 0), where ei denotes the ith standard basis vector. This gives
the bits of π(s′). Next evaluate ef(x, y) = π−1(x)yt at the points (π(s′), ei). This gives the bits of s′.
Finally, from evaluating g at points (0, π−1(ei) + s′) we can obtain the bits of s, i. e., the entire hidden shift
(s, s′).
A standard argument can be invoked [BV97] to recursively construct an oracle which hides a function
computed by a tree, the nodes of which are given by the oracle hiding a string s. In order to evaluate f(x)
at a node, ﬁrst a sequence of smaller instances of the problem have to be solved. We do not go into further
detail of the construction and only note that we get the analogous result as in [BV97], see also [HH08],
namely that a tree of height log n leads to a quantum query complexity of 2log n which is polynomial in n,
whereas the classical query complexity is given by nlog n which grows faster than any polynomial.
The following theorem avoids the adaptive queries in the proof of Theorem 8 and uses oracles of the
form Of in which no queries to the dual bent function are allowed. Since the quantum computer can still
11


---- page 12 ----

determine the shift in polynomial time, here an exponential separation between classical and quantum query
complexity can be shown.
Theorem 9. Let Of be an oracle that hides a hidden shift s for an instance (f, g) of a hidden shift problem
for a bent function f from Maiorana-McFarland class. Then classically Θ(
√
2n) queries are necessary and
sufﬁcient to identify the hidden shift s.
Proof. The proof is similar to the lower bound for the linear structure problem considered in [dBCW02] and
the query lower bound for Simon’s problem [Sim94]. First, note that we can use Yao’s minimax principle
[Yao77] to show limitations of a deterministic algorithm A on the average over an adversarially chosen
distribution of inputs. Hence, we can consider deterministic algorithms and π and s in the deﬁnition of
f(x, y) = xπ(y)t and g(x, y) = f(x, y + s) will be chosen randomly.
The distribution we chose to show the lower is to chose π uniformly at random in S2n, the symmetric
group on the strings of length n, and s = (s1, s2) ∈Z2n
2
such that s1 = 0 and s2 is chosen uniform at
random in Zn
2. The instances we consider are given by oracle access to the functions f(x, y) = xπ(y)t and
g(x, y) = f(x, y + s) = xπ(y + s)t. Now, without loss of generality we can assume that the classical
algorithm A has (adaptively or not) queried the oracle k = nO(1) times, i. e., it has chosen pairs (xi, yi) for
i = 1, . . . , k and obtained results
xiπ(yi)t
=
ai
xiπ(yi + s)t
=
bi.
In order to characterize the information about s after these k queries we deﬁne set D = {xi : i =
1, . . . , k} ∪{yi : i = 1, . . . , k}. We show that if no collision between the values of f and g was produced,
then the information obtained about s is exponentially small. To simplify our argument, we actually make
the classical deterministic algorithm more powerful by giving oracle access to π(x) and π(x + s). Consider
the set of all differences D(−) = {d1 −d2 : d1, d2 ∈D} and the set Dgood = Zn
2 \ D(−). Note that
for an abelian group A and subset D ⊂A with |D|2 < |A| we can always choose a set S such that
D ∩(D + s) = ∅for all s ∈S. Indeed, we can choose S = Dgood since x ∈D ∩(D + s) would imply
that there exist d1, d2 ∈D with d1 = d2 + s, i. e., s ∈D(−) which is a contradiction. Notice in our case
that |S| ≥2n −|D(−)| = 2n −nO(1). Now, we can change the value of the shift s to any other value s′ as
long as the algorithm has not queried s directly (the chances of which are exponentially small: because of
a birthday for the strings s, the probability is given by Θ

1
√
2n

). We do this by choosing π′ in such a way
that it maps π(yi + s) = π′(yi + s′) while being consistent with all other queries. Because of the above
argument, as long as there is no collision, after ℓqueries to f, g, we still have a set S of size |S| ≥2n−nO(1)
of candidates s′, and π′ which are also consistent with the sampled data, showing the lower bound.
Corollary 10. There exists an oracle O implementing a Boolean function such that PO ̸= BQPO.
5
Conclusions
We introduced the hidden shift problem for a class of Boolean functions which are at maximum distance
to all linear functions. For these so-called bent functions the hidden shift problem can be efﬁciently solved
on a quantum computer, provided that we have oracle access to the shifted version of the function as well
as its dual bent function. The quantum computer can extract the hidden shift using just one query to these
two functions and besides this only requires to compute the Hadamard transform and measure qubits in
12


---- page 13 ----

the standard basis. We showed that this task is signiﬁcantly more challenging for a classical computer and
proved an exponential separation between quantum and classical query complexity.
Acknowledgments
The author gratefully acknowledges support by ARO/NSA under grant W911NF-09-1-0569 and would like
thank the anonymous referees for valuable comments on this paper and earlier versions of it.
References
[Aar03]
S. Aaronson. Quantum lower bound for recursive Fourier sampling. Quantum Information and
Computation, 3(2):165–174, 2003.
[AS07]
A. Atici and R. Servedio. Quantum algorithms for learning and testing juntas. Quantum Infor-
mation Processing, 6(5):323–348, 2007.
[BCvD05]
D. Bacon, A. Childs, and W. van Dam. From optimal measurement to efﬁcient quantum algo-
rithms for the hidden subgroup problem over semidirect product groups. In Proceedings of the
46th Annual IEEE Symposium on Foundations of Computer Science, pages 469–478, 2005.
[dBCW02] N. de Beaudrap, R. Cleve, and J. Watrous. Sharp quantum versus classical query complexity
separations. Algorithmica, 34(4):449–461, 2002.
[BJL99]
Th. Beth, D. Jungnickel, and H. Lenz. Design Theory, volume I. Cambridge University Press,
2nd edition, 1999.
[BV97]
E. Bernstein and U. Vazirani.
Quantum complexity theory.
SIAM Journal on Computing,
26(5):1411–1473, 1997. Conference version in Proc. STOC’93, pp. 11–20.
[CG06]
C. Carlet and Ph. Gaborit. Hyper-bent functions and cyclic codes. Journal of Combinatorial
Theory, Ser. A, 113:466–482, 2006.
[CvD07]
A. Childs and W. van Dam. Quantum algorithm for a generalized hidden shift problem. In
Proceedings of the 18th Symposium on Discrete Algorithms (SODA’07), pages 1225–1232,
2007.
[CvD08]
A. Childs and W. van Dam.
Quantum algorithms for algebraic problems.
arXiv Preprint
0812.0380, to appear in Reviews of Modern Physics.
[CSV07]
A. Childs, L. J. Schulman, and U. Vazirani. Quantum algorithms for hidden nonlinear struc-
tures. In Proceedings of the 48th Annual IEEE Symposium on Foundations of Computer Science
(FOCS’07), pages 395–404, 2007.
[CW07]
A. Childs and P. Wocjan. On the quantum hardness of solving isomorphism problems as non-
abelian hidden shift problems. Quantum Information and Computation, 7(5–6):504–521, 2007.
[vDHI03]
W. van Dam, S. Hallgren, and L. Ip. Quantum algorithms for some hidden shift problems. In
Proceedings of the 14th Symposium on Discrete Algorithms (SODA’03), pages 489–498, 2003.
13


---- page 14 ----

[DDW08]
Th. Decker, J. Draisma, and P. Wocjan. Efﬁcient quantum algorithm for identifying hidden
polynomials. Quantum Information and Computation, 2008. To appear, see also arxiv preprint
0706.1219”.
[DJ92]
D. Deutsch and R. Jozsa. Rapid solution of problems by quantum computation. Proceedings
of the Royal Society London, Series A, 439:553–558, 1992.
[Dil75]
J. Dillon. Elementary Hadamard difference sets. In F. (et al.) Hoffman, editor, Proc. 6th S-
E Conf. on Combinatorics, Graph Theory, and Computing, pages 237–249. Winnipeg Utilitas
Math., 1975.
[Dob95]
H. Dobbertin. Construction of bent functions and balanced Boolean functions with high nonlin-
earity. In B. Preneel, editor, Fast Software Encryption, volume 1008 of LNCS, Springer, pages
61–74, 1995.
[FIM+03]
K. Friedl, G. Ivanyos, F. Magniez, M. Santha, and P. Sen. Hidden translation and orbit coset in
quantum computing. In Proc. STOC’03, pages 1–9, 2003.
[Hal02]
S. Hallgren. Polynomial-time quantum algorithms for Pell’s equation and the principal ideal
problem. In Proc. STOC’02, pages 653–658, 2002.
[HH08]
S. Hallgren and A. Harrow. Superpolynomial speedups based on almost any quantum circuit. In
Proceedings of the 35th International Colloquium on Automata, Languages and Programming
(ICALP’08), pages 782–795, 2008.
[HMR+06] S. Hallgren, C. Moore, M. R¨otteler, A. Russell, and P. Sen. Limitations of quantum coset states
for graph isomorphism. In Proceedings of the 38th Annual ACM Symposium on Theory of
Computing (STOC’06), pages 604–617, 2006.
[HZ99]
T. Helleseth and V. Zinoviev. On Z4-linear Goethals codes and Kloosterman sums. Designs,
Codes and Cryptography, 17:269–288, 1999.
[Kit97]
A. Yu. Kitaev. Quantum computations: algorithms and error correction. Russian Math. Surveys,
52(6):1191–1249, 1997.
[KS07]
A. R. Klivans and A. A. Sherstov. Unconditional lower bounds for learning intersections of
halfspaces. Machine Learning, 69(2–3):97–114, 2007.
[Kup05]
G. Kuperberg. A subexponential-time quantum algorithm for the dihedral hidden subgroup
problem. SIAM Journal on Computing, 35(1):170–188, 2005.
[LW90]
G. Lachaud and J. Wolfmann. The weights of the orthogonals of the extended quadratic binary
Goppa codes. IEEE Transactions on Information Theory, 36(3):686–692, 1990.
[Man94]
Y Mansour. Learning Boolean functions via the Fourier transform. In V. P. Roychodhury, K.-
Y. Siu, and A. Orlitsky, eds., Theoretical Advances in Neural Computation and Learning, pp.
391–424. Kluwer, 1994.
[LMS08]
S. Lovett, R. Meshulam, and A. Samorodnitsky. Inverse conjecture for the Gowers norm is
false. In Proceedings of the 40th Annual ACM Symposium on Theory of Computing (STOC’08),
pages 547–556, 2008.
14


---- page 15 ----

[MS77]
F. J. MacWilliams and N. J. A. Sloane. The Theory of Error–Correcting Codes. North–Holland,
Amsterdam, 1977.
[Mon09]
A. Montanaro. Quantum algorithms for shifted subset problems. Quantum Information and
Computation, 9(5&6):500–512, 2009.
[MRRS07] C. Moore, D. N. Rockmore, A. Russell, and L. J. Schulman. The power of strong Fourier sam-
pling: quantum algorithms for afﬁne groups and hidden shifts. SIAM Journal on Computing,
37(3):938–958, 2007.
[NC00]
M. Nielsen and I. Chuang. Quantum Computation and Quantum Information.
Cambridge
University Press, 2000.
[Rot76]
O. S. Rothaus. On “bent” functions. Journal of Combinatorial Theory, Series A, 20:300–305,
1976.
[RS04]
A. Russell and I. Shparlinski.
Classical and quantum function reconstruction via character
evaluation. Journal of Complexity, 20(2–3):404–422, 2004.
[Sho97]
P. Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quan-
tum computer. SIAM Journal on Computing, 26(5):1484–1509, 1997.
[Sim94]
D. R. Simon. On the power of quantum computation.
In Proceedings of the 35th Annual
Symposium on Foundations of Computer Science (FOCS’94), pages 116–123, 1994.
[dW08]
R. de Wolf. A brief introduction to Fourier analysis on the Boolean cube. Theory of Computing
Library–Graduate Surveys, 1:1–20, 2008. Available online from www.theoryofcomputing.org.
[Yao77]
A. Yao. Probabilistic computations: toward a uniﬁed measure of complexity. In Proceedings of
the 18th Annual Symposium on Foundations of Computer Science (FOCS’77), pages 222–227,
1977.
15
