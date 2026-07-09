# Replication workflow

**Paper**: arXiv:quant-ph/0503205 — "A different kind of quantum search", Lov K. Grover, 2005.
**Target dir**: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0503205-different-kind-quantum-search/`
**Executor**: Ollie (subagent) on host CherryRd, 2026-07-05.
**LLM inference used**: none (numeric result is machine-exact; no judge invoked).

## Step-by-step

1. **Fetch paper**
   ```bash
   curl -sL https://arxiv.org/pdf/quant-ph/0503205 -o paper.pdf     # 138 KB
   pdftotext         paper.pdf work/paper.txt                       # for reading
   pdftotext -layout paper.pdf work/paper.layout.txt                # for the nougat fallback
   ```

2. **Read paper, extract the headline claim.** The core testable statement is:
   for the recursion `U_{m+1} = U_m R_s U_m^dag R_t U_m` (with `R_s, R_t` = pi/3 phase shifts on `|s>` and `|t>`), starting from `U_0 = U` with `|U_ts|^2 = 1 - eps`,
   ```
   |U_{m,ts}|^2 = 1 - eps^(3^m)     with query cost q_m = (3^(m+1) - 1)/2.
   ```
   Also: standard Grover oscillates in iteration count k, whereas the pi/3 variant is monotone in m ("fixed point").

3. **Install Qiskit in a fresh venv** (no --break-system-packages).
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install --quiet qiskit numpy matplotlib
   # -> qiskit 2.5.0, numpy 2.5.1
   ```

4. **Implement + run the statevector reproduction.**
   Script: `report/evidence/grover_pi3_fixedpoint.py`.
   - Builds `U` = Walsh-Hadamard on n qubits via `QuantumCircuit.h` + `Operator(qc)`.
   - Builds `R_s`, `R_t` as diagonal 2^n × 2^n operators with a single entry `exp(i * pi/3)`.
   - Standard Grover: iterates `Q = U R_0^(pi) U^dag R_t^(pi)` k=0..12 on N=16, marked idx 5.
   - Pi/3 fixed-point: matrix-composes `U_m R_s U_m^dag R_t U_m` recursively for m=0..3 on N=16 and N=64.
   - Compares sim P against theory `1 - eps^(3^m)`.
   - Writes `standard_grover_probs.json`, `pi3_fixedpoint_probs.json`, `convergence_data.csv`, `convergence.png`, `verdict.json`.

   ```bash
   .venv/bin/python report/evidence/grover_pi3_fixedpoint.py
   # OVERALL_PASS: true — max theory diff 1.4e-14 (N=16), 1.6e-15 (N=64)
   ```

5. **Generate extraction fallbacks.**
   Marker/Nougat are not installed on CherryRd and the shared UICGPU
   parse cluster was unreachable within this subagent's timeout budget.
   The paper is a 7-page born-digital LaTeX arXiv PDF, so `pdftotext`
   recovers the full body text faithfully. Wrote:
   - `extraction/marker.md` (pdftotext-based fallback, clearly labelled)
   - `extraction/nougat.mmd` (pdftotext -layout based fallback, clearly labelled)
   - `extraction/README.md` (documents the fallback)

6. **Write REPORT.tex** (this dir, `report/REPORT.tex`) with claims table,
   method, results-vs-paper tables, and verdict.

7. **Write open questions** (`report/open_questions.json` + `open_questions_body.tex`), 5 grounded in what the reproduction actually revealed (T-count vs unitary cost, noise crossover m*, Sec. 5 averaging convention, dagger-symmetry brittleness, Sec. 6 mis-calibrated-inverse regime).

8. **Compile REPORT.tex → PDF** if `pdflatex` is present on the host.

## Tools / versions used

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 | scripting |
| qiskit | 2.5.0 | statevector simulation, operator algebra |
| numpy | 2.5.1 | numerics |
| matplotlib | (whatever pip pulled) | convergence figure |
| pdftotext (poppler) | system | PDF → text |
| curl | system | arXiv fetch |
| pdflatex | (attempted, may not be present) | REPORT.tex → PDF |

## Estimated work

- Paper skim + claim extraction: ~5 min.
- Sim design + implementation (`grover_pi3_fixedpoint.py`, ~10 KB, both algorithms + N=16/64 sweeps + verdict): ~15 min.
- Run: <10 s (pure statevector, largest instance N=64 = 64-dim vectors).
- Write-up (REPORT.tex + open questions + workflow + artifacts summary + failure analysis): ~20 min.
- Total wall-clock ≈ 45 min; total LLM-tokens spent ≈ this transcript.
