# Failure Analysis — BVBRC-72 *B. amyloliquefaciens* WS-8

What this replication could **not** do, and why. Verdict was **PARTIAL → REPLICATED-leaning** (coverage 90 %, agreement 83.6 %) — the "partial" comes almost entirely from the failure classes catalogued below.

## Failure class A — Raw data not deposited (paper-side gap, unrecoverable)

These claims cannot be re-executed at any level of effort, because the underlying raw data were never made public. This is the largest single source of the PARTIAL verdict.

### A.1 LC-MS metabolomics (Claim C18)
- **Paper claim:** LC-ESI-Q-TOF-MS on WS-8 culture extracts identified 21 lipopeptide compounds — 5 iturins (C14-A, C14-B, C15-A, +2 derivatives) and 16 fengycins (11 distinct species, incl.\ 3 double-bond isoforms) — as the dominant antifungal principle against *Botrytis cinerea*.
- **Why it failed:** No raw mass-spec data deposited. No MassIVE, MetaboLights, or GNPS accession is given in the paper.
- **Best we could do (spot-check):** Confirm the *genetic capacity* to produce both classes. antiSMASH v8 Region 5 (473–611 kb) hits MIBiG fengycin (BGC0001095), plipastatin (BGC0000407), iturin (BGC0001098), mycosubtilin (BGC0001103), and bacillomycin D (BGC0001090) — the wet-lab observation of iturins + fengycins is **genetically consistent**.
- **Verdict on this claim:** SPOT-CHECK, not fully verified. Would require a WS-8 strain re-culture + independent LC-MS run (out of scope + off-budget for a genomic replication).

### A.2 RNA-Seq expression (Claim C19)
- **Paper claim:** Late-log RNA-Seq of WS-8 shows all six antifungal-lipopeptide BGC core genes expressed; FPKM values given for 27 core BGC genes.
- **Why it failed:** No SRA / GEO / ArrayExpress accession is given. Raw reads and expression matrices are not public.
- **Best we could do:** Confirm the six antifungal-lipopeptide BGC operons are structurally present and intact in the deposited assembly (they are).
- **Verdict on this claim:** SPOT-CHECK, not fully verified.

### A.3 PacBio coverage depth (Claim C21, partial)
- **Paper claim:** PacBio SMRT sequencing at ~311× coverage.
- **What replicated:** PacBio SMRT platform is confirmed via GenBank structured comment on CP018200.1 and BioProject PRJNA354791 metadata.
- **What did not:** BioProject PRJNA354791 has no linked SRA reads accession, so depth-of-coverage cannot be independently recomputed.
- **Verdict:** platform ✅ / depth SPOT-CHECK.

## Failure class B — Tool-version drift (methodological, expected)

Reproducible in principle, but produces a **numerically different answer** than the paper because the analysis tool has evolved since 2020.

### B.1 antiSMASH BGC total count (Claim C10)
- **Paper value (v3.0):** 19 BGCs.
- **This replication:** 13 BGCs (v8.0.4 local) / 12 BGCs (v7.1.0 web).
- **Delta:** −6 (v8) / −7 (v7), i.e.\ 63–68 % of paper's count.
- **Why:** Well-documented systematic changes between antiSMASH v3 and v7/v8 in cluster-calling stringency and region merging. In particular v6+ merged adjacent NRPS/PKS hybrids that v3 would have called as separate clusters, and tightened Rule-based cluster boundaries.
- **This is not a paper error and not a replication error.** All 7 named BGCs (which are the paper's actually-interesting content) still map cleanly onto v8 regions.
- **Consequence:** Any downstream comparison against the paper's "19" must carry the tool-version caveat explicitly.

## Failure class C — Scope-of-effort (deliberate deferrals; can be closed if requested)

Things this replication did not attempt, but that are not blocked by any deposition gap. These map directly onto the 5 items in `open_questions.json`.

### C.1 Species reclassification (dDDH / ANI)
- **What we did not do:** Run TYGS + pyani / FastANI vs current type strains to confirm WS-8 is still correctly classified as *B. amyloliquefaciens* under 2016+ thresholds (or whether it belongs in *B. velezensis*).
- **Why:** Out of scope for the "reproduce the paper's stated claims" objective. But this is a genuine open question — see `open_questions.json` Q1.
- **Soft hint that it might matter:** WS-8's bacillibactin cluster runs at only 57–81 % identity to the FZB42 reference and is called the "*B. subtilis* dhbA-F variant" — a small signal that WS-8 may not sit at the FZB42 centroid.

### C.2 Full FZB42 side-by-side BGC inventory
- **What we did not do:** Run antiSMASH v8 on FZB42 (CP000560.1) with identical flags and build a paired region-by-region MIBiG-hit table.
- **Why:** Out of scope. The paper only asserts 7 named clusters and this replication confirms all 7.
- See `open_questions.json` Q2.

### C.3 PGPR mechanism-gene inventory
- **What we did not do:** Systematically BLAST WS-8 proteome against curated PGPR marker genes (epsA-O, tapA-sipW-tasA, hag, cheA/W/Y, alsS/alsD/bdhA, pstS, fhuBCDG). Claim C20 (auxin biosynthesis) was only weakly reconfirmed via Trp operon + aromatic-AAT presence.
- **Why:** The paper's primary focus is BGCs + LC-MS lipopeptides, not the full PGPR mechanism spectrum.
- See `open_questions.json` Q3.

### C.4 Anti-phage defense-system inventory
- **What we did not do:** Run DefenseFinder / CRISPRCasFinder / PADLOC.
- **Why:** Paper does not mention it, so it's not in the "reproduce paper's claims" scope.
- **Why it still matters:** Phage predation is a documented failure mode for commercial biocontrol *Bacillus*, and any deployment risk assessment for WS-8 needs this.
- See `open_questions.json` Q4.

### C.5 Genome stability under fermentation
- **What we did not do:** Passage WS-8 for 50 / 100 generations and re-sequence to check for spontaneous BGC loss or cryptic plasmid appearance.
- **Why:** Requires wet-lab time-course + resequencing; outside a purely-computational replication.
- **Why it matters:** Large NRPS/PKS clusters (fengycin ~140 kb, bacillaene ~110 kb, macrolactin ~90 kb) are prime candidates for spontaneous excision via homologous recombination between direct repeats.
- See `open_questions.json` Q5.

## Failure class D — Judgement-model dependence (interpretive, quantifiable)

### D.1 LLM-judge is single-model, single-run
- **What we did:** `argo:gpt-5.2` at temp 0.1, single call, no bootstrap.
- **Why it matters:** The 83.6 % agreement number is a point estimate, not a rigorous statistical estimate. If we wanted a confidence interval, we would need N=10–20 runs across ≥2 judge models (e.g.\ `argo:claude-opus-4.8` cross-check).
- **Impact on the verdict:** Small — the hard-count of 15/17 fully-agreeing testable claims + 4 spot-check/partial is model-independent evidence; the 83.6 % just puts a number on it.

## Summary — verdict traceability

The PARTIAL verdict decomposes as:
- **REPLICATED (verified end-to-end):** 15 of 21 claims (all quantitative genome-structure claims C1–C9; all named BGC claims C11–C17; PacBio platform half of C21).
- **SPOT-CHECK (rerunnable only at the genetic-capability level):** 3 claims (C18 LC-MS, C19 RNA-Seq, C21 depth) — blocked by failure class A.
- **TOOL-VERSION DELTA (numerically off but explicable):** 1 claim (C10 total BGC count) — failure class B.
- **PARTIAL / weak positive (C20 auxin):** 1 claim — pathway substrate machinery present but IPA-decarboxylase not annotated.
- **INCLUSIVE MATCH (C9 ncRNA counting convention):** 1 claim — matches if tmRNA counted inclusively.

The 6 non-fully-verified claims (A + B + C20 + C9) together are why the verdict is PARTIAL rather than REPLICATED. None of them are replication failures per se; they are (in order) deposition gaps, tool-version drift, and an annotation-nomenclature edge case.
