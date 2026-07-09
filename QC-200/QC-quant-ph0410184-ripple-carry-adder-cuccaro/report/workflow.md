# Workflow — CDKM adder replication

## Step-by-step

1. **Fetch PDF** — `curl -sSL https://arxiv.org/pdf/quant-ph/0410184 -o paper.pdf` (111 KB; sha256 `a13d655d...`).
2. **Extract text** — `pdftotext paper.pdf work/paper.txt`; deposit as `extraction/marker.md` (with `-layout`) and `extraction/nougat.mmd` (no layout) with fallback-provenance headers (real marker / nougat not installed locally).
3. **Set up venv** — `python3 -m venv work/.venv && pip install qiskit qiskit-aer`. Qiskit 2.5.0, Python 3.14.
4. **Implement primitives** — MAJ (Fig 1), UMA 2-CNOT (Fig 2a), UMA 3-CNOT (Fig 2b) as Qiskit subroutines. See `work/cdkm.py`.
5. **Implement simple adder** — Section 2 / Fig 4: sequence of forward MAJ (with prev_carry threading) + CNOT to Z + reverse UMA. Parametric in `uma_variant`.
6. **Implement optimized adder** — Section 3 / Fig 5 pseudocode, direct transliteration (14 lines/time-slices). Valid n ≥ 4.
7. **Sanity: run `cdkm.py` main** — prints per-size resource counts for all three variants. Confirmed match paper formulas.
8. **Correctness — attempt Aer per-input** — too slow at n=8 (killed after ~2 min); pivot to classical-basis walker.
9. **Correctness — classical-basis walker** — `work/verify_fast.py` walks each circuit's gate list and permutes bits. Runs all 288,896 inputs across 3 circuit variants × 5 sizes in ~80s total. **100% pass.**
10. **Superposition check** — `work/verify_statevector.py` runs Qiskit-Aer statevector with A in H^n, verifies expected amplitudes and norm. All 3 test configurations return correct amplitudes and norm 1.0.
11. **Draper QFT control** — `work/draper_control.py` uses `qiskit.circuit.library.DraperQFTAdder` to cross-check with a functionally independent adder. First hand-rolled QFT adder had a wiring bug; replaced with library implementation. All 15 spot-checks pass.
12. **LLM judge** — Argo (free localhost:44497) `argo:gpt-5.2` returned **REPLICATED / confidence high** given the evidence bundle.
13. **Write reports** — REPORT.md (12 KB), REPORT.tex, open_questions.json (5 heavy questions with `next_steps`), workflow.md, artifacts_summary.md, failure_analysis.md.

## Tools & code

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.x | driver language |
| qiskit | 2.5.0 | quantum circuits + Aer sim |
| qiskit-aer | (latest via pip) | statevector simulator |
| poppler pdftotext | 25.x | text extraction (marker/nougat fallback) |
| Argo proxy | local :44497 | free LLM inference (gpt-5.2 for judge) |
| curl | system | PDF download |
| sha256sum | system | provenance hash |

Custom code (all in `work/` and mirrored to `report/evidence/`):
- `cdkm.py` — MAJ, UMA_2cnot, UMA_3cnot, simple_adder, optimized_adder, verify, encode_inputs, resource_counts
- `verify_fast.py` — exhaustive classical-basis test harness
- `verify_statevector.py` — quantum-superposition sanity check
- `draper_control.py` — Draper QFT-adder control comparison

## Effort estimate

Wall-clock: ~90 minutes total (including PDF fetch, venv setup, coding, three iterations to get verification harness fast enough, statevector check, Draper control, report writeup, LLM judge, and formatting).

Compute cost: negligible (local CPU, ~30s for n=8 classical simulation). No GPU used. No paid API calls (Argo proxy is free per lab standing policy).

## Followups suggested by open_questions.json

- Physical-gate-set transpilation study (Q1)
- Fault-tolerant T-count comparison to Draper (Q2)
- Small-n hand-optimized CDKM adders (Q3)
- Coupling-map robustness study (Q4)
- Noise sensitivity CDKM-vs-VBE (Q5)

Each is a well-scoped ~1-2 day study reusing the code in this replication.
