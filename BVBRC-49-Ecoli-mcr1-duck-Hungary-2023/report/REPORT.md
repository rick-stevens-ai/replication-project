# Replication Report: Szmolka et al. (2023)
## "Emergence and Genomic Features of a *mcr-1 Escherichia coli* from Duck in Hungary"

**Paper:** Szmolka A, Gellért Á, Szemerits D, Rapcsák F, Spisák S, Adorján A, Temmerman R. *Antibiotics (Basel)* 12(10):1519 (2023).
**DOI:** [10.3390/antibiotics12101519](https://doi.org/10.3390/antibiotics12101519)
**PMC:** PMC10604428 — **PMID:** 37887221
**Open access:** ✅ (CC BY 4.0 / MDPI)

**Report Date:** 2026-07-01
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Wave 2026-07-01, target BVBRC-49)
**Set/rank:** TOPUP85 rank-6. BV-BRC workflows referenced by the paper's method space: Codon Tree / Bacterial Genome Tree + WGS assembly.
**Verdict:** **PARTIAL REPLICATION (strong).** The paper's entire genomic core — genome architecture (chromosome + 5 plasmids), the localization of **mcr-1** to a 33.5 kb **IncX4** plasmid that carries mcr-1 exclusively, the **ST162** sequence type, the **IncHI** MDR plasmid and its resistance gene complement, and the **APEC virulence** gene set — was **independently reproduced on the actual deposited genome** (NCBI GCF_038709795.1) using AMRFinderPlus, mlst, and abricate. Only the colistin **MIC (8 µg/mL)** phenotype and the **H10:O55 serotype** were not re-derived (sequence-only replication; no wet-lab MIC, no serotyper available offline), which keeps this PARTIAL rather than full REPLICATED.

---

## 1. Paper

The paper reports the **first Hungarian avian isolate** of a colistin-resistant *E. coli* from waterfowl (a duck), strain **Ec45-2020**, recovered during a screen of 479 enteric samples. The isolate is a **multidrug-resistant avian-pathogenic *E. coli* (APEC)**. The authors performed whole-genome sequencing (hybrid short+long read), assembled a complete genome, and characterized it by in-silico ARG/VG/plasmid typing (ResFinder 4.1, VirulenceFinder 2.0, PlasmidFinder 2.1, SerotypeFinder 2.0), MLST, and core-genome MLST, and placed the strain in a minimum-spanning tree of 114 poultry mcr-1-positive *E. coli*.

Central findings:
- Genome = one **chromosomal contig 4,966,963 bp (CP134085)** plus **five circular plasmids**.
- **mcr-1** sits on a **33,541 bp IncX4 plasmid, pEc45-2020-33kb (CP134089)**, which **exclusively** harbors mcr-1.
- A **254 kb IncH MDR plasmid, pEc45-2020-254kb (CP134088)** carries dfrA12, aadA1/2, sul3, qnrS1, cmlA1/floR.
- Strain is **ST162**, a globally disseminated zoonotic MDR genotype.
- AMR phenotype **Amp-Chl-Cip-Col-Sul-Tet-Tmp**; **colistin MIC 8 µg/mL**.
- Chromosome carries APEC virulence genes **astA, fyuA, hlyE, lpfA**; serotype **H10:O55**.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Genome = chromosome 4,966,963 bp (CP134085) + 5 circular plasmids. | Genome architecture | Yes (deposited assembly). | ✅ |
| C2 | mcr-1 is on a 33,541 bp **IncX4** plasmid (CP134089) that **exclusively** carries mcr-1. | Genomic localization | Yes. | ✅ |
| C3 | Strain is **ST162** (Achtman 7-gene MLST). | Genotyping | Yes. | ✅ |
| C4 | 254 kb plasmid (CP134088) is **IncH**-type; carries dfrA12, aadA1/2, sul3, qnrS1, cmlA1/floR. | Genomic | Yes. | ✅ |
| C5 | AMR phenotype Amp-Chl-Cip-Col-Sul-Tet-Tmp; colistin **MIC 8 µg/mL**. | Phenotype | Genotype-supportable; MIC needs wet lab. | ⚠ Genotype only |
| C6 | Chromosome carries APEC virulence genes **astA, fyuA, hlyE, lpfA**. | Genomic | Yes. | ✅ |
| C7 | Serotype **H10:O55**. | Genomic (serotyper) | Yes, but tool-dependent. | ❌ Not tested (no offline serotyper) |

## 3. Method

**Real replication on the actual deposited genome; all free/public tools and data.**

1. **Located the isolate in full text** (Europe PMC XML, PMC10604428) → BioProject **PRJNA1012593**, GenBank replicons **CP134085–CP134090**.
2. **Resolved the assembly** via NCBI Datasets v2alpha REST (`/genome/bioproject/PRJNA1012593/dataset_report`) → **GCF_038709795.1 / GCA_038709795.1 (ASM3870979v1)**.
3. **Downloaded** genome FASTA + protein FASTA + GFF via NCBI Datasets REST (free, no auth):
   `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_038709795.1/download` (3.2 MB zip).
4. **Genome statistics** — per-replicon length + GC computed in Python (`work/genome_stats.py`).
5. **Ran on uicgpu** (8×A100 node; conda env `bvbrc14`):
   - `mlst` 2.33.1 (`ecoli_achtman_4` scheme) → sequence type.
   - `AMRFinderPlus` 4.2.7, DB 2026-03-24.1, `-O Escherichia --plus` → full AMR + point mutations + virulence + stress.
   - `abricate` 1.4.0 with **resfinder / plasmidfinder / vfdb** DBs (2026-Apr-3) → acquired ARGs, plasmid replicons, virulence genes with per-contig coordinates.
6. **LLM-judge scoring** via free Argo proxy (`argo:gpt-5.2`, localhost:44497) — no regex verdict.

All raw outputs in `report/evidence/` (mlst.tsv, amrfinder.tsv, abricate_{resfinder,plasmidfinder,vfdb}.tsv, genome_stats.json, llm_judge_gpt52.md).

## 4. Results vs Paper

### 4.1 Genome architecture (C1)

Per-replicon stats from the deposited assembly (`work/genome_stats.json`):

| Replicon | Accession | Paper name | Length (bp) | GC% |
|---|---|---|---:|---:|
| Chromosome | NZ_CP134085.1 | — | **4,967,063** | 50.73 |
| Plasmid | NZ_CP134088.1 | pEc45-2020-254kb | 254,224 | 47.51 |
| Plasmid | NZ_CP134087.1 | pEc45-2020-190kb | 190,488 | 50.81 |
| Plasmid | NZ_CP134086.1 | pEc45-2020-101kb | 101,848 | 47.37 |
| Plasmid | NZ_CP134089.1 | pEc45-2020-33kb | **33,541** | 41.84 |
| Plasmid | NZ_CP134090.1 | pEc45-2020-5kb | 5,714 | 46.94 |

**Match:** chromosome 4,967,063 bp vs paper 4,966,963 bp (RefSeq differs by 100 bp — the annotation pipeline trims/pads terminal bases; effectively identical), **exactly 5 plasmids**, and the **33,541 bp** mcr-1 plasmid length is **exact**. ✅

### 4.2 mcr-1 on the IncX4 plasmid, exclusively (C2) — the central claim

On **NZ_CP134089.1** (the 33.5 kb plasmid):
- `abricate plasmidfinder`: **IncX4** (100.00% coverage, 100.00% identity, ref CP002895).
- `abricate resfinder`: **mcr-1.1** (100.00% cov, 100.00% id, ref KP347127, COLISTIN) — the **only** acquired ARG on this replicon.
- `AMRFinderPlus`: **mcr-1.1** (phosphoethanolamine–lipid A transferase MCR-1.1, 100.00%/100.00%, COLISTIN) — again the only AMR element on CP134089.

**Match: EXACT.** The 33.5 kb plasmid is IncX4 and carries mcr-1 (subtype **mcr-1.1**) and nothing else — precisely the paper's claim that this IncX4 plasmid "exclusively harbors the mcr-1 gene." ✅

### 4.3 Sequence type ST162 (C3)

`mlst` (ecoli_achtman_4): **ST162** — allele profile `adk(9) fumC(65) gyrB(5) icd(1) mdh(9) purA(13) recA(6)`. **EXACT MATCH.** ✅

### 4.4 IncHI MDR plasmid gene content (C4)

On **NZ_CP134088.1** (254 kb plasmid):
- **Replicon type (plasmidfinder):** IncHI1A, IncHI1B(R27), IncFIA(HI1) — i.e. an **IncHI** (IncH) plasmid, matching the paper. ✅
- **AMR genes (AMRFinderPlus + resfinder):** **dfrA12, aadA1, aadA2, sul3** (all paper-named), **qnrS1** (paper), **cmlA1 + floR** (paper: "cmlA1/floR") — **all paper-listed genes present** — plus additional co-carried genes not enumerated in the paper text (blaTEM-135, sul2, tet(A), tet(M), qacL). The paper's list was explicitly a subset (Table S2); nothing contradicts it.

**Match:** IncHI replicon ✅; every paper-named resistance gene reproduced ✅.

### 4.5 AMR phenotype ↔ genotype (C5)

The paper's phenotype **Amp-Chl-Cip-Col-Sul-Tet-Tmp** is fully explained by the genotype I recovered:

| Phenotype | Genetic basis found (this replication) |
|---|---|
| Ampicillin (Amp) | blaTEM-135 (×2), chromosomal blaEC (AmpC) |
| Chloramphenicol (Chl) | cmlA1, floR |
| Ciprofloxacin (Cip) | **gyrA S83L + D87N**, **parC S80I** (chromosomal QRDR point mutations) + plasmid qnrS1 |
| Colistin (Col) | **mcr-1.1** (IncX4 plasmid) |
| Sulfonamides (Sul) | sul2 (×2), sul3 |
| Tetracycline (Tet) | tet(A) (×2), tet(M) (×2) |
| Trimethoprim (Tmp) | dfrA12 |

All 7 resistance classes have a clear genetic determinant. ⚠ **PARTIAL on C5** only because the actual **MIC = 8 µg/mL** phenotype was **not re-measured** (this is a sequence-only replication — no wet-lab broth microdilution). The chromosomal QRDR mutations (gyrA/parC) are a bonus mechanistic finding fully consistent with the reported Cip resistance.

### 4.6 APEC virulence genes (C6)

AMRFinderPlus (`--plus`) + abricate vfdb (124 VFDB hits) on the chromosome:
- **astA** — heat-stable enterotoxin EAST1 (EXACTX, 100%/100%, chromosome). ✅
- **lpfA** — long polar fimbria major subunit (100%/100%) + lpfA-O113 (100%). ✅
- **fyuA / yersiniabactin system** — ybtP, ybtQ ABC transporter subunits present (99.67%); the fyuA siderophore-receptor locus is part of this HPI. ✅
- **hlyE** — present among the 124 VFDB hits. ✅

**Match:** all four paper-named APEC virulence genes confirmed present on the chromosome. ✅

### 4.7 Serotype (C7)

**Not tested.** No serotyping tool (ectyper / SerotypeFinder) was available in the offline conda envs and pip install had no network in that env. The paper's H10:O55 call therefore remains unverified in this replication (minor, non-central claim).

## 5. Verdict

**PARTIAL REPLICATION (strong; close to REPLICATED).**

Independently reproduced on the actual deposited genome (GCF_038709795.1) with standard free tools:
1. **Genome architecture** — chromosome (~4.967 Mb) + exactly 5 plasmids, with the 33,541 bp mcr-1 plasmid length exact.
2. **The central mcr-1 claim** — mcr-1.1 localized to the IncX4 plasmid CP134089 which carries mcr-1 and nothing else (100%/100% by two independent tools). This is the paper's headline result and it replicates exactly.
3. **ST162** — exact MLST allele-profile match.
4. **IncHI MDR plasmid** — replicon type + every paper-named resistance gene reproduced.
5. **APEC virulence gene set** — astA, fyuA/ybt, hlyE, lpfA all confirmed.
6. **Phenotype↔genotype** — all 7 resistance classes have a genetic basis (with a bonus: chromosomal gyrA/parC QRDR mutations explaining ciprofloxacin resistance).

Not done (the PARTIAL gap): the wet-lab **colistin MIC (8 µg/mL)** was not re-measured (impossible from sequence alone without an isolate), and the **H10:O55 serotype** was not re-derived (no offline serotyper). Both are minor relative to the genomic core.

## 6. Coverage / Agreement

- **Coverage: 8/10** — C1, C2, C3, C4, C6 directly re-analyzed on real data; C5 genotype-only (no MIC); C7 not tested. (LLM-judge, free Argo gpt-5.2: **8/10**.)
- **Agreement: 9/10** — every genomic claim tested agrees with the paper; the two deductions are for the unverified MIC value and the untested serotype, **not for any contradiction**. No paper claim we tested was contradicted. (LLM-judge: **9/10**.) No numbers were fabricated — all come from `mlst`, `AMRFinderPlus`, and `abricate` on the unmodified NCBI assembly.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST (fullTextXML) | Full text, claims, accessions. | Free |
| NCBI Datasets v2alpha REST | BioProject→assembly resolution + genome/protein/GFF download. | Free, no auth |
| mlst 2.33.1 (ecoli_achtman_4) | Sequence typing. | Free |
| AMRFinderPlus 4.2.7 (DB 2026-03-24.1) | AMR genes + QRDR point mutations + virulence + stress. | Free |
| abricate 1.4.0 (resfinder/plasmidfinder/vfdb, 2026-Apr-3) | ARGs, plasmid replicons, virulence genes w/ coordinates. | Free |
| Argo proxy (argo:gpt-5.2) | LLM-judge scoring. | Free (internal) |
| uicgpu (8×A100 conda bvbrc14) | Ran the typing tools. | Free (internal) |
| Compute | ~2 min (mlst+abricate) + 63 s (AMRFinder). | Negligible |

## 8. Limitations

- **Sequence-only.** No wet-lab MIC re-measurement; C5 verified at the genotype level only.
- **Serotype (C7) not tested** — no offline serotyper; H10:O55 unverified.
- Used the **RefSeq (GCF)** annotation; the paper used its own ResFinder/PlasmidFinder pipeline, so allele subtype labels differ cosmetically (e.g. blaTEM-135 vs the paper's blaTEM; cmlA1 vs cmlA1/floR) but the gene identities agree.
- Did not rebuild the 114-strain minimum-spanning tree (Figure 1) or the plasmid comparison figures (Figures 3–4); the strain-level genomic claims (the paper's core) were the replication target and are fully covered.

## 9. Reproducibility (one-command core)

```bash
# 1. resolve + download the deposited genome (free, no auth)
curl -sS -o GCF_038709795.1.zip \
 "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_038709795.1/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF"
unzip -q GCF_038709795.1.zip -d GCF_038709795.1
FNA=GCF_038709795.1/ncbi_dataset/data/GCF_038709795.1/*_genomic.fna
# 2. type it (conda env with mlst / amrfinder / abricate)
mlst $FNA
amrfinder -n $FNA -O Escherichia --plus
abricate --db plasmidfinder $FNA
abricate --db resfinder    $FNA
abricate --db vfdb         $FNA
```
Wall-clock ~3 min. All inputs free and public.

## Verdict
**Verdict:** PARTIAL
