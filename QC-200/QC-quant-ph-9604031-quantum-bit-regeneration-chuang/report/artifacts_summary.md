# Artifacts inventory — QC-quant-ph-9604031

Full inventory of files in the replication tile, mapped to the mandatory
8-artifact bar (Rick 2026-07-05).

## 8 required artifacts

| # | Path | Purpose | Present? |
|---|---|---|---|
| 1 | `paper.pdf` | Original PDF from arXiv | ✅ 134 KB, 4 pages |
| 2 | `extraction/marker.md` | Marker parse (SURROGATE: PyMuPDF; see extraction/README.md) | ✅ 16 KB |
| 3 | `extraction/nougat.mmd` | Nougat parse (SURROGATE: pdftotext -layout; see extraction/README.md) | ✅ 22 KB |
| 4 | `report/REPORT.tex` | Detailed LaTeX report with verdict | ✅ 16 KB |
| 5 | `report/open_questions.json` | 5 heavy-duty open Qs {q,basis,next_steps} | ✅ + mirrored in REPORT.tex §Open Questions |
| 6 | `report/workflow.md` | Workflow, tool versions, work estimate | ✅ |
| 7 | `report/artifacts_summary.md` | This file | ✅ |
| 8 | `report/failure_analysis.md` | Honest failure analysis / gaps | ✅ |

## Additional artifacts (evidence + intermediates)

| Path | Description |
|---|---|
| `work/paper.pdf` | Original arXiv download (duplicate of `paper.pdf`) |
| `work/paper.txt` | `pdftotext -layout` skim (223 lines) |
| `extraction/README.md` | Surrogate-parser explanation |
| `report/evidence/repetition_code_sim.py` | Full simulator, ~350 lines, pure numpy |
| `report/evidence/repetition_code_results.json` | Full sweep results with theory + MC means + standard errors |
| `report/evidence/repetition_code_results.csv` | Same in CSV |
| `report/evidence/repetition_code_plot.png` | MC vs. theory plot |

## Traces (what was actually executed)

1. `curl -sL --max-time 60 -o work/paper.pdf https://arxiv.org/pdf/quant-ph/9604031`
   → 134 KB PDF.
2. `pdftotext -layout work/paper.pdf work/paper.txt` → 223 lines.
3. `python3 -c 'import fitz; ...'` → wrote `extraction/marker.md`.
4. Shell append → `extraction/nougat.mmd`.
5. `python3 report/evidence/repetition_code_sim.py` → 81.9 s wall-clock;
   wrote JSON+CSV+PNG.
6. Report + workflow + failure_analysis composed.

## Verdict summary (see REPORT.tex for full justification)

- **REPLICATED** for the paper's general operational claim (C4:
  redundancy + syndrome ⇒ p → 3p² − 2p³ scaling). All 4 tested p-values
  match theory within 1 SE.
- **SPOT-CHECK** for the paper's exact photonic dual-rail + balanced-QND
  protocol (C1–C3): mechanism verified by careful re-read of Eqs. 1–6,
  not numerically simulated (would require a QuTiP Lindblad model with
  Fock cutoff + cross-Kerr probe, out of scope for a QC-200 tile).
