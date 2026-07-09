# Workflow: BVBRC-56 Liu et al. (2013) *E. cloacae* Comparative Genomics Replication

**Paper:** Liu WY et al. *PLoS ONE* 8(9):e74487 (2013). DOI: 10.1371/journal.pone.0074487
**Set ID:** BVBRC-56 · **Verdict:** PARTIAL · **Analyst:** Ollie (OpenClaw AI)
**Compute host:** uicgpu (8×A100 node) · **Conda env:** `bvbrc56`
**Replication date:** 2026-07-02

---

## 0. Environment

- **Host:** uicgpu (Argonne CELS, 8×A100 node)
- **Env:** conda env `bvbrc56` — DIAMOND, NCBI BLAST+, MAFFT, FastTree, ncbi-datasets-cli, Biopython
- **Auth constraints:** free/no-auth only — used `efetch` for NCBI nuccore + Europe PMC full-text XML for paper text; no BV-BRC private/GUI steps
- **Scoring model:** free-Argo `gpt-5.2` LLM judge (per standing Rick policy)

---

## Step 1 — Paper acquisition
- Full text via Europe PMC XML (open access, CC BY, PMC3771936).
- Extracted claim table (11 claims C1–C11) directly from paper sections + Table 1.

## Step 2 — Genome acquisition
- All 11 comparator genomes **re-downloaded from NCBI nuccore by GenBank accession** using `efetch` (free, no-auth, not the paid `pdf` tool).
- Set: 4 *E. cloacae* strains (ENHKU01 CP003737.1, ATCC13047, EcWSU1, SDM) + 4 other *Enterobacter* species + 3 *Pantoea* outgroups.

## Step 3 — Genome statistics (C1–C3)
- Parsed each `.gbk` file with Biopython.
- Extracted: total length, replicon count, chromosome vs plasmid classification (via source-feature `/plasmid` qualifier + description text), GC%, CDS count, tRNA count, rRNA count.
- rRNA operon count = rRNA-gene-count ÷ 3.
- Output: Table 1 reproduction — all CDS totals exact (4338/5518/4619/4542); GC range recomputed 54.54–55.07% vs paper 54.5–55.1%.

## Step 4 — Pan/core genome (C4–C5)
- Concatenated the 4 *E. cloacae* proteomes.
- **DIAMOND all-vs-all blastp**, e-value ≤ 1e-5.
- Kept reciprocal-best hits with ≥50% identity AND ≥70% coverage both ways.
- **Single-linkage clustering** on retained RBH edges.
- Core = clusters containing a gene from **all 4** strains → 3345 (vs paper's EDGAR 3540).
- Unique/singleton = clusters found in exactly 1 strain → 7.8/7.1/13.3/19.8% (ENHKU01/SDM/EcWSU1/ATCC13047).
- Pan-genome cluster total: 6642.

## Step 5 — Functional feature calling (C8–C10)
- Keyword search over GenBank `product` / `gene` annotation strings.
- **Fimbriae:** matched `fimbrial | pilus | usher | chaperone`, clustered by genomic adjacency.
- **T6SS:** matched core component families ClpV/TssH, Hcp, VgrG, Vip/Imp/Vas/Tss; bona-fide cluster requires **≥6 contiguous** component genes.
- **Carbohydrate:** keyword net over metabolism-related product strings; count and % of genome.
- Result: T6SS ATCC13047=2 ✓ / SDM=1 ✓ / ENHKU01=1+fragment / EcWSU1=0; carbohydrate ~424–432 per strain (~8–10%) vs paper's 640+/13–15%.

## Step 6 — Phylogenomics (C6–C7)
- **AAI** (Average Amino-acid Identity) via DIAMOND reciprocal-best-hit protocol, ≥50% length coverage.
- All 55 pairs across 8 Enterobacter + 3 Pantoea genomes.
- **NJ tree** from (100 − AAI)/100 distance matrix (Biopython Phylo).
- Result: E. cloacae 4-strain clade AAI 93.6–94.0% ✓; Pantoea outgroup 72–73% AAI cleanly separates ✓; *E. aerogenes* falls basally near outgroup (consistent with its reclassification to *Klebsiella aerogenes*).

## Step 7 — Claim scoring
- Free-Argo **`gpt-5.2`** LLM judge given the full claim table + paper numbers + this-work numbers.
- Per-claim verdict: reproduced / partial / not / out-of-scope.
- Overall judge verdict: **PARTIAL** (concordant with human read).
- Never regex-scored.

## Step 8 — Report assembly
- REPORT.md — full narrative + tables.
- WAVE_RESULT one-liner for wave-level aggregation.

---

## Reproducibility notes

1. All raw inputs public (NCBI GenBank accessions; Europe PMC full-text). No paywalled steps.
2. Compute-host constraint: uicgpu 8×A100 was overkill for this workload (DIAMOND all-vs-all across ~50k proteins finished in minutes); a modest laptop with DIAMOND + Biopython would reproduce the same numbers.
3. **Methodology differences that the reader should keep in mind:**
   - Core-count methodology differs (this: DIAMOND RBH @ 50%id/70%cov single-linkage; paper: EDGAR BLAST-Score-Ratio). Expected ~5% shift.
   - Functional annotation: this uses NCBI GenBank product/gene keyword parsing; paper used RAST-SEED subsystems + manual IMG curation. RAST-SEED is materially broader on carbohydrate calls.
   - T6SS: paper manually re-curated with BLAST; this pipeline is automated (contiguous-cluster heuristic) and undercounts on 2/4 strains — a known limitation, not a data disagreement.

## Known gaps / suggested follow-ups

- Rerun core-genome with EDGAR BSR at the paper's exact cutoff to test the 3540 number directly.
- Deploy RAST-SEED subsystem-based carbohydrate call to close the 640 vs ~430 gap.
- Manual BLAST-reconfirm ENHKU01 and EcWSU1 T6SS candidates to match paper's manual-curation depth.
- C7 nearest-neighbor: replace 4-housekeeping-gene call with rMLST (53 ribosomal-protein loci) to see whether ATCC13047 still emerges as ENHKU01's closest relative.
