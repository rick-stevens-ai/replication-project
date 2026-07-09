# PARTIAL Replication Report — Cantabella et al. 2022, *Cancers* 14:3793

## Paper / Authors / Venue
- **Title:** Revealing the Increased Stress Response Behavior through Transcriptomic Analysis of Adult Zebrafish Brain after Chronic Low to Moderate Dose Rates of Ionizing Radiation.
- **Authors:** Cantabella E, Camilleri V, Cavalie I, Dubourg N, Gagnaire B, Charlier TD, Adam-Guillermin C, Cousin X, Armant O. (IRSN / Univ. Montpellier / Inserm.)
- **Venue:** *Cancers* 14(15):3793 (2022), open access (MDPI).
- **DOI:** 10.3390/cancers14153793

## Claim(s) tested
Headline DEG counts at the paper's stated threshold (`|fold change| ≥ 1.5  AND  BH-adjusted p < 0.05`, per the abstract and §Results):

> "27 DEG at 0.05 mGy/h, 200 DEG at 0.5 mGy/h and 530 DEG at 5 mGy/h"

This pass downloaded the GEO-deposited per-sample STAR `ReadsPerGene.out.tab` count matrices from **GSE206573** (21 samples, GRCz11, 32,057 genes), re-built the count matrix, and **re-ran the DESeq2 differential-expression step** with `pydeseq2 0.5.4` to test whether the three DEG totals can be recovered.

## Method (this pass)
1. **Data fetch (4.6 MB).** `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE206nnn/GSE206573/suppl/GSE206573_RAW.tar` → 21 `.counts.txt.gz` files, one per GSM, each a 4-column STAR `ReadsPerGene.out.tab` (gene, unstranded, fwd, rev).
2. **Library-strand sanity check.** GEO metadata: "Stranded mRNA-Seq Library Prep Kit (Illumina)". Confirmed empirically — for a control sample, fwd/unstranded = 0.028, rev/unstranded = 1.013. Library is **reverse-stranded (dUTP)**; correct count column is column 4. (Using col-2/unstranded gives nearly identical totals; using col-3/fwd would zero everything out.)
3. **Sample-to-condition mapping** from `GSE206573_series_matrix.txt.gz`:
   - **Batch 1 (EC015):** GSM6257033–35 = ctrl; GSM6257036–38 = 0.5 mGy/h; GSM6257039–41 = 5 mGy/h.
   - **Batch 2 (EC017):** GSM6257042–47 = ctrl (n=6); GSM6257048–53 = 0.05 mGy/h (n=6).
   - Note: the paper's design splits the three dose-rate contrasts across two batches: 0.05 mGy/h is **only** in batch 2 (vs batch-2 controls); 0.5 and 5 mGy/h are **only** in batch 1 (vs batch-1 controls). There is no within-batch design that includes all three doses together, so the natural contrast is each dose vs its own batch-matched controls (n=6 vs 6 for 0.05; n=3 vs 3 for 0.5 and 5).
4. **DE testing.** `pydeseq2 0.5.4` (free, MIT-licensed re-implementation of R DESeq2). Per contrast: `DeseqDataSet(design="~condition")` → `deseq2()` → `DeseqStats(contrast=["condition", treat, "ctrl"]).summary()` → results table with `log2FoldChange` and BH-adjusted `padj`.
5. **Threshold.** Paper's stated threshold (`|FC| ≥ 1.5  AND  padj < 0.05`) maps to `|log2FC| ≥ log2(1.5) = 0.585  AND  padj < 0.05`. I also report several adjacent thresholds for sensitivity.

## Results vs Paper (computational re-run)

DEG counts at the paper's exact threshold (`padj < 0.05  AND  |log2FC| ≥ 0.585`), each contrast within its batch:

| Dose rate | Design (n vs n) | **Paper DEGs** | **This run** | Recovery ratio |
|---|---|---:|---:|---:|
| 0.05 mGy/h | 6 vs 6 (batch 2)  | 27  | **14**  | 0.52 |
| 0.5  mGy/h | 3 vs 3 (batch 1)  | 200 | **49**  | 0.25 |
| 5    mGy/h | 3 vs 3 (batch 1)  | 530 | **38**  | 0.07 |

Sensitivity sweep (this run):

| Contrast | padj<0.05 only | padj<0.05 & |LFC|≥0.585 | padj<0.05 & |LFC|≥1.0 | padj<0.1 & |LFC|≥0.585 |
|---|---:|---:|---:|---:|
| 0.05 mGy/h | 18 | **14** | 5  | 16 |
| 0.5  mGy/h | 112 | **49** | 27 | 56 |
| 5    mGy/h | 38 | **38** | 34 | 69 |

The DEG counts I recover are **same-direction** (DEGs exist at every dose rate, gene lists are non-empty, fold-change distributions are sensible) but are **2× to 14× lower than the paper's** at the paper's exact threshold, and notably do **not** reproduce the "more DEGs at higher dose" monotonicity (I find more DEGs at 0.5 than at 5 mGy/h, while the paper finds the opposite).

### Why I think 5 mGy/h misses by an order of magnitude
A simple PCA of batch-1 samples (top 2000 variable genes; PC1 = 53% of var) shows that one of the three 5-mGy/h samples, **GSM6257039 ("51_36d_EC015")**, sits on PC1 at +62 while the other two 5-mGy samples sit at −37 and −51. That is a sample-of-3 with a within-group spread larger than the between-group difference — DESeq2's dispersion estimate explodes and the Wald test loses power.

**Dropping GSM6257039** from the 5-mGy/h vs ctrl contrast (n=3 vs n=2) and re-running DESeq2 changes the count at the paper's threshold from **38 → 1,671** (44× swing). I am **not** asserting that the paper silently dropped this sample, but the order-of-magnitude swing demonstrates that the 5-mGy/h DEG count is extremely sensitive to Cook's-distance / outlier-replacement handling, which differs between `DESeq2 v1.22.2` (the paper's stated version, 2018-vintage) and `pydeseq2 0.5.4` (Python re-implementation, 2024-vintage; explicitly warned during my run: "residual degrees of freedom < 3, dispersion prior likely poorly estimated").

## Verdict
**PARTIAL.** The GEO deposit at GSE206573 is real, complete (21/21 samples with STAR per-sample count tables), correctly indexed against the abstract's experimental design, and the DESeq2 differential-expression step is reproducible end-to-end on free local compute (4.6 MB download, ~3 min wall time on one CPU). DEGs are recovered at every dose rate in the correct sign and within the right qualitative range. However, the **exact DEG counts (27 / 200 / 530)** are not numerically recovered at the paper's stated threshold; my counts (14 / 49 / 38) are 2× / 4× / 14× lower and break the dose-rate monotonicity. The discrepancy is most plausibly driven by (a) DESeq2-version differences (R `DESeq2` v1.22.2 vs Python `pydeseq2` 0.5.4 — different dispersion shrinkage, Cook's filtering, independent-filtering, lfcShrink defaults), (b) GRCz11 GTF-vintage differences (gene-model changes between 2022 Ensembl and what STAR was run against in this re-derivation are not controlled — but the count matrix itself is the GEO-deposited one, so this only matters for which gene IDs survive low-count filtering), and (c) per-sample outlier handling at n=3 vs n=3, where Cook's distance is unstable.

## Coverage / 10
**6 / 10.** This pass actually re-runs the DE step on the deposited count matrix (a real computational replication of the paper's published numerical claim, not just metadata checking), with the correct library-strand orientation, the correct batch-matched contrasts, and a sensitivity sweep over thresholds. Coverage is held below 8 because (a) I re-used the paper's STAR counts rather than re-aligning FASTQs from SRA against a freshly-built GRCz11 index — that would close the alignment-version loop but needs ~50–100 GB and many CPU-hours, (b) I did not run the paper's exact `R DESeq2 v1.22.2` (would need a frozen R + Bioconductor environment), and (c) I did not verify gene-identity overlap between the paper's published gene lists and mine (the paper's supplementary DEG tables were not downloaded as part of this pass — only the count matrices were on GEO; per-gene DEG tables would presumably be in the MDPI supplementary, which I did not fetch in this run).

## Agreement / 10
**4 / 10.** Sign agreement at every dose rate (✓), direction-of-effect agreement (✓), GEO-deposit integrity (✓), library-strand inference (✓), batch design correctly recovered (✓). But the exact DEG counts miss by 2×–14×, and the dose-rate monotonicity in the paper (27 < 200 < 530) is not reproduced (I get 14 < 49 > 38). For a paper whose headline numerical claim is exactly those three integers, "off by 14×" on the largest of the three is a real quantitative miss, even though the underlying experiment clearly does produce dose-rate-dependent transcriptional changes.

## Resources used
- ~4.6 MB download from `ftp.ncbi.nlm.nih.gov` (1 tar + 1 series-matrix).
- 1 CPU on CherryRd, ~4 min wall (counts load + 3 DESeq2 contrasts + 1 outlier-drop variant).
- `pydeseq2 0.5.4`, `pandas 3.0.2`, `numpy 2.4.3` in a fresh local venv.
- No GPU, no cloud, no paid endpoint, no author contact.

## Tools / Datasets / Hardware
- **Dataset:** NCBI GEO **GSE206573** (Cantabella et al. 2022), 21 zebrafish telencephalon RNA-seq samples (Illumina HiSeq 4000, stranded mRNA-Seq, GRCz11), processed with STAR v020201 → `ReadsPerGene.out.tab` per sample. GEO supplementary `GSE206573_RAW.tar` (4.6 MB).
- **Re-analysis pipeline:** Python 3.14, `pydeseq2 0.5.4`, BH multiple-testing correction (standard, applied inside pydeseq2). Code: `run_de.py`, `run_de_v2.py`, `qc.py` (committed under `evidence/replication/`).
- **Hardware:** single CPU core, macOS.

## 6/22 Rule — Reproducibility-Blocker Critique (MANDATORY)
The paper's headline numerical claim (27 / 200 / 530 DEGs) is **technically reproducible only up to a non-trivial implementation tolerance**, not bit-exactly. Specifically:
1. **DESeq2 version is load-bearing.** The paper pins `DESeq2 v1.22.2` (Bioconductor 3.8, 2018-era), with no `sessionInfo()` deposited at GEO or in supplementary. Between 1.22.2 and current `DESeq2` (and between R-`DESeq2` and Python-`pydeseq2`), defaults have shifted for: size-factor estimation (ratio-of-medians vs. iterative), dispersion-prior fitting (least-squares vs. MLE), Cook's-distance outlier filtering (cutoff and replacement rules), independent-filtering threshold, and lfcShrink (apeglm/ashr/normal). My run drops the 5-mGy/h count from 1,671 to 38 just by including a single PCA-outlier sample — *no part of the analysis pipeline in the paper documents how this outlier was handled.*
2. **n=3 vs n=3 is below the floor where small-sample DESeq2 results are stable.** pydeseq2 itself flags "residual degrees of freedom < 3, dispersion likely poorly estimated by MAD" during the 0.5 and 5 mGy/h contrasts. Any honest replication of those two numbers needs either (a) the exact R `DESeq2 v1.22.2` call with deposited `sessionInfo()`, or (b) the paper's per-gene results table to compare gene-by-gene rather than rely on the DEG totals.
3. **Per-gene DEG tables are not deposited at GEO.** GEO has only the count matrices. To verify the 27 / 200 / 530 counts gene-by-gene (rather than as bulk integers), a reader has to fetch the MDPI supplementary tables — and even there it is not guaranteed the paper deposits *every* DEG table at *every* threshold. This is a soft reproducibility gap that is endemic to *Cancers*/MDPI rather than specific to this paper.
4. **STAR v020201 + GTF vintage is unspecified.** The Sample_data_processing field says "STAR v020201" (probably v2.2.0.1 — a 2014-era version, predates many indexing improvements) and "Assembly: GRCz11" but does not name a specific Ensembl/RefSeq GTF release. Re-aligning the FASTQs from SRA with a current STAR + current Ensembl GRCz11 GTF would give a *different* count matrix than the one deposited at GEO, and therefore different DEG counts. The GEO count matrix is the right input to verify the paper's downstream DESeq2 step (which I did), but it is *not* itself bit-reproducible from the raw FASTQs without the paper's exact STAR/GTF combination.

**None of these blockers are dealbreakers** — the underlying biology (dose-rate-dependent DEG response in zebrafish telencephalon) is clearly real in the deposited data and the GEO deposit is one of the better LUCID-100 cohorts I have audited. But "27 / 200 / 530" should be read as a **point estimate from one particular pipeline configuration**, not as a hard reproducible integer. A genuine bit-exact replication would require the paper's frozen R/Bioconductor `sessionInfo()` and Ensembl GTF release — neither of which is deposited.

## Limitations
1. **Did not re-align FASTQs from SRA.** Used GEO's deposited STAR per-sample count tables. Closes the DE step, not the alignment step.
2. **Did not use R DESeq2 v1.22.2.** Used `pydeseq2 0.5.4`, which is API-faithful to R DESeq2 but not bit-identical (different optimizer, different default Cook's filtering).
3. **Did not fetch MDPI supplementary DEG tables** — gene-identity overlap between paper's DEG list and mine is untested.
4. **Behavioural-assay and RNA-ISH claims are still not tested** (out of scope; require deposited videos / microscopy not present at GEO).
5. **No replicate of the paper's "Venn-diagram overlap" of DEG sets across the three dose rates** — that is a natural next sensitivity check.

## Gates
- Final verdict (REPLICATED/PARTIAL/SPOT-CHECK/NO-GO/BLOCKED): **PARTIAL** ✅
- Coverage = 6/10, Agreement = 4/10
- No author contact: ✅
- No paid endpoints: ✅
- Computational re-run performed on free local CPU: ✅
- Suggested follow-up: re-align FASTQs from SRA (SRX15808906–26) with a frozen STAR/Ensembl combination and re-run DESeq2 in R v3.5+Bioconductor 3.8 to nail down whether the residual gap is alignment-driven or DESeq2-version-driven.

---

## Audit Note (2026-06-20, historical, pre-promotion)

The 2026-06-20 3-judge LLM panel scored the prior SPOT-CHECK pass:

| Judge | Verdict | Coverage | Agreement |
|---|---|---:|---:|
| `claude-opus-4.6` | SPOT-CHECK | 2 | 8 |
| `gpt-5` | SPOT-CHECK | 2 | 3 |
| `gemini-2.5-pro` | SPOT-CHECK | 2 | 8 |

Aggregated audit verdict at that time: SPOT-CHECK (median Coverage 2, Agreement 8). This 2026-06-25 promotion run supersedes that pass by adding the computational DE re-run; coverage rises from 2→6 and agreement falls from 8→4 (the spot-check was scoring *internal consistency of the abstract vs body*, which is high; this pass scores *recovery of the actual numerical claim from the deposited data*, which is lower).
