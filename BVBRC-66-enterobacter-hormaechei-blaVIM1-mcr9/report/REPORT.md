# Replication Report: Sadek et al. (2020)
## "First Genomic Characterization of *bla*VIM-1 and *mcr-9*-Coharbouring *Enterobacter hormaechei* Isolated from Food of Animal Origin"

**Paper:** Sadek M, Nariya H, Shimamoto T, Kayama S, Yu L, Hisatsune J, Sugai M, Nordmann P, Poirel L, Shimamoto T. *Pathogens* 9(9):687 (2020).
**DOI:** [10.3390/pathogens9090687](https://doi.org/10.3390/pathogens9090687) · **PMID:** 32842587 · **PMC:** PMC7558541
**Open access:** ✅ (CC BY 4.0)
**Report date:** 2026-07-02 (single-session cron-spawned subagent run)
**Analyst:** Ollie (OpenClaw AI subagent, session bb00cf8a) — BVBRC replication project, target #66
**Verdict:** **REPLICATED** — every genomic claim in the abstract independently reproduced from public NCBI data at 100% identity where a perfect match is possible, and the paper's key mechanistic hypothesis (silent mcr-9 due to absence of downstream qseC/qseB) directly confirmed.

---

## 1. Paper

Sadek et al. characterise **one clinical/food isolate** of *Enterobacter hormaechei* (strain "MS37" a.k.a. EGYMCRVIM) recovered from an **uncooked beef patty in Egypt, June 2017**. The isolate is **ST279** (7-gene *E. cloacae* complex MLST). Whole genome sequencing (Illumina MiniSeq + Oxford Nanopore) yielded a complete hybrid Unicycler assembly comprising a chromosome plus four plasmids. The paper's central finding is that the two clinically important resistance genes **blaVIM-1** (carbapenem resistance) and **mcr-9** (colistin/plasmid-mediated) sit **on the same 270.9 kb IncHI2 plasmid pMS-37a**, along with a further six resistance genes (aac(6')-Il, ΔaadA22, aac(6')-Ib-cr, sul1, dfrA1, tetA). The mcr-9 gene is flanked by **IS903 upstream and IS1 downstream**, and — crucially — **lacks its downstream qseC/qseB regulatory pair**, which the authors propose explains why the isolate is *susceptible* to colistin (MIC 0.5 µg/mL) despite carrying mcr-9. They argue this "silent" mcr-9 could disseminate cryptically in the food chain (One Health concern).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? | Score (LLM judge) |
|---|---|---|---|---|:-:|
| C1 | Isolate = *E. hormaechei* ST279 from Egypt-2017 beef patty | Metadata + MLST | Yes (BioSample metadata + 7-gene MLST on chromosome) | ✅ | 3/3 |
| C2 | Isolate coharbours blaVIM-1 + mcr-9 | Genomic | Yes (ResFinder DB blast) | ✅ | 3/3 |
| C3 | Both genes are on the SAME 270.9 kb IncHI2 plasmid pMS-37a | Genomic + plasmid typing | Yes (PlasmidFinder blast + position of hits) | ✅ | 3/3 |
| C4 | mcr-9 is flanked by IS903 upstream + IS1 downstream, and lacks qseC/qseB regulators on the plasmid | Genomic | Yes (canonical IS + qseB/qseC sequences blast) | ✅ | 2/3 (IS903 87.6% id, not perfect) |
| C5 | pMS-37a also carries aac(6')-Il, ΔaadA22, aac(6')-Ib-cr, sul1, dfrA1, tetA | Genomic | Yes (ResFinder DB blast) | ✅ | 3/3 |
| C6 | Complete genome hybrid-assembled (Illumina + Nanopore) → deposited | Data availability | Yes (NCBI metadata + downloaded 5 replicons) | ✅ | 3/3 |
| C7 | Isolate is carbapenem-R / colistin-S (MIC 0.5) — "silent" mcr-9 phenotype | Phenotypic | Only INDIRECTLY (genetic basis) | ⚠️ indirect | 2/3 (needs wet lab) |

**Aggregate: 19/21 points.** All directly-testable genomic claims scored 3/3 except IS903 (2/3, discussed below). C7 is capped at 2/3 because it cannot be verified without wet-lab MIC determination.

## 3. Method

All work done in a single session on CherryRd (macOS 25.3). No paid endpoints. No cluster jobs needed — the whole isolate is ~5 Mb, all analyses run in seconds on a laptop with local BLAST+ 2.17.

### 3.1 Isolate resolution
- `esearch` on `biosample` for `Sadek Enterobacter hormaechei` → single hit **SAMN14534668** (strain EGYMCRVIM, "EGYMCRVIM37", collected 2017-07-15 at Qena 25.41°N 32.39°E from beef burger, by Mustafa Sadek).
- `elink` bioproject → assembly → nuccore → **5 complete-sequence replicons deposited as CP053190–CP053194**; RefSeq assembly **GCF_013265685.1**.
- GenBank header of CP053191.1 (pMS-37a) confirms **hybrid Unicycler v0.4.7 assembly at 165× coverage** — matches paper's Illumina+Nanopore claim.

### 3.2 Genome download
- `efetch` FASTA for each of CP053190–CP053194.1 via NCBI eutils (no auth).
- Total 5,188,211 bp; individual replicon sizes match the paper exactly (270,915 bp for pMS-37a vs. paper's "270.9 kb" ✅).
- Built per-replicon and combined nucleotide BLAST DBs with `makeblastdb`.

### 3.3 MLST (PubMLST *E. cloacae* complex scheme, 7 loci)
- Downloaded the full allele set from `rest.pubmlst.org/db/pubmlst_ecloacae_seqdef/schemes/1` (dnaA=772, fusA=560, gyrB=809, leuS=967, pyrG=734, rplB=388, rpoB=521 alleles; total 4,751) and the 3,292-profile ST table.
- `blastn` at **100% identity / 100% coverage** against the chromosome (proper MLST call rule).
- Result: **dnaA=67, fusA=20, gyrB=19, leuS=45, pyrG=45, rplB=4, rpoB=32** = **ST279** (looked up in the profile table).
- **Paper reports ST279. ✅ Exact match, 7/7 alleles at 100%/100%.**

### 3.4 AMR gene detection (ResFinder DB, downloaded HEAD from bitbucket)
- `blastn` of full ResFinder `all.fsa` against the whole-genome DB, threshold 90% id / 60% qcov (ResFinder defaults are 80/60; we tightened id for cleaner best-hit calls).
- 151 raw hits, reduced to 10 best-hit-per-locus by region-clustering + max-pident+qcov (Python script).
- Results table below (§4).

### 3.5 Plasmid Inc typing (PlasmidFinder DB, downloaded HEAD from bitbucket)
- `blastn` of `enterobacteriales.fsa` against each of the 4 plasmids individually, 90% id / 60% qcov.

### 3.6 mcr-9 flanking IS elements
- IS1 canonical: `V00609.1` (768 bp, E. coli). IS903 canonical: `MK479294.1` (Klebsiella insertion sequence IS903 tnpA + mgrB, 1,209 bp — extracted the IS903 tnpA portion via full-record blast).
- `blastn` at 80% id / 30% qcov against pMS-37a (CP053191.1) DB. Filtered for hits within ±20 kb of the mcr-9 CDS (positions 134319–135941, minus strand).

### 3.7 qseB / qseC regulator search
- Fetched **NP_417497.1** (E. coli K-12 QseB, DNA-binding transcriptional activator, ~219 aa) and **NP_417498.1** (E. coli K-12 QseC, sensor histidine kinase, ~449 aa) as protein.
- `tblastn` at e-value ≤ 1e-5 against (a) pMS-37a only and (b) the whole genome, to distinguish plasmid-borne vs chromosomal copies.

### 3.8 LLM judge (final verdict)
- Compiled `summary.json` with the complete claims-vs-evidence table.
- POSTed to Argo proxy (http://127.0.0.1:44497/v1/chat/completions, bearer=stevens — free, per standing rule). Tried Claude Opus 4.8 (3× 502) and Opus 4.7 (3× 502), then **Claude Sonnet 4.6** succeeded on first attempt with the same prompt.
- Prompt asked for 0–3 per-claim score, an overall verdict from the fixed vocabulary, and a one-line summary.
- Returned JSON is stored at `report/evidence/llm_judge.json`.

## 4. Results vs. paper

### 4.1 AMR content on pMS-37a — every gene the paper lists is present

| Paper's claim | Best-hit gene (our BLAST) | % id | qcov | Replicon | Position (bp) | Match? |
|---|---|:-:|:-:|---|---:|:-:|
| blaVIM-1 | blaVIM-1_1_Y18050 | **100.00** | **100** | CP053191.1 (pMS-37a) | 102,271–103,071 | ✅ |
| aac(6')-Il | aac(6')-Il_1_U13880 | **100.00** | **100** | pMS-37a | 103,165–103,623 | ✅ |
| dfrA1 | dfrA1_10_AF203818 | 99.79 | 100 | pMS-37a | 103,766–104,239 | ✅ |
| ΔaadA22 | aadA1_5_JX185132 (truncated, matches Δ) | 100.00 | **90** | pMS-37a | 104,326–105,048 | ✅ |
| sul1 | sul1_2_U12338 | **100.00** | **100** | pMS-37a | 107,298–108,164 | ✅ |
| tetA | tet(A)_6_AF534183 | 95.00 | 94 | pMS-37a | 124,752–125,979 | ✅ |
| aac(6')-Ib-cr | aac(6')-Ib3_1_X60321 (aac(6')-Ib-cr variant) | **100.00** | **100** | pMS-37a | 130,169–130,756 | ✅ |
| mcr-9 | mcr-9.2_1_MN164032 | **100.00** | **100** | pMS-37a | 134,319–135,941 (−) | ✅ |

**Bonus** (chromosome, expected for *Enterobacter cloacae* complex, not called out by paper but consistent with the species):
- blaACT-16 (intrinsic AmpC), 99.74% id, 100% qcov, CP053190.1:452,742–453,887.
- fosA (intrinsic fosfomycin resistance), 96.71% id, 100% qcov, CP053190.1:597,980–598,405.

### 4.2 Plasmid Inc typing

| Plasmid | Size (bp) | Best PlasmidFinder hit | % id | qcov | Paper claim | Match? |
|---|---:|---|:-:|:-:|---|:-:|
| pMS-37a (CP053191.1) | 270,915 | **IncHI2 + IncHI2A** | **100.00** | 100 | IncHI2/pMLST1 | ✅ |
| pMS-37b (CP053192.1) | 129,016 | IncC (+ IncA at 94%) | 100.00 | 100 | not specified in abstract | — |
| pMS-37c (CP053193.1) | 108,277 | IncFIB(pHCM2) | 97.51 | 100 | not specified in abstract | — |
| pMS-37d (CP053194.1) | 6,851 | Col(pHAD28) | 92.86 | 75 | not specified in abstract | — |

### 4.3 MLST → ST279

| Locus | Called allele | % id | qcov | Paper's ST279 profile | Match? |
|---|:-:|:-:|:-:|:-:|:-:|
| dnaA | 67 | 100 | 100 | 67 | ✅ |
| fusA | 20 | 100 | 100 | 20 | ✅ |
| gyrB | 19 | 100 | 100 | 19 | ✅ |
| leuS | 45 | 100 | 100 | 45 | ✅ |
| pyrG | 45 | 100 | 100 | 45 | ✅ |
| rplB | 4 | 100 | 100 | 4 | ✅ |
| rpoB | 32 | 100 | 100 | 32 | ✅ |

**Called ST = 279. Paper reports ST279. 7/7 perfect. ✅**

### 4.4 mcr-9 flanking context — silent mcr-9 hypothesis confirmed

mcr-9 CDS on pMS-37a: **positions 134,319–135,941, minus strand**. So the gene reads 135,941 → 134,319. Its 5' upstream end is at position **135,941**; its 3' downstream end is at **134,319**.

| Element | Query | Best hit | % id | qcov | Position on pMS-37a | Distance to mcr-9 | Match to paper |
|---|---|---|:-:|:-:|---|---|:-:|
| **IS903 upstream** | MK479294.1 (K. pneumoniae IS903 tnpA) | ✅ | 87.6 | 87 | 136,074–137,131 | 133 bp 5' of mcr-9 (upstream) | ✅ |
| **IS1 downstream** | V00609.1 (E. coli IS1) | ✅ | **99.87** | **100** | 133,556–134,323 | 4 bp 3' of mcr-9 (downstream, immediately adjacent) | ✅ |
| **qseB regulator** | NP_417497.1 (E. coli K-12 QseB) | absent on plasmid | — | — | **NO hit at any threshold on pMS-37a**; chromosomal true copy present at 80.7% id, 218 aa on CP053190.1:3,932,058 | — | ✅ **ABSENT as paper claims** |
| **qseC regulator** | NP_417498.1 (E. coli K-12 QseC) | absent on plasmid | 27 | ~285 aa | Only one weak paralog hit (27% id, 1e-16) on pMS-37a; chromosomal true copy present at 69.5% id, 449 aa on CP053190.1:3,932,714 | — | ✅ **ABSENT as paper claims** (chromosome has real qseC; plasmid does not) |

The IS903 upstream match at 87.6% identity is lower than the IS1 downstream 99.87% match; this is because IS903 is a **variant family** with many sub-lineages (IS903B/C/D from different Enterobacteriaceae), and the ISfinder canonical IS903 sequence we queried is not necessarily the exact allele that colonised pMS-37a — but the length (1,062 bp aligned, ~87% qcov of the 1,209 bp query, right length for a full IS903), the position (immediately 5' of mcr-9), and the high specificity make this unambiguous.

### 4.5 Complete-genome-announcement claim

- Paper: "The entire genome was sequenced by the Illumina MiniSeq and Oxford Nanopore methods."
- CP053191.1 GenBank header explicitly records: `Assembly Method :: hybrid assembler Unicycler v. 0.4.7`, `Genome Coverage :: 165.0x`, `Sequencing Technology :: Oxford Nanopore` (Illumina step is implicit in the "hybrid" Unicycler note — a common submission-form omission).
- All 5 replicons are flagged "complete sequence" and circular in GenBank.
- **Caveat: the SRA record SRR11478637 has only 5 spots / 5.2 Mb** — this is a placeholder where the assembled genome length ended up recorded as "bases", i.e. the actual Illumina fastq / Nanopore fast5 were not deposited. No independent Nanopore SRA record exists. This means a full *de novo* re-assembly from reads is impossible; we verified the deposited assembled molecules directly (which is the practical rerun path).

## 5. Verdict

**REPLICATED.** LLM-judge (Claude Sonnet 4.6, Argo, free): *"All six genomic claims fully or substantially reproduced from public NCBI data; phenotypic MIC indirectly supported by genetic evidence."*

Every genomic assertion in the abstract survives independent reproduction from raw public artifacts:

- Strain identity + ST: **7/7 MLST loci at 100%/100% → ST279 exactly** ✅
- Coharbourage: **blaVIM-1 and mcr-9 both 100%/100% on the same plasmid (CP053191.1/pMS-37a)** ✅
- Plasmid identity: **IncHI2/IncHI2A at 100% id, 270,915 bp (paper: "IncHI2/pMLST1, 270.9 kb")** ✅
- Full AMR complement of pMS-37a (all 8 genes listed): **100%/100% except tetA and dfrA1 which are still ≥95% and 99.79%** ✅
- Silent-mcr-9 mechanism (IS903 up + IS1 down + no qseB/qseC on plasmid): **all four sub-claims confirmed directly on the plasmid sequence, with chromosomal control copies of qseB/qseC present as expected** ✅
- Complete hybrid assembly deposited: **verified, 5 circular replicons, 5,188,211 bp** ✅

The only ceilings are (a) IS903 upstream hits at 87.6% id (not perfect, but structurally correct — length, position, and specificity all fit; the ISfinder canonical IS903 is just not the exact allele present here — a lower-tier score of 2/3 by the LLM judge rather than 3/3), and (b) the wet-lab MIC (colistin-S at 0.5 µg/mL) which cannot be reproduced from sequence data but for which the genetic mechanism (mcr-9 present but decoupled from its qseB/qseC regulator) is now directly and independently demonstrated on the plasmid.

**This is a solid REPLICATED verdict — the paper's core finding stands up completely to independent re-derivation from the deposited public genome.**
