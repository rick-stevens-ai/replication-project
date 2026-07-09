<!-- PROVENANCE NOTE
Marker not installed on host CherryRd at time of this replication (2026-07-05).
No cached Marker parse of arXiv:quant-ph/0301141 existed in central corpus.
This file is a FALLBACK extraction via `pdftotext -layout paper.pdf`
(poppler), lightly reflowed to Markdown.  Structural fidelity (tables, math)
is inferior to a true Marker parse; re-run Marker later and overwrite.
Tool: poppler pdftotext  |  Fallback: yes  |  Real Marker run: no
-->

                                        Shor’s discrete logarithm quantum algorithm for
                                                          elliptic curves




arXiv:quant-ph/0301141v2 22 Jan 2004
                                                          John Proos         and      Christof Zalka

                                                  Department of Combinatorics and Optimization
                                                    University of Waterloo, Waterloo, Ontario
                                                                Canada N2L 3G1
                                                     e-mail: japroos@math.uwaterloo.ca         zalka@iqc.ca

                                                                     November 26, 2024

                                                                            Abstract
                                                We show in some detail how to implement Shor’s efficient quantum
                                            algorithm for discrete logarithms for the particular case of elliptic curve
                                            groups. It turns out that for this problem a smaller quantum computer
                                            can solve problems further beyond current computing than for integer
                                            factorisation. A 160 bit elliptic curve cryptographic key could be broken
                                            on a quantum computer using around 1000 qubits while factoring the
                                            security-wise equivalent 1024 bit RSA modulus would require about 2000
                                            qubits. In this paper we only consider elliptic curves over GF(p) and not
                                            yet the equally important ones over GF(2n ) or other finite fields. The main
                                            technical difficulty is to implement Euclid’s gcd algorithm to compute
                                            multiplicative inverses modulo p. As the runtime of Euclid’s algorithm
                                            depends on the input, one difficulty encountered is the “quantum halting
                                            problem”.


                                       Contents
                                       1 Introduction                                                                      2

                                       2 Review of the quantum algorithm for discrete logarithms                           4
                                         2.1 The discrete logarithm problem (DLP) . . . . . . . . . . . . . . .            4
                                             2.1.1 Examples (ZN and Z∗p ) . . . . . . . . . . . . . . . . . . .            4
                                             2.1.2 Discrete logarithms over elliptic curves . . . . . . . . . . .          5
                                         2.2 Shor’s quantum algorithms . . . . . . . . . . . . . . . . . . . . .           5
                                             2.2.1 The order finding algorithm (factoring) . . . . . . . . . .             5
                                             2.2.2 Assumption for discrete log: order is prime (and known) .               6
                                             2.2.3 The discrete logarithm algorithm . . . . . . . . . . . . . .            6
                                             2.2.4 Using a Fourier transform of order 2n instead of q . . . .              7

                                                                                 1
3 Elliptic curves                                                                 8
  3.1 Representing points on an elliptic curve . . . . . . . . . . . . . .        9

4 Our implementation of the quantum algorithm for discrete log-
  arithms over elliptic curves                                               9
  4.1 Input registers can be eliminated . . . . . . . . . . . . . . . . . . 10
  4.2 Simplifying the addition rule . . . . . . . . . . . . . . . . . . . . 11
  4.3 Decomposition of the group shift . . . . . . . . . . . . . . . . . . 11
       4.3.1 Divisions of the form x, y ↔ x, y/x . . . . . . . . . . . . . 12
       4.3.2 Modular multiplication of two “quantum” numbers . . . . 12

5 The Extended Euclidean Algorithm                                             13
  5.1 Stepwise reversibility . . . . . . . . . . . . . . . . . . . . . . . . . 15
  5.2 Simple implementations with time O(n3 ) and O(n2 log2 n) . . . . 15
      5.2.1 Using bounded divisions . . . . . . . . . . . . . . . . . . . 16
  5.3 Our proposed implementation . . . . . . . . . . . . . . . . . . . . 16
      5.3.1 Desynchronising the parallel computations . . . . . . . . . 17
      5.3.2 Applying this to the extended Euclidean algorithm . . . . 17
      5.3.3 How many steps are necessary? . . . . . . . . . . . . . . . 19
      5.3.4 The quantum halting problem: a little bit of garbage . . . 19
      5.3.5 Saving space: Bounded divisions and register sharing . . . 20
  5.4 Analysis of the Euclidean algorithm implementation . . . . . . . 21
      5.4.1 Running time: O(n2 ) . . . . . . . . . . . . . . . . . . . . 21
      5.4.2 Space: O(n) . . . . . . . . . . . . . . . . . . . . . . . . . . 22
      5.4.3 Possible improvements and alternative approaches . . . . 22

6 Results and a comparison with factoring                                  24
  6.1 Total time for the DLP algorithm . . . . . . . . . . . . . . . . . . 24
  6.2 Total number of qubits (roughly 6n) . . . . . . . . . . . . . . . . 25
  6.3 Comparison with the quantum factoring algorithm . . . . . . . . 26

A Appendix: Detailed analysis of the success probability                    27
  A.1 Order finding algorithm (basis of factoring) . . . . . . . . . . . . 27
  A.2 Discrete logarithm case . . . . . . . . . . . . . . . . . . . . . . . 29

B Appendix: Bounding the number of cycles                                        30


1    Introduction
In 1994 Peter Shor presented two efficient quantum algorithms [1] for compu-
tational problems for which no polynomial time classical algorithms are known.
One problem is to decompose a (large) integer into its prime factors. The
other problem, which we consider here, is finding discrete logarithms over finite
groups. The classical complexity of this problem seems to depend strongly on
the underlying group. A case for which (known) classical algorithms are par-
ticularly inefficient are elliptic curve groups defined over finite fields. Actually


                                         2
most public key cryptography in use today relies either on the presumed hard-
ness of integer factoring (RSA) or that of discrete logarithms over finite fields
or elliptic curves.
    Elliptic curve cryptography (ECC) is sometimes preferred because it allows
shorter key sizes than RSA. This is because the best classical integer factoring
algorithms (the number field sieve, see e.g. [2]), although superpolynomial, have
                                                                             1/3
less than exponential complexities. Very roughly the complexity is O(ec log n ),
where n is the integer to be factored. On the other hand, for discrete logarithms
over elliptic curves, nothing better than “generic” algorithms are known, thus
algorithms which work for any group. These algorithms, e.g. the Pollard ρ
algorithm [3], have truly exponential complexity.
    Shor’s quantum algorithms for integer factoring and discrete logarithms have
about equal complexity, namely typically O(n3 ). Thus there is a larger complex-
ity gap between classical and quantum for discrete logarithms than for factoring.
    Proposals have been made [4, 5] for optimised implementations of the quan-
tum factoring algorithm, in particular for minimising the number of qubits
needed. The best current result by S.Beauregard [4] is that about 2n qubits
are enough. We attempt here a similar optimisation for discrete logarithms
over elliptic curves. The implementation is more difficult, but we still get an
algorithm that uses less qubits and time to solve a problem of similar classical
difficulty when compared to factoring. For problems that can now barely be
solved, the number of qubits is not much less than for factoring, but in the
future, with more powerful classical computers, the gap will increase.
    Elliptic curves used in cryptography [6, 7, 8] are defined either over the field
of arithmetic modulo a prime, thus GF (p), or over GF (2n ). For our implemen-
tation we need to do arithmetic operations in these fields, in particular we must
compute multiplicative inverses. For GF (p), this is done with Euclid’s algo-
rithm for computing the greatest common divisor (gcd), or rather the extended
version of this algorithm. This algorithm can be adapted to the case of any
finite field GF (pn ), but for n > 1 there is the added concern of deciding how
the elements of the field will be represented. So in this paper we only consider
elliptic curves over GF (p).
    Still, the implementation of the extended Euclidean algorithm is the main
technical difficulty we encounter. Fortunately, the algorithm can be made piece-
wise reversible, so that not too much “garbage” has to be accumulated. As for
the factoring algorithm, it is possible to run the whole algorithm with O(n)
qubits. For our implementation of Euclid’s algorithm to achieve the classical
time complexity of O(n2 ), it is necessary to terminate the steps in the algo-
rithm at different points, depending on the input. This is difficult to achieve
with acyclic circuits (which are necessary for computations in “quantum par-
allelism”). We will relegate some of the more cumbersome technical aspects of
our solution to an appendix, and will also discuss possible other approaches.
    In trying to optimise our implementation, we were guided by practical con-
siderations, although to do this, one would really have to know how an actual
quantum computer will look. We put most emphasis on minimising the number



                                         3
of qubits, but also on the total number of gates. We assume that whatever can
be computed classically, should be done classically as long as it doesn’t take
an unreasonable amount of computation. Basically we are trying to optimise a
quantum circuit where a gate can act on any pair of qubits, but it turns out
that most gates are between neighbours like in a cellular automaton. In con-
trast to the earlier papers [4, 5] optimising the quantum factoring algorithm,
we have not thought about parallelising the algorithm, although this may well
be of interest for actual implementations.


2       Review of the quantum algorithm for discrete
        logarithms
2.1     The discrete logarithm problem (DLP)
Let G be a finite cyclic group and let α be a generator of G. The discrete
logarithm problem over G to the base α is defined as given an element β ∈ G
determine the unique d ∈ [0, |G| − 1] such that αd = β. The integer d is denoted
by logα β. Note that while G may be a subgroup of a non-abelian group, G
being cyclic is always an abelian group. Usually it is assumed that the order of
G is known.
    There are two general types of algorithms for solving DLPs. The first type,
called generic algorithms, work for any group, as long as we have a (unique)
representation of group elements and we know how to carry out the group
operation. The best known classical generic algorithms have complexity equal
to about the square root of the order of the group. Thus they are exponential
in the number of bits necessary to describe the problem.
    The second type of algorithms are the algorithms which rely on specific
properties of the group or its representation. As shown in the examples be-
low, some groups have group specific algorithms which can solve the DLP in
subexponential or even polynomial time.

2.1.1    Examples (ZN and Z∗p )
Let N be a positive integer and consider the case when G = ZN the additive
group of integers modulo N . Here the generators of the group are precisely the
α ∈ G such that gcd(α, N ) = 1 and the equation d · α ≡ β (mod N ) can be
solved by finding the multiplicative inverse of α modulo N with the extended
Euclidean algorithm. Thus for this group the DLP can be solved in polynomial
time (O(log2 2 N )).
    There are however groups for which the DLP is not so easy. Suppose that
G = Z∗p the multiplicative group modulo p, which is cyclic, and that α is a
generator of G. Then the DLP is equivalent to solving the equation αd ≡ β
(mod p). There are no known classical algorithms which can solve this problem
in polynomial time. Still, like for integer factoring, the best algorithms have a
subexponential complexity.


                                       4
   Note that if G is a finite cyclic group of order N then G is isomorphic to
ZN in which the DLP is easy. Thus it is not the structure of a group, but its
representation, which can make its DLP difficult.

2.1.2   Discrete logarithms over elliptic curves
Elliptic curves over GF (pn ) are finite abelian groups. Given a point α on an
elliptic curve we can consider the difficulty of solving the DLP in the cyclic
subgroup generated by α. For general elliptic curves (trace not equal to zero or
one) the DLP seems to be computationally quite hard. In particular for these
curves it is not known how to exploit the representation of the group to help
solve the DLP. Thus the best known classical algorithms for the DLP on these
elliptic curves are the generic algorithms whose running times are exponential in
the number of bits necessary to describe the problem. This presumed classical
hardness makes the groups useful for cryptography and has led to systems based
on these group being included in ANSI, IEEE and FIPS standards [6, 7, 8].

2.2     Shor’s quantum algorithms
Both of Shor’s algorithms have later been understood as special cases of a more
general framework, namely the abelian hidden subgroup problem (see e.g. [9, 10,
11]). While in the factoring algorithm we are looking at subgroups of the group
of integers, Z, in the discrete logarithm case, subgroups of Z2 play a role. In
particular we are looking at sublattices of the lattice Z2 , thus elements which can
be written as integer linear combinations of two (linearly independent) vectors
in Z2 . Thus in a way the discrete logarithm algorithm can be viewed as a 2
dimensional version of the factoring algorithm.

2.2.1   The order finding algorithm (factoring)
The basis of the integer factoring algorithm is really an order finding algorithm,
which we briefly review here. We are given an element α in a (finite) group G and
want to find its order. That is, the smallest non-negative integer r with αr = e,
where e is the neutral element. To do this, we prepare a (large) superposition of
N “computational” basis states |xi and compute αx in “quantum parallelism”:
                          N −1                          N −1
                      1 X                          1 X
                     √      |xi              →    √      |x, αx i
                      N x=0                        N x=0

Where N is much larger than any order r that we expect. Now imagine that
we measure the second register and get αx0 (the measurement is not actually
necessary). Then the first register will be left in a superposition of the form
                                      ≈N/r
                                      X
                                 c·          |x0 + k · ri
                                      k=0




                                             5
where x0 is a random number between 0 and r − 1. Now a quantum Fourier
transform (of size N ) will leave this register in a superposition dominated by
basis states that are close to multiples of N/r. Thus a measurement will yield
such a state with high probability. If N is chosen larger than the square of any
expected order r, it is possible to calculate r from the observed state with high
probability. Also N is chosen to be a power of 2, as this gives the simplest
“quantum fast Fourier transform” (QFFT).

2.2.2   Assumption for discrete log: order is prime (and known)
First let us justify a simplifying assumption that we make. We assume that the
order of the base α of the elliptic curve discrete logarithm is prime and that we
know this prime. This is true for the cases standardised for cryptographic use
[6, 7, 8]. Also, if we don’t know the order of α, we can find it with the above
order finding algorithm and also decompose it into its prime factors with the
integer factoring algorithm. Then there is a standard way to reduce the DLP
in a group with composite order, N , into several DLPs with orders equal to the
prime factors of N (see [12]). Thus our simplifying assumption is really without
loss of generality.

2.2.3   The discrete logarithm algorithm
So we have αq = e, with q prime and β = αd where d is unknown and between
0 and q − 1. Consider the function f (x, y) = αx β y for integers x and y. This
function has two independent “periods” in the plane Z2 , namely
          f (x + q, y) = f (x, y)    and       f (x + d, y − 1) = f (x, y)
Thus all x, y with f (x, y) = e define a sublattice of Z2 . The 2 dimensional
Fourier transform then leads to the dual lattice from which d can be determined.
Note that f (x, y) can be thought of as being defined over Zq 2 as f (x, y) =
f (x mod q, y mod q).
    For didactic purposes let us first imagine that we knew a way to carry out
the quantum fast Fourier transform of order q (QFFTq ) , as then the algorithm
would be particularly nice. (Actually it has been shown how to do this approx-
imatively [11, 13], but we won’t use these constructions.) Then we start with
the following state of two quantum registers, and compute αx β y in “quantum
parallelism”:
                   q−1 q−1                     q−1 q−1
                 1 XX                        1 XX
                           |x, yi    →                 |x, y, αx β y i
                 q x=0 y=0                   q x=0 y=0

Again, imagine that we now measure the last register (although this is again not
necessary). Then we will obtain a random element αx0 of the group generated
by α, where x0 is between 0 and q − 1. We will then find the first two registers
in a superposition of all x, y with
                             αx β y = αx (αd )y = αx0

                                         6
Because the order of α is q, this is equivalent to

                             x + dy ≡ x0             (mod q)

Or equivalently x = (x0 − dy) mod q. Thus for each y there is exactly one
solution, and so the state of the first two registers is:
                                       q−1
                                 1 X
                                 √      |x0 − dy, yi
                                  q y=0

Now we Fourier transform each of the two registers with our (hypothetical)
quantum Fourier transform of order q, which acts on basis states as
                                 q−1
                            1 X zz′ ′
              |zi     →     √    ωq |z i                where ωq = e2πi/q
                             q ′
                                 z =0

We obtain
                           q−1         q−1
                      1 1 X            X                 ′     ′
                      √                      ωq(x0 −dy)x ωqyy |x′ , y ′ i
                       qq ′ ′
                            x ,y =0 y=0
                                                                   ′
The sum over y is easy to calculate. It gives qωqx0 x if y ′ ≡ dx′ (mod q) and
vanishes otherwise. Thus we get:
                              q−1
                          1 X x0 x′ ′ ′
                          √    ωq |x , y = dx′ mod qi
                           q ′
                             x =0

We now see that the probability of measuring a basis state is independent of x0 ,
thus it doesn’t matter which x0 we measured above. By measuring, we obtain
a pair x′ , y ′ from which we can calculate d = y ′ (x′ )−1 mod q as long as x′ 6= 0.
(The only disadvantage of allowing the order q not to be a prime, would be that
we would require gcd(x′ , q) = 1.)

2.2.4   Using a Fourier transform of order 2n instead of q
In practise we will want to replace each of the two QFFTq ’s with a quantum
fast Fourier transform of order 2n (QFFT2n ), because this is easy to implement.
For the QFFTq above we will always obtain a pair x′ , y ′ with y ′ ≡ dx′ mod q in
the final measurement. However, for the QFFT2n we will get a high probability
of measuring a pair x′ , y ′ if

                    (x′ q/2n , y ′ q/2n ) ≈ (k, dk)          for some k

For 2n ≈ q we have a good (constant) probability of getting the right values in
Zq 2 by rounding. In appendix A we make this analysis in detail and show that
by investing a reasonable amount of classical post-processing we can with prob-
ability close to 1 obtain the discrete logarithm with a single run of the quantum


                                              7
algorithm. (Of course this is on a perfect, noise free, quantum computer...)
More classical post-processing increases the chances of success because now we
can try out several values in the vicinity of the values x′ , y ′ which we measured.
Also there is a tradeoff between n, thus the number of qubits, and the success
probability. For n increasing beyond log2 q the probability of failure decreases
exponentially.


3     Elliptic curves
As mentioned earlier, elliptic curves over finite fields form abelian groups. We
will now present a brief introduction to elliptic curves over fields of characteristic
not equal to 2 or 3 (i.e. 1 + 1 6= 0 and 1 + 1 + 1 6= 0). For a more in depth
introduction to elliptic curves and their use in cryptography see [14, 15, 16].
    Let K be a field of characteristic not equal to 2 or 3. An elliptic curve over
K is the set of solutions (x, y) ∈ K × K to the equation

                                E : y 2 = x3 + ax + b                              (1)

where a, b ∈ K are constants such that 4a3 + 27b2 6= 0, together with the point
at infinity, which is denoted O. The solutions to equation 1 are called the finite
points on the curve and together with O are called the points on the curve. We
will use E to denote the set of points on an elliptic curve.
    The group operation on the points is written additively and is defined as
follows. If P ∈ E then P + O = O + P = P. If P = (x1 , y1 ), R = (x2 , y2 ) ∈ E
then
                             (
                               O          if (x2 , y2 ) = (x1 , −y1 ),
                   P +R=                                                       (2)
                               (x3 , y3 ) otherwise,

where x3 = λ2 − (x1 + x2 ), y3 = λ(x1 − x3 ) − y1 ,
                         (
                           (y2 − y1 )/(x2 − x1 ) if P 6= R
                    λ=
                           (3x21 + a)/(2y1 )       if P = R

and all operations are performed over the field K.
    It is not hard to check that if (x1 , y1 ) and (x2 , y2 ) are on the curve, then so
is (x3 , y3 ) and thus the above operation is closed on E. While not immediately
clear, the points on the curve together with the above operation form an abelian
group (For a proof see [14]). It is clear from the definition of the group operation
that O is the identity element. If P = (x, y) ∈ E it following directly from
equation 1 that R = (x, −y) is also a point on the curve. Thus if P = (x, y)
then the inverse of P is (x, −y). Note that the elliptic curve group operation is
defined differently over fields of characteristic 2 or 3.
    A famous theorem by Hasse states that if E is an elliptic curve defined over
                                                                                   √
GF (p) then the number of points on E, denoted #E, is p+1−t where |t| ≤ 2 p.


                                          8
This implies that the maximum bit size of the order of a point is approximately
the bit size of p.
   A particular elliptic curve, E, is specified by giving the base field, K, and
the constants a, b ∈ K from equation 1. For our purposes the base field K will
always be GF (p) for some prime p > 3. In practice a and b are selected such
that the order of the group contains a large prime factor, q, as this is necessary
to make the discrete logarithm problem hard. For simplicity we shall assume
that p and q are approximately the same bit size.

3.1    Representing points on an elliptic curve
Suppose we are given an elliptic curve, E : y 2 = x3 + ax+ b, over the field GF (p)
for some prime p > 3. In order for a quantum computer to calculate discrete
logarithms over E we like to have a unique representation of the points on E.
    If P is a finite point on E then P = (x, y), where x and y are integers
modulo p. Thus any finite point can be represented by a unique ordered pair
(x, y) with x, y ∈ {0, 1, . . . , p − 1}. Now all that remains is to determine how
O will be represented. As will be discussed in section 4.2, our implementation
we will not actually require a representation of O. However, if a representation
was required we could simply pick an ordered pair (x, y) which is not on the
curve. For example, (p, p) could be used to represent O for any curve, while
(0, 0) could be used for any curve with b 6= 0.


4     Our implementation of the quantum algorithm
      for discrete logarithms over elliptic curves
We consider an elliptic curve, E, over GF (p), where p is a large prime. The
base of the logarithm is a point P ∈ E whose order is another (large) prime
q, thus qP = O. We want to compute the discrete logarithm, d, of another
point Q ∈ E, thus Q = dP . (Remember that we use additive notation for the
group operation, thus instead of a power of the base element, we have an integer
multiple.)
    As discussed in section 2.2.3, we need to apply the following transformation
                n    n                        n    n
               2 −1 2 −1                     2 −1 2 −1
             1 X X                         1 X X
                         |x, yi     →                  |x, y, xP + yQi
            2n x=0 y=0                    2n x=0 y=0

Thus we need a method of computing (large) integer multiples of group elements.
This can be done by the standard “double and add technique”. This is the
same technique used for the modular exponentiation in the factoring algorithm,
although there the group is written multiplicatively so it’s called the square and
multiply technique. To compute xP + yQ, first we repeatedly double the group
elements P and Q, thus getting the multiples Pi = 2i P and Qi = 2i Q. We then
add together the Pi and Qi for which the corresponding bits of x and y are 1,


                                        9
thus
                                     X                X
                         xP + yQ =          xi Pi +       yi Qi
                                       i              i
           P              P
where x = i xi 2i , y = i yi 2i , Pi = 2i P and Qi = 2i Q. The multiples Pi
and Qi can fortunately be precomputedP classically. Then to perform the above
transformation, start with the state x,y |x, y, Oi. The third register is called
the “accumulator” register and is initialised with the neutral element O. Then
we add the Pi and Qi to this register, conditioned on the corresponding bits of
x and y.

4.1    Input registers can be eliminated
Here we show that the input registers, |x, yi, can actually be shrunk to a single
qubit, thus saving much space. This is accomplished by using the semiclassi-
cal quantum Fourier transform and is completely analogous to what has been
proposed for the factoring algorithm [17] (see also e.g. [4, 5]).
    Griffiths and Niu [18] have observed that the QFFT followed by a mea-
surement can be simplified. Actually it can be described as simply measuring
each qubit in an appropriate basis, whereby the basis depends on the previous
measurement results. (In accordance with quantum computing orthodoxy, we
can also say that before measuring the qubit in the standard basis, we apply
a unitary transformation which depends on the previous measurement results.)
                                    P2n −1,2n −1
Note that in the initial state 21n x=0,y=0 |x, y, Oi the qubits in the x- and
                                                                               √
y-registers are actually unentangled. Each qubits is in the state (|0i + |1i)/ 2.
Now we can see how these two registers can be eliminated: We√do n steps. In
step number i we first prepare a qubit in the state (|0i + |1i)/ 2, then use it
to control the addition of Pi (or Qi ) and finally we measure the control qubit
according to the semiclassical QFFT. In this QFFT the qubits have to be mea-
sured in reversed order, thus from highest significance to lowest. Thus we will
need to proceed from the i = n − 1 step down to the i = 0 step, but this is no
problem.
    In summary, we really only need the accumulator register. We are left being
required to carry out a number of steps whereby we add a fixed (classically
known) point Pi (or Qi ) to a superposition of points. We are working in the
cyclic group generated by P , thus the effect of a fixed addition is to “shift” the
discrete logarithm of each element in the superposition by the same amount.
For this reason we shall refer to these additions of fixed classical points as
“group shifts”. (That the group shifts are conditional on a qubit makes it only
insignificantly more difficult, as we will point out later.) Thus we need unitary
transformations UPi and UQi which acts on any basis state |Si representing a
point on the elliptic curve, as:
         UPi :   |Si → |S + Pi i       and       UQi :       |Si → |S + Qi i
As explained in section 2.2.3 and appendix A, it is sufficient to do n of these
steps for P and n for Q, thus a total of 2n, where n ≈ log2 q.

                                           10
4.2    Simplifying the addition rule
So we have already managed to decompose the discrete logarithm quantum
algorithm into a sequence of group shifts by constant classically known elements.
That is
               UA : |Si → |S + Ai       S, A ∈ E and A is fixed
We propose to only use the addition formula for the “generic” case (i.e. for
P + R where P, R 6= O and P 6= ±R) for the group operation, although it
wouldn’t be very costly to properly distinguish the various cases. Still, it’s not
necessary. First note that the constant group shifts 2i P and 2i Q are not equal
to the neutral element O, because P and Q have order a large prime. (If a group
shift was O, we would of course simply do nothing.) Still, we are left with three
problems. First, that a basis state in the superposition may be the inverse of
the group shift. Second, that a basis state in the superposition may equal the
group shift. Lastly, that a basis state in the superposition may be O. We argue
that with a small modification these will only happen to a small fraction of the
superposition and thus the fidelity lost is negligible.
    To ensure a uniformly small fidelity loss, we propose the following modifica-
tion at the beginning of the DLP algorithm: choose (uniformly) at random an
element k · P 6= O in the group generated by P . Then we initialise the accu-
mulator register in the state |k · P i, instead of |Oi. This overall group shift is
irrelevant, as after the final QFFT it only affects the phases of the basis states.
Now on average in each group shift step we “loose” only a fraction of 1/q of the
superposition by not properly adding inverses of points and an equal amount
for not correctly doubling points. Thus the total expected loss of fidelity from
this error during the 2n group shifts is 4n/q ≈ 4 log2 q/q and is thus an expo-
nentially small amount. As the accumulator no longer begins in the state |Oi,
the superposition |Si to which UA will be applied can only contain |Oi if an
inverse was (correctly) added in the previous addition. Thus O being a basis
state in the superposition will not cause any further loss of fidelity.

4.3    Decomposition of the group shift
The group shift is clearly reversible. A standard procedure might be to do
|S, 0i → |S, S + Ai → |0, S + Ai where in the last step we would uncompute
S by running the addition of −A to S + A backwards. Fortunately we can do
better than this generic technique. In terms of the coordinates of the points,
the group shift is:

          |Si = |(x, y)i   →     |S + Ai = |(x, y) + (α, β)i = |(x′ , y ′ )i

Recall that x = α if and only if (x, y) = ±A and that this portion of the
superposition can be lost (see section 4.2). Thus we use the following group
operation formulas (see eq. 2):

                       y−β   y′ + β
                  λ=       =− ′                x′ = λ2 − (x + α)
                       x−α   x −α

                                        11
The second expression for λ is not difficult to obtain. It will allow us to later
uncompute λ in terms of x′ , y ′ . Actually, when computing λ from x, y we can
directly uncompute y, and similarly we can get y ′ when uncomputing λ:

                    x, y    ↔   x, λ   ↔      x′ , λ   ↔     x′ , y ′

Where a double-sided arrow (↔) indicates that we need to do these operations
reversibly, thus in each step we need also to know how to go backward. Note
that the decomposition of one large reversible step into several smaller individ-
ually reversible ones, is nice because it saves space, as any “garbage” can be
uncomputed in each small step. In more detail the sequence of operations is:
                                         y−β
 x, y ↔ x − α, y − β       ↔ x − α, λ =        ↔                          (3)
                                        x−α
                                          y′ + β
                           ↔ x′ − α, λ = − ′     ↔ x′ − α, y ′ + β ↔ x′ , y ′
                                          x −α
where all the operations are done over GF (p). The second line is essentially
doing the operations of the first line in reverse. The first and last steps are just
modular additions of the constants ±α, −β. They clearly need much less time
(and also less qubits) than the multiplications and divisions (see [19]), so we will
ignore them when calculating the running times. The operation in the middle
essentially involves adding the square of λ to the first register. This operation,
too, is relatively harmless. It uses less “work” qubits than other operations and
thus doesn’t determine the total number of qubits needed for the algorithm.
Still, for time complexity we have to count it as a modular multiplication (more
about this below). So a group shift requires two divisions, a multiplication and
a few additions/subtractions.

4.3.1   Divisions of the form x, y ↔ x, y/x
The remaining two operations are a division and multiplication where one of the
operands is uncomputed in the process. The division is of the form x, y ↔ x, y/x,
where x 6= 0. (different x and y than the last section!). The multiplication in
(3) is simply the division run in the reverse direction. We further decompose
the division into four reversible steps:
            E               m                   E                       m
     x, y   ↔    1/x, y     ↔   1/x, y, y/x     ↔      x, y, y/x        ↔   x, 0, y/x

Where the letters over the arrows are m for “multiplication” and E for “Euclid’s
algorithm” for computing the multiplicative inverse modulo p. The second m is
really a multiplication run backwards to uncompute y.

4.3.2   Modular multiplication of two “quantum” numbers
Before concentrating on Euclid’s algorithm, let’s look at the modular multipli-
cations of the form x, y ↔ x, y, x · y. In the quantum factoring algorithm the
modular exponentiation is decomposed into modular multiplications. But there

                                        12
one factor is a fixed “classical” number. Still, the situation when we want to
act on superpositions of both factors, is not much worse. So we want to do
(explicitly writing mod p for clarity):

                            |x, yi    →    |x, y, x · y mod pi

We now decompose this into a sequence of modular additions and modular
doublings:
              n−1
              X
      x·y =         xi 2i y = x0 y + 2(x1 y + 2(x2 y + 2(x3 y + . . . )))   (mod p)
              i=0

So we do a series of the following operations on the third register:

          A    ↔       2A     ↔      2A + xi y   (mod p)         i = n − 1...0

Modular doubling
The modular doubling is a standard doubling (a left shift by one bit) followed by
a reduction mod p. Thereby we either subtract p or don’t do anything. Whether
we subtract p has to be controlled by a control qubit. At the end this control
qubit can be uncomputed simply by checking whether 2A mod p is even or odd
(because p is odd). For the addition or subtraction of a fixed number like p we
need n carry qubits, which have to be uncomputed by essentially running the
addition backwards (but not undoing everything!). To do the reduction mod p
we will now in any case subtract p, check whether the result is negative, and
depending on that, either only uncompute the carry bits or undo the whole
subtraction. In the end the operation is only slightly more complicated than
the addition of a fixed number.

Modular addition
The second step is a modular addition of the form |x, yi → |x, x + y mod pi.
Again we first make a regular addition. This is only slightly more complicated
than the addition of a fixed number (see e.g. [5] pp. 7,8). Then, again, we
either subtract p or not. To later uncompute the control bit which controlled
this, we have to compare x and x + y mod p, which essentially amounts to
another addition. Thus overall we have two additions.
    So all together for the modular multiplication we have to do n steps, each
roughly consisting of 3 additions. So one multiplication involves some 3n addi-
tions.


5    The Extended Euclidean Algorithm
Suppose A and B are two positive integers. The well known Euclidean algo-
rithm can be used to find the greatest common divisor of A and B, denoted


                                            13
gcd(A, B). The basis of the algorithm is the simple fact that if q is any integer
then gcd(A, B) = gcd(A, B − qA). This implies the gcd doesn’t change if we
subtract a multiple of the smaller number from the larger number. Thus the
larger number can be replaced by its value modulo the smaller number without
affecting the gcd. Given A and B with A ≥ B this replacement can be accom-
plished by calculating q = ⌊A/B⌋ and replacing A by A − qB, where ⌊x⌋ is
the largest integer less than or equal to x. The standard Euclidean algorithm
repeats this replacement until one of the two numbers becomes zero at which
point the other number is gcd(A, B). The table below illustrates the Euclidean
algorithm.
                 gcd(A, B)                                   gcd(1085, 378)
          integers                 quotient          integers         quotient
           (A, B)              q = ⌊A/B⌋           (1085, 378) 2 = ⌊1085/378⌋
                                         B
        (A − qB, B)            q ′ = ⌊ A−qB ⌋       (329, 378) 1 = ⌊378/329⌋
 (A − qB, B − q ′ (A − qB))      ′′
                               q = ...               (329, 49)     6 = ⌊329/49⌋
              ·                ·                      (35, 49)     1 = ⌊49/35⌋
              ·                ·                      (35, 14)     2 = ⌊35/14⌋
              ·                ·                       (7, 14)     2 = ⌊14/7⌋
       (gcd(A, B), 0)                                   (7, 0)
It can be shown that the Euclidean algorithm will involve O(n) iterations (mod-
ular reduction steps) and has a running time of O(n2 ) bit operations, where n
is the bit size of A and B (see [20]).
      Again suppose that A and B are two positive integers. The extended Eu-
clidean algorithm can be used not only to find gcd(A, B) but also integers k
and k ′ such that kA + k ′ B = gcd(A, B). This follows from the fact that after
each iteration of the Euclidean algorithm the two integers are known integer
linear combinations of the previous two integers. This implies that the integers
are always integer linear combinations of A and B. The extended Euclidean
algorithm simply records the integer linear combinations of A and B which
yield the current pair of integers. Thus when the algorithm terminates with
(gcd(A, B), 0) or (0, gcd(A, B)) we will have an integer linear combination of A
and B which equals gcd(A, B).
      Let us now turn our attention to finding x−1 (mod p), for x 6= 0. If the
extended Euclidean algorithm is used to find integers k and k ′ such that kx +
k ′ p = 1 then k ≡ x−1 (mod p). Note that we are not interested in the coefficient
k ′ of p in the integer linear combination. Thus we need only record the coefficient
of x (and not p) in the extended Euclidean algorithm.
      Hence to compute x−1 (mod p) we will maintain two ordered pairs (a, A)
and (b, B), where A and B are as in the Euclidean algorithm and a and b record
the coefficients of x in the integer linear combinations. We shall refer to these
ordered pairs as Euclidean pairs. (Note that A and B will equal ax (mod p) and
bx (mod p)). We begin the algorithm with (a, A) = (0, p) and (b, B) = (1, x).
In each iteration we replace either (a, A) or (b, B). If A ≥ B then we replace
(a, A) with (a − qb, A − qB), where q = ⌊A/B⌋. Otherwise (b, B) is replaced


                                        14
with (b − qa, B − qA), where q = ⌊B/A⌋. The algorithm terminates when one of
the pairs is (±p, 0), in which case the other pair will be (x−1 , 1) or (x−1 − p, 1).
We illustrate the algorithm in the following table.
              x−1 mod p                                       96−1 mod 257
  Euclidean pairs         quotient                   Euclidean pairs     quotient
    (0, p), (1, x)    q = ⌊p/x⌋                      (0, 257), (1, 96) 2 = ⌊257/96⌋
                                x
 (−q, p − qx), (1, x) q ′ = ⌊ p−qx ⌋                 (−2, 65), (1, 96) 1 = ⌊96/65⌋
 (−q, p − qx), (1 + q ′ q, x − q ′ (p − qx))         (−2, 65), (3, 31) 2 = ⌊65/31⌋
          ·                                           (−8, 3), (3, 31) 10 = ⌊31/3⌋
          ·                                           (−8, 3), (83, 1) 3 = ⌊3/1⌋
  (−p, 0), (x−1 , 1)                                (−257, 0), (83, 1)

Note that at termination the Euclidean pairs will either be (−p, 0), (x−1 , 1) or
(x−1 − p, 1), (p, 0). In the later case we have to add p to x−1 − p to get the
standard representation.

5.1     Stepwise reversibility
A priori it’s not clear whether an iteration of the extended Euclidean algorithm
is reversible. In particular it’s not clear whether the quotients q will need
to be stored or if they can be uncomputed. If they need to be stored then
this will constitute a considerable number of “garbage” bits which could only
be uncomputed (in the usual way) once the whole inverse finding algorithm
had finished. Fortunately it turns out that each iteration of the algorithm is
individually reversible.
    Concretely let’s look at uncomputing the quotient q after an iteration which
transformed (a, A), (b, B) into (a − qb, A − qB), (b, B). We know that A > B
and q = ⌊A/B⌋. It is not hard to see that a and b will never have the same sign
and that A > B if and only if |a| < |b|. Therefore ⌊− a−qbb ⌋ = q. Thus we see,
that while q is computed from the second components of the original Euclidean
pairs, it can be uncomputed from the first components of the modified Euclidean
pairs.

5.2     Simple implementations with time O(n3 ) and O(n2 log2 n)
While it is a relief that the extended Euclidean algorithm is piecewise reversible,
we are not at the end of our labours. Note that the number of iterations (modu-
lar reductions) in the algorithm for x−1 mod p depends on x in an unpredictable
way. This is a problem because we want to apply this algorithm to a superposi-
tion of many x’s. Still worse is, that even the individual iterations take different
times for different inputs x when the algorithm is implemented in an efficient
way. Namely, the quotients q tend to be small, and we want to use algorithms
in each iteration which exploit this fact, since for small q the steps can be made
faster. Only then does the extended Euclidean algorithm use time bounded by
O(n2 ).


                                               15
    Suppose that in each iteration of the algorithm we use full sized divisions
and multiplications, thus the ones which we would use if we expected full sized
n bit numbers. These algorithms (e.g. the modular multiplication described in
section 4.3.2) consist of a fixed sequence of O(n2 ) gates and can work just as
well on a superposition of inputs. As there are O(n) iterations, the extended
Euclidean algorithm would then use O(n3 ) gates.

5.2.1   Using bounded divisions
The running time O(n3 ) can be improved by noting that large quotients q are
very rare. Actually in a certain limit the probability for the quotient to be q0
or more, is given by P (q ≥ q0 ) = log2 (1 + 1/q0 ) ≈ 1/(q0 ln 2) (see e.g. [21] Vol.
2, section 4.5.3). If we use an algorithm that works for all quotients with less
than, say, 3 log2 n bits, then the probability of error per iteration will be ≈ 1/n3 .
Or, if acting on a large superposition, this will be the fidelity loss. Because in
the whole discrete logarithm algorithm we have O(n2 ) such iterations (O(n)
iterations for each of the O(n) group shifts), the overall fidelity loss will only be
of order O(1/n). Still, even with these bounded divisions the overall complexity
of the extended Euclidean algorithm would be O(n2 log2 n).
    We would like to obtain a running time of O(n2 ), which would lead to an
O(n3 ) discrete logarithm algorithm. Our proposed implementation of the ex-
tended Euclidean algorithm attains this O(n2 ) running time. Our implemen-
tation is not only faster asymptotically, but also for the sizes n of interest,
although only by a factor of 2 to 3.

5.3     Our proposed implementation
We have investigated various efficient implementations of the extended Eu-
clidean algorithm. Fortunately, the one presented here is one of the simpler
ones. To get an O(n2 ) algorithm, we will not require all the basis states in the
superposition to go through the iterations of Euclid’s algorithm synchronously.
Rather we will allow the computation for each basis state to proceed at its own
pace. Thus at a given time, one computation may be in the course of the 10-
th iteration, while another one is still in the 7-th iteration. Later the second
computation may again overtake the first one.
    The basic observation of our implementation is that it consists of only five
different operations, most of which are essentially additions and subtractions.
Thus each of the many “quantum-parallel” computations (thus each basis state)
can store in a few flag bits which one of these five operations it needs. The
implementation can then simply repeatedly cycle through the five operations
one after the other, each one conditioned on the flag qubits. Thus as each
operation is applied only those basis states which require it will be affected.
For each cycle through the five operations the flag bits of a given computation
will often only allow one operation to be applied to the computation. Therefore
we loose a factor of somewhat less than five in speed relative to a (reversible)
classical implementation.


                                         16
5.3.1    Desynchronising the parallel computations
Let us first explain in more detail the general approach to desynchronising the
“quantum-parallel” computations. Suppose, for example, that there are only
three possible (reversible) operations o1 , o2 and o3 in a computation. Suppose
further that each computation consists of a series of o1 ’s then o2 ’s, o3 ’s and so
on cyclicly. E.g. we would like to apply the following sequence of operations to
two different basis state:

                          . . . o2 o2 o2 o1 o3 o3 o2 o1 o1 o1 o1 |xi
                            . . . o2 o1 o1 o1 o3 o2 o2 o2 o2 o1 |x′ i

Clearly there must be a way for the computation to tell when a series of oi ’s
is finished and the next one should begin. But because we want to do this
reversibly, there must also be a way to tell that an oi is the first in a series.
Say we include in each oi a sequence of gates which flips a flag qubit f if oi is
the first in a sequence and another mechanism that flips it if oi is the last in a
sequence. (If there is a single oi in a sequence, and thus oi is both the first and
the last oi , then f is flipped twice.)
    We will also make use of a small control register c to record which operation
should be applied to a given basis state. Thus we have a triple x, f, c where
x stands for the actual data. We initialise both f and c to 1 to signify that
the first operation will be the first of a series of o1 operations. The physical
quantum-gate sequence which we apply to the quantum computer is:

                  . . . ac o′1   ac o′3 ac o′2 ac o′1     ac o′3 ac o′2 ac o′1 |QCi

Where the o′i are the oi conditioned on i = c and ac stands for “advance
counter”. These operations act as follows on the triple:

          o′i :        if i = c :          x, f, c        ↔   oi (x), f ⊕ f irst ⊕ last, c
          ac :         x, f, c     ↔     x, f, (c + f ) mod 3

Where o′i doesn’t do anything if i 6= c, ⊕ means XOR and (c + f ) mod 3 is
taken from {1, 2, 3}. In the middle of a sequence of oi ’s the flag f is 0 and so
the counter doesn’t advance. The last oi in a series of oi ’s will set f = 1 and
thus the counter is advanced in the next ac step. Then the first operation of
the next series resets f to 0, so that this series can progress.

5.3.2    Applying this to the extended Euclidean algorithm
Back to our implementation of the extended Euclidean algorithm. For rea-
sons which will be discussed below, in our implementation we always store the
Euclidean pair with the larger second coordinate first. Thus one (reversible)
iteration of the algorithm is:
                                                                                             a − qb
(a, A), (b, B)      ↔       (b, B), (a−qb, A−qB)              where     q = ⌊A/B⌋ = ⌊−              ⌋
                                                                                               b

                                                     17
This will be decomposed into the following three individually reversible steps:

   A, B ↔ A − qB, B, q                a, b, q ↔ a − qb, b              and      SWAP        (4)

where by “SWAP” we mean the switching of the two Euclidean pairs. Note
that it appears that all the bits of q must be calculated before they can be
uncompute. This would mean that the computation can not be decomposed
further into smaller reversible steps. We now concentrate on the first of these
operations, which starts with a pair A, B of positive integers where A > B.
Actually, since |a − qb| > |b|, the second operation a, b, q ↔ a − qb, b can be
viewed as the same operation run backwards. The fact that a and b can be
negative (actually they have opposite sign) is only a minor complication.
    So we want to do the division A, B ↔ A − qB, B, q in a way which takes less
time for small q, namely we want to do only around log2 q subtractions. What
we do is essentially grade school long division in base 2. First we check how
often we have to double B to get a number larger than A, and then we compute
the bits of q from highest significance to lowest. In the first phase (operation 1)
we begin with i = 0 and do a series of operations of the form

                                A, B, i    ↔        A, B, i + 1

As explained in section 5.3.1, we need to flip a flag bit f at the beginning and
at the end of this series. The beginning is easily recognised as i = 0. The end
is marked by 2i B > A. Thus testing for the last step essentially involves doing
a subtraction in each step.
    In the second phase (operation 2) we then diminish i by 1 in each step:

         A − q ′ B, B, i + 1, q ′      ↔     A − (q ′ + 2i qi )B, B, i, q ′ + 2i qi

where q ′ = 2i+1 qi+1 + 2i+2 qi+2 + . . . is the higher order bits of q. The new bit
qi is calculated by trying to subtract 2i B from the first register. This is easily
done by subtracting and, if the result is negative (qi = 0), undoing the entire
subtraction in the carry uncomputing phase. The first operation in the second
phase is recognised by checking q ′ = 0 and the last by checking i = 0. Note that
when incrementing and decrementing i we might actually want to shift the bits
of B to the left (resp. right), as then the gates in the subtractions can be done
between neighbouring qubits.
    The third and fourth phases perform a, b, q ↔ a − qb, b and are essentially
the reverses of phases two and one respectively. Thus operations three and four
are

      a − qb + (q ′ + 2i qi )b, b, i, q ′ + 2i qi     ↔     a − qb + q ′ b, b, i + 1, q ′

and

                           a − qb, b, i    ↔        a − qb, b, i − 1

where q ′ and qi are as in phase two. The first and last operation conditions of
phase three are i = 0 and q ′ = 0. While the first and last operation conditions

                                              18
of phase four are |a − qb| < 2i+1 |b| and i = 0. (These conditions are essentially
the last and first operation conditions for phases two and one respectively.)
    Finally we also need to do the SWAP operation where we switch the two
Euclidean pairs so that again their second components are in the order: larger
to the left, smaller to the right. If we didn’t do that, we would have to double
the set of operations above, to take care of the case when the roles of the pairs
are switched. The SWAP of course simply switches the registers qubit by qubit
(although this has to be done conditional on the control register c). As every
sequence of SWAP operations will be of length one, the flag bit f can be left
untouched.

5.3.3    How many steps are necessary?
With the SWAP we have a sequence of five operations which we repeatedly
apply one after the other to the quantum computer. So the question is: How
many times do we need to cycle through the five operations? Each iteration of
Euclid’s algorithm ends with a SWAP and thus requires an integer number of
cycles through the five operations. Also note, that in each iteration the length
of the sequence of operations oi is the same for all four phases. Thus for one
iteration the following operations might actually be applied to one computation:

                  SWAP o4 o4 o4 o3 o3 o3 o2 o2 o2 o1 o1 o1 |xi

The length z of the sequences (here 3) is the bit length of the quotient q in
the iteration (i.e. z = ⌊log2 q⌋ + 1). If each operation is done only once (so
z = 1), everything will be finished with one cycle through the five operations.
In general the number of cycles for the iteration will be 4(z − 1) + 1.
    Let r be the number of iterations in a running of Euclid’s Algorithm on p, x,
let q1 , q2 , . . . , qr be the quotients in each iteration and let t be the total number
of cycles required. Then
                        r
                        X                             r
                                                      X
                   t=     (4⌊log2 (qi )⌋ + 1) = r + 4   ⌊log2 (qi )⌋
                        i=1                            i=1

For p > 2 a bound on t is 4.5 log2 (p) (see appendix B). Thus we can bound the
number of cycles by 4.5n.

5.3.4    The quantum halting problem: a little bit of garbage
Actually, because the inverse computation for each basis state has to be re-
versible it can’t simply halt when B = 0. Otherwise, when doing things back-
ward, we wouldn’t know when to start uncomputing. This has been called the
“quantum halting problem”, although it seems to have little in common with
the actual classical (undecidable) halting problem. Anyway, instead of simply
halting, a computation will have to increment a small (log2 4.5n bit) counter
for each cycle after Euclid’s algorithm has finished. Thus once per cycle we will
check if B = 0 to determine if the completion counter needs to be incremented.

                                           19
This means that at the end of Euclid’s algorithm we will actually have a little
“garbage” besides x−1 mod p. Also, at least one other bit of garbage will be
necessary because, as mentioned earlier, half the time we get x−1 − p instead
of x−1 itself. Note that in our computation of x, y ↔ x, y/x we use Euclid’s
algorithm twice, once for x ↔ x−1 and once for the converse (see section 4.3.1).
Thus we can simply leave the garbage from the first time around and then run
the whole algorithm backwards.

5.3.5   Saving space: Bounded divisions and register sharing
To solve the DLP our algorithm will need to run the Euclidean algorithm 8n
times. Each running of the Euclidean algorithm will require at most 1.5n iter-
ations (see [22]). Thus the DLP algorithm will require at most 12n2 Euclidean
iterations. As mentioned in section 5.2.1, the probability for the quotient, q, in
a Euclidean iteration to be c log2 n or more, is ≈ 1/nc. Thus by bounding q to
3 log2 n-bits (instead of n bits) the total loss of fidelity will be at most 12/n.
    Over the course of Euclid’s algorithm, the first number a in the Euclidean
pair (a, A) gets larger (in absolute value), while A gets smaller. Actually the
absolute value of their product is at most p: At any given time, we store the
two parentheses (a, A) and (b, B). It is easy to check that |bA − aB| remains
constant and equals p during the algorithm (bA − aB simply changes sign from
one iteration to the next and the initial values are (0, p) and (1, x)). Now
p = |bA − aB| ≥ |bA| ≥ |aA|, where we used that a and b have opposite sign
and |a| < |b|. So we see that a and A could actually share one n-bit register.
Similarly, since |bB| ≤ |bA| ≤ p, it follows that b and B could also share an
n-bit register.
    The problem is, that in the different “quantum parallel” computations, the
boundary between the bits of a and those of A (or b and B) could be in different
places. It will be shown in section 5.4.3 that the average number of cycles
required is approximately 3.5n. Thus on average after r cycles we would expect
A and B to have size n − r/3.5 and the size of a and b to be r/3.5. We shall
define the “size perturbation” of a running of the extended Euclidean algorithm
as the maximum number of bits any of A, B, a or b reach above their expected
sizes. Table 1 gives some statistics on size perturbations for various values of n.
For each value of n in the table, the size perturbations were calculated for one
million runnings of Euclid’s algorithm (1000 random inverses for each of 1000
random primes). From√    the table we see that
                                             √ the mean of the size perturbations
ranges from 1.134 n for n = 110  √  to 1.069   n for n = 512 and over all 6 million
calculations was never over 2 n. By analyzing the distributions of the size
perturbations it was seen that for n ∈ [110, 512] the distributions are close to
normal with the given means and standard deviations.
    Thus one method of register sharing between a, A, b and B√would be to take
the size of the registers to be their expected  √ values plus 2 n. In this case
the four registers could be stored in 2n + 8 n qubits (instead of 4n qubits).
Note that a, A, b and B are never larger than p, thus when implementing the
register sharing one would actually use the minimum of n and the expected


                                        20
                n     Mean Size       Standard     Maximum Size
                     Perturbation     Deviation    Perturbation
               110      11.90           1.589           18
               163      14.13           1.878           24
               224      16.35           2.115           25
               256      17.33           2.171           25
               384      21.02           2.600           31
               512      24.20           3.084           38

            Table 1: Size perturbations during Euclid’s Algorithm


             √
value plus 2 n. As the amount of extra qubits added to the expected sizes of
the buffers was only found experimentally, we shall carry through the analysis
of the algorithm both with and without register sharing.

5.4     Analysis of the Euclidean algorithm implementation
The most basic operations, namely additions and subtractions, are in the end
conditioned on several qubits, which seems to complicate things a lot. But before
e.g. doing an addition we can simply compute the AND of these control qubits,
put it into an auxiliary qubit, and use this single qubit to control the addition.
Thus the basic operations will essentially be (singly) controlled additions and
subtractions, as for the factoring algorithm. Detailed networks for this can e.g.
be found in [5].

5.4.1   Running time: O(n2 )
Let us now analyze the running time of our implementation of the extended
Euclidean algorithm. The algorithm consists of 4.5n operation cycles. During
each of these cycles the halting register needs to be handled and each of the five
operations needs to be applied.
    Handling the halting register requires checking if B = 0 and incrementing
the log2 4.5n bit register accordingly. The following table summarises the oper-
ations required in the first four operations of a cycle.

           Main Operation              First Check            Last Check
   1          z-bit ADD                z-bit ZERO              w-bit SUB
   2    w-bit SUB, z-bit SUB      (3 log2 n)-bit ZERO        z- bit ZERO
   3    w-bit ADD, z-bit ADD          z- bit ZERO        (3 log2 n)-bit ZERO
   4          z-bit SUB                 w-bit SUB             z-bit ZERO

Where z = log2 (3 log2 n) is the size of the register for i, w represents the bit
size of the registers for a, A, b and B (w ≤ n and depends on whether or not
register sharing is being used), ZERO means a compare to zero and the w-bit


                                       21
operations are applied to two quantum registers. Lastly, the fifth operation of
the cycle, SWAP, swaps two registers of size at most 2n.
    Therefore each of the 4.5n cycles requires 4 w-bit additions/subtractions, a
SWAP and a w-bit compare to zero, all of which are O(n). The running time
of the w-bit operations dominate the algorithm and lead to a running time of
O(n2 ).

5.4.2   Space: O(n)
Let us now determine the number of qubits required for our implementation of
the extended Euclidean algorithm. The largest storage requirement is for the
two Euclidean pairs (a,√A) and (b, B), which as discussed in section 5.3.5, can
be either 4n or 2n + 8 n bits depending on whether or not register sharing is
used. The next largest requirement is the n bits needed for the carry register
during the additions and subtractions. The quotient q will require (3 log2 n)
bits (see 5.3.5). The halting counter, h, will be of size log2 4.5n, however since
h and q are never required at the same time they can share a register. The i
register needs to be able to hold the bit size of the maximum allowed quotient
(3 log2 n) and thus easily fits in a log2 n register. Lastly the algorithm requires
a small fixed number (< 10) of bits for the flag f , the control register c and
any other control bits. Thus√ we see that the algorithm requires approximately
5n + 4 log2 n + ǫ or 3n + 8 n + 4 log2 n + ǫ bits depending of whether register
sharing is used. In either case we see that the space requirement is O(n).

5.4.3   Possible improvements and alternative approaches
Here we list a few possible improvements and alternatives to our approach. It
might also be that there are standard techniques, which we are not aware of,
for finding (short) acyclic reversible circuits.

Reducing the number of cycles
While 4.5n is a limit on the maximum number of cycles required in the Euclidean
algorithm, there are very few inputs for which the algorithm actually approaches
this bound. For a prime p let Lq (p) be the number of times q occurs as a quotient
when the Euclidean algorithm is run on p, x for all x satisfying 1 < x < p. In
[23] it was shown that
                                              
                    12(p − 1)       (q + 1)2
           Lq (p) =           ln                 ln(p) + O(p(1 + 1/p)3 )
                       π2         (q + 1)2 − 1

Using this fact, it can be shown that the total number of cycles required for
finding x−1 for all 1 < x < p is
               p−1
               X
                     Lq (p) 4⌊log2 (q)⌋ + 1) ≈ (p − 1)3.5 log2 (p)
               q=1




                                          22
Thus the average number of cycles is approximately 3.5n. Experiments con-
ducted seem to show that the distribution
                                   √      of required cycles is close to normal
with a standard deviation of around n. Thus if we run the quantum computer
a few standard deviations beyond the average number of cycles, nearly all com-
putations will have halted making the loss of fidelity minimal. While this still
leads to a O(n3 ) DLP algorithm, the constant involved will have decreased.

Reducing the number of carry qubits
Actually the number of carry qubits can be reduced by “chopping” e.g. an
n-qubit addition into several pieces and have the carry qubits not go much
beyond one piece at a time. (Thereby we sacrifice some fidelity, see e.g. [5].)
This procedure takes somewhat more time than a standard addition, but it may
well make sense to reduce the number of carry qubits (currently n) by a factor
of 2 or 3.

Store length of numbers separately
Here the idea is to also store the bit lengths of the numbers in (a, A) and (b, B).
In the divisions A/B etc. the size of q could be determined by one comparison.
Also
 √ the register sharing might be easier, allowing for fewer than the current
8 n extra qubits. Another possibility might be to synchronise the quantum
parallel computations by the lengths of the numbers. Then we would e.g. even
classically know the size of A.

More classical pre-computation for GF (p)
As mentioned earlier, we can assume that classical computation is much cheaper
than quantum computation. Thus it might be reasonable to classically pre-
compute and store many values specific to GF (p), if these values would help to
make the quantum implementation of Euclid’s algorithm easier. Unfortunately
we haven’t found any way of doing this.

A quantum solution to arithmetic in GF (p)
With an (approximate) quantum Fourier transform of size p, addition modulo
p in a way becomes simpler [24]. It would be nice to find such a “quantum
solution” to both, addition and multiplication. But to us it seems unlikely that
this is possible.

Binary extended Euclidean algorithm
This is a variant of Euclid’s algorithm (see e.g. [21], Vol. 2, p. 338) which only
uses additions, subtractions and bit shifts (divisions by 2). Basically one can
subtract (b, B) from (a, A), but one also divides a parenthesis by 2 till the second
component is odd. We haven’t managed to see that this algorithm is piecewise
reversible. Still, even if it isn’t, it may be enough to keep relatively little garbage


                                          23
around to make it reversible (Our implementation of this algorithm used 7n + ǫ
qubits and had a running time of O(n2 )).


6     Results and a comparison with factoring
6.1     Total time for the DLP algorithm
Let’s collect the total number of quantum gates for the whole discrete logarithm
algorithm. Remember that the success probability of the algorithm is close to
1 (appendix A), thus we assume that we have to do only a single run. We will
not actually go to the lowest level and count the number of gates, but rather
the number of (n-bit) additions.
    In table 2, we decompose each part of the DLP algorithm into its subroutines,
plus things that can be done directly (to the right). At the top are the 2n group
shifts by a fixed (classical) elliptic curve point (section 4.1), n for x · P and
n for y · Q. Each group shift is decomposed into 2 divisions (section 4.3.1), a
multiplication to square λ, and a few modular additions. Multiplications and
additions here are understood to be modulo p (section 4.3.2).


    2n group shifts (e.g. |Ai → |A + 2i · P i)
    |     {z      }
          ↓ each
        2
        | divisions
            {z }     + 1 multiplication (for squaring λ)      + 5 additions
                       |              {z               }
                                  each 3n additions
               ↓ each
             2
             | Euclid’s
                {z }       +         2 multiplications
                                     |      {z       }
                                        each 3n additions
                      ↓ each
                   4.5n cycles
                   | {z }
                          ↓ each
                        5 operations      + halting counter
                        |    {z    }
                                 ↓ each
                            1 (short) addition   + flag + counter operations
                            |       {z       }     |           {z            }
                                          √
                        average ≈ n/2 + 2 n bits   on ≤ 3 log2 n bit registers


                       Table 2: DLP Algorithm Operations

   As discussed in section 5.4.1, a running of Euclid’s algorithm requires 4.5n
cycles through the five operations. If w represents the sizes of the a, A, b and


                                            24
B registers then each of these cycles requires a w-bit compare to zero (for the
halting register), 4 w-bit additions/subtractions, a register swap and some op-
erations on 3 log2 n and log2 (3 log2 n) bit registers. For our analysis we shall
assume that all these operations together are equivalent to 5 w-bit additions
(This is reasonable since the SWAP and compare to zero operations are quite
easy compared to additions, see e.g. [4] fig. 10). After the first running of
Euclid’s algorithm we have found the inverse, but still have some garbage in
the halting register. We saw in section 5.3.4 that the second running of Euclid’s
algorithm will actually be the reverse of the above operations. Thus the run-
ning time of the two instances of Euclid’s algorithm will be double the above
operations.
   To get a nice comparison to the factoring algorithm we need to know how
many classical-quantum additions are required (since the factoring algorithm
uses additions in which one summand is known classically [5]). In order to
do this we assume that a quantum-quantum addition is a factor of 1.7 times
more difficult than a classical-quantum addition (we estimated this ratio from
the networks in [5]). When register sharing
                                         √     is used, √the sizes of the a, A, b and
B registers change linearly
                      √      between   2  n  and  n +  2   n. This implies that on
average w = n/2 + 2 n. This gives a total running time of
                                                    
               T = 2n 5 + 3n + 2[6n + 2(4.5(5n))] · 1.7 ≈ 360n2

n-bit additions with no register sharing and
                                            √   
    T = 2n 5 + 3n + 2[6n + 2(4.5 · 5(n/2 + 2 n))] · 1.7 ≈ 205n2 + 615n3/2

n-bit additions with register sharing.
    As a classical-quantum addition is O(n) this implies that the discrete loga-
rithm algorithm is O(n3 ). Assume a running time of k · n for an n-bit classical-
quantum addition. Then the discrete logarithm algorithm has a running time
of approximately 360kn3 compared to only about 4kn3 for factoring, but the
larger n needed for classical intractability more than compensates for this (see
section 6.3).

6.2    Total number of qubits (roughly 6n)
For the number of qubits necessary for the discrete logarithm algorithm, what
counts is the operations during which the most qubits are needed. Clearly this
is during the extended Euclidean algorithm, and not e.g. in the course of a
modular multiplication.
    In fact, the maximum qubit requirement will occur in the second call to the
Euclidean algorithm within each division (see section 4.3.1). Here we require
two n-bit registers plus a register on which to carry out the Euclidean algorithm
(see table 3). Thus√ the DLP algorithm requires either f (n) = 7n + 4 log2 n + ǫ
or f ′ (n) = 5n + 8 n + 4 log2 n + ǫ bits depending of whether register sharing is
used (see section 5.4.2). Therefore the DLP algorithm, like the extended Euclid
algorithm, uses space O(n).

                                         25
 division
 | {z }
      ↓
      2n + |Euclid
             {z }
                 ↓
             (a, A) + (b, B) + carry qubits +      q + i      + |minor
                                                                     {z stuff}
             |      {z     }   |    {z    }        | {z }
                       √                                        < 10 qubits
               2n + 8 n          n qubits     4 log2 n qubits

            Table 3: Maximum Bit Requirement With Register Sharing


6.3    Comparison with the quantum factoring algorithm
One of the main points of this paper is that the computational “quantum advan-
tage” is larger for elliptic curve discrete logarithms than for the better known
integer factoring problem. With our proposed implementation we have in par-
ticular achieved similar space and time requirements. Namely the number of
qubits needed is also of O(n) and the number of gates (time) of order O(n3 ),
although in both cases the coefficient is larger. Note that the input size n is
also the key size for RSA resp. ECC public key cryptography. Because the best
known classical algorithms for breaking ECC scale worse with n than those for
breaking RSA, ECC keys with the same computational security level are shorter.
Below is a table with such key sizes of comparable security (see e.g. [25]). The
column to the right roughly indicated the classical computing resources neces-
sary in multiples of C, where C is what’s barely possible today (see. e.g. the
RSA challenges [26] or the Certicom challenges [27]). Breaking the keys of the
last line seems to be beyond any conceivable classical computation, at least if
the presently used algorithms can’t be improved.
    Factoring algorithm (RSA)         EC discrete logarithm (ECC) classical
    n      ≈ # qubits       time       n     ≈ # qubits        time     time
               2n            4n3             f ′ (n) (f (n))  360n3
   512        1024       0.54 · 109 110       700 (800)      0.5 · 109    C
                                   9
  1024        2048        4.3 · 10    163 1000 (1200) 1.6 · 109        C · 108
  2048        4096         34 · 109   224 1300 (1600) 4.0 · 109        C · 1017
                                   9                                 9
  3072        6144        120 · 10    256 1500 (1800) 6.0 · 10         C · 1022
                                  13                                 9
  15360      30720       1.5 · 10     512 2800 (3600)        50 · 10   C · 1060
Where f (n) and f ′ (n) are as in section 6.2 with ǫ = 10. The time for the
quantum algorithms is listed in units of “1-qubit additions”, thus the number
of quantum gates in an addition network per length of the registers involved.
This number is about 9 quantum gates, 3 of which are the (harder to implement)
Toffoli gates (see e.g. [5]). Also it seems very probable that for large scale quan-
tum computation error correction or full fault tolerant quantum computation
techniques are necessary. Then each of our “logical” qubits has to be encoded
into several physical qubits (possibly dozens) and the “logical” quantum gates
will consist of many physical ones. Of course this is true for both quantum


                                        26
algorithms and so shouldn’t affect the above comparison. The same is true for
residual noise (on the logical qubits) which will decrease the success probability
of the algorithms. The quantum factoring algorithm may have one advantage,
namely that it seems to be easier to parallelise.

Acknowledgements
Ch.Z. is supported by CSE (Communications Security Establishment) and MI-
TACS (Mathematics of Information Technology and Complex Systems), both
from Canada.


A     Appendix: Detailed analysis of the success
      probability
Here we analyse in some detail the success probability of the discrete logarithm
quantum algorithm when we use the usual quantum Fourier transform of size
N = 2n , as opposed to the ideal case which would have prime size. The result
is, that the algorithm has a probability close to 1 of giving the right answer.
Thus when looking at the runtime we will assume that a single run is enough.

A.1     Order finding algorithm (basis of factoring)
We first consider the case of the order finding algorithm (section 2.2.1) which
is the basis of the factoring algorithm. The discrete logarithm case is then sim-
ply a 2 dimensional version of this. Here we will use the eigenvalue estimation
viewpoint introduced by Kitaev [11] (see also [17]). The advantage of this view-
point is, that the (mixed) state of the register which we ultimately measure is
explicitly written as a mixture of isolated “peaks” (thanks to Mike Mosca for
pointing this out). In the usual picture, which we used in section 2.2.1, we have
the diagonalised form of the mixed state (or, equivalently, we use the Schmidt
normal form between the entangled registers). But there we have to worry about
destructive interference between different peaks, which makes the analysis a bit
less nice.
    So we want to find the order r of a group element α. Again we do:
             1 X                 1 X             1 X
            √     |xi      →    √    |x, αx i = √    |xi Uαx |ei
              N x                N x             N x

Where e is the neutral element and Uα is multiplication by α, thus Uα |gi = |αgi.
(Eigenvalue estimation refers to the eigenvalues of Uα .) Now we write |ei in
terms of eigenstates of Uα . These r eigenstates are easy to find:
              r−1
          1 X kk′ k′
  |Ψk i = √    ωr |α i with           Uα |Ψk i = ωr −k |Ψk i and ωr = e2πi/r
           r ′
              k =0




                                       27
It is also easy to see that |ei is simply a uniform superposition of these states:
                                                      1 X
                                                |ei = √   |Ψk i
                                                       r
                                                                  k

So the state of the quantum computer can be written as
                         1 X             1 X      1 X −kx
                        √    |x, αx i = √     |xi √    ωr |Ψk i
                         N x              N x      r
                                                     k

Now we apply the QFFTN to the first register to obtain:
                                                    !
                  1 X X 1 X           xx′   −kx ′
                 √                 ωN ωr        |x i |Ψk i
                   r       N x
                         ′      k          x

Because the |Ψk i are orthogonal, the state of the first register alone can be
viewed as a mixture of r pure states, one for each k. The probabilities associated
with each of these pure states are equal, namely 1/r, as can be seen from the
previous equation. By summing the geometrical series in the sum over x we get
for these (normalised) pure states:

                  X 1 X                                               X 1 e2πiN (x′ /N −k/r) − 1
                                     xx′        −kx     ′
                                ωN         ωr         |x i    =                                        |x′ i =
                        N   x
                                                                           N e2πi(x′ /N −k/r) − 1
                   x′                                                 x′
    X         ′     sin(π(x′ − kN/r))                                 X         ′      sin(π(x′ − x′0 ))
=        eiφ(x )                         |x′ i                =            eiφ(x )                          |x′ i
                   N sin(π(x′ /N − k/r))                                             N sin(π(x′ − x′0 )/N )
    x′                                                                x′

Where φ(x′ ) is some (irrelevant) phase. We see that each of these states is
dominated by basis states |x′ i with

                                           x′     ≈         k · N/r = x′0

    Thus each of the pure states corresponds to one “smeared out” peak centered
at x′0 . Note that the argument of the sine in the denominator is small. So the
shape of the peak is approximately given by the function sin(πx)/(πx) sampled
at values for x which are integers plus some constant fractional offset, as plotted
in figure 1.
    We are interested in the probability of observing a basis state no farther
away from the center x′0 of the peak than, say ∆x′ . How spread out the peak is,
depends on the fractional offset. If there is no offset, then we simply observe the
central value with probability 1. The largest spread occurs for offset 1/2. (Then
the probabilities of the two closest basis states are each 4/π 2 .) The chance of
obtaining a state at distance ∆x′ decreases as 1/(∆x′ )2 . So the probability of
being away more than ∆x′ on either side is at most about 2/∆x. Because the
total probability is normalised to 1, this tells us what the chance is of coming
within ∆x′ of the central value.



                                                             28
                                                  1




                                                0.5




         –5       –4     –3       –2       –1    0         1    2   x 3    4     5




Figure 1: The function sin(πx)
                          πx . Up to an (irrelevant) phase, the amplitudes near
a “peak” are given by sampling this function at integer intervals, as indicated
by the circles.



A.2     Discrete logarithm case
The discrete logarithm case is analogous, actually it can be viewed as a two
dimensional version of the order finding algorithm. We have
       N −1                                                                    q−1
       X                          X                        X                 1 X
              |x, y, αx β y i =         |x, y, αx+dy i =       |x, yiUα x+dy √   |Ψk i
      x,y=0                       x,y                      x,y
                                                                              q
                                                                               k=0

By applying a Fourier transform of size N to each of the first two registers we
get
                                                                      
     1  X     X    1  X        ′        1 X        ′
     √                   ωN xx ωq −kx        ωN yy ωq −dky |x′ , y ′ i |Ψk i
      q            N   x
                                        N  y
          k    ′ ′x ,y


Again we get a peak for each k, and each with the same probability. The x′ and
y ′ values are independently distributed, each as in the above 1-dimensional case.
For x′ the “central value” is N k/q and for y ′ it is N dk/q. To obtain the values
k and dk which we want, we multiply the observed x′ , y ′ with q/N and round.
Thus, if we chose N (= 2n ) sufficiently larger than q, we are virtually guaranteed
to obtain the correct values, even if x′ and y ′ are a bit off. Alternatively, we
can try out various integer values in the vicinity of our candidate k and dk,
thus investing more classical post-processing to make the success probability
approach 1.




                                                  29
B      Appendix: Bounding the number of cycles
It was shown in section 5.3.3 that the number of cycles required to complete the
Euclidean algorithm on inputs p and x is
                                          r
                                          X
                            t(p, x) = 4         ⌊log2 (qi )⌋ + r
                                          i=1

where q1 , q2 , . . . , qr are the quotients in the Euclidean algorithm.

Lemma 1 If p and x are coprime integers such that p > x ≥ 1 and p > 2 then
t(p, x) ≤ 4.5 log2 (p).
Proof: Assume by way of contradiction that there exist integers (p, x) for
which the lemma does not hold. Let (p, x) be an input for which the number
of Euclidean iterations, r, is minimal subject to the condition that the lemma
does not hold (i.e. t(p, x) > 4.5 log2 (p), p > 2, p > x ≥ 1 and gcd(p, x) = 1).
Let q1 , . . . , qr be the quotients when the Euclidean algorithm is run on (p, x).
    We will now obtain a contradiction as follows. First, we show that if t(p, x) >
4.5 log2 (p) then the Euclidean algorithm with input (p, x) will require at least
three iterations (i.e. r ≥ 3). Next, we show that if t(p, x) > 4.5 log2 (p) and
the Euclidean algorithm run for two iterations on input (p, x) returns the pair
(y, z) then (y, z) also contradict the lemma. Since (y, z) would contradict the
lemma with fewer iterations than (p, x) this contradicts the existence on (p, x).
It is easily verified that the lemma holds provided 2 < p ≤ 15 (simply calculate
t(p, x) for each of the possibilities). We can thus assume that p ≥ 16.
    Recall that the Euclidean algorithm takes as input two integers (a, b) and
terminates when one of a and b is set to zero, at which point the other integer
will be gcd(a, b). An iteration of the Euclidean algorithm on (a, b), with a ≥ b,
returns (a − qb, b), where q = ⌊a/b⌋. Note that since gcd(p, x) = 1 on this input
the algorithm will terminate with either (1, 0) or (0, 1).
    Let us first prove that the Euclidean algorithm with input (p, x) will require
at least three iterations. Since neither p nor x is zero we know that r ≥ 1.
Suppose that r = 1. Then the single iteration of the algorithm transforms (p, x)
to (p − q1 x, x) = (0, 1). This implies that x = 1 and q1 = p. Thus

           t(p, x) = 4⌊log2 (p)⌋ + 1 ≤ 4.5 log2 (p)                (since p > 2)

which implies that r ≥ 2. Suppose that r = 2. Then the two iterations of the
algorithm would transform

            (p, x) → (p − q1 x, x) → (p − q1 x, x − q2 (p − q1 x)) = (1, 0)




                                           30
This implies that p − q1 x = 1 and q2 = x. Thus p − q1 q2 = 1, which implies
that log2 (p) > log2 (q1 ) + log2 (q2 ). Therefore
                  t(p, x)    = 4⌊log2 (q1 )⌋ + 4⌊log2 (q2 )⌋ + 2
                             ≤ 4⌊log2 (q1 ) + log2 (q2 )⌋ + 2
                             < 4⌊log2 (p)⌋ + 2
                             ≤ 4.5 log2 (p)                (since p ≥ 16)
and we have that r ≥ 3. Note that we now know x 6= 1, 2, p − q1 x 6= 1 and
x − q2 (p − q1 x) 6= 0 since any of these would imply r ≤ 2.
    We shall now establish that q1 ∈ {1, 2}. After the first iteration of the
Euclidean algorithm the problem is reduced to running the algorithm on (p −
q1 x, x), for which the quotients will be q2 , . . . , qr . Since xq1 ≤ p we have that
log2 (p) ≥ log2 (x) + log2 (q1 ). Therefore
                                    r
                                    X
         t(x, p − q1 x) =       4         ⌊log2 (qi )⌋ + r − 1
                                    i=2
                            =   t(p, x) − (4⌊log2 (q1 )⌋ + 1)
                            >   4.5 log2 (p) − (4⌊log2 (q1 )⌋ + 1)
                            ≥   4.5 log2 (x) + 4.5 log2 (q1 ) − 4⌊log2 (q1 )⌋ − 1
                            ≥   4.5 log2 (x)         (if q1 ≥ 3)
Thus if q1 ≥ 3 then t(x, p − q1 x) > 4.5 log2 (x), x > 2 and x > p − q1 x ≥ 1, but
this would contradict the minimality of r. Therefore q1 ∈ {1, 2}.
    After two iterations of the Euclidean algorithm on (p, x) the problem has
been reduced to running the algorithm on (p − q1 x, x − q2 (p − q1 x)). We will
now show that the lemma does not hold for (p − q1 x, x − q2 (p − q1 x)). This will
contradict the minimality of r and thus the existence of (p, x). To do this, we
must first show that p − q1 x > 2 and that p − q1 x > x − q2 (p − q1 x) ≥ 1 (so that
the lemma applies). As discussed above, since r ≥ 3 we know that p − q1 x > 1
and that p − q1 x > x − q2 (p − q1 x) ≥ 1, thus we need only show that p − q1 x 6= 2.
    Suppose that p − q1 x = 2. Since q1 ∈ {1, 2} either p = x + 2 or p = 2x + 2.
Since gcd(p, x) = 1 this implies that x is odd and that the Euclidean algorithm
will proceed as follows
                            (p, x) → (2, x) → (2, 1) → (0, 1)
Thus r = 3, q2 = (x − 1)/2, q3 = 2 and
         t(p, x) =     4⌊log2 (q1 )⌋ + 4⌊log2 ((x − 1)/2)⌋ + 4⌊log2 (2)⌋ + 3
                  =    4⌊log2 (q1 x − q1 ))⌋ + 3
                  ≤    4.5 log2 (p = q1 x + 2)
where the last line follows by checking the values for q1 ∈ {1, 2} and x < 64 and
noting that 4.5 log2 (q1 x) > 4 log2 (q1 x) + 3 when x ≥ 64. This would contradict
the fact that the lemma doesn’t hold for (p, x), thus p − q1 x 6= 2.

                                                31
    Now to complete the proof we need only show that t(p−q1 x, x−q2 (p−q1 x)) >
4.5 log2 (p − q1 x). Let x = cp, so p − q1 x = (1 − q1 c)p with 1 > 1 − q1 c > 0. By
the Euclidean algorithm we know that x ≥ q2 (p − q1 x) and thus

         log2 (x) = log2 (p) + log2 (c) ≥ log2 (p) + log2 (1 − q1 c) + log2 (q2 )

Therefore log2 (c/(1 − q1 c)) ≥ log2 (q2 ), which implies 1 − q1 c ≤ 1/(1 + q1 q2 ).
This in turn implies that log2 (p − q1 x) = log2 (p) + log2 (1 − q1 c) ≤ log2 (p) −
log2 (1 + q1 q2 ). Hence
                                            r
                                            X
 t(p − q1 x, x − q2 (p − q1 x))    =    4         ⌊log2 (qi )⌋ + r − 2
                                            i=3
                                   =    t(p, x) − (4⌊log2 (q2 )⌋ + 4⌊log2 (q1 )⌋ + 2)
                                   >    4.5 log2 (p) − (4⌊log2 (q2 )⌋ + 4⌊log2 (q1 )⌋ + 2)
                                   ≥    4.5 log2 (p − q1 x) + Z(q1 , q2 )

where Z(q1 , q2 ) = 4.5 log2 (1 + q1 q2 ) − (4⌊log2 (q2 )⌋ + 4⌊log2 (q1 )⌋ + 2).
   If q1 = 1 then Z(q1 , q2 ) = 4.5 log2 (1 + q2 ) − (4⌊log2 (q2 )⌋ + 2). It is easy to
check that Z(1, q2 ) is non-negative when q2 ∈ {1, . . . , 14} and if q2 ≥ 15 then
Z(1, q2 ) > .5 log2 (1 + q2 ) − 2 ≥ 0. Therefore Z(q1 , q2 ) ≥ 0 when q1 = 1.
   If q1 = 2 then Z(q1 , q2 ) = 4.5 log2 (1 + 2q2 ) − (4⌊log2 (q2 )⌋ + 6). It is easy to
check that Z(2, q2 ) is non-negative when q2 ∈ {1, . . . , 7} and if q2 ≥ 8 then

                Z(2, q2 ) =       4.5 log2 (1 + 2q2 ) − (4⌊log2 (q2 )⌋ + 6)
                          >       4.5(log2 (q2 ) + 1) − (4⌊log2 (q2 )⌋ + 6)
                           ≥      .5 log2 (q2 ) − 1.5
                           ≥      0

Therefore Z(q1 , q2 ) ≥ 0 when q1 = 2.
    Thus Z(q1 , q2 ) ≥ 0 and we have that t(p− q1 x, x− q2 (p− q1 x)) > 4.5 log2 (p−
q1 x). This contradict the minimality of r and thus the existence of (p, x). There-
fore the lemma holds.                                                              ✷

   Note that t(4, 1) = 9 = 4.5 log2 (p) and thus the bound is tight. It is also
worth noting that t(2, 1) = 5 = 5 log2 (p) which is why the requirement p > 2
was included in the lemma.


References
 [1] P. Shor, Algorithms for Quantum Computation: Discrete Logarithms and
     Factoring, Proc. 35th Annual Symposium on Foundations of Computer
     Science. IEEE Press, pp 124-134, Nov. 1994, quant-ph/9508027
 [2] J. Pollard, Factoring with cubic integers, in The Development of the Number
     Field Sieve, Vol. 1554 of Lecture Notes in Math. (1993)

                                              32
 [3] J. Pollard, BIT 15 (1975), p.331, also Knuth [21], Vol. 2, p.385
 [4] S. Beauregard, Circuit for Shor’s algorithm using 2n+3 qubits, quant-
     ph/0205095
 [5] Ch. Zalka, Fast versions of Shor’s quantum factoring algorithm, quant-
     ph/9806084
 [6] ANSI X9.62, Public key cryptography for the financial services industry -
     the Elliptic Curve Digital Signature Algorithm (ECDSA), January 1999
 [7] IEEE P1363, Standard Specifications for Public-Key Cryptography, Febru-
     ary 2000
 [8] US standard FIPS 186-2 (curves are in appendix 6) see e.g.
     http://csrc.nist.gov/encryption/dss/fr000215.html
 [9] M. Ettinger and P. Hoyer, On Quantum Algorithms for Noncommutative
     Hidden Subgroups, quant-ph/9807029
[10] R. Jozsa, Quantum Algorithms and the Fourier Transform, Proc. R. Soc.
     Lond. A (1998) 454, pp.323-337, (also quant-ph/9707033)
[11] A.Yu. Kitaev, Quantum measurements and the Abelian Stabilizer Problem,
     quant-ph/9511026
[12] S.C. Pohlig and M.E. Hellman, An improved algorithm for computing log-
     arithms over GF (p) and its cryptographic significance, IEEE Transactions
     on Information Theory, 24 (1978), 106-110.
[13] S. Hallgren and L. Hales, An Improved Quantum Fourier Trans-
     form Algorithm and Applications, FOCS 2000, (also available at
     http://www.cs.caltech.edu/~hallgren/)
[14] J. Chahal, Topics in Number Theory, Plenum Press, New York, 1988
[15] N. Koblitz, A Course in Number Theory and Cryptography, Springer-
     Verlag, New York, 1994.
[16] A. Menezes, Elliptic Curve Public Key Cryptosystems, Kluwer Academic
     Publishers, Boston, 1993.
[17] R. Cleve et. al., Quantum Algorithms revisited, Proc. R. Soc. Lond. A
     (1998) 454, p.339, (also quant-ph/9708016)
[18] R.B. Griffiths and C.-S. Niu Semiclassical Fourier Transform for Quan-
     tum Computation, Phys.Rev.Lett. 76 (1996) pp.3228-3231 (also quant-
     ph/9511007)
[19] V. Vedral, A. Barenco and A. Ekert, Quantum Networks for Elementary
     Arithmetic Operations, quant-ph/9511018


                                      33
[20] H. Cohen, A Course in Computational Algebraic Number Theory, Springer-
     Verlag, Berlin, 1993.
[21] D. Knuth, The Art of Computer Programming, Volumes 1-3, Addison-
     Wesley 1998
[22] Eric Bach and Jeffery Shallit, Algorithmic Number Theory, MIT Press,
     1996.
[23] H. Heilbronn, On the average length of a class of finite continued fraction,
     in Number Theory and Analysis (Papers in Honor of Edmund Landau),
     pp. 87-96, Plenum, New York, 1969.
[24] T. Draper, Addition on a Quantum Computer, quant-ph/0008033
[25] NIST, Revised draft of Key Management Guideline,
     http://csrc.nist.gov/encryption/kms/
[26] see http://www.rsasecurity.com/rsalabs/challenges/index.html
[27] see http://www.certicom.com/research/ecc_challenge.html




                                       34
