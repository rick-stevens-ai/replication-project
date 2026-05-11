# Subsystem Comparison: Replication of RAST Iron Acquisition Analysis

## Paper Claim
RAST annotation of 4 S. maltophilia genomes revealed **2 putative iron acquisition subsystems**:
1. Iron siderophore sensor and receptor system
2. Heme, hemin uptake and utilization systems / Hemin transport system

Additional subsystems found in some strains:
- Encapsulating protein DyP-type peroxidase and ferritin-like protein oligomers (K279a only)
- Oxidative stress (FUR - all strains)

## BV-BRC Replication Results

### Iron Acquisition Subsystems (class: "Iron acquisition and metabolism")

| Subsystem | K279a | R551-3 | D457 | JV3 |
|-----------|-------|--------|------|-----|
| Iron siderophore sensor & receptor system | ✓ (8 genes) | ✓ (8 genes) | ✓ (5 genes) | ✓ (8 genes) |
| Heme, hemin uptake and utilization systems in GramPositives | ✓ (3 genes) | ✓ (3 genes) | ✓ (3 genes) | ✓ (3 genes) |

### Verdict: **VERIFIED**
- Both subsystems present in all 4 strains, matching paper claim
- Paper says "2 putative subsystems" → BV-BRC confirms exactly 2 subsystems in the "Iron acquisition and metabolism" class

### Roles within Iron siderophore sensor & receptor system
All strains contain:
- Iron siderophore sensor protein (multiple copies)
- Iron siderophore receptor protein (multiple copies)
- FIG006045: Sigma factor, ECF subfamily

### Roles within Heme, hemin uptake and utilization systems in GramPositives
All strains contain:
- Inner membrane protein YbaN (2 copies each)
- Heme oxygenase HemO, associated with heme uptake (1 copy each)

### DyP-type peroxidase subsystem
Paper claims: Only detected in K279a.
BV-BRC result: No formal "Encapsulating protein DyP-type peroxidase" subsystem assignment in any genome.
However, the DyP gene itself (Predicted dye-decolorizing peroxidase) is annotated in ALL 4 strains (PLfam PLF_40323_00040048).
**Verdict**: PARTIALLY CONTRADICTED — the gene is present in all strains, not just K279a. The subsystem category may have changed between RAST versions.

### FUR / Oxidative stress
Paper claims: FUR present across all strains.
BV-BRC result: Ferric uptake regulation protein FUR annotated in all 4 strains.
**Verdict**: VERIFIED
