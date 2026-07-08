# Workflow, Tools, Codes, Effort Estimate

## Narrative
1. Pulled paper PDF from arXiv (`https://arxiv.org/pdf/quant-ph/9805082`).
2. Extracted text via `pdftotext -layout` and inspected key theorems (Theorem 1–6, Corollary 2).
3. Identified the reproducible testable claims (C2 = Theorem 5; C3 = Corollary 2).
4. Set up Python venv under `work/venv`, installed Qiskit 2.5.0 + qiskit-aer 0.17.2 + numpy.
5. Built independent implementation `work/quantum_counting.py` — analytic QPE marginal from the two Grover eigenphases using the Dirichlet-kernel formula. This is faster and more numerically clean than shot sampling.
6. Built `work/verify_qiskit.py` — a gate-level Qiskit circuit for `Count(F,P)` that constructs G as a UnitaryGate, uses controlled-G^{2^j} with count_reg[j], then inverse QFT with swaps.
7. Debugged qubit-ordering issue: first attempt disagreed by L∞ ≈ 0.6 with analytic. Root cause: Qiskit's little-endian gate matrix indexing requires the control qubit to be LAST (MSB) when using block-diagonal `diag(I,U)`. Fixed and re-verified.
8. Multi-case verification `work/verify_qiskit_multi.py` on 7 diverse (n,t,p) — all agree to L∞ ≤ 3e-15.
9. Ran main sweep: n ∈ {4,5,6}, t swept, p ∈ {3..8}, 90 configs total. All 90 satisfy Theorem 5.
10. LLM-judge scoring `work/llm_judge.py` — Argo free endpoint (localhost:44497). First tried `argo:claude-opus-4.8` (upstream JSON parse error at ~26k prompt), fell back to `argo:gpt-5.4` (worked).
11. Wrote LaTeX report and compiled to PDF with `pdflatex`. Wrote all 8 required artifacts.

## Tools / codes / versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (system) | Runtime |
| Qiskit | 2.5.0 | Circuit construction (verify_qiskit.py) |
| qiskit-aer | 0.17.2 | (installed; Statevector used from qiskit.quantum_info) |
| numpy | latest at install (2.x) | Linear algebra, Dirichlet kernel |
| pdftotext | Poppler | Paper extraction (marker/nougat substitute) |
| pdflatex | TeX Live 20260301 | Report compilation |
| curl | system | Argo endpoint calls |
| Argo proxy | localhost:44497 | Free LLM inference (gpt-5.4 for judge) |

## Codes written by this replication
| Path | Lines | Purpose |
|---|---|---|
| `work/quantum_counting.py` | ~200 | Analytic Grover operator + QPE marginal + sweep |
| `work/verify_qiskit.py` | ~110 | Gate-level Qiskit Count(F,P) circuit + sanity single-case check |
| `work/verify_qiskit_multi.py` | ~50 | Multi-case gate-vs-analytic cross-check |
| `work/llm_judge.py` | ~155 | Argo-endpoint LLM-judge harness |

Total: ~515 lines of new Python + 260 lines of LaTeX + support docs.

## Effort estimate
- Wall-clock: ~90 minutes (single agent, single host).
- Compute: fully local on CherryRd (Mac), no GPU needed. Peak memory well under 100 MB (largest matrix at n=6 is 64×64).
- Sweep runtime: ~seconds total across 90 configs.
- Human/agent steps: setup(1) → extraction(1) → analytic impl(1) → sweep(1) → qiskit gate verify + debug(1) → multi-case verify(1) → LLM judge(1) → 8 artifacts + LaTeX build(1). ≈ 8 major steps.
- Runs executed: 3 sweep runs (initial + verify + re-run for logging), 2 qiskit verify runs (debug + fix + multi-case), 2 LLM-judge calls (opus fail → gpt-5.4).
