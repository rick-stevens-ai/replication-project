# Workflow — QC-2204.13641 Real Quantum Amplitude Estimation

**Set:** QC-100
**Paper:** Manzano, Musso, Leitao. *Real Quantum Amplitude Estimation.* arXiv:2204.13641 (2022).
**Replicator:** Ollie (OpenClaw subagent, depth 1)
**Verdict:** REPLICATED
**Backfill date:** 2026-07-06 (original run 2026-07-04)

## Chronological workflow

### 1. Ingest & triage (2026-07-04)
- Pulled `arXiv:2204.13641` PDF into `work/paper.pdf`; ASCII text at `work/paper.txt`.
- Read Algorithm 1 (Sec. 3), Eq. (6, 7, 9, 14, 19), and Fig. 6 (headline scaling plot).
- Identified the paper's most testable headline: **`N_oracle ~ 1/eps` for RQAE vs `~1/eps^2` for classical**, at 95% coverage, quantifiable in a shot-based simulator on a single-qubit toy oracle.

### 2. Scope decision
- Scope: single-qubit toy oracle (`R_y(2 arcsin c)`, `S=2`), 3 true amplitudes (`+0.30, +0.70, -0.40`), 4 target epsilons (`0.05, 0.02, 0.01, 0.005`), 25 reps per config, gamma=0.05, q=2.
- Excluded: noise model, alternative QAE baselines (MLQAE/IQAE), multi-qubit finance oracles. These became **open questions**.

### 3. Implementation (`code/rqae.py`, `code/run_experiment.py`)
- Faithful transcription of Algorithm 1 with Eqs. (14), (19).
- Two transcription bugs hit and fixed (documented in REPORT.md §6):
  - Eq. (14): numerator is `pi/4`, not `pi/2` (a `pi/2` mistake doubles amplification power and wraps the amplified angle past `pi/2`, giving systematic ~0.06 negative bias).
  - Eq. (19): `p` is **squared** in the denominator; missing the square gives ~30 shots instead of ~500 and destroys coverage.
- Both bugs are asymptotic-slope-compatible (they don't change the scaling exponent) but destroy the finite-eps constant.

### 4. Simulation (2026-07-04)
- Ran shot-based `AerSimulator()` (real Bernoulli sampling, not statevector shortcut).
- 3 amplitudes × 4 epsilons × 25 reps × 2 methods (RQAE + classical) = 600 experiments.
- Wall-clock: **238 s** on single M-series CPU.
- Output: `report/evidence/results.json`, `logs/experiment.log`.

### 5. Scoring
- Log–log fit on `N_oracle` vs `1/eps`:
  - RQAE slope: **0.959** (paper: ~1.0) ✓
  - Classical slope: **2.000** (theory: 2.0) ✓
- Coverage: **100%** across all 12 configs (paper: ≥95%) ✓
- RMSE well below `eps_target` in every case.
- Sign correctness verified on `a = -0.4`.

### 6. LLM judge (`code/llm_judge.py`)
- Single call to local Argo proxy (`http://localhost:44497/v1`, `argo:claude-opus-4.7`, key `stevens`) — free endpoint.
- Judge returned: `overall_verdict: REPLICATED`.
- Output: `report/evidence/judge_verdict.json`.

### 7. Report (2026-07-04)
- Wrote `report/REPORT.md` with claims table, method, results, verdict, notes-to-future-replicators, files list.

### 8. Backfill (2026-07-06, this task)
- Backfilled 7 artifacts to meet QC-100 8-artifact standard:
  1. `report/REPORT.tex` — LaTeX mirror with explicit Critique section
  2. `report/open_questions.json` — bare list of 5 open questions with basis + next_steps
  3. `report/open_questions_section.tex` — LaTeX section included by REPORT.tex
  4. `report/workflow.md` — this file
  5. `report/artifacts_summary.md` — file-level inventory
  6. `report/failure_analysis.md` — honest critique (limitations, unresolved questions)
  7. `extraction/nougat.mmd` — nougat extraction stub (paper.txt already exists)
- **No simulations re-run.** All numeric results preserved from 2026-07-04.
- Preserved verdict: **REPLICATED** (headline exercised, slope match confirmed).

## Free-endpoint compliance
- Simulation: local CPU (free).
- LLM judge: Argo proxy `argo:claude-opus-4.7` (free — Rick's standing rule).
- No paid API calls at any point.

## Reproduction command
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2204.13641-real-quantum-amplitude-estimation
python3 -m venv .venv && . .venv/bin/activate
pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy
python code/run_experiment.py    # regenerates report/evidence/results.json
python code/llm_judge.py         # regenerates report/evidence/judge_verdict.json
```
