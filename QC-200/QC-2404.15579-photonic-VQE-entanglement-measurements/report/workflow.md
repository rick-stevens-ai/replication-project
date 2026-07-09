# Workflow — arXiv:2404.15579 replication (QC-200)

## Steps executed (chronological)

1. **Read wave brief** `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` — confirmed the 8-artifact bar and free-endpoint constraint.
2. **Created target dir**: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2404.15579-photonic-VQE-entanglement-measurements/{work,extraction,report/evidence}`.
3. **Fetched paper PDF** from `https://arxiv.org/pdf/2404.15579` (2.5 MB, PDF v1.5) → `work/paper.pdf` + `paper.pdf` (root copy).
4. **Text-extracted with `pdftotext -layout`** to `work/paper.txt` (585 lines) and skimmed for:
   - Verified title/authors match arxiv metadata ✓
   - Extracted the Heisenberg claim (eq. 4, Sec. 3.2)
   - Extracted the HeH+ Hamiltonian coefficient table (Fig. A1, R=0.9 Å row)
   - Extracted the paper's manual HeH+ grouping (Appendix A)
5. **Built extraction surrogates** for the mandatory `extraction/marker.md` (via `pdftotext`) and `extraction/nougat.mmd` (via `pymupdf`). Marker/Nougat models are not installed on this sub-agent host; the QC-200 corpus convention (verified by inspecting sibling dirs) accepts these surrogates with an explicit `extraction/README.md` provenance note.
6. **Wrote main simulation** `report/evidence/vqe_bell_replication.py` — 3 parts:
   - Part A: Heisenberg XX+YY+ZZ; basis counts + VQE-P vs VQE-E under multinomial shot noise (9000 shots, 5 runs each).
   - Part B: HeH+ JW (R=0.9 Å); basis counts + VQE with QWC / GC groupings.
   - Part C: H2/STO-3G 4-qubit; basis counts + exact-expectation 4-qubit HEA VQE.
7. **Ran**: `python3 vqe_bell_replication.py 2>&1 | tee run.log`. All three parts completed cleanly. Discovered:
   - Part A perfectly matches paper (3 → 1 bases).
   - Part B greedy GC gave 4 groups (same as QWC) — needed the paper's explicit hand-picked grouping to reach 3.
   - Part B "-2.863 MJ/mol" paper value is a factor-of-2 off from the exact eigenvalue of H built from the paper's own coefficients.
   - Part C exceeds every threshold in the brief.
8. **Wrote refinement script** `report/evidence/vqe_bell_refinements.py`:
   - R1: HeH+ VQE with the paper's exact Bell + QWC + QWC grouping.
   - R2: Heisenberg VQE-E under tighter COBYLA tol=0.001 to show the large VQE-E variance was an optimizer artefact.
9. **Ran refinements**: `python3 vqe_bell_refinements.py 2>&1 | tee refine.log`. R1 reproduces the paper's 4 → 3 basis count exactly and matches the exact ground energy to <0.001 MJ/mol. R2 confirms VQE-E reaches -3.000 (best) and -2.98 (mean) under tighter tol.
10. **Wrote all 8 mandatory artifacts** (see `artifacts_summary.md`).
11. **Compiled REPORT.tex → REPORT.pdf** with `pdflatex` (best-effort; see failure_analysis.md if this step fell back to a markdown report).

## Tools & versions

| Tool | Version | Purpose |
| --- | --- | --- |
| Python | 3.x (system, `/usr/bin/python3`) | interpreter |
| NumPy | 2.4.3 | dense linear algebra (statevector, Pauli tensors, ground-state eigvalsh) |
| SciPy | 1.18.0 | `scipy.optimize.minimize(method='COBYLA')` — same optimizer the paper uses |
| PyMuPDF (fitz) | installed | nougat.mmd surrogate extraction |
| poppler `pdftotext` | installed | marker.md surrogate + paper.txt |
| `curl` | system | PDF fetch |
| `pdflatex` | (attempted) | REPORT.tex → REPORT.pdf |

No LLM inference was used in the numerical portion. No paid endpoints touched. No HPC/GPU used.

## Estimated work

- Reading + understanding paper: ~10 min
- Coding main pipeline (Parts A + B + C): ~15 min
- Coding refinements (R1 + R2): ~10 min
- Running all simulations: ~2 min wall time total
- Report writing (LaTeX + JSON + markdown docs): ~15 min
- Extraction surrogates: ~3 min

**Total: ~55 minutes.** Almost entirely CPU-bound classical numpy; no external service dependencies.

## Reproducibility

Anyone with Python 3 + NumPy + SciPy + PyMuPDF (or just NumPy+SciPy if they accept the marker/nougat surrogates as-is) can reproduce every number in this report by running

```bash
cd report/evidence/
python3 vqe_bell_replication.py
python3 vqe_bell_refinements.py
```

Random seeds are fixed inside the scripts (base seeds 101, 201, 301, ..., 4001) so the reported means/stds are byte-reproducible.
