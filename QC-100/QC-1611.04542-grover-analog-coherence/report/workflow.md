# Workflow — QC-1611.04542-grover-analog-coherence

## Provenance
- **Paper:** Anand & Pati, arXiv:1611.04542v1 [quant-ph], 14 Nov 2016.
- **Replicator:** OpenClaw QC-100 subagent (Rick Stevens wave).
- **Date:** original run 2026-07-03; artifact backfill 2026-07-06.
- **Host:** CherryRd (macOS 25.3.0). No LLM calls at any step. All numbers direct from Qiskit statevector simulator.
- **Endpoints used:** none (offline compute only). Free tier hygiene: not applicable — no model calls made.

## Step-by-step

1. **Fetch paper.**
   ```
   curl -sL -o work/paper.pdf https://arxiv.org/pdf/1611.04542
   pdftotext -layout work/paper.pdf work/paper.txt
   ```

2. **Environment.**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install qiskit qiskit-aer numpy matplotlib
   ```
   Resolved: Qiskit 2.5.0, Python 3, numpy, matplotlib.

3. **Read paper.** Extracted three primary claims (C1–C3):
   - C1: Grover peak at k_opt ≈ (π/4)√N.
   - C2: C_l1(ρ) → 0 iff P → 1.
   - C3: C_r(ρ) → 0 iff P → 1.
   C4 (2-qubit concurrence tracks dP/dk) and C5 (n-party monogamy) noted but out of scope.

4. **Implement.** `code/grover_coherence.py`:
   - Standard Grover oracle (X-mask → H → MCX → H → X-mask) marking `|0…0>`.
   - Standard diffuser (H⊗ⁿ · X⊗ⁿ · (H·MCX·H) · X⊗ⁿ · H⊗ⁿ).
   - `Statevector.from_instruction` per k.
   - For each k, compute P_success, C_l1 = (Σ|c_i|)² − Σ|c_i|² (pure-state formula), C_r = H({|c_i|²}) bits.

5. **Run.** `python code/grover_coherence.py` for n = 3, 4, 5. Wall-clock <5 s.

6. **Plot.** `python code/plot_tradeoff.py` → three-panel `report/evidence/coherence_success_tradeoff.png` (P, C_l1, C_r vs k for each n).

7. **Compare.** Sim k_peak vs closed-form k_opt; P_sim vs sin²((2k+1)arcsin(1/√N)); C_l1(k_peak)/C_l1(0) trend vs n → confirms C1, C2, C3.

8. **Write report.** REPORT.md; REPORT.tex (this backfill wave).

## Compute budget
- CPU-only, single-core, statevector simulator. No GPU. No HPC.
- Total wall-clock: ~5 s runtime + report writing.

## Repro instructions
```
cd QC-1611.04542-grover-analog-coherence
source .venv/bin/activate                     # or recreate as in step 2
python code/grover_coherence.py               # writes report/evidence/grover_coherence_n{3,4,5}.json + summary.json
python code/plot_tradeoff.py                  # writes report/evidence/coherence_success_tradeoff.png
```

## Non-goals (this workflow does NOT do)
- No noise-model / decoherence sweep (see open question 1).
- No Farhi–Gutmann continuous-time analog Hamiltonian evolution (see open question 2).
- No two-qubit reduced density matrix or concurrence calculation (C4).
- No n-party monogamy inequality verification (C5).
- No comparison to real analog-platform hardware datasets (see open question 5).
