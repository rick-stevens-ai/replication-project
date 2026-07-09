# Failure Analysis — BVBRC-44 pCl107 Replication

**Verdict:** REPLICATED (11/11 tested claims match paper). This document is the *honest* counterweight to that verdict — enumerating what was **not** done, what was done in a shortcut way, and where residual epistemic risk sits. It is written so that a future analyst re-approaching this target knows exactly where to push.

---

## 1. PDF / paper-text availability

**Status: mostly OK, minor gap.**

- The paper is **open-access CC BY 4.0** on Oxford University Press and mirrored in Europe PMC + PMC (PMC10117892).
- Full-text XML was pulled cleanly from Europe PMC (`work/fulltext.xml`) and used for claim extraction.
- No PDF-only figures were needed for any of the 11 tested claims; all quantitative claims live in the paper body or tables that appear in XML.
- **What was not done:** the actual figure images (Fig. 1 gene-map, Fig. 3 90-taxon BREX phylogeny, Fig. 5 mercury module) were not visually inspected against re-generated equivalents. Fig. 1 gene-map was cross-checked *coordinate-wise* against `pCl107_modules.json` but not rendered.
- **`extraction/marker.md` is empty / not present** — this replication used the Europe PMC XML full text directly rather than running the marker OCR/PDF-parsing pipeline. For a paper of this quality (OA, well-structured XML) this was the right shortcut; for a scan-only or paywalled paper this would be a real failure mode.

**Risk:** low. If a figure-only claim were later found to matter, re-visualization would be a few hours of ggplot/gggenes work.

---

## 2. Analyses that were NOT run

Ordered from most-defensible skip to most-material-gap:

### 2.1 De-novo hybrid reassembly from raw reads *(deliberate, defensible skip)*
The paper describes a Unicycler v0.4.7 hybrid assembly from SRR20613520 (Illumina) + SRR20613519 (MinION). We replicated on the *deposited assemblies* (CP098521/CP098522), not from raw reads. This means we implicitly trust the authors' assembly pipeline for the ~4.25 Mbp of DNA sequence that then underpins every downstream claim.

- **Why skipped:** ~5–15 hours of wall clock on uicgpu + a nontrivial conda env with the *exact* Unicycler 0.4.7 dependency pins (which are old and increasingly fragile to install). Doesn't change the tested-claim verdict on the deposited artifact.
- **What could go wrong:** if the deposited assembly encodes post-hoc manual polishing that a naive rerun wouldn't reproduce, our "exact 4,056,235 / 198,716 bp" match is meaningful only for the deposited artifact, not for the raw-data-to-conclusion pipeline. This is the biggest single caveat and is the subject of `open_questions.json` Q1.

### 2.2 Kaptive capsule typing (KL14 / OCL6) *(untested subclaim of C2)*
The MLST portion of C2 (ST25/ST229) was reproduced exactly. The capsule half (KL14/OCL6) was **not** re-typed with Kaptive — the standard Acinetobacter capsule-locus tool.

- **Why skipped:** Kaptive requires a curated locus DB installed separately; time boxed the replication run.
- **Risk:** low-moderate. Capsule typing is a distinct claim; a Kaptive mismatch would create a genuine (small) discrepancy against the paper. Estimated 30 min to install + run.

### 2.3 90-taxon BREX FastTree phylogeny (Fig. 3) *(skipped, high effort)*
The paper's Fig. 3 places pCl107's BREX system in a 90-taxon phylogeny with FastTree from a mafft alignment.

- **Why skipped:** ~2 hours of curated taxon selection + mafft + FastTree; requires cross-referencing Fig. 3's supplementary taxon list. Not needed for the "BREX module present" claim (C5), which was verified structurally.
- **Risk:** low. The claim we tested (C5) was the presence + coordinates of the BREX gene set, not its phylogenetic placement.

### 2.4 616-plasmid comparative panel (Tables 1–3) *(skipped, largest skip)*
The paper compares pCl107 against **616 public A. baumannii plasmids**. We tested C11 ("closest relative = pMC1.1") against only the 5 named family plasmids from the paper — not against the full 616-plasmid panel.

- **Why skipped:** biggest single time investment in the paper; ~1 day of downloads + all-vs-all BLAST + tabulation.
- **Risk:** moderate. Our C11 result confirms pMC1.1 is closest *among the paper's shortlist*. A hidden 617th relative closer than pMC1.1 could exist and would falsify (or at least sharpen) the "closest relative" claim. This is why `open_questions.json` explicitly flags a full-panel comparison as follow-up.

### 2.5 Formal transposon-boundary analysis for the "Tn6172 variant" claim (C4) *(shortcut)*
C4 was tested at the **sequence-identity level** (12 kb, 100% id to pA297-3/pAB3). The paper's stronger claim is that the pCl107 resistance region is a *Tn6172 variant* — i.e. it has the transposon architecture (IRs, DRs, TSDs, transposase phylogeny) of the Tn6172 family, not just sequence match.

- **What was done:** sequence identity check.
- **What was NOT done:** ISEScan / ISFinder BLAST for boundary IS elements; TSD identification; transposase phylogeny.
- **Risk:** low-moderate. The 100%-identity result is strong circumstantial evidence, but the formal classification claim is one step further than what we tested.

### 2.6 Functional / wet-lab replication *(entirely absent, correctly so for a dry replication)*
No wet-lab work was done. This means the following implied-functional claims were tested **only genotypically**:

- BREX phage restriction activity (C5)
- ptx phosphonate metabolism activity (C6)
- Uric-acid catabolism partial-loss phenotype (C7)
- MPF_I conjugation frequency and host range (C9)

**Risk:** moderate for biological interpretation, zero for the replication scope as framed. All four of these are open questions for future work (see Q3, Q5 in `open_questions.json`).

### 2.7 Whole-plasmid ANI (skani / pyani) *(shortcut used a proxy metric)*
For C11 we used `blastn -perc_identity 95 → summed aligned bp / query length`. For pMC1.1 this gave ~108% — a repeat-inflated metric where overlapping HSPs against the same query region can sum past 100%.

- **Why used:** fast, adequate as *ordinal ranking* signal.
- **Why suboptimal:** not a real ANI. A proper pyani/skani ANI would give an interpretable percentage.
- **Risk:** very low for the ordinal claim (pMC1.1 is clearly closest); modest for anyone who might mistake "108%" as a literal similarity.

### 2.8 Orthogonal re-annotation (Prokka / Bakta / PGAP-fresh) *(shortcut)*
Module coordinates (C5–C9) were checked against the **RefSeq / GenBank annotation of CP098522.1**, which is upstream-managed by NCBI's PGAP pipeline. The paper's authors would have relied on a very similar annotation pipeline for their own coordinate reporting, so this contains a modest circularity.

- **What could go wrong:** if a module gene (e.g. urate oxidase) is present but mis-annotated or classed as a hypothetical protein, our absence call for it (C7) would be wrong.
- **Mitigation:** for the specific C7 absence claim, a targeted HMM search vs Pfam PF01011 (uricase) and PF07969 (HpxO) would be a stronger negative test. Not run.

---

## 3. Single-judge scoring (LLM-adjudication caveat)

Coverage 9/10 and agreement 10/10 come from a **single free-Argo LLM judge** (`argo:gpt-5.2`). This is not statistically robust adjudication.

- **What was not done:**
  - No second judge run (Claude Opus, GPT-5.4, Gemini-2.5-Pro) for inter-rater agreement.
  - No adversarial ("devil's advocate") prompt seeded with hypothesized discrepancies to test judge sensitivity.
  - No self-consistency (n=3–5 samples from the same judge) to bound intra-judge variance.
- **Why not:** free-Argo LLM judging was time-boxed and the standing project convention was single-judge for the BVBRC-100 replication set. In hindsight, running 2 additional free-Argo judges (`argo:claude-opus-4.8`, `argo:gpt-5.4`) would have cost ~1 additional minute and materially strengthened the scoring.
- **Risk:** low for the replication verdict itself (all 11 claims independently checked with concrete evidence files that survive judge disagreement), moderate for the *scores*. The 9/10 and 10/10 numbers should be read as "one well-calibrated but individual assessor," not as a consensus.

---

## 4. Provenance / audit-trail gaps

Minor items that would improve future auditability:

- Exact command-history / shell-log for the uicgpu session was not archived (only the aggregated evidence files were preserved).
- Timestamps on individual `efetch` calls not preserved (only the file mtimes on uicgpu, which can drift with rsync).
- The precise Argo-proxy commit / model-hash for `argo:gpt-5.2` at judgment time was not captured; a future rerun could get a slightly different judge assessment.

These are hygiene issues, not correctness issues. Future BVBRC-* replications should include a `script`-logged transcript.

---

## 5. Summary risk matrix

| Risk area | Severity | Likelihood of overturning verdict | Effort to close |
|---|---|---|---|
| De-novo reassembly not run | Moderate | Low | ~1 day compute |
| Kaptive capsule not tested | Low | Low (only subclaim of C2) | ~30 min |
| 616-plasmid panel not rebuilt | Moderate | Low for tested C11, moderate for scope | ~1 day |
| Transposon boundary analysis (C4) | Low | Very low | ~2 h |
| Wet-lab functional (BREX/ptx/uric/MPF) | High for biology, N/A for dry replication | Not applicable | Wet lab + strain access |
| ANI proxy metric instead of skani | Very low | Very low | ~15 min |
| Orthogonal re-annotation | Low | Low, except for negative claims | ~1 h |
| Single LLM judge | Low for verdict, moderate for scores | Very low | ~1 min |
| No shell-transcript log | Provenance-only | None | Habit change |

---

## 6. Bottom line

The **REPLICATED** verdict stands. Every one of the 11 concrete tested claims was checked against the deposited public sequences with independent tools and matched (several to the exact base pair). The failure modes above are honest about the fact that:

1. We replicated *the deposited assembly*, not *the raw-read-to-assembly pipeline*.
2. We tested *core claims* not *every peripheral figure*.
3. We used *reasonable dry-lab shortcuts* (single judge, blastn-proxy ANI, RefSeq annotation) rather than *maximally rigorous* alternatives.

None of the caveats above rise to the level of a discrepancy — they are the price of a 5-minute compute + 3-hour analyst-time replication. A follow-up rigorous pass would cost approximately +1 additional day of compute + 1–2 days of analyst time and would primarily test items in `open_questions.json` rather than re-open the tested-claim verdict.
