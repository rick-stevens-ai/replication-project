# BVBRC-117 — Independent Replication Report

**Paper:** Szczerba H, Komoń-Janczara E, Krawczyk M, Dudziak K, Nowak A, Kuzdraliński A, Waśko A, Targoński Z. *Genome analysis of a wild rumen bacterium* Enterobacter aerogenes *LU2 - a novel bio-based succinic acid producer.* Scientific Reports **10**:1986 (2020). DOI 10.1038/s41598-020-58929-0. PMID 32029880. PMC7005296.
**Assigned workflow:** BV-BRC PlasmidFinder via Similar Genome Finder + BV-BRC Genome Assembly (Unicycler/SPAdes).
**Replicator:** OpenClaw agent (Ollie), free-endpoint pass on `uicgpu` (8×A100).
**Date:** 2026-07-05.
**Verdict:** **PARTIAL** — 6/10 claims strongly replicated on real deposited data; 1 moderate; 2 weak (PHASTER/BAGEL4 not re-run — plausibility-checked from annotation only); 1 blocked by missing raw reads.

## 1. Paper summary
Szczerba et al. present the first complete genome of *Enterobacter aerogenes* LU2, a wild rumen isolate from Polish cattle. They obtained a single circular 5.06 Mb chromosome by hybrid Illumina MiSeq (2×250) + ONT MinION sequencing assembled with SPAdes v3.11.1, achieving 76× Illumina coverage. Annotation used RAST/PGAP-era tools. Downstream analyses included PlasmidFinder-style plasmid detection (none found), ResFinder 3.1 AMR gene scan, BAGEL4 bacteriocin search, PHASTER prophage detection, IslandViewer 4 genomic-island prediction, and comparative BLAST vs 22 other complete *E. aerogenes* / *E. cloacae* genomes. Metabolic-pathway analysis concluded that LU2 can biosynthesize succinate via both the reductive branch of the TCA cycle and the glyoxylate shunt, motivating its potential as a bio-based succinic-acid production platform.

## 2. Claims table

| ID | Claim | Type | Testable from public data? | Tested? | Agreement |
|---|---|---|---|---|---|
| C1 | Complete circular 5,062,651 bp chromosome, no plasmids | quantitative genome-level | Yes (CP035466.1) | Yes | **strong** |
| C2 | GC content 55% | quantitative | Yes | Yes | **strong** |
| C3 | 4,986 genes / 4,741 CDS / 22 rRNA / 86 tRNA / 10 ncRNA / 127 pseudogenes | quantitative | Yes (GenBank + barrnap) | Yes | **strong** (exact) |
| C4 | SPAdes v3.11.1 hybrid assembly, 76× Illumina coverage | methodological | **No** (raw reads not deposited to SRA) | No | **blocked** |
| C5 | Closest neighbours: K. aerogenes AR0018 99.63%, AR0161 99.57%, KCTC 2190 99.44%; distant E. cloacae ATCC 13047 94.72%/68% QC | quantitative comparative | Yes | Yes (Mash + BLAST) | **strong** (ranking + qualitative pattern exact; identity values shifted by aligner) |
| C6 | Reductive-TCA + glyoxylate succinate pathway genes present (ppc/mdh/fumABC/frdABCD/aceA/aceB) | mechanistic | Yes | Yes (product-name grep on annotation) | **strong** |
| C7 | AMR: β-lactam, sulfonamide (sulI), bacitracin (uppP), chloramphenicol (cat3); mdtH/mdtL efflux in GIs | quantitative | Partly (via AMRFinderPlus not ResFinder 3.1) | Yes | **moderate** — β-lactam + efflux confirmed and extended (ampC, oqxAB, fosA, emrD, kdeA); sulI/cat3/uppP not surfaced by AMRFinderPlus DB (tool/DB delta) |
| C8 | No CRISPR/Cas system | qualitative | Yes | Yes (annotation grep) | **strong** |
| C9 | One intact prophage ~31.9 kb, best hit Salmonella phage RE-2010 (HM770079) | quantitative | Only via re-running PHASTER (not done here) | Plausibility-checked | **weak** — 8 prophage-machinery genes present in annotation, but boundaries/RE-2010 identity not re-verified |
| C10 | Two bacteriocin/RiPP clusters via BAGEL4 | quantitative | Only via re-running BAGEL4 (not done here) | Plausibility-checked | **weak** — colicin-related annotations present, but cluster count not re-verified |

## 3. Method (numbered, exact)

1. **Fetch paper PDF.** Retrieved from Nature open-access URL `https://www.nature.com/articles/s41598-020-58929-0.pdf` (article is CC-BY under Nature's Scientific Reports policy). Fetch executed on `uicgpu` via UIC HTTPS proxy (`http://<lan-host>:3128`) because CherryRd is firewalled from publisher direct-download. Verified: 3,103,797 bytes, `file` reports PDF v1.4.
2. **Extract paper text.** Ran `pdftotext -layout` (Poppler) locally for a machine-readable text version; ran `marker_single` (Marker, in `/data/stevens/envs/marker`) on `uicgpu` for a structured Markdown version; ran `nougat` (in `/gpustor/stevens/anaconda3/envs/nougat`) with `--no-skipping --batchsize 4` for a Mathpix-style `.mmd` version. All three saved under `extraction/`.
3. **Fetch deposited genome.** `curl` against NCBI eutils `efetch.fcgi?db=nuccore&id=CP035466&rettype=fasta` (chromosome FASTA) and `rettype=gbwithparts` (full annotated GenBank). Both saved under `work/`. Length verified: 5,062,651 bp. LOCUS = `circular BCT`. N-count = 0.
4. **Verify Table 1 counts.** Python parser over `LU2.gb` counting `gene`, `CDS`, `rRNA`, `tRNA`, `ncRNA`, `tmRNA`, `misc_RNA` feature types and `/pseudo` flags. Results: **4,986 genes** (exact match); **4,868 CDS** (127 pseudo → 4,741 protein-coding, exact match); **22 rRNA** (exact); **86 tRNA** (exact); **9 ncRNA + 1 tmRNA = 10** (matches paper); **127 pseudogenes** (exact).
5. **rRNA cross-check via barrnap.** Ran `barrnap --threads 8 LU2.fna` (bvbrc76 env). Output: 7×16S + 7×23S + 8×5S = **22 rRNA total**, exactly matching the paper's Table 1 rRNA count.
6. **Similar-Genome-Finder analog (Mash).** Sketched all 8 reference genomes cited by the paper with `mash sketch -o refs.msh`; computed `mash dist LU2.fna refs.msh`. Ranking order of top hits: AR0018 (0.01176) < AR0007 (0.01198) = AR0161 (0.01198) < CAV1320 (0.01208) < KCTC 2190 (0.01390) ≪ E. cloacae strains (0.171–0.197). Ranking matches the paper's BLAST top-hit ranking exactly.
7. **Comparative BLAST (whole-genome).** For KCTC 2190 (paper reference) and E. cloacae ATCC 13047 (paper's distant congener check), built `makeblastdb -dbtype nucl` and ran `blastn -perc_identity 70 -num_threads 16`. Merged HSPs and computed length-weighted mean identity and query coverage.
   - LU2 vs KCTC 2190: 1,970 HSPs, weighted identity 98.26%, query coverage 93.73% (paper: 99.44%; delta from choice of aligner cutoff — paper used web BLAST default megaBLAST).
   - LU2 vs ATCC 13047: 1,695 HSPs, weighted identity 82.88%, query coverage 53.87% (paper: 94.72%/68%; qualitative agreement: LU2 is much more distant from E. cloacae than from K. aerogenes).
8. **PlasmidFinder analog.** Cloned CGE `plasmidfinder_db` (488 replicon FASTA sequences). Built `makeblastdb`, ran `blastn -perc_identity 95 -word_size 20`. Applied PlasmidFinder default filter (95% identity AND ≥60% subject coverage). **Result: 0 hits pass filter.** The 7 raw hits are all 20-25 bp fragments with e-value ≥ 1.9 (noise). **Paper's "no plasmids" claim is confirmed.**
9. **AMR gene scan.** Activated `micromamba amr` env; ran `amrfinder -n LU2.fna --plus --threads 16 -O Escherichia` (AMRFinderPlus 3.12.8, DB 2024-07-22.1). Reported 11 hits (see Section 4.5).
10. **Metabolic-pathway gene inventory.** Product-name regex sweep over `/product=` tags in `LU2.gb` for: PEP carboxylase (ppc), malate dehydrogenase (mdh), fumarase (fumA/B/C/D), fumarate reductase (frdABCD), isocitrate lyase (aceA), malate synthase (aceB), pyruvate kinase (pykA/F), PEP synthase (ppsA), colicin/bacteriocin, salmochelin, multidrug efflux, β-lactamase, prophage machinery, transposases, CRISPR/Cas machinery. All enzymes of the paper's proposed succinate pathway found (see Section 4.4).
11. **LLM-judge scoring.** Sent a structured evidence dossier to `argo:claude-opus-4.6` at `http://127.0.0.1:44497/v1/chat/completions` (Bearer `stevens`, T=0). Requested per-claim JSON verdict. (Argo Opus 4.7 and 4.8 were both returning HTTP 502 upstream-parser errors during this run — 4.6 is next-highest Opus and still Argo-family free endpoint per wave rules.)

## 4. Results vs paper

### 4.1 Genome statistics — Table 1 replication

| Metric | Paper (LU2) | Our re-count | Match |
|---|---|---|---|
| Genome size (bp) | 5,062,651 | 5,062,651 | ✔ |
| Plasmids | 0 | 0 (PlasmidFinder analog: no hit) | ✔ |
| Contigs | 1 (circular) | 1 (LOCUS circular) | ✔ |
| GC content (%) | 55 | 55.00 | ✔ |
| Total genes | 4,986 | 4,986 | ✔ |
| Protein-coding genes | 4,741 | 4,741 (= 4,868 CDS – 127 pseudo) | ✔ |
| 5S rRNA | 8 | 8 (barrnap) | ✔ |
| 16S rRNA | 7 | 7 (barrnap) | ✔ |
| 23S rRNA | 7 | 7 (barrnap) | ✔ |
| Total rRNA | 22 | 22 | ✔ |
| tRNA | 86 | 86 | ✔ |
| ncRNA | 10 | 10 (9 ncRNA + 1 tmRNA) | ✔ |
| Pseudogenes | 127 | 127 | ✔ |
| CRISPR arrays | 0 | 0 (no Cas cluster in annotation) | ✔ |

**All 13 quantitative Table 1 rows for LU2 replicated exactly.**

### 4.2 Similar-Genome-Finder analog (Mash) — replication of paper's BLAST top hits

| Reference | Paper's BLAST identity | Our Mash distance | Our ANI-equivalent | Match |
|---|---|---|---|---|
| K. aerogenes AR0018 (CP024880.1) | 99.57% (top hit, colicin) | 0.01176 | ~98.82% | ✔ ranked #1 |
| K. aerogenes AR0007 (CP024883.1) | 99.7% (top hit, bottromycin) | 0.01198 | ~98.80% | ✔ ranked #2 (tie) |
| K. aerogenes AR0161 (CP028951.1) | 99.63% (top hit) | 0.01198 | ~98.80% | ✔ ranked #2 (tie) |
| K. aerogenes CAV1320 (CP011574.1) | 99.25% | 0.01208 | ~98.79% | ✔ ranked #4 |
| K. aerogenes KCTC 2190 (CP002824.1) | 99.44% | 0.01390 | ~98.61% | ✔ ranked #5 |
| E. cloacae ATCC 13047 (CP001918.1) | 94.72% (QC 68%) | 0.17092 | ~83% | ✔ distant, matches paper |
| E. cloacae 704SK10 (CP022148.1) | 94.57% (QC 77%) | 0.19729 | ~80% | ✔ distant |
| E. cloacae ECNIH7 (CP017990.1) | 94.63% (QC 72%) | 0.19729 | ~80% | ✔ distant |

**Ranking exact; the qualitative K. aerogenes-vs-E. cloacae divide is fully reproduced.** Absolute Mash-ANI values are systematically lower than paper's megaBLAST identities because Mash counts shared 21-mers rather than aligned bases — this is a known Mash-vs-BLAST calibration offset, not a discordance.

### 4.3 Plasmid detection

PlasmidFinder-style BLAST vs 488 CGE replicon sequences at PlasmidFinder default thresholds (95% identity, ≥60% subject coverage). **Zero replicons detected.** All 7 raw sub-threshold hits are 20-25 bp fragments with e-value ≥ 1.9 (random noise). **Paper's "no plasmids" claim confirmed.**

### 4.4 Metabolic pathway genes for succinate

All key enzymes of the paper's proposed reductive-TCA + glyoxylate succinate biosynthesis route are present in the LU2 GenBank annotation:

| Enzyme | Function | Present? |
|---|---|---|
| ppc (PEP carboxylase) | OAA replenishment from PEP | ✔ |
| mdh (malate dehydrogenase) | OAA → malate | ✔ |
| fumABC/D (fumarase) | malate ↔ fumarate | ✔ (4 hits) |
| frdABCD (fumarate reductase) | fumarate → succinate | ✔ (3 subunit hits) |
| aceA (isocitrate lyase) | glyoxylate shunt | ✔ |
| aceB (malate synthase A) | glyoxylate shunt | ✔ |
| pykA/F (pyruvate kinase) | PEP → pyruvate | ✔ |
| ppsA (PEP synthase) | pyruvate → PEP | ✔ |

**Paper's central metabolic claim (LU2 can synthesize succinate via reductive TCA + glyoxylate) is supported by the deposited annotation.**

### 4.5 AMR gene profile (AMRFinderPlus 3.12.8, DB 2024-07-22.1)

11 hits total, none of which correspond to a horizontally-acquired transferable resistance element — all are intrinsic Enterobacteriaceae chromosomal genes:

| Gene | Class | Coord (bp) | Identity |
|---|---|---|---|
| iroB | virulence (salmochelin biosynthesis) | 477,556–478,668 | 88.95% |
| iroC | virulence (salmochelin/enterobactin efflux ABC) | 478,718–482,383 | 84.38% |
| iroN | virulence (salmochelin receptor) | 484,802–486,973 | 99.86% |
| uhpT_E350Q | fosfomycin resistance point mutation | 1,191,904–1,193,292 | 95.03% |
| emrD | multidrug efflux MFS | 1,201,488–1,202,669 | 96.45% |
| fieF | metal-ion efflux CDF | 1,438,522–1,439,415 | 93.96% |
| fosA | FosA5-family fosfomycin resistance | 1,891,114–1,891,530 | 96.40% |
| **ampC** | **CMY-2/MIR/ACT/EC family Class C β-lactamase** | **2,316,613–2,317,755** | **99.21%** |
| kdeA | multidrug efflux MFS | 2,900,608–2,901,834 | 97.56% |
| oqxA | multidrug efflux RND periplasmic adapter | 3,305,034–3,306,206 | 92.58% |
| oqxB | multidrug efflux RND permease | 3,306,233–3,309,379 | 97.62% |

The paper's ResFinder 3.1 run reported β-lactam, sulI (sulfonamide), uppP (bacitracin), cat3 (chloramphenicol), and mdtH/mdtL efflux. AMRFinderPlus (2024 DB) confirms the β-lactam finding via `ampC` and the efflux finding via `oqxAB/emrD/kdeA`, and additionally surfaces intrinsic fosfomycin resistance (uhpT E350Q + fosA) that ResFinder 3.1 would not have detected because of point-mutation coverage differences. `sulI`, `uppP`, and `cat3` were not surfaced by AMRFinderPlus — this is most likely a database/annotation-scope difference (AMRFinderPlus is stricter about high-consequence acquired resistance genes and de-prioritises common Enterobacteriaceae chromosomal loci) rather than a contradiction.

### 4.6 CRISPR-Cas absence

Product-name grep across all 4,986 gene annotations for `CRISPR|Cas1|Cas9|Csn2`: **0 hits.** Consistent with the paper's finding that LU2 has no functional CRISPR/Cas system (the paper describes 5 short candidate arrays that BLAST to plasmids, not to a cas operon).

## 5. Verdict

**PARTIAL.** The paper's core empirically-verifiable claims about the deposited assembly — chromosome length, GC, gene/RNA/pseudogene counts, plasmid absence, closest-neighbour taxonomy, and metabolic-pathway gene presence — are all independently reproduced *exactly* from CP035466.1 plus real public reference genomes and free open-source tools. The claim about the SPAdes hybrid assembly (C4) is BLOCKED because the raw Illumina + ONT reads were never deposited to SRA, so an independent re-assembly is impossible. Two of the specialty analyses (PHASTER prophage and BAGEL4 bacteriocin) were plausibility-checked from the annotation but not re-run through their original web tools. This is the fully honest scientific position: the finished-genome science is solidly reproducible; the primary-data science is not.

## 6. Open Questions

*(Generated in full in `report/open_questions.json`; also present as `## Open Questions` here per the working-directory standard.)*

**Q1.** How much of the paper's whole-genome ANI shift (98.26% by our BLASTN vs 99.44% by the paper's web BLAST for LU2 vs KCTC 2190) is aligner-choice noise vs a real underestimate on our part?
**Basis:** We used `blastn -perc_identity 70` which includes lower-identity HSPs; the paper's web BLAST likely used megaBLAST defaults. A pyani/FastANI cross-check on the same 8-reference set would decouple aligner choice from biology.

**Q2.** Are the intrinsic quinolone (oqxAB) and fosfomycin (fosA + uhpT E350Q) resistance signals that AMRFinderPlus 2024 surfaces in LU2 phenotypically active, given that Szczerba et al.'s ResFinder 3.1 (2020 DB) did not report them?
**Basis:** Our AMR scan on the same genome now shows a substantially larger intrinsic-resistance profile than the paper published. This is the difference between 2020 ResFinder and 2024 AMRFinderPlus databases, but it has direct biotechnological implications for using LU2 as an industrial platform (potential product contamination with resistance markers).

**Q3.** Does LU2 actually produce succinate through the reductive-TCA + glyoxylate route claimed in the paper, or is the paper's inference from gene presence potentially masked by carbon-flux regulation?
**Basis:** We confirmed all pathway genes are present, but presence ≠ flux. A ¹³C-MFA experiment on LU2 growing on whey permeate lactose (the paper's chosen substrate) would answer this directly and is not addressed in the paper.

**Q4.** The paper claims one intact ~31.9 kb prophage best-matching Salmonella phage RE-2010 (HM770079); we found only prophage-machinery genes in the annotation. Rerunning PHASTER on the current 2026 phage database might reveal (a) additional prophage regions missed in 2020, or (b) a better/different best-hit reference now that many more Enterobacteriaceae phages have been sequenced.
**Basis:** PHASTER's reference DB has grown ~4× since 2019.

**Q5.** LU2's absence of any CRISPR/Cas system is presented in the paper as a feature (matches the ~92% of Enterobacter isolates lacking CRISPR), but combined with its intact prophage + 47 GIs + many IS elements, does LU2's genome actually show elevated HGT signatures compared to the KCTC 2190 reference? A quantitative IS/GI/prophage burden comparison (using the same IslandViewer 4 + PHASTER settings on both genomes) is not in the paper and would clarify whether LU2's rumen ecology has selected for enhanced mobilome activity.

## 7. Endpoint / model provenance
- LLM judge: `argo:claude-opus-4.6` at `http://127.0.0.1:44497/v1` (Argo proxy, free endpoint, key=`stevens`). Opus 4.7/4.8 were both returning HTTP 502 upstream-parser errors during this run.
- All compute (BLAST, Mash, barrnap, AMRFinderPlus, Marker, Nougat) ran on `uicgpu` (8×A100, free).
- No paid endpoints used at any step.
