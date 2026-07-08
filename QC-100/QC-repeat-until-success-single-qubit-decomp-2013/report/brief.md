# Brief — arXiv:1311.1074 (Paetznick & Svore 2014, RUS)

The paper introduces Repeat-Until-Success (RUS) circuits: non-deterministic
Clifford+T circuits that use ancillas + measurement to implement a target
single-qubit unitary *exactly* on the "success" measurement outcome (with
identity or an easy Clifford on failure), often at dramatically lower T-count
than any ancilla-free approximation. We independently reproduced two of the
paper's smallest and most cited database circuits — Fig. 8 (2 T-gates,
implements `(I + i√2 X)/√3` with success prob 3/4) and Fig. 9 (4 T-gates,
implements `V3 = (I + 2iZ)/√5` with success prob 5/8) — via Qiskit 2.5.0
statevector simulation. Both circuits reproduced the claimed target unitary
with process fidelity 1.0 (up to a global phase) and the claimed success
probability to ~1e-15. LLM judge (Argo `argo:gpt-5.2`, free endpoint):
**REPLICATED**, agreement 0.92.
