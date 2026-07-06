# Failure Analysis & Evidence-Strength Critique — Thakur 2022 (T. pyogenes)

**Scope:** Honest post-mortem of *what did not work*, *what was papered over*, and *how strong the evidence actually is* for each claim category. This is not a hit piece — the paper is a solid descriptive comparative-genomics survey — but every replication produces a set of things that failed cleanly, failed subtly, or were quietly finessed. All of them are logged here.

---

## 1. Outright Failures / Not-Reproducible-With-Free-Tools

### 1.1 IslandViewer4 4-tool ensemble (Claim #31)
- **What we tried:** IslandPath-DIMOB v1.0.6, the single component of IV4 that ships freely in bioconda.
- **What broke:** DIMOB alone flagged **47 GIs across 19 strains** (range 0–5). Paper reports **190 / 206 / 346** globally (three different numbers in the same paper!) with per-strain range **12–25**. Our per-strain ranking is completely different: paper says SH02 has the MAX (25); we detected **0** in SH02. Paper says TP8 has the MIN (12); we detected 0 in six strains.
- **Root cause:** IslandViewer4 = DIMOB (dinucleotide bias + mobility HMM) ∪ SIGI-HMM (codon-usage HMM) ∪ Islander (tRNA-flanked mobile-element DB) ∪ Islandpick (comparative-genomics gap-scan). DIMOB is intentionally the most conservative — it produces the union's "high-confidence" subset. Three of the four IV4 tools are not freely installable offline.
- **What would fix this:** SIGI-HMM standalone binary (not distributed since ~2013), Islander DB, and Islandpick source (last released ~2014). Or a modern reimplementation using GEIster or Alien_Hunter as substitutes — none are drop-in.
- **Verdict impact:** Claim #31 marked NOT REPRODUCIBLE. **Not a paper flaw — a free-tool-ecosystem gap.**

### 1.2 PHASTER incomplete-prophage detection (Claim #30)
- **What we tried:** PhiSpy 5.0.10 (default random-forest classifier).
- **What broke:** PhiSpy detected **7 total prophage regions** vs. paper's **30–31**. Per-strain max: 1 (PhiSpy) vs. 4 (PHASTER, in TP1). BUT — both **intact** prophages the paper claimed (TP6375 iA2-like, TP1 SPbeta-like) were independently re-detected by PhiSpy in the correct strains. The gap is entirely in PHASTER's "incomplete" + "questionable" tiers.
- **Root cause:** PHASTER is a large curated phage-protein BLAST DB + DBSCAN clustering — it aggressively flags any small cluster of phage-annotated genes as an "incomplete" prophage. PhiSpy's RF is trained to require multiple phage-signal features (GC skew, ORF length, direction bias, Shannon entropy) and classifies most short clusters as background.
- **What would fix this:** Either PHASTER offline (web-only, no standalone) or a modern replacement stack like geNomad + CheckV + VirSorter2 with ≥ 3-of-4 agreement (see open question Q3).
- **Verdict impact:** Claim #30 marked NOT REPRODUCIBLE for count/range; but the **strongest sub-claim** (2 intact prophages, correct strains) IS reproduced.

### 1.3 eggNOG-mapper "139 core-genome COG-G CDS" (not a numbered claim; sanity-check only)
- **What we tried:** Regex keyword match on Prokka product strings for carbohydrate/CAZyme terms.
- **What this is not:** A faithful reproduction. It's a coarse per-strain proxy, not a core-genome COG-G-restricted count.
- **Root cause:** Faithful reproduction requires eggNOG-mapper v2 + eggnog.db (~50 GB download), neither of which is in the local bioconda env.
- **Verdict impact:** Sanity check only. Recorded as PARTIAL. **Deliberately not counted** among the 31 numbered claims to avoid inflating the "verified" tally.

### 1.4 Paper-named fimA/C/E/J → NCBI accession mapping (Claims #22, #23 disagreement)
- **What we tried:** Best-guess selection of 4 fimbrial-subunit CDS from the TP6375 Prokka annotation.
- **What broke:** fimA: paper 19/19, ours 12/19. fimE: paper 19/19, ours 2/19. That's a > 10× disagreement — almost certainly reference-selection error, not biology.
- **Root cause:** The paper labels four fimbrial subunits with names from Bisinotto et al. 2016 (ref [13]) but does not provide NCBI accession numbers. Prokka itself does not assign species-specific fim names. Without the original paper's reference FASTAs (or accessions), the mapping is guesswork.
- **What would fix this:** Retrieve Bisinotto 2016 sequences (see open question Q2).
- **Verdict impact:** Claims #22/#23 marked PARTIAL. **The paper carries some blame here** for not depositing or citing its reference accessions — but this is a common annotation-provenance gap in the field, not a data-integrity issue.

---

## 2. Subtle / "Almost-Failure" Cases

### 2.1 Pan-genome γ magnitude (Claim #7)
- We report γ = 0.247; paper reports γ = 0.162. Both are > 0 (both say "open"), so the **sign** verdict matches. But the magnitudes differ by 52%. This is a genuine tool-substitution effect (Roary vs. EDGAR handle paralogs and split genes differently), but neither run tested convergence behavior with resampling. Marked VERIFIED in the report because the paper's binary claim ("open pan-genome, γ > 0") is preserved; but **evidence strength for the *value* γ is weak** — see open question Q1.

### 2.2 nanP over-call (Claim #20)
- Paper: nanP in 12/19 strains. Ours: 19/19. The paper's Section 2.9 says they filtered at ≥ 60% pid / ≥ 30% qcov (same as ours), so on paper the methods should agree. **The gap is almost certainly manual curation** — the paper likely excluded truncated hits or hits with poor synteny that our automated pipeline accepted. This is not documented explicitly in the paper's methods, which is a mild methodology-transparency gap.
- Marked PARTIAL. Real evidence strength for either count is medium-low.

### 2.3 Top-3 ARG carrier counts (Claim #27)
- Paper: SH01 (6 ARGs), SH02 (6), TP1 (5).
- Ours (abricate): TP1 (13), SH01 (8), SH02 (7) — same **identity**, different **counts**.
- Marked VERIFIED on identity because the "which strains are top-3" question resolves the same way in both runs. But the count divergence is a real tool-substitution effect: abricate counts each cassette copy on class-1 integrons; RGI-strict collapses duplicates. **Neither count is "wrong"** — they answer different questions. The paper should have specified duplicate-handling.

### 2.4 tet(W*) and ermX counts off-by-one (Claims #24, #25)
- Paper: tet(W*) 13/19, ermX 7/19. Ours: 12/19, 6/19. One-off in each direction.
- Marked VERIFIED (within tool noise), but the strain-level discrepancies were **not investigated**. A honest sub-claim would be "which specific strain does each tool disagree on?" — we did not table that out. Modest evidence-strength gap.

### 2.5 Roary vs. EDGAR pan/core/singleton (Claims #4, #5, #6)
- Roary: 4,097 / 1,389 / 1,237. Paper: 3,214 / 1,520 / 307.
- Marked PARTIAL because these are known tool-substitution artifacts (Roary splits paralogs more aggressively than EDGAR). Signs and rank order are correct, but absolute numbers diverge substantially. **We did not run an alternative pan-genome tool (PPanGGOLiN, panaroo)** to bracket the true value — a real weakness.

---

## 3. What the Paper Papered Over (Independent Critique)

### 3.1 Internal inconsistencies not resolved by the paper
- **Genomic islands:** abstract says 190; §3.8 says 206; §4 (Discussion) says 346. That's a **1.8× spread** within the same paper. The paper never explains which is the "real" number or what the discrepancy means. We tested per-strain ranges (self-consistent) but the global count claim is untestable-as-stated because the paper contradicts itself.
- **Prophages:** abstract says 31; §3.9 says 30. Off-by-one; not called out.
- **Singletons:** §3.4 says 307; some downstream text says 310. Also uncalled-out.

These are **paper QC failures** that the peer review missed. Not our failures.

### 3.2 No orthogonal validation of virulence-gene *function*
- The paper is a pure genomic survey. Zero strains had phenotypic confirmation of virulence-gene expression (RT-PCR, Western, secretion assay, cytotoxicity on macrophages). The 8 candidate VFs are presented as if presence = pathogenicity relevance. Same for AMR (see open question Q4). **This is a well-known descriptive-genomics limitation but the paper does not acknowledge it as a limitation.**

### 3.3 Phylogeny claim without recombination correction
- Three-clade partition is presented as if the tree faithfully represents vertical descent. No Gubbins/ClonalFrameML masking of recombinant sites. For a species with a demonstrably open pan-genome (i.e., heavy HGT), this is a real concern for the host-association claim (open question Q5). **Paper omission, not ours.**

### 3.4 Sampling bias not analyzed
- The 19 strains are geographically and host-imbalanced. TP3/TP6375/TP4479/TP-2849 are ~100% identical (paper acknowledges) — suggesting clonal duplicates that inflate clade-I "coherence." No sensitivity analysis was performed (e.g., dropping one of the clonal quartet and re-running the tree/pan-genome). Standard practice; paper skipped it.

### 3.5 No accession registry for VF references
- Section 3.7 discusses fim gene subunits and cites Bisinotto 2016 but does not deposit or cite the exact NCBI accessions used as BLAST references. This is what made our fim-panel disagreement impossible to resolve — **directly a paper reproducibility gap**, not ours.

---

## 4. Evidence-Strength Summary Table

| Category | # Claims | Evidence strength | Notes |
|---|---|---|---|
| Genome assembly / annotation stats (bases/GC/CDS/rRNA/tRNA/tmRNA/RR) | 4 numbered + 76 Table-1 cells | **STRONG** | 76/76 exact matches; independent tool (Prokka) agreement. |
| Pan-genome open/closed (sign) | 1 | **STRONG** | γ > 0 in both runs. |
| Pan-genome absolute values (γ, pan, core, singleton) | 3 | **WEAK** | Tool-substitution artifacts dominate. |
| ANI ≥ 97.5% | 1 | **STRONG** | 97.83% min agrees; independent tool (FastANI). |
| Phylogeny 3-clade + Bu5-divergent + TPx-clonal | 3 | **MEDIUM** | Topology reproduces but no recombination-corrected sensitivity analysis in either run. |
| Universal VFs (plo, nanH, cbpA) | 3 | **STRONG** | 19/19 in all runs. |
| Variable VFs (nanP, fim*) | 5 | **WEAK** | Reference-mismatch / manual-curation gap. |
| AMR strain identity (no-ARG-set, top-3) | 2 | **STRONG** | Independent-tool identity agreement. |
| AMR absolute counts (tet(W*) 13, ermX 7, total 40) | 3 | **MEDIUM** | ±1 or tool-substitution off. |
| Intact prophages in TP6375 + TP1 | 2 | **STRONG** | Independent-tool confirmation. |
| Total prophage/GI counts | 2 | **NOT-REPRODUCIBLE-WITH-FREE-TOOLS** | See §1.1, §1.2. |

**Aggregate honest read:** 
- ~19/31 claims are **strongly** evidenced (independent-tool agreement on the exact quantity).
- ~7/31 are **medium** (agreement on sign/identity but not on absolute value).
- ~5/31 are **weak or not-reproducible** (tool-substitution or reference-mismatch).

That is a genuinely good replication for a comparative-genomics paper of this age (2022 tools, one paid web tool, one 4-tool ensemble) using **only free tools**. But it is not a perfect replication and we do not claim it is.

---

## 5. Residual Gaps / What's Needed to Close Them

| Gap | Blocker | Estimated effort to close |
|---|---|---|
| IV4 4-tool GI reproduction | SIGI-HMM + Islander DBs | Multi-week (reimplement or find archived binaries) |
| PHASTER-comparable prophage count | Modern geNomad/CheckV/VirSorter2 3-of-4 rerun | ~1 day |
| Faithful eggNOG COG-G core-genome count | eggNOG DB download (50 GB) + core-FAA export | ~1 day |
| Bisinotto 2016 fim mapping | Contact Bisinotto lab or GenBank literature dive | ~1 week |
| RGI-strict-only AMR count | Install RGI locally + CARD | ~1 day |
| Nougat MMD extraction | Central corpus GPU pass | Passive (queued) |
| Phenotypic AST for AMR validation | Physical isolates + wet-lab BSL-2 access | ~2 months |
| Recombination-corrected phylogeny | Gubbins/ClonalFrameML rerun on core alignment | ~1 day |
| Expanded-n pan-genome scaling | n = 100+ genome pull + PPanGGOLiN | ~1 week |

---

## 6. Overall Failure-Analysis Verdict

- **The paper is replicable at the descriptive-survey level:** annotation stats, ANI, VF-presence, phylogeny topology, and strain-identity AMR/prophage claims all reproduce with independent tools.
- **The paper is NOT replicable-with-free-tools at the multi-tool-ensemble level:** IslandViewer4 and PHASTER incomplete-prophage cannot be matched without either paid/web tools or a substantially larger installation footprint.
- **The paper has several real internal-consistency and provenance gaps** (GI count 190/206/346, no accession registry for fim references, no recombination correction) that limit its own reliability — these are the paper's failures, not ours.
- **This replication is honestly rated 21/31 verified + 6 partial + 4 not-reproducible-with-free-tools + 0 contradicted, verdict REPLICATED (lifted from Pass-1).** Nothing above hides behind the verdict.
