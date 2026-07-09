# Failure Analysis — BVBRC-40 S. thermophilus ACA-DC 2 Replication

**Paper:** Alexandraki et al. (2017), *Standards in Genomic Sciences* **12**:18
**Verdict:** PARTIAL (strong) · Coverage 10/10 · Agreement 7/10
**Purpose:** Honest inventory of what did not reproduce, why, and what would close each gap.

---

## Summary

The replication achieved **exact-to-the-digit agreement on all 7 quantitative Table 3 claims (C1–C7)**
from independently pulled + independently parsed public assemblies. It did **not** fully close three
workflow-dependent claims (C8 function-assignment %, C9 exact CRISPR count, C10 full RASTtk workflow).
No numerical contradictions were observed — every partial is a workflow/threshold gap, not a data
conflict.

Below is a per-failure breakdown.

---

## Failure 1 — Function-assignment percentage (C8)

### What failed
Paper reports **1,182 / 1,850 = 63.89%** of genes with assigned function.
Prokka 1.12 default run reached **653 / 1,818 = 35.9%**.

### Root cause
Not a data or code bug. The paper achieved 63.89% by chaining **RAST v2.0 + WebMGA + EggNOG + Pfam
+ Phobius + manual curation**. Prokka default uses a single-DB search (curated Swiss-Prot
+ bundled reference sets) with no manual curation and no multi-source consensus. Different pipeline,
different coverage — as designed.

### What this means
The replication does **not** reproduce the 63.89% number. If the scientific claim of interest is
functional coverage, this specific claim remains **unreplicated**. The structural claims (gene
counts, RNA counts, pseudogene counts) reproduced fine.

### What would close the gap
1. Rerun the paper's exact multi-tool stack: RAST + WebMGA + EggNOG-mapper + Pfam scan + manual
   curation. All components except manual curation are free.
2. Alternative: run the actual **BV-BRC Comprehensive Genome Analysis (RASTtk)** web service, which
   is the workflow the paper's method was designed to be reproduced by. Free web service, but
   involves job-queue latency.
3. Alternative: run eggNOG-mapper v2 (free) alone on the GCA proteins — a fair estimate of
   modern-standard function assignment; likely lands between Prokka default (35.9%) and paper (63.89%).

### Prevention going forward
For BV-BRC replication set papers whose deliverable is a percentage-of-annotated-genes claim,
default to running BV-BRC CGA (or the full multi-tool stack) rather than Prokka alone.

---

## Failure 2 — Exact CRISPR array count (C9)

### What failed
Paper reports **exactly 2** CRISPR arrays (both single-spacer), one *cas*-associated near
STACADC2_0849, one orphan.
minced at `minNR=2` returns **6 candidates**; default `minNR=3` returns **0**.

### Root cause
Not a data disagreement — a **tool and threshold disagreement**:
- The paper's arrays are single-spacer (2 repeats). Default minced threshold requires ≥3 repeats
  → produces 0.
- Lowering to minNR=2 recovers the paper's arrays but also 4 extra low-repeat candidates that
  CRISPRFinder + manual curation in the paper filtered out.
- Only one tool (minced) was tried.

### What this means
CRISPR **presence** and the distinctive **short/single-spacer/*cas*-adjacent** character are
independently confirmed. The **exact count of 2** is not reproduced. Read this as: "the paper's
biological story about single-spacer CRISPRs holds; the specific count is method-dependent."

### What would close the gap
1. Add CRISPRCasFinder (free) — most direct comparator to the paper's CRISPRFinder.
2. Add CRT and PILER-CR (both free); consensus across ≥3 tools would put the count on firm ground.
3. Manually inspect the 4 extra minNR=2 candidates against known false-positive patterns (e.g.
   tandem repeats not associated with cas genes) to see whether the paper's curator would have
   filtered them.

### Prevention going forward
For any CRISPR-count claim, run ≥2 independent CRISPR tools (CRISPRCasFinder + minced at minimum)
and report the intersection.

---

## Failure 3 — Full RASTtk workflow (C10)

### What failed
Paper's annotation used the **RAST v2.0** workflow (BV-BRC's earlier annotation stack) plus manual
curation. We used **Prokka 1.12** as a free local RASTtk-analog rather than running the actual
BV-BRC CGA service or the RAST server.

### Root cause
Not a failure of tools — a deliberate scope choice for a free-endpoint pipeline. Running
BV-BRC CGA involves a web-service job queue and a paid/gated authentication step that was
avoided this pass. Prokka shares the underlying tool families (Prodigal for CDS, Aragorn for
tRNA/tmRNA, barrnap for rRNA) with the RAST tool stack.

### What this means
The workflow was **approximated, not exactly reproduced**. Structural agreement (tRNA exact, rRNA
±1, CDS reconcilable via pseudogene + small-ORF accounting) is strong evidence the approximation is
faithful. But saying "we ran the paper's workflow" would overstate it.

### What would close the gap
1. Submit GCA_900094135.1 to the actual BV-BRC CGA service (free web login required) — this is the
   canonical closure.
2. Diff BV-BRC CGA output against Prokka output to quantify the analog gap.

### Prevention going forward
For BV-BRC-set papers, budget one BV-BRC CGA run per replication; it's the same time cost as Prokka
once the login is set up.

---

## Failure 4 — Prokka CDS overcall reconciliation was post-hoc

### What failed
Prokka returned **1,818 CDS** vs paper's **1,556 curated CDS**. The reconciliation offered
("≈ 1,556 curated + 224 pseudo-called-as-CDS + ~38 small ORFs") is arithmetically plausible but not
demonstrated at locus level.

### Root cause
Locus-level intersection was not performed. The reconciliation is a plausible accounting argument,
not an actual mapping.

### What this means
The 1,818 vs 1,556 gap is **explained** but not **proven**. A more rigorous replication would
bedtools-intersect Prokka CDS coordinates against paper CDS + pseudogene coordinates and count the
overlap classes.

### What would close the gap
```
bedtools intersect -a prokka.gff -b paper_cds_plus_pseudo.gff -wa -wb
```
then classify each Prokka call as: (a) matches curated CDS, (b) matches pseudogene, (c) small ORF
below curation threshold, (d) genuine novel call.

### Prevention going forward
For any CDS-count discrepancy report, add a coordinate-level intersection table before publishing
the reconciliation.

---

## Failure 5 — Secondary qualitative claims not tested

### What failed
Not tested at all:
- Restriction-modification (RM) systems (paper: REBASE-based inventory)
- Stress-response gene inventory
- Bacteriocin repertoire (paper: BAGEL3)
- Whole-genome phylogeny

### Root cause
Explicit scope choice — this pass focused on the quantitative Table 3 claims + CRISPR. Secondary
qualitative claims were deferred.

### What this means
The replication does **not** speak to whether those qualitative findings hold. Do not read a PARTIAL
verdict here as endorsement of the paper's RM / stress / bacteriocin / phylogeny sections.

### What would close the gap
- **RM systems:** REBASE search (free) on the proteome.
- **Stress genes:** KEGG / GO enrichment (eggNOG-mapper, free).
- **Bacteriocins:** BAGEL4 (current version, free) + antiSMASH bacteriocin module.
- **Phylogeny:** OrthoFinder or Roary on a curated S. thermophilus panel + IQ-TREE / RAxML.

Each of these is enumerated as an open question in `open_questions.json`.

### Prevention going forward
For genome-report papers with mixed quantitative + qualitative deliverables, either scope
qualitative sections up-front or explicitly enumerate them as follow-up open questions
(done here).

---

## Failure 6 — LLM-judge is not an independent oracle

### What failed
argo:gpt-5.2 concurred with coverage 10/10 and agreement 7/10 — but it was fed **our own
compiled evidence** (claims table + our recomputed numbers). It is a consistency check, not an
independent adjudication.

### Root cause
Design of the LLM-judge step: it audits our stated evidence for internal coherence with the
claims table; it does not independently re-fetch the assembly.

### What this means
The judge's concurrence is not zero-evidence — it caught nothing incoherent — but it is not
external validation.

### What would close the gap
Run a second judge model (e.g. argo:claude-opus-4.8) on the same evidence to see if a different
model concurs. Ideally, a "blind" judge fed only the paper text + a URL to the deposit, tasked
with re-deriving Table 3, would be a true independent check.

---

## Prevention lessons captured for future replication waves

1. **BV-BRC-set papers: budget one actual BV-BRC CGA run** rather than Prokka-only. Closes the C8
   function-% and C10 workflow gaps in one step.
2. **CRISPR claims: ≥2 tools, always.** Report the intersection, not a single-tool count.
3. **CDS-count discrepancies: locus-level bedtools intersect, not just arithmetic reconciliation.**
4. **Explicitly enumerate deferred secondary claims** as structured open questions in
   `open_questions.json`. Do not let a PARTIAL verdict silently imply endorsement of
   untested sections.
5. **Second LLM judge** for coverage/agreement — cheap on free Argo, adds real independence.

---

## What this replication does *not* claim

- We do **not** claim to have reproduced the 63.89% function-assignment figure.
- We do **not** claim exactly 2 CRISPR arrays; we claim single-spacer / *cas*-adjacent presence.
- We do **not** claim to have run the paper's exact RAST v2.0 workflow.
- We do **not** claim to have tested RM systems, stress-response genes, bacteriocins, or
  whole-genome phylogeny.
- The verdict is **PARTIAL (strong)**. Not REPLICATED. Not SPOT-CHECK. Deliberate.
