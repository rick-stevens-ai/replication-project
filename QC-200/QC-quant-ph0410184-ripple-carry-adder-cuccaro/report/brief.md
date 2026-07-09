# Brief

Independent replication of the CDKM quantum ripple-carry adder (Cuccaro, Draper,
Kutin, Moulton — arXiv:quant-ph/0410184). We reimplemented both the simple
(Section 2 / Fig 4) and depth-optimized (Section 3 / Fig 5) constructions
from scratch in Qiskit 2.5.0, then exhaustively verified correctness on all
288,896 classical basis inputs for n ∈ {2, 3, 4, 6, 8} (100% pass), confirmed
quantum-superposition action via statevector simulation, and matched the paper's
resource formulas (2n-1 Toffoli, 5n-3 CNOT, 2n-4 NOT, depth 2n+4, 2n+2 qubits)
**exactly** at every tested size. Cross-validated against Qiskit's built-in
Draper QFT adder. **Verdict: REPLICATED.**
