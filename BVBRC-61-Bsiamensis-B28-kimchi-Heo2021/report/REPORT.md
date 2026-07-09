# Replication Report: Heo et al. (2021)
## "Functional Genomic Insights into Probiotic *Bacillus siamensis* Strain B28 from Traditional Korean Fermented *Kimchi*"

**Paper:** Heo S, Kim JH, Kwak MS, Jeong DW, Sung MH. *Foods* 2021, **10**(8):1906.
**DOI:** [10.3390/foods10081906](https://doi.org/10.3390/foods10081906) — **PMID:** 34441683 — **PMCID:** PMC8394110
**Open access:** ✅ CC BY 4.0 (full text pulled from Europe PMC OA XML, not the paid `pdf` tool)

**Set:** BVBRC-61 · **Analyst:** Ollie (OpenClaw AI subagent) · **Date:** 2026-07-02 · **Host:** CherryRd (local, free tools)
**Verdict:** **PARTIAL REPLICATION (strong).**

The genome-derivable core of the paper reproduces cleanly and often *exactly* on the actual deposited public genome (GenBank CP066219–CP066221 / RefSeq GCF_016313165.1): the taxonomic reclassification (ANI), the complete genome architecture (chromosome/plasmid sizes, GC, tRNA/rRNA counts — several to the base pair), the safety genotype (no enterotoxins, no acquired AMR — verified by two independent AMR tools), and the probiotic/functional gene inventory. What is out of reach for a sequence-only replication is the paper's *wet-lab* evidence (enterotoxin PCR gels, disc-diffusion antibiotic phenotypes, β-hemolysis assay, antibacterial-activity plates) — hence PARTIAL rather than full REPLICATED.

---

## 1. Paper summary

Strain B28, isolated from Korean fermented *kimchi* and previously called *B. polyfermenticus*, is sequenced to completion and characterized as a candidate probiotic. The authors (i) reclassify B28 as *Bacillus siamensis* via 16S/MLST/ANI; (ii) report a complete genome (1 chromosome + 2 plasmids); (iii) argue the strain is *safe* (no enterotoxin/hemolysin/acquired-AMR genes; susceptible to 8 antibiotics; non-β-hemolytic); and (iv) catalog probiotic-relevant gene content (bacteriocins, GABA, bile-salt hydrolase, sporulation, adhesion, stress defense, plus strain-unique α-galactosidase and triacylglycerol lipase). This maps directly onto the BV-BRC *Comprehensive Genome Analysis + AMR + Similar Genome Finder* workflow.

## 2. Claims

| # | Claim | Type | Testable from public data? | Tested here? |
|---|---|---|---|---|
| C1 | B28 reclassifies as *B. siamensis* (ANI ≥98% to *B. siamensis*, ~94% to *velezensis*/*amyloliquefaciens*) | Genomic / taxonomy | Yes | ✅ fastANI + skani |
| C2 | Complete genome: chromosome 3,946,178 bp + plasmids 6.1/5.4 kb; GC 45.85%; 86 tRNA, 27 rRNA | Genome stats | Yes | ✅ FASTA + GFF |
| C3a | No *B. cereus*-type enterotoxin genes (Nhe/Hbl/CytK) | Genomic (safety) | Yes | ✅ proteome scan |
| C3b | *hlyIII* hemolysin-III-like gene present (but strain non-β-hemolytic) | Genomic + phenotype | Genotype: yes; phenotype: no | ✅ genotype / ⛔ phenotype |
| C3c | No **acquired** antibiotic-resistance genes; strain susceptible to 8 antibiotics | Genomic + phenotype | Genotype: yes; phenotype: no | ✅ AMRFinderPlus + RGI/CARD / ⛔ disc-diffusion |
| C4a | Bacteriocin/antimicrobial biosynthesis genes present | Genomic | Yes | ✅ (broad); specific "bacitracin operon" name ⚠️ |
| C4b | Probiotic gene content: BSH, GABA, GGT, subtilisin, sporulation, biofilm/EPS, adhesion (flagella/fibronectin), LTA, ROS-scavenging | Genomic | Yes | ✅ proteome survey |
| C4c | Strain-unique genes incl. α-galactosidase (melibiose) & triacylglycerol lipase | Genomic | Yes | ✅ MelA + lipases |
| C5 | Antibacterial activity against foodborne pathogens (Fig 2) | Phenotype (wet-lab) | No | ⛔ out of reach |

## 3. Method

All data free/public; all analysis local on CherryRd. Full tool/version table in `artifact_harvest.md`.

1. **Paper text** — Europe PMC OA full-text XML (`work/paper_fulltext.xml`); claims + accessions extracted.
2. **Genomes** — `datasets` CLI v18.25.1 downloaded B28 (**GCF_016313165.1**, resolved from nuccore CP066219 via eutils elink) plus the 6 comparators named in the paper's Methods (SCSIO 05746 GCA_002850535.1, KCTC 13613ᵀ GCA_000262045.1, *B. amyloliquefaciens* FS1092/RD7-7, *B. velezensis* JJ-D34/KMU01). B28 RefSeq annotation (`protein.faa` 3,808; `genomic.gff`) also pulled.
3. **Genome stats** — `genome_stats.py` (contig sizes, GC, N50); tRNA/rRNA counted from RefSeq GFF.
4. **ANI (C1)** — `fastANI` and `skani` (two independent algorithms), B28 query vs each reference.
5. **AMR / safety (C3)** — **AMRFinderPlus 4.2.7** (DB 2026-03-24.1), protein+nucleotide+GFF (`-a pgap`), `--plus`; cross-checked with **RGI/CARD 3.2.7** (DIAMOND, protein mode). Enterotoxin/hemolysin genotype from proteome scan.
6. **Functional inventory (C4)** — `func_survey.py` regex survey of all 3,808 RefSeq products + targeted greps (GABA, subtilisin/AprX, hlyIII, bacteriocin).
7. **MLST** — `mlst` 2.33.1 (pubMLST *bsubtilis* scheme).
8. **LLM-judge** — free Argo `gpt-5.2` (localhost:44497), temp 0, scored coverage/agreement (`evidence/llm_judge.txt`).

## 4. Results vs paper

### 4.1 C1 — Taxonomy / ANI (reproduced)

| Comparison | Paper ANI | fastANI (this) | skani (this) | >95% species? |
|---|---:|---:|---:|:--:|
| B28 vs *B. siamensis* KCTC 13613ᵀ | 98.61% | **98.42%** | **98.54%** | ✅ |
| B28 vs *B. siamensis* SCSIO 05746 | 97.73% | **97.55%** | **97.67%** | ✅ |
| B28 vs *B. velezensis* (KMU01) | ~94.06–94.28% | 94.32% | 94.18% | ❌ (<95) |
| B28 vs *B. amyloliquefaciens* (FS1092) | ~94% | 94.21% | 94.19% | ❌ (<95) |

All values within ~0.2% of the paper (expected across ANI algorithms/reference versions). Both *B. siamensis* comparisons exceed the 95% species boundary; both other-species comparisons fall below. **Reclassification of B28 from *B. polyfermenticus* to *B. siamensis* is independently reproduced.** → **YES**

### 4.2 C2 — Genome architecture (reproduced, several values EXACT)

| Metric | Paper | This study (GCF_016313165.1) | Match |
|---|---|---|:--:|
| Chromosome | 3,946,178 bp | **3,946,178 bp** | ✅ exact |
| Plasmid pB2801 | 6.1 kb | **6,117 bp** | ✅ |
| Plasmid pB2802 | 5.4 kb | **5,433 bp** | ✅ |
| Contigs (total) | 3 (chr + 2 plasmids) | **3** | ✅ |
| GC% | 45.85% | **45.85%** | ✅ exact |
| tRNA | 86 | **86** | ✅ exact |
| rRNA | 27 | **27** | ✅ exact |
| CDS | 3,573 (COG) / 1,663 (SEED) | 3,831 protein-coding (PGAP) | ⚠️ pipeline-dependent |

Comparator sanity: KCTC 13613ᵀ returned 51 contigs (paper states its genome is *incomplete* ✓); SCSIO 05746 returned 2 contigs (complete ✓). The only non-match is the raw CDS count, a known artifact of different annotation pipelines/snapshots (paper's 3,573 is a COG-categorized subset). **Architecture claim reproduced.** → **YES (genomic sub-claims exact)**

### 4.3 C3 — Safety (genotype reproduced; wet-lab phenotype out of reach)

**Enterotoxins (C3a):** proteome scan for *B. cereus* Nhe/Hbl/CytK enterotoxins → **0 hits (ABSENT)**, matching the paper's PCR-verified absence. **hlyIII (C3b):** RefSeq annotates the hemolysin-III-like gene as "hemolysin family protein" — **PRESENT (×4)**, matching the paper. ✅ genotype.

**AMR (C3c) — two independent tools agree there is no acquired resistance:**

*AMRFinderPlus 4.2.7 (DB 2026-03-24.1):* 5 hits, **all `scope=core` (intrinsic/chromosomal)** —

| Element | Class | Method | %id | Scope |
|---|---|---|---:|---|
| satA | streptothricin | BLASTP | 83.2 | core |
| fosM | fosfomycin | HMM | 75.4 | core |
| bla (subclass B1 MBL) | β-lactam | HMM | 51.1 | core |
| bla (class A) | β-lactam | HMM | 63.4 | core |
| Tet(L/K/45) efflux MFS | tetracycline | HMM | 88.0 | core |

*RGI/CARD 3.2.7:* **9 Strict, 0 Perfect** — vanT/vanY (van-cluster *homolog fragments*, not a functional van operon), qacG/qacJ (disinfectant efflux), FosBx1 (fosfomycin — corroborates fosM), tet(45) (corroborates Tet), BcI (*Bacillus* cephalosporinase — corroborates β-lactamases).

**Interpretation:** neither tool finds any *acquired/mobile* resistance determinant; every hit is an intrinsic *Bacillus* chromosomal homolog (efflux pumps, native β-lactamases, van/fos homologs). This is fully consistent with (a) the paper's phenotypic susceptibility to all 8 antibiotics, and (b) the paper's own Table 2, which explicitly reports putative tet/lincomycin/bicyclomycin/multidrug efflux genes while noting no resistance phenotype. Modern curated databases surface a bit more intrinsic background than the paper's 2021 RAST/SEED view, but the safety-relevant conclusion — *no acquired AMR* — is upheld. → **YES (genotype); phenotype ⛔ un-reproducible from sequence.**

### 4.4 C4 — Probiotic / functional gene content (reproduced)

Survey of all 3,808 RefSeq products (`evidence/func_survey.json`):

| Category | Paper | This study | Match |
|---|---|---|:--:|
| Bile-salt hydrolase (cholylglycine hydrolase) | present | choloylglycine hydrolase family (1) | ✅ |
| GABA production from glutamate | present | GABA permease + γ-glutamyl-γ-aminobutyrate hydrolase + 4-aminobutyrate transaminase | ✅ |
| γ-glutamyltransferase | present | 3 | ✅ |
| Subtilisin | present | serine protease AprX (+ S1C/HtrA) | ✅ |
| Sporulation (Spo0A etc.) | present | 128 incl. Spo0A | ✅ |
| Biofilm / EPS | present | 11 incl. EpsG, BslA, poly-γ-glutamate | ✅ |
| Adhesion: flagella / fibronectin | present | 41 flagellar + fibronectin-binding | ✅ |
| Lipoteichoic acid | present | 7 (LtaS, Dlt operon) | ✅ |
| ROS-scavenging (catalase/SOD/glutathione) | present | 18 (catalase, SOD, GPx, AhpC, Trx) | ✅ |
| Bacteriocin operons | present (bacitracin + mesentericin) | surfactin, Blp class II bacteriocin, lantibiotic immunity, circular bacteriocin (11) | ⚠️ broad yes; exact "bacitracin operon" name not in RefSeq vocabulary |
| **Unique:** α-galactosidase (melibiose) | present | **α-galactosidase MelA** | ✅ |
| **Unique:** triacylglycerol lipase | present | lipase/esterase family (6) | ✅ |

Nearly the entire functional inventory is independently confirmed. The only soft spot is the paper's *specific* bacteriocin-operon naming ("bacitracin + mesentericin"), which the RefSeq annotation does not label identically (though bacteriocin/lantibiotic biosynthesis is unambiguously present). → **YES (with one naming caveat).**

### 4.5 C5 — Antibacterial activity (out of reach)

The Figure-2 antibacterial-activity plate assay against 7–8 foodborne pathogens is a wet-lab experiment that cannot be reproduced from genome sequence. Genotypic proxy (bacteriocin genes present, §4.4) is consistent with the claimed activity but does not constitute replication. → **not tested.**

## 5. LLM-judge (free Argo gpt-5.2)

Independent judge verdict: **PARTIAL**. C1 = YES; C2/C3/C4 = PARTIAL (docking C2 for annotation counts [subsequently closed: tRNA/rRNA exact], and C3/C4 for un-reproducible wet-lab phenotypes and specific bacteriocin naming). Full text in `evidence/llm_judge.txt`. My final verdict aligns with the judge, upgraded to *PARTIAL (strong)* on the strength of the exact-match genome architecture and dual-tool AMR concordance.

## 6. Coverage

Of the paper's testable-from-sequence claims (C1, C2, C3a-c genotype, C4a-c), **~8/9 reproduced** (one naming caveat on bacteriocin operon). The three inherently wet-lab items (enterotoxin PCR gel, disc-diffusion phenotype, antibacterial plates) are out of reach for a genomics replication and are the reason the verdict is PARTIAL rather than REPLICATED. No claim was **contradicted**: the extra intrinsic-AMR homologs surfaced by modern databases do not conflict with the paper (they refine, and match the paper's Table 2 caveat and phenotype).

## Verdict
**Verdict:** PARTIAL

---

`WAVE_RESULT set=BVBRC-61 paper=PMID:34441683(10.3390/foods10081906) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-61-Bsiamensis-B28-kimchi-Heo2021 one_line="B. siamensis B28 (kimchi probiotic): genome architecture reproduced to the base pair (chr 3,946,178 bp + 6.1/5.4 kb plasmids, GC 45.85%, 86 tRNA/27 rRNA all exact), ANI reclassification to B. siamensis confirmed (98.4-98.5%/97.6-97.7% vs 98.61/97.73), safety genotype upheld (no enterotoxins, no acquired AMR by AMRFinderPlus+CARD, only intrinsic Bacillus homologs), full probiotic gene inventory confirmed; wet-lab PCR/disc-diffusion/antibacterial phenotypes out of reach for sequence-only replication."`
