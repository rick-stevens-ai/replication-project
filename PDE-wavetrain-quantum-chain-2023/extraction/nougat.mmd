                                            WaveTrain: A Python package for numerical quantum mechanics
                                                     of chain-like systems based on tensor trains

                                                                           Jerome Riedel∗
                                                            Institut für Chemie, Freie Universität Berlin
                                                          Altensteinstraße 23A, D-14195 Berlin, Germany




arXiv:2302.03725v2 [quant-ph] 13 Feb 2023
                                                                            Patrick Gelß†
                                                          Institut für Mathematik, Freie Universität Berlin
                                                           Arnimallee 3–9, D-14195 Berlin, Germany and
                                                    Zuse-Institut Berlin, Takustraße 7, D-14195 Berlin, Germany

                                                                            Rupert Klein‡
                                                          Institut für Mathematik, Freie Universität Berlin
                                                             Arnimallee 3–9, D-14195 Berlin, Germany

                                                                         Burkhard Schmidt§
                                                          Institut für Mathematik, Freie Universität Berlin
                                                           Arnimallee 3–9, D-14195 Berlin, Germany and
                                                     Weierstraß-Institut für Angewandte Analysis und Stochastik,
                                                             Mohrenstraße 39, 10117 Berlin, Germany
                                                                      (Dated: February 14, 2023)




                                                                                 1
                                             Abstract
     WaveTrain is an open-source software for numerical simulations of chain-like quantum systems
with nearest-neighbor (NN) interactions only. The Python package is centered around tensor train
(TT, or matrix product) format representations of Hamiltonian operators and (stationary or time-
evolving) state vectors. It builds on the Python tensor train toolbox Scikit tt, which provides
efficient construction methods and storage schemes for the TT format. Its solvers for eigenvalue
problems and linear differential equations are used in WaveTrain for the time-independent and
time-dependent Schrödinger equations, respectively. Employing efficient decompositions to con-
struct low-rank representations, the tensor-train ranks of state vectors are often found to depend
only marginally on the chain length N . This results in the computational effort growing only
slightly more than linearly with N , thus mitigating the curse of dimensionality. As a complement
to the classes for full quantum mechanics, WaveTrain also contains classes for fully classical and
mixed quantum-classical (Ehrenfest or mean field) dynamics of bipartite systems. The graphical
capabilities allow visualization of quantum dynamics ‘on the fly’, with a choice of several differ-
ent representations based on reduced density matrices. Even though developed for treating quasi
one-dimensional excitonic energy transport in molecular solids or conjugated organic polymers, in-
cluding coupling to phonons, WaveTrain can be used for any kind of chain-like quantum systems,
with or without periodic boundary conditions, and with NN interactions only.
     The present work describes version 1.0 of our WaveTrain software, based on version 1.2 of
scikit tt, both of which are freely available from the GitHub platform where they will also be
further developed. Moreover, WaveTrain is mirrored at SourceForge, within the framework of
the WavePacket project for numerical quantum dynamics. Worked-out demonstration examples
with complete input and output, including animated graphics, are available.




I.     INTRODUCTION


      Progress in ultra-fast experimental techniques, in particular the generation of ultra-short,
intense laser pulses, has led to substantial advances in atomic and molecular physics, chem-
∗
     jerome.riedel@fu-berlin.de
†
     p.gelss@fu-berlin.de
‡
     rupert.klein@math.fu-berlin.de
§
     burkhard.schmidt@fu-berlin.de

                                                2
ical reaction dynamics, material sciences and related fields [1]. This has also motivated
research in theoretical and simulation studies of quantum dynamics in recent years [2–4].
However, in marked contrast to electronic structure theory where a number of software
packages have been under constant development for years or even decades and which have
reached a remarkable degree of sophistication, general-purpose simulation software for quan-
tum dynamics is relatively scarce. For example, QuTiP is an open-source Python framework
for the dynamics of open quantum systems [5, 6]. Another framework for closed and open
quantum systems, coded in Matlab, aims at applications in quantum optics and condensed
matter [7]. Furthermore, Libra offers a toolbox for quantum and classical dynamics simula-
tions, including non-adiabatic processes in molecular system [8]. This is also a main feature
of WavePacket, a general purpose package for solving coupled Schrödinger or Liouville-von
Neumann equations of closed and open quantum systems, respectively [9–11]. Additionally,
it offers modules for fully classical and mixed quantum-classical dynamics on an equal foot-
ing, as well as a module for optimal control. The latter is the focus of QEngine [12], a C++
library, and of Krotov, a Python implementation of quantum optimal control [13].
   Quantum dynamical simulations using any of the software packages mentioned above are
limited to rather few degrees of freedom. This is because of the use of conventional grid tech-
niques for the representations of quantum states and operators, thus suffering from the curse
of dimensionality, i. e., the exponential growth of storage and CPU time with the number of
dimensions. One way to overcome this problem is the multi-configurational time-dependent
Hartree (MCTDH) implementation and its multi-layer (ML) extensions [14, 15]. This pack-
age is frequently used for complex quantum molecular dynamics simulation tasks, and it
has evolved into a quasi-standard in the chemical physics community. From the quantum
physics point of view, similar concepts are formulated in terms of tensor networks. In fact,
it is well established that the (ML-)MCTDH algorithm corresponds to (hierarchical) Tucker
tensor formats. For various types of tensor networks, the ITensor software library is available
for practical calculations [16]. In particular, it contains the density matrix renormalization
group (DMRG) algorithm for computing low-energy states of quantum systems [17].
   The present work deals with high-dimensional quantum dynamics using tensor train
(TT) representations of quantum states and operators, also known as matrix product states
(MPS) and operators (MPO) [18–20]. The idea behind this format is to decompose a high-
dimensional tensor into a chain-like network of lower-dimensional tensors which enables us

                                             3
to simulate and analyze large-scale problems if the underlying coupling structure allows for
low-rank decompositions. Several applications of tensor trains – which can be considered
as a special case of the ansatz used in the multi-layer (ML) variant of MCTDH [14, 15]
mentioned above – and tensor-train operators have shown that it is possible to mitigate
the curse of dimensionality and to tackle high-dimensional problems which cannot be solved
using conventional numerical methods, see, e.g., dynamical systems [21, 22], system identi-
fication [23, 24], quantum mechanics [25–27], and also quantum machine learning [28, 29].
Typically, the applications require the approximation of the solutions of systems of linear
equations, eigenvalue problems, ordinary/partial differential equations. For this reason, we
use the open-source toolbox Scikit-TT1 , a general-purpose package for tensor trains writ-
ten in Python based on NumPy and Scipy. It provides a powerful TT class as well as
different modules for the automatic construction of tensor trains. Furthermore, Scikit-TT
comprises different solvers for algebraic problems which we need for our simulations.
    Herein, we present version 1.0.0 of the WaveTrain software package which special-
izes on high-dimensional quantum dynamics for systems with a chain-like topology and
nearest-neighbor (NN) interactions only. Using tensor-train (TT) representations based on
the so-called SLIM scheme [30], this packet builds on Scikit-TT thus providing efficient
low-rank tensor approximation approaches which aim at reducing the exponential scaling
of the computational effort for solving time-independent and time-dependent Schrödinger
equations in many dimensions. Being restricted to the SLIM scheme for TT representations
for chain-like quantum systems with NN interactions, this approach is less general than
other tensor schemes such as the (hierarchical) Tucker format underlying the ML–MCTDH
scheme, but has the advantage of very favorable scaling of the numerical effort with the
chain length.
    In our previous papers, the TT scheme was applied to the solution of the time-independent
(TISE) and time-dependent Schrödinger equation (TDSE) for exciton-phonon systems of NN
type, i.e., quasi-1D excitonic chains, ranging from few to about one hundred sites [26, 27].
There it was demonstrated that the storage consumption of the SLIM scheme scales linearly
with the number of sites, and the scaling of the CPU time is only slightly less favorable.
Moreover, for the case of the TISE, convergence with regard to the tensor rank was shown
to be essentially independent of the system size. In another recent study, the efficiency in
1
    https://github.com/PGelss/scikit_tt


                                             4
calculating ground states of chains of linear rotors interacting through their dipole moments
was investigated. There, it was found that for these systems a TT-based approach is less
time- and memory-consuming than the state-of-the-art implementation of ML-MCTDH [31,
32]. Finally, it is mentioned that the WaveTrain platform also contains modules for fully
classical and hybrid quantum-classical dynamics dynamics, both for reference and/or for
treating systems that are too complex for fully a quantum-mechanical treatment.


II.     PHYSICAL SYSTEMS AND HAMILTONIANS


      A.   Tensor trains and the SLIM decomposition


      Throughout the WaveTrain software package we limit ourselves to the treatment of
physical/chemical systems with a chain-like topology with NN (nearest neighbor) interac-
tions only. For such systems, quantum-mechanical Hamiltonians H can be decomposed into
operators that either act locally on single sites or that couple NN pairs in a chain with N
sites. Using a so-called SLIM decomposition [30] where the origin of the acronym is due to
the quantities S, L, I, M), the canonical representation of the tensor H ∈ R(d1 ×d1 )×···×(dN ×dN )
only consists of elementary tensors, where at most two (adjacent) components are unequal
to the identity matrix:

                 H = S1 ⊗ I 2 ⊗ · · · ⊗ I N     +       ...   +   I1 ⊗ · · · ⊗ IN −1 ⊗ SN
                           ξ1
                           X
                      +           L1,λ ⊗ M2,λ ⊗ I3 ⊗ · · · ⊗ IN     +    ...
                           λ=1
                           ξN−1
                           X                                                                   (1)
                      +           I1 ⊗ · · · ⊗ IN −2 ⊗ LN −1,λ ⊗ MN,λ
                            λ=1
                            ξN
                           X
                      +           M1,λ ⊗ I2 ⊗ · · · ⊗ IN −1 ⊗ LN,λ .
                           λ=1

Here all components Si , Li,λ , and Mi,λ as well as the identities Ii are matrices in Rdi ×di where
the di are the dimensions of the Hilbert spaces characterizing quantum states on the sites
i. Note that the last line of Eq. (1) is only to comply with periodic boundary conditions of
cyclic systems and can be omitted otherwise.
      As shown in [30], the structure of such a Hamiltonian corresponds to the topology of
a tensor train (TT, also known as matrix product) format. Gathering all components of

                                                    5
Li,λ (Mi,λ ) in corresponding core elements Li (Mi ) in a row-wise (column-wise) fashion, see
Appendix 2 of Ref. [26], allows to express Hamiltonian H in the following form


                                             u                 }
                                                  I2   0 0 0
                                       w             
                          r            wM 0 0 0 
                                         z
                                       w 2
                    H = S1 L1 I1 M1 ⊗ w              ⊗ ...
                                                     
                                       w S2 L2 I2 0 
                                       v             ~
                                          0 0 0 J2
                             u                       } u     }                            (2)
                               IN −1  0      0   0        IN
                             w                        w     
                             wM
                             w N −1 0        0   0   wMN 
                                                       w     
                        ···⊗w                        ⊗w     .
                             w SN −1 LN −1 IN −1 0  w SN 
                             v                       ~ v     ~
                                 0    0      0 JN −1      LN


where Ji comprises ξi identity matrices Ii along the diagonal and zero matrices else. Note
that the double square bracket notation does not stand for block matrices but for the compact
tensor notation of Ref. [30]. The Appendix of that work gives a proof of the above equation
for all heterogeneous, cyclic systems. For homogeneous systems, the core elements Si , Li ,
Ii , Mi , and Ji do not depend on the site index i.

   The ranks of the TT operator (2) are naturally bounded due to the restriction to NN
interactions only, e.g., for homogeneous and periodic systems, we have ξ1 = · · · = ξN =: ξ
and, thus, R = 2 + 2ξ, see [30]. One of the main advantages of SLIM decompositions is the
linear scaling of the memory consumption with N in case that the TT ranks of the solution
do not increase with the order. Similarly, this also holds for the computational effort when
considering time-independent and -dependent Schrödinger equations, see Secs. III B and
III C, respectively. The considered SLIM decompositions in WaveTrain are constructed
using Scikit-TT.

   In the following subsections we will introduce exemplarily a few simple model Hamiltoni-
ans for chain-like systems with their SLIM decompositions and a description of the Python
classes used for their respective implementations. In particular, those are classes for exci-
tons, for phonons, and for exciton-phonon coupling in quasi–1D chains. Note that all these
classes inherit from a common superclass for the implementation of the chain topology, see
also the class hierarchy diagram shown in Fig. 1.

                                              6
                                              Chain
                                     n site
                                     periodic
                                     homogen
              Exciton                get 2Q (n dim)                      Phonon
         alpha, beta, eta                                           mass, nu, omg
                                     get TT (n basis, qtt)          get 2Q (n dim)
         get 2Q (n dim)
         get SLIM (n dim)                                           get SLIM (n dim)

         get exact (n levels)                                       get exact (n levels)

                                              Coupled               potential (q)
                                     alpha, beta, eta               kinetic (p)
                                     mass, nu, omg                  force (q)
                                     chi, rho, sig, tau             hess pot ()
                                     get 2Q (n dims)                hess kin ()
                                     get SLIM (n dims)
                                     qu coupling
                                     cl coupling


FIG. 1. Hierarchy of the Python classes representing the physical systems and Hamiltonians
available as samples in WaveTrain . Selected attributes and methods of each class are given in
the upper and lower parts, respectively, of the boxes. The corresponding Python files are located
in folder wave train/hamilton.




   B.   Super class Chain: General setup of linear or cyclic chain systems



   The properties of the quasi-1D chain-like topologies underlying all of the present work
are handled in super class Chain. For initialization, this class uses just three parameters. In
addition to n site giving the number of sites, N , the two Boolean variables periodic and
homogen specify whether or not periodic boundary conditions are to be used and whether
the chain is homogeneous or heterogeneous, respectively. According to the latter setting, all
further parameters of the respective Hamiltonians are given either as scalars or as Python
lists. Furthermore, the class Chain contains two methods of general use:

                                                7
   a. Method get 2Q is intended for quantum-mechanical Hamiltonians formulated in
terms of the second quantization. For given dimension d (argument n dim) of the local
Hilbert space, which is assumed to be the same for each of the sites, this method sets up
matrix representations of the raising (a† ) and lowering (a) operators, as well as of the num-
ber operators. Where applicable, the position and momentum operators are obtained from
the ladder operators.
   b. Method get TT is at the very heart of the SLIM formalism within our WaveTrain
package. Given the lists of matrices Si,λ , Li,λ , Ii , Mi,λ (potentially independent of site index i
for homogeneous chains) from one of the sub classes described below, this method serves to
construct the tensor train super cores according to Eq. (2). Subsequently, an instance of class
TT (tensor train) from the Scikit-TT package is created whose attributes (dimensions,
ranks, and cores) are then set accordingly, depending on the initialization parameters n site,
periodic, and homogen.



   C.    Class Exciton: Electronic Dynamics


   As a first example, we introduce a simple Hamiltonian for the excitonic dynamics of
atoms or molecules in a chain-like arrangement. For simplicity, we restrict ourselves here to
a chain of two-state-systems, e.g., assuming only excitations of one electron from the highest
occupied to the lowest unoccupied molecular orbital (HOMO–LUMO). Then, the excitonic
Hamiltonian for a heterogeneous system of N sites can be given in terms of (bosonic) exciton
raising, b†i , and lowering, bi , operators for site i

                                    N
                                    X                   N
                                                        X                          
                         H (ex) =         αi b†i bi +         βi b†i bi+1 + bi b†i+1 + η         (3)
                                    i=1                 i=1


where the αi are local (”on site”) excitation energies and η is a general offset of the energy
scale. The nearest-neighbor (NN) coupling energies βi between site i and i + 1, also known
as ”transfer integrals” or ”hopping integrals”, govern the delocalization and mobility of
excitons within this simple model. Here and throughout the following, the last summand
(i = N) of the NN coupling term (with indices i + 1 replaced by 1) is used for systems with
periodic boundary conditions only and is omitted otherwise.
   The most important methods in class Exciton are described in the following:

                                                         8
   a. Method       init : The following sample input illustrates the handling of excitons
within our WaveTrain software package

    from wave_train.hamilton.exciton import Exciton
    hamilton = Exciton(
         n_site=6, periodic=True, homogen=True,
         alpha=0.1, beta=-0.01, eta=0.0
    )

   This creates an object of class Exciton the definition of which is imported from sub folder
hamilton in the wave train source folder. Note that the first three arguments in the code
above are used to initialize the super class Chain, see Sec. II B, whereas the remaining three
arguments specify the energetic parameters α, β, η as given in Eq. (3), the values of which
are taken here from our previous work in Refs. [26, 27].
   b. Method get SLIM: Based on the above attributes of class Exciton and on the defi-
nition of the ladder operators in class Chain, this method provides the SLIM formulation of
Eq. (3) yielding
                                                                   η
                                                Si = αi b†i bi +     Ii
                                                                   N
                                    Li,1 = βi b†i ,       Mi+1,1 = bi+1
                                    Li,2 = βi bi ,        Mi+1,2 = b†i+1                   (4)

where the dependence on the site index i is omitted for the case of a homogeneous chain.
Note that method get SLIM is called from within method get TT in super class Chain to
construct the tensor train supercores according to Eq. (2), see Sec. II A. The following code
line illustrates this for the case of excitons

    hamilton.get_TT(n_basis=2, qtt=False)

   where the first argument gives the dimension d of the local exciton Hilbert space, i.e., the
size of the electronic basis set.
   c. Method get exact: For the case of homogeneous excitonic chains, i.e., with all sites
being equivalent, this method provides analytic/exact solutions of the time-independent
Schrödinger equation (TISE) based on a Bethe ansatz as given in Ref. [26]. In principle,
the number of analytic solutions to be calculated can be chosen by the user, see Sec. III B

                                                      9
below. However, for linear systems, only the energy levels for the ground state and for the
N states within the Fock space of singly excited states are currently available, which are
obtained in close analogy to Hückel theory. For cyclic systems, we also implemented the
N(N − 1)/2 energy levels for states with two quanta of excitation [33].


   D.     Class Phonon: Vibrational Dynamics


   As another example, we introduce a simple Hamiltonian for the vibrational (phononic)
dynamics of a one-dimensional lattice model based on the harmonic approximation. In
terms of site masses mi , displacement coordinates Ri , and conjugate momenta Pi , a general
Hamiltonian can be written as
                                N        N                N
                             1 X Pi2 1 X               1X
                H   (ph)
                           =         +          2 2
                                            mi νi Ri +       µi ωi2 (Ri − Ri+1 )2           (5)
                             2 i=1 mi 2 i=1            2 i=1

where each site i is restrained around its equilibrium position by harmonic oscillators with
frequencies νi . The NN interactions between neighboring sites i and i + 1 are modeled by
harmonic oscillators with frequency ωi and corresponding reduced masses µi = mi mi+1 /(mi +
mi+1 ).
   In analogy to the treatment of the excitons in Sec. II C, we re-formulate the phononic
Hamiltonian of Eq. (5) using second quantization
                              N                 X N
                              X        †      1                               
                 H   (ph)
                            =     ν̃i ci ci +    −     ω̃i c†i + ci c†i+1 + ci+1            (6)
                              i=1
                                              2    i=1


with raising (c†i ) and lowering (ci ) operators of (local) vibrations of site i. The effective
frequencies of single site and NN pair vibrations are given by
                                           mi−1             mi+1
                               r
                                                    2
                          ν̃i = νi2 +              ωi−1 +          ω2                       (7)
                                       mi + mi−1          mi + mi+1 i
                                     µi ωi2
                          ω̃i = √                                                           (8)
                               2 mi ν̃i mi+1 ν̃i+1
where for linear systems without periodic boundary conditions the second or third term
under the square root of Eq. (7) are omitted for the first (i = 1) or last (i = N) site, respec-
tively. Note that the SLIM structure defined in Eq. (1) is apparent in our formulation (6)
for the phononic Hamiltonian.
   The most important methods in class Phonon are described in the following:

                                                 10
   a. Method     init : This sample input shows the setup of the phonon dynamics using
the WaveTrain package

    from wave_train.hamilton.phonon import Phonon
    hamilton = Phonon(
         n_site=6, periodic=True, homogen=True,
         mass=1, nu=1e-3, omg=2**(1/2)1e-3
    )

   which creates an object of class Phonon which is imported from subfolder hamilton in
the wave train source folder. Again, the first three arguments in the code above are used
to initialize the super class Chain, see Sec. II B, whereas the other three arguments specify
the masses and frequency parameters m, ν, ω as given in Eq. (5). The initialization method
of class Phonon also provides the effective frequencies ν̃ and ω̃, see Eqs. (7), (8).
   b. Method get SLIM: Based on the above attributes of class Phonon and on the matrix
representations of the ladder operators from super class Chain, the SLIM formulation of
Eq. (6) is straight-forwardly expressed as
                                                                    
                                                            †      1
                                                  Si = ν̃i ci ci +
                                                                   2
                                            
                         Li,1 = −ω̃i c†i + ci ,   Mi+1,1 = c†i+1 + ci+1                    (9)

where the dependence on the site index i becomes irrelevant for a homogeneous chain. Again,
method get SLIM is called from within method get TT (super class Chain), to construct
the tensor train supercores, see Eq. (2). The use of this method is illustrated here

    hamilton.get_TT(n_basis=8, qtt=False)

   where the first argument gives the dimension d of the local phonon Hilbert space, i.e.,
the size of the harmonic oscillator vibrational basis set. In practice, this parameter needs
to be determined by convergence tests. Typically, it depends on the total energy available
in the simulated system.
   c. Method get exact: Also for the one-dimensional chain of oscillators given in Eqs. (5),
we implemented reference solutions for homogeneous chains to check the accuracy of the
numeric TISE solvers described in Sec. III B below. For periodic chains, analytic (Bloch type)
solutions are well known, see our previous work [26]. For non-periodic systems, where fully

                                             11
analytic solutions are not available because of the non-uniformity of the effective frequencies
in Eqs. (7) and (8), energy levels are obtained from a conventional normal mode analysis
which is considered to be quasi-exact here. Note that this requires the calculation of the
Hessian matrix of the phonon potential energy function of Eq. (5) which is provided in
method hess pot in class Phonon, see also Fig. 1.


   E.     Class Coupled : Exciton-Phonon-Coupling


   Because the excitonic energy transfer is known to be affected by coupling to vibrational
degrees of freedom, the study of exciton-phonon coupling (EPC) is of vital importance, e.g.
for the transport of electronic energy in semiconducting materials [34–36] or the transport
of amide I vibrational energy in helical proteins [37, 38]. Within the Hilbert space used for
EPC, which is a direct product of the Hilbert spaces for the excitonic and phononic states,
the total Hamiltonian can be written as

                               H = H (ex) ⊗ I(ph) + I(ex) ⊗ H (ph) + H (epc)                                 (10)

where H (ex) and H (ph) are the Hamiltonians for excitons and phonons, see Eqs. (3) and
(6), and where I(ex) and I(ph) are identity operators on the respective Hilbert spaces. A
selection of simple, Fröhlich-Holstein type Hamiltonians H (epc) for the coupling of excitons
and phonons is implemented in WaveTrain
                            N
                            X                        N
                                                     X                            
                                  χi b†i bi ⊗ Ri =         χ̄i b†i bi ⊗     †
                                                                           ci + ci
                            i=1                      i=1
                N
                X                                    XN            h                              i
                      ρi b†i bi ⊗ (Ri+1 − Ri ) =           b†i bi ⊗ ρ̄i c†i+1 + ci+1 − ρ̄¯i c†i + ci
                i=1                                  i=1
              N
              X                                      XN            h                                i
                    σi b†i bi ⊗ (Ri+1 − Ri−1 ) =           b†i bi ⊗ σ̄i c†i+1 + ci+1 − σ̄
                                                                                       ¯i c†i−1 + ci−1
              i=1                                    i=1
N
X                                                  XN                         h                              i
      τi b†i bi+1 + bi b†i+1 ⊗ (Ri+1 − Ri ) =                b†i bi+1 + bi b†i+1 ⊗ τ̄i c†i+1 + ci+1 − τ̄¯i c†i + ci
i=1                                                  i=1
                                                                                                                 (11)

Here the EPC constants χ, ρ, and σ give the linear dependence of the excitonic site energies
α on the positions of, or distances between, nearest or second-nearest sites, respectively. In
contrast, the constants τ characterize the dependence of excitonic coupling energies β on the

                                                           12
corresponding distances thus including also Holstein-Peierls type models. The bar notation
in Eq. (11) is used to convert the EPC constants to second quantization
                                        p
                              χ̄i = χi / 2mi ν̃i ,
                                   p                          p
                        ρ̄i = ρi / 2mi+1 ν̃i+1 , ρ̄¯i = ρi / 2mi ν̃i ,
                                   p                          p
                        σ̄i = σi / 2mi+1 ν̃i+1 , σ̄¯i = σi / 2mi−1 ν̃i−1
                                    p                         p
                          τ̄i = τi / 2mi+1 ν̃i+1 , τ̄¯i = τi / 2mi ν̃i                 (12)

Note that in our previous work [26], the distinction between EPC constants with bars and
double bars was missing, which, however, was not required for the cyclic systems mainly
investigated there.
   In the following, a description of important methods comprising class Coupled will be
given:
   a. Method     init : The following lines of input serve to create an instance of class
Coupled

    from wave_train.hamilton.coupled import Coupled
    hamilton = Coupled(
          n_site=5, periodic=True, homogen=True,
          alpha=0.1, beta=-0.01, eta=0.0,
          mass=1, nu=1e-3, omg=1e-3*2**(1/2),
          chi=0, rho=0, sig=1.6e-4, tau=0
    )

   where the first nine arguments specify the chain topology, the excitons, and the phonons,
see Secs. II B, II C, II D, respectively. The last four arguments specify the parameters
χ, ρ, σ, τ required for the different types of EPC models given in Eq. (11). For simplic-
ity, we only consider the σ–coupling mechanisms in the present work.
   b. Method get 2Q: Unlike classes Exciton and Phonon, which essentially use the in-
herited method get 2Q from super class Chain, the class Coupled overrides the super class
method get 2Q. Here, one object of class Exciton and another object of class Phonon are
created, along with their respective matrix representations for ladder operators. This al-
lows a convenient calculation of direct products of excitonic and phononic operators, e.g.,
bi ⊗ ci+1 , using the Numpy function kron for the Kronecker product.

                                           13
   c. Method get SLIM: This method is intended to provide the SLIM formulation of
Eq. (11) which is given by
                                                                                          
                                                       Si = (χ̄i − ρ̄¯i )b†i bi ⊗ c†i + ci
                         Li,1 = (ρ̄i + σ̄i )b†i bi ,   Mi+1,1 = c†i+1 + ci+1
                                               
                         Li,2 = − c†i + ci ,                    ¯i+1 b†i+1 bi+1
                                                       Mi+1,2 = σ̄
                                                                                 
                                    Li,3 = τ̄i b†i ,                        †
                                                       Mi+1,3 = bi+1 ⊗ ci+1 + ci+1 ,
                                              
                  Li,4 = −τ̄¯i b†i ⊗ c†i + ci ,        Mi+1,4 = bi+1 ,
                                                                                   
                                   Li,5 = τ̄i bi ,     Mi+1,5 = b†i+1 ⊗ c†i+1 + ci+1 ,
                                             
                  Li,6 = −τ̄¯i bi ⊗ c†i + ci ,         Mi+1,6 = b†i+1                          (13)

Also here, the method get SLIM is called within method get TT of super class Chain which
constructs the tensor train super cores, see Sec. II B. The following code line illustrates this
for the case of coupled excitons and phonons

       hamilton.get_TT(n_basis=[2, 8], qtt=False)

   where the Python list in the first argument contains the sizes of the electronic and vibra-
tional basis sets, respectively.


III.    QUANTUM AND CLASSICAL DYNAMICS


   A.     Super classes for quantum and classical mechanics


   This section deals with the implementation of different types of physical/chemical dy-
namics within WaveTrain . The main work horses of our software package are the classes
TISE and TDSE containing numerical solvers for the time-independent and time-dependent
Schrödinger equation based on the TT tensor format, see Secs. III B and III C. For com-
pleteness, we have added classes QCMD and CEoM for mixed quantum-classical molecular
dynamics and fully classical dynamics, see Secs. III D and III E.
   The four main classes inherit from a set of super classes for quantum mechanics, mixed
quantum-classical mechanics, and classical mechanics, see Fig. 2 for a class hierarchy di-
agram. Upon initializing objects of any of these classes, an input argument hamilton is

                                                       14
required, which has to be an object of one of the three classes for excitons, phonons, or cou-
pled systems explained above in Sec. II. Note that quantum-classical dynamics only works
for coupled exciton–phonon systems while fully classical dynamics is restricted to phonons
only. Most importantly, each of the three super classes provides a method observe which
deals with calculating and printing expectation values of important observables such as en-
ergy, positions and momenta of the particles. This is complemented by utility methods such
as calculations of ”braket” scalar products, expectation values with their uncertainties, and
reduced density matrices for quantum simulations.
   In turn, the three super classes inherit from the more fundamental class Mechanics for
general mechanical systems. This class contains method save which writes important quan-
tities into binary data files which can be either of Python ’pickle’ or of Matlab ’mat’ type.
Those file types can also be read by method load which thus serves to obtain deviations
between the results of two simulations, e.g., for the case of different dynamic or different
numerical schemes applied to the same physical problem and the same time discretization.
Note that such a comparison is based on root mean squared deviations (RMSD), either for
the quantum state vectors themselves, for populations, or for expectation values of observ-
ables such as positions or momenta. The corresponding file names for such a comparison
are set as properties save file and load file, and the type of comparison is set by the
string compare. Moreover, class Mechanics also contains a method for linear regressions of
conserved quantities, such as energy or norm of state vectors, or of the mentioned RMSDs.
Finally, methods gaussian and sec hyp can be used to set up wave packets with Gaussian
or hyperbolic secant envelope, respectively, see the description of the eligible sub classes in
Secs. III C, III D.


   B.   Class TISE : Time-Independent Schrödinger Equation


   Solving the time-independent Schrödinger equation (TISE)

                               Ĥ|Ψn i = En |Ψn i,   n = 0, 1, . . .                      (14)

yields a set of stationary quantum states |Ψn i along with their corresponding energies En
where Ĥ is one of the (time-independent) Hamiltonians presented in Sec. II or another one
provided by the user. To beat the curse of dimensionality, the strategy followed in the

                                             15
                                                                  Mechanics
                                                        save file, load file, compare
                                                        save, load
                                                        linear regression
                                                        gaussian, sec hyp


                            QuantumMechanics                                        QuantClassMechanics                ClassicalMechanics
                         hamilton                                                hamilton                          hamilton
                         observe                                                 observe                           observe

                         bra ket, expect, reduce, ...
16


                     TISE                             TDSE                                  QCMD                              CEoM
     n levels                             num steps, step size, sub steps      num steps, step size, sub steps    num steps, step size, sub steps
     solver, eigen                        solver, normalize                    solver, normalize                  solver
                                                                               fundamental                        coherent
     ranks, repeats, conv eps             max rank, repeats, threshold
                                          fundamental, coherent                solve, start solve, update solve   solve, start solve, update solv
     e est, ...
     solve, start solve, update solve     solve, start solve, update solve     strang marchuk,pickaback, ...      runge kutta, quasi exact, ...


     FIG. 2. Hierarchy of the Python classes for quantum and classical dynamics available in WaveTrain . Selected attributes and methods of
     each class are given in the upper and lower parts, respectively, of the corresponding boxes. The corresponding Python files are located in
     folder wave train/dynamics.
WaveTrain software builds on low-rank tensor approximations for the state vectors, in
analogy to the TT representation of the Hamiltonian given in Sec. II A. In practice, the
eigenvalue problem is solved numerically using the alternating linear scheme (ALS) which
is an iterative algorithm based on sequential contractions of the TT cores of Ĥ and |Ψn i
to construct low-dimensional eigenvalue problems [39]. A key feature of the WaveTrain
implementation is that not only ground states but also higher excited states can be obtained
in an efficient way by means of integrated Wielandt deflation which enables us to displace
previously computed eigenvalues while keeping all other eigenvalues unchanged, see [26]. To
avoid an explosion of the computational costs for higher excited states, which would arise
in a straight-forward application of the Wielandt deflation, the computation of the deflated
Hamiltonians is implicitly incorporated into the ALS routine of Scikit-TT.
   The use of class TISE is illustrated here by the following sample input

   from wave_train.dynamics.tise import TISE
   dynamics = TISE(hamilton=hamilton, n_levels=10,
                      solver=’als’, eigen=’eigs’,
                      ranks=15, repeats=20, conv_eps=1e-8,
                      e_est=0.08)
   dynamics.solve()

   where object hamilton pertains to one of the classes described in Sec. II and n levels
gives the desired number of eigenvalues to be calculated. The argument solver serves to
choose the scheme to solve the full eigenproblem, by default the above-mentioned ALS al-
gorithm which is one of the key components of the scikit tt package. The next argument,
eigen, specifies the solver used for the micro-problems within each of the ALS iterations, in
this case the sparse matrix eigensolver ’eigs’ from the SciPy package. Alternative choices
are ’eig’ or ’eigh’. The subsequent arguments serve to specify the ALS parameters, most
importantly the number (ranks) of maximal ranks of the solutions. In all cases, ALS itera-
tions are terminated once the estimated eigenvalues do not change by more than a certain
threshold (conv eps) in the last three ALS sweeps or when the number of sweeps reaches the
limit given by attribute repeats. Finally, the parameter e est gives an estimated energy
(here: α − 2|β|) close to which the energy levels are to be searched. If eigen is set to ’eig’,
eigenvalues closest to e est are chosen from the list of all computed eigenvalues. Otherwise

                                             17
Scipy’s ’eigs’ uses the shift-invert mode to find the desired eigenvalues. This is of impor-
tance, e.g., when calculating the stabilization gained from mutual trapping of phonons and
excitons from the lowest eigenvalue within the N (ex) = 1 manifold [26]. Typically, below
that energy there is a huge number of eigenvalues in the N (ex) = 0 manifold which are not
of interest and which can thus be excluded.
   As an alternative, the WaveTrain package offers quasi-exact solutions, provided that the
dimension of the full Hibert space, dN , is not too large (typically 4096 for a standard PC). In
that case, tensor train methods are bypassed and the eigenproblem for a matricized version of
H is solved directly. This is invoked by setting solver = ’qe’ where the parameter eigen
again specifies the choice of the numeric solver. While this option is clearly not eligible for
longer chains, it serves the purpose of creating reference solutions for shorter chains.
   The resulting energy levels will also be compared against analytic (or semi-analytic)
solutions which are available only for the Hamiltonians (3) for uncoupled excitons and (6)
for uncoupled phonons, see also [26].


   C.   Class TDSE : Time-Dependent Schrödinger Equation


   The evolution of quantum states, Ψ(t), is obtained as a solution of the time-dependent
Schrödinger equation (TDSE) for one of the Hamiltonians Ĥ of Sec. II

                              d
                          i      |Ψ(t)i = Ĥ|Ψ(t)i,   |Ψ(t = 0)i = |Ψ0 i                   (15)
                              dt

where atomic units with ~ = 1 are used. Again, the problem of high dimensionality is tackled
by strategies building on low-rank tensor representations of the state vectors. Our imple-
mentation of class TDSE within WaveTrain builds on the choice of numeric propagators
for tensor trains available within the scikit tt software package. Restricting ourselves to
explicit, reversible, and symplectic schemes, the most obvious choice is a symmetric, second
order Euler (S2) method. This method has been routinely used in the quantum dynamics
community for several decades, where it is also known as second-order differencing scheme
[40, 41]. Within WaveTrain , also higher order variants, e.g. fourth (S4) and sixth (S6)
order differencing methods are available. The former one has been shown to offer a good
compromise between efficiency and accuracy [27].
   Frequently used alternatives are based on operator splitting originally developed for cases

                                                18
where Hamiltonians consist of kinetic and potential energy which are treated separately in
momentum and position representation, respectively [42, 43]. In the present work, however,
we resort to the Hamiltonians of Sec. II B for systems with a chain-like topology and NN
interactions only. For such cases, various novel splitting schemes are available in Scikit-TT
which are based on separating the interlacing pairs of NN sites [17, 27, 44]. Not only the
classical first order Lie-Trotter (LT) and second order Strang-Marchuk (SM) schemes, but
also higher-order compositions of the basic methods are available, namely the 4-th order
Yoshida-Neri (YN) and the 8-th order Kahane-Li (KL) method which have displayed an
excellent accuracy in our test calculations [27]. For more information see Ref. [45], where
an overview of splitting methods with different order is given.
   Finally, note that implicit schemes such as the trapezoidal rule or the midpoint rule are
available within scikit tt, too. However, in our quantum dynamics test simulations they
have displayed a very unfavorable numeric effort because they involve the solutions of large-
scale linear systems of equations. While the use of ALS [39] is an integral part of the TISE
class, doing this at each time step results in an unfavorable numerical effort. Therefore, the
TDSE class is solely based on explicit integration schemes.
   To demonstrate the use of the TDSE class we consider the following sample code lines

   from wave_train.dynamics.tdse import TDSE
   dynamics = TDSE(hamilton=hamilton,
        num_steps=50, step_size=20, sub_steps=5,
        solver=’s2’, normalize=0,
        max_rank=8, threshold=1e-12)

   where the object hamilton refers to one of the Hamiltonian classes of Sec. II. Here we
propagate for 1000 (atomic) units of time, divided into 50 main time steps with a (constant)
length of 20 units. After each of the main steps, expectation values of important observables
are calculated and printed, and a frame is added to the (optionally generated) animated
visualization, see Sec. IV. Internally, each of the main steps can be divided into a (constant)
number of sub steps (here 5). The arguments solver and normalize for the initialization
of class TDSE specify the choice of the numeric solver (two-letter codes explained above)
as well as whether normalization of the state vector after every sub step is to be enforced
or not. The remaining arguments are max rank, the maximal rank in the decomposition

                                             19
of solutions Ψ(t), and threshold the value of which is used for the rank truncation within
the splitting schemes (LT, SM, YN, KL) and the symmetric Euler (S2, S4, S6) schemes. In
both cases, an orthonormalization scheme called higher-order singular value decomposition
(HOSVD) [46] with absolute as well as relative cut-off criteria for singular values is applied
to keep the TT ranks of our solutions bouned by max rank.
   Before actually solving the TDSE, it is necessary to specify the initial state |Ψ(t = 0)i =
|Ψ0 i. To that end, the class TDSE contains method fundamental to set up an initial state
where one (or more) sites are fundamentally (0 → 1) excited while all others are prepared in
their ground state. The resulting quantum state is constructed as a tensor train using the
TT class from the Scikit-TT toolbox. That is, depending on a given vector of coefficients
coeffs, the canonical representation of |Ψ0 i is given by the sum over tensor products of the
                      (k)                                  (k)
form coeff[j] · nk=1 vj for non-zero coefficients, where vj = [0, 1]⊤ if k = j and otherwise
               N

[1, 0]⊤ . The created instance of the TT class then stores the cores of the corresponding TT
representation of |Ψ0 i
   While this method works in an analogous way for excitons and phonons, we note that for
coupled systems only the electronic parts are fundamentally excited whereas the vibrational
parts are in their ground states. In the following Python example


   dynamics.fundamental()
   dynamics.solve()


   the default behavior is to return a state with a single excitation localized at the central
site of the chain, which then serves as an initial state for solving the TDSE. It is also possible
to give a vector of coefficients as input for method fundamental, in which case a weighted
sum of products, each with a single site excitation, is returned. This feature of WaveTrain
can be used, e.g., to construct bell-shaped wave packets with Gaussian or hyperbolic secant
(sech) envelope with settable mean position, mean momentum, and width. The Gaussian
shape is typically used to describe a free particle whereas the sech shape typically occurs as
a solution of nonlinear cubic TDSEs, see e.g. Davydov’s soliton theory [38, 47].
   As an alternative to the use of fundamentally excited states, class TDSE also contains
method coherent which is meant only for vibrational systems, see our description of class
Phonons in Sec. II D. That method serves to set up coherent states of the i–th site which

                                              20
are eigenstates of the lowering operator ci , defined as ci |ζii = ζi |ζii with
                                                          ∞
                                                |ζi |2   X   ζk
                                    |ζii = e−     2          √i |kii                     (16)
                                                         k=0
                                                              k!

Here |kii stands for the k-th harmonic oscillator eigenstate of the i-th site and
                                              r
                                                  2
                                     hRi i =           ζi                                (17)
                                                mi ν̃i
gives the mean value of the displacement coordinate, Ri , of the respective quantum harmonic
oscillator with mass mi and effective frequency ν̃i . In analogy to method fundamental, also
method coherent allows for the possibility of a combination of excitations of several sites.
   In close analogy to class TISE described in Sec. III B, also class TDSE offers quasi-exact
solutions for simulations where the full Hilbert space dimension is not too large. In that
case, the matricized Hamiltonian is exponentiated yielding a direct way to calculate the
time evolution operator. This can be useful when benchmarking the accuracy of different
propagation schemes and/or different time steps, see e.g. our results in Ref. [27]. Moreover,
for two-state systems, class TDSE calculates analytic Bessel function solutions of the time
evolution [48], e.g., for class Exciton explained in Sec. II C. However, their use for bench-
marking TT-based solutions is limited because they build on the assumption of non-periodic,
infinitely-long chains.


   D.   Class QCMD: Quantum-Classical Molecular Dynamics


   The above-mentioned TT-based approaches implemented in WaveTrain can be very
helpful instruments in tackling problems in quantum dynamics of bipartite systems such as
the example of coupled excitons and phonons mentioned in Sec. II E. On the one hand, we
have shown that the computational effort is almost linear in N which allows for treating long
chains [26, 27]. On the other hand, these methods can mitigate the curse of dimensionality
only as long as the problem at hand allows for an acceptable accuracy of the approximate
solution when we restrict ourselves to TT cores with ranks of manageable size. However, the
computational effort for solving the TDSE scales at least with d2 (symmetric Euler) where d
is the dimension of the local Hilbert space. Hence, there are still simulation scenarios where
a fully quantum-mechanical treatment is out of reach with the computational resources of
today, and probably also in the foreseeable future.

                                                 21
   In many simulation scenarios, a clear separation of time and/or energy scales is found. In
the above example of coupled excitons and phonons, the NN excitonic coupling energies β
typically exceed the vibrational energies ν, ω, which is due to the disparity of electronic and
nuclear masses [49]. In such cases, a promising way to overcome the curse of dimensionality
is to resort to hybrid quantum-classical molecular dynamics where only the light (fast)
subsystem is treated quantum-mechanically while the classical approximation for the heavy
(slow) subsystem is used. Such approaches appear especially suitable for problems where a
large local Hilbert space dimension d is due to the latter subsystems being more complicated
than those of Eq. (5). An example are conjugated polymer chains where the chromophoric
sub-units are typically connected by a chain segment of several chemical bonds featuring a
number of stretching, bending, and torsional degrees of freedom [50, 51].
   The simplest quantum-classical approach is given by mean field or Ehrenfest dynamics
which rests on a separability ansatz. There, the state vector of the coupled system is
assumed to be a single product of the two subsystem states which is also known as time-
dependent Hartree method. Moreover, the quantum (excitonic) states can be restricted
                                           PN          †
to the Fock space of singly excited states  i=1 ai (t)bi |0i with time-dependent, complex

coefficients ai (t) and with |0i standing for the electronic ground state. While this assumption
neglects couplings to states bearing two or more excitons, it renders a TT-based approach
for the excitons unnecessary.
   For the example of the Hamiltonians of coupled excitons and phonons introduced in
Sec. II, the evolution of the quantum sub-system (excitons) is governed by a Schrödinger-
type equation

                      dai
                  i       = [αi + σi (Ri+1 − Ri−1 ) + W ] ai + βi−1 ai−1 + βi ai+1         (18)
                      dt

where ai (t) are the expansion coefficients of the excitonic state and where W stands for
the (classical) energy of the phonons. Further, the dynamics of the classical sub-system
(phonons) is described in terms of a classical trajectory, R(t), which is governed by a Newton-
type equation

                              d2 Ri
                         mi         = = −mi νi2 Ri
                               dt2
                                                 2
                                        −µj−1 ωj−1 (Ri − Ri−1 ) − σi−1 |ai−1 |2
                                         +µj ωj2 (Ri+1 − Ri ) + σi+1 |ai+1 |2              (19)

                                                   22
Note that here the two sub-systems given in Eqs (18), (19) are coupled to each other through
terms proportional to the EPC constants σi defined in the third row of Eq. (11). For
detailed discussions of the asymtotics and error estimates of the separabilty ansatz and/or
the classical approximation see, e.g., Refs. [38, 47, 52–54].
   The use of class QCMD is shown in the following sample code lines

   from wave_train.dynamics.qcmd import QCMD
   dynamics = QCMD(hamilton=hamilton,
        num_steps=50, step_size=20, sub_steps=5,
        solver=’sm’, normalize=0)
   dynamics.fundamental()
   dynamics.solve()

   where hamilton has to be an object of class Coupled, see Sec. II E, or another class
for bipartite systems provided by the user. Note that in order to be used for Ehrenfest
quantum-classical mechanics simulations, such classes have to provide methods qu coupling
and cl coupling returning the couplings of one sub-system to the respective other one, see
also Fig. 1. For numerically solving the QCMD scheme, there is a choice of numerical prop-
agators implemented within the QCMD class, such as a generalized Lie-Trotter (’lt’) and
Strang-Marchuk method (option ’sm’ in the example code above), as well as the symplectic
pickaback (’pb’) propagator [55].
   The choice of initial conditions for the quantum sub-system (e.g. excitons) is the same as
in Sec. III C for class TDSE, i.e., fundamental electronic excitations, with the possibility for
Gaussian bell-shaped and sech-shaped superpositions thereof. Note that initial excitations
of the classical sub-system (e.g. phonons) are at present not yet implemented.


   E.   Class CEoM : Classical Equations of Motion


   Moreover, we have added a class for solving classical (Newton’s or Hamilton’s) equations
of motion to the WaveTrain package. The motivation for this is to generate reference solu-
tions for systems where a classical analogue to the quantum-mechanical Hamiltonian exists.
Hence, this class works, e.g., with objects of class Phonon. According to the Ehrenfest theo-
rem, quantum-mechanical expectation values of observables such as positions and momenta

                                             23
coincide with results from classical trajectories, as long as the vibrational Hamiltonian is a
polynomial of order not higher than two, which is indeed the case for our harmonic model
Hamiltonian (5). There, the positions are governed by the Newton-type equation (19), but
without the σ term for the EPC.
   The use of class CEoM is illustrated in the following code lines

   from wave_train.dynamics.ceom import CEoM
   dynamics = CEoM(hamilton=hamilton,
        num_steps=50, step_size=20, sub_steps=5,
        solver=’rk’, normalize=0)
   dynamics.coherent(displace=[1.0 if i == hamilton.n_site//2 else 0.0 for i in range(hamilton.
   dynamics.solve()

   where hamilton is an object of class Phonon, for a description see Sec. II D, or another
class provided by the user for a system for which the use of the classical approximation
is justifiable. Note that for use in classical mechanics simulations, such classes have to
encompass additional methods for the calculations of forces and of classical potential and
kinetic energy, see also Fig. 1. For numerically solving the classical equations of motion, there
is a choice of propagators implemented in class CEoM, such as the Runge-Kutta (option
’rk’ in the example above) and the Velocity-Verlet (’vv’) scheme. In addition, quasi-
exact solutions for the harmonic vibrations are available which require additional Python
methods to calculate the Hessian matrices of the potential and kinetic energy functions, see
also Eq. (25) of Ref. [27]. In the sample code above, method coherent of class CEoM is
used to provide classical initial conditions equivalent to those of a coherent state of quantum
harmonic oscillators with the displacement of the classical particles given by Eq. (17), here
with hRi = 1 at the central site and hRi = 0 everywhere else.


   F.   Class Load : Loading data from a previous simulation


   In addition to generating solutions of (stationary or dynamical) equations of motion
as described in the subsections above, WaveTrain also offers the possibility of load-
ing previously generated solutions If, for example, a TDSE simulation is run with option
load file=tdse 1.pic, essential data are stored in a Python pickle file by virtue of method

                                              24
save in class Mechanics, see Sec. III A. Subsequently, this information is easily retrieved
using class Load

   from wave_train.io.load import Load
   dynamics = Load(’tdse_1’, ’pic’)


   The created object contains not only expectation values of important physical observables
which can be used for automated analysis of series of runs, but also the TT representation
of the last bound state (TISE) or the state at the last time step (TDSE) which allows for
an easy restart of a simulation. Finally, objects of class Load contain also reduced density
information which serve the purpose of creating a new (or different) animated visualization
without having to perform another full simulation, see also the following section.


IV.   GRAPHICAL OUTPUT


   The ability to create rich graphical output is one of the hallmarks of simulations with
the WaveTrain software. To meet the demand of users for rich and insightful graphical
representations, the software package provides a set of default visualization classes. They
allow the user to track the progress and stability of computations at run time or to create
graphical output of previously generated results by utilizing the Load class, see Sec. III F.
After completion of a simulation, the plots are available not only as images (png file format)
but also as animations (mp4 file format) which are created using the ffmpeg tool.[56]
   Classes for visualization are created based on a Dependency Injection (DI) scheme, with
different visualization services being injected into the main class Visual, that handles the
execution order of the respective services. Generally, visualizing the results of solving the
equations of motion introduced in Sec. III clusters into two independent services that can
be separately added to the pipeline for creating visual output. In the main service step the
current quantum or classical state is visualized in a collection of subplots for each of the
sites or in a single view along a discretized axis of site indices, in both cases shown in the left
half of the generated figures. Additionally, a second service can be added to monitor system
properties, i.e., energy (TISE, TDSE, QCMD, CEoM), norm (TISE, TDSE, QCMD) and
autocorrelation function (ACF), C(t) = hψ(0)|ψ(t)i (TDSE, QCMD), optionally displayed
in the right half of the generated figures.

                                               25
   The following code snippet illustrates the setup of an animation for visualizing the quan-
tum dynamics of a single system, e.g., a chain of excitons as shown in Fig. 3



    from wave_train.graphics.factory import VisualTDSE


    graphics = VisualTDSE(
         dynamics=dynamics,
         plot_type=’QuantNumbers’,
         plot_expect=True,
         movie_file=’tdse.mp4’).create()
    graphics.solve()

   Here, it is assumed that dynamics is a previously created object of class TDSE, as de-
scribed in Sec. III C. This instance is then inserted into the factory constructor, which
becomes responsible for internal logical checks, e.g., whether plot type, hamilton instance,
and dynamics instance are compatible. The VisualTDSE factory returns an instance of
the Visual class after a call to the create method, which will inject the respective services.
Visualizations of different dynamics instances follows the same logic, with equivalent factory
classes being provided for TISE, QCMD, and CEoM. In the above code snippet, the ser-
vice QuantNumbers for displaying average quantum numbers for each of the sites has been
selected and the toggle (plot expect) for the visualization of system properties (expectation
values of norm and energy, ACF) has been activated. The setup for high-level visualization
of these observables is routed through the factory interface, that provides the factory classes
for the different dynamics implemented in the WaveTrain software (i.e. TISE, TDSE,
QCMD, CEoM). Please note that the new instance graphics provides a proxy to start solv-
ing the Schrödinger equation, thus replacing the calls to dynamics.solve in the code snippets
given previously in Sec. III. Finally, specifying the movie file keyword argument allows to
create animated output in mp4 file format.
   The visualization of the system state in the left half of the figures is based on the reduced
density formalism. Once calculated, the reduced density matrices for each site can be shown
directly, or in the form of populations or averaged quantum numbers, positions and/or
momenta. For an overview of the different visualization options, see Tab. I. That table also

                                             26
   Service             System          Dynamics              Description

   QuantNumbers Exciton, Phonon TISE, TDSE                   Mean quantum numbers

   Populations         Exciton, Phonon TISE, TDSE            Populations of quantum states

   DensityMat          Exciton, Phonon TISE, TDSE            Reduced density matrices

   PhaseSpace          Phonon          TISE, TDSE, CEoM Mean trajectories in phase space

                                                             Excitonic quantum number and
   Positions2          Coupled         TISE, TDSE, QCMD
                                                             lattice distortions as line plots

                                                             Excitonic quantum numbers and
   QuantDisplace2 Coupled              TISE, TDSE, QCMD
                                                             lattice distortions as bar plots

                                                             Excitonic and phononic
   QuantNumbers2 Coupled               TISE, TDSE,
                                                             quantum numbers as bar plots

TABLE I. Overview of the different visualization services and their cross-dependencies regarding
dynamics and system. Upper four options for simple systems, lower three options for bipartite
systems.

lists the special graphics services designed for use with bipartite systems, e.g. the coupled
exciton-phonon systems described in Sec. II E.
   Optionally, the system properties can be visualized in the right half of the figures. These
properties are directly calculated as overlaps or as expectation values by utilizing the tensor
product as provided by scikit tt. Where possible, system properties are always separated into
their individual contributions, e.g., for bipartite systems the state space is visualized for the
two sub-systems separately. Furthermore, for CEoM simulations, the system energy is split
into kinetic and potential energy contributions whereas for QCMD, energy contributions are
decomposed into the contributions from the quantum and classical subsystem, as well as the
energy pertaining to the quantum-classical coupling.
   Typical graphical output from WaveTrain is illustrated and discussed for four selected
cases.

   • Fig. 3 is a visualization of the quantum dynamics of excitons on a linear chain of
         length N = 21, with parameters from Sec. II C. The left half is showing a snapshot
         for t = 540 after an initial excitation of the central site (i = 11) only. The semi-
         transparent bars show analytic solutions which are available for infinitely long chains

                                               27
       of two-level systems with NN coupling only [48]. While analytic and numerical results
       agree well in the middle of the chain, there are considerable discrepancies near the
       edges of the chain, as expected.

     • Fig. 4 shows the quantum dynamics of phonons on a linear chain of length N = 9,
       with parameters from Sec. II D. The left panel represents a snapshots for t = 2000
       after an initial excitation of the central site (i = 4) to a coherent state with hRi = 50.
       For this value of the initial displacement, the representation of quantum state vectors
       in terms of 8 basis functions per site is almost large enough, with tiny deficiencies still
       visible in the deviation of the norm of the state vectors from unity.

     • Fig. 5 visualizes the dynamics of phonons on a linear chain of length N = 9, with
       parameters from Sec. II D. The left panel shows phase-space portraits for 0 ≤ t ≤ 8400
       starting from an initial displacement with hRi = 20 of the central site (i = 4) only.
       Note that for the quadratic Hamiltonian of Eq. (5), resulting expectation values from
       quantum and classical dynamics coincide by virtue of the Ehrenfest theorem.

     • Fig. 6 shows the quantum-classical dynamics of coupled excitons and phonons on
       a linear chain, with parameters from Sec. II E. The left part of the figure shows a
       snapshot at t = 1875 after preparing an initial state with a sech-like distribution of an
       exciton peaked around the central site (i = 20), see Ref. [26], but without vibrational
       excitation. Hence, this simulation shows the formation of a soliton or, more precisely,
       the onset of the dressing of an exciton with phonons in real time.



V.     DOWNLOAD AND INSTALLATION


     The WaveTrain software is a pure Python3 package and can be readily installed from
the PyPI package index using pip. A command line installation of the WaveTrain software
can be achieved by issuing the following command in a terminal environment

      $ pip install wave_train

     where pip installs into a Python3 installation with minimum version requirement 3.7.0.
The source code is publicly available in the Github repository PGelss/wave train under the

                                              28
FIG. 3. Quantum dynamics of excitons on a linear chain. Left panel: snapshot of quantum numbers
for each of the sites. Right panel: evolution of the mean energy and the norm of the state vector
versus time, as well as the autocorrelation function.




FIG. 4. Quantum dynamics of phonons on a linear chain. Left panel: snapshots of populations of
harmonic oscillator states for each of the sites, arranged in a row-wise manner. Right panel: Same
as in Fig. 3.


GNU General Public License v3.0. For a developer installation of WaveTrain , a specific
version of sckit tt may be required, which can be readily installed from the Github repository
PGelss/scikit tt. By default, WaveTrain installs with the latest scikit tt version.

                                               29
FIG. 5. Classical dynamics of phonons on a linear chain. Left panel: trajectories in phase space
for each of the sites. Right panel: Total energy versus time, along with its decomposition in kinetic
and potential contributions.




FIG. 6. Quantum-classical dynamics of coupled excitons and phonons on a linear chain. Left panel:
Snapshots of mean quantum numbers of the excitons (green bars) and vibrational displacements
(scaled by 0.1) of the sites (orange bars). Upper right panel: Total energy versus time, along
with its decomposition in contributions of the quantum and the classical subsystem, as well as
the quantum-classical coupling. Middle and lower right: Norm and autocorrelation function of the
quantum subsystem only.


                                               30
VI.   CONCLUSIONS AND PROSPECT


   In the present work, we have illustrated the use of WaveTrain for rather simple models
of excitons and phonons from our previous works [26, 27]. However, it is straight-forward
to apply our software to a variety of other quantum systems, as long as they are of a linear
or cyclic chain-like topology with on-site and NN interactions only. Obvious extensions of
the models given above include exciton dynamics with more than two electronic states per
site (e.g., singlet and triplet states) and/or anharmonic description of phonons. Note that
in the latter case one does not necessarily have to use the second quantization introduced
in Eq. (6). It is also posssible to use, e.g., pseudo-spectral representations in coordinate
space to discretize the vibrational degrees of freedom [9, 57]. The flexible structure of the
WaveTrain package also allows for easy implementation of other types of quantum systems
such as chains of spin systems (Ising or Heisenberg models), chains of molecular rotors [32],
or polarons in one-dimensional lattices [58]. In all those cases, one would have to design a
new Python class for the underlying Hamiltonian which inherits from the super-class Chain.
It is recommended for such a class to have a method         init   dealing with the physical
parameters of the Hamiltonian (class attributes) and a method       str   generating a string
for print output. A mandatory ingredient of such a class is a method get SLIM providing
the S, L, I, M matrices from which to construct the tensor cores [30], see also Eqs. (1), (2)
in Sec. II A.

   Moreover, the object-oriented architecture of the WaveTrain package also supports a
straight-forward addition of Python classes for further types of equations of motion. An
obvious choice is the Liouville-von Neumann equation (LvNE) adding dissipation and de-
coherence to quantum dynamics. In that case, tensor trains will be used for the repre-
sentations of the density matrices, and numerical solution of the LvNE will rest on the
efficient ODE solvers available in the scikit tt toolbox, similar to our implementation of
class TDSE described in Sec. III C. A frequently used alternative to the Ehrenfest or mean
field quantum-classical approach implemented in class QCMD is the surface hopping trajec-
tory method, featuring stochastic hopping between different electronic states [59]. In such
a case, TT representations are not required, and a corresponding class should contain its
own propagation methods, as is also the case for class QCMD described in Sec. III D. Yet
another option could be diffusive Langevin dynamics adding friction and stochastic forces to

                                            31
classical dynamics, thus extending the class CEoM, see Sec. III E. Note that the classes for
these three examples will inherit from the respective super classes for fully quantum, mixed
quantum-classical, and purely classic dynamics, as described in Sec. III A. Moreover, when
writing a new Python class for another type of dynamics, the following methods will have to
be implemented: In addition to a method      init   for initialization and a method   str   for
print output, it is mandatory for such a class to encompass a method solve. That method
calls start solve used for initialization of the numerical solvers, e.g., propagation one step
backwards in time which is required for the symmetric Euler scheme to solve the TDSE.
Subsequently, for every time-step a method update solve is called that actually carries out
the propagation. Finally, it should be mentioned that each of the dynamics classes needs to
have (one or several) method(s) to generate an initial system state.
   The WaveTrain software package is hosted and further developed at the Github
platform, along with the scikit tt toolbox for tensor train computations on which it is
based. Moreover, WaveTrain is mirrored at the SourceForge platform, as a part of the
WavePacket project for numerical quantum dynamics which is already in use for a number
of years in several labs [9–11]. That MATLAB software package also features quantum and
mixed quantum-classical dynamics, but for general Hamiltonians, i.e., without the restric-
tion to chain-like topologies. The recently published version 7.0 of WavePacket contains a
MATLAB class definition for the Hamiltonians of Eqs. (3), (5), (11) from the present work.
Hence, integration of WaveTrain into the WavePacket project allows for a simple and
direct comparability of results, thus allowing to benefit from the easy usability and the
advanced graphical capabilities of the latter one. However, such comparisons will have to
be limited to short chains up to N ≈ 3 for TISE or N ≈ 6 for TDSE because - without the
use of tensor train methods - WavePacket suffers from the curse of dimensionality.



   ACKNOWLEDGMENTS


   Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)
under Germany’s Excellence Strategy – The Berlin Mathematics Research Center MATH+
(EXC-2046/1, project ID: 390685689) and by the CRC 1114 “Scaling Cascades in Com-
plex Systems” funded by the Deutsche Forschungsgemeinschaft (project ID: 235221301).
Sebastian Matera (Fritz Haber Institute, Berlin) is acknowledged for insightful discussions.

                                            32
  AUTHOR DECLARATIONS


  Conflict of Interest


  No potential conflict of interest was reported by the authors.


  DATA AVAILABILITY


  The Python scripts used to generate the results shown in Figs. 3–6 are openly available
in the Zenodo repository at https://doi.org/10.5281/zenodo.7354077.




                                           33
 [1] F.   C.        De   Schryver,     S.      De    Feyter,   and      G.    Schweitzer,     eds.,
    Femtochemistry: With the Noble Lecture of A. Zewail (Wiley, Weinheim/Germany, 2001).
 [2] V. May and O. Kühn, Charge and Energy Transfer Dynamics in Molecular Systems (Wiley,
    Berlin, 2000).
 [3] D. Tannor, Introduction to Quantum Mechanics. A Time-Dependent Perspective (University
    Science Books, Sausalito, 2004).
 [4] F. Großmann, Theoretical Femtosecond Physics (Springer, Berlin Heidelberg, 2008).
 [5] J. R. Johansson, P. D. Nation, and F. Nori, QuTiP: An open-source Python framework for the
    dynamics of open quantum systems, Computer Physics Communications 183, 1760 (2012).
 [6] J. R. Johansson, P. D. Nation, and F. Nori, QuTiP 2: A Python framework for the dynamics
    of open quantum systems, Computer Physics Communications 184, 1234 (2013).
 [7] A. Norambuena,      D. Tancara, and R. Coto, Coding closed and open quantum
    systems    in    MATLAB:    applications    in   quantum   optics   and   condensed     matter,
    European Journal of Physics 41, 045404 (2020).
 [8] A. V. Akimov, Libra: An open-Source ”methodology discovery” library for quantum and
    classical dynamics simulations, Journal of Computational Chemistry 37, 1626 (2016).
 [9] B. Schmidt and U. Lorenz, WavePacket:            A Matlab package for numerical quan-
    tum dynamics. I: Closed quantum systems and discrete variable representations,
    Computer Physics Communications 213, 223 (2017).
[10] B. Schmidt and C. Hartmann, WavePacket:            A Matlab package for numerical quan-
    tum dynamics. II: Open quantum systems, optimal control, and model reduction,
    Computer Physics Communications 228, 229 (2018).
[11] B. Schmidt, R. Klein, and L. Cancissu Araujo, WavePacket: A Matlab package for numeri-
    cal quantum dynamics. III. Quantum-classical simulations and surface hopping trajectories,
    Journal of Computational Chemistry 40, 2677 (2019).
[12] J. Sørensen, J. Jensen, T. Heinzel, and J. Sherson, QEngine: A C++ library for quantum
    optimal control of ultracold atoms, Computer Physics Communications 243, 135 (2019).
[13] M. H. Goerz, D. Basilewitsch, F. Gago-Encinas, M. G. Krauss, K. P. Horn, D. M. Reich,
    and C. P. Koch, Krotov: A Python implementation of Krotov’s method for quantum optimal

                                               34
    control (2019), arXiv:1902.11284.
[14] M. H. Beck, A. Jäckle, G. A. Worth, and H.-D. Meyer, The multiconfiguration time-
    dependent Hartree (MCTDH) method: a highly efficient algorithm for propagating wavepack-
    ets, Physics Reports 324, 1 (2000).
[15] H. D. Meyer, F. Gatti, and G. A. Worth, eds., Multidimensional quantum dynamics: MCTDH theory and appli
    (Wiley-VCH, 2009).
[16] M. Fishman, S. R. White, and E. M. Stoudenmire, The ITensor Software Library for Tensor
    Network Calculations (2020), arXiv:2007.14822.
[17] S. Paeckel, T. Köhler, A. Swoboda, S. R. Manmana, U. Schollwöck, and C. Hubig, Time-
    evolution methods for matrix-product states, Annals of Physics 411, 167998 (2019).
[18] I. Affleck, T. Kennedy, E. H. Lieb, and H. Tasaki, Rigorous results on valence-bond ground
    states in antiferromagnets, Physical Review Letters 59, 799 (1987).
[19] I. V. Oseledets, A new tensor decomposition, Doklady Mathematics 80, 495 (2009).
[20] I. V. Oseledets and E. E. Tyrtyshnikov, Breaking the curse of dimensionality, or how to use
    SVD in many dimensions, SIAM Journal on Scientific Computing 31, 3744 (2009).
[21] S. Klus, P. Gelß, S. Peitz, and C. Schütte, Tensor-based dynamic mode decomposition,
    Nonlinearity 31, 3359 (2018).
[22] M. Lücke and F. Nüske, tgEDMD: Approximation of the Kolmogorov operator in tensor train
    format (2021), arXiv:2111.09606.
[23] P. Gelß, S. Klus, J. Eisert, and C. Schütte, Multidimensional approximation of nonlinear
    dynamical systems, Journal of Computational and Nonlinear Dynamics 14, 061006 (2019).
[24] A. Goeßmann, M. Götte, I. Roth, R. Sweke, G. Kutyniok, and J. Eisert, Tensor network
    approaches for learning non-linear dynamical laws (2020), arXiv:2002.12388.
[25] A. Veit and L. R. Scott, Using the tensor-train approach to solve the ground-state eigenprob-
    lem for hydrogen molecules, SIAM Journal on Scientific Computing 39, B190 (2017).
[26] P. Gelß,   R. Klein,    S. Matera, and B. Schmidt, Solving the time-independent
    Schrödinger equation for chains of coupled excitons and phonons using tensor trains,
    The Journal of Chemical Physics 156, 024109 (2022).
[27] P. Gelß, R. Klein, S. Matera, and B. Schmidt, Quantum dynamics of coupled excitons and
    phonons in chain-like systems: tensor train approaches and higher-order propagators (2023),
    arXiv:2302.03568.


                                              35
[28] S.    Klus     and     P.     Gelß,   Tensor-based      algorithms    for    image   classification,
     Algorithms 12, 240 (2019).
[29] W. Huggins, P. Patil, B. Mitchell, K. B. Whaley, and E. M. Stoudenmire, Towards quantum
     machine learning with tensor networks, Quantum Science and Technology 4, 024001 (2019).
[30] P. Gelß, S. Klus, S. Matera, and C. Schütte, Nearest-neighbor interaction systems in the
     tensor-train format, Journal of Computational Physics 341, 140 (2017).
[31] S. Mainali, F. Gatti, D. Iouchtchenko, P.-N. Roy, and H.-D. Meyer, Comparison of the multi-
     layer multi-configuration time-dependent Hartree (ML-MCTDH) method and the density
     matrix renormalization group (DMRG) for ground state properties of linear rotor chains,
     The Journal of Chemical Physics 154, 174106 (2021).
[32] T. Serwatka and P.-N. Roy, Ground state of asymmetric tops with DMRG: water in one
     dimension, The Journal of Chemical Physics 156, 044116 (2022).
[33] Z. Hu, G. S. Engel, and S. Kais, Connecting bright and dark states through accidental degen-
     eracy caused by lack of symmetry, The Journal of Chemical Physics 148, 204307 (2018).
[34] O. V. Mikhnenko, P. W. M. Blom, and T.-Q. Nguyen, Exciton diffusion in organic semicon-
     ductors, Energy Environ. Sci. 8, 1867 (2015).
[35] M. Schröter, S. D. Ivanov, J. Schulze, S. P. Polyutov, Y. Yan, T. Pullerits, and O. Kühn,
     Exciton-vibrational coupling in the dynamics and spectroscopy of Frenkel excitons in molecular
     aggregates, Physics Reports 567, 1 (2015).
[36] A. Zhugayevych and S. Tretiak, Theoretical Description of Structural and Electronic Proper-
     ties of Organic Photovoltaic Materials, Annual Review of Physical Chemistry 66, 305 (2015).
[37] A. C. Scott, Davydov’s soliton revisited, Physica D: Nonlinear Phenomena 51, 333 (1991).
[38] D. D. Georgiev and J. F. Glazebrook, On the quantum dynamics of Davydov solitons in
     protein α-helices, Physica A: Statistical Mechanics and its Applications 517, 257 (2019).
[39] S.    Holtz,     T.         Rohwedder,     and     R.    Schneider,    The     Alternating      Lin-
     ear    Scheme        for     Tensor      Optimization    in    the    Tensor     Train       Format,
     SIAM Journal on Scientific Computing 34, A683 (2012).
[40] A. Askar and A. S. Cakmak, Explicit integration method for the time-dependent Schrodinger
     equation for collision problems, The Journal of Chemical Physics 68, 2794 (1978).
[41] C. Leforestier, R. Bisseling, C. Cerjan, M. Feit, R. Friesner, A. Guldberg, A. Hammerich,
     G. Jolicard, W. Karrlein, H.-D. Meyer, N. Lipkin, O. Roncero, and R. Kosloff, A com-


                                                   36
    parison of different propagation schemes for the time dependent Schrödinger equation,
    Journal of Computational Physics 94, 59 (1991).
[42] J. A. Fleck, J. R. Morris, and M. D. Feit, Time-dependent propagation of high energy laser
    beams through the atmosphere, Applied Physics 10, 129 (1976).
[43] M. D. Feit, J. A. Fleck, and A. Steiger, Solution of the Schrödinger equation by a spectral
    method, Journal of Computational Physics 47, 412 (1982).
[44] R. Orús, A practical introduction to tensor networks: Matrix product states and projected
    entangled pair states, Annals of Physics 349, 117 (2014).
[45] C. Lubich, From Quantum to Classical Molecular Dynamics: Reduced Models and Numerical
    Analysis (European Mathematical Society, Zürich, 2008).
[46] I. V. Oseledets, Tensor-train decomposition, SIAM Journal on Scientific Computing 33, 2295 (2011).
[47] A. S. Davydov, Solitons in Molecular Systems (Reidel, 1985).
[48] V. Kenkre and S. Phatak, Exact probability propagators for motion with arbitrary degree of
    transport coherence, Physics Letters A 100, 101 (1984).
[49] F. Lenz, The Ratio of Proton and Electron Masses, Physical Review 82, 554 (1951).
[50] R. Binder, D. Lauvergnat, and I. Burghardt, Conformational Dynamics Guides Coherent
    Exciton Migration in Conjugated Polymer Materials: First-Principles Quantum Dynamical
    Study, Physical Review Letters 120, 227401 (2018).
[51] F. Di Maiolo, D. Brey, R. Binder, and I. Burghardt, Quantum dynamical simulations of intra-
    chain exciton diffusion in an oligo ( para -phenylene vinylene) chain at finite temperature,
    The Journal of Chemical Physics 153, 184107 (2020).
[52] F. A. Bornemann, P. Nettesheim, and C. Schütte, Quantum-classical molecular dynamics as an
    approximation to full quantum dynamics, The Journal of Chemical Physics 105, 1074 (1996).
[53] I. Burghardt,    R. Carles,    C. F. Kammerer,        B. Lasorne, and C. Lasser, Sep-
    aration   of   scales:   dynamical    approximations    for   composite   quantum    systems,
    Journal of Physics A: Mathematical and Theoretical 54, 414002 (2021).
[54] I. Burghardt, R. Carles, C. F. Kammerer, B. Lasorne, and C. Lasser, Dynamical approxima-
    tions for composite quantum systems: assessment of error estimates for a separable ansatz,
    Journal of Physics A: Mathematical and Theoretical 55, 224010 (2022).
[55] P. Nettesheim, F. A. Bornemann, B. Schmidt, and C. Schütte, An explicit and symplectic inte-
    grator for quantum-classical molecular dynamics, Chemical Physics Letters 256, 581 (1996).


                                              37
[56] S. Tomar, Converting video formats with ffmpeg, Linux journal 2006, 10 (2006).
[57] J. C. Light and T. Carrington, Discrete-Variable Representations and their Utilization,
     Advances in Chemical Physics 114, 263 (2000).
[58] J. T. Devreese and A. S. Alexandrov, Fröhlich polaron and bipolaron: Recent developments,
     Reports on Progress in Physics 72, 066501 (2009).
[59] J.     C.     Tully,     Molecular      dynamics      with      electronic       transitions,
     The Journal of Chemical Physics 93, 1061 (1990).




                                             38
