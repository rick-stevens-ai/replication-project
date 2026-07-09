# Torres et al. 2023 — Marker fallback extraction

> **Source:** paper.pdf (sha256 a6c26201…) → `pdftotext -layout`.
> **Note:** This is a `pdftotext` fallback (Marker binary not available in this replication env); layout is preserved but no equation/table structure. Central Eagle Marker corpus should replace this file when the sha256 sweep hits it.

---

                                                                                  F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




RESEARCH ARTICLE

             Stenotrophomonas goyi sp. nov., a novel bacterium
associated with the alga Chlamydomonas reinhardtii
[version 3; peer review: 2 approved]

María Jesus Torres 1*, Neda Fakhimi                            1,2*, Alexandra Dubini                 1,

David González-Ballester 1
1Departamento de Bioquímica y Biología Molecular, Campus Universitario de Rabanales, Universidad de Cordoba, Córdoba,

Andalusia, 14071, Spain
2Carnegie Institution for Science Department of Biosphere Sciences and Engineering, Stanford, California, 94305, USA

* Equal contributors




v3 First published: 18 Oct 2023, 12:1373                                         Open Peer Review
     https://doi.org/10.12688/f1000research.134978.1
     Second version: 23 Oct 2023, 12:1373
     https://doi.org/10.12688/f1000research.134978.2                             Approval Status
     Latest published: 14 Dec 2023, 12:1373
     https://doi.org/10.12688/f1000research.134978.3                                                   1                   2


                                                                                 version 3
Abstract                                                                         (revision)
                                                                                 14 Dec 2023
Background
                                                                                 version 2
A culture of the green algae Chlamydomonas reinhardtii was                       (revision)          view                 view
accidentally contaminated with three different bacteria in our                   23 Oct 2023

laboratory facilities. This contaminated alga culture showed increased
                                                                                 version 1
algal biohydrogen production. These three bacteria were                          18 Oct 2023
independently isolated.
                                                                                  1. Rosa Leon-Bañares       , University of Huelva,
Methods                                                                             Huelva, Spain

The chromosomic DNA of one of the isolated bacteria was extracted                 2. Gergely Maroti, Biological Research Centre,
and sequenced using PacBio technology. Tentative genome                             Szeged, Hungary
annotation (RAST server) and phylogenetic trees analysis (TYGS server)
were conducted. Diverse growth tests were assayed for the bacterium              Any reports and responses or comments on the

and for the alga-bacterium consortium.                                           article can be found at the end of the article.


Results

Phylogenetic analysis indicates that the bacterium is a novel member
of the Stenotrophomonas genus that has been termed in this work as S.
goyi sp. nov. A fully sequenced genome (4,487,389 base pairs) and its
tentative annotation (4,147 genes) are provided. The genome
information suggests that S. goyi sp. nov. is unable to use sulfate and




                                                                                                                           Page 1 of 16
                                                                                        F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




nitrate as sulfur and nitrogen sources, respectively. Growth tests have
confirmed the dependence on the sulfur-containing amino acids
methionine and cysteine. S. goyi sp. nov. and Chlamydomonas
reinhardtii can establish a mutualistic relationship when cocultured
together.

Conclusions

S. goyi sp. nov. could be of interest for the design of biotechnological
approaches based on the use of artificial microalgae-bacteria
multispecies consortia that take advantage of the complementary
metabolic capacities of their different microorganisms.


Keywords
algae, bacteria, consortia, cocultures, Chlamydomonas,
Stenotrophomonas, vitamins, metabolic complementation


 Corresponding author: Alexandra Dubini (alexandra.dubini@uco.es)
 Author roles: Torres MJ: Formal Analysis, Investigation, Methodology, Visualization, Writing – Review & Editing; Fakhimi N: Formal
 Analysis, Investigation, Methodology, Writing – Review & Editing; Dubini A: Conceptualization, Methodology, Project Administration,
 Resources, Supervision, Writing – Original Draft Preparation, Writing – Review & Editing; González-Ballester D: Conceptualization, Data
 Curation, Methodology, Project Administration, Resources, Supervision, Visualization, Writing – Original Draft Preparation, Writing –
 Review & Editing
 Competing interests: No competing interests were disclosed.
 Grant information: This research was funded by the European ERANETMED [A.D; ERANETMED2-72-300] and NextGenerationEU/PRTR
 [A.D; TED2021-130438B-I00] programs, the Spanish Ministerio de Ciencia e Innovación [D. G-B; PID2019-105936RB-C22] and
 MCIN/AEI/10.13039/501100011033 [D. G-B; TED2021-130438B-I00], the UCO-FEDER [D. G.-B; UCO-1381175], the Plan Propio of University
 of Córdoba [A.D; MOD.4.1 P.P.2016 A. DUBINI] and the Maria Zambrano program [M.J.T; UCOR02MZ].
 The funders had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript.
 Copyright: © 2023 Torres MJ et al. This is an open access article distributed under the terms of the Creative Commons Attribution
 License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.
 How to cite this article: Torres MJ, Fakhimi N, Dubini A and González-Ballester D. Stenotrophomonas goyi sp. nov., a novel bacterium
 associated with the alga Chlamydomonas reinhardtii [version 3; peer review: 2 approved] F1000Research 2023, 12:1373
 https://doi.org/10.12688/f1000research.134978.3
 First published: 18 Oct 2023, 12:1373 https://doi.org/10.12688/f1000research.134978.1




                                                                                                                                 Page 2 of 16
                                                                                 F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




  REVISED Amendments from Version 2
  A second accession number has been provided for the repository of Stenotrophomonas goyi sp. nov. The bacteria is now
  deposited in two internationally recognized culture collections.

  The use of italics within the name of Stenotrophomonas goyi sp. nov. has been homogenized.

  Two references have been updated.

  Any further responses from the reviewers can be found at the end of the article




Introduction
The first described species of the Stenotrophomonas genus was S. maltophilia, which was a Gram-negative bacterium
originally named as Pseudomonas maltophilia, and later transferred in 1993 to the new genus Stenotrophomonas, which
was solely composed of S. maltophilia. In 2001, this species was moved to the genus Xanthomonas before it was finally
moved back again in 2017 to its own genus when Stenotrophomonas pictorum was identified (Ryan et al., 2009; Wei
et al., 2021). Currently, Stenotrophomonas is a genus comprising at least 19 validated species (https://lpsn.dsmz.de/
genus/stenotrophomonas) (Parte et al., 2020). However, the molecular taxonomy of the genus is still somewhat unclear,
and all its members are considered as “orphan species”. All Stenotrophomonas spp. have shown intraspecific hetero-
geneity with high phenotypic, metabolic, and ecological diversity (Ryan et al., 2009).

The main reservoirs of Stenotrophomonas spp. are soil and plants, although they are ubiquitously present in different
environments, including opportunistic human pathogens such as S. maltophilia (Ryan et al., 2009).

Stenotrophomonas spp. show promising potential for different biotechnological applications. Some Stenotrophomonas
spp. are of interest to agriculture due to their ability to promote growth in different plant species. Some Stenotrophomonas
spp. are even capable of establishing symbiotic relationships with plants. This plant growth promotion is related to the
capacity of some Stenotrophomonas spp. to produce the plant growth hormone indole-3-acetic acid (IAA), fix nitrogen,
oxidate elemental sulfur (S) to sulfate, or biocontrol plant pathogens (Banerjee and Yesmin, 2008; Park et al., 2005; Ryan
et al., 2009; Suckstorff and Berg, 2003).

Moreover, they are also considered good candidates for bioremediation due to their tolerance to heavy metals and
capability to metabolize a large variety of organic molecules, including phenolic and aromatic compounds (Liu et al.,
2007; Mora-Salguero et al., 2019; Pages et al., 2008; Ryan et al., 2009). Finally, some Stenotrophomonas spp. can
synthetize useful bioproducts such as antimicrobial and enzymes of biotechnological interest (Rivas-Garcia et al., 2022;
Wolf et al., 2002).

Here we report the genome of Stenotrophomonas goyi sp. nov. isolated from a contaminated microalgae (Chlamydo-
monas reinhardtii) culture. This alga culture was simultaneously contaminated with S. goyi, Microbacterium forte
(Fakhimi et al., 2023a) and Bacillus cereus. The metabolic interactions established between these four microorganisms
are analyzed and discussed in a related publication where the ability of this multispecies consortium to sustain hydrogen
production is highlighted (Fakhimi et al., 2023a).

Methods
Isolation of Stenotrophomonas goyi sp. nov.
This study took place at Campus Universitario de Rabanales, Cordoba, Spain. S. goyi sp. nov. where it was isolated from a
fortuitously contaminated Chlamydomonas reinhardtii culture in the laboratory. Initially, the Chlamydomonas rein-
hardtii culture was simultaneously contaminated with three different bacteria (Fakhimi et al., 2023a). Individual
members of this bacterial community were isolated by sequential rounds of plate streaking in Yeast Extract Mannitol
(YEM) medium (handmade in our lab, described here), until three different types of bacterial colonies were visually
identified. Colonies were grown separately, and the subsequent isolated DNA was used for PCR-amplification of their
partial RNA 16S sequences. After sequencing, the three independently isolated bacteria were identified as members of the
genus Microbacterium, Stenotrophomonas, and Bacillus (Fakhimi et al., 2023a).

Genome sequencing and assembling of S. goyi sp. nov.
DNA extraction and whole genome sequencing using PacBio (Pacific Biosciences) RS II Sequencing System (RRID:
SCR_017988) were performed by SNPsaurus LLC (https://www.snpsaurus.com/). Whole genome sequencing generated
102,238 reads yielding 832,209,774 bases for 166 read depth over the genome (Table 1). Genome was assembled with
Canu (RRID:SCR_015880) 1.7 (Koren et al., 2017) generating a 4,487,389 pb circular genome. The genome
                                                                                                                           Page 3 of 16
                                                                                F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Table 1. Main de novo sequencing and assembly statistics of Stenotrophomonas goyi sp. nov. genome.

 Genome Size (pb)          Fold-coverage         GC content (%)         N° of contigs        Type           Plasmids
 4,487,389                 166                   66.5                   1                    circular       No


completeness was checked by BUSCO 3.0.2 (RRID:SCR_015008) (Manni et al., 2021) and was 94.6% complete, with
94.6% of the genome single copy and 0.0% duplicated. Any other prokaryotic contamination was discarded using
ContEst16S 1.0 (RRID:SCR_000595) (Lee et al., 2017).

Phylogenetic analysis
Phylogenetic analyses were performed using the Type (Strain) Genome Server (TYGS) at Leibniz Institute DSMZ
(German Collection of Microorganisms and Cell Cultures GmbH) (Camacho et al., 2009; Farris, 1972; Kreft et al., 2017;
Lagesen et al., 2007; Lefort et al., 2015; Meier-Kolthoff et al., 2022, 2013; Meier-Kolthoff and Göker, 2019; Ondov
et al., 2016). Information on nomenclature, synonymy and associated taxonomic literature was provided by TYGS's sister
database, the List of Prokaryotic names with Standing in Nomenclature (LPSN). Trees were inferred with FastME
2.1.6.1. Phylogenetic trees were drawn with iTOL (RRID:SCR_018174) (Letunic and Bork, 2021).

Annotation
Tentative annotation of the S. goyi sp. nov. genome was performed using the RAST tool kit, RASTtk (RRID:
SCR_014606) at The Genome Annotation Service (Brettin et al., 2015; Overbeek et al., 2014). BlastKOALA service
was used to automatically assign K numbers to the predicted proteins, which allowed Kyoto Encyclopedia of Genes and
Genomes (KEGG) orthology assignments, the putative characterization of individual gene functions, and the recon-
struction of KEGG pathways (Kanehisa et al., 2016). The PHAge Search Tool Enhanced Release (PHASTER) (RRID:
SCR_005184) was used to locate potential phage sequences within the S. goyi sp. nov. genome (Arndt et al., 2016)

Bacterium growth media and culturing conditions
Bacterial precultures were grown on Yeast Extract Mannitol (YEM) or Luria Broth (LB) media (handmade in our lab).
Some growth experiments were done in Mineral Medium (MM) (Harris, 2008) supplemented with different nutrient
sources (handmade in our lab). Tris-Acetate-Phosphate (TAP) medium (Harris, 2008) (handmade in our lab, described
here) was also used occasionally. In some experiments, a vitamin cocktail (riboflavin, 0.5 mgL-1; p-aminobenzoic acid,
0.1 mgL-1; nicotinic acid 0.1 mgL-1; pantothenic acid, 0.1 mgL-1; pyridoxine, 0.1 mgL-1; biotin, 0.001 mgL-1; vitamin
B12, 0.001 mgL-1; thiamine, 0.001 mgL-1) was added to bacterial cultures. More specific details for each experiment can
be found in the corresponding figure and table legends. All the bacterium cultures were incubated at 24-28°C and under
continuous agitation (130 rpm).

Coculturing algae and bacteria
Chlamydomonas cells were cultured for 3-4 days in TAP medium until mid-logarithmic growth phase, harvested by
centrifugation (5.000 rpm for 5 min) and washed twice with fresh MM. Bacterial batch-cultures were incubated in TYM
or LB medium until the Optical Density at 600 nm (OD600) reached 0.8-1, then harvested by centrifugation (12.000 rpm
for 5 min) and washed twice with fresh MM. Algae and bacteria were cocultured in 250 mL flasks containing 100 mL of
the corresponding medium. Alga-bacterium cocultures were set to initial chlorophyll concentration of 10 μgmL 1 for the
alga and an initial OD600 of 0.1 for the bacterium. Algal and bacterial monocultures were used as controls. All cultures
were incubated at 24°C with continuous agitation (120-140 rpm) and under continuous illumination (80 PPFD).

Determinations of algal and bacterial growth
The algal growth was assessed in terms of chlorophyll content. Chlorophyll measurements were done by mixing 200 μL
of the cultures with 800 μL of ethanol 100%. The mix was incubated at room temperature for 2-3 min, and afterward
centrifuged for 1 min at 12.000 rpm. The supernatant was used to measure chlorophyll (a + b) spectrophotometrically
(DU 800, Beckman Coulter) at 665 and 649 nm (Wintermans and de Mots, 1965).

Bacterial growth in monocultures was estimated spectrophotometrically in terms of OD600 evolution (DU 800, Beckman
Coulter). However, estimation of the bacterial growth in cocultures required bacterium cells separation from the alga
cells. To do this, a customized Selective Centrifugal Sedimentation (SCS) approach was used. This approach consisted in
finding the centrifugation parameters that led to maximize algal cell sedimentation while minimizing bacterial cell
sedimentation (Torres et al., 2022). Thus, measuring the OD of the supernatant after centrifugation can provide an
estimation of the bacterial growth in the cocultures. To do this, the percentages of precipitated cells of each monoculture
were calculated at different forces (from 100 to 500 x g) and times (1 and 2 min) using the measured OD before (ABC) and

                                                                                                                          Page 4 of 16
                                                                             F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




after (AAC) the centrifugation. Centrifugation at 200 x g for 1 min led to 87.9% of Chlamydomonas sedimentation, while
only 2.1% of the bacterial cells dropped (meaning that 97.9% of the S. goyi cells remained in the supernatant). These
parameters were chosen as a good compromise for SCS and used to evaluate the contribution of the bacteria to the OD in
cocultures (SCSOD600).

Results
Identification of Stenotrophomonas goyi sp. nov.
A fortuitous contaminated Chlamydomonas reinhardtii culture (strain 704; CC-3597; https://www.chlamycollection.
org/) was studied due to its enhanced hydrogen production capability. This alga culture turned out to be contaminated
with three different bacterial strains (Fakhimi et al., 2023), one of them consisting in a white-pigmented bacterium
(Figure 1). This bacterium was isolated after several rounds of plate streaking in TYM medium. First, partial PCR
amplification and sequencing of the ribosomal 16S gene allowed the identification of this bacterium as a member of the
Stenotrophomonas genus. Afterwards, the whole genome sequence was obtained. Genome assembling provided one
single circular contig of 4,487,389 pb (Table 1). No plasmids or extrachromosomal elements were identified.

The RAST server identified 4,147 genes (4,066 CDS + 81 rRNAs and tRNAs) (Table 2). Out of these 4,066 CDS
identified by RAST, 1,096 of them were in subsystems. Tentative genome annotation derived from the RAST server is
available in Supplemental Table 1 as Extended data (González-Ballester et al., 2023).

Phylogenetic analyses were performed with both, the whole genome (Figure 2) and the inferred 16S rDNAs (Figure 3).
Pairwise comparisons with the closest type strains genomes are shown in Table 3. These phylogenetic analyses revealed




Figure 1. TAP plate with Chlamydomonas reinhardtii and Stenotrophomonas goyi sp. nov.



Table 2. Genome features of Stenotrophomonas goyi sp. nov. according to the RAST server. tRNA, transfer RNA;
rRNA, ribosomal RNA.

 Genes                         CDS                         tRNAs                         rRNAs
 4,147                         4,066                       71                            10




                                                                                                                      Page 5 of 16
                                                                                                                                                                                                F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




 Tree scale: 0.01
                                                                                                                  0.1076
         0.005
                                                                                                                                                                                                                Xanthomonas maliensis LMG 27592
          100
                                                                                                         0.0999
                                                                                                                                                                                                         Stenotrophomonas panacihumi JCM 16536
                                                                                                                              0.0759
                                                                                                                                                                                                        Stenotrophomonas bentonitica BIIR7
                                    0.0155                                                                                                  0.0751
     0                               100                                                                                                                                                                    Stenotrophomonas nematodicola W5
                                                         0.0054
                                                          100                                                                        0.0697
                                                                       0.0004
                                                                                                                                                                                                    Stenotrophomonas rhizophila DSM 14405
                                                                  40                                                                    0.0737
                                                                                                                                                                                                       Stenotrophomonas goyi sp. nov.
                 0.0118                                                                                                                        0.0802
                                                                                                                                                                                                                Stenotrophomonas tumulicola JCM 30961
                                                0.0142
                                                 100                                                                                                                     0.044
                                                                                              0.0364
                                                                                                                                                                                                                Stenotrophomonas pennii Sa5BUN4
                                                                                                100
                                                                                                                                                                     0.0415
                                                                                                                                                                                                              Stenotrophomonas chelatiphaga DSM 21508
                           0.0062                                                                                                                                        0.0334
                            100
                                                                                                           0.0353
                                                                                                                                                                                                            Stenotrophomonas indicatrix WS40
                                                                                                            100
                                                                                                                                                                         0.0333
                                                                                                                                                                                                           Stenotrophomonas lactitubi M15
                                                     0.0209                                                                                                    0.0406
                                                      100                                                                  0.0048
                                                                                                                                                                                                          Stenotrophomonas pavanii DSM 25135
                                                                                                                            100
                                                                                                                                                                0.0415
                                                                                                                                                                                                           Stenotrophomonas sepilia SM16975 T
                                                                                              0.022
                                                                                               100                                                               0.0379
                                                                                                                                                                                                          Xanthomonas maltophilia NBRC 14161
                                                                                                                             0.0077
                                                                                                                              100                                 0.0377
                                                                                                                                                                                                          Stenotrophomonas geniculata JCM 13324
                                                                                                                                             0.0005
                                                                                                                                       51                         0.0379
                                                                                                                                                                                                           Stenotrophomonas africana LMG 22072


Figure 2. Phylogenetic tree for Stenotrophomonas goyi genome and related closest bacteria. Tree inferred with
FastME 2.1.6.1 using the Genome BLAST Distance Phylogeny (GBDP) distances calculated from genome sequences.
The branch lengths are scaled in terms of GBDP distance formula d5. The numbers above the branches are GBDP
pseudo-bootstrap support values > 60% from 100 replications, with an average branch support of 91.6%. The tree
was rooted at the midpoint. Branch lengths (black) and bootstraps (red) values are indicated. Genome sizes:
3,906,271–5,177,426 pb. Average δ statistics: 0.078 (Holland et al., 2002). Phylogenetic tree drawn with iTOL (Letunic
and Bork, 2021).


                          Tree scale: 0.001
                                                                                                                                                        0.01
                                             0.004
                                                                                                                                                                                                                    Xanthomonas maliensis LMG 27592
                                              95
                                                                                                                                            0.0084
                                                                                                                                                                                                    Stenotrophomonas panacihumi JCM 16536
         0.0011
                                                                                    0.0052
                                                                                                                 Stenotrophomonas bentonitica BIIR7
                            0.002                                                                     0.0017
                              76                                                                              Stenotrophomonas rhizophila DSM 14405
                                                                       0.0031
                                                                         77                       0.0006
                                                                                       0.0002
                                                                                                         Stenotrophomonas nematodicola W5
                                                                                              48
 0                                                                                               0    Stenotrophomonas goyi sp. nov.
                                                                                                        0.0029
                                                                                                                                      Stenotrophomonas tumulicola JCM 30961
                                                                           0.0016
                                                                             87                                                     0.001
                                                                                                      0.0025
                                                                                                                                                Stenotrophomonas pennii Sa5BUN4
                                                                                                        98                    0.0003
                                                                                                                                      Stenotrophomonas chelatiphaga DSM 21508
                           0.0042
                            100                                                                                                       0.0018
                                                                                                                  0.0007
                                                                                                                                              Stenotrophomonas indicatrix WS40
                                                                                                                    50
                                                                                                                                               0.0028
                                                                                                                                                               Stenotrophomonas lactitubi M15
                                                                                     0.0033
                                                                                      100                                                                                  0.0025
                                                                                                                                                                                                Stenotrophomonas africana LMG 22072
                                                                                                                                        0.0035                                              0.0023
                                                                                                                                          99                                                            Xanthomonas maltophilia NBRC 14161
                                                                                                                                                                  0.0013                     0.001
                                                                                                                                                                    73                              Stenotrophomonas pavanii DSM 25135
                                                                                                                                                                                  0.0008
                                                                                                                                                                                    70              0
                                                                                                                                                                                           0.0006
                                                                                                                                                                                                        Stenotrophomonas geniculata JCM 13324
                                                                                                                                                                                             49
                                                                                                                                                                                                           0.0015
                                                                                                                                                                                                                    Stenotrophomonas sepilia SM16975 T


Figure 3. Phylogenetic tree for Stenotrophomonas goyi 16S rDNA and related closest bacteria. Tree inferred with
FastME 2.1.6.1 using the Genome BLAST Distance Phylogeny (GBDP) distances calculated from 16S rDNA gene
sequences. The branch lengths are scaled in terms of GBDP distance formula d5. The numbers above branches are
GBDP pseudo-bootstrap support values > 60% from 100 replications, with an average branch support of 78.6%. The
tree was rooted at the midpoint. Branch lengths (black) and bootstraps (red) values are indicated. RNA16S lengths:
1,385–1,535 pb. Average δ statistics: 0.236 (Holland et al., 2002). Phylogenetic tree drawn with iTOL (Letunic and Bork,
2021).


that the sequenced genome belonged to a new Stenotrophomonas sp.; all dDDH values (d0, d4 and d6) were below 70%
(Meier-Kolthoff et al., 2013) (Table 3). This new bacterial species was named as Stenotrophomonas goyi sp. nov. The
closest related bacteria in terms of whole genome and 16S rDNA similarities were Stenotrophomonas rhizophila DSM
14405 and Stenotrophomonas nematodicola W5, respectively (Figures 2 and 3). S. goyi sp. nov. genome was deposited in
the NCBI as SUB12103906.

BlastKOALA (Kanehisa et al., 2016) service allowed KEGG orthology assignments to characterize individual gene
functions and reconstruct KEGG pathways of S. goyi genome (Supplemental Table 2; Extended data (González-
Ballester et al., 2023)). Some important pathways were either absent or incomplete in S. goyi sp. nov. including
assimilation of nitrate (the whole assimilatory pathway is missing including nitrate transporters) and sulfate (only sulfite
reductase is present). On the other hand, putative complete pathways for the glyoxylate cycle and biosynthesis of biotin,
coenzyme A, pantothenate, riboflavin, tetrahydrofolate, glutathione, pyridoxal-P, lipoic acid, dTDP-L-rhamnose, UDP-
N-acetyl-D-glucosamine, C5 isoprenoids, bacterial lipopolysaccharides, and antimicrobial proteins, among others, were
present. Incomplete pathways for the degradation of aromatic compounds (including phenol, toluene, xylene, methyl-
naphthalene, 3-hydroxytoluene, and terephthalate) and myo-inositol biosynthesis, were also present.

                                                                                                                                                                                                                                                         Page 6 of 16
               Table 3. Pairwise dDDH values between S. goyi sp. nov. and the closest type strains genomes. The digital DNA-DNA Hybridization (dDDH) values are provided along with their
               confidence intervals (C.I.) for the three different Genome BLAST Distance Phylogeny (GBDP) formulas: a) formula d0: length of all High-Scoring segment Pairs (HSPs) divided by
               total genome length; b) formula d4: sum of all identities found in HSPs divided by overall HSP length; formula d6: sum of all identities found in HSPs divided by total genome length
               (Meier-Kolthoff et al., 2013).

                Closest strains to Stenotrophomonas goyi sp.          dDDH           C.I.           dDDH               C.I.             dDDH                C.I.             G+C content
                nov.                                                  (d0, in %)     (d0, in %)     (d4, in %)         (d4, in %)       (d6, in %)          (d6, in %)       difference (in %)
                Stenotrophomonas rhizophila DSM 14405                 50,6           [47.2-54.0]    30,9               [28.6-33.5]      45                  [42.0-48.1]      0,78
                Stenotrophomonas nematodicola W5                      48,9           [45.5-52.4]    29,9               [27.5-32.4]      43,4                [40.4-46.4]      0,82
                Stenotrophomonas bentonitica BIIR7                    40,9           [37.5-44.3]    28,9               [26.5-31.4]      37,1                [34.1-40.1]      0,05
                Xanthomonas maltophilia NBRC 14161                    36,2           [32.8-39.7]    24,8               [22.5-27.3]      32,3                [29.3-35.4]      0,34
                Stenotrophomonas sepilia SM16975 T                    37,4           [34.0-40.9]    24,6               [22.3-27.1]      33,1                [30.1-36.2]      0,06
                Stenotrophomonas lactitubi M15                        37,7           [34.3-41.1]    24,6               [22.3-27.1]      33,3                [30.3-36.4]      0,63
                Stenotrophomonas geniculata JCM 13324                 36,4           [33.0-39.9]    24,4               [22.1-26.9]      32,3                [29.4-35.4]      0,34
                Stenotrophomonas africana LMG 22072                   35             [31.6-38.5]    24,4               [22.0-26.8]      31,3                [28.4-34.4]      0,21
                Stenotrophomonas indicatrix WS40                      39,2           [35.8-42.7]    24,4               [22.0-26.8]      34,2                [31.3-37.3]      0,09
                Stenotrophomonas tumulicola JCM 30961                 33,1           [29.7-36.7]    24,4               [22.0-26.8]      29,9                [27.0-33.0]      0,9
                Stenotrophomonas pavanii DSM 25135                    38,6           [35.3-42.1]    24,3               [22.0-26.8]      33,8                [30.9-36.9]      0,87
                Stenotrophomonas chelatiphaga DSM 21508               36,6           [33.3-40.1]    24,2               [21.9-26.6]      32,4                [29.5-35.5]      0,32
                Stenotrophomonas pennii Sa5BUN4                       35,9           [32.5-39.4]    24                 [21.7-26.5]      31,8                [28.9-34.9]      0,08
                Stenotrophomonas panacihumi JCM 16536                 26,7           [23.4-30.4]    22,4               [20.1-24.8]      24,7                [21.9-27.8]      2,37
                Xanthomonas maliensis LMG 27592                       19,3           [16.1-22.9]    21,5               [19.2-23.9]      18,8                [16.1-21.8]      0,32




Page 7 of 16
                                                                                                                                                                                                       F1000Research 2023, 12:1373 Last updated: 29 JUL 2025
                                                                                  F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Table 4. Growth of S. goyi sp. nov. on different nutrients. Mineral Medium (MM) was supplemented with different
nutrients at 5 gL-1 each, but methanol and ethanol (5 mlL-1). For acetic acid, Tris-Acetate-Phosphate (TAP) medium
was employed (1.05 gL-1 of acetic acid). Vitamins cocktail included riboflavin (0.5 mgL-1), p-aminobenzoic acid (0.1
mgL-1), nicotinic acid (0.1 mgL-1), pantothenic acid (0.1 mgL-1), pyridoxine (0.1 mgL-1), biotin (0.001 mgL-1), vitamin
B12 (0.001 mgL-1), thiamine (0.001 mgL-1). ++, significant growth; +, poor growth; -, no growth.

 Nutrients added                                                        Growth
 Sucrose                                                                -
 Lactose                                                                -
 Lactose + vitamins                                                     -
 Glucose                                                                -
 Glucose + vitamins                                                     -
 Mannitol                                                               -
 Lactic acid                                                            -
 Glycerol                                                               -
 Acetic acid (TAP medium)                                               -
 Tryptone                                                               ++
 Peptone                                                                ++
 Yeast extract                                                          ++
 BSA                                                                    ++




Search with PHASTER (Arndt et al., 2016) revealed one intact prophage (PHAGE_Erwini_phiEt88_NC_015295)
located at position 753112-799783 of the S. goyi sp. nov. genome.

Nutrient requirements of S. goyi sp. nov.
S. goyi sp. nov. showed no growth on MM, or in MM supplemented with different C sources (sucrose, glucose, lactose,
mannitol, or glycerol) (Table 4). The addition of vitamins to the MM supplemented with glucose or lactose did not support
the bacterium growth either (Table 4). However, the bacterium showed an excellent growth when cultivated in MM
supplemented with yeast extract, tryptone, peptone or even Bovine Serum Albumin (BSA) (Table 4), suggesting that this
bacterium has a great capacity to use peptides/amino acids as C source, and probably also as N source. Moreover, the
peptides/amino acids could also provide, in addition to C and N sources, other essential nutrients or even palliate potential
amino acids auxotrophies. Note that MM medium has sulfate as only S source. As commented before, the genome of
S. goyi sp. nov. is lacking a functional sulfate assimilation pathway. Thereby S-containing amino acids, such as cysteine
and methionine, could support the growth in medium rich in peptides/amino acids.

To confirm this hypothesis, S. goyi sp. nov. was inoculated in plates of MM + glucose supplemented with different
combinations of cysteine, methionine, biotin, and thiamine. Only plates containing cysteine and methionine supported
the bacterial growth for several culturing rounds (Figure 4). This result confirms the cysteine and methionine growth
dependence of S. goyi. sp. nov. Cysteine and methionine could provide either a reduced S source or complement an
auxotrophy for these two amino acids. Since S. goyi sp. nov. genome has complete pathways for all the essential amino
acids, is more likely that cysteine and methionine are being used as reduced S sources. Similar results were found for
M. forte, where cysteine and methionine are required as S sources (Fakhimi et al., 2023a).

S. goyi sp. nov. showed optimal growth between 24 and 32°C and pH 5-9 (Table 5). Despite the presence of the complete
multidrug resistance efflux pump MexJK-OprM in the genome (Chuanchuen et al., 2005), no resistance to tetracycline,
rifampicin, chloramphenicol and polymyxin (50 μg/mL each) was observed.

Growth of S. goyi sp. nov -C. reinhardtii consortium
Torres et al. (2022) reported that cocultures of S. goyi sp. nov. (published as Stenotrophomonas sp.) and C. reinhardtii
promoted the growth of the microalga (nearly doubled) when incubated in MM supplemented with glucose and mannitol,
but not when supplemented with acetic acid.




                                                                                                                            Page 8 of 16
                                                                           F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Figure 4. Cysteine and methionine requirements of S. goyi to grow. S. goyi sp. nov. was inoculated in: A) plates of
Mineral Medium (MM) + glucose (5 gL-1); B) MM + glucose + biotin (0.001 mgL-1) + thiamine (0.001 mgL-1); C) MM +
glucose + cysteine (4 mM) + methionine (4 mM); and D) MM + glucose + cysteine + methionine + biotin + thiamine.



Table 5. Growth of S. goyi sp. nov. at different temperatures and pHs. Lysogeny broth (LB) medium was used in all
the conditions.

 Temperature °C                       Growth                       pH                       Growth
 10                                   -                            3                        -
 15                                   +                            4                        +
 20                                   ++                           5                        +++
 24                                   +++                          6                        +++
 28                                   +++                          7                        +++
 32                                   +++                          8                        +++
 37                                   ++                           9                        +++
 42                                   -                            10                       +
                                                                   11                       -



                                                                                                                    Page 9 of 16
                                                                                F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Figure 5. S. goyi sp. nov. and C. reinhardtii growth in consortium. S. goyi-C. reinhardtii consortium, and respective
control monocultures, were incubated in Mineral Medium (MM) supplemented with glucose (5 gL-1) and mannitol
(5 gL-1). A) Chlorophyll content; B) dry weight biomass after 13 days; C) bacterial growth in terms of ODSCS; D) actual
picture of the cultures after 13 days.

Here, it was also checked if the bacterium also benefited when co-cultivated with C. reinhardtii in glucose- and mannitol-
containing media. First, we observed that the chlorophyll content in the cocultures was 2.4 times higher than in the
C. reinhardtii monocultures after 13 days (Figure 5A), which is in accordance with previous results (Torres et al., 2022).
Additionally, the dry biomass resulting from the consortia was 2.2 times higher than the sum of the respective
monocultures (Figure 5B). Finally, the growth of the bacterium in cocultures was very efficient, unlike S. goyi
sp. nov. monocultures (Figure 5C).

These results indicate that S. goyi sp. nov. and C. reinhardtii can establish a mutualistic relationship when incubated in
sugars-containing media. On the one hand, S. goyi sp. nov. can greatly support the growth of the C. reinhardtii in media
supplemented with glucose or mannitol, which are two carbon sources that the alga cannot utilize. Likely, this growth
promotion is due to the release of acetate and/or CO2 from the bacteria after the sugar fermentation. Acetate is the sole
organic carbon source that C. reinhardtii can utilize during heterotrophic/mixotrophic growth (Chaiboonchoe et al.,
2014). On the other hand, S. goyi, sp. nov. can grow in media without amino acids/peptides supplementation when
cocultured with C. reinhardtii, suggesting that the alga must provide some essential nutrients for the bacterium. Reduced
S forms excreted by the alga (e.g., cysteine or methionine) could potentially explain the bacterium growth in the
consortium.

Discussion and conclusions
Stenotrophomonas spp. are common constituents of the rhizosphere, and their potential for agricultural biotechnology is
arising. However, their association with algae is poorly explored. Most plant growth-promoting bacteria (PGPB) are
firstly identified in the rhizosphere and in association with plants. However, many PGPB are then also often commonly


                                                                                                                        Page 10 of 16
                                                                                 F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




found in association with algae. This is likely reflecting that the kind of relationships established between bacteria and
plants are similar to the relationships between bacteria and algae. This could potentially be the case for Stenotrophomonas
spp., although the relative poor taxonomic curation and heterogeneity of the genus may prevent the tracking of its
association with algae.

Some Stenotrophomonas spp. show a limited nutritional range, while others are capable of metabolic versatility (Ryan
et al., 2009). S. goyi sp. nov. is unable to grow in the absence of a source of peptides/amino acids, which imply that in
natural ecosystems it may rely on other microorganisms to obtain essential nutrients. As stated before, S. goyi sp. nov. is
unable to use sulfate as S source. The peptides/amino acids are likely providing S-reduced forms (such as cysteine and
methionine) to S. goyi sp. nov.

Stenotrophomonas goyi sp. nov. was isolated from an alga culture (C. reinhardtii) that showed an enhanced capacity to
produce hydrogen and biomass when incubated in mannitol and yeast extract containing medium (Fakhimi et al., 2023a).
This algal culture was simultaneously contaminated with two other bacteria: Microbacterium forte and Bacillus cereus.
Out of the three bacteria, M. forte was the main responsible for the enhanced algal hydrogen production. However,
C. reinhardtii-M. forte cocultures were unable to produce hydrogen and biomass concomitantly. In addition to M. forte,
the presence of S. goyi sp. nov. and B. cereus in the cocultures was needed to produce jointly hydrogen and algal biomass
(Fakhimi et al., 2023a), which stresses the biotechnological interest of S. goyi sp. nov.

M. forte showed auxotrophy for biotin and thiamine, and like S. goyi sp. nov. was unable to grow on inorganic S sources
(Fakhimi et al., 2023a). In this multispecies association, S. goyi sp. nov. and C. reinhardtii could alleviate the auxotrophy
of M. forte sp. nov. for biotin and thiamine. S. goyi sp. nov. could also provide ammonium derived from the mineralization
of the amino acids to the alga. On the other hand, the alga could provide S-reduced sources such as cysteine and
methionine for S. goyi sp. nov. and M. forte. In any case, this multispecies association was mutually beneficial and
prevented an excessive bacterial growth in cocultures, which could be one of the main drawbacks when algae-bacteria
cocultures are used for biotechnological applications.

Nevertheless, the precise metabolic relationships established in this multispecies consortium that led to the extension of
the C. reinhardtii cells viability during hydrogen production condition is not yet unraveled and need to be further
investigated.

Ethical considerations
Not applicable.

Data availability
Underlying data
Spanish Type Culture Collection (CECT): Stenotrophomonas goyi sp. nov. bacterium. Accession number CECT30764;
https://www.cect.org/vstrn.php?lan=en&cect=30764 (Universidad de Cordoba, 2022).

NCBI Genome: Stenotrophomonas goyi sp. nov. genome sequence. Accession number CP124620; https://identifiers.
org/ncbi/insdc:CP124620 (Fakhimi et al., 2023b).

Extended data
Zenodo: Supplemental Files, https://doi.org/10.5281/zenodo.8091305 (González-Ballester et al., 2023).

This project contains the following extended data:

      - Supplemental Table 1 [Tentative annotation of the S. goyi sp. nov. genome]

      - Supplemental Table 2 [KEGG orthology assignments]

Data are available under the terms of the Creative Commons Attribution 4.0 International license (CC-BY 4.0).

Acknowledgments
The authors acknowledge Dr. Gregorio Gálvez Valdivieso for his invaluable contribution to this research: perfection
sometimes kills new discoveries. We thank the Bio knowledge Lab (BK-L) Ltd. for their kind support. An earlier version
of this article can be found on bioRxiv (doi: https://doi.org/10.1101/2023.05.04.539380).


                                                                                                                           Page 11 of 16
                                                                                                    F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




References

Arndt D, Grant JR, Marcu A, et al.: PHASTER: a better, faster version of the   Manni M, Berkeley MR, Seppey M, et al. : BUSCO Update: Novel and
PHAST phage search tool. Nucleic Acids Res. 2016; 44: W16–W21.                 Streamlined Workflows along with Broader and Deeper Phylogenetic
Publisher Full Text                                                            Coverage for Scoring of Eukaryotic, Prokaryotic, and Viral Genomes.
Banerjee MR, Yesmin L: Sulfur-oxidizing plant growth                           Mol. Biol. Evol. 2021; 38: 4647–4654.
promoting rhizobacteria for enhanced canola performance.                       PubMed Abstract|Publisher Full Text|Free Full Text
US Patent. 2008.                                                               Meier-Kolthoff JP, Auch AF, Klenk HP, et al.: Genome sequence-based
Brettin T, Davis JJ, Disz T, et al.: RASTtk: A modular and extensible          species delimitation with confidence intervals and improved distance
implementation of the RAST algorithm for building custom                       functions. BMC Bioinformatics. 2013; 14.
annotation pipelines and annotating batches of genomes. Sci. Rep.              PubMed Abstract|Publisher Full Text|Free Full Text
2015; 5.                                                                       Meier-Kolthoff JP, Carbasse JS, Peinado-Olarte RL, et al.: TYGS and LPSN: A
Publisher Full Text                                                            database tandem for fast and reliable genome-based classification
Camacho C, Coulouris G, Avagyan V, et al.: BLAST+: Architecture and            and nomenclature of prokaryotes. Nucleic Acids Res. 2022; 50:
applications. BMC Bioinformatics. 2009; 10.                                    D801–D807.
Publisher Full Text                                                            PubMed Abstract|Publisher Full Text|Free Full Text

Chaiboonchoe A, Dohai BS, Cai H, et al. : Microalgal metabolic network         Meier-Kolthoff JP, Göker M: TYGS is an automated high-throughput
model refinement through high-throughput functional metabolic                  platform for state-of-the-art genome-based taxonomy. Nat. Commun.
profiling. Front. Bioeng. Biotechnol. 2014; 2: 1–12.                           2019; 10: 2182.
PubMed Abstract|Publisher Full Text|Free Full Text                             PubMed Abstract|Publisher Full Text|Free Full Text

Chuanchuen R, Murata T, Gotoh N, et al. : Substrate-dependent                  Mora-Salguero D, Florez MJV, Orjuela JH, et al.: Evaluation of the phenol
utilization of OprM or OpmH by the Pseudomonas aeruginosa MexJK                degradation capacity of microalgae-bacteria consortia from the bay
efflux pump. Antimicrob. Agents Chemother. 2005; 49: 2133–2136.                of Cartagena, Colombia. TecnoLógicas. 2019; 22: 149–158.
PubMed Abstract|Publisher Full Text|Free Full Text                             Publisher Full Text

Fakhimi N, Torres MJ, Fernández E, et al.: Chlamydomonas reinhardtii and       Ondov BD, Treangen TJ, Melsted P, et al.: Mash: Fast genome and
Microbacterium forte sp. nov. a mutualistic association that favors            metagenome distance estimation using MinHash. Genome Biol. 2016;
sustainable hydrogen production. Sci. Total Environ. 2023a.                    17: 132.
Publisher Full Text                                                            PubMed Abstract|Publisher Full Text|Free Full Text

Fakhimi N, Dubini A, Gonzalez-Ballester D: Draft genome of                     Overbeek R, Olson R, Pusch GD, et al.: The SEED and the Rapid
Stenotrophomonas goyi sp. nov., a bacterium associated with                    Annotation of microbial genomes using Subsystems Technology
Chlamydomonas reinhartdii. [Dataset]. NCBI Gene. 2023b.                        (RAST). Nucleic Acids Res. 2014; 42: D206–D214.
Reference Source                                                               PubMed Abstract|Publisher Full Text|Free Full Text

Farris JS: Estimating Phylogenetic Trees from Distance Matrices. Am.           Pages D, Rose J, Conrod S, et al.: Heavy metal tolerance in
Nat. 1972; 106: 645–668.                                                       Stenotrophomonas maltophilia. PLoS One. 2008; 3: e1539.
Publisher Full Text                                                            PubMed Abstract|Publisher Full Text|Free Full Text

González-Ballester D, Dubini A, Fakhimi N, Torres MJ: Supplemental Files.      Park M, Kim C, Yang J, et al.: Isolation and characterization of
[Dataset]. Zenodo. 2023.                                                       diazotrophic growth promoting bacteria from rhizosphere of
Publisher Full Text                                                            agricultural crops of Korea. Microbiol. Res. 2005; 160: 127–133.
                                                                               PubMed Abstract|Publisher Full Text
Harris E: The Chlamydomonas Sourcebook: Introduction into
Chlamydomonas and its laboratory use. San Diego, CA: Elsevier Academic         Parte AC, Carbasse JS, Meier-Kolthoff JP, et al.: List of prokaryotic names
Press; 2008.                                                                   with standing in nomenclature (LPSN) moves to the DSMZ. Int. J. Syst.
                                                                               Evol. Microbiol. 2020; 70: 5607–5612.
Holland BR, Huber KT, Dress A, et al.: δ plots: A tool for analyzing           PubMed Abstract|Publisher Full Text|Free Full Text
phylogenetic distance data. Mol. Biol. Evol. 2002; 19: 2051–2059.
PubMed Abstract|Publisher Full Text                                            Rivas-Garcia T, Murillo-Amador B, Preciado-Rangel P, et al.: Debaryomyces
                                                                               hansenii, Stenotrophomonas rhizophila, and Ulvan as Biocontrol
Kanehisa M, Sato Y, Morishima K: BlastKOALA and GhostKOALA: KEGG               Agents of Fruit Rot Disease in Muskmelon (Cucumis melo L.). Plants.
Tools for Functional Characterization of Genome and Metagenome                 2022; 11.
Sequences. J. Mol. Biol. 2016; 428: 726–731.                                   PubMed Abstract|Publisher Full Text|Free Full Text
PubMed Abstract|Publisher Full Text
                                                                               Ryan RP, Monchy S, Cardinale M, et al.: The versatility and adaptation of
Koren S, Walenz BP, Berlin K, et al.: Canu: Scalable and accurate long-        bacteria from the genus Stenotrophomonas. Nat. Rev. Microbiol. 2009;
read assembly via adaptive κ-mer weighting and repeat separation.              7: 514–525.
Genome Res. 2017; 27: 722–736.                                                 Publisher Full Text
PubMed Abstract|Publisher Full Text|Free Full Text
                                                                               Suckstorff I, Berg G: Evidence for dose-dependent effects on plant
Kreft L, Botzki A, Coppens F, et al.: PhyD3: A phylogenetic tree viewer        growth by Stenotrophomonas strains from different origins. J. Appl.
with extended phyloXML support for functional genomics data                    Microbiol. 2003; 95: 656–663.
visualization. Bioinformatics. 2017; 33: 2946–2947.                            Publisher Full Text
PubMed Abstract|Publisher Full Text
                                                                               Torres MJ, González-Ballester D, Gómez-Osuna A, et al.: Chlamydomonas-
Lagesen K, Hallin P, Rødland EA, et al.: RNAmmer: Consistent and rapid         Methylobacterium oryzae cooperation leads to increased biomass,
annotation of ribosomal RNA genes. Nucleic Acids Res. 2007; 35:                nitrogen removal and hydrogen production. Bioresour. Technol. 2022;
3100–3108.                                                                     352: 127088.
PubMed Abstract|Publisher Full Text|Free Full Text                             PubMed Abstract|Publisher Full Text
Lee I, Chalita M, Ha SM, et al.: ContEst16S: An algorithm that identifies      Universidad de Cordoba: Stenotrophomonas sp. Spanish Type Culture
contaminated prokaryotic genomes using 16S RNA gene sequences.                 Collection (CECT). [Dataset]. 2022.
Int. J. Syst. Evol. Microbiol. 2017; 67: 2053–2057.                            Reference Source
Publisher Full Text
                                                                               Wei X, Lei S, Deng Y, et al.: Stenotrophomonas nematodicola sp. nov.,
Lefort V, Desper R, Gascuel O: FastME 2.0: A comprehensive, accurate,          isolated from Caenorhabditis elegans. Arch. Microbiol. 2021; 203:
and fast distance-based phylogeny inference program. Mol. Biol. Evol.          6197–6202.
2015; 32: 2798–2800.                                                           PubMed Abstract|Publisher Full Text
PubMed Abstract|Publisher Full Text|Free Full Text
                                                                               Wintermans JF, de Mots A: Spectrophotometric_characteristics_of_
Letunic I, Bork P: Interactive tree of life (iTOL) v5: An online tool for      chlorophylls_a_and_b_and_their_phenophytins_in_ethanol.pdf.
phylogenetic tree display and annotation. Nucleic Acids Res. 2021; 49:         Biochim. Biophys. Acta. 1965; 109: 448–453.
W293–W296.                                                                     Publisher Full Text
PubMed Abstract|Publisher Full Text|Free Full Text
                                                                               Wolf A, Fritze A, Hagemann M, et al.: Stenotrophomonas rhizophila
Liu Z, Yang C, Qiao C: Biodegradation of p-nitrophenol and                     sp. nov., a novel plant-associated bacterium with antifungal
4-chlorophenol by Stenotrophomonas sp. FEMS Microbiol. Lett. 2007;             properties. Int. J. Syst. Evol. Microbiol. 2002; 52: 1937–1944.
277: 150–156.                                                                  Publisher Full Text
Publisher Full Text




                                                                                                                                                        Page 12 of 16
                                                                       F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Open Peer Review
Current Peer Review Status:


 Version 2


 Reviewer Report 27 November 2023

https://doi.org/10.5256/f1000research.157820.r224973

 © 2023 Maroti G. This is an open access peer review report distributed under the terms of the Creative Commons
 Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the
 original work is properly cited.



       Gergely Maroti
       Institute of Plant Biology, Biological Research Centre, Szeged, Hungary

       The manuscript describes the characteristics of a novel Stenotrophomonas sp. bacterium isolated
       from a complex algal-bacterial association. The genome description is clear and concise, the
       nutrient requirements of the bacterium were also clearly determined.

       The mutualistic growth promoting effects were proven experimentally. The potential molecular
       mechanisms behind the observed effects are not shown or hypothesized, however, it is not the
       goal of this manuscript.

       The conclusions are correct, the application of multispecies consortia including bacteria and green
       algae is a promising way for biological hydrogen production in an economically viably manner.

       Is the work clearly and accurately presented and does it cite the current literature?
       Yes

       Is the study design appropriate and is the work technically sound?
       Yes

       Are sufficient details of methods and analysis provided to allow replication by others?
       Yes

       If applicable, is the statistical analysis and its interpretation appropriate?
       Yes

       Are all the source data underlying the results available to ensure full reproducibility?
       Yes

       Are the conclusions drawn adequately supported by the results?
       Yes



                                                                                                               Page 13 of 16
                                                                        F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




       Competing Interests: No competing interests were disclosed.

       Reviewer Expertise: Algal biotechnology

       I confirm that I have read this submission and believe that I have an appropriate level of
       expertise to confirm that it is of an acceptable scientific standard.


 Reviewer Report 27 November 2023

https://doi.org/10.5256/f1000research.157820.r224972

 © 2023 Leon-Bañares R. This is an open access peer review report distributed under the terms of the Creative
 Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium,
 provided the original work is properly cited.



       Rosa Leon-Bañares
       Laboratory of Biochemistry, Faculty of Experimental Sciences, Marine International Campus of
       Excellence and REMSMA, University of Huelva, Huelva, Andalusia, Spain

       The paper is clearly presented and describes an interesting study, which is detailed presented. In
       this paper, the authors describe the characterization of a new bacterial species of the genus
       Stenotrophomonas, found as contaminant in a culture of the chlorophyte Chlamydomonas
       reinhardtii. The bacterial genome has been sequenced and tentatively annotated. Phylogenetic
       trees based on both whole genome and 16S rDNA sequences were stablished. The growth of the
       new bacteria, either with or without the microalga, was evaluated.

       Functional annotation of the genome of the new bacteria reveled that some important pathways
       are not present in S. goyi genome. This data, beside several growth test carried out with
       aminoacids and /or peptide hydrolysates make the authors suggest that peptides and amino acids
       are a good C source, and probably also a good N or S source, for S. goyi, which can not grow in
       minimal medium not supplemented with aminoacids or peptides. Addition of aminoacid/peptides
       or co-cultivation with the microalga is necessary for the growth of this bacterial. Moreover, the
       microalga growth rate is practically doubled when cultured in the presence of the bacteria. The
       authors propose the establishment of a mutualistic relationship between C. reinhardtii and the
       bacteria, in which the bacteria would provide a carbon source (acetate or CO2 obtained from
       bacterial sugar fermentation) to the microalgae and the bacteria would obtain S-aminoacids
       excreted by the alga.

       The authors suggest that many microalgal-associated bacteria can promote higher plant growth,
       being the characterization of this algal-bacterial consortium of interest to identify potent plant
       growth-promoting bacteria.

       Suggestions:
           ○The assessment of the bacterial growth by determination of optical density is adequate for
            pure cultures, but it is difficult to carry out in mixed algal-bacterial cultures. The authors
            have optimized and validated a selective centrifugal sedimentation approach to separate
            bacteria and microalgae. Although the approach seems to work well, I would suggest


                                                                                                                Page 14 of 16
                                                                  F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




             determination of colony forming units (CFU) to follow bacterial growth in future occasions.
             In may experience, the sedimentation properties of the microalga can change along the
             growth cycle

         ○   Indicate in the legend of Figure 1, that shows a plate with Chlamydomonas reinhardtii and
             Stenotrophomonas goyi sp. nov., the culture medium used. Is it bacterial or algal growth
             médium? Is it MM or has been supplemented with sugars?

     Is the work clearly and accurately presented and does it cite the current literature?
     Yes

     Is the study design appropriate and is the work technically sound?
     Yes

     Are sufficient details of methods and analysis provided to allow replication by others?
     Yes

     If applicable, is the statistical analysis and its interpretation appropriate?
     Not applicable

     Are all the source data underlying the results available to ensure full reproducibility?
     Yes

     Are the conclusions drawn adequately supported by the results?
     Yes

     Competing Interests: No competing interests were disclosed.

     Reviewer Expertise: Biochemistry and Biotechnology of microalgae

     I confirm that I have read this submission and believe that I have an appropriate level of
     expertise to confirm that it is of an acceptable scientific standard.




Comments on this article
Version 2


 Author Response 01 Dec 2023
 David Gonzalez-Ballester

 The comment of Tiago Henriques is totally right. We will amend this error.
 Thanks Tiago for noticing.

 Competing Interests: No competing interests were disclosed.




                                                                                                          Page 15 of 16
                                                                  F1000Research 2023, 12:1373 Last updated: 29 JUL 2025




Reader Comment 22 Nov 2023
Tiago Henriques, University of Coimbra, Coimbra, Portugal

In the "Data availability" section, "NCBI Gene" has the accession number CP116871 which directs to
"Microbacterium sp. A(2022) strain A chromosome, complete genome". I think the accession
nummber that should be there is CP124620.

Competing Interests: No competing interests were disclosed.




The benefits of publishing with F1000Research:

• Your article is published within days, with no editorial bias

• You can publish traditional articles, null/negative results, case reports, data notes and more

• The peer review process is transparent and collaborative

• Your article is indexed in PubMed after passing peer review

• Dedicated customer support at every stage


For pre-submission enquiries, contact research@f1000.com




                                                                                                          Page 16 of 16
