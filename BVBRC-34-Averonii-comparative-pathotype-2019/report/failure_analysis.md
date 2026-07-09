# Failure analysis — BVBRC-34 (Tekedar et al. 2019, A. veronii pathotype)

**Verdict:** PARTIAL REPLICATION (strong). This file is the honest accounting of what did *not* replicate cleanly, why, and what would be needed to close each gap. Nothing was contradicted; the gaps below are gaps of scope, algorithm, and annotation — not disagreements.

## 1. Pan-genome total: 8710 (paper) vs 9664 (this work) — +11%
- **What happened.** The paper used EDGAR 2.0 with a bidirectional BLAST score-ratio (BSR) ortholog criterion; this replication used CD-HIT at 70% identity / 70% coverage on the concatenated 166,630-protein set.
- **Root cause.** CD-HIT is a greedy single-linkage similarity clusterer. EDGAR's BSR criterion tends to merge distant paralogs that CD-HIT will split into separate clusters — expanding the pan-genome total under CD-HIT relative to EDGAR. This is a well-known algorithm-level difference in the pan-genomics literature.
- **What still worked.** The core-genome count is essentially the same (2834 here vs 2855 paper, delta 0.7%) and the core fraction is very close (29.3% vs 30.9%) — because core genes are conserved enough that the two clustering criteria agree. The open-pan conclusion is independently supported by the 3,319 genome-unique cloud genes in the frequency spectrum.
- **Why this is not a bug.** The correct scientific framing is "CD-HIT and EDGAR are cousin methods, not the same method"; reporting the two counts as reproducing each other exactly would be dishonest.
- **How to close.** Re-run pan-genome analysis with Roary or Panaroo at matched identity thresholds; ideally re-run EDGAR itself if the free web tier permits the 41-genome job. Out of scope for the free-tool wave (~30 min compute budget).

## 2. T5SS: un-testable in the abricate/VFDB screen used
- **What happened.** VFDB's product annotations for the 4,592-sequence bundled DB do not label autotransporters as "type V secretion." The T5SS row in the secretion-system table shows 0/41, but that is annotation absence, not biological absence.
- **Root cause.** Annotation-scope gap in VFDB's product-label vocabulary vs the paper's secretion-system nomenclature.
- **What still worked.** 7 of 8 systems (T1SS/T2SS/T4P/flagellum conserved in 41/41; T3SS/T6SS/TAD variable) exactly reproduce the paper's call. C4 is 7/8, not 0/8.
- **How to close.** Run a dedicated autotransporter HMM screen — SecReT5, TXSScan_models (MacSyFinder profiles), or hand-curated Pfam profiles for the passenger + β-barrel domains — against the 41 assemblies. This is a straightforward next step, just not done in this wave.

## 3. C5 exact percentage: "~30% of genomes show substantial variation" not numerically matched
- **What happened.** I reproduce the direction (63.5% of VFDB genes are accessory; per-genome VF-load ranges 66-140) but the paper's exact "~30% of genomes" figure is a threshold + database choice I cannot reproduce without running the paper's specific CLC Genomic Workbench + VFDB-setB pipeline at E<1e-50.
- **Root cause.** Different DB scope (bundled VFDB vs setB) and different threshold conventions. The two screens are asking similar-but-not-identical questions.
- **What still worked.** The qualitative finding — wide variability in virulence-gene content across the 41 strains while core secretion systems stay conserved — is clearly reproduced.
- **How to close.** Obtain VFDB-setB explicitly (not just the abricate-bundled DB), re-screen at E<1e-50 in a BLAST-only pipeline, and re-report the per-genome variability fraction.

## 4. Phylogeny is a mash-distance dendrogram, not a MUSCLE + Neighbor-Joining tree on the core alignment
- **What happened.** The paper built its tree with MUSCLE core-genome alignment + NJ; this replication used mash sketch (s=100000) + all-vs-all k-mer distance + SciPy average-linkage.
- **Root cause.** Free/fast tool substitution for a heavier alignment-based pipeline.
- **What still worked.** The ML09-123↔TH0426 clade is robustly recovered, and this call is independently supported by fastANI (99.927%) and the Jaccard-1.000 VFDB profile. C1 does not depend on the tree topology beyond that clade.
- **Caveat.** The tree topology **outside** the ML/TH clade should not be over-interpreted — mash is an excellent proxy but not equivalent to a core-genome ML/NJ tree.
- **How to close.** Extract the 2834 core-gene clusters from Stage 6, align each with MAFFT, concatenate, run IQ-TREE ML with 1000 UFBoot replicates. A clean overnight job.

## 5. Un-scoped questions (not attempted; not gaps but honest limits)
The following are genuinely open — the 2018 paper did not resolve them, and this replication did not attempt them (see `open_questions.json` for the deeper framing + next-step protocols):
- **Host-of-isolation clustering** across the full NCBI corpus (1,927 A. veronii genomes today vs 41 in 2018 — a ~47× expansion).
- **Plasmid vs chromosomal location** of the variable T3SS/T6SS/TAD loci.
- **AMR / MDR carriage** — CARD/ResFinder screens were not run.
- **Bv. veronii vs bv. sobria** subspecies split monophyly.
- **Quorum-sensing regulator diversity** as a pathotype predictor.

## 6. Wave-scope acknowledgement
~30 minutes of compute on a single A100 node with free tools cannot substitute for the paper's full comparative-genomics pipeline. The correct claim shape is:
- The paper's **conclusions** are independently supported on real public data.
- The paper's **exact numbers** are reproduced where free tools permit (C1, C2, C3-core, C4) and honestly differ where they do not (C3-pan, C5 exact %).
- **No claim was contradicted.**

## 7. Operational failures during the wave itself
- **`argo:claude-opus-4.8` returned a transient 502** when submitting the LLM-judge bundle. Handled per the wave brief's free-endpoint rule: fell back to `argo:gpt-5.2` (also free); never paid. Recorded in REPORT.md §3.7 and §8.
- **NCBI Datasets Hm21 mismatch (0.082 Mb).** Not a failure — NCBI upgraded the Hm21 assembly to a complete genome (`GCF_000464515.2`) since 2018; the size delta is expected and does not indicate a resolution error.
- **No other tool crashes, timeouts, or data-integrity issues** encountered in the 9-stage pipeline.
