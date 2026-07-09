# PROGRESS — LUCID-100 slot 27 (Wave 3, rank 58)

Paper: Liew et al. 2021 IJROBP, DOI 10.1016/j.ijrobp.2020.12.048.

## Chronology

* **2026-06-09 13:39 CDT** — slot picked up. Created
  `lucid100-flash-oxygen-repair-mechanistic-model/` with standard subfolders.
* **2026-06-09 13:39 CDT** — read TSV row via python csv parser (raw `awk`
  missed unescaped quotes); confirmed (i) the paper is the dynamic-UNIVERSE
  FLASH paper by Liew et al. and (ii) the model abbreviation MODELX in the
  TSV abstract redacts "UNIVERSE".
* **2026-06-09 13:39 CDT** — scanned `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/`
  to check for duplication. Found `lucid-universe-repair-doserate-rbe`, which is
  a sibling but covers the **2022** IJMS paper (10.3390/ijms23116268), not the
  2021 IJROBP paper. No duplication; the 2022 folder is reusable as
  reference scaffolding.
* **2026-06-09 13:40 CDT** — paper-PDF fetch attempts:
    * `redjournal.org` (Elsevier) — HTTP 403.
    * `unpaywall.org` (`10.1016/j.ijrobp.2020.12.048`) — `is_oa=false`,
      `has_repository_copy=false`, no OA locations.
    * `osti.gov/biblio/23198562` — 200; HTML only; abstract recovered from
      `<meta name="description">`.
    * `inrepo02.dkfz.de/record/166683` — DKFZ "fast-challenge" SPA shell,
      no useful content via curl.
    * `mdpi.com` PDFs for Liew 2019 / 2020 — HTTP 403 (DDoS protection).
    * Europe PMC fullTextXML for PMC6929106 (Liew 2019) and PMC7278970
      (Liew 2020) — **200, ~130 KB and ~115 KB respectively**, both
      containing all equations from the Modeling Approach sections.
* **2026-06-09 13:40 CDT** — extracted Eqs. 1-7 (Liew 2019: giant-loop,
  HRF parametrization, repair-deficient extension) and Eqs. 1-10 (Liew 2020:
  same + DMSO indirect-action handling). Saved Crossref reference list
  (52 refs) and Semantic Scholar metadata to `artifacts/`.
* **2026-06-09 13:41 CDT** — wrote `code/flash_oxygen_smoke.py` (~290 LOC,
  self-contained, no cross-folder imports) implementing:
    * UNIVERSE giant-loop DSB Monte Carlo
    * HRF(O2) parametrization (Liew 2019 eq. 6, m = 2.94, K = 0.129 %)
    * ROD + reoxygenation ODE (literature defaults g_ROD = 0.42 mmHg/Gy,
      tau_reox = 5 s)
    * First-order exponential repair on iDSB and cDSB pools using DU145
      half-lives from Liew 2022 IJMS Table 1.
* **2026-06-09 13:41 CDT** — fixed typo (`0xLE2025` literal, replaced with
  paper publication-date seed `20210104`); `ast.parse` clean.
* **2026-06-09 13:42 CDT** — ran smoke. Wall clock 64.5 s on CherryRd CPU
  (single thread). Produced 20-row CSV + log-scale SF-vs-[O2] figure.
* **2026-06-09 13:43 CDT** — verified the qualitative FLASH-sparing direction
  reproduces at low initial O2 (CONV 0.0056 → FLASH 0.0275 at 20 Gy/0.5 %)
  and at 10 Gy/0.5 %. At ≥ 2 % O2 the smoke does not reproduce the FLASH
  effect because the literature-default ROD coefficient is too small to
  drop intracellular O2 into the sensitive HRF regime over a single pulse;
  this is the expected limitation of a parameter-free smoke and matches
  qualitative analyses in Petersson 2020 and the Pratx 2019 lineage.
* **2026-06-09 13:43 CDT** — wrote ARTIFACT_MANIFEST.md, README.md, this
  PROGRESS.md, FIRST_PASS_REPORT.md, and the progress JSON under
  `~/.openclaw/workspace/memory/subagent-progress/`.

## Blockers

* Closed-access paper + closed supplement + no released code → cannot do
  bit-exact reproduction. This is **structural**: the same blocker applies
  to every UNIVERSE paper from this group.
* No author contact attempted (per task constraint).
* No paid endpoints used (per task constraint).

## Compute / safety

* CherryRd local CPU, ~65 s wall, ~64 s user, ~120 MB RSS peak.
* No external POST traffic. Only GETs to crossref/unpaywall/europepmc/osti.
* No paywall scraping. No author contact.
