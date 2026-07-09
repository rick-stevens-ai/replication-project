# Attempt Log — BVBRC-39 (2026-07-01)

1. **Dedup** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i finegoldia` → none. Proceeded.
2. **Read briefs** — WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md.
3. **Paper located** — Europe PMC search → PMC5762925, DOI 10.1038/s41598-017-18661-8, open access. Fetched fullTextXML (free, 110 KB) → stripped to plain text.
4. **Extracted accessions** — Found 10 newly-sequenced WGS masters (NDYA–NDYJ) + 7 previously-published (AECM01, AP008971/2, ACHM02, LRPW01, AEDP01, AFUI01, JDVC01) from the Methods "Genome sequences" section.
5. **Extracted testable claims** — two clades @ 90.7% ANI; 12-genome subset = 4 magna + 8 nericia; core proteome 1202 orthologs (68% of avg CDS); CDS 1570–1906 avg 1760; CAMP 2–4 copies; protein L in ~10%; VF heterogeneity; pilus locus conserved.
6. **Mapped WGS → GCA** — queried NCBI Datasets taxon report (278 records). Matched all 17 paper strains 1:1 to current GCA accessions by WGS project prefix AND strain name (double-confirmed). Wrote `paper_17_map.tsv`.
7. **Downloaded genomes** — `datasets download genome accession --inputfile acc_list.txt --include genome,protein,gff3` → fin17.zip (17.4 MB), all 17 with genome + protein FASTA. (First attempt failed: CLI needs `--inputfile`, not space-joined args.)
8. **Genome stats** — `genome_stats.py`: mean CDS 1759 (paper 1760), range 1563–1956, GC 31.7–32.1%, sizes 1679–2033 kb. ✅ near-exact.
9. **ANI / two clades** — fastANI all-vs-all (17×17=289 comparisons). Average-linkage cut into 2 clades → magna=9, nericia=8; inter-clade ANI 90.67–91.70% (min 90.67 ≈ paper 90.7%); intra-clade mean 96.06%. ✅
   - Note: single-linkage @95% initially gave 3 clusters (sub-structure); the paper's *species-level* two-clade boundary sits at ~90.7% ANI, correctly recovered by the 2-way average-linkage cut.
10. **12-genome subset** — among the 10 new + 2 ATCC, split = exactly 4 magna + 8 nericia. ✅ EXACT match to paper. (Historically-labeled *F. magna* strains ATCC 53516 + CCUG54800 fall in the *nericia* clade — consistent with the paper's central "novel species hidden among F. magna" thesis.)
11. **Core/pan-genome** — CD-HIT clustering of 12 concatenated proteomes at c=0.5. Core (in all 12) = 1209 orthologs = 69.9% of avg CDS (paper: 1202 = 68%). Pan-genome 2992 families; 892 singletons → confirms strain-specific heterogeneity. ✅
12. **Virulence factors** — blastp curated UniProt F. magna references vs all 17 proteomes: CAMP 17/17, SufA 17/17 (conserved); FAF 12/17, PAB 8/17, albumin-binding 9/17 (heterogeneous); **protein L 2/17 = 11% (paper ~10%)** ✅. CAMP paralog count = 2/genome for all 17 (paper 2–4 range) ✅.
   - Annotation-keyword survey (`annotation_survey.json`) undercounted CAMP/pilus due to PGAP "hypothetical protein" labels — switched to homology (blastp) which resolved it.
13. **LLM judge** — Argo free `argo:gpt-5.2` (opus-4.8 fallback wired). Verdict **REPLICATED**, coverage 9/9, agreement 9/9.
14. **Wrote report/** — REPORT.md, brief.md, attempt_log.md, artifact_harvest.md, evidence/*.

## What worked
- Exact 1:1 recovery of all 17 original genomes → true same-data replication, not proxy.
- fastANI + CD-HIT independently reproduced the paper's headline numbers to within ~1%.

## What failed / needed fixing
- `datasets` CLI arg quoting (fixed with --inputfile).
- Annotation-keyword VF counting (fixed with blastp homology).
- Single-linkage 95% over-split (used 2-way average-linkage for the species boundary).

## Not attempted (gaps)
- Parsnp 126,647-core-SNP phylogeny + BRIG figures (ANI used as independent equivalent).
- Dedicated Fmp1 pilus phylogeny.
