# Singh et al. 2018 — pdftotext fallback extraction

> **Provenance**: local `pdftotext -layout` from `paper.pdf` (sha256=894bb7d7b692236da82026d65b98c328697abb5be0cce3b63780ebdf897c02c7).
> Central Marker corpus lookup on Eagle/Polaris: not reachable at backfill time.
> This is a plaintext fallback; not a Marker parse. Replace with the Eagle Marker .md
> when the central corpus sweep resolves this sha256.

Singh et al. BMC Microbiology     (2018) 18:175
https://doi.org/10.1186/s12866-018-1325-2




 RESEARCH ARTICLE                                                                                                                                Open Access

Multi-drug resistant Enterobacter
bugandensis species isolated from the
International Space Station and
comparative genomic analyses with human
pathogenic strains
Nitin K. Singh1†, Daniela Bezdan2†, Aleksandra Checinska Sielaff1,6, Kevin Wheeler3, Christopher E. Mason2,4,5
and Kasthuri Venkateswaran1*


  Abstract
  Background: The antimicrobial resistance (AMR) phenotypic properties, multiple drug resistance (MDR) gene
  profiles, and genes related to potential virulence and pathogenic properties of five Enterobacter bugandensis strains
  isolated from the International Space Station (ISS) were carried out and compared with genomes of three clinical
  strains. Whole genome sequences of ISS strains were characterized using the hybrid de novo assembly of Nanopore
  and Illumina reads. In addition to traditional microbial taxonomic approaches, multilocus sequence typing (MLST)
  analysis was performed to classify the phylogenetic lineage. Agar diffusion discs assay was performed to test
  antibiotics susceptibility. The draft genomes after assembly and scaffolding were annotated with the Rapid
  Annotations using Subsystems Technology and RNAmmer servers for downstream analysis.
  Results: Molecular phylogeny and whole genome analysis of the ISS strains with all publicly available Enterobacter
  genomes revealed that ISS strains were E. bugandensis and similar to the type strain EB-247T and two clinical
  isolates (153_ECLO and MBRL 1077). Comparative genomic analyses of all eight E. bungandensis strains showed, a
  total of 4733 genes were associated with carbohydrate metabolism (635 genes), amino acid and derivatives (496
  genes), protein metabolism (291 genes), cofactors, vitamins, prosthetic groups, pigments (275 genes), membrane
  transport (247 genes), and RNA metabolism (239 genes). In addition, 112 genes identified in the ISS strains were
  involved in virulence, disease, and defense. Genes associated with resistance to antibiotics and toxic compounds,
  including the MDR tripartite system were also identified in the ISS strains. A multiple antibiotic resistance (MAR)
  locus or MAR operon encoding MarA, MarB, MarC, and MarR, which regulate more than 60 genes, including
  upregulation of drug efflux systems that have been reported in Escherichia coli K12, was also observed in the ISS
  strains.
  (Continued on next page)




* Correspondence: kjvenkat@jpl.nasa.gov
†
 Nitin K. Singh and Daniela Bezdan contributed equally to this work.
1
 Biotechnology and Planetary Protection Group, Jet Propulsion Laboratory,
California Institute of Technology, M/S 89–2 4800 Oak Grove Dr, Pasadena,
CA 91109, USA
Full list of author information is available at the end of the article

                                        © The Author(s). 2018 Open Access This article is distributed under the terms of the Creative Commons Attribution 4.0
                                        International License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and
                                        reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to
                                        the Creative Commons license, and indicate if changes were made. The Creative Commons Public Domain Dedication waiver
                                        (http://creativecommons.org/publicdomain/zero/1.0/) applies to the data made available in this article, unless otherwise stated.
Singh et al. BMC Microbiology     (2018) 18:175                                                                  Page 2 of 13




 (Continued from previous page)
 Conclusion: Given the MDR results for these ISS Enterobacter genomes and increased chance of pathogenicity
 (PathogenFinder algorithm with > 79% probability), these species pose important health considerations for future
 missions. Thorough genomic characterization of the strains isolated from ISS can help to understand the
 pathogenic potential, and inform future missions, but analyzing them in in-vivo systems is required to discern the
 influence of microgravity on their pathogenicity.
 Keywords: Enterobacter, International Space Station, Phylogenomic analyses,


Background                                                       strains with all publicly available 1291 Enterobacter ge-
Enterobacter      species    are     facultative    anaerobic,   nomes revealed that genomes of these five ISS strains
Gram-stain-negative, and saprophytic microorganisms              were highly similar to only three clinical E. bugandensis
found in soil, sewage, and as a commensal enteric flora          with very high genome similarities and formed a unique
of the human gastrointestinal tract [1]. They have been          ecotype. They are (a) EB-247 strain [13], isolated from
associated with nosocomial infection in humans, causing          neonatal blood of a patient from Tanzania, (b)
bacteremia, endocarditis, septic arthritis, osteomyelitis,       153_ECLO strain [14], isolated from the urine of a neo-
skin and soft tissue infections, lower respiratory tract,        natal patient strain admitted to the University of Wash-
urinary tract, and intra-abdominal infections [2, 3].            ington Medical Center, Seattle, WA and (c) MBRL 1077
Some Enterobacter have also been reported plant patho-           strain, a carbapenemase-producing strain [15] isolated
gens [4]. Antibiotic resistance and its clinical implica-        from the wound of a 72-year-old woman with a history
tions have been extensively studied in genus                     of cutaneous scleroderma, medically complicated obes-
Enterobacter, especially Enterobacter cloacae, which is          ity, and venous insufficiency. In this study, comparative
resistant to cephalosporins, ampicillin, amoxicillin, and        genomic analyses of five ISS strains and three clinical
cefoxitin [5, 6].                                                isolates were carried out to elucidate antimicrobial re-
   In an ongoing effort of the International Space Station       sistance (AMR) phenotypic properties, MDR gene pro-
(ISS) Microbial Observatory investigation, the National          files, and genes related to potential virulence and
Aeronautics and Space Administration (NASA) is catalog-          pathogenic potential of the ISS Enterobacter strains.
ing the total and viable microbial communities of
crew-associated environments using cultivation and mo-
                                                                 Methods
lecular techniques of microbial detection [7, 8]. As a result,
                                                                 Sample collection from ISS environmental surfaces, pro-
five isolates belonging to the Enterobacter bugandensis
                                                                 cessing, cultivation of bacteria were already reported [9].
group of bacteria from two different locations of the ISS
                                                                 When 105 bacterial strains isolated from various ISS lo-
were isolated [9]. Since the initial molecular screening iden-
                                                                 cations were analyzed for their phylogenetic affiliations,
tified these strains as Enterobacter but the identification
                                                                 five isolates were identified as Enterobacter bugandensis.
was not able to resolve their taxonomy to species level, de-
                                                                 The five Enterobacter isolates characterized during this
tailed genomic characterizations were warranted in addition
                                                                 study were isolated from two different locations of the
to the traditional microbiological characterization. Due to
                                                                 ISS flight in March 2015. Four isolates were isolated
its unstable taxonomic structure, methods utilized for the
                                                                 from the waste and hygiene compartment (WHC), and
speciation of Enterobacter varied widely. Commercial bio-
                                                                 one strain from the Advanced Resistive Exercise Device
chemical typing systems such as API® 20E [10] or Vitek® 2,
                                                                 (ARED) foot platform of ISS.
and matrix-assisted laser desorption ionization–time of
flight mass spectrometry (MALDI-TOF MS) [11] methods
have been used, but with limited success. On the basis of        Phenotypic characterization
16S rRNA analysis, Enterobacter was structured as a poly-        The isolates were biochemically identified using Vitek®2
phyletic genus and most of the species could not be re-          Compact gram-negative (GN) cards (bioMerieux, Inc.,
solved [1]. Therefore, multilocus sequence typing (MLST)         Hazelwood, MO) [16] and BioLog (Hayward, CA) car-
analysis was found to be more appropriate for phylogenetic       bon substrate utilization profile characterization [17].
classification of Enterobacter species [12].                     Sample preparation for MALDI-TOF MS protein ana-
   To resolve this question further, whole genome se-            lysis was carried out as previously established [18].
quencing (WGS) and de novo assembly was performed                MALDI-TOF mass spectra were obtained from an Ultra-
on all five ISS E. bugandensis strains, creating MLST and        flex III instrument (Bruker Daltonik, Billerica, MA) op-
genome variation profiles of the ISS strains [13]. Fur-          erated in linear positive mode under Flex-Control 3.1
thermore, comparative genome alignment of the ISS                software. Mass spectra were processed using Flex
Singh et al. BMC Microbiology   (2018) 18:175                                                               Page 3 of 13




Analysis (version 3.1; Bruker Daltonik) and BioTyper         other 4 strains using bwa-mem (http://bio-bwa.source-
software (version 3.1; Bruker Daltonik).                     forge.net/). Postprocessing of the BAM files was per-
                                                             formed using SAMtools [31] and picard (https://
Genome sequence analysis                                     github.com/broadinstitute/picard). GATK HaplotypeCal-
Genomic DNA extraction was performed as described            ler (https://software.broadinstitute.org/gatk/) was used
previously [9]. WGS was performed on the Oxford              for SNP and indels identification.
Nanopore MinION (Oxford, United Kingdom) and                    Pairwise average nucleotide index (ANI) was calcu-
Illumina MiSeq sequencing platform (San Diego, CA). A        lated using the algorithm from Goris et al. 2007 [32] and
hybrid approach was utilized for genome assembly using       GC content was determined using EzTaxon-e [33].
reads from both platforms. Nanopore reads were proc-         Digital DNA-DNA hybridization (dDDH) was performed
essed using Poretools [19] toolkit for the purposes of       using the Genome-to-Genome Distance Calculator 2.0
quality control and downstream analysis. Error corrected     (GGDC 2.0) [34]. Briefly, the genome sequences in
Nanopore and MiSeq reads were assembled using                FASTA format were submitted to GGDC 2.0 along with
SPAdes [20]. Scaffolding of the assembled contigs was        the sequences in FASTA format for the Enterobacter refer-
done using SSpace [21] and gap filling was executed          ence genome that were available: E. aerogenes KCTC
using GapFiller [22]. The draft genomes after assembly       2190, E. asburiae ATCC 35953, E. bugandensis EB-247T,
and scaffolding were annotated with the help of the          E. cancerogenus ATCC 35316, E. cloacae ATCC 13047, E.
Rapid Annotations using Subsystems Technology                hormaechei ATCC 49162, E. kobei DSM 13645, E. lignoly-
(RAST) [23] and RNAmmer servers [24] for down-               ticus SCF1, E. ludwigii EN119, E. massiliensis JC163, E.
stream analysis [25, 26] ISS strains assembly characteris-   mori LMG25706, E. muelleri JM-458T, E. xiangfangensis
tics are given in Additional file 1: Table S1. The 16S       LMG 27195, and E. soli ATCC BAA-2102. The results
rRNA, gyrB, and rpoB gene sequences were retrieved           were obtained by comparing query genomes (ISS isolates)
from the WGS and analyzed for their phylogenetic affili-     with each of the reference genomes to calculate dDDH
ations. The neighbor-joining phylogenetic analysis was       and intergenomic distances. Global comparison of ISS iso-
performed using the MEGA7 software package [27].             lates with other species was done using local BLAST [35].
MLST analysis was carried out as described previously        Genome sequence assemblies were aligned using
[28]. The MLST scheme employed here uses seven               BLASTN and the diagrammatic view was created using
house-keeping genes: dnaA (DNA replication initiator),       BLAST Ring Image Generator (BRIG) software [36].
fusA (codes Elongation factor G), gyrB (DNA replication
and repair), leuS (Leucine tRNA ligase), pyrG (CTP syn-      Nucleotide sequence deposition
thase), rplB (50S ribosomal protein), and rpoB (β subunit    The WGS data submitted to the National Center for
of bacterial RNA polymerase) [29]. The retrieved se-         Biotechnology Information (NCBI) GenBank and NASA
quences were compared with the sequence types depos-         GenLab databases were downloaded and characterized
ited at E. cloacae MLST database [30], concatenated          during this study. The complete genome sequences of all
according to the MLST scheme. The genes were ana-            ISS strains were deposited in NCBI under Bioproject
lyzed independently, or as a single concatenate using        PRJNA319366 as well as at the NASA GeneLab system
neighbor-joining algorithms.                                 (GLDS-67; https://genelab-data.ndc.nasa.gov/genelab/ac-
   The SNP-based phylogenetic tree was generated using       cession/GLDS-67/#). The GenBank/EMBL/DDBJ acces-
CSIPhylogeny [28] version 1.4. Using genome sequences        sion numbers for the 16S rRNA gene sequence of
of multiple isolates CSIPhylogeny calls SNP, filters the     isolated strains are: IF2SW-B1 (KY218809), IF2SW-B5
SNPs, performs site validation, and infers a phylogeny       (KY218813), IF2SW-P2 T (KY218815), IF2SW-P3
based on the concatenated alignment of high-quality          (KY218816), and IF3SW-P2 (KY218819).
SNPs. The analysis included Enterobacter reference whole
genome sequences which were downloaded from the              Results
NCBI GenBank database. This genome-wide SNP analysis         Phenotypic characteristics
allows for higher resolution phylogenetic analysis com-      The ISS strains showed aerobic, motile, rod shape, Gram
pared to other methods, which is necessary for comparing     stain negative characteristics; colonies were pale yellow
highly similar genomes. All positions containing gaps and    in color, formed within 24–36 h at 35 °C on R2A, TSA,
missing data were eliminated. A total of 3832 positions in   and blood agar. Growth was observed at 1–8% NaCl and
the dataset were used to confer the final tree.              in pH range 5–7. The Vitek and BioLog systems as well
   Hybrid-genome-assembly (ONT and Illumina data) of         as MALDI-TOF profiles identified the ISS strains as E.
strain IF3SW-P2 was nominated as reference genome of         ludwigii. The MALDI-TOF profile scores for the tested
the 5 strains sequenced. The IF3SW-P2 genome was             strains were 2.16 (E. ludwigii) and 2.10 (E. asburiae). In
used to realign the Illumina MiSeq reads with reads of       general, no noticeable phenotypic differences were
Singh et al. BMC Microbiology      (2018) 18:175                                                                                                       Page 4 of 13




observed among the Enterobacter species tested including                           while MBRL 1077 isolate was exhibiting 97% similarity
E. bugandensis EB-247T, whose genome is closer to ISS                              with high bootstrap value.
strains. As reported earlier, all these five ISS Enterobacter
isolates were resistant to cefazolin, cefoxitin, oxacillin, peni-                  MLST analysis
cillin and rifampin, while for ciprofloxacin and erythro-                          The genomic contigs of the ISS isolates were searched
mycin, strains were either resistant or intermediate                               for gene sequences of dnaA, fusA, gyrB. leuS, pyrG, rplB,
resistant. For gentamycin and tobramycin some strains                              and rpoB, which are standardized for the use of MLST
were resistant, some intermediate resistant, and some sus-                         analysis and reported for E. cloacae species [29]. The
ceptible [9].                                                                      good congruence between the single-gene reconstruc-
                                                                                   tions and the concatenate reinforced the stability of the
Molecular phylogeny                                                                genealogy were observed. The reconstruction was based
The 16S rRNA gene sequencing of all five isolates placed                           on the RAxML algorithm [37] and the resulting MLST
them within the Enterobacter group and showed max-                                 tree (Fig. 1) shows that the ISS isolates are phlylogeneti-
imum similarity (99.6%) with E. bugandensis EB-247T, E.                            cally related to E. bugandensis clinical strains (EB-247,
cancerogenus LMG 2693, E. ludwigii EN-119, and E.                                  strain 153_ECLO, and isolate MBRL 1077).
mori R18–2 (99 to 100%). Since 16S rRNA gene sequen-
cing analysis is insufficient to differentiate Enterobacter                        SNP analysis
species, polygenic and whole genome-based analyses                                 Even though MLST analysis was clearly able to genomi-
were further attempted. All ISS strains were phylogenet-                           cally resolve the ISS isolates to species level and distin-
ically characterized by the gyrB locus (~ 1.9 kb) and                              guish them from other members of the genus
showed that the ISS isolates form a close group with E.                            Enterobacter, whole genome SNP analysis, SNP tree ana-
bugandensis EB-247T and 153_ECLO strains (> 99%)                                   lysis excluding plasmid sequences, was carried out to


                                                                                          Enterobacter bugandensis IF2SW-P3
                                                                                          Enterobacter bugandensis IF3SW-P2
                                                                                   100
                                                                                          Enterobacter bugandensis IF2SW-B5
                                                                                          Enterobacter bugandensis IF2SW-B1
                                                                                 100
                                                                                          Enterobacter bugandensis IF2SW-P2
                                                                          100             Enterobacter bugandensis EB-247T
                                                                                  66   Enterobacter bugandensis 153 ECLO
                                                                     82
                                                                                         Enterobacter bugandensis MBRL1077
                                                                                                                                           T
                                                                    94                    Enterobacter xiangfangensis LMG 27195
                                                                            100                                                        T
                                                                                       Enterobacter hormaechei ATCC 49162
                                                                                                                                       T
                                                               97                            Enterobacter cloacae ATCC13047
                                                                                                                           T
                                                                                         Enterobacter kobei DSM 13645
                                                                                                                           T
                                                                           100            Enterobacter mori LMG 25706
                                                               30                        Enterobacter muelleri JM-458T
                                                          96                                                                   T
                                                                 27                           Enterobacter ludwigii EN-119
                                                                                                Enterobacter cancerogenus ATCC 35316
                                                                    27
                                                                                                                                               T
                                                     76              58                        Enterobacter asburiae ATCC 35953
                                                                                           100 Enterobacter soli ATCC BAA-2102             T


                                                                                          Enterobacter lignolyticus SCF1
                                                                                         Enterobacter aerogenes KCTC 2190
                                                                                                                                   T
                                                                                             Enterobacter massiliensis JC163
                                                                                                                                                   T
                                                                                                 Xenorhabdus nematophila ATCC 19061


                                0.020

 Fig. 1 Multiple-locus sequence types (MLST) analysis of ISS strains and related species of the Enterobacter. The obtained genomic contigs of the
 ISS isolates (in bold) were searched for gene sequences of dnaA, fusA, gyrB, leuS, pyrG, rplB, and rpoB, which are standardized for the use in MLST
 analysis and reported for E. cloacae species [29]. The retrieved sequences were compared with the sequence types deposited at the Enterobacter
 MLST database, concatenated according to the MLST scheme. The reconstruction was based on the RAxML algorithm [4], and the bootstrap
 values were calculated using 1000 replicates. The bar indicates 2% sequence divergence
Singh et al. BMC Microbiology       (2018) 18:175                                                                                                                               Page 5 of 13




validate these results. The snpTree does not ignore any                                          location #2 (space toilet) and one strain from the ex-
nucleotide positions and is able to consider 100% of the                                         ercise platform (ARED).
chromosomal genome. All the available WGS of the En-
terobacter genus reference genomes from GenBank were                                             ANI values and digital DNA-DNA hybridization
used for SNP analysis with snpTree. Of the 22 total nu-                                          The ANI values for the ISS strains were maximum
cleotide sequences; 58,121 positions were found in all                                           against E. bugandensis EB-247, 153_ECLO, and MBRL
analyzed genomes and 3832 positions in the dataset                                               1077 strains (> 95%) as were those of MLST analyses,
were used to confer the final tree (Fig. 2). The snpTree                                         and the ANI values of rest of the Enterobacter genomes
analyses confirmed and gave a strong validation to the                                           tested were < 91% (Table 1). The digital DNA-DNA
MLST/gyrB data, confirming that all ISS isolates are E.                                          hybridization (dDDH) results of the ISS strain showed
bugandensis but strain MBRL 1077 grouped differently                                             high similarity with E. bugandensis EB-247 (89.2%),
from the members of the E. bugandensis group.                                                    153_ECLO (89.4%), and MBRL 1077 (64%) strains
  SNP identification within ISS strains was carried                                              whereas dDDH value was < 44.6% to all the other avail-
out using GATK HaplotypeCaller. Filtered SNP calls                                               able Enterobacter reference genomes (Table 1). Based on
and indels (after removal of false positives) are given                                          various molecular analyses attempted during this study
in the Additional file 1: Table S1. Post-filtration ana-                                         all five ISS Enterobacter strains were phenotypically and
lyses showed that there were 9, 12, 15, 13, and 0                                                genotypically identified as E. bugandensis.
SNPs seen in IF2SWB1, IF2SWB5, IF2SWP2, IS2WP3
and IS3SWP2, respectively. Further 6, 0, 4, 6, and 0                                             Functional characteristics
indels were seen in IF2SWB1, IF2SWB5, IF2SWP2,                                                   A detailed genome analysis of all five ISS strains and 3
IS2WP3 and IS3SWP2, respectively (Additional file 1:                                             clinical isolates were carried out to understand its gen-
Table S1). A maximum of 15 SNPs was observed                                                     etic makeup. A total of 4733 genes were classified as
among ISS isolates, probably being clonal in origin,                                             carbohydrate metabolism (635 genes), amino acid and
with a very recent common ancestor. However, it                                                  derivatives (496 genes), protein metabolism (291 genes),
should be noted that 4 strains were isolated from                                                cofactors, vitamins, prosthetic groups, pigments (275


                                                                                                                  Enterobacter bugandensis IF2SW-P2

                                                                                                                  Enterobacter bugandensis IF2SW-P3
                                                                                                           100
                                                                                                                  Enterobacter bugandensis IF2SW-B5

                                                                                                      58          Enterobacter bugandensis IF2SW-B1

                                                                                                                  Enterobacter bugandensis IF3SW-P2
                                                                                                 100
                                                                                                                 Enterobacter bugandensis EB-247T
                                                                               100
                                                                                                                 Enterobacter bugandensis 153 ECLO

                                                                        95                                    Enterobacter bugandensis MBRL1077

                                                                                                                                                                    T
                                                                   98                                                         Enterobacter hormaechei ATCC 49162
                                                                                                                                                                            T
                                                                                                100                                Enterobacter xiangfangensis LMG 27195
                                                             74                                                                                             T
                                                                                                                          Enterobacter kobei DSM 13645
                                                                                                                                                        T
                                                  33                                                                    Enterobacter mori LMG 25706
                                                                                                                                         T
                                                                  55                                       Enterobacter muelleri JM-458

                                                 100                                                                                                            T
                                                                                                                                   Enterobacter ludwigii EN-119

                                                                                                                      Enterobacter cancerogenus ATCC 35316

                                                                                                                                                                        T
                           100                          71                                                                          Enterobacter asburiae ATCC 35953
                                                                                                                                                                    T
                                                                                                                             100    Enterobacter soli ATCC BAA-2102

                                                                                                                  Enterobacter aerogenes KCTC 2190

                                                                                                                          Enterobacter lignolyticus SCF1
                                           100
                                                                                                                                                      T
                                             51                                                                       Enterobacter massiliensis JC163
                                                                   T
                            Enterobacter cloacae ATCC13047
                                                                                            T
                                                       Xenorhabdus nematophila ATCC 19061



                                   0.050

 Fig. 2 Single nucleotide polymorphism (SNP) based phylogenetic tree, showing the relationship between the ISS isolates (in bold) and members
 of the Enterobacter genus. The tree was generated using CSI Phylogeny [28] version 1.4
Singh et al. BMC Microbiology       (2018) 18:175                                                                                            Page 6 of 13




Table 1 Digital DDH and ANI values of ISS strains and comparison with various Enterobacter species
Bacteria                         Strain               Source              GenBank accession            ISS Enterobacter bugandensis isolates (n = 5)
                                 number                                   number
                                                                                                       dDDH                        ANI (%)
E. bugandensis                   IF2SW-P2             ISS-WHC             POUR00000000                 100                         100.00
E. bugandensis                   IF2SW-B1             ISS-WHC             POUQ00000000                 100                         99.99
E. bugandensis                   IF2SW-B5             ISS-WHC             RBVJ00000000                 100                         99.99
E. bugandensis                   IF2SW-P3             ISS-WHC             POUP00000000                 100                         99.99
E. bugandensis                   IF3SW-P2             ISS-AREED           POUO00000000                 100                         99.99
                                          T
E. bugandensis                   EB-247               Nosocomial          FYBI00000000                 89.2                        98.66
E. bugandensis                   153 ECLO             Nosocomial          NZ_JVSD00000000              89.4                        98.73
E. bugandensis                   MBRL1077             Nosocomial          PRJNA310238                  63.9                        95.26
E. aerogenes                     KCTC 2190            Nosocomial          CP002824                     22.7                        78.74
                                              T
E. asburiae                      ATCC 35953           Nosocomial          NZ_CP011863                  30.4                        85.59
E. cancerogenus                  ATCC 35316           Stool               NZ_ABWM00000000              31.8                        86.10
                                              T
E. cloacae                       ATCC 13047           Spinal fluid        NC_014121                    35.4                        87.91
E. hormaechei                    ATCC 49162T          Sputum              AFHR01000000                 35.4                        87.82
                                              T
E. kobei                         DSM 13645            Blood               NZ_CP017181                  42.8                        90.54
E. lignolyticus                  SCF1                 Soil                CP002272                     23.5                        79.98
                                          T
E. ludwigii                      EN-119               Human               NZ_CP017279                  34.4                        87.57
E. massiliensis                  JC163T               Stool               NZ_CAEO00000000              22.8                        79.07
E. mori                          LMG 25706T           Mulberry            NZ_AEXB00000000              37.0                        88.59
E. muelleri                      JM-458T              Rhizosphere         FXLQ00000000                 44.6                        90.77
                                              T
Xenorhabdus nematophila          ATCC 19061           Intestine           FN667742                     22.8                        69.41
dDDH digital DNA-DNA hybridization, ANI Average Nucleotide Identity, WHC Waste and Hygiene Compartment, ARED Advanced resistive exercise device (ARED)
foot platform




  Fig. 3 Metabolic functional profiles and subsystem categories distribution of strain IF3SW-P2. 4733 genes were identified that dominated by
  carbohydrate metabolism followed by amino acid and derivatives
Singh et al. BMC Microbiology               (2018) 18:175                                                                                Page 7 of 13




Table 2 Comparative analyses of antimicrobial gene profiles of E. bungandensis isolated from ISS and clinical sources
AMR genes and its role                                                             AMR genes that are present in the strains that are:
                                                                                   ISS (n = 5)        153 ECLO            MBRL 1077           EB247
Cystine ABC transporter, ATP-binding protein                                       +                  +                   +                   +
Cystine ABC transporter, permease protein                                          +                  +                   +                   +
D-cysteine desulfhydrase (EC 4.4.1.15)                                             +                  +                   +                   +
Spectinomycin 9-O-adenylyltransferase                                                                                                         +
Streptomycin 3-O-adenylyltransferase (EC 2.7.7.47)                                                                                            +
Arsenate reductase (EC 1.20.4.1)                                                   +                  +                   +                   +
Arsenic efflux pump protein                                                        +                  +                   +                   +
Arsenic resistance protein ArsH                                                                                                               +
Arsenical resistance operon repressor                                              +                  +                   +                   +
Beta-lactamase (EC 3.5.2.6)                                                        +                  +                   +                   +
Beta-lactamase class C and other penicillin binding proteins                                                              +
Metal-dependent hydrolases of the beta-lactamase superfamily I                     +                  +                   +                   +
Cation efflux system protein CusA                                                  +                  +                   +                   +
Cation efflux system protein CusC precursor                                                                               +                   +
Cation efflux system protein CusF precursor                                                                               +                   +
Cobalt-zinc-cadmium resistance protein                                             +                  +                   +                   +
Cobalt-zinc-cadmium resistance protein CzcA                                        +                  +                   +                   +
Cobalt/zinc/cadmium efflux RND transporter, membrane fusion protein, CzcB family                                          +                   +
Copper-sensing two-component system response regulator CusR                                                               +                   +
DNA-binding heavy metal response regulator                                         +                  +                   +                   +
Heavy metal sensor histidine kinase                                                                                                           +
Probable Co/Zn/Cd efflux system membrane fusion protein                            +                  +                   +                   +
Zinc transporter ZitB                                                              +                  +                   +                   +
Acetyl-coenzyme A carboxyl transferase beta chain (EC 6.4.1.2)                     +                  +                   +                   +
Amidophosphoribosyltransferase (EC 2.4.2.14)                                       +                  +                   +                   +
Colicin V production protein                                                       +                  +                   +                   +
DedA protein                                                                       +                  +                   +                   +
DedD protein                                                                       +                  +                   +                   +
Dihydrofolate synthase (EC 6.3.2.12)                                               +                  +                   +                   +
Folylpolyglutamate synthase (EC 6.3.2.17)                                          +                  +                   +                   +
tRNA pseudouridine synthase A (EC 4.2.1.70)                                        +                  +                   +                   +
Blue copper oxidase CueO precursor                                                 +                  +                   +                   +
Copper resistance protein C precursor                                              +                  +                   +                   +
Copper resistance protein D                                                        +                  +                   +                   +
Copper-translocating P-type ATPase (EC 3.6.3.4)                                    +                  +                   +                   +
Copper homeostasis protein CutE                                                    +                  +                   +                   +
Copper homeostasis protein CutF precursor                                          +                  +                   +                   +
Magnesium and cobalt efflux protein CorC                                           +                  +                   +                   +
Membrane protein, suppressor for copper-sensitivity ScsB                           +                  +                   +                   +
Membrane protein, suppressor for copper-sensitivity ScsD                           +                  +                   +                   +
Secreted protein, suppressor for copper-sensitivity ScsC                           +                  +                   +                   +
Suppression of copper sensitivity: putative copper binding protein ScsA            +                  +                   +                   +
Fosfomycin resistance protein FosA                                                 +                  +                   +                   +
Membrane-bound lysozyme inhibitor of c-type lysozyme                               +                  +                   +                   +
16 kDa heat shock protein A                                                        +                  +                   +                   +
16 kDa heat shock protein B                                                        +                  +                   +                   +
HTH-type transcriptional regulator YidP                                            +                  +                   +                   +
Singh et al. BMC Microbiology              (2018) 18:175                                                                                               Page 8 of 13




Table 2 Comparative analyses of antimicrobial gene profiles of E. bungandensis isolated from ISS and clinical sources (Continued)
AMR genes and its role                                                                           AMR genes that are present in the strains that are:
                                                                                                 ISS (n = 5)        153 ECLO            MBRL 1077           EB247
Mediator of hyperadherence YidE                                                                  +                  +                   +                   +
Outer membrane lipoprotein YidQ                                                                  +                  +                   +                   +
Uncharacterized protein YidR                                                                     +                  +                   +                   +
Mercuric ion reductase (EC 1.16.1.1)                                                                                                                        +
PF00070 family, FAD-dependent NAD(P)-disulphide oxidoreductase                                   +                  +                   +                   +
Mercuric resistance operon coregulator                                                                                                                      +
Mercuric resistance operon regulatory protein                                                                                                               +
Mercuric transport protein, MerE                                                                                                                            +
Acriflavin resistance protein                                                                    +                  +                   +                   +
Macrolide export ATP-binding/permease protein MacB (EC 3.6.3.-)                                  +                  +                   +                   +
Macrolide-specific efflux protein MacA                                                           +                  +                   +                   +
Membrane fusion protein of RND family multidrug efflux pump                                      +                  +                   +                   +
Multi antimicrobial extrusion protein (Na(+)/drug antiporter), MATE family of MDR efflux pumps   +                  +                   +                   +
Multidrug-efflux transporter, major facilitator superfamily (MFS) (TC 2.A.1)                     +                  +                   +                   +
Probable transcription regulator protein of MDR efflux pump cluster                              +                  +                   +                   +
RND efflux system, inner membrane transporter CmeB                                               +                  +                   +                   +
RND efflux system, membrane fusion protein CmeA                                                  +                  +                   +                   +
RND efflux system, outer membrane lipoprotein CmeC                                               +                  +                                       +
RND efflux system, outer membrane lipoprotein, NodT family                                       +                  +                   +                   +
Transcription repressor of multidrug efflux pump acrAB operon, TetR (AcrR) family                +                  +                   +                   +
Type I secretion outer membrane protein, TolC precursor                                          +                  +                   +                   +
Inner membrane component of tripartite multidrug resistance system                               +                  +                   +                   +
Membrane fusion component of tripartite multidrug resistance system                              +                  +                   +                   +
Outer membrane component of tripartite multidrug resistance system                               +                  +                   +                   +
Multiple antibiotic resistance protein MarA                                                      +                  +                   +                   +
Multiple antibiotic resistance protein MarB                                                      +                  +                   +                   +
Multiple antibiotic resistance protein MarC                                                      +                  +                   +                   +
Multiple antibiotic resistance protein MarR                                                      +                  +                   +                   +
DNA-directed RNA polymerase beta subunit (EC 2.7.7.6)                                            +                  +                   +                   +
DNA-directed RNA polymerase beta&#39; subunit (EC 2.7.7.6)                                       +                  +                   +                   +
LSU ribosomal protein L20p                                                                       +                  +                   +                   +
LSU ribosomal protein L35p                                                                       +                  +                   +                   +
Translation initiation factor 3                                                                  +                  +                   +                   +
SSU ribosomal protein S12p (S23e)                                                                +                  +                   +
SSU ribosomal protein S7p (S5e)                                                                  +                  +                   +
Translation elongation factor G                                                                  +                  +                   +
Translation elongation factor Tu                                                                 +                  +                   +
L-aspartate oxidase (EC 1.4.3.16)                                                                +                  +                   +                   +
Quinolinate phosphoribosyltransferase [decarboxylating] (EC 2.4.2.19)                            +                  +                   +                   +
Quinolinate synthetase (EC 2.5.1.72)                                                             +                  +                   +                   +
DNA gyrase subunit A (EC 5.99.1.3)                                                               +                  +                   +                   +
DNA gyrase subunit B (EC 5.99.1.3)                                                               +                  +                   +                   +
Topoisomerase IV subunit A (EC 5.99.1.-)                                                         +                  +                   +                   +
Topoisomerase IV subunit B (EC 5.99.1.-)                                                         +                  +                   +                   +
Streptothricin acetyltransferase, Streptomyces lavendulae type                                   +                  +                   +                   +
Multidrug transporter MdtB                                                                       +                  +                   +                   +
Multidrug transporter MdtC                                                                       +                  +                   +                   +
Singh et al. BMC Microbiology            (2018) 18:175                                                                                Page 9 of 13




Table 2 Comparative analyses of antimicrobial gene profiles of E. bungandensis isolated from ISS and clinical sources (Continued)
AMR genes and its role                                                          AMR genes that are present in the strains that are:
                                                                                ISS (n = 5)        153 ECLO            MBRL 1077           EB247
Multidrug transporter MdtD                                                      +                  +                   +                   +
Probable RND efflux membrane fusion protein                                     +                  +                   +                   +
Response regulator BaeR                                                         +                  +                   +                   +
Sensory histidine kinase BaeS                                                   +                  +                   +                   +
Conserved uncharacterized protein CreA                                          +                  +                   +                   +
Inner membrane protein CreD                                                     +                  +
Two-component response regulator CreB                                           +                  +
Two-component response regulator CreC                                           +                  +



genes), membrane transport (247 genes), and RNA me-                 assembly information, read coverage, assembly break-
tabolism (239 genes) (Fig. 3). To test antimicrobial re-            points, and collapsed repeats. The mapping of unassem-
sistance at genomic level, the ISS strains were further             bled sequencing reads of the ISS genomes against fully
compared with nosocomial isolates (1291 genomes) hav-               annotated E. cloacae central reference sequences is
ing more than 95% ANI identity with the ISS strains,                depicted in Fig. 4.
which taxonomically identified them as same species.
Genomes of the clinical strains of E. bugandensis 247,              Discussion
153_ECLO, and MBRL-1077, whose ANI values were >                    In summary, a comparative phenotypic and genotypic
95%, were used for the genetic comparison to further                analyses of ISS isolates identified as E. bugandensis were
broaden the picture.                                                carried out. Additional genomic analyses revealed a close
  Features playing a broad role and implemented by the              genetic relatedness between ISS isolates and nosocomial
same domain such as Spectinomycin 9-O-adenylyltrans-                earth isolates. MLST and whole genome SNP tree placed
ferase and Streptomycin 3-O-adenylyltransferase (EC                 ISS and nosocomial isolates to a separate clade when
2.7.7.47) were only present in E. bugandensis 247 due to            phylogenetically aligned with other member of genus
the probable lack of selective pressure that might have             Enterobacter. A detailed functional and antimicrobial re-
been encountered by the ISS isolates (Table 2). The pre-            sistance analysis reveals that the ISS isolates have a 79%
dicted arsenic resistance (arsenic resistance protein,              probability of being a human pathogen and share similar
ArsH) noticed in E. bugandensis 247 but not in other                antimicrobial resistance pattern with E. bugandensis
strains should be phenotypically tested to confirm the              EB-247, MBRL-1077 and 153_ECLO strains, making
resistance properties conferred in strain E. bugandensis            them relevant for future missions and crew health
247 and cross checked with the ISS strains for their in-            considerations.
ability to degrade arsenic. Trace metals detected in ISS              A total of 112 identified genes of the ISS strains were
potable water samples, but typically below potability re-           involved in virulence, disease, and defense. Genes associ-
quirements, included arsenic, barium, chromium, cop-                ated with resistance to antibiotics and toxic compounds,
per, iron, manganese, molybdenum, nickel, lead,                     including the multidrug resistance tripartite system (also
selenium, and zinc. No mercury or cadmium was de-                   known as 3-protein systems) as shown in a polychlori-
tected and the arsenic levels varied from nondetectable             nated biphenyl-degrader, Burkholderia xenovorans
in water samples to a maximum of 3.8 μg/L [38].                     LB400 [39], was noticed in the ISS strain. This protein
                                                                    forms the basic structure and plays a crucial role in, the
Global comparison of ISS genomes with other                         functioning of an efflux pump rendering a microbe drug
Enterobacter genomes                                                resistant [40, 41]. A multiple antibiotic resistance (MAR)
A visualization program was reported to be invaluable               locus or MAR operon was observed in ISS strains, which
[36] in determining the genotypic differences between               codes for protein MarA, MarB, MarC, and MarR, and
closely related prokaryotes. Visualizing a prokaryote               regulate more than 60 genes, including upregulation of
genome as a circular image has become a powerful                    drug efflux systems that have been reported in
means of displaying informative comparisons of one                  Escherichia coli K12 [42–44]. Aminoglycoside
genome to a number of others. Using BRIG, a global                  adenylyltransferases, whose role is spectinomycin
visual comparison of ISS isolates with other Enterobacter           9-O-adenylyltransferases, which confers microbial resist-
WGS from the GenBank Microbial Genomes Resource                     ance to the aminoglycosides in Salmonella enterica, was
was carried out. The resulting output of the BRIG                   also seen in ISS strains [45]. Similarly, resistance to
analysis [36], a visualization image, showed draft genome           fluoroquinolones due to a mutation in gyrA gene in S.
Singh et al. BMC Microbiology      (2018) 18:175                                                                                       Page 10 of 13




 Fig. 4 Global comparison of ISS E. bugandensis with other Enterobacter WGS from NCBI Microbial Genomes Resource was done using BRIG.
 Genome sequence assemblies were aligned using BLASTN and the diagrammatic view was created using BRIG software. The innermost ring
 indicates the genomic position of the reference genome (E. bugandensis 247T), next ring indicates GC content, and the third ring indicates GC
 skewness. The remaining 21 rings indicate the presence or absence of BLASTN hits at that position. Each ring represents WGS of single
 Enterobacter species, each shown in different color. Positions covered by BLASTN alignments are indicated in solid colors and gaps (white spaces)
 represent genomic regions not covered by BLASTN alignments. Order of genome from inner ring to outer is as follow: E. aerogenes KCTC 2190, E.
 asburiae ATCC 35953 T, E. bugandensis EB-247T, E. cancerogenus ATCC 35316, E. bugandensis 153_ECLO, E. cloacae ATCC 13047T, E. bugandensis
 MBRL1077, E. hormaechei ATCC 49162T, E. kobei DSM 13645T, E. lignolyticus SCF1, E. ludwigii EN-119T, E. massiliensis JC163T, E. mori LMG 25706T, E.
 muelleri JM-458T, Enterobacter soli ATCC BAA-2102T, Enterobacter xiangfangensis LMG 27195T, E. bugandensis IF2SW-B1, E. bugandensis IF2SW-B5, E.
 bugandensis IF2SW-P2, E. bugandensis IF2SW-P3, E. bugandensis IF3SW-P2, Xenorhabdus nematophila ATCC 19061T



enterica [46], and fosfomycin resistance due to the pres-                      Astronauts have been taking beta-lactam based med-
ence of FosA protein-coding gene, which catalyzes the                        ical drugs for approximately two decades, and ß-lacta-
addition of glutathione to C1 of the oxirane in Serratia                     mase (superfamily I [metal dependent hydrolases] and
marcescens [47], were observed in ISS strains. Multiple                      E.C.3.5.2.6) was present in all strains under study, while
copies of multi-drug resistance (MDR) genes highly                           penicillin-binding proteins (PPB4B) were only present in
homologous to S. marcescens, a pathogen, were iden-                          MBRL-1077. Fluoroquinolone resistance due to gyrase
tified in the ISS Enterobacter genomes, which gives                          and topoisomerase mutation was present in all the
an indication that these strains may be a potential                          strains. Metal-dependent hydrolases, cation efflux sys-
human pathogen. When tested with PathogenFinder                              tem protein CusA, cobalt-zinc-cadmium resistance pro-
[48] algorithm, strain IF2SW-P2T had > 77% probabil-                         tein, cobalt-zinc-cadmium resistance protein CzcA,
ity to be a human pathogen. When compared with E.                            DNA-binding heavy metal response regulator, Co/Zn/Cd
cloacae ATCC 13047, which is a well-described                                efflux system membrane fusion protein, zinc transporter
human pathogen [49], all five ISS strains showed a >                         ZitB were found in both ISS isolate and nosocomial
79% probability score.                                                       organism understudy. These genes principally help in
Singh et al. BMC Microbiology   (2018) 18:175                                                                               Page 11 of 13




detoxification of periplasm by exporting toxic metal         Additional files
cation outside the cell. Determinants of the metal resist-
ance are usually located on the plasmid and readily           Additional file 1: Table S1. Genomic characteristics, single nucleotide
                                                              polymorphism, single nucleotide variations, and insertion/deletions of E.
acquired from the environment and also complement             bugandensis strains isolated from ISS. (XLSX 11 kb)
antibiotic resistance [50, 51]. The plasmid encoded puta-     Additional file 2: Table S2. Plasmid gene content of ISS strains.
tive transcriptional regulators containing the CopG/Arc/      (XLSX 17 kb)
MetJ DNA-binding domain and a metal-binding domain            Additional file 3: Table S3. Detailed function(s) of all the AMR genes
were present in the ISS strains (Additional file 2: Table     associated with 5 ISS strains. (XLSX 14 kb)
S2). Further studies are required for phenotypic
characterization to confirm this trait. Presence of active   Abbreviation
                                                             AMR: Antimicrobial resistance; ANI: Average nucleotide index;
beta lactamase gene, efflux pump, and RND (resistance,       ARED: Advanced Resistive Exercise Device; dDDH: Digital DNA-DNA
nodulation and cell division protein family) protein         hybridization; GGDC: Genome-to-Genome Distance Calculator; GN: Gram-
family renders broad-spectrum resistance to ISS isolates     negative; ISS: International Space Station; MALDI-TOF MS: Matrix-assisted
                                                             laser desorption ionization–time of flight mass spectrometry; MAR: Multiple
from drugs and natural inhibitors.                           antibiotic resistance; MDR: Multiple drug resistance; MLST: Multilocus
   We have recently observed that competency of              sequence typing; NASA: National Aeronautics and Space Administration;
bacteria to acquire foreign genetic material increases in    NCBI: National Center for Biotechnology Information; WGS: Whole genome
                                                             sequencing; WHC: Waste and hygiene compartment
microgravity (in preparation) and similar mechanism for
metal resistance of ISS strain was also predicted. Anti-     Acknowledgements
microbial and metal resistance is also conferred by RND      Part of the research described in this publication was carried out at the Jet
genes [52], which were present in all the strains under      Propulsion Laboratory, California Institute of Technology, under a contract
                                                             with NASA. We would like to thank astronauts Captain Terry Virts and
study. Genomic analysis reveals the presence of genes        Commander Jeffrey Williams for collecting samples aboard the ISS, and the
associated with MDR efflux pump, belonging to RND,           Implementation Team at NASA Ames Research Center for coordinating this
which are reported to be the major contributors of           effort. We would like to thank Stephan Ossowski and Mattia Bosio for their
                                                             insights into hybrid de-novo assembly, Alexa McIntyre for transferring data/
resistance to antibiotic and other toxic compounds to        base-calling, and Jason Wood for critically reading the manuscript. We thank
the bacteria [41]. RND efflux system, inner membrane         Dr. Patricio Jeraldo, Mayo Clinic, Rochester, MN for providing MBRL 1077
transporter CmeB, membrane fusion protein CmeA,              strain and Dr. Stephen J. Salipante, Univ. of Washington, Seattle, WA for pro-
                                                             viding 153_ECLO strain. © 2018 California Institute of Technology. Govern-
outer membrane lipoprotein CmeC, outer membrane              ment sponsorship acknowledged.
lipoprotein NodT family were found in all strains. These
become important for the future space studies, as MDR        Funding
                                                             This research was funded by a 2012 Space Biology NNH12ZTT001N grant no.
has been reported to play role in the physiological func-    19–12829-26 under Task Order NNN13D111T award to KV, which also funded
tion and confer resistance to the substances like bile,      post-doctoral fellowship for ACS and NKS. We would also like to thank the
hormone and host defense molecule [53], which can            Epigenomics Core Facility at Weill Cornell Medicine, the Bert L and N Kuggie
                                                             Vallee Foundation, the WorldQuant Foundation, NASA (NNX14AH50G,
make bacteria a dominant persistor and lead to patho-        NNX17AB26G), the National Institutes of Health (R01ES021006,
genicity in humans.                                          1R21AI129851), the Bill and Melinda Gates Foundation (OPP1151054), and
                                                             the Alfred P. Sloan Foundation (G-2015-13964). The funding bodies had no
                                                             role in designing the study, sample collection, analysis, and interpretation of
                                                             data or in writing the manuscript.
Conclusion
The genomic characterizations showed that the ISS En-        Availability of data and materials
terobacter strains might potentially exhibit pathogenicity   The genome sequences used in the current study are available on the NCBI
                                                             Genome Database under the accession numbers listed in Table 1. Detailed
to human. However, the pathogenicity of the ISS strains      function(s) of all the AMR genes associated with 5 ISS strains mentioned in
compared to clinical strains isolated from patients          Additional file 3: Table S3.
should be explored in vivo experiments before making
                                                             Authors’ contributions
any assumption about whether these potential AMR             Conceived and designed the experiments: KV. Performed the experiments:
gene markers are due to spaceflight changes or not.          NKS, DB, ACS and KW. Analyzed the data: NKS. CM structured and designed
Moreover, the transit time and route for the organisms       verification pipeline for carrying out sequencing, analysis of the de novo
                                                             assemblies, including contig alignment, genome completion, and annotation
from the ISS may have some small impact on the re-           checks. KW carried out the phenotypic assays of the antibiotic assays, Vitek-2
sponse or physiological traits of the bacteria. WGS is       based biochemical characterization, and hemolytic characterization of the
still an important tool to monitor transmission routes of    strains studied. Contributed reagents/materials/analysis tools and acquired
                                                             funding: KV, CM. Wrote the paper: NKS, ACS, DB, CM, and KV. All authors read
opportunistic pathogen bacteria [25, 26]. To avoid this,     and approved the final manuscript.
future missions could utilize Nanopore sequencing dir-
ectly in microgravity as well as additional function and     Ethics approval and consent to participate
                                                             No formal ethics approval was required in this particular study.
taxonomic classification methods [26, 54], and then le-
verage the above detailed analytic steps to gauge rele-      Consent for publication
vance for crew health and safety.                            Not applicable.
Singh et al. BMC Microbiology            (2018) 18:175                                                                                                     Page 12 of 13




Competing interests                                                                          and E. pulveris into Cronobacter as Cronobacter zurichensis nom. nov.,
The authors declare that they have no competing interests                                    Cronobacter helveticus comb. nov. and Cronobacter pulveris comb. nov.,
                                                                                             respectively, and emended description of the genera Enterobacter and
                                                                                             Cronobacter. Syst Appl Microbiol. 2013;36(5):309–19.
Publisher’s Note                                                                       13.   Doijad S, Imirzalioglu C, Yao Y, Pati NB, Falgenhauer L, Hain T, Foesel BU,
Springer Nature remains neutral with regard to jurisdictional claims in                      Abt B, Overmann J, Mirambo MM, et al. Enterobacter bugandensis sp. nov,
published maps and institutional affiliations.                                               isolated from neonatal blood. Int J Syst Evol Microbiol. 2016;66(2):968–74.
                                                                                       14.   Roach DJ, Burton JN, Lee C, Stackhouse B, Butler-Wu SM, Cookson BT,
Author details                                                                               Shendure J, Salipante SJ. A year of infection in the intensive care unit:
1
 Biotechnology and Planetary Protection Group, Jet Propulsion Laboratory,                    prospective whole genome sequencing of bacterial clinical isolates reveals
California Institute of Technology, M/S 89–2 4800 Oak Grove Dr, Pasadena,                    cryptic transmissions and novel microbiota. PLoS Genet. 2015;11(7):
CA 91109, USA. 2Department of Physiology and Biophysics, Weill Cornell                       e1005413.
Medicine, New York, NY, USA. 3Allosource, Centennial, CO, USA. 4The HRH
                                                                                       15.   Norgan AP, Freese JM, Tuin PM, Cunningham SA, Jeraldo PR, Patel R.
Prince Alwaleed Bin Talal Bin Abdulaziz Alsaud Institute for Computational
                                                                                             Carbapenem- and Colistin-resistant Enterobacter cloacae from Delta,
Biomedicine, Weill Cornell Medicine, New York, NY, USA. 5The Feil Family
                                                                                             Colorado, in 2015. Antimicrob Agents Chemother. 2016;60(5):3141–4.
Brain and Mind Research Institute, Weill Cornell Medicine, New York, NY,
                                                                                       16.   Funke G, Monnet D, de Bernardis C, von Graevenitz A, Freney J. Evaluation
USA. 6Present address: Washington State University (WSU) Extension – Youth
                                                                                             of the VITEK 2 system for rapid identification of medically relevant gram-
and Families Program, WSU, Pullman, WA, USA.
                                                                                             negative rods. J Clin Microbiol. 1998;36(7):1948–52.
                                                                                       17.   Wragg P, Randall L, Whatmore AM. Comparison of Biolog GEN III
Received: 12 March 2018 Accepted: 24 October 2018
                                                                                             MicroStation semi-automated bacterial identification system with matrix-
                                                                                             assisted laser desorption ionization-time of flight mass spectrometry and
                                                                                             16S ribosomal RNA gene sequencing for the identification of bacteria of
References
                                                                                             veterinary interest. J Microbiol Meth. 2014;105:16–21.
1. Mezzatesta ML, Gona F, Stefani S. Enterobacter cloacae complex: clinical
                                                                                       18.   Schumann P, Maier T. Chapter 13 - MALDI-TOF mass spectrometry applied
    impact and emerging antibiotic resistance. Future Microbiol. 2012;7(7):
                                                                                             to classification and identification of Bacteria. In: Michael Goodfellow IS,
    887–902.
                                                                                             Jongsik C, editors. Methods in Microbiology, vol. 41: Academic Press; 2014.
2. Chow JW, Fine MJ, Shlaes DM, Quinn JP, Hooper DC, Johnson MP, Ramphal
                                                                                             p. 275–306.
    R, Wagener MM, Miyashiro DK, Yu VL. Enterobacter bacteremia: clinical
                                                                                       19.   Loman NJ, Quinlan AR. Poretools: a toolkit for analyzing nanopore sequence
    features and emergence of antibiotic resistance during therapy. Ann Intern
                                                                                             data. Bioinformatics. 2014;30(23):3399–401.
    Med. 1991;115(8):585–90.
3. Davin-Regli A, Pages JM. Enterobacter aerogenes and Enterobacter cloacae;           20.   Bankevich A, Nurk S, Antipov D, Gurevich AA, Dvorkin M, Kulikov AS, Lesin
    versatile bacterial pathogens confronting antibiotic treatment. Front                    VM, Nikolenko SI, Pham S, Prjibelski AD, et al. SPAdes: a new genome
    Microbiol. 2015;6:392.                                                                   assembly algorithm and its applications to single-cell sequencing. J Comput
4. Chung YR, Brenner DJ, Steigerwalt AG, Kim BS, Kim HT, Cho KY.                             Biol. 2012;19(5):455–77.
    Enterobacter pyrinus sp. nov., an organism associated with Brown leaf spot         21.   Boetzer M, Henkel CV, Jansen HJ, Butler D, Pirovano W. Scaffolding pre-
    disease of pear trees. Int J Syst Evol Microbiol. 1993;43(1):157–61.                     assembled contigs using SSPACE. Bioinformatics. 2011;27(4):578–9.
5. Pages JM, James CE, Winterhalter M. The porin and the permeating                    22.   Nadalin F, Vezzi F, Policriti A. GapFiller: a de novo assembly approach to fill
    antibiotic: a selective diffusion barrier in gram-negative bacteria. Nat Rev             the gap within paired reads. BMC Bioinformatics. 2012;13(14):S8.
    Microbiol. 2008;6(12):893–903.                                                     23.   Aziz RK, Bartels D, Best AA, DeJongh M, Disz T, Edwards RA, Formsma K,
6. Tang HJ, Hsieh CF, Chang PC, Chen JJ, Lin YH, Lai CC, Chao CM, Chuang YC.                 Gerdes S, Glass EM, Kubal M, et al. The RAST server: rapid annotations using
    Clinical significance of community- and healthcare-acquired carbapenem-                  subsystems technology. BMC Genomics. 2008;9:75.
    resistant Enterobacteriaceae isolates. PLoS One. 2016;11(3):e0151897.              24.   Lagesen K, Hallin P, Rodland EA, Staerfeldt HH, Rognes T, Ussery DW.
7. Checinska A, Probst AJ, Vaishampayan P, White JR, Kumar D, Stepanov VG,                   RNAmmer: consistent and rapid annotation of ribosomal RNA genes.
    Fox GE, Nilsson HR, Pierson DL, Perry J, et al. Microbiomes of the dust                  Nucleic Acids Res. 2007;35.
    particles collected from the international Space Station and spacecraft            25.   Castro-Wallace SL, Chiu CY, John KK, Stahl SE, Rubins KH, McIntyre ABR,
    assembly facilities. Microbiome. 2015;3(1).                                              Dworkin JP, Lupisella ML, Smith DJ, Botkin DJ et al: Nanopore DNA
8. Venkateswaran K, Vaishampayan P, Cisneros J, Pierson DL, Rogers SO,                       sequencing and genome assembly on the international Space Station.
    Perry J. International Space Station environmental microbiome -                          bioRxiv 2016.
    microbial inventories of ISS filter debris. Appl Microbiol Biotechnol.             26.   McIntyre ABR, Alexander N, Burton AS, Castro-Wallace S, Chiu CY, John KK,
    2014;98(14):6453–66.                                                                     Stahl SE, Li S, Mason CE: Nanopore detection of bacterial DNA base
9. Urbaniak C, Sielaff AC, Frey KG, Allen JE, Singh N, Jaing C, Wheeler K,                   modifications. bioRxiv 2017.
    Venkateswaran K. Detection of antimicrobial resistance genes associated            27.   Kumar S, Stecher G, Tamura K. MEGA7: molecular evolutionary genetics
    with the international Space Station environmental surfaces. Nat Sci Rep.                analysis version 7.0 for bigger datasets. Mol Biol Evol. 2016;33(7):1870–4.
    2018;8(1):814.                                                                     28.   Larsen MV, Cosentino S, Rasmussen S, Friis C, Hasman H, Marvig RL, Jelsbak
10. Akbari M, Bakhshi B, Najar Peerayeh S. Particular distribution of Enterobacter           L, Sicheritz-Ponten T, Ussery DW, Aarestrup FM, et al. Multilocus sequence
    cloacae strains isolated from urinary tract infection within clonal complexes.           typing of total-genome-sequenced bacteria. J Clin Microbiol. 2012;50(4):
    Iran Biomed J. 2016;20(1):49–55.                                                         1355–61.
11. Khennouchi NCH, Loucif L, Boutefnouchet N, Allag H, Rolain J-M.                    29.   Miyoshi-Akiyama T, Hayakawa K, Ohmagari N, Shimojima M, Kirikae T.
    MALDI-TOF MS as a tool to detect a nosocomial outbreak of extended-                      Multilocus sequence typing (MLST) for characterization of Enterobacter
    Spectrum-β-lactamase- and ArmA methyltransferase-producing                               cloacae. PLoS One. 2013;8(6):e66358.
    Enterobacter cloacae clinical isolates in Algeria. Antimicrob Agents               30.   Jolley KA, Maiden MC. BIGSdb: scalable analysis of bacterial genome
    Chemother. 2015;59(10):6477–83.                                                          variation at the population level. BMC Bioinformatics. 2010;11(1):595.
12. Brady C, Cleenwerck I, Venter S, Coutinho T, De Vos P. Taxonomic                   31.   Li H, Handsaker B, Wysoker A, Fennell T, Ruan J, Homer N, Marth G, Abecasis
    evaluation of the genus Enterobacter based on multilocus sequence analysis               G, Durbin R. Genome project data processing S: the sequence alignment/
    (MLSA): proposal to reclassify E. nimipressuralis and E. amnigenus into                  map format and SAMtools. Bioinformatics. 2009;25(16):2078–9.
    Lelliottia gen. nov. as Lelliottia nimipressuralis comb. nov. and Lelliottia       32.   Goris J, Konstantinidis KT, Klappenbach JA, Coenye T, Vandamme P, Tiedje
    amnigena comb. nov., respectively, E. gergoviae and E. pyrinus into                      JM. DNA–DNA hybridization values and their relationship to whole-genome
    Pluralibacter gen. nov. as Pluralibacter gergoviae comb. nov. and Pluralibacter          sequence similarities. Int J Syst Evol Microbiol. 2007;57(1):81–91.
    pyrinus comb. nov., respectively, E. cowanii, E. radicincitans, E. oryzae and E.   33.   Kim OS, Cho YJ, Lee K, Yoon SH, Kim M, Na H, Park SC, Jeon YS, Lee JH, Yi H,
    arachidis into Kosakonia gen. nov. as Kosakonia cowanii comb. nov.,                      et al. Introducing EzTaxon-e: a prokaryotic 16S rRNA gene sequence database
    Kosakonia radicincitans comb. nov., Kosakonia oryzae comb. nov. and                      with phylotypes that represent uncultured species. Int J Syst Evol Microbiol.
    Kosakonia arachidis comb. nov., respectively, and E. turicensis, E. helveticus           2012;62(Pt 3):716–21.
Singh et al. BMC Microbiology           (2018) 18:175                                Page 13 of 13




34. Meier-Kolthoff JP, Auch AF, Klenk H-P, Goker M. Genome sequence-based
    species delimitation with confidence intervals and improved distance
    functions. BMC Bioinformatics. 2013;14:60.
35. Altschul SF, Gish W, Miller W, Myers EW, Lipman DJ. Basic local alignment
    search tool. J Mol Biol. 1990;215(3):403–10.
36. Alikhan N-F, Petty NK, Ben Zakour NL, Beatson SA. BLAST ring image
    generator (BRIG): simple prokaryote genome comparisons. BMC Genomics.
    2011;12(1):402.
37. Stamatakis A, Ludwig T, Meier H. RAxML-III: a fast program for maximum
    likelihood-based inference of large phylogenetic trees. Bioinformatics. 2005;
    21(4):456–63.
38. Lane HW, Sauer RL, Feeback DL. Isolation: NASA experiments in closed-
    environment living, advanced human life support enclosed system, vol. 104.
    San Diego, California: American Astronautical Society; 2000. p. 1–432.
39. Chain PSG, Denef VJ, Konstantinidis KT, Vergez LM, Agulló L, Reyes VL,
    Hauser L, Córdova M, Gómez L, González M, et al. Burkholderia xenovorans
    LB400 harbors a multi-replicon, 9.73-Mbp genome shaped for versatility.
    Proc Natl Acad Sci. 2006;103(42):15280–7.
40. Zgurskaya HI, Nikaido H. Multidrug resistance mechanisms: drug efflux
    across two membranes. Mol Microbiol. 2000;37(2):219–25.
41. Daury L, Orange F, Taveau JC, Verchere A, Monlezun L, Gounou C, Marreddy
    RK, Picard M, Broutin I, Pos KM, et al. Tripartite assembly of RND multidrug
    efflux pumps. Nat Commun. 2016;7:10731.
42. Hao Z, Lou H, Zhu R, Zhu J, Zhang D, Zhao BS, Zeng S, Chen X, Chan J, He
    C, et al. The multiple antibiotic resistance regulator MarR is a copper sensor
    in Escherichia coli. Nat Chem Biol. 2014;10(1):21–8.
43. Blair JMA, Webber MA, Baylay AJ, Ogbolu DO, Piddock LJV. Molecular
    mechanisms of antibiotic resistance. Nat Rev Micro. 2015;13(1):42–51.
44. Randall LP, Woodward MJ. The multiple antibiotic resistance (mar) locus
    and its significance. Res Vet Sci. 2002;72(2):87–93.
45. Murphy E. Nucleotide sequence of a spectinomycin adenyltransferase
    AAD(9) determinant from Staphylococcus aureus and its relationship to
    AAD(3″) (9). Mol Gen Genet. 1985;200(1):33–9.
46. Sierra JM, Martinez-Martinez L, Vazquez F, Giralt E, Vila J. Relationship
    between mutations in the gyrA gene and quinolone resistance in clinical
    isolates of Corynebacterium striatum and Corynebacterium amycolatum.
    Antimicrob Agents Chemother. 2005;49(5):1714–9.
47. Rigsby RE, Fillgrove KL, Beihoffer LA, Armstrong RN. Fosfomycin resistance
    proteins: a nexus of glutathione transferases and epoxide hydrolases in a
    metalloenzyme superfamily. Methods Enzymol. 2005;401:367–79.
48. Cosentino S, Voldby Larsen M, Møller Aarestrup F, Lund O. PathogenFinder -
    distinguishing friend from foe using bacterial whole genome sequence
    data. PLoS One. 2013;8(10):e77302.
49. Ren Y, Ren Y, Zhou Z, Guo X, Li Y, Feng L, Wang L. Complete genome
    sequence of Enterobacter cloacae subsp. cloacae type strain ATCC 13047. J
    Bacteriol. 2010;192(9):2463–4.
50. Singer AC, Shaw H, Rhodes V, Hart A. Review of antimicrobial resistance in
    the environment and its relevance to environmental regulators. Front
    Microbiol. 2016;7:1728.
51. Oves M. Antibiotics and heavy metal resistance emergence in water borne
    Bacteria. J Investig Genomics. 2016;3(2).
52. Guérin F, Lallement C, Isnard C, Dhalluin A, Cattoir V, Giard J-C. Landscape
    of resistance-nodulation-cell division (RND)-type efflux pumps in
    Enterobacter cloacae Complex. Antimicrob Agents Chemother. 2016;60(4):
    2373–82.
53. Sun J, Deng Z, Yan A. Bacterial multidrug efflux pumps: mechanisms,
    physiology and pharmacological exploitations. Biochem Biophys Res
    Commun. 2014;453(2):254–67.
54. Castro-Wallace SL, Chiu CY, John KK, Stahl SE, Rubins KH, McIntyre ABR,
    Dworkin JP, Lupisella ML, Smith DJ, Botkin DJ, et al. Nanopore DNA
    sequencing and genome assembly on the international Space Station. Sci
    Rep. 2017;7(1):18022.
