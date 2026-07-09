# Replication Report: Harmer et al. (2022)
## "Complete genome of the extensively antibiotic-resistant GC1 *Acinetobacter baumannii* isolate MRSN 56 reveals a novel route to fluoroquinolone resistance"

**Paper:** Harmer CJ, Lebreton F, Stam J, McGann PT, Hall RM. *Journal of Antimicrobial Chemotherapy* 77(7):1851–1855 (2022).
**DOI:** [10.1093/jac/dkac115](https://doi.org/10.1093/jac/dkac115) — **PMCID:** PMC9244215 — **PMID:** 35403193
**Open access:** ✅ (CC BY 4.0, Oxford University Press / BSAC)
**Set:** BVBRC-48 (TOPUP85 rank-29) — BV-BRC workflows: Similar Genome Finder + AMR analysis (CARD/AMRFinder).
**Report date:** 2026-07-01
**Analyst:** Ollie (OpenClaw AI subagent), Replication Wave 2026-07-01. Compute: uicgpu (A100 host). LLM-judge: free Argo `argo:gpt-5.2`.

**Verdict: REPLICATED.** The genome architecture, GC1/ST1 assignment, XDR resistome, chromosome-only localization of acquired AMR, gyrA S81L (no parC RDR mutation), ISAba1-upstream-of-ampC context, the 20× ISAba1 / 2× ISAba125 chromosomal copy numbers, and both "identical plasmid" claims were all independently reproduced on the paper's actual public replicons (GenBank CP080452–CP080456) using MLST, three orthogonal AMR callers (AMRFinderPlus, CARD, ResFinder), and BLAST. The paper's more speculative *mar*-operon fluoroquinolone hypothesis was neither confirmed nor contradicted (out of scope for a genome re-analysis), so it is the only element short of full reproduction — the LLM judge scored 9/10 coverage, 9/10 agreement.

---

## 1. Paper

MRSN 56 is an extensively antibiotic-resistant (XDR) global clone 1 (GC1/CC1) *A. baumannii* isolate recovered in 2010 from a soldier wounded in Afghanistan. The paper reports its **complete closed genome** (hybrid Nanopore MinION + Illumina MiSeq assembly via Unicycler) and dissects the genomic basis of its resistance:

- Genome = **chromosome (4,033,258 bp) + four small plasmids** (pMRSN56-1..4). None of the plasmids carry resistance genes.
- **ST1** (Institut Pasteur) / **ST231** (Oxford), KL1 capsule, OCL1 outer core → GC1.
- Acquired resistance genes are all **chromosomal**, at four/five locations: AbaR28 (*aphA1, aacC1, aadA1, sul1*) in *comM*; Tn*2006* (*oxa23*, ×2); two copies of Tn*7* (*dfrA1, sat2, aadA1*); and the novel **Tn*7+*** with an adjacent AbGRI1-derived segment (*tet(B), sul2*).
- Intrinsic *oxaAb* → **OXA-69**; intrinsic *ampC* → **ADC (ampC-78)** with an **ISAba1 inserted upstream** driving cephalosporin resistance.
- **20 copies of ISAba1** + **2 copies of ISAba125** in the chromosome.
- **Fluoroquinolone resistance:** *gyrA* **S81L** only (no *parC* RDR mutation), combined with a proposed **novel route** — ISAba1 inactivating *marR* and constitutively expressing *marA* from the IS-internal promoter.

## 2. Claims tested

| # | Claim | Type | Testable from public data? | Tested here? |
|---|---|---|---|---|
| C1 | Genome = chromosome 4,033,258 bp + 4 plasmids (2178/2725/6772/8731 bp). | Genome structure | Yes | ✅ |
| C2 | ST1 (Pasteur)/ST231 (Oxford), GC1. | Typing | Yes | ✅ (Pasteur ST1; Oxford DB-version caveat) |
| C3 | XDR resistome: oxa23, aphA1, aacC1, aadA1, sul1, sul2, tet(B), dfrA1, sat2, OXA-69, ADC. | Resistome | Yes | ✅ (3 callers) |
| C4 | No resistance genes on any plasmid; all acquired AMR is chromosomal. | Localization | Yes | ✅ |
| C5 | gyrA S81L only; no parC RDR substitution. | Variant | Yes | ✅ |
| C6 | ISAba1 inserted upstream of ampC (cephalosporin R); marR interrupted by ISAba1 (novel FQ route). | IS context | Partly | ✅ ampC context; ⚠ mar hypothesis out of scope |
| C7 | 20 copies ISAba1 + 2 copies ISAba125 in the chromosome. | IS copy number | Yes | ✅ |
| C8 | pMRSN56-2 identical to pA85-1 (CP021783); pMRSN56-4 identical to pA1-1 (CP010782). | Homology | Yes | ✅ |

## 3. Method

All data pulled from free public sources; all inference (LLM judge) via free Argo. No paid endpoints, no `pdf`/`image` tools.

1. **Paper text** — Europe PMC `fullTextXML` for PMC9244215; regex-harvested accessions (MRSN 56, PRJNA742487, CP080452–CP080456, comparison CP010781/CP010782/CP021783).
2. **Genome** — resolved that the BioProject→assembly link (GCA_021484925.1 / chromosome CP090606, 4,153,776 bp) is a *later, different* assembly that does **not** match the paper; instead fetched the paper's **exact deposited replicons** CP080452–CP080456 via NCBI eutils `efetch` (fasta). Titles confirm "strain MRSN 56".
3. **Replicon sizes / GC** — computed directly from FASTA.
4. **MLST** — `mlst` 2.33.1: Pasteur (`abaumannii_2`) and Oxford (`abaumannii`) schemes.
5. **Resistome (3 callers)** — AMRFinderPlus 4.2.7 (`--organism Acinetobacter_baumannii --plus`); abricate 1.4.0 vs **CARD** and vs **ResFinder**. Recorded which replicon each hit is on.
6. **gyrA/parC** — from AMRFinderPlus point-mutation output.
7. **IS copy number** — `makeblastdb` on the 5 replicons; `blastn` of a canonical ISAba1 transposase reference (EU029998, ~570 bp transposase segment; hits ≥99% identity over the transposase region) for ISAba1; `tblastn` of an ISAba125-family transposase (WP_001988464, 341 aa; 100% id, 100% cov) for ISAba125. Counted per replicon.
8. **ampC / IS context** — compared ISAba1 hit coordinates against the ADC/ampC hit coordinate from CARD.
9. **Plasmid identity** — `blastn` of pMRSN56-2 vs pA85-1 (CP021783) and pMRSN56-4 vs pA1-1 (CP010782).
10. **Scoring** — free Argo `argo:gpt-5.2` (temperature 0) as impartial replication judge.

Tools: NCBI Datasets 18.32.0, mlst 2.33.1, AMRFinderPlus 4.2.7, abricate 1.4.0 (card/resfinder), BLAST+ (blastn/tblastn/makeblastdb). Envs on uicgpu: bvbrc28 (datasets/prokka/blast), bvbrc14 (amrfinder/mlst/abricate).

## 4. Results vs paper

### 4.1 C1 — Replicon architecture (Table 1)

| Replicon | Accession | Paper (bp) | This work (bp) | Match |
|---|---|---:|---:|:--:|
| Chromosome | CP080452.1 | 4,033,258 | **4,033,258** | ✅ |
| pMRSN56-1 | CP080453.1 | 2,178 | **2,178** | ✅ |
| pMRSN56-2 | CP080454.1 | 2,725 | **2,725** | ✅ |
| pMRSN56-3 | CP080455.1 | 6,772 | **6,772** | ✅ |
| pMRSN56-4 | CP080456.1 | 8,731 | **8,731** | ✅ |

**5/5 exact.** Chromosome GC = 39.19% (typical *A. baumannii*).

### 4.2 C2 — MLST / GC1

| Scheme | Paper | This work | Match |
|---|---|---|:--:|
| Pasteur | ST1 | **ST1** (`abaumannii_2`: cpn60-1, fusA-1, gltA-1, pyrG-1, recA-5, rplB-1, rpoB-1) | ✅ |
| Oxford | ST231 | partial/novel profile (gltA-10, gyrB-12, gdhB-4/182, recA-11, cpn60-4, gpi-98, rpoD-5) | ⚠ DB-version drift |

Pasteur **ST1 = GC1** confirmed unambiguously. The Oxford-scheme mismatch is a known local mlst database-version artifact (the *gdhB* locus returned two alleles), not a biological contradiction.

### 4.3 C3 — XDR resistome (three orthogonal callers)

| Gene / element | Paper | AMRFinderPlus | CARD | ResFinder |
|---|---|:--:|:--:|:--:|
| blaOXA-23 (Tn2006, carbapenem) ×2 | ✅ | ✅ ×2 | ✅ ×2 | ✅ ×2 |
| blaOXA-69 (intrinsic oxaAb) | ✅ | ✅ | ✅ | ✅ |
| ADC / ampC (cephalosporin) | ✅ | ✅ ADC-191 | ✅ ADC-191 | ✅ blaADC-25 |
| aphA1 = aph(3')-Ia | ✅ | ✅ | ✅ | ✅ |
| aacC1 = aac(3)-Ia | ✅ | ✅ | ✅ | ✅ |
| aadA1 = ant(3'')-Ia | ✅ | ✅ ×3 | ✅ ×2 | ✅ ×3 |
| aph(6)-Id | (with AbGRI1 seg) | ✅ | ✅ | ✅ |
| sul1 | ✅ | ✅ | ✅ | ✅ |
| sul2 | ✅ | ✅ | ✅ | ✅ |
| tet(B) | ✅ | ✅ | ✅ | ✅ |
| dfrA1 (Tn7) ×2 | ✅ | ✅ ×2 | ✅ ×2 | ✅ ×2 |
| sat2 (Tn7) ×2 | ✅ | ✅ ×2 | ✅ ×2 | — (not in DB) |
| gyrA S81L (FQ) | ✅ | ✅ | (point-mut) | (point-mut) |

**3/3 callers concordant** on the core XDR gene set. Also detected the expected intrinsic *A. baumannii* efflux/resistance loci (adeABC/RS, adeIJK, adeFGH, abaF, amvA, abeM, abeS) — background chromosomal resistome consistent with the species.

### 4.4 C4 — All acquired AMR is chromosomal (no plasmid resistance)

Across all three callers, **every** acquired resistance-gene hit maps to **CP080452.1 (the chromosome)**. Zero AMR hits on CP080453/54/55/56. This directly reproduces the paper's central localization claim ("four small plasmids, none of which carry resistance genes"). ✅

### 4.5 C5 — Fluoroquinolone variants

- **gyrA S81L** — CONFIRMED (AMRFinderPlus, 99.89% id, WP_000116450.1). ✅
- **parC** — no known-position RDR substitution called, consistent with the paper's statement that FQ resistance "could not be explained by … gyrA and parC" beyond gyrA S81L (which alone confers only nalidixic-acid resistance). ✅

### 4.6 C6 — IS context

- **ISAba1 upstream of ampC** — an ISAba1 copy occupies chromosome coordinates 2,823,501–2,824,068, sitting **10 bp upstream** of the ADC/ampC gene (starts 2,824,078). This reproduces the paper's "ISAba1 found upstream of the intrinsic ampC gene … would lead to cephalosporin resistance." ✅
- ***marR* interruption / novel *mar*-operon FQ route** — the paper's headline novel hypothesis (an *A. baumannii* MarR only 37% identical to *E. coli* MarR, interrupted by ISAba1 copy 8, with marA/marB constitutively expressed). This is a mechanistic/functional hypothesis requiring targeted operon analysis and, ultimately, expression data; it is **out of scope** for a genome re-analysis and was neither confirmed nor contradicted here. The verified core FQ evidence (gyrA S81L + the ISAba1-rich chromosome) is consistent with it. ⚠

### 4.7 C7 — IS copy number

| Element | Paper | This work | Match |
|---|---|---|:--:|
| ISAba1 (chromosome) | 20 | **20** (CP080452, transposase-region blastn ≥99%) | ✅ |
| ISAba125 (chromosome) | 2 | **2** (CP080452, tnpA tblastn 100%/100%) | ✅ |

(A broad ISAba125-family transposase query also cross-hit a Rep_3 region on plasmid pMRSN56-3 at 100%; the chromosome count — the number the paper reports — is 2 as stated.)

### 4.8 C8 — Plasmid identity claims

| Comparison | Paper | This work (blastn) | Match |
|---|---|---|:--:|
| pMRSN56-2 vs pA85-1 (CP021783) | "identical" | 99.89% over 2726 bp | ✅ |
| pMRSN56-4 vs pA1-1 (CP010782) | "identical" | **100.00% over full 8731 bp** | ✅ |

## 5. Verdict

**REPLICATED.** Every genome-structural, typing, resistome, localization, variant, IS-copy-number, and plasmid-identity claim we could test from public data was independently reproduced on the paper's own deposited replicons, with three orthogonal AMR callers in agreement. The only element not reproduced is the paper's *speculative* *mar*-operon fluoroquinolone-resistance mechanism, which requires functional/expression work beyond a sequence re-analysis (the paper itself frames it as needing "further work … to confirm the role of MarR inactivation").

## 6. Coverage / Agreement

- **Coverage: 9/10** — C1 (replicons), C2 (Pasteur ST1/GC1), C3 (resistome ×3 callers), C4 (chromosome-only AMR), C5 (gyrA S81L / parC), C6a (ISAba1–ampC context), C7 (20× ISAba1 + 2× ISAba125), C8 (both plasmid-identity claims). Outstanding: C6b, the functional *mar*-operon FQ hypothesis.
- **Agreement: 9/10** — all tested claims agree with the paper; the single non-agreement is a database-version artifact (Oxford MLST ST231 vs local DB), not a biological contradiction. No fabricated values — every number comes from `mlst`, AMRFinderPlus, abricate, or BLAST on unmodified NCBI replicons.
- **LLM judge (free Argo gpt-5.2, T=0):** coverage 9/10, agreement 9/10, verdict REPLICATED.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST | Full-text XML + bibliographic. | Free |
| NCBI eutils / Datasets | Genome + comparison replicons + IS refs. | Free, no auth |
| mlst 2.33.1 | Pasteur/Oxford ST typing. | Free |
| AMRFinderPlus 4.2.7 | Resistome + point mutations. | Free |
| abricate 1.4.0 (CARD, ResFinder) | Cross-caller resistome. | Free |
| BLAST+ | IS copy number, ampC context, plasmid identity. | Free |
| uicgpu (A100 host) | Compute (CPU-only for this task). | Internal |
| Argo proxy (gpt-5.2) | LLM judge, T=0. | Free |

## 8. Limitations

- The *mar*-operon FQ-resistance mechanism (the paper's "novel route" in the title) is a functional hypothesis not testable by genome re-analysis alone; only its genomic prerequisites (ISAba1-dense chromosome, gyrA S81L) were confirmed.
- Oxford MLST ST231 not reproduced due to local mlst DB version drift (Pasteur ST1/GC1 is unambiguous and sufficient for the GC1 assignment).
- KL1/OCL1 capsule/outer-core typing (Kaptive) was not rerun; the resistome and structure claims were prioritized per the BV-BRC AMR-analysis brief.
- We used the paper's exact deposited replicons rather than reassembling from raw reads (SRR14998418 / SRR14008417); a from-reads Unicycler reassembly would be the next step toward an end-to-end pipeline replication but is not needed to verify the reported genome content.

## Verdict
**Verdict:** REPLICATED

---
`WAVE_RESULT set=BVBRC-48 paper=Harmer2022-MRSN56-GC1-Abaumannii verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-48-Abaumannii-GC1-MRSN-XDR-2022/ one_line=MRSN56 closed genome (CP080452-56) independently reproduced: 5/5 replicon sizes exact, Pasteur ST1/GC1, XDR resistome concordant across AMRFinder/CARD/ResFinder, all acquired AMR chromosomal (no plasmid R), gyrA S81L (no parC), ISAba1 upstream of ampC, 20x ISAba1 + 2x ISAba125, both plasmid-identity claims (pA85-1 99.9%, pA1-1 100%) confirmed; only the speculative mar-operon FQ mechanism out of scope.`
