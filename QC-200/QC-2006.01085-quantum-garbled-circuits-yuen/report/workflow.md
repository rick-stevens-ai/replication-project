# Workflow — Independent Replication of arXiv:2006.01085 (Brakerski & Yuen)

## Narrative
1. Fetched paper PDF from arXiv, extracted plain text via `pdftotext`, skimmed
   Sections 1–2 to identify the reproducible core (computation-by-teleportation
   for Clifford gates + classical Yao garbling as the sub-primitive).
2. Recognized the paper is a **theoretical construction**: no benchmark number
   to reproduce. Elected to instantiate the two building blocks that admit a
   concrete numerical demonstration.
3. Built a fresh Python 3.14 venv in `work/venv/`; installed Qiskit 2.5.0,
   NumPy 2.5.1, and `cryptography` (for AES-GCM in the Yao baseline).
4. Wrote `report/evidence/yao_and_gate.py`: Yao's 2-input AND gate with
   AES-256-GCM per-wire labels; the authentication tag on GCM plays the role
   of the classical "point-and-permute" tag (only the correct pair of keys
   decrypts a row cleanly). Verified 4/4 rows.
5. Wrote `report/evidence/qgc_clifford_teleport.py`: the Clifford slice of the
   QGC construction. Implemented the Pauli-frame update rules for H and S from
   the paper's identity `G X^a Z^b = X^{a'} Z^{b'} G` (mod global phase), plus
   the CNOT rule `CNOT (X^a Z^b ⊗ X^c Z^d) CNOT = X^a Z^{b⊕d} ⊗ X^{a⊕c} Z^d`.
   Verified correctness (fidelity ≈ 1) on H|0>, HSH|0>, and CNOT on |0>|+>.
   Verified statistical hiding (uniform Pauli-mask average = maximally mixed
   state) numerically to distance ~1e-16.
6. Wrote `report/evidence/qiskit_crosscheck.py`: recomputed both tests using
   `qiskit.quantum_info` (Statevector, DensityMatrix, Operator) instead of raw
   numpy. Two libraries had to agree; they did (fidelity ≈ 1, hiding distance
   ≈ 5.5e-17).
7. Compiled artifacts and wrote LaTeX report + failure analysis + open
   questions (heavy-duty, replication-grounded).

## Tools / codes / versions
| Tool | Version | Use |
|---|---|---|
| Python | 3.14 | interpreter |
| NumPy | 2.5.1 | density-matrix arithmetic |
| Qiskit | 2.5.0 | independent cross-check via `quantum_info` |
| qiskit-aer | 0.17+ | (installed but not needed at this scale) |
| cryptography | latest | AES-256-GCM for Yao wire-label encryption |
| pdftotext (poppler) | system | PDF -> text extraction |
| curl | system | fetching arXiv PDF |

## Scripts written (this replication)
- `report/evidence/yao_and_gate.py` (~90 LOC): classical Yao GC baseline.
- `report/evidence/qgc_clifford_teleport.py` (~250 LOC): QGC Clifford slice.
- `report/evidence/qiskit_crosscheck.py` (~65 LOC): Qiskit independent check.

## Runs executed
1. `python yao_and_gate.py` — 4/4 truth-table rows correct.
2. `python qgc_clifford_teleport.py` — all 5 sub-tests pass to machine precision.
3. `python qiskit_crosscheck.py` — matches numpy results.

## Effort estimate
- **Compute time:** ~5 s total across all three scripts (toy scale).
- **Wall clock (agent):** ~4 minutes end-to-end (fetch + install + code + report).
- **LOC written by agent:** ~400 lines Python + ~280 lines LaTeX + ~200 lines
  markdown/json (workflow + failure + summary + open questions).
- **Human/agent steps:** ~15 tool calls.

## What was NOT done (out of budget)
- Full T-gate magic-state gadget (Section 5–6 of the paper).
- Nougat/Marker parsing (extraction files are pdftotext copies; central
  Marker/Nougat corpus does not yet contain this arXiv id).
- Explicit garbled-circuit size scaling study.
- LaTeX -> PDF compile (no local `latexmk` verified in path within budget).
