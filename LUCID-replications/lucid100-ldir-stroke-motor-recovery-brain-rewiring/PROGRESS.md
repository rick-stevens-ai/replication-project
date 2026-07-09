# PROGRESS — LUCID100 slot 52 (rank 83, Wave 6, Tier B)

DOI: 10.1016/j.bbi.2023.09.015 — Au NPB et al., *Brain Behav Immun* 2024.

## 2026-06-09 (Tue, CDT) — first pass

- 14:25 — Task received, confirmed slot 52 = rank 83 in `LUCID100_SOLID_MASTER_QA.tsv`.
- 14:25 — Created workspace under `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-ldir-stroke-motor-recovery-brain-rewiring/`.
- 14:26 — Resolved Semantic Scholar paperId 20be9770…, PMID 37774892. Authors: Au, Wu, Kumar, Jin, Y Li, S L Chan, J H C Lai, K W Y Chan, K N Yu, X Wang, C H Eddie Ma. Senior author: Eddie Ma (CityU Hong Kong, Department of Neuroscience). 131 references, 12 citations as of fetch.
- 14:26 — Full PDF closed-access (Elsevier ClinicalKey); Unpaywall reports no OA copy. Abstract obtained via Semantic Scholar API + PubMed.
- 14:26 — PubMed LinkOut surfaced `GSE244016` via NIAID Data Ecosystem. Pulled GEO record: 24 RNA-seq samples, mouse cortex, 300 mGy X-ray vs sham, naive + D1/D3/D7 post-photothrombotic stroke ipsi cortex, n=3 per group; NovaSeq 6000; STAR 2.7.8a; supplementary 7.5 MB TAR of RawCount+TPM tab-delimited files.
- 14:26 — Downloaded GSE244016_RAW.tar (7.8 MB), extracted 24 GSM*.txt.gz to `artifacts/GSE244016_RAW/`.
- 14:27 — Inspected one sample: format `GeneName\tRawCount\tTPM`, 55,274 mouse gene rows. Confirmed organism = mouse despite GEO metadata typo claiming GRCh38.
- 14:27 — Authored `scripts/smoke_replication.py`: 24-sample count load + log2(CPM+1) + per-timepoint Welch DE + Fisher-exact enrichment against 5 curated mouse gene panels.
- 14:27 — Ran smoke on CherryRd; <10 s runtime, <500 MB peak. Outputs in `results/`:
  - counts_matrix.tsv (55,273 × 24)
  - cpm_log2.tsv
  - sample_meta.tsv
  - de_{D1,D3,D7,naive}_LDIR_vs_Sham.tsv
  - smoke_summary.{json,md}
- 14:28 — DE summary (LDIR vs Sham, stroke ipsi cortex, |logFC|>0.585 & p<0.05):
  - D1: 8 up / 21 down
  - D3: 47 up / 8 down
  - D7: 29 up / 10 down
  - naive: small counts; sanity contrast only
  - No genes survive BH FDR < 0.1 at any timepoint (expected for n=3 Welch).
- 14:28 — Curated-set enrichment in LDIR-up nominal hits: essentially null at every timepoint. Only suggestive hit: `Slit1` (axonal projection set) at D3, OR 19.0, p 0.055.
- 14:28 — Worktype curator tag (`omics/signature replication`) is partly correct but understates scope: paper is primarily a **wet-lab mouse study** with embedded bulk RNA-seq. Recommend QA refinement to `wet-lab animal study + omics component (GSE244016)` and keep replication scope to the omics pillar only.
- 14:29 — Wrote README.md, MANIFEST.json, FIRST_PASS_REPORT.md.
- 14:29 — Updated subagent-progress JSON record.

### Status

| Item | State |
|---|---|
| Source-of-truth row found | ✅ rank 83 |
| Folder created | ✅ |
| Paper metadata harvested | ✅ (abstract + authors + IDs) |
| Full PDF | ❌ paywalled, no OA |
| Supplementary tables | ❌ behind Elsevier |
| Public dataset identified | ✅ GSE244016 |
| Dataset downloaded | ✅ 7.5 MB processed counts |
| Counts matrix built | ✅ 55,273 × 24 |
| Smoke DE run | ✅ |
| Curated-set enrichment | ✅ (null with n=3 Welch — expected) |
| FDR-significant DE recovered | ❌ (need DESeq2 + larger n or LRT-across-time) |
| Author contact | ❌ (forbidden per task) |
| Heavy compute used | ❌ (local only, <10 s) |
| Reports written | ✅ README, PROGRESS, FIRST_PASS_REPORT, MANIFEST |
| QA progress JSON updated | ✅ |

### Next actions (for Wave-7 follow-up or upgrade)

1. Install Bioconductor DESeq2 in an R sidecar (uicgpu venv preferred) and re-run with design `~ condition + timepoint + condition:timepoint`, applying `lfcShrink(type="apheglm")`. n=3 per cell makes a full LRT over time the most powerful contrast.
2. Pull MSigDB Hallmark + REACTOME Mm symbol GMTs (gseapy/fgsea) and run preranked GSEA on each timepoint's DESeq2 shrunken logFC list. Compare top up/down pathways to the paper's claimed inflammation/microglia/phagocytosis enrichment.
3. If supplementary DE tables eventually become accessible (Sci-Hub policy disallowed; try institutional access at Argonne or CityU), cross-validate our top-1k DE genes against theirs.
4. Optional: pull SRA FASTQ for one matched pair (Sham vs LDIR D3) and re-align with STAR + GENCODE M30 to verify the upstream pipeline; not needed unless DESeq2 results conflict with paper.
5. Optional: probe whether authors deposited per-mouse behavior/MRI/EEG metrics anywhere (Dryad/Zenodo/figshare search by author name and DOI) — initial scan negative.
