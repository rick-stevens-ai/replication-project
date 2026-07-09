# LLM-Judge Verdicts (Argo proxy — free endpoints only)

All 5 successful judges polled 2026-07-04 via `http://localhost:44497/v1` with the SAME prompt (see `work/judge_pde12.py`).

| Judge (model) | Verdict | Note |
|---|---|---|
| argo:gpt-5.2 | **PARTIAL** | "a central component is corroborated, but the main 3D non-uniqueness claim was not independently reconstructed" |
| argo:gpt-5   | **SPOT-CHECK** | "core theorem is not rederived, but the ingredients and availability checks support the paper's methodology" |
| argo:gpt-5.1 | **SPOT-CHECK** | "given that the core claim remains a rigorous theorem and the replication is a targeted numerical spot-check of a crucial ingredient rather than a full reconstruction of the proof, the appropriate classification is a spot-check" |
| argo:o3      | **SPOT-CHECK** | "a methodological spot-check, not a full reproduction of the main theorem" |
| argo:gemini-2.5-pro | **SPOT-CHECK** | "this verification of artifact availability and method plausibility, without a full re-derivation of the proof, is the definition of a successful spot-check" |

**Consensus (4/5): SPOT-CHECK.** GPT-5.2's PARTIAL is essentially the same substantive judgment (a component is corroborated) but with a slightly more generous label — for a purely analytic theorem where reproduction of the proof itself is not on offer, SPOT-CHECK is the canonically-correct wave-brief vocabulary.

## Judges not usable today
- argo:claude-opus-4.7 / argo:claude-opus-4.8 — Argo proxy returned HTTP 502 with `Failed to parse upstream response: Value at 'choices[0].message' does not match any variant`. Upstream schema bug in Argo today, not a credit issue.
- argo:gpt-5.5 — rejects `temperature=0.0` (`Only the default (1) value is supported`); skipped to keep reproducibility.
