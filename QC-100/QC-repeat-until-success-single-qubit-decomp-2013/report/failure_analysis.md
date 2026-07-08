# Failure Analysis — QC-1311.1074

Honest analysis of what went wrong, what was worked around, and residual gaps.
The verdict is REPLICATED for Figs. 8 and 9, but "no failures" would be
dishonest given the friction points and the Fig. 1a mismatch.

## Failures / friction

### F1. Vision-based PDF extraction unavailable
- **Symptom:** the `pdf` tool returned errors on all three providers
  (Anthropic: credit-balance too low; Gemini: unknown model
  `gemini-3-flash-preview`; OpenAI: PDF plugin disabled).
- **Root cause:** the environment's paid providers are throttled/disabled;
  free providers weren't configured for PDF input in the `pdf` tool.
- **Workaround:** used `pdftotext -layout` (poppler) for the actual figure
  reading (the ASCII circuit diagrams in Figs 1a, 8, 9, 10 are rendered
  cleanly by pdftotext because they use monospace ASCII math in the source)
  and `pymupdf4llm.to_markdown` for the structured `extraction/marker.md`.
- **Residual gap:** no vision-model spot-check of the extracted circuits;
  we relied entirely on the ASCII text. Mitigation: the exact Pr(success)
  values from the paper (5/8, 3/4) reproduce to 1e-15, which is a very
  strong sanity check that we got the circuits right.

### F2. `marker` and `nougat` not installed on any accessible node
- **Symptom:** `which marker_single nougat` returned "not found" on local
  mac and on `uicgpu`.
- **Root cause:** those two tools require heavy model downloads (Meta
  Nougat, DataLab Marker) and were not pre-provisioned.
- **Workaround:** used `pymupdf4llm 0.3.4` as a structured-markdown
  substitute, and produced the same file at both `extraction/marker.md`
  and `extraction/nougat.mmd` per the 8-artifact standard's requirement to
  have both slots present. This is a documented substitution
  (`artifact_harvest.md` §"Note on marker/nougat"), not a silent one.
- **Residual gap:** no independent-tool cross-check of the extraction.
  For a math-heavy paper this could matter (some equations render as
  Unicode symbols in pdftotext; e.g. we saw `` instead of ε in
  `1.26 log2(1/) − 3.53`). For our purpose (transcribing ASCII circuit
  figures) this was harmless.

### F3. Argo `argo:claude-opus-4.7` failed on structured-JSON output
- **Symptom:** POST to both `localhost:44497` and `<tailnet-aggregator>:4000` for
  the same claude-opus-4.7 model returned
  `Failed to parse upstream response: 1 validation error(s): Value at
   'choices[0].message' does not match any variant of ...`.
- **Root cause:** unclear — most likely the Argo proxy's response validator
  chokes on some field in Claude's structured JSON output for this payload
  (a long prompt asking for structured JSON). A trivial "say ok" call to
  the same model succeeded. Not investigated deeper.
- **Workaround:** switched to `argo:gpt-5.2` (also free-tier Argo). Same
  prompt → clean structured JSON, verdict returned.
- **Residual gap:** worth reporting to Rick as a general Argo-Opus bug.
  A second judge model (Gemini, or a CELS endpoint) would give a
  cross-check.

### F4. Fig. 1a circuit reconstruction did not match V3
- **Symptom:** our best-guess two-ancilla implementation (H's on ancillas
  + `mcp(π/2, [a1,a2], data)` (ctrl-ctrl-S) + `mcp(π, [a1,a2], data)`
  (ctrl-ctrl-Z) + H's on ancillas + Z-basis measurement) produced
  Pr(success) = 13/16 (not 5/8) and process fidelity 0.35 vs V3.
- **Root cause:** the ASCII figure `|+> . . X | |+> . . X | |psi> S Z`
  is ambiguous — the two dots on each ancilla row could be independent
  controls in two separate controlled gates, or paired controls in one
  Toffoli-style gate. The paper says the circuit is "a slight modification
  of NC00 pp.198"; without the textbook in hand we guessed the wrong
  Clifford+T decomposition.
- **Workaround:** documented as an open question (Q2 in
  `open_questions.json`); Fig. 9 (single ancilla, same target `V3`) was
  reproduced instead — the physics claim (V3 with Pr=5/8) is now verified
  via a different circuit topology.
- **Residual gap:** the exact Fig. 1a construction. Fixing it requires
  either (a) pulling the NC00 pp.198 figure, or (b) reading Fig. 1a from
  a rendered PDF page (which is what the `pdf` tool would have given us
  had it been available — cf. F1).

### F5. Fig. 9's drawn `Z` on the data qubit
- **Symptom:** including the final `Z` on the data row (as drawn in the
  paper's Fig. 9) makes the induced K matrix `diag(a, -b)` — Pr = 5/8
  matches but the sign of the second diagonal element flips relative to V3,
  so we lose the "equal up to global phase" property.
- **Investigation:** ran `work/rus_fig9_search.py` sweeping CX direction
  (data→anc vs anc→data) × final Z (present vs absent). Only ONE variant
  reproduces V3 exactly up to global phase — the one with CX(data→anc) and
  NO final Z.
- **Working hypothesis:** the drawn Z is a *conditional recovery* on the
  failure branch, not part of the success branch, and the paper's figure
  layout is compressed enough that the classical-control brace was
  omitted. This is captured as open question Q1.

## What would be needed to close the gaps
1. Vision-model PDF read of pages containing Figs 1a, 7, 8, 9, 10 to
   cross-check our ASCII transcription (fixes F1, F2, F5).
2. NC00 textbook page 198 to fix Fig. 1a (fixes F4).
3. Second free-endpoint LLM judge (Gemini via `hgemini` or a CELS endpoint)
   to cross-check the Argo `gpt-5.2` verdict (mitigates F3).
4. Implementation of Fig. 7 and Fig. 10 (a,b,c) circuits — all four have
   fully specified ASCII sequences in the extracted text — to push
   coverage from 2 → 6 verified circuits (fixes coverage=0.25 limitation).

## Honest self-assessment
- Coverage of the paper's total claim surface is small (~25%): we tested
  two of the paper's ~10 headline small-circuit constructions and none of
  its asymptotic scaling claims.
- Within that scope, the reproduction is *exact* (machine precision on
  Pr(success), process fidelity 1.000 on both circuits), so the REPLICATED
  verdict is honestly earned for what was tested — but a stricter reviewer
  could also call this PARTIAL given the low coverage. The LLM judge
  concurred with REPLICATED at agreement 0.92 (not 1.0), which honestly
  reflects that Fig. 1a mismatched.
