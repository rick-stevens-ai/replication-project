# Workflow — arXiv:2110.15958 Hybrid HHL++ replication

## Pipeline (as actually executed)

1. **Fetch paper**
   - Pull arXiv PDF + abstract page to `work/paper.pdf`, `work/abs.html`.
   - `pdftotext` → `work/paper.txt` for grep/section-nav.

2. **Extract testable claims**
   - Read paper.txt end-to-end. Build 7-row claims table (C1–C7).
   - Split into algorithm-level testable (C1–C4: correctness, gate-count
     reduction, qubit-count reduction, fidelity retention) vs.
     hardware-only (C5–C7: novel γ-selection algorithm, Quantinuum
     H-series runs, hardware-measured fidelities in Table 2).
   - QC-100 same-day scope targets C1–C4.

3. **Environment**
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install qiskit qiskit-aer numpy scipy`
   - Verified: qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.5.0 (CPU statevector).

4. **Problem-instance selection**
   - 2×2 Hermitian `A = [[1,-1/3],[-1/3,1]]`, `b = [0,1]`, κ=2.
   - QPE time-scale `t = 3π/4` so eigenvalue phases fall on `{1/4, 1/2}`
     → exactly representable at n_clock=2 (clean fidelity anchor).
   - Classical reference `x = A^{-1} b = [0.375, 1.125]` via
     `numpy.linalg.solve`; normalized for statevector overlap.

5. **Build circuits** (`code/hhl_replication.py`)
   - **Baseline HHL:** QPE (H + controlled-U^{2^k}) → inverse-QFT →
     eigenvalue-inversion (multi-controlled `Ry(2·arcsin(C/λ_k))`) →
     inverse QPE; post-select ancilla=1 AND clock=|0…0⟩.
   - **Hybrid HHL:** classical eigen-decomp `(w, V) = np.linalg.eigh(A)`
     → 2-qubit circuit (sys + ancilla) → V†, two controlled Ry, V;
     post-select ancilla=1. **No QPE, no clock register.**
   - Transpile both to `{cx, u3}` at optimization_level=1.

6. **Run + record**
   - `python3 code/hhl_replication.py 2>&1 | tee logs/run1.log`
   - Extract solution by post-selecting the ancilla=1 branch of the
     full statevector; compute fidelity `F = |⟨x_classical | x_quantum⟩|²`.
   - Write `report/evidence/replication_results.json` (A, b, x_classical,
     per-variant metrics) + `report/evidence/verdict_summary.json`
     (gate/qubit/fidelity comparison + boolean gates).

7. **Verdict + report**
   - Cross-check: fidelity==1.0000 ✓; hybrid CNOT < baseline CNOT ✓;
     hybrid qubits < baseline qubits ✓ → REPLICATED under
     headline-exercised rule.
   - Write `report/REPORT.md` (markdown) + `report/REPORT.tex` (LaTeX).

8. **Backfill (2026-07-06)**
   - Add `REPORT.tex`, `open_questions.json` (5 items), matching
     `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`,
     `failure_analysis.md`, `extraction/nougat.mmd` stub.
   - No re-runs. All existing files preserved.

## Time budget (approximate)

| step                             | wall time |
|----------------------------------|-----------|
| fetch paper + extract claims     | ~2 min    |
| env + install                    | ~2 min    |
| write + debug circuits           | ~4 min    |
| run + record evidence            | <1 min    |
| write REPORT.md                  | ~1 min    |
| **subtotal (original 2026-07-03)** | **~10 min** |
| backfill (2026-07-06)            | ~5 min    |
| **total**                        | **~15 min** |

## Endpoints used

- **Compute:** CherryRd CPU only (Qiskit Aer statevector).
- **Model calls:** none (this was a code+sim replication, not an LLM task).
- **Web:** arXiv only (paper PDF + abstract).
- **Cost:** free-tier only, per standing rule.

## Repro one-liner

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2110.15958-hybrid-hhl-plusplus
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit qiskit-aer numpy scipy
python3 code/hhl_replication.py
```

Expected tail: `VERDICT: REPLICATED`.
