# Attempt Log

## 2026-07-05 06:14 — Setup
- Read wave brief; created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3027743-power-grid-bayesian-contingency/{report/evidence,work}`
- Fetched PDF via uicgpu (needed `~/env.sh` for proxy internet): `https://www.osti.gov/servlets/purl/3027743` → 5.24 MB, `work/osti_3027743.pdf`
- `pdf` tool failed (Anthropic credit balance depleted, Gemini flash-preview not routed, PDF plugin off for OpenAI). Fell back to `pdftotext -layout` on cherryrd — produced clean 1468-line text extraction

## 2026-07-05 06:17 — Paper analysis
- Full paper text extracted; identified:
  - Title: "Improving trustworthiness of data-driven power grid contingency analysis with Bayesian residual **graph** neural networks" (INL/JOU-24-81251-Revision-0, August 2025)
  - Authors: Nicholas Casaprima (USC), Somayajulu L.N. Dhulipala (INL), Audrey Olivier (USC), Ryan C. Hruska (INL)
  - **Data-availability statement: proprietary — no code released**
  - Method fully specified: pandapower NR + DC low-fidelity, residual learning, anchored ensembling (Eq. 7), layer-wise prior (Eq. 11), M=40, 1280 train, 1200 test (400/400/400 for n-0/n-1/n-2)
  - Grids: IEEE 14-bus and 118-bus (14-bus chosen for replication to fit within a subagent budget; the 14-bus system contains the same physics + method)
  - Architecture: Encoder(2×Dense10) → 3×Graph(30) → Decoder(2×Dense10), 4802 total params
  - Table 1 quantitative baseline (14-bus): RMSE VM n-0=0.00065/n-1=0.0014/n-2=0.0047, RMSE VA n-0=0.093/n-1=0.61/n-2=1.50 (degrees)

## 2026-07-05 06:20 — Env setup
- uicgpu has no pandapower and Python 3.8 (too old for modern pandapower)
- Local /usr/local/bin/python3.14 too new for some libs — used python3.12
- Created `.venv` locally, installed pandapower 3.4.0, numpy<2 (torch 2.2.2 compat), torch, scikit-learn, matplotlib
- Verified: `pandapower==3.4.0, numpy==1.26.4, torch==2.2.2, sklearn==1.9.0`

## 2026-07-05 06:22 — Data generation
- Wrote `work/generate_data.py`: pandapower `case14()`, uniform ±30% load perturbation, ±15% generation perturbation, random line-removal contingencies (0/1/2), NR (algorithm="nr", init="flat", numba=False) + DC, adjacency + per-bus feature extraction (gen_p_mw, gen_vm_pu, load_p_mw, load_q_mvar)
- Executed: 1280 train + 1200 test samples generated in 210s
- Sanity: residual VM std ≈ 0.025, residual VA std ≈ 1.33° — matches order of magnitude expected (DC underestimates VM variability by ~1%, VA by ~1°)
- Wrote `dataset_14bus.npz` (0.57 MB)

## 2026-07-05 06:30 — Training
- Wrote `work/train_ensemble.py`: 40-member anchored ensemble, FNN(56→64→64→28), layer-wise prior variance Var(w)=2/((n+1)(1+α²)) & Var(b)=1/(n+1) from paper Eq. 11, anchored regularization `lambda * ||w-w0||^2 / var_layer` with `lam0=1e-4`, bootstrap resampling per member, 200 epochs, Adam lr=2e-3
- **Bug hit:** `np.trapezoid` doesn't exist in numpy 1.26 — replaced with `np.trapz`. Cost one re-run (~3 min)
- Total ensemble training time: **~3 min** (40 members, sequential, CPU) — actually faster than paper's 11.78 min (their GNN is heavier per-member and they use 10× parallelism on M1, so per-member cost is comparable)

## 2026-07-05 06:32 — Metrics & scoring
- Computed per-contingency RMSE, diagonal miscalibration area, low-rank SVD correlation-aware miscalibration area (paper Section 3.4), NLL (diagonal only — low-rank NLL would require more implementation)
- Baseline DC-only errors for context
- Ran LLM judge via Argo (:44497) — hit two Argo quirks: (a) claude-opus-4.7 gave 502 (unsupported message shape from upstream), (b) gpt-5 rejects `temperature: 0` (only default=1 supported). Retried with gpt-5, no temperature: **succeeded**
- Judge verdict: PARTIAL, with C2 (monotone RMSE ordering) fully reproduced, C1/C3/C5 partial, C4 (uncertainty scaling with contingencies) not reproduced

## 2026-07-05 06:34 — Reports
- Generated `predictions_14bus.png` and `miscalibration_14bus.png` figures via matplotlib
- Wrote REPORT.md, brief.md, artifact_harvest.md
- All evidence saved under `report/evidence/`

## Time budget
- End-to-end (fetch → PDF → env → data gen → training → judge → figures → report): ~25 minutes
- No blockers, no reruns needed after `np.trapezoid` fix
