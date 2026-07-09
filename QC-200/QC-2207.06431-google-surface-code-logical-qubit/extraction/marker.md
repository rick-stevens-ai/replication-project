# Extraction: arXiv:2207.06431 — "Suppressing quantum errors by scaling a surface code logical qubit"

> **Extractor:** `pdftotext -layout` (poppler) — Marker/Nougat not installed in this subagent
> venv and full model install (marker-pdf + torch + transformers) would exceed the subagent's
> compute/time budget for a 40-page paper with heavy figures. The full linearized text is in
> `../work/paper.txt` (2754 lines). This file curates the sections the replication depends on.

## Bibliographic
- **Title:** Suppressing quantum errors by scaling a surface code logical qubit
- **Authors:** Google Quantum AI (corresponding: H. Neven, neven@google.com)
- **arXiv:** 2207.06431v2 (20 Jul 2022) — published Nature 614, 676–681 (2023)
- **Preprint retrieved:** 2026-07-05 from https://arxiv.org/pdf/2207.06431 (SHA of local `paper.pdf` recorded in `../report/artifacts_summary.md`)

## Abstract (verbatim, verified against PDF)
> Practical quantum computing will require error rates that are well below what is
> achievable with physical qubits. Quantum error correction offers a path to
> algorithmically-relevant error rates by encoding logical qubits within many physical
> qubits ... We find our distance-5 surface code logical qubit modestly outperforms
> an ensemble of distance-3 logical qubits on average, both in terms of logical error
> probability over 25 cycles and logical error per cycle (2.914% ± 0.016% compared to
> 3.028% ± 0.023%). To investigate damaging, low-probability error sources, we run a
> distance-25 repetition code and observe a 1.7 × 10⁻⁶ logical error per round floor
> set by a single high-energy event (1.6 × 10⁻⁷ when excluding this event).

## Headline testable claims
| ID | Claim | Reported value | Unit |
|----|-------|---------------|------|
| C1 | Distance-5 rotated surface-code memory logical error per cycle | ε₅ = 2.914 ± 0.016 | % |
| C2 | Average distance-3 (4 subgrids) memory logical error per cycle | ε₃ = 3.028 ± 0.023 | % |
| C3 | Suppression factor for d=3→5 | Λ₃/₅ = ε₃/ε₅ ≈ 1.04 (>1) | — |
| C4 | d=25 repetition code logical error floor (with high-energy event) | 1.7 × 10⁻⁶ | per round |
| C5 | Same floor excluding the high-energy event | 1.6 × 10⁻⁷ | per round |
| C6 | Existence of a circuit-noise threshold (Λ<1 above, >1 below) shown in Fig 4c | qualitative | — |

## Device & method summary
- 72-qubit Sycamore-class superconducting processor.
- Rotated surface code, d=5 (49 qubits: 25 data + 24 measure) vs. d=3 (17 qubits: 9 data + 8 measure) on four quadrant subgrids.
- 25 stabilizer cycles per shot; measurement + reset each cycle; Hadamard + CZ scheduling.
- Decoders: minimum-weight perfect matching (MWPM) with correlated pij updates, plus tensor-network / BP baselines. Paper's headline ε values are from a correlated-matching decoder.
- Noise model in text is device-calibrated; Pauli+ simulations (Fig 4a) reproduce experiment.

## Threshold and Λ discussion (§ V and Fig 4)
- Λ_{d/(d+2)} = ε_d / ε_{d+2} > 1 requires operation below threshold.
- Fig 4c contour: sweeping a noise scale factor s, s=1.3 is above threshold (larger codes worse), s ∈ [1.0, 1.2] is close to threshold with turnaround at intermediate d, s=0.9 is below threshold (monotone suppression).
- Their device sits close to threshold; text: "device is close to threshold, reaching algorithmically-relevant logical error rates with manageable overhead requires Λ ≫ 1".

## Numerical values used in Verdict comparison
- ε₃ (experiment) = 3.028% per cycle
- ε₅ (experiment) = 2.914% per cycle
- Λ₃/₅ (experiment) ≈ 1.04

## What we don't reproduce
- Distance-25 repetition-code floor (C4/C5) requires their specific device + high-energy-event data.
- Exact device-calibrated noise model (they have per-gate p1, p2, readout, leakage). Our replication uses the standard uniform circuit-level depolarizing noise built into Stim.

(Full body text and references retained in `../work/paper.txt`.)
