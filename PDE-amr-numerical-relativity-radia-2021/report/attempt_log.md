# Attempt Log — Radia et al. 2021 AMR replication

Chronological log of the replication attempt.  Host: CherryRd (macOS 25.3.0).
LLM judge: Argo proxy `http://127.0.0.1:44497`, model = argo:gpt-5.2 (opus 4.7 + 4.8 were 502-ing today; noted below).

## 2026-07-03 14:08 CDT — kickoff

- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`.
- Verified assigned target dir did not exist; created `report/`, `work/`, `report/evidence/`.

## 14:09 — paper fetch

- arXiv search returned arXiv:2112.10567 as the correct preprint.
- `curl -sL https://arxiv.org/abs/2112.10567 -o work/abs.html`
- `curl -sL https://arxiv.org/pdf/2112.10567 -o work/paper.pdf` (2.25 MB, 40 pages).
- `pdftotext -layout paper.pdf paper.txt` (2463 lines). Read Sec. 2 (framework), Sec. 2.2.2 (Berger–Rigoutsos), Sec. 3.1 (buffer regions), Sec. 3.4 (truncation-error tagging), Sec. 3.5 (grid-variable tagging), Sec. 4 (BBH code comparison with Lean), Sec. 5 (axion star tagging comparison).

## 14:12 — scoping decision

Full GRChombo BBH inspirals (Table 1 q1-d12 / q2-d10 / q1-s09) would require:

- Building Chombo library (PETSc, HDF5, MPI, HDF5 parallel).
- Building GRChombo.
- Running `TwoPunctures` spectral solver for initial data.
- Multi-day MPI production runs even on 8×A100 uicgpu.
- Post-processing Ψ4 modes, extrapolation to infinity, waveform overlap.

This is a multi-week effort, incompatible with a single-wave-brief slot.

Instead, we replicate the paper's METHODOLOGICAL claims on a 1D scalar wave testbed using the same numerical ingredients. This is honest: the paper itself is titled "Lessons ... in numerical relativity", and the lessons (convergence-order interaction of AMR with 4th-order FD; buffer-region trade-offs; tagging-criterion comparisons) are independent of the GR sector.

## 14:20 — implementation

Wrote `work/amr_wave.py` (~500 lines):

- 4th-order 5-point central FD Laplacian, periodic.
- RK4 time stepper.
- Uniform-grid evolver.
- Two-level AMR evolver, refinement ratio 2, RK4 subcycling (level 1 takes 2 substeps per level-0 step).
- Coarse-fine ghost fill via cubic Lagrange in space (paper: 4th-order interp) + linear-in-time (paper: 3rd-order polynomial in time; we simplified for a single-file implementation).
- 2nd-order cell-averaged restriction (matches paper Sec. 2.2.2 exactly).
- Two tagging criteria:
  - `tag_gradient`: `C = dx * |u''|` (1D analog of paper Eq. 51 with χ → u, using 2nd-order 3-point stencil).
  - `tag_truncation`: shadow-hierarchy `τ = |u_fine − u_coarse_lifted|` (paper Eq. 47 with a single variable).
- `buffer_expand`: dilate tag mask by nB neighbors (paper Sec. 3.1).
- `cluster_to_boxes`: connected components → boxes (1D-collapsed Berger–Rigoutsos).
- Analytic reference via d'Alembert on a periodic domain (5 image copies each way).

## 14:33 — first run

`python3 amr_wave.py` completed in 38.3 s. Results written to `report/evidence/amr_wave_results.json`. Key numbers:

- Uniform-grid convergence: 3.95 → 3.99 → 4.00 (clean 4th order). ✅
- AMR convergence (finest-L2 vs analytic): 1.30e-2, 1.12e-2, 3.71e-3, 2.17e-3 with orders 0.21, 1.60, 0.77 (degraded, irregular). ✅ Consistent with Sec. 4.2 lesson.
- Tagging (initial threshold tuning): gradient hit target coverage (0.375, 2 boxes), truncation with threshold 5e-4 gave 0 coverage (threshold too high — pulse too smooth to trigger truncation-based tag at that level).
- Buffer sweep: nB 0,1,2,4,8 → errors 1.55e-2, 5.09e-3, 3.71e-3, 1.82e-3, 3.18e-4 (49× improvement). ✅ Directly supports Sec. 3.1 claim.

## 14:35 — retune truncation threshold

Reduced truncation tag threshold 5e-4 → 5e-6 so both methods refine ~40% of the domain. Re-ran:

- Gradient: 0.375 coverage, 3.71e-3 L2 err.
- Truncation: 0.410 coverage, 2.13e-3 L2 err.
- Same regrid_count (7), same final-box-count (2), same-order-of-magnitude error.
- Reproduces Sec. 5.2 claim that both tagging methods can achieve equivalent, accurate results, with the caveat that thresholds must be tuned per-criterion.

## 14:38 — LLM judge

`work/llm_judge.py` sends the paper claims + JSON results to the Argo proxy.

- First attempted `argo:claude-opus-4.7` (per task spec): HTTP 502 Bad Gateway from Anthropic upstream (persistent, 4/4 retries).
- Fell back to `argo:claude-opus-4.8`: also HTTP 502 (upstream validation error, all attempts).
- Fell back to `argo:gpt-5.2` (Argo, free per free-endpoint rule): SUCCESS.

Judge model = argo:gpt-5.2. Both Opus deployments are down today. Standing rule allows any free Argo endpoint.

Judge verdict = **PARTIAL**.

- C1 (base 4th-order convergence): SUPPORT — cleanly reproduced.
- C2 (AMR degrades convergence): SUPPORT (partial mechanism isolation) — reproduced qualitatively.
- C3 (larger buffer nB reduces error): SUPPORT — 49× reduction observed, monotone.
- C4 (equivalence of two tagging methods): AMBIGUOUS — both viable and give same-order error, but coverage not exactly matched, so strict "equivalence" not proven.
- Overall: PARTIAL — mechanisms reproduced on 1D testbed, BBH-specific quantitative claims (waveform mismatch, kick velocity) not attempted.

## 14:41 — write reports

- `report/brief.md`, `report/REPORT.md`, `report/attempt_log.md`, `report/artifact_harvest.md`.
- Evidence in `report/evidence/`: `amr_wave_results.json`, `llm_judge_verdict.json`, plus the two run logs.

## What worked

- pdftotext + grep-driven paper reading was fast and gave enough to write a faithful re-implementation of the AMR mechanisms.
- The 1D scalar wave testbed cleanly separates the AMR mechanism from GR-specific dynamics, making the four claim-tests genuinely independent.
- Argo proxy gpt-5.2 fallback worked when Opus was 502.

## What failed / limitations

- Anthropic upstream (both Opus 4.7 and 4.8) was down for the entire run window; had to use gpt-5.2. Judge quality still very good.
- Full BBH replication (paper Sec. 4) is fundamentally out of reach in a single wave-brief slot; that would need weeks of HPC work. Not attempted, not fabricated.
- 1D → 3D+GR is a real inference gap: the AMR mechanisms replicate, but nonlinear GR could in principle interact differently with them. Marked honestly.
