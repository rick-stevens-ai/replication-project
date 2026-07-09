# Marker extraction (compact, prose form)

Marker is not installed on cherryrd or in a reachable path on uicgpu. This is a prose-form extraction of the paper's key content using system `pdftotext` (poppler) plus targeted parsing. Raw pdftotext output lives at `work/paper.txt`.

## Metadata
- **Title:** Whole Genome Analyses Accurately Identify *Neisseria* spp. and Limit Taxonomic Ambiguity
- **Authors:** M. Khoder, M. Osman (corresponding: mo368@cornell.edu), I. I. Kassem, R. Rafei, A. Shahin, P. E. Fournier, J.-M. Rolain, M. Hamze
- **Venue:** *International Journal of Molecular Sciences* 23(21):13456 (Nov 3, 2022)
- **DOI:** 10.3390/ijms232113456   **PMID:** 36362240   **PMC:** PMC9657967

## Abstract (summarized)
Draft genomes of four commensal *Neisseria* clinical isolates from semen of infertile Lebanese men were compared against complete NCBI genomes of *N. gonorrhoeae* and *N. meningitidis* plus draft genomes of *N. flavescens*, *N. perflava*, *N. mucosa*, *N. macacae*. WGS accurately identified and corroborated MALDI-TOF species assignments. The combination of isDDH + OrthoANI + pangenome was the best identification approach. Some deposited NCBI Neisseria strains contain taxonomic errors. Robust cutoffs are needed to delineate species using genomic tools.

## The four Lebanese isolates (Table 1 in paper)

| paper name | deposited name | accession | contigs | size (bp) | GC% | CDS | RNAs | paper species |
|---|---|---|---|---|---|---|---|---|
| R19 | CMUL013 / N13 | GCA_900654165 | 34 | 2 207 472 | 49.2 | 2091 | 69 | *N. flavescens* |
| R20 | CMUL032 / N32 | GCA_900654175 | 123 | 2 541 217 | 51.0 | 2288 | 70 | *N. mucosa* |
| R21 | CMUL057 / N57 | GCA_900654185 | 36 | 2 268 952 | 49.0 | 2121 | 86 | *N. flavescens* |
| R23 | CMUL078 / N78 | GCA_900654195 | 79 | 2 194 968 | 49.4 | 2100 | 106 | *N. flavescens* |

## Methods

- **Isolation:** semen samples → polyViteX chocolate agar → API®-NH → MALDI-TOF Biotyper (Bruker, v2.0) → 16S rDNA sequencing.
- **DNA:** EZ1 DNA Tissue Kit (BioRobot EZ1) → Illumina MiSeq (2×250 bp paired-end, 40 h run, 8.2 Gb total, mate-pair library via Nextera).
- **Assembly:** A5 pipeline → Mauve alignment → Prokka + RAST annotation.
- **Virulence:** ABRICATE (https://github.com/tseemann/abricate/).
- **AMR genes:** BLAST in Bio-Edit against ARGannot database (e-value 1e-5) + NCBI nr BLAST confirmation.
- **Reference set:** 128 NCBI Neisseria genomes — 15 gonorrhoeae complete, 91 meningitidis complete, 7 flavescens draft, 4 perflava draft, 9 mucosa (1 complete + 8 draft), 2 macacae draft.
- **Pairwise identity:** OrthoANI (ezbiocloud.net/tools/orthoani), heatmaps rendered in Morpheus (Broad).
- **isDDH:** GGDC formula 2 at http://ggdc.dsmz.de/
- **Pangenome:** Roary on Galaxy Australia (https://usegalaxy.org.au./). Reference genomes per species: gonorrhoeae FA1090, meningitidis MC58, mucosa ATCC 19696, flavescens NCTC8263, macacae ATCC33926.
- **Cutoffs:** 95% OrthoANI, 70% isDDH.

## Key results

1. **API vs MALDI-TOF vs WGS.** API-NH called all four isolates *N. gonorrhoeae* (misidentification). MALDI-TOF reassigned R19/R21/R23 → flavescens, R20 → mucosa. WGS confirmed MALDI-TOF.
2. **R19 vs 128 refs (isDDH, Table 2):** highest isDDH = 65.7% with N. flavescens CDNF3; 30.9% with meningitidis MC58; 29.7% with gonorrhoeae FA1090; 28.9% with mucosa ATCC 19696; 24.3% with perflava CCH10H12; 16.4% with perflava CCH6A12. Notably ~64.2% with perflava UMB0023/UMB0210 (comparable to CDNF3).
3. **OrthoANI heatmaps (Figures 1–2):** R19/R21/R23 cluster with flavescens/perflava at ~82.85%–95.71%; R20 clusters with mucosa (~97.7%).
4. **Boundary calls:** R19/R21/R23 assigned to flavescens on the basis of high OrthoANI 95.66%/95.71% and isDDH 64.2% (below 70% but authors accept this as flavescens).
5. **NCBI mislabeling:** paper identifies specific errors in deposited Neisseria genomes; explicit example: some genomes deposited as "flavescens" cluster with mucosa or with perflava/subflava.
6. **Pangenome:** Neisseria pangenome shows some genomes have no core with other Neisseria spp. and very low OrthoANI (~65%), suggesting they are not really Neisseria at all.

## Software cited
- A5 pipeline (assembly)
- Mauve (contig ordering)
- Prokka (annotation)
- RAST (annotation)
- ABRICATE
- BLAST (Bio-Edit)
- OrthoANI (ezbiocloud)
- GGDC (Genome-to-Genome Distance Calculator, dsmz.de)
- Morpheus (Broad, heatmap)
- Roary (pangenome, on Galaxy Australia)

## Supplementary
Supplementary Materials linked at https://www.mdpi.com/article/10.3390/ijms232113456/s1 — Table S1 lists all 128 reference genome accessions.

## Data Availability Statement
"Not applicable." (The four novel genomes are deposited under GCA_900654165 / 175 / 185 / 195; project PRJEB30649.)
