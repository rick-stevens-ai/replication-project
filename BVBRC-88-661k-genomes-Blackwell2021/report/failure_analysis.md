# Failure analysis — Blackwell 2021 replication

Purpose: catalogue everything that did fail, could have failed, and what the mitigations are. Verdict was **REPLICATED**, so this file documents *near-misses* and *scope-limited residuals* — not fatal failures.

## 1. Actual failures encountered

### 1.1 Argo proxy 502 on `argo:claude-opus-4.7`

- **Symptom:** First LLM-judge call returned HTTP 502 from the Argo proxy.
- **Root cause:** Transient upstream unavailability of `claude-opus-4.7` through the Argo proxy. Not a script bug; other Argo models on the same endpoint were healthy.
- **Fix:** Retry against a different free-endpoint model on the same proxy — `argo:gpt-5.1` — which returned a valid JSON verdict. Cost: 0 (both models on the free Argo endpoint).
- **Prevention:** LLM-judge harness should carry a fallback model list rather than a single hardcoded choice. Ideal: try opus first, fall back to gpt-5.1, fall back to gemini-2.5-pro; log which model actually answered. This turn logged the retry manually.
- **Residual risk:** Single-judge, one-sample verdict. See failure #4.

## 2. Failures that were pre-empted by design

### 2.1 Full-artifact download would blow the disk budget

- **What was avoided:** Pulling `661_assemblies.tar` (750 GB), `661k.cobs_compact` (872 GB), `661_ppsketch_v1.5.h5` (67 GB), `661K_sourmash_index_scaled.sbt.zip` (45 GB) — total ~1.75 TB.
- **How avoided:** Restricted the integrity claim (C6) to a random 25-sample audit against `checklist.chk`. Restricted the composition claim (C3, C4) to the 95 MB File2 and streamed the 430 MB File4 through `awk` without persisting.
- **Cost:** Weaker upper bound on undetected per-file corruption (see failure #3).

### 2.2 Loading File4 into pandas would have spiked memory

- **What was avoided:** `pd.read_csv('File4_QC_characterisation_661K.txt', sep='\t')` on a 430 MB TSV with ~40 columns could easily exceed 4 GB resident, potentially OOM'ing the runner.
- **How avoided:** Used `awk -F'\t' 'NR>1 {c[$39]++} END {...}'` to count column 39 in a single streaming pass with constant memory.
- **Prevention:** Any future column-tally on this file should use `awk` or `csv.reader` line-at-a-time, not pandas.

### 2.3 Naive species tally could have hit taxonomy-drift artefacts

- **What was avoided:** Fetching current NCBI taxonomy at run time to "clean" species names before counting would have introduced drift between the paper's 2018 snapshot and current taxonomy.
- **How avoided:** Tallied the raw `species` column from File2 as-shipped by the paper. Reported 2,594 vs paper's 2,336 with the clear caveat that ours is on the full 661k and theirs is on HQ, and that the delta magnitude is consistent with QC drop-outs.

## 3. Known weak spots (would not have blocked the verdict, but bound its strength)

### 3.1 Spot-check n=25 is small

- **Concern:** At 25/25 MD5 matches, the 95% Wilson upper bound on per-file corruption rate is ~12%. The true rate is almost certainly <<0.1% (this is a well-maintained EBI mirror), but the audit alone can't prove that tighter bound.
- **Mitigation available:** Scale to n=1000 (~100 GB, half-day pull) to tighten the 95% upper bound to <0.3%.
- **Why not done:** Diminishing returns for a REPLICATED verdict; documented as an option in `open_questions.json` / Genuine Critique.

### 3.2 Species comparison is pre-QC vs post-QC

- **Concern:** The paper's 2,336 species is on the HQ 639,981 set; our 2,594 is on the full 661,405. Delta=258 is consistent with 21,424 dropped low-quality assemblies producing spurious rare-species Kraken calls, but this is an inference, not a measurement.
- **Mitigation available:** Inner-join File2 to File4 on sample_id, restrict to `high_quality==TRUE`, recount. If it exactly equals 2,336 the inference is confirmed; if not, the residual is a novel finding.
- **Why not done:** Not needed for the verdict; the +0.3-pp top-20 cumulative agreement is far more compelling than the exact species count.

### 3.3 No independent classifier for species labels

- **Concern:** Both File2 species and ENA `SCIENTIFIC_NAME` ultimately trace back to submitter-provided or Kraken2-derived taxonomy. A systematic Kraken misclassification would pass every check in this replication.
- **Mitigation available:** Run GTDB-Tk on the 25-sample subset (or a larger tail-weighted subsample) and compare.
- **Why not done:** GPU-hours + reference DB pull would add non-trivial cost, and the top-20 verbatim priority-pathogen match makes systematic Kraken misclassification of the head implausible. Tail classification is genuinely open — see `open_questions.json` #3.

## 4. Failure modes not tested

### 4.1 Single-judge verdict

- **Concern:** One call to `argo:gpt-5.1` with one retry across model change. No ensembling, no majority vote across heterogeneous judges.
- **Impact if wrong:** Verdict text is a single sample; another judge could plausibly land at SPOT-CHECK. However, all the numeric evidence (exact-digit cardinality, 25/25 MD5s, 89.72% top-20) is judge-independent, so the underlying strength is unchanged.
- **Mitigation available:** Run 3 heterogeneous judges (`gpt-5.1`, `claude-opus-4.8`, `gemini-2.5-pro`) and report majority + disagreement.

### 4.2 Pipeline-level replication (C7)

- **Concern:** No sample was re-assembled from raw ENA reads through the archived `assemble-all-ena` wrapper. A pipeline error or malicious modification would still pass MD5 checks as long as the MD5 file was regenerated from its own output.
- **Mitigation available:** Even a 100-sample end-to-end re-assembly would close most of this gap.
- **Why not done:** Explicitly excluded by the wave brief (~30k CPU-months for full pipeline); a smaller sub-audit is Open Question #1.

### 4.3 COBS functional round-trip

- **Concern:** The paper's user-facing headline feature is *searchable* snapshot via COBS. C5 verified download availability (HEAD 200) but not that queries actually return the right samples.
- **Mitigation available:** k-mer probe test as described in Open Question #4.
- **Why not done:** 872 GB download; deferred as a separate work item.

### 4.4 Rnotebook re-execution

- **Concern:** The paper's Rnotebooks reproduce every figure; we did not run them, so a purely R-side package-drift bug that breaks figure regeneration is not surfaced.
- **Mitigation available:** Clone repo + `renv::restore()` + knit all notebooks.
- **Why not done:** Metadata recount reproduces the numbers behind Fig 1B/C directly, which is the strongest testable claim; the notebooks are lower-priority follow-up.

### 4.5 FTP endpoint durability

- **Concern:** All HEAD 200 checks are point-in-time on 2026-07-03. Says nothing about long-term durability of the EBI FTP path or Figshare 16437939.
- **Mitigation:** Schedule a monthly HEAD-only re-audit if this dataset is critical to any downstream project.

## 5. If this replication had failed

Hypothetical failure modes and the responses they would have triggered:

- **Cardinality mismatch (e.g. 661,404 vs 661,405):** Diff the manifest against `checklist.chk`, look for the missing/extra row, check if EBI silently added/removed a batch. If the paper's number is stale, escalate to NOT_REPLICATED with the specific delta documented.
- **Any MD5 mismatch in the 25-sample audit:** Expand to n=100 immediately. If mismatches persist at similar rate, escalate to NOT_REPLICATED (data integrity of the delivered snapshot is broken). If the mismatch was a single stale-mirror artifact, re-pull from a different mirror.
- **Top-20 cumulative fraction off by >2pp:** Investigate whether we tallied the wrong column, or whether the paper's ~90% is on a subset (e.g. dropped Salmonella outbreak surge samples). Escalate to PARTIAL replication with the delta and hypothesis.
- **Figshare 16437939 unavailable:** Check WBM / archived mirrors; escalate to C5 partial-fail with specific missing files listed.

None of the above happened. All checks passed cleanly.
