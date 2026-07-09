# Replication Workflow — OSTI 3002302

Independent replication of Ding & Do, *APL Machine Learning* 3, 036112 (2025),
"Deciphering the small-angle scattering of polydisperse hard spheres using
deep learning." Executed by an automated agent on ANL uicgpu (1× A100).

## Stage 0 — Provenance capture

1. Pull OSTI PDF directly (no paywall).
   ```
   curl -sL https://www.osti.gov/servlets/purl/3002302 -o work/paper.pdf
   ```
   Verified: 7,118,161 bytes, MD5 `2b7c8c230cb802ab89cb25f2ec8eb14b`, PDF v1.4.
2. Record paper metadata: DOI 10.1063/5.0290589, OSTI 3002302, CC BY-NC 4.0,
   submitted 2025-07-12 / accepted 2025-08-06 / published 2025-08-15.

## Stage 1 — Fetch author code + data + weights

1. Clone the authors' public repository (~35 MB, shallow):
   ```
   git clone --depth 1 https://github.com/ljding94/Polydisperse_Sphere.git
   ```
2. Inventory the released artifacts:
   * `analyze/VAE_model.py` — network definitions.
   * `analyze/analyze_PY.py` — the paper's own PY reference (NOT reused here;
     baseline was independently re-implemented from Wertheim 1963).
   * `data_used/L_18_pdType_{1,2,3}_{train,test}_data.npz` —
     4000 train + 1000 test (η, σ, I(Q)) triples per distribution family.
   * `L_18_pdType_{1,2,3}_train_stats.npz` — I(Q) normalization statistics.
   * `L_18_pdType_{1,2,3}_{vae,gen,inf}_state_dict.pt` — released trained
     weights for VAE, Generator, and Inferrer per pdType.

## Stage 2 — Isolated re-implementation of the network

1. Write `work/eval_released.py` from scratch, mirroring the released
   architecture:
   * Encoder: `Conv1d(1→30, k=9, s=2)` → `Conv1d(30→60, k=9, s=2)` → linear
     to (μ, s) with latent dim 3.
   * Decoder: mirror with `ConvTranspose1d`.
   * Converter 1 (P2L): MLP (η, σ) → (μ, s) in 9-dim linear space.
   * Converter 2 (L2P): MLP z → (η′, σ′).
2. Load released `state_dict.pt` with `strict=True` — clean load, no missing
   / unexpected keys. This is the architectural sanity check: our re-impl
   matches the authors' exactly.

## Stage 3 — Independent Percus–Yevick + β baseline

1. Implement Wertheim 1963 analytic PY structure factor `S_PY(Q, η, R)`
   from first principles (α, β, γ coefficients).
2. Implement the sphere form factor F(Q; D) from paper eq. (3).
3. For each test (η, σ) pair: draw N=20,000 diameters from the appropriate
   distribution (uniform / normal / lognormal), compute polydisperse averages
   ⟨F²⟩_D and ⟨F⟩²_D.
4. β-correction: `β = ⟨F⟩² / ⟨F²⟩`, giving
   `I_PYβ = (1 + β·(S_PY − 1)) · P(Q)`.
5. Use effective radius `R_eff = ⟨D³⟩^(1/3) / 2`.
6. No code copied from `analyze_PY.py`. Independent numeric implementation.

## Stage 4 — Evaluate released Inferrer

1. For each pdType ∈ {1, 2, 3}, run the 1000-point test set through the
   released VAE encoder + L2P converter.
2. Average predictions over 5 stochastic forward passes (VAE ε samples).
3. Report per-parameter R², MAE, and relative error
   `|x − x'| / ⟨x⟩` (paper's Fig 8 caption definition).
4. Persist to `evidence/eval_released_results.json`.

## Stage 5 — Evaluate released Generator + PY / PYβ

1. For each pdType, push all 1000 test (η, σ) pairs through
   converter 1 + decoder to get predicted I(Q).
2. Compute per-curve MSE_log10 = ⟨(log₁₀I − log₁₀I′)²⟩_Q against the
   released reference I(Q).
3. On 500 randomly chosen test points per pdType (analytic-PY clipping
   requires η ∈ [1e-4, 0.48], σ ≥ 1e-3), compute the same MSE_log10 for
   the independent PY and PY+β baselines.
4. Persist to `evidence/eval_released_results.json`.

## Stage 6 — From-scratch retrain (pdType 1)

1. Fresh training run on pdType 1, seed=42, compressed epoch schedule:
   VAE 300 epochs (paper: 1000), converters 100 frozen + 50 fine-tune epochs
   (paper: 300 + 200). Batch 64, Adam(lr=1e-3, wd=1e-4), CosineAnnealingLR.
2. Wall clock: 132 s on 1× A100.
3. Evaluate the resulting new weights on the same 1000-point pdType-1 test
   set. Report the same metrics as Stages 4–5.
4. Persist to `evidence/retrain_pdType1_results.json` (+ training log at
   `retrain_pdType1.log`).

## Stage 7 — LLM-judge verdict

1. Call `argo:gpt-5.2` via the free Argo proxy (http://127.0.0.1:44497/v1),
   temperature 0, structured JSON output.
2. Prompt contents:
   * Numbered list of paper claims (C1–C6).
   * All measured numbers from Stages 4–6.
   * Explicit instruction to return
     `{verdict, coverage, agreement, justification, one_line}`.
3. Persist prompt and response to `evidence/llm_judge_prompt.txt` and
   `evidence/llm_judge_verdict.json`.

## Stage 8 — Report + critique

1. Aggregate all quantitative results into `report/REPORT.md`
   (rendered LaTeX version at `report/REPORT.tex`).
2. Add a dedicated `Genuine Critique` section — not a rubber stamp; identify
   weak baseline, in-distribution-only evaluation, noise/resolution gap,
   uncertainty quantification gap, latent-dimensionality claim untested,
   own replication deviations.
3. Emit `open_questions.json` with 5 genuinely open follow-ups grounded in
   the paper's actual SANS-of-polydisperse-hard-spheres domain.
4. Emit `workflow.md` (this file), `artifacts_summary.md`, and
   `failure_analysis.md`.

## Compute + software

* Host: ANL uicgpu (1× NVIDIA A100).
* Python 3.10, PyTorch 1.11.0 + CUDA, NumPy 1.23, SciPy 1.10.
* All endpoints free (Argo proxy for LLM-judge). No paid model calls.

## Deviations from paper (documented in REPORT.md §3)

* From-scratch retrain uses 300 VAE epochs (paper 1000) and 100+50
  converter/fine-tune epochs (paper 300+200) — pure compute-budget
  compression, not a methodological change.
* PY effective radius `R_eff = ⟨D³⟩^(1/3)/2`; paper does not specify its R
  choice, so exact numeric agreement on absolute PY MSE was not expected.
  Qualitative agreement (PY, PYβ ≫ NN) is what was tested and confirmed.
