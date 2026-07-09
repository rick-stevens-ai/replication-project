# Workflow — CDKM ripple-carry adder replication

**Paper:** arXiv:quant-ph/0410184 — Cuccaro, Draper, Kutin, Moulton (2004),
"A new quantum ripple-carry addition circuit"
**Set:** QC-200
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0410184-quantum-ripple-carry-adder/`
**Runner:** Ollie (subagent), 2026-07-05
**Host:** CherryRd (macOS, Darwin 25.3.0, Python 3.13)
**Endpoint policy:** free-only. LLM inference: none needed for this replication — verdict is purely
computational (integer gate counts + boolean truth table on a real statevector sim). No LLM-judge call
issued; verdict was decidable by direct comparison.

## Steps

1. **Read the QC wave brief** at `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`
   and confirmed the 8-artifact bar from `REPLICATION_DIR_STANDARD_2026-07-05.md` (referenced there).
2. **Fetch paper.**
   ```bash
   curl -L -o paper.pdf https://arxiv.org/pdf/quant-ph/0410184
   pdftotext paper.pdf paper.txt
   ```
   Verified 9 pages, PDF v1.4. Confirmed authors (Cuccaro, Draper, Kutin, Moulton) from the
   PDF title page — matched the task-line attribution, so no correction.
3. **Extract the headline claims** by skimming `paper.txt`:
   - Optimized adder (Section 3) uses `2n-1` Toffolis, `5n-3` CNOTs, `2n-4` NOTs, depth `2n+4`,
     valid for `n >= 2` (with Figure 5 pseudocode valid for `n >= 4`).
   - Uses `2n+2` qubits total (n for A, n for B, 1 ancilla X, 1 output Z).
   - Ancilla returns to `|0>` at end.
   - Correctness: outputs `|a> |a+b mod 2^n>` in the A, B registers; high carry XOR'd into Z.
4. **Install Qiskit.**
   ```bash
   python3 -m venv ~/.venvs/qc-adder
   source ~/.venvs/qc-adder/bin/activate
   pip install qiskit qiskit-aer numpy
   # Qiskit 2.5.0, qiskit-aer, numpy 2.x
   ```
5. **Implement the adder in `code/cdkm_adder.py`.**
   - `MAJ(qc, c, b, a)` — 2 CNOTs + 1 Toffoli exactly as Figure 1.
   - `UMA_2cnot(qc, c, b, a)` — Figure 2a (Toffoli + 2 CNOTs).
   - `UMA_3cnot(qc, c, b, a)` — Figure 2b for parallelism experiments.
   - `simple_adder(n)` — Figure 4 (MAJ ripple → carry copy → UMA unripple).
   - `optimized_adder(n)` — Figure 5 pseudocode transcribed line-for-line; requires `n >= 4`.
   - Helpers `count_gates` and `circuit_depth`.
6. **Verify in `code/verify_adder.py`.**
   For each `n ∈ {3, 4, 5}` and each input triple `(a, b, z) ∈ [0, 2^n)^2 × {0, 1}`:
   - Prep circuit with X gates for the classical input.
   - Compose with adder, compute `Statevector.from_instruction(full)` (exact — no shots).
   - Assert single-basis-state output, decode bits, compare to the specification.
   - Log gate counts + depth.
   Dump everything to `report/evidence/results.json`.
7. **Run.**
   ```bash
   source ~/.venvs/qc-adder/bin/activate
   python code/verify_adder.py report/evidence/results.json
   ```
   Runtime ~2 seconds for all 2688 test cases.
8. **Author artifacts.**
   - `report/REPORT.tex` — section-by-section report with claims table, method,
     results-vs-paper, verdict, and open questions.
   - `report/open_questions.json` — 5 non-trivial questions grounded in this replication.
   - `report/workflow.md` — this file.
   - `report/artifacts_summary.md` — inventory + genuine critique.
   - `report/failure_analysis.md` — honest friction log (near-empty since replication was clean).
   - `extraction/marker.md` + `extraction/nougat.mmd` — pdftotext fallback (Marker/Nougat not installed).
9. **Attempt PDF compile** with `pdflatex` if available (see `report/artifacts_summary.md`
   for outcome).

## Tools & versions

| Tool                     | Version                    | Where |
|--------------------------|----------------------------|-------|
| Python                   | 3.13 (Homebrew)            | /usr/local/bin/python3 |
| Qiskit                   | 2.5.0                      | ~/.venvs/qc-adder |
| qiskit-aer               | (latest via pip 2026-07-05)| ~/.venvs/qc-adder |
| numpy                    | 2.x (pulled by qiskit)     | ~/.venvs/qc-adder |
| poppler-utils (pdftotext)| system                     | /usr/local/bin/pdftotext |
| pdflatex                 | see failure_analysis.md    | if present |
| curl                     | system                     | for arXiv fetch |

## Work estimate

- Fetch + skim: ~5 min
- Qiskit install: ~1 min
- Adder implementation: ~15 min (two variants, careful about qubit ordering)
- Verification script + run: ~5 min
- Report + open questions + artifact write-up: ~15 min

Total: ~40 min of active agent time. Compute cost: negligible (single-thread
statevector on 12-qubit circuits, all runs < 2s).
