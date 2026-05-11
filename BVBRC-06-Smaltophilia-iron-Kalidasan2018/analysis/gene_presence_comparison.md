# Gene Presence Comparison: 17 Functional Targets

## Method
Used BV-BRC API to search for each of the 17 iron acquisition targets from Table 2 across all 4 genomes.
Primary method: PLfam-based ortholog detection (species-level protein families).
Secondary: keyword-based product name search and manual locus tag mapping.

## K279a Locus Tag Mapping (SMLT_RS → Smlt)
| Target | Paper Locus (RS) | BV-BRC Locus (Smlt) | BV-BRC Product |
|--------|-----------------|---------------------|----------------|
| FeSreg | SMLT_RS12950 | Smlt2716 | Sigma factor, ECF subfamily |
| FeSR | SMLT_RS18575 | Smlt3898 | Iron siderophore receptor protein |
| FeSS | SMLT_RS18580 | Smlt3899 | Iron siderophore sensor protein |
| HemO/HO | SMLT_RS18565 | Smlt3896 | Heme oxygenase HemO |
| HmuV | SMLT_RS11325 | Smlt2357 | Heme ABC transporter, ATPase component |
| Hyp1 | SMLT_RS19415 | Smlt4081 | Inner membrane protein YbaN |
| HmuU | SMLT_RS11320 | Smlt2356 | Heme ABC transporter, permease protein |
| HmuT | SMLT_RS11315 | Smlt2355 | Heme ABC transporter, cell surface receptor |
| Rp2 | SMLT_RS18050 | Smlt3789 | Outer membrane receptor proteins, Fe transport |
| Hup | SMLT_RS03780 | Smlt0794 | Hemin uptake protein HemP/HmuP |
| ETFb | SMLT_RS03080 | Smlt0646 | Electron transfer flavoprotein, beta subunit |
| TonB | SMLT_RS21345 | Smlt4506 | TonB-dependent receptor |
| ExbB | SMLT_RS07890 | Smlt1638 | Ferric siderophore transport, ExbB |
| Htp | SMLT_RS03790 | Smlt0796 | Hypothetical protein (hemin transport) |
| FCR | SMLT_RS03785 | Smlt0795 | Outer membrane hemin receptor (huvA) |
| DyP | SMLT_RS00875 | Smlt0187 | Dye-decolorizing peroxidase (DyP) |
| Fur | SMLT_RS09600 | Smlt1986 | Ferric uptake regulation protein FUR |

## Comparative Presence (via PLfam ortholog search)

| Target | K279a | R551-3 | D457 | JV3 | Paper Claim |
|--------|-------|--------|------|-----|-------------|
| FeSreg | ✓ | ✓ | ✓ | ✓ | Present in all |
| FeSR | ✓ | ✓ | ✓ | ✓ | Present in all |
| FeSS | ✓ | ✓ | ✓ | ✓ | Present in all |
| HemO/HO | ✓ | ✓ | ✓ | ✓ | Present in all |
| HmuV | ✓ | ✓ | ✓ | ✓ | Present in all |
| Hyp1 | ✓ | ✓ | ✓ | ✓ | Present in all |
| HmuU | ✓ | ✓ | ✓ | ✓ | Present in all |
| HmuT | ✓ | ✓* | ✓ | ✓* | Present in all |
| Rp2 | ✓ | ✓ | ✓ | ✓ | Present in all |
| Hup | ✓ | ✓ | ✓ | ✓ | Present in all |
| ETFb | ✓ | ✓ | ✓ | ✓ | Present in all |
| TonB | ✓ | ✓ | ✓ | ✓ | Present in all |
| ExbB | ✓ | ✓ | ✓ | ✓ | Present in all |
| Htp | ✓ | ✓ | ✓ | ✓ | Present in all |
| FCR | ✓ | ✓ | ✓ | ✓ | Present in all |
| DyP | ✓ | ✓ | ✓ | ✓ | Only K279a (subsystem) |
| Fur | ✓ | ✓ | ✓ | ✓ | Present in all |

*HmuT: PLfam not found in R551-3/JV3, but keyword search for "Heme ABC transporter, cell surface" confirms presence.

## Summary
- 17/17 targets confirmed present in K279a ✓
- 17/17 targets confirmed present in R551-3 ✓  
- 17/17 targets confirmed present in D457 ✓
- 17/17 targets confirmed present in JV3 ✓
- Paper's identification of these 17 functional targets is **VERIFIED**
- DyP subsystem assignment discrepancy: paper says subsystem only in K279a, but gene present in all 4
