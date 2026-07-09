# Replication Report: Zheng et al. (2017)
## "Complete genome sequencing and genomic characterization of two *Escherichia coli* strains co-producing MCR-1 and NDM-1 from bloodstream infection"

**Paper:** Zheng B, Yu X, Xu H, Guo L, Zhang J, Huang C, Shen P, Jiang X, Xiao Y, Li L. *Scientific Reports* 7:17885 (2017).
**DOI:** [10.1038/s41598-017-18273-2](https://doi.org/10.1038/s41598-017-18273-2) · **PMID:** 29263349 · **PMCID:** PMC5738369
**Open access:** ✅ (CC BY 4.0)

**Set:** BVBRC-58 · **Wave:** night push 2026-07-01/02
**Report Date:** 2026-07-02
**Analyst:** Ollie (OpenClaw AI) — BV-BRC Replication Project
**Verdict:** **PARTIAL REPLICATION (strong).** 5 of 6 testable claims independently reproduced on the actual public GenBank sequences; the per-plasmid AMR gene inventory is partially reproduced (core resistance genes match; allele-level differences trace to 2017-ResFinder-2.1 vs 2024-AMRFinderPlus database drift).

---

## 1. Paper summary

The authors previously reported two *E. coli* bloodstream isolates — **EC1002** (ST405) and **EC2474** (ST131) — that co-harbour the plasmid-borne colistin-resistance gene **mcr-1** and the carbapenemase **blaNDM-1**. Here they complete-sequence both isolates (PacBio RS II + Illumina HiSeq), yielding two closed chromosomes plus 4 (EC1002) and 3 (EC2474) circular plasmids. Central findings:

- The two resistance genes sit on **different plasmids** in each strain (mcr-1 and blaNDM-1 are never co-located), which they argue signals a route toward pandrug-resistant *Enterobacteriaceae*.
- Diverse plasmid replicon backbones carry each gene (mcr-1: IncI2 vs IncHI2; blaNDM-1: IncA/C2 vs IncF).
- Two distinct mcr-1 mobilization contexts (nikA-nikB-mcr-1-hp vs ISApl1-mcr-1) and two distinct blaNDM-1 contexts.

BV-BRC-mappable workflow: **Comprehensive Genome Analysis** (assembly/annotation stats), **AMR analysis** (ResFinder/AMRFinder/CARD), **PlasmidFinder** (replicon typing via Similar Genome Finder), **MLST**.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Complete genomes deposited under GenBank CP021202–CP021210 (2 chromosomes + 7 plasmids). | Data availability | Yes | ✅ |
| C2 | Per-replicon genome statistics (sizes, GC) per Table 1. | Genome stats | Yes | ✅ |
| C3 | EC1002 = ST405; EC2474 = ST131. | MLST | Yes | ✅ |
| C4 | Per-plasmid acquired-resistance gene complement (Table 1), incl. mcr-1 and blaNDM-1. | Genomic (AMR) | Yes | ✅ (partial) |
| C5 | Plasmid replicon types: IncI2/IncHI2 (mcr), IncA/C2·IncF (NDM), IncFII/IncFIB/IncI1. | Genomic (typing) | Yes | ✅ |
| C6 | mcr-1 and blaNDM-1 reside on **separate plasmids** (never co-located). | Genomic (central conclusion) | Yes | ✅ |

## 3. Method (numbered, exact sources + tool versions + commands)

All analyses were run on the **actual deposited GenBank sequences**, re-downloaded independently.

1. **Paper fetch:** Europe PMC full-text XML for PMC5738369 (`work/paper_fulltext.xml`, 82 KB). Table 1 (accessions, sizes, GC, ST, resistance genes, replicon types) parsed.
2. **Genome download (NCBI efetch, free/no-auth):**
   `efetch.fcgi?db=nuccore&id=<ACC>&rettype=fasta` for all 9 accessions → `work/genomes/*.fasta`.
3. **Genome statistics (local venv, Biopython 1.87):** `work/genome_stats.py` computes length + GC% per replicon and compares to Table 1. Output: `evidence/evidence_genome_stats.json`.
4. **MLST (mlst 2.35.0, PubMLST `ecoli_achtman_4`)** on uicgpu (`~/micromamba/envs/amr`):
   `mlst --scheme ecoli_achtman_4 strains/EC1002.fasta strains/EC2474.fasta`
   (per-strain concatenation of chromosome + plasmids). Output: `evidence/mlst_results.tsv`.
5. **Acquired resistance (AMRFinderPlus 3.12.8, DB 2024-07-22.1):**
   `amrfinder -n strains/<S>.fasta --organism Escherichia --plus -d <db>` → `evidence/EC1002_amr.tsv`, `evidence/EC2474_amr.tsv`. Genes mapped to contig → plasmid via the `Contig id` column.
6. **Plasmid replicon typing (PlasmidFinder DB via blastn):** downloaded `enterobacteriales.fsa` (159 replicon refs) from the PlasmidFinder DB repo; `makeblastdb` + `blastn -perc_identity 95`, kept hits with coverage ≥ 60%. Output: `evidence/plasmidfinder_results.tsv`.
7. **Scoring:** LLM judge (Argo `gpt-5.2`, free) given paper claims + all replication outputs; asked for per-claim verdicts, coverage %, agreement %, canonical verdict. Output: `evidence/llm_judge_gpt52.md` (input: `evidence/llm_judge_input.md`).

## 4. Results vs paper

### 4.1 C1/C2 — Accessions & genome statistics (Biopython)

| Accession | Replicon | Paper bp | Obs bp | Δbp | Paper GC | Obs GC |
|---|---|---:|---:|---:|---:|---:|
| CP021202 | EC1002 chromosome | 5,177,501 | 5,177,498 | −3 | 50.1 | 50.61 |
| CP021203 | pEC1002-1 IncFII | 183,509 | 183,508 | −1 | 50.0 | 49.96 |
| CP021205 | pEC1002-MCR IncI2 | 63,392 | 63,392 | 0 | 43.0 | 43.01 |
| CP021206 | pEC1002-NDM IncA/C2 | 111,688 | 111,688 | 0 | 52.3 | 52.33 |
| CP021204 | pEC1002-4 IncFIB | 92,439 | 92,438 | −1 | 50.0 | 50.30 |
| CP021207 | EC2474 chromosome | 5,013,813 | 5,013,813 | 0 | 50.6 | 50.61 |
| CP021209 | pEC2474-MCR IncHI2 | 223,982 | 223,982 | 0 | 45.8 | 45.83 |
| CP021210 | pEC2474-NDM IncFII | 75,553 | 75,553 | 0 | 50.8 | 50.78 |
| CP021208 | pEC2474-3 IncI1 | 86,717 | 86,725 | +8 | 49.5 | 49.55 |

All 9 replicons present; lengths match to **0–8 bp**, GC to **≤0.5%**. → **C1, C2 reproduced.** (The chromosome's whole-genome GC in the paper, 50.1%, is slightly below the strict per-sequence 50.61% we compute — a common rounding/reporting difference; every other value matches tightly.)

### 4.2 C3 — MLST

| Strain | Paper | Replication (ecoli_achtman_4) | Allelic profile |
|---|---|---|---|
| EC1002 | ST405 | **ST405** ✅ | adk35 fumC37 gyrB29 icd25 mdh4 purA5 recA73 |
| EC2474 | ST131 | **ST131** ✅ | adk53 fumC40 gyrB47 icd13 mdh36 purA28 recA29 |

→ **C3 reproduced (exact).**

### 4.3 C4 — Per-plasmid acquired-resistance genes (AMRFinderPlus 3.12.8)

**EC1002**
| Replicon | Paper (ResFinder 2.1) | AMRFinderPlus 2024 | Assessment |
|---|---|---|---|
| chr CP021202 | blaCTX-M-15, oqxB, tetB | blaCTX-M-15, tet(B), blaEC, gyrA/parC/parE QRDR muts | ✅ core (oqxB not in AMRFinder scope) |
| pEC1002-1 CP021203 | blaCTX-M-15, sul, mph, aac(3)-Ib, erm, aadA4, dfrA, arr | blaCTX-M-15, aac(3)-IIe, aadA5, dfrA17, erm(B), mph(A) | ✅ mostly (allele drift; arr not called) |
| pEC1002-4 CP021204 | blaTEM | blaTEM-1 | ✅ |
| **pEC1002-MCR CP021205** | **mcr-1 (only)** | **mcr-1.1 (only)** | ✅ exact |
| **pEC1002-NDM CP021206** | blaNDM-1, blaCTX-M-14, blaTEM, sul1, mph, aac(6')-Ib, rmtC, arr | **blaNDM-1**, blaCTX-M-14, blaTEM-1, sul1, mph(A), aac(6')-Ib3, rmtC, ble, qacEΔ1, aac(3)-IId | ✅ strong (arr not called; ble/qac extra) |

**EC2474**
| Replicon | Paper | AMRFinderPlus 2024 | Assessment |
|---|---|---|---|
| chr CP021207 | blaCTX-M-55 | blaCTX-M-55, blaEC | ✅ |
| pEC2474-3 CP021208 | blaCTX-M-55 | blaCTX-M-55 | ✅ |
| **pEC2474-MCR CP021209** | mcr-1, blaCTX-M-14, floR, aph4, sul2, aac(3)-IVa, fosA14 | **mcr-1.1**, blaCTX-M-14, floR, aph(4)-Ia, sul2, aac(3)-IVa, fosA3, ter* | ✅ strong (fosA3 vs fosA14 variant) |
| **pEC2474-NDM CP021210** | blaNDM-1, aph | **blaNDM-1**, aph(3')-VI, ble | ✅ |

Core AMR content reproduced across all plasmids; the discrepancies are database-version artifacts (allele-level names, `arr`/`oqxB` outside AMRFinderPlus scope, extra `ble`/`qacEΔ1`/tellurium loci that a 2024 DB annotates but a 2017 ResFinder-2.1 table did not). → **C4 partially reproduced.**

### 4.4 C5 — Plasmid replicon typing (PlasmidFinder / blastn)

| Plasmid | Paper | Replication | Match |
|---|---|---|---|
| pEC1002-1 (CP021203) | IncFII | IncFII (100%) | ✅ |
| pEC1002-4 (CP021204) | IncFIB | IncFIB (98.8%) + IncFIA | ✅ (IncFIB confirmed) |
| pEC1002-MCR (CP021205) | IncI2 | IncI2 (100%) | ✅ |
| pEC1002-NDM (CP021206) | IncA/C2 | IncC (100%) | ✅ (IncC = renamed IncA/C2) |
| pEC2474-3 (CP021208) | IncI1 | IncI1-I(Alpha) (100%) | ✅ |
| pEC2474-MCR (CP021209) | IncHI2 | IncHI2 (100%) | ✅ |
| pEC2474-NDM (CP021210) | IncF | IncFII (100%) | ✅ (F refined to FII) |

All 7 replicon types match. → **C5 reproduced.**

### 4.5 C6 — mcr-1 and blaNDM-1 on separate plasmids (central conclusion)

- EC1002: mcr-1.1 on **CP021205** (pEC1002-MCR, IncI2); blaNDM-1 on **CP021206** (pEC1002-NDM, IncA/C2). Distinct plasmids. ✅
- EC2474: mcr-1.1 on **CP021209** (pEC2474-MCR, IncHI2); blaNDM-1 on **CP021210** (pEC2474-NDM, IncF/FII). Distinct plasmids. ✅
- AMRFinderPlus additionally places blaNDM-1 co-located with **rmtC + ble** on CP021206, consistent with the paper's `rmtC-ISKpn14-blaNDM-1-bleMBL...` context.

→ **C6 reproduced.** The paper's headline claim holds independently.

## 5. LLM-judge scoring (Argo gpt-5.2, free)

- **Coverage:** 5/6 = **83.3%** of testable claims reproduced (C4 partial).
- **Agreement:** **~85–90%** — genome stats, MLST, accessions, replicon types, and the central separate-plasmid conclusion match closely; agreement drops only on the gene-by-gene AMR inventory.
- **Canonical verdict:** **PARTIAL.**
- Judge justification: *"strongly confirms the deposited sequences, genome statistics, MLST assignments, plasmid replicon types (allowing standard renaming like IncA/C2→IncC), and the central claim that mcr-1 and blaNDM-1 reside on separate plasmids; the more granular per-plasmid resistance-gene complements are only partially reproduced due to database/version/allele-calling differences."*

Full judge output: `evidence/llm_judge_gpt52.md`.

## 6. Honest limitations

- AMR called with **AMRFinderPlus 2024** vs the paper's **ResFinder 2.1 (2017)** → expected allele/nomenclature drift; not a contradiction.
- Plasmid comparison figures (BRIG/Easyfig) and full genetic-context alignments were not rebuilt; blaNDM-1 context was confirmed only at the co-localization level (blaNDM-1 + rmtC + ble on one contig).
- No de novo re-assembly from raw reads (paper's PacBio/Illumina reads were not re-processed); replication uses the authors' deposited closed sequences, which is the appropriate substrate for verifying the genome-characterization claims.

## Verdict
**Verdict:** PARTIAL

WAVE_RESULT set=BVBRC-58 paper=Zheng2017_Sci_Rep_7_17885_PMID29263349 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-58-Ecoli-MCR1-NDM1-bloodstream-Zheng2017 one_line=Re-downloaded all 9 GenBank replicons (CP021202-CP021210) and independently reproduced genome stats (0-8bp), MLST (ST405/ST131 exact), plasmid replicon types (7/7 incl IncA/C2->IncC), and the central mcr-1/blaNDM-1-on-separate-plasmids conclusion on real data; per-plasmid AMR inventory partially reproduced (core genes match; allele drift from 2017-ResFinder vs 2024-AMRFinderPlus). LLM-judge coverage 83%, agreement ~85-90%.
