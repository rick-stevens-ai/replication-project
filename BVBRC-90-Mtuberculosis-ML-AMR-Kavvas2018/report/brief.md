# Brief — BVBRC-90

**Paper:** Kavvas ES, Catoiu E, Mih N, Yurkovich JT, Seif Y, Dillon N, Heckmann D, Anand A, Yang L, Nizet V, Monk JM, Palsson BO (2018). "Machine learning and structural analysis of *Mycobacterium tuberculosis* pan-genome identifies genetic signatures of antibiotic resistance." *Nature Communications* 9:4306. DOI: 10.1038/s41467-018-06634-y. PMID: 30333483.

**What:** The authors build a reference-agnostic allele pan-genome of 1595 M. tuberculosis strains from PATRIC (now BV-BRC), then use mutual information + ensemble SVM to identify AMR genes for 13 antibiotics. Claim: recovers 33 known AMR genes, identifies 24 new, uncovers 97 epistatic interactions.

**Why replicate:** BV-BRC-linked flagship application of ML pan-genomics to AMR; foundational for later pan-genome ML on multi-organism panels (Marin 2020 PLOS Comp Biol builds directly on this).

**Method here:** Fetched all Nature/Springer supplementary data (MOESM1 PDF + MOESM4/5/7/9 XLSX ~6 MB); reconstructed the paper's Table 1 known-AMR verification, ranked-MI drug-target recovery, LOR-AMR internal consistency (809 alleles), NCBI H37Rv reference-protein exact-match check on 6 canonical AMR genes, and Benjamini-Hochberg re-analysis of the 307 epistasis candidates in MOESM7. LLM judge (GPT-5.2 via Argo) scored the resulting evidence.

**Verdict:** PARTIAL — the paper's central results (known-gene recovery, MI ranking of drug targets, LOR-label consistency, epistasis, biological plausibility of alleles) are all independently verified from public artifacts alone; end-to-end refit of the SVM cannot be done because the raw per-strain allele matrix is not distributed.
