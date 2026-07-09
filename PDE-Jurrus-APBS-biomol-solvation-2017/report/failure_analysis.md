# Failure Analysis — Jurrus-APBS-2017 replication

Real problems encountered, root cause, workaround, and prevention.

## F1: Direct PDF fetch failed on 3 canonical URLs from CherryRd

**Symptom:** curl of PMC, europepmc (backend), and Wiley OA PDF URLs all returned <6 KB HTML (403 wrappers or Cloudflare bot challenges), not a PDF.

**Root cause:** CherryRd's residential IP triggers publisher / Cloudflare bot-protection. PMC uses a redirect wrapper that only serves PDF to browser-like clients; Wiley (onlinelibrary.wiley.com) is behind Cloudflare with JS challenge required.

**Workaround:** SSH to uicgpu (ALCF Squid proxy), retry same URLs (same failure), then try alternative `https://europepmc.org/articles/PMC5734301?pdf=render` endpoint → succeeded with 1.71 MB PDF. This endpoint serves PDF directly without wrapper redirects and is not Cloudflare-gated.

**Prevention:** Add `europepmc.org/articles/PMC<id>?pdf=render` as the FIRST fallback URL for any OA paper with a PMC accession. It has consistently been the most reliable PMC-side endpoint across many replications.

## F2: Nougat OOM on default GPU

**Symptom:** `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 112.00 MiB. GPU 0 has a total capacity of 79.25 GiB of which 55.38 MiB is free. Process 762263 has 17.69 GiB memory in use.`

**Root cause:** GPU 0 on uicgpu had another process using 17.7 GB + nougat competing. `nvidia-smi` showed GPUs 6 and 7 completely idle (81 GB free each).

**Workaround:** `CUDA_VISIBLE_DEVICES=6 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True nougat ...` → succeeded in 19 s.

**Prevention:** Always run `nvidia-smi --query-gpu=index,memory.free --format=csv,noheader` before GPU jobs and pick the least-used GPU via CUDA_VISIBLE_DEVICES. Never assume GPU 0 is free on shared hosts.

## F3: pdb2pqr30 auto-generated APBS input writes potential file with `.pqr` extension

**Symptom:** Auto-generated `1fas.in` contained `write pot dx 1fas.pqr` (would overwrite the input PQR file). The APBS `write` keyword takes a *basename* (extension is added automatically), so this is technically wrong but not caught by pdb2pqr's input generator.

**Root cause:** pdb2pqr's `apbs-input` templating uses the PQR filename directly as the DX basename, producing collision-prone filenames.

**Workaround:** `sed -i 's|write pot dx 1fas.pqr|write pot dx 1fas_pot|'` before running apbs. Confirmed output DX file went to `1fas_pot.dx` and PQR was preserved.

**Prevention:** For any pdb2pqr30 --apbs-input run, always sed-fix the write basename to strip the `.pqr` extension. Consider filing a PR upstream to fix the template.

## F4: geoflow-auto parser rejected paper-Appendix inputs

**Symptom:** APBS 3.4.1 exited immediately (0.03 s) with no error message when parsing our geometric-flow input file. Same parameters that the paper's Appendix documents.

**Root cause:** APBS 3.4.1's `geoflow-auto` requires additional keywords (likely `dime`/`grid` triples, or specific `stopflag`) that the paper's Appendix does not document. The working template lives only in APBS's source tree `examples/geoflow/*.in`, which is NOT installed by conda-forge.

**Workaround:** None applied — reclassified as an untested claim (C9) and elevated to Open Question Q1.

**Prevention:** For any APBS solver invocation beyond `mg-auto` / `mg-manual`, clone the apbs source repo and cross-reference `examples/<solver>/*.in` for a working template. Add this as a general rule for future APBS replications: **paper Appendix ≠ working input syntax**.

## F5: Argo Claude Opus judge endpoint intermittent 502

**Symptom:** `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both returned HTTP 502 through both the direct Argo wrapper (`localhost:44497`) AND the LiteLLM aggregator (`<tailnet-aggregator>:4000`). Error: "Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage".

**Root cause:** Argo upstream returned a malformed message structure for Opus models — appears to be an intermittent Argo-side bug affecting Claude Opus specifically (LiteLLM aggregator surfaces it as a validation error). Not our fault.

**Workaround:** Fell back to `argo:gpt-5.2` on the same aggregator → succeeded on first try. This is still a free endpoint per project rules.

**Prevention:** Always have a fallback model list for LLM judge calls: `["argo:gpt-5.2", "argo:claude-opus-4.8", "argo:claude-opus-4.7", "argo:gpt-5.4"]`. First success wins. Log which model actually served the judgment.

## Failures NOT encountered (would-be-serious risks that turned out OK)

- APBS convergence did not fail — mg-auto with pdb2pqr's default grid sizing worked robustly on both proteins.
- No numerical instability at 0.15 M NaCl (Debye length correctly computed).
- LPBE↔NPBE gave consistent energies (0.02% relative diff), confirming both solvers are working end-to-end.
- Marker + nougat both extracted comparable amounts of text (555 vs 415 lines) — no PDF extraction pathology.
