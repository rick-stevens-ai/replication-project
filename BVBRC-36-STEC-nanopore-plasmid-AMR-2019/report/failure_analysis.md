# Failure Analysis — BVBRC-36 (González-Escalona et al. 2019, STEC nanopore)

## What failed or was skipped

### 1. C9 (methodological thesis: long-read beats short-read) — deferred, not tested
The paper's central METHODOLOGICAL thesis is that long-read sequencing recovers AMR/virulence/plasmid genes that short-read assembly misses or misassembles. **We did not directly test this** — we used the deposited PacBio-based CP assemblies as ground truth rather than re-assembling raw MinION and MiSeq reads and diffing gene calls. **Impact: real.** Our replication supports the biology (all AMR sits on the 73 kb mobile plasmid — architecturally consistent with the "short-read misses" claim) but does not directly demonstrate the methodological claim. The fix is Q1 in open_questions.json: full raw-read re-assembly on uicgpu (SRR8335317 MinION with CANU/Flye vs SRR8335318 + SRR8333590/91/92 MiSeq with SPAdes), 4–8 h compute.

### 2. Assembly-accuracy claims (99.9% consensus) not independently verified
We accepted the CP consensus. Sequence-accuracy claims of the paper are trusted, not tested. **Impact: low** — the biology built on top matches, which it wouldn't if the consensus was substantively wrong at gene positions.

### 3. Stx phage coordinate mismatch (§4.6 in REPORT.md) — noted, not resolved
The Stx-phage genome COORDINATES differ from paper Table 8 because paper reports MinION-assembly coordinates while we use deposited CP assemblies with different origin rotation. **Impact: none for scientific claim** (all three phage types + chromosomal localization match), presentation-only. Fix pathway is Q4 (genome-origin normalization).

### 4. PHASTER prophage recount NOT run
Paper Table 8 reports prophage counts/sizes; we only verified Stx-carrying-phage type and chromosomal localization. **Impact: moderate** — the paper's phage architecture story is trusted rather than re-derived. Fix pathway is Q2.

### 5. Reference-DB drift is a known-but-unquantified caveat
We used current abricate DBs (ResFinder 3,206 seqs), not the 2019 DB snapshot. Both counts happen to be 6 for CFSAN027346 — either a happy coincidence, or evidence that all extra current-DB genes fall below the 80% cutoff on this specific plasmid. **Not disentangled.** Fix: pin the 2019 DB snapshot and re-run — a good sensitivity test.

### 6. Single LLM-judge below policy ideal
One judge (Argo gpt-5.2, after Opus 502'd). Policy prefers 3-judge scoring. **Verdict is defensible** because the AMR result is EXACT to allele and MLST/virulome patterns are unambiguous, but the scoring layer is thin.

### 7. Plasmid mobility / host-range analysis NOT run
Neither the paper nor this replication directly probes the 73 kb IncFII AMR plasmid's transfer machinery (relaxase, oriT, mating-pair-formation) or its prevalence in the wider STEC/Enterobacteriaceae population. The clinical narrative implicitly depends on transferability. Fix pathway is Q3.

## Backfill-process note (2026-07-05, meta)
Report items (4–8) written INLINE by parent (Ollie main session) from the existing 14 KB `report/REPORT.md`, bypassing the subagent "announce-then-die" failure mode. REPORT.md was extremely rich (all claims, methods, per-strain tables, evidence traces, LLM-judge output already documented) so no fresh compute or subagent needed. Total inline-write time: <5 min.

## Net assessment
Scientific replication is **strong**: 8/9 tested claims fully reproduce, the AMR result is EXACT to the allele level (blaTEM-1B, dfrA8, all on the correct plasmid), MLST 3/3 EXACT, virulome all strain-dependent patterns EXACT, plasmid architecture 7/7 EXACT. Failures split into (a) the methodological C9 claim honestly deferred as needing raw-read re-assembly, (b) presentation-only coordinate mismatches, and (c) missing extensions (PHASTER, plasmid mobility, DB-snapshot sensitivity) that are the real forward work in open_questions.json.
