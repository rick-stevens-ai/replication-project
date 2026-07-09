# Workflow — BVBRC-52 replication of Ocejo et al. 2021

**Paper:** Ocejo M, Oporto B, Lavín JL, Hurtado A. *Scientific Reports* 11:8998 (2021). DOI 10.1038/s41598-021-88318-0 · PMID 33903652 · PMC PMC8076188.
**Verdict:** PARTIAL (strong).
**Compute:** uicgpu (8×A100). Envs: `bvbrc14` (abricate/mlst/blast), `bvbrc38` (SPAdes/fastp/Biopython), `bvbrc28` (NCBI datasets).
**LLM-judge:** Argo `gpt-5.2` (free `localhost:44497`); cross-check `claude-opus-4.8`.

## Pipeline

```
                     +-------------------------------+
                     |  1. Paper & metadata retrieval |
                     |  Europe PMC JATS + MOESM1 PDF  |
                     +---------------+----------------+
                                     |
                                     v
                     +-------------------------------+
                     |  2. Parse Tables S1 + S2      |
                     |  pdftotext -layout -> JSON     |
                     |  (paper_tableS1/S2.json)      |
                     +---------------+----------------+
                                     |
                                     v
                     +-------------------------------+
                     |  3. ENA run table             |
                     |  PRJNA689687 filereport       |
                     |  SRR13362733-802 -> C0xxx map |
                     +---------------+----------------+
                                     |
                                     v
                     +-------------------------------+
                     |  4. Panel selection: 16/70    |
                     |  mechanism-representative     |
                     |  + C0268 exception            |
                     +---------------+----------------+
                                     |
                                     v
              +----------------------+----------------------+
              |                                             |
              v                                             v
   +-----------------------+                    +-----------------------+
   | 5a. fastp trim Q25    |                    | 5b. Raw-read tet(O)   |
   |   min-len 125         |                    |   BLAST (rescue for   |
   |   cap ~150x           |                    |   C0140/C0541/C0680)  |
   +-----------+-----------+                    +-----------+-----------+
               |                                            |
               v                                            |
   +-----------------------+                                |
   | 6. SPAdes --isolate   |                                |
   |   contigs >= 200 bp   |                                |
   +-----------+-----------+                                |
               |                                            |
               v                                            |
        +------+-----------------------+---------------+    |
        |                              |               |    |
        v                              v               v    v
+---------------+          +-------------------+  +---------------------+
| 7a. Assembly  |          | 7b. ABRicate v1.0 |  | 7c. Point mutations |
|   stats via   |          |   6 databases     |  |   tblastn/blastn vs |
|   Biopython   |          |   ResFinder/NCBI  |  |   NCTC 11168 WT     |
|               |          |   CARD/ARG-ANNOT  |  |   (gyrA-86, rpsL-43,|
|               |          |   MEGARes/Plasmid |  |    23S-2075)        |
+-------+-------+          +---------+---------+  +----------+----------+
        |                            |                       |
        |                            v                       |
        |               +-------------------------+          |
        |               | 7d. MLST 7-gene         |          |
        |               |   scheme=campylobacter  |          |
        |               +-----------+-------------+          |
        |                           |                        |
        +-----------+---------------+-----------+------------+
                    |                           |
                    v                           v
        +-------------------------+  +-------------------------+
        | 8. Compare vs Table S2  |  | 9. Concordance table    |
        |   length/GC/contigs     |  |   phenotype (S1) vs     |
        |   Table S1 STs          |  |   genotype (mine)       |
        +-----------+-------------+  |   7 drugs x 16 isolates |
                    |                |   = 112 calls           |
                    |                +------------+------------+
                    |                             |
                    +--------------+--------------+
                                   v
                    +-------------------------------+
                    | 10. LLM judge (Argo gpt-5.2)  |
                    |     + opus-4.8 cross-check    |
                    +---------------+---------------+
                                    |
                                    v
                    +-------------------------------+
                    | 11. REPORT.md / REPORT.tex    |
                    |     verdict: PARTIAL          |
                    +-------------------------------+
```

## Step details

1. **Retrieval.** Europe PMC `/PMC8076188/fullTextXML` for data-availability section (identifies BioProject PRJNA689687, runs SRR13362733–SRR13362802). Supplementary MOESM1 PDF via `supplementaryFiles`.
2. **Parse S1/S2.** `pdftotext -layout` (paid `pdf` tool avoided per wave rules) → `paper_tableS1.json` (isolate → phenotype/MIC + ST/CC), `paper_tableS2.json` (per-isolate raw-read + assembly stats).
3. **ENA map.** `filereport?accession=PRJNA689687&result=read_run` → SRR → strain alias (C0xxx) → species → FASTQ FTP URL.
4. **Panel choice (16/70).** Mechanism-representative: ERY-R coli (23S), GEN-R coli (aph), blaOXA-489 ST-827 coli, TET-R jejuni (tet + mosaic), multiple gyrA-driven CIP/NAL isolates, susceptible control C0444, STR-only discordant C0430, and C0268 (paper's noted CIP-R / NAL-S / gyrA-WT exception).
5. **QC + downsample.** `fastp` sliding-window Q25, min-len 125 (mirrors paper's Trimmomatic+PRINSEQ criteria), `--reads_to_process` cap to ~150× (raw ~1125×; heavy over-coverage — downsampled for tractability). Raw-read tet(O) BLAST run in parallel to cover the known SPAdes assembly-dropout risk.
6. **Assembly.** SPAdes `--isolate` → filter contigs <200 bp (paper's PRINSEQ step).
7. **Downstream.**
   - **7a.** Biopython → length, contigs, N50, GC.
   - **7b.** ABRicate v1.0.0 vs ResFinder / NCBI / CARD / ARG-ANNOT / MEGARes / PlasmidFinder (2026-Apr builds).
   - **7c.** PointFinder not installed → substitute against real *C. jejuni* NCTC 11168 WT (RefSeq GCF_000009085.1, via NCBI `datasets`): `tblastn` WT protein vs each assembly for gyrA residue 86 and rpsL residue 43; `blastn` WT 23S vs each assembly with the resistance position pinned empirically by aligning all copies across ERY-R vs ERY-S — converged cleanly on position **2075**, matching the paper's E. coli-numbered A2075G claim.
   - **7d.** `mlst --scheme campylobacter` (aspA/glnA/gltA/glyA/pgm/tkt/uncA).
8. **Compare vs paper.** Length/GC/contigs vs Table S2; STs vs Table S1.
9. **Concordance.** 7 antimicrobials × 16 isolates = 112 phenotype/genotype calls scored TP/TN/FP/FN.
10. **LLM judge.** Argo gpt-5.2 renders coverage/agreement/verdict → `evidence/judge_output.txt`; cross-check `evidence/judge_opus.txt`.
11. **Reports.** `REPORT.md` + `REPORT.tex` (this dir).

## Reproducibility notes

- All inputs are **public data** (Europe PMC + ENA); no paper numbers were fed into the analysis pipeline (paper tables used only as comparison ground truth at the end).
- Raw reads + assemblies live on uicgpu at `/data/stevens/bvbrc52-campy/`.
- Machine-readable outputs in `report/evidence/`: `RESULTS.json`, `asm_stats.json`, `pointmut.json`, `genotype_vs_phenotype.csv`, `concordance*.json`, `evidence_tetO_reads.json`, abricate summaries, MLST table, LLM-judge transcripts.
- Downloaded accession/URL manifest: `report/artifact_harvest.md`.

## Limitations traceable to workflow choices

- **150× downsampling** (step 5): directly caused three tet(O) assembly dropouts (C0140, C0541, C0680); resolved by parallel raw-read BLAST (step 5b). Assembly-only concordance 91.1%; reads-corrected 93.8%.
- **PointFinder substitute** (step 7c): validated by clean R/S separation + exact-position match to paper, but not tool-identical.
- **Subset scope** (step 4): 16/70 isolates. Full-cohort phylogeny/statistics (paper Figs 1–3) not re-run.
- **Paper's phenotypes**: MICs not independently generated wet-lab; concordance = my-genotype vs paper-phenotype.
