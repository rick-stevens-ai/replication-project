# Brief — MC-VQE electronic transitions (Parrish et al. 2019)

**What:** Independent replication of the reproducible classical-simulator core of
Parrish et al., "Quantum Computation of Electronic Transitions using a
Variational Quantum Eigensolver" (MC-VQE), PRL 122, 230401 (2019); arXiv 1901.01234.

**Why:** MC-VQE is a multistate, contracted VQE that computes ground + several
excited-state energies and oscillator strengths on the same footing, applied to
an ab-initio exciton model (a spin-lattice Hamiltonian). The paper's central
quantitative claims — that a single-layer MC-VQE reproduces FCI excitation
energies to tens of μeV and oscillator strengths to ≪1%, while CIS blue-shifts /
mis-predicts intensities by 10%+ — are pure classical statevector simulation
(the paper itself uses their in-house "Quasar" simulator, no hardware). This is
exactly the kind of reproducible core the wave targets.

**How:** Re-implemented from scratch in NumPy/SciPy: exciton Hamiltonian (Eq. 8 +
supplement element formulas) as an N-qubit spin model; exact FCI by sparse
diagonalization of the full 2^N space; CIS in the (N+1)-dim singles manifold;
MC-VQE with matryoshka CIS-reference state prep, SO(4) two-body entanglers on the
Hamiltonian connectivity graph, state-averaged L-BFGS optimization from a
zero-entanglement guess, and classical diagonalization of the interference-built
contracted Hamiltonian. Two systems: N=8 linear H-aggregate BChl-a stack (CIS
known to fail) and N=18 cyclic LH2 B850 ring (Hilbert dim 262,144). Free
endpoints only; heavy N=18 run on uicgpu.
