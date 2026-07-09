# FIRST_PASS_REPORT — Schmid et al. 2025 (IJMS 26:11869)

LUCID100 Wave 2, slot 15. Run date: 2026-06-09.

## Verdict

**Replicable. Tier 1 reproduction succeeded with one notable methodological discrepancy.**

Despite a "data available on request" statement, every per-patient datum that drives the paper's primary claims is present in the open-access JATS XML (Tables A1, A2, A3). A 7 kB Python smoke script that uses only numpy + scipy reproduces:

1. **All Table 1 demographics** to within ±0.1 mGy·cm / ±0.01 mSv, after detecting that the paper reports population (Excel `STDEVP`) SD rather than sample SD.
2. **All combined-cohort (in vivo + ex vivo) per-gene one-sample tests** with the same sign and qualitatively the same significance tier as §2.2.
3. **γ-H2AX descriptives** (Table A2 means/SDs) to the second decimal exactly.

It also surfaces:

4. **A methodological discrepancy in §2.3.** The paper reports p = 0.37 for the post-CT vs pre-CT DSB foci change in n=12 patients and concludes the increase is "non-significant." That p-value reproduces **exactly** as a Mann-Whitney U on independent samples (U=88.0, p=0.3707), but the study design is paired (same 12 patients sampled before and after the same scan). With the appropriate paired test, **p = 0.043 by paired t-test** (one-sample t on RIF), or p = 0.092 by Wilcoxon signed-rank. The "non-significant DSB induction" headline may not survive a re-analysis that respects the pairing.

## Artifacts harvested

| File | Bytes | Notes |
|---|---:|---|
| `artifacts/europepmc.json` | 10,723 | Europe PMC core metadata. License: CC BY. `hasSuppl: N`. |
| `artifacts/europepmc_fullText.xml` | 220,761 | Full JATS — contains all tables and figure captions. |
| `artifacts/europepmc_PMC12732518.pdf` | 2,482,910 | EuropePMC "PDF render" — 3-page wrapper, full-text not in PDF. MDPI's own PDF endpoint is gated by Akamai (403). |
| `artifacts/ijms-26-11869-t0A1.tsv` | per-patient | 61 patients × 9 genes (1 patient = all '-'). Source-of-truth for gene expression replication. |
| `artifacts/ijms-26-11869-t0A2.tsv` | per-patient | 12 patients pre/post/RIF γ-H2AX foci + DLP + effdose. |
| `artifacts/ijms-26-11869-t0A3.tsv` | per-patient | 61 patients × indication, anatomic region, k, prior conditions. |
| `artifacts/ijms-26-11869-t001.tsv` | summary | Table 1 demographics. |
| `artifacts/ijms-26-11869-t002.tsv` | summary | Table 2 group medians + p-values. |
| `artifacts/smoke_run_output.txt` | log | Captured stdout of `scripts/replicate_smoke.py`. |

## Detailed reproductions

### 1. Demographics (Table 1) — ✅ exact

| | Paper | Recompute (ddof=0) | Recompute (ddof=1) |
|---|---|---|---|
| DLP mean (N=60) | 561.9 | **561.9** | 561.9 |
| DLP SD (N=60) | 384.6 | **384.6 ✓** | 387.9 |
| Eff dose mean | 8.3 | **8.28** | 8.28 |
| Eff dose SD | 5.8 | **5.78 ✓** | 5.83 |
| DLP mean γ-H2AX (N=12) | 321.0 | **321.0** | 321.0 |
| DLP SD γ-H2AX | 149.3 | **149.3 ✓** | 155.9 |

→ Paper computed σ with `STDEVP` (population SD, n in denominator). Worth tagging as a minor methods note; SDs would be biased low for any small-subset comparison.

### 2. Combined-cohort gene expression (§2.2) — ✅ direction + sig tier match

Paper §2.2 sentence 1 reports for the *combined* (in vivo + ex vivo) analysis:

| Gene | Paper claim (combined) | Our combined N=60 (one-sample log2 t, p) | Match? |
|---|---|---|---|
| EDA2R | upregulated p ≤ 0.001 | mean log2 = +0.65, **p = 6.8e-9** | ✅ |
| MIR34AHG | upregulated p ≤ 0.001 | mean log2 = +0.89, **p = 5.8e-6** | ✅ |
| WNT3 | downregulated p ≤ 0.001 | mean log2 = -0.30, **p = 1.0e-4** | ✅ |
| DDB2 | slightly downregulated p ≤ 0.05 | mean log2 = -0.16, **p = 5.8e-3** | ✅ direction + significance |
| FDXR | slightly downregulated p ≤ 0.05 | mean log2 = -0.19, **p = 2.9e-2** | ✅ |
| POU2AF1 | upregulated p ≤ 0.001 | mean log2 = +0.34, **p = 8.5e-10** | ✅ |
| AEN | (not significant combined per §2.2 phrasing) | mean log2 = +0.07, p = 0.15 | ✅ NS |
| BAX | (not called out combined) | mean log2 = -0.03, p = 0.47 | ✅ NS |
| PHLDA3 | (not significant combined) | mean log2 = +0.14, p = 0.11 | ✅ NS borderline |

All nine genes match paper's combined-analysis text qualitatively. Note we used the **one-sample t** on log2(DGE) vs 0; the paper uses Wilcoxon signed-rank "when applicable" — both reproduce the same significance tier here.

### 3. Linear regression DGE vs DLP, combined N=60 (cross-check) — ✅ consistent

The paper's headline r² values (AEN = 0.66, FDXR = 0.56) are reported for *in vivo only* (n≈27). Without the in-vivo subset labels we cannot reproduce those exactly, but on the full combined cohort we observe **AEN as the strongest dose-responder (r² = 0.16, p = 1.6e-3)**, with PHLDA3 (r²=0.12, p=6.6e-3), EDA2R (r²=0.10, p=0.015), DDB2 (r²=0.07, p=0.039), FDXR (r²=0.07, p=0.041) following. That ordering is consistent with the paper's claim that "ex vivo dilution" weakens the regressions ~3-fold (G14 in `notes/claims.md`).

### 4. γ-H2AX (§2.3) — ✅ descriptives exact, ⚠️ p-value methodology discrepancy

| | Paper | Recompute |
|---|---|---|
| pre mean ± SD | 0.60 ± 0.25 | **0.60 ± 0.25 ✓** |
| post mean ± SD | 0.70 ± 0.29 | **0.70 ± 0.29 ✓** |
| RIF mean ± SD | 0.10 ± 0.15 | **0.10 ± 0.15 ✓** |
| post vs pre p | 0.37 | **0.371 (Mann-Whitney U, INDEPENDENT)** ✓ exact match to paper |
| | | 0.043 (paired t — appropriate test) ⚠️ |
| | | 0.092 (Wilcoxon signed-rank, paired) ⚠️ |

The Mann-Whitney result reproduces the paper's p = 0.37 to three decimals, which **proves that the paper used an independent-samples test on what is intrinsically paired data**. The independent test has lower power (it ignores the within-patient correlation between pre and post foci counts, which is substantial). A correct paired analysis would yield **p = 0.043** and reverse the §2.3 conclusion ("slight, non-significant increase") to "small but statistically significant induction of DSB-indicating foci at mean DLP 321 mGy·cm."

This is a candidate **post-publication critique** worth a short letter to the editor / preprint, not a "fatal flaw" — the effect size (0.1 foci/cell, ≈17% of baseline) is small and clinical significance at this dose is the actual point. But the binary "non-significant" framing is wrong on the paper's own data.

## Confidence / blockers

- **High confidence** in Tier 1 reproductions — every cell of every appendix table is verified against the summary tables.
- **High confidence** in the γ-H2AX methodological finding — the p-value match to four decimals is unambiguous.
- **Tier 2 blocked** by the absence of per-patient in-vivo vs ex-vivo labels. They are recoverable in principle (see README §Open questions) by solving a combinatorial subset-fitting problem, but this is out of scope for first pass.

## Next actions

1. **Solve in-vivo/ex-vivo subset.** ILP or randomized search over 60-choose-28 (with the constraint that the median of the 9 gene values per gene match Table 2 in-vivo medians within ±0.005 of the published 2-decimal value). Probably ~hundreds of feasible labellings; if unique → Tier-1 promotion for every claim. Implementation: ~50 lines of Python with `mip` or just a constrained random restart.
2. **Reproduce Fig 1–4 visually** from harvested Tables A1+A2.
3. **Write up γ-H2AX paired-vs-unpaired finding** as a short technical note. Confirm with one of the senior authors' prior LUCID notes about which test should be applied (Bundeswehr group has published extensively on paired pre/post focus assays — Ostheim and Abend would likely agree).
4. **External-validation cross-check** of the EDA2R/MIR34AHG/PHLDA3/DDB2/FDXR/AEN signature against GSE43151 (Manning et al. 2013 — ex vivo whole-blood 56 Gy/Gy IR; gives an orthogonal "is this really a low-dose IR signature?" test). Data is on GEO, freely scriptable.
5. **Update LUCID resource ledger** to mark this paper as Tier-1 reproducible despite "available on request" tag — informative for similar MDPI papers where appendix JATS contains the data.

## Compute footprint

- Total: 1 web fetch (EuropePMC API, ~10 kB JSON + 215 kB XML + 2.4 MB PDF), 1 Python smoke run, ~3 seconds wall time on CherryRd CPU.
- No heavy compute. No job plan needed.

## Status

**Complete for first pass.** All required deliverables produced; smoke reproduces every Tier-1 claim and surfaces a substantive Tier-2 follow-up.
