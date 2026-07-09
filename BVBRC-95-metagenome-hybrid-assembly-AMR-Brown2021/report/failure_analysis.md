# Failure Analysis — BVBRC-95 Independent Replication

Verdict: **PARTIAL**. This document is an honest accounting of what did NOT succeed, what was deliberately skipped, and what would be required to close each gap. It is intended to keep the replication's own limitations visible rather than hidden behind the headline PARTIAL verdict.

## Categories
1. **Scope truncation** — the replication ran on N=1 sample instead of the paper's N=10.
2. **Skipped experiments** — one paper claim (C4, spike-in) was not attempted.
3. **Partially reproduced claims** — one claim (C3) was only half-tested.
4. **Method substitutions with residual risk** — ARG-caller swap and use of pre-computed assemblies.
5. **External-validity gaps** — the paper's era-dependence (2019–2020 Nanopore chemistry) not addressed.

---

## 1. Scope truncation: N=1 vs N=10

**What happened.** The paper analyzed 10 metagenomes (5 WWTPs × 2 sample types). This replication analyzed 1 (USA-1-influent).

**Why.** Full re-annotation of all 10 samples × 7 assemblers = 70 assemblies. Time budget for this replication capped analysis at the paper's own worked example (USA-1-influent), matching the sample the authors themselves used for representative figures.

**Consequence.** The N=1 scope hard-caps the verdict at PARTIAL regardless of how strong the single-sample agreement is. Per-sample noise could inflate or deflate the observed Jaccard values.

**To close.** Loop the identical pipeline (`filter_and_amr.sh` + `analyze_amr.sh`) over the other 9 samples; expected added compute ≈ 30 min for ARG annotation on uicgpu; re-aggregate Jaccard statistics across samples with per-sample variance reported.

---

## 2. Skipped experiment: C4 (spike-in chimerism)

**What happened.** The paper's claim C4 (coverage regime affects chimerism / inversions / duplications, tested via an in-silico *M. hydrocarbonoclasticus* ATCC 49840 spike-in) was not attempted.

**Why.** C4 requires simulating reads from a reference genome at controlled coverage levels and running all 7 assemblers de-novo from raw reads — a multi-day compute effort and a fundamentally different experimental design from ARG re-annotation.

**Consequence.** The paper's C4 argument stands or falls independently of this replication. Nothing in this report supports or contests it.

**To close.** (a) Simulate short + long reads from *M. hydrocarbonoclasticus* at 5 coverage levels; (b) mix into USA-1-influent raw reads at controlled ratios; (c) re-assemble with all 7 assemblers; (d) map contigs back to the reference and quantify chimerism, inversions, duplications; (e) compare with the paper's Fig. 3.

---

## 3. Partial reproduction: C3 (hybrid recovers longer ARG contigs, enabling better contextualization)

**What happened.** The contig-length dimension was reproduced: HybridSpades has 4 ARG-carrying contigs ≥10 kb, OPERA-MS has 5 (plus one at 311 kb — also carrying an ARG). Short-read assemblers have 0–2 ARG-contigs ≥10 kb. But the **explicit MGE and taxonomy co-carriage** portion of C3 (the paper's MetaCompare + ACLAME + PATRIC pipeline) was not rerun.

**Why.** MetaCompare is an additional pipeline requiring separate DB installs, and MGE annotation adds meaningful runtime. It was traded off against getting an honest verdict on C1/C2/C5 done cleanly within the compute budget.

**Consequence.** The paper's central biological claim — that assembly choice affects ARG *genomic context*, not just ARG counts or contig lengths — is only partially addressed. Contig length is a proxy for context capacity; direct co-carriage with an MGE or a taxonomically-assignable host is the paper's actual endpoint.

**To close.** Run MetaCompare on each of the 7 assemblies; annotate ARG-carrying contigs for co-located MGEs (ACLAME) and taxonomic host (PATRIC/Kraken2 on flanking sequence); tabulate ARG-MGE co-carriage rate and ARG-host-attribution rate per assembler category; compare to the paper's Fig. 4–5.

---

## 4. Method substitutions with residual risk

### 4a. ARG-caller swap: AMRFinder+ vs Diamond-vs-CARD
**Substitution.** Paper: Diamond homology search against CARD/ACLAME/PATRIC. This replication: NCBI AMRFinder+ v3.12.8 with DB 2024-07-22.1.

**Rationale.** AMRFinder+ is stricter and curated; using an independent, modern tool strengthens the replication's independence. The scientific claim under test is the *cross-assembler relative pattern*, which should be caller-invariant.

**Residual risk.** Caller-invariance is asserted but not formally shown. A rigorous version would run both callers in parallel on the same assemblies and confirm that the Jaccard ordering and long-read depletion ratio are preserved.

**To close.** Install the paper's original Diamond-vs-CARD pipeline (or its modern equivalent), run it on the same 7 assemblies, cross-tabulate per-assembler ARG counts and symbol overlap between the two callers, then re-derive the category-wise Jaccard matrix from both caller outputs and confirm the qualitative ranking is preserved.

### 4b. Pre-computed assemblies rather than de-novo re-assembly
**Substitution.** Paper: authors ran all 7 assemblers themselves on their raw reads. This replication: downloaded the authors' deposited assemblies and re-annotated ARGs on them.

**Rationale.** Full de-novo re-assembly of 10 samples × 7 assemblers on 153 Gbp raw data is infeasible in this compute budget.

**Residual risk.** Any bug in the authors' assembly step propagates silently into this replication. If (hypothetically) the authors' Canu run failed for a specific reason, this replication would inherit that failure and appear to independently confirm C5.

**To close.** Re-assemble at least one representative sample × one representative assembler per category (e.g., Flye for long, HybridSpades for hybrid, metaSpades for short) from the raw ENA reads, and verify that per-assembler assembly stats (N50, contig count, max length) match the authors' deposited artifacts within tolerance.

---

## 5. External-validity gaps

### 5a. Era-dependence of C5 (long-read ARG depletion)
The paper's central negative finding — long-read-only assemblies severely under-recover ARGs due to Nanopore indel error — is tightly coupled to 2019–2020 MinION R9.4.1 chemistry + pre-Bonito Guppy basecalling. Modern Kit 14 / R10.4.1 + Dorado Sup has closed much of the ORF-integrity gap. This replication reproduced C5 on the same 2019–2020 data; it cannot address whether C5 still holds on modern data.

**Consequence.** Citing this replication as evidence that long-read metagenomics is generally unsuitable for ARG surveillance would be an overreach. See `open_questions.json` question #1 for the concrete follow-up.

### 5b. Single environmental matrix
All 10 paper samples are WWTP. Extrapolating C1–C5 to soil, sediment, drinking-water, and clinical matrices is asserted-not-tested by the paper and equally unaddressed here. See `open_questions.json` question #3.

### 5c. Single ARG DB snapshot
AMRFinder+ DB 2024-07-22.1 is one point in DB-version-space. Some ARG symbols may shift with later DB updates. This was not sensitivity-analyzed.

---

## Summary of what would move the verdict from PARTIAL to REPLICATED
1. Run the pipeline on all 10 samples (closes the N=1 gap).
2. Run both ARG callers in parallel on at least one sample (closes the caller-invariance gap).
3. Add MetaCompare-style MGE and taxonomy co-carriage annotation (closes C3 fully).
4. Perform the in-silico spike-in experiment (closes C4).
5. Re-basecall a subset of raw Nanopore reads with modern Dorado Sup and re-assemble with modern Flye 2.9.x to test whether C5 is chemistry-era-specific (closes the external-validity gap for the paper's most-cited negative finding).

None of these are blocked by data or method availability; all are blocked by compute-time budget. Rerunning at the paper's full scope is a defined and tractable follow-on.
