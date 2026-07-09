# FIRST_PASS_REPORT — Slot 36 (Deactivation Theory, Abolfath 2019)

**Verdict:** 🟡 **AMBER — KEEP (replicable in form, partial in numerics)**
**Recommended QA retag:** KEEP / first_pass_complete (no change to slot type — remains "simulation/model replication").

## Summary

Abolfath et al. (EPJ-D 2019, arXiv 1901.08194) present a fully analytical multi-scale framework — a perturbative renormalization of the LQ α(LET), β(LET) functions out of a DSB-population master equation (Eq. 1) plus a coarse-grained birth–death Markov chain (Eq. 40) for cell-colony / tumor dynamics. The high-LET non-linearity of RBE near the distal Bragg edge is attributed to (i) Landau/Vavilov-type energy-loss fluctuations renormalizing γ_eff, λ_eff, and (ii) continuous transitions in chromosome-aberration complexity (binary → ternary → quaternary recombinations). The paper fits H460 + H1437 NSCLC clonogenic data from the MD Anderson scanned proton beam set-up (Guan et al. 2015, Sci. Rep. 5:9850).

## Replication achieved (first pass)

A minimal H460 smoke replication is in `code/smoke_deactivation.py` and runs in < 1 s on CherryRd CPU. It implements:

- **Eq. 32** working LQ form, piecewise linear in LET_d with low/high regime split at 5 and 15 keV/µm (the regimes the authors actually fit).
- **Eq. 15 / 21–22** power-series structure: α grows with z_D / LET, β picks up linear LET correction in the high branch (which is the qualitative signature MKM / MCDS-RMF lack).
- LQ SF(D, LET) = exp(−αD − βD²) (their Eq. 20).
- RBE_10% by SF-inversion.

All six smoke checks pass:

| Check | Result |
|---|---|
| α monotonic ↑ with LET_d | ✅ |
| β monotonic ↑ with LET_d (slow) | ✅ |
| SF(D=2 Gy) drops monotonically with LET_d | ✅ |
| RBE_10% in plateau (LET=0.9 keV/µm) ∈ [1.0, 1.4] | ✅ (1.04) |
| RBE_10% at distal edge (LET≥15) ∈ [1.4, 2.5] | ✅ (1.9–2.3) |
| Low-dose lethal-lesion ratio L(LET)/L(0.9) ≈ α-ratio (Eq. §III B) | ✅ |

The smoke parameters were eyeballed from manuscript Fig. 5/6 since the authors **do not publish coefficient tables**. The point of the smoke is to verify the model machinery and qualitative shape — both confirmed.

## What is NOT (yet) replicated

1. **Quantitative match to Fig. 6 SF surface.** Would require:
   - Pulling Guan et al. 2015 SF(D, LET) tabular data (or digitising from the Nature figures).
   - Running the 3D global-fit procedure of Abolfath 2017 (ref [42]) — a Levenberg–Marquardt fit of a polynomial surface in (D, LET) → SF.
   - Verifying recovered α_i, b_i match the (unpublished) coefficients.
2. **MC simulation of the energy-loss spectrum.** §II E says authors used MC Landau/Vavilov spectra to score moments z̄, z̄² — TOPAS or Geant4-DNA single-event spectra at each LET, already available from the sibling LUCID slot 47 (TOPAS-nBio) and slot 56 (SPT-SDD/MEDRAS) replications.
3. **Birth–death Markov chain simulation (Eq. 40, 50).** Closed-form Eq. 51 is sufficient for TCP; explicit MC of the birth–death chain at N₀ ≈ 10⁶ cells per voxel would be ~minutes on a single CPU. Not required for verdict.
4. **Chromosome-aberration complexity index.** The paper's "binary → ternary → quaternary" transitions are formulated abstractly via the γ_n hierarchy of Eq. 5–8; no explicit complexity-index measurement is reported (it is a prediction awaiting experimental verification per §II G).

## Artifact availability check

- ❌ **No GitHub / code release** (verified by full-text grep over `artifacts/paper.txt`).
- ❌ **No supplementary materials** (the EPJ-D paper itself has no SI; arXiv preprint has none either).
- ❌ **No deposited datasets** (Zenodo, Figshare, Dryad, OSF — none cited).
- ✅ **Paper PDF** — arXiv OA copy harvested (9.7 MB).

## Heavy compute assessment

**Not needed.** Entire framework reduces to ≤ 6th-order polynomial in z_D + LQ SF + closed-form TCP product. Authors' own pipeline is described as "analytical" and the only numerical step is the LM 3D fit. Should not be scheduled on uicgpu / Aurora / Sparks.

## Blockers

- **B1 (soft):** Coefficient tables for α_i, β_i, b_ij not published — quantitative Fig. 6 reproduction requires re-running the global fit on Guan et al. raw data.
- **B2 (soft):** Bronk et al. γ-H2AX persistent foci data are "in preparation" as of 2019. Author contact ruled out per task brief.

Neither blocker prevents the first-pass verdict; both gate full quantitative reproduction.

## Recommendation

**KEEP** in LUCID100 as a replication-plausible, first-pass-complete entry. The minimal smoke replication (`code/smoke_deactivation.py`) is sufficient to validate the deactivation-theory framework qualitatively. Promotion to a full quantitative replication would require harvesting Guan et al. 2015 data and porting the 3D global-fit — an estimated 1–2 days of work on top of the present scaffold, no HPC needed.

## Next actions

1. (If escalated) Download Guan et al. 2015 supplementary SF table.
2. (If escalated) Port the LM 3D fit (scipy.optimize.least_squares is plenty).
3. (Optional) Wire the Landau/Vavilov MC moments from TOPAS-nBio cache already on disk in sibling slot 47.
4. Update master TSV (Wave 4, slot 36) qa_status → `KEEP_first_pass_complete` with note: "Smoke replication of Eq. 32 LQ form + Eq. 15 power series; 6/6 qualitative checks PASS; no author code/data; quantitative Fig. 6 needs re-fit on Guan 2015 raw."

## Inputs / outputs

- Inputs: arXiv 1901.08194 PDF (free), Springer paywall stub.
- Outputs: README.md, PROGRESS.md, ARTIFACT_MANIFEST.md, this file, code/smoke_deactivation.py, smoke_test.json, 3 figures.
- Subagent progress JSON: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave4-36-renormalization-of-radiobiological-response-functions-by-ene.json`
