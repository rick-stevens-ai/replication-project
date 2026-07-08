# Workflow — QC-2306.12569 Trotter error bounds multiproduct

## Environment
- Host: `CherryRd` (Darwin 25.3.0, x86_64), CPU-only.
- Python 3.13 in a fresh venv under the replication dir.
- `qiskit==2.5.0`, `numpy==2.4.3`, `scipy==1.18.0`.
- Free endpoints only (no LLM required for the numerical replication itself).

## Step-by-step pipeline

1. **Fetch paper.**
   ```bash
   curl -sL https://arxiv.org/pdf/2306.12569 -o work/paper.pdf
   pdftotext -layout work/paper.pdf work/paper.txt
   ```

2. **Set up environment.**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install --quiet qiskit numpy scipy
   ```

3. **Clean-room implementation of paper's Section V** (`code/mpf_replication.py`):
   - `H = sum_j (X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1}) + sum_j h_j Z_j`, `h_j ~ U(-1, 1)`.
   - Second-order Trotter `S_2(t) = e^{-it F_5} e^{-it F_4} e^{-it F_3} e^{-it F_2} e^{-it F_1}`
     with the paper's exact `F_i` split.
   - `rho_k(t) = S_2(t/k)^k |psi_0><psi_0| S_2(t/k)^{-k}` with `|psi_0> = |1010...>`.
   - MPF `mu(t) = sum_i c_i rho_{k_i}(t)` with `k = lambda*(4, 13, 17)`,
     `c = (0.016088, -1.794934, 2.778846)`.
   - Exact reference `rho(t) = e^{-itH} |psi_0><psi_0| e^{itH}` via `scipy.linalg.expm`.
   - Error metric `||.||_1` via singular values.

4. **Run main experiment.**
   ```bash
   python code/mpf_replication.py > logs/run1.log
   ```
   Sweep `n in {3, 4}`, `t = 1.0`, `lambda in {1, 2, 3}`, seed = 1.

5. **Run scaling verification.**
   ```bash
   python code/mpf_scaling_check.py > logs/scaling.log
   ```
   Sweep `lambda in {1..6}`; fit slope of `log(error)` vs `log(lambda)` for
   both Trotter and MPF; write `report/evidence/scaling_check.json`.

6. **Cross-check headline.**
   Confirm MPF slopes at `n=3,4`, `t=1` are within tolerance of the target `-4`
   (measured `-4.036`, `-4.055`); Trotter slopes within tolerance of `-2`
   (measured `-2.001`, `-2.007`).

7. **Write report.**
   `report/REPORT.md` (source of truth), then `report/REPORT.tex` for archival.

## Total wall-clock
~0.1 s across both scripts on one CPU core.

## Artifacts produced (this backfill)
- `report/REPORT.tex` — LaTeX archival version of REPORT.md
- `report/open_questions.json` — 5 open questions with basis + next_steps
- `report/open_questions_section.tex` — LaTeX rendering of the same
- `report/workflow.md` — this file
- `report/artifacts_summary.md` — inventory
- `report/failure_analysis.md` — honest critique
- `extraction/nougat.mmd` — placeholder stub (no re-extraction performed)

## Deliberate non-actions
- No re-running of simulations.
- No LLM calls (free or paid).
- No modification of existing REPORT.md, code, evidence, or logs.
