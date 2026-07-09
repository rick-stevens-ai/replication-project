# BVBRC-113 — Nakazono 2022 (PLoS One): S. epidermidis bacteriocin plasmids

**What:** Independent replication of Nakazono *et al.* 2022 (PMID 35041663), "Complete sequences of epidermin and nukacin encoding plasmids from oral-derived *Staphylococcus epidermidis* and their antibacterial activity" (PLoS ONE 17(1):e0258283).

**Why:** The paper reports two novel bacteriocin-carrying plasmids from oral-derived *S. epidermidis* — pEpi56 (epidermin, 64,386 bp) and pNuk650 (nukacin, 26,160 bp) — deposited under NCBI accessions **OK031036** and **OK031035**. We refetch these public records and directly test the paper's quantitative sequence-level claims (plasmid sizes, ORF counts, epidermin identity to Tü3298 (X62386), nukacin similarity to IVK45 (KP702950), prepeptide/mature peptide mismatches).

**Result:** **PARTIAL replication (score 74/100, LLM-judge)** — every sequence-identity claim reproduces exactly (epidermin KSE56 = 100% aa identity with Tü3298 with 2 nt mismatches; nukacin KSE650 prepeptide differs from IVK45 by 1 aa at position 4; mature peptides identical); plasmid sizes and total ORF counts match Tables 2 & 3 exactly (81 and 29). The "additional seven ORFs on pNuk650 vs pIVK45" claim is off by 5–6 CDS under any straightforward count (raw diff = 12, orthology diff = 13), likely reflecting different annotation depth of pIVK45.
