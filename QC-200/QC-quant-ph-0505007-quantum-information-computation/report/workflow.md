# Workflow — quant-ph/0505007 replication

## Timeline (2026-07-05, single subagent session on CherryRd)

1. **Read the QC wave brief** (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`) and the 8-artifact standard (`REPLICATION_DIR_STANDARD_2026-07-05.md`).
2. **Create the target directory** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0505007-quantum-information-computation/` with `paper.pdf`, `extraction/`, `report/`, `report/evidence/`, `work/`.
3. **Fetch the paper**: `curl -sSL https://arxiv.org/pdf/quant-ph/0505007 -o paper.pdf` → 189,924 bytes, 12-page PDF. Confirmed authors are Tulsi (IISc), Grover (Bell Labs), Patel (CHEP IISc); title is "A New Algorithm for Fixed Point Quantum Search"; venue QIC 2005; v3 last revised 22 Mar 2006.
4. **Extract text**: `pdftotext -layout paper.pdf work/paper.txt` (600 lines).
5. **Skim + identify claim**: the one most-checkable numerical claim is Eq. (6): after q iterations, net error probability equals ε^(2q+1) for every positive integer q. This is a construction the paper proves algebraically; a numpy statevector simulator can verify it exactly.
6. **Environment check**: Python 3.13, numpy 2.4.3 present; qiskit absent (not needed — the register+ancillas fit trivially in a numpy dense simulator at n ≤ 6).
7. **Write the simulator** (`report/evidence/tulsi_grover_patel_fixed_point.py`): explicit dense matrices for the oracle, joint diffusion, and ancilla-2 projectors on a (a1, register n qubits, a2) system with n ∈ {2,3,4} (dims 16, 32, 64). Renormalise outcome-0 branch between iterations (see failure_analysis.md).
8. **Run sweep**: n ∈ {2,3,4}, q ∈ {1,2,3,4}, target index = 0. Wall time < 1 s. Output `report/evidence/results.json`.
9. **Verify**: max |measured − predicted ε^(2q+1)| = 3.3×10⁻¹⁵ (tolerance 10⁻⁹); monotone in q for all n. → **REPLICATED**.
10. **Fallback extractions**: Marker/Nougat unavailable and no central-corpus parse exists for this arXiv id, so produce provenance-headed hand-curated markdown (`extraction/marker.md`) and Nougat-style .mmd (`extraction/nougat.mmd`) from `pdftotext -layout` output, with equations restored from cross-checking the PDF.
11. **Write LaTeX report** (`report/REPORT.tex`) with abstract, claims table, method, results table, verdict; try to compile to PDF (skipped if no LaTeX toolchain).
12. **Write open questions** (`report/open_questions.json` + `report/open_questions_body.tex`, 5 heavy-duty items with next_steps).
13. **Write workflow, artifacts summary, failure analysis** (this file + siblings).

## Tools & versions

| Tool / library      | Version | Purpose                                              |
|---------------------|---------|------------------------------------------------------|
| Python              | 3.13.x  | Simulator language                                   |
| NumPy               | 2.4.3   | Dense complex-vector algebra (statevector simulation)|
| poppler pdftotext   | (system)| Paper text extraction                                |
| curl                | (system)| PDF fetch from arXiv                                 |
| bash / zsh          | (system)| Orchestration                                        |
| pdflatex (optional) | tex-live| Compile REPORT.tex → REPORT.pdf (if available)       |

**Not used:**
- Qiskit / Cirq / PennyLane / Stim — a raw numpy simulator was sufficient and cleaner at these register sizes.
- Marker / Nougat — not installed on CherryRd; used pdftotext + hand curation as documented fallback.
- LLM judges (Argo) — the replication reduces to an exact numerical identity to machine precision, so a deterministic pass/fail test replaces judge scoring.

## Effort estimate

- **Wall-clock**: ~25 min agent time end-to-end (fetch → read → simulator → sweep → report).
- **Compute**: <1 s CPU for the entire sweep (12 cells, dense matrices ≤ 64×64).
- **Lines of Python**: ~185 LOC (`tulsi_grover_patel_fixed_point.py`).
- **Runs executed**: 3 (v1 buggy — bookkeeping error; v2 fixed and verified; final re-run for JSON dump).
- **Documentation LOC**: ~450 lines across REPORT.tex, marker.md, nougat.mmd, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions*.
