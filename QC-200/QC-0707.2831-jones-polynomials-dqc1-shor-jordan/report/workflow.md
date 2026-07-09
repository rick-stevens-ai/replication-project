# Workflow — Shor & Jordan (2007) DQC1 Jones-polynomial replication

## Timeline (elapsed wall clock: ~25 min)

1. **Fetch paper.** `curl -sL https://arxiv.org/pdf/0707.2831 -o work/paper.pdf`
   → 29 pages, 440 KB.  Verified authors from PDF: **Peter W. Shor** (MIT
   Math) and **Stephen P. Jordan** (MIT CTP). Trust-arxiv-id + verify-authors
   rule satisfied.

2. **Extract prose.** `pdftotext -layout paper.pdf paper.txt` (Poppler) +
   PyMuPDF for a page-boundaried dump. Skimmed for headline claim and
   headline number.
   → Headline: *"Evaluating a certain approximation to the Jones polynomial
      at a fifth root of unity for the trace closure of a braid is a complete
      problem for the one clean qubit complexity class."*
   → Concrete number: SJ Eq. (11):
      V_{b^tr}(A^-4) = (-A)^{3w} · D^{n-1} · Tr(ρ_A(b))
      with A = e^{-i·3π/5}, D = φ (golden ratio).

3. **Install tools.** New venv `work/venv`, `pip install qiskit qiskit-aer
   numpy scipy`. Versions:
      qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.5.1, scipy 1.18.0,
      python 3.14.0, poppler 24.x, PyMuPDF 1.27.2, TeX Live 2026.

4. **Implement Fibonacci path-model representation of B_n**
   (`report/evidence/replicate_shor_jordan.py`):
   - Enumerate admissible paths of length n+1 in {p,*} starting at p
     (no two consecutive *).
   - Build E_i as the block-diagonal projector: on each 2-dim block of
     free middle label, E_i = D · |v⟩⟨v| with |v⟩ = (1/√D)|p⟩ + √(1-1/D)|*⟩,
     so E_i^2 = D E_i.  Verified with D = φ.
   - ρ_A(σ_i) = A E_i + A^{-1} I  (SJ Eq. 12).
   - Verified unitarity of ρ_A(σ_1^3) to ‖U†U-I‖ = 6.5e-16.

5. **Implement Fibonacci-weighted Markov trace** (SJ Eqs. 8–9):
   `f_Tr(U) = (Σ_paths_ending_star U[p,p] + φ · Σ_paths_ending_p U[p,p])
             / (n_star + φ · n_p)`.

6. **Implement Shor-Jordan Eq. 11** and compare against the classical
   right-handed trefoil formula V_{3_1}(t) = -t^-4 + t^-3 + t^-1 at
   t = A^-4 = e^{i·12π/5}. Result: **0 absolute error**. Also verified
   left trefoil (σ_1^-3, mirror) matches V_{3_1}(1/t) to 4.4e-16.

7. **Implement DQC1 Hadamard test on Qiskit-Aer density-matrix simulator.**
   Because Fibonacci rep dim = 3 is not a power of 2, embed
   V = U ⊕ 1 into 4 dims (2 target qubits). Analytic density-matrix
   evolution of |+⟩⟨+|_ctrl ⊗ (I/4)_target through the controlled-V
   circuit gives Tr(V)/4 = 2p_0 - 1 exactly. Recovered Tr(U) = 4·Tr(V)/4 - 1
   matches exact trace to 1.3e-15.

8. **Real shot-based Qiskit Hadamard test**
   (`report/evidence/dqc1_qiskit_shots.py`):
   - AerSimulator, controlled-V via `UnitaryGate.control(1)`.
   - Uniform average over the 4 target computational basis states
     (equivalent to I/4 input), 6000 shots per state per {Re,Im}, so
     24{,}000 total shots per part per braid.
   - Right trefoil: |Δ| = 1.8e-2. Left trefoil: |Δ| = 4.7e-3. Both
     consistent with 1/√N shot noise (expected ~6.5e-3 per component).
   - S^† convention for Im-part verified against a 1-qubit
     diag(1, e^{iπ/3}) sanity unitary.

9. **Write REPORT.tex** (5-page detailed report) → `pdflatex REPORT.tex`
   → REPORT.pdf compiled.

10. **Write open_questions.json**, **workflow.md** (this file),
    **artifacts_summary.md**, **failure_analysis.md**, and **extraction/
    marker.md + nougat.mmd** (with surrogate labels per extraction/README.md).

## Tools / codes / versions

| Tool | Version | Role |
|---|---|---|
| curl | (system) | Fetch paper.pdf from arXiv |
| pdftotext (Poppler) | 24.x | Text extraction (nougat surrogate) |
| PyMuPDF / fitz | 1.27.2.3 | Structured extraction (marker surrogate) |
| Python | 3.14.0 | Language |
| numpy | 2.5.1 | Linear algebra |
| scipy | 1.18.0 | (installed, not directly used) |
| qiskit | 2.5.0 | Circuit building |
| qiskit-aer | 0.17.2 | Shot-based simulator + density-matrix ideal |
| TeX Live | 2026.03.01 | pdflatex REPORT.tex |

## LLM usage

**None** for the numerical replication. The Argo endpoint at
`http://localhost:44497` with key `stevens` was kept in reserve for the
(optional) 3-judge scoring pass, but the reproduction stands on exact
linear algebra + Qiskit density-matrix and shot simulation, so no LLM
judgement was required to establish the verdict.

## Effort estimate

- Reading + math extraction: ~5 min
- Coding Fibonacci rep + Markov trace: ~8 min
- Coding + validating Hadamard test (density-matrix + shots): ~6 min
- Writing REPORT.tex + supporting artifacts: ~6 min
- Total: ~25 min wall clock (single 4-core CherryRd session, no HPC use).

## Compute footprint

- Zero HPC / GPU. All runs on `CherryRd` (macOS 25.3.0, x86_64) CPU only.
- Peak memory ~150 MB. Peak wall time per simulation: <3 s.
