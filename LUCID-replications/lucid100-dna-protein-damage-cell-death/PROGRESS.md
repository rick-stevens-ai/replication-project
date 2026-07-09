# PROGRESS — Shuryak & Brenner 2012 (LUCID100 slot 23)

## 2026-06-09 — first-pass artifact harvest + smoke replication

**Subagent:** LUCID100 Wave 3 backfill, slot 23.

### Harvest

- Tried `europepmc.org/articles/pmc3580191?pdf=render` → HTTP 302 → 500
  (`{"error":"Failed to retrieve PDF for pmcid: PMC3580191"}`).
- Tried NCBI PMC `pmc.ncbi.nlm.nih.gov/articles/PMC3580191/pdf/` → 200 but
  21 KB HTML reCAPTCHA challenge page.
- Tried PNAS direct (`https://www.pnas.org/doi/pdf/10.1073/pnas.1009312107`
  for source-data paper) → HTTP 403.
- ✅ Worked: **PMC OAI-PMH** `verb=GetRecord&metadataPrefix=pmc` for
  `oai:pubmedcentral.nih.gov:3580191` returned the full JATS XML
  (80 KB). Body extracted to `artifacts/paper.txt`.
- ✅ Worked: Unpaywall API (`oa_status: green`,
  `version: submittedVersion`). Saved to `artifacts/unpaywall.json`.
- Figure JPGs: every PMC/EuropePMC binary endpoint behind reCAPTCHA;
  abandoned. Figure **captions** and **parameter tables** were fully
  recovered from the JATS XML and are sufficient for replication scoping.

### Model extraction

- 10 sections / 5 equations / 5 figures / 2 tables / 24 references / 0
  supplementary-material elements (confirmed from JATS).
- Equations 1–5, parameter table (Table 1), and mechanism table
  (Table 2) all extracted verbatim into `paper.txt` / `MANIFEST.json`.
- Source dataset is Krisko & Radman 2010 (PNAS, PMC2922536). The
  PNAS paper presents raw `F(D)` / `S(D)` only as figure points (no
  tabular SI), so a future numeric replication will require
  WebPlotDigitizer on those figures.
- **Code search for the FORTRAN simulated-annealing fitter**:
  - GitHub user `igorshuryak`: does not exist.
  - GitHub repository search `shuryak deinococcus`: 0 hits.
  - GitHub code search `Shuryak Krisko Radman`: 0 hits.
  - No Zenodo / Figshare / OSF URL in paper body or references.
  - Verdict: authors' fitting code is **not publicly released**.

### Replication build

- Wrote `scripts/smoke_shuryak_2012.py` (pure Python 3, optional
  matplotlib): implements Eqs. 1–5 verbatim, hard-codes Table 1 best-fit
  parameters, and uses strain-specific approximate `F(D)` curves
  consistent with the paper's qualitative descriptions of Krisko &
  Radman Figs. 1 / 2.
- Smoke run completed in < 1 s on CherryRd CPU.
- Produced `results/summary.csv`, 10 per-strain CSVs, and two PNG
  survival figures.
- **Dominant-mechanism agreement with paper's Table 2: 10 / 10**
  (all five strains × γ + UV).
- Quantitative S(D_end) values are within a few orders of magnitude of
  the paper's headline ranges; tight numeric match requires plugging in
  digitized F(D) instead of the logistic placeholder.

### Outstanding work for a full replication

1. Digitize Krisko & Radman 2010 Fig. 1 (cell survival) and Fig. 2
   (carbonylation) with WebPlotDigitizer → CSV per strain × radiation.
2. Drop those CSVs into `scripts/smoke_shuryak_2012.py` (replace the
   `_logistic_F` callables) and re-run.
3. Add a SciPy least-squares (or random-restart SA) refit to verify the
   Table 1 best-fit parameters fall inside the published 95 % CIs.
4. Add Fig. 4 (Q₁ contour) and Fig. 5 (S vs P) plotters.
5. Optional: extend to extremophiles outside the original dataset
   (*Thermus thermophilus*, *Halobacterium salinarum*).

### Blockers

- PNAS PDF and NCBI PMC PDF both blocked from headless `curl` (403 /
  reCAPTCHA). Not a true blocker for this paper because PMC JATS
  carries everything we need; *would* be a blocker for digitizing
  Krisko & Radman 2010 figures without a real browser.

### Verdict

GREEN-LIGHT, qualitative replication achieved; numeric replication
deferred pending figure digitization.

### QA recommendation

KEEP at Tier A. Downgrade the "verdict_or_plan" column in
`LUCID100_SOLID_MASTER_QA.tsv` from `simulation/model replication` to
`simulation/model replication — qualitative complete; numeric pending
data digitization`.
