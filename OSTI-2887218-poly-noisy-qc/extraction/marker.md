                                          PHYSICAL REVIEW X 15, 041018 (2025)
   Featured in Physics




                      A Polynomial-Time Classical Algorithm for Noisy Quantum Circuits
                              Thomas Schuster ,1,* Chao Yin ,2,* Xun Gao ,2,3 and Norman Y. Yao4
                  1
                      Walter Burke Institute for Theoretical Physics and Institute for Quantum Information and Matter,
                                   California Institute of Technology, Pasadena, California 91125, USA
                                    2
                                      Department of Physics and Center for Theory of Quantum Matter,
                                            University of Colorado, Boulder, Colorado 80309, USA
                                       3
                                         JILA, University of Colorado, Boulder, Colorado 80309, USA
                           4
                            Department of Physics, Harvard University, Cambridge, Massachusetts 02138, USA

                (Received 29 October 2024; revised 3 April 2025; accepted 15 August 2025; published 3 November 2025)

                   We provide a polynomial-time classical algorithm for noisy quantum circuits. The algorithm computes
                the expectation value of any observable for any circuit, with a small average error over input states drawn
                from an ensemble (e.g., the computational basis). Our approach is based upon the intuition that noise
                exponentially damps nonlocal correlations relative to local correlations. This enables one to classically
                simulate a noisy quantum circuit by keeping track of only the dynamics of local quantum information. Our
                algorithm also enables sampling from the output distribution of a circuit in quasipolynomial time, so long
                as the distribution anticoncentrates. A number of implications are discussed, including a fundamental limit
                on the efficacy of noise mitigation strategies: For constant noise rates, any quantum circuit for which error
                mitigation succeeds in polynomial-time on most input states can also be classically simulated in
                polynomial-time on most input states. Our algorithms scale exponentially in the inverse noise rate, which
                is fundamental and makes them impractical for current quantum devices.
                DOI: 10.1103/xct1-7kf2                                   Subject Areas: Quantum Physics, Quantum Information



                        I. INTRODUCTION                                 access to a noiseless oracle [17], hardness results for
                                                                        sampling with extremely high precision [35,52] or error
   Quantum computers are believed to yield exponential
                                                                        detection [26,38,53], and classical algorithms for instanta-
computational advantages over their classical counterparts
                                                                        neous quantum polynomial (IQP) circuits [26,27] and
for certain tasks [1–4]. However, near-term quantum devices
                                                                        random quantum circuits [28–36]. To date, however, there
are inevitably impacted by noise. This raises a key question
                                                                        are few rigorous results on the computational power of
[5–51]: To what degree does noise fundamentally limit any
                                                                        general quantum circuits with low noise rates but without
quantum advantage over classical computation?
                                                                        error correction.
   The answer to this question is well understood in two
                                                                           In this work, we provide a classical algorithm for
limits. On the one hand, for noise rates above a large
                                                                        computing expectation values in any noisy quantum circuit
threshold, seminal works have shown that noisy quantum
                                                                        on most input states. The restriction to “most” input states is
circuits can be simulated classically [5–8]. On the other hand,
                                                                        fundamental, since for a fixed input state and a sufficiently
for sufficiently low noise rates, one can utilize quantum error
correction to perform fault-tolerant computation [9–12].                low noise rate, one can immediately perform quantum error
Nevertheless, the reality of modern quantum experiments                 correction. To this end, with a high probability over input
lies precisely in between these two limits: Noise rates are             states drawn from an ensemble, our algorithm succeeds in
small, but error correction is not typically employed.                  computing the expectation value of any observable (to
Progress in this intermediate regime has been restricted to             within small error) for any noisy quantum circuit. We
several relatively specific contexts: bounds on the circuit             emphasize that our restriction to ensembles of input states is
depth but not the complexity [13–16], tasks that assume                 relatively weak—a wide range of ensembles are allowed,
                                                                        including the computational basis states. The algorithm
                                                                        runs in either polynomial or quasipolynomial time, depend-
  *
      These authors contributed equally to this work.                   ing on the observable and noise model of interest.
                                                                           To compute the expectation value, our algorithm simulates
Published by the American Physical Society under the terms of           the Heisenberg time evolution of the observable in
the Creative Commons Attribution 4.0 International license.
Further distribution of this work must maintain attribution to          the Pauli basis. Building upon seminal recent algorithms
the author(s) and the published article’s title, journal citation,      for random quantum circuits [28–36] and many-body dynam-
and DOI.                                                                ics [46–51,54–59], the key insight underlying our algorithm is



2160-3308=25=15(4)=041018(31)                                    041018-1               Published by the American Physical Society
SCHUSTER, YIN, GAO, and YAO                                                                      PHYS. REV. X 15, 041018 (2025)

 (a)                            (b)                                                    (c)




FIG. 1. (a) Schematic of a noisy quantum circuit. The input state ρ is acted on by a circuit of arbitrary two-qubit gates (pink) and local
noise channels (dots), and concludes with measurement of an observable O. In the gate-based noise model, the noise acts on a qubit only
when a gate is performed (black dots). In the uniform noise model, even when the qubit is idle, noise can occur (dashed dots). (b) For
circuits with uniform noise, our classical algorithm decomposes the expectation value of O as a sum of Pauli paths. We depict each path
by a space-time grid, where each square denotes whether the path is the identity (white) or X, Y, or Z (red, yellow, or purple,
respectively) at that qubit and circuit layer. Our algorithm computes the sum of all low-weight paths (left), and truncates high-weight
paths (right) since they are strongly damped by noise (fading). (c) For circuits with gate-based noise, our algorithm instead simulates the
Heisenberg time evolution of O within the subspace of low-weight Pauli operators. That is, at each layer, we truncate all Pauli operators
with weight above a threshold l (dashed red line). The plot depicts the weight of various components of the time-evolved operator (blue
lines), as they are acted on by noise (fading) and, potentially, truncated by our algorithm (red scissors).


the close connection between sets of Pauli operators that are          noise channels. Here, d is the circuit depth, and t ¼ 1; …; d
hard to classically simulate and those that are strongly affected      indexes the circuit layers in reverse order. After the circuit
by noise. By carefully truncating such high-weight Pauli               is applied, we are interested in either computing the
operators, we achieve a provably efficient and accurate                expectation value of an observable O, trðCfρgOÞ, or
simulation. We emphasize that, despite the prevalence of               sampling from the outcomes when Cfρg is measured in
Pauli truncation methods for nearly six years to date [28], our        the computational basis.
work provides the first rigorous proof that such methods can              We consider two archetypal noise models [Fig. 1(a)]:
succeed for nonrandom circuits. This is enabled by substan-            uniform noise and gate-based noise. In the uniform noise
tially new proof techniques compared to any previous work.             case, every qubit is affected by noise at every circuit layer.
   Our results have wide-ranging consequences for quantum              That is, we take Dt ¼⊗nj¼1 Dj , where Dj fρg ¼ e−γ ρ þ
experiments. First, we show that, for noise rates that do not          ð1 − e−γ Þtrj ðρÞ is a local depolarizing channel of strength γ.
improve as the number of qubits increases, any strategy for            This noise model is relevant for many current experiments,
quantum error mitigation [60–62] can scale efficiently                 in which idle errors affect qubits even when they are not
[63–66] only for quantum circuits that are easy to classically         involved in gates. However, the uniform noise model
simulate. Like our main results, this statement holds for any          allows computation only up to a depth logarithmic in
quantum circuit on most input states. Second, we build upon            the number of qubits, after which the system is close to the
our results to construct a simple and strict test for whether a        maximally mixed state [13,68]. To this end, we also
given quantum circuit can exhibit quantum advantage. We find           consider the so-called gate-based noise model, in which
that any circuit exhibiting advantage on most input states must        qubits are affected by noise only when they participate in
be macroscopically sensitive to noise. Finally, we provide             nonidentity gates, Dt ¼⊗j ∈ Ut Dj . This model allows for
extensions of our algorithm to sampling from circuits with             “fresh qubits” unaffected by idle errors to be inserted at any
output distributions that anticoncentrate, as well as to comput-       circuit layer, which is the standard setting for proofs of
ing expectation values in random quantum circuits with                 fault-tolerant quantum computation [9–12,69]. In both
nonunital noise [36,67], which improves in both run-time               noise models, we incorporate readout noise by taking
and generality compared to existing algorithms [36].                   the final noise channel D0 to act on all qubits. Finally,
                                                                       although we focus on depolarizing noise for the sake of
  A. Classical algorithm for noisy quantum circuits                    simplicity, our results immediately generalize to any single-
  Consider a noisy quantum circuit on n qubits, of the form            qubit noise channel in the so-called depolarizing class. This
                                                                       includes both biased and inhomogeneous noise channels
        Cfρg ¼ D0 fU 1 D1 f…U d Dd fρgU†d …gU†1 g;             ð1Þ     (see Appendix F for further details).
                                                                          The central framework of our approach is the decom-
where ρ is the input state, U t are depth-1 unitaries of               position of the Heisenberg time-evolved observable O in
arbitrary two-qubit gates, and Dt are local depolarizing               the Pauli basis. Crucially, under uniform noise, a Pauli


                                                                041018-2
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                PHYS. REV. X 15, 041018 (2025)

TABLE I. Known results on the computational complexity of various classes of noisy quantum circuits, taking the standard limits
d; ε−1 ¼ polyðnÞ and γ −1 ¼ Oð1Þ. In the first three columns, expectation values are with respect to observables that are sums of
polynomially many Pauli operators; each run-time increases to quasipolynomial otherwise. In the final two columns, entries denote
hardness results arising from quantum error correction [9–13]. We use QNC  g 1 to denote the class of quantum circuits with depth
d ¼ Oðlog n=poly log log nÞ [13], which is just below logarithmic. We note that simpler classical simulations may be obtained for
circuits with specific depths [27] or geometric locality, as we show, for example, in Theorem E2.
                                                                                                              Any circuit,      Any circuit,
                                        Random          Any circuit, most            Any circuit, most         any input         any input
                      IQP circuits      circuits      inputs (uniform noise)        inputs (gate noise)     (uniform noise)     (gate noise)
Expectation             poly(n)         poly(n)             poly(n)                    quasipoly(n)             g1
                                                                                                               QNC                 BQP
values                 Ref. [26]      Refs. [28,31]        Theorem 1                    Theorem 2             Ref. [13]         Refs. [9–12]
Sampling (: with    quasipoly(n)*      poly(n)*          quasipoly(n)*               quasipoly(n)*                g1
                                                                                                             SampQNC             SampBQP
anticoncentration)     Ref. [26]        Ref. [31]         Theorem E1                  Theorem E1              Ref. [13]         Refs. [9–12]



operator P with weight w½P is damped by an amount                  techniques and insights that allow us to overcome the two
e−γw½P , where the weight w is defined as the number of            aforementioned challenges. As aforementioned, both of our
nonidentity elements in the operator. High-weight Pauli             algorithms apply to any noisy quantum circuit on most
operators are thus almost entirely damped by noise, while           input states. We term the allowed ensembles of input states
low-weight operators are less affected. Since there are only        low-average ensembles, which we define immediately
polynomially many, O(ð3nÞw =w!), low-weight operators,              following the theorems below.
this suggests that one might be able to efficiently approxi-           Theorem 1 (Polynomial-time algorithm for quantum
mate a time-evolved observable by only keeping track of             circuits with uniform noise). Consider any quantum circuit
such operators. This intuition has motivated a range of             C with local depolarizing noise of strength γ on each qubit
seminal algorithms for classically simulating noisy quan-           at each circuit layer, any normalized observable O, and a
tum circuits by truncating Pauli operators of high weight           low-average ensemble of states E ¼ fρg. Assume the Pauli
[26,28–34,45–50,54–59]. However, whether it is possible             coefficients of O and ρ can be efficiently computed. For
to turn this intuition into a rigorous classical algorithm for      circuits with uniform noise, there is a classical algorithm
general circuits has remained an essential open question.           that computes the expectation values, trðCfρgOÞ, in time:
   There are two challenges. First, although each individual
                                                                                                                     2
high-weight operator is strongly damped by noise, there                                polyðnÞ · ð1=εÞO(logð1=γÞ=γ ) ;                  ð2Þ
are, in principle, exponentially many such operators. To
address this, existing classical algorithms [28–35] utilize a       if O is a sum of polynomially many Paulis,
strongly simplifying property of random circuits: In a
                                                                                                                                  2
random circuit, different Pauli paths do not coherently                        nO( logð1=γÞ=γ)þO(logð1=εÞ=γd) · ð1=εÞO(logð1=γÞ=γ ) ;   ð3Þ
interfere on average [70]. This enables simple bounds on
the error associated to truncated paths. However, this              for any O, with root-mean-square error ε over the
property does not extend to general circuits. Second, for           ensemble E.
circuits with gate-based noise, the damping of each Pauli              Theorem 2 (Quasipolynomial time algorithm for
operator is given by wUt ½P, the number of nonidentity             quantum circuits with gate-based noise). For circuits
elements of P that are acted upon by gates in Ut .                  with gate-based depolarizing noise of strength γ, there
(Specifically, wUt ½P counts the number of qubits that are         is a classical algorithm that runs in quasipolynomial
both in the support of P and acted on by nonidentity gates in       time,
Ut .) However, a high-weight operator might be involved only                                         pﬃﬃﬃﬃﬃﬃ
in a small number of gates in any given circuit layer. Thus, in                     Oðd · nð1=γÞ logð dþ1=εÞ−1 Þ;       ð4Þ
combination with the first challenge, any rigorous approach
for bounding the truncation error must keep track of the            for any normalized O, with root-mean-square error ε over
history of operators across many circuit layers.                    the ensemble E.
   In what follows, we will begin by stating our main results          Before proceeding to our algorithms, a few brief com-
(Theorems 1 and 2; Table I). In particular, we provide one          ments are in order.
classical algorithm for circuits with uniform noise, which             First, we say that an observable O is normalized if
runs in polynomial time for a large class of observables, and       its normalized Frobenius norm is equal to one:
a second classical algorithm for circuits with gate-based           jjOjj2F ≡ ð1=2n ÞtrðO† OÞ ¼ 1. For example, this is true for
noise, which runs in quasipolynomial time. We will then             any Pauli operator. If an observable is not normalized, the
describe our algorithms, with a focus on delineating the key        errors ε can be simply rescaled by the observable’s norm.


                                                            041018-3
SCHUSTER, YIN, GAO, and YAO                                                                PHYS. REV. X 15, 041018 (2025)

ALGORITHM 1.                                                    ALGORITHM 2.

Classical algorithm for uniform noise                           Classical algorithm for gate-based noise
Input: State ρ, circuit C, observable O; threshold l            Input: State ρ, circuit C, observable O; threshold l
Output: Approximation of trðCfρgOÞ                              Output: Approximation of trðCfρgOÞ
                                     P
  1: Enumerate Pauli paths ⃗P with t w½Pt  ≤ l                   1: Initialize cP ¼ e−γw½P trðOPÞ=2n for w½P ≤ l
                                  Q ðtÞ                           2: for t ¼ 1 to d do
  2: Compute amplitudes cP   ⃗P ¼  t aPt−1 Pt                                                    P ðtÞ
                                                                  3: UpdateP  via cQ ← e−γwUt ½Q P aPQ · cP
              noise c ⃗P ← e−γ
     3: Apply P                  t
                                     w½Pt 
                                              · c ⃗P              4: return P cP trðρPÞ
     4: return P⃗ cP⃗ trðρPd Þ

                                                                with coefficients given by the transition amplitudes,
                                                                  ðtÞ
   Second, while our results apply to any noisy quantum         aPQ ¼ ð1=2n ÞtrðQU†t PU t Þ, at each layer t. Each path is
circuit, they still involve a small amount of randomness via    damped by a factor e−γw½ ⃗P due to noise, where w½P
                                                                P
                                                                                                                             ⃗ ¼
the ensemble of input states. In particular, our metric of
                                                                    t w½Pt  is the sum of the individual weights at each
success is the root-mean-square error ε over a low-average      circuit layer.
ensemble of quantum states, which we define as any                  In more detail, we can derive the above formula
ensemble, E ¼ fρg, whose mixtureP       is close to the max-    as follows. Prior to any time evolution, the observable
imally mixed state, jjð1=jEjÞ ρ ρjj∞ ≤ c=2n for any c ¼         O can
Oð1Þ (see Appendix B). As a simple example, any                        P be decomposed in the Pauli basis as
                                                                O ¼ P0 ð1=2n ÞtrðOP0 ÞP0 . This sets the “initial condition”
complete basis of pure states, such as the computational        for the Pauli path. Next, we can time evolve O through the
basis, forms a low-average ensemble (with c ¼ 1).               final circuit layer U 1. This produces the time-evolved operator,
Intuitively, our attention to average-case performance                        P
                                                                U1 OU†1 ¼ P0 trðOP0 ÞU1 P0 U †1 . As before, we can decom-
excludes quantum error correction because syndrome
qubits will be initialized randomly on average.                 pose this operator in the Pauli basis to find U1 OU†1 ¼
                                                                P P                                           †
                                                                         P1 ð1=2 ÞtrðOP0 Þ · ð1=2 ÞtrðP1 U 1 P0 U 1 Þ · P1 . Here
                                                                                 n                 n
Experiments with random input states are of significant             P0
                                                                 ð1Þ
interest in several settings, including in quantum learning     aP0 P1 ≡ ð1=2n ÞtrðP1 U†1 P0 U1 Þ is a transition amplitude from
[71,72] and quantum many-body dynamics [73–75].
                                                                the Pauli operator P0 to P1 under the first layer of the circuit.
   Third, if preferred, our bounds on the root-mean-square
                                                                Proceeding in this manner d times, we obtain Eq. (5), aside
error ε can be easily translated to probability bounds.
                                                                from the exponential factor involving γ.
That is, for any δ; ε̃, our algorithms succeed in computing
                                                                   To derive the exponential factor, we consider the
the expectation value trðCfρgOÞ to error ε̃ with high
                                                                behavior of the same circuit in the presence of local
probability 1 − δ over input states ρ drawn from E. This
                                                                depolarizing noise. As discussed earlier, the local depolariz-
follows immediately from Theorems 1 and 2pﬃﬃby an
                                                                ing noise channel has a very simple action in the Pauli basis,
application of Markov’s inequality, setting ε ¼ ε̃ δ. The       DfPg ¼ e−γw½P P. Applying this channel at each layer of the
run-time of the algorithms remains polynomial and quasi-        circuit above yields an additional overall multiplicative
polynomial, respectively, for any inverse polynomial ε̃ and
                                                                factor of e−γw½P0  e−γw½P1     e−γw½Pd  , which we abbreviate
δ. Hence, we say that our algorithms succeed on “most”                  ⃗
input states.                                                   as e−γw½P . This completes the derivation of Eq. (5).
                                                                   Our classical algorithm’s approximation for C† fOg is
     B. Classical algorithm for quantum circuits with           given by the sum over all Pauli paths with weight below a
                       uniform noise                            chosen threshold l, i.e., all P      ⃗ with w½P ⃗ ≤ l:
   Our algorithm for uniform noise (Algorithm 1) estimates                           X                      Y
                                                                                                             d               
the expectation value, trðCfρgOÞ ¼ trðρC† fOgÞ, by com-                     Õ ¼             e   −γw½ ⃗P          ðtÞ
                                                                                                                  aPt−1 Pt    Pd :   ð6Þ
puting an approximation Õ of the Heisenberg time-evolved                          ⃗P∶w½ ⃗P≤l              t¼1
observable C† fOg. This approximation is given by the sum
of all low-weight Pauli paths that contribute to C† fOg.        From this approximation, we estimate the expectation value
Here, a Pauli path P  ⃗ ¼ ðP0 ; …; Pd Þ is a sequence of        of interest as trðρÕÞ.
Pauli operators corresponding to each layer of the circuit         We hasten to emphasize that our algorithm is in fact
[Fig. 1(b)], and the exact time-evolved operator can            identical to those from random circuits [28,31]. To this end,
immediately be expressed as a sum over Pauli paths,             our ability to rigorously extend the algorithm to general
                                                                noisy quantum circuits owes to substantial improvements in
        X                           Y ðtÞ 
                                    d
            −γw½ ⃗P 1
                                                                a number of key proof techniques. In particular, to bound
 †
C fOg ¼   e         · n trðOP0 Þ ·      aPt−1 Pt · Pd ;   ð5Þ   the error in the expectation values, we first prove the
        ⃗
                     2              t¼1
             P                                                  following simple lemma.


                                                          041018-4
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                 PHYS. REV. X 15, 041018 (2025)

(a)                                               (b)




FIG. 2. (a) The Pauli tree framework used to prove Theorem 1, which groups Pauli paths according to their weight wt at each circuit
layer t. Our algorithm truncates paths with a summed weight above l. We group these truncations into ðldÞ individual truncations (red
scissors), which enables a tight bound on the algorithm’s error. In the example shown, the branchings at each node correspond to weights
w ¼ 1; …; 5 and we set l ¼ 6, d ¼ 2. (b) To prove Theorem 2, we analyze the flow of Pauli operators from one weight to another under
circuit gates. Here, each bubble depicts the set of Pauli operators of a given weight, and arrows indicate flow from one weight to another.
We show that this flow is lossy in the presence of gate-based noise, in the sense that a decrease −J in support at weight w can increase the
support at weight w þ 1 by at most e−2γ J. This leads to our bound on the cumulative operator weight distribution in Lemma 2.


   Lemma 1. Consider a low-average ensemble E ¼ fρg                     jδOðl − wd ; d − 1Þjj2F , since any Pauli path with weight
and two observables O and Õ. The root-mean-square                      wd at the final layer, and total weight above l, must have
difference between the expectation value of O and Õ is                 total weight above l − wd on the preceding layers (see
less than jjO − ÕjjF .                                                 Appendix C for details). Combined with the first equality,
   Thus, if we are able to bound the Frobenius norm of the              we see that the norm of high-weight Pauli paths at layer d is
sum of truncated Pauli paths, then we can bound the root-               bounded by a sum of analogous norms at layer d − 1.
mean-square error in our algorithm.                                         To complete our proof, we recursively apply this bound
   To bound the norm, we group the exponentially many                   down each layer of the Pauli tree. That is, we bound the
Pauli paths according to their weight at each circuit layer.            contribution of each top layer vertex ðwd Þ as a sum of
This organization is naturally viewed via a tree structure              contributions of vertices at the following layer, ðwd ; wd−1 Þ.
[Fig. 2(a)]. Each layer t of the tree corresponds to a layer of         Each such contribution arises from Pauli paths with weight
the quantum circuit, ordered from t ¼ d; …; 1. At every                 above l − wd − wd−1 on layers up to d − 2, and incurs an
layer, each vertex branches into up to n additional                     associated damping, e−2γðwd þwd−1 Þ . We then bound these
vertices, which correspond to Pauli paths with weight                   contributions in terms of vertices at the next layer,
wt ¼ 1; …; n at that layer. In this manner, each Pauli path             ðwd ; wd−1 ; wd−2 Þ, and so on. We haltPeach sequence of
⃗ is uniquely associated with a particular downward
P                                                                       recursions once the summed weight, dt0 ¼t wt0 , surpasses
sequence of vertices, ðwd Þ; ðwd ; wd−1 Þ; …; ðwd ; …; w0 Þ,            l − t; from here, one can directly bound the remaining
through the tree.                                                       contribution by e−2γðlþ1Þ, since every Pauli path from layer
   The key benefits of the Pauli tree are that (i) the paths            0 to t − 1 has weight at least t [76]. In effect, this recursive
associated   with each vertex are damped by at least                    process groups the truncated Pauli paths according to their
    P  d                                                                earliest subsequence of weights that sum to above l − t.
e−γ t0 ¼t wt0 due to noise and (ii) the tree organization
                                                                        Each grouping can be viewed as a single collective
naturally enables us to bound the norm of sums of Pauli
                                                                        truncation by the algorithm [Fig. 2(a)]. The total error of
paths, by using the orthogonality of Pauli operators at each
                                                                        the algorithm is determined by the number of such
circuit layer. We now outline how these properties enable a             truncations, which a simple counting argument shows is
tight bound on the error of Algorithm 2. Let δOðw; tÞ
                                                                        ðldÞ. This leads to a total error ðldÞe−2γðlþ1Þ. We refer to
denote the sum of all Pauli paths from layer 0 to t with
weight above w. We are interested in the Frobenius norm of              Appendix C for full details.
                                                                            From this error bound, we determine the run-time of
δOðl; dÞ ¼ C† fOg − Õ, which bounds the root-mean-
                                                                        Algorithm 1 by setting l ≈ γ −1 d þ γ −1 logð1=εÞ to achieve
square error of Algorithm 1 via Lemma 1. To analyze
                                                                        a desired error ε. For circuits with uniform noise, the
the Frobenius norm, we leverage properties (i) and
                                                                        maximum nontrivial depth is d ¼ O(γ −1 logð1=εÞ), since
(ii) above to decompose it as a sum of contributions
                                                                        after this depth, expectation values become ε-close to zero
from each weight P      wd at the final circuit layer,
                                                                        and the circuit can be trivially simulated [77]. The run-time
jjδOðl; dÞjj2F ¼ wd jjP wd fδOðl; dÞgjj2F , where P wd proj-            of our classical algorithm is determined by the number of
ects onto Pauli operators of weight wd . We can associate               Pauli paths with weight below l. This is upper bounded by
each term in the sum with a vertex ðwd Þ in the top layer               nl=d · 2OðlÞ for any O [31], and m · 2OðlÞ when O is a sum
of the Pauli tree. We can then bound the contribution                   of m Pauli operators (see Appendix C). Plugging in the
of each vertex as jjP wd fδOðl; dÞgjj2F ≤ e−2γwd j×                     above values of l and d yields Theorem 1.


                                                                041018-5
SCHUSTER, YIN, GAO, and YAO                                                                 PHYS. REV. X 15, 041018 (2025)

      C. Classical algorithm for quantum circuits                   remarkably subtle, due to processes wherein an operator
                 with gate-based noise                              component grows to high weight, then shrinks back to low
   Although Algorithm 1 is quite efficient for quantum              weight, and then grows to high weight again. Our focus on
circuits with uniform noise, where the depth d is at most           the flow of the operator norm allows us to simultaneously
logarithmic, this efficiency does not extend to circuits with       capture damping during the growth in operator weight,
gate-based noise, where the depth d may be large. In such           while avoiding overcounting due to shrinking and regrowth
circuits, the run-time of Algorithm 1 diverges exponentially        processes.
in d owing to the ðldÞ truncations.                                    In more detail, to quantify the norm of a time-evolved
                                                                    operator OðgÞ at weight w, we leverage an object of recent
   To address this, our algorithm for gate-based noise
                                                                    interest in many-body physics: the operator weight dis-
(Algorithm 2) performs only a single truncation at each
                                                                    tribution [78–81]:
circuit layer, of all Pauli operators with weight greater than
l. In particular, at each layer t we store an approximation of                                1
the time-evolved operator within the subspace of low-                            PðgÞ ðwÞ ¼      trðOðgÞ · P w fOðgÞ gÞ:         ð9Þ
                                                                                              2n
weight Pauli operators:
                                 X        ðtÞ
                                                                    Here, we track the evolution through each circuit gate g
                     ÕðtÞ ¼           c̃P P:                 ð7Þ   instead of each circuit layer t. In keeping with our intuition,
                               P∶w½P≤l                             we show that the weight distribution changes in a “local”
                                                                    manner when any unitary two-qubit gate g is applied,
The coefficients are updated from layer to layer via
standard Heisenberg time evolution:                                      PðgÞ ðwÞ ¼ Pðg−1Þ ðwÞ þ JðgÞ ðwÞ − JðgÞ ðw þ 1Þ;       ð10Þ
               ðtÞ
                                   X        ðtÞ   ðt−1Þ
              c̃Q ¼ e−γwUt ½Q            aPQ c̃P         :   ð8Þ   where JðgÞ ðwÞ measures the flow in operator norm from
                                 P∶w½P≤l                           weight w − 1 to w under g. The crucial insight of our proof
                                                                    is to show that this flow becomes lossy for quantum circuits
At the final circuit layer, we compute the expectation              with gate-based noise, in the sense that
value trðρÕðdÞ Þ.
   By performing only d þ 1 truncations in total, Algorithm 2       PðgÞ ðwÞ ≤ Pðg−1Þ ðwÞ
avoids the exponential blowup of Algorithm 1 at large depths.
                                                                               þ f1; e−2γ g · JðgÞ ðwÞ − f1; e−2γ g · JðgÞ ðw þ 1Þ;
In particular, if we denote the truncated operators at layer t as
                                                  P
δOðtÞ ≡ P >l fDt fU†t Õðt−1Þ Ut gg,whereP >l ¼ nw¼lþ1 P w ,                                                                    ð11Þ
                                               P
then we immediately have jjδOjj2F ≤ ðd þ 1Þ dt¼0 jjδOðtÞ jj2F
by the Cauchy-Schwarz inequality. The trade-off is a mod-           where the bound holds for any choices of the constants 1 or
erate increase in run-time compared to Algorithm 1 at the           e−2γ in each of the terms. The strongest bound is obtained
same value of l. In particular, Algorithm 2 performs d              by taking e−2γ when the term is positive, and 1 when
updates on Oðnl Þ low-weight Pauli coefficients, and thus has       negative. In the former case, the bound shows that increases
run-time Oðdnl Þ; see Appendix D for full details.                  in operator norm due to flows inward to weight w are
   The central difficulty in proving Theorem 2 is to bound          damped by e−2γ due to noise; in the latter case, decreases in
the truncation norms jjδOðtÞ jjF within the gate-based noise        the norm due to outward flows are not damped [Fig. 2(b)].
model. This would be straightforward within the uniform                To bound the truncation error, we apply Eq. (11) for
noise model, since a single application of uniform depola-          every circuit gate g and sum over weights w > l. The
rizing noise damps the norm of any operator with weight             currents between high weights cancel, and we find that the
                                                                    total norm above weight l is less than the net current from l
above l by at least e−γðlþ1Þ . However, as aforementioned, it                  P
is not clear whether such a bound applies to the gate-based         to l þ 1, g JðgÞ ðlÞ, damped by e−2γ. By bounding the norm
noise model, where the effect of noise can accumulate               in terms of the net current, we naturally avoid subtleties due to
gradually over many circuit layers.                                 shrinking and regrowth processes. Furthermore, the net
   To show that the bound indeed extends to circuits with           current from weight l to l þ 1 is necessarily bounded by
gate-based noise, our core idea is to track the flow of             the maximum norm at weight l. This is, by a similar
operator norm from one weight to another under each                 inequality, less than the net current from l − 1 to l damped
circuit gate [Fig. 2(b)]. Intuitively, each two-qubit gate can      e−2γ . Iterating l times, we find that the total norm above
transfer operator norm from a weight w to adjacent weights          weight l is less than e−2γðlþ1Þ for any circuit with gate-based
w  1. Thus, for a component of the operator to reach a             noise (see Appendix D for full details).
high weight, it must participate in a high number of circuit           Lemma 2 (Upper bound on weight distributions in
gates, and thereby accrue a large damping due to noise.             noisy quantum circuits). Consider the time evolution
Despite its simplicity, formalizing this intuition can be           OðgÞ of any normalized observable O in any quantum


                                                              041018-6
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                 PHYS. REV. X 15, 041018 (2025)




FIG. 3. Schematic of our results’ implications for quantum error mitigation. For concreteness, we depict a specific error mitigation
strategy, zero noise extrapolation, in which one measures an expectation value hOi for several different noise rates (orange lines), and
performs an extrapolation (green arrow and dashed line) to estimate the ideal expectation value (black line). (a) If error mitigation
succeeds in recovering the ideal expectation value, then the expectation value must be dominated by low-weight Pauli operators (green).
Thus, our classical algorithm can also compute the ideal expectation value. (b) On the other hand, if the ideal expectation value is hard to
compute classically, then it must contain contributions from high-weight Pauli operators (red). Error mitigation cannot capture these
contributions, since they are exponentially suppressed by noise. Thus, the extrapolated expectation value necessarily differs from the
ideal value (red arrows).


circuit with gate-based noise. The cumulative weight                       Corollary 1 (Lower bound on error mitigation). Given
distribution is less than                                               an ideal circuit C, Pauli observable O, and a low-average
                                                                        ensemble E ¼ fρg. Suppose an error mitigation strategy
                   X
                   ∞
                                                                        proceeds by measuring O on any set of noisy circuits
                            PðgÞ ðw0 Þ ≤ e−2γðwþ1Þ            ð12Þ      applied to ρ. For any ε ¼ 1=polyðnÞ, if error mitigation can
                  w0 ¼wþ1
                                                                        estimate trðCfρgOÞ to root-mean-square error ε=2 in
                                                                        polynomial time, there is a classical algorithm to compute
for all γ, w, t. This also holds if we replace OðgÞ with our
                                                                        trðCfρgOÞ to root-mean-square error ε in polynomial time.
classical approximation ÕðgÞ .                                            The reason is simple. If mitigation can recover an ideal
   Applying the lemma Algorithm 2, we find that the total               expectation value from noisy circuits, then one can also
                                        −2γðlþ1Þ . Setting l ≈
         pﬃﬃﬃerror is less than ðd þ 1Þe
truncation
  −1
                                                                        compute the value classically, by substituting our algorithm
γ logð d=εÞ to ensure a small root-mean-square error                    for the circuit results. At an intuitive level, the properties
gives Theorem 2. We remark that our proof of Lemma 2, as                that make error mitigation more efficient (having a signal
outlined above, introduces substantially new techniques                 dominated by low-weight Paulis) also make the signal
compared to any previous Pauli truncation algorithm that                easier to simulate. We emphasize that this discussion
we are aware of.                                                        applies only for noise rates that are constant with respect
                                                                        to n; for smaller noise rates, γ ¼ Õð1=nÞ, a circuit can be
             D. Applications and Implications                           both complex and efficiently mitigable.
   Let us now consider the implications of our algorithms.                 Noisy DQC1 ⊆ BPP. Our results extend to circuits with
We summarize a few of the most prominent ones below,                    a fixed input state within one scenario: when the state is
and direct the interested reader to the Appendixes E–L for              highly mixed. This follows directly from Theorems 1 and 2
details and additional results.                                         because the ensemble composed of a single highly mixed
   Lower bound on quantum error mitigation. Error mit-                  input state is low average (Appendix K). Experiments with
igation seeks to estimate the output of an ideal quantum                highly mixed input states are commonplace in several
circuit via experiments on noisy circuits [60–62,82–87].                quantum technologies, including nuclear magnetic reso-
While the sampling overhead for certain mitigation strat-               nance spectroscopy [91] and solid-state quantum simu-
egies (such as probabilistic error cancellation) is explicitly          lators [92,93]. Formally, this scenario is captured by the
exponential in the number of qubits [60–62], ∼eγnd , for                deterministic quantum computing with one clean qubit
other strategies (such as zero noise extrapolation), an                 (DQC1) model of quantum computation [94]. This model
exponential scaling is known only for certain worst-case                encompasses quantum experiments that are performed
circuits [63–65]. This has raised an intriguing open ques-              by (1) preparing an initial state, j0ih0j ⊗ 1n−1 =2n−1 , which
tion: Can error mitigation scale efficiently for any quantum            is clean on the first qubit and mixed on all others,
circuits of practical interest [88–90]?                                 (2) applying any quantum circuit to this initial state,
   Unfortunately, our results imply a somewhat negative                 and (3) measuring the first qubit in the Z basis. We prove
answer (Fig. 3). For a large class of mitigation strategies,            that any noisy DQC1 circuit can be classically simulated in
any circuit that can be error mitigated in polynomial time              polynomial time.
on most input states can also be classically simulated in                  Sampling from anticoncentrated circuits. Our algorithms
polynomial time on most input states (Appendix I).                      can also be used to sample from noisy quantum circuits,


                                                                041018-7
SCHUSTER, YIN, GAO, and YAO                                                                 PHYS. REV. X 15, 041018 (2025)

provided that the output distribution of the circuit anti-              Our proof follows by an immediate triangle inequality: If
concentrates. Anticoncentration refers to a property of the          a quantum circuit with noise rate γ produces an expectation
output
P        distribution that one is sampling from, namely that         value that is ε away from the ideal expectation value, then
          2
   x pðxÞ ¼ polyðnÞ=2 . Here, pðxÞ is the output proba-
                          n                                          we can classically simulate the ideal expectation value to
bility of a bit string x ∈ f0; 1gn . Intuitively, anticoncentra-     error 2ε by simulating the noisy circuit to precision ε. From
tion guarantees that the output distribution has relatively          Theorem 2, this can be done in time χ ¼ nO(ð1=γÞ logðd=εÞ) .
even support across all bit strings x. Anticoncentration is          Taking the logarithm of both sides, setting d ¼ polyðnÞ,
common in many output distributions [95–101], and is used            and solving for γ yields Corollary 2.
frequently as an ingredient for proofs of both the classical            We propose that this criteria can function as a simple and
hardness [95,102,103] and easiness [31] of sampling tasks.           rigorous “test” for whether a given quantum circuit can
Our algorithm for sampling from noisy quantum circuits               feature an advantage over classical computation. Thus far,
utilizes a standard reduction from noisy circuit sampling to         demonstrations of quantum advantage have been restricted
computing noisy expectation values, which is valid in the            to sampling experiments [95,104], which are inherently
presence of anticoncentration [26]. We achieve sampling to           highly sensitive to noise [105,106]. When moving beyond
within small total variational distance in quasipolynomial           sampling, designing experiments whose expectation values
time (Appendix E).                                                   are macroscopically sensitive to noise in a nontrivial manner
   Random circuits with nonunital noise. Recent works have           is challenging. This is highlighted by recent experiments on
asked [36,67], can random quantum circuits with nonunital            IBM’s quantum processor [89], which, despite involving
noise, such as spontaneous emission, escape the classical            many qubits and high gate fidelities, were rapidly simulated
algorithms known for circuits with unital noise? This was            classically by follow-up works [107–112]. In light of our
answered in part by Ref. [36], which provides an algorithm           work, this can be understood as a consequence of the
for expectation values in random circuits with nonunital             experiments’ insensitivity to noise [113].
noise, that runs in quasipolynomial time for geometrically              More broadly, our criteria are motivated by a recent surge
local circuits, and exponential time (in ε−1 ) for general circuit   of numerical [46,49,50,54–59] and theoretical [114–116]
architectures. Leveraging our proof method for Theorem 1,            studies of many-body quantum dynamics, which show that
we show that Algorithm 1 computes expectation values in              local observables in strongly interacting quantum dynamics
polynomial time for any random circuit with nonunital noise          can often be efficiently simulated using Pauli-truncation-
(Appendix H). We note that a direct extension of Theorem 1           based methods. This occurs even when the dynamics
to nonrandom circuits with nonunital noise is not possible,          appear difficult by all conventional complexity measures.
since for general quantum circuits with nonunital noise one          When performing a quantum experiment, one might seek a
can perform fault-tolerant computation [14].                         simple benchmark for whether the experiment is suscep-
   Quantum advantage beyond sampling. While the focus                tible to such classical simulations. Following Corollary 2,
of our work has been on noisy quantum circuits, our results          we propose that the experiments’ sensitivity to noise
also have broader implications in the search for near-term           provides precisely such a unifying benchmark.
experiments that exhibit a quantum advantage. Namely, by                Finally, it should be noted that the converse of
inverting our Theorem 2, we show that any quantum circuit            Corollary 2 does not hold. Namely, one can design experi-
that is exponentially hard to simulate classically must fail in      ments that are highly sensitive to noise, such as those
the presence of even a macroscopically small noise rate,             involving a many-body observable [89] or a Loschmidt
γ ¼ Ω̃ð1=nÞ (Appendix J).                                            echo [117], yet these are not guaranteed to be classically
   Corollary 2 (Classically hard quantum circuits must be            hard [111]. As a simple example, a Clifford circuit can
highly sensitive to noise). Given any ideal quantum circuit          evolve a local Pauli observable into a high-weight Z string,
C on n qubits with depth d ¼ polyðnÞ, any normalized                 with a large expectation value on any initial computational
observable O, and any low-average ensemble E ¼ fρg.                  basis state. This results in an apparent complexity accord-
Suppose that the run-time of any classical algorithm to              ing to our benchmark, since the string is high weight and
compute the expectation values, trðCfρgOÞ, to root-mean-             therefore highly sensitive to noise. Nevertheless, the circuit
square error ε is lower bounded by χðn; εÞ. Then any noisy           is easily simulable with stabilizer methods. Analogous
implementation of C must only succeed in computing                   “spoofing” behavior occurs for nearly all established
trðCfρgOÞ to root-mean-square error ε for noise rates:               complexity metrics, including the entanglement entropy,
                                                                   magic, operator entanglement, out-of-time-ordered corre-
                            logðnÞ logðn=εÞ                          lators (OTOCs), and others: It is always possible to
                   γ≤O                         :             ð13Þ
                              log (χðn; εÞ)                          construct circuits that appear complex by these metrics
                                                                     but remain classically simulable by other means [118].
In particular, if the classical run-time is exponential in n,        With this in mind, we envision that our criteria are best used
the noisy implementation must succeed only for macro-                alongside existing complexity measures, much as current
scopically small noise rates, γ ¼ O(log2 ðnÞ=n).                     measures are used alongside one another.



                                                               041018-8
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                            PHYS. REV. X 15, 041018 (2025)

                         E. Outlook                                  This comparison becomes more involved for quantum
   Our results provide the most extensive evidence yet that       circuits with uniform noise. As for the gate-based noise
noisy quantum circuits without error correction can be            model, the only existing classical algorithms for uniform
efficiently classically simulated. In the long term, this         noise which explicitly take advantage of the noise are
emphasizes the necessity of quantum error correction for          specific to IQP circuits and random circuits. However, since
achieving a scalable quantum advantage over classical             uniform noise limits the depth of any nontrivial quantum
computation. For experiments without error correction,
                                                                  circuit [13], we should compare the scaling of our theorems
our results demonstrate the necessity of improving the
noise rate proportional to the number of qubits. Moreover,        to existing algorithms for low-depth quantum circuits. In
even at sufficiently low noise rates, our results provide a       particular, we show in Appendix C that expectation values
rigorous test for whether a given circuit can yield a             in quantum circuits with uniform noise become ε-close to
quantum advantage, by establishing, perhaps counterintui-         their values in the maximally mixed state at logarithmic
tively, that such circuits must be highly sensitive to noise.     depth, d ≥ γ −1 logð1=εÞ [77]. With this in mind, we
   Our work opens the door to a number of intriguing              compare the run-time of our classical algorithms to existing
directions. First, is it possible to devise analogous classical   algorithms for circuits of such depth on a case-by-case
algorithms for continuous-time dynamics instead of quan-          basis below.
tum circuits? Second, to what extent do our results carry            (1) Let us begin by considering general (i.e., all-to-all-
over to more general errors, such as dephasing or thermal                 connected) circuit architectures. In this setting, there
noise? Finally, can insights from our proof techniques be                 are no existing classical algorithms for logarithmic
used to improve numerical algorithms for classically                      depth circuits, and so Theorem 1 provides an
simulating quantum systems? In particular, we speculate                   exponential improvement over the naive classical
that our approach may provide a fruitful starting point for               simulation time 2OðnÞ . This exponential improve-
simulating highly connected circuit architectures, where                  ment continues to hold even for more restricted
tensor network methods typically struggle.                                classes of observables, as we discuss below.
                                                                          (a) For the specific case of local observables, we can
                ACKNOWLEDGMENTS                                               moderately improve the naive classical simula-
   We are grateful to Dorit Aharonov, Zhenyu Cai, Matthias                    tion time by restricting to qubits within the light
C. Caro, Andreas Elben, Bill Fefferman, Soumik Ghosh,                         cone of the observable. For general circuits, the
Charvi Goyal, Greg Kahanamoku-Meyer, John Preskill,                           light cone contains 2d qubits, leading to a run-
                                                                                                       Oðγ −1 Þ
                                                                              time of 2Oð2 Þ ¼ 2ð1=εÞ
                                                                                             d
Dominik Wild, and Mike Zalatel for valuable discussions                                                         . This is exponential
                                                                                                            −1
and insights. T. S. acknowledges support from the Walter                      in the inverse precision ε , whereas our Algo-
                                                                                                                                  −2
Burke Institute for Theoretical Physics at Caltech. C. Y. is                  rithm 1 runs in polynomial time, ð1=εÞÕðγ Þ , for
supported by the Department of Energy under Quantum                           local observables.
Pathfinder Grant No. DE-SC0024324. X. G. acknowledges                     (b) For tensor-product observables in general circuits,
support from NSF PFC Grant No. PHYS 2317149 and                               Ref. [119] provides an algorithm with time
start-up grants from CU Boulder. N. Y. Y acknowledges                               2d                      Oðγ −1 Þ logðnÞ

support from the NSF via the QLCI program (Grant                              nO(2 logðn=εÞ) , i.e., nð1=εÞ                 , to estimate
No. OMA-2016245) and the STAQ II Program. The                                 either (i) output probabilities, i.e., O ¼ j0n ih0n j,
Institute for Quantum Information and Matter, with which                      or (ii) the magnitude of Pauli expectation values,
T. S. is affiliated, is an NSF Physics Frontiers Center.                      jtrðCfρgOÞj, where O is Pauli. The run-time is
                                                                              exponential in ε−1 when applied to noisy quantum
                                                                              circuits, due to the double exponential dependence
          APPENDIX A: COMPARISON TO                                           of the original run-time on the depth d. In contrast,
              EXISTING RESULTS                                                in case (i), Algorithm 1 computes output proba-
  In this appendix, we provide a more detailed comparison                     bilities to an exponentially smaller error, ε · 2−n=2 ,
between the run-time of our classical algorithms and                          in quasipolynomial time. In case (ii), Algorithm 1
existing results. Let us first briefly summarize this com-                    computes Pauli expectation values (including their
parison for the gate-based noise model, and then turn to the                  sign) to within the same error as Ref. [119] in
case of uniform noise.                                                        polynomial time.
   (i) For quantum circuits with gate-based noise, the only          (2) We now turn to more restricted circuit architectures,
       existing classical algorithms are restricted to IQP                beginning with the simplest case of 1D circuits. For
       circuits and random circuits (summarized in Table I                tensor-product observables in 1D circuits, our algo-
       of the main text). Thus, for general circuits, Theo-               rithm provides no improvement because a trivial
       rem 2 provides an exponential improvement over the                 classical simulation via matrix product states is
       naive classical simulation time 2OðnÞ .                            already very efficient.


                                                            041018-9
SCHUSTER, YIN, GAO, and YAO                                                               PHYS. REV. X 15, 041018 (2025)

     (a) For tensor-product observables in 1D circuits,                  (a) For tensor-product observables in 3D circuits,
         one can perform a classical simulation using                        Ref. [120] provides an algorithm with run-time
         matrix product states. This has run-time 2OðdÞ ,                              2 1=3                        −2 1=3
                                                                             Oðnd3 2d n =ε2 Þ, i.e., n · ð1=εÞO(γ n logð1=εÞ)
                                           −1
         which translates to ð1=εÞOðγ Þ for quantum                          for quantum circuits with uniform noise. The
         circuits with uniform noise. This is polynomial                     run-time is subexponential in n, and is improved
         in ε−1 as is our algorithm.                                         to either polynomial or quasipolynomial time by
 (3) For 2D circuits, existing classical algorithms become                   our algorithm.
     less efficient, and our results generally provide a                 (b) For local observables in 3D circuits, a direct
     quasipolynomial to polynomial improvement.                              light-cone simulation runs in quasipolynomial
                                                                                         3            −3      2
     (a) For local observables in 2D circuits, the best                      time, 2Oðd Þ ¼ ð1=εÞO(γ logð1=εÞ ) . In contrast,
         existing classical algorithm is a direct simulation                 our Algorithm 1 runs in polynomial time,
                                                                                      −2
         restricted to the light cone of the observable. The                 ð1=εÞÕðγ Þ , and our Algorithm 2 runs in nearly
         light cone contains Oðd2 Þ qubits, which leads to                                               −1      −1
                                                                             polynomial time, ð1=εÞÕ(γ log logðε Þ) .
                             2             −2
         a run-time 2Oðd Þ ¼ ð1=εÞO(γ logð1=εÞ) that is
         quasipolynomial in ε−1 . In contrast, our Algo-                      APPENDIX B: LOW-AVERAGE
                                                     −2
         rithm 1 runs in polynomial time, ð1=εÞÕðγ Þ . We                      ENSEMBLES OF STATES
         note that we can also utilize the same light-cone
                                                                      We now formally define our allowed ensembles of input
         argument to improve the scaling of our Algo-
                                                                   states, which we call low-average ensembles.
         rithm 2, by replacing n with (γ −1 logð1=εÞ)2 in
                                                                      Definition B1 (Low-average ensembles of states).
         Theorem 2. This leads to a run-time                       We say that an ensemble of quantum states E ¼ fρg
                  −1        −1
         ð1=εÞO(γ log logðε Þ) , which is nearly polynomial        is                   ensemble with purity c if jjð1=½jEjÞ×
                                                                   P a low-average
         and has a better dependence on the noise rate γ.             ρ ρjj∞ ≤ c=2 n . For ensembles of pure states and c ¼ 1,
     (b) For tensor-product observables in 2D circuit              this coincides with the definition of a 1-design of states.
         architectures, Ref. [120] provides an algorithm to           As an example, the ensemble of computational basis
                                                        2
         estimate expectation values in time Oðnd2 2d =ε2 Þ        states with n − m random bits and m fixed bits forms a low-
         for any tensor-product observable, O ¼⊗nj¼1 Oj            average ensemble with purity c ¼ 2m. Any complete basis
        with jjOj jj∞ ≤ 1. This translates to a run-time n ·       of pure states forms a low-average ensemble with c ¼ 1.
                  −2
        ð1=εÞO(γ logð1=εÞ) for quantum circuits with uni-             We now state and prove the more general version of our
        form noise, which is quasipolynomial in ε−1 . For          Lemma 1 from the main text.
        Pauli observables, our algorithm improves the run-            Lemma B1 (Extended version of Lemma 1 of the main
                                                                   text). Consider a low-average ensemble E ¼ fρg with
        time to polynomial in ε−1 . For general tensor-
        product observables, we note that our algorithm            purity c and two observables O and Õ. The root-mean-
                                                                   square difference between the expectation value of O and Õ
        computes expectation values       Q to within precision                 pﬃﬃ
        ε · jjOjjF , where jjOjjF ¼ nj¼1 jjOj jjF may be           is less than c · jjO − ÕjjF .
                                                                      Proof of Lemma B1. For simplicity, we begin by
        substantially smaller than 1. Thus, replacing ε →
                                                                   assuming that each state is pure, and afterward generalize
        ε=jjOjjF in Theorem 1 for the sake of comparison to
                                                                   to mixed states. For a pure state ρ ¼ jψihψj, the squared
        Ref. [120], our algorithm has run-time
              −1                                     −2            difference obeys
        nÕðγ ÞþO( logðjjOjjF =εÞ=γd) ðjjOjjF =εÞÕðγ Þ for gen-
        eral observables. This run-time may be better or           trðjψihψjδOÞ2 ¼ hψjδO† jψihψjδOjψ i i ≤ hψjδO† δOjψi;
        worse than that of Ref. [120] depending on the
        scalings of n, d, ε, γ. For example, for large n but                                                                ðB1Þ
        moderate ε and d, the algorithm in Ref. [120] is
        more efficient than our algorithm. On the other            where we recognize the middle expression as the expect-
        hand, for small ε or large d, our algorithm becomes        ation value of jψihψj in the state δOjψi, which is upper
                                                                   bounded by the normalization of the state. Inserting this
        more efficient. In particular, in the case
                                                                   inequality into the mean-square error and applying the low-
        d ¼ Ω( logðnÞ), our algorithm runs in polynomial
                                                                   average condition gives our desired bound,
        time whereas the algorithm in Ref. [120] runs in
        quasipolynomial time.                                       1 X                   1 X
 (4) Finally, for 3D circuit architectures, Theorem 1                    trðjψihψjδOÞ2 ≤       hψjδO† δOjψi
                                                                   jEj ψ                 jEj ψ
     provides a subexponential to polynomial improve-
     ment over existing algorithms for tensor-product              ¼ trðρE · δO† δOÞ ≤ jjρE jj∞ · jjδO† δOjj1 ¼ c · jjδOjj2F ;
     observables, and a quasipolynomial to polynomial
     improvement for local observables.                                                                                     ðB2Þ



                                                            041018-10
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                     PHYS. REV. X 15, 041018 (2025)
                                         P
where we use ρE ¼ ð1=jEjÞ ψ jψihψj to denote the                                  APPENDIX C: CLASSICAL ALGORITHM FOR
mixture of the ensemble.                                                               UNIFORM NOISE (THEOREM 1)
   We now turn to mixed states. Let us write each                                  We now provide our complete proof of Theorem 1 of the
mixedP state in its orthonormal eigenbasis fjψ ρ ig as                          main text. We begin by establishing a short lemma that
ρ ¼ ψ ρ pψ ρ jψ ρ ihψ ρ j. For each mixed state, we can define                  upper bounds the circuit depth of any nontrivial quantum
a quantum channel that dephases states in the eigenbasis of                     circuit with uniform noise.
ρ, Dρ fjψ ρ ihψ ρ jψ 0ρ g ¼ δψ ρ ;ψ 0ρ jψ ρ ihψ ρ j. This allows us to             Lemma C1 (Upper bound on circuit depth for quantum
write each mixed state ρ as its corresponding dephasing                         circuits with uniform noise). Consider any observable O
channel Dρ applied to a pure state jϕρ i:                                       and any quantum circuit C with uniform noise. The
                                                                                Frobenius norm of the nonidentity component of C† fOg
                                                     X pﬃﬃﬃﬃﬃﬃﬃ
      ρ ¼ Dρ fjϕρ ihϕρ jg;                 jϕρ i ¼      pψ ρ jψ ρ i:     ðB3Þ   is upper bounded by e−γðdþ1Þ jjOjjF, where d is the
                                                      ψρ                        circuit depth.
                                                                                   Proof. The Heisenberg time evolution of the nonidentity
                                                                                component of O has weight ≥ 1 at all layers. Thus,
Turning to the mean-square difference in expectation
                                                                                its Frobenius norm decreases by at least a factor e−γ
values, we first rewrite each trace as
                                                                                from each noise channel. Since there are d þ 1
                                                                                noise channels, we have jjC† fOg − trðOÞ=2n · 1jjF ≤
trðρ · δOÞ ¼ trðDρ fjϕρ ihϕρ jg · δOÞ ¼ hϕρ jDρ fδOgjϕρ i;                      e−γðdþ1Þ jjOjjF .                                         ▪
                                                                         ðB4Þ      Lemma C1 can be viewed as an adaptation of Theorem 3
                                                                                in Ref. [13] to the Frobenius norm of observables. Using
since the dephasing channel is equal to its conjugate.                          our Lemma B1, it implies that one can trivially simulate
Applying the same inequality as in Eq. (B1) gives                               expectation
                                                                                    pﬃﬃ      values (to within small root-mean-square error
                                                                                ε · c · jjOjjF over a low-average ensemble of input states
                                                                                with purity c), in any quantum circuit with depth d ≥
                  trðρδOÞ2 ≤ hϕρ jDρ fδO† g · Dρ fδOgjϕρ i:              ðB5Þ
                                                                                γ −1 logð1=εÞ and uniform noise. To do so, one simply
                                                                                replaces the expectation value with its value in the
Since both operators within the expectation value are                           maximally mixed state, trðOÞ=2n . Thus, in what follows,
diagonal in the eigenbasis of ρ, we can compute the                             we need only to analyze the performance of our
expectation value as                                                            Algorithm 1 on circuits of depth d < γ −1 logð1=εÞ.
                                                                                   Accuracy of algorithm. We establish the accuracy of
      hϕρ jDρ fδO† g · Dρ fδOgjϕρ i                                             Algorithm 1 by showing that our approximation Õ is close
         X pﬃﬃﬃﬃﬃﬃﬃ                                pﬃﬃﬃﬃﬃﬃﬃ                     to O in Frobenius norm:
       ¼        pψ ρ ·ðδO† Þψ ρ ψ ρ · ðδOÞψ ρ ψ ρ · pψ ρ :               ðB6Þ
                 ψρ

                                                                                                jjÕ − C† fOgjjF ≤ εjjOjjF :           ðC1Þ
This is upper bounded by the analogous expression that
includes the off-diagonal matrix elements of δO,
                                                                                From Lemma B1, this bounds the root-mean-square error in
X pﬃﬃﬃﬃﬃﬃﬃ                            pﬃﬃﬃﬃﬃﬃﬃ                                  expectation values as desired. For simplicity, we assume
   pψ ρ ·ðδO† Þψ ρ ψ ρ · ðδOÞψ ρ ψ ρ · pψ ρ
 ψρ
                                                                                that the operator O has no identity component; if it does,
      X                                                                         then this can be easily be included by adding a constant
≤               pψ ρ · ðδO† Þψ ρ ψ 0ρ · ðδOÞψ 0ρ ψ ρ ¼ trðρ · δO† δOÞ;   ðB7Þ   offset to the expectation values.
    ψ ρ ;ψ 0ρ                                                                      To show this, it is convenient to write operators
                                                                                as vectors in a doubled Hilbert space, with inner product
since each off-diagonal element contributes an amount                           ⟪AjjB⟫ ¼ trðA† BÞ=2n for operators A, B. The vector norm
pψ ρ ðδO† Þψ ρ ψ 0ρ ðδOÞψ 0ρ ψ ρ ¼ pψ ρ jðδOÞψ 0ρ ψ ρ j2 ≥ 0. Putting it all    is equal to the squared Frobenius norm, ⟪AjjA⟫ ¼ jjAjj2F .
together, we have                                                               In this notation, each unitary layer Ut is represented
                                                                                by a superunitary U t acting as U t jjA⟫ ≡ jjU†t AUt ⟫.
                   1 X              1 X                                         Meanwhile, the uniform noise channel acts on the basis
                        trðρδOÞ2 ≤       trðρ · δO† δOÞ                         of Pauli operators as DjjP⟫ ¼ e−γw½P jjP⟫. Finally, the
                  jEj ρ            jEj ρ
                                                                                projector P l onto Pauli operators of weight w is given
                  ¼ trðρE · δO† δOÞ ≤ c · jjδOjj2F ;                     ðB8Þ   by P w jjP⟫ ¼ δw½P;w jjP⟫. With this notation, our approxi-
                                                P                               mation Õ in Eq. (6) of the main text can be written
where we denote ρE ¼ ð1=jEjÞ                        ρ ρ once again.        ▪    concisely as


                                                                          041018-11
SCHUSTER, YIN, GAO, and YAO                                                                                         PHYS. REV. X 15, 041018 (2025)
                                                    X
                                  jjÕ⟫ ¼                      e−γðw0 þþwd Þ P wd U d    P w2 U 2 P w1 U 1 P w0 jjO⟫;                              ðC2Þ
                                                w0 þþwd ≤l


where wt ≥ 1 is the weight at each layer. Each sequence of projectors in the sum corresponds to a single root-to-leaf
sequence in the Pauli tree [Fig. 2(a) of the main text].
   We would like to bound the Frobenius norm of Õ − C† fOg ≡ jjÕ⟫ − C† jjO⟫. As discussed in the main text, we do so
by breaking up the sum over w0 ; …; wd layer by layer. We then use the fact that the P wt at each layer t project onto
orthogonal subspaces for different wt to upper bound the Frobenius norm. Let us illustrate this for the first layer. We can
write
                                    X
         jjÕ⟫ − C† jjO⟫ ¼                      e−γðw0 þþwd Þ P wd U d    P w1 U 1 P w0 jjO⟫
                                w0 þþwd >l
                                 X
                                 ∞                                 X                                                                        
                                         −γwd                                       −γðw0 þþwd−1 Þ
                           ¼            e       P wd U d                        e                       P wd−1 U d−1    P w1 U 1 P w0 jjO⟫
                                wd ¼1                      w0 þþwd−1 >l−wd

                                 X
                                l−dþ1                                      X                                                                     
                                                    ðl−dþ1Þ
                           ¼             e−γwd P wd            Ud                         e−γðw0 þþwd−1 Þ P wd−1 U d−1    P w1 U 1 P w0 jjO⟫ :     ðC3Þ
                                 wd ¼1                              w0 þþwd−1 >l−wd


In the second line, we pull out the sum over wd. In the third line, we group all terms with weight wd ≥ l − d þ 1 at layer d
together, by defining the modified “projectors”:

                                                    
                                          ðl0 Þ         Pw                                                     w < l0
                                         Pw ≡                                                −γðn−l0 Þ
                                                                                                                                                         ðC4Þ
                                                        P l0 þ e−γ P l0 þ1 þ    þ e                   Pn    w ¼ l0 :

This grouping will reduce the number of terms in our error bound. The upper limit l − d þ 1 is chosen to be just large
enough such that the resulting sum of weights is always greater than l, since there are d additional weights wd−1 ; …; w0
                                                                                                       ðl0 Þ
and each weight is at least 1. Still working with only the first layer, we can now use the fact that P w are orthogonal to
remove them from the Frobenius norm:

               2 l−dþ1                                                                                                                2
                  X                                               X                                                                      
jjÕ⟫ − C† jjO⟫ ¼      e−γwd ðl−dþ1Þ
                                  P        U                                         e−γðw0 þþwd−1 Þ P wd−1 U d−1    P w1 U 1 P w0 jjO⟫ 
                              wd       d
                  F       wd ¼1                                 w0 þþwd−1 >l−wd                                                               F

                         X
                        l−dþ1                                         X                                                                     2
                                                                                                                                                 
                               −2γwd  ðl−dþ1Þ
                      ¼       e      P wd     Ud                                     e−γðw0 þþwd−1 Þ
                                                                                                          P wd−1 U d−1    P w1 U 1 P w0 jjO⟫ 
                         wd ¼1                                    w0 þþwd−1 >l−wd                                                                 F

                         X
                        l−dþ1                       X                                                                       2
                                                                                                                            
                      ≤       e −2γw                              e−γðw0 þþw     Þ P wd−1 U d−1    P w1 U 1 P w0 jjO⟫ :                      ðC5Þ
                                      
                                    d                                             d−1

                         wd ¼1              w0 þþwd−1 >l−wd                                                                    F



In the first line, we use that the Frobenius norm of a sum of orthogonal operators is equal to the sum of the operators’
                                          ðl0 Þ
norms. In the second line, we use that P w and unitary operation cannot increase the norm. This completes our analysis
of the first layer.
   To complete our proof, we repeat the steps above for each remaining layer in the quantum circuit. After doing so once
more, for the second layer, we obtain

                      2 l−dþ1 l−dþ2−wd                                                                       2
                         X      X                       X                                                    
       jjÕ⟫ − C† jjO⟫ ≤               e−2γðwd þwd−1 Þ 
                                                                e−γðw0 þþwd−2 Þ
                                                                                   P     U       P   U P   jjO⟫  :
                                                                               wd−2 d−2         w1 1 w0      
                            F       wd ¼1       wd−1 ¼1                       w0 þþwd−2                                                           F
                                                                              >l−wd −wdþ1




After repeating for all layers, we obtain



                                                                         041018-12
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                                      PHYS. REV. X 15, 041018 (2025)

                               2 l−dþ1 l−dþ2−wd                                                                                           2
                                  X      X             X
                                                        l−wd −−w2
                                                                                                                 X                            
                jjÕ⟫ − C† jjO⟫ ≤                             e−2γðw1 þþwd Þ 
                                                                                                                              e−γw0
                                                                                                                                      P w0 jjO⟫
                                                                                   
                                      F       wd ¼1       wd−1 ¼1            w1 ¼1                         w0 >l−wd −−w1                          F

                                               X l−dþ2−w
                                              l−dþ1 X d                      X
                                                                          l−wd −−w2        X
                                                                                          lþ1−wd −−w1                                     2
                                                                                                                                  ðw Þ       
                                          ¼                                                                e−2γðw0 þþwd Þ P w00 jjO⟫
                                              wd ¼1       wd−1 ¼1            w1 ¼1       w0 ¼lþ1−wd −−w1                                      F
                                                                              X             
                                          ≤ e−2γðlþ1Þ jjOjj2F ·                             1 :                                                          ðC6Þ
                                                                          w0 þþwd ¼lþ1




In the second line, the final sum runs over a single value                               by definition contains at most m Pauli operators.
of w0 . It remains only to compute the final sum in the                                  Otherwise we can choose the circuit layer with the
third line.                                                                              minimum weight, which gives the first term in the mini-
   The sum in Eq. (6) counts the number of sequences                                     mum, nl=d , as in Ref. [31]. Inserting the value of cγ and
ðw0 ; …; wd Þ that sum to l þ 1. Each sequence corresponds                               invoking Lemma C1 to restrict attention to d < γ −1 logð1=εÞ,
to an individual truncation in our algorithm, as discussed                               we find a run-time
and depicted in Fig. 2(a) of the main text. In mathematics,
                                                                                                                                                2
the number of such sequences is well known (referred to as                               min nO(logð1=γÞ=γ)þO(logð1=εÞ=γd) ; m · ð1=εÞO(logð1=γÞ=γ ) :
“the number of compositions of l þ 1 into d þ 1 parts”),
and is equal to ðldÞ. Thus, we have                                                                                                                      ðC11Þ

                                                                                       Taking the first term in the minimum leads to the first
                                                 l
        jjÕ − C† fOgjj2F ≤ e−2γðlþ1Þ ·                     · jjOjj2F :    ðC7Þ          scaling in Theorem 1 of the main text. Taking the second
                                                      d                                  term with m ¼ polyðnÞ leads to the second scaling.     ▪
To determine the required value of l, we use a standard
bound on the binomial coefficient, ðldÞ ≤ ðel=dÞd . We then                                 APPENDIX D: CLASSICAL ALGORITHM FOR
have                                                                                            GATE-BASED NOISE (THEOREM 2)
                                       d                                                We now turn to our Algorithm 2 for gate-based noise. We
 −2γðlþ1Þ
                 l         −2γðlþ1Þ      el                                              begin in Appendix D 1 with a proof of Lemma 2 of the
e           ·         ≤e              ·      ≤ e−γðlþ1Þ ;                  ðC8Þ
                 d                        d                                              main text, and analyze the remaining aspects of the
                                                                                         algorithm in Appendix D 2.
where the second inequality holds as long as
d logðel=dÞ ≤ γðl þ 1Þ. Thus, we can ensure that the                                                 1. Bounding noisy operator growth
desired error bound Eq. (C1) holds by choosing
                                                                                           We now prove Lemma 2 of the main text, which upper
                      l ¼ cγ d þ 2γ    −1
                                            logð1=εÞ;                      ðC9Þ          bounds the cumulative operator weight distribution,

                                                                                                                              X
                                                                                                                              n
where cγ is the solution of cγ ¼ γ −1 logðecγ Þ; at small γ, we                                               QðtÞ ðwÞ ¼               PðtÞ ðw0 Þ;       ðD1Þ
have cγ ¼ γ −1 logðe=γÞ þ O(γ −1 log logð1=γÞ).                                                                              w0 ¼wþ1
  Run-time of algorithm. The run-time of Algorithm 1 is
determined by the number of Pauli paths in our approxi-                                  in any noisy quantum circuit. We also include a
mation of Õ. From Lemma 8 in Ref. [31], the number of                                   slightly stronger bound on the cumulative weight
such paths is upper bounded by                                                           distribution when considering the approximate time-
                                                                                       evolved operator Õ.
min nl=d ; m · 2OðlÞ                                                                        Lemma D1 (Extended version of Lemma 2 of the main
                                                                                       text). Consider the Heisenberg time evolution OðtÞ of an
¼ min nO(cγ þð2=γdÞ logð1=εÞ) ; m · 2Oðcγ dÞ · ð1=εÞOð1=γÞ                               observable O in a quantum circuit with gate-based noise.
                                                                          ðC10Þ          The cumulative weight distribution is less than

if the observable O is a sum of m Pauli operators. To                                                         QðtÞ ðwÞ ≤ e−2γðwþ1Þ · jjOjj2F             ðD2Þ
derive the second term in the minimum, we observe that
in the second part of the proof of Lemma 8 of Ref. [31] we                               for all γ, w, t. We can also extend this to our classical
can choose the layer t to be the final circuit layer, which                              approximation Õ of O, which truncates Pauli operators of


                                                                             041018-13
SCHUSTER, YIN, GAO, and YAO                                                                  PHYS. REV. X 15, 041018 (2025)

weight greater than l between circuit layers. In this case,         where Q0ðgÞ ðw − 1Þ denotes the operator norm at weight
the cumulative operator weight distribution Q̃ðtÞ ðlÞ obeys         above w − 1 after applying U g but before applying the
                                                                    noise channel Dg . Similarly, we have
               X
               d
                     Q̃ðtÞ ðlÞ ≤ e−2γðlþ1Þ · jjOjj2F :     ðD3Þ
                                                                         P0ðgÞ ðwÞ ¼ Pðg−1Þ ðwÞ þ J ðgÞ ðwÞ − JðgÞ ðw þ 1Þ;   ðD6Þ
               t¼0

   Proof of Lemma D1. We begin by proving the first                 where P0ðgÞ ðwÞ is also defined after Ug but before Dg . The
statement; the second will follow shortly after. We keep            current JðgÞ ðwÞ quantifies the net transfer in operator norm
track of the Heisenberg time evolution of O gate by gate.           from weight w − 1 to w by U g. Writing it out explicitly, we
We denote the operator evolved through the first g gates and        have
noise channels of the circuit as OðgÞ ; if gt denotes the final
gate within a circuit layer t, then Oðgt Þ corresponds to OðtÞ in     JðgÞ ðwÞ ¼ ⟪Ow−1;w þ Ow;w jjOw−1;w þ Ow;w ⟫
our layer-by-layer notation. We again use Oð0Þ to denote the                      − ⟪Ow;w jjOw;w ⟫ − ⟪Ow;w−1 jjOw;w−1 ⟫;      ðD7Þ
operator evolved through the readout noise channel.
   The initial observable O will have some operator weight          where we use the doubled bra-ket notation to denote inner
distribution PðwÞ with norm jjOjj2F . After the application of      products of operators, ⟪AjjB⟫ ≡ ð1=2n ÞtrðABÞ, and abbre-
readout noise, the weight distribution is damped to
                                                                    viate Ow;w0 ≡ P w0 fU†g P w fOðg−1Þ gU g g for the component
Pð0Þ ðwÞ ¼ e−2γw PðwÞ. This leads to a trivial upper bound
                                                                    of the operator that starts at weight w and ends at weight w0 .
on the cumulative operator weight distribution at time zero:
                                                                    The first term is the contribution from weights w − 1 and w
              X
              N                                                     before the gate to the norm at weight w after the gate. The
                            0
Qð0Þ ðwÞ ¼             e−2γw Pðw0 Þ ≤ e−2γðwþ1Þ · QðwÞ              second and third term arise when taking the difference with
             w0 ¼wþ1                                                Qðg−1Þ ðw − 1Þ. Although it does not immediately appear so,
         ≤ e−2γðwþ1Þ · jjOjj2F :                           ðD4Þ     the flow is in fact antisymmetric upon exchanging w − 1
                                                                    and w, as it must be in order to preserve the total operator
Our aim is to show that this bound in fact holds for                norm. This can be verified by expanding the first term and
all times.                                                          using ⟪Ow;w jjOw−1;w ⟫ ¼ −⟪Ow−1;w−1 jjOw;w−1 ⟫. This
   We proceed gate by gate. The evolution during each gate          equality is guaranteed because U †g P w fOðg−1Þ gUg and
consists of two steps: First, we apply the unitary gate U g ,       U†g P w−1 fOðg−1Þ gU g are orthogonal.
then we apply local depolarizing noise to the two qubits in            To incorporate the noise channel Dg , we use the fact that
the gate. In the first step, application of Ug can transfer         any operator that increases in weight under Ug (in par-
operator norm between adjacent values of l. We capture              ticular, the operator Ow−1;w ) must have support on both
this by defining the current JðgÞ ðwÞ via                           qubits in U g after the gate is applied. Thus, the norm of
                                                                    such an operator is damped by a factor of e−2γ by the noise
         Q0ðgÞ ðw − 1Þ ¼ Qðg−1Þ ðw − 1Þ þ JðgÞ ðwÞ;        ðD5Þ     channel. In full detail, we have


   PðgÞ ðwÞ ¼ ⟪Ow−1;w þ Ow;w þ Owþ1;w jjDg · Dg jjOw−1;w þ Ow;w þ Owþ1;w ⟫
             ¼ ⟪Ow−1;w þ O1w;w jjDg · Dg jjOw−1;w þ O1w;w ⟫ þ ⟪Owþ1;w þ O2w;w jjDg · Dg jjOwþ1;w þ O2w;w ⟫
               þ ⟪O3w;w jjDg · Dg jjO3w;w ⟫ ≤ e−4γ ⟪Ow−1;w þ O1w;w jjOw−1;w þ O1w;w ⟫
               þ e−2γ ⟪Owþ1;w þ O2w;w jjOwþ1;w þ O2w;w ⟫ þ ⟪O3w;w jjO3w;w ⟫
             ¼ Pðg−1Þ ðwÞ þ e−4γ ⟪Ow−1;w þ O1w;w jjOw−1;w þ O1w;w ⟫ − ⟪O1w;w jjO1w;w ⟫ − ⟪Ow;w−1 jjOw;w−1 ⟫
               þ e−2γ ⟪Owþ1;w þ O2w;w jjOwþ1;w þ O2w;w ⟫ − ⟪O2w;w jjO2w;w ⟫ − ⟪Ow;wþ1 jjOw;wþ1 ⟫
             ≤ Pðg−1Þ ðwÞ þ f1; e−4γ g · ð⟪Ow−1;w þ O1w;w jjOw−1;w þ O1w;w ⟫ − ⟪O1w;w jjO1w;w ⟫ − ⟪Ow;w−1 jjOw;w−1 ⟫Þ
               þ f1; e−2γ g · ð⟪Owþ1;w þ O2w;w jjOwþ1;w þ O2w;w ⟫ − ⟪O2w;w jjO2w;w ⟫ − ⟪Ow;wþ1 jjOw;wþ1 ⟫Þ
             ¼ Pðg−1Þ ðwÞ þ f1; e−4γ g · ð⟪Ow−1;w þ Ow;w jjOw−1;w þ Ow;w ⟫ − ⟪Ow;w jjOw;w ⟫ − ⟪Ow;w−1 jjOw;w−1 ⟫Þ
               þ f1; e−2γ g · ð⟪Owþ1;w þ Ow;w jjOwþ1;w þ Ow;w ⟫ − ⟪Ow;w jjOw;w ⟫ − ⟪Ow;wþ1 jjOw;wþ1 ⟫Þ:                       ðD8Þ




                                                             041018-14
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                        PHYS. REV. X 15, 041018 (2025)

In the second line, we perform the orthogonal decom-                       are orthogonal. The three operators remain orthogonal
position Ow;w ¼ O1w;w þ O2w;w þ O3w;w , where O1w;w is pro-                after application of Dg , since Ow−1;w and Owþ1;w are
portional to Ow−1;w , and O2w;w is proportional to Owþ1;w , and
                                                                           eigenstates of the noise channel Dg (with eigenvalues
O3w;w is orthogonal to both. This is an orthogonal decom-
position because Ow−1;w and Owþ1;w are orthogonal, which                   e−2γ and e−γ , respectively). In the second to last line, we
follows since U †g P w−1 fOðg−1Þ gUg and U†g P wþ1 fOðg−1Þ gU g            use that


           Pðg−1Þ ðwÞ ¼ ⟪Ow;w−1 þ Ow;w þ Ow;wþ1 jjOw;w−1 þ Ow;w þ Ow;wþ1 ⟫
                         ¼ ⟪Ow;w−1 jjOw;w−1 ⟫ þ ⟪Ow;wþ1 jjOw;wþ1 ⟫ þ ⟪O1w;w jjO1w;w ⟫ þ ⟪O2w;w jjO2w;w ⟫ þ ⟪O3w;w jjO3w;w ⟫;                     ðD9Þ


which follows since the five operators in the second line are              current from w to w þ 1 is sourced from the operator’s
orthogonal to one another. Finally, in the last line, we use               support on weight w. To make this precise, let us observe
the notation f1; e−4γ g and f1; e−2γ g to denote that the                  Eq. (D11) with k ¼ w. The rightmost term is precisely the
bound holds for either choice of constant, where one can                   sum we would like to bound. Inverting the inequality, taking
make the choice independently between the two terms.                       the constant e−4γ for each term in the first sum, and using
Recognizing the first three terms in parentheses as JðgÞ ðwÞ               that PðgÞ ðw − 1Þ ≥ 0, we have
and the latter three terms as −JðgÞ ðw þ 1Þ, we have the
                                                                            g
                                                                            X                                                  g
                                                                                                                                X          
simpler bound,                                                                      ðhÞ                    ð0Þ           −4γ          ðhÞ
                                                                                   J ðw þ 1Þ         ≤ P ðwÞ þ e                      J ðwÞ :
      ðgÞ              ðg−1Þ                 −4γ      ðgÞ
    P ðwÞ ≤ P                  ðwÞ þ f1; e         g · J ðwÞ                 h¼1                                                h¼1

                                                                                                                                             ðD13Þ
                   − f1; e−2γ g · JðgÞ ðw þ 1Þ;                    ðD10Þ
                                                                           This bounds the net current from w to w þ 1 by the initial
where again the bound holds for any choice of the                          norm on w, plus the net current from w − 1 to w discounted
constants. When J ðgÞ ðwÞ is positive, the stronger bound                  by e−4γ. We can iterate over the weight to obtain
is obtained by taking the second constant in the first term,
and when it is negative, the first constant. The reverse holds              g
                                                                            X                           X
                                                                                                         w
                                                                                    ðhÞ
for the JðgÞ ðw þ 1Þ term. To summarize, increases in                              J ðw þ 1Þ         ≤           e−4γðk−1Þ · Pð0Þ ðw þ 1 − kÞ:
PðgÞ ðwÞ are discounted by a factor e−4γ or e−2γ due to                      h¼1                         k¼1

gate-based noise, while decreases are not.                                                                                                   ðD14Þ
   We would like to utilize our update rule, Eq. (D10), to
bound the cumulative norm above a threshold weight w. To                   Inserting into Eq. (D12), we find
begin, we can iterate Eq. (D10) over each gate h ¼ 1; …; g
in the circuit to obtain                                                                                 X
                                                                                                         w
                                                                           QðgÞ ðwÞ ≤ Qð0Þ ðwÞ þ               e−4γk · Pð0Þ ðw þ 1 − kÞ:     ðD15Þ
                      X
                       g                                                                                k¼1
PðgÞ ðkÞ ≤ Pð0Þ ðkÞ þ    f1; e−4γ g · JðhÞ ðkÞ
                                h¼1                                        The kth term in the sum corresponds to operators that begin
                 X
                 g                                                         at weight w þ 1 − k and evolve to weight greater than w. We
             −         J ðhÞ ðk þ 1Þ;                              ðD11Þ   find that such operators’ contribution to QðgÞ ðwÞ is dis-
                 h¼1                                                       counted by at least e−4γk , since they have participated in at
                                                                           least k gates. Expressing Pð0Þ ðw þ 1 − kÞ and Qð0Þ ðwÞ in
where we choose the constant 1 for each term in the second
                                                                           terms of their values before readout noise, we have
sum, and for convenience change the variable from w to k.
To bound the cumulative weight distribution above weight                                                   X
                                                                                                           w
w, we can sum over k ¼ w þ 1; …; N. Taking the constant                    QðgÞ ðwÞ ≤ e−2γw ·QðwÞþ                e−4γk ·e−2γðwþ1−kÞ ·Pðwþ1−kÞ
e−4γ for k ¼ w þ 1, and the constant 1 for all other k, we find                                             k¼1
                                                                                          −2γðwþ1Þ
                                            X
                                             g                                      ≤e              ·jjOjj2F ;                              ðD16Þ
     ðgÞ               ð0Þ            −4γ
   Q ðwÞ ≤ Q ðwÞ þ e                              JðhÞ ðw þ 1Þ :   ðD12Þ
                                            h¼1
                                                                           as desired. The right-hand side can be improved to
                                                                           e−4γðwþ1=2Þ · jjOjj2F if the initial observable has weight one.
We would like to bound the sum within the parentheses                         We now turn to the second inequality in the lemma. Our
above. Intuitively, the sum cannot be too large, since the net             classical algorithm truncates high-weight components of


                                                                     041018-15
SCHUSTER, YIN, GAO, and YAO                                                                           PHYS. REV. X 15, 041018 (2025)

ÕðtÞ after each layer of the circuit. As aforementioned, we                                         X qﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
                                                                                                     d
                                                                               ðdÞ      ðdÞ                 ðtÞ
denote the final gate in layer t as gt , so that the truncation          jjO         − Õ jjF ≤                Q̃ ðlÞ
occurs in between gates gt and gt þ 1. To begin, note that                                           t¼0
                                                                                                               d       1=2
the truncation in our classical algorithm cannot increase the                                     pﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ X    ðtÞ
operator weight distribution. This means that the upper                                          ≤ dþ1            Q̃ ðlÞ
                                                                                                                  t¼0
bounds Eqs. (D4) and (D10) continue to apply to noisy                                             pﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
quantum circuit with truncation. Moreover, for the specific                                      ≤ d þ 1e−γðlþ1Þ jjOjjF ;             ðD21Þ
weight w ¼ l, our upper bound on the cumulative weight
distribution can be strengthened to                                    where in the second line we apply the Cauchy-Schwarz
                                                                       inequality, and in the third line we apply Lemma D1.
                                 X
                                  gt                                     From Lemma B1, the above bound on the Frobenius
             Q̃ðtÞ ðlÞ ≤ e−4γ                J̃ðhÞ ðl þ 1Þ ;   ðD17Þ   norm of OðdÞ − ÕðdÞ leads to an upper bound on the root-
                                 h¼gt−1 þ1                             mean-square error for any low-average ensemble:
                                                                                                                           1=2
                                                                                 1 X
since the norm above l is reset to zero by the truncation                               jtrðρOðdÞ Þ − trðρÕðdÞ Þj2
                                                                                jEj   ρ
after layer t − 1. Here, J̃ðgÞ ðlÞ is defined analogous to                       pﬃﬃ pﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
JðgÞ ðlÞ, but with Õ instead of O. Summing over the layers                    ≤ c d þ 1 · e−γðlþ1Þ · jjOjjF :                        ðD22Þ
t, we have                                                                                  pﬃﬃ
                                                                       For a desired error ε cjjOjjF, it suffices to take
X
d                                      g
                                        X d
                                                                                                     pﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
       ðtÞ         ð0Þ
      Q̃ ðlÞ ≤ Q̃ ðlÞ þ e        −4γ           ðhÞ
                                              J̃ ðl þ 1Þ ;     ðD18Þ                              1     dþ1
                                                                                               l ≥ log               − 1:             ðD23Þ
t¼0                                     h¼1                                                       γ       ε

where the right-hand side is now the same quantity we                     Run-time of algorithm. We now turn to the complexity of
bounded for the first inequality. Repeating the steps of that          classically computing the expectation value trðρi ÕðdÞ Þ. As
proof, we find                                                         described in the main text, we do so by simulating the time
                                                                                            P            ðtÞ
                                                                       evolution of ÕðtÞ ¼ P∶w½P≤l cP P layer by layer in the
                X
                d                                                      Pauli basis. This requires keeping track of the real-valued
                       Q̃ðtÞ ðlÞ ≤ e−2γðlþ1Þ · jjOjj2F ;       ðD19Þ                 ðtÞ
                                                                       coefficients cP for all Pauli operators with weight less than
                 t¼0
                                                                       l. There are

as desired.                                                        ▪           X
                                                                               l
                                                                                       n
                                                                                                      
                                                                                                       n                 n − l þ 1 3 ð3nÞl
                                                                       Dl ¼                    ·3 ≤
                                                                                                 k
                                                                                                                · 3l ·               ≤
                                                                               k¼0     k                   l             n − 43 l þ 1 2 l!
                   2. Analysis of algorithm
                                                                                                                                      ðD24Þ
   We now apply our bound on operator weight distribu-
tions to prove Theorem 2. As for Theorem 1, we break our               such coefficients. The sum counts the number of Pauli
proof into two parts, which address the accuracy and run-              operators with weight k by first counting the number of sets
time of Algorithm 2, respectively.                                     of k qubits, ðnkÞ, on which the Pauli has support, and then
   Accuracy of algorithm. Our classical algorithm truncates
                                                                       multiplying by the number of Pauli operators on those k
operator components with weight greater than l in between
                                                                       qubits, 3k . The second inequality upper bounds the sum
each layer of the circuit. Each truncation can increase the
                                                                       when l ≤ 3n=4, and the final inequality upper bounds the
distance between the time-evolved operator OðtÞ and our                fraction by 3=2, which applies for l ≤ n=2.
approximation ÕðtÞ by at most                                            At the beginning of our algorithm, we initialize the
                                                                                     ð0Þ
                                                                       coefficients cP by computing the Pauli coefficients of O.
jjOðtÞ − ÕðtÞ jjF ≤ jjOðt−1Þ − Õðt−1Þ jjF                            As stated in the theorem, we assume that each coefficient
                                                                       can be computed efficiently, i.e., in Oð1Þ time [121], and
                       þ jjP >l fDt fU†t Õðt−1Þ Ut ggjjF ;    ðD20Þ   thus the entire vector in OðDl Þ time. At the end of our
                                                                       algorithm, we compute the trace trðρi ÕðdÞ Þ by computing
by the triangle inequality. The latter term is precisely the           the Pauli coefficients trðρPÞ of ρ and taking their inner
                                                                                          ðdÞ
square root of Q̃ðtÞ ðlÞ, the cumulative weight distribution           product with cP . Again, if each coefficient can be
for our approximation ÕðtÞ . Summing over time steps                  computed in Oð1Þ time, then the expectation value can
t ¼ 0; …; d, we have                                                   be computed in OðDl Þ time.


                                                                 041018-16
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                  PHYS. REV. X 15, 041018 (2025)

   We update the coefficients from layer to layer via                      and
Eq. (8) of the main text, where the transition amplitudes                                                     pﬃﬃﬃﬃﬃﬃ  
                                                Q
 ðtÞ
aQP are computed from the depth-1 unitary Ut ¼ g U g as                                  space ¼ O nð1=γÞ log ð dþ1=εÞ−1 :         ðD29Þ

       1                                                                 This concludes our proof.                                    ▪
 ðtÞ
aPQ ≡ n tr QUt PU †t
       2
       Y1                                                                        APPENDIX E: CLASSICAL ALGORITHMS
     ¼      trsuppðgÞ ðQsuppðgÞ · Dg fU †g PsuppðgÞ Ug gÞ:         ðD25Þ             FOR SAMPLING FROM NOISY
          4
        g                                                                               QUANTUM CIRCUITS

The product runs over all gates g in Ut , where suppðgÞ                       In select cases, our classical algorithms can also be
denotes the pair of qubits in gate g. We see that the n-qubit              leveraged to sample from noisy quantum circuits. In sam-
transition amplitudes factorize into a product of two-qubit                pling, we are interested in reproducing the statistics when the
transition amplitudes. Each two-qubit amplitude can be                     final state of the circuit is measured in the computational
computed in Oð1Þ time, and thus the n-qubit amplitude in                   basis. From Born’s rule, each measurement produces an n-bit
OðnÞ time.                                                                 string z with probability pρ;C ðzÞ ¼ hzjCfρgjzi. In general,
   A naive algorithm to update the coefficients would                      sampling is a strictly harder task than computing expectation
                                        ðtÞ
compute each transition amplitude aQP individually and                     values, since the distribution pρ;C ðzÞ contains information
                      2
thus require Oðn · Dl Þ time. We can moderately improve                    about exponentially many expectation values in the compu-
this scaling by leveraging the sparsity of the transition                  tational basis.
                                                                              We provide three algorithms for sampling from noisy
amplitudes. Note that the support of U t PU †t consists of at
                                                                           quantum circuits. The first two are direct extensions
most 2l qubits: the qubits in suppðPÞ and those that they
                                                                           of Theorems 1 and 2, and apply to any circuit on most
couple to under Ut. Thus, for each P, we only need to                      input states. Similar to previous works [26,31], we require
compute transitions to Q whose support lies within this                    one additional assumption: that the output distribution
set. There are at most ð3=2Þ3l 2ðllÞ ≤ ð3=2Þ12l such Q, by                 of the Pcircuit     anticoncentrates, in the sense that
a similar computation to Eq. (D24). Moreover, each                                      P
                                                                           ð1=jEjÞ ρ z pρ;C̃ ðzÞ2 ¼ Oð2−n Þ for the ensemble
transition amplitude can be computed from a product
                                                                           E ¼ fρg. Here, C̃ denotes the circuit C with the readout
of only l two-qubit transition amplitudes, in contrast to
                                                                           noise channel omitted. Anticoncentration guarantees that
the naive number n=2. Together, these lead to a run-time
                                                                           most expectation values in the computational basis are
of OðDl · 12l · lÞ per circuit layer.
                                                                           close to zero. In the presence of readout noise, this enables
   Inserting our bound on Dl and summing over the d
                                                                           one to sample from pρ;C ðzÞ by computing only a small
circuit layers, our algorithm requires
                                                                           number of low-weight expectation values [26], which we
                                                                         show can be done efficiently using our Algorithms 1 and 2
                        ð36nÞl
       time ¼ O d · l ·          ¼ Oðd · nl Þ;                     ðD26Þ   (see Appendix E for details).
                          l!                                                  Theorem E1 (Sampling from noisy quantum circuits;
                                                                           informal). Consider a noisy quantum circuit C and a low-
where d is the depth of the circuit. On the right, we simplify             average ensemble E ¼ fρg whose Pauli coefficients can be
the expression by using l · 36l =l! ¼ Oð1Þ. (For moderate                  efficiently computed. P Assume
                                                                                                        P the output distribution anti-
values of l ≲ 36, this may incur a large constant prefactor                concentrates, ð1=jEjÞ ρ z pρ;C̃ ðzÞ2 ¼ Oð2−n Þ. Then for
in practice, although it will still be much smaller than the               either uniform or gate-based noise, there is a classical
additional factor of nl in the naive update algorithm.) The                algorithm to sample from pρ;C ðzÞ within root-mean-square
algorithm uses space                                                       total variational distance ε in quasipolynomial time.
                                                                            Our third sampling algorithm specializes to quantum
                          ð3nÞl                                            circuits with low depth. In such circuits, one can exactly
                space ¼ O         ¼ Oðnl Þ;                        ðD27Þ
                            l!                                             compute low-weight expectation values by restricting to the
                                                                           light cone of the observable of interest. Using this property,
                                                             ðtÞ           we show that one can classically sample from any low-
proportional to the number of coefficients cP . These
requirements are comparable to performing exact time                       depth circuit with readout noise, as long as the output
evolution in a system of neff ∼ l logðnÞ qubits.                           distribution of the circuit anticoncentrates. This holds even
  For a desired error ε, we take l according to Eq. (D23).                 when the circuit gates themselves are noiseless.
Plugging into the above, this gives                                           Theorem E2 (Sampling from low-depth quantum circuits
                                                                           with readout noise; informal). Consider a quantum circuit C
                                       pﬃﬃﬃﬃﬃﬃ                           with depolarizing readout noise and a state ρ whose Pauli
               time ¼ O d · nð1=γÞ log ð dþ1=εÞ−1                  ðD28Þ   coefficients can be efficiently computed. Assume the output


                                                                     041018-17
SCHUSTER, YIN, GAO, and YAO                                                                                PHYS. REV. X 15, 041018 (2025)
                                P
distribution anticoncentrates, z pρ;C̃ ðzÞ2 ¼ Oð2−n Þ. If the                    Proof of Lemma E1. Our goal is to sample from the
circuit has depth d ¼ Oðlog nÞ and is geometrically local, or                  probability distribution:
has depth d ¼ Oðlog log nÞ more generally, then there is
classical algorithm to sample from pρ;C ðzÞ within total                                           pDfρg ðsÞ ¼ hsjDfρgjsi:                 ðE3Þ
variational distance ε in quasipolynomial time.
   Quantum advantages for sampling from low-depth cir-                         Let us decompose the projector jsihsj as a sum of Pauli
cuits are highly sought, since low-depth circuits are generally                operators,
less susceptible to experimental noise. Nonetheless, our
result shows that in many cases even a small amount of                                                      1 X
                                                                                               jsihsj ¼                   ð−1Þs·t Zt ;     ðE4Þ
readout noise can preclude any such advantage [122].                                                        2n t ∈ f0;1gn
   In the following subsections, we first establish the
reduction from noisy circuit sampling to expectation values                                  P
in the presence of anticoncentration, and then prove the                       where s · t ≡ i si ti , and Zt ¼⊗ni¼0 ðZi Þti denotes the
theorems above.                                                                Pauli operator with identity support where ti ¼ 0 and Z
                                                                               support where ti ¼ 1. Since w½Zt  ¼ jtj, we have
    1. Reduction from noisy circuit sampling with
        anticoncentration to expectation values                                                       1X
                                                                                         pDfρg ðsÞ ¼      ð−1Þs·t trðZt DfρgÞ
   To extend our classical algorithms for expectation values                                         2n t
to sampling, we leverage the following lemma. The lemma                                               1 X −γjtj
follows almost entirely from Ref. [26], by adapting their                                           ¼ n   e ð−1Þs·t trðZt ρÞ:              ðE5Þ
                                                                                                     2 t
Theorem 4 to state ensembles and neglecting the compo-
nents of the theorem that are specific to IQP circuits.
   Lemma E1. Consider any ensemble of states E ¼ fρg,                          This can be viewed as a Fourier transform over Zn2 of the
sampled in the computational basis with readout noise γ per                    coefficients e−γjtj trðZt ρÞ.
qubit. Let                                                                        Following Ref. [26], our first step is to form a classical
                                                                               approximation qDfρg ðsÞ of the probability distribution
                        1 X nX                                                 pDfρg ðsÞ. We do so via two steps. First, we truncate all
                 ᾱ ¼         2     pρ ðsÞ2            ðE1Þ
                       jEj ρ      s                                            terms in Eq. (E5) with high-weight, jtj > ls . Second, we
denote the mean collision probability of the output dis-                       replace each remaining expectation value trðZt DfρgÞ
tribution before readout noise, multiplied by 2n. Suppose                      with its classical estimate. PWe denote the classical estimate
that, for some ls , one can compute expectation values in ρ                    as at ; we have ð1=jEjÞ ρ jat − trðZt DfρgÞj2 ≤ ε02 by
of Pauli operators with weight less than ls to within root-                    assumption. Together, these two steps give a classical
mean-square error ε0, in time χ. Then there exists a classical                 approximation:
algorithm to simulate sampling to within root-mean-square
total variational distance:                                                                                   1 X
                                                                                              qDfρg ðsÞ ≡                ð−1Þs·t at :      ðE6Þ
                                                                                                              2n t∶jtj≤l
                 pﬃﬃ qﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ                                                        s

            ε ¼ 6 2 ε02 ðnls þ 1Þ þ ᾱe−2γls :                          ðE2Þ
                                                                               The approximation may take small negative values, and is
The classical algorithm takes time Oðχ · nls þ1 Þ per sample.                  thus not guaranteed to be a probability distribution.
  The lemma also holds for any fixed state ρ, by taking the                    However, one can show that it is close to pDfρg ðsÞ in
ensemble E ¼ fρg to be composed of only a single state.                        mean-square total variational distance:

 1 X X                       2   2n X X
       jp
      s DfρgðsÞ
                − qDfρg ðsÞj   ≤          ðpDfρg ðsÞ − qDfρg ðsÞÞ2
jEj ρ                            jEj ρ s
                                                                                          
                                  1 X X                  2       2
                                                                    X
                                                                          −2γjtj         2
                               ¼             trðZt DfρgÞ − at þ          e       trðZt ρÞ
                                 jEj ρ jtj≤l                       jtj>l
                                                                    s                          s

                                                    X                        1 XX                    X                         1 XX
                                                ≤       ε02 þ e−2γðls þ1Þ ·             trðZt ρÞ2 ≤       ε02 þ e−2γðls þ1Þ ·         trðZt ρÞ2
                                                  jtj≤l
                                                                            jEj ρ jtj>l             jtj≤l
                                                                                                                              jEj ρ t
                                                         s                           s                 s

                                                    X                        1 X nX
                                                ≤       ε02 þ e−2γðls þ1Þ ·       2   pρ ðsÞ2 ¼ ðnls þ 1Þε02 þ e−2γðls þ1Þ · ᾱ:           ðE7Þ
                                                  jtj≤l
                                                                            jEj ρ   s
                                                         s




                                                                         041018-18
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                                     PHYS. REV. X 15, 041018 (2025)

In going from the first to second line, we use Eqs. (E5) and                              one can enumerate each low-weight t and compute the sum
(E6) to expand the first and second copy of pDfρg ðsÞ,                                    on the right-hand side exactly term by term. This requires
qDfρg ðsÞ as a sum over variables t and t0 . Because of the                               time χðnls þ 1Þ. Generating a single sample requires that
                             0
sign factor ð−1Þs·t ð−1Þs·t , the sum over s gives a δ function                           we compute one marginal for each value of k ¼ 1; …; n
2n δt;t0 . Using the δ function to eliminate the sum over t0                              [26], and thus requires time χðnls þ 1Þn.                ▪
gives the second line. In going from the fourth to fifth lines,
we reverse these steps to convert the second sum over t to a                                           2. Proofs of sampling algorithms
sum over s. The final line uses the fact that there are at most                              We now provide the detailed statements and proofs of
nls þ 1 bit strings with jtj ≤ ls , as well as the definition of                          our theorems on sampling from noisy quantum circuits.
the mean collision probability ᾱ.                                                        As before, we let C̃ denote the circuit C with the readout
   To translate this approximation into a sampling algo-                                  noise channel omitted. For general circuits, we have the
rithm, we use Lemma 10 in Ref. [26]. The lemma shows                                      following.
that one can construct a true probability distribution                                       Theorem E3 (Sampling from noisy quantum circuits;
q̃Dfρg ðsÞ from qDfρg ðsÞ, at the cost of only a slightly larger                          formal). Consider a noisy quantum circuit C and a low-
total variational distance,                                                               average ensemble E ¼ fρg, where the Pauli coefficients of
          X                                                                               each ρ can be efficiently computed. Let ᾱ denote the mean
             jpDfρg ðsÞ − q̃Dfρg ðsÞj ≤ 4ηρ =ð1 − ηρ Þ;                                   collision probability of C̃fρg multiplied by 2n. For circuits
              s                                                                           with uniform noise, there is a classical algorithm to sample
                     X
where ηρ ≡            jpDfρg ðsÞ − qDfρg ðsÞj;                                     ðE8Þ   from Cfρg to within root-mean-square total variational
                         s                                                                distance ε that runs in time:

for each ρ. We can translate this to the mean-square total                                                      nO(γ
                                                                                                                        −3 logð1=γÞ logðᾱ=εÞ)
                                                                                                                                                 :                     ðE11Þ
variational distance using
                                                                                          For circuits with gate-based noise, there is a classical
                1 X X                                 2                                   algorithm that runs in time:
                              jp
                             s Dfρg
                                    ðsÞ − q̃Dfρg ðsÞj
               jEj ρ
                                                                                                          nO(γ
                                                                                                                   −2 logðnÞ logðᾱ=εÞþγ −1 logðdÞ)
                                                                                                                                                      :                ðE12Þ
                   1 X 2            1 X            4ηρ 2
               ≤               2 þ
                  jEj ρ∶η >1=3     jEj ρ∶η ≤1=3 1 − ηρ                                    In both cases, the run-time is quasipolynomial so long as
                             ρ                           ρ

                             2                      X                                     ᾱ ¼ polyðnÞ. For simplicity of presentation, in the main
                           ε          1
                  ≤ 22          þ 62             η2 ≤ 72ε2 ;                       ðE9Þ   text we take ᾱ ¼ Oð1Þ, which is referred to as anticoncen-
                         ð1=3Þ2      jEj ρ∶η ≤1=3 ρ                                       tration [26,31].
                                                     ρ                                                                                         pﬃﬃﬃﬃﬃ
                                                                                             Proof of Theorem E3. We take ls ¼ ð1=γÞ logð 2ᾱ=εÞ
where we denote the right-hand side of the final line of                                  in Lemma E1 to ensure that the second term in the error is
Eq. (E7) as ε2 . In the first line, we use that the total                                 small. This requires 2ε02 ≤ ε2 =ðnls þ 1Þ for the first term.
variational distance is upper bounded by 2 for any two                                    For circuits with uniform noise, we can compute the
probability distributions, which allows us to replace                                     expectation value of any Pauli operator in time χ ¼
4ηρ =ð1 − ηρ Þ by 2 when ηρ > 1=3. In the second line,                                                       2
                                                                                          ð1=ε0 ÞO(logð1=γÞ=γ ) (Theorem 1). From Lemma E1, this
we use Markov’s inequality to bound the probability                                       gives a total run-time
that ηρ > 1=3.
                                                                                                                                       2                  −3 logð1=γÞ logðᾱ=εÞ)
   To sample from q̃Dfρg ðsÞ, we invoke Sec. 3.2 of                                       Oðχ · nls þ1 Þ ¼ ðnls =ε2 ÞO(logð1=γÞ=γ ) ¼ nO(γ                                         ;
Ref. [26]. The section provides a simple sampling algo-
                                                                                                                                                                       ðE13Þ
rithm, given the ability to compute marginals of the original
approximation qDfρg ðsÞ. Any such marginal can be com-
                                                                                          which establishes Eq. (E11). Similarly, for circuits with
puted exactly by expanding qDfρg ðsÞ as in Eq. (E6):                                      gate-based noise, setting χ according to Eq. (D28) gives a
  X                                                                                       total run-time
                                 1 X X
              qDfρg ðsÞ ¼                             ð−1Þs·t aP
s∶s1k ¼y
                                 2n jtj≤l s∶s1k ¼y                                                   l
                                                                                          nO(ð1=γÞ logðdn s =εÞ) ¼ nO(γ
                                                                                                                          −2 logðnÞ logðᾱ=εÞþγ −1 logðdÞ)
                                                                                                                                                               ;       ðE14Þ
                                         s

                                 1 X
                             ¼               δtkþ1n ;0 · ð−1Þy·t1k · aP :   ðE10Þ   which establishes Eq. (E12).                              ▪
                                 2n jtj≤l                                                    For low-depth circuits, we have the following.
                                         s

                                                                                             Theorem E4 (Sampling from low-depth quantum circuits
Here, the left-hand side is the marginal distribution on the                              with readout noise; formal). Consider any circuit C that is
first k qubits, where y ∈ f0; 1gk . To compute the marginal,                              either depth d ¼ O( logðnÞ), and geometrically local, or


                                                                                    041018-19
SCHUSTER, YIN, GAO, and YAO                                                                     PHYS. REV. X 15, 041018 (2025)

depth d ¼ O log ( logðnÞ), and contains readout noise γ per             N i;t ¼ Dγ ∘ Ñ i;t , where Ñ i;t is the same noise channel
qubit. Let ρ be any state whose Pauli coefficients can be               with each Pauli noise rate γ i;t
                                                                                                       P replaced by γ P − γ. Note that
                                                                                                                       i;t
efficiently computed, and α denote the collision probability
                                                                        Ñ i;t is a valid quantum channel, since γ i;t
                                                                                                                    P − γ ≥ 0 for all i,
of C̃fρg multiplied by 2n. There is classical algorithm to
sample from Cfρg within total variational distance ε in                 t, P. Since Ñ i;t is a single-qubit channel, we can absorb its
time,                                                                   action into the action of the gate preceding it. In this way,
                                                                        one can rewrite the original circuit with arbitrary noise
                              −1 logðᾱ=εÞðlog nÞc )                    channels in the depolarizing class as a new circuit with only
                       2O(γ                            ;     ðE15Þ
                                                                        depolarizing noise channels. Our classical algorithms
where c ¼ D for geometrically local circuits in spatial                 immediately apply to the new circuit, and hence to the
dimension D, and c ¼ Oð1Þ for general circuits.                         original circuit as well.
   Proof of Theorem E4. The theorem follows from a
simple observation: that expectation values of low-weight               APPENDIX G: EXTENSION TO CIRCUITS WITH
Pauli operators can be computed exactly in any circuit of                  NOISE ONLY IN NON-CLIFFORD GATES
sufficiently low depth. More precisely, any Pauli operator                 In this appendix, we show that both of our classical
with initial weight at most ls can have support on at most              algorithms naturally extend to settings where noise occurs
Oðls · dD Þ or Oðls · 2d Þ qubits after Heisenberg time                 only in non-Clifford gates, and Clifford gates are imple-
evolution. The first scaling applies to geometrically local             mented noiselessly. Intuitively, this follows because our
circuits, and the second to any circuit. The expectation                algorithms track operators in the Pauli basis. Clifford gates
value of the Pauli operator can therefore be computed                   permute the Pauli operators, and thus do not increase the
exactly in time 2Oðls ·d p
                           DÞ
                                  2Oðls ·2 Þ. Therefore, setting ε0 ¼
                                           d
                              or
                              ﬃﬃﬃﬃﬃ                                     complexity of our classical approximation. We formalize
0 and ls ¼ γ −1 logð6 2ᾱ=εÞ in Lemma E1, one can                       this in the following extension of our main result.
classically sample from the circuit in time                                Extension G1 (Classical algorithm for noisy quantum
2Oðls ·d ÞþO(ls ·logðnÞ) or 2Oðls ·2 ÞþO(ls ·logðnÞ). Setting d ¼       circuits with non-Clifford noise). Consider the settings of
        D                                d


O( logðnÞ) for geometrically local circuits, the first scaling          Theorems 1 and 2 of the main text but where (i) for the
                                       −1
becomes 2O(ls ·logðnÞ ) ¼ 2O(γ logðᾱ=εÞ·logðnÞ ) . Meanwhile,
                         D                          D                   uniform noise model, noise occurs only in circuit layers that
setting d ¼ O( logðlogðnÞÞ) for general circuits, the second            contain non-Clifford gates and during readout, and (ii) for
                                    Oð1Þ      −1           Oð1Þ         the gate-based noise model, noise occurs only in non-
scaling becomes 2ls ·logðnÞ ¼ 2γ logðᾱ=εÞ·logðnÞ . This                Clifford gates and during readout. Then all of the stated
concludes our proof.                                                ▪   results continue to hold, with the scaling in Theorem 2
                                                                        replaced by
         APPENDIX F: EXTENSION TO ANY                                                                         pﬃﬃﬃﬃﬃﬃ 
          SINGLE-QUBIT NOISE CHANNEL                                                     O d · m2 · nð2=γÞ logð dþ1=εÞ ;        ðG1Þ
           IN THE DEPOLARIZING CLASS
                                                                        where d is the number of circuit layers containing non-
   In this appendix, we briefly discuss the extension of our
                                                                        Clifford gates, and m is the number of Pauli operators with
results to any single-qubit noise channel in the depolarizing
                                                                        nonzero coefficients in O and weight less than or equal
class. The depolarizing class of noise channels corresponds
                                                                        to l.
to all channels whose sole steady state is the maximally
                                                                           The result continues to hold even if the readout is
mixed state. Any single-qubit noise channel N in the
                                                                        noiseless, provided that O is a sum of polynomially many
depolarizing class can be written as a composition of
                                                                        Pauli operators, m ¼ polyðnÞ.
unitary operations and a Pauli noise channel [14],
                                                                           Proof of Extension G1. We provide separate proofs for
N ð·Þ ¼ UN Pauli (Vð·ÞV † )U † , where U; V ∈ Uð2Þ and                  our algorithms for uniform and gate-based noise
N Pauli ðPÞ ¼ e−γP P for each Pauli P ∈ fX; Y; Zg. Here,                   Uniform noise. Let us begin with our algorithm for
N Pauli ð1Þ ¼ 1 and γ P > 0.                                            uniform noise. We use the same approximation Õ of the
   We consider any quantum circuit with either uniform or               Heisenberg time-evolved operator as in Eq. (C2), but where
gate-based noise, in which each single-qubit noise channel              U t now corresponds to the unitary of the tth non-Clifford
is in the depolarizing class. The noise channel, N i;t                  layer combined with all of the ensuing Clifford layers
(specified by U i;t ; V i;t ; γ i;t
                                P ), may depend arbitrarily on          before the (t þ 1)th non-Clifford layer. One can verify that
the qubit and circuit layer. We assume only that each                   Eq. (C2) still holds, because it relies only on the super-
Pauli noise rate is at least constant, γ i;t
                                         P ¼ Ωð1Þ, with respect         unitarity of U t . Therefore, as before, the approximation Õ is
to the system size n.                                                   accurate with small Frobenius error [Eq. (C6)] provided
   Our classical algorithms generalize as follows. We set               that we choose the truncation weight l as in Eq. (C9).
γ ¼ mini;t γ i;t
             P ¼ Ωð1Þ to be the smallest Pauli noise                    Viewing Eq. (C9), the depth d now corresponds to the
rate. We can then rewrite each noise channel as                         number of non-Clifford layers, and, as before, we have


                                                                 041018-20
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                PHYS. REV. X 15, 041018 (2025)

d < γ −1 logð1=εÞ before the system approaches the max-                  From this definition, we can also define a non-Clifford
                                                                                              ðgÞ
imally mixed state.                                                   distance distribution, Pnc ðwÞ, and cumulative non-Clifford
   It remains to show that our algorithm remains efficient—                                    ðgÞ
                                                                      distance distribution, Qnc ðwÞ, for the time-evolved oper-
i.e., that the scaling of the number of Pauli paths in Eq. (C2)
                                                                      ator O. These measure the norm of OðgÞ on Pauli operators
is unchanged. Following Ref. [31], we count the number of
                                                                      with distance w at circuit gate g, and are analogous to the
Pauli paths for each fixed sequence ðl0 ; …; ld Þ individu-
                                                                      weight distribution and cumulative weight distribution
ally, where l0 þ    þ ld ≤ l, since there are at most 2l           defined previously. (One can think of this as working in
such sequences. One starts from the non-Clifford layer with           a “rotating frame” determined by the action of the Clifford
the smallest weight lt , at the beginning of which there are          gates.) From the definition of the non-Clifford distance, the
at most ð3nÞl=d possible Pauli operators (since one must have                          ðgÞ
lt ≤ l=d). If O is a sum of polynomially many Pauli                   distribution Pnc ðwÞ begins as a δ function at zero. The
operators, we start instead at the final circuit layer t ¼ 0, in      distributions do not change under the action of any Clifford
which case this factor is replaced by m. The ensuing non-             gate, and shift by at most one under each non-Clifford gate.
                                                                         With these definitions, one can easily repeat our proof of
Clifford layer can “split” each Pauli operator to at most 2Oðlt Þ
                                                                      Lemma D1 with non-Clifford gate-based noise instead of
new Pauli operators, whose number is unchanged by the
                                                                      two-qubit gate-based noise, and Clifford distance instead of
following Clifford layers. Thus, there are at most
                                                                      Pauli weight. The only change is the factor of e−4γ is
min (ð3nÞl=d ; m) · 2Oðlt Þ possible Pauli operators at the           replaced with e−2γ throughout the proof, where the
beginning of layer t þ 1. Among these, we count only those            replacement arises because an operator can increase in
of weight ltþ1 . At the next non-Clifford layer, each of these        non-Clifford distance despite having support only on one
Pauli operators can split to at most 2Oðltþ1 Þ new Pauli operators,   qubit in the gate and not two. The end result is that at any
and so on. Iterating this argument, our upper bound on                layer t, the cumulative non-Clifford distance distribution is
the number of Pauli paths is exactly the same as before                            ðtÞ
                                                                      less than Qnc ðwÞ ≤ e−2γðwþ1Þ jjOjj2F for all w. If we form a
[Eq. (C10)], which leads to the same run-time as in Theorem 1
                                                                      low-distance approximation,
of the main text.
   Gate-based noise. We now turn to our algorithm for gate-                                ðtÞ
                                                                                                       X            ðtÞ
based noise. We incorporate the non-Clifford noise model                                 Õnc ¼                 c̃P P;           ðG2Þ
into our algorithm by modifying our definition of the Pauli                                       P∶wnc ½P;C;t≤l

weight. In our original algorithm, the Pauli weight served as
                                                                      at each layer t, then we similarly have
a lower bound on the number of two-qubit gates required to            Pd       ðtÞ        −2γðlþ1Þ
grow our initial operator into a Pauli operator of interest. Since       t¼0 Q̃nc ðlÞ ≤ e          jjOjj2F .
each two-qubit gate damped the operator amplitude by a                   It remains only to bound the run-time of our classical
factor e−γ due to noise, we formed an accurate classical              approximation. This is determined by the number of low-
approximation of our time-evolved operator by keeping track           non-Clifford-distance Pauli operators that we must keep
only of low-weight Pauli operators. Applying this intuition to        track of. We begin with the operator O acted on by the
the non-Clifford noise model, we should introduce a modified          readout noise channel. Because of the readout noise, we can
weight that lower bounds the number of non-Clifford gates             truncate all Pauli operators in O with weight above l. From
required to transform our initial operator into some Pauli of         this starting point, each non-Clifford gate can increase the
interest. This modification will depend on the circuit archi-         number of accessible Pauli operators by at most a constant
tecture (i.e., the placement of the Clifford and non-Clifford         factor C: for T gates by a factor of 2, for general two-qubit
gates) as well as the choice of Clifford gates.                       non-Clifford gates by a factor of 15. There are ðnlnc Þ sets of l
   To write this down explicitly, for each observable O,              non-Clifford gates. Thus, there are at most mðnlnc ÞCl ≤
circuit C, and circuit layer t, we define the non-Clifford            mnlnc Cl =l! ¼ Oðmnlnc Þ possible Pauli operators with non-
distance wnc ½P; C; t as the minimal number of non-Clifford          Clifford distance ≤ l at any circuit layer, where m is the
gates in any Pauli path from Q at layer zero to P at layer t,         number of Pauli operators with nonzero coefficients in O
where Q is any Pauli operator with a nonzero coefficient in O.        and weight ≤ l. The coefficients can be updated one by one
For example, at layer zero, the set of Pauli operators in O have      in time Oðm2 n2lnc Þ. Repeating d times for each circuit layer,
non-Clifford distance zero and all other Pauli operators have         we arrive at the scaling in Eq. (G1).                           ▪
non-Clifford distance ∞. At later layers, any Pauli operator
that can be reached from Q in Ovia solely Clifford operations
                                                                           APPENDIX H: EXTENSION TO RANDOM
also has non-Clifford distance zero, at the layers at which it
                                                                                   NONUNITAL NOISE
can be reached. We emphasize that the definition of the non-
Clifford distances changes as we move through the circuit;              We now consider the extension of our classical algorithms
for example, a Pauli operator Q in O may have distance zero           to quantum circuits with nonunital noise. Unital noise
at time zero but distance > 0 at time one, depending on the           corresponds to any noise process that maps the maximally
Clifford gates between time zero and one.                             mixed state to itself, a primary example being depolarizing


                                                               041018-21
SCHUSTER, YIN, GAO, and YAO                                                                   PHYS. REV. X 15, 041018 (2025)

noise. Nonunital noise refers to noise processes that do not        with equal probability. This randomization is performed
preserve the maximally mixed state, such as spontaneous             implicitly in random circuits, via the random gates before and
emission noise (also referred to as amplitude damping).             after each noise channel. We emphasize that we are consid-
   Interestingly, the arguments in Ref. [14] prevent any            ering simulating a specific instance of the random nonunital
immediate extension of our results to nonunital noise. For          noise (with high success probability over the random
any local nonunital noise model, Ref. [14] provides a               instances), and not a mixture of the instances. Finally, as
scheme to perform fault-tolerant quantum computation for            with our previous results, we consider the performance of our
exponentially long times. Their scheme assumes that the             algorithm over an ensemble of input states.
circuit begins in the zero state, in contrast to the input state       This mild form of randomness neatly avoids the no-go
ensembles that we consider. However, for noise models that          results of Ref. [14], by ensuring that the gates in the circuit are
have a product state fixed point, such as spontaneous               decoupled from the structure of the nonunital noise. Thus,
emission, this can easily be circumvented. One simply               even though nonunital noise is present, the circuit cannot
needs to wait for some time O(γ −1 logðn=εÞ) before                 “take advantage” of it. Within this setting, we show that our
applying the circuit in Ref. [14], since after this time            classical algorithms in Theorems 1 and 2 of the main text
any input state will have become close to the fixed point.          apply equally well to circuits with nonunital noise.
   While these arguments exclude classical algorithms for              Extension H1 (Classical algorithm for random nonunital
arbitrary quantum circuits with nonunital noise, recent work        noise). Consider the settings of Theorems 1 and 2 of the
has shown that this may not be the case for restricted classes      main text, but with each local depolarizing channel Di
of circuits [36]. In particular, Ref. [36] introduces a classical   replaced by spontaneous emission Ai; in independently
algorithm for expectation values in random circuits with            random directions with rate γ s ≤ 4=7. Replace each error
nonunital noise. By taking each gate in the circuit to be           metric with its root-mean-square value over the random
independently random, one explicitly excludes the scheme in         direction. Then all of the stated results continue to hold,
Ref. [14] which opens the door to an efficient classical            with γ ¼ log (1=ð1 − γ s =2Þ) ≈ γ s =2 and the factor of d in
simulation. The algorithm in Ref. [36] runs in time                 Eq. (3) of the main text replaced by 1.
expðOf(γ −1 logðε−1 Þ)D gÞ for local observables in geomet-            If one considers instead a random quantum circuit with
rically local circuits in dimension D. This is polynomial in n      uniform spontaneous emission noise, for any circuit archi-
for D ¼ 1, and quasipolynomial for larger D. For nonlocal           tecture, then the run-time of our classical algorithm
observables, the run-time is instead exponential in n, and for      improves to
circuits without geometric locality, it is exponential in ε−1 .
   Our classical algorithms improve upon this performance                                 polyðnÞ · ð1=εÞOð1=γÞ ;                ðH3Þ
in two ways. First, we show that, in fact, a much milder
form of randomness is sufficient to achieve an efficient            if O is a sum of polynomially many Paulis operator,
classical simulation. We elaborate on this in the following
paragraph. Second, we show that, under this mild random-                         nð1=γÞ logð1=εÞ · ð1=εÞOð1=γÞ ;                 ðH4Þ
ness, our classical algorithms achieve run times matching
those in Theorems 1 and 2. Namely, our algorithm runs in            for any O.
polynomial time for any circuit architecture for large classes         We make a few additional remarks. First, for simplicity
of observables, and quasipolynomial time otherwise.                 of analysis, we restrict attention to spontaneous emission
   To elaborate on the first point, we consider quantum             noise as the prototypical example of nonunital noise.
circuits with arbitrary gates, and require only that each           We expect our results to generalize straightforwardly to
nonunital noise channel occurs in a random direction.               any strictly contractive nonunital noise channel [123].
Considering spontaneous emission specifically, our                  Second, the restriction to noise rates below a large
requirement translates to choosing each local spontaneous           threshold, γ s ≤ 4=7, is also chosen as a convenient
emission channel to emit from either the 1 to 0 state,              simplification for our proof. We do not expect larger
                                                                    noise rates to lead to harder classical simulations. Finally,
                                γ           γ                       as a stepping stone in our proof, we prove a general
Aþ fρg ¼ ρ þ γ s h1jρj1ij0ih0j − s j1ih1jρ − s ρj1ih1j;
                                 2           2                      lemma (Lemma H1) showing that expectation values in
                                                     ðH1Þ           circuits with random nonunital noise depend only on the
                                                                    final O(γ −1 logðn=εÞ) layers of the circuit for most input
                                                                    states. This extends a result of Ref. [36], and follows
or the 0 to 1 state,
                                                                    extremely quickly after we introduce the general frame-
                                γ           γ                       work of our proof.
A− fρg ¼ ρ þ γ s h0jρj0ij1ih0j − s j0ih0jρ − s ρj0ih0j;                Proof of Extension H1. The strategy of our proof is to
                                 2           2
                                                                    show that, while nonunital noise can increase the Frobenius
                                                     ðH2Þ           norm of Heisenberg time-evolved operators in certain


                                                             041018-22
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                PHYS. REV. X 15, 041018 (2025)

instances, it decreases the norm on average over the                   where the superoperator Ã is defined via
random directions of the noise channel. Thus, typical
instances of nonunital noise share key properties in                                Ã† f1g ¼ 1;
common with depolarizing noise.
   To show this, let us begin by writing down the action of                         Ã† fXg ¼ X;
the spontaneous emission channel in the Heisenberg                                  Ã† fYg ¼ Y;
picture:
                                                                                                  1 − γs          γs
                                                                                    Ã† fZg ¼              Z            1;        ðH7Þ
                 A† f1g ¼ 1;                                                                    1 − γ s =2    1 − γ s =2
                 A† fXg ¼ ð1 − γ s =2ÞX;                              and D is the depolarizing channel of strength
                 A† fYg ¼ ð1 − γ s =2ÞY;                              γ ¼ − logð1 − γ s =2Þ ≈ γ s =2.
                                                                          We will now show that, in expectation, Ã† does not
                 A† fZg ¼ ð1 − γ s ÞZ  γ s 1:              ðH5Þ      increase the Frobenius norm of any operator. Suppose that
                                                                       Ã† acts on one qubit of a larger system. Let us decompose
The key idea we use is to decompose the spontaneous                    an arbitrary operator O in terms of its support on that qubit,
emission channel into the product,                                     O ¼ 1 ⊗ O1 þ X ⊗ OX þ Y ⊗ OY þ Z ⊗ OZ .
                                                                       Considering the mean-square Frobenius norm over the two
                        A† ¼ Ã† ◯ D;                      ðH6Þ      possible directions of the noise channel, we have

                                                                              
                                                        ð1−γ s Þ2       γ 2s
    E jjÃ† fOgjj2F   ¼jjO1 jj2F þjjOX jj2F þjjOY jj2F þ        þ             jjOZ jj2F
                                                       ð1−γ s =2Þ2 ð1−γ s =2Þ2
                                                                                              
                              2     ð1−γ s Þ2     γ 2s               2       2        1−7γ s =4
                        ≤jjOjjF þ             þ            −1 jjOZ jjF ¼jjOjjF −γ s               jjOZ jj2F ≤jjOjj2F ;              ðH8Þ
                                   ð1−γ s =2Þ2 ð1−γ s =2Þ2                           ð1−γ s =2Þ2


where the final inequality holds if γ s ≤ 4=7. In the first line,         Uniform noise. For our Algorithm 1 for uniform noise,
we use that the cross terms between Z and 1 in Ã† fZg                we require three small additional modifications. The first
vanish in expectation.                                                 two modifications arise because the presence of nonunital
   To connect this to the accuracy of our classical algo-              noise changes our counting of the number of valid Pauli
rithms, let us absorb each superoperator Ã into its                  paths, since nonunital noise can transform nonidentity Pauli
adjacent unitary Ut, leaving only the depolarizing channels            operators to identity Pauli operators (but not vice versa) in
D as the noise channels. We then analyze each setting in               the Heisenberg picture. This requires us to take Pauli paths
Extension H1 as follows.                                               with sequences of weights ðl0 ; …; lt ; 0; …; 0Þ into con-
   Gate-based noise. For our Algorithm 2 for gate-based                sideration, where l0 þ    þ lt ≤ l and t > 0. As our first
noise, the only properties of the unitaries Ut that we used in         modification, when bounding the error in Algorithm 1,
our proofs were that (i) each gate in U t cannot increase the          these new Pauli paths lead to an increased prefactor of
weight of an operator by more than 1 and (ii) each gate                Pd l                     l
                                                                          t¼0 ð t Þ instead of ðdÞ. To derive this, note that in the first
cannot increase the Frobenius norm of an operator. Since the
                                                                       sum of Eq. (C6) we must now sum from wd ¼ 0 to l −
superoperators Ã do not increase the operator weight, we             d þ 1 instead of wd ¼ 1 to l − d þ 1. If wd > 0, the entire
are clearly allowed to absorb them into the Ut with respect to
                                                                       bound proceeds as is and contains ðldÞ individual trunca-
condition (i). In regards to condition (ii), by viewing our
previous proof, one sees that the mean-square error over the           tions. If wd ¼ 0, then we are left with a bound resembling
input state ensemble depends on only the Frobenius norms               our original quantity of interest, but now with d layers
of the truncated operators. Therefore, when taking the mean-           instead of d þ 1. One can then apply the same argument to
square error over the random nonunital noise in addition, the          wd−1 and so on. For instance, the Pauli paths with wd ¼ 0
error will depend only on the mean-square Frobenius norm               and wd−1 > 0 can be grouped into ðldÞ − 1 individual
over the random noise channels. We have just shown that the            truncations, and the Pauli paths with wd ¼ wd−1 ¼ 0 and
superoperators Ã do not increase the mean-square                     wd−2 > 0 can be grouped into ðldÞ − 2 individual trunca-
Frobenius norm. Thus, we are free to absorb the super-                 tions, and so on. In the end, this increased prefactor does
operators Ã into the unitaries U t . Our classical algorithm         not change the stated run-time of our algorithm, since
thus succeeds with run-time as in Theorem 2 of the main                when determining the required value of l we used the
text, with γ ¼ − logð1 − γ s =2Þ ≈ γ s =2.                             inequality ðldÞ ≤ ðel=dÞd [Eq. (C8)]. This inequality is in


                                                                 041018-23
SCHUSTER, YIN, GAO, and YAO                                                                      PHYS. REV. X 15, 041018 (2025)

fact somewhat weak, and is also obeyed by the partial sum
                             P                                         The factor of d can be absorbed into the factor ð1=εÞOð1=γÞ,
of binomial coefficients, dt¼0 ðlt Þ ≤ ðel=dÞd .                       giving our stated run-time.                               ▪
    Our second modification consists of a slight increase in
the algorithm run-time due to the need to keep track of                          APPENDIX I: IMPLICATIONS FOR
the new Pauli paths. When O is a sum of polynomially                             QUANTUM ERROR MITIGATION
many m Pauli operators, nonunital noise increases the
number of Pauli paths by at most a factor of d, correspond-               In this appendix, we prove Corollary 1 of the main text.
ing to the extra sum over t ¼ 1; …; d. For more general O,             We note that the corollary captures nearly all error
                                                                       mitigation strategies of interest, including zero-noise
the sumPd over   t (with l fixed) replaces the factor nl=d
                                                                       extrapolation [60,61], probabilistic error cancellation
with t¼1 nl=t ≤ d · nl .                                               [60], and Clifford data regression [85]. One notable
    Finally, we must slightly modify our argument                      exception is virtual distillation protocols [86,87], which
(Lemma C1) for restricting attention to circuits of depth              evade the settings of our work by performing experiments
d < γ −1 logð1=εÞ. To do so, we provide a simple proof that            involving multiple copies of each input state. Another
observables in any circuit with random nonunital noise                 (partial) exception is noise suppression strategies, such as
depend only on the final O½γ −1 logð1=εÞ layers of the                dynamical decoupling [124,125], which serve to decrease
circuit, for most input states. This was proven recently for           the effective noise rate γ (and thus increase the potential
random quantum circuits using other techniques [36].                   classical complexity), by addressing the microscopic,
    Lemma H1 (Extension of Lemma C1 to random non-                     unitary source of the noise. We remark that, in the corollary,
unital noise). Consider any observable O and any circuit C             the root-mean-square error for an error mitigation strategy
with uniform noise, where each noise channel corresponds               is necessarily taken over both the ensemble of input states
to spontaneous emission in a random direction with                     as well as the probabilistic measurement outcomes of the
rate γ s ≤ 4=7. The root-mean-square Frobenius norm                    noisy quantum experiments themselves.
of the nonidentity component of C† fOg is upper bounded                   Proof of Corollary 1. We denote the set of noisy
by e−γðdþ1Þ jjOjjF, where d is the circuit depth and                   quantum circuits as fC0 g and the number of circuits as
γ ¼ log (1=ð1 − γ s =2Þ) ≈ γ s =2.                                     M ¼ jfC0 gj. To prove the corollary, we adapt our classical
    Proof. We decompose each noise channel as                          algorithms to allow sampling from the measurement out-
A ¼ Ã† ◯ D, and apply Eq. (H8) to the proof of
   †
                                                                       comes of O in each of the M noisy circuits C0 . Without loss
Lemma C1.                                                          ▪   of generality, we can assume that the measurements occur
    The lemma implies that we can approximate C† fOg for               in the eigenbasis of O, so that each outcome is some
depths d ≥ d ¼ γ −1 logð1=εÞ by its identity component,               eigenvalue λ. The outcomes are received with probabilities
       
trðOðd Þ Þ=2n · 1, at layer d. This follows because the               pC0 fρg ðλÞ ¼ trðPλ C0 fρgÞ, where Pλ is the projector onto the
nonidentity components have small root-mean-square                     λ eigenspace of O. Thus, to classically reproduce the result
Frobenius norm, and the layers after d map the identity               of the error mitigation strategy, we need to sample once
operator to itself in the Heisenberg picture. From Lemma B1,           from pC0 fρg ðλÞ for each C0 . We will show that this can be
this approximation suffices to compute
                                     pﬃﬃ expectation values to         done with minimal overhead for Pauli observables, since
within root-mean-square error ε · c · jjOjjF over any low-             each λ takes only two possible eigenvalues 1.
average ensemble of input states with purity c.                           To sample from each individual pC0 fρg ðλÞ, we first
    Random quantum circuits with uniform noise. Finally,               classically compute the expectation value trðOC0 fρgÞ to
we demonstrate the improved run-time of our Algorithm 1                within error ε0. Denote our classical approximation
when applied to random quantum circuits. Compared to the               as aC0 . From this, we approximate the true outcome
general quantum circuits that we consider, the main                    distribution pC0 fρg ð1Þ via qC0 fρg ð1Þ ¼ ð1  aC0 Þ=2.
simplification that occurs for random quantum circuits is              The
                                                                       P        approximation has total variational distance
                                                                                                                  0
that our error bound for Algorithm                1 improves to
                                        qﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ                   jp C0 fρg ð1Þ − qC0 fρg ð1Þj ≤ ε . We can sample from
  −γðlþ1Þ                       −γðlþ1Þ
                                         Pd l                          qC0 fρg ð1Þ efficiently since it takes only two values.
e         jjOjjF instead of e                 t¼0 ð t ÞjjOjjF . This
                                                                          We now analyze how the individual sampling errors
follows because different Pauli paths, on average, do not
                                                                       propagate when we sample from all M noisy circuits fC0 g
coherently interfere in random quantum circuits (we refer to
                                                                       in succession. The ideal outcome distribution is the tensor
Ref. [31] for a comprehensive discussion). This improved
error bound allows us to choose a much smaller threshold               product pðrÞ ¼⊗M      m¼1 pC0r fρg ðri Þ. Here, r ¼ ðr1 ; …; rM Þ for

l ¼ γ −1 logð1=εÞ. This gives a total number of low-weight             rm ∈ f−1; 1g is the sequence of measurement outcomes,
Pauli paths:                                                           and pðrÞ is the probability for a set of M experiments to
                                                                       receive the sequence. Our approximation is the tensor
minðd·nl ;d·mÞ·2OðlÞ ¼ d·minðnð1=γÞlogð1=εÞ ;mÞ·ð1=εÞOð1=γÞ :          product qðrÞ ¼⊗M      m¼1 qC0r fρg ðri Þ. We will bound the total
                                                                       variational distance between pðrÞ andP        qðrÞ. Denote the total
                                                              ðH9Þ     variational distance as TVDðp; qÞ ¼ r jpðrÞ − qðrÞj. We


                                                                041018-24
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                          PHYS. REV. X 15, 041018 (2025)

use the fact that the total variational distance is at most          To conclude our proof, we note that any error mitigation
additive under the tensor product:                                strategy must assign some estimate aðrÞ of trðOCfρgÞ,
                                                                  for every possible sequence r of measurement outcomes.
TVDðp1 ⊗ p2 ; q1 ⊗ q2 Þ ≤ TVDðp1 ; q1 Þ þ TVDðp2 ; q2 Þ:          Without loss of generality, we can assume that jaðrÞj ≤ 1,
                                                                  since jjOjj∞ ¼ 1 for any Pauli operator. Now, we can utilize
                                                          ðI1Þ    the same assignment aðrÞ for our classical algorithm.
                                                                  To bound the mean-square error in our classical estimate,
Applied M times, this gives TVDðp; qÞ ≤ Mε0 .                     we use

X                          X                          X
 qðrÞ(OðrÞ − trðOCfρgÞ)2 ¼  pðrÞ(OðrÞ − trðOCfρgÞ)2 þ  (pðrÞ − qðrÞ) ·(OðrÞ− trðOCfρgÞ)2
 r                                 r                               r
                                 X                                    X
                               ≤  pðrÞ(OðrÞ −trðOCfρgÞ)2 þ4TVDðp;qÞ ≤  pðrÞ(OðrÞ −trðOCfρgÞ)2 þ4Mε0 :                     ðI2Þ
                                   r                                                r



The first term is the root-mean-square error in the error         compute expectation values within root-mean-square error
mitigation strategy. Thus, if error mitigation can compute        4ε in time as stated in Theorem 2. Imposing the lower
the observable to error ε=2, our classical algorithm can do       bound χðnÞ on the run-time of the classical algorithm,
so to root-mean-square error ε by taking ε0 ¼ ε=8M. By            setting d; ε−1 ¼ polyðnÞ, and solving for the noise rate γ
assumption, ε−1 and M are both polynomial in n. Hence,            gives our desired result.                                ▪
ε0−1 is also polynomial in n. Thus, by Theorem 1, the
computation of trðOC0 fρgÞ above can be done in poly-
nomial time, and so the ideal expectation value can also be       APPENDIX K: NOISY QUANTUM CIRCUITS ON
computed in polynomial time.                              ▪           ANY HIGHLY MIXED INPUT STATE
                                                                     As mentioned in the main text, our results in Theorems 1
     APPENDIX J: TEST FOR THE HARDNESS OF                         and 2 immediately extend to circuits on any highly mixed
          A GIVEN QUANTUM CIRCUIT                                 input state. This follows because the ensemble composed of
    Let us now turn to Corollary 2. In general, classical         a single state ρ is low average whenever jjρjj∞ ¼ c=2n with
simulation of noiseless quantum circuits will require             c ¼ Oð1Þ. In fact, we can prove a slightly stronger state-
exponential resources. However, this is not guaranteed            ment, in which this condition on the spectral norm is
for every such circuit. Motivated by modern quantum               replaced by a condition on the Renyi-2 entropy,
experiments, in the main text we proposed Corollary 2             Sð2Þ ðρÞ ¼ log2 ð1=jjρjj22 Þ.
as a simple test for whether a given quantum circuit has the         Corollary K1 (Classical algorithms for noisy quantum
potential to achieve a quantum advantage.                         circuits on highly mixed states). Consider a noisy circuit C
    Proof of Corollary 2. We denote the noiseless quantum         and a state ρ with Renyi-2 entropy Sð2Þ ðρÞ ¼ n − log2 ðcÞ.
circuit as C, and the same circuit with noise as Cγ for a noise   Assume the Pauli coefficients of ρ can be efficiently
rate γ. Let OðdÞ ¼ C† fOg denote the Heisenberg time-             computed. There exists a classical algorithm
                                                          ðdÞ
                                                                                                               pﬃﬃ to compute
evolved observable under the noiseless circuit, Oγ ¼              the state Cfρg to within trace norm error ε · c in time as in
C†γ fOg under the noisy circuit, and ÕðdÞ be the approxi-        Theorems 1 and 2.
mation obtained by applying our classical algorithm to Cγ .          Proof of Corollary K1. The corollary follows by apply-
For each input state ρ, we have                                   ing our Algorithms 1 and 2 to the density matrix ρ instead
                                                                  of an observable. This produces a classical approximation ρ̃
                                               ðdÞ                of the density matrix. The approximation has unit trace but
jtrðρOðdÞ Þ − trðρÕðdÞ Þj ≤ jtrðρOðdÞ Þ − trðρOγ Þj
                                                                  is not guaranteed to be positive. We quantify the error,
                                       ðdÞ                        δρ ¼ ρ̃ − Cfρg, in the approximation via the trace norm
                           þ jtrðρOγ Þ − trðρÕðdÞ Þj:    ðJ1Þ
                                                                  jjδρjj1 . We have
Suppose that the noisy quantum experiment succeeds in
estimating the noiseless expectation value to within root-                    pﬃﬃﬃﬃ              pﬃﬃﬃﬃ             pﬃﬃ
                                                                  jjδρjj1 ≤    2n · jjδρjj2 ≤ ε · 2n · jjρjj2 ¼ ε · c;   ðK1Þ
mean-square error ε, for some noise rate γ. This implies that
the root mean square of the first term on the rhs is less than
ε. Meanwhile, the root mean square of the second term on          where the second inequality follows from the proofs of
the rhs is less than ε if we take l as in Theorem 2 of the        Theorems 1 and 2, and the final inequality uses the
main text. Thus, the classical algorithm in Theorem 2 can         definition of the Renyi-2 entropy.                   ▪


                                                           041018-25
SCHUSTER, YIN, GAO, and YAO                                                                     PHYS. REV. X 15, 041018 (2025)

   APPENDIX L: NOISY QUANTUM CIRCUITS                                  Definition L1 (Spatial disorder in quantum circuit
         WITH SPATIAL DISORDER                                      ensembles). We say that an ensemble of quantum circuits
                                                                    E C ¼ fCg has spatial disorder if the ensemble is invariant
   We can also exchange the ensemble of input states in
                                                                    under conjugation by any single-qubit Pauli operator P:
Theorems 1 and 2 with an ensemble of quantum circuits
applied to any fixed input state. Intuitively, this follows by
                                                                                                fCP g ¼ fCg:                 ðL2Þ
absorbing the preparation of the input state ensemble into
the circuit itself. We illustrate this with a simple example.       As a weaker condition, we say that an ensemble E C has
Consider estimating the expectation value of a Pauli                spatial disorder on a quantum state ρ if the same condition
operator Q over the ensemble of computational basis states.         holds forP a subset E P of Pauli operators such that
We can write each state jsi as a Pauli operator applied to the
                                                                    ð1=jE P jÞ P PρP† ¼ 1=2n .
zero state, jsi ¼ Xs j0n i, with Xs ¼⊗ni¼0 Xsi i . The expect-         Our definition encompasses numerous circuits of interest
ation values are                                                    for the quantum simulation of disordered spin models,
                                                                    including multiple recent experiments [73,126–130]. For
trðCfjsihsjgQÞ ¼ trðCfX s j0n ih0n jX†s g· QÞ                       example, a circuit composed of unitaries of the form
                ¼ trðCXs fj0n ih0n jg· X†s QXs Þ                                  X               X                   
                                                                        Ut ¼ exp i gi Xi · exp i              J ij Zi Zj   ðL3Þ
                ¼ ð−1Þa½Xs ;Q ·trðCXs fj0n ih0n jg· QÞ;   ðL1Þ                        i                  ði;jÞ ∈ U t


where a½Xs ; Q is 0 if Xs and Q commute and 1 if they              has spatial disorder if gi ; J ij are drawn at random from any
anticommute. Here, we define the conjugated circuit                 distributions that are symmetric about zero. We can also
CP fð·Þg ¼ P† CfPð·ÞP† gP, which replaces each unitary              allow, for instance, the gi to be nonrandom if the input state
in the original circuit with its conjugation by P,                  is diagonal in the y or z basis, or the Jij to be nonrandom for
Ut → P† Ut P. We note that multiplying by an overall phase          the x or y basis.
does not change the estimation error. Thus, since our                  Leveraging our Theorems 1 and 2, we show that noisy
classical algorithm can estimate expectation values for             quantum circuits with spatial disorder can be efficiently
the fixed circuit C applied to the ensemble of computational        classically simulated.
basis states, it can also estimate expectation values for the          Corollary L1 (Classical algorithm for noisy quantum
ensemble of circuits fCXs g applied to the fixed input              circuits with spatial disorder). Consider a state ρ, an
state j0n ih0n j.                                                   observable O, and an ensemble E C ¼ fCg of noisy quantum
   Wegeneralizethisexampleintwoways.First,wecanextend               circuits with spatial disorder on ρ. Assume the Pauli
beyond Pauli observables by decomposing             an arbitrary    coefficients of ρ and O can be efficiently computed.
                                         P
observable in the Pauli basis, O ¼ Q cQ Q. Since each               There exists a classical algorithm to compute the expect-
Pauli can be estimated within error ε, the operator O can be        ation values trðCfρgOÞ to within root-mean-square error
estimated within error ε · jjOjjPauli;1, where jjOjjPauli;1 ¼       ε · jjOjjPauli;1 in time as in Theorems 1 and 2 of the
P                                                                   main text.
   Q jcQ j is the Pauli 1-norm. For most observables of interest,
the Pauli 1-norm is upper bounded by the Frobenius                     Proof of Corollary L1. We use the same classical
                                                      pﬃﬃﬃﬃ and     algorithms as in Theorems 1 and 2. The truncations in
spectral norms. In particular, we have jjOjjPauli;1 ≤ mjjOjjF
                                                                    our classical algorithms respect additivity, so that our
for observables that are sums of m Pauli operators, and
                                                                    approximation for O under circuit C is equal to a sum of
jjOjjPauli;1 ≤ Cðd; kÞjjOjj∞ [72] for k-local observables of
                                pﬃﬃﬃ                                the corresponding approximations for each Pauli operator,
degree d, where Cðd; kÞ ¼ 3 d exp (Θðk log kÞ).
   Second, we can replace the specific circuit ensemble                                      ðdÞ
                                                                                                   X       ðdÞ
                                                                                           ÕC ¼    cQ · Q̃C ;               ðL4Þ
fCXs g with any circuit ensemble that is invariant under                                            Q
conjugation by Xs, i.e., fCXs g ¼ fCg for all s. Since the
single-qubit Pauli-X operators generate the full set of Xs ,        where the coefficients cQ are obtained from the Pauli
this is equivalent to the ensemble being invariant under            decomposition of O before time evolution. If we consider
conjugation by single-qubit Pauli-X operators. Hence, we            instead the conjugated quantum circuit CP for some Pauli
refer to this as spatial disorder in the circuit ensemble. In       operators P, we have
the case that the ensemble is invariant under any single-
                                                                                 ðdÞ
                                                                                           X                       ðdÞ
qubit Pauli operator, we can extend this result to arbitrary                   ÕC;P ¼      ð−1Þa½P;Q · cQ · P† Q̃C P:      ðL5Þ
input states. This follows since fPρP† jP n g is a low-                                     Q
average ensemble with c ¼ 1 for any fixed ρ when P is
drawn from the n-qubit Pauli group P n . We capture both of         Thus, the difference between the exact and approximate
these settings with the following definition.                       operator is


                                                             041018-26
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                                PHYS. REV. X 15, 041018 (2025)

                                        ðdÞ     ðdÞ
                                                       X                      ðdÞ   ðdÞ
                                     OC;P − ÕC;P ¼     ð−1Þa½P;Q · cQ · P† QC − Q̃C P:                                             ðL6Þ
                                                        Q


   By assumption, the ensemble E C is invariant under conjugation by any Pauli operator, since this follows from it being
invariant under local Pauli conjugations. Thus, we can replace the average over E C with an identical average over the
ensemble E CP ≡ fCP jC ∈ E C ; P ∈ P n g, where P n is the set of all n-qubit Pauli operators. The mean-square error over E CP is

     1 X                 ðdÞ     ðdÞ   2      1 X X                                   ðdÞ    ðdÞ    2
                tr ρ · ðOC;P − ÕC;P Þ ≤ n                      jcQ j · jtr PρP† · ðQC − Q̃C Þ j
   4 jE C j C;P
    n
                                           4 jE C j C;P       Q

                                              1       X
                                         ≤ n                jc jjc 0 jjtrðPρP† · δQC ÞjjtrðPρP† · δQ0C Þj
                                           4 jE C j C;P;Q;Q0 Q Q
                                                                    X                        1=2  X                      1=2
                                            1 X                     1               †       2       1             †    0  2
                                         ≤              jc jjc 0 j            trðPρP · δQC Þ                trðPρP · δQC Þ       ;   ðL7Þ
                                           jE C j C;Q;Q0 Q Q 4n             P                       4n    P


                                                                                                 ðdÞ      ðdÞ
where the last line uses the Cauchy-Schwarz inequality, and we abbreviate δQC ¼ QC − Q̃C . Now, note that the terms
within parentheses correspond to mean-square error of Q and Q0 under the state ensemble E ¼ fPρP† jP ∈ P n g. By
assumption, this is a zero-average ensemble. Thus, by the results of Theorems 1 and 2, the term is upper bounded ε2 . We
have
                                                                                          X       2
             1 X                 ðdÞ      ðdÞ   2    1 X X                 0      2     2
                        tr ρ · ðOC;P − Õ C;P Þ   ≤                jcQ jjc   j · ε  ¼ ε      jcQ j    ¼ ε2 · jjOjj2Pauli;1 ; ðL8Þ
          4n jE C j C;P                             jE C j C Q; Q0
                                                                           Q
                                                                                           Q


as desired.                                                                                                                            ▪




  [1] R. P. Feynman, Simulating physics with computers, in               [8] J. Kempe, O. Regev, F. Unger, and R. De Wolf, Upper
      Feynman and Computation (CRC Press, 2018),                             bounds on the noise threshold for fault-tolerant quantum
      pp. 133–153.                                                           computing, in Proceedings of the International
  [2] P. W. Shor, Algorithms for quantum computation: Discrete               Colloquium on Automata, Languages, and Programming
      logarithms and factoring, in Proceedings 35th Annual                   (Springer, New York, 2008), pp. 845–856.
      Symposium on Foundations of Computer Science (IEEE,                [9] P. W. Shor, Fault-tolerant quantum computation, in
      1994) pp. 124–134.                                                     Proceedings of 37th Conference on Foundations of Com-
  [3] B. Bauer, S. Bravyi, M. Motta, and G. K.-L. Chan,                      puter Science (IEEE, 1996), pp. 56–65.
      Quantum algorithms for quantum chemistry and quantum              [10] D. Aharonov and M. Ben-Or, Fault-tolerant quantum
      materials science, Chem. Rev. 120, 12685 (2020).                       computation with constant error, in Proceedings of the
  [4] A. M. Dalzell, S. McArdle, M. Berta, P. Bienias, C.-F.                 Twenty-Ninth Annual ACM Symposium on Theory of
      Chen, A. Gilyén, C. T. Hann, M. J. Kastoryano, E. T.                  Computing (1997), pp. 176–188.
      Khabiboulline, A. Kubica et al., Quantum algorithms: A            [11] A. Y. Kitaev, Quantum computations: Algorithms and
      survey of applications and end-to-end complexities, in                 error correction, Russ. Math. Surv. 52, 1191 (1997).
      Quantum Algorithms (Cambridge University Press, Cam-              [12] E. Knill, R. Laflamme, and W. H. Zurek, Resilient quan-
      bridge, England, 2025).                                                tum computation, Science 279, 342 (1998).
  [5] D. Aharonov and M. Ben-Or, Polynomial simulations of              [13] D. Aharonov, M. Ben-Or, R. Impagliazzo, and N. Nisan,
      decohered quantum computers, in Proceedings of 37th                    Limitations of noisy reversible computation, arXiv:quant-
      Conference on Foundations of Computer Science (IEEE,                   ph/9611028.
      1996), pp. 46–55.                                                 [14] M. Ben-Or, D. Gottesman, and A. Hassidim, Quantum
  [6] D. Aharonov, Quantum to classical phase transition in                  refrigerator, arXiv:1301.1995.
      noisy quantum computers, Phys. Rev. A 62, 062311                  [15] A. M. Dalzell, N. Hunter-Jones, and F. G. Brandão, Ran-
      (2000).                                                                dom quantum circuits transform local noise into global
  [7] A. W. Harrow and M. A. Nielsen, Robustness of quantum                  white noise, arXiv:2111.14907.
      gates in the presence of noise, Phys. Rev. A 68, 012308           [16] A. Deshpande, P. Niroula, O. Shtanko, A. V. Gorshkov, B.
      (2003).                                                                Fefferman, and M. J. Gullans, Tight bounds on the




                                                              041018-27
SCHUSTER, YIN, GAO, and YAO                                                                PHYS. REV. X 15, 041018 (2025)

     convergence of noisy random circuits to the uniform            [34] Y. Shao, F. Wei, S. Cheng, and Z. Liu, Simulating quantum
     distribution, PRX Quantum 3, 040329 (2022).                         mean values in noisy variational quantum algorithms: A
[17] S. Chen, J. Cotler, H.-Y. Huang, and J. Li, The complexity          polynomial-scale approach, Phys. Rev. Lett. 133, 120603
     of NISQ, arXiv:2210.07234.                                          (2024).
[18] C. Huang, F. Zhang, M. Newman, J. Cai, X. Gao, Z. Tian,        [35] A. Bouland, B. Fefferman, Z. Landau, and Y. Liu, Noise
     J. Wu, H. Xu, H. Yu, B. Yuan et al., Classical simulation of        and the frontier of quantum supremacy, in Proceedings of
     quantum supremacy circuits, arXiv:2005.06787.                       the 2021 IEEE 62nd Annual Symposium on Foundations of
[19] Y. Liu, X. Liu, F. Li, H. Fu, Y. Yang, J. Song, P. Zhao, Z.         Computer Science (FOCS) (IEEE, 2022), pp. 1308–1317.
     Wang, D. Peng, H. Chen et al., Closing the “quantum            [36] A. A. Mele, A. Angrisani, S. Ghosh, S. Khatri, J. Eisert,
     supremacy” gap: Achieving real-time simulation of a                 D. S. França, and Y. Quek, Noise-induced shallow circuits
     random quantum circuit using a new sunway supercom-                 and absence of barren plateaus, arXiv:2403.13927.
     puter, in Proceedings of the International Conference for      [37] R. Movassagh and J. Schenker, Theory of ergodic quantum
     High Performance Computing, Networking, Storage and                 processes, Phys. Rev. X 11, 041001 (2021).
     Analysis (2021), pp. 1–12.                                     [38] K. Fujii, Noise threshold of quantum supremacy,
[20] F. Pan and P. Zhang, Simulating the Sycamore quantum                arXiv:1610.03632.
     supremacy circuits, arXiv:2103.03074.                          [39] G. Kalai and G. Kindler, Gaussian noise sensitivity and
[21] B. Villalonga, D. Lyakh, S. Boixo, H. Neven, T. S.                  bosonsampling, arXiv:1409.3093.
     Humble, R. Biswas, E. G. Rieffel, A. Ho, and S.                [40] R. García-Patrón, J. J. Renema, and V. Shchesnovich,
     Mandrà, Establishing the quantum supremacy frontier                Simulating boson sampling in lossy architectures, Quan-
     with a 281 Pflop/s simulation, Quantum Sci. Technol. 5,             tum 3, 169 (2019).
     034003 (2020).                                                 [41] H. Qi, D. J. Brod, N. Quesada, and R. García-Patrón,
[22] S. Cheng, C. Cao, C. Zhang, Y. Liu, S.-Y. Hou, P. Xu, and B.        Regimes of classical simulability for noisy Gaussian boson
     Zeng, Simulating noisy quantum circuits with matrix prod-           sampling, Phys. Rev. Lett. 124, 100502 (2020).
     uct density operators, Phys. Rev. Res. 3, 023005 (2021).       [42] C. Oh, L. Jiang, and B. Fefferman, On classical simulation
[23] K. Noh, L. Jiang, and B. Fefferman, Efficient classical             algorithms for noisy boson sampling, arXiv:2301.11532.
     simulation of noisy random quantum circuits in one             [43] C. Oh, M. Liu, Y. Alexeev, B. Fefferman, and L. Jiang,
     dimension, Quantum 4, 318 (2020).                                   Tensor network algorithm for simulating experimental
[24] Z. Chen, Y. Bao, and S. Choi, Optimized trajectory                  Gaussian boson sampling, Nat. Phys. 20, 1461 (2024).
     unraveling for classical simulation of noisy quantum           [44] D. Hangleiter and M. J. Gullans, Bell sampling from
     dynamics, Phys. Rev. Lett. 133, 230403 (2024).                      quantum circuits, Phys. Rev. Lett. 133, 020601 (2024).
[25] Z. Cheng and M. Ippoliti, Efficient sampling of noisy          [45] A. Tanggara, M. Gu, and K. Bharti, Classically spoofing
     shallow circuits via monitored unraveling, PRX Quantum              system linear cross entropy score benchmarking,
     4, 040326 (2023).                                                   arXiv:2405.00789.
[26] M. J. Bremner, A. Montanaro, and D. J. Shepherd, Achiev-       [46] I. Ermakov, O. Lychkovskiy, and T. Byrnes, Unified
     ing quantum supremacy with sparse and noisy commuting               framework for efficiently computable quantum circuits,
     quantum computations, Quantum 1, 8 (2017).                          arXiv:2401.08187.
[27] J. Rajakumar, J. D. Watson, and Y.-K. Liu, Polynomial-         [47] I. Kuprov, N. Wagner-Rundell, and P. Hore, Polynomially
     time classical simulation of noisy IQP circuits with                scaling spin dynamics simulation algorithm based on
     constant depth, in Proceedings of the 2025 Annual                   adaptive state-space restriction, J. Magn. Reson. 189,
     ACM-SIAM Symposium on Discrete Algorithms (SODA),                   241 (2007).
     arXiv:2403.14607.                                              [48] A. Karabanov, I. Kuprov, G. Charnock, A. van der Drift,
[28] X. Gao and L. Duan, Efficient classical simulation of noisy         L. J. Edwards, and W. Köckenberger, On the accuracy of
     quantum computation, arXiv:1810.03176.                              the state space restriction approximation for spin dynam-
[29] B. Barak, C.-N. Chou, and X. Gao, Spoofing linear cross-            ics simulations, J. Chem. Phys. 135 (2011).
     entropy benchmarking in shallow quantum circuits,              [49] T. Rakovszky, C. W. von Keyserlingk, and F. Pollmann,
     arXiv:2005.02421.                                                   Dissipation-assisted operator evolution method for cap-
[30] X. Gao, M. Kalinowski, C.-N. Chou, M. D. Lukin, B.                  turing hydrodynamic transport, Phys. Rev. B 105, 075131
     Barak, and S. Choi, Limitations of linear cross-entropy as          (2022).
     a measure for quantum advantage, PRX Quantum 5,                [50] Y. Yoo, C. D. White, and B. Swingle, Open-system spin
     010334 (2021).                                                      transport and operator weight dissipation in spin chains,
[31] D. Aharonov, X. Gao, Z. Landau, Y. Liu, and U. Vazirani,            Phys. Rev. B 107, 115118 (2023).
     A polynomial-time classical algorithm for noisy random         [51] T. Vovk and H. Pichler, Entanglement-optimal trajectories
     circuit sampling, in Proceedings of the 55th Annual ACM             of many-body quantum Markov processes, Phys. Rev. Lett.
     Symposium on Theory of Computing (2023), pp. 945–957.               128, 243601 (2022).
[32] M.-H. Yung and X. Gao, Can chaotic quantum circuits            [52] A. M. Dalzell, N. Hunter-Jones, and F. G. Brandão, Ran-
     maintain      quantum      supremacy      under     noise?,         dom quantum circuits transform local noise into global
     arXiv:1706.08913.                                                   white noise, Commun. Math. Phys. 405, 78 (2024).
[33] E. Fontana, M. S. Rudolph, R. Duncan, I. Rungger, and C.       [53] L. Paletta, A. Leverrier, A. Sarlette, M. Mirrahimi, and C.
     Cîrstoiu, Classical simulations of noisy variational quan-          Vuillot, Robust sparse IQP sampling in constant depth,
     tum circuits, arXiv:2306.05400.                                     Quantum 8, 1337 (2024).



                                                             041018-28
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                            PHYS. REV. X 15, 041018 (2025)

[54] C. D. White, M. Zaletel, R. S. K. Mong, and G. Refael,          [70] See Ref. [31], where this is referred to as “orthogonality.”
     Quantum dynamics of thermalizing systems, Phys. Rev. B               This requirement is satisfied in random circuits, where
     97, 035127 (2018).                                                   averaged properties of operator time evolution are gov-
[55] B. Ye, F. Machado, C. D. White, R. S. K. Mong, and N. Y.             erned by an incoherent classical Markov process, but not
     Yao, Emergent hydrodynamics in nonequilibrium quantum                more generally.
     systems, Phys. Rev. Lett. 125, 030601 (2020).                   [71] M. C. Caro, H.-Y. Huang, N. Ezzell, J. Gibbs, A. T.
[56] C. Von Keyserlingk, F. Pollmann, and T. Rakovszky,                   Sornborger, L. Cincio, P. J. Coles, and Z. Holmes, Out-
     Operator backflow and the classical simulation of quan-              of-distribution generalization for learning quantum dy-
     tum transport, Phys. Rev. B 105, 245101(R) (2022).                   namics, Nat. Commun. 14, 3751 (2023).
[57] C. D. White, Effective dissipation rate in a Liouvillian-       [72] H.-Y. Huang, S. Chen, and J. Preskill, Learning to predict
     graph picture of high-temperature quantum hydrodynam-                arbitrary quantum processes, arXiv:2210.14894.
     ics, Phys. Rev. B 107, 094311 (2023).                           [73] X. Mi, M. Ippoliti, C. Quintana, A. Greene, Z. Chen, J.
[58] T. Klein Kvorning, L. Herviou, and J. H. Bardarson, Time-            Gross, F. Arute, K. Arya, J. Atalaya, R. Babbush et al.,
     evolution of local information: Thermalization dynamics              Time-crystalline eigenstate order on a quantum processor,
     of local observables, SciPost Phys. 13, 080 (2022).                  Nature (London) 601, 531 (2022).
[59] C. Artiaco, C. Fleckenstein, D. Aceituno Chávez, T. K.          [74] M. Dupont and J. E. Moore, Universal spin dynamics in
     Kvorning, and J. H. Bardarson, Efficient large-scale many-           infinite-temperature one-dimensional quantum magnets,
     body quantum dynamics via local-information time evo-                Phys. Rev. B 101, 121106 (2020).
     lution, PRX Quantum 5, 020352 (2024).                           [75] E. Rosenberg, T. Andersen, R. Samajdar, A. Petukhov, J.
[60] K. Temme, S. Bravyi, and J. M. Gambetta, Error miti-                 Hoke, D. Abanin, A. Bengtsson, I. Drozdov, C. Erickson,
     gation for short-depth quantum circuits, Phys. Rev. Lett.            P. Klimov et al., Dynamics of magnetization at infinite
     119, 180509 (2017).                                                  temperature in a Heisenberg spin chain, Science 384, 48
[61] Y. Li and S. C. Benjamin, Efficient variational quantum              (2024).
     simulator incorporating active error minimization, Phys.        [76] At this halting step, we also group together all weights
     Rev. X 7, 021050 (2017).                                             above the threshold in order to achieve a tighter bound on
[62] Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J.                   the error. See Appendix C for full details.
     Huggins, Y. Li, J. R. McClean, and T. E. O’Brien, Quan-         [77] We note that the maximum nontrivial depth for quantum
     tum error mitigation, Rev. Mod. Phys. 95, 045005 (2023).             circuits with random input states, d ¼ O(γ −1 logð1=εÞ), is
[63] Y. Quek, D. S. França, S. Khatri, J. J. Meyer, and J. Eisert,        slightly shorter than the maximum depth for quantum
     Exponentially tighter bounds on limitations of quantum               circuits with a fixed input state, d ¼ O(γ −1 logðn=εÞ) [13].
     error mitigation, Nat. Phys. 20, 1648 (2024).                        See Appendix C for further details.
[64] R. Takagi, S. Endo, S. Minagawa, and M. Gu, Funda-              [78] D. A. Roberts, D. Stanford, and A. Streicher, Operator
     mental limits of quantum error mitigation, npj Quantum               growth in the SKY model, J. High Energy Phys. 01
     Inf. 8, 114 (2022).                                                  (2018) 122.
[65] R. Takagi, H. Tajima, and M. Gu, Universal sampling             [79] A. R. Brown, H. Gharibyan, S. Leichenauer, H. W. Lin, S.
     lower bounds for quantum error mitigation, Phys. Rev.                Nezami, G. Salton, L. Susskind, B. Swingle, and M.
     Lett. 131, 210602 (2023).                                            Walter, Quantum gravity in the lab. I. Teleportation by
[66] K. Tsubouchi, T. Sagawa, and N. Yoshioka, Universal cost             size and traversable wormholes, PRX Quantum 4, 010320
     bound of quantum error mitigation based on quantum                   (2023).
     estimation theory, Phys. Rev. Lett. 131, 210601 (2023).         [80] T. Schuster, B. Kobrin, P. Gao, I. Cong, E. T.
[67] B. Fefferman, S. Ghosh, M. Gullans, K. Kuroiwa, and K.               Khabiboulline, N. M. Linke, M. D. Lukin, C. Monroe,
     Sharma, Effect of non-unital noise on random circuit                 B. Yoshida, and N. Y. Yao, Many-body quantum telepor-
     sampling, arXiv:2306.16659.                                          tation via operator spreading in the traversable wormhole
[68] As a consequence, our algorithms for uniform noise can be            protocol, Phys. Rev. X 12, 031013 (2022).
     thought of as working explicitly in the regime                  [81] T. Schuster and N. Y. Yao, Operator growth in open
     d ¼ O(γ −1 logðn=εÞ). After this depth, one can approxi-             quantum systems, Phys. Rev. Lett. 131, 160402 (2023).
     mate any expectation value with its value in the maximally      [82] X. Bonet-Monroig, R. Sagastizabal, M. Singh, and T. E.
     mixed state [13].                                                    O’Brien, Low-cost error mitigation by symmetry verifica-
[69] In particular, threshold theorems typically assume two               tion, Phys. Rev. A 98, 062339 (2018).
     ingredients [9–12]: midcircuit measurement and feedfor-         [83] S. McArdle, X. Yuan, and S. Benjamin, Error-mitigated
     ward operations, and the ability to insert “fresh qubits”            digital quantum simulation, Phys. Rev. Lett. 122, 180501
     unaffected by idle errors. In effect, both noise models allow        (2019).
     midcircuit measurement and feedforward operations, since        [84] N. C. Rubin, R. Babbush, and J. McClean, Application of
     one can implement the feedforward operations via con-                fermionic marginal constraints to hybrid quantum algo-
     trolled quantum gates. (For a fixed input state, this can be         rithms, New J. Phys. 20, 053020 (2018).
     made fault tolerant by encoding the state of the “measured”     [85] P. Czarnik, A. Arrasmith, P. J. Coles, and L. Cincio, Error
     qubit in a classical error correcting code at the layer at           mitigation with Clifford quantum-circuit data, Quantum 5,
     which it is “measured.”) Crucially however, the gate-based           592 (2021).
     noise model allows the insertion of fresh qubits, while the     [86] W. J. Huggins, S. McArdle, T. E. O’Brien, J. Lee, N. C.
     uniform noise model does not.                                        Rubin, S. Boixo, K. B. Whaley, R. Babbush, and J. R.



                                                              041018-29
SCHUSTER, YIN, GAO, and YAO                                                                   PHYS. REV. X 15, 041018 (2025)

      McClean, Virtual distillation for quantum error mitiga-        [105] S. Boixo, S. V. Isakov, V. N. Smelyanskiy, R. Babbush, N.
      tion, Phys. Rev. X 11, 041036 (2021).                                Ding, Z. Jiang, M. J. Bremner, J. M. Martinis, and H.
 [87] T. E. O’Brien, S. Polla, N. C. Rubin, W. J. Huggins, S.              Neven, Characterizing quantum supremacy in near-term
      McArdle, S. Boixo, J. R. McClean, and R. Babbush, Error              devices, Nat. Phys. 14, 595 (2018).
      mitigation via verified phase estimation, PRX Quantum 2,       [106] A. Morvan, B. Villalonga, X. Mi, S. Mandra, A.
      020317 (2021).                                                       Bengtsson, P. Klimov, Z. Chen, S. Hong, C. Erickson,
 [88] Y. Kim, C. J. Wood, T. J. Yoder, S. T. Merkel, J. M.                 I. Drozdov et al., Phase transition in random circuit
      Gambetta, K. Temme, and A. Kandala, Scalable error                   sampling, Nature (London) 634, 328 (2024).
      mitigation for noisy quantum circuits produces competitive     [107] J. Tindall, M. Fishman, M. Stoudenmire, and D. Sels,
      expectation values, Nat. Phys. 19, 752 (2023).                       Efficient tensor network simulation of IBM’s kicked Ising
 [89] Y. Kim, A. Eddins, S. Anand, K. X. Wei, E. Van Den Berg,             experiment, PRX Quantum 5, 010308 (2024).
      S. Rosenblatt, H. Nayfeh, Y. Wu, M. Zaletel, K. Temme          [108] T. Begušić, J. Gray, and G. K. Chan, Fast and converged
      et al., Evidence for the utility of quantum computing before         classical simulations of evidence for the utility of quantum
      fault tolerance, Nature (London) 618, 500 (2023).                    computing before fault tolerance, Sci. Adv. 10, eadk4321
 [90] T. L. Scholten, C. J. Williams, D. Moody, M. Mosca, W.               (2024).
      Hurley, W. J. Zeng, M. Troyer, J. M. Gambetta et al.,          [109] K. Kechedzhi, S. Isakov, S. Mandrà, B. Villalonga, X. Mi,
      Assessing the benefits and risks of quantum computers,               S. Boixo, and V. Smelyanskiy, Effective quantum volume,
      arXiv:2401.16317.                                                    fidelity and computational cost of noisy quantum process-
 [91] J. A. Jones, Quantum computing with NMR, Prog. NMR                   ing experiments, Future Gener. Comput. Syst. 153, 431
      Spectrosc. 59, 91 (2011).                                            (2024).
 [92] M. W. Doherty, N. B. Manson, P. Delaney, F. Jelezko, J.        [110] S. Anand, K. Temme, A. Kandala, and M. Zaletel,
      Wrachtrup, and L. C. Hollenberg, The nitrogen-vacancy                Classical benchmarking of zero noise extrapolation be-
      colour centre in diamond, Phys. Rep. 528, 1 (2013).                  yond the exactly-verifiable regime, arXiv:2306.17839.
 [93] C. Zu, F. Machado, B. Ye, S. Choi, B. Kobrin, T. Mittiga,      [111] M. S. Rudolph, E. Fontana, Z. Holmes, and L. Cincio,
      S. Hsieh, P. Bhattacharyya, M. Markham, D. Twitchen                  Classical surrogate simulation of quantum systems with
      et al., Emergent hydrodynamics in a strongly interacting             LOWESA, arXiv:2308.09109.
      dipolar spin ensemble, Nature (London) 597, 45 (2021).         [112] S. Patra, S. S. Jahromi, S. Singh, and R. Orús, Efficient
 [94] E. Knill and R. Laflamme, Power of one bit of quantum                tensor network simulation of IBM’s largest quantum
      information, Phys. Rev. Lett. 81, 5672 (1998).                       processors, Phys. Rev. Res. 6, 013326 (2024).
 [95] F. Arute, K. Arya, R. Babbush, D. Bacon, J. C. Bardin, R.      [113] A similar but less precise connection was made in
      Barends, R. Biswas, S. Boixo, F. G. Brandão, D. A. Buell             Ref. [109].
      et al., Quantum supremacy using a programmable super-          [114] A. Nahum, S. Roy, S. Vijay, and T. Zhou, Real-time
      conducting processor, Nature (London) 574, 505 (2019).               correlators in chaotic quantum many-body systems, Phys.
 [96] D. Hangleiter, J. Bermejo-Vega, M. Schwarz, and J. Eisert,           Rev. B 106, 224310 (2022).
      Anticoncentration theorems for schemes showing a quan-         [115] T. Yoshimura, S. J. Garratt, and J. Chalker, Operator
      tum speedup, Quantum 2, 65 (2018).                                   dynamics in Floquet many-body systems, Phys. Rev. B
 [97] A. M. Dalzell, N. Hunter-Jones, and F. G. S. L. Brandão,             111, 094316 (2025).
      Random quantum circuits anticoncentrate in log depth,          [116] A. Angrisani, A. Schmidhuber, M. S. Rudolph, M. Cerezo,
      PRX Quantum 3, 010333 (2022).                                        Z. Holmes, and H.-Y. Huang, Classically estimating ob-
 [98] T. Schuster, J. Haferkamp, and H.-Y. Huang, Random                   servables of noiseless quantum circuits, arXiv:2409.01706.
      unitaries in extremely low depth, Science 389, 92 (2025).      [117] A. Goussev, R. A. Jalabert, H. M. Pastawski, and D.
 [99] A. Sauliere, B. Magni, G. Lami, X. Turkeshi, and J. De               Wisniacki, Loschmidt echo, Scholarpedia 7, 11687 (2012).
      Nardis, Universality in the anticoncentration of chaotic       [118] For example, for the entanglement entropy and OTOC, one
      quantum circuits, arXiv:2503.00119.                                  can consider a deep Clifford circuit. This generates high
[100] L. Grevink, J. Haferkamp, M. Heinrich, J. Helsen, M.                 entanglement despite being classically simulable via the
      Hinsche, T. Schuster, and Z. Zimborás, Will it glue? On              Gottesman-Knill theorem. For the magic, one can consider
      short-depth designs beyond the unitary group,                        a 1D circuit with many T gates but low circuit depth, or a
      arXiv:2506.23925.                                                    Gaussian fermionic state. Both have an extensive number
[101] L. Cui, T. Schuster, F. Brandao, and H.-Y. Huang, Unitary            of T gates, while remaining simulable via matrix product
      designs in nearly optimal depth, arXiv:2507.06216.                   state and match gate algorithms, respectively. For the
[102] R. Movassagh, The hardness of random quantum circuits,               operator entanglement entropy (and all aforementioned
      Nat. Phys. 19, 1719 (2023).                                          metrics as well), one can consider a generic highly ergodic
[103] A. Bouland, B. Fefferman, C. Nirkhe, and U. Vazirani, On             many-body system. Time-evolved operators in such sys-
      the complexity and verification of quantum random circuit            tems typically feature a linear growth in operator entan-
      sampling, Nat. Phys. 15, 159 (2019).                                 glement entropy over time, despite the operators’
[104] Y. Wu, W.-S. Bao, S. Cao, F. Chen, M.-C. Chen, X. Chen, T.-          expectation values often being efficiently simulated via
      H. Chung, H. Deng, Y. Du, D. Fan et al., Strong quantum              Pauli truncation methods [46,49–51,54–59].
      computational advantage using a superconducting quan-          [119] S. Bravyi, D. Gosset, and Y. Liu, Classical simulation of
      tum processor, Phys. Rev. Lett. 127, 180501 (2021).                  peaked shallow quantum circuits, arXiv:2309.08405.




                                                              041018-30
A POLYNOMIAL-TIME CLASSICAL ALGORITHM FOR NOISY …                                               PHYS. REV. X 15, 041018 (2025)

[120] S. Bravyi, D. Gosset, and R. Movassagh, Classical                 [126] S. Choi, J. Choi, R. Landig, G. Kucsko, H. Zhou, J. Isoya,
      algorithms for quantum mean values, Nat. Phys. 17,                      F. Jelezko, S. Onoda, H. Sumiya, V. Khemani et al.,
      337 (2021).                                                             Observation of discrete time-crystalline order in a dis-
[121] If the individual coefficients can be computed in time τ                ordered dipolar many-body system, Nature (London) 543,
      instead of time Oð1Þ, then the time to read in all                      221 (2017).
      coefficients will be Oðτ · Dl Þ instead of OðDl Þ. Our final      [127] J. Randall, C. Bradley, F. van der Gronden, A. Galicia, M.
      run-time will be unchanged as long as τ ¼ Oðd · l!Þ, and                Abobeih, M. Markham, D. Twitchen, F. Machado, N. Yao,
      will be quasipolynomial in n as long as τ is quasi-                     and T. Taminiau, Many-body–localized discrete time
      polynomial as well.                                                     crystal with a programmable spin-based quantum simu-
[122] To suppress the effect of read-out noise, one can consider              lator, Science 374, 1474 (2021).
      implementing classical error correction prior to measure-         [128] R. Harris, Y. Sato, A. J. Berkley, M. Reis, F. Altomare, M.
      ment (e.g., via a repetition code on each qubit). In this case,         Amin, K. Boothby, P. Bunyk, C. Deng, C. Enderud et al.,
      the output distribution does not anticoncentrate and so our             Phase transitions in a programmable quantum spin glass
      theorem does not apply.                                                 simulator, Science 361, 162 (2018).
[123] M. Raginsky, Strictly contractive quantum channels and            [129] A. D. King, J. Raymond, T. Lanting, R. Harris, A. Zucca, F.
      physically realizable quantum computers, Phys. Rev. A 65,               Altomare, A. J. Berkley, K. Boothby, S. Ejtemaee, C.
      032306 (2002).                                                          Enderud et al., Quantum critical dynamics in a 5,000-qubit
[124] L. Viola, E. Knill, and S. Lloyd, Dynamical decoupling                  programmable spin glass, Nature (London) 617, 61 (2023).
      of open quantum systems, Phys. Rev. Lett. 82, 2417                [130] A. D. King, A. Nocera, M. M. Rams, J. Dziarmaga, R.
      (1999).                                                                 Wiersema, W. Bernoudy, J. Raymond, N. Kaushal, N.
[125] K. Khodjasteh and D. A. Lidar, Fault-tolerant quantum                   Heinsdorf, R. Harris et al., Computational supremacy in
      dynamical decoupling, Phys. Rev. Lett. 95, 180501 (2005).               quantum simulation, arXiv:2403.00910.




                                                                 041018-31
