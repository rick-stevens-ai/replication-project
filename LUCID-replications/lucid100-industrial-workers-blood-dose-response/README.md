# LUCID Replication — Guo et al. *Dose-Response* 2022 (industrial irradiation workers, blood parameters)

**Paper.** Guo J-J, Liu N, Ma Z, Gong Z-J, Liang Y-L, Cheng Q, Zhong X-G, Yao Z-J.
*Dose-Response Effects of Low-Dose Ionizing Radiation on Blood Parameters in
Industrial Irradiation Workers.* **Dose-Response** 20(2), 2022.
DOI [10.1177/15593258221105695](https://doi.org/10.1177/15593258221105695).
PMID 35693871 · PMCID PMC9174562 · Open Access (CC-BY-NC 4.0).

**LUCID100 slot.** Wave 2, Tier A, rank 48, max-rate backfill slot 17.

**Verdict.** PARTIAL — tables internally consistent; approximate refit recovers all 9 GLM dose-response betas within 2 published SE.

**QA retag recommendation.** Master TSV labels this paper as *“simulation/model replication.”* That is **incorrect**. The paper is a **prospective epidemiological cohort study with GLM + restricted-cubic-spline regression** of blood-parameter changes against cumulative dose in 705 industrial irradiation workers. There is **no simulation, no Monte Carlo, no biophysical model**. Correct worktype: **`statistical reanalysis / cohort regression replication`**. See `REPORT.md` for details.

## Files

| File | Purpose |
|---|---|
| `REPORT.md` | Full first-pass report: target, verdict, methods, agreement scores |
| `PROGRESS.md` | Chronological log of this replication run |
| `paper.xml` | EuropePMC JATS full text (source of truth used here) |
| `paper.pdf` | EuropePMC PDF render (1-page cover; XML is canonical) |
| `paper.txt` | Plain-text/Markdown rendering of `paper.xml` incl. all 3 tables |
| `MANIFEST.json` | Artifact manifest with paths, sizes, sha256, provenance |
| `code/replicate_lucid.py` | One-script replication (Tables 2 & 3 → re-fit GLM) |
| `results/table3_internal_consistency.csv` | Recomputed Z, P, CI vs printed |
| `results/table3_approx_refit_summary.csv` | Simulated-refit β vs published β |
| `results/table3_approx_refit_bootstrap.csv` | 400-replicate β distribution |
| `results/summary.json` | Machine-readable result summary |
| `figures/beta_published_vs_simulated.png` | Forest plot: published vs simulated β |

## Re-run

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-industrial-workers-blood-dose-response/
python3 code/replicate_lucid.py
```

Requires Python 3.9+, `numpy`, `scipy`, `pandas`, `statsmodels`, `matplotlib`.
Runs in ~10 s on CherryRd. No GPU. No external network needed (paper.xml is cached).

## TL;DR

- Paper reports a GLM β for dose-group on three blood parameters (RBC, PLT, HB)
  using lowest dose-group (0.101–1.417 mSv) as reference, plus restricted-cubic-spline
  curves with 5 knots.
- **Internal consistency:** every printed (β, SE, Z, P, 95% CI) row in Table 3
  is mutually consistent to within rounding (|ΔZ| ≤ 0.04, |ΔCI| ≤ 0.03).
- **Approximate refit:** simulating individual changes from Table 2 medians
  + IQR (Normal approximation) and refitting a GLM with the same dose-group
  contrasts recovers all 9 published β values within 2·SE_published (mean
  |z| = 0.59, worst |z| = 1.19). Signs and rank ordering match exactly.
- **Cannot replicate without raw data:** the restricted-cubic-spline curves in
  Figure 1 and the spline inflection points (RBC at 2.000/3.000 mSv, HB at
  2.904 mSv) require individual-level dose & outcome values not deposited.

## What this does NOT replicate

- The restricted-cubic-spline curves and inflection points in Figure 1.
- Adjusted models conditioned on individual sex / age / length-of-service / smoking
  (Table 2 only gives marginals stratified by one factor at a time).
- Authors’ choice of knot locations (1st, 25th, 50th, 75th, 95th percentiles of
  cumulative dose) — would need the raw dose distribution.

These are honest gaps from absence of deposited individual data; documented in
`REPORT.md`. Author contact deliberately not pursued (per backfill rules).
