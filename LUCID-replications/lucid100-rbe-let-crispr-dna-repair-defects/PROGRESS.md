# PROGRESS — LUCID100 #63 (Guerra Liberal et al., Med Phys 2024, doi:10.1002/mp.16764)

Owner: Ollie (subagent), slot 32 Wave 4 backfill. Host: CherryRd. CPU only.

## Timeline

- **2026-06-09 13:45 CDT.** Task received. Folder created at `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-rbe-let-crispr-dna-repair-defects/`.
- **2026-06-09 13:46.** Metadata fetched (Crossref, OpenAlex). License confirmed CC-BY 4.0 hybrid OA. PubMed has no PMC ID (not in PMC).
- **2026-06-09 13:47.** Wiley `pdfdirect` retrieval failed (Cloudflare bot-detection → 5 KB HTML stub). Birmingham institutional OA mirror succeeded: `paper_birmingham_submitted.pdf` (10 pages, 866 KB, publishedVersion).
- **2026-06-09 13:48.** `pdftotext -layout` extracted main text (61 KB). Read DAS, methods, results, discussion. DAS = "all data in article + SI"; no Zenodo/GitHub/OSF reference.
- **2026-06-09 13:49.** Located same-author RBE library at https://github.com/sjmcmahon/RBEModels (4 KB, no LICENSE, two Python files). Pulled both files into `artifacts/rbemodels_upstream/`.
- **2026-06-09 13:50.** Built `scripts/smoke_rbe_let_fit.py` (LQ + MID + RBE pipeline + per-genotype RBE/LET regression). Test pass: WT R² = 0.9997, LIG4 R² = 0.9953 (paper: ~0.99).
- **2026-06-09 13:51.** Built `scripts/upstream_models_demo.py` (six phenomenological models from sjmcmahon/RBEModels). McNamara matches paper WT RBE to <1% (1.119/1.282 vs 1.130/1.290).
- **2026-06-09 13:52.** Manifest, FIRST_PASS_REPORT.md, README.md, this PROGRESS.md, JSON progress record written.

## State

| Item | Status |
| --- | --- |
| Paper PDF (OA submitted version) | ✅ in `artifacts/` |
| Bibliometadata (Crossref + OpenAlex) | ✅ |
| Wiley SI PDF | ❌ blocked by Cloudflare; needs manual one-click |
| Per-dose survival CSVs | ❌ (in SI) |
| LQ + MID + RBE pipeline | ✅ `scripts/smoke_rbe_let_fit.py` |
| Smoke fit reproducing paper's linear RBE/LET claim | ✅ R² 0.9997 / 0.9953 |
| Upstream RBEModels cross-check | ✅ McNamara matches WT to <1% |
| Figure replication | ⚠️ partial (`figures/smoke_rbe_vs_let.png`, `figures/upstream_models_vs_paper_wt.png`) — no Fig 1/3 yet |
| Heavy-compute job plan | n/a (CPU only, sub-second runtime) |
| QA retag recommendation | ✅ in `docs/FIRST_PASS_REPORT.md` §7 |

## Next steps (when picked back up)

1. Manual SI download from Wiley → `artifacts/mp16764_SI.pdf` (browser, profile=user).
2. Parse SI tables → `data/survival_per_dose.csv` and `data/dsb_repair_pct.csv`.
3. Promote smoke to full LQ refit via `scipy.optimize.curve_fit`; recompute MID, RBE, SER per (genotype × radiation_quality). Compare with paper Table/Fig 2 values; target ±5%.
4. Reproduce Fig 1 (4 panels), Fig 2 (4 panels), Fig 3 (3 panels). Save under `figures/replicated/`.
5. Optional: cite-graph walk for Fig 4 RBE_D10 meta-analysis.
6. Write final `REPORT.md` with coverage / agreement scores and request a QA retag PR against `LUCID100_SOLID_MASTER_QA.tsv` row 63.
