# Marker-equivalent text extraction of paper.pdf

**Source:** paper.pdf (Kavvas et al. 2018, Nat Commun 9:4306, PMID 30333483, PMC6193043)
**Tool used:** `pdftotext -layout` (Poppler 26.06.0)
**Rationale:** The `marker` CLI is not installed on CherryRd (marker/nougat env absent);
for a native-typeset PDF (not a scan) pdftotext with layout is a functional equivalent
that preserves reading order well enough for evidence citation and claim extraction.
For a rigorous marker rerun, ship paper.pdf to a marker-enabled host.

---

                  ARTICLE
                  DOI: 10.1038/s41467-018-06634-y                 OPEN

                  Machine learning and structural analysis of
                  Mycobacterium tuberculosis pan-genome identiﬁes
                  genetic signatures of antibiotic resistance
                  Erol S. Kavvas 1, Edward Catoiu1, Nathan Mih1,2, James T. Yurkovich 1,2, Yara Seif                                            1, Nicholas Dillon3,4,

                  David Heckmann1, Amitesh Anand1, Laurence Yang1, Victor Nizet 3,4,
                  Jonathan M. Monk1 & Bernhard O. Palsson 1,2,3

1234567890():,;



                  Mycobacterium tuberculosis is a serious human pathogen threat exhibiting complex evolution
                  of antimicrobial resistance (AMR). Accordingly, the many publicly available datasets
                  describing its AMR characteristics demand disparate data-type analyses. Here, we develop a
                  reference strain-agnostic computational platform that uses machine learning approaches,
                  complemented by both genetic interaction analysis and 3D structural mutation-mapping, to
                  identify signatures of AMR evolution to 13 antibiotics. This platform is applied to
                  1595 sequenced strains to yield four key results. First, a pan-genome analysis shows that M.
                  tuberculosis is highly conserved with sequenced variation concentrated in PE/PPE/PGRS
                  genes. Second, the platform corroborates 33 genes known to confer resistance and identiﬁes
                  24 new genetic signatures of AMR. Third, 97 epistatic interactions across 10 resistance
                  classes are revealed. Fourth, detailed structural analysis of these genes yields mechanistic
                  bases for their selection. The platform can be used to study other human pathogens.




                  1 Department of Bioengineering, University of California, San Diego, La Jolla, CA, USA. 2 Bioinformatics and Systems Biology Program, University of California,

                  San Diego, La Jolla, CA, USA. 3 Department of Pediatrics, University of California, San Diego, La Jolla, CA, USA. 4 Skaggs School of Pharmacy and
                  Pharmaceutical Sciences, University of California, San Diego, La Jolla, CA, USA. Correspondence and requests for materials should be addressed to
                  J.M.M. (email: jmonk@ucsd.edu) or to B.O.P. (email: palsson@ucsd.edu)

                  NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications                                                 1
ARTICLE                                                                            NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y




A
         dvancements in genome sequencing technologies have                Assessing allele frequencies identiﬁes key AMR genes. Although
         made available thousands of drug-tested M. tuberculosis           the M. tuberculosis pan-genome clusters provide an informative
         genomes in public databases. With available sequences             view of the global genetic repertoire within a species, they lack the
expected to surpass 60,000 during the next 5 years (https://www.           resolution necessary to discriminate between most AMR pheno-
crypticproject.org/), there is impetus for new quantitative                types. To elucidate ﬁne-grained genetic variation indicative of
approaches that excel at analyzing massive datasets. Methods that          AMR evolution, we separated each pan-genome cluster into
explicitly account for structure amongst features—such as those            groups of exact amino acid sequence variants, or alleles (Sup-
found in the ﬁeld of machine learning—will be essential for                plementary Fig. 3g). In contrast to alignment-based perspectives,
addressing this M. tuberculosis data deluge1.                              the allele-based pan-genome does not reduce non-H37Rv variants
   To date, most approaches compare M. tuberculosis genome                 to a collection of SNPs, but instead represents variants in their
sequences against the H37Rv reference strain in order to identify          functional protein-coding form. This approach accounts for all
single nucleotide polymorphisms (SNPs). Following SNP identi-              protein-coding alleles in the M. tuberculosis pan-genome, thereby
ﬁcation, most studies then focus on the subset of previously               representing the extensive strain-to-strain variation observed in
identiﬁed resistance-determining SNPs that have been previously            bacterial genomes without biasing the variations relative to a
determined to be key resistance-determining mutations, speciﬁ-             single reference genome.
cally those within a handful of genes encoding proteins targeted              We used mutual information (MI)12 as an association metric to
by drugs2. While such studies have proven to be powerful for               identify resistance-determining genes with this newly constructed
diagnostics3 and elucidating mutational steps to AMR2, they                variant pan-genome and the accompanying AMR dataset
do not account for potential genome-wide mutations reﬂecting               (Methods). Importantly, this approach identiﬁed primary
positive AMR selection, such as those found to be related to               resistance-conferring genes previously reported in the literature
cell wall permeability, efﬂux pumps, and compensatory                      (Fig. 1). In addition to MI, we calculated associations using a chi-
mechanisms4.                                                               squared test and an ANOVA F-test, both of which identiﬁed
   Speciﬁc genome-wide functional analyses in M. tuberculosis              similar sets of key AMR genes (P < 0.005; Bonferroni correction)
have shown that ald loss-of-function5, ubiA gain-of-function6,             (Supplementary Data 1). These results suggest that allele
and thyA loss-of-function7 mutations occur in off-target                   frequencies based on exact sequence (i.e., without a metric for
reactions, and confer resistance through modulation of                     genetic distance) are capable of identifying AMR genes, which has
metabolite pools. These results exemplify the complex interplay            previously been shown with k-mer based approaches13–15.
underlying AMR phenotypes that extends beyond the few
genes currently utilized in diagnostic studies. In addition
to limitations of a narrow genetic view, the identiﬁcation of other        Machine learning identiﬁes known and new resistance genes.
types of resistance-conferring mutations, such as deletions8,9,            Although simple and effective, pairwise association tests (i.e., MI,
suggest that SNPs are no longer comprehensive in describing the            chi-squared, and ANOVA F-test) do not simultaneously account
mutational landscape of M. tuberculosis AMR evolution.                     for multiple alleles because the pairwise calculations consider
   Here, we apply a reference-agnostic machine learning                    variants independently of one another. Thus, we tailored a sup-
approach complemented by both genetic interaction and protein              port vector machine (SVM)—a method that inherently accounts
structural analysis to deduce the variability in genetic content and       for structure amongst the features—to uncover AMR-conferring
AMR of 1595 M. tuberculosis strains. The complete analysis                 genes (Methods). Using the allele presence–absence across strains
recapitulates known AMR mechanisms and infers speciﬁc selec-               as the features, the SVM identiﬁed an additional seven known
tion pressures through directed hypotheses.                                AMR gene–antibiotic relations absent from the top 40 ranked
                                                                           alleles determined by pairwise associations, including those
                                                                           associated with complex resistance (Table 1). In particular, ubiA,
Results                                                                    a resistance gene recently found to confer high level resistance to
Characterizing the M. tuberculosis pan-genome. Our ﬁrst goal               ethambutol6, appeared as a strong signal across the ensemble of
was to characterize and understand the gene content of sequenced           SVM simulations—despite not being accounted for in con-
M. tuberculosis strains. We selected a representative set of 1595          temporary M. tuberculosis diagnostics (Supplementary Data 2).
M. tuberculosis strains for which AMR testing data was available
from the PATRIC database10 and come from a wide range of                          Isoniazid        Ofloxacin
studies (see Supplementary Discussion). Strains were selected for                 Rifampicin       Pyrazinamide
                                                                                  Streptomycin
their genetic, geographic, and AMR phenotypic diversity (Sup-                     Ethambutol
plementary Fig. 1). The geographic diversity of these strains
reﬂects areas heavily burdened by M. tuberculosis (Supplementary             MI
Fig. 1a). We constructed a phylogenetic tree for the 1595 strains           (bits)
using a robust set of lineage-deﬁning SNPs11 (Supplementary                 0.6
Fig. 1b and Methods). Finally, strains were selected in order to            0.4
                                                                                                                                                   gy
provide a distribution across commonly used M. tuberculosis                 0.2                                                                 ka    rA
                                                                                                                                                  tG
treatment regimens (Methods). Of these 1595 strains, 1282 strains                                                                        rp
                                                                                                                                           oB
had AMR testing data for isoniazid, rifampicin, streptomycin, and                                                             pn
                                                                                                                                cA
ethambutol (Supplementary Fig. 1c) and 946 (59%) were resistant
to both isoniazid and rifampicin. Following the selection of                         Antibiotics                     rp                 Pan-genome
                                                                                                                  em sL
strains, we determined the pan-genome (i.e., the union of all                                                       bB                    alleles
genes across the strains) represented by these data and analyzed
the distribution of various genomic features (core genes, virulence        Fig. 1 Identiﬁcation of key resistance-conferring genes using mutual
factors, etc.). The pan-genome analysis described a general                information. The pairwise mutual information (vertical axis) between the
theme of high conservation (Supplementary Fig. 2, see Supple-              pan-genome alleles and antibiotic resistance was calculated across all
mentary Discussion for further discussion of M. tuberculosis pan-          possible pairs. The listed genes correspond to the pan-genome alleles that
genome).                                                                   hold the most information about the listed drug’s AMR phenotype

2                        NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications
NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y                                                                                        ARTICLE

 Table 1 Known AMR genes uncovered by machine learning                                    resistance6,17,18. Although the embR alleles appeared few times
                                                                                          across the multiple SVM simulations, their appearance was highly
                                                                                          correlated with alterations in the sign and weight of the ubiA
 Antibiotics                          Known AMR genes
                                                                                          allele (see Supplementary Figure 6). This implies that embR is
 Isoniazid                            katG43, inhAa20, fabG144                            only a predictive feature within the context of ubiA, which may
 Rifampicin                           rpoB45, rpoCa46 Rv3239c47
 Ethambutol                           embB48, embC17, ubiAa6, embRa17
                                                                                          result from the weak penetrance of embR alleles within M.
 Pyrazinamide                         pncA49                                              tuberculosis (Fig. 2a). Logistic regression modeling identiﬁed
 Streptomycin                         rpsL50, gidB51                                      signiﬁcant allele–allele interactions between ubiA and embR
 Oﬂoxacin                             gyrA52                                              alleles (Supplementary Fig. 4). We investigated these interactions
 4-Aminosalicylic acid                folCa7, thyAa53                                     through a co-occurrence table of the genes, where each cell
 Ethionamide                          ethA54, inhAa20                                     corresponds to the number of resistant strains with both alleles
 Known AMR genes                      dprE155, ald5, alr56, murA57, pks258, pks1259,      over the total number of strains with both alleles (Fig. 2a). The log
 associated with other                ppsA60, ppsD60, drrB61, drrC61, moeW55,             odds ratio (LOR)—a measurement of the association of the co-
 antibiotics                          Rv068762, mshD63, gyrB52, Rv187764,                 occurrence of both alleles with AMR phenotype—was used to
                                      Rv019465
                                                                                          color each cell in the co-occurrence table (Fig. 2, see Methods).
 The eight antibiotics shown each have an AUC greater than 0.80 (Supplementary Fig. 5)    We observed that the resistant-dominant ubiA alleles (i.e., those
 aNot found in top 40 ranked alleles determined by mutual information, chi-squared, and
 ANOVA F-test
                                                                                          with high positive LOR), 2 and 4, occurred exclusively in the
                                                                                          background of nonsusceptible-dominant embR alleles (Fig. 2a).
                                                                                          Interestingly, in contrast to embB and ubiA, no embR allele
   The SVM method revealed an abundance of AMR-implicated                                 appeared as a clear resistance determinant (Fig. 2a). Furthermore,
genes involved in metabolic pathways (119/317, 37.5%) (Supple-                            neither embR nor ubiA were signiﬁcantly associated with
mentary Data 2). In fact, the majority of the known AMR                                   ethambutol AMR in pairwise associations tests (Table 1 and
determinants are metabolic enzymes (24/33, 73%). We found                                 Supplementary Data 1), showing that our ensemble-based
over 20 genes related to cell wall processes (26/317, 8.2%), which                        machine learning approach uncovers M. tuberculosis AMR
is consistent with previous ﬁndings of convergent AMR evolution                           complexity. In addition to these known AMR determinants of
in M. tuberculosis4. Furthermore, many high-signal AMR genes,                             ethambutol, our analysis implicated ubiA interactions with
such as pbpA and mmpS3, have recently been identiﬁed as                                   Rv3848 in ethambutol resistance (Table 2 and Supplementary
determinants of intrinsic M. tuberculosis AMR16. The full list of                         Data 4). Interestingly, the resistant-dominant allele of Rv3848
identiﬁed genes for each drug is provided (Supplementary                                  occurs exclusively in the background of the AMR-neutral ubiA
Data 2).                                                                                  allele 3, hinting at an alternative route of high-level ethambutol
                                                                                          resistance.
                                                                                             For identiﬁed isoniazid AMR genes, the co-occurrence table
Machine learning uncovers genetic interactions. Beyond iden-                              highlighted cases where either katG or inhA genes provide the
tifying AMR genes, four key attributes of our ensemble SVM                                dominant mode of resistance (Fig. 2b). Speciﬁcally, the incidence
learning approach enable analysis of genetic interactions under-                          of susceptible katG alleles 1, 2, 5, and 6 (i.e., low LOR) with the
lying variable AMR phenotypes (Methods and Supplementary                                  resistance inhA alleles 2 and 3 (i.e., high LOR) showed that
Fig. 4): (1) the weighting of a particular allele in a speciﬁc SVM                        isoniazid resistance in our dataset arose from either katG or inhA
hyperplane scales with its contribution to a particular AMR                               mutations, but not both. Aside from these two highly studied
phenotype, (2) the sign of the weighting (positive or negative)                           isoniazid AMR determinants, epistatic interactions between katG
corresponds to the contribution of that allele to the AMR phe-                            and oxcA appeared with a high signal and further displayed an
notype (i.e., positive weights correspond to resistance while the                         interesting co-occurrence relationship with katG (Fig. 2b). This
negative weights correspond to susceptibility), (3) the magnitude                         epistatic interaction for oxcA has not been previously described;
and sign of an allele weighting is dependent upon the magnitudes                          speciﬁcally, alleles 3 and 7 of oxcA appear exclusively in isoniazid-
and signs of other alleles within the same hyperplane, and (4) the                        resistant strains. While the AMR phenotypes for the strains
use of bootstrapping (i.e., randomized subsampling of the                                 containing these alleles may be attributed to the presence of the
population with replacement), and stochastic gradient descent                             resistance-dominant katG alleles 3 and 7, as is often offered in
ensures variability in the weights, signs, and set of alleles for each                    studies to “explain resistance”, the variation in AMR phenotypes
SVM hyperplane. Motivated by attributes 3 and 4, we hypothe-                              across the different alleles were determined to be signiﬁcant by
sized that two genes may interact if the weights, signs, and                              the machine learning algorithm and thus motivated further
appearance of their alleles are signiﬁcantly correlated across the                        investigation. Co-occurrence tables of epistatic AMR genes are
ensemble of SVM hyperplanes (Methods). Therefore, to identify                             provided for the ten antibiotic classiﬁcations (Supplementary
genetic interactions contributing to AMR in M. tuberculosis                               Data 5).
strains, we constructed a correlation matrix of allele weights
across the ensemble of randomized SVM hyperplanes (Supple-
mentary Data 3) and ﬁltered for the top 60 highest gene–gene                              Structural analysis suggest drivers of selection. Although the
correlations for eight AMR classiﬁcations. The resulting set of                           machine learning results agree with experimental literature, it
gene–gene pairs were interrogated through logistic regression                             remains unclear whether the uncovered genetic features are either
modeling, selecting those gene pairs with statistically signiﬁcant                        true determinants of AMR or possible artifacts of the statistical
allele–allele interactions (P < 0.05; Benjamini–Hochberg correc-                          learning algorithm. To gain additional insight into whether or not
tion) (Methods and Supplementary Fig. 4). This approach                                   the uncovered alleles are causal in AMR evolution, we mapped
uncovered 94 potential genetic interactions (Supplementary                                the alleles of the 254 AMR genes to protein structures using both
Fig. 4).                                                                                  experimental crystal structures (20/254) and predicted homology
   We can use the evolution of ethambutol resistance as a case                            models (50/254) using the ssbio Python package (Methods and
study to examine the output of our approach. Epistasis analysis of                        Supplementary Data 6)19. Out of the 254 genes, 217 had available
ethambutol AMR genes implicated interactions between embB,                                protein sequence annotations (i.e., binding domains, secondary
ubiA, and embR; all genes known to contribute to ethambutol                               structures, etc.). First, we established a positive control by

NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications                                                 3
ARTICLE                                                                                                                               NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y



               a Min       Log odds ratio             Max                       # of resistant strains with
                                                                                both row and column alleles                         # of unique major
                    –                                 +                                                                           lineages comprised                      Selected SVM feature
                                                                                Total # of strains with                            by the strains with
                 Susceptible                 Resistant                       both row and column alleles                               both alleles

                                                                           embB                                                                  embR                         Rv3848
                                1     2       3           4       5          6  7             8         9         10        11          1       2   3           4         1      2          3    #R Total   4

                                –     –       –           –        1   –            –         –         –         –          –          –
                                                                                                                                                1
                                                                                                                                                        –
                                                                                                                                                                8         1    7
                                                                                                                                                                                            –    10   165
                          1                                       1441                                                                          35 1           126 2      7 1 151 2
                                                                                                                             48         9              39                        48                         2
                          2     –     –       –           –        –        –       –         –         –         –                             –               –         –                 –    48   50
                                                                                                                             50 1       9 1            41 1                      50 1
                    ubiA 3      12    92      7   9                –         4   8     6    26   61   92                               116      –      264      –         –     342 25
                                                                                                                                                                                                 384 1030
                                19 1 147 3    7 2 12 2                      10 3 13 2 10 2 469 3 72 2 129 3                            274 3           731 3                    9693 26 1                   0
                                      2                                     1         2                2                                5               3                        8               8    10
                          4     –
                                      2 1
                                              –           –        –
                                                                            1 1       2 1
                                                                                            –     –
                                                                                                       3 2                              6 2
                                                                                                                                                –
                                                                                                                                                        4 1
                                                                                                                                                                –         –
                                                                                                                                                                                10 2
                                                                                                                                                                                     –

                          5     –     2       –           –        –        –       –         –         –         –          –
                                                                                                                                        1
                                                                                                                                                –
                                                                                                                                                        1
                                                                                                                                                                –         –
                                                                                                                                                                                 2
                                                                                                                                                                                            –    2    10    –2
                                      9 1                                                                                               3 1             7 1                     10 1

                         #R 14       99       7           9        1        5       8         9        27         64        158        144      2      330      9         2     444         25
                                                                                                                                                                                                            –4
                        Total 21     166      7       13          147       12      13       13        487        76        201        311      37     828     129        8     1259        26


                                     b                            inhA                                                   oxcA
                                                              1        2        3        1         2         3          4         5         6    7      8           #R Total
                                                           11   2   1                    1    12             –          –         –      3       –       –           18   159
                                                  1       148 1 3 2 1 1                  30 1 68 3                                       48 3
                                                           19   2   16                                                 25                               12           37   145           4
                                                  2                                      –         –         –                    –      –       –
                                                          1272 2 1 16 1                                                106 1                            37 2
                                                          172   –   –                    4   78   29                    1         1   43   14           1           175   175
                                                  3                                      4 1 78 3 29 1                  1 1       1 1 43 3 14 1         1 1                             2
                                                          172 4
                                                          305                            –        –          –         241        –      –       –      62          306   312
                                                  4                    –        –
                                                          311 1                                                        245 1                            64 1
                                      katG                                                                                                                                              0
                                                           19   9               –        3    17                                         6       –      –            30   210
                                                  5                                                          –          –         –
                                                          198 4 10 2                     32 1 1183                                      41 3

                                                  6
                                                          4            –
                                                                             1           –         –         –         5
                                                                                                                                  –      –       –                   5     47           –2
                                                          46                 1 1                                       40 1
                                                          196                            5   108 36                     –         –     29   11                     203   205
                                                  7                    –        –        5 1 1103 36 1                                                  –                               –4
                                                          198 4                                                                         29 4 11 1
                                                          158          –        –        –         –         –        126         –      –       –      28          159   162
                                                  8
                                                          1611                                                        129 1                             28 1

                                               #R 998 15                     18          15       258        66        438        1      96     26     112
                                             Total 1499 17                   18          74       430        66        568       11     180     26     146


Fig. 2 Allele co-occurrence tables of correlated AMR genes. Co-occurrence of epistatic genes identiﬁed in a ethambutol and b isoniazid. For the rows on
the bottom and on the far right, #R refers to the total number of strains that have the allele and are resistant to the speciﬁc drug. Total refers to the total
number of strains that have that allele that were tested on that speciﬁc drug. Each cell is colored by the log odds ratio (LOR) with respect to the AMR
phenotype. The numbers in the bottom right of each allele co-occurrence box describes the number of unique sublineages comprised by the strains with
both alleles (Methods). The alleles enclosed by a purple box represent those chosen as features by the support vector machine (SVM). Note that in some
cases the rows and columns do not sum up to the total strains due to rare cases when strains lack those alleles (Methods)


mapping the alleles of known AMR genes to protein structures                                                            decreases in the presence of ethambutol6, the SNP suggests a
and veriﬁed that resistance-conferring alleles were located in                                                          relative increase over alleles 1 and 3 in expression of the
annotated structural regions that indicate the known mechanism                                                          ethambutol target, embB, through increased DNA binding. For
of action (Supplementary Fig. 7). For example, structural map-                                                          oxcA, the resistance-dominant alleles, 3 and 7, uniquely share
ping of the isoniazid AMR-determinant, inhA, showed that the                                                            mutations at residue 253, which is contained in the thiamin
resistance-dominant alleles of 2 and 3 are located within two                                                           diphosphate-dependent enzyme M-terminal domain and is 4.51
NAD-binding domains (Fig. 3a). The incidence of these two                                                               Å proximal to a mutation at residue 224 shared by most alleles
alleles in proximal NAD-binding domains is congruent with the                                                           (Fig. 3). Notably, oxcA is an essential oxalyl-CoA decarboxylase
experimentally derived mechanism of action, which describes the                                                         enzyme that converts toxic oxalyl-CoA to CO2 and formyl-CoA,
bactericidal effect of tight binding between the isoniazid-NAD                                                          and plays a role in low pH adaptation in E. coli23. The totality of
adduct and inhA20,21. Moreover, the resistance-conferring                                                               studies describing the poisonous effect of glyoxylate24, signiﬁcant
mutations in the NAD-binding domains explains the previously                                                            acid stress in the macrophage environment, use of CO2 as a
described allele co-occurrence of susceptible katG alleles 1, 2, 5,                                                     carbon source25, and the importance of glyoxylate metabolism in
and 6, with resistant inhA alleles 2 and 3, because the isoniazid-                                                      antibiotic tolerance26, all suggest that the uncovered resistance-
NAD adduct results from binding to katG, which would only                                                               conferring adaptations in oxcA increase depletion of oxalyl-CoA
occur if the M. tuberculosis strain lacks the resistance-conferring                                                     through increased binding afﬁnity of the thiamin diphosphate
katG mutation that disables the isoniazid binding opportunity.                                                          cofactor. Without structural models, sequence annotations of
With established conﬁdence through case–controls, we set out to                                                         structural features enabled the delineation of resistant and
analyze the implicated and uncovered AMR genes.                                                                         susceptible allele mutations to unique structural domains—
   Revisiting the ethambutol case study, we noticed that the                                                            highlighting an advantage of our exact-variant perspective
susceptible-dominant embR alleles shared an SNP that is 14.6 Å                                                          (Fig. 3b). We provide a list of newly implicated AMR genes
away from the DNA-binding domain (Fig. 3a). Given that embR                                                             along with their associated antibiotic, key mutation frequency,
is a positive regulator of embB22 and that the expression of embB                                                       and structural protein features (Table 2).

4                              NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications
NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y                                                                                                                                 ARTICLE

 Table 2 Newly proposed AMR genes

 Gene                       Drug                               Dominant allele                           Mutation                         Structural domain feature
 Rv3848                     EMB, XDR                           R: (25/26)                                SNP                              Outside transmembrane helical domain
 embR                       EMB                                S: (2/37, 9/129)                          SNP                              Proximal to DNA-binding domain
 Rv3129                     EMB                                R: (8/11)                                 SNP                              –
 proC                       EMB                                S: (1/27, 11/127)                         SNP                              –
 kdpC                       EMB                                R: (80/91)                                SNP 11                           Inside transmembrane helical domain
 oxcA                       INH                                R: (66/66, 26/26)                         SNP 253                          TPP enzyme M-terminal domain
 chp2                       ETA                                R: (29/37, 34/60)                         SNP 296                          DELs in mutagen and helical domain
 lipD                       ETA                                R: (48/58, 8/12)                          SNP 105                          Inside beta-lactamase domain
 Rv3471c                    ETA, XDR, SM                       R: (48/50)                                SNP 64                           Inside Cupin 1 domain
 mmpL11                     PAS                                R: (35/48)                                SNP 520                          –
 Rv0044c                    PAS                                R: (13/13)                                DEL 137–264                      BAC Luciferase
 Rv0954                     PAS                                R: (34/46, 4/6)                           SNP 223                          Different mutational backgrounds
 Rv2560                     PZA                                S: (6/41)                                 DEL 1–80                         Compositional bias Proline-rich domain
 Rv2090                     RIF, INH                           S: (9/67, 6/46, 5/51)                     SNP 295                          –
 lpqZ                       RIF                                S: (10/91, 12/79)                         SNP 119                          Within opuAC signaling domain
 Rv1597                     RIF, MDR, INH                      R: (18/19)                                SNP 196                          No mutation in methyltransferase domain
 Rv1543                     RIF, MDR                           S: (10/84, 12/80)                         SNP 128                          Proximal to binding domain
 nuoL                       MDR, PAS                           R: (17/17)                                SNP 503                          Outside transmembrane helical domain
 dnaA                       SM                                 R: (22/22)                                SNP 233                          Proximal to nucleotide binding domain 213
 yajC                       SM                                 R: (30/30)                                SNP 87                           Within transmembrane helical domain
 accD5                      OFX, MDR                           R: (16/16)                                SNP 127                          Within CoA carboxyltransferase domain
 Rv3041c                    RIF, OFX, SM, MDR                  R: (20/28, 25/44)                         SNP 140                          SNP in ATP binding domain
 VapC21                     XDR                                R: (14/23, 14/20)                         DEL 88–138                       Within second magnesium binding domain
 The mutation column represents the distinguishing mutation for the resistant or susceptible-dominant allele(s). Abbreviations: R, resistant; S, susceptible; EMB, ethambutol; PAS, para-aminosalicylic acid;
 INH, isoniazid; PZA, pyrazinamide; RMP, rifampicin; SM, streptomycin; OFX, oﬂoxacin; ETA, ethionamide; MDR, multidrug resistant; XDR, extensively-drug resistant




Resistant and susceptible alleles are globally stratiﬁed. Since                                              The pan-genome properties derived by our computational
our set of M. tuberculosis strains spans multiple continents, we                                          platform reﬂect the current understanding of M. tuberculosis
geographically contextualized our set of SVM-derived AMR genes                                            genetic variability. The other three categories of results are
towards delineating possible country-speciﬁc adaptations                                                  intertwined. We recovered 33 known AMR genes and uncovered
(Table 2). We observed that resistant and susceptible alleles of the                                      an additional 24 novel genetic targets. This demonstrates the
identiﬁed AMR genes were stratiﬁed amongst speciﬁc countries of                                           platform’s ability to generate hypotheses that may expand our
origin: resistant-dominant alleles were primarily located in                                              knowledge of the genetic basis of AMR in M. tuberculosis. Some
Belarus, South Africa, and South Korea, while susceptible alleles                                         of these new targets are surprising (e.g., Rv3471c) and some are
were primarily located in India (Table 2). The geographic locality                                        understandable (e.g., oxcA), but all provide an impetus for more
of ethambutol, rifampicin, and isoniazid resistant alleles suggests                                       detailed experimental studies (Supplementary Discussion).
a genetic basis underlying the successful proliferation of M.                                                The third and fourth categories of results are interconnected and
tuberculosis in Belarus—a country with the highest prevalence of                                          detail intricate features underlying M. tuberculosis AMR evolution.
multidrug resistant (MDR) strains ever recorded27. We observed                                            The 74 epistatic interactions revealed are new but in many cases
that the resistant alleles associated with para-aminosalicylic acid                                       involve known gene partners (e.g., ubiA). In other cases, these new
(PAS) were based in the high-burden MDR country of South                                                  epistatic interactions involve novel gene products (e.g., Rv2090).
Korea. Since PAS was a key component in the standard MDR                                                  This novelty, reinforced by structural insights, inform a new line of
treatment regimen of South Korea28, these alleles may represent                                           experimental inquiry (Supplementary Discussion). The larger
speciﬁc adaptations to post-MDR PAS treatment that could be                                               implications of these intricacies are threefold: (1) genetic back-
leveraged to better optimize the regimen. In total, these results                                         ground contributes to AMR phenotypic variation, but may be
portray a geographic basis for M. tuberculosis AMR evolution and                                          subtle (e.g., embR); (2) high-level resistance mutations are pre-
demonstrate that our phylogenetically-agnostic machine learning                                           valent in off-target genes, such as transmembrane proteins (e.g.,
approach is capable of capturing population behavior, which                                               Rv3848); and (3) high-level resistance mutations localize to coun-
often confounds AMR predictions29,30.                                                                     tries with poor M. tuberculosis management (i.e., Belarus). These
                                                                                                          features point to the adverse effects of prolonged treatment31.
                                                                                                             While our framework successfully identiﬁes genetic AMR sig-
Discussion                                                                                                natures, there are limitations to our approach that future efforts
The data deluge on M. tuberculosis and its AMR characteristics is                                         may expand upon. For one, our platform utilizes prior knowledge
likely to continue unabated until all M. tuberculosis strains iso-                                        of known gene–antibiotic relationships and thus does not provide
lated from patients will be sequenced with associated metadata to                                         a means to uniquely deconvolve out an association of a region
guide clinical management. A reference-agnostic computational                                             with a speciﬁc drug (Supplementary Discussion). In addition,
platform needs to be developed to receive, warehouse and con-                                             while our structural analysis provided a foundation for hypo-
tinually analyze this data. We have taken the ﬁrst step at devel-                                         thesizing potential evolutionary drivers, it did not provide further
oping a computational platform to meet this challenge. The                                                support to the causality of an allele. Novel statistical methods may
platform was applied to 1595 sequenced strains to yield results in                                        leverage variations in structural features towards supporting
four categories: pan-genome properties, identiﬁcation of genes                                            causal alleles. Furthermore, our approach lacks the ability to
conferring antibiotic resistance, their epistatic interactions, and                                       understand systemic relationships connecting the alleles on a
protein structure based mechanistic insights.                                                             mechanistic level, such as interacting changes in biochemical ﬂux.

NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications                                                                                                    5
ARTICLE                                                                                               NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y



      inhA                               Alleles              embR                                              oxcA                       Alleles
                                                                                          Alleles
       a                             1      2    3                                 1      2     3 4                            1   2   3   4     5 6  7                    8
                   res 21            –      – SNP                      res 1–7     –      – DEL DEL                    res 11 SNP SNP SNP SNP –    –  –                    –
                 res 194             –    SNP –                        res 110     –     SNP – SNP                  res 29    SNP              SNP –  –                    –
                        #R 998 15 18                                       #R 144        2     330 9              res 224     SNP SNP SNP – SNP SNP SNP                    –
             Isoniazid                                    Ethambutol
                      Total 1499 17 18                                   Total 311       37    828 129            res 253      –   – SNP –       – – SNP                   –
                             NAD binding                                     DNA binding domain                           #R     15    258    66   438 1        96   26   112
                                                                                                            Isoniazid
      NAD binding via amide and carbonyl                                            FHA domain                           Total   74    430    66   569 11      180   26   146
                                                                                                                 TPP enzyme N domain
                                                                                                                 TPP enzyme C domain
                                                                                                                 TPP enzyme M domain




       Rv3471c                Alleles                                  vapC21                                                         kdpC                        Alleles
                                                                                          Alleles
                           1  2     3                4                                                                                                        1      2    3
       b                                                                            1  2  3     4  5                     7
                 res 1–16 – DEL DEL                  –                                                                                               res 11   –      – SNP
                                                                          res 1–24 DEL –  –     –  –                     –
                 res 1–48 DEL –     –                –                                                                                               res 53   –    SNP –
                                                                          res 1–27 – DEL DEL –     –                     –
                   res 17 – DEL DEL                  –
                                                                        res 88–138    DEL –     – DEL                    –                              #R 377 472        90
                   res 64 –   – SNP                  –                                                                                         MDR
                                                                        res 92–138 –   –  – DEL –                        –                            Total 620 840       94
                         #R      0 124 61            0                                                                                  Transmembrane helical domain
               XDR                                                                 #R    4     14   23     36     14 123
                       Total    14 1418 89           28                XDR
                                                                                 Total   13    23   209    77     20 1263
                         #R      5 569 70            14                                                                                yajC                       Allelas
       Streptomycin                                                                        Mg2+ binding site res 8                                           1       2    3
                       Total    11 1265 81           25
                                                                                          Mg2+ binding site res 97                                 res 1–28 –        – DEL
                                Cupin 1 domain                                                                                                                       –    –
                                                                                                                                                     res 87 SNP
                                                                                                                                                       #R30 543 84
      Rv2560                   Alleles                                   Rv3041c                                                      Streptomycin
                                                                                                       Alleles                                       Total
                                                                                                                                                         30 1209 147
                           1   2     4 6                  7                                        1   2     3          4
                                                                                                                                        Transmembrane helical domain
                 res 1–81 DEL –      – –                  –                               res 1–6 DEL DEL –             –
                  res 210 SNP SNP SNP SNP                 –                                 res 7 SNP SNP –             –
                                                                                                                                      accD5                   Alleles
                         #R      6       24   3    91     1                               res 140 SNP      SNP          –                                   1    2    3
     Pyrazinamide
                       Total    41       36   3   114     7                                     #R 20     435    25     172                          res 9 INS INS –
                                                                          Streptomycin
                      Compositional bias proline-rich                                         Total 28    891    44     413                        res 127 SNP –      –

                    Transmembrane helical domain                                                #R 31     592    44     270                            #R     16 722 194
                                                                                     MDR                                                      MDR
                                                                                              Total 33    972    56     477                          Total    16 1142 366
                                                                                     ATP nucleotide binding domain                    CoA carboxyltransferase domain

                                                                                   Min        Log odds ratio      Max
                                # of resistant strains with allele
                                                                                     –                            +                    Reference allele
                               Total # of tested strains with allele
                                                                                   Susceptible               Resistant

Fig. 3 3D and annotated protein structure mutation maps for identiﬁed AMR genes. a 3D protein structures with mapped mutations are shown for inhA,
embR, and oxcA. The colors adjacent to and within the structural mutation table correspond to domains and mutations displayed on the protein structure,
respectively. b Mutation tables for seven new AMR genes. The colors in the mutation table correspond to the incidence of an annotated structural feature
located below the table. The two rows directly below the mutation table are colored according to the log odds ratio between the allele frequency and AMR
phenotype. Two AMR classes are shown for Rv3471c and Rv3041c


Future efforts may integrate genome-scale models of pathogens                                   Methods
towards elucidating and understanding the genetic signatures of                                 M. tuberculosis strain dataset. The selected set of M. tuberculosis strains are
antibiotic resistance32.                                                                        representative of various antimicrobial resistance phenotypes, geographic isolation
                                                                                                sites, and genetic diversity. References for the published and unpublished data sets
   Taken together, the platform presented here meets the pressing                               are provided (Supplementary Discussion, Supplementary Data 7). The sequencing
need for disparate data-type analysis enabled by rapidly growing                                data for the TB Antibiotic Resistance Catalog (TB-ARC) projects (Supplementary
data available for M. tuberculosis pathogenesis and AMR. It both                                Data 7) were generated at the Broad institute. Additional information for each of
recovers known AMR features (i.e., positive control) and reveals                                these unpublished projects can be found at the Broad Institute website. All data
                                                                                                were acquired from the PATRIC database.
new ones. This platform utilizes a unique combination of pan-
genomic analysis, machine learning, structural analysis, and
geographic contextualization. These data types are likely to                                    M. tuberculosis pan-genome construction and QA/QC. We employed QA/QC of
become available for all urgent and serious threat human pro-                                   the constructed 1595 pan-genome by initially ﬁltering out outlier strains. The
karyotic pathogens in the near future. Similar results to those                                 initial selection of 1603 strains was reduced to 1595 upon review of both the cluster
                                                                                                size distribution and the number of unique clusters across the set of all strains
presented here are thus likely to appear on a pathogen-speciﬁc                                  (Supplementary Fig. 3a, b). We found only four strains in the PATRIC database
basis in the coming years.                                                                      that had either a very low (<2000) or high number (>5500) of clusters. The ﬁnal

6                               NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications
NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y                                                                                                         ARTICLE

selection of 1595 strains has a cluster size distribution between 3900 and 4400, and      Furthermore, we performed bootstrapping by randomly selecting a subpopulation
a reasonable unique cluster distribution where the number of unique clusters did          representing 80% of the training data for each SVM simulation.
not exceed 160 (note that unique is deﬁned here as being in only one strain). The             Prior to simulation, we took out the primary resistance-conferring gene of an
pan-genome of all 1595 strains was constructed by clustering protein sequences            antibiotic from the machine learning analysis of other antibiotics in order to
based on their sequence homology using the CD-hit package (v4.6). CD-hit clusters         amplify the signal of other genes—a preprocessing step previously utilized in AMR
protein sequences based on their sequence identity33. CD-hit clustering was per-          gene identiﬁcation studies5 (Supplementary Table 3). For example, all katG alleles
formed with 0.8 threshold for sequence identity and a word length of 5.                   were only accounted for as features in the machine learning analysis for isoniazid.
                                                                                          Furthermore, we removed all mobile element proteins, PE/PPE/PE-PGRS proteins,
                                                                                          transposases, and hypothetical proteins from consideration in the machine learning
Pan-genome core and unique cutoff determination. We determined the core and               analysis due to primarily appearing in the accessory and unique pan-genome of M.
unique pan-genome through sensitivity analysis by plotting the change in core and         tuberculosis which may confound the results. Finally, we balanced the class weight
unique cutoff values by the change in percentage. The cutoffs were chosen to be at        in the SVM algorithm in order to account for the imbalance of resistant and
the point where the second derivative of the curve is the largest. The curve              susceptible strains seen for each drug in our dataset.
represents the change in pan-genome core percentage to changes in the number of               Features were selected from the SVM based on a threshold value. The value was
strains a gene must be found in to be deﬁned as core (Supplementary Fig. 3c, d).          determined through tenfold cross-validation where the threshold value was
                                                                                          optimized through grid search (Supplementary Table 3). The use of bootstrapping
Phylogenetic tree and categorization of lineages. We created a robust phylo-              in the machine learning algorithm may account for biased subpopulations in the
genetic tree of the 1595 strains using SNPs at the core genome. Speciﬁcally, we           data, which often confounds GWAS analysis for M. tuberculosis29,30.
chose a set of 2803 core genes that appeared in at least 1593 strains, included the
H37Rv reference strain (83332.12). We used needle34 to align sequences within the         Filtering of gene sets for epistatic analysis. Leveraging machine learning
2803 pan-genome clusters (a cluster is representative of a particular loci) to the        towards identiﬁcation of genetic interactions, we constructed a correlation matrix
H37Rv reference allele. We built a binary SNP matrix using all of the SNPs                of allele weights across the ensemble of randomized SVM hyperplanes for each
identiﬁed from the 2803 genes (21,206 SNPs in total), and then estimated a                antibiotic (Supplementary File 3). We limited our machine learning analysis to
maximum-likelihood phylogeny using RaXML version 835. The tree was visualized             AMR classiﬁcations that achieved an average AUC (i.e., average area under
using iTOL36.                                                                             ensemble of receiver–operator curves) greater than 0.80 (Supplementary Fig. 5).
    We used an existing SNP typing scheme11 for categorizing the strains into             We selected the top 100 gene–gene correlations that include genes in the top 25
lineages and sublineages.                                                                 ranked SVM alleles for each antibiotic. We limited the correlations to in the top 25
    Speciﬁcally, we used a total of 141 SNPs for identifying lineages and sublineages     ranked alleles in order to avoid the case when low weighted alleles appear sparsely
for our 1595 TB strains. These SNPs were previously determined to be sufﬁcient for        with other low weighted alleles, which lead to signiﬁcant correlations. The resulting
categorizing lineages11. Of these SNPs, 61 were in nonsynonymous sites and the            set of gene–gene pairs were then analyzed using a logistic regression model in order
other 70 were SNPs found in drug resistance genes. These 141 SNPs comprised a             to determine statistically signiﬁcant interactions. The ﬁltering of potential
total of 74 genes. The presence of SNPs were then used to categorize the strains          gene–gene pairs prior to classical quantitative epistasis analysis addresses the
into the deﬁned lineages. Of the 1595 strains, 1366 strains were categorized and 229      problem of combinatorial explosion of pairwise interaction terms in conventional
were uncategorized. The remaining 229 strains were categorized according to their         techniques.
proximity to strains with lineage-deﬁning SNPs, with proximity deﬁned according
to our core genome SNP phylogeny. We have included the frequency of lineage
variants in order to help readers discern between epistatic alleles and those in tight    Epistatic analysis with logistic regression models. We utilized logistic regres-
linkage (Supplementary Data 8). Implicated co-occurring alleles that span different       sion to identify signiﬁcant epistatic interactions. A logistic regression model was
lineages are unlikely to be in tight linkage (i.e., hitchhikers).                         built for each potential gene–gene pair previously determined by the ensemble
    For the numeric subscripts shown in Fig. 2—describing the number of unique            SVM correlation analysis. The variables of the gene–gene logistic regression model
sublineages for each allele–allele pair—were determined as the maximum number             were composed of both alleles and allele–allele interaction variables:
of unique sublineages at a single branch amongst all lineage/sublineage branches..                                 X           X             XX
For example, an allele co-occurrence which has strains in both lineage 1.1 and 1.2                       Y  βo þ      βa þ
                                                                                                                      i i i
                                                                                                                                    β b þ
                                                                                                                                   j Iþj j
                                                                                                                                                        β     ab;
                                                                                                                                                     i;j IþJþk i j
                                                                                                                                                                           ð1Þ
counts as two sublineages. An allele co-occurrence which has strains in both
lineage 1.1, 1.1.2, 1.1.3, 1.1.3.1, 1.1.3.2, and 1.1.3.3 counts as three sublineages
                                                                                          where i and j index the alleles for genes a and b, respectively, I and J are the total
(1.1.3.1, 1.1.3.2, and 1.1.3.3). If an allele co-occurrence has strains in sublineages
                                                                                          number of alleles for genes a and b, respectively, Y is the binary AMR phenotype, k
4.1, 4.1.2, and 4.1.2.1, then only one sublineage is counted, since the strains can be
                                                                                          indexes each unique interaction term, aibj, and β is the regression coefﬁcient
traced through a single lineage (4.1 to 4.1.2 to 4.1.2.1).
                                                                                          corresponding to each predictor. The interaction terms were limited to cases in
                                                                                          which the two alleles co-occur in at least one strain. The interaction variable was
Pan-genome-wide correlation analysis. We performed pairwise association                   the dot product of the two allele presence–absence vectors. In order to account for
analysis for all alleles in the pan-genome and for the 13 antibiotics to identify key     collinearity in the variables, we applied the following three ﬁltering criteria (note
AMR genes. We utilized MI, chi-squared tests, and ANOVA F-tests. MI has many              that ai is interchangeable with bj):
statistical beneﬁts, which include being a nonparametric method that can quantify
nonlinear relationships, unlike Pearson’s correlation which measures a linear             1.   If the allele ai presence–absence is the same as the interaction aibj
relationship. MI has proven to be a natural and powerful means to equitably                    presence–absence, remove the aibj interaction variable from the logistic
quantify statistical associations in large datasets37. The pairwise MI was calculated          regression model
for each column vector in the unique variant pan-genome with each drug sus-               2. If the allele ai presence–absence is equal to allele bj presence–absence, remove
ceptibility vector (Supplementary Fig. 3g). The discrete entropy calculations were             both variables as well as the allele–allele interaction variable, aibj.
carried out using the Non-Parametric Entropy Estimation Toolbox (NPEET,                   3. If the allele ai presence–absence is equal to the sum of all interaction variables
https://github.com/gregversteeg/NPEET). Since both vectors are binary, the naive               involving that allele (i.e., aibj for all j), remove the allele variable, but keep the
implementation of discrete entropy estimation used in NPEET is sufﬁcient. The top              interaction variables.
40 MI associations for 11 drugs are recorded (Supplementary Data 1).                          We ﬁltered for allele–allele interactions with P value < 0.05 after
    Associations were similarly calculated with chi-squared and ANOVA tests. P            Benjamini–Hochberg multiple-testing corrections. The resulting set of gene–gene
values were adjusted using the Bonferroni multiple-hypothesis testing correction.         interactions encompassing signiﬁcant allele–allele interactions were portrayed
Theses statistical tests and corrections were implemented using the python                through allele co-occurrence tables (Supplementary Data 5). Logistic regression
package, statsmodels38. The top 40 associations determined by chi-squared and             and statistical tests were implemented using the python package statsmodels38.
ANOVA F-test were recorded for 10 AMR classiﬁcations (Supplementary Data 1).
                                                                                          Calculation of log odds ratio in allele co-occurrence tables. The odds ratio of
Allele feature selection through support vector machines. The support vector              each cell in the allele co-occurrence tables was determined as follows:
machine (SVM) attempts to account for all variants together by learning a mul-
                                                                                                                                     BR  NR
tidimensional hyperplane that best separates the susceptible and resistant strains.                                           OR ¼           ;                                   ð2Þ
The resulting hyperplane is a function of all exact-variant vectors in the pan-                                                      BS  NS
genome. Since the goal is not to predict resistance with high accuracy, but to
instead extract key insights from the data, we take a feature selection approach by       where BR is the number of strains that have both alleles and are resistant to the
gearing the linear SVM with an L1-norm penalty and stochastic gradient descent            speciﬁed antibiotic, NR is the number of strains that do not have both alleles and
optimization algorithm using the scikit-learn package. The L1-norm enforces               are resistant to the speciﬁed antibiotic, BS is the of strains that have both alleles and
sparsity in the decision function, which is ideal for feature selection. The stochastic   are susceptible to the speciﬁed antibiotic, NS is the number of strains that do not
gradient descent algorithm, in conjunction with the L1-norm, returns a different          have both alleles and are susceptible to the speciﬁed antibiotic. For a single allele,
set of signiﬁcant features each run. Since the chosen SVM does not reach the same         the odds ratio was calculated the same way with each variable representing the
solution, we look at the ensemble of 200 SVM feature selection simulations.               single allele case. If any of the four values (BR, BS, NR, and NS) were zero, 0.5 was

NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications                                                                       7
ARTICLE                                                                                               NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y


added to each value in order to ensure a value when computing the logarithm of                       in MDR Mycobacterium tuberculosis. J. Antimicrob. Chemother. 70,
the odds ratio.                                                                                      2511–2514 (2015).
                                                                                               10.   Wattam, A. R. et al. PATRIC, the bacterial bioinformatics database and
Missing alleles in allele co-occurrence tables counts. The lack of speciﬁc alleles                   analysis resource. Nucleic Acids Res. 42, D581–D591 (2014).
shown in the allele co-occurrence table is due to strains missing some alleles. For            11.   Coll, F. et al. A robust SNP barcode for typing Mycobacterium tuberculosis
example, embB allele 5 is found in 147 strains but only 144 strains have both embB                   complex strains. Nat. Commun. 5, 4812 (2014).
allele 5 and ubiA allele 2 (Fig. 2). Speciﬁcally, the three strains missing the three          12.   Shannon, C. E. A mathematical theory of communication. Bell Syst. Tech. J.
ubiA alleles are the following PATRIC strains as described by their genome                           27, 623–656 (1948).
identiﬁers: 1423432.3, 1448794.3, and 1448824.3. Searching on the PATRIC                       13.   Earle, S. G. et al. Identifying lineage effects when controlling for population
database for either ubiA or Rv3806c results in 0 hits for these organisms. While it is               structure improves power in bacterial association studies. Nat. Microbiol 1,
unlikely that the strain is missing this allele, these limitations are not due to the                16041 (2016).
analysis but instead results from the selection of strains. These events happen quite          14.   Lees, J. A. et al. Sequence element enrichment analysis to determine the
rarely and were accounted for in the partitioning of pan-genome portions. The                        genetic basis of bacterial phenotypes. Nat. Commun. 7, 12797 (2016).
large sample size was able to recapitulate the key genes due to large sample size.             15.   Jaillard, M. et al. Representing genetic determinants in bacterial GWAS with
                                                                                                     compacted De Bruijn graphs. Preprint at https://www.biorxiv.org/content/
Structural protein analysis of identiﬁed AMR genes. For identiﬁed AMR genes,                         early/2017/03/03/113563 (2017).
the ssbio software was used to gain gene-speciﬁc, protein sequence and structure               16.   Xu, W. et al. Chemical genetic interaction proﬁling reveals determinants of
based information about residue-level changes (SNPs and deletions) present in the                    intrinsic antibiotic resistance in Mycobacterium tuberculosis. Antimicrob.
M. tuberculosis alleles19. Each AMR gene was mapped to a reference protein                           Agents Chemother. 61, e01334–17 (2017).
sequence ﬁle obtained from UniProt39 and sequence-based metadata identifying                   17.   Xu, Y., Jia, H., Huang, H., Sun, Z. & Zhang, Z. Mutations found in embCAB,
protein-speciﬁc features (e.g., active sites, secondary structures, and mutations in                 embR, and ubiA genes of ethambutol-sensitive and -resistant Mycobacterium
studied wild-type strains) was used to determine the occurrence of allele-speciﬁc                    tuberculosis clinical isolates from China. Biomed. Res. Int. 2015, 951706
AMR mutations within the gene feature set (Supplementary Data 6). When                               (2015).
available, AMR genes were additionally mapped to experimentally obtained protein               18.   Brossier, F. et al. Molecular analysis of the embCAB locus and embR gene
structures from the RCSB Protein Data Bank or to homology structures generated                       involved in ethambutol resistance in clinical isolates of Mycobacterium
using the Iterative Threading ASSEmbly Reﬁnement (I-TASSER) platform40,41. To                        tuberculosis in France. Antimicrob. Agents Chemother. 59, 4800–4808 (2015).
help elucidate the mechanistic effects of AMR mutations, both AMR mutations and                19.   Mih, N. et al. ssbio: a Python framework for structural systems
the residue-level feature set were mapped to these structures and visualized using                   biology. Bioinformatics 34, 2155–2157 (2018).
the NGLview Jupyter notebook plugin42. The structural information was utilized to              20.   Rozwarski, D. A., Grant, G. A., Barton, D. H., Jacobs, W. R. Jr & Sacchettini, J.
calculate distances between each mutation and annotated protein feature (Sup-                        C. Modiﬁcation of the NADH of the isoniazid target (InhA)
plementary Data 6).                                                                                  from Mycobacterium tuberculosis. Science 279, 98–102 (1998).
                                                                                               21.   Rawat, R., Whitty, A. & Tonge, P. J. The isoniazid-NAD adduct is a slow,
Code availability. The computational platform is provided as a github code                           tight-binding inhibitor of InhA, the Mycobacterium tuberculosis enoyl
repository.                                                                                          reductase: adduct afﬁnity and drug resistance. Proc. Natl Acad. Sci. USA 100,
                                                                                                     13881–13886 (2003).
                                                                                               22.   Sharma, K. et al. Transcriptional control of the mycobacterial embCAB
Data availability                                                                                    operon by PknH through a regulatory protein, EmbR, in vivo. J. Bacteriol. 188,
All data utilized in this study is publicly available at the PATRIC database. Identiﬁers for         2936–2944 (2006).
the 1595 genomes are provided in the Supplementary Information (Supplementary                  23.   Werther, T. et al. New insights into structure–function relationships of oxalyl-
Data7). References for the published and unpublished data sets can be found in the                   CoA decarboxylase from Escherichia coli. FEBS J. 277, 2628–2640 (2010).
Supplementary Information (Supplementary Data 7). The sequencing data for the TB               24.   Puckett, S. et al. Glyoxylate detoxiﬁcation is an essential function of malate
Antibiotic Resistance Catalog (TB-ARC) projects (Supplementary Data 7) were generated                synthase required for carbon assimilation in Mycobacterium tuberculosis. Proc.
at the Broad institute. Additional information for each of these unpublished projects can            Natl Acad. Sci. USA 114, E2225–E2232 (2017).
be found at the Broad Institute website (https://olive.broadinstitute.org/projects/tb_arc).    25.   Beste, D. J. V. et al. 13C metabolic ﬂux analysis identiﬁes an unusual route for
                                                                                                     pyruvate dissimilation in mycobacteria which requires isocitrate lyase and
                                                                                                     carbon dioxide ﬁxation. PLoS Pathog. 7, e1002091 (2011).
Received: 26 January 2018 Accepted: 6 September 2018
                                                                                               26.   Nandakumar, M., Nathan, C. & Rhee, K. Y. Isocitrate lyase mediates broad
                                                                                                     antibiotic tolerance in Mycobacterium tuberculosis. Nat. Commun. 5, 4306
                                                                                                     (2014).
                                                                                               27.   Skrahina, A. et al. Alarming levels of drug-resistant tuberculosis in Belarus:
                                                                                                     results of a survey in Minsk. Eur. Respir. J. 39, 1425–1431 (2012).
                                                                                               28.   Park, J. S. Issues related to the updated 2014 Korean guidelines for
References                                                                                           tuberculosis. Tuberc. Respir. Dis. 79, 1–4 (2016).
1.   Davis, J. J. et al. Antimicrobial resistance prediction in PATRIC and RAST.               29.   Power, R. A., Parkhill, J. & de Oliveira, T. Microbial genome-wide association
     Sci. Rep. 6, 27930 (2016).                                                                      studies: lessons from human GWAS. Nat. Rev. Genet. 18, 41–50 (2017).
2.   Manson, A. L. et al. Genomic analysis of globally diverse Mycobacterium                   30.   Chen, P. E. & Shapiro, B. J. The advent of genome-wide association studies for
     tuberculosis strains provides insights into the emergence and spread of                         bacteria. Curr. Opin. Microbiol. 25, 17–24 (2015).
     multidrug resistance. Nat. Genet. 49, 395–402 (2017).                                     31.   Gagneux, S. et al. The competitive cost of antibiotic resistance
3.   Walker, T. M. et al. Whole-genome sequencing for prediction of                                  in Mycobacterium tuberculosis. Science 312, 1944–1946 (2006).
     Mycobacterium tuberculosis drug susceptibility and resistance: a retrospective            32.   Kavvas, E. S. et al. Updated and standardized genome-scale reconstruction
     cohort study. Lancet Infect. Dis. 15, 1193–1202 (2015).                                         of Mycobacterium tuberculosis H37Rv, iEK1011, simulates ﬂux states
4.   Farhat, M. R. et al. Genomic analysis identiﬁes targets of convergent positive                  indicative of physiological conditions. BMC Syst. Biol. 12, 25 (2018).
     selection in drug-resistant Mycobacterium tuberculosis. Nat. Genet. 45,                   33.   Li, W. & Godzik, A. Cd-hit: a fast program for clustering and comparing large
     1183–1189 (2013).                                                                               sets of protein or nucleotide sequences. Bioinformatics 22, 1658–1659 (2006).
5.   Desjardins, C. A. et al. Genomic and functional analyses of Mycobacterium                 34.   Rice, P., Longden, I. & Bleasby, A. EMBOSS: the European Molecular Biology
     tuberculosis strains implicate ald in D-cycloserine resistance. Nat. Genet. 48,                 Open Software Suite. Trends Genet. 16, 276–277 (2000).
     544–551 (2016).                                                                           35.   Stamatakis, A. RAxML version 8: a tool for phylogenetic analysis and post-
6.   Saﬁ, H. et al. Evolution of high-level ethambutol-resistant tuberculosis through                analysis of large phylogenies. Bioinformatics 30, 1312–1313 (2014).
     interacting mutations in decaprenylphosphoryl-[beta]-D-arabinose                          36.   Letunic, I. & Bork, P. Interactive tree of life (iTOL) v3: an online tool for the
     biosynthetic and utilization pathway genes. Nat. Genet. 45, 1190–1197 (2013).                   display and annotation of phylogenetic and other trees. Nucleic Acids Res. 44,
7.   Zheng, J. et al. para-Aminosalicylic acid is a prodrug targeting dihydrofolate                  W242–W245 (2016).
     reductase in Mycobacterium tuberculosis. J. Biol. Chem. 288, 23447–23456                  37.   Kinney, J. B. & Atwal, G. S. Equitability, mutual information, and the maximal
     (2013).                                                                                         information coefﬁcient. Proc. Natl Acad. Sci. USA 111, 3354–3359 (2014).
8.   Moradigaravand, D. et al. dfrA thyA double deletion in para-aminosalicylic                38.   Seabold, S. & Perktold, J. Statsmodels: econometric and statistical modeling
     acid-resistant Mycobacterium tuberculosis Beijing strains. Antimicrob. Agents                   with python. In Proc. 9th Python Science Conference (eds van der Walt, S. &
     Chemother. 60, 3864–3867 (2016).                                                                Millman, J.) 57 (SciPy, 2010).
9.   Martinez, E., Holmes, N., Jelfs, P. & Sintchenko, V. Genome sequencing                    39.   The UniProt Consortium. UniProt: the universal protein
     reveals novel deletions associated with secondary resistance to pyrazinamide                    knowledgebase. Nucleic Acids Res. 45, D158–D169 (Springer, New York, 2017).


8                                 NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications
NATURE COMMUNICATIONS | DOI: 10.1038/s41467-018-06634-y                                                                                                     ARTICLE

40. Berman, H. M. et al. The protein data bank. Nucleic Acids Res. 28, 235–242        61. Li, G. et al. Study of efﬂux pump gene expression in rifampicin-
    (2000).                                                                               monoresistant Mycobacterium tuberculosis clinical isolates. J. Antibiot. 68,
41. Yang, J. et al. The I-TASSER Suite: protein structure and function                    431–435 (2015).
    prediction. Nat. Methods 12, 7–8 (2015).                                          62. Jang, J. et al. Efﬂux attenuates the anti-bacterial activity of Q203
42. Nguyen, H., Case, D. A. & Rose, A. S. NGLview—Interactive molecular                   in Mycobacterium tuberculosis. Antimicrob. Agents Chemother. doi: 0.1128/
    graphics for Jupyter notebooks. Bioinformatics 34, 1241-1242 (2017).                  AAC.02637-16 (2017).
43. Musser, J. M. et al. Characterization of the catalase-peroxidase gene (katG)      63. Vilchèze, C. et al. Mycothiol biosynthesis is essential for ethionamide
    and inhA locus in isoniazid-resistant and susceptible strains of Mycobacterium        susceptibility in Mycobacterium tuberculosis. Mol. Microbiol. 69, 1316–1329
    tuberculosis by automated DNA sequencing: restricted array of mutations               (2008).
    associated with drug resistance. J. Infect. Dis. 173, 196–202 (1996).             64. Li, X.-Z., Elkins, C. A. & Zgurskaya, H. I. Efﬂux-Mediated Antimicrobial
44. Torres, J. N. et al. Novel katG mutations causing isoniazid resistance in             Resistance in Bacteria: Mechanisms, Regulation and Clinical Implications
    clinical M. tuberculosis isolates. Emerg. Microbes Infect. 4, e42 (2015).             (Springer, New York, 2016).
45. Taniguchi, H. et al. Rifampicin resistance and mutation of the rpoB gene          65. Danilchanka, O., Mailaender, C. & Niederweis, M. Identiﬁcation of a novel
    in Mycobacterium tuberculosis. FEMS Microbiol. Lett. 144, 103–108 (1996).             multidrug efﬂux pump of Mycobacterium tuberculosis. Antimicrob. Agents
46. de Vos, M. et al. Putative compensatory mutations in the rpoC gene of                 Chemother. 52, 2503–2511 (2008).
    rifampin-resistant Mycobacterium tuberculosis are associated with ongoing
    transmission. Antimicrob. Agents Chemother. 57, 827–832 (2013).
47. Louw, G. E. et al. Rifampicin reduces susceptibility to oﬂoxacin in rifampicin-   Acknowledgments
    resistant Mycobacterium tuberculosis through efﬂux. Am. J. Respir. Crit. Care     We thank Anand Sastry for helpful discussions regarding machine learning. This
    Med. 184, 269–276 (2011).                                                         research was supported by the NIH NIAID grant (1-U01-AI124316-01), and the NIH
48. Telenti, A. et al. The emb operon, a gene cluster of Mycobacterium                NIGMS (award U01GM102098).
    tuberculosis involved in resistance to ethambutol. Nat. Med. 3, 567–570
    (1997).                                                                           Author contributions
49. Scorpio, A. & Zhang, Y. Mutations in pncA, a gene encoding pyrazinamidase/        E.K., J.M.M. and B.O.P. conceived and designed the study. E.K. conducted all analysis,
    nicotinamidase, cause resistance to the antituberculous drug pyrazinamide in      with contributions from E.C., N.M., D.H., and J.M.M., E.K., Y.S. and J.M.M. performed
    tubercle bacillus. Nat. Med. 2, 662–667 (1996).                                   the pan-genome analysis. E.K. and D.H. performed the epistatic interaction analysis. E.C.
50. Nair, J., Rouse, D. A., Bai, G.-H. & Morris, S. L. The rpsL gene and              and N.M. developed the 3D protein structural analysis pipeline. E.K., J.T.Y., E.C., N.M.,
    streptomycin resistance in single and multiple drug-resistant strains             Y.S., N.D., A.A., L.Y., D.H., V.N., J.M.M. and B.O.P. provided study oversight, wrote the
    of Mycobacterium tuberculosis. Mol. Microbiol. 10, 521–527 (1993).                manuscript, and edited the manuscript. J.M.M. and B.O.P. managed the study. All
51. Wong, S. Y. et al. Mutations in gidB confer low-level streptomycin resistance     authors reviewed and approved the ﬁnal manuscript.
    in Mycobacterium tuberculosis. Antimicrob. Agents Chemother. 55, 2515–2522
    (2011).
52. Von Groll, A. et al. Fluoroquinolone resistance in Mycobacterium                  Additional information
    tuberculosis and mutations in gyrA and gyrB. Antimicrob. Agents                   Supplementary Information accompanies this paper at https://doi.org/10.1038/s41467-
    Chemother. 53, 4498–4500 (2009).                                                  018-06634-y.
53. Fivian-Hughes, A. S., Houghton, J. & Davis, E. O. Mycobacterium
    tuberculosis thymidylate synthase gene thyX is essential and potentially          Competing interests: The authors declare no competing interests.
    bifunctional, while thyA deletion confers resistance to p-aminosalicylic
    acid. Microbiology 158, 308–318 (2012).                                           Reprints and permission information is available online at http://npg.nature.com/
54. Morlock, G. P., Metchock, B., Sikes, D., Crawford, J. T. & Cooksey, R. C. ethA,   reprintsandpermissions/
    inhA, and katG loci of ethionamide-resistant clinical Mycobacterium
    tuberculosis isolates. Antimicrob. Agents Chemother. 47, 3799–3805 (2003).        Publisher's note: Springer Nature remains neutral with regard to jurisdictional claims in
55. Wang, F. et al. Identiﬁcation of a small molecule with activity against drug-     published maps and institutional afﬁliations.
    resistant and persistent tuberculosis. Proc. Natl Acad. Sci. USA 110,
    E2510–E2517 (2013).
56. Nakatani, Y. et al. Role of alanine racemase mutations in Mycobacterium
    tuberculosis d-cycloserine resistance. Antimicrob. Agents                                           Open Access This article is licensed under a Creative Commons
    Chemother. 61 e01575–17 (2017).                                                                     Attribution 4.0 International License, which permits use, sharing,
57. Eschenburg, S., Priestman, M. & Schönbrunn, E. Evidence that the fosfomycin       adaptation, distribution and reproduction in any medium or format, as long as you give
    target Cys115in UDP-N-acetylglucosamine enolpyruvyl transferase (MurA) is         appropriate credit to the original author(s) and the source, provide a link to the Creative
    essential for product release. J. Biol. Chem. 280, 3757–3763 (2004).              Commons license, and indicate if changes were made. The images or other third party
58. Gopal, P. et al. Pyrazinamide resistance is caused by two distinct mechanisms:    material in this article are included in the article’s Creative Commons license, unless
    prevention of coenzyme A depletion and loss of virulence factor                   indicated otherwise in a credit line to the material. If material is not included in the
    synthesis. ACS Infect. Dis. 2, 616–626 (2016).                                    article’s Creative Commons license and your intended use is not permitted by statutory
59. Philalay, J. S., Palermo, C. O., Hauge, K. A., Rustad, T. R. & Cangelosi, G. A.   regulation or exceeds the permitted use, you will need to obtain permission directly from
    Genes required for intrinsic multidrug resistance in Mycobacterium                the copyright holder. To view a copy of this license, visit http://creativecommons.org/
    avium. Antimicrob. Agents Chemother. 48, 3412–3418 (2004).                        licenses/by/4.0/.
60. Bisson, G. P. et al. Upregulation of the phthiocerol dimycocerosate
    biosynthetic pathway by rifampin-resistant, rpoB mutant Mycobacterium
    tuberculosis. J. Bacteriol. 194, 6441–6452 (2012).                                © The Author(s) 2018




NATURE COMMUNICATIONS | (2018)9:4306 | DOI: 10.1038/s41467-018-06634-y | www.nature.com/naturecommunications                                                                   9
