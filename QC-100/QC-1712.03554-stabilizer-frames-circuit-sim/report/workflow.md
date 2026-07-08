# Workflow — QC-1712.03554 Stabilizer Frames Replication

## 1. Paper acquisition
- Downloaded arXiv:1712.03554 (Garc'ia & Markov, "Simulation of Quantum Circuits via Stabilizer Frames", 10 Dec 2017). No OCR needed (arXiv PDF is text-native); Nougat MMD stub kept at `extraction/nougat.mmd` for pipeline uniformity.

## 2. Claim distillation
- Read Sections 3–6 of the paper. Distilled 6 candidate claims (H1–H6).
- Classified H1–H4 as replicable at n ≤ 10, t ≤ 8 using free open tools (Qiskit + Stim + numpy). Classified H5 (QuIDDPro head-to-head) and H6 (multithreaded Quipu speedup) as non-replicable: neither the QuIDDPro binary nor the Quipu source is publicly available in 2026.

## 3. From-scratch implementation
- Wrote `work/stabilizer_frame.py` (~205 lines Python) implementing:
  - `Branch` = `(n, ops, amp)` where `ops` is a list of Clifford gates preparing the stabilizer state from |0>^n.
  - Clifford ops (H, S, S†, X, Y, Z, CNOT, CZ, SWAP) = list append; O(|F|) per gate.
  - T gate via exact rank-2 decomposition T = e^{iπ/8}(cos(π/8) I – i sin(π/8) Z). Each branch splits into (identity, Z_q) with the two amplitudes.
  - Amplitude sum-out via Qiskit Statevector per branch.
- Wrote `work/run_experiment.py` as driver: deterministic seeds, main sweep + scaling probe + Stim cross-check + JSON dump.

## 4. Reference-simulator setup
- Fresh venv (`.venv`), installed: stim 1.16.0, qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.5.0. Python 3.14.6 on macOS 25.3.0 x64 (m1).
- All free/open-source. No paid endpoints used.

## 5. Execution
- Main sweep: n ∈ {6, 8, 10} × t ∈ {0, 1, 2, 3, 4} = 15 configurations, all seeded.
- Scaling probe: n = 6, t ∈ {5, 6, 7, 8} = 4 configurations.
- Independent Clifford cross-check: t = 0 at n ∈ {6, 8, 10}, three simulators (frame, Qiskit exact, Stim tableau).
- All raw metrics dumped to `report/evidence/results.json`.

## 6. Metric analysis
- Frame size χ: compared to theoretical 2^t; measured exactly for all 19 configurations.
- Amplitude error: max_x |Ψ̂_x − Ψ_x^exact| after global-phase alignment (align at argmax|Ψ_x^exact|), vs 1e-10 tolerance from brief. Worst measured: 1.12e-16.
- Runtime per-T ratios computed for scaling probe.
- Stim vs Qiskit at t = 0 verified as independent code path with known fp32 residual (~6e-9).

## 7. LLM-judge panel
- 3 free Argo endpoints (gpt-4.1, gemini-2.5-pro, gpt-5.2). Each got the raw JSON table + tested-claims list; asked for structured verdict on H1–H4.
- Panel: 2× REPLICATED (high), 1× PARTIAL (medium, encoding-style dissent only).
- Raw responses in `report/evidence/judge.json`.

## 8. Verdict integration
- Majority + all four measured claims green ⇒ REPLICATED.
- Scope caveats (encoding-style deviation, no head-to-head vs QuIDDPro, small t regime, no structured benchmarks) documented in REPORT.md §6 and REPORT.tex "Critique" section.

## 9. Backfill (2026-07-06)
- Added REPORT.tex, open_questions.json (5 items), open_questions_section.tex, workflow.md (this file), artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub.
- No sims re-run. Existing REPORT.md, evidence/, work/ preserved verbatim.
