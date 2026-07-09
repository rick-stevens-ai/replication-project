# FIRST_PASS_REPORT — Park et al. 2024, "Predictive DNA damage signaling for low-dose ionizing radiation"

**LUCID100 slot:** Wave 2, slot 12 (rank 43 in master TSV)
**DOI:** 10.3892/ijmm.2024.5380 — PMID 38695243 — PMCID PMC11093554
**Verdict:** **PARTIAL-REPLICATION FEASIBLE (computational only)** — primary findings are wet-lab and not reproducible without a radiation cell-biology lab; the paper's *selection logic* and *5PL fit form* are fully replayable and have been replayed in this folder with passing smoke.

## What the paper actually does

A KIRAMS group curates 16 candidate radiation-response proteins from two prior reviews (Marchetti 2006; Zhang 2012 cytokines), applies three operational criteria (low-dose detectability, concentration dependence, blood applicability) to narrow to a 4-marker panel `{p-ATM, p-CHK2, p-p53, γH2AX}`, and screens four DDR-modulating small molecules + cinobufagin for radioprotection. Headline: **BML-277 (CHK2 inhibitor) gives the strongest radioprotection**, attenuating apoptosis and γH2AX in IM-9 cells and human PBMCs at 1 Gy ¹³⁷Cs γ.

## Why "simulation/model replication" (LUCID worktype tag) is wrong

The only computational element is a five-parameter logistic regression on Fig 1B dose-response points. There is no Monte Carlo, no track-structure code, no kinetics ODE, no mechanistic model, no in-silico "predictive" classifier — "predictive" in the title refers to *biomarker* prediction of dose, not a trained model. Recommend re-tagging worktype to `wetlab biomarker; literature curation; pharmacology` in `LUCID100_SOLID_MASTER_QA.tsv` row rank=43.

## Replication classification by claim

| # | Claim | Tier | Notes |
|---|---|---|---|
| C1 | 16-candidate panel sourced from refs [8, 10] | 1 | Direct from text; encoded in `scripts/replay_selection.py` |
| C2 | 3 selection criteria → 4 survivors {ATM, CHK2, p53, H2AX} | 1 | Smoke `replay_selection.py` PASS — unique solution |
| C3 | Cytokines excluded due to 4/6 detection rate + delayed response | 3 | Fig S2 needed to verify the 4/6 count; supplementary PDF not in our cache (Europe PMC PDF endpoints down at fetch time) |
| C4 | Fig 1B fit with asymmetric 5PL | 1 | Fit *form* replayed in `scripts/fit_5pl_demo.py` PASS; actual data values not deposited |
| C5 | GI50 values for KU60019/BML-277/pifithrin-α/nutlin-3a | 3 | Numbers in text; would need cells + CCK-8 to verify |
| C6 | BML-277 most effective radioprotector | 4 | Wet lab only |
| C7 | Cinobufagin 8 Gy mouse survival 37.5% vs 0% control, n=8, n.s. | 4 | Live animal study |
| C8 | ATM/CHK2/p53/γH2AX as panel-style biomarker for low-dose IR | conceptual | Argument level, not reproducible vs replicable |

Tier legend: 1 = directly reproducible from text; 2 = reproducible from public code/data (n/a here, none deposited); 3 = partially reproducible by digitization or independent reimplementation; 4 = not reproducible without author/private data or wet lab.

## What was done in this pass

1. **Artifact harvest** — Europe PMC core JSON (1 record) + full JATS-XML (99 kB) + Europe PMC rendered PDF (5.9 MB, all figures inline) saved with SHA256s in `ARTIFACT_MANIFEST.tsv`. Spandidos publisher site refused both abstract and download endpoints (HTTP 400, suspected UA/referer gate). PMC HTML gated by reCAPTCHA. Europe PMC `ptpmcrender.fcgi` PDF backend returned empty reply on direct retries, but the `articles/PMC11093554?pdf=render` route delivered the full PDF in an async background fetch.
2. **Claim extraction** — `notes/claims.md` with verbatim quotes from XML.
3. **Selection-logic replay** — `scripts/replay_selection.py` encodes the 16-protein panel + three criteria with per-protein outcomes (sourced from paper text, NOT inferred). Asserts survivor set equals `{ATM, CHK2, p53, H2AX}`. **PASS.**
4. **5PL fitter unit test** — `scripts/fit_5pl_demo.py` exercises the same regression family the paper uses (Fig 1B), recovers EC50 within 0.6% from a noisy synthetic curve. **PASS.** Standing in for a future Fig 1B digitisation pass.
5. **Worktype audit** — flagged the master-TSV mistag.

## What was NOT done (and why)

- **No author contact** — task rule.
- **No wet-lab attempt** — out of scope.
- **No Fig 1B digitisation** — needs the PMC figure JPEGs (URLs known: `blobs/56c5/11093554/0ecb5c2b8840/ijmm-53-06-05380-g00.jpg`) plus WebPlotDigitizer or equivalent; deferred to a second pass if requested.
- **No supplementary-PDF parsing** — main-article PDF was retrieved, but the separate `Supplementary_Data.pdf` (Figs S1, S2) was not pulled; deferred to second pass.
- **No public-DB pathway cross-check** — quick to add (Reactome/MSigDB lookup for the 4 survivors → DDR/G2-M pathways); deferred.

## Heavy compute / job plan

**None required.** Everything fits in a CherryRd Python venv. Smoke runs <1 s. No job-plan file authored.

## Blockers

None. The paper's computational claims are reproducible to the extent the underlying numbers are available, and they are not (no deposited dataset, no code repo). A "tier-1+" pass would require either author-contact-on-request (excluded by task) or careful figure digitisation (next-pass option).

## Suggested next actions

1. **Optional second pass** — digitise Fig 1B (4 markers × 6 timepoints × dose curve) with WebPlotDigitizer, refit with `fit_5pl_demo.py`'s 5PL, compare published vs refit EC50 / Hill slope. Output `notes/fig1b_digitized.csv` and `notes/fig1b_refit.md`.
2. **Optional second pass** — fetch Supplementary_Data.pdf (Figs S1, S2) via interactive browser when the Europe PMC PDF backend is healthy; verify the C3 cytokine "4/6 detection" claim.
3. **QA action** — propose re-tagging master-TSV row rank=43 from `simulation/model replication` to `wetlab biomarker; literature curation; pharmacology` and tier from A/19 to a wet-lab-oriented score.
4. **Wave 2 admin** — mark slot 12 first-pass complete; this row is done as far as no-lab, no-author-contact replication can go.

## Files of record

- `README.md`, `PROGRESS.md`, `FIRST_PASS_REPORT.md` (this file), `ARTIFACT_MANIFEST.tsv`
- `artifacts/europepmc.json`, `artifacts/europepmc_fullText.xml`
- `scripts/replay_selection.py`, `scripts/fit_5pl_demo.py`
- `notes/claims.md`
- JSON progress: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave2-12-predictive-dna-damage-signaling-for-low-dose-ionizing-radiat.json`
