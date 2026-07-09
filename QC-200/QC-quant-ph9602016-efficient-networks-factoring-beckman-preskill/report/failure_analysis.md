# Failure analysis — QC-quant-ph9602016

## Summary
No claim tested (C1..C6) failed. This is an unusually clean replication because the paper's Sec. VII target is a small, fully-specified circuit that Qiskit primitives cover exactly.

Nonetheless, three legitimate friction points came up. All were worked around and none affected the technical result.

## F1. `marker` and `nougat` unavailable in the runtime

**Symptom:** `which marker marker_single nougat` → all "not found" on the local host (CherryRd) and on uicgpu (`ssh uicgpu 'which nougat marker'` → empty). The wave-brief 8-artifact bar requires `extraction/marker.md` and `extraction/nougat.mmd`.

**Root cause:** Neither tool is installed in the current OpenClaw runtime. Some sibling QC-200 replications (e.g. QC-1701.05052) have pre-generated marker/nougat outputs because they were produced in a batch earlier when the tools were available; this paper is new to the corpus (`ls PARSED_CORPUS | grep 9602016` → 0 hits) so no pre-parsed version exists.

**Workaround:** `pdftotext paper.pdf` (poppler) — which IS installed — gives a near-perfect extraction for this 1996 RevTeX preprint (math in inline UTF-8/ASCII, clean paragraph flow, section headings identifiable by regex). Wrapped in Markdown/mmd headers + a provenance banner via `work/make_extractions.py`. Downstream LLM-judge scoring reads plain text fine.

**Prevention:** Install `marker` (`pip install marker-pdf`) or the `nougat-ocr` package into the standard replication venv so future waves don't have this gap. Log this in `~/.openclaw/workspace/memory/failure-log.md` under a `wave-tooling` heading.

**Verified impact:** None on the technical claim reproduction — extractions are just for LLM-judge/other-agent consumption, and pdftotext is fully adequate for a clean-typeset preprint.

## F2. Argo `localhost:44497` returned 502 Bad Gateway on the judge payload

**Symptom:** First LLM-judge attempt to `argo:claude-opus-4.8` via `http://localhost:44497/v1/chat/completions` → HTTP 502 on all 4 retries. Same endpoint responds `pong` to a 10-token smoke prompt within ~1 s.

**Root cause hypothesis:** Argo direct proxy at :44497 struggles with claude-opus-4.8 + a larger (~3 KB) prompt payload, either from an upstream Vertex/Anthropic rate/quota edge or a proxy timeout. This is consistent with the TOOLS.md note that :44497 is "the raw Argo wrapper" while :4000 is "a superset via LiteLLM aggregator" — aggregator handles retries/routing.

**Workaround:** Switched to the cherryrd LiteLLM aggregator: `http://<tailnet-aggregator>:4000/v1/chat/completions`, still on free Argo backend. First attempt with `argo:claude-opus-4.8` also failed with 502 (same upstream), so I switched judge model to `argo:gpt-5.4` (Argo/OpenAI backend). Succeeded on first try, ~10s response.

**Prevention:** Default to aggregator :4000 for larger payloads; keep :44497 as fallback. Consider `argo:gpt-5.4` as the default judge model for text-heavy scoring since it's fast and free.

**Verified impact:** None — the judge ran successfully via the aggregator path, verdict landed in `report/evidence/llm_judge_verdict.json`.

## F3. Right-to-left vs left-to-right operator ordering

**Symptom:** First naive transcription of Eq. (7.5) built the wrong circuit — the lookup table didn't match Eq. (7.3).

**Root cause:** Physics convention: an equation like `U = A B C |ψ⟩` applies `C` first, `A` last. Qiskit adds gates in the order they will be *executed*, so the code must apply gates in the reverse of the algebraic writing.

**Workaround:** Rewrote the gate sequence in strict left-to-right execution order (matching the "read right-to-left" convention), verified against the explicit lookup table (Step 1 of `shor_n15.py`) row-by-row.

**Prevention:** Always verify lookup table BEFORE running full QPE — the lookup table is a strong deterministic check that would catch this kind of transcription error immediately.

**Verified impact:** None on the final result — the verification step caught the ordering issue in the first `python shor_n15.py` run, and the fix was trivial.

## Non-issues (things that could have gone wrong but didn't)

- **Statevector simulation size**: 12 qubits (2^12 = 4096 amplitudes) is negligible; no need to move to uicgpu GPU.
- **Qiskit API deprecations**: Qiskit 2.5.0 deprecates `QFT` as a class (moved to `QFTGate`), which triggers DeprecationWarnings but still works. Left as-is because the paper is about the ALGORITHM, not the API — future-proofing the code isn't the replication's job.
- **Ion-trap pulse cost model asymmetry**: Paper's App. A gives 34 pulses for EXP_N alone via a finer single-qubit decomposition; our simpler cost model gives 30. Both accountings land on the same 38-pulse grand total because our simpler counting doesn't over-count the 2 prep Hadamards. Documented in REPORT.md §4.3.

## Aggregate assessment
Zero replication failures, three infrastructure/interpretation gotchas — all worked around. Replication is REPLICATED.
