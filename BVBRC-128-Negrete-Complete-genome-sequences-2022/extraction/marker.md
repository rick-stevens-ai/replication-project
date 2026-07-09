<!-- Extracted via pdftotext -layout (Marker-substitute); central Marker manifest unavailable for this paper — 2026-07-06 -->
Negrete et al. Gut Pathogens    (2022) 14:23
https://doi.org/10.1186/s13099-022-00500-5                                                                                                      Gut Pathogens


 RESEARCH                                                                                                                                                  Open Access

Complete genome sequences and genomic
characterization of five plasmids harbored
by environmentally persistent Cronobacter
sakazakii strains ST83 H322 and ST64 GK1025B
obtained from powdered infant formula
manufacturing facilities
Flavia J. Negrete1,2, Katie Ko1,2, Hyein Jang1, Maria Hoffmann3, Angelika Lehner4, Roger Stephan4,
Séamus Fanning5,6, Ben D. Tall1 and Gopal R. Gopinath1*



  Abstract
  Background: Cronobacter sakazakii is a foodborne pathogen that causes septicemia, meningitis, and necrotizing
  enterocolitis in neonates and infants. The current research details the full genome sequences of two extremely per-
  sistent C. sakazakii strains (H322 and GK1025B) isolated from powdered infant formula (PIF) manufacturing settings.
  In addition, the genetic attributes associated with five plasmids, pH322_1, pH322_2, pGK1025B_1, pGK1025B_2, and
  pGK1025B_3 are described.
  Materials and Methods: Using PacBio single-molecule real-time ­(SMRT®) sequencing technology, whole genome
  sequence (WGS) assemblies of C. sakazakii H322 [Sequence type (ST)83, clonal complex [CC] 83) and GK1025B (ST64,
  CC64) were generated. Plasmids, also sequenced, were aligned with phylogenetically related episomes to determine,
  and identify conserved and missing genomic regions.
  Results: A truncated ~ 13 Kbp type 6 secretion system (T6SS) gene cluster harbored on virulence plasmids pH322_2
  and pGK1025B_2, and a second large deletion (~ 6 Kbp) on pH322_2, which included genes for a tyrosine-type
  recombinase/integrase, a hypothetical protein, and a phospholipase D was identified. Within the T6SS of pH322_2
  and pGK1025B_2, an arsenic resistance operon was identified which is in common with that of plasmids pSP291_1
  and pESA3. In addition, PHASTER analysis identified an intact 96.9 Kbp Salmonella SSU5 prophage gene cluster
  in pH322_1 and pGK1025B_1 and showed that these two plasmids were phylogenetically related to C. sakazakii
  plasmids: pCS1, pCsa767a, pCsaC757b, pCsaC105731a. Plasmid pGK1025B_3 was identified as a novel conjugative
  Cronobacter plasmid. Furthermore, WGS analysis identified a ~ 16.4 Kbp type 4 secretion system gene cluster harbored
  on pGK1025B_3, which contained a phospholipase D gene, a key virulence factor in several host–pathogen diseases.



*Correspondence: Gopal.Gopinathrao@fda.hhs.gov
1
  Center for Food Safety and Applied Nutrition, Office of Applied Research
and Safety Assessment, U. S. Food and Drug Administration, Laurel, MD, USA
Full list of author information is available at the end of the article


                                        © The Author(s) 2022. Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which
                                        permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the
                                        original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or
                                        other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line
                                        to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory
                                        regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this
                                        licence, visit http://​creat​iveco​mmons.​org/​licen​ses/​by/4.​0/. The Creative Commons Public Domain Dedication waiver (http://​creat​iveco​
                                        mmons.​org/​publi​cdoma​in/​zero/1.​0/) applies to the data made available in this article, unless otherwise stated in a credit line to the data.
Negrete et al. Gut Pathogens   (2022) 14:23                                                                        Page 2 of 12




  Conclusion: These data provide high resolution information on C. sakazakii genomes and emphasizes the need for
  furthering surveillance studies to link genotype to phenotype of strains from previous investigations. These results
  provide baseline data necessary for future in-depth investigations of C. sakazakii that colonize PIF manufacturing
  facility settings and genomic analyses of these two C. sakazakii strains and five associated plasmids will contribute to a
  better understanding of this pathogen’s survival and persistence within various “built environments” like PIF manufac-
  turing facilities.
  Keywords: Cronobacter sakazakii, Whole genome sequencing, Plasmids, Built environment, Complete genomes,
  PHASTER, Phage-plasmids


Background                                                      in the environments of another European PIF manufac-
Cronobacter sakazakii is an opportunistic foodborne             turing facility. These ST64 strains were phylogenetically
pathogen that causes serious intestinal and extraintes-         related to other strains obtained from sources such as
tinal systemic infections such as acute gastroenteritis,        clinical samples, environments of USA dairy powder
septicemia, meningitis, urosepsis, osteomyelitis, wound         manufacturing facilities, spices, and mushrooms from the
infections, and pneumonia in individuals of all ages [1–        Middle East and China. Draft whole genome sequence
5]. Pre-term, low-birth weight, and/or immune compro-           (WGS) assemblies of these strains, together with other
mised neonates and infants are highly susceptible to C.         PIF production environmental-associated strains, con-
sakazakii. Moreover, severe invasive infections such as         firmed a ST phylogenetic relatedness among them [16].
septicemia, meningitis, and necrotizing enterocolitis are       In the present study, we report the completed genome
hallmarks of this organism’s pathogenicity. Additionally,       sequences of these two highly persistent C. sakazakii
outcomes from such invasive infantile infections often          strains, H322 and GK1025B, and describe the genomic
leave individuals with lifelong debilitating and neurologic     characterization of five plasmids harbored by them. The
impairments such as developmental delays, hydroceph-            results of this study will facilitate a greater understanding
aly, mental retardation, and other chronic neurological         of the survival and persistence of such foodborne patho-
sequelae [3, 6, 7]. C. sakazakii infections observed in         gens within these “built- environments”.
these individuals have been epidemiologically linked to
consumption of intrinsically and extrinsically contami-         Methods
nated lots of reconstituted powdered infant (PIF) and fol-      Bacterial strains and DNA isolation
low up formulas; thus, contamination of such products is        Cronobacter sakazakii H322 and GK1025B were grown
a challenging task for both infant formula manufacturers        in 5 ml of Trypticase Soy Broth (TSB, BBL, Becton Dick-
and caretakers [7–10]. Another trend that both clinicians       inson, Franklin Lakes, NJ, USA) supplemented with
and public health scientists must recognize is that unsafe      1% NaCl (TSBS), and incubated at 37 °C for 18 h with
personal hygiene breast-feeding practices, such as the use      shaking conditions of 160 rpm (Thomas Scientific, Inc.,
of contaminated personalized breast pumps, may also             Swedesboro, NJ, USA). Isolation of genomic DNA was
lead to infantile infections such as septicemia and men-        performed using a 2 ml aliquot of each culture using the
ingitis [11–14].                                                robotic QIACube workstation and the automated Qia-
  Chase et al. [15] described C. sakazakii H322, as a           gen DNeasy technology (Qiagen, Inc., Germantown, MD,
highly persistent sequence type (ST) 83, clonal com-            USA) following the manufacturer’s recommendations as
plex (CC) 83 strain that was obtained from a lot of con-        described by Jang et al. [17, 18].
taminated PIF manufactured in Europe that was never
released to the public. Chase et al. [15] further showed        Whole genome sequencing, assembly, and annotation:
that the persistence of C. sakazakii H322 and other phy-        The single-molecule real-time (SMRT) sequel sequenc-
logenetically related ST83 strains, which were also found       ing technology [19] from PacBio (Pacific Biosciences,
within the production environment of this facility, and its     Menlo Park, CA, USA) was utilized to create high-
presence could be traced back for more than four years.         quality long-read datasets of C. sakazakii strains H322
Microarray analysis showed that these strains differed          (SRR8305966) and GK1025B (SRR8305970). The ini-
among them by sequence divergence in 5–38 genes [15].           tial processing of long-sequencing reads was carried
In separate studies, Gopinath et al. [16] and Chase et al.      out using the RS_HGAP_Assembly.2 protocol (default
[29] described several malonate-positive ST64, CC64 C.          parameters) implemented in the Pacific Biosciences
sakazakii strains, including GK1025B (a PIF manufac-            SMRT analysis portal (version 2.3.1). Quality filtering
turing environmental isolate), that were found persisting       was performed automatically during assembly using the
Negrete et al. Gut Pathogens            (2022) 14:23                                                                                                 Page 3 of 12




SMRT Portal P-filter module and using the Hierarchi-                                     of GenomeTrakr datasets along with publicly available
cal Genome Assembly Process 3 (HGAP3) pipeline. For                                      genomes hosted at NCBI.
generating complete genomes, a hybrid assembly strategy
with UniCycler assembly software [20] implemented on                                     Results and discussion
the Pathosystems Resource Integration Center (PATRIC)                                    Genome and plasmid characterization
database web-server (https://​patri​cbrc.​org/​app/​Assem​                               The characteristics of the completed genomes and closed
bly2). Long-read short read archive (SRA) files from                                     plasmids harbored by C. sakazakii strains H322 and
PacBio and corresponding WGS datasets of the strains                                     GK1025B are summarized in Table 1. Each genome con-
obtained from sequencing runs performed on an Illu-                                      sisted of a single circular chromosome of 4,350,614 bp
mina MiSeq platform (Illumina, San Diego, CA, USA)                                       and 4,362,605 bp in size, contained a GC content of
[15, 16, 29] were combined following the instructions                                    56.7% and 56.9%, and 4,146 and 3,693 coding DNA
on the web-server. The Prokaryotic Genome Annotation                                     sequences (CDS), respectively. Two plasmids were
Pipeline (PGAP) annotations [21] of these completed                                      identified as being harbored by C. sakazakii H322 and
genomes, plasmid sequences, and their accession num-                                     three plasmids were identified to be carried by C. saka-
bers were released under FDA GenomeTrakr Bioproject                                      zakii GK1025B. None of the five plasmids identified by
on NCBI (PRJNA258403), which is part of FDA’s food-                                      genome sequencing were predicted on CGE’s Plasmid-
borne pathogen research comprehensive Bioproject at                                      finder [24]. In addition to the closed plasmids generated
NCBI (PRJNA186875). The RAST Seedviewer was used                                         from long-read sequencing, PHASTER analysis showed
to help provide consistent and accurate genome annota-                                   that C. sakazakii strain H322 hosted four intact prophage
tions across the genomes and plasmid sequences [22].                                     sequences (Additional file 2: Table S2) that were located
                                                                                         on the chromosome which included a 47.4 Kbp Salmo-
Genomic analyses                                                                         nella SEN34 (NCBI accession #: NC_028699), a 37.4
The PROKSEE server (https://​beta.​proks​ee.​ca/​proje​cts) was                          Kbp Enterobacteria mEp235 (NC_019708), a 43.5 Kbp
used to generate high-quality navigable maps of each circu-                              Salmonella 118970_sal3 (NC_031940), and a 17.7 Kbp
lar plasmid as previously described [23]. Each Cronobacter                               Enterobacteria P1 (NC_005856), prophage. An incom-
plasmid’s sequence was submitted to CGE’s Plasmidfinder                                  plete generalized transducing Salmonella bacteriophage
(https://​cge.​cbs.​dtu.​dk/​servi​ces/​Plasm​idFin​der/) for in sil-                    ES18 prophage (NC_006949) prophage was also iden-
ico determination of incompatibility plasmids such as IncF,                              tified. Three intact Cronobacter prophage sequences
IncHI1, IncHI2, IncN, and IncI1 plasmids [24]. For prophage                              were additionally identified by PHASTER analysis on
sequence identification, C. sakazakii strain FASTA data                                  the chromosome of GK1025B: Cronobacter ENT47670
sets were uploaded to the PHASTER (PHAge Search Tool                                     (NC_019927), Cronobacter ESSI_2 (NC_047854), and
Enhanced Release) web server and pipeline (https://​phast​                               Cronobacter phiES15 (NC_018454). The complete chro-
er.​ca/, last accessed 8.25.2021, [25, 26]). Mauve, Progressive                          mosomal sequences of the two C. sakazakii allowed
Mauve, and Geneious suite 12.0 ([27]; https://​www.​genei​ous.​                          for detailed annotation and identification of mobilome
com/) were used for alignment and visualization as needed.                               sequences that could be applied for comparative analysis
BLAST analysis for the presence of pH322_1 was per-                                      with other strains of Cronobacter and related organisms.
formed on an in-house database of 683 genomes consisting



Table 1 Characteristics of C. sakazakii H322 and GK1025B complete genomes and plasmids from Bioproject ­PRJNA258403a
Strain ID/Plasmid         Genome/            %GC content       Number of CDS         CRISPR arrays      NCBI biosample          NCBI genbank ID   NCBI accession
                          plasmid size                                                                  ID                                        number
                          (bp)

H322                      4,350,614          56.7              4146                  1                  SAMN06124518            CP078110          MRXM01000000
pH322_1                     100,741          50.2                137                                                            CP078111
pH322_2                     118,185          56.8                118                                                            CP078112
GK1025B                   4,362,605          56.9              3693                  2                  SAMN04329637            CP078106          MCOE01000000
pGK1025B_1                  101,769          51.1                141                                                            CP078107
pGK1025B_2                  120,182          56.6                133                                                            CP078108
pGK1025B_3                   46,5 28         51.0                 82                                                            CP078109
a
    Information was obtained from NCBI (https://​www.​ncbi.​nlm.​nih.​gov/​genome/​brows​e/#​!/​proka​ryotes/​1170/) and summarized
Negrete et al. Gut Pathogens    (2022) 14:23                                                                                            Page 4 of 12




Description of H322 plasmids: pH322_1 and pH322_2                           the origin of replication gene, repA, two iron acquisi-
A 100,741 bp pCS1-like closed plasmid, named                                tion systems, an aerobactin-like siderophore (named
pH322_1 was identified to be similar to the plasmid                         Cronobactin, iucABCD/iutA), and an ABC ferric-iron
pseudomolecule initially predicted from H322 draft                          transporter gene cluster (eitCBAD) as described by
whole genome contig sequences by Chase et al. [15].                         Franco et al. [31].
The sequence relatedness of pH322_1 to pCS1 har-
bored by C. sakazakii NCIMB 8272 (alias NCTC 8155)                          Description of GK1025B plasmids: pGK1025B_1,
after PROKSEE analysis using the β-version of CGView                        pGK1025B_2 and pGK1025B_3
Server [23] is shown in Fig. 1A. It had a GC content                        Complete sequences of three plasmids, pGK1025B_1,
of 50.2% and harbored 137 CDS. Unique features con-                         pGK1025B_2, and pGK1025B_3 was obtained by long-
tained on this plasmid included 12 mobile genetic ele-                      read sequencing and PGAP annotation (Additional file 1:
ments comprising six copies of an Insertion Sequence                        Table S1 [21]). pGK1025B_1 was 101,769 bp in size and
3 family transposase, three exonucleases (3–5′ exonu-                       contained 141 CDS, of which 70 genes encoded for hypo-
clease, SbcCD subunit D, and an unnamed exonucle-                           thetical proteins (Additional file 1: Table S1) and had
ase), a RecA recombinase, and a site-specific integrase                     a GC content of 51.1%. An intact 99.4 Kbp gene cluster
(Additional file 1: Table S1). PGAP analysis also identi-                   encoding for a Salmonella SSU5 prophage (NC_018843)
fied several phage-related genes on pH322_1 such as                         was identified using PHASTER and was like pH322_1
genes encoding for a phage exonuclease, and a phage                         (Additional file 2: Table S2) described earlier. This is a
tail fiber identified as side tail fiber protein, Stf (Addi-                slightly smaller sized prophage SSU5 gene cluster than
tional file 1: Table S1). PHASTER analysis identified                       what was reported by Kim et al. (103 Kbp; 2012) but is
and confirmed the presence of an intact 96.9 Kb Sal-                        slightly larger than the prophage gene cluster present in
monella SSU5 (NCBI accession number: NC_018843)                             pH322_1 (96.9 Kb). As was the case for pH322_1, the
prophage gene cluster [25] (Additional file 2: Table S2)                    prophage gene cluster contained genes encoding for
located on pH322_1.                                                         prophage structural proteins including terminase, capsid
  The second plasmid named pH322_2 and harbored                             and tail proteins. Genes encoding for a lysin, an integrase,
by C. sakazakii H322 was 118,185 bp in size and con-                        and a recombinase protein, and possessed a GC content
tained a GC content of 56.8%. There were 118 CDS                            of 51.1% were also noted.
identified by PGAP annotation. Analysis using PROK-                            pGK1025B_2 was identified as a slightly smaller ver-
SEE [23], showed the plasmid to be closely related to                       sion (120,182 bp) of the virulence plasmid, pESA3
C. sakazakii virulence plasmid pSP291_1 harbored by                         (131,196 bp) that Franco et al. [31] described for C. saka-
ST4 C. sakazakii SP291 as described by Power et al.                         zakii strain BAA-894. It contained 133 CDS, possessed a
[30]. BLAST analysis showed that the virulence plas-                        GC content of 56.6%, and harbored a homolog of repA,
mid pH322_2 shares significant homology with the                            the plasmid’s origin of replication gene and a homolog of
virulence plasmid backbones of pSP291_1 and pESA3                           Cronobacter plasminogen activator, cpa (location: 6338
(data not shown). They share conserved features like                        to 7276 bp). As described earlier, other noted genetic


 (See figure on next page.)
 Fig. 1 A Sequence alignment of C. sakazakii phage-plasmid class members, pH322_1 and GK1025B_1: Annotated genomes of known
 phage-plasmids were aligned and compared to identify conserved and divergent sequence features. The annotation of each gene is from NCBI. The
 inner circle represents the sequence clockwise and the scale marks indicate positions of annotated genes. GenBank annotations of the reference
 pCsaC105731a (100,874 bp, coding DNA sequence (CDS) in black arranged outside ring), pCS1 (110,093 pb, Blue), pCsa767a (109,716 bp, purple),
 pCsaC757b (109,716 bp, Green), pGK1025B_1 (101,769 bp, Red) and pH322_1 (100,741 bp, Tan) was downloaded as GFF files for the analysis
 using the default configuration on the PROKSEE server. Across the circular genomes, selected genes or regions of interest are shown as follows:
 Missing regions identified by the BLAST analysis on the CGView server’s PROKSEE software are shown as ‘gaps’ on each of the circular genomes. The
 analysis was carried out on PROKSEE Server from the Stothard Research Group (University of Alberta, Canada) that uses BLAST analysis to illustrate
 conserved and missing genomic sequences (available online: https://​beta.​proks​ee.​ca/​tools). B Sequence Comparison of C. sakazakii virulence
 plasmid class members pH322_2 and pGK1025B_2: Annotated genomes of some known virulence plasmids were aligned and compared to identify
 conserved and divergent sequence features. The annotation of each gene is from NCBI. The inner circle represents the sequence clockwise and the
 scale marks indicate positions of annotated genes. GenBank annotations of the reference pESA3 (131,196 bp, CDS in black arranged outside ring),
 pSP291_1 (118,136 bp, Green), pH322_2 (118,185 bp, light blue), and pGK1025B_2 (120,182 bp, purple) was downloaded as GFF files for the analysis
 using the default configuration on the PROKSEE server. Across the circular genomes, selected genes or regions of interest are shown as follows:
 Franco et al. [31], adapted siderophore loci with Cronobactin gene, Iron ABC transporter genes, (T6SS), parAB genes, and the cpa gene. Missing
 regions identified by the BLAST analysis on the CGView server’s PROKSEE software are shown as ‘gaps’ on each of the circular genomes. The analysis
 was on the PROKSEE Server from the Stothard Research Group (University of Alberta, Canada) that uses BLAST analysis to illustrate conserved and
 missing genomic sequences (available online: https://​beta.​proks​ee.​ca/​tools)
Negrete et al. Gut Pathogens    (2022) 14:23                                                         Page 5 of 12




 Fig. 1 (See legend on previous page.)



features among these virulence plasmids include: a      encoding for HigB/HipA, and a methyl-accepting chemo-
siderophore aerobactin biosynthesis gene cluster (now   taxis protein I (serine chemoreceptor protein) gene.
named Cronobactin/siderophore receptor, iucABCD/          pGK1025B_3 is a plasmid of 46,528 bp in size. It pos-
iutA), a bicistronic toxin-antitoxin gene complex       sesses a GC content of 51.1% and harbored 50 genes
Negrete et al. Gut Pathogens     (2022) 14:23                                                                                             Page 6 of 12




encoding for hypothetical proteins; however, it is a con-                    pCsaC105731a, pCsa767a, and pCsaC757b. PHASTER
jugative plasmid like pESA2 which is harbored by C.                          analysis also identified and confirmed an intact Sal-
sakazakii BAA-894 [31, 33]. A ~ 16.4 Kbp type 4 secre-                       monella SSU5 prophage in the C. muytjensii plasmid
tion system gene cluster was found, and most notably it                      pCmuyJZ38_1 [36] and a E. coli P1-like prophage on
contains within this gene cluster a copy of a phospholi-                     p505108-MDR and pGW1 (Additional file 2: Table S2).
pase D gene (plD, located between ~ 9308 to ~ 9841 bp,                       Analysis using the Mauve progressiveAlignment tool [28]
NCBI Locus Tag: AUM97_022060).                                               revealed the variations in the size of the prophage region
                                                                             in these plasmids when compared with SSU5 as reported
Comparative genomic analysis of the novel                                    by Kim et al. [37] (Fig. 2B). To understand the distribu-
phage‑plasmids pH322_1 and pGK1025B_1                                        tion and prevalence of the phage-plasmids within Crono-
Initial sequence analyses described above suggested that                     bacter species, we performed a BLAST analysis on 683
pGK1025B_1 and pH322_1 belong to a unique category                           draft WGS genomes and closed plasmids representative
of plasmids called phage-plasmids (extrachromosomal                          of all seven species using the genes found on pH322_1.
DNA molecules that host intact prophage sequences and                        The results identified the phage-plasmid like sequences
strictly behave like plasmids) that have been known since                    (from pH332_1) in three C. malonaticus strains (two
the 1960s [34, 35]. Sequence comparison of repA gene                         ST129 and a single ST7), and 133 C. sakazakii strains
sequences from pH322_1 and pGK1025B_1 (locus_tags                            which represented 18 different STs and these results are
BTK77_021130 and AUM97_021275, respectively) sug-                            shown in Additional file 3: Table S3.
gested that these plasmids possessed a mutually exclusive                      As noted above, the acquisition of plasmids contain-
origin of replication and different sub-groups of IncF1B                     ing prophages was a unique finding which was initially
category. It was reported that SSU5 phage bearing plas-                      reported by Ikeda and Tomizawa for prophage P1 in
mids usually belong to IncF1B incompatibility group in                       Escherichia coli [34]. It was reported that rather than
other Enterobactereaceae members [35]. Some previ-                           integrating its prophage genome into the host bacte-
ously reported Cronobacter plasmids belong to this rare                      rium’s chromosome, its DNA was found to replicate as
category of phage-plasmids along with the two plasmids                       a circular plasmid in the lysogen. Prophage SSU5 is like
identified in this study suggesting an expansion of genetic                  E. coli prophages P1 and D6, which are also harbored
diversity among this emerging foodborne pathogen                             on plasmids, are common in the Enterobacteriales,
[15, 36]. We identified sequences containing significant                     and were also among the first prophages found to be
homology to pGK1025B_1 and pH322_1 from among                                associated with plasmids [38]. Plasmids and prophages
the known Cronobacter plasmids by BLAST analysis.                            are key contributors to bacterial evolution and when
The properties of these prophages are summarized in                          found together as a single unit are often now referred
Additional file 2: Table S2 and suggest a prevalence of                      to as phage–plasmids, which possess properties of
phage-plasmid like sequences of varied lengths in dif-                       both plasmids and prophages, for example, P1, N15
ferent plasmids containing homologous sequences to                           or SSU5. Biological characterization of these phage-
SSU5. Figure 2A shows the prophage gene cluster region                       plasmids is poorly understood. Pfeifer et al. screened
from SSU5 in comparison with a few selected related C.                       over 2500 phages and 12,000 plasmids from across
sakazakii plasmids like pH322_1, pGK1025B-1, pCS1,                           a diverse collection of bacterial phyla and identified



 (See figure on next page.)
 Fig. 2 A Comparison of SSU5 prophage features with known C. sakazakii phage-plasmid class members: Four known and two new plasmid
 sequences from this study were compared using PROKSEE with the annotations of the Salmonella prophage SSU5. The inner circle represents
 the sequence clockwise and the scale marks indicate positions of annotated genes. GenBank annotations of the reference phage-plasmid SSU5
 (CDS in Black colored ring, arranged outside ring), pCS1 (Green), pCsa767a (purple), pCsaC757b (Tan), pCsaC105731a (Red), pGK1025B_1 (Teal)
 and pH322_1 (Mauve) were downloaded as GFF files for analysis using the default configuration on the PROKSEE server. Across the circular
 genomes, selected genes or regions of interest are shown as follows: Missing regions identified by the BLAST analysis on the CGView server’s
 PROKSEE software are shown as ‘gaps’ (white color) on each of the circular genomes. These plasmids contained a near-complete SSU5 phage. A
 BLAST analysis of 630 + WGS assemblies of Cronobacter revealed varied coverage of the phage sequences in many plasmids (See Additional file 3:
 Table S3). The analysis was carried out on the PROKSEE Server from the Stothard Research Group (University of Alberta, CA) that uses BLAST analysis
 to illustrate conserved and missing genomic sequences (available online: https://​beta.​proks​ee.​ca/​tools). B Mauve alignment of SSU5 illustrates
 variations in lengths of the phage-sequences in Cronobacter plasmids: Plasmids from C. sakazakii and C. muytjensii were compared using the Mauve
 progressive alignment tool (http://​darli​nglab.​org/​mauve/​user-​guide/​progr​essiv​emauve.​html, [27, 28]) implemented on Geneious suite 12. pCS1
 from C. sakazakii NCTC 8155 was seen to be the largest plasmid with almost 110 kb when compared to pCmuyZ38_1 from C. muytjensii JZ38 and
 the two new plasmids from this study. A detailed analysis of these plasmids, and their inclusion in plasmid-finding pipelines, would enable the
 identification of SSU5-like sequences from the growing number of Cronobacter WGS datasets
Negrete et al. Gut Pathogens    (2022) 14:23                                                            Page 7 of 12




 Fig. 2 (See legend on previous page.)



780 phage–plasmids grouped into eight distinct cat-       only very rarely annotated as being phage related, much
egories based on sequence features. This study further    less as prophages [38]. Often a genome may contain an
suggested a role for the phage-plasmids in genetically    integration hot spot such as that found for Lactococcus
connecting phages and other mobile (and transducing)      lactis subsp. cremoris which contains 20% of its genome
genetic elements [35]. Salmonella prophage SSU5 rep-      as IS elements [39]. This suggests that a genome can
resents a different type of lysogenic phage with a cir-   exist in an active evolutionary state, as it can readily
cular phage-plasmid that is also very common in other     accommodate new DNA and/or loose genome regions
members of the Enterobacteriales; however, they are
Negrete et al. Gut Pathogens    (2022) 14:23                                                                                            Page 8 of 12




 Fig. 3 Sequence analysis of newly described C. sakazakii conjugative class member pGK1025B_3: Annotated genomes from pGK1025B_3 and
 other Cronobacter conjugative plasmids were compared using PROKSEE for identifying conserved and unique sequence features. The inner circle
 represents the sequence clockwise and the scale marks indicate positions of annotated genes. GenBank annotations of the reference pGK1025B_3
 (46,528 bp, CDS in Black arranged outside ring), pC16KP0065-1 (168,415 bp, Teal), pC16KP0098-3 (49,279 bp, Purple), pC17KP0040-2 (56,619 bp,
 Dark Blue), pMG333 (134,435 bp, Tan), and pESA2 (31,208 bp, Green) were downloaded as a GFF file for analysis using the default configuration
 on the PROKSEE server. Across the circular genomes, selected genes or regions of interest are shown as follows: Missing regions identified by the
 BLAST analysis on the CGView server’s PROKSEE software are shown as ‘gaps’ on each of the circular genomes. The analysis was carried out on the
 PROKSEE Server from the Stothard Research Group (University of Alberta, CA) that uses BLAST analysis to illustrate conserved and missing genomic
 sequences (available online: https://​beta.​proks​ee.​ca/​tools)




as well. Similarly, pH322_1 and pGK1025B_1 with an                          [1, 31, 32]. Both the plasmids contained a truncated ~ 13
abundance of mobile genetic elements found in these                         kbp type six secretion system (T6SS) gene cluster which
phage-plasmid sequences (Additional file 1: Table S1)                       shares homology with a similar region harbored by
may represent such a genetic element. Furthermore, the                      pESA3, and pSP291_1. PROKSEE analysis showed that a
fact that C. sakazakii strains H322 and GK1025B con-                        similar truncated T6SS with a large deletion in the region
tain multiple plasmids may offer selective advantages to                    for SP291_1 and pH322_2 compared to that of pESA3.
a bacterial host which may also reflect their adaptative                    In addition to the deletion within the T6SS gene clus-
abilities to persist within the nutrient-rich environment                   ter, pH322_2 also had a second large deletion of ~ 6 Kbp,
of a built environment, such as that of powdered infant                     which includes genes for a tyrosine-type recombinase/
formula manufacturing facilities [40].                                      integrase, a hypothetical protein, and a phospholipase
                                                                            D. These results correlate with those reported by Franco
Genomic analysis of the virulence plasmids, pH322_2                         et al. [31]; Tall et al. [32], Chase et al. [15], and Jang et al.
and pGK1025B_2                                                              [1] who had described the presence of a virulence plas-
The shared genome backbone (Additional file 1: Table S1)                    mid like pH322_2, pGK1025B_2, pESA3 and pSP291_1
of pH322_2 and pGK1025B_2 with that of virulence plas-                      in a high percentage of C. sakazakii strains (629 of 652,
mids, pESA3 [31] and pSP291_1 [30] is shown in Fig. 1B.                     96%). Two functional T6SS clusters were reported by
Both plasmids harbored a Cronobacter plasminogen                            Wang et al., 2018 in the C. sakazakii strain ATCC12868
activator (cpa) encoding Protease VII or Omptin precur-                     although the genome sequences are not available on
sor (EC 3.4.23.49) (Additional file 1: Table S1) homolo-                    NCBI for comparison [42]. In contrast, truncated T6SS
gous to the Salmonella outer membrane protease, PgtE                        segments on pESA3-like virulence plasmids reported by
Negrete et al. Gut Pathogens   (2022) 14:23                                                                                         Page 9 of 12




 Fig. 4 Comparative analysis of rep gene sequences identifies plasmid pGK1025B_3 as a unique category of conjugative plasmid in
 Enterobacteriaceae: A nearest neighbor joining phylogenetically tree was developed using a BLASTn analysis with the rep gene (gene locus
 CP078109) from Cronobacter sakazakii strain MOD1-GK1025B plasmid pGK1025B_3, complete sequence. This rep gene from this plasmid grouped
 separately and uniquely when compared to rest of the rep gene sequences from the other microorganisms. The top cluster contains the query
 (shown with an asterisk) and the same sequence as the unique hit. The parameters used to develop the tree included the rep (CP078109.1) gene
 from pGK1025B_3 in a BLASTn analysis against a database represented by Enterobacteriaceae and related endosymbionts (NCBI taxid:91347) using
 NCBI’s nearest neighbor algorithm. Bar marker represents 0.01 bp substitutions



Franco et al. [31] and others had not been characterized                  Sequence analysis of conjugative plasmid pGK1025B_3
in vivo or share sequence homology with the chromo-                       compared with pESA2 and other Enterobacteriaceae
somal clusters rendering their use just as a possible ‘sig-               plasmids
nature sequence’ for this category of plasmids. A Cobalt                  Sequence alignment of newly described pGK1025B_3
ABC transporter gene cluster encoding for an ATP-bind-                    compared with other conjugative class members pro-
ing protein (CbtL), permease protein (CbtK), and two                      duced on the PROKSEE server (Fig. 3) suggest that this
copies of a substrate-binding protein gene (CbtJ) were                    plasmid represents a new conjugative plasmid that only
found on pGK1025B_2, but not on pH322_2 Additional                        has marginal sequence homology with pEAS2 from
file 4: Figure S1.                                                        C. sakazakii BAA-894 [1, 33]. Interestingly, a known
                                                                          virulence gene coding a phospholipase D (PLD) was
Negrete et al. Gut Pathogens   (2022) 14:23                                                                                       Page 10 of 12




identified within a complete T4SS cluster harbored on           This information could also be used in future studies to
pGK1025B_3 (Additional file 5: Figure S2). Results of a         develop basic differences between non-pathogenic and
BLASTn analysis using the rep (CP078109.1) gene from            pathogenic microorganisms found within these food
pGK1025B_3 queried against Enterobacteriaceae and               manufacturing environments. Finally, future analysis of
related endosymbionts (NCBI taxid:91347), showed a              the genome sequences of wild-type C. sakazakii strains
shared homology with many related rep genes. Align-             will shed more light on the importance of plasmids and
ment of these gene sequences, shown in Fig. 4 revealed          phage-plasmids and their role in survival and persis-
that the rep gene of pGK1025B_3 clustered distinctly            tence in PIF manufacturing environments, and as causa-
separated from a larger cluster of 91 rep genes of related      tive agents of severe-invasive human infectious diseases.
plasmids of members of the Enterobacteriaceae. These            This study highlights the increased discriminatory power
results suggest that the rep gene of pGK1025B_3 may             of WGS analysis and emphasizes the need for furthering
represent a novel Cronobacter origin of replication gene        extended surveillance studies and provides insights link-
carried by a previously uncharacterized Cronobacter             ing the genotype–phenotype of C. sakazakii from previ-
conjugative plasmid that harbors within its gene clus-          ously published longitudinal surveillance investigations.
ter a phospholipase D gene. Future surveillance studies
to identify the prevalence of pGK1025B_3 like plasmids          Supplementary Information
as well as functional genetic studies are needed. Phos-         The online version contains supplementary material available at https://​doi.​
pholipase D (PLD) represents a heterogeneous group              org/​10.​1186/​s13099-​022-​00500-5.
of lipolytic esterases, which are either secreted into the
                                                                  Additional file 1: Table S1. PGAP annotation of genes carried on
extracellular milieu, or directly injected into the host cell     pH322_1, pH322_2, pGK1025B_1, pGK1025B_2, and pGK1025B_3 that are
cytosol by a wide variety of Gram-positive and Gram-              harbored by C. sakazakii H322 and GK1025B.a.
negative bacteria through Type 6 and Type 4 secretion             Additional file 2: Table S2. Results of PHASTER analysis for various Crono-
systems [41]. It plays an important role in several host–         bacter plasmids including pH322_1, pH322_2, pGK1025B_1, pGK1025B_2,
                                                                  and pGK1025B_3.a.
pathogen physiological interactions involved in bacte-
                                                                  Additional file 3: Table S3. BLAST analysis of 683 Cronobacter genomes
rial pathogenesis, including cell invasion, evasion of the
                                                                  housed in a local database for the presnece of phage-plasmid pH322_1.
host immune response through escape of or maturation
                                                                  Additional file 4: Figure S1 Multiple alignment analysis of the Crono-
avoidance within phagosomes, establishment of tissue              bacter arsenic operon within the T6SS of virulence plasmids, pSP291_1,
colonization, and systemic spread. The contribution of            pH322_2, pGK1025B_2, and pESA3, as displayed by using Geneious suite.
the Cronobacter version of PLD in the pathogenicity of            The black horizontal bar indicates the consensus sequence. The blue line
                                                                  indicates sequence coverage; the green represents percent identity with
this organism needs to be further studied.                        red presenting little homology; and green representing high homology.
                                                                  The arsenic operon consists of three genes: arsenate reductase (arsC,
Conclusions                                                       glutaredoxin), arsenic transporter, and a gene encoding a metalloregula-
                                                                  tor ArsR/SmtB family transcription factor. The operon is flanked by genes
The mechanisms related to the persistence of Cronobac-            encoding for a TrkH family potassium uptake protein and dihydrodipicoli-
ter strains within the built environment such as that of          nate synthase family protein.
powdered infant formula manufacturing facilities are              Additional file 5: Figure S2 Cronobacter phospholipase D family pro-
currently unknown. The use of whole-genome sequenc-               tein within the T4SS of pGK1025B_3 as displayed by using Geneious suite.
                                                                  The phospholipase D family protein is flanked by genes encoding for two
ing of Cronobacter isolates obtained from the “built envi-        hypothetical proteins and a conjugative relaxase and VirB11 (a member of
ronment” as part of a routine surveillance strategy is only       the superfamily of traffic ATPases). Other adjacent genes include VirB10,
in its infancy but is a first step in determining the rela-       which has a role in regulating substrate transfer to the extracellular space,
                                                                  and VirB9 which encode for a channel protein that forms heterodimers
tionships of Cronobacter species that possess a long-term         with VirB7. VirB7 is localized at the outer membrane and plays a stabilizing
persistence phenotype in food manufacturing facilities.           role with the other VirB proteins during assembly of the T4SS pilus.
WGS analyses demonstrated that these two persistent C.
sakazakii strains possess five plasmids of which fall into      Acknowledgements
three different plasmid classes, such as the virulence plas-    This manuscript is being submitted by FN in partial fulfilment of the require-
mids pSP291_1 and pESA3 originally characterized by             ments for a Master of Science degree in Biological Sciences, University of
                                                                Maryland Biological Science’s Graduate Program, University of Maryland,
Power et al. [30] and Franco et al. [31], a prophage bear-      College Park. We thank Dr. Felix Reich (Institute for Food Quality and Safety,
ing pCS1-like plasmid originally described by Chase et al.      University of Veterinary Medicine Hannover, Bischofsholer Damm 15, 30173
[15], and an uncharacterized conjugative plasmid like           Hannover, Germany) for providing the strain GK1025B and for helpful sugges-
                                                                tions and discussions. Trade names of commercial products mentioned in this
that of pGK1025B_3 that possesses a phospholipase D             publication do not imply any recommendation or endorsement by the Food
gene within its T4SS gene cluster. The genomic informa-         and Drug Administration.
tion about these two highly persistent C. sakazakii strains
                                                                Author contributions
H322 and GK1025B provides insights to design further            FN, GG, BDT, and AL developed the concept for this paper. FN, HJ, GG, AL,
in-depth investigations of a facility’s microbiota profile.     SF, RS KK, and BDT designed the experiments and contributed to the initial
Negrete et al. Gut Pathogens         (2022) 14:23                                                                                                     Page 11 of 12




drafts of the paper paper. BDT and GG completed the final draft and revisions.    7.  Strysko J, Cope JR, Martin H, Tarr C, Hise K, Collier S, et al. Food safety and
MH carried out PacBio sequencing and initial SMRT pipeline processing. GG             invasive Cronobacter infections during early infancy, 1961–2018. Emerg
performed hybrid assembly, annotations, and genomic data submission. GG,              Infect Dis. 2020;26:857–65. https://​doi.​org/​10.​3201/​eid26​05.​190858.
FN, and KK carried out the genomic analyses and illustrations. KK carried out     8. Noriega FR, Kotloff KL, Martin MA, Schwalbe RS. Nosocomial bacteremia
PHASTER analysis, and KK and FN performed the PROKSEE analyses. All authors           caused by Enterobacter sakazakii and Leuconostoc mesenteroides result-
contributed to the article and approved the submitted version. All authors            ing from extrinsic contamination of infant formula. Pediatr Infect Dis J.
read and approved the final manuscript.                                               1990;9:447–9.
                                                                                  9. Himelright I, Harris E, Lorch V, Anderson M, Jones T, Craig A, et al. Entero-
Funding                                                                               bacter sakazakii infections associated with the use of powdered infant
Funds supporting this work were obtained internally through U.S. FDA appro-           formula—tennessee, 2001. Morb Mortal Wkly Rep. 2002;51:297–300.
priations, and the University of Maryland, Joint Institute for Food Safety and    10. Iversen C, Forsythe SJ. Risk profile of Enterobacter sakazakii, an emergent
Applied Nutrition (JIFSAN) that supported FN and KK through a cooperative             pathogen associated with infant milk formula. Trends Food Sci Technol.
agreement with the FDA (#FDU001418). Moreover, funding for research fellow            2003;2003(14):443–54.
HJ was provided by Oak Ridge Institute for Science and Education of Oak           11. Friedemann M. Enterobacter sakazakii in food and beverages
Ridge, Tennessee.                                                                     (other than infant formula and milk powder). Int J Food Microbiol.
                                                                                      2007;116:1–10.
Availability of data and materials                                                12. Jason J. Prevention of invasive Cronobacter infections in young infants
Not applicable.                                                                       fed powdered infant formulas. Pediatrics. 2012;130:e1076–84. https://​
                                                                                      doi.​org/​10.​1542/​peds.​2011-​3855.
                                                                                  13. Bowen A, Wiesenfeld HC, Kloesz JL, Pasculle AW, Nowalk AJ, Brink L,
Declarations                                                                          Elliot E, Martin H, Tarr CL. Notes from the field: Cronobacter sakazakii
                                                                                      infection associated with feeding extrinsically contaminated expressed
Ethics approval and consent to participate                                            human milk to a premature infant—pennsylvania. Morb Mortal Wkly
Not applicable.                                                                       Rep. 2017;66:761–2.
                                                                                  14. McMullan R, Menon V, Beukers AG, Jensen SO, van Hal SJ, Davis R.
Consent for publication                                                               Cronobacter sakazakii infection from expressed breast milk. Australia
Yes.                                                                                  Emerg Infect Dis. 2018;24:393–4.
                                                                                  15. Chase HR, Gopinath GR, Eshwar AK, Stoller A, Fricker-Feer C, Gangiredla
Competing interests                                                                   J, et al. Comparative genomic characterization of the highly persistent
The authors declare that they have no competing interests.                            and potentially virulent Cronobacter sakazakii ST83, CC65 strain H322
                                                                                      and other ST83 strains. Front Microbiol. 2017;8:1136.
Author details                                                                    16. Gopinath GR, Chase HR, Gangiredla J, Eshwar A, Jang H, Patel I, Negrete
1
  Center for Food Safety and Applied Nutrition, Office of Applied Research            F, Finkelstein S, Park E, Chung T, Yoo Y, Woo J, Lee Y, Park J, Choi H,
and Safety Assessment, U. S. Food and Drug Administration, Laurel, MD, USA.           Jeong S, Jun S, Kim M, Lee C, Jeong H, Fanning S, Stephan R, Iversen
2
  Joint Institute for Food Safety and Applied Nutrition, University of Maryland       C, Reich F, Klein G, Lehner A, Tall BD. Genomic characterization of
College Park, College Park, MD, USA. 3 Center for Food Safety and Applied             malonate positive Cronobacter sakazakii serotype O:2, sequence type
Nutrition, Office of Regulatory Science, Food and Drug Administration, College        64 strains, isolated from clinical, food, and environment samples. Gut
Park, MD, USA. 4 Institute for Food Safety and Hygiene, University of Zürich,         Pathog. 2018. https://​doi.​org/​10.​1186/​s13099-​018-​0238-9.
Zurich, Switzerland. 5 WHO Collaborating Centre for Cronobacter, University       17. Jang H, Chase HR, Gangiredla J, Grim CJ, Patel IR, Kothary MH, et al.
College Dublin, Dublin, Ireland. 6 School of Public Health, Physiotherapy             Analysis of the molecular diversity among Cronobacter species isolated
and Population Science, UCD Centre for Food Safety, University College                from filth flies using targeted PCR, pan genomic DNA microarray, and
Dublin, Dublin, Ireland.                                                              whole genome sequencing analyses. Front Microbiol. 2020;11: 561204.
                                                                                  18. Jang H, Woo J, Lee Y, Negrete F, Finkelstein S, Chase HR, Addy N, Ewing
Received: 8 December 2021 Accepted: 16 May 2022                                       L, Beaubrun JJG, Patel I, Gangiredla J, Eshwar A, Jaradat ZW, Seo K,
                                                                                      Shabarinath S, Fanning S, Stephan R, Lehner A, Tall BD, Gopinath GR.
                                                                                      Draft genomes of Cronobacter sakazakii strains isolated from dried
                                                                                      spices bring unique insights into the diversity of plant-associated
                                                                                      strains. Stand Genomic Sci. 2018;13:35. https://​doi.​org/​10.​1186/​
References                                                                            s40793-​018-​0339-6.
1. Jang H, Gopinath GR, Eshwar A, Srikumar S, Nguyen S, Gangiredla J,             19. Eid J, Fehr A, Gray J, Luong K, Lyle J, Otto G, Peluso P, Rank D, Baybayan P,
    Patel IR, Finkelstein SB, Negrete F, Woo J, Lee Y, Fanning S, Stephan R,          Bettman B, Bibillo A, Bjornson K, Chaudhuri B, Christians F, Cicero R, Clark
    Tall BD, Lehner A. The secretion of toxins and other exoproteins of               S, Dalal R, Dewinter A, Dixon J, Foquet M, Gaertner A, Hardenbol P, Heiner
    Cronobacter: role in virulence, adaption, and persistence. Microorganisms.        C, Hester K, Holden D, Kearns G, Kong X, Kuse R, Lacroix Y, Lin S, Lundquist
    2020;8(2):229. https://​doi.​org/​10.​3390/​micro​organ​isms8​020229.             P, Ma C, Marks P, Maxham M, Murphy D, Park I, Pham T, Phillips M, Roy J,
2. Holý O, Petrželová J, Hanulík V, Chromá M, Matoušková M, Forsythe SJ.              Sebra R, Shen G, Sorenson J, Tomaney A, Travers K, Trulson M, Vieceli J,
    Epidemiology of Cronobacter spp. isolates from patients admitted to               Wegener J, Wu D, Yang A, Zaccarin D, Zhao P, Zhong F, Korlach J, Turner S.
    the Olomouc University Hospital (Czech Republic). Epidemiol Mikrobiol             Real-time DNA sequencing from single polymerase molecules. Science.
    Imunol. 2014;63:69–72.                                                            2009;323:133–8.
3. Patrick ME, Mahon BE, Greene SA, Rounds J, Cronquist A, Wymore K,              20. Wick RR, Judd LM, Gorrie CL. and Holt KE Unicycler: resolving bacterial
    et al. Incidence of Cronobacter spp. infections, United States, 2003–2009.        genome assemblies from short and long sequencing reads. PLoS Com-
    Emerg Infect Dis. 2014;20:1520–3.                                                 put Biology. 2017;13(6): e1005595. https://​doi.​org/​10.​1371/​journ​al.​pcbi.​
4. Alsonosi A, Hariri S, Kajsík M, Oriešková M, Hanulík V, Röderová M, et al.         10055​95.
    The speciation and genotyping of Cronobacter isolates from hospitalised       21. Haft DH, DiCuccio M, Badretdin A, Brover V, Chetvernin V, O’Neill K, Li W,
    patients. Eur J Clin Microbiol Infect Dis. 2015;34:1979–88.                       Chitsaz F, Derbyshire MK, Gonzales NR, Gwadz M, Lu F, Marchler GH, Song
5. Yong W, Guo B, Shi X, Cheng T, Chen T, JiangX, et al. An investigation of an       JS, Thanki N, Yamashita RA, Zheng C, Thibaud-Nissen F, Geer LY, Marchler-
    acute gastroenteritis outbreak: Cronobacter sakazakii, a potential cause of       Bauer A, Pruitt KD. RefSeq: an update on prokaryotic genome annotation
    food-borne illness. Front Microbiol. 2018;2018(9):549.                            and curation. Nucleic Acids Res. 2018;46(D1):D851–60. https://​doi.​org/​10.​
6. Friedemann M. Epidemiology of invasive neonatal Cronobacter                        1093/​nar/​gkx10​68.
    (Enterobacter sakazakii) infections. Eur J Clin Microbiol Infect Dis.         22. Overbeek R, Olson R, Pusch GD, Olsen GJ, DavisDisz JJT, et al. The SEED
    2009;28:1297–304.                                                                 and the rapid annotation of microbial genomes using subsystems
Negrete et al. Gut Pathogens          (2022) 14:23                                                                                                       Page 12 of 12




      technology (RAST). Nucleic Acids Res. 2014;42:D206–14. https://​doi.​org/​         Cronobacter sakazakii SP291. Appl Environ Microbiol. 2019. https://​doi.​
      10.​1093/​nar/​gkt12​26.                                                           org/​10.​1128/​AEM.​01993-​18.
23.   Stothard P, Grant JR, Van Domselaar G. Visualizing and comparing               41. Flores-Díaz M, Monturiol-Gross L, Naylor C, Alape-Girón A, Flieger A.
      circular genomes using the CGView family of tools. Brief Bioinform.                Bacterial sphingomyelinases and phospholipases as virulence factors.
      2019;2019(20):1576–82.                                                             Microbiol Mol Biol Rev. 2016;80:597–628. https://​doi.​org/​10.​1128/​MMBR.​
24.   Carattoli A, Hasman H. PlasmidFinder and in silico pMLST: identification           00082-​15.
      and typing of plasmid replicons in whole-genome sequencing (WGS). In:          42. Wang M, Cao H, Wang Q, Xu T, Guo X, Liu B. The roles of two type VI
      de la Cruz F, editor. Horizontal gene transfer. New York: Humana; 2020. p.         secretion systems in Cronobacter sakazakii ATCC 12868. Front Microbiol.
      285–94.                                                                            2018;22(9):2499.
25.   Arndt D, Grant JR, Marcu A, Sajed T, Pon A, Liang Y, Wishart DS. PHASTER:
      a better, faster version of the PHAST phage search tool. Nucleic Acids Res.
      2016;44(w1):W16-21. https://​doi.​org/​10.​1093/​nar/​gkw387.                  Publisher’s Note
26.   Zhou Y, Liang Y, Lynch KH, Dennis JJ, Wishart DS. PHAST: a fast phage          Springer Nature remains neutral with regard to jurisdictional claims in pub-
      search tool. Nucleic Acids Res. 2011;39:W347–52.                               lished maps and institutional affiliations.
27.   Darling AC, Mau B, Blattner FR, Perna NT. Mauve: multiple alignment
      of conserved genomic sequence with rearrangements. Genome Res.
      2004;14:1394–403. https://​doi.​org/​10.​1101/​gr.​22897​04.
28.   Darling AE, Mau B, Perna NT. Progressivemauve: multiple genome align-
      ment with gene gain, loss and rearrangement. PLoS ONE. 2010;5: e11147.
      https://​doi.​org/​10.​1371/​journ​al.​pone.​00111​47.
29.   Chase HR, Gopinath GR, Gangiredla J, Patel IR, Kothary MH, Carter L,
      Sathyamoorthy V, Lee B, Park E, Yoo YJ, Chung TJ, Choi H, Jun S, Park J,
      Jeong S, Kim M, Reich F, Klein G, Tall BD. Genome sequences of malonate-
      positive cronobacter sakazakii serogroup O:2, sequence Type 64 strains
      CDC 1121-73 and GK1025, isolated from human bronchial wash and
      a powdered infant formula manufacturing plant. Genome Announc.
      2016;4(6):e01072-1116.
30.   Power KA, Yan Q, Fox EM, Cooney S, Fanning S. Genome sequence of
      Cronobacter sakazakii SP291, a persistent thermotolerant isolate derived
      from a factory producing powdered infant formula. Genome Announc.
      2013. https://​doi.​org/​10.​1128/​genom​eA.​00082-​13.
31.   Franco AA, Hu L, Grim CJ, Gopinath G, Sathyamoorthy V, Jarvis KG, Lee
      C, Sadowski J, Kim J, Kothary MH, McCardell BA, Tall BD. Characterization
      of putative virulence genes on the related repFIB plasmids harbored by
      Cronobacter spp. Appl Environ Microbiol. 2011;77:3255–67.
32.   Tall BD, Gopinath GR, Gangiredla J, Patel IR, Fanning S, Lehner A. Food
      microbiology fundamentals and frontiers. In: Doyle MP, Diez-Gonzalez F,
      Hill C, editors. Chapter 14. Cronobacter species. 5th ed. Washington, DC:
      ASM Press; 2019. p. 389–414.
33.   Kucerova E, Clifton SW, Xia XQ, Long F, Porwollik S, Fulton L, Fronick C,
      Minx P, Kyung K, Warren W, Fulton R, Feng D, Wollam A, Shah N, Bhonagiri
      V, Nash WE, Hallsworth-Pepin K, Wilson RK, McClelland M, Forsythe SJ.
      Genome sequence of Cronobacter sakazakii BAA-894 and comparative
      genomic hybridization analysis with other Cronobacter species. PLoS
      ONE. 2010;5(3):9556. https://​doi.​org/​10.​1371/​journ​al.​pone.​00095​56.
34.   Ikeda H, Tomizawa J. Prophage P1, and extrachromosomal replication
      unit Cold Spring Harb. Symp Quant Biol. 1968;33(791):798. https://​doi.​
      org/​10.​1101/​sqb.​1968.​033.​01.​091.
35.   Pfeifer E. Moura de Sousa JA, Touchon M, and Rocha EPC, Bacteria have
      numerous distinctive groups of phage–plasmids with conserved phage
      and variable plasmid gene repertoires. Nucleic Acids Res. 2021;49:2655–
      73. https://​doi.​org/​10.​1093/​nar/​gkab0​64.
36.   Eida AA, Bougouffa S, L’Haridon F, Alam I, Weisskopf L, Bajic VB, Saad
      MM, Hirt H. Genome insights of the plant-growth promoting bacterium
      Cronobacter muytjensii Z38 with volatile-mediated antagonistic activity
      against Phytophthora infestans. Front Microbiol. 2020;11:369. https://​doi.​
      org/​10.​3389/​fmicb.​2020.​00369.
                                                                                         Ready to submit your research ? Choose BMC and benefit from:
37.   Kim M, Kim S, Ryu S. Complete genome sequence of bacteriophage SSU5
      specific for Salmonella enterica serovar Typhimurium rough strains. J Virol.
                                                                                           • fast, convenient online submission
      2012;86:10894.
38.   Gilcrease EB, Casjens SR. The genome sequence of Escherichia coli                    • thorough peer review by experienced researchers in your field
      tailed phage D6 and the diversity of enterobacteriales circular plasmid              • rapid publication on acceptance
      prophages. Virology. 2018;515:203–14. https://​doi.​org/​10.​1016/j.​virol.​
                                                                                           • support for research data, including large and complex data types
      2017.​12.​019.
39.   Erazo Garzon A, Mahony J, Bottacini F, Kelleher P, van Sinderen D. Com-              • gold Open Access which fosters wider collaboration and increased citations
      plete genome sequence of Lactococcus lactis subsp. cremoris 3107, Host               • maximum visibility for your research: over 100M website views per year
      for the model lactococcal P335 bacteriophage TP901–1. Microbiol Res
      Announce. 2019. https://​doi.​org/​10.​1128/​MRA.​01635-​18.                       At BMC, research is always in progress.
40.   Srikumar S, Cao Y, Yan Q, Van Hoorde K, Nguyen S, Cooney S, Gopi-
      nath GR, Tall BD, Sivasankaran SK, Lehner A, Stephan R, Fanning S.                 Learn more biomedcentral.com/submissions
      RNA Sequencing-based transcriptional overview of xerotolerance in
