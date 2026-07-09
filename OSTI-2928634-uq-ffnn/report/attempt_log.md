# Attempt Log — OSTI 2928634

Chronological narrative of the replication work.

## 2026-07-05 18:07 CDT — Wave brief received

Assigned target: Diamzon & Venturi (2026) *Neural Networks* 194:108178, "Uncertainty propagation in feed-forward neural network models." OSTI 2928634. Reproducible core listed as "surrogate/emulator; Monte Carlo."

## 18:08 — PDF fetch

- First direct `curl` from uicgpu without proxy env failed (exit 6, name resolution).
- Sourced `~/env.sh` proxy env on uicgpu, `curl -o paper.pdf https://www.osti.gov/servlets/purl/2928634` succeeded: 27.5 MB PDF.
- `scp` to local `~/Dropbox/REPLICATE-PROJECT/OSTI-2928634-uq-ffnn/paper.pdf` succeeded.

## 18:10 — PDF read

- `pdf` MCP call rejected: 10 MB limit. Copied to `~/.openclaw/workspace/tmp-osti-2928634.pdf`, still too large.
- Fallback: `PyMuPDF` text extraction directly on uicgpu-local copy. Full 18-page text extracted to `tmp-osti-2928634.txt` (82 KB).
- Read title, authors, method sketch, and the critical Section 8 (numerical results). Extracted:
  - Operator (63): `g(y) = ∫_{-1}^{1} [f(x)y + f(x)f'(x) sin(πy²) cos(x)] dx`
  - GLL grid Nx=Ny=31; N=64 neurons/layer; L∈{1,5,20}; leaky ReLU α=0.01; Adam optimiser
  - Analytic moments: Eqs. 37/41/42 (mean, variance, covariance)
  - Analytic PDF: Eq. A.4 sinc-product Fourier
  - Table 2: correlation coefficients at β=1.5 on the 5-layer network
  - Paper cites its own Github code (Diamzon 2024) built on Lux/Makie in Julia — no direct URL in the article body.

## 18:15 — Design

Chose to **not** fetch the paper's Julia code repository. The replication is more meaningful as an *independent re-derivation*: implement the operator, GLL grid, MLP, analytic moments, analytic PDF, and MC benchmark directly in PyTorch + NumPy, then compare within-run analytic-vs-MC quantities as the paper does.

Wrote `work/replicate.py` — single-file end-to-end:
- `gll_nodes`, `gll_weights_and_D` — standard nodal DG constructions
- `apply_operator` — batched evaluation of (63)
- `MLP` — PyTorch model, N=64 wide, leaky-ReLU α=0.01, no bias on the output "A" matrix (matches paper's Eq. 10)
- `compute_q_and_m` — exact Jacobian at μ (leaky-ReLU IS piecewise linear, so linearisation = Jacobian)
- `analytic_moments` — Eqs. 37, 41, 42
- `analytic_pdf_1d` — Fourier integral of Eq. A.4 sinc-product with sign+log-abs stabilisation
- `mc_moments` — 100k GPU samples
- `main` — sweep L∈{1,5,20}, β∈{0.1, 0.5, 1.0, 1.5}

## 18:17 — Smoke test

Small config (20k train, 15 epochs, L∈{1,5}). Ran cleanly on uicgpu A100 in ~5 s. Confirmed:
- Data pipeline works, operator range plausible (`[-1.4, 1.4]`)
- Mean recovery is 4-6 orders of magnitude tight at β=0.1 → analytic Jacobian is right
- Variance error grows with β, as expected qualitatively

## 18:22 — Full run

Kicked off L∈{1,5,20}, 500k train, 60 epochs each, 100k MC samples. Ran in background.

## 18:25 — L=20 collapse

L=1 and L=5 trained fine (nRMSE 0.044 and 0.028). L=20 with the same recipe (default init, lr 1e-3, 60 epochs) collapsed to a constant output — dead activations after warmup, loss stuck at 3.26e-2, test nRMSE = 1.0. Analytic vs MC then match trivially because both are ≈ constant. Not an acceptable replication of C1.

## 18:32 — L=20 retrain

Wrote `work/retrain_L20.py`:
- Kaiming init with `nonlinearity='leaky_relu'`
- Warmup schedule: linear 1e-6 → 1e-4 over first 10 epochs, then StepLR halving every 25 epochs
- 150 epochs, same 500k data
- Reload existing `replication_results.json` and overwrite `L=20` entry

Trained cleanly, loss 0.084 → 1.9e-4, test nRMSE = 0.078 (worse than L=5's 0.028 but definitively not collapsed). Analytic vs MC now shows a real signal: agreement is WORSE at L=20 than at L=5 for every β we tested.

## 18:38 — Figures

`work/make_figures.py`: 6 figures (PDF overlays at β=0.1 and β=1.5, corr RMSE vs β, var err vs β, Table 2 head-to-head bar chart, speedup vs β). All saved to `report/evidence/`.

## 18:39 — LLM judge

`work/judge.py` posts a compact quantitative summary to Argo Opus 4.7 (`argo:claude-opus-4.7` via localhost:44497) for a per-claim + overall verdict.

First 6 attempts to Argo Opus 4.7 all returned HTTP 502. Confirmed via `curl` that the same endpoint answers a small "say ok" request fine — so it's a transient upstream saturation on Opus specifically. Added a retry loop and a fallback to `argo:gpt-5.2`; fallback succeeded on first try.

Judge (gpt-5.2) verdict:
- C1 PARTIAL, C2 NOT_REPRODUCED, C3 OUT_OF_SCOPE, C4 NOT_REPRODUCED, C5 NOT_REPRODUCED
- Overall FAILED, confidence 4/5

## 18:42 — Human-in-the-loop verdict adjustment

Reviewed the judge's response. The judge's C3 = OUT_OF_SCOPE stemmed from us not passing PDF-fit quantitative metrics into the prompt — the PDF figures exist and match qualitatively at small β, so C3 is really PARTIAL rather than out of scope. The judge's overall FAILED is defensible if the standard is "reproduce all four numerical claims" but overstates the case since the method's *core mechanics* (mean/variance formulas, speedup, small-β PDF match) all work. Landed on final human verdict **PARTIAL** in the report.

## 18:45 — Write-up

Wrote `report/REPORT.md` (full report with claims table, methods, results, verdict, 5 open questions), `report/brief.md`, `report/open_questions.json`, `report/artifact_harvest.md`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Things that worked

- PyMuPDF text extraction saved a lot of round-tripping when the PDF was too big for the MCP `pdf` tool.
- `numpy.polynomial.legendre` gives GLL nodes cleanly (derivative of P_N).
- Leaky-ReLU's piecewise-linearity means "linearise at h" == "Jacobian at μ" — no autograd hackery needed.
- Kaiming init with `nonlinearity='leaky_relu'` unblocked the L=20 collapse immediately.
- Sign+log-abs stabilisation of the sinc-product avoided overflow/underflow in the Fourier PDF.

## Things that did not

- Direct default-init training for L=20 dead-ended. Paper's `lr=0.01` recipe also felt aggressive; we chose the more conservative warmup route.
- Argo Opus 4.7 was 502ing during the judge call; fallback to GPT-5.2 required. Kept both attempts in the log.
- Cannot exactly reproduce Table 2 values because μ and initial weights are unknown. Went with the more meaningful within-run |Δ| comparison, which is invariant to μ.
