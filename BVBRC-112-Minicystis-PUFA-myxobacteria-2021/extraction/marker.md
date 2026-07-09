<!-- BVBRC-112 — Marker-equivalent extraction of paper.pdf
  Source PDF: paper.pdf (sha256 9791ec6f1daba20bf838971089cea90ddf1e4ca74e53fb6877d5368ab9035d3c)
  DOI: 10.1186/s12864-021-07955-x  PMID: 34511070  PMCID: PMC8436480
  Paper: Pal S, Sharma G, Subramanian S. Complete genome sequence and identification of
         polyunsaturated fatty acid biosynthesis genes of the myxobacterium Minicystis rosea
         DSM 24000T. BMC Genomics 22:655 (2021).
  Extraction method: pdftotext -layout (poppler 22.x) — MARKER-EQUIVALENT FALLBACK.
    Central Eagle SCOUT Marker corpus not queried in this backfill pass (no sha256 in wave record).
    A cleaner XML-derived plaintext is available at work/paper_body.txt (30 KB, from PMC XML).
  Backfill: 2026-07-05 (Ollie / OpenClaw / Argo Opus 4.7).
-->

Pal et al. BMC Genomics      (2021) 22:655
https://doi.org/10.1186/s12864-021-07955-x




 RESEARCH                                                                                                                                           Open Access

Complete genome sequence and
identification of polyunsaturated fatty acid
biosynthesis genes of the myxobacterium
Minicystis rosea DSM 24000T
Shilpee Pal1†, Gaurav Sharma1,2† and Srikrishna Subramanian1*


  Abstract
  Background: Myxobacteria harbor numerous biosynthetic gene clusters that can produce a diverse range of
  secondary metabolites. Minicystis rosea DSM 24000T is a soil-dwelling myxobacterium belonging to the
  suborderSorangiineae and family Polyangiaceae and is known to produce various secondary metabolites as well as
  polyunsaturated fatty acids (PUFAs). Here, we use whole-genome sequencing to explore the diversity of
  biosynthetic gene clusters in M. rosea.
  Results: Using PacBio sequencing technology, we assembled the 16.04 Mbp complete genome of M. rosea DSM
  24000T, the largest bacterial genome sequenced to date. About 44% of its coding potential represents paralogous
  genes predominantly associated with signal transduction, transcriptional regulation, and protein folding. These
  genes are involved in various essential functions such as cellular organization, diverse niche adaptation, and
  bacterial cooperation, and enable social behavior like gliding motility, sporulation, and predation, typical of
  myxobacteria. A profusion of eukaryotic-like kinases (353) and an elevated ratio of phosphatases (8.2/1) in M. rosea
  as compared to other myxobacteria suggest gene duplication as one of the primary modes of genome expansion.
  About 7.7% of the genes are involved in the biosynthesis of a diverse array of secondary metabolites such as
  polyketides, terpenes, and bacteriocins. Phylogeny of the genes involved in PUFA biosynthesis (pfa) together with
  the conserved synteny of the complete pfa gene cluster suggests acquisition via horizontal gene transfer from
  Actinobacteria.
  Conclusion: Overall, this study describes the complete genome sequence of M. rosea, comparative genomic
  analysis to explore the putative reasons for its large genome size, and explores the secondary metabolite potential,
  including the biosynthesis of polyunsaturated fatty acids.
  Keywords: Myxobacteria, Whole-genome sequencing, Evolution, Secondary metabolites, Comparative genomics




* Correspondence: krishna@imtech.res.in
†
 Shilpee Pal and Gaurav Sharma contributed equally to this work.
1
 CSIR-Institute of Microbial Technology (CSIR-IMTECH), Chandigarh, India
Full list of author information is available at the end of the article

                                        © The Author(s). 2021 Open Access This article is licensed under a Creative Commons Attribution 4.0 International License,
                                        which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give
                                        appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if
                                        changes were made. The images or other third party material in this article are included in the article's Creative Commons
                                        licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons
                                        licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
                                        permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.
                                        The Creative Commons Public Domain Dedication waiver (http://creativecommons.org/publicdomain/zero/1.0/) applies to the
                                        data made available in this article, unless otherwise stated in a credit line to the data.
Pal et al. BMC Genomics   (2021) 22:655                                                                       Page 2 of 15




Background                                                    DHA, EPA as well as linolenic acid (LA), γ-linolenic acid
Myxobacteria are Gram-negative, rod-shaped, soil-             (GLA), stearidonic acid (SDA), and docosapentaenoic
dwelling δ-proteobacteria taxonomically classified within     acid (DPA) [18]. Unlike marine microorganisms, myxo-
the order Myxococcales and distributed across diverse         bacterial pfa gene clusters include only four genes i.e.,
ecological niches [1–3]. While the δ-proteobacteria are       pfa1 (homolog of pfaD), pfa2 (homolog of pfaA), pfa3
anaerobic sulfate or sulfur-reducing microbes, myxobac-       (homolog of pfaC), and a homolog of pfaE gene [18].
teria are aerobes except for the facultative anaerobe         These Pfa proteins contain various domains and catalytic
Anaeromyxobacter spp. and the strictly anaerobic Pajar-       sites such as Pfa1 (PfaD) in Aetherobacter contains enoyl
oellobacter spp. [4, 5]. Unlike their close δ-                reductase (ER) domain, multi-functional Pfa2 (PfaA)
proteobacteria relatives, they have large genomes (9–16       protein contains several domains, i.e. β-ketoacyl synthase
Mbp) with the exception of Anaeromyxobacter spp. (~ 5         (KS), malonyl/acyltransferase (MAT/AT), acyl carrier
Mbp), Vulgatibacter (4.35 Mbp), and Pajaroellobacter          protein (ACP), ketoreductase (KR) and PKS-like dehy-
(1.82 Mbp). Apart from cellular functions, most of the        dratase (PS-DH) domains; and Pfa3 (PfaC) has KS, chain
functionally annotated proteins are associated with sev-      length factor (CLF), acyltransferase (AT), Fab-A like
eral intriguing physiological characteristics such as glid-   dehydratase (DH), pseudo-domain dehydratase (DH’)
ing motility, predation, fruiting body formation, biofilm     and       1-acylglycerol-3-phosphate      O-acyltransferase
formation, social behavior, etc. [6–13]. Myxobacterial        (AGPAT) domain. In addition to these consecutive
vegetative cells can swarm by social and adventurous          genes, another gene pfaE encodes for 4′-phosphopan-
gliding in search of nutrients or for predating other mi-     tetheinyl transferase (PPTase) [25] and is located at a
crobes [3]. During starvation, myxobacterial cells (>105)     separate locus in Aetherobacter and S. cellulosum So
construct fruiting bodies which enclose myxospores that       ce56 genomes. These domains are not similarly distrib-
can initiate their vegetative cycle in favorable growth       uted in myxobacterial proteomes [18]. For example, the
conditions [14].                                              AT domain, seen in Pfa3 of Aetherobacter, is not present
  Myxobacteria are known for their vast biosynthetic po-      in S. cellulosum So ce56. Diversity of these domains have
tential, as evident by the secretion of a large variety of    been reported to cause product variations from pfa gene
bioactive molecules such as alkaloid, polyketide, terpene,    clusters of terrestrial myxobacteria [18].
aminocoumarin, beta-lactam, etc., produced from poly-            To characterize and explore the huge biosynthetic po-
ketide synthase (PKS), nonribosomal polypeptide synthe-       tential of myxobacteria, whole-genome sequencing of
tase (NRPS), and their hybrids [15, 16]. These                more strains is needed. Here we report the complete
compounds are known to have various antibiotic, anti-         genome sequence of M. rosea DSM 24000T and identify
fungal and antitumor activities [17]. Most of these stud-     several biosynthetic gene clusters including one involved
ied organisms belonging to Sorangium and                      in the synthesis of PUFA. We also perform comparative
Aetherobacter have been reported as potent producers of       genome analysis of M. rosea and other related myxobac-
polyunsaturated fatty acids (PUFAs), including eicosa-        teria to glean insights about the expansion in genome
pentaenoic acid (EPA) and docosahexaenoic acid (DHA)          size that makes the M. rosea DSM 24000T genome the
[18]. These n-3 (omega-3) and n-6 (omega-6) are associ-       largest bacterial genome known to date.
ated with blood-pressure-lowering properties and are
used for the treatment of cardiovascular diseases, dia-       Results and discussion
betes, and obesity [19]. Fish oils are well-known             Genomic properties of M. rosea DSM 24000T
eukaryotic sources of DHA and EPA [20] but might be           The M. rosea genome assembled into a complete circu-
contaminated with organic pollutants. Considering the         lar chromosome of length 16,040,666 bp with 69.07%
huge demand for PUFA due to its health benefits, alter-       GC. It has been deposited in GenBank under the acces-
nate PUFA synthesis via an anaerobic route integrated         sion number CP016211.1 within the BioProject number
with a polyketide synthase (PKS) instead of the fatty acid    PRJNA321464. The assembly process did not detect any
synthase (FAS) has been explored in prokaryotes [21,          plasmid sequence. This is not surprising as among the
22]. This pathway for PUFA synthesis employs pfa gene         genomes of order Myxococcales, only one organism M.
clusters containing a total of five consecutive genes         fulvus 124B02 has been reported to harbor a plasmid,
(pfaA, pfaB, pfaC, pfaD, and pfaE) in marine microor-         pMF1 [26]. However, as we have used Bluepippin size
ganisms such as S. pneumatophori SCRC-2738, M. mar-           selection in our sequencing, we might have missed any
ina MP-1, and P. profundum SS9 [22–24]. Recently,             smaller size plasmid. RAST-based annotation has pre-
these pfa gene clusters have also been explored in non-       dicted 14,121 genes that consist of 14,018 protein-
marine terrestrial myxobacteria Aetherobacter sp.             coding genes, 88 tRNAs, four 5S–16S-23S rRNA op-
SBSr008, Aetherobacter fasciculatus SBSr002, and S. cel-      erons, one transfer-messenger RNA, and two non-
lulosum So ce56 in producing arachidonic acid (ARA),          coding RNAs (each belongs to RNase_P_RNA and SRP_
Pal et al. BMC Genomics      (2021) 22:655                                                                           Page 3 of 15




Table 1 Assembly and annotation statistics for the complete           hypothetical proteins in M. rosea. Our pan-genome
genome sequence of M. rosea DSM 24000T                                studies with 19 other myxobacteria (having > 9 Mbp
Organism name                          Minicystis rosea DSM 24000 T   genome size) revealed vast diversity among all studied
Sequencing data                        PacBio P6C4 chemistry          members.
Total reads                            4,41,539
                                                                      Core genome
Total bases                            3,48,84,02,643 bp
                                                                      Our study suggested that 650 orthologous protein-
Average read length                    7,900 bp
                                                                      coding genes are conserved and constitute the core gen-
Average reference coverage             217X                           ome. This category includes only 5.03% of M. rosea pro-
Bio-project number                     PRJNA321464                    teins in contrast with its vast gene content (Table S2a).
NCBI Accession number                  CP016211.1                     COG-based functional characterization of core proteins
Genome size                            16,040,666 bp                  in M. rosea reveals that ‘Metabolism’ [MET] (44.14%)
                                                                      representation is higher than ‘Information Storage and
GC content                             69.07%
                                                                      Processing’ [ISP] (28.76%) and ‘Cellular Processes and
Chromosome                             1
                                                                      Signaling’ [CPS] (27.70%). Most of the core proteins in
CDS                                    14,018                         M. rosea are involved in translation [J] (16.59%), coen-
Coding density                         87.31%                         zyme metabolism [H] (8.68%), lipid metabolism [I]
CDS from (+) strand                    6,983                          (8.07%), energy production [C] (7%), post-translational
CDS from (−) strand                    7,035                          modification [O] (6.85%), amino acid transport [E]
                                                                      (6.39%), transcription [K] (6.24%), cell wall biogenesis
tRNA                                   88
                                                                      [M] (5.78%), replication [L] (5.78%), nucleotide metabol-
5S–16S-23S rRNA                        4
                                                                      ism [F] (5.33%), and signal transduction [T] (5.02%) (Fig.
tmRNA                                  1                              S2).
ncRNA                                  2
Max. CDS length                        22,116 bp                      Accessory genome
Mean CDS length                        1,003 bp                       This study identified a total of 8947 (63.83%) accessory
                                                                      genes in M. rosea (Fig. 3), which are associated with the
Genes containing Pfam domains          7,844 (55.96%)
                                                                      COG category CPS in higher number (39.29%) as com-
Genes with COG identified              6,275 (44.76%)
                                                                      pared to the MET (36.86%) and ISP (16.74%) categories.
Hypothetical proteins                  5,503 (39.26%)                 Most of the accessory proteins are involved in signal
                                                                      transduction [T] (17.02%), transcription [K] (10.57%),
RNA class) (Table 1). As of date, the genome sequence                 cell wall biogenesis [M] (7.33%), lipid metabolism [I]
of M. rosea is the largest amongst kingdom bacteria                   (6.56%), amino acid transport [E] (5.67%), energy pro-
(Fig. 1), and is ~ 1.26 Mbp larger than the genome of the             duction [C] (5.33%), and secondary metabolites biosyn-
myxobacteria S. cellulosum So0157–2 (14,782,125 bp),                  thesis [Q] (5.19%) (Fig. S2).
which has been previously reported as the largest pro-
karyotic genome [27].                                                 Unique genome
  16S rRNA-based phylogenetic tree indicates that M.                  A total of 4421 (31.54%) proteins do not display any sig-
rosea DSM 24000T is a close relative of members of the                nificant identity with selected myxobacteria, which are
family Polyangiaceae in suborder Sorangiineae (Fig. 2).               mentioned as unique proteins in M. rosea (Table S2a).
Similar tree topology has also been observed in the                   Among them, only 347 unique proteins have been func-
marker-gene-based tree where M. rosea is closely clus-                tionally identified which are associated with the COG
tered with selected species of the genera within the Poly-            category CPS (34%) followed by MET (30.25%) and ISP
angiaceae family (Fig. S1). Moreover, M. rosea also                   (13.83%). Majority of unique known proteins are in-
shows higher DDH and ANI values with the Sorangium                    volved in signal transduction [T] (12.68%), transcription
spp. as compared to other myxobacteria (Table S1) sug-                [K] (10.29%), cell wall biogenesis [M] (9.80%), lipid me-
gesting their close relatedness.                                      tabolism [I] (5.76%), secondary metabolites biosynthesis
                                                                      [Q] (5.19%), coenzyme metabolism [H] (4.61%), and
Analysis of genome expansion and protein function in M.               post-translational modification [O] (4.32%) (Fig. S2).
rosea DSM 24000T                                                      Among unique proteins in M. rosea, 125 proteins exhibit
M. rosea encodes 14,018 protein-coding sequences                      significant similarity with exogenous genetic materials,
which account for 87.50% coding density with an aver-                 including integrated plasmids, phages, and insertion se-
age gene size of 1003 bp (Table 1). A total of 6,167 (~               quence (IS) elements (Table S2a). Twenty-four genomic
44%) coding sequences have been annotated as                          islands (GIs) have been identified in M. rosea comprising
Pal et al. BMC Genomics     (2021) 22:655                                                                                         Page 4 of 15




 Fig. 1 Circular representation of the genome of M. rosea DSM 24000T showing GC skew, GC content, genes on leading and lagging strands, core
 genes, duplicate genes, unique genes, unique exogenous genes, secondary metabolites producing genes (BGCs), and eukaryotic-like kinase (ELK)
 synthesizing genes from inner to outer layers respectively


a total of 6,15,248 bp (3.84%) of the genome (Table S2b).                genome size [29]. Earlier, a linear relationship has been
The GIs containing unique exogenous genes (Table S2b)                    observed between the signaling proteins, including two-
may help facilitate horizontal gene transfer [28].                       component system (TCS) proteins, and genome size in
                                                                         host-associated, as well as, environmental bacteria [30].
Signal transduction                                                      M. rosea also shows a higher number (323 proteins) of
Overall, our genome analysis indicates an abundance of                   TCS proteins, which comprise 145 orphan histidine ki-
signal transduction proteins as well as transcriptional                  nases (HK), 125 orphan response regulators (RR), and 53
regulators in M. rosea. Our analysis is supported by pre-                hybrid TCS proteins as compared to S. cellulosum
vious studies reporting a strong correlation between the                 So0157–2 (309 TCS proteins) as well as other Soran-
number of bacterial transcriptional regulators and                       gium spp. (Fig. 4A). However, no strong correlation (r =
Pal et al. BMC Genomics     (2021) 22:655                                                                                          Page 5 of 15




 Fig. 2 16S rRNA-based phylogenetic tree shows a close association of M. rosea with the members of the family Polyangiaceae in suborder
 Sorangiineae. The left and right stripes represent the suborder and family-level taxonomy (color-coded), respectively
Pal et al. BMC Genomics       (2021) 22:655                                                                                                  Page 6 of 15




 Fig. 3 Flower plot representing the total (outermost layer), unique (second layer) (strain specific), accessory (third layer), and core proteins (center
 of the plot) in M. rosea and other 19 myxobacteria


0.531, p < 0.05) between the genome size and the num-                          number of ELKs increases with increasing genome size
ber of TCS proteins has been found in myxobacteria, as                         in bacteria [34]. A significant strong positive correlation
reported previously [9]. Apart from the environmental                          between genome size and number of ELKs (r = 0.859,
diversity, the complex life cycle also influences the num-                     p < 0.001) is seen. In contrast to ELKs, M. rosea has
bers of TCS proteins in the case of myxobacteria [31]. In                      fewer protein phosphatases (PPs) (43 genes), comprising
addition to the TCS system, signal transduction mecha-                         all three major families of PPs i.e., serine/threonine PPs
nisms are also facilitated by serine, threonine, and tyro-                     (PPP-family = 9 genes), metal-dependent serine/threo-
sine phosphorylation mediated protein kinases in                               nine PPs (PPM-family) including PP2c-type (21 genes)
prokaryotes. This protein family in myxobacteria has                           and SpoIIE-like PPs (5 genes), and tyrosine-specific PPs
been reported to have strong sequence similarity with                          (PTP-family) including dual-specificity PTPs (5 genes),
eukaryotic-like kinases (ELKs) [32]. M. rosea contains                         low molecular weight protein PTPs (2 genes) and PTPZ-
353 ELKs, which is higher than S. cellulosum So ce56                           like PTPs (1 gene). In response to the peripheral stimuli,
(317) [33], as well as other myxobacteria (Fig. 4B). The                       protein kinases phosphorylate the target proteins,
Pal et al. BMC Genomics      (2021) 22:655                                                                                              Page 7 of 15




 Fig. 4 Bar plot representations of two-component system (TCS) categories [histidine kinase, response regulator, and hybrid TCS] (A), eukaryotic-
 like kinases (ELKs) (B), and secretome (C) in myxobacteria along with their genome size
Pal et al. BMC Genomics   (2021) 22:655                                                                         Page 8 of 15




whereas, phosphatases deactivate them by removing the          [44]. Moreover, a higher number of lipid metabolism [I]
phosphate groups [35]. Thus, kinase/phosphatase ratio          associated proteins than carbohydrate metabolism [G]
regulates the bacterial cell differentiation and develop-      reveals efficient utilization of lipid as an energy source in
ment to quickly adapt to the persistently varying envir-       M. rosea similar to that observed in M. xanthus [45].
onment [36]. It has also been reported that PP2c-type          Lipids have been observed in producing diverse morpho-
PPs can compete with ELKs in bacteria [37]. However, a         logical characters such as fruiting body formation in
higher number of PP2c-type PPs has been observed in            myxobacteria upon amino acid and carbon depletion
M. rosea (21 genes) than A. dehalogenans (2 genes), M.         [46]. Steroid biosynthesis in M. rosea further explores
xanthus (4 genes), and S. cellulosum So ce56 (16 genes),       the importance of lipid bodies as signaling molecules
reported as the highest PP2c-type PPs containing               similar to the steroid hormones in animals [47]. Thus,
prokaryote [38]. Moreover, an elevated ratio of ELKs/          sophisticated intercellular communication for niche
PPs has been also observed in M. rosea (8.2/1), as in A.       adaptation and morphogenetic variations may facilitate
dehalogenans (1.7/1), M. xanthus (6.9/1), and S. cellulo-      the retention of a huge amount of protein-coding genes
sum So ce56 (7.7/1) [38]. It could explain the phosphor-       in M. rosea.
ylation events which cannot be reversed by PPs during
multicellular development in myxobacteria [38]. We             Duplication events
identified 90 ELK proteins as being involved in the fruit-     Paralogous genes, which arise by gene duplications,
ing body production in M. rosea by BLASTP search               comprise 44.10% genes in M. rosea (Table S2a). Using
(length ≥ 50% and e-value ≤1e-10) against the fruiting         the same parameters to define paralogous genes, we find
body forming proteins of M. xanthus [39] and HMM-              that well-studied members of the family Polyangiaceae
profile based searches [40]. However, crucial genes for        i.e., S. cellulosum So ce56 and S. cellulosum So0157–2
fruiting body development (actA, asgA, csgA, fruA, and         contain 47.10 and 41.80% paralogous genes, respectively.
sdeK) identified in M. xanthus are absent in M. rosea          Our results are in agreement with previous reports sug-
and in S. cellulosum So ce56 [33]. Therefore, as sug-          gesting that the extensive expansion of paralogous genes
gested in earlier studies [41], it can be argued that an al-   account for the large genome size [48], similar to that
ternative mechanism for fruiting body development may          reported in S. cellulosum So ce56 [33] and S. cellulosum
exist in M. rosea [42].                                        So0157–2 [27]. Most of the functionally annotated par-
                                                               alogous proteins are involved in signal transduction [T]
Secretome analysis                                             (21.41%), transcription [K] (12.04%), cell wall biogenesis
Our analysis revealed that 3035 proteins constitute the        [M] (8.08%), lipid metabolism [I] (7.30%), post-
secretome in M. rosea, which is higher as compared to          translational modification [O] (6.89%), and biosynthesis
other myxobacteria (Fig. 4C). Significant positive correl-     of secondary metabolites [Q] (5.47%) in M. rosea. Thus,
ation is seen between genome size and the number of            the majority of gene duplications have occurred for
secretome proteins (r = 0.845, p < 0.001). KEGG pathway        those proteins in M. rosea that may help it to respond to
analysis [43] has also revealed a higher number of pro-        the environmental signals and in regulatory mechanisms
teins (104 proteins) are involved in the secretion system      for niche adaptation.
in M. rosea (KEGG pathway ID - mrm03070) as com-
pared to A. dehalogenans 2CP-1 (47 proteins), C. fuscus        Pfam-based functional characterization
DSM 2262 (60 proteins), A. gephyra DSM 2261T (58               Using HMM profile-based searches, we identified that
proteins), M. hansupus (53 proteins), L. luteola DSM           7446 M. rosea proteins were mapped to 2576 Pfam fam-
27648T (35 proteins), S. amylolyticus DSM 53668T (44           ilies. Comparative analysis of protein families reveals
proteins), S. cellulosum So ce56 (67 proteins), S. cellulo-    that several families such as protein kinase (360 mem-
sum So0157–2 (64 proteins), and V. incomptus DSM               bers); histidine kinase (344 members); helix-turn-helix
27710T (27 proteins). An extensive secretion system may        (315 members), TetR (139 members), transcription regu-
explain the selection of such a large number of associ-        lators like σ54 (104 members); repeats such as tetratrico-
ated genes in M. rosea for executing sophisticated cellu-      peptide repeats (134 members), pentapeptide repeats
lar crosstalk and adaptation to diverse environments.          (107 members), VCBS (91 members), Sel1 (16 mem-
  A variety of regulatory systems are broadly distributed      bers); phage_GPD (71 members); FGE-sulfatase (69
across the M. rosea proteome, with most of them in-            members); short-chain dehydrogenase (115 members);
volved in transcription regulation. Free-living and soil-      and radical SAM (70 members) are overrepresented in
dwelling large-genome-containing bacteria usually ac-          M. rosea as compared to other Sorangiineae members
quire a complex regulatory network and a higher num-           (C. apiculatus, L. luteola, Polyangium spp., S. amylolyti-
ber of corresponding genes to survive in environments          cus, and S. cellulosum) (Table S2c). These families are
where the resources for growth are scarce but diverse          associated with signaling systems, regulatory networks,
Pal et al. BMC Genomics   (2021) 22:655                                                                         Page 9 of 15




protein folding, and genome packaging in M. rosea.            several domains such as KS, chain length factor (CLF),
Apart from these, some families such as, abhydrolase_7,       acyltransferase (AT), Fab-A-like dehydratase (DH),
aerolysin, bile_hydr_trans, creD, disintegrin, endonucle-     pseudo-domain dehydratase (DH’), and 1-acylglycerol-3-
ase_1, endotoxin_N, expansin_C, gluconate_2-dh3, gly_         phosphate O-acyltransferase (AGPAT) (Fig. 5AI) as de-
transf_sug, glyco_hydro, lectin_legB, lipase_bact_N, lipo-    tected in Aetherobacter spp. (Fig. 5AII). A close phylo-
calin, peptidase_C2, TPP_enzyme_M_2, etc. are exclu-          genetic relationship is also present between the Pfa3
sively identified in M. rosea (Table S2c). Complex            protein of M. rosea and Aetherobacter spp. (Fig. 5BIII).
lifestyles in diverse environments might facilitate gene      The KS domain catalyzes condensation reaction for fatty
gain, loss, or duplication in microbes for adaptation to      acid chain elongation [52], whereas CLF controls the
that niche [49]. The retention/modification of duplicated     fatty acid chain length [53]. MAT/AT acts as a chain ex-
genes helps to conserve the protein functions amongst         tender by selecting and transferring malonic esters with
different environments [50], which could be one of the        the help of ACP. Other enzymes like KR, DH, and ER
predominant causes for the large genome size in M.            introduce structural diversity in the fatty acid chain.
rosea.                                                        They act as tailoring enzymes that reduce intermediate
                                                              keto groups, thus modifying the nascent fatty acid chain
Biosynthetic gene clusters in M. rosea DSM 24000T             [54]. The integration of AGPAT domain into Pfa3 pro-
especially polyunsaturated fatty acid (PUFA) biosynthetic     tein has been reported as a unique feature of the terres-
genes                                                         trial myxobacterial PUFA synthases, which catalyzes acyl
Genome mining revealed 47 BGCs (encoded by 1081               group’s transfer to generate phosphatidic acid in the
genes) comprising 7.71% of protein-coding genes in M.         chain-terminating step of PUFA synthesis [55]. Post-
rosea. The major fraction of biosynthetic genes encode        translational modification of ACP occurs by the phos-
NRPS (252 genes; 7 clusters) followed by terpene (171         phopantetheinylation that converts apo-ACP to an active
genes; 9 clusters), PKS (128 genes; 4 clusters), ribosomal    holo form by 4′-phosphopantetheinyl transferase
synthesized and post-translationally modified peptide         (PPTase) [25]. PPTase domain has been observed in
(RiPP) (75 genes; 7 clusters), arylpolyene (75 genes; 2       PfaE protein [A7982_13498] which is located at a separ-
clusters), lanthipeptide (73 genes; 3 clusters), RRE-         ate locus of M. rosea proteome (Fig. 5AI) as observed in
containing (70 genes; 4 clusters), indole (56 genes; 3        other myxobacteria like Aetherobacter (Fig. 5AII) and
clusters), and NRPS-PKS hybrid (30 genes; 1 cluster).         Sorangium (Fig. 5AIII) [18].
Other clusters such as phosphonate (1 cluster; 38 genes),       The acyltransferase (AT) domain is distinctly encoded
thioamitide (2 clusters; 32 genes), thiopeptide (1 cluster;   by PfaB in marine γ-proteobacteria such as S. pneumato-
30 genes), phenazine (1 cluster; 20 genes), LAP (1 clus-      phori SCRC-2738, P. profundum SS9 [22, 23], and M.
ter; 18 genes), and siderophore (1 cluster; 13 genes) are     marina MP-1 [24]. Whereas, AT domain is integrated
also detected in the M. rosea genome. The representa-         into the carboxy-terminus of pfa3 in M. rosea (Fig. 5AI)
tion of BGC genes in the M. rosea genome is more than         as observed in terrestrial myxobacteria Aetherobacter
the average bacterial genome (3.7%) and is similar to or-     (Fig. 5AII) [18]. The domain shows 65.26% and 64.91%
ganisms from the genus Streptomyces, Myxococcus, Sor-         identities with the AT domains of pfa3 proteins in Aether-
angium, and Burkholderia [51].                                obacter fasciculatus and Aetherobacter sp. SBSr008, re-
  Further analysis of PKSs in M. rosea DSM 24000T re-         spectively. It plays a significant role in shaping the final
veals the pfa gene cluster comprises four genes (pfa1,        PUFA products synthesized from the PUFA gene cluster.
pfa2, pfa3, and pfaE) (Fig. 5) as observed in Aetherobac-     However, the AT domain is not present in pfa3 of Soran-
ter and Sorangium [18]. Domain analysis of the respect-       gium (Fig. 5AIII), which has been suggested as the reason
ive proteins shows that Pfa1 (PfaD) [A7982_11504]             for the inability of Sorangium to produce DHA and EPA
contains a nitronate monooxygenase domain of enoyl re-        [18]. Overall, homology studies suggest that the PUFA
ductase (ER) (Fig. 5AI). Sequence similarity and domain       clusters in M. rosea and Aetherobacter are unique
conservation of Pfa1 are seen between M. rosea and            amongst myxobacteria, containing all ten enzyme domains
Aetherobacter spp. (Fig. 5BI). Several functional do-         to yield PUFAs [56] including ARA, DHA, EPA as well as
mains, i.e., β-ketoacyl synthase (KS), malonyl/acyltrans-     LA, GLA, SDA, and DPA. The fully functional PUFA syn-
ferase (MAT/AT), acyl carrier protein (ACP),                  thase in M. rosea enables it to produce approximately 30%
ketoreductase (KR), and PKS-like dehydratase (PS-DH)          of the total cellular fatty acids [57]. Overall, the phylogeny
are positioned similarly in Pfa2 of M. rosea [A7982_          of each gene (Fig. 5B) within the PUFA cluster reveal that
11505] and Aetherobacter spp. (Fig. 5AI). The Pfa2            these PUFA genes are evolutionarily closely related to
protein-based phylogenetic tree also reveals close re-        Actinobacteria, suggesting that M. rosea might have ac-
latedness between Aetherobacter spp. and M. rosea             quired these genes from Streptomyces species via horizon-
(Fig. 5BII). Pfa3 in M. rosea [A7982_11506] comprises         tal gene transfer.
Pal et al. BMC Genomics     (2021) 22:655   Page 10 of 15




         A




         B




         C




 Fig. 5 (See legend on next page.)
Pal et al. BMC Genomics     (2021) 22:655                                                                                            Page 11 of 15




 (See figure on previous page.)
 Fig. 5 PUFA biosynthetic gene cluster organization, their phylogeny, and synteny analysis: A PUFA biosynthetic gene clusters and their respective
 domains in M. rosea DSM 24000T (I), Aetherobacter sp. SBSr008 (II), and S. cellulosum So ce56 (III). B Maximum likelihood-based phylogenetic
 analysis shows close relatedness of the M. rosea DSM 24000T PUFA biosynthetic proteins: Pfa1 [A7982_11504/APR86155.1] (I), Pfa2 [A7982_11505/
 APR86156.1] (II), and Pfa3 [A7982_11506/APR86157.1] (III) in members belonging to the genus Aetherobacter, Sorangium, Streptomyces, Azospirillum,
 Tahibacter, etc. C Synteny analysis of pfa gene cluster in M. rosea DSM 24000T with the close relatives belonging to the genus Aetherobacter,
 Sorangium, Streptomyces, Azospirillum, Tahibacter, etc.


   To further confirm how this cluster evolved within M.                   might be facilitated via gene-duplication followed by
rosea, we also performed synteny studies based on iden-                    functional diversification of these proteins. A vast num-
tified homologs across close relatives. We identified that                 ber of biosynthetic genes (7.71% of the coding potential)
the pfa gene cluster in M. rosea along with close rela-                    reveals the diversity of secondary metabolites production
tives Aetherobacter and Sorangium is completely con-                       in M. rosea. Our study has identified the previously
served with the PUFA synthetic gene cluster in several                     known functional PUFA biosynthetic gene cluster in the
Streptomyces spp., Azospirillum melinis, Tahibacter                        genome, one of the few known prokaryotic sources of
aquaticus, etc. (Fig. 5C). Conclusively, based on our                      DHA, EPA, LA, GLA, SDA, and DPA. Additionally,
phylogenetic and synteny analysis, we speculate that the                   based on our phylogenetic and synteny studies, we
pfa gene cluster might have been horizontally trans-                       hypothesize that this cluster might have been horizon-
ferred to M. rosea and closely related myxobacteria i.e.,                  tally transferred from Actinobacteria. Our study on the
Aetherobacter and Sorangium from Actinobacteria.                           genome sequencing, functional characterization, and pfa
                                                                           gene cluster analysis of M. rosea could further help bio-
Conclusions                                                                technological areas for heterologous expression of
Myxobacteria are well known for their large genome size                    PUFAs from prokaryotes.
and genomic content, as well as the potential to produce
a wide range of secondary metabolites, including polyun-                   Materials and methods
saturated fatty acids. Although there has been a huge                      Bacterial culture and isolation of genomic DNA
surge in next-generation sequencing of microbes in the                     The actively growing plate culture of M. rosea was pro-
last three decades, however, in comparison to other soil                   cured from Deutsche Sammlung von Mikroorganismen
bacteria, only a few whole-genome sequences of myxo-                       und Zellkulturen (DSMZ) as strain number DSM
bacteria are available. In the present work, we have se-                   24000T (also known as strain SBNa008 or NCCB
quenced, assembled, and annotated a 16.04 Mbp circular                     100349). The colonies from the procured sample were
genome of M. rosea DSM 24000T, the largest bacterial                       subcultured on VY/2 agar (DSMZ Medium 9) plates.
genome sequenced to date along with its genome                             These actively growing subculture plates were used to
characterization, and further emphasized the putative                      isolate whole genomic DNA using Zymogen Research
reasons for its genome expansion. Phylogenetic analysis                    Bacterial/fungal DNA isolation kit and Phenol-
and genome-genome distance calculation suggest M.                          Chloroform-Isoamyl alcohol (PCI) methods. The quan-
rosea to be a close relative of the members of suborder                    tity and quality of the extracted DNA were confirmed by
Sorangiineae in the family Polyangiaceae. Due to its                       gel electrophoresis and Nanodrop and supported by
complex social behavior, diverse niche adaptation, and                     Qubit quantification.
large genome size, M. rosea encodes a plethora of genes.
Analysis of protein families reveals that most of the                      Genome sequencing and assembly of M. rosea DSM
functionally identified proteins are associated with regu-                 24000T
latory functions, protein folding, and genome packaging.                   Isolated high-quality DNA was used for whole-genome
Overrepresentation of protein families such as protein                     sequencing (WGS) on a Pacific Biosciences RSII instru-
kinase, histidine kinase, tetR, transcription regulators                   ment available at the McGill University and Genome
like σ54, tetratricopeptide and pentapeptide repeats,                      Quebec Innovation Center, Montreal (Quebec), Canada.
VCBS, sel1, phage_GPD, FGE-sulfatase, short-chain de-                      SMRTbell long library was created with 10 mg whole
hydrogenase, and radical SAM, as well as higher num-                       genomic DNA using a 20-kb template preparation
bers of secretomes and eukaryotic-like kinases in M.                       method using Procedure and Checklist-20 kb Template
rosea as compared to other myxobacteria, are important                     Preparation using BluePippin™ Size Selection (https://
explanations for genome expansion. Therefore, the                          www.pacb.com/wp-content/uploads/Procedure-
requisite of adaptation in varied niches and complex                       Checklist-Preparing-gDNA-Libraries-Using-the-
myxobacterial multicellular behavior could be the driv-                    SMRTbell-Express-Template-Preparation-Kit-2.0.pdf;
ing forces behind genome expansion in M. rosea, which                      last accessed: 3 Sep 2021). Later the library was loaded
Pal et al. BMC Genomics   (2021) 22:655                                                                    Page 12 of 15




onto three single molecules real-time (SMRT) cells and        smaller genome size, 19 myxobacterial representatives
sequenced using P6 polymerase and C4 chemistry                from three suborders of the order Myxococcales, i.e. Sor-
(P6C4) with 180-min movie time. PacBio sequencing             angiineae (C. apiculatus DSM 436, P. fumosum, Polyan-
generated 4,41,539 raw reads (3,48,84,02,643 bp) with an      gium sp. SDU3–1, S. cellulosum So ce26, S. cellulosum
average read length of 7900 bp. The Hierarchical Gen-         So ce56, S. cellulosum So ce836, S. cellulosum So
ome Assembly Process (HGAP) Pipeline v. SMRT v2.3.0           ceGT47, S. cellulosum So0003–19-2, S. cellulosum
and consensus polishing with Quiver [58] were used to         So0007–03, S. cellulosum So0008–312, S. cellulosum
generate de novo assembly using default parameters.           So0157–2, S. cellulosum So0163, Labilithrix luteola
Gene prediction and functional annotation were per-           DSM 27648T, S. amylolyticus DSM 53668T) [33], Cysto-
formed by Rapid Annotation using Subsystem Technol-           bacterineae(A. gephyra DSM 2261T, C. fuscus DSM
ogy (RAST) [59], whereas rRNA and tRNA genes were             52655, H. minutum DSM 14724T, Myxococcus hansu-
predicted using RNAmmer 1.2 [60] and tRNAscan-SE-             pus), and Nannocystineae (E. salina DSM 1520) [9, 70–
1.23 [61]. RNAz 2.0 tool [62] was used to identify struc-     72] were selected to perform pangenome analysis via
tured non-coding RNA (P > 0.85). A circular plot for M.       identifying homologous and orthologous proteins using
rosea DSM 24000T genome was drawn using BRIG (v               Proteinortho (v6) (https://www.bioinf.uni-leipzig.de/
0.95-dev.0004) [63].                                          Software/proteinortho/) [73]. Paralogous proteins in M.
                                                              rosea were identified by all-against-all BLAST analysis
Phylogenetic analysis and estimation of DNA-DNA               (identity ≥30% and e-value ≤1e-10) of proteomes in M.
hybridization and average nucleotide identity                 rosea DSM 24000T using NCBI Blast+ 2.10.1 package
The 16S rRNA sequences reported for the members of            [74]. Exogenous genetic materials in M. rosea DSM
all three myxobacteria suborders i.e., Cystobacterineae,      24000T were identified by performing BLASTP (e-value
Nannocystineae, and Sorangiineae were retrieved from          ≤1e-30) against the dataset of plasmids, phages, and in-
the NCBI database. 16S rRNA sequences from all myxo-          sertion sequence (IS) elements retrieved from the ACLA
bacteria and an outgroup D. retbaense DSM 5692 were           ME database (http://aclame.ulb.ac.be/). Genomic islands
aligned using ClustalW [64]. The alignment was used to        in the M. rosea genome were identified using Island-
generate a phylogenetic tree using the GTR-GAMMA              Viewer 4 [75].
model [bootstrap: 100] of maximum likelihood (ML)
method in the RAxML (v8) tool [65] and visualized by          Protein domains and functional analysis
iTOL [66]. We also performed phylogenetic analysis of         Functional family and domains in all selected members
myxobacteria using 40 universal single-copy genes (gtp1,      of Sorangiineae were identified by scanning the Pfam-A
pheS, argS, rpsL, rpsG, rpsB, rplK, rplA, rplC, rplD, rplB,   database (v32.0) [76] using the hmmscan program (e-
rplY, rpsC, rplN, rplE, rpsH, rplF, rpsE, rpsM, rpsK, rplM,   value ≤1e-5) of HMMER (http://hmmer.janelia.org/)
rpsI, hisS, serS, rpsO, rpsS, rpsQ, rplP, rplO, cysS, rplR,   [77]. Representative domains of two-component system
leuS, rpsD, valS, tsaD, rpoB, rpoA, secY, ffh, and ftsY)      (TCS) such as, HisKA (PF00512), Hpt (PF01627), HAT-
which were identified as marker genes (MGs) using             Pase_c (PF02518), His_kinase (PF06580), HWE_HK
fetchMGs tool (http://motu-tool.org/fetchMG.html)             (PF07536), HisKA_2 (PF07568), HisKA_3 (PF07730),
[67]. Nucleotide sequences of these marker genes were         HATPase_c_2 (PF13581) and Response_reg (PF00072)
retrieved from each genome, aligned using ClustalW,           were identified. Eukaryotic like kinases (Elks): Pkinase
and further concatenated. The tree was generated using        (PF00069), Pkinase_C (PF00433) and Pkinase_Tyr
the GTR-GAMMA model of the ML method [bootstrap:              (PF07714); and protein phosphatases (PPs): PP2C_2
100] in RAxML (v8) tool and visualized by iTOL.               (PF13672, COG0631), SpoIIE (PF07228, COG2208),
  In silico DNA-DNA hybridization (DDH) and Average           PPPs (PF00149, COG0639) DSPc (PF00782, COG2365)
Nucleotide Identity (ANI) were calculated between M.          and LMWPc (PF01451, COG0394, COG2453), and
rosea DSM 24000T and other 21 selected members (all           PTPZ      (COG4464)      were     explored.   Functional
representative genomes from suborder Sorangiineae and         categorization of M. rosea proteins was performed by es-
a few representative genomes from other families in           timating their Clusters of Orthologous Groups (COGs)
order Myxoccales) using Genome-to-Genome Distance             [78] using the NCBI COG database [79]. The aforemen-
Calculator (GGDC) server [68] and ANI Calculator [69]         tioned gene clusters were grouped into various COG
respectively.                                                 categories such as ‘Cellular processes and Signaling’
                                                              [CPS], ‘Information Storage and Processing’ [ISP], ‘Me-
Working data, functional characterization, and estimation     tabolism’ [MET], and ‘Poorly Characterized’ [PC] [80].
of orthologous genes                                          SignalP (v5.0) [81], PRED-TAT [http://www.compgen.
As two [Vulgatibacter incomptus, Pajaroellobacter abor-       org/tools/PREDTAT] and PRED-LIPO [http://www.
tibovis EBA] out of 21 selected genomes have relatively       compgen.org/tools/PRED-LIPO] were used to identify
Pal et al. BMC Genomics         (2021) 22:655                                                                                                   Page 13 of 15




the secretome via signal peptide detection. Screened                            Acknowledgments
secretory protein sequences were used as queries on the                         We thank Dr. Ramya TNC for providing us workplace to purify the genomic
                                                                                DNA and for proofreading the manuscript.
TMHMM server, and protein sequences with 0–2 trans-
membrane domains were considered as final secretomes                            Authors’ contributions
[82].                                                                           SP analyzed, investigated, validate, and prepared the manuscript; GS
                                                                                conceptualized, analyzed, investigated, supervised, reviewed, and edited the
                                                                                manuscript; SS: the project administrator, conceptualized, supervised,
Estimation of biosynthetic gene clusters in M. rosea DSM                        reviewed, and edited the manuscript. All authors have approved the final
24000T                                                                          version of the manuscript.
Prediction of BGCs in M. rosea was performed using the
                                                                                Funding
antiSMASH tool (v5.0) (https://antismash.                                       S.P. would like to thank the Science and Engineering Research Board,
secondarymetabolites.org) [83] and the identified BGCs                          Department of Science and Technology for financial assistance under the
were further processed using the BiG-SCAPE program                              National Post-Doctoral Fellowship (File Number- PDF/2019/003065). G.S.
                                                                                would like to thank the Council of Scientific and Industrial Research (CSIR) re-
(https://git.wageningenur.nl/medema-group/BiGSCAPE)                             search fellowship and Department of Science and Technology (DST)-INSPIRE
[84]. Among the estimated BGCs, PUFA producing gene                             Faculty Award, Government of India for financial support. This work is sup-
cluster was identified by considering the PUFA biosyn-                          ported by intramural funds of CSIR (OLP0175) and a project “Expansion and
                                                                                modernization of Microbial Type Culture Collection and Gene Bank (MTCC)
thetic genes in Aetherobacter sp. SBSr008 (gene acces-                          jointly supported by the CSIR Grant No. BSC0402 and Department of Biotech-
sion no. - AIJ50375.1, AIJ50376.1, and AIJ50377.1), A.                          nology (DBT) Govt. of India Grant No. BT/PR7368/INF/22/177/2012”. The fund-
fasciculatus SBSr002 (gene accession no. - AIJ50372.1,                          ing bodies played no role in the design of the study, collection, analysis, and
                                                                                interpretation of data, and in writing the manuscript.
AIJ50373.1, and AIJ50374.1), and S. cellulosum So ce56
(gene accession no. - CAN90975.1, CAN90976.1,                                   Availability of data and materials
CAN90977.1, and CAN95221.1) [18]. BLAST searches                                The complete genome sequence of Minicystis rosea DSM 24000T and its
were performed for each of the Pfa1, Pfa2, and Pfa3 pro-                        annotations are deposited at DDBJ/ENA/GenBank under accession number
                                                                                CP016211.1.
tein sequences of M. rosea DSM 24000T, and were fur-
ther considered for phylogenetic analysis using the                             Declarations
WAG (G + I + F) model of the Maximum Likelihood
method in MEGA X [85]. The trees were visualized                                Ethics approval and consent to participate
                                                                                Not applicable.
using iTOL.
                                                                                Consent for publication
Abbreviations
                                                                                Not applicable.
CPS: Cellular Processes and Signaling; MET: Metabolism; ISP: Information
Storage and Processing; TCS: Two-component system; HK: Histidine kinases;
RR: Response regulators; ELKs: Eukaryotic-like kinases; PPs: Protein            Competing interests
phosphatases; BGC: Biosynthetic gene cluster; PKS: Polyketide synthase;         The authors with listed names declare no conflict of interest to disclose.
NRPS: Nonribosomal polypeptide synthetase; RiPP: Ribosomal synthesized
and post-translationally modified peptide; PUFA: Polyunsaturated fatty acid;    Author details
                                                                                1
KS: β-ketoacyl synthase; MAT/AT: Malonyl/acyltransferase; ACP: Acyl carrier      CSIR-Institute of Microbial Technology (CSIR-IMTECH), Chandigarh, India.
                                                                                2
protein; KR: Ketoreductase; PS-DH: PKS-like dehydratase; CLF: Chain length       Institute of Bioinformatics and Applied Biotechnology (IBAB), Bengaluru,
factor; AT: Acyltransferase; DH: Fab-A-like dehydratase; DH’: Pseudo-domain     Karnataka, India.
dehydratase; AGPAT: 1-acylglycerol-3-phosphate O-acyltransferase; PPTase: 4′-
phosphopantetheinyl transferase                                                 Received: 3 May 2021 Accepted: 23 August 2021


Supplementary Information                                                       References
The online version contains supplementary material available at https://doi.    1. Dawid W. Biology and global distribution of myxobacteria in soils. FEMS
org/10.1186/s12864-021-07955-x.                                                     Microbiol Rev. 2000;24(4):403–27. https://doi.org/10.1111/j.1574-6976.2000.
                                                                                    tb00548.x.
 Additional file 1: Fig. S1. Single-copy genes-based phylogenetic tree          2. Iizuka T, Jojima Y, Fudou R, Yamanaka S. Isolation of myxobacteria from the
 of myxobacteria. Branch color and leaf stripes represent the suborder and          marine environment. FEMS Microbiol Lett. 1998;169(2):317–22. https://doi.
 family-level taxonomy (color-coded), respectively.                                 org/10.1111/j.1574-6968.1998.tb13335.x.
                                                                                3. Reichenbach H. The ecology of the myxobacteria. Environ Microbiol. 1999;
 Additional file 2: Fig. S2. COG functional categorization of the Total,
                                                                                    1(1):15–21. https://doi.org/10.1046/j.1462-2920.1999.00016.x.
 Accessory, Core, and Unique proteins in M. rosea. CPS = Cellular Processes
                                                                                4. Sanford RA, Cole JR, Tiedje JM. Characterization and description of
 and Signaling, ISP = Information Storage and Processing, MET =
                                                                                    Anaeromyxobacter dehalogenans gen. nov., sp. nov., an aryl-halorespiring
 Metabolism, and PC = Poorly characterized.
                                                                                    facultative anaerobic myxobacterium. Appl Environ Microbiol. 2002;68(2):
 Additional file 3: Table S1. DDH and ANI values between M. rosea and               893–900. https://doi.org/10.1128/AEM.68.2.893-900.2002.
 selected myxobacteria. Color intensity changes from green to orange            5. Wolf-Jackel GA, Hansen MS, Larsen G, Holm E, Agerholm JS, Jensen TK.
 corresponding with higher to lower values, respectively.                           Diagnostic studies of abortion in Danish cattle 2015-2017. Acta Vet Scand.
 Additional file 4: Table S2. a) Distribution of core, unique, duplicate,           2020;62(1):1. https://doi.org/10.1186/s13028-019-0499-4.
 ELK, BGC genes in M. rosea. Unique exogenous genes in Column E have            6. Kaiser D, Robinson M, Kroos L. Myxobacteria, polarity, and multicellular
 been shaded using orange color.; b) Identified genomic islands in M.               morphogenesis. Cold Spring Harb Perspect Biol. 2010;2(8):a000380. https://
 rosea genome; and c) Comparative distribution of Pfam families among               doi.org/10.1101/cshperspect.a000380.
 the selected myxobacterial genomes.                                            7. Moine A, Agrebi R, Espinosa L, Kirby JR, Zusman DR, Mignot T, et al.
                                                                                    Functional organization of a multimodular bacterial chemosensory
Pal et al. BMC Genomics            (2021) 22:655                                                                                                         Page 14 of 15




      apparatus. PLoS Genet. 2014;10(3):e1004164. https://doi.org/10.1371/journal.     29. van Nimwegen E. Scaling laws in the functional content of genomes. Trends
      pgen.1004164.                                                                        Genet. 2003;19(9):479–84. https://doi.org/10.1016/S0168-9525(03)00203-8.
8.    Munoz-Dorado J, Marcos-Torres FJ, Garcia-Bravo E, Moraleda-Munoz A, Perez        30. Galperin MY. A census of membrane-bound and intracellular signal
      J. Myxobacteria: moving, killing, feeding, and surviving together. Front             transduction proteins in bacteria: bacterial IQ, extroverts and introverts. BMC
      Microbiol. 2016;7:781.                                                               Microbiol. 2005;5(1):35. https://doi.org/10.1186/1471-2180-5-35.
9.    Sharma G, Khatri I, Subramanian S. Comparative genomics of myxobacterial         31. Whitworth DE, Cock PJA. Two-component systems of the myxobacteria:
      chemosensory systems. J Bacteriol. 2018;200(3):e00620.                               structure, diversity and evolutionary relationships. Microbiology (Reading).
10.   Sharma G, Yao AI, Smaldone GT, Liang J, Long M, Facciotti MT, et al. Global          2008;154(Pt 2):360–72. https://doi.org/10.1099/mic.0.2007/013672-0.
      gene expression analysis of the Myxococcus xanthus developmental time            32. Munoz-Dorado J, Inouye S, Inouye M. A gene encoding a protein serine/
      course. Genomics. 2021;113(1 Pt 1):120–34. https://doi.org/10.1016/j.ygeno.2         threonine kinase is required for normal development of M. xanthus, a gram-
      020.11.030.                                                                          negative bacterium. Cell. 1991;67(5):995–1006. https://doi.org/10.1016/0092-
11.   Thiery S, Kaimer C. The predation strategy of Myxococcus xanthus. Front              8674(91)90372-6.
      Microbiol. 2020;11:2. https://doi.org/10.3389/fmicb.2020.00002.                  33. Schneiker S, Perlova O, Kaiser O, Gerth K, Alici A, Altmeyer MO, et al.
12.   Velicer GJ, Vos M. Sociobiology of the myxobacteria. Annu Rev Microbiol.             Complete genome sequence of the myxobacterium Sorangium cellulosum.
      2009;63(1):599–623. https://doi.org/10.1146/annurev.micro.091208.073158.             Nat Biotechnol. 2007;25(11):1281–9. https://doi.org/10.1038/nbt1354.
13.   Whitfield DL, Sharma G, Smaldone GT, Singer M. Peripheral rods: a                34. Perez J, Castaneda-Garcia A, Jenke-Kodama H, Muller R, Munoz-Dorado J.
      specialized developmental cell type in Myxococcus xanthus. Genomics. 2020;           Eukaryotic-like protein kinases in the prokaryotes and the myxobacterial
      112(2):1588–97. https://doi.org/10.1016/j.ygeno.2019.09.008.                         kinome. Proc Natl Acad Sci U S A. 2008;105(41):15950–5. https://doi.org/10.1
14.   Kiskowski MA, Jiang Y, Alber MS. Role of streams in myxobacteria aggregate           073/pnas.0806851105.
      formation. Phys Biol. 2004;1(3–4):173–83. https://doi.org/10.1088/1478-3         35. Kole HK, Abdel-Ghany M, Racker E. Specific dephosphorylation of
      967/1/3/005.                                                                         phosphoproteins by protein-serine and -tyrosine kinases. Proc Natl Acad Sci
15.   Gerth K, Pradella S, Perlova O, Beyer S, Muller R. Myxobacteria: proficient          U S A. 1988;85(16):5849–53. https://doi.org/10.1073/pnas.85.16.5849.
      producers of novel natural products with various biological activities--past     36. Pereira SF, Goss L, Dworkin J. Eukaryote-like serine/threonine kinases and
      and future biotechnological aspects with the focus on the genus                      phosphatases in bacteria. Microbiol Mol Biol Rev. 2011;75(1):192–212.
      Sorangium. J Biotechnol. 2003;106(2–3):233–53. https://doi.org/10.1016/j.            https://doi.org/10.1128/MMBR.00042-10.
      jbiotec.2003.07.015.                                                             37. Madec E, Laszkiewicz A, Iwanicki A, Obuchowski M, Seror S. Characterization
16.   Fischbach MA, Walsh CT. Assembly-line enzymology for polyketide and                  of a membrane-linked Ser/Thr protein kinase in Bacillus subtilis, implicated
      nonribosomal peptide antibiotics: logic, machinery, and mechanisms. Chem             in developmental processes. Mol Microbiol. 2002;46(2):571–86. https://doi.
      Rev. 2006;106(8):3468–96. https://doi.org/10.1021/cr0503097.                         org/10.1046/j.1365-2958.2002.03178.x .
17.   Reichenbach H, Hofle G. Biologically active secondary metabolites from           38. Treuner-Lange A. The phosphatomes of the multicellular myxobacteria
      myxobacteria. Biotechnol Adv. 1993;11(2):219–77. https://doi.org/10.1016/            Myxococcus xanthus and Sorangium cellulosum in comparison with other
      0734-9750(93)90042-L.                                                                prokaryotic genomes. PLoS One. 2010;5(6):e11164. https://doi.org/10.1371/
18.   Gemperlein K, Rachid S, Garcia R, Wenzel S, Müller R. Polyunsaturated 1 fatty        journal.pone.0011164.
      acid biosynthesis in myxobacteria: different PUFA synthases and their            39. Goldman B, Bhat S, Shimkets LJ. Genome evolution and the emergence of
      product diversity. Chem Sci. 2014;5(5):1733–41. https://doi.org/10.1039/c3           fruiting body development in Myxococcus xanthus. PLoS One. 2007;2(12):
      sc53163e.                                                                            e1329. https://doi.org/10.1371/journal.pone.0001329.
19.   Lorente-Cebrian S, Costa AG, Navas-Carretero S, Zabala M, Martinez JA,           40. Steinegger M, Meier M, Mirdita M, Vohringer H, Haunsberger SJ, Soding J.
      Moreno-Aliaga MJ. Role of omega-3 fatty acids in obesity, metabolic                  HH-suite3 for fast remote homology detection and deep protein
      syndrome, and cardiovascular diseases: a review of the evidence. J Physiol           annotation. BMC Bioinformatics. 2019;20(1):473. https://doi.org/10.1186/s12
      Biochem. 2013;69(3):633–51. https://doi.org/10.1007/s13105-013-0265-4.               859-019-3019-7.
20.   Sahena F, Zaidul ISM, Jinap S, Saari N, Jahurul HA, Abbas KA, et al. PUFAs in    41. Huntley S, Hamann N, Wegener-Feldbrugge S, Treuner-Lange A, Kube M,
      fish: extraction, fractionation, importance in health. Compr Rev Food Sci F.         Reinhardt R, et al. Comparative genomic analysis of fruiting body formation
      2009;8(2):59–74. https://doi.org/10.1111/j.1541-4337.2009.00069.x.                   in Myxococcales. Mol Biol Evol. 2011;28(2):1083–97. https://doi.org/10.1093/
21.   Shulse CN, Allen EE. Widespread occurrence of secondary lipid biosynthesis           molbev/msq292.
      potential in microbial lineages. PLoS One. 2011;6(5):e20146. https://doi.org/1   42. Garcia R, Gemperlein K, Muller R. Minicystis rosea gen. nov., sp. nov., a
      0.1371/journal.pone.0020146.                                                         polyunsaturated fatty acid-rich and steroid-producing soil myxobacterium.
22.   Metz JG, Roessler P, Facciotti D, Levering C, Dittrich F, Lassner M, et al.          Int J Syst Evol Microbiol. 2014;64(Pt 11):3733–42. https://doi.org/10.1099/ijs.
      Production of polyunsaturated fatty acids by polyketide synthases in both            0.068270-0 .
      prokaryotes and eukaryotes. Science. 2001;293(5528):290–3. https://doi.org/1     43. Kanehisa M, Goto S. KEGG: kyoto encyclopedia of genes and genomes.
      0.1126/science.1059593.                                                              Nucleic Acids Res. 2000;28(1):27–30. https://doi.org/10.1093/nar/28.1.27.
23.   Allen EE, Bartlett DH. Structure and regulation of the omega-3                   44. Konstantinidis K, Tiedje J. Trends between gene content and genome size
      polyunsaturated fatty acid synthase genes from the deep-sea bacterium                in prokaryotic species with larger genomes. PNAS. 2004;101(9):3160–5.
      Photobacterium profundum strain SS9. Microbiology (Reading). 2002;148(Pt             https://doi.org/10.1073/pnas.0308653100.
      6):1903–13. https://doi.org/10.1099/00221287-148-6-1903.                         45. Bretscher AP, Kaiser D. Nutrition of Myxococcus xanthus, a fruiting
24.   Morita N, Tanaka M, Okuyama H. Biosynthesis of fatty acids in the                    myxobacterium. J Bacteriol. 1978;133(2):763–8. https://doi.org/10.1128/
      docosahexaenoic acid-producing bacterium Moritella marina strain MP-1.               jb.133.2.763-768.1978.
      Biochem Soc Trans. 2000;28(6):943–5. https://doi.org/10.1042/bst0280943.         46. Bhat S, Boynton TO, Pham D, Shimkets LJ. Fatty acids from membrane lipids
25.   Orikasa Y, Nishida T, Hase A, Watanabe K, Morita N, Okuyama H. A                     become incorporated into lipid bodies during Myxococcus xanthus
      phosphopantetheinyl transferase gene essential for biosynthesis of n-3               differentiation. PLoS One. 2014;9(6):e99622. https://doi.org/10.1371/journal.
      polyunsaturated fatty acids from Moritella marina strain MP-1. FEBS Lett.            pone.0099622.
      2006;580(18):4423–9. https://doi.org/10.1016/j.febslet.2006.07.008.              47. Bode HB, Zeggel B, Silakowski B, Wenzel SC, Reichenbach H, Muller R.
26.   Zhao JY, Zhong L, Shen MJ, Xia ZJ, Cheng QX, Sun X, et al. Discovery of the          Steroid biosynthesis in prokaryotes: identification of myxobacterial steroids
      autonomously replicating plasmid pMF1 from Myxococcus fulvus and                     and cloning of the first bacterial 2,3(S)-oxidosqualene cyclase from the
      development of a gene cloning system in Myxococcus xanthus. Appl                     myxobacterium Stigmatella aurantiaca. Mol Microbiol. 2003;47(2):471–81.
      Environ Microbiol. 2008;74(7):1980–7. https://doi.org/10.1128/AEM.02143-07.          https://doi.org/10.1046/j.1365-2958.2003.03309.x.
27.   Han K, Li ZF, Peng R, Zhu LP, Zhou T, Wang LG, et al. Extraordinary              48. Hooper SD, Berg OG. On the nature of gene innovation: duplication
      expansion of a Sorangium cellulosum genome from an alkaline milieu. Sci              patterns in microbial genomes. Mol Biol Evol. 2003;20(6):945–54. https://doi.
      Rep. 2013;3(1):2101. https://doi.org/10.1038/srep02101.                              org/10.1093/molbev/msg101.
28.   Juhas M, Crook DW, Dimopoulou ID, Lunter G, Harding RM, Ferguson DJ,             49. Gevers D, Vandepoele K, Simillon C, Van de Peer Y. Gene duplication and
      et al. Novel type IV secretion system involved in propagation of genomic             biased functional retention of paralogs in bacterial genomes. Trends
      islands. J Bacteriol. 2007;189(3):761–71. https://doi.org/10.1128/JB.01327-06.       Microbiol. 2004;12(4):148–54. https://doi.org/10.1016/j.tim.2004.02.007.
Pal et al. BMC Genomics          (2021) 22:655                                                                                                           Page 15 of 15




50. Hahn M. Distinguishing among evolutionary models for the maintenance of                PLoS One. 2016;11(2):e0148593. https://doi.org/10.1371/journal.pone.014
    gene duplicates. J Hered. 2009;100(5):605–17. https://doi.org/10.1093/                 8593.
    jhered/esp047.                                                                   72.   Sharma G, Subramanian S. Unravelling the complete genome of
51. Cimermancic P, Medema M, Claesen J, Kurita K, Wieland Brown L,                         Archangium gephyra DSM 2261T and evolutionary insights into
    Mavrommatis K, et al. Insights into secondary metabolism from a global                 myxobacterial chitinases. Genome Biol Evol. 2017;9(5):1304–11. https://doi.
    analysis of prokaryotic biosynthetic gene clusters. Cell. 2014;158(2):412–21.          org/10.1093/gbe/evx066.
    https://doi.org/10.1016/j.cell.2014.06.034.                                      73.   Lechner M, Findeiss S, Steiner L, Marz M, Stadler PF, Prohaska SJ.
52. Heath RJ, Rock CO. The claisen condensation in biology. Nat Prod Rep.                  Proteinortho: detection of (co-)orthologs in large-scale analysis. BMC
    2002;19(5):581–96. https://doi.org/10.1039/b110221b.                                   Bioinformatics. 2011;12:124.
53. Tang Y, Tsai SC, Khosla C. Polyketide chain length control by chain length       74.   Altschul SF, Madden TL, Schaffer AA, Zhang J, Zhang Z, Miller W, et al.
    factor. J Am Chem Soc. 2003;125(42):12708–9. https://doi.org/10.1021/ja03              Gapped BLAST and PSI-BLAST: a new generation of protein database search
    78759.                                                                                 programs. Nucleic Acids Res. 1997;25(17):3389–402. https://doi.org/10.1093/
54. Staunton J, Weissman KJ. Polyketide biosynthesis: a millennium review. Nat             nar/25.17.3389.
    Prod Rep. 2001;18(4):380–416. https://doi.org/10.1039/a909079g.                  75.   Bertelli C, Laird MR, Williams KP, Simon Fraser University Research
55. Yoshida K, Hashimoto M, Hori R, Adachi T, Okuyama H, Orikasa Y, et al.                 Computing G, Lau BY, Hoad G, et al. IslandViewer 4: expanded prediction of
    Bacterial long-chain polyunsaturated fatty acids: their biosynthetic genes,            genomic islands for larger-scale datasets. Nucleic Acids Res. 2017;45(W1):
    functions, and practical use. Mar Drugs. 2016;14(5):94.                                W30–5. https://doi.org/10.1093/nar/gkx343.
56. Ujihara T, Nagano M, Wada H, Mitsuhashi S. Identification of a novel type of     76.   Finn RD, Bateman A, Clements J, Coggill P, Eberhardt RY, Eddy SR, et al.
    polyunsaturated fatty acid synthase involved in arachidonic acid                       Pfam: the protein families database. Nucleic Acids Res. 2014;42(Database
    biosynthesis. FEBS Lett. 2014;588(21):4032–6. https://doi.org/10.1016/j.               issue):D222–30. https://doi.org/10.1093/nar/gkt1223.
    febslet.2014.09.023.                                                             77.   Eddy SR. Accelerated profile HMM searches. PLoS Comput Biol. 2011;7(10):
57. Garcia R, Stadler M, Gemperlein K, Muller R. Aetherobacter fasciculatus gen.           e1002195. https://doi.org/10.1371/journal.pcbi.1002195.
    nov., sp. nov. and Aetherobacter rufus sp. nov., novel myxobacteria with         78.   Tatusov RL, Galperin MY, Natale DA, Koonin EV. The COG database: a tool
    promising biotechnological applications. Int J Syst Evol Microbiol. 2016;              for genome-scale analysis of protein functions and evolution. Nucleic Acids
    66(2):928–38. https://doi.org/10.1099/ijsem.0.000813.                                  Res. 2000;28(1):33–6. https://doi.org/10.1093/nar/28.1.33.
58. Chin CS, Alexander DH, Marks P, Klammer AA, Drake J, Heiner C, et al.            79.   Galperin MY, Makarova KS, Wolf YI, Koonin EV. Expanded microbial genome
    Nonhybrid, finished microbial genome assemblies from long-read SMRT                    coverage and improved protein family annotation in the COG database.
    sequencing data. Nat Methods. 2013;10(6):563–9. https://doi.org/10.1038/               Nucleic Acids Res. 2015;43(Database issue):D261–9. https://doi.org/10.1093/
    nmeth.2474.                                                                            nar/gku1223.
59. Aziz RK, Bartels D, Best AA, DeJongh M, Disz T, Edwards RA, et al. The RAST      80.   Hsiao WW, Ung K, Aeschliman D, Bryan J, Finlay BB, Brinkman FS. Evidence
    server: rapid annotations using subsystems technology. BMC Genomics.                   of a large novel gene pool associated with prokaryotic genomic islands.
    2008;9(1):75. https://doi.org/10.1186/1471-2164-9-75.                                  PLoS Genet. 2005;1(5):e62. https://doi.org/10.1371/journal.pgen.0010062.
60. Lagesen K, Hallin P, Rodland EA, Staerfeldt HH, Rognes T, Ussery DW.             81.   Almagro Armenteros JJ, Tsirigos KD, Sonderby CK, Petersen TN, Winther O,
    RNAmmer: consistent and rapid annotation of ribosomal RNA genes.                       Brunak S, et al. SignalP 5.0 improves signal peptide predictions using deep
    Nucleic Acids Res. 2007;35(9):3100–8. https://doi.org/10.1093/nar/gkm160.              neural networks. Nat Biotechnol. 2019;37(4):420–3. https://doi.org/10.1038/
61. Lowe TM, Eddy SR. tRNAscan-SE: a program for improved detection of                     s41587-019-0036-z.
    transfer RNA genes in genomic sequence. Nucleic Acids Res. 1997;25(5):           82.   Mastronunzio JE, Tisa LS, Normand P, Benson DR. Comparative secretome
    955–64. https://doi.org/10.1093/nar/25.5.955.                                          analysis suggests low plant cell wall degrading capacity in Frankia
62. Gruber AR, Findeiss S, Washietl S, Hofacker IL, Stadler PF. RNAz 2.0:                  symbionts. BMC Genomics. 2008;9(1):47. https://doi.org/10.1186/1471-2164-
    improved noncoding RNA detection. Pac Symp Biocomput. 2010;69–79.                      9-47.
    https://doi.org/10.1142/9789814295291_0011.                                      83.   Blin K, Shaw S, Steinke K, Villebro R, Ziemert N, Lee SY, et al. antiSMASH 5.0:
                                                                                           updates to the secondary metabolite genome mining pipeline. Nucleic
63. Alikhan NF, Petty NK, Ben Zakour NL, Beatson SA. BLAST Ring Image
                                                                                           Acids Res. 2019;47(W1):W81–7. https://doi.org/10.1093/nar/gkz310.
    Generator (BRIG): simple prokaryote genome comparisons. BMC Genomics.
                                                                                     84.   Navarro-Munoz JC, Selem-Mojica N, Mullowney MW, Kautsar SA, Tryon JH,
    2011;12(1):402. https://doi.org/10.1186/1471-2164-12-402.
                                                                                           Parkinson EI, et al. A computational framework to explore large-scale
64. Larkin MA, Blackshields G, Brown NP, Chenna R, McGettigan PA, McWilliam
                                                                                           biosynthetic diversity. Nat Chem Biol. 2020;16(1):60–8. https://doi.org/10.103
    H, et al. Clustal W and Clustal X version 2.0. Bioinformatics. 2007;23(21):
                                                                                           8/s41589-019-0400-9.
    2947–8. https://doi.org/10.1093/bioinformatics/btm404.
                                                                                     85.   Kumar S, Stecher G, Li M, Knyaz C, Tamura K. MEGA X: molecular
65. Stamatakis A. RAxML version 8: a tool for phylogenetic analysis and post-
                                                                                           evolutionary genetics analysis across computing platforms. Mol Biol Evol.
    analysis of large phylogenies. Bioinformatics. 2014;30(9):1312–3. https://doi.
                                                                                           2018;35(6):1547–9. https://doi.org/10.1093/molbev/msy096.
    org/10.1093/bioinformatics/btu033.
66. Letunic I, Bork P. Interactive Tree Of Life v2: online annotation and display
    of phylogenetic trees made easy. Nucleic Acids Res. 2011;39(Web Server           Publisher’s Note
    issue):W475–8.                                                                   Springer Nature remains neutral with regard to jurisdictional claims in
67. Milanese A, Mende DR, Paoli L, Salazar G, Ruscheweyh HJ, Cuenca M, et al.        published maps and institutional affiliations.
    Microbial abundance, activity and population genomic profiling with
    mOTUs2. Nat Commun. 2019;10(1):1014. https://doi.org/10.1038/s41467-019-
    08844-4.
68. Auch AF, von Jan M, Klenk HP, Goker M. Digital DNA-DNA hybridization for
    microbial species delineation by means of genome-to-genome sequence
    comparison. Stand Genomic Sci. 2010;2(1):117–34. https://doi.org/10.4056/
    sigs.531120.
69. Yoon SH, Ha SM, Lim J, Kwon S, Chun J. A large-scale evaluation of
    algorithms to calculate average nucleotide identity. Antonie Van
    Leeuwenhoek. 2017;110(10):1281–6. https://doi.org/10.1007/s10482-017-
    0844-4.
70. Sharma G, Khatri I, Subramanian S. Complete genome of the starch-
    degrading myxobacteria Sandaracinus amylolyticus DSM 53668T. Genome
    Biol Evol. 2016;8(8):2520–9. https://doi.org/10.1093/gbe/evw151.
71. Sharma G, Narwani T, Subramanian S. Complete genome sequence and
    comparative genomics of a novel myxobacterium Myxococcus hansupus.
