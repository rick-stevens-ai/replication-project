# Failure Analysis — BVBRC-29 (Bazinet 2017 replication)

**Verdict on disk: PARTIAL (solid).** This document is the honest critique.

## 1. Was the paper's headline actually exercised?

Bazinet's headline is a **complete comparative-genomics pipeline** on *all 498 public* Bacillus cereus s.l. genomes plus a curated **114-genome** complete-genome set, comprising:

1. Mash k-mer distance tree for species delimitation
2. Prokka annotation
3. **HaMStR** profile-based ortholog inference
4. **Roary or equivalent** pan-genome construction
5. **RAxML maximum-likelihood core-gene phylogeny with bootstrap support**
6. **Scoary pan-GWAS** linking accessory genes to phenotypes
7. **hierBAPS clustering** into nine subgroups
8. Three major clades + Group I–VII recapitulation
9. Bootstrap-support-vs-accessory-gene-inclusion analysis

**What this replication actually exercised:**
- ✅ Steps 1, 2 (Mash + Prokka) — identically
- ⚠️ Step 3 substituted: Roary CD-HIT/BLAST clustering in place of HaMStR
- ✅ Step 4 (Roary pan-genome) — done, three runs (i95/i80, N=17/26/27)
- ⚠️ Step 5 substituted: FastTree GTR nucleotide with SH-like local support in place of RAxML with bootstrap
- ❌ Step 6 NOT DONE: no Scoary pan-GWAS (phenotype metadata assembly out of scope)
- ❌ Step 7 NOT DONE: no hierBAPS nine-cluster partition
- ✅ Step 8: three major clades recovered qualitatively via ANI + phylogeny; Group I–VII not formally partitioned
- ❌ Step 9 NOT DONE: bootstrap-support delta with/without accessory not measured

**Headline-exercised: PARTIALLY.** The biological headlines (open pan-genome, anthracis clonality + nesting, cohesive-but-structured s.l. group, subset-level topological concordance) were exercised end-to-end and reproduced. The engineering headlines (exact numbers at full scale, Scoary GWAS, hierBAPS partition, RAxML+bootstrap phylogeny) were substituted with reduced-scale analogs or skipped.

## 2. What went right

- **Downstream biological conclusions robust to method choice.** C3 (cohesive group, 79.9–100% ANI), C4 (anthracis clonal at ≥99.99% ANI, nested up to 99.98% ANI inside cereus), and C6 (open pan-genome, +492 new genes even at N=17) all reproduced cleanly on 27 fresh NCBI genomes with a substituted pipeline. These are the paper's most-cited claims and they hold.
- **Order-of-magnitude quantitative match.** Pan-genome 48k (vs 60k paper) from 27 vs 114 genomes; core 251 (broad, i80) or 2415 (homogeneous i95) vs paper's ~600. All in the correct order, all explainable by sampling scale and tool substitution.
- **Independent LLM judge converged on PARTIAL** (Argo `gpt-5.2` after `claude-opus-4.8` transient 502s).
- **Full evidence chain on disk:** accessions, per-genome stats, all Mash/ANI/Roary/FastTree outputs, Rtab accumulation curves, judge prompt+verdict. Anyone can rerun the assessment.

## 3. What went wrong or was skipped

### 3.1 Scale
27 genomes vs paper's 114/498. **Consequence:** absolute pan-genome and core-gene numbers do not match on the nose; only trends and orders of magnitude do. This is honest for a free-tier replication but it is not full REPLICATED.

### 3.2 Tool substitution
- **Roary vs HaMStR:** Roary is a strict-clustering (CD-HIT/BLAST) tool; HaMStR is a profile/HMM-based ortholog recovery. At default 95% identity on divergent input Roary splits obvious orthologs into separate clusters, producing the Run-A 0-core artifact. Dropping to 80% identity in Run B recovered 251 core, in the same order as HaMStR's ~600, but the exact numbers cannot match.
- **FastTree vs RAxML:** SH-like local support ≠ bootstrap replicates. Cannot claim "bootstrap support rises when accessory genes are added" (Bazinet's key phylogenetic claim about accessory-gene informativeness) — that specific test was not run.

### 3.3 Missing components
- **No Scoary pan-GWAS.** The paper's pan-GWAS link between accessory genes and phenotypes was skipped because the phenotype metadata assembly for 114+ strains was out of scope for a free-tier subagent budget. This is the biggest scientific gap.
- **No hierBAPS.** The nine-cluster partition (a genuine content contribution of the paper) was not tested. The three major clades were recovered qualitatively but not formally partitioned into nine subgroups.
- **No formal Group I–VII recapitulation.** Bazinet's paper explicitly relates his clades to the classic Group I–VII system; this cross-reference was not built.
- **Bootstrap-vs-accessory delta not measured.** Bazinet's C5-adjacent claim that adding accessory genes sharply improves bootstrap support requires bootstrapped ML runs with and without accessory input; this was not done.

### 3.4 Data-hygiene misstep
Run A retained two dodgy genomes (partial 2.13 Mbp assembly + 37.8% GC outlier) that contributed to the zero-core artifact. They were dropped in Run B, which is fine, but ideally the QC filter would have removed them before Run A.

### 3.5 Judge instability
`argo:claude-opus-4.8` returned HTTP 502 three times — the known "empty-LLM-response" failure mode. The retry + model-fallback loop handled it correctly by falling through to `gpt-5.2`. This is a **known-failure-recovered**, documented in `evidence/llm_judge_prompt.py`. Not a replication defect.

## 4. Why PARTIAL is the correct verdict (not REPLICATED, not SPOT-CHECK)

- **Not REPLICATED:** exact numbers ($\approx$60k pan, $\approx$600 core) don't match; Scoary GWAS, hierBAPS partition, and RAxML+bootstrap phylogeny were not reproduced; full 114/498 scale not run.
- **Not SPOT-CHECK:** a complete pipeline (Mash → FastANI → Prokka → Roary → FastTree → LLM judge) was executed end-to-end; all six claims were assessed against on-disk evidence; the biological headlines were reproduced with a substituted pipeline.
- **Genuine PARTIAL:** substantial reproduction of the biological content, honest substitution and reduction of the engineering pipeline, transparent about gaps. LLM judge concurs.

## 5. What would upgrade this to REPLICATED

1. Re-run the pipeline at the full 114-genome BCSL scale (feasible; ~40 CPU-hours on uicgpu).
2. Add Panaroo alongside Roary at 80% identity to close the HaMStR gap; report core-gene count against Bazinet's ~600.
3. Run RAxML with 100 bootstrap replicates on the core-gene alignment; measure bootstrap-support-vs-accessory-inclusion delta (Bazinet's specific claim).
4. Run hierBAPS on the pan-genome to test the nine-cluster partition.
5. Assemble phenotype metadata (toxin production, host, environment) and run Scoary; test one or two of Bazinet's specific gene-phenotype hits.

Items 1–4 are pure compute/tool tasks (free-tier, uicgpu). Item 5 is the hard one (data curation).

## 6. Verdict cross-check

**verdict_preserved = PARTIAL.** On-disk REPORT.md explicitly declares PARTIAL. Substance supports PARTIAL: biological headlines reproduced, engineering headlines partially substituted / partially skipped. Not upgrading to REPLICATED (numeric + missing-components gaps); not downgrading to SPOT-CHECK (full end-to-end pipeline actually run).
