# Workflow — Liu 2020 VQA-Poisson Replication

## Overview
End-to-end pipeline for independent replication of Liu et al. (2020),
"Variational Quantum Algorithm for the Poisson Equation" (arXiv:2012.07014,
Phys. Rev. A 104, 022418).

Wall time: ~60 minutes. Verdict: PARTIAL. LLM-judge (Argo/gpt-5.2): PARTIAL, confidence 90.

## Stage 0 — Artifact Fetch
- **Input:** paper preprint ID `arXiv:2012.07014v1`.
- **Action:** download PDF from `https://arxiv.org/pdf/2012.07014.pdf`.
- **Output:** `work/liu_vqa_poisson.pdf` (720 KB, 6 pages + refs + Appendix A).
- **Notes:** no external datasets required — the problem is fully specified
  by the canonical finite-difference tridiagonal matrix and RHS `b_i = f(x_i)`,
  `f(x) = x`, `x_i = i/(n+1)`, `i = 1..n`.

## Stage 1 — Environment Setup
- **Local (CherryRd, macOS arm64):**
  - `python3 -m venv work/venv`
  - `source work/venv/bin/activate`
  - `pip install numpy scipy` → numpy 2.5.0, scipy 1.18.0 on python 3.14.
- **Remote (uicgpu, Ubuntu, 8×A100):**
  - Existing conda env with python 3.10, numpy 1.23.5, scipy 1.10.1.
  - Access via SSH mesh alias `uicgpu` (routes via Tailscale).

## Stage 2 — Implementation (`work/liu_vqa.py`, 14 KB, MIT)
Re-derived entirely from paper equations. No paper-provided reference code
was used.

Function map:
1. `build_A(m)` — dense reference tridiagonal `(-1, 2, -1)` matrix,
   size `2^m × 2^m`.
2. `decompose_A(m)` — recursive per Eq. (11).
3. `decompose_B(m)`, `decompose_C(m)` — Eqs. (13)–(18).
4. `decompose_Asq_pure(m)` — expands compound leaves into pure
   single-qubit tensor products giving the paper's `4m+1` count.
5. `verify_A(m)` / `verify_Asq(m)` — max-abs error vs. ground truth.
6. `ansatz(theta, m, p)` — hardware-efficient RX+RZ+linear-CNOT
   ansatz (Fig. 3 style, simplified). Params: `2·m·p`. Applied via
   tensordot + moveaxis for `O(2^m)` speed.
7. `cost_E(theta, m, p, A, A², |b⟩)` — Eq. (6) evaluated exactly on
   the statevector (no shot noise).
8. `run_vqa(m, p)` — 20 random-init restarts (uniform, near-zero,
   near-π), each optimized with scipy L-BFGS-B and BFGS
   (`gtol=1e-9`, `maxiter=500`).
9. `run_vqa_warmstart(m, p, prev_θ)` — adaptive-layer growth.
10. `min_layers_for_099(m)` — increments `p` until threshold met.

## Stage 3 — Local Sweep (m = 2..4)
```
python3 work/liu_vqa.py > report/evidence/main_run.log
```
Runs C1 (m=1..6), C2 (m=1..6), C3 (m=2..4). Fast: <5 minutes on CherryRd.

## Stage 4 — Remote Sweep (m = 5, 6)
Local wall time infeasible for m ≥ 5; offloaded to uicgpu.
```
rsync work/liu_vqa*.py uicgpu:~/liu_vqa_repl/
ssh uicgpu 'cd ~/liu_vqa_repl && parallel --colsep " " -j 16 \
  "OMP_NUM_THREADS=1 python3 liu_vqa_parallel.py {1} {2} {3}" \
  <<< "$(for m in 5 6; do for p in 1..8; do echo $m $p 20; done; done)" \
  > vqa_m56_results.jsonl'
scp uicgpu:~/liu_vqa_repl/vqa_m56_results.jsonl work/
```
- `-j 16` parallelism across A100 cores (statevector fits comfortably in
  RAM; no GPU actually needed for m ≤ 6).
- One JSON per `(m, p)` per line in `vqa_m56_results.jsonl`.
- **Cutoff:** m=6, p=3..8 jobs (each >800 s serial) were still running when
  the report was finalized; sweep truncated at p=2 for m=6.

## Stage 5 — Merge Results
```
python3 work/finalize.py
```
Combines local `main_run` output with `vqa_m56_results.jsonl` into unified
`report/evidence/results.json`. Populates:
- `C1_A_decomposition` (m=1..6)
- `C2_Asq_decomposition_pure` (m=1..6)
- `C3_VQA_sweep_local` (m=2..4)
- `C3_VQA_sweep_uicgpu` (m=5..6)

## Stage 6 — LLM-Judge
```
python3 work/llm_judge.py
```
Feeds full `results.json` + console log to `argo:gpt-5.2` via
Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (FREE, key `stevens`).
Requests structured JSON verdict per claim.
Writes `report/evidence/llm_judge.json` (raw + parsed).

## Stage 7 — Report Assembly
Manual synthesis of REPORT.md from:
- `results.json` (numeric evidence tables)
- `llm_judge.json` (independent non-regex verdict)
- `attempt_log.md` (chronological log)
- `artifact_harvest.md` (public artifact provenance)

## Data Flow Diagram
```
  arXiv:2012.07014 PDF
         |
         v
  Manual re-derivation of Eqs. 11-18
         |
         v
  work/liu_vqa.py --------> Local sweep (m=2..4) --> main_run.log
         |                                                |
         +-------> uicgpu ---> Parallel sweep (m=5,6) --> vqa_m56_results.jsonl
                                                          |
                                                          v
                                              work/finalize.py
                                                          |
                                                          v
                                              report/evidence/results.json
                                                          |
                                                          v
                                              work/llm_judge.py
                                                (Argo gpt-5.2, FREE)
                                                          |
                                                          v
                                              report/evidence/llm_judge.json
                                                          |
                                                          v
                                              report/REPORT.md (manual synthesis)
```

## Reproduction Recipe (bootstrap from scratch)
```
mkdir -p PDE-Liu-VQA-poisson-equation-2020/{work,report/evidence}
cd PDE-Liu-VQA-poisson-equation-2020
curl -o work/liu_vqa_poisson.pdf https://arxiv.org/pdf/2012.07014.pdf
python3 -m venv work/venv && source work/venv/bin/activate
pip install numpy scipy
# Copy in work/liu_vqa.py, work/liu_vqa_parallel.py, work/finalize.py, work/llm_judge.py
python3 work/liu_vqa.py > report/evidence/main_run.log
# [Remote sweep as in Stage 4]
python3 work/finalize.py
python3 work/llm_judge.py
```

## Compute Budget
| Stage | Host | Wall time |
|---|---|---|
| Local m=2..4 sweep | CherryRd | ~5 min |
| uicgpu m=5, p=1..8 (parallel -j 16) | uicgpu | ~10 min |
| uicgpu m=6, p=1..2 completed | uicgpu | ~15 min |
| uicgpu m=6, p=3..8 (cutoff, incomplete) | uicgpu | ~35 min budget spent, incomplete |
| Merge + LLM-judge | CherryRd | ~2 min |
| Report writing | CherryRd | ~15 min |
| **Total** | | **~60 min** |
