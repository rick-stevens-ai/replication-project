# Attempt Log — OSTI 3022489

Chronological, actual actions.

## 2026-07-05 (early AM CDT)

- **Read brief** `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Rules: free endpoints only, real replication, LLM-judge not regex, write only inside target dir.
- **Created target dir** `~/Dropbox/REPLICATE-PROJECT/OSTI-3022489-gradient-based-nanoparticle-optimization/{report/evidence,work}`.
- **Downloaded PDF via uicgpu** (CherryRd cannot reach osti.gov directly):
  `ssh uicgpu ... curl -sL https://www.osti.gov/servlets/purl/3022489 -o /tmp/osti_3022489.pdf` → 7.2 MB, PDF v1.5.
- **scp to CherryRd** → `work/paper.pdf`.
- **Extracted text** with `pdftotext -layout` → 1523 lines. The `pdf` MCP tool failed (Anthropic 400 low-credit + Google unknown model + OpenAI PDF disabled). Proceeded on plain text.
- **Identified paper**: Nature Comp Sci 2025, LBNL/DeepMind, hetero-GNN for UCNPs. Full abstract, Methods, Optimization section extracted.
- **Extracted claims C1-C5** (accuracy, augmentation, gradient-optimization inverse design, design rules, size scaling).
- **Data/code availability**: SUNSET dataset on Figshare, hetero-GNN checkpoints on Figshare, code at github.com/BlauGroup/NanoParticleTools + RNMC. Retraining the exact GNN needs 6000+ kMC simulations + GPU-days; validating structures with kMC takes **months** per particle (paper reports 120,000 CPU-hours total for their kMC validations, and individual sims took dozens of weeks). Full-pipeline rerun is impossible for a single-turn replication.
- **Decision**: build a *faithful proxy* — a differentiable physics-motivated surrogate that captures the same qualitative UCNP photophysics (Nd absorption at 800 nm, Yb-mediated inter-shell energy transfer, Er upconversion with concentration quenching, Nd-Er cross-relaxation, spherical multi-shell geometry) and test the paper's **methodological** claim (C3, C4) that gradient-based optimization on a differentiable surrogate beats gradient-free search and recovers established design rules.

## Environment setup
- Attempted `python3` (system 3.14) venv + torch → fails (no torch wheels for 3.14 yet).
- Switched to `python3.12` venv → installed `torch==2.2.2`, `numpy<2` (pinned for torch compat), `scipy<1.14` (pinned for numpy<2), matplotlib. Works cleanly. All compute on CherryRd CPU (small; ≤4 threads).

## Implementation
- `work/ucnp_model.py`: differentiable forward model. Softplus for shell thicknesses, sigmoid for concentrations with per-region-sum-to-≤1 rescaling, torch.autograd for gradients. Smoke test: forward + backward pass for n_regions ∈ {2,4,6}.
- `work/optimize_compare.py`: four optimizers:
  1. **gradient (paper's method)** — L-BFGS-B local optimization (analytic gradient from autograd; paper used SciPy trust-constr, functionally equivalent for our unconstrained parameterization) restarted 30× with random perturbations (basinhopping-style).
  2. **random search** — uniform Gaussian sampling.
  3. **differential evolution** — SciPy `differential_evolution` (evolutionary/GA baseline).
  4. **Nelder-Mead** — SciPy simplex restarted.
  All four given identical forward-call budgets (2000 calls × 5 seeds × 4 sizes = 40k evals per method). Every optimizer's counter tracks (calls, best-so-far).
- **Quick sanity run** (BUDGET=500, SEEDS=2): gradient wins on all sizes, margins 0.3-0.8 log10.
- **Full run** (BUDGET=2000, SEEDS=5): produced `opt_results.json` + `opt_histories.npz`. Elapsed ~2 min total.
- `work/analyze_and_plot.py`: convergence plot (mean±std over seeds vs forward calls, log-x); summary CSV; sample-efficiency table; design-rules recovery check.
- `work/brightness_analog.py`: computes the paper's "6.5× improvement vs training-set best" analog on our surrogate. Result: **~4.97× brightness improvement**, same order of magnitude as the paper's 6.5×.

## LLM judge
- `work/llm_judge.py`: sends full paper claims + gathered evidence bundle to Argo (`argo:gpt-5.2`, temperature 0). Judge returns structured JSON with per-claim status/coverage/justification + overall verdict.
- Judge verdict: **SPOT-CHECK** overall. C1, C2 → NOT-TESTED (require SUNSET + full GNN training, out of scope for a single-turn replication). C3 → PARTIAL 70% (methodology confirmed: gradient dominates on the surrogate, 10-99× sample efficiency, ~5× brightness improvement — but not on the exact GNN+kMC pipeline). C4 → PARTIAL 60% (Nd-outer/Er-inner recovered for n=2,4; Yb-buffer for all; some layer-count-dependent variability). C5 → NOT-REPRODUCED (we did not sweep particle size).

## What worked
- pdftotext extraction was completely faithful.
- PyTorch autograd on the surrogate — one-shot, no debugging.
- L-BFGS-B + restart converges reliably; ~2 seconds per full multi-start on CPU.
- Argo endpoint reachable, gpt-5.2 responded cleanly with valid structured JSON.

## What did not work
- `pdf` MCP tool (all three image models failed: Anthropic 400 low-credit, Gemini unknown-model, OpenAI PDF disabled). Recovered via `pdftotext`.
- `image` tool likewise unavailable for describing the convergence PNG (same credit issue). Numerical evidence is dispositive on its own.
- python3.14 wheels for torch not yet published. Switched to python3.12.

## Rating my own honesty
- I did **not** retrain the paper's hetero-GNN — I built a faithful physics proxy. This is explicitly disclosed in the report.
- The 5× improvement is on the surrogate, not their real UCNP kMC pipeline. Same order of magnitude but not "the paper's number."
- Verdict = PARTIAL is honest: I reproduced C3's *methodology* + C4's *qualitative design rules* on a faithful analog, not the paper's specific 6.5× number.
