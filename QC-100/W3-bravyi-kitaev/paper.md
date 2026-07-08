## The Bravyi-Kitaev transformation for quantum computation of electronic structure

Jacob T. Seeley, Martin J. Richard, Peter J. Love Haverford College Department of Physics 370 Lancaster Ave Haverford, PA 19041

(Dated: November 27, 2024)

Quantum simulation is an important application of future quantum computers with applications in quantum chemistry, condensed matter, and beyond. Quantum simulation of fermionic systems presents a specific challenge. The Jordan-Wigner transformation allows for representation of a fermionic operator by O(n) qubit operations. Here we develop an alternative method of simulating fermions with qubits, first proposed by Bravyi and Kitaev [S. B. Bravyi, A.Yu. Kitaev, Annals of Physics 298, 210-226 (2002)], that reduces the simulation cost to O(log n) qubit operations for one fermionic operation. We apply this new Bravyi-Kitaev transformation to the task of simulating quantum chemical Hamiltonians, and give a detailed example for the simplest possible case of molecular hydrogen in a minimal basis. We show that the quantum circuit for simulating a single Trotter time-step of the Bravyi-Kitaev derived Hamiltonian for H<sup>2</sup> requires fewer gate applications than the equivalent circuit derived from the Jordan-Wigner transformation. Since the scaling of the Bravyi-Kitaev method is asymptotically better than the Jordan-Wigner method, this result for molecular hydrogen in a minimal basis demonstrates the superior efficiency of the Bravyi-Kitaev method for all quantum computations of electronic structure.

## I. INTRODUCTION

In his seminal article that anticipated the field of quantum information, Feynman argued that simulating quantum systems on classical computers takes an amount of time that scales exponentially with the size of the system, while the cost of quantum simulations can scale in polynomial time with system size [\[1\]](#page-35-0). This possibility may offer a path forward for computational chemistry [\[2,](#page-35-1) [3\]](#page-35-2). A quantum simulation algorithm for quantum chemical Hamiltonians enables the efficient calculation of properties such as energy spectra [\[3\]](#page-35-2), reaction rates [\[4,](#page-35-3) [5\]](#page-36-0), correlation functions [\[6\]](#page-36-1), and molecular properties [\[7\]](#page-36-2) for molecules larger than those that are currently accessible through classical calculations.

Quantum simulation of electronic structure requires a representation of fermions by systems of qubits. Significant progress has been made on efficient quantum simulation of fermions. In 1997, Abrams and Lloyd proposed a simulation scheme for fermions hopping on a lattice [\[8\]](#page-36-3). In 2002, Somma et al. used the Jordan-Wigner to generalize the simulation scheme proposed by Abrams and Lloyd [\[9,](#page-36-4) [10\]](#page-36-5). The Jordan-Wigner transformation has since been used to outline a scalable quantum algorithm for the simulation of molecular electron dynamics, and to design an explicit quantum circuit for simulating a Trotter time-step of the molecular electronic Hamiltonian for H<sup>2</sup> in a minimal basis [\[3,](#page-35-2) [11\]](#page-36-6). Further refinements of the Jordan-Wigner construction were made by Verstrate and Cirac [\[12\]](#page-36-7) and by Bravyi and Kitaev [\[13\]](#page-36-8). From the point of view of fundamental physics, such constructions can be regarded as giving a negative answer to the question of whether fundamental fermi fields are required to explain observed fermionic degrees of freedom [\[14\]](#page-36-9). Practically speaking, such constructions show that quantum computation of electronic structure does not suffer from an analog of the sign problem; that is, fermion antisymmetry represents no significant obstacle to efficient algorithms.

Theoretical progress in quantum simulation has been accompanied by experimental successes. In 2010, Lanyon et al. calculated the energy spectrum of a hydrogen molecule using an optical quantum computer [\[15\]](#page-36-10). For a review of photonic quantum simulators, see [\[16\]](#page-36-11). Du et al. repeated this result to higher precision with NMR shortly thereafter [\[17\]](#page-36-12). Digital quantum simulations of the kind considered in the present paper have been implemented in ion traps using up to 100 gates and 6 qubits [\[18\]](#page-36-13). The progress of trapped ion quantum simulation is detailed in [\[19\]](#page-36-14).

Quantum computation of electronic structure has been the subject of simulation studies [\[3,](#page-35-2) [20\]](#page-36-15) and has been extended to cover relativistic systems [\[21\]](#page-36-16). The history of calculations in quantum chemistry provides a useful sequence of problems reaching from calculations that can be performed on experimental quantum computers today to calculations at the present research frontier [\[22\]](#page-36-17). Despite these promising results, the scaling of the number of gates

required by the algorithm outlined in [\[3,](#page-35-2) [11\]](#page-36-6) remains challenging. It is a subject of active research to find improvements to the (polynomial) scaling of the cost of the algorithm described in [\[3,](#page-35-2) [11\]](#page-36-6). Several improvements are described in [\[23\]](#page-36-18), and the techniques of that work could be combined with those of the present paper to further reduce the resource requirements.

![](_page_2_Picture_2.jpeg)

FIG. 1: A simulation scheme first encodes fermionic states in qubits, then acts with the qubit operator representing the fermionic operator (obtained by the associated transformation), then inverts the encoding to obtain the resultant fermionic state. The criterion for a successful simulation scheme is that this procedure reproduces the action of the fermionic operator, i.e. that Path 1 is equivalent to Path 2, for all basis states — in other words, that this diagram commutes.

<span id="page-2-0"></span>A fermionic simulation scheme can be broken into two pieces: first, to map occupation number basis vectors to states of qubits; and second, to represent the fermionic creation and annihilation operators in terms of operations on qubits in a way that preserves the fermionic anti-commutation relations, as illustrated in Figure [1.](#page-2-0) Previous simulation algorithms have used a straightforward mapping of fermionic occupation number basis states to

qubit states that was originally defined by Zanardi in the context of entanglement [\[3,](#page-35-2) [9,](#page-36-4) [24\]](#page-36-19). The Jordan-Wigner transformation is then used to write the electronic Hamiltonian as a sum over products of Pauli spin operators acting on the qubits of the quantum computer. Subsequently the Hamiltonian terms hk, where Hˆ = P <sup>k</sup> hk, are converted into the unitary gates that are the corresponding time evolution operators. Even though the h<sup>k</sup> do not necessarily commute, their sequential execution on a quantum computer can be made to approximate the unitary propagator e −iHt ˆ through a Trotter decomposition [\[25](#page-36-20)[–28\]](#page-37-0). Finally, the iterative phase estimation algorithm (IPEA) is used to approximate the eigenvalue of an input eigenstate [\[3,](#page-35-2) [11,](#page-36-6) [28\]](#page-37-0).

In this paper we treat the Trotterization process and IPEA as standard procedures. We develop the Bravyi-Kitaev basis and Bravyi-Kitaev transformation, both named after the authors who first proposed such a scheme [\[13\]](#page-36-8), which provide a more efficient mapping between electronic Hamiltonians and qubit Hamiltonians. While the occupation number basis and the Jordan-Wigner transformation allow for the representation of a single fermionic creation or annihilation operator by O(n) qubit operations, the Bravyi-Kitaev basis and transformation require only O(log n) qubit operations to represent one fermionic operator. It is worth noting that Bravyi and Kitaev were concerned with exploring the power of fermions as the basic hardware units of a quantum computer, rather than with the simulation of fermions by qubits [\[13\]](#page-36-8). However, understanding how the structure of fermionic systems can be employed to process information helps us understand how standard quantum information procedures can be used to simulate the structure of fermionic systems. We work out a detailed application of the Bravyi-Kitaev transformation to the operators that appear in quantum chemical Hamiltonians, providing a new way of mapping electronic Hamiltonians to qubit Hamiltonians. We also give explicit Pauli decompositions of the qubit operators derived from this new transformation for the quantum chemical Hamiltonian for H<sup>2</sup> in a minimal basis. We show that the quantum circuit for simulating a single first-order Trotter time-step of the Bravyi-Kitaev minimal basis molecular hydrogen Hamiltonian requires 30 single-qubit gates and 44 CNOT gates, as compared to 46 single-qubit gates and 36 CNOT gates for the Jordan-Wigner Hamiltonian derived in [\[11\]](#page-36-6). Finally, we show that a chemicalprecision estimate of the ground state eigenvalue of the Bravyi-Kitaev Hamiltonian can be obtained in 3 first-order Trotter steps, with a total cost of 222 gates, while the Jordan-Wigner Hamiltonian requires 4 first-order Trotter steps for a total of 328 gates. Since the

Bravyi-Kitaev transformation is known to be asymptotically more efficient, this result for the simplest possible case of molecular hydrogen in a minimal basis demonstrates the superior efficiency of the Bravyi-Kitaev method for all molecular quantum simulations.

In Section [II](#page-4-0) we will review basic quantum chemistry in second quantized form as well as the Jordan Wigner transformation. In Section [III](#page-7-0) we discuss alternatives to the occupation number basis, including the Bravyi-Kitaev basis, which we go on to describe in detail in Section [IV.](#page-12-0) In Section [V](#page-15-0) we present the Bravyi-Kitaev transformation, which allows us to represent creation and annihilation operators in the Bravyi-Kitaev basis. In Section [VI](#page-18-0) we compute the products of these operators that occur in electronic structure Hamiltonians. In Section [VII](#page-23-0) we compute the molecular electronic structure Hamiltonian of H<sup>2</sup> in a minimal basis using the Bravyi-Kitaev basis and transformation. In Section [VIII](#page-27-0) we make an explicit comparison between the Bravyi-Kitaev transformation and the Jordan Wigner transformation by simulating the Trotterization procedure. We close the paper with some conclusions about the utility of the Bravyi-Kitaev transformation.

## <span id="page-4-0"></span>II. BACKGROUND

### A. Fermionic systems and second quantization

We may describe fermionic systems using the formalism of second quantization, in which n single-particle states can be either empty or occupied by a spinless fermionic particle. In the context of quantum chemistry these n states represent spin orbitals, ideally one-electron energy eigenfunctions and often molecular orbitals found by the Hartree-Fock method [\[29,](#page-37-1) [30\]](#page-37-2). We consider a subspace of the full Fock space which is spanned by 2<sup>n</sup> electronic basis states |fn−<sup>1</sup> . . . f0i, where f<sup>j</sup> ∈ {0, 1} is the occupation number of orbital j (restricted to these values due to the Pauli exclusion principle). This is called the occupation number basis.

Any interaction of a fermionic system can be expressed in terms of products of the creation and annihilation operators a † <sup>j</sup> and a<sup>j</sup> , for j ∈ {0, . . . , n−1}. Due to the exchange anti-symmetry of fermions, the action of a † <sup>j</sup> or a<sup>j</sup> introduces a phase to the electronic basis state that depends on the occupancy of all orbitals with index less than j in the occupation number representation. (One can choose instead to define these operators so that it is the

occupation of orbitals with index greater than j that determines the phase — the ordering of orbitals is arbitrary.) These operators act on occupation number basis vectors as follows:

$$a_j^{\dagger} | f_{n-1} \dots f_{j+1} \ 0 \ f_{j-1} \dots f_0 \rangle = (-1)^{\sum_{s=0}^{j-1} f_s} | f_{n-1} \dots f_{j+1} \ 1 \ f_{j-1} \dots f_0 \rangle;$$
 (1)

$$a_j^{\dagger} | f_{n-1} \dots f_{j+1} \ 1 \ f_{j-1} \dots f_0 \rangle = 0;$$
 (2)

$$a_j | f_{n-1} \dots f_{j+1} \ 1 \ f_{j-1} \dots f_0 \rangle = (-1)^{\sum_{s=0}^{j-1} f_s} | f_{n-1} \dots f_{j+1} \ 0 \ f_{j-1} \dots f_0 \rangle;$$
 (3)

$$a_j | f_{n-1} \dots f_{j+1} 0 f_{j-1} \dots f_0 \rangle = 0.$$
 (4)

The canonical fermionic anti-commutation relations enforce the exchange anti-symmetry:

$$[a_j, a_k]_+ = 0, [a_j^{\dagger}, a_k^{\dagger}]_+ = 0, [a_j, a_k^{\dagger}]_+ = \delta_{jk} \mathbf{1},$$
 (5)

where the anti-commutator of operators A and B is defined by [A, B]<sup>+</sup> ≡ AB + BA.

The molecular electronic Hamiltonian of interest in the electronic structure problem is:

<span id="page-5-0"></span>
$$\hat{H} = \sum_{i,j} h_{ij} \ a_i^{\dagger} a_j + \frac{1}{2} \sum_{i,j,k,l} h_{ijkl} \ a_i^{\dagger} a_j^{\dagger} a_k a_l.$$
 (6)

The coefficients hij and hijkl are one- and two-electron overlap integrals, which can be precomputed classically and input to the quantum simulation as parameters [\[3,](#page-35-2) [11,](#page-36-6) [29\]](#page-37-1).

As an application of the techniques presented in this paper (Section [VII\)](#page-23-0), we treat molecular hydrogen in a minimal basis. Thus, we construct two spatial molecular orbitals by taking linear combinations of the localized atomic spatial wavefunctions: ψ<sup>g</sup> = ψH<sup>1</sup> + ψH<sup>2</sup> and ψ<sup>u</sup> = ψH<sup>1</sup> − ψH2. Here the subscripts g and u stand for the German words gerade and ungerade — even and odd. In general one must take a Slater determinant to determine the correctly anti-symmetrized wavefunctions of the fermionic system, but in this case we can guess them by inspection. The form of the spatial wavefunctions is determined by the choice of basis set. STO-3G is a commonly used Gaussian basis set — for further details see [\[29,](#page-37-1) [30\]](#page-37-2).

Molecular spin orbitals are formed by taking the product of these two molecular spatial orbitals with one of two orthogonal spin functions, |αi and |βi. Thus, the four molecular spin orbitals in our model of the hydrogen molecule (which correspond to the operators a (†) j ) are:

$$|\chi_0\rangle = |\psi_g\rangle|\alpha\rangle, \qquad |\chi_1\rangle = |\psi_g\rangle|\beta\rangle, \qquad |\chi_2\rangle = |\psi_u\rangle|\alpha\rangle, \qquad |\chi_3\rangle = |\psi_u\rangle|\beta\rangle.$$
 (7)

In the next section we will review the occupation number basis and the Jordan-Wigner transformation, which together have been established as a standard method for mapping fermionic systems to quantum computers [3, 9, 11, 15].

## B. The Jordan-Wigner transformation

The form of electronic occupation number basis vectors suggests the following identification between electronic basis states on the left and states of our quantum computer [24]:

$$|f_{n-1} \dots f_1 f_0\rangle \to |q_{n-1}\rangle \dots \otimes |q_1\rangle \otimes |q_0\rangle, \qquad f_j = q_j \in \{0, 1\}.$$
 (8)

That is, we let the state of each qubit  $|q_j\rangle$  store  $f_j$ , the occupation number of orbital j. We refer to this method of encoding fermionic states as the occupation number basis for qubits. The next step is to map fermionic creation and annihilation operators onto operators on qubits.

We can form one-qubit creation and annihilation operators,  $\hat{Q}^+$  and  $\hat{Q}^-$ , that act on qubits of our quantum computer as follows:

$$\hat{Q}^{+}|0\rangle = |1\rangle, \qquad \hat{Q}^{+}|1\rangle = 0, \qquad \hat{Q}^{-}|1\rangle = |0\rangle, \qquad \hat{Q}^{-}|0\rangle = 0.$$
 (9)

We could proceed by following the standard recipe for turning p-qubit quantum gates into operators acting on an n-qubit quantum computer  $(n \ge p)$  by taking the tensor product of the gates acting on the target qubits with the identity acting on the other (n-p) qubits. However, it is easy to show that the qubit creation and annihilation operators formed in this way do not obey the fermionic anti-commutation relations.

Expressing the qubit creation and annihilation operators in terms of Pauli matrices suggests a way forward:

$$\hat{Q}^{+} = |1\rangle\langle 0| = \frac{1}{2}(\sigma^{x} - i\sigma^{y}), \qquad \hat{Q}^{-} = |0\rangle\langle 1| = \frac{1}{2}(\sigma^{x} + i\sigma^{y}).$$
 (10)

The mutual anti-commutation of the three Pauli matrices allows us to recognize that  $\hat{Q}^{\pm}$  anti-commutes with  $\sigma^z$ . Thus if we represent the action of  $a_j^{\dagger}$  or  $a_j$  by acting with  $\hat{Q}_j^{\pm}$  and with  $\sigma^z$  on all qubits with index less than j, our qubit operators will obey the fermionic anti-commutation relations. Put differently, the states of our quantum computer will acquire the same phases under the action of our qubit operator as do the electronic basis states under

the action of the corresponding creation or annihilation operator. The effect of the string of  $\sigma^z$  gates is to introduce the required phase change of -1 if the parity of the set of qubits with index less than j is 1 (odd), and to do nothing if the parity is 0 (even), where the parity of a set of qubits is just the sum (mod 2) of the numbers that represent the states they are in.

We can then completely represent the fermionic creation and annihilation operators in terms of basic qubit gates as follows:

$$a_j^{\dagger} \equiv \mathbf{1}^{\otimes n-j-1} \otimes \hat{Q}^+ \otimes [\sigma^{z\otimes j}], \qquad a_j \equiv \mathbf{1}^{\otimes n-j-1} \otimes \hat{Q}^- \otimes [\sigma^{z\otimes j}].$$
 (11)

A more compact notation, of which we will make extensive use throughout this paper, is:

$$a_j^{\dagger} \equiv \hat{Q}_j^{+} \otimes Z_{j-1}^{\rightarrow} = \frac{1}{2} (X_j \otimes Z_{j-1}^{\rightarrow} - iY_j \otimes Z_{j-1}^{\rightarrow}); \tag{12}$$

$$a_j \equiv \hat{Q}_j^- \otimes Z_{j-1}^{\rightarrow} = \frac{1}{2} (X_j \otimes Z_{j-1}^{\rightarrow} + iY_j \otimes Z_{j-1}^{\rightarrow}), \tag{13}$$

where:

$$Z_i^{\to} \equiv \sigma_i^z \otimes \sigma_{i-1}^z \otimes \cdots \sigma_1^z \otimes \sigma_0^z, \tag{14}$$

and where it is assumed that any qubit not explicitly operated on is acted on by the identity. The operator  $Z_i^{\rightarrow}$  is a "parity operator" with eigenvalues  $\pm 1$ , corresponding to eigenstates for which the subset of bits with index less than or equal to i has even or odd parity, respectively.

The above correspondence, a mapping of interacting fermions to spins, is the Jordan-Wigner transformation [3, 10, 11, 31]. Jordan and Wigner introduced this transformation in 1928 in the context of 1D lattice models, but it has since been applied to quantum simulation of fermions [3, 9–11]. The problem with this method is that as a consequence of the non-locality of the parity operator  $Z_i^{\rightarrow}$ , the number of extra qubit operations required to simulate a single fermionic operator scales as O(n). In the next section we consider two alternatives to the occupation number basis that were suggested by Bravyi and Kitaev [13].

#### <span id="page-7-0"></span>III. ALTERNATIVES TO THE OCCUPATION NUMBER BASIS

#### A. The parity basis

The extra qubit operations required to simulate one fermionic operator when using the Jordan-Wigner method result from operating with  $\sigma^z$  on all qubits with index less than j.

This task could be accomplished by a single application of  $\sigma^z$  if instead of using qubit j to store  $f_j$ , we used qubit j to store the *parity* of all occupied orbitals up to orbital j [13]. That is, we could let qubit j store  $p_j = \sum_{s=0}^j f_s$ . (Throughout this paper, all sums of binary variables are taken mod 2). We follow [13] and call this encoding of fermionic states in qubit states the *parity* basis.

It is useful to define the transformations between bases we will consider in terms of maps between bit strings. For all the transformations we consider, which involve only sums of bits mod 2, it is possible to represent their action by matrices acting on the vector of bit values corresponding to a given logical basis state. For example, the occupation number basis state  $|f_7 \dots f_1 f_0\rangle$  is equivalent to the following vector:

$$(f_7, \dots, f_1, f_0)^T \tag{15}$$

In terms of these vectors the map to the parity basis is given by:

<span id="page-8-0"></span>
$$p_i = \sum_{j} [\pi_n]_{ij} \ f_j, \tag{16}$$

where n is the number of orbitals.  $\pi_n$  is the  $(n \times n)$  matrix defined below. Note that we index the matrix  $\pi_n$  from the lower right corner, for consistency with our orbital numbering scheme.

$$[\pi_n]_{ij} = \begin{cases} 1 & i < j \\ 0 & i \ge j \end{cases}, \quad \text{so that} \quad \pi_n = \begin{pmatrix} 1 & 1 & \cdots & 1 \\ 0 & 1 & \cdots & 1 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & 1 \end{pmatrix}$$
 (17)

For example, to change the occupation number basis state |10100111\rangle into its corresponding

parity basis state  $|10011101\rangle$ , we act with the matrix  $\pi_8$  on the appropriate bit string:

$$\begin{array}{cccccccccccccccccccccccccccccccccccc$$

With this understanding of the parity basis transformation, we can now derive the transformation that maps fermionic operators into operators in the parity basis. Since the parity of the set of orbitals with index less than j is what determines whether the action of  $a_j^{(\dagger)}$  introduces a phase of -1, operating with  $\sigma^z$  on qubit (j-1) alone will introduce the necessary phase to the corresponding qubit state in the parity basis.

However, unlike the Jordan-Wigner transformation, we cannot represent the creation or annihilation of a particle in orbital j by simply operating with  $\hat{Q}^{\pm}$  on qubit j, because in the parity basis qubit j does not store the occupation of orbital j, but the parity of all orbitals with index less than or equal to j. Thus whether we need to act with  $\hat{Q}^+$  or  $\hat{Q}^-$  on qubit j depends on qubit (j-1). If qubit (j-1) is in the state  $|0\rangle$ , then qubit j will accurately reflect the occupation of orbital j, and simulating  $a_j^{\dagger}$  will require acting on qubit j with  $\hat{Q}^+$ , as before. But if qubit (j-1) is in the state  $|1\rangle$ , then qubit j will have inverted parity compared to the occupation of orbital j, and we will instead need to act with  $\hat{Q}^-$  on qubit j to simulate  $a_j^{\dagger}$  (and *vice versa* for the annihilation operator).

The operator equivalent to  $\hat{Q}^{\pm}$  in the parity basis is therefore a two-qubit operator acting on qubits j and j-1:

$$\hat{\mathcal{P}}_{j}^{\pm} \equiv \hat{Q}_{j}^{\pm} \otimes |0\rangle\langle 0|_{j-1} - \hat{Q}_{j}^{\mp} \otimes |1\rangle\langle 1|_{j-1} = \frac{1}{2}(X_{j} \otimes Z_{j-1} \mp iY_{j}). \tag{19}$$

Additionally, creating or annihilating a particle in orbital j changes the parity data that must be stored by all qubits with index greater than j. Thus we must update the cumulative sums  $p_k$  for k > j by applying  $\sigma^x$  to all qubits  $|p_k\rangle$ , k > j [13]. The representations of the creation and annihilation operators in the parity basis are then:

$$a_j^{\dagger} \equiv X_{j+1}^{\leftarrow} \otimes \hat{\mathcal{P}}_j^{+} = \frac{1}{2} (X_{j+1}^{\leftarrow} \otimes X_j \otimes Z_{j-1} - i X_{j+1}^{\leftarrow} \otimes Y_j); \tag{20}$$

$$a_j \equiv X_{j+1}^{\leftarrow} \otimes \hat{\mathcal{P}}_j^- = \frac{1}{2} (X_{j+1}^{\leftarrow} \otimes X_j \otimes Z_{j-1} + i X_{j+1}^{\leftarrow} \otimes Y_j), \tag{21}$$

where:

$$X_i^{\leftarrow} \equiv \sigma_{n-1}^x \otimes \sigma_{n-2}^x \otimes \cdots \sigma_{i+1}^x \otimes \sigma_i^x. \tag{22}$$

This is the equivalent of the Jordan-Wigner transformation for the parity basis. The operator  $X_i^{\leftarrow}$  is the "update operator", which updates all qubits that store a partial sum including orbital (i-1) when the occupation number of that orbital changes. It is straightforward to verify that these mappings satisfy the fermionic anti-commutation relations. But to simulate fermionic operators in the parity basis, we have traded the trailing string of  $\sigma^z$  gates required by the Jordan-Wigner transformation for a leading string of  $\sigma^x$  gates whose length also scales as O(n), and we have not improved on the efficiency of the Jordan-Wigner simulation procedure. In the next section, we explore a third possibility.

## B. The Bravyi-Kitaev basis

Two kinds of information are required to simulate fermionic operators with qubits: the occupation of the target orbital, and the parity of the set of orbitals with index less than the target orbital. The previous two approaches are dual in the way that they store this information. With the occupation number basis and its associated Jordan-Wigner transformation, the occupation information is stored locally but the parity information is non-local, whereas in the parity basis method and its corresponding operator transformation, the parity information is stored locally but the occupation information is non-local.

The Bravyi-Kitaev basis is a middle ground. That is, it balances the locality of occupation and parity information for improved simulation efficiency. The general form of such a scheme must be to use qubits  $|b_j\rangle$  to store partial sums  $\sum_{s=k}^l f_s$  of occupation numbers according to some algorithm. For ease of explanation, in the exposition that follows, when we write that a qubit "stores a set of orbitals", what is meant is that the qubit stores the parity of the set of occupation numbers corresponding to that set of orbitals.

Bravyi and Kitaev's encoding has an elegant binary grouping structure [13]. In this scheme, qubits store the parity of a set of  $2^x$  orbitals, where  $x \geq 0$ . A qubit of index j

always stores orbital j. For even values of j, this is the only orbital that it stores, but for odd values of j, it also stores a certain set of adjacent orbitals with index less than j. Just as with the parity basis transformation, this encoding can be symbolized in a matrix β<sup>n</sup> that acts on bit string vectors corresponding to occupation number basis vectors of length n to transform them to the corresponding Bravyi-Kitaev-encoded bit strings (again, all additions done mod 2). In terms of these vectors, the map from the occupation number basis to the Bravyi-Kitaev basis is:

$$b_i = \sum_j [\beta_n]_{ij} f_j, \tag{23}$$

where the matrix β<sup>n</sup> is given in Figure [2](#page-11-0) below.

$$\beta_{1} = \beta_{1}^{-1} = \begin{bmatrix} 1 \end{bmatrix}$$

$$\beta_{2^{x+1}} = \begin{bmatrix} \beta_{2^{x}} & 0 \\ 0 & \beta_{2^{x}} \end{bmatrix} \quad \beta_{2^{x+1}}^{-1} = \begin{bmatrix} \beta_{2^{x}} & 0 \\ 0 & \beta_{2^{x}} \end{bmatrix}$$

<span id="page-11-0"></span>FIG. 2: The matrix β<sup>n</sup> that transforms occupation number basis vectors of length n into the Bravyi-Kitaev basis. β<sup>1</sup> is a (1 × 1) matrix with a single entry of 1. Subsequent iterations of the matrix that act on occupation number basis vectors of length 2<sup>x</sup> are constructed by taking 1⊗β<sup>2</sup> x−1 and then filling in the top row of the first quadrant of this matrix with 1's. β<sup>n</sup> for 2<sup>x</sup> < n < 2 x+1 is just the (n × n) segment of β<sup>2</sup> <sup>x</sup>+1 that includes b<sup>0</sup> through bn−1. The recursion pattern for the inverse transformation matrix is also shown. An entry of 1 in row b<sup>i</sup> , column f<sup>j</sup> means that b<sup>i</sup> is a partial sum including f<sup>j</sup> .

For example, to change the occupation number basis state |10100111i into its corresponding Bravyi-Kitaev basis state |10101101i, we act with the matrix β<sup>8</sup> on the appropriate bit string vector:

$$\begin{array}{cccccccccccccccccccccccccccccccccccc$$

This encoding strikes a balance between the occupation number basis and the parity basis methods. The parity of occupied orbitals up to orbital j is no longer stored in a single qubit, but the Bravyi-Kitaev encoding stores the parity of orbitals with index less than j in a few partial sums whose number scales as  $O(\log j) \leq O(\log n)$  [13]. Likewise, we no longer need to update all the qubits with index greater than j, but only those that store partial sums which include occupation number j. Each occupation number enters an additional partial sum only if the number of single particle states n is doubled, and so the overall cost of simulating a single fermionic operator with qubits scales as  $O(\log n)$  [13].

Given this encoding, we need to determine — for an arbitrary index j — which qubits in the Bravyi-Kitaev basis store the parity of all orbitals with index less than j, which qubits store a partial sum including orbital j, and which qubits determine whether qubit j has the same parity or inverted parity with respect to orbital j. These sets of indices will allow us to explicitly construct the fermionic creation and annihilation operators in the Bravyi-Kitaev basis. In the next section, we define these sets of qubit indices.

### <span id="page-12-0"></span>IV. SETS OF QUBITS RELEVANT TO THE BRAVYI-KITAEV BASIS

In this section we define the sets of qubits that are involved in the Bravyi-Kitaev transformation. These are the *parity set* (the qubits in the Bravyi-Kitaev basis that store the parity of all orbitals with index less than j), the *update set* (the qubits that store a partial sum including orbital j), and the *flip set* (the qubits that determine whether qubit j has the same parity as orbital j).

#### A. The parity set

For an arbitrary index j, we would like to know which set of qubits in the Bravyi-Kitaev basis tells us whether or not the state of the quantum computer needs to acquire a phase change of -1 under the action of a creation or annihilation operator acting on orbital j. The parity of this set of qubits has the same parity as the set of orbitals with index less than j, and so we will call this set of qubit indices the "parity set" of index j, or P(j). To determine the elements of P(j), we consider the transformation from the Bravyi-Kitaev basis to the parity basis. From equation (16) we know that  $p_i = \sum_j [\pi_n]_{ij} f_j$ . Given the inverse transformation matrix  $\beta_n^{-1}$ , it is also true that:

$$f_j = \sum_{k} [\beta_n^{-1}]_{jk} \ b_k, \tag{25}$$

and hence:

$$p_{i} = \sum_{j} [\pi_{n}]_{ij} \left( \sum_{k} [\beta_{n}^{-1}]_{jk} b_{k} \right)$$
 (26)

$$= \sum_{k} [\pi_n \beta_n^{-1}]_{ik} \ b_k \tag{27}$$

The matrix  $\pi_n \beta_n^{-1}$  is the transformation matrix from the Bravyi-Kitaev basis to the parity basis. Therefore, the nonzero entries to the right of the main diagonal in row i of the matrix  $\pi_n \beta_n^{-1}$  give the indices of qubits in the Bravyi-Kitaev basis that can be used to compute the cumulative parity of orbitals with index less than i. An entry of 1 in row i, column j of  $\pi_n \beta_n^{-1}$  (where j < i, i.e. to the right of the main diagonal by our numbering) indicates that  $j \in P(i)$ :

$$\pi_8 \beta_8^{-1} = \begin{pmatrix} 7 & 6 & 5 & 4 & 3 & 2 & 1 & 0 \\ 7 & 1 & 1 & 1 & 0 & 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 0 & 1 & 0 & 0 & 0 \\ 5 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 5 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 1 & 1 & 0 \\ 2 & 0 & 0 & 0 & 0 & 1 & 1 & 1 & 0 \\ 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 \end{pmatrix}$$
 which implies: 
$$\begin{cases} P(7) = \{6, 5, 3\} \\ P(6) = \{5, 3\} \\ P(5) = \{4, 3\} \\ P(4) = \{3\} \\ P(3) = \{2, 1\} \\ P(2) = \{1\} \\ P(1) = \{0\} \\ P(0) = \emptyset \end{cases}$$

## B. The update set

For arbitrary j, we define the set of qubits (other than qubit j) that must be updated when the occupation of orbital j changes. We call this set the "update set" of index j, or U(j). This is the set of qubits in the Bravyi-Kitaev basis that store a partial sum including orbital j. Any Bravyi-Kitaev qubit that stores a partial sum that includes occupation number j is in U(j). Since even indexed qubits store only the occupation of the corresponding orbital, update sets contain only odd indices. It is straightforward to determine the elements of U(j) from the transformation matrix  $\beta_n$  that maps bit strings in the occupation number basis to the Bravyi-Kitaev basis. The columns of this transformation matrix show which qubits in the Bravyi-Kitaev basis store a particular orbital, and so the nonzero entries in column j above the main diagonal determine the qubits other than qubit j that must be updated when the occupancy of orbital j changes. These are the elements of the update set.

$$\beta_{8} = \begin{cases} b_{7} & f_{6} & f_{5} & f_{4} & f_{3} & f_{2} & f_{1} & f_{0} \\ b_{7} & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ b_{6} & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ b_{5} & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 \\ b_{5} & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 1 & 1 & 1 & 1 \\ b_{2} & 0 & 0 & 0 & 0 & 1 & 1 & 1 & 1 \\ b_{1} & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 \\ b_{0} & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{cases}$$
 which implies: 
$$\begin{cases} U(7) = \emptyset \\ U(6) = \{7\} \\ U(5) = \{7\} \\ U(4) = \{5, 7\} \\ U(3) = \{7\} \\ U(2) = \{3, 7\} \\ U(1) = \{3, 7\} \\ U(0) = \{1, 3, 7\} \end{cases}$$

It should be clear that update sets depend on the size of the basis used. For example, if 16 basis functions were used instead of the 8 used in the example above, all the update sets other than U(7) would also include index 15.

#### C. The flip set

For arbitrary j, we need to know what set of Bravyi-Kitaev qubits determines whether qubit j has the same parity or inverted parity with respect to orbital j. We will call this

set of Bravyi-Kitaev qubits the "flip set" of j, or F(j), because this set is responsible for whether  $b_j$  has flipped parity with respect to  $f_j$ . This is the set that stores the parity of occupation numbers other than  $f_j$  in the sum  $b_j$ . Since even-indexed qubits store only the orbital with the same index, the flip set of even indices is always the empty set. One can determine the elements of F(j) by looking at the inverse transformation matrix  $\beta_n^{-1}$  that maps bit strings in the Bravyi-Kitaev basis to the occupation number basis. The columns with nonzero entries to the right of the main diagonal in row i of this inverse transformation matrix give the indices of the Bravyi-Kitaev qubits that together store the same set of orbitals as is stored by  $|b_i\rangle$ . These are the elements of the flip set.

$$\beta_{8}^{-1} = \begin{cases} f_{7} & f_{6} & f_{5} & f_{4} & f_{3} & f_{2} & f_{1} & f_{0} \\ f_{6} & f_{7} & f_{8} & f_{7} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{7} & f_{8} & f_{7} & f_{8} & f_{8} & f_{8} \\ f_{7} & f_{8} & f_{7} & f_{8} & f_{8} \\ f_{7} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8} & f_{8} \\ f_{8} & f_{8}$$

With these sets defined, we can derive the mapping from fermionic operators to qubit operators that is the equivalent of the Jordan-Wigner transformation in the Bravyi-Kitaev basis.

#### <span id="page-15-0"></span>V. THE BRAVYI-KITAEV TRANSFORMATION

In this section we will give an explicit prescription, in terms of Pauli matrices, for representing the creation and annihilation operators that act on the Bravyi-Kitaev basis states. Operating in this basis requires that we find the analogues to the qubit creation and annihilation operators ( $\hat{Q}^{\pm}$  in the occupation number basis,  $\hat{\mathcal{P}}^{\pm}$  in the parity basis) as well as the parity operator,  $Z_i^{\rightarrow}$ , and the update operator,  $X_i^{\leftarrow}$ , in the Bravyi-Kitaev basis. We will first define some notation.

For our purposes it is the parity of subsets of orbitals or qubits that matters, not the individual occupation numbers or states of the qubits in the set. Thus, it is useful to define operators that project onto the subspace of the Hilbert space of the entire computer for which the subset of qubits with indices in S has the parity selected for by the operator (even for  $\hat{E}_S$ , odd for  $\hat{O}_S$ ). We can express these operators in terms of Pauli matrices as follows:

$$\hat{E}_S = \frac{1}{2}(\mathbf{1} + Z_S), \qquad \hat{O}_S = \frac{1}{2}(\mathbf{1} - Z_S),$$
 (31)

where  $Z_S$  is shorthand for the  $\sigma^z$  gate applied to all qubits in S. With this notation established, we will next write equations for the qubit operators in the Bravyi-Kitaev basis that represent creation and annihilation operators acting on orbital j. To begin we will consider the case for which j is even, because this will allow us to build intuition for the more difficult case for which j is odd.

## A. Representing $a_j^{(\dagger)}$ in the Bravyi-Kitaev basis for j even

In the case that j is even, we should act with  $\hat{Q}^{\pm}$  on qubit j, just as for the Jordan-Wigner transformation, because the Bravyi-Kitaev encoding stores orbitals with  $j=0 \pmod{2}$  in the qubit with the same index. There are then two additional tasks that dictate how to represent the fermionic operators in the Bravyi-Kitaev basis: determining the parity of occupied orbitals with index less than j, and updating qubits with index greater than j that store a partial sum that includes occupation number j.

The parity of the set of qubits in P(j) is equal to that of the set of orbitals with index less than j. By analogy with the Jordan-Wigner transformation, we act with  $\sigma^z$  on all qubits with indices in P(j), that is, we apply the operator  $Z_{P(j)}$ . The number of qubits in P(j) scales as  $O(\log j) \leq O(\log n)$  [13].

Secondly, by analogy with the parity basis method, we also act with  $\sigma^x$  on all qubits in the appropriate U(j); that is, we apply the operator  $X_{U(j)}$ . This has the effect of updating all the qubits that store a set of orbitals including orbital j. The size of U(j) also scales like  $O(\log n)$  [13]. To summarize: to represent  $a_j^{\dagger}$  or  $a_j$  in the Bravyi-Kitaev basis, for j even, we act with  $\sigma^z$  on all qubits in P(j),  $\hat{Q}^{\pm}$  on qubit j, and with  $\sigma^x$  on all qubits in U(j):

$$a_i^{\dagger} \equiv X_{U(j)} \otimes \hat{Q}_i^{\dagger} \otimes Z_{P(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} - i X_{U(j)} \otimes Y_j \otimes Z_{P(j)}); \tag{32}$$

$$a_j \equiv X_{U(j)} \otimes \hat{Q}_j^- \otimes Z_{P(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} + iX_{U(j)} \otimes Y_j \otimes Z_{P(j)}). \tag{33}$$

In the next section, we will consider the case for which j is odd.

## B. Representing $a_j^{(\dagger)}$ in the Bravyi-Kitaev basis for j odd

To represent the creation or annihilation of a particle in orbital j in the Bravyi-Kitaev basis, for j even, we could simply act with  $\hat{Q}^{\pm}$  on qubit j because that qubit stores only the occupation of orbital j. For j odd, qubit j stores a partial sum of occupation numbers of orbitals including, but not limited to, orbital j. Thus, in this case the state of Bravyi-Kitaev qubit j is either equal to the occupation of orbital j (if the parity of the other orbitals that it stores is even), or opposite to that of orbital j (if the parity of the other orbitals that it stores is 1). Thus, whether representing the creation or annihilation of a particle in orbital j requires that we act with  $\hat{Q}^+$  or  $\hat{Q}^-$  on qubit j in the Bravyi-Kitaev basis depends on the parity of all occupation numbers other than  $f_j$  that are included in the partial sum  $b_j$  — i.e. the parity of the flip set of index j. If the parity of the set of qubits with indices in F(j) is even, then the creation or annihilation of a particle in orbital j requires acting with  $\hat{Q}^+$  or  $\hat{Q}^-$ , respectively, as usual. But if the parity of this set of qubits is odd, then the creation of a particle requires acting with  $\hat{Q}^+$ . The Bravyi-Kitaev analogues to the qubit creation and annihilation operators are therefore:

$$\hat{\Pi}_j^{\pm} \equiv \hat{Q}_j^{\pm} \otimes \hat{E}_{F(j)} - \hat{Q}_j^{\mp} \otimes \hat{O}_{F(j)} = \frac{1}{2} (X_j \otimes Z_{F(j)} \mp iY_j). \tag{34}$$

The updating procedure in this case in which j is odd works in exactly the same way as it does in the case that j is even. In applying the parity operator, however, we need only consider the qubits that are in P(j) but not in F(j), because the relative sign in the  $\hat{\Pi}_j^{\pm}$  operator implicitly calculates the parity of the subset of the parity set that is also in the flip set of index j. It is convenient to therefore introduce the new "remainder set":

$$R(j) \equiv P(j) \setminus F(j). \tag{35}$$

Thus, the fermionic creation and annihilation operators acting on orbital j for j odd are represented in the Bravyi-Kitaev basis as follows:

$$a_j^{\dagger} \equiv X_{U(j)} \otimes \hat{\Pi}_j^+ \otimes Z_{R(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} - i X_{U(j)} \otimes Y_j \otimes Z_{R(j)}); \tag{36}$$

$$a_j \equiv X_{U(j)} \otimes \hat{\Pi}_j^- \otimes Z_{R(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} + i X_{U(j)} \otimes Y_j \otimes Z_{R(j)}). \tag{37}$$

It is evident by inspection that the only difference in the algebraic form of the operators between the even- and odd-indexed cases is that the second term involves  $Z_{P(j)}$  for the even case, but  $Z_{R(j)}$  for the odd case. Therefore we define:

$$\rho(j) \equiv \begin{cases} P(j) & \text{if } j \text{ is even;} \\ R(j) & \text{if } j \text{ is odd.} \end{cases}$$
 (38)

Now the fermionic creation and annihilation operators acting on arbitrary j are represented in the Bravyi-Kitaev basis as:

$$a_j^{\dagger} \equiv X_{U(j)} \otimes \hat{\Pi}_j^+ \otimes Z_{R(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} - iX_{U(j)} \otimes Y_j \otimes Z_{\rho(j)}); \tag{39}$$

$$a_j \equiv X_{U(j)} \otimes \hat{\Pi}_j^- \otimes Z_{R(j)} = \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} + i X_{U(j)} \otimes Y_j \otimes Z_{\rho(j)}). \tag{40}$$

These are useful basic results, but the operators that appear in the molecular electronic Hamiltonian are actually products of these creation and annihilation operators. In the next section, we derive general expressions for products of these second-quantized operators.

# <span id="page-18-0"></span>VI. PAULI REPRESENTATIONS OF SECOND-QUANTIZED OPERATORS IN THE BRAVYI-KITAEV BASIS

In this Section we derive simplified algebraic expressions for classes of Hermitian secondquantized fermionic operators in the Bravyi-Kitaev basis. The five relevant classes of operators are summarized in Table I. We will give complete compact algebraic expressions for only the number operators and the Coulomb and exchange operators. It is not possible to give the algebraic form for the remaining three classes of operators without considering an impractical number of sub-cases, so we opt to give general expressions for products of the form  $a_i^{\dagger}a_j$ , and show how to use these results to generate algebraic expressions for the remaining classes of operators.

## <span id="page-18-1"></span>A. Number operators: $h_{ii} a_i^{\dagger} a_i$

The number operators are of the form  $h_{ii}$   $a_i^{\dagger}a_i$  and have eigenvalues corresponding to the occupation number of orbital i. We would like to find a simplified expression for this class of operators in the Bravyi-Kitaev basis.

| Operator                   | Second quantized form                                                                    |
|----------------------------|------------------------------------------------------------------------------------------|
| Number operator            | †<br>hii<br>a<br>ai<br>i                                                                 |
| Coulomb/exchange operators | †<br>†<br>hijji<br>a<br>a<br>ajai<br>i<br>j                                              |
| Excitation operator        | †<br>†<br>hij<br>(a<br>aj<br>+<br>a<br>ai)<br>i<br>j                                     |
| Number-excitation operator | †<br>†<br>†<br>†<br>hijjk<br>(a<br>a<br>ajak<br>+<br>a<br>a<br>ajai)<br>i<br>j<br>j<br>k |
| Double excitation operator | †<br>†<br>†<br>†<br>hijkl<br>(a<br>a<br>akal<br>+<br>a<br>a<br>ajai)<br>i<br>j<br>l<br>k |

<span id="page-19-0"></span>TABLE I: The five classes of Hermitian second quantized operators that appear in electronic Hamiltonians. In general the overlap integrals hij and hijkl may be complex.

Given the results of Section [V,](#page-15-0) we can write the following:

$$a_i^{\dagger} a_i = \frac{1}{2} (X_{U(i)} \otimes X_i \otimes Z_{P(i)} - i X_{U(i)} \otimes Y_i \otimes Z_{\rho(i)})$$

$$\times \frac{1}{2} (X_{U(i)} \otimes X_i \otimes Z_{P(i)} + i X_{U(i)} \otimes Y_i \otimes Z_{\rho(i)}).$$

$$(41)$$

Given that σ xσ <sup>x</sup> = σ yσ <sup>y</sup> = σ zσ <sup>z</sup> = 1, it follows that (XS) <sup>2</sup> = (YS) <sup>2</sup> = (ZS) <sup>2</sup> = 1. We are left with:

$$a_i^{\dagger} a_i = \frac{1}{4} [\mathbf{1} + i(X_i Y_i) \otimes Z_{P(i) \setminus \rho(i)} - i(Y_i X_i) \otimes Z_{P(i) \setminus \rho(i)} + \mathbf{1}]$$

$$\tag{42}$$

$$= \frac{1}{2} (\mathbf{1} - Z_i \otimes Z_{P(i) \setminus \rho(i)}). \tag{43}$$

Now, when i is even, ρ(i) = P(i), and so P(i) \ ρ(i) = ∅. When i is odd, ρ(i) = R(i), and so P(i) \ ρ(i) = F(i). Conveniently, F(i) = ∅ for i even, so if we define the following:

$$\underline{F(i)} \equiv F(i) \cup \{i\},\tag{44}$$

then we can represent the number operators for arbitrary i (even or odd) as follows:

$$a_i^{\dagger} a_i = \frac{1}{2} (\mathbf{1} - Z_{\underline{F(i)}}). \tag{45}$$

In the next section we consider the Coulomb and exchange operators.

#### B. Coulomb and exchange operators: hijji a † i a † j aja<sup>i</sup>

The Coulomb operators are of the form a † ia † <sup>j</sup>aja<sup>i</sup> , while the exchange operators are of the form a † ia † <sup>j</sup>aia<sup>j</sup> = −a † ia † <sup>j</sup>aja<sup>i</sup> . Since these two kinds of operators can be grouped together algebraically, we consider them as one case. The fermionic anti commutation relations ensure that a † ia † <sup>j</sup>aja<sup>i</sup> = −a † ia † <sup>j</sup>aia<sup>j</sup> = (a † <sup>i</sup>ai)(a † <sup>j</sup>a<sup>j</sup> ). Thus, we can consider the Coulomb and exchange operators as a product of two number operators. With the result from Section [VI A,](#page-18-1) we can write the following:

$$a_i^{\dagger} a_j^{\dagger} a_j a_i = \frac{1}{2} (\mathbf{1} - Z_{\underline{F(i)}}) \times \frac{1}{2} (\mathbf{1} - Z_{\underline{F(j)}})$$
 (46)

$$= \frac{1}{4}(\mathbf{1} - Z_{F(i)} - Z_{F(j)} + Z_{F(i)}Z_{F(j)}). \tag{47}$$

Any overlap between supp(ZF(i)) and supp(ZF(j)), where supp(Oˆ) is the support of the operator Oˆ, i.e. those tensor factors on which it acts nontrivially, will result in the local product σ zσ <sup>z</sup> = 1. Thus, we only actually need to act with σ <sup>z</sup> on the union of F(i) and F(j) minus their intersection, i.e. the symmetric difference of these two sets. Thus we define the following notation:

$$\underline{F_{ij}} \equiv \underline{F(i)} \triangle \underline{F(j)} = (\underline{F(i)} \cup \underline{F(j)}) \setminus (\underline{F(i)} \cap \underline{F(j)}). \tag{48}$$

We can then give the algebraic expression for the Coulomb and exchange operators:

$$a_i^{\dagger} a_j^{\dagger} a_j a_i = \frac{1}{4} (\mathbf{1} - Z_{\underline{F(i)}} - Z_{\underline{F(j)}} + Z_{\underline{F_{ij}}}). \tag{49}$$

In the next section we consider general products of the form a † iaj .

#### C. Products of the form a † i aj

We can assume without loss of generality that i < j. The algebraic form for products of this kind depends on the parity of the indices. There are four cases and we will work through the first case in detail, and simply present the results for the other cases.

Using the result of Section [V,](#page-15-0) we obtain the following when i and j are even:

<span id="page-20-0"></span>
$$a_i^{\dagger} a_j = \frac{1}{2} (X_{U(i)} \otimes X_i \otimes Z_{P(i)} - i X_{U(i)} \otimes Y_i \otimes Z_{P(i)})$$

$$\times \frac{1}{2} (X_{U(j)} \otimes X_j \otimes Z_{P(j)} + i X_{U(j)} \otimes Y_j \otimes Z_{P(j)}).$$

$$(50)$$

For each of the four terms resulting from multiplying out the operators in equation [\(50\)](#page-20-0) above, we must consider what products of local qubit operators can result. There are three potential sources of local qubit operator products: overlap between the update set of qubit i and the update set of qubit j, overlap between the update set of qubit i and the parity set of qubit j, and overlap between the parity set of qubit i and the parity set of qubit j. Any overlap between the update sets of qubits i and j will result in the local product  $\sigma^x \sigma^x = 1$ ; any overlap between the update set of qubit i and parity set of qubit j will result in the local product  $\pm i\sigma^y$ ; and any overlap in the parity sets of qubits i and j will result in the local product  $\sigma^z \sigma^z = 1$ . Thus we define the following sets:

$$U_{ij} \equiv U(i) \triangle U(j), \qquad \alpha_{ij} \equiv U(i) \cap P(j), \qquad P_{ij}^{0} \equiv P(i) \triangle P(j).$$
 (51)

Note that in the case that i and j are even, we do not need to consider the possibility that  $j \in U(i)$  because U(i) contains only odd elements. Similarly, we do not need to consider the possibility that  $i \in P(j)$ , because P(j) for j even contains only odd elements.

As an example, we will show how to use the sets defined above to simplify the term  $(X_{U(i)} \otimes X_i \otimes Z_{P(i)})(X_{U(j)} \otimes X_j \otimes Z_{P(j)})$ . For this term, we need only apply  $\sigma^x$  to the set of qubits  $U_{ij} \setminus \alpha_{ij} \cup \{i, j\}$ ,  $\sigma^y$  to the qubit with index in  $\alpha_{ij}$  (which set in general has at most 1 element, and in the case that i and j are even always contains 1 element), and  $\sigma^z$  to the qubits in the set  $P_{ij}^0 \setminus \alpha_{ij}$ . Thus, this term simplifies to:

$$(X_{U(i)} \otimes X_i \otimes Z_{P(i)})(X_{U(j)} \otimes X_j \otimes Z_{P(j)}) = -i \ X_{U_{ij} \setminus \alpha_{ij} \cup \{i,j\}} Y_{\alpha_{ij}} Z_{P_{ij}^0 \setminus \alpha_{ij}}.$$
 (52)

Using the same reasoning for the other terms, we arrive at the following result:

$$a_i^{\dagger} a_j = \frac{1}{4} X_{U_{ij} \setminus \alpha_{ij}} Y_{\alpha_{ij}} Z_{P_{ij}^0 \setminus \alpha_{ij}} [Y_j X_i - X_j Y_i - i(X_j X_i + Y_j Y_i)]. \tag{53}$$

This is our result for the case that i and j are even. The algebraic expressions for the other cases can be derived in the same manner, with the added complication that the expression for the product  $a_i^{\dagger}a_j$  varies, depending on if  $i \in P(j)$  and/or  $j \in U(i)$ . This complication results in a proliferation of sub-cases: two for the case that i is odd and j is even, three for the case that i is even and j is odd, and four for the case that i and j are odd. The only additional sets we need to define are the analogs of  $P_{ij}^0$  for when one or both of the indices are odd:

$$P_{ij}^1 \equiv P(i) \triangle R(j), \qquad P_{ij}^2 \equiv R(i) \triangle P(j), \qquad P_{ij}^3 \equiv R(i) \triangle R(j).$$
 (54)

The results for all cases are summarized below in Table II. In the following sub-sections we show how to use the contents of Table II to generate algebraic expressions for the excitation operators, the number-excitation operators, and the double-excitation operators.

## D. Excitation operators: $h_{ij} \, \left( a_i^\dagger a_j + a_j^\dagger a_i \right)$

Providing for the possibility that the integral  $h_{ij}$  is complex, we can write:

$$h_{ij} (a_i^{\dagger} a_j + a_j^{\dagger} a_i) = \Re\{h_{ij}\}(a_i^{\dagger} a_j + a_j^{\dagger} a_i) + \Im\{h_{ij}\}(a_i^{\dagger} a_j - a_j^{\dagger} a_i).$$
 (55)

Applying this to the case when i and j are even, we find the following:

$$h_{ij} (a_i^{\dagger} a_j + a_j^{\dagger} a_i) = \frac{1}{2} X_{U_{ij} \setminus \alpha_{ij}} Y_{\alpha_{ij}} Z_{P_{ij}^0 \setminus \alpha_{ij}} [ \Re\{h_{ij}\} (Y_j X_i - X_j Y_i) + \Im\{h_{ij}\} (X_j X_i + Y_j Y_i)].$$
 (56)

Similar expressions for other cases are easily generated by taking the appropriate form of  $a_i^{\dagger}a_j$  from Table II.

**E.** Number-excitation operators: 
$$h_{ijjk}$$
  $(a_i^{\dagger}a_j^{\dagger}a_ja_k + a_k^{\dagger}a_j^{\dagger}a_ja_i)$ 

Due to the fermionic anti-commutation relations, the following is true:

$$a_i^{\dagger} a_j^{\dagger} a_j a_k + a_k^{\dagger} a_j^{\dagger} a_j a_i = (a_i^{\dagger} a_k + a_k^{\dagger} a_i)(a_j^{\dagger} a_j). \tag{57}$$

We see that this is simply a product of an excitation operator and a number operator. We have previously given algebraic expressions for both of these classes of operators, so it is not difficult to combine them for an expression for the number-excitation operators. Let us consider the example when i and k are even. Then we have the following:

$$h_{ijjk} (a_i^{\dagger} a_k + a_k^{\dagger} a_i) a_j^{\dagger} a_j = \frac{1}{2} X_{U_{ik} \setminus \alpha_{ik}} Y_{\alpha_{ik}} Z_{P_{ik}^0 \setminus \alpha_{ik}} [\Re\{h_{ijjk}\} (Y_k X_i - X_k Y_i)$$

$$+ \Im\{h_{ijjk}\} (X_k X_i + Y_k Y_i)] \times \frac{1}{2} (\mathbf{1} - Z_{F(j)}).$$
(58)

To simplify, all we need to consider is the intersection between  $\underline{F(j)}$  and the support of  $(a_i^{\dagger}a_k + a_k^{\dagger}a_i)$ . In this case the support of the excitation operator is  $U_{ik} \cup \alpha_{ik} \cup P_{ik}^0 \cup \{i, k\}$ . The form of the simplification will vary depending on these sets, but the process of reducing local operator products by exploiting the relationship between the three Pauli matrices is unchanged. In the cases when i and k are not both even, all that changes is the form of the excitation operator from Table II that must be used.

#### F. Double-excitation operators: hijkl (a † i a † j aka<sup>l</sup> + a † l a † k ajai)

The double-excitation operators involve four distinct indices, and are obviously the most algebraically complicated class of operators we are considering. The impractical number of sub-cases depending on the specific combination of indices i, j, k, l means that we only outline the procedure for deriving algebraic expressions for this class of operators. The fermionic commutation relations ensure that the following is true:

$$(a_i^{\dagger} a_j^{\dagger} a_k a_l + a_l^{\dagger} a_k^{\dagger} a_j a_i) = (a_i^{\dagger} a_l)(a_j^{\dagger} a_k) + (a_l^{\dagger} a_i)(a_k^{\dagger} a_j). \tag{59}$$

Allowing for the integral hijkl to be complex, we can write:

$$h_{ijkl} \left( a_i^{\dagger} a_j^{\dagger} a_k a_l + a_l^{\dagger} a_k^{\dagger} a_j a_i \right) = \left[ \Re\{h_{ijkl}\} \left( a_i^{\dagger} a_l a_j^{\dagger} a_k + a_l^{\dagger} a_i a_k^{\dagger} a_j \right) \right.$$

$$\left. + \Im\{h_{ijkl}\} \left( a_i^{\dagger} a_l a_j^{\dagger} a_k - a_l^{\dagger} a_i a_k^{\dagger} a_j \right) \right].$$

$$\left. (60)$$

Since (a † <sup>i</sup>ala † <sup>j</sup>ak) † = a † <sup>l</sup> aia † <sup>k</sup>a<sup>j</sup> , we can simply consider the algebraic expression for the product of two operators of the form a † <sup>i</sup>a<sup>j</sup> as given in Table [II,](#page-24-0) and then add or subtract it to its Hermitian conjugate. Each of the operators a † <sup>i</sup>a<sup>l</sup> and a † <sup>j</sup>a<sup>k</sup> will fit into one of the ten cases presented in Table [II.](#page-24-0) In multiplying out the algebraic expressions for these two products, what is important is the set {supp(a † <sup>i</sup>al) ∩ supp(a † <sup>j</sup>ak)}. Any qubits in this set will have a product of local operators acting on it which must be simplified.

## <span id="page-23-0"></span>VII. THE MOLECULAR ELECTRONIC HAMILTONIAN FOR THE HYDROGEN MOLECULE IN THE BRAVYI-KITAEV BASIS

The molecular electronic Hamiltonian [\(6\)](#page-5-0) may be divided into one and two-electron terms:

$$\hat{H} = \sum_{i,j} h_{ij} a_i^{\dagger} a_j + \frac{1}{2} \sum_{i,j,k,l} h_{ijkl} a_i^{\dagger} a_j^{\dagger} a_k a_l = \hat{H}^{(1)} + \hat{H}^{(2)}.$$
 (61)

We treat molecular hydrogen in a minimal basis, so the sums above run over the four spin orbitals defined above. These spin orbitals will be indexed 0 through 3, as will be the fermionic creation and annihilation operators. We derive the simplified expressions for the individual terms of this Hamiltonian in the Bravyi-Kitaev basis. The overlap integrals hij and hijkl for 0 ≤ i ≤ 3 are given in Table [III.](#page-25-0) These are the same as were used in [\[11\]](#page-36-6) and were calculated using a restricted Hartree-Fock calculation in the PyQuante quantum chemistry package [\[32\]](#page-37-4). With these integrals and the algebraic expressions for second quantized

| Index parity           |                | Conditions     |         | †<br>Algebraic expression for<br>a<br>aj<br>i                                                                                                  |  |
|------------------------|----------------|----------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------|--|
|                        | i<br>∈<br>P(j) | j<br>∈<br>U(i) | αij<br> |                                                                                                                                                |  |
| i, j<br>even           | No             | No             | 1       | 1<br>4XUij\αij<br>Yαij<br>ZP<br>[YjXi<br>−<br>XjYi<br>−<br>i(XjXi<br>+<br>YjYi)]<br>0<br>ij\αij                                                |  |
|                        | No             | No             | 1       | 1<br>4XUij\αij<br>Yαij<br>Zαij<br>[(YjXi<br>−<br>iXjXi)<br>ZP<br>−<br>(XjYi<br>+<br>iYjYi)<br>ZP<br>]<br>0<br>2<br>ij<br>ij                    |  |
| i<br>odd,<br>j<br>even |                |                |         |                                                                                                                                                |  |
|                        | Yes            | No             | 0       | 1<br>4XUij<br>Zi<br>[(YjYi<br>−<br>iXjXiYi)<br>ZP<br>+ (XjXi<br>+<br>iYjXi)<br>ZP<br>]<br>0<br>2<br>ij<br>ij                                   |  |
|                        | No             | No             | 1       | 1<br>4XUij\αij<br>Yαij<br>Zαij<br>[−(XjYi<br>+<br>iXjXi)<br>ZP<br>+ (YjXi<br>−<br>iYjYi)<br>ZP<br>]<br>0<br>1<br>ij<br>ij                      |  |
| i<br>even,<br>j<br>odd | No             | Yes            | 1       | 1<br>4XUij\j<br>[−Xαij<br>(Yi<br>−<br>iXi)<br>Yαij<br>ZP<br>ij\αij + (iYi<br>−<br>Xi)<br>ZP<br>]<br>0<br>1<br>ij∪j                             |  |
|                        | Yes            | Yes            | 0       | 1<br>4XUij\j<br>[(Xi<br>−<br>iYi) + (iYi<br>−<br>Xi)<br>ZP<br>]<br>1<br>ij∪j                                                                   |  |
| i, j<br>odd            | No             | No             | 1       | 1<br>4XUij\αij<br>YαijZαij<br>[−iXjXiZP<br>+<br>YjXiZP<br>−<br>XjYiZP<br>−<br>iYjYiZP<br>]<br>0<br>1<br>2<br>3<br>ij<br>ij<br>ij<br>ij         |  |
|                        | Yes            | No             | 0       | 1<br>4XUij<br>Zi<br>[(−iXjYiZP<br>+<br>YjYiZP<br>) +<br>XjXiZP<br>+<br>iYjXiZP<br>]<br>0<br>1<br>2<br>3<br>ij<br>ij<br>ij<br>ij                |  |
|                        | No             | Yes            | 1       | 1<br>4XUij\j<br>[−Xαij<br>(YiZP<br>+<br>iXiZP<br>)YαijZαij<br>−<br>(XiZP<br>−<br>iYiZP<br>)Zj<br>]<br>2<br>0<br>1<br>3<br>ij<br>ij<br>ij<br>ij |  |
|                        | Yes            | Yes            | 0       | 1<br>4XUij\j<br>[Zi(−iYiZP<br>+<br>XiZP<br>) +<br>Zj<br>(−XiZP<br>+<br>iYiZP<br>)]<br>0<br>2<br>1<br>3<br>ij<br>ij<br>ij<br>ij                 |  |

<span id="page-24-0"></span>TABLE II: The algebraic expressions for general products of the form a † i a<sup>j</sup> in the Bravyi-Kitaev basis. These expressions vary in form depending on the parity of the indices i and j, as well as on the overlaps between the parity and update sets of the indices. The notation O<sup>S</sup> is shorthand to indicate that the operator O does not operate on the qubits in the set S (i.e. Z<sup>P</sup> 0 ij Z<sup>j</sup> = Z<sup>P</sup> 0 ij\j ).

operators given in Section [VI,](#page-18-0) we can express the molecular electronic Hamiltonian for H<sup>2</sup> as a sum of products of Pauli matrices. In the next two subsections we consider the oneand two-electron Hamiltonians separately.

| Integrals                                                                                               | Value (a.u.) |
|---------------------------------------------------------------------------------------------------------|--------------|
| h00<br>=<br>h11                                                                                         | −1.252477    |
| h22<br>=<br>h33                                                                                         | −0.475934    |
| h0110<br>=<br>h1001                                                                                     | 0.674493     |
| h2332<br>=<br>h3223                                                                                     | 0.697397     |
| h0220<br>=<br>h0330<br>=<br>h1221<br>=<br>h1331<br>=<br>h2002<br>=<br>h3003<br>=<br>h2112<br>=<br>h3113 | 0.663472     |
| h0202<br>=<br>h1313<br>=<br>h2130<br>=<br>h2310<br>=<br>h0312<br>=<br>h0132                             | 0.181287     |

<span id="page-25-0"></span>TABLE III: The overlap integrals for molecular hydrogen in a minimal basis. The integrals were obtained through a restricted Hartree-Fock calculation in the PyQuante quantum chemistry package at an internuclear separation of 1.401000 atomic units (7.414 × 10−<sup>11</sup> m).

## <span id="page-25-1"></span>A. The Bravyi-Kitaev Pauli representation of Hˆ (1)

We can write the one-electron terms in the Hamiltonian as:

$$\hat{H}^{(1)} = h_{00}a_0^{\dagger}a_0 + h_{11}a_1^{\dagger}a_1 + h_{22}a_2^{\dagger}a_2 + h_{33}a_3^{\dagger}a_3.$$
 (62)

Using the expressions for number operators derived in Section [V,](#page-15-0) we know that in the Bravyi-Kitaev basis, these operators are:

$$a_0^{\dagger} a_0 = \frac{1}{2} (\mathbf{1} - \sigma_0^z);$$
 (63)

$$a_1^{\dagger} a_1 = \frac{1}{2} (\mathbf{1} - \sigma_1^z \sigma_0^z);$$
 (64)

$$a_2^{\dagger} a_2 = \frac{1}{2} (\mathbf{1} - \sigma_2^z);$$
 (65)

$$a_3^{\dagger} a_3 = \frac{1}{2} (\mathbf{1} - \sigma_3^z \sigma_2^z \sigma_1^z). \tag{66}$$

We now proceed to the simulation of Hˆ (2) .

## B. The Bravyi-Kitaev Pauli representation of Hˆ (2)

Following the work of Whitfield et al. [\[11\]](#page-36-6), Hˆ (2) simplifies to the following expression for molecular hydrogen in a minimal basis:

$$\hat{H}^{(2)} = h_{0110} a_0^{\dagger} a_1^{\dagger} a_1 a_0 + h_{2332} a_2^{\dagger} a_3^{\dagger} a_3 a_2 + h_{0330} a_0^{\dagger} a_3^{\dagger} a_3 a_0 + h_{1221} a_1^{\dagger} a_2^{\dagger} a_2 a_1$$
 (67)

$$+(h_{0220} - h_{0202})a_0^{\dagger}a_2^{\dagger}a_2a_0 + (h_{1331} - h_{1313}) \quad a_1^{\dagger}a_3^{\dagger}a_3a_1 + h_{0132}(a_0^{\dagger}a_1^{\dagger}a_3a_2 + a_2^{\dagger}a_3^{\dagger}a_1a_0) + h_{0312}(a_0^{\dagger}a_3^{\dagger}a_1a_2 + a_2^{\dagger}a_1^{\dagger}a_3a_0).$$

This term in the Hamiltonian is made up of six Coulomb/exchange operators and two double-excitation operators. Using Section VI, it is easy to give algebraic expressions for the Coulomb and exchange operators:

$$a_0^{\dagger} a_1^{\dagger} a_1 a_0 = \frac{1}{4} (\mathbf{1} - \sigma_0^z - \sigma_1^z \sigma_0^z + \sigma_1^z); \tag{68}$$

$$a_2^{\dagger} a_3^{\dagger} a_3 a_2 = \frac{1}{4} (\mathbf{1} - \sigma_2^z - \sigma_3^z \sigma_2^z \sigma_1^z + \sigma_3^z \sigma_1^z); \tag{69}$$

$$a_0^{\dagger} a_3^{\dagger} a_3 a_0 = \frac{1}{4} (\mathbf{1} - \sigma_0^z - \sigma_3^z \sigma_2^z \sigma_1^z + \sigma_3^z \sigma_2^z \sigma_1^z \sigma_0^z); \tag{70}$$

$$a_1^{\dagger} a_2^{\dagger} a_2 a_1 = \frac{1}{4} (\mathbf{1} - \sigma_2^z - \sigma_1^z \sigma_0^z + \sigma_2^z \sigma_1^z \sigma_0^z); \tag{71}$$

$$a_0^{\dagger} a_2^{\dagger} a_2 a_0 = \frac{1}{4} (\mathbf{1} - \sigma_2^z - \sigma_0^z + \sigma_2^z \sigma_0^z);$$
 (72)

$$a_1^{\dagger} a_3^{\dagger} a_3 a_1 = \frac{1}{4} (\mathbf{1} - \sigma_3^z \sigma_2^z \sigma_1^z - \sigma_1^z \sigma_0^z + \sigma_3^z \sigma_2^z \sigma_0^z). \tag{73}$$

The two double-excitation operators are somewhat more complicated. As an example, we will derive the Pauli representation of  $h_{0312}(a_0^{\dagger}a_3^{\dagger}a_1a_2 + a_2^{\dagger}a_1^{\dagger}a_3a_0)$ . Following in Section VI, we consider  $a_0^{\dagger}a_3^{\dagger}a_1a_2$  as  $(a_0^{\dagger}a_2)(a_3^{\dagger}a_1)$ , a product of two operators of the form  $a_i^{\dagger}a_j$ . The term  $a_0^{\dagger}a_2$  is of the type when i and j are both even, while the term  $a_1^{\dagger}a_3$  is of the type when i and j are odd, and  $i \in P(j)$ ,  $j \in U(i)$ , and  $|\alpha_{ij}| = 0$ . Using the appropriate expressions from Table II, we find the following:

$$a_0^{\dagger} a_2 = \frac{1}{4} (\sigma_2^y \sigma_1^y \sigma_0^x - \sigma_2^x \sigma_1^y \sigma_0^y - i \sigma_2^x \sigma_1^y \sigma_0^x - i \sigma_2^y \sigma_1^y \sigma_0^y); \tag{74}$$

$$a_1^{\dagger} a_3 = \frac{1}{4} \left( -i\sigma_2^z \sigma_1^y \sigma_0^z + \sigma_2^z \sigma_1^x - \sigma_3^z \sigma_1^x \sigma_0^z + i\sigma_3^z \sigma_1^y \right). \tag{75}$$

Now we note that  $\operatorname{supp}(a_0^{\dagger}a_2) \cap \operatorname{supp}(a_1^{\dagger}a_3) = \{2,1,0\}$ , and so we must expect to simplify local operator products on qubits with these indices. Taking the product, we find the following:

$$a_{0}^{\dagger}a_{2}a_{1}^{\dagger}a_{3} = \frac{1}{16} ( \sigma_{2}^{x}\sigma_{0}^{x} - i\sigma_{2}^{x}\sigma_{0}^{y} + \sigma_{2}^{x}\sigma_{1}^{z}\sigma_{0}^{x} - i\sigma_{2}^{x}\sigma_{1}^{z}\sigma_{0}^{y}$$

$$+ i\sigma_{2}^{y}\sigma_{0}^{x} + \sigma_{2}^{y}\sigma_{0}^{y} + i\sigma_{2}^{y}\sigma_{1}^{z}\sigma_{0}^{x} + \sigma_{2}^{y}\sigma_{1}^{z}\sigma_{0}^{y}$$

$$+ \sigma_{3}^{z}\sigma_{2}^{x}\sigma_{0}^{x} - i\sigma_{3}^{z}\sigma_{2}^{x}\sigma_{0}^{y} + \sigma_{3}^{z}\sigma_{2}^{x}\sigma_{1}^{z}\sigma_{0}^{x} - i\sigma_{3}^{z}\sigma_{2}^{x}\sigma_{1}^{z}\sigma_{0}^{y}$$

$$+ i\sigma_{3}^{z}\sigma_{2}^{y}\sigma_{0}^{x} + \sigma_{3}^{z}\sigma_{2}^{y}\sigma_{0}^{y} + i\sigma_{3}^{z}\sigma_{2}^{y}\sigma_{1}^{z}\sigma_{0}^{x} + \sigma_{3}^{z}\sigma_{2}^{y}\sigma_{1}^{z}\sigma_{0}^{y} ).$$

$$(76)$$

Since the integral  $h_{0132}$  is real, we can simply add the above result to its Hermitian conjugate to find the expression for the double-excitation operator. Repeating the above

procedure for the second double excitation operator, we arrive at the following results:

$$a_0^{\dagger} a_3^{\dagger} a_1 a_2 + a_2^{\dagger} a_1^{\dagger} a_3 a_0 = \frac{1}{8} ( -\sigma_2^x \sigma_0^x + \sigma_2^x \sigma_1^z \sigma_0^x - \sigma_2^y \sigma_0^y + \sigma_2^y \sigma_1^z \sigma_0^y - \sigma_3^z \sigma_2^x \sigma_0^x + \sigma_3^z \sigma_2^z \sigma_0^z - \sigma_3^z \sigma_2^z \sigma_0^z - \sigma_3^z \sigma_2^z \sigma_0^z + \sigma_3^z \sigma_2^y \sigma_1^z \sigma_0^y );$$

$$(77)$$

$$a_0^{\dagger} a_1^{\dagger} a_3 a_2 + a_2^{\dagger} a_3^{\dagger} a_1 a_0 = \frac{1}{8} ( \sigma_2^x \sigma_0^x + \sigma_2^x \sigma_1^z \sigma_0^x + \sigma_2^y \sigma_0^y + \sigma_2^y \sigma_1^z \sigma_0^y + \sigma_3^z \sigma_2^x \sigma_0^x + \sigma_3^z \sigma_2^x \sigma_1^z \sigma_0^x + \sigma_3^z \sigma_2^y \sigma_0^z + \sigma_3^z \sigma_2^y \sigma_1^z \sigma_0^y ).$$
 (78)

Thus, using the integrals from Table [III](#page-25-0) and the Pauli expressions for the number operators derived in Section [VII A,](#page-25-1) as well as the Coulomb/exchange operators and the doubleexcitation operators derived in this section, we can represent the molecular electronic Hamiltonian for the hydrogen molecule as a sum of products of Pauli matrices in the Bravyi-Kitaev basis:

<span id="page-27-1"></span>
$$\hat{H}_{BK} = -0.81261 \ \mathbf{1} + 0.171201 \ \sigma_0^z + 0.16862325 \ \sigma_1^z - 0.2227965 \ \sigma_2^z + 0.171201 \ \sigma_1^z \sigma_0^z$$

$$+0.12054625 \ \sigma_2^z \sigma_0^z + 0.17434925 \ \sigma_3^z \sigma_1^z + 0.04532175 \ \sigma_2^x \sigma_1^z \sigma_0^x + 0.04532175 \ \sigma_2^y \sigma_1^z \sigma_0^y$$

$$+0.165868 \ \sigma_2^z \sigma_1^z \sigma_0^z + 0.12054625 \ \sigma_3^z \sigma_2^z \sigma_0^z - 0.2227965 \ \sigma_3^z \sigma_2^z \sigma_1^z$$

$$+0.04532175 \ \sigma_3^z \sigma_2^x \sigma_1^z \sigma_0^x + 0.04532175 \ \sigma_3^z \sigma_2^y \sigma_1^z \sigma_0^y + 0.165868 \ \sigma_3^z \sigma_2^z \sigma_1^z \sigma_0^z .$$
 (79)

This Hamiltonian is isospectral to the Jordan-Wigner derived Hamiltonian [\[11\]](#page-36-6):

<span id="page-27-2"></span>
$$\hat{H}_{JW} = -0.81261 \ \mathbf{1} + 0.171201 \ \sigma_0^z + 0.171201 \ \sigma_1^z - 0.2227965 \ \sigma_2^z - 0.2227965 \ \sigma_3^z$$

$$+0.16862325 \ \sigma_1^z \sigma_0^z + 0.12054625 \ \sigma_2^z \sigma_0^z + 0.165868 \ \sigma_2^z \sigma_1^z + 0.165868 \ \sigma_3^z \sigma_0^z$$

$$+0.12054625 \ \sigma_3^z \sigma_1^z + 0.17434925 \ \sigma_3^z \sigma_2^z - 0.04532175 \ \sigma_3^x \sigma_2^x \sigma_1^y \sigma_0^y$$

$$+0.04532175 \ \sigma_3^x \sigma_2^y \sigma_1^y \sigma_0^x + 0.04532175 \ \sigma_3^y \sigma_2^x \sigma_1^x \sigma_0^y - 0.04532175 \ \sigma_3^y \sigma_2^y \sigma_1^x \sigma_0^x. \ (80)$$

Writing the electronic Hamiltonians in the form of equations [\(79\)](#page-27-1) and [\(80\)](#page-27-2) allows for a comparison of the computational resources required to simulate them on a quantum computer. Not all tensor products of Pauli matrices that appear in these Hamiltonians commute with one another, so exponentiating them requires the use of a Trotter approximation. The next section details the Trotterization process for the Hamiltonian in the Bravyi-Kitaev basis.

## <span id="page-27-0"></span>VIII. TROTTERIZATION

Ideally, one could simulate the propagator e −iHt ˆ , where Hˆ = P <sup>k</sup> hk, by sequentially exponentiating the individual terms h<sup>k</sup> on a quantum simulator. However, e <sup>−</sup>iHt <sup>ˆ</sup> = Q e −ihkt

only in the case that the set of h<sup>k</sup> all mutually commute. Both the Bravyi-Kitaev and Jordan-Wigner Hamiltonians contain terms that do not commute with one another, and so a Suzuki-Trotter approximation must be used. The first four orders of Suzuki-Trotter formulae are [\[27\]](#page-37-5):

$$e^{(A+B)t} \approx (e^{At/n}e^{Bt/n})^n + O(t\Delta t); \tag{81}$$

$$e^{(A+B)t} \approx (e^{At/2n}e^{Bt/n}e^{At/2n})^n + O(t(\Delta t)^2);$$
 (82)

$$e^{(A+B)t} \approx \left(e^{\frac{7}{24}At/n}e^{\frac{2}{3}Bt/n}e^{\frac{3}{4}At/n}e^{\frac{-2}{3}Bt/n}e^{\frac{-1}{24}At/n}e^{Bt/n}\right)^n + O(t(\Delta t)^3); \tag{83}$$

$$e^{(A+B)t} \approx (\prod_{i=1}^{5} e^{p_i At/2n} e^{p_i Bt/n} e^{p_i At/2n})^n + O(t(\Delta t)^4),$$
 (84)

where in the 4th order equation, the constants are given by:

$$p_1 = p_2 = p_4 = p_5 = \frac{1}{4 - 4^{1/3}}, \qquad p_3 = 1 - 4p_1.$$
 (85)

The terms of both the Bravyi-Kitaev Hamiltonian and the Jordan-Wigner Hamiltonian can be broken into two subsets, where the terms in each subset all mutually commute but the subsets do not commute with one another. These groups are as follows:

$$\hat{H}_{BK,Z} = -0.81261 \, \mathbf{1} + 0.171201 \, \sigma_0^z + 0.16862325 \, \sigma_1^z - 0.2227965 \, \sigma_2^z + 0.171201 \, \sigma_1^z \sigma_0^z$$

$$+ 0.12054625 \, \sigma_2^z \sigma_0^z + 0.17434925 \, \sigma_3^z \sigma_1^z + 0.165868 \, \sigma_2^z \sigma_1^z \sigma_0^z$$

$$+ 0.12054625 \, \sigma_3^z \sigma_2^z \sigma_0^z - 0.2227965 \, \sigma_3^z \sigma_2^z \sigma_1^z + 0.165868 \, \sigma_3^z \sigma_2^z \sigma_1^z \sigma_0^z;$$
 (86)

$$\hat{H}_{BK,XY} = 0.04532175 \ \sigma_2^x \sigma_1^z \sigma_0^x + 0.04532175 \ \sigma_2^y \sigma_1^z \sigma_0^y + 0.04532175 \ \sigma_3^z \sigma_2^x \sigma_1^z \sigma_0^x$$

$$+ 0.04532175 \ \sigma_3^z \sigma_2^y \sigma_1^z \sigma_0^y; \tag{87}$$

$$\hat{H}_{JW,Z} = -0.81261 \, \mathbf{1} + 0.171201 \, \sigma_0^z + 0.171201 \, \sigma_1^z - 0.2227965 \, \sigma_2^z - 0.2227965 \, \sigma_3^z$$

$$+ 0.16862325 \, \sigma_1^z \sigma_0^z + 0.12054625 \, \sigma_2^z \sigma_0^z + 0.165868 \, \sigma_2^z \sigma_1^z + 0.165868 \, \sigma_3^z \sigma_0^z$$

$$+ 0.12054625 \, \sigma_3^z \sigma_1^z + 0.17434925 \, \sigma_3^z \sigma_2^z;$$

$$(88)$$

$$\hat{H}_{JW,XY} = - \quad 0.04532175 \, \sigma_3^x \sigma_2^x \sigma_1^y \sigma_0^y + 0.04532175 \, \sigma_3^x \sigma_2^y \sigma_1^y \sigma_0^x + 0.04532175 \, \sigma_3^y \sigma_2^x \sigma_1^x \sigma_0^y$$

$$- \quad 0.04532175 \, \sigma_3^y \sigma_2^y \sigma_1^x \sigma_0^x. \tag{89}$$

To understand what computational resources are required for exponentiating operators of this kind, consider the example of the exponentiation of a fourfold product of σ <sup>z</sup> matrices, e i(σ <sup>z</sup>⊗σ <sup>z</sup>⊗σ <sup>z</sup>⊗σ z ) , which is depicted in a circuit diagram in Figure [3](#page-29-0) [\[28\]](#page-37-0).

![](_page_29_Picture_1.jpeg)

FIG. 3: A demonstration of how to exponentiate tensor products of Pauli matrices. First, the parity of the four qubits is computed with CNOT gates, and then a single-qubit phase rotation R<sup>z</sup> is applied. Then, we uncompute the parity with three further CNOT gates.

<span id="page-29-0"></span>In general, an n-fold tensor product of Pauli-Z matrices will require 2(n − 1) CNOT gates and one single-qubit gate (SQG) to exponentiate on a quantum computer. If there are Pauli-X or -Y matrices in the tensor product, we must apply the single-qubit Hadamard or R<sup>x</sup> gate to change basis to the X or Y basis, respectively, before we compute the parity of the set of qubits with CNOT's, and also apply the inverse gates as part of the uncomputing stage [\[28\]](#page-37-0). These gates are given by:

$$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1\\ 1 & -1 \end{bmatrix} \qquad R_x = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & i\\ i & 1 \end{bmatrix}$$
 (90)

Thus, each non-σ z term in a tensor product of Pauli matrices adds 2 single-qubit gates to the cost of exponentiation. For example, the circuit for exponentiating the term σ y 3σ x 2σ x 1σ y 0 is depicted in Figure [4](#page-30-0)

Using the resource counting methods detailed above, we can count the number of singlequbit gates (SQG's) and CNOT gates required to exponentiate (for arbitrary propagation time) the subsets of the Hamiltonians for both encodings. The results of this analysis are in Table [IV.](#page-30-1)

We now have the tools to compare the number of gates required to compute the ground state eigenvalue of either the Bravyi-Kitaev Hamiltonian or the Jordan-Wigner Hamiltonian to chemical precision (±10<sup>−</sup><sup>4</sup> a.u). Due to the small size of our model of the hydrogen system, it is easy for a classical computer to simulate the behavior of the quantum simulator. The true propagator U = e −iHt ˆ can be computed to sufficient precision by a matrix exponential function in Mathematica or a similar software package. Time evolution of the ground state

<span id="page-30-0"></span>![](_page_30_Picture_1.jpeg)

FIG. 4: A demonstration of how to exponentiate tensor products of Pauli-X and -Y matrices. First, the qubits are put in the correct basis by the application of R<sup>x</sup> or Hadamard gates. Then, the parity of the four qubits is computed with CNOT gates, and then a single-qubit phase rotation R<sup>z</sup> is applied. Then, we uncompute the parity with more CNOT gates, and finally change back to the computational (Z) basis.

|             | SQG's | CNOT's | Totals |
|-------------|-------|--------|--------|
| HˆBK,Z      | 10    | 24     | 34     |
| HˆBK,XY     | 20    | 20     | 40     |
| Totals      | 30    | 44     | 74     |
| Hˆ<br>JW,Z  | 10    | 12     | 22     |
| Hˆ<br>JW,XY | 36    | 24     | 60     |
| Totals      | 46    | 36     | 82     |

<span id="page-30-1"></span>TABLE IV: The number of single-qubit gates and CNOT gates required to exponentiate subsets of the electronic Hamiltonian for the hydrogen molecule, represented in terms of spin variables through either the Bravyi-Kitaev transformation or the Jordan-Wigner transformation.

by the true propagator will result in phase evolution:

$$U|\psi_g\rangle = e^{-iE_g t}|\psi_g\rangle. \tag{91}$$

We can therefore compute the exact eigenvalue as follows:

$$\langle \psi_g | U | \psi_g \rangle = \langle \psi_g | e^{-iE_g t} | \psi_g \rangle = e^{-iE_g t}. \tag{92}$$

We set the propagation time to unity, and extract the true eigenvalue E<sup>g</sup> from the complex phase e −iE<sup>g</sup> . To approximate the eigenvalue, we use a Suzuki-Trotter approximation to the

true propagator,  $\tilde{U}$ , and perform an analogous procedure:

$$\frac{\langle \psi_g | \tilde{U} | \psi_g \rangle}{|\langle \psi_g | \tilde{U} | \psi_g \rangle|} = e^{-i\tilde{E}_g t}.$$
(93)

The approximation to the true ground state eigenvalue,  $\tilde{E}_g$ , becomes better as we increase the number of Trotter steps n. Figure 5 below plots the estimated eigenvalues of the minimal basis Jordan-Wigner and Bravyi-Kitaev Hamiltonians as a function of the number of gates required, for the first four orders of Suzuki-Trotter formulae.

We now compare this result to previous estimates. The benchmark is the gate count given in [11] for approximating the Jordan-Wigner Hamiltonian's ground state eigenvalue. It is clear from Figure 5 that our first order approximation requires  $\approx 900$  gates to obtain chemical precision for the Jordan-Wigner Hamiltonian, while the gate estimate in [11] was about 500 for the same task. This discrepancy arises from the fact that any number of variants on the first order Suzuki-Trotter formula could have been used in [11]. Given a noncommuting set of Hamiltonian terms, there is some optimal ordering that will produce the best accuracy. It is not possible to know in advance which ordering is optimal, and given that the number of terms in an electronic Hamiltonian scales as  $O(n^4)$ , in general it is difficult to optimize over the space of possible orderings. We have used the most naïve variant of the first order Suzuki-Trotter formula in Figure 5:

$$e^{-i\hat{H}t} = e^{-i(\hat{H}_Z + \hat{H}_{XY})t} \approx (e^{-i\hat{H}_Z \frac{t}{n}} e^{-i\hat{H}_{XY} \frac{t}{n}})^n.$$
 (94)

However, due to the small size of our model of the hydrogen molecule, it is easy to find an ordering that produces better accuracy. A second, more sophisticated, variant of the first order formula is to arrange the terms in  $\hat{H}_Z$  and  $\hat{H}_{XY}$  in order of descending coefficient magnitude. For example, for the Bravyi-Kitaev Hamiltonian, we have:

$$\hat{H}_Z: \{h_{Z0}, h_{Z1}, h_{Z2}, \ldots\} = \{-0.81261 \ \mathbf{1}, -0.2227965 \ \sigma_2^z, -0.2227965 \ \sigma_3^z \sigma_2^z \sigma_1^z, \ldots\}; \ (95)$$

$$\hat{H}_{XY}: \{h_{XY0}, h_{XY1}, h_{XY2}, \ldots\} = \{0.04532175 \ \sigma_2^x \sigma_1^z \sigma_0^x, 0.04532175 \ \sigma_2^y \sigma_1^z \sigma_0^y, \ldots\}.$$
(96)

Then, we approximate the propagator by alternately exponentiating one term from the ordered list of  $\hat{H}_Z$  terms and one term from the ordered list of  $\hat{H}_{XY}$  terms until we have used all terms from  $\hat{H}_{XY}$ . Then we exponentiate the rest of  $\hat{H}_Z$ :

$$e^{-i\hat{H}t} \approx \left(e^{-ih_{Z0}\frac{t}{n}}e^{-ih_{XY0}\frac{t}{n}}e^{-ih_{Z1}\frac{t}{n}}e^{-ih_{XY1}\frac{t}{n}}\cdots e^{-ih_{XY3}\frac{t}{n}}e^{-ih_{Z4}\frac{t}{n}}e^{-ih_{Z5}\frac{t}{n}}\cdots\right)^{n}.$$
 (97)

![](_page_32_Figure_1.jpeg)

<span id="page-32-0"></span>FIG. 5: The approximation to the ground state eigenvalue, for both the Bravyi-Kitaev Hamiltonian (squares) and Jordan-Wigner Hamiltonian (circles), as a function of the number of gates required. The solid curves are the first order Suzuki-Trotter approximations, the dot-dashed second order, the dotted third order, and the dashed fourth. The dotted horizontal line represents the true eigenvalue, while the solid lines above and below represent the bounds for chemical precision.

With this method, we find that the number of gates required to obtain a chemical precision estimate of the ground state eigenvalue of the Jordan-Wigner Hamiltonian is ≈ 300, fewer than the result from [\[11\]](#page-36-6). Figure [6](#page-33-0) compares the eigenvalue approximations for the na¨ıve first order method and the more sophisticated variant.

The point is that the systematic advantage of the Bravyi-Kitaev method over the Jordan-Wigner method is not obscured by the kind of term-ordering optimization that we have demonstrated above. Exponentiating the Bravyi-Kitaev Hamiltonian requires 74 gates per first order Trotter step (of any variant), while the Jordan-Wigner Hamiltonian requires 82 gates per first order Trotter step. To obtain a precision of ±10<sup>−</sup><sup>4</sup> a.u to the true eigenvalue with the na¨ıve first order Suzuki-Trotter approximation requires 11 Trotter steps for both the Bravyi-Kitaev and Jordan-Wigner Hamiltonian, for a total cost of 814 gates versus

![](_page_33_Figure_1.jpeg)

<span id="page-33-0"></span>FIG. 6: The approximation to the ground state eigenvalue, for both the Bravyi-Kitaev Hamiltonian (squares) and Jordan-Wigner Hamiltonian (circles), as a function of the number of gates required. The solid curve is the na¨ıve first order Suzuki-Trotter approximation, while the dashed curve is the result from alternating the noncommuting terms. The dotted horizontal line represents the true eigenvalue, while the solid lines above and below represent the bounds for chemical precision. The ground state eigenvalue of the Bravyi-Kitaev Hamiltonian can be approximated to chemical precision with 222 gates, while it takes 328 gates to do the same for the Jordan-Wigner Hamiltonian.

902 gates. With the noncommuting terms intermixed, it takes only 3 Trotter steps to obtain the same precision for the Bravyi-Kitaev Hamiltonian, and 4 Trotter steps for the Jordan-Wigner Hamiltonian. Thus, if we intermix the noncommuting terms, the Bravyi-Kitaev transformation allows one to utilize 222 gates instead of the 328 gates required by the Jordan-Wigner transformation to obtain an equally precise estimate of the hydrogen molecule's ground state eigenvalue when using a first order Suzuki-Trotter approximation. When using higher-order Suzuki-Trotter approximations to obtain better than chemical precision, the gate savings increases (Fig. [7\)](#page-34-0).

![](_page_34_Figure_1.jpeg)

<span id="page-34-0"></span>FIG. 7: The gate savings of using the Bravyi-Kitaev method instead of the Jordan-Wigner method, as a function of the precision in the estimate of the ground state eigenvalue for the first four orders of Suzuki-Trotter formulae. The vertical line is the threshold error for chemical precision. The triangle data points are first order, the squares second, the circles third, and the diamonds fourth.

### IX. CONCLUSIONS

In this paper we have worked out a detailed application of the Bravyi-Kitaev transformation to Hermitian second quantized operators that appear in quantum chemical Hamiltonians. We suggest that this transformation should replace the Jordan-Wigner transformation for fermionic quantum simulation algorithms. We have demonstrated that the Bravyi-Kitaev transformation results in a small reduction in the number of gates, from 328 gates to 222 gates, required to implement a quantum simulation algorithm for electron dynamics in the simplest possible molecular system of H<sup>2</sup> in a minimal basis.

In some sense, molecular hydrogen in a minimal basis is a poor showcase of the power of the Bravyi-Kitaev transformation. Our description of this molecule utilizes four molecular orbitals, and hence four qubits. The spin Hamiltonians we derive using either the Bravyi-Kitaev transformation or the Jordan-Wigner Hamiltonian involve four-local Pauli tensor products, the result being that the cost of simulating time evolution under the BravyiKitaev Hamiltonian on a quantum computer is only slightly reduced from that for the Jordan-Wigner Hamiltonian. However, were we to use a more sophisticated description of the H<sup>2</sup> — for example, with eight molecular orbitals — the Jordan-Wigner spin Hamiltonian would contain up to eight-local Pauli tensor products, while the Bravyi-Kitaev spin Hamiltonian would not. Given the asymptotically better O(log n) scaling of the Bravyi-Kitaev method as compared to the O(n) scaling of the Jordan-Wigner transformation, the difference between the two methods will become greater for larger basis sets and larger molecules — the simulation of which is, after all, is the true goal of quantum simulation for quantum chemistry, since the small molecules are within the reach of conventional computers. However, by showing that the Bravyi-Kitaev method is more efficient for the smallest conceivable chemical system, we have demonstrated that there is no algorithmic overhead inherent to the Bravyi-Kitaev method that must be overcome by scaling up the size of problems to which it is applied. We have demonstrated the superior efficiency of the Bravyi-Kitaev transformation for all quantum chemical simulations. Thus, making use of the Bravyi-Kitaev transformation for fermionic quantum simulation will make simulations of larger molecules and with larger basis sets more readily accessible to experiment.

## X. ACKNOWLEDGMENTS

The authors thank the Aspuru-Guzik group for their hospitality during the summers of 2011 and 2012, when parts of this work were completed. We are indebted to Jarod Maclean, John Parkhill, Sam Rodriques, Joshua Schrier, Robert Seeley, and James Whitfield for productive discussions. This project is supported by NSF CCI center, "Quantum Information for Quantum Chemistry (QIQC)", award number CHE-1037992, by NSF award PHY-0955518 and by AFOSR award no FA9550-12-1-0046.

<span id="page-35-1"></span><span id="page-35-0"></span><sup>[1]</sup> R. P. Feynman, Optics News, 11, 11 (1985).

<span id="page-35-2"></span><sup>[2]</sup> S. Lloyd, Science, 273, 1073 (1996).

<span id="page-35-3"></span><sup>[3]</sup> A. Aspuru-Guzik, A. D. Dutoi, P. J. Love, and M. Head-Gordon, Science, 309, 1704 (2005).

<sup>[4]</sup> D. A. Lidar and H. Wang, Phys. Rev. E, 59, 2429 (1999).

- <span id="page-36-0"></span>[5] I. Kassal, S. P. Jordan, P. J. Love, M. Mohseni, and A. Aspuru-Guzik, P Natl Acad Sci Usa, 105, 18681 (2008).
- <span id="page-36-2"></span><span id="page-36-1"></span>[6] G. Ortiz, J. Gubernatis, E. Knill, and R. Laflamme, Phys. Rev. A, 64, 022319 (2001).
- <span id="page-36-3"></span>[7] I. Kassal and A. Aspuru-Guzik, Journal of Chemical Physics, 131, 4102 (2009).
- <span id="page-36-4"></span>[8] D. S. Abrams and S. Lloyd, Phys. Rev. Lett., 79, 2586 (1997).
- [9] R. Somma, G. Ortiz, J. E. Gubernatis, E. Knill, and R. Laflamme, Phys. Rev. A, 65, 42323 (2002).
- <span id="page-36-6"></span><span id="page-36-5"></span>[10] P. Jordan and E. Wigner, Z. Phys., 47, 631 (1928).
- <span id="page-36-7"></span>[11] J. D. Whitfield, J. Biamonte, and A. Aspuru-Guzik, Molecular Physics, 109, 735 (2011).
- [12] F. Verstraete and J. I. Cirac, Journal of Statistical Mechanics: Theory and Experiment, 09, 012 (2005).
- <span id="page-36-9"></span><span id="page-36-8"></span>[13] S. Bravyi and A. Kitaev, Annals of Physics, 298, 210 (2002), [quant-ph/0003137v2](http://arxiv.org/abs/quant-ph/0003137v2) .
- <span id="page-36-10"></span>[14] R. C. Ball, Phys. Rev. Lett., 95, 176407 (2005).
- [15] B. P. Lanyon, J. D. Whitfield, G. G. Gillett, M. E. Goggin, M. P. Almeida, I. Kassal, J. D. Biamonte, M. Mohseni, B. J. Powell, M. Barbieri, A. Aspuru-Guzik, and A. G. White, Nature Chemistry, 2, 106 (2010).
- <span id="page-36-12"></span><span id="page-36-11"></span>[16] A. Aspuru-Guzik and P. Walther, Nature Physics, 8, 285 (2012).
- <span id="page-36-13"></span>[17] J. Du, N. Xu, X. Peng, P. Wang, S. Wu, and D. Lu, Phys. Rev. Lett., 104, 030502 (2010).
- [18] B. P. Lanyon, C. Hempel, D. Nigg, M. M¨uller, R. Gerritsma, F. Z¨ahringer, P. Schindler, J. T. Barreiro, M. Rambach, G. Kirchmair, M. Hennrich, P. Zoller, R. Blatt, and C. F. Roos, Science, 334, 57 (2011), (c) 2011: Science.
- <span id="page-36-15"></span><span id="page-36-14"></span>[19] R. Blatt and C. F. Roos., Nature Physics, 8, 277 (2012).
- <span id="page-36-16"></span>[20] L. Veis and J. Pittner, Journal of Chemical Physics, 133, 4106 (2010).
- [21] L. Veis, J. Viˇsˇn´ak, T. Fleig, S. Knecht, T. Saue, L. Visscher, and J. Pittner, Phys. Rev. A, 85, 030304 (2012).
- <span id="page-36-18"></span><span id="page-36-17"></span>[22] P. J. Love, Advances in Chemical Physics (2012), in Press, arxiv:1208.5524.
- [23] N. C. Jones, J. D. Whitfield, P. L. McMahon, M.-H. Yung, R. V. Meter, A. Aspuru-Guzik, and Y. Yamamoto, (2012), arxiv:1204.0567v1.
- <span id="page-36-20"></span><span id="page-36-19"></span>[24] P. Zanardi, Phys. Rev. A, 65, 042101 (2002).
- [25] H. F. Trotter, Proceedings of the American Mathematical Society, 10, 545 (1959).
- [26] M. Suzuki, Physics Letters A, 165, 387 (1992).

- <span id="page-37-5"></span>[27] N. Hatano and M. Suzuki, in Quantum Annealing and Other Optimization Methods, Lecture Notes in Physics 679 , edited by A. Das and B. K. Chakrabarti (Springer, 2005) pp. 36–68.
- <span id="page-37-0"></span>[28] M. A. Nielsen and I. L. Chuang, Quantum computation and quantum information (Cambridge University Press, Cambridge, 2000).
- <span id="page-37-2"></span><span id="page-37-1"></span>[29] R. McWeeny, Methods of Molecular Quantum Mechanics (Academic Press, 1992).
- [30] A. Szabo and N. Ostlund, Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory (Dover Publications, 1996).
- <span id="page-37-3"></span>[31] A. Dutta, U. Divakaran, D. Sen, B. K. Chakrabarti, T. F. Rosenbaum, and G. Aeppli, (2010), [arxiv:1012.0653v1](http://arxiv.org/abs/arxiv:1012.0653v1) .
- <span id="page-37-4"></span>[32] R. P. Muller, "Python quantum chemistry (pyquante) program," (2007).