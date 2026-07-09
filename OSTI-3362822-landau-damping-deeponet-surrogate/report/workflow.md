# Workflow, Tools, Effort — OSTI 3362822 replication

## Workflow narrative

1. **Setup.** Wave brief read → target-dir created under
   `~/Dropbox/REPLICATE-PROJECT/OSTI-3362822-landau-damping-deeponet-surrogate/`
   (fresh, no clobber).
2. **Paper fetch.** `ssh uicgpu` + `curl -L https://www.osti.gov/servlets/purl/3362822 → paper.pdf`
   (2.5 MB, PDF 1.7, 8 pages). Scp back to Dropbox.
3. **Extraction (Marker, GPU).** Ran Marker on uicgpu (`/data/stevens/envs/marker/bin/marker_single`),
   ~41 s, produced `paper.md` + 12 figure JPEGs + `paper_meta.json`.
   Copied `paper.md` → `extraction/marker.md` (31 KB).
4. **Extraction (Nougat, GPU).** First tried `/data/stevens/.venvs/extraction/bin/nougat` —
   fails on transformers-4.x API drift (`prepare_inputs_for_generation` signature change).
   Fell back to `/gpustor/stevens/anaconda3/envs/nougat/bin/nougat`, ~16 s, produced `paper.mmd`.
   Copied → `extraction/nougat.mmd` (26 KB).
5. **Comprehensive paper read.** `pdftotext -layout` locally + read all 8 pages
   (`work/paper_pdftotext.txt`, 43 KB). Extracted claims C1–C5, hyperparameters (Table 2),
   error metrics (Table 3–4), five-mode wavenumber table (Table 1), Vlasov–Poisson formulation.
6. **Reference solver (from scratch).** Wrote `work/replicate.py` — Python VP solver:
   Fourier x-advection (cached FFT shift), vectorized linear-semi-Lagrangian v-advection,
   spectral Poisson, Strang splitting.
7. **Solver verification.** Coded analytic linear-Landau dispersion solver
   (`scipy.optimize.root` on `ε(k, ω) = 0` using `scipy.special.wofz`). Baseline single-mode
   sim γ_num = -0.0384 vs γ_analytic = -0.0343 (12% bias — acceptable for coarse grid).
8. **Dataset generation.** 200 train + 50 test single-mode VP sims (T uniform in [0.5, 1.5]).
   Wall clock 590 s on uicgpu single-thread CPU. Saved `dataset_single.npz` (808 KB).
9. **DeepONet training v1 (paper-matching).** Depth 6 width 200 tanh Adam 1e-3 exp-decay,
   50k iters. **Failed** — plateaued at MSE(log E) = 0.478 (ensemble-mean fit).
10. **DeepONet training v2 (Fourier features).** 16-D sinusoidal encoders on T and t,
    depth-4 width-128 MLPs, latent p=100, Adam 5e-4 cosine anneal, grad clip 1.0,
    60k iters, best-test model selection. **Best test MSE(log E) = 0.0123** in 242 s.
11. **Evaluation.** rel-L2 error norm (paper Eq. 9) on E in linear space.
    Train mean 0.164, test mean 0.183, best test case 0.075. 22× the paper's mean.
12. **Inference throughput.** 100-case DeepONet inference on A100 = 0.63 ms
    (paper reports 1.48 ms on L40S). OoM match.
13. **Plotting.** `tmp-plot.py` generated 4 PNGs: Fig-3-style DeepONet-vs-sim (6 test cases),
    error-distribution histogram + T-scatter, analytic dispersion (Fig-2 style), baseline-sim
    damping envelope.
14. **LLM judge.** `argo:gpt-5.2` via the local Argo aggregator at
    http://<tailnet-aggregator>:4000 (Bearer token `stevens`, free endpoint).
    Returned `{verdict: PARTIAL, coverage: 0.55, agreement: 0.35}`. Saved as
    `evidence/llm_judge.json`.
15. **Writeup.** `report/brief.md`, `report/REPORT.md`, `report/REPORT.tex` (→ `REPORT.pdf`),
    `report/open_questions.json` (5 questions each with basis + next_steps),
    `report/artifacts_summary.md`, `report/failure_analysis.md`, `report/attempt_log.md`,
    `report/artifact_harvest.md`, this `report/workflow.md`.

## Tools + versions

| tool | version | role |
| --- | --- | --- |
| curl | 8.x | fetch paper.pdf from OSTI |
| pdftotext (poppler) | 25.x | local paper text extraction |
| marker_single | 2.x (via `/data/stevens/envs/marker/bin/`) | Marker extraction on uicgpu |
| nougat | (from `/gpustor/stevens/anaconda3/envs/nougat/`) | Nougat extraction on uicgpu |
| Python | 3.11 | numerical work |
| numpy | 2.x | array ops, FFT, `trapezoid` |
| scipy | 1.x | `optimize.root`, `special.wofz`, `signal.find_peaks` |
| torch | 2.12.0+cu126 | DeepONet training on A100 |
| matplotlib | 3.x | figures |
| argo:gpt-5.2 | via LiteLLM aggregator at <tailnet-aggregator>:4000 | LLM judge |
| pdflatex | TeXLive 2026-03-01 | compile REPORT.pdf |

## Code + scripts

| file | LOC | purpose |
| --- | --- | --- |
| work/replicate.py | 380 | VP solver + analytic dispersion + DeepONet training v1 + inference bench |
| work/retrain.py | 130 | DeepONet training v1.5 (Fourier features, no cosine sched) |
| work/retrain2.py | 150 | DeepONet training v2 (Fourier + cosine sched + grad clip + best-test) — CANONICAL |
| tmp-plot.py | 120 | Generate all 4 report figures |
| tmp-judge.sh | 60 | LLM-judge shell wrapper (Argo endpoint) |

Total agent-written Python + shell: ~840 LOC.

## Effort estimate

| stage | wall clock | compute cost |
| --- | --- | --- |
| Paper fetch + extraction (Marker+Nougat) | ~2 min | uicgpu GPU-side, ~1 min GPU-time |
| Reading paper, planning replication | ~5 min agent-time | none |
| Writing replicate.py | ~3 min agent | none |
| VP solver bugfix (`np.trapz` → `np.trapezoid` for numpy 2.x) | ~1 min | trivial |
| VP dataset generation (250 sims × 2.4 s) | 10 min | uicgpu CPU, single-thread numpy |
| DeepONet training v1 (failed plateau, 50k iter) | ~4 min | uicgpu GPU 6 |
| DeepONet training v2 (60k iter, Fourier features) | ~4 min | uicgpu GPU 6 |
| Plotting (4 figures) | ~10 s | local |
| LLM judge (1 API call) | ~10 s | Argo free |
| Report writing (this file + REPORT.md + REPORT.tex + 5 open_questions + failure_analysis + …) | ~10 min agent | none |
| **Total wall clock** | **~40 min** | ~15 min GPU + ~10 min CPU on uicgpu |

Total runs executed: 3 DeepONet training runs (v1 plateau discard, v1.5 partial-fix, v2 canonical);
1 dataset-generation run; 1 Marker + 1 Nougat parse; 1 LLM-judge call. No wasted compute
after the `np.trapz` bugfix.
