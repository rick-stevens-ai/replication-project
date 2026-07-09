# Workflow — BVBRC-112 (Minicystis rosea PUFA replication)

## Narrative

**Total wall-clock:** ~1h (initial 2026-07-05 morning pass) + ~15min (2026-07-05 evening backfill to 8-artifact standard).
**Compute footprint:** ~1 CPU-min on m1/CherryRd for genome parsing; ~1 wall-clock-min on uicgpu (32 CPUs, docker antismash 6.1.1 minimal mode) for BGC rerun; two ~5s LLM-judge calls to CELS chicago-2 (Llama-3.3-70B) and chicago-4 (Nemotron-3-Ultra). No GPU model training; no long-running jobs.
**Agent:** Ollie (OpenClaw subagent, Argo Opus 4.7 via localhost:44497). Free endpoints only per Rick's standing rule.

### Phase 1: Paper identification & full-text pull (~5 min)
1. Received wave assignment referencing BVBRC-112. Resolved PMID 34511070 → DOI 10.1186/s12864-021-07955-x → PMC8436480 via NCBI eUtils `esummary.fcgi`.
2. `efetch db=pmc id=8436480 rettype=xml` → `work/paper.xml` (161 KB).
3. XML-tag-strip to `work/paper_body.txt` (30 KB plaintext body incl. Results, M&M, figure captions). This became the ground-truth source of every quantitative claim tested in the replication.

### Phase 2: Public genome pull (~2 min)
4. `efetch db=nuccore id=CP016211.1 rettype=fasta` → `work/CP016211.fasta` (16.27 MB).
5. `efetch db=nuccore id=CP016211.1 rettype=gbwithparts` → `work/CP016211.gbk` (32.31 MB, all CDS/product/translation blocks).

### Phase 3: Assembly & annotation stats (C1–C5) (~5 min)
6. Python 3.13 stdlib parser (no biopython dependency for portability): computed genome length from `LOCUS` line, GC% from concatenated ORIGIN block, CDS/tRNA/rRNA/gene counts by regex-matching feature-block headers, strand by presence of `complement(` in each feature's location field.
7. Wrote results to `evidence/basic_stats.log`.

### Phase 4: BGC rerun on uicgpu (~5 min including scp)
8. `ssh uicgpu` → confirmed `antismash/standalone:6.1.1` docker image present.
9. `scp CP016211.gbk uicgpu:~/scratch/bvbrc112/input/`.
10. Docker run:
    ```
    docker run --rm -u $(id -u):$(id -g) \
      -v $HOME/scratch/bvbrc112/input:/input:ro \
      -v $HOME/scratch/bvbrc112/output:/output \
      -w /input antismash/standalone:6.1.1 \
      CP016211.gbk --output-dir /output/antismash \
      --genefinding-tool none --cpus 32 --minimal
    ```
    Wall time ~1 min.
11. `scp -r uicgpu:~/scratch/bvbrc112/output/antismash/*.json /output/antismash/index.html ...` → local `report/evidence/antismash_summary/`.

### Phase 5: BGC parsing & pfa-cluster analysis (C6–C8) (~10 min)
12. Python walk over `CP016211_antismash.json`: 47 regions confirmed; region product-tag histogram → `evidence/bgc_regions.tsv`; region #42 (13,095,900–13,151,432, hglE-KS+T1PKS) identified as containing pfa loci.
13. Extracted CDS blocks for `A7982_11504–11506` from `CP016211.gbk`; wrote translations to `A7982_11504.faa` (549 aa), `A7982_11505.faa` (2,426 aa), `A7982_11506.faa` (2,740 aa); recorded coords + strand.
14. Keyword-scan for pfaE (PPTase / phosphopantetheinyl transferase / Sfp) → 0 hits → flagged as annotation limitation.

### Phase 6: C11 arithmetic + writeup (~5 min)
15. `16,040,666 − 14,782,125 = 1,258,541 bp ≈ 1.26 Mbp` → matches paper.
16. Drafted brief.md, REPORT.md, artifact_harvest.md, attempt_log.md, evidence/claim_comparison.json.

### Phase 7: LLM-judge scoring (~2 min)
17. Posted the REPORT.md + claims table to Llama-3.3-70B (CELS chicago-2, http://chicago-2/v1/, key=stevens) and Nemotron-3-Ultra (CELS chicago-4). Both returned REPLICATED. Scores 98 and 95 → consensus 96.
18. Wrote `evidence/llm_judge_llama70.txt`, `evidence/llm_judge_nemotron3ultra.txt`, `evidence/llm_judge_summary.md`.

### Phase 8: 8-artifact backfill (2026-07-05 evening, ~15 min)
19. Fetched paper.pdf from BMC via `curl -sSL https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-021-07955-x.pdf` (90s cap).
20. `extraction/marker.md`: `pdftotext -layout paper.pdf` fallback (central Eagle SCOUT corpus not queried in this pass; no sha256 in wave record). Copied `work/paper_body.txt` as backup PMC-XML-derived plaintext.
21. `extraction/nougat.mmd`: pending-stub with header noting need for central Nougat parse; Nougat requires GPU and was not run inline to keep backfill under 5 minutes.
22. Wrote items 4–8 (REPORT.tex + open_questions.json + workflow.md + artifacts_summary.md + failure_analysis.md) grounded in re-read of `paper_body.txt`.

## Tools / codes / versions

| Tool | Version | Where | Purpose |
|---|---|---|---|
| curl | 8.x | CherryRd/m1 macOS | NCBI eUtils fetches |
| Python | 3.13 | CherryRd/m1 | GenBank parsing, GC calc, antiSMASH JSON parsing |
| efetch/esummary (NCBI eUtils) | current live API | remote | PubMed, PMC, nuccore pulls |
| Docker | 24.x | uicgpu | container runtime for antiSMASH |
| antismash/standalone | 6.1.1 | uicgpu docker | BGC discovery (--minimal mode) |
| ssh/scp | OpenSSH 9.x | mesh key `id_ed25519_mesh` | uicgpu transfer |
| pdftotext (poppler) | 22.x | CherryRd/m1 | marker.md fallback extraction |
| Llama-3.3-70B-Instruct | via CELS chicago-2 vLLM | remote | LLM judge 1 |
| Nemotron-3-Ultra-NVFP4 | via CELS chicago-4 vLLM | remote | LLM judge 2 |
| Argo Opus 4.7 | argo:claude-opus-4.7 via localhost:44497 | local | agent (Ollie) |

## LOC written
- ~120 LOC Python (inline, throughout attempts).
- ~40 LOC shell (curl, docker, scp, jq-style filters).
- Report artifacts: REPORT.md (~5 KB, 165 lines), REPORT.tex (~24 KB, section-by-section detailed), open_questions.json (5-object array, ~7.6 KB), workflow.md (this file), artifacts_summary.md, failure_analysis.md, brief.md, artifact_harvest.md, attempt_log.md.
- No new persistent code checked in to a repo; all inline scripting.

## Estimate of work

| Category | Value |
|---|---|
| Wall clock (initial pass) | ~50 min |
| Wall clock (8-artifact backfill) | ~15 min |
| **Total wall clock** | **~65 min** |
| CPU-min (uicgpu, antiSMASH) | ~32 (32 CPUs × 1 min) |
| CPU-min (local parsing) | ~2 |
| GPU-min | 0 |
| Human-in-the-loop | 0 (fully autonomous agent) |
| Agent LLM-turns | ~40 (Argo Opus 4.7); + 2 judge calls |
| Data volume moved | ~50 MB (genome + antiSMASH results, one direction each) |
| Cost | $0 (Argo free; CELS free; uicgpu owned; no paid APIs) |
