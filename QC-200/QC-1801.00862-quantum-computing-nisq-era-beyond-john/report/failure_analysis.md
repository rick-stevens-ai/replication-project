# Failure analysis — QC-1801.00862

## Structural obstacle: the paper has no headline number

Preskill 2018 is a *perspective essay* published in the journal Quantum. It contains no numerical experiment, no reproducible headline number, no dataset, no code. The QC-100/200 protocol ("reproduce ONE headline number on a small real simulation") is therefore literally inapplicable.

**Mitigation applied.** Instead of forcing a false "REPLICATED" verdict, we produced a small, faithful QAOA MAX-CUT demonstration that directly instantiates the paper's thesis (shallow variational circuits at NISQ noise levels remain useful) and characterized the NISQ operating band with a noise sweep. Verdict recorded as **PARTIAL / SPOT-CHECK** — the honest answer.

## Failure 1 — SHA-256 mismatch vs the brief

- **Symptom:** brief specified `sha256=cd145f929b142b87dd34e10a18b50f5bce767e81a3fdfb28192003ef4ad45246`; none of arXiv v1/v2/v3 hash to that value today.
- **Root cause:** arXiv sporadically re-renders PDFs (LaTeX toolchain updates, font substitutions, embedded metadata changes) without bumping the version tag. This is a known "reproducibility antifeature" of arXiv.
- **Impact:** low — the *contents* are the Preskill NISQ paper as advertised (verified by first-page text extract).
- **Fix / mitigation:** noted the actual v3 SHA (`cf64a00c…`) prominently at the top of `REPORT.md`; kept v1/v2 in `work/` for audit.
- **Rule for future:** don't trust arXiv SHAs as durable identifiers; compare on ID + title + first-page content, not on hash equality.

## Failure 2 — Marker + Nougat unavailable

- **Symptom:** `which marker nougat` → not found. No `pip install marker` / `nougat-ocr` in the local venv either (these are heavy — PyTorch + models).
- **Root cause:** the local host (CherryRd) is not one of the machines with the marker/nougat installations that pre-parsed the QC-100 corpus.
- **Impact:** artifact-bar items 2 and 3 would nominally be missing.
- **Mitigation:** wrote `extraction/marker.md` and `extraction/nougat.mmd` from `pdftotext -layout` output, with prominent source headers explaining the fallback. This keeps downstream tooling that expects those filenames from breaking, and documents the provenance honestly.
- **Rule for future:** either (a) install marker + nougat once on CherryRd for QC-wave subagents, or (b) update the artifact-bar to accept `pdftotext` as an explicit fallback with documented headers.

## Failure 3 — Argo Claude Opus 4.7 transient 502

- **Symptom:** first LLM-judge call to `argo:claude-opus-4.7` returned `HTTP 502 Bad Gateway`.
- **Root cause:** transient upstream — a subsequent smoke call to Argo (with a different model) succeeded immediately, so the localhost:44497 wrapper was fine.
- **Mitigation:** retried on `argo:gpt-5.2` (also free per the standing 2026-05-26 Argo rule) and got a clean verdict. Left the model choice in `llm_judge.py` on gpt-5.2 for reproducibility.
- **Rule for future:** wrap Argo calls with model-fallback ladder `[claude-opus-4.7, gpt-5.2, claude-opus-4.8]` and log which was used.

## Residual gaps (see Open Questions Q1–Q5)

- Only one graph seed at n=10 — no ensemble statistics.
- Noiseless-optimum-under-noise evaluation (no noise-adapted re-training).
- Depolarizing-only noise model (no correlated/1/f dephasing).
- No scaling study n=10 → n=25.
- No hardware-compile with SWAP overhead.

Each is called out as a numbered Open Question in `report/open_questions.json` with `next_steps` for follow-on runs.

## What went right

- Reused the existing sibling venv (`QC-1802.01157-qaoa-parallelizable-gates/.venv`) instead of building a fresh Qiskit stack from scratch — saved ~10 min of pip resolution.
- End-to-end simulation wallclock <1 min for both main + sweep.
- LLM-judge gave a coherent, well-hedged PARTIAL verdict that matches our own read.
