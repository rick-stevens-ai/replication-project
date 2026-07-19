# Failure Analysis — smejkal2022 (arXiv:2204.10844)

## What failed / friction
1. **Sign-change counting bug (fixed).** Initial d-wave lobe count returned 8 instead of 4
   because exact zeros at the nodes produced `sign==0` samples, each creating two apparent
   transitions in `np.diff(np.sign())`. Fix: drop exact zeros and add a periodic wrap-around
   term. Root cause: node-hitting discretization. Now returns 4 (correct d-wave).
2. **LLM-judge endpoint.** `argo:claude-opus-4.x` returned an upstream response-parse error
   through the LiteLLM aggregator (validation error on choices[0].message) on 2026-07-19.
   Worked around by using `argo:claude-sonnet-4.6` (also free Argo) — verified live before use.

## Residual gaps (scope limits, NOT failures)
- **C4 material DFT not attempted.** RuO2/MnTe/CrSb ab initio band structures need DFT; out of
  scope for CPU-only model replication. Documented as method-limited.
- **Reduced model.** Single-orbital d-wave only; g-/i-wave materials and multi-orbital
  hybridization not captured (recurring reduced-model caveat for this campaign).
- **Model-normalized units.** Energies in units of t; no absolute-meV comparison possible.
- **No SOC / magnons / transport.** Secs III.C–D observables outside the minimal electronic model.

## What's needed to close
Multi-orbital Wannier TB for a specific compound + SOC term → Berry curvature/AHC; mean-field
Hubbard for the interacting origin; linear spin-wave theory for magnons. See open_questions.json.

## Honesty note
This is a conceptual/model replication of a REVIEW — the verdict REPLICATED applies to the
symmetry-classification and representative-model claims (C1–C3), which are the paper's thesis,
NOT to a numeric match of any single material figure.
