# Attempt Log (chronological)

1. Read WAVE_BRIEF_2026-07-01.md + OSTI100_TOPUP50 TSV; listed existing OSTI-* dirs to avoid collisions.
2. Excluded already-done (2997724, 2480245, 3007459, 3028840, 1974586, 2564727, 2574844, 3365789) + existing 3001323 dir.
3. Fetched candidate PDFs #3,#4,#6,#7 via `ssh uicgpu` OSTI purl proxy (CherryRd times out on OSTI). Ran `pdftotext -l 6` triage.
4. **Picked rank #6 OSTI 3024991** (Vlasov-Poisson ROM): reproducible computational core, clean **analytic validation target** (Landau damping rate + POD reducibility), light compute, no proprietary data, no heavy table OCR.
5. Extracted full FOM discretization (Sec 2) + exact problem params: prescribed-E (α=0.1, vT=1, tf=130, 128²) and Landau (k=1, α∈[0.01,0.03], vT∈[0.8,1], tf=15).
6. Created target dir `OSTI-3024991-vlasov-poisson-rom/` (verified non-colliding).
7. Wrote `vlasov_fom.py` (WENO5 Jiang-Shu + Rusanov flux splitting, FFT Poisson, RK4) + `run_replication.py`.
8. Copied to uicgpu, ran under `~/env.sh`. numpy 1.23.5 / scipy 1.10.1.
9. **Results v1:** prescribed-E POD matched paper well (n_f=23 vs 24; err 0.13% vs 0.2%). BUT Landau field-energy did NOT damp (measured γ positive) — bug.
10. **Diagnosis:** prescribed-E (external field) worked → x/v advection correct. Self-consistent Landau failed → suspected E-field sign in Poisson↔Vlasov coupling.
11. Verified analytic dispersion solver independently: k=0.5 → γ=-0.15336 (exact textbook value), k=1 → γ=-0.851. Solver is correct.
12. Ran `landau_signsweep.py` (k=0.5, canonical benchmark, both E signs, nx=128 nv=256).
    - sign=+1: γ_fit=+0.136 (wrong, growing).
    - **sign=-1: γ_fit=-0.1495 vs analytic -0.15336 → 2.5% error.** ✓ Correct convention identified.
13. Set FOM default `efield_sign=-1` (documented: matches paper eq1/eq2 sign convention + reproduces canonical Landau rate).
14. Generated figures (`make_plots.py`); pulled all artifacts to `report/evidence/`.
15. LLM-judge (Argo gpt-5.2, free, temp=0): **PARTIAL**, coverage 67%, agreement 85%.

## What worked
- FOM reimplementation from equations alone.
- Prescribed-E POD reducibility reproduced near-exactly.
- Canonical Landau rate reproduced to 2.5% after sign fix.

## What was out of scope / not done
- Tensorial ROM (3rd-order tensor nonlinear update), time-/energy-windowed ROMs (TW/EW-ROM), two-stream instability, the 90× speedup claim — these are ROM-engineering claims, not core physics; excluded per <25min efficiency target.
- Did not run the authors' HyPar binaries (independent reimplementation is a stronger test).
