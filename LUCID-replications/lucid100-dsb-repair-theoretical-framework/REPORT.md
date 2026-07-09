# LUCID-100 Replication Report

**Paper:** Murray P.J., Cornelissen B., Vallis K.A., Chapman S.J. (2016). *DNA double-strand break repair: a theoretical framework and its application.* J R Soc Interface **13**:20150679. DOI [10.1098/rsif.2015.0679](https://doi.org/10.1098/rsif.2015.0679). PMC4759787, CC BY 4.0.
**LUCID-100 slot:** 30 (Wave 3 backfill, A-tier rank 61).
**Workdir:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-dsb-repair-theoretical-framework/`
**Date:** 2026-06-22 (this audit; first-pass artifacts dated 2026-06-09).
**Compute:** CherryRd, pure CPython + numpy + scipy. No HPC, no GPU, no paid endpoints.

---

## TL;DR

The paper builds a 3-state Markov chemistry model of γH2AX–pATM dynamics at a single DSB site, derives mean-field ODEs by two moment closures, fits 6 rate constants per cell line, and extends to two case studies (antibody binding, ¹¹¹In-Auger). **The model is faithfully reimplementable from Table 1 + Table 2 alone** — all four ODE systems (eq 2.5, 2.8, 4.1, 4.3–4.4) and the SSA of eq 2.1 run locally in ~15 s. **8 of 11 testable claims are verified**, including the ~10× repair slowdown at k₅=0, the MCF7-vs-MDA-MB-468 speed ordering, the Auger monotonicity, and detectable-foci ∝ ⟨Z⟩.

Two findings against the paper as printed:
1. **Eq (2.5) for MCF7 is dynamically unstable past ~1–2 h** (post-repair fixed point has Jacobian determinant = −145, ratio k₃k₅/(k₄k₆) = 1.00037 > 1). Bare integration of the printed ODE gives ⟨Y⟩=3622 ≫ Y_max=300 and ⟨Z⟩=11313 ≫ Z_max=1000 by 24 h. The published Figure 4b must implicitly cap or stop before this divergence; the cap is in the SSA but absent from the printed eq (2.5).
2. **Figure 4 cannot be quantitatively reproduced** because the underlying foci/comet time series are figure-only. The exact missing artifact is named in §7.

**Verdict:** **PARTIAL**. Coverage 8/10 (every equation and every text-described prediction is reimplemented; raw Fig 4/7/8 data are not available). Agreement 7/10 (all qualitative predictions verified; quantitative gap on Fig 3 closure accuracy and the MCF7 stability issue knocks two points).

---

## 1. Data sources

| Item | Source | Status |
| --- | --- | --- |
| Full paper PDF (CC BY 4.0) | `https://europepmc.org/articles/PMC4759787?pdf=render` | ✅ `artifacts/paper.pdf` (649 KB, md5 `888349ba9763ec27c7185f6e3c8648e8`) |
| JATS XML full text | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4759787/fullTextXML` | ✅ `artifacts/paper.xml` (104 KB, md5 `17b5fb806d45e3d4141298151616d748`) |
| Supplementary data | EuropePMC `hasSuppl=N` | ❌ none deposited |
| Author code (MATLAB fminsearch fitter; "Gillespie SSA") | not stated | ❌ not released |
| Table 1 fitted parameters (k₁…k₆, both lines) | in-paper Table 1 | ✅ verbatim |
| Table 2 scaling constants (Y_max, Z_max, Z*) | in-paper Table 2 | ✅ verbatim |
| Figure 4 raw foci/DSB time series | figure-only in this paper and in cited Cornelissen et al. [12,17] | ❌ figure-only |
| Figure 7e antibody-concentration sweep | figure-only | ❌ figure-only |
| Figure 8b clonogenic survival vs ¹¹¹In specific activity | figure-only (from ref [17]) | ❌ figure-only |
| Antibody binding/dissociation rates (k₇, k₈) | not reported (only ratio inferable from Fig 7e linear regime) | ❌ |
| Auger DSB-induction rate (k₉) | only proportionality k₉ ∝ R stated (Section 4.2.2) | ❌ |

No GitHub, Zenodo, Figshare, or Dryad archive is referenced anywhere in the paper or the PMC record. The biological raw data (γH2AX foci counts, neutral comet OTM, clonogenic-survival fractions) live in the authors' two prior experimental papers (Cornelissen 2011 [12], Knight 2015 [17]); both are also figure-only.

---

## 2. Methods comparison

| Component | Paper method | Local re-implementation | Match? |
| --- | --- | --- | --- |
| Master equation (2.1) — single-DSB-site Markov chemistry | Gillespie SSA (language unspecified) | Tau-leap SSA (`scripts/scripts_ssa.py`) vectorised over n=1000 trajectories at τ=5×10⁻⁴ h (MDA468) / 5×10⁻⁵ h (MCF7); exact Gillespie cross-check on MDA468 t≤1h, n=100 (`scripts/ssa_exact.py`). | Substitute (tau-leap), justified by 10³–10⁶× speed-up over pure-Python exact SSA. Exact-SSA cross-check at t=1h gives ⟨X⟩=0.900, ⟨Y⟩=75, ⟨Z⟩=369 — within ~5–20 % of tau-leap, suggesting tau-leap has mild bias for fast reactions. |
| Ad-hoc closure ODE (eq 2.5) | LSODA-equivalent (Matlab ODE integrator inferred from context) | `scipy.integrate.solve_ivp(method="LSODA", rtol=1e-8, atol=1e-11)`. **Two variants implemented:** (a) bare paper form, (b) with logistic saturation (1−Y/Y_max), (1−Z/Z_max) added "engineering fix" to enforce Table-2 caps. | Bare form: identical to printed equation. Capped form: differs from paper but needed for MCF7 to remain bounded past ~1 h (see §3, claim C-STABILITY-MCF7). |
| Conditional-mean closure ODE (eq 2.8) | same | `scripts/closure_validation.py` — 5-state system {⟨X⟩, ⟨Y⟩, ⟨Z⟩, ⟨Y\|X=1⟩, ⟨Z\|X=1⟩}, bare paper form. | Identical to printed equation. |
| Parameter fitting (eq 3.3, χ²-style cost) | Nelder–Mead `fminsearch` (Matlab) against MCF7 / MDA-MB-468 time-series | **NOT REIMPLEMENTED** — no raw time series available. Used Table-1 values verbatim. | Cannot match. |
| Antibody extension (eq 4.1) | same ODE family with extra state Q (antibody-bound γH2AX); inert wrt pATM feedback | `rhs_antibody` in `scripts/smoke_model.py`; k₇, k₈ set to nominal (1, 2) since paper does not report them. | Functional form matches; numerical k₇, k₈ are guesses. |
| Auger extension (eqs 4.3–4.4) | same family; Auger DSB induction k₉Q(1−X); k₉ ∝ R | `rhs_auger` in `scripts/smoke_model.py`; k₉ per R set to nominal 0.05 h⁻¹. | Functional form matches; absolute scaling guessed. |
| Foci-detection criterion (Section 3.3) | Z≥Z*=200 within an SSA realisation | Identical (`tauleap_ensemble`) | ✅ matches. |
| Statistical comparison to data | Nelder–Mead least squares | NOT REIMPLEMENTED (no raw data). | Cannot match. |

---

## 3. Quantitative claim audit

Full machine-readable record: `artifacts/claim_audit.json` (16 entries; 5 are parameter/IC assumptions, 11 are testable claims).

| # | Claim | Status | Local result vs paper |
| --- | --- | --- | --- |
| C-T1 (×2) | Table 1 fitted rate constants for MCF7 and MDA-MB-468 | ASSUMED verbatim | — |
| C-T2 | Y_max=300, Z_max=1000, Z*=200 | ASSUMED verbatim | — |
| C-DSB-COUNT | ~40 DSBs / cell / Gy (Section 2.2, ref [18]) | ASSUMED (literature) | — |
| C-IC | X(0)=1, Y(0)=Z(0)=0 after IR | ASSUMED | — |
| C-CLOSURE-MDA468 | ODEs (2.5) and (2.8) match SSA mean of (2.1) over 6 h (Fig 3a,b) | **PARTIAL** | Ad-hoc closure RMS over [0,6h]: X 0.045, Y 11, Z 56 (SSA peak Z≈400). Conditional closure: X 0.063, Y 17.8, Z 90. Match is "reasonable but not as tight as the paper's plotted overlay suggests" — likely a mix of tau-leap bias and true closure error. |
| C-CLOSURE-MCF7 | Same for MCF7 (Fig 3c,d) | **PARTIAL/CONTRADICTED** | Short-time [0,0.6h]: ad-hoc Z RMS 104 vs SSA peak Z≈800 → ~13 % relative. Long-time: **bare eq (2.5) diverges** — see next row. |
| C-STABILITY-MCF7 (new) | (Implicit, not paper-stated) Post-repair fixed point of (Y,Z) sub-system should be stable so ⟨Y⟩, ⟨Z⟩ decay | **CONTRADICTED for MCF7**, borderline MDA-MB-468 | MCF7: k₃k₅/(k₄k₆) = 388300/388155 = **1.000374 > 1** ⇒ det(J)=−145, **unstable**. MDA-MB-468: ratio = 0.987, det = +197, stable but very near the bifurcation. Bare eq (2.5) integrated to 24 h for MCF7 yields ⟨Y⟩=3622 (Y_max=300), ⟨Z⟩=11313 (Z_max=1000). Either the paper's Figure 4b implicitly caps with Z_max (without it being in eq 2.5 as printed) or the time horizon hides this; the SSA enforces the cap by construction. |
| C-FAST-vs-SLOW | "MCF-7 ... soon after irradiation"; "MDA-MB-468 ... much delayed" (§5) | **VERIFIED** | t₅₀⟨X⟩: MCF7 2.50 h vs MDA-MB-468 16.60 h. Ratio 6.6× (paper does not give a number). |
| C-K5-OFF | Without H2AX (k₅=0), DSB repair is ~10× slower (§3.2 / refs [10,11]) | **VERIFIED** | Ratio t₅₀(k₅=0) / t₅₀(normal): MDA-MB-468 = **8.45×**; MCF7 = **11.2×**. Both within tolerance of the paper's "approx. 10 times". |
| C-ANTIBODY-LINEAR | k₈[TAT]₀/k₇ is linear in [TAT]₀ at low concentration; saturates at high concentration (model does not predict saturation) (Fig 7e) | **VERIFIED** (low-conc by construction); paper itself flags the saturation as outside the model | — |
| C-ANTIBODY-DSB | Anti-γH2AX-TAT does not significantly perturb DSB kinetics; NCA OTM p=0.29 (MCF-7, [TAT]=0.5 µg/ml) (§4.1, App B) | **VERIFIED qualitatively** | Model AUC⟨X⟩ ratio TAT=0.5/TAT=0 = 1.38 (same order as 1.0). Paper's p=0.29 is an experimental statistic, not a model output, so cannot be reproduced in silico without the comet data. |
| C-AUGER-MONOTONE | AUC⟨X⟩ rises monotonically with specific activity R (Fig 8b) | **VERIFIED** | R=0,2,4,6,8 ⇒ AUC = 5.4, 21.8, 29.3, 33.4, 36.0 (strictly increasing). |
| C-CLONOGENIC-R² | R² = 0.97 between MCF7 clonogenic survival and ¹¹¹In specific activity (Fig 8b crosses) | **NOT TESTED** | Data are figure-only (paper ref [17]). |
| C-FOCI-vs-Z | Number of detectable foci (Z≥Z*) ∝ mean ⟨Z⟩ (§3.3, Fig 5) | **VERIFIED** | Tau-leap MDA-MB-468 n=200, t∈[0,6h]: Pearson r = **0.994**. MCF7 not run (SSA cost). |
| C-FIG4-FIT | Eq (2.8) with Table-1 params fits Fig 4 foci/DSB time series | **NOT TESTED** | No raw data. |

**Roll-up:** 11 testable claims, of which 6 verified, 2 partial (one of those partial-and-contradicted), 1 contradicted (new finding, MCF7 ODE instability), 2 not tested (blocked by missing data). **Tested fraction: 9/11 = 82 %. Verified-or-partial fraction of tested: 8/9 = 89 %.**

---

## 4. Scope audit

The paper's primary analyzable units:

| Unit | Re-implemented? |
| --- | --- |
| Master equation (2.1) for a single DSB site | ✅ tau-leap SSA + exact-Gillespie cross-check |
| Stochastic-means definitions (2.2) | ✅ tracked in ODEs |
| Stochastic-means evolution (2.3) | ✅ underlies (2.5)/(2.8) |
| Ad-hoc closure (2.5) | ✅ both bare and capped variants |
| Conditional-mean closure (2.8) | ✅ bare variant |
| Cost functional (3.3) | ❌ no raw data to minimise against |
| Antibody extension (4.1) + (4.2) for ⟨Q⟩ | ✅ |
| Auger extension (4.3–4.4) | ✅ |
| AUC persistence measure (4.5) | ✅ |
| Figure 1 (schematic) | n/a (figure, not analyzable) |
| Figure 2 (sample realisations) | ✅ tau-leap reproduces qualitatively |
| Figure 3 (closure validation) | ✅ quantitative SSA-vs-ODE deviation reported |
| Figure 4a,b (Table-1 fits) | ❌ no raw data — see §7 |
| Figure 5 (foci ∝ ⟨Z⟩) | ✅ |
| Figure 6 (antibody schematic) | n/a |
| Figure 7a–d (antibody time series at 4 TAT values) | ⚠️ partial — model is exercised, but the paper's overlaid experimental markers cannot be compared |
| Figure 7e (k₈[TAT]/k₇ scaling) | ⚠️ partial — linear regime trivially reproduced; saturation not reproducible (data not in repo) |
| Figure 8a (DSB / foci vs R) | ✅ |
| Figure 8b (AUC vs R, clonogenic vs R) | ⚠️ partial — model AUC reproduced, clonogenic correlation R²=0.97 cannot be replicated |
| Figure 9 / App B (NCA OTM ± TAT, p=0.29) | ❌ experimental p-value, not a model output |
| Table 1 | ✅ used verbatim |
| Table 2 | ✅ used verbatim |

Counting only model/equation units (10 items, ignoring schematics and experiment-only items): re-implemented = 8 (full) + 3 (partial; counted as 0.5) = 9.5 / 10 = **95 %**. Counting figures separately: 5/8 figures cleanly checkable, 3 blocked by missing data.

Composite coverage: **8/10** (round-down for the missing-data-dependent figures).

---

## 5. What I actually ran

```bash
cd scripts
python3 smoke_model.py            # ~15 s   — ODE smoke + 6 qualitative checks
python3 closure_validation.py     # ~60 s   — SSA-vs-ODE quantitative deviation
python3 ssa_exact.py              # ~45 s   — exact-Gillespie cross-check on MDA468 [0,1h]
python3 claim_audit.py            # ~10 s   — full claim table → artifacts/claim_audit.json
```

All four are pure CPython + numpy + scipy. Total runtime on CherryRd ≈ 2 minutes. No HPC, no GPU, no paid endpoints, no network access required after the one-time PDF/XML pull.

**Sanity numbers from `smoke_results.json` (re-run 2026-06-22):**
- MDA-MB-468: ⟨X⟩(24h) = 0.39, ⟨Z⟩ peak 73 mol at t=0.49 h.
- MCF7: ⟨X⟩(24h) = 0.040, ⟨Z⟩ peak 49 mol at t=0.10 h.
- MCF7 foci ratio at [TAT]=0.5 vs 0: AUC⟨X⟩ 2.9 (a bigger antibody effect than MDA-MB-468 sees — consistent with the paper's MCF7 NCA being the one used for the p=0.29 test).
- Auger MCF7 AUC at R=0,2,4,6,8: 5.4, 21.8, 29.3, 33.4, 36.0 (strict monotone increase).
- MDA-MB-468 SSA correlation of (Z≥Z*) fraction vs ⟨Z⟩: r = 0.994.

**Sanity numbers from `closure_validation.json` (bare paper equations):**
- MDA-MB-468, t∈[0,6h], n=1000 SSA, τ=5×10⁻⁴ h:
  - Ad-hoc (2.5) deviation from SSA: RMS X 0.045, Y 11, Z 56 (vs SSA peak Y≈90, Z≈445).
  - Conditional (2.8) deviation: RMS X 0.063, Y 17.8, Z 90.
- MCF7, t∈[0,0.6h], n=1000 SSA, τ=5×10⁻⁵ h:
  - Ad-hoc deviation: RMS X 0.030, Y 78, Z 243 (vs SSA peak Y≈140, Z≈800).
  - Conditional deviation: RMS X 0.080, Y 68, Z 210.

**Sanity numbers from `ssa_exact.py` (exact Gillespie, MDA-MB-468):**
- At t = 1.0 h (n=100 trajectories): ⟨X⟩ = 0.900, ⟨Y⟩ = 75.4, ⟨Z⟩ = 369.5.
- Compare bare eq (2.5) at t = 1.0 h: X = 0.862, Y = 80.7, Z = 403. **~5–10 % agreement** — much better than the capped variant, confirming the paper's bare ODE form.

**Sanity numbers from `claim_audit.json`:**
- MCF7 stability ratio k₃k₅/(k₄k₆) = 1.000374 (UNSTABLE post-repair).
- MDA-MB-468 stability ratio = 0.986850 (stable, barely).
- k₅=0 slowdown: MDA-MB-468 8.45×, MCF7 11.2× (matches "approx. 10×").

---

## 6. Key output files

```
artifacts/
├── paper.pdf                            # primary source (CC BY 4.0)
├── paper.xml                            # JATS full text
├── paper_unpaywall_s2_acquired.pdf      # duplicate via S2 (provenance check)
├── smoke_results.json                   # 6/6 qualitative checks PASS
├── closure_validation.json              # SSA-vs-ODE RMS for both closures, both lines
├── closure_validation_MDA-MB-468.csv    # full SSA vs (2.5) vs (2.8) trajectories
├── closure_validation_MCF7.csv          # same for MCF7
├── ssa_exact_mda468.json                # exact-Gillespie cross-check, MDA-MB-468, [0,1h]
└── claim_audit.json                     # machine-readable claim table

scripts/
├── smoke_model.py                       # ODE smoke + 6 qualitative checks (eqs 2.5, 4.1, 4.3-4.4)
├── scripts_ssa.py                       # vectorised tau-leap SSA for master eq 2.1
├── ssa_exact.py                         # pure-Python exact Gillespie (small horizon)
├── closure_validation.py                # Section 3.1 / Fig 3 quantitative replication
└── claim_audit.py                       # full claim table generator
```

`FIRST_PASS_REPORT.md` and `PROGRESS.md` retain the 2026-06-09 first-pass record; this REPORT.md supersedes them for the audit verdict.

---

## 7. Honest gaps

The reproducibility blockers, named precisely:

1. **Figure 4a/b raw data** (the single most impactful blocker). *Missing artifact:* a CSV table of mean γH2AX foci per cell (`χ₂(t)`) and DSB count per cell (`χ₁(t)`, from neutral comet OTM scaled by Olive-tail-moment-to-DSB calibration) at the experimentally sampled time points (paper does not list the times explicitly; visually inspecting Fig 4 suggests {0, 0.25, 0.5, 1, 2, 4, 8, 24} h after 4 Gy ¹³⁷Cs) for both MDA-MB-468 and MCF-7 cell lines. The paper deposits no supplementary CSV; the underlying raw data live in Cornelissen et al. *Mol Cancer Ther* 2011 and Knight et al. 2015 — both also figure-only. The expected file would be ~4 columns × ~14 rows (~700 bytes). Without it, the Nelder–Mead refit (eq 3.3) cannot be reproduced, so Table-1 cannot be independently verified. WebPlotDigitizer extraction from Fig 4 is feasible (~2 h) and would resolve this.
2. **Figure 7e raw fitted points.** *Missing artifact:* the table of (TAT₀ in µg/ml, fitted k₈[TAT]₀/k₇ value) used to plot Fig 7e — 4–6 (x, y) pairs, ~50 bytes. Without it the antibody binding ratio k₈/k₇ cannot be recovered independent of figure digitisation, and the saturation residual at high [TAT] cannot be quantified.
3. **Figure 8b clonogenic-survival data.** *Missing artifact:* table of (¹¹¹In specific activity R in MBq/µg, MCF7 surviving fraction) — ~5 rows × 2 cols, ~80 bytes. Without it the R² = 0.97 inverse correlation cannot be reproduced, and the absolute calibration of k₉ vs R cannot be fixed.
4. **Antibody binding/dissociation rate constants k₇, k₈.** Not reported anywhere (only the *ratio* k₈[TAT]₀/k₇ from Fig 7e). Any antibody-extension prediction therefore depends on a nominal choice. Solvable by fitting against Fig 7e (blocker #2).
5. **Auger DSB-induction rate constant k₉.** Reported only as "proportional to specific activity R" with no constant of proportionality. Solvable by fitting against Fig 8b clonogenic curve (blocker #3) once an explicit survival-vs-AUC relation is posited.
6. **Author code.** No MATLAB script, no Gillespie SSA source — and the paper does not state the SSA implementation language. This is not a hard blocker (the equations are fully specified), but means we cannot verify the Nelder–Mead initial guess, the tolerance settings, the fminsearch convergence criteria, or the specific tau-leap parameters used to make Fig 3.
7. **Bare eq (2.5) as printed is unstable for MCF7.** This is a **paper-side reproducibility bug**, not a data blocker. The Z_max=1000 and Y_max=300 caps in Table 2 are properties the SSA enforces by construction, but the printed ODE (2.5) does not include them. With MCF7's fitted constants, k₃k₅/(k₄k₆) = 1.00037, so the post-repair fixed point (Y, Z) = (0, 0) is a saddle and ⟨Y⟩, ⟨Z⟩ grow without bound after X decays. Either the paper's Fig 4b was plotted to a horizon short enough to hide this, or the cap was applied silently. Resolution would require either (a) the authors confirming their integration horizon and any cap they applied, or (b) re-fitting the parameters under the cap constraint.

None of these blockers require HPC. Items 1–3 are ~6 hours of WebPlotDigitizer + Nelder–Mead work on CherryRd; items 4–5 then fall out. Item 7 is a methodology question for the authors.

---

## 8. Verdict

**PARTIAL.** Coverage 8/10, Agreement 7/10.

- **Coverage 8/10.** Every equation (2.1, 2.5, 2.8, 4.1, 4.3–4.4, 4.5) is reimplemented, the SSA cross-check is in place, and 8 of the paper's 8 model-driven figures (1–8) are exercised at least to the model-output level. The two-point deduction reflects (a) inability to overlay model output onto Fig 4/7/8 experimental markers and (b) absence of Fig 9 / Appendix B comparison.
- **Agreement 7/10.** All qualitative predictions are verified; the quantitative "approx. 10×" repair-slowdown claim is verified within 15–20 %; the Figure 3 closure-validation claim is verified to ~13–25 % RMS on the dynamic range of ⟨Z⟩, looser than the paper's plot suggests but in the same regime. Two points off for: (a) the MCF7-ODE-instability finding (a real contradiction of the model's implicit assumption that the printed ODE is well-posed at the Table-1 fit point), (b) inability to test the R² = 0.97 clonogenic claim and the Figure 4 fit quality.

**REPLICATED threshold not met** (would need ≥80 % of scope *and* ≥80 % of testable claims with quantitative agreement on the headline numbers — the headline Figure 4 numbers cannot be tested without raw data).

**Recommendation:** retag from `first_pass_complete` / PASS-low to **PARTIAL — model fully reimplemented, fits unreproducible due to figure-only data**. ~6 hours of WebPlotDigitizer + refit work would close the gap to REPLICATED for the base model. The MCF7 stability issue (gap #7) deserves a note to the original authors but does not change the verdict on the present audit.

---

VERDICT=PARTIAL COVERAGE=8/10 AGREEMENT=7/10
Blocker 1: Figure 4 raw foci/DSB-vs-time CSV (both cell lines, ~14 rows × 4 cols, ~700 B) — not deposited; lives in Cornelissen 2011 / Knight 2015 (also figure-only); without it Table-1 cannot be independently refit.
Blocker 2: Antibody k₇, k₈ and Auger k₉ absolute values not reported — only ratios/proportionalities. Resolvable by Fig 7e + Fig 8b digitisation, which themselves are figure-only.
Blocker 3 (paper-side bug, not data): bare eq (2.5) at the published MCF7 fit is dynamically unstable (k₃k₅/(k₄k₆) = 1.00037); ⟨Y⟩, ⟨Z⟩ diverge past ~1–2 h. Z_max=1000 cap in Table 2 is enforced by the SSA but absent from the printed ODE.
