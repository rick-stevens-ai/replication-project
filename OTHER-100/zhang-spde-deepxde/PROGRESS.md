# PROGRESS — Zhang SPDE DeepXDE Re-pass

## 2026-06-23 (this session)

### Pass-1 identity check
- Pass 1 report at `report/REPORT_v2.md` cited the correct paper in its appendix
  (Zhang/Lu/Guo/Karniadakis JCP 397:108850, NN-aPC) but actually replicated
  examples from a *different* Zhang paper — arXiv:1905.01205 "Learning in
  Modal Space" (stochastic advection / Burgers / reaction–diffusion).
- That cross-paper mismatch is the root cause of the LOW agreement (4/10):
  the prior pass measured a parametric PINN against modal-decomposition
  results from a paper this folder isn't supposed to be about.
- Decision: preserve pass-1 verbatim as `REPORT.pass1.md`. Restart against
  the *real* paper (arXiv:1809.08327 / JCP 397:108850).

### Re-pass plan
1. Fetched arXiv:1809.08327 PDF.  → `paper/zhang_1809.08327_quantifying_uncertainty.pdf`.
2. Parsed via `pdftotext -layout`. → `PARSER_PROVENANCE.md`.
3. Enumerated all 2 numeric tables in the paper:
   - Table 1: Inverse stochastic elliptic, 1st vs 2nd-order aPC errors.
   - Table 2: Active learning steps 0/1/2/11 (skipped this pass — 50k epoch,
     stateful sensor placement, scope explicitly outside re-pass budget).
4. Built a single-script replication at `code/repass/nn_apc_replication.py`
   covering Example 4.1.1 (forward stochastic Poisson) and Example 4.1.2
   (inverse stochastic elliptic, Table 1, both aPC orders).
5. Set up isolated venv with `numpy<2`, `scipy<1.13`, `torch 2.2.2`,
   `deepxde 1.10.0` (CPU only — A100 not needed at this size).
6. Smoke test (1000 ep) ran clean on all three sub-experiments.
7. Full run (20k epochs each, ~30 min) launched in background.

### Coverage uplift target
- Pass 1: cov=6 (against WRONG paper). Agreement=4/10.
- Re-pass aim: cov ≥ 8 against the right paper, with honest agreement
  diagnosis for each table-1 entry.
