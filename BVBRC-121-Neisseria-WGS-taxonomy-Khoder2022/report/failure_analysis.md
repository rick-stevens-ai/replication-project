# Failure Analysis — BVBRC-121

Every thing that didn't work, root cause, fix applied, prevention rule.

## 1. `pdf` tool → paid endpoint routing
**Symptom:** `pdf` tool call returned "Your credit balance is too low to access the Anthropic API" (from `anthropic/claude-opus-4-8`).
**Root cause:** OpenClaw's `pdf` tool preferentially routes to Anthropic Claude, which requires paid credits. The wave brief mandates free endpoints only.
**Fix:** used `pdftotext` (system poppler, `/usr/local/bin/pdftotext`) on the local Mac.
**Prevention:** for replication-project work, always prefer `pdftotext` for text-heavy PDFs; use `marker` (on uicgpu) or `nougat` (on a GPU node) for equation/figure-heavy PDFs; only use the `pdf` tool when the target is a native-analysis PDF and free credit is available.

## 2. `env.sh` `mkdir -p ""` bug on uicgpu
**Symptom:** any script that sourced `~/env.sh` under `set -e` exited with code 1 before doing anything.
**Root cause:** `env.sh` contains `mkdir -p "$HF_HOME"` before `HF_HOME` is defined (variable expands to empty string, `mkdir -p ""` returns non-zero, `set -e` kills the script).
**Fix:** dropped `-e` from `set -euo pipefail` → `set -uo pipefail`; explicitly exported proxy env in each script.
**Prevention:** documented in this file; consider filing an env.sh bugfix on uicgpu (move `mkdir -p` calls after their `export` counterparts).

## 3. NCBI `datasets` `.1` version suffix + archive path
**Symptom:** all 4 Lebanese-isolate downloads produced valid `.zip` files (654 KB, 751 KB etc.) but the fetch script reported "no fna found" and dropped them.
**Root cause:** The zip's internal directory is `ncbi_dataset/data/GCA_900654165.1/GCA_900654165.1_PRJEB30649-R19_genomic.fna` (with the `.1` version). The script looked for `ncbi_dataset/data/GCA_900654165/` (no version). Fetching with `GCA_900654165` also works (NCBI resolves to the latest version) but the archive still uses the version in the path.
**Fix:** always specify `.1` explicitly in accession lists; use `find "${A}_dir/ncbi_dataset/data" -name "*.fna" | head -1` to locate the FASTA agnostically.
**Prevention:** hard rule for all future NCBI datasets scripts — use `find` to locate files rather than assuming a directory layout.

## 4. Contaminated reference accession list (7/15 wrong taxon)
**Symptom:** first skani run produced weird ~85% ANI values everywhere; a header check revealed one row was `Bacillus sp.` — investigation showed 7 of my initial 15 accession guesses returned non-Neisseria genomes (Bacillus, Bacteroides, Streptococcus, Streptomyces, Staphylococcus, Ligilactobacillus, E. coli).
**Root cause:** I generated accession numbers from the paper's mentioned strain names by pattern (e.g., "the ATCC 33926 mucosa strain" → GCF_000186405). NCBI accession-space is not partitioned by taxon; the same GCF prefix range covers all species. Guessing accessions was fundamentally wrong.
**Fix:** replaced every non-Neisseria accession by taxon search: `datasets summary genome taxon "Neisseria X" --assembly-source RefSeq --limit 8 | jq/python filter by exact organism_name match | fetch top N`. This is the only correct way to pull "N genomes of species X".
**Prevention:** never guess NCBI accession numbers by pattern. Always resolve name-to-accession via `datasets summary genome taxon` or the official Entrez esearch endpoint. Always header-check every downloaded FASTA before analysis.

## 5. Withdrawn/suppressed NCBI accession
**Symptom:** `GCF_000185145.1` (paper's *N. mucosa* ATCC 19696 reference) downloaded successfully but the zip contained only metadata (~3.4 KB), no genome FASTA.
**Root cause:** the assembly has been suppressed from RefSeq (probably as duplicate/superseded); NCBI datasets returns the metadata package without the sequence.
**Fix:** substituted `GCF_003044445.1` (*N. mucosa* C2008000159); confirmed 96.06% ANI to R20 satisfying the paper's C2 claim.
**Prevention:** always verify the fetched `.fna` is non-empty (>1 kB) before adding to the analysis set. For any paper-cited accession that fails, taxon-search for a modern replacement.

## 6. Argo Claude 502 Bad Gateway
**Symptom:** `argo:claude-opus-4.8` returned HTTP 502 Bad Gateway on both routes (direct :44497 and aggregator :4000) at 2026-07-05 evening. Small `curl` "ping" prompts succeeded, but the 7 KB LLM-judge prompt failed.
**Root cause:** likely a transient Argo backend issue with the Claude route (or a request-size threshold). `argo:gpt-5.2` was healthy simultaneously.
**Fix:** fell back to `argo:gpt-5.2` via the LiteLLM aggregator (`<tailnet-aggregator>:4000`). Verified 8 KB prompts work; ran the judge successfully.
**Prevention:** LLM-judge scripts should probe multiple free-endpoint models automatically and use the first one that responds to a warmup prompt. Documented `argo:gpt-5.2` on the aggregator as a reliable free-endpoint alternative.

## 7. Heuristic per-claim check missed the strongest signal for C4
**Symptom:** my Python analyzer's C4 heuristic reported VK64 best-hit as mucosa (93.66%), missing the stronger macacae hit (96.83%).
**Root cause:** the heuristic only compared 4 species (mucosa/flavescens/subflava/gono) and did not include macacae in the comparison.
**Fix:** the LLM judge caught the omission from the full ANI matrix and corrected the interpretation in its verdict. Updated the REPORT.md and this failure log to reflect the corrected finding.
**Prevention:** for automated per-claim heuristic checks, always compare against **all** references in the matrix, not just a hand-picked subset. Better still, feed the full matrix to the LLM judge and let it identify the top hits — as I did here, which caught my error.

## 8. Not attempted (out of scope)
- **isDDH via GGDC** — web-only, no batch API. Not automatable in a subagent time budget.
- **Roary pangenome** — feasible (Prokka + Roary locally), but would add ~30 minutes of Prokka annotation + Roary run. Out of scope for the wave-brief time budget.
- **Full 128-reference set** — feasible (~40 minutes of `datasets download`), out of scope; used 15 stratified refs instead. Filed as Q1 in open_questions.
