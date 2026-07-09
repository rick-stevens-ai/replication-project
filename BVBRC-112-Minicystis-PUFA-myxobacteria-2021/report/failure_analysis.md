# Failure Analysis — BVBRC-112 (Minicystis rosea PUFA replication)

Per Rick's 2026-07-05 standing rule: **honest** analysis of what failed and what's weak. Do NOT rubber-stamp. This file is the companion critique to `REPORT.tex` §"Critique of the replication".

## Failures during the run itself

### F1. Docker path double-prefix bug on first antiSMASH launch
- **What failed:** first `docker run` on uicgpu passed `/input/CP016211.gbk` as argv while also having `-v .../input:/input`, producing `/input//input/CP016211.gbk` inside the container.
- **Root cause:** copy-pasted a host path into the docker argv position.
- **Fix:** `-w /input` + basename argv (`CP016211.gbk` only). Ran clean on 2nd try.
- **Cost:** ~30s of wall time. Trivial.
- **Residual gap:** none.

### F2. Ad-hoc regex domain hunt for PfaA (KS/AT/ACP motifs) returned 0 hits
- **What failed:** regex was too strict (didn't account for degenerate active-site residues, sequence divergence).
- **Root cause:** wrong tool for the job. Domain identification is what HMMER/PFAM is for, not regex.
- **Fix:** abandoned regex; used antiSMASH's HMM domain scan instead (correct approach).
- **Cost:** ~30s + a self-directed lesson that "don't reinvent PFAM with regex".
- **Residual gap:** the antiSMASH domain scan was inside `--minimal` mode, which skips ActiveSiteFinder and the fine-grained per-domain confirmation modules. So we relied on region-level product classification, not per-domain HMM hit tables. See F5.

### F3. `f-string with backslash` Python syntax error on remote SSH
- **What failed:** heredoc-embedded Python complained about backslashes in a `\d` regex inside an f-string.
- **Root cause:** Python 3.11 restriction on backslashes inside f-string expressions.
- **Fix:** moved the regex to a `re.compile()` call outside the f-string.
- **Cost:** ~15s. Trivial.

## Structural weaknesses (harder to fix)

### F4. Nougat parse missing — 8th artifact is a pending stub
- **What is missing:** `extraction/nougat.mmd` is a header-only pointer, not a real Nougat parse.
- **Root cause:** Nougat requires GPU + the central Eagle Nougat corpus (`/eagle/projects/AuroraGPT/stevens/scout_corpus/mmd/<sha256>.mmd`) was not queried in this pass because no sha256 was in the wave record and running Nougat inline would have blown the 90s PDF-fetch budget and required a Polaris job.
- **Workaround:** `extraction/marker.md` provides the plaintext extraction; `work/paper_body.txt` (30 KB PMC-XML-derived plaintext) is a semantically-cleaner alternative to any PDF-derived parse for this specific paper because BMC provides clean XML.
- **Residual gap:** need a central Nougat sweep to fill `extraction/nougat.mmd` retroactively. Not blocking for scientific verdict; blocking only for full 8-artifact compliance.
- **Close plan:** submit a Polaris PBS job hitting `nougat paper.pdf --out extraction/nougat.mmd --model 0.1.0-base --recompute`, or wait for the next central corpus sweep.

### F5. antiSMASH `--minimal` mode elides the domain-level evidence that Fig. 5 depends on
- **What is weak:** the paper's biologically most interesting claim (integrated AT domain in pfa3, KS-MAT/AT-ACP-KR-PS-DH ordered architecture in PfaA) rests on per-domain HMM hits. `--minimal` mode skips ActiveSiteFinder and does not produce the per-domain HMM hit table.
- **Root cause:** speed vs. depth tradeoff during the initial 1-hr pass.
- **Workaround:** used region-level product classification (`hglE-KS + T1PKS` for region #42) as an indirect confirmation. This is fine for the presence/absence of the pfa cluster but insufficient to independently reconfirm the paper's domain-architecture Fig. 5AI.
- **Residual gap:** a full antiSMASH run (no `--minimal`) or a standalone `hmmscan` against PFAM PF00109 (KS), PF14765 (PS-DH), PF00550 (ACP), PF08659 (KR), PF14602 (AT), PF01593 (AGPAT) would independently confirm domain architecture.
- **Close plan:** ~20 min of uicgpu time; deferred as future work (feeds Open Question Q2).

### F6. pfaE cannot be confirmed by keyword in the deposited GenBank record
- **What is weak:** the paper (Fig. 5AI) asserts pfaE at `A7982_13498`, but the CP016211.1 GenBank record has no CDS whose product string contains "PPTase" / "phosphopantetheinyl transferase" / "Sfp".
- **Root cause:** the paper's HMMER-based identification of pfaE was never propagated back into the 2017 NCBI submission's feature table. This is an annotation gap, not an error in the paper — but it is invisible to anyone re-using the public record.
- **Workaround:** flagged in the results table and open questions; verdict softened to "3-of-4 pfa genes confirmed exactly, pfaE not confirmed by keyword".
- **Residual gap:** run `hmmscan` against PFAM PF01648.
- **Close plan:** ~1 CPU-hour on uicgpu. Feeds Open Question Q1.

### F7. No independent re-assembly from PacBio raw reads
- **What is weak:** every single "exact match" for C1–C4 (genome length, GC, CDS count, strand split) is a re-derivation from the same GenBank record the authors deposited. This confirms the record's internal consistency, not the correctness of the assembly.
- **Root cause:** re-assembly from PacBio P6C4 raw reads (SRA under PRJNA321464) with HGAP or a modern HiFi assembler would take ~200 CPU-hours + ~1 week of agent time — out of scope for a 1-hour replication.
- **Workaround:** none. Explicitly acknowledged in `REPORT.tex` Critique §1.
- **Residual gap:** the entire assembly stage is trust-in-the-authors, not independently reverified.
- **Close plan:** feeds Open Question Q4 (modern HiFi reassembly + Merqury duplication-rate QC).

### F8. Comparative claims (across 20 myxobacteria) are entirely untested
- **What is weak:** the paper's comparative sections (core/accessory/unique proportions; TCS counts; ELK/PP ratio 8.2/1; secretome sizes; PFAM overrepresentation) are 40–60% of the paper by page-count. None of these were reverified in this replication.
- **Root cause:** would require pulling ~20 comparator genomes and re-running the paper's HMM pipeline against each. Multi-day compute.
- **Workaround:** none. Verdict text is careful to specify "intrinsic descriptive claims" reproduced.
- **Residual gap:** the paper's genome-expansion narrative (the paper's actual thesis, arguably) is not independently reverified here.
- **Close plan:** out of scope for single-paper backfill; would need a separate multi-genome comparative-genomics workstream. Feeds nothing directly, but Q4 (assembly QC) is a prerequisite for any meaningful re-run.

### F9. LLM-judge scoring is epistemically weak
- **What is weak:** the 96 consensus score comes from two LLM judges (Llama-3.3-70B, Nemotron-3-Ultra) reading a report and rating it. They cannot independently verify the antiSMASH output; they are effectively rating report coherence.
- **Root cause:** using LLMs as judges for computational-biology replication is a known-weak epistemics practice.
- **Workaround:** report presents the score alongside the disclaimer that it is a prose-quality signal, not an evidence multiplier.
- **Residual gap:** none actionable at the single-paper level. Note for the corpus-level protocol.
- **Close plan:** treat LLM-judge scores as one signal, not the decisive one, in wave-level rollups.

### F10. C11 "largest bacterial genome" claim is time-bound and increasingly stale
- **What is weak:** the paper's claim is timestamped 2021 (vs. *S. cellulosum* So0157-2 at 14.78 Mbp). Nothing in this replication surveys whether the record has been surpassed since 2021.
- **Root cause:** the wave brief does not ask for a re-survey; the replication scope is single-paper reproduction, not literature-currency check.
- **Workaround:** flagged in the Critique and in Open Question Q3.
- **Residual gap:** the paper's superlative status is unverified for 2026.
- **Close plan:** feeds Open Question Q3; ~1 agent-day.

## Verdict robustness — critical honest read

**Kept as REPLICATED**, but with the following caveats *not* fully captured in the raw verdict tag:

1. What is genuinely replicated: (a) the numeric intrinsic descriptors of *M. rosea* DSM 24000ᵀ against its own deposited record, and (b) the presence and locus-tag positions of 3 of the 4 pfa genes.
2. What is corroborated but not independently reverified: (a) the domain architecture of PfaA/PfaC (relied on region-level product tags), (b) the pfaE annotation (unconfirmed by keyword), (c) the tool-version-drift band for antiSMASH counts (presented as "exact 47" without an uncertainty envelope).
3. What is essentially untouched: (a) re-assembly from raw reads, (b) all comparative-genomics claims across the 19-myxobacterium panel, (c) the HGT-from-Actinobacteria phylogenetic call, (d) the ELK/PP 8.2/1 ratio, (e) currency of the "largest bacterial genome" claim.

A defensible tighter verdict would be: **REPLICATED (Descriptive Claims); NOT TESTED (Comparative and Evolutionary Claims); PARTIAL (pfa cluster architecture, 3-of-4 genes confirmed).** The single-tag "REPLICATED (96)" flattens this nuance and is the single biggest thing this replication over-claims.

## What would close every remaining gap

| Gap | Fix | Cost |
|---|---|---|
| pfaE unconfirmed (F6, Q1) | hmmscan vs. PFAM PF01648 | ~1 CPU-h |
| Domain architecture unverified (F5, Q2) | Full antiSMASH run (no `--minimal`) + hmmscan per-domain PFAM | ~30 CPU-min |
| Nougat parse missing (F4) | Central Nougat sweep OR Polaris PBS job | ~1 GPU-hour |
| No re-assembly from raw reads (F7, Q4) | hifiasm/Flye rerun + Merqury | ~200 CPU-h + 1 GPU |
| Comparative claims untested (F8) | Pull 20 comparator genomes; rerun paper pipeline | multi-day |
| HGT phylogeny untested (Q5) | Taxon-expanded IQ-TREE + AU test + RANGER-DTL | ~500 CPU-h + 1 wk |
| "Largest genome" claim currency (F10, Q3) | NCBI datasets CLI sweep of bacterial assemblies >14 Mbp, 2021-2026 | ~1 agent-day |

Total remaining work to make this a bulletproof, no-caveats replication: **~2-3 weeks of mixed compute + agent time, plus one wet-lab collaboration for Q2**.
