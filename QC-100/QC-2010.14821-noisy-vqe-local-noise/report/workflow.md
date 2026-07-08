# Workflow — QC-2010.14821 (noisy VQE, local noise)

## 1. Paper acquisition
- arXiv: [2010.14821](https://arxiv.org/abs/2010.14821), v2 (14 Apr 2021).
- PDF fetched → `work/paper.pdf`; pdftotext dump → `work/paper.txt`.
- Confirmed authorship: Zeng, Wu, Cao, Zhang, Hou, Xu, Zeng (subagent brief mis-attributed to "Gentini et al." — corrected in REPORT.md).

## 2. Claim triage
Identified 9 distinct claims (C1–C9). Marked C3, C4, C5 as headline (numerical, testable). Marked C7 (three noise-channel comparison), C8 (n=6 mean-field beat), C9 (IBM device match) as out-of-scope for a CPU-only replication run within subagent time budget.

## 3. Environment build
- Host: CherryRd (macOS Darwin 25.3.0), Python 3.14.
- Isolated `.venv/` (subsequently deleted for space; recreation recipe in REPORT.md §6).
- Package pins: `qiskit==2.5.0`, `qiskit-aer==0.17.2`, numpy 2.5.0, scipy, matplotlib.

## 4. Code
- `code/vqe_noisy.py` — implements the paper's Fig. 2 hardware-efficient ansatz byte-for-byte, drives noiseless COBYLA optimization at n_qubits=4, d in {2,3}, then evaluates Tr(ρH) at the noiseless optimum under a local depolarizing NoiseModel for each p in the sweep.
- `code/analyze_and_plot.py` — fits small-p linearity, computes depth-accumulation ratios, emits both PNG plots.

## 5. Runs
```bash
# Smoke test:
python code/vqe_noisy.py --n-qubits 2 --d 1 --n-seeds 2 --maxiter 200 \
    --outdir report/evidence/smoke_n2_d1 --p-values 0,1e-3,1e-2

# Headline sweeps:
python code/vqe_noisy.py --n-qubits 4 --d 2 --n-seeds 5 --maxiter 800 \
    --outdir report/evidence/main_n4_d2 --p-values 0,1e-4,3e-4,1e-3,3e-3,1e-2
python code/vqe_noisy.py --n-qubits 4 --d 3 --n-seeds 5 --maxiter 1500 \
    --outdir report/evidence/main_n4_d3 --p-values 0,1e-4,3e-4,1e-3,3e-3,1e-2

# Analysis + plots:
python code/analyze_and_plot.py
```
All seeds fixed (0..4). All outputs deterministic.

## 6. Results extraction
Raw `results.json` files aggregated by `analyze_and_plot.py` → `analysis_summary.json`. Two PNG figures.

## 7. Verdict assembly
Cross-referenced observed slopes / ratios against paper §III text and Fig. 3 curves; verdict **REPLICATED (strong)** for C3–C6 depolarizing-noise claims. Documented optimizer shortfall (0.965 vs 0.98 baseline) as an orthogonal, non-fatal issue.

## 8. Backfill packaging (2026-07-06)
- Converted `report/REPORT.md` → `report/REPORT.tex` with matching structure, tables, and honest Critique section.
- Wrote `open_questions.json` (5 truly-open items with concrete next-steps recipes), `open_questions_section.tex` (LaTeX version, `\input`'d at end of REPORT.tex).
- Added `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.
- Placeholder `extraction/nougat.mmd` — the paper was ingested via arXiv PDF + pdftotext, not via Nougat OCR; the stub records this and points to `work/paper.txt`.
- No re-runs; no new simulations. Existing evidence preserved verbatim.
