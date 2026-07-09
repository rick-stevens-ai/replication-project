# Marker Extraction (Fallback via pdftotext)

*Note: Marker (VikParuchuri/marker) was not available in this environment. This
extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful text fallback, matching the convention used by sibling QC-200 dirs.*

**Source:** `paper.pdf` — arXiv:quant-ph/9705041v4 (Terhal & Smolin, 1997; Phys. Rev. A 58, 1822)

---

                                                                           Single quantum querying of a database

                                                                               Barbara M. Terhal(1) and John A. Smolin(2)
                                        (1)
                                              Instituut voor Theoretische Fysica, Universiteit van Amsterdam, Valckenierstraat 65, 1018 XE Amsterdam, and Centrum
                                                                                          voor Wiskunde en Informatica,
                                                                               Kruislaan 413, 1098 SJ Amsterdam, The Netherlands.
                                                                                            Email: terhal@phys.uva.nl
                                                        (2)
                                                            IBM Research Division, T.J. Watson Research Center, Yorktown Heights, New York 10598, USA.
                                                                                         Email: smolin@watson.ibm.com
                                                                                                (November 26, 2024)



                                                                                                          marked item in as few queries to the database as possi-




arXiv:quant-ph/9705041v4 14 Nov 1997
                                           We present a class of fast quantum algorithms, based on        ble. The queries are bit strings x of length n such that
                                       Bernstein and Vazirani’s parity problem, that retrieve the         the database returns the answer
                                       entire contents of a quantum database Y in a single query.
                                       The class includes binary search problems and coin-weighing                                    n
                                                                                                                                              !
                                                                                                                                     X
                                       problems. Our methods far exceed the efficiency of classical               a(x, y) = x · y ≡      xi yi mod 2         (1.1)
                                       algorithms which are bounded by the classical information-                                     i=1
                                       theoretic bound. We show the connection between classi-
                                       cal algorithms based on several compression codes and our          where xi and yi are the ith bits of x and y. A simple
                                       quantum-mechanical method.                                         version of this problem is the case in which the allowed
                                                                                                          queries x have Hamming weight 1. The information re-
                                       PACS: 03.67.-a, 03.67.Lx, 89.70.+c                                 trieved by a single query xj = δij is small–it adds or
                                                                                                          eliminates item i from the set of possible marked items.
                                                                                                          It thus takes n − 1 queries to locate the marked item in
                                                                                                          the worst case. A surprising result of Grover [3] is that
                                                                                                          a quantum mechanical algorithm can be faster than √   this
                                                                                                          and find the marked item with high probability in O( n)
                                                                                                          quantum queries, contrary to one’s “classical” intuition.
                                                           I. INTRODUCTION
                                                                                                          Grover’s algorithm does not, however, violate the infor-
                                                                                                          mation theoretic lower bound on the minimal number of
                                          Quantum computers have been shown recently to be                queries M .
                                       able to solve certain problems faster than any known al-              The information-theoretic lower bound [4] on M is
                                       gorithm running on a classical computer [1–3]. These               given by the amount of information in the database di-
                                       problems include factoring, which can be performed in              vided by the maximal amount of information retrieved
                                       polynomial time on a quantum computer [2], but is                  by a query which has A possible answers, i.e.
                                       widely believed to be exponentially difficult on a clas-
                                       sical computer, and database lookup, which is provably                                       H(Y )
                                       faster on a quantum computer [3]. Understanding the                                    M≥           ,                    (1.2)
                                                                                                                                    log2 A
                                       power of quantum algorithms and developing new algo-
                                       rithms is of major interest as the building of a quantum
                                                                                                                             P
                                                                                                          where H(Y ) = − y py log2 py , py is the probability for
                                       computer will require a huge investment.
                                                                                                                               P
                                                                                                          Y to contain y and y py = 1.
                                          In this paper we present quantum algorithms for binary            A quantum algorithm employs a database which re-
                                       search and coin-weighing problems in which the informa-            sponds to superpositions of queries with superpositions
                                       tion in a quantum database is retrieved with a single              of answers. The quantum database acts on two input
                                       query. These are applications of Bernstein and Vazirani            registers: register X containing the query state |xi and
                                       parity problem [5] and provide a strong illustration of the        register B, an output register of dimension A initially
                                       power of quantum computation and point out the limi-               containing state |bi. We define the operation of querying
                                       tations of classical information-theoretic bounds applied          the database as
                                       to quantum computers.
                                          Information theory is a useful tool for analyzing the                   Ry : |x, bi → |x, [b + a(x, y)] mod Ai        (1.3)
                                       efficiency of classical algorithms. Problems involving
                                       information retrieval from a database are particularly             where Ry is a classical reversible transformation which
                                       amenable to such analysis. Consider this database search           maps basis states to basis states (that is, a permutation
                                       problem: we have a database Y that contains n items,               matrix) depending on the contents of the database, and
                                       of which a single one is marked. This database is repre-           a(x, y) is the answer to query x, given database state y.
                                       sented as a bit string y of length n with Hamming weight           In a classical query only query basis states |xi are used
                                       one (y has exactly one “1”). One would like to locate the          and the output register B is initially set to |0i. However,


                                                                                                      1
a quantum database is not restricted to working only on              Coin weighing problems are a group of problems in
basis states but can handle arbitrary superpositions of in-        which a set of defective coins is to be identified in a total
puts [7]. Because of this the information that is retrieved        set of coins. Assume there are two types of coins, good
by a single quantum query is not bounded by log2 A. The            and bad ones, and we can weigh arbitrary sets of coins
relevant quantity in the quantum setting is the accessi-           with a spring-scale ( which gives the weight of the set of
ble information in the registers X and B (together called          coins directly, as opposed to a balance which compares
XB) and the internal state of the quantum computer Φ               two sets of coins). All sets of coins are equiprobable. A
about the database Y . Together these are always in a              set of n coins is represented as a bit string y of length n
one of a set of pure states {|ψy i, py }y∈Y and the accessi-       where yi = 1 indicates that coin i is defective. A weighing
ble information on y is bounded by the Kholevo bound               can be represented by a query string x, where xi specifies
[8]                                                                whether coin i is included in the set to be weighed. The
                                                                   result of a classical weighing is the Hamming weight of
              Iacc (ΦXB) ≤ S(ΦXB),                    (1.4)        the bitwise product of x and y, wH (x ∧ y). For this
                                                                   problem the information theoretic bound (1.2) gives
where S(ΦXB) = −TrρΦXB log2 ρΦXBPis the Von Neu-
mann entropy of ΦXB and ρΦXB = y py |ψy ihψy |. In                                               n
                                                                                     M≥                 .                 (2.1)
the case of a classical query, the Von Neumann entropy                                     log2 (n + 1)
S(ΦXB) is strictly less than log2 dim(B) = log2 A which
gives rise to the classical bound (1.2). The quantum algo-         This is close to what the best predetermined algorithm
rithms that will be presented in this paper “violate” the          which perfectly identifies the set of coins can achieve [4]
classical information-theoretic bound by extracting extra
                                                                                                        2n
information in the phases of the query register X. It is                          lim Mpre (n) =               .          (2.2)
notable that Grover’s Hamming weight one problem [3]                             n→∞                  log2 (n)
has been proven optimal [9,10]; no quantum algorithm
                                                                      If one has a spring scale capable of performing weigh-
for this problem can violate the classical information-
                                                                   ings in superposition, then, one can use the Bernstein-
theoretic bound (1.2).
                                                                   Vazirani algorithm to identify the defective coins per-
   The quantum algorithms presented here are a ma-
                                                                   fectly with a single weighing.
jor improvement on the classical algorithms in terms of
                                                                      Define n′ ≡ 2⌈ n+1
                                                                                      2 ⌉ − 1. We construct a query state
computation time if the computation performed by the
database is costly. All our algorithms make use of an in-                                         n          ′

teraction with the database of the form a(x, y) = x · y. A                     1 X          1    X
                                                                        |ψi = √     |xi ⊗ √ ′        (−1)b |bi.           (2.3)
direct implementation of such a database takes O(log n)                        2n x        n + 1 b=0
time using n Toffoli and n XOR gates in parallel. The
database can however be more general than this. Any                The special preparation of register B will make the result
function f (x) with the property that it can be written            of a quantum query end up in the phases of X while
as f (x) = x · y can function as a database. The cir-              leaving register B itself unchanged (cf. [9]). After the
cuit that computes f (x) for any input x ∈ {0, 1}n runs            query we have (using (−1)wh (x∧y) = (−1)x·y )
in some time T (n). We will compare the running time
of the quantum algorithms including this circuit to the                     1 X                  1    Xn           ′


classical running time.                                            |ψy i = √     (−1)x·y |xi ⊗ √ ′        (−1)b |bi. (2.4)
                                                                            2n x                n + 1 b=0

     II. THE PARITY PROBLEM AND COIN                               Thereafter we perform a Hadamard transform H on the
                 WEIGHING                                          query register
                                                                                         1 X
   Bernstein and Vazirani [5,6] have given the first prob-                     H: |xi → √     (−1)x·z |zi.                (2.5)
                                                                                         2n z
lem in which a single quantum query to the database is
sufficient and a strong violation of the classical informa-        This results in the final state
tion theoretic bound comes about. In their parity prob-
lem they consider a database Y which contains an arbi-                                        n   ′
                                                                                        1    X
trary n-bit string y. The answer to queries represented                         |yi ⊗ √ ′        (−1)b |bi,               (2.6)
by n-bit strings x to the database is the parity of the                                n + 1 b=0
bits common to x and y given by a(x, y) = x · y. Note
the the problem is to determine y in its entirety, not to          thus retrieving y within a single query.
merely determine the parity of y. Bernstein and Vazirani              Note that this coin-weighing algorithm uses only the
show that y can be determined in a single query to the             parity of the Hamming weight of the answer whereas the
database. Here we apply this quantum algorithm to the              full Hamming weight is available from the database and
coin weighing problem.                                             is fruitfully used in the classical algorithm.


                                                               2
  We can compare the total running time of this quan-               the queries have Hamming weight n/2. The database
tum algorithm with that of the classical algorithm. The             contains a bit string y with Hamming weight 1. Let us
preprocessing and postprocessing of the register X of the           first look at the problem in which all these bit strings are
query state and the preprocessing of the B register all             equiprobable. We assume that n is an integer power of
consist of the Hadamard transforms on individual bits               two. For other n one simply extends the database size to
                                                                  the next higher power of two.
                     1    1 1                                          Classically it is well known that the marked item can
                R= √               .                (2.7)
                      2 1 −1                                        be found in log2 n queries, which achieves the classical
                                                                    information-theoretic bound (1.2). The k th query, gk , is
which can be done in parallel. The total running time               a string of 2k−1 zeros alternating with a string of 2k−1
is then simply 2 + T (n). In the classical algorithm                ones, where k = 1 . . . log2 n, i.e.
the database circuit is used at least (see Eq. 2.1)
n/ log2 (n + 1) times resulting in a total running time                                  g1 = 01010101..
of at least nT (n)/ log2 (n + 1).                                                        g2 = 00110011..
                                                                                                                            (3.2)
                                                                                         g3 = 00001111..
                                                                                               etc.
        III. COMPRESSIVE ALGORITHMS
                                                                      The result of query gk is
   In this section we will consider modifications of this
problem in which the information in the database H(Y )                              zk ≡ gk · y = a(gk , y),                (3.3)
is less than n bits. In these cases retrieving the data from
                                                                    where zk is the k th bit of the encoding z of y. Each
the source can be viewed as a problem of data compres-
                                                                    y will have a different encoding z and thus z uniquely
sion of a source Y . We will restrict ourselves here to the
                                                                    determines y. The gk s are the generators of the group
compression of the data from a single use of the source.
                                                                    F of Walsh functions whose group multiplication rule is
In the classical case, each query to the database retrieves
                                                                    addition modulo 2. We can represent a Walsh function
a single digit of the word into which the bit string y will         fs as
be encoded. The minimal set of predetermined classical
queries will serve to construct the single quantum query                                    log2 n
                                                                                             X
algorithm. We will use coding schemes that minimize the                             fs =             gi si mod 2,           (3.4)
amount of pre/postprocessing in the single query quan-                                       i=1
tum algorithm. A classically optimal encoding scheme
(cf. [12]) has                                                      where s is an arbitrary bit string of length log2 n. The
                                                                    quantum-mechanical algorithm makes use of superposi-
                                                                    tions of all the Walsh functions. We construct the query
                      X
             H(Y ) ≤      pi li ≤ H(Y ) + 1,            (3.1)
                       i
                                                                    state

where li the length of the compacted yi and pi the prob-                              1 X            |0i − |1i
                                                                               |ψi = √     |s, fs i ⊗ √        .            (3.5)
ability that the database contains bit string yi . It is                               n s                2
not guaranteed however that such an optimal encoding
scheme can be implemented by the type of database in-               After one query the state becomes
teraction that one is given to use, namely (1.3).
                                                                                 1 X                         |0i − |1i
   In the following section we present single query quan-               |ψy i = √     (−1)a(fs ,y) |s, fs i ⊗ √        .    (3.6)
tum algorithms of which the construction is based on op-                          n s                             2
timal classical encoding schemes, namely Huffman cod-
ing. In the section thereafter we consider more general             It can be shown that
type of databases and use a random coding scheme. Each                                1X                      ′

of these schemes will require precomputation of a set of                 hψy |ψy′ i =     (−1)a(fs ,y)+a(fs ,y ) = δyy′ .   (3.7)
                                                                                      n s
queries based on the encoding schemes. The time for
this computation will not be counted in the total run-              We can write
ning time as the queries can be precomputed once and
                                                                                            log2n
reused on subsequent problems.                                                               X
                                                                              a(fs , y) =           sk a(gk , y) mod 2.     (3.8)
                                                                                            k=1
               A. Binary search problem
                                                                    Using (3.3) it follows that a(fs , y) = s · z, and with this
                                                                    we can rewrite (3.7) as
  Binary search problems are defined as problems in
which the database responds with two answers to the                                     1X             ′
                                                                         hψy |ψy′ i =       (−1)s·z+s·z = δzz′ = δyy′ .     (3.9)
query. Here we look at such a search problem in which                                   n s


                                                                3
   As all states |ψy i and |ψy′ i are orthogonal, they can be       of the Walsh generators in the equal probabilities case.
distinguished by a measurement and no further queries               This is illustrated with an example in Figure 2. (In fact,
to the database are required.                                       the Huffman construction results in Walsh queries in the
   What are the transformations that are required for pre-          equal-probability-case.)
and postprocessing of the query? The preparation of the
queries takes 1 + n/2 log2 n steps. Register s is prepared                           p1=0.3
                                                                                                       Code
                                                                                                                          Queries
in superposition using parallel one-bit Hadamard trans-                              p2=0.2           1   11
forms and used as input to the circuit shown in Figure                               p3=0.15          2   01             g1=10011
1. The circuit in Figure 1 uses multi-bit XORs which we                                               3   00             g2=11000
                                                                                     p4=0.15
have counted as being in series. The same sequence in                                                 4   101            g3=00010
reverse is used as the postprocessing. The total time                                p5=0.1           5   100
is thus 2 + n log2 n + T (n). In the classical case the                         FIG. 2. Example of a Huffman code
queries are also prepared using the circuit in Figure 1,
but the multi-bit XORs can be done in parallel, and the                Classically, instead of querying with the Walsh genera-
total time is (log2 n)/2 + T (n) log2 n. Note that in the           tors, one can use these Huffman queries, until the marked
Cirac-Zoller ion-trap model [13] of quantum computation             item has been found. The optimality of the Huffman code
a multi-bit XOR gate can be done in parallel by using the           assures that the expected number of queries is minimized.
“bus phonon” modes. Such quantum computers run our                  Choose the set of queries that will take the place of the
algorithm in time 2 + log2 n + T (n).                               Walsh generators in the following way. Select a set of m
   Note that we could have used all possible queries as in          queries, the first m queries that are used in the classical
section II to retrieve y and subsequently compacted y to            case, such that the probability of not finding the marked
z. This would have taken 2 + T (n) for the algorithm plus           item after these m queries is very small. The value of m
n log2 n steps for the compression, which is the same as            will depend on the probability distribution. If
this direct compression.
                                                                                         m ≤ ⌈log2 n⌉,                      (3.10)

                                                                    this Huffman scheme can be more efficient than a Walsh
  s                                                                 scheme.
                                                                       Note that this requirement is not necessarily satisfied
                                                                    for all probability distributions. For example for the dis-
                                                                                                   9
                                                                    tribution p1 = 1/10, pi = 10n    , i = 1 . . . n, the length of
                                                                    n − 1 encoded words will be about ⌈log2 n⌉. If we choose
                                                                    ⌈log2 n⌉ − s queries, the probability of error will be go to
                                                                    9/10 exponentially as 2−s .
                                                                       This set of m queries will take the place of the Walsh
                                                                    generators in our quantum algorithm. The circuit which
                                                                    implements the Huffman queries will be as in Fig. 1
                                                                    but with a different pattern of XORs corresponding the
                                                                    Huffman queries. All the database states that gave rise
                                                         fs         to distinct codewords after these m classical queries will
                                                                    give rise to distinct |ψy i in our quantum algorithm.
                                                                       If we query only once, the total running time will be
                                                                    2+mn+T (n) if we are willing to accept a small chance of
                                                                    error. A classical algorithm that uses the same Huffman
                                                                    queries and has the same probability of error takes m/2+
                 FIG. 1. “Walsh” Circuit                            mT (n) time. Thus for some probability distributions, m
                                                                    can be significantly smaller than log2 n and the algorithm
   If we generalize this problem to databases that have             is faster than a straightforward search with the Walsh
unequal probabilities assigned to different y’s, a scheme           queries.
based on Huffman coding [12] is sometimes more efficient
in terms of pre/post processing. We assume that the
probability distribution, or H(Y ) is known beforehand.                                  B. Random coding
   Huffman coding is a fixed-to-variable-length encoding
of a source, in our case the database, which is optimal in             The binary search and the coin weighing problem are
the                                                                 special cases of a more general problem in which we have
P sense that it minimizes the average codeword length
   i pi li ≤ H(Y ) + 1 with H(Y ) the entropy of the source.
                                                                    a database Y that contains k arbitrary base A strings of
The encoding prescribes a set of queries that play the role         length n. Here we restrict ourselves to databases that
                                                                    contain k equally probable strings.

                                                                4
  The queries x are all possible base A strings of length n,         For c(s) ∈ CA there is a one-to-one map between c(s)
the elements of (ZZA )n . The database returns the answer          and its encoding z defined in (3.12). This is true as
                     n
                     X                                                        ∀i c ∈ CA , c · gi = 0 ⇔ c = 0                     (3.16)
         a(x, y) =       xi yi mod A ≡ x · y .       (3.11)
                     i                                             which follows from the linear independence of the gener-
                                                                   ators.
The information H(Y ) is equal to logA k. A classical pre-
                                                                     In the quantum algorithm we construct a state
determined algorithm to determine y with high probabil-
ity makes use of m = logA k + l random strings, where                                                            A−1
l is a small integer. Pick m linearly independent ran-                       1        X                    1 X b
                                                                      |ψi = √                 |s, c(s)i ⊗ √       ωA |bi,        (3.17)
dom base A strings of length n; these are the queries gi ,                   m                              A b=0
                                                                                  s|c(s)∈CA
i = 1 . . . m. Similarly to (3.3) we define the encoding as
                                                                                i2π

                     zk = gk · y                     (3.12)        with ωA = e A . The query results in the state
                                                                                                                           A−1
where zk is the k th digit of z. The gi s are used to com-                  1     X           −a(c(s),y)                1 X b
                                                                   |ψy i = √                ωA             |s, c(s)i ⊗ √       ωA |bi.
press the string y of length n to the codewords z of length                 m                                            A b=0
                                                                                s|c(s)∈CA
m. What is the probability that the codeword z de-
termines y uniquely? The probability that two base A                                                                             (3.18)
strings of length
                mm are mapped onto the same codeword
is equal to A1 . Thus, the probability of a collision              We can write, using the encoding z of y defined in (3.12)
with y is
                                                                                      a(c(s), y) = s · z.                        (3.19)
                          m k−1
                           1
           pcol = 1 − 1 −           .                (3.13)        Thus we have
                           A
                                                                                          1 X s·(z−z′ )
For small 2−l we approximate                                               hψy |ψy′ i =       ω         = δzz′ .                 (3.20)
                                                                                          m s A
                    k−1
                2−l
           
 pcol = 1 − 1 −          ∼ 2−l (1 − 1/k) + O(2−2l ) .              If two different strings y and y ′ are mapped onto a dif-
                 k                                                 ferent codeword, they are thus distinguishable by a mea-
                                                     (3.14)        surement. The probability that this occurs (3.14) can be
                                                                   made arbitrary small just as in the classical case since the
This probability can be made arbitrarily small for only            encoding is the same. In order to measure, we reverse the
a relatively small l. Thus O(logA k) random gi s are suf-          preparation steps and then we perform a Fourier trans-
ficient to retrieve the information with arbitrarily low           form over (ZZA )n
probability of error. It is clear that for negative l the
length of the codewords is not sufficiently large to avoid                                  1 X s·z
                                                                                HA : |si → √    ω |zi.                           (3.21)
collisions. A codeword length of O(logA k) is thus neces-                                   m z A
sary as well as sufficient. If the contents of the database
are to be determined with certainty, the codeword length           A measurement in the query basis determines z and, with
must be made larger. A code with no collisions and with            high probability, y.
codeword length O(2 logA k) always exists (cf. the dis-              The circuit used to implement the random coding is
cussion of the birthday problem [15]).                             similar to that in Figure 1 but the XORS are replaced by
   Our quantum algorithm to determine the contents of              summation base A operators,
the database in a single query with high probability
makes use of this classical random coding construction.                      XORA (a, b) = (a + b) mod A                         (3.22)
The random strings gi , i = 1 . . . m are the generators of
a group CA . The multiplication rule for this group is a           and their locations are according to the random queries.
digit-wise addition modulo A and the identity element is              The total quantum running time is 2 + mn + T (n).
the string 0. Members of CA can be written as                      Here the basic unit of time is an operation on an A-
                                                                   dimensional Hilbert space. The classical time using the
                                                                   same random codewords is m/2 + mT (n). Since m is
                              X
       c(s) ∈ CA ⇒ c(s)k =       (gi )k si mod A      (3.15)
                                i                                  less than n, this algorithm is better than the direct coin-
                                                                   weighing algorithm provided we are willing to tolerate a
with c(s)k the k th digit of a group element c(s) and s is a       small chance of error bounded by pcol .
base A string of length m. Due to the linear independence
of the generators, CA is a subgroup of (ZZA )n with Am
elements.

                                                               5
                   IV. DISCUSSION                                       the X register is always reset to |0i to ensure it gives
                                                                        no information on Y . This would not matter to a classi-
   We have discussed the complexity of our quantum al-                  cal query where all the information is in B, but severely
gorithms compared to a classical setup and shown that                   cripples the quantum algorithm. It is not known if such
                                                                        a database will allow any improvement over classical al-
the quantum algorithms are faster in situations in which
                                                                        gorithms.
T (n) > O(n). In problems where querying the database
                                                                    [8] A.S. Kholevo, Problemy Peredachi Informatsii; 9, 3
would occur repeatedly, a bigger (real) separation be-
                                                                        (1973). This paper has appeared in English translation
tween the classical computation time and the quantum                    in Problems of Information Transmission 9, 177 (1973).
computation time could be achieved (see [6] for an in-              [9] C.H. Bennett, E. Bernstein, G. Brassard and U. Vazirani,
stance of such a problem).                                              to appear in SIAM Journal on Computing, also Report-
   It is noteworthy that in the binary search problem in                No. quant-ph/9701001.
the classical case only the generators of the Walsh func-          [10] M. Boyer, G. Brassard, P. Hoyer, and A. Tapp, to appear
tions are required, while the quantum algorithm needs all               in the Proceedings of Physics of Computation ’96, also
the Walsh functions to achieve this speedup. It would be                Report-No. quant-ph/9605034.
interesting to find out whether any speedup is possible            [11] C.E. Shannon, Bell Syst. Tech. J. 27, 379,623 (1948).
if the database only responds to queries which are the             [12] T.M.Cover, J.A.Thomas, Elements of information the-
generators.                                                             ory, Wiley Series in Telecommunications, 1991.
   We have chosen the quantum database Ry as defined               [13] J.I. Cirac and P. Zoller, Phys. Rev. Lett. 74, 4091 (1995).
in (1.3) to make a fair comparison with the classical set-              cf S. Braunstein and J.A. Smolin, Phys. Rev. A. 55, 945
ting. A unitary Uy could easily become more powerful                    (1997) for a discussion.
as was pointed out in [14]. At its most general, a quan-           [14] J.Machta, “Phase information in Quantum Oracle
tum database could be defined by an arbitrary unitary                   Computing”, Physics Department, University of Mas-
transformation acting on an input register and a hidden                 sachusetts at Amherst, manuscript, May 1996.
quantum state (the database). This has no good classical           [15] W.Feller An introduction to probability theory and its ap-
analogue and might be be worthwhile to explore.                         plications, Vol. I, John Wiley & Sons, 1957, p.33.
   We would like to thank Charles H. Bennett, David P.
DiVincenzo and Markus Grassl for helpful discussions,
and the Army Research Office and the Institute for Sci-
entific Interchange, Italy, for financial support. B.M.T.
would like to thank Bernard Nienhuis and Paul Vitanyi
for advice and encouragement.




 [1] D. Simon, “On the power of quantum computation,” Pro-
     ceedings of the 35th Annual Symposium on the Foun-
     dations of Computer Science (IEEE Computer Society
     Press, Los Alamitos, CA 1994), p. 116.
 [2] P.W. Shor, “Algorithms for quantum computation: dis-
     crete log and factoring,” Proceedings of the 35th An-
     nual Symposium on the Foundations of Computer Sci-
     ence (IEEE Computer Society Press, Los Alamitos, CA
     1994), p. 124.
 [3] L.K. Grover, “A fast quantum mechanical algorithm for
     database search,” Proceedings of the 28th Annual ACM
     Symposium on Theory of Computing, 1996, pp. 212-219.
 [4] cf. Martin Aigner, Combinatorial Search, John Wiley &
     Sons, 1988.
 [5] E.Bernstein, U.Vazirani, “Quantum complexity theory”,
     Proceedings of the 25th Annual ACM Symposium on
     Theory of Computing, 1993, pp.11-20.
 [6] E.Bernstein, U.Vazirani, “Quantum complexity theory”,
     final version of [5]. To appear in SIAM Journal on Com-
     puting.
 [7] One could have a nonunitary quantum database where



                                                               6
