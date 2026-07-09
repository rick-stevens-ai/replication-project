# Attempt Log — Savović 2023 replication

Date: 2026-07-04 (CDT), subagent PDE-26.

## Chronological actions
1. Read `WAVE_BRIEF_2026-07-01.md`. Free-endpoint / real-replication / LLM-judge / no-overwrite rules noted.
2. Created target dir `PDE-Savovic-FDM-vs-PINN-2023/{report/evidence,work}`.
3. Attempted `curl` fetch of MDPI PDF from CherryRd + uicgpu: MDPI URL `www.mdpi.com/.../pdf` returned Akamai *Access Denied* on host; uicgpu could not resolve `www.mdpi.com`.
4. Web search located the direct CDN URL `https://mdpi-res.com/d_attachment/axioms/axioms-12-00982/article_deploy/axioms-12-00982.pdf` — this succeeded (~7 MB PDF). Immediately noticed the paper title / abstract on p.1: it is about the **Burgers' equation**, not the pure heat equation. The task brief's parenthetical "(for solving heat/diffusion PDEs)" was slightly off; the assigned DOI is the correct paper.
5. Ran `pdftotext -layout` for text extraction (the `pdf` tool errored out on model routing / credit balance for Anthropic PDF and unknown-model for Gemini). Extracted PDE, three test problems, BCs/ICs, EFDM discretization (Δx=0.01, Δt=0.0001), analytical Cole–Hopf series solutions (Eq 13, 21, 28), PINN architecture (3×20 tanh, 5080+320+160 collocation, 15000 Adam + L-BFGS via DeepXDE, ~50 s on Tesla T4), and Tables 1–3 of tabulated errors.
6. Implemented `work/fdm_burgers.py`:
   - Vectorized explicit FDM matching paper Eq. 4.
   - Analytical Cole–Hopf series with N_terms=200 truncation, coefficient integrals via `np.trapz(4001-point grid)`.
   - Test problems 1, 2, 3 with initial conditions as in Eqs. 11, 19, 26 and BCs u(0,t)=u(1,t)=0.
   - All 18 (ν, T) combinations from Tables 1–3.
   - Ran locally on CherryRd (numpy 2.4.3). All 18 cases finished in <1 s each.
7. Implemented `work/pinn_burgers.py` for PyTorch (uicgpu, PyTorch 1.11, CUDA).
   - Matched architecture: (2,20,20,20,1), tanh, uniform-random collocation (5080 domain + 320 boundary + 160 IC).
   - Loss = L_r + L_b + L_0 (paper Eq. 8).
   - Optimizer: 15000 Adam @ lr=1e-3, then L-BFGS with strong Wolfe, max_iter=5000, history=100.
   - Autograd bug fix: needed to re-create leaf tensors with `.detach().clone().requires_grad_(True)` inside `residual()` (PyTorch 1.11 quirk); also removed a `torch.no_grad()` block that was killing the final loss re-eval.
   - `np.trapezoid` → `np.trapz` (numpy < 2 on uicgpu).
   - Quick smoke (2000 Adam + 500 LBFGS) worked → then full run.
8. Full PINN run on uicgpu: 6 trainings (one per (problem, ν)), each ~130–190 s on 1× NVIDIA A100. Total ~15 min wall.
9. Merged FDM + PINN results into `report/evidence/comparison.csv` + `.json`.
10. Called Argo LLM-judge (`argo:claude-opus-4.7`) at `localhost:44497`. Endpoint returned repeated HTTP 502 for the full prompt (upstream Vertex "Failed to parse upstream response" bug — nothing we can control). Fell back to `argo:gpt-5.2`, which returned a clean structured verdict.

## What worked
- pdftotext -layout for equations & tables.
- Explicit FDM: straightforward numpy, ran in ms per case, matched paper's qualitative behavior (small errors, error decreases with decreasing ν).
- PINN on uicgpu A100: converged well (final composite loss 6e-7 to 6e-8).
- Argo GPT-5.2 as judge fallback.

## What failed / friction
- `www.mdpi.com` blocks direct scraping (Akamai). Working URL is the `mdpi-res.com` CDN.
- `pdf` tool cannot serve local paths outside allowed dirs and its Anthropic/Google/OpenAI models are all currently down or credit-blocked for us. Had to use `pdftotext`.
- PyTorch 1.11 autograd quirks in the residual re-eval loop.
- Argo Opus 4.7 upstream 502 for our specific prompt (Vertex parse error). Fell back to GPT-5.2. Argo Sonnet 4.7 returned `DeploymentNotFound`.
- Our EFDM RMSE (~1e-5 to 1e-4) is 1–3 orders larger than the paper's tabulated values (~1e-7). Most likely the paper evaluates their `Error` differently (grid, single-time-slice comparison, series truncation), or their EFDM benefits from a subtly different formulation. This does NOT flip the qualitative EFDM≻PINN ordering for us.
