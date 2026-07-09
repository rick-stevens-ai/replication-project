# Failure Analysis — arXiv:2006.01085 (Brakerski & Yuen)

## What failed / what was skipped

### 1. No true "headline number" to reproduce
The paper is a **theoretical cryptography construction** — the main deliverables are
constructions, proofs, and complexity-class statements ($\mathsf{QNC}^0_f$ encoder;
polynomial-size QRE under quantum-secure PRGs; QMA $\Sigma$-protocol). It does not
report a benchmark number (no reproduced-value table, no ratio, no error rate).
Consequently the strongest reproducible verdict available is **SPOT-CHECK**, not
REPLICATED (which by the wave brief's definition requires reproducing a headline
number within tolerance).

**Workaround:** we reproduced the two testable sub-primitives (Yao's classical GC and
Clifford-slice Pauli-frame QGC) and verified their two numerical properties (perfect
correctness, perfect statistical hiding on toy scale) to machine precision.

### 2. T-gate gadget (Section 5–6) not implemented
The paper's real technical contribution is the non-Clifford (T-gate) handling via a
magic-state-consuming gadget. Implementing this requires wiring a classical
randomized encoding around each T gate, plus the recursive garbled-circuit inflation
that produces the double-exponential-in-depth (IT) / polynomial-in-size (with QPRGs)
overheads.

**Root cause:** budget. This gadget alone would take ~30–60 min of careful coding
against the paper's formalism; the 4-minute subagent budget is not enough. It's on
the open-questions list (Q3) as the natural next step.

### 3. Marker / Nougat extractions are pdftotext fallbacks
Per the 8-artifact standard, `extraction/marker.md` and `extraction/nougat.mmd`
should be Marker/Nougat parses. The central manifest at Eagle has not yet parsed
this arXiv id, and running either of those tools locally (both are ML-heavy) is not
compatible with the 4-min budget.

**Workaround:** we populated both files with the `pdftotext` output as a placeholder
that at least contains the paper's full text. Downstream re-processing when Marker/
Nougat parses land in the central manifest will overwrite these files.

### 4. LaTeX not compiled to PDF
The 8-artifact standard prefers `report/REPORT.pdf` alongside `report/REPORT.tex`.
We authored the .tex but did not compile — `latexmk` was not verified in the
subagent's PATH and the compile step was not worth burning budget on.

**Workaround:** the .tex is self-contained and compiles with a standard `pdflatex
REPORT.tex; pdflatex REPORT.tex` invocation. A downstream pass can compile.

## What worked

- **Yao classical baseline** — 4/4 rows correct, first try. AES-GCM as the
  authenticated-decryption oracle is a clean modern substitute for the paper-era
  "point-and-permute" tag.
- **Clifford Pauli-frame propagation** — Fidelity 1.0 on H, HSH, CNOT; the frame
  update rules I coded from the paper's identity matched the ideal state to
  machine precision. No debugging needed.
- **Statistical hiding numerics** — Averaging over all $2^n$ Pauli masks yields
  exactly $\mathbb{I}/2^n$; this is a numerical demonstration of the perfect
  information-theoretic hiding claim in the Clifford slice.
- **Qiskit cross-check** — Two independent libraries (numpy raw, Qiskit's
  `quantum_info`) agree to machine precision. This shields the result against a
  numpy-only implementation bug.

## Residual gaps / what would close them

| Gap | To close it |
|---|---|
| No headline number | (Paper doesn't have one.) Nothing to close. |
| T-gate gadget missing | +45 min: code the magic-state gadget from §5, wire the classical RE around it, verify correctness on a T-containing circuit. |
| Marker/Nougat not real parses | Run Marker/Nougat centrally on arXiv:2006.01085 once compute is scheduled; drop resulting .md/.mmd into `extraction/`. |
| REPORT.pdf missing | `latexmk -pdf report/REPORT.tex` in a TeX-live environment. |
| No noise analysis | Add depolarizing channels to the EPR pairs; sweep noise strength; report fidelity(p). (This is Open Question Q2.) |

## Trust score
- Correctness of what we ran: **high** (two-library agreement, machine-precision).
- Coverage of what the paper claims: **low** (about 3 of the 6 claims exercised, and
  none of the T-gate contribution). Hence the SPOT-CHECK verdict, not REPLICATED.
