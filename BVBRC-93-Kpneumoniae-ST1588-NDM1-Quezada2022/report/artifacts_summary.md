# BVBRC-93 Artifacts Summary

**Dataset:** BVBRC-93-Kpneumoniae-ST1588-NDM1-Quezada2022
**Paper:** Quezada-Aguiluz et al., *Antibiotics* 2022, 11(9):1207 (PMID 36139987)
**Verdict:** REPLICATED (LLM-judge coverage 0.90, agreement 0.98)

---

## 1. Report deliverables (`report/`)

| Path | Description |
|------|-------------|
| `report/REPORT.md` | Canonical Markdown replication report (Claims table, Methods, Results-vs-paper, Verdict). |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section (6 items). |
| `report/open_questions.json` | 5 open scientific questions grounded in ST1588 / NDM-1 biology, with basis + next steps. |
| `report/workflow.md` | Full 24-step reproducible workflow. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Enumerated risks, near-misses, and honest limits. |
| `report/evidence/` | Raw tool outputs (mlst, amrfinder, kleborate, plasmidfinder BLAST, pairwise plasmid BLAST, Fig. 1B landmark parse). |

## 2. Independent raw evidence (`work/` on uicgpu)

| Path | Description | Provenance |
|------|-------------|------------|
| `work/data/UCO361_all_contigs.fasta` | Full 15-contig assembly, 5,841,932 bp, md5 `85adabb6d97992295a31f788fad0a1dc`. | NCBI EFetch (`rettype=fasta`), assembly `JAMJQY010000000`. |
| `work/data/pNDM1_UCO361.gb` | RefSeq PGAP annotation of plasmid contig (326 CDS). | NCBI EFetch (`rettype=gbwithparts`), `NZ_JAMJQY010000002.1`. |
| `work/data/pNDM1_UCO361_only.fasta` | Extracted plasmid contig for pairwise BLASTn. | Sliced from full assembly. |
| `work/data/MN598004.1.fasta` | pNDM-1-EC12 reference (351,777 bp). | NCBI EFetch. |
| `work/data/CP041388.1.fasta` | pRAO166a reference (382,325 bp). | NCBI EFetch. |
| `work/plasmidfinder_db/` | PlasmidFinder database (post-paper snapshot). | `git clone` from `bitbucket.org/genomicepidemiology/plasmidfinder_db`. |

## 3. Tool outputs

| File | Content | Key result |
|------|---------|------------|
| `mlst_klebsiella.tsv` | mlst 2.35.0 output. | ST1588, 7/7 exact allele matches. |
| `amrfinder_out.tsv` | AMRFinderPlus 3.12.8 (DB 2024-07-22.1). | 46 rows, 19 AMR-class hits; blaNDM-1 100/100. |
| `kleborate_out/` | Kleborate v3.2.4 with kpsc preset. | ST1588, KL108, O1αβ,2β, virulence_score=0, 12 AMR genes. |
| `pfinder_hits.tsv` | BLASTn vs PlasmidFinder DB (≥95% id, ≥60% cov). | Contig 2: pC39-family partials (post-paper DB). Contig 3: IncFIB(K)_1 (98.93/100). |
| `pairwise_MN598004.tsv` | BLASTn pNDM-1_UCO361 vs MN598004.1. | 92 HSPs, longest 57,352 bp @ 98.64%, total ≥90% id = 211,270 bp. |
| `pairwise_CP041388.tsv` | BLASTn pNDM-1_UCO361 vs CP041388.1. | 96 HSPs, longest 39,233 bp @ 99.02%, total ≥90% id = 215,338 bp. |
| `fig1B_landmarks.tsv` | Parsed 300000–315000 bp CDS features. | All 6 landmarks in exact expected order. |

## 4. LLM-judge artifact

- **Endpoint:** `http://127.0.0.1:44497/v1/chat/completions` (Argo proxy, free).
- **Model:** `argo:gpt-5.1`.
- **API key:** `stevens`.
- **Response:** `{"verdict":"REPLICATED","coverage_frac":0.9,"agreement_frac":0.98,"one_line":"All genomically testable claims are independently reproduced with only minor annotation-label differences and a clarified, but not contradictory, interpretation of megaplasmid novelty."}`
- **Cost:** $0.00 (Argo is free per project rule).

## 5. External references used

| Accession | Description | Purpose |
|-----------|-------------|---------|
| `JAMJQY010000000` | UCO-361 WGS assembly (target). | Independent replication input. |
| `NZ_JAMJQY010000002.1` | pNDM-1_UCO361 plasmid contig (314,976 bp). | Fig. 1B landmark check + pairwise BLASTn. |
| `MN598004.1` | pNDM-1-EC12, *E. cloacae* NDM-1 megaplasmid (351,777 bp). | Paper's stated "closest plasmid." |
| `CP041388.1` | pRAO166a, paper's stated "different environment" comparator (382,325 bp). | Whole-plasmid backbone comparison. |
| `CP061701` | pC39 (post-paper deposit). | Source of current PF DB repHI5B/repFIB hits on contig 2. |
| `PRJNA224116` | BioProject. | Deposit context. |
| `SAMN28534325` | BioSample. | Deposit context. |
| `GCF_023554495.1` | RefSeq assembly. | RefSeq PGAP annotation source. |

## 6. Reproducibility summary

- **All inputs md5-checksummed** on retrieval (full assembly md5 recorded).
- **All tool versions logged** in report Methods section.
- **Working dir fresh** — no reuse of prior BVBRC-46 outputs (separate `/data/stevens/bvbrc93-kpneu-st1588-independent/`).
- **Endpoints:** NCBI E-utilities, EuropePMC REST, PlasmidFinder Bitbucket, Argo proxy `:44497`. No paid APIs.
- **Compute:** uicgpu A100 pool (no Mac cycles used for BLASTn / annotation).
