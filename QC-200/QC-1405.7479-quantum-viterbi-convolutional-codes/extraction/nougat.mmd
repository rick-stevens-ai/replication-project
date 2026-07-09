arXiv:1405.7479v2 [quant-ph] 20 Jun 2015

A QUANTUM ALGORITHM FOR VITERBI DECODING
OF CLASSICAL CONVOLUTIONAL CODES
JON R. GRICE AND DAVID A. MEYER
Abstract. We present a quantum Viterbi algorithm (QVA) with better than classical performance under certain conditions. In this paper
the proposed algorithm is applied to decoding classical convolutional
codes, for instance; large constraint length Q and short decode frames
N . Other applications of the classical Viterbi algorithm where Q is
large (e.g. speech processing) could experience significant speedup with
the QVA. The QVA exploits the fact that the decoding trellis is similar
to the butterfly diagram of the fast Fourier transform, with its corresponding fast quantum algorithm. The tensor-product structure of the
butterfly diagram corresponds to a quantum superposition that we show
can be efficiently prepared. The quantum speedup is possible because
the performance of the QVA depends on the fanout (number of possible
transitions from any given state in the hidden Markov model) which is
in general much less than Q. The QVA constructs a superposition of
states which correspond to all legal paths through the decoding lattice,
with phase a function of the probability of the path being taken given received data. A specialized amplitude amplification procedure is applied
one or more times to recover a superposition where the most probable
path has a high probability of being measured.

1. Introduction
In his 1971 paper on the Viterbi Algorithm (VA), Forney [8] noted that
“Many readers will have noticed that the trellis reminds them of the computational flow diagram of the fast Fourier transform (FFT). In fact, it is
identical, except for length, and indeed the FFT is also ordinarily organized
cellwise. While the add-and-compare computations of the VA are unlike
those involved in the FFT, some of the memory-organization tricks developed for the FFT may be expected to be equally useful here.”
The celebrated quantum Fourier transform [6], [5] uses tensor-product
structure to achieve its increase in efficiency over its classical counterpart,
and so in this paper we propose a quantum Viterbi algorithm (QVA) taking advantage of the tensor-product structure of the trellis that in certain
applications may outperform the (classical) VA.
Amongst many other applications, the VA [18] is useful in the decoding of
convolutional codes. Thus, in this paper we will demonstrate the application
Date: June 23, 2015.
1

2

JON R. GRICE AND DAVID A. MEYER

of a quantum algorithm to decoding classical convolutional codes. Quantum algorithms for decoding simplex codes [2], more generally Reed-Muller
codes [12] have been proposed and show improvements over the classical
algorithms. Protecting quantum information with convolutional encoding
has been discussed in [4, 14]. Applying Grover’s algorithm to the decoding
of convolutional codes has been demonstrated in [11], which shares some
superficial features to the QVA in this paper.
For a finite alphabet Q, the VA [8] is a way to find the most likely sequence
of states π ∗ ∈ QN that a hidden Markov model (HMM) transitions through
given a set of observations Z, called emissions. The maximum number of
paths branching away from a given state in a single step of the process will
be defined to be the fanout F .
A single iteration of the QVA will be shown to have gate complexity
O(N |Q|F (log F )2 ) and time complexity O(N log F ), if |Q| quantum systems
can be manipulated simultaneously.
Even if F is not considerably smaller than |Q|, the gates involving the |Q|
complexity factor can be performed in parallel. However F is often a fixed
number within a family of HMMs indexed by size |Q|, for example a large
graph (|Q|2 very large) where every node is connected to a few (F ) of its
neighbors. k-order HMMs can be recast into a first order HMM with large
|Q| and typically low F .
The first step of the QVA is to prepare a lattice of paths through the
HMM with each path corresponding to a quantum state. The states can
be preloaded with probability amplitudes at the same time in some variants
of the QVA. Then the phases of the states are marked with a function
depending on the probability of the path occurring. This can also be done
simultaneously with the lattice building and take advantage of the tensorproduct structure of the lattice. Finally a function-optimization algorithm is
called to extract the path probabilities from the relative phases of the paths
and convert them to probability amplitudes. In this paper, the optimization
algorithm is a variant of amplitude amplification. The phase marking step
and the amplification step can be repeated some number of times to make
the most probable path more likely to be observed, and we will call those
steps together an iteration of the algorithm.
√
The number of iterations in general can be up to O( L) as in Grover’s
algorithm [1], where here L = N F log F . This means that in addition to the
parallelism in |Q|, the QVA can be used with advantage when F is smaller
than |Q| and when the number of amplification steps required is low (e.g.
short decoding frames).
The convolutional codes defined below were chosen as a concrete and familiar example, rather than the most appropriate to the algorithm. On the
other hand, their code lattice has a low ‘fanout’ F and hence showcases the
QVA’s superior performance in |Q|. If using the maximal amount
of par√
N
allelism, the QVA decodes the convolutional code in time O( F N log F ).
One can see the advantage is most apparent for F ≪ Q and for short decode

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
3

frames N . Some general HMMs with absorbing states will also show similar
advantages.
In some applications of the QVA multiple trials need to be performed.
That is, the problem is set up and the algorithm is iterated the proper number of times, the output is measured and stored, and the process is repeated
to accumulate classical statistical data. These trials can be performed in
parallel. For decoding the convolutional codes in this paper, the number of
trials needed depends on the number of errors to be corrected.
We also analyze a variant of the QVA (the probabilistic QVA) in section
3.1 with multiple trials and no iterations - the probability amplitudes are
loaded into the paths during the lattice building step. The probability of
selecting the wrong answer (not finding the mode) falls exponentially in the
number of trials. There are applications where using the probabilistic QVA
is advantageous – but for decoding it seems that the QVA gives square root
better performance than the probabilistic QVA.
The first key idea of the QVA is to represent a particular path through the
lattice, say π = π1 π2 · · · πN as the quantum state |π1 π2 · · · πN i, where each
|πi i ∈ CQ . This algorithm is a parallel algorithm; all of the approximately
CF admissible paths exist in superposition with equal amplitudes and with
phases according to their probabilities as the algorithm builds the lattice.
So the following lattice (here Q = {0, 1, 2})
0•
1•
2•

p0,0
p0,2

0•
1•
2•

p0,0
p0,2
p2,1
p2,2

0•
1•
2•

is represented by the unnormalized quantum state
|ψ2 i = eif (p0,0 )f (p0,0 ) |000i + eif (p0,0 )f (p0,2 ) |002i
(1)

+ eif (p0,2 )f (p2,1 ) |021i + eif (p0,2 )f (p2,2 ) |022i,

where f is some strictly increasing function (for example, the logarithm).
We will call the operation that builds the lattice Hφ and the operation that
marks the states Gφ .
We will write F N the space of paths π that are admissible given a sequence
of emissions, so that |F N | ≈ F N .
The second key idea is to use a variant of amplitude amplification to shift
the phases from the states into their amplitudes. By analogy to Grover’s algorithm and to Gφ , we will call this step GF N . This procedure is reminiscent
of both the Grover-based function minimization algorithms [7] and the multiphase kickback scheme of Meyer and Pommersheim [10]. Multiplying (1)
by a global phase so that the most probable state (having the largest of the
f (pi,j pj,k )) has phase −1 gives lesser probable states a phase closer to 1 if the
monotonic function f is chosen correctly. For decoding convolutional codes

4

JON R. GRICE AND DAVID A. MEYER

this function corresponds to the number of errors that must have occurred
for that path to have been taken. In many cases, amplitude amplification
still works even though the
√ ‘unmarked’ states do not have phase equal to 1.
This can take up to π/4 L lattice building and amplifications steps, where
L = F N is the number of states to search, as in Grover’s algorithm, but in
the cases we will discuss below it may be fewer.
2. The Algorithm
As mentioned in the introduction, the algorithm first builds a quantum
state, each step adding a tensor factor sequentially in the forward direction.
2.1. The building blocks of Hφ and Gφ . We start with an HMM of |Q|
states, where the state at time step 1 ≤ n ≤ N is written xn , but is hidden;
instead an emission yn ∈ Z is made visible by the HMM at the time the
transition from xn to xn+1 is made. The probability of the transition is
written
P (i, j|y) = Pr(xn+1 = j|xn = i, yn = y),
with emission probabilities
P (y|i, j) = Pr(yn = y|xn+1 = j, xn = i).
We also let
Pi,j (y) = P (i, j|y)P (y|i, j),
and clearly we have
(2)

Q
X

P (i, j|y) = 1 for all y.

j=1

If the additional condition
X
Pi,j (y) = 1 for all i, y
(3)
j

holds, then the transition probabilities could be stored in the state amplitudes instead of the phases, which would allow an algorithm bypassing the
amplification step. HMMs that have this condition (3) however, are quite
uncommon.
P
The unnormalized state |ψk,y i = j eif (pk,j (y)) |ji represents a transition
from state k to state j given y, with F or fewer computational basis states in
superposition. The Hφ Gφ block links these transitions together into paths
whose total phase corresponds to the probability of the path being taken.
For a state |ψi, let Uψ be some unitary operation such that Uψ : |0i → |ψi.
There are many possible operators which satisfy that requirement, with a
canonical (but generally nonoptimal) choice being given in section 2.3.

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
5

The controlled operation which is active on the input pattern being |ψc i =
|ki, implementing some unitary operation U : CQ → CQ will be denoted
(4)

|ψc i /

k

|ψt i /

U

That is, the above controlled operation takes |ki|ψt i to |kiU |ψt i, extended
by linearity, and acts as the identity on all |ji|ψi for j 6= k.
For example, if Q = 2 then the gate
1
U|1i
is the standard two-qubit controlled not gate [13], up to relative phase, since
for a 2 × 2 unitary U|1i : |0i → |1i forces U|1i : |1i → α|0i.
We will let the gate
(5)

/

Vy
/
stand for the string of controlled operations:
/

0

1

2

···

Q

/

U|ψ0,y i

U|ψ1,y i

U|ψ2,y i

···

U|ψQ,y i

One can see that the matrix representation of the unitary operator Vy :
CQ ⊗ CQ → CQ ⊗ CQ in the computational basis is block diagonal with the
U|ψi,y i for the blocks.
2.2. The Gφ step. Given an initial distribution |ψ0 i and sequence of emissions {yi }N
i=1 perform
(6)

|ψ0 i
|0i
|0i
|0i
..
.
|0i

Vy 1
Vy 2
Vy3

···
···

VyN−1

Vy N
|0i
where the slashes denoting bundles of quantum wires are omitted for clarity.
This construction of Gφ implements N of the Vy blocks, each of which are
composed of Q controlled operations, for a gate complexity of O(N QF (log F )2 ).
The gate complexity can be improved by considering Gφ as sequence of F N
commuting Grover marking operators Gπ , for each π ∈ F N , restricted to

6

JON R. GRICE AND DAVID A. MEYER
Q

the subspace corresponding to F N and marking with a phase of ei j f (πj )
instead of −1. Each Grover operator can be implemented with gate complexity log(F N ) [20], the product of which is preceded by an operation HF N
which builds an equal superposition of states in F N . The Grover inversion
restricted to F N ,
X
1
|πihπ|,
GF N = I − √
F N π∈F N
and the operation HF N can also be implemented with log(F N ) gates. A concrete, but less efficient construction of GF N follows the procedure outlined
above for Gφ .
Each of the Vy are implicitly classically controlled, conditional on the
emissions which is the code as received. To show that the construction (6)
implements Gφ we have:
Proposition 1. Fixing a set of emissions {yi }, The state of the system
after one execution of (6) is
X Q
(7)
|ψf i =
ei j f (πj ) |πi,
π∈F N

where

Q

j πj is the probability of the path π ∈ Q

N being taken.

Proof. Assume the assertion is true for N − 1 steps, so
X Q
|ψN −1 i =
ei j f (πj ) |π1 π2 · · · πN −1 i,
π

with the sum over all possible paths π of length N − 1, and then apply the
gate
|xi
|0i

Vy N

with the last qubit of |ψN −1 i being fed into the wire marked with |xi. The
output of that operation will be
X i QN−1 f (π )
j
|ψN i =
e j=1
|π1 π2 · · · πN −2 i|ψi,yN i
i s.t.
πN−1 =i

=

X

i s.t.
πN−1 =i

X

j s.t.
πN =j

ei

QN−1
j=1

f (πj )

|π1 π2 · · · πN −2 ii|jieif (Pi,j (yN ))

= |ψf i.
The base case follows from the definition: If π1 is the path from i to j (given
y1 ), then π1 = Pi,j (y1 ).


A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
7

2.3. Implementation of a canonical unitary Uψ . The classically controlled operation HF N is built up from quantum controlled Uψ gates where
|ψi is a superposition of quantum states representing the fanout of a state
P2q
in the HMM. For q = log |Q| and if |ψi =
i=1 ψi |ii, with K of the ψi
nonzero, we call K the fanout of the state, and hence the maximum K for
all the ψ derived from the HMM transitions is F , the fanout of the HMM.
When every state has the same fanout equal to F , |ψi is always an equal
superposition. Otherwise, there are cases when Uψ must take |0i to some
|ψi ∈ RK+1 .
For binary convolutional codes defined in section 3, with k the number
of bits in the message block, F = 2k , the number of possible states that the
encoder can transition to given a new message block entering the encoder.
For the codes in that section, Q can be made arbitrarily large (while F
remains fixed) by increasing the constraint length.
Now we construct the sub-block Uψ from basic gates, in particular


cos 2θ − sin θ2
,
Ry (θ) =
sin θ2 cos θ2
and then use generalized Toffoli gates to construct the controlled operations
in Vy . The following method is similar to that in [13].
If Ry,a,b is the two-level unitary acting nontrivially on the subspace spanned
by |ai, |bi then constructing a unitary matrix R with specified first column
|φi will give R : |0i → |φi.
For some 2 × 2 unitary matrix W , we write W{|ai,|bi} for the two-level
unitary operator which acts as W on the subspace spanned by {|ai, |bi} and
as the identity elsewhere. That is,
W{|ai,|bi} |ai = (W )1,1 |ai + (W )1,2 |bi,

W{|ai,|bi} |bi = (W )2,1 |ai + (W )2,2 |bi and

W{|ai,|bi} |ψi = |ψi,

for |ψi not in the span of {|ai, |bi}. Let

cos 2θ
Ry (θ) =
sin θ2

− sin θ2
cos θ2



be the y-rotation operator, or the exponentiated Y gate. If the context is
clear we will also write
√


t
− 1 − t2
√
(8)
Ry (t) =
.
1 − t2
t
We claim that the first column of
V := Ry (θ1 ){|0i,|1i} Ry (θ2 ){|0i,|2i} · · · Ry (θN ){|0i,|N i}

8

JON R. GRICE AND DAVID A. MEYER

in the computational basis is the vector


cos(θ1 ) cos(θ2 ) · · · cos(θK )
cos(θ2 ) cos(θ3 ) · · · cos(θK ) sin(θ1 )


cos(θ3 ) cos(θ4 ) · · · cos(θK ) sin(θ2 )


(9)

,
..


.


 cos(θK−1 ) cos(θK−2 ) sin(θK−1 ) 
cos(θK ) sin(θK )
which is equivalent to spherical coordinates in RK+1 . Thus we have constructed a gate
V : |0i → |ψi
for any |ψi ∈ RK+1 , which is sufficient for our purposes. To see that this is
true, assume that a product of k Ry matrices has the block form


0
k

.. 
Y

. 
Ry (θj ){|0i,|ji} =  ~a
 ⊕ IK−1−(k+1) .

0 
j=1
0 0 0···0 0 1

A

Since Ry (θk+1 ){|0i,|k+1i} has the matrix form


cos(θk+1 ) 0 · · ·
0 − sin(θk+1 )


0
1 0 ···
0

 ⊕ IK−1−(k+1) ,


0
0 1
0
0
sin(θk+1 ) 0 0 · · ·
cos(θk+1 )
we find the product






′

A′′ 
Ry (θj ){|0i,|ji} =  cos(θj+1 )~a
 ⊕ IK−1−(k+1) .


j=1
′′′
sin(θj+1 ) 0 0 · · · 0 0 A
k
Y

A

Thus using the base case: ~a = (cos θ1 , sin θ1 ) and the recursion for ~a we get
(9). Therefore it requires K (F ) rotation operators Ry to implement V in
addition to the logic to change the subspaces that the Ry act on. Using the
Gray coding technique for the universal construction of quantum gates [13],
the subspace changing logic requires f 2 2f , (where F = 2f ) operations per
V , or F (log F )2 ). One can obtain even better results in the combinatorial
control logic by exploiting the special structure of V , but we will not need
them here.
In the first amplification step of a trial we can combine HF N with Gφ by
interlacing phase rotation operators eiZtj with the two-level unitaries Ry,a,b
above. To implement the classically controlled Gφ separate from HF N as
needed for subsequent amplification steps in the trial, a similar procedure
to the above is implemented, using the same Toffoli combinatorial logic.

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
9

3. Decoding a rate 1/2 convolutional code
An (n, k)-convolutional code [3] is a trellis code, which divides a datastream into message blocks of length k and encodes them into code blocks
of length n. We will limit our discussion to binary convolutional codes, in
which the datastream is a string of bits. An encoder can be defined by its
generator matrix G(x), a k by n matrix of polynomials in Z2 [x]. If the
encoder has a memory of the previous m blocks, the generator polynomials
have degree m at most. The following diagram represents an encoder for a
(2, 1)-convolutional code with m = 2.
(10)

⊕
•

d

1

2

⊕

⊕

O0

O1

The datastream is split into single bits and enters the encoder at the symbol
d. At each discrete timestep the bit at d is shifted right to the memory cell
labeled 1 , and the previous contents of 1 are shifted into 2 . The contents
of 2 are then discarded. The outputs O1 and O2 are formed by the various
sums (in the field Z2 ) of memory contents and d. The generator matrix for
encoder (10) is
G(x) = [1 + x2

1 + x + x2 ],

where the power of x represents the time delay on the bit. Presumably
the code words pass through a noisy channel and are received as receive
blocks by the decoder. Since the sequence of states (shift register contents)
in the encoder can be modeled by an HMM, the classical VA can be used
to implement the decoder module by tracing the most probable sequence of
states for the encoder given the sequence of receive blocks.
The state diagram for the code generated by (10) is
0/00

00

1/11

1/10

1/00
0/11

01

10

0/01
0/10

11
1/01

where the states are the boxed memory contents of the shift registers in the
encoder. The transition to the next state is an arrow labeled by i/o0 o1 ,
where i is the message bit and o0 o1 are the code bits.

10

JON R. GRICE AND DAVID A. MEYER

To implement the algorithm, we consider a lattice segment representing
the reception of the codeword 00:
(11)

p00

00

p01

01

p10

10

p11

11

with arrows representing
0 errors

, with phase rotation p0 ,

1 error

, with phase rotation p1 ,

2 errors

, with phase rotation p2 ,

occurring in the channel. The phase rotation p = eiω will be chosen so that
there is a high probability of observing the most probable path after a fixed
number of amplification steps. The idea is to make the paths with the fewest
errors have a relative phase which is close to −1 while the less likely paths
are made to have relative phase close to 1. Under such circumstances, one
would expect the algorithm to behave like a slightly noisy Grover search
algorithm with the marked state being the most probable path.
For example, take N = 4, so we have Q = (C2 )4 but we only need to
search F N = C4 . Supposing that no errors have occurred, the diagonal of
Gφ looks like a permutation of
gφ = (p0 , p2 , p3 , p3 , p3 , p4 , p4 , p4 , p4 , p4 , p5 , p5 , p5 , p5 , p6 , p7 ),
where the permutation would be the identity in this case if the most probable
√
path is |0000i. Setting ω = 0.68 and amplifying three times (≈ π/4 24 )
gives the state
(−0.76 + 0.29i)|0000i + (0.16 − 0.05i)|0001i + · · · + (0.37 − 0.04i)|1111i,
giving answer |0000i upon measurement with probability Pr0 = 0.673.
The optimal phase ω ∗ varies with N as the following table shows:
3
4
5
6
7
8
9
10
N
iterations
2
3
5
7
9
13
19
25
ω∗
0.84 0.68 0.61 0.51 0.44 0.39 0.35 0.31
Pr0
0.73 0.67 0.73 0.76 0.76 0.79 0.82 0.73
√
The amplitude of the most probable state after approximately π/4 F N
iterations is a weighted sum of exponentials in independent variable ω with
high frequency components increasing with N . One can gain intuition into
choosing a good value for ω by looking at the phase difference between the
most probable state and the second most; it appears like damped oscillation.

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
11

To get the most phase difference we want the maximum negative excursion.
This must occur at the first local minimum. The oscillation frequency increases as the higher order terms are added so ω ∗ must decrease with N .
Now suppose that one error has occurred. The diagonal of Gφ will look
like a permutation of
gφ1 = (p1 , p2 , p3 , p3 , p3 , p3 , p4 , p4 , p4 , p4 , p4 , p5 , p5 , p5 , p6 , p8 )
or
gφ2 = (p1 , p3 , p3 , p3 , p3 , p4 , p4 , p4 , p4 , p4 , p4 , p5 , p5 , p5 , p6 , p6 )
or one of four other similar vectors, depending on where the error occurred.
For these vectors, the maximal chance of success of observing |0000i tends
to occur at an ω closer to 1 than for the zero error case gφ . We will say that
gφ and {gφ1 , gφ2 } belong to different error classes. Similarly, for two errors,
the task of distinguishing vectors like
gφ3 = (p2 , p2 , p2 , p2 , p3 , p3 , p3 , p4 , p4 , p5 , p5 , p5 , p5 , p6 , p6 , p7 )
is performed optimally for different ω and number of iterations. There are
several ways to proceed in order to optimize the success of the algorithm for
a given maximum number of errors corrected. One is the ‘detune’ ω; driving
ω to a value closer to 0 makes the probabilities of the possible paths closer to
one another. The path probabilities are separated in different proportions
as one changes the number of iterations, which is possible another way to
find a compromise between the error classes.
We feel the best procedure is to adopt a sort of adaptive algorithm. For
the first few trials (the number of trials needed is discussed below) ω is
close to optimal for finding the paths corresponding to the most probable
number of errors. If after those trials the expected mode is not achieved, ω
is changed to correspond to the next most probable set of errors, and so on.
Note that this procedure will introduce time complexity factor according to
the number of probability classes. Hence for these convolutional codes, this
factor depends the maximum number of errors to be corrected.
We can convert (11) to a unitary operation V00 (5) using the representation as was obtained in (1). The operation V00 then must map the following:
1
|00i|00i 7−→ √ |00i(ei0 |00i + e2iω |01i)
2
1
|01i|00i 7−→ √ |01i(e2iω |00i + ei0 |01i)
2
1
|10i|00i 7−→ √ |10i(eiω |01i + eiω |11i)
2
1
|11i|00i 7−→ √ |11i(eiω |01i + eiω |11i)
2

12

JON R. GRICE AND DAVID A. MEYER

which can be implemented by the following quantum circuit:
(12)

•
H
H

•

•

•

•

eiω

Rz (ω)

using the definition (8).
Notice that the two Hadamard gates implement a block of HF N (and
hence are only called in the first iteration) while
the remaining gates im
1 0
and the gate eiω =
plement a block of Gφ . The gate Rz (ω) =
iω
0
e
 iω

e
0
. Essentially the same operations are implemented in V01 , V10
0 eiω
and V11 .
3.1. Trial reduction via amplitude amplification. When condition (3)
holds, or by suitable choice of f , the results of section 2.3 can be used to
put the probabilities of the paths into the amplitudes of the corresponding
state. Thus with a single iteration of the algorithm the most probable path
is most likely to be observed. One may ask if this probabilistic version of
the QVA might be preferred over having to repeatedly apply the amplitude
amplitication iteration. The lemma below will tell us that for these convolutional codes, O(F N ) trials of one iteration are needed √
to have a good chance
of finding the most probable path, in contrast to O( F N ) iterations with
O(1) trials for the QVA.
The trials for the probalistic QVA can be performed in parallel on an
ensemble of r quantum systems each containing Q qubits. After performing
the measurement step, we get S samples of size QN . Finding the most
probable event is an instance of the multinomial selection problem [16]. We
use the following lemma from [9]:
Lemma 1. Consider a collection of numbers with sum one. Denote the
largest b and the next largest by b′ . Carry out r runs in the corresponding probability distribution and denote by κ(r) the probability that the most
frequent outcome is not the most probable (i.e. the b-outcome). Then the
following limit exists:
(b − b′ )2
− log κ(r)
=λ=
.
r→∞
r
2[b(1 − (b − b′ ))2 + b′ (1 + (b − b′ )2 )]
lim

Hence κ(r) → 0 as e−λr .
When no errors have occurred in the channel, b = E0N and b′ = E1 E0N −1 ,
for E0 an appropriate value chosen for no error occurring in a particular

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
13

code word and E1 a value chosen for one error. Then
λ=

1 E0N
.
2 6 − E0N

it is decided, for example, that a decode error probability of e−2 ≈ 0.13 is
acceptable, then we have

or

0.8N
4
= ,
N
6 − 0.8
r
r ∼ 24(1.25)N − 4,

if E0 = 0.8. A similar procedure is used when collecting the results from the
trials of the QVA. Each r trials are performed in parallel and then measured
giving an array of length r of strings of length N log Q . The array is sorted
in rN log(Q) log(rN log Q) time and then the mode is extracted by scanning
the array[17].
The probabilistic QVA seems to be most naturally applied to problems
with a large Q and small N . When there is a path with probability close
to the most probable path, lots of extra trials are needed to separate those
out.
The general analysis of the QVA is difficult, but we can see if a single
iteration QVA behaves similarly to a single trial of the probabilistic QVA.
Let the diagonal of Gφ = (g0 , g1 , · · · , gL ), with the gi s roughly corresponding to the path probabilities and if we consider the amplitude of the
most probable path after a single application of Hφ Gφ and GF N , we get
PL−1 2
|g0 (L − 2) − 2 i=1
gi |
,
Pr0 =
3
L
2
2
since the first row of GF N is (− l−2
L , L , · · · , L ). Pr0 is maximal, of course,
when

(13)

L
X
gi ) = π + Arg(g0 ),
Arg(
i=1

which corresponds to Gφ = (−1, 1, · · · , 1), the standard Grover diagonal.
For L = 2N and with gi = 1 for i > 0, the probability of measuring a state
other than the most probable is then
1 − Pr0 =

(2N − 4)2
,
22N

which means that asymptotically a single iteration trial is only O(1) times
better than a random guess, which is correct with probability 1/2N . Thus
it is best to either use multiple iterations or to put the probabilities directly
into the amplitudes as when implementing the probabilistic QVA.

14

JON R. GRICE AND DAVID A. MEYER

4. Discussion
A possibility for an improved algorithm is to preload the amplitudes of the
states with a function depending on their probabilities using a Hφ modified
so that the system is already rotated near the desired state with amplitude
of |0i greater than the others and then apply some number of iterations of
Gφ GF N .
Further research is needed to determine if the optimization step of the
algorithm is optimal. Other interesting algorithms are possible using phase
kickbacks other than −1.
References
[1] L. K. Grover. A Fast Quantum Mechanical Algorithm for Database Search Proceedings, 28th Annual ACM Symposium on the Theory of Computing (STOC), 1996.
[2] Alexander Barg and Shiyu Zhou. A quantum decoding algorithm of the simplex code.
Proceedings of the 36th Annual Allerton Conference, 1998.
[3] Richard E. Blahut. Algebraic Codes for Data Transmission. Cambridge University
Press, 2003.
[4] H. F. Chau. Quantum convolutional error-correcting codes. Phys. Rev. A., 58, 1998.
[5] D. Coppersmith. An approximate Fourier transform useful in quantum factoring. IBM
Research Report RC 19642, 1994.
[6] D. Deutsch. Quantum theory, the Church-Turing principle and the universal quantum
computer. Proc. R. Soc. Lond. A, 400(97), 1985.
[7] C. Durr and P. Hoyer. A quantum algorithm for finding the minimum.
arxiv:9607014v2, 1996.
[8] G.D. Forney Jr. The Viterbi algorithm. Proceedings of the IEEE, 61(3):268–278, 1973.
[9] Robert Geroch. Perspectives in Computation, chapter 13, pages 100–101. The University of Chicago press, 2009.
[10] D. A. Meyer and J. Pommersheim. Single-query learning from Abelian and nonAbelian Hamming distance oracles. Chicago Journal of Theoretical Computer Science,
2010.
[11] J. Rahhal and D. Abu-Al-Nadi and M. Hawa. Evolutional Computation in Coded
Communications: An Implementation of Viterbi Algorithm IEEE Congress on Evolutionary Computation, 2007.
[12] Ashley Montanaro. The quantum query complexity of learning multilinear polynomials. Information Processing Letters, 112(11):438–442, 2012.
[13] Michael A. Nielsen and Issac I. Chuang. Quantum Computation and Quantum Information. Cambridge University Press, 2000.
[14] H. Ollivier and J.-P. Tillich. Description of a quantum convolutional code. Phys. Rev.
Lett., 91(177902), 2003.
[15] L. Rabiner. A tutorial on hidden Markov models and selected applications in speech
recognition. Proc. of the IEEE, 77(2), 1989.
[16] James Ramey and Khursheed Alam. A sequential procedure for selecting the most
probable multinomial event. Biometrika, 66(1):171–173, 1979.
[17] Steven Skiena. The Algorithm Design Manual. Springer, 2008.
[18] Andrew Viterbi. Error bounds for convolutional codes and an asyptotically optimal
decoding algorithm. IEEE Transactions on Information Theory, 13(2):260–269, 1967.
[19] Mark M. Wilde and Todd A. Brun. Entanglement-assisted quantum convolutional
coding. Physical Review A, 81(042333), 2010.
[20] M. Zubairy Z. Diao and G. Chen. A quantum circuit design for Grover’s algorithm.
Z. Naturforsch, (57a), 2002.

A QUANTUM ALGORITHM FOR VITERBI DECODING OF CLASSICAL CONVOLUTIONAL CODES
15

E-mail address: jgrice, dmeyer@math.ucsd.edu

