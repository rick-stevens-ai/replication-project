# REPORT — Cosmic Reionization On Computers: Properties of the Post-Reionization IGM

**OSTI ID:** 1275503 · **Authors:** Gnedin, N. Y.; Becker, G. D.; Fan, X. · **Year:** 2017  
**Journal:** *The Astrophysical Journal*, 841, 13 (arXiv: 1605.03183)  
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/1275503-COSMIC-REIONIZATION-ON-COMPUTERS/`

---

## Paper claim (one paragraph)

Gnedin, Becker & Fan (2017) use the CROC (Cosmic Reionization On Computers) radiation-hydrodynamic simulations — full 3D AMR hydro with OTVET radiative transfer at 100 pc resolution in 40 h⁻¹ Mpc boxes — to predict five statistical probes of the post-reionization intergalactic medium at z = 5–6: (1) the cumulative distribution of effective Gunn–Peterson optical depth in 40 h⁻¹ Mpc skewers, (2) dark gap length distributions for varying τ_min thresholds, (3) sensitivity of gap statistics to τ_min, (4) transmission peak height/width distributions, and (5) a "DC mode" convergence test showing that denser regions have *lower* opacity because they reionize earlier. The paper finds good agreement with observations at z ≲ 5.5 but identifies a significant discrepancy at 5.5 < z < 5.7 (simulations too opaque) and a systematic deficit of wide transmission peaks, attributed to the absence of individual quasar proximity zones in the simulation.

---

## What we replicated

This is a **shallow replication** — we did *not* run the actual CROC radiation-hydrodynamic simulation (which requires ~10⁴ CPU-cores for months of wall-time on the ART AMR code with OTVET radiative transfer). Instead, we built a **semi-analytic surrogate** using the Fluctuating Gunn–Peterson Approximation (FGPA) with lognormal density fields, reproducing the same five statistical analyses:

| # | Analysis | Method |
|---|----------|--------|
| 1 | Flux PDF (CDF of τ_eff) in 5 redshift bins | 500 synthetic 40 h⁻¹ Mpc sightlines per z-bin, FGPA with lognormal densities + UV fluctuations, calibrated rescaling |
| 2 | Dark gap distributions (4 z-bins × 3 τ_min) | Contiguous regions with F < e^{-τ_min}; L_g dP/dL_g computed |
| 3 | Gap sensitivity to τ_min | Same analysis at z = 5.7–5.9 with τ_min = 2.5, 3.0, 3.5 |
| 4 | Transmission peak statistics | Peaks at half-maximum, SNR ≥ 3; height + width distributions |
| 5 | Reionization history + DC mode test | Sigmoid reionization model; 30 independent 20 h⁻¹ Mpc realisations at z = 5.7 |

Key methodological differences from the original:

| Aspect | GBF17 (CROC) | This work |
|--------|-------------|-----------|
| Density field | 3D AMR hydro (ART code) | 1D lognormal random field |
| Radiative transfer | OTVET (3D, self-consistent) | Analytic UVB + lognormal fluctuations |
| Temperature | Non-equilibrium chemistry | Power-law T–Δ relation |
| Resolution | 100 pc physical, 1024³ | 4096 pixels per 40 h⁻¹ Mpc |
| Calibration | ε_UV = 0.15 (physics-based) | τ_eff rescaling to match observations |
| Runtime | ~months on ~10⁴ cores | ~3 minutes on single core (Apple Silicon) |

---

## Key results (paper vs ours table)

| Quantity | Paper (GBF17) | Ours | Match? |
|----------|--------------|------|--------|
| **⟨τ_eff⟩ at z = 5.2** | ~2.0 (obs target) | 2.69 ± 0.01 | ⚠️ High by ~35% |
| **⟨τ_eff⟩ at z = 5.4** | ~2.5 (obs target) | 3.68 ± 0.05 | ⚠️ High by ~30% |
| **⟨τ_eff⟩ at z = 5.6** | ~3.2 (obs target) | 5.12 ± 0.16 | ⚠️ High by ~50% |
| **⟨τ_eff⟩ at z = 5.8** | ~4.0 (obs target) | 7.49 ± 1.80 | ❌ High by ~60% |
| **⟨τ_eff⟩ at z = 6.0** | ~5.5 (obs target) | 20.6 ± 12.6 | ❌ Much too opaque |
| **Flux PDF shape** | Steep CDF, broad at high z | Qualitatively similar | ✅ Shape reproduced |
| **5.5 < z < 5.7 tension** | Sims more opaque than data | Model even more opaque | ✅ Same tension, amplified |
| **Gap dist. shape** | Peaked at ~5–15 Mpc | Consistent morphology | ✅ Qualitative match |
| **Gap τ_min sensitivity** | Shape preserved, tail shifts | Reproduced | ✅ Good match |
| **Peak heights ⟨h_p⟩** | Faithfully matched to obs | 0.047 (z ~ 5.5) | ✅ Order correct |
| **Peak widths ⟨w_p⟩** | Lack of wide peaks (deficit) | 590 km/s; narrow only | ✅ Same deficiency |
| **Peaks at z > 5.75** | Very few | 0 detected | ✅ Consistent |
| **T₀(z = 5.0)** | ~10⁴–1.5×10⁴ K | 12,488 K | ✅ In range |
| **T₀(z = 6.0)** | Near-isothermal | 15,000 K, γ = 1.14 | ✅ Consistent |
| **DC mode correlation** | Negative r(δ, τ_eff) | r = −0.061 | ✅ Reproduced (weak) |
| **Reionization midpoint** | z ~ 6–7 | z ~ 7.0 (volume-weighted) | ✅ Consistent |
| **Gap counts (z = 5.5–5.7, τ_min = 2.5)** | 77 (obs) | 769 | ⚠️ ~10× more (box-size sampling) |
| **Gap counts (z = 5.7–5.9, τ_min = 2.5)** | 46 (obs) | 500 (1 per sightline) | ⚠️ All opaque |

---

## Honest gaps

**This replication is fundamentally shallow.** We must be explicit about what was *not* replicated:

1. **No radiation-hydrodynamics.** The entire scientific contribution of CROC is the self-consistent coupling of 3D AMR hydrodynamics (ART code, 100 pc resolution) with on-the-fly radiative transfer (OTVET). Our 1D lognormal FGPA model is a textbook approximation that predates CROC by decades. We validated the *statistical analysis pipeline* (how to compute flux PDFs, gap distributions, peak statistics), not the simulation itself.

2. **Quantitative opacity mismatch.** Our ⟨τ_eff⟩ values are systematically 30–300% too high, especially at z > 5.5. The lognormal model cannot capture the void structure, shock-heated filaments, or patchy ionization topology that CROC resolves. This is not a calibration failure — it reflects a fundamental limitation of the surrogate model.

3. **No 3D density–velocity–temperature correlations.** Real IGM sightlines traverse a 3D field with correlated structures. Our 1D lognormal model with a power-law T–Δ relation misses these correlations entirely.

4. **No individual quasar proximity zones.** GBF17 identify this as the cause of the missing wide transmission peaks. Our model inherits this limitation because quasars appear only as a global UV background.

5. **Approximate transfer function.** We used the BBKS fitting formula rather than a Boltzmann code (CAMB/CLASS), introducing percent-level power spectrum errors.

6. **No original simulation data accessed.** We did not obtain or compare against actual CROC outputs, simulation snapshots, or skewer catalogs. All "paper" values in the comparison table are read from the published figures and text.

7. **Rescaling factors (0.18–0.49) are large corrections.** These effectively absorb all the physics we're missing into a single fudge factor per redshift bin. The fact that they are far from unity confirms the surrogate is a poor stand-in for the actual simulation.

---

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **5/10** | All 5 statistical analyses from the paper are implemented and produce output (flux PDF, dark gaps, gap sensitivity, peak statistics, DC mode + reionization). However, the underlying physics — radiation-hydrodynamic simulation with AMR + OTVET — is entirely replaced by a semi-analytic surrogate. We replicated the *analysis methodology*, not the *simulation*. |
| **Agreement** | **4/10** | Qualitative trends are correct: monotonic τ_eff increase, gap distributions shift with τ_min, DC mode anti-correlation sign is reproduced, same wide-peak deficit. But quantitative values for ⟨τ_eff⟩ diverge by 30–300%, gap counts are off by 10×, and the high-z bins (z > 5.7) are essentially saturated. The agreement is at the level of "a textbook FGPA model can get the trends right" rather than "we verified CROC's specific predictions." |

---

## Deliverables

| Artefact | Path |
|----------|------|
| Replication code (Python, ~400 lines) | `replication/croc_replication.py` |
| Numerical results (JSON) | `replication/analysis_results.json` |
| Detailed LaTeX report (replication) | `replication/replication_report.tex` |
| Compiled replication report (PDF) | `replication/replication_report.pdf` |
| Stub LaTeX report (earlier pass) | `report/1275503_replication_report.tex` |
| Fig 1 — Flux PDF (5 z-bins) | `replication/figures/fig1_flux_pdf.png` |
| Fig 2 — Dark gap distributions | `replication/figures/fig2_dark_gaps.png` |
| Fig 3 — Gap sensitivity to τ_min | `replication/figures/fig3_gap_taumin.png` |
| Fig 5 — Peak statistics | `replication/figures/fig5_peak_stats.png` |
| Fig 6L — Reionization history | `replication/figures/fig6_reion.png` |
| Fig 6R — DC mode test | `replication/figures/fig6_dc_mode.png` |
| Extra — T–Δ relation | `replication/figures/extra_T_delta.png` |
| Extra — Sample spectra | `replication/figures/extra_spectra.png` |
| This report | `REPORT.md` |

**Friction points:** F5 (force-field / hyperparameter drift — the entire CROC simulation physics is replaced by an analytic approximation with tuned rescaling parameters).

**To re-run:** `cd ~/Dropbox/REPLICATE-PROJECT/1275503-COSMIC-REIONIZATION-ON-COMPUTERS/replication && python croc_replication.py` (requires Python 3.10+, NumPy, SciPy, Matplotlib; ~3 min on single core).
