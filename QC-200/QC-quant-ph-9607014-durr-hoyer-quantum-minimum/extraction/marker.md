# Marker Extraction (Fallback via pdftotext)

*Note: Marker (VikParuchuri/marker) was not available in this environment. This
extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful text fallback. The full plain-text extraction of the paper follows.*

**Source:** `paper.pdf` — arXiv:quant-ph/9607014v2 (Dürr & Høyer, 1996)

---

                                                        A quantum algorithm for finding the minimum∗
                                                                          Christoph Dürr†                     Peter Høyer‡
                                                                                           July 1996


                                      1     Introduction                                                  We first give the minimum searching algorithm,




arXiv:quant-ph/9607014v2 7 Jan 1999
                                                                                                        then the proof of the probability of success.
                                      Let T [0..N − 1] be an unsorted table of N items, each
                                      holding a value from an ordered set. For simplicity, Quantum Minimum Searching Algorithm
                                      assume that all values are distinct. The minimum
                                      searching problem is to find the index y such that T [y] 1. Choose threshold index 0 ≤ y ≤ N − 1 uniformly
                                      is minimum. This clearly requires a linear number of        at random.
                                      probes on a classical probabilistic Turing machine.
                                                                                               2. Repeat the following and interrupt it when√ the
                                         Here, we give a simple quantum
                                                                    √       algorithm which
                                                                                                  total running time is more than 22.5 N +
                                      solves the problem using O( N ) probes. The main
                                                                                                  1.4 lg2 N .1 Then go to stage 2(2c).
                                      subroutine is the quantum exponential searching al-
                                      gorithm of [2], which itself is a generalization of          (a) Initialize the memory as j √1N |ji|yi.
                                                                                                                                 P
                                      Grover’s recent quantum searching algorithm [3].                  Mark every item j for which T [j] < T [y].
                                      Due to a general lower bound of [1], this is within
                                      a constant factor of the optimum.                            (b) Apply the quantum exponential searching
                                                                                                        algorithm of [2].
                                                                                                              (c) Observe the first register: let y ′ be the out-
                                      2     The algorithm                                                         come. If T [y ′ ] < T [y], then set threshold
                                                                                                                  index y to y ′ .
                                      Our algorithm calls the quantum exponential search-
                                      ing algorithm of [2] as a subroutine to find the index             3. Return y.
                                      of a smaller item than the value determined by a par-
                                      ticular threshold index. The result is then chosen as                By convention, we assume that stage 2(2a) takes
                                      the new threshold. This process is repeated until the             lg(N ) time steps and that one iteration in the expo-
                                      probability that the threshold index selects the min-             nential searching algorithm takes one time step. The
                                      imum is sufficiently large.                                       work performed in the stages 1, 2(2c), and 3 is not
                                         If there are t ≥ 1 marked table entries, the quan-             counted.
                                      tum exponential searching algorithm will return one                  For the analysis of the probability of success, as-
                                      of them with p   equal probability after an expected              sume that there is no time-out, that is, the algorithm
                                      number of O( N/t ) iterations. If no entry is                     runs long enough to find the minimum. We refer to
                                      marked, then it will run forever. We obtain the fol-              this as the infinite algorithm. We start by analyzing
                                      lowing theorem.                                                   the expected time to find the minimum.
                                                                                                           At any moment the infinite algorithm searches the
                                      Theorem 1 The algorithm given below finds the in-                 minimum among the t items which are less than T [y].
                                      dex of the minimum value with probability at least 12 .           During the execution any such element will be chosen
                                                            √
                                      Its running time is O( N ).                                       at some point as the threshold with some probabil-
                                          ∗ This work was supported by the alcom-it Research Pro-
                                                                                                        ity. The following lemma states that this probability
                                      gramme of the EU, the rand2 Esprit Working Group, and the         is the inverse of the rank of the element and is inde-
                                      ISI Foundation.                                                   pendent of the size of the table.
                                          † Laboratoire de Recherche en Informatique, Université

                                      Paris-Sud, bât. 490, F–91405 Orsay, France.         Email:       Lemma 1 Let p(t, r) be the probability that the index
                                      durr@lri.fr.                                                      of the element of rank r will ever be chosen when the
                                          ‡ Dept. of Math. and Comp. Science, Odense Univer-

                                      sity, Campusvej 55, DK–5230 Odense M, Denmark. Email:                1 As notation, we use lg for the binary logarithm and ln for

                                      u2pi@imada.ou.dk.                                                 the natural logarithm.


                                                                                                    1
infinite algorithm searches among t elements. Then        stage 2(2a) before T [y] holds the minimum is at most
p(t, r) = 1/r if r ≤ t, and p(t, r) = 0 otherwise.                  N
                                                                    X
                                                                          p(N, r) lg N =(HN − 1) lg N
Proof. The case r > t is obvious. The case r ≤ t                    r=2

is proven by induction on t for a fixed r: The basis                              ≤ ln N lg N
p(r, r) = 1/r is obvious since the output distribu-                                  7
tion of the exponential searching algorithm is uni-                               ≤ lg2 N,
                                                                                    10
form. Assume that for all k ∈ [r, t] the equation
                                                       where HN denotes the N th harmonic number.
p(k, r) = 1/r holds. Then when t + 1 elements are
                                                         Theorem 1 follows immediately from lemma 2 since
marked, y is chosen uniformly among all t+ 1 indices,
                                                       after at most 2m0 iterations, T [y] holds the minimum
and can hold an item of rank either r, greater than r,
                                                       value with probability at least 12 .
or less than r. Only the former two cases contribute
to the summation:

                         t+1
                                                          3    Final remarks
                    1    X    1
     p(t + 1, r) =     +         p(k − 1, r)            The probability of success can be improved by run-
                   t+1       t+1
                          k=r+1                         ning the algorithm c times. Let y be such that T [y] is
                    1     t+1−r 1                       the  minimum among the outcomes. With probabil-
                =      +            ·
                  t+1       t+1        r                ity at least 1 − 1/2c, T [y] holds the minimum of the
                  1                                     table. Clearly, the probability of success is even bet-
                = .
                  r                                     ter if we run the algorithm only once with time-out
                                                        c2m0 , because then we use the information provided
                                                        by the previous steps.
   The expected number of iterations used by the ex-       If the values in T are not distinct, we use the
ponential searching algorithm of [2] to find the index same algorithm as for the simplified case. The anal-
of a marked item — among
                       p N items where t items are ysis of the general case is unchanged, except that in
marked — is at most 29 N/t (see [2]). We can now lemma 1, the equation p(t, r) = 1/r now becomes an
deduce the expected time used to find the minimum: inequality, p(t, r) ≤ 1/r. Hence, the lower bound for
                                                        the success probability given in theorem 1 for the
                                                        simplified case is also a lower bound for the general
Lemma 2 The expected total time used by the infi- case.
nite algorithm before y holds
                         √ the7 index      of the mini-
                                      2
mum is at most m0 = 45 4   N  + 10 lg   N .
                                                          Acknoledgment
Proof. The expected total number of time steps of We wish to thank Stephane Boucheron for raising this
stage 2(2b) before T [y] holds the minimum is at most problem to us and also Richard Cleve and Miklos
                                                         Santha for helpful discussions.
 N            r
                           √   N −1
X           9     N      9     X      1 1
    p(N, r)           =     N              √
r=2
            2   r − 1    2     r=1
                                    r +  1 r             References
                                      N −1
                                                 !
                         9√      1 X −3/2                [1] C.H. Bennett, E. Bernstein, G. Brassard and
                      ≤     N       +      r
                         2       2    r=2                    U. Vazirani, Strengths and weaknesses of quan-
                                                             tum computing, SIAM Journal on Computing,
                                                       !
                         9√      1       N −1
                                      Z
                      ≤     N       +         r−3/2 dr       Volume 26, Number 5 1510–1523, 1997.
                         2       2      r=1
                                                 N −1 ! [2] M. Boyer, G. Brassard, P. Høyer and A. Tapp,
                         9√
                                      
                                 1          −1/2             Tight bounds on quantum searching, Fortschritte
                      =     N       + −2r
                         2       2                r=1        Der Physik, 1998.
                         45 √
                      ≤       N.                         [3] L.K. Grover, A fast quantum mechanical algo-
                          4                                  rithm for database search, Proc. 28th Ann. ACM
                                                             Symp. on Theory of Comput., 212–219, 1996.
  The expected total number of time steps of

                                                      2
