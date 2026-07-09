# BVBRC-94 — Brief

**Paper:** Milerienė J, Aksomaitienė J, Kondrotienė K, Ásledóttir T, Vegarud GE, Šernienė L, Malakauskas M.
*Whole-Genome Sequence of Lactococcus lactis Subsp. lactis LL16 Confirms Safety, Probiotic Potential, and Reveals Functional Traits.*
Microorganisms (MDPI) 11(4):1034 (2023). **DOI:** [10.3390/microorganisms11041034](https://doi.org/10.3390/microorganisms11041034) — PMID 37110457 — PMCID PMC10145936.
**Open access:** ✅ (CC BY 4.0 / MDPI).

## What the paper does
Whole-genome sequencing (Illumina MiSeq, Nextera XT) of an indigenous Lithuanian dairy isolate `Lactococcus lactis subsp. lactis LL16`. Runs SEED/RAST subsystem annotation, EFSA-style *in silico* safety screens (ResFinder, VirulenceFinder, PathogenFinder), plasmid + IS + CRISPR detection (MobileElementFinder, CRISPRFinder), bacteriocin prediction (BAGEL v4), secondary-metabolite BGC detection (antiSMASH 5.0), and *in vitro* GABA production in fermented milk. Assembled genome deposited at GenBank as **JARHUB000000000** (assembly `GCA_029912225.1` / `GCF_029912225.1`).

## Core claims tested here
1. **Species / phylogeny (C1)** — LL16 is `L. lactis subsp. lactis`; closest fully-sequenced relative is `L. lactis subsp. lactis UC06` (NZ_CP015902.1).
2. **Genome stats (C2)** — 2,589,406 bp, 35.4% GC, 246 RAST subsystems, 2878 CDS, 63 tRNAs (paper text "CDA/RNRs 2878/63" appears to be an OCR-mangled CDS/tRNA count).
3. **Safety (C3)** — no acquired antibiotic-resistance genes, no virulence factors, no biogenic-amine decarboxylases.
4. **Bacteriocins (C4)** — genome encodes putative Lactococcin B (LcnB) and Enterolysin A (EnlA) clusters.
5. **Plasmid (C5)** — a single plasmid replication region matching **repUS4 / repA_pCI2000** (paper says 99.57% identity to pCI2000, `AF178424`).
6. **Mobile / CRISPR (C6)** — 3 IS elements (IS6 family: ISS1B, ISS1N, ISLla3) + 1 CRISPR array (3 spacers, DR=23) + a Cas gene.
7. **Secondary metabolites (C7)** — one antiSMASH-detectable BGC classified as **type III polyketide synthase (T3PKS)**.
8. **GABA-related (C8)** — genome carries a functional GABA-producing pathway (glutamate decarboxylase + Glu/GABA antiporter).

## Replication scope
Independent rerun from public artifacts (NCBI Datasets assembly + downstream tools). No cell-culture *in vitro* rerun — the *in vitro* GABA quantification in fermented milk (Section 3.10) is genuinely non-reproducible from a subagent workstation, and is out of scope.
