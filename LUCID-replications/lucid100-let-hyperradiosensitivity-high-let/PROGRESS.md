# PROGRESS.md — LUCID100 Wave 3 / Slot 21

## 2026-06-09 (Tue) — first pass (subagent, ~10 min)

- **Source-of-truth lookup.** Master TSV `LUCID100_SOLID_MASTER_QA.tsv`
  row 52 (Wave 3, rank A-17): DOI `10.1667/rade-25-00194`, Sennhenn et al.
  2026 Radiation Research, original worktype tag `omics/signature
  replication`. KEEP-rated.
- **Legitimacy check.** Crossref ✅ (Vol 205, Feb 2026, 5 authors).
  PubMed ✅ PMID 41651140. Europe PMC: not OA, not in EPMC, no preprint.
  arXiv/bioRxiv: no preprint. Unpaywall: `is_oa=false`.
  Publisher landing (kglmeridian.com) returns metadata + abstract only;
  full body paywalled.
- **Open dataset traced.** The 93-curve corpus is overwhelmingly the
  Polgár, Schofield, Madas 2022 *Scientific Data* (DOI
  `10.1038/s41597-022-01653-3`, CC-BY, PMC9458642) hosted on STOREDB
  STUDY1163 / DATASET1252 (DOI `10.20348/STOREDB/1163`). Two paper
  co-authors are common: Polgár & Madas.
- **Artifact harvest.** Found `download.jsp?fileId=` pattern in STOREDB
  HTML and retrieved one-shot tokenized download URLs for FILE12921,
  12923, 12933, 12935 → `data/{database_v1.xlsx, database_v2.xlsx,
  study_and_dataset_description_v{1,2}.pdf}`. sha256-stamped in
  ARTIFACT_MANIFEST.tsv.
- **Parser.** `code/parse_db.py` reads `database_v2.xlsx` (1422 rows,
  single sheet "Database"). Resolves block layout (header row carries
  dataset id + LQ-fit params; second row carries IR-fit params; cell-line
  and irradiation properties stacked over 4–5 rows). Outputs:
  - `results/curves_long.csv` — 1020 `(id, dose_Gy, SF, SF_min, SF_max)`
  - `results/curves_meta.csv` — 101 datasets with published LQ & IR
    parameters, cell line, irradiation descriptor.
- **Smoke fits.** `code/fit_models.py` (numpy + scipy + matplotlib):
  - LQ + Joiner–Marples IR models with bounded least-squares;
  - AICc-based model selection;
  - per-curve LQ vs IR comparison; HRS-positive list ranked by ΔAICc;
  - cohort histogram of ΔAICc.
  Results: 101/101 curves fit. **Re-fit IR parameters reproduce the
  digitized published values to within ~11% (median)** for α_r, α_s, D_c.
  40 of 98 curves show a textbook HRS-IRR signature (ΔAICc > 4 with
  α_s ≫ α_r, D_c < 1 Gy). Top hits: id 5 (Marples & Joiner 1993 V79,
  ΔAICc 35.6), id 1 (Lambin 1993 HT29, ΔAICc 25.2) — landmark HRS studies.
- **LET-compression check.** `code/let_compression.py` parses LET strings
  out of `irradiation` descriptors. Only 9 high-LET datasets exist in the
  public corpus. Median D_c and α_s/α_r are essentially flat between
  low-LET (n=51) and high-LET (n=9) subsets — *as expected*, because the
  paper's headline LET-compression result depends on helium/carbon ion
  data **not bundled in STOREDB**.
- **Verdict.** KEEP, replication-plausible with caveats. Smoke
  replication of the upstream LQ/IR backbone is solid; the paper's
  proprietary MML and MML×LEM extensions are paywalled. Recommended
  retag: `omics/signature replication` → `computational model /
  dose-response`.
- **Cost.** No paid endpoints used. Compute: < 10 s single-core on
  CherryRd. Artifact size ≈ 1.2 MB. No heavy-compute job needed.
- **Outputs.** README.md, FIRST_PASS_REPORT.md, PROGRESS.md (this),
  ARTIFACT_MANIFEST.tsv, 4 figures, 4 derived CSVs, 1 summary JSON, 3
  scripts, 4 raw artifacts. Subagent progress JSON updated under
  `~/.openclaw/workspace/memory/subagent-progress/`.

## 2026-06-22 (Mon) — final pass (subagent, ~5 min)

- **Strengthened replication.** New script `code/strengthen_fits.py`
  reruns LQ + Joiner–Marples IR fits on all 101 STOREDB v2 curves with:
  bootstrap 95% CIs (B=200, 98/101 curves), AICc + BIC model selection,
  goodness-of-fit on log10(SF) (R² + RMSE), per-cell-line and
  per-LET-band aggregation, and Mann–Whitney U tests low- vs high-LET.
- **Headline numbers.** Median R²(log SF): IR 0.969 vs LQ 0.851. IR
  beats LQ by ΔAICc > 4 in 41% (40/98) and by ΔBIC > 2 in 79%.
  Independent re-fit reproduces published IR params to median |rel diff|
  10.6% (α_r), 11.8% (α_s), 11.2% (D_c). 52 cell lines, 5 LET bands.
  Low-vs-high LET Mann–Whitney: D_c p=0.24, α_s/α_r p=0.14 (directional
  compression as paper claims, but underpowered at n_high=7).
- **Verified GitHub Org.** `Radiobiology-Informatics-Consortium` exists
  but contains ONLY 1 repo: `RBO` (Radiation Biology Ontology). No
  MML/LEM repo. Documented as Blocker 3.
- **Cross-checked open dataset PDFs.** `pdftotext | grep` for LEM/MML/
  GitHub/multiscale on both v1+v2 description PDFs returned ZERO hits.
  Confirms the modelling content is genuinely paywall-gated.
- **Final verdict.** `report/REPORT.md` (~18 KB): PARTIAL replication,
  Coverage 5/10, Agreement 8/10. Three named, specific reproducibility
  blockers: (1) paywalled article body, (2) helium/carbon-ion validation
  cohort not in STOREDB (PIDE-v3.2 named as next-pass fallback), (3) no
  MML/LEM implementation in the consortium GitHub org.
- **Cost.** Zero paid endpoints. ~3.5 min single-core CPU on CherryRd.
  Project folder now ~1.6 MB.
- **Outputs (new).** report/REPORT.md, code/strengthen_fits.py,
  results/fits_strengthened.csv, results/cellline_summary.csv,
  results/let_band_summary.csv, results/strengthened_summary.json,
  figures/gof_loglog.png, figures/published_vs_fit.png,
  figures/let_band_dc.png, figures/let_band_amp.png.
  All pre-existing files preserved unchanged.
