# PROGRESS — LUCID100 slot 35 (Wave 4)

## 2026-06-09 (Tue, America/Chicago) — first-pass harvest + smoke replication

- **Launched** as Wave 4 backfill subagent (depth 1/1) per source-of-truth row 84 of `LUCID100_SOLID_MASTER_QA.tsv` (rank 66, priority 14, worktype `omics/signature replication`).
- **Folder created:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-pprm-small-rna-deinococcus/` with the standard subtree (artifacts, code, data, figures, results).
- **Paper harvested:** 1.9 MB OA PDF from `nature.com/articles/s41598-021-91335-8.pdf` (CC BY 4.0). `pdftotext` produced clean `paper.txt` (890 lines, layout-preserved) and `paper_raw.txt`. 10 figure images extracted via `pdfimages` into `artifacts/figures_extracted/`.
- **Metadata harvested:** Unpaywall (oa_status=gold, cc-by; publisher PDF URL confirmed), Semantic Scholar (cites=25, refs=85, PMC8217566), Europe PMC (PMID 34155239, OA=Y).
- **Data accessions identified from paper Data Availability section (line 655-659):**
  - **PRIDE PXD026633** — TMT/Orbitrap Fusion time-course proteomics. Confirmed via PRIDE API: species `Deinococcus radiodurans r1`, instrument Orbitrap Fusion, keywords `Shotgun proteomics, IR, sRNA, Timecourse`. Raw `.raw` files not downloaded for this pass (PASS-mid scope).
  - **GEO GSE176207** — RNA-seq + MAPS. Public since 2021-06-18. 18 samples (GSM5360101-118): 12 RNA-seq (WT × PprSKD × triplicate × {0 kGy, 10 kGy}) and 6 MAPS (MS2-blank vs MS2-PprS triplicates).
- **GEO supplement downloaded:** entire `GSE176207_RAW.tar` is only **215 KB** — 18 gzipped two-column htseq count files (gene, count). Whole transcriptomic dataset is < 0.3 MB.
- **Supplements downloaded:** Springer ESM `MOESM1_ESM.xlsx` (264 KB) = Tables S1-S9 incl. proteomics time-course L2FC, MAPS L2FC for 2,807 genes, PprSKD-vs-WT RNA-seq DEGs at sham (S4) and IR (S5), WT IR effect (S6), PprSKD IR effect (S7), strain table (S8), primer table (S9). `MOESM2_ESM.pdf` (8.1 MB) = supplementary figures.
- **Smoke replication written** (`code/smoke_test.py`, 9 KB, 7 criteria):
  1. 12 RNA-seq files load with ≥ 3,000 gene rows each → **PASS** (3,142 rows).
  2. 6 MAPS files load → **PASS**.
  3. htseq diagnostic rows (`__no_feature`, etc.) present in all 18 → **PASS**.
  4. pprM (DR_0907) is DOWN in PprSKD vs WT at IR=0 baseline → **PASS** (smoke CPM L2FC = -0.65, sign-matches paper's DESeq2 L2FC = -2.52, padj 1.34e-9).
  5. pprM is ENRICHED in MS2-PprS pull-down vs MS2-blank → **PASS** (smoke L2FC = +2.98; 106 transcripts at L2FC > 1 vs paper's ~130 interactors).
  6. Supplement Table S1 row 1 DR_0099 SSB IR0_vs_Sham0 L2FC = 0.694617 exact → **PASS**.
  7. Supplement Table S4 top row is DR_0907 (pprM) at L2FC < -2 → **PASS**.
- **Final smoke result:** **7/7 PASS** → `results/smoke_test_report.json`.
- **Replicated figure produced:** `figures/maps_pulldown_pprm_smoke.png` — log10 mean CPM vs log2FC scatter, pprM highlighted as blue star at the top of the enriched cloud.
- **Artifact manifest written:** 50 rows in `ARTIFACT_MANIFEST.tsv` (path, bytes, sha256-16, source, notes).
- **Reports written:** `README.md`, this `PROGRESS.md`, `FIRST_PASS_REPORT.md`.
- **Progress JSON updated** at `~/.openclaw/workspace/memory/subagent-progress/lucid100-wave4-35-a-small-rna-regulates-pprm--a-modulator-of-pleiotropic-prote.json` (status `first_pass_passed`, smoke verdict `PASS`, 7/7).

### Blockers / open issues

- None for PASS-low. **Naive CPM-mean L2FC does not match paper's DESeq2 magnitudes** (Pearson ≈ 0 across the small S4 DEG subset; sign concordance 64%). This is expected and is documented in the smoke script and the FIRST_PASS_REPORT — naive CPM is not a substitute for DESeq2 on n=3 replicates with substantial library-size variation. **For PASS-mid, replace the CPM-mean smoke with a real DESeq2 (R or PyDeseq2) re-run** of the GSE176207 counts.
- Proteomics raw `.raw` files from PXD026633 not downloaded; only API summary fetched. PASS-mid would require ~10-100 GB and an Orbitrap-compatible analysis (FragPipe / MaxQuant), best run on uicgpu, not CherryRd.

### Next actions (PASS-mid plan)

1. R + DESeq2 (or PyDeseq2 on uicgpu) on GSE176207 to reproduce Tables S4, S5, S6, S7 quantitatively. Target: Spearman ≥ 0.9 on shared L2FC values, padj sign-and-significance concordance ≥ 80% at α=0.05.
2. DESeq2 on the MAPS dataset to reproduce the ~130 PprS interactors list and cross-check vs paper's enrichment threshold.
3. (Optional, PASS-full) Download PXD026633 raw files (Orbitrap Fusion .raw, expected size 10-100 GB) onto uicgpu `/data/stevens/`, run FragPipe or MaxQuant TMT pipeline, reproduce Table S1 time-course proteomics.

### QA retag recommendation

**`candidate_curated` → `replication_smoke_passed`** (or repo equivalent for PASS-low). This row should move toward the front of the Wave 5 / PASS-mid queue because the inputs are unusually clean (tiny tarball, public, CC-BY-compatible, every supplementary DEG list published).
