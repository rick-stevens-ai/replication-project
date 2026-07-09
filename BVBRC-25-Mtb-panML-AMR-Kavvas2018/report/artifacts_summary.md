# Artifacts Summary — Kavvas 2018 M. tuberculosis pan-genome ML AMR

**Target:** BVBRC-25 replication wave
**Verdict:** PARTIAL
**Root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-25-Mtb-panML-AMR-Kavvas2018/`

## Input data (authors' published intermediates, `work/data/`)
| File | Dimensions | Purpose |
|---|---|---|
| `pangen_allele_df.csv` | 1,595 strains × 15,367 alleles | Allele presence/absence matrix (md5 e124e874...) |
| `pangen_cluster_df.csv` | 1,595 × 11,039 | Cluster presence/absence matrix |
| `cluster_info.csv` | 11,039 rows | Cluster → Rv id / gene_name / product / pan-category |
| `resistance_data.csv` | 1,595 × 19 drug cols | Binary R/S phenotypes (13 drugs used) |
| `strain_information.csv` | 1,595 rows | Strain metadata |
| `europepmc.json` | — | Bibliographic record (PMID 30333483) |
| `fulltext.xml` | — | Paper full-text (Europe PMC) for method extraction |

All from `github.com/erolkavvas/microbial_AMR_ML/data/`. Free, no auth, direct curl.

## Code (own re-implementation, `work/`)
| Script | Runtime | Purpose |
|---|---|---|
| `replicate_fast.py` | 5.5 s (uicgpu) | Vectorised exact discrete binary–binary MI (bits) + Bonferroni χ² across 10 drugs; collapse alleles→genes; write top-40 + canonical-gene ranks |
| `replicate_svm.py` | 70 s (uicgpu, 64-way joblib) | Ensemble L1-SVM (SGDClassifier hinge, penalty=l1, class_weight=balanced), 200 sims × 80% bootstrap, paper's exact preprocessing (drop PE/PPE/PGRS + drop other-drugs' primary genes), 7 drugs, gene-level selection frequency |

A first slow sklearn per-pair MI attempt was superseded by `replicate_fast.py`'s vectorised version — noted in `attempt_log.md` in `work/`.

## Evidence outputs (`report/evidence/`)
| File | Content |
|---|---|
| `pangenome_stats.json` | C1: per-category cluster counts + PE/PPE/PGRS enrichment (core 3.3% / accessory 24.5% / unique 30.6%) |
| `association_results.json` | C2a: per-drug (10 drugs) top-40 gene MI rankings + canonical-primary-gene rank |
| `svm_results.json` | C2b: per-drug (7 drugs) ensemble SVM gene-level selection frequency, top-40 + known-gene ranks (including ubiA rank 24 for ethambutol) |
| `run_logs.txt` | uicgpu run logs |
| `llm_judge_verdict.json` | Argo `gpt-5.2` structured verdict: PARTIAL, coverage 6, agreement 6 |
| `llm_judge_verdict2.json` | Argo `gpt-4o` structured verdict: PARTIAL, coverage 8, agreement 6 |

## Reports (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable report (17 KB) |
| `REPORT.tex` | LaTeX version + Genuine Critique section |
| `open_questions.json` | 5 open questions grounded in what was and was not resolved |
| `workflow.md` | Step-by-step reproduction workflow |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | What did not replicate and why |

## Key numeric results
- **Pan-genome:** 1,595 strains, 11,039 clusters (Core 3,419 / Accessory 2,402 / Unique 5,218), 15,367 alleles, 13 antibiotics
- **PE/PPE/PGRS enrichment:** 3.3% (core) → 24.5% (accessory) → 30.6% (unique) — 7–9× enrichment in variable genome
- **MI primary-gene recovery (10 drugs tested, 6 pass top-40):** rpoB→1, pncA→1, gyrA→1, rpsL→2, embB→3, katG→4
- **SVM additional-gene recovery:** ubiA→24 (EMB, MI was 81), rpoC→2 (RIF, MI was 273), inhA→38 (INH, MI was 1172), gid→37 (STR, MI was 579), ethA→4 (ETH, MI was 180)
- **LLM judge consensus:** PARTIAL, coverage 6–8/10, agreement 6/10 (two independent Argo endpoints)

## What is NOT here
- No RAxML core-SNP phylogeny (would need CD-HIT re-run or authors' core-gene alignment)
- No 97-interaction epistasis sweep (C3) — logistic-regression gene-gene sweep not attempted
- No 3-D structural mutation mapping (C4) — needs PDB structures + authors' mapping pipeline
- No lineage-stratified sensitivity analysis (Lineage 2 Beijing vs EAI vs LAM)
- No full 33-known + 24-new gene enumeration — only representative recovery tested
- No CRyPTIC MIC-based phenotypic-DST validation of novel signatures

## Free-resource inventory
| Resource | Used for | Cost |
|---|---|---|
| Europe PMC REST + full-text XML | Bibliography + method extraction | Free |
| GitHub `erolkavvas/microbial_AMR_ML` | Authors' pan-genome matrices | Free, no auth |
| uicgpu (255 cores, 2 TB RAM) | MI + ensemble SVM compute | Free (internal) |
| numpy / scipy / scikit-learn / joblib | Vectorised MI, χ², SGD-SVM | Free |
| Argo proxy (`gpt-5.2`, `gpt-4o`) | LLM-judge verdicts | Free (localhost:44497) |

**Total spend: $0.** All heavy compute on internal free capacity; no paid LLM calls.
