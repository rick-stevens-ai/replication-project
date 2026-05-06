# Shrestha et al. 2022 - Paper Notes

## Citation
Shrestha P, et al. "Prediction of trehalose-metabolic pathway and comparative analysis of KEGG, MetaCyc, and RAST databases based on complete genome of Variovorax sp. PAMC28711." BMC Genomic Data 23, 2 (2022). https://doi.org/10.1186/s12863-021-01020-y

## Key Info
- **PMID**: 34991451 / PMC8734048
- **GenBank accession**: NZ_CP014517.1
- **KEGG organism code**: vaa (pathway map vaa00500 - "Starch and sucrose metabolism")
- **Organism**: Variovorax sp. PAMC28711 (cold-adapted, lichen-associated, Antarctic)

## Core Claims (from paper)

### Table 1: Enzyme presence across databases
| Pathway | EC Number | KEGG | MetaCyc | RAST |
|---------|-----------|------|---------|------|
| OtsA (trehalose-6-P synthase) | EC 2.4.1.15 | O | O | O |
| OtsB (trehalose-6-P phosphatase) | EC 3.1.3.12 | O | O | O |
| TreY (maltooligosyl-trehalose synthase) | EC 5.4.99.15 | X | X | O |
| TreZ (maltooligosyl-trehalose trehalohydrolase) | EC 3.2.1.141 | O | O | O |
| TreS (trehalose synthase) | EC 5.4.99.16 | O | O | O |

"O" = present, "X" = absent

### Table 2: Database comparison (versions from Aug 2018)
| Category | MetaCyc (Base) | KEGG (Module) | MetaCyc (Superpathways) | KEGG (Map) |
|----------|---------------|---------------|------------------------|------------|
| Pathway count | 2,688 | 339 | 381 | 530 |
| Pathway reactions | 15,329 | 11,004 | - | - |

### Key findings:
1. KEGG had 1 missing enzyme: TreY (EC 5.4.99.15)
2. MetaCyc also missing TreY (EC 5.4.99.15)
3. RAST found all enzymes including TreY
4. Three biosynthesis pathways: OtsA/OtsB, TreY/TreZ, TreS
5. One degradation pathway: TreH (trehalase)
6. TreY CDS found at positions 335612-3352054 via RAST/SEED Viewer
7. Five distinct trehalose synthesis pathways exist in nature (TreY/TreZ, TreS, OtsA/OtsB, TreP, TreT)
8. Variovorax sp. PAMC28711 uses 3 of the 5 pathways
9. MetaCyc v22.5 had 2,688 pathways
10. KEGG v87.0 had 339 metabolic modules
11. MetaCyc had 2,859 pathways from 3,185 organisms (later in text)
12. MetaCyc had 15,329 reactions vs KEGG 11,004

## Trehalose biosynthesis pathways mentioned:
1. OtsA/OtsB (EC 2.4.1.15 / EC 3.1.3.12) - present in archaea, bacteria, fungi, plants, arthropods, protists
2. TreY/TreZ (EC 5.4.99.15 / EC 3.2.1.141) - present in archaea and bacteria
3. TreS (EC 5.4.99.16) - present only in bacteria
4. TreP (EC 2.4.1.64) - present in protists, bacteria, and fungi
5. TreT (EC 2.4.1.245) - present in archaea and bacteria

## Figures
- Fig 1: KEGG pathway map (vaa00500) - starch and sucrose metabolism
- Fig 2: MetaCyc trehalose biosynthesis + degradation pathways
- Fig 3: Complete trehalose metabolic pathway summary
- Fig 4: RAST annotation showing trehalose biosynthesis genes
