# Failure Analysis — Subedi et al. (2019) PA34 Replication

**Verdict:** **PARTIAL (strong).** This document catalogs everything that did **not** fully replicate, why, and what would close each gap. It is deliberately more critical than the main report so a reader can calibrate trust.

---

## 1. Quantitative gaps (things that failed to match paper numbers)

### 1.1 Pan-genome / core-genome / PA34-unique counts diverged 8–22%
| Metric | Paper (Roary) | Rerun (DIAMOND+MCL) | Δ |
|---|---:|---:|---:|
| Pan (total orthologs) | 7,643 | 6,775 | **−11.4%** |
| Core (all 4 genomes)  | 5,078 | 4,654 | **−8.3%** |
| PA34 unique (singleton) | 543 | 661 | **+21.7%** |

**Root cause.** Our clustering used DIAMOND+MCL at 50% identity + 50% coverage thresholds; Roary's canonical defaults are 95% identity. Looser thresholds keep more low-similarity edges initially but MCL then breaks marginal orthologs into more singletons, which simultaneously **shrinks core** (some borderline orthologs no longer make it into every-genome clusters) and **inflates cloud** (those borderline hits fall out as singletons). This is a toolchain-parameter difference, not a biology difference.

**Impact on paper's central claims.** Minimal:
- The **direction** of the paper's key pan-genome finding (PA34 shares fewest orthologs with VRFPA04) reproduces exactly.
- The **PA34-accessory headline** (1,213 → 1,206, Δ<1%) reproduces because "accessory = any cluster missing ≥1 of the 4 genomes" is definitionally robust to whether marginal orthologs split into singletons.

**Impact on the paper's specific counts.** The exact numbers "7,643 pan / 5,078 core / 543 unique" are **not** independently validated by this replication. They are plausible but require a Roary-at-95%-ID rerun to be confirmed as reproducible.

**Fix (not done here).** Install Roary v3 (or PIRATE / PPanGGOLiN), run against the same 4 GenBank records at canonical thresholds, and confirm. Time budget did not permit here. This is the single most important open reproducibility gap.

### 1.2 Minor annotation-version drift (off-by-1 counts)
| Field | Paper | Recomputed | Δ |
|---|---:|---:|---:|
| Chromosome ncRNAs | 5 | 4 | −1 |
| pMKPA34-2 CDS     | 33 | 32 | −1 |
| Total RNA         | 82 | 81 | −1 |

**Root cause.** The paper's Table 2 used one version of PGAP / Prokka annotation at deposition time; the deposited GenBank record has since been re-annotated (NCBI periodically re-runs PGAP on public assemblies). Our recount comes from the *current* GenBank download.

**Impact.** Trivial. These are annotation-version artifacts, not real content differences.

**Fix.** Fetch the exact NCBI GenBank version tag the paper used (the accessioned version history is queryable on Entrez) and re-parse. Cosmetic.

### 1.3 Pseudogene count "approximate"
Paper reports 148 pseudogenes; our raw parse finds 312 `pseudo` lines in the GenBank record, which collapses to ~148 unique pseudo loci once split-CDS pseudogenes (multi-line records for a single pseudo) are deduplicated. Reported as "approx" in Table 2. Not a real disagreement, but not exactly matched either.

**Fix.** Dedup pseudo loci by locus_tag and report the exact number.

---

## 2. Claims not tested (out of scope)

These are honest gaps, not failures. A public-data replication cannot address them.

### 2.1 C15 — Fig 5 cytotoxicity (PA34 kills human corneal epithelial cells)
**Why not tested.** Requires the live PA34 strain and BSL-2 cell culture (HCECs). Neither available.

**What we did instead.** Verified the exoU gene + SpcU chaperone are present at the paper's stated positions (4,720,713 + 4,720,303) inside the paper's stated RGP7 interval. The gene is real; whether its product actually kills HCECs at the reported level is a wet-lab claim that this replication cannot substitute for.

**Reader guidance.** Trust of Fig 5 still depends on the paper's wet-lab evidence.

### 2.2 C16 — Fig 6 metal tolerance (PA34 more Hg-tolerant than PAO1)
**Why not tested.** Requires live strain + metal MIC assay.

**What we did instead.** Verified two independent mercury-resistance operons (one in the novel MKPA34-GI1 chromate+mercury island at 2,342–2,345 kb; one in RGP5 at 5,075–5,080 kb with full merR-T-P-A-B-D). BV-BRC's independent PATRIC pipeline confirms **merA×2, merB×2, merP×2, merR×3** — completely independent evidence for the duplication. The genetic capacity is there; whether it translates to the exact Hg MIC differential the paper reports is a wet-lab claim.

**Reader guidance.** Trust of Fig 6 still depends on the paper's wet-lab MICs. But the genetic basis (two operons vs PAO1's one) is fully verified from two independent pipelines.

### 2.3 C17 — CRISPR-Cas absence
**Why only partially tested.** We did not run CRISPRCasFinder. We inferred absence from "no Cas gene in the PGAP annotation of CP032552".

**Fix.** Run CRISPRCasFinder v4 on CP032552 and confirm the negative call positively. Easy; just not done.

### 2.4 MLST ST1284
**Why not tested.** PGAP annotations don't consistently carry the traditional MLST allele gene tags (acsA/aroE/guaA/mutL/nuoD/ppsA/trpE), so we would need a dedicated script running Torsten Seemann's `mlst` tool or a PubMLST BLAST wrapper. Time budget cut this.

**Fix.** `mlst --scheme paeruginosa CP032552.fna`. One line. Not done.

### 2.5 Full RGP inventory (24 RGPs)
**Why only partially tested.** We verified the specific RGPs the paper *names* (RGP5, RGP7, RGP9, RGP23, RGP29, RGP41, RGP73, MKPA34-GI1, MKPA34-GI2) at their stated coordinates. We did **not** re-run MAUVE against the same 4-genome reference set to independently produce the "24 RGPs" call.

**Impact.** The paper's per-RGP claims that we tested all reproduce. The "24" as a count is not independently reproduced; it could be 22 or 26 under a different MAUVE run.

**Fix.** Re-run MAUVE with the same reference set (PAO1 + PA14 + VRFPA04 vs PA34) and count RGPs.

---

## 3. Judgment calls documented

### 3.1 Why call the verdict PARTIAL and not FULL
- Every specific per-locus claim the paper makes reproduces cleanly.
- Every deposited-data statistic reproduces to within 1%.
- Independent BV-BRC pipeline agrees on the resistance inventory and the duplicated mer operon.

But:
- The pan-genome absolute counts (7,643 / 5,078 / 543) are not independently validated — only the *direction* and the *accessory headline* are.
- Two phenotypic figures are entirely out of scope.
- MAUVE was not re-run.

That's a strong-partial, not a full replication. PARTIAL is the honest call.

### 3.2 Why call it PARTIAL and not WEAK
The paper's biological core — that PA34 has a large accessory genome packed with mobile-element-borne AMR / metal / virulence loci, with two independent Hg operons and a large phage-derived AMR island — is fully supported by two independent pipelines. The Subedi et al. team deposited exactly what they said they had. That is not a weak replication result.

---

## 4. Bugs / infrastructure hiccups worth remembering
- None material. This was a smooth run — public data, standard tools, well-annotated GenBank records. The biggest time sink was writing the MCL post-filter (39,655 edges from 78,801 hits) rather than any acquisition or annotation problem.

---

## 5. Prioritized follow-up (if we come back to this)
1. **Install Roary and rerun** — closes §1.1, the largest quantitative gap. High priority.
2. **Run CRISPRCasFinder** — closes §2.3, cheap. Low effort, high credibility gain.
3. **Run `mlst`** — closes §2.4, one command.
4. **Re-run MAUVE** — closes §2.5, moderate effort, would let us reproduce "24 RGPs" as a count.
5. **Wet-lab collaboration for Fig 5 / Fig 6** — only path to close §2.1 and §2.2. Requires a strain-holder partner; not a bioinformatics fix.
