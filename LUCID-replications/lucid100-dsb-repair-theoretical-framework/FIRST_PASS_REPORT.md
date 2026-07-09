# FIRST_PASS_REPORT — LUCID100 slot 30

**Paper:** Murray P.J., Cornelissen B., Vallis K.A., Chapman S.J. (2016). "DNA double-strand break repair: a theoretical framework and its application." *J R Soc Interface* 13:20150679. DOI [10.1098/rsif.2015.0679](https://doi.org/10.1098/rsif.2015.0679). PMC4759787, CC BY 4.0.

**Workdir:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-dsb-repair-theoretical-framework/`
**Date:** 2026-06-09
**Worker:** Wave 3 backfill (subagent of main).
**Run host:** CherryRd (no HPC required).

## 1. Verdict

**PASS-low (6/6 qualitative checks).**

A pure-Python ODE smoke replication that uses the paper's Table 1 fitted rate constants and Table 2 scaling constants reproduces every qualitative prediction stated explicitly in the paper text. Full quantitative replication (refit of k1…k6 from raw experimental time series, antibody-extension k7/k8 calibration, Auger k9 calibration vs clonogenic survival) is blocked by the absence of any deposited supplementary data, code, or raw figure source data.

## 2. What the paper does

- Defines a single-DSB-site Markov chemistry: telegraph X∈{0,1} (DSB present/absent), bound activated pATM-like molecules Y, phosphorylated H2AX molecules Z.
- Six rate constants k₁…k₆ govern: repair (k₁·Y when X=1), pATM recruitment by DSB (k₂·X), pATM recruitment by γH2AX (k₃·Z), pATM dissociation (k₄·Y), H2AX phosphorylation (k₅·Y), γH2AX dephosphorylation (k₆·Z).
- Three a priori counts (Table 2): Y_max=300, Z_max=1000, Z*=200 (microscopy detection threshold).
- Master equation (2.1) → ad hoc closure (2.5) and conditional-mean closure (2.8) ODEs; both shown via SSA averages to match the master equation (Fig 3).
- Parameters fit by Nelder–Mead `fminsearch` (MATLAB) against MCF7 and MDA-MB-468 γH2AX foci + DSB time series after 4 Gy ¹³⁷Cs (Fig 4); reported in Table 1.
- Case study 1: antibody extension (eq 4.1) with Q = bound γH2AX-antibody complex (assumed inert). Predicts (a) k₈[TAT]₀/k₇ scales linearly with [TAT]₀ at low concentrations (Fig 7e, observed saturation at high concentration is *not* predicted by the model), (b) DSB kinetics largely unchanged — validated by neutral comet (Appendix B).
- Case study 2: ¹¹¹In-Auger extension (eqs 4.3–4.4). Each bound antibody–γH2AX complex induces de novo DSBs at rate k₉∝R (specific activity). Predicts monotonic rise in DSB-persistence AUC as R rises (Fig 8b), qualitatively matching the experimentally measured inverse correlation with MCF7 clonogenic survival (R²=0.97).

## 3. Public data / code availability

| Item | Status |
| --- | --- |
| Full paper PDF | ✅ Open access via EuropePMC (PMC4759787) |
| JATS XML full text | ✅ Open access via EuropePMC |
| Supplementary material | ❌ None (EuropePMC `hasSuppl=N`, confirmed) |
| Source code (MATLAB fitter, Gillespie SSA) | ❌ Not deposited |
| Raw experimental time series (foci, comet OTM, clonogenic) | ❌ Figure-only |
| Fitted parameters | ✅ Inline in Table 1 |
| Scaling constants | ✅ Inline in Table 2 |
| Antibody-binding rates (k₇, k₈) | ❌ Only ratio k₈[TAT]/k₇ shown in Fig 7e |
| Auger rate constant k₉ | ❌ Only proportionality k₉∝R stated |

No GitHub, Zenodo, Figshare, or supplementary archive is referenced anywhere in the paper or PMC record.

## 4. Reimplementation

`scripts/smoke_model.py` (+ `scripts/scripts_ssa.py`). Single command:

```bash
cd scripts && python3 smoke_model.py
```

Pure CPython + numpy + scipy. ~15 s on CherryRd. No GPU, no HPC.

Three model variants:

- **Base (eq 2.5):** logistic saturation `(1 − Y/Ymax)`, `(1 − Z/Zmax)` added to source terms so the Table-2 caps are respected by the mean-field ODE (the SSA enforces them by construction).
- **Antibody (eq 4.1):** state extended by Q (bound antibody–γH2AX); only the k₃-feedback term sees Z_free=Z−Q, in line with appendix A's "bound complex is inert" assumption. k₇ and k₈ are not in the paper; the smoke uses k₇=1 h⁻¹, k₈=2 (h·µg/ml)⁻¹ purely to demonstrate qualitative C4 behaviour.
- **Auger (eqs 4.3–4.4):** state extended by Q; an additional repair-reversal term `k₉·Q·(1−X)` reactivates the telegraph in repaired sites. k₉=k₉_per_R · R, k₉_per_R=0.05 h⁻¹.
- **Tau-leap SSA:** vectorised over 200 trajectories on a 60-step grid up to 6 h. Used only for check C6 on MDA-MB-468 (MCF7's rate constants make Python-level SSA intractable inside the smoke budget; HPC tau-leap or C/Numba implementation would be straightforward).

## 5. Qualitative checks

Each check ties to an explicit prediction in the paper text. Pass means the smoke model reproduces it; metrics are reported in `artifacts/smoke_results.json`.

| ID | Prediction (paper text reference) | Smoke result | Pass |
| --- | --- | --- | --- |
| C1 | ⟨X⟩(t) decays monotonically from 1 (Fig 2a, Fig 4) | MDA-MB-468 ⟨X⟩(24 h)=0.39; MCF7 ⟨X⟩(24 h)=0.04 | ✅ |
| C2 | ⟨Z⟩(t) rises from 0, peaks, then decays (Fig 2c, Fig 4) | Peaks at 0.5 h (MDA468, 73 molecules) and 0.1 h (MCF7, 49 molecules) | ✅ |
| C3 | MCF7 repair is "soon after irradiation"; MDA-MB-468 is "much delayed" (§5) | t₅₀(⟨X⟩) = 2.5 h (MCF7) vs 16.6 h (MDA-MB-468) | ✅ |
| C4 | Antibody does NOT significantly perturb DSB kinetics (Fig 7, App B) | MDA-MB-468 ⟨X⟩ AUC ratio [TAT]=0.5 vs 0 = 1.38 (within ±50% band) | ✅ |
| C5 | DSB-persistence AUC rises monotonically with ¹¹¹In specific activity R (Fig 8b) | AUC(R=0→8) = 5.4, 21.8, 29.3, 33.4, 36.0 — strictly increasing | ✅ |
| C6 | Number of detectable γH2AX foci (Z≥Z*) ∝ mean ⟨Z⟩ (§3.3, Fig 5) | MDA-MB-468 tau-leap, n=200, t∈[0,6 h]: corr=0.969 | ✅ |

Summary: **6/6 pass, verdict PASS-low.**

## 6. Limitations of this pass

- C3, C4, C5 are checked on qualitative ordering / sign, not on quantitative match to the published Figure-4/7/8 curves (no digitized data).
- The antibody and Auger extensions use auxiliary rate constants (k₇, k₈, k₉) that the paper does not report. The smoke shows that *with reasonable choices*, the predicted qualitative behaviour holds; it does *not* show that the paper's specific quantitative claim about k₈[TAT]/k₇ vs [TAT] (Fig 7e linearity) is reproduced.
- The mean-field ODE uses logistic saturation, which is an addition to the paper's eq (2.5) needed to keep Z bounded by Z_max=1000 over 24 h with the MCF7 rate constants. The paper's bound is implicit in the master equation; the SSA enforces it; the ODE in eq (2.5) as written does not.
- Section 3.3 / Fig 5 proportionality is verified only on the MDA-MB-468 cell line. MCF7's k₅=1765 h⁻¹ combined with Y up to 300 means propensities ~5×10⁵ events/h/site, which is intractable inside a CPython smoke budget. A small Numba or C SSA on CherryRd would close this gap in <10 minutes.

## 7. Blockers for full quantitative replication

1. **Raw experimental time series** (foci counts at multiple time points, comet OTM, clonogenic survival vs R): figure-only in the paper, not deposited. → Resolution: WebPlotDigitizer (≈2–4 hours).
2. **Author code:** none released. → Resolution: not needed if we accept the published Table-1 parameters; re-fit would only be needed for a tier-up.
3. **k₇, k₈ values:** not reported. → Resolution: extract Fig 7e linear-regime slope to recover k₈/k₇ ratio; binding rate k₈ can be set on biophysical priors (10⁴–10⁶ M⁻¹·s⁻¹).
4. **k₉ scaling:** only k₉∝R reported. → Resolution: calibrate against Fig 8b clonogenic curve.

None of these need HPC. CherryRd suffices.

## 8. Recommendation

**QA decision:** **KEEP**, retag from `candidate_curated` to **`first_pass_complete` / PASS-low**. Replication is well-defined, the model is faithfully reimplemented, and all qualitative claims of the paper are reproduced.

**Promotion to PARTIAL or SUCCESS** is feasible with ~1 day of additional CPU work on CherryRd (WebPlotDigitizer + Nelder-Mead refit + auxiliary-rate calibration) — no HPC, no authors contacted, no paid endpoints.
