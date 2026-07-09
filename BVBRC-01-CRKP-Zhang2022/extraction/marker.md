Article

Genomic Evolution of ST11 Carbapenem-Resistant Klebsiella
pneumoniae from 2011 to 2020 Based on Data from the
Pathosystems Resource Integration Center
Na Zhang 1,2,†, Yue Tang 2,†, Xiaojing Yang 1,2, Meiling Jin 1,2, Jiali Chen 1,2, Shiyu Qin 2,3, Fangni Liu 1,2, Xiong Liu 4,
Jinpeng Guo 2, Changjun Wang 1,2,3,* and Yong Chen 2,*

                                           1 School of Public Health, China Medical University, Shenyang 110122, China
                                           2 Department of Emergency Response, Chinese PLA Center for Disease Control and Prevention,
                                             Beijing 100071, China
                                           3 College of Public Health, Zhengzhou University, Zhengzhou 450001, China

                                           4 Department of Information, Chinese PLA Center for Disease Control and Prevention, Beijing 100071, China

                                           * Correspondence: science2008@hotmail.com (C.W.); chenyonger@126.com (Y.C.)
                                           † These authors contribute equally to this work.


                                           Abstract: (1) Objective: ST11 carbapenem-resistant Klebsiella pneumoniae (CRKP) is widespread
                                           throughout the world, and the mechanisms for the transmission and evolution of major serotypes,
                                           ST11-KL47 and ST11-KL64, were analyzed to investigate the global distribution and evolutionary
                                           characteristics of ST11 CRKP; (2) Methods: The Pathosystems Resource Integration Center
                                           (PATRIC) database was downloaded and all K. pneumoniae from 2011 to 2020 were screened to ob-
                                           tain ST11 CRKP genome assemblies with basic information. The relationship of serotype evolution
                                           between KL47 and KL64 was then investigated using statistical and bioinformatic analysis; (3) Re-
Citation: Zhang, N.; Tang, Y.; Yang,       sults: In total, 386 ST11 CRKP isolates were included for analysis. Blood (31.09%, 120/386), respira-
X.; Jin, M.; Chen, J.; Qin, S.; Liu, F.;   tory tract (23.06%, 89/386), and feces (20.21%, 78/386) were the major sources of samples. China was
Liu, X.; Guo, J.; Wang, C.; et al.
                                           the leading country where ST11 CRKP was isolated. KL47 and KL64 were found to be the most
Genomic Evolution of ST11
                                           prevalent serotypes. ST11-KL64 CRKP [median 78(P25-P75: 72~79.25)] had remarkably more viru-
Carbapenem-Resistant Klebsiella
                                           lence genes than the KL47 [median 63(P25~P75: 63~69)], and the distinction was statistically signifi-
pneumoniae from 2011 to 2020 Based
                                           cant (p < 0.001). A differential comparison of virulence genes between KL47 and KL64 revealed 35
on Data from the Pathosystems
Resource Integration Center. Genes
                                           differential virulence genes, including rmpA/rmpA2, iucABCD, iutA, etc. The comparison of the re-
2022, 13, 1624. https://doi.org/           combination of serotype-determining regions between the two serotypes revealed that KL64 CRKP
10.3390/genes13091624                      carried more nucleotide sequences in the CD1-VR2-CD2 region than KL47 CRKP. More nucleotide
                                           sequences added approximately 303 base pairs (bp) with higher GC content (58.14%), which might
Academic Editor: Stefano Lonardi
                                           facilitate the evolution of the serotype toward KL64; (4) Conclusions: KL47 and KL64 have become
Received: 21 August 2022                   the predominant serotypes of ST11 CRKP. KL64 CRKP carries more virulence genes than KL47 and
Accepted: 8 September 2022                 has increased by approximately 303 bp through recombinant mutations, thus facilitating the evolu-
Published: 10 September 2022               tion of KL47 to KL64. Stricter infection prevention and control measures should be developed to
Publisher’s Note: MDPI stays neu-          deal with the epidemic transmission of ST11-KL64 CRKP.
tral with regard to jurisdictional
claims in published maps and institu-      Keywords: global; whole-genome sequence; serotype; distribution characteristics; evolution
tional affiliations.




                                           1. Introduction
Copyright: © 2022 by the authors. Li-
                                               As an important Gram-negative bacterium, Klebsiella pneumoniae can cause a variety
censee MDPI, Basel, Switzerland.
                                           of healthcare-associated infections, including pneumonia, bloodstream infections, and
This article is an open access article
                                           wound or surgical site infections. The frequent use of antibiotics has made it easier for K.
distributed under the terms and con-
ditions of the Creative Commons At-
                                           pneumoniae to undergo chromosomal changes and develop antibiotic resistance [1]. Car-
tribution (CC BY) license (https://cre-
                                           bapenem-resistant K. pneumoniae (CRKP) belongs to a commonly detected pathogen in
ativecommons.org/licenses/by/4.0/).




Genes 2022, 13, 1624. https://doi.org/10.3390/genes13091624                                                            www.mdpi.com/journal/genes
Genes 2022, 13, 1624                                                                                           2 of 12




                       hospitals all around the world. CRKP infection has become a serious health threat because
                       of its aggressive pathogenesis [2], poor prognosis, and high mortality [3,4].
                             Multilocus sequence typing (MLST) uses nucleic acid sequences to classify bacteria
                       and examine strain diversity by amplifying the internal segments of seven housekeeping
                       genes and analyzing their sequences. Serotyping is an immunological technique that can
                       classify the same bacterium into different subspecies and is used to distinguish several
                       forms of the same pathogen. The predominant multilocus sequence type in China is ST11,
                       while ST258 is the predominant sequence type in the United States and European coun-
                       tries [5,6]. Both ST11 and ST258 belong to the CG258 clonal lineage. The most common
                       and effective method for serotyping is to compare the DNA homology of the wzc gene’s
                       CD1-VR2-CD2 variable region. In this region, 80.00% of homology is considered different
                       serotypes, while more than 96.00% of homology is considered the same serotype [7]. In
                       recent years, the proportion of ST11-KL64 in CRKP strains has gradually increased [8],
                       while ST11-KL47 remains dominant in some areas [9].
                             Some studies have suggested that serotypes ST11-KL47 and ST11-KL64 have an evo-
                       lutionary relationship, and recombinant mutations have occurred in ST11-KL47 strains,
                       resulting in serotype conversion to KL64 [10]. ST11-KL64 CRKP carried the virulence
                       genes (rmpA/rmpA2, iucABCD and iutA), and the presence of these virulence genes could
                       be linked to the transformation of KL47 into KL64.
                             To investigate the genomic differences and evolutionary mechanisms between the
                       two serotypes, we performed a study based on screening and analyzing ST11 CRKP ge-
                       nomic data sourced from the Pathosystems Resource Integration Center (PATRIC) [11]
                       database between 2011 to 2020.

                       2. Materials and Methods
                       2.1. Data Sources
                            All K. pneumoniae genome sequences from 2011 to 2020 were collected from the
                       PATRIC database, which was screened based on the host, sample sources, presence of the
                       carbapenemase-encoding gene, and isolation nation. A human host, eight sample sources
                       (blood, urine, feces, bronchoalveolar lavage, respiratory secretions, wound pus, catheter,
                       and sterile body fluids), and carriage of any one of the carbapenemase-encoding genes
                       (including blaKPC, blaNDM, blaVIM, blaIMP, etc.) were used as inclusion criteria. As the number
                       of KL47 and KL64 serotypes did not change significantly over a short period of time, such
                       as one year, whereas the change in the dominance of KL47 and KL64 serotypes in ST11
                       CRKP over five years was more intuitive, and thus the samples were divided into two
                       periods for comparison: 2011–2015 and 2016–2020.

                       2.2. Analysis of Virulence Genes, Resistance Genes, and Plasmids
                            The strains were identified and screened for carrying carbapenemase-encoding genes
                       using Kleborate [12] software. The number of virulence genes, resistance genes, and plas-
                       mids carried by each strain were determined by comparing with CARD [13], VFDB [14],
                       and Plasmid Finder [15] databases using Abricate software, and genome annotation was
                       performed using Prokka v1.12 [16].

                       2.3. Bioinformatics Analysis
                            Core genome alignment was obtained using Roray v3.13.0 [17], single nucleotide pol-
                       ymorphism (SNP) recombination analysis was performed using snippy, the recombina-
                       tion results were combined and the best model was calculated using modeltest-ng, while
                       the maximum likelihood tree was drawn using raxml-ng afterward, and the phylogenetic
                       tree obtained by the maximum likelihood method was used along with the recombination
                       data using ClonalFrameML v1.12 [18] to deconstruct and obtain the reconstructed images.
                       The phylogenetic tree was displayed using iqtree v2.2.0.3 [19]. Jalview v2.11.2.2 [20,21]
Genes 2022, 13, 1624                                                                                            3 of 12




                       was used for alignment display, and a comparison of KL47 and KL64 representative
                       strains with wzc genes was performed using blast v2.13.0, and visualized by CGview [22].

                       2.4. Differential Gene Analysis
                            GO enrichment analysis of virulence genes with statistically significant differences in
                       the number of virulence genes between KL47 and KL64 CRKP was performed using DA-
                       VID [23] software, and bubble plots were generated using R version 4.2.0 (R Core Team.
                       R: A language and environment for statistical computing. R Foundation for Statistical
                       Computing, Vienna, Austria; 2022. URL: https://www.R-project.org/ (accessed on 10 May
                       2022)).

                       2.5. Statistical Analysis
                             Statistical analysis was performed using R version 4.2.0 (R Core Team. R: A language
                       and environment for statistical computing. R Foundation for Statistical Computing, Vi-
                       enna, Austria; 2022. URL: https://www.R-project.org/ (accessed on 10 May 2022)). Firstly,
                       the numbers of virulence genes, resistance genes, and plasmids carried by KL47 and KL64
                       CRKP were compared. Continuous variables that met normality were described using the
                       mean ± standard deviation, and differences between the two groups were compared using
                       the two independent samples t-test. If continuous variables did not meet normality, they
                       were described using the median (interquartile), and non-parametric tests (Mann–Whit-
                       ney-U test) were used to compare differences between groups. The chi-square test of in-
                       dependence was used to compare the differences in the proportions of resistance or viru-
                       lence genes in different groups. When one or more cell counts in a 2 × 2 table were less
                       than 5, Fisher’s exact test was used. A p-value < 0.05 was considered statistically signifi-
                       cant.

                       3. Results
                       3.1. Clinical and Molecular Characterizations of ST11 CRKP
                             There were 2356 CRKP genome assemblies obtained after database screening, includ-
                       ing 1620 CRKPs from 2011 to 2015, and 736 CRKPs from 2016 to 2020. There were 165
                       (10.19%, 165/1620) ST11 CRKP genome assemblies in 2011–2015, and 221 (30.03%, 221/736)
                       ST11 CRKP genome assemblies in 2016–2020, the information of 386 ST11 CRKP strains
                       was in Supplementary Table S1. In total, blood samples accounted for 31.09% (120/386) of
                       all sample sources, while the proportions of respiratory fluids, feces, urine, wound pus,
                       alveolar lavage fluid, sterile body fluids, and catheter samples were 23.06% (89/386),
                       20.21% (78/386), 18.39% (71/386), 2.85% (11/386), 2.07% (8/386), 1.30% (5/386), and 1.04%
                       (4/386), respectively. Between 2011 and 2015, the top three carbapenemase genes were
                       blaKPC-2 (84.24%, 139/165), blaNDM-1 (6.06%, 10/165), and blaOXA-48 (3.03%, 5/165). From 2016 to
                       2020, the top three carbapenemase genes were blaKPC-2 (81.45%, 180/221), blaNDM-1 (8.60%,
                       19/221), and blaOXA-48 (4.52%, 10/221). In total, 386 ST11 CRKP strains belonged to 51 sero-
                       types, including 20 serotypes during 2011–2015, and 36 serotypes during 2016–2020. KL47
                       was the predominated serotype (44.85%, 74/165) and KL64 made up 10.91% (18/165) of all
                       serotypes in the first five years. During 2016–2020, KL64 accounted for 47.06% (104/221),
                       while KL47 accounted for 16.74% (37/221) of all serotypes. (Figure 1).
Genes 2022, 13, 1624                                                                                               4 of 12




                       Figure 1. Serotype variation over 10 years. ST11 CRKP serotype distribution in 2011–2015; ST11
                       CRKP serotype distribution in 2016–2020. Unknown (KL64), an unknown serotype similar to KL64,
                       and other unknown serotypes are indicated as well.

                            There were 111 KL47 CRKP, and the proportions of blood samples, respiratory secre-
                       tions, urine, feces, wound pus, bronchoalveolar lavage, catheter, and sterile body fluids
                       were 31.53% (35/111), 25.23% (28/111), 18.92% (21/111), 16.22% (18/111), 3.60% (4/111),
                       1.80% (2/111), 1.80% (2/111), and 0.90% (1/111), respectively. The main country sources of
                       KL47 were China (59.46%, 66/111) and Brazil (9.91%, 11/111), and the highest numbers
                       were from the years 2016 (27.03%, 30/111) and 2018 (20.72%, 23/111). There were 122 KL64
                       CRKP, and the proportions of blood, feces, respiratory secretions, urine, catheter, sterile
                       bodily fluids, wound pus, and bronchoalveolar lavage were 36.89% (45/122), 27.87%
                       (34/122), 17.21% (21/122), 14.75% (18/122), 1.64% (2/122), 0.82% (1/122), 0.82% (1/122), and
                       0, respectively. The majority of the strains collected from 2011 to 2020 were from China
                       (64.51%, 249/386), Brazil (9.84%, 38/386), and the United States (8.55%, 33/386), with the
                       most strains being collected in the years 2015 (18.13%, 70/386) and 2016 (23.58%, 91/386).

                       3.2. Presence of Carbapenem Resistance and Virulence Genes in KL47 and KL64.
                            A total of five kinds of carbapenemase genes were identified in the KL47 CRKP
                       strains, including blaKPC-2 (96.40%, 107/111), blaNDM-1 (1.80%, 2/111), blaNDM-5 (0.90%, 1/111),
                       blaVIM-1 (0.90%, 1/111), and blaOXA-245 (0.90%, 1/112). Thirty-four KL47 CRKP strains carried
                       the virulence genes iucABCD/iutA, fifteen KL47 CRKP strains carried rmpA genes and
                       thirty-three KL47 CRKP strains carried rmpA2 genes. Four carbapenemase genes were
                       present in the KL64 CRKP strains, including blaKPC-2 (97.54%, 119/122), blaOXA-181 (1.64%,
                       2/122), blaOXA-48 (0.82%, 1/122), and blaKPC-30 (0.82%, 1/122). A total of 50.00% (61/122) of
                       KL64 CRKP strains carried iucCD/iutA, while 50.82% (62/122) of KL64 CRKP carried iu-
                       cAB. The KL64 and KL47 carried equivalent numbers of resistance genes [median 15
                       (P25~P75: 14~18)]. However, the ST11-KL64 CRKP [median 78(P25~P75: 72~79.25)] had re-
                       markably more virulence genes than the ST11-KL47 CRKP strains [median 63(P25~P75:
                       63~69)] (p < 0.001). In comparison to ST11-KL64 CRKP [median 3(P25~P75: 3~4)], ST11-KL47
                       CRKP carried more plasmids [median 4(P25~P75: 3~4)] (p < 0.003) (Table 1).

                       Table 1. Comparison of differences in the number of resistance genes, virulence genes, and plasmids
                       carried between KL47 and KL64 CRKP.

                                                                                 Group
                                      Variables                                                              p-Value
                                                                         KL47                KL64
Genes 2022, 13, 1624                                                                                          5 of 12




                                                                      n = 111               n = 122
                         Number of Cabarpenemase genes               15 (14, 18)          15 (14, 18)     0.380
                             Number of plasmids                        4 (3, 4)             3 (3, 4)      0.003
                           Number of virulence genes                 63 (63, 69)         78 (72, 79.25)   <0.001

                       3.3. Comparison of the Virulence Genes Distribution between KL47 and KL64
                            To determine the differences in virulence genes carried by KL47 and KL64, we exam-
                       ined the 134 virulence genes carried by both ST11-KL47 and ST11-KL64 in the VFDB da-
                       tabase. As a result, the proportions of 35 virulence genes were significantly different be-
                       tween the KL47 and KL64 strains (p < 0.05) (Table 2). The wbbM, wbbN, wbbO, wzm, and
                       wzt genes are lipopolysaccharide-related genes that play a role in O-antigen processing,
                       lipopolysaccharide synthesis, and virulence evolution. All the ST11-KL47 strains carry the
                       entF gene, while 92.62% (113/122) of the ST11-KL64 strains carry this gene. More ST11-
                       KL64 strains carry the glf (95.90%, 117/122) and gnd (100%, 122/122) genes. The entF gene
                       is a cytoplasmic enzyme for making siderophore enterobactin. The glf gene is a capsule
                       biosynthesis gene that is essential for capsule biosynthesis. The gnd gene is a gluconate
                       dehydrogenase gene and has a highly variable nucleotide sequence that plays a facilitat-
                       ing role in virulence evolution. The carriage of gnd and glf in ST11-KL64 strains might play
                       an important role in the evolution of virulence.

                       Table 2. Differential of virulence genes between KL47 and KL64.

                                                                          Group
                                  Virulence Genes                    KL47        KL64             χ2         p
                                                                    n = 111     n = 122
                                          acrA                        105         122           4.786     0.029
                                          clbA                         1          19           15.946     <0.001
                         clbB/clbC/clbD/clbE/clbF/clbG/clbH            1          20           17.011     <0.001
                                    clbI/clbN/clbO                     1          19           15.946     <0.001
                              clbL/clbM/clbP/clbQ/clbS                 1          20           17.011     <0.001
                                          entF                        111         113           6.647     0.010
                                           glf                         3          117          202.116    <0.001
                                           gnd                         3          122          221.262    <0.001
                                          iucA                        32          60           10.075     0.002
                                          iucB                        34          62            9.779     0.002
                                   iucC/iucD/iutA                     34          61            9.030     0.003
                                          mrkI                        101         121           8.665     0.003
                                         rmpA                          1          45           47.497     <0.001
                                        rmpA2                         30          59           11.205     0.001
                                          senB                         0           8            5.689     0.017
                                       vipA/tssB                      106         73            41.509    <0.001
                                         wbbM                          0          114          203.085    <0.001
                                         wbbN                          0          117          213.819    <0.001
                                         wbbO                          0          110          189.586    <0.001
                                          wzm                          0          118          217.522    <0.001
                                           wzt                         0          117          213.819    <0.001

                            Fourteen genes were discovered to be enriched in five pathways after the aforemen-
                       tioned thirty-five differential genes were subjected to GO enrichment analyses. In the
                       GO:0019290 pathway (Figure 2), which contains the chemical reaction and process leading
                       to the creation of iron carriers produced by aerobic or parthenogenic anaerobic bacteria
                       with low molecular weight Fe (III) integrators, the iron carrier genes iucABCD and iutA
                       are primarily enriched. Clb is an ICEKp-associated pathogenicity locus that is enriched in
Genes 2022, 13, 1624                                                                                                6 of 12




                       three pathways, including transferase activity, transferring acyl groups, phosphopan-
                       tetheine binding, and ligase activity. The iro, iuc, rmpA, and rmpA2 are loci associated with
                       pathogenic plasmids, and KL64 CRKP strains carry more genes, including Clb, iro, iuc,
                       rmpA, and rmpA2 genes, the difference being statistically significant. It is hypothesized
                       that ST11-KL64 CRKP contains more virulence genes than KL47 due to iron carrier-asso-
                       ciated chemical reactions that promote bacterial growth, reproduction, and virulence
                       spread, as well as the pathogenicity locus gene Clb, which plays an important role in vir-
                       ulence evolution. Some studies have confirmed that these genes in ST11-KL64 strains
                       arose during recombination due to the gain or loss of gene clusters involved in heavy
                       metal resistance and mobile genetic elements, as a manifestation of the evolution of ST11-
                       KL47 to ST11-KL64 after a recombination event [10].




                       Figure 2. GO analysis of differential genes. Thirty-five differentially virulent genes were included
                       in the GO enrichment analysis using DAVID software, and bubble plots were visualized using R
                       v4.2.0.

                       3.4. Serotype Evolutionary Characterization of ST11 CRKP
                            All the 386 ST11 CRKP strains can be divided into 9 clades in the phylogenetic tree.
                       KL125 belonged to the original evolutionary serotype of ST11 strains, followed by KL14
                       and KL24; then, KL105 and KL27 underwent evolutionary mutations to evolve into the
                       currently popular serotypes, including KL64, KL47, K21, etc. Most of these unknown sero-
                       types shared sequence similarities with KL107, indicating that KL107 represents an inter-
                       mediate type from which several strains have evolved. China submitted 249 CRKP strains
                       with 33 serotypes and the maximum number of CRKP strains (64.25%, 248/386), according
                       to an analysis of the phylogeny of ST11-CRKP strains from different nations around the
                       world (Figure 3). Strains from the same period and geographical area show more homol-
                       ogy in phylogenetic branches. Some CRKP strains from different regions also show a high
                       degree of evolutionary homology, suggesting that the evolution of CRKP strains needs to
                       be considered from a global perspective.
Genes 2022, 13, 1624   7 of 12
Genes 2022, 13, 1624                                                                                                 8 of 12




                       Figure 3. Phylogenetic tree of 386 ST11 CRKP strains. The phylogenetic tree is colored according to
                       the different serotypes. The country of collection, year of collection, and sample type of each strain
                       are annotated with color.

                            Our analysis of SNP recombination events between ST11 CRKP strains revealed that
                       KL47 and KL64 in the same large clade were highly similar in the locations where recom-
                       bination occurred (Figure 4). In contrast, KL64 had only two more recombination regions
                       (249514-250776, 1119662-1120610) than KL47, which carried 6 and 5 SNPs, respectively.




                       Figure 4. Recombination analysis of 386 ST11 CRKP isolates. Recombinant genomic regions (RD1
                       and RD2) were predicted by Gubbins and visualized by Phandango.

                            To verify the relationship between KL47 and KL64, we drew a phylogenetic tree and
                       visualized the recombination regions. As a result, the 233 KL47 and KL64 CRKP strains
                       could be divided into a total of five clades, with all KL47 CRKP located in one large clade
                       and the closest related KL64 CRKP showing more recombinant nucleotide sequence mu-
                       tations (Figure 5).




                       Figure 5. Phylogenetic and recombination analysis of KL47 and KL64. Images drawn with Clon-
                       alFrameML. The 233 strains of KL47 and KL64 CRKP can be divided into a total of 5 clades; KL47
                       CRKP all located in a large clade. The blue boxed area on the right side of the graph corresponds to
                       the recombination of each strain in the region of positions 1 × 106 to 3 × 106 .
Genes 2022, 13, 1624                                                                                                9 of 12




                       3.5. The Potential Mechanisms for the Evolution of ST11 CRKP from KL47 to KL64
                             We first compared the nucleotide sequence of KL47 and KL64 in the VR2 variable
                       region and discovered that the KL64 strains possess more nucleotide sequences in this
                       region, indicating that mutations occurred by increasing the number of nucleotide se-
                       quences in the VR2 variable region of the wzc gene based on KL47, facilitating the serotype
                       shift. The nucleotide sequence profile of the wzc gene in the CD1-VR2-CD2 region directly
                       affects the serotype (Figure 6A). The variation in the serotype-determining wzc gene is
                       essentially the same in strains ST11-KL47 and ST11-KL64 of the same serotypes. We se-
                       lected two strains with complete genome sequences in ST11-KL47 and ST11-KL64, which
                       are highly representative and can provide more reliable results. Representative strains
                       573.19986 and 573.25802 were chosen for KL47 and KL64, respectively.




                       Figure 6. Serotype comparison of KL47 and KL64. (A) Baseline comparison of the CRKP VR2 varia-
                       ble region in KL47 and KL64; (B) Sequence characteristics of KL47 and KL64 in the wzc gene’s CD1-
                       VR2-CD2 region. KL64 CRKP has more nucleotide sequences in the VR2 region. The region of KL47
                       alignment re-sults in two sequences of 1491 bp and 342 bp, respectively, with a total of 1835 bp and
                       a GC content of 53.84%, while the KL64 CRKP obtained a sequence of 2138 bp after alignment with
                       the wzc gene, with a GC content of 58.14%.

                            The region of KL47 compared to the wzc gene produced two sequences of 1491 base
                       pairs (bp) and 342 bp, totaling 1835 bp, with a GC content of 53.84%, whereas the KL64
                       CRKP compared to the wzc gene produced a sequence of 2138 bp, with a GC content of
                       58.14% (Figure 6B). The nucleotide sequence length in the CD1-VR2-CD2 region of KL64
                       CRKP was increased by around 303 bp compared to KL47, and it had a greater GC content,
                       which encouraged the mutation of the serotype from KL47 to KL64. After Prokka annota-
                       tion, we discovered that the cps area contained a particular tyrosine-protein kinase (Puta-
                       tive tyrosine-protein kinase in cps region), leading us to believe that the recombination
                       events took place at the Capsular biosynthesis site.

                       4. Discussion
                            Compared with previous studies [24–26], our global investigation of ST11 CRKP over
                       10 years demonstrated a gradual unification of the most prevalent clonal strains of car-
                       bapenem-resistant K. pneumoniae bearing blaKPC-2 in a dominant position. Blood was the
                       predominant sample type in our collection of ST11 CRKP, while China was one of the
Genes 2022, 13, 1624                                                                                       10 of 12




                       main country sources of the strains, suggesting that the transmission of CRKP in the blood
                       is common worldwide, especially in China, and requires more attention. In addition,
                       blaNDM-1 and blaOXA-48 are significant carbapenemase genes in ST11 CRKP, while the clonal
                       spread of blaOXA-48, blaKPC-2, and blaCTX-M-14 was responsible for the outbreak of ST11 CRKP
                       over a long period [27]. Most ST11 CRKP strains were found in China between 2011 and
                       2020 [28], demonstrating that serotypes of ST11-KL47 and ST11-KL64 are evolving and
                       spreading more quickly there. Comparison to previous studies found that ST11-KL47 and
                       ST11-KL64 CRKP have become dominant prevalent variants that cannot be disregarded
                       and require attention. In our study, ST11-KL64 CRKP has been spreading worldwide and
                       has begun to displace KL47 as the predominant serotype of ST11 CRKP, which was similar
                       to a previous study [10]. KL47 could evolve into KL47 and KL64, a phenomenon known
                       as transmission evolution [26]. It is undeniable that the evolution of KL47 to KL64 is grad-
                       ually becoming the mainstream trend, and ST11-KL64 CRKP will account for an increas-
                       ing proportion of all ST11 types. Additionally, KL64 is linked to high virulence [29], sug-
                       gesting that ST11 carbapenem-resistant K. pneumoniae is evolving into a highly virulence
                       strain.
                             Previous research has shown that the rmpA/rmpA2, iucABCD, and iutA genes were
                       present in all ST11-KL64 CRKP. By examining 122 strains of ST11-KL64 CRKP, we found
                       that the percentage of these genes carried varied between 36.89 and 50.82 percent when
                       the Kleborate software identified the strain as ST11-KL64 CRKP. It is worth noting that
                       ST11-KL64 strains carrying rmpA/rmpA2, iucABCD, and iutA genes all harbored the blaKPC-
                       2 gene, and were only isolated from Chinese samples.

                             It was found that ST11-KL64 CRKP carried more virulence genes [median 78 (P25~P75:
                       72~79.25)] than KL47 [median 63 (P25~P75: 63~69)]. A comparison of the two serotypes re-
                       garding the number of 134 virulence genes carried revealed 35 virulence genes with sta-
                       tistically significant differences, including rmpA/rmpA2, iucABCD, iutA genes, etc., con-
                       firming that these virulence genes were differential genes between the two serotypes
                       ST11-KL64 and ST11-KL47, consistent with previous studies [10]. Furthermore, it has been
                       demonstrated that high virulence genes carrying KL47 and KL64 CR-hvKP exhibit a high
                       level of clonality [30], confirming the evolutionary advantage of propagation when high
                       virulence genes and carbapenem resistance genes co-exist.
                             There are variable numbers of virulence genes and plasmids in the ST11-KL47 and
                       ST11-KL64 CRKP. The CD1-VR2-CD2 region of the wzc gene exhibits a nucleotide se-
                       quence increase of about 303 bp in KL64, as well as a better GC content, which facilitates
                       the transformation from KL47 to KL64. The evolution of the serotype to KL64 likely re-
                       sulted from mutations in various regions of the nucleotide sequence, and KL64 CRKP it-
                       self underwent recombination in specific regions during evolution, leading to the produc-
                       tion of certain virulence genes such as rmpA2, iucABCD, etc., rather than the acquisition
                       of more virulence genes or plasmids leading to the evolution of the serotype to KL64 [24].
                             Our research has certain limitations. Firstly, only the PATRIC database was used for
                       sample screening, and there was insufficient diversity among the CRKP strains included
                       in the study. Secondly, there were no related experiments performed to demonstrate the
                       effect of recombination of particular region fragments on the transformation of KL47 into
                       KL64. However, in this study, we characterized ST11 CRKP strains from across the globe.
                       At the same time, the evolutionary mechanisms of the serotypes of ST11-KL47 and ST11-
                       KL46 were studied in depth, which can be used as a reference for evolutionary studies of
                       KL47 to KL64.
                             In summary, we found that KL47 and KL64 were the main serotypes of ST11 K. pneu-
                       moniae. KL47 and KL64 belong to a large evolutionary branch, and KL47 is the evolution-
                       ary ancestor of KL64. Comparative analysis of differential genes revealed that ST11-KL64
                       carries multiple virulence genes that might arise from a recombination process. In addi-
                       tion, KL64 CRKP carried 303 bp more nucleotide sequences in the CD1-VR2-CD2 region
                       with higher GC content (58.14%) than KL47 CRKP, which facilitated the evolution of the
Genes 2022, 13, 1624                                                                                                            11 of 12




                                  serotype toward KL64. The discovery that mobile genetic elements play a role in the evo-
                                  lution of recombination provides a new basis for exploring the evolutionary process of the
                                  ST11-KL64 CRKP [10].

                                  Supplementary Materials: The following supporting information can be downloaded at:
                                  https://www.mdpi.com/article/10.3390/genes13091624/s1, Table S1. Genomic information of 386
                                  ST11 CRKP strains.
                                  Author Contributions: Conceptualization, N.Z. and Y.C.; Data curation, N.Z., Y.T., X.Y., M.J., J.C.,
                                  S.Q. and F.L.; Formal analysis, N.Z.; Funding acquisition, Y.C.; Methodology, N.Z. and J.G.; Project
                                  administration, Y.C.; Software, N.Z. and X.L.; Supervision, C.W. and Y.C.; Visualization, N.Z.; Writ-
                                  ing—original draft, N.Z. and Y.T.; Writing—review and editing, N.Z., Y.T. and Y.C. All authors
                                  have read and agreed to the published version of the manuscript.
                                  Funding: This research was funded by a grant from National Key Program for Infectious Diseases
                                  of China (2018ZX10733-402) and Beijing Nova Program (Z181100006218107), and the APC was
                                  funded by a grant from National Key Program for Infectious Diseases of China (2018ZX10733-402).
                                  Institutional Review Board Statement: It’s “Not applicable” for studies not involving humans or
                                  animals.
                                  Data Availability Statement: Genomic data for 386 ST11 CRKP downloaded from the Pathosystems
                                  Resource Integration Center (PATRIC) are shown in Supplementary Table S1.
                                  Acknowledgments: We are grateful to the PATRIC database (https://patricbrc.org/ (accessed on 20
                                  April 2022)) for providing the genomic data of K. pneumoniae.
                                  Conflicts of Interest: The authors have no conflicts of interest to declare.

References
1.    Xu, J.; Zhao, Z.; Ge, Y.; He, F. Rapid Emergence of a Pandrug-Resistant Klebsiella pneumoniae ST11 Isolate in an Inpatient in a
      Teaching Hospital in China After Treatment with Multiple Broad-Spectrum Antibiotics. Infect. Drug Resist. 2020, 13, 799–804.
2.    Zhao, Y.; Zhang, X.; Torres, V.V.L.; Liu, H.; Rocker, A.; Zhang, Y.; Wang, J.; Chen, L.; Bi, W.; Lin, J.; et al. An Outbreak of
      Carbapenem-Resistant and Hypervirulent Klebsiella pneumoniae in an Intensive Care Unit of a Major Teaching Hospital in Wen-
      zhou, China. Front. Public Health 2019, 7, 229.
3.    Munoz-Price, L.S.; Poirel, L.; Bonomo, R.A.; Schwaber, M.J.; Daikos, G.L.; Cormicanm, M.; Cornaglia, G.; Garau, J.; Gniadkow-
      ski, M.; Hayden, MK.; et al. Clinical epidemiology of the global expansion of Klebsiella pneumoniae carbapenemases. Lancet Infect.
      Dis. 2013, 13, 785–796.
4.    Agyeman, A.A.; Bergen, P.J.; Rao, G.G.; Nation, R.L.; Landersdorfer, C.B. A systematic review and meta-analysis of treatment
      outcomes following antibiotic therapy among patients with carbapenem-resistant Klebsiella pneumoniae infections. Int. J. Antimi-
      crob. Agents 2020, 55, 105833.
5.    Gu, D.; Dong, N.; Zheng, Z.; Lin, D.; Huang, M.; Wang, L.; Chan, E.W.; Shu, L.; Yu, J.; Zhang, R.; et al. A fatal outbreak of ST11
      carbapenem-resistant hypervirulent Klebsiella pneumoniae in a Chinese hospital: A molecular epidemiological study. Lancet In-
      fect. Dis. 2018, 18, 37–46.
6.    Dong, N.; Zhang, R.; Liu, L.; Li, R.; Lin, D.; Chan, E.W.; Chen, S. Genome analysis of clinical multilocus sequence Type 11
      Klebsiella pneumoniae from China. Microb. Genom. 2018, 4, e000149.
7.    Pan, Y.J.; Lin, T.L.; Chen, Y.H.; Hsu, C.R.; Hsieh, P.F.; Wu, M.C.; Wang, J.T. Capsular types of Klebsiella pneumoniae revisited by
      wzc sequencing. PLoS ONE 2013, 8, e80670.
8.    Zhao, J.; Liu, C.; Liu, Y.; Zhang, Y.; Xiong, Z.; Fan, Y.; Zou, X.; Lu, B.; Cao, B. Genomic characteristics of clinically important
      ST11 Klebsiella pneumoniae strains worldwide. J. Glob. Antimicrob. Resist. 2020, 22, 519–526.
9.    Guo, L.; Wang, L.; Zhao, Q.; Ye, L.; Ye, K.; Ma, Y.; Shen, D.; Yang, J. Genomic Analysis of KPC-2-Producing Klebsiella pneumoniae
      ST11 Isolates at the Respiratory Department of a Tertiary Care Hospital in Beijing, China. Front. Microbiol. 2022, 13, 929826.
10.   Zhou, K.; Xiao, T.; David, S.; Wang, Q.; Zhou, Y.; Guo, L.; Aanensen, D.; Holt, K.E.; Thomson, NR.; Grundmann, H.; et al. Novel
      Subclone of Carbapenem-Resistant Klebsiella pneumoniae Sequence Type 11 with Enhanced Virulence and Transmissibility,
      China. Emerg. Infect. Dis. 2020, 26, 289–297.
11.   Gillespie, J.J.; Wattam, A.R.; Cammer, S.A.; Gabbard, J.L.; Shukla, M.P.; Dalay, O.; Driscoll, T.; Hix, D.; Mane, S.P.; Mao, C.; et
      al. PATRIC: The comprehensive bacterial bioinformatics resource with a focus on human pathogenic species. Infect. Immun.
      2011, 79, 4286–4298.
12.   Lam, M.M.C.; Wick, R.R.; Watts, S.C.; Cerdeira, L.T.; Wyres, K.L.; Holt, K.E. A genomic surveillance framework and genotyping
      tool for Klebsiella pneumoniae and its related species complex. Nat. Commun. 2021, 12, 4188.
Genes 2022, 13, 1624                                                                                                               12 of 12




13.   Jia, B.; Raphenya, A.R.; Alcock, B.; Waglechner, N.; Guo, P.; Tsang, K.K.; Lago, B.A.; Dave, B.M.; Pereira, S.; Sharma, A.N.; et al.
      CARD 2017: Expansion and model-centric curation of the comprehensive antibiotic resistance database. Nucleic Acids Res. 2017,
      45, D566–D573.
14.   Chen, L.; Zheng, D.; Liu, B.; Yang, J.; Jin, Q. VFDB 2016: Hierarchical and refined dataset for big data analysis–10 years on.
      Nucleic Acids Res. 2016, 44, D694–D697.
15.   Carattoli, A.; Zankari, E.; García-Fernández, A.; Voldby, Larsen. M.; Lund, O.; Villa, L.; Møller, Aarestrup. F.; Hasman, H. In
      silico detection and typing of plasmids using PlasmidFinder and plasmid multilocus sequence typing. Antimicrob. Agents
      Chemother. 2014, 58, 3895–3903.
16.   Seemann, T. Prokka: Rapid prokaryotic genome annotation. Bioinformatics 2014, 30, 2068–2069.
17.   Page, A.J.; Cummins, C.A.; Hunt, M.; Wong, V.K.; Reuter, S.; Holden, M.T.; Fookes, M.; Falush, D.; Keane, J.A.; Parkhill, J. Roary:
      Rapid large-scale prokaryote pan genome analysis. Bioinformatics 2015, 31, 3691–3693.
18.   Didelot, X.; Wilson, D.J.; ClonalFrame, M.L. Efficient inference of recombination in whole bacterial genomes. PLoS Comput. Biol.
      2015, 11, e1004041.
19.   Nguyen, L.T.; Schmidt, H.A.; von Haeseler, A.; Minh, B.Q. IQ-TREE: A fast and effective stochastic algorithm for estimating
      maximum-likelihood phylogenies. Mol. Biol. Evol. 2015, 32, 268–274.
20.   Procter, J.B.; Carstairs, G.M.; Soares, B.; Mourão, K.; Ofoegbu, T.C.; Barton, D.; Lui, L.; Menard, A.; Sherstnev, N.; Roldan-Mar-
      tinez, D.; et al. Correction to: Alignment of Biological Sequences with Jalview. Methods Mol. Biol. 2021, 2231, C1.
21.   Waterhouse, A.M.; Procter, J.B.; Martin, D.M.; Clamp, M.; Barton, G.J. Jalview Version 2—a multiple sequence alignment editor
      and analysis workbench. Bioinformatics 2009, 25, 1189–1191.
22.   Grant, J.R.; Stothard, P. The CGView Server: A comparative genomics tool for circular genomes. Nucleic Acids Res. 2008, 36,
      W181–W184.
23.   Sherman, B.T.; Hao, M.; Qiu, J.; Jiao, X.; Baseler, M.W.; Lane, H.C.; Imamichi, T.; Chang, W. DAVID: A web server for functional
      enrichment analysis and functional annotation of gene lists (2021 update). Nucleic Acids Res. 2022, 50, W216–W221.
24.   Zhao, D.; Shi, Q.; Hu, D.; Fang, L.; Mao, Y.; Lan, P.; Han, X.; Zhang, P.; Hu, H.; Wang, Y.; et al. The Emergence of Novel Sequence
      Type Strains Reveals an Evolutionary Process of Intraspecies Clone Shifting in ICU-Spreading Car-bapenem-Resistant Klebsiella
      pneumoniae. Front. Microbiol. 2021, 12, 691406.
25.   Gu, B.; Bi, R.; Cao, X.; Qian, H.; Hu, R.; Ma, P. Clonal dissemination of KPC-2-producing Klebsiella pneumoniae ST11 and ST48
      clone among multiple departments in a tertiary teaching hospital in Jiangsu Province, China. Ann. Transl. Med. 2019, 7, 716.
26.   Lin, D.; Chen, J.; Yang, Y.; Cheng, J.; Sun, C. Epidemiological Study of Carbapenem-resistant Klebsiella Pneumoniae. Open Med.
      2018, 13, 460–466.
27.   Chen, CM.; Guo, MK.; Ke, S.C.; Lin, Y.P.; Li, C.R.; Vy Nguyen, H.T.; Wu, L.T. Emergence and nosocomial spread of ST11 car-
      bapenem-resistant Klebsiella pneumoniae co-producing OXA-48 and KPC-2 in a regional hospital in Taiwan. J. Med. Microbiol.
      2018, 67, 957–964.
28.   Liu, J.; Yu, J.; Chen, F.; Yu, J.; Simner, P.; Tamma, P.; Liu, Y.; Shen, L. Emergence and establishment of KPC-2-producing ST11
      Klebsiella pneumoniae in a general hospital in Shanghai, China. Eur. J. Clin. Microbiol. Infect. Dis. 2018, 37, 293–299.
29.   Wei, T.; Zou, C.; Qin, J.; Tao, J.; Yan, L.; Wang, J.; Du, H.; Shen, F.; Zhao, Y.; Wang, H. Emergence of Hypervirulent ST11-K64
      Klebsiella pneumoniae Poses a Serious Clinical Threat in Older Patients. Front. Public Health 2022, 10, 765624.
30.   Ouyang, P.; Jiang, B.; Peng, N.; Wang, J.; Cai, L.; Wu, Y.; Ye, J.; Chen, Y.; Yuan, H.; Tan, C.; et al. Characteristics of ST11 KPC-2-
      producing carbapenem-resistant hypervirulent Klebsiella pneumoniae causing nosocomial infection in a Chinese hospital. J. Clin.
      Lab. Anal. 2022, 36, e24476.
