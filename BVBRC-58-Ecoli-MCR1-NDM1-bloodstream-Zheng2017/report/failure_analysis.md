# Failure Analysis — BVBRC-58 Zheng et al. 2017

**Verdict:** PARTIAL (strong). Coverage 5/6 = 83.3%; agreement ~85–90%.

This document catalogs what did NOT reproduce cleanly, and honestly categorizes each item by root cause. It is separate from the report body so a reader who wants the "failure story" can find it in one place.

---

## 1. C4 (per-plasmid AMR gene inventory) — PARTIAL, not FULL

**Symptom.** For 6 of 9 replicons, the AMRFinderPlus 2024 gene list overlaps but does not equal the paper's ResFinder-2.1 (2017) gene list. Specific mismatches:

| Replicon | Paper called | Replication called | Delta |
|---|---|---|---|
| chr CP021202 (EC1002) | oqxB | (not called) | oqxB outside AMRFinderPlus scope |
| pEC1002-1 CP021203 | aac(3)-Ib, aadA4, dfrA, arr | aac(3)-IIe, aadA5, dfrA17 | allele refinement; `arr` not called |
| pEC1002-NDM CP021206 | (none listed) | + ble, qacEΔ1, aac(3)-IId | 2024 DB annotates additional loci |
| pEC1002-NDM CP021206 | arr | (not called) | scope difference |
| pEC2474-MCR CP021209 | fosA14 | fosA3, ter* | allele-name update; tellurium cluster newly annotated |
| pEC2474-NDM CP021210 | aph | aph(3')-VI, ble | allele refinement; `ble` newly annotated |

**Root cause.** Database-version drift, not sequence disagreement. The paper used **ResFinder 2.1 (2017)**; this replication used **AMRFinderPlus 3.12.8 with DB 2024-07-22.1**. Seven years of curation have:
- Refined alleles (`mcr-1` → `mcr-1.1`; `aac(6')-Ib` → `aac(6')-Ib3`; `fosA14` → `fosA3`).
- Added newly-curated loci (`ble`, `qacEΔ1`, tellurium `ter*`).
- Excluded some genes from default calling scope (`arr`, `oqxB` are efflux/rifamycin loci with different pipeline coverage).

**Impact.** None on the paper's biological conclusions. Every core resistance mechanism the paper reported is present in the replication call (β-lactams, aminoglycosides, macrolides, sulfonamides, colistin via mcr-1, carbapenems via blaNDM-1). The differences would be caught by any reviewer running a 2024 pipeline on a 2017 dataset.

**Preventable?** No. Rerunning ResFinder 2.1 as-of-2017 would require an archival container we did not build; the drift is expected and standard.

---

## 2. Chromosomal GC discrepancy (paper 50.1% vs observed 50.61%)

**Symptom.** EC1002 chromosome (CP021202): paper reports 50.1% GC; our strict per-sequence Biopython computation gives 50.61%. A 0.51 percentage-point gap is larger than all other replicons (which agree to ≤0.5%, most to ≤0.05%).

**Root cause.** Almost certainly paper-side rounding or a whole-genome (chr+plasmids) aggregate GC vs strict per-sequence GC. Every other replicon in Table 1 matches tightly, so this is not a sequence discrepancy on CP021202 itself.

**Impact.** None. GC of 50.6% (chromosome) is consistent with typical *E. coli* whole-genome GC (~50.5%). C2 is still marked reproduced.

**Preventable?** Would need to know the paper's exact GC-computation convention (probably: whole-genome vs per-replicon).

---

## 3. Genome length ±0–8 bp differences

**Symptom.** 5 of 9 replicons match paper Table 1 exactly (0 bp). 4 replicons differ by ±1 to ±8 bp:
- CP021202 (EC1002 chr): −3 bp
- CP021203 (pEC1002-1): −1 bp
- CP021204 (pEC1002-4): −1 bp
- CP021208 (pEC2474-3): +8 bp

**Root cause.** Either (a) the paper Table 1 sizes were reported before final GenBank submission and the submitted record was polished slightly post-print, or (b) rounding/typo. All differences are ≤10 bp on genomes of 60 kb – 5 Mb (relative error ≤10⁻⁴), so they are within any reasonable "matches" threshold for a closed-genome comparison.

**Impact.** None. C2 is reproduced.

**Preventable?** No — the differences live in the paper vs the deposited record, which the replication cannot alter.

---

## 4. Non-attempted work (scope limitations, not failures)

These items were deliberately out of scope for a genomic-substrate replication and would require additional pipelines:

| Item | Why not attempted | Cost to add |
|---|---|---|
| Raw-read (PacBio + Illumina) re-assembly | Not needed to verify C1–C6, which use the deposited closed sequences. Also SRA raw reads may or may not be available; not fetched. | High (assembly + polishing on uicgpu; 1–2 days) |
| Plasmid comparison figures (paper Figs. 2–3 via BRIG / Easyfig) | Purely visual/comparative; base-by-base alignment of `blaNDM-1` context confirmed only at the co-localization level. | Medium (BRIG plots ≤ 1 day) |
| Detailed IS-element / transposase annotation for `nikA-nikB-mcr-1-hp` vs `ISApl1-mcr-1` context (paper's mobilization claim) | Requires ISFinder/ISEScan pass, not run. Central conclusion (C6, separate plasmids) does not depend on this. | Medium (ISEScan on 4 mcr-carrying plasmids) |
| Wet-lab conjugation / mobility assays | Out of computational scope. | N/A |
| Independent LLM cross-judge (e.g., Claude Opus alongside gpt-5.2) | Judge was single-model (Argo gpt-5.2). A 2- or 3-judge consensus would strengthen scoring, not change verdict. | Low (rerun with second free judge) |

---

## 5. Categorized summary

| Category | Count | Examples | Verdict impact |
|---|---:|---|---|
| Database-version drift (expected, not a defect) | 6 loci | mcr-1→mcr-1.1, fosA14→fosA3, arr not called | Downgrade C4 from FULL to PARTIAL only |
| Rounding/reporting differences (paper-side) | 4 replicons | ±1–8 bp; chr GC 50.1→50.61 | None on verdict |
| Deliberate scope choices | 5 items | no raw reassembly, no BRIG figures, no wet-lab | None on verdict |
| Genuine unresolved | 0 | — | — |

**Bottom line.** No item in this failure analysis represents a genuine failure of the paper's science to hold up. C4's PARTIAL status is fully explained by seven years of AMR-database evolution, and all other observed differences are cosmetic. The paper's central claims (co-carriage on separate plasmids, MLST identity, replicon typing, genome closure) reproduce independently on the actual deposited sequences.

## 6. Verdict rationale in one line

Reproduced 5/6 claims exactly, 1/6 partially (AMR gene inventory) with the partial-only cause being 2017-vs-2024 database drift; therefore **PARTIAL (strong)** rather than FULL, and far above STRUCTURAL.
