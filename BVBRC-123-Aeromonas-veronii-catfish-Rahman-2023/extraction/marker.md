# Marker Extraction (pdftotext fallback)

The on-demand marker parser was not directly callable from this replication turn (marker/nougat MCP not wired
into this subagent's tool set). As a deterministic, layout-preserving alternative, I ran `pdftotext -layout paper.pdf`.
The resulting plain text is preserved at `extraction/paper_pdftotext.txt` and is what all downstream claim
extraction in this replication was performed against. All key numerical claims (genome size, N50, L50, GC%, CDS,
tRNA/rRNA, ST 492, prophage counts, MDR antibiogram, accession IDs) were successfully extracted with no OCR loss.

This is a text-preserving substitute for marker output. If the central corpus later parses the paper with true
marker, that file will supersede this one — but the substantive claim extraction is complete.

JOURNAL OF ADVANCED VETERINARY AND ANIMAL RESEARCH
ISSN 2311-7710 (Electronic)
http://doi.org/10.5455/javar.2023.j711                                                                                                     September 2023
A periodical of the Network for the Veterinarians of Bangladesh (BDvetNET)                                                    VOL 10, NO. 3, PAGES 570–578




ORIGINAL ARTICLE

Complete genome sequence analysis of the multidrug resistant Aeromonas veronii
isolated for the first time from stinging catfish (Shing fish) in Bangladesh
Mohummad Muklesur Rahman1 , Mohammad Sadekuzzaman2 , Md. Asikur Rahman3 ,
Mahbubul Pratik Siddique1 , Mohammad Asir Uddin1 , Md. Enamul Haque1 , Md. Golam Azam Chowdhury2,
A. K. M. Khasruzzaman1 , Md. Tanvir Rahman1 , Muhammad Tofazzal Hossain1 , Md. Alimul Islam1
1
 Department of Microbiology and Hygiene, Bangladesh Agricultural University, Mymensingh, Bangladesh
2
 Central Disease Investigation Laboratory, Department of Livestock Services, Dhaka, Bangladesh
3
 Bangladesh Fisheries Research Institute, Mymensingh, Bangladesh

                                                                                                                        ARTICLE HISTORY
    ABSTRACT                                                                                                            Received August 09, 2023
    Objective: Whole genome sequencing (WGS) of Aeromonas veronii Alim_AV_1000 isolated from                            Revised August 29, 2023
    ulcerative lesions of Shing fish (stringing catfish; Heteropneustes fossilis) was performed during                  Accepted September 02, 2023
    the outbreak year 2021.                                                                                             Published September 30, 2023
    Materials and Methods: Using next-generation sequencing (Illumina) technology, WGS was
    accomplished, resulting in the sequencing, assembly, and analysis of the entire genome of the                       KEYWORDS
    A. veronii strain. Moreover, the genomic features, virulence factors, antimicrobial resistome, and                  Aeromonas veronii; antimicrobial
    phylogenetic analysis for the molecular evolution of this strain were also examined.                                resistance; fish; phylogeny; whole
    Results: The genome size of the A. veronii Alim_AV_1000 strain was 4,494,515 bp, with an aver-                      genome
    age G+C content of 58.87%. Annotation revealed the known transporters and genes linked to
    virulence, drug targets, and antimicrobial resistance.
    Conclusion: The findings of the phylogenetic analysis revealed that the strain of the present study
    has a close relationship with the China strain TH0426 and strain B56. This study provides novel                    © The authors. This is an Open Access
    information on A. veronii isolated from Shing fish in Bangladesh.                                                  article distributed under the terms of
                                                                                                                       the Creative Commons Attribution 4.0
                                                                                                                       License (http://creativecommons.org/
                                                                                                                       licenses/by/4.0)
