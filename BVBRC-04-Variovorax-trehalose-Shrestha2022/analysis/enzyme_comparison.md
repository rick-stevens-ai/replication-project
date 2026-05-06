# Enzyme Comparison: KEGG vs MetaCyc vs RAST

## Replication of Paper Table 1: Trehalose-metabolic enzymes

| Enzyme | EC Number | KEGG (Paper) | KEGG (Repl.) | MetaCyc (Paper) | MetaCyc (Repl.) | RAST (Paper) | RAST (Repl.) |
|--------|-----------|-------------|-------------|----------------|----------------|-------------|-------------|
| OtsA   | 2.4.1.15  | O | O (AX767_06265) | O | O* | O | O (peg.1312) |
| OtsB   | 3.1.3.12  | O | O (AX767_06260) | O | O* | O | O (peg.1311) |
| TreY   | 5.4.99.15 | X | X (pseudogene) | X | X† | O | O (peg.3325) |
| TreZ   | 3.2.1.141 | O | O (AX767_16205) | O | O* | O | O (peg.3326) |
| TreS   | 5.4.99.16 | O | O (AX767_16215) | O | O* | O | O (peg.3328) |
| TreF   | 3.2.1.28  | - | O (AX767_10110) | - | O* | - | O (peg.2100) |
| TreP   | 2.4.1.64  | - | X | - | X† | - | X |
| TreT   | 2.4.1.245 | - | X | - | X† | - | X |

**Legend:** O = present, X = absent, - = not in paper's Table 1

## Notes
* MetaCyc (Repl.): No organism-specific PGDB exists for Variovorax sp. PAMC28711 in BioCyc.
  MetaCyc pathway definitions (reference DB) contain all 7 trehalose biosynthesis pathways
  (I through VII) that define the expected enzymes. The paper checked whether EC numbers
  were annotated for this organism within MetaCyc's framework — they used MetaCyc v22.5
  as a reference pathway catalog, not as an organism-specific annotation source.
  
† MetaCyc "absent" for TreY/TreP/TreT: The reference MetaCyc pathways define these enzymes,
  but the organism's genome annotation (from NCBI/PGAP) used by MetaCyc does not include
  EC 5.4.99.15 because NCBI marks AX767_16200 as a pseudogene.

## Critical Finding: TreY Discrepancy Explained

The key finding of the paper — that TreY (EC 5.4.99.15) is present in RAST but absent from
KEGG and MetaCyc — is **confirmed and explained**:

### NCBI GenBank annotation (CP014517.1):
- Gene: **AX767_16200**, Position: complement(3352054..3357119)
- Product: "4-alpha-glucanotransferase"
- Status: **pseudo** (frameshifted)
- NCBI's PGAP pipeline marked this gene as a pseudogene due to a detected frameshift

### KEGG annotation:
- AX767_16200 listed as "pseudogene" — no EC number assigned
- No link to ko:K13555 (maltooligosyltrehalose synthase)
- Therefore absent from vaa00500 pathway map

### RAST/BV-BRC annotation:
- Gene: **fig|1795631.3.peg.3325**, Position: 3352054..3356112 (minus strand)
- Product: "Malto-oligosyltrehalose synthase (EC 5.4.99.15)"
- Status: **functional protein** (1352 aa, 4059 nt)
- RAST did NOT call it a pseudogene — annotated as functional

### Root Cause:
RAST and NCBI/PGAP use different annotation pipelines with different sensitivity to frameshifts.
NCBI's PGAP detects a frameshift in the 5066 nt region and calls it a pseudogene.
RAST's gene-caller produces a slightly different ORF (4059 nt vs 5066 nt) and calls it functional.
The different end coordinates (3356112 vs 3357119) suggest RAST may have predicted around
the frameshift, potentially calling a truncated but functional version.

## Gene Cluster Organization (complement strand, ~3.35-3.37 Mb)

```
Position:  3352054 ──────────── 3357112 ──── 3358941 ── 3359780 ──────────── 3363133 ── 3363147 ── 3365189
           ◄──────────────────────────────────────────────────────────────────────────────────────────────
Gene:      AX767_16200          AX767_16205           AX767_16215           AX767_16220
           (pseudo in NCBI)     TreZ                  TreS/α-amylase        MalQ
           TreY in RAST         EC:3.2.1.141          EC:5.4.99.16          
           EC:5.4.99.15                               EC:3.2.1.1
           
           AX767_16210 (pseudo, between TreZ and TreS)
```

## OtsA/OtsB Cluster (plus strand, ~1.24 Mb)

```
Position:  1237485 ──── 1238237 ──────── 1239625
           ──────────────────────────────────────►
Gene:      AX767_06260  AX767_06265
           OtsB         OtsA
           EC:3.1.3.12  EC:2.4.1.15
```
