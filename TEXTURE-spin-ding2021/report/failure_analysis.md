# Failure Analysis — ding2021 (arXiv:2105.04495)

## What failed / friction
- No code failures; ran clean first try. LLM-judge opus-4.x aggregator parse error 2026-07-19 (used free sonnet-4.6).

## Residual gaps (=> PARTIAL)
- **Experimental data not reproduced.** This is an experimental paper (Py/oxidized-Cu Hall bars,
  6T, 300K). The measured MR ratios, the Cu*-thickness curve absolute values, and the Py-thickness
  spin-diffusion/dephasing-length extractions require the physical samples and are out of scope.
- **Phenomenological coefficients.** D_AMR, D_SMR are hand-chosen; the replication is a THEORETICAL
  consistency check that the OREMR angular framework distinguishes OREMR from AMR (the paper's core
  argument), not a fit to measured data. C1-C3 are analytic consequences of the model.
- **Interface conductance not microscopic.** The orbital mixing conductance is not computed from an
  interface Rashba model (Open Q1).

## What's needed to close
Interface spin+orbital Rashba model for G_orb (Open Q1); coupled spin+orbital diffusion fit to the
thickness data (Open Q2); shunt-vs-quenching decomposition (Open Q4). See open_questions.json.

## Honesty note
Verdict PARTIAL is correct: the SMR/OREMR angular-dependence theory + the beta-scan discriminator +
the interfacial signature are reproduced; no measured experimental observable is independently
regenerated. Experiment-paper theory-core replication.
