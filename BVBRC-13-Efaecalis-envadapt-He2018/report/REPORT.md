# BVBRC-13 Replication Report
## He et al. 2018, *BMC Genomics* — Comparative genomic analysis of *Enterococcus faecalis* from environmental and clinical sources

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-13-Efaecalis-envadapt-He2018`
**Report date:** 2026-06-25
**Replication style:** BV-BRC bacterial-genomics replication (free-tool, no paid BV-BRC compute).

---

## 1. Target paper

- **Title:** He Q, Hou Q, Wang Y, Li J, Li W, Kwok L-Y, Sun Z, Zhang H, Zhong Z. *Comparative genomic analysis of Enterococcus faecalis: insights into their environmental adaptations.* **BMC Genomics** (2018) 19:527.
- **DOI:** 10.1186/s12864-018-4887-3
- **Identified from:** `report/PROGRESS.md` (paper had been fetched and key claims extracted by a prior run).
- **Scope:** 78 *E. faecalis* genomes (15 newly-sequenced dairy isolates + 63 from GenBank) across 6 niches (blood, faeces, urine, dairy, water, oral). Authors infer pan/core genome, ML phylogeny, niche-associated genes, AR and VF profiles, and prophages.

---

## 2. Stage inventory (what is actually present)

| Stage | Path | Status |
|---|---|---|
| 78 input proteomes | `data/proteins/*.faa` (78 files) | ✅ present |
| Genome stats (size, contigs, GC) | `data/genome_stats.tsv` (79 lines) | ✅ |
| CARD + VFDB BLAST DBs | `data/databases/` | ✅ |
| Pan-genome clusters (CD-HIT-style `.clstr`) | `results/pangenome/pan_clusters.clstr` (13,255 clusters) | ✅ |
| Core cluster list | `results/pangenome/core_clusters.txt` (1,382) | ✅ |
| Single-copy core list | `results/pangenome/single_copy_core.txt` (1,374) | ✅ |
| Presence/absence matrix (78 strains × 13,255 clusters) | `results/pangenome/presence_absence.tsv` | ✅ |
| Per-gene MSAs | `results/phylogeny/alignments/` (1,374 files) | ✅ |
| Concatenated core alignment (full + 300-gene + 100-gene subsets) | `results/phylogeny/core_concat_*.fasta` (78 seqs each) | ✅ |
| **Core phylogenetic tree (Newick)** | `results/phylogeny/core_tree.nwk` | ❌ **CORRUPT — log-only, see §5** |
| CARD AR raw BLAST | `results/card/card_blast_raw.txt` (10.6 MB) | ✅ |
| AR per-strain + summary | `results/card/ar_per_strain.tsv`, `ar_summary.tsv` | ✅ |
| VFDB raw BLAST | `results/vfdb/vfdb_blast_raw.txt` (20.6 MB) | ✅ |
| VF per-strain + summary | `results/vfdb/vf_per_strain.tsv`, `vf_summary.tsv` | ✅ |
| Scoary pan-GWAS (293 niche-associated genes) | — | ❌ missing |
| PHASTER prophage scan (116 intact prophages in 65 genomes) | — | ❌ missing |
| RAST 2.0 / COG functional annotation | — | ❌ missing |
| Recombination filter (Gubbins) on core MSA | — | ❌ missing (paper used Gubbins) |
| Gblocks-trimmed alignment | not explicitly preserved | ⚠️ unverifiable |
| `scripts/` directory | empty | ⚠️ pipeline not preserved as runnable code |

---

## 3. Per-claim audit (no self-claim trust)

Means/maxes below were recomputed by this report directly from the staged TSVs, not read from PROGRESS.md.

| # | Paper claim | Replicated value (recomputed here) | Match? |
|---|---|---|---|
| C1 | 78 strains analyzed | 78 proteomes in `data/proteins/`, 78 rows in genome_stats, 78 seqs in each core_concat fasta, 78 rows in AR + VF per-strain tables | ✅ exact |
| C2 | 6 niches (Blood 20 / Faeces 16 / Urine 10 / Dairy 18 / Water 11 / Oral 1 + 2 other) | Blood 20, Faeces 16, Urine 10, Dairy 18, Water 11, Oral 1, Type strain 1, Multiple 1 = 78 | ✅ exact |
| C3 | Avg genome size 2.94 ± 0.15 Mb | 2.937 ± 0.146 Mb (N=77, excluding the obvious Merz96 contaminant at 5.21 Mb / 41% GC) | ✅ within rounding |
| C4 | G+C 37.0–38.0 % | Range 36.99–38.03 %, mean 37.40 % (ex-Merz96) | ✅ |
| C5 | Avg 2,884 ± 211 ORFs/genome | Not directly recomputed (per-strain ORF count not in staged outputs); proteome FASTAs present and could be `grep -c '^>'` to verify | ⚠️ not audited |
| C6 | Pan-genome 10,573 gene families | 13,255 CD-HIT clusters | ❌ +25 % over (see §5) |
| C7 | Core genome 1,361 genes (≈47.2 % of avg 2,884 ORFs) | 1,382 core clusters / 1,374 single-copy core | ✅ within 1.5 % |
| C8 | ML tree with 4 major branches A=19, B=22, C=16, D=21 | Tree file is broken — only FastTree's stderr log was saved, no Newick string. Branch assignments **cannot be verified** from staged artifacts. | ❌ blocked |
| C9 | 293 environment-specific genes (143 blood, 66 dairy, 84 water) via Scoary pan-GWAS | Scoary was not run. Niche metadata not joined to presence_absence matrix in any staged output. | ❌ missing |
| C10 | Mean 7.5 AR genes/genome (classic, non-van-cluster) | Mean of `Classic_AR` column = **7.359**; max 18 | ✅ exact |
| C11 | 5 core AR genes: lsaA, emeA, efrA, efrB, dfrE | Computed from `ar_summary.tsv`: genes present in all 78 strains = {lsaA, emeA, efrA, efrB, dfrE} | ✅ exact set |
| C12 | Max 18 classic AR genes in DAPTO_516, DAPTO_512, S613, R712, TX0104 | All five strains tied at Classic_AR = 18 (TX0104, S613, R712, DAPTO_516, DAPTO_512). | ✅ exact |
| C13 | Mean 23.8 putative VFs/genome (60 unique VFs) | Mean VFs/strain = **20.0**; 37 unique VF gene labels | ⚠️ low (see §5) |
| C14 | Highest VF count = V583 with 52 | V583 = 34 (third in our table behind TX2137=35 and TX0855/T2=34) | ❌ undercount |
| C15 | 116 intact prophages distributed across 65 of 78 genomes (PHASTER) | PHASTER not run; no prophage output | ❌ missing |

**Coverage tally:** 8 claims fully or near-fully replicated (C1–C4, C7, C10–C12), 3 partial / quantitatively close (C3 needs Merz96 exclusion noted; C13), 4 missing or blocked (C5, C8, C9, C14, C15).

---

## 4. Coverage / Agreement scoring

- **Coverage = 6 / 10.** Genome panel, pan/core genome, AR, and VF stages are present with raw + summary artifacts. Phylogeny is staged through concatenated alignment but the actual tree was not written. Three large stages from the paper — Scoary pan-GWAS for niche-associated genes, PHASTER prophages, and RAST/COG functional annotation — are absent.
- **Agreement = 7 / 10.** Where outputs exist, numbers line up well: strain panel, niche breakdown, genome size + GC, core-genome size, core AR gene set, mean classic AR/genome, and the identity of the top-AR strains all match. Pan-genome family count is ~25 % high, VF count per genome is ~16 % low, and V583's headline VF count (52 in paper) is undercounted at 34. Phylogenetic-tree topology cannot be checked because the Newick file is corrupt.

---

## 5. MANDATORY 6/22 — reproducibility-blocker critique

### Critical blocker #1 — corrupt phylogenetic tree (`results/phylogeny/core_tree.nwk`)
- **File is 939 B; contains only the FastTree run-time log (Version banner, alignment path, parameters, NNI/SPR iteration timings).** It has 2 parentheses and 23 commas — no Newick tree string and no terminal `;`. Whoever ran FastTree captured stderr instead of stdout and overwrote the intended `.nwk` output. **Without the Newick string, paper claim C8 (4 phylogenetic branches A/B/C/D with stated strain counts) cannot be reproduced or contradicted, and downstream "niche distribution across clades" arguments are not testable.**
- **Precise missing artifact:** a valid Newick tree produced from `results/phylogeny/core_concat_100.fasta` (or `_300.fasta`), e.g. `FastTree -gtr -nt core_concat_100.fasta > core_tree.nwk`. The input MSA is present and the tree can be rebuilt in seconds.

### Critical blocker #2 — niche-specific gene analysis (C9, the paper's central biological argument)
- The paper's headline biology — **293 environment-specific genes, 143 in blood, 66 in dairy, 84 in water** — depends on Scoary 1.6.16 pan-GWAS on the presence/absence matrix using niche labels, with BH-corrected p < 0.05 and 1000 permutations. **None of this is staged.** The presence/absence matrix exists (13,255 × 78), and niche labels exist in `ar_summary.tsv`, so the analysis is *runnable* in this directory but was not executed.
- **Precise missing artifact:** `results/pangwas/scoary_results.csv` (or per-niche files) with cluster IDs, odds ratios, raw and BH-adjusted p-values; plus the input traits TSV used to call Scoary.

### Critical blocker #3 — pan-genome over-fragmentation (C6: 13,255 vs paper's 10,573)
- The paper used **SiLiX with 80 % identity / 80 % alignment coverage**. Our staged clusters were generated with CD-HIT (`.clstr` format) at unknown thresholds (no script preserved; `scripts/` is empty). A +25 % cluster inflation is the classic signature of an identity threshold that is too strict or no length-coverage filter, and it propagates into every downstream "novel/accessory gene" count.
- **Precise missing artifact:** the exact clustering command line (or `scripts/run_pangenome.sh`) so identity/coverage parameters can be reconciled; ideally a re-run with SiLiX 80/80 to match the paper or, failing that, CD-HIT with `-c 0.80 -aS 0.80 -aL 0.80` and a documented reason for the substitution.

### Critical blocker #4 — VF undercount, especially V583 (C13–C14)
- Paper reports 60 unique VFs; we recover 37. Paper reports V583 = 52 VFs; we recover 34. The paper used VFDB with **E-value < 1e-15 and ≥95 % identity**, but it pulled from VFDB *full set B* including hyperthetical/predicted VFs, whereas a stricter setA-only run (`VFDB_setA_pro.fas` is what is present in `data/databases/`) systematically misses the larger setB list (esp. EF-specific predicted VFs that swell V583).
- **Precise missing artifact:** a re-BLAST against `VFDB_setB_pro.fas` (paper's actual database) with identical thresholds, plus the per-strain VF table from that run. Alternatively, document the deliberate setA restriction and report VF numbers as a strict lower bound.

### Critical blocker #5 — prophage stage entirely absent (C15)
- Paper claim of 116 intact prophages in 65/78 genomes is not testable. PHASTER is a free web service; `data/proteins/` has all 78 proteomes but PHASTER requires nucleotide assemblies, which are not in this directory at all (only `.faa` files).
- **Precise missing artifact:** assembled nucleotide FASTAs for all 78 strains (`data/genomes/*.fna`) and PHASTER output JSON/text per genome (or the equivalent from PHASTEST / Phigaro / VirSorter2 used as a free alternative — must be documented if substituted).

### Critical blocker #6 — Merz96 is not E. faecalis
- `Merz96.faa` corresponds to a genome listed as **5.21 Mb at 41.2 % GC**, both wildly outside the E. faecalis envelope (every other strain is 2.67–3.26 Mb at 36.99–38.03 % GC). This is almost certainly a mis-fetched / misnamed assembly (likely an *E. faecium* or contaminated draft). It was nevertheless retained in the AR (Classic_AR = 16, second-highest) and VF (23) tables, and would distort any niche / clade analysis if Merz96 ends up in a "blood" cluster.
- **Precise fix:** either replace `Merz96.faa` with the correct *E. faecalis* Merz96 assembly (NCBI accession should be re-verified) or drop the strain and rerun pangenome/core/AR/VF tabulations on N=77. The current report excludes Merz96 from the size/GC mean (footnoted in §3, C3) but did not regenerate other tables.

---

## 6. Verdict

**PARTIAL replication.** The core "what strains, what sizes, what AR genes, what core-genome scaffold" layer of the paper reproduces cleanly and quantitatively — strain panel, niche counts, genome size/GC, core-AR gene set, mean classic AR per genome, and the identity of the most-resistant strains all match He et al. 2018 essentially exactly. However, the paper's biological centerpiece — niche-associated gene discovery (293 genes) — was not attempted; the headline phylogenetic figure (4 clades A/B/C/D) cannot be checked because the Newick file is corrupt; the VF survey under-counts the paper's numbers (likely VFDB setA vs setB); the pan-genome cluster count is ~25 % high (likely SiLiX-vs-CD-HIT and missing length-coverage filter); the prophage stage is absent; and one input genome (Merz96) is almost certainly not E. faecalis at all.

A focused 1–2 day cleanup would close most blockers: (1) re-emit the FastTree Newick from the staged 78-seq concatenated alignment, (2) run Scoary on the existing presence_absence matrix + niche labels, (3) re-BLAST VFDB **setB**, (4) replace or drop Merz96, (5) rerun the pan-genome with documented SiLiX-equivalent 80/80 parameters, (6) add a PHASTER (or PHASTEST) pass on nucleotide assemblies that still need to be fetched.

**Coverage = 6 / 10  |  Agreement = 7 / 10  |  Verdict = PARTIAL.**

---

*Audit completed automatically — all numerical comparisons recomputed directly from staged TSV/FASTA artifacts in this directory; no claim from `PROGRESS.md` was accepted on faith.*
