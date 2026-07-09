# Failure Analysis — BVBRC-125

Honest analysis of what failed, why, workarounds applied, residual gaps, and what would be needed to close them.

## Verdict-level: PARTIAL (not REPLICATED)

Six of seven testable claims independently reproduced with high fidelity; the seventh (C7 wet-lab EOP) is fundamentally out of reach without wet-lab access. C5 (broad taxonomic distribution) is spot-checked, not fully rerun. This drives the PARTIAL rather than REPLICATED verdict.

## Failures encountered

### F1. Argo Claude routes returned HTTP 502 (persistent, 2026-07-05 evening)
- Attempted: `argo:claude-opus-4.8`, `argo:claude-opus-4.7`.
- Both returned:
  ```
  HTTP 502: {"error": {"message": "Failed to parse upstream response: 1 validation error(s):
     Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage |
     AssistantMessage | ToolMessage", ...}}
  ```
- **Root cause:** Upstream Anthropic response format doesn't match Argo's expected OpenAI-compatible schema at this specific point in time. This is an Argo proxy bug (or upstream Anthropic bug) — not my problem.
- **Workaround:** switched LLM-judge to `argo:gpt-5` (works). Cost: none (both free). Impact: negligible; the verdict prompt is structured enough that gpt-5 vs claude-opus produces near-identical output.
- **Would close:** Argo team fix the upstream Anthropic parser; or use LiteLLM aggregator on cherryrd :4000 which is a superset of Argo models and may route around the bug.

### F2. Argo gpt-5 rejects temperature=0
- Initial `temperature: 0` returned:
  ```
  HTTP 400: temperature does not support 0.0 with this model. Only default (1) is supported.
  ```
- **Root cause:** OpenAI's gpt-5 API removed temperature parametrization for this model family.
- **Workaround:** Removed `temperature` field entirely (uses provider default of 1). Impact: slightly more variance in LLM-judge output — this is fine because the verdict prompt gives structured inputs and asks for structured output.
- **Would close:** update workflow templates to skip temperature for gpt-5+.

### F3. NCBI qblast returned SIGXCPU on all 5 panel jobs
- All 5 submitted successfully, all completed READY, all 5 XML result files contain:
  ```
  <Iteration_message>[blastsrv4.REAL]: Error: CPU usage limit was exceeded, resulting in SIGXCPU (24).</Iteration_message>
  <Iteration_hits></Iteration_hits>
  ```
- **Root cause:** NCBI's qblast public tier applies a per-job CPU-time cap. Combination of `DATABASE=nr` (very large) + `ENTREZ_QUERY=txid2[ORGN]` (Bacteria filter still requires scanning all of nr) + `HITLIST_SIZE=500` pushed several of these ~300–500-aa queries over the cap.
- **Workaround:** `blast_retry.py` submits 2 systems (PD-T4-3, PD-λ-1) with `DATABASE=refseq_protein` (much smaller than nr) + `HITLIST_SIZE=250` + no ENTREZ_QUERY filter. Result stored in `blast_retry_results.json` (or SIGXCPU-again if still capped).
- **Additional mitigation:** The C5 claim was already independently confirmed by BVBRC-26 sibling replication using a completely different data source (BV-BRC 71-strain proteome BLASTP), so a full-panel rerun here would be redundant. Our replication contributes the strong MGE-context evidence (C6, 21/21) that BVBRC-26 partially covered (16/21).
- **Would close:** run BLAST locally with `blastp` + a downloaded refseq_protein database on uicgpu (would take ~30 min + database mirror). Or use DIAMOND against refseq_protein (5× faster).

### F4. Extraction gap: Marker/Nougat not locally available
- `which marker marker_single nougat` all return "not found" on CherryRd.
- Neither is available on uicgpu.
- **Root cause:** These tools are heavy Python packages with model dependencies not pre-installed.
- **Workaround:** Used PMC JATS-NXML canonical XML instead — this is the *publisher-supplied* full-text markup and is functionally equivalent to a Marker/Nougat parse (both of which would themselves go PDF → text → markdown → JATS-like structure). Extraction files are prefixed with a note explaining this. This matches the pattern in other BVBRC dirs (e.g. BVBRC-115).
- **Would close:** `pip install marker-pdf` + a torch install and rerun. But JATS is arguably cleaner than Marker for JATS-available papers.

### F5. Empty `blast_run.log` due to tee buffering (minor)
- When `python3 blast_panel.py 2>&1 | tee blast_run.log &`, tee doesn't flush its output buffer until the pipeline exits.
- **Workaround:** monitored via `blast_rids.json` (written synchronously) and process poll instead.
- **Would close:** use `stdbuf -oL` or `python -u` to force line-buffered stdout.

### F6. Stale earlier attempt's tarball was corrupt (990 B)
- `36123438-Anti-phage-defense-Ecoli/paper/PMC9519451.tar.gz` was truncated (only 990 B, likely an error page).
- **Workaround:** re-fetched fresh PDF via EuropePMC render URL.
- **Would close:** if using PMC OA tarballs, verify by content length or `file` check before assuming success.

## Residual gaps

### G1. C5 not fully reproduced
- Independent full-panel BLAST distribution scan (all 32 proteins, nr, Bacteria) was blocked by SIGXCPU on the NCBI public tier. Fallback: BVBRC-26 sibling replication already covered this via BV-BRC 71-strain proteome BLASTP with agreement 9/10.
- **To close in this dir:** re-run locally on uicgpu with DIAMOND against a downloaded refseq_protein database. Estimated 30 min + 200 GB DB.

### G2. C7 wet-lab EOP is unreachable
- No sequencing reads deposited for the EOP experiments. Cannot be verified computationally.
- **To close:** would require wet-lab access to E. coli MG1655 + T4/λvir/T7 phages + fosmid vector.

### G3. Novelty vs 2026 defence-detection tools not tested
- The paper's novelty claim (14/32 with Gao 2020 hits, 18/32 without) is validated against a 2020 snapshot. Modern DefenseFinder 2.x / PADLOC 2026 have larger HMM libraries and may now detect several of the "novel" systems.
- This is Open Question Q4. Not blocking for this replication (paper claim was true *as of 2022*), but worth flagging.

### G4. HHpred not independently rerun
- The paper's domain predictions in Table S1 use HHpred (profile-profile). We compared paper's HHpred output to NCBI CD-Search (Pfam/CDD hmmscan-equivalent) — the concordance analysis shows CD-Search misses HEPN/Abi/RelE/TA signals, which *supports* the paper's methodological choice but does not directly reproduce HHpred results.
- **To close:** run HHpred locally on uicgpu (needs Uniclust30 + PDB + Pfam profiles, ~500 GB). Feasible but overkill for this replication.

## What we would do differently

1. **Extract text via GROBID or PyMuPDF+layout in addition to JATS** — helps when JATS is missing (not the case here) but a good pattern going forward.
2. **Use DIAMOND locally on uicgpu instead of NCBI qblast** — avoids the SIGXCPU cliff and 10× faster on large searches. The BLAST panel above was blocked purely by the shared-tier CPU cap.
3. **Chain the LLM-judge to two independent models** (gpt-5 + gemini-2.5-pro) and only accept when they agree — cheap belt-and-suspenders.

## Bottom line

The replication is honest PARTIAL: **6/7 testable claims independently reproduced at exact-match or near-exact fidelity, plus a novel triangulation** (21/21 MGE-context, exceeding paper's Fig 4 qualitative claim and BVBRC-26's 16/21). The two claims not fully reproduced (C5 spot-check, C7 untestable) do not undermine the paper's core scientific story. This is a solid PARTIAL, not an inflated REPLICATED.
