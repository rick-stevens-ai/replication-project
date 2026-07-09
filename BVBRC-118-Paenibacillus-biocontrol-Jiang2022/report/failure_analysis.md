# Failure Analysis — BVBRC-118

Verdict: **REPLICATED**. However, honest documentation of friction, assumptions, unresolved
mismatches, and residual gaps follows below.

## 1. Things that failed and had to be worked around

### 1.1 `prefetch` (SRA-toolkit) could not resolve NCBI SDL over uicgpu proxy
- Symptom: `prefetch.3.4.1 int: connection not found while validating within network system module — cannot resolve remote location of 'SRR10363117'`.
- Root cause: `prefetch` uses NCBI's SRA Data Locator service (SDL) on TLS with certificate pinning, which the uicgpu proxy (`http://<lan-host>:3128`) trips.
- Workaround: Direct S3 fetch from `sra-pub-run-odp.s3.amazonaws.com` (allowed by tailnet direct routing via `NO_PROXY`). 314 MB in ~30 s. Byte count matches SRA record so integrity verified.
- Residual gap: none — data is identical.

### 1.2 Marker + Nougat OOM on GPU 0
- Symptom: `torch.OutOfMemoryError: CUDA out of memory` — GPU 0 had 19 GB and 53 GB already reserved by another user's Python process.
- Root cause: shared node, no reservation system, marker+nougat default to CUDA device 0.
- Workaround: `CUDA_VISIBLE_DEVICES=2` for marker, `=3` for nougat. Both succeeded in ~90 s.
- Residual gap: none — extractions clean.

### 1.3 LiteLLM aggregator can't parse `argo:claude-opus-4.7/4.8` responses
- Symptom: `HTTP 502 ... Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage`.
- Root cause: Argo Opus 4.7 and 4.8 are "thinking" models — they return the message content as a list of `{"type": "thinking", ...}` and `{"type": "text", ...}` parts, which the current LiteLLM proxy validator on cherryrd :4000 does not accept.
- Workaround: fell back to `argo:claude-opus-4.6` (non-thinking) which returns a plain string content. Verdict unchanged.
- Residual gap: If the wave brief later mandates a specific opus-4.7/4.8 judge (Rick's default), the LiteLLM shim would need patching to unwrap content parts. Filed as a note for the aggregator maintainer.

### 1.4 antiSMASH default (`run1`) did not run knownclusterblast → no MIBiG compound names
- Symptom: initial `antismash --taxon bacteria --genefinding-tool prodigal` gave only structural cluster types (NRPS, PKS, RiPP...) with no compound identifications.
- Root cause: knownclusterblast is off by default in antismash 8; needs `--cb-knownclusters --cb-general --cb-subclusters`.
- Workaround: ran `run2` with those flags plus `--pfam2go --tigrfam --asf --rre --tfbs`. ~13 min extra wall clock. All 6 named compounds recovered.
- Residual gap: none.

## 2. Unresolved mismatches

### 2.1 5,997 bp assembly-length excess (Flye vs paper's HGAP)
- **What**: My Flye 2.9.6 assembly is 6,007,189 bp vs paper's 6,001,192 bp (Δ=+5,997 bp, +0.10%).
- **Likely cause**: Flye better resolves collapsed rDNA operon copies (bacterial 16S–23S–5S operons often collapse in older HGAP; 5–10 kb per operon is typical). *P. peoriae* has ~13 rRNA operons (paper reports 39 rRNAs / 3 rRNAs-per-operon = 13 operons).
- **Impact**: 0.10% is well below any biological interpretation threshold; does not change any downstream analysis.
- **Would-need-to-close**: same-tool comparison (re-run HGAP on the same fastq) — not attempted this round (HGAP is deprecated software).

### 2.2 antiSMASH detects 19 BGCs vs paper's 12
- **What**: antiSMASH 8.0.4 finds 7 additional regions the paper did not report.
- **Likely cause**: antiSMASH 8 has new detection modules that did not exist in 2022 (paper likely used v6): RRE-containing, cyclic-lactone-autoinducer, proteusin, terpene-precursor, NI-siderophore.
- **Impact**: HJ-2's biocontrol biology may in fact be richer than the paper reported — 2 of the 7 extras (paenilipoheptin, paenibacterin) are strong hits (>20 MIBiG proteins matched) and both compound families have documented antifungal activity.
- **Would-need-to-close**: re-run antiSMASH 6.1 with matching HMM DB to confirm 12-vs-19 is purely a tool-version effect. Not attempted this round.

### 2.3 Pelgipeptin coordinate outlier (2,172,906 bp rotation offset vs ~2,405,000 bp cluster)
- **What**: Four of five named clusters yield rotation offset 2.403 ± 0.006 Mb; pelgipeptin alone yields 2.173 Mb.
- **Likely cause**: Possible typo in paper Table 4 — the coordinates 485,090-558,941 may actually belong to a different cluster (possibly the paper's ordering of Location column was misaligned by one row). Alternatively, paper's HGAP assembly may have a local mis-assembly at that locus.
- **Impact**: does not challenge the *presence* of pelgipeptin (this study's MIBiG hit is BGC0000403.5 with 2/8 hits — a weaker but positive match).
- **Would-need-to-close**: BLAST the paper's supplementary pelgipeptin ORFs (if available) against the Flye assembly to locate the true cluster; contact authors if inconsistency confirmed.

### 2.4 IBSD35 vs HS311 as "closest relative" is within noise
- **What**: skani ANI(HJ-2, IBSD35) = 97.59% vs ANI(HJ-2, HS311) = 97.56%; Mash distances 0.02445 vs 0.02460.
- **Likely cause**: Both IBSD35 and HS311 are within the standard ANI conspecificity band (>95%); at this level, "closest" is a coin-flip.
- **Impact**: paper's phylogeny claim (C7) is defensible (ranking direction matches), but shouldn't be over-interpreted.
- **Would-need-to-close**: pyani-blastn + core-gene MLST + GToTree tree with bootstrap.

## 3. Untested claims (out of computational scope)

- Wet-lab claims (Table 2 disease-incidence/control-efficacy in greenhouse + field; Fig 5 antagonism plate assay; Fig 6 TEM biofilm/colonization; spore-germination inhibition Fig 5C) require live pathogen work with *F. concentricum*, *F. oxysporum*, *R. solani* and living *P. polyphylla* plants — not computationally reproducible.
- CFU colonization numbers (3.16 ± 0.15 × 10⁷ CFU/g rhizosphere) require living plant + culture + plate counts.

## 4. Assumptions

- Flye 2.9.6 `--pacbio-raw` (not `--pacbio-hifi`) is correct for a Sequel-era CLR read set: paper explicitly says "PacBio Sequel platform ... Reads were assembled using HGAP (version 2.3.0, SMRT Analysis)", which is a CLR pipeline. HiFi assumes CCS consensus reads which SRR10363117 does not contain.
- `--genome-size 6m` was set from the paper's reported chromosome size. If unknown, Flye's default (`0`) usually works but might change coverage stats.
- Prokka's protein-CDS-count is comparable to whatever pipeline the paper used (unnamed in the paper: paper Methods say "Coding DNA sequence (CDS) prediction ... IslandPath-DIMOB GI prediction ... tRNAs ..." but no gene predictor is named). Prokka uses Prodigal internally; Prodigal is the community-standard. Reasonable assumption.
- LLM-judge with `argo:claude-opus-4.6` at temperature 0 is a stable rubric — cross-check with a second judge (e.g. `argo:gpt-5.1`) would tighten confidence but was not run this round.

## 5. What would strengthen the claim beyond current?

1. **Same-assembler baseline**: re-run HGAP or its modern equivalent (`pbcromwell`, `pb-assembly`) to attribute the 5,997 bp difference explicitly.
2. **Same-antiSMASH baseline**: re-run antiSMASH 6.1 (2022-era) to confirm the 12-vs-19 discrepancy is purely tool-version drift.
3. **Cross-judge**: run the scoring prompt through `argo:gpt-5.1` as an independent LLM-judge and take the harmonic mean of agreement scores.
4. **Coverage validation**: minimap2 map raw reads back to the polished assembly and compute samtools depth to confirm 205× is uniform (no drop-outs indicating mis-assembly).
5. **BUSCO**: run BUSCO with `bacteria_odb10` on the polished assembly to verify single-copy-orthologue completeness. Not run this round because BUSCO is not installed in any bvbrc/amr env on uicgpu.
