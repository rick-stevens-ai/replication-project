# Artifact Harvest — BVBRC-107

## Paper
- **PDF (Open Access, CC0)**: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0220494&type=printable → `work/paper.pdf` (1,314,417 bytes)
- **PMC**: https://pmc.ncbi.nlm.nih.gov/articles/PMC6667211
- **DOI**: 10.1371/journal.pone.0220494 · **PMID**: 31361781 · **Venue**: PLoS ONE 14(7):e0220494 (2019-07-30)

## Genome assemblies (deposited by the authors)

All from NCBI Nucleotide via eutils `efetch` (rettype=fasta, retmode=text). Public, no auth.

| Strain | Accession | Molecule | Length (bp) | Paper's stated size |
|---|---|---|---|---|
| CFSAN027343 | CP037943.1 | Chromosome | 5,768,712 | ~5.7 Mb (5,770,507 file bytes; fasta) |
| CFSAN027343 | CP037944.1 | Plasmid pCFSAN027343 | ~88,561 | 88 kb ✓ |
| CFSAN027346 | CP037945.1 | Chromosome | ~5,672,000 | ~5.6 Mb |
| CFSAN027346 | CP037946.1 | Plasmid pCFSAN027346-1 | ~95,599 | 95 Kb ✓ |
| CFSAN027346 | CP037947.1 | Plasmid pCFSAN027346-2 | ~72,000 | 72 Kb ✓ |
| CFSAN027350 | CP037941.1 | Chromosome | ~5,451,905 | ~5.4 Mb |
| CFSAN027350 | CP037942.1 | Plasmid pCFSAN027350 | ~157,300 | 157 kb ✓ |

Downloaded to `work/ncbi_fasta/*.fa` (7 files, 17.4 MB total). Full paper accession statement: "MiSeq data (SRR8333591, SRR8333592, SRR8333590), MinION data (SRR8335317, SRR8335318, SRR8335317), and PacBio assemblies [CFSAN027343 (CP037943 and CP037944), CFSAN027346 (CP037945, CP037946, and CP037947), and CFSAN027350 (CP037941 and CP037942)]."

## Reference databases (CGE, public via Bitbucket)

| DB | Repo | # sequences | Notes |
|---|---|---|---|
| PlasmidFinder | bitbucket.org/genomicepidemiology/plasmidfinder_db | 488 | Enterobacteriales + all Inc replicons |
| VirulenceFinder (E. coli + stx) | bitbucket.org/genomicepidemiology/virulencefinder_db | 5,102 | virulence_ecoli.fsa + stx.fsa concatenated |
| ResFinder (all classes) | bitbucket.org/genomicepidemiology/resfinder_db | 3,212 | all.fsa concatenated set |
| SerotypeFinder (O+H) | bitbucket.org/genomicepidemiology/serotypefinder_db | ~500 | O_type.fsa + H_type.fsa |
| pubMLST (mlst tool) | tseemann/mlst bundled | – | `ecoli` (Pasteur), `ecoli_achtman_4` (Achtman = paper's scheme) |
| AMRFinderPlus DB | NCBI, version 2024-07-22.1 | – | Downloaded via `amrfinder_update`; used with `--organism Escherichia --plus` |

## Tools used

Same or equivalent free tools as the paper:

| Paper tool | Version in paper | This replication | Version |
|---|---|---|---|
| Ridom SeqSphere+ (MLST) | v2.4.0 (Achtman scheme) | `mlst` (Torsten Seemann) | 2.35.0 (`ecoli_achtman_4`) |
| VirulenceFinder | 1.5 (CGE) | direct BLAST vs virulence_ecoli.fsa + AMRFinderPlus (with --plus) | blastn 2.16.0, AMRFinderPlus 3.12.8 |
| ResFinder | 2.1 (CGE) | direct BLAST vs resfinder all.fsa + AMRFinderPlus | idem |
| PlasmidFinder (implicit) | – | direct BLAST vs plasmidfinder_db | blastn 2.16.0 |
| serotype (paper: gene set from Ridom) | – | direct BLAST vs serotypefinder O_type+H_type | blastn 2.16.0 |

All BLAST screens use megablast, `-perc_identity 90`, `-qcov_hsp_perc 60`, `-evalue 1e-30`.

## Compute environment
- `ssh uicgpu` (~/env.sh for proxy internet)
- micromamba env: `~/micromamba/envs/amr` (blast 2.16.0, AMRFinderPlus 3.12.8, mlst 2.35.0)
- Work dir: `~/work/bvbrc107/`
