# Workflow — replication of arXiv:2306.16192

## 1. Ingest
- `pdftotext -layout paper.pdf paper.txt` (native text layer; no OCR/vision).
- Read abstract, Sec. II (model/Eq.1-2), Sec. III (phase diagram, FM, Eq.3),
  Appendix A 3 (single-magnon matrix Eq. A1), Appendix A 4 (two-magnon).

## 2. Classify + scope
- Assigned class = loop-current. Determined this is a **partial/adjacent** fit:
  a many-body SU(3) chiral spin-liquid model, not a tight-binding LC metal.
  The chiral `iK_I` term is the genuine TRS-breaking (loop-current-like) piece.
- Selected the **analytical single-magnon core** as the machine-checkable target
  (TSL/CSL tensor-network claims marked out-of-scope, not faked).

## 3. Kernel reuse
- Read `shared-kernels/loop_current_kagome_kernel.py`.
- Reused kagome geometry, reciprocal vectors, `bz_grid`, and the batched
  `eigvalsh`-over-BZ-grid pattern; reused the "imaginary hopping = broken TRS"
  concept (kernel `flux` -> paper `±iK_I`). See PROVENANCE.md.
- Specialised the 3×3 Bloch matrix to Eq. A1 in `code/magnon_su3_kagome.py`.

## 4. Implement checks (`code/run_checks.py`)
Five quantitative claims, all recomputed independently and compared:
1. FM energy `e_F = 2J+4K_R/3` over 2000 random sphere points.
2. q=0 magnon eigenvalues vs analytic `{0,−6(J+K_R)±2√3K_I}` over 3000 pts.
3. one-magnon instability line `J+K_R<−|K_I|/√3` via min-over-BZ magnon energy,
   scanned over a 61×41 (J+K_R,K_I) grid on a 90×90 BZ.
4. dispersion invariance under J/K_R split at fixed J+K_R.
5. flat 0-energy band on the boundary (bandwidth on vs off the line).

## 5. Performance fix
- First run (per-k Python loop, ~20M eigvalsh) hung >2.5 min. Killed it and
  **vectorised** `all_magnon_eigs` to batch-diagonalise the whole BZ stack.
  Full suite then finished in seconds. (See failure_analysis.md.)

## 6. Extra qualitative check (`code/plot_bands.py`)
- Γ-M-K-Γ magnon bands for stable/boundary/unstable cases.
- Flat-band eigenvector inter-sublattice phases probed → exactly ±π/3,
  confirming the paper's chiral hexagon-mode `e^{ijπ/3}` statement.

## 7. Artifacts
- Wrote `work/results.json`, `work/run_log.txt`, `work/magnon_bands.png`.
- Wrote report/ (REPORT.tex + PDF, open_questions.json, workflow.md,
  artifacts_summary.md, failure_analysis.md), extraction/marker.md, PROVENANCE.md.

## Reproduce
```
cd code
python3 -u run_checks.py     # -> ../work/results.json  (5/5 PASS)
python3 -u plot_bands.py     # -> ../work/magnon_bands.png
```
