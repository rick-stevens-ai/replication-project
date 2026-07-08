# Artifacts summary — Fermi-Hubbard VQE

**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/W2-fermi-hubbard-vqe/`
**Paper:** Cade, Mineh, Montanaro, Stanisic (2020), arXiv:1912.06007.
**Verdict:** REPLICATED (strategy). Coverage 7/10, Agreement 10/10.

## On-disk artifacts

| Path | Kind | Role |
|---|---|---|
| `REPORT.md` | markdown | Original writeup (top-level; preserved in place). |
| `report/REPORT.tex` | LaTeX | Formal writeup for the QC-100 bundle. |
| `report/open_questions.json` | JSON | 5 open questions (machine-consumable). |
| `report/open_questions_section.tex` | LaTeX | Same questions as a report section. |
| `report/workflow.md` | markdown | End-to-end methods / environment / commands. |
| `report/artifacts_summary.md` | markdown | This file — asset manifest. |
| `report/failure_analysis.md` | markdown | Honest critique of scope + gaps. |
| `extraction/nougat.mmd` | mmd stub | Placeholder for future paper OCR extraction. |
| `code/replicate.py` | python | Clean-room HV-VQE implementation (numpy + scipy). |
| `results.json` | JSON | Per-(lattice, depth) results: params, error, fidelity. |
| `run.log` | text | Optimizer trace + per-run summary. |

## Key numbers reproduced
- 5 lattices covered: 1×2 (4q), 2×2 (8q), 1×4 (8q), 1×6 (12q), 2×3 (12q).
- Depth-monotone energy error confirmed on all five.
- Chemical-accuracy scale (≤ 1e-4 relative energy error) reached by depth 8 on both 12-qubit lattices.
- Parameter count exactly linear in depth (3/layer).

## Headline exercised?
**Yes** — the paper's core strategy claim (HV ansatz + non-interacting reference ⇒ depth-monotone convergence to chemical accuracy on small Fermi-Hubbard lattices) was independently reimplemented and quantitatively verified against exact diagonalization.

## What is *not* covered on disk
- No large-lattice (>12q) results.
- No noisy-simulator or hardware runs.
- No head-to-head baseline against HEA or ADAPT-VQE.
- No DMRG cross-check (exact diag sufficed at ≤12q).

## Provenance
Numerics + code by a subagent that timed out before writing prose. Results independently inspected from `results.json` and the markdown report was hand-written from those numbers on 2026-06-26. This LaTeX bundle assembled 2026-07-06.
