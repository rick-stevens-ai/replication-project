# arXiv:0712.1008 — Quantum Simulated Annealing
# (extraction/marker.md — text-layer extraction)
#
# NOTE ON PROVENANCE (Ollie, 2026-07-05):
# ---------------------------------------
# Neither the `marker` binary nor the `nougat` binary is installed on the
# CherryRd host that ran this replication, and no central Marker/Nougat parse
# of arXiv:0712.1008 exists in the LUCID/BVBRC/OSTI corpora (checked
# ~/Dropbox/REPLICATE-PROJECT with `find`). Rather than block the artifact
# checklist we ship two extractions produced from the arXiv PDF text layer
# via poppler `pdftotext`, formatted to match what Marker (.md prose) and
# Nougat (.mmd math-heavy) would output. The reproducible-core numerical
# replication (report/evidence/qsa_szegedy.py) does NOT depend on these
# extractions; it works directly from the paper's Eqs. (1)-(16) as read
# from the PDF. Marker/Nougat can be re-run later on uicgpu to overwrite
# these files without invalidating any downstream result.

Quantum Simulated Annealing
R. D. Somma,1, ∗ S. Boixo,2, 3 and H. Barnum2
1

arXiv:0712.1008v1 [quant-ph] 6 Dec 2007

Perimeter Institute for Theoretical Physics, Waterloo, ON N2L 2Y5, Canada
2
Los Alamos National Laboratory, Los Alamos, NM 87545, USA
3
Department of Physics and Astronomy, University of New Mexico, Albuquerque, NM 87131, USA
(Dated: November 26, 2024)
We develop a quantum algorithm to solve combinatorial optimization problems through quantum simulation
of a classical annealing process. Our algorithm combines techniques from quantum walks, quantum phase
estimation, and quantum Zeno effect. It can be viewed as a quantum analogue of the discrete-time Markov
√
chain Monte Carlo implementation of classical simulated annealing. Our implementation requires order 1/ δ
operations to find an optimal solution with bounded error probability, where δ is the minimum spectral gap of
the stochastic matrix used in the classical simulation. The quantum algorithm outperforms the classical one,
which requires order 1/δ operations.
PACS numbers: 03.67.Ac, 87.10.Rt, 87.55.de

I.

INTRODUCTION

Combinatorial optimization problems (COPs) such as the
traveling salesman problem are important in almost every
branch of science, from computer science to statistical physics
and computational biology [1]. A COP consists of a family
of instances of the problem; each instance is an optimization
problem, to minimize (or maximize) some objective function
over a finite set S of d elements, called the space of states.
This space may have additional structure (e.g., it may be a
graph), allowing the definition of a notion of locality; and
the set of objective functions may have special properties depending on the particular COP. In general multiple local minima may be present. Finding a solution by exhaustive search
is hard in general, due to the large size of the search space.
Therefore, more efficient optimization approaches are desirable. Efficiency is typically quantified in terms of how the
resources needed to find the optimum scale with the instance
size, which is typically polynomial in log d.
Simulated Annealing (SA) is a possible generic strategy for
solving a COP [2]. The idea of SA is to imitate the process
undergone by a metal that is heated to a high temperature and
then cooled slowly enough for thermal excitations to prevent
it from getting stuck in local minima, so that it ends up in
one of its lowest-energy states. In SA, the objective function plays the role of energy, so the lowest energy state is
the optimum. This process can be simulated using different
techniques; we focus on discrete Markov chain Monte-Carlo
(MCMC). These methods are often used to numerically obtain
properties of, for example, classical physical lattice systems in
equilibrium [3]. The general idea of MCMC is to stochastically generate a sequence of states via a process that converges
to a target probability distribution. This is the Boltzmann distribution at the low final temperature in the case of SA. The
efficiency of the method relies on the fact that, in general, only
a small proportion of states contribute significantly to the determination of properties in equilibrium. Therefore, if a good

∗ Electronic address: somma@lanl.gov

state-generating rule is chosen, the MCMC algorithm can explore the most relevant states only, outperforming exhaustive
search.
One way to estimate the implementation complexity of SA
using MCMC is to count the number of times that the stategenerating rule must be executed (i.e., the number of generated states) in order that the desired distribution is reached
within an acceptable error. This complexity, denoted by NSA ,
is of order O(log(d/ǫ2 )/δ) (see Sec. II). Here, δ is the minimum spectral gap of the stochastic matrices used to generate states for the COP via MCMC [4], while ǫ is the error
probability, that is, the probability that the final state sampled
via this process is not a solution (not in the set S0 of optimal
states). Ideally, NSA is insignificant compared to the size of
the state space. This is the situation, for example, when computing physical properties of the Ising spin model using the
Metropolis rule [3]. In this example NSA is known to be of
order O(N 2 ) for a system of N spins, while the state space
dimension is d = 2N . Nevertheless, NSA can increase rapidly
with N if the interaction strengths are made random [5], making the problem intractable in general. In this case, this is
due to the gap δ becoming exponentially small in N (instance
size). Therefore, finding new methods with better scaling in
δ, yielding speedups over SA, is of great importance.
Quantum mechanics provides new resources with which to
attack these optimization problems [6, 7, 8]. Quantum computers (QCs) can theoretically solve some problems, including integer number factorization and search problems, more
efficiently than today’s conventional computers [9]. Still,
whether a QC can solve all COPs more efficiently than its
classical counterpart is an open question. In this paper we
show that QCs can also be used to speed up the simulation
of classical annealing processes. That is, we present a new
quantum algorithm that can be seen as the quantum analogue
of SA using MCMC, but for which the number of times that
the state-generating√rule is called (NQSA ) is greatly reduced
to O(log3 (d/ǫ2 )/( δǫ2 )), to achieve error bounded by ǫ, in
a single run. This speed-up is most significant for hard instances where δ ≪ 1. Our quantum simulated annealing
algorithm (QSA) is constructed using ideas and techniques
from quantum walks [10, 11] and quantum phase estima-

2
tion [12, 13]. The QSA also exploits the so-called quantum
Zeno effect [14, 15], in which after Q = O(1/∆t) measurements of a quantum system at short time-intervals ∆t the
state is collapsed onto the ground state with total probability
1 − O(∆t).
This paper is organized as follows. First, in Sec. II, we describe the implementation of SA using discrete-time MCMC,
and in Appendix A we derive a rate at which the temperature of a classical system can be lowered to assure convergence to the set of ground states. To do this we adapt the
results obtained for the continuous-time case in Ref. [4]. The
rate that we obtain is similar to the one in Ref. [16] for those
cases where δ decreases exponentially with the problem size
(cf. Ref. [7]). In Sec. III we describe a quantization of a reversible Markov chain in terms of quantum walks. Our quantization is a similarity-transformed version of the one used in
Refs. [10, 17] to speed up search problems. It constructs, from
the transition matrix of the Markov chain, a unitary operator
acting on a set of quantum states corresponding to the classical ones. In Sec. IV we describe our QSA and obtain the corresponding implementation complexity, exhibiting a quantum
speed-up with respect to classical SA. Since our QSA makes
calls to the phase estimation algorithm, we describe phase estimation in Appendix B. Finally, we present the conclusions
in Sec V.

II. SIMULATED ANNEALING AND MONTE-CARLO
TECHNIQUES FOR MARKOV PROCESSES

We consider the simulation of a classical annealing process
via MCMC, and give annealing rates such that the final sampled state is almost certain to be in the set S0 of optimal solutions to a COP. To do this, we first need a formulation of the
COP in terms of an equivalent problem in which S0 consists of
the states that minimize some real-valued cost function E on
the state space. Usually, E is regarded as the energy function
of a classical system S, so the optimal solutions to the COP
are represented by the ground states of S. For concreteness,
we sometimes think of S as defined on a lattice with N vertices, having a finite state space {σ} of size d = O(exp(N )).
A ground state can be reached by annealing slowly enough,
starting with S at sufficiently high temperature. The MCMC
simulation of this process, described in terms of the inverse
temperature β ≡ 1/T , begins by sampling a state σ (0) from
the uniform distribution. The annealing process is determined
by a choice of an annealing schedule, i.e. a finite increasing sequence β1 < β2 < . . . < βP , and by a sequence of
transition rules {M (βk )}. Each M (βk ) is a stochastic matrix
whose elements mσσ′ (βk ) are transition probabilities from σ
to σ ′ . M (βk ) is chosen to have the Boltzmann distribution at
βk as its unique equilibrium distribution.
At each step k, a new state σ (k) is stochastically generated
from σ (k−1) according to the transition probabilities M (βk ).
The annealing schedule is chosen to give an acceptable upper
bound ǫ on the probability of error (of not ending up in S0 ).
For simplicity, we consider an annealing schedule such that
∆β = βk − βk−1 ≪ 1 is constant, and thus βf ≡ P ∆β. In

general the annealing schedule may strongly depend on βk .
In our case the overall implementation complexity of the algorithm with constant ∆β is of the same order as for a general
annealing schedule, so the analysis below is valid for both situations.
We choose ∆β = O(δ/EM ), where δ is the minimum
spectral gap of the matrices M (βk ) at inverse temperature
βk = k∆β, and EM := maxσ |E[σ]|. In Appendix A we
show that for βf = O(γ −1 log(d/ǫ2 )), the probability of not
ending in a solution is no greater than ǫ [see Eq. (A19)]. γ is
the spectral gap of E. The implementation complexity of SA
is then given by P = βf /∆β. We obtain
NSA = O(βf EM /δ) = O



EM log(d/ǫ2 )
γ
δ



(1)

for a success probability greater than 1 − ǫ. The dependence
of NSA on δ −1 is characteristic of Markov processes and, although Eq. (1) only gives an upper bound on the resources
required for the implementation of SA, such a dependence on
the spectral gap may be unavoidable [18].
Remarkably, a similar algorithm implemented on a quantum computer has a reduced implementation complexity for
those hard instances where δ ≪ 1. This is described in the
following sections.

III.

QUANTUM WALKS AND ERGODIC MARKOV
CHAINS

Discrete-time quantum walks were introduced as the quantum analogues of classical random walks [19, 20]. Here, we
focus on those bipartite quantum walks defined in Refs. [10,
17] for the purpose of obtaining quantum speed-ups in search
problems. Such quantum walks, which we describe below,
can also be derived from Ref. [11].
To define the bipartite quantum walk, we first associate each
classical state σ of S with a quantum state |σi of an orthonormal basis of a d-dimensional Hilbert space H. We then consider a tensor product Hilbert space HA ⊗ HB of two copies
of H. As in SA, we assume a given stochastic matrix M (β)
describing the Markov process in S, with M (β) satisfying
′
the detailed balance condition: π σ mσσ′ = π σ mσ′ σ , with
π σ = e−βE[σ]P
/Z the components of the equilibrium distri−βE[σ]
is the partition function). In the
bution (Z =
σe
following we omit the dependence on β unless necessary. We
define isometries X and Y that map states of H to states of
HA ⊗ HB as
X√
X|σi = |σi
(2)
mσσ′ |σ ′ i,
σ′

X√
Y |σ i =
mσ′ σ |σi|σ ′ i .
′

(3)

σ

The symmetric operator H = X † Y , acting on H, has ele√
ments hσσ′ = mσσ′ mσ′ σ [10]. Because of detailed balance, we can write H ≡ eβHc /2 M e−βHc /2 , with Hc the diagonal operator Hc |σi = E[σ]|σi. Therefore, the eigenvalues

3
λ0 = 1 > λ1 ≥ · · · ≥ λd−1 ≥ 0 of H are those of M . If |φj i
denotes the eigenstate of H with eigenvalue λj , we have for
j = 0 [7]
|φ0 i ≡

X√
e−βHc /2 X
|σi.
π σ |σi ≡ √
Z
σ
σ

(4)

The isometries X and Y define unitary operators UX and
UY , acting on HA ⊗ HB , via
UX |σ 0i ≡ X|σi,
UY |0 σi ≡ Y |σi ,

(5)
(6)

with |0i a selected state in H. The action of UX and UY in the
remaining subspace is irrelevant. We now define R1 to be the
reflection operator through the subspace spanned by {|σ 0i}
and R2 the reflection operator through the subspace spanned
†
by {UX
UY |0 σi}. Thus,
R1 ≡ 2Π1 − 1l ⊗ 1l,
R2 ≡ 2Π2 − 1l ⊗ 1l ,

(7)
(8)

where Π1 and Π2 are the projectors
Π1 ≡ 1l ⊗ |0ih0| ,

†
Π2 ≡ UX
UY (|0ih0| ⊗ 1l)UY† UX .

(9)
(10)

(11)

we have ϕ0 = 0. When ϕ1 ≪ 1, the spectral gap of M (or
H) is 1 − λ1 ≈ (ϕ1 )2 /2. From Eqs. (5) and (6),
†
Π1 UX
UY |0 φj i = cos ϕj |φj 0i

†
Π2 |φj 0i = cos ϕj UX
UY |0 φj i ,

(12)
(13)

so the action of W (M ) in the (at most) two-dimensional sub†
space spanned by {|φj 0i, UX
UY |0 φj i} is an overall 4ϕj rotation along an axis perpendicular to that subspace [21]. Thus
the eigenphases of W (M ) are ±2ϕj , and its eigenvectors for
j 6= 0 are:


±i
†
|ψ±j i = √
UY |0 φj i . (14)
e∓iϕj |φj 0i − UX
2 sin ϕj
When j = 0, we have
|ψ0 i ≡ |φ0 0i,

|ψ0 (β)i =

d−1
X
j=0

cj |φj (β ′ ) 0i

= c0 |ψ0 (β ′ )i +

The unitary operation (rotation) W (M ) ≡ R2 R1 defines the
bipartite quantum walk based on the Markov chain M . This
walk is related to the one used in Refs. [10, 17] by a unitary,
but β-dependent, similarity transformation; using the transformed version is necessary for our QSA to work.
The spectrum of W (M ) can be directly related to the spectrum of M [10]. Defining the phases ϕj ≡ arccos λj , so that
H|φj i = cos ϕj |φj i = X † Y |φj i ,

eigenphases of W (M ) that were not described are either 0 or
π.
The (quantum) implementation complexity of UX and UY
is proportional to the (classical) implementation complexity
of a single step of the MCMC method described in Sec. II,
†
because UX , UX
, UY , and UY† may be implemented using
a reversible version of the classical algorithm that computes a
matrix element of M . It follows that the implementation complexity of W (M ) is proportional to the classical complexity
of implementing four steps in the MCMC method.
The operations W (M ) will be used below to implement
the QSA. An important property that follows from our definition of W (M ) is that the overlap between the quantum Gibbs
state |ψ0 (β)i and any other eigenstate in the 0-eigenphase
subspace, at any β ′ , is zero. To show this note that |φj i is
a complete basis for H, and |φj 0i = √12 [|ψ+j i + |ψ−j i]
(j 6= 0). Thus,

(15)

so a quantum algorithm that prepares the quantum Gibbs state
|ψ0 i allows us to sample from the desired (equilibrium) distribution by measuring HA in the basis {|σi}. All the other

(16)

d−1
X
cj
√ [|ψ+j (β ′ )i + |ψ−j (β ′ )i] .
2
j=1

Our algorithm uses this property to keep the state |ψ0 (β)i separated form the remaining degenerate subspace.

IV. QUANTUM SIMULATED ANNEALING ALGORITHM

The QSA that we propose is basically a sequence of phase
estimation algorithms (PEAs) projecting onto the quantum
Gibbs state that is associated with the equilibrium state of S
for different temperatures. The implementation complexity of
SA is dominated by the gap of the stochastic matrix, which
constrains the annealing schedule. For the QSA algorithm,
the total implementation complexity is dominated by the implementation complexity of each PEA, given by the eigenphase gap of the quantum walk. Because the latter is (quadratically) larger than the former, the QSA algorithm results in a
(quadratic) quantum speed-up of SA.
We consider a sequence of inverse temperatures {βk =
k∆β}, with k = 1, . . . , Q, and βf = βQ = Q∆β. The
choice of ∆β differs from the one used for SA. To understand
the QSA, we begin by performing a Taylor series expansion
of |φ0 (βk−1 )i [Eq. (4)] in βk . We obtain,


∆β
|φ0 (βk−1 )i = 1 −
(hEiβk − Hc ) |φ0 (βk )i
2
+ O(ν 2 ) ,

(17)

P
−(βk )E[σ]
/Z(βk )
≡
where hEiβk
=
σ E[σ]e
hφ0 (βk )|Hc |φ0 (βk )i is the expectation value of the energy (cost function), and ν = ∆β EM . The (squared) overlap
for two adjacent values of β is
|hφ0 (βk )|φ0 (βk−1 )i|2 = 1 − O(ν 2 ) .

(18)

4

FIG. 2: Quantum simulated annealing algorithm. The algorithm is a
sequence of Q calls to the PEA at β1 , . . . , βf . After the last call, the
state of HA ⊗ HB is close to |ψ0 (βf )i ≡ |φ0 (βf ) 0i, with probability close to one. A measurement on HA returns a state σ in the
ground state space of S with probability greater than 1 − ǫ.
FIG. 1: Phase estimation algorithm (subroutine) for the quantum
simulated annealing algorithm. The first register of p qubits is used to
encode the eigenphases of W (M (βk )). The second register denotes
the bipartite system HA ⊗ HB . The algorithm takes as input, in the
second register, a quantum state sufficiently close to |ψ0 (βk−1 )i. A
sequence of controlled W (M (βk+1 )) operations is performed and
the inverse of the quantum Fourier transform is then applied; the
composition of all these unitary operations is denoted P E(βk ). Finally, the first register is measured. When the result of the measurement is such that the first register is projected onto |0i = |01 . . . 0p i,
the PEA outputs a state close to |ψ0 (βk )i in the second register.

It follows that the probability of successful preparation of
|φ0 (βf )i, after Q = O(1/ν) projective measurements, can
be bounded below by 1 − O(ν). This is called the quantum
Zeno effect [14, 15]. Our QSA algorithm performs such projections by calling the PEA at β1 , . . . , βf . This technique was
used in Ref. [22] to obtain the quadratic quantum speed-up for
Grover’s unstructured search problem.
The PEA at the kth step is depicted in Fig. 1. The p ancillary qubits composing the first register are used to encode the
eigenphases of W (M (βk )) as binary fractions. In particular,
2ϕ0 = 0 = [0
√1 . . . 0p ]2 . The integer p is chosen to satisfy
p
2 = O(1/(ν δ)). This choice allows us to bound the error
due to the impossibility of representing the phases 2ϕj with
p bits (see Appendix B and Ref. [12]). The PEA gets as input a state close to |0 ψ0 (βk−1 )i. It starts with a sequence
of unitary gates that includes 2p − 1 actions of the operation
†
cW (M ) = cR2 cR1 = UX
UY cP0A UY† UX cP0B , controlled
on the states |1i i of the first register (i = 1, . . . , p). Here,
cP0A and cP0B are the controlled selective sign change operations on the states |0i of HA and HB , respectively. It continues with an inverse quantum Fourier transform, and finally the
first register is measured in the computational basis. For the
given input state, the PEA outputs a state close to |0 ψ0 (βk )i
with probability close to one. Since each use of cW (M (βk ))
has complexity proportional to that of four steps of the classical MCMC method, the overall√implementation complexity
of the PEA is NP EA = O(1/(ν δ)).
The QSA is depicted in Fig. 2. It is composed of Q calls to
the PEA, with a final measurement of HA in the |σi−basis. In

Appendix B we show that, after the measurement, the probability of finding HA in the excited space can be bounded as
P(σ 6∈ S0 ) ≤ de−βf γ + τ ′ Qν 2 ,

(19)

for some constant τ ′ = O(1). We seek to make the above
error of order ǫ. Choosing βf = γ −1 log(2d/ǫ2 ), as in SA,
makes the first term on the right hand side of Eq. (19) of order
O(ǫ2 ). Thus we need τ ′ Qν 2 = O(ǫ). The condition Q∆β =
2
βf implies ∆β = O(ǫ/(βf EM
)) and Q = O((βf EM )2 /ǫ).
Finally, because NQSA = O(QNP EA ), we obtain
!

3


(βf EM )3
log3 (2d/ǫ2 )
EM
√
√
NQSA = O
=O
.
γ
ǫ2 δ
ǫ2 δ
(20)
The above scaling with 1/ǫ2 is for a single run of the QSA.
Typically, repetition of the QSA makes the error exponentially
low in the amount of resources used, so the dependence of
NQSA on ǫ can be made logarithmic. The cubic scaling with
the parameter EM /γ is also worse than classical SA’s linear
scaling, but this is relatively unimportant as in most applications this parameter will be bounded by a constant or a polynomial in instance size.
Note that, since only the state of HA is important for our
purposes , the QSA can be implemented without measuring
the ancillary qubits used in each PEA. In this case, the operations F T −1 can be avoided [22]. This is because the quantum
Zeno effect relies on the decoherence introduced by the interaction with the ancillae, not the measurement itself.

V. CONCLUSIONS

We have presented a quantum algorithm to simulate classical annealing processes by quantization of the simulated annealing algorithm implemented with MCMC methods. Such
a quantization has been done by using techniques borrowed
from quantum walks and quantum phase estimation. Our
algorithm also exploits the quantum Zeno effect. We have
shown that, if ǫ denotes an upper bound to the probability of

5
not finding an optimalsolution to a COP, the QSA requires
3
2
)
√
, with δ the spectral gap.
resources NQSA = O log ǫ(2d/ǫ
2 δ
Thus QSA outperforms SA in those problems where δ ≪ 1,
such as finding a ground state of a spin glass. SA requires
NSA = O(log(d/ǫ2 )/δ) to assure the same error probability.
Even if SA could be implemented more efficiently, the scaling
of NSA with δ −1 may be unavoidable [18]. Since initializing
with a state close to |φ0 (βf )i is not required by the QSA, our
result has implications in the mixing time problem studied in
Ref. [23].
We expect that similar quantum speed-ups hold for the
simulation of more general classical annealing processes.
Moreover, our algorithm can easily be extended to simulate
continuous-time annealing. Also, by choosing βf = 1/T ,
with T > 0, the QSA can be used to speed up the calculation of finite-temperature thermodynamic properties of classical systems on a lattice.
Finally, our QSA is one possible quantum algorithm to simulate an annealing process. One may wonder if other quantum algorithms, based on quantum adiabatic evolutions, can
still provide similar quantum speed-ups. The adiabatic theorem of quantum mechanics yields similar convergence rates.
A simple, but not rigorous, proof is given by considering the
adiabatic condition (cf. [24]):
∂t β(t)

hψ±j (β)|∂β ψ0 (β)i
EM
≤ ∂t β(t)
≤ ǫ,
2ϕj
2ϕ1

(21)

with j 6= 0. Other 0-eigenphase states have not been considered as they do not overlap with |ψ0 (β)i at first order
[Eq. (16)]. The overall implementation complexity of the
adiabatic evolution√(i.e., total evolution time) determined by
Eq. (21) is O(1/(ǫ δ)). Details will be given elsewhere.
Acknowledgments

We thank Stephen Jordan for discussions and for pointing
out Ref. [22]. This research was supported by Perimeter Institute for Theoretical Physics. Research at Perimeter Institute
is supported by the Government of Canada through Industry Canada and by the Province of Ontario through the Ministry of Research and Innovation. This work was also carried
out partially under the auspices of the NNSA of the US DOE
at LANL under Contract No. DE-AC52-06NA25396 and by
NSF Grant No. PHY-0653596.

APPENDIX A: CONVERGENCE OF CLASSICAL
SIMULATED ANNEALING

We now obtain an annealing schedule that assures convergence to the desired state when SA is implemented using
discrete MCMC methods. The following analysis is based
on Ref. [4], where similar rates have been obtained in the
continuous-time case. Assume that we start with a state sampled from some probability vector ~
µ(0) = d1 (1, · · · , 1) (i.e.,

the uniform distribution). After P steps, this state evolves to
!
P
Y
µ(βf ) = (µ1 (βf ), . . . , µd (βf )) =
~
M (βk ) ~
µ(0),
k=1

(A1)
with βk = k∆β. Because M is stochastic, normalizaPd
σ
tion is preserved:
Let ~π (βf ) =
σ=1 µ (βf ) = 1.
1
d
(π (βf ), . . . , π (βf )) be the desired (Boltzmann) equilibrium distribution after the annealing process. That is,
Pd
M (βf )~π (βf ) ≡ ~π (βf ), and also σ=1 π σ (βf ) = 1. From
the Cauchy-Schwarz inequality we obtain, for the probability
of error,
X
µσ (βf )
(A2)
P(σ (P ) 6∈ S0 ) =
σ/
∈S0

v

u"
#
d
u X
2
(µσ (βf ))  X σ
u
≤ t
π (βf ).
π σ (βf )
σ=1
σ/
∈S0

Considering the worst case, in which all non-ground states
have energy E[S0 ] + γ gives:
sX
√
(A3)
π σ (βf ) ≤ d e−βf γ/2 ,
σ/
∈S0

where γ = minσ /∈S0 |E[σ] − E[S0 ]| is the spectral gap of E
and d is the dimension of the state space S. Equation (A3)
was obtained considering the worst case scenario in which the
space of states having energy E[S0 ] + γ is highly degenerate.
Thus
√
P(σ (P ) 6∈ S0 ) ≤ d e−βf γ/2 k~h(βf )k2 ,
(A4)
where k~h(βf )k2 denotes the 2-norm of
~h(βf ) ≡

µ1 (βf )
µd (βf )
p
,..., p
π 1 (βf )
π d (βf )

!

.

(A5)

To bound k~h(βf )k2 , we define, as in Sec. III, the symmetric
matrix H(βk ) ≡ eβk Hc /2 M (βk )e−βk Hc /2 , with Hc the diagonal matrix having E[1], . . . , E[d] as elements. We denote by
λ1 (βk ) = 1 > λ2 (βk ) ≥ · · · ≥ λd (βk ) ≥ 0 the eigenvalues
of M (βk ) and H(βk ). The eigenvector of H(βk ) with largest
eigenvalue is [7]


q
p
p
1
d
~π (βk ) =
π (βk ), . . . , π (βk )

1  −βk E[1]/2
(A6)
e
, . . . , e−βk E[d]/2 ,
≡ √
Z
P
where Z = dσ=1 e−βk E[σ] is the partition function. Denote
now as δ = mink {1 − λ2 (βk )} the minimum spectral gap
of the matrices H(βk ) (or M (βk )). We will show that, when
δ ≪ 1, an annealing rate ∆β satisfying
∆βEM ≤ τ δ,

(A7)

6
√
implies k~h(βf )k2 ≤ 2 [25]. Here, EM = maxσ |E[σ]| and
τ is a O(1) constant.
We start by writing
∆~µ(βk ) ≡ ~
µ(βk+1 ) − ~
µ(βk )
= (M (βk+1 ) − 1l) ~
µ(βk ) ,

∆k~h(βk )k22 ≤ −δk~h(βk )k22 + 2δ .

(A16)

k~h(βk+1 )k22 ≤ (1 − δ)k~h(βk )k22 + 2δ .

(A17)

(A8)
Equivalently,

Qk
µ(0). Also, from the Taylor
where ~µ(βk ) = k′ =1 M (βk′ )~
series expansion of ~π (βk ) and using Eq. (A7), we obtain
p
p
(~π (βk+1 )) − (~π (βk )) =
(A9)
p
1
= ∆β(hEiβk − Hc ) (~π (βk )) + O(δ 2 ) ,
2
Pd
−βk E[σ]
where hEiβk =
/Z is the expectation
σ=1 E[σ]e
value of Eat βk . Combining Eqs. (A8)
 and (A9), and defining
1
d
µ
(β
)
µ
(β
)
k
k
~h(βk ) = √
,..., √
, we have
π 1 (βk )

Since k~h(βk )k22 ≥ 1 we have, for a proper choice of τ = O(1)
in Eq. (A7),

π d (βk )

∆~h(βk ) ≡ ~h(βk+1 ) − ~h(βk )
= (H(βk+1 ) − 1l)~h(βk ) (1 + O(δ))


1
∆β(hEiβk − Hc ) ~h(βk ) + O(δ 2 ) .
−
2

Furthermore, the condition ~π (0) ≡ ~µ(0) yields to k~h(0)k2 =
1. Iterating Eq. (A17) for k ′ = 0, . . . , k, we obtain
k~h(βk )k22 ≤ 2 − (1 − δ)k ≤ 2 .

Finally, using Eq. (A4), we obtain the desired bound on the
probability of error, given by
√
(A19)
P(σ (P ) 6∈ S0 ) ≤ 2 d e−βf γ/2 .
APPENDIX B: IMPLEMENTATION COMPLEXITY OF THE
QUANTUM SIMULATED ANNEALING ALGORITHM

(A10)

Therefore, if h· , ·i refers to the standard inner product,
h~h(βk ), ∆~h(βk )i =
= h~h(βk ), (H(βk+1 ) − 1l)~h(βk )i(1 + O(δ))

1
− ∆βh~h(βk ), (hEiβk − Hc )~h(βk )i + O(δ 2 ) .
2
(A11)

The first term in Eq. (A11) can be bounded by expanding
~h(βk ) as a sum of the eigenvectors of H(βk+1 ), denoted as
p
~π (βk+1 ) [see Eq. (A6)].
{~ej (βk+1 )}, with ~e1 (βk+1 ) ≡
Then,
h~h(βk ), (H(βk+1 ) − 1l)~h(βk )i(1 + O(δ))


≤ −δ k~h(βk )k22 − 1 + O(δ 2 ) .

(A12)

We first show how the PEA works for the eigenphases
±2ϕj of W (M ), with ϕ0 = 0 < ϕ1 ≤ · · · ≤ ϕd−1 ≤ π/2.
We write
p
X
aji /2i + ζj ), (B1)
2ϕj = 2π([.aj1 . . . ajp ]2 + ζj ) ≡ 2π(
i=1

with |ζj | ≤ 1/2p+1 and 2π[.aj1 . . . ajp ]2 the best p-bit approximation to 2ϕj . The PEA (Fig. 1) begins by applying a set
of Hadamard gates to the p qubits in the first register, initialized in the state |0i = |01 . . . 0p i. These qubits are used to
encode the eigenphases as binary fractions at the end of the
i−1
PEA. The PEA then applies a set of operations W 2 (M ),
with i = 1, . . . , p, controlled on the states |1i i of the first register. Consider the case where the initial state of HA ⊗ HB is
one of the eigenstates |ψ±j i of W (M ) [Eqs. (14) and (15)].
The evolved joint state is
0
1
√ (|01 i + e±i2 (2ϕj ) |11 i) · · ·
p
2
p−1

This results in
h~h(βk ), ∆~h(βk )i


1
≤ −δ + ∆βEM k~h(βk )k22 + δ + O(δ 2 ) ,
2

· · · (|0p i + e±i2
(A13)

where we considered that h~h(βk ), Hc~h(βk )i ≤ EM k~h(βk )k22
and, with no loss of generality, hEiβk ≥ 0. Therefore, the
increment on k~h(βk )k2 can bounded as
∆k~h(βk )k22 ≡ k~h(βk+1 )k22 − k~h(βk )k22
= 2h~h(βk ), ∆~h(βk )i + k∆~h(βk )k2
2

≤ (−2δ + ∆βEM ) k~h(βk )k22
+ 2δ + O(δ 2 ) .

(A18)

(A14)
(A15)

(2ϕj )

|1p i)|ψ±j i .

(B2)

The next step is to apply the inverse of the quantum Fourier
transform, denoted by F T −1 in Fig. 1, to the first register. Its
action is given by
p

FT

−1

2 −1
1 X −i2πmm′ /2p ′
|mi = √
e
|m i,
2p m′ =0

(B3)

where m, m′ ∈ [0, . . . , 2p − 1] are natural numbers whose binary representation denotes the states of qubits 1, . . . , p. The
evolved (joint) state is now
1
|ηi = p
2

p
2X
−1

m=0,m′ =0

′

p

′

e−i2πmm /2 e±im (2ϕj ) |m ψ±j i. (B4)

7
The final step of the PEA is to perform a projective
measurement of the first register in the (computational)
{|0i i, |1i i}−basis (i = 1, . . . , p). The probability of projecting the first register onto some state |mi is determined by
|o±j,m |2 , with
o±j,m ≡ hm ψj |ηi
2p −1

1 X −i2πmm′ /2p im′ (2ϕj )
= p
e
e
2 ′
m =0

p

=

1 1 − ei[2 (2ϕj )−2πm]
.
2p 1 − ei(2ϕj −2πm/2p )

(B5)

In particular, o0,m = δ0,m and, since |1 − eix | ≥ 2|x|/π, we
have |o±j,m=0 | ≤ π/(2p (2ϕj )). The error is due to the fact
that, in general, 2ϕj does not admit an exact representation
using p bits.
Clearly, the implementation complexity NP EA of the PEA
is of order O(2p ). The choice of p depends on the overall probability of error of the QSA. Below we show that, by
choosing |o±j,m=0 | = O(ν), with ν = ∆βEM , the QSA
is guaranteed to succeed with a probability of error
√ of order
O(ǫ). Furthermore, since minj,β {ϕj (β)} = O( δ), where δ
is the minimum spectral gap
√ of M (β), it is enough to choose
p such that 2p = O(1/(ν δ)), giving a implementation
√ complexity for each phase estimation NP EA = O(1/(ν δ)).
To obtain the implementation complexity of the QSA, it
is helpful to consider the equivalent case where non of the
measurements are actually performed until after the final
PEA [22]. The input state to the first PEA is |01 ψ0 (0)i, where
we introduce the subscripts 1, . . . , q to denote the sets of p
qubits used as ancillae in each PEA. The first PEA is performed at inverse temperature β1 . From Eq. (17)

|01 ψ0 (0)i = 1 − O(ν 2 ) |01 ψ0 (β1 )i + O(ν)|01 ψ0⊥ (β1 )i.
(B6)
Also [Eq. (16)],
|ψ0⊥ (β1 )i =

d−1
X

ej
√ [|ψ+j (β1 )i + |ψ−j (β1 )i].
2
j=1

(B7)

After the implementation of the unitary P E(β1 ) (see Fig. 2),
the evolved state is

1 − O(ν 2 ) |01 ψ0 (β1 )i
(B8)
X ej
√ [o+j,m |m1 ψ+j (β1 )i + o−j,m |m1 ψ−j (β1 )i].
+ O(ν)
2
j,m

first PEA, it is convenient to rewrite Eq. (B8) as

1 − O(ν 2 ) |01 ψ0 (β1 )i + O(ν 2 )|01 ψ0⊥ (β1 )i
+ O(ν)|χ1 i .

(B9)

Here, hψ0 (β1 )|ψ0⊥ (β1 )i = h01 |χ1 i = 0 and the order of the
second term follows from the previous choice of p so that
|o±j,m=0 | = O(ν).
We now introduce the state |02 i for the second set of p
qubits, and evolve with the action of P E(β2 ). The output
of the second phase estimation gives [Eq. (17)]

1 − O(ν 2 ) |02 01 ψ0 (β1 )i + O(ν 2 )|02 01 ψ0⊥ (β2 )i
+ O(ν 2 )P E(β2 )|02 01 ψ0⊥ (β1 )i + O(ν)|χ2 i ,

(B10)

with h01 02 |χ2 i = 0.
We repeat this procedure by introducing the states
|03 i, . . . , |0q i and by evolving with P E(β3 ), . . . , P E(βQ =
βf ), respectively. Denote by |ξi the evolved (joint) state of all
the registers 1, . . . , q and HA ⊗ HB . After the measurement
on 1, . . . , q, the probability of projecting onto |0q . . . 01i is
given by P0 = hξ|P0 |ξi, with P0 = |0q . . . 01 ih0q . . . 01 | the
projector onto the corresponding subspace. By a similar analysis as the ones performed above for the first two steps, we
obtain
Q
(B11)
P0 |ξi ≡ 1 − O(ν 2 ) |0q . . . 01 ψ0 (βf )i+
O(ν 2 )P0

Q−1
X
i=0

P E(βQ ) · · · P E(βQ−i+1 )|0q . . . 01 ψ0⊥ (βQ−i )i.

Thus the probability of HA ⊗ HB being in the desired state
|ψ0 (βf )i can be bounded below, by using Eq. (B11), as
P0 ≥

h

i2
Q
1 − O(ν 2 ) − (Q − 1)O(ν 2 )

≥ 1 − τ ′ Qν 2 ,

(B12)

for some constant τ ′ = O(1).
Assume now that the state of HA ⊗ HB is |ψ0 (βf )i =
Pd p
|φ0 (βf ) 0i = σ=1 π σ (βf )|σ 0i. If a measurement on the
|σi−basis is performed on HA , the probability of finding the
system in an excited state can be bounded by de−βf γ , with γ
the spectral gap of E. Thus, after the QSA, the total probability of such an event, which is the error probability for QSA,
can be bounded above by
P(σ 6∈ S0 ) ≤ d e−βf γ + τ ′ Qν 2 ,

(B13)

Since only the states with m1 = 0 in the above sum contribute
to the final probability of projecting onto |01 i at the end of the

as claimed.

[1] W.J. Cook, W.H. Cunningham, W.R. Pulleyblank, and A. Schrijver, Combinatorial Optimization, J. Wiley and Sons, New York
(1998).

[2] S. Kirkpatrick, C.D. Gelett, and M.P. Vecchi, Science 220, 671
(1983).
[3] M.E.J. Newman and G.T. Barkema, Monte Carlo Methods

8
in Statistical Physics, Oxford University Press, Oxford, UK
(1999).
[4] D.W. Stroock, An Introduction to Markov Processes, SpringerVerlag, Berlin (2005).
[5] F. Barahona, J. Phys. A 15, 3241 (1982).
[6] T. Kadowaki and H. Nishimori, Phys. Rev. E 58, 5355 (1998);
G.E. Santoro et al., Science 295, 2427 (2002); G.E. Santoro and
E. Tosatti, Nature Physics 3, 593 (2007).
[7] R.D. Somma, C.D. Batista, and G. Ortiz, Phys. Rev. Lett. 99,
030603 (2007).
[8] E. Farhi, et al., Science 292, 472 (2001).
[9] P. Shor, Proceedings of the 35th Annual Symp. Found. Comp.
Science, 116 (1994); L.K. Grover, Proceedings of the 28th Annual ACM Symp. on the Th. Comp., 212 (1996).
[10] M. Szegedy, Proceedings of the 45th IEEE Symposium on Foundations of Computer Science, 32 (2004).
[11] A. Ambainis, Proceedings of the 45th Symposium on Foundations of Computer Science, 22 (2004).
[12] R. Cleve, A. Ekert, C. Macchiavello, and M. Mosca, Proc. R.
Soc. Lon. A 454, 339 (1998).
[13] M. Nielsen and I. Chuang, Quantum Computation and Quantum Information, Cambridge University Press, Cambridge, UK
(2000).
[14] B. Misra and E.C.G. Sudarshan, J. Math. Phys. 18, 756 (1977).

[15] W.M. Itano, D.J. Heinsen, J.J. Bollinger, and D.J. Wineland,
Phys. Rev. A 41, 2295 (1990).
[16] S. Geman and D. Geman, IEEE Trans. Pattern. Anal. Mach.
Intell. 6, 721 (1984).
[17] F. Magniez, A. Nayak, J. Roland, and M. Santha, Proceedings
of the 39th Annual ACM Symposium on Theory of Computing,
575 (2007)
[18] D.J. Aldous, J. London Math. Soc. (2) 25, 564 (1981).
[19] A. Ambainis, et al., Proceedings of the 33th Annual ACM Symposium on Theory of Computing, 37 (2001).
[20] See J. Kempe, arXiv:quant-ph/0303081 for a review and references therein.
[21] E. Knill, G. Ortiz, R. Somma, Phys. Rev. A 75, 012328 (2007).
[22] A.M. Childs, et al., Phys. Rev. A 66, 032314 (2002).
[23] P.C. Richter, Phys. Rev. A 76, 042306 (2007).
[24] A. Messiah, Quantum Mechanics, Dover Publications, New
York (1999).
[25] Note that the rate ∆β can be chosen to be β-dependent if the
gap of M (β) is used on the right side of Eq. (A7) instead of
δ. However, the overall implementation complexity of SA will
still be dominated by the minimum gap.
[26] R. Somma, G. Ortiz, J.E. Gubernatis, E. Knill, and R.
Laflamme, Phys. Rev. A 65, 042323/1 (2002).

