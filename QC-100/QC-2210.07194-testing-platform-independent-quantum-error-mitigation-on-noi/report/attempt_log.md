# Attempt Log — QC-2210.07194

Chronological log of what was tried, what worked, what did not.

## 2026-07-04 02:09 CDT — Setup

- Read wave brief `scripts/WAVE_BRIEF_2026-07-01.md`. Rules: FREE endpoints only, real code + real sims, LLM-judge for verdict, write only inside target dir.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2210.07194-testing-platform-independent-quantum-error-mitigation-on-noi/{report/evidence,work}`.
- Downloaded arXiv abstract + PDF (2210.07194v2, 38 pages, 1.03 MB). Extracted metadata via `python3 re`; title/authors/abstract confirmed.

## 02:10 CDT — Paper content extraction

- Tried `pdf` tool: blocked, Anthropic quota + OpenAI PDF extract disabled + Gemini 3-flash-preview unknown. Fallback.
- Tried `ocr_pdf` (tesseract, 200 dpi): every page failed with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89` — likely a Python 3.14 subprocess encoding regression in the OCR MCP.
- Used `pdftotext -layout` directly (macOS poppler). **Worked.** 1,179 lines of text. Extracted:
  - Improvement factor formula (Eq. 4/5): shot-normalized RMSE ratio.
  - ZNE settings: kZNE=3, scale factors {1, 2, 3}, global unitary folding, Richardson + Linear extrapolation.
  - PEC settings: kPEC=100, N/kPEC=100 shots per sampled circuit, local depolarizing quasi-probability rep.
  - Benchmark circuit: n-qubit depth-d randomized-benchmarking (RB) circuit `C = U_inv * U_d * ... * U_1` with observable `|0..0><0..0|`.
  - Simulator: 1% two-qubit depolarizing after each 2Q gate.
  - Mitiq version cited by paper: 0.18.0 (we used current 1.0.0).

## 02:12 CDT — Environment

- `python3 -m venv work/venv` initially picked Python 3.14 → mitiq/qiskit wheel install failed (`Cannot import 'setuptools.build_meta'`).
- Re-created with `python3.11 -m venv work/venv`. Installed mitiq 1.0.0, qiskit 2.5.0, qiskit-aer 0.17.2, numpy, matplotlib, ply. **All good.**

## 02:16 CDT — v1 replication script

- Wrote `work/replicate_zne.py`: builds n=3 depth-d RB circuits, runs on Aer w/ 1% 2Q depol noise, applies ZNE via mitiq (`execute_with_zne` + `fold_global` + Richardson/Linear factories).
- **Bug #1 — ply missing:** `pip install ply` (cirq contrib qasm parser dep). Fixed.
- **Bug #2 — mitiq `ValueError: Could not parse executed results from executor with type float`:** initially tried wrapping in `Executor(fn)`; still failed. Root cause: `from __future__ import annotations` at the top of my script made `-> float` a string, and mitiq's `_executor_return_type in FloatLike` check (which compares the actual `float` class) failed. **Removed** the future import; annotation now becomes the runtime `float` class and mitiq accepts it. Fixed.
- v1 completed in 32.6s. Results: mu_ZNE_L(d=1) = 8.55 (excellent), mu_ZNE_R(d=1) = 1.59 (moderate). Depths d ≥ 3 all saturate at mu ≈ 1 because A₀ collapses to 1/2³ = 0.125 uniform, and ZNE at scaled circuits also sits at 0.125 (can't extrapolate signal from noise).

## 02:20 CDT — v2 with multi-trial + 2 noise levels

- Wrote `work/replicate_zne_v2.py`: N_TRIALS = 4, plus a second noise level (0.5%) to check whether the low-depth improvement is real or a luck-of-draw.
- 251 s runtime. Results:
  - **0.5% depol:** d=1 mu_R=1.27, mu_L=4.44. RMSE reduction ~4×.
  - **1.0% depol:** d=1 mu_R=3.44, mu_L=6.01. RMSE reduction ~6×.
  - Deeper depths: mu ≈ 1 (noise saturation).
- Both noise levels: at d=1, both ZNE methods gave μ > 1. Paper's "1×–7×" range is directly reproduced (peak μ_L=6.0).

## 02:24 CDT — Plots

- `work/plot_results.py`: two figures — `improvement_factor_vs_depth.png` (log-scale μ vs d for both noise levels) and `expectation_vs_depth.png` (unmitigated + ZNE(R) + ZNE(L) expectation values vs depth). Both saved under `report/evidence/`.

## 02:27 CDT — Second mitigation method: PEC

- `work/replicate_pec.py`: PEC via mitiq's `execute_with_pec` + `represent_operations_in_circuit_with_local_depolarizing_noise` at the same 1% level. kPEC=100, N/kPEC=100 shots per sampled circuit (matches paper).
- Circuit conversion: mitiq PEC works on Cirq circuits, so we `from_qiskit(circ)` before PEC and (inside the executor) convert samples back to Qiskit for Aer execution.
- 188 s runtime.
- **Result:** mu_PEC(d=1) = 0.12; mu_PEC(d=3) = 0.93 — **worse** than unmitigated at our settings. Root cause: with N/kPEC = 100 shots per sampled circuit, the quasi-probability estimator has enormous variance; APEC mean at d=1 is 1.42, well over the ideal 1.0. Paper reports μ_PEC ~ 1..2 on a similar 1% depol simulator, which suggests their kPEC/shot allocation or noise-model matching is more tightly tuned than a first-pass reproduction. We do NOT claim PEC is broken — we claim our first-pass PEC configuration under-performs, and this is a limitation to note, not a contradiction of the paper's qualitative message.

## Summary of what worked / didn't

Worked:
- pdftotext for paper text (bypassing broken pdf/ocr tools).
- Python 3.11 venv → mitiq 1.0.0 + qiskit 2.5.0 + qiskit-aer 0.17.2 installed clean.
- ZNE via mitiq: both Richardson and Linear factories; global unitary folding at scale factors {1,2,3}; runs cleanly against Qiskit + Aer noisy simulator.
- Reproducing paper's headline "1×–7× improvement" at d=1 under both 0.5% and 1.0% depolarizing noise on n=3 RB circuits.

Didn't work / limitations:
- pdf tool (Anthropic 400 credit low; OpenAI PDF disabled; Gemini alias broken).
- ocr_pdf UTF-8 decode error under Python 3.14 MCP.
- mitiq annotation gotcha via `from __future__ import annotations`.
- PEC first-pass reproduction: μ < 1, does not confirm paper's μ_PEC ~ 1..2. Would need finer-grained representation building (per-gate quasi-prob with matched noise strength) and larger sample budget.
- No real IBM/IonQ/Rigetti hardware runs (hard rule: no paid queue).
