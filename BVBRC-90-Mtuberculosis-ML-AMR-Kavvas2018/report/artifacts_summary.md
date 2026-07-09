# Artifacts summary — BVBRC-90 (Kavvas et al. 2018)

## Report deliverables (`report/`)
- `REPORT.md` — canonical narrative report (v1, 2026-07-04). Verdict PARTIAL (strong).
- `REPORT.tex` — LaTeX rendition with headline-vs-exercised table + genuine critique section.
- `open_questions.json` — 5 open questions as bare JSON list, {q, basis, next_steps} per entry.
- `open_questions_section.tex` — 5 open questions as LaTeX enumerated section (input by REPORT.tex).
- `workflow.md` — end-to-end 8-stage pipeline documentation (inputs / actions / outputs / gotchas).
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of the PARTIAL verdict, what was NOT done.
- `brief.md` — original task brief from Rick.
- `attempt_log.md` — chronological attempt log with commands + inline analysis code.
- `artifact_harvest.md` — supplementary-artifact provenance (URLs + MD5s).

## Evidence bundle (`report/evidence/`) — JSON-only intermediates fed to LLM judge
- `mi_top40.json` — MI top-40 gene lists per drug from MOESM4.
- `svm_features.json` — SVM-SGD selected genes per drug from MOESM5.
- `table1_verification.json` — Table 1 known-gene SVM recovery.
- `table1_full_verify.json` — combined MI+SVM recovery per gene.
- `mi_rank_check.json` — canonical drug-target MI rank per drug.
- `moesm9_summary.json` — per-antibiotic allele counts and R/S/N distribution.
- `ncbi_seq_verification.json` — NCBI H37Rv reference vs MOESM9 allele match.
- `known_new_gene_recovery.json` — Table 1 + Table 2 gene recovery in MOESM9.
- `evidence_bundle.json` — consolidated summary passed to LLM judge.
- `judge_prompt.txt` — exact prompt (fixed, reproducible).
- `llm_judge_gpt5.json` — GPT-5.2 verdict JSON (PARTIAL, 75%, 95%).

## Working directory (`work/`)
### Raw supplementary data (`work/data/`, 6.06 MB)
- `41467_2018_6634_MOESM1_ESM.pdf` (5.38 MB) — supplementary information PDF.
- `41467_2018_6634_MOESM4_ESM.xlsx` — Sup Data 1: MI/χ²/ANOVA top-40 per drug × 12 sheets.
- `41467_2018_6634_MOESM5_ESM.xlsx` — Sup Data 2: SVM-SGD selected alleles × 10 drug sheets.
- `41467_2018_6634_MOESM7_ESM.xlsx` — Sup Data 4: 307 epistatic interaction candidates.
- `41467_2018_6634_MOESM8_ESM.xlsx` — **MISSING** (Springer 403 AccessDenied).
- `41467_2018_6634_MOESM9_ESM.xlsx` — Sup Data 6: 2000 alleles × 15 cols (seq, label, drug, uniprot, LOR, Rv-id, gene_name, pident, reference_seq).

### Code (`work/code/`)
- `analysis.py` — driver script consolidating all 6 tests C1-C7.

### Intermediates (`work/intermediates/`) — mirrors of `report/evidence/` + reference proteome
- `h37rv_reference_proteins.fasta` — 6 NCBI H37Rv canonical AMR-gene RefSeqs (katG, pncA, rpoB, gyrA, inhA, rpsL) as ground truth for Test C5.
- 10 JSON intermediates matching `report/evidence/`.
- `analysis_summary.json` — top-level summary of all tests.

## Extraction (`extraction/`)
- `nougat.mmd` — stub. Nougat was NOT run on this paper; PMC provides clean native-text HTML/XML and the supplementary XLSX files were already the primary data source. The stub records this decision + provides fallback OCR pointers.

## Verdict cross-check
- `REPORT.md` line 15: `**Verdict:** **PARTIAL REPLICATION (strong).**` — canonical.
- `REPORT.tex` matches.
- Headline exercised? — **feature-list / tabular headlines YES; quantitative ML-performance headline (AUC>0.80) NO** (raw matrix not distributed). Honest PARTIAL.
