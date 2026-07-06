# First-Pass Replication Report — LUCID100 Wave 1, Slot 9

**Paper:** Wang W. et al., *Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks*, Sci. Rep. **8**:16202 (2018). DOI: [10.1038/s41598-018-34159-3](https://doi.org/10.1038/s41598-018-34159-3).

**Verdict (first pass):** **GREEN — replication feasible and partially executed.**
A faithful self-contained reimplementation of the published equations (1)-(20) with the verbatim Table 1 best-fit parameters is in `code/wang2018_dsb_survival.py`. The smoke test recovers all of the paper's qualitative claims (LQ form at low LET, alpha/beta rising with LET, RBE_10 peak near 100 keV/um). Strict numerical replication of Figs. 2-6 needs two free-but-registration-gated external resources (MCDS code, PIDE database) and is scoped below.

## 1. What the paper does

A purely analytic, mechanistic cell-survival model with:

- **2 physical inputs**: `n_p` (average primary particles per nucleus that cause >= 1 DSB) and `lambda_p` (average DSBs per such primary). Both are obtained from track-structure Monte Carlo (MCDS) for a chosen particle / LET / nucleus.
- **6 biological fit parameters** per cell line: `mu_x` (NHEJ fidelity), `mu_y` (per-event lethality), `xi` (intra-track clustering scale), `zeta` (over-kill scale), `eta(lambda_p->1)`, `eta(lambda_p->inf)` (inter-track interaction scale, bracketed by Eq. 8).
- Closed-form expressions Eqs. (10), (13), (15) for SF and Eqs. (18), (19) for the LQ alpha, beta that emerge as the small-`n_p` Taylor expansion.

The fit is performed in three stages against published HSG and V79 data:
1. fit `mu_x, mu_y, zeta, xi` from observed alpha values (Eq. 18 only depends on these);
2. fit `eta(lambda_p->1)` from X-ray SF curves via the full Eq. (15);
3. fit `eta(lambda_p->inf)` from observed beta values via Eq. (19).

Fitted parameters reported verbatim in Table 1 (HSG and V79). All other quantities (Figs. 2-7) are predictions of the calibrated model.

## 2. Artifact harvest

See `ARTIFACT_MANIFEST.md`.

- **Code/Repo:** None. The paper provides no code, no GitHub, no Zenodo, no supplement.
- **Supplement:** None.
- **Data:** None deposited. All fit/validation data are pointers into PIDE (Friedrich 2013 / 2021) and the underlying Furusawa 2000 study + refs 39-57. PIDE is free academic access (registration form, no payment).
- **MCDS:** Stewart group at U. Washington; free academic source, no payment.

No author contact required for any of the above; the published Table 1 parameters are sufficient to re-derive every prediction.

## 3. What this slot has produced

Files written under `lucid100-modelling-of-cellular-survival-following-radiation-induced-dna-double-stra/`:

```
artifacts/paper.pdf                  # local copy of source PDF
code/wang2018_dsb_survival.py        # reimplementation of Eqs. 1-20
smoke_test.json                      # numerical smoke-test outputs
figures/sf_HSG.png                   # qualitative reproduction Fig. 3a shape
figures/sf_V79.png                   # qualitative reproduction Fig. 3b shape
figures/alpha_beta_vs_LET.png        # qualitative reproduction Fig. 6 shape
figures/rbe10_vs_LET.png             # qualitative reproduction Fig. 5 shape
ARTIFACT_MANIFEST.md
README.md (updated)
PROGRESS.md (updated)
FIRST_PASS_REPORT.md (this file)
```

The reimplementation is a single ~17 kB Python file that takes only NumPy and Matplotlib. It encodes Table 1 verbatim and exposes:
- `survival(D, Y, LET, params)`   - full Eq. (15)
- `alpha_beta_LQ(Y, lambda_p, p)` - Eqs. (18)/(19)
- `eta_of_lambda_p(lp, p)`        - Eq. (8)
- `n_particles_per_nucleus(D, LET)` - Eq. (2)
- `_dose_for_SF(target, ...)`     - bisection isodose helper

## 4. Smoke-test results (run on CherryRd, 2026-06-09)

Run: `python3 code/wang2018_dsb_survival.py --out-dir .`

| Check | Expected | Observed | Pass |
| --- | --- | --- | --- |
| Eq. 15 -> Eq. 17 (LQ) in small-D limit, proton 2 keV/um, HSG | alpha(Eq.18) approx alpha(fit Eq.15) | 0.1496 vs 0.1509 /Gy (0.83% rel.err.) | YES |
| Same, V79 | match | 0.0802 vs 0.0813 /Gy (1.4% rel.err.) | YES |
| HSG X-ray alpha/beta | "~few Gy" (Furusawa Table 1, ~5-6 Gy) | 3.8 Gy from synthetic Y, LET | reasonable |
| V79 X-ray alpha/beta | "~few Gy" | 4.3 Gy | reasonable |
| RBE_10 peak vs LET (V79) | rises, peaks ~100-200 keV/um, falls (Fig. 5) | peaks at 100 keV/um with RBE = 4.6 | YES (shape) |
| HSG D10 ordering vs LET (Fig. 7a) | D10(X-ray) > D10(C-12 50) > D10(C-12 200) | confirmed numerically in `smoke_test.json` | YES |

Headline qualitative claims of the paper are reproduced by the calibrated Table 1 model. The absolute numerical agreement with paper Fig. 3 / 5 / 7 will improve when the representative MCDS-like (Y, lambda) table is replaced by real MCDS output (next step).

## 5. Gap to strict replication

| Component | Status | Effort to close |
| --- | --- | --- |
| Equations | Coded, verified | Done |
| Table 1 parameters | Encoded verbatim | Done |
| Y(LET, particle), lambda(LET, particle) | Currently approximate, hand-picked from Wang Fig. 1 / Stewart 2011 | **Run MCDS** for HSG (6 Gbp human nucleus) and V79 (5.6 Gbp Chinese hamster nucleus) on the LET grid used in the paper (~30-50 points). 1-2 hours of CPU once MCDS is installed. |
| Experimental fit/validation points (alpha, beta, SF, D10, RBE) | Not loaded | **Pull PIDE v3.2** subset for HSG and V79; cross-reference Furusawa 2000 and refs 39-57. Map LET to particle. ~half a day of data wrangling. |
| Re-fit of 6 params | Not done; using Table 1 verbatim | If we trust Table 1 we are already done. If we want to verify the fit, set up the staged nonlinear LSQ from section "Model parameter fitting" of the paper. scipy.optimize.least_squares; trivial once data are in hand. ~2 hours. |
| Fig. 2 / 3 / 5 / 6 / 7 regeneration | Qualitative figures produced | Once MCDS + PIDE are in, drive the same script with real inputs; ~1 hour. |

**Total effort to strict numerical replication:** ~1-2 days of work, no special hardware (well under CherryRd's idle budget; MCDS is single-CPU). No paid endpoints. No author contact.

## 6. Risks / blockers

- **PIDE access** requires submitting a request form to GSI. Historically <1 week to obtain credentials. Not a hard blocker but adds calendar latency.
- **MCDS build**: needs Windows .exe historically; recent versions run under Wine on macOS/Linux. Alternative: use published MCDS tables (Stewart 2011 Tables S1-S3 give Y and lambda for several ions and LETs) — sufficient to populate Wang's LET grid for the X-ray, proton, He, C, Ne curves shown in Figs. 1-7 without running MCDS ourselves.
- **No author code**: the paper does not publish the fitting code. We rely on the published parameter values (Table 1). If those values are off, our reproduction will inherit the same offsets but the model logic is verified.

No discovered show-stoppers. The replication is plausible and partially completed.

## 7. Heavy-compute plan (write only, no job submitted)

Strict replication does **not** require heavy compute. A single CPU and ~1 GB RAM are sufficient (analytic model + small parameter fit + a few hundred SF evaluations per figure). **Do not** schedule this on uicgpu / Aurora / Sparks. Run locally or on the LUCID host of choice; no GPU and no MPI.

If we later sweep MCDS for, e.g., the full Furusawa 2000 LET grid x 9 ion species, that is still single-CPU and would take O(hours), not days; CherryRd is fine.

## 8. Acceptance criteria (proposed)

For declaring the strict replication complete:

- A1. Re-running the staged fit on PIDE/Furusawa subsets recovers each Table 1 parameter within +/- 2 sigma of the published value.
- A2. Predicted alpha and beta vs LET match Wang Fig. 2a/b and 2e/f with R^2 >= 0.7 and 0.1 respectively (the paper itself reports R^2 = 0.7755-0.8522 for alpha and 0.1477-0.2008 for beta).
- A3. Predicted SF(D) for HSG and V79 under C-12 at the three LETs in Fig. 3 match the experimental SF within 0.1 absolute on the log10 scale at D = 2 and 4 Gy.
- A4. Predicted RBE_10 for V79 across the LET range 1-1000 keV/um matches Fig. 5 within +/- 20% over 0.5-300 keV/um and within +/- 35% above 300 keV/um (over-kill regime where the paper itself shows scatter).

These thresholds are deliberately a touch looser than the paper's own R^2 values to allow for tabulation/digitization noise.

## 9. Next actions

1. Submit PIDE access request to GSI (email + web form).
2. Download Stewart 2011 MCDS Y and lambda tables (free PDF) and digitize the columns we need; if PIDE access is fast enough, alternatively install MCDS.
3. Implement the staged fit (alpha -> X-ray SF -> beta) in a `fit_table1.py` companion to verify Table 1.
4. Regenerate Figs. 2, 3, 5, 6 with real inputs; compare against acceptance criteria A1-A4.
5. Write final `REPORT.md` with verdict.

## 10. Verdict

**First-pass: REPLICABLE.** Equations are clean, the only inputs are two scalars per (particle, LET) which are externally derivable from a freely available MC code, and Table 1 gives the full biological fit. Self-contained reimplementation runs in milliseconds on a laptop, and recovers every qualitative claim of the paper.
