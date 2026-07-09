# Brief — BVBRC-38: Gen2Epi (2019)

**What:** Independent replication of Sundaraj/Demczuk et al. 2019 "Gen2Epi: an automated whole-genome
sequencing pipeline for linking full genomes to antimicrobial susceptibility and molecular epidemiological
data in *Neisseria gonorrhoeae*" (BMC Genomics 20:165, DOI 10.1186/s12864-019-5542-3).

**Why/how:** Gen2Epi is a pipeline that (1) assembles Illumina short reads into full-length *N. gonorrhoeae*
scaffolds and (2) auto-assigns NG-MLST / NG-MAST / NG-STAR molecular typing and AMR-determinant information.
Its distribution is a CentOS-7 VirtualBox image (anonymous FTP `ftp://ftp.cs.usask.ca/pub/combi`). Rather than
run the image, we independently re-implemented the paper's **method** on **real public data**: the 11 WHO 2016
reference strains (WHO F,G,K,L,M,N,O,P,X,Y,Z) that Gen2Epi itself used as its reference/validation set
(ENA PRJEB14020, Unemo 2016 finished PacBio genomes), plus a genuine SPAdes de-novo assembly of WHO_F from raw
Illumina reads (ENA ERR5860304). We reproduced: genome-assembly statistics (vs Table 1 WHO column), full 7-locus
NG-MLST typing (pubMLST alleles + profiles), and NG-STAR AMR-determinant detection (penA mosaic, gyrA/parC QRDR,
ponA L421P, mtrR, porB/penB, 23S rRNA copies) — then validated the AMR calls against the known WHO-panel
resistance phenotypes (Unemo 2016). All endpoints free/public; LLM-judge scoring via free Argo.
