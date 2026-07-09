# Artifacts Summary — OSTI 3002302

Independent replication of Ding & Do, "Deciphering the small-angle scattering
of polydisperse hard spheres using deep learning," *APL Machine Learning* 3,
036112 (2025). Verdict: **REPLICATED**.

## Report directory (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary human-readable independent replication report. |
| `REPORT.tex` | LaTeX version of the report with a dedicated `Genuine Critique` section. |
| `open_questions.json` | 5 genuinely open follow-up questions grounded in the SANS-of-polydisperse-hard-spheres domain, with `{q, basis, next_steps}`. |
| `workflow.md` | Stage-by-stage execution log of the replication (Stages 0–8). |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | What went wrong / almost went wrong, and how it was handled. |

## Author-released artifacts (external, from
https://github.com/ljding94/Polydisperse_Sphere)

| Artifact | Notes |
|---|---|
| `analyze/VAE_model.py` | Network definitions (Encoder/Decoder/Converters). |
| `analyze/analyze_PY.py` | Authors' PY reference — NOT reused; baseline was independently re-implemented from Wertheim 1963. |
| `data_used/L_18_pdType_{1,2,3}_train_data.npz` | 4000 (η, σ, I(Q)) training triples per distribution family. |
| `data_used/L_18_pdType_{1,2,3}_test_data.npz` | 1000-point test set per family. |
| `L_18_pdType_{1,2,3}_train_stats.npz` | I(Q) normalization statistics. |
| `L_18_pdType_{1,2,3}_vae_state_dict.pt` | Released VAE weights per family. |
| `L_18_pdType_{1,2,3}_gen_state_dict.pt` | Released Generator weights per family. |
| `L_18_pdType_{1,2,3}_inf_state_dict.pt` | Released Inferrer weights per family. |

## Independent replicator artifacts (`evidence/`, referenced from REPORT.md)

| File | Contents |
|---|---|
| `eval_released_results.json` | Full JSON dump of Inferrer + Generator + PY / PYβ metrics across all three pdTypes on the released 1000-point test set (Stages 4–5 in workflow.md). |
| `retrain_pdType1_results.json` | From-scratch retrain metrics on pdType 1 with compressed schedule (Stage 6). |
| `retrain_pdType1.log` | Training-loss log for the from-scratch retrain. |
| `llm_judge_prompt.txt` | Structured prompt sent to `argo:gpt-5.2` LLM judge. |
| `llm_judge_verdict.json` | LLM judge return: verdict=REPLICATED, coverage=0.8, agreement=0.95, plus justification. |

## Primary source

| Item | Value |
|---|---|
| Paper | Ding & Do, *APL Machine Learning* 3, 036112 (2025) |
| DOI | [10.1063/5.0290589](https://doi.org/10.1063/5.0290589) |
| OSTI ID | 3002302 |
| PDF (OSTI) | https://www.osti.gov/servlets/purl/3002302 |
| PDF bytes | 7,118,161 |
| PDF MD5 | `2b7c8c230cb802ab89cb25f2ec8eb14b` |
| License | CC BY-NC 4.0 |

## Headline quantitative results

* **Inferrer** (Claim C2): R² ≥ 0.99987 for both η and σ on all three
  distribution families, with sub-1% relative error (η: 0.32–0.34%;
  σ: 0.39–0.49%).
* **Generator vs PY/PYβ** (Claim C3): NN generator's log₁₀-space MSE is
  17–120× smaller than the independently re-implemented PY / PYβ analytic
  baselines (best: 120× vs PY on uniform pdType; worst: 17× vs PYβ on
  normal pdType).
* **From-scratch retrain** (Claim C6): every metric within ~2× of the
  released weights on pdType 1, using a 3–4× shorter training schedule
  (132 s wall clock on 1× A100, seed 42).
* **Claims coverage**: 5 of 6 tested (C1, C2, C3, C5, C6 tested; C4
  latent-dimensionality / SVD analysis accepted as consistent with the
  released architecture, not directly re-verified).

## Compute + cost

* Host: ANL uicgpu (1× NVIDIA A100). Free institutional resource.
* Python 3.10, PyTorch 1.11.0 + CUDA, NumPy 1.23, SciPy 1.10.
* LLM-judge: `argo:gpt-5.2` via Argo proxy (http://127.0.0.1:44497/v1) —
  free ANL-internal endpoint.
* Zero paid model calls. Zero paid compute.

## Traceability

Every number in REPORT.md's results tables traces back to
`evidence/eval_released_results.json` (Stages 4–5) or
`evidence/retrain_pdType1_results.json` (Stage 6). No numbers were
introduced anywhere in the report that are not present in those two JSON
files. The LLM-judge verdict block in REPORT.md §4.4 is a verbatim excerpt
of `evidence/llm_judge_verdict.json`.
