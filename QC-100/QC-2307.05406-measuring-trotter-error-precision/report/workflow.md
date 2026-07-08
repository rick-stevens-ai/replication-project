# Workflow — arXiv:2307.05406 replication

## Environment
- Host: CherryRd (macOS, MacBook-class)
- Python 3, NumPy 2.4.3, SciPy 1.18.0
- No GPU; dense statevector on CPU
- Free endpoints only (LLM-judge panel via Argo: `argo:gpt-5.1`, `argo:gemini-2.5-pro`)

## Steps

1. **Paper read** (once). Extracted:
   - Central estimator (Eq. 8):  η_F^(24) = sqrt(1 − |⟨T4 ψ | T2 ψ⟩|²)
   - Adaptive rule: δt_new = C · δt · (ε / η_est)^{1/(m+1)}, m=2 → cube root
   - Benchmark H (Eq. 27–28): mixed-field Ising, L=18, J_z=−1, h_z=0.2, h_x=−2
   - Initial state: fully -ŷ polarized
   - Tolerances: 10^{-3/2}, 10^{-2}; safety C=0.95
   - Comparison bound: Eq. (29) via nested commutator operator norms

2. **Reimplement from equations only.** No author code consulted. ~200 LOC in NumPy/SciPy:
   - Build A, B, H = A + B dense (2^L × 2^L)
   - Exact U = expm(−i δt H) as ground truth
   - T2 (Strang), T4 (Forest-Ruth triple-jump with s = 1/(2 − 2^{1/3}))
   - Two metrics: η_true (T2 vs exact), η_est^(24) (T4 vs T2)
   - Adaptive loop until convergence

3. **Scale down** to L=6, 8, 10 (up to 1024×1024 dense expm) — small-but-faithful per QC-100 brief. Same physics, more tractable expm.

4. **Runs**:
   - `python3 work/trotter24.py`   → L=6 + L=8, scan + adaptive
   - `python3 work/trotter24_L10.py` → L=10 adaptive
   - Total wall time ~50 s.

5. **Verdict via LLM-judge panel** (Argo, free): two independent judges (`argo:gpt-5.1`, `argo:gemini-2.5-pro`); both AGREE / REPLICATED (confidence 0.86 and 0.95). No regex parsing, no author self-scoring.

6. **Artifacts written**:
   - `report/REPORT.md`, `report/REPORT.tex`
   - `report/evidence/trotter24_results.json`, `trotter24_L10.json`
   - `report/evidence/llm_judge_gpt51.json`, `llm_judge_gemini.json`
   - Code mirrored under `report/evidence/`
   - This workflow, `artifacts_summary.md`, `failure_analysis.md`, `open_questions.json`, `open_questions_section.tex`
   - `extraction/nougat.mmd` (stub)

## What I did NOT do
- Did not go to L=18 (memory/time). Consequence: C3 headline (~10× ratio) only extrapolated.
- Did not implement observable-based variant (needs sampling machinery).
- Did not implement noise / hardware simulation.
- Did not implement time-dependent Trotter (Magnus/Dyson variants).

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2307.05406-measuring-trotter-error-precision/work
python3 trotter24.py         # ~3 s
python3 trotter24_L10.py     # ~45 s
```
