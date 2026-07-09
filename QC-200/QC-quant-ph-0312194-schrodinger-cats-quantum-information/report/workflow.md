# Workflow — Replication of arXiv:quant-ph/0312194

## Goal
Independently reproduce the numerically-checkable core identities of the cat-qubit
toolbox proposed by Gilchrist, Nemoto, Munro, Ralph, Glancy, Braunstein, Milburn (2003).

## Steps executed
1. **Fetch paper**
   - `curl -sL https://arxiv.org/pdf/quant-ph/0312194 -o paper.pdf`  (173 kB, 10 pages, v1 24 Dec 2003)
2. **Verify authors from fetched PDF** (per QC brief)
   - `pdftotext -layout paper.pdf work/paper.txt`
   - First page confirms authors: A. Gilchrist, K. Nemoto, W. J. Munro, T. C. Ralph,
     S. Glancy, S. L. Braunstein, G. J. Milburn.
3. **Environment setup**
   - `python3 -m venv work/venv && source work/venv/bin/activate`
   - `pip install qutip numpy scipy`
4. **Identify checkable claims** by skimming the extracted text:
   - C1: cat-state normalization/orthogonality
   - C2: `<alpha|-alpha> = exp(-2|alpha|^2)` scaling
   - C3: two-mode cat Bell concurrence -> 1 as alpha grows
   - C4: linear phase shift `exp(-i*pi*n_hat)` = Z gate on cat basis
5. **Implement + run**
   - Wrote `report/evidence/cat_replication.py` (~200 lines, Fock dim 40, alpha sweep
     {0.5,1.0,1.5,2.0,2.5,3.0}).
   - Ran; results saved to `report/evidence/results.json`.
6. **Extractions**
   - Marker and Nougat were not installed on the host at run time; the QC brief
     permits fallback. `extraction/marker.md` and `extraction/nougat.mmd` therefore
     contain `pdftotext -layout` output with an explicit fallback header at the top
     of each file. No other central corpus parse was pulled in (search under
     `~/Dropbox/REPLICATE-PROJECT/` for parses timed out and was killed).
7. **Write reports**
   - `report/REPORT.tex` (11.9 kB) with per-claim MATCH/MISMATCH tables + verdict + Open Questions section.
   - `report/open_questions.json` (5 heavy-duty follow-on questions grounded in this run).
   - `report/workflow.md` (this file).
   - `report/artifacts_summary.md` (inventory).
   - `report/failure_analysis.md` (friction + gaps).

## Tools + versions
| tool         | version | source | note |
|--------------|---------|--------|------|
| Python       | 3.14    | system | Homebrew python3 |
| numpy        | 2.5.1   | PyPI   | installed into work/venv |
| scipy        | 1.18.0  | PyPI   | installed into work/venv |
| QuTiP        | 5.3.0   | PyPI   | primary simulation engine (Fock ops, coherent states) |
| pdftotext    | Poppler | system | -layout mode used for fallback extraction |
| curl         | system  | system | paper fetch |
| Argo (LLM)   | n/a     | localhost:44497 | NOT used (no LLM judge required — self-verdict) |

## Effort estimate
- Wallclock: ~15 min end-to-end (paper fetch + venv build + code + run + reports).
- Actual simulation runtime: <2 s.
- Human/agent-time equivalent: light — this is a small-instance-faithful, CPU-only
  reproduction of algebraic identities, not a resource-heavy training run.

## What was NOT done
- Universal-gate-set demo (in-line squeezing, teleportation-based two-cat CNOT).
- Metrology examples (Heisenberg-limited weak-force detection, Ramsey interferometry).
- Loss/decoherence channels.
- 3-judge Argo panel (self-verdict used per QC brief step 7 fallback).
