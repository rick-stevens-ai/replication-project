# CLAIMS.md — Rasp 2018 testable-claims enumeration (re-pass)

Source: `~/.openclaw/workspace/tmp-pdf/rasp2018.txt` (pdftotext of `rasp_2018_arxiv.pdf`, arXiv 1806.04731v3).

**FEASIBLE_OFFLINE legend:**
- **YES** = testable with the Zenodo sample data (`preproc_features.nc` + `preproc_targets.nc` + `sample_SPCAM_1.nc`) and the trained 9×256 PASS-1 net, no prognostic SPCAM-CAM coupling needed.
- **DIAG** = testable in *diagnostic mode* (apply NN to SPCAM state, compare NN-predicted field vs SPCAM-truth field) — surrogate for prognostic claim, no GCM run.
- **NO**  = requires the modified SPCAM Fortran source + a CAM build environment + multi-year prognostic run.
- **NO-DATA** = even diagnostic mode is impossible because the required SPCAM dataset (e.g. +4K SST, zonal SST perturbation) is not in the Zenodo deposit.

| # | Short name | Source | What's needed | FEASIBLE_OFFLINE | PASS-1 status | RE-PASS plan |
|---|---|---|---|---|---|---|
| C1 | 9-layer × 256-node FC architecture | "nine layer deep, fully-connected network with 256 nodes in each layer" (Methods §"Model and neural network setup") | Build the network, count params | YES | ✅ covered | re-verify param count vs paper's stated 567,361 |
| C2 | ~500K trainable parameters | "the network has around half a million parameters" / "567,361 learnable parameters" (Suppl. Methods) | Param count | YES | ✅ covered | re-verify exact match |
| C3 | LeakyReLU(0.3) lowest training loss | "LeakyReLU activation function max(0.3x, x) resulted in the lowest training losses" (Suppl. Methods) | Train identical net w/ ReLU and tanh, compare losses | YES | ❌ NOT TESTED in pass 1 | **NEW TEST** — train 9×256 with ReLU + tanh, compare val-loss |
| C4 | Adam optimizer, batch 1024, lr=1e-3 with 5× decay every 3 epochs | "Adam … learning rate of 1×10⁻³ which was divided by five every three epochs … batch size of 1024" (Suppl. Methods) | Reproduce training schedule | YES | ⚠ partial — pass 1 used constant lr 1e-3 | **NEW TEST** — re-train control with paper-exact schedule, compare to flat-lr baseline |
| C5 | 18 training epochs sufficient | "trained for 18 epochs" (Suppl. Methods) | 18-epoch training run | YES | ✅ covered (we did 20) | re-verify val-loss already plateaus by epoch 18 |
| C6 | Deep > shallow on training loss | "deeper, larger networks achieve lower training losses" (Methods) | Architecture sweep | YES | ✅ covered (5 archs) | re-verify with depth-vs-mean-loss summary |
| C7 | 2-4 layer networks unstable / 4-layer minimum | "encountered unstable modes and unrealistic artifacts for networks with two or one hidden layers … A four layer network was the minimal complexity to provide good results" (Suppl. Methods) | Train 1, 2, 3, 4-layer nets, look at val-loss + R² | YES | ⚠ partial — pass 1 had 2-layer, 4-layer but no 1 or 3 | **NEW TEST** — train depth-1, depth-3 nets, fill in the depth-vs-skill curve |
| C8 | Mean offline R²(ΔT) high (Gentine 2018 GRL companion: ~0.7) | implied via citation (23) | Train on full 140M samples (paper) — or on 778K sample, accept the 3× gap | YES (with caveat) | ✅ covered — got 0.247 mean, 0.654 max | re-verify; document magnitude gap |
| C9 | Mid-tropospheric R² peak, near-surface R² collapse, TOA degeneracy | implicit in paper's "low training skill in the boundary-layer (23) suggests …" (Variability §) | Per-vertical-level R² profile | YES | ✅ covered | re-verify and add latitude-binned version |
| C10 | NN-predicted heating field reproduces mean climatology of SPCAM | Fig. 1A: "mean sub-grid heating … in close agreement with a single latent heating tower at the ITCZ and secondary free-tropospheric heating maxima at the mid-latitude storm tracks" | NN-predict tendencies on SPCAM state, average to climatology, compare to SPCAM-truth climatology | DIAG | ⚠ pass 1 marked OUT-OF-SCOPE | **NEW TEST** — build offline diagnostic ΔT(lat,p) climatology from NN vs from SPCAM truth |
| C11 | NN-predicted moistening field reproduces SPCAM climatology | Fig. S2: "Mean convective sub-grid moistening rates" | Same as C10 for ΔQ | DIAG | ⚠ OUT-OF-SCOPE in pass 1 | **NEW TEST** — same |
| C12 | ITCZ peak co-located with max SST at 5°N | "ITCZ peak, which is co-located with the maximum SSTs at 5°N" (Mean climate §) | Latitude-binned mean ΔT field | DIAG | ⚠ OUT-OF-SCOPE in pass 1 | **NEW TEST** — verify latitude of mean-heating max in both SPCAM truth + NN prediction |
| C13 | ITCZ "slightly sharper" in NNCAM than SPCAM | "ITCZ peak … is slightly sharper in NNCAM compared to SPCAM" (Mean climate §) | Compare FWHM of ITCZ peak in NN vs SPCAM | DIAG | ⚠ OUT-OF-SCOPE | **NEW TEST** — measure FWHM of meridional heating peak (NN vs SPCAM) |
| C14 | NN heating/moistening variance < SPCAM variance | Fig. 2B + S3A: "NNCAM shows reduced variance compared to SPCAM and even CTRLCAM, mostly located at the shallow cloud level around 900 hPa and in the boundary-layer" | std(NN-pred)/std(SPCAM-truth) by latitude+level | DIAG | ⚠ OUT-OF-SCOPE | **NEW TEST** — per-(lat,lev) std ratio, look for shallow-cloud underprediction |
| C15 | NN predictions are smoother (lose vertical/horizontal variability) | "neural network's predictions are much smoother, i.e. they lack the vertical and horizontal variability of SPCAM" (Variability §) | Spatial autocorrelation length, vertical-gradient std of NN vs SPCAM | DIAG | ⚠ OUT-OF-SCOPE | **NEW TEST** — vertical-difference RMS as smoothing proxy |
| C16 | Network approximately conserves column moist static energy | "NNCAM conserves column moist static energy to a remarkable degree (Fig. 4A)" | Per-prediction: Cp/g∫ΔT_phy dp − H − F_rad   vs   Lv/g∫ΔQ_phy dp − E. Plot scatter, compare slope to 1, compute RMS of imbalance. **Note**: Zenodo preproc set is 60-out (no F_rad, no H, no E in targets). Use SPCAM sample diagnostic file (PHQ, TPHYSTND, FLNT, FLNS, FSNT, FSNS, SHFLX, LHFLX) for this. | DIAG | ⚠ OUT-OF-SCOPE | **NEW TEST** — column-energy balance NN-pred vs SPCAM truth using sample_SPCAM_1.nc fields. Output: scatter slope, R², residual RMS. |
| C17 | Globally integrated total energy stable for 5-year run | Fig. 4B: solid lines, "stable without noticeable drift" | Requires prognostic NNCAM | NO | ⚪ explicit OUT-OF-SCOPE | not testable offline; document blocker |
| C18 | Globally integrated moisture stable for 5-year run | Fig. 4B: dashed lines | Requires prognostic NNCAM | NO | ⚪ OUT-OF-SCOPE | not testable offline; document blocker |
| C19 | NNCAM precipitation distribution matches SPCAM tail | Fig. 2A: "precipitation distribution in NNCAM closely matches that of SPCAM, including the tail" | Precip histogram from prognostic run. **Offline surrogate:** compare distribution of column-integrated NN-predicted ΔQ (proxy for precip) vs SPCAM PRECT distribution. | DIAG | ⚪ OUT-OF-SCOPE | **NEW TEST** — diagnostic precip-proxy histogram NN vs SPCAM truth |
| C20 | Prognostic NNCAM stable for multi-year sims | Abstract + Discussion: "prognostic multi-year simulations are stable" | Requires modified SPCAM Fortran + 5-year CAM run | NO | ⚪ OUT-OF-SCOPE | not testable offline; document blocker |
| C21 | NNCAM ~10× faster total than SPCAM | "factor 10 compared to SPCAM" (Suppl. Methods) | Run a fair NN-inference benchmark and compare to SPCAM published per-timestep cost | YES (rough) | ❌ NOT TESTED | **NEW TEST** — measure NN forward-pass cost per grid column (×60 inputs) on uicgpu A100 and on CherryRd CPU; document the bound. NOT a full 1:1 with the paper's "physics" measurement but verifies inference cost is small relative to a 30-min GCM step. |
| C22 | NN reproduces equatorial wave spectrum / MJO | Fig. 3 + Discussion | Requires 5-year prognostic NNCAM | NO | ⚪ OUT-OF-SCOPE | document blocker |
| C23 | NN runs stably under wavenumber-1 SST perturbation | Fig. 5A + Generalization § | Requires perturbed-SST CAM run | NO | ⚪ OUT-OF-SCOPE | document blocker |
| C24 | NN fails to extrapolate to +4K SST climate | Fig. 5B + Generalization § | Requires +4K SPCAM dataset and prognostic NNCAM at +4K | NO-DATA | ⚪ OUT-OF-SCOPE | document blocker — +4K SST data not on Zenodo |
| C25 | NN can interpolate between trained climates (NNCAM-ref+4K experiment) | Generalization § + Fig. 5B | Requires +4K SPCAM data + two-climate-trained NN + prognostic run | NO-DATA | ⚪ OUT-OF-SCOPE | document blocker |

## Re-pass coverage targets

PASS-1 covered claims: **C1, C2, C6, C8, C9** (5 claims fully covered out of 25; ≈ 20%; but pass 1 wisely weighted the score by claim *importance*, hence 6/10 not 2/10).

RE-PASS will add coverage for **C3, C4, C5, C7, C10, C11, C12, C13, C14, C15, C16, C19, C21** — that's 13 additional claims. Of those, C16 (energy conservation) and C10-C13 (mean-climate reproduction) are among the paper's *named central results*, so they should lift the coverage score meaningfully.

Claims that remain genuinely out of scope (require Fortran/SPCAM/CAM build or unavailable data):
**C17, C18, C20, C22, C23, C24, C25** — 7 claims. These are the prognostic, multi-year, and out-of-distribution-climate experiments. We will name the exact missing artifact for each.

### Honest expected ceiling

If we land C10-C16 + C19 + C21 as offline-diagnostic surrogates and re-confirm C1-C9, the coverage score should rise from 6/10 to ≈8/10. Agreement score depends on whether the NN's diagnostic-mode field really matches SPCAM-truth at the climatology level — there's a real risk that the data-limited net (trained on 778K samples vs paper's 140M) just doesn't get the ITCZ peak crisp enough. We will report honestly.
