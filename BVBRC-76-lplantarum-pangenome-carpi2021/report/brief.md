# Brief: BVBRC-76 — Carpi et al. 2021 L. plantarum pan-genome

**Paper.** Carpi FM, Coman MM, Silvi S, Picciolini M, Verdenelli MC, Napolioni V. "Comprehensive pan-genome analysis of *Lactiplantibacillus plantarum* complete genomes." *J Appl Microbiol* 132:592–604 (2022, first published 2021). DOI 10.1111/jam.15199, PMID 34216519, PMC9290807, CC-BY open access.

**What.** They pulled every complete *L. plantarum* assembly from NCBI as of July 2020 (541 total assemblies → 130 complete → 127 with RefSeq annotations), reannotated with Prokka v1.14.5, and ran Roary v3.11.2 pan-genome analysis (thresholds core ≥99%, soft-core 95–99%, shell 15–95%, cloud <15%). Headline numbers: **1,436 core + 414 soft-core + 1,858 shell + 13,203 cloud = 16,911 total pan-genome gene clusters**; pan-genome is **"open"** (still gaining genes past 100 strains); ~**70% of probiotic marker genes fall in core/soft-core**.

**Why replicate.** Data is 100% public (NCBI Assembly), tool stack is FOSS (Prokka + Roary), thresholds explicit. Independent rederivation of the pan-genome tests both the data-availability claim and the core method.

**This replication.** Rederived the July-2020 RefSeq complete-genome census from NCBI Datasets v2 (**124 unique RefSeq strains, matching the paper's 127 within curation drift**), downloaded all 124 FASTA assemblies, reannotated with Prokka 1.14.6 (paper: 1.14.5), and ran Roary 3.13.0 (paper: 3.11.2) with the paper's exact percent-of-strains thresholds. Report the four-class partition and total pan-genome size back against the paper's numbers.
