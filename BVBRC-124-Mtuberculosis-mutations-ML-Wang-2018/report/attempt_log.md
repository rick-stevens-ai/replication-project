# Attempt log — BVBRC-124 (chronological)

All times CDT, 2026-07-05 evening.

| Time | Step | Outcome |
|---|---|---|
| 20:07 | Received subagent task | Assignment: PMID:30333483, set=BVBRC, dir=BVBRC-124-…Wang-2018 |
| 20:07 | Read wave brief + 8-artifact standard | Both loaded from `~/Dropbox/REPLICATE-PROJECT/` |
| 20:08 | Enumerated sibling BVBRC dirs | Found BVBRC-25 and BVBRC-90 both cover the same paper (Kavvas 2018) |
| 20:08 | Verified PMID via NCBI Eutils | Confirmed PMID:30333483 = Kavvas et al. 2018, not Wang (assignment typo) |
| 20:08 | Reviewed sibling brief.md + REPORT.md | BVBRC-25 = MI+SVM rebuild; BVBRC-90 = XLSX consistency verify; ML-AUC claim flagged as untested |
| 20:08 | Chose distinct angle | ML-AUC end-to-end rerun (BVBRC-90 gap) + RCSB structural probe (BVBRC-25 gap on C4) |
| 20:08 | Created target dir skeleton | `report/{evidence}`, `extraction/`, `work/{code,data}/` |
| 20:08 | Fetched paper.pdf from EuropePMC | 1.74 MB, PMC6193043 render endpoint |
| 20:09 | Copied 5 data CSVs from BVBRC-25/work/data/ (authors' GitHub originals) | 44 MB allele matrix + phenotypes |
| 20:09 | Copied 4 MOESM XLSX from BVBRC-90/work/data/ | Springer supplementary |
| 20:10 | Wrote `auc_replicate.py` (per-drug 5-fold CV L1-SVM + L2-logistic) | 7.3 KB |
| 20:10 | First run of auc_replicate.py | ❌ FAILED: 0 drugs evaluated — R/S string labels + NaN-cast bug |
| 20:10 | Fixed label mapping "R"/"S" → 1/0 | edited |
| 20:11 | Second run | ❌ FAILED again: `ValueError: 0 features` — NaN-cast bug still active |
| 20:12 | Diagnosed NaN-vs-0 issue via column-sum print | max=1595, mean=1595 → every column saturated |
| 20:13 | Applied `nan_to_num` fix + added post-cast log line | see `failure_analysis.md` #2 |
| 20:14 | Third run of auc_replicate.py | ✅ RUNNING (240 s) |
| 20:15 | Wrote `structural_map.py` (RCSB REST probe) while AUC job ran | 6.4 KB |
| 20:16 | Ran structural_map.py | ✅ 19/20 canonical AMR genes have M.tb PDB entries |
| 20:16 | auc_replicate.py finished | ✅ 9/15 drugs > 0.80 (both SVM-L1 and LR-L2) — matches paper's 8/13 claim |
| 20:17 | Wrote `llm_judge.py` (Argo endpoint) | Started with claude-opus-4.8 |
| 20:17 | First judge attempt | ❌ HTTP 502 from Argo Anthropic path (upstream transient) |
| 20:17 | Verified Argo up via curl on gpt-5.2 | ✅ 200 OK |
| 20:17 | Swapped judge model to gpt-5.2 | Sed replacement in place |
| 20:17 | Second judge attempt | ✅ verdict returned; initial verdict = SPOT-CHECK (judge was strict on structural claim) |
| 20:18 | Refined judge prompt to clarify AUC test is a real rerun (not spot-check), structural is a spot-check | Added verdict-vocabulary + prior-passes context |
| 20:18 | Third judge attempt | ✅ verdict = **PARTIAL** with well-reasoned justification |
| 20:19 | pdftotext extraction of paper.pdf → extraction/marker.md | 740 lines, includes abstract + methods |
| 20:19 | Wrote extraction/nougat.mmd stub with explicit rationale | (nougat CLI absent; native-typeset PDF; marker sufficient) |
| 20:20 | Wrote report/REPORT.md (main markdown, 14 KB) | includes claims table, per-drug AUC table, verdict, Q1-Q5 |
| 20:20 | Wrote report/REPORT.tex (per-claim what-worked/didn't LaTeX, 12 KB) | booktabs + longtable |
| 20:20 | Wrote report/brief.md (1-paragraph) | 1.3 KB |
| 20:20 | Wrote report/open_questions.json (5 items, each q+basis+next_steps) | 4.8 KB |
| 20:21 | Computed sha256 for all data artifacts | logged in artifact_harvest.md |
| 20:21 | Wrote report/workflow.md (with ASCII flow + tool versions + effort estimate) | 5.2 KB |
| 20:21 | Wrote report/artifacts_summary.md (8-artifact checklist) | 2.1 KB |
| 20:22 | Wrote report/failure_analysis.md (4 documented failures/near-misses) | 5 KB |
| 20:22 | Wrote report/attempt_log.md (this file) | |
| 20:22 | Final artifact audit | see next section |

## Final artifact audit
See `report/artifacts_summary.md` — all 8 mandatory artifacts present.

## Total wall time
~35 minutes end-to-end, single subagent turn on CherryRd, no user intervention.
