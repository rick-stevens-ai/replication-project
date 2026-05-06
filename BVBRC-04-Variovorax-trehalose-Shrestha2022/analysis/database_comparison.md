# Database Comparison: KEGG vs MetaCyc vs RAST

## Replication of Paper Table 2: Database statistics

### Paper's Table 2 (versions as of Aug 2018)

| Category | MetaCyc (Base pathways) | KEGG (Modules) | MetaCyc (Superpathways) | KEGG (Pathway maps) |
|----------|------------------------|----------------|------------------------|---------------------|
| Pathway count | 2,688 | 339 | 381 | 530 |
| Pathway reactions | 15,329 | 11,004 | - | - |

### Current Database Versions (May 2026)

| Category | Value (2026) | Paper Value (2018) | Notes |
|----------|-------------|-------------------|-------|
| KEGG release | 118.0+ | 87.0 | ~31 releases later |
| KEGG total reference pathways | 585 | 530 | Growth: +10.4% |
| KEGG total modules | 692,069 | ~339 (ref) | Large growth (organism-specific modules) |
| KEGG total KOs | 28,216 | - | |
| KEGG total genomes | 26,598 | - | |
| MetaCyc version | 29.6 | 22.5 | 7 major versions later |

**Note:** The paper's Table 2 values represent the 2018 snapshot. We cannot reproduce
the exact 2018 numbers from current APIs since both KEGG and MetaCyc have grown significantly.
The paper's numbers are consistent with the documented growth trajectory of both databases.

### Organism-specific statistics for Variovorax sp. PAMC28711

| Metric | KEGG (vaa) | BV-BRC/RAST | NCBI RefSeq |
|--------|-----------|-------------|-------------|
| Total genes | 4,159 | 4,263 (PATRIC CDS) | 4,104 (RefSeq CDS) |
| Pathway maps with genes | 133 | - | - |
| Modules with genes | 56 | - | - |
| Subsystems annotated | - | 191 | - |
| Genome size (bp) | 4,316,152 | 4,316,152 | 4,316,152 |
| GC content (%) | - | 65.97 | 65.97 |
| Contigs | 1 | 1 | 1 |

## Trehalose Pathway Coverage Comparison

### MetaCyc reference pathways (all 7 trehalose biosynthesis pathways)

| MetaCyc ID | Name | Key Enzymes | In Variovorax? |
|------------|------|-------------|----------------|
| TRESYN-PWY | trehalose biosynthesis I | OtsA + OtsB | YES (both present) |
| PWY-881 | trehalose biosynthesis II | TreP-like + phosphatase | PARTIAL |
| TREHALOSESYN-PWY | trehalose biosynthesis III | trehalose synthase + phosphatase | PARTIAL |
| PWY-2622 | trehalose biosynthesis IV | TreS | YES |
| PWY-2661 | trehalose biosynthesis V | TreX + TreY + TreZ | YES* (TreY debated) |
| PWY-5983 | trehalose biosynthesis VI | TreT | NO |
| PWY-5985 | trehalose biosynthesis VII | TreP | NO |

*TreY is present in RAST but called pseudogene in NCBI/KEGG

### Paper's claim: "3 of 5 known trehalose pathways present"
- OtsA/OtsB pathway: **CONFIRMED** (all databases agree)
- TreY/TreZ pathway: **CONFIRMED with caveat** (RAST says functional, NCBI says pseudogene)
- TreS pathway: **CONFIRMED** (all databases agree)
- TreP pathway: **CONFIRMED absent** (all databases agree)
- TreT pathway: **CONFIRMED absent** (all databases agree)
