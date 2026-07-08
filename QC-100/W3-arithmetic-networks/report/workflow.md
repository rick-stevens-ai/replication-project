# Workflow — W3 Arithmetic Networks (Vedral-Barenco-Ekert 1996)

## Paper Identification
- Vedral, Barenco, Ekert, *Quantum Networks for Elementary Arithmetic
  Operations*, Phys. Rev. A **54**, 147–153 (1996).
- Foundational reversible-circuit constructions underlying Shor's algorithm.

## Replication Strategy
1. **Read the paper's Figs. 2–6** — extract the exact gate-level structure of:
   - Fig. 2/3: plain ripple adder + CARRY/SUM primitives
   - Fig. 4: adder-mod-N (add a, subtract N, overflow-detect, conditional
     add-back, temp reset via subtract-a / re-add-a)
   - Fig. 5: controlled modular multiplication
   - Fig. 6: modular exponentiation a^x mod N
2. **Implement each subnetwork in `replicate.py`** using only NOT/CNOT/Toffoli
   (the paper's own gate set). No modern quantum library primitives.
3. **Validate at four levels**:
   - Exhaustive basis-state sweep (all (a,b) at small n) with temp-register
     zero-check
   - Full permutation-unitarity check on the plain adder (n=2,3) over all
     2^(3n+1) basis states
   - Gate-count scaling by counting emitted elementary gates for n=2..8 and
     linear-fitting
   - Modular-exp value/order tables to confirm the composed circuit yields
     the correct classical function
4. **Cross-check the paper's memory formulas** 7n+1, 5n+2, 4n+3 by evaluating
   for N ∈ {15, 21, 35} and comparing to the "about 20 ions for N=15" claim.

## Tools Used
- Python 3 with numpy (permutation-unitarity enumeration).
- No external quantum-simulator dependency (Qiskit/Cirq deliberately avoided
  to keep the implementation independent of library-provided primitives).
- All computation local; no external endpoints.

## Verification Hierarchy
| Level | What it proves | Where applied |
|---|---|---|
| Basis-state sweep + temp reset | classical-reversible correctness | plain adder n=2..4, mod-adder N=3..15 |
| Permutation over 2^k | genuine reversible unitary | plain adder n=2,3 |
| Gate-count linear fit | matches paper's O(n) asymptotic | adder n=2..8 |
| Composition argument | mult O(n²), exp O(n³) | structural |

## Artifacts (this replication)
- `paper.md` — extracted paper structure + claim list
- `replicate.py` — independent gate-level reimplementation
- `results.json` — machine output of every sweep + fit
- `REPORT.md` — top-level human report (original)
- `report/REPORT.tex` — full LaTeX report with critique + open questions
- `report/open_questions.{json,section.tex}` — 5 open questions
- `report/failure_analysis.md` — honest critique of scope limits

## Verdict Rationale
Every headline claim was independently reimplemented and exhaustively
validated at the stated scope. The two scope limits (full-statevector
verification of controlled mult/exp; classical-vs-reversible overhead
comparison) are honestly flagged in the critique. Verdict: **REPLICATED**.
