# Failure analysis

Honest assessment of what didn't work, what we worked around, and what remains open.

## What failed

### F1 — marker / nougat unavailable
- **Symptom.** Neither `marker_single` nor `nougat` was installed on the local host (CherryRd) or on `uicgpu` (the `marlamr` conda env lacks the `marker` Python module).
- **Root cause.** Environment gap: no auto-provisioned marker/nougat on either host.
- **Workaround.** Used `pdftotext -layout` (poppler-utils) as fallback for both `extraction/marker.md` and `extraction/nougat.mmd`. Documented the fallback in `extraction/EXTRACTION_NOTE.md` and in an HTML-comment header inside each file.
- **Residual gap.** For a paper with heavy LaTeX math, marker/nougat would produce cleaner Markdown/MathML output than pdftotext. The pdftotext output preserves reading order but mangles multiline formulas.
- **Would need to close.** Install `marker-pdf` (~1 GB dependencies) in a dedicated conda env; add to standard replication env.

### F2 — PDF-analysis tool blocked
- **Symptom.** `pdf` tool refused local paths ("not under an allowed directory") and Anthropic credit balance too low; Google Gemini model name unknown; OpenAI PDF-extract plugin disabled.
- **Root cause.** Sandbox policy on local paths + expired API credits + missing plugin.
- **Workaround.** Read the paper directly from `extraction/paper.txt`; the paper is short (23 pages) and the technical content self-contained.
- **Residual gap.** None material.

### F3 — Argo Claude Opus 4.7 routing through LiteLLM
- **Symptom.** Judge call to `argo:claude-opus-4.7` returned `502 Bad Gateway` with `litellm.BadRequestError: OpenAIException - Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage`.
- **Root cause.** LiteLLM aggregator (as-configured on cherryrd) is unable to normalize the Anthropic response schema for Claude Opus 4.7 through the Argo proxy.
- **Workaround.** Switched to `argo:gpt-5.1` (also free); worked immediately. Documented in `attempt_log.md`.
- **Residual gap.** LiteLLM aggregator's Argo Claude route is broken; should be filed as a bug against the aggregator config.

### F4 — `read -r -d ''` in bash script + `set -e`
- **Symptom.** Bash judge-runner silently exited with rc=1 and no output.
- **Root cause.** `read -r -d ''` returns exit code 1 when it doesn't find the delimiter, which is a normal condition. Combined with `set -e`, the script died.
- **Workaround.** Rewrote judge caller in Python (`run_judge.py`).

### F5 — Python urllib.request 502
- **Symptom.** `urllib.request.urlopen` to the aggregator returned 502, but `curl` to the same endpoint worked.
- **Root cause.** Unclear — possibly `urllib` sending an unusual `User-Agent` or `Expect: 100-continue` that the aggregator/Argo rejects.
- **Workaround.** Switched to `subprocess.run(['curl', ...])`.

### F6 — Paper's printed ρ_{[2,1]}(σ_2) matrix (Section 3) not unitary
- **Symptom.** Both natural literal readings of the paper's printed 2 × 2 matrix have `U† U − I ≠ 0` at O(1).
- **Root cause.** Almost certainly a typesetting/OCR artifact in the paper (or an unusual convention). The paper's general formula (13)–(15) yields a unitary representation, and our numerically constructed ρ_{[2,1]}(σ_2) *is* unitary with the correct spectrum {−1, q}.
- **Workaround.** Reported as C7 in the claims table with `status = FAIL as printed`; the underlying algebra is fine.
- **Residual gap.** Erratum candidate. See Open Question Q2.

### F7 — Hadamard approximation plateau
- **Symptom.** BFS with pruning shows best Frobenius distance oscillating between 0.10 and 0.24 for depths 11–15 rather than smoothly decreasing.
- **Root cause.** BFS pruning (keeping only the 200,000 states closest to the target) prevents the search from exploring "detour" paths that would eventually converge, and greedy hillclimb gets stuck in local minima. Solovay–Kitaev's guarantee is *existence* of a length-L approximation, not that a greedy or truncated search will find it.
- **Workaround.** None in this pass; documented as Open Question Q1 and Q3.
- **Residual gap.** Would need a proper Solovay–Kitaev iterated construction to verify the theoretical 1/l² convergence.

## What was NOT attempted (honest)

- No full simulation of a BQP-hard instance via CS5 (Thms 2.2/2.3) — this would require full topological Hilbert-space construction on n = 3k ~ 60+ punctures and Aharonov–Ben-Or fault-tolerance layer. Weeks of engineering, not minutes.
- No comparison against alternative Fibonacci-anyon libraries (e.g., `Fibonacci_anyons` julia packages) — deliberately, to keep the replication independent.
- No cross-check of the ρ_{[3,3]}(σ_2) or ρ_{[4,2]}(σ_2) explicit block-structure printed in Section 3 (we do check the spectra + relations, which are the semantic content).

## Residual verdict caveats

The verdict is **REPLICATED**, but this specifically means the paper's *concrete numerical claims* — dimensions, unitarity, braid/TL relations, spectrum, multiplicities — are independently reproduced. The paper's *main theorems* (universality of CS5 for BQP, density of ρ(B_6) in SU(5) × SU(8), fault-tolerance under AB) are theorems, not numerical claims, and are not directly reproducible; we only confirm their numerical ingredients.
