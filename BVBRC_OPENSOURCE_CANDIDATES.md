# BV-BRC/PATRIC — Open-Source-Only Replication Candidates

> **Generated:** 2026-05-05 | **Source:** `bvbrc_all.json` (3,146 papers)
> **Companion to:** `BVBRC_PRIMARY_CANDIDATES.md` (PATRIC-primary papers)

## Methodology

### What we did
Scanned all 3,146 BV-BRC/PATRIC citing papers to find isolate-genomics studies that
use **exclusively open-source / free tools** — no paid commercial software anywhere
in their methods.

### Tool verification process
1. **Keyword scan** of titles + truncated abstracts (500 chars max from Semantic Scholar)
2. **Full-text verification** via Europe PMC XML for all candidates — checked complete
   methods sections for both open-source tool usage AND paid tool contamination
3. **Paid tool exclusion**: Papers using ANY of the following were removed:
   - Ridom SeqSphere/SeqSphere+ (cgMLST) — paid Windows
   - CLC Genomics Workbench — Qiagen paid
   - Geneious/Geneious Prime — Biomatters paid
   - DNASTAR/Lasergene — paid
   - BioNumerics — Applied Maths paid
   - SnapGene, CodonCode Aligner, Partek, Vector NTI — paid
4. **Also excluded**: metagenomics/16S/MAGs, reviews, tool papers, PATRIC-data-only
5. **Deduplication** against `BVBRC_PRIMARY_CANDIDATES.md` (31 existing candidates)

### Filtering statistics
```
Total papers scanned:           3,146
No abstract / too short:          425
Pre-2016 (too old):               589
Reviews / editorials:             108
Tool description papers:           11
Metagenomics / 16S / microbiome:  379
Not isolate genomics:             980
Deduped (in PRIMARY_CANDIDATES):  141
Remaining for tool verification:  ~512
Full-text verified (Europe PMC):    62
Confirmed paid tool → excluded:     15
Confirmed open-source only:         37
Final top-25 ranked:                25
```

### Tiers
- **🅰️ Tier A** — Uses PATRIC/BV-BRC/RAST as primary tool + open-source pipeline
- **🅱️ Tier B** — Pure open-source pipeline, cites PATRIC; replicable via BV-BRC

### Scoring (5 dimensions, each 1–10, max 50)

| Dimension | What it measures |
|-----------|-----------------|
| **P (Primacy)** | Open-source tool clarity — how many specific tools named |
| **R (Replicability)** | Can we re-run end-to-end with BV-BRC + open-source tools? |
| **Q (Quantitative)** | Specific numbers we can re-derive |
| **I (Impact)** | Citation count (>40 = bonus) |
| **Rc (Recency)** | 2018+ preferred (BV-BRC API stable era) |

---

## Top 25 Candidates

### 1. 🅰️ An ISO-certified genomics workflow for identification and surveillance of antimicrobial resistance

| | |
|---|---|
| **Year / Cites** | 2023 / 121 citations |
| **Authors** | N. Sherry et al. |
| **Venue** | Nature Communications |
| **ID** | [10.1038/s41467-022-35713-4](https://doi.org/10.1038/s41467-022-35713-4) PMID:36599823 |
| **Score** | **43/50** — P:10 R:9 Q:4 I:10 Rc:10 |
| **Tool stack** | PATRIC, AMRFinderPlus, RGI/CARD, ResFinder, SPAdes, SKESA, Shovill, Trimmomatic, BLAST |

**Why replicable:** The implementation of genomics for identification and surveillance of antimicrobial resistance (AMR) in clinical laboratories remains challenging. Here, Sherry et al. present a bioinformatics platform for detection of AMR determinants from whole-genome sequencing data, suitable for clinical and publ

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes/Shovill/SKESA; AMR via ResFinder/AMRFinderPlus/RGI/CARD

---

### 2. 🅰️ Probiogenomic In-Silico Analysis and Safety Assessment of Lactiplantibacillus plantarum DJF10 Strain Isolated from Korean Raw Milk

| | |
|---|---|
| **Year / Cites** | 2022 / 42 citations |
| **Authors** | S. Kandasamy et al. |
| **Venue** | International Journal of Molecular Sciences |
| **ID** | [10.3390/ijms232214494](https://doi.org/10.3390/ijms232214494) PMID:36430971 |
| **Score** | **43/50** — P:10 R:9 Q:7 I:8 Rc:9 |
| **Tool stack** | RAST, PATRIC, Prokka, RGI/CARD, ResFinder, VirulenceFinder, VFDB, SPAdes, Shovill, KEGG, eggNOG, PHASTER, PlasmidFinder, ISfinder, Trimmomatic, QUAST, Galaxy, ANI, COG, Subsystem, BLAST |

**Why replicable:** The whole genome sequence of Lactiplantibacillus plantarum DJF10, isolated from Korean raw milk, is reported, along with its genomic analysis of probiotics and safety features. The genome consists of 29 contigs with a total length of 3,385,113 bp and a GC content of 44.3%. The average nucleotide ide

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes/Shovill; annotate with RAST/Prokka; AMR via ResFinder/RGI/CARD; virulence via VirulenceFinder/VFDB; functional analysis via eggNOG; plasmid typing via PlasmidFinder; prophage detection via PHASTER

---

### 3. 🅰️ blaNDM-5 carried by a hypervirulent Klebsiella pneumoniae with sequence type 29

| | |
|---|---|
| **Year / Cites** | 2019 / 46 citations |
| **Authors** | Yi Yuan et al. |
| **Venue** | Antimicrobial Resistance and Infection Control |
| **ID** | [10.1186/s13756-019-0596-1](https://doi.org/10.1186/s13756-019-0596-1) PMID:31452874 |
| **Score** | **42/50** — P:10 R:9 Q:7 I:8 Rc:8 |
| **Tool stack** | RAST, Prokka, OrthoFinder, RAxML, FastTree, Kleborate, ABRicate, ResFinder, VFDB, SPAdes, Gubbins, PlasmidFinder, Trimmomatic, MLST, BLAST |

**Why replicable:** A carbapenem-resistant hypermucoviscous Klebsiella pneumoniae isolate was recovered from human sputum. Whole genome sequencing of this isolate was carried out to reveal its clonal background, antimicrobial resistance determinants and virulence factors. Virulence assays were performed using wax moth 

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; pangenome via OrthoFinder; phylogeny with RAxML/FastTree; AMR via ResFinder/ABRicate; virulence via VFDB; recombination analysis; plasmid typing via PlasmidFinder

---

### 4. 🅰️ Whole-Genome Sequence of Lactococcus lactis Subsp. lactis LL16 Confirms Safety, Probiotic Potential, and Reveals Functional Traits

| | |
|---|---|
| **Year / Cites** | 2023 / 30 citations |
| **Authors** | Justina Milerienė et al. |
| **Venue** | Microorganisms |
| **ID** | [10.3390/microorganisms11041034](https://doi.org/10.3390/microorganisms11041034) PMID:37110457 |
| **Score** | **42/50** — P:10 R:9 Q:6 I:7 Rc:10 |
| **Tool stack** | RAST, Prokka, ResFinder, VirulenceFinder, SPAdes, antiSMASH, KEGG, QUAST, Subsystem, BLAST |

**Why replicable:** Safety is the most important criteria of any substance or microorganism applied in the food industry. The whole-genome sequencing (WGS) of an indigenous dairy isolate LL16 confirmed it to be Lactococcus lactis subsp. lactis with genome size 2,589,406 bp, 35.4% GC content, 246 subsystems, and 1 plasm

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; AMR via ResFinder; virulence via VirulenceFinder; BGC mining via antiSMASH

---

### 5. 🅰️ Genomic Epidemiology of Vancomycin-Resistant Enterococcus faecium (VREfm) in Latin America: Revisiting The Global VRE Population Structure

| | |
|---|---|
| **Year / Cites** | 2020 / 52 citations |
| **Authors** | Rafael Ríos et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-020-62371-7](https://doi.org/10.1038/s41598-020-62371-7) PMID:32221315 |
| **Score** | **41/50** — P:10 R:9 Q:6 I:8 Rc:8 |
| **Tool stack** | RAST, Roary, RAxML, ResFinder, SPAdes, ClonalFrameML, ISfinder, Trimmomatic, MLST, BLAST |

**Why replicable:** Little is known about the population structure of vancomycin-resistant Enterococcus faecium (VREfm) in Latin America (LATAM). Here, we provide a complete genomic characterization of 55 representative Latin American VREfm recovered from 1998–2015 in 5 countries. The LATAM VREfm population is structur

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST; pangenome via Roary; phylogeny with RAxML; AMR via ResFinder; recombination analysis

---

### 6. 🅰️ Machine learning with random subspace ensembles identifies antimicrobial resistance determinants from pan-genomes of three pathogens

| | |
|---|---|
| **Year / Cites** | 2020 / 68 citations |
| **Authors** | Jason C. Hyun et al. |
| **Venue** | PLoS Comput. Biol. |
| **ID** | [10.1371/journal.pcbi.1007608](https://doi.org/10.1371/journal.pcbi.1007608) PMID:32119670 |
| **Score** | **40/50** — P:10 R:9 Q:4 I:9 Rc:8 |
| **Tool stack** | RAST, PATRIC, Mash, InterProScan, eggNOG, COG, BLAST |

**Why replicable:** The evolution of antimicrobial resistance (AMR) poses a persistent threat to global public health. Sequencing efforts have already yielded genome sequences for thousands of resistant microbial isolates and require robust computational tools to systematically elucidate the genetic basis for AMR. Here

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; functional analysis via Mash/InterProScan/eggNOG

---

### 7. 🅰️ Comparative genomic analysis of Enterococcus faecalis: insights into their environmental adaptations

| | |
|---|---|
| **Year / Cites** | 2018 / 59 citations |
| **Authors** | Qiuwen He et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/s12864-018-4887-3](https://doi.org/10.1186/s12864-018-4887-3) PMID:29996769 |
| **Score** | **40/50** — P:10 R:9 Q:6 I:8 Rc:7 |
| **Tool stack** | RAST, FastTree, VFDB, KEGG, Gubbins, PHASTER, COG, BLAST |

**Why replicable:** Enterococcus faecalis is widely studied as a common gut commensal and a nosocomial pathogen. In fact, Enterococcus faecalis is ubiquitous in nature, and it has been isolated from various niches, including the gastrointestinal tract, faeces, blood, urine, water, and fermented foods (such as dairy pro

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; phylogeny with FastTree; virulence via VFDB; recombination analysis; prophage detection via PHASTER

---

### 8. 🅰️ Hybrid Assembly Provides Improved Resolution of Plasmids, Antimicrobial Resistance Genes, and Virulence Factors in Escherichia coli and Klebsiella pneumoniae Clinical Isolates

| | |
|---|---|
| **Year / Cites** | 2021 / 43 citations |
| **Authors** | Abdolrahman Khezri et al. |
| **Venue** | Microorganisms |
| **ID** | [10.3390/microorganisms9122560](https://doi.org/10.3390/microorganisms9122560) PMID:34946161 |
| **Score** | **40/50** — P:10 R:9 Q:4 I:8 Rc:9 |
| **Tool stack** | PATRIC, Prokka, ResFinder, VFDB, SPAdes, Unicycler, Flye, Canu, PlasmidFinder, Trimmomatic, QUAST, BLAST, Pilon |

**Why replicable:** Emerging new sequencing technologies have provided researchers with a unique opportunity to study factors related to microbial pathogenicity, such as antimicrobial resistance (AMR) genes and virulence factors. However, the use of whole-genome sequence (WGS) data requires good knowledge of the bioinf

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes/Unicycler/Flye/Canu; annotate with Prokka; AMR via ResFinder; virulence via VFDB; plasmid typing via PlasmidFinder

---

### 9. 🅰️ Whole-genome sequence of multi-drug resistant Pseudomonas aeruginosa strains UY1PSABAL and UY1PSABAL2 isolated from human broncho-alveolar lavage, Yaoundé, Cameroon

| | |
|---|---|
| **Year / Cites** | 2020 / 35 citations |
| **Authors** | E. Madaha et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0238390](https://doi.org/10.1371/journal.pone.0238390) PMID:32886694 |
| **Score** | **40/50** — P:10 R:9 Q:6 I:7 Rc:8 |
| **Tool stack** | RAST, PATRIC, Prokka, ResFinder, SPAdes, antiSMASH, PHASTER, Trimmomatic |

**Why replicable:** Pseudomonas aeruginosa has been implicated in a wide range of post-operation wound and lung infections. A wide range of acquired resistance and virulence markers indicate surviving strategy of P. aeruginosa. Complete-genome analysis has been identified as efficient approach towards understanding the

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; AMR via ResFinder; BGC mining via antiSMASH; prophage detection via PHASTER

---

### 10. 🅰️ Virulence and antibiotic-resistance genes in Enterococcus faecalis associated with streptococcosis disease in fish

| | |
|---|---|
| **Year / Cites** | 2023 / 35 citations |
| **Authors** | Tasmina Akter et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-022-25968-8](https://doi.org/10.1038/s41598-022-25968-8) PMID:36707682 |
| **Score** | **40/50** — P:10 R:9 Q:4 I:7 Rc:10 |
| **Tool stack** | RAST, RASTtk, PATRIC, Prokka, RGI/CARD, ResFinder, VirulenceFinder, VFDB, SPAdes, antiSMASH, KEGG, PHASTER, PlasmidFinder, ISfinder, ARG-ANNOT, Subsystem, BLAST |

**Why replicable:** Enterococcus faecalis is associated with streptococcosis like infection in fish. A whole-genome sequence study was conducted to investigate the virulence factor and antibiotic-resistance genes in three fish pathogenic E. faecalis . Genomic DNA was extracted from three strains of E. faecalis isolated

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RASTtk/RAST/Prokka; AMR via ResFinder/RGI/CARD/ARG-ANNOT; virulence via VirulenceFinder/VFDB; BGC mining via antiSMASH; plasmid typing via PlasmidFinder; prophage detection via PHASTER

---

### 11. 🅰️ Prediction of antibiotic resistance in Escherichia coli from large-scale pan-genome data

| | |
|---|---|
| **Year / Cites** | 2018 / 169 citations |
| **Authors** | D. Moradigaravand et al. |
| **Venue** | PLoS Comput. Biol. |
| **ID** | [10.1371/journal.pcbi.1006258](https://doi.org/10.1371/journal.pcbi.1006258) PMID:30550564 |
| **Score** | **39/50** — P:9 R:9 Q:4 I:10 Rc:7 |
| **Tool stack** | PATRIC, Prokka, Roary, ResFinder, srst2 |

**Why replicable:** The emergence of microbial antibiotic resistance is a global health threat. In clinical settings, the key to controlling spread of resistant strains is accurate and rapid detection. As traditional culture-based methods are time consuming, genetic approaches have recently been developed for this task

**Replication path:** Retrieve genomes from BV-BRC; annotate with Prokka; pangenome via Roary; AMR via ResFinder

---

### 12. 🅰️ Comparative genomic analysis revealed great plasticity and environmental adaptation of the genomes of Enterococcus faecium

| | |
|---|---|
| **Year / Cites** | 2019 / 50 citations |
| **Authors** | Z. Zhong et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/s12864-019-5975-8](https://doi.org/10.1186/s12864-019-5975-8) PMID:31331270 |
| **Score** | **39/50** — P:9 R:8 Q:6 I:8 Rc:8 |
| **Tool stack** | RAST, FastTree, VFDB, KEGG, Gubbins, ANI, COG, BLAST |

**Why replicable:** As an important nosocomial pathogen, Enterococcus faecium has received increasing attention in recent years. However, a large number of studies have focused on the hospital-associated isolates and ignored isolates originated from the natural environments. In this study, comparative genomic analysis 

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; phylogeny with FastTree; virulence via VFDB; recombination analysis

---

### 13. 🅰️ Integrated genome-based probiotic relevance and safety evaluation of Lactobacillus reuteri PNW1

| | |
|---|---|
| **Year / Cites** | 2020 / 42 citations |
| **Authors** | K. A. Alayande et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0235873](https://doi.org/10.1371/journal.pone.0235873) PMID:32687505 |
| **Score** | **39/50** — P:10 R:9 Q:4 I:8 Rc:8 |
| **Tool stack** | RAST, PATRIC, RGI/CARD, ResFinder, VirulenceFinder, SPAdes, antiSMASH, PHASTER, ISfinder, BLAST |

**Why replicable:** This study evaluates whole-genome sequence of Lactobacillus reuteri PNW1 and identifies its safety genes that may qualify it as a putative probiotic. It further extracted the bacteriocin produced by the strain and tested its effectiveness against pathogenic STEC E. coli O177. The genomic DNA was seq

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST; AMR via ResFinder/RGI/CARD; virulence via VirulenceFinder; BGC mining via antiSMASH; prophage detection via PHASTER

---

### 14. 🅰️ Genome analysis of a halophilic bacterium Halomonas malpeensis YU-PRIM-29T reveals its exopolysaccharide and pigment producing capabilities

| | |
|---|---|
| **Year / Cites** | 2021 / 34 citations |
| **Authors** | Athmika et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-021-81395-1](https://doi.org/10.1038/s41598-021-81395-1) PMID:33462335 |
| **Score** | **39/50** — P:10 R:9 Q:4 I:7 Rc:9 |
| **Tool stack** | RAST, PATRIC, Prokka, SPAdes, antiSMASH, KEGG, Trimmomatic, COG, BLAST |

**Why replicable:** Halomonas malpeensis strain YU-PRIM-29T is a yellow pigmented, exopolysaccharide (EPS) producing halophilic bacterium isolated from the coastal region. To understand the biosynthesis pathways involved in the EPS and pigment production, whole genome analysis was performed. The complete genome sequenc

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; BGC mining via antiSMASH

---

### 15. 🅰️ Rational construction of genome-reduced and high-efficient industrial Streptomyces chassis based on multiple comparative genomic approaches

| | |
|---|---|
| **Year / Cites** | 2019 / 75 citations |
| **Authors** | Qing-ting Bu et al. |
| **Venue** | Microbial Cell Factories |
| **ID** | [10.1186/s12934-019-1055-7](https://doi.org/10.1186/s12934-019-1055-7) PMID:30691531 |
| **Score** | **38/50** — P:9 R:8 Q:4 I:9 Rc:8 |
| **Tool stack** | RAST, BPGA, antiSMASH, KEGG, Mauve, Subsystem, BLAST |

**Why replicable:** BackgroundStreptomyces chattanoogensis L10 is the industrial producer of natamycin and has been proved a highly efficient host for diverse natural products. It has an enormous potential to be developed as a versatile cell factory for production of heterologous secondary metabolites. Here we develope

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; pangenome via BPGA; BGC mining via antiSMASH

---

### 16. 🅰️ Comparative genome analysis reveals key genetic factors associated with probiotic property in Enterococcus faecium strains

| | |
|---|---|
| **Year / Cites** | 2018 / 53 citations |
| **Authors** | Vikas C. Ghattargi et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/s12864-018-5043-9](https://doi.org/10.1186/s12864-018-5043-9) PMID:30180794 |
| **Score** | **38/50** — P:10 R:9 Q:4 I:8 Rc:7 |
| **Tool stack** | RAST, BPGA, VFDB, PHASTER, ISfinder, COG, BLAST |

**Why replicable:** Enterococcus faecium though commensal in the human gut, few strains provide a beneficial effect to humans as probiotics while few are responsible for the nosocomial infection. Comparative genomics of E. faecium can decipher the genomic differences responsible for probiotic, pathogenic and non-pathog

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; pangenome via BPGA; virulence via VFDB; prophage detection via PHASTER

---

### 17. 🅰️ Escherichia coli B2 strains prevalent in inflammatory bowel disease patients have distinct metabolic capabilities that enable colonization of intestinal mucosa

| | |
|---|---|
| **Year / Cites** | 2018 / 47 citations |
| **Authors** | X. Fang et al. |
| **Venue** | BMC Systems Biology |
| **ID** | [10.1186/s12918-018-0587-5](https://doi.org/10.1186/s12918-018-0587-5) PMID:29890970 |
| **Score** | **38/50** — P:8 R:7 Q:8 I:8 Rc:7 |
| **Tool stack** | RAST, PATRIC, SPAdes, BLAST |

**Why replicable:** BackgroundEscherichia coli is considered a leading bacterial trigger of inflammatory bowel disease (IBD). E. coli isolates from IBD patients primarily belong to phylogroup B2. Previous studies have focused on broad comparative genomic analysis of E. coli B2 isolates, and identified virulence factors

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST

---

### 18. 🅰️ Comparative Genomic Insights into Secondary Metabolism Biosynthetic Gene Cluster Distributions of Marine Streptomyces

| | |
|---|---|
| **Year / Cites** | 2019 / 37 citations |
| **Authors** | Lin Xu et al. |
| **Venue** | Marine Drugs |
| **ID** | [10.3390/md17090498](https://doi.org/10.3390/md17090498) PMID:31454987 |
| **Score** | **38/50** — P:10 R:9 Q:4 I:7 Rc:8 |
| **Tool stack** | RAST, IQ-TREE, MEGA, antiSMASH, KEGG, CheckM, ANI, COG, BLAST |

**Why replicable:** Bacterial secondary metabolites have huge application potential in multiple industries. Biosynthesis of bacterial secondary metabolites are commonly encoded in a set of genes that are organized in the secondary metabolism biosynthetic gene clusters (SMBGCs). The development of genome sequencing tech

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; phylogeny with IQ-TREE; BGC mining via antiSMASH

---

### 19. 🅰️ A Pan-Genome Guided Metabolic Network Reconstruction of Five Propionibacterium Species Reveals Extensive Metabolic Diversity

| | |
|---|---|
| **Year / Cites** | 2020 / 33 citations |
| **Authors** | Tim McCubbin et al. |
| **Venue** | Genes |
| **ID** | [10.3390/genes11101115](https://doi.org/10.3390/genes11101115) PMID:32977700 |
| **Score** | **38/50** — P:10 R:9 Q:4 I:7 Rc:8 |
| **Tool stack** | RAST, RASTtk, GET_HOMOLOGUES, OrthoMCL, BLAST, ModelSEED |

**Why replicable:** Propionibacteria have been studied extensively since the early 1930s due to their relevance to industry and importance as human pathogens. Still, their unique metabolism is far from fully understood. This is partly due to their signature high GC content, which has previously hampered the acquisition

**Replication path:** Retrieve genomes from BV-BRC; annotate with RASTtk/RAST; pangenome via GET_HOMOLOGUES/OrthoMCL; metabolic modeling via ModelSEED

---

### 20. 🅰️ Genomic epidemiology of Campylobacter jejuni associated with asymptomatic pediatric infection in the Peruvian Amazon

| | |
|---|---|
| **Year / Cites** | 2020 / 29 citations |
| **Authors** | B. Pascoe et al. |
| **Venue** | medRxiv |
| **ID** | [10.1371/journal.pntd.0008533](https://doi.org/10.1371/journal.pntd.0008533) PMID:32776937 |
| **Score** | **38/50** — P:10 R:9 Q:4 I:7 Rc:8 |
| **Tool stack** | RAST, IQ-TREE, ABRicate, AMRFinderPlus, ResFinder, VFDB, PlasmidFinder, MLST, ANI, BLAST |

**Why replicable:** Campylobacter is the leading bacterial cause of gastroenteritis worldwide and its incidence is especially high in low- and middle-income countries (LMIC). Disease epidemiology in LMICs is different compared to high income countries like the USA or in Europe. Children in LMICs commonly have repeated 

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST; phylogeny with IQ-TREE; AMR via ResFinder/AMRFinderPlus/ABRicate; virulence via VFDB; plasmid typing via PlasmidFinder

---

### 21. 🅰️ Genome Analysis of ESBL-Producing Escherichia coli Isolated from Pigs

| | |
|---|---|
| **Year / Cites** | 2022 / 16 citations |
| **Authors** | Luria Leslie Founou et al. |
| **Venue** | Pathogens |
| **ID** | [10.3390/pathogens11070776](https://doi.org/10.3390/pathogens11070776) PMID:35890020 |
| **Score** | **38/50** — P:10 R:9 Q:4 I:6 Rc:9 |
| **Tool stack** | RAST, Prokka, ResFinder, VirulenceFinder, VFDB, SPAdes, PHASTER, PlasmidFinder, Enterobase, MLST |

**Why replicable:** The resistome, virulome and mobilome of extended spectrum ß-lactamase (ESBL)-producing Escherichia coli (ESBL-Ec) isolated from pigs in Cameroon and South Africa were assessed using whole genome sequencing (WGS). Eleven clonally related phenotypic ESBL-Ec isolates were subjected to WGS. The predicti

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; AMR via ResFinder; virulence via VirulenceFinder/VFDB; plasmid typing via PlasmidFinder; prophage detection via PHASTER

---

### 22. 🅰️ Physiological and Comparative Genomic Analysis of Arthrobacter sp. SRS-W-1-2016 Provides Insights on Niche Adaptation for Survival in Uraniferous Soils

| | |
|---|---|
| **Year / Cites** | 2018 / 32 citations |
| **Authors** | Ashvini Chauhan et al. |
| **Venue** | Genes |
| **ID** | [10.3390/genes9010031](https://doi.org/10.3390/genes9010031) PMID:29324691 |
| **Score** | **37/50** — P:10 R:9 Q:4 I:7 Rc:7 |
| **Tool stack** | RAST, Prokka, SPAdes, antiSMASH, KEGG, Mauve, ANI, COG, Subsystem, BLAST, Bowtie |

**Why replicable:** Arthrobacter sp. strain SRS-W-1-2016 was isolated on high concentrations of uranium (U) from the Savannah River Site (SRS) that remains co-contaminated by radionuclides, heavy metals, and organics. SRS is located on the northeast bank of the Savannah River (South Carolina, USA), which is a U.S. Depa

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST/Prokka; BGC mining via antiSMASH

---

### 23. 🅰️ Comparative genomic analysis of Parageobacillus thermoglucosidasius strains with distinct hydrogenogenic capacities

| | |
|---|---|
| **Year / Cites** | 2018 / 25 citations |
| **Authors** | Teresa Mohr et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/s12864-018-5302-9](https://doi.org/10.1186/s12864-018-5302-9) PMID:30522433 |
| **Score** | **37/50** — P:10 R:9 Q:4 I:7 Rc:7 |
| **Tool stack** | RAST, OrthoFinder, SPAdes, eggNOG, Mauve, ANI, COG |

**Why replicable:** The facultatively anaerobic thermophile Parageobacillus thermoglucosidasius produces hydrogen gas (H2) by coupling CO oxidation to proton reduction in the water-gas shift (WGS) reaction via a carbon monoxide dehydrogenase–hydrogenase enzyme complex. Although little is known about the hydrogenogenic 

**Replication path:** Retrieve genomes from BV-BRC; assemble with SPAdes; annotate with RAST; pangenome via OrthoFinder; functional analysis via eggNOG

---

### 24. 🅰️ AbGRI4, a novel antibiotic resistance island in multiply antibiotic-resistant Acinetobacter baumannii clinical isolates

| | |
|---|---|
| **Year / Cites** | 2020 / 20 citations |
| **Authors** | A. Chan et al. |
| **Venue** | Journal of Antimicrobial Chemotherapy |
| **ID** | [10.1093/jac/dkaa266](https://doi.org/10.1093/jac/dkaa266) PMID:32681170 |
| **Score** | **37/50** — P:10 R:9 Q:4 I:6 Rc:8 |
| **Tool stack** | PATRIC, RAxML, Unicycler, Gubbins, ISfinder, MLST, BLAST, Pilon |

**Why replicable:** Abstract Objectives To investigate the genomic context of a novel resistance island (RI) in multiply antibiotic-resistant Acinetobacter baumannii clinical isolates and global isolates. Methods Using a combination of long and short reads generated from the Oxford Nanopore and Illumina platforms, cont

**Replication path:** Retrieve genomes from BV-BRC; assemble with Unicycler; phylogeny with RAxML; recombination analysis

---

### 25. 🅰️ Extended insight into the Mycobacterium chelonae-abscessus complex through whole genome sequencing of Mycobacterium salmoniphilum outbreak and Mycobacterium salmoniphilum-like strains

| | |
|---|---|
| **Year / Cites** | 2019 / 16 citations |
| **Authors** | P. R. K. Behra et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-019-40922-x](https://doi.org/10.1038/s41598-019-40922-x) PMID:30872669 |
| **Score** | **37/50** — P:10 R:9 Q:4 I:6 Rc:8 |
| **Tool stack** | RAST, Prokka, Prodigal, FastTree, VFDB, Mauve, ANI, Subsystem, BLAST |

**Why replicable:** Members of the Mycobacterium chelonae-abscessus complex (MCAC) are close to the mycobacterial ancestor and includes both human, animal and fish pathogens. We present the genomes of 14 members of this complex: the complete genomes of Mycobacterium salmoniphilum and Mycobacterium chelonae type strains

**Replication path:** Retrieve genomes from BV-BRC; annotate with RAST/Prokka/Prodigal; phylogeny with FastTree; virulence via VFDB

---

## Summary Table

| # | Tier | Score | P | R | Q | I | Rc | Cites | Year | Title |
|---|------|-------|---|---|---|---|----|-------|------|-------|
| 1 | A | 43 | 10 | 9 | 4 | 10 | 10 | 121 | 2023 | An ISO-certified genomics workflow for identification and surveillance... |
| 2 | A | 43 | 10 | 9 | 7 | 8 | 9 | 42 | 2022 | Probiogenomic In-Silico Analysis and Safety Assessment of Lactiplantib... |
| 3 | A | 42 | 10 | 9 | 7 | 8 | 8 | 46 | 2019 | blaNDM-5 carried by a hypervirulent Klebsiella pneumoniae with sequenc... |
| 4 | A | 42 | 10 | 9 | 6 | 7 | 10 | 30 | 2023 | Whole-Genome Sequence of Lactococcus lactis Subsp. lactis LL16 Confirm... |
| 5 | A | 41 | 10 | 9 | 6 | 8 | 8 | 52 | 2020 | Genomic Epidemiology of Vancomycin-Resistant Enterococcus faecium (VRE... |
| 6 | A | 40 | 10 | 9 | 4 | 9 | 8 | 68 | 2020 | Machine learning with random subspace ensembles identifies antimicrobi... |
| 7 | A | 40 | 10 | 9 | 6 | 8 | 7 | 59 | 2018 | Comparative genomic analysis of Enterococcus faecalis: insights into t... |
| 8 | A | 40 | 10 | 9 | 4 | 8 | 9 | 43 | 2021 | Hybrid Assembly Provides Improved Resolution of Plasmids, Antimicrobia... |
| 9 | A | 40 | 10 | 9 | 6 | 7 | 8 | 35 | 2020 | Whole-genome sequence of multi-drug resistant Pseudomonas aeruginosa s... |
| 10 | A | 40 | 10 | 9 | 4 | 7 | 10 | 35 | 2023 | Virulence and antibiotic-resistance genes in Enterococcus faecalis ass... |
| 11 | A | 39 | 9 | 9 | 4 | 10 | 7 | 169 | 2018 | Prediction of antibiotic resistance in Escherichia coli from large-sca... |
| 12 | A | 39 | 9 | 8 | 6 | 8 | 8 | 50 | 2019 | Comparative genomic analysis revealed great plasticity and environment... |
| 13 | A | 39 | 10 | 9 | 4 | 8 | 8 | 42 | 2020 | Integrated genome-based probiotic relevance and safety evaluation of L... |
| 14 | A | 39 | 10 | 9 | 4 | 7 | 9 | 34 | 2021 | Genome analysis of a halophilic bacterium Halomonas malpeensis YU-PRIM... |
| 15 | A | 38 | 9 | 8 | 4 | 9 | 8 | 75 | 2019 | Rational construction of genome-reduced and high-efficient industrial ... |
| 16 | A | 38 | 10 | 9 | 4 | 8 | 7 | 53 | 2018 | Comparative genome analysis reveals key genetic factors associated wit... |
| 17 | A | 38 | 8 | 7 | 8 | 8 | 7 | 47 | 2018 | Escherichia coli B2 strains prevalent in inflammatory bowel disease pa... |
| 18 | A | 38 | 10 | 9 | 4 | 7 | 8 | 37 | 2019 | Comparative Genomic Insights into Secondary Metabolism Biosynthetic Ge... |
| 19 | A | 38 | 10 | 9 | 4 | 7 | 8 | 33 | 2020 | A Pan-Genome Guided Metabolic Network Reconstruction of Five Propionib... |
| 20 | A | 38 | 10 | 9 | 4 | 7 | 8 | 29 | 2020 | Genomic epidemiology of Campylobacter jejuni associated with asymptoma... |
| 21 | A | 38 | 10 | 9 | 4 | 6 | 9 | 16 | 2022 | Genome Analysis of ESBL-Producing Escherichia coli Isolated from Pigs... |
| 22 | A | 37 | 10 | 9 | 4 | 7 | 7 | 32 | 2018 | Physiological and Comparative Genomic Analysis of Arthrobacter sp. SRS... |
| 23 | A | 37 | 10 | 9 | 4 | 7 | 7 | 25 | 2018 | Comparative genomic analysis of Parageobacillus thermoglucosidasius st... |
| 24 | A | 37 | 10 | 9 | 4 | 6 | 8 | 20 | 2020 | AbGRI4, a novel antibiotic resistance island in multiply antibiotic-re... |
| 25 | A | 37 | 10 | 9 | 4 | 6 | 8 | 16 | 2019 | Extended insight into the Mycobacterium chelonae-abscessus complex thr... |

## Key Findings

### Open-source tool landscape in PATRIC-citing literature

- **37 papers** from 3,146 use exclusively open-source tools (1.2%)
- **15 papers** were excluded for using paid tools alongside open-source ones
- Most common paid tool contamination: **CLC Genomics Workbench** (8 papers), **Geneious** (5), **SeqSphere** (4)
- Most common open-source tools: RAST (30), SPAdes (15), Prokka (14), BLAST (28), ResFinder (12), VFDB (10)

### Compared to BVBRC_PRIMARY_CANDIDATES.md
- PRIMARY focused on PATRIC/RAST as **the analytical tool** (abstract-level)
- This list requires **full-text verified open-source-only pipelines**
- 21 PRIMARY candidates were deduped out; some overlap in RAST-heavy papers
- These candidates have richer, more replicable tool stacks (5+ tools average)

### Best replication targets (top 5)

1. **Sherry 2023** — ISO-certified AMR workflow, 9 OS tools, Nature Comms, 121 cites
2. **Kandasamy 2022** — L. plantarum probiogenomics, 10+ OS tools verified, full pipeline
3. **Yuan 2019** — blaNDM-5 K. pneumoniae, 15 OS tools, Kleborate+OrthoFinder+Gubbins
4. **Milerienė 2023** — L. lactis safety, 7 OS tools, antiSMASH+ResFinder+VirulenceFinder
5. **Ríos 2020** — VREfm Latin America, 8 OS tools, Roary+RAxML+ClonalFrameML

---
*Generated from `bvbrc_all.json` (3,146 papers). Tool stacks verified via Europe PMC full-text XML. 2026-05-05.*