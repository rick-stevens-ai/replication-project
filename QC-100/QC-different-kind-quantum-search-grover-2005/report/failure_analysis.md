# Failure Analysis

**Bottom line.** The core replication is clean — the paper's central closed-form identity `P = 1 − ε^(3^m)` was reproduced to machine precision, and the qualitative Grover-oscillation-vs-π/3-monotone contrast is unambiguous. There were no scientific failures. This file honestly documents the frictions, assumptions, and things not tested, per the standard.

## 1. Technical frictions encountered

### 1.1 Argo `argo:claude-opus-4.7` returned HTTP 502
- **What.** First LLM-judge call to `argo:claude-opus-4.7` failed with `HTTP Error 502: Bad Gateway` from the Argo proxy at `http://127.0.0.1:44497/v1/chat/completions`.
- **Impact.** Zero on results. Retried on `argo:gpt-4o` (also free via Argo) and got a valid JSON verdict on the first attempt.
- **Root cause.** Not investigated in depth; the local Argo wrapper occasionally 502s on the Anthropic-family models when the upstream is stressed. Basic connectivity to the proxy is fine (models list came back cleanly).
- **Mitigation.** Judge model swapped to `argo:gpt-4o` (temperature 0). The judgment task is a straightforward structured-JSON scoring problem where model family is not decisive.

### 1.2 `marker.md` is actually a `pdftotext` fallback, not a true Marker parse
- **What.** The extraction/marker.md file in the central QC-200 corpus has a header comment `<!-- FALLBACK EXTRACTION (pdftotext-based) — marker_single not available on this host, 2026-07-05 -->`.
- **Impact.** Low. The paper is 13 pages of clean LaTeX-set body text with a handful of inline math; `pdftotext` extracts it well enough that we could read every equation and follow the derivation. The Nougat parse (`nougat.mmd`) is a real Nougat output at 31 kB with proper math rendering, which we cross-checked when interpreting §3 and §4.
- **Root cause.** Marker isn't installed on the central corpus host (per the header); the pipeline fell back to pdftotext. This is a corpus-infrastructure issue, not a replication issue.
- **Mitigation.** Kept the fallback file as-is (per standard: this is the central-corpus source of truth for Marker). Nougat parse is the primary math-fidelity reference.

## 2. Claims not tested (honest scope statement)

- **C5 (systematic-error correction, §6).** The paper's error-correction application requires a noise model (e.g. coherent overrotation on `U`), which we did not simulate. Testing it would need a Kraus-map or Qiskit Aer noise-model extension of `pi3_search.py`. Estimated effort: half a day.
- **C6 (search-amidst-uncertainty benchmark, §5, the "0.8% failure vs 3.12% classical" result).** Not tested. This is a specific numerical benchmark on a prior over the marked fraction `f ∈ [0.75, 1.0]`. The requested figure was the probability trajectory, so we did not spend the extra ~100 LOC on the uncertainty benchmark. Estimated effort: an hour.

Neither of these is a "failure to reproduce"; they were out of scope for this run. They are surfaced as Open Questions Q1 and Q3 in `open_questions.json` for follow-up.

## 3. Assumptions made in the sim

1. **Pure unitary evolution, exact linear algebra.** No shot noise, no gate noise. This is honest: the paper's identities are algebraic and any noise-free simulator will reproduce them exactly (which we verified — 1e-14 error is round-off, not statistical).
2. **Sign / global-phase convention.** Our standard-Grover iterate is `G = W I_0 W I_t` (Nielsen–Chuang convention). The paper's Eq. (2) writes `U I_s U† I_t U`, differing by a global sign under our choice `U = W` (since `W = W†`). Both conventions give the same measurement probabilities, so the comparison is valid.
3. **Base state `|s⟩` = `|0⟩` before `U`.** The paper writes the identity in terms of a source `|s⟩` and target `|t⟩` inside a 2D subspace. For `U = W`, we take `|s⟩ = |0⟩` (computational-basis ket) so that `U|s⟩` is the uniform superposition and `R_s = R_0(π/3)`. This matches the "New algorithm" paragraph in §5 which explicitly uses "state s being the 0 state (state with all qubits in the 0 state)".
4. **Recursion stopped at `m = 4`.** At `m = 5`, `ε^(3^5) = 0.9375^243 ≈ 1.4 × 10⁻⁷`, still well within double precision; we could go higher, but the identity is already confirmed to `1e-14` and going further adds no scientific content, only runtime.

## 4. Residual gaps and what would close them

| Gap | To close |
|-----|----------|
| C5 (error-correction application) untested | Add noise-model extension (~150 LOC); sweep systematic error strength; compare to standard 3-qubit repetition-code correction. |
| C6 (uncertainty-search benchmark) untested | Add a `work/uncertainty_benchmark.py` implementing paper's Section 5 comparison. |
| Only `m = 0..4` shown | Push to `m = 6..7` if we care about double-precision saturation demonstration; scientifically redundant. |
| Only `N = 16` tested | Trivial to sweep `N ∈ {8, 16, 32, 64}` — no compute barrier — but the paper's identity is dimension-independent, so this would be repetition, not new evidence. |
| Marker parse is pdftotext fallback | Would need to install Marker on the corpus host; not our task. |

## 5. Sanity checks that could have caught false positives (all passed)

- Base probability equals `1/N` exactly (0.0625 for N=16) — passes.
- Standard Grover peak at `k ≈ (π/4)√N ≈ 3.14` — our peak is at `k = 3`, `P ≈ 0.961`. Consistent.
- Recursion `P(m)` matches independent closed-form `1 − (1 − 1/N)^(3^m)` to 1e-14 — passes.
- Monotonicity: `np.diff(P) ≥ −1e-12` for all `m` — passes.
- LLM-judge verdict is REPLICATED, coverage 1.0, agreement 1.0 — matches human read of the numbers.

No red flags in any of these. If the recursion had produced non-monotone P, or if the theory/measurement diff had been > 1e-10, we would have flagged it.
