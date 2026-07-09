# Failure Analysis — BVBRC-49 (Szmolka et al. 2023)

**Verdict:** PARTIAL REPLICATION (strong).

This file catalogs, honestly and without spin, what did NOT work, was NOT done, or fell outside the scope of a sequence-only replication. The purpose is to justify the PARTIAL verdict — i.e. to make clear why this work did not promote itself to REPLICATED.

---

## 1. Wet-lab MIC not re-measured (paper claim C5)

**What the paper claims:** colistin MIC = **8 µg/mL** for isolate Ec45-2020 (paper text).

**What this replication did:** verified the *genetic basis* for colistin resistance — mcr-1.1 present on IncX4 plasmid CP134089 at 100% coverage / 100% identity by both AMRFinderPlus and abricate resfinder. Verified all seven resistance classes in the paper's Amp-Chl-Cip-Col-Sul-Tet-Tmp phenotype have a clear genetic determinant.

**What this replication did NOT do:** re-measure the actual MIC number. Broth microdilution requires the live isolate and a wet-lab bench.

**Why this matters:** the MIC value itself is inherited from the paper, not independently generated. mcr-1 presence is necessary but not sufficient for a specific MIC value; the numeric phenotype (8 µg/mL vs, say, 4 or 16 µg/mL) cannot be pinned down from sequence.

**How this could be closed:** contact the corresponding author for the Ec45-2020 isolate (or a preserved subculture), or find an equivalent mcr-1+ IncX4 ST162 duck E. coli in a biobank (e.g. NEBIH veterinary reference lab, DSMZ), and perform broth microdilution per EUCAST 2023 breakpoints.

## 2. Serotype H10:O55 not re-derived (paper claim C7)

**What the paper claims:** serotype **H10:O55** for Ec45-2020 via SerotypeFinder 2.0.

**What this replication did:** nothing. C7 was skipped.

**Why this failed:** no serotyping tool (ectyper, SerotypeFinder, SeqSero) was pre-installed in the `bvbrc14` conda env on uicgpu, and `pip install` had no outbound network in that env. Rather than add scope or wait on env fixes, we accepted this gap as scoped-out for a fast replication.

**Why this matters:** H10:O55 is a minor, non-central claim — the paper's headline is mcr-1 on IncX4 in ST162, not the serotype. But it is a real, un-tested paper claim.

**How this could be closed:** install ectyper (`pip install ectyper` or conda `bioconda::ectyper`) in a network-enabled env, re-run on the same GCF_038709795.1 assembly. ~5-minute fix in the right environment.

## 3. 114-strain minimum-spanning tree not rebuilt (paper Figure 1)

**What the paper does:** places Ec45-2020 in a minimum-spanning tree (MST) of 114 poultry mcr-1+ E. coli using cgMLST, showing epidemiological/phylogenetic context (Figure 1).

**What this replication did:** nothing at the phylogenetic-context level.

**Why this was scoped out:** the paper's strain-level claims (genome architecture, mcr-1 localization, ST162 typing, IncH gene content, APEC virulence set) were the target of this replication. Rebuilding the MST would have required downloading 114 additional assemblies, running cgMLST (chewBBACA or similar), and MST construction — many hours of additional work for a claim that is not strain-level.

**Why this matters:** the paper's phylogenetic positioning of Ec45-2020 in the broader European/global poultry mcr-1 population is thus neither confirmed nor challenged by this replication. A reader wanting to know "is Ec45-2020 an outlier or a typical member of the European poultry mcr-1 cluster?" will not find an answer here.

**How this could be closed:** pull the 114 accessions from the paper's supplementary, run chewBBACA against the Enterobase E. coli cgMLST v1 scheme, build MST in GrapeTree, and re-render Figure 1.

## 4. Plasmid comparison figures not rebuilt (paper Figures 3-4)

**What the paper does:** compares the IncX4 mcr-1 plasmid and the IncHI MDR plasmid backbones against reference plasmids from other geographies/hosts (Figures 3-4), typically via BLAST-ring or Mauve-style alignments.

**What this replication did:** nothing at the plasmid-comparison level.

**Why this was scoped out:** same reasoning as #3 — strain-level claims were the target. The plasmid backbone comparisons are important for the "is this Central European IncX4 backbone shared globally?" question but do not affect the paper's central factual claim that mcr-1 is on IncX4 in this strain (which IS confirmed).

**Why this matters:** whether Ec45-2020's IncX4 plasmid backbone is monophyletic with global IncX4-mcr-1 or represents an independent introduction is an open question (see open_questions.json #1).

**How this could be closed:** curate a set of complete IncX4-mcr-1 plasmid sequences from NCBI, run pyANI / MOB-suite / BRIG for backbone comparisons.

## 5. We tested the deposited assembly, not the raw reads

**What a strict from-scratch replication would do:** download SRA raw reads (Illumina short-read + Nanopore long-read), run a hybrid assembly (Unicycler / Trycycler), re-derive plasmid circularity independently, THEN type.

**What this replication did:** trusted the deposited GCF_038709795.1 RefSeq assembly and typed it.

**Why this matters:** we verify that the deposited assembly supports the paper's typing claims. We do NOT independently verify the assembly itself. If there were a subtle assembly error (mis-assembled plasmid junction, chimeric contig), we would inherit it.

**Why this is acceptable for PARTIAL:** re-assembly would multiply compute cost by ~50× (hybrid assembly is slow) for a marginal gain in independence, given that the deposited assembly has the same replicon count (chromosome + 5) and matches paper lengths within pipeline cosmetic differences.

## 6. RefSeq annotation cosmetic differences

**Observation:** RefSeq chromosome length is **4,967,063 bp** vs paper's **4,966,963 bp** — a 100 bp delta. Allele subtype labels differ cosmetically: paper "blaTEM" → AMRFinderPlus "blaTEM-135"; paper "cmlA1/floR" → separate "cmlA1" and "floR" hits.

**Why this is not a failure:** these are annotation-pipeline artifacts (terminal base trim/pad on chromosome; more granular allele calling by newer resfinder DB). Gene identities agree.

**Why we mention it:** a reader doing side-by-side table comparison should not be confused by these harmless deltas.

## 7. Extra genes on IncH plasmid not enumerated in paper text

**Observation:** on CP134088 (254 kb IncH plasmid) we recovered blaTEM-135, sul2, tet(A), tet(M), qacL — genes the paper's main-text list did not mention (the paper listed dfrA12, aadA1/2, sul3, qnrS1, cmlA1/floR).

**Interpretation:** most likely the paper's Table S2 is an editorial subset and these additional genes are simply not enumerated in the main text prose. We cannot rule out that this reflects a curation gap in the paper.

**Why this is not a contradiction:** every paper-named gene IS present. The extras add to, they do not subtract from, the paper's claim.

---

## Summary: why this is PARTIAL, not REPLICATED

- ✅ 5 of 7 paper claims (C1, C2, C3, C4, C6) exactly matched on the deposited assembly.
- ⚠ 1 of 7 (C5) partially matched — genotype ✅ but MIC number not re-measured.
- ❌ 1 of 7 (C7) not tested at all — no offline serotyper.
- ❌ 2 non-strain-level analyses (paper Figure 1 MST, Figures 3-4 plasmid comparisons) scoped out entirely.

A REPLICATED verdict would require closing at least (C5) with a wet-lab MIC and (C7) with a serotyper run. This replication is honest that it did neither, so it stops at PARTIAL — but the PARTIAL is strong: the genomic headline (mcr-1.1 on IncX4 alone, in ST162, with the paper's full ARG / VG / plasmid-typing set) fully replicates on real deposited data with three independent free tools. No claim tested was contradicted; the gaps are gaps, not failures of the paper.
