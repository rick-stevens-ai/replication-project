# BVBRC-30 — MDR *Enterobacter bugandensis* from the ISS (Singh/Urbaniak et al. 2018)

## Metadata
- **Paper:** Multi-drug resistant *Enterobacter bugandensis* from the ISS and comparative genomics with human pathogenic strains
- **Journal/DOI:** BMC Microbiology 2018, 18:175 · 10.1186/s12866-018-1325-2 · PMID 30466389 · PMCID PMC6251167
- **Domain:** microbial comparative genomics / AMR
- **Status:** PARTIAL (strong core replication; verdict from 3 independent LLM judges: 2 PARTIAL, 1 REPLICATED)

## Claims Tested
- C1 Species ID by ANI (ISS = *E. bugandensis*) — **replicated** (ANI to clinical comparators within 0.03–0.30% of paper Table 1)
- C2 5 ISS strains near-clonal — **replicated** (fastANI ≥99.988%; identical MLST ST2504)
- C3 AMR/MDR gene repertoire — **replicated** (blaACT AmpC, fosA, oqxAB, metal efflux across all 5)
- C4 wet-lab susceptibility — not reproducible (genotype consistent)
- C5 genome stats/gene counts — consistent (RAST counts not re-run)
- C6 phylogenetic placement — superseded by MLST+ANI

## What Was Reproduced
Downloaded the 5 ISS + 3 clinical *E. bugandensis* deposited genomes (BioProject PRJNA319366 + paper accessions) plus 5 outgroup *Enterobacter* species; ran all-vs-all fastANI, AMRFinderPlus, MLST, and minimap2/paftools SNP calling on real data.

## How to Run
```bash
cd work
# genomes downloaded via: datasets download genome accession <list> --include genome
fastANI --ql genome_list.txt --rl genome_list.txt -o ani_matrix.tsv -t 8
conda run -n amrfinder amrfinder -n genomes/<strain>.fna --plus -o amr/<strain>.tsv
conda run -n mlst-env mlst genomes/*.fna
```

## Results
- `report/REPORT.md` — full analysis
- `work/ani_summary.json`, `work/amr_summary.json`, `work/genome_stats.json`, `work/judge_scores.json`

## Limitations
Exact SNP counts differ (assembly-vs-assembly 81–183 vs paper's read-mapping 9–15; same clonality conclusion). Wet-lab phenotypes and RAST subsystem counts not computationally reproduced. All compute free/local.
