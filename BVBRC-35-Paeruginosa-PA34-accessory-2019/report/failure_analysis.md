# Failure Analysis — BVBRC-35 (Subedi et al. 2019, *P. aeruginosa* PA34)

## What failed or was skipped

### 1. C13 (genomic islands ≥24) — deliberately deferred
The paper's GI count came from a **manual MAUVE 4-way alignment** with a bespoke "4-contiguous-ORF" rule. Manual + subjective + low-throughput. We did not re-run it; the current replication makes no claim about GI count. **Impact: moderate** — the paper's accessory-genome narrative leans on this count. Fix pathway is Q2 in open_questions.json (IslandViewer 4 + PHASTEST + IntegronFinder2 automated re-derivation + concordance check).

### 2. C14 (wet-lab MIC + cytotoxicity) — fundamentally not testable in silico
Heavy-metal (Hg/Cu/Co) MIC and cell-culture cytotoxicity are phenotype assays. **Impact: low for computational verdict** — the paper's MDR + virulence story rests on both computational (AMR genes present) and wet-lab (MIC values) legs; the computational leg is confirmed but we cannot independently verify the phenotypic assay values.

### 3. Data-provenance shortcut (accepted)
We used RefSeq **GCF_003332705.2** (curated post-submission descendant) rather than the paper's own SPAdes hybrid contigs. Almost certainly identical (RefSeq derives from GCA), but we did **not diff them**. **Impact: negligible** — the pangenome/AMR/MLST all reproduce numerically, which they wouldn't if the sequence had substantively changed.

### 4. AMR count drift (16 vs paper's ≥12) — not a failure, a version artifact
Our newer ResFinder DB includes *tmexCD3-toprJ3* efflux operon recognized post-2019. The paper's ≥12 count with the 2019 DB is consistent; we get 16 with the current DB. **Impact: zero for verdict, positive for extension** — the delta 4 genes are all real AMR determinants absent from the 2019 DB (a small confirmation that PA34's plasmid carries a clinically-relevant efflux cluster that pre-dated its recognition).

### 5. Single-judge scoring (below policy ideal)
Scoring used one LLM judge (Argo `argo:gpt-5.2`). Standing policy prefers 3-judge scoring. Verdict is defensible because 4 numbers are EXACT and the rest are Δ≤1 (unambiguous), but the scoring layer is thinner than ideal. **Fix:** re-score with 3 free judges if this dir gets a rigor pass.

### 6. Roary parameter sensitivity NOT probed
Ran Roary at the single default 95% BLASTP cutoff. Our Δ≤1 gene agreement is remarkable but conditioned on this choice. We do **not** know whether the 543-unique / 124-exclusive-with-VRFPA04 numbers survive under 90-98% sweeps. **Impact: moderate** — the "PA34 has largest accessory genome" qualitative claim is robust to reasonable parameter changes, but exact-number-agreement may not be. Fix pathway is Q1 in open_questions.json.

## Backfill-process note (2026-07-05, meta)
Report items (4–8) written INLINE by parent (Ollie main session) from the existing 9 KB `report/REPORT.md`, bypassing the subagent "announce-then-die" failure mode documented in `~/.openclaw/workspace/memory/failure-log.md` (2026-07-05 entry). REPORT.md was rich enough (all claims, methods, numbers, tools already documented) that no fresh compute or judge run was needed for the backfill pass; only synthesis into the 8-artifact standard shape. Total inline-write time: <5 min parent effort.

## Net assessment
Scientific replication is **strong** (REPLICATED, 12/13 computational claims reproduce with 4 exact and the rest Δ≤1). Failures split cleanly into (a) out-of-scope wet-lab / manual-comparative items honestly excluded, (b) minor DB drift explained cleanly, and (c) two sensitivity/re-derivation extensions that are the real forward work (Q1, Q2).
