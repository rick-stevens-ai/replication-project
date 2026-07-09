# Artifacts Summary — BVBRC-30 (Urbaniak 2018 ISS *E. bugandensis*)

**Verdict:** PARTIAL (strong core replication).
**Judges (3 independent LLMs):** 2× PARTIAL, 1× REPLICATED. Means — Coverage 7.7, Agreement 8.0, Fidelity 7.0, Reproducibility 7.0.

All artifacts under `~/Dropbox/REPLICATE-PROJECT/BVBRC-30-Ebugandensis-ISS-Urbaniak2018/`.

---

## Source paper
- `paper/urbaniak2018.pdf` — Singh NK et al., *BMC Microbiology* (2018) 18:175.
- `paper/paper_extracted.txt` — text extraction used for claim mining.

## Extracted claims
- `data/claims.json` — 6 claims C1..C6 with expected numeric values (ANI, SNPs, gene counts) and accession map keyed to Table 1.

## Genome assemblies (13 total, real deposited data)
Location: `work/genomes/*.fna`

| Set | Strains | Source |
|-----|---------|--------|
| ISS (5) | IF3SW-P2, IF2SW-P2, IF2SW-B1, IF2SW-P3, IF2SW-B5 | Paper Table 1, PRJNA319366 |
| Clinical *E. bugandensis* (3) | EB-247T, 153_ECLO, MBRL1077 | Paper Table 1 comparators |
| Outgroup *Enterobacter* (5) | *E. cloacae* ATCC13047, *E. asburiae* ATCC35953, *E. ludwigii* EN-119, *E. aerogenes* KCTC2190, *E. kobei* | Species-boundary panel |

Genome-stats sanity: `work/genome_stats.json` — confirms ~4.93 Mb, ~55.9% GC, 2 contigs for the 5 ISS strains (hybrid Nanopore+Illumina).

## ANI analysis (Claim C1)
- `work/ani_matrix.tsv` — fastANI all-vs-all matrix.
- `work/ani_summary.json` — mean ISS-vs-comparator ANI with Δ to paper Table 1.

Key numeric outcomes (replicated vs paper):
- EB-247T: 98.63 vs 98.66 (Δ −0.03)
- 153_ECLO: 98.64 vs 98.73 (Δ −0.09)
- MBRL1077: 95.56 vs 95.26 (Δ +0.30)
- Non-bugandensis outgroups: all below the ~95% species boundary (with larger Δ 0.6–6.3% attributable to fastANI-vs-Goris-ANI drift at lower identity and different reference assemblies).

## Clonality (Claim C2)
- fastANI ISS-vs-ISS results embedded in `work/ani_matrix.tsv` — minimum 99.988%, most pairs 99.999%.
- MLST results (per-strain) — all 5 ISS → **ST2504** identical; clinical distinct (EB-247=ST495, 153_ECLO=ST659). Independent of anything in the paper.
- `work/snp2/*.var` — minimap2 + paftools SNP calls against IF3SW-P2 reference for the other 4 ISS strains. Counts: 81–183 SNPs (paper reported 9–15 via bwa-mem + GATK; documented method-dependent gap).

## AMR / MDR (Claim C3)
- `work/amr/*.tsv` — per-strain AMRFinderPlus 4.2.7 outputs.
- `work/amr_summary.json` — aggregated per-strain AMR gene set.

All 5 ISS strains share an **identical** core AMR set:
- `blaACT` — AmpC class-C β-lactamase (paper Table 2: “Beta-lactamase class C and other PBPs”)
- `fosA` — fosfomycin resistance
- `oqxA` / `oqxB` — RND multidrug efflux
- `fieF` — ferrous-iron/metal efflux (Co/Zn/Cd)

Clinical strains carry an expanded set (silA, qnrE, blaIMI-1 carbapenemase in MBRL1077, extra fosA7) — consistent with the paper's theme of broader AMR in clinical isolates.

## Consolidated evidence
- `work/analysis_summary.md` — narrative synthesis of ANI + MLST + AMR + SNP results, keyed back to paper claims C1..C6.

## Judging
- `work/judge_scores.json` — 3-judge LLM rubric scores. Result: 2× PARTIAL, 1× REPLICATED. Means: Coverage 7.7 / Agreement 8.0 / Fidelity 7.0 / Reproducibility 7.0.

## Report deliverables
- `report/REPORT.md` — human-readable verdict + tables (canonical text report).
- `report/REPORT.tex` — LaTeX version with dedicated Genuine Critique section.
- `report/open_questions.json` — 5 truly open follow-on scientific questions (spaceflight-induced genome plasticity; ISS AMR-plasmid HGT dynamics; ESKAPE risk stratification for long-duration missions; biofilm gene repertoire on spacecraft surfaces vs ICU niches; comparative virulence phenotypes ISS vs clinical).
- `report/workflow.md` — pipeline description (retrieval → ANI → clonality → AMR → judging → report).
- `report/failure_analysis.md` — honest catalogue of what did not close and why.
- `report/artifacts_summary.md` — this file.

## Explicit non-artifacts (out of scope)
- **Wet-lab susceptibility phenotype data (C4).** Requires cultures/Vitek.
- **RAST subsystem gene counts (C5).** Not regenerated; AMRFinderPlus (different paradigm) used for the AMR subset only.
- **dDDH values.** Paper used GGDC web service; ANI serves as the equivalent species-boundary metric here.
- **Raw Illumina reads + bwa-mem + GATK SNP filter pipeline.** Would be needed to reproduce the paper's exact 9–15 SNP counts.

## Reproducibility footprint
- All tools free/local (fastANI, AMRFinderPlus 4.2.7, mlst 2.33.1, minimap2, paftools, biopython 1.87, NCBI Datasets 18.25.1).
- All genomes public; accessions verified against paper Table 1.
- Runs on a laptop in minutes; no GPU, no HPC, no paid API calls.
