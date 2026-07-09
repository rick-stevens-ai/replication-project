# Failure Analysis — BVBRC-28 (Gustaw 2021 *L. hilgardii* FLUB Pangenome)

**Verdict:** PARTIAL REPLICATION (strong; borderline REPLICATED).

This document catalogs what did **not** replicate, or replicated only partially, and diagnoses each gap. There are zero direction-reversing contradictions; every failure below is either a pipeline-substitution artifact, a service-availability gap, or an out-of-scope claim (wet-lab / non-computational).

---

## 1. Claim-by-claim failure map

| Claim | Status | Failure mode |
|---|---|---|
| C1 — genome size 3,190,226 bp / GC 40.09% / 6 replicons | ✅ EXACT | No failure. Every replicon matches Table 1 to the base pair. |
| C2 — 3043 genes / 2871 CDS / 79 RNA / 93 pseudogenes (PGAP+PATRIC) | ⚠ PARTIAL (numeric miss; qualitative preserved) | Pipeline substitution: Prokka replaces PGAP+PATRIC → ~4% CDS delta. |
| C3 — 4181 clusters, 49.3% core | ⚠ PARTIAL (bracketed) | Roary 4089 (48.9% core), mmseqs2 4190 (45.9% core). Paper sits between the two pipelines. |
| C4 — FLUB 266 singletons | ✅ NEAR-EXACT | 260–269 across three runs; no failure. |
| C5 — all pairs ≥97% ANI, FLUB↔ATCC 27305 99.909% | ⚠ MOSTLY MATCHED | fastANI 99.77% vs 99.909% (0.14 pp gap); two cross-clade pairs at 96.86–96.87% (0.13–0.14 pp under paper's floor). |
| C6 — dDDH d4 76.5% (FLUB↔ATCC 8290) | ❌ NOT DIRECTLY REPRODUCED | GGDC is a rate-limited web batch service, not free-scriptable locally. Substituted ANI as an indirect species-membership proxy. |
| CRISPR / prophage / genomic-island counts | ❌ NOT ATTEMPTED | Out of scope for this pass; separate services (CRISPRCasFinder, PHASTER, IslandViewer). |
| Wet-lab phenotypes (Bioscreen C ethanol/sugar tolerance, fructophily) | ❌ NOT ATTEMPTED | Non-computational; requires physical strain culture. |
| Functional identity of FLUB singletons (arsenic detox, surface-layer, metabolic cluster) | ❌ NOT VERIFIED | We reproduced the *count* (266 ≈ 268) but did not verify the *identity* of the singleton genes. |

---

## 2. Root-cause analysis of each miss

### 2.1 C2 — CDS count delta (~4%)
- **Symptom:** Prokka reports 2991 FLUB CDS vs. paper's 2871.
- **Root cause:** Different gene finder (Prodigal in Prokka vs. GeneMarkS-2/PGAP), different pseudogene handling (Prokka does not aggressively split into pseudogenes), different RNA models (Prokka Barrnap+Aragorn vs. PGAP's PGAP-specific RNA callers).
- **Not fixable without:** running PGAP itself (NCBI-hosted or Docker image), which is possible but was out of scope for the free-only stack.
- **Impact on verdict:** minor. Qualitative claim "FLUB has the most CDS of the set" reproduces.

### 2.2 C3 — Pangenome partition drift
- **Symptom:** Roary reports 4089 / 48.9% core; mmseqs2 reports 4190 / 45.9% core; paper reports 4181 / 49.3% core. Two pipelines *bracket* the paper.
- **Root cause A (annotation):** input CDS calls differ between Prokka (Roary input), Prodigal (mmseqs input), and the paper's PGAP+PATRIC combined annotation.
- **Root cause B (clustering algorithm):** Roary uses CD-HIT+BLASTP; mmseqs2 uses k-mer prefiltering + Smith-Waterman. Even at nominally identical 95% identity, edge-of-threshold cluster memberships differ.
- **Root cause C (strain-set drift):** 2026 RefSeq is not identical to 2020 RefSeq. ±2% cluster drift is expected.
- **Impact on verdict:** partition *shape* is reproduced (three-way core/accessory/singleton at ~46–49% / ~29–31% / ~22–23%). Numeric exactness is pipeline-sensitive.
- **Not fixable without:** exact re-run of the paper's PATRIC pipeline on the paper-era exact strain set.

### 2.3 C5 — ANI numeric gap (0.14 pp)
- **Symptom:** FLUB ↔ ATCC 27305 fastANI = 99.77%; paper reports 99.909%. Two cross-clade pairs come in at 96.86–96.87% (paper's stated floor is ≥97%).
- **Root cause:** the paper's ANI value likely came from an OrthoANI/JSpecies variant, not fastANI. fastANI uses a mash-based fragment approach that gives systematically slightly lower values (~0.1–0.3 pp lower typical) than alignment-based ANIm/ANIb/OrthoANI on the same input.
- **Impact on verdict:** no direction reversal; closest-neighbor structure preserved. Marginal pairs remain unambiguously conspecific (≥95% species threshold).
- **Not fixable without:** running OrthoANI-USEARCH or ANIm (pyani) as a secondary check.

### 2.4 C6 — dDDH not reproduced (the biggest gap)
- **Symptom:** No independent numeric value for FLUB ↔ ATCC 8290 dDDH; paper reports 76.5%.
- **Root cause:** GGDC (the canonical dDDH service at DSMZ) is a web batch tool with per-user rate limits and an interactive job form; there is no free-scriptable API suitable for batch replication.
- **Substitute used:** ANI ≥96.9% across all pairs and the tight FLUB↔ATCC 27305↔ATCC 8290 clustering. This supports the *taxonomic conclusion* (FLUB is a bona-fide *L. hilgardii*) but does NOT verify the specific 76.5% value.
- **Not fixable without:** hand-submitting the pair to GGDC (feasible but manual) or installing/running a local dDDH tool.
- **Impact on verdict:** this is the primary reason the headline is PARTIAL rather than REPLICATED.

### 2.5 CRISPR / prophage / mobile-element inventories
- **Symptom:** not attempted.
- **Root cause:** each requires a separate service (CRISPRCasFinder, PHASTER, IslandViewer) with its own web submission workflow; setting these up cleanly was outside this pass's ~15-min compute budget.
- **Not fixable without:** an additional pipeline pass with those tools.

### 2.6 Wet-lab phenotypes (Bioscreen C ethanol/sugar/fructophily)
- **Symptom:** not attempted.
- **Root cause:** requires physical strain culture, Bioscreen C spectrophotometer, and controlled substrate/temperature conditions.
- **Impact on verdict:** these are the paper's *headline biological* claims. This replication verifies the paper's *genomic* substrate but says nothing about whether the paper's phenotype measurements are correct.
- **Not fixable without:** wet-lab replication (out of scope for this project).

### 2.7 Functional identity of FLUB's unique genes
- **Symptom:** we reproduced 266 ≈ 268 singletons but did not verify that they correspond to the paper's stated categories (arsenic detox, surface-layer proteins, metabolic cluster).
- **Root cause:** functional annotation of singleton sets was not part of this replication's scope.
- **Impact on verdict:** in principle a malicious or careless author could produce the same singleton *count* with completely different biology. This replication does not detect that class of failure.
- **Not fixable without:** COG/KEGG/eggNOG functional annotation of the singleton set + manual mapping to the paper's stated categories.

---

## 3. Threats to the replication itself (self-audit)

| Threat | Description | Mitigation applied |
|---|---|---|
| Assembly re-use | We used the same NCBI assembly the paper deposited; genome-stats match by construction. | Documented in report §8; per-replicon verification confirms the deposit is internally consistent with the paper's Table 1 (not always true in genomics papers). |
| Strain-set drift | 2026 RefSeq ≠ 2020 RefSeq. | Reported both 5- and 6-genome runs; explicitly documented ±2% cluster drift. |
| Deposit redundancy | ATCC 8290 / DSM 20176 / LH500 are ~99.9% identical (one lineage, three deposits). | Reported both the 5- and 6-genome pangenomes to make the effect visible. |
| LLM-judge as verdict | Argo gpt-5.2 is a check on our bookkeeping, not an independent scientific reviewer. | Headline verdict retained at PARTIAL-strong (conservative human-set floor) even though the consolidated LLM-judge scored REPLICATED. |

---

## 4. Operational failures encountered during the run

### 4.1 Roary Perl module missing (fixed)
- **Symptom:** Roary post-analysis crashed on missing `File::Find::Rule` module.
- **Root cause:** perl-5.22-vs-5.26 include-path mismatch in the conda env; the module was installed for one Perl version but Roary invoked the other.
- **Fix:** placed the pure-Perl `File::Find::Rule` module on the 5.22 include path, re-ran. Documented in `work/attempt_log`.
- **Impact:** ~10 min of debugging; no data lost.

### 4.2 MGYG-HGUT-01333 not available via NCBI GCA
- **Symptom:** NCBI Datasets returned metadata but no FASTA for the MGYG genome.
- **Root cause:** MGnify-derived MAGs are not always mirrored into NCBI with sequence.
- **Fix:** pulled FASTA from ENA browser API instead.
- **Impact:** ~5 min; documented in workflow.md §1.

---

## 5. What would upgrade this to a full REPLICATED verdict

To move from PARTIAL-strong → REPLICATED, three specific gaps would need to close:

1. **dDDH numeric reproduction.** Hand-submit the FLUB × {ATCC 8290, ATCC 27305, LMG 07934, LH500} pairs to GGDC and record the d4 values; check against the paper's 76.5%.
2. **PGAP annotation.** Run PGAP (via NCBI's Docker image or hosted service) on the FLUB assembly and compare gene/CDS/RNA/pseudogene counts to the paper's exact numbers.
3. **Functional identity of FLUB singletons.** eggNOG-mapper or COG annotation on the 260–268 singleton set to verify the paper's stated categories (arsenic detox, surface-layer proteins, metabolic cluster).

Steps 1 and 3 are ~30 min of additional work each. Step 2 is ~1–2 hours (PGAP Docker setup + run). None require paid services.

Wet-lab phenotypes (C2 in the biology sense) remain permanently out of scope for a computational replication.
