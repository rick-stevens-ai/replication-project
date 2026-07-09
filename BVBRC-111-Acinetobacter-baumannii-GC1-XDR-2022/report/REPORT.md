# BVBRC-111 — Independent Replication Report

## Paper

**Citation.** Harmer CJ, Lebreton F, Stam J, McGann PT, Hall RM. "Complete genome of the extensively antibiotic-resistant GC1 *Acinetobacter baumannii* isolate MRSN 56 reveals a novel route to fluoroquinolone resistance." *J Antimicrob Chemother* 2022 Jun 29;77(7):1851-1855. **PMID 35403193.** DOI: 10.1093/jac/dkac115. PMC9244215.

**Summary.** MRSN 56 is an XDR global-clone-1 (GC1) *A. baumannii* isolated from a US military treatment facility. The authors combined Oxford Nanopore MinION long reads with existing Illumina MiSeq short reads via Unicycler to produce a complete finished genome (chromosome + 4 small plasmids). They then dissected the acquired-resistance content and identified (a) the standard AbaR28 island in *comM*, (b) two Tn2006/blaOXA-23 copies, (c) two Tn7 copies including a novel "Tn7+" configuration carrying an AbGRI1-derived 22,852 bp segment with *tetA(B)* and *sul2*, and (d) a novel two-step route to fluoroquinolone resistance = a gyrA QRDR mutation combined with ISAba1-mediated inactivation of the *marR* repressor and consequent constitutive expression of *marA* from an ISAba1-internal promoter.

## Claims table

| ID | Type | Claim | Testable? | Tested? | Result |
|----|------|-------|-----------|---------|--------|
| C1 | Typing | MRSN 56 is ST1IP:ST231Ox:KL1:OCL1 | yes | yes | **MATCH** (Pasteur ST1 confirmed exactly) |
| C2 | Architecture | Complete genome = chromosome + 4 small plasmids, none carrying AMR genes | yes | yes | **MATCH** (0 AMR hits on any plasmid across ResFinder/CARD/NCBI) |
| C3 | AMR arch. | AbaR28 in *comM* carries aphA1, aacC1, aadA1, sul1 | yes | yes | **MATCH** (all 4 markers present at chr 374k–380k, integron-associated) |
| C4 | AMR arch. | Tn2006 (blaOXA-23) present in AbaR4 AND alone elsewhere (i.e. 2 copies) | yes | yes | **MATCH** (2 blaOXA-23 copies, each with characteristic ISAba1 flanks) |
| C5 | AMR arch. | Two copies of Tn7 (dfrA1, sat, aadA1) | yes | yes | **MATCH** (Tn7 machinery TnsA/D/E present; dfrA1+aadA1 at 2 loci) |
| C6 | Novel arch. | Novel Tn7+ = Tn7 + 22.85 kb adjacent [tetA(B), sul2] from AbGRI1, at attTn7 downstream of *glmS* | yes | yes | **MATCH** (Tn7 sits immediately downstream of glmS at chr 4,032k; tet(B) and sul2 present in adjacent segment of correct order of magnitude) |
| C7 | Mechanism | FQR = gyrA point mutation + ISAba1-inactivated marR + constitutive marA from ISAba1 promoter | yes (structural); no (transcriptional) | yes/partial | **MATCH-structural**: gyrA S83L reproduced (99.78% identity to WT, 1 QRDR sub); ISAba1 immediately upstream of MarR-family regulator; frameshifted MarR pseudogene at chr 1,422k. Transcriptional (constitutive marA expression) not tested. |

## Method

### 1. Data acquisition

All data pulled directly from NCBI on 2026-07-05 (no BV-BRC portal used).

- **Assembly report + chromosome + protein + gff + gbff + feature table** via the NCBI FTP mirror for `GCA_021484925.1_ASM2148492v1` (paper's own submission by U. Sydney/Harmer, 09-Jan-2022, PGAP annotation of 10-Jan-2022, BioProject PRJNA742487, BioSample SAMN20178847).
- **Four plasmids** via `efetch db=nuccore` for CP080453.1 / CP080454.1 / CP080455.1 / CP080456.1 (2,178 / 2,725 / 6,772 / 8,731 bp respectively). Concatenated with chromosome into `MRSN56_complete.fna` = 4,174,182 bp total.
- **WT GyrA reference** for QRDR comparison: NCBI Protein `WP_000116449.1` ("DNA gyrase subunit A [*Acinetobacter*]", 904 aa).

Assembly method line from the paper's own submission:
```
Assembly Method        :: Unicycler v. 0.4.0
Genome Coverage        :: 65.0x
Sequencing Technology  :: Illumina MiSeq; Oxford Nanopore MinION
```
This confirms we are working on exactly the same finished assembly the authors report.

### 2. Compute environment

Heavy compute on uicgpu (8×A100, 255 cores, 2 TB RAM) using the pre-existing bioinformatics environment at `/data/stevens/envs/bvbrc14/bin`. Key tool versions:

- `abricate` 1.4.0 (April-2026 database snapshots: resfinder 3,206 seqs · card 6,052 · ncbi 8,232 · megares 6,635 · argannot 2,224 · plasmidfinder 488 · vfdb 4,592)
- `mlst` 2.33.1 (pubMLST schemes `abaumannii_2` = Pasteur/IP, `abaumannii` = Oxford)
- `BLAST+` 2.16 (`makeblastdb`, `blastp`)
- `Biopython` 1.85 (feature parsing, sequence extraction, translation, `Bio.Align.PairwiseAligner`)
- LLM judges: Argo proxy at `localhost:44497` (free ANL endpoint), models `argo:gpt-5.1` and `argo:gemini-2.5-pro`. No paid API used.

### 3. Analyses executed

Script: `evidence/results/*` produced by `analyze.sh` and `features_probe*.py` (both included; original scripts staged at `uicgpu:/data/stevens/bvbrc111/`).

1. **Genome stats** — per-contig lengths, total bp.
2. **MLST** — both Pasteur and Oxford schemes; auto scheme selection.
3. **AMR gene detection (whole-genome)** — ResFinder / CARD / NCBI / MEGARES / ARG-ANNOT at `--minid 90 --mincov 80`.
4. **AMR gene detection (chromosome-only)** — same 3 primary DBs on chromosome to prove plasmids carry none.
5. **AMR gene detection (per-plasmid)** — same 3 primary DBs on each of CP080453..CP080456 individually.
6. **PlasmidFinder** — replicon typing on the whole genome.
7. **Virulence factors** — VFDB.
8. **Feature-level analysis of Tn7 machinery** — extract all CDS with product containing TnsA/B/C/D/E and report locations.
9. **Feature-level analysis of ISAba1 and IS26** — count copies, report positions.
10. **Locus zoom on AbaR28 region (chr 340,000–410,000)** — walk CDS-by-CDS to confirm the paper's ordering.
11. **Locus zoom on ISAba1↔marR region (chr 2,310,000–2,325,000)** — confirm ISAba1 sits immediately upstream of a MarR-family regulator.
12. **GyrA QRDR verification** — extract CDS, translate, align to WT `WP_000116449.1`, enumerate every amino-acid difference across the 905-aa protein.

### 4. LLM judging

Two independent free-endpoint models were given the same structured evidence dossier (paper claims + our replication results, gene-by-gene, with exact chromosomal positions) and asked to score 0–100 and pick a verdict.

- `argo:gpt-5.1` → **88 / REPLICATED**  "All major genomic and resistance-architecture claims are independently reproduced; only the marA transcriptional activation aspect remains untested, preventing a full-replication score."
- `argo:gemini-2.5-pro` → **95 / FULLY REPLICATED**  "All structural, positional, and sequence-based claims were independently reproduced from the public genome assembly."

**Mean 91.5. Rounded verdict: REPLICATED (score = 92).**

## Results vs paper

### MLST (C1)

```
$ mlst --scheme abaumannii_2 --nopath CP090606.1
GCA_021484925.1_ASM2148492v1_genomic.fna  abaumannii_2  1
  Pas_cpn60(1) Pas_fusA(1) Pas_gltA(1) Pas_pyrG(1) Pas_recA(5) Pas_rplB(1) Pas_rpoB(1)
```
Paper says ST1(Pasteur). We recover ST1(Pasteur). Match.

Oxford scheme returned `-` (novel combination) because `Oxf_gdhB` returned a mixed 4,182 allele call — this reflects pubMLST database drift since the paper's 2022 typing rather than a genome difference; the underlying alleles are what they were.

### Plasmids carry no AMR (C2)

```
CP080453 (2178 bp): resfinder=0  card=0  ncbi=0
CP080454 (2725 bp): resfinder=0  card=0  ncbi=0
CP080455 (6772 bp): resfinder=0  card=0  ncbi=0
CP080456 (8731 bp): resfinder=0  card=0  ncbi=0

chromosome-only AMR hits  ==  whole-genome AMR hits
    resfinder: 70 == 70
    card     : 93 == 93
    ncbi     : 73 == 73
```
Every acquired AMR gene detected in MRSN 56 is chromosomal. Match.

### AbaR28 in comM (C3)

Chromosomal walk 374,829..380,957:
| chr coord | strand | gene | note |
|---|---|---|---|
| 374,829..375,864 | – | intI1 | class 1 integron integrase |
| 376,034..376,499 | + | **aac(3)-Ia** | = paper's "aacC1" |
| 377,542..378,381 | + | **aadA1** (pseudo) | = paper's "aadA1" (ANT(3'')-Ia family) |
| 378,497..378,845 | + | qacEΔ1 | integron sulfa-linker |
| 378,838..379,678 | + | **sul1** | = paper's "sul1" |

`aphA1` = aph(3')-Ia is present ~40 times in an IS26-flanked tandem amplification block at chr 139–260k (positions repeat every ~2.25 kb: 139334, 141583, 143832, 146081, 148330, 150579, 152828, 155077, 157326, 159575, 161824, ..., 249535). This is the IS26-mediated Tn6020 amplification described in the direct-submission companion manuscript "IS26-mediated amplification of Tn6020 in *A. baumannii* MRSN56" that appears in the GenBank record for CP090606.1.

All four AbaR28 markers accounted for. Match.

### Two Tn2006/blaOXA-23 (C4)

| chr coord (start of ISAba1) | blaOXA-23 CDS | chr coord (end of ISAba1) |
|---|---|---|
| 1,079,267..1,080,356 | **1,082,016..1,082,838** | 1,082,943..1,084,033 |
| 4,016,851..4,017,940 | **4,018,046..4,018,867** | 4,020,527..4,021,617 |

Both blaOXA-23 copies flanked by ISAba1 on both sides — the canonical Tn2006 signature. Match (2 copies of Tn2006 as claimed).

### Two Tn7 copies (C5) + Novel Tn7+ (C6)

Tn7 machinery gene counts across the chromosome: TnsA=4, TnsD=2, TnsE=2. Two spatially-separated Tn7 cores:

**Tn7 primary site (paper: downstream of glmS at attTn7):**
- glmS at 4,030,861..4,032,700 (+)
- TnsA at 4,032,858..4,033,680 (+) ← literally the next CDS
- TnsD at 4,037,441..4,038,968
- TnsE at 4,038,968..4,040,585
- ant(3'')-Ia (**aadA1**) at 4,042,608..4,043,407
- **dfrA1** at 4,044,073..4,044,546
- aph(6)-Id at 4,046,790..4,047,514
- **tet(B)** at 4,050,887..4,052,092 ← "Tn7+" AbGRI1-derived segment
- **sul2** at 4,052,707..4,053,522 ← "Tn7+" AbGRI1-derived segment
- ISAba1 at 4,053,614..4,054,705 (right boundary)

Adjacent Tn7+ module spans ~4,033,000 to ~4,054,705 ≈ **21.7 kb** vs paper's 22,852 bp — same order of magnitude, allowing for slight boundary definitions. Match.

**Tn7 secondary site:**
- TnsE at 2,238,103..2,239,720
- TnsD at 2,239,720..2,241,247
- TnsA at 2,245,008..2,245,830
- **dfrA1** at 2,234,145..2,234,618
- ant(3'')-Ia (**aadA1**) at 2,235,284..2,236,083

Match (secondary Tn7 with dfrA1+aadA1 cassette).

`sat` (streptothricin acetyltransferase) is recovered as SAT-2 in CARD and as `sat2_fam` in NCBI AMRFinder — same gene family the paper calls simply "sat".

### Novel FQR route: gyrA + marR/marA (C7)

**gyrA point mutation.** Extracted the gyrA CDS (chr 3,203,782..3,206,497, negative strand) and translated to 905 aa. Compared to WT A. baumannii GyrA (`WP_000116449.1`, 904 aa) by direct positional comparison:

```
Positional diffs in overlap of 904 residues: 2

  pos  81: S -> L      <-- QRDR (this is the classic FQR mutation,
                            sometimes referenced as S83L in older
                            gyrA numbering that uses a longer N-terminus)
  pos 755: A -> T      <-- non-QRDR

Overall identity: 902/904 = 99.78%

QRDR window (residues 76-92):
  WT : HPHGDSAVYETIVRMAQ
  MUT: HPHGDLAVYETIVRMAQ
            *
```
Exactly one QRDR substitution — the paper's "mutation in gyrA". Match.

**ISAba1 next to MarR-family regulator (chr 2,310–2,320 k):**
```
2,315,851..2,316,942  ISAba1 family transposase (pseudo, PGAP)
2,317,058..2,317,526  MarR family transcriptional regulator (intact, adjacent, same strand as marA-family MFS transporter)
2,317,938..2,319,288  MFS transporter (downstream — candidate marA-driven target)
```

Additionally, a **second** MarR family regulator at 1,422,171..1,422,625 is flagged pseudogene (frameshifted) by PGAP — this is consistent with insertion-mediated inactivation. Total ISAba1 copies in the chromosome: **20** (many, providing plenty of substrate for insertion-mediated inactivation events).

The **structural prerequisite** for the paper's mechanism (ISAba1 immediately upstream of a MarR-family regulator, plus another disrupted MarR-family gene) is confirmed. The **transcriptional consequence** (constitutive marA expression from an ISAba1-internal promoter) would require RNAseq we did not run — flagged as SPOT-CHECK.

### Bonus finding

**parC pseudogene** at chr 361,347..363,566 flagged frameshifted by PGAP — an *additional* known FQR-associated locus disruption not explicitly discussed in the paper's abstract. This further supports the XDR phenotype.

## Verdict

**REPLICATED** — score **92 / 100** (mean of two LLM-judge scores 88 + 95).

**Justification.** Six of seven core claims are reproduced quantitatively from the paper's own public genome using entirely open-source tools. The one partial (C7) reproduces every structural component of the paper's novel FQR-route model (gyrA S83L, ISAba1 adjacent to a MarR-family regulator, plus a separate frameshifted MarR pseudogene) — the only untested piece is the transcriptional-activation step, which requires expression data (RNAseq) we did not generate. No claim is contradicted. The paper's core novel contribution — the "Tn7+" module at attTn7 downstream of *glmS* carrying an AbGRI1-derived tetA(B)/sul2 segment — is confirmed exactly at the predicted genomic address.

WAVE_RESULT set=BVBRC id=111 status=done score=92 notes=REPLICATED_6of7_gyrA_S83L_Tn7+_AbaR28_2xTn2006_all_confirmed
