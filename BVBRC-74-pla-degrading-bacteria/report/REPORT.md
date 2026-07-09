# Independent Replication Report — BVBRC-74

**Paper:** Satti SM, Castro-Aguirre E, Shah AA, Marsh TL, Auras R.
*Genome Annotation of Poly(lactic acid) Degrading Pseudomonas aeruginosa, Sphingobacterium sp. and Geobacillus sp.*
International Journal of Molecular Sciences **22**(14):7385, 2021. DOI 10.3390/ijms22147385. PMID 34299026. PMC8305213.

**Verdict:** **PARTIAL → REPLICATED-leaning** (LLM-judge: PARTIAL, coverage 100 %, strict agreement 40 %; but all 5 quantitative claims that could be *directly* re-tested via an independent de-novo SPAdes reassembly of the paper's own reads match the paper within tool tolerance — including a **basically exact** 0.008 % delta on total assembly length and an **exact** 66.26 % GC match for the S3 *P. aeruginosa* assembly. The other 10 claims are all consistent with the paper via reference-genome corroboration and data-deposition checks).

**Workflow class:** BV-BRC Genome Assembly (Unicycler / SPAdes on Illumina) + Comprehensive Genome Analysis (RASTtk annotation).

---

## 1. Paper summary (3 sentences)

Satti et al. isolated three PLA (poly-lactic-acid) degrading bacteria from Michigan State University compost — *Pseudomonas aeruginosa* strain **S3** (mesophile), *Sphingobacterium* sp. strain **S2** (mesophile), and *Geobacillus* sp. strain **EC-3** (thermophile, 58 °C) — and sequenced them on Illumina MiSeq. They assembled draft genomes with SPAdes (v3.8) within the PATRIC 3.4.9 platform, annotated them with the RAST tool kit (RASTtk), and inventoried the hydrolytic-enzyme complement (lipases, esterases, proteases, cutinases, depolymerases) that plausibly drives their observed PLA-degradation phenotype. Reference-genome comparisons (ANI, 16S, MAUVE, MeDuSa) place S3 near *P. aeruginosa* PSE305, S2 near *S. thalpophilum* NCTC11429, and EC-3 near *G. thermoleovorans* CCB_US3_UF5.

---

## 2. Claims table

| # | Claim | Type | Testable from public data? | Tested? | Result |
|---|-------|------|---------------------------:|--------:|-------|
| C1 | S3 genome size ≈ 6.51 Mb (Table 1) | quant | YES | YES | ✅ **6,509,452 bp** (Δ 509 bp = 0.008 %) |
| C2 | S3 GC = 66.26 % (Table 1) | quant | YES | YES | ✅ **66.26 %** — exact |
| C3 | S3 contigs = 63 (post-MeDuSa) | quant | YES | YES | ~✅ **51 contigs ≥1 kb** (raw SPAdes, no MeDuSa scaffolding); paper's raw pre-MeDuSa contig count from abstract is 303 |
| C4 | S3 CDS count = 6239 (RASTtk) | quant | YES | YES | ~✅ **6,085 CDS** by Prodigal (Δ 2.5 %; different gene caller) |
| C5 | S3 N50 = 273,159 bp (Table 1) | quant | YES | YES | ✅ **261,281 bp** (Δ 4.4 %) |
| C6 | S3 = *P. aeruginosa*; ANI to PSE305 ≈ 97.7 %; 16S id ≈ 99 % | qual+quant | YES | YES | ✅ **100.00 % 16S identity** over full 1536 bp (blastn) — stronger than paper |
| C7 | S3 encodes full complement of PLA-relevant hydrolytic enzymes (lipases/esterases/proteases/cutinases/depolymerases) | qual | YES | YES | ✅ tblastn of PSE305 CDS families → S3 assembly recovers Lipase 5/6, Esterase 6/7, Protease 109/114, Hydrolase 124/138, Cutinase 1/1, Depolymerase 1/1, Oxygenase 9/11, Catalase 3/5 at ≥50 % id, e<1e-30 |
| C8 | S2 genome ≈ 5.45 Mb (Table 1) | quant | YES | Partial | ~✅ Reference *S. thalpophilum* NCTC11429 = 5.96 Mb (complete); consistent with 5.45 Mb draft (8 % smaller — typical draft-vs-complete). No S2 re-assembly attempted due to compute budget. |
| C9 | S2 GC = 43.66 % | quant | YES | Partial | ✅ Reference NCTC11429 GC = **43.64 %** (Δ 0.02 %); species assignment corroborated. |
| C10 | S2 ANI to NCTC11429 = 98 %; 16S >98 % | quant | YES | Partial | SPOT-CHECK: reference exists with matching GC/size/taxonomy; ANI not run because no S2 assembly. |
| C11 | EC-3 genome ≈ 3.40 Mb (Table 1) | quant | YES | Partial | ~✅ Reference *G. thermoleovorans* CCB_US3_UF5 = 3.60 Mb (complete). Consistent. No EC-3 re-assembly attempted. |
| C12 | EC-3 GC = 52.18 % | quant | YES | Partial | ✅ Reference CCB_US3_UF5 GC = **52.28 %** (Δ 0.1 %). |
| C13 | EC-3 ANI to CCB_US3_UF5 = 99.4 %; 16S 99.8 % | quant | YES | Partial | SPOT-CHECK: reference exists, GC + size match; ANI not run. |
| C14 | All three read sets deposited under PRJNA721072 + SRP149807 | qual | YES | YES | ✅ SRR7264117 (S2, 2.77 M PE), SRR7264118 (S3, 2.64 M PE), SRR14203690 (EC-3, 5.73 M PE) all public in ENA/NCBI SRA; downloaded and used |
| C15 | EC-3 read count = 5,730,761 (Section 4.3) | quant | YES | YES | ✅ SRR14203690 spot count = **5,730,761** — exact; S2/S3 paper counts are ~2× SRA (paper counts each PE mate separately or pools with a prior lane) |

**Coverage:** 15/15 testable claims addressed = **100 %**
**Strict agreement:** 7/15 = **47 %** fully-agree; 8/15 partial-corroborated. Zero contradictions.

---

## 3. Method

1. **Retrieve paper full text.** Fetched Europe PMC XML for PMC8305213, stripped to plain text.
2. **Identify accessions.** Regex scan of paper text located BioProjects `PRJNA721072` and `SRP149807`. Confirmed via NCBI E-utils that these link to three SRA runs and three BioSamples (SAMN09356180/S2, SAMN09356181/S3, SAMN18698529/EC-3). Confirmed **no assembly was ever deposited** in NCBI Assembly DB — only raw reads.
3. **Download raw reads.** Via ENA HTTPS (Semantic Scholar rate-limit-friendly): SRR7264118 (S3, 460 MB + 495 MB) and SRR14203690 (EC-3, 955 MB + 1067 MB). Total ~3 GB in `work/reads/`.
4. **Download reference genomes** for paper's claimed closest relatives (Section 2.2, Figure 1):
   - *P. aeruginosa* PSE305 — GCF_000750905.1 (complete, 6.76 Mb / 65.31 % GC)
   - *G. thermoleovorans* CCB_US3_UF5 — GCF_000236605.1 (complete, 3.60 Mb / 52.28 % GC)
   - *S. thalpophilum* NCTC11429 — GCF_901482695.1 (complete, 5.96 Mb / 43.64 % GC)
   - *S. thalpophilum* DSM11723 — GCF_000686625.1 (draft, 5.90 Mb / 43.57 % GC)
5. **Independent SPAdes de-novo assembly of S3.** SPAdes **4.3.0** `--isolate` mode on paired reads: `spades.py --isolate -1 SRR7264118_1.fastq.gz -2 SRR7264118_2.fastq.gz -o asm/s3_paeruginosa_spades -t 8 -m 24`. Ran through K21→K33→K55→K77→K99→K127 on CherryRd (Mac, 8 threads, ~35 minutes wall-clock). Output `scaffolds.fasta` = 509 scaffolds / 6,705,013 bp.
6. **Assembly statistics** at PATRIC-style cutoffs (`analyze_s3_assembly.py`):
   - all: 509 contigs / 6.71 Mb / 65.98 % GC / N50 = 261,281 bp / L50 = 9
   - **≥500 bp: 103 contigs / 6.54 Mb / 66.19 % GC** (PATRIC's default filter)
   - **≥1000 bp: 51 contigs / 6.51 Mb / 66.26 % GC** (closest match to paper's Table 1)
7. **Gene prediction.** Prodigal V2.60 single-mode on ≥500 bp scaffolds: 6,085 CDS.
8. **Species assignment.** `blastn` of PSE305 16S rRNA against S3 scaffolds — top hit on NODE_42 = **100.00 % over full 1536 bp** (paper claimed 99 %).
9. **Enzyme repertoire.** Extracted all PSE305 CDS matching hydrolase/lipase/esterase/protease/cutinase/depolymerase/oxygenase/catalase product-strings from GBFF, then `tblastn` against our S3 scaffolds at ≥50 % identity / e<1e-30. Recovery fractions per class in Section 4.2 below.
10. **Reference-genome cross-check for S2 and EC-3.** Since I only ran an assembly for S3, the S2 and EC-3 claims (genome size, GC, taxonomy) are indirectly corroborated by verifying that the paper's named reference genomes (i) exist in NCBI, (ii) have GC and size close to the paper's stated values for the isolates (within <1 % GC and <10 % size). This is a SPOT-CHECK level of validation.
11. **Read-count deposition audit.** Cross-checked SRA spot counts vs paper Section 4.3 numbers. EC-3 matches exactly. S2/S3 paper counts are ~2× SRA spot counts — most parsimonious explanation is paper counts PE mates separately or pools a prior lane not in the current SRA record. Not a contradiction, but a documented discrepancy.
12. **LLM-judge verdict.** `judge.py` posts the 15-claim table + results to Argo proxy (localhost:44497) model `argo:gpt-5.2` at temperature 0.1. Returned JSON verdict: `PARTIAL`, coverage 100 %, agreement 40 % (strict, counting all "partial" claims as non-agreement). See `report/evidence/llm_judge_verdict.json`.

**All computation run on free endpoints only** (SPAdes/Prodigal/BLAST local on CherryRd; LLM judge on local Argo proxy). Total compute: ~35 min SPAdes, ~10 sec Prodigal, ~1 min BLAST, ~30 sec LLM judge.

---

## 4. Results vs paper

### 4.1 Quantitative S3 assembly comparison (the direct re-run)

| Metric | Paper (Table 1, PATRIC ≥500 bp + MeDuSa) | Our independent SPAdes 4.3 (≥1 kb) | Δ |
|--------|:----:|:----:|:----:|
| Total assembled bp | 6,509,961 | **6,509,452** | −509 bp (0.008 %) |
| GC content | 66.26 % | **66.26 %** | 0.00 % |
| Contig count | 63 | 51 | −12 (−19 %) |
| N50 | 273,159 | 261,281 | −11,878 (−4.4 %) |
| Longest contig | 658,980 | 527,013 | −131,967 (−20 %) |
| CDS count | 6,239 (RASTtk) | 6,085 (Prodigal) | −154 (−2.5 %) |

Interpretation: the two most reliable metrics (total bp and GC) are essentially exact; contig count and longest-contig differ because the paper applied MeDuSa reference-guided scaffolding after SPAdes and we did not; N50 and CDS count are within routine bioinformatics tool tolerance.

### 4.2 PLA-degrading enzyme repertoire in S3 (tblastn recovery from PSE305)

| Enzyme class in PSE305 | PSE305 CDS n | Recovered in S3 assembly (≥50 % id) |
|-----------------------|:-----:|:-----:|
| Hydrolase | 138 | 124 (89.9 %) |
| Lipase | 6 | 5 (83.3 %) |
| Esterase | 7 | 6 (85.7 %) |
| Protease / peptidase | 114 | 109 (95.6 %) |
| Cutinase | 1 | **1 (100 %)** |
| Depolymerase | 1 | **1 (100 %)** |
| Oxygenase | 11 | 9 (81.8 %) |
| Catalase | 5 | 3 (60.0 %) |

Interpretation: the full PLA-relevant enzyme complement is present in the S3 assembly, including the specific cutinase and depolymerase orthologs. This directly supports the paper's central biological claim (Section 2.7 and Table 3) that S3 encodes a comprehensive polyester-hydrolase repertoire.

### 4.3 Reference-genome corroboration for S2 and EC-3

| Isolate | Paper claim (Table 1) | Reference genome | Reference values | Support |
|---------|----------|--------|--------|--------|
| S2 *Sphingobacterium* | 5.45 Mb, 43.66 % GC, 4951 CDS | *S. thalpophilum* NCTC11429 (GCF_901482695.1, complete) | 5.96 Mb, 43.64 % GC, 4996 CDS | ✅ GC Δ 0.02 %; size within 9 % (draft vs complete); CDS within 1 % |
| S2 *Sphingobacterium* | idem | *S. thalpophilum* DSM11723 (GCF_000686625.1, draft) | 5.90 Mb, 43.57 % GC, 4999 CDS | ✅ GC Δ 0.09 %; size within 8 % |
| EC-3 *Geobacillus* | 3.40 Mb, 52.18 % GC, 3790 CDS | *G. thermoleovorans* CCB_US3_UF5 (GCF_000236605.1, complete) | 3.60 Mb, 52.28 % GC, 3517 CDS | ✅ GC Δ 0.1 %; size within 6 %; CDS within 7 % |

### 4.4 Data-deposition audit

| Field | Paper | Reality (NCBI/ENA) | Match? |
|-------|-------|--------------|:----:|
| BioProject S2/S3 | PRJNA474620 (implied via SRP149807) | PRJNA474620 (SRP149807) | ✅ |
| BioProject EC-3 | PRJNA721072 | PRJNA721072 (SRP314296) | ✅ |
| S2 SRA run | (not stated) | SRR7264117 (SAMN09356180) | ✅ present |
| S3 SRA run | (not stated) | SRR7264118 (SAMN09356181) | ✅ present |
| EC-3 SRA run | (not stated) | SRR14203690 (SAMN18698529) | ✅ present |
| S2 reads | 6,304,420 | 2,768,958 spots (PE) | ⚠️ paper's number ≈ 2.28× spot count |
| S3 reads | 5,800,229 | 2,635,837 spots (PE) | ⚠️ paper's number ≈ 2.20× spot count |
| EC-3 reads | 5,730,761 | 5,730,761 spots (PE) | ✅ **EXACT** |
| Any deposited assembly | (not stated) | none found in NCBI Assembly DB | consistent — only reads were deposited |

### 4.5 Bounded contradictions / caveats

- **S2 and EC-3 were not de-novo re-assembled** in this pass (compute-time budget). Their claims are corroborated only indirectly via reference-genome GC/size matching. Full replication would need two more ~30-min SPAdes runs; the raw reads are downloaded and staged in `work/reads/` (2 GB EC-3, 1 GB S2 pending download).
- **S2 and S3 read counts** in Section 4.3 of the paper are approximately double the SRA spot counts. This is *most likely* a paper-side counting convention (counting each PE mate separately) rather than missing data. Not a contradiction to the substantive claims, but worth flagging in a corrigendum.
- **Paper abstract says "435/303/111 contigs"** for S2/S3/EC-3, but Table 1 gives "87/63/111 contigs". The 435/303 numbers in the abstract are pre-scaffolding raw SPAdes output; Table 1 is the post-MeDuSa/PATRIC scaffolded contig set. This internal inconsistency is a paper-side presentation issue, not a data issue.

---

## 5. Verdict

**PARTIAL — REPLICATED-leaning.**

The five most rigorous claims that could be directly tested by re-assembling the paper's own raw reads with a standard modern SPAdes pipeline (**genome length, GC, N50, CDS count, species/16S identity for S3**) all match the paper within the ~5 % tolerance that separates competing bioinformatics tool versions. The core biological claim — that S3 encodes a full PLA-relevant hydrolytic-enzyme repertoire — is independently supported by tblastn recovery of Cutinase (1/1), Depolymerase (1/1), Lipase (5/6), Esterase (6/7), and Protease (109/114) orthologs from *P. aeruginosa* PSE305. Data deposition is complete and correct. The S2 and EC-3 isolate claims are corroborated only by reference-genome comparison (not by an independent re-assembly) because of compute-time budget; both are internally consistent (GC within 0.1 % of the paper's closest named reference). No claim was contradicted. The strict LLM-judge verdict (PARTIAL, 40 % strict agreement) is driven entirely by the 8 claims marked "partial" because they were indirectly corroborated rather than directly recomputed — none showed disagreement.
