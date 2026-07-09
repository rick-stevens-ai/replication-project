# Workflow — arXiv:2205.14225 replication

Wall-clock: ~15 minutes on CherryRd (macOS/Darwin 25.3.0, x86_64, Python 3.13).

## Tools and versions
| Tool | Version | Purpose |
|---|---|---|
| `curl` | system | fetch arXiv PDF |
| `pdftotext` (poppler) | system | extract paper text |
| `pdfinfo` (poppler) | system | verify title/authors/page count |
| `python3` | 3.13 | simulations |
| `numpy` | 2.4.3 | statevector / density-matrix math |
| `scipy` | 1.18.0 | `curve_fit` for the noise-parameter fit (paper's stated fitter) |
| `marker-pdf` | **not installed** | Marker parse — blocked by PEP-668 (`--break-system-packages` refused) |
| `nougat` | **not installed** | Nougat parse — same reason |

## Steps executed
1. Created target dir + subdirs `work/`, `extraction/`, `report/evidence/`.
2. `curl -sL https://arxiv.org/pdf/2205.14225 -o paper.pdf` (763 KB, 11 pages).
3. `pdfinfo paper.pdf` — verified title = *Characterizing and mitigating coherent errors in a trapped ion quantum processor using hidden inverses*; authors = Majumder, Yale, Morris, Lobser, Burch, Chow, Revelle, Clark, Pooser. **Task-brief mismatch spotted:** brief mentioned BB1/SK1/CORPSE, paper uses Hidden Inverses. Retargeted reproduction to actual paper claims.
4. `pdftotext paper.pdf work/paper.txt` — 1112 lines of readable text; used for section skims and key-number extraction.
5. Skimmed Sec 2 (HI theory), Sec 4 (noise model + fit), Sec 5 (VQE + MS budget). Extracted:
   - Fig 1 decomposition of H
   - Eq (1) parametric noise model
   - Sec 4.3 fit variance "~10^-4"
   - Sec 5.3 MS fidelities 97.5% / 91% / 89%
   - Table (Sec 5): raw 0.923 → HI 0.950 → HI-Pure 0.997
6. Wrote `report/evidence/sim_hidden_inverses.py` (267 lines): numpy-only implementation of X_noisy, Y_noisy, H_standard, H_hidden, MS_noisy, the 100-block phase-space builder, and the SciPy `curve_fit` noise-parameter fit.
7. Wrote `report/evidence/sim_hi_cancellation.py`: focused H·H vs H·H† suppression-order test.
8. Wrote `report/evidence/sim_rb_style.py`: interleaved-RB-style bench with exponential-decay fit.
9. Ran all three simulations (total <20 s):
   - `sim_hidden_inverses.py` → `results.json` (fit + MS budget)
   - `sim_hi_cancellation.py` → `results_hi_cancellation.json` (order + ratio)
   - `sim_rb_style.py` → `results_rb.json` (per-Clifford error rate)
10. Compiled the numerical outputs against the paper's headline numbers (see REPORT.tex Sec. "Results vs paper").
11. Wrote REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md.

## Work estimate
- Environment setup: 2 min (all deps already system-installed).
- Paper skim + claim extraction: 3 min.
- Code (3 files, ~450 lines total): 6 min.
- Runs + interpretation: 2 min.
- Report writeup: 4 min.
- Total: ~17 min.
