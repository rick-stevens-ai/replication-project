# Failure Analysis — BVBRC-123

## What FAILED (technical failures encountered + resolution)

### F1. NCBI PMC direct PDF endpoint
- Attempt: `curl -sL https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10636080/pdf/`
- Result: HTTP 200 but 1,817 bytes of HTML (redirect/spam page), not PDF.
- Cause: PMC bulk-PDF endpoint blocks non-browser UAs even with UA spoofing.
- Fix: Switched to Europe PMC OA render `https://europepmc.org/articles/PMC10636080?pdf=render` → clean 2.26 MB PDF first try.

### F2. OpenClaw `pdf` tool
- Attempt 1: Path under `~/Dropbox/...` — rejected ("Local media path is not under an allowed directory").
- Attempt 2: Copied to `/tmp/` — same rejection.
- Attempt 3: Copied to `~/.openclaw/workspace/media/` — path accepted, but then Anthropic returned 400 "Your credit balance is too low", Google gemini-3-flash-preview returned "Unknown model", OpenAI gpt-5.5 returned "PDF extraction disabled".
- Cause: All 3 configured PDF-vision fallbacks unavailable.
- Fix: Used `pdftotext -layout` — actually worked better for numeric tables anyway. Free, deterministic, no LLM cost.

### F3. Paper's stated BioProject accession is WRONG
- Attempt: `datasets_v2 /genome/bioproject/PRJNA810265` (paper's cited accession).
- Result: 200 OK but returned *Pasteurella multocida* DC2020 by the same institution — wrong organism.
- Cause: Paper appears to have copy-pasted the wrong PRJNA number (likely a concurrent submission by the same lab, at the time of writing).
- Fix: Searched NCBI Assembly directly for strain name "Alim_AV_1000" → correct BioProject PRJNA827572, correct assembly GCA_026738955.1.
- **This became a claim-level contradiction** noted in the report.

### F4. Local `mlst` binary
- Attempt: `mlst --scheme aeromonas_1 refseq.fna`
- Result: `XS.c: loadable library and perl binaries are mismatched (got handshake key 0xfa80080, needed 0xf880080)`
- Cause: Homebrew Perl (5.42) vs abricate's bundled BioPerl (built against 5.40 or earlier). Classic macOS Perl ABI drift.
- Fix: Called pubMLST REST API directly instead — same result quality, no local dependency.

### F5. pubMLST REST first-attempt encoding
- Attempt: `curl -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode "sequence@refseq.fna" ...`
- Result: HTTP 400 "Failed to deserialize content: malformed JSON string".
- Cause: pubMLST REST endpoint requires JSON body, not form-encoded, and FASTA-with-headers breaks JSON string escaping.
- Fix: `Content-Type: application/json`, body `{"base64": true, "sequence": "<base64-encoded FASTA>"}` per pubMLST API docs. Worked first try after fix.

### F6. Argo local :44497 for LLM-judge
- Attempt: `claude-opus-4.7` at `http://127.0.0.1:44497/v1/chat/completions`.
- Result: HTTP 502 Bad Gateway.
- Cause: Transient argo-proxy issue; possibly upstream Anthropic rate.
- Fix: Switched to cherryrd litellm aggregator `http://<tailnet-aggregator>:4000/v1`. Tried claude-opus-4.8 (also 502), gpt-5.4 (worked).
- Lesson: for LLM-judge, always fall back through the aggregator's model list rather than pinning a single model.

## What was NOT ATTEMPTED (and why)

### N1. Wet-lab fish infection reproduction (Table 5)
- Requires live A. veronii isolate + BSL-2 aquarium facility + 40 healthy Shing fish.
- Explicitly out of scope for a bioinformatics replication wave.
- Documented as unverifiable in main report.

### N2. Full PHASTER prophage re-run
- PHASTER webserver requires interactive submission + email; PHASTEST REST exists but ~30 min compute.
- Used PGAP-annotation-based phage-gene clustering as a documented proxy.
- Would strengthen prophage claim if fully rerun; qualitative reproduction was sufficient for verdict.

### N3. Reannotation with Prokka/Bakta on same assembly
- Would isolate annotator-driven CDS-count variance (paper RAST 4229 vs my PGAP 4099).
- Ran out of time budget; noted in workflow.md as extension.

### N4. Full RaxML tree reconstruction
- Would validate paper's "TH0426 closest sibling" tree topology.
- Non-trivial to match the paper's exact PGFam alignment + MUSCLE + RaxML fast-boot; substituted ANI-triangulation which shows all comparators are essentially equidistant.

### N5. OrthoFinder proteome-conservation check vs NZ_CP044060.1
- Would test paper's "≥95% conserved" claim.
- OrthoFinder wall-clock ~10 min per pair; deferred as extension.

## Systematic lessons for the wave
1. **Never trust a paper's stated BioProject accession** without verifying via strain-name search. Two of BVBRC-123's own accessions (PRJNA, "SUB..." BioSample) were wrong-or-nonstandard.
2. **pdftotext > paid-vision PDF tools** for numeric-table extraction in bioinformatics papers. Free, deterministic, layout-preserving.
3. **pubMLST REST > local mlst binary** on macOS with Homebrew Perl. No brew reinstall cycle.
4. **LLM-judge fallback chain** matters: local Argo → aggregator with multiple models. Never pin a single model for the verdict step.
5. **Paper accession errors are common and consequential.** Building a systematic cross-check tool would be a useful project-wide utility.
