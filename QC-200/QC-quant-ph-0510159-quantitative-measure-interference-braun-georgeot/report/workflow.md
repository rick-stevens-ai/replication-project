# Workflow — quant-ph/0510159 replication

## Timeline (single subagent turn, ~2026-07-05 16:16 CDT)

1. **Fetch + skim (2 min).** `curl` the PDF, `pdftotext -layout`, grep for
   the key equations ("I(P)", "Hadamard", "i-bit", "Grover", "Shor").
2. **Extract definition (2 min).** Confirmed Eq. 6 (general P) and Eq. 8
   (unitary case: `I(P(U)) = N - Σ|U_ik|^4`) from the layout dump.
3. **Implement + run (5 min).** Single 200-line Python file
   `report/evidence/interference.py`, NumPy only. Covers:
   - standard gates (I, X, Y, Z, H, CNOT, SWAP, Toffoli),
   - Walsh-Hadamard tensors W_1..W_4,
   - QFT_1..QFT_5,
   - beam-splitter closed-form check across 6 angles,
   - tensor identity across 16 pairs,
   - Grover for n = 3..8 (full unitary + algorithm-only),
   - teleportation encoder (8x8 unitary).
4. **Write extraction fallbacks (marker/nougat) (3 min).** Neither tool was
   installed; central corpus had nothing; produced schema-compatible manual
   extractions of the ~8 core equations plus a pdftotext layout dump.
5. **Write REPORT.tex + failure_analysis + artifacts_summary + open_questions
   (10 min).**

Total wall clock: ~25 min.

## Tools & versions

| Tool             | Version                              | Role                       |
|------------------|--------------------------------------|----------------------------|
| Python           | 3 (system)                           | driver                     |
| NumPy            | system (>= 1.20)                     | dense matrix ops           |
| pdftotext        | poppler `pdftotext -layout`          | PDF -> text                |
| curl             | system                               | arXiv PDF fetch            |
| marker           | not installed (fallback used)        | intended parse (see failure_analysis) |
| nougat           | not installed (fallback used)        | intended parse (see failure_analysis) |
| Qiskit/Cirq/Stim | not needed                           | measure is pure linear algebra |

The interference measure of Eq. 8 is a two-line NumPy function; no external
QC framework was required. The Grover unitary is built explicitly with
`np.linalg.matrix_power(D @ O, k)` — direct dense evaluation for n ≤ 8
(N ≤ 256) is trivial (< 1 s wallclock for the full sweep).

## Estimate of work

- **Lines of code (real, not comment):** ~180 in `interference.py`.
- **Independent numeric probes:** 17 standard-gate claims + 6 beam-splitter
  angles + 16 tensor pairs + 6 Grover n-values + 1 teleportation = **46
  matched or bounded probes**, of which 45 match to machine precision and 1
  (Grover "actually used" asymptote) matches only qualitatively due to a
  definitional ambiguity.
- **Papers cross-referenced:** just this one; no follow-up literature dive
  (would be Q1 in the open questions).
- **Skipped:** Shor sim (Q5) — would need ~1 h more to build and cross-check
  the 12-qubit factoring circuit for R=15.

## Reproduction command

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0510159-quantitative-measure-interference-braun-georgeot
python3 report/evidence/interference.py
# Reads only its own hard-coded gates and produces report/evidence/results.json
# and report/evidence/run.log.
```
