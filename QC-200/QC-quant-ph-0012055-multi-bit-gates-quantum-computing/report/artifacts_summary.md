# Artifacts inventory — quant-ph/0012055 replication

All paths relative to `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/`.

## Required 8 artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Provenance |
|---|----------|------|--------|------------|
| 1 | Original PDF                | `paper.pdf`                                   | ✅ present (113 kB, 4 pages) | Fetched from `https://arxiv.org/pdf/quant-ph/0012055` on 2026-07-05 |
| 2 | Marker parse                | `extraction/marker.md`                        | ✅ present (fallback: pdftotext -layout + hand annotation) | Marker not installed on host; central corpus has no parsed copy |
| 3 | Nougat parse                | `extraction/nougat.mmd`                       | ✅ present (fallback: hand-lifted LaTeX/mmd) | Nougat not installed; central corpus has no parsed copy |
| 4 | LaTeX report                | `report/REPORT.tex`                           | ✅ present | Full section-by-section, claims table, results-vs-paper table, verdict. PDF compile attempted (see status) |
| 5 | Open questions              | `report/open_questions.json`                  | ✅ present | 5 heavy questions Q1–Q5, each `{q, basis, next_steps}` |
| 6 | Workflow                    | `report/workflow.md`                          | ✅ present | Tools + versions + time estimate + reproducibility commands |
| 7 | Artifacts summary           | `report/artifacts_summary.md`                 | ✅ present (this file) | |
| 8 | Failure analysis            | `report/failure_analysis.md`                  | ✅ present | Honest gaps + friction |

## Supplementary artifacts

| Path | Description |
|------|-------------|
| `code/wsm_toffoli.py`                          | Main QuTiP 5.3 simulation of Eq. (5). 288 LOC. |
| `code/toffoli_phase_and_gatecount.py`          | Toffoli-vs-CCNOT phase decomposition + Qiskit MCXGate transpile for gate counts. |
| `report/evidence/wsm_toffoli_results.json`     | 19 numerical cases (K x N_Fock x osc-state x thermal-n_bar) with F_avg, unitarity, leakage. |
| `report/evidence/toffoli_phase_and_gatecount.json` | Phase-relation numerics + Qiskit transpile counts for C^2-NOT, C^3-NOT. |
| `logs/run1.log`                                | Console log of `wsm_toffoli.py` run. |
| `logs/run2.log`                                | Console log of `toffoli_phase_and_gatecount.py` run. |
| `work/paper.txt`                               | `pdftotext -layout` dump of the paper (315 lines). |
| `venv/`                                        | Python 3.14 venv with QuTiP 5.3, Qiskit 2.5, NumPy 2.4.3, SciPy 1.18.0. Not needed for reading the report; drop if space-constrained. |

## Provenance traces

- **arXiv fetch:** `curl -sSL -o paper.pdf https://arxiv.org/pdf/quant-ph/0012055` at 2026-07-05T08:59 CDT. `file paper.pdf` → `PDF document, version 1.4, 4 pages`.
- **Central corpus check for pre-parsed marker/nougat:**
  - `find ~/Dropbox -maxdepth 5 -type d -name 'marker*' -o -name 'nougat*'` → 8 dirs found, but all for LUCID / virophage projects; **no** QC-100 or QC-200 corpus hit.
  - Decision: use `pdftotext -layout` fallback for both, clearly labeled in header.
- **Simulation reproducibility:** all commands documented in `workflow.md`. Total repo size ~150 kB. Simulations rerun in <5 seconds cold on a single CPU core.

## Cross-references

- `REPORT.tex` references all evidence JSON files and log files by relative path.
- `open_questions.json` items Q1–Q5 each cite the specific numerical evidence line (e.g. Q1 cites the leakage 1.4e-5 vs 7.7e-10 K-scaling row in the `wsm_toffoli_results.json` table).
- `failure_analysis.md` cross-references specific friction points (Marker/Nougat fallback, phase-convention subtlety).
