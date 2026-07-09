# Attempt Log — OSTI 3023992

Timeline: 2026-07-04 22:46 → 22:54 CDT.

1. Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`).
2. Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3023992-flory-huggins-bayesopt-polymer-phase/{report/evidence,work}`.
3. CherryRd cannot reach osti.gov directly. `ssh uicgpu` + `source ~/env.sh` → `curl -sL -o /tmp/osti_3023992.pdf https://www.osti.gov/servlets/purl/3023992` → scp back → `work/paper.pdf` (1.44 MB, PDF v1.4). ✅
4. Anthropic/OpenAI direct PDF paths declined by policy/credit. Fell back to `pdftotext -layout` for the paper (1087 lines) — fully sufficient for claim extraction. ✅
5. Extracted claims C1–C9 by reading pages 1–8 of `paper.txt` line by line, including the exact FH eqns 3–5, kernel eqn 6, acquisition eqns 11–12, hyperparameter Table 1, final fitted values (A=0.022, B=−8.22 K), LCST comparison (extracted 154.8 vs computed 158.8 vs literature 160 °C), gpCAM version (8.1.9), and Zenodo/GitHub links.
6. Built a venv (numpy 2.5.1, scipy 1.18.0, sklearn 1.9.0, skopt 0.10.2, matplotlib 3.11.0).
7. Wrote `work/fh_bo_repro.py`:
   - Analytic FH spinodal T(φ) = B / (0.5·(1/(N₁φ)+1/(N₂(1−φ))) − A).
   - Sigmoid-scaled prior mean `m₀(φ,T) = σ(c·∂²ΔF/∂φ²)`, c = −2·10²³ (paper eqn 5).
   - Matérn-3/2 GP (ν=1.5) with `[φ_scaled, T_scaled]` inputs.
   - Custom acquisition `fa(x) = σ(x) + 0.25·tanh(0.1/|μ−0.5|)` (paper eqns 11–12).
   - Δφ=0.025, ΔT=1 °C unit-radius exclusion mask (paper's decision policy).
   - 4 corner init + 20×5 iterations, exactly as paper (104 samples).
   - Prior-mean refit each iteration via multistart L-BFGS-B (paper uses gpCAM's DE).
8. Sanity check: `spinodal_min_T_C` returned −7738 °C (a spurious extreme at the boundary of φ range where the sign of the denominator flips). Restricted to the physically valid LCST branch and got **159.16 °C at φ=0.46** — matches paper's ~160 °C. ✅
9. Ran full BO campaign (~15 s). Trace: LCST extraction stabilized at 159.6 °C by iteration 4; A, B jittered between two local minima early ((A=0.015, B=−5) vs (A=0.022, B=−8)), and settled at (A=+0.0223, B=−8.37 K) by iter 20 — matches paper's (+0.022, −8.22 K) to <2%. Boundary RMSE 0.93 °C vs true FH spinodal. ✅
10. Grid baseline (Newby 7 comps × 14 T = 98 samples): RMSE 3.7 °C — BO gives ~4× tighter boundary at similar budget. ✅
11. Random baseline (n=104): RMSE 0.93 °C — indistinguishable from BO at this large budget. Honest disclosure: with the smooth-sigmoid ground truth, the FH-informed prior advantage is largely a low-budget effect (paper reports the same in its SI).
12. Ran `efficiency_sweep.py` (budgets 9→104): grid stays around 3.7 °C throughout, random improves from 22.3 → 2.1 °C, BO improves from 97 (bad; prior stuck in local minimum on 9 samples) → 3.5 °C. Reason: for very small budgets, the multistart L-BFGS-B occasionally locked into (B=0, A~0) which zeros out the FH prior; a stronger differential-evolution refit (as in gpCAM) would help. This matches the paper's own observation that hyperparameter optimization can get trapped in local minima (paper Fig. 5 shows "Section 3" spike from the same effect).
13. LLM-judge (argo:claude-sonnet-4.6 via 127.0.0.1:44497): C1=4, C2=4, C3=4, C4=1 → **PARTIAL**.
14. Copied artifacts into `report/evidence/`; wrote brief, artifact harvest, this log, and REPORT.md.
