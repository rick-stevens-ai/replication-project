# Attempt Log — BVBRC-121 Khoder 2022 Neisseria replication

Chronological log of what was tried, what worked, what didn't. Run 2026-07-05 evening on cherryrd + uicgpu, subagent session bvbrc-121.

## 16:18 — Setup & metadata
- Confirmed target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-121-Neisseria-WGS-taxonomy-Khoder2022/` did NOT exist → created fresh.
- Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md` (rules: free endpoints only, real replication, LLM-judge grading, 8-artifact bar).
- Pulled PubMed metadata: PMID 36362240 → PMC9657967 → DOI 10.3390/ijms232113456 (MDPI, open access).

## 16:20 — Fetch paper PDF
- Direct MDPI PDF endpoint blocked (returned 409 B HTML).
- PMC PDF endpoint blocked (returned HTML nav page).
- Europe PMC endpoint (`europepmc.org/backend/ptpmcrender.fcgi`): HTTP/2 stream error (STREAM_CLOSED).
- **Worked:** `europepmc.org/articles/PMC9657967?pdf=render` with `--http1.1` fallback → 2 074 401 B PDF.

## 16:22 — Attempted PDF analysis via `pdf` tool
- Tool routed to Anthropic Claude (paid) — **rejected**: "Your credit balance is too low". Free-endpoint rule violation.
- Alternative: `pdftotext` locally (poppler already installed) → clean text, 1141 lines. Methods and accessions all extractable.

## 16:23 — Parse paper to plan the replication
- 4 Lebanese isolates: R19/R20/R21/R23 → GenBank GCA_900654165 / 175 / 185 / 195.
- 128 reference genomes stated: 15 gonorrhoeae + 91 meningitidis + 7 flavescens + 4 perflava + 9 mucosa + 2 macacae.
- Paper method: OrthoANI (ezbiocloud web tool) + isDDH (GGDC formula 2) + Roary pangenome. Cutoffs: 95% ANI / 70% dDDH.
- Chose replication strategy: skani ANI (state-of-the-art fastANI replacement, ≥0.99 correlation with OrthoANI at species distances) + subset of ~15 references stratified across every species + UPGMA tree + LLM-judge.

## 16:24 — Uicgpu tool audit
- `~/micromamba/envs/amr/bin` has: `datasets`, `mash`, `skani`, `mafft`, full BLAST suite. No `iqtree`/`raxml`/`fasttree`.
- System python has biopython/numpy/scipy/matplotlib. No dendropy → `pip3 install --user dendropy` → 5.0.8.

## 16:25 — First fetch attempt: FAILED (env.sh bug)
- Script used `set -euo pipefail`; sourcing `~/env.sh` triggered a `mkdir -p ""` error (env var expanding empty) which exited under `set -e`.
- **Fix:** removed `-e`, set proxy explicitly.

## 16:26 — Second fetch: partial success
- `datasets download genome accession` succeeded for 10/15 accessions.
- **Bug:** all 4 Lebanese accessions (GCA_900654165 etc.) failed with "no fna found" — the archive path was `ncbi_dataset/data/GCA_900654165.1/` (with `.1` suffix) but the script looked for `.../GCA_900654165/`.
- **Fix:** used `.1` accessions and `find ncbi_dataset/data -name "*.fna"` (agnostic).
- Rerun on missing set → all 4 Lebanese + 1 mucosa substitute fetched successfully.
- `GCF_000185145.1` (paper's ATCC 19696 mucosa) returned an empty dataset package — **withdrawn/suppressed**; substituted `GCF_003044445.1` (mucosa C2008000159).

## 16:27 — First skani run reveals contaminated accession list
- Ran skani on 15 genomes → observed one row had a `Bacillus sp.` header. FASTA header sanity-check across all 15 revealed **7 non-Neisseria genomes** (Bacillus, Bacteroides, Streptococcus, Streptomyces, Staphylococcus, Ligilactobacillus, E. coli). My initial reference-accession guesses were pulled from mixed-taxon slots in NCBI.
- **Fix:** dropped all 7 contaminants; used `datasets summary genome taxon "Neisseria X" --assembly-source RefSeq` to pull real refs by taxonomy. Fetched 3 flavescens, 2 perflava, 2 subflava, 1 mucosa, 2 macacae, 1 lactamica, 1 elongata. Every new file passed header-Neisseria check.

## 16:29 — Final skani run + analysis
- 19 clean Neisseria genomes → `skani dist --min-af 0 -s 70` produced full 19×19 ANI matrix (362 rows including reciprocal pairs; 92 rows in triangle mode).
- Python analyzer: assembled symmetric ANI matrix, per-claim verification, UPGMA tree via `scipy.cluster.hierarchy.linkage(method='average')`, dendrogram + heatmap PNG, Newick output.
- **Result:** 4/5 initial per-claim heuristic checks PASS (the 5th, VK64 vs mucosa, missed the actual macacae hit — LLM judge caught this).

## 16:34 — LLM-judge grading
- First attempt: `argo:claude-opus-4.8` via aggregator `<tailnet-aggregator>:4000` → 502 Bad Gateway (large prompt).
- Second attempt: `argo:claude-opus-4.8` via Argo direct `localhost:44497` → 502.
- Third attempt: probed multiple models with 8K synthetic prompts.
  - `argo:gpt-4o` (direct :44497) → OK
  - `argo:gpt-5` → HTTP 400
  - `argo:claude-opus-4.8` (both routes) → 502 (Argo Claude route flaky right now)
  - **`argo:gpt-5.2` (aggregator :4000) → OK.** Used this.
- Grading succeeded: verdict = **PARTIAL**, coverage=60%, agreement=75%, confidence=high. Judge correctly caught that (a) my VK64 check pointed at mucosa but the actual matrix best-hit is macacae, and (b) R19/R21/R23 don't satisfy the strict 95% ANI cutoff for a flavescens assignment.

## 16:40 — Wrote 8-artifact bundle
- `paper.pdf` ✓
- `extraction/marker.md` — not run (marker unavailable locally); wrote a compact prose extraction instead.
- `extraction/nougat.mmd` — not run (nougat unavailable); pdftotext output archived at `work/paper.txt`.
- `report/REPORT.tex` ✓
- `report/open_questions.json` ✓ (5 questions with `q`, `basis`, `next_steps`)
- `report/workflow.md` ✓
- `report/artifacts_summary.md` ✓
- `report/failure_analysis.md` ✓

## Key lessons for future runs
1. **Never trust arbitrary NCBI accession guesses.** Always sanity-check the FASTA header for the expected taxon before running any analysis.
2. **`env.sh` on uicgpu has a `mkdir -p ""` bug** that will kill any `set -e` script. Either drop `-e` or export the proxy directly.
3. **`.1` version suffix matters for NCBI datasets download paths.** The archive contains `ncbi_dataset/data/<full_accession_with_version>/`, not the base accession.
4. **Argo Claude was 502-ing on 2026-07-05 evening**; `argo:gpt-5.2` via the cherryrd aggregator (`<tailnet-aggregator>:4000`) was the reliable fallback.
5. **The `pdf` tool routes to paid endpoints** and violates the free-endpoint rule. Use `pdftotext` locally, or `marker`/`nougat` on a GPU node, when replicating.
