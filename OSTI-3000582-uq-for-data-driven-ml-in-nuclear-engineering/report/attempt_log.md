# Attempt Log — OSTI 3000582 replication

All times CDT (America/Chicago).

## 2026-07-02

- 20:07  Received wave assignment (OSTI-3000582, rank 45/TOPUP50, TOPUP50-hardest).
         Read `WAVE_BRIEF_2026-07-01.md` → hard rules understood: free endpoints
         only, real replication only, LLM-judge verdict, preserve completed
         work.
- 20:07  Confirmed target dir does not exist; created
         `~/Dropbox/REPLICATE-PROJECT/OSTI-3000582-uq-for-data-driven-ml-in-nuclear-engineering/{report/{evidence,},work/}`.
- 20:09  `ssh uicgpu` + `source ~/env.sh` (needed for cluster HTTPS proxy
         `<lan-host>:3128` — first curl failed with DNS error because I
         forgot the proxy env). Fetched OSTI PDF (3.9 MB, PDF 1.5). scp'd
         copy to workspace/work/paper.pdf.
- 20:10  Tried the `pdf` analyzer tool for structured extraction — failed
         because paid Anthropic/OpenAI PDF backends are exhausted, and the
         path guard didn't cover Dropbox anyway. Fell back to `pdftotext
         -layout` — 2368 lines of clean text extracted (Wu et al., 41 pp).
- 20:12  Parsed paper: it's a perspective + demo paper with a very concrete
         Section IV.A "Analytical GP" toy benchmark (μ(x)=x+0.02x²+5sinx,
         Matern 5/2 length 0.2, tent σ(x), 1000 points from 10 GP
         realizations). Section IV.B (SAFARI-1) needs private data. Decision:
         reproduce Section IV.A completely with all six UQ methods.
- 20:13  On uicgpu, no ready-made env has scipy+pytorch+xgboost+pyro. Broke
         `unnt-repl` (GLIBCXX version mismatch on scipy). Created fresh
         `osti3000582` env via mamba/conda-forge (numpy 1.26, scipy 1.17,
         sklearn 1.9, torch 2.12+cu129, xgboost 3.2, pyro 1.9) — 8 A100s
         visible.
- 20:14  Wrote `work/replicate_uq.py` (~500 lines) implementing all six UQ
         methods with paper-specified hyperparameters:
           * Mean-DNN [200,500,500,200] tanh + L2 + Adam
           * DE-head predicting (μ, σ) with Gaussian NLL, ensemble of 10
           * MCD DNN with dropout=0.25
           * BNN via Pyro PyroModule + AutoDiagonalNormal + SVI
           * Split-CP + SRCP on top of DNN and XGBoost
           * XGBoost with 200 trees, max_depth=12
           * GP with default RBF + White kernel (paper: "different kernel
             than the one used to generate the data")
         First run: two bugs
           (1) matern52 shape mismatch when both args have length 1 → fixed
               by explicit `.reshape(-1, 1)`.
           (2) BNN Pyro sample sites collided (`nn.ModuleList` of
               PyroModule[nn.Linear] gave all layers the sample-site name
               `weight`) → fixed by naming each layer `lin0..lin3` via
               `setattr`. Also forced CPU for BNN (Pyro sampled params
               default to CPU; tiny 3×10 model, no perf cost).
- 20:16  Full 6-method run complete in **56 s** on 1 A100. All 6 methods
         trained + evaluated. Coverage 0.92–0.99, all near the 95% target.
- 20:16  Generated `work/make_figs.py` → 6-panel comparison figure + true-only
         dataset figure. Pulled results into `report/evidence/`.
- 20:18  LLM-judge (Argo `argo:gpt-5` via localhost:44497, FREE) called with
         detailed evidence. Verdict returned: **PARTIAL** (coverage 4/5,
         agreement 3/5, 4 clean + 2 partial claims). Saved to
         `report/evidence/llm_judge_verdict.json`.
- 20:20  Wrote REPORT.md, brief.md, artifact_harvest.md.
- 20:21  Cleanup: `~/.openclaw/workspace/tmp_osti_*` staging files removed.

## Failure log
- (small) BNN device mismatch — Pyro sampled parameters live on CPU by
  default; can't just `.to(DEVICE)` a `PyroModule` and expect the sample
  sites to move. Workaround: run BNN entirely on CPU (tiny model, no cost).
- (small) `nn.ModuleList` with `PyroModule[nn.Linear]` collides sample-site
  names because each `.weight` / `.bias` fires `pyro.sample("weight", ...)`
  under the same module scope. Give each layer a unique attribute name.
- (external) `pdf` tool + `image` tool both routed to paid Anthropic/OpenAI
  endpoints and failed with 400 (credit balance). Free path: `pdftotext` for
  the paper, human-readable figure saved to disk for later inspection.
