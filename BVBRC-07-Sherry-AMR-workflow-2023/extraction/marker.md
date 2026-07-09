<!-- BACKFILL 2026-07-05: pdftotext -layout fallback (Marker/Nougat not installed locally).
     Source: paper.pdf (fetched from https://www.nature.com/articles/s41467-022-35713-4.pdf)
     SHA256: 35e3c83f2ecaa386b109858c151d252c1fc28fc444ec6a282422c6414b4847c2
     DOI: 10.1038/s41467-022-35713-4
     Backfill this later from the central Marker corpus (SCOUT/OSTI manifests on Eagle) keyed on the above sha256 or DOI. -->

                                    Article                                                                                                       https://doi.org/10.1038/s41467-022-35713-4


                                    An ISO-certiﬁed genomics workﬂow
                                    for identiﬁcation and surveillance of
                                    antimicrobial resistance
                                    Received: 1 June 2022                                 Norelle L. Sherry 1,2,3, Kristy A. Horan1, Susan A. Ballard 1,
                                                                                          Anders Gonҫalves da Silva1, Claire L. Gorrie 3, Mark B. Schultz 1,
                                    Accepted: 21 December 2022
                                                                                          Kerrie Stevens1, Mary Valcanis1, Michelle L. Sait1, Timothy P. Stinear                     3
                                                                                                                                                                                      ,
                                                                                          Benjamin P. Howden 1,2,3,4 & Torsten Seemann 1,3,4

                                        Check for updates


1234567890():,;   1234567890():,;
                                                                                          Realising the promise of genomics to revolutionise identiﬁcation and surveil-
                                                                                          lance of antimicrobial resistance (AMR) has been a long-standing challenge in
                                                                                          clinical and public health microbiology. Here, we report the creation and
                                                                                          validation of abritAMR, an ISO-certiﬁed bioinformatics platform for genomics-
                                                                                          based bacterial AMR gene detection. The abritAMR platform utilises NCBI’s
                                                                                          AMRFinderPlus, as well as additional features that classify AMR determinants
                                                                                          into antibiotic classes and provide customised reports. We validate abritAMR
                                                                                          by comparing with PCR or reference genomes, representing 1500 different
                                                                                          bacteria and 415 resistance alleles. In these analyses, abritAMR displays 99.9%
                                                                                          accuracy, 97.9% sensitivity and 100% speciﬁcity. We also compared genomic
                                                                                          predictions of phenotype for 864 Salmonella spp. against agar dilution results,
                                                                                          showing 98.9% accuracy. The implementation of abritAMR in our institution
                                                                                          has resulted in streamlined bioinformatics and reporting pathways, and has
                                                                                          been readily updated and re-veriﬁed. The abritAMR tool and validation data-
                                                                                          sets are publicly available to assist laboratories everywhere harness the power
                                                                                          of AMR genomics in professional practice.


                                    Antimicrobial resistance (AMR) is an increasingly well-recognised                include the fact that phenotypic testing can be performed more
                                    threat to global health1–3. A clear understanding of the genomic and             rapidly than genotypic testing for many common pathogens, and the
                                    mechanistic basis for AMR is required to inform clinicians and public            correlation between genotype and phenotype can be variable due to
                                    health teams, from the level of individual patients through to                   incomplete knowledge of AMR mechanisms that impact function4,8.
                                    population-level surveillance4,5. By providing additional, timely data on        However, technological advances in whole genome sequencing (WGS)
                                    acquired AMR genes or gene mutations that confer resistance, geno-               means the process is becoming more cost-effective and the turn-
                                    mic sequencing has the potential to signiﬁcantly enhance AMR sur-                around time for sequencing a microbial genome is decreasing
                                    veillance and inform patient treatment beyond conventional                       signiﬁcantly9.
                                    phenotypic susceptibility testing methods6,7.                                         A lack of international standards for genomic detection of AMR
                                          The use of genomics in the detection and surveillance of bacterial         mechanisms means it is difﬁcult to compare results between
                                    AMR is lagging behind other applications of genomics, such as strain             laboratories10,11. To facilitate implementation, the development of
                                    typing and phylogenetic analysis. Contributors to the lack of uptake             standardised and extensive open-access AMR databases and the


                                    1
                                     Microbiological Diagnostic Unit Public Health Laboratory (MDU-PHL), Department of Microbiology & Immunology, University of Melbourne at the Peter
                                    Doherty Institute for Infection & Immunity, Melbourne, Victoria, Australia. 2Department of Infectious Diseases, Austin Health, Heidelberg, Victoria, Australia.
                                    3
                                     Department of Microbiology & Immunology, University of Melbourne at the Peter Doherty Institute for Infection & Immunity, Melbourne, Australia. 4These
                                    authors jointly supervised this work: Benjamin P. Howden, Torsten Seemann.        e-mail: bhowden@unimelb.edu.au


                                    Nature Communications | (2023)14:60                                                                                                                          1
Article                                                                                                                          https://doi.org/10.1038/s41467-022-35713-4


validation of bioinformatic analytical tools for the detection of AMR is                          validation dataset could be adopted for use in public health and clin-
crucial4,12. Another hurdle to the acceptance and implementation of                               ical sequencing laboratories to assist those involved in AMR surveil-
AMR genomics is how the data can be meaningfully reported outside                                 lance and clinical applications.
of research or reference laboratory settings4. If the implementation of
WGS for AMR is going to be accepted for the detection of AMR resis-                               Results
tance, it is important to consider the way in which complex genomic                               The abritAMR bioinformatics pipeline
data is presented to clinicians, nurses, public health surveillance                               abritAMR is a pipeline for characterisation and reporting of AMR
teams, and other stakeholders with varying understanding of geno-                                 determinants from bacterial sequences, adapting the AMRFinderPlus
mics, and thus how to interpret ﬁndings13. This is a gap in the bioin-                            tool and database for use in clinical and public health microbiology.
formatic tools currently available for AMR, as outputs are not usually                            Using the outputs from AMRFinderPlus, AMR mechanisms are further
tailored for clinical reports, or easily modiﬁable to suit local reporting                        classiﬁed by antimicrobial class and/or mechanism to suit clinical and
requirements.                                                                                     public health microbiology (CPHM) needs, and subsequently ﬁltered
     In many countries, clinical and public health microbiology                                   according to local reporting requirements, with results ready for
laboratories are required to meet International Standards Organiza-                               incorporation into sample reports (overview Fig. 1, outputs Fig. 2;
tion (ISO), or ISO-equivalent, standards to be accredited to operate14.                           further details available in Methods and Supplementary Figure 1). An
These standards require the implementation of standardised operat-                                additional module generates inferred susceptibility results (currently
ing procedures, quality management systems, staff training and rig-                               validated for Salmonella spp.; output Fig. 2, reporting logic detailed in
orous validation of all processes used to generate results and reports in                         Supplementary Figure 2).
each laboratory15. Currently, the relevant standards for medical
laboratories (last released in 2012) are not designed to assess the                               Validation of the abritAMR pipeline: overview
performance of bioinformatic tools, making validation to meet these                               To validate the abritAMR pipeline, we compared performance to PCR
standards difﬁcult for laboratories, in addition to the paucity of                                results for key AMR genes, to AMRFinderPlus results on synthetic read
publicly-available validation datasets4.                                                          data from reference genomes, and to phenotypic data for Salmonella
     Here we design and validate a bioinformatic tool, abritAMR, a                                spp. (Fig. 3).
wrapper for the NCBI AMRFinderPlus tool16 for the detection of AMR                                     abritAMR performed very well against the four validation panels,
determinants from whole genome sequencing data16, with outputs                                    with an overall accuracy of 99.9% (95% CI 99.9–99.9%), sensitivity
adapted for clinical and public health microbiology reporting. We                                 97.9% (97.5-98.4%), and speciﬁcity 100% (100-100%) (Table 1). Impor-
envisage that this pipeline, extensive validation methods and                                     tantly, the abritAMR pipeline was reliable for the high-risk AMR gene



                                                              Input: genome assembly in FASTA format
                                                                                               Mutation
                                                                               AMR gene


                  AbritAMR
                                               AMR gene detection                     Mutational resistance detection
                                                 (all samples)                       (validated species samples only)

                                                        AMR gene                                           Mutation




                            AMRFinderPlus
                                                   AMR protein database
                                                                                                 AMR mutation database

                                                 Output allele / gene name
                                                 of matched AMR protein                       Output details of AMR mutation
                                                                                                                                        Report outputs



                        Classification       Genes binned                                  Mutations binned
                                                                     Class 1                                          Class 2
                                             by functional           geneA                 by functional              Mutation
                                                                                                                                    Output: “Detailed Report”

                          database
                                             AMR class                                     AMR class




                        Reporting
                                            1. Classifies as reportable or                1. Combines AMR genes and              Output: “Final AMR gene report”
                                               non-reportable (by species)                   mutations
                                            2. Limits reporting of intrinsic              2. Creates inferred antibiogram
                          logic
                                                                                                                                 Output: “Inferred antibiogram
                                               AMR mechanisms                                (validated species only)                     report”



Fig. 1 | Overview of abritAMR pipeline. Assembled bacterial genomic sequence                      Report output, Fig. 2 and Supplementary Data 1). An additional step then applies
data (short- or long-read or hybrid assemblies, fasta format) are inputted in to the              reporting logic tailored to local requirements to produce per-isolate reports with
abritAMR pipeline to identify acquired AMR genes and mutations. The pipeline                      acquired AMR genes, excluding common intrinsic AMR genes from being reported
implements the AMRFinderPlus tool, identifying AMR genes (BLASTx search), and                     in speciﬁc species (Final AMR Gene Report), and phenotypic inference for speciﬁed
optionally identiﬁes mutations associated with AMR for speciﬁed species where                     species, where validated (Inferred Antibiogram Report, Fig. 2 and Supplementary
mutational data are available. Identiﬁed AMR genes + /− mutations are then binned                 Data 1). AMR, antimicrobial resistance.
into functional AMR classes according to the classiﬁcation database (Detailed



Nature Communications | (2023)14:60                                                                                                                                               2
Article                                                                                                              https://doi.org/10.1038/s41467-022-35713-4




Fig. 2 | Examples of abritAMR pipeline outputs. This ﬁgure demonstrates abri-          as notiﬁable AMR mechanisms) from lower-priority groups, (iii) identiﬁcation of
tAMR features and outputs across four different species (genome sequence A,            clinically-relevant AMR mechanisms within a drug class (e.g. separation of ESBLs
Escherichia coli; genome sequence B, Klebsiella pneumoniae; genome sequence C,         and AmpCs from genes encoding ﬁrst-generation cephalosporin resistance;
Acinetobacter baumannii; genome D, Salmonella enterica). The horizontal lanes          separation of metallo-beta-lactamase (MBL) carbapenemases and other carbape-
represent the different output stages: top lane, raw AMRFinderPlus output; middle      nemases due to differences in patient treatment), and (iv) application of tailored
lane, abritAMR Detailed Report output (aligned to and binned by Enhanced Sub-          reporting logic to separate reportable and non-reportable genes according to local
class from abritAMR’s classiﬁcation database); bottom lane, abritAMR’s Final AMR       requirements, thus de-cluttering the report for clinicians and public health teams.
Gene Report (genomes A-C) after application of tailored reporting logic to meet        Note, only ‘Exact’ matches (100% sequence identity and coverage) and ‘Close’
local requirements, and Inferred Antibiogram Report (genome D), currently vali-        matches (90-<100% identity and 90-<100% sequence coverage) from the AMRFin-
dated for Salmonella spp. Key features include: (i) simpliﬁcation of mechanism or      derPlus tool are reported by abritAMR. Abbreviations: MBL, metallo-beta-lacta-
drug class bins, (ii) identiﬁcation and separation of high-priority AMR groups (such   mase; ESBL, extended-spectrum beta-lactamase.


classes that are notiﬁable as part of our national critical antimicrobial              suspected CPE isolates such as these), as different colonies with and
resistance surveillance system (CARAlert) in Australia17, with 99.9%                   without the ESBL/AmpC gene may have been picked for PCR and WGS,
accuracy (95% CI 99.9–100%), 98.9% sensitivity (98.3–99.3%) and 100%                   potentially explaining these discrepancies. No discrepant results were
speciﬁcity (100–100%) across these classes (carbapenemases, 16 S                       detected for mecA and van gene detection, and only one allele was
ribosomal methyltransferases, mobile colistin resistance genes, ESBLs                  incorrectly assigned compared to Sanger sequencing (99.7% accuracy)
(including AmpCs), vancomycin resistance genes, and oxazolidinone                      (Table 1 and Fig. 4). Overall performance of abritAMR against PCR
and phenicol resistance (optrA, cfr and poxtA genes)).                                 yielded 99.6% accuracy (95% CI 99.0-99.9%), 99.6% sensitivity (99.0-
                                                                                       99.9%) and 99.4% speciﬁcity (97.9-99.9%).
Validation results compared to PCR and Sanger sequencing
The abritAMR pipeline was highly accurate compared to PCR (carba-                      Identiﬁcation of AMR genes from synthetic reads
penemase, ESBL, van and mec gene PCRs) with 1179/1184 (99.6%)                          The presence or absence of 415 AMR genes across 321 genomes (133215
resistance genes correctly detected, and compared well to Sanger                       alleles) was tested by running abritAMR on synthetic reads from
sequencing (carbapenemase allele calling) with 355/356 (99.7%) alleles                 complete reference genomes, and comparing to the (native) AMRFin-
correctly identiﬁed by WGS. After discrepancy resolution (including                    derPlus results on the complete genome, considered the ‘gold stan-
repeat PCR and/or WGS, or examination of partial genes detected by                     dard’ (Fig. 3). Overall accuracy of AMR gene detection by abritAMR was
abritAMR), ﬁve discrepancies between PCR and WGS results remained,                     excellent, with 133127/133215 alleles called correctly, resulting in 99.9%
including three potential false negatives (PCR positive, WGS negative)                 accuracy (95% CI 99.9-99.9%), 97.5% sensitivity (96.9-98.0%), and 100%
consisting of one CTX-M and two CMY genes not detected by abri-                        sensitivity (100-100%) (Fig. 5). Note that any discrepancies here include
tAMR; at least one of these was due to the presence of a contig break in               differences in abritAMR performance compared to AMRFinderPlus, as
the gene leading to smaller fragments not detected by AMRFinderPlus.                   well as differences between complete genomes and (synthetic) short-
Additionally, two potential false positives (PCR negative, WGS posi-                   read data, which likely accounts for at least a proportion of the dis-
tive) were identiﬁed, one CMY-42 and one IMP-62, conﬁrmed by repeat                    crepant results.
PCR and sequencing; both genes were reported to be within the                                The majority of discrepancies were false negatives, with the ami-
inclusivity range of the assay as per the manufacturer’s instructions,                 noglycoside AMR genes being most common (32/88, 36.4%), especially
although this was validated by in silico PCR by the manufacturer (and                  the aac(6’)-Ib family, implicated in 18 false negatives, and speciﬁcally
observed in our dataset). Alternatively, these discrepancies may be due                the aac(6’)-Ib-cr5 allele (11/18). Some of these were detected as partial
to plasmid dropout in culture (which is commonly observed with                         genes at the site of contig breaks, possibly related to slightly higher GC


Nature Communications | (2023)14:60                                                                                                                                     3
Article                                                                                                                    https://doi.org/10.1038/s41467-022-35713-4



                A                        DNA extraction and
                                          library preparation                             B                      Download closed genome




                  Whole genome sequencing                       Detect AMR genes             Fragment closed genome                   Identify true AMR genes
                   to create short read data                        with PCR               to create synthetic read data                with AMRFinderPlus




                       Conduct de novo                                                           Conduct de novo
                       genome assembly                                                           genome assembly
                                  contig 1                                                                   contig 1
                                   contig 2                                                                   contig 2
                                    contig 3                                                                   contig 3




                                               AbritAMR                                                                    AbritAMR
                                  Detect AMR genes with AbritAMR                                             Detect AMR genes with AbritAMR


                                      Output detected AMR genes                                                 Output detected AMR genes



                                    Compare AMR gene results                                                  Compare AMR gene results

Fig. 3 | Validation of abritAMR outputs compared to PCR and synthetic read             platforms) to mimic library preparation from bacterial DNA. Synthetic reads then
data. A Validation compared to PCR data – Assembled short-read sequence data           underwent the same analytical processes as for usual usage (genome assembly and
from bacterial isolates are run through the abritAMR pipeline and compared to          input into abritAMR pipeline). These results were then compared to AMRFinderPlus
multiplex real-time PCR results for the same AMR genes. B Synthetic data – where       results on the complete bacterial reference genomes, minimizing the risk of dis-
no validation dataset or PCR assay was available for comparison, synthetic read        cordant results due to disparities between AMR databases. Abbreviations: AMR,
data were generated from publicly-available closed reference genomes by frag-          antimicrobial resistance; PCR, polymerase chain reaction. Source data are provided
mentation with the art-illumina tool45 (using the error proﬁle from local sequencing   as a Source Data ﬁle.



content (leading to lower sequence coverage) in these genes. The                       Validation of inferred antibiogram (Salmonella spp.)
other major theme was difﬁculty resolving sequences with multiple                      Validation of inferred phenotype against phenotypic AST data
alleles of the same gene family, which were often collapsed into a                     demonstrated 98.9% accuracy (95% CI 98.7–99.1%), 98.9% sensitivity
single gene detection by abritAMR or miscalled as a different allele. For              (98.4–99.3) and 98.9% speciﬁcity (98.7–99.1%) overall (Table 1, Sup-
example, this included a sequence with CTX-M-3, CTX-M-14 and CTX-                      plementary Table 2 and Fig. 6). Accuracy of phenotypic inference was
M-65 identiﬁed by AMRFinderPlus, and called as CTX-M-3 and CTX-M-                      ≥98% for 11/13 antimicrobials (85%), with lower accuracy identiﬁed for
24 by abritAMR. Four out of the ﬁve ‘false positive’ detections were                   streptomycin (95.5%, 95% CI 93.7–96.9%) and ciproﬂoxacin (96.8%,
actually allele miscalls within the same gene family. Collapse of repe-                95% CI 95.4–97.8%), similar to previous ﬁndings using different
ated regions or duplicate alleles is often a feature of short-read                     bioinformatic methods21.
sequencing, hence the discrepancies here may be a feature of com-                           A number of ‘false positive’ results were identiﬁed for strepto-
paring (synthetic) short-read data to complete genomes, rather than a                  mycin (resistant genotype [AMR genes or mutations detected], sus-
feature of abritAMR. Notably, use of alternative genome assembly tools                 ceptible phenotype; n = 30/716 (4.2%) isolates). The AMR genes
(SKESA18 and SPAdes19) did not resolve the discrepancies, with similar                 detected in phenotypically susceptible isolates were also detected in
performance to Shovill20 (based on SPAdes; Supplementary Table 1).                     non-susceptible isolates, although the non-susceptible isolates more
                                                                                       often had >1 AMR gene (1 AMR gene, 22% phenotypically resistant; 2 or
Limit of detection and precision                                                       more AMR genes, 81.4% phenotypically resistant), suggesting that
The limit of detection of the abritAMR pipeline was assessed to                        these AMR mechanisms had small but additive effects on phenotype.
determine the minimum average sequencing depth for acceptable                          Evaluation of phenotype-genotype concordance for azithromycin
accuracy of AMR gene detection (as required for clinical microbiology                  identiﬁed ﬁve ‘false negatives’ (susceptible phenotype, no AMR
validation and accreditation). Accuracy was found to be consistent                     mechanism detected) and two ‘false positives’ (AMR mechanism
(99.9%) across the 40X to 150X range, with 40X being the minimum                       detected but phenotypically susceptible; neither isolate carried the
coverage accepted by our accredited quality control (QC) pipeline.                     dominant resistance mechanism for azithromycin in Salmonella spp.
Repeatability and reproducibility (precision) were assessed (replicates                (mph(A); one carried mef(B), an efﬂux pump with variable activity, and
within and across sequencing runs) and found to be 100% concordant.                    one carried ere(A), an esterase with lower afﬁnity for azithromycin22).


Nature Communications | (2023)14:60                                                                                                                                    4
Article                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    https://doi.org/10.1038/s41467-022-35713-4


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Similar to streptomycin, ciproﬂoxacin also had a number of




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ‘Detected’ refers to AMR gene detected in reference dataset (PCR/allelic variant/synthetic reads) and also in abritAMR results from WGS.




                                                                                                                                                    Sensitivity (%, 95% CI) Speciﬁcity (%, 95% CI) PPV (%, 95% CI) NPV (%, 95% CI)
                                                                                                                                                                                                                                                                                                      99.9 (99.9–99.9)




                                                                                                                                                                                                                                                                                                                                                         99.8 (99.6–99.9) 99.9 (99.9–99.9)
                                                                                                                                                                                                                                                                       99.1 (97.5–99.8)                                                                                                                   100 (99.9–100)                               99.7 (99.6–99.8)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 phenotype-genotype mismatches, likely due to low-level resistance
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 conferred by AMR mechanisms. Isolates with one AMR gene most
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 often had an intermediate phenotype (81.3% intermediate, 12.4%
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 resistant, 6.2% susceptible), whilst isolates with ≥2 AMR genes were all
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 phenotypically resistant. Despite these discordances, the best corre-




Table 1 | Performance characteristics of abritAMR bioinformatic pipeline for detection of acquired AMR genes and inferred phenotype from WGS data
                                                                                                                                                                                                                                                                                                                                                                                                                                                       96.1 (95.2–96.8)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 lation between genotype and phenotype (S/I/R) was determined



                                                                                                                                                                                                                                                                       99.8 (99.1–100)                99.8 (99.6–100)                                                                                     99.8 (99.5–100)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 according to the number of AMR mechanisms detected (any type).
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 This was coded into the reporting logic: absence of AMR mechanisms,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ‘susceptible’, one AMR mechanism, ‘intermediate’, two or more AMR




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ‘Not detected’ refers to AMR genes detected in reference dataset, but not WGS.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 mechanisms, ‘resistant’. In this application, the use of an ‘intermediate’
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 category implies that MICs are likely to be borderline for these sam-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ples, i.e. may test susceptible or resistant on AST. Note that these
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 results are only used for epidemiologic purposes (not for patient



                                                                                                                                                                                                                                                                       99.4 (97.9–99.9)               100 (100–100)                                      100 (100–100)                                    100 (100–100)                                98.9 (98.7–99.1)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 treatment), and hence over-calling resistance is more suitable for this
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 purpose than non-detection of AMR mechanisms.

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Sample outputs and incorporation into microbiology report
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Two different outputs are used in the abritAMR pipeline: (i) Detailed
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Report output, where AMR genes or mutations are shown by enhanced
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 subclass, as classiﬁed by the abritAMR database, and (ii) Final AMR




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               CI conﬁdence interval, PPV positive predictive value, NPV negative predictive value, WGS whole genome sequencing, AMR antimicrobial resistance, AST antimicrobial susceptibility testing; X, times.
                                                                                                                                                                                                                                                                       99.6 (99.0–99.9)               97.5 (96.9–98.0)                                   97.9 (97.5–98.4)                                 98.9 (98.3–99.3)                             98.9 (98.4–99.3)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Gene Report output (binned into reportable and non-reportable
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 genes) after reporting logic is applied (Fig. 2 and Supplementary
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Data 1). An example of the output of the additional module incorpor-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ating mutational resistance and Inferred Antibiogram Report pheno-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 type (currently validated for Salmonella spp.) is also shown in
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Supplementary Data 1.




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             100% repeatability and reproducibility (within- and between-run
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Implementation processes



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               a




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Accuracy 99.9% at all coverage levels tested (40X – 150X)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 After the validation process, implementation processes included




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Presence or absence of each of 415 AMR gene alleles was assessed across the 321 genomes, resulting in 133215 alleles for comparison across the dataset.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 modifying report outputs, integration with the existing LIMS, and




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Accuracy 99.7% (355/356 alleles correctly identiﬁed)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 documentation of the standard operating procedure (SOP). Multiple
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 groups were consulted on the proposed report outputs, including
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 reporting scientists with domain expertise (ensure results were easily
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 interpretable and met reporting obligations across different patho-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 gens), quality management staff (ensure results met legal require-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ments), and end-users (public health teams and clinicians).
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Subsequently, all staff involved in detection, reporting or interpreta-




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             precision)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 tion of AMR results were trained in the use and interpretation of


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               b
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 abritAMR, and clients were educated about the change (although only




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Calculated by drug class (enhanced subclass from classiﬁcation database). Range of sensitivity varied from 70-100% for each subclass (see Supplementary Table 3 for subclasses, and Fig. 5 for performance across subclasses).
                                                                                                                                                    Accuracy (%, 95% CI)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 minimal differences were noticeable to clients, such as change in
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 report formats) before full implementation into routine workﬂows.



                                                                                                                                                                                                                                                                       99.6 (99.0–99.9)               99.9 (99.9–99.9)                                   99.9 (99.9–99.9)                                 99.9 (99.9–100)                              98.9 (98.7–99.1)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Implementation led to streamlined workﬂows, including rapid bioin-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 formatic processing of large sequencing runs (AMR gene detection for
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 a 96-sample run completed in <3 min with 256 CPUs), and less manual
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 re-classiﬁcation of AMR gene results by laboratory scientists (e.g.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 moving genes between reportable and non-reportable ﬁelds, removing
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 intrinsic AMR genes from reportable ﬁelds).




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Critical AMR subclasses – deﬁned as classes containing AMR genes nationally-reportable to the CARAlert program. Includes all carbapenemases, ESBL, ESBL (AmpC type), ribosomal methyltransferases, colistin, oxazolidinone & phenicol resistance, vancomycin.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               c




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Sanger sequencing for allelic variants (n = 356 alleles)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Discussion




                                                                                                                                                                                                                                                                                                 Synthetic reads (n = 321 isolates, 133215 allelesa,b)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 The use of genomics in clinical and public health microbiology (CPHM)




                                                                                                                                                                                                                                                                                                                                                                                                                                                       Inferred phenotype concordance with AST (all
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 has increased substantially in the last decade, particularly in the ﬁelds




                                                                                                                                                                                                                                                                                                                                                         Overall performance (PCR & synthetic data)   Critical AMR subclassesc (all validation sets)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 of pathogen typing and outbreak investigations5,7,23. Detection of AMR
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 from WGS data has somewhat lagged behind other applications of
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 WGS, likely due its inherent complexity in comparison to simple and




                                                                                                                                                                                                                                     Detection of acquired AMR genes
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 effective phenotypic AST4. This complexity is multi-faceted but
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 includes the vast array of resistance mechanisms for testing (a single
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 phenotype may be encoded by many different AMR mechanisms), and




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Precision (n = 13 isolates)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               d




                                                                                                                                                                                                                                                                       PCR (n = 1184 isolates)                                                                                                                                                         antimicrobials)d
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 the limitations of phenotype-genotype correlation, particularly for




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Inferred phenotype validation for Salmonella spp., compared to agar dilution (CLSI methods and 2020 breakpoints). Detailed performance metrics available in Supplementary Table 2 and Fig. 6.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 less-common organisms and drug classes24,25. If not addressed sys-



                                                                                                                                                    Validation panel                                                                                                                                                                                                                                                                                                                                                                                                    Limit of detection
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 tematically, these issues may render genomic AMR difﬁcult to identify
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 comprehensively across all pathogens seen in a CPHM laboratory, and
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 difﬁcult to communicate to clinicians and public health units13,26.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Globally, the paucity of highly accurate, reproducible bioinfor-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 matic tools for detection of AMR mechanisms has been recognised as


Nature Communications | (2023)14:60                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      5
Article                                                                                                                                                                                                     https://doi.org/10.1038/s41467-022-35713-4


                                A                                                            B
                                                                                                                        50




                                 Number of genes detected                                    Number of genes detected
                                                                                                                        40
                                                            20                                                                                                                                        Final result after
                                                                                                                        30                                                                            discrepancy testing
                                                                                                                                                                                                           False negative
                                                            10                                                          20                                                                                 False positive
                                                                                                                                                                                                           True negative
                                                                                                                        10                                                                                 True positive
                                                             0                                                           0

                                                                   mecA   none                                                                                vanB   vanC                  none
                                                                                                                                                                                vanA & B
                                                                                                                                 vanA

                                                             mec genes detected
                                                                                                                                            van genes detected
                                C1                                                                                      C2
                                                                    *




                                 Number of genes detected                                                                    Number of genes detected
                                                                                                                                                        300
                                                            300

                                                                                                                                                        200
                                                            200
                                                                                         *                                                                                                                                  *
                                                            100                                                                                         100
                                                                                 *
                                                                                     *
                                                                                                                                                                                                             *
                                                              0                                                                                           0                 *                *                       *                *
                                                                                                                                                                                       OXA−181
                                                                                                                                                                                                   CMY−109
                                                                                                                                                                                                                               CTX−M−15
                                                                           GES
                                                                             IMI                                                                                IMP−1
                                                                                                                                                               IMP−14                              CMY−116
                                                                                                                                                                                                   CMY−129
                                                                            IMP                                                                                IMP−15                              CMY−141
                                                                                                                                                                                                   CMY−145
                                                                                                                                                                                                                                CTX−M−3
                                                                                                                                                                                                   CMY−150
                                                                                                                                                                                       OXA−232
                                                                           KPC
                                                                          NDM                                                                                  IMP−26
                                                                                                                                                                IMP−4                              CMY−152
                                                                                                                                                                                                    CMY−16
                                                                                                                                                                                                     CMY−2
                                                                           SME                                                                                 IMP−62                               CMY−39
                                                                                                                                                                                                                               CTX−M−55
                                                                                                                                                                                                    CMY−42
                                                                                                                                                                                        OXA−48
                                                                            VIM
                                                                    OXA−23−like                                                                                 IMP−7                               CMY−48
                                                                                                                                                                                                     CMY−6
                                                                                                                                                                                                    CMY−63
                                                                    OXA−48−like                                                                                                                     CMY−65
                                                                                                                                                                                                       CMY
                                                                    OXA−51−like
                                                                    OXA−58−like
                                                                           CMY                                                                                                       OXA−48−like                               CTX−M−62
                                                                  CTX−M group 1
                                                                  CTX−M group 9
                                                                           none                                                                                                                                             CTX−M group 1
                                                                                                                                                                     IMP        OXA-48-like          CMY              CTX-M group 1
                                      CP and ESBL gene classes detected                                                                                        Discrepant CP and ESBL classes; gene breakdown
Fig. 4 | Performance of abritAMR pipeline to detect AMR mechanisms com-                                                                                              multiplex PCR (vanA/B/C). Panel C1, detection of genes within carbapenemase and
pared to PCR. Each panel details the identiﬁcation of AMR mechanisms by abri-                                                                                        ESBL gene families compared to multiplex PCR panel (AusDiagnostics CRE panel);
tAMR compared to the ‘gold standard’ multiplex PCR assays used in our laboratory.                                                                                    asterisks represent groups where discrepancies were identiﬁed, and expanded out
True positive, detected by both PCR and abritAMR; true negative, not detected by                                                                                     in Panel C2 to show the speciﬁc gene discrepancies between the two methods.
either PCR or abritAMR; false positive, detected by abritAMR but not multiplex PCR,                                                                                  Abbreviations: AMR antimicrobial resistance, PCR polymerase chain reaction, CP
and within the known range of the PCR assay; false negative, detected by multiplex                                                                                   carbapenemase, ESBL extended-spectrum beta-lactamase. Source data are pro-
PCR but not by abritAMR. Panel A, mec genes compared to multiplex PCR (mecA/                                                                                         vided as a Source Data ﬁle.
mecC, no mecC detected by either method). Panel B, van genes compared to



one of the main limiting factors to wider application of genomics in the                                                                                             mechanisms are detected). The capacity to include AMR genes or
CPHM setting4,27. Here, we have designed and validated a bioinformatic                                                                                               mutations of local signiﬁcance would be a welcome addition to AMR-
platform for genomic detection of AMR determinants across bacterial                                                                                                  FinderPlus, further extending its utility.
species focusing on reporting requirements for clinical and public                                                                                                        When this work commenced, there were no classiﬁcations of AMR
health microbiology, performed a rigorous validation, and imple-                                                                                                     mechanisms into drug classes in the AMRFinderPlus database, hence
mented it to achieve an ISO-ccertiﬁed genomic workﬂow for AMR. This                                                                                                  we created our own classiﬁcation database, which has also evolved in
was achieved by adapting an existing software tool and database                                                                                                      parallel with the great advances made by the AMRFinderPlus team.
(AMRFinderPlus), and adding a modiﬁed classiﬁcation step plus                                                                                                        There are (now) a small number of essential differences in the drug
reporting logic to produce tailored reports for a CPHM audience.                                                                                                     class classiﬁcations that we feel are important to enhance its utility for
      This platform relies heavily on the comprehensive, well-curated                                                                                                CPHM. Key examples include separating carbapenem resistance into
and frequently updated AMR database behind AMRFinderPlus, as well                                                                                                    different groups based on their mechanisms; separating into ‘carba-
as the excellent software tool, which uses multiple search methods to                                                                                                penemase’, ‘carbapenemase (MBL)’ and ‘carbapenemase (OXA-51
best identify AMR genes and mutations (with results annotated by the                                                                                                 family)’ enables reporting each group separately, as antibiotic choices
type of ‘match’, to allow scientists and clinicians to understand the                                                                                                differ with metallo-beta-lactamases (MBLs) compared to non-MBL
degree of conﬁdence behind each call)16. Notably, outputs for other                                                                                                  carbapenemases, and OXA-51 family carbapenemases are weak and
large AMR databases, such as CARD28 and ResFinder29, could be                                                                                                        intrinsic to Acinetobacter spp. and routine reporting is not required
modiﬁed to achieve similar tailored reports to abritAMR; our choice                                                                                                  (coded as part of reporting logic). This combination of tailored clas-
was based on the ease of integration into our existing workﬂows and                                                                                                  siﬁcation and reporting logic allows the vast and complex array of AMR
reporting. abritAMR’s speed allows for rapid detection of AMR genes in                                                                                               mechanisms to be distilled into results and reports that can be
routine high-throughput workﬂows, with AMR gene detection com-                                                                                                       understood by scientists, clinicians and public health teams alike,
pleted on a 96-sample sequencing run within 3 min. The addition of                                                                                                   without a great deal of prior knowledge. Future development will focus
mutations to AMRFinderPlus for an increasing number of species has                                                                                                   on restructuring the database to include different levels (classes,
been very useful in our early applications, enabling our public health                                                                                               subclasses) to take advantage of the higher resolution of classiﬁcations
laboratory to move to a fully-genomic workﬂow for Salmonella sur-                                                                                                    now included in AMRFinderPlus.
veillance, as all samples were sequenced for typing and phylogenetic                                                                                                      Notably, the key limitations of AMRFinderPlus are also lim-
analysis (a sub-sample of isolates still undergo AST to ensure new AMR                                                                                               itations of both ResFinder30 and CARD-RGI31 tools in different


Nature Communications | (2023)14:60                                                                                                                                                                                                                 6
Article                                                                                                                                                                               https://doi.org/10.1038/s41467-022-35713-4


                                  A

                                                              15000   *              *
                                                                                         *




                                   Number of alleles tested
                                                                                                                                                                                 Final result after
                                                              10000       *                                   *                                                                  discrepancy testing
                                                                                                                                                                                      False negative
                                                                                                                                                                                      False positive
                                                                                                         *                           *                                                True negative
                                                               5000
                                                                                                                                                                                      True positive


                                                                                 *                                                                                     *
                                                                                                 *                      *      *
                                                                  0
                                                                                      Carbapenemases
                                                                                                 ESBL
                                                                                    ESBL (AmpC type)
                                                                                             Methicillin
                                                                      Penicillin resistance (S. aureus)
                                                                                 Other beta−lactamase
                                                                                Aminoglycosides (Rmt)
                                                                                 Other discrepant Agly.
                                                                         Other non−discrepant Agly.
                                                                                  Amikacin / Quinolone
                                                                                             Quinolone
                                                                             Macro., Linco. & Strepto.
                                                                                             Phenicols
                                                                            Oxazolidinone & Phenicol
                                                                                           Vancomycin
                                                                                           Sulfonamide
                                                                                          Trimethoprim
                                                                                             Rifamycin
                                                                                           Fusidic Acid
                                                                                           Tetracycline
                                                                                            Fosfomycin
                                                                                                Colistin
                                                                                             Mupirocin
                                                                                                  Other
                                  B
                                                                300




                                   Number of alleles tested
                                                                200




                                                                100




                                                                  0
                                                                                                                                                                                           sul1
                                                                      GES−20   CTX−M−14                                                                                                                    tet(A)
                                                                                                                                                                       erm(A)                     arr−3
                                                                                                     SHV−11                                                                                                         bleO
                                                                                                                                                               qnrB6
                                                                                                                   aac(3)−IIa                                                   catA1


                                                                                                                                             aac(6')−Ib−cr5
                                                                               CTX−M−21      blaR1                 aac(6')−Ib
                                                                                                                   aac(6')−Ib'                                                  catA2                      tet(L)
                                                                      NDM−1    CTX−M−24       PC1    SHV−28       aac(6')−Ib3                                                                             tet(M)    sat4
                                                                                                                                                                       mph(A)   catB3
                                                                               CTX−M−65                           aac(6')−Ib4
                                                                                                                       aadA1                                                                              tet(O)
                                                                      NDM−5      GES−19               TEM−1            aadA2
                                                                                                                     ant(6)−Ia                                                                                      Other
                                                                                 SHV−12      Pen.                  aph(3')−Ia
                                                                                                                  aph(3')−VIa                                                   Phenicol                    Tet.
                                                                      Carb.
                                                                                 SHV−30
                                                                                                     Other BL
                                                                                                                    aph(6)−Id                                 Quin.                         Rif.
                                                                                 ESBL                             Other discrep. Agly.                                                Sulfon.
                                                                                                                                         Ami. / Quin. Mac., Lin. & Strep.

Fig. 5 | Performance of abritAMR pipeline compared to synthetic read data. This                                             of genes with discrepant results within each subclass. A full list of AMR subclasses
ﬁgure shows the presence or absence of 415 AMR genes across 321 genomes                                                     included in the validation set can be found in Supplementary Table 3. Abbrevia-
identiﬁed by abritAMR (performed on assembled synthetic read data) compared to                                              tions: EBL extended-spectrum beta-lactamase, Rmt ribosomal methyltransferase,
AMRFinderPlus on complete genome sequences (‘gold standard’). True positive,                                                Agly aminoglycoside, Macro., Linco. & Strepto, macrolides, lincosamides and
detected by AMRFinderPlus and abritAMR; true negative, not detected by either                                               streptogramins (combined class); Carb., carbapenemase; Pen., penicillin resistance
AMRFinderPlus or abritAMR; false positive, detected by abritAMR but not by AMR-                                             (S. aureus); Other BL, other beta-lactamase; Other discrep. Agly, other discrepant
FinderPlus; false negative, detected by AMRFinderPlus but not by abritAMR. Panel                                            aminoglycoside subclass; Ami./Quin., amikacin/quinolone subclass; Quin., quino-
A, abritAMR results by enhanced subclasses (further grouped to simplify visuali-                                            lones; Mac., Lin. & Strep., macrolides, lincosamides and streptogramins; Sulfon.,
sation); asterisks represent classes with any discrepant result (false positive or false                                    sulfonamides; Rif., rifampicin; Tet., tetracyclines. Source data are provided as a
negative), and are examined in more detail in Panel B. Panel B shows a detailed view                                        Source Data ﬁle.



ways; ResFinder classiﬁes AMR determinants into a small number                                                              maintaining a balance between accessibility and accuracy to
of antimicrobial classes, but lacks the resolution needed for the                                                           enable validation and accreditation.
more difﬁcult classes described above (particularly beta-lactams),                                                                In a CPHM setting, it is critical to validate any new test or analytical
whilst CARD-RGI maintains an ontologic focus, where anti-                                                                   process to ensure the veracity of results, and that the results (outputs
microbial targets and mechanisms are identiﬁed at varying levels,                                                           or reports in this case) are ﬁt-for-purpose12. However, formal test
but not grouped in a way that facilitates CPHM reporting and                                                                validation and accreditation procedures are based on wet-lab assays,
clinician understanding. However, both tools offer the accessi-                                                             and not always easily transferable to new methods such as WGS32. This
bility of a graphical user interface (GUI) and the option of using                                                          may require some creative thinking about different ways to validate a
raw reads as inputs for analysis, which are particularly important                                                          new genomic test33, as demonstrated here with the use of synthetic
considerations for laboratories without dedicated bioinformatic                                                             sequencing reads generated from complete reference genomes. Ide-
expertise. Ideally, all large AMR databases and tools should facil-                                                         ally, a broad range of publicly-available reference datasets with geno-
itate clinically-relevant reporting of AMR determinants through                                                             typic and phenotypic data would be made freely available to assist with
‘interpretation’ of outputs for clinical needs, and modiﬁable                                                               validation and bench-marking for databases, tools and new pipelines
reporting logic to tailor outputs to reporting requirements, whilst                                                         such as this, greatly advancing the development of AMR genomics4,34.


Nature Communications | (2023)14:60                                                                                                                                                                                           7
Article                                                                                                              https://doi.org/10.1038/s41467-022-35713-4




                             Ampicillin




                           Cefotaxime




                           Meropenem




                           Gentamicin




                            Kanamycin




                          Streptomycin
                                                                                                                                  Genotype classification
                                                                                                                                  compared to phenotypic AST



       Antimicrobial
                                                                                                                                        False negative
                          Sulfathiazole
                                                                                                                                        False positive
                                                                                                                                        True negative
                                                                                                                                        True positive
                          Trimethoprim




                            Trim Sulfa




                           Tetracycline




                       Chloramphenicol




                          Azithromycin




                          Ciprofloxacin



                                          0            250                       500                        750
                                                                 Number of isolates

Fig. 6 | Performance of inferred phenotype from abritAMR compared to anti-             negative, no AMR mechanisms detected in phenotypically resistant isolate. For
microbial susceptibility testing (AST). Classiﬁcation of genotype (AMR                 ciproﬂoxacin, ‘true positive’ deﬁned as concordant intermediate or resistant results
mechanism detection) compared to the ‘gold standard’ phenotypic AST for each           (phenotype and genotype). Abbreviations: AST, antimicrobial susceptibility test-
isolate and antimicrobial. True positive, genotypic and phenotypic resistance; true    ing; AMR, antimicrobial resistance; Trim-sulfa, trimethoprim-sulfamethoxazole.
negative, no AMR mechanisms detected in phenotypically susceptible isolate; false      Source data are provided as a Source Data ﬁle.
positive, AMR mechanism identiﬁed in phenotypically susceptible isolate; false


Initiatives such as the NCBI National Database of Antibiotic Resistant                 a dataset that may be used for validation of genomic detection of AMR
Organisms (NDARO)35 and PATRIC36 are promising, but currently lim-                     determinants against PCR results, and a method for validating against
ited in scale, and further global data sharing is required here to                     synthetic genomic data, to assist other laboratories to validate their
advance phenotype-genotype correlations. Here, we have contributed                     own AMR workﬂows.


Nature Communications | (2023)14:60                                                                                                                                      8
Article                                                                                               https://doi.org/10.1038/s41467-022-35713-4


      As with all attempts to validate new WGS pipelines and workﬂows,      The abritAMR bioinformatics pipeline
our study has limitations. The absence of a ‘gold-standard’ dataset to      The aims for development of this bioinformatic pipeline were to detect
compare results from our pipeline to means that we must compare to          AMR genes and mutations accurately and reliably from bacterial whole
imperfect standards, such as existing testing methods with lower            genome sequencing (WGS) data, which could be validated against PCR
resolution (PCR) and use synthetic sequencing data to compare targets       and other data sources, implemented in a public health or clinical
not covered by PCR in our laboratory. Until these issues are addressed      microbiology laboratory, and successfully accredited by governing
globally, laboratories will have to persist with these challenging com-     bodies. The abritAMR bioinformatic platform takes a genome assem-
parisons, and rely on new initiatives such as proﬁciency testing pro-       bly from short-read data, long-read data or hybrid assemblies (fasta
grams (PTPs) for WGS (with participation being a requirement for test       ﬁle) as input (once it has met deﬁned QC parameters), and includes ﬁve
accreditation in our setting) to start to standardise results across        main components (Fig. 1):
laboratories and countries. Whilst abritAMR was highly accurate               i. NCBI’s AMRFinderPlus tool (https://github.com/ncbi/amr) – abri-
overall, a small proportion of discrepant results were identiﬁed, of             tAMR implements this tool to identify AMR genes in genome
which the majority were false negative results. Most of these dis-               sequences, using a combination of BLASTx (matching the protein
crepancies are likely due to the comparison of synthetic short-read              sequences of AMR genes to the protein sequence of the query
data to complete genomes, where contig breaks within a gene result in            isolate) and Hidden Markov Models (HMMs)16.
non-detection, or plasmid dropout in culture, leading to non-                ii. NCBI’s AMRFinderPlus database – abritAMR uses this frequently
identiﬁcation of plasmid-borne AMR determinants in WGS data. In                  updated database (https://github.com/ncbi/amr/wiki/AMRFinder
our validation, use of a different genome assembly tool had minimal              Plus-database), which is a comprehensive and extensively curated
impact, although it is critical to include this as a consideration in the        database of AMR gene sequences. Current functionality includes
validation process, particularly where discrepancies are present.                mainly AMR genes (‘core’ database), with point mutations (spe-
      We envisage that the abritAMR pipeline will most likely be applied         cies-speciﬁc) and virulence genes increasingly being included in
in CPHM settings, and hope that it may assist sequencing laboratories            the ‘plus’ database. In more recent iterations, AMR genes and
address the difﬁcult question of how to best report these data to                point mutations include information about the antimicrobial class
clinicians and public health teams with limited AMR knowledge.                   and subclass (or speciﬁc antimicrobials) that they confer
However, it may also have utility in other settings including research,          resistance to.
particularly where complex AMR data need to be binned into func-            iii. Classiﬁcation database – While the AMRFinderPlus database
tional classes to facilitate understanding when the user is less familiar        includes some information about the antibiotic class and subclass
with AMR. In our view, it is critical for medical microbiologists, scien-        affected for each AMR gene, these classiﬁcations are not always
tists and bioinformaticians to continue to work together to navigate             easily translatable for clinical and public health practice. For
the challenges of communicating complex AMR data to clients, to                  example, the beta-lactam subclass ‘cephalosporin’ includes AMR
advance the reach of genomic AMR and maximise the beneﬁts of this                genes conferring resistance to ﬁrst-generation cephalosporins
potentially transformative technology.                                           (narrow-spectrum cephalosporinases, such as blaOXA-1), or third-
                                                                                 generation cephalosporins (such as blaCTX-M ESBLs), which have
Methods                                                                          very different implications for AMR surveillance and patient
Setting and existing genomics workﬂow                                            management. The local abritAMR classiﬁcation database is based
The Microbiological Diagnostic Unit Public Health Laboratory (MDU                on the current version of the AMRFinderPlus database, with an
PHL) is a state reference laboratory for bacterial pathogens, including          added ﬁeld (‘Enhanced subclass’) to translate the NCBI subclasses
carbapenemase-producing Enterobacterales (CPE), Acinetobacter spp.,              into more functional versions for our purposes (logic detailed in
Pseudomonas spp., vancomycin-resistant enterococci (VRE) and enteric             Supplementary Table 3, examples in Fig. 2). This ﬁeld is updated
pathogens37–39. The laboratory has a strong emphasis on genomics,                following each new database release (logic detailed in Supple-
primarily for epidemiologic surveillance, with increasing applications           mentary Table 4).
for clinical purposes. In conjunction with the Department of Health         iv. Species-speciﬁc reporting logic (AMR genes, all species) –
Victoria, we have embarked upon a broad program to increase imple-               Currently, most AMR genes detected by this pipeline are not
mentation of pathogen genomics for public health purposes, either                required to be reported for surveillance or clinical purposes;
enhancing or superseding current laboratory methods.                             reporting data on all AMR genes found in an isolate runs the risk
     Our existing genomics workﬂow (incorporating sample receipt,                of overwhelming clients with unnecessary data and missing the
nucleic acid extraction, library preparation, short-read sequencing              most pertinent AMR genes detected. As such, we developed a
(Illumina NextSeq or MiSeq), and quality control (QC) of reads                   reporting logic process to ﬁlter the AMR genes detected in each
including de novo genome assembly) has already been validated and                isolate into ‘reportable’ or ‘non-reportable’ categories, to mirror
accredited by the National Association of Testing Authorities Australia          the usual reporting requirements diagnostic laboratories (Sup-
(NATA, analogous to Clinical Laboratory Improvement Amendments                   plementary Figure 1). This logic takes into account the species
[CLIA] in USA)40–42. Details of this workﬂow can be found in Supple-             when determining what is reportable, limiting the reporting of
mentary Methods. Brieﬂy, single colonies from overnight pure bac-                intrinsic AMR genes (such as blaOXA-51 subtypes in Acinetobacter
terial sub-cultures were selected and placed in lysis buffer. DNA                baumannii), and differentiating between AMR genes that are only
extraction was performed on the QIAsymphony using the DSP Virus/                 reportable in certain species (e.g. ESBL genes reportable for
Pathogen Mini Kit, and library preparation performed using Nextera               national surveillance of Salmonella spp.), while always reporting
XT (Illumina Inc.) according to manufacturer’s instructions. WGS was             signiﬁcant AMR genes that are not limited by species (e.g.
performed on NextSeq 500/550 or MiSeq platforms (Illumina Inc.),                 carbapenemase and mcr genes). Non-reportable genes are also
generating 150 bp or 300 bp paired-end reads respectively. Reads were            made available to the reporting pathologists and senior scientists
assembled de novo using Shovill20. QC requirements for fastq reads to            and recorded in the laboratory information management system
be included in subsequent analysis were (i) Q-score ≥30, (ii) data with a        (LIMS), enabling detailed review of all detected AMR genes,
minimum estimated average genome coverage of >40X, and (iii) esti-               correlation with phenotype, and movement between reportable
mated genome size within range for observed species (see Supple-                 and non-reportable categories when required as part of any
mentary Methods for detailed descriptions).                                      routine results review process before reporting.



Nature Communications | (2023)14:60                                                                                                               9
Article                                                                                                https://doi.org/10.1038/s41467-022-35713-4


 v. Inferred phenotype (AMR genes and mutations, validated species          Synthetic reads. For the remaining AMR gene targets where PCR was
    only) – The pattern of AMR genes and mutations detected can be          not readily available to compare with abritAMR, we created synthetic
    used to infer phenotype for a given isolate. In abritAMR, this is       short-read sequence data from complete, publicly available genomes
    currently validated for Salmonella spp., and reported for epide-        from RefSeq or GenBank, and compared abritAMR results on synthetic
    miologic purposes in our laboratory, replacing routine anti-            short reads to AMRFinderPlus results from the complete genomes. To
    microbial susceptibility testing (AST) of Salmonella spp. for public    do this, we generated synthetic 150 bp paired-end reads using the art-
    health surveillance (reporting logic detailed in Supplementary          illumina tool45 to fragment the complete genome sequences, incor-
    Figure 2, Inferred Antibiogram Report example shown in Sup-             porating error proﬁle data from a NextSeq500 sequencer, at 40X to
    plementary Data 1).                                                     150X average genome coverage (40X is the minimum coverage
                                                                            accepted for QC) (Fig. 3). This dataset comprised 321 isolates (49 spe-
abritAMR outputs                                                            cies) covering 415 unique AMR alleles from 43 resistance subclasses
abritAMR outputs include a Detailed Report output, consisting of a          (Supplementary Table 3 and Figures 9 & 10). abritAMR results from
table (comma separated values ﬁle) of AMR genes or mutations                synthetic reads were compared to (native) AMRFinderPlus results from
detected for each sample, listed by enhanced subclass (e.g. “Car-           complete genome sequences. This allowed direct comparisons of
bapenemase (MBL)”, “Colistin”), or a Final AMR Gene Reports, a              presence or absence of AMR genes, therefore avoiding the problem of
table of AMR genes detected for each sample binned into ‘repor-             discrepancies in AMR gene nomenclature that may lead to false dis-
table’ or ‘not reportable’ ﬁelds, when the species-speciﬁc reporting        cordance if two different AMR gene databases were compared.
logic is applied (Fig. 2). Additionally, when run on validated species
(currently Salmonella spp.), abritAMR also produces an Inferred             Precision testing. abritAMR results from a test panel of 13 organisms
Antibiogram Report. All alleles listed in these outputs are either          (12 genera, Supplementary Table 6) sequenced multiple times (both
‘exact matches’ (100% identity and 100% sequence coverage                   within and across sequencing runs) using different sequencing plat-
compared to the reference protein sequence) or ‘close matches’              forms in our laboratory (NextSeq and MiSeq) and a range of sequen-
(90-<100% identity and 90-<100% sequence coverage compared to               cing modes (low, mid and high throughput) and read lengths
the reference protein sequence, marked by an asterisk [*] to dis-           (75–300 bp). Different combinations were compared to assess analy-
tinguish from exact matches), as deﬁned by AMRFinderPlus. Partial           tical precision (repeatability and reproducibility).
matches (>90% identity, 50-<90% coverage compared to reference
protein sequence) are listed separately, and must be examined               Determination of limit of detection. The limit of detection for mole-
further if deemed suitable for reporting. Where an internal stop            cular assays is normally the lowest amount of nucleic acid target that
codon (i.e. truncated gene) or HMM match are recorded by AMR-               can be detected by the assay. This deﬁnition is not strictly applicable to
FinderPlus, no result is reported by abriTAMR. Examples of abri-            whole genome sequencing, as the WGS assay is qualitative with a
tAMR pipeline outputs are shown in Fig. 2, demonstrating how the            standardised DNA concentration being used in the sequencing reac-
AMRFinderPlus output is modiﬁed by abritAMR (binned into                    tion. Instead, the limit of detection in this context was calculated as the
enhanced subclass according to abritAMR’s classiﬁcation database,           minimum average coverage across the genome required for accurate
and separated into reportable and non-reportable categories by the          detection of gene targets or allele variants. Synthetic paired-end reads
reporting logic).                                                           (150 bp) were generated at a range of sequencing coverages, from the
                                                                            minimum average coverage accepted for our routine QC (40 X) up to
Validation of the abritAMR pipeline                                         150 X coverage.
To validate abritAMR, results from the pipeline were compared to
results from PCR testing, Sanger sequencing and synthetic read sets as      Determination of inferred phenotype (Salmonella spp.). We vali-
detailed below. For the purposes of validation, both ‘exact’ and ‘close’    dated phenotypic inference (Susceptible/Intermediate/Resistant, S/I/
matches were considered as ‘detected’. Pre-speciﬁed sensitivity and         R) against an existing dataset of 864 sequenced Salmonella spp. with
speciﬁcity thresholds were deﬁned for successful validation prior to        antimicrobial susceptibility (AST) data generated by agar dilution from
analysis.                                                                   2018-2019. For the ﬂuoroquinolone drug class, the S/I/R phenotypes
                                                                            associated with combinations of AMR genes and mutations were
Validation datasets                                                         analysed to determine the relative weighting of each AMR mechanism
All isolates used in validation were obtained as part of routine AMR        to infer a phenotype most reliably from in silico analysis.
surveillance under public health laboratory functions, and hence were
exempt from requiring ethics approval. Data were de-identiﬁed for the       Discordant result resolution
validation study (no patient or clinical data were used).                   Discordant results were divided into two categories: ﬁrstly, PCR nega-
                                                                            tive, WGS positive (false positive) - this may be due to the AMR gene
PCR. This dataset included 1184 bacterial isolates (42 species), that had   detected by WGS not being included in the range of the PCR panel. If the
previously been tested by PCR, including a carbapenemase and ESBL           gene was known to be included in the range of the PCR panel (as stated
real-time multiplex PCR (n = 1020 isolates, AusDiagnostics 16-well CRE      by the manufacturer), the isolate was retested by PCR and WGS to
panel, catalogue no. 21098, version 03; Sydney, Australia), van gene        resolve this discrepancy. Secondly, PCR positive, WGS negative (false
PCR (n = 121, in-house assay for vanA, vanB, vanC1 and vanC2/3              negative) – this may be due to an AMR gene being fragmented across
genes43) and mecA PCR (n = 43, in-house assay for mecA44)(Supple-           two or more contigs, hence partial matches were assessed; if no partial
mentary Figures 3–6).                                                       matches were found, the sequence was interrogated using alternative
                                                                            tools; if this failed to resolve the discrepancy, the isolate was retested by
PCR and Sanger sequencing for allelic variants. This dataset inclu-         PCR and WGS. Where possible, discrepancies between phenotypic and
ded 347 isolates (20 species) with carbapenemase resistance genes           genotypic results were investigated through repeat phenotypic testing
detected by a range of carbapenemase and ESBL PCR assays across six         and/or repeat sequencing of the isolate.
different carbapenemase resistance gene families (targets and primers
detailed in Supplementary Table 5), with Sanger sequencing subse-           Re-veriﬁcation processes
quently performed to identify the carbapenemase allelic variant             In accordance with ISO standards, the abritAMR pipeline must be re-
(Supplementary Figures 7 & 8).                                              veriﬁed after each database or tool update. Database updates are


Nature Communications | (2023)14:60                                                                                                                   10
Article                                                                                                     https://doi.org/10.1038/s41467-022-35713-4


reveriﬁed by conﬁrming that the updated database performs to the                 9.  Vincent, A. T., Derome, N., Boyle, B., Culley, A. I. & Charette, S. J.
same criteria as was deﬁned in the original validation, using the syn-               Next-generation sequencing (NGS) in the microbiological world:
thetic dataset described above (‘abritAMR test suite’). Updates to the               How to make the most of your money. J. Microbiol Methods 138,
abritAMR software may take the form of minor patches or major                        60–71 (2017).
updates. Minor patches are changes that do not impact underlying                 10. Coolen J. P. M., et al. Centre-speciﬁc bacterial pathogen typing
structure or core logic of the pipeline, such as ﬁxes for typographical              affects infection-control decision making. Microbial Genomics
errors or addition of functionality which does not impact the core logic             7 (2021).
of the tool, e.g. changes to log outputs. In these cases, a full rever-          11. Doyle R. M., et al. Discordant bioinformatic predictions of anti-
iﬁcation is deemed unnecessary and running of the abritAMR test suite                microbial resistance from whole-genome sequencing data of bac-
is sufﬁcient. However, other changes which may impact the core logic                 terial isolates: an inter-laboratory study. Microbial Genomics
or structure of the outputs require a complete reveriﬁcation as                      6 (2020).
described for database updates. Any change in performance is asses-              12. Gargis, A. S., Kalman, L. & Lubin, I. M. Assuring the quality of next-
sed, the cause identiﬁed, and modiﬁcations made before the changes                   generation sequencing in clinical microbiology and public health
are implemented for reporting. All changes to abritAMR are tracked in                laboratories. J. Clin. Microbiol 54, 2857–2865 (2016).
GitHub and the versions managed using conda.                                     13. Crisan, A., McKee, G., Munzner, T. & Gardy, J. L. Evidence-based
                                                                                     design and evaluation of a whole genome sequencing clinical
Statistical analysis                                                                 report for the reference microbiology laboratory. PeerJ 6,
Test performance characteristics (accuracy, sensitivity, speciﬁcity,                 e4218 (2018).
positive and negative predictive values, including conﬁdence intervals)          14. International Organization for Standardization (ISO).
were calculated using the epiR package for R (version 4.1.1), used in                ISO15189:2012: Medical laboratories - Requirements for quality and
RStudio (version 1.4.1717).                                                          competence. 2012. https://www.iso.org/standard/56115.html
                                                                                     (accessed 18/09/2022 2022).
Reporting summary                                                                15. International Organization for Standardization (ISO). Medical
Further information on research design is available in the Nature                    laboratory testing: how can we trust the results? 2021. https://www.
Portfolio Reporting Summary linked to this article.                                  iso.org/news/ref2617.html (accessed 18/09/2022 2022).
                                                                                 16. Feldgarden M., et al AMRFinderPlus and the Reference Gene Cat-
Data availability                                                                    alog facilitate examination of the genomic links among anti-
Sequence data used in this study are available on NCBI Sequence Read                 microbial resistance, stress response, and virulence. Sci. Rep.
Archive (BioProjects PRJNA529744, PRJNA565795, PRJNA856406,                          11 (2021).
PRJNA856415, PRJNA857525, PRJNA857526, PRJNA857528, PRJNA857531,                 17. Australian Commission on Safety and Quality in Health Care.
PRJNA857533, PRJNA857534, PRJNA870170 and PRJNA319593) with                          National Alert System for Critical Antimicrobial Resistances (CAR-
accession numbers provided in Supplementary Data 2. Accession num-                   Alert). https://www.safetyandquality.gov.au/our-work/
bers for the complete genomes used to generate the synthetic validation              antimicrobial-resistance/antimicrobial-use-and-resistance-
dataset are provided in Supplementary Data 2. PCR results for the PCR                australia-surveillance-system/national-alert-system-critical-
validation dataset are available in Supplementary Data 2 and on GitHub               antimicrobial-resistances-caralert (2021).
(https://github.com/MDU-PHL/abritAMR)46. Source data are provided                18. Souvorov A., Agarwala R., Lipman D. J. SKESA: strategic k-mer
with this paper.                                                                     extension for scrupulous assemblies. Genome Biol. 19 (2018).
                                                                                 19. Bankevich, A. et al. SPAdes: a new genome assembly algorithm and
Code availability                                                                    its applications to single-cell sequencing. J. Comput Biol. 19,
Code for the abritAMR pipeline is publicly available at https://github.              455–477 (2012).
com/MDU-PHL/abritAMR (https://doi.org/10.5281/zenodo.7370627).                   20. Seemann T. Shovill: assemble bacterial isolate genomes from Illu-
                                                                                     mina paired-end reads. GitHub; (2017).
References                                                                       21. Sia, C. M. et al. Genomic diversity of antimicrobial resistance in non-
1.   O’Neill J. Review on antimicrobial resistance: Tackling a crisis for the        typhoidal Salmonella in Victoria, Australia. Microb. Genomics 7,
     health and wealth of nations. London, UK: UK Government (2014).                 000725 (2021).
2.   Centres for Disease Control and Prevention (CDC). Antibiotic                22. Gomes, C. et al. Macrolide resistance mechanisms in Enter-
     resistance threats in the United States, 2019. Atlanta, GA: U.S.                obacteriaceae: focus on azithromycin. Crit. Rev. Microbiol 43,
     Department of Health & Human Services (2019).                                   1–30 (2017).
3.   World Health Organization. Global action plan on antimicrobial              23. Armstrong, G. L. et al. Pathogen genomics in public health. N. Engl.
     resistance. Geneva: WHO (2015).                                                 J. Med 381, 2569–2580 (2019).
4.   Ellington, M. J. et al. The role of whole genome sequencing in              24. Ruppe E., Cherkaoui A., Lazarevic V., Emonet S., Schrenzel J.
     antimicrobial susceptibility testing of bacteria: report from the               Establishing genotype-to-phenotype relationships in bacteria
     EUCAST Subcommittee. Clin. Microbiol Infect. 23, 2–22 (2017).                   causing hospital-acquired pneumonia: a prelude to the application
5.   Motro, Y. & Moran-Gilad, J. Next-generation sequencing applica-                 of clinical metagenomics. Antibiotics (Basel) 6 (2017).
     tions in clinical bacteriology. Biomol. Detect Quantif. 14, 1–6 (2017).     25. Mahfouz, N., Ferreira, I., Beisken, S., Von Haeseler, A. & Posch, A. E.
6.   Maugeri, G., Lychko, I., Sobral, R. & Roque, A. C. A. Identiﬁcation             Large-scale assessment of antimicrobial resistance marker data-
     and antibiotic-susceptibility proﬁling of infectious bacterial agents:          bases for genetic phenotype prediction: a systematic review. J.
     a review of current and future trends. Biotech. J. 14, 1700750 (2019).          Antimicrob. Chemother. 75, 3099–108 (2020).
7.   Besser, J., Carleton, H. A., Gerner-Smidt, P., Lindsey, R. L. & Trees, E.   26. Rossen, J. W. A., Friedrich, A. W. & Moran-Gilad, J. Practical issues in
     Next-generation sequencing technologies and their application to                implementing whole-genome-sequencing in routine diagnostic
     the study and control of bacterial infections. Clin. Microbiol Infect.          microbiology. Clin. Microbiol Infect. 24, 355–360 (2018).
     24, 335–341 (2018).                                                         27. World Health Organization. GLASS whole-genome sequencing for
8.   Boolchandani, M., D’Souza, A. W. & Dantas, G. Sequencing-based                  surveillance of antimicrobial resistance. Geneva: WHO (2020).
     methods and resources to study antimicrobial resistance. Nat. Rev.          28. Mcarthur, A. G. et al. The Comprehensive Antibiotic Resistance
     Genet 20, 356–370 (2019).                                                       Database. Antimicrob. Agents Chemother. 57, 3348–3357 (2013).


Nature Communications | (2023)14:60                                                                                                                       11
Article                                                                                                  https://doi.org/10.1038/s41467-022-35713-4


29. Zankari, E. et al. Identiﬁcation of acquired antimicrobial resistance     Acknowledgements
    genes. J. Antimicrob. Chemother. 67, 2640–2644 (2012).                    MDU PHL is funded by the Victorian Government Department of Health.
30. Bortolaia, V. et al. ResFinder 4.0 for predictions of phenotypes from     BPH receives an investigator grant from National Health and Medical
    genotypes. J. Antimicrob. Chemother. 75, 3491–3500 (2020).                Research Council Australia (GNT1196103). NLS received an Australian
31. Alcock, B. P. et al. CARD 2020: antibiotic resistome surveillance         Government Research Training Program (RTP) scholarship. We sincerely
    with the comprehensive antibiotic resistance database. Nucleic            thank the NCBI’s AMRFinderPlus team for their dedication to producing
    Acids Res. 48, D517–d25 (2020).                                           and maintaining high-quality tools and database for detection of AMR
32. Kozyreva, V. K. et al. Validation and implementation of clinical          mechanisms from WGS data. We also thank Cheryll Sia for sharing her
    laboratory improvements act-compliant whole-genome sequen-                insights on genotype-phenotype correlations for ﬂuoroquinolone resis-
    cing in the public health microbiology laboratory. J. Clin. Microbiol     tance in Salmonella.
    55, 2502–2520 (2017).
33. Angers-Loustau A. et al. The challenges of designing a benchmark          Author contributions
    strategy for bioinformatics pipelines in the identiﬁcation of anti-       N.L.S., K.H., B.P.H., A.G.S. and T.S. conceived the project. N.L.S. and K.H.
    microbial resistance determinants using next generation sequen-           designed the software with input from A.G.S., T.S. and M.B.S. N.LS. and
    cing technologies. F1000Research 7 (2018).                                K.H. wrote the manuscript, C.L.G. created ﬁgures, B.P.H., T.P.S. and T.S.
34. Bogaerts, B. et al. Validation of a bioinformatics workﬂow for routine    supervised the manuscript writing and editing. K.H., T.S., S.A.B., N.L.S.
    analysis of whole-genome sequencing data and related challenges           and A.G.S. designed the validation. M.L.S., K.S. and M.V. contributed to
    for pathogen typing in a European national reference center:              the validation, N.L.S. and K.H. performed and analysed the validation
    Neisseria meningitidis as a proof-of-concept. Front Microbiol 10,         results. All authors reviewed, edited and approved the manuscript.
    362 (2019).
35. National Center for Biotechnology Information. National Database          Competing interests
    of Antibiotic Resistant Organisms (NDARO). (2022). https://www.           The authors declare no competing interests.
    ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/ (accessed
    2022-04 21 2022).                                                         Additional information
36. Davis, J. J. et al. The PATRIC Bioinformatics Resource Center:            Supplementary information The online version contains
    expanding data and analysis capabilities. Nucleic Acids Res. 48,          supplementary material available at
    D606–D612 (2020).                                                         https://doi.org/10.1038/s41467-022-35713-4.
37. Lane, C. R. et al. Search and Contain: Impact of an integrated
    genomic and epidemiological surveillance and response program             Correspondence and requests for materials should be addressed to
    for control of carbapenemase-producing Enterobacterales. Clin.            Benjamin P. Howden.
    Infect. Dis. 73, e3912–e3920 (2021).
38. Ingle, D. J. et al. Genomic epidemiology and antimicrobial resis-         Peer review information Nature Communications thanks Frank Aar-
    tance mechanisms of imported typhoid in Australia. Antimicrob.            estrup, Kara Tsang and the other, anonymous, reviewer for their con-
    Agents Chemother. 65, e0120021–e0120021 (2021).                           tribution to the peer review of this work. Peer reviewer reports are
39. Ingle D. J. et al. Prolonged outbreak of multidrug-resistant Shigella     available.
    sonnei harboring blaCTX-M-27 in Victoria, Australia. Antimicrob
    Agents Chemother 64 (2020).                                               Reprints and permissions information is available at
40. National Association of Testing Authorities Australia (NATA). https://    http://www.nature.com/reprints
    nata.com.au/ (2021).
41. Centres for Disease Control and Prevention (CDC). Clinical                Publisher’s note Springer Nature remains neutral with regard to jur-
    Laboratory Improvement Amendments (2022).                                 isdictional claims in published maps and institutional afﬁliations.
42. Bolger, A. M., Lohse, M. & Usadel, B. Trimmomatic: a ﬂexible trimmer
    for Illumina sequence data. Bioinformatics 30, 2114–2120 (2014).          Open Access This article is licensed under a Creative Commons
43. Dutka-Malen, S., Evers, S. & Courvalin, P. Detection of glycopeptide      Attribution 4.0 International License, which permits use, sharing,
    resistance genotypes and identiﬁcation to the species level of            adaptation, distribution and reproduction in any medium or format, as
    clinically relevant enterococci by PCR. J. Clin. Microbiol 33,            long as you give appropriate credit to the original author(s) and the
    24–27 (1995).                                                             source, provide a link to the Creative Commons license, and indicate if
44. Louie, L. et al. Rapid detection of methicillin-resistant staphylococci   changes were made. The images or other third party material in this
    from blood culture bottles by using a multiplex PCR assay. J. Clin.       article are included in the article’s Creative Commons license, unless
    Microbiol 40, 2786–2790 (2002).                                           indicated otherwise in a credit line to the material. If material is not
45. Huang, W., Li, L., Myers, J. R. & Marth, G. T. ART: a next-generation     included in the article’s Creative Commons license and your intended
    sequencing read simulator. Bioinformatics 28, 593–594 (2011).             use is not permitted by statutory regulation or exceeds the permitted
46. Horan K., Goncalves da Silva A., Seemann T. Establishing ISO-             use, you will need to obtain permission directly from the copyright
    certiﬁed genomics workﬂows for identiﬁcation and surveil-                 holder. To view a copy of this license, visit http://creativecommons.org/
    lance of antimicrobial resistance (code for abritAMR software).           licenses/by/4.0/.
    https://github.com/MDU-PHL/abritamr; https://doi.org/10.
    5281/zenodo.7370627 (2022).                                               © The Author(s) 2023




Nature Communications | (2023)14:60                                                                                                                    12
