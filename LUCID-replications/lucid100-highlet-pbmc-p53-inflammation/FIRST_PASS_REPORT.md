# FIRST_PASS_REPORT — LUCID Slot 53 (Wave 6)

**Paper:** Buset et al., *High-LET Carbon and Iron Ions Elicit a Prolonged and Amplified p53 Signaling and Inflammatory Response Compared to low-LET X-Rays in Human Peripheral Blood Mononuclear Cells*, **Frontiers in Oncology 11:768493 (2021)**. DOI 10.3389/fonc.2021.768493.
**Date:** 2026-06-09, America/Chicago.
**Subagent session:** `agent:main:subagent:0963c525-0e98-4d80-b1b0-06a610e73f03`.

---

## 1. Verdict

| Field | Value |
|---|---|
| First-pass replication feasibility | **GO** |
| Raw data publicly available? | **Yes** — ArrayExpress E-MTAB-3463 + E-MTAB-5761, both verified open (HTTP 200) |
| Author contact needed? | **No** |
| Paid endpoints needed? | **No** |
| Heavy compute on CherryRd? | **No** — defer to uicgpu (RMA on 76 CELs) |
| Smoke test on CherryRd | **PASS** — 6/6 CELs parsed as HuGene-1_0-st-v1 AGCC v1 |
| QA recommendation | **RETAG: B (candidate_curated) → A (replication-ready)** |

## 2. What the paper claims (replication targets)

1. **All DE genes (any radiation type vs sham) are up-regulated** at 1 Gy / 8 h.
2. **p53 dominates the regulatory signature** across all three radiation types (Enrichr TF analysis).
3. **Heavy ions enrich immune/inflammatory GO terms** that are not significant in the X-ray-only DE set.
4. **Carbon ions induce more transcript-variant changes** (alt splicing ANOVA in Partek).
5. **qPCR at 24 h shows higher fold-change for heavy ions** than X-rays on PCNA, GADD45A, RPS27L, ASTN2, NDUFAF6, FDXR, MAMDC4 ⇒ prolonged amplitude.
6. **One iron-arm donor has a distinct DNA-repair gene profile** (per-donor heatmap of DNA repair genes).
7. **γH2AX foci show more residual damage** with heavy ions than X-rays at later time points.

Replication scope realistically targetable from public data: **claims 1, 2, 3, 4, 6** (microarray-derived), with cross-check of claim 5 against the microarray 8 h timepoint (paper itself notes 8 h vs 24 h discrepancy is part of the message). Claims 5 (qPCR at 24 h) and 7 (γH2AX) require fresh experimental data and are out of scope here.

## 3. Artifacts harvested (already on disk)

```
/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-highlet-pbmc-p53-inflammation/
  ├── artifacts/
  │   ├── fonc-11-768493.pdf            (7,909,496 bytes; 30 pp)
  │   └── cel_sniff_output.txt          (smoke-test stdout, PASS)
  ├── data/
  │   ├── E-MTAB-3463.sdrf.txt          (23,801 B; 60 X-ray assays)
  │   ├── E-MTAB-3463.idf.txt           (5,168 B)
  │   ├── E-MTAB-5761.sdrf.txt          (6,951 B; 16 heavy-ion assays)
  │   ├── E-MTAB-5761.idf.txt           (6,031 B)
  │   ├── cel_urls.txt                  (76 CEL URLs + header)
  │   └── cel_subset/                   (6 CELs, ~67 MB, 1 per condition)
  └── scripts/
      ├── cel_header_sniff.py           (Python-only smoke parser)
      └── RUN_PLAN.md                   (uicgpu R + Bioconductor recipe)
```

Plus `MANIFEST.json`, `README.md`, `PROGRESS.md`, and a JSON progress record under `~/.openclaw/workspace/memory/subagent-progress/lucid53.json`.

## 4. Data-availability summary

### E-MTAB-3463 — *X-ray transcriptional response of PBMCs* (SCK-CEN)

- Platform: **Affymetrix HuGene-1_0-st-v1**
- 10 healthy donors × 3 doses {0, 0.1, 1.0 Gy} × 2 technical reps = **60 CELs**
- Factors balanced: 20 sham / 40 X-ray; 20 per dose level
- Direct CEL URL pattern: `https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/463/E-MTAB-3463/Files/SCK-CEN_Donor{N}_{dose}Gy_{rep}.CEL`

### E-MTAB-5761 — *High-LET (C, Fe) transcriptional response of PBMCs* (GSI)

- Platform: **Affymetrix HuGene-1_0-st-v1** (same as above ⇒ joint RMA viable)
- 4 carbon-ion donors + 4 iron-ion donors, each with paired {0 Gy sham, 1 Gy} at 8 h = **16 CELs**
- Direct CEL URL pattern: `https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/761/E-MTAB-5761/Files/{C,Fe}_{0,1}Gy_8H_D{N}.CEL`

Total raw payload: **76 CELs, ≈ 830 MB**. All open. No registration. No auth.

## 5. Smoke test (what we actually ran on CherryRd)

```
python3 scripts/cel_header_sniff.py data/cel_subset/*.CEL
```

Output (excerpt; full text in `artifacts/cel_sniff_output.txt`):

```
file                          | size_bytes | array_type        | ...
C_0Gy_8H_D1.CEL               | 11124975   | HuGene-1_0-st-v1  | ...
C_1Gy_8H_D1.CEL               | 11131127   | HuGene-1_0-st-v1  | ...
Fe_0Gy_8H_D1.CEL              | 11097283   | HuGene-1_0-st-v1  | ...
Fe_1Gy_8H_D1.CEL              | 11095467   | HuGene-1_0-st-v1  | ...
SCK-CEN_Donor1_0.0Gy_1.CEL    | 11103119   | HuGene-1_0-st-v1  | ...
SCK-CEN_Donor1_1.0Gy_1.CEL    | 11105475   | HuGene-1_0-st-v1  | ...

OK: all 6 CELs share array_type=HuGene-1_0-st-v1
```

**Significance:** the magic bytes confirm valid AGCC v1, and the
`affymetrix-array-type` header field confirms identical array design across
X-ray and heavy-ion experiments. That is exactly what the paper's Methods state
and what the joint analysis requires. The full RMA + limma pipeline therefore
has a clear, low-risk path on uicgpu.

(The probe-intensity matrix itself was deliberately *not* decoded here — that's
what Bioconductor `oligo::read.celfiles` + `rma()` is for, and that lives in
the run plan, not the smoke.)

## 6. Replication-quality DE / signature methods needed for full run

Per paper Methods (M&M):

- RMA on Partek (we substitute `oligo::rma` in R — equivalent algorithm: background-correct + quantile-norm + log2 + median-polish summarization)
- ANOVA with **dose, donor, time-point** as factors; FDR (Benjamini-Hochberg) at 0.05; optional |FC| ≥ 2
- Alternative-Splicing ANOVA (Partek) at FDR < 0.05 (limma `diffSplice` is the standard FOSS equivalent; results are platform-config-sensitive — flag as approximate)
- Venn comparison via Venny (any FOSS tool fine)
- **RRHO** via UCLA online tool (use `RRHO` Bioconductor package locally to avoid the web dep)
- **Enrichr** for TF + GO BP enrichment (`enrichR` R package wraps the same API)

All five steps are pure FOSS. See `scripts/RUN_PLAN.md` for the script skeleton.

## 7. Blockers / open items

1. **Supplementary Tables 1, 5, 6** (primer list; full DE up-gene lists per radiation; full GO enrichment results) are referenced in the Frontiers HTML at the `#supplementary-material` anchor but the direct download URLs are not exposed in the static HTML scrape. Pattern guesses against the standard Frontiers downloader returned 404. They are still freely accessible from the article page via a normal browser click. **Action:** if a hard cross-check of our DE/signature against the published gene lists is needed, fetch via the browser-automation skill — not blocking for the GO verdict.
2. **Heavy compute** (76-CEL RMA + DE + RRHO) must run on uicgpu, not CherryRd. Recipe is ready in `scripts/RUN_PLAN.md`; expected wall time under 15 minutes.
3. **No author contact** required — all data is open.

## 8. Next actions (recommended)

1. (uicgpu) Execute `scripts/RUN_PLAN.md` to produce `xray/carbon/iron` DE tables + 3-way Venn + RRHO + enrichR TF/GO panels.
2. (browser) Pull Frontiers supplementary tables for direct gene-list cross-check.
3. After step 1+2, write `REPORT.md` with side-by-side: our DE/signature vs paper claims 1–4 and 6.
4. Apply the QA retag in the LUCID master TSV: row 84 should move from `B / candidate_curated` to `A / replication-ready` (both raw accessions live, joint single-platform design, smoke PASS).

---

*Generated by subagent on 2026-06-09 CDT. Files referenced are deterministic and reproducible from `data/cel_urls.txt` + `scripts/`.*
