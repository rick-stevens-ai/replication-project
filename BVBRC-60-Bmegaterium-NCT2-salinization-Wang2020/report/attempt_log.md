# Attempt Log

1. Read WAVE_BRIEF_2026-07-01.md and BVBRC-17 exemplar structure.
2. Dedup candidate selection from BVBRC_TOPUP85_2026-06-26.tsv ranks 48+. Verified existing set (BVBRC-01..59) via `ls`. Rank 48 = *Bacillus megaterium* NCT-2 (PMID:32190639) — no Bacillus megaterium in existing set, genome-announcement/comparative-genomics paper with clear public data → selected. Rank 49 (L. plantarum) overlaps BVBRC-08; skipped.
3. Confirmed OA via Europe PMC (PMCID PMC7066406, CC-BY). Downloaded full-text XML → text. Extracted 11 accessions CP032527–CP032537.
4. Located deposited assembly: `esearch` assembly db → GCA_000334875.3 / GCF_000334875.3 (Complete Genome; species reclassified *Priestia megaterium*). v.1 is the old draft (204 contigs); v.3 is the complete genome. Downloaded GCA_000334875.3 (FASTA+GFF+protein) via NCBI Datasets v2 REST.
5. Computed per-replicon size/GC (Python stdlib): chromosome 5,193,616 bp / 38.18% + 10 plasmids (9,625–132,087 bp), total 5,883,957 bp / 37.78%. → C1, C2 match.
6. Parsed GFF for feature counts: 6,038 gene+pseudo, 5,605 proteins, 203 RNA genes, 230 pseudogenes, 142 tRNA, 53 rRNA (19×5S,17×16S,17×23S). → C3 essentially exact.
7. Downloaded 5 comparator genomes. First attempt mis-mapped two accessions (GCF_000023165.1 was Mycoplasma, GCF_000022825.1 was Yersinia); re-resolved correct accessions via esearch: QM B1551=GCF_000025825.1, DSM 319=GCF_000025805.1, subtilis 168=GCF_000009045.1, cereus Q1=GCF_000013065.1, licheniformis DSM13=GCF_000011645.1. Recomputed comparative table → matches Table 1 within 0.1–0.3%. → C4.
8. Ran fastANI NCT-2 vs the 5 comparators: DSM 319 = 98.2% (closest), QM B1551 = 96.5% (2nd), others <80% (unreported/distant). Reproduces paper phylogenetic ordering. → C5.
9. Grep functional gene inventories in deposited protein annotation: nitrogen metabolism, phosphate (pstSCAB + alk. phosphatase + glucose 1-DH), IAA (aldehyde DH + amidase), stress (glycine betaine ABC, betaine-aldehyde DH, SOD, catalase) — all present. → C6.
10. LLM judge (Argo gpt-5.2, free proxy): REPLICATED, coverage 1.00, agreement 1.00. Wrote evidence + report.

## What worked / failed
- Worked: NCBI Datasets REST for genome + annotation; deposited genome carries full RefSeq annotation so gene/RNA counts reproduced almost exactly; fastANI cleanly reproduced the phylogenetic ordering.
- Failed then fixed: two initial guessed comparator accessions were wrong species — resolved by esearch lookups before use.
- All compute ran locally (small genomes, ~6 Mb each); no need for uicgpu.
