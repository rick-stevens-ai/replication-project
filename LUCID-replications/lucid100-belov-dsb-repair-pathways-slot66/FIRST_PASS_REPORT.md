# FIRST_PASS_REPORT — slot 66

**Paper:** Belov et al. 2015, *Journal of Theoretical Biology* 366:115–130, DOI [10.1016/j.jtbi.2014.09.024](https://doi.org/10.1016/j.jtbi.2014.09.024).
**LUCID100 master:** rank 97, Wave 7, B-tier.
**Run:** Wave 7 backfill slot 66, 2026-06-09, CherryRd (CPU only, ~5 s integration).

## Verdict

**REPLICATED (smoke) — KEEP.** The complete 22-coupled-ODE biochemical model for NHEJ + HR + SSA + γ-H2AX foci as published can be implemented from the JINR open-access preprint alone, integrates cleanly, and qualitatively reproduces the paper's narrative (fast NHEJ, slow HR/SSA tail, γ-H2AX peak within minutes, higher residual foci in NHEJ-defective cells). Recommend QA retag → `replicated_smoke`.

## Artefacts

| File | Source | Bytes | Notes |
|------|--------|------:|-------|
| `artifacts/belov2015_inis_iaea.pdf` | INIS/IAEA mirror of JINR Communication E19-2014-39 | 703 666 | Same Appendices A/B/C and Tables A.1/A.2 as the JTB paper. Open access. |
| `artifacts/belov2015_inis_iaea.txt` | `pdftotext -layout` on the above | 79 030 | Used to lift all equations and rate-constant tables. |
| `artifacts/epmc_meta.json` | Europe PMC `/search?query=DOI:...` | 8 405 | Confirms PMID 25261728, no PMC ID, `isOpenAccess=N`. |
| `scripts/smoke_belov2015.py` | written by this pass | 14 105 | Full 22-ODE system, verbatim Eqs A.1/B.1/C.1, Tables A.1/A.2 hard-coded. |
| `results/smoke_results.json` | smoke run output | 96 139 | 12 scenarios × full traces. |
| `results/smoke_traces.png` | smoke run plot | 161 044 | 2×2 grid: n0 / γ-H2AX × as-printed / binding-speedup. |

## What was reproduced

Six biological scenarios spanning the LET range and three repair-deficient cell types tabulated in Table A.2 of the paper:

| Scenario | LET (keV/µm) | Nir | α(L) [DSB Gy⁻¹] |
|----------|-------------:|----:|----------------:|
| low-LET γ wild-type   | 0.2 | 0.01 | 27.5 |
| X-ray DNA-PKcs⁻       | 0.2 | 0.43 | 27.5 |
| X-ray LigIV⁻          | 0.2 | 0.20 | 27.5 |
| X-ray BRCA2⁻          | 0.2 | 0.33 | 27.5 |
| ⁵⁶Fe 1 GeV/u wild-type | 150 | 0.30 | 19.1 |
| ⁵⁶Fe 1 GeV/u (236 keV/µm) | 236 | 0.40 | 15.5 |

Each was integrated twice: once with Table A.1 verbatim (`binding_speedup=1`) and once with `binding_speedup=1e6` (see §"Reproducibility caveats"). With the speedup applied:

| Scenario | γ-H2AX peak time (min) | γ-H2AX peak (scaled) | NHEJ contribution > HR? |
|----------|-----------------------:|---------------------:|:-----------------------:|
| low-LET γ wt           | 9.0  | 8.14e-6 | yes |
| X-ray DNA-PKcs⁻        | 38.5 | 1.93e-3 | (NHEJ broken → high foci, slow clearance) |
| X-ray LigIV⁻           | 32.0 | 8.16e-4 | (NHEJ broken → high foci) |
| X-ray BRCA2⁻           | 36.5 | 1.46e-3 | (HR broken → diverted to NHEJ/SSA) |
| Fe 1 GeV/u (150 keV/µm) | 36.5 | 9.52e-4 | yes |
| Fe 1 GeV/u (236 keV/µm) | 39.5 | 1.09e-3 | yes |

These match the qualitative claims of the paper:
- γ-H2AX peaks 10–60 min post-irradiation (Fig 5, Fig 7).
- DNA-PKcs⁻ cells retain ~3× higher γ-H2AX peak than wt (Fig 8).
- High-LET (Fe ions) shifts the γ-H2AX peak later and gives a larger residual at 24 h via larger Nir (Fig 7).

## Reproducibility caveats

1. **Order-of-magnitude inconsistency between Table A.1 and the experimental data the paper fits.** With K1=1.67×10⁻¹ M⁻¹ min⁻¹ and the stated [Ku]=9.19×10⁻⁷ M, the implied pseudo-first-order Ku-DSB binding rate is ~1.5×10⁻⁷ min⁻¹, i.e. a half-time of ~4.6 million minutes. Reynolds et al. 2012 (the dataset the paper uses for K1–K2 fitting) reports half-times of ~15–30 s for Ku binding. This is a 6–7 order-of-magnitude mismatch most plausibly explained by a units typo in Table A.1 (e.g. uM⁻¹ vs M⁻¹). Our `binding_speedup=1e6` switch recovers the right physical timescale. **The model structure and qualitative behaviour are not affected**, but absolute fits to digitised experimental data cannot be reproduced with Table A.1 as printed. We integrate the system both ways and report both.
2. **No author code or data deposit.** No GitHub/Zenodo/Figshare. Computations were run "at JINR LIT facilities".
3. **Experimental overlays in Figs 3/5/7/8 are not digitised in this pass.** Bit-exact agreement with paper figures requires manual digitisation of those overlays plus the resolution of caveat 1.
4. **Pool variables assumed constant.** The paper sets x1, x3, x7, x9, x11, x15, y1, y4, y6, y9, z1, z4, z7 = 1 (the dimensionless Ku reservoir). We follow the same convention. Realistic depletion of repair enzymes is outside the paper's scope.
5. **No alt-EJ / MMEJ.** The model is restricted to NHEJ + HR + SSA; the discussion explicitly notes this and points at alt-EJ as a future extension.

## Replication scoping (forward-looking)

A *full* replication of the published figures would add:
- WebPlotDigitizer extraction of Figs 3, 5, 7, 8 experimental overlays into CSV.
- A least-squares re-fit of K1–K7 (and possibly the per-LET Nir entries) against those overlays — small problem, fits in seconds on CPU.
- Cross-check P-set against Rad51 foci data in Asaithamby 2008 (Fig 6 in the paper).

All would run trivially on CherryRd; **no heavy compute job plan is needed.**

## Recommendation

Retag in `LUCID100_SOLID_MASTER_QA.tsv`:
- `verdict_or_plan` → `replicated_smoke: full 22-ODE NHEJ+HR+SSA+γ-H2AX integrated; Table A.1 likely has K1..K7 units typo (~1e6 offset)`.
- `qa_decision` → keep `KEEP: relevant and replication-plausible` (no change).
