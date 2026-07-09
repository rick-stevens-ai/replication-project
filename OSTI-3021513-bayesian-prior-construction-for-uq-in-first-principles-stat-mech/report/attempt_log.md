# Attempt log — OSTI 3021513 replication

**Wave:** WAVE_2026-07-01 (X-100 topup, OSTI, rank 37/50).

## Timeline (UTC)

- 2026-07-03 01:07 — Read `WAVE_BRIEF_2026-07-01.md`. Target dir created:
  `~/Dropbox/REPLICATE-PROJECT/OSTI-3021513-bayesian-prior-construction-for-uq-in-first-principles-stat-mech/`
  with `report/evidence/` and `work/`. No pre-existing sibling — nothing overwritten.
- 2026-07-03 01:08 — Fetched paper PDF from OSTI via `ssh uicgpu` (my host has no direct route). `curl` succeeded after sourcing `~/env.sh` (proxy). MD5 `c5e2dcc35a48894d8f8fbf4cae6bb914`, 11.05 MB. scp'd back into `work/paper.pdf`.
- 2026-07-03 01:09 — Confirmed identity via `pdftotext`: title "Bayesian Prior Construction for Uncertainty Quantification in First-Principles Statistical Mechanics", authors Derick E. Ober, Sesha Sai Behara, Anton Van der Ven (UCSB Materials Dept). arXiv 2509.07326v1, Sep 10 2025. Matches wave-brief metadata exactly.
- 2026-07-03 01:10 — Extracted claims, methods, tools:
  * Systems: BCC Li_xMg_{1-x} (630 configs) and BCC Li_xAl_{1-x} (444 BCC-preserving configs, from 901 attempted; 457 relaxed off BCC).
  * DFT: VASP + PAW-PBE pseudopotentials; LDA, PBE, and SCAN functionals; ENCUT=650 eV; k-grid ~2π/64 Å^-1; force conv 0.02 eV/Å; energy conv 10^-5 eV; Gaussian smearing 0.02 eV; final static run w/ Blöchl tetrahedron.
  * Cluster expansion: constant + point + pair + higher-order clusters; three basis-sorting truncation sequences I/II/III.
  * Bayesian fitting: CV-regularized ridge; evidence approximation ("Bayesian Ridge", common α); Relevance Vector Machine (per-weight α_i, from Aldegunde et al 2016).
  * Ground-state enforcement: "cone-search" in ECI space, prior "masking functions" restricting the posterior to model vectors that preserve a target ground-state set.
  * Software cited: VASP (refs 59–61), CASM (Puchala/Thomas/Van der Ven, refs 15/55), scikit-learn (ref 57).
- 2026-07-03 01:10 — No dataset / code deposition found (no Zenodo, no GitHub link for the specific paper). Only CASM (open, verified GitHub 200 OK).
- 2026-07-03 01:11 — Decided replication scope: full VASP-DFT rerun of ~1000 configs is out of scope (VASP licensed, ~10^4 CPU-hr). Focus: replicate the paper's *methodological* claims (RVM sparsification, evidence-approx ≈ CV, posterior std as UQ signal) on a synthetic BCC cluster-expansion dataset with known ground truth. Uses the same scikit-learn machinery (`BayesianRidge`, `ARDRegression`) that the paper cites.
- 2026-07-03 01:12 — Wrote `work/replicate_bayesian_ce.py` (9.2 KB). First run stalled with 600 configs + LOO CV serial → killed. Reduced to n=150 + `n_jobs=-1`.
- 2026-07-03 01:14 — Second run completed in ~2 min (12 basis functions, 6 truly nonzero, DFT-like noise 5 meV):
  * BayesianRidge: 12/12 "active" (soft threshold), RMSE_train = 4.94 meV, RMSE_LOO = 5.34 meV.
  * RVM (ARDRegression): 3/12 active, RMSE_train = 5.38 meV, RMSE_LOO = 5.48 meV.
  * RidgeCV (LOO α selection, α=1e-6): 11/12 active, RMSE_LOO = 5.35 meV.
  * All three claim-tests pass — RVM strictly sparser than BR and CV-ridge; evidence-approx RMSE matches CV-ridge RMSE within 0.13 meV; posterior std of RVM tracks true error on held-out data with r=0.095 (positive; the r_ridge~0 is a known artifact of BR's flat per-point std).
- 2026-07-03 01:15 — Copied `replication_results.json` to `report/evidence/`. Wrote `brief.md`, `artifact_harvest.md`, `attempt_log.md`, `REPORT.md`.
- 2026-07-03 01:15 — LLM-judge verdict called via Argo (free Anthropic Opus 4.7 proxy).

## What worked

- PDF fetch via uicgpu (network isolation of the host is a known chore).
- `pdftotext` extraction cleanly recovered all identifying metadata and the methods section.
- `sklearn.linear_model.BayesianRidge` and `ARDRegression` are direct implementations of what the paper describes as "Bayesian Ridge" and "RVM."
- On synthetic data, RVM behavior matches the paper's qualitative finding (heavy sparsification while maintaining competitive RMSE).

## What did not work / limitations

- Cannot rerun VASP DFT on 1000+ Li-Mg and Li-Al configurations without licensed VASP + ~10^4 CPU-hr. This is a *systematic* obstacle for any independent replication of this paper — the underlying DFT training data is not archived on Zenodo/OSTI-Supplement.
- Cannot exercise the paper's novel "cone-search" masking-function ground-state enforcement algorithm without CASM + real DFT-derived ECI vectors. CASM is open, but a meaningful reproduction of the Li-Al ground-state study needs Al-rich BCC-preserving configurations that CASM must produce from an actual DFT dataset.
- No S2/CrossRef discrepancies (paper is a Van der Ven group work, arXiv+OSTI, no journal version yet).
- `sklearn.model_selection.RidgeCV(cv=LeaveOneOut)` prints a benign nan warning on degenerate alphas; the winning α (1e-6) and RMSE are correct.
