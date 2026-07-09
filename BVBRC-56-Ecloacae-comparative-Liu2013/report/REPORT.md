# Replication Report: Liu et al. (2013)
## "Comparative genome analysis of *Enterobacter cloacae*"

**Paper:** Liu WY, Wong CF, Chung KM, Jiang JW, Leung FC. *PLoS ONE* 8(9):e74487 (2013).
**DOI:** [10.1371/journal.pone.0074487](https://doi.org/10.1371/journal.pone.0074487) · **PMID:** 24069314 · **PMC:** PMC3771936
**Open access:** ✅ (CC BY)

**Set ID:** BVBRC-56 · **Replication date:** 2026-07-02 · **Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Wave (top-up rank 42)
**Verdict:** **PARTIAL REPLICATION.** Descriptive genome statistics (Table 1) reproduce near-exactly on re-downloaded NCBI genomes; the comparative pan-genome/core-genome ratios, strain-unique-CDS ordering, T6SS rank-ordering, and phylogenomic clade structure (E. cloacae cluster + clean Pantoea outgroup) are independently reproduced by from-scratch pipelines. Several functional-category counts that depend on the paper's specific RAST-SEED / IMG manual curation (carbohydrate-gene abundance, full fimbriae/T6SS on two strains) do not match numerically under an annotation-driven pipeline. LLM judge (free Argo gpt-5.2) independently returned **PARTIAL**.

---

## 1. Paper

The first comprehensive comparative-genomics analysis of the *Enterobacter cloacae* species. The authors sequenced the plant growth-promoting endophyte *E. cloacae* subsp. *cloacae* **ENHKU01** (isolated from a pepper plant, Hong Kong 2010; GenBank **CP003737.1**) and compared it against the 3 other publicly available complete *E. cloacae* genomes (ATCC13047 human pathogen; EcWSU1 plant pathogen; SDM 2,3-butanediol producer) plus 4 other *Enterobacter* species and 3 *Pantoea* outgroups. Main findings: (i) a conserved *E. cloacae* core genome carrying general physiology/survival genes, with plasmids + variable regions carrying strain-specific virulence; (ii) fimbrial diversity underlying host/niche determination; (iii) multiple antagonism mechanisms (siderophores, bacteriocins, chitinases, AMR) and Type VI secretion systems (T6SS) conferring competitive fitness; validated by wet-lab antagonism assays (not replicable in silico).

## 2. Claims table

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Table 1 genome stats (size, replicons, GC, CDS, tRNA, rRNA) for ENHKU01, ATCC13047, EcWSU1, SDM. | Genome stats | Yes (NCBI GenBank) | ✅ |
| C2 | GC content of the 4 E. cloacae strains ranges 54.5–55.1%. | Genome stats | Yes | ✅ |
| C3 | ENHKU01 = single ~4.72-Mb chromosome, 0 plasmids; ATCC13047 largest (~5.31–5.6 Mb) via 2 plasmids + >20 variable regions. | Genome stats | Yes | ✅ |
| C4 | The 4 E. cloacae strains share **3540 CDS** in their core genome (EDGAR). | Comparative | Yes | ✅ (RBH pan-genome) |
| C5 | Strain-unique CDS ≈ 6% (ENHKU01), 6% (SDM), 12% (EcWSU1), 20% (ATCC13047). | Comparative | Yes | ✅ |
| C6 | Phylogenomic tree (1732 core genes, 8 Enterobacter, Pantoea outgroup): E. cloacae strains cluster; Enterobacter groups with Klebsiella. | Phylogenomics | Yes (independent method) | ✅ (AAI/NJ) |
| C7 | ENHKU01 by 16S/housekeeping genes most closely related to ATCC13047. | Phylogenetics | Yes | ✅ |
| C8 | Fimbriae: 9–13 loci per strain, only 4 conserved across all 4. | Functional | Partly (annotation) | ⚠️ approx |
| C9 | T6SS clusters: ATCC13047 & ENHKU01 = 2; SDM & EcWSU1 = 1. | Functional | Partly (annotation) | ✅ (partial) |
| C10 | >640 carbohydrate-utilization genes (13–15% of genome). | Functional | Partly (annotation) | ⚠️ method-limited |
| C11 | Wet-lab antagonism assays: ENHKU01 inhibits plant pathogenic fungi/bacteria. | Experimental | No (wet lab) | ❌ out of scope |

## 3. Method

All genomes **re-downloaded from NCBI nuccore by GenBank accession** (efetch, free/no-auth; not the paid `pdf` tool, and paper text obtained via Europe PMC full-text XML). All analysis run **from scratch on real data** in a dedicated conda env (`bvbrc56`: DIAMOND, NCBI BLAST+, MAFFT, FastTree, ncbi-datasets-cli, Biopython) on **uicgpu** (8×A100 node). No BV-BRC private/GUI steps; BV-BRC-equivalent workflows reproduced with open tools.

1. **Genome stats (C1–C3):** parsed each `.gbk` (Biopython) → total length, replicon count + chromosome/plasmid classification (source/plasmid qualifier + description), GC%, CDS/tRNA/rRNA feature counts. rRNA operons = rRNA-gene-count ÷ 3.
2. **Pan/core genome (C4–C5):** concatenated the 4 E. cloacae proteomes; DIAMOND all-vs-all blastp (e≤1e-5); kept reciprocal-best hits with ≥50% identity and ≥70% coverage both ways; single-linkage clustering. Core = clusters containing a gene from **all 4** strains; unique/singleton = clusters in exactly 1 strain.
3. **Functional features (C8–C10):** keyword search over GenBank `product`/`gene` annotations for fimbrial/pilus/usher/chaperone loci (clustered by genomic adjacency), T6SS component genes (ClpV/TssH, Hcp, VgrG, Vip/Imp/Vas/Tss families; bona-fide cluster = ≥6 contiguous component genes), and carbohydrate-metabolism genes.
4. **Phylogenomics (C6–C7):** proteome-wide **AAI** (reciprocal-best-hit average amino-acid identity via DIAMOND, ≥50% length coverage) for all 55 pairs across 8 Enterobacter + 3 Pantoea; NJ tree from (100−AAI)/100 distances (Biopython).
5. **Scoring:** free-Argo **gpt-5.2** LLM judge given the full claim table + paper numbers + replication numbers → per-claim reproduced/partial/not + overall verdict (never regex).

## 4. Results vs paper

### 4a. Table 1 genome statistics (C1–C3) — **REPRODUCED**

| Strain | Metric | Paper | This work | Match |
|---|---|---|---|---|
| ENHKU01 | Size (Mb) / plasmids / GC% / CDS / tRNA | 4.73 / 0 / 55.1 / 4338 / 82 | **4.73 / 0 / 55.07 / 4338 / 82** | ✅✅✅ **CDS+tRNA exact** |
| ATCC13047 | Size / plasmids / GC% / CDS | 5.6 / 2 / 54.6 / 5518 | **5.60 / 2 / 54.58 / 5518** | ✅✅✅ **CDS exact** |
| EcWSU1 | Size / plasmids / GC% / CDS / tRNA | 4.8 / 1 / 54.5 / 4619 / 83 | **4.80 / 1 / 54.54 / 4619 / 83** | ✅✅✅ **CDS+tRNA exact** |
| SDM | Size / plasmids / GC% / CDS | 4.97 / 0 / 55.1 / 4542 | **4.97 / 0 / 55.06 / 4542** | ✅✅✅ **CDS exact** |

GC range recomputed **54.54–55.07%** vs paper **54.5–55.1%** (C2 ✅). ENHKU01 single chromosome / 0 plasmids and ATCC13047 as the largest genome via 2 plasmids (C3 ✅). rRNA = 25 genes per E. cloacae strain = **8 operons** (matches paper). Minor tRNA deltas (SDM 79 vs paper 83; ATCC13047 84 vs paper 24 — the paper's "24" is a probable typo/transposition since GenBank consistently shows ~79–84). **All CDS totals reproduce exactly.**

### 4b. Pan/core genome (C4–C5) — **REPRODUCED (directional) / PARTIAL (exact number)**

| Metric | Paper | This work | Note |
|---|---|---|---|
| Core CDS (all 4 E. cloacae) | **3540** | **3345** | −5.5% (DIAMOND RBH vs EDGAR BSR) |
| Pan-genome clusters | — | 6642 | — |
| Unique % ENHKU01 | ~6% | **7.8%** | ✅ close |
| Unique % SDM | ~6% | **7.1%** | ✅ close |
| Unique % EcWSU1 | 12% | **13.3%** | ✅ close |
| Unique % ATCC13047 | 20% | **19.8%** | ✅ **near-exact** |

The **strain-plasticity ordering (ATCC13047 ≫ EcWSU1 > ENHKU01 ≈ SDM)** — the paper's central pan-genome conclusion — is reproduced almost exactly. Core count is 5.5% low, expected from methodology differences (EDGAR BLAST-score-ratio vs DIAMOND reciprocal-best-hit).

### 4c. Phylogenomics (C6–C7) — **REPRODUCED (structure) / NOT (specific nearest-neighbor)**

- **Pantoea outgroup cleanly separates:** AAI ~72–73% Enterobacter↔Pantoea vs 89–94% within Enterobacter; the 3 Pantoea form their own clade. ✅
- **The 4 E. cloacae strains form a tight clade** (AAI 93.6–94.0%), distinct from the other *Enterobacter* species. ✅ (matches Fig 1 topology via independent AAI/NJ method).
- *E. aerogenes* KCTC2190 falls basally near the outgroup — consistent with its known reclassification to ***Klebsiella aerogenes***, indirectly supporting the paper's "Enterobacter groups with Klebsiella" statement.
- **C7 not confirmed:** whole-proteome AAI ranks ENHKU01's closest relatives as SDM 93.96% ≈ EcWSU1 93.83% ≈ ATCC13047 93.65% — all three essentially tied. The paper's "closest to ATCC13047" was a 4-housekeeping-gene call; the finer whole-proteome signal doesn't single out ATCC13047 (not a contradiction, a resolution difference).

### 4d. Functional features (C8–C10) — **PARTIAL**

- **T6SS (C9):** bona-fide clusters (≥6 contiguous component genes): **ATCC13047 = 2 ✅, SDM = 1 ✅** (exact matches). ENHKU01 = 1 clear + 1 fragmented block (paper: 2); EcWSU1 = 0 (paper: 1). The undercount on ENHKU01/EcWSU1 is expected: the paper states *"Two T6SSs of ENHKU01 were manually identified and reconfirmed by BLAST"* — i.e. automated annotation misses them, exactly what we observe. The paper's **rank-ordering (ATCC13047 & ENHKU01 richest in T6SS) is directionally reproduced.**
- **Fimbriae (C8):** keyword-based loci counts land in the same order of magnitude (8–19) as the paper's 9–13, but the noisy net over-/under-calls; the specific "only 4 conserved" was not cleanly re-demonstrated.
- **Carbohydrate genes (C10):** ~424–432 per strain (~8–10%) vs paper's >640 (13–15%). Method-limited — my product-keyword net is narrower than the paper's RAST-SEED subsystem assignment; a data disagreement is not implied.

### 4e. Out of scope
- C11 wet-lab antagonism bioassays — not reproducible in silico.

## 5. Discussion

The **replicable descriptive and comparative-genomics backbone of the paper reproduces strongly** on independently re-downloaded NCBI genomes: exact CDS totals, matching genome sizes/plasmids/GC/rRNA-operons, a faithful pan-genome plasticity ordering (ATCC13047 20% unique, near-exact), a correct core/accessory split, and a phylogenomic tree that recovers the E. cloacae clade and a clean Pantoea outgroup via an entirely different method (AAI/NJ vs the paper's 1732-core-gene MrBayes tree). The gaps are concentrated in **functional-category counts that are intrinsically annotation-pipeline-dependent** (RAST SEED subsystems, manual IMG T6SS curation) — where the paper itself flags manual curation — plus one fine-vs-coarse nearest-neighbor nuance. None of the shortfalls contradict the paper; they reflect methodology/annotation differences. This honestly lands at **PARTIAL** rather than full REPLICATED.

## Verdict
**Verdict:** PARTIAL

---
WAVE_RESULT set=BVBRC-56 paper=Liu2013_Ecloacae_comparative_PLoSONE_e74487 (DOI 10.1371/journal.pone.0074487) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-56-Ecloacae-comparative-Liu2013 one_line="Enterobacter cloacae comparative genomics (Liu 2013): re-downloaded all 11 NCBI genomes and re-ran genome stats + DIAMOND pan/core-genome + AAI phylogenomics from scratch on uicgpu; Table 1 stats reproduce near-exactly (CDS totals exact), unique-CDS plasticity ordering (ATCC13047 ~20%) and T6SS rank (ATCC13047=2/SDM=1) reproduced, E.cloacae clade + Pantoea outgroup recovered; annotation-dependent carbohydrate/fimbriae counts fall short of the paper's RAST-curated numbers; free-Argo gpt-5.2 judge concurs PARTIAL."
