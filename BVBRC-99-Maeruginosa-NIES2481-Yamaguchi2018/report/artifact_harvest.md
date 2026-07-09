# Artifact harvest — BVBRC-99

All artifacts are publicly available (no auth), pulled 2026-07-04 via NCBI
E-utilities and PMC.

| Artifact | URL / accession | Size | Notes |
|---|---|---:|---|
| Paper (PMC HTML) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5865083/ | 133,763 B | CC BY-NC, extracted text 19,939 B |
| NIES-2481 chromosome FASTA | NCBI nuccore CP012375.1 (uid 1052158287) | 4,354,398 B | 4,293,006 bp seq |
| NIES-2481 chromosome GenBank | NCBI nuccore CP012375.1, rettype=gbwithparts | 9,118,526 B | 4,292 CDS, 6 rRNA, 41 tRNA |
| NIES-2481 plasmid FASTA | NCBI nuccore CP025929.1 (uid 1333047330) | 149,723 B | 147,539 bp seq |
| NIES-2481 plasmid GenBank | NCBI nuccore CP025929.1, rettype=gbwithparts | 325,943 B | 164 CDS, 5 repeat_region |
| NIES-2549 chromosome FASTA | NCBI nuccore CP011304.1 (uid 815963219) | 4,355,622 B | 4,294,213 bp seq |
| NIES-2549 chromosome GenBank | NCBI nuccore CP011304.1, rettype=gbwithparts | 9,138,778 B | 4,282 CDS, 6 rRNA, 41 tRNA |
| NIES-2549 plasmid FASTA | NCBI nuccore CP026286.1 (uid 1336651322) | 7,163 B | 6,987 bp seq |
| mcyA reference proteins | NCBI protein WP_061431778.1, WP_012266628.1, BAG03679.1 | 8,691 B | 3 × 2,787 aa (McyA canonical) |

## Derived evidence files (report/evidence/)

| File | Description |
|---|---|
| `summary_stats.json` | JSON of length + GC + feature counts + tblastn tallies |
| `NIES2481_16S.fasta` | 2 × 1,460-bp 16S rRNA copies from NIES-2481 chromosome |
| `NIES2549_16S.fasta` | 2 × 1,460-bp 16S rRNA copies from NIES-2549 chromosome |
| `mcyA_vs_chr.tsv` | tblastn hits of mcyA refs vs NIES-2481 chromosome (117 lines, none strict) |
| `mcyA_vs_pla.tsv` | tblastn hits of mcyA refs vs NIES-2481 plasmid (0 lines) |
