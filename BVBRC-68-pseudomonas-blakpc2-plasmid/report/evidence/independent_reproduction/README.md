# Independent from-scratch reproduction — 2026-07-03 16:13 CDT

Re-ran BVBRC-68 independently (fresh NCBI efetch by accession, separate stdlib
code + separate BLAST) to VERIFY the replication's numbers rather than assert them.
~3 minutes, laptop, no GPU.

| Claim | Replication reported | Independent re-run | Match |
|---|---|---|---|
| C1 length pPA1011 (MH734334.1) | 62,793 bp | 62,793 bp | exact |
| C2 GC% | 58.78% | 58.78% | exact |
| C3 KPC-2 protein length | 293 aa | 293 aa | exact |
| C3 identity to canonical KPC-2 | 100.00% | 293/293 = 100.00% | exact |
| C4 blaKPC CDS | environment | 17,676-18,557, "Carbapenem-hydrolyzing beta-lactamase KPC" | confirmed |
| C5 novelty vs p14057 (KY296095.1) | 82.15% @ 98.70% id | 82.17% @ 98.65% id | within BLAST jitter |

C1-C4 are bit-identical (deterministic by accession). C5 delta is BLAST HSP-set
jitter (22 HSPs this run vs 19 original). Conclusion: BVBRC-68 reproduces cleanly
from public accessions with standard bioinformatics tools.
