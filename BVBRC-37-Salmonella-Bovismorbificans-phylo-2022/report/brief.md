# BVBRC-37 — Brief

**What:** Independent replication of Gopinath et al. 2022 (*Microorganisms* 10(6):1199, DOI 10.3390/microorganisms10061199), a phylogenomic study of *Salmonella enterica* subsp. *enterica* serovar Bovismorbificans from clinical + food sources that reports the serovar splits into **two distinct polyphyletic lineages** — one backbone of ST142/ST377/ST1499/ST2640 versus a separate ST150 lineage.

**Why testable:** The paper deposited all 81 newly-sequenced WGS assemblies in NCBI BioProject **PRJNA378379** (GenomeTrakr, CC-BY, public). This makes the serovar confirmation, MLST/ST distribution, whole-genome clustering (two-lineage claim), source linkage (clinical+food), and AMR/virulence content directly re-derivable on real public data with standard open tools.

**Outcome:** All 82 Bovismorbificans genomes in the BioProject were pulled fresh (NCBI Datasets REST) and re-analyzed on uicgpu (SeqSero2, mlst/pubMLST, mash + hierarchical clustering, AMRFinderPlus). Serovar (82/82 Bovismorbificans, 8:r:1,5), the exact four dominant STs, the two-cluster topology (ST150 isolated vs the four-ST backbone), the clinical+food multi-country sampling, and the AMR/virulence feature classes all reproduce. **Verdict: REPLICATED** (LLM-judge, free Argo gpt-5.2; coverage ~0.92).
