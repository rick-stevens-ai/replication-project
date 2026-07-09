# Artifact Harvest — BVBRC-56

## Paper (open access)
- Liu WY, Wong CF, Chung KM, Jiang JW, Leung FC. "Comparative genome analysis of Enterobacter cloacae." PLoS One 2013;8(9):e74487.
- DOI: 10.1371/journal.pone.0074487 · PMID 24069314 · PMC3771936 · CC BY.
- Full text XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3771936/fullTextXML (220 KB, saved to work/fulltext.xml; readable text work/fulltext.txt)

## Genomes (all re-downloaded from NCBI nuccore by GenBank accession via efetch; free, no auth)
Downloaded to uicgpu:/data/stevens/bvbrc56/genomes/ (both .fna and full .gbk with parts).

| Strain | Role | GenBank accession(s) | .fna bytes | replicons |
|---|---|---|---:|---:|
| E.cloacae subsp. cloacae ENHKU01 | paper focal strain | CP003737.1 | 4,794,169 | 1 |
| E.cloacae subsp. cloacae ATCC13047 | E.cloacae comp | CP001918.1, CP001919.1, CP001920.1 | 5,679,045 | 3 |
| E.cloacae subsp. dissolvens SDM | E.cloacae comp | CP003678.1 | 5,039,296 | 1 |
| E.cloacae EcWSU1 | E.cloacae comp | CP002886.1, CP002887.1 | 4,866,788 | 2 |
| E.aerogenes KCTC2190 | Enterobacter comp | CP002824.1 | 5,355,847 | 1 |
| E.lignolyticus SCF1 (NCBI: "E.cloacae SCF1") | Enterobacter comp | CP002272.1 | 4,882,883 | 1 |
| E.asburiae LF7a | Enterobacter comp | CP003026.1, CP003027.1, CP003028.1 | 5,083,953 | 3 |
| Enterobacter sp. 638 | Enterobacter comp | CP000653.1, CP000654.1 | 4,743,400 | 2 |
| Pantoea sp. At-9b | outgroup | NC_014837.1 | 4,431,170 | 1 |
| Pantoea vagans C9-1 | outgroup | NC_014562.1 | 4,082,539 | 1 |
| Pantoea ananatis LMG20103 | outgroup | NC_013956.1 | 4,757,372 | 1 |

Note: paper's E. cloacae NCTC9394 was excluded by the authors themselves ("sequence data were not available for download"), so it is not part of this replication either.

## Derived artifacts (in report/evidence/)
- genome_stats.json — per-strain length/GC/CDS/tRNA/rRNA (Table 1 replication)
- pangenome_result.json — pan/core clusters + per-strain unique %
- functional_result.json, t6ss_result.json, t6ss_ge6.json — fimbriae / T6SS / carbohydrate counts
- aai_matrix.json, enterobacter_aai.nwk — proteome-wide AAI matrix + NJ tree (phylogenomics)
- llm_judge_gpt52.txt — free-Argo gpt-5.2 replication judge scorecard
- phylo_lite.py — phylogenomics script (copy)

## Tools (conda env bvbrc56 on uicgpu, created for this task)
DIAMOND, NCBI BLAST+, MAFFT, FastTree, ncbi-datasets-cli, Biopython (python 3.10, bioconda).
