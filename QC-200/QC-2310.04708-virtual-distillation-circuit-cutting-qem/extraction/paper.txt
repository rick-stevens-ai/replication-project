                                              Enhancing Virtual Distillation with Circuit Cutting
                                                       for Quantum Error Mitigation
                                                               Peiyi Li                                  Ji Liu                           Hrushikesh Pramod Patil
                                                        NC State University                 Argonne National Laboratory                      NC State University
                                                         Raleigh, NC, USA                        Lemont, IL, USA                             Raleigh, NC, USA
                                                          pli11@ncsu.edu                           ji.liu@anl.gov                             hpatil2@ncsu.edu

                                                                                Paul Hovland                                          Huiyang Zhou
                                                                       Argonne National Laboratory                                 NC State University




arXiv:2310.04708v2 [quant-ph] 10 Oct 2023
                                                                            Lemont, IL, USA                                        Raleigh, NC, USA
                                                                           hovland@mcs.anl.gov                                      hzhou@ncsu.edu

                                               Abstract—Virtual distillation is a technique that aims to miti-     and then perform measurements on these copies [10]. By
                                            gate errors in noisy quantum computers. It works by preparing          utilizing the information obtained from these measurements,
                                            multiple copies of a noisy quantum state, bridging them through        one can estimate
                                            a circuit, and conducting measurements. As the number of copies                       the expectation value with respect to the state
                                            increases, this process allows for the estimation of the expectation   ρM / Tr ρM , where M represents the number of copies. As
                                            value with respect to a state that approaches the ideal pure           M increases, this state approaches the closest pure state to
                                            state rapidly. However, virtual distillation faces a challenge in      ρ exponentially fast [9]. By effectively approaching a pure
                                            realistic scenarios: preparing multiple copies of a quantum state      state, the technique enables a more accurate estimation of the
                                            and bridging them through a circuit in a noisy quantum computer        expectation value, thereby enhancing the reliability of quantum
                                            will significantly increase the circuit size and introduce excessive
                                            noise, which will degrade the performance of virtual distillation.     computations.
                                            To overcome this challenge, we propose an error mitigation strat-         Virtual distillation holds great potential as a technique to
                                            egy that uses circuit-cutting technology to cut the entire circuit     mitigate the detrimental effects of noise in quantum systems.
                                            into fragments. With this approach, the fragments responsible for      However, for near-term quantum devices, several obstacles can
                                            generating the noisy quantum state can be executed on a noisy          hinder the effectiveness of virtual distillation. First, the need
                                            quantum device, while the remaining fragments are efficiently
                                            simulated on a noiseless classical simulator. By running each          for 2-qubit gates, which are essential for “bridging” multiple
                                            fragment circuit separately on quantum and classical devices and       copies of a quantum state, can lead to a significant increase
                                            recombining their results, we can reduce the noise accumulation        in the number of required SWAP gates. Due to the limited
                                            and enhance the effectiveness of the virtual distillation technique.   qubit connectivity in near-term quantum devices, additional
                                            Our strategy has good scalability in terms of both runtime             swap gates must be inserted before applying 2-qubit gates that
                                            and computational resources. We demonstrate our strategy’s
                                            effectiveness through noisy simulation and experiments on a real       involve non-adjacent qubits. Unfortunately, both these inserted
                                            quantum device.                                                        SWAP gates and the 2-qubit gates used to “bridge” multiple
                                               Index Terms—Quantum Error Mitigation, Virtual Distillation,         state copies introduce significant noise, substantially com-
                                            Quantum Circuit Cutting                                                promising the reliability of the virtual distillation process.
                                                                                                                   Second, the process of preparing multiple copies of a cir-
                                                                   I. I NTRODUCTION                                cuit is vulnerable to crosstalk errors [6]. Crosstalk between
                                               Quantum computation holds immense promise for solving               instructions can corrupt the quantum state when multiple in-
                                            complex problems beyond the reach of classical computers.              structions are executed simultaneously [4]. Virtual distillation
                                            However, quantum systems are highly susceptible to errors              can be more susceptible to crosstalk between instructions,
                                            caused by various noise sources. These errors can severely             given that the preparation of multiple state copies signif-
                                            degrade the performance and reliability of quantum algo-               icantly increases the likelihood of parallel gate executions
                                            rithms. Therefore, it is essential to develop techniques that          on nearby qubits. Furthermore, the virtual distillation circuit
                                            can mitigate the effects of errors and enhance the quality of          can be more susceptible to detection crosstalk (or readout)
                                            quantum computation.                                                   crosstalk [6] because the preparation of multiple state copies
                                               In the quest to mitigate errors and enhance the reliabil-           and the subsequent measurements introduce a large number
                                            ity of quantum computations, various techniques have been              of measurement operations. As program size expands and the
                                            proposed. One notable technique, known as virtual distilla-            number of measurement operations increases, it becomes more
                                            tion [9], [18] or error suppression by derangement [10], aims          susceptible to readout crosstalk [8].
                                            to achieve exponential suppression of errors when estimating              To improve the reliability and effectiveness of virtual distil-
                                            the expectation value of an observable. The main idea behind           lation on near-term quantum devices, further noise mitigation
                                            virtual distillation is to prepare multiple copies of a noisy          techniques are needed. Reference [10] has explored zero-noise
                                            quantum state, denoted as ρ, “bridging” them through a circuit         extrapolation [1], [2] to mitigate the effects of noise of the
virtual distillation circuits. However, they primarily focused      By computing ⟨O⟩mitigated , virtual distillation approximates the
on demonstrating the performance of zero-noise extrapolation        expectation value with respect to the dominant eigenstate
in a depolarizing noise model. In a realistic scenario where        |ψ1 ⟩ ⟨ψ1 |. Although the dominant eigenstate |ψ1 ⟩ ⟨ψ1 | is not
various noise sources exist in the virtual distillation circuit,    necessarily the desired state |ψ⟩ ⟨ψ|, theoretical analysis [11]
applying zero-noise extrapolation becomes challenging. The          shows the mismatch between these two states is exponen-
presence of multiple noise sources complicates the process of       tially smaller than the build-up of the other erroneous states
finding an accurate curve-fitting model, rendering zero-noise       |ψk ⟩ ⟨ψk |k̸=1 . This approach enables the mitigation of errors
extrapolation less effective in practice.                           and provides an enhanced estimation of quantum observables.
   This limitation highlights the need to develop alternative
noise mitigation strategies that are better suited for real-world   B. Circuit Implementation of Virtual Distillation
                                                                                                                                
scenarios. In this paper, we propose noise mitigation using           To estimate the expectation value of the state ρM / Tr ρM ,
a quantum circuit-cutting strategy for virtual distillation on      Ref. [9] utilize the following equation:
quantum devices. Our proposed approach involves cutting the                         Tr OρM
                                                                                              
                                                                                                  Tr Oi S (M ) ρ⊗M
                                                                                                                    
virtual distillation circuit into smaller fragments and running                                 =                             (4)
                                                                                     Tr (ρM )      Tr S (M ) ρ⊗M
them independently. By doing so, our proposed scheme can
mitigate a significant amount of noise, and our experiments         Here, Oi represents the observable O acting on an arbitrary
demonstrate the effectiveness of our strategy in enhancing the      subsystem i, while S (M ) denotes the cyclic shift operator
performance of virtual distillation on real quantum devices.        applied to M systems.
   This paper is organized as follows: In Section II, we provide       This equation provides an expression for estimating the
a review of the virtual distillation protocol and the circuit       desired expectation value by relating it to the trace of the ob-
structure typically used in this protocol, then we analyze the      servable Oi S (M ) ρ⊗M and the trace of S (M ) ρ⊗M . To estimate
overhead of a virtual distillation circuit on real devices and      these two traces, it is necessary to prepare M copies of the
highlight the motivation for our work. Section III introduces       state ρ. For practical implementation on near-term quantum
our quantum circuit-cutting strategy and discusses its potential    devices, we will focus on the case of preparing two copies of
for enhancing virtual distillation. Section IV describes the        the state.
experimental setup, including the benchmarks, evaluation met-          The circuit implementation involves two main steps. First,
rics, and noise models. Experimental results and performance        M copies of the state ρ need to be prepared. In the context
analysis will be presented in Section V. Finally, Section VI        of preparing two copies, it is represented as ρ⊗2 . The second
concludes the paper.                                                step is to measure the expectation value of ρ⊗2 with respect
            II. BACKGROUND AND MOTIVATION                           to the observables S (M ) and Oi S (M ) . Reference [9] discusses
                                                                    two methods for measuring these observables. One approach
A. Theory of Virtual Distillation
                                                                    involves the introduction of ancilla qubits, where the √ ancilla
   This section reviews the theory of Virtual Distillation, and     qubits are prepared in the state |+⟩ = (|0⟩ + |1⟩)/ 2 and a
the notation used is based on Ref. [9], [18]. When the state        sequence of controlled-SWAP gates are applied to “bridge” the
preparation process is affected by incoherent noise, the desired    M copies of ρ. Alternatively, another approach eliminates
pure quantum state, represented as |ψ⟩ ⟨ψ|, can be distorted        the requirement for ancilla qubits. This method relies on
into a mixed state, described by the density matrix:                diagonalizing gates designed to diagonalize the observables
                          d
                          X                                         S (M ) and Oi S (M ) . These diagonalizing gates “bridge” the M
                     ρ=         λk |ψk ⟩ ⟨ψk |               (1)    copies of ρ and allow measurement of these observables in
                          k=1                                       the computational basis. We can then estimate the expectation
In Equation (1), λk represents the probability  of the system in    values based on the measurement outcomes. The virtual distil-
                                   P
the state |ψk ⟩, where λk ≤ 1 and k λk = 1. For simplicity,         lation circuit with diagonalizing gate implementation is shown
we assume that the first state |ψ1 ⟩ ⟨ψ1 | in the mixture is the    in Fig. 1.
dominant eigenstate, with λ1 being the dominant eigenvalue.            In practical scenarios, the execution of controlled-SWAP
   To mitigate the effects of noise and restore the purity of       gates on near-term quantum devices often introduces substan-
the state, the mixed state ρ can be exponentiated M times,          tial noise, rendering the implementation of virtual distillation
normalizing ρM yields:                                              using ancilla qubits impractical. As a result, the remainder of
                            Pd                                      this paper focuses on the virtual distillation implementation
                                    M
                   ρM         k=1 λk |ψk ⟩ ⟨ψk |                    by utilizing diagonalizing gates.
                          =        d
                                                             (2)
                 Tr (ρM )                 M
                                P
                                   k=1 λk                           C. Virtual Distillation Circuit Complexity on Device with
   The mitigated expectation value, denoted as ⟨O⟩mitigated , is    Limited Connectivity
obtained by evaluating
                      the trace of the observable O with the          According to the findings in Ref. [9], the implementation of
state ρM / Tr ρM :                                                  the virtual distillation circuit requires only a single additional
                                           
                                 Tr OρM                             layer of diagonalizing gates. Consequently, the number of extra
                 ⟨O⟩mitigated :=                             (3)    gates needed for virtual distillation exhibits a linear growth
                                  Tr (ρM )
     Original
      Circuit




                                                       physical circuit on device

                logical circuit
                                                                                                        q0       RY                                RY                                                    RY
                                                   Original                                                       [0]                               [3]                                                   [6]
                                      Mapping       Circuit
     Original
   Original
                                     to physical
                                       device                                                           q1       RY                                              RY                                                  RY
      Circuit                                                                                                     [1]                                                [4]                                                 [7]
    Circuit

                                                   Original                                             q2       RY                                              RY                                                  RY
                                                    Circuit                                                       [2]                                                [5]                                                 [8]

                Diagonalizing gate

                                                                                    Fig. 2: Example of a 3 qubit RealAmplitudes circuit with 2
Fig. 1: The virtual distillation circuit with two copies of the                     repetitions and circular entanglement.
original circuit and the diagonalizing gates. When mapping the
virtual distillation circuit to a device with limited connectivity,
extra SWAP gates are introduced to move the diagonalizing
                                                                                                       2500       CNOT gate count for                                       14000       CNOT gate count for
gates to adjacent qubits with coupling.                                                                           the original circuit
                                                                                                                                                                            12000
                                                                                                                                                                                        the original circuit
                                                                                                       2000       additional CNOT gates                                                 additional CNOT gates



                                                                                     CNOT gate count                                                      CNOT gate count
                                                                                                                  introduced in constructing the                                        introduced in constructing the
relative to the number of qubits in the circuit. Furthermore,                                                     virtual distillation circuit                              10000       virtual distillation circuit
                                                                                                       1500                                                                  8000
Ref. [10] suggests that the preparation of the quantum state |ψ⟩                                       1000                                                                  6000
typically necessitates O[a(N )N ] gates, where a(N ) represents                                         500
                                                                                                                                                                             4000
the computation depth. However, in scenarios where the com-                                                                                                                  2000
                                                                                                          0 10          20     30        40        50                           0 10       20       30          40         50
putational problems extend beyond a constant-depth circuit,                                                      Qubit number of the circuit                                           Qubit number of the circuit
the gate count in the primary computation increases at a faster                     (a) Circuit transpiled using coupling (b) Circuit transpiled using coupling
rate than O(N ). Consequently, as the computation is scaled                         map of fully connectivity             map from ibm_sherbrooke
up, the additional gate count required for constructing the
                                                                                    Fig. 3: Change of circuit size with respect to the number of
virtual distillation circuit becomes relatively less significant.
                                                                                    qubits. Note that the total CNOT gate count in the virtual
   Nevertheless, it is crucial to acknowledge that the afore-
                                                                                    distillation circuit is equal to two times the CNOT gate count in
mentioned study does not take into account the inherent
                                                                                    the original circuit, plus the additional CNOT gates introduced
connectivity limitations of near-term quantum devices. The
                                                                                    during the construction of the diagonalizing gates.
qubits in the superconducting quantum computers [3], [7] and
the neutral atom array quantum computers [15] are not fully                         tion approach to examine the impact of additional SWAP gates
connected. While the existing trapped-ion devices featuring                         on circuit size. To evaluate the overhead associated with ap-
tens of qubits offer full connectivity, the challenge lies in de-                   plying virtual distillation on a near-term device, we transpiled
signing a scalable QCCD (Quantum Charge-Coupled Device)                             both the original circuits and the circuits after applying the
architecture [13] that comprises thousands of qubits. Such an                       virtual distillation approach. The transpilation process utilized
architecture would consist of multiple fully-connected clusters;                    a coupling map derived from the 127-qubit IBM machine,
however, the inter-connection across these clusters remains                         named ibm_sherbrooke. This machine adopts a heavy hex
limited. The connectivity limitation in the quantum devices re-                     lattice topology commonly used in IBM quantum machines.
quires the insertion of additional SWAP gates before applying                       The optimization level is set to 3 to minimize the number
the diagonalizing gates. Fig. 1 shows an example of mapping                         of additional inserted SWAP operations. The resulting CNOT
a 6-qubit virtual distillation circuit to a physical device with                    gate counts after transpilation are presented in Fig. 3b. For
linear connectivity. Three SWAP gates are inserted for qubit                        comparison purposes, we also included the circuit translation
routing. In the worst-case scenario, each diagonalizing gate                        results using a fully connected coupling map in Fig. 3a.
requires at most N − 1 SWAP gates to move the two logical                              We systematically increased both the number of qubits
qubits to adjacent physical qubits. Therefore, the upper bound                      (ranging from 10 to 50) and the alternating layers of rotation-
of the number of extra gates introduced by virtual distillation                     Y gates and CNOT gates (ranging from 10 to 50) to modify
is O(N 2 ). As the circuit size grows, the number of these                          the gate complexity of the original circuit. Figure 3a illustrates
additional gates increases at a rate faster than linear, resulting                  the ideal scenario with a fully connected coupling map, where
in a substantial overhead.                                                          the additional gate count required for constructing a virtual
   In order to assess the impact of these additional SWAP gates                     distillation circuit grows linearly with respect to the number of
in the virtual distillation circuit, we employed a RealAmpli-                       qubits, resulting in a relatively smaller overhead compared to
tudes circuit from Qiskit library [20]. The RealAmplitudes                          the increase in gate count of the original circuit. However, by
circuit is commonly utilized as an ansatz circuit in chemistry                      visualizing the changes in circuit size on a limited connected
applications and consists of alternating layers of rotation-Y                       coupling map from the real quantum device through Fig.
gates and CNOT gates. An example of the RealAmplitudes                              3b, it becomes evident that as the circuit scales up, the
circuit can be seen in Fig. 2.                                                      number of additional gates required for constructing the virtual
   In our study, we utilized the RealAmplitudes circuit as the                      distillation circuit remains substantial, introducing significant
original circuit for state preparation, varying the number of                       overhead. This observation highlights the fact that running
qubits and layers. Subsequently, we applied the virtual distilla-                   the virtual distillation circuit on a limited connectivity device
significantly increases circuit complexity, thereby undermining                                      distillation circuit facilitates the identification of good cutting
the effectiveness of the virtual distillation approach. In light of                                  points.
this, we propose a solution for enabling the application of the
                                                                                                     B. Applying Quantum Circuit Cutting in Virtual Distillation
virtual distillation approach on near-term quantum devices by
employing circuit-cutting techniques to reduce gate complexity                                           As discussed in Section II-C, implementing virtual distilla-
significantly.                                                                                        tion circuits on real devices has two challenges: 1) Additional
                                                                                                      SWAP gates are inserted before applying the diagonalizing
            III. ENHANCING VIRTUAL DISTILLATION                                                       gates. 2) Both the inserted SWAP gates and the diagonalizing
   In this section, we will delve into enhancing the virtual                                          gates are subject to noise and may hinder the virtual distillation
distillation circuit by utilizing quantum circuit-cutting tech-                                       result.
niques. We begin by introducing the theory behind quantum                                                These two challenges can be effectively addressed by
circuit cutting. Subsequently, we explain how this method can                                         cutting the virtual distillation circuit into fragments of the
be applied to the virtual distillation circuit, highlighting the                                      diagonalizing gates and fragments of the original circuit that
advantages of our approach.                                                                           prepares the noisy quantum state. First, by independently
                                                                                                      executing these smaller fragments, the requirement for in-
A. Quantum Circuit Cutting                                                                            serting SWAP operations is significantly reduced. Second,
  This section provides a basic overview of Quantum Circuit                                           since the size of each diagonalizing gate does not increase
Cutting [5], [12], [17]. In Ref. [12], it was shown that an                                           with the number of qubits in the original circuit, we can
arbitrary quantum state represented by a density matrix ρ, can                                        efficiently simulate the diagonalizing gates on a noise-free
be decomposed as:                                                                                     classical simulator. This simulation aids in mitigating the
                      1 X                                                                             noise introduced by the diagonalizing gates and enhances
                 ρ≃          M ⊗ trn (Mn ρ)                (5)                                        the overall performance. Liu et al. introduced the Simulated
                      2
                              M ∈B
                                                                                                      Quantum Error Mitigation (SQEM) framework [16] where
Here, B represents the basis of self-adjoint 2 × 2 matrices,                                          they leveraged circuit cutting to simulate the Pauli Check
where for convenience, we can select B ≡ {X, Y, Z, I} as the                                          Sandwiching circuit [19] for quantum error mitigation.
basis. The symbol trn denotes a partial trace operation with                                             Ideally, our objective is to cut out all the diagonalizing
respect to qubit n, while Mn denotes the action of the operator                                       gates simultaneously; however, the number of subcircuit copies
M on qubit n, with the operator I acting on the remaining                                             grows exponentially with the number of cuts. To overcome this
qubits.                                                                                               limitation, we leverage the fact that diagonalizing gates are
                                   Three copies of subcircuit j       Four copies of subcircuit k     only applied pairwise and propose a pairwise circuit cutting
                                                    Measure in
                                                     X-basis
                                                                                 Y
                                                                                                      scheme. The proposed scheme is demonstrated in Fig. 5. The
                                              X                                                       original circuit for generating the noisy quantum state is an
                                                    Measure in
                                                     Y-basis                     Y                    n-qubit circuit and we prepare two copies of the noisy state
        X        Y                            X                   +                                   in the virtual distillation circuit.
                                                    Measure in                   Y
                                                     Z-basis                                             • First, the virtual distillation circuit is executed on a
                                              X
                                                                                 Y                            physical device to acquire the unmitigated noisy output
                                                                                                              distribution Pum (q0 q0′ q1 q1′ ...qn−1 qn−1     ′
                                                                                                                                                                   ).
        Fig. 4: Circuit cutting for a single-qubit      circuit.
                                              Physical device                                            • Then,
                                                                                                    Classical simulator we will replicate the virtual distillation circuit
                                                            Measure in X,
   Each term in the equation (5) can be dividedY, Z basis         into two                                    n times to obtain Mitigated n    mitigated
                                                                                                                                         Pairwise distribution pairwise distributions
                                                                                                                                           ′
          OriginalThe first component, trn (Mn ρ), corresponds to
components.                                                                                                   P (q0 q0 ), ..., P (qn−1 qn−1     ). Since the goal is to obtain
           Circuit
the measurement      of the observable Mn while the system is in                                              pairwise distribution, each replica only consists of gates
the state ρ. This portion of the circuit can be referred to as                                                that have dependency with the measurement, i.e., two
subcircuit j. The second component involves the initialization                                                identical subcircuits of the original circuit and a diagonal-
                                              Physical device
or preparation of the eigenstates of M . This segment can be                                        Classical izing
                                                                                                              simulatorgate. The diagonalizing gate is cut out and simulated

denoted as subcircuit k. By following this approach,             the equa-                                    on a noise-free simulator, while the rest of the                    circuit is
                                                                                                                                                                           Mitigated
                                                           Measure in X,
                                                                                                                                                   Bayesian           virtual distillation
          Original
tion demonstrates      how   a quantum  state can   be   reconstructed
                                                             Y, Z basis                                       executed on a physical device.                              distribution
           Circuit                                                                                                                                 Probability
after a cut is made on one of its qubits, as illustrated in Fig. 4.                                      • Lastly, to obtain the final                   mitigated result, we need
                                                                                                                                                Recombination
This technique forms the core of quantum circuit cutting.                                                     to update the unmitigated noisy output distribution
   As shown in Fig. 4, cutting one wire results
                                              Physical in  three copies
                                                       device                                                 Pum (q0 q0′ q1 q1′ ...qn−1 qn−1′
                                                                                                                                                  ) with mitigated pairwise dis-
                                                                                                                                                             ′
of the subcircuit j and four copies of the subcircuit k. It is                                                tributions
                                                                                                     Classical simulator
                                                                                                                             P (q  q
                                                                                                                                 0 0  ), ..., P (q n−1 qn−1 ). We utilize the re-
important to    highlight that the total number of copies exhibits
          Original                                                                                            combination method described in [16] to merge these
           Circuit                                                                                            results and produce the overall mitigated output.
exponential     growth as the number of cuts made to        Measureain X,circuit
                                                             Y, Z basis
increases. Therefore, an efficient scheme with circuit-cutting                                           To optimize the circuit and reduce noise, we utilize the
needs to find good cutting points that limit the total number of                                      following optimizations in the scheme. Firstly, when executing
cuts in the circuit. While identifying suitable cutting points in                                     the part on the classical simulator, we can reuse the results
general poses challenges, the inherent structure of the virtual                                       of the diagonalizing gate if the separated diagonalizing gates
                                            Physical device                  Classical simulator
                                                         Measure in X,
                                                          Y, Z basis
                                                                                                           Mitigated Pairwise distribution

        Original
         Circuit                                                         +

                                            Physical device
                                                                             Classical simulator

                                                         Measure in X,
        Original                                          Y, Z basis                                                                               Mitigated
         Circuit                                                         +                                                      Bayesian
                                                                                                                                Probability
                                                                                                                                              virtual distillation
                                                                                                                                                  distribution
                                                                                                                              Recombination

           ..                                     ..                                  ..
            .                                      .                                   .
                                            Physical device

                                                                             Classical simulator
        Original
         Circuit
                                                         Measure in X,
                                                          Y, Z basis
                                                                         +

                                                                              Unmitigated virtual distillation distribution




Fig. 5: Demonstration of applying quantum circuit-cutting to the virtual distillation circuit. The transparent gates in the circuit
are the ones that have no dependency on the diagonalizing gates.


have the same matrix. This approach saves computation time                     the device, increasing the likelihood of successful execution
and resources. Secondly, for the part executed on the quantum                  and achieving desired results.
device, we eliminate any gates that are not predecessors of the                   To obtain the final mitigated output, the outcomes from
separated diagonalizing gate. This pruning process results in a                each step, which correspond to individual pairs of qubits in
more compact and less noisy circuit that is customized for the                 the circuit, need to be combined. The recombination method
specific quantum device. As shown in Fig. 5, the transparent                   described in [16] provides an effective approach for merging
gates in the diagram are the ones that have no dependency on                   these results. By leveraging classical post-processing tech-
the diagonalizing gates and can be eliminated.                                 niques, we can integrate the outcomes from each step and
                                                                               generate the overall mitigated output.
C. Advantage of Applying Quantum Circuit Cutting in Virtual                       In summary, applying the quantum circuit cutting technique
Distillation                                                                   in virtual distillation brings several advantages, including effi-
   The application of the quantum circuit cutting technique                    cient parallel execution, noise reduction, and accurate outcome
in virtual distillation offers several notable advantages. These               recombination. These advantages contribute to improving the
advantages contribute to enhancing the performance and ef-                     performance, reliability, and scalability of virtual distillation,
fectiveness of the virtual distillation circuit.                               making it a promising approach for near-term quantum de-
   First, by dividing the virtual distillation circuit into multiple           vices.
parallel steps, we enable efficient execution of the circuit. This
parallelization allows us to take advantage of the available                   D. Complexity Analysis
computational resources and accelerate the overall processing                     The proposed scheme is scalable with respect to the number
time. Furthermore, by reusing the results of the diagonalizing                 of qubits N in the original circuit. The total time is directly
gate on the classical simulator, we reduce the computational                   proportional to the number of runs performed on the physical
overhead associated with redundant calculations. Additionally,                 device. As we replicate the virtual distillation circuit N times
by removing irrelevant gates that are not predecessors of                      and the circuit cutting results in three copies for each replica,
the separated diagonalizing gate, we eliminate unnecessary                     the total number of hardware runs is O(3N ). The runtime can
operations, resulting in a more concise and streamlined cir-                   be reduced since the hardware execution of these copies can
cuit. This pruning process mitigates the impact of noise and                   be parallelized.
significantly improves the quality of the mitigated pairwise                      Regarding the computational complexity associated with
                                        ′
distributions P (q0 q0 ), ..., P (qn−1 qn−1 ). Also, by eliminating            simulating diagonalizing gates, the size of the diagonalizing
non-essential gates, we create a circuit that is optimized for the             gate is determined by the number of copies M in the virtual
connectivity and operational constraints of the quantum device.                distillation setup. Since a large value of M significantly
This customization improves the circuit’s compatibility with                   increases the size of the virtual distillation circuit, it is
common practice to set M to 2, and the diagonalizing gates        The median CNOT error is 7.936e−3, the median gate time is
become two-qubit gates. Consequently, the classical simulation    346.667 ns, the median readout error is 1.200e−2, the median
complexity is bounded by a constant value O(C). Since the         T1 is 120.385 µs, and the median T2 is 138.652 µs.
number of diagonalizing gates in the circuit is N and the            In order to provide a more realistic evaluation of our
gates are simulated independently, the classical computational    approach, we incorporated additional noise sources in our
complexity is O(N ). Notably, many diagonalizing gates are        experiments. Specifically, we modeled the ZZ crosstalk for
identical so we can reuse the simulation results to reduce the    CNOT gates and the readout crosstalk. By including these
classical computational overhead.                                 noise sources, we aimed to accurately capture the impact they
                                                                  have on the performance and effectiveness of different error
         IV. E XPERIMENTAL M ETHODOLOGY
                                                                  mitigation approaches.
A. Benchmark
                                                                     To model the ZZ crosstalk for CNOT gates, we adopted
   To evaluate the effectiveness of our approach, we con-         a method similar to the one described in [14]. This involved
ducted experiments using the Variational Quantum Eigensolver      introducing additional RZZ gates in the circuit whenever there
(VQE) algorithm to solve the MaxCut problem. We utilized          were CNOT gates in the same layer and in adjacent positions.
the RealAmplitudes circuit as Ansatz for the VQE algorithm,       We set the angle θ of the inserted RZZ gate to −π/3.5 based
which consists of alternating rotation Y gates and CNOT gates,    on the Ref. [14].
e.g., Fig. 2. In our experiments, we set the alternating layer       Readout crosstalk refers to the phenomenon where the
number of the rotation Y gates and CNOT gates to 2. The           measurement of one qubit can be affected by the state of
circuit parameters were fixed to the optimal values obtained      neighboring qubits due to unintended coupling [6]. The basic
using the ‘COBYLA’ optimizer on a noise-free simulator. The       noise model only considers the single-qubit readout errors
problem Hamiltonian for the MaxCut problem is defined as:         which assumes that the readout noise acts independently
                          X 1                                     on each individual qubit. To model the readout crosstalk,
                   H=             (1 − Zi Zj )             (6)    we introduced a 2-qubit readout error matrix for pairs of
                                2
                         (i,j)∈E
                                                                  neighboring qubits. In our simulations, we set the readout error
where Zi is the Pauli Z operator acting on qubit i. E is the      matrix as:
set of the graph edges in the MaxCut problem.                                                                   
                                                                                  0.991 0.003 0.003 0.003
B. Evaluation Criteria                                                           0.003 0.991 0.003 0.003
                                                                                                                
                                                                                 0.003 0.003 0.991 0.003
   To assess the effectiveness of different error mitigation
approaches, we calculate the absolute error of the expectation                    0.003 0.003 0.003 0.991
value for the problem Hamiltonian compared to the noise-free      E. Comparison with Extrapolation Approach
expectation value. This allows us to quantify the deviation of
each error mitigation approach from the noise-free solution.          We conducted a comparison with the zero-noise extrapola-
To assess the gate complexity of different error mitigation       tion approach [1], [2] commonly employed for quantum error
approaches, we transpile the circuit into basis gates and count   mitigation. The extrapolation technique aims to estimate the
the number of CNOT gates. This provides a measure of the          expectation value of an observable by extrapolating measure-
gate operations required by each error mitigation approach,       ments obtained from circuits at different noise levels.
offering a comparison of the circuit complexities.                    In the case of the extrapolation approach for virtual dis-
                                                                  tillation, we followed a similar methodology as described in
C. Experiment Platform                                            Ref. [10], where we scaled up the diagonalizing gates in the
   Our experiments were conducted using the Qiskit frame-         virtual distillation circuit for the extrapolation process. This
work v0.39.0. We utilized both a real quantum machine, a 27-      scaling was specifically applied to the diagonalizing gates, as
qubit ibm_hanoi, and a simulator, Qiskit Aer simulator, in        they are often subject to noise and can limit the precision of
our experiment. The simulator allows us to simulate quantum       the virtual distillation approach in realistic scenarios.
circuits under both noise-free and noisy conditions. We set           In our experiments, we choose three scale factors 1, 3, and
the shot number to 10,000 for both the simulator and the real     5, for linear extrapolation.
quantum machine.                                                      The implementation of our approach and the comparison
                                                                  results with the extrapolation approach are publicly available
D. Noise Models
                                                                  at https://github.com/peiyi1/project error mitigation.
   Qiskit offers noise models that incorporate certain sources
of noise from real quantum devices, and we use the noise                                 V. EVALUATION
model from real quantum device ibm_hanoi as our basic
noise model. This basic noise model considers factors such as         In this section, we compare different error mitigation
gate errors, gate time, T1 and T2 relaxation times, and readout   approaches under different noise models. Then we run ex-
errors for each qubit. The parameter of this noise model is       periments on real machines to show that our approach works
based on the calibration data taken on September 27, 2023.        for real quantum devices.
A. Comparison under Different Noise Models                            mitigating errors in quantum circuits.
   To evaluate the noise robustness of our circuit-cutting ap-        B. Real Device Results
proach, we conducted a comparative analysis with different               To validate the practical applicability of our approach,
error mitigation approaches across various noise models. The          we conducted experiments on a 27-qubit quantum device
results of these comparisons are presented in Table I and             ibm_hanoi. The results for a 4-qubit and a 6-qubit VQE
Table II, which display the simulation outcomes for the 4-            circuit are presented in Table III. Our circuit-cutting approach
qubit and 6-qubit VQE circuits, respectively.                         outperforms other error mitigation methods, highlighting the
   To showcase the circuit optimization achieved through our          effectiveness of our approach in real-world quantum comput-
approach, we compared the number of CNOT gates in different           ing environments.
error mitigation techniques. Our focus on the CNOT gate count            In addition to the experiments reported in Table III, we also
is motivated by the fact that 2-qubit gates typically introduce       performed experiments on a 10-qubit VQE circuit. However,
more gate noise in comparison to single-qubit gates and the           despite applying circuit cutting, the resulting subcircuits still
CNOT gate is a widely used 2-qubit gate in superconduct-              contained a substantial number of gates, leading to significant
ing systems. After applying the circuit-cutting technique, the        noise that prevented us from obtaining adequately mitigated
CNOT gate count decreases compared with other mitigation              pairwise distributions required for updating the noisy out-
approaches. By eliminating unnecessary gates, our approach            put distribution effectively. Consequently, we were unable
reduces the overall gate count, thereby mitigating the impact of      to achieve satisfactory results. This further emphasizes the
noise. This reduction in gate count leads to improved pairwise        scalability and practical limitations of existing error mitigation
distributions, ultimately enhancing the accuracy of the output        approaches for larger quantum circuits.
distributions in the presence of noise.
                                                                                             VI. CONCLUSION
   Table I and Table II also provide the expectation value
and the absolute error obtained by different approaches under             In this paper, we propose a circuit-cutting based scheme
various noise models. The results demonstrate that as the             aimed at enhancing the virtual distillation technique on near-
complexity of the noise model increases, the error mitigation         term quantum devices. We observe the virtual distillation’s
effectiveness of the virtual distillation approach diminishes.        performance is hampered by the limited connectivity and
However, our circuit-cutting approach maintains a high level          the noisy operations in the near-term quantum devices. To
of error mitigation across different noise models. This achieve-      address these challenges, we propose an efficient and effective
ment is attributed to the division of the circuit into smaller        scheme that involves cutting the virtual distillation circuit into
fragments, which greatly reduces the occurrence of CNOT               fragments and simulating the diagonalizing gates on noise-
gates executing at the same layer and in adjacent positions,          free simulators. This approach allows us to obtain high-
thereby eliminating a significant portion of the ZZ crosstalk         quality pairwise distributions that can be utilized to update
noise. Table I and Table II display the count of RZZ gates            the original noisy distribution. Our experiments on a noisy
when modeling the ZZ crosstalk for CNOT gates, indicating             simulator and real device show that our proposed approach
that our circuit-cutting approach introduces less ZZ crosstalk,       outperforms both the canonical and the extrapolation-enhanced
whereas the original virtual distillation approach introduces a       virtual distillation methods.
substantial amount of ZZ crosstalk. Furthermore, the tables                               ACKNOWLEDGEMENTS
also illustrate the efficient mitigation of readout crosstalk            We thank the anonymous reviewers for their valuable com-
achieved by our circuit-cutting approach. This is achieved by         ments. This work is partly funded by NSF grants 1818914
reducing the number of measurement operations in the circuit.         (with a subcontract to NC State University from Duke Univer-
Conversely, the original virtual distillation circuit requires the    sity), and 2120757 (with a subcontract to NC State University
preparation of at least two copies of the circuit, resulting in an    from the University of Maryland). It is also supported by
amplification of readout crosstalk due to the increased number        the U.S. Department of Energy, Office of Science, National
of qubits and measurement operations.                                 Quantum Information Science Research Centers.
   When comparing our circuit-cutting approach with the
extrapolation approach, we observe that for smaller virtual                                     R EFERENCES
distillation circuits, as illustrated in Table I, the extrapolation    [1] Y. Li and S. C. Benjamin, “Efficient variational quan-
method indeed exhibits effective error mitigation. However,                tum simulator incorporating active error minimization,”
as shown in Table II, as the circuit size increases and the                Phys. Rev. X, vol. 7, p. 021 050, 2 Jun. 2017.
complexity of the noise model grows, the effectiveness of the          [2] K. Temme, S. Bravyi, and J. M. Gambetta, “Error
extrapolation approach decreases. This is because the presence             mitigation for short-depth quantum circuits,” Phys. Rev.
of multiple noise sources complicates the establishment of an              Lett., vol. 119, p. 180 509, 18 Nov. 2017.
accurate curve-fitting model for extrapolation. In contrast, our       [3] J. Kelly, Preview of bristlecone, Google’s new quan-
circuit-cutting approach consistently achieves error reduction             tum processor, 2019. [Online]. Available: https : / / ai .
even in the presence of more complex noise sources. This                   googleblog . com / 2018 / 03 / a - preview - of - bristlecone -
highlights the effectiveness and reliability of our approach in            googles-new.html.
                                                            TABLE I: Simulation results for the 4-qubit VQE circuit
                                                            gate count                                               expectation value                       absolute error
       error mitigation method                 CN OT gate count RZZ gate count                         basic1    basic+GCT 2 basic+GCT+RCT 3    basic   basic+GCT basic+GCT+RCT
             no mitigation                            17                   0                          -2.6594       -2.656             -2.637   0.313      0.316            0.335
          virtual distillation                        63                  16                          -2.7925       -2.696             -2.681   0.180      0.276            0.291
 virtual distillation + extrapolation              63,71,796           16,24,32                       -3.003        -2.911             -2.895   0.031      0.061            0.077
 virtual distillation + circuit cutting          11,14,17,177           0,0,0,0                       -2.914        -2.914             -2.913   0.058      0.058            0.059
 1 basic denotes the basic noise model that Qiskit offers that incorporates noise from real quantum device ibm hanoi
 2 basic + GCT denotes the basic noise model, which includes the ZZ crosstalk for CNOT gates
 3 basic + GCT + RCT denotes the basic noise model that includes both the ZZ crosstalk for CNOT gates and the readout crosstalk
 4 The ideal expectation value for the original circuit in a noise-free simulator is -2.972
 5 The expectation value for the virtual distillation circuit with noise-free diagonalizing gates is -2.965
 6 The numbers 63, 71, and 79 represent the CNOT gate count for the extrapolation circuit with noise scales of 1, 3, and 5, respectively.
 7 The numbers 11,14,17 and 17 represent the CNOT gate counts for the virtual distillation circuit when cutting and measuring each pair of qubits in the circuit, respectively.



                                                            TABLE II: Simulation results for the 6-qubit VQE circuit
                                                            gate count                                              expectation value                        absolute error
       error mitigation method                 CN OT gate count RZZ gate count                          basic     basic+GCT basic+GCT+RCT       basic   basic+GCT basic+GCT+RCT
             no mitigation                             31                   0                         -4.278 1      -4.300            -4.269    0.644      0.622            0.653
          virtual distillation                        117                  36                          -4.5622      -4.222            -4.199    0.360      0.699            0.723
  virtual distillation+ extrapolation            117,129,141            36,56,72                       -4.914       -4.506            -4.482    0.008      0.416            0.440
 virtual distillation + circuit cutting        16,18,21,26,28,31       2,0,0,8,4,0                     -4.842       -4.785            -4.783    0.080      0.137            0.139
 1 The ideal expectation value for the original circuit in a noise-free simulator is -4.922
 2 The expectation value for the virtual distillation circuit with noise-free diagonalizing gates is -4.903




       TABLE III: Real device results for the VQE circuit                                                   [11]     B. Koczor, “The dominant eigenvector of a noisy quan-
                                  4-qubit circuit                         6-qubit circuit                            tum state,” New Journal of Physics, vol. 23, no. 12,
  error mitigation
       method
                        expectation value    absolute error     expectation value    absolute error                  p. 123 047, 2021.
   no mitigation            -2.540 1                0.432           -3.635 2                1.287           [12]     M. A. Perlin, Z. H. Saleem, M. Suchara, and J. C.
 virtual distillation        -1.964                 1.008            -2.659                 2.263
 virtual distillation
                             -2.101                 0.871            -3.002                 1.920
                                                                                                                     Osborn, “Quantum circuit cutting with maximum-
  + extrapolation
 virtual distillation                                                                                                likelihood tomography,” npj Quantum Information,
                             -2.747                 0.225            -4.498                 0.424
  + circuit cutting                                                                                                  vol. 7, 2021.
 1 The ideal expectation value for the original circuit in a noise-free simulator is -2.972
 2 The ideal expectation value for the original circuit in a noise-free simulator is -4.922                 [13]     J. M. Pino, J. M. Dreiling, C. Figgatt, et al., “Demon-
 [4]      P. Murali, D. C. Mckay, M. Martonosi, and A. Javadi-                                                       stration of the trapped-ion quantum ccd computer ar-
          Abhari, “Software mitigation of crosstalk on noisy                                                         chitecture,” Nature, vol. 592, no. 7853, pp. 209–213,
          intermediate-scale quantum computers,” in ASPLOS,                                                          2021.
          ACM, Mar. 2020.                                                                                   [14]     M. Ahsan, S. A. Z. Naqvi, and H. Anwer, “Quantum
 [5]      T. Peng, A. W. Harrow, M. Ozols, and X. Wu, “Sim-                                                          circuit engineering for correcting coherent noise,” Phys.
          ulating large quantum circuits on a small quantum                                                          Rev. A, vol. 105, p. 022 428, 2 Feb. 2022.
          computer,” Physical Review Letters, vol. 125, no. 15,                                             [15]     T. Graham, Y. Song, J. Scott, et al., “Multi-qubit en-
          Oct. 2020.                                                                                                 tanglement and algorithms on a neutral-atom quantum
 [6]      M. Sarovar, T. Proctor, K. Rudinger, K. Young, E.                                                          computer,” Nature, vol. 604, no. 7906, pp. 457–462,
          Nielsen, and R. Blume-Kohout, “Detecting crosstalk                                                         2022.
          errors in quantum information processors,” Quantum,                                               [16]     J. Liu, A. Gonzales, and Z. H. Saleem, Classical sim-
          vol. 4, p. 321, Sep. 2020.                                                                                 ulators as quantum error mitigators via circuit cutting,
 [7]      J. Chow, O. Dial, and J. Gambetta, IBM quantum                                                             2022. arXiv: 2212.07335 [quant-ph].
          breaks the 100-qubit processor barrier, 2021. [Online].                                           [17]     G. Uchehara, M. Medvidovic, and A. Apte, Quantum
          Available: https://research.ibm.com/blog/127- qubit-                                                       circuit cutting, 2022. [Online]. Available: https : / /
          quantum-processor-eagle.                                                                                   pennylane . ai / qml / demos / tutorial quantum circuit
 [8]      P. Das, S. Tannu, and M. Qureshi, “JigSaw: Boosting                                                        cutting.
          fidelity of NISQ programs via measurement subsetting,”                                            [18]     P. Vikstål, G. Ferrini, and S. Puri, Study of noise in
          in MICRO, ACM, Oct. 2021.                                                                                  virtual distillation circuits for quantum error mitigation,
 [9]      W. J. Huggins, S. McArdle, T. E. O’Brien, et al.,                                                          2022. arXiv: 2210.15317 [quant-ph].
          “Virtual distillation for quantum error mitigation,” Phys.                                        [19]     A. Gonzales, R. Shaydulin, Z. H. Saleem, and M.
          Rev. X, vol. 11, p. 041 036, 4 Nov. 2021.                                                                  Suchara, “Quantum error mitigation by pauli check
[10]      B. Koczor, “Exponential error suppression for near-term                                                    sandwiching,” Scientific Reports, vol. 13, no. 1, p. 2122,
          quantum devices,” Phys. Rev. X, vol. 11, p. 031 057, 3                                                     2023.
          Sep. 2021.                                                                                        [20]     Realamplitudes, https://qiskit.org/documentation/stubs/
                                                                                                                     qiskit.circuit.library.RealAmplitudes.html.
