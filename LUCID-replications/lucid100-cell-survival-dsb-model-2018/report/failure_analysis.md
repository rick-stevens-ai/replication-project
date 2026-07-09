# Failure Analysis --- Honest Critique

Wang et al. 2018, *Sci Rep* 8:16202 --- DSB cell-survival model replication.

**This is not a whitewash.** The paper's math reproduces, but the replication as a whole is **PARTIAL, not REPLICATED**, for real substantive reasons enumerated below.

## 1. Queue-verdict mismatch (flagged per instruction)

**Queue label:** REPLICATED
**Actual REPORT.md verdict (§5):** PARTIAL
**Actual REPORT.md §7 (MCDS promotion appendix, 2026-06-21):** "STAYS PARTIAL"
**This backfill preserves:** PARTIAL

**Why the mismatch matters.** If the LUCID queue was used to score model performance or to certify "which papers are REPLICATED", promoting this to REPLICATED would be a factual error. The underlying evidence explicitly does not support REPLICATED status. The 2026-06-21 MCDS promotion test was *designed* to promote it (that's why it was run) and *failed* to do so; someone or some process updated the queue label anyway. This is exactly the class of queue-vs-artifact drift Rick called out in the 2026-07-05 hard requirement.

## 2. What actually failed in the replication

### 2.1 Testable-and-tested claim coverage: 6/30 = 20%

Below the 80%/80% REPLICATED threshold by a factor of four. Not a marginal PARTIAL --- a clear PARTIAL.

### 2.2 The parameterization is not first-principles-reproducible

This is the load-bearing failure.

| $Y_X$ scenario | Value (HSG) | D10 predicted | Error vs paper 4.08 Gy |
|---|---:|---:|---:|
| McMahon 2017 MCDS calibration | 34.4 | 6.57 Gy | +61% |
| Kukla MCDS 3.10A (low-LET) | 8.3 | 27.3 Gy | +569% |
| Free-fit (backed out from D10) | 55.5 | 4.08 Gy | 0% (circular) |

**No independent MCDS calibration reproduces the paper's D10.** The Table 1 fit parameters + published D10 are only self-consistent when $Y_X$ is treated as a free parameter $\approx$55 --- a value Wang does not publish, and that Kukla's fresh MCDS 3.10A run undershoots by a factor of ~7.

This is not a rounding disagreement. It is a factor-of-6 gap between "what independent MCDS says the input should be" and "what Wang's fit parameters implicitly require". Either:

- (a) Wang's MCDS configuration used non-standard cluster definitions or nucleus geometry that inflates $Y_X$ by ~7x --- if so, the paper omitted this critical configuration detail.
- (b) The Table 1 parameters absorb calibration errors from a specific undocumented $Y_X$ value --- if so, the parameters are not transferable and the "mechanistic" framing is overstated.
- (c) The 4.08/7.07 Gy D10 values themselves are anchored to a specific experimental subset whose MCDS pre-processing is undocumented.

None of these are resolvable from published information alone. **This gap is real, load-bearing, and the paper does not acknowledge it.**

### 2.3 The 2026-06-21 MCDS promotion attempt FAILED

Kukla generated a fresh MCDS 3.10A $\Sigma_{\text{DSB}}(\text{LET})$ curve, motivated exactly by the hypothesis that a better MCDS would close the $Y_X$ gap and promote PARTIAL$\to$REPLICATED. The result:

- HSG D10 predicted 27.3 Gy vs paper 4.08 Gy: **+569% error**
- V79 D10 predicted 30.0 Gy vs paper 7.07 Gy: **+324% error**

The promotion attempt *strengthened* the PARTIAL verdict rather than overturning it. Documented in `results/mcds_promotion_result.txt` and REPORT.md §7. This is a genuine negative result --- the standard treatment would be to promote or demote; the honest outcome was "attempted promotion, promotion refuted, verdict confirmed PARTIAL".

### 2.4 Raw-curve refits (106 curves) not performed

The paper's central methodological claim is that 6 parameters fit 106 clonogenic-survival curves (54 HSG + 52 V79) with the quoted $R^2$ values (0.78-0.99 depending on target). None of these 106 refits were performed in this replication because:

- PIDE v3.2 requires institutional-email registration + manual approval (blocker not resolved in the replication window)
- Furusawa et al. 2000 raw survival points are behind the BioOne paywall

This is a data-access failure, not a methodological failure --- but it means the paper's central quantitative claims (all the $R^2$ values in Table 2 / Figs 2--5) are **untested** here. 18/30 headline claims are untestable because of these two blockers.

### 2.5 RBE and mixed-beam claims (Figs 4-5) not tested

Requires MCDS $Y(\text{LET}), \lambda(\text{LET})$ per particle species for 5+ ions. MCDS was not installed in the original replication window; Kukla's later single low-LET point does not close this gap.

## 3. Which specific claims were tested vs assumed

Per Rick's 2026-07-05 hard requirement:

### 3.1 LET dependence
- **Qualitatively tested:** $\alpha$-peak location, $\alpha/\beta$-rise, $\beta$-decline all match paper *qualitatively*.
- **Not quantitatively tested:** no $R^2$ against Furusawa/PIDE data. The paper's own $R^2(\alpha) \approx 0.78$ and $R^2(\beta) \approx 0.15$ are not verified here.

### 3.2 Mixed-beam prediction (Fig 5, $R^2=0.762$)
- **Not tested.** Requires per-particle MCDS + PIDE mixed-beam curves.

### 3.3 Dose-rate
- **Not addressed by the paper.** The Poisson NHEJ formulation assumes acute delivery. Chronic / low-dose-rate regimes are outside the paper's scope. Not a replication gap.

### 3.4 In-sample vs out-of-sample
- **In-sample only.** The paper fits and evaluates on the same 106 curves. There is **no held-out validation set**. All reported $R^2$ values are in-sample. This is a paper-side methodological weakness that gets propagated as "the model has high $R^2$" without qualification. Any real predictive-power claim needs cross-validation, which the paper does not do.

### 3.5 DSB $\to$ lethal-lesion conversion
- **Phenomenological, not mechanistic.** The 6 fit parameters $(\mu_x, \mu_y, \zeta, \xi, \eta_1, \eta_\infty)$ are effective coefficients. Their functional forms are Poisson-misrepair-motivated (which is a mechanistic *heuristic*), but the parameter values are not derived from NHEJ biochemistry (Ku70/80 binding, DNA-PKcs kinetics, XRCC4 ligation rates, etc.). The paper's framing as a "mechanistic model" is misleading; more precise language would be "semi-empirical framework with Poisson-motivated functional forms".

## 4. Residual uncertainty

The dominant residual uncertainty is the $Y_X$ ambiguity (§2.2). Without either (a) the authors' original MCDS input files or (b) a from-scratch full-fit rerun on the 106 PIDE curves with a documented independent MCDS calibration, no third party can distinguish among the three explanations in §2.2. This is not a small number-fudging discrepancy; it is a factor-of-6 gap that the paper does not disclose.

Secondary uncertainties:
- Whether the RBE predictions generalize to unfit LETs (Q2 in open_questions).
- Whether DSB complexity (vs number) is a missing predictor (Q3).
- Whether the model transfers to hypoxia (Q4).
- Whether track-structure DSB spectrum vs collapsed $\lambda$ matters at proton clinical LETs (Q5).

## 5. What would flip the verdict to REPLICATED

Estimated 20-40 h of additional work (see workflow.md §Work estimate):

1. PIDE registration + Furusawa data acquisition (institutional email + waiting period)
2. MCDS install + rerun with Wang geometry
3. Full 106-curve refit; compare Table 1 against fresh fit
4. Cross-validate (leave-one-ion-out)
5. Regenerate Figs 4-5 quantitatively

Or, shortcut: **contact Junli Li (Tsinghua)** and request the original MCDS input tables. If the authors provide them and they reproduce the ~55 $Y_X$, that resolves §2.2 immediately and promotes to REPLICATED. If they don't respond or the data is unavailable, PARTIAL is the accurate ceiling.

## 6. What I did NOT do

- I did not re-run any simulations for this backfill (per instruction).
- I did not re-generate figures; the existing PNGs are preserved.
- I did not modify any existing file (REPORT.md, src/, results/, figures/, paper.pdf all preserved).
- I did not soften the verdict to match the queue label.
- I did not claim to have tested anything I did not test.
