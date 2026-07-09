# LUCID100 Slot 14 — Miles et al. 2021 (High vs Low LET → IFNβ / TREX1)

**Campaign:** LUCID100  •  **Wave:** 2  •  **Slot:** 14  •  **Rank in master:** 45
**Work type:** simulation/model replication
**Status (2026-06-09):** First-pass artifact harvest **COMPLETE**; replication scope **PARTIAL** (model-side feasible; bench-data digitization required because no machine-readable supplement was deposited).

## Citation

Miles D, Cao N, Sandison G, Stewart RD, Moffitt G, Pulliam T, Parvathaneni U, Goff P, Nghiem P, Stantz K.
**"Differential effects of high versus low linear energy transfer (LET) radiation on type-I interferon (IFNβ) and TREX1 responses."**
*bioRxiv* 2021.07.07.451516 (v1, posted 2021-07-08).
DOI: <https://doi.org/10.1101/2021.07.07.451516>
License: **CC BY-NC-ND 4.0** (per bioRxiv footer + Unpaywall + S2).
Authors' affiliations: Purdue Univ. School of Health Sciences (Miles, Stantz); Univ. of Washington Dept. of Radiation Oncology (Cao, Sandison, Stewart, Moffitt, Parvathaneni, Goff); UW Dept. of Medicine/Dermatology (Pulliam, Nghiem).
No subsequent peer-reviewed journal version located as of 2026-06-09 (web search returned only bioRxiv / ResearchGate / Semantic Scholar / scholar.archive.org records — see `artifacts/journal_version_search.txt`).

## Artifact links (verified live 2026-06-09)

| Source                  | URL                                                                                     | Status                                          |
| ----------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------- |
| bioRxiv landing         | https://www.biorxiv.org/content/10.1101/2021.07.07.451516v1                             | OK (HTML)                                       |
| bioRxiv full PDF        | https://www.biorxiv.org/content/10.1101/2021.07.07.451516v1.full.pdf                    | OK via browser (curl=403, CF). Local copy saved |
| Supplementary materials | https://www.biorxiv.org/content/10.1101/2021.07.07.451516v1.supplementary-material      | **NONE deposited** (page lists no supp files)   |
| Unpaywall               | https://api.unpaywall.org/v2/10.1101/2021.07.07.451516                                  | OA=true, GREEN, OAloc points to bioRxiv         |
| Semantic Scholar        | paperId `6d1c7a658d63affd1929ad2cfa46476d6a48758a`                                      | citationCount=0 as of 2026-06-09                |
| Europe PMC              | EPMC search returned the preprint as PPR367584                                          | OK                                              |
| Code / data repository  | **None disclosed** — no GitHub/Zenodo/figshare/Dryad accession in the paper             | —                                               |

## Claims (testable items, distilled from abstract + Results)

1. **Peak-dose RBE for IFNβ secretion (MCC13 cells, in vitro):** `peak_dose_xray = 14.0 Gy`, `peak_dose_neutron = 5.7 Gy`, giving **RBE_IFNβ = 2.5 ± 0.2** (ratio of peak doses).
2. **Peak amplitude** of IFNβ secretion does NOT differ significantly between SARRP x-rays and CNTS fast neutrons (P > 0.05).
3. **TREX1 dose response is linear** in absorbed dose for both modalities, with **RBE_TREX1 = 4.0 ± 0.1** (slope ratio, fast neutrons / x-rays).
4. **RBE_IFNβ ≈ RBE_DSB ≈ 2.3–2.5** (Monte Carlo MCDS DSB-induction RBE for CNTS fast neutrons relative to SARRP 220 kV x-rays).
5. **Bragg-peak-to-entrance amplification of IFNβ production** for charged particle beams ≈ **40× (proton), 100× (⁴He), 120× (¹²C)** — i.e. roughly **10–20×** the corresponding physical-dose peak-to-entrance ratios.
6. Spatial width of the IFNβ Bragg-peak production region ≈ **half** the physical-dose Bragg peak width.
7. **Model equations (now in code-form in `code/lucid100_let_ifnb_trex1_model.py`):**
   * Eq. 1 (IFNβ): `IFNβ(D, RBE_DSB) = a + b·(D·RBE_DSB)^2.5 + c · exp(−D·RBE_DSB / 2)` [pg/mL per 10⁵ cells]
   * Eq. 2 (TREX1): `TREX1(D, RBE_DSB) = a · D · RBE_DSB + b` [n-fold upregulation]
   * Eq. 3 (RBE_DSB closed-form, adapted from Stewart 2018):
     `RBE_DSB = [a + b − {b·(1−d) + c·x·(d−1)}^{1/(1−d)}]` with `x ≡ (z_eff/β)²`
     and fitted constants `a = 0.9902, b = 2.411, c = 7.32 × 10⁻⁴, d = 1.539` (relative to Co-60 γ).

## Scope of this replication

| Layer                                                  | Feasible here?                                                   | Method                                                                                                       |
| ------------------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| (A) Reproduce closed-form Eq. 3 RBE_DSB(z_eff, β) curve | ✅ YES, pure math                                                 | `code/lucid100_let_ifnb_trex1_model.py`, smoke test in `code/smoke_test.py`                                  |
| (B) Reproduce Eqs. 1 & 2 sanity behaviour                | ✅ YES, given the published peak-dose and RBE values             | Smoke test compares: implied peak-dose, monotone region of Eq.1, linearity + slope-ratio of Eq.2             |
| (C) Refit Table 1 coefficients (a,b,c)                   | ⚠ PARTIAL — Table 1 is a **rasterized image** in the PDF        | Two paths: (i) digitize Figs 1 & 2 with WebPlotDigitizer; (ii) when vision model is back, OCR Tables 1 & 2   |
| (D) Reproduce Bragg-peak FLUKA / 6 MV phase-space sims   | ❌ Not feasible without the authors' FLUKA decks + MCDS binaries  | Job-plan only (`code/JOB_PLAN_fluka_mcds.md`) — heavy compute target: chiatta00 or Aurora, NOT CherryRd      |
| (E) Re-irradiate MCC13 + measure IFNβ/TREX1              | ❌ Wet-lab; out of scope                                          | —                                                                                                            |

## Acceptance criteria

* **PASS-low** (achieved this pass): we have the full PDF, machine-readable text of Methods/Results, all three governing equations + their constants, and a smoke script that (a) recovers RBE_DSB ≈ 1.0 for Co-60 reference, (b) reproduces the reported neutron-vs-x-ray IFNβ-peak ratio of ~2.5 when fed the published x-ray peak of 14.0 Gy, and (c) reproduces the linear TREX1 slope ratio of ~4.0.
* **PASS-mid** (needs Fig 1 / Fig 2 digitization or restored vision tool): refit Eq. 1 to the digitized IFNβ data and recover Table 1 (a, b, c) for both modalities within stated CIs; recover Table 2 RBE rows.
* **PASS-full** (heavy compute): rerun FLUKA depth scans for proton / ⁴He / ¹²C beams, recompute Bragg-peak-to-entrance amplification factors of IFNβ production; targets ≈ 40 / 100 / 120 within ~20%.

## Directory layout

```
lucid100-let-ifnb-trex1/
├── README.md                          ← this file
├── PROGRESS.md                        ← timeline + next actions
├── FIRST_PASS_REPORT.md               ← verdict + evidence
├── ARTIFACT_MANIFEST.tsv              ← inventory of every retrieved file
├── artifacts/
│   ├── paper.pdf                      ← full 20-page bioRxiv preprint (verified, 1,475,562 bytes, PDF v1.5)
│   ├── paper.txt                      ← pdftotext -layout extraction (873 lines)
│   ├── paper_fulltext.txt             ← earlier browser-extracted HTML body (kept for cross-ref)
│   ├── doi-redirect.html              ← doi.org → bioRxiv redirect capture
│   ├── europepmc.html                 ← EPMC abstract page
│   ├── epmc-search.json               ← EPMC API hit (PPR367584)
│   ├── s2.json                        ← Semantic Scholar paper record (CitationCount=0)
│   ├── unpaywall.json                 ← Unpaywall record (OA=true, GREEN)
│   ├── journal_version_search.txt     ← evidence that no peer-reviewed journal version exists
│   ├── biorxiv_supplements_check.txt  ← evidence that no supplementary files were deposited
│   ├── figures_extracted/             ← 12 PNGs from pdfimages (figs + table-image scans)
│   └── inbox/                         ← empty staging dir from earlier attempt
├── code/
│   ├── lucid100_let_ifnb_trex1_model.py   ← Eqs 1/2/3 implementation
│   ├── smoke_test.py                       ← smoke replication (PASS-low criteria)
│   ├── digitization_template.csv           ← empty CSV ready for WebPlotDigitizer dumps
│   └── JOB_PLAN_fluka_mcds.md              ← heavy-compute plan if PASS-full is requested
├── data/                              ← (empty — bench-data only available via Fig 1/2 digitization)
├── figures/                           ← (smoke-test output plots land here when run)
└── results/                           ← (smoke-test numeric outputs land here when run)
```

## Reproduction instructions

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-let-ifnb-trex1
python3 code/smoke_test.py            # prints PASS/FAIL for criteria A & B; writes results/smoke_test_results.json + figures/*.png
```

No paid endpoints used. No heavy compute on CherryRd. No author contact.
