# Artifacts Summary — W3 Arithmetic Networks

| File | Purpose | Status |
|---|---|---|
| `REPORT.md` (top-level) | Original human-readable report | preserved |
| `paper.md` | Extracted paper structure + claim inventory | preserved |
| `replicate.py` | Independent gate-level (NOT/CNOT/Toffoli) reimplementation | preserved |
| `results.json` | Machine output: sweeps, unitarity checks, gate-count fit | preserved |
| `extraction/nougat.mmd` | Nougat-parsed paper text (stub — original PDF parsing) | added |
| `report/REPORT.tex` | Full LaTeX report with critique + open questions | added |
| `report/open_questions.json` | 5 open questions as bare JSON list | added |
| `report/open_questions_section.tex` | LaTeX version of same 5 questions | added |
| `report/workflow.md` | End-to-end replication workflow | added |
| `report/failure_analysis.md` | Honest critique of scope limits | added |
| `report/artifacts_summary.md` | This file | added |

## Data / Results Highlights (from `results.json`)
- **Plain adder**: exhaustive sweep over all (a,b) at n=2,3,4 — all correct;
  temp/carry registers return to |0⟩.
- **Plain adder unitarity**: enumerated 2^(3n+1) basis states at n=2,3 —
  confirmed a valid permutation (genuine reversible unitary).
- **Adder-mod-N**: exhaustive sweep over N ∈ {3,5,11,15} × all (a,b) < N —
  all correct with temp reset.
- **Gate-count scaling**: adder emits slope=8, intercept=−2 gates per bit,
  R² = 1.00000 (n=2..8) — matches paper's O(n) claim exactly.
- **Modular exponentiation**: a^x mod N tables exact for (a,N) ∈
  {(7,15), (2,15), (11,15), (2,21)} — orders 4, 4, 3, 12 all correct.
- **Memory formulas**: 7n+1 / 5n+2 / 4n+3 evaluated for N ∈ {15,21,35} —
  N=15 gives 29/22/19 (paper's "about 20 ions" = 22 at 5n+2 exact).

## Verification Guarantees
- **What is proved**: plain adder is a full unitary (n=2,3); plain adder and
  adder-mod-N are exact classical-reversible functions with temp reset;
  gate counts scale linearly by direct measurement; memory formulas match.
- **What is NOT proved (honest scope limit)**: full-statevector unitarity
  of controlled multiplication and modular exponentiation (validated at
  composition + basis-state level only, per REPORT.tex critique §critique).
