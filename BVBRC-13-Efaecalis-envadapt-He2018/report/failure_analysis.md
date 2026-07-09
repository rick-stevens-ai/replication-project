# Failure Analysis — BVBRC-13 (He 2018, *E. faecalis*)

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-13-Efaecalis-envadapt-He2018`
**Verdict:** PARTIAL replication (Coverage 6/10, Agreement 7/10).
**Purpose of this doc:** name each failure precisely, diagnose the root cause without spin, and give the specific fix (free tools only).

---

## Summary of failure modes

| # | Failure | Impact on paper claims | Severity | Fixable in-directory? |
|---|---|---|---|---|
| F1 | Corrupt phylogenetic tree (`core_tree.nwk` is a FastTree stderr log) | C8 (4 clades A/B/C/D) unverifiable | **HIGH** — blocks headline figure | ✅ yes, seconds of runtime |
| F2 | Scoary pan-GWAS never run | C9 (293 niche-associated genes — paper's central biological claim) | **HIGH** — biological centerpiece missing | ✅ yes, matrix + labels already staged |
| F3 | Pan-genome over-fragmented (13,255 vs 10,573; +25 %) | C6 wrong; propagates into every accessory/novel-gene count | **MEDIUM** | ⚠️ requires re-cluster and preserving params |
| F4 | VF count systematically low (mean 20.0 vs 23.8; 37 vs 60 unique; V583 34 vs 52) | C13, C14 undercounted | **MEDIUM** | ✅ yes, refetch VFDB setB and re-BLAST |
| F5 | PHASTER prophage stage entirely absent | C15 (116 intact prophages in 65 genomes) untestable | **MEDIUM** | ⚠️ requires fetching 78 nucleotide assemblies first (not in-directory) |
| F6 | Merz96 is not *E. faecalis* (5.21 Mb, 41.2 % GC) but was kept in AR/VF tables | Silent contamination of any niche/clade tabulation | **MEDIUM** | ✅ drop or replace; N=77 rerun |
| F7 | ORF count per genome never recomputed | C5 (2884 ± 211 ORFs) unaudited | LOW | ✅ trivial: `grep -c '^>' *.faa` |
| F8 | `scripts/` directory empty | Pipeline is not runnable; parameters lost | LOW–MEDIUM (reproducibility hazard) | ⚠️ archaeology needed to reconstruct |
| F9 | Gubbins recombination filter missing | Paper's Methods explicitly used Gubbins pre-phylogeny | LOW–MEDIUM | ✅ yes, once alignment method reconstructed |
| F10 | RAST 2.0 / COG functional annotation missing | Blocks functional-category enrichment analysis | LOW | ✅ RAST-tk + COGclassifier are free |

---

## Detailed diagnoses

### F1 — Corrupt phylogenetic tree
**File:** `results/phylogeny/core_tree.nwk` (939 B).
**What went wrong:** File contains only FastTree's stderr log — version banner, alignment path, iteration parameters, NNI/SPR timings. Content has 2 parentheses, 23 commas, and no terminal `;`. This is not a Newick tree.
**Root cause (single-writer error):** The FastTree invocation redirected stderr instead of stdout. FastTree emits the tree on stdout and progress on stderr — invoking `FastTree ... 2> core_tree.nwk` (or missing the `>` entirely) produces exactly this artifact.
**Fix:** `FastTree -gtr -nt results/phylogeny/core_concat_100.fasta > results/phylogeny/core_tree.nwk` (input MSA already staged, 78 seqs).
**Prevention:** In `scripts/04_align_tree.sh`, use explicit `1>tree.nwk 2>fasttree.log` and add a post-hoc validity check (`grep -c ');' tree.nwk` must equal 1).

### F2 — Scoary pan-GWAS never run
**Impact:** This IS the paper's biological centerpiece. He 2018 leads with the 293-gene niche-associated set (143 blood / 66 dairy / 84 water). Without it, we have not replicated the paper's actual biological finding — only its scaffold.
**Why it's fixable in-directory:** the two required inputs already exist and are the right shape:
  - `results/pangenome/presence_absence.tsv` (78 × 13,255) → Scoary's `-g` argument.
  - `results/card/ar_summary.tsv` contains niche labels → one-hot-encode into a `traits.tsv` → Scoary's `-t` argument.
**Fix:** `scoary -g presence_absence.tsv -t traits.tsv -n core_tree.nwk -p 0.05 --collapse -e 1000`. Requires F1 fixed first (Scoary needs the tree for phylogeny correction).
**Caveat:** Scoary's built-in correction is basic. A stronger follow-up (see `open_questions.json` Q1) uses treeWAS or pyseer with a proper kinship matrix, because the 78-strain niche panel is not niche-balanced.

### F3 — Pan-genome over-fragmentation (+25 %)
**Numbers:** 13,255 CD-HIT clusters vs paper's 10,573 SiLiX 80/80 families.
**Root cause candidates (parameters not preserved because `scripts/` is empty):**
  1. CD-HIT identity threshold set too strict (e.g. `-c 0.90` or higher instead of 0.80).
  2. Missing alignment-length coverage filter (default CD-HIT allows short partial matches to found new clusters; SiLiX 80/80 requires 80 % length coverage).
  3. Combined effect.
**Consequence:** every downstream "accessory" and "unique" gene count inherits the +25 % inflation. Not directly falsifying the paper's claim, but silent bias in the same direction.
**Fix:** rerun with either SiLiX 80/80 (preferred, matches paper) or CD-HIT `-c 0.80 -aS 0.80 -aL 0.80 -n 5`. Preserve the command line in `scripts/03_pangenome.sh` this time.

### F4 — VF undercount (setA vs setB)
**Numbers:** mean 20.0 vs paper 23.8; 37 unique labels vs paper 60; V583 = 34 vs paper 52.
**Root cause (unambiguous):** `data/databases/` contains `VFDB_setA_pro.fas` (curated core VFs) but the paper used the full setB (curated + predicted/hypothetical). SetB includes many predicted VFs specific to well-characterized clinical strains like V583 — hence V583's particular undercount (52 → 34).
**Fix:** fetch `VFDB_setB_pro.fas` and re-BLAST with the paper's thresholds (E<1e-15, ≥95 % identity). Alternatively, keep setA and declare the VF numbers as a strict, curated lower bound in the report.
**Judgment call:** setB includes putative VFs based on homology that may not be functionally validated. For a rigorous replication of the paper, use setB. For a rigorous *biological* claim, setA is defensible but requires an explicit caveat.

### F5 — PHASTER prophage stage absent
**Blocker:** PHASTER requires nucleotide assemblies (`.fna`), but `data/` only contains proteomes (`.faa`). This is an ingest gap, not a runtime gap.
**Fix:** fetch 78 nucleotide assemblies from NCBI (accessions inferrable from strain names in `ar_summary.tsv`), stage as `data/genomes/*.fna`, then batch-submit to PHASTER (or use PHASTEST for higher-throughput free processing, or Phigaro / VirSorter2 as fully-local alternatives).
**Effort:** ~200 MB download, ~1 hour of PHASTER batch time, ~30 min to tabulate.

### F6 — Merz96 contamination
**Evidence:** `Merz96.faa` genome = 5.21 Mb / 41.2 % GC. Every other strain is 2.67–3.26 Mb / 36.99–38.03 % GC. This is far outside the *E. faecalis* envelope — almost certainly an *E. faecium* misfetch or a contaminated draft.
**Current handling:** excluded only from the size/GC mean footnote in the audit table (C3). Still present in AR (Classic_AR = 16, second-highest) and VF (23) tables. Would silently distort any niche/clade cross-tab.
**Fix:** verify the correct NCBI accession for E. faecalis strain "Merz96"; refetch and rebuild proteome, or drop the strain and rerun pangenome / core / AR / VF on N=77.
**Prevention:** add a QC gate in `scripts/02_qc.sh` that rejects any strain with genome size or GC more than 3σ from the panel mean.

### F7 — ORF count unaudited (C5)
**Trivially closeable:** `for f in data/proteins/*.faa; do echo -e "$(basename $f .faa)\t$(grep -c '^>' $f)"; done > orf_counts.tsv`, then mean / SD.
**Left open because:** low priority — nothing hinges on this if strain panel and genome sizes match.

### F8 — Empty `scripts/`
**Root cause:** pipeline was executed but never version-controlled or preserved as runnable code.
**Impact:** every parameter (CD-HIT thresholds, BLAST E-values, MSA method, FastTree invocation, VFDB setA vs setB decision) is now lost. Blockers F3 and F4 are direct consequences.
**Fix (future work):** capture each stage as a shell script under `scripts/` (see `workflow.md` runbook). This is the highest-leverage fix for future replicability even though its immediate impact is low.

### F9 — Gubbins missing
**Paper's Methods explicitly used Gubbins** to filter recombination from the core alignment before phylogeny. Our staged concatenated alignments do not appear to be Gubbins-filtered (no `.gubbins.*` files present).
**Fix:** `run_gubbins.py results/phylogeny/core_concat_full.fasta --prefix results/phylogeny/core_gubbins`. Downstream: rerun FastTree on the Gubbins-filtered alignment for a fair comparison with the paper's tree.

### F10 — RAST 2.0 / COG missing
**Paper used RAST 2.0 + COG for functional-category enrichment** (their Fig. 4). Not staged here.
**Fix:** RAST-tk (SEED-based, free CLI) or Prokka + COGclassifier. Neither requires paid infrastructure.

---

## Meta-lesson (single most important)

**Preserve command lines with outputs.** Of the ten failures above, at least four (F3, F4, F6, F9) exist or are ambiguous specifically because `scripts/` is empty and the invocations that produced the artifacts were not captured. In any future replication run, `scripts/` should be treated as a first-class deliverable, on the same footing as `results/`. Every stage in `workflow.md` should be checked in as a runnable script so that (a) parameter drift is visible, (b) discrepancies with the paper have a specific line of code to critique, and (c) a re-run of the pipeline is a single command rather than an archaeology project.

---

## Two-day cleanup priority order (dependency-driven)

1. **F1 fix** (seconds): rebuild FastTree Newick → unblocks C8 and F2.
2. **F6 fix** (minutes): drop Merz96 or replace → clean AR/VF tables.
3. **F2 fix** (~1 hour): Scoary pan-GWAS with the fixed tree → tests C9.
4. **F4 fix** (~1 hour): re-BLAST VFDB setB → closes C13/C14.
5. **F3 fix** (~1 hour): SiLiX-equivalent 80/80 pan-genome → closes C6, likely reduces downstream noise.
6. **F5 fix** (~1 day): fetch nucleotide assemblies + PHASTER → closes C15.
7. **F8 fix** (ongoing): preserve every command line above as `scripts/NN_stage.sh`.
8. **F9, F10, F7** (optional): Gubbins, RAST/COG, ORF count — polish, not blockers.

Estimated total effort to move Verdict from PARTIAL → COMPLETE: **1–2 days of focused work**, all with free tools already available.
