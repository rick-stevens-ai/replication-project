# Artifact Harvest — BVBRC-29

## Source paper
- `work/bazinet2017.pdf` (7.5 MB) + `work/bazinet2017.txt` (116 KB) — Bazinet AL 2017, BMC Evol Biol 17:176, DOI 10.1186/s12862-017-1020-1, PMID 28768476. Open Access (CC-BY 4.0). (Pre-downloaded.)

## Public genome data (NCBI Datasets REST, free/no-auth)
Downloaded 2026-07-01 via `datasets download genome accession <ACC> --include genome` (datasets 18.32.0). 27 genomes, 41 MB package, all records validated. Full accession→label map in `evidence/accessions.txt`. Seeded from the paper's Table 1 RefSeq accessions:

| Accession | Label | Species | Role |
|-----------|-------|---------|------|
| GCF_000007845.1 | B_anthracis_Ames | *B. anthracis* Ames | Table 1 HaMStR ref |
| GCF_000007825.1 | B_cereus_ATCC14579 | *B. cereus s.s.* ATCC 14579 | Table 1 HaMStR ref |
| GCF_000017425.1 | B_cytotoxicus_NVH391-98 | *B. cytotoxicus* | Table 1 HaMStR ref |
| GCF_000832605.1 | B_mycoides_ATCC6462 | *B. mycoides* | Table 1 HaMStR ref |
| GCF_000161455.1 | B_pseudomycoides_DSM12442 | *B. pseudomycoides* | Table 1 HaMStR ref |
| GCF_000008505.1 | B_thuringiensis_97-27 | *B. thuringiensis* 97-27 | Table 1 HaMStR ref |
| GCF_000496285.1 | B_toyonensis_BCT-7112 | *B. toyonensis* | Table 1 HaMStR ref |
| GCF_000018825.1 | B_weihenstephanensis_KBAB4 | *B. weihenstephanensis* KBAB4 | Table 1 HaMStR ref |
| GCF_000712595.1 | B_manliponensis_root | *B. manliponensis* | paper's root taxon |
| GCF_000299035.1 | B_bingmayongensis | *B. bingmayongensis* | BCSL_498 addition |
| GCF_008807735.1 | B_wiedmannii | *B. wiedmannii* | BCSL_498 addition |
| GCF_0016832xx / 0016830xx (6) | B_anthracis_2..7 | *B. anthracis* strains | clonality test |
| GCF_000143605 / 000833275 / 000021225(AH187) / 000290435 | B_cereus_2..4 | *B. cereus* | diversity |
| GCF_000190515 / 000015065 / 000832825 / 001455345 / 000833085 / 000832985 | B_thuringiensis_2..7 | *B. thuringiensis* | diversity |

## Generated artifacts (in evidence/)
- `genome_stats.csv` — contigs, length, GC% per genome
- `fastani_out.tsv` — all-vs-all FastANI (627 pairs)
- `mash_dist.tsv` — all-vs-all Mash distances (729 pairs)
- `ani_summary.txt` — ANI clonality/nesting/cohesion analysis
- `roary_full27_summary.txt` — full 27-genome pan-genome (0 core / 48,118 total)
- `roary_i80_26genomes_summary.txt` — 26 genomes @ blastp 80% (251 core / 26,839 total)
- `roary_clade1_summary.txt` — 17-genome homogeneous Clade-1 (2,415 core / 15,247 total)
- `panacc_clade1_pan.Rtab`, `panacc_clade1_core.Rtab`, `panacc_clade1_new.Rtab` — accumulation curves (open pan-genome)
- `core_gene_tree_clade1.nwk` — FastTree GTR ML tree from Roary core alignment
- `accessory_binary_tree_clade1.nwk` — Roary accessory presence/absence tree (Bazinet's "accessory binary tree")
- `llm_judge_verdict.json` (+ `_pretty.json`) — free-Argo LLM-judge scoring (verdict PARTIAL)
- `llm_judge_prompt.py` — exact judge prompt + evidence bundle used

## Full intermediate data (on uicgpu, not synced to Dropbox due to size)
`/data/stevens/bvbrc29/` — raw FASTAs (`fasta/`), Prokka GFFs (`gff/`), full Roary output dirs (`roary_out/`, `roary_i80/`, `roary_clade1/` incl. `gene_presence_absence.csv`, `core_gene_alignment.aln`), Mash sketch. Reproducible from `accessions.txt` + the scripts in that dir (`stats.py`, `ani.py`, `run_prokka.sh`, `run_roary.sh`, `roary2.sh`, `clade1.sh`, `tree_final.sh`).
