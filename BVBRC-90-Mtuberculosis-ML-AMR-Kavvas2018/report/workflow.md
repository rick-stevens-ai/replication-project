# Workflow — BVBRC-90 Kavvas et al. 2018 replication

**Target paper:** Kavvas ES, et al. *Nat Commun* 9:4306 (2018). DOI: 10.1038/s41467-018-06634-y.
**Set:** BVBRC. **Directory:** `BVBRC-90-Mtuberculosis-ML-AMR-Kavvas2018`.
**Verdict:** PARTIAL (strong).

## Stage 1 — Paper + supplementary artifact acquisition
- **Inputs:** DOI, Springer static-content CDN URLs, laptop network.
- **Actions:**
  1. `curl -L` loop over `MOESM{1,4,5,7,8,9}` from the Springer CDN into `work/data/`.
  2. Verify MD5s and record in `report/artifact_harvest.md`.
- **Outputs:** `work/data/41467_2018_6634_MOESM{1,4,5,7,9}_ESM.{pdf,xlsx}` (5 files, 6.06 MB).
- **Gotcha:** MOESM8 (co-occurrence tables, Sup Data 5) returns Springer `AccessDenied` XML with HTTP 403. Not blocking — the underlying signal is recoverable from MOESM9 + MOESM7. Did NOT escalate to Springer or archive.org.

## Stage 2 — Test C2/C7 — known + new AMR-gene recovery
- **Inputs:** MOESM4 (MI/χ²/ANOVA per drug), MOESM5 (SVM-SGD selected alleles per drug), MOESM9 (full 254-allele AMR panel).
- **Actions:** `openpyxl` parse each sheet; string-match Table 1 (33 known genes) and Table 2 (23 new genes) against per-drug top-40 MI + top-59 SVM lists and the full 254 panel. Repeat with case normalization.
- **Outputs:** `report/evidence/mi_top40.json`, `svm_features.json`, `table1_verification.json`, `table1_full_verify.json`, `known_new_gene_recovery.json`.
- **Result:** 27/33 exact and 28/33 case-norm (85%) at the panel level; 14/18 (78%) at the drug-specific top-tier level; 22/23 exact and 23/23 case-norm for Table 2.
- **Gotcha:** `Chp2` vs `chp2`; the paper's tabulation uses inconsistent capitalization vs the supplementary sheets.

## Stage 3 — Test C3 — MI ranking of canonical drug targets
- **Inputs:** MOESM4 top-40 per drug.
- **Actions:** for each of 8 drugs with a well-known canonical target (rpoB/rifampicin, katG/isoniazid, etc.), compute the target's rank in the MI-sorted allele list.
- **Outputs:** `report/evidence/mi_rank_check.json`.
- **Result:** 3/8 at rank #1; 6/8 in top-5. Null-hypothesis probability of the observed pattern (~1000 candidate genes) is ~10⁻⁹.

## Stage 4 — Test C4 — LOR sign vs AMR label internal consistency
- **Inputs:** MOESM9 (2000 alleles × 15 cols including `allele_LOR` and R/S/N label).
- **Actions:** for each R allele check `LOR > 0`; for each S allele check `LOR < 0`.
- **Outputs:** `report/evidence/moesm9_summary.json`.
- **Result:** 809/809 (100%). Perfect internal-validity check on the paper's data pipeline.

## Stage 5 — Test C5 — allele-sequence realism vs NCBI H37Rv
- **Inputs:** MOESM9 (allele AA sequences per gene), NCBI E-utils `efetch` on 6 canonical AMR RefSeqs (NP_216424.1 katG, NP_216559.1 pncA, NP_215181.1 rpoB, NP_214520.1 gyrA, NP_216000.1 inhA, NP_215196.1 rpsL).
- **Actions:** fetch NCBI FASTA over HTTPS; compare against highest-pident MOESM9 allele per Rv gene ID.
- **Outputs:** `report/evidence/ncbi_seq_verification.json`, `work/intermediates/h37rv_reference_proteins.fasta`.
- **Result:** 4/6 byte-identical, 1 near-identical (gyrA, 837/838), 1 truncated cluster variant (rpoB, 1096/1172 aa — paper-acknowledged consequence of reference-agnostic clustering).

## Stage 6 — Test C6 — epistatic interaction significance
- **Inputs:** MOESM7 (307 candidate gene-gene interactions with logistic-regression p-values).
- **Actions:** Benjamini-Hochberg FDR correction at α=0.05 on all 307; then verify specific pairs the paper text calls out.
- **Outputs:** included in `evidence_bundle.json`.
- **Result:** 232 pass BH (superset of the paper's 94, because we omit the paper's per-class top-60 pre-filter). All 5 paper-highlighted pairs (embB:ubiA, ubiA:embR, katG:oxcA, katG:inhA, gyrA:ansP2) confirmed with p<0.05; katG:inhA at p=5.2e-23.

## Stage 7 — LLM judge pass
- **Inputs:** `report/evidence/evidence_bundle.json` (consolidated summary) + `report/evidence/judge_prompt.txt` (fixed prompt).
- **Actions:** POST to Argo proxy `http://<tailnet-aggregator>:44497/v1/chat/completions`, model `argo:gpt-5.2` (FREE endpoint per standing Rick rule), zero temperature, JSON-only response.
- **Outputs:** `report/evidence/llm_judge_gpt5.json`.
- **Result:** verdict PARTIAL, coverage 75%, agreement 95%. Not blind — the judge sees our summary, not the paper. Treat as self-consistency signal.

## Stage 8 — Report assembly
- `report/REPORT.md` — canonical narrative (human read).
- `report/REPORT.tex` — LaTeX rendition of the above with headline-vs-exercised table + genuine critique.
- `report/open_questions.{json,_section.tex}` — 5 follow-up questions with basis + next-steps.
- `report/artifact_harvest.md`, `attempt_log.md`, `brief.md` — provenance + audit trail.
- `report/failure_analysis.md` — honest critique of the PARTIAL verdict + methodological gaps.
- `report/artifacts_summary.md` — one-line inventory of every file in the deliverable.
- `extraction/nougat.mmd` — Nougat OCR stub (NOT run; paper is native-text HTML from PMC).

## Compute + cost budget
- **Compute:** CherryRd laptop, Python 3.13 + openpyxl, no GPU, no cluster.
- **API calls:** 6 NCBI efetch (free), 1 Argo LLM-judge call (free endpoint).
- **Wall time:** ~15 min end-to-end.
- **Cost:** $0.
- **Standing rule respected:** free endpoints only, no paid API, no ALCF token burn.
