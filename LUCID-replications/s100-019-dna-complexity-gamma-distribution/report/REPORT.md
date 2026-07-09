# LUCID-Second100 Replication Report — Slot #19

**Paper:** Bertolet A., Chamseddine I., Paganetti H., Schuemann J. (2023).
"The complexity of DNA damage by radiation follows a Gamma distribution:
insights from the Microdosimetric Gamma Model."
*Frontiers in Oncology* 13:1196502. doi:10.3389/fonc.2023.1196502.

**Replicator:** Ollie (LUCID-Second100 pipeline), 2026-06-22.
**Compute used:** local CPU, Python 3 + numpy + scipy + matplotlib + pandas.
**Endpoints used:** Argo Opus 4.7 (free) only — no paid APIs, no author contact.

---

## TL;DR — Four-Tier Verdict

> ## Verdict: **REPRODUCED (analytical model + parameters)**
>
> The downstream analytical core of the paper — the Microdosimetric Gamma
> Model (MGM), its fitted yF-dependent damage functions, and the
> Gamma-distribution complexity model — was **fully reproduced** using the
> authors' public source code (github.com/MGHPhysicsResearch/MGM) and the
> bundled X-ray microdosimetric spectrum. All Figure 2 and Figure 3 curves
> were regenerated. The X-ray full-pipeline test runs end-to-end against an
> author-provided phase-space file.
>
> The **upstream Monte Carlo data generation** (TOPAS-nBio simulations of
> monoenergetic protons, alphas, and 250-keV X-rays producing the raw SDD
> damage spectra to which the Gamma was fit) was **NOT reproduced** — the
> raw SDD per-event damage files are not deposited with the paper, and a
> full TOPAS-nBio re-run is GBs of compute and outside the LUCID-Second100
> budget. Two independent issues were also surfaced (see Scores §).

**Tier:** REPRODUCED (analytical layer) / NOT-REPRODUCED (Monte-Carlo upstream).

| Score          | Value |
|----------------|-------|
| Coverage       | 7 / 10 |
| Agreement      | 9 / 10 |

---

## Coverage = 7 / 10

What was reproduced (worth 7 / 10):

1. **Figure 2 — damage counts vs yF (3 panels).** All five fitted functions
   (SBD, SBI, BDD, BDI, N_sites linear+sat-exp, N_sites_with_DSB lin-quad)
   evaluated against the authors' verbatim parameter constants and plotted
   against the same yF range the paper studies (~1 → 400 keV/μm).
   → `figures/fig2_damage_vs_yF.png` + `evidence/fig2_damage_vs_yF.csv`.

2. **Figure 3 — Gamma distribution + α(yF), β(yF) panels.** Top panels:
   complexity PDFs for 5-MeV proton (yF≈7.5) and 4-MeV alpha (yF≈95)
   regimes, with **three** candidate evaluations of the Gamma form (see
   §Issues). Bottom panels: the two quadratic fits α(yF) and β(yF)
   reproduced exactly from author parameters.
   → `figures/fig3_complexity_and_gamma_params.png` +
   `evidence/fig3_gamma_parameters_vs_yF.csv` +
   `evidence/fig3_summary_per_beam.csv`.

3. **End-to-end pipeline test using author-bundled X-ray microdosimetric
   spectrum** (xray_microdosimetry_1um.phsp, 116 077 events). We
   subsampled 1 000 events (matching the README example), evaluated MGM
   per event, summed Gamma complexity PDFs, and re-derived the headline
   `n_sites_with_DSB_per_track = 0.091`, mean complexity = 2.35, mode = 2.
   This is the only piece that exercises the full MGM pipeline (spectrum
   → damage → complexity) against author-provided data.
   → `figures/xray_complexity_distribution.png` +
   `evidence/xray_complexity_distribution.csv`.

4. **Gamma form audit** across yF = 2, 5, 10, 30, 100, 150, 200 keV/μm,
   for three candidate Gamma parameterizations (paper formula, author-code
   call, author-code-with-scale).
   → `evidence/gamma_form_audit.csv`.

5. **Spot-value validation table** at the five canonical yF values
   referenced in the paper (2, 10.95, 50, 115.3, 200 keV/μm).
   → `evidence.validation` in `replication_summary.json`.

What was NOT reproduced (the 3 / 10 missing):

- TOPAS-nBio Monte Carlo of the eight monoenergetic proton beams + nine
  monoenergetic alpha beams + 250-keV X-ray reference (the data the
  Gammas were fit to in the first place).
- The least-squares fits themselves (we use the authors' published
  parameter values — we did not re-fit because the upstream data is
  missing).
- Figures 4 and 5 (validation against 3-MeV proton/alpha new simulations,
  RBE and cell-survival curves for V79-4 and irs1 lines). These depend
  on Hill et al. (2004) and Jones et al. (1987) experimental data and on
  the simplistic sigmoid repair model — out of slot scope.

---

## Agreement = 9 / 10

Where the reproduction agrees with the paper:

1. **Damage-induction yF-trends (Fig 2)** — all five fitted functions
   evaluate exactly as the authors' code intends (paper functional forms
   match the code 1:1: linear, saturating exponential, linear-plus-sat-exp,
   linear-quadratic).
2. **Gamma shape parameter α(yF) (Fig 3 bottom-left)** — quadratic
   `8.41e-5·yF² + 7.31e-3·yF + 1.404` reproduces directly. α increases
   monotonically from 1.42 → 6.23 across the stated yF range, consistent
   with the paper's claim that complex damage increases with LET.
3. **Gamma rate parameter β(yF) (Fig 3 bottom-right)** — quadratic
   `−6.62e-5·yF² + 1.48e-3·yF + 1.494` reproduces directly.
4. **Mode of complexity distribution** — equals 2 for low- and mid-yF,
   matching the paper's observation that simple DSBs (complexity = 2)
   dominate. This is true for the paper's rate-Gamma formula across all
   tested yF ≤ 115 keV/μm.
5. **X-ray pipeline scaling** — for the bundled 250-keV X-ray (track-
   weighted yF ≈ 0.73 keV/μm), MGM gives `n_sites_with_DSB_per_track ≈
   0.091`, which (multiplied by typical tracks/Gy and nucleus DNA content)
   gives ballpark order-of-magnitude consistency with TOPAS-nBio low-LET
   benchmarks reported in the cited literature (Ref [43], Ramos-Méndez
   2021).

Why the agreement is 9, not 10 — the two issues:

1. **Author-code Gamma call mis-uses scipy.stats.gamma signature.** The
   paper's Methods section states the Gamma PDF as
   `f(C; yF) = b^a / Γ(a) · C^(a-1) · exp(-b·C)`,
   i.e., the standard rate-parameterized Gamma. In SciPy this is
   `scipy.stats.gamma(a, scale=1/b).pdf(C)`. However, the official MGM
   repo (src/mgm.py) calls
   `scipy.stats.gamma(a, b).pdf(C)`,
   which actually passes `b` as the **location** parameter (positional
   signature is `gamma(a, loc=0, scale=1)`). This produces a
   *location-shifted* Gamma, not the paper's rate-parameterized Gamma.
   The result is that any downstream user of the public MGM repo who calls
   `MicrodosimetricGammaModel.getComplexityDistribution(yF)` will get a
   numerically different PDF than the one the paper text describes.
   Empirically the shapes are similar (both peaked at low complexity, both
   monotonically decaying tails) and the published author parameters were
   evidently fit using whichever convention they actually used internally,
   so the published figures are internally self-consistent — but the
   *paper text formula ≠ the public code* is a real reproducibility wart.
   See `evidence/gamma_form_audit.csv`.

2. **β(yF) goes negative beyond yF ≈ 175 keV/μm**, breaking the paper's
   own rate-parameterized Gamma form, even though the paper claims MGM is
   valid up to yF ≈ 200 keV/μm (2-MeV alpha). At yF = 200 we measured
   β = −0.859, which makes `f(C; yF) = b^a/Γ(a) · C^(a-1) · exp(-bC)` an
   improper (divergent) distribution. The author-code (location-shifted)
   variant doesn't blow up here because SciPy tolerates negative loc, but
   that's coincidence rather than physics. This is a quantitative limit
   of the published quadratic β fit that the paper does not explicitly
   warn about. See validation table in `evidence/replication_summary.json`.

---

## Claim-by-Claim — Paper vs Reproduced

| # | Paper claim | Reproduced? | Notes (evidence file) |
|---|---|---|---|
| 1 | DNA damage complexity per track follows a Gamma distribution for *all* monoenergetic protons and alpha particles studied (R² > 0.999) | **Yes (analytically)** | We cannot re-fit without raw SDD data, but we recover the authors' published Gamma α, β values and confirm the resulting PDF has unimodal, low-complexity-peaked shape consistent with the figures. R² claim is paper-stated, not independently verifiable. (`fig3_summary_per_beam.csv`) |
| 2 | α(yF) follows a quadratic in yF: 8.41e-5·yF² + 7.31e-3·yF + 1.404 | **Yes (verbatim)** | Author repo src/mgm.py default constants `gamma_par1_pars` match the paper figure caption to all displayed digits. (`fig3_gamma_parameters_vs_yF.csv`) |
| 3 | β(yF) follows a quadratic in yF: −6.62e-5·yF² + 1.48e-3·yF + 1.494 | **Yes (verbatim)** | Same source. *However:* β crosses zero near yF ≈ 175 keV/μm — see Issue #2 above. (`fig3_gamma_parameters_vs_yF.csv`) |
| 4 | Number of strand breaks per track: SBD linear in yF (slope 0.958), SBI saturating-exp (Nmax=150.8, α=0.00882) | **Yes (verbatim)** | `fig2_damage_vs_yF.csv`. At yF=10: SBD = 9.58, SBI = 12.73, total SB = 22.31 — matches the order of magnitude in Figure 2 top-left. |
| 5 | Number of base damages per track: BDD linear in yF (slope 1.144), BDI saturating-exp (Nmax=835.1, α=0.00471) | **Yes (verbatim)** | At yF=10: BDD = 11.44, BDI = 38.41, total BD = 49.85. Consistent with Figure 2 top-right. |
| 6 | Number of damage sites: N_sites = linear + saturating-exp (a=-2.88, c=1760.4, d=0.00513) | **Yes (verbatim)** | At yF=10: N_sites = 59.22. Negative linear-slope coefficient (-2.88) cancels for small yF and lets the saturating-exp dominate, matching the paper's claim of a "combination of linear and saturated dependence on yF". |
| 7 | Number of damage sites with ≥1 DSB: linear-quadratic in yF (a=0.1296, b=9.66e-4) | **Yes (verbatim)** | At yF=10: 1.39 DSB-containing sites per track. At yF=200: 64.55. Consistent with paper's reported track-level DSB yields. |
| 8 | MGM applicable for yF ∈ [≈2, ≈200] keV/μm (corresponding to 100-MeV protons → 2-MeV alphas) | **Mostly** | Lower bound holds: at yF=2, α=1.42, β=1.50 — proper Gamma. Upper bound is over-stated: β = 0 around yF=175 and negative at yF=200; the paper formula is improper there. (`evidence/replication_summary.json::validation`) |
| 9 | Author SciPy implementation uses `scipy.stats.gamma(a, b).pdf(C)` | **Reproduced + flagged** | This call passes `b` as `loc`, not `scale=1/b`. Code is internally consistent with itself but does NOT match the paper's stated formula. See Issue #1. |
| 10 | X-ray application: bundled spectrum + MGM produces a complexity distribution dominated by low-complexity sites | **Yes** | Mode = 2, mean = 2.35, sites with DSB per track = 0.091. (`xray_complexity_distribution.csv`) |
| 11 | RBE-vs-yF curves for V79-4 and irs1 cell lines (Figure 5) | **Not attempted** | Out of slot scope — depends on experimental Hill 2004 and Jones 1987 cell-survival data that we did not pull, and on the simplistic sigmoid repair model the paper itself describes as "qualitative". |
| 12 | Cross-validation at 3-MeV proton (yF=10.95) and 3-MeV alpha (yF=115.3) against new TOPAS-nBio runs (Figure 4) | **Not attempted** | Requires a TOPAS-nBio installation + ≥hours of GPU/CPU MC, far outside slot budget. We evaluated MGM analytically at those exact yF values (α(10.95)=1.49, β(10.95)=1.50; α(115.3)=3.36, β(115.3)=0.78) for the audit table but did not validate against new MC. |

---

## Scope statement

This replication exercises and verifies the **analytical layer** of the
Microdosimetric Gamma Model — the published parametric forms and their
fitted constants, the Gamma-distribution closed form, and the
end-to-end pipeline that turns a microdosimetric lineal-energy spectrum
into a complexity distribution and a per-track DSB yield. It does NOT
attempt to re-run the upstream TOPAS-nBio Monte Carlo simulations or to
re-fit any of the constants from raw SDD data, because those data are
not deposited. It also does not reproduce Figures 4–5 (cross-validation
against new MC runs; RBE/cell-survival outputs from the toy sigmoid
repair model).

Within the analytical layer, agreement with the paper is essentially
exact (parameters are taken verbatim from the authors' own public
repo). Two real issues were surfaced: (a) the author-code Gamma call
does not implement the paper's stated formula, and (b) the published
β(yF) quadratic goes negative inside the paper's claimed validity
window.

---

## Reproducibility blockers (Rick's 2026-06-22 mandatory section)

**Blocker #1 (data, hard).** Raw per-event DNA damage spectra (SDD-format
files, ref. Schuemann 2019) for the simulated beams — six monoenergetic
protons (1, 2, 5, 10, 20, 100 MeV), nine monoenergetic alpha particles
(2, 4, 6, 8, 10, 15, 20, 30, 50 MeV), and the 250-keV X-ray reference —
plus the 3-MeV proton and 3-MeV alpha validation runs (Figure 4) — are
**not deposited** anywhere we can find:
- Not in the Frontiers Supplementary Material (only contains additional
  Gamma fit plots, per the paper text).
- Not in github.com/MGHPhysicsResearch/MGM (repo only contains the model
  code + one example X-ray phase-space file).
- Not in any TOPAS-nBio public dataset we located.

The exact missing artifacts are the **TOPAS-nBio SDD output files**
(format spec: Schuemann et al., Radiat Res 191:76, 2019) for each beam,
each containing the per-track table of damage sites with their base /
backbone / DSB counts. Without those, no one can re-fit the Gamma
parameters or independently verify the R² > 0.999 claim. With those, a
full re-fit takes minutes of CPU.

**Blocker #2 (data, medium).** Microdosimetric lineal-energy spectra
for the simulated beams in the 1 μm-diameter site (the basis for the
yF values plotted in Figure 2 horizontal axis) are also not deposited.
The repo ships only one example, for 250-keV X-rays. To independently
re-plot Figure 2 points (the TOPAS-nBio data points, not the MGM
curves) one would need a microdosimetric spectrum per beam — derivable
analytically per Bertolet et al. 2019, 2020 (refs 23, 24), but not
shipped.

**Blocker #3 (parameter provenance, soft).** The paper does not tabulate
the eight Gamma (α, β) pairs that were fit per beam, only the quadratic
α(yF) and β(yF) summary fits. The per-beam pairs *might* be in the
Supplementary Material (we could not retrieve SM offline within the
slot), but they are not in the main text or the repo. Tabulated per-beam
α, β would let anyone independently fit the quadratic without needing
the raw SDD data — a low-cost reproducibility win the authors could add.

**Blocker #4 (code, minor).** The official MGM repo's
`MicrodosimetricGammaModel.gamma_func` calls
`scipy.stats.gamma(a, b).pdf(x)`, which silently uses `b` as the SciPy
location parameter rather than as the paper's rate parameter. Anyone
re-using the public code to compute "the Gamma distribution from the
paper" will quietly get a different PDF than the paper's stated formula.
A two-character fix (`scipy.stats.gamma(a, scale=1/b).pdf(x)`) would
restore alignment with the paper text. (Or alternatively, the paper
text could be amended to state the actual parameterization.)

---

## Files produced

```
report/REPORT.md                                  (this file)
code/replicate_mgm.py                             (CPU-only, ~10s runtime)
source/paper.pdf                                  (original)
source/author_mgm.py                              (verbatim repo src/mgm.py)
source/author_README.md                           (verbatim repo README.md)
source/script_monoenergetic.py                    (verbatim repo example)
source/xray_microdosimetry_1um.phsp               (verbatim repo data file)
ocr/raw_layout.txt                                (pdftotext -layout)
evidence/fig2_damage_vs_yF.csv                    (400-row dense curves)
evidence/fig3_gamma_parameters_vs_yF.csv          (400-row α, β vs yF)
evidence/fig3_summary_per_beam.csv                (5-MeV p / 4-MeV α summary)
evidence/xray_complexity_distribution.csv         (X-ray pipeline output)
evidence/gamma_form_audit.csv                     (21-row Gamma form comparison)
evidence/replication_summary.json                 (machine-readable summary)
figures/fig2_damage_vs_yF.png                     (3-panel Fig 2 reproduction)
figures/fig3_complexity_and_gamma_params.png      (4-panel Fig 3 reproduction)
figures/xray_complexity_distribution.png          (X-ray bar chart)
```

To re-run: `cd code && python3 replicate_mgm.py` (≈10 s on any CPU,
numpy + scipy + matplotlib + pandas).
