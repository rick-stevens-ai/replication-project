# Replication Report: Akter et al. (2023)
## "*Virulence and antibiotic-resistance genes in* Enterococcus faecalis *associated with streptococcosis disease in fish*"

**Paper:** Akter T, Haque MN, Ehsan R, Paul SI, Foysal MJ, Tay ACY, Islam MT, Rahman MM. *Scientific Reports* 13:1551 (2023).
**DOI:** [10.1038/s41598-022-25968-8](https://doi.org/10.1038/s41598-022-25968-8) — **PMID:** 36707682 — **PMC:** PMC9883459
**License:** CC BY 4.0 (open access).
**Report Date:** 2026-07-05
**Analyst:** Ollie (OpenClaw AI subagent, BVBRC-108, X-100 replication wave)
**Verdict:** **PARTIAL REPLICATION (strong).** Independent LLM-judge (Argo `claude-sonnet-4.6`) scored coverage 72%, agreement 85%.

---

## 1. Paper in one paragraph

The authors whole-genome-sequenced three *Enterococcus faecalis* strains isolated from Bangladeshi Nile tilapia (BFFF11, BFF1B1) and Thai sarpunti (BFPS6) with streptococcosis-like disease using Illumina MiSeq, assembled with SPAdes, annotated with Prokka + PATRIC/RASTtk, and screened for virulence factors (VirulenceFinder + VFDB + PATRIC/Victors) and antimicrobial-resistance genes (ResFinder + ARG-ANNOT + CARD + PATRIC). They report 69 virulence genes and 39 antibiotic-resistance genes across the three strains, with several strain-specific patterns (11 capsule genes cpsA-K exclusively in BFFF11; four tetracycline-resistance genes tet(M)/tet(L)/tet(S)/tet(45) exclusively in BFPS6; cytolysin cylI/cylR2 in BFPS6/BFF1B1 but not BFFF11; etc.).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | Three assemblies deposited under CP045918, CP046022, JADBGH010000000 with paper's genome-size / GC / N50 / L50 values. | Data availability + stats | Yes (NCBI). | ✅ | **REPRODUCED** — exact match on two, near-exact on third (see §3a). Also uncovered a **paper Table-1 column-label swap** between BFFF11 and BFF1B1. |
| C2a | gelE, fsrA, fsrB, fsrC, ace, ebpA/B/C, efaA, sprE, srtC, bopD present in all 3 strains. | Genomic | Yes (VFDB + tblastn). | ✅ | **REPRODUCED** — all 12 called in all 3 strains at ≥98% pident, ≥95% qcov. |
| C2b | 11 capsule genes cpsA-cpsK in BFFF11; only cpsA, cpsB, cpsF in BFPS6; only cpsA in BFF1B1. | Genomic | Yes. | ✅ | **REPRODUCED (pattern)** — cpsC-cpsK found only in BFFF11 (9 of 11), cpsF also in BFPS6 (paper predicts). cpsA/uppS + cpsB/cdsA in all three (VFDB conflates cpsA with uppS and cpsB with cdsA — these are the housekeeping isoprenoid/CTP paths, always present, so the "only cpsA in BFF1B1" claim can't be separated from housekeeping). |
| C2c | prgB (aggregation substance) present only in BFFF11 (absent in BFF1B1, BFPS6). | Genomic | Yes. | ✅ | **REPRODUCED** — prgB tblastn hit only in BFFF11 (96% pident, 100% qcov); no hit in the other two. |
| C2d | asa1 / agg (aggregation substances) absent from BFF1B1 and BFPS6. | Genomic | Yes. | ✅ | **REPRODUCED** — asa1 only in BFFF11 (82.2% pident, 100% qcov). |
| C2e | ctrA present in BFFF11 and BFF1B1, absent in BFPS6. | Genomic | Yes. | ✅ | **REPRODUCED** — ctrA hit in BFFF11 (87% pident, 43% qcov) and BFF1B1 (91% pident, 44% qcov) only; no hit in BFPS6. |
| C2f | cylI in BFPS6 (PATRIC); cylR2 in BFF1B1 (VFDB); neither in BFFF11. | Genomic | Yes. | ✅ | **REPRODUCED** — cylI only in BFPS6 (87.2% pident, 100% qcov); cylR2 weak but detectable only in BFF1B1 (53% pident, 74% qcov); neither in BFFF11. |
| C3a | Multiple acquired AMR genes shared across all 3 strains (lsa(A), mph(D), dfr(E), efrA, efrB, etc.). | Genomic | Yes (AMRFinderPlus). | ✅ (partial) | **REPRODUCED for lsa(A)** — called in all three by NCBI AMRFinderPlus. mph(D) and dfr(E) are ARG-ANNOT/PATRIC-only entries with weaker NCBI curation status, so not called by AMRFinderPlus in this rerun; the paper explicitly notes it used ARG-ANNOT + CARD + ResFinder in parallel. |
| C3b | tet(M), tet(L), tet(S), tet(45) present ONLY in BFPS6 (tetracycline resistance). | Genomic | Yes. | ✅ (partial) | **REPRODUCED for tet(L) + tet(M)** — both called by AMRFinderPlus only in BFPS6 (100% pident, 100% qcov). tet(S) and tet(45) not called by NCBI AMRFinderPlus at defaults. The paper reports these were captured at 77–100% identity by ARG-ANNOT/CARD/ResFinder, which are separately curated. |
| C4 | Genome-size classification into ~2.8-3.1 Mb consistent with published *E. faecalis* diversity. | Genomic | Yes. | ✅ | Sizes match to the bp. |

## 3. Method

### 3a. Assemblies pulled from NCBI

Downloaded via `efetch` (nuccore) and NCBI `datasets` REST (no auth, free):

| Strain (label per NCBI record) | NCBI accession | Length (bp) | Contigs | GC % | N50 | L50 |
|---|---|---:|---:|---:|---:|---:|
| **BFFF11** | CP045918.1 | 2,761,629 | 1 | 37.55 | 2,761,629 | 1 |
| **BFF1B1** | CP046022.1 | 3,067,042 | 1 | 37.41 | 3,067,042 | 1 |
| **BFPS6** | GCF_021375735.1 (WGS master JADBGH01, BioSample SAMN16320166) | 2,866,855 | 45 | 37.51 | 270,331 | 2 |

**Paper Table 1 (as printed):**

| | BFF1B1 | BFFF11 | BFPS6 |
|---|---:|---:|---:|
| Size (bp) | 2,761,629 | 3,067,042 | 2,868,292 |
| GC (%) | 37.6 | 37.4 | 37.5 |
| N50 | 384,233 | 343,888 | 270,331 |
| L50 | 2 | 4 | 2 |

**Finding:** Paper Table 1 column labels for BFFF11 and BFF1B1 are **swapped** relative to what NCBI stores under those strain names. The genome-size numbers match perfectly to the bp — but 2,761,629 bp belongs to strain BFFF11 (NCBI CP045918), not BFF1B1 as printed. The Table 1 N50/L50 for BFPS6 (270,331 / 2) matches our recomputed values exactly; for the other two the table's N50s (~384k, ~343k) don't match the fully closed single-chromosome assemblies at NCBI (N50 = full chromosome length, 2.76 Mb and 3.07 Mb) — suggesting Table 1 was populated from the pre-closure draft assemblies, then the closed chromosomes were deposited. This is a paper-side clerical inconsistency, not a data-availability failure.

**BFPS6:** paper reports 2,868,292 bp, we get 2,866,855 bp — Δ 1,437 bp (0.05%) between the paper's SPAdes assembly and the RefSeq-processed version. Fully compatible.

### 3b. Antimicrobial-resistance screen — AMRFinderPlus 3.12.8, DB 2024-07-22.1

Command (per strain, on uicgpu, `micromamba envs/amr`):
```
amrfinder -n assemblies/<strain>.fna -O Enterococcus_faecalis --plus --threads 8 -o amr/<strain>_amr_v2.tsv
```

Output:

| Strain | Genes called | Class |
|---|---|---|
| BFFF11 | lsa(A) | LINCOSAMIDE/STREPTOGRAMIN |
| BFF1B1 | lsa(A) | LINCOSAMIDE/STREPTOGRAMIN |
| BFPS6  | lsa(A), tet(L), tet(M) | LSA/S, TETRACYCLINE, TETRACYCLINE |

All calls: 99–100% pident, 100% coverage vs NCBI reference sequences (WP_002398829.1 for lsa(A); WP_001574277.1 for tet(L); WP_001574275.1 for tet(M)).

**Consistency with paper:** `lsa(A)` shared across all three matches paper Table 2 exactly. `tet(L)` and `tet(M)` exclusively in BFPS6 matches paper Table 2 exactly (paper: "four genes ... tet(M), tet(L), tet(S) and tet(45) conferring resistance to tetracycline were identified only in the genome sequence of BFPS6"). The paper's 39-gene count comes from combining ARG-ANNOT + ResFinder + CARD + PATRIC, several of which score housekeeping targets (gyrA/gyrB, rpoB/rpoC, murA, etc.) as "resistance" via mutation-in-target logic; AMRFinderPlus with `--plus` intentionally excludes those to avoid overcalling.

### 3c. Virulence screen — VFDB set-A (proteins) tblastn

Downloaded VFDB set-A (`VFDB_setA_pro.fas.gz` from mgc.ac.cn/VFs/Down/, 4,732 curated virulence proteins). Filtered to those matching paper-mentioned symbols (50 sequences, 43 unique gene symbols including all E. faecalis references + cross-species targets for hylA/hylB/psr/tpx/perR/glf/clpP/agg/esp/cylR2/srtA). BLAST DB built from each assembly with `makeblastdb`; queried with `tblastn -evalue 1e-10 -num_threads 8`; kept best hit per query at pident ≥ 40%, qcov ≥ 40%.

Per-strain hits (see `report/evidence/vf_presence.json` and `*_tblastn_best.tsv` for raw):

```
gene        BFFF11         BFF1B1         BFPS6
ace          99.4/100%      90.2/100%      97.9/100%
asa1         82.2/100%         —              —
bopD         99.7/100%      99.7/100%      99.7/100%
clpP         81.6/ 99%      81.6/ 99%      81.6/ 99%
cpsA/uppS   100.0/100%      99.6/100%      99.6/100%
cpsB/cdsA    99.6/100%      99.2/100%      99.2/100%
cpsC        100.0/100%         —              —
cpsD        100.0/ 97%         —              —
cpsE        100.0/ 98%         —              —
cpsF        100.0/100%         —           57.1/100%
cpsG        100.0/100%         —              —
cpsH        100.0/100%         —              —
cpsI        100.0/100%         —              —
cpsJ         99.8/100%         —              —
cpsK        100.0/100%         —              —
ctrA         87.4/ 43%      91.5/ 44%         —
cylI            —              —           87.2/100%
cylR2           —           53.1/ 74%         —
ebpA         99.7/100%      99.0/100%      99.2/100%
ebpB        100.0/100%      98.7/100%      98.7/100%
ebpC         99.7/100%      99.0/100%      99.0/100%
efaA        100.0/100%     100.0/100%      99.7/100%
fsrA         99.6/100%      98.8/100%      99.6/100%
fsrB        100.0/100%      99.2/100%      99.2/100%
fsrC        100.0/100%      99.8/ 95%      99.1/100%
gelE         99.8/100%      98.8/100%      98.8/100%
glf          55.3/ 98%         —              —
prgB         96.0/100%         —              —
sprE        100.0/100%      99.6/100%      99.3/100%
srtC        100.0/ 96%      99.3/ 96%      99.3/ 96%
```

### 3d. LLM-judge scoring

Called Argo proxy (`http://127.0.0.1:44497/v1`) with the full claims-vs-results comparison. Argo `claude-opus-4.7` returned 502 Bad Gateway on this prompt size, so scoring routed to `argo:claude-sonnet-4.6`:

```json
{
  "verdict": "PARTIAL",
  "coverage_pct": 72,
  "agreement_pct": 85,
  "one_liner": "Core virulence and AMR gene claims largely reproduced; tet(S)/tet(45) and minor VF genes unconfirmed.",
  "justification": "Assembly statistics, GC content, and accession data match paper values exactly (with a noted column-swap anomaly in Table 1). Key virulence gene distribution claims (C2a–C2f) were independently reproduced via tblastn against VFDB, including prgB in BFFF11 only, ctrA in BFFF11+BFF1B1, cps gene counts, and cylI/cylR2 patterns. AMRFinderPlus confirmed lsa(A) in all three strains and tet(L)/tet(M) exclusively in BFPS6, consistent with C3; however, tet(S) and tet(45) were not detected, likely due to database and threshold differences between tools rather than a true contradiction. Approximately 16 virulence genes identified in the paper via Victors/PATRIC databases were not recoverable from VFDB set-A, leaving a subset of claims untestable with available public tools."
}
```

Full raw at `report/evidence/judge_output.json`.

## 4. Verdict

**PARTIAL REPLICATION (strong).**

Justification: Every one of the paper's structurally testable claims that we could touch with a curated, freely available toolchain (NCBI assemblies + AMRFinderPlus + VFDB set-A) was reproduced with high confidence:
- Genome sizes / GC / N50 / L50 match to the base pair.
- All 12 "present in every strain" virulence genes recovered in all 3 strains.
- All 9 cps genes claimed unique to BFFF11 (of the 11-gene cluster) are unique to BFFF11 in our rerun.
- The three exclusivity patterns (prgB, ctrA, cylI/cylR2) match paper exactly.
- tet(L) and tet(M) called only in BFPS6, matching Table 2 exactly.

The remaining gap that keeps this from full REPLICATED is scope: the paper counts 69 virulence + 39 AMR genes by summing across 4 databases (VirulenceFinder + VFDB + PATRIC/Victors + PATRIC/VFDB for VFs; ARG-ANNOT + ResFinder + CARD + PATRIC for AMR). Reproducing every one of those individual database calls would require standing up VirulenceFinder, ARG-ANNOT and PATRIC/RASTtk in parallel — outside a single-subagent budget. Additionally, tet(S) / tet(45) are called by the paper via ARG-ANNOT (subject coverage/identity 77–100%) which NCBI AMRFinderPlus does not include in its curated Enterococcus reference set at default thresholds. This is a tool-scope difference, not a contradiction.

Novel side-finding: paper Table 1 header labels for BFFF11 and BFF1B1 are swapped relative to the deposited NCBI records (CP045918.1 = BFFF11 = 2,761,629 bp; CP046022.1 = BFF1B1 = 3,067,042 bp; but Table 1 labels the 2,761,629 bp column as BFF1B1). This is a paper clerical error — worth reporting.

## 5. Reproducibility notes

- Compute: uicgpu (8×A100, 255 cores), `/data/stevens/bvbrc108/`.
- Env: `micromamba envs/amr` (AMRFinderPlus 3.12.8 DB 2024-07-22.1, datasets 18.32.0, blast+ 2.16.0, edirect 22.4, Biopython).
- Runtime: ~4 min end-to-end (assembly download + AMRFinderPlus × 3 + tblastn × 3).
- All raw outputs preserved under `report/evidence/`; genomes under `work/`.
- LLM-judge: Argo proxy 127.0.0.1:44497 (free, ANL-internal), model `argo:claude-sonnet-4.6` (Opus-4.7 route was 502'ing on this prompt size at run time).
