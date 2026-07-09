# BVBRC-111 — Brief

**Paper:** Harmer et al. 2022, *J Antimicrob Chemother* 77(7):1851-1855. PMID 35403193. DOI 10.1093/jac/dkac115.
"Complete genome of the extensively antibiotic-resistant GC1 *Acinetobacter baumannii* isolate MRSN 56 reveals a novel route to fluoroquinolone resistance."

**What we did:** Downloaded the paper's own public NCBI assembly (GCA_021484925.1 for the chromosome CP090606.1, plus plasmid accessions CP080453–CP080456 for the four small plasmids), then re-ran the paper's core analyses independently using open tools: MLST (Pasteur + Oxford schemes), AMR gene detection across ResFinder + CARD + NCBI + MEGARES + ARG-ANNOT, PlasmidFinder, protein-level extraction of gyrA and QRDR alignment against WT reference WP_000116449.1, and feature-level location analysis of Tn7 machinery, ISAba1/IS26 insertion sequences, and the AbaR28 island in *comM*. Compared every quantitative or positional claim to the paper.

**Result:** 6/7 core claims fully reproduced (ST1 Pasteur, 4 AMR-free plasmids, AbaR28 in *comM* with aphA1/aacC1/aadA1/sul1, two Tn2006/blaOXA-23 copies with ISAba1 flanks, two Tn7 copies with dfrA1/aadA1/sat, novel Tn7+ configuration downstream of *glmS* with tetA(B)/sul2, gyrA S83L QRDR mutation). The 7th (ISAba1-mediated marR inactivation with constitutive marA expression) is structurally reproduced but the transcriptional-activation aspect requires RNAseq we did not run. Two independent LLM judges scored 88 and 95 (mean 91.5). Verdict: **REPLICATED**.
