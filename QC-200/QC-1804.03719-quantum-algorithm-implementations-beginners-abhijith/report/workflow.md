# Workflow — Abhijith et al. 1804.03719 replication

## Timeline (single subagent, 2026-07-05)

1. **Setup** — Created target dir `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1804.03719-quantum-algorithm-implementations-beginners-abhijith/` and skeleton `{work, extraction, report/evidence}`.
2. **Paper acquisition** — `curl` the arXiv PDF (`https://arxiv.org/pdf/1804.03719`) into `work/paper.pdf` (8.75 MB, 100+ pages). Copied to `paper.pdf` at repo root per the 8-artifact rule.
3. **Title/author verification** — `pdftotext -layout` on the PDF confirmed:
   - Title: **Quantum Algorithm Implementations for Beginners**
   - Authors: Abhijith J., Adetokunbo Adedoyin, John Ambrosiano, ..., Stephan Eidenbenz, Andreas Bärtschi, Patrick J. Coles, Marc Vuffray, Andrey Y. Lokhov (all Los Alamos National Laboratory; LA-UR-20-22353)
   - arXiv id 1804.03719v3 (27 Jun 2022 revision)
   - SCOUT's title-starts-with-"ABHIJITH" was a Marker-style front-matter bleed of the first author's given name — confirmed and flagged in Q5 of open questions.
4. **Environment** — Created Python 3.12.13 venv (Python 3.14 breaks the marker-pdf transitive numpy pin). Installed `qiskit==2.5.0`, `qiskit-aer`, `numpy==2.5.1`, `marker-pdf`.
5. **Three real Qiskit reproductions** — Wrote and ran three self-contained scripts (no code copied from the paper — implemented from scratch off the paper's algorithm descriptions):
   - `report/evidence/bv.py` — Bernstein-Vazirani, n=4, s=1011.
   - `report/evidence/grover.py` — Grover, N=8, single marked state |101>, k*=2 iterations.
   - `report/evidence/qpe.py` — QPE with t=4 counting qubits on a 1-qubit U with phi=1/8.
   Each script uses `qiskit.quantum_info.Statevector.from_instruction` (no shots, no noise, no fabricated numbers). All three matched paper predictions to double-precision (see `report/REPORT.tex` Section 4).
6. **Extraction** — `marker_single work/paper.pdf extraction/marker_out` kicked off in the background (Marker's first invocation downloads several hundred MB of layout+OCR+recognition models, then processes the 100+ page PDF on CPU — expected ~15-60 min wall). If Marker did not complete inside the wave time budget, `extraction/marker.md` falls back to a `pdftotext -layout` surrogate with clear provenance header. `extraction/nougat.mmd` is generated as a documented `pdftotext -layout` surrogate; Nougat is not installable on Darwin 25 + Python 3.12+ (torchvision SDK block), the same convention already adopted in the sibling QC-quant-ph-9709029 replication.
7. **Report** — Wrote `report/REPORT.tex` with paper summary, claims table (5 claims), method (per-algorithm), results-vs-paper table, verdict + justification, and 5 open questions. Attempted to compile with `pdflatex` if available (see failure_analysis.md).
8. **Reports** — Wrote `report/open_questions.json` (5 questions, each with `q`, `basis`, `next_steps`), `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Tools & versions
| Tool | Version | Where |
|---|---|---|
| Python | 3.12.13 | `venv/bin/python` |
| pip | latest | `venv/bin/pip` |
| qiskit | 2.5.0 | pip |
| qiskit-aer | latest | pip |
| numpy | 2.5.1 | pip |
| marker-pdf | latest 3.x | pip |
| pdftotext | Poppler | `/usr/local/bin` |
| curl | macOS 26 | `/usr/bin/curl` |

## Estimated work performed by this replication
- Paper read (targeted, Grover/BV/QPE sections + intro + table of contents): ~5 min.
- Environment setup (python3.12 venv, qiskit+marker install): ~4 min wall.
- Three Qiskit scripts written from scratch (BV/Grover/QPE): ~10 min.
- Running the three simulations end-to-end: <5 s wall combined.
- Marker parse launched in background (may or may not have finished inside the wave budget); nougat surrogate + hdr: <1 min.
- Report drafting (REPORT.tex + open_questions.json + workflow/artifacts_summary/failure_analysis): ~10 min.
- Total wall: ~30 min, no HPC/GPU used, CPU-only.
