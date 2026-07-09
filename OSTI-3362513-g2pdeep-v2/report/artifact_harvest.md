# Artifact harvest — OSTI-3362513 / G2PDeep-v2

All artifacts pulled from public/free sources on 2026-07-02.

| # | Artifact | URL / accession | Size (B) | HTTP status | Notes |
|---|---|---|---:|---|---|
| A1 | OSTI-3362513 full PDF | https://www.osti.gov/servlets/purl/3362513 | 5,031,661 | 200 (via uicgpu proxy) | Zeng et al., Biomolecules 2025, 15, 1673. Saved to `work/osti_3362513.pdf`. |
| A2 | G2PDeep-v2 web front-end | https://g2pdeep.org/ | 844 (React SPA shell) | 200 | Live; React app served from Django backend. |
| A3 | G2PDeep-v2 main JS bundle | https://g2pdeep.org/static/js/main.2237ed21.js | 7,103,662 | 200 | 40+ `/api/*` endpoints enumerated from bundle. |
| A4 | Backend counter API — datasets | https://g2pdeep.org/api/analytics/get_dataset_count/ | 55 | 200 | Returned `{"num_datasets": 187}`. |
| A5 | Backend counter API — models | https://g2pdeep.org/api/analytics/get_model_count/ | 52 | 200 | `{"num_models": 68}`. |
| A6 | Backend counter API — projects | https://g2pdeep.org/api/analytics/get_project_count/ | 55 | 200 | `{"num_projects": 590}`. |
| A7 | Backend catalog API — datasets types | https://g2pdeep.org/api/information/fetch_all_dataset_type/ | 1,428 | 200 | Full JSON listing 6 omics types with descriptions. |
| A8 | Backend catalog API — study cases | https://g2pdeep.org/api/information/fetch_all_study_cases_database | 74 | 200 | `["TCGA (non-uniform)", "TCGA (uniform)"]`. |
| A9 | FireBrowse TCGA metadata | http://firebrowse.org/api/v1/Metadata/Cohorts?format=json | 3,296 | 200 | Complete 38-cohort list incl. BRCA, SKCM, HNSC etc. Saved to `evidence/firebrowse_cohorts.json`. |
| A10 | GitHub code repo (reference/v1 model) | https://github.com/shuaizengMU/G2PDeep_model | git clone | — | Apache-2.0, 7 stars, 4 related public forks. Also cited from README of the v2 paper. |
| A11 | SoyNAM SNP-encoded height dataset | (bundled in A10) `data/SoyNAM/height.{train,test}.csv` | 39,341,781 + 9,902,879 | — | 4110 train / 1028 test rows × 4237 cols (label + 4236 SNPs). Real, cited to Diers et al. (SoyNAM). |
| A12 | SoyNAM SNP-encoded yield dataset | (bundled in A10) `data/SoyNAM/yield.{train,test}.csv` | 38,282,352 + 9,625,719 | — | 4001 train / 1001 test rows × 4237 cols. |
| A13 | Related public repos found | GitHub search `q=g2pdeep in:name` | — | 200 | 5 hits: `shuaizengMU/G2PDeep_model`, `shuaizengMU/G2PDeep_model_legecy`, `shuaizengMU/G2PDeep_model_collection`, `MaoZain/G2PDeep`, `Mohammad-Vahed/G2PDeep`. |

## Independently generated evidence (this run)

| # | File | Size | What it is |
|---|---|---:|---|
| E1 | `report/evidence/metrics_height.json` | 723 | Held-out test PCC/SCC/MSE/MAE for SoyNAM height (real training, uicgpu A100, TF 2.8, 40 ep). |
| E2 | `report/evidence/metrics_yield.json` | 720 | Same for SoyNAM yield (39 ep, early-stopped). |
| E3 | `report/evidence/g2pdeep_api_probes.md` | ~2 kB | Textual capture of the 10 backend endpoints probed with HTTP status + first 500 B of body. |
| E4 | `report/evidence/firebrowse_cohorts.json` | 3,296 | Raw FireBrowse cohort catalog (proves the underlying TCGA source is still reachable). |
| E5 | `report/evidence/github_repo_g2pdeep_model.json` | ~5 kB | GitHub API metadata for the reference code repo. |
| E6 | `work/paper.txt` | ~200 kB | Full-paper plaintext (pdftotext -layout). |
| E7 | `work/code/G2PDeep_model/` | full clone | Cloned Apache-2.0 reference code with the SoyNAM data payload. |

**No paywalled resources, no private data, no fabricated numbers.**
