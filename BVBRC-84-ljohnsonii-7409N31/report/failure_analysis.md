# Failure analysis — BVBRC-84

Honest catalog of every thing that did not work, did not fully test, or is a genuine limitation. Verdict is **PARTIAL** because of these, not despite them.

## 1. Hard blockers (paper-side data gaps)

### 1.1 Raw reads not deposited (C12 — the primary blocker)
- **Symptom:** `esearch db=sra term=SAMN21619988` returns `count=0`.
- **Impact:** the paper's methodological core claim — that HGAP v.3 on PacBio RSII yields exactly this assembly — cannot be independently re-executed. The reader receives only the finished assembly, not the primary data that produced it.
- **Who owns it:** authors + Journal of Animal Science and Technology 2023 editorial policy accepted a genome-announcement without SRA deposit.
- **Fix requires:** author-side deposit of PacBio RSII subreads (or CCS) under SAMN21619988.
- **Prevents verdict upgrade:** yes. Without raw reads there is no path to REPLICATED.

### 1.2 HGAP v.3 configuration not reported
- **Symptom:** paper says "HGAP v.3" but does not disclose min read length, min subread quality, seed-read length cutoff, or target coverage.
- **Impact:** even if raw reads existed, byte-exact reassembly would still require guessing parameters.
- **Fix requires:** author-supplied config or SMRT Analysis run report.

## 2. Soft limitations (this-replication-side)

### 2.1 Annotation drift on CDS count (C3)
- **Symptom:** paper reports 2,222 CDS (PATRIC 2022); PATRIC in 2026 reports 2,235 (+13, 0.6%); prodigal ab initio reports 2,147; RefSeq PGAP 2026 reports 2,117.
- **Impact:** no single canonical CDS number. Paper's number is faithful to its 2022 PATRIC snapshot; that snapshot is no longer live.
- **Not a bug**, but the LLM-judge downgraded C3 from EXACT to WITHIN-DRIFT for exactly this reason.
- **Fix requires:** either freeze a specific annotation timestamp in the paper, or accept ~1–4% drift as normal.

### 2.2 PATRIC undercounts 23S rRNA
- **Symptom:** paper reports 24 rRNA (PATRIC); barrnap and RefSeq PGAP both report 36 (12 complete 5S+16S+23S operons). PATRIC has 12×5S + 12×16S + 0×23S.
- **Impact:** paper's number is faithful to PATRIC but biologically incomplete. Anyone reading "24 rRNA" and expecting complete operons would be misled by the annotation source, not by the underlying sequence.
- **Fix requires:** either the paper should have used RefSeq PGAP counts, or PATRIC should re-scan for 23S. Both are outside our control.

### 2.3 Carbohydrate hydrolysis claim (C11) only inventory-supported
- **Symptom:** we can count 30 BV-BRC Carbohydrate subsystem entries across 4 subclasses. We did NOT BLAST specific GH families, did NOT run growth-curve assays, did NOT test enzymatic activity.
- **Impact:** claim is consistent with the inventory but is not proven. Any strong claim of "hydrolyzes fibrous AND non-fibrous carbohydrates" in vivo remains unvalidated.
- **Fix requires:** targeted GH family analysis (CAZy / dbCAN) + growth-curve panel on defined mono-, oligo-, and cellodextrin substrates.

### 2.4 Species-boundary check not performed
- **Symptom:** paper assigns "*Lactobacillus johnsonii*" but does not report ANI or dDDH against L. johnsonii ATCC 33200T, L. gasseri ATCC 33323T, or L. acidophilus ATCC 4356T.
- **Impact:** given the historical misclassification inside the L. acidophilus complex, the species assignment is not independently verified in this replication.
- **Fix requires:** pyani ANIb + ANIm and TYGS/dDDH runs (both possible on public data, not done here).

## 3. Tooling / infrastructure incidents (transient)

### 3.1 Argo Claude endpoints returned 502 on the judge payload
- **Symptom:** both `argo:claude-opus-4.7` and `argo:claude-opus-4.8` returned upstream 502 validation errors on the specific LLM-judge payload. Small requests to the same models worked fine.
- **Root cause:** Argo/Anthropic response-shape bug on structured JSON payloads of this shape/size.
- **Mitigation applied:** fell back to `argo:gpt-5.2`, which returned a full structured verdict. Fallback was seamless; verdict is retained and stored at `report/evidence/llm_judge.json`.
- **Future prevention:** wave code should treat Argo Anthropic endpoints as transiently unreliable for large structured payloads; keep `argo:gpt-5.2` as documented fallback.

### 3.2 Wave-brief workflow classification mismatch
- **Symptom:** wave brief classified BVBRC-84 as Unicycler/SPAdes; paper actually used HGAP v.3 (PacBio-only long-read).
- **Impact:** if we had blindly followed the brief and forced Unicycler/SPAdes, the re-run would have been scientifically inappropriate (Unicycler is designed for short-read / hybrid, not long-read-only).
- **Decision:** kept the paper's HGAP v.3 as canonical; logged the brief mismatch here and in REPORT.md §Limitations.
- **Fix requires:** wave-brief classifier should read the paper's actual sequencing tech before assigning assembler.

### 3.3 FTP feature-count fetch returned HTML 404
- **Symptom:** attempted FTP-side `feature_count.txt.gz` fetch got HTML 404 content.
- **Impact:** none — BV-BRC and Datasets API paths already provided the counts. FTP path abandoned; file kept in `work/` for provenance only.

## 4. Not-yet-attempted (out of scope but honestly noted)
- CAZy / dbCAN CAZyme profile (would deepen C11).
- antiSMASH v7 secondary-metabolite scan (bacteriocin cluster discovery).
- CRISPRCasFinder (immunomodulation-relevant loci).
- PHASTEST / geNomad prophage scan.
- Full EFSA QPS-style probiotic safety dossier.
- Any wet-lab validation.

## 5. Net assessment
- **What replicated:** every deposited quantitative and metadata claim.
- **What did not replicate:** the process claim (HGAP reassembly) is blocked by absent raw reads; the qualitative claim is inventory-supported only.
- **What is a genuine paper-side improvement request:** deposit raw reads under SAMN21619988; report the HGAP config; add ANI/dDDH species-boundary check; add at least one functional carbohydrate-hydrolase assay.
- **Verdict:** **PARTIAL**, held. Every failure mode above is documented, none are hidden.
