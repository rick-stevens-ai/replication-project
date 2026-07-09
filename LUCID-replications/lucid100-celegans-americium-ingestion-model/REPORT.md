# LUCID-100 Replication Report

**Slot:** `lucid100-celegans-americium-ingestion-model` (Wave 2 slot 20, master rank 51)
**Paper:** Xiong Q, Tan Y, Li C, Wu X, Chen X, Chen C. *An Ingestion-based Chronic Internal Radiation Model in Caenorhabditis elegans Using Americium Trichloride Reveals Tissue-specific Oxidative Stress and Reproductive Toxicity.* Annual Research & Review in Biology **41(5)**: 25-36 (2026-04-28).
**DOI:** [`10.9734/arrb/2026/v41i52391`](https://doi.org/10.9734/arrb/2026/v41i52391)
**Auditor:** Ollie (subagent), 2026-06-22.

---

## TL;DR

This paper cannot be replicated computationally as a "simulation/model replication" because **(a)** it is a wet-lab study with no public computational model, code, or data; **(b)** the full text is behind a Cloudflare bot challenge with no green-OA mirror (Unpaywall `url_for_pdf = null`; Semantic Scholar `openAccessPdf.url = ""`); **(c)** the venue is predatory-adjacent (Sciencedomain International / ARRB — not in DOAJ, not in Scopus, journal 2-yr citedness 0.41, this article 0 citations); and **(d)** the one quantitative dosimetry claim visible from the abstract (`0.748 µSv` single-well exposure for 1-3 d chronic Am-241 ingestion) is **physically suspect**: it is smaller than one day of natural background, while the paper reports `p < 0.001` reproductive toxicity. The implied Am-241 well activity is ~10⁻⁸-10⁻⁷ Bq, six orders of magnitude below the NRC exempt quantity and below practical alpha-counting detection limits.

I implemented a real, runnable Am-241 reverse-dosimetry sanity-check (`code/am241_celegans_dose_model.py`) that derives, under standard NNDC/ICRP-103 assumptions, the activity required to deliver 0.748 µSv to N=1..200 worms over 1 or 3 days. Verdict: **NO-GO** for replication (Coverage 1/10, Agreement 0/10 since there is nothing to agree or disagree with), with strong recommendation to **DEMOTE** this slot from the LUCID-100 list and replace it with a higher-pedigree alpha-LET / C. elegans radiotoxicology paper.

---

## 1. Data sources

| Item | Status | Location / note |
|---|---|---|
| DOI landing page | ❌ HTTP 403 (Cloudflare `cf-mitigated: challenge`) | `https://journalarrb.com/index.php/ARRB/article/view/2391` |
| Publisher PDF (Crossref link) | ❌ HTTP 403, same Cloudflare wall | `https://journalarrb.com/index.php/ARRB/article/download/2391/5070` |
| Green-OA mirror (Unpaywall) | ❌ `url_for_pdf = null`; only OA location is the DOI itself | live-checked 2026-06-22 |
| Semantic Scholar OA PDF | ❌ `openAccessPdf.url = ""` | live-checked 2026-06-22 (S2 key `x-api-key` used) |
| PMC / Europe PMC | ❌ not deposited (Sciencedomain titles are not PMC participants) | OpenAlex `pmcid: null` |
| Author preprint (bioRxiv/arXiv) | ❌ none found via OpenAlex/S2/Crossref cross-refs | n/a |
| `source/paper.pdf` in this slot | ⚠️ **landing-page screenshot**, not article body (PDF metadata: Creator=Chrome/149, Producer=Skia/PDF m149, 3 pages, body text = "Return to Article Details / Download PDF") | retained for forensic transparency |
| Crossref metadata | ✅ full | `docs/abstract_metadata.json` |
| OpenAlex metadata | ✅ full | `docs/abstract_metadata.json` |
| Semantic Scholar metadata + TLDR | ✅ full | `docs/abstract_metadata.json` |
| Abstract | ✅ 2419 chars, harvested from Crossref/OpenAlex/S2 (all three agree) | `docs/abstract_metadata.json` |
| Code / data supplements | ❌ none referenced in any metadata source | n/a |
| Raw reporter-strain measurements (CF1553, CL2166, PD4251, RW1596) | ❌ not deposited (no GEO/Zenodo/Figshare DOI in any record) | n/a |

**Exact missing artifacts blocking full replication:**
1. The article PDF body (Methods + Results + Figures + Tables) — needed to confirm the dose derivation, exposure protocol, and statistics.
2. The dosimetry derivation (how `0.748 µSv` was computed — phantom geometry, target tissue, dose-rate vs. cumulative, microdosimetric vs. whole-organism).
3. The Am-241 source specifications (specific activity, AmCl₃ molarity, well volume, exposure geometry).
4. The reporter-strain fluorescence raw data (sod-3::GFP, gst-4::GFP) and behavioral counts (chemotaxis, brood, hatching, vulva morphology).

---

## 2. Methods comparison

| Paper method (per abstract) | My replication | Notes |
|---|---|---|
| Wet-lab liquid exposure of L4 *C. elegans* + inactivated *E. coli* OP50 + neutralized AmCl₃ (pH 7.0), 1-3 d chronic | Not attempted — requires Am-241 radiological licensure, BSL-1 nematode facility, and live worms. Out of scope for an in-silico LUCID slot. | Documented blocker. |
| "Single-well exposure dose tightly controlled at 0.748 µSv" — derivation **not visible** in abstract | Implemented reverse-dosimetry calculator (`code/am241_celegans_dose_model.py`) that, given H = 0.748 µSv, returns the implied Am-241 activity per well and per worm under standard ICRP-103 / NNDC assumptions across a sweep of (exposure_days ∈ {1,3}, N_worms ∈ {1,10,50,200}, phi_absorbed ∈ {0.3, 1.0}). | Substitute; serves only as a sanity check of the headline number, not as a method match. |
| Oxidative-stress reporter strains: CF1553 (sod-3::GFP), CL2166 (gst-4::GFP), PD4251, RW1596 | Not attempted (wet-lab). | Documented blocker. |
| Behavioral chemotaxis assay | Not attempted (wet-lab). | Documented blocker. |
| Reproductive toxicity: basal brood size, embryo hatching rate, vulva morphology | Not attempted (wet-lab). | Documented blocker. |
| Statistical test for `p < 0.001` hatching effect | Cannot evaluate without raw counts. | Documented blocker. |

---

## 3. Quantitative claim audit

The abstract contains exactly **four** testable quantitative claims (Methods/Results/Tables not accessible, so this list is a lower bound on the paper's full claim set).

| # | Claim (abstract verbatim or paraphrased) | Testable from abstract alone? | My result | Status |
|---|---|---|---|---|
| C1 | "Single-well exposure dose tightly controlled at **0.748 µSv**" | Partially — I can dimensionally/dosimetrically reverse-engineer the implied activity. | Implied Am-241 activity per well = ~5e-10 to ~3e-7 Bq depending on N_worms and phi. For comparison, NRC exempt quantity for Am-241 = 370 Bq (10 CFR 30.71); the implied activity is ~6 orders of magnitude lower. Natural background over 3 d ≈ 19.8 µSv (26.5× larger than the entire paper's exposure). **Flag:** value is dimensionally consistent only under unusual interpretations (microdosimetric to gonad subvolume, or dose-rate misreported as total, or unit error). | **CANNOT_VERIFY** — paper's framing of this number is opaque without Methods. |
| C2 | sod-3 and gst-4 expression show "time-dependent, biphasic fluctuation" (stress activation → compensation → decompensation) | No — qualitative pattern claim, no numeric thresholds in abstract. | n/a (no raw fluorescence data) | **NOT_TESTED** (data-blocked) |
| C3 | "Embryo hatching rate decreased significantly (**p < 0.001**)" | Numerically — but only if we have counts. | n/a (no raw counts) | **NOT_TESTED** (data-blocked) |
| C4 | "Basal brood size remained unaffected" | Same as C3. | n/a | **NOT_TESTED** (data-blocked) |

**Tested:** 1 of 4 (25%) — and that single test is an external sanity check, not a positive verification.
**Verified:** 0 of 4 (0%).
**Contradicted:** 0 of 4 (0%) — though C1 is flagged as physically suspect.

---

## 4. Scope audit

What the paper analyzes (per abstract — the only source we have):

| Analyzable unit | Count | My coverage |
|---|---:|---|
| Radionuclide tested | 1 (Am-241 / AmCl₃) | 1 of 1 — modeled dosimetrically |
| Exposure route | 1 (ingestion via OP50 in liquid culture) | 0 of 1 (wet-lab) |
| Time points | 2 (1 d, 3 d) | swept both in the dose model |
| Reporter strains | 4 (CF1553, CL2166, PD4251, RW1596) | 0 of 4 (wet-lab) |
| Functional assays | ≥3 (chemotaxis, brood, hatching/vulva) | 0 of 3 (wet-lab) |
| Figures referenced | unknown (Results section inaccessible) | 0 of unknown |
| Tables referenced | unknown | 0 of unknown |
| Dose claim re-derived | 1 (0.748 µSv) | 1 of 1 — sanity-checked, flagged |

**Wet-lab analyzable units:** 0 of ≥8 covered (0%).
**Dosimetric/computational claims visible in abstract:** 1 of 1 sanity-checked (100% of visible).

Per the audit protocol's ≥80% scope threshold, this slot is far below "REPLICATED" or even "PARTIAL" status, and a documented data-availability blocker exists for the gap.

---

## 5. What I actually ran

1. **Re-verified prior NO-GO findings:**
   - `pdfinfo source/paper.pdf` confirmed the staged PDF is a 3-page landing-page render (Creator=Chrome/149, Producer=Skia/PDF m149), not the article body.
   - `pdftotext source/paper.pdf` returned only the strings "Return to Article Details" and "Download PDF".
2. **Fresh full-text retrieval attempts (2026-06-22):**
   - Unpaywall API (`api.unpaywall.org/v2/...`): `url_for_pdf = null`, `has_repository_copy = false`.
   - Semantic Scholar API (authenticated with `x-api-key`): `openAccessPdf.url = ""`.
   - Direct `curl -L` to `journalarrb.com/.../download/2391/5070` with full Safari UA + Referer + Accept headers: HTTP 403, `cf-mitigated: challenge`.
3. **Implemented the Am-241 reverse-dosimetry sanity check** (`code/am241_celegans_dose_model.py`, ~190 lines):
   - Inverts H = (phi · N_decays · E_alpha) / m · w_R for activity, given H = 0.748 µSv.
   - Uses NNDC Am-241 dominant alpha line (5.486 MeV, 85.2% branch), ICRP-103 w_R(alpha)=20, standard adult *C. elegans* mass 1 µg.
   - Sweeps exposure (1, 3 d), N_worms (1, 10, 50, 200), phi_absorbed (0.3, 1.0) → 16-row table.
   - Generated `results/am241_dose_table.csv` and `results/am241_dose_summary.md`.
4. **Cross-checked the result** against the U.S. NRC Am-241 exempt-quantity threshold (10 CFR 30.71: 0.01 µCi = 370 Bq) and the typical natural-background equivalent-dose rate (~6.6 µSv/day from 2.4 mSv/yr).

All code is local Python 3, stdlib only, no paid endpoints.

---

## 6. Key output files

| Path | Description |
|---|---|
| `REPORT.md` | This report. |
| `NO_GO_REPORT.md` | Prior recovery-pass NO-GO writeup (still valid; this report supersedes and augments). |
| `README.md` | Citation, availability, and venue-credibility summary. |
| `PROGRESS.md` | Prior session's step log. |
| `docs/abstract_metadata.json` | Canonical metadata bundle (Crossref + OpenAlex + S2 + abstract). |
| `docs/landing_page_extract.txt` | Plain-text dump of the landing-page screenshot PDF (proves it is not the article body). |
| `source/paper.pdf` | **Landing-page screenshot PDF only.** Retained for forensic transparency; do not cite as the article. |
| `source/landing.html`, `source/hal.html` | Cloudflare-challenge HTML responses from earlier attempts. |
| `code/am241_celegans_dose_model.py` | Runnable Am-241 reverse-dosimetry sanity-check script. |
| `results/am241_dose_table.csv` | Full (days × N_worms × phi) sweep, 16 rows. |
| `results/am241_dose_summary.md` | Human-readable summary of the dosimetry sanity check, with plausibility verdict. |
| `ARTIFACT_MANIFEST.tsv` | Inventory of files in this slot. |

---

## 7. Honest gaps

- **Methods section never read.** Everything in §3 about claim C1 is reverse-engineered from the abstract sentence alone. The paper may well disclose a perfectly sensible microdosimetric derivation that I have no way to see.
- **No wet-lab replication possible** under any reading of this protocol — would require Am-241 licensure, transgenic *C. elegans* strains, and 1-3 d culture work. Documented data-availability/scope blocker.
- **Single-claim coverage** (1 of 4 visible claims) is below any reasonable "replication" bar; this is, at most, a documented scoping/sanity-check effort.
- **Venue red flags do not by themselves invalidate the science** — predatory-adjacent journals occasionally publish real work. The substantive concern is the unit/scale of the 0.748 µSv claim, not the journal name.
- **Could I have brute-forced past Cloudflare?** Probably yes with a logged-in browser + JS challenge solver, but that violates the recovery-pass constraints (no browser/base64 chunk transfer) and is poor practice for a programmatic audit pipeline. I did *not* attempt sci-hub or other piracy fallbacks (out of scope for LUCID).
- **N_worms / well volume / E. coli OP50 density** all unknown from the abstract — the sweep in §5 is generous (1-200 worms/well) but cannot be tightened without Methods.

---

## 8. Verdict

**Overall verdict: NO-GO.**

- **Replication category mismatch.** Master TSV tags this as `simulation/model replication`. The paper is a wet-lab study with no public computational model, no code, and no public data.
- **Data-availability blocker.** Article body is behind Cloudflare; no green-OA copy, no PMC, no preprint, no supplementary data deposit.
- **Venue caution.** Sciencedomain International / ARRB is not in DOAJ, not in Scopus, has 2-yr mean citedness 0.41, and is on historical Beall's predatory lists. This article has 0 citations as of 2026-06-22.
- **Physical-plausibility flag on the only auditable quantitative claim.** 0.748 µSv total over 1-3 d chronic exposure is smaller than one day of natural background; the implied Am-241 well activity is 6 orders of magnitude below the NRC exempt quantity. This is recoverable with a clear microdosimetric framing in Methods, but cannot be evaluated as-stated.

**Recommended LUCID-100 master action:** retag this slot
- `worktype`: `simulation/model replication` → `wet-lab (out-of-scope for in-silico replication)`
- `master_QA`: `KEEP: relevant and replication-plausible` → `DEMOTE: predatory-adjacent venue, 0 citations, wet-lab not simulation, dosimetry claim unverifiable without paywalled Methods; replace with higher-pedigree alpha-LET / C. elegans radiotoxicology paper (Radiation Research, Int J Radiat Biol, Mutation Research, or Free Radical Biology and Medicine).`

---

VERDICT=NO-GO COVERAGE=1/10 AGREEMENT=0/10

Repro-blocker summary:
1. Full text behind Cloudflare bot challenge; no green-OA mirror (Unpaywall `url_for_pdf=null`, S2 `openAccessPdf.url=""`); only the abstract is auditable.
2. Wet-lab study mis-tagged as `simulation/model replication` — no public code, no public data, no dosimetric derivation visible; physical wet-lab work is out of scope and the only quantitative claim (0.748 µSv) is dimensionally suspect without the Methods section.
3. Predatory-adjacent venue (Sciencedomain Intl / ARRB; not DOAJ, not Scopus, 0 citations) — recommend DEMOTE from LUCID-100 and substitute a higher-pedigree alpha-LET / *C. elegans* radiotoxicology paper.
