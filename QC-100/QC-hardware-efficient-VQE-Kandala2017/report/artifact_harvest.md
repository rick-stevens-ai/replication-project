# Artifact Harvest

All public artifacts pulled for this replication. Free endpoints only.

| Artifact | Source URL | Local path | Size | Notes |
|---|---|---|---|---|
| arXiv abstract page | https://arxiv.org/abs/1704.05018 | work/arxiv_abs.html | ~45 KB | metadata + abstract |
| ar5iv full-text HTML | https://ar5iv.org/abs/1704.05018 | work/ar5iv.html | ~1.27 MB | full paper body, equations, claim text (no paid PDF/image tools) |
| extracted plain text | (derived from ar5iv.html) | work/paper_text.txt | ~112 KB | stripped text used for claim extraction |
| claim excerpts | (derived) | report/evidence/paper_claim_excerpts.txt | small | verbatim excerpts of the tested claims |

## Software / data provenance
- **Molecular Hamiltonians:** generated locally with PennyLane `qml.qchem.molecular_hamiltonian`
  (PySCF backend, STO-3G basis, Jordan–Wigner mapping), then Z₂-tapered
  (`qml.symmetry_generators` / `qml.taper`, removing 2 spin-parity qubits) to reproduce the
  paper's 2/4/6-qubit encodings. No external Hamiltonian files needed — built from first
  principles from atomic geometries.
- **Active spaces:** H₂ full (4 spin-orbitals → 2 qubits after tapering); LiH
  active_electrons=2, active_orbitals=3 (→ 4 qubits); BeH₂ active_electrons=4,
  active_orbitals=4 (→ 6 qubits). Chosen to hit the paper's stated qubit counts.
- **Exact reference (FCI-in-active-space):** exact lowest eigenvalue of the same tapered
  qubit Hamiltonian (`numpy.linalg.eigvalsh`).

## Tool versions
- Python 3.12.13 (venv)
- PennyLane 0.45.1
- PySCF 2.13.1
- NumPy 2.x / SciPy 1.18
- Simulator: PennyLane `default.qubit`, `diff_method="backprop"` (exact statevector +
  exact gradients). `lightning.qubit` pre-compiled binary unavailable on this host → used
  `default.qubit` (numerically identical, just slower).
