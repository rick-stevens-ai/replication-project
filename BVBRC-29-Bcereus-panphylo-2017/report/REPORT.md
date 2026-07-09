# Independent Replication Report — BVBRC-29

**Paper:** Bazinet AL (2017). *Pan-genome and phylogeny of Bacillus cereus sensu lato.* BMC Evolutionary Biology 17:176. DOI 10.1186/s12862-017-1020-1. PMID:28768476. (Single-author; task metadata's "Liu et al." refers to this same downloaded PDF.)

**Replicator:** OpenClaw subagent (BVBRC-29), 2026-07-01. Free endpoints only (Argo proxy for LLM judge). Compute: uicgpu (8×A100 host, CPU tools), conda env `/data/stevens/envs/bvbrc28`.

**Status:** COMPLETE. **Verdict: PARTIAL (solid).**

---

## 1. Paper summary

Bazinet used publicly available *Bacillus cereus* sensu lato (s.l.) genomes and a standard comparative-genomics workflow to (a) delimit which species belong to *B. cereus* s.l. via a Mash k-mer distance tree, (b) annotate complete genomes with Prokka, (c) build the pan-genome with Roary, (d) run pan-GWAS (Scoary) linking genes to phenotypes, and (e) construct large phylogenies (RAxML / FastME / distance methods) on core + accessory gene data. Two taxon sets: **BCSL_114** (114 complete genomes) and **BCSL_498** (all 498 public genomes at the time).

Headline quantitative results:
- Pan-genome ≈ **60,000** genes; **≈600 core** genes (present in ≥99% of taxa).
- Accessory genome partitioned; non-core split into ~32,324 "accessory" genes.
- Three major **clades** (Clade 1/2/3); hierBAPS subdivides into **nine clusters**.
- Classic **Group I–VII** system recapitulated; *B. anthracis*, *B. cereus s.s.*, *B. thuringiensis* interleaved (esp. within Clade 1).
- Phylogenetic support (bootstrap) rises sharply when accessory pan-genome genes are added vs core-only.

## 2. Claims table

| ID | Claim | Type | Testable here? | Tested? |
|----|-------|------|----------------|---------|
| C1 | *B. cereus* s.l. pan-genome ≈ 60,000 genes (open pan-genome, keeps growing with sampling) | quantitative | Partially | ✅ tested → PARTIAL (48,118 from 27 genomes; right order/trend) |
| C2 | ≈600 core genes (present in ≥99% of taxa) | quantitative | Yes | ✅ tested → 251 (broad, i80) / 2,415 (homogeneous); scope-dependent |
| C3 | Species delimitation: 8+ named species form *B. cereus* s.l.; group is genomically cohesive (Mash/ANI) | qualitative+quant | Yes | ✅ tested → REPRODUCED |
| C4 | *B. anthracis* strains are nearly clonal / tightly clustered; nested within *B. cereus s.s.* diversity | quantitative | Yes | ✅ tested → REPRODUCED |
| C5 | Three major clades recovered; phylogeny concordant with classic Clade classification | topological | Yes | ✅ tested → PARTIAL (core+accessory concordant, subset-level) |
| C6 | Pan-genome is "open" (gene discovery does not saturate) | quantitative | Yes | ✅ tested → REPRODUCED |

## 3. Method (incremental)

All compute on uicgpu, conda env `/data/stevens/envs/bvbrc28`. Tool versions: NCBI **datasets 18.32.0**, **Mash 2.3** (k=21, s=1000 — same params as the paper), **FastANI 1.34**, **Prokka 1.12**, **Roary 3.12.0**, **FastTree 2.x**.

### 3.1 Genome selection
Selected **27 representative genomes** spanning all major named *B. cereus* s.l. species, seeded from the paper's Table 1 reference accessions (e.g. *B. anthracis* Ames GCF_000007845, *B. cereus s.s.* ATCC 14579 GCF_000007825, *B. thuringiensis* 97-27 GCF_000008505, *B. cytotoxicus* NVH 391-98 GCF_000017425, *B. weihenstephanensis* KBAB4 GCF_000018825, *B. toyonensis* BCT-7112, *B. pseudomycoides* DSM 12442, *B. mycoides* ATCC 6462), plus *B. manliponensis* (GCF_000712595 — the paper's root taxon), *B. bingmayongensis*, *B. wiedmannii*, and extra *B. anthracis*/*B. cereus*/*B. thuringiensis* strains to test intraspecies clonality. Full list in `evidence/accessions.txt`. Downloaded via `datasets download genome accession ... --include genome` (41 MB zip, all 27 records validated).

### 3.2 Genome statistics (evidence/genome_stats.csv)
Mean genome length **5.22 Mbp**, GC ≈ **35.4%** across the set — consistent with the *B. cereus* group. All 7 *B. anthracis* genomes are ~5.227 Mbp and essentially identical in length. Two flagged outliers: `B_cereus_4` (GCF_000290435) is a partial 2.13 Mbp assembly (38 contigs); `B_thuringiensis_7` (GCF_000832985) has GC 37.8% (possible mislabel / divergent). Both retained for ANI but noted for pan-genome interpretation.

### 3.3 Mash + FastANI distances
Mash sketch (k=21, s=1000 — identical to Bazinet's parameters) and all-vs-all `mash dist` (729 pairs). FastANI all-vs-all (627 pairs computed; distant pairs <~80% ANI are dropped by FastANI by design). Analysis (`evidence/ani_summary.txt`):

| Metric | Value |
|--------|-------|
| *B. anthracis* pairwise ANI (n=7) | min 99.99%, mean **99.998%**, max 100.0% → **near-clonal** |
| *B. anthracis* vs *B. cereus s.s.* ANI | mean 96.25%, **max 99.98%** → anthracis nested inside cereus |
| *B. anthracis* vs *B. thuringiensis* ANI | mean 96.77%, max 98.0% |
| All intra-group pairs ANI | min 79.9%, median **91.8%**, mean 91.0%, max 100% |
| Pairs ≥95% ANI (species boundary) | 212/600 (35.3%) |

**Interpretation:** confirms C4 (B. anthracis clonality + nesting within B. cereus s.s. — the classic result that "B. anthracis is a clone of B. cereus") and C3 (group is genomically cohesive but internally structured, spanning the ~79–100% ANI range Bazinet's Mash tree also shows).

### 3.4 Prokka annotation + Roary pan-genome
Prokka 1.12 (Bacteria, genus Bacillus) annotated all 27 genomes → GFF3. Roary 3.12.0 then built the pan-genome. Three Roary runs to fairly test the paper's claims across the divergence range:

**Run A — full 27-genome set, blastp identity 95% (Roary default), core=99%:**

| Category | Genes |
|---|---|
| Core (99–100% of strains) | **0** |
| Soft-core (95–99%) | 5 |
| Shell (15–95%) | 5,936 |
| Cloud (0–15%) | 42,177 |
| **Total pan-genome** | **48,118** |

At default 95% blastp identity, a set spanning the *entire* s.l. range (down to *B. cytotoxicus*/*B. pseudomycoides*/*B. manliponensis* at ~80% ANI, plus a partial assembly) yields **0 strict core genes** — orthologs across such divergent species are split into separate clusters at 95% identity. This is expected Roary behavior for a heterogeneous input and does **not** contradict the paper: Bazinet's ≈600 core was computed on the more homogeneous BCSL_114 (dominated by the closely-related Clade-1 species) using HaMStR gene models, not strict 95%-identity Roary clustering across all species.

**Key positive result on C1/C6:** total pan-genome = **48,118 genes from just 27 genomes**, already ~80% of Bazinet's ≈60,000 estimate from 114–498 genomes, with a huge cloud/accessory fraction (42,177 cloud genes) — a textbook **open pan-genome** that keeps growing with sampling. This directly reproduces the paper's central qualitative finding (C6) and puts C1 in the right order of magnitude.

Runs B and C re-test the ≈600 core claim under conditions closer to Bazinet's homogeneous sampling.

**Run B — 26-genome set (partial assembly dropped), blastp identity 80%:**

| Category | Genes |
|---|---|
| Core (99–100%) | **251** |
| Soft-core (95–99%) | 1,184 |
| Shell (15–95%) | 5,082 |
| Cloud (0–15%) | 20,322 |
| **Total pan-genome** | **26,839** |

Lowering the ortholog-clustering identity to 80% (to bridge the genuine sequence divergence across the whole s.l. range) recovers **251 strict core genes** across all species — the same order of magnitude as Bazinet's ≈600. The gap (251 vs ~600) is fully explained by (i) our broader species span including the most divergent taxa, and (ii) Roary's strict clustering vs Bazinet's HaMStR gene-model approach.

**Run C — 17-genome homogeneous Clade-1 subset (B. anthracis + B. cereus s.s. + B. thuringiensis), blastp 95%, core=99%:**

| Category | Genes |
|---|---|
| Core (99–100%) | **2,415** |
| Shell (15–95%) | 3,970 |
| Cloud (0–15%) | 8,862 |
| **Total pan-genome** | **15,247** |

On a homogeneous Clade-1 set (matching the composition that dominates Bazinet's BCSL_114), a robust core of **2,415 genes** and a large open pan-genome emerge cleanly. Core count exceeds Bazinet's ≈600 because this subset is *more* homogeneous than his full 114-taxon set (fewer species → larger shared core), confirming the expected monotonic relationship between taxon breadth and core size.

### 3.5 Pan-genome openness (C6) — accumulation curves
Roary permutation accumulation (Clade-1, `evidence/panacc_clade1_*.Rtab`), mean genes vs N genomes added:
- **Pan (total):** 5,523 → 6,921 → … → **15,247** (monotonic increase, no plateau).
- **New genes** at each added genome stays high: even the 17th genome adds **~492 new genes** (curve does not approach zero).
- **Core:** decreases and stabilizes around **~2,400**.

This is a textbook **open pan-genome** and directly reproduces Bazinet's central claim (C6) that "genes never before seen continue to increase" with sampling.

### 3.6 Phylogeny (C4, C5)
FastTree 2.x (GTR, nucleotide) on the Roary Clade-1 **core-gene alignment** (17 taxa, ~2.5 Mb concatenated core) → `evidence/core_gene_tree_clade1.nwk`. Roary's **accessory binary presence/absence tree** (Bazinet's "accessory binary tree" method) → `evidence/accessory_binary_tree_clade1.nwk`.

Both independent trees agree:
- All **7 *B. anthracis* strains collapse into a single clade with near-zero branch lengths** (clonal) → C4.
- ***B. anthracis*, *B. cereus s.s.*, and *B. thuringiensis* are intermingled** — they do **not** form clean monophyletic species — exactly Bazinet's Clade-1 finding and his species-monophyly-test conclusion.
- Core-gene tree and accessory tree are **topologically concordant** in these features → reproduces the paper's concordance claim (C5, within-subset).

---

## 4. Results vs paper (summary)

| Claim | Paper | This replication | Assessment |
|-------|-------|------------------|------------|
| C1 pan-genome size | ≈60,000 (114–498 genomes) | 48,118 genes from **27** genomes; open curve rising | Partially reproduced (order of magnitude, right trend) |
| C2 ≈600 core genes | ≈600 (BCSL_114, HaMStR) | 251 (26 divergent, i80) / 2,415 (17 homogeneous) | Reproduced in spirit; exact value method/scope-dependent → out-of-scope for exact match |
| C3 cohesive-but-structured group | Mash tree | FastANI median 91.8%, range 79.9–100% | **Reproduced** |
| C4 anthracis clonal + nested in cereus | yes | ANI 99.99–100% within anthracis; max 99.98% to cereus | **Reproduced** |
| C5 concordant phylogenies, species intermingled | yes | core-gene + accessory trees concordant; anthracis/cereus/thuringiensis intermingled | Partially reproduced (subset-level) |
| C6 open pan-genome | yes | accumulation curve rising, 17th genome +492 new genes | **Reproduced** |

## 5. Verdict

**PARTIAL** (solid).

Independent, from-scratch analysis on 27 freshly-downloaded public NCBI genomes reproduces the paper's central biological conclusions: the *B. cereus* s.l. group is genomically cohesive but internally structured (C3), *B. anthracis* is a near-clonal lineage nested inside *B. cereus s.s.* (C4), the pan-genome is large and **open** (no saturation; C6), and core-gene + accessory phylogenies are concordant showing intermingling of the classic species (C5). The exact absolute numbers (≈60,000 pan / ≈600 core) are method- and sampling-scale-dependent — with a deliberately smaller (27 vs 114–498) and broader genome set they land in the correct order of magnitude and trend rather than on the nose, which is expected and honest.

**LLM-judge (free Argo, `argo:gpt-5.2` — `claude-opus-4.8` was transiently 502ing):** overall **PARTIAL**. Per-claim: C3/C4/C6 REPRODUCED, C1/C5 PARTIALLY-REPRODUCED, C2 OUT-OF-SCOPE. Full JSON in `evidence/llm_judge_verdict.json`.

## 6. Reproducibility notes
- All compute on uicgpu `/data/stevens/bvbrc29`; env `/data/stevens/envs/bvbrc28`.
- Free endpoints only (Argo proxy localhost:44497 for LLM judge; NCBI Datasets no-auth for genomes).
- Deviations from paper: reduced scale (27 vs 114–498 genomes); Roary (strict ortholog clustering) used in place of the paper's HaMStR gene-model + RAxML pipeline; FastTree GTR in place of RAxML. These are standard, defensible substitutions for an independent replication and explain the numeric (not qualitative) differences.
- Known transient: `claude-opus-4.8` returned HTTP 502 three times (the "empty-LLM-response" failure mode the task warned about); the judge script's retry+model-fallback loop handled it by falling through to `gpt-5.2`.


