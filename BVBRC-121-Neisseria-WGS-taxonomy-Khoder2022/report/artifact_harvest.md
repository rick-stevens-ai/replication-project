# Artifact Harvest — public data pulled for BVBRC-121

All fetched from NCBI Datasets REST via the `datasets` CLI on `uicgpu` (through the standard HTTP proxy). Every genome verified to contain "Neisseria" in the FASTA header (this check caught 7 wrong-taxon accessions in an initial guess-list that had to be dropped and replaced by taxon-search).

## Paper PDF
| item | source | size | notes |
|---|---|---|---|
| paper.pdf | https://europepmc.org/articles/PMC9657967?pdf=render | 2 074 401 B | full OA PDF, MDPI, doi 10.3390/ijms232113456 |

## Lebanese isolate genomes (paper's four novel WGS submissions)
| accession | strain | claimed species (paper) | header (as deposited) | bytes |
|---|---|---|---|---|
| GCA_900654165.1 | R19 (paper) / N13 (deposited) | N. flavescens | Neisseria flavescens strain N13 | 2 239 126 |
| GCA_900654175.1 | R20 (paper) / N32 (deposited) | N. mucosa | Neisseria mucosa strain N32 | 2 587 183 |
| GCA_900654185.1 | R21 (paper) / N57 (deposited) | N. flavescens | Neisseria flavescens strain N57 | 2 301 616 |
| GCA_900654195.1 | R23 (paper) / N78 (deposited) | N. flavescens | Neisseria flavescens strain N78 | 2 231 847 |

## Reference genomes (stratified subset of the paper's 128 refs)
| accession | strain | species (as deposited) | notes |
|---|---|---|---|
| GCF_000006845.1 | FA1090 | N. gonorrhoeae | paper's gono ref |
| GCF_000008805.1 | MC58 | N. meningitidis | paper's meni ref |
| GCF_005221285.1 | ATCC13120 | N. flavescens | complete chromosome; type-strain equivalent to paper's NCTC8263 (NCTC8263 accession itself was withdrawn/missing under GCF_000241835.1 in the current release) |
| GCF_001618015.1 | CD-NF1 | N. flavescens | draft |
| GCF_001618065.1 | CD-NF2 | N. flavescens | draft, mentioned in paper |
| GCF_002847985.1 | UMB0210 | N. perflava | draft, mentioned in paper |
| GCF_041433205.1 | 27098_8_142 | N. perflava | draft |
| GCF_005221305.1 | ATCC49275 | N. subflava | complete chromosome |
| GCF_003044355.1 | C2005001510 | N. subflava | draft |
| GCF_003044445.1 | C2008000159 | N. mucosa | draft — replacement for withdrawn paper ref ATCC 19696 (GCF_000185145.1 now empty in NCBI Datasets) |
| GCF_000220865.1 | ATCC33926 (old asm) | N. macacae | paper's macacae ref, older assembly (paper accession GCF_000186405.1 turned out to be a Streptococcus in current release — mixed-up assembly ID) |
| GCF_022749495.1 | ATCC33926 | N. macacae | current complete chromosome for ATCC33926 (paired against the old asm as an internal sanity check — 99.99% ANI ✓) |
| GCF_000260655.1 | VK64 | N. sicca (deposited) | mentioned in paper as example of NCBI mislabeling; independently confirmed here as 96.83% ANI to N. macacae |
| GCF_003351565.1 | M17106 | N. lactamica | complete chromosome (extra reference outside paper's ingroup) |
| GCF_900453895.1 | NCTC10660 | N. elongata | outgroup for the tree |

Total: 4 Lebanese + 15 references = 19 genomes.

## Dropped/withdrawn accessions encountered
- `GCF_000185145.1` (N. mucosa ATCC 19696, paper's mucosa ref) — download package returned only metadata, no `.fna`; the assembly appears to have been withdrawn/suppressed. Substituted with `GCF_003044445.1` (N. mucosa C2008000159, 96.06% ANI to R20).
- Seven original accession guesses returned non-Neisseria genomes (Bacillus, Bacteroides, Streptococcus, Streptomyces, Staphylococcus, Ligilactobacillus, E. coli) — these were dropped after a first-line-of-FASTA sanity check and replaced by taxon-search (`datasets summary genome taxon "Neisseria X"`).

## Tools + versions used
- NCBI `datasets` CLI 18.32.0 — genome download
- `skani` (in micromamba `amr` env, `~/micromamba/envs/amr/bin/skani`) — pairwise ANI (state-of-the-art, correlates >0.99 with OrthoANI at species-level distances)
- `mash` 2.x (same env) — k-mer distance sketch for cross-check
- Python 3.8.10 + numpy 1.23.5 + scipy 1.10.1 + matplotlib 3.7.5 + dendropy 5.0.8 — UPGMA tree + heatmap
- Argo LiteLLM aggregator (chicago-1 :4000, model `argo:gpt-5.2`) — free-endpoint LLM judge

## Analysis outputs (in `report/evidence/`)
- `ani_matrix_final.tsv` — 19×19 skani ANI matrix, strain-labeled
- `tree_heatmap.png` — UPGMA dendrogram + ANI heatmap figure
- `upgma_tree.nwk` — Newick tree
- `claim_verification.json` — per-claim numerical evidence
- `llm_judge_verdict.json` — LLM-judge verdict (PARTIAL, coverage 60%, agreement 75%)

Raw intermediates (in `work/results/`): `ani_matrix.tsv` (skani raw), `ani_triangle.tsv` (skani sparse), `mash_dist.tsv` (mash raw), `all_genomes.msh` (mash sketch), `genome_list.txt`.
