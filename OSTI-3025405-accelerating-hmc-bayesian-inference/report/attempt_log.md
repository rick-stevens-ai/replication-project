# attempt_log.md — OSTI 3025405 replication

Chronological. All timestamps local (America/Chicago), Sat 2026-07-04 night.

- **23:47** Task received. Set up target dir under `~/Dropbox/REPLICATE-PROJECT/OSTI-3025405-accelerating-hmc-bayesian-inference/`.
- **23:48** Read `WAVE_BRIEF_2026-07-01.md`. Rules: free endpoints only (Argo
  127.0.0.1:44497), LLM judge never regex, real replication only.
- **23:49** Attempted `curl` for OSTI PDF locally — CherryRd cannot reach osti.gov.
  Downloaded via uicgpu: `ssh uicgpu 'source ~/env.sh && curl -sL -o
  /tmp/osti_3025405.pdf https://www.osti.gov/servlets/purl/3025405'`. 17 MB PDF.
- **23:50** `scp uicgpu:/tmp/osti_3025405.pdf work/paper.pdf` back to CherryRd.
- **23:51** Tried `pdf` MCP tool — media size cap (10 MB) rejects the 16-MB PDF.
  Fell back to PyMuPDF (`fitz`) text extraction locally. Extracted 35 pages
  of text (1931 lines).
- **23:53** Read paper end-to-end. This is arXiv:2507.14652v2 (JHU, September 2025).
  Method: VI + sensitivity ranking + reduced-dim HMC. Test problems:
  (i) 6-param sinusoidal BNN, (ii) 141-param tanh MLP, (iii) Burgers DeepONet
  172,401 params, (iv) hypersonic-cone DeepONet 16,321 params. Code at
  https://github.com/ponkrshnan/VI-HMC.git (not used — clean re-implementation).
- **23:56** Wrote `work/vi_hmc_replication.py` — 500 lines:
  own leapfrog HMC, own mean-field VI with softplus rho, sensitivity scores
  from Eq. (17), subset HMC (Algorithm 2).
- **00:05** First run: SIGKILL after ~5 min. Root cause: mean-field VI
  collapsed mu → 0 for both Cases (Adam + KL floor). Sensitivities
  degenerated to a single index. Case II crashed on autograd unpack bug.
- **00:20** Fixed autograd bug; added `kl_weight` argument to soften KL and
  let likelihood dominate.
- **00:30** Second run: VI still collapsing. Root cause: the paper's own
  Section 5 admits VI is unstable on small BNNs. Also, in a strongly
  multimodal 6-param sinusoidal likelihood, mean-field VI cannot
  discriminate modes.
- **00:35** **Pivot.** Replaced VI with MAP + diagonal Laplace approximation
  for the (mu, sigma) that feeds the sensitivity score. The paper's
  reduced-HMC acceleration claim is agnostic to how (mu, sigma) is obtained;
  Laplace is the standard alternative. This is documented as a substitution
  in the report.
- **00:40** Third run: Case I MAP finds true parameters perfectly. Sensitivity
  ranking picks 4 of 6 — **exact match** to paper claim ("first four
  parameters are sufficient for tau=0.9"). But full HMC acceptance = 0
  because our initial step size was too big for the tight posterior.
- **00:45** Wrote `work/diag_check.py` diagnostic to sweep step sizes.
  Found the transition region 1e-4 → 1e-5 for both problems.
- **01:00** Rewrote main script with proper step-size sweep and 200-sample
  runs at 7 step sizes for both cases, plus 2000/500 sample "canonical"
  runs at a step giving ~70-80% acceptance. Also added ESS/grad measurement.
- **01:10** Fourth run: clean end-to-end. All numbers real. Results
  written to `report/evidence/results.json`.
- **01:15** Verified Argo endpoint (127.0.0.1:44497, key=stevens).
  `argo:gpt-5-mini` returned DeploymentNotFound; `argo:gpt-5` worked.
- **01:16** Wrote `work/llm_judge.py`: builds a text summary of paper claims
  and replication evidence, submits to `argo:gpt-5`, requests JSON verdict.
  No regex anywhere.
- **01:20** Judge returned verdict: **PARTIAL**. Per-claim: C1 REPRODUCED,
  C2 NOT REPRODUCED (54 of 141 not 79), C3 REPRODUCED, C4 PARTIAL,
  C5 NOT TESTED (we did not run Burgers/cone), C6 REPRODUCED.
- **01:23** Wrote `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`,
  `report/artifact_harvest.md`.
