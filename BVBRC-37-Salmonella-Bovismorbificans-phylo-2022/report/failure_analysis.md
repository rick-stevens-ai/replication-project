# Failure Analysis — BVBRC-37 / Gopinath 2022 Bovismorbificans

**Purpose:** An honest, unflattering catalog of what this replication did not do, where it took shortcuts, what could bite a re-runner or a peer reviewer, and what should be graded as "weakness of the evidence" versus "success worth trusting." Nothing here overturns the **REPLICATED** verdict — but everything here is a real limitation.

---

## 1. What was NOT reproduced (in-scope but not attempted)

### 1.1 The paper's actual custom methodology (C7)
- **2690-locus custom core-genome MLST schema** built from 150 complete Salmonella genomes — not rebuilt. Would require running chewBBACA (or equivalent) on the paper's exact seed set with the paper's own filtering criteria. Feasible; simply not done.
- **k-mer-binning survey of >260 strains** — not rerun. The paper's k, sketch parameters, and binning threshold were not extracted from the text with enough specificity for a byte-identical rerun.
- **Digital DNA tiling-array / SARA/SARB near-neighbor mining** — not rerun. This method depends on legacy microarray probe sequences that are not distributed as a drop-in modern artifact; a re-implementation would require reconstructing probe sequences from the paper's supplement (if listed) and BLASTing against modern Bovismorbificans assemblies.

**Consequence:** we replicated the paper's *biological conclusions* (two-lineage split, dominant STs, mixed sources, AMR/virulence classes) using an *independent* method (mash + hierarchical clustering, MLST, SeqSero2, AMRFinderPlus). We did *not* replicate the paper's *method*. A methods-reproducible verdict is stronger than a conclusions-reproducible verdict, and we're claiming the weaker one.

### 1.2 A proper phylogenetic tree
- No SNP-based reference-mapped alignment (snippy/Parsnp).
- No ML tree with bootstraps (RAxML-NG, IQ-TREE).
- No Bayesian tree (MrBayes, BEAST2).
- No branch supports at all for the ST150-vs-backbone split.
- No cluster-stability metrics (silhouette, gap statistic, prediction strength).
- No sensitivity analysis over linkage method (single/complete/Ward would each give somewhat different geometries) or over cluster count k.

The mash + average-linkage + 2-cluster cut recovers the paper's headline topology, but "topology recovered by a proxy method" is weaker evidence than "well-supported ML tree with high bootstrap on the deep branch."

### 1.3 Plasmid and prophage biology
- **Plasmid replicon typing** (mob-suite, PlasmidFinder) — not run.
- **pVirBov reconstruction per isolate** — not done. `spv` presence is called at gene level by AMRFinderPlus (56/82); we did not verify the intact `spvRABCD` operon, did not assemble the plasmid, did not check for rearrangements.
- **Prophage prediction** (PHASTER, VirSorter2) — not run. Paper discusses prophage content; we do not.

### 1.4 Isolate-by-isolate concordance
- AMR and virulence agreement is at the **feature-class level** (intrinsic efflux ubiquitous; acquired AMR sparse; `spv` in ~majority).
- We did **not** perform gene-by-gene, isolate-by-isolate cross-check against the paper's supplementary tables. Individual mismatches could exist and would not be visible in our summary tallies.

### 1.5 Numerical reconciliation
- We recovered **82** Bovismorbificans genomes; paper reports **81** newly-sequenced. Delta of 1.
- We report **70 clinical, 8 food**; paper reports **69 clinical, 9 food, 1 feed, 1 animal, 1 env** among the 81.
- These small deltas are almost certainly post-publication BioSample metadata edits or a Table-1-vs-BioProject accounting difference. We did NOT per-genome reconcile against paper Table 1 to prove that.

## 2. Known/likely limitations of the ones we DID reproduce

### 2.1 Serovar call has a mild circularity (C2)
SeqSero2 in k-mer mode is highly accurate for Bovismorbificans, but the input genomes were retrieved by filtering NCBI's organism annotation for "…serovar Bovismorbificans." 82/82 concordance therefore partly reflects consistency of NCBI's own metadata rather than a truly blind reconfirmation from raw reads. A cleaner test would draw a mixed Salmonella set and let SeqSero2 select the serovar.

### 2.2 ST150 "lineage" rests on n=2 (C4)
The separate lineage is only two genomes wide in our set. Two isolates is a weak evidentiary base for calling a lineage — one badly-assembled or contaminated genome and the branch inflates. The paper's own ST150 support draws on the broader custom-schema and microarray context we did not reconstruct.

### 2.3 Geography is Swiss-dominated (C5)
75/82 = Switzerland, 5 Canada, 2 USA. The two-lineage claim as we tested it is therefore really a claim about the paper's specific European + North American clinical-surveillance sample, not a global claim. Testing global generality would need a much broader Enterobase pull (see `open_questions.json` Q4).

## 3. Judge / verdict caveats

### 3.1 Single judge, not an ensemble
- Verdict scored by **one** LLM (`argo:gpt-5.2`, free tier).
- Intended first-choice judge was `argo:claude-opus-4.8` — returned HTTP 502 (known Argo proxy issue that day). We fell back to `gpt-5.2` and did not retry Opus later.
- No self-consistency vote (multiple runs, temperature > 0, majority-vote).
- No cross-model ensemble (e.g. gpt-5.2 + claude-opus + a Sophia model).
- No human adjudication.

### 3.2 Coverage estimate (≈ 0.92) is soft
- Not derived from a claim-by-claim a-priori rubric.
- Comes from the judge's holistic reading.
- Treat as ordinal ("high") not cardinal ("92%").

### 3.3 Judge saw a summarized evidence bundle, not raw artifacts
The judge scored a curated evidence bundle. It did not independently re-inspect the per-genome SeqSero2 or MLST tables. Sub-population noise not surfaced in the bundle would not have been detectable to the judge.

## 4. Provenance / reproducibility gaps

- **NCBI Datasets contents drift.** We did not archive the exact dataset snapshot; a rerun months later may pull 82 ± 2 genomes depending on GenBank edits.
- **AMRFinderPlus DB version pinned but not itself checksum-recorded** in the report. We noted `2024-07-22.1` but did not save a SHA-256 of the DB tarball.
- **Input FASTAs not hashed.** No SHA-256 manifest of the 82 assemblies. If BioProject accessions were re-uploaded (rare but possible), we would not detect it.
- **Random seeds.** Mash and SciPy hclust are deterministic, so no seed-management issue; but any bootstrapping (which we did not do) would need seeds.

## 5. PDF availability

- The paper itself is **open access, CC BY**, freely downloadable from MDPI and PMC (PMC9228720). No paywall barrier for a re-runner.
- The **replication report is provided as `REPORT.md` + `REPORT.tex`**. The compiled **`REPORT.pdf`** is NOT included in this backfill (this task was pure-write from `REPORT.md`); a re-runner can compile with `pdflatex REPORT.tex` in the report directory. No figures beyond `evidence/dendrogram.png` need to be embedded, and the `.tex` uses only standard packages (`geometry`, `booktabs`, `hyperref`, `longtable`, `xcolor`, `fancyvrb`).
- The paper's **Supplementary Materials** (Table 1 strain-by-strain metadata, custom schema locus list, k-mer-bin parameters, tiling-array probe sequences if any) were **not systematically re-extracted** into machine-readable form for this replication. That is the single biggest gap for anyone wanting to rerun the paper's own method rather than the biological conclusions.

## 6. Unrun manual analyses (candidates for future work)

- Bootstrapped ML core-genome tree (see `open_questions.json` Q1).
- Within-backbone sub-structure at k > 2 (Q2).
- Plasmid reconstruction and pVirBov architecture (Q3).
- Global Enterobase re-analysis (Q4).
- Reimplementation of the paper's own custom schema via chewBBACA (Q5).
- Prophage prediction and comparison across STs.
- Per-isolate AMR/virulence concordance against paper Supplementary Tables.
- Multi-judge ensemble re-scoring.
- Tip-dated Bayesian phylogeography (BEAST2) for the ST377 hummus-outbreak sub-clade.

## 7. Grading

| Dimension | Grade | Justification |
|---|---|---|
| Biological conclusions replicated | A− | All 5 directly-testable claims (C1–C5) reproduced on independent public data; C6 at feature-class level. |
| Method replicated | D | Paper's custom pipeline (C7) was not attempted; a proxy method was used. |
| Statistical rigor | C | Two-cluster cut without bootstraps or stability metrics. |
| Provenance / auditability | B− | Tool versions logged; DB version pinned; per-artifact hashes and snapshot pinning missing. |
| Verdict robustness | C+ | Single free-tier LLM judge, no ensemble, no human review. |
| Cost discipline | A | Zero paid endpoint use; all-free tool stack. |

**Overall:** the biological verdict (REPLICATED) is well-supported for the claims we tested; the verdict is *not* a statement that we independently re-implemented the paper's methodology or that we bootstrapped the phylogeny. Peer-review-level rigor requires the items in §6.
