# Brief — Hardware-efficient VQE (Kandala et al. 2017)

**What:** Independent replication of the classically-simulable core of Kandala et al.,
*"Hardware-efficient variational quantum eigensolver for small molecules and quantum
magnets"* (Nature 549:242, 2017; arXiv:1704.05018). We implement the paper's
hardware-efficient ansatz (interleaved single-qubit Euler rotations + entangling CNOT
network — the noiseless analog of the paper's cross-resonance U_ENT) and run VQE on a
**noiseless statevector simulator** (PennyLane `default.qubit`, exact-gradient Adam) for
H₂ (2 qubits), LiH (4 qubits), and BeH₂ (6 qubits), using the paper's qubit encoding
(Jordan–Wigner + Z₂ spin-parity tapering removing exactly 2 qubits, giving the paper's
2/4/6 qubit counts).

**Why:** The paper's hardware results depend on a specific superconducting device, but its
central *algorithmic* claims — (C2) the hardware-efficient ansatz reaches **chemical
accuracy (~0.0016 Ha)** versus exact/FCI along the dissociation curve, and (C3) the
**critical circuit depth grows with molecule size** — are, by the authors' own numerical
methodology, classically simulable for these small systems. That simulable core is what we
independently reproduce here on free compute, comparing to exact diagonalization of the
same qubit Hamiltonian (the "exact curve" the paper plots against).
