# Fluit et al. 2021 - Paper Notes
## "Characterization of clinical Ralstonia strains and their taxonomic position"
DOI: 10.1007/s10482-021-01637-0 | PMID: 34463860 | PMC: PMC8448721

## Key Data
- 18 clinical Ralstonia strains sequenced (Illumina NextSeq)
- BioProject: PRJNA611754
- SRP: SRP252286
- 54 additional strains from GenBank used for ANIb

## 18 Study Strains
| Strain | Species (WGS) | Group | Country |
|--------|--------------|-------|---------|
| 16-551634 | R. pickettii | E2 | Netherlands |
| 16-551636 | R. pickettii | E2 | Netherlands |
| 16-543514 | R. pickettii | E2 | Netherlands |
| 16-551632 | R. pickettii | E2 | Netherlands |
| 16-551637 | R. pickettii | E2 | Netherlands |
| 16-543504 | R. pickettii | E1 | Netherlands |
| 16-551631 | R. pickettii | E1 | Netherlands |
| 16-551635 | R. pickettii | E1 | Netherlands |
| 16-535633 | R. mannitolilytica | D2 | Spain |
| 16-535634 | R. mannitolilytica | D2 | Spain |
| 16-535635 | R. mannitolilytica | D2 | Spain |
| 16-545260 | R. mannitolilytica | D2 | USA |
| 16-545261 | R. mannitolilytica | D2 | USA |
| 16-535632 | R. mannitolilytica | D2 | Spain |
| 16-535638 | R. mannitolilytica | D1 | Spain |
| 16-543498 | R. mannitolilytica | D1 | Netherlands |
| 16-551633 | R. insidiosa | G | Netherlands |
| 16-535637 | R. new spp. | F | Spain |

## Quantitative Claims to Test
1. **Genome sizes**: R. mannitolilytica avg 5,272,894 bp; R. pickettii avg 4,932,406 bp; R. insidiosa 6,385,888 bp; new spp. 5,676,110 bp
2. **GC content**: R. mannitolilytica 65.85%; R. pickettii 63.68%; R. insidiosa 63.25%; new spp. 63.32%
3. **cgMLST based on 517 core genes** - tree topology separating species
4. **ANIb clustering into 8 groups (A-H)** with 0.95 cutoff for species
5. **All 18 strains carry blaOXA-22 and blaOXA-60 family genes**
6. **Only strains 545260 and 545261 carry additional resistance genes** (aadA2, ant(2'')-Ia, aph(6)-Id, cmlA1, strA, sul1)
7. **Colistin MICs >16 mg/l for all strains**
8. **Ciprofloxacin MICs ≤0.12 mg/l** for most strains (exceptions: 4 R. mannitolilytica ≥32)
9. **Co-trimoxazole MICs ≤1 mg/l** for most (exceptions: 3 R. mannitolilytica ≥8)
10. **16S rRNA tree: 78 sequences, 1395 positions, log likelihood -2740.49**
11. **OXA-22 tree: 29 amino acid sequences, 279 positions**
12. **OXA-60 tree: 27 amino acid sequences, 271 positions**
13. **R. pickettii FDAARGOS-410 clusters with R. mannitolilytica (group D2)** in ANIb
14. **At least 45-fold coverage for all 18 strains**
15. **Maximum 117 contigs** per strain

## Methods
- Assembly: SPAdes v3.11.1, contigs ≥500 bp with ≥10x coverage
- ANIb: pyani v0.2.3, BLAST 2.2.28+, 1020 bp fragments, complete linkage, Euclidean distance
- cgMLST: Ridom SeqSphere v5.0.0, 517 core genes, 90% identity threshold
- Annotation: RAST v2.0
- AMR: ResFinder
- Phylogenetics: MEGA-X v10.0.4 (JTT for OXA, Tamura-Nei for 16S), 500 bootstrap
- MICs: ISO broth microdilution
