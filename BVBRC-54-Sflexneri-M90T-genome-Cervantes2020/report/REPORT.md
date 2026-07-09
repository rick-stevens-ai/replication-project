# Replication Report: Cervantes-Rivera, Tronnet & Puhar (2020)
## "Complete genome sequence and annotation of the laboratory reference strain *Shigella flexneri* serotype 5a M90T and genome-wide transcriptional start site determination"

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020).
**DOI:** [10.1186/s12864-020-6565-5](https://doi.org/10.1186/s12864-020-6565-5)
**PMC:** PMC7132871 — **PMID:** 32252626
**Open access:** ✅ (CC BY 4.0 / BMC)

**Set:** BVBRC-54 · **Report Date:** 2026-07-02 · **Analyst:** Ollie (OpenClaw AI) — BV-BRC Replication Project
**Verdict:** **PARTIAL REPLICATION (strong).** The deposited genome's core structural claims are reproduced *to the base pair* (two circular replicons; chromosome 4,596,714 bp; plasmid pWR100 232,195 bp), and the paper's central biology — that the pWR100 virulence megaplasmid carries the complete Type-3 Secretion System — is independently reconstructed via specialty-gene scanning. The de-novo assembly-from-raw-reads step and the dRNA-seq TSS quantification (6723/7328) were not re-executed, so this is PARTIAL, not full REPLICATED.

---

## 1. Paper

*Shigella flexneri* 5a M90T is one of the two flagship laboratory reference strains for *Shigella*
pathogenesis research worldwide. Despite decades of molecular-pathogenesis work on it, no complete
genome existed — only a gapped chromosome scaffold (annotated off a different serotype, 5b 8401) plus
an independently sequenced virulence plasmid (pWR501/AF348706). This paper closes that gap: it reports
the **first complete, gapless genome** for serotype 5a M90T as two circular replicons — the chromosome
and the pWR100 virulence megaplasmid — assembled from **PacBio SMRT** long reads with **Canu 1.7**
(~157× coverage) and polished with **Illumina RNA-seq** (a novel long-DNA + short-RNA hybrid strategy).
It further reports genome-wide transcriptional start sites via dRNA-seq (6723 primary + 7328 secondary
TSS) and integrates the annotation into RegulonDB/RSAT.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Complete gapless genome = exactly 2 circular replicons (chromosome + pWR100). | Assembly structure | Yes (deposited assembly). | ✅ Reproduced exactly |
| C2 | Chromosome = 4,596,714 bp; plasmid pWR100 = 232,195 bp. | Assembly metrics | Yes. | ✅ Reproduced exactly (bp-for-bp) |
| C3 | Assembled via PacBio SMRT (Canu 1.7, ~157×) + Illumina RNA-seq polish. | Methods/provenance | Only by re-assembling raw reads. | ❌ Not re-run (finished assembly verified, not the assembly step) |
| C4 | Annotation feature counts (CDS/tRNA/rRNA/IS/pseudogenes); high IS load (402). | Annotation content | Partially (re-annotate; IS typing separate). | ⚠️ Partially (tRNA/rRNA match; CDS/pseudo within a few %) |
| C5 | pWR100 encodes the T3SS essential for invasion. | Functional gene content | Yes (specialty-gene scan). | ✅ Reproduced |
| C6 | dRNA-seq: 6723 primary + 7328 secondary TSS. | Transcriptomics | Only by re-processing dRNA-seq reads. | ❌ Not re-run (data availability noted) |
| C7 | Genome + annotation publicly deposited and usable. | Availability | Yes. | ✅ Verified |

## 3. Method (this report)

All heavy analysis ran on **uicgpu** (8×A100 node; CherryRd was under memory pressure). Free tools only.

1. **Paper acquisition.** Europe PMC core query on PMID 32252626 → confirmed OA (CC BY), PMC7132871,
   `hasData=Y`. Pulled full-text XML and parsed Tables 1–3 for the paper's exact numbers.
2. **Genome identification.** NCBI assembly search for *S. flexneri* 5a M90T returned six assemblies.
   Selected **GCF_004799585.1 (ASM479958v1)** — submitter **Umeå University** (= the paper's lab, MIMS),
   released 2019-04-18, level **Complete Genome**. Cross-check: its `contig_n50` = 4,596,714 (the paper's
   chromosome) and `total − chromosome` = 232,195 (the paper's plasmid) — a decisive identity match.
3. **Genome download.** Fetched FASTA + GFF + protein + sequence report via the **NCBI Datasets REST v2alpha**
   API (free, no auth). Replicons: chromosome **NZ_CP037923.1 / CP037923.1**, plasmid pWR100
   **NZ_CP037924.1 / CP037924.1**.
4. **Independent genome statistics.** Parsed the FASTA directly (Python): replicon count, per-replicon
   length, GC.
5. **Independent re-annotation.** **Prokka 1.12** (conda env `bvbrc28`) de-novo on the FASTA.
6. **Specialty-gene / BV-BRC-equivalent workflow** (conda env `bvbrc14`):
   - **abricate 1.4.0** vs **VFDB, Victors, ecoli_vf** (= BV-BRC Specialty Genes: Virulence VFDB/Victors),
     **CARD, ResFinder, NCBI** (= BV-BRC AMR), **PlasmidFinder** (= BV-BRC PlasmidFinder-via-similar-genome).
   - **AMRFinderPlus 4.2.7** (`--organism Escherichia --plus`) = the paper's CARD/AMRFinder AMR path.
   - **mlst 2.33.1** (Achtman *E. coli*/*Shigella* scheme).
7. **LLM-judge scoring.** Free Argo proxy (`argo:gpt-5.2`, localhost:44497) scored each claim from the
   evidence and issued the verdict (see §6). No regex scoring.

## 4. Results vs paper

### 4.1 Genome structure (C1, C2) — EXACT
| Replicon | Accession | Paper (bp) | Independent (bp) | Match |
|---|---|---:|---:|---|
| Chromosome | CP037923 | 4,596,714 | 4,596,714 | **EXACT** |
| Plasmid pWR100 | CP037924 | 232,195 | 232,195 | **EXACT** |
| Total / # circular replicons | — | 4,828,909 / 2 | 4,828,909 / 2 | **EXACT** |

Independent GC: chromosome 50.92%, plasmid 45.68% (NCBI report 51.0% / 45.5%).

### 4.2 Annotation (C4) — consistent across independent pipelines
| Feature | Paper (Prokka+curation) | RefSeq PGAP | Prokka 1.12 (here) |
|---|---:|---:|---:|
| tRNA (genome) | 102 | 102 | 103 |
| rRNA (genome) | 22 | 22 | 22 |
| CDS (total) | 4,949 (4629+320) | 4,053 protein-coding | 5,004 (4720+284) |
| Pseudogenes (total) | 769 (640+129) | 757 | — |
| IS elements | 402 (296+106) | — | not re-typed |

tRNA and rRNA match near-exactly across all three; CDS/pseudogene totals differ by only a few percent —
the expected divergence between independent annotation pipelines, not a reproduction failure. The paper's
own pseudogene total (769) and RefSeq's (757) agree to ~1.5% — the high pseudogene/IS burden is the
genomic signature of *Shigella* reductive evolution, corroborated here.

### 4.3 Virulence plasmid = T3SS (C5) — REPRODUCED (the paper's central biology)
The independent VFDB/Victors scan places the **entire T3SS system on plasmid NZ_CP037924.1**:
- **Structural apparatus (mxi/spa):** mxiA,C,D,E,G,H,I,J,K,L,M,N + spa9,13,15,24,29,32,33,40,47
- **Invasins + chaperones:** ipaA,B,C,D + ipgA,B1,B2,C,D,E,F
- **Effectors:** osp (B,C1,C2,C3,D1,D2,D3/senA,E1,E2,F,G,I,Z) + ipaH (1.4,2.5,4.5,7.8,9.8)
- **Regulators + motility:** virF, virB (master cascade); icsA/virG, icsB, icsP/sopA
- **Replicon type (PlasmidFinder):** IncFII on the 232 kb megaplasmid — consistent with pWR100.

The chromosome carries the **SHI-2 pathogenicity island aerobactin siderophore** (iucABCD/iutA) — exactly
as the paper's Background describes ("SHI-2 … the aerobactin siderophore system").

### 4.4 Additional characterization
- **MLST:** ST631 (Achtman *E. coli*/*Shigella* scheme).
- **AMR (AMRFinderPlus):** only intrinsic **blaEC** (chromosomal ampC-type β-lactamase) + **emrE** efflux;
  **no acquired resistance** — consistent with M90T being a laboratory reference strain, not an MDR clinical
  isolate. (The paper makes no AMR claim; this is a clean negative control on the AMR workflow.)

### 4.5 Not reproduced
- **C3 (assembly from raw reads):** the finished assembly's structure/lengths were verified exactly, but
  the Canu-from-PacBio + Illumina-polish pipeline was not re-executed on raw reads.
- **C6 (TSS counts 6723/7328):** raw dRNA-seq (TEX ±) libraries were not fetched/re-processed; only data
  availability is noted.

## 5. Threats to validity
- The deposited assembly *is* the paper's own product (Umeå/MIMS), so C1/C2 verify the deposited artifact
  matches the paper's reported numbers rather than re-deriving them from raw reads — appropriate for a
  genome-announcement paper, but the reason C3 keeps this at PARTIAL.
- Annotation-count comparisons cross pipeline boundaries (Prokka 1.12 vs the paper's Prokka+manual curation
  vs NCBI PGAP); small numeric differences are expected and not treated as disagreement.
- IS-element count (402) was corroborated only indirectly (pseudogene load), not by re-running ISfinder.

## 6. LLM-judge verdict (Argo gpt-5.2, free)
Coverage: **5/7 claims tested = 71%**. All tested claims agree with the paper; C1–C2 reproduced *exactly*;
C5 (T3SS on plasmid) reproduced; C4 broadly consistent (IS count not directly re-typed). C3 (raw-read
assembly) and C6 (TSS counts) not re-executed. Judge's final call: **PARTIAL** — "independently confirms
the deposited complete-genome structure and exact replicon lengths, and corroborates that the virulence
plasmid carries a complete T3SS gene set … however, the raw-read assembly strategy and the dRNA-seq TSS
quantifications were not re-executed." Full text in `report/evidence/` (judge_verdict.md in work/).

## 7. Reproducibility pointers
- Assembly: `GCF_004799585.1` (GenBank `GCA_004799585.1`) · replicons `CP037923.1` (chromosome),
  `CP037924.1` (pWR100) · BioSample `SAMN10608416`.
- Download: NCBI Datasets REST `…/genome/accession/GCF_004799585.1/download`.
- Tools: Prokka 1.12, abricate 1.4.0 (VFDB/Victors/CARD/PlasmidFinder 2026-Apr dbs), AMRFinderPlus 4.2.7,
  mlst 2.33.1 (uicgpu conda envs bvbrc28 / bvbrc14).
- Evidence: `report/evidence/{genome_stats_comparison.md, virulence_T3SS_summary.txt, abricate_*.tsv,
  amrfinder.tsv, mlst.tsv, prokka_stats.txt}`.

## Verdict
**Verdict:** PARTIAL

WAVE_RESULT set=BVBRC-54 paper=PMID:32252626 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-54-Sflexneri-M90T-genome-Cervantes2020 one_line=S. flexneri 5a M90T complete genome (Cervantes-Rivera 2020) independently verified: 2 circular replicons + chromosome 4,596,714 bp + pWR100 232,195 bp reproduced bp-for-bp, full T3SS/ipa/mxi/spa/osp/virF reconstructed on pWR100 via VFDB scan; raw-read assembly and dRNA-seq TSS counts not re-executed.
