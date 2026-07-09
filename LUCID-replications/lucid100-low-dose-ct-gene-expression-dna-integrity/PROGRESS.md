# PROGRESS — LUCID100 slot 15

Paper: Schmid et al. 2025 (IJMS 26:11869) — "Impact of Low-Dose CT Radiation on Gene Expression and DNA Integrity"
DOI: 10.3390/ijms262411869 · PMCID: PMC12732518

## Timeline (UTC)

- 2026-06-09 18:03 — Slot 15 launched by Wave 2 backfill scheduler.
- 2026-06-09 18:04 — Confirmed paper not yet started; created workspace folder `lucid100-low-dose-ct-gene-expression-dna-integrity/`.
- 2026-06-09 18:04 — Pulled EuropePMC core JSON + JATS full text + EuropePMC PDF render.
- 2026-06-09 18:04 — MDPI HTML/PDF endpoints returned Akamai 403; pivoted to JATS-only harvest. `hasSuppl: N` confirmed, but all numeric data is inline in appendix tables.
- 2026-06-09 18:05 — Extracted Tables A1 (per-patient gene expression), A2 (γ-H2AX foci), A3 (scan metadata), T1 (demographics), T2 (group medians) to TSV.
- 2026-06-09 18:05 — Catalogued claims in `notes/claims.md` (cohort, gene expression combined / in-vivo / ex-vivo / vs-comparison, dose response, DSB).
- 2026-06-09 18:06 — Wrote `scripts/replicate_smoke.py` for Tier-1 reproduction (demographics, combined-cohort GE, regression, γ-H2AX).
- 2026-06-09 18:06 — Smoke run #1: DLP SD mismatch surfaced → recognized that paper uses population SD (`STDEVP`); script updated.
- 2026-06-09 18:07 — Smoke run #2: γ-H2AX paired test gave p=0.043, paper reports p=0.37 → investigated → reproduced paper's p=0.37 *exactly* with Mann-Whitney U on independent samples (U=88.0, p=0.3707).
- 2026-06-09 18:08 — Smoke run #3 (final): all four sections PASS; methodological discrepancy surfaced and asserted in script.
- 2026-06-09 18:08 — Wrote `README.md`, `FIRST_PASS_REPORT.md`, `ARTIFACT_MANIFEST.tsv`.
- 2026-06-09 18:08 — Updated `~/.openclaw/workspace/memory/subagent-progress/lucid100-wave2-15-*.json` to status=complete.

## Final state

- README.md ✅
- PROGRESS.md ✅ (this file)
- FIRST_PASS_REPORT.md ✅
- ARTIFACT_MANIFEST.tsv ✅
- artifacts/ (9 files) ✅
- scripts/replicate_smoke.py ✅ (Tier-1 PASS)
- notes/claims.md ✅
- Heavy compute: none required
- Author contact: none made
- Paid endpoints: none used

## Verdict

**Tier-1 replicable with one substantive Tier-2 methodological finding (independent-samples test used on paired DSB data; correct paired test would flip the §2.3 conclusion from non-significant to p=0.043).**

## Tier-2 advance (2026-06-22)

- 2026-06-22 11:10 — Subagent picked up paper to advance to FINAL report.
- 2026-06-22 11:11 — Identified abstract/Table-2 inconsistency: abstract says n=28 in vivo / n=32 ex vivo; Table 2 says n=27 / n=33.
- 2026-06-22 11:12 — Wrote `scripts/infer_invivo_subset.py` (joint simulated annealing on Table 2 medians for both 27- and 28-patient splits).
- 2026-06-22 11:15 — SA ran 30 starts × 40K iter for each size (~4 min CPU). Best fit: n_in=28 (max median-error 0.020); 15 tied subsets (AMBIGUOUS).
- 2026-06-22 11:16 — Wrote `scripts/replicate_tier2.py`: 9-gene in-vivo + ex-vivo tests, in/ex Mann-Whitney comparison, in-vivo + ex-vivo dose-response OLS, FDXR ratio, DLP-stratified subgroup, paired DSB re-analysis, p53-target pathway test, dose-response and DSB figures.
- 2026-06-22 11:17 — Tier-2 results: G13 BAX r²=0.136/p=0.054 and EDA2R r²=0.127/p=0.063 reproduce to ~3 dp; G12 AEN r²=0.564 vs paper 0.66 and FDXR r²=0.466 vs 0.56 (subset-ambiguity gap); G15 EDA2R ex-vivo p=1.2e-4 reproduces; novel p53-target pathway score in-vivo p=1.7e-4 vs ex-vivo p=0.19.
- 2026-06-22 11:18 — Confirmed via full-text grep: paper has zero GEO/SRA/EGA/ArrayExpress accession; DAS "available on request" is the only data path.
- 2026-06-22 11:19 — Wrote `report/REPORT.md` with verdict PARTIAL / Coverage 8 / Agreement 8 / claim-by-claim table / 4 named reproducibility blockers (single most important: missing per-patient `Incubation` column in Table A1).

## Tier-2 verdict

**PARTIAL — Coverage 8/10, Agreement 8/10.** 22/28 claims fully agree, 4/28 partially (subset-label-dependent), 2/28 fail (DSB paired-test critique, misleading DAS). Single-column fix (`Incubation`) would close the r² gap; raw Ct CSV would enable full pipeline re-derivation.
