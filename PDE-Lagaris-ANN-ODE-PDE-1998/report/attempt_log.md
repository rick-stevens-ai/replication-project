# Attempt log — 2026-07-05 CDT

1. Read the wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`)
   and confirmed rules: free endpoints only, real replication only, LLM-judge
   verdicts (no regex), write only inside target dir.

2. Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Lagaris-ANN-ODE-PDE-1998`
   with `report/{evidence}` and `work/` subdirs.

3. Environment: system Python 3.14 has no torch wheels yet; created a
   `python3.12 -m venv work/venv`, `pip install torch numpy scipy matplotlib`,
   then downgraded `numpy<2` for compatibility with the shipped scipy build.
   `torch.__version__ = 2.2.2`, `numpy.__version__ = 1.26.4`.

4. Downloaded the paper from arXiv: `physics/9705023 v1` →
   `work/lagaris_1998.pdf` (330 KB, 26 pages). Extracted plain text with
   `pdftotext -layout`. Read the exact statements of Problems 1, 3, 5, the
   trial-solution forms, and the paper's reported accuracy numbers (Table 1
   for Problem 5: neural 5e-7 at training AND at 30×30 interpolation; FEM
   2e-8 at training but 1.5e-5 at interpolation).

5. Implemented the trial-solution method in `work/lagaris_ann.py`
   (single-hidden-layer sigmoid MLP, 10 units, torch double, L-BFGS with
   strong-Wolfe line search). Trial solutions used exactly the forms in the
   paper:
   - P1:  Ψ_t = 1 + x N(x)
   - P3 (BVP):  Ψ_t = x·sin(1)·e^{-1/5} + x(1-x) N(x)
   - P5:  Ψ_t = A(x,y) + x(1-x)y(1-y) N(x,y),
          A built from the Dirichlet boundary functions via the paper's Eq. 18.

6. First run: P1, P3, P5 all trained. Errors on 200-point (200×200 for P5,
   actually 41×41 = 1681) dense evaluation grid:
     P1: max err 2.717e-05, RMSE 1.513e-05
     P3: max err 3.543e-06, RMSE 1.968e-06
     P5: max err 9.588e-07, RMSE 3.470e-07
   All within the same order of magnitude as the paper's Fig 2/5/Table 1.
   Interpolation FD comparator failed because scipy import chain hit
   `np.long` deprecation in numpy 1.26.

7. Replaced `scipy.interpolate.CubicSpline` with a self-contained natural
   cubic-spline implementation (no scipy dependency). Rerun succeeded:
     C4 comparator (Problem 1, 10-point trapezoid FD + cubic-spline interp):
       FD max err at training  = 7.989e-04
       FD max err dense (200)  = 1.864e-03
       ANN max err dense (200) = 2.717e-05
       ratio FD/ANN            = 68.6×
     → the paper's qualitative interpolation-superiority claim is confirmed.

8. Figures written: `fig_p1.png`, `fig_p3.png`, `fig_p5.png` (solution +
   pointwise |err|, log scale). All under `report/evidence/`.

9. Verified Argo proxy up (`/health` = healthy; `/v1/models` lists `argo:gpt-5`).
   Wrote `work/llm_judge.py` — pure stdlib POST to Argo, no external LLM libs.
   First attempt hit HTTP 400 because gpt-5 rejects arbitrary `temperature`.
   Fixed by omitting `temperature` for reasoning models.

10. LLM judge (`argo:gpt-5`) returned:
      coverage_score = 10
      agreement_score = 9
      verdict = REPLICATED
    Full output at `report/evidence/llm_judge.json`.

11. Wrote REPORT.md, brief.md, artifact_harvest.md, attempt_log.md.
    Total wall time end-to-end: ~5 minutes (30 s of that is the actual solves).
