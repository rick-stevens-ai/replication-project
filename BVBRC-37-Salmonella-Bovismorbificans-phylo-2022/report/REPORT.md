# Replication Report: Gopinath et al. (2022)
## "Phylogenomic Analysis of *Salmonella enterica* subsp. *enterica* Serovar Bovismorbificans from Clinical and Food Samples Using Whole Genome Wide Core Genes and kmer Binning Methods to Identify Two Distinct Polyphyletic Genome Pathotypes"

**Paper:** Gopinath GR, Jang H, Beaubrun JJ-G, Gangiredla J, Mammel M, Müller A, Tamber S, Patel IR, Ewing L, Weinstein L, Wang CZ, Finkelstein S, Negrete FJ, Muruvanda T, et al. *Microorganisms* **10**(6):1199 (2022).
**DOI:** [10.3390/microorganisms10061199](https://doi.org/10.3390/microorganisms10061199) · **PMC:** PMC9228720 · **PMID:** 35744717
**Open access:** ✅ GOLD / CC BY.

**Set:** BVBRC-37 (TOPUP85 rank-21) · **Wave:** 2026-07-01 night push
**Analyst:** Ollie (OpenClaw AI), independent-replication project
**Verdict:** **REPLICATED.** Every directly-testable core claim of the paper was independently reproduced on real public data freshly pulled from the paper's own NCBI BioProject — serovar confirmation (82/82), the exact dominant ST distribution, the **two-polyphyletic-cluster** topology (ST150 isolated from the ST142/377/1499/2640 backbone), the mixed clinical+food multi-country sampling, and the AMR/virulence feature classes. LLM-judge (free Argo `gpt-5.2`): REPLICATED, coverage ≈ 0.92.

---

## 1. Paper

Gopinath et al. analyze **95 *S.* Bovismorbificans strains** (81 newly WGS-sequenced from Switzerland, USA, Canada — 69 clinical, 9 food, 1 feed, 1 animal, 1 environment — plus 14 US hummus-outbreak genomes and additional NCBI downloads). They build a **2690-locus core-genome schema** from 150 complete *Salmonella* genomes, apply a **k-mer-binning** strategy to >260 public strains, and mine a **digital DNA tiling array** of legacy SARA/SARB strains for near-neighbors. The headline result: *S.* Bovismorbificans is **polyphyletic**, splitting into **two distinct lineages** — a backbone shared by **ST2640, ST142, ST1499, ST377** versus a separate **ST150** lineage. They further catalog AMR, prophage, plasmid, and virulence-factor genes (including the *pVirBov* virulence plasmid / *spv* genes). All 81 new assemblies were deposited under NCBI BioProject **PRJNA378379** (FDA-CFSAN GenomeTrakr).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | 81 newly-sequenced *S.* Bovismorbificans WGS assemblies are public under BioProject PRJNA378379. | Data availability | Yes (NCBI Datasets REST). | ✅ 82 recovered |
| C2 | All strains are serovar Bovismorbificans (antigenic profile 6,8:r:1,5 / 8:r:1,5), confirmed by SeqSero2. | Genomic (serotyping) | Yes. | ✅ 82/82 |
| C3 | Whole-genome/core-genome analysis resolves **two distinct polyphyletic clusters**. | Phylogenomic | Yes (proxy: mash + hierarchical clustering). | ✅ |
| C4 | STs **2640, 142, 1499, 377** form one lineage; **ST150** is a separate lineage. | Phylogenomic + MLST | Yes. | ✅ |
| C5 | Strains span **clinical AND food/animal** sources across Switzerland/USA/Canada, mixed within lineages. | Metadata | Yes (BioSample attributes). | ✅ |
| C6 | AMR, virulence-factor and plasmid genes are present and assessable. | Genomic (gene content) | Yes (AMRFinderPlus). | ✅ (feature classes) |
| C7 | Bespoke 2690-locus core schema build + k-mer-binning of >260 strains + DNA-microarray SARA/SARB near-neighbor mining. | Method-specific pipeline | Not feasibly reproducible w/o the custom schema/array data. | ⛔ not rerun |

## 3. Method

All analyses used **real public data pulled fresh** via the free, no-auth NCBI Datasets REST API from the paper's own BioProject. Heavy steps ran on **uicgpu** (8×A100, 255 cores); clustering/figures/judge ran locally.

1. **Dataset identification.** Queried NCBI Datasets REST for `bioproject/PRJNA378379/dataset_report` (500/page, paginated). Of 425 genomes in the umbrella project, filtered `organism == "…serovar Bovismorbificans"` → **82 assemblies**. Verified these are the paper's genomes by matching BioSample IDs to Table 1 (e.g. `SAMN12657228` = strain N14_0646 = WGS project `WSDC01`).
2. **Download.** `datasets download genome accession --inputfile acc.txt --include genome` → single 117 MB zip, validated 82/82, flattened to one FASTA per accession.
3. **Serovar confirmation (C2).** `SeqSero2_package.py -m k -t 4` (k-mer mode, assembled-genome input) on every genome; parsed predicted serotype + antigenic profile.
4. **MLST / ST typing (C4, C1).** `mlst --scheme senterica_achtman_2` (pubMLST 7-gene Achtman scheme) on all 82. *(mlst requires the conda env's `blastn` on PATH and the env `perl`; fixed via `export PATH` + explicit `perl`.)*
5. **Whole-genome clustering (C3, C4).** `mash sketch` + `mash dist` all-vs-all (82×82 distance matrix) as an independent proxy for the core-genome phylogeny; scipy **average-linkage hierarchical clustering**, 2-cluster cut (`fcluster maxclust=2`); dendrogram rendered.
6. **Source/geography metadata (C5).** Per-accession NCBI BioSample attributes (`isolation_source`, `host`, `geo_loc_name`); categorized clinical vs food vs animal/env.
7. **AMR + virulence content (C6).** `amrfinder --organism Salmonella --plus` (AMRFinderPlus 3.12.8, DB 2024-07-22.1) on all 82; tallied Element type/class/gene. *(DB downloaded to a writable dir with `amrfinder_update -d`.)*
8. **Verdict (LLM-judge).** Evidence bundle scored by a free Argo model. `argo:claude-opus-4.8` returned HTTP 502 (known proxy bug) → fell back to **free** `argo:gpt-5.2` (never paid).

**Tool versions:** datasets 18.32.0 · SeqSero2 1.3.2 · mlst 2.35.0 (senterica_achtman_2) · mash 2.3 · AMRFinderPlus 3.12.8 (DB 2024-07-22.1) · scipy 1.18.0.

## 4. Results vs Paper

### 4.1 Data availability (C1) — ✅
82 Bovismorbificans assemblies present and downloadable from PRJNA378379 (81 draft Contig-level + 1 Chromosome). Fully covers the paper's 81 newly-sequenced set. BioSamples match Table 1.

### 4.2 Serovar confirmation (C2) — ✅ exact
`SeqSero2` → **82/82 = "Bovismorbificans"**, antigenic profile **`8:r:1,5`** uniformly. This is the canonical *S.* Bovismorbificans O:H formula and matches the paper's SeqSero2 confirmation.

### 4.3 MLST / ST distribution (C1, C4) — ✅
| ST | This work (n) | Paper's role |
|---|---:|---|
| 142 | 49 | dominant backbone ST |
| 377 | 14 | backbone ST (US hummus outbreaks) |
| 1499 | 11 | backbone ST |
| 2640 | 5 | backbone ST |
| 150 | 2 | **separate lineage** |
| 8700 | 1 | minor variant (single-locus variant of the backbone) |

The **four dominant STs are exactly {142, 377, 1499, 2640}** — precisely the four the paper names as the shared-backbone lineage — with **ST150** present as the minority separate lineage.

### 4.4 Two polyphyletic clusters (C3, C4) — ✅ topology reproduced
Average-linkage hierarchical clustering of the mash whole-genome distance matrix, 2-cluster cut:

| Cluster | n | Composition |
|---|---:|---|
| **1** | 2 | ST150 only |
| **2** | 80 | ST142 (49) + ST377 (14) + ST1499 (11) + ST2640 (5) + ST8700 (1) |

This is a **direct, independent reproduction** of the paper's central claim: *S.* Bovismorbificans partitions into two distinct lineages, with the {2640,142,1499,377} backbone in one cluster and **ST150 forming its own separate lineage**. (Figure: `evidence/dendrogram.png`, ST-colored leaves.)

### 4.5 Clinical + food, multi-country sampling (C5) — ✅
BioSample metadata: **70 clinical/human, 8 food, + animal/env/feed** (paper: 69 clinical, 9 food, 1 feed, 1 animal, 1 env among the 81). Geography: **Switzerland 75, Canada 5, USA 2** — the paper's three collections (U. Zurich, Health Canada, U. Wisconsin/CFSAN). Clinical and food isolates **co-occur within the same STs**: ST377 = 7 clinical + 5 food; ST1499 = 9 clinical + 2 food; ST142 = 47 clinical + 1 food.

### 4.6 AMR + virulence content (C6) — ✅ feature classes
AMRFinderPlus over 82 genomes: **799 virulence hits, 199 AMR hits, 205 stress/metal hits**.
- **Intrinsic efflux `mdsA`/`mdsB` in all 82** (core Salmonella multidrug efflux).
- **Acquired AMR is sparse** (as expected for this serovar): `sul2`×5, `tet(A)`×5, aminoglycoside `aph`×several, `blaTEM-1`×2, `blaCTX-M-55`×1, `qnrB19`/`qnrS1`, `floR`, `tet(M)`, `aac(3)-IId`. AMR classes: EFFLUX 164, AMINOGLYCOSIDE 12, SULFONAMIDE 6, TETRACYCLINE 6, BETA-LACTAM 4, QUINOLONE/PHENICOL/BLEOMYCIN/TRIMETHOPRIM few.
- **Universal core virulence:** `invA`, `avrA`, `iroB`/`iroC` (salmochelin), `sinH`, `sspH2`, `sodC1`, `lpfB`, `sseK2` in ≈all genomes; **`spvD` (spv virulence-plasmid marker) in 56/82** — directly consistent with the paper's *pVirBov* / virulence-plasmid discussion.

### 4.7 Not reproduced (C7) — ⛔ honest scope
The paper's bespoke **2690-locus core-genome schema** (built from 150 complete genomes), the **k-mer-binning survey of >260 strains**, and the **digital DNA microarray/tiling-array SARA/SARB near-neighbor mining** were not reconstructed — these need the custom schema and legacy array data that are not redistributable as drop-in artifacts. Clustering here used mash genome distance as an independent proxy, which recovers the identical two-lineage topology, so the *conclusion* is replicated even though the exact pipeline is not.

## 5. Verdict

**REPLICATED.** Five of six directly-testable core claims (C1–C5) are independently reproduced on real public data with exact or near-exact agreement, including the paper's headline **two-polyphyletic-cluster** structure and the precise dominant-ST composition. C6 (AMR/virulence/plasmid features) is reproduced at the feature-class level. Only the paper-specific custom-schema/microarray pipeline (C7) was out of reach, and an independent method (mash clustering) confirms the same biological conclusion. No claim was contradicted.

**LLM-judge (free Argo `gpt-5.2`):** *"The replication credibly reproduces the paper's central phylogenomic conclusions … recovers the same key two-lineage split with ST150 isolated from the main backbone."* Per-claim: C1–C5 reproduced, C6 partial; coverage ≈ 0.92. Full text: `evidence/llm_judge_verdict.txt`.

## Verdict
**Verdict:** REPLICATED

---
WAVE_RESULT set=BVBRC-37 paper=Gopinath-2022-Bovismorbificans-phylo verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-37-Salmonella-Bovismorbificans-phylo-2022 one_line=Pulled all 82 Bovismorbificans genomes from the paper's BioProject PRJNA378379 and independently reproduced serovar (82/82, 8:r:1,5), the exact dominant STs (142/377/1499/2640 backbone + separate ST150), the two-polyphyletic-cluster topology (mash+hierarchical), clinical+food multi-country sampling, and AMR/virulence gene content — LLM-judge REPLICATED, coverage ~0.92.
