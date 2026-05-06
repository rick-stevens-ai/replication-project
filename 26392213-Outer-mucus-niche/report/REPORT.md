# Replication Report: PMID 26392213

## Paper
**"The outer mucus layer hosts a distinct intestinal microbial niche"**  
Li H, Limenitakis JP, Fuhrer T, Geuking MB, Lawson MA, Wyss M, Brugiroux S, Keller I, Macpherson JA, Rupp S, Stolp B, Stein JV, Stecher B, Sauer U, McCoy KD, Macpherson AJ.  
*Nature Communications* 6, 8292 (2015).  
DOI: [10.1038/ncomms9292](https://doi.org/10.1038/ncomms9292) | PMID: 26392213 | PMC: PMC4595636

---

## Claim Under Test

The paper claims that the **outer mucus layer** of the mouse intestine hosts a **distinct microbial community** that differs from the **luminal contents**. The inner mucus layer is described as essentially sterile. This is demonstrated via:

1. **16S rRNA amplicon sequencing** (V5-V6 region, Ion Torrent PGM) of outer mucus vs luminal content samples from colon, cecum, and ileum of SPF (specific pathogen-free) mice and sDMDMm2 (stable defined moderately diverse microbiota from mouse) gnotobiotic mice.
2. **PCoA ordination** (weighted UniFrac) showing spatial separation of mucus and content communities.
3. **Statistical testing** (Adonis/PERMANOVA) showing significant community differences.

The core claim (Figure 1 of the paper) is that outer mucus samples cluster separately from luminal content samples in ordination space.

---

## Data Sources

| Source | Accession | Description |
|--------|-----------|-------------|
| Figshare | [doi:10.6084/m9.figshare.1499145](https://doi.org/10.6084/m9.figshare.1499145) | 16S rRNA amplicon data (3 FASTQ + 3 mapping files) |
| SRA | PRJEB8805 | Whole genome sequences of 12 sDMDMm2 isolates (NOT 16S) |

**Key finding during replication**: The deposited 16S data is on **Figshare**, not SRA/ENA. The SRA-linked data contains only whole-genome isolate sequences, which is easily confused with the 16S community data.

### Data Integrity

All three FASTQ files verified by MD5 checksum against Figshare metadata:

| File | Size | MD5 | Status |
|------|------|-----|--------|
| SPF_chip_1.fastq.gz | 469 MB | 9585ac3076392c4c9091e935bef736fa | ✓ |
| SPF_chip_2.fastq.gz | 256 MB | a8a5695d28c0d736cca664cafa1eb03e | ✓ |
| sDMDMm2.fastq.gz | 421 MB | 6b4553a29135153dd87efa931bfedbbb | ✓ |

---

## Methods: Paper vs Replication

| Step | Paper | Replication | Impact |
|------|-------|-------------|--------|
| Demultiplexing | QIIME 1.8.0 | Custom Python (exact barcode match) | Equivalent |
| OTU clustering | UCLUST 97% similarity | Truncation-based clustering (200bp) | **Lower resolution** — approximation of 97% OTUs |
| Reference database | Greengenes 13_8 | None (no taxonomy assignment) | No taxonomic resolution |
| Distance metric | Weighted UniFrac | Bray-Curtis, Jaccard | **Different** — weighted UniFrac requires phylogenetic tree |
| Ordination | PCoA | PCoA (scikit-bio) | Equivalent |
| Statistical test | Adonis (vegan R package) | PERMANOVA (scikit-bio) | Equivalent (same underlying algorithm) |
| Normalization | Not specified | Raw counts | May differ |

### Key Methodological Differences

1. **Distance metric**: The paper used weighted UniFrac (requires phylogenetic tree + Greengenes taxonomy), while we used Bray-Curtis (abundance-based) and Jaccard (presence/absence). This is the most significant difference — UniFrac can highlight phylogenetically meaningful differences that Bray-Curtis misses.

2. **OTU clustering**: Our truncation-based approach generates many more "OTUs" (121K vs likely ~5-10K with proper 97% clustering), inflating richness metrics but the relative abundance patterns should be similar.

3. **No taxonomy**: Without Greengenes assignment, we cannot assess which specific taxa differ between compartments.

---

## Results

### Dataset Structure

**SPF Dataset (Figure 1):**
- 6 SPF mice (G1-G6), each with:
  - 5 colon sections (Mucus + Content per section)
  - 3 cecum sections (Mucus + Content per section)
  - 1 ileum section (Mucus + Content)
- 2 Ion Torrent chips (chip_1 → mice G1-G3, chip_2 → mice G4-G6)
- Total: 101 samples passing QC (≥500 reads), 3.78M assigned reads

**sDMDMm2 Dataset (Supplementary Figure 5):**
- Multiple gnotobiotic mice, similar dissection scheme
- 60 samples, 2.77M assigned reads
- Note: Unbalanced design — 40 mucus vs 20 content samples

### Demultiplexing Rates

| Chip | Total Reads | Assigned | Rate |
|------|-------------|----------|------|
| SPF_chip_1 | 3,140,246 | 2,558,819 | 81.5% |
| SPF_chip_2 | 2,695,499 | 1,219,362 | 45.2% |
| sDMDMm2 | 3,044,043 | 2,771,159 | 91.0% |

The lower rate for chip_2 (45%) suggests sequencing quality issues or adapter contamination on that chip.

### Alpha Diversity

| Dataset | Compartment | n | Shannon (mean ± SD) | Observed OTUs (mean ± SD) |
|---------|-------------|---|---------------------|--------------------------|
| SPF | Outer Mucus | 49 | 6.50 ± 0.60 | 5,430 ± 5,744 |
| SPF | Luminal Content | 52 | 6.49 ± 0.83 | 6,506 ± 6,472 |
| sDMDMm2 | Outer Mucus | 40 | 3.51 ± 0.44 | 2,791 ± 852 |
| sDMDMm2 | Luminal Content | 20 | 3.38 ± 0.27 | 3,281 ± 817 |

**Shannon diversity** is virtually identical between mucus and content in SPF mice (6.50 vs 6.49). In the gnotobiotic sDMDMm2, mucus is slightly higher (3.51 vs 3.38), but variance is large. **Observed OTU richness** trends higher in luminal content in both datasets, consistent with the lumen receiving shed microbiota from across the gut.

Alpha diversity by **gut location** shows the expected pattern: Ileum has lower diversity (Shannon 4.99 SPF, 3.99 sDMDMm2) than Cecum (7.01, 3.52) and Colon (6.47, 3.37).

### Beta Diversity — PERMANOVA

#### Overall (Outer Mucus vs Luminal Content)

| Dataset | Metric | F-statistic | p-value | R² | Significant? |
|---------|--------|-------------|---------|-----|-------------|
| SPF | Bray-Curtis | 3.032 | **0.001** | 3.0% | ✓ |
| SPF | Jaccard | 1.372 | **0.008** | — | ✓ |
| sDMDMm2 | Bray-Curtis | 4.213 | **0.003** | 6.8% | ✓ |
| sDMDMm2 | Jaccard | 1.417 | **0.002** | — | ✓ |

#### Location-specific PERMANOVA (Bray-Curtis)

| Dataset | Location | F | p | R² | Significant? |
|---------|----------|---|---|-----|-------------|
| SPF | Colon | 2.199 | **0.015** | 4.0% | ✓ |
| SPF | Cecum | 3.014 | **0.010** | 8.4% | ✓ |
| SPF | Ileum | 2.117 | **0.025** | 19.0% | ✓ |
| sDMDMm2 | Colon | 4.934 | **0.002** | 12.7% | ✓ |
| sDMDMm2 | Cecum | 2.310 | 0.078 | 12.0% | ✗ |
| sDMDMm2 | Ileum | 0.650 | 0.819 | — | ✗ |

#### Location Effect (for comparison)

| Dataset | Factor | F | p |
|---------|--------|---|---|
| SPF | Location | 5.925 | **0.001** |
| sDMDMm2 | Location | 9.801 | **0.001** |

### ANOSIM

| Dataset | R-statistic | p-value |
|---------|-------------|---------|
| SPF | 0.063 | **0.004** |
| sDMDMm2 | 0.049 | 0.196 |

ANOSIM R values near 0 indicate nearly complete overlap between groups. The SPF R=0.063 is statistically significant but reflects minimal biological separation. The sDMDMm2 R=0.049 is not significant.

---

## Comparison with Paper's Figure 1

### What the Paper Shows
Figure 1b of the paper shows a weighted UniFrac PCoA where mucus and content samples form **two somewhat overlapping but distinguishable clusters**, with the primary separation along PC1. The paper reports Adonis p < 0.05 for the compartment effect.

### What We Found
Our Bray-Curtis PCoA shows:

1. **SPF**: A horseshoe/arch pattern with mucus and content samples **extensively overlapping**. PERMANOVA is significant (p=0.001) but explains only **3.0% of variance (R²)**. The strongest driver of community variation is **gut location** (ileum vs cecum vs colon), not compartment (mucus vs content).

2. **sDMDMm2**: Better numerical separation (R²=6.8%) but still substantial overlap in ordination space. The **colon** shows the strongest mucus-content distinction (R²=12.7%), while cecum and ileum do not show significant separation.

### Qualitative Agreement
- ✓ PERMANOVA confirms a **statistically significant** compartment effect in both datasets
- ✓ The effect is consistent across distance metrics (Bray-Curtis, Jaccard)
- ✓ The colon shows the most robust mucus-content difference
- ✓ Gut location (ileum vs cecum vs colon) is a stronger driver than compartment

### Quantitative Concerns
- ✗ Effect sizes are **very small** (R² = 3-7% overall)
- ✗ ANOSIM R values are near zero (0.05-0.06), indicating minimal separation
- ✗ Visual inspection of PCoA shows **extensive overlap**, not distinct clustering
- ✗ With 101 samples (SPF) and 60 samples (sDMDMm2), even tiny effects become statistically significant
- ✗ The pseudoreplication structure (multiple sections per mouse per organ) inflates sample sizes and may bias PERMANOVA
- △ We used Bray-Curtis rather than weighted UniFrac, which may underestimate phylogenetically-structured differences

---

## Scoring

### Claim: "The outer mucus layer hosts a distinct intestinal microbial niche"

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Data availability** | 8/10 | Data found on Figshare (not SRA as implied); complete mapping files + raw reads |
| **Statistical significance** | 9/10 | PERMANOVA p < 0.01 in both datasets, across metrics |
| **Effect size** | 4/10 | R² = 3-7%; ANOSIM R ≈ 0.05; communities heavily overlap |
| **Visual separation (PCoA)** | 4/10 | No clear clustering; extensive overlap in ordination |
| **Consistency across datasets** | 7/10 | Both SPF and sDMDMm2 show significant but small effects |
| **Robustness across locations** | 5/10 | Significant for colon; weaker/non-significant for cecum and ileum |
| **Methodological match** | 5/10 | Different distance metric (Bray-Curtis vs UniFrac); no taxonomy; no proper OTU clustering |

### Overall Replication Score: **6/10 — Partially Replicated**

**The statistical significance of the compartment effect replicates**, but the word "distinct" in the title overstates what the data show. The outer mucus community is **subtly different** from the luminal contents — enough to be detected by PERMANOVA with adequate sample sizes — but the two compartments share the vast majority of their community composition. The communities are better described as **overlapping with compositional shifts** rather than as distinct niches.

### Caveats

1. **Distance metric mismatch**: Our use of Bray-Curtis rather than weighted UniFrac may underestimate the compartment effect if the key differences are between phylogenetically related taxa with different abundances (which UniFrac handles well).

2. **OTU clustering**: Our truncation-based approach is cruder than UCLUST and may fragment real biological OTUs, diluting the signal.

3. **No rarefaction**: We did not rarefy to equal sampling depth, which could introduce bias since sequencing depth varied substantially across samples.

4. **Pseudoreplication**: Multiple sections from the same mouse are treated as independent samples, inflating degrees of freedom. A mixed-effects model with mouse as a random effect would be more appropriate.

5. **No taxonomy**: Without taxonomic assignment, we cannot evaluate whether specific taxa (e.g., *Bacteroides*, *Lachnospiraceae*) are enriched in mucus as the paper claims.

---

## Files Generated

```
analysis/
├── figures/
│   ├── SPF_PCoA_v2.png          # Main PCoA (Bray-Curtis), PC1-2 and PC1-3
│   ├── SPF_alpha_v2.png         # Alpha diversity by location and compartment
│   ├── SPF_heatmap_v2.png       # Top 30 OTUs heatmap
│   ├── sDMDMm2_PCoA_v2.png     # PCoA for gnotobiotic dataset
│   ├── sDMDMm2_alpha_v2.png    # Alpha diversity
│   └── sDMDMm2_heatmap_v2.png  # Top 30 OTUs heatmap
├── SPF_metadata_v2.csv
├── SPF_alpha_diversity_v2.csv
├── SPF_otu_table.csv            # Full OTU table (105 MB)
├── sDMDMm2_metadata_v2.csv
├── sDMDMm2_alpha_diversity_v2.csv
├── sDMDMm2_otu_table.csv        # Full OTU table (16 MB)
├── replication_summary_v2.json
scripts/
├── replicate_analysis.py        # v1 (had chip-mapping bug)
└── replicate_analysis_v2.py     # v2 (corrected)
data/raw/
├── SPF_chip_1.fastq.gz          # 469 MB, Ion Torrent PGM
├── SPF_chip_2.fastq.gz          # 256 MB
├── sDMDMm2.fastq.gz             # 421 MB
├── SPF_map1.txt                 # QIIME mapping (mice G1-G3)
├── SPF_map2.txt                 # QIIME mapping (mice G4-G6)
└── sDMDMm2_map.txt              # QIIME mapping (gnotobiotic)
```

---

## Conclusion

The paper's core statistical finding — that PERMANOVA detects a significant difference between outer mucus and luminal content communities — **replicates**. However, the effect is **small** (R² ≈ 3-7%), and the characterization of the outer mucus as hosting a "distinct niche" is stronger than what the data support. The microbial communities in mucus and luminal content are **largely overlapping** with subtle compositional shifts, particularly in the colon. The strongest driver of community variation across these samples is **gut anatomical location** (ileum vs cecum vs colon), which explains substantially more variance than the mucus-content distinction.

A full replication using the original pipeline (QIIME 1.8.0, UCLUST, weighted UniFrac, Greengenes) or modern equivalents (QIIME2, DADA2, Silva) would be needed to assess whether the UniFrac metric reveals stronger compartment separation than Bray-Curtis.

---

*Report generated: 2026-05-05*  
*Analysis time: ~40 minutes (download + compute on local CPU)*  
*Environment: Python 3.10, scikit-bio 0.7.2, conda microbiome env on macOS*
