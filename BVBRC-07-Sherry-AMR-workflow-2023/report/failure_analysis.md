# failure_analysis.md — Sherry et al. 2023 replication

Honest analysis of what failed, what was worked around, and what evidence is genuinely weak. The pass-1 report gave a `REPLICATED (HIGH confidence)` verdict; this file preserves that verdict at the numeric level but discounts the CONFIDENCE label because of the shortcuts and evidence-strength gaps documented below.

---

## Part A — What actually failed (or was skipped) during the replication

### A1. Assembly-from-reads step was NOT reproduced (pass 1)
**What we did:** Ran AMRFinderPlus on complete NCBI reference genomes.
**What the paper did:** Assembled short reads with Shovill, THEN ran AMRFinderPlus.
**Root cause:** Downloading, QC-trimming, and assembling ~1500 isolates from SRA would have required ~500 GB + weeks of CPU on the available hardware. We chose to score AMRFinderPlus against reference genomes directly.
**Consequence:** Our pass-1 "100% verified" number for gene detection is measured on the EASIEST possible input (closed reference genomes). The paper's numbers are on assemblies where contig breaks matter. These two are not directly comparable.
**Residual gap:** The delta between "AMRFinder on ref genome" and "AMRFinder on short-read assembly of that genome" is exactly the paper's residual FN rate, and we did not measure it independently for the full 321-genome set. Pass 2 addressed this for 2 genomes only.

### A2. abritAMR's post-processing layer was NOT reproduced
**What we did:** Ran AMRFinderPlus directly (via `amrfinder` binary).
**What the paper did:** Wrote abritAMR (Python wrapper) that adds (a) drug-class binning via a custom "enhanced subclass" database, (b) reportable/non-reportable filtering with species-specific logic, (c) inferred antibiogram module for Salmonella.
**Root cause:** Time / scope decision — abritAMR's value-add is downstream of AMRFinderPlus and is validated by the paper only against paper-defined class buckets. Independently verifying the class-mapping requires curating our own truth table.
**Consequence:** We verified the DETECTION layer (AMRFinderPlus finds the genes) but not the REPORTING layer (abritAMR bins and filters them correctly). The paper's "99.9% accuracy" is *jointly* about both layers; our replication only backs the detection layer.
**Residual gap:** ~20% of the paper's value proposition (the CPHM-facing reporting logic) is un-replicated. Would take ~1-2 days to close: install abritAMR, run on the same 58 genomes, diff the outputs.

### A3. LOD and precision re-pass covered only 2 genomes at 2 tools (pass 2)
**What we did:** wgsim + SPAdes + AMRFinderPlus at 40X / 80X / 120X / 150X on 2 genomes, plus 3 seeds at 80X for precision.
**What the paper did:** LOD on synthetic reads (paper: no explicit N reported for LOD; likely used the full 321-genome dataset at each coverage). Precision on 13 real isolates with real MiSeq/NextSeq replicates.
**Root cause:** The third planned genome (GCA_000284595.1) did not complete within budget; time constraint kept N=2.
**Consequence:** Our 100% recall / 100% Jaccard results are on **n=2 genomes**. This is statistically thin. The paper's LOD claim (99.9% at 40X-150X) is on their full validation set; our result cannot invalidate or confirm it at scale.
**Residual gap:** Need to expand re-pass to at least 20-30 genomes to give a meaningful CI on the LOD/precision numbers.

### A4. Read simulator drift (wgsim vs. art_illumina)
**What we did:** Used `wgsim` (Heng Li) with default 2% base error + 0.1% mutation rate.
**What the paper did:** Used `art_illumina` with the empirical NextSeq500 error profile from the local sequencing runs.
**Root cause:** wgsim was already installed and is faster; art_illumina requires the empirical profile file to reproduce paper's exact conditions.
**Consequence:** Our LOD sweep is a *harder* test (wgsim's 2% error > real-world 0.5%) but with a different error *distribution* (position-independent uniform vs. position-dependent empirical). Results may not compose cleanly with the paper's LOD numbers.
**Fix if wanted:** Re-run with art_illumina + NextSeq500 profile file; probably shifts nothing but should be documented as identical.

### A5. Database version drift (2022 → 2026-03-24.1)
**What we did:** Used AMRFinderPlus DB 2026-03-24.1.
**What the paper did:** Used the DB current in ~2022 (specific date not stated in the paper).
**Root cause:** Paper's exact DB snapshot is not archived by NCBI in an easily-installable form; installing the current DB was the path of least resistance.
**Consequence:** A newer DB can add alleles (usually) but can also rename or split families (aac(6')-Ib → aac(6')-Ib' fam split is an example). Our 100% agreement with source data is safe because source data is frozen numbers; but any comparison of RAW gene calls (our TSVs vs. the paper's TSVs) would show drift. We did not do that raw-call comparison.
**Residual gap:** No longitudinal DB-drift analysis. This is Open Question Q4.

### A6. Only 58/321 genomes analyzed (pass 1)
**What we did:** Sampled 58 genomes covering 100% of the 49 species.
**What the paper did:** Full 321-genome dataset.
**Root cause:** Time budget; picked one representative per species then padded up to 58.
**Consequence:** We claim 100% species coverage, which is true, but the per-allele denominator we can address is ~58 × 415 = ~24,000 alleles (not 133,215). If per-species allele diversity is heterogeneous, our coverage is skewed.
**Residual gap:** Expanding to 321 would take ~5 hours CPU; no fundamental blocker.

### A7. C13 counting-boundary discrepancy (aac(6')-Ib FN)
**What we found:** aac(6')-Ib FN = 17 in source data (paper reports 18).
**Root cause:** Likely one allele straddles the aac(6')-Ib / aac(6')-Ib' boundary in the source-data spreadsheet; without the paper's exact SQL or Python code we cannot say which allele is the delta.
**Consequence:** Trivial (1 count on 88 discrepancies), but a real reproducibility gap. Ideally the paper should ship the exact recomputation code, not just the xlsx.
**Residual gap:** ~15 min to iterate through classification rules and pin the delta.

### A8. Marker + Nougat extractions are fallback / pending (backfill 2026-07-05)
**What we did:** `pdftotext -layout` fallback for marker.md; PENDING stub for nougat.mmd.
**What the standard requires:** Real Marker parse and real Nougat parse.
**Root cause:** Neither `marker` nor `nougat` binary installed on the host running this backfill. Marker requires a heavy CPU/GPU install; Nougat requires GPU.
**Consequence:** Table structure and equation content may be lost in pdftotext; the paper is table-heavy so this matters for automated downstream QA. Header + sha256 in nougat.mmd stub enables central-corpus backfill later.
**Fix path:** Central corpus sweep on Eagle (SCOUT/OSTI manifests) keyed on sha256 `35e3c83f...4847c2` — copy in when available.

---

## Part B — Critique of the paper's evidence strength

Even taking the replication as clean, several aspects of the paper's evidence base are weaker than the headline numbers suggest.

### B1. Synthetic-read self-consistency loop drives the 99.9% headline
The 99.9% overall accuracy is dominated by the synthetic dataset (133,127 correct of 133,215 = 99.934%). But the synthetic dataset is:
- reads generated by art_illumina FROM the same reference genomes,
- assembled by Shovill (which uses SPAdes),
- called by AMRFinderPlus (via abritAMR wrapper),
- compared to AMRFinderPlus calls on the ORIGINAL reference genomes.

Any error introduced by the BLASTx/HMM/database layer is INVISIBLE by construction, because both sides of the comparison use the same caller. Only the assembly-loss channel is testable. This is not a full validation of the caller against ground truth; it is a validation of "does Shovill lose alleles when you round-trip through 150 bp PE reads at 40X+ coverage". The paper's discussion acknowledges this ("differences between complete genomes and (synthetic) short-read data ... likely accounts for at least a proportion of the discrepant results") but the headline number does not reflect the caveat. This is Open Question Q1.

### B2. Precision experiment is under-powered and comparing near-identical inputs
The 100% within/between-run precision on n=13 isolates is measured on *the same isolate, sequenced again on the same or a similar platform, called by the same software with the same DB*. That's an extraordinarily controlled setting. Real-world precision variance sources — mixed cultures, plasmid dropout, library batch effects, HPC scheduler non-determinism, ARM64 vs x86_64 BLAST tie-breaking, DB updates between runs — are not exercised at all. See Open Question Q2.

### B3. Discrepancy resolution rules are asymmetric
The paper resolves discrepancies as follows:
- **PCR positive, WGS negative (FN):** examine partial-hit contigs; if still no hit, retest by PCR and WGS.
- **PCR negative, WGS positive (FP):** repeat PCR and sequence; if gene "in the range" of PCR panel per manufacturer, resolve as WGS-correct.

The FP resolution is much more forgiving (the WGS call can be "confirmed" by re-PCR or by pointing to the manufacturer's PCR inclusivity claim), while the FN resolution requires the WGS to actually recover something. This asymmetry inflates the sensitivity number (via FP-to-TN reclassification) more than the specificity number. The paper explicitly walks the reader from FN=7/FP=3 (pre-resolution) to FN=3/FP=2 (post-resolution) — a favorable move on 5/10 discordant calls. Not wrong, but worth flagging.

### B4. Salmonella phenotype set is single-lab, single-country, single-year window
866 isolates from Australia 2018-2019. No external cross-validation. Publication of the model as ISO-certifiable in *other* labs / *other* countries implicitly assumes the Salmonella circulating in Victoria 2018-2019 is representative of the world's Salmonella phenotype-genotype landscape. Fluoroquinolone resistance in particular has strong geographic structure (gyrA/parC mutation profiles differ across S. Typhi lineages). See Open Question Q3.

### B5. No head-to-head against ResFinder, CARD-RGI, or ARIBA
The Discussion compares abritAMR *narratively* to ResFinder (fewer classes) and CARD-RGI (ontology-focused) but never runs the same 321-genome dataset through those competitors. This is odd for a validation paper — the "novel" contribution is the classification database + reporting logic, not the calling; a head-to-head vs. equivalent tools would sharpen the case for ISO adoption of abritAMR *over* ResFinder-family or CARD. Our replication ran RGI + ResFinder on subsets but didn't structure a comparison either.

### B6. DB-drift re-verification protocol is under-specified
The paper says the pipeline "must be re-verified after each database or tool update" and describes an "abritAMR test suite" for minor updates, but does NOT publish (a) what accuracy delta triggers full re-validation, (b) any actual re-verification results across DB versions, (c) the composition or provenance of the test suite. For a paper whose central claim is "ISO-certified", this is the specific operational gap that would matter most for another lab adopting abritAMR. See Open Question Q4.

### B7. "3-min for 96 samples on 256 CPUs" claim is not reproducible
The Discussion trumpets rapid wall-clock but does not specify: CPU model, RAM, disk, whether that's abritAMR + AMRFinderPlus or just AMRFinderPlus, whether QC/assembly is included. Not central to the validation but weakens the "streamlined workflow" claim.

### B8. Author affiliation clustering
All senior authors are MDU-PHL / U Melbourne co-authors. Tool authors validating their own tool on their own lab's data is common in the field but is a well-known bias source. External replication (e.g. via NCBI Pathogens or CDC AR Bank data) would strengthen the case. This is not a defect of the paper per se, but a call for the field to move to independent-benchmarking initiatives (which the paper itself endorses in the Discussion).

---

## Part C — What would be needed to close the residual gaps

| Gap | Effort | Yield |
|---|---|---|
| A1 (assembly step) | ~1 week + 500 GB SRA download | Direct test of assembly-loss channel; would validate or invalidate the paper's biggest evidence layer |
| A2 (abritAMR wrapper) | ~1-2 days | Verify the CPHM-facing reporting layer — the paper's actual novel contribution |
| A3 (n=2 → n=30 for LOD) | ~1 day CPU | Statistically defensible LOD replication |
| A5 (DB drift) | ~1 week | Answer Open Question Q4; publishable in its own right |
| A6 (58 → 321 genomes) | ~5 h CPU | Close per-allele coverage to 100% |
| A7 (C13 delta) | ~15 min | Trivial reproducibility polish |
| A8 (Marker/Nougat) | central corpus copy | Automatic once sha256 shows up in Eagle manifest |
| B1 (self-consistency loop) | major benchmark project | Open Question Q1 — one of the more publishable follow-ons |
| B3-B6 (paper-level) | each is a paper-sized project | Would produce several follow-on publications |

---

## Bottom line

- **Numeric replication:** SUCCESS. Every testable claim from source data reproduces within tolerance, both by hand recomputation and by re-running AMRFinderPlus on reference genomes. LOD and precision re-pass replicate the paper's high-accuracy result (100% at all tested coverages / seeds) on a small subset.
- **Evidence-strength replication:** PARTIAL. The paper's numbers are correct given the paper's design; but the design has known and named weaknesses (self-consistency loop, under-powered precision, single-lab phenotype set, missing head-to-head, missing DB-drift protocol). Our replication reproduced the design without correcting these weaknesses.
- **Verdict kept:** REPLICATED. Confidence downgrade recommended from `HIGH` (as stated in `REPORT.md`) to `MEDIUM–HIGH`, on the grounds that the replication depth on the SOFTWARE side (58/321 genomes, no abritAMR wrapper, wgsim vs art_illumina, newer DB) is thinner than a full ISO-level re-validation would demand, and on the grounds that the paper itself has evidence-strength gaps (Part B) that our replication did not close.
