# LUCID100 — Slot 37 (Wave 4, rank 14)
## RBE of ²²⁵Ac vs ¹⁷⁷Lu for [²²⁵Ac]Ac-PSMA / [¹⁷⁷Lu]Lu-PSMA therapy using TOPAS / TOPAS-nBio / MEDRAS (Rumiantcev et al. 2023)

- **DOI:** [10.1186/s40658-023-00567-2](https://doi.org/10.1186/s40658-023-00567-2)
- **Journal:** EJNMMI Physics 10:53 (2023). CC-BY 4.0, open access.
- **Authors:** Rumiantcev M¹*, Li WB², Lindner S¹, Liubchenko G¹, Resch S¹, Bartenstein P¹, Ziegler SI¹, Böning G¹, Delker A¹
  1. Dept. Nuclear Medicine, LMU University Hospital, Munich
  2. Federal Office for Radiation Protection (BfS), Medical/Occupational Radiation Protection
- **LUCID slot:** 37 / Wave 4 / rank 14 / `candidate_curated` → **PARTIAL FIRST PASS COMPLETE (analytical + MEDRAS smoke)**
- **Work folder:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-ac225-lu177-psma-topas-medras-rbe`

## What the paper does
End-to-end Monte Carlo pipeline to estimate the relative biological effectiveness of ²²⁵Ac vs ¹⁷⁷Lu for radiopharmaceutical therapy of metastatic castration-resistant prostate cancer (mCRPC):
1. **TOPAS / TOPAS-nBio** (Geant4 10.06-p03 + TOPAS-nBio v1.0) simulates radionuclide decay (`g4decay` + `g4radioactivedecay`), particle transport, and DNA damage in a 4.65 µm spherical nucleus embedded in ellipsoidal cells (5 cell-shape variants, 2 internalization scenarios — fully internalized vs membrane-bound — 2D and 3D cluster arrangements).
2. **DNA damage scoring:** `NucleusDNADamage` scorer writes SDDv1.0 files; chemistry via `TsEmDNAChemistry`.
3. **MEDRAS** (McMahon, [sjmcmahon/Medras-MC](https://github.com/sjmcmahon/Medras-MC), BSD-2-Clause) simulates stochastic DSB rejoining at fixed default parameters (σ/Rₙ=0.04187, λf=2.07 h⁻¹, λs=0.259 h⁻¹, 24 h cutoff).
4. **RBE** derived analytically from fitted `N_DSB(D)` curves: linear-quadratic for ¹⁷⁷Lu, linear for ²²⁵Ac (because of high-LET track structure).

Headline results (full repair, 3D, geom 1, full internalization):
- Initial-damage RBE ≈ **2.14** (dose-independent, ratio of slopes b₂₂₅Ac / b₁₇₇Lu).
- Post-repair RBE varies between **9.38** (low dose) and **1.46** (50 Gy nucleus dose).

## Why this matters for LUCID
- Directly couples three of the LUCID modeling pillars: **Geant4-DNA track structure → SDDv1.0 damage handoff → MEDRAS mechanistic repair → RBE**. Same chain used in slots 16, 19, 25.
- Provides a clinically grounded test case (real ¹⁷⁷Lu-PSMA SPECT-derived source-point densities, Resch et al.) for the simulation chain that other slots exercised with idealized irradiations.
- Confirms the **dose-dependent RBE** signal that mechanistic DSB-repair models predict for α emitters — a key claim that MEDRAS itself is built on.

## Relation to prior LUCID slots
| Slot | Folder | What it provides | Used here |
|------|--------|------------------|-----------|
| 16 | `lucid-medras-mc` | Working MEDRAS-MC install + SDD generator + repair fidelity pipeline | **Reused directly** for the alpha-vs-electron smoke run |
| 19 (Wave 2 backfill 47) | `lucid100-topas-proton-cellular-response` | TOPAS-nBio Zhu 2020 proton replication notes + 120 k thread-h cost flag | Same compute-cost regime — confirms why full reproduction needs HPC |
| 25 | `lucid100-topas-medras-cellbycell` | SPT-SDD library accelerator (Lim et al. 2026) | A possible *future* speed-up route for this paper's pipeline |
| (this) | `lucid100-ac225-lu177-psma-topas-medras-rbe` | First LUCID radiopharmaceutical-therapy α-vs-β RBE replication | — |

## What we have here
- `artifacts/paper.pdf`, `artifacts/paper.txt` — the published paper (3.7 MB, 22 pages).
- `artifacts/supplementary_MOESM1.docx` (+ `.txt`) — official supplement: full physics/chemistry module list, MEDRAS parameter values, compute environment, RBE uncertainty derivation.
- `artifacts/supplementary_landing.html` — Springer landing page snapshot (for provenance).
- `code/medras_smoke.py` — minimal MEDRAS-MC pipeline that generates SDD files for ¹⁷⁷Lu-like electrons (1 MeV) and ²²⁵Ac-like α-particles (~5–8 MeV, Z=2) and runs repair fidelity. Cross-checks the **direction** and **rough magnitude** of the RBE_initial signal reported in the paper.
- `code/rbe_analytical.py` — uses the published fit parameters from Tables 3 & 4 to reproduce the RBE(D₁₇₇Lu) and RBE(D₂₂₅Ac) curves analytically (Eqs. 6 & 7).
- `results/` — CSVs and figures from both smoke runs.
- `ARTIFACT_MANIFEST.md` — every file, where it came from, license, provenance.
- `FIRST_PASS_REPORT.md` — verdict and quantitative cross-check.
- `HPC_JOB_PLAN.md` — what it would cost to actually run the full 4000-simulation campaign.

## What we do *not* have / cannot have
- **No author code release.** Paper has no GitHub/Zenodo/Figshare repository for the TOPAS input decks or analysis scripts. Only the MEDRAS upstream is open (already replicated in slot 16). Listed under "TODO" as a softer no-go: code request would require author contact, which is excluded by task constraints.
- **No TOPAS input decks (.txt control files).** We can reconstruct them from the supplement's parameter list, but the exact geometry placement (Eq. 1 cell-cluster builder), source-point sampling for SPECT-derived densities, and lesion-by-lesion clinical inputs would need to be rebuilt from scratch.
- **No raw SDD output, no fitted parameter CSVs, no figure data.** Tables 3 & 4 in the paper give the LQ fit parameters per (cell geometry × internalization × 2D/3D) — these are the only numerical artifacts we can reproduce analytically.
- **Full HPC reproduction is infeasible on CherryRd.** Largest single simulation: 34 h init + 139 h execute + 46 GiB RAM. Total 4000 simulations × ~5–50 h each = ~tens of thousands of CPU-hours. See `HPC_JOB_PLAN.md`.

## Reproducibility verdict (one-liner)
**PARTIAL.** Method is fully described and the downstream repair model (MEDRAS) is replicable today on a laptop. The upstream Geant4-DNA TOPAS-nBio simulation is fully specified but compute-bound (requires HPC and 1-2 weeks wall time to redo all 4000 simulations). Published RBE results are reproducible *analytically* from the supplied fit parameters (Tables 3 & 4) without re-running TOPAS at all.

## License & ethics
- Paper: CC-BY 4.0.
- MEDRAS-MC: BSD-2-Clause.
- TOPAS / TOPAS-nBio: free for research, registration required (not redistributable).
- No author contact, no paid endpoints used. No PHI/PII handled.

## See also
- `PROGRESS.md` — chronological log.
- `FIRST_PASS_REPORT.md` — quantitative verdict.
- `HPC_JOB_PLAN.md` — what a real reproduction would take.
- `ARTIFACT_MANIFEST.md` — full file inventory.
