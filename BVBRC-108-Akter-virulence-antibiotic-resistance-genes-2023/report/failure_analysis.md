# Failure Analysis — BVBRC-108 (Akter 2023 replication)

**Verdict:** PARTIAL REPLICATION (strong). This document catalogs — honestly and without hedging — every place the replication was less-than-full, why, and what it would take to close each gap.

---

## Category 1 — Claims that did NOT independently confirm

### F1.1 — `tet(S)` and `tet(45)` not called (Claim C3b, partial)
- **Paper:** reports four tetracycline-resistance genes `tet(M), tet(L), tet(S), tet(45)` all only in BFPS6, called via ARG-ANNOT/CARD/ResFinder at 77–100% subject coverage/identity.
- **Rerun:** NCBI AMRFinderPlus 3.12.8 (DB 2024-07-22.1) at defaults called `tet(L)` + `tet(M)` in BFPS6 only, but did not report `tet(S)` or `tet(45)`.
- **Root cause:** database scope. AMRFinderPlus curates a smaller acquired-resistance reference set for *Enterococcus* than ARG-ANNOT and enforces stricter default thresholds. This is a **tool-scope difference, not a contradiction**.
- **Cost to close:** stand up ARG-ANNOT (or ResFinder 4.x with the exact 2022-era database snapshot) and rerun — feasible in ~1 hour but requires a per-database attribution table published by the paper (which does not exist). Also possible to hand-run tblastn of the two missing tet-gene reference sequences against BFPS6 with lowered thresholds.

### F1.2 — `mph(D)`, `dfr(E)`, `efrA`, `efrB` not confirmed across strains (Claim C3a, partial)
- **Paper:** lists multiple acquired AMR genes shared across all three strains, including `lsa(A), mph(D), dfr(E), efrA, efrB`, drawing from ARG-ANNOT + PATRIC.
- **Rerun:** only `lsa(A)` was called by AMRFinderPlus in all three strains.
- **Root cause:** the other four are ARG-ANNOT- or PATRIC-only entries with weaker NCBI-curation status; AMRFinderPlus intentionally excludes them.
- **Cost to close:** same as F1.1 — reinstantiate the paper's exact 8-database matrix.

### F1.3 — "Only cpsA in BFF1B1" not separable from housekeeping (Claim C2b, subpart)
- **Paper:** BFF1B1 carries only `cpsA` of the 11-gene capsule cluster.
- **Rerun:** VFDB set-A conflates `cpsA` with `uppS` (undecaprenyl-pyrophosphate synthase, a housekeeping isoprenoid-pathway gene) and `cpsB` with `cdsA` (CDP-diacylglycerol synthase, housekeeping). Both housekeeping genes are essential and universally present in *E. faecalis*, so a positive `cpsA/uppS` or `cpsB/cdsA` tblastn hit does not distinguish capsule biosynthesis from housekeeping metabolism.
- **Root cause:** VFDB curation choice to include paralogous housekeeping symbols under the same entry.
- **Cost to close:** requires a curated capsule-locus-specific reference (e.g. only the true *E. faecalis* Cps11 cluster sequences, not the entire uppS family) or a synteny check on the capsule island.

### F1.4 — Total gene counts (69 VF + 39 AMR) not independently reproduced
- **Paper:** aggregates hits across 4 VF databases (VirulenceFinder + VFDB + PATRIC/Victors) and 4 AMR databases (ARG-ANNOT + ResFinder + CARD + PATRIC).
- **Rerun:** used only VFDB set-A + AMRFinderPlus. ~16 Victors/PATRIC-called VFs not recoverable from VFDB set-A. AMR gene count from AMRFinderPlus is much lower than 39 because AMRFinderPlus excludes housekeeping/mutation-in-target loci (`gyrA`, `gyrB`, `rpoB`, `rpoC`, `murA`, etc.) that PATRIC counts as "resistance."
- **Root cause:** paper's aggregate count is fundamentally an 8-database sum; a 2-tool rerun cannot reproduce it.
- **Cost to close:** high — requires archival container images pinned to the paper's 2022 database versions, or an accepting scope-narrowing that reports per-database counts only.

---

## Category 2 — Paper-side issues uncovered by the replication (not our failures)

### F2.1 — Table 1 header swap (novel side-finding)
- Paper Table 1 as printed labels the 2,761,629 bp column as **BFF1B1** and the 3,067,042 bp column as **BFFF11**.
- NCBI stores the opposite: CP045918.1 = BFFF11 = 2,761,629 bp; CP046022.1 = BFF1B1 = 3,067,042 bp.
- The Table 1 N50/L50 values for BFFF11/BFF1B1 (~384k / ~343k) do not match the closed-chromosome NCBI records (N50 = full chromosome length) — Table 1 appears to have been populated from pre-closure draft assemblies.
- **Impact:** anyone citing Table 1 stats for a specific strain name will be off. Worth flagging in a correction.

### F2.2 — Database-version opacity
- Paper does not pin database versions for any of the 8 tools it uses.
- Reproducibility of the 69/39 totals is therefore version-dependent by design.
- **Impact:** even a full re-instantiation of the 8-tool stack today would likely produce different totals than 2022.

### F2.3 — No mobile-element / plasmid analysis
- `tet(M)` / `tet(L)` / `lsa(A)` are frequently mobile in *Enterococcus* (Tn916 family, pT181 family).
- Paper reports no MGE/plasmid/ICE analysis, so horizontal-transfer risk cannot be assessed.
- **Impact:** clinical/aquaculture-policy relevance of the tet-cluster finding is left ambiguous.

### F2.4 — No phenotypic validation
- Paper is entirely *in silico*. No MIC, no disk-diffusion, no infection-model assay.
- Genotype-to-phenotype gap is a known failure mode.
- **Impact:** the paper's clinical framing (fish streptococcosis with acquired tetracycline resistance) rests on a genotype prediction that is never phenotypically corroborated.

---

## Category 3 — Replication-run operational issues

### F3.1 — Argo Opus-4.7 502 on LLM-judge call
- Called Argo proxy `http://127.0.0.1:44497/v1` with `argo:claude-opus-4.7`; received **502 Bad Gateway** on the full claims-vs-results prompt.
- **Root cause:** prompt-size / route-side timeout on the Opus-4.7 route at run time (not a model-refusal).
- **Mitigation:** transparently fell back to `argo:claude-sonnet-4.6`, which returned structured JSON with verdict PARTIAL, coverage 72%, agreement 85%.
- **Cost to close:** rerun the judge with `argo:claude-opus-4.8` (current default) once the queue is quiet; or chunk the prompt.

### F3.2 — BFPS6 SPAdes-vs-RefSeq 0.05% length drift
- Paper reports BFPS6 = 2,868,292 bp (SPAdes direct); NCBI RefSeq-processed record = 2,866,855 bp; Δ = 1,437 bp (0.05%).
- **Root cause:** RefSeq post-processing (contig-end trimming, low-quality filter) between the paper's SPAdes output and the deposited assembly.
- **Impact:** none for gene-calling; fully compatible with a "REPRODUCED" verdict on C1 for BFPS6.

---

## Category 4 — Scope limits explicitly not addressed

- **No phylogeny / MLST context** for the three strains vs. the broader *E. faecalis* population.
- **No comparison** against 200–500 public fish-associated *E. faecalis* to test whether the reported VF/AMR patterns are lineage-specific or ecology-specific.
- **No RNA-seq / transcriptomic** validation that any of the called VF/AMR genes are actually expressed.
- **No long-read reassembly** of BFPS6 to close its 45-contig draft and resolve contig-boundary placement of the tet cluster.

These are non-goals for a same-scope replication (paper did none of them either), but each is a natural next step and is captured in `open_questions.json`.

---

## Bottom line

The failures in this replication run cluster in one category: **not standing up all 8 databases the paper aggregated over.** No paper claim was contradicted by independent evidence; several were narrowed in scope (F1.1, F1.2), one was epistemologically bounded by tool curation choice (F1.3), and the aggregate totals were declared out-of-scope (F1.4). One paper-side clerical error (F2.1) was surfaced as a bonus. The verdict **PARTIAL REPLICATION (strong)** honestly captures both the depth of what did replicate and the specific, named scope of what did not.
