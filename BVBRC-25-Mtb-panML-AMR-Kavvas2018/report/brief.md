# BVBRC-25 — Brief

**Paper:** Kavvas ES, Catoiu E, Mih N, Yurkovich JT, Seif Y, Dillon N, Heckmann D, Anand A, Yang L, Nizet V, Monk JM, Palsson BO.
*Machine learning and structural analysis of Mycobacterium tuberculosis pan-genome identifies genetic signatures of antibiotic resistance.*
**Nature Communications** 9:4306 (2018). **DOI:** [10.1038/s41467-018-06634-y](https://doi.org/10.1038/s41467-018-06634-y) — **PMID** 30333483 — **PMCID** PMC6193043. Open access (CC BY 4.0).

## What / why
The authors build an allele-level **pan-genome of 1,595 publicly available (PATRIC/BV-BRC) *M. tuberculosis* strains**, pair it with binary R/S phenotypes for **13 antibiotics**, and use **pairwise association (mutual information, chi-squared, ANOVA F-test)** plus an **ensemble L1-regularized SVM** to recover known resistance genes and nominate new AMR signatures, then add epistasis (logistic regression) and 3-D structural mapping. Four headline results: (1) the pan-genome is highly conserved with variation concentrated in PE/PPE/PGRS genes; (2) 33 known resistance genes corroborated + 24 new AMR signatures; (3) 97 epistatic interactions across 10 resistance classes; (4) structural mechanisms for selected genes.

## Replication scope (this pass — REAL rerun)
Because the authors published their **processed pan-genome matrices** (allele presence/absence 1595×15,367; cluster→gene map; 13-drug R/S table) on GitHub (`erolkavvas/microbial_AMR_ML`), we independently **re-implemented their core computational pipeline from scratch** (our own MI/chi-squared and ensemble-SVM code, not their notebooks) on the real data and tested whether it recovers the paper's central claims:
- **Result #1** (conservation + PE/PPE/PGRS enrichment) — recomputed from cluster_info.
- **Result #2, association half** (MI recovers primary AMR genes) — re-derived per drug.
- **Result #2, ML half** (ensemble L1-SVM recovers additional known genes after preprocessing) — re-derived per drug.

Heavy MI/SVM compute run on **uicgpu** (255 cores, 2 TB RAM). Free tooling only (numpy/scipy/scikit-learn). Out of scope: full RAxML phylogeny rebuild, the 3-D structural mutation mapping, and exhaustive epistasis logistic-regression sweep.
