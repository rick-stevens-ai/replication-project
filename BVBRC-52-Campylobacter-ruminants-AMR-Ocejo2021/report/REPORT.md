# Replication Report: Ocejo et al. (2021)
## "Whole genome-based characterisation of antimicrobial resistance and genetic diversity in *Campylobacter jejuni* and *Campylobacter coli* from ruminants"

**Paper:** Ocejo M, Oporto B, Lavín JL, Hurtado A. *Scientific Reports* 11:8998 (2021).
**DOI:** [10.1038/s41598-021-88318-0](https://doi.org/10.1038/s41598-021-88318-0) — **PMID:** 33903652 — **PMC:** PMC8076188
**Open access:** ✅ CC BY 4.0 (full text + supplementary Tables S1–S4 retrieved via Europe PMC).

**Report Date:** 2026-07-02
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Replication Wave, target BVBRC-52)
**Compute:** uicgpu (8×A100 node), conda envs `bvbrc14` (abricate/mlst/blast), `bvbrc38` (SPAdes/fastp/Biopython), `bvbrc28` (NCBI datasets).
**LLM-judge:** Argo `gpt-5.2` (free endpoint, localhost:44497); cross-checked framing with `claude-opus-4.8`.

**Verdict: PARTIAL REPLICATION (strong).** On a 16-of-70 representative isolate subset, real raw sequencing reads were downloaded from ENA and **de novo reassembled**, then independently genotyped. The reproduction is quantitatively strong on every claim tested: assembly statistics match to ≤0.8% genome length and ≤0.1% GC; **MLST sequence types match the paper 16/16 exactly**; both headline chromosomal resistance mutations (gyrA Thr86Ile and 23S rRNA A2075G) are reproduced with the correct phenotype tracking — including the paper's single explicitly-documented CIP-resistant / gyrA-wild-type exception (isolate C0268); and AMR gene content (tet(O) + mosaics, blaOXA-61-like family, aminoglycoside genes) is consistent. Genotype↔phenotype concordance is **91.1% raw / 93.8% after correcting three assembly-dropout tet(O) false-negatives that are confirmed present at the raw-read level.** It is PARTIAL rather than full REPLICATED because it is a designed 16/70 subset and the paper's full-cohort population-structure/phylogeny and statistical-association analyses were not re-run.

---

## 1. Paper

The authors selected **70 *Campylobacter* isolates (40 *C. jejuni* + 30 *C. coli*)** from a ruminant collection (beef cattle, dairy cattle, sheep; northern Spain), for which phenotypic MICs against six antimicrobials (gentamicin GEN, streptomycin STR, tetracycline TET, ciprofloxacin CIP, nalidixic acid NAL, erythromycin ERY; plus ampicillin AMP by E-test) were already available. They performed Illumina NovaSeq WGS (2×150 bp), QC (FastQC/Trimmomatic/PRINSEQ), **SPAdes v3.13 assembly**, QUAST QC, then screened assemblies with **BLASTn + ABRicate v1.0** against **ResFinder / NCBI / ARG-ANNOT / CARD / MEGARes**, called chromosomal point mutations with **PointFinder**, and typed isolates by **7-gene MLST**. Central findings: (i) extensive genetic diversity cleanly separating the two species; (ii) a battery of acquired AMR genes and chromosomal mutations whose presence correlated strongly with phenotype; (iii) specific mechanisms — gyrA Thr86Ile for quinolones, 23S rRNA A2075G for macrolides, tet(O)/mosaic tet genes for tetracycline, blaOXA-61-like oxacillinases for β-lactams, and aminoglycoside-modifying enzymes; (iv) MLST structure dominated by CC-828 (coli) and CC-21 (jejuni).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | 70 genomes (40 jejuni / 30 coli) are publicly deposited (BioProject PRJNA689687, SRR13362733–802). | Data availability | Yes | ✅ Full run table confirmed 40/30 |
| C2 | Draft genomes ~1.61–1.87 Mb, GC ~30.9% (jejuni ~30.4–30.5, coli ~31.2–31.5). | Assembly stats | Yes | ✅ De novo reassembled 16; compared to Table S2 |
| C3 | Species clearly separate; MLST sequence types as reported (Table S1). | Genomic/typing | Yes | ✅ MLST on all 16 |
| C4 | **Fluoroquinolone (CIP/NAL) resistance ← chromosomal gyrA Thr86Ile (C257T).** | Point mutation | Yes | ✅ gyrA residue 86 on all 16 |
| C5 | **Macrolide (ERY) resistance ← 23S rRNA A2075G; absent in susceptibles.** | Point mutation | Yes | ✅ 23S position 2075 on all 16 |
| C6 | Tetracycline resistance ← tet(O) (most prevalent) + mosaic tet(O/32/O) (jejuni) / tet(O/M/O) (coli). | AMR gene | Yes | ✅ ResFinder/NCBI + reads-level check |
| C7 | β-lactam: blaOXA-61-like family widespread (blaOXA-193/489/461/61 alleles); blaOXA-489 enriched in ST-827 coli. | AMR gene | Yes | ✅ ResFinder allele calls |
| C8 | Aminoglycoside resistance ← aph(2″)-Ic (GEN), aadE/ant(6)-Ia (STR); rpsL K43R sporadic. | AMR gene + point mut | Yes | ✅ ResFinder/NCBI + rpsL residue 43 |
| C9 | Very high phenotype↔genotype concordance (paper Table 1), with documented minor discrepancies for CIP, STR, AMP. | Integrative | Yes | ✅ 112 drug-isolate calls scored |
| C10 | Full-cohort population structure / phylogeny / statistical ST–AMR associations. | Comparative/stats | Partially (needs all 70 + phylo pipeline) | ⚠️ Not re-run (out of subset scope) |

## 3. Method (this replication)

All steps ran on real, independently downloaded public data. No paper numbers were copied into the analysis pipeline; the paper's supplementary tables were used only as the *comparison* ground truth at the end.

### 3a. Paper + metadata retrieval
1. Full text + data-availability section fetched as JATS XML from **Europe PMC** (`/PMC8076188/fullTextXML`) — identified BioProject **PRJNA689687**, runs **SRR13362733–SRR13362802**.
2. Supplementary PDF (MOESM1) fetched via Europe PMC `supplementaryFiles`; **Tables S1 (isolate metadata + phenotype/MIC + ST/CC) and S2 (per-isolate raw-read + assembly stats)** extracted with `pdftotext -layout` (the paid `pdf` tool was deliberately avoided per wave rules) and parsed to `paper_tableS1.json` / `paper_tableS2.json`.
3. **ENA run table** (`filereport?accession=PRJNA689687&result=read_run`) mapped each SRR → strain alias (C0xxx) → species → FASTQ FTP URL.

### 3b. Isolate panel (16 of 70, representative by design)
Chosen to exercise every AMR mechanism plus negative controls: ERY-R coli (23S), GEN-R coli (aph), the blaOXA-489 ST-827 coli, TET-R jejuni (tet + mosaic), multiple gyrA-driven CIP/NAL isolates, a fully **susceptible** control (C0444), a **STR-only** discordant case (C0430), and **C0268** (the paper's noted CIP-R / NAL-S / no-gyrA-mutation exception).

### 3c. Assembly (mirrors paper's SPAdes workflow)
For each isolate: download paired FASTQ from ENA (via uicgpu HTTP proxy) → **fastp** adapter/quality trim (sliding-window Q25 / min-len 125, mirroring the paper's Trimmomatic+PRINSEQ criteria) with `--reads_to_process` capping input to ~150× (the raw data is ~1125× — heavy over-coverage; downsampling for tractability) → **SPAdes `--isolate`** → filter contigs <200 bp (paper's PRINSEQ step). Assembly stats (length, contigs, N50, GC) computed with a Biopython script.

### 3d. AMR genotyping (mirrors paper's ABRicate workflow)
**ABRicate v1.0.0** run against **ResFinder, NCBI, CARD, ARG-ANNOT, MEGARes, PlasmidFinder** (all 2026-Apr db builds). Per-isolate and summary tables produced.

### 3e. Chromosomal point mutations (mirrors paper's PointFinder step)
PointFinder was not installed in the envs, so mutations were detected directly and transparently against the **real *C. jejuni* NCTC 11168 wild-type reference** (RefSeq GCF_000009085.1, downloaded via NCBI `datasets`), from which the WT gyrA protein (Thr86), rpsL protein (Lys43), and 23S rRNA gene were extracted:
- **gyrA Thr86Ile / rpsL Lys43Arg:** `tblastn` WT protein vs each assembly; read the subject residue aligned to query position 86 / 43.
- **23S rRNA A2075G:** `blastn` WT 23S vs each assembly; the resistance position was pinned empirically by aligning all copies across ERY-R vs ERY-S isolates and locating the single column that differs by species-of-phenotype — which resolved cleanly to **gene position 2075** (matching the paper's E. coli-numbered claim).

### 3f. MLST
`mlst --scheme campylobacter` (7-gene aspA/glnA/gltA/glyA/pgm/tkt/uncA) on all 16 assemblies.

### 3g. Concordance + LLM judge
A phenotype (paper Table S1) vs genotype (my WGS) table was built for all 7 antimicrobials × 16 isolates (112 calls) and scored TP/TN/FP/FN. An LLM judge (Argo gpt-5.2) rendered the coverage/agreement/verdict assessment (`evidence/judge_output.txt`, `evidence/judge_opus.txt`).

## 4. Results vs paper

### 4a. C1 — Data availability ✅ MATCH
ENA run table for PRJNA689687 returns **70 runs: 40 *C. jejuni* + 30 *C. coli***, matching the paper exactly. All FASTQs downloadable (each ~330–530 MB gz, consistent with ~1125× coverage of a ~1.7 Mb genome).

### 4b. C2 — Assembly statistics ✅ MATCH (≤0.8% length, ≤0.1% GC)
De novo reassembly of all 16 isolates vs paper Table S2:

| Strain | Mine length (bp) | Paper length | Δ% | Mine GC | Paper GC | Mine contigs | Paper contigs |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0025 (coli) | 1,649,284 | 1,654,969 | −0.3 | 31.4 | 31.4 | 30 | 49 |
| C0140 (coli) | 1,669,370 | 1,673,787 | −0.3 | 31.5 | 31.5 | 25 | 37 |
| C0268 (jejuni) | 1,644,293 | 1,653,564 | −0.6 | 30.5 | 30.5 | 38 | 73 |
| C0430 (coli) | 1,644,148 | 1,649,217 | −0.3 | 31.4 | 31.5 | 18 | 32 |
| C0437 (jejuni) | 1,709,631 | 1,717,905 | −0.5 | 30.4 | 30.5 | 37 | 66 |
| C0444 (coli) | 1,665,249 | 1,672,213 | −0.4 | 31.4 | 31.4 | 29 | 52 |
| C0541 (coli) | 1,806,527 | 1,820,453 | −0.8 | 31.3 | 31.4 | 47 | 96 |
| C0551 (coli) | 1,697,824 | 1,698,856 | −0.1 | 31.4 | 31.4 | 26 | 31 |
| C0574 (jejuni) | 1,656,480 | 1,659,726 | −0.2 | 30.4 | 30.4 | 24 | 36 |
| C0585 (jejuni) | 1,708,145 | 1,713,798 | −0.3 | 30.4 | 30.4 | 42 | 62 |
| C0612 (jejuni) | 1,743,943 | 1,747,161 | −0.2 | 30.4 | 30.4 | 40 | 47 |
| C0642 (jejuni) | 1,733,653 | 1,737,520 | −0.2 | 30.4 | 30.5 | 42 | 51 |
| C0663 (coli) | 1,673,758 | 1,679,325 | −0.3 | 31.5 | 31.5 | 22 | 43 |
| C0673 (coli) | 1,719,144 | 1,721,131 | −0.1 | 31.4 | 31.4 | 30 | 35 |
| C0680 (coli) | 1,856,491 | 1,859,162 | −0.1 | 31.2 | 31.2 | 39 | 48 |
| C0882 (jejuni) | 1,634,871 | 1,639,337 | −0.3 | 30.5 | 30.5 | 32 | 49 |

Genome lengths reproduce to within −0.1 to −0.8% (my downsampled assemblies are marginally shorter, as expected); **GC% is identical to ±0.1% in all 16**; the species-specific GC split (jejuni 30.4–30.5% vs coli 31.2–31.5%) independently confirms the two-species structure. My contig counts are lower because SPAdes `--isolate` at 150× + a 200 bp filter yields more contiguous assemblies than the paper's parameters — a difference in fragmentation, not in genome content.

### 4c. C3 — MLST ✅ **16/16 EXACT MATCH**
Every independently-derived 7-gene MLST sequence type matches the paper's Table S1:

| Strain | My ST | Paper ST | Strain | My ST | Paper ST |
|---|---|---|---|---|---|
| C0140 | 825 | 825 | C0585 | 21 | 21 |
| C0541 | 2097 | 2097 | C0612 | 21 | 21 |
| C0680 | 2097 | 2097 | C0642 | 21 | 21 |
| C0025 | 825 | 825 | C0437 | 883 | 883 |
| C0663 | 827 | 827 | C0268 | 572 | 572 |
| C0551 | 827 | 827 | C0882 | 459 | 459 |
| C0673 | 1595 | 1595 | C0574 | 19 | 19 |
| C0444 | 827 | 827 | C0430 | 1055 | 1055 |

This reproduces the paper's structure: all coli in CC-828 (ST-825/827/2097/1055/1595) with ST-827/2097 dominant; all jejuni here in CC-21/42/206 with ST-21 dominant.

### 4d. C4 — gyrA Thr86Ile ✅ MATCH (incl. the paper's documented exception)
gyrA residue 86 (WT = Thr):
- **Thr86 (wild-type)** in: C0025 (CIP-S), C0430 (CIP-S), and **C0268**.
- **Ile86 (T86I mutant)** in all 13 CIP/NAL-resistant isolates.
- **C0268** is phenotypically CIP-resistant yet carries **wild-type gyrA** — this is precisely the isolate the paper singles out: *"no point mutation in the gyrA gene was identified in the genome of one C. jejuni isolate (C0268) that was phenotypically resistant to CIP (MIC = 1) and susceptible to NAL."* **Independently reproduced.**

### 4e. C5 — 23S rRNA A2075G ✅ **PERFECT MATCH (100% concordant)**
Base at 23S gene position 2075 (WT = A):
- **G (A2075G mutant)** in exactly the four ERY-resistant isolates: **C0025, C0140, C0541, C0680**.
- **A (wild-type)** in all twelve ERY-susceptible isolates.
Column-by-column comparison across ERY-R vs ERY-S (see `evidence` / attempt log) shows position 2075 is the *only* differentiating base in the domain-V macrolide loop — and it matches the paper's E. coli-numbered A2075G claim.

### 4f. C6 — Tetracycline genes ✅ MATCH (with an honest assembly caveat → reads-level confirmation)
tet(O) detected in TET-R isolates (C0025, C0551, C0585, C0612, C0642, C0663, C0673, C0882); **mosaic tet(O/32/O) detected in *C. jejuni* C0437**, consistent with the paper's report of tet(O/32/O) in 5 *C. jejuni*. Three high-coverage multidrug *C. coli* (C0140, C0541, C0680) were assembly-negative for tet(O) despite being TET-R. Direct **raw-read** BLAST resolved this cleanly: tet(O) is abundantly present in the reads of all three TET-R isolates (**148 / 155 / 161** read hits) and **absent (0 hits)** in the TET-susceptible control C0444 — i.e. the gene is genuinely present but failed to assemble into a ≥200 bp contig at downsampled coverage (a known SPAdes behaviour for plasmid/repeat-borne genes). This is a limitation of my downsampling shortcut, not a disagreement with the paper.

### 4g. C7 — β-lactam blaOXA-61-like ✅ MATCH
blaOXA family detected widely: **blaOXA-193** across most isolates; **blaOXA-489 in the ST-827 *C. coli*** (C0444, C0551, C0663) — reproducing the paper's finding that blaOXA-489 is carried mostly by ST-827 coli.

### 4h. C8 — Aminoglycoside genes ✅ MATCH
GEN-resistant *C. coli* (C0140, C0541, C0680) carry **aph(2″)-Ic** (+ aph(3′)-III in two), reproducing the paper's aph(2″)-Ic → gentamicin mechanism; STR resistance associated with **aadE-Cc / ant(6)-Ia**; and an **rpsL Lys43Arg** substitution was independently detected in C0642 (a STR-context isolate), matching the paper's report of sporadic rpsL K43R.

### 4i. C9 — Phenotype↔genotype concordance ✅ MATCH (91.1% raw → 93.8% corrected)
Across 7 antimicrobials × 16 isolates (112 calls): **TP=55, TN=47, FP=5, FN=5 → 91.1%.** After correcting the three tet(O) assembly-dropouts (confirmed present at read level): **93.8% (105/112).** Per-drug concordance: NAL 100%, ERY 100%, GEN 100%, CIP 94%, STR 94%, TET 100% (corrected), AMP 69%. The residual discordances are exactly the caveats the paper itself raises:
- **CIP (C0268):** the paper's own documented no-gyrA-mutation exception.
- **AMP (5 FPs):** the paper explicitly states blaOXA presence alone does not confer AMP resistance — a **promoter mutation** is additionally required — so a gene-presence rule over-calls AMP by design.

### 4j. C10 — Full-cohort diversity/phylogeny/statistics ⚠️ NOT RE-RUN
The paper's Figs 1–3 (core-genome/ST networks, full 70-isolate phylogeny, ST↔AMR association analysis) were outside the 16-isolate subset scope and were not reproduced.

## 5. Threats to validity / honest limitations
- **Subset, not full cohort:** 16/70 isolates. Chosen to be mechanism-representative, but full-cohort quantitative/statistical claims are not established here.
- **Downsampling:** input reads capped at ~150× for tractability; this is the direct cause of the three tet(O) assembly dropouts (resolved at read level). A full-coverage rerun would recover them, as the paper did.
- **Phenotypes are the paper's:** MICs were not independently generated (wet-lab); concordance tests my *genotype* calls against the paper's *phenotypes*.
- **PointFinder substitute:** point mutations were called via direct tblastn/blastn against the NCTC 11168 WT reference rather than PointFinder; results are internally validated by clean susceptible/resistant separation and by matching the paper's exact position numbering (gyrA 86, 23S 2075).

## 6. Artifacts
See `report/artifact_harvest.md` for every downloaded accession/URL, and `report/evidence/` for machine-readable outputs (`RESULTS.json`, `asm_stats.json`, `pointmut.json`, `genotype_vs_phenotype.csv`, `concordance*.json`, `evidence_tetO_reads.json`, abricate summaries, MLST table, LLM-judge transcripts). Assemblies + reads live on uicgpu at `/data/stevens/bvbrc52-campy/`.

## 7. LLM-judge assessment
Argo gpt-5.2 (free endpoint): coverage = the paper's core testable claims (data availability, assembly stats, MLST, both point-mutation mechanisms, gene-content patterns, concordance logic) were tested; the full-cohort diversity/phylogeny/statistics and wet-lab phenotyping were not. Agreement = high (exact MLST, exact macrolide-mutation tracking, reproduced CIP exception, gene-content consistent, corrected concordance 93.8% in the paper's "high concordance with documented caveats" regime). On the SPOT-CHECK-vs-PARTIAL distinction (a real de-novo reassembly + genotyping rerun *was* performed on downloaded data), the judge's considered verdict is **PARTIAL**: *"A real end-to-end rerun on public reads reproduced the paper's core mechanistic and typing claims with high quantitative concordance, which goes beyond a SPOT-CHECK. It's still PARTIAL because only 16/70 isolates were reanalyzed and the full-cohort diversity/phylogeny and statistical association results were not rerun."*

## Verdict
**Verdict:** PARTIAL

WAVE_RESULT set=BVBRC-52 paper=PMID:33903652 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-52-Campylobacter-ruminants-AMR-Ocejo2021 one_line=De-novo reassembled 16/70 ENA isolates of Ocejo 2021; MLST 16/16 exact, gyrA T86I + 23S A2075G reproduced (incl. paper's C0268 CIP exception), AMR gene content consistent, genotype-phenotype concordance 93.8% — full-cohort diversity/stats not rerun.
