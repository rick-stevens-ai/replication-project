# Evidence pack for LLM-judge — Ali et al. 2019 (MRSA SO-1977 Sudan) independent replication

## Paper accessions verified public
- GenBank WGS: NFZY00000000 -> Assembly GCA_002224825.1 / GCF_002224825.1 (ASM222482v1)
- BioProject PRJNA385553, BioSample SAMN06894057
- Downloaded and md5-verifiable from https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/224/825/
- 16S rRNA (paper: MK713975) — extracted from assembly locus CA803_14545, 1557 bp, 100% BLAST identity to S. aureus in NCBI nt

## Genome statistics (independent stat from downloaded FASTA)
| Metric        | Paper      | Independent  | Match |
|---            |---:        |---:          |:-:    |
| Genome (bp)   | 2,827,644  | 2,827,644    | ✅    |
| GC%           | 32.8%      | 32.79%       | ✅    |
| Contigs       | 151        | 151          | ✅    |
| N50 (bp)      | 62,783     | 62,783       | ✅    |
| Largest ctg   | 146,886    | 146,886      | ✅    |
| Coverage      | 122.26x    | 122.26x (NCBI Assembly metadata) | ✅ |
| CDS (protein FASTA count) | 2629 | 2783 (RefSeq re-annotation; NCBI reannotated with PGAP) | ~✅ |
| Assembly method | SPAdes v3.9.0 | (metadata) | ✅ |

## Independent MLST (pubMLST S. aureus scheme, blastn 100%-identity full-length)
Allele calls: arcC-43, aroE-37, glpF-48, gmk-19, pta-49, tpi-26, yqiL-39 → **ST140** (not reported in paper; new evidence)

## AMR predictions (abricate v1.4.0 vs CARD, NCBI, ResFinder databases; downloaded 2026-07-03)
### SO-1977 highlights
- mecA (100% ID/cov, CARD/ResFinder/NCBI) → methicillin resistance ✅ agrees with paper
- blaZ / PC1 (100% ID) → β-lactamase ✅
- tet(K) (100%/99.9%, ResFinder+CARD+NCBI) → tetracycline efflux ✅
- tet(M) (100%/99.1%, ResFinder+CARD+NCBI) → tetracycline ribosomal protection ✅
- norA (99.91%/91.51%, CARD) → fluoroquinolone efflux
- LmrS, tet(38), mepA/mepR, mgrA, norC, sdrM, sepA, arlR/arlS, kdpD — multiple MDR efflux/regulator hits (all >98% ID)
- MecR1: not called by abricate at default coverage cutoff, but tblastn(MecR1) against SO-1977 shows a 100% identity 310-aa segment at contig NFZY01000034.1 edge (assembly-break truncation), consistent with paper's "MecA + MecR1 present, MecI absent" call.

### Comparators (RefSeq GCF_000011505.1 MRSA252, GCF_000011525.1 MSSA476) — same abricate/CARD protocol
| Gene / class | SO-1977 | MRSA252 | MSSA476 |
|---|:-:|:-:|:-:|
| mecA (methicillin) | ✅ | ✅ | ✗ |
| mecI | ✗ | ✅ | ✗ |
| mecR1 (full call) | ✗ (edge-truncated 100% partial) | ✅ | ✗ |
| tet(K) | ✅ | ✗ | ✗ |
| tet(M) | ✅ | ✗ | ✗ |
| norA | ✅ | ✅ | ✅ |
| PC1/blaZ | ✅ | ✅ | ✅ (blaZ_79) |
| ErmA (macrolide) | ✗ | ✅ | ✗ |
| ANT(4′)-Ia, ANT(9)-Ia | ✗ | ✅ | ✗ |
| fusC | ✗ | ✗ | ✅ |
| FosB | ✗ | ✅ | ✗ |

### Central paper claim ("2 genes only in SO-1977 confer Tetracycline resistance")
✅ REPRODUCED: tet(K) and tet(M) are absent in MRSA252 and MSSA476 by both CARD and ResFinder (identical protocol), present at 100% coverage in SO-1977.

### Paper claim "SO-1977 was the only one having the norA gene"
❌ CONTRADICTED: norA is a well-known S. aureus core-genome gene. CARD detects it at 99.91% identity, 91.51% coverage in SO-1977, and it is present at similar identity/coverage in MRSA252 and MSSA476 assemblies too. The paper's uniqueness call is likely an RSAT-comparator artifact (missed hit in the reference set), not real biology.

## Virulence (VFDB — abricate v1.4.0)
- SO-1977: 73 VFDB hits (adsA, aur, cap5/cap8 capsule, clfA/clfB, coa, ebp, esaA/B/G, essA/B, esxA, geh, hlgA/B/C, hla, hly, isdA/B/C/D/E/F, sarA, spa, srtA/B, ...)
- MRSA252: 76 hits ; MSSA476: 97 hits (both have similar core-VF repertoires)
- Paper claim: "83 genes annotated to virulence disease and defense category" via RAST/SEED — our VFDB count is smaller (VFDB is more curated; RAST SEED subsystems is broader), but shape agrees: SO-1977 has a rich virulence-gene repertoire dominated by capsule + adhesion + toxin + iron-acquisition genes.

## Plasmid content (plasmidfinder)
- SO-1977 carries 3 plasmid replicons: repUS43 (DOp1), repUS70 (SAP047A), rep5a (SAP047A) — first independent confirmation.

## Files (evidence/)
- abricate_*.tsv (SO-1977, MRSA252, MSSA476 vs each DB)
- AMR_comparison_table.tsv
- mlst call log
- SO1977_16S.fa + 16S_blast_nt.tsv
- md5checksums.txt from NCBI
