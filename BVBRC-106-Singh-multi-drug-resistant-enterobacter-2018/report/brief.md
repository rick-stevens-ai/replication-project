# Brief — BVBRC-106

**Paper**: Singh et al. 2018. "Multi-drug resistant *Enterobacter bugandensis* species isolated from the International Space Station and comparative genomic analyses with human pathogenic strains." *BMC Microbiology* 18:175 (PMID 30466389, PMC6251167).

**What we're doing**: Independently replicate the paper's core claims by (a) pulling the 5 ISS *E. bugandensis* assemblies (BioProject PRJNA319366; accessions POUO, POUP, POUQ, POUR, RBVJ) and the 3 clinical comparators (EB-247T FYBI, 153_ECLO NZ_JVSD, MBRL-1077 PRJNA310238) from NCBI, (b) reproducing the ANI/ANI-like matrix that classifies all five ISS isolates as *E. bugandensis* (paper reports ANI ≥ 98.66 % ISS vs. clinical, 95.26 % vs. MBRL-1077), and (c) screening the 8 genomes for AMR genes with AMRFinderPlus (modern equivalent of the paper's RAST-subsystem AMR call). Verdict rendered by an LLM judge (Argo) comparing our numbers against the paper's Table 1 + AMR narrative.

**Why**: The paper is a WGS+comparative-genomics claim with all data public, so it's cleanly independently checkable with modern tooling.
