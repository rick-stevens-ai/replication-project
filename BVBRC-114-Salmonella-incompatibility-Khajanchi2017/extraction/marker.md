# Marker extraction placeholder (pdftotext -layout fallback)

> Note: Central Marker manifest was not found for PMID 28768482. This is a text-only
> fallback produced by `pdftotext -layout` on paper.pdf. Suitable for text queries;
> not a true structured Marker parse (no formal tables/figures).

---
Khajanchi et al. BMC Genomics (2017) 18:570
DOI 10.1186/s12864-017-3954-5




 RESEARCH ARTICLE                                                                                                                                Open Access

Comparative genomic analysis and
characterization of incompatibility group
FIB plasmid encoded virulence factors of
Salmonella enterica isolated from food
sources
Bijay K. Khajanchi1* , Nur A. Hasan2,3, Seon Young Choi2,3, Jing Han1, Shaohua Zhao4, Rita R. Colwell2,3,
Carl E. Cerniglia1 and Steven L. Foley1*


  Abstract
  Background: The degree to which the chromosomal mediated iron acquisition system contributes to virulence
  of many bacterial pathogens is well defined. However, the functional roles of plasmid encoded iron acquisition
  systems, specifically Sit and aerobactin, have yet to be determined for Salmonella spp. In a recent study, Salmonella
  enterica strains isolated from different food sources were sequenced on the Illumina MiSeq platform and found to
  harbor the incompatibility group (Inc) FIB plasmid. In this study, we examined sequence diversity and the
  contribution of factors encoded on the IncFIB plasmid to the virulence of S. enterica.
  Results: Whole genome sequences of seven S. enterica isolates were compared to genomes of serovars of S.
  enterica isolated from food, animal, and human sources. SeqSero analysis predicted that six strains were serovar
  Typhimurium and one was Heidelberg. Among the S. Typhimurium strains, single nucleotide polymorphism (SNP)-
  based phylogenetic analyses revealed that five of the isolates clustered as a single monophyletic S. Typhimurium
  subclade, while one of the other strains branched with S. Typhimurium from a bovine source. DNA sequence based
  phylogenetic diversity analyses showed that the IncFIB plasmid-encoded Sit and aerobactin iron acquisition systems
  are conserved among bacterial species including S. enterica. The IncFIB plasmid was transferred to an IncFIB plasmid
  deficient strain of S. enterica by conjugation. The transconjugant SE819::IncFIB persisted in human intestinal
  epithelial (Caco-2) cells at a higher rate than the recipient SE819. Genes of the Sit and aerobactin operons in the
  IncFIB plasmid were differentially expressed in iron-rich and iron-depleted growth media.
  Conclusions: Minimal sequence diversity was detected in the Sit and aerobactin operons in the IncFIB plasmids
  present among different bacterial species, including foodborne Salmonella strains. IncFIB plasmid encoded factors
  play a role during infection under low-iron conditions in host cells.
  Keywords: Salmonella enterica, Incompatibility group FIB plasmid, Iron acquisition systems (SitABCD and aerobactin),
  Human intestinal epithelial (Caco-2) cells, Virulence, Single nucleotide polymorphism (SNP), Whole genome
  sequencing (WGS)




* Correspondence: bijay.khajanchi@fda.hhs.gov; steven.foley@fda.hhs.gov
1
 U.S. Food and Drug Administration, National Center for Toxicological
Research, Jefferson, AR, USA
Full list of author information is available at the end of the article

                                        © The Author(s). 2017 Open Access This article is distributed under the terms of the Creative Commons Attribution 4.0
                                        International License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and
                                        reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to
                                        the Creative Commons license, and indicate if changes were made. The Creative Commons Public Domain Dedication waiver
                                        (http://creativecommons.org/publicdomain/zero/1.0/) applies to the data made available in this article, unless otherwise stated.
Khajanchi et al. BMC Genomics (2017) 18:570                                                                        Page 2 of 14




Background                                                      the colonization and pathogenicity in many bacteria
Salmonellosis, the leading bacterial foodborne illness in       [11–13]. The role of the chromosomal mediated Sit iron
the United States, is associated with consumption of            acquisition system in virulence of many bacterial patho-
food contaminated with Salmonella spp. [1]. In the US           gens is well defined [14, 15]. However, functional roles
alone, it is estimated that more than 1 million Salmon-         of iron acquisition transport systems encoded by the
ella infections occur annually, resulting in approximately      IncFIB plasmid have yet to be determined for Salmon-
20,000 hospitalizations and 400 deaths [1] . S. enterica        ella. The main objectives of this study were: i) to analyze
has been identified as the source of multiple outbreaks         and compare genomes of IncFIB plasmid containing S.
associated with meat and poultry products in the US             enterica strains isolated from turkeys and chicken; ii) to
and other countries [2]. Approximately 42% of reported          determine the sequence diversity of IncFIB plasmid
cases occur in children under 10 years of age [3]. The          encoded Sit and aerobactin operons in different bacteria
most common manifestation of Salmonella infection is            including Salmonella; iii) to evaluate the degree of con-
gastroenteritis. However, in severe cases, septicemia or        tribution of IncFIB plasmid encoded factors in virulence
organ system infections can develop [4]. Some S. enter-         of S. enterica.
ica serovars cause more invasive infections than others;           Iron is an essential cofactor for various metabolic
for example, a previous study demonstrated serovars             enzymes associated with important biological pathways
Heidelberg and Typhimurium were more invasive, i.e.,            in both microorganisms and host [16]. For example, iron
representing 13% and 6% of infections, respectively [5].        influences butyrate production by modulating expression
Thus, it is important to understand those factors               of butyryl-coenzyme A (CoA):acetate CoA-transferase
contributing to the more severe manifestations of this          enzyme of butyrate producer such as Roseburia intesti-
disease.                                                        nalis [17]. In the recent past, butyrate has been identi-
  Incompatibility group (Inc) FIB plasmids (also commonly       fied as an important metabolite for maintaining healthy
known as ColV plasmids) can encode both virulence factors       microbiota in human gut [17]. Iron is also an important
and antimicrobial resistance genes [6, 7]. These plasmids       growth factor for pathogenic bacteria, with iron concen-
have been shown to contribute to the virulence of extra-        trations of 10−6 to 10−7 M required by most microorgan-
intestinal pathogenic Escherichia coli (ExPEC) [7–9]. It has    isms to carry out metabolic processes, including electron
been demonstrated that horizontal gene transfer of IncFIB       transport, glycolysis, DNA synthesis, and defense against
plasmid resulted in the emergence of a dominant avian           toxic reactive oxygen intermediates (ROI) [18]. In re-
clonal type of S. enterica, namely serovar Kentucky [10]. In    sponse to infection, eukaryotic hosts utilize strategies to
the same study, investigators examined distribution of these    limit iron availability to pathogens. Specific host proteins,
plasmids among 902 Salmonella isolates from different           such as transferrin, lactoferrin, and ferritin, generally bind
poultry sources. The IncFIB plasmid was found to occur          to haem to form a complex within haemoprotein, result-
predominantly in serovar Kentucky (72.9% of isolates            ing in unavailability of free iron [19, 20]. Additionally, iron
tested), followed by Typhimurium (15%) and Heidelberg           is required by macrophages and/or other host cells for the
(1.7%); the latter two serovars are among the most com-         production of ROI and reactive nitrogen intermediate
monly associated with disease in humans [10]. Results of        (RNI) which, both aid in the elimination of pathogens
the study demonstrated that acquisition of the IncFIB           [16]. On the other hand, pathogens have evolved to
plasmid by S. enterica serovar Kentucky significantly in-       encode various iron acquisition systems in the chromo-
creased its ability to colonize the chicken cecum and cause     some and plasmids, including those mentioned above, to
extra-intestinal disease [10]. The potential for horizontal     sequester iron from the host to establish an infection
gene transfer of virulence and fitness related factors          [21, 22]. For instances, it has shown that aerobactin
encoded by the IncFIB plasmid between Salmonella and            defective mutants of avian pathogenic E. coli (APEC)
other enteric bacteria exists in isolates recovered from food   and uropathogenic E. coli (UPEC) showed reduced
sources. This is a potential concern for human health as        virulence in a chicken infection model [9]. Previous
these virulent species of bacteria can be acquired by           study demonstrated that SitABCD iron acquisition sys-
humans via contaminated foods.                                  tem encoded by chromosome of S. Typhimurium re-
  A previous study carried out in our laboratory showed         quired for complete virulence of this pathogen [15].
that IncFIB plasmids from Salmonella carry genes asso-          Plasmid encoded Sit and aerobactin iron acquisition
ciated with virulence, including iron acquisition trans-        systems homologs have been identified in Cronobacter
port systems, such as the Fur (ferric uptake regulator),        spp. which possesses several virulence associated genes
regulated iron ABC transporter (sitABCD) and the aero-          [23, 24].
bactin iron acquisition (iucABCD-iutA) system [6]. Fur,            Recently, we sequenced seven S. enterica isolates from
a transcriptional and post-transcriptional regulator that       different food sources such as turkey and chicken, six of
senses iron in the environment, plays a crucial role in         which contained IncFIB plasmids [25]. In the present
Khajanchi et al. BMC Genomics (2017) 18:570                                                                    Page 3 of 14




study, we used single nucleotide polymorphism (SNP)-           enterica isolates were predicted using SeqSero, a WGS
based phylogenetic analysis to compare genome se-              based tool (www.denglab.info/SeqSero) [28].
quences of these isolates to selected S. enterica serovars
isolated from food, animal, and human sources available        Single nucleotide polymorphism (SNP) analysis
on the public data base. Additionally, we conducted            A phylogenetic tree of the sequenced Salmonella genomes
phylogenetic analysis of the IncFIB plasmid encoded Sit        (n = 52) was constructed with the parsnp program
and aerobactin operons to determine sequence diversity         (Harvest software) [29], which identifies core genomes
of these factors. The expression of genes within these         across isolates and builds a phylogeny using maximum
operons was also evaluated at the transcriptional level        likelihood and core single nucleotide polymorphisms
following growth in iron-rich or iron-depleted media. To       (SNPs). Seven S. enterica isolates (SE163A, SE696A,
delineate functional roles of IncFIB plasmid encoded fac-      SE710A, SE452, SE478, SE397 and SE819) were sequenced
tors in virulence, invasion, and persistence of S. enterica,   in our study; the genome sequences of the rest of the 45
human intestinal epithelial cells (Caco-2) were infected       Salmonella enterica strains isolated from food, animal,
with IncFIB negative recipient SE819, transconjugant           and human sources were obtained from a public data
SE819::IncFIB, and wild type (plasmid donor) SE163A            base. Detail information of the isolates used in the SNP
strains. The results provide data useful in understanding      analysis was listed in the Table 1.
the functional roles of iron acquisition systems encoded
by IncFIB plasmids of S. enterica and related pathogens.       Phylogenetic analysis of iron acquisition systems
                                                               Composite phylogenetic trees were generated by averaging
Methods                                                        pair-comparisons of DNA sequences of the S. enterica and
Bacterial strains and growth medium                            E. coli strains harboring IncFIB plasmids for each of the
Bacterial isolates included in this study (Additional file     genes in either Sit (sitABCD) or aerobactin (iucABCD-
1: Table S1) were sub-cultured on sheep’s blood agar           iutA) operons, based on unweighted pair group means,
plates (Remel, Lenexa, KS). Single colonies were picked        employing the average (UPGMA) clustering algorithm,
and grown overnight in Luria-Bertani (LB) medium sup-          BioNumerics (version 7.6, Applied Maths, Kortrijk,
plemented with the following antibiotics: tetracycline         Belgium).
(32 μg/mL); kanamycin (32 μg/mL); and nalidixic acid
(64 μg/mL). Sodium azide (350 μg/mL) (Sigma-Aldrich,           Conjugation and in vitro passage
St. Louis, MO) was used in the media for conjugation.          Conjugation experiments were performed as described
Ferric chloride (100 μM) and 2,2/−bipyridyl (200 μM)           previously [30], with some modifications that were
(Sigma-Aldrich) were added to LB broth to prepare              specifically employed for this study. To obtain a trans-
iron-rich and iron-depleted growth media, respectively.        conjugant that only contain IncFIB plasmid in SE819,
                                                               we performed the conjugation experiments in two steps.
Whole genome sequencing (WGS)                                  In the first conjugation experiment, plasmids present in
Genomic DNA was extracted with the DNeasy Blood                the wild type S. enterica SE163A were transferred to the
and Tissue Kit (Qiagen, Valencia, CA), and sequenced at        sodium azide resistant recipient E. coli J53 using a plate
the University of Arkansas for Medical Sciences DNA            mating strategy [31]. Briefly, the donor and recipient
Sequencing Core Facility (Little Rock, AR). To construct       strains were cross streaked on selective LB agar plates
DNA libraries, the Nextera XT DNA Sample Prep Kit              containing sodium azide (350 μg/mL) and kanamycin
was employed, following manufacturer’s instructions            (32 μg/mL) and incubated at 37 °C. After approximately
(Illumina, San Diego, CA). Sequencing was performed            48 h, the cells from the intersection were collected and
on the Illumina MiSeq with 2 × 250 paired-end reads            re-streaked onto selective plates containing sodium azide
[25]. CLC Genomics Workbench (version 8.5.1; Qiagen,           (350 μg/mL) and kanamycin (32 μg/mL). Individual col-
Germantown, MD) was used for trimming and de novo              onies were picked and sub-cultured onto MacConkey
assembly of paired-end reads. Contigs less than 200 nu-        agar. Subsequently, colorless colonies were picked form
cleotides were excluded from analysis. Draft genomes           selective plate and transconjugants were confirmed by
of S. enterica were annotated with the Rapid Annota-           PCR targeting of the plasmid specific genes present in
tion using Subsystem Technology (RAST) [26], Patho-            different plasmids in the donor SE163A strain (IncFIB,
systems Resource Integration Center (PATRIC) [27],             IncA/C and IncX4) [10, 32]. Transconjugants containing
and NCBI Prokaryotic Pipeline (PGAP). More detailed            IncFIB but lacking the other plasmids were selected and
descriptions of the sequencing experiments were re-            stored at −80 °C. In the second conjugation experiment,
ported by Khajanchi et al. (2016) [25]. The S. enterica        a single colony of E. coli J53::IncFIB (Additional file 1:
WGS data were submitted to NCBI and the accession              Table S1) and S. enterica SE819 lacking IncFIB plasmid
numbers were listed in Table 1. Serovars of the seven S.       were grown in LB medium overnight at 37 °C. The
Khajanchi et al. BMC Genomics (2017) 18:570                                                                              Page 4 of 14




Table 1 Salmonella enterica isolates employed in the SNP analysis of this study
Strain                       Serovar           Isolation Country   State     Source              Isolation Date   Accession
SE163Ac                      Typhimuriumb      USA                 OH        Turkey diagnostic   2002             LSZD00000000
SE696Ac                      Typhimuriumb      USA                 MW        Turkey processing   2000             LXHA00000000
             c                             b
SE710A                       Typhimurium       USA                 ND        Turkey diagnostic   1992             LXGZ00000000
SE819c                       Heidelbergb       USA                 MD        Turkey              2002             LSZE00000000
SE397c                       Typhimuriumb      USA                 INAa      Chicken carcass     1999             LYRR00000000
         c                                 b
SE452                        Typhimurium       USA                 INA       Ground turkey       1999             LYRS00000000
SE478c                       Typhimuriumb      USA                 INA       Turkey              1999             LYRT00000000
SESL476                      Heidelberg        USA                 MN        Food                2003             NC_011083.1
SECVM20752                   Heidelberg        USA                 NC        Turkey              2002             AMNR00000000
SE21381                      Heidelberg        USA                 CT        Food                2002             AMMZ00000000
SECVM24359                   Heidelberg        USA                 MO        Turkey              2003             AMNP00000000
SE29169                      Heidelberg        USA                 CT        Food                2003             APIX00000000
SE41563                      Heidelberg        USA                 OR        Human               2011             AJGX00000000a
SE41565                      Heidelberg        USA                 WA        Food                2011             AJHA00000000a
SE41567                      Heidelberg        USA                 WA        Food                2011             AMNG00000000
SE41573                      Heidelberg        USA                 OH        Human               2011             AJGY00000000a
SE41576                      Heidelberg        USA                 OH        Human               2011             AMNH00000000
SE82–2052                    Heidelberg        USA                 ME        Human               1982             AMMX00000000b
SEN1536                      Heidelberg        USA                 GA        Food                2004             AKYN00000000
SEN15757                     Heidelberg        USA                 GA        Food                2007             AMND00000000
SEN18393                     Heidelberg        USA                 CT        Food                2008             AMNF00000000
SEN19992                     Heidelberg        USA                 CA        Food                2009             AMMC00000000
SEN26457                     Heidelberg        USA                 CO        Food                2010             AMNE00000000
SEN29341                     Heidelberg        USA                 MN        Food                2011             AMNJ00000000
SEN4403                      Heidelberg        USA                 CA        Food                2005             AMMT00000000
SEN4496                      Heidelberg        USA                 CO        Food                2005             AMMQ00000000
SESARA31                     Heidelberg        USA                 MD        Swine               1987             AMLV00000000
SESARA32                     Heidelberg        USA                 TX        Dog                 1986             AMLU00000000
SESARA37                     Heidelberg        USA                 CO        Turkey              1987             AMLR00000000
SEN13–01290                  Heidelberg        Canada              Quebec    Food                2012             CP012930.1
SE12–4374                    Heidelberg        Canada              Quebec    Human               2012             CP012924.1
SECFSAN002064                Heidelberg        USA                 INA       Human               2012             CP005995.1
SECFSAN002069                Heidelberg        USA                 WA        Chicken             2012             CP005390.2
SEB182                       Heidelberg        France              INA       Cattle              INA              CP003416.1
SECVM_N41746                 Heidelberg        USA                 NY        Food                2012             NZ_JYYX01000033.1
SECVM_N42472                 Heidelberg        USA                 GA        Food                2012             NZ_JYZU01000053.1
SECVM_N37938                 Heidelberg        USA                 NY        Food                2011             NZ_JYWR01000049.1
SECVM_N30683                 Heidelberg        USA                 NM        Food                2011             NZ_JYUW01000029.1
SET000240                    Typhimurium       Japan               INA       Human               2000             AP011957.1
SELT2                        Typhimurium       INA                 INA       Human               1940s            NC_003197.1
SECFSAN001921                Typhimurium       INA                 INA       Food                INA              CP006048.1
SECDC_H2662                  Typhimurium       INA                 INA       Human               1997             CP014979.1
SEUSDA-ARS-USMARC-1808       Typhimurium       USA                 INA       INA                 INA              CP014969.1
SERM9437                     Typhimurium       USA                 CO        Food                2009             CP012985.1
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                     Page 5 of 14




Table 1 Salmonella enterica isolates employed in the SNP analysis of this study (Continued)
SESA972816                        Typhimurium          China                  INA           Cattle                  2002                CP007484.1
SECDC_2009K-1640                  Typhimurium          USA                    INA           Human                   2009                CP014975.1
SECDC_2010K-1587                  Typhimurium          USA                    INA           Human                   2006                CP014965.1
EUSDA-ARS-USMARC-1810             Typhimurium          USA                    INA           Cattle                  2005                CP014982.1
EUSDA-ARS-USMARC-1880             Typhimurium          USA                    INA           Cattle                  2003                CP014981.1
SECVM29188                        Kentucky             USA                    GA            Food                    2003                CP001122.1
SECDC191                          Kentucky             INA                    INA           INA                     INA                 NZ_ABEI00000000.1
SESK222-32B                       Kentucky             INA                    INA           Food                    2005                NZ_JUIU00000000.1
a
  INA; information not available
b
  Salmonella serovars were predicted using SeqSero, a WGS-based tool [28]
c
 Seven S. enterica isolates (SE163A, SE696A, SE710A, SE452, SE478, SE397 and SE819) were sequenced in this study; the genome sequences of the rest of the 45
Salmonella isolates used for SNP analysis were obtained from a public data base


donor (E. coli J53::IncFIB) and recipient (SE819) strains                          RNA isolation and reverse transcription (RT) PCR
were mixed at a ratio of 1:1 and centrifuged at 7000                               Wild type, recipient, and transconjugant strains were
RPM for 5 min, and the pellet was spread onto LB agar                              grown in LB, iron-rich, and iron-depleted media sup-
and incubated at 37 °C for 4–5 h. Cells were harvested                             plemented with tetracycline. RNA was isolated from
from the LB agar and spread onto selective MacConkey                               approximately 109 cells collected at mid-logarithmic
agar plates supplemented with kanamycin (32 μg/mL) and                             phase with the Ribopure Bacterial RNA Isolation Kit
nalidixic acid (64 μg/mL). After incubation overnight at                           (Ambion, Invitrogen, Carlsbad, CA), following manu-
37 °C, 15 transconjugants were screened by PCR for the                             facturer’s instructions. Genomic DNA was removed by
presence of the IncFIB plasmid.                                                    treatment with DNase I and the RNA concentration
  In addition to generation of IncFIB positive transcon-                           was measured with a NanoDrop spectrometer (Thermo
jugants, generation of IncFIB plasmid cured strains was                            Scientific, Waltham, MA).
attempted by serially passaging strains SE163A, SE417,                               Quantitative reverse transcription-PCR (qRT-PCR)
and SE478 on LB agar plates for up to 34 days. A PCR                               was performed to determine expression of the encoded
template was prepared from a single colony at each                                 iron acquisition genes on the IncFIB plasmid under
passage and examined for presence or absence of the                                iron-rich and iron-depleted growth conditions. cDNA
plasmid by PCR. Previous studies in our laboratory                                 was synthesized from 250 ng RNA using the iScript
demonstrated that SE819 is a less virulent isolate lacking                         cDNA synthesis kit (BioRad, Hercules, CA), following
several virulence associated plasmids and successfully                             manufacturer’s instructions. Primers were designed
used as the recipient for conjugation studies [30, 32].                            using the PrimerQuest tool (Integrated DNA Technolo-
                                                                                   gies, Coralville, IA) and are listed in Additional file 1:
Growth kinetics                                                                    Table S2. The sitA primer was designed to detect only
Wild type (SE163A), recipient (SE819), and transconju-                             transcripts produced from plasmid encoded sitA and not
gant (SE819::IncFIB) strains were grown in LB overnight                            from the chromosome. qRT-PCR was performed using
at 37 °C with shaking (180 RPM). The optical density                               iQ SYBR green super-mix and CFX touch real-time PCR
(OD) was measured at 600 nm, using a Genesys 10UV                                  detection system (Bio-Rad). The Salmonella gmk gene
spectrophotometer (Thermo Electron Corp., Madison,                                 served as endogenous control, to normalize expression
WI). To determine growth kinetics, the overnight cul-                              [33]. No-reverse-transcriptase (NRT) controls and no-
tures of these three strains were inoculated into fresh                            template controls (NTC) were also used to monitor for
LB, LB supplemented with ferric chloride (iron-rich),                              genomic DNA contamination of the RNA. Differential
and LB supplemented with 2,2/ bipyridyl (iron-depleted)                            gene expression and fold differences were calculated by
media. The initial OD was adjusted to 0.5 for LB and                               relative quantification (ΔΔ threshold cycle [ΔΔCT]),
iron-rich LB. A higher initial OD (3.0) was used in the                            using Bio-Rad CFX manager software. Two independent
case of iron-depleted LB to accommodate slow growth                                experiments using two biological replicates and four
under iron deficient conditions. The cell suspensions                              technical replicates for each strain were carried out.
were incubated with shaking (180 RPM) at 37 °C and
the OD was measured in 1 h intervals for 8 h, followed                             Bacterial invasion assay
by a final reading at 24 h. Three biological replicates for                        Bacterial invasion assays were performed using human
each sample and each condition were employed and                                   intestinal epithelial cells (Caco-2) as described previously
experiments were repeated three times.                                             [32], with some modifications that were specifically
Khajanchi et al. BMC Genomics (2017) 18:570                                                                      Page 6 of 14




employed for this study. Briefly, 105 Caco-2 cells/well         [25]. Six of the strains contained IncFIB plasmids and
were seeded in 24-well tissue culture plates and incu-          the other (SE819), a less virulent strain, was used as the
bated at 37 °C overnight. Cells in one of the wells were        recipient for conjugation. The isolates containing the
counted using Cellometer Auto T4 (Nexcelom Bioscience,          IncFIB plasmids were predicted to be serovar Typhimur-
Lawrence, MA) and the Caco-2 cells were infected with           ium using the WGS based Salmonella serotyping tool
SE819, transconjugant SE819::IncFIB, and wild type              SeqSero, while SE819 was identified as serovar Heidel-
SE163A strains at multiplicity of infection (MOI) of 10.        berg (Table 1). The genome sequences of the isolates
After incubation for 1 h at 37 °C, the cells were washed        were compared to determine evolutionary relatedness to
twice with PBS to remove bacteria that had not infected         previously sequenced genomes (n = 45) of S. enterica
the Caco-2 cells and incubated with 200 μg/ml of genta-         serovars isolated from various food, animal, and human
micin. After incubation for 1 h at 37 °C, the cells were        sources (Table 1), using core genome SNP-based phylo-
washed twice with PBS and lysed with 0.1% chilled Triton        genetic analyses. A SNP based evolutionary tree showed
X-100, followed by dilution and plating on TSA agar to          each serovar joined distinct phylogenetic clades, irre-
obtain colony forming unit counts (CFUs) of bacteria fol-       spective of presence or absence of an IncFIB plasmid
lowing overnight incubation at 37 °C. Three replicates per      (Fig. 1a). To understand the evolutionary relatedness of
strain were included and the experiments were repeated          the S. Typhimurium isolates (n = 17) including the
three times.                                                    IncFIB positive strains from the current study, a S.
  To determine influence of iron in invasion of bacteria        Typhimurium-specific phylogenetic tree was constructed
in to host cells, wild-type (SE163A), recipient (SE819)         (Fig. 1b). It showed five of the IncFIB plasmid containing
and transconjugant (SE819::IncFIB) strains were grown           S. enterica strains isolated from turkey-associated
overnight in iron-rich and iron-depleted media prior to         sources (SE163A, SE696A, SE710A, SE452, SE478) clus-
infection of Caco-2 cells.                                      tered in a single monophyletic clade. The other S. enter-
                                                                ica isolate from chicken (SE397) branched separately
Bacterial persistence assay                                     together with the S. Typhimurium strain (SEUSDA-
Caco-2 cells were infected similar to the invasion assay.       ARS-USMARC-1880) isolated from a bovine source
After 1 h incubation, the cells were washed twice with          (Fig. 1b). These data indicate that the five S. enterica
PBS and incubated with 100 μg/ml of gentamicin for              IncFIB plasmid-containing isolates from turkey associ-
48 h. After incubation, cells were washed, lysed, and           ated sources have nearly identical chromosomal genetic
CFUs were counted as in the invasion assay procedure,           relatedness.
with three replicates per strain and experiments carried
out in triplicate.                                              Phylogenetic analysis of sitABCD and iucABCD-iutA iron
  Since variable number of adherence of Caco-2 cells            acquisition systems
was observed in each experiment, the % invasion and %           The IncFIB plasmids of Salmonella examined in this study
persistence was determined per 106 Caco-2 cells in order        encode the Fur regulated iron transporter (sitABCD) and
to normalize the number of host cells in different exper-       aerobactin (iucABCD-iutA). The sitABCD iron transporter
iments performed. Likewise, number of bacteria for 10           can be encoded both in a plasmid and on the chromo-
MOI was different for each experiment hence, to                 some, whereas the iucABCD-iutA iron acquisition system
normalize this variation between the experiments; % of          is plasmid-encoded. Interestingly, sequence annotation re-
invasion and % of persistence were determined for each          vealed all six of the IncFIB positive strains possessing the
of the strain and plotted the graph as % invasion per 106       sit operon, both in the chromosome and IncFIB plasmid.
Caco-2 cells and % persistence per 106 Caco-2 cells.            Phylogenetic analysis of both plasmid and chromosome
                                                                encoded sitABCD transporters from the different Salmon-
Statistical analysis                                            ella isolates and E. coli strains were performed to investi-
Student’s t-test was used to determine statistically signifi-   gate the genomic diversity of this system (Fig. 2). All
cant difference between sample groups, with a P-value           chromosome-encoded sit operons of S. enterica clustered
≤0.05 considered significant.                                   in one clade, including the reference LT2 S. Typhimurium
                                                                strain, while the plasmid-encoded sit operon of different
Results                                                         serovars of Salmonella and E. coli separated into a distinct
SNP analysis                                                    clade (Fig. 2). To highlight the differences, PCR primers
To understand the role of IncFIB plasmids and how the           designed for the plasmid-encoded sit genes did not amp-
genes they carry contribute to Salmonella virulence,            lify chromosome sit genes, as evident by the lack of PCR
seven S. enterica strains that were isolated from turkeys       products for S. enterica SE819. Our results indicate that
and chicken in different geographic locations in the USA        plasmid-encoded Sit systems are conserved in both
were sequenced (Table 1 and Additional file 1: Table S1)        Salmonella and E. coli while sequence diversity was found
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                  Page 7 of 14




   a                                                                                      b




 Fig. 1 SNP based phylogenetic analysis of Salmonella enterica strains isolated from food, animal, and human sources. a SNP based evolutionary
 tree showed that each serovar joined distinct phylogenetic clades, irrespective of presence or absence of an IncFIB plasmid. b Five IncFIB containing S.
 Typhimurium isolates (SE163A, SE696A, SE710A, SE452, and SE478) clustered in one clade (shown in the box) and SE397 was found to be identical to S.
 Typhimurium USDA-1880. Seven S. enterica isolates (SE163A, SE696A, SE710A, SE452, SE478, SE397 and SE819) marked with text boxes were sequenced
 in our study; the genome sequences of the other isolates were obtained from a public data base. Harvest, a core genome SNP mining tool (https://
 www.cbcb.umd.edu/software/harvest), was used to generate the SNP tree. S. enterica SL476 was employed as a reference for SNP detection


between plasmid and chromosome encoded Sit operons                             better in the LB and iron-rich LB than in iron-depleted
in the tested S. enterica isolates (Fig. 2). The plasmid-                      LB. Highest growth rates of the strains were observed
encoded aerobactin iron transporter genes were also con-                       under iron-rich conditions, compared to LB and iron-
served in the different species of Salmonella and E. coli,                     depleted LB. The donor/wild type S. enterica SE163A
with nearly identical sequences, i.e., ~99% identity (Fig. 3).                 grew better in iron-depleted LB, compared to the re-
                                                                               cipient and transconjugant strains. Overall, the results
Conjugation and stability of the IncFIB plasmid                                showed the three S. enterica strains demonstrated dif-
To examine the role of the IncFIB plasmid mediated                             ferent growth kinetics, depending on the presence of
iron acquisition systems of S. enterica, a transconjugant                      iron in the growth medium (Fig. 4).
(SE819::IncFIB) was generated that contained the IncFIB
virulence associated plasmid, in which S. enterica SE819                       qRT-PCR
and SE163A served as recipient and donor, respectively.                        To determine gene expression of plasmid encoded Sit
The presence of the IncFIB plasmid in the transconju-                          and aerobactin operons, the transcripts of the sitA,
gants was confirmed by PCR; transcripts of the IncFIB-                         iucA, and iutA genes in wild type, transconjugant, and
associated genes were found in both donor and trans-                           recipient strains grown in iron-rich and iron-depleted
conjugant, but not in the recipient strain.                                    LB were examined using qRT-PCR. Increased level (~3
   The construction of the transconjugant was essential,                       log) of sitA expression was found in the transconjugant
since the IncFIB plasmids appear to be stable, in that                         strain grown under iron-depleted compared to iron-
after 25 to 34 passages SE163A, SE417, and SE478 had                           rich conditions (Fig. 5a). However, due to variation
not lost the IncFIB plasmid, as evidenced by PCR ampli-                        among replicates, the difference was not statistically
fication of the IncFIB replicon. Therefore, addition of                        significant. A significantly increased level of sitA ex-
the IncFIB plasmid to the less virulent strain was im-                         pression was observed in SE163A in the iron-depleted
portant for evaluating the impact of the plasmid on the                        growth medium, as compared with iron-rich (Fig. 5a).
virulence of S. enterica.                                                      As expected, the sitA transcript was not detected in
                                                                               SE819, which lacked the plasmid. The expression of
Growth kinetics                                                                iucA in the transconjugant strain in iron-depleted con-
Growth kinetics of donor, recipient, and transconjugant                        ditions was significantly greater (~3 log), compared to
strains were determined by growth in LB, LB supplemented                       iron-rich (Fig. 5b), while expression was similar for
with ferric chloride (iron-rich), and LB supplemented with                     SE163A in both the iron-depleted and iron-rich media
2,2/ bipyridyl (iron-depleted) (Fig. 4). In general, all grew                  (Fig. 5b). Results of iutA gene expression were similar
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                             Page 8 of 14




 Fig. 2 Phylogenetic analysis of the IncFIB plasmid and chromosome encoded sitABCD iron transporter. Seven S. enterica isolates (SE163A, SE696A,
 SE710A, SE452, SE478, SE397, and SE819) were sequenced in this study and the sitABCD sequences of the other isolates were from the NCBI database.
 All isolates, except for SE819, contained the IncFIB plasmid. The phylogenetic tree was generated using the UPGMA clustering algorithm


to iucA, with a ~ 2.5-fold difference of expression for                     this difference was not statistically significant by Student’s
transconjugants and similar levels of expression for S.                     t-test. A significantly higher number of transconjugants
enterica SE163A (Fig. 5c).                                                  were found to persist in Caco-2 cells, compared to the re-
                                                                            cipient strain (Fig. 6b).
Invasion and persistence in Caco-2 cells                                       Both recipient and transconjugant strains invaded in
To assess the role of the IncFIB plasmid in invasion and                    Caco-2 cells at similar rates when grown in iron-rich
persistence in host cells, human intestinal epithelial cells                and iron-depleted media prior to infection (Fig. 7a).
(Caco-2) were infected with recipient, transconjugant, and                  Wild type strain invaded at higher rate in both iron-
wild type strains of S. enterica. Significantly increased in-               rich and iron-depleted conditions than the recipient
vasion and persistence of the wild type in Caco-2 cells was                 and transconjugant, however, this difference was not
observed, compared to transconjugant and recipient                          statistically significant (Fig. 7a). When grown in iron-
strains. A slightly higher uptake was observed in the trans-                rich media, the transconjugant persisted at lower rate
conjugant, compared to the recipient (Fig. 6a). However,                    in Caco-2 cells as compared the recipient; however, this
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                               Page 9 of 14




 Fig. 3 Phylogenetic analysis of the IncFIB plasmid encoded iucABCD-iutA iron transporter. Seven S. enterica isolates (SE163A, SE696A, SE710A,
 SE452, SE478, SE397, and SE819) were sequenced in this study and the iucABCD-iutA sequences of the other isolates were from the NCBI database. All
 isolates, except for SE819, contained the IncFIB plasmid. Since the iucABCD-iutA transporter is encoded only on a plasmid, the SE819 strain was
 excluded from analysis. The phylogenetic tree was generated using the UPGMA clustering algorithm



difference was not statistically significant. Whereas, in                    persistence rate both in iron-rich and iron-depleted
iron-depleted media, the transconjugant persisted                            conditions (Fig. 7b).
significantly higher rate than the recipient (Fig. 7b).
Interestingly, transconjugant persisted at higher rate                       Discussion
when grown in the iron-depleted than the iron-rich                           Dissemination of plasmid mediated antimicrobial resist-
media (Fig. 7b). Wild type strain persisted significantly                    ance and virulence genes of bacterial pathogens is a
higher rate in both iron-rich and iron-depleted condi-                       persistent health concern [6, 34]. A better understand-
tions than the recipient and transconjugant. Unlike                          ing of the contribution of specific types of plasmids to
transconjugant, wild type strain showed similar                              antimicrobial resistance and virulence is important for




 Fig. 4 Growth kinetics of S. enterica strains in iron available in vitro growth media. Wild type (SE163A), recipient (SE819), and transconjugant
 (SE819::IncFIB) strains were grown in: LB; LB amended with ferric chloride (iron-rich); and LB amended with 2,2/ bipyridyl (iron-depleted). Each
 data point represents the average OD of three replicates. Three independent experiments were performed to examine growth kinetics of the
 strains. Results of a representative experiment are shown in the graph. ID = iron-depleted and IR = iron-rich
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                  Page 10 of 14




  a                                                 b                                                   c




 Fig. 5 Gene expression of sitA, iucA, and iutA in S. enterica strains grown under low-iron and high-iron conditions. Differential gene expression
 was examined in the S. enterica donor (SE163A), recipient (SE819), and transconjugant (SE819::IncFIB) strains using qRT-PCR and SYBR green assay.
 a relative gene expression of sitA; b relative gene expression of iucA; c relative gene expression of iutA, shown in a representative experiment. The
 error bars show the standard error of mean for two biological replicates (consisting of four technical replicates) of each strain. gmk was used as a
 reference gene to normalize the expression of target genes in different samples grown under low and high iron conditions. SE819 strain which
 does not possess IncFIB plasmid used as control to normalize the background gene expressions. Student’s t-test was performed to determine the
 statistically significant difference between two groups of samples. A p value ≤0.05 was considered a significant difference between the two
 groups compared, as indicated by the asterisks (ns = not significant)


development of novel strategies to control the spread of                        sources, revealed serovar specific clades (Fig. 1a), indi-
these plasmids among foodborne pathogens. In the                                cating paraphyletic relationships. More importantly,
present study, the genetic background of S. enterica iso-                       within the S. Typhimurium clade, five of the IncFIB
lates containing IncFIB plasmids and the iron acquisition                       plasmid containing turkey-associated isolates formed
systems encoded by these plasmids were analyzed by both                         into a unique single monophyletic subclade distinct from
in silico analysis and laboratory based experiments.                            the other sequences analyzed (Fig. 1b). It is interesting
  SNP analysis of genomes of a number of S. enterica                            to note that the IncFIB plasmid was integrated into the
strains representing serovars Heidelberg, Typhimurium,                          chromosome of S. Typhimurium SET000240 after isola-
and Kentucky isolated from food, animal, and human                              tion from a human patient, indicating IncFIB encoded


                      a                                                        b




 Fig. 6 Invasion and persistence assays of different strains of S. enterica. Human intestinal epithelial cells (Caco-2) were infected with recipient SE819,
 transconjugant and wild type SE163A of S. enterica at MOI of 10. Bacterial invasion (a) and persistence assays (b) were performed 1 h and 48 h post
 infection, respectively. A slightly higher uptake and increased persistence was observed when Caco-2 cells were infected with the transconjugant strain
 as compared to the recipient SE819 strain. The error bars show the standard error of means for three biological replicates of three independent
 experiments. Student’s t-test was performed to determine the statistically significant difference between two groups of sample. A p value ≤0.05 was
 considered a significant difference between the two groups compared, as indicated by the asterisks (wild type vs. recipient and transconjugant vs.
 recipient). Statistically non-significant differences are indicated by “ns”
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                Page 11 of 14




                      a                                                    b




 Fig. 7 Invasion and persistence assays of different strains of S. enterica grown in iron-rich and iron-depleted conditions prior to infection. Recipient
 SE819, transconjugant and wild type SE163A of S. enterica strains were grown in iron-rich and iron-depleted media overnight prior to infect
 human intestinal epithelial cells (Caco-2) with at MOI of 10. Bacterial invasion (a) and persistence assays (b) were performed 1 h and 48 h post
 infection, respectively. The error bars show the standard error of means for 2–3 biological replicates of two independent experiments. Student’s
 t-test was performed to determine the statistically significant difference between two groups of sample. A p value ≤0.05 was considered a
 significant difference between the two groups compared, as indicated by the asterisks. Statistically non-significant differences are indicated by “ns”




genes have the potential to be maintained as a plasmid                         isolates whose genomes have been sequenced in this
with the ability to integrate into the chromosome [35].                        study; however, there appears to be significant sequence
Hence, this plasmid has the potential to disseminate by                        diversity between the two sitABCD operons (Fig. 2).
horizontal gene transfer into Salmonella and other                             Degree of virulence depending on whether the sitABCD
pathogens.                                                                     transporters are encoded on both the chromosome and
   Previous studies have shown that IncFIB plasmids have                       the plasmid versus one or the other may influence the
the potential to contribute to increased colonization and                      virulence of pathogen. It is known that chromosome
fitness in the chick embryo and/or other avian animal                          encoded sitABCD play role in virulence [15], however,
models when infected with avian pathogenic E. coli [36,                        currently there is scarcity of study evaluating the role of
37] and S. Kentucky [10]. Hence, dissemination of the                          plasmid encoded sitABCD in virulence of S. enterica and
IncFIB plasmid into Salmonella serovars, such as Typhi-                        other pathogens. Also, it remains to be determined
murium and Heidelberg, which are known to cause hu-                            whether presence of both sitABCD will contribute in
man infections, may contribute to improved survival in                         virulence as synergistic manner. We speculate that plas-
food animals, resulting in increased opportunities for                         mid and chromosomally encoded sitABCD transporters
human infection via contaminated food products. In                             may exhibit differential expression within the host and
addition to encoding factors contributing to virulence,                        the natural environment. Further research is needed to
IncFIB plasmids in Salmonella often carry multiple anti-                       substantiate this conclusion.
microbial resistance genes [6], which is problematic if                          The IncFIB plasmids demonstrated stability in in
they cause diseases requiring antimicrobial therapy. The                       vitro culture, as evidenced by retention of the plasmid
identification and evaluation of specific factors relative                     after repeated passaging. Host addiction genes (vagCD
to colonization, virulence, and plasmid dissemination are                      and ccdAB), encoded on this plasmid likely contribute
important for finding effective ways to control these                          to stability of the plasmid [40–42] and is indicative of
foodborne pathogens and reduce spread of virulence and                         the plasmid’s importance to the bacterial cell in food
antimicrobial resistance plasmids in the food production                       animal environments. While stably maintained in the
environment and exposure to humans.                                            bacterial host, copies of the plasmid are able to be
   Iron is one of the key signaling elements that helps                        transferred to recipients. The IncFIB plasmid was able
pathogens sense their environment as well as regulate                          to be transferred from Salmonella to E. coli and vice
gene expression to survive under reduced iron condi-                           versa via conjugation, confirming the IncFIB to be a
tions in human and animal hosts [13, 38, 39]. Bacterial                        conjugative plasmid.
pathogens are known to possess iron transporter systems                          During the growth kinetics experiments, wild type,
that facilitate survival under low iron conditions [9, 21,                     recipient, and transconjugant strains all showed slower
22]. In the present study, the focus was on plasmid-                           and/or reduced growth under low iron conditions when
encoded iron transporter systems encoded by sitABCD                            compared to high iron conditions (Fig. 4), indicating the
and iucABCD-iutA. sitABCD genes are present both in                            importance of iron for replication and growth of these
the chromosome and on the IncFIB plasmids of the six                           Salmonella isolates and supporting results of previous
Khajanchi et al. BMC Genomics (2017) 18:570                                                                      Page 12 of 14




studies [10, 43]. In addition, SE819 (recipient) and            persistence in the host was significantly higher in the
SE819::IncFIB (transconjugant) showed similar growth            transconjugant than recipient (Fig. 6b), indicating
kinetics in vitro in iron-depleted media. The reason why        IncFIB plasmid contributes to invasion and persistence.
transconjugant did not show any growth advantage in             However, the specific mechanisms are not known. Add-
iron-depleted growth media is currently unknown. Since,         itionally, the wild type strain SE163A showed signifi-
wild type strain (SE163A) showed increased growth kinet-        cantly higher invasion and persistence in Caco-2 cells
ics in iron-depleted media compared to the recipient and        compared to transconjugant and recipient (Fig. 6a & b).
transconjugants; therefore additional factors may require       In addition, transconjugant persisted at higher rate
in addition to IncFIB plasmid to obtain growth advantages       when grown in iron-depleted than the iron-rich media
in iron-depleted condition. Additional experiments are es-      prior to infection while, wild type strain showed similar
sential to test this hypothesis.                                persistence rate in both iron-rich and iron-depleted
   Expression of the plasmid encoded sitA, iucA, and            conditions (Fig. 7b). The distinct persistence of wild
iutA genes were greater under iron-depleted conditions          type and tansconjugant when grown in iron-rich and
compared with iron-rich conditions in the transconju-           iron-depleted conditions prior to infection of Caco-2
gant SE819::IncFIB, while increased sitA transcript was         cells may be due to the difference in the genetic back-
observed only under iron-depleted conditions in the             bone of these strains. From these observations we
case of SE163A. iucA and iutA of SE163A were                    speculate that factors encoded on the IncFIB plasmid
expressed similarly under both iron-rich and iron-              contribute synergistically to facilitate uptake and per-
depleted growth media. The cause of the observed dif-           sistence in the host. Whereas additional virulence fac-
ference in expression profiles of wild type and the             tors, which are either encoded by other virulence
transconjugant remains unknown, but is likely related           associated plasmid(s) or reside on the chromosome,
to differences in the bacterial genomes or other plasmids       contribute to increased infectivity and fitness within
present in the wild type strain. Botteldoom et al. [33] in-     host cells. However, we have to interpret of these find-
vestigated the expressions of the different housekeeping        ings cautiously as wild type strain possesses several
genes (16S rRNA, rpoD and gmk) of Salmonella enterica           virulence associated plasmids which is absent in the
in different growth conditions by qRT-PCR. They demon-          recipient strain. Additionally, substantial nucleotides
strated that expression of gmk was more stable than the         sequence diversity were found in the different virulence
other two housekeeping genes in various growth condi-           associated genes examined such as phoQ, sdiA, sinH,
tions tested. In our initial experiment, we examined both       avrA, ssaQ, sopB, bcfC, htpG, iroN, eutR, ssaC, sifA,
16S rRNA and gmk as reference genes for normalizations;         and spaN encoded on the chromosome between SE819
we also observed that expression of gmk was stable than         (recipient) and other six isolates including wild type
16S rRNA in different growth conditions. Therefore, in          strain SE163A (data not shown). Future studies would
the further experiments, we used gmk as the reference           be helpful to examine the role of plasmid encoded factors
gene to normalize the gene expressions in qRT-PCR.              associated with IncX4, IncA/C, and/or IncI1 plasmids
   Fur is an iron regulatory component and is a well-           often co-located with IncFIB plasmids, in both invasion
studied transcription repressor of target gene(s) repression    and the persistence of host cells, by generating transconju-
in response to iron [44–46]. Fur binds to consensus re-         gants containing combinations of plasmids.
gions upstream of target genes Fur-box [47, 48]. A previ-
ous study identified consensus sequences of Fur-box in
the S. Typhimurium genome [48] and several studies have         Conclusions
suggested that Fur regulates directly or indirectly the         In conclusion, it has been shown that there is minimal se-
many virulence factors of pathogens, including shiga-like       quence diversity in the iron acquisition systems of IncFIB
toxins in E. coli [47], colonization capacity of Helicobacter   plasmids present among different bacterial species, includ-
pylori in the human stomach [13], biofilm formation of          ing foodborne Salmonella serovars, suggesting that similar
Vibrio species, and Type 3 secretion systems of Shigella        plasmid encoded virulence factor(s) may disseminate
and S. Typhimurium [11]. The chromosome encoded                 among bacterial pathogens. The results of the study show
sitABCD in S. Typhimurium is regulated by Fur, an iron          that the IncFIB plasmids contribute to an increased ability
transporter required for virulence [15]. The mechanisms         to persist in intestinal epithelial cells as well as the viru-
of regulation of plasmid-encoded genes of sitABCD and           lence potential of an organism. Thus, because IncFIB plas-
iucABCD-iutA operons in response to iron have yet to be         mids have the potential to carry both virulence and
determined.                                                     antimicrobial resistance genes, they represent a health
   In the invasion assays, a slightly higher percentage up-     concern since transfer of a single plasmid to a susceptible
take of the transconjugant strain was observed compared         bacterial strain can render it both more virulent and re-
to the recipient (Fig. 6a). Similarly, the percentage of        sistant to multiple antimicrobial agents.
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                                 Page 13 of 14




Additional file                                                                      3.    Scallan E, Mahon BE, Hoekstra RM, Griffin PM. Estimates of illnesses,
                                                                                           hospitalizations and deaths caused by major bacterial enteric pathogens in
                                                                                           young children in the United States. Pediatr Infect Dis J. 2013;32(3):217–21.
 Additional file 1: Table S1. Salmonella spp. that were sequenced and
                                                                                     4.    Wilmshurst P, Sutcliffe H. Splenic abscess due to Salmonella heidelberg. Clin
 constructed for this research. Table S2. Primers employed for qRT-PCR
                                                                                           Infect Dis. 1995;21(4):1065.
 (PDF 66 kb)
                                                                                     5.    Jones TF, Ingram LA, Cieslak PR, Vugia DJ, Tobin-D'Angelo M, Hurd S, Medus
                                                                                           C, Cronquist A, Angulo FJ. Salmonellosis outcomes differ substantially by
Abbreviations                                                                              serotype. J Infect Dis. 2008;198(1):109–14.
IncFIB: Incompatibility group (Inc) FIB plasmid; S. enterica: Salmonella enterica;   6.    Han J, Lynne AM, David DE, Tang H, Xu J, Nayak R, Kaldhone P, Logue CM,
SNP: Single nucleotide polymorphism; WGS: Whole genome sequencing                          Foley SL. DNA sequence analysis of plasmids from multidrug resistant
                                                                                           Salmonella enterica serotype Heidelberg isolates. PLoS One. 2012;7(12):e51160.
Acknowledgements                                                                     7.    Johnson TJ, Siek KE, Johnson SJ, Nolan LK. DNA sequence of a ColV plasmid
The authors thank Dr. R. Doug Wagner for providing the Caco-2 cells used in                and prevalence of selected plasmid-encoded virulence genes among avian
this research. The opinions expressed in this manuscript are solely the re-                Escherichia coli strains. J Bacteriol. 2006;188(2):745–58.
sponsibility of the authors and do not necessarily represent the official views      8.    Aguero ME, de la Fuente G, Vivaldi E, Cabello F. ColV increases the virulence
and policy of the US Food and Drug Administration or National Institutes of                of Escherichia coli K1 strains in animal models of neonatal meningitis and
Health. Reference to any commercial materials, equipment, or process does                  urinary infection. Med Microbiol Immunol. 1989;178(4):211–6.
not in any way constitute approval, endorsement, or recommendation by                9.    Gao Q, Wang X, Xu H, Xu Y, Ling J, Zhang D, Gao S, Liu X. Roles of iron
the Food and Drug Administration.                                                          acquisition systems in virulence of extraintestinal pathogenic Escherichia coli:
                                                                                           salmochelin and aerobactin contribute more to virulence than heme in a
                                                                                           chicken infection model. BMC Microbiol. 2012;12:143.
Funding
                                                                                     10.   Johnson TJ, Thorsness JL, Anderson CP, Lynne AM, Foley SL, Han J, Fricke
The FDA Commissioner’s Fellowship Program is acknowledged for this research
                                                                                           WF, McDermott PF, White DG, Khatri M, et al. Horizontal gene transfer of a
project and support for BKK. The University of Arkansas for Medical Sciences
                                                                                           ColV plasmid has resulted in a dominant avian clonal type of Salmonella
(UAMS) Sequencing Facility is funded in part by NIH Grant no. UL1TR000039
                                                                                           enterica serovar Kentucky. PLoS One. 2010;5(12):e15524.
and the UAMS Translational Research Institute and Center for Microbial
Pathogenesis and Host Inflammatory Responses Grant no. P20GM103625.                  11.   Porcheron G, Dozois CM. Interplay between iron homeostasis and virulence:
                                                                                           fur and RyhB as major regulators of bacterial pathogenicity. Vet Microbiol.
                                                                                           2015;179(1–2):2–14.
Availability of data and materials                                                   12.   Mey AR, Wyckoff EE, Kanukurthy V, Fisher CR, Payne SM. Iron and fur
The S. enterica WGS data have been deposited to NCBI (BioProject:                          regulation in Vibrio cholerae and the role of fur in virulence. Infect Immun.
PRJNA312617).                                                                              2005;73(12):8167–78.
                                                                                     13.   Ernst FD, Bereswill S, Waidner B, Stoof J, Mader U, Kusters JG, Kuipers EJ, Kist M,
Authors’ contributions                                                                     van Vliet AH, Homuth G. Transcriptional profiling of Helicobacter pylori fur- and
BK, SF, SZ: designed and coordinated the study, carried out experiments and                iron-regulated gene expression. Microbiology. 2005;151(Pt 2):533–46.
wrote the manuscript; NH, SY, JH: performed SNP analyses and wrote the               14.   Sabri M, Leveille S, Dozois CM. A SitABCD homologue from an avian
manuscript; CC, RC: provided scientific data interpretation and wrote the                  pathogenic Escherichia coli strain mediates transport of iron and manganese
manuscript. All authors read and approved the submitted manuscript.                        and resistance to hydrogen peroxide. Microbiology. 2006;152(Pt 3):745–58.
                                                                                     15.   Janakiraman A, Slauch JM. The putative iron transport system SitABCD
Ethics approval and consent to participate                                                 encoded on SPI1 is required for full virulence of Salmonella typhimurium.
Not Applicable.                                                                            Mol Microbiol. 2000;35(5):1146–55.
                                                                                     16.   Schaible UE, Kaufmann SH. Iron and microbial infection. Nat Rev Microbiol.
Consent for publication                                                                    2004;2(12):946–53.
Not Applicable.                                                                      17.   Dostal A, Lacroix C, Bircher L, Pham VT, Follador R, Zimmermann MB,
                                                                                           Chassard C. Iron modulates butyrate production by a child gut microbiota
Competing interests                                                                        in vitro. MBio. 2015;6(6):e01453–15.
The authors declare that they have no competing interests.                           18.   Weinberg ED. Iron and infection. Microbiol Rev. 1978;42(1):45–66.
                                                                                     19.   Kaplan J. Mechanisms of cellular iron acquisition: another iron in the fire.
                                                                                           Cell. 2002;111(5):603–6.
Publisher’s Note                                                                     20.   Hentze MW, Muckenthaler MU, Andrews NC. Balancing acts: molecular
Springer Nature remains neutral with regard to jurisdictional claims in                    control of mammalian iron metabolism. Cell. 2004;117(3):285–97.
published maps and institutional affiliations.                                       21.   Di Lorenzo M, Stork M. Plasmid-Encoded Iron Uptake Systems. Microbiol
                                                                                           Spectr. 2014;2(6):PLAS-0030-2014.
Author details                                                                       22.   Runyen-Janecky LJ. Role and regulation of heme iron acquisition in gram-
1
 U.S. Food and Drug Administration, National Center for Toxicological                      negative pathogens. Front Cell Infect Microbiol. 2013;3:55.
Research, Jefferson, AR, USA. 2Center of Bioinformatics and Computational            23.   Franco AA, Hu L, Grim CJ, Gopinath G, Sathyamoorthy V, Jarvis KG, Lee C,
Biology, University of Maryland Institute of Advanced Computer Studies,                    Sadowski J, Kim J, Kothary MH, et al. Characterization of putative virulence
University of Maryland, College Park, MD, USA. 3CosmosID, Inc., Rockville, MD,             genes on the related RepFIB plasmids harbored by Cronobacter spp. Appl
USA. 4U.S. Food and Drug Administration, Center for Veterinary Medicine,                   Environ Microbiol. 2011;77(10):3255–67.
Laurel, MD, USA.                                                                     24.   Grim CJ, Kothary MH, Gopinath G, Jarvis KG, Beaubrun JJ, McClelland M, Tall
                                                                                           BD, Franco AA. Identification and characterization of Cronobacter iron
Received: 21 March 2017 Accepted: 23 July 2017                                             acquisition systems. Appl Environ Microbiol. 2012;78(17):6035–50.
                                                                                     25.   Khajanchi BK, Han J, Gokulan K, Zhao S, Gies A, Foley SL. Draft Genome
                                                                                           Sequences of Four Salmonella enterica Strains Isolated from Turkey-
References                                                                                 Associated Sources. Genome Announc. 2016;4(5):e01122–16.
1. Scallan E, Hoekstra RM, Angulo FJ, Tauxe RV, Widdowson MA, Roy SL, Jones          26.   Aziz RK, Bartels D, Best AA, DeJongh M, Disz T, Edwards RA, Formsma K,
    JL, Griffin PM. Foodborne illness acquired in the United States–major                  Gerdes S, Glass EM, Kubal M, et al. The RAST server: rapid annotations using
    pathogens. Emerg Infect Dis. 2011;17(1):7–15.                                          subsystems technology. BMC Genomics. 2008;9:75.
2. Folster JP, Pecic G, Rickert R, Taylor J, Zhao S, Fedorka-Cray PJ, Whichard J,    27.   Wattam AR, Abraham D, Dalay O, Disz TL, Driscoll T, Gabbard JL, Gillespie JJ,
    McDermott P. Characterization of multidrug-resistant Salmonella enterica               Gough R, Hix D, Kenyon R, et al. PATRIC, the bacterial bioinformatics
    serovar heidelberg from a ground turkey-associated outbreak in the United              database and analysis resource. Nucleic Acids Res. 2014;42(Database issue):
    States in 2011. Antimicrob Agents Chemother. 2012;56(6):3465–6.                        D581–91.
Khajanchi et al. BMC Genomics (2017) 18:570                                                                                                       Page 14 of 14




28. Zhang S, Yin Y, Jones MB, Zhang Z, Deatherage Kaiser BL, Dinsmore BA,
    Fitzgerald C, Fields PI, Deng X. Salmonella serotype determination utilizing high-
    throughput genome sequencing data. J Clin Microbiol. 2015;53(5):1685–92.
29. Treangen TJ, Ondov BD, Koren S, Phillippy AM. The harvest suite for rapid
    core-genome alignment and visualization of thousands of intraspecific
    microbial genomes. Genome Biol. 2014;15(11):524.
30. Kaldhone P, Nayak R, Lynne AM, David DE, McDermott PF, Logue CM, Foley
    SL. Characterization of Salmonella enterica serovar Heidelberg from turkey-
    associated sources. Appl Environ Microbiol. 2008;74(16):5038–46.
31. Bradley DE, Taylor DE, Cohen DR. Specification of surface mating systems
    among conjugative drug resistance plasmids in Escherichia coli K-12. J
    Bacteriol. 1980;143(3):1466–70.
32. Gokulan K, Khare S, Rooney AW, Han J, Lynne AM, Foley SL. Impact of
    plasmids, including those encodingVirB4/D4 type IV secretion systems, on
    Salmonella enterica serovar Heidelberg virulence in macrophages and
    epithelial cells. PLoS One. 2013;8(10):e77866.
33. Botteldoorn N, Van Coillie E, Grijspeerdt K, Werbrouck H, Haesebrouck F,
    Donne E, D'Haese E, Heyndrickx M, Pasmans F, Herman L. Real-time reverse
    transcription PCR for the quantification of the mntH expression of
    Salmonella enterica as a function of growth phase and phagosome-like
    conditions. J Microbiol Methods. 2006;66(1):125–35.
34. Foley SL, Johnson TJ, Ricke SC, Nayak R, Danzeisen J. Salmonella
    pathogenicity and host adaptation in chicken-associated serovars. Microbiol
    Mol Biol Rev. 2013;77(4):582–607.
35. Izumiya H, Sekizuka T, Nakaya H, Taguchi M, Oguchi A, Ichikawa N, Nishiko
    R, Yamazaki S, Fujita N, Watanabe H, et al. Whole-genome analysis of
    Salmonella enterica serovar typhimurium T000240 reveals the acquisition of
    a genomic island involved in multidrug resistance via IS1 derivatives on the
    chromosome. Antimicrob Agents Chemother. 2011;55(2):623–30.
36. Gibbs PS, Maurer JJ, Nolan LK, Wooley RE. Prediction of chicken embryo
    lethality with the avian Escherichia coli traits complement resistance, colicin
    V production, and presence of the increased serum survival gene cluster
    (iss). Avian Dis. 2003;47(2):370–9.
37. Ginns CA, Benham ML, Adams LM, Whithear KG, Bettelheim KA, Crabb BS,
    Browning GF. Colonization of the respiratory tract by a virulent strain of
    avian Escherichia coli requires carriage of a conjugative plasmid. Infect
    Immun. 2000;68(3):1535–41.
38. Litwin CM, Calderwood SB. Role of iron in regulation of virulence genes.
    Clin Microbiol Rev. 1993;6(2):137–49.
39. da Silva Neto JF, Lourenco RF, Marques MV. Global transcriptional response
    of Caulobacter crescentus to iron availability. BMC Genomics. 2013;14:549.
40. Mnif B, Vimont S, Boyd A, Bourit E, Picard B, Branger C, Denamur E, Arlet G.
    Molecular characterization of addiction systems of plasmids encoding
    extended-spectrum beta-lactamases in Escherichia coli. J Antimicrob
    Chemother. 2010;65(8):1599–603.
41. Engelberg-Kulka H, Glaser G. Addiction modules and programmed cell death
    and antideath in bacterial cultures. Annu Rev Microbiol. 1999;53:43–70.
42. Pullinger GD, Lax AJ. A Salmonella dublin virulence plasmid locus that
    affects bacterial growth under nutrient-limited conditions. Mol Microbiol.
    1992;6(12):1631–43.
43. Nugent SL, Meng F, Martin GB, Altier C. Acquisition of Iron is Required for
    growth of Salmonella spp. in tomato fruit. Appl Environ Microbiol. 2015;
    81(11):3663–70.
44. Bjarnason J, Southward CM, Surette MG. Genomic profiling of iron-
    responsive genes in Salmonella enterica serovar typhimurium by high-
    throughput screening of a random promoter library. J Bacteriol. 2003;
    185(16):4973–82.
45. Hantke K. Members of the fur protein family regulate iron and zinc transport in      Submit your next manuscript to BioMed Central
    E. coli and characteristics of the fur-regulated fhuF protein. J Mol Microbiol
    Biotechnol. 2002;4(3):217–22.                                                        and we will help you at every step:
46. Hantke K. Regulation of ferric iron transport in Escherichia coli K12: isolation
                                                                                          • We accept pre-submission inquiries
    of a constitutive mutant. Mol Gen Genet. 1981;182(2):288–92.
47. Calderwood SB, Mekalanos JJ. Iron regulation of Shiga-like toxin expression in        • Our selector tool helps you to find the most relevant journal
    Escherichia coli is mediated by the fur locus. J Bacteriol. 1987;169(10):4759–64.     • We provide round the clock customer support
48. de Lorenzo V, Wee S, Herrero M, Neilands JB. Operator sequences of the
                                                                                          • Convenient online submission
    aerobactin operon of plasmid ColV-K30 binding the ferric uptake regulation
    (fur) repressor. J Bacteriol. 1987;169(6):2624–30.                                    • Thorough peer review
                                                                                          • Inclusion in PubMed and all major indexing services
                                                                                          • Maximum visibility for your research

                                                                                          Submit your manuscript at
                                                                                          www.biomedcentral.com/submit
