# Failure Analysis — Turner 2019 γ-H2AX Biodosimetry

**Verdict is REPLICATED, but the label is narrower than it sounds.** This
file inventories what the replication does NOT establish, honestly.

## What actually failed / didn't work

### 1. Individual parameter values (r, p) could not be pinned down
Our refit slides (r, p) off the paper's individual values:
- paper: r = 1.07×10⁶ d⁻¹, p = 0.153
- refit: (r, p) drifts under a soft upper bound r ≤ 10⁸

Root cause: the stretched-exponential Q₂ = 1 − (1+rt)^p becomes
Q₂ ≈ 1 − (rt)^p in the r·t≫1 regime — only p·log(r) is identified.
This is a **structural non-identifiability**, not numerical noise, and
the paper does not flag it. A rewrite in identifiable coordinates
(e.g. one parameter for the asymptotic slope, one for early-time scale)
would fix it. Not our bug — but not a "verbatim replication" of Table 2
either.

### 2. ROC AUC gap of 0.09 vs paper
- Paper AUC: 0.93 (CI 0.806–1.0)
- Ours (paper params): 0.84
- Ours (refit + MC): 0.85

Ours lands inside the paper's 95% CI, but 0.09 below the point estimate.
The most likely explanation is a sample-size difference: the paper's
0.93 appears to treat each of the 8 mice per point as an independent
sample (n≈160), whereas we can only work from published group means
(n=20 = 4 activities × 5 days). We cannot close this gap without raw
per-mouse fluorescence values, which are not in the supplements.

### 3. No blind-dose challenge was reproduced
The paper's "Monte Carlo validation" operates on the SAME data used to
fit the model. There is no held-out mouse, no held-out activity level,
no external test set. Our replication inherits this limitation exactly —
we did not construct a synthetic hold-out either, because the point of
this pass was faithful reproduction, not extension. The claim
"AUC = 0.93 for retrospective activity classification" is therefore an
**in-sample fit statistic**, not a genuine predictive-performance
number.

### 4. Biokinetics (Eq. 3) not re-derived from raw data
The paper's Table 1 doses depend on a two-exponential whole-body
retention fit with (fast: 0.6 d, slow: 7.8 d) half-lives. Reproducing
Eq. 3 requires per-animal retention time series that are not published.
We used Table 1 doses verbatim as-published. This is a **spot-check**,
not an end-to-end reproduction of the physics side of the pipeline.

## Coverage gaps by physical regime

| Regime the paper covers | Regime replication tests | Regime NEITHER covers |
|-------------------------|--------------------------|-----------------------|
| Acute IV bolus, 5.74–9.28 MBq internal ¹³⁷Cs | Same (verbatim) | External photon at same integrated dose |
| Days 2, 3, 5, 7, 14 post-injection | Same (verbatim) | Days 1, 4, 6, 10, 21+ (undersampled outside 2–3 d optimum) |
| Whole-body well-mixed biokinetics | Same (verbatim) | Partial-body / non-uniform contamination |
| Group means of n=8 mice | Same (verbatim) | Single-donor CV / real-deployment noise |
| Blood + spleen MNCs | Same (verbatim) | Other tissues; other DDR markers |
| Accrued dose 3.4–5.6 Gy (day 14) | Same | Operational triage regime <0.5 Gy |

**The replication reproduces the paper's regime cleanly but the paper's
regime is narrow.** It does not establish that γ-H2AX biodosimetry
works in the operationally relevant sub-Gy regime, and this replication
cannot change that.

## Residual uncertainty

1. **Model identifiability.** Individual (r, p) are not uniquely
   determined by the published data. The biological interpretation of
   r ("repair rate") and p ("stretch exponent") is therefore weaker
   than the paper suggests.
2. **Inter-individual CV.** Unknown from published data. Any single-mouse
   deployment noise estimate would require raw per-animal fluorescence.
3. **Species translation.** All data is C57BL/6 mice; extrapolation to
   humans is not tested here and is well outside the paper's scope.
4. **LoD.** The lowest activity is far above the operational triage
   cut-off. The pipeline may or may not resolve 0.1–0.5 Gy — unknown.
5. **Time-window optimum.** Sampled only at 5 discrete days; the true
   information-theoretic optimum sampling time is not localized.

## Honest bottom line

The Turner 2019 fit and its in-sample Monte-Carlo inversion **reproduce
cleanly** from public data with no author contact and no paid tools.
That is a genuine scientific-integrity win: someone else can rebuild
this pipeline in ~30 seconds from what BMC actually published, and get
matching correlations and matching-CI ROC.

But calling this "REPLICATED" hides that the paper itself only
establishes an **in-sample calibration** in a narrow physical regime
with **degenerate parameters**. The replication is faithful; the
underlying claim is not as strong as the paper's abstract suggests.
Future work (see `open_questions.json`) should test blind-dose
challenges, low-dose LoD, non-uniform geometry, and joint-assay
integration before this technique is deployed for actual triage.
