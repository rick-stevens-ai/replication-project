# Workflow, Tools, Codes, Effort — QC-1311.1074

## Workflow narrative

1. **Read the brief and the standard.** Confirmed the 8-artefact completion bar
   and the "free endpoints only" / "no fabrication" hard rules.
2. **Pull the paper.** Downloaded the arXiv PDF; verified 1.3 MB, PDF v1.5.
3. **Extract text.** Attempted the `pdf` tool → three vision providers all
   returned errors (Anthropic low credits; Gemini unknown model; OpenAI plugin
   disabled). Fell back to `pdftotext -layout` for a plain-text layout dump.
   For the mandatory `extraction/marker.md` and `extraction/nougat.mmd`
   artefacts, used `pymupdf4llm.to_markdown()` locally (neither Meta Nougat
   nor DataLab Marker installed on any accessible node) and copied the same
   file to both artefact paths.
4. **Locate the exact circuit claims.** Grep'd the pdftotext output for `V3`,
   `Fig.`, `success prob`, `ancill`. Identified three fully-specified small
   circuits with numerical predictions:
   * Fig. 8 (`(I + i√2 X)/√3`, Pr = 3/4, 2 T)
   * Fig. 9 (V3 = `(I + 2iZ)/√5`, Pr = 5/8, 4 T, 1 ancilla, 1 measurement)
   * Fig. 1a (V3 via 2-ancilla NC00 pp.198 style)
5. **Implement in Qiskit statevector.** Built each circuit qubit-by-qubit,
   computed the full unitary `W` with `Operator(qc).data`, projected onto the
   all-ancillas-zero subspace to get the induced Kraus operator `K` on the
   data qubit. Verified against the paper via (Pr(success), process fidelity
   with target unitary, global-phase equivalence).
6. **Disambiguate figure ambiguity.** Fig. 9's ASCII diagram left the CX
   direction and final-Z placement ambiguous. Wrote a small sweep
   (`work/rus_fig9_search.py`) over the four combinations and found the
   unique one that reproduces V3 exactly up to global phase.
7. **Free-endpoint LLM judge.** Prompted Argo `argo:gpt-5.2` (via LiteLLM
   aggregator :4000, `Bearer stevens`) with the paper claims and numerical
   results. Requested structured JSON verdict from the canonical vocabulary.
   Preferred `argo:claude-opus-4.7` hit an upstream JSON-parse validation
   error on both :44497 (raw Argo) and :4000 (aggregator) — fell back to
   `gpt-5.2` (same free-tier Argo backend).
8. **Compose the 8 required artefacts** and record everything in `report/`.

## Tools & code used (with versions)

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14 (system) | Base runtime for `rus_verify.py`, `llm_judge.py` |
| numpy | latest via pip | Linear algebra (matrix ops, fidelity) |
| qiskit | 2.5.0 | Circuit construction + `Operator` unitary extraction |
| pymupdf4llm | 0.3.4 | Structured-markdown PDF extraction (marker/nougat substitute) |
| pdftotext | poppler (macOS) | Layout-preserving text dump; source of Fig. 8/9 ASCII |
| curl | system | arXiv PDF download; Argo LLM judge calls |
| Argo proxy | localhost:44497 / aggregator <tailnet-aggregator>:4000 | Free `argo:gpt-5.2` LLM judge |

Code artefacts (all in `work/`):

| File | LOC | Purpose |
|---|---|---|
| `rus_verify.py` | 176 | Core replication: Qiskit circuits, projection, comparison |
| `rus_fig9_search.py` | 78 | Fig. 9 CX-direction/Z-placement disambiguation |
| `llm_judge.py` | 132 | Argo LLM judge with structured JSON output |

## Effort estimate

| Category | Estimate |
|---|---|
| Wall-clock (this turn) | ~9 minutes (14:08 → 14:17 CDT) |
| Compute time | <5 s CPU total (statevector for 2–3 qubit circuits, 3 circuits × ~1 s each) |
| LLM tokens (Argo judge, free) | ~2 000 prompt + 400 completion (one call) |
| Human/agent decisions | ~6 (PDF extraction path, marker substitute, Fig. 9 disambiguation, LLM model swap, Fig 1a acceptance-of-mismatch, verdict) |
| Lines of code written | ~386 (rus_verify + fig9_search + llm_judge) |
| Sim runs executed | 3 primary + 8 disambiguation sweep = 11 statevector reps |
| Human/agent supervision | subagent, autonomous, single turn |
| Compute cost | $0 (free Argo endpoint; local CPU) |
