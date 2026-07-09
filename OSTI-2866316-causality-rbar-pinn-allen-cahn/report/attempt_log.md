# Attempt log — OSTI 2866316

1. Read WAVE_BRIEF_2026-07-01.md + OSTI100_TOPUP50 list. Skipped all already-done IDs (ranks 1-8 done) and existing OSTI-* dirs. Highest still-undone with reproducible computational core + OA PDF = rank #9, OSTI 2866316 (Causality-RBAR PINN for Allen-Cahn).
2. Fetched OA PDFs for candidates 2866316 / 2552927 / 3012815 via `https://www.osti.gov/servlets/purl/<id>` through **uicgpu** proxy (CherryRd times out on osti.gov; needed `source ~/env.sh` on uicgpu — first curl failed exit 6 host-resolve until env sourced). pdftotext each.
3. Chose 2866316: clean, exactly-specified causality algorithm (Eqs 9-11) with ε=10; canonical Allen-Cahn testbed that has a computable spectral reference (no proprietary data needed for the mechanism test). NOTE paper's own benchmark is COMSOL (proprietary) → tested the mechanism on the origin (ref [18]) 1D Allen-Cahn benchmark instead.
4. Wrote `allen_cahn_causal_pinn.py`: Fourier-spectral IMEX reference solver + vanilla PINN + causal PINN (Eqs 9-11 exact, ε=10). Ran on uicgpu GPU.
5. **Perf issue #1:** first version looped 100 slabs in Python per iter → ~100s and stuck at it=0. Killed.
6. **Perf issue #2:** vectorized slabs into one (Nt×Nx) autograd pass; still ~40s/1000 iter at 100×256. Reduced to 64 slabs × 200 pts, 12k iters each to fit budget. Killed the 20k run, relaunched.
7. Ran to completion on GPU3: vanilla 12k (144s train) then causal 12k (145s train), each with a spectral-reference L2 eval at 101 time snapshots.
8. Results: vanilla rel-L2 0.692 (train loss ~1e-2 → "low loss but wrong solution" REPRODUCED); causal rel-L2 0.861 (did NOT beat vanilla at this compute). Per-t: both accurate early, ~100% error by t=1.
9. Verified causal weights active in log (wmin 3.9e-2 → 0): Eq. 11 behavior REPRODUCED.
10. LLM-judge via free Argo gpt-5.2 (`llm_judge_prompt.py`): verdict PARTIAL — mechanism + failure-mode reproduced, improvement claim not (RBAR + full-recipe training out of scope).
11. Wrote REPORT.md / brief.md / this log / artifact_harvest.md; pulled results.json + training.log + PDF + code to the target dir.

Honest note: the negative on the improvement claim is a *reduced-compute* result, not a contradiction. Origin causality PINN needs ~2-3e5 iters + hard BC + Fourier features; paper's gain also depends on RBAR (not implemented). Flagged as PARTIAL, not CONTRADICTED.
