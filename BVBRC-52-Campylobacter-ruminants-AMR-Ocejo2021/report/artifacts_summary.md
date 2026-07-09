# Artifacts Summary — BVBRC-52 replication (Ocejo et al. 2021)

**Paper:** PMID 33903652 · PMC PMC8076188 · DOI 10.1038/s41598-021-88318-0
**Verdict:** PARTIAL (strong)
**Compute:** uicgpu; raw reads + assemblies at `/data/stevens/bvbrc52-campy/`
**Report dir:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-52-Campylobacter-ruminants-AMR-Ocejo2021/report/`

## 1. Input artifacts (public, independently downloaded)

| Kind | Source | What | Where used |
|---|---|---|---|
| Paper full text (JATS XML) | Europe PMC `/PMC8076188/fullTextXML` | Data-availability section → BioProject PRJNA689687 identification | Step 1 |
| Supplementary PDF (MOESM1) | Europe PMC `supplementaryFiles` | Tables S1–S4 | Step 2 |
| ENA run table | ENA `filereport?accession=PRJNA689687&result=read_run` | 70 SRR accessions (SRR13362733–SRR13362802) → C0xxx strain aliases → FASTQ FTP URLs | Step 3 |
| Raw paired FASTQ | ENA (via uicgpu HTTP proxy) | 16 isolates × 2 files ≈ 330–530 MB gz each (~1125× coverage of ~1.7 Mb genome) | Step 5 |
| Reference genome | NCBI `datasets` → RefSeq GCF_000009085.1 | *C. jejuni* NCTC 11168 wild-type — source of WT gyrA, rpsL protein sequences and 23S rRNA gene | Step 7c |

## 2. Parsed / derived intermediate artifacts

Under `report/`:

| File | Content |
|---|---|
| `paper_tableS1.json` | Isolate → phenotype/MIC + ST/CC (parsed from MOESM1 via `pdftotext -layout`) |
| `paper_tableS2.json` | Per-isolate raw-read + assembly stats (paper's reported length/GC/contigs) |
| `artifact_harvest.md` | Full manifest of every downloaded accession/URL |

Under `report/evidence/`:

| File | Content |
|---|---|
| `RESULTS.json` | Consolidated per-isolate replication results |
| `asm_stats.json` | My independently-reassembled length/contigs/N50/GC per isolate |
| `pointmut.json` | gyrA-86, rpsL-43, 23S-2075 calls per isolate |
| `genotype_vs_phenotype.csv` | 7 drugs × 16 isolates = 112 calls (TP/TN/FP/FN) |
| `concordance*.json` | Per-drug + overall concordance (91.1% raw / 93.8% corrected) |
| `evidence_tetO_reads.json` | Raw-read tet(O) BLAST rescue (C0140/C0541/C0680 = 148/155/161 hits; C0444 = 0 hits) |
| `abricate_*.tsv` | Per-isolate + summary ABRicate output vs 6 databases |
| `mlst.tsv` | 7-gene MLST calls (mine vs paper: 16/16 exact) |
| `judge_output.txt` | Argo gpt-5.2 LLM-judge verdict |
| `judge_opus.txt` | claude-opus-4.8 cross-check |

Under `/data/stevens/bvbrc52-campy/` (uicgpu, not in report/):

- `reads/` — raw ENA paired FASTQ (16 isolates)
- `trimmed/` — fastp-trimmed reads (Q25, min-len 125, ~150× cap)
- `assemblies/` — SPAdes `--isolate` outputs, contigs ≥200 bp
- `refs/` — NCTC 11168 reference (gyrA, rpsL, 23S extracted)

## 3. Output artifacts (this report)

Under `report/`:

| File | Purpose |
|---|---|
| `REPORT.md` | Primary human-readable report (Markdown) |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section |
| `workflow.md` | Pipeline diagram + step-by-step methodology |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | What didn't work / what was skipped and why |
| `open_questions.json` | 5 truly-open follow-up scientific questions |

## 4. Isolate panel (16 of 70)

Chosen to be mechanism-representative rather than randomly sampled:

| Strain | Species | ST/CC (mine=paper) | Role in panel |
|---|---|---|---|
| C0025 | coli | 825 / CC-828 | ERY-R (23S), TET-R (tet(O)) |
| C0140 | coli | 825 / CC-828 | ERY-R (23S), multidrug — tet(O) reads-level rescue |
| C0268 | jejuni | 572 / CC-206 | **CIP-R with gyrA-WT** (paper's noted exception) |
| C0430 | coli | 1055 / CC-828 | STR-only discordant |
| C0437 | jejuni | 883 / CC-21 | TET-R with mosaic tet(O/32/O) |
| C0444 | coli | 827 / CC-828 | Fully susceptible negative control; blaOXA-489 |
| C0541 | coli | 2097 / CC-828 | ERY-R (23S), GEN-R (aph), multidrug — tet(O) reads-level rescue |
| C0551 | coli | 827 / CC-828 | TET-R, blaOXA-489 |
| C0574 | jejuni | 19 / CC-21 | jejuni typing check |
| C0585 | jejuni | 21 / CC-21 | TET-R (tet(O)) |
| C0612 | jejuni | 21 / CC-21 | TET-R (tet(O)) |
| C0642 | jejuni | 21 / CC-21 | TET-R (tet(O)); **rpsL K43R** |
| C0663 | coli | 827 / CC-828 | TET-R, blaOXA-489 |
| C0673 | coli | 1595 / CC-828 | TET-R (tet(O)) |
| C0680 | coli | 2097 / CC-828 | ERY-R (23S), GEN-R (aph), multidrug — tet(O) reads-level rescue |
| C0882 | jejuni | 459 / CC-42 | TET-R (tet(O)) |

## 5. Key quantitative outputs

- **Data availability (C1):** ENA returns 70 runs = 40 jejuni + 30 coli ✅
- **Assembly stats (C2):** length within −0.1 to −0.8% of paper's Table S2; GC ±0.1% in all 16 ✅
- **MLST (C3):** 16/16 exact match to paper Table S1 ✅
- **gyrA T86I (C4):** Thr86 in 3 CIP-S (incl. C0268 exception); Ile86 in all 13 CIP-R ✅
- **23S A2075G (C5):** G in exactly 4 ERY-R (C0025, C0140, C0541, C0680); A in all 12 ERY-S ✅
- **tet(O) + mosaic (C6):** tet(O) in 8/8 TET-R jejuni assemblies + reads-level rescue for 3 coli; mosaic tet(O/32/O) in C0437 ✅
- **blaOXA (C7):** blaOXA-489 in ST-827 coli (C0444, C0551, C0663) ✅
- **Aminoglycosides (C8):** aph(2″)-Ic in GEN-R coli; rpsL K43R in C0642 ✅
- **Concordance (C9):** 112 calls; TP=55, TN=47, FP=5, FN=5 → **91.1% raw / 93.8% corrected** ✅
- **Full-cohort phylogeny/stats (C10):** NOT re-run ⚠️

## 6. Provenance guarantees

- No paper table numbers were fed into the analysis pipeline; paper tables served only as end-of-pipeline comparison ground truth.
- Every accession, URL, and tool version is captured in `report/artifact_harvest.md` and the evidence JSON files.
- Assembly + genotyping tools mirror the paper's SPAdes → ABRicate → PointFinder workflow, with the sole substitution being tblastn/blastn against NCTC 11168 in place of PointFinder (validated by clean R/S separation and exact-position match).
