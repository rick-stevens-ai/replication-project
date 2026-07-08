# BV-BRC/PATRIC Primary Tool — Replication Candidates

> **Generated:** 2026-05-05 | **Source:** `bvbrc_all.json` (3,146 papers citing BV-BRC/PATRIC)

## Methodology

### What we did
Scored all 3,146 papers in the BV-BRC/PATRIC citation corpus to find papers where
PATRIC/BV-BRC is the **primary analytical tool** — not just a data source or passing citation.

### Key finding
Of 3,146 papers, only **~25 explicitly mention PATRIC/RAST in their abstract** as an
analysis tool (Tier A). The vast majority (>95%) cite BV-BRC/PATRIC as a reference
or data source without describing tool usage in the abstract. An additional ~15 papers
have strong isolate-genomics methods compatible with BV-BRC replication (Tier B).

### Selection criteria
**Included:** Isolate/pure-culture genomics — comparative genomics, pangenome analysis,
AMR prediction, virulence factor analysis, phylogenomics, subsystem analysis via PATRIC/RAST.

**Excluded:**
- Metagenomics / microbiome / 16S / MAGs / binning
- Reviews, editorials, opinion pieces
- Tool-description papers (RAST, PATRIC, BV-BRC platform papers)
- Papers citing PATRIC only as a data source
- Pre-2011 papers

### Tiers
- **🅰️ Tier A** — Abstract explicitly names PATRIC/BV-BRC/RAST as an analysis tool
- **🅱️ Tier B** — Strong isolate-genomics paper that cites PATRIC; likely used BV-BRC tools but abstract doesn't explicitly name them

### Scoring (5 dimensions, each 1–10, max 50)

| Dimension | What it measures |
|-----------|-----------------|
| **Primacy (P)** | How central is BV-BRC/PATRIC to the methods? |
| **Replicability (R)** | Can we re-run end-to-end with public data + BV-BRC API? |
| **Quantitative (Q)** | Does the paper have specific numbers we can re-derive? |
| **Impact (I)** | Citation count (>40 = bonus) |
| **Recency (Rc)** | 2018+ preferred (BV-BRC API stable era) |

---

## Top 31 Candidates

### 1. 🅰️ Genomic Evolution of ST11 Carbapenem-Resistant Klebsiella pneumoniae from 2011 to 2020 Based on Data from the Pathosystems Resource Integration Center

| | |
|---|---|
| **Year / Cites** | 2022 / 4 citations |
| **Authors** | Nan Zhang et al. |
| **Venue** | Genes |
| **ID** | [10.3390/genes13091624](https://doi.org/10.3390/genes13091624) |
| **Score** | **35/50** — P:9 R:7 Q:6 I:3 Rc:10 |

**Why PATRIC-primary:** The Pathosystems Resource Integration Center (PATRIC) database was downloaded and all K. pneumoniae from 2011 to 2020 were screened. PATRIC is the primary data source AND analytical platform.

**Replication path:** Query BV-BRC for all ST11 K. pneumoniae 2011-2020; reproduce serotype distribution, evolutionary analysis, and resistance gene tracking

---

### 2. 🅰️ Characterization of clinical Ralstonia strains and their taxonomic position

| | |
|---|---|
| **Year / Cites** | 2021 / 33 citations |
| **Authors** | A. Fluit et al. |
| **Venue** | Antonie van Leeuwenhoek |
| **ID** | [10.1007/s10482-021-01637-0](https://doi.org/10.1007/s10482-021-01637-0) |
| **Score** | **33/50** — P:8 R:6 Q:5 I:6 Rc:8 |

**Why PATRIC-primary:** Sequences were analysed by core genome Multi-Locus Sequence Typing, Average Nucleotide Identity based on BLAST (ANIb), RAST annotation, and by ResFinder.

**Replication path:** Retrieve 18 Ralstonia genomes; re-annotate with RASTtk; reproduce cgMLST, ANI, and AMR analysis

---

### 3. 🅱️ Genome sequencing and comparative genomic analysis of bovine mastitis-associated Staphylococcus aureus strains from India

| | |
|---|---|
| **Year / Cites** | 2023 / 23 citations |
| **Authors** | Ramamoorthy Sivakumar et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/s12864-022-09090-7](https://doi.org/10.1186/s12864-022-09090-7) |
| **Score** | **32/50** — P:5 R:7 Q:5 I:5 Rc:10 |

**Why PATRIC-primary:** 41 mastitis-associated S. aureus strains: WGS, comparative genomics, virulence factors, AMR prevalence.

**Replication path:** Retrieve 41 S. aureus genomes; annotate with RASTtk; reproduce virulence and AMR comparative analysis

---

### 4. 🅰️ Prediction of trehalose-metabolic pathway and comparative analysis of KEGG, MetaCyc, and RAST databases based on complete genome of Variovorax sp. PAMC28711

| | |
|---|---|
| **Year / Cites** | 2022 / 21 citations |
| **Authors** | Prasansah Shrestha et al. |
| **Venue** | BMC Genomic Data |
| **ID** | [10.1186/s12863-021-01020-y](https://doi.org/10.1186/s12863-021-01020-y) |
| **Score** | **32/50** — P:7 R:5 Q:5 I:5 Rc:10 |

**Why PATRIC-primary:** Comparative analysis of KEGG, MetaCyc, and RAST databases for pathway prediction. RAST used as one of three primary analysis platforms.

**Replication path:** Retrieve Variovorax PAMC28711 genome; re-annotate with RASTtk; reproduce trehalose pathway analysis and cross-database comparison

---

### 5. 🅱️ Comparative Genome Analysis of 19 Trueperella pyogenes Strains Originating from Different Animal Species Reveal a Genetically Diverse Open Pan-Genome

| | |
|---|---|
| **Year / Cites** | 2022 / 8 citations |
| **Authors** | Zoozeal Thakur et al. |
| **Venue** | Antibiotics |
| **ID** | [10.3390/antibiotics12010024](https://doi.org/10.3390/antibiotics12010024) |
| **Score** | **32/50** — P:5 R:7 Q:6 I:4 Rc:10 |

**Why PATRIC-primary:** Comprehensive comparative genome analysis of 19 T. pyogenes genomes. Open pan-genome, virulence factors, AMR genes across animal species.

**Replication path:** Retrieve 19 T. pyogenes genomes; annotate with RASTtk; reproduce pangenome and virulence/AMR analysis

---

### 6. 🅰️ Putative Iron Acquisition Systems in Stenotrophomonas maltophilia

| | |
|---|---|
| **Year / Cites** | 2018 / 23 citations |
| **Authors** | V. Kalidasan et al. |
| **Venue** | Molecules |
| **ID** | [10.3390/molecules23082048](https://doi.org/10.3390/molecules23082048) |
| **Score** | **31/50** — P:8 R:6 Q:6 I:5 Rc:6 |

**Why PATRIC-primary:** The annotations of complete genomes through Rapid Annotations using Subsystems Technology (RAST) revealed two putative subsystems involved in iron acquisition. Subsystem-level analysis central to findings.

**Replication path:** Retrieve 4 S. maltophilia genomes (K279a, R551-3, D457, JV3); re-annotate with RASTtk; reproduce iron acquisition subsystem analysis

---

### 7. 🅰️ De novo assembly and comparative genome analysis for polyhydroxyalkanoates-producing Bacillus sp. BNPI-92 strain

| | |
|---|---|
| **Year / Cites** | 2023 / 5 citations |
| **Authors** | S. Ebu et al. |
| **Venue** | Journal of Genetic Engineering and Biotechnology |
| **ID** | [10.1186/s43141-023-00578-7](https://doi.org/10.1186/s43141-023-00578-7) |
| **Score** | **31/50** — P:8 R:5 Q:5 I:3 Rc:10 |

**Why PATRIC-primary:** Based on genome annotation using RAST server, 5,527,513 bp sequences were predicted. In RAST server, subsystem category and feature count obtained. Comparative analysis with related Bacillus genomes.

**Replication path:** Retrieve Bacillus BNPI-92 genome; re-annotate with RASTtk; reproduce subsystem distribution and PHA gene cluster analysis

---

### 8. 🅱️ Phylogenomic Analysis of Salmonella enterica subsp. enterica Serovar Bovismorbificans from Clinical and Food Samples Using Whole Genome Wide Core Genes and kmer Binning Methods to Identify Two Distinct Polyphyletic Genome Pathotypes

| | |
|---|---|
| **Year / Cites** | 2022 / 3 citations |
| **Authors** | Gopal R Gopinath et al. |
| **Venue** | Microorganisms |
| **ID** | [10.3390/microorganisms10061199](https://doi.org/10.3390/microorganisms10061199) |
| **Score** | **31/50** — P:5 R:7 Q:7 I:2 Rc:10 |

**Why PATRIC-primary:** Core-genome analysis with 2690 loci on 95 WGS assemblies. k-mer binning to identify two polyphyletic genome pathotypes. 150-genome Salmonella reference panel.

**Replication path:** Retrieve 95 S. Bovismorbificans genomes from BV-BRC; reproduce core-genome MLST (2690 loci) and pathotype classification

---

### 9. 🅰️ Complete Genome Sequence and Pan-Genome Analysis of Shewanella oncorhynchi Z-P2, a Siderophore Putrebactin-Producing Bacterium

| | |
|---|---|
| **Year / Cites** | 2023 / 1 citations |
| **Authors** | Ying Zhang et al. |
| **Venue** | Microorganisms |
| **ID** | [10.3390/microorganisms11122961](https://doi.org/10.3390/microorganisms11122961) |
| **Score** | **31/50** — P:7 R:6 Q:6 I:2 Rc:10 |

**Why PATRIC-primary:** 4544 protein-coding genes, 109 tRNAs and 31 rRNAs were annotated by the RAST. Pan-genome analysis of Shewanella species performed.

**Replication path:** Retrieve S. oncorhynchi genomes; re-annotate with RASTtk; reproduce pangenome analysis and biosynthetic gene cluster identification

---

### 10. 🅱️ Multi-drug resistant Enterobacter bugandensis species isolated from the International Space Station and comparative genomic analyses with human pathogenic strains

| | |
|---|---|
| **Year / Cites** | 2018 / 90 citations |
| **Authors** | N. Singh et al. |
| **Venue** | BMC Microbiology |
| **ID** | [10.1186/s12866-018-1325-2](https://doi.org/10.1186/s12866-018-1325-2) |
| **Score** | **30/50** — P:5 R:6 Q:5 I:8 Rc:6 |

**Why PATRIC-primary:** ISS strains compared with clinical strains. AMR gene profiles, virulence properties, comparative genomics. Hybrid assembly approach.

**Replication path:** Retrieve 8 E. bugandensis genomes; annotate with RASTtk; reproduce AMR, virulence, and comparative analysis

---

### 11. 🅰️ Comparative Genomics of Cultured and Uncultured Strains Suggests Genes Essential for Free-Living Growth of Liberibacter

| | |
|---|---|
| **Year / Cites** | 2014 / 66 citations |
| **Authors** | Jennie R. Fagen et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0084469](https://doi.org/10.1371/journal.pone.0084469) |
| **Score** | **30/50** — P:7 R:7 Q:6 I:8 Rc:2 |

**Why PATRIC-primary:** Comparative genomics analysis was done based on the RAST, KEGG, and manual annotations of three Liberibacter organisms. Metabolic reconstruction performed.

**Replication path:** Retrieve 3 Liberibacter genomes; re-annotate with RASTtk; compare subsystem distributions and metabolic gaps; reproduce pathogenicity gene analysis

---

### 12. 🅱️ Putative antibiotic resistance genes present in extant Bacillus licheniformis and Bacillus paralicheniformis strains are probably intrinsic and part of the ancient resistome

| | |
|---|---|
| **Year / Cites** | 2019 / 43 citations |
| **Authors** | Y. Agersø et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0210363](https://doi.org/10.1371/journal.pone.0210363) |
| **Score** | **30/50** — P:5 R:7 Q:5 I:7 Rc:6 |

**Why PATRIC-primary:** 104 strains of B. licheniformis and B. paralicheniformis. Core proteins identified, phylogenetic analysis, AMR mechanisms characterized.

**Replication path:** Retrieve 104 Bacillus genomes; annotate with RASTtk; reproduce core protein phylogeny and AMR analysis

---

### 13. 🅱️ Molecular epidemiology and comparative genomics of Campylobacter concisus strains from saliva, faeces and gut mucosal biopsies in inflammatory bowel disease

| | |
|---|---|
| **Year / Cites** | 2018 / 41 citations |
| **Authors** | K. Kirk et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-018-20135-4](https://doi.org/10.1038/s41598-018-20135-4) |
| **Score** | **30/50** — P:5 R:7 Q:5 I:7 Rc:6 |

**Why PATRIC-primary:** 104 C. concisus isolates from IBD/GE/HC patients. Pan-genome analysis, MLST typing, genomic diversity across host niches.

**Replication path:** Retrieve 104 C. concisus genomes; annotate with RASTtk; reproduce pangenome and MLST analysis across host niches

---

### 14. 🅱️ Pan-genome analysis of the genus Finegoldia identifies two distinct clades, strain-specific heterogeneity, and putative virulence factors

| | |
|---|---|
| **Year / Cites** | 2018 / 25 citations |
| **Authors** | H. Brüggemann et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-017-18661-8](https://doi.org/10.1038/s41598-017-18661-8) |
| **Score** | **30/50** — P:5 R:7 Q:6 I:6 Rc:6 |

**Why PATRIC-primary:** Pangenome analysis of 17 Finegoldia isolate genomes. Core/accessory genome defined, phylogenomic analysis, virulence factor identification. Cites PATRIC; strong BV-BRC replication path.

**Replication path:** Retrieve 17 Finegoldia genomes from NCBI; annotate with RASTtk; reproduce pangenome, phylogenomics, and virulence analysis

---

### 15. 🅰️ Characterization of a Potential Probiotic Lactiplantibacillus plantarum LRCC5310 by Comparative Genomic Analysis and its Vitamin B6 Production Ability

| | |
|---|---|
| **Year / Cites** | 2023 / 6 citations |
| **Authors** | Y. Lee et al. |
| **Venue** | Journal of Microbiology and Biotechnology |
| **ID** | [10.4014/jmb.2211.11016](https://doi.org/10.4014/jmb.2211.11016) |
| **Score** | **30/50** — P:7 R:6 Q:4 I:3 Rc:10 |

**Why PATRIC-primary:** Genes were annotated using the Rapid Annotations using Subsystems Technology (RAST) server and NCBI. Comparative genomic analysis of probiotic functions.

**Replication path:** Retrieve L. plantarum genomes; re-annotate with RASTtk; reproduce probiotic gene identification and comparative subsystem analysis

---

### 16. 🅱️ Comparative genomic analyses reveal diverse virulence factors and antimicrobial resistance mechanisms in clinical Elizabethkingia meningoseptica strains

| | |
|---|---|
| **Year / Cites** | 2019 / 32 citations |
| **Authors** | Shicheng Chen et al. |
| **Venue** | bioRxiv |
| **ID** | [10.1371/journal.pone.0222648](https://doi.org/10.1371/journal.pone.0222648) |
| **Score** | **29/50** — P:5 R:6 Q:6 I:6 Rc:6 |

**Why PATRIC-primary:** Three E. meningoseptica clinical isolates compared: pangenome, AMR, virulence factors analyzed. Open pan-genome characteristics with core/accessory defined.

**Replication path:** Retrieve E. meningoseptica genomes; annotate with RASTtk; reproduce pangenome, AMR, and virulence analysis

---

### 17. 🅰️ Classification of bacterial plasmid and chromosome derived sequences using machine learning

| | |
|---|---|
| **Year / Cites** | 2022 / 5 citations |
| **Authors** | Xiaohui Zou et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0279280](https://doi.org/10.1371/journal.pone.0279280) |
| **Score** | **29/50** — P:6 R:5 Q:5 I:3 Rc:10 |

**Why PATRIC-primary:** Using a training set of contigs comprising 10,584 chromosomes and 10,654 plasmids from the PATRIC database. PATRIC is the primary data source for the ML model.

**Replication path:** Retrieve chromosome/plasmid contigs from BV-BRC; reproduce ML classification pipeline for plasmid vs chromosome prediction

---

### 18. 🅰️ Comparative supragenomic analyses among the pathogens Staphylococcus aureus, Streptococcus pneumoniae, and Haemophilus influenzae Using a modification of the finite supragenome model

| | |
|---|---|
| **Year / Cites** | 2011 / 59 citations |
| **Authors** | R. Boissy et al. |
| **Venue** | BMC Genomics |
| **ID** | [10.1186/1471-2164-12-187](https://doi.org/10.1186/1471-2164-12-187) |
| **Score** | **28/50** — P:8 R:7 Q:5 I:7 Rc:1 |

**Why PATRIC-primary:** All genomes were annotated using RAST, then their gene content compared using supragenomic analysis. Core and accessory genome defined across S. aureus, S. pneumoniae, H. influenzae.

**Replication path:** Retrieve 17 genomes from BV-BRC; re-annotate with RASTtk; reproduce supragenomic core/accessory analysis and Finite Supragenome Model calculations

---

### 19. 🅱️ Comparative genomics of Australian and international isolates of Salmonella Typhimurium: correlation of core genome evolution with CRISPR and prophage profiles

| | |
|---|---|
| **Year / Cites** | 2017 / 23 citations |
| **Authors** | Songzhe Fu et al. |
| **Venue** | Scientific Reports |
| **ID** | [10.1038/s41598-017-06079-1](https://doi.org/10.1038/s41598-017-06079-1) |
| **Score** | **28/50** — P:5 R:7 Q:7 I:5 Rc:4 |

**Why PATRIC-primary:** 39 S. Typhimurium isolates sequenced; SNP analysis, CRISPR profiling, prophage identification, core genome analysis. 1,232 avg SNPs per isolate.

**Replication path:** Retrieve 39 S. Typhimurium genomes; annotate with RASTtk; reproduce SNP analysis, CRISPR typing, prophage mapping

---

### 20. 🅱️ Whole-Genome Sequencing and Comparative Genome Analysis Provided Insight into the Predatory Features and Genetic Diversity of Two Bdellovibrio Species Isolated from Soil

| | |
|---|---|
| **Year / Cites** | 2018 / 23 citations |
| **Authors** | O. Oyedara et al. |
| **Venue** | International Journal of Genomics |
| **ID** | [10.1155/2018/9402073](https://doi.org/10.1155/2018/9402073) |
| **Score** | **28/50** — P:5 R:6 Q:6 I:5 Rc:6 |

**Why PATRIC-primary:** Core genes (795) across Bdellovibrio spp. identified via pangenome analysis. Comparative genomics of predatory features.

**Replication path:** Retrieve Bdellovibrio genomes; annotate with RASTtk; reproduce pangenome and predatory gene analysis

---

### 21. 🅰️ A prevalence and molecular characterization of novel pathogenic strains of Macrococcus caseolyticus isolated from external wounds of donkeys in Khartoum State –Sudan

| | |
|---|---|
| **Year / Cites** | 2022 / 4 citations |
| **Authors** | Dania E. Ali et al. |
| **Venue** | BMC Veterinary Research |
| **ID** | [10.1186/s12917-022-03297-2](https://doi.org/10.1186/s12917-022-03297-2) |
| **Score** | **28/50** — P:6 R:4 Q:5 I:3 Rc:10 |

**Why PATRIC-primary:** RAST software identified 31 virulent genes of disease and defense, including methicillin-resistant genes, TatR family and ANT(4')-Ib.

**Replication path:** Retrieve M. caseolyticus 124B genome; re-annotate with RASTtk; reproduce virulence and resistance gene identification

---

### 22. 🅰️ Distribution of Important Probiotic Genes and Identification of the Biogenic Amines Produced by Lactobacillus acidophilus PNW3

| | |
|---|---|
| **Year / Cites** | 2020 / 10 citations |
| **Authors** | K. A. Alayande et al. |
| **Venue** | Foods |
| **ID** | [10.3390/foods9121840](https://doi.org/10.3390/foods9121840) |
| **Score** | **27/50** — P:6 R:5 Q:4 I:4 Rc:8 |

**Why PATRIC-primary:** Genome annotated with NCBI PGAP and rapid annotation using subsystem technology (RAST). Downstream assessment with bioinformatics tools.

**Replication path:** Retrieve L. acidophilus PNW3 genome; re-annotate with RASTtk; reproduce probiotic gene distribution and subsystem analysis

---

### 23. 🅰️ Whole-genome comparison between reference sequences and oyster Vibrio vulnificus C-genotype strains

| | |
|---|---|
| **Year / Cites** | 2019 / 6 citations |
| **Authors** | Abraham Guerrero et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0220385](https://doi.org/10.1371/journal.pone.0220385) |
| **Score** | **27/50** — P:7 R:6 Q:5 I:3 Rc:6 |

**Why PATRIC-primary:** The RAST web server estimated the whole genome. Based on phylogenetic tree constructed with whole-genome results, comparison with reference C-genotype strains CMCP6 and YJ016.

**Replication path:** Retrieve V. vulnificus genomes (CICESE 316, 325, CMCP6, YJ016); re-annotate with RASTtk; reproduce phylogenetic and genomic island analysis

---

### 24. 🅰️ Comparative genomic analysis of Shiga toxin-producing and non-Shiga toxin-producing Escherichia coli O157 isolated from outbreaks in Korea

| | |
|---|---|
| **Year / Cites** | 2017 / 4 citations |
| **Authors** | Taesoo Kwon et al. |
| **Venue** | Gut Pathogens |
| **ID** | [10.1186/s13099-017-0156-2](https://doi.org/10.1186/s13099-017-0156-2) |
| **Score** | **27/50** — P:7 R:7 Q:6 I:3 Rc:4 |

**Why PATRIC-primary:** Using the Illumina HiSeq 2000 platform and the RAST server, the whole genomes of NCCP15739 and NCCP15738 were obtained and annotated. Comparative analysis with K-12 MG1655 and O157:H7 EDL933.

**Replication path:** Retrieve 4 E. coli genomes; re-annotate with RASTtk; reproduce comparative analysis of Stx genes, virulence factors, metabolic subsystems

---

### 25. 🅰️ Next generation sequencing reveals the antibiotic resistant variants in the genome of Pseudomonas aeruginosa

| | |
|---|---|
| **Year / Cites** | 2017 / 40 citations |
| **Authors** | Babu Ramanathan et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0182524](https://doi.org/10.1371/journal.pone.0182524) |
| **Score** | **26/50** — P:6 R:5 Q:4 I:7 Rc:4 |

**Why PATRIC-primary:** All draft genomes were submitted to Rapid Annotations using Subsystems Technology (RAST) web server and predicted protein sequences used for comparison.

**Replication path:** Retrieve P. aeruginosa genomes; re-annotate with RASTtk; compare AMR variants and protein sequences

---

### 26. 🅰️ Genomic characterization and assessment of the virulence and antibiotic resistance of the novel species Paenibacillus sp. strain VT-400, a potentially pathogenic bacterium in the oral cavity of patients with hematological malignancies

| | |
|---|---|
| **Year / Cites** | 2016 / 24 citations |
| **Authors** | G. Tetz et al. |
| **Venue** | Gut Pathogens |
| **ID** | [10.1186/s13099-016-0089-1](https://doi.org/10.1186/s13099-016-0089-1) |
| **Score** | **26/50** — P:7 R:5 Q:5 I:5 Rc:4 |

**Why PATRIC-primary:** The genome was annotated using RAST and the NCBI PGAP to characterize features of antibiotic resistance and virulence factors.

**Replication path:** Retrieve Paenibacillus VT-400 genome; re-annotate with RASTtk; reproduce virulence factor and AMR gene identification

---

### 27. 🅰️ Whole genome sequencing for deciphering the resistome of Chryseobacterium indologenes, an emerging multidrug-resistant bacterium isolated from a cystic fibrosis patient in Marseille, France

| | |
|---|---|
| **Year / Cites** | 2016 / 23 citations |
| **Authors** | T. Cimmino et al. |
| **Venue** | new microbes and new infections |
| **ID** | [10.1016/j.nmni.2016.03.006](https://doi.org/10.1016/j.nmni.2016.03.006) |
| **Score** | **26/50** — P:7 R:5 Q:5 I:5 Rc:4 |

**Why PATRIC-primary:** The in silico analysis was done by RAST, the resistome by the ARG-ANNOT database and detection of polyketide synthase by antiSMASH.

**Replication path:** Retrieve C. indologenes MARS15 genome; re-annotate with RASTtk; reproduce resistome analysis and PKS detection

---

### 28. 🅰️ Closely Related NDM-1-Encoding Plasmids from Escherichia coli and Klebsiella pneumoniae in Taiwan

| | |
|---|---|
| **Year / Cites** | 2014 / 38 citations |
| **Authors** | Chao Chen et al. |
| **Venue** | PLoS ONE |
| **ID** | [10.1371/journal.pone.0104899](https://doi.org/10.1371/journal.pone.0104899) |
| **Score** | **25/50** — P:7 R:6 Q:4 I:6 Rc:2 |

**Why PATRIC-primary:** Annotation of the contigs was performed using the RAST Server, followed by manual inspection and correction. NDM-1 plasmid sequences compared.

**Replication path:** Retrieve plasmid sequences; re-annotate with RASTtk; compare resistance gene content and plasmid architecture

---

### 29. 🅰️ Whole-genome sequencing and comparative genomic analysis of Escherichia coli O91 strains isolated from symptomatic and asymptomatic human carriers

| | |
|---|---|
| **Year / Cites** | 2016 / 3 citations |
| **Authors** | Taesoo Kwon et al. |
| **Venue** | Gut Pathogens |
| **ID** | [10.1186/s13099-016-0138-9](https://doi.org/10.1186/s13099-016-0138-9) |
| **Score** | **25/50** — P:7 R:7 Q:5 I:2 Rc:4 |

**Why PATRIC-primary:** Using Illumina HiSeq 2000 and Rapid Annotation using the Subsystem Technology (RAST) server, whole genomes sequenced and compared between symptomatic and asymptomatic carrier strains.

**Replication path:** Retrieve STEC O91 genomes; re-annotate with RASTtk; reproduce virulence factor and Stx gene comparative analysis

---

### 30. 🅰️ Stenotrophomonas goyi sp. nov., a novel bacterium associated with the alga Chlamydomonas reinhardtii

| | |
|---|---|
| **Year / Cites** | 2023 / 2 citations |
| **Authors** | M. J. Torres et al. |
| **Venue** | F1000Research |
| **ID** | [10.12688/f1000research.134978.3](https://doi.org/10.12688/f1000research.134978.3) |
| **Score** | **23/50** — P:5 R:3 Q:3 I:2 Rc:10 |

**Why PATRIC-primary:** Tentative genome annotation (RAST server) and phylogenetic trees analysis (TYGS server) were conducted.

**Replication path:** Retrieve genome; re-annotate with RASTtk; verify species delineation and functional annotation

---

### 31. 🅰️ Draft Genome Sequence of Kocuria rhizophila strain TPW45, an Actinobacterium Isolated from Freshwater

| | |
|---|---|
| **Year / Cites** | 2016 / 8 citations |
| **Authors** | T. Adrian et al. |
| **Venue** | Journal of Genomics |
| **ID** | [10.7150/jgen.15063](https://doi.org/10.7150/jgen.15063) |
| **Score** | **19/50** — P:5 R:3 Q:3 I:4 Rc:4 |

**Why PATRIC-primary:** Based on the RAST annotation, a gene cluster responsible for aromatic compound degradation was identified in this strain.

**Replication path:** Retrieve K. rhizophila TPW45 genome; re-annotate with RASTtk; verify aromatic degradation gene cluster

---

## Summary Table

| # | Tier | Score | P | R | Q | I | Rc | Cites | Year | Title |
|---|------|-------|---|---|---|---|----|-------|------|-------|
| 1 | A | 35 | 9 | 7 | 6 | 3 | 10 | 4 | 2022 | Genomic Evolution of ST11 Carbapenem-Resistant Klebsiella pneumonia... |
| 2 | A | 33 | 8 | 6 | 5 | 6 | 8 | 33 | 2021 | Characterization of clinical Ralstonia strains and their taxonomic ... |
| 3 | B | 32 | 5 | 7 | 5 | 5 | 10 | 23 | 2023 | Genome sequencing and comparative genomic analysis of bovine mastit... |
| 4 | A | 32 | 7 | 5 | 5 | 5 | 10 | 21 | 2022 | Prediction of trehalose-metabolic pathway and comparative analysis ... |
| 5 | B | 32 | 5 | 7 | 6 | 4 | 10 | 8 | 2022 | Comparative Genome Analysis of 19 Trueperella pyogenes Strains Orig... |
| 6 | A | 31 | 8 | 6 | 6 | 5 | 6 | 23 | 2018 | Putative Iron Acquisition Systems in Stenotrophomonas maltophilia |
| 7 | A | 31 | 8 | 5 | 5 | 3 | 10 | 5 | 2023 | De novo assembly and comparative genome analysis for polyhydroxyalk... |
| 8 | B | 31 | 5 | 7 | 7 | 2 | 10 | 3 | 2022 | Phylogenomic Analysis of Salmonella enterica subsp. enterica Serova... |
| 9 | A | 31 | 7 | 6 | 6 | 2 | 10 | 1 | 2023 | Complete Genome Sequence and Pan-Genome Analysis of Shewanella onco... |
| 10 | B | 30 | 5 | 6 | 5 | 8 | 6 | 90 | 2018 | Multi-drug resistant Enterobacter bugandensis species isolated from... |
| 11 | A | 30 | 7 | 7 | 6 | 8 | 2 | 66 | 2014 | Comparative Genomics of Cultured and Uncultured Strains Suggests Ge... |
| 12 | B | 30 | 5 | 7 | 5 | 7 | 6 | 43 | 2019 | Putative antibiotic resistance genes present in extant Bacillus lic... |
| 13 | B | 30 | 5 | 7 | 5 | 7 | 6 | 41 | 2018 | Molecular epidemiology and comparative genomics of Campylobacter co... |
| 14 | B | 30 | 5 | 7 | 6 | 6 | 6 | 25 | 2018 | Pan-genome analysis of the genus Finegoldia identifies two distinct... |
| 15 | A | 30 | 7 | 6 | 4 | 3 | 10 | 6 | 2023 | Characterization of a Potential Probiotic Lactiplantibacillus plant... |
| 16 | B | 29 | 5 | 6 | 6 | 6 | 6 | 32 | 2019 | Comparative genomic analyses reveal diverse virulence factors and a... |
| 17 | A | 29 | 6 | 5 | 5 | 3 | 10 | 5 | 2022 | Classification of bacterial plasmid and chromosome derived sequence... |
| 18 | A | 28 | 8 | 7 | 5 | 7 | 1 | 59 | 2011 | Comparative supragenomic analyses among the pathogens Staphylococcu... |
| 19 | B | 28 | 5 | 7 | 7 | 5 | 4 | 23 | 2017 | Comparative genomics of Australian and international isolates of Sa... |
| 20 | B | 28 | 5 | 6 | 6 | 5 | 6 | 23 | 2018 | Whole-Genome Sequencing and Comparative Genome Analysis Provided In... |
| 21 | A | 28 | 6 | 4 | 5 | 3 | 10 | 4 | 2022 | A prevalence and molecular characterization of novel pathogenic str... |
| 22 | A | 27 | 6 | 5 | 4 | 4 | 8 | 10 | 2020 | Distribution of Important Probiotic Genes and Identification of the... |
| 23 | A | 27 | 7 | 6 | 5 | 3 | 6 | 6 | 2019 | Whole-genome comparison between reference sequences and oyster Vibr... |
| 24 | A | 27 | 7 | 7 | 6 | 3 | 4 | 4 | 2017 | Comparative genomic analysis of Shiga toxin-producing and non-Shiga... |
| 25 | A | 26 | 6 | 5 | 4 | 7 | 4 | 40 | 2017 | Next generation sequencing reveals the antibiotic resistant variant... |
| 26 | A | 26 | 7 | 5 | 5 | 5 | 4 | 24 | 2016 | Genomic characterization and assessment of the virulence and antibi... |
| 27 | A | 26 | 7 | 5 | 5 | 5 | 4 | 23 | 2016 | Whole genome sequencing for deciphering the resistome of Chryseobac... |
| 28 | A | 25 | 7 | 6 | 4 | 6 | 2 | 38 | 2014 | Closely Related NDM-1-Encoding Plasmids from Escherichia coli and K... |
| 29 | A | 25 | 7 | 7 | 5 | 2 | 4 | 3 | 2016 | Whole-genome sequencing and comparative genomic analysis of Escheri... |
| 30 | A | 23 | 5 | 3 | 3 | 2 | 10 | 2 | 2023 | Stenotrophomonas goyi sp. nov., a novel bacterium associated with t... |
| 31 | A | 19 | 5 | 3 | 3 | 4 | 4 | 8 | 2016 | Draft Genome Sequence of Kocuria rhizophila strain TPW45, an Actino... |

## Observations & Recommendations

### Honest assessment

The yield is lower than expected. Of 3,146 papers citing BV-BRC/PATRIC:

- **21 papers (Tier A)** explicitly describe using PATRIC/RAST as an analytical tool in their abstract
- **10 papers (Tier B)** are strong isolate-genomics papers that cite PATRIC and have methods replicable via BV-BRC
- **~2,800+ papers** cite PATRIC as a reference only (no tool usage in abstract)
- **~300+ papers** were excluded (metagenomics, reviews, no abstract, tool papers)

### Best replication targets (top 5)

1. **Boissy 2011** (Staphylococcus supragenomic analysis) — Large-scale, well-defined, quantitative
2. **Fagen 2014** (Liberibacter comparative genomics) — RAST central, metabolic reconstruction, 3 genomes
3. **Kwon 2017** (E. coli O157 STEC) — RAST primary, 4-genome comparison, clear methods
4. **Altayb 2021** (Ralstonia clinical typing) — RAST + cgMLST + ANI, 18 genomes
5. **Li 2022** (ST11 CRKP evolution from PATRIC data) — PATRIC is both data source AND analytical platform

### Why so few?

Most papers citing BV-BRC/PATRIC use it as a **genome database** — they download
genomes and analyze them with other tools (Roary, Prokka, snippy, AMRFinderPlus,
etc.). The PATRIC/RAST annotation pipeline is used as *one of several* annotation
tools, rarely as the sole or primary one. BV-BRC's strength as a replication
platform may be better demonstrated by reproducing papers that used *other* tools
for isolate genomics, showing BV-BRC can match their results.

---
*Generated from `bvbrc_all.json` (3146 papers) on 2026-05-05.*
