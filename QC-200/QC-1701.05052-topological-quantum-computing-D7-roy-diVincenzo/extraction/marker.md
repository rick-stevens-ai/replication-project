# D 7 Topological Quantum Computing

Ananda Roy and David P. DiVincenzo Institute for Quantum Information, RWTH Aachen University and Peter Grunberg Institut and Institute for Advanced Simulation, ¨ Forschungszentrum Julich GmbH ¨

# Contents

| 1 |                                          | Introduction                                             | 2  |
|---|------------------------------------------|----------------------------------------------------------|----|
| 2 |                                          | Abelian anyons                                           |    |
|   | 2.1                                      | Basics of abelian anyons                                 | 3  |
|   | 2.2                                      | A physical realization of abelian anyons                 | 4  |
| 3 | Non-abelian anyons                       |                                                          | 8  |
|   | 3.1                                      | Basic definition of a Majorana fermion .                 | 8  |
|   | 3.2                                      | Non-abelian statistics of Majorana fermions              | 9  |
|   | 3.3                                      | A physical realization of Majorana fermions .            | 11 |
| 4 | Quantum computing with Majorana fermions |                                                          | 13 |
|   | 4.1                                      | Clifford operations on Majorana qubits .                 | 13 |
|   | 4.2                                      | Implementation of a controlled-phase gate                | 14 |
|   | 4.3                                      | π/8<br>Implementation of a<br>rotation .                 | 15 |
|   | 4.4                                      | Robustness to imperfect preparations of ancilla qubits . | 16 |
| 5 | Conclusion                               |                                                          | 16 |
| 6 | Acknowledgments                          |                                                          | 16 |

Lecture Notes of the 48th IFF Spring School "Topological Matter – Topological Insulators, Skyrmions and Majoranas" (Forschungszentrum Julich, 2017). All rights reserved. ¨

# <span id="page-1-0"></span>1 Introduction

Quantum computers have shown great promise as a resource providing exponential speedup over classical computers for certain problems. Akin to their classical counterparts, quantum computers will be prone to errors. There are two major sources of errors. First, the most formidable source of error is decoherence. To perform quantum computation, quantum information must be stored, processed and read out while protecting it from the debilitating effects of decoherence. Second, even if the system is protected from decoherence, it is almost certain that all the operations performed on the quantum information during its processing will be imperfect. These errors will accumulate over the duration of the computation, eventually causing failure. Thus, for a quantum computing scheme to be feasible, it needs to be fault-tolerant. What this means is that the quantum computer can still perform its task effectively while its components are imperfect. A major breakthrough in this field is the threshold theorem, which asserts that ideal quantum circuits can be simulated efficiently by noisy ones provided the error rates of individual gates are below a certain threshold [\[1,](#page-16-0) [2,](#page-16-1) [3\]](#page-16-2).

Topological quantum computing is an approach to fault-tolerant quantum computation, where the protection from errors occurs not from active intervention, but at a hardware level. The advantage of this approach is that it is robust to localized imperfections. First envisioned by Alexei Kitaev [\[4\]](#page-16-3), this scheme makes use of a non-abelian exchange statistics of elementary excitations of some two-dimensional quantum many-body system. These excitations form the degenerate ground-space of this topologically ordered system, and all other states are separated from this space by a finite excitation gap. In order to perform computation in this scheme, one needs to create pairs of these non-abelian excitations (called non-abelian anyons) from vacuum, separating them spatially, transporting them around each other to implement the logical gates and finally, fusing them together for measurements.

In order for this scheme to be viable, there are two conditions that must be fulfilled. First, there could be errors due to quantum tunneling between the non-abelian anyons. These processes can take place even at zero temperature. But, the amplitude of these processes are exponentially suppressed with the spatial separation of these particles and goes as e −L/l<sup>0</sup> , where L is the spatial separation and l<sup>0</sup> is some characteristic length scale of topological ordering of the system. Thus, to prevent such tunneling during quantum information processing and storage, L has to be much larger than l0. Second, at finite temperature, undesired thermally excited quasiparticles can lead to errors. The generation rate of these particles are exponentially suppressed by a Boltzmann factor e <sup>−</sup>∆/T , where ∆ is the excitation energy and T is the temperature. Therefore, the temperature must be low enough so that there are sufficiently low number of these undesired excitations.

There are several physical systems where these excitations could, in principle, be found, manipulated and measured. Non-abelian anyons were proposed as elementary excitations of the ν = 5/2 state in the fractional quantum hall effect [\[5\]](#page-16-4). The braiding statistics of these particles and their possible use in quantum computing has been investigated thoroughly. For more information on this topic, the reader is invited to consult [\[6,](#page-16-5) [7\]](#page-16-6). In a pathbreaking work [\[8\]](#page-16-7), it was proposed that the non-abelian statistics of the excitations of the ν = 5/2 state are shared by the Majorana excitations of a 2D spinless p + ip superconductor. Since then, there have been other theoretical models [\[9,](#page-16-8) [10\]](#page-16-9) which also support these non-abelian excitations. Moreover, several experimental realizations of these Majorana excitations in solid state systems have also been proposed (for a comprehensive review, see [\[11\]](#page-16-10)).

In this lecture note, we will focus on implementation of topological quantum computation with

Majorana fermions. The note is organized as follows. We begin by reviewing the basics of abelian anyons in Sec. [2.1.](#page-2-1) Then, we describe how abelian anyons can be found in a theoretical model, namely the honeycomb model, proposed by Alexei Kitaev [\[10\]](#page-16-9). In Sec. [2.2,](#page-3-0) we describe the model, followed by a brief outline of its exact solution and finally describe the abelian anyonic excitations present in this model. Next, we cover the basics of Majorana fermions in Sec. [3.1,](#page-7-1) followed by a demonstration of their non-abelian exchange statistics in Sec. [3.2.](#page-8-0) Subsequently, in Sec. [3.3,](#page-10-0) we describe how these excitations can occur in the honeycomb model mentioned above in presence of a magnetic field. Next, we describe how to perform topological quantum computing with these Majoranas. We keep our discussion sufficiently general so that they can applied to any system that supports these excitations. In Sec. [4.1,](#page-12-1) we describe protocols to implement Clifford gates with these Majorana excitations, followed by implementation of controlled-Z gate in Sec. [4.2](#page-13-0) and π/8 gate in Sec. [4.3.](#page-14-0) We briefly discuss the effect of imperfections in these protocols in Sec. [4.4.](#page-15-0) Finally, concluding remarks are presented in Sec. [5.](#page-15-1)

# <span id="page-2-0"></span>2 Abelian anyons

### <span id="page-2-1"></span>2.1 Basics of abelian anyons

Abelian anyons are particles which exist in (2 + 1) dimensions. Exchange of these particles along some topologically specified trajectories gives rise to a multiplication of the overall wavefunction of the quantum state of the system by a phase-factor e iϕ. In general, ϕ can be any rational multiple of 2π. Since clockwise and counter-clockwise exchanges are not equivalent, the group of these exchanges is the infinite braid group instead of the permutation group [\[12\]](#page-16-11). Abelian anyons transform as one-dimensional representation of this group.

The simplest example of an abelian anyon is a flux-charge composite particle that occurs in (2 + 1) dimensional electromagnetism models, first studied by Wilczek [\[13,](#page-16-12) [14\]](#page-16-13). In this model, the charges take integer values and the magnetic vortices carry fluxes which are real numbers. Each of these excitations are separately bosonic, but considered together they show nontrivial statistics due to the Aharonov-Bohm effect [\[15\]](#page-16-14). This is understood as follows. When a charge q goes around a flux φ, the system picks up an overall Aharonov-Bohm phase 2πqφ/h, where h is the Planck's constant. As in the Aharonov-Bohm effect, this phase is topological in nature, *i.e.* it is robust to deformation of the trajectory and depends only on the overall winding number of the charge about the flux. Now, what happens when two of these charge-flux composites (q, φ) are interchanged? When they are interchanged, each of the charges go half-way around the flux of the other composite. Therefore, each contribute an Aharonov-Bohm phase of πqφ/h. Thus, the wave-function gets multiplied by e iϕ, where ϕ = 2πqφ/h. Note that this phase is the same as rotating one of these composite particles (q, φ) by 2π, which is what one expects from the usual spin-statistics relation.

Next, we describe the exchange statistics of molecules composed of anyons. Consider two molecules composed of n anyons. Let each of the anyons have an exchange statistic given by the phase ϕ. What is then the exchange statistic of these two molecules? Due to the interchange, each of the n charges of one molecule goes around n fluxes of the other molecule. Thus, each molecule contributes a phase of n <sup>2</sup>ϕ/2 and the total wave-function is multiplied by a factor e in2ϕ (see Chap. 9.4 of [\[16\]](#page-16-15)).

In the next section, we will describe a physical model for interacting spins on a honeycomb

![](_page_3_Figure_2.jpeg)

<span id="page-3-2"></span>**Fig. 1:** (a) Schematic of the honeycomb lattice (image from [10]). The lattice is composed of two sublattices, shown with solid and empty circles. Spin-1/2 particles are located at each vertex of the lattice and they interact through nearest neighbor interaction. The form of the interaction depends on the type of link that connects them. For instance, two spins connected by an x-link interact through an XX interaction. Similar behavior holds for the y-links and z-links. (b) One plaquette of honeycomb lattice (image from [10]). The plaquette operator  $(W_p)$  is given by the product of six Pauli operators, one for each site of the plaquette. Which kind of Pauli operator shows up at each site depends on the nature of the external link at each site.

lattice, first proposed by Kitaev [10], which supports these abelian excitations for a certain choice of parameters<sup>1</sup>. We will see that the abelian anyons in this model are exactly the flux-charge composites described above.

### <span id="page-3-0"></span>2.2 A physical realization of abelian anyons

#### The honeycomb model

Consider spin-1/2 particles (spin being the only relevant degree of freedom) located at the vertices of a honeycomb lattice (cf. Fig. 1). They interact through nearest neighbor interaction, and the form of the interaction depends on the type of link that connects them. For instance, two spins connected by an x-link interact with an XX interaction. Similar behavior holds for y-links and z-links. Thus, the Hamiltonian is given by:

<span id="page-3-3"></span>
$$H = -J_x \sum_{x-links} \sigma_j^x \sigma_k^x - J_y \sum_{y-links} \sigma_j^y \sigma_k^y - J_z \sum_{z-links} \sigma_j^z \sigma_k^z, \tag{1}$$

where  $J_x, J_y, J_z$  are the parameters that determine the strength of these interactions. We will choose these parameters to be positive for simplicity. The case for any of them being negative can be analyzed similarly. One can check that plaquette operators for each hexagonal plaquette defined by  $W_p = \sigma_1^x \sigma_2^y \sigma_3^z \sigma_4^x \sigma_5^y \sigma_6^z$  (with eigenvalues  $w_p = \pm 1$ ) are conserved quantities since they commute with each other and H. Thus, the total Hilbert space splits up into sectors of different plaquette operator eigenspaces. In fact, in each sector, one can exactly solve the problem. This is outlined below.

<span id="page-3-1"></span><sup>&</sup>lt;sup>1</sup>As we will see later, this model also supports non-abelian anyons for a different choice of parameters.

![](_page_4_Figure_2.jpeg)

<span id="page-4-0"></span>**Fig. 2:** Brick-wall lattice, equivalent to the honeycomb lattice (image from [17]). In blue is shown the enumeration of the spins used for the Jordan-Wigner transformation.

#### <span id="page-4-1"></span>**Exact solution of the honeycomb model**

There are two distinct ways to solve the honeycomb model. One was proposed by Kitaev in his pioneering work [10] by mapping each spin to four Majorana fermions. Here, we take an alternate approach, where we solve the problem using Jordan-Wigner transformation. This transformation maps the spins to fermions in an equivalent brick-wall lattice with open boundary condition, with the enumeration of the spins shown in Fig. 2. Our analysis follows closely that of Chen and Nussinov [17].

We begin by mapping the spins to fermions as follows:

$$\sigma_{ij}^{+} = \left[ \prod_{j' < j} \prod_{i'} \sigma_{i'j'}^{z} \right] \left[ \prod_{i' < i} \sigma_{i'j}^{z} \right] c_{ij}^{\dagger}, \tag{2}$$

$$\sigma_{ij}^z = 2c_{ij}^{\dagger}c_{ij} - 1, \tag{3}$$

where the indices i, j denote the cartesian coordinates of the lattice sites and  $\sigma_{ij}^+ = (\sigma_{ij}^x + i\sigma_{ij}^y)/2$ . Under this mapping, the Hamiltonian becomes

$$H = J_x \sum_{x-links} (c^{\dagger} - c)_w (c^{\dagger} + c)_b - J_y \sum_{y-links} (c^{\dagger} + c)_b (c^{\dagger} - c)_w$$
$$-J_z \sum_{z-links} (2c^{\dagger}c - 1)_b (2c^{\dagger}c - 1)_w, \tag{4}$$

where w, b indicate whether the fermion is on a white or black lattice site. We introduce Majorana operators for each of the black and white lattice sites as follows:

$$A_w = i(c^{\dagger} - c)_w, B_w = (c^{\dagger} + c)_w, A_b = (c^{\dagger} + c)_b, B_b = i(c^{\dagger} - c)_b.$$
 (5)

Then, the Hamiltonian transforms to:

<span id="page-4-2"></span>
$$H = -iJ_x \sum_{x-links} A_w A_b + iJ_y \sum_{y-links} A_b A_w - iJ_z \sum_{z-links} \alpha_r A_b A_w.$$
 (6)

In the last line, we have defined the operator α<sup>r</sup> ≡ iBbB<sup>w</sup> along each z-link, where r is the coordinate of the midpoint of the link. Note that each α<sup>r</sup> commutes with the Hamiltonian and is thus a conserved quantity.

Next, we solve the above Hamiltonian for α<sup>r</sup> = 1, ∀r. This is the relevant choice to solve the Hamiltonian in the (ground space) vortex-free sector [\[10,](#page-16-9) [17\]](#page-16-16), when all the w<sup>p</sup> = 1. To that end, we define a fermion operator as:

$$d = (A_w + iA_b)/2, d^{\dagger} = (A_w - iA_b)/2.$$
(7)

This leads to

$$H = J_x \sum_{r} (d_r^{\dagger} + d_r)(d_{r+e_x}^{\dagger} - d_{r+e_x}) + J_y \sum_{r} (d_r^{\dagger} + d_r)(d_{r+e_y}^{\dagger} - d_{r+e_y}) + J_z \sum_{r} (2d_r^{\dagger}d_r - 1),$$
(8)

where ex, e<sup>y</sup> are unit vectors shown in Fig. [2.](#page-4-0) Fourier transforming the above equation yields a p-wave superconducting Hamiltonian:

<span id="page-5-2"></span><span id="page-5-0"></span>
$$H_g = \sum_{q} \left\{ \epsilon_q d_q^{\dagger} d_q + \left( i \frac{\Delta_q}{2} d_q^{\dagger} d_{-q}^{\dagger} + h.c. \right) \right\}, \tag{9}$$

where the subscript g indicates that this Hamiltonian describes the vortex free sector. The energy and gap parameters of this superconducting Hamiltonian is given by:

$$\epsilon_q = 2J_z - 2J_x \cos q_x - 2J_y \cos q_y, \ \Delta_q = 2J_x \sin q_x + 2J_y \sin q_y.$$
 (10)

The Hamiltonian H<sup>g</sup> can easily be diagonalized by Bogoliubov transformation. The detailed form of the excitation spectrum is not relevant for our discussion and the interested reader can consult [\[17\]](#page-16-16) for details. However, one can already see from Eq. [\(10\)](#page-5-0) that the spectrum is gapless for:

<span id="page-5-1"></span>
$$J_x \le J_y + J_z, J_y \le J_z + J_x, J_z \le J_x + J_y, \tag{11}$$

and the system is in a gapped phase whenever these conditions are violated. The complete phase-diagram is shown in Fig. [3.](#page-6-0)

Next, we will analyze the excitations in one of the gapped phases of the honeycomb model. We will show that these excitations are indeed abelian anyons. To that end, it will be sufficient to consider the model in perturbation theoretical limit Jx, J<sup>y</sup> J<sup>z</sup> in phase Az. Our analysis will follow that of [\[10\]](#page-16-9).

### <span id="page-5-3"></span>Abelian anyons in the honeycomb model

The starting point of this perturbation theory analysis is the Hamiltonian (H = H<sup>0</sup> + V ) given in Eq. [\(1\)](#page-3-3), where

$$H_0 = -J_z \sum_{z-links} \sigma_j^z \sigma_k^z, \ V = -J_x \sum_{x-links} \sigma_j^x \sigma_k^x - J_y \sum_{y-links} \sigma_j^y \sigma_k^y.$$
 (12)

The ground state for J<sup>x</sup> = J<sup>y</sup> = 0 is highly degenerate with each pair of spins connected by z-links being either in | ↑↑i or in | ↓↓i and can be thought of an effective spin. Next, we include

![](_page_6_Picture_2.jpeg)

Fig. 3: *Phase diagram for the honeycomb model (image from [\[10\]](#page-16-9)). The model supports three gapped phases (*Ax, Ay, Az*) and one gapless phase (*B*), depending on the parameters* Jx, Jy, J<sup>z</sup> *[cf. Eq.* [\(11\)](#page-5-1)*].*

<span id="page-6-0"></span>the perturbing Hamiltonian V . In order to compute the effective Hamiltonian on this ground space, one needs to perform either a self-energy calculation or a Schrieffer-Wolff transformation (see Appendix B of [\[18\]](#page-16-17)). The non-trivial Hamiltonian shows up in the fourth-order calculation [\[10\]](#page-16-9). We merely state the final result:

<span id="page-6-1"></span>
$$H_{\text{eff}} = -J_{\text{eff}} \Big( \sum_{\text{vertices}} A_s + \sum_{\text{plaquettes}} B_p \Big), \tag{13}$$

where Jeff = J 2 xJ 2 y /(16J 3 z ) and As, B<sup>p</sup> are defined below. Here, we have already made a unitary transformation that puts each of the effective spins of the original model on the links of a square lattice (Fig. [4\)](#page-7-2). Note that this is in contrast to the original model where the spins are on the vertices. The operators As, B<sup>p</sup> are defined as:

$$A_s = \prod_{\text{star(s)}} \sigma_j^x, \ B_p = \prod_{\text{boundary(p)}} \sigma_j^z, \tag{14}$$

where the σ x,z j denote the Pauli operators for the effective spins. It is easy to check that the operators As, B<sup>p</sup> commute with each other and thus, with Heff. The ground state is given by the state with the eigenvalues of each of As, B<sup>p</sup> being +1. Excited states can be obtained by flipping the eigenvalues of the star and plaquette operators. When a specific A<sup>s</sup> operator has eigenvalue −1, the excitation is called an electric charge and is located at the vertex s. On the other hand, when a specific B<sup>p</sup> operator has eigenvalue −1, the excitation is a magnetic vortex and is located at the plaquette p. These electric charges and magnetic vortices behave exactly like the ones described in Sec. [2.1.](#page-2-1) Both the electric charges and the magnetic vortices are bosonic when considered separately. However, moving an electric charge around a magnetic vortex gives a nontrivial phase of −1, as would be expected due to the Aharonov-Bohm effect. Thus, the electric charge and magnetic vortex excitations of the gapped phase are abelian anyons. A more detailed proof of this can be found in [\[17\]](#page-16-16). The different superselection sectors of this phase and their braiding rules of them are explicitly given in [\[10\]](#page-16-9).

![](_page_7_Picture_2.jpeg)

Fig. 4: *Effective lattice for the Hamiltonian given in Eq.* [\(13\)](#page-6-1) *(image from [\[19\]](#page-16-18)). Here, the effective spins of the honeycomb lattice reside on the links and not on the vertices. The Hamiltonian is given in Eq.* [\(13\)](#page-6-1)*, which is composed of star operators* A<sup>s</sup> = Q star(s) σ x <sup>j</sup> *and the plaquette operators* B<sup>p</sup> = Q boundary(p) σ z j *.*

# <span id="page-7-2"></span><span id="page-7-0"></span>3 Non-abelian anyons

Non-abelian anyons are excitations in (2 + 1) dimensions, which when exchanged along some topologically specified trajectories, the overall wavefunction of the system gets multiplied by a unitary matrix. Since matrix-multiplication is non-commutative, these excitations show nonabelian exchange statistics. In terms of the braid group representations, the non-abelian anyons transform according to representations which have dimensions > 1. In this note, we focus on one kind of such non-abelian particles: the Majorana fermions.

# <span id="page-7-1"></span>3.1 Basic definition of a Majorana fermion

In this section, we describe the basic properties of Majorana fermions, following the treatments of [\[20,](#page-16-19) [21\]](#page-16-20). Consider 2n spatially well-separated Majoranas γ1, . . . γ2n. Since a Majorana degree of freedom is half a fermionic degree of freedom, one can combine them to give rise to full fermions:

<span id="page-7-4"></span>
$$f_j = (\gamma_{2j-1} + i\gamma_{2j})/2.$$
 (15)

This, in turn, implies:

$$\gamma_{2j-1} = f_j^{\dagger} + f_j, \tag{16}$$

$$\gamma_{2j} = i(f_j^{\dagger} - f_j). \tag{17}$$

Note that the Majorana operators are hermitian, γ<sup>j</sup> = γ † j , satisfying the following anti-commutation relations:

<span id="page-7-3"></span>
$$\{\gamma_j, \gamma_k\} = 2\delta_{jk}.\tag{18}$$

The last equation follows from the usual fermion anti-commutation relations for the operators fj . Eq. [\(18\)](#page-7-3) implies that γ 2 <sup>j</sup> = 1. It is important to realize that it does not make sense to talk about the occupancy of a Majorana mode. The naively constructed "Majorana number operator",  $\gamma_j^\dagger \gamma_j$  is identically = 1. Similar set of reasoning proves that  $\gamma_j \gamma_j^\dagger = 1$ . Thus, in the traditional sense, the Majorana mode is empty and filled at the same time. However, it is possible to speak of the number states  $|n_j\rangle$ , which are eigenstates of the number operator  $n_j = f_j^\dagger f_j, j = 1, \ldots, n$ . In terms of the Majorana fermions, these number operators are given by:

$$n_j = f_j^{\dagger} f_j = \frac{1}{2} (1 + i\gamma_{2j-1}\gamma_{2j}), j = 1, \dots, n.$$
 (19)

In general for spatially separated Majorana fermions, the way to re-write them in terms of traditional fermions is non-unique  $^2$ . Note that the ground space of these 2n Majorana fermions is  $2^n$ -fold degenerate, corresponding to each  $n_i$  being equal to zero or one.

### <span id="page-8-0"></span>3.2 Non-abelian statistics of Majorana fermions

In this section, we describe the non-abelian exchange statistics of the Majorana fermions. We keep our treatment sufficiently general so that it is applicable to any system that supports these excitations.

An essential component of non-abelian statistics is a degenerate ground space, which as discussed above, is true for a system supporting spatially separated Majorana fermions<sup>3</sup>. Further, this ground space must be separated from all the excited states by an excitation gap, so that the exchange statistics is well-defined. Then, exchange operations, performed adiabatically compared to the excitation gap, can bring the system from one ground state to another.

Consider again 2n spatially localized Majorana fermions:  $\gamma_i, i=1,\ldots,2n$ . Fixing the initial position of the Majoranas, consider a permutation of the Majoranas. The exchange statistics of these Majoranas is given by a unitary representation of the braid group. This group, denoted by  $B_{2n}$ , is generated by exchange operations  $B_{i,i+1}, i=1,\ldots,2n-1$  of the neighboring Majoranas labeled by i and i+1. These operators satisfy the following relations:

<span id="page-8-3"></span>
$$B_{i,i+1}B_{j,j+1} = B_{j,j+1}B_{i,i+1}, |i-j| > 1,$$
 (20)

$$B_{i,i+1}B_{j,j+1}B_{i,i+1} = B_{j,j+1}B_{i,i+1}B_{j,j+1}, \qquad |i-j| = 1.$$
 (21)

Next, we give a simple argument to motivate the explicit representation of the braid operations [22]. Consider a clockwise exchange of the two Majorana fermions,  $\gamma_i$  and  $\gamma_{i+1}$  (cf. Fig. 5). This is accomplished by acting these operators by conjugation with the unitary operator  $B_{i,i+1}$ . Let us denote the Majorana operators after the exchange by  $\gamma_i'$  and  $\gamma_{i+1}'$ . Therefore,

$$\gamma_i' = B_{i,i+1}\gamma_i B_{i,i+1}^{\dagger}, \ \gamma_{i+1}' = B_{i,i+1}\gamma_{i+1} B_{i,i+1}^{\dagger}.$$
(22)

Since the position of the two Majoranas are interchanged by this operation,

$$\gamma_i' = \alpha_i \gamma_{i+1}, \ \gamma_{i+1}' = \alpha_{i+1} \gamma_i', \tag{23}$$

<span id="page-8-1"></span><sup>&</sup>lt;sup>2</sup>However, when two Majorana fermion wave-functions overlap, it is natural to combine them into a traditional fermion.

<span id="page-8-2"></span><sup>&</sup>lt;sup>3</sup>In general, the degeneracy of the ground space is lifted for finite separation of the Majoranas. The energy splitting is exponentially suppressed with the spatial separation. We will always assume this splitting to be small enough to be negligible.

![](_page_9_Picture_2.jpeg)

![](_page_9_Picture_3.jpeg)

**Fig. 5:** Schematic of braiding operations of Majorana excitations. (a) Schematic of a clockwise exchange of two Majorana fermions  $\gamma_i$  and  $\gamma_{i+1}$ . (b) Schematic of moving the Majorana fermion  $\gamma_i$  around  $\gamma_{i+1}$  in a clockwise direction.

<span id="page-9-0"></span>where  $\alpha_i, \alpha_{i+1} \in \Re$  since the Majorana operators are real. Since this local exchange operation does not change the fermion number parity,

$$-i\gamma_i\gamma_{i+1} = -i\gamma_i'\gamma_{i+1}'. (24)$$

This implies that

$$\alpha_i \alpha_{i+1} = -1. \tag{25}$$

Thus, one of the Majorana fermions picks up a negative sign and the other doesn't. There is a gauge degree of freedom in choosing which of the Majoranas picks up the negative sign. We will work with the convention that

$$\alpha_i = 1, \alpha_{i+1} = -1. {(26)}$$

Thus, the result of this exchange operation is

$$\gamma_i \rightarrow \gamma_{i+1},$$
 (27)

$$\gamma_{i+1} \rightarrow -\gamma_i,$$
 (28)

$$\gamma_j \rightarrow \gamma_j, \ j \notin \{i, i+1\}.$$
 (29)

and the relevant unitary representation of this braid group transformation is

<span id="page-9-1"></span>
$$B_{i,i+1} = \exp\left(-\frac{\pi}{4}\gamma_i\gamma_{i+1}\right) = \frac{1}{\sqrt{2}}\left(1 - \gamma_i\gamma_{i+1}\right).$$
 (30)

Similarly, a anti-clockwise exchange instead results in  $\gamma_i \to -\gamma_{i+1}$ ,  $\gamma_{i+1} \to \gamma_i$ , which is described by the operator  $B_{i,i+1}^{-1} = \exp\left(\frac{\pi}{4}\gamma_i\gamma_{i+1}\right) = (1+\gamma_i\gamma_{i+1})/\sqrt{2}$ .

Next, we discuss the effect of bringing one Majorana fermion around another and back to its original position (cf. Fig. 5). Topologically, this is equivalent to two successive exchanges. Thus, the associated operator is given by  $B_{i,i+1}^2 = -\gamma_i \gamma_{i+1}$ , leading to the transformation

$$\gamma_i \to (-\gamma_i \gamma_{i+1}) \, \gamma_i \, (-\gamma_i \gamma_{i+1})^{\dagger} = -\gamma_i, \tag{31}$$

$$\gamma_{i+1} \to \left(-\gamma_i \gamma_{i+1}\right) \gamma_{i+1} \left(-\gamma_i \gamma_{i+1}\right)^{\dagger} = -\gamma_{i+1}. \tag{32}$$

Thus, the operation of bringing one Majorana fermion around another results in introducing a minus sign into each Majorana operator. It is easy to check that the operation generated by  $B_{i,i+1}^3$  is equivalent to that of  $B_{i,i+1}^{-1}$ , while  $B_{i,i+1}^4$  gives rise to the identity operation.

Having obtained the explicit representation of the braid group, we are finally in a position to demonstrate the non-abelian statistics of the Majorana fermions. Exchanges of distinct pairs of Majoranas commute [see Eq. [\(20\)](#page-8-3)]. However, whenever two exchanges involve some of the same Majorana fermions, the braid operators do not commute

$$[B_{i-1,i}, B_{i,i+1}] = \gamma_{i-1}\gamma_{i+1}. \tag{33}$$

The above equation explicitly shows the non-abelian statistics of the Majorana fermions.

### <span id="page-10-0"></span>3.3 A physical realization of Majorana fermions

In this section, we describe a theoretical model whose excitations are these Majorana fermions. To that end, consider again the honeycomb model of Kitaev [\[10\]](#page-16-9) described in Sec. [2.2.](#page-3-0) As we saw in the discussion of the exact solution (see Sec. [2.2\)](#page-4-1), the system can be either in a gapped or gapless phase depending on the choice of the coupling constants Jx, Jy, J<sup>z</sup> [see Eq. [\(11\)](#page-5-1)]. Consider the gapless phase [phase (B) of Fig. [3\]](#page-6-0) and let us choose J<sup>x</sup> = J<sup>y</sup> = J<sup>z</sup> = J for simplicity. In Sec. [2.2,](#page-4-1) we showed that this phase supports gapless fermions [cf. Eqs. [\(9\)](#page-5-2),[\(10\)](#page-5-0)] in the vortex-free sector. Vortices can be included by flipping the signs of the variables α<sup>r</sup> from +1 to −1 [see Eq. [\(6\)](#page-4-2)] and they are gapped in all the phases Ax, Ay, A<sup>z</sup> and B (see also discussion in Sec. [2.2\)](#page-5-3). However, in phase B, because of the gapless fermions, these vortices do not have well-defined exchange statistics *i.e.* the transformation of the quantum state depends on the exact trajectory of the exchange. Thus, a spectral gap needs to be opened before one can talk about exchange statistics.

It can be shown that for this honeycomb lattice, no time-reversal preserving perturbation can open a gap in the B phase (see [\[10\]](#page-16-9) for proof). However, adding a uniform magnetic field (which does not preserve time-reversal symmetry) opens the desired gap. We showed in Sec. [2.2](#page-4-1) that the unperturbed honeycomb model can be mapped to a 2D spinless p-wave superconductor. Here, we will show that adding a magnetic field adds a ip component to the superconductor, in addition to opening a mass gap for the fermions of Sec. [2.2.](#page-4-1) As a consequence, each vortex then has an unpaired Majorana fermion pinned to it. These Majoranas show non-abelian exchange statistics and can be used for topological quantum computation.

Denoting the different components of the magnetic field as hx, hy, hz, we get the total Hamiltonian of the system to be

<span id="page-10-2"></span>
$$H_{\text{tot}} = H + H_{\text{mag}}$$

$$H = -J_x \sum_{x-links} \sigma_j^x \sigma_k^x - J_y \sum_{y-links} \sigma_j^y \sigma_k^y - J_z \sum_{z-links} \sigma_j^z \sigma_k^z,$$

$$H_{\text{mag}} = -\sum_j \left( h_x \sigma_j^x + h_y \sigma_j^y + h_z \sigma_j^z \right). \tag{34}$$

Once again, we calculate the effective Hamiltonian on the vortex-free sector. A third order Schrieffer-Wolff or self-energy calculation yields the effective Hamiltonian to be [\[10\]](#page-16-9):

<span id="page-10-1"></span>
$$H_{\text{mag,eff}} \sim -\frac{h_x h_y h_z}{J^2} \sum_{j,k,l} \sigma_j^x \sigma_k^y \sigma_l^z, \tag{35}$$

where the relevant contributing terms are shown in Fig. [6\(](#page-11-0)a) and its symmetric permutations. Note that exact prefactor is difficult to compute and this crude estimate of the effective Hamiltonian will be sufficient for our purposes. In the perturbation calculation, the total Hamiltonian

![](_page_11_Picture_2.jpeg)

![](_page_11_Picture_3.jpeg)

Fig. 6: *Images from [\[10\]](#page-16-9). (a) Schematic of a contributing term in the effective Hamiltonian due to the magnetic field [see Eq.* [\(35\)](#page-10-1)*]. (b) Schematic of the interactions of the spins in the honeycomb lattice in presence of a magnetic field. In addition to the nearest neighbor interaction, shown as solid arrows, present due to the unperturbed Hamiltonian [Eq.* [\(1\)](#page-3-3)*], the magnetic field gives rise to next-to-nearest neighbor interaction [see Eq.* [\(34\)](#page-10-2)*], shown as dashed arrows. This next-to-nearest neighbor interaction is the crucial ingredient that opens the gap in the spectrum.*

<span id="page-11-0"></span>is then given by

$$\tilde{H}_g = -J_x \sum_{x-links} \sigma_j^x \sigma_k^x - J_y \sum_{y-links} \sigma_j^y \sigma_k^y - J_z \sum_{z-links} \sigma_j^z \sigma_k^z - \frac{h_x h_y h_z}{J^2} \sum_{j,k,l} \sigma_j^x \sigma_k^y \sigma_l^z.$$
(36)

In addition to the nearest neighbor interaction between the spins present in the unperturbed Hamiltonian, the magnetic field adds next-to-nearest neighbor interactions [see Fig. [6\(](#page-11-0)b)]. To analyze this Hamiltonian, we will again use the Jordan-Wigner transformation method [\[17\]](#page-16-16) outlined in Sec. [2.2.](#page-4-1) One could also use the original method of Kitaev [\[10\]](#page-16-9) by mapping each spin to four Majorana fermions. Since most of the steps are similar to what is described in Sec. [2.2,](#page-4-1) we merely state the final effective Fourier-transformed Hamiltonian

$$\tilde{H}_g = \sum_q \left\{ \epsilon_q d_q^{\dagger} d_q + \left( i \frac{\Delta_q + i \tilde{\Delta}_q}{2} d_q^{\dagger} d_{-q}^{\dagger} + h.c. \right) \right\}, \tag{37}$$

where

$$\tilde{\Delta}_q = \frac{4h_x h_y h_z}{J^2} \left\{ \sin(q_y - q_x) + \sin q_x - \sin q_y \right\}$$
(38)

and q, ∆<sup>q</sup> are defined earlier. In the vicinity of the Dirac points of the unperturbed Hamiltonian (qx, qy) = (±π/3, ∓π/3), one can expand the above Hamiltonian and show that H˜ g indeed supports the same Majorana excitations as a 2D spinless p + ip superconducting Hamiltonian. The Majorana edge modes appear at the boundary between regions with hxhyh<sup>z</sup> > 0 and hxhyh<sup>z</sup> < 0 (more on Majorana wavefunctions for a p + ip superconductor can be found in [\[11\]](#page-16-10)). Moreover, vortex excitations in this phase have Majorana zero modes attached to them [\[23\]](#page-16-22). The proof in terms of the Chern number and more details on the superselection sectors and braiding rules can be found in [\[10\]](#page-16-9).

Next we describe how to perform universal quantum computation using these Majorana fermions. We will keep our discussion sufficiently abstract and general so that they can be applied to any physical system that supports these excitations.

# <span id="page-12-0"></span>4 Quantum computing with Majorana fermions

### <span id="page-12-1"></span>4.1 Clifford operations on Majorana qubits

In this section, we describe a computational model based on Majorana fermions. Following [\[24\]](#page-16-23), first we define the computational Hilbert space, in which one can prepare an initial state, a set of unitary operations on this Hilbert space and a set of measurements.

In principle, it is possible to encode a qubit in two Majorana fermions. The ground and excited states of the qubit will then be the unoccupied and occupied states of the fermionic mode of Eq. [\(15\)](#page-7-4). However, due to fermion superselection rules, one cannot prepare this qubit in a superposition of ground and excited states. Therefore, we will redundantly encode a qubit in 4 Majorana fermions. Thus, the computational Hilbert space of n qubits, C 2n , will be encoded in 4n Majorana fermions γ<sup>i</sup> , i = 1, . . . , 4n. We choose the logical subspace to be given by the constraint γ4i−3γ4i−2γ4i−1γ4<sup>i</sup> = −1, i = 1, . . . , n. In this space, the initial state: |0i = |0i ⊗n can be generated by preparing quadruples of these 4n Majorana fermions from vacuum. The connection between the logical Pauli operators of the n qubits and the 4n Majorana fermions can be written as:

$$\sigma_z^{(i)} = -i\gamma_{4i-3}\gamma_{4i-2} \tag{39}$$

$$\sigma_x^{(i)} = -i\gamma_{4i-2}\gamma_{4i-1}, \tag{40}$$

$$\sigma_y^{(i)} = -i\gamma_{4i-3}\gamma_{4i-1}. (41)$$

As shown in Sec. [3.2](#page-8-0) [cf. Eq. [\(30\)](#page-9-1)], the nearest neighbor exchange operations are

$$B_{i,i+1} = \exp\left(-\frac{\pi}{4}\gamma_i\gamma_{i+1}\right). \tag{42}$$

These nearest neighbor exchanges can be composed to give rise to a nonlocal exchange operation

$$B_{i,j} = \exp\left(-\frac{\pi}{4}\gamma_i\gamma_j\right), i \le j - 2 \tag{43}$$

as follows:

$$B_{i,j} = B_{j-1,j} \cdots B_{i+1,i+2} B_{i,i+1} B_{i+1,i+2}^{\dagger} \cdots B_{j-1,j}^{\dagger}. \tag{44}$$

Here, the nonlocal exchange operator Bi,j acts on the Majorana fermions in the following manner

$$B_{i,j}\gamma_k B_{i,j}^{\dagger} = \gamma_k, \text{ if } k \notin \{i, j\},$$

$$= \gamma_j, \text{ if } k = i,$$

$$= -\gamma_i, \text{ if } k = j.$$
(45)

Among the set of measurements, the nearest neighbor fusion process of two Majorana fermions gives rise to a non-destructive projective measurement of the observable

$$F_{i,i+1} = -i\gamma_i\gamma_{i+1}. (46)$$

These, together with the braiding operations, give rise to measurements of any observable Fi,j because

$$F_{i,j} = B_{i+1,j} F_{i,i+1} B_{i+1,j}^{\dagger}. \tag{47}$$

However, performing the aforementioned braiding operations and measurements is not sufficient for performing universal quantum computing. This can be understood as follows. First, using the mapping of the Pauli matrices to Majorana fermions and the conjugating action of the braid operations, it follows that any braid operation maps the group of Pauli operators to itself. Therefore, all the braid operators belong to the Clifford group. Second, the measurement operators involve only Pauli operators. Thus, by Gottesman-Knill theorem [25], any computation performed by the braid operations and measurements described above can be simulated efficiently by a classical computer.

An alternate way to understand the same is in terms of fermionic linear optical quantum computing (FLOQC) [26, 27, 28]. In terms of FLOQC, the initial state is the Fock vacuum, the braid operations are canonical transformations generated by quadratic Hamiltonians and the observables  $F_{i,j}$  are single-mode occupation numbers. Therefore, these operations can be efficiently simulated classically [28]. A similar connection can also be made with linear optical quantum computing with Fock states [29].

As will be shown below, this limitation is overcome by a resource of two ancilla states, denoted by  $|a_4\rangle$  and  $|a_8\rangle$ . The first state,  $|a_4\rangle$ , enables an operation beyond the Clifford group, namely a rotation by  $\pi/8$ . The second state,  $|a_8\rangle$ , enables a nonlinear operation beyond FLOQC, namely, the controlled-phase gate, that can be used to entangle qubits. In what follows, we describe how this is accomplished assuming availability of ideal ancilla states. The case of imperfect ancillas will be alluded to at the end.

### <span id="page-13-0"></span>4.2 Implementation of a controlled-phase gate

In this section, we prove, following [24], that ancilla qubits (composed of eight Majorana modes) in the state  $|a_8\rangle$ , together with single-qubit Clifford operations, can be used to perform a controlled-phase rotation on a system qubit (composed of four Majorana modes), where

$$|a_8\rangle \equiv \frac{1}{\sqrt{2}} (|0,0\rangle + |1,1\rangle). \tag{48}$$

In the first step of the proof, we show that ancilla qubits in the state  $|a_8\rangle$ , together with braiding operations, can be used to make a nondestructive four-Majorana-mode measurement. In the second step, we show that this four-Majorana-mode measurement allows one to make a four-Majorana-mode unitary operation. Note that this four-Majorana unitary gate cannot be accomplished by simple braiding operations. In the third step, we show that this four-Majorana mode unitary gate, together with single-qubit Clifford operations, give rise to the controlled-phase gate.

Consider a qubit, encoded in four Majorana modes  $\gamma_i, i=1,\ldots,4$ , in an arbitrary state  $|\psi\rangle$  and two ancilla qubits, encoded in eight Majorana modes  $\gamma_i, i=5,\ldots,12$ , in the state  $|a_8\rangle$ . First, the circuit in Fig. 7(a) is applied to the joint state  $|\psi\rangle\otimes|a_8\rangle$ . Second, the observables  $T_1=-i\gamma_1\gamma_2, T_2=-i\gamma_3\gamma_4, T_3=-i\gamma_5\gamma_6$  and  $T_4=-i\gamma_7\gamma_8$  are measured. Third, the Clifford gates  $\gamma_2\gamma_9, \gamma_4\gamma_{10}, \gamma_6\gamma_{11}$  and  $\gamma_8\gamma_{12}$  are applied [not shown in Fig. 7(a)]. It can be shown (see [24] for details) that these set of actions amount to projecting  $|\psi\rangle$  to  $1/2(I\pm\gamma_1\gamma_2\gamma_3\gamma_4)|\psi\rangle$ , followed by teleportation of the qubit state encoded in  $\gamma_i, i=1,\ldots,4$  to the four Majorana modes  $\gamma_i, i=9,\ldots,12$  [Fig. 7(b)]. Here, the  $\pm$  depends on the measurement outcomes in the second step. This, shows that an ancilla state  $|a_8\rangle$ , together with single-qubit Clifford operations, gives rise to a four-Majorana projective measurement. This concludes the first step of the proof.

![](_page_14_Picture_2.jpeg)

**Fig. 7:** Images from [24]. (a) Schematic of the circuit needed for implementation of four-Majorana projective measurement. (b) Teleportation circuit, equivalent to the circuit in (a).

<span id="page-14-1"></span>For the second step, consider six-Majorana modes  $\gamma_i, i=1,\ldots,6$  prepared in a state  $|\psi'\rangle$ , such that  $(\gamma_5+i\gamma_6)|\psi'\rangle=0$ . Next, we make a measurement of  $\gamma_1\gamma_2\gamma_4\gamma_5$ , followed by that of  $-i\gamma_3\gamma_5$ . It can be shown that these two measurements, together with single-qubit Clifford gates, gives rise to a unitary rotation of  $\exp(i\pi/4\,\gamma_1\gamma_2\gamma_3\gamma_4)$  (see [24] for details). This concludes the second step of the proof.

For the third step, we need to only show that the four-Majorana mode unitary operation, together with single-qubit Clifford gates, is sufficient to perform a controlled-phase gate. To that end, consider two qubits encoded in the Majoranas  $\gamma_i$ ,  $i=1,\ldots,4$  and  $\gamma_j$ ,  $j=5,\ldots,8$  respectively. Then, the controlled-phase gate is given by:

$$\Lambda(\sigma_z) = \exp\left\{i\frac{\pi}{4}(1 - \sigma_z^{(1)})(1 - \sigma_z^{(2)})\right\},\tag{49}$$

where  $\sigma_z^{(1)}=-i\gamma_3\gamma_4$  and  $\sigma_z^{(2)}=-i\gamma_5\gamma_6$ . Thus,

$$\Lambda(\sigma_z) = e^{i\pi/4} \exp\left(-i\frac{\pi}{4}\gamma_3\gamma_4\gamma_5\gamma_6\right) \exp\left(-\frac{\pi}{4}\gamma_3\gamma_4\right) \left(-\frac{\pi}{4}\gamma_5\gamma_6\right). \tag{50}$$

Therefore, the controlled-phase gate is indeed composed of a four-qubit unitary rotation  $\exp(-i\pi/4 \gamma_3 \gamma_4 \gamma_5 \gamma_6)$ , together with single-qubit Clifford operations. This completes the proof.

# <span id="page-14-0"></span>4.3 Implementation of a $\pi/8$ rotation

In this section, we describe the proof that an ancilla qubit in the state  $|a_4\rangle$  can be used to perform a rotation by  $\pi/8$  on a target qubit in an unknown state following [30, 24], where

$$|a_4\rangle \equiv \frac{1}{\sqrt{2}} (|0\rangle + e^{i\pi/4}|1\rangle).$$
 (51)

Consider a system qubit in an unknown state  $\psi = a|0\rangle + b|1\rangle$ . Thus, the system and ancilla qubits together are in the state  $|\psi\rangle\otimes|a_4\rangle$ . First, perform the joint measurement  $\sigma_z\otimes\sigma_z$  on the two qubits. This can be done since any two-qubit Pauli measurement can be reduced to a single-qubit Pauli measurement using Clifford operations. The outcomes for this measurement  $\pm 1$  appear with probability 1/2, with the final two-qubit state being projected to

$$|\Psi_1^+\rangle = a|0,0\rangle + be^{i\pi/4}|1,1\rangle,$$
 (52)

$$|\Psi_1^-\rangle = ae^{i\pi/4}|0,1\rangle + b|1,0\rangle. \tag{53}$$

Second, apply the controlled-not gate on the two qubits with the system qubit as the control qubit. This can be achieved by a combination of the controlled-phase gate (whose implementation was described above) and the single-qubit Clifford rotations. After this step, the state of the two-qubits is given by:

$$|\Psi_2^+\rangle = (a|0\rangle + be^{i\pi/4}|1\rangle) \otimes |0\rangle,$$
 (54)

$$|\Psi_2^-\rangle = \left(ae^{i\pi/4}|0\rangle + b|1\rangle\right) \otimes |1\rangle.$$
 (55)

In the final step, the ancilla is measured in the {|0i, |1i} basis. An outcome of |0i results in a π/8 rotation on the system qubit, while for an outcome |1i, an extra braid gate |0ih0| + i|1ih1| accomplishes the same.

## <span id="page-15-0"></span>4.4 Robustness to imperfect preparations of ancilla qubits

As explained in Sec. [4.1,](#page-12-1) the topologically protected braiding operations and measurements are insufficient to perform universal quantum computing. To accomplish the latter, one needs to have additional ancilla qubits in certain 'magic' states (|a4i and |a8i). Therefore, these magic states are necessarily generated by non-topological operations which are noisy and unprotected. One way to implement these non-topological operations is to bring two anyons sufficiently close to each other, wait for a desired amount of time and then returning the anyons to their initial positions. Since this operation is noisy, instead of having perfect ancilla qubits in states |a4i and |a8i, one prepares them to some precision, characterized by their fidelity <sup>i</sup> = 1 − ha<sup>i</sup> |ρ|aii, i = 4, 8, where ρ is the density matrix of the ancilla qubit. A major breakthrough in this field was accomplished with the result of [\[24\]](#page-16-23), which proves that for <sup>4</sup> < 0.14 and <sup>8</sup> < 0.38 and perfect topologically protected Clifford operations, one can distill ideal states |a4i and |a8i. The details of the proof lie outside the scope of this set of lecture notes, but the interested reader is invited to consult [\[30,](#page-17-4) [24\]](#page-16-23) for details.

# <span id="page-15-1"></span>5 Conclusion

To summarize, we have presented, in this lecture note, a review of topological quantum computation with Majorana fermions. First, we discussed basic properties of abelian anyons and described a theoretical model that supports these excitations. Second, we discussed the basic properties of Majorana fermions. We discussed their non-abelian exchange statistics and described a theoretical model where these excitations can be found. Third, we discuss how to perform topological quantum computing with the Majorana fermions. We discuss the implementation of single qubit Clifford gates, controlled-Z gate and π/8 gate, which together are sufficient for universal quantum computing.

# <span id="page-15-2"></span>6 Acknowledgments

Discussions with Fabian Hassler, Barbara Terhal and Daniel Zeuch are gratefully acknowledged. A.R. acknowledges the support through the ERC Consolidator Grant No. 682726 and D.P.D. acknowledges the support of the Alexander von Humboldt foundation.

# References

- <span id="page-16-0"></span>[1] P. Shor, *Proceedings of the 37th Symposium on the Foundations of Computer Science*, 56 (1996)
- <span id="page-16-1"></span>[2] D. Aharonov and M. Ben-Or, *arXiv* quant-ph*/9611025* (1996)
- <span id="page-16-2"></span>[3] E. Knill, R. Laflamme and W. Zurek, *Phys. Rev. B* 453, 365 (1998)
- <span id="page-16-3"></span>[4] A. Kitaev, *Annals of Physics* 303, 2 (2003)
- <span id="page-16-4"></span>[5] G. Moore and N. Read, *Nucl. Phys. B* 360, 362 (1991)
- <span id="page-16-5"></span>[6] A. Stern, *Annals of Physics* 323, 204 (2008)
- <span id="page-16-6"></span>[7] C. Nayak, S. H. Simon, A. Stern, M. Freedman and S. Das Sarma, *Rev. Mod. Phys.* 80, 1083 (2008)
- <span id="page-16-7"></span>[8] N. Read and D. Green, *Phys. Rev. B* 61, 10267 (2000)
- <span id="page-16-8"></span>[9] M. A. Levin and X.-G. Wen, *Phys. Rev. B* 71, 045110 (2005)
- <span id="page-16-9"></span>[10] A. Kitaev, *Annals of Physics* 321, 2 (2006)
- <span id="page-16-10"></span>[11] J. Alicea, *Rep. Prog Phys.* 75, 076501 (2012)
- <span id="page-16-11"></span>[12] L. H. Kauffman, *Knots and Physics* (1993)
- <span id="page-16-12"></span>[13] F. Wilczek, *Phys. Rev. Lett.* 48, 1144 (1982)
- <span id="page-16-13"></span>[14] F. Wilczek, *Phys. Rev. Lett.* 48, 1146 (1982)
- <span id="page-16-14"></span>[15] J.J. Sakurai, *Modern Quantum Mechanics* (1993)
- <span id="page-16-15"></span>[16] J. Preskill, *Lecture notes: http://www.theory.caltech.edu/people/preskill/ph219/* (2004)
- <span id="page-16-16"></span>[17] H-D. Chen and Z. Nussinov, *J. Phys. A: Math. Theor.* 41, 075001 (2008)
- <span id="page-16-17"></span>[18] R. Winkler, *Spin-Orbit Coupling Effects in Two-Dimensional Electron and Hole Systems* (2003)
- <span id="page-16-18"></span>[19] E. Dennis, A. Kitaev, A. Landahl and J. Preskill, *Journal of Mathematical Physics* 43, 4452 (2002)
- <span id="page-16-19"></span>[20] D. A. Ivanov, *Phys. Rev. Lett.* 86, 268 (2001)
- <span id="page-16-20"></span>[21] M. Leijnse and K. Flensberg, *Semicond. Sci. Technol.* 27, 124003 (2012)
- <span id="page-16-21"></span>[22] F. Hassler, *arXiv* quant-ph*/1404.0897* (2014)
- <span id="page-16-22"></span>[23] F. J. Burnell and C. Nayak, *Phys. Rev. B.* 84, 125125 (2011)
- <span id="page-16-23"></span>[24] S. Bravyi, *Phys. Rev. A* 73, 042313 (2006)
- <span id="page-16-24"></span>[25] M. Nielsen and I. Chuang, *Quantum Computation and Quantum Information* (2000)

- <span id="page-17-0"></span>[26] E. Knill, *arXiv* quant-ph*/0108033* (2001)
- <span id="page-17-1"></span>[27] B.M. Terhal and D. DiVincenzo, *Phys. Rev. A* 65, 032325 (2002)
- <span id="page-17-2"></span>[28] S. Bravyi, *Quant. Inf. Comput.* 5(3), 216 (2005)
- <span id="page-17-3"></span>[29] E. Knill, R. Laflamme and G. Milburn, *Nature*, 409, 46 (2001)
- <span id="page-17-4"></span>[30] S. Bravyi and A. Kitaev, *Phys. Rev. A* 71, 022316 (2005)