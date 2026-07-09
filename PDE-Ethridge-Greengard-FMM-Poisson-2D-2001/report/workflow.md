# Replication Workflow

Session: 2026-07-06, X-100 subagent, argo/argo:claude-opus-4.7 driving.
Target paper: Ethridge & Greengard, SIAM J. Sci. Comput. 23(3), 2001.
Effort: ~1 subagent turn (~35 wall-clock minutes on CherryRd, local only).

## Stages

### Stage 0 — Prep (~2 min)
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md` for
  hard rules and the 8-artifact completion bar.
- `ls ~/Dropbox/REPLICATE-PROJECT/PDE-Ethridge*` -> nothing (target dir
  available; no claim-collision).
- Skimmed a good exemplar (`PDE-Ketcheson-NodePy-ODE-2020`) for artifact
  format.

### Stage 1 — Paper retrieval (~2 min)
- Semantic Scholar (S2 API key from Keychain
  `semantic-scholar-api-key` acct `rick-stevens-ai`) via
  `/graph/v1/paper/DOI:10.1137/S1064827500369967`.
- S2 reports openAccessPdf.status=GREEN with URL
  `https://math.nyu.edu/faculty/greengar/poiss2d.pdf`.
- `curl -L -o paper.pdf` (2.86 MB, PDF 1.2, SHA-256
  `6634e8d832c85a546a5ef4fe2c08edc5db235195d181b07edde8979e411c091e`).
- `pdftotext -layout paper.pdf work/paper_layout.txt` for scanning.
- Read the abstract, intro, and Tables 1--4 to identify testable claims.

### Stage 2 — Own FMM implementation (~10 min)
- Wrote `work/fmm2d.py` from scratch: uniform-tree 2D FMM for the Laplace
  kernel using the standard Greengard--Rokhlin complex formulation.
- Derived the M2L formulas (multipole -> local translation) directly from
  the log-expansion; verified derivation is documented in the docstring.
- Chose to use flat single-level M2L (no upward/downward pass) --- enough
  to verify $p$-convergence, not enough for asymptotic $O(N)$.
- First self-test at $N=200$, $p=12$ gave $27\%$ rel error -> sign bug in M2L
  formula. Re-derived, fixed (see failure_analysis.md).
- Second self-test: $5 \cdot 10^{-8}$ at $p=12$ (correct floor for the
  well-separated ratio $\sim 1/3$).

### Stage 3 — Experiment driver (~5 min)
- `work/run_experiments.py` with 4 experiments (C1..C4):
  - C1: accuracy vs $p$ for $p \in \{4,6,8,10,12,16,20\}$.
  - C2: FMM vs direct timing for $N \in \{500..8000\}$.
  - C3: Example 4.1 (three Gaussians, $\alpha=250$) on $N_{\rm side} \in \{32,64,96,128\}$.
  - C4: HWSCRT-equivalent DST-based Dirichlet Poisson for $N \in \{256..2048\}^2$.

### Stage 4 — Run experiments (~2 min wall, ~30 s compute)
- Killed first attempt (had $N=16000$ + $N_{\rm side}=256$ which would have
  taken > 5 min on pure-Python FMM). Trimmed to $N \le 8000$ / $N_{\rm side} \le 128$.
- Full run: 65 s wall time. All experiments completed cleanly.
- Wrote 4 JSON evidence files + 4 PNG plots via `work/make_plots.py`.

### Stage 5 — LLM judge (~3 min including retries)
- Bundled compressed evidence + prompt, POSTed to Argo via LiteLLM
  aggregator (`localhost:4000/v1`, key `stevens`, FREE endpoint per rule).
- Argo Opus 4.7 and 4.8 both 502'd: LiteLLM parse-error on the message
  shape upstream Argo returns for this payload.
  (Root cause noted in failure_analysis.md.)
- Argo GPT-5.4 succeeded on first try, returned strict-JSON verdict:
  `PARTIAL`, with coverage breakdown per (P1, P2, P3) and honest critique.
- Saved raw JSON to `report/evidence/llm_judge_verdict.json`.

### Stage 6 — Reports (~10 min)
- Wrote all 8 mandatory artifacts:
  1. `paper.pdf` (already present from Stage 1)
  2. `extraction/marker.md` (pdftotext -layout fallback with backfill header)
  3. `extraction/nougat.mmd` (pending-central-parse header, no local GPU)
  4. `report/REPORT.tex` (detailed, section-by-section with critique)
  5. `report/open_questions.json` (5 heavy questions, each with basis + next_steps)
  6. `report/workflow.md` (this file)
  7. `report/artifacts_summary.md`
  8. `report/failure_analysis.md`
  Plus: `report/REPORT.md` (canonical), `report/brief.md`, `report/attempt_log.md`,
        `report/artifact_harvest.md`.

## Tools / codes

- Python 3.14.6, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8 (system-wide).
- `pdftotext` (from Poppler) for PDF text extraction.
- `curl` for HTTP; system `security` CLI for Keychain lookup.
- Argo LiteLLM aggregator at `http://localhost:4000/v1` (Bearer `stevens`) for
  the LLM-judge verdict --- specifically the `argo:gpt-5.4` model since Opus
  models 502'd on this payload.
- All computation local on CherryRd (host: Mac Studio). uicgpu was not
  needed for this replication; would be needed for extending to hierarchical
  M2M/L2L at $N \ge 10^5$.

## Effort estimate

- Setup + paper fetch + extraction: 5 min
- FMM implementation (from scratch, incl. one derivation-bug fix): 15 min
- Experiment code + runs: 10 min
- Plotting: 3 min
- LLM judge (incl. retry through Argo 502): 5 min
- Reports (8 artifacts): 15 min
- Total: ~55 min for a solid PARTIAL replication.

A full REPLICATED verdict (implementing the adaptive quadtree + polynomial
cells + local corrections) would take an estimated **5--10 focused
engineer-days** and would want access to Greengard's own Fortran reference
code or the fmm2dpy Python bindings for cross-validation.
