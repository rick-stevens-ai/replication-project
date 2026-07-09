# Workflow — QC-200 replication of quant-ph/9602016

**Paper:** Beckman, Chari, Devabhaktuni, Preskill (1996), *Efficient networks
for quantum factoring*, arXiv:quant-ph/9602016 (CALT-68-2021).
**Host:** CherryRd (macOS 25.3.0, x86_64, Python 3.11).
**Elapsed effort:** ~90 minutes end-to-end (one subagent run).
**Verdict:** REPLICATED (Sec. VII / N=15 headline construction).

## Stage-by-stage workflow

### 1. Resolve + fetch the paper (~2 min)
- `mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9602016-efficient-networks-quantum-factoring/{extraction,report,code,logs,work,report/evidence}`
- `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/9602016` → 490 992 B, 56 pages, PDF 1.4.
- `pdftotext -layout paper.pdf work/paper.txt` (2 976 lines), `pdftotext -raw paper.pdf work/paper_raw.txt` (3 525 lines).
- Author list verified from the PDF's own title page: David Beckman, Amalavoyal N. Chari, Srikrishna Devabhaktuni, John Preskill (Caltech).

### 2. Identify the concrete, reproducible claim (~10 min)
- `grep -n -i "N = 15|38 laser|6 trapped|proof.of.principle|a = 7|a = 11"` on `work/paper.txt` isolated Section VII.
- Read Sec. VII in full (lines 2218–2360). Extracted the four sub-claims that are **actually checkable in ideal statevector simulation**:
  - Eq. (7.3) lookup table for x=7: {0→1, 1→7, 2→4, 3→13}
  - Eq. (7.5) circuit constructing EXP N(7,15) on 6 qubits
  - Eq. (7.6) complexity [6 NOT, 0 CNOT, 4 Toffoli] → 34 pulses on Cirac-Zoller
  - Eq. (7.10) uniform-y prediction after the L=2 QFT
- Noted the discrepancy: the abstract's "38 pulses" number requires the further-optimized EXP N' (Eq. 7.9) using custom Appendix A gates; the first construction (Eq. 7.5) plus 2-Hadamard prep + 6-pulse QFT = 42 pulses.

### 3. Install the simulator (~2 min)
- `python3.11 -m venv .venv && source .venv/bin/activate`
- `pip install -q qiskit qiskit-aer numpy`
- Recorded versions: `qiskit 2.5.0`, `qiskit-aer 0.17.2`, `numpy 2.4.6`.

### 4. Implement the circuit (~15 min)
- Wrote `code/expn_7_15.py` (~13 KB) implementing:
  - `build_expn_7_15(with_superposition)` — exact Eq. (7.5) operator with the rightmost-operator-first convention.
  - `verify_lookup_table()` — exhaustive check of all 4 a inputs.
  - `verify_entangled_state()` — fidelity vs. analytical target of Eq. (7.2).
  - `gate_counts_and_pulses()` — `count_ops()` and Cirac-Zoller pulse arithmetic.
  - `full_shor_period_finding_15_7()` — QFT and y-marginal to check Eq. (7.10).
- Key implementation choice: **right-to-left application** of the operator string. This was the one place a wrong choice would have silently produced a scrambled output. Cross-checked against the paper's Sec. VI ADD conventions (Eq. 6.36).

### 5. Run the simulation (~1 min)
- `python code/expn_7_15.py | tee logs/expn_7_15.log`
- All primary claims (C5, C6, C7, C8, C9, C10, C11) matched exactly.

### 6. Write extractions + report + open questions (~30 min)
- `extraction/marker.md` (5.7 KB) — structured Markdown fallback (Marker not available on the host; documented).
- `extraction/nougat.mmd` (4.0 KB) — LaTeX/Mathpix-flavored fallback (Nougat not available on the host; documented).
- `report/REPORT.tex` (13.9 KB) — full LaTeX report with claims table, method, results-vs-paper table, verdict, and 5 open questions.
- `pdflatex REPORT.tex` → `report/REPORT.pdf` (5 pages, 248 KB).
- `report/open_questions.json` — 5 machine-readable open questions with basis + next_steps.
- `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Tools and versions

| Tool | Version | Role |
| :-- | :-- | :-- |
| Python | 3.11 (Homebrew system) | Interpreter |
| qiskit | 2.5.0 | Circuit construction, statevector sim |
| qiskit-aer | 0.17.2 | (Available if we need shots; here we used analytical statevector) |
| numpy | 2.4.6 | Fidelity computation, target-state construction |
| pdftotext (Poppler) | system default | Paper text extraction (fallback for Marker/Nougat) |
| pdflatex (TeX Live 20260301) | Homebrew | Compile REPORT.tex to REPORT.pdf |
| Marker | **not installed** | Would replace `extraction/marker.md` |
| Nougat | **not installed** | Would replace `extraction/nougat.mmd` |
| Argo LLM proxy | localhost:44497 | Not used this run — the checks were purely deterministic simulation |

## Estimate of work done

- **Reading:** ~20 min (56 pages of a 1996 paper, mostly skimming §II-VI, deep read of §I and §VII).
- **Implementation:** ~15 min for the ~230-line Qiskit script (small because Eq. 7.5 is only 10 gates).
- **Verification runs:** ~1 min total wall (statevector sim on 6 qubits is instantaneous).
- **Writing:** ~30 min for extractions + REPORT + questions + this file.
- **Total:** roughly 90 minutes for a full-cycle, single-paper, single-agent replication.

Because the paper was written in 1996 and predates Qiskit-era abstractions, the
biggest cost was **notation translation** (operator products, big-endian vs.
little-endian, right-to-left convention) rather than any actual quantum
subtlety. The physics/algorithms were fully verified by direct statevector
comparison.
